# Project Snapshot - Detailed Steps

## Purpose
**Create comprehensive snapshot of project state for future reference and resumption**

Project Snapshot focuses on:
- Documenting final state of the project at closure
- Capturing all architectural decisions and their rationale
- Preserving context for future maintenance or enhancement
- Enabling efficient project resumption months or years later

**Note**: This is a consolidation stage that pulls together information from across the project lifecycle.

## Prerequisites
- All CONSTRUCTION stages must be complete
- Release Documentation must be complete
- Project is ready for closure or handoff

---

## Step-by-Step Execution

### Step 1: Gather Project Artifacts
- [ ] Collect all INCEPTION phase artifacts
- [ ] Collect all CONSTRUCTION phase artifacts
- [ ] Collect release documentation
- [ ] Review audit.md for key decisions

### Step 2: Create Project Snapshot Document
- [ ] Create `aidlc-docs/closure/project-snapshot.md`:

```markdown
# Project Snapshot

## Metadata
- **Project Name**: [Name]
- **Version**: [X.Y.Z]
- **Snapshot Date**: [YYYY-MM-DD]
- **Status**: [Completed | Maintenance | Active Development]

## Executive Summary
[2-3 paragraph summary of what was built, for whom, and why.
Include key business outcomes and technical achievements.]

## Scope Summary

### What Was Built
- [High-level capability 1]
- [High-level capability 2]
- [High-level capability 3]

### What Was NOT Built (Explicitly Out of Scope)
- [Item 1]
- [Item 2]

## Architecture Overview

### System Context
[Brief description of how this system fits in larger ecosystem]

### Component Summary
| Component | Purpose | Technology |
|-----------|---------|------------|
| [name] | [purpose] | [tech stack] |

### Architecture Diagram
[Reference to architecture diagram or embedded diagram]

## Technology Stack

### Runtime
| Layer | Technology | Version |
|-------|------------|---------|
| Language | [e.g., Java] | [17] |
| Framework | [e.g., Spring Boot] | [3.x] |
| Database | [e.g., PostgreSQL] | [15] |

### Development
| Tool | Purpose | Version |
|------|---------|---------|
| [tool] | [purpose] | [version] |

### Infrastructure
| Service | Purpose | Configuration |
|---------|---------|---------------|
| [service] | [purpose] | [key config] |

## Key Decisions Summary

### Architectural Decisions
| Decision | Choice | Rationale | ADR Reference |
|----------|--------|-----------|---------------|
| [topic] | [decision] | [why] | ADR-001 |

### Technology Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| [topic] | [decision] | [why] |

## API Summary
| API | Type | Purpose | Specification |
|-----|------|---------|---------------|
| [name] | REST/GraphQL | [purpose] | [link to spec] |

## Data Model Summary
[High-level description of main entities and their relationships]

## Integration Points
| System | Integration Type | Purpose | Status |
|--------|------------------|---------|--------|
| [system] | [type] | [purpose] | Active |

## User Stories Implemented
- Total stories: [N]
- Completed: [N]
- [Reference to stories.md]

## Known Issues and Technical Debt
| Issue | Impact | Recommendation |
|-------|--------|----------------|
| [issue] | [Low/Med/High] | [recommendation] |

## Performance Characteristics
| Metric | Expected | Achieved |
|--------|----------|----------|
| Response time | [target] | [actual] |
| Throughput | [target] | [actual] |

## Security Considerations
- Authentication: [method used]
- Authorization: [approach]
- Data protection: [measures]
- Compliance: [standards met]

## Operational Information
- Monitoring: [approach/tools]
- Logging: [approach/tools]
- Alerting: [approach/tools]

## Team and Contacts
| Role | Name | Contact |
|------|------|---------|
| Technical Lead | [name] | [contact] |
| Product Owner | [name] | [contact] |

## How to Resume This Project
1. Read this snapshot document completely
2. Review ADRs in `aidlc-docs/inception/adrs/`
3. Check for any changes to codebase since snapshot
4. If significant changes found, run Reverse Engineering
5. Proceed with Change Management process for new work

## Document References
| Document | Location | Purpose |
|----------|----------|---------|
| Requirements | aidlc-docs/inception/requirements/ | Original requirements |
| User Stories | aidlc-docs/inception/user-stories/ | Story details |
| API Contracts | aidlc-docs/inception/api-contracts/ | API specifications |
| ADRs | aidlc-docs/inception/adrs/ | Decision records |
| Release Docs | aidlc-docs/operations/release/ | Deployment info |

### Testing and QA Coverage
- [ ] Include QA Matrix (`aidlc-docs/inception/qa-matrix.md`) with final test execution status
- [ ] Document traceability chain completeness (HU → API → QA → E2E) per `common/traceability.md`
- [ ] Record E2E test results summary
- [ ] Flag any unresolved orphan requirements or orphan tests
```

### Step 3: Validate Snapshot Completeness
- [ ] All major sections are populated
- [ ] References point to existing documents
- [ ] No placeholder text remaining
- [ ] Technical accuracy verified

### Step 4: Log Snapshot Creation
- [ ] Log completion with timestamp in `aidlc-docs/audit.md`
- [ ] Include snapshot version and summary
- [ ] Use ISO 8601 timestamp format

### Step 5: Present Completion Message

```markdown
# 📸 Project Snapshot Complete

[AI-generated summary of project snapshot in bullet points]

> **📋 SNAPSHOT CREATED:**  
> Please examine the project snapshot at: `aidlc-docs/closure/project-snapshot.md`



> **🚀 WHAT'S NEXT?**
>
> - ✅ **Proceed to Version & Archive** - Continue closure process

---
```

### Step 6: Update Progress
- [ ] Mark Project Snapshot complete in `aidlc-docs/aidlc-state.md`
- [ ] Proceed to Version & Archive stage

---

## Critical Rules

### Completeness
- Snapshot must be self-contained
- Reader should understand project without other documents
- All references must be valid

### Future-Proof
- Write for someone unfamiliar with the project
- Explain WHY, not just WHAT
- Include context that may be forgotten

### Accuracy
- Verify all technical details
- Confirm versions and configurations
- Validate against actual codebase
