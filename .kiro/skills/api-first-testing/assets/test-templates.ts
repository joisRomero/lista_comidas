// @ts-nocheck
import { test, expect } from '@playwright/test';
import { EntityListPage, EntityFormPage, EntityDetailPage } from '../pages/EntityPage';

const BASE_URL = process.env.API_URL || 'http://localhost:{port}';
const entityIdKey = '{entityId}';
const fieldIdKey = '{fieldId}';

test.describe('{Entity} API', () => {
  test.describe('GET /api/v1/{resource}', () => {
    test('should list all', async ({ request }) => {
      const response = await request.get(`${BASE_URL}/api/v1/{resource}`);
      expect(response.ok()).toBeTruthy();
      const body = await response.json();
      expect(body.success).toBe(true);
      expect(body.data).toHaveProperty('items');
      expect(Array.isArray(body.data.items)).toBeTruthy();
      expect(body).toHaveProperty('pagination');
    });

    test('should filter by statusId', async ({ request }) => {
      const response = await request.get(`${BASE_URL}/api/v1/{resource}?statusId=100`);
      expect(response.ok()).toBeTruthy();
      const body = await response.json();
      body.data.items.forEach((item: { status: { masterTableId: number } }) => {
        expect(item.status.masterTableId).toBe(100);
      });
    });

    test('should paginate', async ({ request }) => {
      const response = await request.get(`${BASE_URL}/api/v1/{resource}?page=1&pageSize=5`);
      expect(response.ok()).toBeTruthy();
      const body = await response.json();
      expect(body.data.items.length).toBeLessThanOrEqual(5);
      expect(body.pagination.pageSize).toBe(5);
    });

    test('should search', async ({ request }) => {
      const response = await request.get(`${BASE_URL}/api/v1/{resource}?search=test`);
      expect(response.ok()).toBeTruthy();
    });
  });

  test.describe('GET /api/v1/{resource}/{id}', () => {
    test('should return detail for valid ID', async ({ request }) => {
      const listResponse = await request.get(`${BASE_URL}/api/v1/{resource}?pageSize=1`);
      const listBody = await listResponse.json();
      if (listBody.data.items.length === 0) return;

      const id = listBody.data.items[0][entityIdKey];
      const response = await request.get(`${BASE_URL}/api/v1/{resource}/${id}`);
      expect(response.ok()).toBeTruthy();
      const body = await response.json();
      expect(body.data.item[entityIdKey]).toBe(id);
    });

    test('should return 404 for non-existent', async ({ request }) => {
      const response = await request.get(`${BASE_URL}/api/v1/{resource}/999999`);
      expect(response.status()).toBe(404);
    });
  });

  test.describe('POST /api/v1/{resource}', () => {
    test('should create with valid data', async ({ request }) => {
      const response = await request.post(`${BASE_URL}/api/v1/{resource}`, {
        data: { name: `TEST-${Date.now()}`, [fieldIdKey]: 100 },
      });
      expect(response.status()).toBe(201);
      const body = await response.json();
      expect(body.data.item).toHaveProperty('{entityId}');
    });

    test('should return 400 for missing required fields', async ({ request }) => {
      const response = await request.post(`${BASE_URL}/api/v1/{resource}`, {
        data: {},
      });
      expect(response.status()).toBe(400);
      const body = await response.json();
      expect(body.success).toBe(false);
      expect(body.errors).toBeDefined();
    });
  });

  test.describe('PUT /api/v1/{resource}/{id}', () => {
    test('should update in valid state', async ({ request }) => {
      const createRes = await request.post(`${BASE_URL}/api/v1/{resource}`, {
        data: { name: `UPDATE-TEST-${Date.now()}`, [fieldIdKey]: 100 },
      });
      const createBody = await createRes.json();
      const id = createBody.data.item[entityIdKey];

      const response = await request.put(`${BASE_URL}/api/v1/{resource}/${id}`, {
        data: { name: `UPDATED-${Date.now()}` },
      });
      expect(response.ok()).toBeTruthy();
    });
  });

  test.describe('DELETE /api/v1/{resource}/{id}', () => {
    test('should delete in DRAFT state', async ({ request }) => {
      const createRes = await request.post(`${BASE_URL}/api/v1/{resource}`, {
        data: { name: `DELETE-TEST-${Date.now()}`, [fieldIdKey]: 100 },
      });
      const createBody = await createRes.json();
      const id = createBody.data.item[entityIdKey];

      const response = await request.delete(`${BASE_URL}/api/v1/{resource}/${id}`);
      expect(response.ok()).toBeTruthy();
      const body = await response.json();
      expect(body.data.result).toBe('SUCCESS');
    });
  });

  test.describe('POST /api/v1/{resource}/{id}/{verb}', () => {
    let entityId: number;

    test.beforeAll(async ({ request }) => {
      const createRes = await request.post(`${BASE_URL}/api/v1/{resource}`, {
        data: { name: `OP-TEST-${Date.now()}`, [fieldIdKey]: 100 },
      });
      const body = await createRes.json();
      entityId = body.data.item[entityIdKey];
    });

    test('should {verb} when in {REQUIRED_STATE}', async ({ request }) => {
      const response = await request.post(
        `${BASE_URL}/api/v1/{resource}/${entityId}/{verb}`,
        { data: {} }
      );
      expect(response.ok()).toBeTruthy();
      const body = await response.json();
      expect(body.data.item.status.name).toBe('{NEW_STATE}');
    });

    test('should fail when not in {REQUIRED_STATE}', async ({ request }) => {
      const response = await request.post(
        `${BASE_URL}/api/v1/{resource}/${entityId}/{verb}`,
        { data: {} }
      );
      expect(response.status()).toBe(400);
      const body = await response.json();
      expect(body.success).toBe(false);
    });
  });

  test.describe('POST /api/v1/{resource}/{id}/{subResource}/{subId}/remove', () => {
    test('should remove with justification', async ({ request }) => {
      const response = await request.post(
        `${BASE_URL}/api/v1/{resource}/{entityId}/{subResource}/{subEntityId}/remove`,
        { data: { justification: 'Test removal reason' } }
      );
      expect(response.ok()).toBeTruthy();
      const body = await response.json();
      expect(body.data.result).toBe('SUCCESS');
    });

    test('should fail without justification', async ({ request }) => {
      const response = await request.post(
        `${BASE_URL}/api/v1/{resource}/{entityId}/{subResource}/{subEntityId}/remove`,
        { data: {} }
      );
      expect(response.status()).toBe(400);
    });
  });

  test.describe('PUT /api/v1/{resource}/{id}/{subResource}/reorder', () => {
    test('should reorder successfully', async ({ request }) => {
      const response = await request.put(
        `${BASE_URL}/api/v1/{resource}/{entityId}/{subResource}/reorder`,
        { data: { itemIds: [3, 1, 2] } }
      );
      expect(response.ok()).toBeTruthy();
      const body = await response.json();
      expect(body.success).toBe(true);
    });
  });
});

test.describe('{Entity} E2E', () => {
  test('should display list with data', async ({ page }) => {
    const listPage = new EntityListPage(page);
    await listPage.goto();
    await listPage.waitForTable();
    expect(await listPage.getRowCount()).toBeGreaterThan(0);
  });

  test('should create new entity', async ({ page }) => {
    const listPage = new EntityListPage(page);
    const formPage = new EntityFormPage(page);

    await listPage.goto();
    await listPage.clickCreate();
    await formPage.fill({ name: `E2E-${Date.now()}` });
    await formPage.submit();

    await expect(page.locator('.ant-message-success')).toBeVisible();
  });

  test('should perform operation (state transition)', async ({ page }) => {
    const detailPage = new EntityDetailPage(page);
    await detailPage.goto(1);
    await detailPage.clickOperation('{verb}');
    await detailPage.confirmDialog();

    await expect(page.locator('.ant-message-success')).toBeVisible();
    await expect(detailPage.statusBadge).toHaveText('{NewStateName}');
  });

  test('should filter list by status', async ({ page }) => {
    const listPage = new EntityListPage(page);
    await listPage.goto();
    await listPage.filterByStatus(100);
    await listPage.waitForTable();
  });

  test('should search list', async ({ page }) => {
    const listPage = new EntityListPage(page);
    await listPage.goto();
    await listPage.search('test');
    await listPage.waitForTable();
  });
});
