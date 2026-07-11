# Database Folder Structure

```
database/
├── README.md                           # Documentation (tables, SPs, dependencies)
├── {Schema}/
│   ├── 00_Schema.sql                   # CREATE SCHEMA {Schema}
│   ├── 01_Tables.sql                   # Table definitions
│   ├── StoredProcedures/               # All SPs for this schema
│   │   └── {Schema}.{Action}{Entity}.sql
│   └── Migrations/                     # Incremental changes
│       └── YYYYMMDD_{Description}.sql
└── _archive/                           # Backup of deprecated files (optional)
```

## File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Schema | `00_Schema.sql` | `00_Schema.sql` |
| Tables | `01_Tables.sql` | `01_Tables.sql` |
| Stored Procedure | `{Schema}.{Action}{Entity}.sql` | `Cases.CreateCase.sql` |
| Migration | `YYYYMMDD_{Description}.sql` | `20251229_AddReviewContext.sql` |

## Execution Order

### First Time (New Database)

```bash
# 1. Shared schemas (if not exist)
database-shared/Log/00_Schema.sql
database-shared/Log/01_Tables.sql
database-shared/Log/StoredProcedures/Log.GetErrorInfo.sql

# 2. Config schema (catalogs)
Cnfg/00_Schema.sql
Cnfg/01_Tables.sql
Cnfg/01_Insert_Catalogs.sql

# 3. Application schema
{Schema}/00_Schema.sql
{Schema}/01_Tables.sql
{Schema}/StoredProcedures/*.sql
```

### Updates Only

```bash
# Modified SPs
{Schema}/StoredProcedures/{Modified_SP}.sql

# Structural changes
{Schema}/Migrations/YYYYMMDD_{Description}.sql
```

## When to Use Migrations

| Change Type | Use Migration? |
|-------------|----------------|
| New SP | No - add to StoredProcedures/ |
| Modify SP | No - update existing file |
| Add table column | **Yes** |
| Add index | **Yes** |
| Insert catalog data | **Yes** |
| Structural changes | **Yes** |
