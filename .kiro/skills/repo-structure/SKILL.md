---
name: repo-structure
description: >
  Repository codification and project type inference for ANTA multi-repo projects.
  Given a project code and type, generates the full repository map automatically.
  Trigger: When defining repository structure, creating projects, setting up multi-repo.
metadata:
  author: anta
  version: "2.0"
  scope: [root]
  auto_invoke: "repositorio, proyecto, código de repo, multi-repo, monolito, micro-frontend, estructura de proyecto"
  phase: [inception]
  layer: null
  validates_with: validate_repo_structure
  validation_profile: structure
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Ask project code FIRST | ALWAYS | All repo names derive from it. MUST be numeric format (e.g., `200-034`). Do NOT use generic IDs (R1, R2, repo-001, TBD) |
| Ask project type SECOND | ALWAYS | Determines which repos to generate |
| ALWAYS include project code question in clarification questions | ALWAYS | This question MUST appear in the requirement-verification-questions.md file during Requirements Analysis |
| Ask modules ONLY for Micro types | CONDITIONAL | Each module = Domain API + Frontend Domain pair |
| Present generated map for confirmation | ALWAYS | User may add/remove/rename repos |
| Record confirmed map as HARD CONSTRAINT | ALWAYS | Feeds Workflow Planning, QA Matrix, HU Guides, Build & Test |

---

## Questions (in order)

### Q1: Project Code

> "¿Cuál es el código del proyecto/repositorio?"

Format: numeric with dash. Example: `000-020`, `200-026`

### Q2: Project Type

> "¿Qué tipo de proyecto es?"

| Type | Description |
|------|-------------|
| **Single Repo** | Everything in one repository |
| **Monolith Web** | Single backend + single frontend |
| **Monolith Mobile** | Single backend + mobile app |
| **Monolith Web+Mobile** | Single backend + web + mobile |
| **Micro Web** | Microservices + micro-frontends |
| **Micro Mobile** | Microservices + mobile |
| **Micro Web+Mobile** | Microservices + micro-frontends + mobile |

### Q3: Modules (Micro types only)

> "¿Qué módulos/dominios tiene el proyecto?"

Example: `mantenimiento`, `reportes`, `seguridad`

---

## Suffix Convention

### Fixed Suffixes (one per project)

| Suffix | Role | When Present |
|--------|------|--------------|
| (none) | Single Repo | Single-repo only |
| `97` | Documentation Hub | All multi-repo |
| `40` | Core API (API Cross) | All multi-repo |
| `45` | Gateway | All multi-repo |
| `90` | Frontend Host | Web projects |
| `51` | Mobile | Mobile projects |

### Decremental Suffixes (one per module, Micro types only)

| Starting Suffix | Direction | Role | Assignment |
|----------------|-----------|------|------------|
| `39` | Decreasing (`39, 38, 37...`) | Domain API | One per module, in declaration order |
| `89` | Decreasing (`89, 88, 87...`) | Frontend Domain | One per module, in declaration order |

The first declared module gets `39`/`89`, the second gets `38`/`88`, and so on. Each module always gets a **pair** (Domain API + Frontend Domain) in Web projects, or just Domain API in Mobile-only projects.

### Naming Pattern

All repos use pure numeric codes (direct concatenation, no separator, no module names):

```
{PROJECT_CODE}{SUFFIX}
```

Example: code `000-020` + suffix `40` → `000-02040`
Example: code `000-020` + first module suffix `39` → `000-02039`
Example: code `000-020` + second module suffix `38` → `000-02038`

> **IMPORTANT**: Repository codes are ALWAYS purely numeric. The module name is tracked in the Repository Map as a label, never embedded in the code.

---

## Inference Rules

### Single Repo

| Repo | Role |
|------|------|
| `{CODE}` | Single Repo |

> Example: code `000-020` → repo `000-020`

### Monolith Web

| Repo | Role |
|------|------|
| `{CODE}97` | Documentation Hub |
| `{CODE}40` | Core API |
| `{CODE}45` | Gateway |
| `{CODE}90` | Frontend Host |

> Example: code `000-020` → `000-02097`, `000-02040`, `000-02045`, `000-02090`

### Monolith Mobile

| Repo | Role |
|------|------|
| `{CODE}97` | Documentation Hub |
| `{CODE}40` | Core API |
| `{CODE}45` | Gateway |
| `{CODE}51` | Mobile |

> Example: code `000-020` → `000-02097`, `000-02040`, `000-02045`, `000-02051`

### Monolith Web+Mobile

| Repo | Role |
|------|------|
| `{CODE}97` | Documentation Hub |
| `{CODE}40` | Core API |
| `{CODE}45` | Gateway |
| `{CODE}90` | Frontend Host |
| `{CODE}51` | Mobile |

> Example: code `000-020` → `000-02097`, `000-02040`, `000-02045`, `000-02090`, `000-02051`

### Micro Web (per module)

| Repo | Role |
|------|------|
| `{CODE}97` | Documentation Hub |
| `{CODE}40` | Core API |
| `{CODE}45` | Gateway |
| `{CODE}90` | Frontend Host |
| `{CODE}39` | Domain API — Module 1 |
| `{CODE}89` | Frontend Domain — Module 1 |
| `{CODE}38` | Domain API — Module 2 |
| `{CODE}88` | Frontend Domain — Module 2 |
| ... | (decreasing per additional module) |

> Example: code `000-020`, modules `mantenimiento, reportes` →
>
> | Code | Role | Module |
> |------|------|--------|
> | `000-02097` | Documentation Hub | — |
> | `000-02040` | Core API | — |
> | `000-02045` | Gateway | — |
> | `000-02090` | Frontend Host | — |
> | `000-02039` | Domain API | mantenimiento |
> | `000-02089` | Frontend Domain | mantenimiento |
> | `000-02038` | Domain API | reportes |
> | `000-02088` | Frontend Domain | reportes |

### Micro Mobile (per module)

| Repo | Role |
|------|------|
| `{CODE}97` | Documentation Hub |
| `{CODE}40` | Core API |
| `{CODE}45` | Gateway |
| `{CODE}51` | Mobile |
| `{CODE}39` | Domain API — Module 1 |
| `{CODE}38` | Domain API — Module 2 |
| ... | (decreasing per additional module) |

> Example: code `000-020`, modules `mantenimiento, reportes` →
>
> | Code | Role | Module |
> |------|------|--------|
> | `000-02097` | Documentation Hub | — |
> | `000-02040` | Core API | — |
> | `000-02045` | Gateway | — |
> | `000-02051` | Mobile | — |
> | `000-02039` | Domain API | mantenimiento |
> | `000-02038` | Domain API | reportes |

### Micro Web+Mobile (per module)

| Repo | Role |
|------|------|
| `{CODE}97` | Documentation Hub |
| `{CODE}40` | Core API |
| `{CODE}45` | Gateway |
| `{CODE}90` | Frontend Host |
| `{CODE}51` | Mobile |
| `{CODE}39` | Domain API — Module 1 |
| `{CODE}89` | Frontend Domain — Module 1 |
| `{CODE}38` | Domain API — Module 2 |
| `{CODE}88` | Frontend Domain — Module 2 |
| ... | (decreasing per additional module) |

> Example: code `000-020`, modules `mantenimiento, reportes` →
>
> | Code | Role | Module |
> |------|------|--------|
> | `000-02097` | Documentation Hub | — |
> | `000-02040` | Core API | — |
> | `000-02045` | Gateway | — |
> | `000-02090` | Frontend Host | — |
> | `000-02051` | Mobile | — |
> | `000-02039` | Domain API | mantenimiento |
> | `000-02089` | Frontend Domain | mantenimiento |
> | `000-02038` | Domain API | reportes |
> | `000-02088` | Frontend Domain | reportes |

---

## Output

Present generated map for user confirmation:

```markdown
## Repository Structure

Project: `{CODE}` | Type: `{TYPE}`

| ID | Code | Role | Module |
|----|------|------|--------|
| 1 | 000-02097 | Documentation Hub | — |
| 2 | 000-02040 | Core API | — |
| 3 | 000-02045 | Gateway | — |
| 4 | 000-02090 | Frontend Host | — |
| 5 | 000-02039 | Domain API | mantenimiento |
| 6 | 000-02089 | Frontend Domain | mantenimiento |
| 7 | 000-02038 | Domain API | reportes |
| 8 | 000-02088 | Frontend Domain | reportes |

> ¿Es correcta esta estructura? Puedes agregar, quitar o renombrar repositorios.
```

> Note: Repository codes are ALWAYS purely numeric (e.g., `000-02039`), never alphabetic identifiers. The Module column is a human-readable label for reference — it is NOT part of the code.

Confirmed table → **HARD CONSTRAINT** in requirements.

---

## Checklist

- [ ] Project code captured
- [ ] Project type identified
- [ ] Modules listed (if micro)
- [ ] Repo map generated with correct suffixes
- [ ] User confirmed the repo map
- [ ] Map recorded as HARD CONSTRAINT

---

## Related Skills

| Task | Skill |
|------|-------|
| Architecture patterns | `anta-architecture` |
| HU template format | `hu-template` |
| Database conventions per repo | `database` |
