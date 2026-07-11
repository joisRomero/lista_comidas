---
name: code-review
description: >
  ANTA-specific code review checklist with validator integration and Judgment Day trigger.
  Trigger: During Code Review stage, before creating PRs, or when asked to review code.
metadata:
  author: anta
  version: "2.0"
  scope: [root]
  auto_invoke: "code review, review, before commit, check code, PR ready"
  phase: [construction]
  layer: null
  validates_with: null
  validation_profile: null
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Run Core Library validators BEFORE manual review | ALWAYS | Deterministic checks catch convention violations that AI hallucinates as passing |
| MUST READ changed files — never review from memory | ALWAYS | v1.2.0 benchmark proved AI invents compliance when it doesn't read the actual code |
| Fix all CRITICAL/MAJOR before approval | ALWAYS | Don't merge broken code |
| Trigger Judgment Day for high-risk changes | CONDITIONAL | 2 blind judges catch what 1 reviewer misses (see `judgment-day` skill) |

---

## Step 1: Run Validators (Core Library)

**BEFORE** reading any code, run the deterministic validators:

```bash
# Full validation report
python config/validators/runner.py --all --report path/to/project/

# Or by profile
python config/validators/runner.py --profile conventions-lint path/to/database/
python config/validators/runner.py --profile build-unit path/to/backend/
python config/validators/runner.py --profile build-component path/to/frontend/
```

| Result | Action |
|--------|--------|
| ERRORS | **MUST fix** before continuing review — these are convention violations |
| WARNINGS | Note for reviewer — may be intentional |
| PASS | Proceed to manual review |

---

## Step 2: Risk Assessment (Judgment Day Trigger)

Evaluate if this unit needs adversarial review:

| Signal | Threshold |
|--------|-----------|
| Files changed | >10 files |
| Auth/security modules | Any file in auth, security, or authorization layers |
| New API write endpoints | POST/PUT/DELETE operations added |
| Database schema changes | New tables, column modifications |
| Multi-repo gateway changes | Ocelot routing, gateway config |
| Critical validator errors | ERRORS from Step 1 |

**IF any signal is TRUE** → Load `judgment-day` skill, execute full protocol (2 blind judges).

**IF no signal is TRUE** → Continue with standard review below.

---

## Step 3: Manual Review — ANTA Conventions

### Database (Stored Procedures)

| Check | ANTA Convention | Validator |
|-------|----------------|-----------|
| SP naming | `SP_{Entity}_{Action}` (e.g., `SP_Employee_Create`) | `validate_sp` |
| Schema | User's chosen schema, not abbreviated (e.g., `Training`, not `Trn`) | `validate_db_schema` |
| Audit columns | `RecordStatus`, `RecordCreationUser`, `RecordCreationDate`, `RecordEditUser`, `RecordEditDate` on ALL tables | `validate_audit_columns` |
| QUOTENAME | ALL dynamic SQL wrapped in `QUOTENAME()` — no exceptions | `validate_sp` |
| Error codes | `RAISERROR('VAL_001\|Message\|Field', 16, 1)` — pipe-delimited, typed codes | `validate_sp` |
| TRY/CATCH | Every SP with writes has `BEGIN TRY` / `BEGIN CATCH` with `ROLLBACK` | `validate_sp` |
| Pagination | List SPs have `@Page`, `@PageSize`, `@Search`, `@SortBy`, `@SortOrder` | `validate_sp` |
| RecordStatus filter | WHERE clauses include `RecordStatus = 'A'` (active only) | `validate_sp` |
| No `SELECT *` | Explicit column lists always | Manual |

### Backend (.NET Minimal API)

| Check | ANTA Convention | Validator |
|-------|----------------|-----------|
| Handler pattern | `[FromServices]` DI, NOT constructor injection | `validate_dotnet_handler` |
| Response wrapper | ALL responses use `ApiResponse<T>` — never raw types | `validate_dotnet_handler` |
| Validation | FluentValidation on ALL commands — `UseJsonValidation<T>()` | `validate_dotnet_handler` |
| Auth | `HeaderToken` via `[FromServices]` — NOT Bearer, NOT `[Authorize]` | `validate_auth_pattern` |
| SP calls | `Dapper` with `CommandType.StoredProcedure` — never raw SQL | Manual |
| Error mapping | `SpResultHelper` → `ApiResponse.Fail()` with error codes | Manual |
| Shared libs | `ANTA.Shared.*` packages from CodeArtifact — correct versions | `validate_dotnet_deps` |
| Project files | `.csproj`, `appsettings.json`, `nuget.config`, `launchSettings.json` present | `validate_dotnet_project` |
| Endpoint registration | Module pattern: `{Module}Endpoints.cs` + `{Module}Module.cs` | Manual |

### Frontend (React)

| Check | ANTA Convention | Validator |
|-------|----------------|-----------|
| No `: any` | Zero `any` types in TypeScript — use proper interfaces | `validate_no_any` |
| Feature structure | `Page.tsx` + `hooks/` + `components/` + `types/` per feature | `validate_react_feature` |
| Anta* wrappers | Use `AntaButton`, `AntaTable`, etc. — never raw Ant Design | `validate_react_shared` |
| Logic hooks | `use{Feature}Logic` pattern — pages only render, logic in hooks | Manual |
| CSS Modules | `*.module.css` per component — no inline styles, no Tailwind | Manual |
| Routing | `location.state` for entity IDs — NOT URL params | Manual |
| Barrel exports | `index.ts` per feature with named exports | `validate_react_feature` |
| Service IDs | Defined in `shared/utils/service-ids.ts` as enums | Manual |

### Docker

| Check | ANTA Convention | Validator |
|-------|----------------|-----------|
| Dockerfile_local | Multi-stage (SDK noble → aspnet noble), CodeArtifact auth, secure user, SERVICE_PORT | `validate_docker` |
| docker-compose.yml | `antamina-network` (external), `CODEARTIFACT_AUTH_TOKEN`, image tag `200-0{PORT}` | `validate_docker` |
| docker-compose.proxy.yml | SQL proxy with `alpine/socat`, bridge network | Manual |

### Auth Patterns

| Check | ANTA Convention | Validator |
|-------|----------------|-----------|
| Backend auth | `HeaderToken` from `[FromServices]` — NOT Bearer token | `validate_auth_pattern` |
| EmployeeId | Extracted from `HeaderToken`, not from request body | `validate_auth_pattern` |
| GET endpoints | Skip `HeaderToken` check (read-only, no auth mutation) | `validate_auth_pattern` |
| OpenAPI security | Two apiKey schemes: `code` + `header` (NOT `BearerAuth`) | `validate_openapi` |

---

## Step 4: Cross-Layer Checks

| Check | What to Verify |
|-------|---------------|
| API contract alignment | Endpoints match `openapi.yaml` — paths, methods, request/response shapes |
| SP ↔ Handler mapping | Every SP called from a handler exists and parameter names match |
| Frontend ↔ API alignment | Service IDs in frontend match actual endpoint IDs in Lion |
| Error code consistency | `VAL_xxx` / `BUS_xxx` codes match between SP RAISERROR and frontend error display |
| Repo structure | Files in correct repo (API code in ApiInterna-*, frontend in Front-*) |

---

## Step 5: Automated Checks

```bash
# Backend
dotnet build src/{Project}.Api/
dotnet test tests/{Project}.Api.Tests/

# Frontend
npm run build          # rsbuild build
npx vitest run         # unit tests (*.spec.ts)
npx tsc --noEmit       # type check

# Validators
python config/validators/runner.py --all --report .
```

---

## Finding Severity

| Severity | Criteria | Action |
|----------|----------|--------|
| **CRITICAL** | Security vulnerability, data loss risk, auth bypass, SP injection | MUST fix — blocks merge |
| **MAJOR** | Convention violation caught by validator, missing error handling, wrong auth pattern | MUST fix — blocks merge |
| **MINOR** | Naming inconsistency, missing comment, non-blocking style issue | Should fix — doesn't block |
| **SUGGESTION** | Alternative approach, performance optimization, readability improvement | Optional |

---

## Review Report Format

```markdown
# Code Review Report — {Unit Name}

## Validator Results
- Errors: {N} (MUST fix)
- Warnings: {N} (noted)

## Manual Review Findings

| # | File:Line | Issue | Severity | Convention | Fix |
|---|-----------|-------|----------|------------|-----|
| 1 | SP_Employee_Create.sql:18 | Missing QUOTENAME on @Column | CRITICAL | validate_sp | Wrap with QUOTENAME() |
| 2 | CreateEmployeeHandler.cs:25 | Constructor injection instead of [FromServices] | MAJOR | validate_dotnet_handler | Refactor to [FromServices] |
| 3 | EmployeesPage.tsx:42 | Uses raw Button instead of AntaButton | MAJOR | validate_react_shared | Replace with AntaButton |

## Summary
- Critical: {N}
- Major: {N}
- Minor: {N}
- Suggestions: {N}

## Judgment Day
{If triggered: see judgment-day-report.md | If not triggered: "Standard review — risk level LOW/MEDIUM"}
```

---

## Checklist

### Before Review
- [ ] Core Library validators executed (`runner.py --all --report`)
- [ ] Risk assessment done (Judgment Day trigger check)
- [ ] Changed files identified and READ (not reviewed from memory)

### During Review
- [ ] Database conventions verified (SP naming, audit columns, QUOTENAME, error codes)
- [ ] Backend conventions verified (handler pattern, ApiResponse, FluentValidation, auth)
- [ ] Frontend conventions verified (no any, feature structure, Anta* wrappers, logic hooks)
- [ ] Docker conventions verified (if Docker files changed)
- [ ] Cross-layer alignment checked (API contract, SP↔handler, frontend↔API)

### After Review
- [ ] All CRITICAL/MAJOR findings fixed
- [ ] Validator re-run passes (0 ERRORS)
- [ ] Review report generated
- [ ] If Judgment Day: verdict is APPROVED or ESCALATED

---

## Related Skills

| Task | Skill |
|------|-------|
| Adversarial QA (high-risk) | `judgment-day` |
| PR conventions | `pull-request` |
| Unit test conventions | `test-standards` |
| Error handling | `error-handling` |
| Security patterns | `security` |
| API spec compliance | `api-first-spec` |
