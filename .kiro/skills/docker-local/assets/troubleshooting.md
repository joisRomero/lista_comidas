# Docker Local Troubleshooting

## Error: "Unable to find package ANTA.Shared..."

**Cause**: CodeArtifact token expired (12h duration).

**Solution**:
```powershell
# Refresh token
$env:CODEARTIFACT_AUTH_TOKEN = aws codeartifact get-authorization-token `
    --domain {artifact-domain} --domain-owner {aws-account-id} `
    --region us-east-1 --profile dev-antamina `
    --query authorizationToken --output text

# Rebuild
docker-compose up -d --build
```

---

## Error: "Could not open a connection to SQL Server"

**Verify**:

1. **VPN connected**:
```powershell
Test-NetConnection {sql-server-host} -Port 1433
```

2. **Port forward configured**:
```powershell
netsh interface portproxy show all
```

3. **Restart containers**:
```powershell
docker-compose down
docker-compose up -d
```

---

## SQL Server IP Changed

Run as **Administrator**:

```powershell
# 1. Get new IP
nslookup {sql-server-host}

# 2. Remove old port forward
netsh interface portproxy delete v4tov4 listenport=1433 listenaddress=0.0.0.0

# 3. Create new port forward
netsh interface portproxy add v4tov4 listenport=1433 listenaddress=0.0.0.0 connectport=1433 connectaddress={NEW_IP}
```

---

## Containers Won't Start

```powershell
# View error logs
docker-compose logs

# Clean and rebuild
docker-compose down -v
docker system prune -f
docker-compose up -d --build
```
