# API HTTP Clients Reference (shared-happy + shared-universal)
Reference extracted from source code under `Artifacts/shared-happy/src/` and `Artifacts/shared-universal/src/`.

## Table of Contents
- [Happy Service Client](#happy-service-client)
- [Universal API Gateway Client](#universal-api-gateway-client)
- [Resilience Patterns (shared)](#resilience-patterns-shared)

## Happy Service Client
### AddAntaminaHappy() - full signature
```csharp
public static IHttpClientBuilder AddAntaminaHappy(
    this IServiceCollection services,
    Action<ServiceHappyOptions> configure,
    Action<TrackingHeaderOptions>? configureTracking = null)
```
Registers `IApiServiceHappy` -> `ApiServiceHappy`, `IAuthentication` -> `Authentication` (Transient), and `HappyServiceHealthCheck` with named client `HappyHealthCheck`.

### ServiceHappyOptions - all properties
```csharp
public sealed class ServiceHappyOptions : IValidatableOptions
{
    public string Uri { get; set; } = string.Empty;
    public string Authentication_GetDeserializeObject { get; set; } = string.Empty;
    public string Authentication_GetHeaderValidate { get; set; } = string.Empty;
    public string UserAgent { get; set; } =
        $"ANTA.Shared.Happy/{typeof(ServiceHappyOptions).Assembly.GetName().Version}";
    public ResilienceOptions Resilience { get; set; } = new();
    public void Validate();
}
```

### TrackingHeaderOptions - all properties
```csharp
public sealed class TrackingHeaderOptions : IValidatableOptions
{
    public string PathHeaderName { get; set; } = "X-Request-Path";
    public string MethodHeaderName { get; set; } = "X-Request-Method";
    public bool Enabled { get; set; } = true;
    public Dictionary<string, string> CustomHeaders { get; set; } = new();
    public void Validate();
}
```

### IApiServiceHappy - PostAnonymousAsync<T>() signature
```csharp
Task<ApiGenericResponse<TypeObject>> PostAnonymousAsync<TypeObject>(
    string url,
    object entity,
    IRequestContext? requestContext = null,
    CancellationToken ct = default);
```

### IAuthentication - GetDeserializeObject(), GetHeaderValidate()
```csharp
Task<ApiGenericResponse<Response<string>>> GetDeserializeObject(
    EncryptRequest entity,
    CancellationToken ct = default);

Task<ApiGenericResponse<bool>> GetHeaderValidate(
    HeaderValidateRequest entity,
    IRequestContext? requestContext = null,
    CancellationToken ct = default);
```

### Happy ResilienceOptions - all Polly config properties
```csharp
public sealed class ResilienceOptions : IValidatableOptions
{
    public int HttpClientTimeoutSeconds { get; set; } = 100;
    public int RequestTimeoutSeconds { get; set; } = 30;
    public int RetryCount { get; set; } = 3;
    public int RetryBaseDelaySeconds { get; set; } = 2;
    public int CircuitBreakerFailuresBeforeBreaking { get; set; } = 5;
    public int CircuitBreakerDurationSeconds { get; set; } = 30;
    public bool EnableRetry { get; set; } = true;
    public bool EnableCircuitBreaker { get; set; } = true;
    public bool EnableTimeout { get; set; } = true;
    public void Validate();
}
```

### AddHappyServiceHealthCheck() - signature
```csharp
public static IHealthChecksBuilder AddHappyServiceHealthCheck(
    this IHealthChecksBuilder builder,
    string name = "happy-service",
    HealthStatus? failureStatus = null,
    IEnumerable<string>? tags = null,
    TimeSpan? timeout = null)
```

### Additional Happy public APIs (complete coverage)
```csharp
public interface IRequestContext { string Path { get; } string Method { get; } IDictionary<string, string> CustomHeaders { get; } }
public sealed class RequestContext : IRequestContext
{
    public string Path { get; set; } = string.Empty;
    public string Method { get; set; } = string.Empty;
    public IDictionary<string, string> CustomHeaders { get; set; } = new Dictionary<string, string>();
    public RequestContext();
    public RequestContext(string path, string method);
    public RequestContext(string path, string method, IDictionary<string, string> customHeaders);
}
public sealed class ApiGenericResponse<T> { public bool IsSuccess { get; set; } public T? Result { get; set; } public string Message { get; set; } = string.Empty; }
public sealed class EncryptRequest { public string TextTransform { get; set; } = string.Empty; public string Code { get; set; } = string.Empty; }
public sealed class HeaderValidateRequest { public string Code { get; set; } = string.Empty; public string Header { get; set; } = string.Empty; }
public sealed class Response<T> { public bool Status { get; set; } = true; public int State { get; set; } = 200; public string Message { get; set; } = "Ok"; public T? Value { set; get; } public ResultResponse? ResultResponse { set; get; } }
public sealed class ResultResponse { public int Id { get; set; } public int IdResult { get; set; } public int CodeResult { get; set; } public string MessageResult { get; set; } = string.Empty; }
public static IRequestContext ToRequestContext(this HttpContext httpContext);
public static IRequestContext ToRequestContext(this HttpContext httpContext, params string[] includeHeaders);
public static IRequestContext ToRequestContext(this HttpContext httpContext, IDictionary<string, string> customHeaders);
public const string ContentTypeJson = "application/json";
public const string TimeoutError = "Timeout";
public const string HttpClientName = "HappyHealthCheck";
```

## Universal API Gateway Client
### AddAntaminaUniversal() - full signature
```csharp
public static IHttpClientBuilder AddAntaminaUniversal(
    this IServiceCollection services,
    Action<ServiceUniversalOptions> configure)
```
Registers `IApiServiceUniversal` -> `ApiServiceUniversal` and `UniversalServiceHealthCheck` with named client `UniversalHealthCheck`.

### ServiceUniversalOptions - all properties
```csharp
public sealed class ServiceUniversalOptions : IValidatableOptions
{
    public string Uri { get; set; } = string.Empty;
    public string UserAgent { get; set; } =
        $"ANTA.Shared.Universal/{typeof(ServiceUniversalOptions).Assembly.GetName().Version}";
    public ResilienceOptions Resilience { get; set; } = new();
    public void Validate();
}
```

### IApiServiceUniversal - GetAsync<T>(), PostAsync<T>()
```csharp
Task<ApiGenericResponse<T>> GetAsync<T>(string url, CancellationToken ct = default) where T : class;
Task<ApiGenericResponse<T>> PostAsync<T>(string url, object entity, CancellationToken ct = default) where T : class;
```

### Universal ResilienceOptions - all Polly config
```csharp
public sealed class ResilienceOptions : IValidatableOptions
{
    public int HttpClientTimeoutSeconds { get; set; } = 100;
    public int RequestTimeoutSeconds { get; set; } = 30;
    public int RetryCount { get; set; } = 3;
    public int RetryBaseDelaySeconds { get; set; } = 2;
    public int CircuitBreakerFailuresBeforeBreaking { get; set; } = 5;
    public int CircuitBreakerDurationSeconds { get; set; } = 30;
    public bool EnableRetry { get; set; } = true;
    public bool EnableCircuitBreaker { get; set; } = true;
    public bool EnableTimeout { get; set; } = true;
    public void Validate();
}
```

### AddUniversalServiceHealthCheck() - signature
```csharp
public static IHealthChecksBuilder AddUniversalServiceHealthCheck(
    this IHealthChecksBuilder builder,
    string name = "universal-service",
    HealthStatus? failureStatus = null,
    IEnumerable<string>? tags = null,
    TimeSpan? timeout = null)
```

### Additional Universal public APIs (complete coverage)
```csharp
public sealed class ApiGenericResponse<T> { public bool IsSuccess { get; set; } public T? Result { get; set; } public string Message { get; set; } = string.Empty; }
public sealed class UniversalResponse<T> { public bool Status { get; set; } = true; public int State { get; set; } = 200; public string Message { get; set; } = "Ok"; public T? Value { get; set; } public ResultResponse? ResultResponse { get; set; } }
public sealed class ResultResponse { public string Id { get; set; } = string.Empty; public string CodeResult { get; set; } = string.Empty; public string MessageResult { get; set; } = string.Empty; }
public const string ContentTypeJson = "application/json";
public const string TimeoutError = "Timeout";
public const string HttpClientName = "UniversalHealthCheck";
```

## Resilience Patterns (shared)
Both clients implement `Retry`, `Circuit Breaker`, and `Timeout` in DI and validate through `ResilienceOptions.Validate()`.

| Pattern | Toggle | Config Properties | Default | Implementation note |
|---|---|---|---|---|
| Retry | `EnableRetry` | `RetryCount`, `RetryBaseDelaySeconds` | `3`, `2` | Handles transient HTTP errors + `429`; honors `Retry-After` when present, else exponential backoff `base^attempt` |
| Circuit Breaker | `EnableCircuitBreaker` | `CircuitBreakerFailuresBeforeBreaking`, `CircuitBreakerDurationSeconds` | `5`, `30s` | Opens after configured failures and resets after break window |
| Timeout (policy) | `EnableTimeout` | `RequestTimeoutSeconds` | `30s` | Polly timeout per request |
| Timeout (HttpClient) | n/a | `HttpClientTimeoutSeconds` | `100s` | Sets `HttpClient.Timeout` |

Health checks use named clients with fixed timeout `10s` and `HEAD` probe to base URI.
