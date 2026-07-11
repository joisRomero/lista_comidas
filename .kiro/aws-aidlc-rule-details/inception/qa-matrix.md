# QA Matrix Generation

**Purpose**: Generate the QA Matrix — the central traceability artifact that links User Stories to test cases BEFORE code implementation begins. The matrix must be comprehensive enough to serve as direct input for automated test generation (API tests, UI tests, E2E flows).

## Prerequisites
- API Contract Design must be complete (endpoints to test against)
- User Stories must be defined (HU IDs to link to)
- ISO 27001 Assessment must be complete (if applicable, for security test cases)
- Application Design must be available (for UI component identification, if applicable)

---

## Step 1: Load Traceability Context

- [ ] Load `common/traceability.md` for chain definition and rules
- [ ] Load API contracts from `aidlc-docs/inception/api-contracts/`
- [ ] Load User Stories from `aidlc-docs/inception/user-stories/`
- [ ] Load ISO 27001 assessment from `aidlc-docs/inception/iso-27001/` (if available)
- [ ] Load Application Design from `aidlc-docs/inception/application-design/` (if available, for UI test identification)
- [ ] **Multi-Repo only**: Load HU-Repo Distribution Map from `aidlc-docs/inception/plans/hu-repo-distribution.md` (if available). This provides the Repo ID per HU, used to tag each test case with its target repository.

---

## Step 2: Extract Traceability Inputs

- [ ] List all HU IDs with their associated API endpoints
- [ ] Identify all API endpoints from contracts
- [ ] Map each endpoint to its owning HU(s)
- [ ] Identify UI components/pages associated with each HU (from Application Design)
- [ ] Flag any orphan endpoints (not linked to any HU)
- [ ] Flag any orphan HUs (no API endpoints)

---

## Step 3: Classify Test Layers

Each test case must be assigned to exactly ONE test layer:

| Layer | Code | Scope | Tool Pattern | When to Use |
|-------|------|-------|-------------|-------------|
| **API** | `API` | Single endpoint request/response | HTTP client (fetch, axios, supertest) | Endpoint-level validation: status codes, response schemas, error handling |
| **UI** | `UI` | Single page/component interaction | Browser automation (Playwright, Cypress) | Component rendering, form validation, user interactions on ONE page |
| **E2E** | `E2E` | Multi-step user workflow across pages/endpoints | Browser automation (Playwright) | Complete user journeys that span multiple pages, involve navigation, and test integrated flows |

**Classification Rules**:
- If the test validates ONLY an API response → `API`
- If the test validates a UI component behavior on ONE page → `UI`
- If the test requires navigating between pages or involves a sequence of user actions across the application → `E2E`
- Security tests that validate HTTP responses → `API`
- Security tests that validate UI behavior (e.g., redirects, visible error messages) → `UI`

---

## Step 4: Generate QA Test Cases

For each API endpoint, generate test cases:
- **Happy path**: Valid input → expected output
- **Error/validation**: Invalid input → proper error handling
- **Edge cases**: Boundary values, empty inputs, large payloads
- **Security**: From ISO 27001 controls if applicable (auth, input sanitization, data exposure)

**Rules**:
- [ ] Assign unique IDs: format `QA-{HU-ID}-{SEQ}` (e.g., QA-HU001-001)
- [ ] Assign priority: High (happy path + security), Medium (error paths), Low (edge cases)
- [ ] Assign test layer: `API`, `UI`, or `E2E` per classification rules above
- [ ] Define preconditions for each test case
- [ ] Identify required test data for each test case

---

## Step 5: Define E2E User Flows

**Purpose**: Group related test cases into complete user workflows that span multiple endpoints and/or pages.

For each E2E flow:
- [ ] Define a unique flow ID: format `E2E-{SEQ}` (e.g., E2E-001)
- [ ] Describe the complete user journey
- [ ] List the ordered sequence of steps (each step = one user action)
- [ ] Map each step to the QA test cases it validates
- [ ] Identify which HUs are covered by the flow
- [ ] Define preconditions for the entire flow
- [ ] Define expected final state after the flow completes

**E2E Flow Identification Rules**:
- Group test cases that belong to the same user journey (e.g., register → login → use feature)
- Cross-HU flows are encouraged — they validate integration between stories
- Each flow must have a clear START state and END state
- Prioritize flows by business criticality

---

## Step 6: Build Test Data Catalog

**Purpose**: Define the test data needed to execute all test cases and E2E flows.

For each test data entry:
- [ ] Assign a unique data ID: format `TD-{SEQ}` (e.g., TD-001)
- [ ] Describe the data entity and its purpose
- [ ] Define field values (use realistic but synthetic data)
- [ ] Specify which test cases and E2E flows use this data
- [ ] Indicate if the data must exist BEFORE tests run (seed data) or is created DURING tests

---

## Step 7: Build QA Matrix Document

Create `aidlc-docs/inception/qa-matrix.md` with the following structure:

```markdown
# QA Matrix - [PROJECT_NAME]

## 1. Traceability Table

### [HU-ID]: [HU Title]

| HU ID | API Endpoint | QA Test Case ID | Test Description | Layer | Type | Repo | Preconditions | Test Data | Priority | Status |
|-------|-------------|-----------------|------------------|-------|------|------|---------------|-----------|----------|--------|
| HU-001 | POST /api/resource | QA-HU001-001 | Create resource with valid data | API | Happy Path | [Repo ID] | Authenticated as admin | TD-001 | High | Pending |
| HU-001 | POST /api/resource | QA-HU001-002 | Create resource missing required field → 400 | API | Error | [Repo ID] | Authenticated as admin | TD-002 | Medium | Pending |
| HU-001 | /page/resources | QA-HU001-010 | Resource form shows validation errors on submit | UI | Error | [Repo ID] | Logged in, on /page/resources | TD-002 | Medium | Pending |

> **Note**: The **Repo** column is populated from the HU-Repo Distribution Map (`aidlc-docs/inception/plans/hu-repo-distribution.md`). For single-repo projects, this column can be omitted or set to a single value.

[Repeat table per HU]

## 2. Security Test Cases (ISO 27001)

| QA Test Case ID | Description | ISO Control | Layer | Preconditions | Priority | Status |
|-----------------|-------------|-------------|-------|---------------|----------|--------|
| QA-SEC-001 | Access protected route without JWT → 401 | A.8.3 | API | No auth token | High | Pending |
| QA-SEC-002 | Admin action with student token → 403 | A.8.3 | API | Authenticated as student | High | Pending |
| QA-SEC-003 | SQL injection in search fields | A.8.28 | API | Authenticated | High | Pending |
| QA-SEC-004 | XSS in text input fields | A.8.28 | UI | Logged in, on form page | High | Pending |

## 3. E2E User Flows

### E2E-001: [Flow Name - e.g., "Complete User Registration and First Course Access"]

| Attribute | Value |
|-----------|-------|
| **Priority** | High |
| **HUs Covered** | HU-001, HU-002, HU-003 |
| **Preconditions** | Clean browser session, no existing user account |
| **Test Data** | TD-001, TD-005 |
| **Expected Final State** | User is logged in and can see enrolled course content |

**Steps**:

| Step | Action | Page/Endpoint | Expected Result | Validates QA |
|------|--------|---------------|-----------------|-------------|
| 1 | Navigate to registration page | /register | Registration form is displayed | - |
| 2 | Fill registration form with valid data | /register | Form accepts input | QA-HU001-001 |
| 3 | Submit registration | POST /auth/register | Success message, redirect to login | QA-HU001-001 |
| 4 | Fill login form with new credentials | /login | Form accepts input | QA-HU001-005 |
| 5 | Submit login | POST /auth/login | Redirect to dashboard | QA-HU001-005 |
| 6 | Navigate to course catalog | /courses | Course list is displayed | QA-HU003-001 |
| 7 | Click on a course | /courses/:id | Course detail with enrollment option | QA-HU003-005 |

[Repeat for each E2E flow]

## 4. Test Data Catalog

| Data ID | Entity | Purpose | Fields | Used By | Seed/Runtime |
|---------|--------|---------|--------|---------|-------------|
| TD-001 | Valid User | Registration happy path | name: "Test User", email: "test@example.com", password: "SecurePass123!" | QA-HU001-001, E2E-001 | Runtime |
| TD-002 | Invalid User | Missing required fields | name: "", email: "", password: "" | QA-HU001-003 | Runtime |
| TD-003 | Admin User | Admin operation tests | name: "Admin", email: "admin@test.com", role: "admin" | QA-ADM001-*, E2E-003 | Seed |

## 5. Coverage Summary

| Metric | Value |
|--------|-------|
| **Total HUs** | [X] |
| **Total API Endpoints** | [X] |
| **Total QA Test Cases** | [X] |
| **- API layer** | [X] |
| **- UI layer** | [X] |
| **- E2E flows** | [X] flows covering [Y] steps |
| **Orphan HUs (no tests)** | [list or "None"] |
| **Orphan Endpoints (no HU)** | [list or "None"] |
| **Test Data entries** | [X] |

## 6. Distribution by HU

| HU ID | Total | API | UI | E2E | Happy | Error | Edge | Security |
|-------|-------|-----|----|-----|-------|-------|------|----------|
| HU-001 | 12 | 8 | 2 | 2 | 5 | 4 | 1 | 2 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
| **TOTAL** | **X** | **X** | **X** | **X** | **X** | **X** | **X** | **X** |

## 7. E2E Flow Index

| E2E ID | Flow Name | HUs Covered | Repos Involved | Steps | Priority |
|--------|-----------|-------------|---------------|-------|----------|
| E2E-001 | Complete registration and first access | HU-001, HU-002, HU-003 | [Repo-A, Repo-B, Repo-C] | 7 | High |
| E2E-002 | Admin creates and publishes course | HU-ADM-001, HU-ADM-002 | [Repo-A, Repo-B] | 10 | High |
| ... | ... | ... | ... | ... | ... |

> **Note**: The **Repos Involved** column is derived from the HU-Repo Distribution Map. For single-repo projects, this column can be omitted.
```

---

## Step 8: Validate Completeness

- [ ] Every HU has at least one QA test case
- [ ] Every API endpoint has at least one QA test case
- [ ] No orphan tests (all linked to HU + endpoint)
- [ ] Security test cases cover all applicable ISO 27001 controls
- [ ] Every HU involved in user-facing features has at least one E2E flow
- [ ] Every E2E flow has defined preconditions, test data, and expected final state
- [ ] Test Data Catalog covers all referenced TD-IDs
- [ ] Layer classification is consistent (no API-only tests marked as E2E)

---

## Step 9: Update State Tracking

- [ ] Update `aidlc-docs/aidlc-state.md` to mark QA Matrix Generation complete

---

## Step 10: Present for Approval

- [ ] Log in `audit.md`
- [ ] Present completion message:

```markdown
# 📊 QA Matrix Generated

**Coverage**: [X] test cases across [Y] HUs and [Z] endpoints
**Layers**: [A] API tests, [B] UI tests, [C] E2E flows ([D] steps total)
**Test Data**: [E] data entries defined

> **📋 REVIEW REQUIRED:**
> Please examine the QA Matrix at: `aidlc-docs/inception/qa-matrix.md`
>
> Key sections to review:
> 1. **Traceability Table** — Are all HUs and endpoints covered?
> 2. **E2E User Flows** — Do the flows represent real user journeys?
> 3. **Test Data Catalog** — Is the test data realistic and sufficient?
> 4. **Security Tests** — Are ISO 27001 controls properly covered?

> **🚀 WHAT'S NEXT?**
>
> **You may:**
>
> - 🔧 **Request Changes** - Modify test cases, flows, or coverage
> - ✅ **Approve & Continue** - Proceed to **HU Guide Generation** (multi-repo) or **Per-Unit Loop** (single repo)
```

---

## Critical Rules

- **Timing**: QA Matrix is generated BEFORE code implementation — it defines WHAT to test.
- **Execution**: Build & Test stage UPDATES this matrix with execution results (Status column).
- **Multi-Repo**: In multi-repo projects, HU Guides pull QA test case IDs from this matrix.
- **Stability**: IDs must be globally unique and stable (don't reassign IDs if matrix is regenerated).
- **Traceability**: See `common/traceability.md` for the complete traceability chain definition.
- **Layer discipline**: Every test case has exactly ONE layer (API, UI, or E2E). Never duplicate a test across layers — test it at the lowest appropriate layer.
- **E2E minimalism**: E2E flows validate integrated journeys, not individual endpoints. If a test can be done at API layer, keep it there — E2E is for workflows.
- **Test data isolation**: Each E2E flow should be independent. Use unique test data to avoid interference between flows.
- **Playwright compatibility**: E2E flow steps must describe user-visible actions (click, fill, navigate, verify text) — not internal API calls. This ensures direct translation to Playwright scripts.
