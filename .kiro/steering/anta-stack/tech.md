---
inclusion: always
---

# ANTA Technology Stack

## Backend

| Technology | Version | Purpose |
|-----------|---------|---------|
| .NET | 8.0 | Minimal API framework |
| Dapper | Latest | Micro-ORM for SP calls (anonymous objects, not DynamicParameters) |
| SQL Server | 2019+ | Database with stored procedures |
| FluentValidation | Latest | Request validation with typed error codes |
| Ocelot | 23.2 | API Gateway routing |

### Backend Patterns
- **Minimal API** with vertical slice modules (not controllers)
- **Stored Procedures** for all data access — no raw SQL in handlers
- **SpResultHelper** for SP error handling (SELECT ErrorCode pattern)
- **ApiResponse\<T\>** wrapper for all responses
- **DictionaryMappingHelper** for dynamic column mapping
- **Happy** library for JWT authentication
- **Lion** library for role-based authorization

### Shared Libraries
- `ANTA.Shared.Common` — Base types, ApiResponse, pagination
- `ANTA.Shared.Common.Validation` — FluentValidation base classes
- `ANTA.Shared.Logging` — Structured logging
- `ANTA.Shared.Auth` — Happy authentication middleware
- `ANTA.Shared.Authorization` — Lion permission middleware
- `ANTA.Shared.Gateway` — Ocelot gateway extensions
- `ANTA.Shared.Swagger` — OpenAPI documentation
- `ANTA.Shared.Resilience` — Retry policies

## Frontend

| Technology | Version | Purpose |
|-----------|---------|---------|
| React | 19 | UI framework |
| TypeScript | 5.x | Type-safe JavaScript |
| Rsbuild | 1.5.x | Build tool (Rspack-based) |
| Module Federation | 0.21.6 | Microfrontend runtime |
| Ant Design | 6.x | UI component library |
| TanStack Query | 5.x | Server state management |
| React Router DOM | 7.x | Client-side routing |
| Ky | 1.x | HTTP client (host only) |
| Zustand | 5.x | Client state management (host only) |
| Zod | 4.x | Runtime schema validation (host only) |

### Host vs Remote Dependencies

| Dependency | Host | Remote | Notes |
|-----------|------|--------|-------|
| React, TypeScript, Ant Design, TanStack Query | ✅ | ✅ | Shared via Module Federation |
| React Router DOM | ✅ | ✅ | Routing in both layers |
| Ky | ✅ | ❌ | HTTP client lives in host; remotes call via shared hooks |
| Zustand | ✅ | ❌ | Global state (session, layout) managed by host |
| Zod | ✅ | ❌ | Auth/config validation in host; remotes use FluentValidation-style |

### Frontend Patterns
- **Microfrontend architecture**: Host app + Child apps via Module Federation
- **Feature folders**: Each feature is self-contained (`types.ts`, `hooks/`, `components/`, `Page.tsx`)
- **Anta\* wrappers**: All Ant Design components wrapped (AntaButton, AntaTable, etc.)
- **CSS Modules**: Scoped styles per component
- **use{Feature}Logic** hooks: Pages only render, logic lives in hooks

## Infrastructure

| Technology | Purpose |
|-----------|---------|
| AWS Cognito | Identity provider (via Happy) |
| Docker | Local development |
| CodeArtifact | Private npm/NuGet registry |
