---
name: react-hooks
description: >
  React hooks patterns for ANTA: Query, Mutation, Logic hooks, state management.
  Trigger: When implementing hooks, calling APIs, or managing state.
metadata:
  author: anta
  version: "2.0"
  scope: [root]
  auto_invoke: "hook, useQuery, useMutation, TanStack Query, API call, estado"
  phase: [construction]
  layer: [frontend]
  validates_with: validate_react_feature
  validation_profile: build-component
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Use `enabled` param for conditional queries | ALWAYS | Control when query runs |
| Return `{ verbAction, isPending }` from mutations | ALWAYS | Property name matches the action verb (create, submit, delete, add, etc.) |
| Extract ALL page logic to `use{Feature}Logic` | ALWAYS | Separation of concerns |
| Use `pathParams` for URL parameters | ALWAYS | Host adapter pattern |
| Access data as `data?.data.items` | ALWAYS | API response structure |

---

## Hook Types

| Hook Type | Purpose | Returns |
|-----------|---------|---------|
| Query | GET requests | `useQuery` result |
| Mutation | POST/PUT/DELETE | `{ verbAction, isPending }` where verbAction is: create, submit, delete, add, remove, validate, observe, reject, etc. |
| Logic | Page state + handlers | Data, State, Handlers |

---

## Adapter Pattern

Children consume Host factories through adapters:

```typescript
// shared/adapters/useHostApi.ts
import { createServiceMutation, createServiceQuery, createServiceBlobMutation } from 'host/factories';

/**
 * Adapter para consumir la factory de queries del Host
 * Facilita cambios futuros en la integración con el host
 */
export const useHostServiceQuery = () => createServiceQuery;

/**
 * Adapter para consumir la factory de mutaciones del Host
 * Facilita cambios futuros en la integración con el host
 */
export const useHostServiceMutation = () => createServiceMutation;

/**
 * Adapter para consumir la factory de mutaciones blob del Host
 * Facilita cambios futuros en la integración con el host
 */
export const useHostServiceBlobMutation = () => createServiceBlobMutation;
```
NOTE: These are NOT real hooks — they return factory functions directly. Named "use" by convention for consistency.

---

## Host API Factories (Reference)

The Host exports 5 factory functions via Module Federation. They abstract **Ky HTTP client + TanStack Query + Lion service resolution**. Children never import Ky or build URLs manually.

### Factory API

| Factory | Returns | Purpose |
|---------|---------|---------|
| `createServiceQuery<TData, TParams>(serviceId, queryParams?, pathParams?, options?)` | `UseQueryResult<TData>` | GET request via service ID |
| `createProcessQuery<TData, TParams>(processId, serviceIndex?, queryParams?, pathParams?, options?)` | `UseQueryResult<TData>` | GET request via process ID |
| `createServiceMutation<TData, TVariables>(serviceId, options?)` | `UseMutationResult<TData, Error, TVariables>` | POST/PUT/DELETE via service ID |
| `createProcessMutation<TData, TVariables>(processId, serviceIndex?, options?)` | `UseMutationResult<TData, Error, TVariables>` | POST/PUT/DELETE via process ID |
| `createServiceBlobMutation<TVariables>(serviceId, options?)` | `UseMutationResult<Blob, Error, TVariables>` | Binary download (PDF/Excel) |

### Service Resolution

Factories resolve endpoints **dynamically** from the user's menu context (Lion permissions):

```
serviceId (number) → useCurrentOption() → menu.services[serviceId] → { method, path }
```

If the user lacks permission to a service, the factory **throws** — no silent failures.

### pathParams Pattern

Mutations support path parameter interpolation via a `pathParams` property in the variables object:

```typescript
// Factory destructures pathParams from variables, sends rest as JSON body
// URL: /clinic-groups/:clinicGroupId → /clinic-groups/123
mutation.mutate({
  pathParams: { clinicGroupId: '123' },  // Interpolated into URL
  name: 'Updated Name',                   // Sent as JSON body
  description: null,
});
```

### Query Key Strategy

Factories build query keys automatically: `[serviceId, queryParams, pathParams, enabled]`. This ensures proper cache invalidation when params change.

### Usage Examples

**Query** — List with filters:
```typescript
export function useClinicsQuery(filters: ClinicsFilters) {
  const createServiceQuery = useHostServiceQuery();
  return createServiceQuery<ResponseApi<ClinicsData[]>, ClinicsFilters>(
    ClinicsService.FindAll,
    filters,  // queryParams → ?page=1&pageSize=10&search=...
  );
}
```

**Mutation** — Create/Update with pathParams:
```typescript
export function useUpdateClinicGroup() {
  const createServiceMutation = useHostServiceMutation();
  const mutation = createServiceMutation<ResponseApi<MutationResult>, UpdateClinicGroupRequest>(
    ClinicGroupsService.Update,
  );

  return {
    update: (data: UpdateClinicGroupRequest, options?: { onSuccess?: () => void }) =>
      mutation.mutate(data, { onSuccess: () => options?.onSuccess?.() }),
    isPending: mutation.isPending,
  };
}
```

**Blob Mutation** — Excel export:
```typescript
export function useExportClinics() {
  const createServiceBlobMutation = useHostServiceBlobMutation();
  const mutation = createServiceBlobMutation<ExportClinicsRequest>(
    ClinicsService.Export,
  );

  return {
    exportExcel: (filters: ExportClinicsRequest) => mutation.mutate(filters),
    isPending: mutation.isPending,
  };
}
```

> **Service IDs**: Defined in `shared/utils/service-ids.ts` as enums mapping to Lion process IDs.

---

## Quick Reference

### Query Hook Structure

```typescript
// Simple query (no params) — e.g. get current user data
import { useHostServiceQuery } from '../../../shared/adapters/useHostApi';
import { FeatureService } from '../types';
import type { ResponseApi, EmployeeDto } from '../../../shared/utils/types';

export type FeatureResponse = ResponseApi<EmployeeDto>;

export function useFeatureQuery() {
  const createQuery = useHostServiceQuery();
  return createQuery<FeatureResponse>(FeatureService.GetFeature);
}

// Query with params — e.g. paginated list with search
export function useFeatureListQuery(params?: FeatureListParams, enabled = true) {
  const createQuery = useHostServiceQuery();
  return createQuery<FeatureListResponse, FeatureListParams>(
    FeatureService.GetFeatureList,
    params,
    undefined,
    { enabled, staleTime: 0 }
  );
}

// Query with path params
export function useCase(generalDataId: number, enabled = true) {
  const createQuery = useHostServiceQuery();
  return createQuery<CaseResponse>(
    CaseService.GetCase,
    undefined,
    { generalDataId: generalDataId.toString() },
    { enabled }
  );
}
```

> **Key patterns**: Define response type alias (`export type XResponse = ResponseApi<XDto>`) in the hook file or types.ts. Import service IDs from types/constants.

### Mutation Hook Structure

```typescript
import { useHostServiceMutation } from '../../../shared/adapters/useHostApi';
import { FeatureService } from '../types/constants';

// Request type MUST extend Record<string, unknown> (required by host factory)
export interface UpdateFeatureRequest extends Record<string, unknown> {
  contactPhone: string;
  contactEmail: string;
}

export interface UpdateFeatureResponse {
  success: boolean;
  data: { message: string };
  message: string | null;
  errors: Array<{ code: string | null; field: string | null; message: string | null }> | null;
  pagination: { page: number; pageSize: number; totalRecords: number; totalPages: number; hasNext: boolean; hasPrevious: boolean } | null;
  metadata: Record<string, unknown> | null;
}

export function useUpdateFeatureMutation() {
  const createServiceMutation = useHostServiceMutation();
  const updateMutation = createServiceMutation<UpdateFeatureResponse, UpdateFeatureRequest>(
    FeatureService.UpdateFeature
  );

  return {
    update: (data: UpdateFeatureRequest, options?: { onSuccess?: () => void }) =>
      updateMutation.mutate(data, { onSuccess: () => options?.onSuccess?.() }),
    isPending: updateMutation.isPending,
    isError: updateMutation.isError,
    error: updateMutation.error,
  };
}
```

> **CRITICAL**: Request interfaces MUST `extends Record<string, unknown>` — the host factory requires this constraint.

More mutation naming examples:
- `useSubmitCase` → `{ submit, isPending }`
- `useDeleteCase` → `{ delete: deleteCase, isPending }` (note: backtick or alias needed in destructure)
- `useTakeForReview` → `{ takeForReview, isPending }`
- `useAddParticipant` → `{ add, isPending }`
- `useRemoveParticipant` → `{ remove, isPending }`
- `useValidateCase` → `{ validate, isPending }`
- `useObserveCase` → `{ observe, isPending }`
- `useRejectCase` → `{ reject, isPending }`

### Blob Mutation Hook

```typescript
export function useGenerateActaByCase() {
  const createMutation = useHostServiceBlobMutation();
  const mutation = createMutation<Record<string, unknown>>(CasesService.GenerateActa);

  return {
    generate: (generalDataId: number, options?: { onSuccess?: () => void }) =>
      mutation.mutate(
        { pathParams: { generalDataId: generalDataId.toString() } },
        {
          onSuccess: (blob) => {
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'Acta.pdf';
            link.click();
            window.URL.revokeObjectURL(url);
            options?.onSuccess?.();
          },
        },
      ),
    isPending: mutation.isPending,
  };
}
```

### Composite/Catalog Hook

```typescript
export function useCatalogs() {
  const createQuery = useHostServiceQuery();
  
  const documentTypes = createQuery<CatalogResponse>(CatService.GetDocs, undefined, undefined, { staleTime: 300000 });
  const caseTypes = createQuery<CatalogResponse>(CatService.GetCaseTypes, undefined, undefined, { staleTime: 300000 });
  
  return {
    documentTypes: documentTypes.data?.data.items ?? [],
    caseTypes: caseTypes.data?.data.items ?? [],
    isLoading: documentTypes.isLoading || caseTypes.isLoading,
    isError: documentTypes.isError || caseTypes.isError,
    refetchAll: () => Promise.all([documentTypes.refetch(), caseTypes.refetch()]),
  };
}
```

### Logic Hook Structure

```typescript
import { useState } from 'react';
import { useCurrentProfile } from 'host/session';
import { useFeatureQuery } from './useFeatureQuery';
import { useUpdateFeatureMutation, type UpdateFeatureRequest } from './useFeatureMutation';

const PROFILES_WITH_LIST_ACCESS = ['200-146-USER'];

export const useFeatureLogic = () => {
  // Local state
  const [editMode, setEditMode] = useState(false);
  const [pageNumber, setPageNumber] = useState(1);
  const [pageSize] = useState(10);
  const [listSearchQuery, setListSearchQuery] = useState('');
  const [editItemVisible, setEditItemVisible] = useState(false);
  const [selectedItem, setSelectedItem] = useState<FeatureItem | null>(null);

  // Host hooks — useCurrentProfile from host/session
  const profile = useCurrentProfile();
  const hasListAccess = PROFILES_WITH_LIST_ACCESS.includes(profile?.Key ?? '');

  // Queries
  const { data: featureResponse, isLoading, refetch } = useFeatureQuery();
  const updateMutation = useUpdateFeatureMutation();

  // Derived data
  const featureData = featureResponse?.data;

  // Handlers
  const handleUpdate = (data: UpdateFeatureRequest) => {
    updateMutation.update(data, {
      onSuccess: () => { setEditMode(false); refetch(); },
    });
  };

  const handleCancelEdit = () => setEditMode(false);
  const handlePageChange = (page: number) => setPageNumber(page);

  const handleListFilter = (search: string) => {
    setListSearchQuery(search);
    setPageNumber(1); // Reset page on filter change
  };

  return {
    // Data
    featureData, isLoading,
    // State
    editMode, setEditMode,
    // Handlers
    handleUpdate, handleCancelEdit, isUpdating: updateMutation.isPending,
    // List data
    hasListAccess, pageNumber, pageSize, handlePageChange,
    handleListFilter,
    // Modal state
    editItemVisible, selectedItem,
  };
};
```

> **Key patterns**: Use `useCurrentProfile()` from `host/session` for profile-based feature flags. Organize return as Data → State → Handlers. Reset page on filter change.

---

## Accessing API Data

```typescript
// Flat response (single object) — e.g. current feature data
const { data: featureResponse } = useFeatureQuery();
const featureData = featureResponse?.data;  // data?.data for flat response

// List response (paginated) — e.g. feature list with filters
const { data: featureListData } = useFeatureListQuery(params);
const items = featureListData?.data?.items ?? [];  // data?.data?.items for list
const totalRecords = featureListData?.pagination?.totalRecords ?? 0;
const totalPages = featureListData?.pagination?.totalPages ?? 0;
```

> **Note**: Use `??` (nullish coalescing) with `[]` or `0` defaults, not `||`.

---

## Modal State Pattern

```typescript
const [modal, setModal] = useState<{
  open: boolean;
  item: ItemType | null;
}>({ open: false, item: null });
```

---

## Error Handling

The project's QueryClient handles errors globally via queryCache and mutationCache. No need for per-mutation error handling in most cases.

| Function | Purpose |
|----------|---------|
| `handleError(error, context)` | Display toast based on error type |
| `withRetry(fn, maxRetries, delay)` | Auto-retry with exponential backoff |
| `useConfirm()` | Modal.confirm from Ant Design |
| `useErrorHandler()` | Unified hook for error handling |

---

## TanStack Query v5 Notes

- `onSuccess`/`onError` removed from `useQuery` options in v5.
- `cacheTime` renamed to `gcTime`.
- `isLoading` renamed to `isPending`.
- Project uses `staleTime: 0` for most queries (always refetch).
- QueryClient defaults: `retry: 0`, `refetchOnWindowFocus: false`, `staleTime: 5min`, `gcTime: 10min`.

---

## Checklist

### Query Hooks
- [ ] `enabled` parameter for conditional fetching
- [ ] Types defined in same file (Params, Data, Response)
- [ ] Return full query result
- [ ] `pathParams` converted to string always

### Mutation Hooks
- [ ] Return `{ verbAction, isPending }` (not `{ action, isPending }`)
- [ ] Verb matches hook name (useCreateX → create, useDeleteX → delete)
- [ ] `pathParams` for URL parameters (converted to string)
- [ ] Optional `onSuccess` callback

### Logic Hooks
- [ ] ALL page logic extracted
- [ ] Organized return (Data, State, Handlers)
- [ ] Modal state with `{ open, item }` pattern
- [ ] Reset page on filter change
- [ ] Uses `useConfirm()` for confirmations
- [ ] Uses toast from `host/toast` for notifications
- [ ] Uses `navigate` with state for navigation

### Data Access
- [ ] `data?.data.items` for lists
- [ ] `data?.data.item` for single
- [ ] Default to `[]` or `null`

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Query, Mutation, Logic hook templates | [hook-templates.ts](assets/hook-templates.ts) |
| Error handling (handleError, withRetry, useConfirm) | [error-handling.ts](assets/error-handling.ts) |
| File upload/download hooks (S3 presigned) | [file-hooks.ts](assets/file-hooks.ts) |

## Related Skills

- **Component Patterns**: `react`
- **Microfrontend Adapters**: `microfrontend`
- **Host Exports**: `microfrontend` for factories

