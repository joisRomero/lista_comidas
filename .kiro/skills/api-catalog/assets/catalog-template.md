# API Catalog Template

## Full Catalog Format

```markdown
# API Catalog - {ProjectName}

Generated: {date}

## Summary

| Module | Endpoints | SPs |
|--------|-----------|-----|
| {Module1} | 5 | 5 |
| {Module2} | 8 | 8 |
| **Total** | **13** | **13** |

---

## Module: {Module1}

| Endpoint | Method | Path | SP | Service ID | Screen | Route |
|----------|--------|------|----|------------|--------|-------|
| List {Entity} | GET | /api/v1/{entities} | `{Schema}.List{Entity}` | 100 | Listado de {Entity} | `/{entities}` |
| Get {Entity} | GET | /api/v1/{entities}/{id} | `{Schema}.Get{Entity}` | 101 | Detalle de {Entity} | `/{entities}/:id` |
| Create {Entity} | POST | /api/v1/{entities} | `{Schema}.Create{Entity}` | 102 | Crear {Entity} | `/{entities}/new` |
| Update {Entity} | PUT | /api/v1/{entities}/{id} | `{Schema}.Update{Entity}` | 103 | Editar {Entity} | `/{entities}/:id/edit` |
| Delete {Entity} | DELETE | /api/v1/{entities}/{id} | `{Schema}.Delete{Entity}` | 104 | - | - |

---

## Module: {Module2}
...
```

---

## Example Output

```markdown
# API Catalog - GestionContratos

Generated: 2026-01-17

## Summary

| Module | Endpoints | SPs |
|--------|-----------|-----|
| Casos | 5 | 5 |
| Sesiones | 4 | 4 |
| Mantenimiento | 12 | 12 |
| **Total** | **21** | **21** |

---

## Module: Casos

| Endpoint | Method | Path | SP | Service ID | Screen | Route |
|----------|--------|------|----|------------|--------|-------|
| List Case | GET | /api/v1/cases | `Casos.ListCase` | 100 | Listado de Casos | `/cases` |
| Get Case | GET | /api/v1/cases/{caseId} | `Casos.GetCase` | 101 | Detalle de Caso | `/cases/:caseId` |
| Create Case | POST | /api/v1/cases | `Casos.CreateCase` | 102 | Crear Caso | `/cases/new` |
| Update Case | PUT | /api/v1/cases/{caseId} | `Casos.UpdateCase` | 103 | Editar Caso | `/cases/:caseId/edit` |
| Delete Case | DELETE | /api/v1/cases/{caseId} | `Casos.DeleteCase` | 104 | - | - |

### Sub-entities: Case Items

| Endpoint | Method | Path | SP | Service ID | Screen | Route |
|----------|--------|------|----|------------|--------|-------|
| List Case Items | GET | /api/v1/cases/{caseId}/items | `Casos.ListCaseItem` | 110 | - | - |
| Add Case Item | POST | /api/v1/cases/{caseId}/items | `Casos.AddCaseItem` | 111 | Agregar Item | `/cases/:caseId/items/add` |
| Delete Case Item | DELETE | /api/v1/cases/{caseId}/items/{itemId} | `Casos.DeleteCaseItem` | 112 | - | - |

---

## Module: Sesiones
...
```
