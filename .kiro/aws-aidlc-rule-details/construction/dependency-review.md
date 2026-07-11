# Dependency Review - Detailed Steps

## Purpose
**Validate third-party dependencies for security, licensing, and maintainability**

Dependency Review focuses on:
- Identifying security vulnerabilities in dependencies
- Validating license compatibility with project requirements
- Assessing dependency health and maintenance status
- Ensuring dependencies align with organizational standards

**Note**: This stage should execute before or during Code Generation to catch issues early.

## Prerequisites
- Application Design should be complete
- Technology stack has been defined
- Initial dependency list can be identified from design artifacts

## Intelligent Assessment Guidelines

**WHEN TO EXECUTE DEPENDENCY REVIEW**: Use this assessment:

### Execute IF:
- New dependencies are being introduced
- Major version upgrades of existing dependencies
- Security-sensitive application (fintech, healthcare, etc.)
- Dependencies with copyleft or restrictive licenses
- Dependencies from unfamiliar or less-established sources

### Lighter Review IF:
- Minor version updates of established dependencies
- Well-known, widely-used libraries (React, Spring, Express, etc.)
- Dependencies already approved in organizational registry

---

## Step-by-Step Execution

### Step 1: Inventory Dependencies
- [ ] List all direct dependencies from design/planning artifacts
- [ ] Identify transitive dependencies (dependencies of dependencies)
- [ ] Categorize by type (runtime, development, testing)
- [ ] Create `aidlc-docs/construction/dependency-review/dependency-inventory.md`

### Step 2: Security Assessment
- [ ] Check dependencies against known vulnerability databases
  - CVE databases
  - GitHub Security Advisories
  - npm audit / pip audit / OWASP Dependency-Check (as applicable)
- [ ] Identify vulnerabilities by severity (Critical, High, Medium, Low)
- [ ] Document remediation options for identified vulnerabilities
- [ ] Assess risk of vulnerable dependencies

### Step 3: License Review
- [ ] Identify license for each dependency
- [ ] Check license compatibility with project license
- [ ] Flag any copyleft licenses (GPL, AGPL) for review
- [ ] Flag any commercial or proprietary licenses
- [ ] Document license obligations (attribution, source disclosure, etc.)

### Step 4: Health Assessment
- [ ] Check last update date for each dependency
- [ ] Review maintenance status (active, deprecated, abandoned)
- [ ] Check issue/PR response time as indicator of health
- [ ] Identify dependencies with single maintainer risk
- [ ] Flag dependencies with limited community support

### Step 5: Generate Dependency Report
- [ ] Create `aidlc-docs/construction/dependency-review/dependency-report.md` with:

```markdown
# Dependency Review Report

## Date
[YYYY-MM-DD]

## Summary
- Total dependencies: [N]
- Direct: [N] | Transitive: [N]
- Security issues found: [N]
- License concerns: [N]
- Health concerns: [N]

## Security Findings

| Dependency | Version | Vulnerability | Severity | Remediation |
|------------|---------|---------------|----------|-------------|
| [name] | [ver] | [CVE-XXXX] | Critical | Upgrade to X.X |

## License Summary

| License Type | Count | Dependencies |
|--------------|-------|--------------|
| MIT | [N] | [list] |
| Apache 2.0 | [N] | [list] |
| GPL 3.0 | [N] | [list] ⚠️ |

## Health Concerns

| Dependency | Concern | Risk | Recommendation |
|------------|---------|------|----------------|
| [name] | Last update 2+ years ago | Medium | Consider alternative |

## Recommendations
[List of action items]

## Approval Status
- [ ] Security findings reviewed
- [ ] License compliance confirmed
- [ ] Health risks accepted
```

### Step 6: Handle Findings
If issues are identified:
- [ ] Present findings to user with recommendations
- [ ] For critical security issues: Recommend blocking until resolved
- [ ] For license issues: Determine legal/compliance impact
- [ ] For health issues: Recommend alternatives or risk acceptance

### Step 7: Log Approval Prompt
- [ ] Log approval prompt with timestamp in `aidlc-docs/audit.md`
- [ ] Include summary of findings and recommendations
- [ ] Use ISO 8601 timestamp format

### Step 8: Present Completion Message

```markdown
# 📦 Dependency Review Complete

[AI-generated summary of dependency review in bullet points]

> **📋 REVIEW REQUIRED:**  
> Please examine the dependency report at: `aidlc-docs/construction/dependency-review/dependency-report.md`



> **🚀 WHAT'S NEXT?**
>
> **You may:**
>
> - 🔧 **Address Issues** - Resolve security/license/health issues before proceeding
> ⚠️ **Accept Risks** - Document accepted risks and proceed
> - ✅ **Approve & Continue** - All dependencies approved, proceed to **Code Generation**

---
```

### Step 9: Wait for Explicit Approval
- [ ] Do not proceed until user explicitly approves dependency review
- [ ] Critical security issues should block progression
- [ ] Document any accepted risks in audit.md

### Step 10: Update Progress
- [ ] Mark Dependency Review complete in `aidlc-docs/aidlc-state.md`
- [ ] Update the "Current Status" section
- [ ] Carry forward any accepted risks to project documentation

---

## Critical Rules

### Security First
- Critical vulnerabilities should block Code Generation
- High vulnerabilities require explicit risk acceptance
- Document all security decisions

### License Compliance
- Copyleft licenses require legal review
- Commercial licenses may require procurement
- All license obligations must be documented

### Ongoing Monitoring
- Dependency review is not one-time
- Re-run during major updates or before releases
- Integrate with CI/CD for continuous monitoring

## Common Vulnerability Sources

- **npm**: `npm audit`, Snyk, GitHub Dependabot
- **Python**: `pip-audit`, Safety, Snyk
- **Java/Maven**: OWASP Dependency-Check, Snyk
- **Go**: `govulncheck`, Snyk
- **.NET**: `dotnet list package --vulnerable`
