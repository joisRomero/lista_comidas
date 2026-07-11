---
name: database
description: >
  SQL Server conventions for ANTA projects: schemas, naming, parameters, errors, pagination, logging.
  Trigger: When working with SQL Server, tables, schemas, or database design.
metadata:
  author: anta
  version: "3.0"
  scope: [root]
  enforcement: mandatory
  auto_invoke: "SQL Server, database, tabla, esquema, columna, indice, vista, funcion"
  phase: [construction]
  layer: [database]
  validates_with: validate_db_schema
  validation_profile: conventions-lint
---

## MCP SQL Server Configuration

Projects use `@bytebase/dbhub` MCP server. **Always use MCP tools** for database operations.

```json
{
  "mcp": {
    "sqlserver": {
      "command": ["npx", "-y", "@bytebase/dbhub@latest", "--transport", "stdio",
        "--dsn", "sqlserver://{User}:{Password}@{Server}:{Port}/{Database}?trustServerCertificate=true"],
      "enabled": true
    }
  }
}
```

| Tool | Purpose |
|------|---------|
| `execute_sql` | Execute SQL queries |
| `search_objects` | Explore database schema |

---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Use `WITH(NOLOCK)` on all SELECT joins | ALWAYS | Prevent locks |
| Filter `RecordStatus = 'A'` in joins | ALWAYS | Soft delete convention |
| Use `SYSDATETIMEOFFSET()` for dates | ALWAYS | Timezone-aware |
| PK with IDENTITY must be **DESC** | ALWAYS | Recent records first, better query perf |
| Check Constraint on RecordStatus | ALWAYS | `CHECK (RecordStatus IN ('A','I','*'))` |
| Booleans as `BIT NOT NULL DEFAULT 0` | ALWAYS | No NULLs in boolean logic |
| Use `SELECT *` | NEVER | Performance, fragile mappings |

---

## Schemas

### Standard Schemas

| Schema | Purpose |
|--------|---------|
| `Log` | Logging and errors |
| `Sec` | Security/Auth |
| `Cnfg` | Configuration/Catalogs |
| `Core` | Main transactional business |
| `Mstr` | Master data |
| `Ext` | External data (SAP, ERP) |
| `Rpt` | Report views |

> **Note:** These are ANTA template schemas. Each project defines domain-specific schemas.
> Example: ComiteContratos uses `Cases`, `Sessions`, `Cross`, `Catalog`, `Cnfg`, `Ext`.

### Catalog Table Pattern

For reusable status/type catalogs, use a hierarchical master table pattern:

| Column | Type | Description |
|--------|------|-------------|
| `MasterTableId` | `INT` PK | Unique identifier |
| `MasterTableIdParent` | `INT NULL` | Parent category (NULL for root nodes) |
| `Name` | `VARCHAR(200)` | Display label |
| `Description` | `NVARCHAR(MAX)` | Extended description |
| `Value` | `NVARCHAR(MAX)` | Programmatic value |
| `DisplayOrder` | `SMALLINT` | Sort order |
| + 5 audit columns | | Standard audit columns |

---

## Naming Conventions

### Database

| Attribute | Convention | Example |
|-----------|-----------|---------|
| Name | `{Environment}_{Name}` | `Dev_ContractsCommittee` |
| Style | UpperCamelCase | |
| Collation | `SQL_Latin1_General_CP1_CI_AS` | |

### Tables & Columns

| Type | Pattern | Data Type | Example |
|------|---------|-----------|---------|
| Table | `{Schema}.{Name}` (singular, max 50 chars) | | `Core.Transaction` |
| Primary Key | `{TableName}Id` | INT IDENTITY(1,1) default | `TransactionId` |
| Foreign Key | `{ReferencedTable}Id` | Same as referenced PK | `StatusId` |
| Boolean | `Is{Name}` | **BIT NOT NULL DEFAULT 0** | `IsActive`, `IsDeleted` |
| Date | `{Name}Date` | DATETIMEOFFSET(7) | `ExpirationDate` |
| General | UpperCamelCase | As needed | `Name`, `Amount` |

#### ID Types

| Type | When to Use |
|------|-------------|
| `INT IDENTITY(1,1)` | **Default** — internal tables, best performance |
| `BIGINT IDENTITY(1,1)` | High volume tables (>2 billion rows) |
| `UNIQUEIDENTIFIER` | External integration, distributed sync, public APIs |

#### PK Ordering (Mandatory)

| ID Type | PK Order | Reason |
|---------|----------|--------|
| INT/BIGINT IDENTITY | **DESC** (mandatory) | Recent records first, optimizes typical queries |
| UNIQUEIDENTIFIER | ASC (default) | `NEWSEQUENTIALID()` already generates ordered values |

```sql
-- Correct: DESC for IDENTITY PKs
CONSTRAINT PK_{Schema}_{Table} PRIMARY KEY CLUSTERED ({Table}Id DESC)

-- Wrong (avoid): defaults to ASC
CONSTRAINT PK_{Schema}_{Table} PRIMARY KEY CLUSTERED ({Table}Id)
```

### Stored Procedures

| Operation | Pattern | Example |
|-----------|---------|---------|
| List (paginated) | `{Schema}.List{Entity}` | `Core.ListItems` |
| Get by ID | `{Schema}.Get{Entity}` | `Personnel.GetEmployee` |
| Search (advanced) | `{Schema}.Search{Entity}` | `Operations.SearchTasks` |
| Create | `{Schema}.Create{Entity}` | `Core.CreateItem` |
| Update | `{Schema}.Update{Entity}` | `Core.UpdateItem` |
| Delete (soft) | `{Schema}.Delete{Entity}` | `Core.DeleteItem` |
| Workflow | `{Schema}.Submit{Entity}` | `Operations.SubmitTask` |
| History | `{Schema}.Get{Entity}History` | `Operations.GetTaskHistory` |
| Sub-entities | `{Schema}.{Action}{SubEntity}` | `Personnel.ListDependents` |

> **Entity name is MANDATORY** in all SP names, regardless of schema complexity.
> **All nomenclature in English** — table names, column names, SP names, entity names.

**List vs Search:**

| Operation | Use | Characteristics |
|-----------|-----|-----------------|
| `List` | Standard paginated listing | Simple filters, pagination |
| `Search` | Advanced search | Multiple criteria, no pagination, `TOP(@MaxRecords)` |

### Constraints & Indexes

| Type | Pattern | Example |
|------|---------|---------|
| Primary Key | `PK_{Schema}_{Table}` | `PK_Cases_GeneralData` |
| Foreign Key | `FK_{Schema}_{Table}_{Relation}` | `FK_Cases_GeneralData_DocumentType` |
| Unique | `UN_{Schema}_{Table}_{Columns}` | `UN_Mstr_Person_DocumentNumber` |
| Check | `CK_{Schema}_{Table}_{Column}` | `CK_Cnfg_MasterTable_RecordStatus` |
| Default | `DF_{Schema}_{Table}_{Column}` | `DF_Cases_GeneralData_RecordStatus` |
| Index NC | `IXN_{Schema}_{Table}_{Columns}` | `IXN_Cases_GeneralData_CurrentStatusId` |
| Index C | `IXC_{Schema}_{Table}_{Columns}` | `IXC_Cases_GeneralData_GeneralDataId` |

### Triggers (avoid when possible — prefer SP logic)

| Type | Pattern | Example |
|------|---------|---------|
| After Insert | `TR_{Schema}_{Table}_AI` | `TR_Cases_GeneralData_AI` |
| After Update | `TR_{Schema}_{Table}_AU` | `TR_Cases_GeneralData_AU` |
| After Delete | `TR_{Schema}_{Table}_AD` | `TR_Cases_GeneralData_AD` |
| Instead Of | `TR_{Schema}_{Table}_IO` | `TR_Cases_GeneralData_IO` |

### Functions & Views

| Type | Pattern | Example |
|------|---------|---------|
| Scalar Function | `{Schema}.{Name}` | `Cnfg.IsReservedWord` |
| Table Function (Inline TVF) | `{Schema}.Get{Name}` | `Cnfg.GetCatalogItemsByParent` |
| View | `{Schema}.VW_{Name}` | `Rpt.VW_CasesWithStatus` |

> Prefer Inline TVF over Multi-Statement TVF. Report views go in `Rpt` schema.

---

## Parameters & Variables

| Type | Prefix | Example |
|------|--------|---------|
| Input param | `@ParamI` | `@ParamIPage` |
| Output param | `@ParamO` | `@ParamOTotalRecords` |
| Variable | `@V` | `@VOffset` |
| Constant | `@C` | `@CMaxPageSize` |
| Temp table | `#` | `#Result` |
| Table variable | `@` | `@AllowedColumns` |

---

## Audit Columns (Required)

| Column | Type |
|--------|------|
| RecordCreationUser | `VARCHAR(50) NOT NULL` |
| RecordCreationDate | `DATETIMEOFFSET(7) NOT NULL DEFAULT SYSDATETIMEOFFSET()` |
| RecordEditUser | `VARCHAR(50) NULL` |
| RecordEditDate | `DATETIMEOFFSET(7) NULL` |
| RecordStatus | `CHAR(1) NOT NULL DEFAULT 'A'` |

### RecordStatus Values

| Value | Meaning | Usage |
|-------|---------|-------|
| `A` | Active | Default for new records |
| `I` | Inactive | Disabled but visible in admin |
| `*` | Logical Delete | Soft-deleted, filtered out in all queries |

### Check Constraint (Mandatory)

Every table with `RecordStatus` **must** include:

```sql
CONSTRAINT CK_{Schema}_{Table}_RecordStatus CHECK (RecordStatus IN ('A', 'I', '*'))
```

### Table Template

```sql
CREATE TABLE {Schema}.{Table} (
    {Table}Id INT IDENTITY(1,1) NOT NULL,
    -- ... domain columns ...
    RecordCreationUser VARCHAR(50) NOT NULL,
    RecordCreationDate DATETIMEOFFSET(7) NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    RecordEditUser VARCHAR(50) NULL,
    RecordEditDate DATETIMEOFFSET(7) NULL,
    RecordStatus CHAR(1) NOT NULL DEFAULT 'A',

    CONSTRAINT PK_{Schema}_{Table} PRIMARY KEY CLUSTERED ({Table}Id DESC),
    CONSTRAINT CK_{Schema}_{Table}_RecordStatus CHECK (RecordStatus IN ('A', 'I', '*'))
);
```

---

## Error Codes

| Prefix | Use | HTTP |
|--------|-----|------|
| `VAL_` | Input validation | 400 |
| `{MOD}_001` | Not found | 404 |
| `{MOD}_002` | Duplicate/Conflict | 409 |
| `{MOD}_003+` | Business rule | 422 |
| `AUTH_` | Authorization | 403 |
| `SYS_` | System error | 500 |

---

## SP Error Return Pattern

SPs return business/validation errors via **SELECT** (not RAISERROR). System errors are caught by TRY/CATCH.

```sql
-- Business/validation error:
IF @Amount <= 0
BEGIN
    SELECT 'VAL_001' AS ErrorCode, 'amount' AS Field, 'El monto debe ser mayor a 0' AS Message;
    RETURN;
END

-- Not found:
IF NOT EXISTS (SELECT 1 FROM Core.Entity WHERE EntityId = @ParamIEntityId AND RecordStatus = 'A')
BEGIN
    SELECT 'ENT_001' AS ErrorCode, 'entityId' AS Field, 'Entidad no encontrada' AS Message;
    RETURN;
END
```

The backend handler reads this result set and maps `ErrorCode` → HTTP status using `SpResultHelper.ThrowIfError()`.

---

## Pagination

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `@ParamIPage` | INT | Page number (1-based, default 1) |
| `@ParamIPageSize` | INT | Page size (default 20, max 100) |
| `@ParamISearch` / `@ParamISearchFilter` | NVARCHAR(100) | General search (LIKE) |
| `@ParamISortBy` | NVARCHAR(50) | Sort column (single column) |
| `@ParamISortOrder` | NVARCHAR(4) | ASC or DESC (default DESC) |

### Pagination Result — Single ResultSet with TotalCount

List SPs return `COUNT(*) OVER() AS [TotalCount]` as an additional column in the same ResultSet:

```sql
SELECT
    b.[BookingId],
    b.[EmployeeId],
    -- ... other columns ...
    COUNT(*) OVER() AS [TotalCount]
FROM [Schema].[Table] b WITH(NOLOCK)
WHERE b.[RecordStatus] = 'A'
ORDER BY ...
OFFSET (@ParamIPage - 1) * @ParamIPageSize ROWS
FETCH NEXT @ParamIPageSize ROWS ONLY;
```

> The C# handler reads `TotalCount` from the first row and calculates `TotalPages`, `HasNext`, `HasPrevious` in the response mapping.

### Parameter Normalization

Pagination params are **normalized** (never return errors):

```sql
IF @ParamIPageSize > 100 SET @ParamIPageSize = 100;
IF @ParamIPageSize < 1 SET @ParamIPageSize = 20;
IF @ParamIPage < 1 SET @ParamIPage = 1;
```

---

## Security Validations

| Function | Purpose |
|----------|---------|
| `Cnfg.IsReservedWord(@value)` | Validate input doesn't contain SQL reserved words |
| `Cnfg.HasInvalidCharacters(@value)` | Detect SQL injection characters |

### Soft Delete in JOINs

```sql
-- ALWAYS filter RecordStatus in JOINs
SELECT h.ColumnA, d.ColumnB
FROM {Schema}.Header h WITH(NOLOCK)
INNER JOIN {Schema}.Detail d WITH(NOLOCK) 
    ON h.HeaderId = d.HeaderId AND d.RecordStatus = 'A'
WHERE h.RecordStatus = 'A';
```

### Table Access Order (Prevent Deadlocks)

Always access tables in this order:
1. `Mstr` (Master data)
2. `Cnfg` (Configuration)
3. `Core` / Custom schema (Transactional)
4. `Log` (Logging — last)

---

## CTE Guidelines

| Scenario | Use CTE | Use Temp Table |
|----------|---------|----------------|
| Simple query, used once | ✅ | |
| Hierarchical data (tree) | ✅ Recursive | |
| Reuse result multiple times | | ✅ `#Temp` |
| Large source (>100k rows) | | ✅ `#Temp` with index |
| Pagination over filtered set | | ✅ `#Temp` |

---

## Index Best Practices

### INCLUDE Clause (Mandatory for Performance)

**All nonclustered indexes SHOULD use INCLUDE** to avoid key lookups:

```sql
-- Correct: INCLUDE frequently queried columns
CREATE NONCLUSTERED INDEX IXN_Cases_GeneralData_CurrentStatusId
ON Cases.GeneralData (CurrentStatusId)
INCLUDE (CaseCode, CaseName, EstimatedAmount, RecordCreationDate)
WHERE RecordStatus = 'A';

-- Wrong: Missing INCLUDE causes expensive lookups
CREATE NONCLUSTERED INDEX IXN_Cases_GeneralData_CurrentStatusId
ON Cases.GeneralData (CurrentStatusId)
WHERE RecordStatus = 'A';
```

**Guidelines**:
- Include columns frequently selected in queries using this index
- Include columns used in WHERE/JOIN but not in the index key
- Balance: More INCLUDE columns = larger index but faster queries
- Typical INCLUDE: 3-5 columns most commonly accessed with the indexed column

---

## Logging Tables

| Table | Purpose | Source |
|-------|---------|--------|
| `Log.LogDB` | DB errors (SP CATCH blocks) | SQL Server |
| `Log.AuditHttp` | Incoming HTTP requests | Clients → API |
| `Log.AuditEndpoint` | Outgoing HTTP calls | API → External |
| `Log.LogHttp` | HTTP exceptions | Middleware |
| `Log.LogJob` | Background job execution | Hangfire/Workers |

---

## Extended Properties (Documentation)

Use `sys.sp_addextendedproperty` to document database objects:

```sql
-- Table documentation
EXEC sys.sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Employee master data synced from SAP', 
    @level0type = N'SCHEMA', @level0name = N'SAP',
    @level1type = N'TABLE', @level1name = N'Employee';

-- Column documentation
EXEC sys.sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'SAP employee code (VARCHAR(10) external PK)', 
    @level0type = N'SCHEMA', @level0name = N'SAP',
    @level1type = N'TABLE', @level1name = N'Employee',
    @level2type = N'COLUMN', @level2name = N'EmployeeId';

-- SP documentation
EXEC sys.sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Gets a single entity with related status information', 
    @level0type = N'SCHEMA', @level0name = N'Core',
    @level1type = N'PROCEDURE', @level1name = N'GetItem';

-- Index documentation
EXEC sys.sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Index for employee lookups by document number', 
    @level0type = N'SCHEMA', @level0name = N'SAP',
    @level1type = N'TABLE', @level1name = N'Employee',
    @level2type = N'INDEX', @level2name = N'IXN_SAP_Employee_DocumentNumber';
```

---

## Checklist

- [ ] Audit columns complete (Record*)
- [ ] `RecordStatus` has Check Constraint `CK_{Schema}_{Table}_RecordStatus`
- [ ] PK with IDENTITY uses **DESC** ordering
- [ ] Booleans use `BIT NOT NULL DEFAULT 0`
- [ ] Constraints with correct naming (PK, FK, UN, CK, DF, IXN)
- [ ] Nonclustered indexes use **INCLUDE** clause with frequently queried columns
- [ ] Extended Properties added for tables, columns, SPs, indexes
- [ ] `WITH(NOLOCK)` on all SELECT JOINs
- [ ] `RecordStatus = 'A'` filter in JOINs
- [ ] Parameters with `@ParamI` / `@ParamO` prefix
- [ ] Business errors via `SELECT ErrorCode, Field, Message` + `RETURN`
- [ ] Pagination uses `COUNT(*) OVER() AS [TotalCount]` in same ResultSet
- [ ] Table access order respected (Mstr → Cnfg → Core → Log)

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Error codes catalog | [error-codes.md](assets/error-codes.md) |
| Migration template | [migration-template.sql](assets/migration-template.sql) |
| Folder structure & execution order | [folder-structure.md](assets/folder-structure.md) |

## Related Skills

- **SP Templates**: `database-sp`
- **Error Handling**: `error-handling`
- **Integration**: `dotnet-integration`
