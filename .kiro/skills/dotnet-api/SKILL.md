---
name: dotnet-api
description: >
  .NET 8 Minimal API structure for ANTA projects: modules, features, requests, responses, endpoints.
  Trigger: When creating API endpoints, requests, responses, or project structure.
metadata:
  author: anta
  version: "2.0"
  scope: [root]
  auto_invoke: ".NET, API, endpoint, request, response, minimal API"
  phase: [inception, construction]
  layer: [backend]
  validates_with: validate_dotnet_handler
  validation_profile: build-unit
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Use `ApiResponse<TResponse>` with typed response | ALWAYS | Type safety |
| Use `ApiResponse<object>` | NEVER | Loses type information |
| Use `[AsParameters]` for list requests | ALWAYS | Proper binding |
| Put sort defaults in Handler, not Request | ALWAYS | Single source of truth |
| Use `[FromQuery(Name = "camelCase")]` | ALWAYS | API naming convention |
| Use `HeaderToken` for current user | ALWAYS | Context from Gateway |
| Endpoints are static classes with static `Map()` method | ALWAYS | Consistent pattern |
| SP constants class: `{Module}StoredProcedures.cs` | ALWAYS | Full module name, NOT abbreviated (e.g., `EmployeeStoredProcedures`, NOT `EmpStoredProcedures`) |
| Schema in SP class MUST match user's chosen schema | ALWAYS | If user chose `HR`, use `HR` — not `Emp`, `Empl` |
| Generate FluentValidation validators for Create/Update | ALWAYS | `{Action}{Entity}Validator.cs` in each feature folder. Register with `AddValidatorsFromAssemblyContaining` in Module |

---

## Project Structure

```
Modules/{Module}/
├── {Module}Module.cs
├── {Module}StoredProcedures.cs
├── Common/
│   └── DictionaryMappingHelper.cs
├── Shared/
│   ├── {Entity}QueryService.cs          // Reusable complex queries
│   ├── {Entity}DetailResponse.cs        // Shared response DTOs
│   └── {Entity}DetailMappingProfile.cs  // Shared mapping profiles
└── Features/{Entity}/
    ├── List{Entity}/
    │   ├── List{Entity}Endpoint.cs
    │   ├── List{Entity}Handler.cs
    │   ├── List{Entity}Request.cs
    │   ├── List{Entity}Response.cs
    │   ├── List{Entity}Validator.cs         // FluentValidation
    │   └── List{Entity}MappingProfile.cs    // Optional, for AutoMapper
    ├── Get{Entity}/
    ├── Create{Entity}/
    ├── Update{Entity}/
    └── Delete{Entity}/
```

Each feature folder follows the `{Action}{Entity}` prefix convention for all files.

---

## Endpoint Pattern

Endpoints are **static classes** with a static `Map(IEndpointRouteBuilder)` method and a private static `Handle` method.

### GET Endpoint (no validation)

```csharp
public static class Get{Entity}Endpoint
{
    public static void Map(IEndpointRouteBuilder app)
    {
        app.MapGet("/", Handle)
            .Produces<ApiResponse<Get{Entity}Response>>(StatusCodes.Status200OK)
            .ProducesProblem(StatusCodes.Status404NotFound)
            .ProducesProblem(StatusCodes.Status500InternalServerError)
            .WithSummary("Obtener {Entity}")
            .WithDescription("Obtiene informacion de {Entity} del usuario actual");
    }

    private static async Task<IResult> Handle(
        [FromServices] Get{Entity}Handler handler,
        [FromServices] HeaderToken headerToken,
        CancellationToken ct)
    {
        var currentUser = headerToken?.EmployeeId ?? throw new UnauthorizedAccessException("Usuario no autenticado");
        var result = await handler.HandleAsync(currentUser, ct);
        return Results.Ok(ApiResponse<Get{Entity}Response>.Ok(result, "Datos obtenidos exitosamente"));
    }
}
```

### PUT/POST Endpoint (with validation)

```csharp
public static class Update{Entity}Endpoint
{
    public static void Map(IEndpointRouteBuilder app)
    {
        app.MapPut("/", Handle)
            .WithValidation<Update{Entity}Request>()
            .Produces<ApiResponse<Update{Entity}Response>>(StatusCodes.Status200OK)
            .ProducesProblem(StatusCodes.Status400BadRequest)
            .ProducesProblem(StatusCodes.Status409Conflict)
            .ProducesProblem(StatusCodes.Status500InternalServerError)
            .WithSummary("Actualizar {Entity}")
            .WithDescription("Actualiza informacion de {Entity} del usuario actual");
    }

    private static async Task<IResult> Handle(
        Update{Entity}Request request,
        [FromServices] Update{Entity}Handler handler,
        [FromServices] HeaderToken headerToken,
        CancellationToken ct)
    {
        var currentUser = headerToken?.EmployeeId ?? throw new UnauthorizedAccessException("Usuario no autenticado");
        var result = await handler.HandleAsync(request, currentUser, currentUser, ct);
        return Results.Ok(ApiResponse<Update{Entity}Response>.Ok(result, "Datos actualizados exitosamente"));
    }
}
```

### Key Differences from Generic ANTA Pattern

- `HeaderToken.EmployeeId` is the user identifier propagated from Gateway middleware
- Use `throw new UnauthorizedAccessException("Usuario no autenticado")` instead of `?? "system"`
- Always include `.WithSummary()` and `.WithDescription()` for Swagger docs
- Messages in Spanish

---

## Request Binding

| Source | Pattern | Example |
|--------|---------|---------|
| Body | Automatic for POST/PUT | `Create{Entity}Request request` |
| Query | `[AsParameters]` on list request | `[AsParameters] List{Entity}Request request` |
| Route | Parameter name matches route template | `int {entityId}` (from `/{{entityId}}`) |
| Services | `[FromServices]` attribute | `[FromServices] Create{Entity}Handler handler` |
| Header | Via DI (middleware sets it) | `[FromServices] HeaderToken headerToken` |

### currentUser Extraction

Always extract from `HeaderToken` (injected by middleware from Gateway headers). `EmployeeId` is the authenticated user identifier:

```csharp
var currentUser = headerToken?.EmployeeId ?? throw new UnauthorizedAccessException("Usuario no autenticado");
```

> NEVER use `?? "system"` — always throw `UnauthorizedAccessException` if no user context.

---

## HTTP Method → Status Code Mapping

| Method | Success Code | Pattern |
|--------|-------------|---------|
| GET (single) | 200 | `Results.Ok(ApiResponse<T>.Ok(data))` |
| GET (wrapped) | 200 | `Results.Ok(ApiResponse.OkItem(data))` |
| GET (list) | 200 | `Results.Ok(ApiResponse.OkList(items, pagination))` |
| POST | 201 | `Results.Created(location, ApiResponse<T>.Ok(data, message))` |
| PUT | 200 | `Results.Ok(ApiResponse<T>.Ok(data, message))` |
| DELETE | 200 | `Results.Ok(ApiResponse<T>.Ok(data, message))` |

> **Note:** `OkItem<T>()` and `OkList<T>()` are on non-generic `ApiResponse`, not `ApiResponse<T>`. Use them for wrapped payloads (`ItemData<T>`, `ItemsData<T>`). See `dotnet-shared-libs` skill for full overloads.

---

## Module Pattern

```csharp
public static class {Module}Module
{
    public static IServiceCollection Add{Module}Module(this IServiceCollection services)
    {
        // Register handlers
        services.AddScoped<Get{Entity}Handler>();
        services.AddScoped<Update{Entity}Handler>();

        // Register validators (scans assembly for all validators)
        services.AddValidatorsFromAssemblyContaining<Update{Entity}Validator>();

        return services;
    }

    public static void Map{Module}Endpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/v1/{entity-path}")
            .WithTags("{Entity}");

        Get{Entity}Endpoint.Map(group);
        Update{Entity}Endpoint.Map(group);
    }
}
```

> Manual mapping from `dynamic` results is common. Register AutoMapper only when your module uses MappingProfiles.

---

## Request Pattern

```csharp
public class ListItemsRequest : IPagedRequest
{
    [FromQuery(Name = "page")] public int Page { get; set; }
    [FromQuery(Name = "pageSize")] public int PageSize { get; set; }
    [FromQuery(Name = "search")] public string? Search { get; set; }
    [FromQuery(Name = "sortBy")] public string? SortBy { get; set; }
    [FromQuery(Name = "sortOrder")] public string? SortOrder { get; set; }
}
```

---

## Response Pattern

Response classes use simple properties with `string.Empty` defaults for required strings and `?` for nullable:

```csharp
public class Get{Entity}Response
{
    // Required fields — string.Empty default
    public string EmployeeId { get; set; } = string.Empty;
    public string FirstName { get; set; } = string.Empty;
    public string LastName { get; set; } = string.Empty;

    // Nullable fields
    public string? Email { get; set; }
    public string? Phone { get; set; }
    public string? OrganizationalUnitCode { get; set; }
    public DateTime? ExpirationDate { get; set; }
}
```

### Response Structure

| Type | Structure |
|------|-----------|
| GET detail | `data: { item: {...} }` or flat response |
| GET list | `data: { items: [...] }` |
| POST create | `data: { item: {...} }` |
| PUT update | `data: { item: {...} }` or `data: { message: "..." }` |
| DELETE | `data: { id: int }` |

> For simple endpoints (like Get{Entity}), the response can be flat (no `item` wrapper) — the handler returns the response directly and the endpoint wraps it in `ApiResponse<T>.Ok(result, message)`.

---

## Validation (FluentValidation)

| Code | Description | Validate in |
|------|-------------|-------------|
| VAL_001 | Required field | API |
| VAL_002 | Invalid format | API |
| VAL_003 | Duplicate value | SP |
| VAL_004 | FK not exists | SP |
| VAL_007 | Out of range | API |
| VAL_008 | Length exceeded | API |

```csharp
RuleFor(x => x.Name)
    .NotEmpty().WithErrorCode("VAL_001").WithMessage("Name is required")
    .MaximumLength(500).WithErrorCode("VAL_008");
```

---

## Checklist

### Module
- [ ] `{Module}Module.cs` with `Add{Module}Module()` and `Map{Module}Endpoints()`
- [ ] `{Module}StoredProcedures.cs` with SP constants
- [ ] Register in `Program.cs`

### Request
- [ ] `[FromQuery(Name = "camelCase")]` for query params
- [ ] Implement `IPagedRequest` for lists
- [ ] Sort defaults in Handler, not Request

### Endpoint
- [ ] Static class with static `Map(IEndpointRouteBuilder)` method
- [ ] Private static `Handle` method
- [ ] `HeaderToken` for current user context
- [ ] `.WithPaginationDefaults()` for lists
- [ ] `.WithValidation<T>()` for create/update
- [ ] `[AsParameters]` for list Request
- [ ] Correct HTTP status code (201 for POST, 200 for GET/PUT/DELETE)

## Post-Creation Tasks

- [ ] Update `docs/API_CATALOG.md` (use `api-catalog` skill)
- [ ] Update `CHANGELOG.md` (use `changelog` skill)

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Endpoint templates (List, Get, Create) | [endpoint-templates.cs](assets/endpoint-templates.cs) |

## Related Skills

- **Handler Patterns**: `dotnet-handler`
- **Error/Pagination**: `dotnet-integration`
- **SP Patterns**: `database-sp`
