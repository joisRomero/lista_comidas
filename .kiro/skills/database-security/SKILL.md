---
name: database-security
description: >
  SQL Server security validations: reserved words, invalid characters, error code catalog,
  input validation patterns, and safe dynamic sorting with QUOTENAME.
  Trigger: When implementing SP validations, error codes, or SQL injection prevention.
metadata:
  author: anta
  version: "1.0"
  scope: [root]
  enforcement: mandatory
  auto_invoke: "validación SQL, SQL injection, palabra reservada, código de error, VAL_, SYS_, AUTH_, QUOTENAME, seguridad BD"
  phase: [inception, construction]
  layer: [database]
  validates_with: validate_sp
  validation_profile: conventions-lint
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Validate reserved words before any dynamic name usage | ALWAYS | Prevent SQL injection via object names |
| Validate invalid characters on all free-text inputs | ALWAYS | Prevent injection via special chars |
| Use QUOTENAME + whitelist for dynamic sorting | ALWAYS | Only safe columns in ORDER BY |
| Use standard error code prefixes (VAL_, {MOD}_, SYS_, AUTH_) | ALWAYS | Consistent error handling across all SPs |
| Return errors as `SELECT ErrorCode, Field, Message` + `RETURN` | ALWAYS | Compatible with ApiError structure |
| Normalize pagination params, don't reject | ALWAYS | UX-friendly, no error on bad page/size |

---

## Reserved Words Validation

### Table

```sql
CREATE TABLE Cnfg.SQLReservedWords (
    Word VARCHAR(50) PRIMARY KEY
);

INSERT INTO Cnfg.SQLReservedWords (Word) VALUES
('SELECT'),('INSERT'),('UPDATE'),('DELETE'),('DROP'),('CREATE'),('ALTER'),
('TABLE'),('INDEX'),('VIEW'),('PROCEDURE'),('FUNCTION'),('TRIGGER'),
('DATABASE'),('SCHEMA'),('GRANT'),('REVOKE'),('EXEC'),('EXECUTE'),
('UNION'),('JOIN'),('WHERE'),('FROM'),('INTO'),('VALUES'),('SET'),
('NULL'),('NOT'),('AND'),('OR'),('IN'),('EXISTS'),('BETWEEN'),('LIKE'),
('ORDER'),('GROUP'),('HAVING'),('BY'),('AS'),('ON'),('PRIMARY'),('FOREIGN'),
('KEY'),('CONSTRAINT'),('DEFAULT'),('CHECK'),('UNIQUE'),('IDENTITY'),
('TRUNCATE'),('BACKUP'),('RESTORE'),('BEGIN'),('END'),('COMMIT'),('ROLLBACK'),
('TRANSACTION'),('CURSOR'),('DECLARE'),('FETCH'),('OPEN'),('CLOSE'),
('IF'),('ELSE'),('WHILE'),('CASE'),('WHEN'),('THEN'),('RETURN'),
('PRINT'),('RAISERROR'),('THROW'),('TRY'),('CATCH'),('WITH'),('CTE'),
('MERGE'),('OUTPUT'),('INSERTED'),('DELETED'),('TOP'),('DISTINCT'),
('COUNT'),('SUM'),('AVG'),('MIN'),('MAX'),('CAST'),('CONVERT'),('COALESCE'),
('ISNULL'),('NULLIF'),('GETDATE'),('SYSDATETIME'),('DATEADD'),('DATEDIFF'),
('USER'),('SYSTEM'),('ADMIN'),('PASSWORD'),('LOGIN'),('MASTER'),('TEMPDB'),
('MODEL'),('MSDB'),('SYS'),('INFORMATION_SCHEMA'),('XP_'),('SP_');
```

### Function

```sql
CREATE OR ALTER FUNCTION Cnfg.IsReservedWord (
    @ParamIWord VARCHAR(100)
)
RETURNS BIT
AS
BEGIN
    DECLARE @VResult BIT = 0;

    IF EXISTS (
        SELECT 1
        FROM Cnfg.SQLReservedWords
        WHERE Word = UPPER(LTRIM(RTRIM(@ParamIWord)))
    )
        SET @VResult = 1;

    RETURN @VResult;
END
```

---

## Invalid Characters Validation

```sql
CREATE OR ALTER FUNCTION Cnfg.HasInvalidCharacters (
    @ParamIValue VARCHAR(500)
)
RETURNS BIT
AS
BEGIN
    DECLARE @VResult BIT = 0;

    IF @ParamIValue LIKE '%[-;''"%*]%'
       OR @ParamIValue LIKE '%[-][-]%'       -- --
       OR @ParamIValue LIKE '%[/][*]%'       -- /*
       OR @ParamIValue LIKE '%[*][/]%'       -- */
       OR CHARINDEX(CHAR(0), @ParamIValue) > 0  -- null byte
        SET @VResult = 1;

    RETURN @VResult;
END
```

---

## Usage in SPs

```sql
-- Validate before any operation
IF Cnfg.IsReservedWord(@ParamIName) = 1
BEGIN
    SELECT 'VAL_003' AS ErrorCode,
           'name' AS Field,
           'El nombre contiene una palabra reservada de SQL' AS Message;
    RETURN;
END

IF Cnfg.HasInvalidCharacters(@ParamIName) = 1
BEGIN
    SELECT 'VAL_004' AS ErrorCode,
           'name' AS Field,
           'El nombre contiene caracteres no permitidos' AS Message;
    RETURN;
END
```

---

## Error Code Catalog

### Validation Errors (VAL_)

| Code | Description |
|------|-------------|
| VAL_001 | Campo requerido |
| VAL_002 | Formato inválido |
| VAL_003 | Palabra reservada SQL |
| VAL_004 | Caracteres no permitidos |
| VAL_005 | Rango de fechas inválido |
| VAL_006 | JSON inválido |
| VAL_007 | Valor fuera de rango |
| VAL_008 | Longitud excedida |

### Business Errors ({MOD}_)

| Code | Description |
|------|-------------|
| {MOD}_001 | Registro no encontrado |
| {MOD}_002 | Registro duplicado |
| {MOD}_003 | Registro en uso (no se puede eliminar) |
| {MOD}_004 | Estado no permite esta operación |
| {MOD}_005 | Límite excedido |

> `{MOD}` = module prefix (e.g., CASE_001, ORD_001, CAT_001)

### System Errors (SYS_)

| Code | Description |
|------|-------------|
| SYS_001 | Error interno de sistema |

### Auth Errors (AUTH_)

| Code | Description |
|------|-------------|
| AUTH_001 | No autorizado |
| AUTH_002 | Token expirado |
| AUTH_003 | Permisos insuficientes |

### Error Return Pattern

```sql
SELECT '{PREFIX}_{CODE}' AS ErrorCode,
       '{fieldName}' AS Field,
       '{Descriptive message}' AS Message;
RETURN;
```

---

## Input Validation Patterns

### Date Range

```sql
IF @ParamIStartDate > @ParamIEndDate
BEGIN
    SELECT 'VAL_005' AS ErrorCode,
           'startDate' AS Field,
           'La fecha inicial no puede ser mayor a la fecha final' AS Message;
    RETURN;
END
```

### JSON

```sql
IF @ParamIData IS NOT NULL AND ISJSON(@ParamIData) = 0
BEGIN
    SELECT 'VAL_006' AS ErrorCode,
           'data' AS Field,
           'El formato JSON no es válido' AS Message;
    RETURN;
END
```

### Limit Without Pagination

```sql
DECLARE @CMaxRecords INT = 1000;
SELECT TOP (@CMaxRecords) *
FROM {Schema}.TableName
WHERE RecordStatus = 'A';
```

---

## Safe Dynamic Sorting (Anti-Injection)

```sql
-- 1. Declare whitelist
DECLARE @AllowedColumns TABLE (ColName VARCHAR(50));
INSERT INTO @AllowedColumns VALUES
    ('Code'), ('Name'), ('Amount'), ('RecordCreationDate');

-- 2. Sanitize input
DECLARE @VProcessedSort VARCHAR(200) = REPLACE(REPLACE(@ParamISortBy,' ',''),';','');

-- 3. Validate against whitelist + QUOTENAME
DECLARE @VSortColumnValidated VARCHAR(MAX) = (
    SELECT STRING_AGG(QUOTENAME(s.value), ', ')
    FROM STRING_SPLIT(@VProcessedSort, ',') s
    WHERE EXISTS (SELECT 1 FROM @AllowedColumns WHERE ColName = s.value)
);

-- 4. Fallback to default
IF ISNULL(@VSortColumnValidated, '') = ''
    SET @VSortColumnValidated = QUOTENAME('RecordCreationDate');

-- 5. Validate sort order
DECLARE @VValidSortOrder VARCHAR(4) =
    CASE WHEN UPPER(@ParamISortOrder) IN ('ASC','DESC')
         THEN UPPER(@ParamISortOrder) ELSE 'ASC' END;
```

---

## Checklist

- [ ] Cnfg.SQLReservedWords table exists
- [ ] Cnfg.IsReservedWord function deployed
- [ ] Cnfg.HasInvalidCharacters function deployed
- [ ] All SPs validate free-text inputs with both functions
- [ ] Error codes follow standard prefixes (VAL_, {MOD}_, SYS_, AUTH_)
- [ ] Error return uses `SELECT ErrorCode, Field, Message` + `RETURN`
- [ ] Dynamic sorting uses whitelist + QUOTENAME pattern
- [ ] Date range validations present where applicable
- [ ] JSON validations present where applicable
- [ ] SELECTs without pagination use TOP limit

---

## Related Skills

| Task | Skill |
|------|-------|
| Database naming, schemas, parameters | `database` |
| SP templates (List, Get, Create, etc.) | `database-sp` |
| Audit columns, soft delete, Log schema | `database-audit` |
| Table design, constraints, indexes | `database-modeling` |
