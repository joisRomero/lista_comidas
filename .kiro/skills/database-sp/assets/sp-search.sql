/* ==============================================================================
-- Object:      {Schema}.Search{Entity}
-- Author:      Development Team
-- Created:     YYYY-MM-DD
-- Version:     1.0
-- Description: Advanced search for {entities} with multiple criteria
-- ServiceId:   {ServiceId}
-- Rules:       {Business rules}
-- Parameters:
--   @ParamICode (VARCHAR, optional): Exact code match
--   @ParamIName (VARCHAR, optional): Partial name match
--   @ParamIStatusId (INT, optional): Status filter
--   @ParamIAmountFrom (DECIMAL, optional): Minimum amount
--   @ParamIAmountTo (DECIMAL, optional): Maximum amount
--   @ParamIDateFrom (DATE, optional): Start date
--   @ParamIDateTo (DATE, optional): End date
--   @ParamIMaxRecords (INT): Max results (default 1000)
-- Returns:
--   ResultSet 1: Matching records (no pagination)
-- Security:
--   {Security notes}
-- ===========================================================================
-- CHANGE HISTORY:
-- Version  Date        Author              Description
-- -------  ----------  ------------------  ------------------------------------
-- 1.0      YYYY-MM-DD  Development Team    Initial creation
============================================================================== */

CREATE OR ALTER PROCEDURE [{Schema}].[Search{Entity}]
    @ParamICode       VARCHAR(20) = NULL,
    @ParamIName       VARCHAR(100) = NULL,
    @ParamIStatusId   INT = NULL,
    @ParamIAmountFrom DECIMAL(18,2) = NULL,
    @ParamIAmountTo   DECIMAL(18,2) = NULL,
    @ParamIDateFrom   DATE = NULL,
    @ParamIDateTo     DATE = NULL,
    @ParamIMaxRecords INT = 1000
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        ---------------------------------------------------------------
        -- PASO 1: Validaciones
        ---------------------------------------------------------------
        IF @ParamIDateFrom IS NOT NULL AND @ParamIDateTo IS NOT NULL 
           AND @ParamIDateFrom > @ParamIDateTo
        BEGIN
            SELECT 'VAL_005' AS ErrorCode,
                   'dateFrom' AS Field,
                   'La fecha inicial no puede ser mayor a la fecha final' AS Message;
            RETURN;
        END

        IF @ParamIAmountFrom IS NOT NULL AND @ParamIAmountTo IS NOT NULL 
           AND @ParamIAmountFrom > @ParamIAmountTo
        BEGIN
            SELECT 'VAL_005' AS ErrorCode,
                   'amountFrom' AS Field,
                   'El monto inicial no puede ser mayor al monto final' AS Message;
            RETURN;
        END

        -- Normalize max records
        IF @ParamIMaxRecords IS NULL OR @ParamIMaxRecords < 1 OR @ParamIMaxRecords > 10000
            SET @ParamIMaxRecords = 1000;

        ---------------------------------------------------------------
        -- PASO 2: Busqueda
        ---------------------------------------------------------------
        SELECT TOP (@ParamIMaxRecords)
            T.{Entity}Id AS Id,
            T.Code,
            T.Name,
            T.Amount,
            T.StatusId,
            S.Value AS StatusName,
            T.RecordCreationDate
        FROM [{Schema}].[{Entity}] T WITH(NOLOCK)
        LEFT JOIN Cnfg.MasterTable S WITH(NOLOCK) 
            ON T.StatusId = S.MasterTableId
            AND S.RecordStatus = 'A'
        WHERE T.RecordStatus = 'A'
            AND (@ParamICode IS NULL OR T.Code = @ParamICode)
            AND (@ParamIName IS NULL OR T.Name LIKE '%' + @ParamIName + '%')
            AND (@ParamIStatusId IS NULL OR T.StatusId = @ParamIStatusId)
            AND (@ParamIAmountFrom IS NULL OR T.Amount >= @ParamIAmountFrom)
            AND (@ParamIAmountTo IS NULL OR T.Amount <= @ParamIAmountTo)
            AND (@ParamIDateFrom IS NULL OR T.RecordCreationDate >= @ParamIDateFrom)
            AND (@ParamIDateTo IS NULL OR T.RecordCreationDate <= @ParamIDateTo)
        ORDER BY T.RecordCreationDate DESC;

    END TRY
    BEGIN CATCH
        EXEC Log.GetErrorInfo;
    END CATCH
END
GO

-- Extended Property
EXEC sys.sp_addextendedproperty
    @name = N'MS_Description',
    @value = N'{Description}',
    @level0type = N'SCHEMA', @level0name = N'{Schema}',
    @level1type = N'PROCEDURE', @level1name = N'Search{Entity}';
GO
