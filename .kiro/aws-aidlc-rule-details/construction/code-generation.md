# Code Generation - Detailed Steps

## Overview
This stage generates code for each unit of work through two integrated parts:
- **Part 1 - Planning**: Create detailed code generation plan with explicit steps
- **Part 2 - Generation**: Execute approved plan to generate code, tests, and artifacts

**Note**: For brownfield projects, "generate" means modify existing files when appropriate, not create duplicates.

## Prerequisites
- Unit Design Generation must be complete for the unit
- NFR Implementation (if executed) must be complete for the unit
- All unit design artifacts must be available
- Unit is ready for code generation

---

# PART 1: PLANNING

## Step 1: Analyze Unit Context
- [ ] Read unit design artifacts from Unit Design Generation
- [ ] Read unit story map to understand assigned stories
- [ ] Identify unit dependencies and interfaces
- [ ] Validate unit is ready for code generation

**Multi-Repo Mode**: For multi-repo projects, verify the HU Guide for this unit is available (distributed from the Documentation Hub). The guide contains the API subset, implementation checklist, and traceability links specific to this repository. See `construction/hu-guide-template.md`.

**Authorization Context**: If the project has an authorization matrix (`aidlc-docs/inception/authorization-matrix.md`), load the `lion` skill and identify which screens/processes this unit implements. This feeds:
- **Frontend**: AuthGuard route checks, `getProcess()` button visibility, `getServicePath()` endpoint resolution
- **Backend**: `ProfileCodes.cs` constants matching the matrix's Profile table

### SKILL CHECK: database / code-standards
**IF** `aidlc-state.md` → Organizational Skills section lists ANY skills related to database or code standards:
1. Load ALL relevant skill files. Match by ID or name pattern:
   - Database family: `db-standards`, `database`, `database-sp`, `database-audit`, `database-modeling`, `database-security`
   - API family: `api-standards`, `api-first-spec`, `api-first-backend`, `api-first-frontend`, `api-first-testing`
   - Code family: `code-standards`
   - Any other skill whose name or description relates to code generation conventions
2. **Separate skills by enforcement level** (read `enforcement` field from each skill's YAML frontmatter):
   - **Mandatory skills** (`enforcement: mandatory`): Auto-apply as HARD CONSTRAINTS without asking.
   - **Optional skills** (`enforcement: optional` or field absent): Ask user for confirmation.
3. **For mandatory skills** — inform the user (do NOT ask):
   > *"Applying mandatory organizational standards to code generation:*
   > *- [Skill ID]: [brief description]*
   > *- ...*
   > *These are fixed standards. You can override specific parts if needed."*
   Apply directly:
   - `db-standards` / `database`: Database naming conventions, schema patterns, access patterns
   - `database-sp`: Stored procedure templates, parameter conventions, error handling patterns
   - `database-audit`: Audit columns, RecordStatus soft delete, Log schema, GetErrorInfo
   - `database-modeling`: Table design, column types, constraints, indexes, CTEs, transactions
   - `database-security`: SQL injection prevention, error code catalog, input validations
   - `api-first-*`: API specification, backend/frontend generation, testing patterns
   - `code-standards`: Folder structure, naming conventions, architecture patterns, code organization
4. **For optional skills** — ask user: *"I also found optional skills: [list]. Should I apply these to code generation?"*
   - IF user confirms → Apply as constraints
   - IF user declines → Proceed without them
5. **Precedence**: Organizational Standards (HARD CONSTRAINTS from Step 5) override skill content if they conflict. User runtime overrides take precedence over everything.
**ELSE** (no skills available):
- Continue with standard behavior — use Organizational Standards from Requirements if available, otherwise make technology choices based on context

**See `common/organizational-skills.md` for the full skills system documentation (including enforcement levels).**

## Step 2: Create Detailed Unit Code Generation Plan
- [ ] Read workspace root and project type from `aidlc-docs/aidlc-state.md`
- [ ] Determine code location (see Critical Rules for structure patterns)
- [ ] **Brownfield only**: Review reverse engineering code-structure.md for existing files to modify
- [ ] Document exact paths (never aidlc-docs/)
- [ ] Create explicit steps for unit generation:
  - Project Structure Setup (greenfield only)
  - Business Logic Generation
  - Business Logic Unit Testing
  - Business Logic Summary
  - API Layer Generation
  - API Layer Unit Testing
  - API Layer Summary
  - Repository Layer Generation
  - Repository Layer Unit Testing
  - Repository Layer Summary
  - Frontend Components Generation (if applicable)
  - Frontend Components Unit Testing (if applicable)
  - Frontend Components Summary (if applicable)
  - Database Migration Scripts (if data models exist)
  - Documentation Generation (API docs, README updates)
  - Deployment Artifacts Generation
- [ ] Number each step sequentially
- [ ] Include story mapping references
- [ ] Add checkboxes [ ] for each step

## Step 3: Include Unit Generation Context
- [ ] For this unit, include:
  - Stories implemented by this unit
  - Dependencies on other units/services
  - Expected interfaces and contracts
  - Database entities owned by this unit
  - Service boundaries and responsibilities

## Step 4: Create Unit Plan Document
- [ ] Save complete plan as `aidlc-docs/construction/plans/{unit-name}-code-generation-plan.md`
- [ ] Include step numbering (Step 1, Step 2, etc.)
- [ ] Include unit context and dependencies
- [ ] Include story traceability
- [ ] Ensure plan is executable step-by-step
- [ ] Emphasize that this plan is the single source of truth for Code Generation

## Step 5: Summarize Unit Plan
- [ ] Provide summary of the unit code generation plan to the user
- [ ] Highlight unit generation approach
- [ ] Explain step sequence and story coverage
- [ ] Note total number of steps and estimated scope

## Step 6: Log Approval Prompt
- [ ] Before asking for approval, log the prompt with timestamp in `aidlc-docs/audit.md`
- [ ] Include reference to the complete unit code generation plan
- [ ] Use ISO 8601 timestamp format

## Step 7: Wait for Explicit Approval
- [ ] Do not proceed until the user explicitly approves the unit code generation plan
- [ ] Approval must cover the entire plan and generation sequence
- [ ] If user requests changes, update the plan and repeat approval process

## Step 8: Record Approval Response
- [ ] Log the user's approval response with timestamp in `aidlc-docs/audit.md`
- [ ] Include the exact user response text
- [ ] Mark the approval status clearly

## Step 9: Update Progress
- [ ] Mark Code Planning complete in `aidlc-state.md`
- [ ] Update the "Current Status" section
- [ ] Prepare for transition to Code Generation

---

# PART 2: GENERATION

## Step 10: Load Unit Code Generation Plan
- [ ] Read the complete plan from `aidlc-docs/construction/plans/{unit-name}-code-generation-plan.md`
- [ ] Identify the next uncompleted step (first [ ] checkbox)
- [ ] Load the context for that step (unit, dependencies, stories)

## Step 11: Execute Current Step
- [ ] Verify target directory from plan (never aidlc-docs/)
- [ ] **Brownfield only**: Check if target file exists
- [ ] Generate exactly what the current step describes:
  - **If file exists**: Modify it in-place (never create `ClassName_modified.java`, `ClassName_new.java`, etc.)
  - **If file doesn't exist**: Create new file
- [ ] Write to correct locations:
  - **Application Code**: Workspace root per project structure
  - **Documentation**: `aidlc-docs/construction/{unit-name}/code/` (markdown only)
  - **Build/Config Files**: Workspace root
- [ ] Follow unit story requirements
- [ ] Respect dependencies and interfaces

## Step 12: Update Progress
- [ ] Mark the completed step as [x] in the unit code generation plan
- [ ] Mark associated unit stories as [x] when their generation is finished
- [ ] Update `aidlc-docs/aidlc-state.md` current status
- [ ] **Brownfield only**: Verify no duplicate files created (e.g., no `ClassName_modified.java` alongside `ClassName.java`)
- [ ] Save all generated artifacts

## Step 13: Per-Layer QA Verification (MANDATORY)

**CRITICAL**: Each layer MUST pass its QA profile BEFORE the layer is considered complete. Code Review CANNOT approve without QA evidence.

Each layer runs **two verification passes**: (1) deterministic validators from Core Library v1.5.5, then (2) build/tooling checks. Fix validator errors BEFORE running build — validators catch convention issues that would waste build cycles.

- [ ] **BD layer QA** — Conventions Lint:
  - **Validators (deterministic)**: Run `python config/validators/runner.py --profile conventions-lint {db_path}`
    - `validate_sp` → SP naming, QUOTENAME, audit columns, error codes, TRY/CATCH
    - `validate_db_schema` → CREATE TABLE conventions, naming
    - `validate_audit_columns` → RecordStatus, RecordCreationUser/Date, RecordEditUser/Date
  - If validator ERRORS → fix → re-run validator → repeat (max 3 iterations)
  - Validate SQL syntax (CREATE/ALTER TABLE, SP structure)
  - **If ANY check fails**: Fix BD layer BEFORE proceeding to Backend/Frontend
- [ ] **Backend layer QA** — Build + Unit Tests:
  - **Validators (deterministic)**: Run `python config/validators/runner.py --profile build-unit {backend_path}`
    - `validate_dotnet_handler` → [FromServices], ApiResponse\<T\>, FluentValidation, handler pattern
    - `validate_dotnet_project` → launchSettings.json, appsettings.Local.json, nuget.config
    - `validate_dotnet_deps` → ANTA.Shared.* references, versions
  - If validator ERRORS → fix → re-run validator → repeat (max 3 iterations)
  - Run `dotnet build` — MUST exit code 0
  - Run unit tests — all MUST pass
  - Validate generated endpoints match openapi.yaml (method, path, request/response types)
  - Validate all imports resolve (no missing using statements)
  - **If build fails**: Fix before marking Backend complete
- [ ] **Frontend layer QA** — Build + Component Tests:
  - **Validators (deterministic)**: Run `python config/validators/runner.py --profile build-component {frontend_path}`
    - `validate_react_feature` → feature structure (page, hooks, types, store), barrel files
    - `validate_react_shared` → 11 Anta\* wrappers present, useHostAuth
    - `validate_no_any` → zero `any` in .ts/.tsx files
  - If validator ERRORS → fix → re-run validator → repeat (max 3 iterations)
  - Run `tsc --noEmit` — MUST exit code 0
  - Run `rsbuild build` — MUST exit code 0
  - Run component tests (React Testing Library) — all MUST pass
  - Validate generated hooks/pages match openapi.yaml endpoints
  - **If build fails**: Fix before marking Frontend complete

**Fix loop rule**: Max 3 validator iterations per layer. If errors persist after 3 attempts → log in `aidlc-docs/audit.md`, escalate to Code Review for human triage.

**Evidence requirement**: Log QA results (validator output + build/test command output) in `aidlc-docs/audit.md`. Code Review Step 3 MUST reference this evidence.

## Step 14: Continue or Complete Generation
- [ ] If more steps remain, return to Step 10
- [ ] If all steps complete AND all per-layer QA has passed (Step 13), proceed to present completion message

## Step 15: Present Completion Message
- Present completion message in this structure:
     1. **Completion Announcement** (mandatory): Always start with this:

```markdown
# 💻 Code Generation Complete - [unit-name]
```

     2. **AI Summary** (optional): Provide structured bullet-point summary
        - **Brownfield**: Distinguish modified vs created files (e.g., "• Modified: `src/services/user-service.ts`", "• Created: `src/services/auth-service.ts`")
        - **Greenfield**: List created files with paths (e.g., "• Created: `src/services/user-service.ts`")
        - List tests, documentation, deployment artifacts with paths
        - Keep factual, no workflow instructions
     3. **Formatted Workflow Message** (mandatory): Always end with this exact format:

```markdown
> **📋 REVIEW REQUIRED:**  
> Please examine the generated code at:
> - **Application Code**: `[actual-workspace-path]`
> - **Documentation**: `aidlc-docs/construction/[unit-name]/code/`



> **🚀 WHAT'S NEXT?**
>
> **You may:**
>
> - 🔧 **Request Changes** - Ask for modifications to the generated code based on your review  
> - ✅ **Continue to Next Stage** - Approve code generation and proceed to **[next-unit/Build & Test]**

---
```

## Step 16: Wait for Explicit Approval
- Do not proceed until the user explicitly approves the generated code
- Approval must be clear and unambiguous
- If user requests changes, update the code and repeat the approval process

## Step 17: Record Approval and Update Progress
- Log approval in audit.md with timestamp
- Record the user's approval response with timestamp
- Mark Code Generation stage as complete for this unit in aidlc-state.md

## Step 18: Skill Feedback Capture (Early Detection)

**See `common/skill-feedback.md` for full feedback definitions (result types, severity levels, file format).**

This is the **earliest detection point** for skill pattern issues — captured during generation itself, before Code Review or Build & Test validate the output.

IF `aidlc-state.md` → Organizational Skills section lists any consumed skills:
- [ ] For each Skill ID that **actively generated code patterns** in this unit:
  - Read skill version from YAML frontmatter (`metadata.version`)
  - Did the agent need to deviate from the skill's prescribed pattern to satisfy requirements? → Record `correction` with explanation of the deviation
  - Was the skill missing a pattern the agent had to invent from scratch? → Record `gap` with the missing guidance description
- [ ] Assign severity per entry: `low` | `medium` | `high`
- [ ] Append entries to `aidlc-docs/skill-feedback.md` (create file with header template from `common/skill-feedback.md` if it does not exist). Include the Version column.
- [ ] Do NOT record `ok` at this stage — only Code Review and Build & Test can confirm a pattern is correct

ELSE: Skip — no skills consumed, no feedback to capture.

---

## Critical Rules

### Code Location Rules
- **Application code**: Workspace root only (NEVER aidlc-docs/)
- **Documentation**: aidlc-docs/ only (markdown summaries)
- **Read workspace root** from aidlc-state.md before generating code

**Structure patterns by project type**:
- **Brownfield**: Use existing structure (e.g., `src/main/java/`, `lib/`, `pkg/`)
- **Greenfield single unit**: `src/`, `tests/`, `config/` in workspace root
- **Greenfield multi-unit (microservices)**: `{unit-name}/src/`, `{unit-name}/tests/`
- **Greenfield multi-unit (monolith)**: `src/{unit-name}/`, `tests/{unit-name}/`

### Mandatory Scaffolding Checklist (Greenfield)

**CRITICAL**: For greenfield projects, EVERY layer MUST generate its scaffolding files. These are NOT optional — missing scaffolding files mean the project won't build.

#### BD Layer Scaffolding
- [ ] `00_Schema.sql` — Schema creation (e.g., `CREATE SCHEMA [Emp]`)

#### Backend Layer Scaffolding
- [ ] `.csproj` — Project file with package references
- [ ] `Program.cs` — Application entry point with module registration
- [ ] `appsettings.json` + `appsettings.Development.json` — Configuration
- [ ] `launchSettings.json` — Launch profiles (ports, environment)
- [ ] `nuget.config` — NuGet package sources (if custom feeds)
- [ ] Module registration file (e.g., `EmployeesModule.cs`) — Endpoint + handler DI registration

#### Frontend Layer Scaffolding
- [ ] `package.json` — Dependencies and scripts
- [ ] `rsbuild.config.ts` — Rsbuild/Module Federation configuration
- [ ] `mf-entry.js` — Microfrontend entry point
- [ ] `App.tsx` — Root component with routing
- [ ] `shared/components/` — Copy 11 Anta* wrapper components from design-system skill
- [ ] `shared/constants.ts`, `shared/types.ts` — Shared types and constants
- [ ] `shared/hooks/index.ts` — Hook barrel exports

#### Docker Scaffolding (via `docker-local` skill)
- [ ] `Dockerfile_local` — Development Dockerfile
- [ ] `docker-compose.yml` — Service composition

#### Gateway Scaffolding (via `dotnet-gateway` skill)
- [ ] Ocelot route configuration for the new module

**Code Gen Plan (Part 1) MUST include all applicable scaffolding items as checkboxes. Code Review MUST verify all scaffolding items are generated.**

### Brownfield File Modification Rules
- Check if file exists before generating
- If exists: Modify in-place (never create copies like `ClassName_modified.java`)
- If doesn't exist: Create new file
- Verify no duplicate files after generation (Step 12)

### Planning Phase Rules
- Create explicit, numbered steps for all generation activities
- Include story traceability in the plan
- Document unit context and dependencies
- Get explicit user approval before generation

### Generation Phase Rules
- **NO HARDCODED LOGIC**: Only execute what's written in the unit plan
- **FOLLOW PLAN EXACTLY**: Do not deviate from the step sequence
- **UPDATE CHECKBOXES**: Mark [x] immediately after completing each step
- **STORY TRACEABILITY**: Mark unit stories [x] when functionality is implemented
- **RESPECT DEPENDENCIES**: Only implement when unit dependencies are satisfied

### Automation Friendly Code Rules
When generating UI code (web, mobile, desktop), ensure elements are automation-friendly:
- Add `data-testid` attributes to interactive elements (buttons, inputs, links, forms)
- Use consistent naming: `{component}-{element-role}` (e.g., `login-form-submit-button`, `user-list-search-input`)
- Avoid dynamic or auto-generated IDs that change between renders
- Keep `data-testid` values stable across code changes (only change when element purpose changes)

## Completion Criteria
- Complete unit code generation plan created and approved
- All steps in unit code generation plan marked [x]
- All unit stories implemented according to plan
- All code and tests generated (tests will be executed in Build & Test phase)
- Deployment artifacts generated
- Complete unit ready for build and verification
