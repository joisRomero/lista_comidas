/* ==============================================================================
-- Object:      {Schema}.Delete{Entity}
-- Author:      {Author}
-- Created:     YYYY-MM-DD
-- Version:     1.0
-- Description: Eliminación lógica de {entity} (RecordStatus = '*')
-- ServiceId:   {ServiceId}
-- Parameters:
--   @ParamI{Entity}Id INT                - ID del registro
--   @ParamIRecordEditUser VARCHAR(50)    - Usuario de auditoría
-- Returns:
--   ResultSet 1: Confirmación con ID eliminado, o Error
-- Security:
--   @ParamIRecordEditUser from HeaderToken
-- ===========================================================================
-- CHANGE HISTORY:
-- Version  Date        Author          Description
-- -------  ----------  --------------  --------------------------------------
-- 1.0      YYYY-MM-DD  {Author}        Creación inicial
============================================================================== */

CREATE OR ALTER PROCEDURE [{Schema}].[Delete{Entity}]
    @ParamI{Entity}Id     INT,
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
        -- PASO 2: Eliminación lógica
        -------------------------------------------------------------------
        UPDATE [{Schema}].[{Entity}]
        SET [RecordStatus]   = '*',
            [RecordEditUser] = @ParamIRecordEditUser,
            [RecordEditDate] = SYSDATETIMEOFFSET()
        WHERE [{Entity}Id] = @ParamI{Entity}Id
          AND [RecordStatus] = 'A';

        -------------------------------------------------------------------
        -- PASO 3: Confirmación
        -------------------------------------------------------------------
        SELECT @ParamI{Entity}Id AS [{Entity}Id],
               'Registro eliminado' AS [Message];

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
    @level1type = N'PROCEDURE', @level1name = N'Delete{Entity}';
GO
