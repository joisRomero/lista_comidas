/* ==============================================================================
-- Object:      {Schema}.Merge{Entity}Items
-- Author:      Development Team
-- Created:     YYYY-MM-DD
-- Version:     1.0
-- Description: Sync {entity} items (bulk INSERT/UPDATE/DELETE)
-- ServiceId:   {ServiceId}
-- Rules:       {Business rules}
-- Parameters:
--   @ParamIParentId (INT): Parent entity ID
--   @ParamIItems (NVARCHAR(MAX)): JSON array of items
--   @ParamIRecordCreationUser (VARCHAR): User executing the operation
-- Returns:
--   ResultSet 1: Updated items list
--   ResultSet 2: Operation summary metadata
-- Security:
--   {Security notes}
-- ===========================================================================
-- CHANGE HISTORY:
-- Version  Date        Author              Description
-- -------  ----------  ------------------  ------------------------------------
-- 1.0      YYYY-MM-DD  Development Team    Initial creation
============================================================================== */

CREATE OR ALTER PROCEDURE [{Schema}].[Merge{Entity}Items]
    @ParamIParentId           INT,
    @ParamIItems              NVARCHAR(MAX),
    @ParamIRecordCreationUser VARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        ---------------------------------------------------------------
        -- PASO 1: Validaciones
        ---------------------------------------------------------------
        IF @ParamIParentId IS NULL
        BEGIN
            SELECT 'VAL_001' AS ErrorCode, 'parentId' AS Field, 'El ID padre es requerido' AS Message;
            RETURN;
        END

        IF @ParamIItems IS NULL OR ISJSON(@ParamIItems) = 0
        BEGIN
            SELECT 'VAL_006' AS ErrorCode, 'items' AS Field, 'El formato de items no es JSON valido' AS Message;
            RETURN;
        END

        IF @ParamIRecordCreationUser IS NULL
        BEGIN
            SELECT 'VAL_001' AS ErrorCode, 'recordCreationUser' AS Field, 'El usuario es requerido' AS Message;
            RETURN;
        END

        IF NOT EXISTS (SELECT 1 FROM [{Schema}].[{ParentEntity}] WHERE {ParentEntity}Id = @ParamIParentId AND RecordStatus = 'A')
        BEGIN
            SELECT '{MOD}_001' AS ErrorCode, 'parentId' AS Field, 'No existe el registro padre especificado' AS Message;
            RETURN;
        END

        ---------------------------------------------------------------
        -- PASO 2: Parsear JSON a tabla temporal
        ---------------------------------------------------------------
        DROP TABLE IF EXISTS #Items;

        SELECT 
            CAST(JSON_VALUE(j.value, '$.itemId') AS INT) AS ItemId,
            JSON_VALUE(j.value, '$.name') AS Name,
            JSON_VALUE(j.value, '$.value') AS Value,
            CAST(JSON_VALUE(j.value, '$.order') AS SMALLINT) AS [Order]
        INTO #Items
        FROM OPENJSON(@ParamIItems) j;

        ---------------------------------------------------------------
        -- PASO 3: Variables de control
        ---------------------------------------------------------------
        DECLARE @VInserted INT = 0;
        DECLARE @VUpdated INT = 0;
        DECLARE @VDeleted INT = 0;

        DECLARE @OutputTable TABLE (
            Action VARCHAR(10),
            ItemId INT
        );

        ---------------------------------------------------------------
        -- PASO 4: MERGE (con transaccion)
        ---------------------------------------------------------------
        BEGIN TRAN;

        MERGE [{Schema}].[{Entity}Item] AS TARGET
        USING #Items AS SOURCE
        ON TARGET.{Entity}ItemId = SOURCE.ItemId
           AND TARGET.{ParentEntity}Id = @ParamIParentId

        WHEN MATCHED AND TARGET.RecordStatus != '*' THEN
            UPDATE SET
                TARGET.Name            = SOURCE.Name,
                TARGET.Value           = SOURCE.Value,
                TARGET.[Order]         = SOURCE.[Order],
                TARGET.RecordEditUser  = @ParamIRecordCreationUser,
                TARGET.RecordEditDate  = SYSDATETIMEOFFSET()

        WHEN NOT MATCHED BY TARGET THEN
            INSERT ({ParentEntity}Id, Name, Value, [Order], RecordCreationUser, RecordCreationDate, RecordStatus)
            VALUES (@ParamIParentId, SOURCE.Name, SOURCE.Value, SOURCE.[Order],
                    @ParamIRecordCreationUser, SYSDATETIMEOFFSET(), 'A')

        WHEN NOT MATCHED BY SOURCE 
             AND TARGET.{ParentEntity}Id = @ParamIParentId 
             AND TARGET.RecordStatus = 'A' THEN
            UPDATE SET
                TARGET.RecordStatus   = '*',
                TARGET.RecordEditUser = @ParamIRecordCreationUser,
                TARGET.RecordEditDate = SYSDATETIMEOFFSET()

        OUTPUT $action, ISNULL(INSERTED.{Entity}ItemId, DELETED.{Entity}ItemId)
        INTO @OutputTable;

        COMMIT TRAN;

        ---------------------------------------------------------------
        -- PASO 5: Contar resultados
        ---------------------------------------------------------------
        SELECT @VInserted = COUNT(*) FROM @OutputTable WHERE Action = 'INSERT';
        SELECT @VUpdated = COUNT(*) FROM @OutputTable WHERE Action = 'UPDATE';
        SELECT @VDeleted = COUNT(*) FROM @OutputTable WHERE Action = 'DELETE';

        ---------------------------------------------------------------
        -- PASO 6: ResultSet 1 - Items actualizados
        ---------------------------------------------------------------
        SELECT 
            {Entity}ItemId AS ItemId,
            Name,
            Value,
            [Order],
            RecordStatus
        FROM [{Schema}].[{Entity}Item]
        WHERE {ParentEntity}Id = @ParamIParentId
          AND RecordStatus = 'A'
        ORDER BY [Order], Name;

        ---------------------------------------------------------------
        -- PASO 7: ResultSet 2 - Metadata
        ---------------------------------------------------------------
        SELECT 
            @VInserted AS Inserted,
            @VUpdated  AS Updated,
            @VDeleted  AS Deleted,
            @VInserted + @VUpdated + @VDeleted AS TotalAffected;

        ---------------------------------------------------------------
        -- PASO 8: Limpieza
        ---------------------------------------------------------------
        DROP TABLE IF EXISTS #Items;

    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0
            ROLLBACK TRAN;

        DROP TABLE IF EXISTS #Items;
        EXEC Log.GetErrorInfo;
    END CATCH
END
GO

-- Extended Property
EXEC sys.sp_addextendedproperty
    @name = N'MS_Description',
    @value = N'{Description}',
    @level0type = N'SCHEMA', @level0name = N'{Schema}',
    @level1type = N'PROCEDURE', @level1name = N'Merge{Entity}Items';
GO
