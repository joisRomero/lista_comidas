---
name: react
description: >
  React 19 architecture for ANTA projects: feature folders, types, components, UI patterns.
  Trigger: When creating React features, components, or project structure.
metadata:
  author: anta
  version: "2.0"
  scope: [root]
  auto_invoke: "React, componente, feature, TypeScript frontend"
  phase: [construction]
  layer: [frontend]
  validates_with: validate_react_feature
  validation_profile: build-component
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Use feature folders structure | ALWAYS | Self-contained modules |
| Prefix wrappers with `Anta` | ALWAYS | Distinguish from Ant Design |
| Use CSS Modules for styles | ALWAYS | Scoped styles |
| Extract logic to `use{Feature}Logic` hook | ALWAYS | Pages only render |
| Use barrel exports (index.ts) | ALWAYS | Clean imports |
| Each component folder MUST have its own `index.ts` | ALWAYS | TypeScript module resolution requires it when barrel imports from folder path |
| Use `any` type | NEVER | Type safety |

---

## Project Structure

```
src/
├── features/
│   └── {feature-name}/
│       ├── components/
│       │   └── {Component}/
│       │       ├── {Component}.tsx
│       │       └── {Component}.module.css
│       ├── hooks/
│       │   ├── use{Entity}.ts          # Query hook
│       │   ├── use{Action}{Entity}.ts   # Mutation hook
│       │   └── use{Feature}Logic.ts     # Logic hook
│       ├── types/
│       │   ├── constants.ts            # Service IDs, enums
│       │   ├── form.types.ts           # Form value types
│       │   └── index.ts               # Re-exports
│       ├── {Feature}Page.tsx           # Page (DIRECTLY in feature root)
│       ├── {Feature}Page.module.css    # Page styles
│       └── index.ts                   # Barrel export
├── shared/
│   ├── adapters/                      # Host integration (useHostApi, useHostAuth)
│   ├── components/                    # Anta* wrappers
│   │   ├── {AntaComponent}/
│   │   │   ├── {AntaComponent}.tsx
│   │   │   ├── {AntaComponent}.module.css
│   │   │   └── index.ts              # Barrel: export component + types
│   │   └── index.ts                  # Root barrel: re-exports all components
│   ├── hooks/                         # Shared hooks
│   ├── types/                         # Shared types (member.types.ts, provider.types.ts)
│   └── utils/                         # Formatters, service-ids, constants
├── App.tsx                            # Routes only
├── App.css
├── main.tsx                           # Minimal bootstrap
└── env.d.ts                           # Module declarations
```

---

## Pages Pattern

Pages are simple — render header + delegate to main component:

```typescript
const CasesPage = () => {
  const navigate = useNavigate();
  const currentProfile = useCurrentProfile();
  
  return (
    <div className={styles.card}>
      <div className={styles.cardHeader}>
        <div className={styles.cardTitle}>
          <FileTextOutlined className={styles.cardIcon} />
          <AntaTypography.Title level={4}>Lista de Casos</AntaTypography.Title>
        </div>
        {isAllowed && <AntaButton type="primary" onClick={...}>Crear</AntaButton>}
      </div>
      <MainTable />
    </div>
  );
};
CasesPage.displayName = 'CasesPage';
```

---

## Anta* Wrapper Pattern

ALL wrappers use `forwardRef` and set `displayName`. Most input wrappers default to `size="large"`.

```typescript
import { forwardRef } from 'react';
import { Button } from 'antd';
import type { ButtonProps } from 'antd';
import styles from './AntaButton.module.css';

export interface AntaButtonProps extends ButtonProps {}

export const AntaButton = forwardRef<HTMLButtonElement, AntaButtonProps>(
  ({ className, size = 'large', ...props }, ref) => (
    <Button
      ref={ref}
      size={size}
      className={`${styles.button} ${className ?? ''}`}
      {...props}
    />
  )
);
AntaButton.displayName = 'AntaButton';
```

### Component Barrel Files (MANDATORY)

Every component folder in `shared/components/` MUST have its own `index.ts` barrel file.
Without it, `export * from './AntaComponent'` in the root barrel won't resolve.

```typescript
// shared/components/{AntaComponent}/index.ts (standard component)
export { AntaButton } from './AntaButton';
export type { AntaButtonProps } from './AntaButton';
```

```typescript
// shared/components/AntaForm/index.ts (component with extras)
export { AntaForm, AntaFormItem, useAntaForm, useAntaFormWatch } from './AntaForm';
export type { AntaFormProps, AntaFormItemProps, AntaFormInstance } from './AntaForm';
```

```typescript
// shared/components/AntaTypography/index.ts (namespace component)
export { AntaTypography } from './AntaTypography';
```

```typescript
// shared/components/index.ts (root barrel — re-exports all)
export * from './AntaButton';
export * from './AntaInput';
export * from './AntaSelect';
// ... one line per Anta* component
```

### Key Wrapper Details
- **AntaInput**: Includes TextArea, Password, Search variants via `Object.assign`.
- **AntaSelect**: Exposes `Select.Option`.
- **AntaForm**: Exports `useAntaForm` (= `Form.useForm`) and `useAntaFormWatch` (= `Form.useWatch`).
- **AntaTypography**: A namespace: `{ Title, Text, Paragraph, Link }`.

---

## Routing Pattern (react-router-dom 7.x)

`App.tsx` contains ONLY routes. Wrapped in `<section>`. Set `displayName`:

```typescript
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { FeaturePage } from './features/{feature}';
import { DetailPage } from './features/{feature-detail}';
import './App.css';

const App: React.FC = () => {
  return (
    <section>
      <Routes>
        <Route index element={<FeaturePage />} />
        <Route path="detail" element={<DetailPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </section>
  );
};

App.displayName = 'App';
export default App;
```

> Use `index` for the default route. Use `<Navigate replace />` or `<h1>Página no encontrada</h1>` for 404 fallback.

### Extracted Routes (3+ routes)

For apps with many routes, extract to `routes.tsx`:

```typescript
// routes.tsx
import { Route } from 'react-router-dom';
import { ClinicsPage } from '@/features/clinics';
import { ConfigurationPage } from '@/features/configuration';
import { ContactsPage } from '@/features/contacts';

export const appRoutes = (
  <>
    <Route index element={<ClinicsPage />} />
    <Route path="configurations" element={<ConfigurationPage />} />
    <Route path="contacts" element={<ContactsPage />} />
  </>
);

// App.tsx
import { appRoutes } from '@/routes';

const App: React.FC = () => (
  <section>
    <Routes>
      {appRoutes}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  </section>
);
```

### MFE Routing Rules

| Rule | Rationale |
|------|-----------|
| NO `basename` in BrowserRouter | Host handles routing context |
| NO `React.lazy` for route components | Bundle is already small per remote |
| NO `useParams` for entity IDs | Use `location.state` instead (see below) |
| All routes flat or single-level nesting | Keep routing simple in remotes |

---

## State Passing Between Routes

Uses `location.state` for passing data between pages (NOT URL params):

```typescript
// Navigate forward with state
navigate('detail', { state: { id: record.generalDataId } });

// Navigate back
navigate(-1);

// Receive state in target page
const location = useLocation();
const { id } = (location.state as { id: number } | null) ?? {};
```

> **Why state over URL params**: In MFE architecture, URL params can conflict with host routing. State is private to the child app and doesn't affect the URL.

---

## Role-based Rendering

Uses `useCurrentProfile()` from host/session to handle permissions:

```typescript
const currentProfile = useCurrentProfile();
const isSupplyProfile = currentProfile?.Key === 'SUPPLY';
const isSecretariatProfile = currentProfile?.Key === 'SECRETARIAT';

{isSupplyProfile && <AntaButton>Action</AntaButton>}
```

---

## Service IDs Pattern

Service IDs are numeric identifiers that map to backend endpoints via the Host's service registry. Stored in `types/constants.ts`:

```typescript
export const FeatureService = {
  GetFeature: 85004,
  UpdateFeature: 85005,
} as const;
```

> Each service ID is a unique number assigned by the backend team. The Host resolves these IDs to actual API URLs at runtime.

---

## Enums for Catalogs and Statuses

```typescript
export enum AGENDA_STATUS { DRAFT = 'DRAFT', SCHEDULED = 'SCHEDULED' }
export enum CASE_TABS { GENERAL = 'general', PROVIDERS = 'providers' }
export enum CATALOG { CASE_TYPES = 'CASE_TYPES' }
```

---

## Standard Confirmations

Use `useConfirm()` from host/hooks:

```typescript
const confirm = useConfirm();
confirm({
  title: 'Confirmar eliminacion',
  content: '¿Estas seguro?',
  okText: 'Eliminar',
  okButtonProps: { danger: true },
  cancelText: 'Cancelar',
  centered: true,
  onOk: () => { /* action */ },
});
```

---

## Checklist

### Structure
- [ ] Feature in `features/{feature-name}/`
- [ ] Pages in feature root (NOT in components subfolder)
- [ ] Components in `components/{Component}/` with `index.ts`
- [ ] **Each component folder has `index.ts`** exporting component + types
- [ ] **Root `shared/components/index.ts`** re-exports all component folders
- [ ] Hooks in `hooks/use{Action}.ts`
- [ ] Service IDs and Enums in `types/constants.ts`
- [ ] Barrel exports in `index.ts`

### Components
- [ ] Anta* prefix for Ant Design wrappers
- [ ] All Anta* wrappers use `forwardRef` + `displayName`
- [ ] Default `size="large"` for input wrappers
- [ ] CSS Modules for styles
- [ ] Props extending original component
- [ ] `className` prop supported
- [ ] Pages without logic (render only)
- [ ] `displayName` set for ALL exported components

### Types
- [ ] Request interface with proper params
- [ ] Response interface with full API structure
- [ ] Service IDs as const object
- [ ] Enums for statuses and catalogs

### Routing
- [ ] State passing via `navigate('path', { state: {...} })`
- [ ] `App.tsx` contains only routes

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Common types (ResponseApi, MasterTable, Status) | [types.ts](assets/types.ts) |
| Component patterns (Anta*, Modal, Confirm) | [patterns.tsx](assets/patterns.tsx) |

## Related Skills

- **Hook Patterns**: `react-hooks`
- **Microfrontend**: `microfrontend`
- **Design System**: `design-system`
