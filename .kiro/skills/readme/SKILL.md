---
name: readme
description: >
  README template for ANTA modules.
  Trigger: When creating module documentation, README files, or project docs.
metadata:
  author: anta
  version: "1.0"
  scope: [root]
  auto_invoke: "readme, module documentation, project documentation"
  phase: [operations]
  layer: null
  validates_with: null
  validation_profile: null
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Update README on every module change | ALWAYS | Keep docs current |
| Include all environment variables | ALWAYS | Deployment needs them |
| Document how to run locally | ALWAYS | Onboarding |
| Keep it concise | ALWAYS | Long READMEs don't get read |

---

## README Template

```markdown
# {Module Name}

{One-line description of what this module does}

## Quick Start

\`\`\`bash
# Backend
cd src/{Project}.Api
dotnet run

# Frontend
cd Front{Module}/src/{Project}.Front
npm install && npm run dev
\`\`\`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/{entities} | List all |
| GET | /api/v1/{entities}/{id} | Get by ID |
| POST | /api/v1/{entities} | Create |
| PUT | /api/v1/{entities}/{id} | Update |
| DELETE | /api/v1/{entities}/{id} | Delete |

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `ConnectionStrings__Default` | SQL Server connection | `Server=localhost;Database=...` |
| `Happy__BaseUrl` | Auth service URL | `https://happy.anta.pe` |
| `S3__BucketName` | Storage bucket | `anta-documents` |

## Project Structure

\`\`\`
src/{Project}.Api/
├── Program.cs
└── Modules/
    └── {Module}/
        ├── {Module}Module.cs
        └── Features/
            ├── List/
            ├── Get/
            ├── Create/
            └── Update/
\`\`\`

## Dependencies

- **Happy**: Authentication
- **Lion**: Authorization  
- **Arroba**: Notifications (if applicable)

## Related Documentation

- [API Catalog](docs/API_CATALOG.md)
- [Swagger UI](http://localhost:5000/swagger)
```

---

## README Sections by Module Type

### Backend Module

| Section | Required |
|---------|----------|
| Quick Start | ✅ |
| Endpoints | ✅ |
| Environment Variables | ✅ |
| Project Structure | ✅ |
| Dependencies | ✅ |
| Database (schemas, SPs) | Optional |

### Frontend Module

| Section | Required |
|---------|----------|
| Quick Start | ✅ |
| Pages/Routes | ✅ |
| Environment Variables | ✅ |
| Project Structure | ✅ |
| Host Dependencies | ✅ (if microfrontend) |

### Fullstack Module

Combine both, but keep it DRY. Reference shared docs.

---

## When to Update README

| Event | Action |
|-------|--------|
| New endpoint added | Add to Endpoints table |
| New env variable | Add to Environment Variables |
| New dependency | Add to Dependencies |
| Structure change | Update Project Structure |
| Module complete | Full review |

---

## Anti-Patterns

| Don't | Why |
|-------|-----|
| Copy entire API spec | That's what Swagger is for |
| Document every function | Code should be self-documenting |
| Include sensitive data | Security risk |
| Write tutorials | Keep it reference-style |

---

## Checklist

- [ ] One-line description at top
- [ ] Quick Start works (copy-paste runnable)
- [ ] All endpoints listed
- [ ] All env variables documented
- [ ] Project structure current
- [ ] Dependencies listed
- [ ] Links to related docs

---

## Related Skills

| Task | Skill |
|------|-------|
| API documentation | `swagger` |
| Changelog entries | `changelog` |
| Project structure | `anta-architecture` |
