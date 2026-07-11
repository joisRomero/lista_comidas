# API Middleware Audit
Public API reference for `ANTA.Shared.Common.Inspection` and `ANTA.Shared.Common.Logging`.

## Table of Contents
- [Exception Handler](#exception-handler)
- [Audit HTTP](#audit-http)
- [Audit Endpoint](#audit-endpoint)
- [Background Queue](#background-queue)
- [Serilog](#serilog)
- [CorrelationId](#correlationid)
- [LogStreamProvider](#logstreamprovider)
- [Store Interfaces](#store-interfaces)

## Exception Handler
```csharp
public static IServiceCollection AddAntaminaExceptionHandler(this IServiceCollection services, Action<ExceptionHandlerOptions> configure)
public static IApplicationBuilder UseAntaminaExceptionHandler(this IApplicationBuilder app)
public sealed class ExceptionHandlerOptions : IValidatableOptions
{
    public string ApplicationName { get; set; } = "Unknown";
    public bool SaveToDatabase { get; set; } = true;
    public long MaxRequestBodySizeToBuffer { get; set; } = 65536;
    public void Validate();
}
```
- `Validate()` requires non-empty `ApplicationName`.
- `MaxRequestBodySizeToBuffer` controls request buffering before reading body on exception.
- If `SaveToDatabase` is true, middleware attempts `ILogHttpStore.SaveAsync(LogHttp, ct)`.

## Audit HTTP
```csharp
public static IServiceCollection AddAntaminaAuditHttp(this IServiceCollection services, Action<AuditHttpOptions> configure)
public static IApplicationBuilder UseAntaminaAuditHttp(this IApplicationBuilder app)
public sealed class AuditHttpOptions : IValidatableOptions
{
    public bool SaveToDatabase { get; set; } = true;
    public string[] ExcludedPaths { get; set; } = ["swagger", "index", "favicon", "health"];
    public void Validate();
}
```
- `Validate()` enforces `ExcludedPaths != null`.
- Request path is excluded if it `Contains` any configured entry (case-insensitive).

`AuditHttp` model:
```csharp
public sealed class AuditHttp
{
    public int HttpStatusCode { get; set; }
    public string? UrlScheme { get; set; }
    public string? HostPort { get; set; }
    public string? Path { get; set; }
    public string? Method { get; set; }
    public string? RequestHeader { get; set; }
    public string? RequestBody { get; set; }
    public string? ResponseHeader { get; set; }
    public string? ResponseBody { get; set; }
    public string? CorrelationId { get; set; }
    public string? IpAddress { get; set; }
    public TimeSpan? Duration { get; set; }
    public DateTime? CreateDate { get; set; }
}
```

## Audit Endpoint
```csharp
public static IHttpClientBuilder AddAntaminaAuditEndpoint(this IHttpClientBuilder builder, Action<AuditEndpointOptions> configure)
public sealed class AuditEndpointOptions : IValidatableOptions
{
    public bool SaveToDatabase { get; set; } = true;
    public void Validate();
}
```
`AddAntaminaAuditEndpoint()` behavior:
- validates options;
- `TryAddSingleton<IHttpContextAccessor, HttpContextAccessor>();`
- `TryAddSingleton<IAuditQueue, AuditQueue>();`
- when `SaveToDatabase`, `TryAddEnumerable(ServiceDescriptor.Singleton<IHostedService, AuditBackgroundService>());`
- `AddTransient<AuditEndpointHandler>();` and `AddHttpMessageHandler<AuditEndpointHandler>();`

`AuditEndpoint` model (with CallerInfo fields):
```csharp
public sealed class AuditEndpoint
{
    public int HttpStatusCode { get; init; }
    public int? Retry { get; init; }
    public string? UrlScheme { get; init; }
    public string? HostPort { get; init; }
    public string? Path { get; init; }
    public string? Method { get; init; }
    public TimeSpan? Duration { get; init; }
    public DateOnly? CreateDateOnly { get; init; }
    public DateTime? CreateDate { get; init; }
    public string? ResponseBody { get; init; }
    public string? RequestHeader { get; init; }
    public string? RequestBody { get; init; }
    public string? ResponseHeader { get; init; }
    public string? CallerPath { get; init; }
    public string? CallerMethod { get; init; }
    public string? CallerIp { get; init; }
    public string? CallerUser { get; init; }
    public string? CorrelationId { get; init; }
}
```

## Background Queue
```csharp
public interface IAuditQueue
{
    int Count { get; }
    long DroppedCount { get; }
    bool Enqueue(AuditEndpoint audit);
    ValueTask<AuditEndpoint> DequeueAsync(CancellationToken cancellationToken);
    bool TryDequeue(out AuditEndpoint? audit);
}
```
- `AuditQueue` uses `Channel<AuditEndpoint>` capacity `1000`.
- Options: `FullMode=Wait`, `SingleReader=true`, `SingleWriter=false`.
- `Enqueue()` calls `TryWrite`; on full queue, increments `DroppedCount` and drops new item.
- Code comment references DropOldest intent; effective implementation is manual drop-on-full.
- `AuditBackgroundService : BackgroundService, IAuditBackgroundService` dequeues and persists via `IAuditEndpointStore`, logs via `ILogJobStore`, and drains queue on shutdown (30s timeout).

Fire-and-forget flow:
```text
Request -> AuditEndpointHandler.SendAsync -> Build AuditEndpoint (+ CallerPath/Method/Ip/User, CorrelationId)
        -> IAuditQueue.Enqueue -> Immediate HTTP response
Background: AuditBackgroundService -> IAuditQueue.DequeueAsync -> IAuditEndpointStore.SaveAsync -> ILogJobStore.SaveAsync
```

## Serilog
```csharp
public static IHostBuilder UseAntaminaSerilog(this IHostBuilder builder, string applicationName, string? logGroupName = null, string? outputTemplate = null)
public static void CreateBootstrapLogger(IConfiguration configuration, string? outputTemplate = null)
public static void CloseLogger()
```
- Default `outputTemplate`: `{Timestamp:yyyy-MM-dd HH:mm:ss.fff zzz} [{Level:u3}] [{CorrelationId}] {Message:lj} {Properties}{NewLine}{Exception}`
- Default `logGroupName`: `/aws/AntaminaNet8`
- Always console sink
- `Local`: auto file sink `./Logs/{applicationName}-.txt` (daily rolling)
- Non-`Local`: CloudWatch sink with `BatchSizeLimit=100`, `QueueSizeLimit=10000`, `Period=10s`, `CreateLogGroup=true`, `RetryAttempts=5`, `LogStreamNameProvider=new LogStreamProvider(applicationName)`
- `CreateBootstrapLogger()` creates startup logger; `CloseLogger()` invokes `Log.CloseAndFlush()`

## CorrelationId
```csharp
public sealed class CorrelationIdMiddleware(RequestDelegate next)
public static IApplicationBuilder UseCorrelationId(this IApplicationBuilder builder)
public static string? GetCorrelationId(HttpContext? context)
```
- Header key: `X-Correlation-Id`
- Middleware reads incoming header or generates new value, stores in `HttpContext.Items["CorrelationId"]`, pushes Serilog `LogContext` property, and appends response header
- Generation code:
```csharp
return $"{DateTime.UtcNow:yyyyMMddHHmmss}-{Guid.NewGuid():N}"[..32];
```
- Format starts as `yyyyMMddHHmmss-guid`; final value is truncated to 32 chars

## LogStreamProvider
CloudWatch stream format:
```text
{ApplicationName}_{yyyy-MM-dd}
```
Implementation uses UTC date and per-day cache.

## Store Interfaces
```csharp
public interface IAuditEndpointStore { Task<int> SaveAsync(AuditEndpoint audit, CancellationToken cancellationToken = default); }
public interface IAuditHttpStore { Task SaveAsync(AuditHttp audit, CancellationToken cancellationToken = default); }
public interface ILogHttpStore { Task<int> SaveAsync(LogHttp log, CancellationToken cancellationToken = default); }
public interface ILogJobStore { Task<int> SaveAsync(LogJob logJob, CancellationToken cancellationToken = default); }
```
