# Changelog Entry Templates

## Section Headers

```markdown
### 🚀 Added
### 🔄 Changed
### ⚠️ Deprecated
### ❌ Removed
### 🐞 Fixed
### 🔐 Security
```

## Entry Patterns

> **Note:** Section headers already provide the verb. Entries describe WHAT, not the action.

### Feature Addition (🚀 Added)

```markdown
- User profile management with avatar upload [(#XXXX)](link)
- GET /api/users endpoint for user listing [(#XXXX)](link)
- Dark mode toggle in application settings [(#XXXX)](link)
```

### Behavior Change (🔄 Changed)

```markdown
- Dashboard layout from flex to CSS grid [(#XXXX)](link)
- Pagination limit from 10 to 25 items per page [(#XXXX)](link)
- Error messages now include error codes [(#XXXX)](link)
```

### Bug Fix (🐞 Fixed)

```markdown
- Form validation failing on special characters [(#XXXX)](link)
- Memory leak in dashboard component on unmount [(#XXXX)](link)
- Pagination breaking when navigating to last page [(#XXXX)](link)
```

### Security Patch (🔐 Security)

```markdown
- axios from 1.5.0 to 1.6.0 (CVE-2023-45857) [(#XXXX)](link)
- SQL injection vulnerability in search endpoint [(#XXXX)](link)
- XSS vulnerability in user comments [(#XXXX)](link)
```

### Deprecation (⚠️ Deprecated)

```markdown
- Legacy /api/v1/users endpoint, use /api/v2/users [(#XXXX)](link)
- OldComponent, will be removed in v3.0.0 [(#XXXX)](link)
```

### Removal (❌ Removed)

```markdown
- Deprecated /api/v1/legacy endpoint [(#XXXX)](link)
- Support for Node.js 16 [(#XXXX)](link)
```

## Version Header Templates

### Unreleased

```markdown
## [Unreleased]
```

### Released

```markdown
## [1.2.0] - 2024-01-15

---
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

- Initial user management module [(#100)](link)
- Authentication with Happy library [(#101)](link)

### 🐞 Fixed

- Application crash on invalid token [(#102)](link)

---
```
