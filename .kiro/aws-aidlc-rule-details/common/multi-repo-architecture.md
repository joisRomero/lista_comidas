# Multi-Repo Architecture

**Purpose**: Define the multi-repo architecture model used when a project spans multiple repositories.

## Core Principle

In a multi-repo architecture, the project is decomposed into specialized repositories with distinct roles. The AI-DLC process is orchestrated from a central hub, while implementation is distributed across code repositories using self-contained guides.

## Repository Roles

- **Documentation Hub Repository**: The central repository where the AI-DLC process runs (Inception, Operations, Closure, Change Management). It contains all specifications, plans, QA matrices, and E2E tests. This is the primary workspace for the AI agent during planning and testing phases.
- **Gateway Repository**: The API gateway or routing layer that manages traffic and cross-cutting concerns. This repository is always present in multi-repo setups.
- **Core API Repository**: Contains shared or cross-cutting backend services, modules, and database schemas. This repository is always present.
- **Domain API Repository**: Contains domain-specific backend services with their own modules and database schemas. These are present only in microservice architectures and there can be multiple domain repositories.
- **Frontend Host Repository**: The main frontend application containing the layout, routing, and shared components. Present in web projects.
- **Frontend Domain Repository**: Micro-frontend child applications. These are present only in micro-frontend architectures and there can be multiple domain repositories.
- **Mobile Repository**: The mobile application codebase. Present in mobile projects.

## Architecture Combinations

| Combo | Description | Repos Involved |
|-------|-------------|----------------|
| Monolith Web | Single backend + single frontend | Doc Hub, Gateway, Core API, Frontend Host |
| Monolith Mobile | Single backend + mobile | Doc Hub, Gateway, Core API, Mobile |
| Monolith Web+Mobile | Single backend + web + mobile | Doc Hub, Gateway, Core API, Frontend Host, Mobile |
| Micro Web | Microservices + micro-frontends | Doc Hub, Gateway, Core API, Domain APIs, Frontend Host, Frontend Domains |
| Micro Mobile | Microservices + mobile | Doc Hub, Gateway, Core API, Domain APIs, Mobile |
| Micro Web+Mobile | Microservices + micro-frontends + mobile | All repo types |

## Workflow with Multi-Repo

1. **Inception**: Runs entirely in the **Documentation Hub Repository**. All planning, requirements, and architectural decisions are centralized here.
2. **Construction**:
   - API contracts are designed in the Doc Hub.
   - Self-contained **HU Guides** are generated per repository based on the API contracts and user stories.
   - HU Guides are manually copied from the Doc Hub to the target code repositories.
   - Development occurs in each code repository following its specific HU Guide.
   - Developers confirm completion of HUs in the code repositories before returning to the Doc Hub.
3. **Build & Test (E2E)**: Runs from the **Documentation Hub Repository** after all code repositories have completed their assigned HUs.
4. **Operations**: Orchestrated from the **Documentation Hub Repository**.
5. **Closure**: Finalized in the **Documentation Hub Repository**.

## Distribution Model

- **Manual Copying**: HU Guides are generated in the Documentation Hub and then manually copied to the target code repositories.
- **Compatibility**: No symlinks or shell scripts are used for distribution to ensure full Windows compatibility.
- **Verification**: Developers provide verbal or written confirmation of HU completion when returning to the Documentation Hub to trigger the next stage.

## Early Detection

Repository structure (single-repo vs multi-repo) is now captured **during Requirements Analysis** (Step 5b in `inception/requirements-analysis.md`) rather than being detected later in the workflow. When the user identifies a multi-repo architecture, they provide a Repository Structure table with columns [ID | Name | Role]. This table is recorded as a **HARD CONSTRAINT** in the requirements document, ensuring all downstream stages — Workflow Planning, QA Matrix, HU Guide Generation, and Build & Test — operate with a consistent, user-confirmed repository map from the start.

## HU-Repo Distribution

During Workflow Planning (Step 5b in `inception/workflow-planning.md`), an **HU-Repo Distribution Map** is generated for multi-repo projects. This map assigns each User Story (HU) to the specific repositories it impacts, based on the repository structure captured in Requirements Analysis.

- **Artifact**: `aidlc-docs/inception/plans/hu-repo-distribution.md`
- **Consumers**:
  - **QA Matrix** (`inception/qa-matrix.md`): Uses the Repo column in the Traceability Table and Repos Involved in the E2E Flow Index
  - **HU Guide Generation** (`construction/hu-guide-template.md`): Loads the distribution map to determine which guides to generate per repository
  - **Build & Test** (`construction/build-and-test.md`): Uses the map for Repo Completion Tracking before launching E2E tests

## Database Location

Database schemas and migrations live **inside each API repository** (Core API or Domain API) that owns the data. There is no separate database-only repository; data ownership follows the service boundaries.
