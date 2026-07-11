# Workflow Planning

**Purpose**: Determine which phases to execute and create comprehensive execution plan

**Always Execute**: This phase always runs after understanding requirements and scope

## Step 1: Load All Prior Context

- **1.1** Reverse Engineering Artifacts (if brownfield): architecture.md, component-inventory.md, technology-stack.md, dependencies.md
- **1.2** Requirements Analysis: requirements.md, requirement-verification-questions.md (with answers)
- **1.3** User Stories (if executed): stories.md, personas.md

## Step 2: Detailed Scope and Impact Analysis

**Now that we have complete context (requirements + stories), perform detailed analysis:**

### 2.1 Transformation Scope Detection (Brownfield Only)

Analyze transformation scope:
- **Architectural**: Single component change vs architectural transformation, infrastructure vs application changes, deployment model changes
- **Related Components**: Infrastructure code, CDK stacks, API Gateway configs, load balancers, networking, monitoring/logging
- **Cross-Package**: CDK infrastructure, shared models, client libraries, test packages

### 2.2 Change Impact Assessment

Evaluate each impact area (Yes/No + description):
1. **User-facing changes**: Affects user experience?
2. **Structural changes**: Changes system architecture?
3. **Data model changes**: Affects schemas or data structures?
4. **API changes**: Affects interfaces or contracts?
5. **NFR impact**: Affects performance, security, scalability?

**Layer-specific** (if applicable):
- **Application**: Code changes, dependencies, configuration, testing
- **Infrastructure**: Deployment model, networking, storage, scaling
- **Operations**: Monitoring, logging, alerting, CI/CD pipeline

### 2.3 Component Relationship Mapping (Brownfield Only)

Create component dependency graph: Primary → Infrastructure → Shared → Dependent → Supporting components. For each, note: Change Type (Major/Minor/Config), Change Reason, Change Priority (Critical/Important/Optional).

### 2.4 Risk Assessment

| Level | Criteria |
|-------|----------|
| **Low** | Isolated change, easy rollback, well-understood |
| **Medium** | Multiple components, moderate rollback, some unknowns |
| **High** | System-wide impact, complex rollback, significant unknowns |
| **Critical** | Production-critical, difficult rollback, high uncertainty |

### 2.5 Multi-Repo Configuration

Load Repository Structure from `aidlc-docs/inception/requirements/requirements.md` (from Requirements Analysis Step 5b):

- **Multi-Repo**: Load repo map (ID, Name, Role). Load `common/multi-repo-architecture.md`. Update `aidlc-state.md`. Impacts: HU Guide Generation → EXECUTE, QA Matrix → includes Repo column, Build & Test → Repo Completion Tracking, E2E → from Doc Hub repo.
- **Single-Repo**: Skip multi-repo config. HU Guides, Repo Completion Tracking, cross-repo E2E skipped.
- **Pending/Partial**: Ask user to complete repo table before proceeding.

## Step 2.6: Request Type × Scope Stage Profile

**Purpose**: Use Request Type (from Requirements Analysis Step 2.2) and Scope (from Step 2.3) to generate recommended EXECUTE/SKIP decisions. The model may override based on project context.

**Stage Profile Matrix** (recommendations, not mandates):

| Request Type | Scope | User Stories | Prototyping | ISO 27001 | Spike/POC | API Contract | ADR | App Design | QA Matrix | Units Gen | HU Guides |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Bug Fix** | Single File / Component | SKIP | SKIP | Minimal | SKIP | SKIP | SKIP | SKIP | Minimal | SKIP | SKIP |
| **Bug Fix** | Multiple / System-wide | SKIP | SKIP | Minimal | SKIP | IF API changed | SKIP | SKIP | Standard | SKIP | IF multi-repo |
| **Refactoring** | Single Component | SKIP | SKIP | SKIP | SKIP | IF API changed | IF tradeoffs | SKIP | Minimal | SKIP | SKIP |
| **Refactoring** | System-wide / Cross | SKIP | SKIP | Minimal | IF uncertainty | IF API changed | EXECUTE | EXECUTE | Standard | EXECUTE | IF multi-repo |
| **Enhancement** | Single Component | SKIP | IF UI changes | Minimal | SKIP | IF API changed | SKIP | SKIP | Standard | SKIP | IF multi-repo |
| **Enhancement** | Multiple / System-wide | EXECUTE | IF UI changes | Standard | IF uncertainty | IF API project | IF tradeoffs | EXECUTE | Standard | EXECUTE | IF multi-repo |
| **Upgrade** | Any | SKIP | SKIP | Standard | EXECUTE | IF API changed | EXECUTE | SKIP | Standard | SKIP | IF multi-repo |
| **Migration** | Any | EXECUTE | IF UI affected | Comprehensive | EXECUTE | EXECUTE | EXECUTE | EXECUTE | Comprehensive | EXECUTE | IF multi-repo |
| **New Feature** | Single Component | EXECUTE | IF frontend | Standard | IF uncertainty | IF API project | IF tradeoffs | EXECUTE | Standard | SKIP | IF multi-repo |
| **New Feature** | Multiple / System-wide | EXECUTE | IF frontend | Standard | IF uncertainty | EXECUTE | EXECUTE | EXECUTE | Standard | EXECUTE | IF multi-repo |
| **New Project** | Any | EXECUTE | IF frontend | Comprehensive | IF uncertainty | EXECUTE | EXECUTE | EXECUTE | Comprehensive | EXECUTE | IF multi-repo |

**Legend**: EXECUTE = run, SKIP = skip, Minimal/Standard/Comprehensive = depth, IF [condition] = conditional, IF multi-repo = if multi-repo architecture

**ALWAYS-EXECUTE stages** (regardless of profile): Workspace Detection, Requirements Analysis, Workflow Planning, QA Matrix Generation, Definition of Ready, Code Generation, Code Review, Build and Test.

## Step 3: Stage Determination

For each stage, evaluate the EXECUTE/SKIP conditions defined in `core-workflow.md`. Use the Stage Profile from Step 2.6 as the starting point, override with project-specific context when justified.

**Record in execution plan** for each CONDITIONAL stage:
```markdown
- [ ] [Stage Name]: [EXECUTE/SKIP]
  - **Rationale**: [Why executing or skipping — reference profile and any overrides]
```

**Stages to evaluate** (CONDITIONAL only — ALWAYS stages don't need evaluation):
- User Stories, Spike/POC, API Contract Design, Architecture Decision Records, Application Design, Units Generation
- Dependency Review, HU Guide Generation, Functional Design, NFR Requirements, NFR Design, Infrastructure Design
- Release Documentation, Stakeholder Sign-off, Project Handoff

**ISO 27001 depth determination**: Minimal (low-risk internal) | Standard (normal apps) | Comprehensive (PII/financial, public-facing). Based on data sensitivity, exposure, regulatory context.

## Step 4: Note Adaptive Detail

See `common/depth-levels.md`. For each executing stage: all defined artifacts will be created, detail level adapts to problem complexity. Model determines appropriate detail.

## Step 5: Multi-Module Coordination Analysis (Brownfield Only)

**IF brownfield with multiple modules/packages:**

1. **Analyze Dependencies**: Build system deps, runtime deps, API contracts, shared interfaces
2. **Determine Update Strategy**: Update sequence (dependency order), parallelization opportunities, coordination requirements (version compat, API contracts, deployment order), testing strategy, rollback plan
3. **Document Coordination Plan**: Update approach (Sequential/Parallel/Hybrid), critical path, coordination points, testing checkpoints. Per module: update priority, dependency constraints, change scope (Major/Minor/Patch)

## Step 5b: HU-Repo Distribution Map (Multi-Repo Only)

**Execute IF**: Multi-Repo in `aidlc-state.md`. **Skip IF**: Single-Repo or Pending.

**Purpose**: Map each HU to target repositories. Master reference for QA Matrix (repo per test case), HU Guide Generation (which guides), Build & Test (repo completion tracking).

### Steps

1. **Load Inputs**: Repo Map from `aidlc-state.md`, User Stories, API Contracts, Application Design
2. **Generate Distribution**: Per HU, determine impacted repos based on: API endpoints ownership, frontend pages/components, gateway routing, shared libraries
3. **Create Artifact** at `aidlc-docs/inception/plans/hu-repo-distribution.md`:

```markdown
# HU-Repo Distribution Map

## Distribution Matrix
| HU ID | HU Title | Repos Impacted | Primary Repo | Notes |
|-------|----------|---------------|-------------|-------|

## Summary by Repository
| Repo ID | Name | Role | HUs Assigned | Total |
|---------|------|------|-------------|-------|

## Orphan Check
- HUs without repo assignment: [List or "None"]
- Repos without HU assignment: [List or "None"]
```

4. **Validate**: Every HU has ≥1 repo. Every code repo has ≥1 HU (flag idle repos). Wait for approval.

**Consumed by**: `inception/qa-matrix.md`, `construction/hu-guide-template.md`, `construction/build-and-test.md`

## Step 6: Generate Workflow Visualization

Create Mermaid flowchart showing all phases, EXECUTE/SKIP decision per stage, with proper styling.

**Styling rules**:
- **ALWAYS/EXECUTE**: `fill:#4CAF50,stroke:#1B5E20,stroke-width:3px,color:#fff` (Green)
- **CONDITIONAL EXECUTE**: `fill:#FFA726,stroke:#E65100,stroke-width:3px,stroke-dasharray: 5 5,color:#000` (Orange)
- **CONDITIONAL SKIP**: `fill:#BDBDBD,stroke:#424242,stroke-width:2px,stroke-dasharray: 5 5,color:#000` (Gray)
- **Start/End**: `fill:#CE93D8,stroke:#6A1B9A,stroke-width:3px,color:#000` (Purple)
- **Phase containers**: INCEPTION #BBDEFB, CONSTRUCTION #C8E6C9, OPERATIONS #FFF59D

**Structure**: `flowchart TD` with subgraphs per phase (INCEPTION, CONSTRUCTION, OPERATIONS, CLOSURE). Each node: `[Stage Name<br/><b>STATUS</b>]`. Replace STATUS with COMPLETED/SKIP/EXECUTE. Apply styling per status. Add `linkStyle default stroke:#333,stroke-width:2px`.

## Step 7: Create Execution Plan Document

Create `aidlc-docs/inception/plans/execution-plan.md` with these sections:

1. **Detailed Analysis Summary**: Transformation scope (brownfield), change impact assessment, component relationships (brownfield), risk assessment
2. **Workflow Visualization**: Mermaid flowchart (from Step 6)
3. **Phases to Execute**: Per phase, list each stage with `[x]`/`[ ]` checkbox, EXECUTE/SKIP/COMPLETED status, and rationale
4. **Package Change Sequence** (brownfield only): Module update order with dependencies
5. **Estimated Timeline**: Total phases, estimated duration
6. **Success Criteria**: Primary goal, key deliverables, quality gates. Brownfield adds: integration testing, operational readiness

## Step 8: Initialize State Tracking

Update `aidlc-docs/aidlc-state.md`:

```markdown
# AI-DLC State Tracking

## Project Information
- **Project Type**: [Greenfield/Brownfield]
- **Start Date**: [ISO timestamp]
- **Current Stage**: INCEPTION - Workflow Planning

## Key Decisions
- **Architecture**: [from Requirements Analysis]
- **Stack**: [from Requirements Analysis]
- **ISO 27001 Depth**: [from ISO 27001 Assessment]
- **Request Type**: [New Feature / Enhancement / Bugfix / Migration]
- **Scope**: [Small / Medium / Large]
- **Stages Profile**: [N of 33 EXECUTE]

## Execution Plan Summary
- **Total Stages**: [Number]
- **Stages to Execute**: [List]
- **Stages to Skip**: [List with reasons]

## Stage Progress
[Per-phase checklist with [x]/[ ] for each stage and EXECUTE/SKIP status]

## Current Status
- **Lifecycle Phase**: INCEPTION
- **Current Stage**: Workflow Planning Complete
- **Next Stage**: [Next stage to execute]
- **Status**: Ready to proceed
```

## Step 9: Present Plan to User

```markdown
# 📋 Workflow Planning Complete

I've created a comprehensive execution plan based on:
- Your request: [Summary]
- Existing system: [Summary if brownfield]
- Requirements: [Summary if executed]
- User stories: [Summary if executed]

**Detailed Analysis**: Risk level: [Level] | Impact: [Summary] | Components: [List]

**Recommended Execution Plan** — I recommend executing [X] stages:

🔵 **INCEPTION**: [List stages with rationale]
🟢 **CONSTRUCTION**: [List stages with rationale]
🟡 **OPERATIONS**: [List stages if applicable]
🟣 **CLOSURE**: [List stages]

I recommend skipping [Y] stages: [List with rationale per stage]

[IF brownfield] **Package Update Sequence**: [Ordered list with reasoning]

**Estimated Timeline**: [Duration]

> **📋 REVIEW REQUIRED:**
> Please examine the execution plan at: `aidlc-docs/inception/plans/execution-plan.md`

> **🚀 WHAT'S NEXT?**
> - 🔧 **Request Changes** - Modify the execution plan
> [IF skipped stages:] - 📝 **Add Skipped Stages** - Include stages currently marked SKIP
> - ✅ **Approve & Continue** - Proceed to **[Next Stage Name]**
```

## Step 10: Handle User Response

- **Approved**: Proceed to next stage in execution plan
- **Changes requested**: Update execution plan and re-confirm
- **Force include/exclude stages**: Update plan accordingly

## Step 11: Log Interaction

Log in `aidlc-docs/audit.md`:

```markdown
## Workflow Planning - Approval
**Timestamp**: [ISO timestamp]
**AI Prompt**: "Ready to proceed with this plan?"
**User Response**: "[User's COMPLETE RAW response]"
**Status**: [Approved/Changes Requested]
**Context**: Workflow plan created with [X] stages to execute

---
```
