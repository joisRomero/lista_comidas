---
name: api-catalog
description: >
  Generate complete API inventory/catalog documenting all endpoints end-to-end.
  Maps: SP → API Endpoint → Service ID → Frontend Screen → Route.
  Trigger: When documenting APIs, creating service inventory, onboarding docs.
metadata:
  author: anta
  version: "1.0"
  scope: [root]
  auto_invoke: "api catalog, api inventory, service catalog, endpoint documentation"
  phase: [operations]
  layer: null
  validates_with: null
  validation_profile: null
---

## Purpose

Generate a complete inventory of all services in the project, mapping:

```
Database (SP) → Backend (Endpoint) → Service ID → Frontend (Screen + Route)
```

Useful for: Documentation, Developer onboarding, Frontend/Backend coordination, QA test planning

---

## Quick Reference

### Generation Workflow

```
1. Scan database/ for SP files → Extract: Schema, Action, Entity
2. Scan Modules/ for Endpoint files → Extract: Method, Path, Name
3. Match SP ↔ Endpoint by naming convention
4. Get Service IDs from config/DB
5. Scan frontend routes → Map API path to frontend route
6. Generate markdown catalog
```

### Data Source Locations

| Source | Location |
|--------|----------|
| Stored Procedures | `database/{Schema}/StoredProcedures/` |
| Endpoints | `src/{Project}.Api/Modules/{Module}/Features/` |
| Module Registration | `src/{Project}.Api/Modules/{Module}/{Module}Module.cs` |
| SP Constants | `src/{Project}.Api/Modules/{Module}/{Module}StoredProcedures.cs` |
| Service IDs | Database menu config or `mf-remotes.json` |
| Frontend Routes | `Front{Module}/src/{Project}.Front/src/App.tsx` |

### Naming Convention Mapping

| Endpoint Name | SP Name | Method | Path |
|---------------|---------|--------|------|
| `List{Entity}` | `{Schema}.List{Entity}` | GET | `/{entities}` |
| `Get{Entity}` | `{Schema}.Get{Entity}` | GET | `/{entities}/{id}` |
| `Create{Entity}` | `{Schema}.Create{Entity}` | POST | `/{entities}` |
| `Update{Entity}` | `{Schema}.Update{Entity}` | PUT | `/{entities}/{id}` |
| `Delete{Entity}` | `{Schema}.Delete{Entity}` | DELETE | `/{entities}/{id}` |

### Screen Name Convention

| Action | Screen Name |
|--------|-------------|
| List | `Listado de {Entity}` |
| Get | `Detalle de {Entity}` |
| Create | `Crear {Entity}` |
| Update | `Editar {Entity}` |
| Delete | - (no screen) |

---

## Output Location

Save catalog to:
- `docs/API_CATALOG.md` - Main documentation
- Update `project-context` Service IDs section

---

## Checklist

- [ ] Scanned all SP files in database/
- [ ] Scanned all Endpoint files in Modules/
- [ ] Matched SP ↔ Endpoint by convention
- [ ] Retrieved Service IDs
- [ ] Mapped frontend routes
- [ ] Generated summary table
- [ ] Generated per-module tables
- [ ] Saved to docs/API_CATALOG.md
- [ ] Updated project-context

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Catalog template and example | [catalog-template.md](assets/catalog-template.md) |
| Data sources and conventions | [data-sources.md](assets/data-sources.md) |

## Related Skills

| Task | Skill |
|------|-------|
| SP patterns | `database-sp` |
| Endpoint patterns | `dotnet-api` |
| Frontend routes | `react` |
| Project context | `project-context` |
