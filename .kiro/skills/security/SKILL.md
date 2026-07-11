---
name: security
description: >
  Security patterns for ANTA applications.
  Trigger: When implementing validation, authorization, CORS, or security headers.
metadata:
  author: anta
  version: "1.0"
  scope: [root]
  auto_invoke: "security, validation, XSS, SQL injection, CORS, authorization"
  phase: [inception, construction]
  layer: [backend]
  validates_with: null
  validation_profile: null
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Use parameterized queries (Dapper) | ALWAYS | SQL injection prevention |
| Validate on backend, not just frontend | ALWAYS | Frontend can be bypassed |
| Use Lion for authorization | ALWAYS | Centralized permission management |
| Sanitize user-generated content display | ALWAYS | XSS prevention |

---

## SQL Injection Prevention

```csharp
// ✅ SAFE - Dapper automatically parameterizes
await connection.QueryAsync<Entity>(
    "Schema.GetEntity",
    new { Id = request.Id, Name = request.Name },
    commandType: CommandType.StoredProcedure);

// ❌ UNSAFE - NEVER DO THIS
var sql = $"SELECT * FROM Users WHERE Name = '{name}'";
```

---

## Input Validation (Quick Reference)

| Layer | Tool | Error Format |
|-------|------|--------------|
| Backend | FluentValidation | `VAL_001\|Message\|Field` |
| Frontend | Ant Design rules | `{ required: true, message: "..." }` |

See [validation-templates.md](assets/validation-templates.md) for full examples.

---

## Authorization (Lion)

### Backend

```csharp
app.MapGet("/", async (ILionService lion, HttpContext ctx) =>
{
    var hasAccess = await lion.HasPermissionAsync(
        ctx.User.GetUserId(), "contracts", "read");
    
    if (!hasAccess)
        throw new ForbiddenException("AUTH_001", "Sin permiso");
});
```

### Frontend

```typescript
const { hasPermission } = useLion();

{hasPermission("contracts", "create") && (
  <Button onClick={handleCreate}>Nuevo</Button>
)}
```

---

## XSS Prevention

```tsx
// ✅ SAFE - React escapes by default
<div>{userInput}</div>

// ❌ UNSAFE - Only with DOMPurify
import DOMPurify from "dompurify";
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userInput) }} />
```

---

## Source Code Repository Security (by Provider)

When describing repository security controls (e.g., in ISO 27001 assessments), use the CORRECT terminology for each provider. DO NOT use GitHub terminology for non-GitHub providers.

| Control | GitHub | Azure DevOps | AWS CodeCommit | Bitbucket |
|---------|--------|-------------|----------------|-----------|
| Branch restrictions | Branch protection rules | Branch policies | **Approval Rule Templates** + IAM branch policies | Branch permissions |
| Code review enforcement | Required reviews | Required reviewers | **Approval Rule Templates** (min approvals) | Required approvals |
| Auth method | PAT / SSH / GitHub App | PAT / SSH / Azure AD | **IAM + AWS SSO** (git-remote-codecommit) | PAT / SSH / App passwords |
| Merge strategy | Merge / Squash / Rebase | Merge / Squash / Semi-linear | **Fast-forward only** (default) | Merge / Squash |
| CI triggers | GitHub Actions | Azure Pipelines | **CodePipeline + CodeBuild** | Bitbucket Pipelines |

**CRITICAL**: AWS CodeCommit does NOT have "branch protection" as a feature name. The equivalent is **Approval Rule Templates** for review enforcement and **IAM policies** for branch access control. Never write "CodeCommit: branch protection" — this is incorrect.

---

## Checklist

- [ ] All DB queries use parameterized Dapper calls
- [ ] FluentValidation on all commands
- [ ] Lion permission check on sensitive endpoints
- [ ] No `dangerouslySetInnerHTML` without DOMPurify
- [ ] CORS configured only for known origins
- [ ] Security headers in Gateway
- [ ] No secrets in frontend code or logs

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Validation templates, CORS, headers | [validation-templates.md](assets/validation-templates.md) |

## Related Skills

| Task | Skill |
|------|-------|
| Lion authorization | `lion` |
| Happy authentication | `happy` |
| Gateway configuration | `dotnet-gateway` |
| Error handling | `error-handling` |
