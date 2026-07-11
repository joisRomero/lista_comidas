# Validation Patterns

## Error Response Format

```sql
SELECT 'ERROR_CODE' AS ErrorCode,
       'fieldName' AS Field,
       'Human readable message' AS Message;
RETURN;
```

## Validation Examples

```sql
---------------------------------------------------------------
-- PASO 1: Validaciones
---------------------------------------------------------------

-- Required field (only if not validated in API)
IF @ParamIName IS NULL OR LEN(LTRIM(RTRIM(@ParamIName))) = 0
BEGIN
    SELECT 'VAL_001' AS ErrorCode, 'name' AS Field, 'Name is required' AS Message;
    RETURN;
END

-- Entity not found
IF NOT EXISTS (SELECT 1 FROM {Schema}.{Entity} WHERE {Entity}Id = @ParamIId AND RecordStatus = 'A')
BEGIN
    SELECT '{MOD}_001' AS ErrorCode, '{entity}Id' AS Field, '{Entity} not found' AS Message;
    RETURN;
END

-- Duplicate check
IF EXISTS (SELECT 1 FROM {Schema}.{Entity} WHERE Code = @ParamICode AND {Entity}Id != @ParamIId AND RecordStatus = 'A')
BEGIN
    SELECT '{MOD}_002' AS ErrorCode, 'code' AS Field, 'Code already exists' AS Message;
    RETURN;
END

-- Invalid FK reference
IF NOT EXISTS (SELECT 1 FROM Cnfg.MasterTable WHERE MasterTableId = @ParamITypeId)
BEGIN
    SELECT 'VAL_004' AS ErrorCode, 'typeId' AS Field, 'Invalid type reference' AS Message;
    RETURN;
END

-- State validation
DECLARE @VCurrentStatus VARCHAR(50);
SELECT @VCurrentStatus = s.Name
FROM {Schema}.{Entity} e WITH(NOLOCK)
INNER JOIN Cnfg.MasterTable s WITH(NOLOCK) ON e.StatusId = s.MasterTableId
WHERE e.{Entity}Id = @ParamIId;

IF @VCurrentStatus != 'DRAFT'
BEGIN
    SELECT '{MOD}_003' AS ErrorCode, 'statusId' AS Field, 'Operation only allowed in DRAFT status' AS Message;
    RETURN;
END

-- Minimum requirements
DECLARE @VProviderCount INT;
SELECT @VProviderCount = COUNT(*) FROM {Schema}.Provider WHERE {Entity}Id = @ParamIId AND RecordStatus = 'A';

IF @VProviderCount < 1
BEGIN
    SELECT '{MOD}_004' AS ErrorCode, 'providers' AS Field, 'At least 1 provider is required' AS Message;
    RETURN;
END
```

---

## Error Codes Standard

### Error Code Prefixes

| Prefix | HTTP | Category | Mapped Exception |
|--------|------|----------|------------------|
| `VAL_*` | 400 | Input validation | `ValidationException` |
| `{MOD}_001` | 404 | Not found | `NotFoundException` |
| `{MOD}_002` | 409 | Duplicate/Conflict | `ConflictException` |
| `{MOD}_003+` | 422 | Business rule | `BusinessRuleException` |
| `AUTH_*` | 403 | Authorization | `ForbiddenException` |
| `SYS_*` | 500 | System error | `BusinessException` |

### Validation Codes (VAL_) - HTTP 400

| Code | Description | Where to Validate |
|------|-------------|-------------------|
| VAL_001 | Required field | API (FluentValidation) |
| VAL_002 | Invalid format | API (FluentValidation) |
| VAL_003 | SQL reserved word | **SP** (requires DB) |
| VAL_004 | Invalid characters | **SP** (requires DB) |
| VAL_005 | Invalid date/amount range | **SP** (requires DB) |
| VAL_006 | Invalid JSON format | API |
| VAL_007 | Value out of range | API (FluentValidation) |
| VAL_008 | Length exceeded | API (FluentValidation) |

### Module Codes Pattern ({MOD}_)

| Code | HTTP | Description |
|------|------|-------------|
| `{MOD}_001` | 404 | Entity not found |
| `{MOD}_002` | 409 | Entity already exists (duplicate) |
| `{MOD}_003+` | 422 | Business rule violation |

**Example for Cases module:**
- `CASE_001` → Case not found (404)
- `CASE_002` → Duplicate provider RUC (409)
- `CASE_003` → Invalid state for operation (422)
- `CASE_004` → Minimum requirements not met (422)

### Where to Validate

| Type | Where | Why |
|------|-------|-----|
| Required fields | API | Fast fail, no DB round-trip |
| Format validation | API | Regex, email, RUC format |
| Length limits | API | Fast fail |
| Duplicates | **SP** | Requires DB query |
| FK exists | **SP** | Requires DB query |
| State transitions | **SP** | Requires current state |
| Business rules | **SP** | Complex logic with data |
| Reserved words | **SP** | Requires Cnfg.SQLReservedWords lookup |
| Invalid characters | **SP** | SQL injection prevention |

---

## Security Validations

### Reserved Word Check

```sql
IF Cnfg.IsReservedWord(@ParamIName) = 1
BEGIN
    SELECT 'VAL_003' AS ErrorCode, 'name' AS Field, 'El nombre contiene una palabra reservada de SQL' AS Message;
    RETURN;
END
```

### Invalid Characters Check

```sql
IF Cnfg.HasInvalidCharacters(@ParamIName) = 1
BEGIN
    SELECT 'VAL_004' AS ErrorCode, 'name' AS Field, 'El nombre contiene caracteres no permitidos' AS Message;
    RETURN;
END
```

### Date Range Validation

```sql
IF @ParamIStartDate IS NOT NULL AND @ParamIEndDate IS NOT NULL 
   AND @ParamIStartDate > @ParamIEndDate
BEGIN
    SELECT 'VAL_005' AS ErrorCode, 'startDate' AS Field, 'La fecha inicial no puede ser mayor a la fecha final' AS Message;
    RETURN;
END
```

### JSON Validation

```sql
IF @ParamIData IS NOT NULL AND ISJSON(@ParamIData) = 0
BEGIN
    SELECT 'VAL_006' AS ErrorCode, 'data' AS Field, 'El formato JSON no es valido' AS Message;
    RETURN;
END
```
