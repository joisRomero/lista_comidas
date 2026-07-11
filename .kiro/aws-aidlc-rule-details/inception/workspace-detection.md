# Workspace Detection

**Purpose**: Determine workspace state and check for existing AI-DLC projects

## Step 1: Check for Existing AI-DLC Project

Check if `aidlc-docs/aidlc-state.md` exists:
- **If exists**: Resume from last phase (load context from previous phases)
- **If not exists**: Continue with new project assessment

## Step 2: Scan Workspace for Existing Code

**Determine if workspace has existing code:**
- Scan workspace for source code files (.java, .py, .js, .ts, .jsx, .tsx, .kt, .kts, .scala, .groovy, .go, .rs, .rb, .php, .c, .h, .cpp, .hpp, .cc, .cs, .fs, etc.)
- Check for build files (pom.xml, package.json, build.gradle, etc.)
- Look for project structure indicators
- Identify workspace root directory (NOT aidlc-docs/)

**Record findings:**
```markdown
## Workspace State
- **Existing Code**: [Yes/No]
- **Programming Languages**: [List if found]
- **Build System**: [Maven/Gradle/npm/etc. if found]
- **Project Structure**: [Monolith/Microservices/Library/Empty]
- **Workspace Root**: [Absolute path]
```

## Step 3: Determine Next Phase

**IF workspace is empty (no existing code)**:
- Set flag: `brownfield = false`
- Next phase: Requirements Analysis

**IF workspace has existing code**:
- Set flag: `brownfield = true`
- Check for existing reverse engineering artifacts in `aidlc-docs/inception/reverse-engineering/`
- **IF reverse engineering artifacts exist**: Load them, skip to Requirements Analysis
- **IF no reverse engineering artifacts**: Next phase is Reverse Engineering

## Step 3.5: Scan for Organizational Skills (Optional)

**Purpose**: Discover pre-existing organizational skill files (templates, standards, conventions) that can accelerate downstream stages. This step is non-blocking — if no skills are found, the workflow continues normally.

**See `common/organizational-skills.md` for full documentation of the skills system.**

**Scan locations** (check in order, first match wins):
1. `.kiro/skills/`
2. `.amazonq/skills/`
3. `skills/`

**IF a skills directory is found**:
1. Scan all `.md` files (including subdirectories)
2. Derive Skill ID from the directory name (e.g., `skills/hu-template/SKILL.md` → Skill ID `hu-template`) or filename without extension (e.g., `skills/api-standards.md` → Skill ID `api-standards`)
3. Match discovered Skill IDs against built-in mappings (see `common/organizational-skills.md` → Built-in Skill IDs table)
4. **MANDATORY — Determine enforcement level**: For each discovered skill, determine if it is `mandatory` or `optional`.

   **FAST PATH — Known Mandatory Skills**: These skills have `metadata.enforcement: mandatory` in their YAML frontmatter. If you find any of these Skill IDs, mark them `mandatory` WITHOUT needing to open the file:

   | Skill ID | Mandatory |
   |----------|-----------|
   | `database` | ✅ |
   | `database-audit` | ✅ |
   | `database-modeling` | ✅ |
   | `database-security` | ✅ |
   | `database-sp` | ✅ |
   | `happy` | ✅ |
   | `hu-template` | ✅ |
   | `api-first-spec` | ✅ |
   | `api-first-backend` | ✅ |
   | `api-first-frontend` | ✅ |
   | `api-first-testing` | ✅ |

   **For any skill NOT in the table above**: Read the YAML frontmatter and check `metadata.enforcement`. Default to `optional` if absent.

   **CRITICAL**: Do NOT default all skills to `optional` without checking this table. The 11 skills above are ALWAYS mandatory when present.
5. Record all discovered skills in the `aidlc-state.md` Organizational Skills section (see template below), including the Enforcement column with the ACTUAL value read from each file
6. Log discovery summary: "Found N organizational skill(s): [list of Skill IDs]. M mandatory, K optional."

**IF no skills directory is found**:
- Log: "No organizational skills directory found — continuing with standard workflow"
- Skip silently — no impact on any downstream stage

## Step 4: Create Initial State File

Create `aidlc-docs/aidlc-state.md`:

```markdown
# AI-DLC State Tracking

## Project Information
- **Project Type**: [Greenfield/Brownfield]
- **Start Date**: [ISO timestamp]
- **Current Stage**: INCEPTION - Workspace Detection

## Workspace State
- **Existing Code**: [Yes/No]
- **Reverse Engineering Needed**: [Yes/No]
- **Workspace Root**: [Absolute path]

## Organizational Skills
- **Skills Directory**: [path if found, or "None"]
- **Skills Loaded**:

| Skill ID | File | Matched Stage | Enforcement |
|----------|------|---------------|-------------|
| [e.g., hu-template] | [e.g., skills/hu-template/SKILL.md] | [e.g., User Stories] | [mandatory/optional] |

> **Note**: Organizational Skills are populated during Workspace Detection (Step 3.5). If no skills directory is found, this section reads "None" and all stages use standard behavior. See `common/organizational-skills.md`.

## Repository Structure
- **Architecture**: [Single-Repo / Multi-Repo / Pending]
- **Architecture Combo**: [Monolith Web / Monolith Mobile / Micro Web / Micro Web+Mobile / Custom / N/A]
- **Repository Map** (if Multi-Repo):

| Repo ID | Name/Alias | Role | Status |
|---------|-----------|------|--------|
| [Populated from Requirements Analysis Step 5b] | | | Pending |

> **Note**: Repository Structure is populated during Requirements Analysis (Step 5b). If the user does not provide repo info, Architecture defaults to "Single-Repo" and multi-repo features are skipped.

## Key Decisions (carry forward — DO NOT re-ask)

> Populated progressively as stages complete. On session resumption, treat these as HARD CONSTRAINTS.

- **Architecture**: [Single-Repo / Multi-Repo — populated at Requirements Analysis Step 5b]
- **Stack**: [Populated at Requirements Analysis from tech.md or Reverse Engineering]
- **ISO 27001 Depth**: [Minimal / Standard / Comprehensive — populated at ISO 27001 Assessment]
- **Request Type**: [New Feature / Enhancement / Bugfix / Migration — populated at Workflow Planning]
- **Scope**: [Small / Medium / Large — populated at Workflow Planning]
- **Stages Profile**: [N of 33 EXECUTE — populated at Workflow Planning]

## Code Location Rules
- **Application Code**: Workspace root (NEVER in aidlc-docs/)
- **Documentation**: aidlc-docs/ only
- **Structure patterns**: See code-generation.md Critical Rules

## Stage Progress

### 🔵 INCEPTION PHASE
- [x] Workspace Detection
- [ ] Reverse Engineering (if applicable)
- [ ] Requirements Analysis
- [ ] User Stories (if applicable)
- [ ] ISO 27001 Assessment
- [ ] Spike/POC (if applicable)
- [ ] API Contract Design (if applicable)
- [ ] Architecture Decision Records (if applicable)
- [ ] Workflow Planning
- [ ] Application Design (if applicable)
- [ ] QA Matrix Generation
- [ ] Units Generation (if applicable)
- [ ] Definition of Ready (GATE)

### 🟢 CONSTRUCTION PHASE
- [ ] Dependency Review (if applicable)
- [ ] HU Guide Generation (if multi-repo)
- [ ] Functional Design (per unit)
- [ ] NFR Requirements (if applicable)
- [ ] NFR Design (if applicable)
- [ ] Infrastructure Design (if applicable)
- [ ] Code Generation
- [ ] Code Review
- [ ] Build and Test

### 🟡 OPERATIONS PHASE
- [ ] Release Documentation (if applicable)
- [ ] Operations (placeholder)

### 🟣 CLOSURE PHASE
- [ ] Project Snapshot
- [ ] Version & Archive
- [ ] Stakeholder Sign-off (if applicable)
- [ ] Project Handoff (if applicable)

### 🔄 CHANGE MANAGEMENT (if re-entering closed project)
- [ ] Re-Onboarding
- [ ] Change Request
- [ ] Impact Analysis
```

## Step 5: Present Completion Message

**For Brownfield Projects:**
```markdown
# 🔍 Workspace Detection Complete

Workspace analysis findings:
• **Project Type**: Brownfield project
• [AI-generated summary of workspace findings in bullet points]
• **Next Step**: Proceeding to **Reverse Engineering** to analyze existing codebase...
```

**For Greenfield Projects:**
```markdown
# 🔍 Workspace Detection Complete

Workspace analysis findings:
• **Project Type**: Greenfield project
• **Next Step**: Proceeding to **Requirements Analysis**...
```

## Step 6: Automatically Proceed

- **No user approval required** - this is informational only
- Automatically proceed to next phase:
  - **Brownfield**: Reverse Engineering (if no existing artifacts) or Requirements Analysis (if artifacts exist)
  - **Greenfield**: Requirements Analysis
