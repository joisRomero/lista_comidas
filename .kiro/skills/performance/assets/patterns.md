# Performance Patterns

## Pagination SP Pattern

```sql
CREATE PROCEDURE Schema.ListEntities
    @PageNumber INT = 1,
    @PageSize INT = 20,
    @SearchTerm NVARCHAR(100) = NULL
AS
BEGIN
    SELECT COUNT(*) AS TotalCount
    FROM Entities
    WHERE (@SearchTerm IS NULL OR Name LIKE '%' + @SearchTerm + '%');
    
    SELECT Id, Code, Name, CreatedAt
    FROM Entities
    WHERE (@SearchTerm IS NULL OR Name LIKE '%' + @SearchTerm + '%')
    ORDER BY CreatedAt DESC
    OFFSET (@PageNumber - 1) * @PageSize ROWS
    FETCH NEXT @PageSize ROWS ONLY;
END
```

## Pagination Handler Pattern

```csharp
public async Task<PaginatedResult<EntityDto>> Handle(Query request)
{
    using var multi = await _db.QueryMultipleAsync(
        "Schema.ListEntities",
        new { request.PageNumber, request.PageSize, request.SearchTerm });
    
    var totalCount = await multi.ReadSingleAsync<int>();
    var items = (await multi.ReadAsync<EntityDto>()).ToList();
    
    return new PaginatedResult<EntityDto>(items, totalCount, request.PageNumber, request.PageSize);
}
```

## Index Strategy

```sql
-- Foreign keys (ALWAYS index)
CREATE INDEX IX_Contracts_CustomerId ON Contracts(CustomerId);

-- Search columns
CREATE INDEX IX_Contracts_Code ON Contracts(Code);

-- Composite for common filters
CREATE INDEX IX_Contracts_Status_CreatedAt ON Contracts(Status, CreatedAt DESC);

-- Include for covering queries
CREATE INDEX IX_Contracts_CustomerId_Inc 
ON Contracts(CustomerId) INCLUDE (Code, Status, Amount);
```

## Backend Caching

```csharp
public async Task<List<StatusDto>> GetStatuses()
{
    return await _cache.GetOrCreateAsync("statuses", async entry =>
    {
        entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(1);
        return await _db.QueryAsync<StatusDto>("Schema.ListStatuses");
    });
}
```

## Frontend Caching (TanStack Query)

```typescript
// Reference data - long cache
const { data: statuses } = useQuery({
  queryKey: ["statuses"],
  queryFn: getStatuses,
  staleTime: 1000 * 60 * 60, // 1 hour
  gcTime: 1000 * 60 * 60 * 2, // 2 hours
});

// Transactional data - short cache
const { data: contracts } = useQuery({
  queryKey: ["contracts", filters],
  queryFn: () => getContracts(filters),
  staleTime: 1000 * 30, // 30 seconds
});
```

## Streaming Export

```csharp
app.MapGet("/export", async (HttpContext ctx, IDbConnection db) =>
{
    ctx.Response.ContentType = "text/csv";
    ctx.Response.Headers.Add("Content-Disposition", "attachment; filename=export.csv");
    
    await using var writer = new StreamWriter(ctx.Response.Body);
    await writer.WriteLineAsync("Id,Code,Name");
    
    await foreach (var item in db.QueryUnbufferedAsync<Entity>("Schema.ListAll"))
    {
        await writer.WriteLineAsync($"{item.Id},{item.Code},{item.Name}");
    }
});
```

## Virtual Scrolling (Frontend)

```typescript
import { useVirtualizer } from "@tanstack/react-virtual";

const virtualizer = useVirtualizer({
  count: items.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 50,
});
```
