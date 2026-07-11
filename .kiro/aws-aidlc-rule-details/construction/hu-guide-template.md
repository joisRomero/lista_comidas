# HU Guide Template

**Purpose**: Define the template for generating self-contained HU (User Story) Guides for distribution to code repositories.

## Overview

In multi-repo architectures, implementation is guided by self-contained HU Guides. Each guide provides all the context, requirements, and technical specifications needed to implement a specific User Story (HU) within a target repository, without requiring access to the Documentation Hub.

For more details on the multi-repo model, see `common/multi-repo-architecture.md`.

## Prerequisites

- API Contract Design must be complete for the relevant endpoints.
- User Stories (HUs) must be defined and prioritized.
- Target repository roles must be identified.

---

# HU GUIDE TEMPLATE

Each generated guide must follow this structure:

### HU Context
- **User Story**: [Text of the HU]
- **Acceptance Criteria**: [List of ACs]
- **Priority**: [High/Medium/Low]

### API Spec Subset
- [Only the endpoints, schemas, and contracts relevant to THIS HU in THIS repository]

### ISO 27001 Controls
- [Applicable security controls identified during assessment, if any]

### Implementation Checklist
- [ ] Task 1: [Description]
- [ ] Task 2: [Description]
- [ ] ...

### Applicable Skills
- [Slot for project-specific development skills. To be filled at runtime by the agent.]

### Unit Test Requirements
- **Test Cases**: [List of required tests]
- **Coverage Expectations**: [e.g., 80% line coverage, all edge cases]

### Code Review Checklist
- [ ] [Standard review item]
- [ ] [HU-specific review item]

### PR Template
- **Description**: [Standard description linking back to the HU ID]
- **Changes**: [List of changes]
- **Verification**: [How to verify the changes]

### Traceability
- **HU ID**: [ID]
- **API Endpoints**: [List of endpoints]
- **QA Test Case IDs**: [List of related test cases]

---

## Step-by-Step Execution

### Step 1: Analyze HU and Repo Context
- [ ] Load HU-Repo Distribution Map from `aidlc-docs/inception/plans/hu-repo-distribution.md` — this provides the pre-mapped list of which repos each HU impacts (generated during Workflow Planning Step 5b).
- [ ] For each HU, read the Distribution Matrix to identify target repositories and their roles.
- [ ] Extract the specific requirements and API contracts for each target repository.

### Step 2: Generate HU Guides
- [ ] Create a separate HU Guide for each repository involved in the HU.
- [ ] Ensure each guide is self-contained with all necessary context.
- [ ] Use the template structure defined above.
- [ ] Include actionable checkboxes for all implementation tasks.

### Step 3: Save and Distribute
- [ ] Save generated guides to: `aidlc-docs/construction/{hu-id}/guides/{repo-role}-guide.md`
- [ ] Notify the user that guides are ready for manual distribution to target repositories.

## Generation Rules

- **One Guide Per Repo**: If an HU spans multiple repositories, generate one specific guide for each repository containing only its relevant portion.
- **Self-Contained**: Include ALL context needed for implementation. Do not reference external files located in the Documentation Hub.
- **Actionable**: Every implementation task must have a checkbox `[ ]`.
- **Agnostic**: Do not reference specific technology stacks unless defined in the project's NFR Design.
- **Format**: Use standard Markdown. Avoid Unicode box-drawing characters.

## Completion Message

Once the HU Guides are generated, present the following message:

```markdown
# 📄 HU Guides Generated - [HU-ID]

## Summary
- **HU**: [HU Title]
- **Target Repositories**: [List of repo roles]
- **Location**: `aidlc-docs/construction/[hu-id]/guides/`

> **📋 DISTRIBUTION REQUIRED:**  
> Please manually copy the generated guides to their respective target repositories.

> **🚀 WHAT'S NEXT?**
>
> **You may:**
>
> - 🔧 **Request Changes** - Modify the generated guides
> - ✅ **Continue** - Proceed to implementation in code repositories
```

## Critical Rules

- **No External References**: Guides must not point to files in the Doc Hub that won't be present in the code repo.
- **Manual Distribution**: Distribution is manual; do not attempt to automate via scripts or symlinks.
- **Traceability**: Always maintain the link between HU ID, API endpoints, and QA test cases.
