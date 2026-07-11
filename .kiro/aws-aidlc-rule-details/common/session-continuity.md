# Session Continuity Templates

## Welcome Back Prompt Template
When a user returns to continue work on an existing AI-DLC project, present this prompt:

```markdown
**Welcome back! I can see you have an existing AI-DLC project in progress.**

Based on your aidlc-state.md, here's your current status:
- **Project**: [project-name]
- **Current Phase**: [INCEPTION/CONSTRUCTION/OPERATIONS/CLOSURE/CHANGE MANAGEMENT]
- **Current Stage**: [Stage Name]
- **Last Completed**: [Last completed step]
- **Next Step**: [Next step to work on]

**What would you like to work on today?**

A) Continue where you left off ([Next step description])
B) Review a previous stage ([Show available stages])
C) Request a change to a closed project (enters CHANGE MANAGEMENT)

[Answer]: 
```

## MANDATORY: Session Continuity Instructions

1. **Always read aidlc-state.md first** when detecting existing project
2. **Parse Key Decisions as HARD CONSTRAINTS** — These were already decided. DO NOT re-ask:
   - Architecture (Single/Multi-Repo)
   - Stack
   - ISO 27001 Depth
   - Request Type and Scope
   - Stages Profile (which stages EXECUTE/SKIP)
3. **Load ONLY artifacts needed for the CURRENT stage** — NOT all previous stages:

   | Current Stage | Load These Artifacts |
   |---------------|---------------------|
   | Early Inception (WD, RE, RA) | Workspace analysis only |
   | User Stories, ISO, Spike | requirements.md |
   | API Contract Design, ADRs | requirements.md + stories.md |
   | Workflow Planning, App Design | requirements.md + stories.md + openapi.yaml (if exists) |
   | Definition of Ready | readiness-checklist.md (if exists) |
   | Code Generation | functional-design.md of current unit + openapi.yaml |
   | Code Review | Generated code files of current unit |
   | Build and Test | All code files + QA matrix |
   | Operations | Build results + release artifacts |
   | Closure | Project snapshot artifacts |
   | Change Management | Archived snapshot + change request |

4. **If Key Decisions section is incomplete** — read the specific artifact to fill the gap, then UPDATE aidlc-state.md with the missing decision for next session
5. **Adapt options** based on architectural choice and current phase
6. **Show specific next steps** rather than generic descriptions
7. **Log the continuity prompt** in audit.md with the actual current system timestamp
8. **Context Summary**: After loading, state what was loaded (1 line) for user awareness
9. **Asking questions**: ALWAYS in dedicated `.md` files with `[Answer]:` tags — NEVER in chat

## Phase-Specific Continuity Handling

### CLOSURE Phase Continuity
When resuming in CLOSURE phase:
- Load complete project state from all previous phases
- Check which closure stages are complete (Snapshot, Archive, Sign-off, Handoff)
- Present status of closure checklist items
- Offer to continue with next incomplete closure stage

### CHANGE MANAGEMENT Phase Continuity
When resuming in CHANGE MANAGEMENT phase:
- Load the archived project snapshot first
- Check if Re-Onboarding is complete (context restored)
- Check if Change Request is documented
- Check if Impact Analysis is complete
- If analysis complete, show recommended re-entry point (INCEPTION/CONSTRUCTION/OPERATIONS)
- Offer to continue with recommended phase or review analysis

### Completed Project Handling
When project shows status "CLOSED" or "ARCHIVED":
- Inform user project was previously completed
- Offer options:
  - A) View project summary and artifacts
  - B) Enter CHANGE MANAGEMENT to request modifications
  - C) Start new project in same workspace (requires confirmation)

## Error Handling
If artifacts are missing or corrupted during session resumption, see [error-handling.md](error-handling.md) for guidance on recovery procedures. 
