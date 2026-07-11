# Pagination Handler Pattern

## Request Implementation

```csharp
public class List{Entity}Request : IPagedRequest
{
    [FromQuery(Name = "page")]
    public int Page { get; set; }

    [FromQuery(Name = "pageSize")]
    public int PageSize { get; set; }

    [FromQuery(Name = "search")]
    public string? Search { get; set; }

    [FromQuery(Name = "sortBy")]
    public string? SortBy { get; set; }

    [FromQuery(Name = "sortOrder")]
    public string? SortOrder { get; set; }

    [FromQuery(Name = "statusId")]
    public int? StatusId { get; set; }
}
```

## Handler: Multiple ResultSets

```csharp
public async Task<(List{Entity}Response Data, PaginationResult Pagination)> HandleAsync(
    List{Entity}Request request, CancellationToken ct)
{
    var command = new CommandDefinition(
        StoredProcedures.List{Entity},
        new
        {
            ParamIPage = request.Page,
            ParamIPageSize = request.PageSize,
            ParamISearch = request.Search,
            ParamISortBy = request.SortBy ?? "{Entity}Id",
            ParamISortOrder = request.SortOrder ?? "DESC"
        },
        commandType: CommandType.StoredProcedure,
        cancellationToken: ct
    );

    using var multi = await _db.QueryMultipleAsync(command);

    // ResultSet 1: Data (or error)
    var result = await multi.ReadAsync<dynamic>();
    var list = result.ToList();
    
    SpResultHelper.ThrowIfError(list.FirstOrDefault());

    var items = list
        .Select(r => _mapper.Map<{Entity}Item>((IDictionary<string, object>)r))
        .ToList();

    // ResultSet 2: Pagination
    var pagination = await multi.ReadFirstOrDefaultAsync<PaginationResult>()
        ?? new PaginationResult(request.Page, request.PageSize, 0);

    return (new List{Entity}Response { Items = items }, pagination);
}
```

## Endpoint: Return with Pagination

```csharp
private static async Task<IResult> Handle(
    [FromServices] List{Entity}Handler handler,
    [AsParameters] List{Entity}Request request,
    CancellationToken ct)
{
    var (data, pagination) = await handler.HandleAsync(request, ct);

    return Results.Ok(
        ApiResponse<List{Entity}Response>.Ok(
            data,
            pagination,
            "{Entity} list retrieved"
        )
    );
}
```

## Endpoint Registration

```csharp
app.MapGet("/", Handle)
    .WithPaginationDefaults()              // maxPageSize = 50
    .Produces<ApiResponse<List{Entity}Response>>(200);

// For bulk endpoints:
app.MapGet("/bulk", Handle)
    .WithPaginationDefaults(maxPageSize: 1000);
```
