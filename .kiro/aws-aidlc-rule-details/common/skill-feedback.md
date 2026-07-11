# Skill Feedback

**Purpose**: Define how and when to capture feedback about organizational skill performance during Construction, enabling skills to mature iteratively across projects.

## Why Skill Feedback?

Organizational skills (see `common/organizational-skills.md`) provide templates, standards, and conventions. But skills are only useful if they produce correct, efficient code. Without feedback:
- Skills with outdated patterns persist unchallenged
- Teams repeat the same corrections project after project
- Skill maintainers have no signal about what works and what doesn't

The feedback loop captures **skill performance data** during Construction stages and aggregates it during Closure for the skill maintainers.

## Feedback File

All feedback is recorded in a single project-level file:

**Location**: `aidlc-docs/skill-feedback.md`

**Created**: On first feedback entry (during Code Generation, Code Review, or Build & Test)

**Format**:

```markdown
# Skill Feedback Log

## Project Information
- **Project**: [Name from aidlc-state.md]
- **Started**: [YYYY-MM-DD]

## Feedback Entries

| Date | Skill ID | Version | Stage | Result | Detail | Severity |
|------|----------|---------|-------|--------|--------|----------|
| [YYYY-MM-DD] | [skill-id] | [version from skill YAML] | [code-generation / code-review / build-and-test] | [ok / correction / gap] | [description] | [low / medium / high] |
```

> **Version tracking**: Always record the skill version from its YAML frontmatter (`metadata.version`). This enables correlating feedback with specific skill releases — when a skill is updated, you can verify whether previous issues were addressed.

## Result Types

| Result | Meaning | When to Record |
|--------|---------|----------------|
| **ok** | Skill-generated pattern was correct and required no changes | Code review approved code that followed the skill, or build succeeded with skill patterns |
| **correction** | Skill-generated pattern needed manual adjustment | Code review found issues in skill-derived code, or build failed due to skill pattern |
| **gap** | Skill was missing guidance that the project needed | Reviewer or developer had to invent a pattern the skill should have covered |

## Severity Levels

| Severity | Meaning | Examples |
|----------|---------|----------|
| **low** | Minor style or preference issue | Naming convention mismatch, comment format |
| **medium** | Functional impact requiring code changes | Wrong default value, missing validation, incorrect query pattern |
| **high** | Build failure, security issue, or data integrity risk | SQL injection pattern, missing audit columns, broken transaction handling |

## When to Capture Feedback

Feedback is captured at **three** points during Construction:

### 0. Code Generation (SKILL FEEDBACK CAPTURE)

During code generation, the agent can detect skill pattern issues early — before code review or build. This is the earliest detection point:

- [ ] Load consumed skills from `aidlc-state.md` → Organizational Skills section
- [ ] For each skill that actively generated code patterns in this unit:
  - Did the agent need to deviate from the skill's prescribed pattern to satisfy requirements? → Record `correction` with explanation
  - Was the skill missing a pattern the agent had to invent from scratch? → Record `gap` with the missing guidance
- [ ] Read skill version from YAML frontmatter (`metadata.version`) for each entry
- [ ] Append entries to `aidlc-docs/skill-feedback.md`

> **Note**: Do NOT record `ok` at this stage. Code Generation cannot confirm a pattern is correct — only Code Review and Build & Test can validate that.

### 1. Code Review (SKILL FEEDBACK CAPTURE)

After completing the code review for each unit, evaluate each organizational skill that was consumed during code generation:

- [ ] Load consumed skills from `aidlc-state.md` → Organizational Skills section
- [ ] For each skill that **actively generated code patterns** in this unit:
  - Was the skill-generated pattern accepted as-is in the review? → Record `ok`
  - Did the reviewer flag issues in skill-derived code? → Record `correction` with the finding
  - Did the reviewer identify patterns the skill should have covered? → Record `gap`
- [ ] Read skill version from YAML frontmatter (`metadata.version`) for each entry
- [ ] Append entries to `aidlc-docs/skill-feedback.md`

> **"ok" rule**: Only record `ok` when the skill's patterns **actively generated code** in this unit and that code passed review. Do NOT record `ok` for skills that were merely loaded/referenced but did not produce code in the current unit.

### 2. Build & Test (SKILL FEEDBACK CAPTURE)

After build or test failures, check whether any failure traces back to a skill-generated pattern:

- [ ] For each build/test failure:
  - Is the failing code derived from an organizational skill pattern? → Record `correction`
  - Is the failure caused by a missing pattern the skill should define? → Record `gap`
- [ ] If all skill-derived patterns pass → Record `ok` for each skill that **actively generated code** in the build (once per build cycle). Do NOT record `ok` for skills that were only loaded but did not produce code.
- [ ] Read skill version from YAML frontmatter (`metadata.version`) for each entry
- [ ] Append entries to `aidlc-docs/skill-feedback.md`

## SKILL FEEDBACK CHECK Block

Consuming stages include a block that follows this pattern:

```
### SKILL FEEDBACK CAPTURE
IF `aidlc-state.md` → Organizational Skills section lists any consumed skills:
  1. Load the list of consumed Skill IDs
  2. For each Skill ID that ACTIVELY GENERATED CODE in this unit/build:
     a. Read the skill version from YAML frontmatter (`metadata.version`)
     b. Evaluate the result: ok | correction | gap
        - "ok" only when skill patterns actively produced code that passed validation
        - Do NOT record "ok" for skills merely loaded but not used to generate code
     c. If correction or gap: describe the specific issue
     d. Assign severity: low | medium | high
     e. Append row to `aidlc-docs/skill-feedback.md` including Version column
  3. If file does not exist, create it with the header template above
ELSE:
  Skip — no skills consumed, no feedback to capture
```

## Aggregation at Closure

During Project Handoff (Step 5: Lessons Learned), feedback is aggregated into a **Skill Health Report**. See `closure/project-handoff.md` for the aggregation procedure and report format.

## Key Principles

- **Non-blocking**: Feedback capture NEVER blocks stage progression. It is recorded alongside existing steps, not as a gate.
- **Skill-scoped**: Feedback is always tied to a specific Skill ID. Generic code issues are NOT skill feedback — they belong in the code review report.
- **Cumulative**: Each project accumulates its own feedback log. Cross-project aggregation happens via the `collect-feedback.sh` script (see `scripts/`).
- **Actionable**: Every `correction` and `gap` entry must include enough detail for the skill maintainer to understand and act on it.
- **Agnostic**: This system works with any IDE, agent, or model — it's pure Markdown state tracking.
