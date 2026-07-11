# Error Codes Catalog

## Validation Errors (VAL_)

| Code | Description |
|------|-------------|
| VAL_001 | Required field |
| VAL_002 | Invalid format |
| VAL_003 | SQL reserved word |
| VAL_004 | Invalid characters |
| VAL_005 | Invalid date range |
| VAL_006 | Invalid JSON |
| VAL_007 | Value out of range |
| VAL_008 | Length exceeded |

## Module Errors ({MOD}_)

| Code | Description | HTTP |
|------|-------------|------|
| {MOD}_001 | Entity not found | 404 |
| {MOD}_002 | Duplicate/Conflict | 409 |
| {MOD}_003 | Entity in use (cannot delete) | 422 |
| {MOD}_004 | Status does not allow this operation | 422 |
| {MOD}_005 | Limit exceeded | 422 |

Replace `{MOD}` with module prefix: USER, ORDER, CASE, etc.

## Auth Errors (AUTH_)

| Code | Description |
|------|-------------|
| AUTH_001 | Not authorized |
| AUTH_002 | Token expired |
| AUTH_003 | Insufficient permissions |

## System Errors (SYS_)

| Code | Description |
|------|-------------|
| SYS_001 | Internal error (logged) |
| SYS_002 | Database connection error |
| SYS_003 | External service error |

---

## Log.LogDB Table

```sql
CREATE TABLE [Log].[LogDB] (
    [LogDBId]           INT IDENTITY(1,1) NOT NULL,
    [ErrorNumber]       INT NULL,
    [ErrorSeverity]     INT NULL,
    [ErrorState]        INT NULL,
    [ErrorProcedure]    VARCHAR(150) NULL,
    [ErrorLine]         INT NULL,
    [ErrorMessage]      VARCHAR(500) NULL,
    [CreateDate]        DATETIMEOFFSET(7) NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    CONSTRAINT [PK_LogDB] PRIMARY KEY CLUSTERED ([LogDBId] DESC)
);
```

## Log.GetErrorInfo (v2.4 — with internal TRY/CATCH)

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

    -- Return structured error compatible with ApiError
    SELECT
        'SYS_001' AS ErrorCode,
        CAST(NULL AS VARCHAR(100)) AS Field,
        CASE
            WHEN @VLogId > 0 THEN CONCAT('Error interno [Ref:', @VLogId, ']')
            ELSE CONCAT('Error interno [', @VErrorProcedure, ':', @VErrorLine, ']')
        END AS Message;
END
```

---

## Log.AuditHttp Table

```sql
CREATE TABLE [Log].[AuditHttp] (
    [AuditHttpId]       INT IDENTITY(1,1) NOT NULL,
    [HttpStatusCode]    INT NULL,
    [UrlScheme]         VARCHAR(50) NULL,
    [HostPort]          VARCHAR(200) NULL,
    [Path]              VARCHAR(500) NULL,
    [Method]            VARCHAR(10) NULL,
    [RequestHeader]     NVARCHAR(MAX) NULL,
    [RequestBody]       NVARCHAR(MAX) NULL,
    [ResponseHeader]    NVARCHAR(MAX) NULL,
    [ResponseBody]      NVARCHAR(MAX) NULL,
    [CorrelationId]     VARCHAR(50) NULL,
    [IpAddress]         VARCHAR(50) NULL,
    [Duration]          VARCHAR(20) NULL,
    [CreateDate]        DATETIMEOFFSET(7) NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    CONSTRAINT [PK_AuditHttp] PRIMARY KEY CLUSTERED ([AuditHttpId] DESC)
);
```

## Log.LogJob Table

```sql
CREATE TABLE [Log].[LogJob] (
    [LogJobId]          INT IDENTITY(1,1) NOT NULL,
    [NameJob]           VARCHAR(200) NULL,
    [StateJob]          VARCHAR(50) NULL,      -- Started, Completed, Failed
    [CorrelationId]     VARCHAR(50) NULL,
    [Duration]          VARCHAR(20) NULL,
    [Exception]         NVARCHAR(MAX) NULL,
    [InnerException]    NVARCHAR(MAX) NULL,
    [StackTrace]        NVARCHAR(MAX) NULL,
    [Data]              NVARCHAR(MAX) NULL,    -- Additional JSON
    [Message]           NVARCHAR(500) NULL,
    [CreateDateOnly]    DATE NULL,
    [CreateDate]        DATETIMEOFFSET(7) NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    CONSTRAINT [PK_LogJob] PRIMARY KEY CLUSTERED ([LogJobId] DESC)
);
```
