# Traceability Reference

**Purpose**: Define the traceability chain used across the AI-DLC process to ensure every requirement is tested and every test is linked to a requirement.

## Traceability Chain

The AI-DLC process maintains a continuous chain of evidence from requirements to executable code:

```
HU (User Story) → API Contract → QA Test Cases (API/UI/E2E layers, with Repo tag in multi-repo) → E2E User Flows → Test Data → Executable Test Code
```

## Each Link Explained

- **HU → API Contract**: Each User Story maps to one or more API endpoints defined in API Contract Design. The HU Guide includes only the relevant API subset.
- **API Contract → QA Test Cases**: Each API endpoint generates QA test cases covering happy path, error paths, edge cases, and security validations. Each test case is classified into a test layer (API, UI, or E2E).
- **QA Test Cases → E2E User Flows**: Related test cases are grouped into complete user workflows (E2E flows) that span multiple endpoints and pages. Each E2E flow defines ordered steps with expected results.
- **E2E User Flows → Test Data**: Each test case and E2E flow references entries from the Test Data Catalog, ensuring reproducible and isolated test execution.
- **Test Data + Flows → Executable Test Code**: E2E flows with their test data are translated directly into executable test scripts (e.g., Playwright).

## Test Layers

Every QA test case belongs to exactly ONE layer:

| Layer | Scope | Tool Pattern |
|-------|-------|-------------|
| **API** | Single endpoint request/response | HTTP client (fetch, axios, supertest) |
| **UI** | Single page/component interaction | Browser automation (Playwright, Cypress) |
| **E2E** | Multi-step user workflow across pages | Browser automation (Playwright) |

**Rule**: Test at the lowest appropriate layer. API-only validations stay at API layer. Only cross-page user journeys warrant E2E.

## QA Matrix

The **QA Matrix** is the central traceability artifact saved to `aidlc-docs/inception/qa-matrix.md`. It serves as the single source of truth for testing status and coverage.

The QA Matrix contains 7 sections:

1. **Traceability Table** — Per-HU test cases with layer, type, preconditions, and test data references
2. **Security Test Cases** — ISO 27001-derived tests with control mapping
3. **E2E User Flows** — Complete user journeys with ordered steps mapped to QA test cases
4. **Test Data Catalog** — All test data entries with unique IDs, field values, and usage references
5. **Coverage Summary** — Metrics by layer, type, and orphan detection
6. **Distribution by HU** — Breakdown per HU by layer and type
7. **E2E Flow Index** — Quick reference of all flows with HU coverage and step counts

**Mapping Table Structure**:
| HU ID | API Endpoint | QA Test Case ID | Test Description | Layer | Type | Preconditions | Test Data | Priority | Status |
|-------|--------------|-----------------|------------------|-------|------|---------------|-----------|----------|--------|
| HU-001 | POST /api/resource | QA-HU001-001 | Create resource with valid data | API | Happy Path | Authenticated as admin | TD-001 | High | Pending |

- **Generation**: Generated BEFORE code implementation during the QA Matrix Generation stage.
- **Updates**: Build & Test stage UPDATES the Status column as tests execute (Pending → Pass/Fail).

## Traceability Rules

To maintain integrity, the following rules must be enforced:
- Every HU must have at least one QA test case.
- Every API endpoint must have at least one QA test case.
- Every HU involved in user-facing features must be covered by at least one E2E flow.
- Every E2E flow must have defined preconditions, test data, and expected final state.
- Every test data reference (TD-ID) in test cases must exist in the Test Data Catalog.
- **Orphan tests**: Any test not linked to an HU must be flagged for review.
- **Orphan requirements**: Any HU without associated tests must be flagged as a coverage gap.
- **Layer discipline**: Never duplicate a test across layers. Test at the lowest appropriate layer.

## Multi-Repo Traceability

In multi-repo projects, traceability spans across repository boundaries:
- **Repo Dimension**: Each test case in the QA Matrix Traceability Table is tagged with the **Repo ID** from the HU-Repo Distribution Map (`aidlc-docs/inception/plans/hu-repo-distribution.md`). This enables filtering test cases by repository and tracking per-repo coverage.
- **Documentation Hub**: The QA Matrix lives in the Documentation Hub repository to provide a centralized view.
- **HU Guides**: Include traceability links specific to each repository's implementation (HU ID → API endpoints → QA test case IDs).
- **E2E Flow Index**: Each E2E flow lists the **Repos Involved**, making it clear which repositories participate in each cross-cutting user journey.
- **E2E Orchestration**: E2E tests are executed from the Documentation Hub, testing integrated workflows across all code repositories.
- **Repo Completion Tracking**: Before launching E2E tests, Build & Test verifies all code repositories have completed their assigned HU implementations by cross-referencing the HU-Repo Distribution Map.
- **Test Data Distribution**: Seed data definitions from the Test Data Catalog are included in HU Guides for repository-level setup.
