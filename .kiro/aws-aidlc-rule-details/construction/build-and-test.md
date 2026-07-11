# Build and Test

**Purpose**: Build all units and execute comprehensive testing strategy

## Prerequisites
- Code Generation must be complete for all units
- All code artifacts must be generated
- Project is ready for build and testing

---

## Step 1: Analyze Testing Requirements

Analyze the project to determine appropriate testing strategy:
- **Unit tests**: Already generated per unit during code generation
- **Integration tests**: Test interactions between units/services
- **Performance tests**: Load, stress, and scalability testing
- **End-to-end tests**: Complete user workflows
- **Contract tests**: API contract validation between services
- **Security tests**: Vulnerability scanning, penetration testing

---

## Step 2: Verify and Update QA Matrix

**See `common/traceability.md` for traceability chain definition.**

**Note**: The QA Matrix was generated BEFORE code implementation (in the QA Matrix Generation stage). This step VERIFIES completeness and UPDATES it with test execution results.

Load `aidlc-docs/inception/qa-matrix.md`:

- [ ] Verify all HU IDs have associated QA test cases (no orphans)
- [ ] Verify all API endpoints have associated QA test cases (no orphans)
- [ ] Verify layer classification is correct: API tests for endpoint validation, UI tests for page interactions, E2E for cross-page workflows
- [ ] Update QA Matrix Status column as tests execute (Pending → Pass/Fail) — per layer:
  - **API layer**: Update as unit/integration tests run
  - **UI layer**: Update as component/page tests run
  - **E2E layer**: Update as E2E flow steps execute
- [ ] Add any additional test cases discovered during implementation (assign layer and test data)
- [ ] Verify Test Data Catalog entries are sufficient for all test cases
- [ ] Generate coverage summary: total test cases by layer, passed, failed, pending

---

## Step 3: Generate Build Instructions

Create `aidlc-docs/construction/build-and-test/build-instructions.md`:

```markdown
# Build Instructions

## Prerequisites
- **Build Tool**: [Tool name and version]
- **Dependencies**: [List all required dependencies]
- **Environment Variables**: [List required env vars]
- **System Requirements**: [OS, memory, disk space]

## Build Steps

### 1. Install Dependencies
\`\`\`bash
[Command to install dependencies]
# Example: npm install, mvn dependency:resolve, pip install -r requirements.txt
\`\`\`

### 2. Configure Environment
\`\`\`bash
[Commands to set up environment]
# Example: export variables, configure credentials
\`\`\`

### 3. Build All Units
\`\`\`bash
[Command to build all units]
# Example: mvn clean install, npm run build, brazil-build
\`\`\`

### 4. Verify Build Success
- **Expected Output**: [Describe successful build output]
- **Build Artifacts**: [List generated artifacts and locations]
- **Common Warnings**: [Note any acceptable warnings]

## Troubleshooting

### Build Fails with Dependency Errors
- **Cause**: [Common causes]
- **Solution**: [Step-by-step fix]

### Build Fails with Compilation Errors
- **Cause**: [Common causes]
- **Solution**: [Step-by-step fix]
```

---

## Step 4: Generate Unit Test Execution Instructions

Create `aidlc-docs/construction/build-and-test/unit-test-instructions.md`:

```markdown
# Unit Test Execution

## Run Unit Tests

### 1. Execute All Unit Tests
\`\`\`bash
[Command to run all unit tests]
# Example: mvn test, npm test, pytest tests/unit
\`\`\`

### 2. Review Test Results
- **Expected**: [X] tests pass, 0 failures
- **Test Coverage**: [Expected coverage percentage]
- **Test Report Location**: [Path to test reports]

### 3. Fix Failing Tests
If tests fail:
1. Review test output in [location]
2. Identify failing test cases
3. Fix code issues
4. Rerun tests until all pass
```

---

## Step 5: Generate Integration Test Instructions

Create `aidlc-docs/construction/build-and-test/integration-test-instructions.md`:

```markdown
# Integration Test Instructions

## Purpose
Test interactions between units/services to ensure they work together correctly.

## Test Scenarios

### Scenario 1: [Unit A] → [Unit B] Integration
- **Description**: [What is being tested]
- **Setup**: [Required test environment setup]
- **Test Steps**: [Step-by-step test execution]
- **Expected Results**: [What should happen]
- **Cleanup**: [How to clean up after test]

### Scenario 2: [Unit B] → [Unit C] Integration
[Similar structure]

## Setup Integration Test Environment

### 1. Start Required Services
\`\`\`bash
[Commands to start services]
# Example: docker-compose up, start test database
\`\`\`

### 2. Configure Service Endpoints
\`\`\`bash
[Commands to configure endpoints]
# Example: export API_URL=http://localhost:8080
\`\`\`

## Run Integration Tests

### 1. Execute Integration Test Suite
\`\`\`bash
[Command to run integration tests]
# Example: mvn integration-test, npm run test:integration
\`\`\`

### 2. Verify Service Interactions
- **Test Scenarios**: [List key integration test scenarios]
- **Expected Results**: [Describe expected outcomes]
- **Logs Location**: [Where to check logs]

### 3. Cleanup
\`\`\`bash
[Commands to clean up test environment]
# Example: docker-compose down, stop test services
\`\`\`
```

---

## Step 6: Generate Performance Test Instructions (If Applicable)

Create `aidlc-docs/construction/build-and-test/performance-test-instructions.md`:

```markdown
# Performance Test Instructions

## Purpose
Validate system performance under load to ensure it meets requirements.

## Performance Requirements
- **Response Time**: < [X]ms for [Y]% of requests
- **Throughput**: [X] requests/second
- **Concurrent Users**: Support [X] concurrent users
- **Error Rate**: < [X]%

## Setup Performance Test Environment

### 1. Prepare Test Environment
\`\`\`bash
[Commands to set up performance testing]
# Example: scale services, configure load balancers
\`\`\`

### 2. Configure Test Parameters
- **Test Duration**: [X] minutes
- **Ramp-up Time**: [X] seconds
- **Virtual Users**: [X] users

## Run Performance Tests

### 1. Execute Load Tests
\`\`\`bash
[Command to run load tests]
# Example: jmeter -n -t test.jmx, k6 run script.js
\`\`\`

### 2. Execute Stress Tests
\`\`\`bash
[Command to run stress tests]
# Example: gradually increase load until failure
\`\`\`

### 3. Analyze Performance Results
- **Response Time**: [Actual vs Expected]
- **Throughput**: [Actual vs Expected]
- **Error Rate**: [Actual vs Expected]
- **Bottlenecks**: [Identified bottlenecks]
- **Results Location**: [Path to performance reports]

## Performance Optimization

If performance doesn't meet requirements:
1. Identify bottlenecks from test results
2. Optimize code/queries/configurations
3. Rerun tests to validate improvements
```

---

## Step 7: Generate Additional Test Instructions (As Needed)

Based on project requirements, generate additional test instruction files:

### Contract Tests (For Microservices)
Create `aidlc-docs/construction/build-and-test/contract-test-instructions.md`:
- API contract validation between services
- Consumer-driven contract testing
- Schema validation

### Security Tests
Create `aidlc-docs/construction/build-and-test/security-test-instructions.md`:
- Vulnerability scanning
- Dependency security checks
- Authentication/authorization testing
- Input validation testing

### Repo Completion Tracking (Multi-Repo Only)

**Execute IF**: Project architecture is Multi-Repo (from `aidlc-state.md`).

Before launching E2E tests, verify that ALL code repositories have completed their assigned HU implementations. Load the HU-Repo Distribution Map from `aidlc-docs/inception/plans/hu-repo-distribution.md`.

Create or update `aidlc-docs/construction/build-and-test/repo-completion-tracking.md`:

```markdown
# Repo Completion Tracking

## Status
| Repo ID | Name | Role | HUs Assigned | HUs Completed | Status |
|---------|------|------|-------------|---------------|--------|
| [ID] | [Name] | [Role] | HU-001, HU-003 | HU-001, HU-003 | ✅ Complete |
| [ID] | [Name] | [Role] | HU-001, HU-002 | HU-001 | ⏳ In Progress |

## Gate
- **All repos complete**: [Yes / No]
- **Blocking repos**: [List repos still in progress]
- **Ready for E2E**: [Yes / No]
```

**Rules**:
- [ ] Load repo list and HU assignments from HU-Repo Distribution Map
- [ ] For each repo, verify completion status (user confirms verbally or via checklist)
- [ ] DO NOT launch E2E tests until ALL repos show "Complete" status
- [ ] If a repo is blocking, present status to user and ask how to proceed (wait / skip / partial E2E)
- [ ] Log completion confirmations in `audit.md`

### End-to-End Tests
Create `aidlc-docs/construction/build-and-test/e2e-test-instructions.md`:

**Multi-Repo E2E Testing**: In multi-repo projects, E2E tests are orchestrated from the Documentation Hub repository after ALL code repositories have completed their HU implementations (verified by Repo Completion Tracking above).

**Source**: E2E User Flows are ALREADY DEFINED in the QA Matrix (Section 3: E2E User Flows). This step translates them into executable test scripts.

- [ ] Load E2E User Flows from `aidlc-docs/inception/qa-matrix.md` (Section 3)
- [ ] Load Test Data Catalog from `aidlc-docs/inception/qa-matrix.md` (Section 4)
- [ ] For each E2E flow, generate an executable test script:
  - Use flow steps as test actions (navigate, fill, click, verify)
  - Use Test Data Catalog entries for input values
  - Use preconditions to set up test state
  - Validate expected results at each step
  - Verify expected final state after flow completes
- [ ] Organize test scripts by priority (High flows run first)
- [ ] Document environment setup for cross-repo testing
- [ ] Define success criteria and exit conditions

**E2E Flow → Test Script Mapping**:
| E2E Flow ID | Flow Name | Test Script | QA Test Cases Covered | Repos Involved | Priority |
|-------------|-----------|-------------|----------------------|----------------|----------|
| E2E-001 | Complete user registration flow | e2e/registration-flow.spec.ts | QA-HU001-001, QA-HU001-005 | Gateway, Core API, Frontend Host | High |

**Execution Order**:
1. All code repos confirm HU completion
2. E2E environment is set up from Documentation Hub
3. Seed test data is loaded (entries marked "Seed" in Test Data Catalog)
4. E2E tests execute against deployed services following flow step order
5. Results are recorded in the QA Matrix (Status column per flow step)
6. Traceability report is generated showing coverage by layer (API/UI/E2E)

---

## Step 7b: Structure Validation (Core Library v1.5.5)

**After build and tests pass**, run structural validators as the final convention catch. Issues missed during Code Generation per-layer QA are caught here.

- [ ] Run `python config/validators/validate_repo_structure.py {project_root}` — validates project folder structure against `structure.md` conventions
- [ ] Run `python config/validators/validate_docker.py {project_root}` — validates Dockerfile\_local and docker-compose.yml completeness (if applicable)
- [ ] Run `python config/validators/runner.py --profile cross-cutting {project_root}` — validates auth patterns: HeaderToken (not Bearer), middleware ordering (if applicable)
- [ ] If ERRORS → fix → re-build (if structural fix affects build) → re-validate
- [ ] Log results in `aidlc-docs/audit.md`

**This is the final structural gate** — if it passes, the project's convention compliance is verified across all layers.

---

## Step 8: Generate Test Summary

Create `aidlc-docs/construction/build-and-test/build-and-test-summary.md`:

```markdown
# Build and Test Summary

## Build Status
- **Build Tool**: [Tool name]
- **Build Status**: [Success/Failed]
- **Build Artifacts**: [List artifacts]
- **Build Time**: [Duration]

## Test Execution Summary

### Unit Tests
- **Total Tests**: [X]
- **Passed**: [X]
- **Failed**: [X]
- **Coverage**: [X]%
- **Status**: [Pass/Fail]

### Integration Tests
- **Test Scenarios**: [X]
- **Passed**: [X]
- **Failed**: [X]
- **Status**: [Pass/Fail]

### Performance Tests
- **Response Time**: [Actual] (Target: [Expected])
- **Throughput**: [Actual] (Target: [Expected])
- **Error Rate**: [Actual] (Target: [Expected])
- **Status**: [Pass/Fail]

### Additional Tests
- **Contract Tests**: [Pass/Fail/N/A]
- **Security Tests**: [Pass/Fail/N/A]
- **E2E Tests**: [Pass/Fail/N/A]

## Overall Status
- **Build**: [Success/Failed]
- **All Tests**: [Pass/Fail]
- **Ready for Operations**: [Yes/No]

## Next Steps
[If all pass]: Ready to proceed to Operations phase for deployment planning
[If failures]: Address failing tests and rebuild
```

---

## Step 9: Update State Tracking

Update `aidlc-docs/aidlc-state.md`:
- Mark Build and Test stage as complete
- Update current status

---

## Step 10: Present Results to User

Present comprehensive message:

```
"🔨 Build and Test Complete!

**Build Status**: [Success/Failed]

**Test Results**:
✅ Unit Tests: [X] passed
✅ Integration Tests: [X] scenarios passed
✅ Performance Tests: [Status]
✅ Additional Tests: [Status]

**Generated Files**:
1. ✅ qa-matrix.md
2. ✅ build-instructions.md
3. ✅ unit-test-instructions.md
4. ✅ integration-test-instructions.md
5. ✅ performance-test-instructions.md (if applicable)
6. ✅ [additional test files as needed]
7. ✅ build-and-test-summary.md

Review the summary in aidlc-docs/construction/build-and-test/build-and-test-summary.md

**Ready to proceed to Operations stage for deployment planning?""
```

---

## Step 11: Log Interaction

**MANDATORY**: Log the phase completion in `aidlc-docs/audit.md`:

```markdown
## Build and Test Stage
**Timestamp**: [ISO timestamp]
**Build Status**: [Success/Failed]
**Test Status**: [Pass/Fail]
**Files Generated**:
- qa-matrix.md
- build-instructions.md
- unit-test-instructions.md
- integration-test-instructions.md
- performance-test-instructions.md
- build-and-test-summary.md

---
```

---

## Step 12: Skill Feedback Capture

**See `common/skill-feedback.md` for full feedback definitions (result types, severity levels, file format).**

IF `aidlc-state.md` → Organizational Skills section lists any consumed skills:
- [ ] For each build or test failure in this cycle:
  - Is the failing code derived from an organizational skill pattern? → Read skill version from YAML frontmatter (`metadata.version`), then record `correction` with the failure detail
  - Is the failure caused by a missing pattern the skill should define? → Record `gap` with the missing guidance description
- [ ] If all skill-derived patterns pass without issues → Record `ok` for each skill that **actively generated code** in this build (once per build cycle). Do NOT record `ok` for skills that were only loaded but did not produce code.
- [ ] Read skill version from YAML frontmatter (`metadata.version`) for each entry
- [ ] Assign severity per entry: `low` | `medium` | `high`
- [ ] Append entries to `aidlc-docs/skill-feedback.md` (create file with header template from `common/skill-feedback.md` if it does not exist). Include the Version column.

ELSE: Skip — no skills consumed, no feedback to capture.
