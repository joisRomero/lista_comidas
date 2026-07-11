# Project Handoff - Detailed Steps

## Purpose
**Complete knowledge transfer and formally close the project**

Project Handoff focuses on:
- Transferring knowledge to support and operations teams
- Capturing lessons learned for continuous improvement
- Completing all administrative closure activities
- Creating final project closure record

**Note**: This is the final stage of the project lifecycle, combining knowledge transfer and lessons learned.

## Prerequisites
- Stakeholder Sign-off must be complete
- All project deliverables are accepted
- Support and operations teams are identified

---

## Step-by-Step Execution

### Step 1: Identify Handoff Recipients
- [ ] List teams/individuals receiving handoff:
  - Operations/Support team
  - Maintenance developers
  - Business stakeholders (for ongoing ownership)
  - Security/Compliance (if applicable)
- [ ] Confirm availability for handoff sessions

### Step 2: Prepare Knowledge Transfer Materials
- [ ] Compile handoff documentation:
  - Project Snapshot (reference)
  - Architecture overview
  - Operational runbooks
  - Troubleshooting guides
  - Common issues and resolutions
  - Escalation procedures

### Step 3: Create Knowledge Transfer Document
- [ ] Create `aidlc-docs/closure/knowledge-transfer.md`:

```markdown
# Knowledge Transfer Document

## Overview
- **Project**: [Name]
- **Version**: [X.Y.Z]
- **Handoff Date**: [YYYY-MM-DD]

## System Overview

### What Does This System Do?
[Plain language explanation for support team]

### Key User Journeys
1. [User journey 1]: [description]
2. [User journey 2]: [description]

### Critical Business Processes
| Process | Components Involved | Impact if Down |
|---------|---------------------|----------------|
| [process] | [components] | [impact] |

## Operational Guide

### Health Checks
| Check | Endpoint/Command | Expected Result |
|-------|------------------|-----------------|
| API Health | GET /health | 200 OK |
| DB Connection | [command] | [expected] |

### Common Operations
| Operation | Procedure | Frequency |
|-----------|-----------|-----------|
| [operation] | [steps] | [frequency] |

### Monitoring & Alerts
| Alert | Meaning | Response |
|-------|---------|----------|
| [alert] | [what it means] | [what to do] |

## Troubleshooting Guide

### Common Issues
| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| [symptom] | [cause] | [steps to resolve] |

### Diagnostic Commands
```bash
# Check application logs
[command]

# Check database status
[command]

# Restart service
[command]
```

### Escalation Path
| Severity | Response Time | Contact |
|----------|---------------|---------|
| Critical | [time] | [contact] |
| High | [time] | [contact] |
| Medium | [time] | [contact] |

## Key Contacts
| Role | Name | Contact | Availability |
|------|------|---------|--------------|
| Original Dev Lead | [name] | [contact] | [availability post-handoff] |
| Product Owner | [name] | [contact] | [availability] |

## Training Completed
| Session | Attendees | Date | Materials |
|---------|-----------|------|-----------|
| [session] | [attendees] | [date] | [link] |

## Handoff Confirmation
- [ ] Operations team has received all documentation
- [ ] Support team has received troubleshooting guides
- [ ] Access and permissions transferred
- [ ] Training sessions completed
- [ ] Q&A session conducted
```

### Step 4: Conduct Handoff Sessions
- [ ] Schedule handoff sessions with recipients
- [ ] Walk through system architecture
- [ ] Demonstrate key operations
- [ ] Review troubleshooting procedures
- [ ] Conduct Q&A session

### Step 5: Capture Lessons Learned
- [ ] Conduct retrospective with project team
- [ ] Create `aidlc-docs/closure/lessons-learned.md`:

```markdown
# Lessons Learned

## Project Information
- **Project**: [Name]
- **Version**: [X.Y.Z]
- **Retrospective Date**: [YYYY-MM-DD]
- **Participants**: [List]

## What Went Well
| Item | Impact | Recommendation |
|------|--------|----------------|
| [item] | [positive impact] | [continue/adopt more widely] |

## What Could Be Improved
| Item | Impact | Recommendation |
|------|--------|----------------|
| [item] | [negative impact] | [specific improvement] |

## Process Insights

### Planning Phase
- [Insight about planning effectiveness]

### Execution Phase
- [Insight about execution]

### Communication
- [Insight about team/stakeholder communication]

### Tools & Technology
- [Insight about tools used]

## Recommendations for Future Projects
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

## Metrics Summary
| Metric | Target | Actual | Notes |
|--------|--------|--------|-------|
| Timeline | [target] | [actual] | |
| Scope | [target] | [actual] | |
| Quality | [target] | [actual] | |

## Team Acknowledgments
[Recognize team contributions]
```

### Step 5b: Generate Skill Health Report

**See `common/skill-feedback.md` for feedback definitions and capture rules.**

IF `aidlc-docs/skill-feedback.md` exists (feedback was captured during Construction):
- [ ] Load all entries from `aidlc-docs/skill-feedback.md`
- [ ] Aggregate entries per Skill ID: count `ok`, `correction`, and `gap` results
- [ ] Determine max severity per skill across all entries
- [ ] Assign status per skill:
  - **Healthy**: Zero corrections or gaps
  - **Monitor**: 1 correction or gap
  - **Needs Improvement**: ≥2 corrections or gaps
- [ ] Create `aidlc-docs/closure/skill-health-report.md`:

```markdown
# Skill Health Report

## Project Information
- **Project**: [Name from aidlc-state.md]
- **Report Date**: [YYYY-MM-DD]
- **Feedback Entries Analyzed**: [N]

## Per-Skill Summary

| Skill ID | Version | OK | Corrections | Gaps | Max Severity | Status |
|----------|---------|-----|-------------|------|--------------|--------|
| [skill-id] | [version(s) observed] | [N] | [N] | [N] | [low/medium/high] | [✅ Healthy / 🟡 Monitor / 🔴 Needs Improvement] |

> **Version tracking**: List all versions observed during the project. If a skill was updated mid-project, list both (e.g., "1.0, 1.1"). This enables correlating improvements with version bumps.

## Skills Needing Attention

### [Skill ID] — 🔴 Needs Improvement
**Issues**:
| Date | Version | Stage | Result | Detail | Severity |
|------|---------|-------|--------|--------|----------|
| [entries from skill-feedback.md for this skill] |

**Recommendation**: [Specific action for skill maintainer]

## Recommendations for Central Atlas Repository
1. [Recommendation 1 — reference specific skill and issue]
2. [Recommendation 2]

## Cross-Project Aggregation
To consolidate feedback across multiple projects, run:
\`\`\`bash
./scripts/collect-feedback.sh <output-file> <project-path-1> [project-path-2] ...
\`\`\`
```

- [ ] Include skill health summary in `aidlc-docs/closure/lessons-learned.md` under "Tools & Technology" section
- [ ] Log skill health report generation in `aidlc-docs/audit.md`

ELSE: Skip — no skill feedback was captured during Construction.

### Step 6: Complete Administrative Closure
- [ ] Verify all documentation is complete
- [ ] Confirm all artifacts are archived
- [ ] Transfer ownership of systems/accounts
- [ ] Close project-related access (if applicable)
- [ ] Update project status in portfolio (if applicable)

### Step 7: Create Closure Record
- [ ] Create `aidlc-docs/closure/project-closure-record.md`:

```markdown
# Project Closure Record

## Project Information
- **Project Name**: [Name]
- **Final Version**: [X.Y.Z]
- **Start Date**: [YYYY-MM-DD]
- **End Date**: [YYYY-MM-DD]
- **Duration**: [X months/weeks]

## Closure Checklist

### Deliverables
- [x] All requirements delivered
- [x] All user stories completed
- [x] Documentation complete
- [x] Code archived

### Approvals
- [x] Stakeholder sign-off obtained
- [x] Technical approval obtained
- [x] Operations approval obtained

### Handoff
- [x] Knowledge transfer completed
- [x] Support team trained
- [x] Documentation transferred
- [x] Access/ownership transferred

### Retrospective
- [x] Lessons learned captured
- [x] Recommendations documented

## Final Project Status
**STATUS: CLOSED**

## Closing Statement
[Brief closing statement about project success and outcomes]

## Authorized By
- **Name**: _______________
- **Role**: _______________
- **Date**: _______________
- **Signature**: _______________
```

### Step 8: Log Project Closure
- [ ] Log final closure with timestamp in `aidlc-docs/audit.md`
- [ ] Include closure summary
- [ ] Use ISO 8601 timestamp format

### Step 9: Present Completion Message

```markdown
# 🎉 Project Closure Complete

**Project [Name] v[X.Y.Z] is officially CLOSED**

[AI-generated summary of closure in bullet points]

> **📋 CLOSURE DOCUMENTS:**  
> - Knowledge Transfer: `aidlc-docs/closure/knowledge-transfer.md`
> - Lessons Learned: `aidlc-docs/closure/lessons-learned.md`
> - Closure Record: `aidlc-docs/closure/project-closure-record.md`



> **✅ PROJECT CLOSURE COMPLETE**
>
> All closure activities have been completed:
> - ✅ Project Snapshot created
> - ✅ Version archived
> - ✅ Stakeholder sign-off obtained
> - ✅ Knowledge transfer completed
> - ✅ Lessons learned captured
>
> The project is now in maintenance mode.

---
```

### Step 10: Update Final Progress
- [ ] Mark Project Handoff complete in `aidlc-docs/aidlc-state.md`
- [ ] Update project status to CLOSED
- [ ] Archive aidlc-state.md with final status

---

## Critical Rules

### Complete Transfer
- Support team must be capable of independent operation
- All critical knowledge must be documented
- No single points of knowledge should remain

### Lessons Captured
- Conduct retrospective while project is fresh
- Be specific and actionable in recommendations
- Share lessons with broader organization

### Formal Closure
- Create official closure record
- Obtain authorized sign-off on closure
- Maintain closure documentation permanently
