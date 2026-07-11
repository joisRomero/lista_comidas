---
inclusion: always
---

# ANTA Software Factory — Product Overview

## What is ANTA?

ANTA is an internal software factory that builds enterprise applications for Antamina (mining company). All projects share the same tech stack, patterns, and conventions documented in Atlas skills.

## Target Users

- Internal business units (Operations, Finance, HR, Legal, Contracts)
- Enterprise users accessing via corporate intranet
- Authenticated via AWS Cognito through the Happy library

## Key Business Domains

Projects span multiple business domains including:
- Contract management and committee workflows
- Session management and voting systems
- Document and case management
- Approval workflows

## Architecture Philosophy

- **Microfrontend architecture**: Independent deployable frontends per domain
- **Vertical slice backend**: One module per business domain with its own endpoints, handlers, and stored procedures
- **Database-driven**: SQL Server stored procedures are the single source of truth for business logic
- **API Gateway**: Ocelot-based gateway with Happy authentication

## Quality Standards

- Type safety everywhere (no `any` in TypeScript, typed responses in C#)
- Every pattern is documented as a skill in Atlas
- Code must follow established conventions — skills are the source of truth
