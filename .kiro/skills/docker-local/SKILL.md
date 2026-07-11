---
name: docker-local
description: >
  Docker local development setup for ANTA APIs with VPN and SQL Server access.
  Trigger: When setting up Docker for local development, connecting to corporate DB.
metadata:
  author: anta
  version: "1.0"
  scope: [root]
  auto_invoke: "docker local, docker-compose, SQL proxy, CodeArtifact token"
  phase: [construction]
  layer: [backend]
  validates_with: validate_docker
  validation_profile: structure
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Start SQL proxy ONCE before any service | ALWAYS | Shared network |
| Refresh CodeArtifact token before build | ALWAYS | Token expires every 12h |
| Use `host.docker.internal` for DB connection | ALWAYS | Docker network routing |
| Configure WSL2 mirrored networking | FIRST TIME | VPN access from containers |

---

## Prerequisites

- Windows 10/11 with WSL2 enabled
- Docker Desktop (v4.20+) with WSL2 backend
- AWS CLI v2 configured with profile `dev-antamina`
- AWS Client VPN connected

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Network                           │
│  ┌────────────────┐     ┌────────────────┐                  │
│  │  {service}     │────▶│   sql-proxy    │                  │
│  │  Port: {PORT}  │     │   Port: 1433   │                  │
│  └────────────────┘     └───────┬────────┘                  │
└─────────────────────────────────┼───────────────────────────┘
                                  │ host.docker.internal:1433
                    ┌─────────────────────────────┐
                    │  Windows Port Forward       │
                    │  0.0.0.0:1433 → SQL_IP      │
                    └─────────────────────────────┘
                                  │ AWS Client VPN
                    ┌─────────────────────────────┐
                    │  SQL Server (AWS RDS)       │
                    └─────────────────────────────┘
```

---

## First-Time Setup

### 1. Configure WSL2 Networking

```powershell
$wslConfig = @"
[wsl2]
networkingMode=mirrored
dnsTunneling=true
firewall=false
autoProxy=true
"@
$wslConfig | Out-File -FilePath "$env:USERPROFILE\.wslconfig" -Encoding utf8NoBOM -Force
```

### 2. Configure Port Forward (Admin PowerShell)

```powershell
nslookup {sql-server-host}
netsh interface portproxy add v4tov4 listenport=1433 listenaddress=0.0.0.0 connectport=1433 connectaddress={SQL_SERVER_IP}
netsh interface portproxy show all
```

### 3. Restart Docker Desktop

---

## Daily Workflow

### 1. Get CodeArtifact Token (expires 12h)

```powershell
$env:CODEARTIFACT_AUTH_TOKEN = aws codeartifact get-authorization-token `
    --domain {artifact-domain} --domain-owner {aws-account-id} `
    --region us-east-1 --profile dev-antamina `
    --query authorizationToken --output text
```

### 2. Start SQL Proxy (ONCE)

```powershell
docker-compose -f docker-compose.proxy.yml up -d
```

### 3. Build and Run Service

```powershell
docker-compose up -d --build
```

### 4. Verify

```powershell
docker ps
curl http://localhost:{PORT}/swagger
```

---

## Common Commands

| Command | Description |
|---------|-------------|
| `docker-compose up -d --build` | Build and start |
| `docker-compose down` | Stop containers |
| `docker-compose logs -f` | View logs |
| `docker system prune -f` | Clean unused |

---

## Checklist: New Service

### Files
- [ ] `Dockerfile_local` with multi-stage build (SDK 8.0-noble → aspnet 8.0-noble)
- [ ] `docker-compose.yml` with service config
- [ ] `docker-compose.proxy.yml` (copy from existing service — run ONCE only)
- [ ] `nuget.config` with CodeArtifact source

### Configuration
- [ ] Container name follows `source-{service-type}` pattern
- [ ] Image tag follows `200-0{PORT}` pattern
- [ ] Unique port assigned
- [ ] Correct `CODE_PATH` in Dockerfile
- [ ] Correct DLL name in ENTRYPOINT
- [ ] Uses `antamina-network` (external)
- [ ] `ConnectionStrings__DEV_STANDAR` set (if service connects to DB)
- [ ] Dockerfile TZ = `Etc/UTC`, docker-compose TZ = `America/Lima`

### Testing
- [ ] CodeArtifact token refreshed
- [ ] SQL proxy running
- [ ] Swagger accessible
- [ ] DB connection works

---

## Naming Conventions

| Element | Pattern | Example |
|---------|---------|---------|
| Container name | `source-{service-type}` | `source-apigateway`, `source-apiinterna-cases` |
| Image tag | `200-0{PORT}` | `200-03445`, `200-03439` |
| Service port | Unique per service | `3445` (gateway), `3439` (api interna) |
| Network | `antamina-network` (external, shared) | Always the same |

## Inter-Service Communication

Services communicate via container names within `antamina-network`:

```yaml
environment:
  - SessionsApi__BaseUrl=http://source-apiinterna-sessions:3438
```

> Use the container name (e.g., `source-apiinterna-sessions`) as hostname. Docker resolves it within the shared network.

## Placeholders

| Placeholder | Example |
|-------------|---------|
| `{service-name}` | `apigateway`, `apiinterna-cases` |
| `{PORT}` | `3445` |
| `{ProjectName}` | `SystemName.ApiGateway` |
| `{sql-server-host}` | `data01.asid.antamina.com` |
| `{DatabaseName}` | `DB_GESTION_CONTRATOS` |
| `{DbUser}` | `sa` |
| `{DbPassword}` | `(from team)` |

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Dockerfile template | [dockerfile-template](assets/dockerfile-template) |
| docker-compose templates | [docker-compose-templates.yml](assets/docker-compose-templates.yml) |
| Troubleshooting guide | [troubleshooting.md](assets/troubleshooting.md) |
