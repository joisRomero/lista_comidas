// @ts-nocheck
import { Page, Locator } from '@playwright/test';

export class EntityListPage {
  readonly page: Page;
  readonly table: Locator;
  readonly createButton: Locator;
  readonly searchInput: Locator;
  readonly statusFilter: Locator;
  readonly pagination: Locator;

  constructor(page: Page) {
    this.page = page;
    this.table = page.locator('[data-testid="{entity}-table"]');
    this.createButton = page.locator('[data-testid="create-{entity}-btn"]');
    this.searchInput = page.locator('[data-testid="search-input"]');
    this.statusFilter = page.locator('[data-testid="status-filter"]');
    this.pagination = page.locator('.ant-pagination');
  }

  async goto() {
    await this.page.goto('/{resource}');
  }

  async waitForTable() {
    await this.table.waitFor({ state: 'visible' });
  }

  async getRowCount() {
    return await this.table.locator('tbody tr').count();
  }

  async filterByStatus(statusId: number) {
    await this.statusFilter.click();
    await this.page.locator(`[data-value="${statusId}"]`).click();
  }

  async search(text: string) {
    await this.searchInput.fill(text);
    await this.searchInput.press('Enter');
  }

  async clickCreate() {
    await this.createButton.click();
  }

  async clickRow(index: number) {
    await this.table.locator(`tbody tr:nth-child(${index + 1})`).click();
  }
}

export class EntityFormPage {
  readonly page: Page;
  readonly nameInput: Locator;
  readonly submitButton: Locator;
  readonly cancelButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.nameInput = page.locator('[data-testid="name-input"]');
    this.submitButton = page.locator('[data-testid="submit-btn"]');
    this.cancelButton = page.locator('[data-testid="cancel-btn"]');
  }

  async fill(data: { name: string; [key: string]: string | number }) {
    await this.nameInput.fill(data.name);
    for (const [key, value] of Object.entries(data)) {
      if (key === 'name') continue;
      const input = this.page.locator(`[data-testid="${key}-input"]`);
      if (await input.isVisible()) {
        await input.fill(String(value));
      }
    }
  }

  async submit() {
    await this.submitButton.click();
  }

  async cancel() {
    await this.cancelButton.click();
  }
}

export class EntityDetailPage {
  readonly page: Page;
  readonly statusBadge: Locator;
  readonly editButton: Locator;
  readonly deleteButton: Locator;
  readonly confirmDialogModal: Locator;
  readonly confirmButton: Locator;
  readonly cancelDialogButton: Locator;
  readonly justificationInput: Locator;

  constructor(page: Page) {
    this.page = page;
    this.statusBadge = page.locator('[data-testid="status-badge"]');
    this.editButton = page.locator('[data-testid="edit-{entity}-btn"]');
    this.deleteButton = page.locator('[data-testid="delete-{entity}-btn"]');
    this.confirmDialogModal = page.locator('[data-testid="confirm-dialog"]');
    this.confirmButton = page.locator('[data-testid="confirm-btn"]');
    this.cancelDialogButton = page.locator('[data-testid="cancel-dialog-btn"]');
    this.justificationInput = page.locator('[data-testid="justification-input"]');
  }

  async goto(entityId: number) {
    await this.page.goto(`/{resource}/${entityId}`);
  }

  async clickOperation(verb: string) {
    await this.page.locator(`[data-testid="${verb}-{entity}-btn"]`).click();
  }

  async confirmDialog() {
    await this.confirmButton.click();
  }

  async cancelDialog() {
    await this.cancelDialogButton.click();
  }

  async removeSubEntity(subEntityId: number, justification: string) {
    await this.page.locator(`[data-testid="remove-{subEntity}-${subEntityId}-btn"]`).click();
    await this.justificationInput.fill(justification);
    await this.confirmButton.click();
  }

  async getSubEntityCount() {
    return await this.page.locator('[data-testid="{subEntity}-row"]').count();
  }
}
