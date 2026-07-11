# Change Request - Detailed Steps

## Purpose
**Document and formalize requested changes to a previously delivered project**

Change Request focuses on:
- Capturing complete details of the requested change
- Documenting business justification and urgency
- Establishing scope boundaries for the change
- Creating traceable record of change requests

**Note**: This stage documents WHAT is being requested. Impact Analysis determines HOW to handle it.

## Prerequisites
- Re-Onboarding must be complete
- Project context has been loaded
- Change request has been received from stakeholder

---

## Step-by-Step Execution

### Step 1: Gather Request Information
- [ ] Interview requestor or review change request submission
- [ ] Clarify any ambiguous aspects of the request
- [ ] Understand business context and urgency
- [ ] Identify stakeholders affected by the change

### Step 2: Classify Change Type
Determine the type of change:
- [ ] **Feature Addition**: New functionality
- [ ] **Feature Modification**: Change to existing functionality
- [ ] **Bug Fix**: Correction of defect
- [ ] **Enhancement**: Improvement to existing feature
- [ ] **Technical**: Refactoring, upgrade, or technical improvement
- [ ] **Regulatory/Compliance**: Required by external mandate

### Step 3: Determine Urgency
- [ ] **Critical**: Business-stopping, immediate attention required
- [ ] **High**: Significant impact, needs priority handling
- [ ] **Medium**: Important but can be scheduled normally
- [ ] **Low**: Nice to have, can wait for next major release

### Step 4: Create Change Request Document
- [ ] Create `aidlc-docs/change-management/CR-[NNN]-[brief-name].md`:

```markdown
# Change Request: CR-[NNN]

## Request Information
- **CR Number**: CR-[NNN]
- **Title**: [Descriptive title]
- **Requested By**: [Name/Role]
- **Request Date**: [YYYY-MM-DD]
- **Target Version**: [X.Y.Z or TBD]

## Classification
- **Type**: [Feature Addition / Modification / Bug Fix / Enhancement / Technical / Compliance]
- **Urgency**: [Critical / High / Medium / Low]
- **Priority**: [To be determined after Impact Analysis]

## Change Description

### Summary
[2-3 sentence summary of the requested change]

### Detailed Description
[Full description of what is being requested]

### Business Justification
[Why is this change needed? What business problem does it solve?]

### Expected Outcome
[What should the system do after this change is implemented?]

## Scope

### In Scope
- [Item 1]
- [Item 2]
- [Item 3]

### Out of Scope
- [Item 1]
- [Item 2]

### Affected Areas (Initial Assessment)
- [ ] Backend/API
- [ ] Frontend/UI
- [ ] Database
- [ ] Infrastructure
- [ ] Configuration
- [ ] Documentation
- [ ] Other: [specify]

## Stakeholders
| Stakeholder | Role | Interest |
|-------------|------|----------|
| [name] | [role] | [interest in this change] |

## Constraints
| Constraint | Description |
|------------|-------------|
| Timeline | [any deadline requirements] |
| Budget | [any budget constraints] |
| Technical | [any technical constraints] |
| Regulatory | [any compliance requirements] |

## Attachments/References
- [Link or reference to supporting materials]

## Request Status
- **Status**: [Submitted / Under Review / Approved / Rejected / Deferred]
- **Reviewed By**: [Name]
- **Review Date**: [YYYY-MM-DD]

## Notes
[Additional notes or context]
```

### Step 5: Generate Clarifying Questions
If information is incomplete:
- EMBED questions using [Answer]: tag format
- Focus on scope, constraints, and acceptance criteria
- Clarify ambiguous requirements

**Question categories**:
- **Scope Clarification** - Exact boundaries of the change
- **Acceptance Criteria** - How do we know it's done correctly?
- **Dependencies** - Other systems or features affected?
- **Constraints** - Timeline, budget, technical limitations?
- **Testing** - How should this be validated?

### Step 6: Request User Input
- [ ] Present clarifying questions to requestor
- [ ] Collect answers using [Answer]: tags
- [ ] Update CR document with responses
- [ ] Validate understanding with requestor

### Step 7: Validate CR Completeness
- [ ] All required sections are complete
- [ ] No ambiguous language remains
- [ ] Scope boundaries are clear
- [ ] Business justification is documented

### Step 8: Log Change Request
- [ ] Log CR submission with timestamp in `aidlc-docs/audit.md`
- [ ] Include CR number and summary
- [ ] Use ISO 8601 timestamp format

### Step 9: Present Completion Message

```markdown
# 📝 Change Request Documented

**CR-[NNN]: [Title]**

[AI-generated summary of change request in bullet points]

> **📋 CHANGE REQUEST:**  
> Please examine the CR at: `aidlc-docs/change-management/CR-[NNN]-[name].md`
>
> **Summary:**
> - Type: [type]
> - Urgency: [urgency]
> - Requested By: [name]



> **🚀 WHAT'S NEXT?**
>
> - ✅ **Proceed to Impact Analysis** - Assess impact and determine implementation path

---
```

### Step 10: Update Progress
- [ ] Mark Change Request complete in `aidlc-docs/aidlc-state.md`
- [ ] Proceed to Impact Analysis stage

---

## Critical Rules

### Complete Documentation
- All changes must have formal CR document
- No implementation without documented CR
- Verbal requests must be documented

### Clear Scope
- Scope must have explicit boundaries
- Out of scope items must be documented
- Avoid scope ambiguity

### Traceability
- Each CR has unique identifier
- CR links to implementation artifacts later
- Changes are traceable to original request

## Change Request Numbering
- Use sequential numbering: CR-001, CR-002, etc.
- Include brief name in filename for identification
- Example: `CR-001-add-payment-method.md`
