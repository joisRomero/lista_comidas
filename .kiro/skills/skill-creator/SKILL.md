---
name: skill-creator
description: >
  Creates new AI agent skills following the ANTA conventions.
  Trigger: When user asks to create a new skill, add agent instructions, or document patterns for AI.
metadata:
  author: anta
  version: "1.0"
  scope: [root]
  auto_invoke: "Creating new skills"
  phase: null
  layer: null
  validates_with: null
  validation_profile: null
---

## When to Create a Skill

Create a skill when:
- A pattern is used repeatedly and AI needs guidance
- Project-specific conventions differ from generic best practices
- Complex workflows need step-by-step instructions
- Decision trees help AI choose the right approach

**Don't create a skill when:**
- Documentation already exists (create a reference instead)
- Pattern is trivial or self-explanatory
- It's a one-off task

---

## Skill Structure

```
skills/{skill-name}/
├── SKILL.md              # Required - main skill file
├── assets/               # Optional - templates, schemas, examples
│   ├── template.sql
│   └── schema.json
└── references/           # Optional - links to local docs
    └── docs.md
```

---

## SKILL.md Template

```markdown
---
name: {skill-name}
description: >
  {One-line description of what this skill does}.
  Trigger: {When the AI should load this skill}.
metadata:
  author: anta
  version: "1.0"
  scope: [root]              # [root], [api], [ui], or specific paths
  auto_invoke: "{keywords}"  # Comma-separated trigger words
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| {Rule description} | ALWAYS/NEVER | {Why this matters} |

## Naming Conventions

| Object | Pattern | Example |
|--------|---------|---------|
| {Object type} | {Pattern} | {Concrete example} |

## Code Patterns

### {Pattern Name}
{Minimal example - max 20 lines}

## Commands

```bash
{Common commands with copy-paste examples}
```

## Resources

- **Templates**: See [assets/](assets/) for {description}
- **References**: See [references/](references/) for local docs
```

---

## Naming Conventions

| Type | Pattern | Examples |
|------|---------|----------|
| Generic skill | `{technology}` | `react`, `typescript`, `playwright` |
| ANTA-specific | `anta-{component}` | `anta-api`, `anta-ui` |
| Internal library | `{library-name}` | `happy`, `lion`, `arroba` |
| Database | `database` | SQL Server patterns |
| Workflow skill | `{action}-{target}` | `skill-creator` |

---

## Decision: assets/ vs references/

```
Need code templates?        → assets/
Need SQL templates?         → assets/
Need JSON schemas?          → assets/
Link to existing docs?      → references/
Link to internal wikis?     → references/
```

**Key Rule**: Keep SKILL.md under 200 lines. Heavy content goes to assets/.

---

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier (lowercase, hyphens) |
| `description` | Yes | What + Trigger in one block |
| `metadata.author` | Yes | `anta` for internal skills |
| `metadata.version` | Yes | Semantic version as string |
| `metadata.scope` | Yes | Where this skill applies |
| `metadata.auto_invoke` | No | Keywords that trigger auto-load |

---

## Content Guidelines

### DO
- Start with Critical Rules (ALWAYS/NEVER table)
- Use tables for naming conventions and decision trees
- Keep code examples minimal (max 20 lines each)
- Include Commands section with copy-paste commands
- Reference assets/ for complete templates

### DON'T
- Duplicate content from existing docs
- Include lengthy explanations
- Add troubleshooting sections (keep focused)
- Put complete templates inline (use assets/)
- Exceed 200 lines in SKILL.md

---

## Registering the Skill

After creating the skill, add it to root `AGENTS.md`:

**Skills table:**
```markdown
| `{skill-name}` | {Description} | [SKILL.md](skills/{skill-name}/SKILL.md) |
```

**Auto-invoke table:**
```markdown
| {Action description} | `{skill-name}` |
```

---

## Checklist Before Creating

- [ ] Skill doesn't already exist (check `skills/`)
- [ ] Pattern is reusable (not one-off)
- [ ] Name follows conventions
- [ ] Frontmatter is complete
- [ ] Critical Rules are clear (ALWAYS/NEVER)
- [ ] Code examples are minimal (<20 lines)
- [ ] Heavy templates moved to assets/
- [ ] Added to AGENTS.md

## Resources

- **Templates**: See [assets/](assets/) for SKILL.md template
