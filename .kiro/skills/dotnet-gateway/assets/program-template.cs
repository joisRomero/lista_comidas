using ANTA.Shared.Common.Data;
using ANTA.Shared.Common.Inspection;
using ANTA.Shared.Common.Logging;
using ANTA.Shared.Happy.Configuration;
using ANTA.Shared.Happy.Extensions;
using ANTA.Shared.Happy.HealthChecks;
using ANTA.Shared.Common.Api.HealthChecks;
using YourProject.ApiGateway.Services;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Microsoft.AspNetCore.Localization;
using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;
using Ocelot.DependencyInjection;
using Ocelot.Middleware;
using Serilog;
using System.Globalization;

const string projectName = "YourProject";
const string applicationName = "ApiGateway";

var builder = WebApplication.CreateBuilder(args);
var configuration = builder.Configuration;
var environment = builder.Environment;

configuration.AddJsonFile($"appsettings.{environment.EnvironmentName}.json", optional: false, reloadOnChange: true);
configuration.AddJsonFile($"configuration.{environment.EnvironmentName}.json", optional: false, reloadOnChange: true);

SerilogExtensions.CreateBootstrapLogger(configuration);

builder.Host.UseAntaminaSerilog(
    applicationName: applicationName,
    logGroupName: "/aws/" + projectName);

builder.Services.AddHttpContextAccessor();

builder.Services.AddMvc()
    .AddNewtonsoftJson(options =>
    {
        options.SerializerSettings.ReferenceLoopHandling = ReferenceLoopHandling.Ignore;
        options.SerializerSettings.ContractResolver = new DefaultContractResolver();
    });

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddOcelot(configuration)
    .AddDelegatingHandler<CorrelationIdDelegatingHandler>(true)
    .AddDelegatingHandler<MissingBodyDelegatingHandler>(true);
builder.Services.AddSwaggerForOcelot(configuration);

builder.Services.AddCors(o => o.AddPolicy("All", builder =>
{
    builder.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader();
}));

builder.Services.AddAntaminaData(
    configuration.GetConnectionString("DEV_STANDAR")!,
    stores => {
        stores.UseLogHttp();
        stores.UseAuditHttp();
        stores.UseAuditEndpoint();
    });

var isSaveLogDb = configuration.GetValue<bool>("ExceptionOptions:IsSaveLogDb");
var isSaveAuditHappy = configuration.GetValue<bool>("ExceptionOptions:IsSaveAuditHappy");

builder.Services.AddAntaminaHappy(
    options =>
    {
        var section = configuration.GetSection(nameof(ServiceHappyOptions));
        section.Bind(options);
        if (string.IsNullOrEmpty(options.Uri))
            throw new InvalidOperationException("ServiceHappyOptions not configured");
    },
    tracking =>
    {
        tracking.PathHeaderName = "trexa";
        tracking.MethodHeaderName = "trexb";
        tracking.Enabled = true;
    })
.AddAntaminaAuditEndpoint(opt => opt.SaveToDatabase = isSaveAuditHappy);

builder.Services.AddHealthChecks()
    .AddHappyServiceHealthCheck(tags: ["external"]);

builder.Services.AddAntaminaExceptionHandler(opt =>
{
    opt.ApplicationName = applicationName;
    opt.SaveToDatabase = isSaveLogDb;
});
builder.Services.AddAntaminaAuditHttp(opt => opt.SaveToDatabase = isSaveLogDb);

try
{
    Log.Information("Starting {AppName}...", applicationName);

    var app = builder.Build();

    var supportedCultures = new[] { new CultureInfo("es-PE") };
    app.UseRequestLocalization(new RequestLocalizationOptions
    {
        DefaultRequestCulture = new RequestCulture("es-PE"),
        SupportedCultures = supportedCultures,
        FallBackToParentCultures = false
    });
    CultureInfo.DefaultThreadCurrentCulture = CultureInfo.CreateSpecificCulture("es-PE");

    app.UseCorrelationId();
    app.UseAntaminaAuditHttp();
    app.UseAntaminaExceptionHandler();

    app.UsePathBase("/apigateway");

    app.UseSwagger();
    app.UseSwaggerForOcelotUI(opt =>
    {
        opt.PathToSwaggerGenerator = "/swagger/docs";
    }, uiOpt =>
    {
        uiOpt.RoutePrefix = "swagger";
    });

    app.UseCors("All");
    app.UseStaticFiles();
    app.UseRouting();
    app.UseAuthorization();

    app.MapControllers();
    app.MapHealthChecks("/health", new HealthCheckOptions
    {
        ResponseWriter = HealthCheckResponseWriter.WriteResponse
    });

    app.UseValidationHeader();
    await app.UseOcelot();

    await app.RunAsync();

    Log.Information("Stopping {AppName}...", applicationName);
}
catch (Exception ex)
{
    Log.Fatal(ex, "Fatal error during startup of {AppName}", applicationName);
}
finally
{
    SerilogExtensions.CloseLogger();
}
