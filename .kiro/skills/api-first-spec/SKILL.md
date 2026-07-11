---
name: api-first-spec
description: >
  Generate comprehensive API specification documents per module.
  Includes: Scope, ERD, Catalogs, States, Endpoints, SPs, DTOs, Business Rules, Error Codes.
  Trigger: When documenting APIs, creating spec documents, API first documentation.
metadata:
  author: anta
  version: "2.0"
  scope: [root]
  enforcement: mandatory
  auto_invoke: "api spec, api documentation, spec document, api first doc"
  phase: [inception]
  layer: null
  validates_with: validate_openapi
  validation_profile: spec-gate
---

## Purpose

Generate detailed API specification documents following ANTA standard format.

**Output:** `Documentacion/api-first/{MODULE}.md`

---

## Document Structure

```markdown
# API First - {ModuleName} ({ApiName})

| Propiedad | Valor |
|-----------|-------|
| Version | 1.0 |
| Fecha | {date} |
| Puerto | {port} |
| Base URL | `/api/v1/{resource}` |
| Esquema BD | {Schema} |

---

**CHANGELOG v1.0**
- Documento inicial
- {X} endpoints documentados
- {N} subdomains: {list}

---

## Indice

1. [Alcance](#1-alcance)
2. [Modelo de Datos](#2-modelo-de-datos)
3. [Catalogos Requeridos](#3-catalogos-requeridos)
4. [Flujo de Estados](#4-flujo-de-estados)
5. [Endpoints REST](#5-endpoints-rest)
6. [Stored Procedures](#6-stored-procedures)
7. [DTOs Compartidos](#7-dtos-compartidos)
8. [Reglas de Negocio](#8-reglas-de-negocio)
9. [Codigos de Error](#9-codigos-de-error)
```

**Full section templates:** See [assets/section-templates.md](assets/section-templates.md)

---

## Section Summary

| Section | Content |
|---------|---------|
| 1. Alcance | Included/Excluded functionality |
| 2. Modelo de Datos | Mermaid ERD + Tables list |
| 3. Catalogos | MasterTables required |
| 4. Flujo de Estados | States + Actions matrix |
| 5. Endpoints REST | Per endpoint: params, request, response, rules, SP |
| 6. Stored Procedures | Endpoint → SP mapping |
| 7. DTOs Compartidos | MasterTable, StatusItem, etc. |
| 8. Reglas de Negocio | By category (Creation, Edit, Permissions) |
| 9. Codigos de Error | VAL_xxx, BUS_xxx, NOT_FOUND |

---

## Endpoint Types

Each endpoint follows one of these response patterns:

| Type | HTTP Pattern | Response Shape | When to Use |
|------|-------------|----------------|-------------|
| List | `GET /resource` | `data.items[]` + `pagination` | Paginated listing with filters |
| Get | `GET /resource/{id}` | `data.item{}` | Single entity detail |
| Create | `POST /resource` | `data.item{}` (201) | New entity creation |
| Update | `PUT /resource/{id}` | `data.item{}` | Modify existing entity |
| Delete | `DELETE /resource/{id}` | `data.result{}` | Soft delete |
| Operation | `POST /resource/{id}/{verb}` | `data.item{}` | State transitions (submit, approve, cancel, etc.) |
| Remove | `POST /resource/{id}/sub/{subId}/remove` | `data.result{}` | Remove sub-entity with justification |
| Reorder | `PUT /resource/{id}/sub/reorder` | `data.items[]` | Reorder sub-entities |
| Search | `GET /resource` (with `limit`) | `data.items[]` (no pagination) | Autocomplete / limited search |

**Section templates for each type:** See [assets/section-templates.md](assets/section-templates.md)

---

## Generation Workflow

1. **Analyze Module**
   - Scan `Modules/{Module}/Features/` for endpoints
   - Scan `database/{Schema}/` for tables and SPs
   - Extract DTOs from Request/Response files

2. **Build Sections**
   - ERD from table relationships
   - Endpoints from code
   - SP mapping from Handler files
   - Business rules from validators and SP logic

3. **Generate Document**
   - Follow template structure
   - Include all JSON examples
   - Document all parameters

4. **Update Index**
   - Add to `Documentacion/api-first/README.md`

---

## File Locations

```
Documentacion/
└── api-first/
    ├── README.md           # Index of all API specs
    ├── {MODULE1}.md        # Module 1 spec
    ├── {MODULE2}.md        # Module 2 spec
    └── ...
```

---

## Checklist

For each API module:

- [ ] Header with version, date, port, base URL, schema
- [ ] Changelog section
- [ ] Scope (included/excluded)
- [ ] ER diagram in Mermaid
- [ ] Tables list with descriptions
- [ ] Catalogs required
- [ ] State flow diagram
- [ ] All endpoints documented with:
  - [ ] Path/Query parameters
  - [ ] Request JSON (POST/PUT)
  - [ ] Response JSON
  - [ ] Correct response shape per endpoint type (items[] vs item{} vs result{})
  - [ ] Business rules
  - [ ] Operations documented with state preconditions and resulting state
  - [ ] SP reference
- [ ] SP mapping table
- [ ] Shared DTOs
- [ ] Business rules by category
- [ ] Error codes (VAL, BUS, NOT_FOUND)
- [ ] Updated README.md index

---

## Post-Creation Tasks

After creating/updating spec:

- [ ] Update `Documentacion/api-first/README.md` index
- [ ] Update `docs/API_CATALOG.md` (use `api-catalog` skill)
- [ ] Update `CHANGELOG.md` (use `changelog` skill)

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| All section templates | [section-templates.md](assets/section-templates.md) |
| README.md template | [readme-template.md](assets/readme-template.md) |

## Related Skills

| Task | Skill |
|------|-------|
| API Catalog (summary) | `api-catalog` |
| Backend implementation | `agent-backend` |
| SP patterns | `database-sp` |
| Endpoint patterns | `dotnet-api` |
