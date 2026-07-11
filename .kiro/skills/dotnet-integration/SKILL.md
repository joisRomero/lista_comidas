---
name: dotnet-integration
description: >
  SP to API integration patterns: error mapping, pagination, validation, response structure.
  Trigger: When connecting stored procedures to .NET APIs, handling SP errors, or implementing pagination.
metadata:
  author: anta
  version: "2.0"
  scope: [root]
  auto_invoke: "SP error, ApiResponse, pagination, SpResultHelper, FluentValidation"
  phase: [construction]
  layer: [backend]
  validates_with: validate_dotnet_handler
  validation_profile: build-unit
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Use `SpResultHelper.ThrowIfError()` after reading SP | ALWAYS | Consistent error handling |
| Use `ApiResponse<T>` with typed response | ALWAYS | Never `ApiResponse<object>` |
| Validate in API: format, required, length | ALWAYS | Fast fail before DB |
| Validate in SP: duplicates, FK, business rules | ALWAYS | Data integrity |
| Use `.WithPaginationDefaults()` for list endpoints | ALWAYS | Consistent pagination |

---

## ApiResponse Structure

### Data Structure by Endpoint Type

| Endpoint Type | Data Structure | Response Class |
|---------------|----------------|----------------|
| GET detail | `{ item: {...} }` | `{Action}Response { Item }` |
| GET list | `{ items: [...] }` | `{Action}Response { Items }` |
| POST create | `{ item: {...} }` | `{Action}Response { Item }` |
| PUT update | `{ item: {...} }` | `{Action}Response { Item }` |
| DELETE | `{ {entity}Id: int }` | `{Action}Response { {Entity}Id }` |

### ApiResponse Class

The `errors` field is `List<ApiError>?` (array, not single object). Includes optional `Metadata`:

```csharp
public class ApiResponse<T>
{
    public bool Success { get; set; }
    public T? Data { get; set; }
    public string Message { get; set; }
    public List<ApiError>? Errors { get; set; }
    public PaginationResult? Pagination { get; set; }
    public Dictionary<string, object>? Metadata { get; set; }
}
```

### Factory Methods

| Method | Use | Example |
|--------|-----|---------|
| `Ok(data, message)` | Simple response | GET detail, POST, PUT, DELETE |
| `Ok(data, pagination, message)` | With pagination | GET lists |
| `Fail(message, errors)` | Error with list | Validation failed |

---

## Pagination

### IPagedRequest Interface

```csharp
public interface IPagedRequest
{
    int Page { get; set; }           // REQUIRED, must be > 0
    int PageSize { get; set; }       // REQUIRED, must be > 0
    string? Search { get; set; }     // Optional
    string? SortBy { get; set; }     // Optional
    string? SortOrder { get; set; }  // Optional, default DESC
}
```

### PaginationDefaultsFilter Behavior

| Parameter | Validation | Normalization |
|-----------|------------|---------------|
| `page` | **Required** (400 if <= 0) | - |
| `pageSize` | **Required** (400 if <= 0) | Caps at maxPageSize (default 50) |
| `sortOrder` | Optional | Default "DESC", uppercase |

---

## Validation

### Where to Validate

| Validation Type | Where | Technology |
|-----------------|-------|------------|
| Required, formats, lengths | API | FluentValidation |
| Invalid JSON syntax | Middleware | JsonValidationMiddleware |
| Duplicates, FK exists, state | SP | SQL |

### Validation Error Codes

| Code | Description | Validate in |
|------|-------------|-------------|
| `VAL_001` | Required field | API |
| `VAL_002` | Invalid format | API |
| `VAL_003` | Duplicate value | SP |
| `VAL_004` | FK not exists | SP |
| `VAL_006` | Invalid JSON syntax | Middleware |
| `VAL_007` | Out of range | API |
| `VAL_008` | Length exceeded | API |

### FluentValidation Example

Validation messages MUST be in Spanish:

```csharp
public class Update{Entity}Validator : AbstractValidator<Update{Entity}Request>
{
    public Update{Entity}Validator()
    {
        RuleFor(x => x.ContactPhone)
            .NotEmpty()
            .WithErrorCode("VAL_001")
            .WithMessage("El celular de contacto es requerido")
            .Matches(@"^\d{9,15}$")
            .WithErrorCode("VAL_002")
            .WithMessage("El celular debe contener entre 9 y 15 dígitos");

        RuleFor(x => x.ContactEmail)
            .NotEmpty()
            .WithErrorCode("VAL_001")
            .WithMessage("El correo de contacto es requerido")
            .EmailAddress()
            .WithErrorCode("VAL_002")
            .WithMessage("El formato del correo es inválido")
            .MaximumLength(100)
            .WithErrorCode("VAL_008")
            .WithMessage("El correo no puede exceder 100 caracteres");
    }
}
```

> All `.WithMessage()` texts MUST be in Spanish. Each rule chain has its own `.WithErrorCode()` + `.WithMessage()` pair.

### Nested Validator Pattern

For requests with child collections, use `RuleForEach` with child validators:

```csharp
// Parent validator with child validators
public class Create{Entity}Validator : AbstractValidator<Create{Entity}Request>
{
    public Create{Entity}Validator()
    {
        RuleFor(x => x.Title)
            .NotEmpty().WithErrorCode("VAL_001");

        RuleForEach(x => x.Providers)
            .SetValidator(new Create{Entity}ProviderItemValidator())
            .When(x => x.Providers != null && x.Providers.Count > 0);
    }
}
```

### Endpoint with Validation

`.WithValidation<T>()` comes from the `ANTA.Shared.Common.Validation` package. The custom endpoint filter handles validation automatically — no manual validation needed in endpoint handlers.

```csharp
app.MapPost("/", Handle)
    .WithValidation<Create{Entity}Request>()
    .Produces<ApiResponse<Create{Entity}Response>>(201)
    .ProducesProblem(400);
```

---

## JSON Response Examples

### List with Pagination

```json
{
  "success": true,
  "data": { "items": [...] },
  "message": "Items retrieved",
  "pagination": {
    "page": 1, "pageSize": 10,
    "totalRecords": 25, "totalPages": 3,
    "hasNext": true, "hasPrevious": false
  }
}
```

### Detail

```json
{
  "success": true,
  "data": { "item": {...} },
  "message": "Item retrieved"
}
```

### Error

```json
{
  "success": false,
  "data": null,
  "message": "Validation failed",
  "errors": [
    { "code": "VAL_001", "message": "Name is required", "field": "Name" },
    { "code": "VAL_008", "message": "Name exceeds maximum length", "field": "Name" }
  ]
}
```

---

## Checklist

### Error Handling
- [ ] `SpResultHelper.ThrowIfError()` after reading SP result
- [ ] Error codes follow convention (VAL_, {MOD}_001, etc.)

### Response
- [ ] `ApiResponse<T>` with typed response class
- [ ] `{ item: {...} }` for detail, `{ items: [...] }` for list

### Pagination
- [ ] Request implements `IPagedRequest`
- [ ] `.WithPaginationDefaults()` on endpoint
- [ ] Handler returns `(Data, PaginationResult)` tuple

### Validation
- [ ] FluentValidation for API-side checks
- [ ] `.WithValidation<T>()` on endpoint
- [ ] Error codes on all validation rules

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Error mapping (SP to HTTP) | [error-mapping.md](assets/error-mapping.md) |
| Pagination handler pattern | [pagination-handler.md](assets/pagination-handler.md) |
| DictionaryMappingHelper | [dictionary-mapping.md](assets/dictionary-mapping.md) |

---

## Notes

- .NET 8 recommends `TypedResults` for better OpenAPI metadata generation, but the current codebase uses `Results.Ok()` / `Results.Created()`. Follow the existing pattern for consistency.

---

## Related Skills

| Task | Skill |
|------|-------|
| SP Templates | `database-sp` |
| Handler Patterns | `dotnet-handler` |
| API Structure | `dotnet-api` |
