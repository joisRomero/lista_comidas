---
name: api-first-backend
description: >
  Generate backend code from OpenAPI spec: Stored Procedures, Handlers, Endpoints.
  DB-driven approach: SP first, then API layer.
  Trigger: When implementing backend from OpenAPI spec, generating SP from endpoints.
metadata:
  author: anta
  version: "3.0"
  scope: [root]
  enforcement: mandatory
  auto_invoke: "api first, openapi, swagger, generate backend, spec to code"
  phase: [construction]
  layer: [backend]
  validates_with: null
  validation_profile: null
---

## Workflow

```
OpenAPI Spec → Parse → SP (DB first) → Handler → DTOs → Endpoint
```

---

## Step 1: Parse OpenAPI Spec

Extract for each endpoint:
- Path, Method, OperationId
- Request body schema
- Response schema
- Path/Query parameters

---

## Step 2: Map to ANTA Patterns

| HTTP Method | Action | SP Prefix | Handler |
|-------------|--------|-----------|---------|
| `GET` (list) | List | `List{Entity}` | `List{Entity}Handler` |
| `GET` (single) | Get | `Get{Entity}` | `Get{Entity}Handler` |
| `POST` | Create | `Create{Entity}` | `Create{Entity}Handler` |
| `PUT` | Update | `Update{Entity}` | `Update{Entity}Handler` |
| `DELETE` | Delete | `Delete{Entity}` | `Delete{Entity}Handler` |
| `POST` (operation) | {Verb} | `{Verb}{Entity}` | `{Verb}{Entity}Handler` |
| `POST` (remove) | Remove | `Remove{SubEntity}` | `Remove{SubEntity}Handler` |
| `PUT` (reorder) | Reorder | `Reorder{SubEntities}` | `Reorder{SubEntities}Handler` |

**Operations** (state transitions via `POST /{id}/{verb}`): Use verb as SP prefix. Example: `POST /agendas/{id}/schedule` -> SP `ScheduleAgenda`, Handler `ScheduleAgendaHandler`.

**Sub-entities** (from `/entities/{id}/items`): Use `Add`/`Remove` instead of `Create`/`Delete`. Remove uses `POST /{subId}/remove` with justification body.

---

## Type Mapping

| OpenAPI Type | C# Type | SQL Type |
|--------------|---------|----------|
| `integer` | `int` | `INT` |
| `integer` (int64) | `long` | `BIGINT` |
| `number` | `decimal` | `DECIMAL(18,2)` |
| `string` | `string` | `NVARCHAR` |
| `string` (date) | `DateOnly` | `DATE` |
| `string` (date-time) | `DateTime` | `DATETIME2` |
| `boolean` | `bool` | `BIT` |

---

## Generation Order (DB-driven)

1. **SP first** - Database is source of truth
2. **SP Result class** - Maps SP output
3. **Handler** - Calls SP, maps to response
4. **Request/Response DTOs** - Match OpenAPI schema
5. **Endpoint** - Minimal API wrapper
6. **Validator** (optional) - FluentValidation

---

## SP Error Pattern

SPs return business errors via **SELECT** (not RAISERROR):

```sql
-- Validation/business errors → SELECT + RETURN
IF @Amount <= 0
BEGIN
    SELECT 'VAL_001' AS ErrorCode, 'Amount' AS Field, 'El monto debe ser mayor a 0' AS Message;
    RETURN;
END

-- System errors → TRY/CATCH
BEGIN CATCH
    EXEC Log.GetErrorInfo;
END CATCH
```

The handler uses `SpResultHelper.ThrowIfError()` to detect the error row and throw the appropriate exception (mapped to HTTP status by the middleware).

---

## Handler Pattern

Handlers use Dapper with **anonymous objects** for parameters, and `SpResultHelper.ThrowIfError()` for error detection:

```csharp
public class CreateEntityHandler(IDbConnection db)
{
    public async Task<CreateEntityResponse> Handle(CreateEntityRequest request, string currentUser)
    {
        var result = await db.QueryFirstOrDefaultAsync<CreateEntitySpResult>(
            EntityStoredProcedures.CreateEntity,
            new
            {
                ParamIName = request.Name,
                ParamIAmount = request.Amount,
                ParamICreationUser = currentUser
            },
            commandType: CommandType.StoredProcedure
        );

        SpResultHelper.ThrowIfError(result);

        return new CreateEntityResponse
        {
            EntityId = result.EntityId,
            Name = result.Name
        };
    }
}
```

### List Handler (Paginated)

List handlers read **2 result sets** using `QueryMultipleAsync`:

```csharp
public class ListEntitiesHandler(IDbConnection db)
{
    public async Task<ApiResponse<List<ListEntityResponse>>> Handle(ListEntitiesRequest request)
    {
        using var multi = await db.QueryMultipleAsync(
            EntityStoredProcedures.ListEntities,
            new
            {
                ParamIPage = request.Page,
                ParamIPageSize = request.PageSize,
                ParamISearch = request.Search,
                ParamISortBy = request.SortBy,
                ParamISortOrder = request.SortOrder
            },
            commandType: CommandType.StoredProcedure
        );

        var items = (await multi.ReadAsync<ListEntitySpResult>()).ToList();
        SpResultHelper.ThrowIfError(items);

        var pagination = await multi.ReadFirstOrDefaultAsync<PaginationResult>();

        return ApiResponse<List<ListEntityResponse>>.Ok(
            items.Select(MapToResponse).ToList(),
            pagination
        );
    }
}
```

---

## Dapper Parameters

**Always use anonymous objects** (not `DynamicParameters`):

```csharp
// ✅ Correct: Anonymous object
new
{
    ParamICaseId = request.CaseId,
    ParamIName = request.Name,
    ParamICreationUser = currentUser
}

// ❌ Wrong: DynamicParameters
var p = new DynamicParameters();
p.Add("ParamICaseId", request.CaseId);
```

---

## Endpoint Pattern

Endpoints use Minimal API with these conventions:

```csharp
public static class CreateEntityEndpoint
{
    public static RouteHandlerBuilder Map(RouteGroupBuilder group)
    {
        return group.MapPost("/", Handle)
            .WithValidation<CreateEntityRequest>()
            .WithName("CreateEntity")
            .Produces<ApiResponse<CreateEntityResponse>>(StatusCodes.Status201Created);
    }

    private static async Task<IResult> Handle(
        [FromBody] CreateEntityRequest request,
        [FromServices] CreateEntityHandler handler,
        [FromHeader(Name = "HeaderToken")] string currentUser)
    {
        var result = await handler.Handle(request, currentUser);
        return Results.Created($"/entities/{result.EntityId}", ApiResponse<CreateEntityResponse>.Ok(result));
    }
}
```

### Key Conventions

| Convention | Pattern |
|-----------|---------|
| Validation | `.WithValidation<T>()` for POST/PUT |
| Handler injection | `[FromServices]` |
| Current user | `[FromHeader(Name = "HeaderToken")]` |
| Success response | `ApiResponse<T>.Ok(data)` or `ApiResponse<T>.Ok(data, pagination)` |
| Created response | `Results.Created(uri, ApiResponse<T>.Ok(data))` |

---

## Operation Handler Pattern

Operations (state transitions) follow the same handler structure but with verb-based naming:

```csharp
public class {Verb}{Entity}Handler(IDbConnection db)
{
    public async Task<{Verb}{Entity}Response> Handle({Verb}{Entity}Request request, string currentUser)
    {
        var result = await db.QueryFirstOrDefaultAsync<{Verb}{Entity}SpResult>(
            {Module}StoredProcedures.{Verb}{Entity},
            new
            {
                ParamI{Entity}Id = request.{Entity}Id,
                ParamI{OptionalField} = request.{OptionalField},
                ParamIModificationUser = currentUser
            },
            commandType: CommandType.StoredProcedure
        );

        SpResultHelper.ThrowIfError(result);

        return new {Verb}{Entity}Response
        {
            {Entity}Id = result.{Entity}Id,
            Status = new StatusItem
            {
                MasterTableId = result.StatusId,
                Name = result.StatusName,
                Value = result.StatusValue
            }
        };
    }
}
```

### Operation Endpoint

```csharp
public static class {Verb}{Entity}Endpoint
{
    public static RouteHandlerBuilder Map(RouteGroupBuilder group)
    {
        return group.MapPost("/{entityId}/{verb}", Handle)
            .WithValidation<{Verb}{Entity}Request>()
            .WithName("{Verb}{Entity}")
            .Produces<ApiResponse<{Verb}{Entity}Response>>();
    }

    private static async Task<IResult> Handle(
        [FromRoute] int entityId,
        [FromBody] {Verb}{Entity}Request request,
        [FromServices] {Verb}{Entity}Handler handler,
        [FromHeader(Name = "HeaderToken")] string currentUser)
    {
        request.{Entity}Id = entityId;
        var result = await handler.Handle(request, currentUser);
        return Results.Ok(ApiResponse<{Verb}{Entity}Response>.Ok(result));
    }
}
```

**Common operations:**

| Operation | Verb | Request Body | SP Name |
|-----------|------|-------------|---------|
| Submit | submit | `{}` or optional | `Submit{Entity}` |
| Schedule | schedule | `{ actaNumber }` | `Schedule{Entity}` |
| Start | start | `{}` | `Start{Entity}` |
| Cancel | cancel | `{ reason? }` | `Cancel{Entity}` |
| End | end | `{}` | `End{Entity}` |
| Approve | approve | `{ notes? }` | `Approve{Entity}` |
| Reject | reject | `{ reason }` | `Reject{Entity}` |

---

## Checklist

For each endpoint in spec:

- [ ] SP created in `database/{Schema}/StoredProcedures/`
- [ ] SP errors via `SELECT ErrorCode, Field, Message` (not RAISERROR)
- [ ] SP constant added to `{Module}StoredProcedures.cs`
- [ ] Handler uses `SpResultHelper.ThrowIfError()` for error detection
- [ ] Handler uses anonymous objects for Dapper params (not DynamicParameters)
- [ ] Handler created in `Features/{Action}{Entity}/`
- [ ] Request DTO matches query/body params
- [ ] Response DTO matches spec schema
- [ ] Endpoint uses `.WithValidation<T>()` for POST/PUT
- [ ] Operation endpoints use verb-based naming (`{Verb}{Entity}Handler`)
- [ ] Operation SPs validate state preconditions before executing
- [ ] Remove endpoints use `POST /{subId}/remove` with justification body
- [ ] Endpoint uses `[FromServices]` for handler, `HeaderToken` for user
- [ ] Endpoint returns `ApiResponse<T>.Ok()` for responses
- [ ] Endpoint registered in `{Module}Module.cs`
- [ ] Validator added (for POST/PUT)

## Post-Generation Tasks

- [ ] Update `docs/API_CATALOG.md` (use `api-catalog` skill)
- [ ] Update `CHANGELOG.md` (use `changelog` skill)

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| SP, Handler, DTO, Endpoint templates | [generation-templates.md](assets/generation-templates.md) |

## Related Skills

| Task | Skill |
|------|-------|
| SP patterns | `database-sp` |
| Handler patterns | `dotnet-handler` |
| Endpoint patterns | `dotnet-api` |
| Validation, errors | `dotnet-integration` |
