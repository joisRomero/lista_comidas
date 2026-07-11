# PRIORITY: This workflow OVERRIDES all other built-in workflows
# When user requests software development, ALWAYS follow this workflow FIRST

## Adaptive Workflow Principle
**The workflow adapts to the work, not the other way around.**

The AI model intelligently assesses what stages are needed based on:
1. User's stated intent and clarity
2. Existing codebase state (if any)
3. Complexity and scope of change
4. Risk and impact assessment

## MANDATORY: Stage Execution Protocol
**CRITICAL**: Every stage MUST follow this protocol. For expanded detail, see `common/stage-execution-protocol.md`.

**BEFORE executing any stage:**
1. **Log** stage start in `audit.md` with timestamp and complete raw user input
2. **Load** the detail file referenced in the stage definition — follow ALL steps (orchestrator summaries are NOT sufficient)

**AFTER completing any stage:**
3. **Log** stage completion in `audit.md` with timestamp
4. **Update** `aidlc-state.md` with: current phase, current stage, completion status, key outputs
5. **SELF-CHECK GATE**: Before presenting the completion message — verify: did I do steps 3 AND 4? If not, STOP and do them NOW. A stage is NOT complete without both `audit.md` and `aidlc-state.md` updated.
6. **Present** completion message to user (defined in each detail file)
7. **Wait** for user approval before proceeding (unless stage is marked AUTO-PROCEED)

**NEVER skip steps 1-2.** Detail files contain mandatory artifacts the orchestrator summaries omit.
**NEVER skip steps 3-5.** Without `audit.md` and `aidlc-state.md` updates, the audit trail breaks and session resumption fails. The Self-Check Gate (step 5) exists because agents consistently skip state updates when they're not verified at the transition point.
**NEVER assume user intent not explicitly stated.** When in doubt, consult `common/overconfidence-prevention.md`.

## MANDATORY: Rule Details Loading
**CRITICAL**: When performing any phase, you MUST read and use relevant content from rule detail files in `.kiro/aws-aidlc-rule-details/` or `.amazonq/aws-aidlc-rule-details/` directory.

**Common Rules**: Load at workflow start:
- Load `common/session-continuity.md` for session resumption (if aidlc-state.md exists)

**On-demand** (load ONLY when needed):
- `common/stage-execution-protocol.md` → for expanded Entry/Execution/Exit protocol detail
- `common/question-format-guide.md` → before creating any question file
- `common/content-validation.md` → before creating any artifact file
- `common/organizational-skills.md` → during Workspace Detection skill scan
- `common/terminology.md` → if any term is ambiguous (Phase vs Stage, Unit vs Service)
- `common/overconfidence-prevention.md` → when assessment decision is ambiguous
- `common/multi-repo-architecture.md` → only if multi-repo detected
- `common/traceability.md` → during QA Matrix and Build & Test
- `common/workflow-changes.md` → only if user requests scope change mid-workflow

## MANDATORY: Content Validation
**CRITICAL**: Before creating ANY file, validate content per `common/content-validation.md`:
- Mermaid diagram syntax, ASCII art (`common/ascii-diagram-standards.md`), special character escaping, text alternatives, parsing compatibility

## MANDATORY: Question File Format
**CRITICAL**: All questions MUST follow `common/question-format-guide.md` — multiple choice (A-E), `[Answer]:` tags, validation and ambiguity resolution.

## MANDATORY: Custom Welcome Message
**CRITICAL**: When starting ANY software development request, you MUST display the welcome message.

**How to Display Welcome Message**:
1. Load the welcome message from `.kiro/aws-aidlc-rule-details/common/welcome-message.md` or `.amazonq/aws-aidlc-rule-details/common/welcome-message.md`
2. Display the complete message to the user **translated to the user's language** (per Language Matching rule)
3. This should only be done ONCE at the start of a new workflow
4. Do NOT load this file in subsequent interactions to save context space

## MANDATORY: Language Matching
**CRITICAL**: Always respond in the same language the user uses.
- Spanish input → Spanish response. English input → English response. Any language → match it.
- **Exception**: Keep technical terms (stage names, file names, code) in English.

---

# INCEPTION PHASE

**Purpose**: Planning, requirements gathering, and architectural decisions — determine WHAT to build and WHY

**Stages**: Workspace Detection (ALWAYS) → Reverse Engineering (CONDITIONAL) → Requirements Analysis (ALWAYS) → User Stories (CONDITIONAL) → Prototyping (CONDITIONAL) → ISO 27001 Assessment (ALWAYS) → Spike/POC (CONDITIONAL) → API Contract Design (CONDITIONAL) → Architecture Decision Records (CONDITIONAL) → Workflow Planning (ALWAYS) → Application Design (CONDITIONAL) → QA Matrix Generation (ALWAYS) → Units Generation (CONDITIONAL) → Definition of Ready (ALWAYS)

---

## Workspace Detection (ALWAYS, AUTO-PROCEED)

**Steps** (follow Stage Execution Protocol):
1. Load `inception/workspace-detection.md`
2. Check for `aidlc-state.md` (resume if found), scan workspace, determine brownfield/greenfield
3. **Scan for Organizational Skills** (Step 3.5): Check `.kiro/skills/`, `.amazonq/skills/`, or `skills/`. Register in `aidlc-state.md`. See `common/organizational-skills.md`
4. Determine next: Reverse Engineering (brownfield, no artifacts) OR Requirements Analysis

## Reverse Engineering (CONDITIONAL)

**Execute IF**: Existing codebase detected AND no previous artifacts
**Skip IF**: Greenfield OR previous artifacts exist

**Steps** (follow Stage Execution Protocol):
1. Load `inception/reverse-engineering.md`
2. Analyze packages, business transactions, architecture, code structure, APIs, components, interactions, tech stack, dependencies

## Requirements Analysis (ALWAYS — Adaptive Depth)

Depth: **Minimal** (clear, simple) | **Standard** (normal) | **Comprehensive** (complex, high-risk)

**Steps** (follow Stage Execution Protocol):
1. Load `inception/requirements-analysis.md`
2. Load reverse engineering artifacts (if brownfield), analyze intent, determine depth
3. **MANDATORY — Skill Resolver**: Before generating clarification questions, resolve skills for this stage per `common/skill-resolver.md` and `skills/SKILLS-MANIFEST.md`. The Resolver loads: `repo-structure`, `database-modeling`, `database`, `database-audit`, `dotnet-shared-libs`. Use their conventions in the questions and requirements output.
4. **MANDATORY (Step 5)**: Ask about organizational/technology standards. Present Workspace Detection skills as defaults. Record as HARD CONSTRAINTS — downstream stages must respect without re-asking
5. **MANDATORY (Step 5b)**: Ask about repository structure (single-repo vs multi-repo). If multi-repo, record full repo table (ID with real codes from project code, Name, Role) as HARD CONSTRAINTS. Feeds Workflow Planning, QA Matrix, HU Guides, Build & Test

## User Stories (CONDITIONAL)

**Execute IF**: User-facing features, multiple personas, complex business rules, acceptance criteria needed, stakeholder collaboration
**Skip IF**: Pure refactoring, simple bug fixes, infrastructure-only, no user impact
**Default**: When in doubt, favor inclusion

**Two-part stage**: Part 1 (Planning) → Part 2 (Generation)

**Steps** (follow Stage Execution Protocol):
1. Load `inception/user-stories.md`
2. Perform intelligent assessment (Step 1) to validate stories are needed
3. Reference Requirements Analysis artifacts if available
4. Part 1: Story plan with questions → user answers → analyze ambiguities → approval
5. Part 2: Execute approved plan → stories + personas

## Prototyping (CONDITIONAL)

**Execute IF**: Frontend screens exist in scope
**Skip IF**: Backend-only changes or no UI screens in scope
**ASK IF UNSURE**: If frontend screens exist, ASK the user "¿Deseas generar prototipos HTML antes de continuar?" — do NOT skip silently

**Steps** (follow Stage Execution Protocol):
1. Load `inception/prototyping.md`
2. **MANDATORY — Skill Resolver**: Resolve skills for this stage per `common/skill-resolver.md`. The Resolver loads `html-prototype` for static mockup generation.
3. Identify screens from Requirements Analysis (list, form, detail pages)
4. Generate static HTML mockups using ANTA design system CSS (zero JavaScript)
5. Copy `anta-prototype.css` + HTML files to `aidlc-docs/inception/prototypes/`
6. Present prototype file list to user for browser review
7. **Wait for explicit approval**: User must approve screens before proceeding to API Contract Design

---

## ISO 27001 Assessment (ALWAYS — Adaptive Depth)

Depth: **Minimal** (low-risk internal) | **Standard** (normal apps) | **Comprehensive** (PII/financial, public-facing)

**Steps** (follow Stage Execution Protocol):
1. Load `inception/iso-27001-assessment.md`
2. Load prior context, determine depth by data sensitivity/exposure
3. Identify applicable Annex A controls (Organizational, People, Physical, Technological), map to requirements

## Spike/POC (CONDITIONAL)

**Execute IF**: New technology, unfamiliar integrations, high uncertainty, multiple architectural options
**Skip IF**: Known technology, established patterns, low risk

**Steps** (follow Stage Execution Protocol):
1. Load `inception/spike-poc.md`
2. Execute timeboxed investigation, document findings and recommendations

## API Contract Design (CONDITIONAL)

**Execute IF**: API development (REST/GraphQL/gRPC), service interfaces, contract-first approach
**Skip IF**: No API work, pure frontend/CLI, existing APIs unchanged

**Steps** (follow Stage Execution Protocol):
1. Load `inception/api-contract-design.md`
2. **MANDATORY — Skill Resolver**: Resolve skills for this stage per `common/skill-resolver.md`. The Resolver loads: `api-first-spec`, `database-modeling`, `database-security`, `database-audit`, `dotnet-api`, `lion`. These inform ANTA patterns in the openapi.yaml and authorization matrix.
3. Define endpoints, methods, resources, request/response schemas, error conventions
4. **MANDATORY**: Generate OpenAPI/AsyncAPI specification files (`openapi.yaml` for REST) with ANTA patterns (see api-contract-design.md Step 6)
5. **MANDATORY**: Generate Authorization Matrix — map screens, endpoints, actions, and roles (see api-contract-design.md Step 6b). Output: `aidlc-docs/inception/authorization-matrix.md`. If Lion MCP available, register automatically.
6. **MANDATORY**: Pass Spec Validation Gate (see api-contract-design.md Step 8) — incomplete spec blocks Construction parallel layers

## Architecture Decision Records (CONDITIONAL)

**Execute IF**: Significant architectural decisions, technology selections, multi-approach trade-offs
**Skip IF**: Minor changes, obvious choices, no trade-offs to document

**Steps** (follow Stage Execution Protocol):
1. Load `inception/architecture-decision-records.md`
2. Document context, options with pros/cons, decision, rationale, consequences

---

## Workflow Planning (ALWAYS)

**Steps** (follow Stage Execution Protocol):
1. Load `inception/workflow-planning.md` + `common/content-validation.md`
2. Load all prior context (reverse engineering, intent, requirements, user stories)
3. Determine phases to execute, depth levels per phase
4. **Generate Stage Profile** (Step 2.6): Request Type × Scope matrix → EXECUTE/SKIP recommendations (overridable by project context)
5. **Generate HU-Repo Distribution Map** (Step 5b, multi-repo only): HU → repo mapping → `aidlc-docs/inception/plans/hu-repo-distribution.md`
6. Create multi-package change sequence (brownfield), generate workflow visualization (validate Mermaid syntax)
7. Validate all content per `content-validation.md` before file creation

## Application Design (CONDITIONAL)

**Execute IF**: New components/services needed, business rules need design, service layer required
**Skip IF**: Changes within existing boundaries, no new components

**Steps** (follow Stage Execution Protocol):
1. Load `inception/application-design.md`
2. Load reverse engineering artifacts (if brownfield), execute at appropriate depth

## QA Matrix Generation (ALWAYS)

Generates traceability matrix (HU → API → QA Test Cases) before Definition of Ready. See `common/traceability.md`.

**Steps** (follow Stage Execution Protocol):
1. Load `inception/qa-matrix.md` + `common/traceability.md`
2. Extract HU IDs and linked API endpoints from contracts and stories
3. Load Application Design (if available) for UI components per HU
4. Generate test cases per endpoint: happy path, error/validation, edge cases, security (from ISO assessment)
5. Classify by layer: `API` | `UI` | `E2E`. Assign IDs: `QA-{HU-ID}-{SEQ}`
6. Define E2E User Flows, build Test Data Catalog (`TD-{SEQ}`)
7. Create `aidlc-docs/inception/qa-matrix.md` with 7 sections
8. Flag orphan HUs (no tests) or orphan endpoints (no HU link)

## Units Generation (CONDITIONAL)

**Execute IF**: Multiple units of work, multiple services/modules, complex decomposition
**Skip IF**: Single unit, no decomposition needed

**Steps** (follow Stage Execution Protocol):
1. Load `inception/units-generation.md`
2. Load reverse engineering artifacts (if brownfield), execute at appropriate depth

## Definition of Ready (ALWAYS — Gate to CONSTRUCTION)

Final validation gate. Ensures all INCEPTION artifacts are complete, no blocking issues remain, stakeholder alignment confirmed.

**Steps** (follow Stage Execution Protocol):
1. Load `inception/definition-of-ready.md`
2. Verify required artifacts, no blocking questions, stakeholder approvals, dependency availability

---

# 🟢 CONSTRUCTION PHASE

**Purpose**: Detailed design, NFR implementation, and code generation — determine HOW to build it

**Multi-Repo**: Load `common/multi-repo-architecture.md` at phase start for repo roles and distribution model.

**Stages**: Dependency Review (CONDITIONAL) → HU Guide Generation (CONDITIONAL) → Per-Unit Loop [Functional Design → NFR Requirements → NFR Design → Infrastructure Design → Code Generation → Code Review] → Build and Test (ALWAYS)

**Notes**:
- Each unit is completed fully (design + code) before moving to the next
- QA Matrix is generated in INCEPTION; Build and Test UPDATES it with execution results
- In multi-repo projects, HU Guides are generated before the Per-Unit Loop and manually distributed

---

## Dependency Review (CONDITIONAL)

**Execute IF**: New external dependencies, significant version upgrades, security-sensitive deps
**Skip IF**: No new dependencies, minor internal changes only

**Steps** (follow Stage Execution Protocol):
1. Load `construction/dependency-review.md`
2. Review licenses, CVEs, maintenance status, alternatives

## HU Guide Generation (CONDITIONAL — Multi-Repo Only)

**Execute IF**: Multi-repo architecture AND API contracts AND HUs defined
**Skip IF**: Single-repo project

**Steps** (follow Stage Execution Protocol):
1. Load `construction/hu-guide-template.md` + `common/multi-repo-architecture.md`
2. Load QA Matrix (`aidlc-docs/inception/qa-matrix.md`) for test case IDs
3. Per HU, generate self-contained guides per target repo: API spec subset, ISO controls, implementation checklist, traceability links
4. Save to `aidlc-docs/construction/{hu-id}/guides/{repo-role}-guide.md`
5. Notify user to manually copy guides to target code repositories

---

## Per-Unit Loop

**For each unit, execute the following stages in sequence. Complete each unit fully before the next.**

### Functional Design (CONDITIONAL, per-unit)

**Execute IF**: New data models, complex business logic, business rules need design
**Skip IF**: Simple logic changes, no new business logic

**Steps** (follow Stage Execution Protocol + Construction 2-option completion):
1. Load `construction/functional-design.md`
2. Execute functional design for this unit

### NFR Requirements (CONDITIONAL, per-unit)

**Execute IF**: Performance, security, scalability, or tech stack selection requirements
**Skip IF**: No NFR requirements, tech stack already determined

**Steps** (follow Stage Execution Protocol + Construction 2-option completion):
1. Load `construction/nfr-requirements.md`
2. Execute NFR assessment for this unit

### NFR Design (CONDITIONAL, per-unit)

**Execute IF**: NFR Requirements was executed, patterns need incorporation
**Skip IF**: No NFR requirements, NFR Requirements was skipped

**Steps** (follow Stage Execution Protocol + Construction 2-option completion):
1. Load `construction/nfr-design.md`
2. Execute NFR design for this unit

### Infrastructure Design (CONDITIONAL, per-unit)

**Execute IF**: Infrastructure mapping, deployment architecture, cloud resources needed
**Skip IF**: No infrastructure changes, already defined

**Steps** (follow Stage Execution Protocol + Construction 2-option completion):
1. Load `construction/infrastructure-design.md`
2. Execute infrastructure design for this unit

### Code Generation (ALWAYS, per-unit — Per-Layer Model)

**Always executes for each unit**

**Code Generation operates in 3 phases with per-layer resolution** (see `common/skill-resolver.md`):

**Phase 1**: BD layer → Code Gen → Review → Conventions Lint
**Phase 2**: Backend + Frontend layers → PARALLEL (both from openapi.yaml) → Code Gen → Review → Build+Tests
**Phase 3**: E2E global (Build & Test stage)

**Execution**:
1. **MANDATORY**: Log any user input during this stage in audit.md
2. Load all steps from `construction/code-generation.md`
3. **MANDATORY — Skill Resolver**: Before generating ANY file, resolve skills per layer using `common/skill-resolver.md` and `skills/SKILLS-MANIFEST.md`. The Resolver handles all skill loading — do NOT hardcode skill references inline.
4. **PART 1 - Planning**: Create code generation plan with checkboxes, identifying which layers apply. Get user approval.
5. **PART 2 - Generation**: Execute approved plan per layer in dependency order.

   **MANDATORY — Sub-Agent Delegation Per Layer**:
   Each layer MUST be executed by delegating to a sub-agent task. Do NOT generate all layers yourself sequentially — invoke a sub-agent for each layer with the resolved Project Standards block (see `common/skill-resolver.md` Step 3). This enables parallel execution of Backend + Frontend.

   **Layer execution sequence with delegation**:
   - **Phase 1 — BD layer**: Delegate BD Code Gen to sub-agent → sub-agent generates SQL (schema, tables, SPs) with database-* skills → **BD QA**: sub-agent runs Conventions Lint (naming, audit columns, error codes, SQL syntax)
     - **BD PASS** → continue to Phase 2
     - **BD FAIL → STOP**: Notify all layers, report findings. Do NOT proceed with Backend/Frontend on broken BD.
   - **Phase 2 — Backend + Frontend PARALLEL**: After BD passes, delegate TWO sub-agents simultaneously (both work from validated openapi.yaml):
     - **Backend sub-agent**: Generate .NET code (endpoints, handlers, validators, DTOs) + scaffolding (Docker, Gateway) with dotnet-* skills → **Backend QA**: `dotnet build` + unit tests + validate endpoints match openapi.yaml. **QA MUST pass before sub-agent reports completion.**
     - **Frontend sub-agent**: Generate React code (hooks, components, pages) with react-* skills → **Frontend QA**: `tsc --noEmit` + `rsbuild build` + component tests. **QA MUST pass before sub-agent reports completion.**
   - **Phase 3 — E2E**: Handled in Build & Test stage (after all units complete)
6. **Skill Feedback Capture (Early Detection)**: If organizational skills actively generated code patterns, capture deviations and gaps immediately — do NOT record `ok` at this stage (see `common/skill-feedback.md`)
7. **MANDATORY**: Present standardized 2-option completion message as defined in code-generation.md - DO NOT use emergent behavior
8. **Wait for Explicit Approval**: User must choose between "Request Changes" or "Continue to Next Stage" - DO NOT PROCEED until user confirms
9. **MANDATORY**: Log user's response in audit.md with complete raw input

### Code Review (ALWAYS, per-unit)

**Always executes after Code Generation for each unit**

**Purpose**: Systematic review of generated code before proceeding to next unit or Build and Test

**Execution**:
1. **MANDATORY**: Log any user input during this stage in audit.md
2. Load all steps from `construction/code-review.md`
3. **MANDATORY — Skill Resolver**: Resolve the same skills loaded during Code Generation for this unit. Use them to VERIFY generated code matches conventions.
4. Execute code review — **MUST actually READ the generated files**, not assume compliance:
   - Review code against design specifications and loaded skill conventions
   - Validate error handling patterns
   - Verify test coverage adequacy
   - Identify potential security issues
   - Check for performance concerns
5. Document findings and recommendations — **mark items as NOT IMPLEMENTED if the code does not match, do NOT rubber-stamp**
6. **Skill Feedback Capture**: Evaluate skill performance and append feedback entries (see `construction/code-review.md` and `common/skill-feedback.md`)
7. **MANDATORY**: Present standardized 2-option completion message - DO NOT use emergent behavior
8. **Wait for Explicit Approval**: User must choose between "Request Changes" or "Continue to Next Stage" - DO NOT PROCEED until user confirms
9. **MANDATORY**: Log user's response in audit.md with complete raw input

---

## Build and Test (ALWAYS)

**Steps** (follow Stage Execution Protocol):
1. Load `construction/build-and-test.md`
2. Generate build + test instructions: unit, integration, performance, contract, security, E2E
3. **Repo Completion Tracking** (multi-repo): Verify all repos completed assigned HUs before E2E. Cross-ref `aidlc-docs/inception/plans/hu-repo-distribution.md`
4. Create instruction files in `build-and-test/` subdirectory
5. **Skill Feedback**: Evaluate skill patterns against build/test results. See `common/skill-feedback.md`

---

# 🟡 OPERATIONS PHASE

**Purpose**: Release documentation and operational readiness — how to DEPLOY and RUN it

## Release Documentation (CONDITIONAL)

**Execute IF**: Ready for release/handoff, deployment instructions or runbooks needed
**Skip IF**: Internal tooling, prototype, documentation already complete

**Steps** (follow Stage Execution Protocol):
1. Load `operations/release-documentation.md`
2. Generate release notes, deployment checklist, environment requirements, operational runbook, rollback procedures

## Operations (PLACEHOLDER)

Future scope: deployment planning, monitoring, incident response, maintenance workflows.

---

# 🟣 CLOSURE PHASE

**Purpose**: Formal project completion, archival, and handoff — properly CLOSE and ARCHIVE the project

## Project Snapshot (ALWAYS)

**Steps** (follow Stage Execution Protocol):
1. Load `closure/project-snapshot.md`
2. Capture: final architecture, configuration values, dependencies with versions, environment specs, project metrics

## Version & Archive (ALWAYS)

**Steps** (follow Stage Execution Protocol):
1. Load `closure/version-archive.md`
2. Assign version, create tagged release/archive, store documentation bundle, generate manifest

## Stakeholder Sign-off (CONDITIONAL)

**Execute IF**: Formal stakeholders, contractual/compliance requirements, multi-team handoff
**Skip IF**: Personal/internal project, no formal stakeholders, continuous delivery

**Steps** (follow Stage Execution Protocol):
1. Load `closure/stakeholder-signoff.md`
2. Generate sign-off checklist, document acceptance criteria status, record approvals

## Project Handoff (CONDITIONAL)

**Execute IF**: Transferring to different team, maintenance transition, knowledge transfer needed
**Skip IF**: Same team continues, project being deprecated

**Steps** (follow Stage Execution Protocol):
1. Load `closure/project-handoff.md`
2. Generate handoff package, knowledge transfer checklist, contacts/escalation paths, known issues/tech debt

---

# 🔄 CHANGE MANAGEMENT PHASE

**Purpose**: Handle changes to closed/completed projects — safely RE-OPEN and MODIFY completed work

**When to Enter**: Changes requested to a project that has completed CLOSURE.

## Re-Onboarding (ALWAYS)

**Steps** (follow Stage Execution Protocol):
1. Load `change-management/re-onboarding.md`
2. Locate/load project snapshot, restore docs, verify state matches archive, identify drift, rebuild context

## Change Request (ALWAYS)

**Steps** (follow Stage Execution Protocol):
1. Load `change-management/change-request.md`
2. Document change description, rationale, requestor, priority, type, success criteria

## Impact Analysis (ALWAYS)

**Steps** (follow Stage Execution Protocol):
1. Load `change-management/impact-analysis.md`
2. Identify affected components/dependencies, assess risk, estimate effort
3. Determine re-entry: **INCEPTION** (major scope, new features) | **CONSTRUCTION** (implementation, bug fixes) | **OPERATIONS** (docs, deployment)
4. Document rollback strategy, route to recommended phase

---

## Key Principles

- **Adaptive Execution**: Only execute stages that add value
- **Transparent Planning**: Always show execution plan before starting
- **User Control**: User can request stage inclusion/exclusion
- **Progress Tracking**: Update aidlc-state.md with executed and skipped stages
- **Complete Audit Trail**: Log ALL user inputs in audit.md — capture COMPLETE RAW INPUT, never summarize
- **Quality Focus**: Complex changes get full treatment, simple changes stay efficient
- **Content Validation**: Always validate content before file creation per content-validation.md rules
- **NO EMERGENT BEHAVIOR**: Construction stages use standardized 2-option completion messages ONLY

## MANDATORY: Plan-Level Checkbox Enforcement

1. **NEVER complete any work without updating plan checkboxes**
2. **IMMEDIATELY after completing ANY step in a plan file, mark that step [x]**
3. **This must happen in the SAME interaction where the work is completed**
4. **NO EXCEPTIONS**: Every plan step completion MUST be tracked

**Two-Level Tracking**: Plan-Level (detailed execution) + Stage-Level (`aidlc-state.md`). Update both immediately.

## Prompts Logging Requirements

- **MANDATORY**: Log EVERY user input with timestamp in audit.md — capture COMPLETE RAW INPUT (never summarize)
- **MANDATORY**: Log every approval prompt with timestamp before asking, every response after receiving
- **CRITICAL**: ALWAYS append to audit.md — NEVER overwrite
- Use ISO 8601 timestamps. Include stage context.

### Audit Log Format:
```markdown
## [Stage Name or Interaction Type]
**Timestamp**: [ISO timestamp]
**User Input**: "[Complete raw user input - never summarized]"
**AI Response**: "[AI's response or action taken]"
**Context**: [Stage, action, or decision made]

---
```

### Correct Tool Usage for audit.md

✅ CORRECT: Read audit.md → Append/Edit changes
❌ WRONG: Read audit.md → Overwrite entire file with old + new content

## Directory Structure

```text
<WORKSPACE-ROOT>/                   # ⚠️ APPLICATION CODE HERE
├── [project-specific structure]    # Varies by project (see code-generation.md)
│
├── aidlc-docs/                     # 📄 DOCUMENTATION ONLY
│   ├── assets/                     # 📁 SHARED ASSETS (cross-phase)
│   │   ├── references/             # User-provided: wireframes, screenshots, external docs
│   │   └── diagrams/               # Generated: Mermaid exports, architecture visuals
│   ├── inception/                  # 🔵 INCEPTION PHASE
│   │   ├── plans/
│   │   ├── reverse-engineering/
│   │   ├── requirements/
│   │   ├── user-stories/
│   │   ├── prototypes/
│   │   ├── spike-poc/
│   │   ├── api-contracts/
│   │   ├── authorization-matrix.md
│   │   ├── adrs/
│   │   ├── application-design/
│   │   └── definition-of-ready/
│   ├── construction/               # 🟢 CONSTRUCTION PHASE
│   │   ├── plans/
│   │   ├── dependency-review/
│   │   ├── {unit-name}/
│   │   │   ├── functional-design/
│   │   │   ├── nfr-requirements/
│   │   │   ├── nfr-design/
│   │   │   ├── infrastructure-design/
│   │   │   ├── code/
│   │   │   └── code-review/
│   │   └── build-and-test/
│   ├── operations/                 # 🟡 OPERATIONS PHASE
│   │   └── release/
│   ├── closure/                    # 🟣 CLOSURE PHASE
│   │   ├── snapshots/
│   │   ├── archives/
│   │   ├── signoffs/
│   │   └── handoffs/
│   ├── change-management/          # 🔄 CHANGE MANAGEMENT
│   │   ├── change-requests/
│   │   └── impact-analyses/
│   ├── aidlc-state.md
│   └── audit.md
```

**CRITICAL RULE**:
- Application code: Workspace root (NEVER in aidlc-docs/)
- Documentation: aidlc-docs/ only
- Project structure: See code-generation.md for patterns by project type
