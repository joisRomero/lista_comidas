---
name: swagger
description: >
  OpenAPI/Swagger documentation generation and maintenance.
  Trigger: When creating API docs, updating Swagger, generating OpenAPI specs.
metadata:
  author: anta
  version: "1.0"
  scope: [root, backend]
  auto_invoke: "swagger, openapi, api documentation, api docs"
  phase: [construction]
  layer: [backend]
  validates_with: null
  validation_profile: null
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Keep Swagger always updated | ALWAYS | Must reflect real API state |
| Include request/response examples | ALWAYS | Easier testing and understanding |
| Document all error codes | ALWAYS | Frontend needs to handle them |
| Use OpenAPI 3.0 format | ALWAYS | Industry standard |

---

## File Location

```
src/{Project}.Api/
├── swagger.json          ← Generated (don't edit manually)
└── Modules/
    └── {Module}/
        └── Features/
            └── {Feature}/
                └── Endpoint.cs  ← Swagger attributes here
```

---

## Endpoint Documentation

```csharp
app.MapPost("/", async (CreateContractRequest request, IHandler handler) =>
{
    var result = await handler.Handle(request);
    return Results.Ok(ApiResponse<ContractDto>.Ok(result));
})
.WithName("CreateContract")
.WithTags("Contracts")
.WithDescription("Creates a new contract")
.Produces<ApiResponse<ContractDto>>(200)
.Produces<ApiResponse<object>>(400)
.Produces<ApiResponse<object>>(409)
.Produces<ApiResponse<object>>(422);
```

---

## Request/Response Documentation

```csharp
/// <summary>
/// Request to create a contract
/// </summary>
public record CreateContractRequest(
    /// <summary>Unique contract code (uppercase, max 20 chars)</summary>
    /// <example>CON-2024-001</example>
    string Code,
    
    /// <summary>Contract amount in USD</summary>
    /// <example>15000.50</example>
    decimal Amount,
    
    /// <summary>Customer ID</summary>
    /// <example>123</example>
    int CustomerId
);
```

---

## Error Response Documentation

```csharp
/// <summary>
/// Standard API error response
/// </summary>
public record ApiError(
    /// <summary>Error code for programmatic handling</summary>
    /// <example>CON_002</example>
    string Code,
    
    /// <summary>Human-readable error message</summary>
    /// <example>Ya existe un contrato con este código</example>
    string Message,
    
    /// <summary>Field that caused the error (if applicable)</summary>
    /// <example>Code</example>
    string? Field
);
```

---

## Swagger UI Configuration

```csharp
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "Contracts API",
        Version = "v1",
        Description = "API for contract management"
    });
    
    // Include XML comments
    var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    c.IncludeXmlComments(xmlPath);
});

// In pipeline
app.UseSwagger();
app.UseSwaggerUI();
```

---

## OpenAPI Output Example

```yaml
paths:
  /api/v1/contracts:
    post:
      tags: [Contracts]
      summary: Creates a new contract
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateContractRequest'
            example:
              code: "CON-2024-001"
              amount: 15000.50
              customerId: 123
      responses:
        '200':
          description: Contract created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApiResponseContractDto'
        '400':
          description: Validation error
        '409':
          description: Contract already exists
        '422':
          description: Business rule violation
```

---

## Checklist

- [ ] All endpoints have `.WithName()` and `.WithTags()`
- [ ] All endpoints have `.Produces<>()` for each status code
- [ ] Request DTOs have XML comments with examples
- [ ] Response DTOs have XML comments
- [ ] Error codes documented
- [ ] Swagger UI accessible at `/swagger`
- [ ] XML documentation enabled in .csproj

---

## Related Skills

| Task | Skill |
|------|-------|
| API endpoint patterns | `dotnet-api` |
| Error codes | `error-handling` |
| API spec design | `api-first-spec` |
