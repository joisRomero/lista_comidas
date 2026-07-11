# Backend Structure

## Repository Structure

### Shared Libraries (NuGet - CodeArtifact)

```
repo: AntaShared/
├── shared-common/              → ANTA.Shared.Common
├── shared-common-api/          → ANTA.Shared.Common.Api
├── shared-common-inspection/   → ANTA.Shared.Common.Inspection
├── shared-common-data/         → ANTA.Shared.Common.Data
├── shared-common-logging/      → ANTA.Shared.Common.Logging
├── shared-happy/               → ANTA.Shared.Happy
├── shared-storage/             → ANTA.Shared.Storage
└── database/                   → SQL Scripts (Log schema)
```

### API Repositories

```
repo: ApiGateway/               → API Gateway with Ocelot (port 10000)
repo: ApiInterna{Module}/       → Domain API (port 34XX)

All with same internal structure:
└── src/{ProjectName}.Api/
    └── {ProjectName}.Api.csproj
```

**Important:** All repos use same project structure for standardized deploy:
```bash
dotnet publish src/{ProjectName}.Api -o output
```

---

## API Structure

### Multi-Module API

```
repo: api-{name}/
├── src/
│   └── {ProjectName}.Api/
│       ├── Modules/
│       │   ├── {Module1}/
│       │   │   ├── {Module1}Module.cs
│       │   │   ├── {Module1}StoredProcedures.cs
│       │   │   ├── Common/
│       │   │   │   └── DictionaryMappingHelper.cs
│       │   │   └── Features/
│       │   │       └── {Entity}/
│       │   │           ├── List{Entity}/
│       │   │           ├── Get{Entity}/
│       │   │           ├── Create{Entity}/
│       │   │           ├── Update{Entity}/
│       │   │           └── Delete{Entity}/
│       │   └── {Module2}/
│       ├── Program.cs
│       └── appsettings.json
├── database/
│   ├── {Schema1}/
│   │   ├── 00_Schema.sql
│   │   ├── 01_Tables.sql
│   │   ├── StoredProcedures/
│   │   └── Migrations/
│   └── {Schema2}/
└── README.md
```

### Single-Module API

```
repo: api-{name}/
├── src/
│   └── {ProjectName}.Api/
│       ├── Modules/
│       │   └── {Module}/
│       │       ├── {Module}Module.cs
│       │       ├── {Module}StoredProcedures.cs
│       │       └── Features/
│       │           ├── {Entity}/          # Main entity CRUD
│       │           ├── {SubEntity1}/      # Sub-entities
│       │           └── {SubEntity2}/
│       └── Program.cs
├── database/
│   └── {Schema}/
└── README.md
```

---

## Feature Structure (Vertical Slice)

Each feature is self-contained:

```
Features/{Action}{Entity}/
├── {Action}{Entity}Request.cs        # Input DTO
├── {Action}{Entity}Response.cs       # Output DTO
├── {Action}{Entity}Handler.cs        # Business logic (calls SP)
├── {Action}{Entity}Endpoint.cs       # Minimal API endpoint
├── {Action}{Entity}Validator.cs      # FluentValidation (optional)
└── {Action}{Entity}MappingProfile.cs # AutoMapper (for List/Get)
```

---

## Module Pattern

### {Module}Module.cs

```csharp
public static class {Module}Module
{
    public static IServiceCollection Add{Module}Module(this IServiceCollection services)
    {
        // AutoMapper
        services.AddAutoMapper(typeof({Module}Module).Assembly);

        // FluentValidation
        services.AddValidation();
        services.AddValidatorsFromAssembly(typeof({Module}Module).Assembly);

        // Handlers
        services.AddScoped<List{Entity}Handler>();
        services.AddScoped<Get{Entity}Handler>();
        services.AddScoped<Create{Entity}Handler>();
        services.AddScoped<Update{Entity}Handler>();
        services.AddScoped<Delete{Entity}Handler>();

        // Shared services (optional)
        services.AddScoped<{Entity}QueryService>();

        return services;
    }

    public static void Map{Module}Endpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/v1/{resource}")
            .WithTags("{Module}");

        List{Entity}Endpoint.Map(group);
        Get{Entity}Endpoint.Map(group);
        Create{Entity}Endpoint.Map(group);
        Update{Entity}Endpoint.Map(group);
        Delete{Entity}Endpoint.Map(group);
    }
}
```

### {Module}StoredProcedures.cs

```csharp
public static class {Module}StoredProcedures
{
    private const string Schema = "{Schema}";
    
    public const string List{Entity} = $"{Schema}.List{Entity}";
    public const string Get{Entity} = $"{Schema}.Get{Entity}";
    public const string Create{Entity} = $"{Schema}.Create{Entity}";
    public const string Update{Entity} = $"{Schema}.Update{Entity}";
    public const string Delete{Entity} = $"{Schema}.Delete{Entity}";
    
    // Sub-entities use Add/Delete instead of Create/Delete
    public const string Add{SubEntity} = $"{Schema}.Add{SubEntity}";
    public const string Delete{SubEntity} = $"{Schema}.Delete{SubEntity}";
}
```

---

## Program.cs Template

```csharp
using ANTA.Shared.Common.Api.Extensions;
using ANTA.Shared.Common.Data;
using ANTA.Shared.Common.Inspection;
using ANTA.Shared.Common.Logging;
using ANTA.Shared.Common.Api.HealthChecks;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using {ProjectNamespace}.Api.Modules.{Module};
using Serilog;

const string projectName = "{ProjectName}";
const string applicationName = "Api{Module}";

var builder = WebApplication.CreateBuilder(args);
var configuration = builder.Configuration;

// Bootstrap logger
SerilogExtensions.CreateBootstrapLogger(configuration);

// Serilog + CloudWatch
builder.Host.UseAntaminaSerilog(
    applicationName: applicationName,
    logGroupName: "/aws/" + projectName);

// Database connection
builder.Services.AddAntaminaData(
    configuration.GetConnectionString("DefaultConnection")!,
    stores => { stores.UseLogHttp(); });

// HeaderToken (from API Gateway)
builder.Services.AddHeaderToken();

// Modules
builder.Services.Add{Module}Module();

// Exception handling
var isSaveLogDb = configuration.GetValue<bool>("ExceptionOptions:IsSaveLogDb");
builder.Services.AddAntaminaExceptionHandler(opt =>
{
    opt.ApplicationName = applicationName;
    opt.SaveToDatabase = isSaveLogDb;
});

// Swagger with Happy auth
builder.Services.AddSwaggerWithHappyAuth(
    title: "API {Module}",
    version: "v1",
    description: "API for {description}");

// Health Checks
builder.Services.AddHealthChecks();

try
{
    Log.Information("Starting {ApplicationName}...", applicationName);

    var app = builder.Build();

    app.UseSwagger();
    app.UseSwaggerUI();

    app.UseCorrelationId();
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
```

---

## Package References

```xml
<ItemGroup>
    <PackageReference Include="AutoMapper" Version="13.0.1" />
    <PackageReference Include="Dapper" Version="2.1.35" />
    <PackageReference Include="Microsoft.Data.SqlClient" Version="5.2.2" />
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.5.0" />
    <PackageReference Include="System.Text.Json" Version="8.0.5" />
</ItemGroup>

<!-- ANTA Shared Libraries -->
<ItemGroup>
    <PackageReference Include="ANTA.Shared.Common" Version="1.0.*" />
    <PackageReference Include="ANTA.Shared.Common.Api" Version="1.0.*" />
    <PackageReference Include="ANTA.Shared.Common.Logging" Version="1.0.*" />
    <PackageReference Include="ANTA.Shared.Common.Inspection" Version="1.0.*" />
    <PackageReference Include="ANTA.Shared.Common.Data" Version="1.0.*" />
</ItemGroup>
```

---

## Shared Services

For reusable queries across features:

```csharp
// Shared/{Entity}QueryService.cs
public class {Entity}QueryService
{
    private readonly IDbConnection _db;
    private readonly IMapper _mapper;

    public async Task<{Entity}DetailDto> Get{Entity}DetailAsync(int {entity}Id, CancellationToken ct)
    {
        // Reusable query logic
    }
}
```
