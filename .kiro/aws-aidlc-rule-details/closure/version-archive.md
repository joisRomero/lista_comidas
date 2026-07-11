# Version & Archive - Detailed Steps

## Purpose
**Version project artifacts and archive for long-term preservation**

Version & Archive focuses on:
- Applying consistent version tags across all project artifacts
- Creating immutable archive of project state
- Enabling precise project restoration at any version
- Maintaining traceability between code and documentation

**Note**: This stage creates a permanent record that should not be modified after creation.

## Prerequisites
- Project Snapshot must be complete
- All artifacts are finalized
- Version number is confirmed

---

## Step-by-Step Execution

### Step 1: Determine Version Number
- [ ] Confirm release version follows semantic versioning (MAJOR.MINOR.PATCH)
- [ ] Verify version is not already used
- [ ] Document version in snapshot

### Step 2: Version Documentation
- [ ] Create versioned documentation directory:
  ```
  aidlc-docs/
  ├── v[X.Y.Z]/                    ← Archived version
  │   ├── inception/
  │   ├── construction/
  │   ├── operations/
  │   ├── closure/
  │   └── VERSION.md
  └── current -> v[X.Y.Z]          ← Symlink to latest
  ```
- [ ] Copy current documentation to versioned directory
- [ ] Create VERSION.md in versioned directory

### Step 3: Create Version Manifest
- [ ] Create `aidlc-docs/v[X.Y.Z]/VERSION.md`:

```markdown
# Version [X.Y.Z]

## Version Information
- **Version**: [X.Y.Z]
- **Release Date**: [YYYY-MM-DD]
- **Archive Date**: [YYYY-MM-DD]
- **Git Tag**: v[X.Y.Z]
- **Git Commit**: [full SHA]

## Version Contents

### Code Repositories
| Repository | Branch | Commit | Tag |
|------------|--------|--------|-----|
| [repo-back] | main | [SHA] | v[X.Y.Z] |
| [repo-front] | main | [SHA] | v[X.Y.Z] |

### Documentation
| Document | Path | Status |
|----------|------|--------|
| Project Snapshot | closure/project-snapshot.md | ✅ |
| Requirements | inception/requirements/ | ✅ |
| User Stories | inception/user-stories/ | ✅ |
| API Contracts | inception/api-contracts/ | ✅ |
| ADRs | inception/adrs/ | ✅ |
| Release Docs | operations/release/ | ✅ |

### Artifacts
| Artifact | Location | Checksum |
|----------|----------|----------|
| [artifact] | [location] | [SHA256] |

## Changes Since Previous Version
[Summary of changes from previous version, or "Initial Release"]

## Verification
- [ ] All documents archived
- [ ] Git tags applied
- [ ] Checksums recorded
- [ ] Archive tested for restoration
```

### Step 4: Apply Git Tags
- [ ] Tag code repositories with version:
  ```
  git tag -a v[X.Y.Z] -m "Release [X.Y.Z]: [brief description]"
  ```
- [ ] Push tags to remote repositories
- [ ] Verify tags are accessible

### Step 5: Create Archive Package (Optional)
If offline archive is required:
- [ ] Create compressed archive of documentation
- [ ] Include code snapshots if required
- [ ] Generate checksums for archive files
- [ ] Store in designated archive location

### Step 6: Update Version Registry
- [ ] Create or update `aidlc-docs/VERSION-HISTORY.md`:

```markdown
# Version History

| Version | Date | Type | Summary |
|---------|------|------|---------|
| [X.Y.Z] | [date] | [Major/Minor/Patch] | [brief summary] |
| [X.Y.Z-1] | [date] | [type] | [summary] |

## Active Versions
- **Current**: v[X.Y.Z]
- **Previous**: v[X.Y.Z-1]

## Archived Versions
| Version | Archive Location | Status |
|---------|------------------|--------|
| v[X.Y.Z] | aidlc-docs/v[X.Y.Z]/ | Active |
```

### Step 7: Verify Archive Integrity
- [ ] Confirm all files are properly archived
- [ ] Verify git tags are correct
- [ ] Test that archived version can be restored
- [ ] Validate checksums if created

### Step 8: Log Archive Creation
- [ ] Log completion with timestamp in `aidlc-docs/audit.md`
- [ ] Include version and archive details
- [ ] Use ISO 8601 timestamp format

### Step 9: Present Completion Message

```markdown
# 📦 Version & Archive Complete

**Version [X.Y.Z] has been archived**

[AI-generated summary of archiving in bullet points]

> **📋 ARCHIVE CREATED:**  
> - Documentation: `aidlc-docs/v[X.Y.Z]/`
> - Git Tag: `v[X.Y.Z]`
> - Version History: `aidlc-docs/VERSION-HISTORY.md`



> **🚀 WHAT'S NEXT?**
>
> - ✅ **Proceed to Stakeholder Sign-off** - Continue closure process

---
```

### Step 10: Update Progress
- [ ] Mark Version & Archive complete in `aidlc-docs/aidlc-state.md`
- [ ] Proceed to Stakeholder Sign-off stage

---

## Critical Rules

### Immutability
- Archived versions must not be modified
- Any changes require new version
- Preserve original state exactly

### Traceability
- Version must link code and documentation
- Git commits must be recorded
- All artifacts must be identifiable

### Recoverability
- Archives must be restorable
- Verify restoration process
- Document restoration steps
