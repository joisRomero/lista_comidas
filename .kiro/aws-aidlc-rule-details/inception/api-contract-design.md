# API Contract Design - Detailed Steps

## Purpose
**Define API contracts before implementation (API-First approach)**

API Contract Design focuses on:
- Designing API specifications before writing implementation code
- Enabling parallel development between API consumers and providers
- Establishing clear contracts for integration points
- Validating API design with stakeholders before development

**Note**: This stage produces API specifications (OpenAPI, AsyncAPI, GraphQL schemas). Implementation happens in Code Generation.

## Prerequisites
- Requirements Analysis must be complete
- Application Design recommended (provides component context)
- API requirements identified in user stories or requirements

## MANDATORY: Skill Resolver — Pre-Load Skills

**BEFORE starting this stage**, the Skill Resolver loads these skills to ensure the openapi.yaml follows ANTA patterns:

| Skill | What It Provides |
|-------|-----------------|
| `api-first-spec` | Response shapes (`data.items[]`/`data.item{}`/`data.result{}`), endpoint type patterns, document structure |
| `database-modeling` | ERD, entity relationships → feeds schemas and data types |
| `database-security` | Error code catalog (`VAL_xxx`, `BUS_xxx`) → feeds error response schemas |
| `database-audit` | Audit columns (RecordStatus, timestamps) that appear in response schemas |
| `dotnet-api` | Response wrapper `ApiResponse<T>`, pagination params, `HeaderToken` auth pattern |

**Also load outputs from previous stages**:
- Requirements Analysis → entities, schema, relationships, business rules
- User Stories → operations (submit, approve, reject), acceptance criteria, state flows
- ISO 27001 Assessment → authentication and data protection requirements

## Intelligent Assessment Guidelines

**WHEN TO EXECUTE API CONTRACT DESIGN**: Use this assessment before proceeding:

### Execute IF:
- New REST, GraphQL, or gRPC APIs being created
- Existing API modifications or versioning required
- Integration with external systems or third parties
- Multiple teams will consume or implement the API
- Event-driven architecture with message contracts needed
- Public or partner-facing APIs

### Skip IF:
- No API endpoints in scope
- Internal-only code with no service boundaries
- Simple CRUD with auto-generated APIs (still document, but lighter touch)

---

## Step-by-Step Execution

### Step 1: Analyze API Context
- [ ] Read requirements and user stories for API-related functionality
- [ ] Identify all API endpoints, events, or service boundaries
- [ ] Determine API consumers (frontend, mobile, external, internal services)
- [ ] Review existing APIs if brownfield (for consistency)

### Step 2: Create API Design Plan
- [ ] Generate plan with checkboxes for API contract design
- [ ] Each API or service boundary should have explicit design steps
- [ ] Include review and validation checkpoints
- [ ] Save plan as `aidlc-docs/inception/plans/api-contract-plan.md`

### Step 3: Generate Context-Appropriate Questions
**DIRECTIVE**: Focus on API design decisions that affect the contract.

- EMBED questions using [Answer]: tag format
- Focus on consumer needs, versioning, and standards

**Question categories** (as applicable):
- **API Style** - REST, GraphQL, gRPC, or hybrid?
- **Versioning Strategy** - URL path, header, or query parameter versioning?
- **Authentication** - API keys, OAuth, JWT, or other?
- **Data Formats** - JSON, XML, Protocol Buffers?
- **Pagination** - Offset, cursor, or keyset pagination?
- **Error Handling** - Error response format and codes?
- **Rate Limiting** - Limits and quota policies?

### Step 4: Request User Input
- [ ] Ask user to fill [Answer]: tags in the API plan
- [ ] Clarify consumer requirements and constraints
- [ ] Confirm API standards and conventions

### Step 5: Collect and Analyze Answers
- [ ] Wait for user to provide answers using [Answer]: tags
- [ ] Analyze for ambiguities or conflicting requirements
- [ ] Create follow-up questions if needed

### Step 5b: FR→Endpoint Mapping (MANDATORY before generating spec)

**BEFORE writing any openapi.yaml**, create an explicit mapping table from requirements to endpoints. This prevents functionality loss during spec generation.

- [ ] Open `requirements.md` and list EVERY functional requirement (FR-xx)
- [ ] For each FR, determine the HTTP method + path
- [ ] **Workflow Detection**: If ANY FR defines state transitions (e.g., DRAFT→SUBMITTED→APPROVED):
  - [ ] List ALL transition endpoints — one per arrow in the state diagram. Common miss: **return/revert** transitions
  - [ ] Add history/audit entity endpoint (GET detail should include transition history)
  - [ ] Add `WorkflowActionRequest` schema with optional `comments` field for approve/reject
- [ ] **Catalog Detection**: If ANY FR references catalog/lookup data (departments, positions, categories):
  - [ ] Add GET list endpoint per catalog (for dropdowns)
  - [ ] Add filter param if catalogs are hierarchical (e.g., positions filtered by department)
- [ ] Present the mapping table to validate coverage before generating:

```markdown
| FR | Action | Method | Path | Notes |
|----|--------|--------|------|-------|
| FR-xx | List | GET | / | Pagination + filters |
| FR-xx | Create | POST | / | Initial state |
| FR-xx | Update | PUT | /{id} | State restrictions |
| FR-xx | Delete | DELETE | /{id} | Soft delete |
| FR-xx | Detail | GET | /{id} | + related entities |
| FR-xx | [Transition 1] | POST | /{id}/[verb] | STATE_A → STATE_B |
| FR-xx | [Transition 2] | POST | /{id}/[verb] | STATE_B → STATE_C |
| FR-xx | [Transition N] | POST | /{id}/[verb] | STATE_X → STATE_A ← REVERT EASY TO MISS |
| Catalog | [Catalog name] | GET | /[catalog] | For dropdown |
| Catalog | [Child catalog] | GET | /[catalog]?[ParentId] | Filtered by parent |
```

**Every row in this table MUST have a corresponding path in the generated openapi.yaml. No exceptions.**

### Step 6: Generate API Contracts
- [ ] Create `aidlc-docs/inception/api-contracts/` directory
- [ ] For REST APIs: Generate OpenAPI 3.x specification (`openapi.yaml`)
- [ ] For async/events: Generate AsyncAPI specification (`asyncapi.yaml`)
- [ ] For GraphQL: Generate schema definition (`schema.graphql`)

**MANDATORY — ANTA Patterns in openapi.yaml** (loaded from pre-loaded skills):

The openapi.yaml MUST include these ANTA-standard components. A generic spec will cause incorrect code in Backend and Frontend parallel layers.

#### Content Requirements
- [ ] **API versioning**: OpenAPI `servers` section MUST include versioned base path `/api/v1/{module}`. `info.version` set.
- [ ] **Response wrapper**: `ApiResponse` schema with `success`, `data`, `errors`, `metadata`
- [ ] **Error schema**: `ErrorItem` with `code` (VAL_xxx, BUS_xxx), `field`, `message`
- [ ] **ErrorResponse separate**: Error responses (4xx, 5xx) use dedicated `ErrorResponse` schema, NOT the success schema
- [ ] **Pagination**: `PaginationResult` schema + 5 standard query params (Page, PageSize, Search, SortBy, SortOrder) on every GET list endpoint
- [ ] **StatusItem schema**: `masterTableId`, `name`, `value` — for state flow entities
- [ ] **Auth**: Two apiKey security schemes named `code` and `header` (matches `AddSwaggerWithHappyAuth` from ANTA.Shared.Common.Api). NEVER BearerAuth, NEVER single `HappyAuth` scheme
- [ ] **Response shapes per endpoint type** (from `api-first-spec`):
  - GET list → `data.items[]` + `pagination`
  - GET single → `data.item{}`
  - POST create → `data.item{}` (201)
  - PUT update → `data.item{}`
  - DELETE → `data.result{}`
  - POST operation → `data.item{}` or `data.result{}`
  - POST remove → `data.result{}` with justification body
- [ ] **Operations with state flow**: Each `POST /{id}/{verb}` endpoint MUST document state precondition and resulting state in description (e.g., "State: DRAFT → SUBMITTED")
- [ ] **Request/response examples**: At least one example per endpoint
- [ ] **Complete schemas**: Every schema MUST have properties with types — no `type: object` without properties
- [ ] **Separate List vs Detail schemas**: List endpoints return lightweight `{Entity}ListItem` (table columns only). Detail endpoints return full `{Entity}Detail` (all fields + nested entities like workflow history)

#### Structure Conventions (DRY spec)
- [ ] **Use `$ref` for reusable components**: Common parameters (Page, PageSize, Search, SortBy, SortOrder, {entity}Id path param) → `components/parameters/`. Common responses (400, 404, 500) → `components/responses/`. Shared schemas → `components/schemas/`
- [ ] **Use `allOf` to reduce schema duplication**: When `CreateRequest` and `UpdateRequest` share most properties, extract a `{Entity}Base` schema and compose with `allOf`. Example: `UpdateRequest: allOf: [$ref: '#/.../EntityBase', properties: {id: ...}]`
- [ ] **Use `tags`**: Group endpoints by domain (`Employees`, `Workflow`, `Catalogs`). Every endpoint MUST have at least one tag
- [ ] **403 Forbidden**: Include on endpoints that require specific roles (e.g., approve/reject require Approver role)
- [ ] **DO NOT inline response schemas**: Define once in `components/schemas/`, reference everywhere via `$ref`

#### NFR Annotations (recommended)
- [ ] **Performance NFRs in spec**: If NFRs define latency or throughput targets, annotate endpoints with extension properties:
  ```yaml
  /:
    get:
      x-nfr-latency-ms: 500      # NFR-2.1: list must respond < 500ms
      x-nfr-throughput-rps: 100   # Expected peak requests per second
  /export:
    get:
      x-nfr-latency-ms: 5000     # NFR-2.3: export < 5s
  ```
  These are informational — they don't affect code generation but document expectations for load testing.

#### Idempotency for Workflow Operations (recommended)
- [ ] **Idempotency-Key header**: State transition endpoints (`POST /{id}/start`, `POST /{id}/cancel`, `POST /{id}/close`) SHOULD document an `Idempotency-Key` request header for safe retries:
  ```yaml
  parameters:
    - name: Idempotency-Key
      in: header
      required: false
      schema:
        type: string
        format: uuid
      description: Client-generated UUID for safe retry. Server returns same response if key was already processed.
  ```
  This prevents duplicate state transitions when the frontend retries after network errors.

### Step 6b: Generate Authorization Matrix (Lion)

**MANDATORY for ANTA projects.** After generating the openapi.yaml, derive the authorization matrix that maps screens, endpoints, actions, and roles. This matrix feeds Lion registration and frontend/backend permission code during Construction.

**Inputs required**:
- `aidlc-docs/inception/api-contracts/openapi.yaml` — all endpoints
- `aidlc-docs/inception/user-stories/stories.md` — personas/roles
- `aidlc-docs/inception/requirements/requirements.md` — business rules, access constraints

**Load skill**: `lion` (provides matrix format, 3-level access control model, naming conventions)

#### 6b.1: Identify Screens from Endpoints

- [ ] Group API endpoints by UI screen/page
- [ ] Define screen hierarchy: root → visible modules → hidden sub-screens (create, edit, view)
- [ ] Each frontend route = one Option in Lion
- [ ] Parent screens (list/index) → `is_visible: true`
- [ ] Sub-screens (create, edit, view, approve) → `is_visible: false`

#### 6b.2: Define Profiles from Personas

- [ ] Map each persona/actor from user stories to a Lion profile
- [ ] Define profile code pattern: `{app_code}-{PROFILE_CODE}` (e.g., `200-146-ADMIN`)
- [ ] Determine which screens each profile can access (Level 1)

#### 6b.3: Determine Access Control Level

- [ ] **Level 1 only** (Profile → Screen): If all users with screen access can do everything on that screen
- [ ] **Level 1 + 2** (Profile → Screen + Action): If roles differ in what they can DO on the same screen (e.g., ADMIN can delete, USER cannot)
- [ ] **Level 1 + 2 + 3** (+ Service → Process): If backend must enforce action-level endpoint blocking
- [ ] Document the chosen level in the matrix header

#### 6b.4: Map Endpoints to Screens as Services

- [ ] For each screen, list which openapi.yaml endpoints it calls
- [ ] GET list → parent/list screen
- [ ] POST create → "create" sub-screen
- [ ] GET by ID → "view" sub-screen
- [ ] PUT/PATCH update → "edit" sub-screen
- [ ] Shared endpoints (catalogs, employees, files) → registered on EACH screen that uses them
- [ ] Use MasterTable method codes: GET=17001, POST=17002, PUT=17003, DELETE=17004, PATCH=17005

#### 6b.5: Define Processes (if Level 2+)

- [ ] For mutating operations, define action processes per screen
- [ ] Standard names: `btnNew` (POST), `btnEdit` (PUT/PATCH), `btnDelete` (DELETE), `btnExportExcel` (export)
- [ ] Workflow names: `btnApprove`, `btnReject`, `btnSubmit`
- [ ] Map each process to profiles that can execute it

#### 6b.6: Generate Matrix Document

- [ ] Save as `aidlc-docs/inception/authorization-matrix.md`
- [ ] Include 4 tables: **Profiles**, **Options (Screens)**, **Services (Endpoints per Screen)**, **Processes (Actions per Screen)**
- [ ] See `lion` skill → "Matrix Format" for exact table structure

#### 6b.7: Validate Matrix Completeness

- [ ] Every endpoint in openapi.yaml appears in at least one screen's services
- [ ] Every screen assigned to at least one profile
- [ ] If processes defined, each assigned to at least one profile
- [ ] Cross-reference with FR→Endpoint mapping (Step 5b) — no orphaned endpoints

#### 6b.8: Lion MCP Registration (OPTIONAL)

If the Lion MCP server is available, register the matrix:

- [ ] Check MCP availability (Lion runs on `http://localhost:8080/mcp`)
- [ ] If available → follow registration order from `lion` skill (application → options → processes → services → profiles → assignments)
- [ ] If NOT available → the matrix document is the deliverable. Registration can happen later
- [ ] Max 2 parallel MCP calls (SQL Server concurrency limit)

### Step 7: Create API Summary Document
- [ ] Create `aidlc-docs/inception/api-contracts/api-summary.md` with:
  - API overview and purpose
  - Authentication requirements
  - Base URLs and environments
  - Versioning approach
  - Quick reference of endpoints/operations
  - Links to full specifications

### Step 7b: Skill Compliance Gate (MANDATORY)

**BEFORE running the Spec Validation Gate**, verify the openapi.yaml uses EXACT identifiers from loaded mandatory skills. See `common/skill-resolver.md` → Skill Compliance Gate for the full protocol.

Quick checks for API Contract:
- [ ] **API versioning**: paths use `/api/v1/{module}` prefix (e.g., `/api/v1/employees`) — from `dotnet-api` compact rules
- [ ] Audit columns in schemas use `RecordCreationUser`, `RecordCreationDate`, `RecordEditUser`, `RecordEditDate`, `RecordStatus` (NOT generic synonyms)
- [ ] RecordStatus is `string` with enum `['A', 'I', '*']` (NOT integer, NOT 0/1)
- [ ] Error codes follow `VAL_xxx` / `BUS_xxx` pattern from `database-security` skill
- [ ] Response wrapper is `ApiResponse` with `success`/`data`/`errors` (NOT custom names)
- [ ] Security scheme is `HappyAuth` apiKey (NOT BearerAuth) — from `happy` skill
- [ ] Pagination params are `Page`, `PageSize`, `Search`, `SortBy`, `SortOrder` (exact names from `dotnet-api` skill)

**If ANY identifier is paraphrased or renamed**: Correct the spec BEFORE proceeding to the Spec Validation Gate.

### Step 8: Validate Contracts (Spec Validation Gate)

**MANDATORY**: The openapi.yaml must pass ALL checks before this stage is complete. This spec feeds Backend and Frontend layers in parallel during Construction — an incomplete spec produces mismatched code.

#### Deterministic Spec Validation (Core Library v1.5.5)

**Run BEFORE the manual checklist below** — this catches naming, schema, response shape, auth, and pagination issues deterministically:

- [ ] Run `python config/validators/validate_openapi.py aidlc-docs/inception/api-contracts/openapi.yaml`
- [ ] If ERRORS → fix the spec → re-run the validator → repeat until clean
- [ ] If only WARNINGS → review each with user, proceed if acceptable
- [ ] Log validator output (errors/warnings count) in `aidlc-docs/audit.md`
- [ ] **GATE**: Do NOT proceed to the manual checks below with validator errors outstanding

The validator covers rules `API_RESPONSE_SHAPE`, `PAGINATION_PARAMS`, `ERROR_SCHEMA`, `HEADER_TOKEN_AUTH`, `SCHEMAS_COMPLETE`, `EXAMPLES_PRESENT`, `STATE_OPERATIONS` deterministically. The manual checks below remain as a semantic safety net for coverage, consistency, and cross-reference verification.

#### Core Schema Checks
- [ ] **API versioning** — `servers` section defines base URL with `/api/v1/{module}` path. All endpoint paths are relative to this versioned prefix. `info.version` is set.
- [ ] **Schemas complete** — All properties defined with type + example. No `type: object` without properties
- [ ] **Response shapes** — All responses use `ApiResponse` pattern with `success`/`data`/`errors`
- [ ] **Pagination** — GET list endpoints have Page/PageSize/Search/SortBy/SortOrder query params
- [ ] **Operations** — Each `POST /{id}/{verb}` documents state flow in description
- [ ] **Examples** — At least one request/response example per endpoint
- [ ] **Consistency** — Check for consistency across related APIs
- [ ] **Coverage (FR→Endpoint cross-reference)** — Open `requirements.md` and list EVERY functional requirement that implies an API operation (CRUD actions, state transitions, catalog lookups). For EACH, verify a matching path+method exists in the openapi.yaml. If ANY FR has no endpoint, the spec is INCOMPLETE. Common misses: state transition endpoints (submit, approve, reject, **return/revert**), catalog listing endpoints, bulk operations
- [ ] **Syntactically valid** — OpenAPI 3.x compliant

#### Error Response Checks
- [ ] **ErrorResponse schema separate from SuccessResponse** — Error responses (4xx, 5xx) MUST use a dedicated `ErrorResponse` schema (with `success: false`, `errors: ErrorItem[]`), NOT the same `ApiResponse<T>` used for success. Do NOT include `pagination` or `data.items[]` in error schemas
- [ ] **ErrorItem schema complete** — Must have `code` (string, VAL_xxx/BUS_xxx pattern), `field` (string, nullable), `message` (string)
- [ ] **500 response on ALL endpoints** — Every endpoint MUST define a `500` response with `ErrorResponse` schema. This is the universal server error contract

#### Auth Checks (Happy Integration — must match `AddSwaggerWithHappyAuth`)
- [ ] **Security schemes** — TWO apiKey schemes defined with literal names `code` and `header` (type: apiKey, in: header). This matches the `AddSwaggerWithHappyAuth()` NuGet extension.
- [ ] **Both required** — `security` array lists both `code: []` and `header: []` together (AND-logic)
- [ ] **No wrong names** — MUST NOT use `HappyAuth` (single scheme), `HappyAuthCode`, `BearerAuth`, `Bearer`, or any custom name. The Swagger UI must show exactly two input fields: `code` and `header`.

#### Endpoint Convention Checks
- [ ] **POST create at root** — Create endpoints use `POST /` (root of the resource), NOT `POST /create`. Follow REST conventions: `POST /employees` creates an employee, not `POST /employees/create`
- [ ] **State operations as verbs** — State change endpoints use `POST /{id}/{verb}` pattern (e.g., `POST /{id}/submit`, `POST /{id}/approve`)

**If any check fails**: Correct the spec and re-validate. Do NOT approve with an incomplete spec.

### Step 9: Log Approval Prompt
- [ ] Log approval prompt with timestamp in `aidlc-docs/audit.md`
- [ ] Include reference to API contracts
- [ ] Use ISO 8601 timestamp format

### Step 10: Present Completion Message

```markdown
# 📡 API Contract Design Complete

[AI-generated summary of API contracts created in bullet points]

> **📋 REVIEW REQUIRED:**  
> Please examine the API contracts at: `aidlc-docs/inception/api-contracts/`



> **🚀 WHAT'S NEXT?**
>
> **You may:**
>
> - 🔧 **Request Changes** - Ask for modifications to API contracts
> 👥 **Share with Consumers** - Distribute contracts for parallel development
> - ✅ **Approve & Continue** - Approve contracts and proceed to **[Workflow Planning/Definition of Ready]**

---
```

### Step 11: Wait for Explicit Approval
- [ ] Do not proceed until user explicitly approves API contracts
- [ ] If changes requested, update contracts and repeat approval
- [ ] Document approval in audit.md

### Step 12: Update Progress
- [ ] Mark API Contract Design stage complete in `aidlc-docs/aidlc-state.md`
- [ ] Update the "Current Status" section
- [ ] Prepare contracts for use in Code Generation

---

## Critical Rules

### Contract-First Principle
- Specification must exist before implementation code
- Changes to API must update specification first
- Implementation must match specification exactly

### Specification Standards
- Use OpenAPI 3.0+ for REST APIs
- Use AsyncAPI 2.0+ for event-driven APIs
- Use SDL for GraphQL schemas
- Include examples for all operations

### Versioning Requirements
- Document versioning strategy in api-summary.md
- Breaking changes require version increment
- Maintain backward compatibility when possible

### Consumer Collaboration
- Share contracts early for parallel development
- Collect feedback from API consumers
- Document consumer-specific requirements
