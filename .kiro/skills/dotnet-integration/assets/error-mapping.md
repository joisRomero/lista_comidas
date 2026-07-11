# Error Mapping (SP to HTTP)

## Error Flow

```
SP Error Code        SpResultHelper           Exception              HTTP Status
─────────────────────────────────────────────────────────────────────────────────
VAL_xxx          →   ValidationException   →   Middleware catches →   400 Bad Request
{MOD}_001        →   NotFoundException     →   Middleware catches →   404 Not Found
{MOD}_002        →   ConflictException     →   Middleware catches →   409 Conflict
{MOD}_003+       →   BusinessRuleException →   Middleware catches →   422 Unprocessable
AUTH_xxx         →   ForbiddenException    →   Middleware catches →   403 Forbidden
SYS_xxx          →   BusinessException     →   Middleware catches →   500 Internal
```

## SP Error Format

```sql
SELECT '{CODE}' AS ErrorCode,
       'fieldName' AS Field,
       'Descriptive message' AS Message;
RETURN;
```

## SpResultHelper Usage

```csharp
var result = await multi.ReadAsync<dynamic>();
var firstRow = result.FirstOrDefault();

SpResultHelper.ThrowIfError(firstRow);
```

## Exception Classes (ANTA.Shared.Common.Exceptions)

```csharp
BusinessException (base)
├── NotFoundException      // 404 - {MOD}_001
├── ValidationException    // 400 - VAL_xxx
├── ConflictException      // 409 - {MOD}_002
├── ForbiddenException     // 403 - AUTH_xxx
├── BusinessRuleException  // 422 - {MOD}_003+
└── BadGatewayException    // 502 - External services
```

## Error Codes

| Code | Description | Where | HTTP |
|------|-------------|-------|------|
| VAL_001 | Required field | API | 400 |
| VAL_002 | Invalid format | API | 400 |
| VAL_007 | Value out of range | API | 400 |
| VAL_008 | Length exceeded | API | 400 |
| {MOD}_001 | Not found | SP | 404 |
| {MOD}_002 | Duplicate/Conflict | SP | 409 |
| {MOD}_003+ | Business rule | SP | 422 |
| AUTH_001 | Unauthorized | API/SP | 403 |
| SYS_001 | System error | SP | 500 |
