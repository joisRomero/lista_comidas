---
name: happy
description: >
  ANTA authentication library. Handles token validation via AWS Cognito, user identity resolution,
  and HeaderToken propagation from ApiGateway to internal APIs.
  Trigger: When implementing login, logout, tokens, session management, or authentication flow.
metadata:
  author: anta
  version: "2.0"
  scope: [root]
  enforcement: mandatory
  auto_invoke: "authentication, login, logout, token, session, Happy, HeaderToken, auth"
  phase: [construction]
  layer: [backend, frontend]
  validates_with: validate_auth_pattern
  validation_profile: cross-cutting
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| NEVER use standard Bearer JWT in internal APIs | ALWAYS | ANTA uses Happy + HeaderToken pattern, not raw JWT |
| Internal APIs get `HeaderToken` via DI, not from HTTP headers directly | ALWAYS | Gateway handles token validation, APIs consume `HeaderToken` object |
| Use `[FromServices] HeaderToken headerToken` in endpoint handlers | ALWAYS | Injected by `AddHeaderToken()` middleware |
| Use `headerToken.EmployeeId` for audit fields (RecordCreationUser, RecordEditUser) | ALWAYS | Consistent user identification |
| OpenAPI specs MUST NOT use `BearerAuth` security scheme | ALWAYS | Use `code` + `header` apiKey schemes (matches `AddSwaggerWithHappyAuth`). NEVER `BearerAuth`, `HappyAuth` (single), or custom names |

---

## Authentication Flow

```
┌─────────────┐     code + header       ┌─────────────────────┐
│  Frontend   │ ───────────────────────►│    ApiGateway       │
│  (React)    │     (Happy encrypted)   │  (Ocelot + Happy)   │
└─────────────┘                         │                     │
                                        │  ValidationHeader   │
                                        │  Middleware:        │
                                        │  1. Extract code +  │
                                        │     header from     │
                                        │     HTTP headers    │
                                        │  2. Call Happy      │
                                        │     .GetDeserialize │
                                        │     Object()        │
                                        │  3. Validate token  │
                                        │     expiration      │
                                        │  4. Call Happy      │
                                        │     .GetHeaderValid │
                                        │     ate() for       │
                                        │     permissions     │
                                        │  5. Convert to      │
                                        │     HeaderToken     │
                                        │  6. Serialize as    │
                                        │     HTTP header     │
                                        │     "HeaderToken"   │
                                        └──────────┬──────────┘
                                                   │ HeaderToken (JSON in header)
                                        ┌──────────▼──────────┐
                                        │   Internal API      │
                                        │  (.NET 8 Minimal)   │
                                        │                     │
                                        │  AddHeaderToken()   │
                                        │  → Deserializes     │
                                        │    header to DI     │
                                        │  → Injectable as    │
                                        │    [FromServices]   │
                                        │    HeaderToken      │
                                        └─────────────────────┘
```

---

## Gateway Setup (ApiGateway/Program.cs)

```csharp
// Happy Service registration
builder.Services.AddAntaminaHappy(
    options =>
    {
        var section = configuration.GetSection(nameof(ServiceHappyOptions));
        section.Bind(options);
    },
    tracking =>
    {
        tracking.PathHeaderName = "trexa";
        tracking.MethodHeaderName = "trexb";
        tracking.Enabled = true;
    })
.AddAntaminaAuditEndpoint(opt => opt.SaveToDatabase = isSaveAuditHappy);

// In pipeline (AFTER UseOcelot routing, BEFORE request forwarding)
app.UseValidationHeader();
await app.UseOcelot();
```

---

## Internal API Setup (Api{Module}/Program.cs)

```csharp
// Register HeaderToken deserialization from Gateway header
builder.Services.AddHeaderToken();
```

One line. The `AddHeaderToken()` extension method:
1. Reads the `HeaderToken` HTTP header from incoming request
2. Deserializes the JSON to a `HeaderToken` object
3. Registers it in DI as scoped service
4. Available via `[FromServices] HeaderToken headerToken` in any endpoint

---

## Endpoint Usage

```csharp
public static class CreateEmployeeEndpoint
{
    public static void Map(IEndpointRouteBuilder app)
    {
        app.MapPost("/", Handle)
            .WithValidation<CreateEmployeeRequest>()
            .Produces<ApiResponse<ItemData<CreateEmployeeItem>>>(StatusCodes.Status201Created)
            .ProducesProblem(StatusCodes.Status400BadRequest);
    }

    private static async Task<IResult> Handle(
        CreateEmployeeRequest request,
        [FromServices] CreateEmployeeHandler handler,
        [FromServices] HeaderToken headerToken,     // ← Injected by AddHeaderToken()
        CancellationToken ct)
    {
        var result = await handler.HandleAsync(request, headerToken, ct);
        return Results.Created($"/{result.EmployeeId}",
            ApiResponse<ItemData<CreateEmployeeItem>>.Ok(result));
    }
}
```

### Using HeaderToken for audit

```csharp
// In Handler — pass user to SP for audit columns
var parameters = new
{
    ParamIFirstName = request.FirstName,
    ParamILastName = request.LastName,
    // ... other params
    ParamIRecordCreationUser = headerToken.EmployeeId  // ← From HeaderToken
};
```

---

## Frontend Headers

The frontend does NOT send Bearer tokens. It sends:

| Header | Value | Description |
|--------|-------|-------------|
| `code` | Encrypted string | Happy-encrypted session code |
| `header` | Encrypted string | Happy-encrypted user data |

These are obtained from the Happy login flow and stored in the frontend session.

---

## OpenAPI Spec — Security Schemes

**DO NOT use BearerAuth.** The correct security schemes for ANTA APIs:

### Gateway-facing spec (what Swagger UI shows — matches `AddSwaggerWithHappyAuth()`)

The NuGet `ANTA.Shared.Common.Api` defines TWO `apiKey` schemes with literal names `code` and `header`:

```yaml
components:
  securitySchemes:
    code:
      type: apiKey
      in: header
      name: code
      description: Código de autenticación Happy
    header:
      type: apiKey
      in: header
      name: header
      description: Token JWT del usuario (HeaderToken)

security:
  - code: []
    header: []
```

This is what `AddSwaggerWithHappyAuth(title, version, description)` generates. Use EXACTLY these scheme names — NOT `HappyAuth`, NOT `HappyAuthCode`, NOT `BearerAuth`.

### Internal API header (Gateway → Internal API)

The Gateway middleware `UseValidationHeader()` validates `code` + `header`, calls Happy service, and injects a serialized `HeaderToken` JSON as the `headertoken` HTTP header to internal APIs. Internal APIs read it via `AddHeaderToken()` → `[FromServices] HeaderToken headerToken`.

### Which to use in OpenAPI specs?

- **All ANTA APIs**: Use `code` + `header` schemes (matches `AddSwaggerWithHappyAuth`)
- **NEVER**: `BearerAuth`, `Bearer`, `HappyAuth` (single), or raw JWT schemes

---

## Excluded Paths (no auth required)

The Gateway skips authentication for:
- `/health` — health checks
- `/swagger` — API documentation
- Static files (`.ico`, `.png`, `.css`, `.js`, etc.)
- Paths listed in `ExcludePath` config section

---

## Key Types

| Type | Package | Description |
|------|---------|-------------|
| `HeaderToken` | ANTA.Shared.Common | User context object (UserCode, roles, etc.) |
| `IAuthentication` | ANTA.Shared.Happy.Services | Happy auth service interface |
| `ServiceHappyOptions` | ANTA.Shared.Happy.Configuration | Happy service URL + config |
| `EncryptRequest` | ANTA.Shared.Happy.Models | Input for decrypt (Code + TextTransform) |
| `HappyUserResponse` | ANTA.Shared.Happy.Models | Decrypted user data from Happy |
| `HeaderValidateRequest` | ANTA.Shared.Happy.Models | Input for permission validation |

---

## Checklist

- [ ] Gateway: `AddAntaminaHappy()` registered with correct options
- [ ] Gateway: `UseValidationHeader()` in pipeline before `UseOcelot()`
- [ ] Internal API: `AddHeaderToken()` in Program.cs
- [ ] Endpoints: `[FromServices] HeaderToken headerToken` parameter
- [ ] Handlers: Use `headerToken.EmployeeId` for audit fields
- [ ] OpenAPI: Security schemes use literal names `code` and `header` (matches `AddSwaggerWithHappyAuth`)
- [ ] OpenAPI: BOTH schemes listed in `security` array (AND-logic)
- [ ] OpenAPI: NO `BearerAuth`, `Bearer`, `HappyAuth` (single), or custom names
- [ ] Excluded paths configured for health/swagger/static

## Related Skills

| Task | Skill |
|------|-------|
| Authorization (roles/permisos) | `lion` |
| API endpoint patterns | `dotnet-api` |
| Gateway configuration | `dotnet-gateway` |
