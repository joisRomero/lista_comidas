# Skills Manifest — ANTA Stack

**Version**: 1.2 (v1.7.0 Core Library — Validators wired + Lion skill v2.0 + validate_cross_stage)
**Skills count**: 46
**Last updated**: 2026-05-09

---

## How to Use

1. The **Skill Resolver** loads this manifest automatically before each stage
2. For each stage, load the SKILL.md files listed in the Stage → Skills Map
3. Cross-cutting skills are injected conditionally based on HU/requirements
4. Auto-invoke (file extension → skill) remains as a safety net for file writes

**Load protocol**: Read the skill's `SKILL.md` file from `config/skills/{skill-id}/SKILL.md` BEFORE executing the stage or writing code.

---

## Stage → Skills Map

### INCEPTION Phase

| Stage | Skills | Purpose |
|-------|--------|---------|
| Workspace Detection | *(discovers and registers all skills)* | Scan `skills/` directory, record in aidlc-state.md |
| Reverse Engineering | `anta-architecture` | Understand existing architecture patterns |
| Requirements Analysis | `repo-structure`, `database-modeling`, `database`, `database-audit`, `dotnet-shared-libs` | Data model conventions, repo codification, real package names |
| User Stories | `hu-template` | HU template format and fields |
| ISO 27001 Assessment | `security-baseline` · `security` | Pre-established security controls |
| Spike/POC | *(contextual — resolve by topic)* | — |
| API Contract Design | `api-first-spec`, `database-modeling`, `database-security`, `database-audit`, `dotnet-api` | ANTA patterns for openapi.yaml generation |
| Architecture Decision Records | `anta-architecture` | Architecture options and tradeoffs |
| Workflow Planning | — | No skills needed (meta-planning) |
| Application Design | `anta-architecture` · `design-system` | Component and service design |
| QA Matrix | `api-first-testing` · `playwright` | Test scenarios and test data catalog |
| Units Generation | — | No skills needed (decomposition) |
| Definition of Ready | — | Validation gate, no skills needed |

### CONSTRUCTION Phase — Per-Layer Profiles

Construction Code Generation subdivides into **3 layers + scaffolding**. Each layer has its own Code Gen → Review → QA cycle.

#### Layer: BD (Database)

| Type | Skills |
|------|--------|
| **Code** | `database` · `database-sp` · `database-modeling` · `database-audit` · `database-security` |
| **Validators** | `validate_sp` · `validate_db_schema` · `validate_audit_columns` |
| **QA Profile** | `conventions-lint` — validate naming, audit columns, RecordStatus, QUOTENAME, error codes, SQL syntax |

#### Layer: Backend (.NET)

| Type | Skills |
|------|--------|
| **Code** | `dotnet-api` · `dotnet-handler` · `dotnet-integration` · `dotnet-startup` · `dotnet-shared-libs` · `error-handling` |
| **Scaffolding** | `docker-local` · `dotnet-gateway` |
| **Validators** | `validate_dotnet_handler` · `validate_dotnet_project` · `validate_dotnet_deps` · `validate_docker` |
| **QA Profile** | `build-unit` — `dotnet build`, unit tests, validate endpoints vs openapi.yaml |
| **QA Skills** | `test-standards` · `api-first-testing` |

#### Layer: Frontend (React)

| Type | Skills |
|------|--------|
| **Code** | `react` · `react-hooks` · `design-system` · `microfrontend` · `typescript` |
| **Validators** | `validate_react_feature` · `validate_react_shared` · `validate_no_any` |
| **QA Profile** | `build-component` — `tsc --noEmit`, `rsbuild build`, React Testing Library |
| **QA Skills** | `test-standards` · `playwright` |

#### E2E (Global — after all layers)

| Type | Skills |
|------|--------|
| **Code** | `playwright` · `api-first-testing` |
| **QA Profile** | Integration Tests — Playwright full-stack (API + UI) |

### CONSTRUCTION Phase — Other Stages

| Stage | Skills |
|-------|--------|
| Prototyping | `html-prototype` |
| Dependency Review | `dotnet-shared-libs` |
| HU Guide Generation | Resolved per repo role (see table below) |

#### HU Guide Generation — Skills by Repo Role

When generating HU Guides for multi-repo projects, load skills based on the TARGET REPO's role:

| Repo Role | Skills to Load | Why |
|-----------|---------------|-----|
| **Gateway** (ApiGateway) | `dotnet-gateway` · `dotnet-api` · `happy` | Gateway routes, Ocelot config, header validation, Happy auth |
| **Backend Domain** (ApiInterna-*) | `dotnet-startup` · `dotnet-api` · `dotnet-handler` · `dotnet-integration` · `dotnet-shared-libs` · `database` · `database-sp` · `database-modeling` · `database-audit` · `database-security` · `error-handling` | Full backend stack: scaffolding files, endpoints, handlers, DB |
| **Frontend Host** (Front-Layout) | `microfrontend` · `react` · `react-hooks` · `design-system` · `typescript` | Host app setup, routing, shared components |
| **Frontend Domain** (Front-*) | `microfrontend` · `react` · `react-hooks` · `design-system` · `typescript` | Child microfrontend: shared/components copy checklist (11 Anta* wrappers from design-system skill), hooks, pages |

**Cross-cutting skills** are injected per HU requirements (same rules as Code Generation — see Cross-Cutting Skills table).

**The HU Guide MUST include** the resolved skill conventions as a "Project Standards" section so the receiving repo agent has complete context without needing the manifest.

### OPERATIONS Phase

| Stage | Skills |
|-------|--------|
| Release Documentation | `changelog` · `readme` |
| Operations | — (placeholder) |

### CLOSURE Phase

| Stage | Skills |
|-------|--------|
| Project Snapshot | — |
| Version & Archive | `changelog` |
| Stakeholder Sign-off | — |
| Project Handoff | *(aggregates Skill Health Report from skill-feedback data)* |

### CHANGE MANAGEMENT Phase

| Stage | Skills |
|-------|--------|
| Re-Onboarding | — |
| Change Request | — |
| Impact Analysis | `anta-architecture` |

---

## Cross-Cutting Skills (Conditional Injection)

These skills are injected into the layers that need them, determined by HU/requirements context:

| Skill | Condition | Injected Into |
|-------|-----------|---------------|
| `happy` | HU requires authentication | Backend + Frontend |
| `lion` | HU requires roles/permissions | Backend + Frontend |
| `arroba` | HU requires notifications | Backend |
| `export-excel` | HU requires Excel export | BD + Backend + Frontend |
| `security` | Always in Backend; conditional in Frontend | Backend (+ Frontend) |
| `performance` | HU with high data volume | BD + Backend |

---

## Construction Execution Model

```
Phase 1:  BD → Code Gen → Review → Conventions Lint
              |
              +-- pass → continue
              +-- FAIL → notify all, STOP
              |
Phase 2:  Backend → Code Gen → Review → Build+Tests  --+
          Frontend → Code Gen → Review → Build+Tests --+ PARALLEL
              |                                          (both from openapi.yaml)
              +-- both pass → continue
              +-- one fails → fix in its layer
              |
Phase 3:  E2E global (Build & Test stage)
```

**Prerequisite for Phase 2**: openapi.yaml must pass Spec Validation Gate — including `validate_openapi` deterministic check (see skill-resolver.md).

**Core Library Validators** (v1.7.0): Each layer runs deterministic validators from `config/validators/` after Code Generation and before Code Review. Validators are mapped to skills via `validates_with` in YAML frontmatter. See skill-resolver.md → Post-Generation Validation for the full protocol.

---

## Skill Inventory by Domain (46 skills)

### Database (5)

| Skill ID | Description |
|----------|-------------|
| `database` | SQL Server naming, schemas, conventions, error codes, pagination |
| `database-sp` | Stored procedure CRUD patterns, transactions, pagination SP |
| `database-modeling` | Table design, CREATE/ALTER TABLE, constraints, indexes, data types |
| `database-audit` | Audit columns, RecordStatus CHAR(1), soft delete, Log schema, GetErrorInfo |
| `database-security` | SQL injection prevention, QUOTENAME, IsReservedWord, error code catalog |

### Backend .NET (7)

| Skill ID | Description |
|----------|-------------|
| `dotnet-api` | Minimal API endpoints, requests, responses, ApiResponse wrapper |
| `dotnet-handler` | Handler pattern, Dapper SP calls, SpResultHelper, DictionaryMappingHelper |
| `dotnet-integration` | FluentValidation, SP error handling, error codes mapping |
| `dotnet-startup` | Program.cs, module registration, middleware configuration |
| `dotnet-gateway` | API Gateway, Ocelot config, header validation, DelegatingHandlers |
| `dotnet-shared-libs` | ANTA.Shared.* library configuration and middleware order |
| `error-handling` | Exception handling patterns, error propagation, logging |

### Frontend React (5)

| Skill ID | Description |
|----------|-------------|
| `react` | React features, components, types, project structure, Anta* wrappers |
| `react-hooks` | TanStack Query hooks, useHostServiceQuery/Mutation adapters, state management |
| `design-system` | Ant Design styling, Anta* wrapper components, CSS modules |
| `microfrontend` | Microfrontend setup, rsbuild config, Host exports, child app structure |
| `typescript` | TypeScript types, interfaces, strict mode conventions |

### API First (4)

| Skill ID | Description |
|----------|-------------|
| `api-first-spec` | API specification document format (9 sections: Scope→Error Codes) |
| `api-first-backend` | Generate backend code from OpenAPI spec: SP → Handler → Endpoint |
| `api-first-frontend` | Generate frontend code from OpenAPI spec: types → hooks → pages |
| `api-first-testing` | Generate E2E tests from OpenAPI spec: scenarios → Page Objects → tests |

### Architecture (2)

| Skill ID | Description |
|----------|-------------|
| `anta-architecture` | ANTA system architecture, repo structure, module patterns |
| `project-bootstrap` | New project setup, first-time configuration |

### Internal Libraries (3)

| Skill ID | Description |
|----------|-------------|
| `happy` | Authentication — JWT, tokens, login flow |
| `lion` | Authorization — roles, permissions, access control |
| `arroba` | Notifications — email, push, in-app notifications |

### Cross-Cutting (3)

| Skill ID | Description |
|----------|-------------|
| `security` | Security validation, SQL injection prevention, XSS, CORS |
| `performance` | Pagination, caching, query optimization, load patterns |
| `export-excel` | Excel export: SP @ParamIIsExport → ClosedXML handler → useExport hook |

### DevOps & Quality (7)

| Skill ID | Description |
|----------|-------------|
| `docker-local` | Dockerfile_local, docker-compose.yml, docker-compose.proxy.yml |
| `playwright` | Playwright E2E test patterns, page objects, assertions |
| `code-review` | Code review checklist, conventions verification |
| `judgment-day` | Adversarial QA — 2 blind judges, verdict synthesis, fix loop (high-risk changes only) |
| `pull-request` | PR creation, description format, review process |
| `changelog` | CHANGELOG.md entry format, conventional commit mapping |
| `swagger` | Swagger/OpenAPI documentation generation |
| `readme` | README.md template and structure |

### Documentation (2)

| Skill ID | Description |
|----------|-------------|
| `hu-template` | User Story template format, fields, numbering |
| `repo-structure` | Repository codification convention, project type inference |

### API Catalog (1)

| Skill ID | Description |
|----------|-------------|
| `api-catalog` | API inventory, service catalog, endpoint summary |

### Prototyping (1)

| Skill ID | Description |
|----------|-------------|
| `html-prototype` | Static HTML mockups with ANTA design system CSS for stakeholder visual approval |

### Meta (2)

| Skill ID | Description |
|----------|-------------|
| `skill-creator` | Skill creation guidelines and template structure |
| `skill-sync` | Skill synchronization between Framework-IA and Atlas |

---

## Compact Rules (Pre-Digested — for Sub-Agent Injection)

**Purpose**: When delegating work (to sub-agents or between stages), inject these compact rules DIRECTLY into the prompt as `## Project Standards (auto-resolved)`. Sub-agents do NOT need to read the full SKILL.md — these 5-15 line summaries contain the EXACT identifiers they must use.

**Inspired by**: [gentle-ai](https://github.com/Gentleman-Programming/gentle-ai) `_shared/skill-resolver.md` — compact rules pattern.

### database-audit
- 5 mandatory audit columns on ALL transactional tables: `RecordCreationUser VARCHAR(50)`, `RecordCreationDate DATETIMEOFFSET(7)`, `RecordEditUser VARCHAR(50)`, `RecordEditDate DATETIMEOFFSET(7)`, `RecordStatus CHAR(1) DEFAULT 'A'`
- RecordStatus values: `'A'` = Active, `'I'` = Inactive, `'*'` = Deleted. NEVER use INT, NEVER use 0/1
- Soft delete: `SET RecordStatus = '*'` — NEVER physical DELETE
- ALWAYS filter `RecordStatus = 'A'` in JOINs and WHERE clauses
- SP params: `@ParamIRecordCreationUser` for CREATE, `@ParamIRecordEditUser` for UPDATE/DELETE
- Check constraint: `CK_{Schema}_{Table}_RecordStatus CHECK (RecordStatus IN ('A', 'I', '*'))`
- Error capture: `Log.GetErrorInfo` in every SP CATCH block

### database-modeling
- Tables: singular UpperCamelCase (e.g., `Employee`, NOT `Employees`)
- PK: `{TableName}Id INT IDENTITY(1,1)` with DESC ordering
- FK: `{ReferencedTable}Id` — same type as referenced PK
- Booleans: `BIT NOT NULL DEFAULT 0` — NEVER nullable
- Dates: `DATETIMEOFFSET(7)` — NEVER `DATETIME` or `DATE` for timestamps
- Schema: use the name the USER chose — NEVER abbreviate or invent alternatives
- Database name: `{Env}_{Name}` UpperCamelCase (e.g., `Dev_RRHH`)

### database-security
- Error codes: `VAL_xxx` (validation), `BUS_xxx` (business rule) — NEVER generic `ERR_001`
- Dynamic identifiers: ALWAYS wrap with `QUOTENAME()` — prevents SQL injection
- Reserved words: check with `IsReservedWord()` before using as identifiers
- Input validation: validate ALL SP parameters before processing

### database-sp
- SP naming: `{Schema}.{Action}{Entity}` (e.g., `Emp.ListEmployee`, `Emp.CreateEmployee`)
- Actions: `List`, `Get`, `Create`, `Update`, `Delete`, `Search`
- Pagination SP: `@ParamIPage INT`, `@ParamIPageSize INT`, `@ParamISearch NVARCHAR(200)`, `@ParamISortBy NVARCHAR(100)`, `@ParamISortOrder NVARCHAR(4)`
- All SPs use TRY/CATCH with `Log.GetErrorInfo`
- Return error codes via `SELECT @ErrorCode AS ErrorCode` — NEVER RAISERROR for business errors

### database
- Schema naming: short, domain-meaningful (2-4 chars): `Emp`, `HR`, `Cases`, `Cnfg`
- Standard schemas: `Log` (logging), `Sec` (security), `Cnfg` (catalogs), `Core` (transactional), `Mstr` (masters)
- Collation: `SQL_Latin1_General_CP1_CI_AS`
- No `SELECT *` — ALWAYS list columns explicitly
- Use `WITH(NOLOCK)` on SELECT queries

### dotnet-api
- **Base path**: `/api/v1/{module}` — ALL endpoints live under this versioned prefix (e.g., `/api/v1/cases`, `/api/v1/employees`)
- Module registration: `app.MapGroup("/api/v1/{module}")` in `{Module}Module.cs`
- Response wrapper: `ApiResponse<T>` with properties `success`, `data`, `errors`, `metadata`
- Pagination params: `Page`, `PageSize`, `Search`, `SortBy`, `SortOrder` (exact names)
- GET list response: `ApiResponse<ListData<T>>` with `data.items[]` + `pagination`
- GET single: `ApiResponse<ItemData<T>>` with `data.item{}`
- POST create: returns `201 Created` with `ApiResponse<ItemData<T>>`
- DELETE: `ApiResponse<ResultData>` with `data.result{}`
- Endpoint pattern: `{Action}{Entity}Endpoint.cs` with static `Map(IEndpointRouteBuilder app)`

### happy
- Auth field for audit: `headerToken.EmployeeId` — NEVER `UserCode`, `UserId`, or `UserName`
- Internal APIs: `[FromServices] HeaderToken headerToken` — injected by `AddHeaderToken()` middleware
- Gateway: `UseValidationHeader()` before `UseOcelot()`
- Security schemes in OpenAPI: TWO apiKey schemes named `code` and `header` (matches `AddSwaggerWithHappyAuth`) — NEVER `BearerAuth` or single `HappyAuth`
- Frontend sends TWO headers: `code` + `header` (Happy-encrypted) — NOT Bearer token
- Excluded paths (no auth): `/health`, `/swagger`, static files

### repo-structure
- Project code format: numeric with dash (e.g., `200-034`) — NEVER generic IDs like `R1`, `repo-001`, `TBD`
- Repo naming: `{PROJECT_CODE}{SUFFIX}` — purely numeric, no module names embedded
- Fixed suffixes: `97` = Doc Hub, `40` = Core API, `45` = Gateway, `90` = Frontend Host, `51` = Mobile
- Decremental suffixes: `39/89` (first module), `38/88` (second), `37/87` (third) — API/Frontend pairs
- ALWAYS ask project code question during Requirements Analysis

---

## File Extension → Skill (Quick Reference)

Safety net for file writes — the Skill Resolver is the primary loading mechanism.

| File Pattern | Skills |
|-------------|--------|
| `*.sql` | `database-sp` + `database` + `database-modeling` + `database-audit` + `database-security` |
| `*Endpoint.cs` | `dotnet-api` |
| `*Handler.cs` | `dotnet-handler` |
| `*Validator.cs` | `dotnet-integration` |
| `Program.cs` / `*Module.cs` | `dotnet-startup` |
| `*Gateway*` / `configuration.json` | `dotnet-gateway` |
| `*.tsx` / `*.ts` (features/) | `react` |
| `use*Query.ts` / `use*Mutation.ts` | `react-hooks` |
| `rsbuild.config.ts` | `microfrontend` |
| `*.module.css` | `design-system` |
| `Dockerfile*` / `docker-compose*` | `docker-local` |
| `openapi.yaml` | `api-first-spec` |
| `*.spec.ts` / `*.e2e.ts` | `playwright` + `api-first-testing` |
