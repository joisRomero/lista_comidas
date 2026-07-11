/* ==============================================================================
-- Object:      {Schema}.Update{Entity}
-- Author:      {Author}
-- Created:     YYYY-MM-DD
-- Version:     1.0
-- Description: Actualiza un registro existente de {entity}
-- ServiceId:   {ServiceId}
-- Parameters:
--   @ParamI{Entity}Id INT                - ID del registro
--   @ParamIName VARCHAR(100)             - Nuevo nombre
--   @ParamIRecordEditUser VARCHAR(50)    - Usuario de auditoría
-- Returns:
--   ResultSet 1: Registro actualizado con JOINs completos, o Error
-- Security:
--   @ParamIRecordEditUser from HeaderToken
-- ===========================================================================
-- CHANGE HISTORY:
-- Version  Date        Author          Description
-- -------  ----------  --------------  --------------------------------------
-- 1.0      YYYY-MM-DD  {Author}        Creación inicial
============================================================================== */

CREATE OR ALTER PROCEDURE [{Schema}].[Update{Entity}]
    @ParamI{Entity}Id     INT,
    @ParamIName           VARCHAR(100),
    @ParamIRecordEditUser VARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        -------------------------------------------------------------------
        -- PASO 1: Validaciones
        -------------------------------------------------------------------
        IF NOT EXISTS (
            SELECT 1 FROM [{Schema}].[{Entity}]
            WHERE [{Entity}Id] = @ParamI{Entity}Id
              AND [RecordStatus] = 'A'
        )
        BEGIN
            SELECT 'NOT_FOUND' AS ErrorCode,
                   '{entity}Id' AS Field,
                   '{Entity} no encontrado' AS Message;
            RETURN;
        END

        -------------------------------------------------------------------
        -- PASO 2: UPDATE
        -------------------------------------------------------------------
        UPDATE [{Schema}].[{Entity}]
        SET [Name]           = @ParamIName,
            [RecordEditUser] = @ParamIRecordEditUser,
            [RecordEditDate] = SYSDATETIMEOFFSET()
        WHERE [{Entity}Id] = @ParamI{Entity}Id
          AND [RecordStatus] = 'A';

        -------------------------------------------------------------------
        -- PASO 3: Retornar registro actualizado con JOINs
        -------------------------------------------------------------------
        SELECT
            t.[{Entity}Id],
            t.[Name],
            t.[RecordEditUser],
            t.[RecordEditDate]
        FROM [{Schema}].[{Entity}] t WITH(NOLOCK)
        WHERE t.[{Entity}Id] = @ParamI{Entity}Id;

    END TRY
    BEGIN CATCH
        EXEC [Log].[GetErrorInfo];
    END CATCH
END
GO

EXEC sys.sp_addextendedproperty
    @name = N'MS_Description',
    @value = N'{Description}',
    @level0type = N'SCHEMA', @level0name = N'{Schema}',
    @level1type = N'PROCEDURE', @level1name = N'Update{Entity}';
GO
