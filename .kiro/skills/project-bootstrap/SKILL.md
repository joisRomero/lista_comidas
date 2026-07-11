---
name: project-bootstrap
description: >
  Entry point for onboarding to an ANTA project.
  Trigger: When starting work on a new project, first time setup, or project orientation.
metadata:
  author: anta
  version: "1.0"
  scope: [root]
  auto_invoke: "new project, first time, getting started, project setup, onboarding"
  phase: [inception]
  layer: null
  validates_with: null
  validation_profile: null
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Complete ALL steps in order | ALWAYS | Each step depends on previous |
| Don't skip project-context | NEVER | Foundation for all work |
| Verify Docker before coding | ALWAYS | Need running services |

---

## Bootstrap Checklist

### Phase 1: Orientation (Read-Only)

```
□ Step 1: Read project-context
  └─ Location: .claude/project-context/SKILL.md (EDIT THIS FILE IN PLACE)
  └─ Symlinked to .codex/ and .gemini/ automatically
  └─ If has <!-- Fill: --> placeholders → Go to Phase 2

□ Step 2: Read API_CATALOG.md
  └─ Location: docs/API_CATALOG.md
  └─ If missing → Generate with `api-catalog` skill after Phase 2

□ Step 3: Understand structure
  └─ Backend: src/{Project}.Api/
  └─ Frontend: Front{Module}/src/{Project}.Front/
  └─ Database: database/{Schema}/
```

### Phase 2: Setup (If Needed)

```
□ Step 4: Fill project-context (if has placeholders)
  └─ EDIT IN PLACE: .claude/project-context/SKILL.md
  └─ DO NOT create new file, fill the existing template
  └─ Replace all <!-- Fill: --> comments with actual values
  └─ Sections to fill:
     • Project name, purpose
     • Tech stack versions
     • Module list with ports
     • Schema list
     • Key conventions

□ Step 5: Configure DB MCP (if missing)
  └─ Check: opencode.json in project root
  └─ If missing, create with SQL Server config (see assets/mcp-config.md)
  └─ Get DSN from appsettings.json or docker-compose.yml
  └─ Enables: Direct SP exploration via MCP

□ Step 6: Generate API Catalog (if missing)
  └─ Use: `api-catalog` skill
  └─ Output: docs/API_CATALOG.md
```

### Phase 3: Environment

```
□ Step 7: Start Docker services
  └─ Command: docker compose up -d
  └─ Verify: docker compose ps (all healthy)
  └─ Use `docker-local` skill if issues

□ Step 8: Verify connectivity
  └─ Backend: curl http://localhost:{port}/health
  └─ Database: SQL Server connection test
  └─ Frontend: npm run dev → http://localhost:5173
```

---

## Quick Commands

```bash
# Check if Docker running
docker compose ps

# Start all services
docker compose up -d

# View logs if issues
docker compose logs -f {service}

# Backend health check
curl http://localhost:5000/health

# Frontend dev server
cd Front{Module}/src/{Project}.Front && npm run dev
```

---

## Project Structure Map

```
{ProjectRoot}/
├── .claude/
│   ├── project-context/
│   │   └── SKILL.md          ← FILL THIS (shared via symlinks)
│   └── skills/               ← Atlas skills (symlinked)
├── docs/
│   └── API_CATALOG.md        ← Service inventory
├── src/
│   └── {Project}.Api/        ← Backend
│       ├── Program.cs
│       └── Modules/
│           └── {Module}/
│               ├── {Module}Module.cs
│               └── Features/
├── Front{Module}/
│   └── src/{Project}.Front/  ← Frontend
│       ├── src/
│       │   ├── api/          ← Generated types/hooks
│       │   ├── components/
│       │   └── pages/
│       └── package.json
├── database/
│   └── {Schema}/
│       ├── Tables/
│       └── StoredProcedures/
└── docker-compose.yml
```

---

## Common First Tasks

| Task | Skills to Load |
|------|----------------|
| Add new feature | `api-first-spec` → `agent-fullstack` |
| Fix backend bug | `dotnet-handler`, `database-sp` |
| Fix frontend bug | `react`, `react-hooks` |
| Add new endpoint | `dotnet-api`, `dotnet-integration` |
| Add new SP | `database-sp` |
| Write tests | `playwright`, `api-first-testing` |

---

## Troubleshooting

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| "Connection refused" | Docker not running | `docker compose up -d` |
| "SP not found" | Missing migration | Run DB scripts |
| "CORS error" | Gateway misconfigured | Check `dotnet-gateway` |
| "Module not found" | Dependencies missing | `npm install` |
| "Port in use" | Conflicting service | `docker compose down` first |

---

## Checklist

When starting on new ANTA project:
- [ ] Located `.claude/project-context/SKILL.md`
- [ ] Filled all `<!-- Fill: -->` placeholders (edit in place)
- [ ] Understand module structure
- [ ] Docker services running
- [ ] Can hit health endpoint
- [ ] Know which schema(s) I'm working with
- [ ] API Catalog available (or generated)

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| MCP configuration template | [mcp-config.md](assets/mcp-config.md) |

## Related Skills

| Task | Skill |
|------|-------|
| Project architecture | `anta-architecture` |
| Docker setup | `docker-local` |
| API documentation | `api-catalog` |
| Feature workflow | `api-first-spec` |
