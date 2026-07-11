---
inclusion: always
---

# ANTA Project Structure & Conventions

## Repository Structure

Each ANTA project follows this structure:

```
{ProjectName}/
├── Api{Module}/           # .NET 8 Minimal API
│   ├── Modules/
│   │   └── {Feature}/
│   │       ├── Endpoints/
│   │       │   └── {Action}{Entity}Endpoint.cs
│   │       ├── Handlers/
│   │       │   └── {Action}{Entity}Handler.cs
│   │       ├── Requests/
│   │       │   └── {Action}{Entity}Request.cs
│   │       ├── Responses/
│   │       │   └── {Action}{Entity}Response.cs
│   │       ├── Validators/
│   │       │   └── {Action}{Entity}Validator.cs
│   │       └── {Feature}Module.cs
│   └── Program.cs
├── ApiGateway/            # Ocelot API Gateway
├── Front{Module}/         # React 19 microfrontend
│   └── src/
│       ├── features/
│       │   └── {feature}/
│       │       ├── types.ts
│       │       ├── hooks/
│       │       │   ├── use{Feature}Query.ts
│       │       │   ├── use{Feature}Mutation.ts
│       │       │   └── use{Feature}Logic.ts
│       │       ├── components/
│       │       │   └── {Component}.tsx
│       │       └── {Feature}Page.tsx
│       ├── services/
│       │   └── {feature}Service.ts
│       └── shared/
│           └── components/
├── Database/              # SQL Server scripts
│   └── StoredProcedures/
│       └── {Schema}.{Action}{Entity}.sql
└── docs/
    └── API_CATALOG.md
```

## Code Language Rule

- **All code identifiers MUST be in English**: folder names, file names, component names, function names, variable names, hook names, CSS class names, route paths, and type/interface names.
- **Spanish is allowed ONLY in**: user-facing strings (labels, messages, tooltips), code comments, and documentation files.
- This applies to all layers: Frontend (TS/TSX), Backend (C#), Database (SQL identifiers).

## Naming Conventions

| Language | Convention |
|----------|-----------|
| C# | PascalCase for public, _camelCase for private fields |
| TypeScript | camelCase for variables/functions, PascalCase for types/components |
| SQL | UPPER_CASE for keywords, `{Schema}.{Action}{Entity}` for SPs |
| Files (C#) | PascalCase: `GetContractHandler.cs` |
| Files (TS) | PascalCase for components: `ContractList.tsx`, camelCase for hooks: `useContractQuery.ts` |
| CSS Modules | `{Component}.module.css` |

## Code Quality Rules

- **No `any`** in TypeScript — use proper types
- **No `SELECT *`** in SQL — list all columns explicitly
- **No magic strings** — use constants or enums
- **Always handle errors explicitly** — no empty catch blocks
- **No `as any`**, `@ts-ignore`, or `@ts-expect-error` — fix the types
- **No raw Ant Design imports** — use Anta* wrappers

## SP Naming Pattern

```
{Schema}.{Action}{Entity}
```

Actions: `List`, `Get`, `Create`, `Update`, `Delete`

Examples:
- `Employees.ListEmployees`
- `Bookings.GetBooking`
- `Bookings.CreateBooking`

## Commands

```bash
# Backend
dotnet build
dotnet run

# Frontend
pnpm install
pnpm dev
pnpm build
```
