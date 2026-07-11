---
name: api-first-testing
description: >
  Generate E2E tests from OpenAPI spec using Playwright.
  Generates test cases, Page Objects, and assertions from endpoints.
  Trigger: When creating E2E tests from OpenAPI spec, generating Playwright tests.
metadata:
  author: anta
  version: "2.0"
  scope: [root]
  enforcement: mandatory
  auto_invoke: "api first testing, openapi tests, e2e from spec, playwright generate"
  phase: [inception, construction]
  layer: [e2e]
  validates_with: null
  validation_profile: null
---

## Workflow

```
OpenAPI Spec → Parse → Generate Scenarios → Page Objects → API Tests → E2E Tests
```

---

## Step 1: Generate Test Scenarios

From each endpoint:

| Endpoint Type | Test Case | Type |
|---------------|-----------|------|
| GET /entities (list) | List all | Happy path |
| GET /entities (list) | List with filter | Happy path |
| GET /entities (list) | List with search | Happy path |
| GET /entities (list) | List with pagination | Happy path |
| POST /entities (create) | Valid data | Happy path |
| POST /entities (create) | Missing required fields | Validation (400) |
| POST /entities (create) | Duplicate unique field | Business error (409) |
| GET /entities/{id} (get) | Valid ID | Happy path |
| GET /entities/{id} (get) | Non-existent ID | Not found (404) |
| PUT /entities/{id} (update) | Valid data | Happy path |
| PUT /entities/{id} (update) | Invalid state | Business error (400) |
| DELETE /entities/{id} (delete) | Valid ID in DRAFT | Happy path |
| DELETE /entities/{id} (delete) | Invalid state | Business error (400) |
| POST /entities/{id}/{verb} (operation) | Valid state transition | Happy path |
| POST /entities/{id}/{verb} (operation) | Wrong source state | Business error (400) |
| POST /entities/{id}/{verb} (operation) | Missing preconditions | Business error (400) |
| POST /sub/{subId}/remove (remove) | Valid with justification | Happy path |
| POST /sub/{subId}/remove (remove) | Missing justification | Validation (400) |
| PUT /sub/reorder (reorder) | Valid reorder | Happy path |

---

## Step 2: Page Objects

```typescript
export class EntityListPage {
  readonly page: Page;
  readonly table: Locator;
  readonly createButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.table = page.locator('[data-testid="entity-table"]');
    this.createButton = page.locator('[data-testid="create-entity-btn"]');
  }

  async goto() { await this.page.goto('/entities'); }
  async waitForTable() { await this.table.waitFor({ state: 'visible' }); }
  async clickCreate() { await this.createButton.click(); }
}
```

---

## Step 3: API Tests

```typescript
test('should list all', async ({ request }) => {
  const response = await request.get(`${BASE_URL}/api/v1/entities`);
  expect(response.ok()).toBeTruthy();
  const body = await response.json();
  expect(body.data).toHaveProperty('items');
});

test('should return 404 for non-existent', async ({ request }) => {
  const response = await request.get(`${BASE_URL}/api/v1/entities/999999`);
  expect(response.status()).toBe(404);
});
```

## Step 3b: Operation API Tests

State transition tests require setup (entity in correct state):

```typescript
test.describe('{Verb} {Entity}', () => {
  let entityId: number;

  test.beforeAll(async ({ request }) => {
    // Create entity in required state
    const createResponse = await request.post(`${BASE_URL}/api/v1/{resource}`, {
      data: { name: `TEST-${Date.now()}` },
    });
    const body = await createResponse.json();
    entityId = body.data.item.{entityId};
  });

  test('should {verb} when in {REQUIRED_STATE}', async ({ request }) => {
    const response = await request.post(
      `${BASE_URL}/api/v1/{resource}/${entityId}/{verb}`,
      { data: { {optionalField}: 'value' } }
    );

    expect(response.ok()).toBeTruthy();
    const body = await response.json();
    expect(body.data.item.status.name).toBe('{NEW_STATE}');
  });

  test('should fail when not in {REQUIRED_STATE}', async ({ request }) => {
    // Entity is now in {NEW_STATE}, not {REQUIRED_STATE}
    const response = await request.post(
      `${BASE_URL}/api/v1/{resource}/${entityId}/{verb}`
    );

    expect(response.status()).toBe(400);
    const body = await response.json();
    expect(body.errors[0].code).toBe('BUS_001');
  });
});
```

**Remove sub-entity test:**

```typescript
test('should remove with justification', async ({ request }) => {
  const response = await request.post(
    `${BASE_URL}/api/v1/{resource}/${entityId}/{subResource}/${subEntityId}/remove`,
    { data: { justification: 'Test removal reason' } }
  );

  expect(response.ok()).toBeTruthy();
  const body = await response.json();
  expect(body.data.result).toBe('SUCCESS');
});

test('should fail without justification', async ({ request }) => {
  const response = await request.post(
    `${BASE_URL}/api/v1/{resource}/${entityId}/{subResource}/${subEntityId}/remove`,
    { data: {} }
  );

  expect(response.status()).toBe(400);
});
```

---

## Step 4: E2E Tests

```typescript
test('should create new entity', async ({ page }) => {
  const listPage = new EntityListPage(page);
  const formPage = new EntityFormPage(page);
  
  await listPage.goto();
  await listPage.clickCreate();
  await formPage.fill({ name: `E2E-${Date.now()}` });
  await formPage.submit();
  
  await expect(page.locator('.ant-message-success')).toBeVisible();
});
```

---

## Test Data IDs

| Component | data-testid |
|-----------|-------------|
| List table | `{entity}-table` |
| Create button | `create-{entity}-btn` |
| Edit button | `edit-{entity}-btn` |
| Delete button | `delete-{entity}-btn` |
| Form inputs | `{field}-input` |
| Submit button | `submit-btn` |
| Operation button | `{verb}-{entity}-btn` |
| Justification input | `justification-input` |
| Confirm dialog | `confirm-dialog` |
| Confirm button | `confirm-btn` |
| Cancel button (dialog) | `cancel-dialog-btn` |

---

## File Structure

```
tests/
├── api/
│   └── {feature}.api.spec.ts
├── e2e/
│   └── {feature}.e2e.spec.ts
├── pages/
│   └── {Feature}Page.ts
└── fixtures/
    └── {feature}.fixtures.ts
```

---

## Checklist

- [ ] Page Object for related UI
- [ ] API test: happy path
- [ ] API test: error cases (400, 404)
- [ ] Operation test: valid state transition
- [ ] Operation test: wrong source state (should fail)
- [ ] Operation test: missing preconditions (should fail)
- [ ] Remove test: with justification (should pass)
- [ ] Remove test: without justification (should fail)
- [ ] Test setup creates entities in required state (beforeAll)
- [ ] E2E test: happy path flow
- [ ] E2E test: error handling
- [ ] `data-testid` added to components

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Page Object templates | [page-objects.ts](assets/page-objects.ts) |
| Test templates (API + E2E) | [test-templates.ts](assets/test-templates.ts) |

## Related Skills

| Task | Skill |
|------|-------|
| Playwright patterns | `playwright` |
| Component selectors | `design-system` |
