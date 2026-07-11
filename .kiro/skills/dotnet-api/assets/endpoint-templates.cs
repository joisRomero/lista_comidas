public static class ListItemsEndpoint
{
    public static void Map(IEndpointRouteBuilder app)
    {
        app.MapGet("/", Handle)
            .WithPaginationDefaults()
            .Produces<ApiResponse<ListItemsResponse>>(StatusCodes.Status200OK)
            .ProducesProblem(StatusCodes.Status400BadRequest);
    }

    private static async Task<IResult> Handle(
        [FromServices] ListItemsHandler handler,
        [FromServices] HeaderToken headerToken,
        [AsParameters] ListItemsRequest request,
        CancellationToken ct = default)
    {
        var currentUser = headerToken?.EmployeeId
            ?? throw new UnauthorizedAccessException("Usuario no autenticado");
        var (data, pagination) = await handler.HandleAsync(currentUser, request, ct);
        return Results.Ok(ApiResponse<ListItemsResponse>.Ok(data, pagination, "Items retrieved"));
    }
}

public static class GetItemEndpoint
{
    public static void Map(IEndpointRouteBuilder app)
    {
        app.MapGet("/{itemId:int}", Handle)
            .Produces<ApiResponse<GetItemResponse>>(StatusCodes.Status200OK)
            .ProducesProblem(StatusCodes.Status404NotFound);
    }

    private static async Task<IResult> Handle(
        int itemId,
        [FromServices] GetItemHandler handler,
        CancellationToken ct = default)
    {
        var result = await handler.HandleAsync(itemId, ct);
        return Results.Ok(ApiResponse<GetItemResponse>.Ok(result, "Item retrieved"));
    }
}

public static class CreateItemEndpoint
{
    public static void Map(IEndpointRouteBuilder app)
    {
        app.MapPost("/", Handle)
            .WithValidation<CreateItemRequest>()
            .Produces<ApiResponse<CreateItemResponse>>(StatusCodes.Status201Created)
            .ProducesProblem(StatusCodes.Status400BadRequest);
    }

    private static async Task<IResult> Handle(
        CreateItemRequest request,
        [FromServices] CreateItemHandler handler,
        [FromServices] HeaderToken headerToken,
        CancellationToken ct)
    {
        var currentUser = headerToken?.EmployeeId
            ?? throw new UnauthorizedAccessException("Usuario no autenticado");
        var result = await handler.HandleAsync(request, currentUser, ct);
        return Results.Created(
            $"/api/v1/items/{result.Item!.ItemId}",
            ApiResponse<CreateItemResponse>.Ok(result, "Item created")
        );
    }
}
