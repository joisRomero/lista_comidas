---
name: skill-sync
description: >
  Syncs skill metadata to AGENTS.md Auto-invoke section.
  Trigger: After creating/modifying a skill, regenerating Auto-invoke table.
metadata:
  author: anta
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "After creating/modifying a skill"
    - "Regenerate AGENTS.md Auto-invoke table"
  phase: null
  layer: null
  validates_with: null
  validation_profile: null
---

## Purpose

Keeps AGENTS.md Auto-invoke section in sync with skill metadata. When you create or modify a skill, run the sync script to automatically update the table.

## Required Skill Metadata

Each skill that should appear in Auto-invoke needs these fields in frontmatter:

```yaml
metadata:
  scope: [root]                    # Always root for ANTA (single AGENTS.md)
  auto_invoke: "Action description"  # Or list of actions
```

### auto_invoke Options

```yaml
# Option A: single action
auto_invoke: "Creating stored procedures"

# Option B: multiple actions
auto_invoke:
  - "Creating stored procedures"
  - "Modifying SP templates"
```

---

## Usage

### After Creating/Modifying a Skill

```bash
./skills/skill-sync/assets/sync.sh
```

### Dry Run (Preview Changes)

```bash
./skills/skill-sync/assets/sync.sh --dry-run
```

---

## What It Does

1. Reads all `skills/*/SKILL.md` files
2. Extracts `metadata.auto_invoke` from frontmatter
3. Generates Auto-invoke table
4. Updates the `## Auto-invoke Skills` section in `AGENTS.md`

---

## Example

Given this skill metadata:

```yaml
# skills/database-sp/SKILL.md
metadata:
  scope: [root]
  auto_invoke:
    - "Creating stored procedures"
    - "SP with pagination, transactions"
```

The sync script generates in `AGENTS.md`:

```markdown
## Auto-invoke Skills

| Action | Skill |
|--------|-------|
| Creating stored procedures | `database-sp` |
| SP with pagination, transactions | `database-sp` |
```

---

## Checklist After Modifying Skills

- [ ] Added `metadata.auto_invoke` to new/modified skill
- [ ] Ran `./skills/skill-sync/assets/sync.sh`
- [ ] Verified AGENTS.md updated correctly
