public class List{Feature}Handler
{
    private readonly IDbConnection _db;
    private readonly IMapper _mapper;

    public List{Feature}Handler(IDbConnection db, IMapper mapper)
    {
        _db = db;
        _mapper = mapper;
    }

    public async Task<(List{Feature}Response Data, PaginationResult Pagination)> HandleAsync(
        List{Feature}Request request, CancellationToken ct)
    {
        var command = new CommandDefinition(
            StoredProcedures.List{Feature},
            new
            {
                ParamIPage = request.Page,
                ParamIPageSize = request.PageSize,
                ParamISearch = request.Search,
                ParamISortBy = request.SortBy ?? "{Feature}Id",
                ParamISortOrder = request.SortOrder ?? "DESC"
            },
            commandType: CommandType.StoredProcedure,
            cancellationToken: ct
        );

        using var multi = await _db.QueryMultipleAsync(command);
        
        var itemsResult = await multi.ReadAsync<dynamic>();
        var itemsList = itemsResult.ToList();
        
        SpResultHelper.ThrowIfError(itemsList.FirstOrDefault());
        
        var items = itemsList
            .Select(r => _mapper.Map<List{Feature}Item>((IDictionary<string, object>)r))
            .ToList();
        
        var pagination = await multi.ReadFirstOrDefaultAsync<PaginationResult>() 
            ?? new PaginationResult(request.Page, request.PageSize, 0);
        
        return (new List{Feature}Response { Items = items }, pagination);
    }
}
