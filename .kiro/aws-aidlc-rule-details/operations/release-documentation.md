# Release Documentation - Detailed Steps

## Purpose
**Create comprehensive release documentation for production deployment**

Release Documentation focuses on:
- Documenting all information needed for production deployment
- Providing clear deployment instructions and configurations
- Capturing environment requirements and dependencies
- Enabling operations team to deploy without developer assistance

**Note**: This stage produces documentation only, not automated deployment. Deployment execution is handled by operations teams or CI/CD pipelines.

## Prerequisites
- Build & Test must be complete
- Code Review must be approved
- All units are ready for release
- Version number has been determined

---

## Step-by-Step Execution

### Step 1: Gather Release Context
- [ ] Collect all completed units and their artifacts
- [ ] Review build and test results
- [ ] Identify release version (semantic versioning recommended)
- [ ] Determine target environments (staging, production)

### Step 2: Create Release Package Inventory
- [ ] List all artifacts to be deployed:
  - Application binaries/packages
  - Database migration scripts
  - Configuration files
  - Static assets
  - Infrastructure changes (if any)
- [ ] Document artifact versions and checksums

### Step 3: Document Environment Requirements
- [ ] Create `aidlc-docs/operations/release/environment-requirements.md`:
  - Runtime requirements (language versions, frameworks)
  - System dependencies (OS, libraries)
  - Infrastructure requirements (compute, memory, storage)
  - Network requirements (ports, protocols, endpoints)
  - Third-party service dependencies

### Step 4: Document Configuration
- [ ] Create `aidlc-docs/operations/release/configuration-guide.md`:
  - All configuration parameters
  - Environment-specific values (without secrets)
  - Feature flags and their states
  - Integration endpoints
  - Placeholder locations for secrets (do not document actual secrets)

### Step 5: Create Deployment Instructions
- [ ] Create `aidlc-docs/operations/release/deployment-instructions.md`:

```markdown
# Deployment Instructions - Release [VERSION]

## Pre-Deployment Checklist
- [ ] Backup current production state
- [ ] Verify target environment is accessible
- [ ] Confirm all dependencies are available
- [ ] Notify stakeholders of deployment window
- [ ] Prepare rollback plan

## Deployment Steps

### Step 1: [First Action]
**Description**: [What this step does]
**Command/Action**: 
```
[specific command or action]
```
**Expected Result**: [What should happen]
**Verification**: [How to verify success]

### Step 2: [Second Action]
...

## Post-Deployment Verification
- [ ] Health check endpoints respond correctly
- [ ] Key functionality smoke test passes
- [ ] Logs show no errors
- [ ] Monitoring dashboards show normal metrics

## Rollback Procedure
### When to Rollback
- [Criteria that trigger rollback]

### Rollback Steps
1. [Step 1]
2. [Step 2]
...

## Support Contacts
- Technical Lead: [name/contact]
- Operations: [name/contact]
- On-call: [escalation path]
```

### Step 6: Document Database Changes
If database changes exist:
- [ ] Create `aidlc-docs/operations/release/database-changes.md`:
  - Migration scripts in order
  - Rollback scripts
  - Data transformation requirements
  - Backup requirements
  - Estimated migration duration

### Step 7: Create Release Notes
- [ ] Create `aidlc-docs/operations/release/release-notes.md`:

```markdown
# Release Notes - Version [VERSION]

## Release Date
[YYYY-MM-DD]

## Summary
[Brief description of this release]

## New Features
- [Feature 1]: [Description]
- [Feature 2]: [Description]

## Improvements
- [Improvement 1]: [Description]

## Bug Fixes
- [Fix 1]: [Description] (Fixes #[issue])

## Breaking Changes
- [Change 1]: [Description and migration path]

## Known Issues
- [Issue 1]: [Description and workaround]

## Dependencies Updated
- [Dependency]: [old version] → [new version]

## Related Stories/Tickets
- [Story/Ticket references]
```

### Step 8: Compile Release Package
- [ ] Create `aidlc-docs/operations/release/release-manifest.md`:
  - Complete list of documents in release package
  - Artifact locations
  - Version information
  - Approval status

### Step 9: Log Release Documentation
- [ ] Log completion with timestamp in `aidlc-docs/audit.md`
- [ ] Include release version and summary
- [ ] Use ISO 8601 timestamp format

### Step 10: Present Completion Message

```markdown
# 📄 Release Documentation Complete - Version [VERSION]

[AI-generated summary of release documentation in bullet points]

> **📋 DOCUMENTATION READY:**  
> Please examine the release documentation at: `aidlc-docs/operations/release/`
>
> **Documents created:**
> - environment-requirements.md
> - configuration-guide.md
> - deployment-instructions.md
> - database-changes.md (if applicable)
> - release-notes.md
> - release-manifest.md



> **🚀 WHAT'S NEXT?**
>
> **Release documentation is ready for:**
>
> 👥 **Operations Handoff** - Share with operations team for deployment
> 🔍 **Review** - Technical review of deployment instructions
> - ✅ **Approve & Proceed** - Documentation approved, proceed to **CLOSURE** phase

---
```

### Step 11: Wait for Explicit Approval
- [ ] Do not proceed until user explicitly approves release documentation
- [ ] If changes requested, update documentation
- [ ] Document approval in audit.md

### Step 12: Update Progress
- [ ] Mark Release Documentation complete in `aidlc-docs/aidlc-state.md`
- [ ] Update the "Current Status" section
- [ ] Prepare for transition to CLOSURE phase

---

## Critical Rules

### Documentation Completeness
- Operations team should be able to deploy using documentation alone
- No tribal knowledge required
- All steps must be explicit and verifiable

### Security
- Never include actual secrets, passwords, or API keys
- Use placeholders with clear naming
- Reference secure secret management procedures

### Rollback Requirements
- Every release must have rollback procedure
- Rollback should be tested before production deployment
- Rollback criteria must be clearly defined

### Version Control
- All release documentation should be version-controlled
- Tag documentation with release version
- Maintain history of release documents

## Release Documentation Checklist

```markdown
## Release [VERSION] Checklist

### Documentation
- [ ] Environment requirements documented
- [ ] Configuration guide complete
- [ ] Deployment instructions verified
- [ ] Database changes documented (if any)
- [ ] Release notes finalized
- [ ] Rollback procedure included

### Approvals
- [ ] Technical Lead approved
- [ ] Operations reviewed
- [ ] Security reviewed (if applicable)

### Handoff
- [ ] Operations team briefed
- [ ] Support team notified
- [ ] Stakeholders informed of release window
```
