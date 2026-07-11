# Requirements Analysis (Adaptive)

**Assume the role** of a product owner

**Adaptive Phase**: Always executes. Detail level adapts to problem complexity.

**See [depth-levels.md](../common/depth-levels.md) for adaptive depth explanation**

## Prerequisites
- Workspace Detection must be complete
- Reverse Engineering must be complete (if brownfield)

## Execution Steps

### Step 1: Load Reverse Engineering Context (if available)

**IF brownfield project**:
- Load `aidlc-docs/inception/reverse-engineering/architecture.md`
- Load `aidlc-docs/inception/reverse-engineering/component-inventory.md`
- Load `aidlc-docs/inception/reverse-engineering/technology-stack.md`
- Use these to understand existing system when analyzing request

### Step 2: Analyze User Request (Intent Analysis)

#### 2.1 Request Clarity
- **Clear**: Specific, well-defined, actionable
- **Vague**: General, ambiguous, needs clarification
- **Incomplete**: Missing key information

#### 2.2 Request Type
- **New Feature**: Adding new functionality
- **Bug Fix**: Fixing existing issue
- **Refactoring**: Improving code structure
- **Upgrade**: Updating dependencies or frameworks
- **Migration**: Moving to different technology
- **Enhancement**: Improving existing feature
- **New Project**: Starting from scratch

#### 2.3 Initial Scope Estimate
- **Single File**: Changes to one file
- **Single Component**: Changes to one component/package
- **Multiple Components**: Changes across multiple components
- **System-wide**: Changes affecting entire system
- **Cross-system**: Changes affecting multiple systems

#### 2.4 Initial Complexity Estimate
- **Trivial**: Simple, straightforward change
- **Simple**: Clear implementation path
- **Moderate**: Some complexity, multiple considerations
- **Complex**: Significant complexity, many considerations

### Step 3: Determine Requirements Depth

**Based on request analysis, determine depth:**

**Minimal Depth** - Use when:
- Request is clear and simple
- No detailed requirements needed
- Just document the basic understanding

**Standard Depth** - Use when:
- Request needs clarification
- Functional and non-functional requirements needed
- Normal complexity

**Comprehensive Depth** - Use when:
- Complex project with multiple stakeholders
- High risk or critical system
- Detailed requirements with traceability needed

### Step 4: Assess Current Requirements

Analyze whatever the user has provided:
   - Intent statements or descriptions (already logged in audit.md)
   - Existing requirements documents (search workspace if mentioned)
   - Pasted content or file references
   - Convert any non-markdown documents to markdown format 

### Step 5: Identify Organizational / Technology Standards

**MANDATORY**: Before analyzing completeness, explicitly ask the user if there are pre-established organizational or technology standards that constrain this project. This prevents the agent from making free-choice technology decisions that conflict with existing organizational norms.

#### SKILL PRE-CHECK (before asking)

**IF** `aidlc-state.md` → Organizational Skills section lists loaded skills:
1. Review ALL loaded skills for any that relate to technology standards. Match against built-in Skill IDs (see `common/organizational-skills.md`) and also recognize skills by name pattern. Common matches include:
   - Database: `db-standards`, `database`, `database-sp`, `database-audit`, `database-modeling`, `database-security`
   - API: `api-standards`, `api-first-spec`, `api-first-backend`, `api-first-frontend`, `api-first-testing`
   - Code: `code-standards`
   - Security: `security-baseline`
   - Any other skill whose name or description relates to technology conventions
2. **Separate skills by enforcement level** (read the `enforcement` field from each skill's YAML frontmatter):
   - **Mandatory skills** (`enforcement: mandatory`): Auto-apply as HARD CONSTRAINTS. Do NOT ask for confirmation.
   - **Optional skills** (`enforcement: optional` or field absent): Present for user confirmation.
3. **For mandatory skills** — inform the user (do NOT ask):
   > "The following mandatory organizational standards are being applied automatically:
   > - [Skill ID]: [brief description of what it covers]
   > - [Skill ID]: [brief description of what it covers]
   > - ...
   >
   > These are fixed standards. You can override specific parts if needed."
4. **For optional skills** — ask the user:
   > "I also found optional organizational skills:
   > - [Skill ID]: [brief description of what it covers]
   > - ...
   >
   > Should I use these as additional standards? You can confirm all, select specific ones, or skip them."
5. If the user confirms optional skills → extract constraints and record as HARD CONSTRAINTS
6. If the user declines optional skills → proceed without them
7. **IMPORTANT**: Even with skills pre-loaded, still ask the full question below to catch any standards NOT covered by skills

**IF** no skills are loaded → proceed directly with the standard question below.

**Ask directly**:

> "Are there pre-established organizational or technology standards for this project? For example:
> - **Programming languages and frameworks** (backend, frontend)
> - **Database** (engine, ORM, access patterns)
> - **Authentication** (SSO, identity provider, token strategy)
> - **Authorization** (permissions system, role management)
> - **Infrastructure** (cloud provider, container platform, CI/CD)
> - **Shared libraries** (internal packages, SDKs, utilities)
> - **Project structure** (archetypes, templates, naming conventions)
> - **Configuration management** (secrets, environment variables, parameter stores)
> - **Logging and monitoring** (observability stack)
>
> If yes, please describe them. If no, technology choices will be evaluated during the process."

**Processing rules**:
- If the user provides standards → Record them in the requirements document under a dedicated **"Organizational Standards"** section. These become **HARD CONSTRAINTS** — all downstream stages (Application Design, NFR Requirements, Code Generation, etc.) MUST respect them without re-asking or suggesting alternatives.
- If the user says "no" or has no standards → Proceed normally. Technology choices remain open for downstream stages to evaluate.
- If the user provides partial standards (e.g., "DB is always SQL Server but frontend is flexible") → Record what is fixed as constraints and what is open as decisions to be made later.

**IMPORTANT**: Do NOT skip this question. Even if the user's initial request mentions specific technologies, confirm whether those are personal preferences or organizational mandates. The distinction matters — preferences can be challenged, mandates cannot.

### Step 5b: Identify Repository Structure

**MANDATORY**: After organizational standards, determine the project's repository structure. This determines whether the project follows a single-repo or multi-repo model, which impacts downstream stages (QA Matrix, HU Guides, Build & Test, E2E orchestration).

#### SKILL CHECK: repo-structure

**IF** `aidlc-state.md` → Organizational Skills section lists a skill with ID `repo-structure`:

1. Load the `repo-structure` skill file content.
2. **DO NOT ask the generic multi-repo question below. Use the skill's question flow EXCLUSIVELY.**
3. Check if the user already provided the project code and/or project type in their initial request:
   - If project code was provided → use it directly, do NOT re-ask.
   - If project type was provided (or can be inferred from the request) → use it directly, do NOT re-ask.
   - If modules were listed (for Micro types) → use them directly, do NOT re-ask.
4. Only ask questions the user has NOT already answered.
5. **PROJECT CODE GATE (MANDATORY)**: Before generating ANY repository names or previews:
   - The project code MUST be explicitly confirmed by the user (either in initial request or via a question).
   - Do NOT infer the project code from the workspace directory path (e.g., `666-02597` is a framework repo number, NOT a project code).
   - If the project code is unknown, ask for it FIRST: "¿Cuál es el código del proyecto? (e.g., 200-034)"
   - Only AFTER the user confirms the project code → generate repository names using that code.
   - If you generate a preview BEFORE the code is confirmed, use `{PROJECT_CODE}` as placeholder.
6. Apply the skill's inference rules to auto-generate the complete repository map.
7. Present the generated map for user confirmation:
   > "Based on the `repo-structure` skill convention, I generated this repository map:
   > [TABLE]
   > Is this correct? You can add, remove, or rename repositories."
8. If the user confirms → record as HARD CONSTRAINT.
9. If the user wants changes → adjust and re-confirm.
10. **SKIP the generic question entirely** — go directly to Step 6.

**ELSE** (no `repo-structure` skill available):

Ask directly:

> "Does this project use multiple repositories? For example:
> - A separate backend API and frontend application
> - An API gateway with domain-specific services
> - A documentation hub where planning happens, with code in other repos
>
> If yes, please list each repository:
>
> | Repo ID | Name/Alias | Role |
> |---------|-----------|------|
> | [e.g., repo-001] | [e.g., Internal API] | [Core API / Domain API / Gateway / Frontend Host / Frontend Domain / Mobile / Documentation Hub] |
>
> If no, or you're unsure, we'll continue with a single-repo approach."

**See `common/multi-repo-architecture.md` for role definitions and architecture combinations.**

**Processing rules** (apply to BOTH paths — skill or manual):
- If the user provides/confirms a repository table → Record it in the requirements document under a dedicated **"Repository Structure"** section. These become **HARD CONSTRAINTS** — all downstream stages (Workflow Planning, QA Matrix, HU Guide Generation, Build & Test) MUST use this repository map. Set project architecture to **Multi-Repo**.
- If the user says "no", is unsure, or has no multi-repo structure → Set project architecture to **Single-Repo**. Multi-repo features (HU Guide Generation, Repo Completion Tracking, cross-repo E2E orchestration) will be skipped.
- If the user provides partial information → Record what is known, mark unknowns for resolution during Workflow Planning.

### Step 6: Thorough Completeness Analysis

**CRITICAL**: Use comprehensive analysis to evaluate requirements completeness. Default to asking questions when there is ANY ambiguity or missing detail.

**MANDATORY**: Evaluate ALL of these areas and ask questions for ANY that are unclear:
- **Functional Requirements**: Core features, user interactions, system behaviors
- **Non-Functional Requirements**: Performance, security, scalability, usability
- **User Scenarios**: Use cases, user journeys, edge cases, error scenarios
- **Business Context**: Goals, constraints, success criteria, stakeholder needs
- **Technical Context**: Integration points, data requirements, system boundaries
- **Quality Attributes**: Reliability, maintainability, testability, accessibility
- **Organizational Standards Gaps**: If standards were provided in Step 5, verify there are no missing details (e.g., user said "we use SSO" but didn't specify which provider)
- **Repository Structure Gaps**: If multi-repo was indicated in Step 5b, verify all repos have IDs and roles assigned. Flag any repos with unclear ownership or missing roles
- **Data Model Gaps**: For every field the user mentions as a "type", "category", "department", "position", "status", or similar classifiable value — determine if it should be a **FK to a catalog table** (normalized) or **free text** (denormalized). If `database-modeling` skill is loaded, default to FK catalog unless the user explicitly says free text. Ask if unclear: "¿[Campo] es un catálogo (tabla maestra con dropdown) o texto libre?"

**When in doubt, ask questions** - incomplete requirements lead to poor implementations.

### Step 7: Generate Clarifying Questions (PROACTIVE APPROACH)
   - **ALWAYS** create `aidlc-docs/inception/requirements/requirement-verification-questions.md` unless requirements are exceptionally clear and complete
   - Ask questions about ANY missing, unclear, or ambiguous areas
   - Focus on functional requirements, non-functional requirements, user scenarios, and business context
   - Request user to fill in all [Answer]: tags directly in the questions document
   - If presenting multiple-choice options for answers:
     - Label the options as A, B, C, D etc.
     - Ensure options are mutually exclusive and don't overlap
     - ALWAYS include option for custom response: "X) Other (please describe after [Answer]: tag below)"
   - Wait for user answers in the document
   - **MANDATORY**: Analyze ALL answers for ambiguities and create follow-up questions if needed
   - **MANDATORY**: Keep asking questions until ALL ambiguities are resolved OR user explicitly asks to proceed

### ⛔ GATE: Await User Answers
DO NOT proceed to Step 8 until all questions in requirement-verification-questions.md are answered and validated.
Present the question file to the user and STOP.

### Step 8: Generate Requirements Document
   - **PREREQUISITE**: Step 7 gate must be passed — all answers received and analyzed
   - Create `aidlc-docs/inception/requirements/requirements.md`
   - Include intent analysis summary at the top:
     - User request
     - Request type
     - Scope estimate
     - Complexity estimate
   - Include **Organizational Standards** section (from Step 5) if provided — clearly marked as HARD CONSTRAINTS
   - Include **Repository Structure** section (from Step 5b) if provided — clearly marked as HARD CONSTRAINTS with repo table [ID | Name | Role] and architecture type (Single-Repo / Multi-Repo)
   - Include both functional and non-functional requirements
   - Incorporate user's answers to clarifying questions
   - Provide brief summary of key requirements

### Step 8a: Generate C4 Architecture Diagrams (Comprehensive Only)

**MANDATORY for Comprehensive depth. SKIP for Minimal and Standard depth.**

Comprehensive depth projects (complex, high-risk, multiple integrations) benefit from visual architecture context. Standard depth projects already capture actors, integrations, and boundaries in text — a diagram would duplicate that information.

**For Standard/Minimal**: Skip this step. Architecture diagrams belong in Application Design where they inform actual design decisions.

**For Comprehensive**: Generate a C4 Level 1 (System Context) diagram embedded in `requirements.md` under an **"Architecture Overview"** section. This helps stakeholders visualize complex system boundaries with 5+ external integrations.

**Validate diagrams** per `common/content-validation.md` Mermaid rules. Always include a text alternative.

#### Mermaid C4 Syntax Reference

Use Mermaid's built-in C4 diagram types — NOT generic flowcharts.

**Available diagram types**: `C4Context`, `C4Container`, `C4Component`, `C4Dynamic`, `C4Deployment`

**Available functions**:

| Function | Purpose |
|---|---|
| `Person(alias, label, description)` | Internal user/actor |
| `Person_Ext(alias, label, description)` | External user/actor |
| `System(alias, label, description)` | The system being built |
| `System_Ext(alias, label, description)` | External system |
| `Container(alias, label, technology, description)` | Container inside system boundary |
| `ContainerDb(alias, label, technology, description)` | Database container |
| `ContainerQueue(alias, label, technology, description)` | Message queue container |
| `Rel(from, to, label, technology)` | Relationship between elements |
| `BiRel(from, to, label, technology)` | Bidirectional relationship |
| `System_Boundary(alias, label)` | System boundary grouping |
| `Container_Boundary(alias, label)` | Container boundary grouping |

#### Diagram Rules

- **Alias IDs**: camelCase, no spaces, no special chars
- **Labels**: User's language for labels, English for alias IDs
- **Scope**: Show ONLY what is in requirements scope
- **Granularity**: 5-15 elements per diagram
- **Relationships**: Verb/action label + technology (`"Autentica"`, `"OIDC"`)
- **Visual references**: If user provided wireframes/screenshots, store in `aidlc-docs/assets/references/`

**Note**: C4 Level 2 (Container) and Level 3 (Component) diagrams belong in Application Design, not here. Requirements Analysis defines WHAT, not HOW the system is structured internally.

### Step 8b: Skill Compliance Gate (MANDATORY)

**BEFORE presenting the requirements for approval**, verify that the generated document uses EXACT identifiers from loaded mandatory skills. This gate prevents cascading failures — wrong names here propagate to API Contract → Backend → Frontend.

**Verification checklist** (for each loaded mandatory skill that defines concrete identifiers):

- [ ] **database-audit**: Audit columns MUST be `RecordCreationUser`, `RecordCreationDate`, `RecordEditUser`, `RecordEditDate`, `RecordStatus`. NOT `CreatedBy`, `CreatedAt`, `UpdatedBy`, `UpdatedAt`, or any other synonym.
- [ ] **database-audit**: RecordStatus MUST be `CHAR(1)` with values `'A'` (Active), `'I'` (Inactive), `'*'` (Deleted). NOT INT, NOT 0/1, NOT boolean.
- [ ] **database-audit**: Soft delete = `RecordStatus = '*'` + filter `RecordStatus = 'A'` in queries. NOT `RecordStatus = 0` or `IsDeleted = true`.
- [ ] **database-modeling**: Table names = singular UpperCamelCase. PK = `{TableName}Id`. FK = `{ReferencedTable}Id`. Dates = `DATETIMEOFFSET(7)`.
- [ ] **database-modeling**: Schema name = the one the USER chose (from questions). Do NOT invent or abbreviate.
- [ ] **happy**: Authentication field = `headerToken.EmployeeId`. NOT `UserCode`, `UserId`, or `UserName`.
- [ ] **repo-structure**: If loaded, project code MUST have been asked. Repository names follow suffix convention.

**If ANY check fails**: Correct the requirements.md BEFORE proceeding. Do NOT present for approval with skill-violating content.

**General rule**: For ANY identifier (column, type, value, parameter, response field) where a loaded skill provides the exact name — the requirements document MUST use that exact name. See `common/skill-resolver.md` → Literal Compliance Rule.

### Step 9: Update State Tracking

Update `aidlc-docs/aidlc-state.md`:

```markdown
## Key Decisions
- **Architecture**: [Single-Repo / Multi-Repo — from Step 5b]
- **Stack**: [Technologies identified from Reverse Engineering or tech.md]

## Stage Progress
### 🔵 INCEPTION PHASE
- [x] Workspace Detection
- [x] Reverse Engineering (if applicable)
- [x] Requirements Analysis
```

### Step 10: Log and Proceed
   - Log approval prompt with timestamp in `aidlc-docs/audit.md`
   - Present completion message in this structure:
     1. **Completion Announcement** (mandatory): Always start with this:

```markdown
# 🔍 Requirements Analysis Complete
```

     2. **AI Summary** (optional): Provide structured bullet-point summary of requirements
        - Format: "Requirements analysis has identified [project type/complexity]:"
        - List key functional requirements (bullet points)
        - List key non-functional requirements (bullet points)
        - Mention architectural considerations or technical decisions if relevant
        - DO NOT include workflow instructions ("please review", "let me know", "proceed to next phase", "before we proceed")
        - Keep factual and content-focused
     3. **Formatted Workflow Message** (mandatory): Always end with this exact format:

```markdown
> **📋 REVIEW REQUIRED:**  
> Please examine the requirements document at: `aidlc-docs/inception/requirements/requirements.md`



> **🚀 WHAT'S NEXT?**
>
> **You may:**
>
> - 🔧 **Request Changes** - Ask for modifications to the requirements if required based on your review
>
> [IF User Stories will be skipped, add this option:]
> - 📝 **Add User Stories** - Choose to include **User Stories** stage (currently skipped based on project simplicity)
>
> - ✅ **Approve & Continue** - Approve requirements and proceed to **[User Stories/Workflow Planning]**

---
```

**Note**: Include the "Add User Stories" option only when User Stories stage will be skipped. Replace [User Stories/Workflow Planning] with the actual next stage name.

   - Wait for explicit user approval before proceeding
   - Record approval response with timestamp
   - Update Requirements Analysis stage complete in aidlc-state.md