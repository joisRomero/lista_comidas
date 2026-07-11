---
name: pull-request
description: >
  Creates Pull Requests following conventions.
  Trigger: When creating PRs (PR template, title conventions, changelog).
metadata:
  author: anta
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Create a PR with gh pr create"
    - "Review PR requirements"
    - "Fill PR template"
  phase: [construction]
  layer: null
  validates_with: null
  validation_profile: null
---

## PR Creation Process

1. **Analyze changes**: `git diff main...HEAD` to understand ALL commits
2. **Determine affected components**: Backend, Frontend, Database
3. **Fill template sections** based on changes
4. **Create PR** with `gh pr create`

## PR Template Structure

```markdown
## Descripción

{Resumen de los cambios realizados}

## Tipo de cambio

- [ ] Bug fix (cambio que soluciona un issue)
- [ ] Nueva funcionalidad (cambio que agrega funcionalidad)
- [ ] Breaking change (cambio que afecta funcionalidad existente)
- [ ] Refactoring (cambio que no agrega funcionalidad ni corrige bugs)
- [ ] Documentación
- [ ] Configuración/CI

## Componentes afectados

- [ ] Backend (.NET API)
- [ ] Frontend (React)
- [ ] Base de datos (SQL Server)
- [ ] Configuración/DevOps

## Issue relacionado

Fix #XXXX

## Checklist

- [ ] Mi código sigue los estándares del proyecto
- [ ] He realizado self-review de mi código
- [ ] He agregado comentarios en código complejo
- [ ] He actualizado la documentación si aplica
- [ ] Mis cambios no generan nuevos warnings
- [ ] He agregado tests que prueban mi fix/feature
- [ ] Los tests existentes pasan localmente
- [ ] He actualizado el CHANGELOG.md si aplica

## Screenshots (si aplica)

{Capturas de pantalla para cambios de UI}

## Notas adicionales

{Cualquier información adicional relevante}
```

## Component-Specific Rules

| Component | Checklist Extra |
|-----------|-----------------|
| Backend | API specs updated? Endpoints documented? |
| Frontend | Screenshots Mobile/Tablet/Desktop? Responsive? |
| Database | Migration scripts? Performance tested? |

## Title Conventions (Conventional Commits)

Format: `type(scope): description`

### Types

| Type | Usage |
|------|-------|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `docs` | Solo documentación |
| `style` | Formato (no afecta lógica) |
| `refactor` | Refactoring sin cambio funcional |
| `perf` | Mejora de performance |
| `test` | Agregar o corregir tests |
| `chore` | Mantenimiento, CI, configs |

### Scopes (opcional)

| Scope | Usage |
|-------|-------|
| `api` | Cambios en backend |
| `ui` | Cambios en frontend |
| `db` | Cambios en base de datos |
| `auth` | Autenticación (Happy) |
| `authz` | Autorización (Lion) |

### Examples

```
feat(api): add user profile endpoint
fix(ui): resolve button alignment in header
refactor(db): optimize user query performance
chore: update dependencies
```

## Commands

```bash
# Check current branch status
git status
git log main..HEAD --oneline

# View full diff
git diff main...HEAD

# Create PR with heredoc for body
gh pr create --title "feat(api): add user endpoint" --body "$(cat <<'EOF'
## Descripción

Agrega endpoint para gestión de usuarios.

## Tipo de cambio

- [x] Nueva funcionalidad

## Componentes afectados

- [x] Backend (.NET API)

## Checklist

- [x] Mi código sigue los estándares del proyecto
- [x] He realizado self-review de mi código
EOF
)"

# Create draft PR
gh pr create --draft --title "feat: description"
```

## Before Creating PR

1. All tests pass locally
2. Linting passes
3. CHANGELOG updated (if applicable)
4. Branch is up to date with main
5. Commits are clean and descriptive
6. No console.log or debug code left
