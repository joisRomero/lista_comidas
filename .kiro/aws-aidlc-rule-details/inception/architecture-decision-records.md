# Architecture Decision Records (ADRs) - Detailed Steps

## Purpose
**Document significant architectural decisions and their rationale**

Architecture Decision Records focus on:
- Capturing WHY decisions were made, not just WHAT was decided
- Preserving context for future team members or project resumption
- Tracking alternatives considered and trade-offs evaluated
- Creating an audit trail of architectural evolution

**Note**: ADRs are living documents. Decisions can be superseded but original records are preserved.

## Prerequisites
- Requirements Analysis should be complete
- Application Design may trigger additional ADRs
- Significant technical decisions have been identified

## Intelligent Assessment Guidelines

**WHEN TO CREATE ADRs**: Record decisions that:

### Require ADR:
- Affect multiple components or system boundaries
- Involve technology selection (frameworks, databases, cloud services)
- Are difficult or expensive to change later
- Involve trade-offs between competing concerns
- Deviate from established patterns or standards
- Have long-term implications for the system

### Skip ADR:
- Trivial implementation details
- Decisions easily reversible
- Standard patterns already documented elsewhere
- Personal coding style preferences

---

## Step-by-Step Execution

### Step 1: Identify Decisions Requiring Documentation
- [ ] Review requirements, design, and spike findings
- [ ] List decisions that meet ADR criteria
- [ ] Prioritize based on impact and irreversibility
- [ ] Create initial decision inventory

### Step 2: Create ADR Plan
- [ ] Generate plan with checkboxes for each ADR to create
- [ ] Include context gathering and review steps
- [ ] Save plan as `aidlc-docs/inception/plans/adr-plan.md`

### Step 3: Generate Context-Appropriate Questions
**DIRECTIVE**: Focus on capturing decision context and stakeholder input.

- EMBED questions using [Answer]: tag format
- Focus on constraints, priorities, and trade-off preferences

**Question categories** (as applicable):
- **Context** - What problem are we solving? What constraints exist?
- **Options** - What alternatives should be considered?
- **Criteria** - How should we evaluate options?
- **Stakeholders** - Who should be involved in this decision?

### Step 4: Request User Input
- [ ] Ask user to fill [Answer]: tags for decision context
- [ ] Gather input on evaluation criteria
- [ ] Identify decision-makers and stakeholders

### Step 5: Create ADR Directory Structure
- [ ] Create `aidlc-docs/inception/adrs/` directory
- [ ] Establish numbering convention (ADR-001, ADR-002, etc.)
- [ ] Create index file `aidlc-docs/inception/adrs/README.md`

### Step 6: Generate Individual ADRs
For each significant decision, create ADR following this template:

```markdown
# ADR-[NNN]: [Decision Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Date
[YYYY-MM-DD]

## Context
[Describe the situation and problem that requires a decision.
Include relevant constraints, requirements, and forces at play.]

## Decision
[State the decision clearly and concisely.
Start with "We will..." or "We have decided to..."]

## Alternatives Considered

### Option 1: [Name]
- **Description**: [Brief description]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]

### Option 2: [Name]
- **Description**: [Brief description]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]

[Additional options as needed]

## Rationale
[Explain WHY this decision was made over alternatives.
Reference specific criteria, constraints, or priorities.]

## Consequences

### Positive
- [Expected benefits]

### Negative
- [Known trade-offs or risks]

### Neutral
- [Other implications]

## Related Decisions
- [Links to related ADRs if any]

## References
- [Links to relevant documentation, research, or standards]
```

### Step 7: Create ADR Index
- [ ] Update `aidlc-docs/inception/adrs/README.md` with:
  - List of all ADRs with status
  - Quick reference table
  - Decision timeline

### Step 8: Log Approval Prompt
- [ ] Log approval prompt with timestamp in `aidlc-docs/audit.md`
- [ ] Include reference to ADRs created
- [ ] Use ISO 8601 timestamp format

### Step 9: Present Completion Message

```markdown
# 📋 Architecture Decision Records Complete

[AI-generated summary of ADRs created in bullet points]

> **📋 REVIEW REQUIRED:**  
> Please examine the Architecture Decision Records at: `aidlc-docs/inception/adrs/`



> **🚀 WHAT'S NEXT?**
>
> **You may:**
>
> - 🔧 **Request Changes** - Revise decisions or add alternatives
> ➕ **Add More ADRs** - Document additional decisions
> - ✅ **Approve & Continue** - Accept decisions and proceed to **[next stage]**

---
```

### Step 10: Wait for Explicit Approval
- [ ] Do not proceed until user explicitly approves ADRs
- [ ] If changes requested, update ADRs and repeat approval
- [ ] Document approval in audit.md

### Step 11: Update Progress
- [ ] Mark ADR stage complete in `aidlc-docs/aidlc-state.md`
- [ ] Update the "Current Status" section
- [ ] ADRs remain living documents throughout project

---

## Critical Rules

### Immutability Principle
- Never delete or modify accepted ADRs
- Supersede with new ADR if decision changes
- Preserve historical context

### Documentation Standards
- Use consistent numbering (ADR-001, ADR-002)
- Include date for all status changes
- Link related ADRs explicitly

### Content Requirements
- Always include alternatives considered
- Always explain rationale (WHY, not just WHAT)
- Document both positive and negative consequences

### Ongoing Maintenance
- Review ADRs when resuming projects
- Create new ADRs for significant changes during construction
- Reference ADRs in related documentation

## ADR Lifecycle

```
Proposed → Accepted → [Active]
                   ↓
            Deprecated (no longer applies)
                   or
            Superseded (replaced by new ADR)
```
