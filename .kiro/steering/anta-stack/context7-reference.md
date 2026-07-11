---
inclusion: auto
name: context7-reference
description: External library documentation reference. Use when working with any ANTA tech stack library to query up-to-date docs.
---

# External Documentation Reference

When working with external libraries, **ALWAYS query official documentation** for up-to-date patterns. Library APIs change frequently — never assume based on older knowledge.

## Frontend Libraries

| Library | When to Query |
|---------|---------------|
| React 19 | New APIs, hooks behavior, ref patterns |
| Ant Design | Component props, customization, theming |
| TanStack Query | Query options, mutation patterns, caching |
| Zustand | Store patterns, middleware, persist |
| Zod | Schema validation, transforms, refinements |
| Playwright | Selectors, assertions, test patterns |

## Backend Libraries

| Library | When to Query |
|---------|---------------|
| .NET 8 Minimal API | Route groups, TypedResults, endpoint filters |
| Dapper | QueryMultipleAsync, CommandDefinition, type handlers |
| Ocelot | Route config, DelegatingHandlers, middleware hooks |
| FluentValidation | AbstractValidator, RuleFor, WithErrorCode, async rules |

## Why This Matters

- Library APIs change between major versions
- Official docs prevent outdated patterns
- Especially critical for: React 19 ref changes, TanStack Query v5 API, .NET 8 minimal API patterns
