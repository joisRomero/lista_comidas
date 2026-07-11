# Spike/POC - Detailed Steps

## Purpose
**Technical investigation to reduce uncertainty before committing to a solution**

Spike/POC focuses on:
- Exploring technical feasibility of proposed solutions
- Validating assumptions about technologies, integrations, or approaches
- Reducing risk by proving concepts before full implementation
- Time-boxed investigation with clear success criteria

**Note**: Spikes are exploratory and may result in throwaway code. The goal is learning, not production-ready artifacts.

## Prerequisites
- Requirements Analysis must be complete
- Technical uncertainty or risk has been identified
- Spike scope and time-box have been defined

## Intelligent Assessment Guidelines

**WHEN TO EXECUTE SPIKE/POC**: Use this assessment before proceeding:

### Execute Spike IF:
- New technology or framework being introduced
- Integration with unfamiliar external systems
- Performance requirements with unknown feasibility
- Multiple architectural approaches under consideration
- High-risk technical decisions with limited team experience
- Third-party API or service behavior needs validation

### Skip Spike IF:
- Team has prior experience with the technology
- Standard patterns with well-documented solutions
- Low-risk changes within established architecture
- Clear, proven implementation path exists

---

## Step-by-Step Execution

### Step 1: Define Spike Scope
- [ ] Identify the specific technical question to answer
- [ ] Define clear success criteria (what proves feasibility?)
- [ ] Set time-box duration (typically 1-3 days)
- [ ] Document what is OUT of scope for this spike

### Step 2: Create Spike Plan
- [ ] Generate spike plan with checkboxes for investigation steps
- [ ] Include specific experiments or prototypes to build
- [ ] Define expected deliverables (findings document, prototype, decision)
- [ ] Save plan as `aidlc-docs/inception/plans/spike-plan.md`

### Step 3: Generate Investigation Questions
**DIRECTIVE**: Focus on the specific technical uncertainty being investigated.

- EMBED questions using [Answer]: tag format
- Focus on clarifying success criteria and constraints
- Identify any dependencies or access requirements

**Question categories** (as applicable):
- **Technology Selection** - Which options to evaluate?
- **Integration Requirements** - What systems to connect?
- **Performance Criteria** - What benchmarks to achieve?
- **Constraints** - Time, resources, or technical limitations?

### Step 4: Request User Input
- [ ] Ask user to fill [Answer]: tags in the spike plan
- [ ] Clarify any ambiguous success criteria
- [ ] Confirm time-box and resource allocation

### Step 5: Execute Investigation
- [ ] Build minimal prototype or proof of concept
- [ ] Document findings as you progress
- [ ] Track time spent against time-box
- [ ] Note blockers, surprises, and learnings

### Step 6: Document Findings
- [ ] Create `aidlc-docs/inception/spike/spike-findings.md` with:
  - Original question and success criteria
  - Approach taken
  - Results and observations
  - Recommendation (proceed, pivot, or abandon)
  - Risks and considerations discovered
  - Estimated effort for full implementation

### Step 7: Log Approval Prompt
- [ ] Log approval prompt with timestamp in `aidlc-docs/audit.md`
- [ ] Include reference to spike findings
- [ ] Use ISO 8601 timestamp format

### Step 8: Present Completion Message

```markdown
# 🔬 Spike/POC Complete

[AI-generated summary of spike findings and recommendation in bullet points]

> **📋 REVIEW REQUIRED:**  
> Please examine the spike findings at: `aidlc-docs/inception/spike/spike-findings.md`



> **🚀 WHAT'S NEXT?**
>
> **Based on spike results, you may:**
>
> - ✅ **Proceed with Recommended Approach** - Continue to Application Design with validated approach
> - 🔄 **Pivot** - Investigate alternative approach based on findings
> ⛔ **Reassess Requirements** - Findings suggest requirements need revision

---
```

### Step 9: Wait for Explicit Approval
- [ ] Do not proceed until user explicitly approves the spike outcome
- [ ] If user requests additional investigation, extend or create new spike
- [ ] Document decision in audit.md

### Step 10: Update Progress
- [ ] Mark Spike/POC stage complete in `aidlc-docs/aidlc-state.md`
- [ ] Update the "Current Status" section
- [ ] Carry forward learnings to subsequent stages

---

## Critical Rules

### Time-Box Enforcement
- Spikes must have defined end time
- If time-box expires without conclusion, document partial findings
- Never let spikes expand indefinitely

### Throwaway Code Policy
- Spike code is for learning, not production
- Do not refactor spike code into production - rewrite with proper design
- Keep spike prototypes in separate directory or branch

### Documentation Requirements
- All spikes must produce findings document
- Negative results are valuable - document what doesn't work
- Include enough detail for future reference
