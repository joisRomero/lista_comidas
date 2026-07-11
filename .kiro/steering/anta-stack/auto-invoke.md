---
inclusion: always
---

# Skill Auto-Invoke

**Primary mechanism**: The **Skill Resolver** (`common/skill-resolver.md`) loads skills automatically per stage and per layer. This file is a **safety net** for file writes.

## Rule

**NEVER write a file without loading its matching skill first.**

## File Extension → Skill (Quick Reference)

| File Pattern | Skills |
|-------------|--------|
| `*.sql` | `database-sp` + `database` + `database-modeling` + `database-audit` + `database-security` |
| `*Endpoint.cs` | `dotnet-api` |
| `*Handler.cs` | `dotnet-handler` |
| `*Validator.cs` | `dotnet-integration` |
| `Program.cs` / `*Module.cs` | `dotnet-startup` |
| `*Gateway*` / `configuration.json` | `dotnet-gateway` |
| `*.tsx` / `*.ts` (features/) | `react` |
| `use*Query.ts` / `use*Mutation.ts` | `react-hooks` |
| `rsbuild.config.ts` | `microfrontend` |
| `*.module.css` | `design-system` |
| `Dockerfile*` / `docker-compose*` | `docker-local` |
| `openapi.yaml` | `api-first-spec` |
| `*.spec.ts` / `*.e2e.ts` | `playwright` + `api-first-testing` |

## Full Mapping

See `skills/SKILLS-MANIFEST.md` for:
- Complete skill inventory (45 skills)
- Stage → Skills Map (which skills load for each DLC stage)
- Construction per-layer profiles (BD, Backend, Frontend)
- Cross-cutting conditional injection rules

## Load Protocol

1. Read the skill's `SKILL.md` from `config/skills/{skill-id}/SKILL.md`
2. For fullstack scaffolding, consult `SKILLS-MANIFEST.md` for per-layer skill profiles
3. Load ALL required skills BEFORE starting to write — not one at a time
