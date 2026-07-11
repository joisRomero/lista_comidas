/* ==============================================================================
-- Object:      {Schema}.Get{Entity}
-- Author:      {Author}
-- Created:     YYYY-MM-DD
-- Version:     1.0
-- Description: Obtiene detalle completo de {entity} por ID
-- ServiceId:   {ServiceId}
-- Parameters:
--   @ParamI{Entity}Id INT - ID del registro
-- Returns:
--   ResultSet 1: Detalle completo del registro con JOINs, o Error
-- ===========================================================================
-- CHANGE HISTORY:
-- Version  Date        Author          Description
-- -------  ----------  --------------  --------------------------------------
-- 1.0      YYYY-MM-DD  {Author}        Creación inicial
============================================================================== */

CREATE OR ALTER PROCEDURE [{Schema}].[Get{Entity}]
    @ParamI{Entity}Id INT
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        -------------------------------------------------------------------
        -- PASO 1: Validar existencia
        -------------------------------------------------------------------
        IF NOT EXISTS (
            SELECT 1
            FROM [{Schema}].[{Entity}] WITH(NOLOCK)
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
        -- PASO 2: Retornar detalle completo
        -------------------------------------------------------------------
        SELECT
            t.[{Entity}Id],
            t.[Name],
            -- Full name pattern:
            -- CONCAT_WS(' ', e.[FirstName], e.[MiddleName], e.[ThirdName],
            --     e.[LastName], e.[SecondLastName]) AS [EmployeeName],
            -- Nested object pattern:
            -- s.[MasterTableId] AS [Status.MasterTableId],
            -- s.[Name]          AS [Status.Name],
            -- s.[Value]         AS [Status.Value],
            t.[RecordCreationUser],
            t.[RecordCreationDate],
            t.[RecordEditUser],
            t.[RecordEditDate]
        FROM [{Schema}].[{Entity}] t WITH(NOLOCK)
        -- INNER JOIN [Maintenance].[MasterTable] s WITH(NOLOCK)
        --     ON t.[StatusId] = s.[MasterTableId]
        WHERE t.[{Entity}Id] = @ParamI{Entity}Id
          AND t.[RecordStatus] = 'A';

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
    @level1type = N'PROCEDURE', @level1name = N'Get{Entity}';
GO
