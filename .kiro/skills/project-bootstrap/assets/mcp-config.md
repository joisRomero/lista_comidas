# Database MCP Configuration

## OpenCode / Claude Code

Create `opencode.json` in project root:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "sqlserver": {
      "type": "local",
      "command": [
        "npx", "-y", "@bytebase/dbhub@latest",
        "--transport", "stdio",
        "--dsn", "sqlserver://{user}:{password}@{server}:{port}/{database}?trustServerCertificate=true"
      ],
      "enabled": true,
      "timeout": 30000
    }
  }
}
```

## Where to Find Connection Details

1. **appsettings.Development.json**
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server={server};Database={database};User Id={user};Password={password};"
  }
}
```

2. **docker-compose.yml**
```yaml
services:
  sqlserver:
    environment:
      - SA_PASSWORD={password}
    ports:
      - "1433:1433"
```

3. **Ask user** if not found in config files

## DSN Format

```
sqlserver://{user}:{password}@{server}:{port}/{database}?trustServerCertificate=true
```

### Examples

**Local Docker:**
```
sqlserver://sa:YourPassword123@localhost:1433/MyDatabase?trustServerCertificate=true
```

**Corporate (via VPN):**
```
sqlserver://domain\\user:password@dbserver.corp.local:1433/ProductionDB?trustServerCertificate=true
```

## Verify MCP is Working

After configuring, restart your AI assistant and test:
- Ask: "List tables in the database"
- Or: "Show me the stored procedures in schema X"

If it works, you'll get real data back.
