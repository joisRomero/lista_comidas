# Handler Templates

## List with Pagination

```csharp
using System.Data;
using ANTA.Shared.Common;
using ANTA.Shared.Common.Data.Helpers;
using AutoMapper;
using Dapper;

public class ListItemsHandler
{
    private readonly IDbConnection _db;
    private readonly IMapper _mapper;

    public ListItemsHandler(IDbConnection db, IMapper mapper)
    {
        _db = db;
        _mapper = mapper;
    }

    public async Task<(ListItemsResponse Response, PaginationResult Pagination)> HandleAsync(string currentUser, string? currentRole, ListItemsRequest request, CancellationToken ct = default)
    {
        var command = new CommandDefinition(
            ItemsStoredProcedures.ListItems,
            new
            {
                ParamIPage = request.Page,
                ParamIPageSize = request.PageSize,
                ParamISearch = request.Search,
                ParamISortBy = request.SortBy ?? "ItemId",
                ParamISortOrder = request.SortOrder ?? "DESC",
                ParamICurrentUser = currentUser,
                ParamICurrentRole = currentRole
            },
            commandType: CommandType.StoredProcedure,
            cancellationToken: ct
        );

        var result = (await _db.QueryAsync<dynamic>(command)).ToList();

        SpResultHelper.ThrowIfError(result.FirstOrDefault());

        var items = result
            .Select(r => _mapper.Map((IDictionary<string, object>)r))
            .ToList();

        var totalCount = result.Any()
            ? ((IDictionary<string, object>)result.First()).GetValue<int>("TotalCount")
            : 0;
        var pagination = PaginationResult.Create(request.Page, request.PageSize, totalCount);

        return (new ListItemsResponse { Items = items }, pagination);
    }
}
```

## List with Sub-collections

```csharp
public async Task<(ListItemsResponse Response, PaginationResult Pagination)> HandleAsync(string currentUser, string? currentRole, ListItemsRequest request, CancellationToken ct = default)
{
    var command = new CommandDefinition(
        ItemsStoredProcedures.ListItems,
        new
        {
            ParamIPage = request.Page,
            ParamIPageSize = request.PageSize,
            ParamISearch = request.Search,
            ParamISortBy = request.SortBy ?? "ItemId",
            ParamISortOrder = request.SortOrder ?? "DESC",
            ParamICurrentUser = currentUser,
            ParamICurrentRole = currentRole
        },
        commandType: CommandType.StoredProcedure,
        cancellationToken: ct
    );

    using var multi = await _db.QueryMultipleAsync(command);

    var itemsResult = (await multi.ReadAsync<dynamic>()).ToList();
    SpResultHelper.ThrowIfError(itemsResult.FirstOrDefault());

    var items = itemsResult
        .Select(r => _mapper.Map((IDictionary<string, object>)r))
        .ToList();

    var totalCount = itemsResult.Any()
        ? ((IDictionary<string, object>)itemsResult.First()).GetValue<int>("TotalCount")
        : 0;
    var pagination = PaginationResult.Create(request.Page, request.PageSize, totalCount);

    var relatedItems = (await multi.ReadAsync<dynamic>())
        .Select(r => _mapper.Map((IDictionary<string, object>)r))
        .ToList();

    return (new ListItemsResponse { Items = items, RelatedItems = relatedItems }, pagination);
}
```

## Get Detail with Sub-collections

```csharp
public async Task<GetItemResponse> HandleAsync(int itemId, string currentUser, CancellationToken ct = default)
{
    var command = new CommandDefinition(
        ItemsStoredProcedures.GetItem,
        new { ParamIItemId = itemId, ParamICurrentUser = currentUser },
        commandType: CommandType.StoredProcedure,
        cancellationToken: ct
    );

    using var multi = await _db.QueryMultipleAsync(command);

    var itemResult = await multi.ReadAsync<dynamic>();
    var itemRow = itemResult.FirstOrDefault();

    SpResultHelper.ThrowIfError(itemRow);

    var item = _mapper.Map<GetItemDetail>((IDictionary<string, object>)itemRow);

    var details = (await multi.ReadAsync<dynamic>())
        .Select(r => _mapper.Map<DetailItem>((IDictionary<string, object>)r))
        .ToList();

    item.Details = details;

    return new GetItemResponse { Item = item };
}
```

## Create with Related Entities

```csharp
public class CreateItemHandler
{
    private readonly IDbConnection _db;

    public CreateItemHandler(IDbConnection db)
    {
        _db = db;
    }

    public async Task<CreateItemResponse> HandleAsync(
        CreateItemRequest request, string currentUser, CancellationToken ct = default)
    {
        var item = await CreateItemAsync(request, currentUser, ct);
        await SaveDetailsAsync(item.ItemId, request.Details, currentUser, ct);
        return new CreateItemResponse { Item = item };
    }

    private async Task<CreateItemItem> CreateItemAsync(
        CreateItemRequest request, string currentUser, CancellationToken ct)
    {
        var command = new CommandDefinition(
            ItemsStoredProcedures.CreateItem,
            new
            {
                ParamIName = request.Name,
                ParamIDescription = request.Description,
                ParamITypeId = request.TypeId,
                ParamIRecordCreationUser = currentUser
            },
            commandType: CommandType.StoredProcedure,
            cancellationToken: ct
        );

        var result = await _db.QuerySingleAsync<dynamic>(command);
        SpResultHelper.ThrowIfError(result);
        var dict = (IDictionary<string, object>)result;

        return new CreateItemItem
        {
            ItemId = Convert.ToInt32(dict["ItemId"]),
            Code = DictionaryMappingHelper.GetString(dict, "Code"),
            Status = DictionaryMappingHelper.MapStatus(dict, "Status")
        };
    }

    private async Task SaveDetailsAsync(
        int itemId, IList<CreateDetailItem>? details, string currentUser, CancellationToken ct)
    {
        if (details == null || details.Count == 0) return;

        foreach (var detail in details)
        {
            var command = new CommandDefinition(
                ItemsStoredProcedures.AddDetail,
                new
                {
                    ParamIItemId = itemId,
                    ParamIDescription = detail.Description,
                    ParamIRecordCreationUser = currentUser
                },
                commandType: CommandType.StoredProcedure,
                cancellationToken: ct
            );
            var result = await _db.QuerySingleAsync<dynamic>(command);
            SpResultHelper.ThrowIfError(result);
        }
    }
}
```
