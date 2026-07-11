using ANTA.Shared.Common.Extensions;
using ANTA.Shared.Common.Api.Extensions;
using ANTA.Shared.Common.Data;
using ANTA.Shared.Common.Inspection;
using ANTA.Shared.Common.Logging;
using ANTA.Shared.Common.Validation;
using ANTA.Shared.Common.Api.HealthChecks;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Serilog;
using YourProject.Api.Modules.YourModule;

const string projectName = "YourProject";
const string applicationName = "ApiYourModule";

var builder = WebApplication.CreateBuilder(args);
var configuration = builder.Configuration;

SerilogExtensions.CreateBootstrapLogger(configuration);

builder.Host.UseAntaminaSerilog(
    applicationName: applicationName,
    logGroupName: "/aws/" + projectName);

builder.Services.AddAntaminaData(
    configuration.GetConnectionString("DEV_STANDAR")!,
    stores => { stores.UseLogHttp(); });

builder.Services.AddHeaderToken();

builder.Services.AddYourModule();

var isSaveLogDb = configuration.GetValue<bool>("ExceptionOptions:IsSaveLogDb");
builder.Services.AddAntaminaExceptionHandler(opt =>
{
    opt.ApplicationName = applicationName;
    opt.SaveToDatabase = isSaveLogDb;
});

builder.Services.AddSwaggerWithHappyAuth(
    title: "API YourModule - YourProject",
    version: "v1",
    description: "API description here");

builder.Services.AddHealthChecks();

try
{
    Log.Information("Starting {ApplicationName}...", applicationName);

    var app = builder.Build();

    app.UseSwagger();
    app.UseSwaggerUI(options =>
    {
        options.SwaggerEndpoint("/swagger/v1/swagger.json", "API YourModule v1");
    });

    app.UseCorrelationId();
    app.UseJsonValidation();
    app.UseAntaminaExceptionHandler();

    app.MapYourModuleEndpoints();
    app.MapHealthChecks("/health", new HealthCheckOptions
    {
        ResponseWriter = HealthCheckResponseWriter.WriteResponse
    });

    await app.RunAsync();

    Log.Information("Stopping {ApplicationName}...", applicationName);
}
catch (Exception ex)
{
    Log.Fatal(ex, "Fatal error during startup of {ApplicationName}", applicationName);
}
finally
{
    SerilogExtensions.CloseLogger();
}
