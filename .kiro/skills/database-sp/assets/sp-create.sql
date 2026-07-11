/* ==============================================================================
-- Object:      {Schema}.Create{Entity}
-- Author:      {Author}
-- Created:     YYYY-MM-DD
-- Version:     1.0
-- Description: Crea un nuevo registro de {entity}
-- ServiceId:   {ServiceId}
-- Rules:       {Business rules, e.g. RN-XXX-001..003}
-- Parameters:
--   @ParamIName VARCHAR(100)             - Nombre del registro
--   @ParamIRecordCreationUser VARCHAR(50)- Usuario de auditoría
-- Returns:
--   ResultSet 1: Registro creado con JOINs completos, o Error
-- Security:
--   @ParamIRecordCreationUser from HeaderToken
-- ===========================================================================
-- CHANGE HISTORY:
-- Version  Date        Author          Description
-- -------  ----------  --------------  --------------------------------------
-- 1.0      YYYY-MM-DD  {Author}        Creación inicial
============================================================================== */

CREATE OR ALTER PROCEDURE [{Schema}].[Create{Entity}]
    @ParamIName               VARCHAR(100),
    @ParamIRecordCreationUser VARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        -------------------------------------------------------------------
        -- CONSTANTS
        -------------------------------------------------------------------
        -- DECLARE @CDefaultStatusId INT = {StatusId};

        -------------------------------------------------------------------
        -- VARIABLES
        -------------------------------------------------------------------
        DECLARE @VNewId INT;

        -------------------------------------------------------------------
        -- PASO 1: Validaciones
        -------------------------------------------------------------------
        -- Duplicate check
        IF EXISTS (
            SELECT 1 FROM [{Schema}].[{Entity}]
            WHERE [Name] = @ParamIName AND [RecordStatus] = 'A'
        )
        BEGIN
            SELECT '{MOD}_002' AS ErrorCode,
                   'name' AS Field,
                   'Ya existe un registro con este nombre' AS Message;
            RETURN;
        END

        -- Authorization check pattern (when needed):
        -- IF @VHasPermission = 0
        -- BEGIN
        --     SELECT 'AUTH_UNAUTHORIZED' AS ErrorCode,
        --            'employeeId' AS Field,
        --            'No tiene permiso para esta operación' AS Message;
        --     RETURN;
        -- END

        -------------------------------------------------------------------
        -- PASO 2: INSERT
        -------------------------------------------------------------------
        INSERT INTO [{Schema}].[{Entity}] (
            [Name],
            [RecordCreationUser],
            [RecordStatus]
        )
        VALUES (
            @ParamIName,
            @ParamIRecordCreationUser,
            'A'
        );

        SET @VNewId = SCOPE_IDENTITY();

        -------------------------------------------------------------------
        -- PASO 3: Retornar registro creado con JOINs
        -------------------------------------------------------------------
        SELECT
            t.[{Entity}Id],
            t.[Name],
            -- CONCAT_WS for full names, dot notation for nested objects
            t.[RecordCreationDate]
        FROM [{Schema}].[{Entity}] t WITH(NOLOCK)
        WHERE t.[{Entity}Id] = @VNewId;

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
    @level1type = N'PROCEDURE', @level1name = N'Create{Entity}';
GO
