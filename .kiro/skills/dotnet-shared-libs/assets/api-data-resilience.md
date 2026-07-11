# API Reference: ANTA.Shared.Common.Data (Data Resilience)
Source: `Artifacts/shared-common-data/src/ANTA.Shared.Common.Data`

## Table of Contents
- [AddAntaminaData()](#addantaminadata)
- [DataStoreOptions](#datastoreoptions)
- [DataResilienceOptions](#dataresilienceoptions)
- [DataOptions](#dataoptions)
- [IResilientDbExecutor](#iresilientdbexecutor)
- [IDbConnectionFactory](#idbconnectionfactory)
- [SpResultHelper](#spresulthelper)
- [Stores](#stores)
- [Store Selection by API Type](#store-selection-by-api-type)
- [Health Checks](#health-checks)
- [Constants](#constants)

## AddAntaminaData()
Current source has 7 public overloads (includes 2 legacy convenience overloads).

```csharp
public static IServiceCollection AddAntaminaData(this IServiceCollection services, string connectionString, Action<DataStoreOptions> configure)
public static IServiceCollection AddAntaminaData(this IServiceCollection services, string connectionString, Action<DataStoreOptions> configure, Action<DataResilienceOptions>? configureResilience)
public static IServiceCollection AddAntaminaData(this IServiceCollection services, string connectionString, string connectionName, Action<DataStoreOptions> configure)
public static IServiceCollection AddAntaminaData(this IServiceCollection services, string connectionString, string connectionName, Action<DataStoreOptions> configure, Action<DataResilienceOptions>? configureResilience)
public static IServiceCollection AddAntaminaData(this IServiceCollection services, IDbConnectionFactory connectionFactory, Action<DataStoreOptions> configure, Action<DataResilienceOptions>? configureResilience = null)
public static IServiceCollection AddAntaminaData(this IServiceCollection services, IDbConnectionFactory connectionFactory)
public static IServiceCollection AddAntaminaData(this IServiceCollection services, string connectionString)
```

## DataStoreOptions

```csharp
public sealed class DataStoreOptions : IValidatableOptions
{
    public DataStoreOptions UseLogHttp();
    public DataStoreOptions UseAuditHttp();
    public DataStoreOptions UseAuditEndpoint();
    public DataStoreOptions UseLogJob();
    public DataStoreOptions UseAll();
    public void Validate();
}
```

Store intent:
- `UseLogHttp()` -> `ILogHttpStore`
- `UseAuditHttp()` -> `IAuditHttpStore`
- `UseAuditEndpoint()` -> `IAuditEndpointStore`
- `UseLogJob()` -> `ILogJobStore`
- `UseAll()` -> all stores

## DataResilienceOptions

```csharp
public sealed class DataResilienceOptions : IValidatableOptions
{
    public bool Enabled { get; set; } = true;
    public int RetryCount { get; set; } = 3;
    public int RetryBaseDelaySeconds { get; set; } = 1;
    public bool EnableCircuitBreaker { get; set; } = true;
    public int CircuitBreakerFailureThreshold { get; set; } = 5;
    public int CircuitBreakerDurationSeconds { get; set; } = 30;
    public void Validate();
}
```

## DataOptions

```csharp
public sealed class DataOptions : IValidatableOptions
{
    public string ConnectionString { get; set; } = string.Empty;
    public string ConnectionName { get; set; } = "SqlServer";
    public void Validate();
}
```

## IResilientDbExecutor

```csharp
public interface IResilientDbExecutor
{
    Task ExecuteAsync(Func<IDbConnection, Task> operation, CancellationToken cancellationToken = default);
    Task<T> ExecuteAsync<T>(Func<IDbConnection, Task<T>> operation, CancellationToken cancellationToken = default);
    Task ExecuteAsync(Func<IDbConnection, Task> operation, Func<Exception, Task> fallback, CancellationToken cancellationToken = default);
    Task<T> ExecuteAsync<T>(Func<IDbConnection, Task<T>> operation, Func<Exception, Task<T>> fallback, CancellationToken cancellationToken = default);
}
```

## IDbConnectionFactory

```csharp
public interface IDbConnectionFactory
{
    IDbConnection CreateConnection();
}
```

Package implementation:

```csharp
public sealed class SqlConnectionFactory : IDbConnectionFactory
{
    public SqlConnectionFactory(DataOptions options);
    public IDbConnection CreateConnection();
}
```

## SpResultHelper

```csharp
public static class SpResultHelper
{
    public static bool HasError(object? row);
    public static void ThrowIfError(object? row);
    public static void ValidateFirstRow<T>(IEnumerable<T> result) where T : class;
}
```

Behavior notes:
- `HasError` checks `IDictionary<string, object>` and `"ErrorCode"` key.
- `ThrowIfError` no-ops when error shape is absent.
- `ValidateFirstRow<T>` validates first row and delegates to `ThrowIfError`.

Error code mapping table:

| Error pattern | Exception type |
|---|---|
| `VAL_*` | `ValidationException` |
| `AUTH_*` | `ForbiddenException` |
| `SYS_*` | `BusinessException` |
| `*_001` | `NotFoundException` |
| `*_002` | `ConflictException` |
| default (`*_003+` and others) | `BusinessRuleException` |

## Stores

```csharp
public sealed class AuditEndpointStore(IResilientDbExecutor executor) : IAuditEndpointStore
{ public Task<int> SaveAsync(AuditEndpoint audit, CancellationToken cancellationToken = default); }

public sealed class AuditHttpStore(IResilientDbExecutor executor) : IAuditHttpStore
{ public Task SaveAsync(AuditHttp audit, CancellationToken cancellationToken = default); }

public sealed class LogHttpStore(IResilientDbExecutor executor) : ILogHttpStore
{ public Task<int> SaveAsync(LogHttp log, CancellationToken cancellationToken = default); }

public sealed class LogJobStore(IResilientDbExecutor executor) : ILogJobStore
{ public Task<int> SaveAsync(LogJob logJob, CancellationToken cancellationToken = default); }
```

Store/SP linkage:
- `AuditEndpointStore` -> `StoredProcedures.CreateAuditEndpoint`
- `AuditHttpStore` -> `StoredProcedures.CreateAuditHttp`
- `LogHttpStore` -> `StoredProcedures.CreateLogHttp`
- `LogJobStore` -> `StoredProcedures.CreateLogJob`

## Store Selection by API Type

| API Type | Recommended registration |
|---|---|
| Internal API | `stores.UseLogHttp().UseAuditHttp()` |
| Gateway | `stores.UseLogHttp().UseAuditHttp().UseAuditEndpoint()` |
| Worker | `stores.UseLogHttp().UseLogJob()` |

## Health Checks

```csharp
public static IHealthChecksBuilder AddSqlServerHealthCheck(this IHealthChecksBuilder builder, string name = "sql-server", HealthStatus? failureStatus = null, IEnumerable<string>? tags = null, TimeSpan? timeout = null)
```

```csharp
public sealed class SqlServerHealthCheck(DataOptions options, ILogger<SqlServerHealthCheck> logger) : IHealthCheck
{ public Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext context, CancellationToken cancellationToken = default); }
```

Response data keys from `CheckHealthAsync`:
- Healthy: `connectionName`, `server`, `database`
- Unhealthy SQL: `connectionName`, `error`, `sqlError`

Handled SQL error codes:
- `18456` (`SqlConstants.AuthenticationFailedErrorCode`)
- `4060` (`SqlConstants.DatabaseNotFoundErrorCode`)
- `-2` (`SqlConstants.TimeoutErrorCode`)
- `53` (`SqlConstants.ServerNotFoundErrorCode`)

Connectivity probe:
- `SqlConstants.HealthCheckQuery` = `"SELECT 1"`

## Constants

### StoredProcedures

```csharp
public static class StoredProcedures
{
    public const string CreateAuditHttp = $"{DbSchemas.Log}.CreateAuditHttp";
    public const string CreateLogHttp = $"{DbSchemas.Log}.CreateLogHttp";
    public const string CreateAuditEndpoint = $"{DbSchemas.Log}.CreateAuditEndpoint";
    public const string CreateLogJob = $"{DbSchemas.Log}.CreateLogJob";
}
```

### DbSchemas

```csharp
public static class DbSchemas
{
    public const string Log = "Log";
}
```

### SqlConstants

```csharp
public static class SqlConstants
{
    public const string HealthCheckQuery = "SELECT 1";
    public const int AuthenticationFailedErrorCode = 18456;
    public const int DatabaseNotFoundErrorCode = 4060;
    public const int TimeoutErrorCode = -2;
    public const int ServerNotFoundErrorCode = 53;
}
```
