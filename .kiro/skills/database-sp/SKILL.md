---
name: database-sp
description: >
  SP templates (List, Get, Create, Update, Delete, Search, Merge), STRING_SPLIT+QUOTENAME sorting.
  Trigger: When creating or modifying stored procedures.
metadata:
  author: anta
  version: "4.0"
  scope: [root]
  enforcement: mandatory
  auto_invoke: "stored procedure, SP, crear SP, modificar SP, paginacion SP"
  phase: [construction]
  layer: [database]
  validates_with: validate_sp
  validation_profile: conventions-lint
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Include v2.4 header with Object/Author/Created/Version/Description/ServiceId/Rules/Parameters/Returns/Security + CHANGE HISTORY | ALWAYS | Traceability |
| Use TRY/CATCH with `EXEC Log.GetErrorInfo` | ALWAYS | Error handling |
| Use `SET NOCOUNT ON;` | ALWAYS | Performance |
| Entity name MANDATORY in all SP names | ALWAYS | Consistency: {Schema}.{Action}{Entity} always |
| Use `WITH(NOLOCK)` on SELECT joins | ALWAYS | Read performance |
| Use CASE/WHEN or QUOTENAME+allowed columns for safe sorting | ALWAYS | SQL injection prevention |
| Return created/updated record after mutation | ALWAYS | API consistency |
| Use dot notation for nested structures | ALWAYS | C# mapping compatibility |

---

## SP Types Decision

| Need | SP Type | Template |
|------|---------|----------|
| List with pagination | List | [sp-list.sql](assets/sp-list.sql) |
| Get single record by ID | Get | [sp-get.sql](assets/sp-get.sql) |
| Insert new record | Create | [sp-create.sql](assets/sp-create.sql) |
| Update existing record | Update | [sp-update.sql](assets/sp-update.sql) |
| Soft delete (RecordStatus = '*') | Delete | [sp-delete.sql](assets/sp-delete.sql) |
| Advanced search without pagination | Search | [sp-search.sql](assets/sp-search.sql) |
| Bulk sync (insert/update/delete) | Merge | [sp-merge.sql](assets/sp-merge.sql) |
| Multiple tables in one operation | Use transaction | [transaction-patterns.md](assets/transaction-patterns.md) |

---

## Standard Structure

Every SP follows this structure:

```sql
/* Header with CHANGE HISTORY */

CREATE OR ALTER PROCEDURE [{Schema}].[{Operation}{Entity}]
    @ParamI...
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
         -- PASO 1: Validaciones (SELECT ErrorCode for business errors + RETURN)
         -- PASO 2: Operacion (count, query, or mutation)
         -- PASO 3: Resultado (SELECT data)
     END TRY
     BEGIN CATCH
         EXEC Log.GetErrorInfo;  -- For system/SQL errors only
     END CATCH
 END
```

---

## Sections Pattern

Use numbered sections with separators:

```sql
---------------------------------------------------------------
-- PASO N: Section description
---------------------------------------------------------------
```

| SP Type | Sections |
|---------|----------|
| **CRUD Simple** | 1. Validaciones, 2. Operacion, 3. Resultado |
| **GET Simple** | 1. Validaciones (optional), 2. Resultado |
| **With Transaction** | 1. Validaciones, 2. Preparacion, 3. Transaccion, 4. Resultado |

---

## Nested Structure Pattern

Use **dot notation** for nested objects (mapped by C# manual mapping from dynamic):

```sql
-- MasterTable pattern (e.g. ItemStatus)
st.MasterTableId AS [Status.MasterTableId],
st.Name AS [Status.Name],
st.Value AS [Status.Value]

-- Extended MasterTable with colors (StatusItem pattern)
s.MasterTableId AS [Status.MasterTableId],
s.Name AS [Status.Name],
s.Value AS [Status.Value],
s.AdditionalOne AS [Status.BackgroundColor],
s.AdditionalTwo AS [Status.TextColor],
s.AdditionalThree AS [Status.Type]
```

> **Note**: C# handlers map these using manual mapping from `dynamic` (not AutoMapper). The dot notation creates nested objects in the response.

---

## Sorting Pattern (Safe)

### Preferred: STRING_SPLIT Whitelist + CASE/WHEN

Used in all ANTA SPs. Validates sort column against a whitelist using `STRING_SPLIT`, then uses `CASE/WHEN` for type-safe ordering:

```sql
-- 1. Declare allowed columns as comma-separated string
DECLARE @VAllowedColumns NVARCHAR(MAX) = 'CreatedDate,Priority,OwnerId,CategoryId,StatusId,RecordCreationDate';

-- 2. Validate sort column against whitelist
IF @ParamISortBy IS NULL OR @ParamISortBy NOT IN (SELECT [value] FROM STRING_SPLIT(@VAllowedColumns, ','))
    SET @ParamISortBy = 'CreatedDate';  -- default column
IF @ParamISortOrder NOT IN ('ASC', 'DESC')
    SET @ParamISortOrder = 'DESC';       -- default order

-- 3. Use CASE/WHEN in ORDER BY (type-safe, no dynamic SQL)
ORDER BY
    CASE WHEN @ParamISortOrder = 'ASC' THEN
        CASE @ParamISortBy
            WHEN 'CreatedDate' THEN CONVERT(NVARCHAR(50), t.[CreatedDate], 126)
            WHEN 'Priority' THEN t.[Priority]
            WHEN 'OwnerId' THEN CAST(t.[OwnerId] AS NVARCHAR(50))
            WHEN 'CategoryId' THEN CAST(t.[CategoryId] AS NVARCHAR(50))
            WHEN 'StatusId' THEN CAST(t.[StatusId] AS NVARCHAR(50))
            WHEN 'RecordCreationDate' THEN CONVERT(NVARCHAR(50), b.[RecordCreationDate], 126)
        END
    END ASC,
    CASE WHEN @ParamISortOrder = 'DESC' THEN
        CASE @ParamISortBy
            WHEN 'CreatedDate' THEN CONVERT(NVARCHAR(50), t.[CreatedDate], 126)
            WHEN 'Priority' THEN t.[Priority]
            WHEN 'OwnerId' THEN CAST(t.[OwnerId] AS NVARCHAR(50))
            WHEN 'CategoryId' THEN CAST(t.[CategoryId] AS NVARCHAR(50))
            WHEN 'StatusId' THEN CAST(t.[StatusId] AS NVARCHAR(50))
            WHEN 'RecordCreationDate' THEN CONVERT(NVARCHAR(50), b.[RecordCreationDate], 126)
        END
    END DESC
OFFSET (@ParamIPage - 1) * @ParamIPageSize ROWS
FETCH NEXT @ParamIPageSize ROWS ONLY;
```

### Alternative: QUOTENAME + Dynamic SQL

Only for SPs with >10 sortable columns where CASE/WHEN becomes unwieldy:

```sql
DECLARE @VProcessedSort VARCHAR(200) = REPLACE(REPLACE(@ParamISortBy,' ',''),';','');
DECLARE @VSortColumnValidated VARCHAR(MAX) = (
    SELECT STRING_AGG(QUOTENAME(s.value), ', ')
    FROM STRING_SPLIT(@VProcessedSort, ',') s
    WHERE EXISTS (SELECT 1 FROM @VAllowedColumns WHERE ColumnName = s.value)
);
IF ISNULL(@VSortColumnValidated, '') = ''
    SET @VSortColumnValidated = QUOTENAME('RecordCreationDate');
```

### Decision Guidance

| Pattern | When to Use |
|---------|-------------|
| STRING_SPLIT + CASE/WHEN | **Default** — all SPs, no dynamic SQL |
| QUOTENAME + dynamic SQL | >10 sortable columns only |

---

## Pagination Pattern

### Single ResultSet with TotalCount

List SPs include `COUNT(*) OVER() AS [TotalCount]` as the last column in the same ResultSet (no separate metadata ResultSet):

```sql
SELECT
    t.[{Entity}Id],
    t.[OwnerId],
    -- ... columns ...
    COUNT(*) OVER() AS [TotalCount]
FROM [{Schema}].[{Entity}] t WITH(NOLOCK)
WHERE t.[RecordStatus] = 'A'
ORDER BY ...
OFFSET (@ParamIPage - 1) * @ParamIPageSize ROWS
FETCH NEXT @ParamIPageSize ROWS ONLY;
```

> The C# handler reads `TotalCount` from the first row and calculates pagination metadata (`TotalPages`, `HasNext`, `HasPrevious`).

---

## Search Pattern (LIKE)

For text search across multiple columns, build a search pattern variable:

```sql
DECLARE @VSearchPattern NVARCHAR(102) = NULL;
IF @ParamISearchFilter IS NOT NULL AND LTRIM(RTRIM(@ParamISearchFilter)) <> ''
    SET @VSearchPattern = '%' + LTRIM(RTRIM(@ParamISearchFilter)) + '%';
```

Then use in WHERE clause with OR conditions:

```sql
AND (@VSearchPattern IS NULL OR
     CONCAT_WS(' ', e.[FirstName], e.[MiddleName], e.[ThirdName], e.[LastName], e.[SecondLastName]) LIKE @VSearchPattern
     OR e.[DocumentNumber] LIKE @VSearchPattern
     OR t.[Code] LIKE @VSearchPattern)
```

---

## Full Name Pattern

Use `CONCAT_WS` for building full names from a related person table (handles NULLs automatically):

```sql
CONCAT_WS(' ', p.[FirstName], p.[MiddleName], p.[LastName], p.[SecondLastName]) AS [PersonName]
```

This pattern is used in all SPs that return employee names. `CONCAT_WS` skips NULL values, so partial names render correctly.

---

## CONSTANTS and VARIABLES Sections

SPs that reference MasterTable IDs or computed values use named sections at the top of the body:

```sql
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        -------------------------------------------------------------------
        -- CONSTANTS
        -------------------------------------------------------------------
        DECLARE @CStatusDraft     INT = 1101;
        DECLARE @CStatusSubmitted INT = 1102;
        DECLARE @CStatusApproved  INT = 1103;

        -------------------------------------------------------------------
        -- VARIABLES
        -------------------------------------------------------------------
        DECLARE @VGroupId      INT;
        DECLARE @VNewEntityId  INT;
        DECLARE @VHasPermission BIT = 0;
```

| Prefix | Purpose | Example |
|--------|---------|---------|
| `@C` | Constants (MasterTable IDs, fixed values) | `@CStatusDraft INT = 1101` |
| `@V` | Variables (computed during execution) | `@VNewEntityId INT` |

---

## Authorization Pattern (Hierarchical)

For SPs that validate who can act on behalf of another employee:

```sql
-------------------------------------------------------------------
-- PASO 0: Validar autorización jerárquica
-------------------------------------------------------------------
-- 1. Self-check: user acting on themselves
IF @ParamIBookedByEmployeeId = @ParamIEmployeeId
    SET @VHasPermission = 1;

-- 2. Elevated roles: DOCTOR, LEADERF can act on anyone
ELSE IF @ParamIBookedByRole IN ('200-146-DOCTOR', '200-146-LEADERF')
    SET @VHasPermission = 1;

-- 3. COORD: same OrgUnit check
ELSE IF @ParamIBookedByRole = '200-146-COORD'
BEGIN
    IF EXISTS (
        SELECT 1
        FROM [Personnel].[Employee] e1 WITH(NOLOCK)
        INNER JOIN [Personnel].[Employee] e2 WITH(NOLOCK)
            ON e1.[OrganizationalUnitCode] = e2.[OrganizationalUnitCode]
        WHERE e1.[EmployeeId] = @ParamIBookedByEmployeeId
          AND e2.[EmployeeId] = @ParamIEmployeeId
          AND e1.[RecordStatus] = 'A'
          AND e2.[RecordStatus] = 'A'
    )
        SET @VHasPermission = 1;
END

-- 4. USER: CTE descendants (manager hierarchy)
ELSE
BEGIN
    ;WITH Descendants AS (
        SELECT [EmployeeId]
        FROM [Personnel].[Employee] WITH(NOLOCK)
        WHERE [EmployeeId] = @ParamIBookedByEmployeeId
          AND [RecordStatus] = 'A'
        UNION ALL
        SELECT e.[EmployeeId]
        FROM [Personnel].[Employee] e WITH(NOLOCK)
        INNER JOIN Descendants d ON e.[ManagerId] = d.[EmployeeId]
        WHERE e.[RecordStatus] = 'A'
    )
    SELECT @VHasPermission = 1
    FROM Descendants
    WHERE [EmployeeId] = @ParamIEmployeeId;
END

IF @VHasPermission = 0
BEGIN
    SELECT 'AUTH_UNAUTHORIZED' AS ErrorCode,
           'employeeId' AS Field,
           'No tiene permiso para esta acción' AS Message;
    RETURN;
END
```

---

## Error Handling Pattern

SPs use **two different mechanisms** for errors:

### Business/Validation Errors → SELECT + RETURN

Returned as a result set row. The handler reads `ErrorCode` and maps to HTTP status.

```sql
-- Validation error
IF @Amount <= 0
BEGIN
    SELECT 'VAL_001' AS ErrorCode, 'Amount' AS Field, 'El monto debe ser mayor a 0' AS Message;
    RETURN;
END

-- Business rule error (duplicate)
IF EXISTS (SELECT 1 FROM Core.Contract WHERE Code = @ParamICode AND RecordStatus = 'A')
BEGIN
    SELECT 'CON_002' AS ErrorCode, 'Code' AS Field, 'Ya existe un contrato con este código' AS Message;
    RETURN;
END

-- Not found error
IF NOT EXISTS (SELECT 1 FROM Cases.[Case] WHERE CaseId = @ParamICaseId AND RecordStatus = 'A')
BEGIN
    SELECT 'CAS_001' AS ErrorCode, 'CaseId' AS Field, 'Caso no encontrado' AS Message;
    RETURN;
END
```

### System/SQL Errors → TRY/CATCH

`EXEC Log.GetErrorInfo` captures unexpected SQL exceptions (deadlocks, constraint violations, etc.):

```sql
BEGIN TRY
    -- business logic here
END TRY
BEGIN CATCH
    EXEC Log.GetErrorInfo;  -- System errors only
END CATCH
```

---

## JSON Parameters Pattern

For complex nested data, receive JSON as `NVARCHAR(MAX)` and parse with `OPENJSON`:

```sql
-- Parameter declaration
@ParamICasesJson NVARCHAR(MAX) = NULL

-- Parse with OPENJSON and insert
INSERT INTO Cases.AgendaCase (AgendaId, CaseId, OrderIndex, RecordCreationUser, RecordCreationDate, RecordStatus)
SELECT
    @VAgendaId,
    CaseId,
    OrderIndex,
    @ParamICreationUser,
    SYSDATETIMEOFFSET(),
    'A'
FROM OPENJSON(@ParamICasesJson)
WITH (
    CaseId INT '$.caseId',
    OrderIndex INT '$.orderIndex'
);
```

Use this pattern when:
- Inserting/updating multiple child records in one SP call
- Receiving arrays from the frontend
- Batch operations

---

## File Organization

| Pattern | Example |
|---------|---------|
| `{Schema}.{Action}{Entity}.sql` | `Core.CreateItem.sql` |

```
{Schema}/
└── StoredProcedures/
    ├── {Schema}.Create{Entity}.sql
    ├── {Schema}.Get{Entity}.sql
    ├── {Schema}.List{Entity}.sql
    ├── {Schema}.Update{Entity}.sql
    └── {Schema}.Delete{Entity}.sql
```

> **All nomenclature in English** — SP names, file names, entity names.

---

## Extended Properties (SP Documentation)

Document all stored procedures using `sys.sp_addextendedproperty`:

```sql
-- SP documentation
EXEC sys.sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Lists entities with filters and pagination', 
    @level0type = N'SCHEMA', @level0name = N'Core',
    @level1type = N'PROCEDURE', @level1name = N'ListItems';
```

Add Extended Property at the end of every SP file, after the GO statement.

---

## Checklist

- [ ] Header with CHANGE HISTORY table
- [ ] Parameters with `@ParamI` / `@ParamO` prefix
- [ ] Variables with `@V` / `@C` prefix
- [ ] `SET NOCOUNT ON;`
- [ ] `WITH(NOLOCK)` on all SELECT joins
- [ ] TRY/CATCH with `EXEC Log.GetErrorInfo`
- [ ] `SET XACT_ABORT ON` if using transactions
- [ ] Safe sorting (CASE/WHEN or QUOTENAME+allowed columns)
- [ ] Business errors via `SELECT ErrorCode, Field, Message` (not RAISERROR)
- [ ] JSON parameters via `NVARCHAR(MAX)` + `OPENJSON` when needed
- [ ] Dot notation for nested structures
- [ ] Return created/updated record after mutations
- [ ] TotalCount via `COUNT(*) OVER()` in same ResultSet
- [ ] Extended Property added for SP documentation

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Header template | [sp-header.sql](assets/sp-header.sql) |
| List SP template | [sp-list.sql](assets/sp-list.sql) |
| Get SP template | [sp-get.sql](assets/sp-get.sql) |
| Create SP template | [sp-create.sql](assets/sp-create.sql) |
| Update SP template | [sp-update.sql](assets/sp-update.sql) |
| Delete SP template | [sp-delete.sql](assets/sp-delete.sql) |
| Search SP template | [sp-search.sql](assets/sp-search.sql) |
| Merge SP template | [sp-merge.sql](assets/sp-merge.sql) |
| Validation patterns & error codes | [validation-patterns.md](assets/validation-patterns.md) |
| Transaction patterns | [transaction-patterns.md](assets/transaction-patterns.md) |

---

## Post-Change Tasks

After creating or modifying a SP:

- [ ] Update `docs/API_CATALOG.md` (use `api-catalog` skill)
- [ ] Update `CHANGELOG.md` (use `changelog` skill)

---

## Related Skills

| Task | Skill |
|------|-------|
| Database naming, schemas | `database` |
| Handler calling SP | `dotnet-handler` |
| SP error mapping to HTTP | `dotnet-integration` |
