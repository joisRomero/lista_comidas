# Service Boundaries

## Core Principle

> "APIs are only as good as their boundaries. If Service A can secretly access the database of Service B, you don't have services. You have a distributed mess."

## Database Schema Ownership

| API | Writes To | Reads From |
|-----|-----------|------------|
| api-maintenance | Cnfg | Cnfg, Log |
| api-{domain} | {Domain} | {Domain}, Cnfg, Log |
| All | Log (audit) | Log |

### Golden Rule

- **Cross-read**: Allowed (validate FKs, get catalogs)
- **Cross-write**: PROHIBITED (each API writes only to its schemas)
- **Log schema**: Special - all write audit via ANTA.Shared.Common.Data

---

## Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Each API owns its schema exclusively | ALWAYS | No cross-service DB access |
| Expose capabilities, not data | ALWAYS | Lower coupling |
| Gateway is the single entry point | ALWAYS | Security, logging, auth |
| No direct API-to-API calls internally | PREFER | Go through Gateway or use events |

---

## Expose Capabilities, Not Data

Design APIs around **use cases**, not data structures:

```csharp
// WRONG: Exposes raw data - high coupling
public interface I{Module}Api
{
    {Entity} Get{Entity}(int {entity}Id);
    List<{Entity}> GetAll{Entities}();
}

// CORRECT: Exposes capabilities - controlled coupling
public interface I{Module}Api
{
    bool Can{Entity}PerformAction(int {entity}Id, string actionCode);
    {Entity}SummaryDto Get{Entity}Summary(int {entity}Id);
    bool Validate{Entity}Permission(int {entity}Id, string permission);
}
```

---

## Service Communication Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Gateway routing** | Frontend → Backend | All client requests go through Gateway |
| **Direct SP call** | Same API, same schema | Handler calls SP in its own schema |
| **API call via Gateway** | Cross-domain query | Module A API needs Module B info → call via Gateway |
| **Shared lookup tables** | Reference data | `MasterTable` in `Config` schema, read-only from other APIs |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (MF)                             │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│   │   Host   │  │  Child A │  │  Child B │  │  Child C │           │
│   └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘           │
└────────┼─────────────┼─────────────┼─────────────┼──────────────────┘
         │             │             │             │
         └─────────────┴──────┬──────┴─────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         API GATEWAY                                  │
│   • Authentication (Happy)                                          │
│   • Header validation                                               │
│   • Route to internal APIs                                          │
└────────────────────────────┬────────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   API Internal  │ │   API Internal  │ │   API Internal  │
│      Module A   │ │      Module B   │ │      Module C   │
│                 │ │                 │ │                 │
│  ┌───────────┐  │ │  ┌───────────┐  │ │  ┌───────────┐  │
│  │ Schema A  │  │ │  │ Schema B  │  │ │  │ Schema C  │  │
│  │ (owned)   │  │ │  │ (owned)   │  │ │  │ (owned)   │  │
│  └───────────┘  │ │  └───────────┘  │ │  └───────────┘  │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┴───────────────────┘
                             │
                   ┌─────────▼─────────┐
                   │    SQL Server     │
                   │   (all schemas)   │
                   └───────────────────┘
```

---

## What Each Service Owns

| Service | Owns | Can Read (shared) |
|---------|------|-------------------|
| API Module A | Schema A (full CRUD) | `Config.MasterTable` |
| API Module B | Schema B (full CRUD) | `Config.MasterTable` |
| API Module C | Schema C (full CRUD) | `Config.MasterTable` |

---

## Forbidden Patterns

| Pattern | Why It's Wrong |
|---------|----------------|
| API A calls SP in Schema B | Breaks ownership boundary |
| API A has direct DB connection to Schema B | Tight coupling |
| Frontend calls API A and API B directly | Bypass Gateway security |
| Shared mutable tables across APIs | Race conditions, unclear ownership |

---

## Allowed Cross-Service Communication

1. **Read-only shared reference data** (`Config.MasterTable`)
2. **Gateway-mediated API calls** (if truly needed)
3. **Event-based async communication** (future: SNS/SQS)
