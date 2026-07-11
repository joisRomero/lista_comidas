# API-First Backend Generation Templates

## 1. List SP Template

```sql
CREATE PROCEDURE {Schema}.List{Entity}
    @ParamIPage INT = 1,
    @ParamIPageSize INT = 10,
    @ParamISearch NVARCHAR(200) = NULL,
    @ParamIStatusId INT = NULL,
    @ParamISortBy NVARCHAR(50) = '{DefaultSort}',
    @ParamISortOrder NVARCHAR(4) = 'DESC'
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @Offset INT = (@ParamIPage - 1) * @ParamIPageSize;

    -- Result Set 1: Data
    SELECT
        e.{Entity}Id,
        e.Code,
        e.Name,
        s.MasterTableId AS StatusId,
        s.Name AS StatusName,
        s.Value AS StatusValue,
        s.AdditionalOne AS StatusBackgroundColor,
        s.AdditionalTwo AS StatusTextColor
    FROM {Schema}.{Entity} e
    INNER JOIN Cnfg.MasterTable s ON s.MasterTableId = e.StatusId
    WHERE e.RecordStatus = 1
        AND (@ParamISearch IS NULL OR e.Name LIKE '%' + @ParamISearch + '%')
        AND (@ParamIStatusId IS NULL OR e.StatusId = @ParamIStatusId)
    ORDER BY
        CASE WHEN @ParamISortOrder = 'ASC' THEN
            CASE @ParamISortBy
                WHEN '{Entity}Id' THEN e.{Entity}Id
            END
        END ASC,
        CASE WHEN @ParamISortOrder = 'DESC' THEN
            CASE @ParamISortBy
                WHEN '{Entity}Id' THEN e.{Entity}Id
            END
        END DESC
    OFFSET @Offset ROWS FETCH NEXT @ParamIPageSize ROWS ONLY;

    -- Result Set 2: Pagination
    SELECT
        @ParamIPage AS Page,
        @ParamIPageSize AS PageSize,
        COUNT(*) AS TotalRecords
    FROM {Schema}.{Entity} e
    WHERE e.RecordStatus = 1
        AND (@ParamISearch IS NULL OR e.Name LIKE '%' + @ParamISearch + '%')
        AND (@ParamIStatusId IS NULL OR e.StatusId = @ParamIStatusId);
END
```

## 2. Get SP Template

```sql
CREATE PROCEDURE {Schema}.Get{Entity}
    @ParamI{Entity}Id INT
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (SELECT 1 FROM {Schema}.{Entity} WHERE {Entity}Id = @ParamI{Entity}Id AND RecordStatus = 1)
    BEGIN
        SELECT 'NOT_FOUND' AS ErrorCode, NULL AS Field, '{Entity} no encontrado' AS Message;
        RETURN;
    END

    -- Main entity
    SELECT
        e.{Entity}Id,
        e.Code,
        e.Name,
        s.MasterTableId AS StatusId,
        s.Name AS StatusName,
        s.Value AS StatusValue
    FROM {Schema}.{Entity} e
    INNER JOIN Cnfg.MasterTable s ON s.MasterTableId = e.StatusId
    WHERE e.{Entity}Id = @ParamI{Entity}Id AND e.RecordStatus = 1;
END
```

## 3. Create SP Template

```sql
CREATE PROCEDURE {Schema}.Create{Entity}
    @ParamIName NVARCHAR(200),
    @ParamI{FieldId} INT,
    @ParamICreationUser NVARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        -- Validations
        IF EXISTS (SELECT 1 FROM {Schema}.{Entity} WHERE Name = @ParamIName AND RecordStatus = 1)
        BEGIN
            SELECT 'VAL_001' AS ErrorCode, 'name' AS Field, 'El nombre ya existe' AS Message;
            RETURN;
        END

        DECLARE @{Entity}Id INT;
        DECLARE @InitialStatusId INT = (SELECT MasterTableId FROM Cnfg.MasterTable WHERE Name = 'DRAFT' AND GroupCode = '{ENTITY}_STATUSES');

        INSERT INTO {Schema}.{Entity} (Name, {FieldId}, StatusId, CreationUser, CreationDate, RecordStatus)
        VALUES (@ParamIName, @ParamI{FieldId}, @InitialStatusId, @ParamICreationUser, GETUTCDATE(), 1);

        SET @{Entity}Id = SCOPE_IDENTITY();

        -- Return created entity
        SELECT
            e.{Entity}Id,
            e.Code,
            e.Name,
            s.MasterTableId AS StatusId,
            s.Name AS StatusName,
            s.Value AS StatusValue
        FROM {Schema}.{Entity} e
        INNER JOIN Cnfg.MasterTable s ON s.MasterTableId = e.StatusId
        WHERE e.{Entity}Id = @{Entity}Id;

    END TRY
    BEGIN CATCH
        EXEC Log.GetErrorInfo;
    END CATCH
END
```

## 4. Operation SP Template (State Transition)

```sql
CREATE PROCEDURE {Schema}.{Verb}{Entity}
    @ParamI{Entity}Id INT,
    @ParamI{OptionalField} NVARCHAR(500) = NULL,
    @ParamIModificationUser NVARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        DECLARE @CurrentStatusName NVARCHAR(50);
        SELECT @CurrentStatusName = s.Name
        FROM {Schema}.{Entity} e
        INNER JOIN Cnfg.MasterTable s ON s.MasterTableId = e.StatusId
        WHERE e.{Entity}Id = @ParamI{Entity}Id AND e.RecordStatus = 1;

        -- Validate entity exists
        IF @CurrentStatusName IS NULL
        BEGIN
            SELECT 'NOT_FOUND' AS ErrorCode, NULL AS Field, '{Entity} no encontrado' AS Message;
            RETURN;
        END

        -- Validate state precondition
        IF @CurrentStatusName != '{REQUIRED_STATE}'
        BEGIN
            SELECT 'BUS_001' AS ErrorCode, NULL AS Field, '{Entity} no esta en estado valido para esta operacion' AS Message;
            RETURN;
        END

        -- Execute transition
        DECLARE @NewStatusId INT = (SELECT MasterTableId FROM Cnfg.MasterTable WHERE Name = '{NEW_STATE}' AND GroupCode = '{ENTITY}_STATUSES');

        UPDATE {Schema}.{Entity}
        SET StatusId = @NewStatusId,
            ModificationUser = @ParamIModificationUser,
            ModificationDate = GETUTCDATE()
        WHERE {Entity}Id = @ParamI{Entity}Id;

        -- Return result
        SELECT
            e.{Entity}Id,
            e.Code,
            s.MasterTableId AS StatusId,
            s.Name AS StatusName,
            s.Value AS StatusValue
        FROM {Schema}.{Entity} e
        INNER JOIN Cnfg.MasterTable s ON s.MasterTableId = e.StatusId
        WHERE e.{Entity}Id = @ParamI{Entity}Id;

    END TRY
    BEGIN CATCH
        EXEC Log.GetErrorInfo;
    END CATCH
END
```

## 5. List Handler Template

```csharp
public class List{Entity}Handler(IDbConnection db)
{
    public async Task<ApiResponse<List<List{Entity}Response>>> Handle(List{Entity}Request request)
    {
        using var multi = await db.QueryMultipleAsync(
            {Module}StoredProcedures.List{Entity},
            new
            {
                ParamIPage = request.Page,
                ParamIPageSize = request.PageSize,
                ParamISearch = request.Search,
                ParamISortBy = request.SortBy,
                ParamISortOrder = request.SortOrder
            },
            commandType: CommandType.StoredProcedure
        );

        var items = (await multi.ReadAsync<List{Entity}SpResult>()).ToList();
        SpResultHelper.ThrowIfError(items);

        var pagination = await multi.ReadFirstOrDefaultAsync<PaginationResult>();

        return ApiResponse<List<List{Entity}Response>>.Ok(
            items.Select(MapToResponse).ToList(),
            pagination
        );
    }
}
```

## 6. Get Handler Template

```csharp
public class Get{Entity}Handler(IDbConnection db)
{
    public async Task<Get{Entity}Response> Handle(int entityId)
    {
        var result = await db.QueryFirstOrDefaultAsync<Get{Entity}SpResult>(
            {Module}StoredProcedures.Get{Entity},
            new { ParamI{Entity}Id = entityId },
            commandType: CommandType.StoredProcedure
        );

        SpResultHelper.ThrowIfError(result);

        return new Get{Entity}Response { ... };
    }
}
```

## 7. Create Handler Template

```csharp
public class Create{Entity}Handler(IDbConnection db)
{
    public async Task<Create{Entity}Response> Handle(Create{Entity}Request request, string currentUser)
    {
        var result = await db.QueryFirstOrDefaultAsync<Create{Entity}SpResult>(
            {Module}StoredProcedures.Create{Entity},
            new
            {
                ParamIName = request.Name,
                ParamI{FieldId} = request.{FieldId},
                ParamICreationUser = currentUser
            },
            commandType: CommandType.StoredProcedure
        );

        SpResultHelper.ThrowIfError(result);

        return new Create{Entity}Response { ... };
    }
}
```

## 8. Operation Handler Template (State Transition)

```csharp
public class {Verb}{Entity}Handler(IDbConnection db)
{
    public async Task<{Verb}{Entity}Response> Handle({Verb}{Entity}Request request, string currentUser)
    {
        var result = await db.QueryFirstOrDefaultAsync<{Verb}{Entity}SpResult>(
            {Module}StoredProcedures.{Verb}{Entity},
            new
            {
                ParamI{Entity}Id = request.{Entity}Id,
                ParamI{OptionalField} = request.{OptionalField},
                ParamIModificationUser = currentUser
            },
            commandType: CommandType.StoredProcedure
        );

        SpResultHelper.ThrowIfError(result);

        return new {Verb}{Entity}Response
        {
            {Entity}Id = result.{Entity}Id,
            Status = new StatusItem
            {
                MasterTableId = result.StatusId,
                Name = result.StatusName,
                Value = result.StatusValue
            }
        };
    }
}
```

## 9. List Endpoint Template

```csharp
public static class List{Entity}Endpoint
{
    public static RouteHandlerBuilder Map(RouteGroupBuilder group)
    {
        return group.MapGet("/", Handle)
            .WithName("List{Entity}")
            .Produces<ApiResponse<List<List{Entity}Response>>>();
    }

    private static async Task<IResult> Handle(
        [AsParameters] List{Entity}Request request,
        [FromServices] List{Entity}Handler handler)
    {
        var result = await handler.Handle(request);
        return Results.Ok(result);
    }
}
```

## 10. Create Endpoint Template

```csharp
public static class Create{Entity}Endpoint
{
    public static RouteHandlerBuilder Map(RouteGroupBuilder group)
    {
        return group.MapPost("/", Handle)
            .WithValidation<Create{Entity}Request>()
            .WithName("Create{Entity}")
            .Produces<ApiResponse<Create{Entity}Response>>(StatusCodes.Status201Created);
    }

    private static async Task<IResult> Handle(
        [FromBody] Create{Entity}Request request,
        [FromServices] Create{Entity}Handler handler,
        [FromHeader(Name = "HeaderToken")] string currentUser)
    {
        var result = await handler.Handle(request, currentUser);
        return Results.Created($"/{resource}/{result.{Entity}Id}", ApiResponse<Create{Entity}Response>.Ok(result));
    }
}
```

## 11. Operation Endpoint Template

```csharp
public static class {Verb}{Entity}Endpoint
{
    public static RouteHandlerBuilder Map(RouteGroupBuilder group)
    {
        return group.MapPost("/{entityId}/{verb}", Handle)
            .WithValidation<{Verb}{Entity}Request>()
            .WithName("{Verb}{Entity}")
            .Produces<ApiResponse<{Verb}{Entity}Response>>();
    }

    private static async Task<IResult> Handle(
        [FromRoute] int entityId,
        [FromBody] {Verb}{Entity}Request request,
        [FromServices] {Verb}{Entity}Handler handler,
        [FromHeader(Name = "HeaderToken")] string currentUser)
    {
        request.{Entity}Id = entityId;
        var result = await handler.Handle(request, currentUser);
        return Results.Ok(ApiResponse<{Verb}{Entity}Response>.Ok(result));
    }
}
```
