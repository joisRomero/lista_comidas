using YourProject.Api.Modules.YourModule.Features.Items.ListItems;
using YourProject.Api.Modules.YourModule.Features.Items.GetItem;
using YourProject.Api.Modules.YourModule.Features.Items.CreateItem;
using ANTA.Shared.Common.Validation;

namespace YourProject.Api.Modules.YourModule;

public static class YourModuleModule
{
    public static IServiceCollection AddYourModule(this IServiceCollection services)
    {
        services.AddAutoMapper(typeof(YourModuleModule).Assembly);

        services.AddValidation();
        services.AddValidatorsFromAssembly(typeof(YourModuleModule).Assembly);

        services.AddScoped<ListItemsHandler>();
        services.AddScoped<GetItemHandler>();
        services.AddScoped<CreateItemHandler>();

        return services;
    }

    public static void MapYourModuleEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/v1/items")
            .WithTags("Items");

        ListItemsEndpoint.Map(group);
        GetItemEndpoint.Map(group);
        CreateItemEndpoint.Map(group);
    }
}
