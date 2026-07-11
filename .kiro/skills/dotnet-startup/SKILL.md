---
name: dotnet-startup
description: >
  Program.cs and module registration patterns for ANTA .NET APIs.
  Trigger: When creating new API projects, adding modules, or configuring middleware.
metadata:
  author: anta
  version: "2.0"
  scope: [root]
  auto_invoke: "Program.cs, AddAntaminaData, AddHeaderToken, Module, middleware"
  phase: [construction]
  layer: [backend]
  validates_with: validate_dotnet_project
  validation_profile: build-unit
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Use ANTA.Shared.Common extensions | ALWAYS | Standardized infrastructure |
| Register modules with `Add{Module}Module()` | ALWAYS | Consistent DI pattern |
| Map endpoints with `Map{Module}Endpoints()` | ALWAYS | Minimal API pattern |
| Middleware order: CorrelationId → JsonValidation → ExceptionHandler | ALWAYS | Correct pipeline |
| Swagger middleware BEFORE CorrelationId chain | ALWAYS | Swagger not wrapped by exception handler |
| Generate `Properties/launchSettings.json` | ALWAYS | Required for local development (port, environment) |
| Generate `appsettings.Local.json` | ALWAYS | Required for local DB connection string |
| Generate `nuget.config` | ALWAYS | Required for ANTA.Shared.* NuGet from CodeArtifact |

---

## Program.cs Constants (MANDATORY)

Every internal API starts with two constants:

```csharp
const string projectName = "{ProjectName}";           // Project name (shared across all APIs)
const string applicationName = "Api{Module}"; // Unique per API (e.g., "ApiUserData", "ApiBookings")
```

---

## Service Registration Order

```csharp
// 1. Logging (bootstrap)
SerilogExtensions.CreateBootstrapLogger(configuration);
builder.Host.UseAntaminaSerilog(
    applicationName: applicationName,
    logGroupName: "/aws/" + projectName);

// 2. Database (Internal API: ONLY UseLogHttp — AuditHttp is Gateway-only)
builder.Services.AddAntaminaData(
    configuration.GetConnectionString("DEV_STANDAR")!,
    stores =>
    {
        stores.UseLogHttp();
    });

// 3. Authentication context
builder.Services.AddHeaderToken();

// 4. Validation (FluentValidation DI)
builder.Services.AddAntaminaValidation();

// 5. Mapping (explicit mappers — no reflection)
builder.Services.AddAntaminaMapping(typeof(Program).Assembly);

// 6. Modules (Handlers + Validators)
builder.Services.Add{Module}Module();

// 6. Exception Handling
var isSaveLogDb = configuration.GetValue<bool>("ExceptionOptions:IsSaveLogDb");
builder.Services.AddAntaminaExceptionHandler(opt =>
{
    opt.ApplicationName = applicationName;
    opt.SaveToDatabase = isSaveLogDb;
});

// 7. Swagger with Happy auth
builder.Services.AddSwaggerWithHappyAuth(
    title: "API {Description} - {ProjectName}",
    version: "v1",
    description: "API para {description}");

// 8. Health Checks
builder.Services.AddHealthChecks();
```

---

## Middleware Order (CRITICAL)

```csharp
var app = builder.Build();

// Swagger (BEFORE the CorrelationId/Exception middleware chain)
app.UseSwagger();
app.UseSwaggerUI(options =>
{
    options.SwaggerEndpoint("/swagger/v1/swagger.json", "API {Description} v1");
});

app.UseCorrelationId();            // 1. Correlation ID para rastreo distribuido
app.UseJsonValidation();           // 2. Valida sintaxis JSON (devuelve VAL_006)
app.UseAntaminaExceptionHandler(); // 3. Captura excepciones, guarda en LogHttp

// Map endpoints
app.Map{Module}Endpoints();

app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = HealthCheckResponseWriter.WriteResponse
});

await app.RunAsync();
```

| Order | Middleware | Purpose |
|-------|------------|---------|
| — | `UseSwagger()` + `UseSwaggerUI()` | API docs (outside exception chain) |
| 1 | `UseCorrelationId()` | Distributed tracing |
| 2 | `UseJsonValidation()` | JSON syntax validation (VAL_006) |
| 3 | `UseAntaminaExceptionHandler()` | Catches exceptions, logs to DB |

> Swagger goes BEFORE the CorrelationId/Exception middleware chain.

---

## Module Registration Pattern

```csharp
public static class {Module}Module
{
    public static IServiceCollection Add{Module}Module(this IServiceCollection services)
    {
        // Register handlers
        services.AddScoped<Get{Entity}Handler>();
        services.AddScoped<Update{Entity}Handler>();

        // Register validators (scans assembly for all validators)
        services.AddValidatorsFromAssemblyContaining<Update{Entity}Validator>();

        return services;
    }

    public static void Map{Module}Endpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/v1/{path}")
            .WithTags("{Tag}");

        Get{Entity}Endpoint.Map(group);
        Update{Entity}Endpoint.Map(group);
    }
}
```

> Register AutoMapper in a module only when the feature set includes MappingProfiles. Manual mapping remains valid for simpler handlers.

---

## AddAntaminaData Stores

### Internal API (e.g., ApiUserData, ApiBookings)

```csharp
builder.Services.AddAntaminaData(
    configuration.GetConnectionString("DEV_STANDAR")!,
    stores =>
    {
        stores.UseLogHttp();  // Exception logging to DB — ONLY this for internal APIs
    });
```

### Gateway ONLY

```csharp
builder.Services.AddAntaminaData(
    configuration.GetConnectionString("DEV_STANDAR")!,
    stores =>
    {
        stores.UseLogHttp();       // Exception logging
        stores.UseAuditHttp();     // Request/response audit
        stores.UseAuditEndpoint(); // Outgoing HTTP calls audit
    });
```

| Store | Purpose | Used In |
|-------|---------|---------|
| `UseLogHttp()` | Exception logging to DB | All APIs + Gateway |
| `UseAuditHttp()` | Request/response audit | Gateway ONLY |
| `UseAuditEndpoint()` | Outgoing HTTP calls audit | Gateway ONLY |
| `UseLogJob()` | Background job logging | Worker services |

> AuditHttp se maneja SOLO en el Gateway para evitar duplicación.

---

## ANTA.Shared Extensions

| Extension | Package | Purpose |
|-----------|---------|---------|
| `AddAntaminaData()` | Common.Data | DB + stores |
| `AddHeaderToken()` | Common.Api | Parse HeaderToken from Gateway |
| `AddAntaminaExceptionHandler()` | Common.Inspection | Exception handling + logging |
| `AddSwaggerWithHappyAuth()` | Common.Api | Swagger + Happy auth |
| `UseAntaminaSerilog()` | Common.Logging | Serilog + CloudWatch |
| `AddValidation()` | Common.Validation | FluentValidation DI registration |
| `UseJsonValidation()` | Common.Validation | JSON syntax middleware (VAL_006) |

> **NuGet version:** Current ANTA.Shared packages are at `1.0.0-beta.41` across all libraries.

---

## Adding a New Module

1. Create folder structure:
   ```
   Modules/{Module}/
   ├── {Module}Module.cs
   ├── {Module}StoredProcedures.cs
   └── Features/{Entity}/{Action}{Entity}/
   ```

2. Register in Program.cs:
   ```csharp
   builder.Services.AddNewModule();
   app.MapNewModuleEndpoints();
   ```

---

## Checklist

- [ ] Constants `projectName` ("{ProjectName}") and `applicationName` ("Api{Module}") defined
- [ ] Bootstrap logger before anything else
- [ ] `AddAntaminaData` with `DEV_STANDAR` connection string and `UseLogHttp()` only (internal API)
- [ ] `AddHeaderToken` for gateway integration
- [ ] `AddValidation()` for FluentValidation DI
- [ ] Module registered with `Add{Module}Module()`
- [ ] Exception handler configured with `ApplicationName` and `SaveToDatabase`
- [ ] Swagger with `AddSwaggerWithHappyAuth()` (title, version, description)
- [ ] Swagger middleware BEFORE CorrelationId chain
- [ ] Middleware in correct order: CorrelationId → JsonValidation → ExceptionHandler
- [ ] Health checks configured with `HealthCheckResponseWriter`
- [ ] `await app.RunAsync()` (not `app.Run()`)
- [ ] try/catch/finally with `SerilogExtensions.CloseLogger()`

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Complete Program.cs template | [program-template.cs](assets/program-template.cs) |
| Module template | [module-template.cs](assets/module-template.cs) |

## Related Skills

- **API Structure**: `dotnet-api`
- **Handler Patterns**: `dotnet-handler`
- **Shared Libraries**: `dotnet-shared-libs`
