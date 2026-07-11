---
name: api-first-frontend
description: >
  Generate frontend code from OpenAPI spec: TypeScript types, React Query hooks, base components.
  Trigger: When implementing frontend from OpenAPI spec, generating types from endpoints.
metadata:
  author: anta
  version: "3.0"
  scope: [root]
  enforcement: mandatory
  auto_invoke: "api first frontend, openapi types, swagger frontend, generate frontend"
  phase: [construction]
  layer: [frontend]
  validates_with: null
  validation_profile: null
---

## Workflow

```
OpenAPI Spec → Parse → Generate Service IDs → Generate Hooks (with inline types) → Generate Logic Hook → Generate Page
```

---

## Step 1: Parse OpenAPI Spec

Extract from spec:
- Schemas from `components/schemas`
- Endpoints from `paths`
- Request/Response types per endpoint

---

## Step 2: Generate TypeScript Types

Types are defined **INLINE** in hook files (except form types and constants).

| OpenAPI Type | TypeScript Type |
|--------------|-----------------|
| `integer` | `number` |
| `string` | `string` |
| `string` (format: date-time) | `string` |
| `boolean` | `boolean` |
| `array` | `T[]` |
| `object` | `interface` |

**Note:** All nullable fields use `string | null` (not optional `string?`). Request types must extend `Record<string, unknown>`.

---

## Step 3: Generate Query Hooks

Update to use adapter pattern:

```typescript
export function use{Entity}s(params?: {Entity}sQueryParams, enabled = true) {
  const createQuery = useHostServiceQuery();
  return createQuery<{Entity}sResponse, {Entity}sQueryParams>(
    {Feature}Service.Get{Entity}s,
    params,
    undefined,
    { enabled, staleTime: 0 }
  );
}

// With path params
export function use{Entity}(id: number, enabled = true) {
  const createQuery = useHostServiceQuery();
  return createQuery<{Entity}Response>(
    {Feature}Service.Get{Entity}ById,
    undefined,
    { id: id.toString() },
    { enabled }
  );
}
```

---

## Step 4: Generate Mutation Hooks

Update to use adapter pattern and REAL naming. NO query invalidation or toasts here.

```typescript
export function useCreate{Entity}() {
  const createServiceMutation = useHostServiceMutation();
  const createMutation = createServiceMutation<Create{Entity}Response, Create{Entity}Request>(
    {Feature}Service.PostCreate{Entity},
  );

  return {
    create: (data: Create{Entity}Request, options?: { onSuccess?: () => void }) =>
      createMutation.mutate(data, {
        onSuccess: () => options?.onSuccess?.(),
      }),
    isPending: createMutation.isPending,
  };
}
```

---

## Step 4b: Generate Operation Mutation Hooks

Operations (state transitions) are mutations with verb-based naming. Request body may be empty or have specific fields:

```typescript
export function use{Verb}{Entity}() {
  const createServiceMutation = useHostServiceMutation();
  const createMutation = createServiceMutation<{Verb}{Entity}Response, {Verb}{Entity}Request>(
    {Feature}Service.Post{Verb}{Entity},
  );

  return {
    {verb}: (data: {Verb}{Entity}Request, options?: { onSuccess?: () => void }) =>
      createMutation.mutate(data, {
        onSuccess: () => options?.onSuccess?.(),
      }),
    isPending: createMutation.isPending,
  };
}
```

**Naming convention:**

| Operation | Hook Name | Action Returned |
|-----------|-----------|-----------------|
| Submit | `useSubmit{Entity}` | `submit` |
| Schedule | `useSchedule{Entity}` | `schedule` |
| Start | `useStart{Entity}` | `start` |
| Cancel | `useCancel{Entity}` | `cancel` |
| End | `useEnd{Entity}` | `end` |
| Approve | `useApprove{Entity}` | `approve` |
| Reject | `useReject{Entity}` | `reject` |
| Remove | `useRemove{SubEntity}` | `remove` |
| Reorder | `useReorder{SubEntities}` | `reorder` |

---

## Step 5: Generate Blob Mutation Hooks

For file downloads:

```typescript
export function useGenerate{Entity}Blob() {
  const createMutation = useHostServiceBlobMutation();
  const mutation = createMutation<Record<string, unknown>>({Feature}Service.Generate{Entity});

  return {
    generate: (id: number, options?: { onSuccess?: () => void }) =>
      mutation.mutate(
        { pathParams: { id: id.toString() } },
        {
          onSuccess: (blob) => {
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'Document.pdf';
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

---

## File Structure

```
features/{feature-name}/
├── components/
│   └── {Component}/
│       ├── {Component}.tsx
│       └── {Component}.module.css
├── hooks/
│   ├── use{Entity}s.ts            # List query hook
│   ├── use{Entity}.ts             # Detail query hook (with pathParams)
│   ├── useCreate{Entity}.ts       # Create mutation hook
│   ├── useUpdate{Entity}.ts       # Update mutation hook  
│   ├── useDelete{Entity}.ts       # Delete mutation hook
│   ├── use{Verb}{Entity}.ts        # Operation mutation hook (state transition)
│   ├── useRemove{SubEntity}.ts     # Remove sub-entity mutation hook
│   ├── useReorder{SubEntities}.ts  # Reorder mutation hook
│   ├── use{Feature}Logic.ts       # Logic hook (orchestrates everything)
│   └── useCatalogs.ts             # Composite catalog queries
├── types/
│   ├── constants.ts               # Service IDs, enums
│   ├── form.types.ts              # Form value types (optional)
│   └── index.ts                   # Re-exports
├── {Feature}Page.tsx              # Page component
├── {Feature}Page.module.css       # Page styles
└── index.ts                       # Barrel export
```

---

## Service IDs

Defined in `types/constants.ts`:

```typescript
export const {Feature}Service = {
  // CRUD
  Get{Entity}s: 100,
  Get{Entity}ById: 101,
  PostCreate{Entity}: 102,
  PutUpdate{Entity}: 103,
  Delete{Entity}: 104,
  // Operations (state transitions)
  Post{Verb}{Entity}: 110,
  Post{Verb2}{Entity}: 111,
  // Sub-entities
  Get{SubEntity}s: 200,
  PostAdd{SubEntity}: 201,
  PostRemove{SubEntity}: 202,
  PutReorder{SubEntities}: 203,
  // Files
  PostGenerate{Entity}Blob: 300,
} as const;
```

---

## Generation Order

1. **Service IDs first** — in `types/constants.ts`
2. **Types inline with hooks** — Request/Response in same file as hook
3. **Query hooks** — One per GET endpoint
4. **Mutation hooks** — One per POST/PUT/DELETE/Operation endpoint
5. **Logic hook** — Orchestrates queries + mutations + state
6. **Page component** — Renders UI, delegates to logic hook

---

## Checklist

- [ ] Service IDs in `types/constants.ts` as `const { ... } as const`
- [ ] Request types extend `Record<string, unknown>`
- [ ] Response types include full API structure (success, data, errors, pagination, metadata)
- [ ] Query hook uses `useHostServiceQuery()` adapter
- [ ] Mutation hook uses `useHostServiceMutation()` adapter
- [ ] Mutation returns `{ verbAction, isPending }` (verb matches hook name)
- [ ] Operation hooks use verb-based naming (`use{Verb}{Entity}`)
- [ ] Operation hooks return `{ verb, isPending }` matching the action name
- [ ] Remove hooks accept justification in request body
- [ ] Service IDs grouped: CRUD (100s), Operations (110s), Sub-entities (200s), Files (300s)
- [ ] NO query invalidation in mutation hooks (use refetch in logic hook)
- [ ] NO toast in mutation hooks (handle in logic hook)
- [ ] Blob mutation for file downloads uses `useHostServiceBlobMutation()`
- [ ] Types defined inline with hooks (except form types and service IDs)
- [ ] All nullable fields use `string | null` (not optional `string?`)

---

## Related Skills

| Task | Skill |
|------|-------|
| React patterns | `react` |
| Hook patterns | `react-hooks` |
| Host factories | `microfrontend` |
