using ANTA.Shared.Common.Api.Extensions;
using ANTA.Shared.Common.Api.HealthChecks;
using ANTA.Shared.Common.Data;
using ANTA.Shared.Common.Inspection;
using ANTA.Shared.Common.Logging;
using ANTA.Shared.Common.Mapping.Extensions;
using ANTA.Shared.Common.Validation;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Serilog;

const string projectName = "{ProjectName}";
const string applicationName = "Api{Module}";

var builder = WebApplication.CreateBuilder(args);
var configuration = builder.Configuration;

// 1. Bootstrap logger
SerilogExtensions.CreateBootstrapLogger(configuration);

// 2. Serilog + CloudWatch
builder.Host.UseAntaminaSerilog(
    applicationName: applicationName,
    logGroupName: "/aws/" + projectName);

// 3. Database connection
builder.Services.AddAntaminaData(
    configuration.GetConnectionString("DefaultConnection")!,
    stores => { stores.UseLogHttp(); });

// 4. HeaderToken (from API Gateway)
builder.Services.AddHeaderToken();

// 5. Exception handling
var isSaveLogDb = configuration.GetValue<bool>("ExceptionOptions:IsSaveLogDb");
builder.Services.AddAntaminaExceptionHandler(opt =>
{
    opt.ApplicationName = applicationName;
    opt.SaveToDatabase = isSaveLogDb;
});

// 6. Swagger with Happy auth
builder.Services.AddSwaggerWithHappyAuth(
    title: "API {Module}",
    version: "v1",
    description: "API for {description}");

// 7. Health Checks
builder.Services.AddHealthChecks()
    .AddSqlServerHealthCheck();

// 8. Validation
builder.Services.AddAntaminaValidation(typeof(Program).Assembly);

// 9. Mapping
builder.Services.AddAntaminaMapping(typeof(Program).Assembly);
builder.Services.ValidateMappingRegistrations(typeof(Program).Assembly);

// 10. Modules
builder.Services.Add{Module}Module();

try
{
    Log.Information("Starting {ApplicationName}...", applicationName);

    var app = builder.Build();

    app.UseSwagger();
    app.UseSwaggerUI();

    app.UseCorrelationId();
    app.UseJsonValidation();
    app.UseAntaminaExceptionHandler();

    app.Map{Module}Endpoints();
    app.MapHealthChecks("/health", new HealthCheckOptions
    {
        ResponseWriter = HealthCheckResponseWriter.WriteResponse
    });

    await app.RunAsync();
}
catch (Exception ex)
{
    Log.Fatal(ex, "Fatal error during startup");
}
finally
{
    SerilogExtensions.CloseLogger();
}
