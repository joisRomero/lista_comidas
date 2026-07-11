# Validation Templates

## Backend Validation (FluentValidation)

```csharp
public class CreateContractValidator : AbstractValidator<CreateContractCommand>
{
    public CreateContractValidator()
    {
        RuleFor(x => x.Code)
            .NotEmpty().WithMessage("VAL_001|El código es requerido|Code")
            .MaximumLength(20).WithMessage("VAL_002|Máximo 20 caracteres|Code")
            .Matches(@"^[A-Z0-9-]+$").WithMessage("VAL_003|Solo mayúsculas, números y guiones|Code");
        
        RuleFor(x => x.Amount)
            .GreaterThan(0).WithMessage("VAL_004|El monto debe ser mayor a 0|Amount");
        
        RuleFor(x => x.Email)
            .EmailAddress().When(x => !string.IsNullOrEmpty(x.Email))
            .WithMessage("VAL_005|Email inválido|Email");
    }
}
```

## Frontend Validation (Ant Design)

```typescript
const rules = {
  code: [
    { required: true, message: "El código es requerido" },
    { max: 20, message: "Máximo 20 caracteres" },
    { pattern: /^[A-Z0-9-]+$/, message: "Solo mayúsculas, números y guiones" },
  ],
  amount: [
    { required: true, message: "El monto es requerido" },
    { type: "number", min: 0.01, message: "Debe ser mayor a 0" },
  ],
};
```

## CORS Configuration

```csharp
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy.WithOrigins(
                "http://localhost:5173",
                "https://app.anta.pe")
            .AllowAnyMethod()
            .AllowAnyHeader()
            .AllowCredentials();
    });
});

app.UseCors("AllowFrontend");
```

## Security Headers

```csharp
app.Use(async (context, next) =>
{
    context.Response.Headers.Add("X-Content-Type-Options", "nosniff");
    context.Response.Headers.Add("X-Frame-Options", "DENY");
    context.Response.Headers.Add("X-XSS-Protection", "1; mode=block");
    await next();
});
```
