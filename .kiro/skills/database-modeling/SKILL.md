---
name: database-modeling
description: >
  Data modeling standards for SQL Server: schemas, table design, column types, constraints, indexes,
  triggers, functions, views, CTEs, and transactions.
  Trigger: When designing tables, creating schemas, adding constraints, or modeling data structures.
metadata:
  author: anta
  version: "1.0"
  scope: [root]
  enforcement: mandatory
  auto_invoke: "modelado, tabla, columna, constraint, índice, esquema, foreign key, primary key, CREATE TABLE, diseño de datos"
  phase: [inception, construction]
  layer: [database]
  validates_with: validate_db_schema
  validation_profile: conventions-lint
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| PK with IDENTITY must use DESC ordering | ALWAYS | Recent records first, better query performance |
| Booleans must be `BIT NOT NULL DEFAULT 0` | ALWAYS | Avoid NULL logic complexity |
| Dates must be `DATETIMEOFFSET(7)` | ALWAYS | Timezone-aware consistency |
| Tables must be singular UpperCamelCase | ALWAYS | Naming consistency |
| Max 50 chars for table names | ALWAYS | Avoid truncation in tooling |
| Check Constraint mandatory on RecordStatus | ALWAYS | Data integrity |
| Prefer INT IDENTITY for internal PKs | ALWAYS | Best performance for internal tables |
| Use GUID only for external integration | CONDITIONAL | Sync between distributed systems |

---

## Schemas

### Standard Schemas (All Applications)

| Schema | Purpose | Examples |
|--------|---------|----------|
| `Log` | Logging and errors | LogDB, GetErrorInfo |
| `Sec` | Security/Auth | Users, Roles, Permissions |
| `Cnfg` | Configuration/Catalogs | MasterTable, Settings |
| `Core` | Core transactional business | Base transactional tables |
| `Mstr` | Masters | Person, Company, OrganizationalUnit |
| `Ext` | External data (Workers/Jobs) | SAP_Vendors, ERP_Materials |
| `Rpt` | Reports | Optimized views for reports |

### Custom Schemas (Per Application)

Each application defines additional schemas following same naming rules.

| Example App | Custom Schema | Tables |
|-------------|---------------|--------|
| ContractsCommittee | `Cases` | GeneralData, Provider, Document |
| Procurement | `Orders` | PurchaseOrder, OrderItem, Supplier |

---

## Database Naming

| Object | Pattern | Style | Example |
|--------|---------|-------|---------|
| Database | `{Env}_{Name}` | UpperCamelCase | `Dev_ContractsCommittee` |
| Schema | User-defined per module | Short, meaningful | `HR`, `Cases`, `Cnfg`, `Ext` |
| Table | `{Schema}.{Name}` | Singular UpperCamelCase | `Cases.GeneralData`, `HR.Employee` |
| Collation | `SQL_Latin1_General_CP1_CI_AS` | — | — |

### Schema Selection Rules
- **Schema MUST be the one chosen by the user** during Requirements Analysis — do NOT abbreviate or invent alternatives
- If user says `HR`, use `HR` — NOT `Emp`, `Empl`, `RRHH`, or any other variation
- Schema name should be short (2-4 chars) and domain-meaningful
- Standard schemas: `Log`, `Sec`, `Cnfg`, `Core`, `Mstr`, `Ext`, `Rpt` (see Schemas section below)
- Custom schemas are per-module: `HR`, `Cases`, `Sessions`, `Orders`, etc.

---

## Column Types

| Type | Pattern | Data Type | Example |
|------|---------|-----------|---------|
| Primary Key | `{TableName}Id` | INT/BIGINT/UNIQUEIDENTIFIER | `GeneralDataId` |
| Foreign Key | `{ReferencedTable}Id` | Same as referenced PK | `DocumentTypeId` |
| Boolean | `Is{Name}` | `BIT NOT NULL DEFAULT 0` | `IsActive`, `IsDeleted` |
| Date | `{Name}Date` | `DATETIMEOFFSET(7)` | `CreationDate` |
| General | UpperCamelCase | As needed | `Name`, `Amount` |

### ID Type Selection

| Type | When to Use |
|------|-------------|
| `INT IDENTITY(1,1)` | **Default** — internal tables, best performance |
| `BIGINT IDENTITY(1,1)` | High-volume tables (>2 billion rows) |
| `UNIQUEIDENTIFIER` | External integration, distributed sync, public APIs |

### PK Ordering (IDENTITY)

```sql
-- Correct: DESC for IDENTITY PKs
CONSTRAINT PK_{Schema}_{Table} PRIMARY KEY CLUSTERED ({Table}Id DESC)

-- Wrong: ASC default (avoid)
CONSTRAINT PK_{Schema}_{Table} PRIMARY KEY CLUSTERED ({Table}Id)
```

> GUID PKs use ASC (NEWSEQUENTIALID() already generates ordered values).

---

## Constraints and Indexes

### Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| Primary Key | `PK_{Schema}_{Table}` | `PK_Cases_GeneralData` |
| Foreign Key | `FK_{Schema}_{Table}_{Relation}` | `FK_Cases_GeneralData_DocumentType` |
| Unique | `UN_{Schema}_{Table}_{Columns}` | `UN_Mstr_Person_DocumentNumber` |
| Check | `CK_{Schema}_{Table}_{Column}` | `CK_Cnfg_MasterTable_RecordStatus` |
| Index NC | `IXN_{Schema}_{Table}_{Columns}` | `IXN_Cases_GeneralData_CurrentStatusId` |
| Index C | `IXC_{Schema}_{Table}_{Columns}` | `IXC_Cases_GeneralData_GeneralDataId` |
| Default | `DF_{Schema}_{Table}_{Column}` | `DF_Cases_GeneralData_RecordStatus` |

### Index Best Practices

#### INCLUDE Clause (Mandatory for Performance)

**All nonclustered indexes SHOULD use INCLUDE** to avoid expensive key lookups:

```sql
-- Correct: INCLUDE frequently queried columns
CREATE NONCLUSTERED INDEX IXN_Cases_GeneralData_CurrentStatusId
ON Cases.GeneralData (CurrentStatusId)
INCLUDE (CaseCode, CaseName, EstimatedAmount, RecordCreationDate)
WHERE RecordStatus = 'A';

-- Wrong: Missing INCLUDE causes lookups to clustered index
CREATE NONCLUSTERED INDEX IXN_Cases_GeneralData_CurrentStatusId
ON Cases.GeneralData (CurrentStatusId)
WHERE RecordStatus = 'A';
```

**INCLUDE Guidelines**:
- Include columns frequently selected in queries using this index
- Include columns used in WHERE/JOIN but not in the index key
- Typical INCLUDE: 3-5 columns most commonly accessed
- Balance: More columns = larger index but faster queries
- Review query patterns to determine optimal INCLUDE columns

#### Filtered Indexes

Use WHERE clause to index only active records:

```sql
CREATE NONCLUSTERED INDEX IXN_Cases_GeneralData_CaseCode
ON Cases.GeneralData (CaseCode)
INCLUDE (CaseName, CurrentStatusId)
WHERE RecordStatus = 'A';
```

---

## Table Template

```sql
CREATE TABLE {Schema}.{Table} (
    {Table}Id              INT IDENTITY(1,1) NOT NULL,
    -- business columns...
    RecordCreationUser     VARCHAR(50) NOT NULL,
    RecordCreationDate     DATETIMEOFFSET(7) NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    RecordEditUser         VARCHAR(50) NULL,
    RecordEditDate         DATETIMEOFFSET(7) NULL,
    RecordStatus           CHAR(1) NOT NULL DEFAULT 'A',

    CONSTRAINT PK_{Schema}_{Table} PRIMARY KEY CLUSTERED ({Table}Id DESC),
    CONSTRAINT CK_{Schema}_{Table}_RecordStatus CHECK (RecordStatus IN ('A', 'I', '*'))
);
```

---

## Triggers

| Type | Pattern | Example |
|------|---------|---------|
| After Insert | `TR_{Schema}_{Table}_AI` | `TR_Cases_GeneralData_AI` |
| After Update | `TR_{Schema}_{Table}_AU` | `TR_Cases_GeneralData_AU` |
| After Delete | `TR_{Schema}_{Table}_AD` | `TR_Cases_GeneralData_AD` |
| Instead Of | `TR_{Schema}_{Table}_IO` | `TR_Cases_GeneralData_IO` |

> **Avoid triggers when possible.** Prefer logic in SPs.

---

## Functions and Views

| Type | Pattern | Example |
|------|---------|---------|
| Scalar Function | `{Schema}.{Name}` | `Cnfg.IsReservedWord` |
| Table Function | `{Schema}.Get{Name}` | `Cnfg.GetCatalogItemsByParent` |
| View | `{Schema}.VW_{Name}` | `Rpt.VW_CasesWithStatus` |

### Function Rules

| Rule | Description |
|------|-------------|
| Avoid scalar functions in WHERE | Prevents index usage |
| Prefer Inline TVF | Better performance than Multi-Statement TVF |
| No GETDATE() in functions | Pass dates as parameters |

### View Rules

| Rule | Description |
|------|-------------|
| No `SELECT *` | Specify columns |
| `WITH(NOLOCK)` | For report views |
| No nested views | Max 1 nesting level |
| Schema `Rpt` | Report views go in Rpt schema |

---

## CTEs vs Temp Tables

| Scenario | Use CTE | Use #Temp |
|----------|---------|-----------|
| Simple query, one-time use | ✅ | ❌ |
| Hierarchical data (tree) | ✅ Recursive | ❌ |
| Reuse result multiple times | ❌ | ✅ |
| Large source (>100k rows) | ❌ | ✅ with index |
| Pagination over filtered data | ❌ | ✅ |

---

## Transactions

| Scenario | Transaction? | Reason |
|----------|-------------|--------|
| Single table, simple | ❌ No | SQL Server is atomic per statement |
| Multiple related tables | ✅ Required | All or nothing |
| MERGE with additional logic | ✅ Required | Coordinate operations |
| SELECT only | ❌ No | No data modification |
| Calls to other modifying SPs | ✅ Required | Coordinate rollback |

### Transaction Rules

| Rule | Description |
|------|-------------|
| `SET XACT_ABORT ON` | **Mandatory** — auto rollback on error |
| `XACT_STATE() <> 0` | Use instead of `@@TRANCOUNT` for rollback |
| Minimal scope | Open transaction as late as possible |
| No SELECTs inside | Read queries go outside the transaction |
| No nesting | Avoid nested transactions |
| Table access order | `Mstr → Cnfg → Core/{Custom} → Log` (prevents deadlocks) |

---

## Extended Properties (Documentation)

Document all database objects using `sys.sp_addextendedproperty`:

```sql
-- Table
EXEC sys.sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Transaction records for operational workflows', 
    @level0type = N'SCHEMA', @level0name = N'Core',
    @level1type = N'TABLE', @level1name = N'Transaction';

-- Column
EXEC sys.sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'FK to Cnfg.MasterTable for transaction status', 
    @level0type = N'SCHEMA', @level0name = N'Core',
    @level1type = N'TABLE', @level1name = N'Transaction',
    @level2type = N'COLUMN', @level2name = N'StatusId';

-- Index
EXEC sys.sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Index for status-based transaction lookups', 
    @level0type = N'SCHEMA', @level0name = N'Core',
    @level1type = N'TABLE', @level1name = N'Transaction',
    @level2type = N'INDEX', @level2name = N'IXN_Core_Transaction_StatusId';
```

---

## Checklist

- [ ] Table uses correct schema (Log/Sec/Cnfg/Core/Mstr/Ext/Rpt/Custom)
- [ ] Table name is singular UpperCamelCase, max 50 chars
- [ ] PK follows `{Table}Id` pattern with correct type
- [ ] PK with IDENTITY uses DESC ordering
- [ ] Booleans are `BIT NOT NULL DEFAULT 0`
- [ ] Dates are `DATETIMEOFFSET(7)`
- [ ] All constraints follow naming convention
- [ ] Nonclustered indexes use **INCLUDE** clause with 3-5 frequently queried columns
- [ ] Extended Properties added for tables, key columns, and indexes
- [ ] RecordStatus has CHECK constraint
- [ ] Transaction rules applied (single vs multi-table)

---

## Related Skills

| Task | Skill |
|------|-------|
| Audit columns, soft delete, Log schema | `database-audit` |
| SP naming, parameters, error codes | `database` |
| SP templates (List, Get, Create, etc.) | `database-sp` |
