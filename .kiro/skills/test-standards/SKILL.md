---
name: test-standards
description: >
  Unit test conventions for ANTA backend (.NET xUnit) and frontend (Vitest + React Testing Library).
  Trigger: When generating unit tests, component tests, or test infrastructure.
metadata:
  author: anta
  version: "1.0"
  scope: [root]
  auto_invoke: "unit test, test, xunit, vitest, testing library, spec, test file"
  phase: [construction]
  layer: [backend, frontend]
  validates_with: null
  validation_profile: null
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Backend uses xUnit + NSubstitute + FluentAssertions | ALWAYS | Matches ANTA shared libraries (ANTA.Shared.Common.Tests) |
| Frontend uses Vitest + React Testing Library | ALWAYS | Rsbuild-compatible, modern, fast |
| Test naming: `Method_Scenario_Expected` (backend) | ALWAYS | Consistency across ANTA projects |
| Test naming: `*.spec.tsx` / `*.spec.ts` (frontend) | ALWAYS | ANTA standard, colocated with source |
| Arrange/Act/Assert pattern | ALWAYS | Readable, debuggable |
| NO `@vitejs/plugin-react` in test config | NEVER | ANTA uses Rsbuild, not Vite. Use `@swc/jest` transform or Vitest builtin JSX |
| NO Moq — use NSubstitute | ALWAYS | Cleaner syntax, ANTA standard |
| NO Jest — use Vitest | ALWAYS | Better ESM/TypeScript support with Rsbuild |
| ALL test files use `*.spec.ts(x)` | ALWAYS | Single convention for unit + E2E (Vitest supports both `.test` and `.spec`) |
| Test descriptions in Spanish | ALWAYS | Matches domain language and UI labels |

---

# Backend Unit Tests (.NET)

## Stack

| Package | Version | Purpose |
|---------|---------|---------|
| `xunit` | 2.6.2 | Test framework |
| `xunit.runner.visualstudio` | 2.5.4 | Test runner |
| `Microsoft.NET.Test.Sdk` | 17.8.0 | Test SDK |
| `FluentAssertions` | 6.12.0 | Readable assertions |
| `NSubstitute` | 5.1.0 | Mocking (NOT Moq) |
| `coverlet.collector` | 6.0.0 | Code coverage |

## Project Structure

```
{ApiProject}/
├── src/
│   └── {Project}.Api/
│       ├── Modules/
│       │   └── {Module}/
│       │       ├── Handlers/
│       │       ├── Endpoints/
│       │       └── Validators/
│       └── {Project}.Api.csproj
└── tests/
    └── {Project}.Api.Tests/
        ├── Modules/
        │   └── {Module}/
        │       ├── Handlers/
        │       │   └── Create{Entity}HandlerTests.cs
        │       └── Validators/
        │           └── Create{Entity}ValidatorTests.cs
        ├── Fixtures/
        │   └── DapperMockHelpers.cs
        └── {Project}.Api.Tests.csproj
```

## Test Project (.csproj)

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
    <PackageReference Include="xunit" Version="2.6.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.5.4">
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
    <PackageReference Include="FluentAssertions" Version="6.12.0" />
    <PackageReference Include="NSubstitute" Version="5.1.0" />
    <PackageReference Include="coverlet.collector" Version="6.0.0">
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\..\src\{Project}.Api\{Project}.Api.csproj" />
  </ItemGroup>
</Project>
```

## Naming Convention

```
{MethodName}_{Scenario}_{ExpectedResult}
```

Examples:
- `Handle_WhenEmployeeExists_ReturnsEmployee`
- `Handle_WhenEmployeeNotFound_ReturnsNotFoundError`
- `Validate_WhenEmailEmpty_ShouldHaveValidationError`
- `Validate_WhenRequestValid_ShouldNotHaveErrors`

## Handler Test (Dapper + SP)

```csharp
using FluentAssertions;
using NSubstitute;
using System.Data;
using Xunit;

namespace MyProject.Api.Tests.Modules.Employees.Handlers;

public class GetEmployeeHandlerTests
{
    private readonly IDbConnection _db;
    private readonly GetEmployeeHandler _handler;

    public GetEmployeeHandlerTests()
    {
        _db = Substitute.For<IDbConnection>();
        _handler = new GetEmployeeHandler(_db);
    }

    [Fact]
    public async Task Handle_WhenEmployeeExists_ReturnsEmployee()
    {
        // Arrange
        var request = new GetEmployeeRequest { EmployeeId = 1 };
        var expected = new EmployeeResponse { EmployeeId = 1, Name = "Juan Perez" };

        _db.QuerySingleOrDefaultAsync<EmployeeResponse>(
            Arg.Any<string>(),
            Arg.Any<object>(),
            commandType: CommandType.StoredProcedure
        ).Returns(expected);

        // Act
        var result = await _handler.Handle(request);

        // Assert
        result.Success.Should().BeTrue();
        result.Data.Should().BeEquivalentTo(expected);
    }

    [Fact]
    public async Task Handle_WhenEmployeeNotFound_ReturnsNotFoundError()
    {
        // Arrange
        var request = new GetEmployeeRequest { EmployeeId = 999 };

        _db.QuerySingleOrDefaultAsync<EmployeeResponse>(
            Arg.Any<string>(),
            Arg.Any<object>(),
            commandType: CommandType.StoredProcedure
        ).Returns((EmployeeResponse?)null);

        // Act
        var result = await _handler.Handle(request);

        // Assert
        result.Success.Should().BeFalse();
        result.Errors.Should().ContainSingle()
            .Which.Code.Should().Be("BUS_001");
    }
}
```

## Validator Test (FluentValidation)

```csharp
using FluentValidation.TestHelper;
using Xunit;

namespace MyProject.Api.Tests.Modules.Employees.Validators;

public class CreateEmployeeValidatorTests
{
    private readonly CreateEmployeeValidator _validator = new();

    [Fact]
    public void Validate_WhenNameEmpty_ShouldHaveValidationError()
    {
        // Arrange
        var model = new CreateEmployeeRequest { Name = "", Email = "test@anta.com" };

        // Act
        var result = _validator.TestValidate(model);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Name);
    }

    [Fact]
    public void Validate_WhenRequestValid_ShouldNotHaveErrors()
    {
        // Arrange
        var model = new CreateEmployeeRequest
        {
            Name = "Juan Perez",
            Email = "jperez@antamina.com",
            AreaId = 1
        };

        // Act
        var result = _validator.TestValidate(model);

        // Assert
        result.ShouldNotHaveAnyValidationErrors();
    }

    [Theory]
    [InlineData("")]
    [InlineData("invalid")]
    [InlineData("@nodomain")]
    public void Validate_WhenEmailInvalid_ShouldHaveValidationError(string email)
    {
        // Arrange
        var model = new CreateEmployeeRequest { Name = "Test", Email = email };

        // Act
        var result = _validator.TestValidate(model);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Email);
    }
}
```

## SP Error Code Test

```csharp
[Fact]
public async Task Handle_WhenSpReturnsErrorCode_ReturnsMappedError()
{
    // Arrange
    var request = new CreateEmployeeRequest { Name = "Duplicate" };
    var spResult = new SpResultHelper { ErrorCode = "VAL_001", ErrorMessage = "Employee already exists" };

    _db.QuerySingleAsync<SpResultHelper>(
        Arg.Any<string>(),
        Arg.Any<object>(),
        commandType: CommandType.StoredProcedure
    ).Returns(spResult);

    // Act
    var result = await _handler.Handle(request);

    // Assert
    result.Success.Should().BeFalse();
    result.Errors.Should().ContainSingle()
        .Which.Code.Should().Be("VAL_001");
}
```

## What to Test (Backend)

| Layer | Test | Example |
|-------|------|---------|
| **Handlers** | Happy path + error codes + null cases | SP returns data / SP returns error / SP returns null |
| **Validators** | Required fields, format, range, combinations | Empty name, invalid email, negative amounts |
| **SP Result Mapping** | ErrorCode mapping to ApiResponse | VAL_001→validation, BUS_001→business, null→success |
| **Endpoint registration** | Routes exist with correct HTTP method | GET /employees, POST /employees |

## Running Backend Tests

```bash
# All tests
dotnet test tests/{Project}.Api.Tests/

# With coverage
dotnet test tests/{Project}.Api.Tests/ --collect:"XPlat Code Coverage"

# Specific class
dotnet test --filter "FullyQualifiedName~CreateEmployeeHandlerTests"
```

---

# Frontend Unit Tests (React)

## Stack

| Package | Version | Purpose |
|---------|---------|---------|
| `vitest` | latest | Test runner (Rsbuild-compatible) |
| `@testing-library/react` | latest | Component rendering + queries |
| `@testing-library/jest-dom` | latest | DOM matchers (toBeInTheDocument, etc.) |
| `@testing-library/user-event` | latest | User interaction simulation |
| `jsdom` | latest | Browser environment for tests |

## Setup

**Install** (devDependencies):
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

**vitest.config.ts** (at project root — NO Vite plugins):
```typescript
import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      'host/factories': path.resolve(__dirname, './src/__mocks__/host-factories.ts'),
      'host/hooks': path.resolve(__dirname, './src/__mocks__/host-hooks.ts'),
      'host/toast': path.resolve(__dirname, './src/__mocks__/host-toast.ts'),
      'host/session': path.resolve(__dirname, './src/__mocks__/host-session.ts'),
    },
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test-setup.ts'],
    include: ['src/**/*.spec.{ts,tsx}'],
    exclude: ['node_modules', 'dist'],
  },
});
```

**src/test-setup.ts**:
```typescript
import '@testing-library/jest-dom';
import { afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';

afterEach(() => {
  cleanup();
});
```

**package.json** scripts:
```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage"
  }
}
```

## Module Federation Mocks

Since children import from `host/*` via Module Federation, tests need mocks:

```typescript
// src/__mocks__/host-factories.ts
export const createServiceQuery = () => ({ data: null, isLoading: false, error: null });
export const createServiceMutation = () => ({ mutate: () => {}, isPending: false });
export const createServiceBlobMutation = () => ({ mutate: () => {}, isPending: false });

// src/__mocks__/host-hooks.ts
export const useCurrentOption = () => ({ getProcessById: () => null });
export const useErrorHandler = () => ({ handleError: () => {} });
export const useConfirm = () => ({ confirm: () => Promise.resolve(true) });

// src/__mocks__/host-toast.ts
export const toast = {
  success: () => {},
  error: () => {},
  info: () => {},
  warning: () => {},
};

// src/__mocks__/host-session.ts
export const useCurrentUser = () => ({ id: '1', name: 'Test User' });
export const useCurrentProfile = () => ({ Key: 'ADMIN' });
```

> These mocks are resolved via `resolve.alias` in vitest.config.ts — no `vi.mock()` needed per test file.

## Project Structure

Tests colocated with source:

```
src/
├── features/
│   └── employees/
│       ├── EmployeesPage.tsx
│       ├── EmployeesPage.spec.tsx          # Page test
│       ├── hooks/
│       │   ├── useEmployeesLogic.ts
│       │   └── useEmployeesLogic.spec.ts   # Hook test
│       └── components/
│           ├── EmployeeForm.tsx
│           └── EmployeeForm.spec.tsx        # Component test
├── shared/
│   └── utils/
│       ├── formatDate.ts
│       └── formatDate.spec.ts              # Utility test
├── __mocks__/                              # Module Federation mocks
│   ├── host-factories.ts
│   ├── host-hooks.ts
│   ├── host-toast.ts
│   └── host-session.ts
├── test-setup.ts
└── test-utils/
    └── createQueryWrapper.tsx              # Shared test wrapper
```

## Query Client Wrapper

```typescript
// src/test-utils/createQueryWrapper.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import type { ReactNode } from 'react';

export function createQueryWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0 },
      mutations: { retry: false },
    },
  });

  return function Wrapper({ children }: { children: ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    );
  };
}
```

## Hook Test

```typescript
// features/employees/hooks/useEmployeesLogic.spec.ts
import { renderHook, act, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { useEmployeesLogic } from './useEmployeesLogic';
import { createQueryWrapper } from '@/test-utils/createQueryWrapper';

describe('useEmployeesLogic', () => {
  it('should initialize with empty filters', () => {
    const { result } = renderHook(() => useEmployeesLogic(), {
      wrapper: createQueryWrapper(),
    });

    expect(result.current.filters.search).toBe('');
    expect(result.current.filters.page).toBe(1);
  });

  it('should update search filter', () => {
    const { result } = renderHook(() => useEmployeesLogic(), {
      wrapper: createQueryWrapper(),
    });

    act(() => {
      result.current.setSearch('Juan');
    });

    expect(result.current.filters.search).toBe('Juan');
    expect(result.current.filters.page).toBe(1); // Reset to page 1
  });
});
```

## Component Test

```typescript
// features/employees/components/EmployeeForm.spec.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { EmployeeForm } from './EmployeeForm';
import { createQueryWrapper } from '@/test-utils/createQueryWrapper';

describe('EmployeeForm', () => {
  it('should render all form fields', () => {
    render(<EmployeeForm onSubmit={() => {}} />, {
      wrapper: createQueryWrapper(),
    });

    expect(screen.getByLabelText(/nombre/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /guardar/i })).toBeInTheDocument();
  });

  it('should call onSubmit with form data', async () => {
    const onSubmit = vi.fn();
    const user = userEvent.setup();

    render(<EmployeeForm onSubmit={onSubmit} />, {
      wrapper: createQueryWrapper(),
    });

    await user.type(screen.getByLabelText(/nombre/i), 'Juan Perez');
    await user.type(screen.getByLabelText(/email/i), 'jperez@antamina.com');
    await user.click(screen.getByRole('button', { name: /guardar/i }));

    expect(onSubmit).toHaveBeenCalledWith(
      expect.objectContaining({
        name: 'Juan Perez',
        email: 'jperez@antamina.com',
      })
    );
  });

  it('should show validation error for empty name', async () => {
    const user = userEvent.setup();

    render(<EmployeeForm onSubmit={() => {}} />, {
      wrapper: createQueryWrapper(),
    });

    await user.click(screen.getByRole('button', { name: /guardar/i }));

    expect(await screen.findByText(/nombre es requerido/i)).toBeInTheDocument();
  });
});
```

## What to Test (Frontend)

| Layer | Test | Example |
|-------|------|---------|
| **Logic hooks** | State changes, filter updates, pagination | `useEmployeesLogic` search/page/sort |
| **Mutation hooks** | mutate called with correct params | `useCreateEmployee` calls factory |
| **Components** | Renders fields, handles events, shows errors | Form renders, submit calls onSubmit |
| **Utils** | Pure function input/output | `formatDate`, `formatCurrency` |

## What NOT to Test (Frontend)

| Skip | Reason |
|------|--------|
| Ant Design internals (AntaTable sorting, AntaModal open/close) | Tested by Ant Design |
| Module Federation loading | Infrastructure, not app logic |
| CSS Module class names | Brittle, no business value |
| Host adapter implementations | Mocked — tested in host project |

## Running Frontend Tests

```bash
# All tests
npm test

# Watch mode (dev)
npm run test:watch

# With coverage
npm run test:coverage

# Specific file
npx vitest run src/features/employees/hooks/useEmployeesLogic.spec.ts
```

---

## Checklist

### Backend
- [ ] Test project `{Project}.Api.Tests.csproj` with xUnit + NSubstitute + FluentAssertions
- [ ] Handler tests: happy path + error codes + null/empty cases
- [ ] Validator tests: required fields + format + [Theory] for multiple inputs
- [ ] SP error mapping tests: VAL_xxx, BUS_xxx → ApiResponse.Fail
- [ ] `dotnet test` passes with 0 failures

### Frontend
- [ ] `vitest.config.ts` with jsdom + Module Federation alias mocks
- [ ] `test-setup.ts` with jest-dom + cleanup
- [ ] `__mocks__/` for host/* Module Federation imports
- [ ] `test-utils/createQueryWrapper.tsx` for TanStack Query
- [ ] Logic hook tests: state changes, filter updates
- [ ] Component tests: render + interaction + validation errors
- [ ] `npm test` passes with 0 failures

---

## Related Skills

| Task | Skill |
|------|-------|
| Handler patterns | `dotnet-handler` |
| FluentValidation | `dotnet-api` |
| React hooks | `react-hooks` |
| React components | `react` |
| E2E / API tests | `api-first-testing`, `playwright` |
