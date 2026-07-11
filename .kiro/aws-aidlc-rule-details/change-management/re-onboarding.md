# Re-Onboarding - Detailed Steps

## Purpose
**Restore project context for previously closed or paused projects**

Re-Onboarding focuses on:
- Loading project history and decisions from archived artifacts
- Validating current state matches documented state
- Identifying changes made outside the documented workflow
- Preparing context for new change requests

**Note**: This stage is the entry point when returning to a previously closed project.

## Prerequisites
- Project Snapshot must exist from previous closure
- Version archive must be accessible
- New work request has been received

---

## Step-by-Step Execution

### Step 1: Locate Project Artifacts
- [ ] Find project snapshot: `aidlc-docs/closure/project-snapshot.md`
- [ ] Locate version history: `aidlc-docs/VERSION-HISTORY.md`
- [ ] Identify latest archived version: `aidlc-docs/v[X.Y.Z]/`
- [ ] Verify audit trail: `aidlc-docs/audit.md`

### Step 2: Load Project Context
- [ ] Read Project Snapshot completely
- [ ] Review Architecture Decision Records (ADRs)
- [ ] Load API contracts if applicable
- [ ] Review known issues and technical debt
- [ ] Understand current technology stack

### Step 3: Validate Current State
- [ ] Compare documented state with actual codebase:
  - Check if documented files exist
  - Verify technology versions match
  - Confirm API contracts are current
- [ ] Identify any undocumented changes:
  - Files added outside workflow
  - Configuration changes
  - Dependency updates

### Step 4: Create Re-Onboarding Report
- [ ] Create `aidlc-docs/change-management/re-onboarding-report.md`:

```markdown
# Re-Onboarding Report

## Project Information
- **Project**: [Name]
- **Last Version**: [X.Y.Z]
- **Closure Date**: [YYYY-MM-DD]
- **Re-Onboarding Date**: [YYYY-MM-DD]
- **Time Since Closure**: [X months/years]

## Context Loaded

### Project Snapshot
- [x] Loaded and reviewed
- **Key Summary**: [Brief summary of what the project does]

### Architecture Decisions
- **Total ADRs**: [N]
- **Key Decisions**:
  - [Decision 1 summary]
  - [Decision 2 summary]

### Technology Stack
| Component | Documented Version | Current Version | Status |
|-----------|-------------------|-----------------|--------|
| [tech] | [version] | [version] | ✅/⚠️ |

### API Contracts
| API | Status | Notes |
|-----|--------|-------|
| [API] | Current/Outdated | [notes] |

## State Validation

### Documented vs Actual State
| Aspect | Match | Notes |
|--------|-------|-------|
| Code structure | ✅/⚠️ | [notes] |
| Dependencies | ✅/⚠️ | [notes] |
| Configuration | ✅/⚠️ | [notes] |
| API contracts | ✅/⚠️ | [notes] |

### Undocumented Changes Found
| Change | Impact | Recommendation |
|--------|--------|----------------|
| [change] | [impact] | [recommendation] |

### Drift Assessment
- **Drift Level**: [None / Minor / Significant]
- **Recommendation**: [Proceed / Run Reverse Engineering / Investigate]

## Known Issues Reminder
[List key issues from project snapshot that are still relevant]

## Technical Debt Status
[Summarize outstanding technical debt]

## Recommendations

### Before Proceeding with Changes
1. [Recommendation 1]
2. [Recommendation 2]

### Context Refresh Needed
- [ ] None - documentation is current
- [ ] Run Reverse Engineering - significant drift detected
- [ ] Update specific artifacts: [list]

## Re-Onboarding Status
- [ ] **READY** - Context loaded, proceed to Change Request
- [ ] **NEEDS REFRESH** - Run Reverse Engineering first
- [ ] **BLOCKED** - Issues require resolution first
```

### Step 5: Handle State Drift
If significant drift detected:
- [ ] **Minor Drift**: Document differences and proceed
- [ ] **Moderate Drift**: Update documentation to match current state
- [ ] **Significant Drift**: Execute Reverse Engineering stage

### Step 6: Load Relevant History
- [ ] Review recent audit.md entries
- [ ] Check for any pending change requests
- [ ] Review lessons learned from previous closure
- [ ] Understand any constraints or commitments

### Step 7: Log Re-Onboarding
- [ ] Log completion with timestamp in `aidlc-docs/audit.md`
- [ ] Include context summary and drift assessment
- [ ] Use ISO 8601 timestamp format

### Step 8: Present Completion Message

```markdown
# 🔄 Re-Onboarding Complete

**Project context has been restored**

[AI-generated summary of re-onboarding in bullet points]

> **📋 RE-ONBOARDING REPORT:**  
> Please examine the report at: `aidlc-docs/change-management/re-onboarding-report.md`
>
> **Context Status:**
> - Project Snapshot: ✅ Loaded
> - ADRs: ✅ Reviewed
> - State Validation: [Status]
> - Drift Level: [None/Minor/Significant]



> **🚀 WHAT'S NEXT?**
>
> [If Ready:]
> - ✅ **Proceed to Change Request** - Document the new change request
>
> [If Needs Refresh:]
> - 🔄 **Run Reverse Engineering** - Update documentation first
>
> [If Blocked:]
> ⚠️ **Resolve Issues** - Address identified blockers

---
```

### Step 9: Update Progress
- [ ] Create or update `aidlc-docs/aidlc-state.md` for change cycle
- [ ] Mark Re-Onboarding complete
- [ ] Proceed to Change Request stage

---

## Critical Rules

### Context Before Action
- Never start changes without loading context first
- Validate state before assuming documentation is current
- Identify drift before proceeding

### Documentation Check
- Verify all referenced documents exist
- Confirm versions match between docs and code
- Note any discrepancies

### Knowledge Transfer
- If original team is unavailable, flag knowledge gaps
- Document assumptions made during re-onboarding
- Seek clarification for critical uncertainties
