---
name: typescript
description: >
  TypeScript strict patterns and best practices.
  Trigger: When implementing or refactoring TypeScript in .ts/.tsx (types, interfaces, generics, const maps, type guards, removing any, tightening unknown).
metadata:
  author: anta
  version: "2.0"
  scope: [root, frontend]
  auto_invoke: "Writing TypeScript types/interfaces"
  phase: [construction]
  layer: [frontend]
  validates_with: validate_no_any
  validation_profile: build-component
---

## Const Types Pattern (REQUIRED)

```typescript
// ✅ ALWAYS: Create const object first, then extract type
const STATUS = {
  ACTIVE: "active",
  INACTIVE: "inactive",
  PENDING: "pending",
} as const;

type Status = (typeof STATUS)[keyof typeof STATUS];

// ❌ NEVER: Direct union types
type Status = "active" | "inactive" | "pending";
```

**Why?** Single source of truth, runtime values, autocomplete, easier refactoring.

## Flat Interfaces (REQUIRED)

```typescript
// ✅ ALWAYS: One level depth, nested objects → dedicated interface
interface UserAddress {
  street: string;
  city: string;
}

interface User {
  id: string;
  name: string;
  address: UserAddress;  // Reference, not inline
}

interface Admin extends User {
  permissions: string[];
}

// ❌ NEVER: Inline nested objects
interface User {
  address: { street: string; city: string };  // NO!
}
```

## Never Use `any`

```typescript
// ✅ Use unknown for truly unknown types
function parse(input: unknown): User {
  if (isUser(input)) return input;
  throw new Error("Invalid input");
}

// ✅ Use generics for flexible types
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

// ❌ NEVER
function parse(input: any): any { }
```

## Utility Types

```typescript
Pick<User, "id" | "name">     // Select fields
Omit<User, "id">              // Exclude fields
Partial<User>                 // All optional
Required<User>                // All required
Readonly<User>                // All readonly
Record<string, User>          // Object type
Extract<Union, "a" | "b">     // Extract from union
Exclude<Union, "a">           // Exclude from union
NonNullable<T | null>         // Remove null/undefined
ReturnType<typeof fn>         // Function return type
Parameters<typeof fn>         // Function params tuple
```

## Type Guards

```typescript
function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value
  );
}
```

## Import Types

```typescript
import type { User } from "./types";
import { createUser, type Config } from "./utils";
```

## Response API Generic Type

The project uses a standard API response wrapper:

```typescript
// shared/utils/types.ts
export interface ResponseApi<T> {
  success: boolean;
  data: T;
  message: string | null;
  errors: Array<{
    code: string | null;
    field: string | null;
    message: string | null;
  }> | null;
  pagination: {
    page: number;
    pageSize: number;
    totalRecords: number;
    totalPages: number;
    hasNext: boolean;
    hasPrevious: boolean;
  };
  metadata: Record<string, unknown> | null;
}
```

## Request Type Patterns

Requests extend `Record<string, unknown>`:

```typescript
export interface CreateCaseRequest extends Record<string, unknown> {
  caseName: string | null;
  caseTypeId: number;
  estimatedAmount: number;
  providers: ProviderItem[] | null;
  // ...
}
```

## Service ID Constants

Use `as const` for service IDs:

```typescript
export const CasesService = {
  GetCases: 3001,
  PostCreateCase: 3002,
  PutUpdateCase: 3003,
} as const;
```

## Enum Pattern

Use string enums for statuses and catalogs:

```typescript
export enum AGENDA_STATUS {
  DRAFT = 'DRAFT',
  SCHEDULED = 'SCHEDULED',
  IN_PROGRESS = 'IN_PROGRESS',
  COMPLETED = 'COMPLETED',
  CANCELLED = 'CANCELLED',
}

export enum CATALOG {
  CASE_TYPES = 'CASE_TYPES',
  PROCESS_TYPES = 'PROCESS_TYPES',
  DURATION_UNITS = 'DURATION_UNITS',
}
```

## Module Declarations (env.d.ts)

```typescript
declare module '*.svg?react' {
  import type React from 'react';
  const ReactComponent: React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
  export default ReactComponent;
}

declare module '*.module.css' {
  const classes: { readonly [key: string]: string };
  export default classes;
}

// Host Module Federation declarations
declare module 'host/factories' {
  export const createServiceQuery: (...) => ...;
  export const createServiceMutation: (...) => ...;
  // etc.
}

declare module 'host/toast' { ... }
declare module 'host/logger' { ... }
declare module 'host/session' { ... }
declare module 'host/hooks' { ... }
```

## Nullable Fields Pattern

API types use `string | null` (not optional):

```typescript
// CORRECT (project pattern)
interface CaseItem {
  caseName: string | null;
  description: string | null;
  currentStatus: StatusItem | null;
}

// INCORRECT (not used in this project)
interface CaseItem {
  caseName?: string;
  description?: string;
}
```

## Status Item Type

Common pattern for status objects:

```typescript
interface StatusItem {
  masterTableId: number;
  name: string | null;
  value: string | null;
  backgroundColor: string | null;
  textColor: string | null;
  type: string | null;
}
```

## Props Interface Pattern

Use `readonly` for component props:

```typescript
interface CasesTableProps {
  readonly isSupplyProfile: boolean;
  readonly isSecretariatProfile: boolean;
}
```

## Generic Table Props

```typescript
export interface AntaTableProps<T extends object = object> extends TableProps<T> {}
```

