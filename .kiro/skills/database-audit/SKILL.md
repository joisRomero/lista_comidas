---
name: database-audit
description: >
  Audit columns, logging tables, and error capture for SQL Server.
  Covers RecordStatus soft delete, Log schema (LogDB, AuditHttp, LogJob), and GetErrorInfo SP.
  Trigger: When creating tables with audit columns, implementing error logging, or HTTP auditing.
metadata:
  author: anta
  version: "1.0"
  scope: [root]
  enforcement: mandatory
  auto_invoke: "auditoría, audit, RecordStatus, LogDB, GetErrorInfo, AuditHttp, soft delete, log de errores"
  phase: [inception, construction]
  layer: [database]
  validates_with: validate_audit_columns
  validation_profile: conventions-lint
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| ALL transactional tables MUST have 5 audit columns | ALWAYS | Consistent tracking of who/when/status |
| RecordStatus MUST be `CHAR(1) NOT NULL DEFAULT 'A'` with CHECK constraint | ALWAYS | Prevents NULL ambiguity |
| Use `SYSDATETIMEOFFSET()` for all dates | ALWAYS | Timezone-aware timestamps |
| Soft delete sets `RecordStatus = '*'`, NEVER physical DELETE | ALWAYS | Audit trail preservation |
| ALWAYS filter `RecordStatus = 'A'` in JOINs | ALWAYS | Prevent stale data leaks |
| Error capture via `Log.GetErrorInfo` in every CATCH | ALWAYS | Centralized error logging |

---

## Audit Columns (Mandatory on Transactional Tables)

| Column | Type | Description |
|--------|------|-------------|
| `RecordCreationUser` | `VARCHAR(50) NOT NULL` | User who created the record |
| `RecordCreationDate` | `DATETIMEOFFSET(7) NOT NULL DEFAULT SYSDATETIMEOFFSET()` | Creation timestamp with timezone |
| `RecordEditUser` | `VARCHAR(50) NULL` | User who last modified |
| `RecordEditDate` | `DATETIMEOFFSET(7) NULL` | Last modification timestamp |
| `RecordStatus` | `CHAR(1) NOT NULL DEFAULT 'A'` | A=Active, I=Inactive, *=Deleted |

### RecordStatus Values

| Value | Meaning | Usage |
|-------|---------|-------|
| `A` | Active | Default for new records, visible in all queries |
| `I` | Inactive | Disabled but may be visible in admin views |
| `*` | Logical Delete | Soft-deleted, ALWAYS filtered out (`RecordStatus = 'A'` in JOINs) |

### Check Constraint (Mandatory)

```sql
CONSTRAINT CK_{Schema}_{Table}_RecordStatus CHECK (RecordStatus IN ('A', 'I', '*'))
```

### User Parameters in SPs

| Operation | Required Parameter |
|-----------|--------------------|
| CREATE | `@ParamIRecordCreationUser VARCHAR(50)` |
| UPDATE | `@ParamIRecordEditUser VARCHAR(50)` |
| DELETE (soft) | `@ParamIRecordEditUser VARCHAR(50)` |

---

## Soft Delete Pattern

```sql
-- DELETE = UPDATE RecordStatus to '*'
UPDATE {Schema}.{Table}
SET RecordStatus   = '*',
    RecordEditUser = @ParamIRecordEditUser,
    RecordEditDate = SYSDATETIMEOFFSET()
WHERE {Table}Id = @ParamIId;
```

### JOINs — Always Filter RecordStatus

```sql
SELECT h.*, d.*
FROM {Schema}.HeaderTable h WITH(NOLOCK)
INNER JOIN {Schema}.DetailTable d WITH(NOLOCK)
    ON h.HeaderId = d.HeaderId
    AND d.RecordStatus = 'A'  -- ← NEVER forget in JOINs
WHERE h.RecordStatus = 'A';
```

---

## Log Schema Tables

| Table | Purpose | Source |
|-------|---------|--------|
| `Log.LogDB` | DB errors (SP CATCH blocks) | SQL Server |
| `Log.AuditHttp` | Incoming HTTP requests | Clients → API |
| `Log.AuditEndpoint` | Outgoing HTTP calls | API → External |
| `Log.LogHttp` | HTTP exceptions | Middleware |
| `Log.LogJob` | Background job execution | Workers |

### Log.LogDB

```sql
CREATE TABLE [Log].[LogDB] (
    [LogDBId]         INT IDENTITY(1,1) NOT NULL,
    [ErrorNumber]     INT NULL,
    [ErrorSeverity]   INT NULL,
    [ErrorState]      INT NULL,
    [ErrorProcedure]  VARCHAR(150) NULL,
    [ErrorLine]       INT NULL,
    [ErrorMessage]    VARCHAR(500) NULL,
    [CreateDate]      DATETIMEOFFSET(7) NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    CONSTRAINT [PK_LogDB] PRIMARY KEY CLUSTERED ([LogDBId] DESC)
);
```

### Log.AuditHttp

```sql
CREATE TABLE [Log].[AuditHttp] (
    [AuditHttpId]    INT IDENTITY(1,1) NOT NULL,
    [HttpStatusCode] INT NULL,
    [UrlScheme]      VARCHAR(50) NULL,
    [HostPort]       VARCHAR(200) NULL,
    [Path]           VARCHAR(500) NULL,
    [Method]         VARCHAR(10) NULL,
    [RequestHeader]  NVARCHAR(MAX) NULL,
    [RequestBody]    NVARCHAR(MAX) NULL,
    [ResponseHeader] NVARCHAR(MAX) NULL,
    [ResponseBody]   NVARCHAR(MAX) NULL,
    [CorrelationId]  VARCHAR(50) NULL,
    [IpAddress]      VARCHAR(50) NULL,
    [Duration]       VARCHAR(20) NULL,
    [CreateDate]     DATETIMEOFFSET(7) NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    CONSTRAINT [PK_AuditHttp] PRIMARY KEY CLUSTERED ([AuditHttpId] DESC)
);
```

### Log.LogJob

```sql
CREATE TABLE [Log].[LogJob] (
    [LogJobId]       INT IDENTITY(1,1) NOT NULL,
    [NameJob]        VARCHAR(200) NULL,
    [StateJob]       VARCHAR(50) NULL,      -- Started, Completed, Failed
    [CorrelationId]  VARCHAR(50) NULL,
    [Duration]       VARCHAR(20) NULL,
    [Exception]      NVARCHAR(MAX) NULL,
    [InnerException] NVARCHAR(MAX) NULL,
    [StackTrace]     NVARCHAR(MAX) NULL,
    [Data]           NVARCHAR(MAX) NULL,
    [Message]        NVARCHAR(500) NULL,
    [CreateDateOnly] DATE NULL,
    [CreateDate]     DATETIMEOFFSET(7) NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    CONSTRAINT [PK_LogJob] PRIMARY KEY CLUSTERED ([LogJobId] DESC)
);
```

---

## Error Capture SP

```sql
CREATE OR ALTER PROCEDURE [Log].[GetErrorInfo]
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @VErrorNumber INT = ERROR_NUMBER();
    DECLARE @VErrorSeverity INT = ERROR_SEVERITY();
    DECLARE @VErrorState INT = ERROR_STATE();
    DECLARE @VErrorProcedure VARCHAR(150) = ERROR_PROCEDURE();
    DECLARE @VErrorLine INT = ERROR_LINE();
    DECLARE @VErrorMessage VARCHAR(500) = ERROR_MESSAGE();
    DECLARE @VCreateDate DATETIMEOFFSET(7) = SYSDATETIMEOFFSET();
    DECLARE @VLogId INT;

    BEGIN TRY
        INSERT INTO [Log].[LogDB] (
            ErrorNumber, ErrorSeverity, ErrorState,
            ErrorProcedure, ErrorLine, ErrorMessage, CreateDate
        )
        VALUES (
            @VErrorNumber, @VErrorSeverity, @VErrorState,
            @VErrorProcedure, @VErrorLine, @VErrorMessage, @VCreateDate
        );
        SET @VLogId = SCOPE_IDENTITY();
    END TRY
    BEGIN CATCH
        SET @VLogId = -1;
    END CATCH

    -- Return compatible with ApiError
    SELECT
        'SYS_001' AS ErrorCode,
        CAST(NULL AS VARCHAR(100)) AS Field,
        CASE
            WHEN @VLogId > 0 THEN CONCAT('Error interno [Ref:', @VLogId, ']')
            ELSE CONCAT('Error interno [', @VErrorProcedure, ':', @VErrorLine, ']')
        END AS Message;
END
```

### Usage in SPs

```sql
BEGIN TRY
    -- SP logic...
END TRY
BEGIN CATCH
    IF XACT_STATE() <> 0
        ROLLBACK TRANSACTION;

    EXEC Log.GetErrorInfo;  -- Logs and returns structured error
END CATCH
```

---

## Checklist

- [ ] All transactional tables have 5 audit columns
- [ ] RecordStatus has CHECK constraint (`A`, `I`, `*`)
- [ ] All dates use `DATETIMEOFFSET(7)` with `SYSDATETIMEOFFSET()`
- [ ] Soft delete updates RecordStatus, never physical DELETE
- [ ] All JOINs filter `RecordStatus = 'A'`
- [ ] Log.LogDB table exists in Log schema
- [ ] Log.GetErrorInfo SP exists and is called in every CATCH
- [ ] CREATE SPs require `@ParamIRecordCreationUser`
- [ ] UPDATE/DELETE SPs require `@ParamIRecordEditUser`

---

## Related Skills

| Task | Skill |
|------|-------|
| Database naming, schemas, columns | `database` |
| SP templates (List, Get, Create, Update, Delete) | `database-sp` |
| Data modeling (tables, constraints, indexes) | `database-modeling` |
