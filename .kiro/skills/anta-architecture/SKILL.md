---
name: anta-architecture
description: >
  ANTA project architecture blueprint: repo structure, API patterns, modules, frontend microfrontends.
  Trigger: When creating new projects, scaffolding APIs, or understanding system architecture.
metadata:
  author: anta
  version: "1.2"
  scope: [root]
  auto_invoke: "new project, scaffold, architecture, repo structure, API structure, microfrontend"
  phase: [inception]
  layer: null
  validates_with: null
  validation_profile: null
---

## Architecture Overview

### Backend

| Pattern | Description |
|---------|-------------|
| **Modular Monolith** | Separate APIs per domain |
| **Vertical Slice** | Each feature is self-contained |
| **Minimal APIs** | .NET 8 minimal API style |
| **Dapper + SP** | No Entity Framework |

### Frontend

| Pattern | Description |
|---------|-------------|
| **Microfrontends** | Module Federation (Host + Children) |
| **Feature-based** | Each feature is self-contained |
| **Server State** | TanStack Query for API data |
| **Client State** | Zustand for UI state |

### Principles

- Each API = own repository
- Each API = one or more DB schemas
- Business logic in Stored Procedures
- Shared Libraries via NuGet (CodeArtifact)
- POST/PUT return complete object (not just ID)
- 1 SP per feature
- DB Standard v2.3 for naming
- Host provides shared dependencies (React, Ant Design, factories)
- Children are independent deployable units

---

## Stack

### Backend

| Component | Technology |
|-----------|------------|
| Framework | .NET 8 |
| API Style | Minimal APIs |
| Architecture | Vertical Slice |
| ORM | Dapper |
| DB Logic | Stored Procedures (SQL Server) |
| Auth | AWS Cognito + Happy |
| Storage | AWS S3 |
| Private NuGet | AWS CodeArtifact |

### Frontend

| Component | Technology |
|-----------|------------|
| Framework | React 19 |
| Language | TypeScript 5.x |
| Build Tool | Rsbuild |
| Microfrontends | Module Federation |
| UI Library | Ant Design |
| Server State | TanStack Query 5 |
| Client State | Zustand |
| Routing | React Router 7 |
| Forms | Ant Design Form |

---

## Naming Conventions

### Files & Classes

| Element | Convention | Example |
|---------|------------|---------|
| Feature folder | PascalCase, verb + noun | `Create{Entity}`, `List{Entity}` |
| Request DTO | `{Action}{Entity}Request` | `Create{Entity}Request` |
| Response wrapper | `{Action}{Entity}Response` | `Create{Entity}Response` |
| Response item | `{Action}{Entity}Item` | `Create{Entity}Item` |
| Handler | `{Action}{Entity}Handler` | `Create{Entity}Handler` |
| Endpoint | `{Action}{Entity}Endpoint` | `Create{Entity}Endpoint` |

### SP Naming

| Operation | Main Entity | Sub-entity |
|-----------|-------------|------------|
| Create | `Create{Entity}` | `Add{SubEntity}` |
| Delete | `Delete{Entity}` | `Delete{SubEntity}` |
| List | `List{Entity}` | `List{SubEntity}` |

### URL Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Path segments | `kebab-case` | `/api/v1/team-members` |
| Route parameters | `camelCase` | `/{entityId}` |
| Query parameters | `camelCase` | `?statusId=1` |

---

## API Gateway

### Ocelot Routes

| Upstream (Gateway) | Downstream (API) | Port |
|-------------------|------------------|------|
| `/{Module}/api/v1/*` | `/api/v1/*` | 34XX |

### Gateway Features

- Happy authentication (code + header)
- HeaderToken generation
- Correlation ID
- Exception handling
- Health checks
- Swagger aggregation

---

## Response Patterns

| Endpoint Type | Data Structure |
|---------------|----------------|
| GET detail | `data: { item: {...} }` |
| GET list | `data: { items: [...] }` + `pagination` |
| POST create | `data: { item: {...} }` |
| PUT update | `data: { item: {...} }` |
| DELETE | `data: { {entity}Id: int }` |

---

## Placeholders Reference

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{ProjectName}` | Name of the project | `Procurement`, `Inventory` |
| `{Module}` | Module name (PascalCase) | `Orders`, `Products` |
| `{Schema}` | DB schema name | `Orders`, `Products` |
| `{Entity}` | Main entity name | `Order`, `Product` |
| `{SubEntity}` | Child entity name | `OrderItem`, `ProductImage` |
| `{Action}` | CRUD action | `List`, `Get`, `Create`, `Update`, `Delete` |
| `{Feature}` | Frontend feature name | `Orders`, `Products` |
| `{modulename}` | Module name lowercase | `orders`, `products` |

---

## Detailed Documentation

For detailed templates and code examples, see:

| Topic | Asset |
|-------|-------|
| Backend structure, modules, Program.cs | [backend-structure.md](assets/backend-structure.md) |
| Frontend structure, Host/Child, rsbuild | [frontend-structure.md](assets/frontend-structure.md) |
| Service boundaries, schema ownership | [service-boundaries.md](assets/service-boundaries.md) |
| New project checklists | [checklists.md](assets/checklists.md) |

---

## Related Skills

| Task | Skill |
|------|-------|
| Program.cs patterns | `dotnet-startup` |
| Endpoint patterns | `dotnet-api` |
| Handler patterns | `dotnet-handler` |
| SP to API bridge | `dotnet-integration` |
| SP patterns | `database-sp` |
| Gateway patterns | `dotnet-gateway` |
| React patterns | `react` |
| React hooks | `react-hooks` |
| Microfrontend setup | `microfrontend` |
| Design system | `design-system` |
| TypeScript patterns | `typescript` |
