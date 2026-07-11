---
name: changelog
description: >
  Manages changelog entries following keepachangelog.com format.
  Trigger: When creating PRs, adding changelog entries, or working with CHANGELOG.md.
metadata:
  author: anta
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Add changelog entry for a PR or feature"
    - "Update CHANGELOG.md"
    - "Create PR that requires changelog entry"
  phase: [operations, closure]
  layer: null
  validates_with: null
  validation_profile: null
---

## Changelog Location

Each project should have a `CHANGELOG.md` in the root directory.

## Format Rules (keepachangelog.com)

### Section Order (ALWAYS this order)

```markdown
## [Unreleased]

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
```

### Emoji Prefixes (REQUIRED)

| Section | Emoji | Usage |
|---------|-------|-------|
| Added | `### 🚀 Added` | New features, endpoints, components |
| Changed | `### 🔄 Changed` | Modifications to existing functionality |
| Deprecated | `### ⚠️ Deprecated` | Features marked for removal |
| Removed | `### ❌ Removed` | Deleted features |
| Fixed | `### 🐞 Fixed` | Bug fixes |
| Security | `### 🔐 Security` | Security patches, CVE fixes |

### Entry Format

```markdown
### 🚀 Added

- Description of feature [(#XXXX)](link-to-pr)
- Another feature [(#YYYY)](link-to-pr)

### 🐞 Fixed

- Description of fix [(#ZZZZ)](link-to-pr)
```

**Rules:**
- **Blank line after section header** before first entry
- **Blank line between sections**
- Be specific: what changed, not why (that's in the PR)
- One entry per PR
- No period at the end
- Do NOT start with redundant verbs (section header provides the action)

### Semantic Versioning Rules

Follow [semver.org](https://semver.org/):

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Bug fixes, patches | PATCH (x.y.**Z**) | 1.0.1 → 1.0.2 |
| New features (backwards compatible) | MINOR (x.**Y**.0) | 1.0.2 → 1.1.0 |
| Breaking changes, removals | MAJOR (**X**.0.0) | 1.1.0 → 2.0.0 |

**CRITICAL:** `### ❌ Removed` entries MUST only appear in MAJOR version releases.

### Released Versions Are Immutable

**NEVER modify already released versions.** Once a version is released, its changelog section is frozen.

### Version Header Format

```markdown
## [Unreleased]

### 🚀 Added

- New feature here

---

## [1.2.0] - 2024-01-15

### 🚀 Added

- Previous released feature
```

## Adding a Changelog Entry

### Step 1: Determine Change Type

| Change | Section |
|--------|---------|
| New feature, endpoint, component | 🚀 Added |
| Behavior change, refactor | 🔄 Changed |
| Bug fix | 🐞 Fixed |
| CVE patch, security improvement | 🔐 Security |
| Feature removal | ❌ Removed |
| Deprecation notice | ⚠️ Deprecated |

### Step 2: Add Entry to Unreleased Section

```markdown
## [Unreleased]

### 🐞 Fixed

- Button alignment in dashboard header [(#123)](https://github.com/org/repo/pull/123)
```

## Examples

### Good Entries

```markdown
### 🚀 Added

- User profile management endpoint [(#123)](link)
- Dark mode toggle in settings [(#124)](link)

### 🐞 Fixed

- Form validation failing on special characters [(#125)](link)
- Memory leak in dashboard component [(#126)](link)

### 🔐 Security

- Dependencies updated to patch CVE-2024-1234 [(#127)](link)
```

### Bad Entries

```markdown
- Fixed bug.                              # Too vague, has period
- Added new feature for users             # Missing PR link, redundant verb
- Add search bar [(#123)]                 # Redundant verb
- This PR adds a cool new thing (#123)    # Wrong link format, conversational
```

## Commands

```bash
# View current UNRELEASED section
head -50 CHANGELOG.md

# Check if changelog was updated in branch
git diff main...HEAD -- CHANGELOG.md
```

## Full Entry Example

```markdown
## [Unreleased]

### 🚀 Added

- User profile management with avatar upload [(#123)](link)
- Export to PDF functionality in reports [(#124)](link)

### 🔄 Changed

- Dashboard layout now uses grid instead of flex [(#125)](link)

### 🐞 Fixed

- Login form not validating email format [(#126)](link)
- Pagination breaking on last page [(#127)](link)

### 🔐 Security

- Updated axios to 1.6.0 to patch CVE-2023-45857 [(#128)](link)

---

## [1.2.0] - 2024-01-15

### 🚀 Added

- Initial user management module
```

## Resources

- **Templates**: See [assets/entry-templates.md](assets/entry-templates.md)
- **keepachangelog.com**: https://keepachangelog.com/en/1.1.0/
