public class Get{Feature}Handler
{
    private readonly IDbConnection _db;
    private readonly IMapper _mapper;

    public Get{Feature}Handler(IDbConnection db, IMapper mapper)
    {
        _db = db;
        _mapper = mapper;
    }

    public async Task<Get{Feature}Response> HandleAsync(int {feature}Id, CancellationToken ct)
    {
        var command = new CommandDefinition(
            StoredProcedures.Get{Feature},
            new { ParamI{Feature}Id = {feature}Id },
            commandType: CommandType.StoredProcedure,
            cancellationToken: ct
        );

        using var multi = await _db.QueryMultipleAsync(command);
        
        var itemResult = await multi.ReadAsync<dynamic>();
        var itemRow = itemResult.FirstOrDefault();
        
        SpResultHelper.ThrowIfError(itemRow);
        
        var item = _mapper.Map<Get{Feature}Detail>((IDictionary<string, object>)itemRow);
        
        // If SP returns sub-collections in additional ResultSets:
        // var subItems = (await multi.ReadAsync<dynamic>())
        //     .Select(r => _mapper.Map<SubItemDetail>((IDictionary<string, object>)r))
        //     .ToList();
        // item.SubItems = subItems;
        
        return new Get{Feature}Response { Item = item };
    }
}
