# Definition of Ready - Detailed Steps

## Purpose
**Gate that validates all prerequisites are met before entering Construction phase**

Definition of Ready focuses on:
- Ensuring requirements are clear, complete, and unambiguous
- Validating that design artifacts are sufficient for implementation
- Confirming dependencies are identified and resolved
- Providing a quality gate between planning and execution

**Note**: This is a checkpoint, not a lengthy stage. It validates completeness and identifies gaps.

## Prerequisites
- Requirements Analysis must be complete
- All applicable INCEPTION stages must be complete
- Workflow Planning must indicate Definition of Ready should execute

## Definition of Ready Checklist

The following criteria must be validated before proceeding to CONSTRUCTION:

### Requirements Readiness
- [ ] All requirements are documented and approved
- [ ] Acceptance criteria are defined for each requirement
- [ ] No open questions or ambiguities in requirements
- [ ] Non-functional requirements are specified (if applicable)

### User Stories Readiness (if applicable)
- [ ] User stories follow agreed format
- [ ] Each story has clear acceptance criteria
- [ ] Stories are appropriately sized for implementation
- [ ] Story dependencies are identified

### Design Readiness
- [ ] Application design is complete and approved
- [ ] Component boundaries are clearly defined
- [ ] API contracts are specified (if applicable)
- [ ] Architecture decisions are documented (ADRs)
- [ ] Multi-repo architecture identified (if applicable): repo roles assigned, architecture combination selected (see common/multi-repo-architecture.md)
- [ ] HU-Repo Distribution Map complete (if multi-repo): all HUs mapped to target repositories (`aidlc-docs/inception/plans/hu-repo-distribution.md`)
- [ ] API contracts ready for QA Matrix generation (if API project)
- [ ] Authorization Matrix generated (if API project) — screens, endpoints, actions, roles mapped from openapi.yaml + user stories (`aidlc-docs/inception/authorization-matrix.md`)
- [x] QA Matrix Generation complete — traceability table, E2E flows, test data catalog

### Technical Readiness
- [ ] Technical uncertainties resolved (spikes completed)
- [ ] Technology stack is defined
- [ ] Development environment requirements are documented
- [ ] Third-party dependencies are identified
- [ ] ISO 27001 Assessment completed (if project handles sensitive data, verify assessment depth was appropriate)
- [ ] Repository structure confirmed (single-repo or multi-repo with repo map in aidlc-state.md)
- [ ] QA Matrix generated with full traceability coverage

### Dependencies Readiness
- [ ] External dependencies are identified
- [ ] Integration points are documented
- [ ] Access to required systems/services is confirmed
- [ ] Data requirements are specified

---

## Step-by-Step Execution

### Step 1: Load INCEPTION Artifacts
- [ ] Read all completed INCEPTION phase artifacts
- [ ] Create checklist of available documentation
- [ ] Identify which optional stages were executed

### Step 2: Evaluate Readiness Criteria
- [ ] Check each applicable criterion from the checklist above
- [ ] Document status of each criterion (Ready / Not Ready / N/A)
- [ ] Identify gaps or missing items

### Step 2b: Cross-Stage Consistency Checks (if applicable stages were executed)
- [ ] **Error codes**: Every error code in `stories.md` (VAL_xxx, BUS_xxx) exists in `requirements.md`. Every error code in `api-summary.md` exists in both `stories.md` and `requirements.md`. No orphan codes.
- [ ] **Endpoints ↔ FRs**: Every functional requirement that implies an API operation has a matching endpoint in `openapi.yaml`. No orphan FRs.
- [ ] **HUs ↔ Endpoints**: Every User Story maps to at least one endpoint (or is UI-only with justification). No orphan stories.
- [ ] **ISO controls ↔ Summary**: If ISO 27001 was executed, every category in the compliance summary appears in the assessment body. No phantom entries.
- [ ] **Prototypes ↔ Stories**: If Prototyping was executed, every screen in the prototypes maps to at least one User Story.
- [ ] If ANY inconsistency is found: document it as a gap and present to user in Step 4.

### Step 3: Create Readiness Assessment
- [ ] Create `aidlc-docs/inception/definition-of-ready.md` with:
  - Summary of INCEPTION stages completed
  - Readiness checklist with status
  - List of any gaps or blockers
  - Recommendation (Ready / Not Ready)

### Step 4: Handle Gaps (if any)
If gaps are identified:
- [ ] Document specific gaps and their impact
- [ ] Determine remediation path for each gap
- [ ] Present options to user:
  - Return to relevant INCEPTION stage to address gap
  - Accept gap with documented risk
  - Defer gap to be addressed during CONSTRUCTION (if minor)

### Step 5: Generate Readiness Questions (if needed)
If clarification is needed:
- EMBED questions using [Answer]: tag format
- Focus on resolving blockers or validating assumptions

### Step 6: Log Assessment
- [ ] Log readiness assessment with timestamp in `aidlc-docs/audit.md`
- [ ] Include complete checklist results
- [ ] Document any accepted risks or deferrals

### Step 7: Present Completion Message

**If READY:**
```markdown
# ✅ Definition of Ready - PASSED

[AI-generated summary of readiness assessment in bullet points]

> **📋 ASSESSMENT COMPLETE:**  
> All readiness criteria have been met. See: `aidlc-docs/inception/definition-of-ready.md`



> **🚀 READY FOR CONSTRUCTION**
>
> All prerequisites for CONSTRUCTION phase are satisfied.
>
> - ✅ **Proceed to CONSTRUCTION** - Begin with first unit design/implementation

---
```

**If NOT READY:**
```markdown
# ⚠️ Definition of Ready - GAPS IDENTIFIED

[AI-generated summary of gaps found in bullet points]

> **📋 GAPS IDENTIFIED:**  
> The following items need attention before proceeding:
> [List of specific gaps]



> **🚀 OPTIONS:**
>
> - 🔄 **Address Gaps** - Return to [specific stage] to resolve gaps
> ⚠️ **Accept Risk** - Proceed with documented risks (not recommended)
> ❌ **Pause** - Stop and reassess project scope

---
```

### Step 8: Wait for Explicit Decision
- [ ] Do not proceed until user explicitly confirms readiness
- [ ] If returning to address gaps, update audit.md
- [ ] If accepting risks, document explicitly in audit.md

### Step 9: Update Progress
- [ ] Mark Definition of Ready complete in `aidlc-docs/aidlc-state.md`
- [ ] Update the "Current Status" section
- [ ] If ready, transition to CONSTRUCTION phase

---

## Critical Rules

### Gate Enforcement
- This is a mandatory checkpoint before CONSTRUCTION
- Cannot be skipped even for simple projects
- Gaps must be explicitly addressed or accepted

### Documentation Requirements
- All readiness decisions must be documented
- Accepted risks must be explicitly recorded
- Readiness assessment becomes part of project record

### Lightweight Execution
- This is a validation checkpoint, not a lengthy stage
- Focus on checklist verification, not new artifact creation
- Should complete quickly if INCEPTION was thorough

## Readiness Summary Template

```markdown
# Definition of Ready Assessment

## Date
[YYYY-MM-DD]

## INCEPTION Stages Completed
- [x] Workspace Detection
- [x] Requirements Analysis
- [ ] Reverse Engineering (N/A - Greenfield)
- [x] User Stories
- [x] Application Design
- [x] API Contract Design
- [x] Architecture Decision Records
- [x] Workflow Planning

## Readiness Checklist

| Category | Criterion | Status | Notes |
|----------|-----------|--------|-------|
| Requirements | All requirements documented | ✅ Ready | |
| Requirements | Acceptance criteria defined | ✅ Ready | |
| Design | Application design approved | ✅ Ready | |
| Design | API contracts specified | ✅ Ready | |
| Technical | Spikes completed | ✅ Ready | |
| Dependencies | External deps identified | ✅ Ready | |

## Gaps Identified
[None | List of gaps]

## Risks Accepted
[None | List of accepted risks]

## Recommendation
**[READY TO PROCEED | NOT READY - Address Gaps]**

## Approvals
- [ ] Technical Lead: ___
- [ ] Product Owner: ___
```
