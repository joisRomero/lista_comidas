---
name: dotnet-handler
description: >
  Handler patterns for ANTA .NET APIs: Dapper, SP calls, mapping, error handling.
  Trigger: When implementing handlers, calling stored procedures, or mapping results.
metadata:
  author: anta
  version: "3.0"
  scope: [root]
  auto_invoke: "handler, Dapper, PaginationResult, mapping, SpResultHelper, GetValue"
  phase: [construction]
  layer: [backend]
  validates_with: validate_dotnet_handler
  validation_profile: build-unit
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Call `SpResultHelper.ThrowIfError()` after reading SP | ALWAYS | Proper error handling |
| Use `QueryAsync` for simple lists; `QueryMultipleAsync` only for sub-collections | ALWAYS | Simple lists use one ResultSet with `COUNT(*) OVER()` |
| Return tuple `(Data, Pagination)` for lists | ALWAYS | Consistent pattern |
| Use `CommandDefinition` with `CancellationToken` | ALWAYS | Proper async handling |
| Set sort defaults in Handler | ALWAYS | Single source of truth |
| Pass `currentUser` to handlers | ALWAYS | Audit trail |
| Use module-specific `{Module}StoredProcedures` | ALWAYS | Schema-prefixed SP names |
| Use anonymous objects for Dapper params | ALWAYS | No DynamicParameters — SPs return results via SELECT |
| No interface for handlers | ALWAYS | Concrete class with constructor injection |

---

## Handler Class Pattern

Handlers are **concrete classes** — no interface. Use constructor injection for dependencies and register with `services.AddScoped<XxxHandler>()`.

```csharp
public class Get{Entity}Handler
{
    private readonly IDbConnection _db;

    public Get{Entity}Handler(IDbConnection db)
    {
        _db = db;
    }

    public async Task<Get{Entity}Response> HandleAsync(string employeeId, CancellationToken ct = default)
    {
        var command = new CommandDefinition(
            {Entity}StoredProcedures.Get{Entity},
            new { ParamIEmployeeId = employeeId },
            commandType: CommandType.StoredProcedure,
            cancellationToken: ct
        );

        var result = await _db.QuerySingleAsync<dynamic>(command);
        SpResultHelper.ThrowIfError(result);
        var dict = (IDictionary<string, object>)result;

        return new Get{Entity}Response
        {
            EmployeeId = dict.GetValue<string>("EmployeeId") ?? string.Empty,
            FirstName = dict.GetValue<string>("FirstName") ?? string.Empty,
            LastName = dict.GetValue<string>("LastName") ?? string.Empty,
            Email = dict.GetValue<string>("Email"),
            Phone = dict.GetValue<string>("Phone"),
            ContactPhone = dict.GetValue<string>("ContactPhone"),
        };
    }
}
```

> Use manual mapping as default for `dynamic` results. When your project uses MappingProfiles, inject `IMapper` in list/detail handlers.

### Value Extraction: 2-Layer Pattern

**Layer 1 — Access (shared library):** Use `DictionaryExtensions.GetValue<T>()` from `ANTA.Shared.Common.Extensions` for all value extraction from Dapper dynamic results. Never reimplement null/DBNull checking.

```csharp
using ANTA.Shared.Common.Extensions;

// Instead of: (string)result.Name or result.Name != null ? (string)result.Name : null
var dict = (IDictionary<string, object>)result;
var name = dict.GetValue<string>("Name") ?? string.Empty;   // non-nullable string
var email = dict.GetValue<string>("Email");                   // nullable string
var age = dict.GetValue<int?>("Age");                         // nullable int
var amount = dict.GetValue<decimal?>("Amount") ?? 0m;         // nullable with default
```

**Layer 2 — Domain mapping (project-level):** Create a `DictionaryMappingHelper` for composite objects that reuses `GetValue<T>()` internally:

```csharp
using ANTA.Shared.Common.Extensions;

public static class DictionaryMappingHelper
{
    // Composite mapper for prefixed keys (e.g., "CurrentStatus.MasterTableId")
    public static MasterTable? MapMasterTable(IDictionary<string, object> dict, string prefix)
    {
        var id = dict.GetValue<int?>($"{prefix}.MasterTableId");
        if (id == null) return null;

        return new MasterTable
        {
            MasterTableId = id.Value,
            Name = dict.GetValue<string>($"{prefix}.Name") ?? string.Empty,
            Value = dict.GetValue<string>($"{prefix}.Value") ?? string.Empty,
            AdditionalOne = dict.GetValue<string>($"{prefix}.AdditionalOne"),
            AdditionalTwo = dict.GetValue<string>($"{prefix}.AdditionalTwo")
        };
    }
}
```

> **Anti-pattern:** Never create custom `GetString()`/`GetNullableString()` methods — `GetValue<T>()` already handles null, DBNull, and type conversion generically.

---

## Handler Types Quick Reference

| Type | Dapper Method | Returns | Use Case |
|------|---------------|---------|----------|
| List | `QueryAsync` | `(Response, PaginationResult)` | Paginated lists (TotalCount via COUNT(*) OVER()) |
| List + Sub-collections | `QueryMultipleAsync` | `(Response, PaginationResult)` | List with nested data (e.g., agendas + cases) |
| Get | `QuerySingleAsync` or `QueryMultipleAsync` | `Response` | Single item, or detail with sub-collections |
| Create | `QuerySingleAsync` | `Response` | Single row result |
| Update | `QuerySingleAsync` | `Response` | Single row result |
| Delete | `QuerySingleAsync` | `Response` | Returns ID confirmation |

---

## Handler Structure

```csharp
public class {Action}{Entity}Handler
{
    private readonly IDbConnection _db;

    public {Action}{Entity}Handler(IDbConnection db)
    {
        _db = db;
    }

    public async Task<{Response}> HandleAsync(
        {Request} request, string currentUser, CancellationToken ct = default)
    {
        var command = new CommandDefinition(
            {Module}StoredProcedures.{Action}{Entity},
            new { /* params */ },
            commandType: CommandType.StoredProcedure,
            cancellationToken: ct
        );

        // See handler types below for Dapper method
    }
}
```

### Manual Mapping Pattern

Map from `dynamic` result to typed Response using `DictionaryExtensions.GetValue<T>()`:

```csharp
var dict = (IDictionary<string, object>)result;

// Required field — GetValue with null coalescing
EmployeeId = dict.GetValue<string>("EmployeeId") ?? string.Empty,

// Nullable field — GetValue returns null by default
Email = dict.GetValue<string>("Email"),
Phone = dict.GetValue<string>("Phone"),
ExpirationDate = dict.GetValue<DateTime?>("ExpirationDate"),

// Nested MasterTable — use DictionaryMappingHelper for prefixed keys
BookingStatus = DictionaryMappingHelper.MapMasterTable(dict, "BookingStatus"),
```

---

## Dapper Parameters

**Always use anonymous objects** for SP parameters. This codebase does NOT use `DynamicParameters` — SPs return results via SELECT (no OUTPUT params needed).

```csharp
var command = new CommandDefinition(
    {Module}StoredProcedures.Create{Entity},
    new {
        ParamI{Entity}Id = request.Id,
        ParamI{Entity}Name = request.Name,
        ParamIDescription = request.Description,
        ParamIRecordCreationUser = currentUser
    },
    commandType: CommandType.StoredProcedure,
    cancellationToken: ct
);
```

### JSON Parameters

For complex nested data, serialize to JSON and pass as `NVARCHAR(MAX)`. The SP then uses `OPENJSON` to parse:

```csharp
var casesJson = JsonSerializer.Serialize(request.Cases, JsonSerializerOptionsProvider.Default);

var command = new CommandDefinition(
    {Module}StoredProcedures.Create{Entity},
    new {
        ParamICasesJson = casesJson,
        ParamIRecordCreationUser = currentUser
    },
    commandType: CommandType.StoredProcedure,
    cancellationToken: ct
);
```

---

## Handler with In-Code Validation

Handlers can throw `ValidationException` for checks that don't fit FluentValidation (e.g., parsing, cross-field logic):

```csharp
public async Task<CreateSessionResponse> HandleAsync(
    CreateSessionRequest request, string currentUser, CancellationToken ct = default)
{
    if (!TimeSpan.TryParse(request.ScheduledTime, out _))
        throw new ValidationException(CommonErrorCodes.VAL_002, "Formato de hora inválido", "scheduledTime");

    var command = new CommandDefinition(/* ... */);
    // ...
}
```

> Use `CommonErrorCodes.VAL_002` (invalid format) for parsing failures. FluentValidation handles required/length/range; handler validates semantic correctness.

---

## Delete Handler Pattern

Delete handlers return an ID confirmation response (not `void`):

```csharp
public async Task<Delete{Entity}Response> HandleAsync(
    int {entityId}, string currentUser, CancellationToken ct = default)
{
    var command = new CommandDefinition(
        {Module}StoredProcedures.Delete{Entity},
        new { ParamI{Entity}Id = {entityId}, ParamIRecordCreationUser = currentUser },
        commandType: CommandType.StoredProcedure,
        cancellationToken: ct
    );

    var result = await _db.QuerySingleAsync<dynamic>(command);
    SpResultHelper.ThrowIfError(result);
    return new Delete{Entity}Response { {Entity}Id = (int)result.{Entity}Id };
}
```

---

## StoredProcedures Constants

Each module has `{Module}StoredProcedures.cs` with `private const string Schema`:

```csharp
namespace {ProjectName}.Api.Modules.{Module};

public static class {Entity}StoredProcedures
{
    private const string Schema = "Employees";

    public const string Get{Entity} = $"{Schema}.Get{Entity}";
    public const string Update{Entity} = $"{Schema}.Update{Entity}";
}
```

> Use `private const string Schema` (not `public const string schema`).

---

## SpResultHelper Error Mapping

| SP Code | Exception | HTTP |
|---------|-----------|------|
| `VAL_*` | ValidationException | 400 |
| `{MOD}_001` | NotFoundException | 404 |
| `{MOD}_002` | ConflictException | 409 |
| `{MOD}_003+` | BusinessRuleException | 422 |
| `AUTH_*` | ForbiddenException | 403 |
| `SYS_*` | BusinessException | 500 |

```csharp
// After every SP call
SpResultHelper.ThrowIfError(result.FirstOrDefault());
```

---

## Mapping Patterns

Use two complementary mapping approaches depending on module complexity:

| Scenario | Pattern | Location |
|----------|---------|----------|
| Create/Update/Delete and simple queries | Manual mapping from `dynamic` | In handler |
| List/Get with many fields | MappingProfile + `IMapper` | Handler + MappingProfile |
| Shared reusable mapping helpers | `DictionaryMappingHelper` | `Modules/{Module}/Common` |

### Nullable Field Mapping

```csharp
var dict = (IDictionary<string, object>)result;

// String nullable — returns null if missing/DBNull
Email = dict.GetValue<string>("Email"),

// DateTime nullable
ExpirationDate = dict.GetValue<DateTime?>("ExpirationDate"),

// Int nullable
ClinicId = dict.GetValue<int?>("ClinicId"),
```

### Nested Object Mapping (MasterTable)

When SP uses dot notation aliases like `bs.MasterTableId AS [BookingStatus.MasterTableId]`, Dapper returns flat properties. Use `DictionaryMappingHelper`:

```csharp
// SP returns: BookingStatus.MasterTableId, BookingStatus.Name, BookingStatus.Value
// In C# handler, use the composite mapper:
BookingStatus = DictionaryMappingHelper.MapMasterTable(dict, "BookingStatus"),
```

---

## Shared Query Service

When 2+ endpoints need same complex query, extract to a shared service:

```csharp
// Modules/{Module}/Shared/{Entity}QueryService.cs
public class {Entity}QueryService
{
    private readonly IDbConnection _db;
    private readonly IMapper _mapper;

    public {Entity}QueryService(IDbConnection db, IMapper mapper)
    {
        _db = db;
        _mapper = mapper;
    }

    public async Task<{Entity}DetailResponse> Get{Entity}DetailAsync(int id, CancellationToken ct)
    {
        // Complex multi-ResultSet query shared by Get{Entity}, Process{Entity}, etc.
    }
}

// Register: services.AddScoped<{Entity}QueryService>();
```

Used when Get{Entity} and other endpoints (e.g., Process{Entity}, Return{Entity}) need the same detail query.

---

## Nested Resource Validation

For `DELETE /items/{itemId}/details/{detailId}`:

```csharp
// Pass both IDs to SP - SP validates ownership
new { ParamIItemId = itemId, ParamIDetailId = detailId, ParamICurrentUser = currentUser }
```

---

## Checklist

- [ ] `SpResultHelper.ThrowIfError()` after every SP call
- [ ] `QueryAsync` for simple lists, `QueryMultipleAsync` only for sub-collections
- [ ] `QuerySingleAsync` for single-row results
- [ ] Sort defaults in CommandDefinition
- [ ] Tuple `(Data, Pagination)` for lists
- [ ] `currentUser` passed from endpoint
- [ ] Module-specific `{Module}StoredProcedures` constants
- [ ] MappingProfile for List/Get, DictionaryMappingHelper for Create/Update
- [ ] Null-check for nested MasterTable/StatusItem
- [ ] Anonymous objects for params (not DynamicParameters)
- [ ] JSON serialization for complex nested data passed to SP
- [ ] Handler-level validation for non-FluentValidation checks

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Handler templates (List, Get, Create) | [handler-templates.md](assets/handler-templates.md) |
| Mapping patterns (Profile, Helper) | [mapping-patterns.md](assets/mapping-patterns.md) |

## Related Skills

- **Endpoint Patterns**: `dotnet-api`
- **SP Patterns**: `database-sp`
- **Error/Pagination/Validation**: `dotnet-integration`
