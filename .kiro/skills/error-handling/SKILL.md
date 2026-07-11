---
name: error-handling
description: >
  Error handling patterns across all layers (SP, Backend, Frontend).
  Trigger: When implementing error handling, exceptions, error responses, or error UI.
metadata:
  author: anta
  version: "2.0"
  scope: [root]
  auto_invoke: "error handling, exception, error response, try catch, error boundary"
  phase: [construction]
  layer: [backend]
  validates_with: validate_dotnet_handler
  validation_profile: build-unit
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Use typed exceptions, not generic `Exception` | ALWAYS | Automatic HTTP mapping |
| Return error codes, not just messages | ALWAYS | Frontend can handle programmatically |
| Log at the boundary, not everywhere | ALWAYS | Avoid duplicate logs |
| Never expose stack traces to clients | NEVER | Security risk |

---

## Error Flow

```
SP (SELECT ErrorCode) → Handler (SpResultHelper.ThrowIfError) → Typed Exception → UseAntaminaExceptionHandler Middleware → ApiResponse → Frontend (toast/form)
```

---

## Layer-by-Layer Reference

### 1. Stored Procedure

SPs return errors as a **SELECT result set**, NOT via RAISERROR:

```sql
-- validation
IF @Amount <= 0
BEGIN
    SELECT 'VAL_001' AS ErrorCode, 'Amount' AS Field, 'El monto debe ser mayor a 0' AS Message;
    RETURN;
END

-- business rule
IF EXISTS (SELECT 1 FROM Contracts WHERE Code = @Code)
BEGIN
    SELECT 'CON_002' AS ErrorCode, 'Code' AS Field, 'Ya existe un contrato con este código' AS Message;
    RETURN;
END

-- success
SELECT @NewId AS Id;
```

**Error Format:** Error codes are set in variables, then returned via `SELECT ErrorCode, Field, Message`. The SP uses `RETURN` to exit after the error result set.

### 2. Backend Handler

Handlers use `SpResultHelper.ThrowIfError()` to check SP results. **No try/catch blocks** — exceptions bubble up to middleware.

```csharp
public async Task<CreateEntityResponse> Handle(CreateEntityCommand request)
{
    var result = await _db.QuerySingleAsync<dynamic>("Schema.SP_CreateEntity", request);
    SpResultHelper.ThrowIfError(result);  // Reads ErrorCode from result, throws typed exception

    return new CreateEntityResponse { Item = MapToEntity(result) };
}
```

`SpResultHelper.ThrowIfError(result)` inspects the result set for an `ErrorCode` column. If present, it maps the error code prefix to the appropriate typed exception and throws it.

### 3. Exception Types → HTTP Status

| Exception | HTTP | When |
|-----------|------|------|
| `ValidationException` | 400 | Input invalid |
| `ForbiddenException` | 403 | No permission |
| `NotFoundException` | 404 | Entity not found |
| `ConflictException` | 409 | Duplicate |
| `BusinessRuleException` | 422 | Rule violation |
| `BadGatewayException` | 502 | External service down |

### 4. API Response Format

The `errors` field is an **array** of `ApiError` objects (not a single `error` object):

```json
{
  "success": false,
  "data": null,
  "message": "Error message",
  "errors": [
    { "code": "CON_002", "message": "Ya existe un contrato con este código", "field": "Code" }
  ]
}
```

### 5. Frontend Handling

```typescript
const mutation = useMutation({
  mutationFn: createContract,
  onError: (error: ApiError) => {
    if (error.field) {
      form.setFields([{ name: error.field, errors: [error.message] }]);
    } else {
      notification.error({ message: error.message });
    }
  },
});
```

---

## Error Code Prefixes

| Prefix | Category | Example |
|--------|----------|---------|
| `VAL_` | Validation (400) | `VAL_001` - Required field |
| `AUTH_` | Authorization (403) | `AUTH_001` - No permission |
| `{MOD}_001` | Not found (404) | `CON_001` - Contract not found |
| `{MOD}_002` | Duplicate (409) | `CON_002` - Contract exists |
| `{MOD}_003+` | Business rule (422) | `CON_003` - Invalid state |
| `SYS_` | System (500) | `SYS_001` - Unexpected error |

---

## Checklist

- [ ] SP returns `SELECT ErrorCode, Field, Message` for errors
- [ ] Handler calls `SpResultHelper.ThrowIfError()` after every SP call
- [ ] `UseAntaminaExceptionHandler` middleware returns `ApiResponse` with `errors` array
- [ ] Frontend checks `error.field` for form errors vs toast
- [ ] Error codes follow prefix convention
- [ ] No stack traces in production responses

---

## Related Skills

| Task | Skill |
|------|-------|
| SP patterns | `database-sp` |
| Exception middleware | `dotnet-shared-libs` |
| Handler patterns | `dotnet-handler` |
| React error handling | `react` |
