# ISO 27001:2022 Assessment (Adaptive)

**Assume the role** of a security architect

**Adaptive Phase**: Always executes. Detail level adapts to project risk and data sensitivity.

**See [depth-levels.md](../common/depth-levels.md) for adaptive depth explanation**

## Purpose
**Assess ISO/IEC 27001:2022 compliance needs based on project scope.**

This is a lightweight assessment to identify relevant Annex A controls for the project being built. It is NOT a full organizational audit, but a project-specific security scoping exercise. Based on ISO/IEC 27001:2022 and its companion guide ISO/IEC 27002:2022.

## Prerequisites
- Requirements Analysis must be complete
- User Stories must be complete (if applicable)

## Execution Steps

### Step 1: Load Prior Context
- [ ] Load `aidlc-docs/inception/requirements/requirements.md`
- [ ] Load `aidlc-docs/inception/user-stories/user-stories.md` (if available)
- [ ] Identify data types (PII, financial, intellectual property), exposure (internal/external), and regulatory context.

### Step 2: Determine Assessment Depth
**Based on project risk, determine depth:**

- **Minimal Depth** - Use when:
  - Low-risk internal tools
  - No PII or sensitive data
  - Limited exposure
  - *Action*: Tag applicable control domains only, no deep analysis.

- **Standard Depth** - Use when:
  - Normal business applications
  - Standard user data
  - Internal or authenticated external access
  - *Action*: Identify applicable controls, map to requirements, note security considerations.

- **Comprehensive Depth** - Use when:
  - High-risk systems
  - PII, financial data, or critical infrastructure
  - Public-facing or high-exposure
  - *Action*: Full control mapping, risk assessment, and detailed compliance requirements document.

### Step 3: Generate Clarifying Questions (Conditional)
**IF depth is Standard or Comprehensive**:
- [ ] Create `aidlc-docs/inception/iso-27001/security-verification-questions.md`
- [ ] Ask about data residency, encryption requirements, access control policies, and third-party integrations.
- [ ] Request user to fill in all [Answer]: tags directly in the document.
- [ ] Wait for user answers before proceeding.

### Step 4: Identify Applicable Controls (ISO 27001:2022 Annex A)
- [ ] Evaluate which of the **4 control categories** (93 controls total) apply to THIS project:

  **A.5 Organizational Controls** (37 controls):
  - **A.5.1** Policies for information security
  - **A.5.2** Information security roles and responsibilities
  - **A.5.3** Segregation of duties
  - **A.5.7** Threat intelligence *(NEW in 2022)*
  - **A.5.8** Information security in project management
  - **A.5.10** Acceptable use of information and assets
  - **A.5.14** Information transfer
  - **A.5.15** Access control
  - **A.5.16** Identity management
  - **A.5.17** Authentication information
  - **A.5.19-A.5.22** Supplier/cloud security
  - **A.5.23** Information security for cloud services *(NEW in 2022)*
  - **A.5.24-A.5.28** Incident management and evidence collection
  - **A.5.29-A.5.30** Business continuity and ICT readiness
  - **A.5.31-A.5.36** Legal, regulatory, and compliance requirements
  - **A.5.37** Documented operating procedures
  - *(Select only controls relevant to THIS project — skip organizational-level controls)*

  **A.6 People Controls** (8 controls):
  - **A.6.1** Screening
  - **A.6.2** Terms and conditions of employment
  - **A.6.3** Information security awareness and training
  - **A.6.5** Responsibilities after termination
  - **A.6.7** Remote working
  - **A.6.8** Information security event reporting
  - *(Typically minimal for software projects unless team onboarding/offboarding is in scope)*

  **A.7 Physical Controls** (14 controls):
  - **A.7.4** Physical security monitoring
  - **A.7.9** Security of assets off-premises
  - **A.7.10** Storage media
  - **A.7.14** Secure disposal or re-use of equipment
  - *(Usually applicable only if project involves hosting infrastructure or physical devices)*

  **A.8 Technological Controls** (34 controls):
  - **A.8.1** User endpoint devices
  - **A.8.2** Privileged access rights
  - **A.8.3** Information access restriction
  - **A.8.4** Access to source code
  - **A.8.5** Secure authentication
  - **A.8.7** Protection against malware
  - **A.8.8** Management of technical vulnerabilities
  - **A.8.9** Configuration management *(NEW in 2022)*
  - **A.8.10** Information deletion *(NEW in 2022)*
  - **A.8.11** Data masking *(NEW in 2022)*
  - **A.8.12** Data leakage prevention *(NEW in 2022)*
  - **A.8.13-A.8.14** Information backup and redundancy
  - **A.8.15-A.8.16** Logging and monitoring activities *(NEW in 2022)*
  - **A.8.20-A.8.22** Network security and web filtering *(NEW in 2022)*
  - **A.8.23-A.8.24** Segregation of networks and use of cryptography
  - **A.8.25-A.8.27** Secure development lifecycle and security testing
  - **A.8.28** Secure coding *(NEW in 2022)*
  - **A.8.31-A.8.34** Development/test environments, change management, and system testing
  - *(Most software projects will have significant applicability in this category)*

### Step 5: Map Controls to Requirements
- [ ] Link identified controls to functional and non-functional requirements.
- [ ] Ensure security is integrated into the project's core features.

### Step 6: Generate Security Considerations
- [ ] For each applicable domain, define what the development team must consider.
- [ ] Focus on actionable guidance for the Construction phase.

### ⛔ GATE: Review Security Context
DO NOT proceed to Step 7 until all security context is clear and any clarifying questions are answered.

### Step 7: Create ISO 27001 Assessment Document
- [ ] Create `aidlc-docs/inception/iso-27001/iso-27001-assessment.md` with the following structure:
  - **Project Security Profile**: Data types, exposure level, regulatory context.
  - **Applicable Control Domains**: List with relevance justification.
  - **Control-to-Requirement Mapping**: Traceability matrix.
  - **Security Considerations for Development**: Actionable guidelines.
  - **Recommended Security Testing**: Verification steps for Build & Test.

### Step 7b: Self-Validation Gate (before presenting for approval)

Before presenting the assessment for user approval, verify internal consistency:
- [ ] **Summary ↔ Body**: Every control category listed in the Compliance Summary section must appear in the Applicable Controls body (and vice versa). No phantom entries.
- [ ] **Control status**: Every row in the control mapping table has a status indicator (✅ Implemented / ⚠️ Partial / ❌ Not applicable / 🔄 Delegated). No blank status cells.
- [ ] **Provider terminology**: If source code repository controls are mentioned (A.8.4, A.8.25-A.8.27), verify correct provider terminology per `security` skill → "Source Code Repository Security" table (e.g., "Approval Rule Templates" for CodeCommit, NOT "branch protection").
- [ ] **Open Items numbered**: Any items deferred to later stages are numbered (ISO-OI-01, ISO-OI-02, etc.) and listed in a dedicated "Open Items" section at the end.

### Step 8: Update State Tracking
- [ ] Update `aidlc-docs/aidlc-state.md`:
```markdown
## Stage Progress
### 🔵 INCEPTION PHASE
...
- [x] ISO 27001 Assessment
```

### Step 9: Log and Proceed
- [ ] Log approval prompt with timestamp in `aidlc-docs/audit.md`
- [ ] Present completion message:

```markdown
# 🛡️ ISO 27001 Assessment Complete

[AI-generated summary of the security profile and key applicable control domains]

> **📋 REVIEW REQUIRED:**  
> Please examine the assessment document at: `aidlc-docs/inception/iso-27001/iso-27001-assessment.md`

> **🚀 WHAT'S NEXT?**
>
> **You may:**
>
> - 🔧 **Request Changes** - Ask for modifications to the security assessment
> - ✅ **Approve & Continue** - Approve the assessment and proceed to **[Spike/POC / API Contract Design]**

---
```

## Critical Rules

### Scoping Accuracy
- Focus ONLY on controls relevant to the software project.
- Do not include organizational-level controls (e.g., office physical security) unless directly relevant to the hosting environment.

### Actionable Guidance
- Security considerations must be specific enough for developers to implement in the Construction phase.
- Avoid generic "be secure" statements; specify protocols, algorithms, or patterns where possible.

### Provider-Specific Terminology
- When referencing source code repository controls (A.8.4, A.8.25-A.8.27), use the CORRECT terminology for the project's repo provider. See `security` skill → "Source Code Repository Security (by Provider)" for the exact terms.
- **Common mistake**: Writing "branch protection" for AWS CodeCommit — the correct term is "Approval Rule Templates" + "IAM branch policies".

### Adaptive Depth Enforcement
- Do not over-engineer assessments for low-risk projects.
- Ensure comprehensive analysis for high-risk projects to prevent security debt.
