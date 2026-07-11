# AI-DLC Terminology Glossary

## Core Terminology

### Phase vs Stage

**Phase**: One of the five high-level lifecycle phases in AI-DLC
- 🔵 **INCEPTION PHASE** - Planning & Architecture (WHAT and WHY)
- 🟢 **CONSTRUCTION PHASE** - Design, Implementation & Test (HOW)
- 🟡 **OPERATIONS PHASE** - Deployment & Monitoring
- 🟣 **CLOSURE PHASE** - Archival & Handoff
- 🟠 **CHANGE MANAGEMENT PHASE** - Re-entry & Evolution

**Stage**: An individual workflow activity within a phase
- Examples: Context Assessment stage, Requirements Assessment stage, Code Planning stage
- Each stage has specific prerequisites, steps, and outputs
- Stages can be ALWAYS-EXECUTE or CONDITIONAL

**Usage Examples**:
- ✅ "The CONSTRUCTION phase contains 7 stages"
- ✅ "The Code Planning stage is always executed"
- ✅ "We're in the INCEPTION phase, executing the Requirements Assessment stage"
- ❌ "The Requirements Assessment phase" (should be "stage")
- ❌ "The CONSTRUCTION stage" (should be "phase")

## Five-Phase Lifecycle

### INCEPTION PHASE
**Purpose**: Planning and architectural decisions  
**Focus**: Determine WHAT to build and WHY  
**Location**: `inception/` directory

**Stages**:
- Workspace Detection (ALWAYS)
- Reverse Engineering (CONDITIONAL - Brownfield only)
- Requirements Analysis (ALWAYS - Adaptive depth)
- User Stories (CONDITIONAL)
- ISO 27001 Assessment (ALWAYS - Adaptive depth)
- Workflow Planning (ALWAYS)
- Application Design (CONDITIONAL)
- QA Matrix Generation (ALWAYS)
- Design - Units Planning/Generation (CONDITIONAL)

**Outputs**: Requirements, user stories, architectural decisions, unit definitions, ISO 27001 assessment, QA Matrix

### CONSTRUCTION PHASE
**Purpose**: Detailed design and implementation  
**Focus**: Determine HOW to build it  
**Location**: `construction/` directory

**Stages**:
- HU Guide Generation (CONDITIONAL - Multi-repo)
- Functional Design (CONDITIONAL, per-unit)
- NFR Requirements (CONDITIONAL, per-unit)
- NFR Design (CONDITIONAL, per-unit)
- Infrastructure Design (CONDITIONAL, per-unit)
- Code Planning (ALWAYS)
- Code Generation (ALWAYS)
- Build and Test (ALWAYS)

**Outputs**: Design artifacts, NFR implementations, code, tests, HU Guides

### OPERATIONS PHASE
**Purpose**: Deployment and operational readiness  
**Focus**: How to DEPLOY and RUN it  
**Location**: `operations/` directory

**Stages**:
- Release Documentation (CONDITIONAL)
- Operations (PLACEHOLDER)

**Outputs**: Build instructions, deployment guides, monitoring setup, verification procedures, release notes

### CLOSURE PHASE
**Purpose**: Project archival and formal handoff  
**Focus**: How to CLOSE and HANDOVER  
**Location**: `closure/` directory

**Stages**:
- Project Snapshot (ALWAYS)
- Version Archive (ALWAYS)
- Stakeholder Signoff (CONDITIONAL)
- Project Handoff (CONDITIONAL)

**Outputs**: Final state capture, tagged release, signoff document, handoff package

### CHANGE MANAGEMENT PHASE
**Purpose**: Re-entry into closed projects for maintenance or evolution  
**Focus**: How to RE-ENTER and SCOPE changes  
**Location**: `change-management/` directory

**Stages**:
- Re-onboarding (ALWAYS)
- Change Request (ALWAYS)
- Impact Analysis (ALWAYS)

**Outputs**: Restored context, change scope, impact assessment

---

## Workflow Stages

### Always-Execute Stages
- **Workspace Detection**: Initial analysis of workspace state and project type
- **Requirements Analysis**: Gathering requirements (depth varies based on complexity)
- **Workflow Planning**: Creating execution plan for which phases to run
- **Code Planning**: Creating detailed implementation plans for code generation
- **Code Generation**: Generating actual code based on plans and prior artifacts
- **Build and Test**: Building all units and executing comprehensive testing

### Conditional Stages
- **Reverse Engineering**: Analyzing existing codebase (brownfield projects only)
- **User Stories**: Creating user stories and personas (includes Story Planning and Story Generation)
- **Application Design**: Designing application components, methods, business rules, and services
- **Design**: Designing system components (includes Units Planning, Units Generation, per-unit design)
- **Functional Design**: Technology-agnostic business logic design (per-unit)
- **NFR Requirements**: Determining NFRs and selecting tech stack (per-unit)
- **NFR Design**: Incorporating NFR patterns and logical components (per-unit)
- **Infrastructure Design**: Mapping to actual infrastructure services (per-unit)

## Application Design Terms

- **Component**: A functional unit with specific responsibilities
- **Method**: A function or operation within a component with defined business rules
- **Business Rule**: Logic that governs method behavior and validation
- **Service**: Orchestration layer that coordinates business logic across components
- **Component Dependency**: Relationship and communication pattern between components

## Architecture Terms (Infrastructure)

### Unit of Work
A logical grouping of user stories for development purposes. The term used during planning and decomposition.

**Usage**: "We need to decompose the system into units of work"

### Service
An independently deployable component in a microservices architecture. Each service is a separate unit of work.

**Usage**: "The Payment Service handles all payment processing"

### Module
A logical grouping of functionality within a single service or monolith. Modules are not independently deployable.

**Usage**: "The authentication module within the User Service"

### Component
A reusable building block within a service or module. Components are classes, functions, or packages that provide specific functionality.

**Usage**: "The EmailValidator component validates email addresses"

- **HU (Historia de Usuario)**: User Story. A user-centered narrative that describes a feature from the perspective of the end user. Each HU maps to API endpoints and QA test cases via the traceability chain.
- **Documentation Hub**: The central repository where the AI-DLC process orchestrates planning (Inception), testing (Build & Test E2E), release (Operations), and archival (Closure). In multi-repo projects, this is the command center.
- **QA Matrix**: The central traceability artifact that maps HU → API Endpoint → QA Test Case → E2E Test Script. Generated before code implementation, updated with results during Build & Test. Stored in `aidlc-docs/inception/qa-matrix.md`.
- **Traceability Chain**: The end-to-end link from requirements to tests: HU → API Contract → QA Test Cases → E2E Test Plan → E2E Test Code. See `common/traceability.md`.
- **Multi-Repo Architecture**: A project structure where code is distributed across multiple repositories with distinct roles (Doc Hub, Gateway, Core API, Domain API, Frontend Host, Frontend Domain, Mobile). See `common/multi-repo-architecture.md`.
- **HU Guide**: A self-contained implementation guide generated per User Story per repository. Includes API subset, ISO 27001 controls, implementation checklist, unit test requirements, code review checklist, and traceability links. See `construction/hu-guide-template.md`.
- **Repository Structure**: The project's repository architecture classification — Single-Repo (all code in one repository) or Multi-Repo (code distributed across multiple repositories with distinct roles). Identified during Requirements Analysis (Step 5b). Recorded as a HARD CONSTRAINT when multi-repo.
- **HU-Repo Distribution Map**: A mapping artifact that assigns each User Story (HU) to the specific repositories it impacts. Generated during Workflow Planning (Step 5b, multi-repo only). Consumed by QA Matrix, HU Guide Generation, and Build & Test. Stored in `aidlc-docs/inception/plans/hu-repo-distribution.md`.
- **Stage Profile**: A recommended set of EXECUTE/SKIP decisions for all stages, derived from the combination of Request Type and Initial Scope. Generated during Workflow Planning (Step 2.6). Can be overridden by project-specific context.
- **Repo Completion Tracking**: A verification mechanism in Build & Test that confirms all code repositories have completed their assigned HU implementations before launching E2E tests. Multi-repo only. Cross-references the HU-Repo Distribution Map.
- **Organizational Skill**: A Markdown file containing pre-established templates, standards, or conventions that an organization uses across projects. Skills are discovered during Workspace Detection (Step 3.5) and consumed by downstream stages via SKILL CHECK blocks. Skills are optional, additive, and external to the framework. See `common/organizational-skills.md`.
- **Skill ID**: The identifier used to match a discovered skill to the stage that consumes it. Derived from the skill's directory name or filename. Built-in Skill IDs (e.g., `hu-format`, `db-standards`, `code-standards`) are auto-mapped to stages; custom IDs are available as general references. See `common/organizational-skills.md` → Built-in Skill IDs table.
- **Skill Enforcement Level**: A field in the skill's YAML frontmatter (`enforcement: mandatory` or `enforcement: optional`) that controls how the skill is consumed. Mandatory skills are auto-applied as HARD CONSTRAINTS without user confirmation. Optional skills (default) require user confirmation before applying. See `common/organizational-skills.md` → Skill Enforcement Levels.

## Terminology Guidelines

### When to Use Each Term

**Unit of Work**:
- During Units Planning and Units Generation phases
- When discussing system decomposition
- In planning documents and discussions
- Example: "How should we decompose this into units of work?"

**Service**:
- When referring to independently deployable components
- In microservices architecture contexts
- In deployment and infrastructure discussions
- Example: "The Order Service will be deployed to ECS"

**Module**:
- When referring to logical groupings within a service
- In monolith architecture contexts
- When discussing internal organization
- Example: "The reporting module generates all reports"

**Component**:
- When referring to specific classes, functions, or packages
- In design and implementation discussions
- When discussing reusable building blocks
- Example: "The DatabaseConnection component manages connections"

## Stage Terminology

### Planning vs Generation
- **Planning**: Creating a plan with questions and checkboxes for execution
- **Generation**: Executing the plan to create artifacts

Examples:
- Story Planning → Story Generation
- Units Planning → Units Generation
- Unit Design Planning → Unit Design Generation
- NFR Planning → NFR Generation
- Code Planning → Code Generation

### Depth Levels
- **Minimal**: Quick, focused execution for simple changes
- **Standard**: Normal depth with standard artifacts for typical projects
- **Comprehensive**: Full depth with all artifacts for complex/high-risk projects

## Artifact Types

### Plans
Documents with checkboxes and questions that guide execution.
- Located in `aidlc-docs/plans/`
- Examples: `story-generation-plan.md`, `unit-of-work-plan.md`

### Artifacts
Generated outputs from executing plans.
- Located in various `aidlc-docs/` subdirectories
- Examples: `requirements.md`, `stories.md`, `design.md`

### State Files
Files tracking workflow progress and status.
- `aidlc-state.md`: Overall workflow state
- `audit.md`: Complete audit trail of all interactions

## Common Abbreviations

- **AI-DLC**: AI-Driven Development Life Cycle
- **NFR**: Non-Functional Requirements
- **UOW**: Unit of Work
- **API**: Application Programming Interface
- **CDK**: Cloud Development Kit (AWS)
