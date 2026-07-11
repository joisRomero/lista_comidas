---
name: judgment-day
description: >
  Adversarial code review with two blind judges in parallel.
  Trigger: When Code Review detects high-risk changes (>10 files, security modules, new features).
metadata:
  author: anta
  version: "1.0"
  scope: [root]
  auto_invoke: "judgment day, adversarial review, que lo juzguen"
  phase: [construction]
  layer: null
  validates_with: null
  validation_profile: null
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Orchestrator NEVER reviews code | ALWAYS | Only coordinates — judges do the review |
| Two judges, always parallel, always blind | ALWAYS | Single reviewer has blind spots |
| Both must agree for CRITICAL confirmation | ALWAYS | Prevents false positives |
| Fresh context per judge | ALWAYS | Prevents relationship drift (leniency) |
| Fix agent is separate from judges | ALWAYS | Surgical fixes only, no refactoring |
| Re-judge after every fix round | ALWAYS | Fixes must be validated before closing |
| Max 2 fix iterations then ask user | ALWAYS | Prevents infinite loops |

---

## When to Activate

Judgment Day is triggered during Code Review (Step 4) when the change is **high risk**.

| Risk Level | Criteria | Code Review Approach |
|------------|----------|---------------------|
| **Low** | Typo, 1 file, config change | Standard review (1 pass) |
| **Medium** | Small feature, 2-5 files | Standard review + approval gate |
| **High** | New feature, >10 files, security modules, auth flows, data access | **Judgment Day** |

**High-risk signals** (any ONE triggers JD):
- Change touches auth, security, or data access layers
- More than 10 files changed in the unit
- New API endpoints with write operations (POST/PUT/DELETE)
- Database schema changes (new tables, column modifications)
- Multi-repo changes affecting Gateway routing
- Code Gen Plan flagged critical issues in Step 3

---

## Protocol

### Pattern 0: Skill Resolution

Before launching judges, resolve project standards via Skill Resolver:

1. Read `SKILLS-MANIFEST.md` for current stage (Code Review)
2. Identify skills matching the changed code (file extensions, layer)
3. Extract **Compact Rules** from each matching SKILL.md
4. Build identical `## Project Standards` block for injection into both judges AND fix agent

### Pattern 1: Parallel Blind Review

```
Orchestrator (YOU)
    │
    ├── delegate → Judge A ── fresh context, blind
    │
    └── delegate → Judge B ── fresh context, blind
    
    Wait for BOTH before proceeding.
```

**If agent supports parallel sub-agents** (OpenCode, Kiro with sub-agents):
- Launch Judge A and Judge B in parallel via delegation
- Both receive identical inputs (see Judge Prompt below)
- Neither knows the other exists

**If agent does NOT support sub-agents** (Amazon Q, single-agent Kiro):
1. Perform Review A → save to `aidlc-docs/judgment-findings-a.md`
2. Clear mental context — approach the next review as a FRESH perspective
3. Perform Review B → save to `aidlc-docs/judgment-findings-b.md`
4. Synthesize both files into verdict table

### Pattern 2: Verdict Synthesis

After BOTH judges complete, build the verdict table:

```markdown
## Judgment Day — Verdict Table

| # | Finding | Judge A | Judge B | Severity | Status |
|---|---------|---------|---------|----------|--------|
| 1 | Missing null check auth.go:42 | ✅ | ✅ | CRITICAL | Confirmed |
| 2 | Windows path edge case | ❌ | ✅ | WARNING (theoretical) | INFO |
| 3 | SP naming mismatch | ✅ | ❌ | SUGGESTION | Suspect |
```

**Classification rules**:

| Judge A | Judge B | Result |
|---------|---------|--------|
| ✅ CRITICAL | ✅ CRITICAL | **Confirmed** → must fix |
| ✅ WARNING (real) | ✅ WARNING (real) | **Confirmed** → must fix |
| ✅ any | ❌ | **Suspect** → report, do NOT auto-fix |
| ❌ | ✅ any | **Suspect** → report, do NOT auto-fix |
| ✅ WARNING (theoretical) | ✅ or ❌ | **INFO** → downgrade, log only |
| ✅ SUGGESTION | any | **Suggestion** → fix inline if trivial |

**WARNING classification rule**:
- `WARNING (real)` → Normal intended use can trigger the issue
- `WARNING (theoretical)` → Contrived, malicious, or impossible path → demote to INFO

### Pattern 3: Fix and Re-judge

1. Present confirmed findings to user — **ask before fixing**
2. If user approves fixes:
   - Delegate to fix agent (see Fix Agent Prompt)
   - Fix agent applies **surgical fixes only** — no refactoring
3. After fixes applied → **re-launch both judges** on changed files
4. Synthesize Round 2 verdict
5. If still confirmed issues after Round 2 → ask user: continue fixing or accept?
6. **Max 2 fix iterations** — then present final verdict

### Pattern 4: Terminal States

```
JUDGMENT: APPROVED ✅    — Zero confirmed CRITICALs + zero confirmed real WARNINGs
JUDGMENT: ESCALATED ⚠️   — Unresolved issues after 2 rounds, user decides
```

**HALLUCINATING verdict**: If judges invent problems that clearly don't exist in the code, mark as `JUDGMENT: APPROVED (judges hallucinated)` and note in audit.md. This is a signal the code is clean.

---

## Judge Prompt

```markdown
You are an adversarial code reviewer. Your ONLY job is to find problems.
Do NOT praise code. Do NOT defer to the author. Assume nothing is correct.

## Target
{list of files to review with paths}

## Project Standards (auto-resolved)
{compact rules from Skill Resolver — identical for both judges}

## Review Criteria
- Correctness: logical errors, behavior mismatches with requirements
- Edge cases: missing states, null handling, boundary conditions
- Error handling: propagation, logging, recovery paths
- Performance: N+1 queries, wasteful loops, excessive allocations
- Security: injection, hardcoded secrets, auth boundary violations
- Naming/conventions: project standards compliance (ANTA patterns)

## Return Format
Findings only. No praise. No summaries.

Each finding:
- **Severity**: CRITICAL | WARNING (real) | WARNING (theoretical) | SUGGESTION
- **File**: path/to/file.ext (line N)
- **Issue**: What is wrong and why it matters
- **Fix**: One-line intent (not full code)

WARNING rule:
- Normal intended use can trigger → WARNING (real)
- Contrived/malicious/impossible path → WARNING (theoretical)

If code is clean: VERDICT: CLEAN — No issues found.
```

---

## Fix Agent Prompt

```markdown
You are a surgical fix agent. Apply ONLY the confirmed issues listed below.

## Confirmed Issues to Fix
{confirmed findings table from verdict synthesis}

## Project Standards (auto-resolved)
{same compact rules block — identical to judges}

## Instructions
- Fix ONLY confirmed issues. Nothing else.
- Do NOT refactor beyond the required fix.
- Do NOT change code that was not flagged.
- If fixing a repeated pattern in touched files, fix all occurrences of that pattern.
- Return: file path, line, and one-line fix summary per change.
```

---

## Output Format

Generate `aidlc-docs/construction/{unit-name}/judgment-day-report.md`:

```markdown
# Judgment Day Report — {Unit Name}

**Date**: {ISO 8601}
**Risk Level**: HIGH
**Trigger**: {why JD was activated — e.g., ">10 files changed", "auth module modified"}
**Files Reviewed**: {count}
**Round**: {1 or 2}

---

## Verdict Table

| # | File:Line | Finding | Judge A | Judge B | Severity | Status |
|---|-----------|---------|---------|---------|----------|--------|
| 1 | src/Handlers/CreateEmployee.cs:42 | Missing null check on EmployeeId | ✅ | ✅ | CRITICAL | Confirmed |
| 2 | database/HR/StoredProcedures/SP_Employee_Create.sql:18 | QUOTENAME missing on dynamic column | ✅ | ✅ | CRITICAL | Confirmed |
| 3 | src/Features/employees/hooks/useEmployeeMutation.ts:25 | Missing error handling on mutation | ✅ | ❌ | WARNING (real) | Suspect |
| 4 | src/Handlers/ListEmployees.cs:31 | Theoretical race condition on parallel requests | ❌ | ✅ | WARNING (theoretical) | INFO |
| 5 | src/Endpoints/EmployeeEndpoints.cs:15 | Consider extracting route constants | ✅ | ✅ | SUGGESTION | Suggestion |

## Summary

| Severity | Count | Action |
|----------|-------|--------|
| CRITICAL (Confirmed) | {N} | Must fix before merge |
| WARNING real (Confirmed) | {N} | Must fix before merge |
| Suspect | {N} | Review — only 1 judge flagged |
| INFO (Theoretical) | {N} | Logged, no action needed |
| Suggestion | {N} | Fix if trivial |

---

## Decision Required

**Confirmed issues that MUST be fixed ({N} total):**

| # | File:Line | Issue | Proposed Fix |
|---|-----------|-------|-------------|
| 1 | src/Handlers/CreateEmployee.cs:42 | Missing null check on EmployeeId | Add guard clause `if (request.EmployeeId == null) return ApiResponse.Fail(...)` |
| 2 | database/HR/StoredProcedures/SP_Employee_Create.sql:18 | QUOTENAME missing | Wrap dynamic column with `QUOTENAME(@ColumnName)` |

**Suspect issues to review ({N} total):**

| # | File:Line | Issue | Judge | Your Call |
|---|-----------|-------|-------|-----------|
| 3 | useEmployeeMutation.ts:25 | Missing error handling | Judge A only | [ ] Fix / [ ] Skip |

---

**What would you like to do?**

1. **Fix all confirmed** — Apply fixes for all confirmed issues, then re-judge
2. **Fix confirmed + selected suspects** — Mark which suspects to include (edit table above)
3. **Skip fixes, accept as-is** — Log findings, proceed without fixing
4. **Escalate** — Stop, review manually before proceeding

[Answer]:
```

After user responds:
- Option 1 or 2 → Delegate to Fix Agent → Re-judge (Pattern 4)
- Option 3 → Log `JUDGMENT: APPROVED (with known issues)` in audit.md
- Option 4 → Log `JUDGMENT: ESCALATED` in audit.md

---

## Checklist

### Before Launching Judges
- [ ] Skill Resolver executed — Project Standards block ready
- [ ] Target scope identified (changed files list)
- [ ] High-risk trigger confirmed (check criteria table)

### After Verdict Synthesis
- [ ] All confirmed findings presented to user
- [ ] User approved/rejected fix plan
- [ ] Fix agent applied surgical fixes only
- [ ] Re-judge completed after fixes (if fixes were applied)
- [ ] Final verdict logged: APPROVED or ESCALATED
- [ ] Results appended to Code Review Report
- [ ] audit.md updated with Judgment Day verdict

---

## Related Skills

| Task | Skill |
|------|-------|
| Standard code review | `code-review` (construction stage) |
| Validator pre-check | Core Library validators (Step 3b) |
| API spec compliance | `api-first-spec` |
| Security patterns | `security` |
