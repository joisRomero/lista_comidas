# Data Sources for API Catalog

Analyze these sources to build the catalog:

## 1. Stored Procedures

**Location:** `database/{Schema}/StoredProcedures/`

```sql
-- Extract SP name from file
CREATE PROCEDURE {Schema}.{Action}{Entity}
```

## 2. Backend Endpoints

**Location:** `src/{Project}.Api/Modules/{Module}/Features/`

```csharp
// From Endpoint.cs
app.MapGet("/", ...).WithName("List{Entity}");
app.MapGet("/{id}", ...).WithName("Get{Entity}");
app.MapPost("/", ...).WithName("Create{Entity}");
```

## 3. Module Registration

**Location:** `src/{Project}.Api/Modules/{Module}/{Module}Module.cs`

```csharp
// Extract route prefix
var group = app.MapGroup("/api/v1/{entities}")
```

## 4. SP Constants

**Location:** `src/{Project}.Api/Modules/{Module}/{Module}StoredProcedures.cs`

```csharp
public const string List{Entity} = "{Schema}.List{Entity}";
```

## 5. Service IDs

**Location:** Database menu config or `mf-remotes.json` service mapping

## 6. Frontend Routes

**Location:** `Front{Module}/src/{Project}.Front/src/App.tsx` or router config

```typescript
<Route path="/{entities}" element={<{Entity}List />} />
<Route path="/{entities}/:id" element={<{Entity}Detail />} />
```

---

## Naming Convention Mapping

### Main Entities

| Endpoint Name | SP Name | Method | Path Pattern |
|---------------|---------|--------|--------------|
| `List{Entity}` | `{Schema}.List{Entity}` | GET | `/{entities}` |
| `Get{Entity}` | `{Schema}.Get{Entity}` | GET | `/{entities}/{id}` |
| `Create{Entity}` | `{Schema}.Create{Entity}` | POST | `/{entities}` |
| `Update{Entity}` | `{Schema}.Update{Entity}` | PUT | `/{entities}/{id}` |
| `Delete{Entity}` | `{Schema}.Delete{Entity}` | DELETE | `/{entities}/{id}` |

### Sub-entities

| Endpoint Name | SP Name | Method | Path Pattern |
|---------------|---------|--------|--------------|
| `List{SubEntity}` | `{Schema}.List{SubEntity}` | GET | `/{entities}/{id}/{subentities}` |
| `Add{SubEntity}` | `{Schema}.Add{SubEntity}` | POST | `/{entities}/{id}/{subentities}` |
| `Delete{SubEntity}` | `{Schema}.Delete{SubEntity}` | DELETE | `/{entities}/{id}/{subentities}/{subId}` |

---

## Screen Name Convention

| Action | Screen Name Pattern |
|--------|---------------------|
| List | `Listado de {Entity}` |
| Get | `Detalle de {Entity}` |
| Create | `Crear {Entity}` |
| Update | `Editar {Entity}` |
| Delete | - (no screen, action only) |
