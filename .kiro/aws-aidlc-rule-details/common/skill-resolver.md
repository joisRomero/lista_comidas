# Skill Resolver Protocol

**Purpose**: Resolve and load the correct organizational skills before every stage execution and sub-agent delegation. The Skill Resolver is the **single mechanism** for skill loading — replaces all inline skill references in the orchestrator.

## When to Apply

1. **Before EVERY stage execution** — resolve skills for the current stage
2. **Before EVERY sub-agent delegation** — inject Project Standards into sub-agent prompt
3. **Before EVERY file write** — safety net via file extension mapping (complements auto-invoke)

---

## Resolution Flow

### Step 1: Stage Resolution (Before Each Stage)

```
1. Read current stage from aidlc-state.md
2. Look up stage in SKILLS-MANIFEST.md → Stage → Skills Map
3. Load each listed SKILL.md file from config/skills/{skill-id}/
4. If in Construction Code Generation:
   → Also resolve per-layer profile (see Step 2)
5. Check cross-cutting table:
   → Does the current HU/requirements trigger any cross-cutting skill?
   → If yes, load those too
6. Apply enforcement levels:
   → mandatory = auto-apply as HARD CONSTRAINT, inform user
   → optional = ask user for confirmation
```

### Step 2: Per-Layer Resolution (Construction Code Generation Only)

When executing Code Generation, resolve skills per layer:

```
1. Read Code Gen Plan (universal input) or HU Guide (multi-repo)
2. Identify which layers apply for this unit:
   - BD: always (if any database work)
   - Backend: always (if any .NET API work)
   - Frontend: always (if any React work)
   - Gateway/Docker: scaffolding — included in Backend layer
3. For each layer: resolve code skills + QA skills from SKILLS-MANIFEST.md layer profile
4. Resolve cross-cutting skills from HU/requirements context
5. Execute layers in dependency order (see Construction Execution Model)
```

### Step 3: Sub-Agent Injection (Before Delegation)

When delegating work to a sub-agent (Code Gen sub-agent, Code Review, Judgment Day):

```
1. Identify what the sub-agent will work on (files, scope, layer)
2. Resolve skills for that scope using SKILLS-MANIFEST.md
3. Extract compact rules from each skill:
   - Checklist items
   - Key conventions (naming, patterns, constraints)
   - Anti-patterns (what NOT to do)
4. Build a "Project Standards" block (see template below)
5. Inject into sub-agent prompt as HARD CONSTRAINTS
```

#### Project Standards Block Template

**CRITICAL**: Use the **Compact Rules** section from `skills/SKILLS-MANIFEST.md` as the primary source for the Project Standards block. Compact rules are pre-digested 5-15 line summaries with EXACT identifiers — they prevent paraphrasing. Do NOT summarize or rephrase compact rules — copy them verbatim.

```markdown
## Project Standards (auto-resolved from Compact Rules)

### {skill-name-1}
{Copy compact rules block verbatim from SKILLS-MANIFEST.md}

### {skill-name-2}
{Copy compact rules block verbatim from SKILLS-MANIFEST.md}

### Checklist
{Combined checklist from loaded skills for this layer}
```

**Why compact rules over full SKILL.md**: Full skills (200+ lines) cause agents to "understand conceptually" and then paraphrase identifiers. Compact rules (5-15 lines) contain only the actionable literals — much harder to paraphrase.

---

## Construction Execution Model

### Dependency Chain

```
Phase 1:  BD layer
          └── Code Gen → Review → Conventions Lint
              |
              +-- PASS → continue to Phase 2
              +-- FAIL → notify all layers, report findings, STOP
                         (do NOT proceed with Backend/Frontend on broken BD)

Phase 2:  Backend layer + Frontend layer (PARALLEL)
          ├── Backend → Code Gen → Review → Build + Unit Tests
          └── Frontend → Code Gen → Review → Build + Component Tests
              |
              Both work from the VALIDATED openapi.yaml (API contract)
              They do NOT depend on each other
              |
              +-- Both PASS → continue to Phase 3
              +-- One FAILS → fix in its layer, does NOT block the other
              +-- Both FAIL → fix independently, then continue

Phase 3:  E2E global
          └── Playwright full-stack tests (API + UI)
              Requires ALL layers completed
```

### QA Profiles by Layer

Each layer has a specific QA definition — QA is NOT generic:

| Layer | QA Profile | What It Does | What It Does NOT Do |
|-------|-----------|-------------|-------------------|
| **BD** | Conventions Lint | Validate naming, audit columns, RecordStatus, QUOTENAME, error codes against skill rules. Validate SQL syntax. | Does NOT execute SPs (no DB available at this point) |
| **Backend** | Build + Unit Tests | `dotnet build` + unit tests + validate endpoints match openapi.yaml | Does NOT run integration tests (needs real DB) |
| **Frontend** | Build + Component Tests | `tsc --noEmit` + `rsbuild build` + component tests with React Testing Library | Does NOT run E2E (needs real backend) |
| **E2E** | Integration global | Playwright full-stack against running app. API tests + UI tests. | Final stage — everything is available |

### Gateway and Docker

Gateway (Ocelot config) and Docker (Dockerfile + compose) are **scaffolding** — generated as part of Backend Code Gen. They do NOT get their own Code Gen → Review → QA cycle.

---

## Spec Validation Gate

**When**: After Phase 1 (BD), before Phase 2 (Backend + Frontend parallel).
**Why**: Backend and Frontend both work from the openapi.yaml. If the spec is incomplete, parallel work produces mismatched code.

### Validation Checklist

| Check | Verifies | Fails If |
|-------|----------|----------|
| API versioning | `servers` has `/api/v1/{module}` base path, `info.version` set | Missing version prefix or unversioned paths |
| Schemas complete | All properties defined with type + example | Any schema is just `type: object` without properties |
| Response shapes | All responses use ApiResponse pattern | Response missing `success`/`data`/`errors` structure |
| ErrorResponse separate | Error responses (4xx, 5xx) use dedicated ErrorResponse schema | Same ApiResponse used for both success and error (no pagination/data in errors) |
| ErrorItem complete | ErrorItem has code (VAL_xxx/BUS_xxx), field, message | Missing fields or no error code pattern |
| 500 response universal | Every endpoint defines 500 with ErrorResponse | Any endpoint missing 500 response |
| Pagination | GET list endpoints have 5 query params | Missing Page/PageSize/Search/SortBy/SortOrder |
| Operations | Each operation documents state flow | `POST /{id}/{verb}` without state description |
| Auth (Happy) | Two apiKey schemes named `code` and `header` (matches `AddSwaggerWithHappyAuth`) | Using BearerAuth, single `HappyAuth` scheme, or custom names |
| Happy dual headers | Both `code` and `header` custom headers documented | Missing either header |
| No BearerAuth | Spec does not use Bearer/BearerAuth | BearerAuth found in securitySchemes |
| POST create at root | Create endpoints use `POST /` not `POST /create` | Sub-route pattern for create operations |
| Examples | At least one example per endpoint | Endpoint without request/response examples |

### On Failure

1. Agent identifies which checks failed
2. Agent corrects the openapi.yaml
3. Re-validates
4. Phase 2 is BLOCKED until all checks pass

---

## Cross-Cutting Skill Resolution

Cross-cutting skills are NOT loaded by default — they are injected based on HU/requirements context:

```
1. Read HU/requirements for the current unit
2. Check each cross-cutting condition:
   - Auth mentioned? → load `happy` into Backend + Frontend
   - Roles/permissions mentioned? → load `lion` into Backend + Frontend
   - Notifications mentioned? → load `arroba` into Backend
   - Excel export mentioned? → load `export-excel` into BD + Backend + Frontend
   - High data volume? → load `performance` into BD + Backend
3. `security` is ALWAYS loaded into Backend
   - Load into Frontend only if frontend security patterns apply
```

---

## Input Sources

The Skill Resolver uses different inputs depending on the context:

| Context | Primary Input | What It Provides |
|---------|--------------|-----------------|
| INCEPTION stages | aidlc-state.md + Requirements | Current stage, discovered skills |
| Construction (single-repo) | Code Gen Plan | Files to generate → infer layers |
| Construction (multi-repo) | HU Guide + Code Gen Plan | Scope per repo + files → infer layers |
| Sub-agent delegation | Layer scope + file list | What the sub-agent will work on |

---

## Graceful Degradation

| Scenario | Behavior |
|----------|----------|
| No SKILLS-MANIFEST.md found | Warn: "No skills manifest found." Fall back to auto-invoke file extension mapping |
| No skills directory found | Warn: "No organizational skills directory found." Continue with standard AI-DLC behavior |
| Skill referenced in manifest but SKILL.md missing | Warn: "Skill {id} not found." Skip and continue |
| No HU/requirements for cross-cutting resolution | Skip cross-cutting injection, proceed with base layer skills only |
| Sub-agent delegation without manifest | Warn: "Sub-agent will work without project standards." Proceed with generic review only |

---

## Precedence Rules

1. **User runtime declarations** override skill content — even mandatory skills
2. **Organizational Standards** (Requirements Analysis Step 5) override conflicting skill content
3. **Spec Validation Gate** blocks Construction Phase 2 — no override
4. **Mandatory skills** are auto-applied — user is informed, not asked
5. **Optional skills** provide defaults — user confirms before applying
6. **Cross-cutting skills** are additive — they complement layer skills, never replace them

---

## Post-Generation Validation (Core Library v1.7.0)

After Code Generation completes for a layer, the Skill Resolver runs validators declared in each skill's YAML frontmatter.

### Resolution Flow

```
1. For each active skill in the current layer:
   a. Read `validates_with` from skill's YAML frontmatter
   b. If `validates_with` is null → skip (methodological skill, no code to validate)
   c. If validator exists in config/validators/ → queue for execution
   d. If validator file missing → warn and skip (graceful degradation)

2. Deduplication:
   - Multiple skills may reference the SAME validator
     (e.g., database-sp and database-security both use validate_sp)
   - The Resolver collects UNIQUE validators for the layer
   - Each validator runs ONCE per file, not once per skill

3. Execution:
   - Run collected validators against generated files for this layer
   - Use runner.py --profile {profile} for batch execution:
     * BD layer → conventions-lint profile
     * Backend layer → build-unit profile
     * Frontend layer → build-component profile

4. Fix Loop:
   a. Present errors to agent with file, line, rule, suggestion
   b. Agent fixes each error based on CONCRETE validator output
   c. Re-run ONLY the affected validators (not all)
   d. Max 3 iterations per layer
   e. If errors persist after 3 attempts → log in audit.md, escalate to Code Review

5. Gate:
   - Layer proceeds to next step ONLY when all validators pass
     (or max iterations reached with escalation logged)
   - Validator WARNINGS do not block — they are noted for Code Review
```

### Validation Profiles (mapped to QA Profiles)

| Layer | Validator Profile | Validators |
|-------|------------------|------------|
| **BD** | `conventions-lint` | `validate_sp`, `validate_db_schema`, `validate_audit_columns` |
| **Backend** | `build-unit` | `validate_dotnet_handler`, `validate_dotnet_project`, `validate_dotnet_deps` |
| **Frontend** | `build-component` | `validate_react_feature`, `validate_react_shared`, `validate_no_any` |
| **Structure** | `structure` | `validate_repo_structure`, `validate_docker` |
| **Cross-cutting** | `cross-cutting` | `validate_auth_pattern` |
| **Spec** | `spec-gate` | `validate_openapi` |

### Integration Points

Validators are wired into the workflow at 4 points (see each file for full protocol):

1. **Inception → API Contract Design** (Step 8): `validate_openapi` runs as the first check of the Spec Validation Gate
2. **Construction → Code Generation** (Step 13): Per-layer validators run after generating code for each layer
3. **Construction → Code Review** (Step 3b): `runner.py --all --report` generates a Validator Report injected into reviewer context
4. **Construction → Build & Test** (Step 7b): `validate_repo_structure`, `validate_docker`, `validate_auth_pattern` run as final structural catch

---

## Key Principles

- **Single mechanism**: The Skill Resolver is the ONLY way skills are loaded. No inline hardcoded skill references in the orchestrator
- **Stage-aware**: Each stage gets exactly the skills it needs — no more, no less
- **Layer-aware**: Construction resolves skills per layer, not monolithically
- **Fail-fast**: BD failure stops everything. Spec validation gates Phase 2
- **Parallel-ready**: Backend and Frontend layers can execute simultaneously from validated spec
- **Graceful degradation**: Missing skills or manifest = warn and continue, never crash
- **Additive only**: Skills complement the workflow, never skip stages or bypass gates
- **LITERAL COMPLIANCE (CRITICAL)**: When a skill defines specific names, types, values, or patterns — use them **VERBATIM** in all generated output. Do NOT rename, abbreviate, paraphrase, or substitute with generic equivalents. This applies to column names, type definitions, error codes, response shapes, file names, parameter names, and any other concrete value the skill prescribes.

---

## Literal Compliance Rule (MANDATORY)

**Problem this solves**: Agents load skills, announce they're applying them, but then generate output using generic/paraphrased names instead of the exact values the skill defines. This causes cascading failures — wrong names in Requirements propagate to API Contract → Backend → Frontend.

**Rule**: When generating ANY artifact (requirements, openapi.yaml, code, SQL, documentation) that references a concept defined by a loaded skill:

1. **COPY the exact identifier** from the skill — do not invent synonyms
2. **COPY the exact type** from the skill — do not simplify or generalize
3. **COPY the exact values/enums** from the skill — do not substitute

**Examples of violations (NEVER DO THIS)**:

| Skill Defines | Agent Writes (WRONG) | Why It's Wrong |
|---------------|---------------------|----------------|
| `RecordCreationUser VARCHAR(50)` | `CreatedBy` | Paraphrased column name |
| `RecordCreationDate DATETIMEOFFSET(7)` | `CreatedAt DATETIME` | Renamed + wrong type |
| `RecordStatus CHAR(1) DEFAULT 'A'` | `RecordStatus INT DEFAULT 1` | Wrong type + wrong values |
| `RecordStatus = '*'` (deleted) | `RecordStatus = 0` | Wrong value |
| `headerToken.{EntityId}` | `headerToken.UserCode` | Wrong property name |
| `ApiResponse<T>` with `success/data/errors` | `{ status, result }` | Wrong response shape |

**Self-check before generating**: For each table, endpoint, schema, or component — ask: "Does a loaded skill define the exact names/types for this? If yes, am I using those EXACT names/types?" If not, correct before outputting.

---

## Skill Compliance Gate (Reusable — referenced by multiple stages)

**When to run**: AFTER generating any artifact that references skill-defined identifiers, BEFORE presenting for user approval.

**Protocol**:
1. Open `skills/SKILLS-MANIFEST.md` → **Compact Rules** section
2. For each skill with compact rules that was loaded for the current stage, read its compact rules block
3. Scan the generated artifact for any reference to concepts defined in those compact rules
4. Verify the artifact uses the **EXACT identifier** from the compact rules — not a synonym or paraphrase
5. **If mismatch found**: Correct inline. Do NOT present the artifact with mismatched identifiers.

**Why compact rules make this easier**: Each compact rules block is 5-15 lines with ONLY the literals. Scanning 50 lines of compact rules is faster and more reliable than scanning 1000+ lines across multiple SKILL.md files.

**Common failure patterns to check**:

| Domain | Skill Says | Agent Often Writes (WRONG) |
|--------|-----------|---------------------------|
| Audit columns | `RecordCreationUser` | `CreatedBy`, `CreatedUser`, `CreateUser` |
| Audit columns | `RecordCreationDate` | `CreatedAt`, `CreatedDate`, `CreateDate` |
| Audit columns | `RecordEditUser` | `UpdatedBy`, `ModifiedBy`, `LastModifiedUser` |
| Audit columns | `RecordEditDate` | `UpdatedAt`, `ModifiedAt`, `LastModifiedDate` |
| Soft delete | `RecordStatus CHAR(1) = '*'` | `IsDeleted BIT`, `RecordStatus = 0`, `Status = 'Deleted'` |
| Active filter | `RecordStatus = 'A'` | `RecordStatus = 1`, `IsActive = true` |
| Auth | `headerToken.{EntityId}` | `headerToken.UserCode`, `userId`, `currentUser` |
| Response | `ApiResponse<T>` with `success/data/errors` | `{ status, result }`, `{ ok, payload }` |
| Error codes | `VAL_xxx`, `BUS_xxx` | `ERR_001`, `VALIDATION_ERROR`, generic strings |

**This gate is NOT optional.** Stages that MUST run this gate:
- Requirements Analysis (Step 8b)
- API Contract Design (before Spec Validation Gate)
- Code Generation (before per-layer QA)
