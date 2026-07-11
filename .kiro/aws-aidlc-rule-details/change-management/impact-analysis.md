# Impact Analysis - Detailed Steps

## Purpose
**Assess change impact and determine appropriate implementation path**

Impact Analysis focuses on:
- Evaluating technical and business impact of requested changes
- Determining effort required for implementation
- Assessing risk level of the change
- Deciding appropriate workflow path (low/medium/high impact)

**Note**: This stage determines HOW to handle the change, based on the documented Change Request.

## Prerequisites
- Change Request must be complete
- Project context loaded from Re-Onboarding
- Technical resources available for assessment

---

## Step-by-Step Execution

### Step 1: Load Change Request Context
- [ ] Read Change Request document
- [ ] Review project snapshot for affected areas
- [ ] Load relevant ADRs that may be impacted
- [ ] Review current API contracts if applicable

### Step 2: Analyze Technical Impact

#### Code Impact Assessment
- [ ] Identify files/modules that require modification
- [ ] Estimate lines of code affected
- [ ] Identify new components required
- [ ] Assess complexity of changes

#### Architecture Impact Assessment
- [ ] Does change affect system boundaries?
- [ ] Does change require new components?
- [ ] Does change modify existing interfaces?
- [ ] Does change require new ADRs?

#### Data Impact Assessment
- [ ] Does change require database modifications?
- [ ] Is data migration required?
- [ ] Does change affect data flows?
- [ ] Are there data integrity considerations?

#### Integration Impact Assessment
- [ ] Are external integrations affected?
- [ ] Are API contracts changing?
- [ ] Are there upstream/downstream impacts?

### Security and Compliance Impact
- [ ] Does the change affect ISO 27001 controls identified in the original assessment?
- [ ] If yes, flag as HIGH impact and require security review during re-entry

### Multi-Repo Impact
- [ ] For multi-repo projects: does the change require HU Guide regeneration and re-distribution?
- [ ] Identify which repositories are affected by the change
- [ ] If HU Guides need updating, increase impact classification accordingly

### Step 3: Analyze Business Impact
- [ ] Which user personas are affected?
- [ ] Are existing workflows impacted?
- [ ] Is user retraining required?
- [ ] Are there SLA implications?

### Step 4: Estimate Effort
- [ ] Development effort (story points or hours)
- [ ] Testing effort
- [ ] Documentation effort
- [ ] Deployment effort
- [ ] Total estimated effort

### Step 5: Assess Risk Level
| Risk Factor | Assessment |
|-------------|------------|
| Technical complexity | Low / Medium / High |
| Integration risk | Low / Medium / High |
| Data risk | Low / Medium / High |
| Timeline risk | Low / Medium / High |
| **Overall Risk** | Low / Medium / High |

### Step 6: Classify Impact Level
Based on analysis, classify the change:

#### LOW Impact
- Single component change
- No architectural changes
- No API contract changes
- No database schema changes
- Minimal testing required
- **Path**: Direct to Code Generation

#### MEDIUM Impact
- Multiple components affected
- Minor architectural considerations
- Possible API changes (non-breaking)
- Minor database changes
- Standard testing required
- **Path**: Abbreviated INCEPTION + CONSTRUCTION

#### HIGH Impact
- System-wide changes
- Architectural changes required
- Breaking API changes
- Significant database changes
- Extensive testing required
- **Path**: Full INCEPTION + CONSTRUCTION cycle

### Step 7: Create Impact Analysis Document
- [ ] Create `aidlc-docs/change-management/CR-[NNN]-impact-analysis.md`:

```markdown
# Impact Analysis: CR-[NNN]

## Change Request Reference
- **CR Number**: CR-[NNN]
- **Title**: [Title]
- **Analysis Date**: [YYYY-MM-DD]
- **Analyst**: [Name/Role]

## Technical Impact Assessment

### Code Impact
| Area | Files Affected | Complexity | Notes |
|------|----------------|------------|-------|
| [area] | [count] | Low/Med/High | [notes] |

**Summary**: [X files affected, Y new files required]

### Architecture Impact
- [ ] System boundaries unchanged
- [ ] New components required: [Yes/No - list if yes]
- [ ] Interface changes: [Yes/No - describe if yes]
- [ ] New ADRs needed: [Yes/No - topics if yes]

### Data Impact
- [ ] Database changes required: [Yes/No]
- [ ] Migration complexity: [None/Low/Medium/High]
- [ ] Data integrity considerations: [describe]

### Integration Impact
- [ ] External systems affected: [list]
- [ ] API contract changes: [Yes/No - breaking/non-breaking]
- [ ] Upstream/downstream impacts: [describe]

## Business Impact Assessment
| Aspect | Impact | Notes |
|--------|--------|-------|
| User personas affected | [list] | |
| Workflow changes | [Yes/No] | [describe] |
| Training required | [Yes/No] | |
| SLA implications | [Yes/No] | |

## Effort Estimate
| Activity | Estimate | Confidence |
|----------|----------|------------|
| Development | [X days/points] | Low/Med/High |
| Testing | [X days/points] | Low/Med/High |
| Documentation | [X days/points] | Low/Med/High |
| Deployment | [X days/points] | Low/Med/High |
| **Total** | **[X days/points]** | |

## Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [risk] | Low/Med/High | Low/Med/High | [mitigation] |

**Overall Risk Level**: [LOW / MEDIUM / HIGH]

## Impact Classification

### Classification: [LOW / MEDIUM / HIGH]

### Justification
[Explain why this classification was chosen]

### Recommended Path

#### For LOW Impact:
- [ ] Skip INCEPTION stages
- [ ] Proceed directly to Code Generation
- [ ] Standard Code Review
- [ ] Update documentation

#### For MEDIUM Impact:
- [ ] Update affected requirements
- [ ] Create/modify user stories
- [ ] Skip full Application Design
- [ ] Full CONSTRUCTION cycle
- [ ] Update project snapshot

#### For HIGH Impact:
- [ ] Full Requirements Analysis
- [ ] User Stories update
- [ ] Application Design review/update
- [ ] API Contract updates (if applicable)
- [ ] New/updated ADRs
- [ ] Full CONSTRUCTION cycle
- [ ] New version release

## Affected Artifacts
| Artifact | Action Required |
|----------|-----------------|
| requirements.md | [Update/None] |
| stories.md | [Add/Update/None] |
| application-design.md | [Update/None] |
| API contracts | [Update/None] |
| ADRs | [New/Update/None] |

## Recommendation
[Clear recommendation on how to proceed with this change]

## Approval
- [ ] Impact analysis reviewed
- [ ] Classification agreed
- [ ] Path approved
- **Approved By**: _______________
- **Date**: _______________
```

### Step 8: Log Impact Analysis
- [ ] Log completion with timestamp in `aidlc-docs/audit.md`
- [ ] Include impact classification and recommended path
- [ ] Use ISO 8601 timestamp format

### Step 9: Present Completion Message

```markdown
# 📊 Impact Analysis Complete

**CR-[NNN]: [Title]**

[AI-generated summary of impact analysis in bullet points]

> **📋 IMPACT ANALYSIS:**  
> Please examine the analysis at: `aidlc-docs/change-management/CR-[NNN]-impact-analysis.md`
>
> **Assessment Summary:**
> - Impact Level: [LOW / MEDIUM / HIGH]
> - Effort Estimate: [X days/points]
> - Risk Level: [LOW / MEDIUM / HIGH]



> **🚀 RECOMMENDED PATH:**
>
> [Based on classification, one of:]
>
> 🟢 **LOW Impact** - Proceed directly to Code Generation
> 🟡 **MEDIUM Impact** - Abbreviated INCEPTION, then CONSTRUCTION
> 🔴 **HIGH Impact** - Full INCEPTION and CONSTRUCTION cycle

---
```

### Step 10: Wait for Approval
- [ ] Do not proceed until impact classification is approved
- [ ] If disagreement, revisit analysis
- [ ] Document final decision in audit.md

### Step 11: Route to Appropriate Path
Based on approved classification:
- **LOW**: Proceed to Code Generation
- **MEDIUM**: Proceed to Requirements Analysis (abbreviated)
- **HIGH**: Proceed to full Requirements Analysis

---

## Critical Rules

### Thorough Analysis
- Do not underestimate impact to speed things up
- Consider all affected areas
- Include realistic effort estimates

### Classification Criteria
- Classification must be justified
- When in doubt, classify higher
- Significant uncertainty = higher impact

### Approval Required
- Impact classification requires stakeholder approval
- Don't proceed without agreement on path
- Document any disagreements

## Quick Reference: Impact Paths

```
LOW IMPACT
    └──→ Code Generation → Code Review → Build & Test

MEDIUM IMPACT
    └──→ Requirements (update) → Stories (update) → Code Generation → ...

HIGH IMPACT
    └──→ Full INCEPTION cycle → Full CONSTRUCTION cycle
```
