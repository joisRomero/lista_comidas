# Code Review - Detailed Steps

## Purpose
**Systematic review of code changes before integration**

Code Review focuses on:
- Ensuring code quality and adherence to standards
- Identifying defects, security issues, and design problems early
- Knowledge sharing across team members
- Validating implementation matches requirements and design

**Note**: This stage executes after Code Generation, before Build & Test for each unit.

## Prerequisites
- Code Generation must be complete for the unit
- Code is ready for review (not work-in-progress)
- Reviewer context is available (design docs, requirements)

## Review Scope

Code review should evaluate:

### Functional Correctness
- [ ] Code implements requirements correctly
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] Business logic matches design specifications

### Code Quality
- [ ] Code follows project coding standards
- [ ] Code is readable and maintainable
- [ ] Functions/methods have single responsibility
- [ ] No code duplication (DRY principle)
- [ ] Appropriate naming conventions used

### Security (Checklist)
- [ ] No hardcoded secrets or credentials
- [ ] Input validation implemented
- [ ] Output encoding for XSS prevention
- [ ] SQL injection prevention (parameterized queries)
- [ ] Authentication/authorization properly implemented
- [ ] Sensitive data handled appropriately
- [ ] Verify compliance with ISO 27001 controls identified in Inception assessment (if applicable)
- [ ] Validate implementation matches HU Guide acceptance criteria and traceability requirements

### Performance
- [ ] No obvious performance anti-patterns
- [ ] Database queries are optimized
- [ ] Appropriate caching considered
- [ ] Resource cleanup (connections, files, memory)

### Testing
- [ ] Unit tests cover new functionality
- [ ] Test cases are meaningful (not just coverage)
- [ ] Edge cases tested
- [ ] Tests are maintainable

---

## Step-by-Step Execution

### Step 1: Prepare Review Context
- [ ] Gather relevant design documents for the unit
- [ ] Review requirements and user stories being implemented
- [ ] Understand scope of changes
- [ ] Identify files changed and their purpose

### Step 2: Create Review Checklist
- [ ] Generate unit-specific review checklist based on scope
- [ ] Include standard review criteria (above)
- [ ] Add context-specific items based on unit type:
  - API endpoints: Request validation, response formats, error codes
  - Data access: Query safety, transaction handling
  - UI components: Accessibility, responsiveness
  - Security modules: Authentication flows, encryption

### Step 3: Code Gen Plan Completeness Check (MANDATORY)

**BEFORE reviewing code quality**, verify the Code Gen Plan is fully executed:

- [ ] Open the Code Gen Plan from `aidlc-docs/construction/plans/{unit-name}-code-generation-plan.md`
- [ ] Check EVERY checkbox in the plan:
  - For each `[x]` item → verify the corresponding file EXISTS in the workspace (not just claimed complete)
  - For each `[ ]` item → this is an INCOMPLETE delivery. Flag as **Critical Issue**: "Code Gen Plan item not completed: [item description]"
- [ ] **Scaffolding completeness**: Cross-reference the Mandatory Scaffolding Checklist (see code-generation.md). For each required scaffolding file, verify it exists
- [ ] **Per-layer QA evidence**: Verify `aidlc-docs/audit.md` contains QA results (build output, lint summary) for each layer. If missing → flag as **Critical Issue**: "No QA evidence for [layer] layer"
- [ ] **If ANY plan item is `[ ]` (unchecked)**: Code Review verdict MUST be "Changes Required" or "Rejected". Do NOT approve incomplete deliveries

### Step 3b: Pre-Review Validator Check (Core Library v1.5.5)

**Run ALL applicable validators before starting the code review.** Convention errors must be fixed before human/AI review — reviewers should focus on logic, security, and architecture.

- [ ] Run `python config/validators/runner.py --all --report {project_path}`
- [ ] Review the generated `validator-report.json`:
  - If ERRORS remain → return to Code Generation to fix. Do NOT start review with known validator errors
  - If only WARNINGS → note them for the reviewer but proceed
- [ ] Inject the Validator Report into the reviewer's context:
  - **Standard review**: Reviewer reads report before examining code
  - **Judgment Day (v1.6.0)**: Both judges receive the report (see judgment-day skill)
- [ ] Reviewers **SKIP** convention checks that validators already cover (naming, audit columns, response shapes, file structure, QUOTENAME, `any` usage). Focus on:
  - Business logic correctness and edge cases
  - Security vulnerabilities and data exposure
  - Architecture alignment and design patterns
  - Performance implications
  - Validator WARNINGS as potential logic/security hints

### Step 3c: Risk Assessment — Judgment Day Trigger

Evaluate if this unit requires adversarial review:

| Signal | Threshold |
|--------|-----------|
| Files changed | >10 files |
| Auth/security modules | Any file in auth, security, or authorization layers |
| New API write endpoints | POST/PUT/DELETE operations added |
| Database schema changes | New tables, column modifications |
| Multi-repo gateway changes | Ocelot routing, gateway config |
| Critical issues from Step 3 | Code Gen Plan flagged critical items |

**IF any signal is TRUE** → Load `judgment-day` skill and execute Judgment Day Protocol (2 blind judges, verdict synthesis, fix loop). Append results to the Code Review Report (Step 5).

**IF no signal is TRUE** → Proceed with standard review (Step 4).

### Step 4: Execute Code Review
- [ ] Review each changed file systematically
- [ ] Document findings with:
  - File and line reference
  - Issue description
  - Severity (Critical, Major, Minor, Suggestion)
  - Recommended fix
- [ ] Note positive aspects (good patterns, clever solutions)
- [ ] If Judgment Day was executed (Step 3c), merge JD findings into this review

### Step 5: Generate Review Report
- [ ] Create `aidlc-docs/construction/{unit-name}/code-review-report.md` with:

```markdown
# Code Review Report - [Unit Name]

## Review Date
[YYYY-MM-DD]

## Reviewer
[AI-DLC / Human Reviewer Name]

## Scope
- Files reviewed: [N]
- Lines of code: [N]
- Related stories: [list]

## Summary
- Critical issues: [N]
- Major issues: [N]
- Minor issues: [N]
- Suggestions: [N]

## Findings

### Critical Issues
[Must be resolved before merge]

| # | File | Line | Issue | Recommendation |
|---|------|------|-------|----------------|
| 1 | [file] | [line] | [description] | [fix] |

### Major Issues
[Should be resolved before merge]

| # | File | Line | Issue | Recommendation |
|---|------|------|-------|----------------|

### Minor Issues
[Can be resolved in follow-up]

| # | File | Line | Issue | Recommendation |
|---|------|------|-------|----------------|

### Suggestions
[Optional improvements]

| # | File | Line | Suggestion |
|---|------|------|------------|

## Security Checklist Results
- [x] No hardcoded secrets
- [x] Input validation present
- [ ] Needs attention: [specific item]

## Positive Observations
[Good patterns, well-written code, etc.]

## Review Decision
- [ ] **Approved** - Ready for merge
- [ ] **Approved with Minor Changes** - Can merge after addressing minor issues
- [ ] **Changes Required** - Must address major/critical issues before merge
- [ ] **Rejected** - Significant rework needed
```

### Step 6: Handle Review Findings
Based on findings:
- [ ] **Critical/Major Issues**: Return to Code Generation for fixes
- [ ] **Minor Issues**: Document for fix before or after merge
- [ ] **No Blocking Issues**: Proceed to approval

### Step 7: Log Review Prompt
- [ ] Log review completion with timestamp in `aidlc-docs/audit.md`
- [ ] Include summary of findings
- [ ] Use ISO 8601 timestamp format

### Step 8: Present Completion Message

**MANDATORY**: Always present the review report and wait for user decision.

```markdown
# 🔍 Code Review Complete - [Unit Name]

## Review Summary
[AI-generated summary of review findings in bullet points]
- Files reviewed: [N]
- Critical issues: [N]
- Major issues: [N]
- Minor issues: [N]

## Key Findings
[List top 3-5 most important findings]

> **📋 REVIEW REQUIRED:**  
> Please examine the complete code review report at: `aidlc-docs/construction/[unit-name]/code-review-report.md`

> **🚀 WHAT'S NEXT?**
>
> **Select a review decision:**
>
> - ✅ **Approve** - Code is ready for Build & Test
>
> - ⚠️ **Approve with Minor Changes** - Proceed, address minor issues in follow-up
>
> - 🔧 **Request Changes** - Return to Code Generation to address issues
>
> - ❌ **Reject** - Significant rework needed, reassess approach

---
```

### Step 9: Wait for Explicit Decision
**CRITICAL**: Do NOT proceed to Build & Test until user explicitly approves.

- [ ] Wait for user to select a decision option
- [ ] Do not auto-approve or skip this step
- [ ] If "Request Changes" or "Reject": Return to Code Generation
- [ ] If "Approve" or "Approve with Minor Changes": Proceed to Build & Test
- [ ] Document decision in audit.md with timestamp

### Step 10: Update Progress
- [ ] Mark Code Review complete for unit in `aidlc-docs/aidlc-state.md`
- [ ] Update the "Current Status" section
- [ ] Track any deferred minor issues for follow-up

### Step 11: Skill Feedback Capture

**See `common/skill-feedback.md` for full feedback definitions (result types, severity levels, file format).**

IF `aidlc-state.md` → Organizational Skills section lists any consumed skills:
- [ ] Load the list of consumed Skill IDs for this unit
- [ ] For each Skill ID that **actively generated code patterns** in this unit:
  - Read skill version from YAML frontmatter (`metadata.version`)
  - Was the skill-generated pattern accepted as-is in the review? → Record `ok`
  - Did the review flag issues in skill-derived code? → Record `correction` with the finding reference
  - Did the review identify missing guidance the skill should have covered? → Record `gap`
  - Do NOT record `ok` for skills that were merely loaded but did not produce code in this unit
- [ ] Assign severity per entry: `low` | `medium` | `high`
- [ ] Append entries to `aidlc-docs/skill-feedback.md` (create file with header template from `common/skill-feedback.md` if it does not exist). Include the Version column.

ELSE: Skip — no skills consumed, no feedback to capture.

---

## Critical Rules

### Review Quality
- Review should be thorough, not rubber-stamp
- All code paths should be examined
- Security checklist is mandatory

### Finding Classification
- **Critical**: Security vulnerabilities, data loss risks, blocking bugs
- **Major**: Significant bugs, design violations, performance issues
- **Minor**: Style issues, minor improvements, non-blocking bugs
- **Suggestion**: Optional enhancements, alternative approaches

### Blocking Criteria
- Critical issues always block
- Major issues should block (can override with justification)
- Minor issues do not block but should be tracked

### Documentation
- All reviews must produce a report
- Findings must be actionable and specific
- Positive feedback is encouraged

## Integration with Version Control

When integrated with Git workflows:
- Create review report before merge/PR approval
- Reference report in merge commit or PR
- Track issue resolution in subsequent commits
