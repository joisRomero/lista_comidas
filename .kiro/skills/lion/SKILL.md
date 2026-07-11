---
name: lion
description: >
  ANTA authorization system. Generates authorization matrices from API specs and role definitions.
  Optionally registers in Lion via MCP. During Construction, provides integration hooks for
  frontend (AuthGuard, process checks) and backend (ProfileCodes).
  Trigger: When defining permissions, roles, access control, or generating authorization matrices.
metadata:
  author: anta
  version: "2.0"
  scope: [root]
  enforcement: mandatory
  auto_invoke: "authorization, permissions, roles, access control, Lion, profile, process, option, service, authorization matrix"
  phase: [inception, construction]
  layer: [backend, frontend]
  validates_with: null
  validation_profile: null
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| ALWAYS generate the Authorization Matrix BEFORE writing any permission code | ALWAYS | The matrix is the single source of truth — all code derives from it |
| Matrix is the primary artifact — Lion MCP registration is optional | ALWAYS | MCP may not be available; the matrix must be self-sufficient |
| Processes are OPTIONAL — only define when a screen needs per-action control | CONTEXT | Simple screens where all users can do everything don't need processes |
| Services are scoped PER OPTION, not globally per application | ALWAYS | Each screen declares which endpoints it can call |
| ProfileCodes constants MUST match Lion profile codes exactly | ALWAYS | Mismatch causes silent authorization failures |

---

## Lion Data Model

```
Application
├── Options (screens — hierarchical tree)
│   ├── Services (API endpoints per screen)
│   └── Processes (actions/buttons per screen)
├── Profiles (roles)
│   ├── Profile ↔ Options (screen access)
│   └── Profile ↔ Processes (action access)
├── Details (Cognito/OAuth config)
├── Hubs (portal links)
└── Application Users, Managers, Cloud Resources, Properties
```

### MasterTable Reference Codes

| Parent | Code | Name |
|--------|------|------|
| 17000 | 17001 | GET |
| 17000 | 17002 | POST |
| 17000 | 17003 | PUT |
| 17000 | 17004 | DELETE |
| 17000 | 17005 | PATCH |
| 11000 | 11012 | .NET 8.0 Angular 17 |
| 19000 | 19001 | code (Cognito response) |

---

## 3-Level Access Control

| Level | Controls | When to use |
|-------|----------|-------------|
| **1**: Profile → Option | Screen visibility | Always (minimum) |
| **2**: Profile → Process | Action permissions per screen | Roles differ in what they can DO on the same screen |
| **3**: Service → Process | Endpoint blocked without process | Full backend enforcement needed |

**Decision**: Level 1 only = simple. Level 1+2 = most apps. All 3 = strict enforcement.

---

## [Inception] Authorization Matrix

Generated during **API Contract Design — Step 6b** (see `inception/api-contract-design.md`). This is the primary deliverable.

### Matrix Format

The matrix lives in `aidlc-docs/authorization-matrix.md` and contains 4 tables:

**Table 1 — Profiles**

| Code | Name | Description |
|------|------|-------------|
| ADMIN | Administrador | Full access |
| USER | Usuario | View + limited actions |

**Table 2 — Options (Screens)**

| Code | Name | Route | Visible | Parent | ADMIN | USER |
|------|------|-------|---------|--------|-------|------|
| 0001 | Home | / | yes | — | yes | yes |
| 0100 | Casos | cases | yes | 0001 | yes | yes |
| 0101 | Nuevo Caso | cases/create | no | 0100 | yes | — |
| 0102 | Ver Caso | cases/view | no | 0100 | yes | yes |

**Table 3 — Services (Endpoints per Screen)**

| Screen | Svc Code | Path | Method | Process |
|--------|----------|------|--------|---------|
| Casos | 3001 | /Cases/api/v1/cases | GET | — |
| Nuevo Caso | 3002 | /Cases/api/v1/cases | POST | btnNew |
| Ver Caso | 3003 | /Cases/api/v1/cases/{id} | GET | — |

**Table 4 — Processes (Actions per Screen)** — only if Level 2+

| Screen | Process Code | Name | Description | ADMIN | USER |
|--------|-------------|------|-------------|-------|------|
| Casos | btnNew | Nuevo | Create record | yes | — |
| Casos | btnEdit | Editar | Edit record | yes | — |
| Casos | btnExportExcel | Exportar | Export to Excel | yes | yes |

### How to Derive the Matrix from API Spec

**Step 1 — Identify Screens**: Group API endpoints by UI page.
- Each frontend route = one Option in Lion
- Parent screens (modules) → `is_visible: true`, shown in sidebar
- Sub-screens (create, edit, view) → `is_visible: false`, navigated to

**Step 2 — Map Endpoints to Screens**: For each screen, list its API calls.
- GET list → parent screen
- POST create → "create" sub-screen
- GET by ID → "view" sub-screen
- Shared endpoints (catalogs, employees, files) → registered on EACH screen that uses them

**Step 3 — Define Actions** (if Level 2+): For mutating operations, define processes.
- Standard naming: `btnNew`, `btnEdit`, `btnDelete`, `btnExportExcel`
- Workflow actions: `btnApprove`, `btnReject`, `btnSubmit`
- UI controls: `show{Feature}`, `only{Restriction}`

**Step 4 — Define Profiles**: From user stories / stakeholder input.
- Map each profile → screens it can access (Level 1)
- Map each profile → actions it can execute per screen (Level 2)

**Step 5 — Validate**:
- Every API spec endpoint appears in at least one screen's services
- Every screen assigned to at least one profile
- If processes exist, each assigned to at least one profile

### Option Hierarchy Convention

```
Root (visible, menu container)
├── Bienvenida (visible, landing page)
├── Module A (visible, list screen)
│   ├── Nuevo (hidden, create form)
│   ├── Editar (hidden, edit form)
│   ├── Ver Detalle (hidden, view detail)
│   └── Custom sub-screen (hidden)
├── Module B (visible, list screen)
│   └── ...
└── Mantenimiento (visible, admin config)
```

### Process Naming Convention

| Process Code | Typical Method | Description |
|-------------|----------------|-------------|
| `btnNew` | POST | Create new record |
| `btnEdit` | PUT/PATCH | Edit existing record |
| `btnDelete` | DELETE | Delete record |
| `btnExportExcel` | GET (export) | Export to Excel |
| `btnDetails` | GET (by ID) | View detail |
| `btnClone` | POST | Create from existing |
| `btnApprove` | POST/PATCH | Approve workflow item |
| `btnReject` | POST/PATCH | Reject workflow item |
| `btnSubmit` | POST | Submit for review |

---

## [Inception] Lion MCP Registration (Optional)

If Lion MCP is available (`http://localhost:8080/mcp`), register the matrix. Otherwise, the matrix document is the deliverable.

### Registration Order (MANDATORY)

```
1. create_application        → id_application
2. create_application_detail → Cognito config (if needed)
3. create_application_hub    → portal link (if needed)
4. create_option             → each screen, parents FIRST
5. create_option_process     → each action per screen (if Level 2+)
6. create_service            → each endpoint per screen, link to process if Level 3
7. create_profile            → each role
8. assign_option_to_profile  → screen × profile
9. assign_process_to_profile → action × profile (if Level 2+)
```

### MCP Concurrency

SQL Server connection limit. **Max 2 parallel MCP calls.** Batch by entity type.

### Registration Example

```
# Application
create_application(code="200-XXX", name="App Name", id_architecture="11012")

# Options (parents first)
create_option(id_application=ID, code="0001", name="Home",
              url_option="/", is_visible=true, icon_option="fas fa-home", order_option=1)
create_option(id_application=ID, code="0100", name="Module",
              id_application_option_parent=HOME_ID, url_option="module",
              is_visible=true, order_option=2)

# Processes (if Level 2+)
create_option_process(id_application_option=OPT_ID, code="btnNew",
                      name="btnNew", process_description="Create new record",
                      value_default="1")

# Services (link to process if Level 3)
create_service(id_application_option=OPT_ID, code="3001",
               path="/Module/api/v1/items", id_method="17001")
create_service(id_application_option=OPT_ID, code="3002",
               path="/Module/api/v1/items", id_method="17002",
               id_application_option_process=PROCESS_ID)

# Profiles + assignments
create_profile(id_application=ID, code="ADMIN", name="Administrador")
assign_option_to_profile(id_application_profile=PROF_ID, id_application_option=OPT_ID)
assign_process_to_profile(id_application_option_process=PROC_ID,
                          id_application_profile=PROF_ID)
```

---

## [Construction] Frontend Integration Hooks

These apply when building the frontend. The `react` skill handles component patterns — this section covers only Lion-specific authorization hooks.

### How Permissions Arrive

Login (Happy) → `SecurityService.Access()` → Lion returns `Profile[].Option[].Process[] + Service[]` → stored in `sessionStorage`.

The frontend does NOT call Lion directly. Permissions arrive via Happy as a nested structure:
`Profile → Option[] → Process[] + Service[]`.

### What to Implement

| What | How | When |
|------|-----|------|
| **Route guard** | Check `sessionStorageMenu` for matching `OptionUrl` | Applied to every protected route |
| **Button visibility** | `getProcess()` → check if `ProcessId` exists for current screen | Components with conditional actions |
| **Endpoint resolution** | `getServicePath(serviceCode)` → resolve from menu `Service[]` | API calls from components |
| **Profile switching** | `setProfileByCode(profileId)` → reload menu | If app has multiple profiles per user |

### Key Session Storage Keys

| Key | Content |
|-----|---------|
| `sessionStorageMenu` | Menu tree with Options, Processes, Services |
| `sessionStorageProfile` | Current profile ID |
| `sessionStorageRole` | Available profiles for switching |

### Permission Check Pattern

```typescript
// Get processes for current screen
const processes = storageCredentials.getProcess(); // reads sessionStorageMenu

// Check action availability
const canCreate = processes.some(p => p.ProcessId === 'btnNew');
const canExport = processes.some(p => p.ProcessId === 'btnExportExcel');
```

> For full component patterns, see `react` skill. For AuthGuard implementation, see `happy` skill.

---

## [Construction] Backend Integration Hooks

These apply when building backend APIs. The `dotnet-api` skill handles endpoint patterns — this section covers only Lion-specific items.

### ProfileCodes Constants

Define in each domain API that needs role-conditional logic:

```csharp
public static class ProfileCodes
{
    public const string User = "200-XXX-USER";
    public const string Admin = "200-XXX-ADMIN";
    // Pattern: {app_code}-{PROFILE_CODE}
}
```

Codes MUST match the matrix's Profile table exactly.

### Authorization Enforcement

Authorization happens at the **API Gateway** via Happy (see `happy` skill). Backend APIs do NOT enforce permissions — they trust the gateway.

```
Frontend → Gateway (Happy validates Lion permissions) → Backend API (trusts gateway)
```

No `[Authorize]` attributes needed. If a handler needs role-conditional logic, use `headerToken.ProfileCode` — but prefer the Lion permission model over if/else role checks.

> For endpoint patterns and HeaderToken usage, see `dotnet-api` and `happy` skills.

---

## Checklist

### [Inception] Matrix
- [ ] All API spec endpoints mapped to screens
- [ ] Screen hierarchy defined (root → modules → sub-screens)
- [ ] Profiles defined with screen access
- [ ] Processes defined where action-level control needed
- [ ] Matrix saved to `aidlc-docs/authorization-matrix.md`
- [ ] Matrix reviewed by stakeholder

### [Inception] Lion Registration (if MCP available)
- [ ] Application created with correct code and architecture
- [ ] Options created parent-first
- [ ] Services registered per option with correct method codes
- [ ] Profiles created and assigned to options
- [ ] Processes assigned to profiles (if Level 2+)

### [Construction] Frontend
- [ ] Route guard checks menu for access
- [ ] `getProcess()` for button visibility
- [ ] Profile switching (if multi-profile)

### [Construction] Backend
- [ ] `ProfileCodes.cs` matches matrix exactly
- [ ] No `[Authorize]` attributes — gateway handles it

## Workflow Integration

| Phase | Stage | What happens |
|-------|-------|-------------|
| Inception | API Contract Design — Step 6b | Matrix generated from openapi.yaml + user stories |
| Inception | API Contract Design — Step 6b.8 | Optional Lion MCP registration |
| Construction | Code Generation (frontend) | AuthGuard, getProcess(), button visibility |
| Construction | Code Generation (backend) | ProfileCodes.cs constants |

## Related Skills

| Task | Skill |
|------|-------|
| Authentication (login, tokens, HeaderToken) | `happy` |
| API endpoint patterns | `dotnet-api` |
| Gateway configuration | `dotnet-gateway` |
| API contract design | `api-first-spec` |
| React component patterns | `react` |
