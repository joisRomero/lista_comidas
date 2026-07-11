---
name: dotnet-shared-libs
description: >
  ANTA.Shared.* libraries configuration and usage patterns.
  Trigger: When configuring APIs, using shared libraries, setting up middleware, or handling exceptions.
metadata:
  author: anta
  version: "3.0"
  scope: [root]
  auto_invoke: "ANTA.Shared, AddAntamina, UseAntamina, shared library, middleware order, exception handling, validation, ApiResponse, PaginationResult, HeaderToken"
  phase: [inception, construction]
  layer: [backend]
  validates_with: validate_dotnet_deps
  validation_profile: build-unit
---

## Critical Rules
| Rule | Type | Rationale |
|------|------|-----------|
| Use `Action<Options>` pattern for configuration | ALWAYS | Fail-fast validation on startup |
| Order middleware correctly | ALWAYS | CorrelationId first, then validation/audit, then exception |
| Use typed exceptions for business errors | ALWAYS | Automatic HTTP mapping and consistent error contracts |
| Use UTC for all logging timestamps | ALWAYS | Distributed tracing consistency |
| Use `OkItem<T>/OkList<T>` from non-generic `ApiResponse` class | ALWAYS | Prevents wrong static call on `ApiResponse<T>` |

---

## Libraries Overview
| Library | Purpose | NuGet Package |
|---------|---------|---------------|
| `shared-common` | Base contracts: `ApiResponse`, exceptions, error codes, common helpers | `ANTA.Shared.Common` |
| `shared-common-api` | API contracts/utilities: `HeaderToken`, pagination contracts, Swagger helpers | `ANTA.Shared.Common.Api` |
| `shared-common-data` | Dapper infra, stores, resilient DB executor, SQL health checks | `ANTA.Shared.Common.Data` |
| `shared-common-logging` | Serilog + CloudWatch + CorrelationId middleware | `ANTA.Shared.Common.Logging` |
| `shared-common-inspection` | Exception middleware + audit HTTP middleware + endpoint audit handler | `ANTA.Shared.Common.Inspection` |
| `shared-common-validation` | FluentValidation registration + JSON validation + endpoint filters | `ANTA.Shared.Common.Validation` |
| `shared-happy` | Happy auth HTTP client + tracking headers + resilience + health checks | `ANTA.Shared.Happy` |
| `shared-storage` | S3 presigned URLs + storage service + rate limiting + health checks | `ANTA.Shared.Storage` |
| `shared-universal` | Universal gateway HTTP client + resilience + health checks | `ANTA.Shared.Universal` |
| `Mapping/` | Explicit mapping (`IMapper`, `IUpdater`) with registration validation | `ANTA.Shared.Common.Mapping` |
> NuGet version note: ANTA.Shared packages are currently stable at `1.0.0` unless a project pins newer versions.

---

## Dependency Chain
| Level | Libraries | Notes |
|------|-----------|-------|
| Level 0 | `shared-common`, `Mapping/` | Core contracts and mapping abstractions |
| Level 1 | `shared-common-api`, `shared-common-data`, `shared-common-validation`, `shared-common-logging` | Platform registration layer |
| Level 2 | `shared-common-inspection`, `shared-happy`, `shared-universal`, `shared-storage` | Runtime middleware and external integrations |
Guideline:
- Register Level 1 services before Level 2 middleware/clients.
- Start new APIs from `assets/program-template.cs`.

---

## Quick Configuration Reference

### Data Layer
Basic:
```csharp
builder.Services.AddAntaminaData(connectionString, stores =>
{
    stores.UseLogHttp();
    stores.UseAuditHttp();
    stores.UseAuditEndpoint();
    stores.UseLogJob();
});
```
With resilience overload:
```csharp
builder.Services.AddAntaminaData(connectionString, stores =>
{
    stores.UseLogHttp();
}, resilience => { resilience.RetryCount = 5; });
```
Available public overload families:
- `connectionString + configureStores`
- `connectionString + configureStores + configureResilience`
- `connectionString + connectionName + configureStores (+ optional resilience)`
- `IDbConnectionFactory + configureStores (+ optional resilience)`
- Legacy convenience: `connectionString` only and `IDbConnectionFactory` only
Store intent:
- `UseLogHttp()` -> exception logs
- `UseAuditHttp()` -> inbound request/response audit
- `UseAuditEndpoint()` -> outbound HTTP audit
- `UseLogJob()` -> worker/background logs

### Exception Handler
```csharp
builder.Services.AddAntaminaExceptionHandler(opt =>
{
    opt.ApplicationName = "ApiName";
    opt.SaveToDatabase = true;
});
```
Notes:
- `ApplicationName` is required.
- `SaveToDatabase` persists through `ILogHttpStore` when available.
- `MaxRequestBodySizeToBuffer` defaults to `65536` and controls buffered request-body size on exception capture.

### Logging
```csharp
SerilogExtensions.CreateBootstrapLogger(configuration);
builder.Host.UseAntaminaSerilog("ApiName", "/aws/Project", outputTemplate: null);
```
Notes:
- `UseAntaminaSerilog(applicationName, logGroupName, outputTemplate)` supports custom template.
- Default output includes `[{CorrelationId}]`.
- Call `SerilogExtensions.CloseLogger()` in `finally`.

### Validation
```csharp
builder.Services.AddAntaminaValidation(typeof(Program).Assembly);
app.UseJsonValidation();
app.MapPost("/v1/items", Handle).WithValidation<CreateItemRequest>();
```
Helpers:
- `ToApiErrors()` transforms validation failures to `List<ApiError>`.
- `ThrowIfInvalid()` throws validation exception from invalid result.

### Happy Auth
```csharp
builder.Services.AddAntaminaHappy(
    options => { options.Uri = "https://happy"; },
    tracking => { tracking.Enabled = true; });
```

### Universal
```csharp
builder.Services.AddAntaminaUniversal(options =>
{
    options.Uri = "https://universal/.../Comando/";
});
```

### Storage
```csharp
builder.Services.AddAntaminaStorage(
    s => configuration.Bind("S3Storage", s),
    StorageRateLimitLevel.Standard);
```
`StorageRateLimitLevel` quick table:
| Level | Value | Effective limit |
|------|-------|-----------------|
| `Disabled` | `0` | No limiter |
| `Low` | `1` | `50/min` per IP |
| `Standard` | `2` | `100/min` per IP |
| `High` | `3` | `200/min` per IP |
| `Critical` | `4` | `30/min` per IP |

### Mapping
```csharp
builder.Services.AddAntaminaMapping(typeof(Program).Assembly);
builder.Services.ValidateMappingRegistrations(typeof(Program).Assembly);
```

### Audit HTTP config
```csharp
builder.Services.AddAntaminaAuditHttp(opt =>
{
    opt.SaveToDatabase = true;
    opt.ExcludedPaths = ["swagger", "health", "favicon"];
});
```
Use with Gateway pipeline: `app.UseAntaminaAuditHttp();`

### Audit Endpoint config
```csharp
builder.Services.AddHttpClient("External")
    .AddAntaminaAuditEndpoint(opt => { opt.SaveToDatabase = true; });
```
Adds endpoint audit delegating handler; when enabled it also wires queue/background persistence.

---

## ApiResponse Pattern (CRITICAL REWRITE)
`ApiResponse<T>` core properties:
- `Success`, `Data`, `Message`, `Errors`, `Pagination`, `Metadata`

`ApiResponse<T>.Ok(...)` overloads (all):
```csharp
ApiResponse<T>.Ok(T data, string message = "Operación exitosa");
ApiResponse<T>.Ok(T data, PaginationResult pagination, string message = "Operación exitosa");
ApiResponse<T>.Ok(T data, Dictionary<string, object> metadata, string message = "Operación exitosa");
ApiResponse<T>.Ok(T data, PaginationResult pagination, Dictionary<string, object> metadata, string message = "Operación exitosa");
```
`ApiResponse<T>.Fail(...)` overloads:
```csharp
ApiResponse<T>.Fail(string message, List<ApiError> errors);
ApiResponse<T>.Fail(string message, ApiError error);
ApiResponse<T>.Fail(string code, string message, string? field = null);
```
CRITICAL CALLOUT:
- `OkItem<T>()` and `OkList<T>()` are on non-generic `ApiResponse`.
- Never call `ApiResponse<T>.OkItem` or `ApiResponse<T>.OkList`.

Non-generic wrappers:
```csharp
ApiResponse<ItemData<T>> ApiResponse.OkItem<T>(T item, string message = "Operación exitosa");
ApiResponse<ItemData<T>> ApiResponse.OkItem<T>(T item, Dictionary<string, object> metadata, string message = "Operación exitosa");
ApiResponse<ItemsData<T>> ApiResponse.OkList<T>(List<T> items, string message = "Operación exitosa");
ApiResponse<ItemsData<T>> ApiResponse.OkList<T>(List<T> items, PaginationResult pagination, string message = "Operación exitosa");
ApiResponse<ItemsData<T>> ApiResponse.OkList<T>(List<T> items, Dictionary<string, object> metadata, string message = "Operación exitosa");
ApiResponse<ItemsData<T>> ApiResponse.OkList<T>(List<T> items, PaginationResult pagination, Dictionary<string, object> metadata, string message = "Operación exitosa");
```
`ApiError` factory methods:
```csharp
new ApiError(string code, string message, string? field = null);
ApiError.Validation(string code, string field, string message);
ApiError.General(string code, string message);
```
Quick usage:
```csharp
return ApiResponse.OkItem(dto);
return ApiResponse.OkList(items, pagination);
return ApiResponse<ContractDto>.Fail("CON_001", "Contrato no encontrado", "contractId");
```

---

## Pagination
`PaginationResult` properties:
- `Page`, `PageSize`, `TotalRecords`, `TotalPages`, `HasNext`, `HasPrevious`
Factory:
```csharp
var pagination = PaginationResult.Create(page, pageSize, totalRecords);
```
`IPagedRequest` (5 properties):
- `Page`
- `PageSize`
- `Search`
- `SortBy`
- `SortOrder`
Endpoint filter:
```csharp
app.MapGet("/v1/items", Handle)
   .WithPaginationDefaults(maxPageSize: 100);
```
Behavior:
- Requires `Page > 0` and `PageSize > 0`.
- Caps `PageSize` to `maxPageSize`.
- Defaults and uppercases `SortOrder` (`DESC`).
- Normalizes blank `Search` and `SortBy` to `null`.

---

## Error Handling
Exception hierarchy:
| Exception | HTTP | Usage |
|-----------|------|-------|
| `ValidationException` | 400 | Input and business validation failures |
| `ForbiddenException` | 403 | Authorization and permission failures |
| `NotFoundException` | 404 | Resource not found |
| `ConflictException` | 409 | Duplicate or state conflict |
| `BusinessRuleException` | 422 | Business rule violation |
| `BadGatewayException` | 502 | Downstream service failure |

Error code prefixes:
| Prefix | HTTP | Category |
|--------|------|----------|
| `VAL_` | 400 | Validation/input |
| `{MOD}_001` | 404 | Not found |
| `{MOD}_002` | 409 | Conflict |
| `{MOD}_003+` | 422 | Business rule |
| `AUTH_` | 403 | Authorization |
| `SYS_` | 500 | System/internal |

`CommonErrorCodes` (18 constants):
- `VAL_`: `VAL_001`, `VAL_002`, `VAL_003`, `VAL_004`, `VAL_005`, `VAL_006`, `VAL_007`, `VAL_008`
- `AUTH_`: `AUTH_001`, `AUTH_002`, `AUTH_003`
- `PERM_`: `PERM_001`, `PERM_002`
- `SYS_`: `SYS_001`, `SYS_002`, `SYS_003`, `SYS_004`
- `FILE_`: `FILE_001`, `FILE_002`, `FILE_003`

`SpResultHelper` quick reference:
```csharp
SpResultHelper.ThrowIfError(firstRow);
```
Behavior:
- Reads SP first-row dictionary shape and checks `ErrorCode`.
- No-op if row does not match error shape.
- Throws typed exception by code pattern.
Mapping table:
| Error pattern | Exception type |
|---|---|
| `VAL_*` | `ValidationException` |
| `AUTH_*` | `ForbiddenException` |
| `SYS_*` | `BusinessException` |
| `*_001` | `NotFoundException` |
| `*_002` | `ConflictException` |
| default (`*_003+` and others) | `BusinessRuleException` |

---

## Cross-cutting Models
`BaseAuditableEntity` (5):
- `RecordCreationUser`
- `RecordCreationDate`
- `RecordEditUser`
- `RecordEditDate`
- `RecordStatus`
`MasterTable` (6):
- `MasterTableId`
- `Name`
- `Value`
- `AdditionalOne`
- `AdditionalTwo`
- `AdditionalThree`
Wrapper pattern:
- `ItemData<T>` for single-item responses (`Item`)
- `ItemsData<T>` for list responses (`Items`)
`DocumentMetadataDto` (5):
- `FileName`
- `FileExtension`
- `FileSizeKB`
- `FilePath`
- `ContentType`
`DictionaryExtensions`:
```csharp
dict.GetValue<T>("Key");
dict.GetValueOrDefault<T>("Key", defaultValue);
```
`IValidatableOptions` contract:
```csharp
public interface IValidatableOptions { void Validate(); }
```

---

## HeaderToken
Key properties:
- `Token`
- `Profile`
- `Email`
- `EmployeeId`
- `CodTra`
- `AuthorityLevel`
Notes:
- `HeaderToken : EmployeeDataBase, IHeaderToken`.
- Inherits 40+ properties from `EmployeeDataBase` (employee identity, hierarchy, org metadata).
- Full property list is in `assets/api-common-models.md`.

---

## Middleware Order (CRITICAL)
```csharp
app.UseSwagger();
app.UseSwaggerUI();
app.UseCorrelationId();
app.UseJsonValidation();
app.UseAntaminaAuditHttp();
app.UseAntaminaExceptionHandler();
app.UseRateLimiter();
app.MapEndpoints();
app.MapHealthChecks("/health");
```
Order notes:
- Swagger before operational chain.
- `UseCorrelationId()` first.
- `UseJsonValidation()` before exception handling.
- `UseAntaminaAuditHttp()` Gateway-only.
- `UseAntaminaExceptionHandler()` wraps endpoint execution errors.

---

## Store Selection by API Type
| API Type | Stores to enable | Why |
|---|---|---|
| Internal API | `UseLogHttp().UseAuditHttp()` | API exception and request traceability |
| Gateway | `UseLogHttp().UseAuditHttp().UseAuditEndpoint()` | Adds outbound endpoint audit |
| Worker | `UseLogHttp().UseLogJob()` | Background execution observability |

---

## Health Checks
```csharp
builder.Services.AddHealthChecks()
    .AddSqlServerHealthCheck()
    .AddHappyServiceHealthCheck(tags: ["external"])
    .AddUniversalServiceHealthCheck(tags: ["external"])
    .AddS3StorageHealthCheck();
```
```csharp
app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = HealthCheckResponseWriter.WriteResponse
});
```
Notes:
- Register only checks used by the API.
- Add `AddUniversalServiceHealthCheck()` when Universal client is configured.

---

## Conventions & Anti-Patterns
Conventions:
- Use explicit options + `Validate()` in all `AddAntamina*` registrations.
- Keep response contracts standardized with `ApiResponse`.
- Normalize validation errors through shared `ApiError`.
- Keep middleware order deterministic across services.
Anti-patterns:
- Never use `ApiResponse<T>.OkItem` or `ApiResponse<T>.OkList`; use `ApiResponse.OkItem<T>` and `ApiResponse.OkList<T>`.
- Do not enable Gateway audit middleware in internal APIs by default.
- Do not bypass `SpResultHelper.ThrowIfError()` when consuming SP first-row contracts.

---

## Checklist
### Base Registration
- [ ] Start from `assets/program-template.cs` for new APIs
- [ ] `SerilogExtensions.CreateBootstrapLogger()` before service build
- [ ] `UseAntaminaSerilog(applicationName, logGroupName, outputTemplate?)`
### Data Layer
- [ ] Choose the correct `AddAntaminaData()` overload
- [ ] Enable stores by API type (Internal/Gateway/Worker)
- [ ] Tune resilience options when needed
- [ ] Enforce `SpResultHelper.ThrowIfError()` in handlers
### Inspection + Middleware
- [ ] `AddAntaminaExceptionHandler()` with `ApplicationName`
- [ ] Review `MaxRequestBodySizeToBuffer`
- [ ] `UseCorrelationId()` first in chain
- [ ] `UseJsonValidation()` before exception handler
- [ ] `UseAntaminaAuditHttp()` only when required
### HTTP Clients
- [ ] Configure `AddAntaminaHappy(...)` when Happy is used
- [ ] Configure `AddAntaminaUniversal(...)` when Universal is used
- [ ] Add `AddAntaminaAuditEndpoint(...)` on outbound `HttpClient` when audit is required
### Response + Pagination
- [ ] Use correct `ApiResponse<T>.Ok(...)` overload
- [ ] Use `ApiResponse.OkItem<T>()` and `ApiResponse.OkList<T>()` for wrapper payloads
- [ ] Apply `.WithPaginationDefaults(maxPageSize)` to paged endpoints
### Mapping + Validation
- [ ] `AddAntaminaMapping(...)` + `ValidateMappingRegistrations(...)`
- [ ] Validation registration + middleware + endpoint filters in place
- [ ] Validation failures converted to shared `ApiError`
### Health + Runtime
- [ ] Register health checks only for active dependencies
- [ ] `MapHealthChecks("/health")` with `HealthCheckResponseWriter.WriteResponse`
- [ ] Call `SerilogExtensions.CloseLogger()` in `finally`

---

## Detailed Documentation (Asset Index)
| Topic | Asset | When to Load |
|-------|-------|-------------|
| Complete Program.cs template | `program-template.cs` | Starting new API |
| Resilience & fallback patterns | `resilience-config.md` | Configuring Polly |
| ApiResponse, errors, models, HeaderToken | `api-common-models.md` | Implementing endpoints/responses |
| Data layer, stores, SpResultHelper | `api-data-resilience.md` | Configuring data access |
| Middleware, audit, logging, CorrelationId | `api-middleware-audit.md` | Setting up middleware pipeline |
| Happy + Universal HTTP clients | `api-http-clients.md` | Configuring Gateway clients |
| S3 Storage, rate limiting | `api-storage.md` | Implementing file upload/download |
| Mapping: IMapper, IUpdater, Converters | `api-mapping.md` | Implementing explicit mappers |
Asset path prefix for links in this skill: `assets/{file}`.

---

## Related Skills
- **Startup patterns**: `dotnet-startup`
- **Exception to HTTP mapping**: `dotnet-integration`
- **SP error handling**: `database-sp`
