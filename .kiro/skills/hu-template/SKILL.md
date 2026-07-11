---
name: hu-template
description: >
  Template for writing User Stories (Historias de Usuario) in ANTA format.
  Input for API First specs. Follows standard format with acceptance criteria.
  Trigger: When writing user stories, creating HUs, defining requirements.
metadata:
  author: anta
  version: "2.0"
  scope: [root]
  enforcement: mandatory
  auto_invoke: "historia de usuario, user story, HU, requirements, requerimiento"
  phase: [inception]
  layer: null
  validates_with: null
  validation_profile: null
---

## Purpose

Define User Stories (HUs) that serve as input for API First specifications.

```
HU (QUÉ quiere el usuario) → API First (CÓMO se implementa) → Implementación
```

---

## HU Template

```markdown
## {REPO_CODE}-{SEQ}: {Título descriptivo}

**Epic:** {Epic Name}
**Layer:** {FRONT / APIGATEWAY / BACK}
**Repo:** {REPO_CODE}

### Historia

**Como** {rol/actor}
**Quiero** {acción/funcionalidad}
**Para** {beneficio/valor}

### Descripción

{Contexto adicional}

### Criterios de Aceptación

- [ ] CA1: {Criterio verificable}
- [ ] CA2: {Criterio verificable}

### Reglas de Negocio

| Regla | Descripción |
|-------|-------------|
| RN-001 | {Regla} |

### Mockup/Prototipo

> Referencia: {Link a Miro/Figma}

### Datos de Prueba

| Escenario | Input | Output Esperado |
|-----------|-------|-----------------|
| Happy path | {datos} | {resultado} |
| Error | {datos inválidos} | {mensaje} |

### Dependencias

- [ ] {REPO_CODE}-{OTHER}: {Dependencia}
- [ ] Catálogo: {Catálogo requerido}

### Notas Técnicas

{Consideraciones para el dev}

---

**Prioridad:** {Alta/Media/Baja}
**Estimación:** {S/M/L/XL}
**Sprint:** {número}
```

---

## HU Numbering and Grouping

### Single-Repo Projects

When the project uses **Single-Repo** architecture (no `repo-structure` skill, or single repo declared):

- **Repo Code** = project code (e.g., `200-034`)
- **Layer** = `FULL` (BD + BACK + FRONT in same repo). Exception: backend-only or frontend-only HUs use `BACK` or `FRONT`
- **Numbering** = `{PROJECT_CODE}-{SEQ}` — single continuous sequence

```
EPIC: {Epic Name} | {MODULE}
├── 200-034-001  HU (FULL — Listado de empleados)
├── 200-034-002  HU (FULL — Crear empleado)
├── 200-034-003  HU (BACK — Notificaciones de workflow)
└── 200-034-004  HU (FULL — Eliminar empleado)
```

### Multi-Repo Projects

When the project uses **Multi-Repo** architecture (via `repo-structure` skill):

### Epic Level (Grouping)

Each Epic groups all HUs for a functional module. The Epic is identified by the **module name** and contains HUs from all repos involved.

```
EPIC: {Epic Name} | {MODULE}
├── {REPO_CODE_1}-001  HU (Layer 1)
├── {REPO_CODE_1}-002  HU (Layer 1)
├── {REPO_CODE_2}-001  HU (Layer 2)
└── {REPO_CODE_3}-001  HU (Layer 3)
```

### HU Numbering Convention

```
{REPO_CODE}-{SEQUENTIAL}
```

- `{REPO_CODE}`: Numeric repository code from the `repo-structure` skill (e.g., `200-14890`)
- `{SEQUENTIAL}`: Three-digit number starting at `001`, **continuous per repo** (never resets)

Each repo maintains its own independent sequential counter. Domain repos (suffixes 39, 38... / 89, 88...) naturally belong to one module, so their numbering is scoped to that module. Base repos (Host 90, Gateway 45, Cross 40) accumulate HUs across all modules with a single continuous sequence.

### Grouping by Layer/Repo

HUs within an Epic are grouped by layer (repo):

| Layer | Suffix | Repo Code (example) | HU Examples |
|-------|--------|---------------------|-------------|
| **FRONT HOST** | `90` | `200-14890` | `200-14890-001`, `200-14890-002` |
| **FRONT DOMAIN** | `89, 88...` | `200-14889` (module 1) | `200-14889-001`, `200-14889-002` |
| **FRONT DOMAIN** | | `200-14888` (module 2) | `200-14888-001` |
| **APIGATEWAY** | `45` | `200-14845` | `200-14845-001` |
| **BACK CROSS** | `40` | `200-14840` | `200-14840-001`, `200-14840-002` |
| **BACK DOMAIN** | `39, 38...` | `200-14839` (module 1) | `200-14839-001`, `200-14839-002` |
| **BACK DOMAIN** | | `200-14838` (module 2) | `200-14838-001` |

### Complete Example (Micro Web — 2 modules)

Project code: `200-148` | Modules: `mantenimiento` (first), `sesiones` (second)

```markdown
## EPIC: Gestión de Mantenimiento | MANTENIMIENTO

| Layer | Code | Type | Title |
|-------|------|------|-------|
| **EPIC** | — | MOD | Gestión de Mantenimiento |
| FRONT HOST | 200-14890-001 | HU | Agregar ruta Mantenimiento al menú |
| FRONT MANT | 200-14889-001 | HU | Pantalla listado de equipos |
| FRONT MANT | 200-14889-002 | HU | Formulario creación de equipo |
| FRONT MANT | 200-14889-003 | HU | Pantalla detalle de equipo |
| APIGATEWAY | 200-14845-001 | HU | Ruta gateway /mantenimiento/* |
| BACK MANT | 200-14839-001 | HU | SP ListEquipment + endpoint GET |
| BACK MANT | 200-14839-002 | HU | SP CreateEquipment + endpoint POST |
| BACK MANT | 200-14839-003 | HU | SP GetEquipment + endpoint GET/:id |
| BACK CROSS | 200-14840-001 | HU | Servicio lookup catálogos compartidos |

## EPIC: Gestión de Sesiones | SESIONES

| Layer | Code | Type | Title |
|-------|------|------|-------|
| **EPIC** | — | MOD | Gestión de Sesiones |
| FRONT HOST | 200-14890-002 | HU | Agregar ruta Sesiones al menú |
| FRONT SES | 200-14888-001 | HU | Pantalla listado de sesiones |
| FRONT SES | 200-14888-002 | HU | Pantalla detalle de sesión |
| APIGATEWAY | 200-14845-002 | HU | Ruta gateway /sesiones/* |
| BACK SES | 200-14838-001 | HU | SP ListSessions + endpoint GET |
| BACK SES | 200-14838-002 | HU | SP GetSession + endpoint GET/:id |
```

Note how base repos continue their numbering across epics:
- **Front Host** (`200-14890`): `-001` in Mantenimiento, `-002` in Sesiones
- **Gateway** (`200-14845`): `-001` in Mantenimiento, `-002` in Sesiones
- **Domain repos** start at `-001` within their own module (each domain repo belongs to exactly one module)

> **Requires**: `repo-structure` skill loaded to derive repo codes. If no repo-structure skill, fall back to manual repo IDs.

---

## Acceptance Criteria - SMART

| Attribute | Description |
|-----------|-------------|
| **S**pecific | Claro y sin ambigüedad |
| **M**easurable | Se puede verificar |
| **A**chievable | Técnicamente posible |
| **R**elevant | Aporta valor |
| **T**estable | QA puede probarlo |

| ❌ Bad | ✅ Good |
|--------|---------|
| "El sistema es rápido" | "Carga en menos de 2s" |
| "Funciona bien" | "Muestra mensaje de éxito" |

---

## HU to API First Mapping

| HU Section | API First Section |
|------------|-------------------|
| Criterios de Aceptación | Endpoints |
| Reglas de Negocio | Business Rules + SP |
| Datos de Prueba | Request/Response examples |
| Dependencias (catálogos) | Catálogos Requeridos |

---

## Checklist

- [ ] HU code follows `{REPO_CODE}-{SEQ}` format
- [ ] HU assigned to correct Epic and Layer
- [ ] Formato "Como/Quiero/Para"
- [ ] Al menos 3 criterios de aceptación
- [ ] Criterios verificables (testables)
- [ ] Reglas de negocio documentadas
- [ ] Link a mockup/prototipo
- [ ] Datos de prueba (happy + error)
- [ ] Dependencias identified with correct repo codes
- [ ] Prioridad y estimación

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Complete HU example | [hu-example.md](assets/hu-example.md) |

## Related Skills

| Task | Skill |
|------|-------|
| API specification | `api-first-spec` |
| Backend implementation | `agent-backend` |
| Frontend implementation | `agent-frontend` |
