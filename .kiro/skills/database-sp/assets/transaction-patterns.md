# Transaction Patterns

## When to Use

| Scenario | Transaction? |
|----------|--------------|
| Single table, simple operation | No |
| Multiple related tables | **Yes** |
| Insert header + details | **Yes** |
| Status change + history | **Yes** |

---

## Transaction Template

```sql
CREATE OR ALTER PROCEDURE {Schema}.CreateWithDetails
    @ParamIName               VARCHAR(100),
    @ParamIDetails            NVARCHAR(MAX),  -- JSON array
    @ParamIRecordCreationUser VARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRAN;

        -- Insert header
        INSERT INTO {Schema}.Header (Name, RecordCreationUser)
        VALUES (@ParamIName, @ParamIRecordCreationUser);

        DECLARE @VHeaderId INT = SCOPE_IDENTITY();

        -- Insert details from JSON
        INSERT INTO {Schema}.Detail (HeaderId, Description, RecordCreationUser)
        SELECT @VHeaderId, JSON_VALUE(j.value, '$.description'), @ParamIRecordCreationUser
        FROM OPENJSON(@ParamIDetails) j;

        COMMIT TRAN;

        -- Return created record
        SELECT H.HeaderId, H.Name FROM {Schema}.Header H WHERE H.HeaderId = @VHeaderId;

    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0 ROLLBACK TRAN;
        EXEC Log.GetErrorInfo;
    END CATCH
END
```

---

## Status Change with History

```sql
CREATE OR ALTER PROCEDURE {Schema}.Submit{Entity}
    @ParamI{Entity}Id INT,
    @ParamICurrentUser VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        ---------------------------------------------------------------
        -- PASO 1: Validaciones
        ---------------------------------------------------------------
        DECLARE @VCurrentStatusValue VARCHAR(50);
        DECLARE @VCurrentStatusId INT;
        
        SELECT @VCurrentStatusId = e.CurrentStatusId,
               @VCurrentStatusValue = cs.Value
        FROM {Schema}.{Entity} e WITH(NOLOCK)
        INNER JOIN Cnfg.MasterTable cs WITH(NOLOCK) ON e.CurrentStatusId = cs.MasterTableId
        WHERE e.{Entity}Id = @ParamI{Entity}Id;

        IF @VCurrentStatusValue IS NULL
        BEGIN
            SELECT '{MOD}_001' AS ErrorCode, '{entity}Id' AS Field, 
                   '{Entity} not found' AS Message;
            RETURN;
        END;

        IF @VCurrentStatusValue != 'DRAFT'
        BEGIN
            SELECT '{MOD}_003' AS ErrorCode, 'statusId' AS Field, 
                   'Can only submit from DRAFT status' AS Message;
            RETURN;
        END;

        ---------------------------------------------------------------
        -- PASO 2: Get target status
        ---------------------------------------------------------------
        DECLARE @VNewStatusId INT;
        
        SELECT @VNewStatusId = MasterTableId
        FROM Cnfg.MasterTable WITH(NOLOCK)
        WHERE TableName = '{Entity}Status' AND Value = 'SUBMITTED';

        ---------------------------------------------------------------
        -- PASO 3: Transaction
        ---------------------------------------------------------------
        BEGIN TRAN;

        UPDATE {Schema}.{Entity}
        SET CurrentStatusId = @VNewStatusId,
            RecordEditUser = @ParamICurrentUser,
            RecordEditDate = SYSDATETIMEOFFSET()
        WHERE {Entity}Id = @ParamI{Entity}Id;

        -- Status history
        INSERT INTO {Schema}.StatusHistory
        ({Entity}Id, PreviousStatusId, NewStatusId, ActionName, RecordCreationUser)
        VALUES
        (@ParamI{Entity}Id, @VCurrentStatusId, @VNewStatusId, 'Submit', @ParamICurrentUser);

        COMMIT TRAN;

        ---------------------------------------------------------------
        -- PASO 4: Resultado
        ---------------------------------------------------------------
        SELECT e.{Entity}Id,
               cs.MasterTableId AS [CurrentStatus.MasterTableId],
               cs.Name AS [CurrentStatus.Name],
               cs.Value AS [CurrentStatus.Value]
        FROM {Schema}.{Entity} e WITH(NOLOCK)
        INNER JOIN Cnfg.MasterTable cs WITH(NOLOCK) ON e.CurrentStatusId = cs.MasterTableId
        WHERE e.{Entity}Id = @ParamI{Entity}Id;

    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0 ROLLBACK TRAN;
        EXEC Log.GetErrorInfo;
    END CATCH
END
```

---

## Transaction Rules

| Rule | Description |
|------|-------------|
| `SET XACT_ABORT ON` | Auto-rollback on errors |
| `BEGIN TRAN` / `COMMIT TRAN` | Wrap all related operations |
| `IF XACT_STATE() <> 0 ROLLBACK TRAN` | Check before rollback in CATCH |
| Return after COMMIT | Always return data after successful commit |
| SELECTs outside TRAN | Read-only SELECTs go after COMMIT, not inside the transaction |

---

## XACT_STATE vs @@TRANCOUNT

| Function | What it indicates | When to use |
|----------|-------------------|-------------|
| `@@TRANCOUNT` | Number of active nested transactions | Only to verify nesting |
| `XACT_STATE()` | State: 1=active, 0=none, -1=uncommittable | **Always for ROLLBACK** |

> **Important:** `XACT_STATE()` detects "uncommittable" transactions that `@@TRANCOUNT` cannot. Always use `XACT_STATE() <> 0` before ROLLBACK in CATCH blocks.
