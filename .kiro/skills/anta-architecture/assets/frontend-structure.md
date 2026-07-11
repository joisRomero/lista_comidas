# Frontend Structure

## Repository Structure

### Shared Libraries (npm - Internal Registry)

```
repo: CommonFront/
├── packages/
│   └── common-front/            → @anta/common-front
│       ├── src/
│       │   ├── components/      # Shared UI components
│       │   ├── hooks/           # Shared hooks
│       │   ├── utils/           # Utilities
│       │   └── index.ts
│       └── package.json
└── README.md
```

### Frontend Repositories

```
repo: FrontLayout/               → Host (port 3000) - provides shared deps
repo: Front{Module}/             → Child microfrontend

All with same internal structure:
└── src/{ProjectName}.Front/
    └── package.json
```

**Important:** All repos use same project structure for standardized deploy.

---

## Host Structure (FrontLayout)

```
FrontLayout/
└── src/{ProjectName}.Layout/
    ├── src/
    │   ├── app/
    │   │   ├── providers/           # Context providers
    │   │   ├── routes/              # Route definitions
    │   │   └── App.tsx
    │   ├── lib/
    │   │   ├── api/
    │   │   │   └── factories/       # createServiceQuery, createServiceMutation
    │   │   ├── exports/             # Exported hooks for children
    │   │   ├── logger/              # Logger utility
    │   │   ├── notifications/       # Toast system
    │   │   └── session/             # Auth/session management
    │   ├── shared/
    │   │   ├── components/          # Shared components (Anta* wrappers)
    │   │   └── hooks/               # Shared hooks
    │   ├── main.tsx
    │   └── index.css
    ├── mf-remotes.json              # Remote children config
    ├── rsbuild.config.ts
    ├── package.json
    └── tsconfig.json
```

### Host Exposes

| Export | Description |
|--------|-------------|
| `./factories` | `createServiceQuery`, `createServiceMutation`, `createServiceBlobMutation` |
| `./hooks` | `useCurrentOption`, `useErrorHandler`, `useConfirm`, `useFileUpload` |
| `./toast` | Toast notifications |
| `./logger` | Logging utility |
| `./session` | `useCurrentUser`, `useCurrentProfile`, `getAuthHeaders` |

---

## Child Structure (Front{Module})

```
Front{Module}/
└── src/{ProjectName}.Front/
    ├── @mf-types/host/              # Auto-generated Host types
    ├── src/
    │   ├── features/
    │   │   └── {Feature}/
    │   │       ├── components/
    │   │       ├── hooks/
    │   │       ├── types/
    │   │       └── index.ts
    │   ├── shared/
    │   │   ├── adapters/            # Host integration adapters
    │   │   │   ├── useHostApi.ts
    │   │   │   ├── useHostAuth.ts
    │   │   │   └── index.ts
    │   │   ├── components/
    │   │   └── hooks/
    │   ├── App.tsx
    │   └── main.tsx
    ├── rsbuild.config.ts
    ├── package.json
    └── tsconfig.json
```

---

## Feature Structure

Each feature is self-contained:

```
features/{Feature}/
├── components/
│   ├── {Feature}List.tsx           # List view component
│   ├── {Feature}Detail.tsx         # Detail view component
│   ├── {Feature}Form.tsx           # Form component
│   └── {Feature}Filters.tsx        # Filter component
├── hooks/
│   ├── use{Feature}Query.ts        # Query hook
│   ├── use{Feature}Mutation.ts     # Mutation hook
│   └── use{Feature}Store.ts        # Zustand store (if needed)
├── types/
│   └── {feature}.types.ts          # TypeScript types
└── index.ts                        # Public exports
```

---

## rsbuild.config.ts Template (Child)

```typescript
import { defineConfig } from '@rsbuild/core';
import { pluginReact } from '@rsbuild/plugin-react';
import { pluginModuleFederation } from '@module-federation/rsbuild-plugin';
import { dependencies as deps } from './package.json';

const hostUrl = process.env.HOST_URL || 'http://localhost:3000';

export default defineConfig({
  plugins: [
    pluginReact(),
    pluginModuleFederation({
      name: '{modulename}',           // lowercase, no spaces
      filename: 'mf-entry.js',
      exposes: {
        './App': './src/App',         // Only expose App
      },
      remotes: {
        host: `host@${hostUrl}/mf-entry.js`,
      },
      shared: {
        react: { singleton: true, eager: false, requiredVersion: deps.react },
        'react-dom': { singleton: true, eager: false, requiredVersion: deps['react-dom'] },
        'react-router-dom': { singleton: true, eager: false, requiredVersion: deps['react-router-dom'] },
        antd: { singleton: true, eager: false, requiredVersion: deps.antd },
        '@tanstack/react-query': { singleton: true, eager: false },
      },
    }),
  ],
  tools: {
    htmlPlugin: false,  // Child doesn't generate HTML
  },
});
```

---

## Host vs Child Comparison

| Aspect | Host | Child |
|--------|------|-------|
| `eager` | `true` | `false` |
| `remotes` | `{}` (dynamic) | Points to Host |
| `exposes` | factories, hooks, etc. | Only `./App` |
| `htmlPlugin` | enabled | `false` |
| Port | 3000 | 300X |
