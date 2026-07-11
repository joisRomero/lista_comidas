---
name: dotnet-gateway
description: >
  API Gateway patterns with Ocelot, Happy auth, header validation, and distributed tracing.
  Trigger: When creating or modifying API Gateway, Ocelot configuration, or authentication middleware.
metadata:
  author: anta
  version: "2.0"
  scope: [root]
  auto_invoke: "ApiGateway, Ocelot, HeaderToken, ValidationHeader, DelegatingHandler"
  phase: [construction]
  layer: [backend]
  validates_with: null
  validation_profile: null
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Validate `code` and `header` headers via Happy | ALWAYS | Authentication |
| Convert HappyUser to HeaderToken for internal APIs | ALWAYS | Standardized identity |
| Propagate X-Correlation-Id to downstream services | ALWAYS | Distributed tracing |
| Use AuditHttp in Gateway (not in internal APIs) | ALWAYS | Single audit point |
| Exclude system paths from auth validation | ALWAYS | Health checks, Swagger |
| Upstream routes use `/{Service}/api/v1/{everything}` pattern | ALWAYS | PascalCase service prefix |
| Gateway PathBase is `/apigateway` | ALWAYS | Consistent URL prefix |

---

## Gateway vs Internal API Responsibilities

| Concern | Gateway | Internal API |
|---------|---------|--------------|
| Happy auth validation | YES | NO |
| AuditHttp (request/response logging) | YES | NO |
| LogHttp (exception logging) | YES | YES |
| CorrelationId generation | YES | NO (receives from Gateway) |
| HeaderToken parsing | NO (creates it) | YES (reads it) |
| Swagger aggregation | YES | YES (individual) |

---

## Key Packages

| Package | Version |
|---------|---------|
| Ocelot | 23.2.0 |
| MMLib.SwaggerForOcelot | 8.2.0 |
| Microsoft.AspNetCore.Authentication.JwtBearer | 8.0.3 |
| ANTA.Shared.Happy | 1.0.0-beta.41 |
| Dapper | 2.1.35 (audit logging) |

---

## HeaderToken Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                           GATEWAY                                    │
├─────────────────────────────────────────────────────────────────────┤
│  1. Receive request with 'code' and 'header' headers               │
│  2. Validate via Happy service (GetDeserializeObject)              │
│  3. Get HappyUserResponse → Convert to HeaderToken                  │
│  4. Serialize HeaderToken → Add as 'HeaderToken' header             │
│  5. Forward to internal API via Ocelot                              │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        INTERNAL API                                  │
├─────────────────────────────────────────────────────────────────────┤
│  1. AddHeaderToken() parses 'HeaderToken' header                    │
│  2. Endpoint reads IHeaderToken from HttpContext                    │
│  3. Pass currentUser to handler from HeaderToken.EmployeeId         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Happy Auth Integration (Detailed)

The `ValidationHeaderMiddleware` performs the full auth flow:

1. **Required headers from client**: `code` and `header`
2. **Auth steps**:
   1. `IAuthentication.GetDeserializeObject()` → decrypt credentials
   2. Deserialize response to `HappyUserResponse`
   3. Validate JWT token expiration (check `exp` claim)
   4. `IAuthentication.GetHeaderValidate()` → permission check
   5. Convert to `HeaderToken` → serialize → add as request header
3. **Tracking headers**: `trexa` (request path), `trexb` (HTTP method)

---

## Middleware Order (CRITICAL)

```csharp
// Localization (es-PE)
app.UseRequestLocalization(...);

app.UseCorrelationId();            // 1. Distributed tracing
app.UseAntaminaAuditHttp();        // 2. Request/response capture
app.UseAntaminaExceptionHandler(); // 3. Exception handling

app.UsePathBase("/apigateway");    // 4. Path prefix
app.UseSwagger();                  // 5. Swagger
app.UseSwaggerForOcelotUI(...);    // 6. Aggregated Swagger UI
app.UseCors("All");                // 7. CORS
app.UseStaticFiles();
app.UseRouting();
app.UseAuthorization();
app.MapControllers();

app.MapHealthChecks("/health", ...);  // 8. Health checks

app.UseValidationHeader();         // 9. Happy auth validation (BEFORE Ocelot)
await app.UseOcelot();             // 10. LAST - route to downstream
```

---

## CORS Policy

```csharp
builder.Services.AddCors(o => o.AddPolicy("All", builder =>
    builder.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader()
));
```

> **Note:** Very permissive — suitable for internal APIs behind VPN.

---

## Ocelot Configuration

`configuration.{Environment}.json`:

**Route pattern**: `/{Service}/api/v1/{everything}` → `/api/v1/{everything}`

- Upstream uses **PascalCase** service prefix (e.g. `/{Module}/...`)
- Downstream strips the prefix, routing to `/api/v1/{everything}`
- Each route includes `UpstreamHeaderTransform` for IP forwarding

```json
{
  "Routes": [
    {
      "UpstreamPathTemplate": "/{Module}/api/v1/{everything}",
      "DownstreamPathTemplate": "/api/v1/{everything}",
      "DownstreamScheme": "http",
      "DownstreamHostAndPorts": [{ "Host": "{DownstreamHost}", "Port": {DownstreamPort} }],
      "UpstreamHttpMethod": ["GET", "POST", "DELETE", "PUT", "PATCH"],
      "SwaggerKey": "Api{Module}",
      "UpstreamHeaderTransform": { "IpClient": "{RemoteIpAddress}" }
    }
  ],
  "SwaggerEndPoints": [
    {
      "Key": "Api{Module}",
      "Config": [{ "Name": "{Module} API", "Version": "v1", "Url": "{DownstreamSwaggerUrl}" }]
    }
  ],
  "GlobalConfiguration": {
    "BaseUrl": "{GatewayBaseUrl}"
  }
}
```

### Generic Downstream Services

| Service | SwaggerKey | Upstream Prefix |
|---------|-----------|-----------------|
| `{Module}` | `Api{Module}` | `/{Module}/api/v1/{everything}` |
| `{Feature}` | `Api{Feature}` | `/{Feature}/api/v1/{everything}` |
| `Session` | `ApiSession` | `/Session/api/v1/{everything}` |

> Keep routes and downstream URLs environment-driven in `configuration.{Environment}.json`.

---

## DelegatingHandlers

Register in Program.cs:

```csharp
builder.Services.AddOcelot(configuration)
    .AddDelegatingHandler<CorrelationIdDelegatingHandler>(true)
    .AddDelegatingHandler<MissingBodyDelegatingHandler>(true);
```

| Handler | Purpose |
|---------|---------|
| `CorrelationIdDelegatingHandler` | Propagates X-Correlation-Id to downstream |
| `MissingBodyDelegatingHandler` | Handles multipart form data forwarding |

---

## Excluded Paths

Paths excluded from Happy auth validation (configured in `appsettings.json`):

```json
"ExcludePath": ["/swagger", "/health"]
```

---

## Health Checks

```csharp
builder.Services.AddHealthChecks()
    .AddHappyServiceHealthCheck(tags: ["external"]);
```

Mapped at `/health` with JSON response formatter.

---

## Checklist

- [ ] DelegatingHandlers registered: CorrelationId, MissingBody
- [ ] ValidationHeaderMiddleware BEFORE Ocelot (step 9 → 10)
- [ ] AuditHttp in Gateway only
- [ ] LogHttp in both Gateway and Internal APIs
- [ ] Excluded paths configured: `/swagger`, `/health`
- [ ] HeaderToken created from HappyUser and forwarded
- [ ] SwaggerForOcelot configured with all downstream APIs (`Api{Module}`, `Api{Feature}`, etc.)
- [ ] CORS "All" policy configured
- [ ] Health checks include Happy service
- [ ] PathBase set to `/apigateway`
- [ ] Upstream routes use `/{Service}/api/v1/{everything}` pattern

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Program.cs template | [program-template.cs](assets/program-template.cs) |
| DelegatingHandlers | [delegating-handlers.cs](assets/delegating-handlers.cs) |

---

## Related Skills

| Task | Skill |
|------|-------|
| Internal API Setup | `dotnet-startup` |
| Handler Patterns | `dotnet-handler` |
| Happy Library | `happy` |
