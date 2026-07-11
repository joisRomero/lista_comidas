---
name: playwright
description: >
  Playwright E2E testing patterns.
  Trigger: When writing Playwright E2E tests (Page Object Model, selectors, MCP exploration workflow).
metadata:
  author: anta
  version: "1.0"
  scope: [root, frontend]
  auto_invoke: "Writing Playwright E2E tests"
  phase: [inception, construction]
  layer: [e2e]
  validates_with: null
  validation_profile: null
---

## MCP Workflow (MANDATORY If Available)

**If you have Playwright MCP tools, ALWAYS use them BEFORE creating any test:**

1. **Navigate** to target page
2. **Take snapshot** to see page structure and elements
3. **Interact** with forms/elements to verify exact user flow
4. **Take screenshots** to document expected states
5. **Verify page transitions** through complete flow (loading, success, error)
6. **Document actual selectors** from snapshots (use real refs and labels)
7. **Only after exploring** create test code with verified selectors

**If MCP NOT available:** Proceed with test creation based on docs and code analysis.

**Why This Matters:** Precise tests, accurate selectors, real flow validation, avoid over-engineering, prevent flaky tests.

## File Structure

```
tests/
├── base-page.ts              # Parent class for ALL pages
├── helpers.ts                # Shared utilities
└── {page-name}/
    ├── {page-name}-page.ts   # Page Object Model
    ├── {page-name}.spec.ts   # ALL tests here (NO separate files!)
    └── {page-name}.md        # Test documentation
```

**File Naming:** `sign-up.spec.ts` (all tests), `sign-up-page.ts` (page object), `sign-up.md` (docs). NO separate files like `sign-up-critical-path.spec.ts`.

## Selector Priority (REQUIRED)

```typescript
// 1. BEST - getByRole for interactive elements
this.submitButton = page.getByRole("button", { name: "Submit" });

// 2. BEST - getByLabel for form controls
this.emailInput = page.getByLabel("Email");

// 3. SPARINGLY - getByText for static content only
this.errorMessage = page.getByText("Invalid credentials");

// 4. LAST RESORT - getByTestId when above fail
this.customWidget = page.getByTestId("date-picker");

// AVOID fragile selectors
this.button = page.locator(".btn-primary");  // NO
this.input = page.locator("#email");         // NO
```

## Scope Detection (ASK IF AMBIGUOUS)

| User Says | Action |
|-----------|--------|
| "a test", "one test", "new test" | Create ONE test() in existing spec |
| "comprehensive tests", "all tests", "test suite" | Create full suite |

## Page Object Reuse (CRITICAL)

**Always check existing page objects before creating new ones!**

```typescript
// GOOD: Reuse existing page objects
import { SignInPage } from "../sign-in/sign-in-page";
import { HomePage } from "../home/home-page";

test("User can sign up and login", async ({ page }) => {
  const signUpPage = new SignUpPage(page);
  const signInPage = new SignInPage(page);  // REUSE
  const homePage = new HomePage(page);      // REUSE
});

// BAD: Recreating functionality that exists in other page objects
```

## Tag Categories

- **Priority:** `@critical`, `@high`, `@medium`, `@low`
- **Type:** `@e2e`
- **Feature:** `@signup`, `@signin`, `@dashboard`
- **Test ID:** `@SIGNUP-E2E-001`, `@LOGIN-E2E-002`

## Refactoring Guidelines

### Move to `BasePage`:
Navigation helpers, common UI interactions (notifications, modals), repeated verification patterns, error handling

### Move to `helpers.ts`:
Test data generation, setup/teardown utilities, custom assertions, API helpers, time utilities

## Commands

```bash
npx playwright test                    # Run all
npx playwright test --grep "login"     # Filter by name
npx playwright test --ui               # Interactive UI
npx playwright test --debug            # Debug mode
npx playwright test tests/login/       # Run specific folder
```

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Page object templates | [page-object-templates.ts](assets/page-object-templates.ts) |

## Related Skills

- **API testing setup**: `api-first-testing`
- **React components**: `react`
