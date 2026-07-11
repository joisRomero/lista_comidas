---
name: performance
description: >
  Performance patterns for ANTA applications.
  Trigger: When implementing pagination, caching, query optimization, or large data handling.
metadata:
  author: anta
  version: "1.0"
  scope: [root]
  auto_invoke: "performance, pagination, caching, optimization, slow query, large data"
  phase: [construction]
  layer: [database, backend]
  validates_with: null
  validation_profile: null
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Always paginate list endpoints | ALWAYS | Prevent memory issues |
| Use `SELECT` only needed columns | ALWAYS | Reduce data transfer |
| Index foreign keys and search columns | ALWAYS | Query performance |
| Cache reference data, not transactional | ALWAYS | Stale data risk |

---

## Pagination Quick Reference

### API Response Format

```json
{
  "success": true,
  "data": [...],
  "pagination": { "pageNumber": 1, "pageSize": 20, "totalCount": 150, "totalPages": 8 }
}
```

### Frontend Hook

```typescript
const { data } = useQuery({
  queryKey: ["entities", { page, pageSize, search }],
  queryFn: () => getEntities({ page, pageSize, search }),
  placeholderData: keepPreviousData,
});
```

---

## Query Optimization Tips

```sql
-- ✅ Use EXISTS instead of COUNT for checks
IF EXISTS (SELECT 1 FROM Contracts WHERE Code = @Code)

-- ✅ Use TOP 1 when only checking existence
SELECT TOP 1 Id FROM Contracts WHERE CustomerId = @CustomerId

-- ✅ Avoid SELECT *
SELECT Id, Code, Name FROM Contracts

-- ✅ Use NOLOCK for read-only reports (with caution)
SELECT * FROM Contracts WITH (NOLOCK) WHERE Status = 'Active'
```

---

## Caching Strategy

| Cache | TTL | Example |
|-------|-----|---------|
| Reference data | 1 hour | Status list, categories |
| User permissions | 5 min | Lion permissions |
| Configuration | 10 min | Feature flags |
| **DON'T cache** | - | Transactional data |

### Frontend (TanStack Query)

```typescript
// Reference data - long cache
staleTime: 1000 * 60 * 60 // 1 hour

// Transactional data - short cache
staleTime: 1000 * 30 // 30 seconds
```

---

## Large Data Handling

| Technique | When |
|-----------|------|
| Streaming export | CSV/Excel downloads |
| Virtual scrolling | Long lists in UI |
| Cursor pagination | Infinite scroll |

---

## Checklist

- [ ] All list endpoints paginated (default 20, max 100)
- [ ] Foreign keys indexed
- [ ] Search columns indexed
- [ ] SP uses `SELECT` specific columns
- [ ] Reference data cached appropriately
- [ ] Large exports use streaming
- [ ] Frontend uses `staleTime` for reference data

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Full patterns (SP, Handler, Caching, Export) | [patterns.md](assets/patterns.md) |

## Related Skills

| Task | Skill |
|------|-------|
| SP patterns | `database-sp` |
| TanStack Query | `react-hooks` |
| API response format | `dotnet-api` |
