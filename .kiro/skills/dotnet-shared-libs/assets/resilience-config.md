# Resilience Configuration

## Happy Client Resilience Options

```csharp
options.Resilience = new ResilienceOptions
{
    // Retry with exponential backoff
    EnableRetry = true,
    RetryCount = 3,
    RetryBaseDelaySeconds = 2,  // 2s, 4s, 8s

    // Circuit Breaker
    EnableCircuitBreaker = true,
    CircuitBreakerFailuresBeforeBreaking = 5,
    CircuitBreakerDurationSeconds = 30,

    // Timeout
    EnableTimeout = true,
    HttpClientTimeoutSeconds = 100,
    RequestTimeoutSeconds = 30
};
```

## Circuit Breaker States

```
CLOSED (normal operation)
    ↓ 5 consecutive failures
OPEN (rejects requests, 30s)
    ↓ timeout expires
HALF-OPEN (test mode)
    ↓ success → CLOSED
    ↓ failure → OPEN
```

## Graceful Degradation (Fallback)

For non-critical operations, use fallback to maintain service availability.

```csharp
// Without fallback - throws exception on failure
var items = await executor.ExecuteAsync(
    conn => conn.QueryAsync<Item>("SELECT * FROM Items"));

// With fallback - returns empty list on failure
var items = await executor.ExecuteAsync(
    conn => conn.QueryAsync<Item>("SELECT * FROM Items"),
    ex => Task.FromResult(Enumerable.Empty<Item>()));

// With fallback - returns cached value
var config = await executor.ExecuteAsync(
    conn => conn.QueryFirstAsync<Config>(sp),
    ex => Task.FromResult(_cachedConfig));
```

| Scenario | Recommended Fallback |
|----------|---------------------|
| Lists/Grids | Empty list `[]` |
| Configuration | Cached or default value |
| Counters | `0` or last known value |
| Searches | Empty results |

**DO NOT use fallback** for critical operations (payments, transactions).
