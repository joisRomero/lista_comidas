---
name: microfrontend
description: >
  Module Federation setup for ANTA: Host exports, Child configuration, adapters.
  Trigger: When setting up microfrontends, creating child apps, or using Host exports.
metadata:
  author: anta
  version: "2.0"
  scope: [root]
  auto_invoke: "microfrontend, Module Federation, host, child, remote, mf-entry"
  phase: [construction]
  layer: [frontend]
  validates_with: validate_react_shared
  validation_profile: build-component
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Host uses `eager: true` for shared deps | ALWAYS | Immediate load |
| Child uses `eager: false` for shared deps | ALWAYS | Deferred load |
| Child exposes only `./App` | ALWAYS | Single entry point |
| Use adapters to consume Host exports | ALWAYS | Abstraction layer |
| Match dependency versions Host ↔ Child | ALWAYS | Avoid conflicts |
| Use `mf-entry.js` as entry file | ALWAYS | Standard naming |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     HOST (Layout)                            │
├─────────────────────────────────────────────────────────────┤
│  Exposes: ./factories, ./hooks, ./toast, ./logger, ./session│
│  Shared: react, react-dom, antd, @tanstack/react-query,     │
│          zustand, react-toastify                            │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │  Child A │  │  Child B │  │  Child C │                   │
│  │  ./App   │  │  ./App   │  │  ./App   │                   │
│  └──────────┘  └──────────┘  └──────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Host Exports

| Export | Functions |
|--------|-----------|
| `./factories` | `createServiceQuery`, `createProcessQuery`, `createServiceMutation`, `createServiceBlobMutation`, `createProcessMutation` |
| `./hooks` | Re-exports factories + `useRemotes`, `useErrorHandler`, `useCurrentOption`, `useConfirm`, `useFileUpload`, `useDownloadFile` |
| `./toast` | `toast.success()`, `toast.error()`, `toast.info()`, `toast.warning()`, `toast.loading()`, `toast.dismiss()` |
| `./logger` | `logger.log()`, `logger.warn()`, `logger.error()`, `logger.info()`, `logger.debug()` |
| `./session` | `useCurrentUser`, `useCurrentProfile`, `useAvailableProfiles`, `useMenu`, `useAuthState`, `getAuthHeaders`, `getCurrentProfile` |

---

## Adapter Pattern

Children MUST use adapters to consume Host exports to maintain a clean abstraction layer.

```typescript
// shared/adapters/useHostApi.ts
export const useHostServiceQuery = () => createServiceQuery;
export const useHostServiceMutation = () => createServiceMutation;
export const useHostServiceBlobMutation = () => createServiceBlobMutation;

// shared/adapters/useHostAuth.ts  
export const useHostAuth = () => {
  const { getProcessById } = useCurrentOption();
  return { getProcessById };
};

// shared/adapters/index.ts
export { useHostServiceQuery, useHostServiceMutation, useHostServiceBlobMutation } from './useHostApi';
export { useHostAuth } from './useHostAuth';
export { toast } from 'host/toast';
export { logger } from 'host/logger';
```

---

## Naming Conventions

| Field | Location | Language | Example |
|-------|----------|----------|---------|
| `name` | `rsbuild.config.ts` | English lowercase | `cases` |
| `name` | `mf-remotes.json` | Spanish (display) | `Casos` |
| `path` | `mf-remotes.json` | English lowercase | `cases` |
| `scope` | `mf-remotes.json` | English lowercase | `cases` |
| Package name | `package.json` | `mf-{module}-remote` | `mf-cases-remote` |

**Rule**: Only `name` in `mf-remotes.json` is Spanish (UI display). Everything else is English lowercase.

---

## Child Setup

### Project Structure

```
Front{Module}/
└── src/{Project}.Front/
    ├── @mf-types/               # ⚠️ AT PROJECT ROOT (same level as src/, package.json)
    │   ├── index.d.ts
    │   └── host/
    │       ├── apis.d.ts
    │       ├── factories.d.ts
    │       ├── hooks.d.ts
    │       ├── logger.d.ts
    │       ├── session.d.ts
    │       ├── stores.d.ts
    │       ├── toast.d.ts
    │       └── compiled-types/  # Full type definitions
    ├── src/
    │   ├── features/
    │   ├── shared/
    │   │   └── adapters/        # Host adapters (REQUIRED)
    │   ├── App.tsx
    │   └── main.tsx
    ├── package.json
    ├── rsbuild.config.ts
    └── tsconfig.json
```

> **CRITICAL**: `@mf-types/` MUST be at the project root (alongside `src/`, `package.json`, `tsconfig.json`), NOT inside `src/`. The `tsconfig.json` path alias `"./@mf-types/host/*"` resolves relative to the project root.

### @mf-types Setup

The `@mf-types/` folder contains type declarations for all Host Module Federation exports. Without it, TypeScript cannot resolve any `host/*` import.

**How to obtain @mf-types:**
1. **Copy from an existing child project** that already has it — recommended for new projects
2. **Auto-generated by Host** when running `npm run dev` with `dts: true` in Host's Module Federation config

```bash
# Copy @mf-types from an existing child project
cp -r ../Front{ExistingModule}/src/{Project}.Front/@mf-types ./@mf-types
```

### Bootstrap (main.tsx)

Children's `main.tsx` is minimal. No providers needed — auth, query client, and theme come from Host.

```typescript
// main.tsx (Child)
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
);
```

### tsconfig.json Paths

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "host/*": ["./@mf-types/host/*"]
    }
  }
}
```

---

## Host vs Child Comparison

| Aspect | Host | Child |
|--------|------|-------|
| `eager` | `true` | `false` |
| `remotes` | `{}` (dynamic) | Points to Host |
| `exposes` | factories, hooks, etc. | Only `./App` |
| `htmlPlugin` | enabled | `false` |
| Port | 64238 | Unique per child (set in `server.port`) |
| Entry File | `mf-entry.js` | `mf-entry.js` |
| Plugin Version | `0.21.6` | `0.21.6` |

> **IMPORTANT**: Each child app MUST configure a unique `server.port` in `rsbuild.config.ts` to avoid port conflicts during development:
> ```typescript
> export default defineConfig({
>   mode,
>   server: {
>     port: 300X  // Unique per child — coordinate with team
>   },
>   // ...
> });
> ```

---

## Shared Dependencies

### Host Shared (eager: true)

| Dependency | Version |
|------------|---------|
| `react` | 19.1.1 |
| `react-dom` | 19.1.1 |
| `react-router-dom` | 7.9.1 |
| `@tanstack/react-query` | 5.89.0 |
| `react-toastify` | 11.0.5 |
| `antd` | 6.0.1 |
| `zustand` | 5.0.8 |

### Child Shared (eager: false)

| Dependency | Version |
|------------|---------|
| `react` | 19.1.1 |
| `react-dom` | 19.1.1 |
| `react-router-dom` | 7.9.1 |
| `antd` | 6.0.1 |
| `@tanstack/react-query` | 5.89.0 |

**Note**: `react-toastify` and `zustand` are NOT declared in children shared (they use host's via `./toast` and `./session` exports).

---

## Host Internal Dependencies

These libraries are used **only inside the Host**. Children access their functionality indirectly through the factories and hooks the Host exports via Module Federation.

### Ky (HTTP Client)

The Host implements API clients using Ky with auth interceptors. Children NEVER import Ky directly — they use `createServiceQuery` / `createServiceMutation` from `host/factories`.

```typescript
// lib/api/client.ts (HOST ONLY)
import ky from 'ky';

export const apiBaseClient = ky.create({
  prefixUrl: import.meta.env.PUBLIC_APP_SERVER_URI_API,
  hooks: {
    beforeRequest: [
      (request) => {
        const token = window.__getAuthToken?.();
        if (token) request.headers.set('Authorization', `Bearer ${token}`);
      },
    ],
    afterResponse: [
      async (request, options, response) => {
        if (response.status === 401) {
          await window.__refreshToken?.();
          return ky(request, options); // Retry with fresh token
        }
      },
    ],
  },
});

export const apiBlobClient = apiBaseClient.extend({
  headers: { Accept: 'application/octet-stream' },
});
```

> **Why Ky over axios**: Smaller bundle, native fetch-based, better TypeScript types, built-in retry/hooks.

### Zustand (Host State)

The Host manages global state (session, menu, profiles) via Zustand stores. Children access this state through `host/session` exports — they never create Zustand stores themselves.

```typescript
// stores/session.store.ts (HOST ONLY)
import { create } from 'zustand';

interface SessionState {
  user: User | null;
  profile: Profile | null;
  menu: MenuItem[];
  setUser: (user: User) => void;
  setProfile: (profile: Profile) => void;
}

export const useSessionStore = create<SessionState>((set) => ({
  user: null,
  profile: null,
  menu: [],
  setUser: (user) => set({ user }),
  setProfile: (profile) => set({ profile }),
}));
```

> **Children consume via**: `useCurrentUser()`, `useCurrentProfile()`, `useMenu()` from `host/session`.

### Zod (Host Validation)

The Host uses Zod for runtime validation of environment config and auth payloads. Children do NOT use Zod — their form validation uses TanStack Query error responses from the backend (FluentValidation).

```typescript
// src/config/env.ts (HOST ONLY)
import { z } from 'zod';

const envSchema = z.object({
  PUBLIC_APP_ENVIRONMENT: z.string().min(1),
  PUBLIC_APP_NAME: z.string().min(1),
  PUBLIC_APP_TITLE: z.string().min(1),
  PUBLIC_APP_SERVER_URI_API: z.string().min(1),
  PUBLIC_APP_SERVER_SERVICE_HAPPY: z.string().url(),
  PUBLIC_APP_COGNITO_DOMAIN: z.string().min(1),
  PUBLIC_APP_CLIENT_ID: z.string().min(1),
});

export const env = envSchema.parse(import.meta.env);

export const isLocal = env.PUBLIC_APP_ENVIRONMENT === 'local';
export const isProd = env.PUBLIC_APP_ENVIRONMENT === 'prd';
```

> **Prefix convention**: Rsbuild exposes env vars with `PUBLIC_` prefix to `import.meta.env`. NEVER use `VITE_` prefix — that's Vite, not Rsbuild.

> **Why host-only**: Zod validates infrastructure config at startup. Children don't need it because their API validation comes from backend FluentValidation errors surfaced through TanStack Query.

---

## Frontend Build Commands

```bash
# Frontend commands (npm-based template)
npm install
npm run dev
npm run build
```

> Use `npm` for frontend operations unless your repository standard defines otherwise.

## Development Workflow

```bash
# 1. Start Host FIRST (required)
cd Front-{Host}/src/{Project}.Front/ && npm run dev

# 2. Start Child (in another terminal)
cd Front-{Module}/src/{Project}.Front && npm run dev
```

| App | Default Port |
|-----|--------------|
| Host (Front-{Host}) | 64238 |
| Front-{Module} | {PORT} |
| Front-{AnotherModule} | {PORT+1} |

> Each child MUST have a unique `server.port` in `rsbuild.config.ts`. Coordinate ports with the team to avoid conflicts.

---

## Production Build

### Chunk Splitting

Both Host and Child use vendor-based chunk splitting for cache optimization:

```typescript
performance: {
  chunkSplit: {
    strategy: 'split-by-experience',  // or 'custom' for Host
    override: {
      cacheGroups: {
        'vendor-react': { test: /node_modules[\\/](react|react-dom|react-router-dom)[\\/]/, priority: 30 },
        'vendor-query': { test: /node_modules[\\/]@tanstack/, priority: 25 },
        vendor: { test: /node_modules/, priority: 10 },
      },
    },
  },
},
```

### Version File

Each MF generates a `version.json` in the dist output for deployment tracking:

```typescript
// shared/utils/generateVersionFile.ts
import { writeFileSync } from 'fs';

export const generateVersionFile = (name: string, version: string) => ({
  name: 'generate-version',
  setup(api: any) {
    api.onAfterBuild(() => {
      writeFileSync('./dist/version.json', JSON.stringify({ name, version, buildDate: new Date().toISOString() }, null, 2));
    });
  },
});
```

Add to plugins: `generateVersionFile('{modulename}', version)`

### Obfuscation

Production builds use `javascript-obfuscator` with `debugProtection: true` and `stringArray` encoding. Full config in `assets/rsbuild-child.ts`. Key settings:

| Setting | Value | Purpose |
|---------|-------|---------|
| `debugProtection` | `true` | Prevents DevTools debugging |
| `debugProtectionInterval` | `4000` | Refreshes protection timer |
| `disableConsoleOutput` | `true` | Strips console.* calls |
| `stringArrayEncoding` | `['base64']` | Encodes string literals |
| `stringArrayWrappersCount` | `200` | Increases decoding complexity |

> Install as devDependency: `javascript-obfuscator: "4.1.1"`

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `Shared module not found` | Version mismatch | Match versions in package.json |
| `Cannot find module 'host/...'` | Host not running OR `@mf-types` missing | Start Host first; verify `@mf-types/` exists at project root |
| `@mf-types/host` empty | Types not generated | Run `npm run dev` in Host first |
| `@mf-types` exists but TS still fails | Folder placed inside `src/` instead of project root | Move `@mf-types/` to project root (alongside `package.json`) |
| Port conflict between children | No `server.port` configured | Add unique `server: { port: XXXX }` to each child's `rsbuild.config.ts` |

---

## Checklist

### Child Setup
- [ ] `package.json` with name `mf-{module}-remote`
- [ ] `rsbuild.config.ts` with `dts: false`, `htmlPlugin: false`, and correct `name`
- [ ] **`rsbuild.config.ts` has `server: { port: XXXX }` with unique port**
- [ ] **`@mf-types/` folder exists at project root** (not inside `src/`)
- [ ] `shared/adapters/` with useHostApi, useHostAuth
- [ ] `tsconfig.json` with `host/*` path pointing to `./@mf-types/host/*`
- [ ] `eager: false` for all shared deps
- [ ] Production build uses obfuscation

### Host Integration
- [ ] Added to `mf-remotes.json`
- [ ] Menu configured in backend
- [ ] Routes match module path

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Child rsbuild.config.ts template | [rsbuild-child.ts](assets/rsbuild-child.ts) |
| Host adapters template | [adapters.ts](assets/adapters.ts) |
| Child package.json template | [package-child.json](assets/package-child.json) |

---

## Related Skills

| Task | Skill |
|------|-------|
| React patterns | `react` |
| React hooks | `react-hooks` |
| Design system | `design-system` |
| TypeScript | `typescript` |

