/* ==============================================================================
-- Object:      {Schema}.List{Entity}
-- Author:      {Author}
-- Created:     YYYY-MM-DD
-- Version:     1.0
-- Description: Listado paginado de {entities} con filtros y ordenamiento
-- ServiceId:   {ServiceId}
-- Parameters:
--   @ParamIPage INT              - Número de página (default 1)
--   @ParamIPageSize INT          - Tamaño de página (default 20, max 100)
--   @ParamISearch NVARCHAR(100)  - Búsqueda general (opcional)
--   @ParamISortBy NVARCHAR(50)   - Columna de ordenamiento
--   @ParamISortOrder NVARCHAR(4) - ASC o DESC (default DESC)
-- Returns:
--   ResultSet 1: Lista paginada con TotalCount via COUNT(*) OVER()
-- ===========================================================================
-- CHANGE HISTORY:
-- Version  Date        Author          Description
-- -------  ----------  --------------  --------------------------------------
-- 1.0      YYYY-MM-DD  {Author}        Creación inicial
============================================================================== */

CREATE OR ALTER PROCEDURE [{Schema}].[List{Entity}]
    @ParamIPage         INT = 1,
    @ParamIPageSize     INT = 20,
    @ParamISearch       NVARCHAR(100) = NULL,
    @ParamISortBy       NVARCHAR(50) = 'RecordCreationDate',
    @ParamISortOrder    NVARCHAR(4) = 'DESC'
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        -------------------------------------------------------------------
        -- PASO 1: Normalizar parámetros de paginación
        -------------------------------------------------------------------
        IF @ParamIPageSize > 100 SET @ParamIPageSize = 100;
        IF @ParamIPageSize < 1 SET @ParamIPageSize = 20;
        IF @ParamIPage < 1 SET @ParamIPage = 1;

        -------------------------------------------------------------------
        -- PASO 2: Validar columna de ordenamiento (whitelist)
        -------------------------------------------------------------------
        DECLARE @VAllowedColumns NVARCHAR(MAX) = '{Col1},{Col2},RecordCreationDate';
        IF @ParamISortBy IS NULL
            OR @ParamISortBy NOT IN (SELECT [value] FROM STRING_SPLIT(@VAllowedColumns, ','))
            SET @ParamISortBy = 'RecordCreationDate';
        IF @ParamISortOrder NOT IN ('ASC', 'DESC')
            SET @ParamISortOrder = 'DESC';

        -------------------------------------------------------------------
        -- PASO 3: Preparar patrón de búsqueda LIKE
        -------------------------------------------------------------------
        DECLARE @VSearchPattern NVARCHAR(102) = NULL;
        IF @ParamISearch IS NOT NULL AND LTRIM(RTRIM(@ParamISearch)) <> ''
            SET @VSearchPattern = '%' + LTRIM(RTRIM(@ParamISearch)) + '%';

        -------------------------------------------------------------------
        -- PASO 4: Resultado paginado con COUNT(*) OVER()
        -------------------------------------------------------------------
        SELECT
            t.[{Entity}Id],
            t.[Name],
            -- Full name pattern (when joining Personnel.Employee):
            -- CONCAT_WS(' ', e.[FirstName], e.[MiddleName], e.[ThirdName],
            --     e.[LastName], e.[SecondLastName]) AS [EmployeeName],
            -- Nested object pattern (when joining MasterTable):
            -- s.[MasterTableId] AS [Status.MasterTableId],
            -- s.[Name]          AS [Status.Name],
            -- s.[Value]         AS [Status.Value],
            t.[RecordCreationDate],
            COUNT(*) OVER() AS [TotalCount]
        FROM [{Schema}].[{Entity}] t WITH(NOLOCK)
        -- INNER JOIN [Cnfg].[MasterTable] s WITH(NOLOCK)
        --     ON t.[StatusId] = s.[MasterTableId]
        WHERE t.[RecordStatus] = 'A'
          AND (@VSearchPattern IS NULL OR t.[Name] LIKE @VSearchPattern)
        ORDER BY
            CASE WHEN @ParamISortOrder = 'ASC' THEN
                CASE @ParamISortBy
                    WHEN '{Col1}' THEN CONVERT(NVARCHAR(50), t.[{Col1}], 126)
                    WHEN 'RecordCreationDate' THEN CONVERT(NVARCHAR(50), t.[RecordCreationDate], 126)
                END
            END ASC,
            CASE WHEN @ParamISortOrder = 'DESC' THEN
                CASE @ParamISortBy
                    WHEN '{Col1}' THEN CONVERT(NVARCHAR(50), t.[{Col1}], 126)
                    WHEN 'RecordCreationDate' THEN CONVERT(NVARCHAR(50), t.[RecordCreationDate], 126)
                END
            END DESC
        OFFSET (@ParamIPage - 1) * @ParamIPageSize ROWS
        FETCH NEXT @ParamIPageSize ROWS ONLY;

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
    @level1type = N'PROCEDURE', @level1name = N'List{Entity}';
GO
