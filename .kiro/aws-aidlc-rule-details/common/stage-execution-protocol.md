# Stage Execution Protocol

Every stage in the AI-DLC workflow follows this protocol. Stages reference this file instead of repeating these steps individually.

> **Design Note**: The core protocol (steps 1-6) is also defined inline in `core-workflow.md` (first 50 lines) to guarantee visibility regardless of file loading order. This file provides expanded detail and audit log formats. This redundancy is **intentional** — see Lessons Learned below.

## Entry

1. **Log** in `audit.md`:
   ```markdown
   ## [Phase] > [Stage Name] — Started
   **Timestamp**: [ISO 8601]
   **User Input**: "[Complete raw input if any — never summarize]"
   ```
2. **Load** the detail file referenced in the stage definition (e.g., `Load inception/workspace-detection.md`)
3. **Follow ALL steps** in the detail file — the summaries in the orchestrator are NOT sufficient

## Execution

4. Execute all steps defined in the detail file
5. Execute any stage-specific steps listed in the orchestrator (unique to that stage)

## Exit

6. **Log** stage completion in `audit.md`:
   ```markdown
   ## [Phase] > [Stage Name] — Completed
   **Timestamp**: [ISO 8601]
   **AI Response**: "[Action taken or result summary]"
   **Context**: [Key outputs, decisions made]
   ```
7. **Update** `aidlc-state.md` with:
   - Current phase and stage
   - Completion status
   - Key outputs (1-line summary)
   - **HOW to update**: Use `edit` (find-and-replace) to change `- [ ] {StageName}` to `- [x] {StageName}` — do NOT use `write` that appends new checkboxes. The state file must have exactly ONE entry per stage.
7b. **Idempotency check** for `audit.md`: Before appending a "Completed" entry, verify:
   - The stage artifact file(s) ACTUALLY EXIST in the filesystem
   - No existing "Completed" entry for this stage+timestamp already exists in `audit.md`
   - If the file does not exist yet, do NOT log "Completed" — log "Attempted" instead and retry the write
8. **SELF-CHECK GATE (MANDATORY)**: Before presenting the completion message, verify:
   - [ ] Did I append the stage completion log to `audit.md`? (Step 6)
   - [ ] Did I update `aidlc-state.md` with current stage + status? (Step 7)
   - [ ] Did I populate Key Decisions in `aidlc-state.md` for decisions made in THIS stage? (Step 7c)
   - [ ] Did I run ALL validators required by this stage and log results in `audit.md`? (Step 8b)
   - **If ANY is missing**: STOP. Do it NOW before proceeding. A stage is NOT complete without all updates.

   **Key Decisions update triggers** (only these stages):

   | Stage | Must Populate |
   |-------|--------------|
   | Requirements Analysis | Architecture, Stack |
   | ISO 27001 Assessment | ISO 27001 Depth |
   | Workflow Planning | Request Type, Scope, Stages Profile |

   Other stages: skip Key Decisions check (no new decisions to record).

   **Validator execution triggers** (only these stages):

   | Stage | Validator Command | What It Checks |
   |-------|------------------|----------------|
   | API Contract Design | `python config/validators/validate_openapi.py {openapi.yaml}` | Response shapes, pagination, auth schemes, base path |
   | Prototyping | `python config/validators/validate_html_prototype.py {html files}` | CSS class usage, undefined classes |
   | Code Generation (BD) | `python config/validators/runner.py --profile conventions-lint {db_path}` | SP naming, QUOTENAME, audit columns |
   | Code Generation (Backend) | `python config/validators/runner.py --profile build-unit {backend_path}` | Handler pattern, ApiResponse, FluentValidation, deps |
   | Code Generation (Frontend) | `python config/validators/runner.py --profile build-component {frontend_path}` | Feature structure, Anta* wrappers, no-any |
   | Code Review | `python config/validators/runner.py --all --report {project_path}` | Full validation report |
   | Build and Test | `python config/validators/runner.py --profile structure {project_path}` | Repo structure, Docker, auth patterns |

   **Validator enforcement rule**: If a stage has a validator in this table, you MUST:
   1. Run the command (execute it, don't just reference it)
   2. Log the output (errors/warnings count) in `audit.md`
   3. Fix ERRORS before presenting completion (max 3 fix iterations)
   4. If errors persist after 3 iterations → log as ESCALATED in `audit.md`, proceed with warning

   Other stages: skip validator check (no validators apply).
9. **Present** completion message to user (defined in each detail file)
10. **Wait** for user approval before proceeding to the next stage
    - **Exception**: Stages marked `AUTO-PROCEED` in the orchestrator skip the wait
11. **Log** user's approval response in `audit.md` with complete raw input

## Construction Stage Completion

Construction stages (Functional Design through Code Review) use a **standardized 2-option completion message**:

- Option 1: **Request Changes** — user asks for modifications
- Option 2: **Continue to Next Stage** — user approves

**NEVER create 3-option menus or other emergent navigation patterns in Construction stages.**

## Invariants (NEVER violate)

- **NEVER skip Entry steps 1-3.** Detail files contain mandatory artifacts the orchestrator summaries omit.
- **NEVER skip Exit steps 6-8.** Without `audit.md`, `aidlc-state.md`, and Key Decisions updates, session resumption breaks and the agent will re-ask decided questions.
- **NEVER present a completion message without passing the Self-Check Gate (step 8).** The completion message is the LAST thing the user sees — if state files aren't updated before it, they won't be updated at all.
- **NEVER assume user intent not explicitly stated.** When in doubt, consult `common/overconfidence-prevention.md`.
- **NEVER summarize or paraphrase user input** in audit log entries — capture complete raw text.
- **ALWAYS append** to `audit.md` — NEVER overwrite.

## Token Budget Checkpoint (Phase Boundaries)

At the **end of each phase** (last stage of INCEPTION, CONSTRUCTION, OPERATIONS, CLOSURE), append a token checkpoint to `audit.md`:

```markdown
## TOKEN CHECKPOINT — [Phase] Complete
**Timestamp**: [ISO 8601]
**Phase**: [INCEPTION | CONSTRUCTION | OPERATIONS | CLOSURE | CHANGE-MANAGEMENT]
**Stages executed**: [count]
**Skills loaded this phase**: [list skill IDs]
**Estimated context usage**: [if platform exposes token count, log it; otherwise "not available"]
**Observations**: [any signs of context pressure: forgotten rules, repeated questions, missed conventions]
```

**When to log**: After Exit step 7 (aidlc-state.md update) of the LAST stage in each phase.
**Why**: Empirical data to detect context window saturation. If the agent starts dropping conventions in later phases, the checkpoint identifies where pressure began.
**This is OPTIONAL**: Skip if the platform does not expose token metrics. The "Observations" field is always useful regardless.

---

## Lessons Learned (from v1.1.0 validation)

These design decisions come from production validation with 5+ projects:

1. **Position over reference**: MANDATORY instructions must appear in the first 50 lines of `core-workflow.md`. When state-update rules were only in "Key Principles" at line 872, agents deprioritized them. The inline protocol at the top of the orchestrator exists because of this.
2. **Lazy-load exposes implicit dependencies**: In v1.0.0, eager-loaded common files (process-overview.md, session-continuity.md) reinforced the stage completion protocol as a side effect. When v1.1.0 moved them to on-demand, agents stopped updating `aidlc-state.md` because no explicit step told them to. Lesson: every critical behavior must be an explicit step, never an implicit side effect of context loading.
3. **Short transition-gate reminders > lengthy principle sections**: Each stage in the orchestrator says "(follow Stage Execution Protocol)" — this short reminder at the execution point provides better compliance per token than a long principles section far from the action.
4. **Intentional redundancy for critical paths**: The protocol appears in two places (inline in orchestrator + this file). This is NOT duplication — it's a resilience pattern. The inline version ensures compliance even if this file is never loaded. This file provides the expanded detail (audit formats, construction rules) for when it IS loaded.
5. **Completion semantics must be unambiguous**: "Stage complete" means ALL exit steps (3-6) are done. A stage is NOT complete just because the detail file steps finished — state tracking and user approval are part of completion.
