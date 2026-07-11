# ANTA.Shared.Storage Public API Reference

Reference generated from `Artifacts/shared-storage/src/**/*.cs` source files.
Audience: AI agents implementing upload/download flows with `IS3StorageService`.

## Table of Contents
- [AddAntaminaStorage()](#addantaminastorage)
- [S3StorageOptions](#s3storageoptions)
- [IS3StorageService](#is3storageservice)
- [StorageRateLimitLevel](#storageratelimitlevel)
- [Rate Limiting Configuration](#rate-limiting-configuration)
- [Content Type Validation](#content-type-validation)
- [Health Check](#health-check)

## AddAntaminaStorage()

Defined in `Extensions/StorageExtensions.cs`.

### Overloads

```csharp
IServiceCollection AddAntaminaStorage(this IServiceCollection services, Action<S3StorageOptions> configure)

IServiceCollection AddAntaminaStorage(this IServiceCollection services, Action<S3StorageOptions> configure, bool useDefaultContentTypes)

IServiceCollection AddAntaminaStorage(this IServiceCollection services, Action<S3StorageOptions> configureStorage, StorageRateLimitLevel rateLimitLevel, bool useDefaultContentTypes = false)
```

### Behavior
- All overloads build `S3StorageOptions`, call `Validate()`, and register core services.
- Core registrations: `S3StorageOptions` (singleton), `IAmazonS3` (singleton), `IS3StorageService` -> `S3StorageService` (singleton), `S3StorageHealthCheck` (singleton).
- `useDefaultContentTypes` calls `S3StorageOptions.UseDefaultContentTypesIfEmpty()`, which is currently a no-op and marked `[Obsolete]`.
- Rate-limited overload also registers `StorageRateLimitOptions` and `AddRateLimiter(...)` policy when enabled.

## S3StorageOptions

Defined in `Configuration/S3StorageOptions.cs`.

### Properties
- `string BucketName` (required)
- `string Region = "us-east-1"` (required)
- `string ProjectName` (required)
- `int UploadUrlExpirationSeconds = 300`
- `int DownloadUrlExpirationSeconds = 300`
- `long MaxFileSizeKB = 10240`
- `int MaxBatchConcurrency = 10`
- `int MaxBatchSize = 100`
- `List<string> AllowedContentTypes = new()` (legacy compatibility only)

### Validation rules (`Validate()`)
- `BucketName`, `ProjectName`, `Region` cannot be null/whitespace.
- `UploadUrlExpirationSeconds`, `DownloadUrlExpirationSeconds`, `MaxFileSizeKB`, `MaxBatchConcurrency`, `MaxBatchSize` must be `> 0`.

## IS3StorageService

Defined in `Abstractions/IS3StorageService.cs`.

```csharp
PresignedUrlResponse GetUploadUrl(PresignedUrlRequest request)
IReadOnlyList<PresignedUrlResponse> GetUploadUrlBatch(IEnumerable<PresignedUrlRequest> requests)
PresignedUrlResponse GetDownloadUrl(string filePath, string? fileName = null)
Task<bool> DeleteAsync(string filePath, CancellationToken ct = default)
Task<bool> ExistsAsync(string filePath, CancellationToken ct = default)
Task<bool> MoveAsync(string sourceFilePath, string destinationFilePath, CancellationToken ct = default)
Task<bool> MoveBatchAsync(IEnumerable<(string SourcePath, string DestinationPath)> files, CancellationToken ct = default)
```

### Parameter/behavior notes from `Services/S3StorageService.cs`
- `GetUploadUrl` and `GetUploadUrlBatch` are synchronous URL generation (no network call); both validate each request.
- Upload key format: `{ProjectName}/{Prefix}/{Guid}-{SanitizedFileName}` (prefix omitted when null/empty).
- `GetDownloadUrl` optionally sets `Content-Disposition: attachment; filename="{sanitized}"` when `fileName` is provided.
- `DeleteAsync`/`MoveAsync` return `false` on `AmazonS3Exception` (no throw for those cases).
- `ExistsAsync` returns `false` when S3 returns `404 NotFound`.
- `MoveBatchAsync` throws `ArgumentOutOfRangeException` when `files.Count > MaxBatchSize`; concurrency capped by `MaxBatchConcurrency`.

## StorageRateLimitLevel

Defined in `Configuration/StorageRateLimitOptions.cs`.

- `Disabled = 0` -> no limiter (`Enabled == false`)
- `Low = 1` -> `50/min` per client IP
- `Standard = 2` -> `100/min` per client IP
- `High = 3` -> `200/min` per client IP
- `Critical = 4` -> `30/min` per client IP

All active levels use fixed window config: `WindowSeconds = 60`, `QueueLimit = 0`.

## Rate Limiting Configuration

Defined in `Configuration/StorageRateLimitOptions.cs` and applied in `Extensions/StorageExtensions.cs`.

### StorageRateLimitOptions members
- `StorageRateLimitLevel Level = Disabled`
- `string ClientIpHeader = "X-Forwarded-For"`
- `bool Enabled => Level != Disabled`
- `Validate()` requires non-empty `ClientIpHeader`.

### Runtime behavior
- Policy name is internal constant `AntaminaStorageRateLimit`.
- Rejection status code is `429`.
- Partition key is client IP resolved via `httpContext.GetClientIpAddress(rateLimitOptions.ClientIpHeader)`.
- Endpoints group (`MapStorageEndpoints`) applies `.RequireRateLimiting(...)` only when `StorageRateLimitOptions.Enabled` is true.

## Content Type Validation

Source: `Utilities/UploadRequestValidator.cs`, `Configuration/S3StorageOptions.cs`, `Models/PresignedUrlRequest.cs`, `Endpoints/StorageEndpointHandlers.cs`.

- Current validator checks only:
  - `FileName` required (`FILE_VAL_001`)
  - `FileSizeKB <= MaxFileSizeKB` (`FILE_002`)
- No active MIME allowlist validation is implemented in current source.
- `AllowedContentTypes` is explicitly marked legacy/backward-compatibility.
- `UseDefaultContentTypesIfEmpty()` is `[Obsolete]` and currently no-op.
- Endpoint handlers default missing `ContentType` to `application/octet-stream` before calling storage service.

## Health Check

Defined in `HealthChecks/HealthCheckExtensions.cs`.

```csharp
IHealthChecksBuilder AddS3StorageHealthCheck(this IHealthChecksBuilder builder, string name = "s3-storage", HealthStatus? failureStatus = null, IEnumerable<string>? tags = null, TimeSpan? timeout = null)
```

Implementation details from `HealthChecks/S3StorageHealthCheck.cs`:
- Uses `ListObjectsV2Async` with `MaxKeys = 1` to verify connectivity/permissions.
- Healthy result data includes `bucket` and `region`.
- Unhealthy mappings include:
  - `BucketNotFound` for `404`
  - `AccessDenied` for `403`
  - `Unknown` (or AWS `ErrorCode`) for other S3 errors
