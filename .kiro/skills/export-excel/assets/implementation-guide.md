# Export Excel - Implementation Guide

Ejemplos generalizados del patron de implementacion fullstack.

---

## Ejemplo Completo: Export{Entity}

### SP (fragmento clave)

```sql
-- Parametro agregado al SP existente ListItems
@ParamIIsExport BIT = 0

-- Bloque export ANTES del paginado
IF @ParamIIsExport = 1
BEGIN
    SELECT
        i.[ItemId],
        i.[ItemCode],
        i.[ItemName],
        i.[CategoryName],
        i.[CreatedDate],
        i.[StatusName],
        i.[CreatedBy],
        i.[UpdatedDate],
        i.[Notes]
    FROM [Schema].[Item] i WITH(NOLOCK)
    WHERE i.[RecordStatus] = 'A'
      AND (@ParamIStatusFilter IS NULL OR i.[StatusId] = @ParamIStatusFilter)
      AND (@ParamIStartDateFilter IS NULL OR i.[CreatedDate] >= @ParamIStartDateFilter)
      AND (@ParamIEndDateFilter IS NULL OR i.[CreatedDate] <= @ParamIEndDateFilter)
      AND (@VSearchPattern IS NULL OR i.[ItemName] LIKE @VSearchPattern OR i.[ItemCode] LIKE @VSearchPattern)
    ORDER BY i.[CreatedDate] DESC;

    RETURN;
END
```

### Request

```csharp
public class Export{Entity}Request
{
    public int? StatusFilter { get; set; }
    public string? SearchFilter { get; set; }
    public string? StartDateFilter { get; set; }   // string?, NO DateOnly?
    public string? EndDateFilter { get; set; }     // string?, NO DateOnly?
    public string? SortBy { get; set; }
    public string? SortOrder { get; set; }
}
```

### Response

```csharp
public class Export{Entity}Response
{
    public string FileBase64 { get; set; } = string.Empty;
    public string FileName { get; set; } = string.Empty;
    public string ContentType { get; set; } = string.Empty;
}
```

### Handler

```csharp
using ANTA.Shared.Common.Data.Helpers;
using ClosedXML.Excel;
using Dapper;
using System.Data;

public class Export{Entity}Handler
{
    private readonly IDbConnection _db;

    public Export{Entity}Handler(IDbConnection db) => _db = db;

    public async Task<Export{Entity}Response> HandleAsync(
        Export{Entity}Request request,
        string employeeId,
        string role,
        CancellationToken ct = default)
    {
        var command = new CommandDefinition(
            {Module}StoredProcedures.Export{Entity},
            new
            {
                ParamIEmployeeId = employeeId,
                ParamIRole = role,
                ParamIStatusFilter = request.StatusFilter,
                ParamISearchFilter = request.SearchFilter,
                ParamIStartDateFilter = request.StartDateFilter,
                ParamIEndDateFilter = request.EndDateFilter,
                ParamIPage = 1,
                ParamIPageSize = 1,
                ParamISortBy = request.SortBy ?? "CreatedDate",
                ParamISortOrder = request.SortOrder ?? "DESC",
                ParamIIsExport = true
            },
            commandType: CommandType.StoredProcedure,
            cancellationToken: ct
        );

        var results = await _db.QueryAsync<dynamic>(command);
        var list = results.ToList();

        if (list.Count > 0)
            SpResultHelper.ThrowIfError(list[0]);

        using var stream = GenerateExcel(list);
        var bytes = stream.ToArray();

        return new Export{Entity}Response
        {
            FileBase64 = Convert.ToBase64String(bytes),
            FileName = $"items-export-{DateTime.Now:yyyyMMdd-HHmmss}.xlsx",
            ContentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        };
    }

    private static MemoryStream GenerateExcel(List<dynamic> rows)
    {
        using var workbook = new XLWorkbook();
        var worksheet = workbook.Worksheets.Add("Items");

        var headers = new[]
        {
            "Code", "Name", "Category", "Created Date",
            "Status", "Created By", "Updated Date", "Notes"
        };

        for (var i = 0; i < headers.Length; i++)
            worksheet.Cell(1, i + 1).Value = headers[i];

        var headerRange = worksheet.Range(1, 1, 1, headers.Length);
        headerRange.Style.Font.Bold = true;
        headerRange.Style.Fill.BackgroundColor = XLColor.LightGray;

        var row = 2;
        foreach (var r in rows)
        {
            var dict = (IDictionary<string, object>)r;
            worksheet.Cell(row, 1).Value = GetString(dict, "ItemCode");
            worksheet.Cell(row, 2).Value = GetString(dict, "ItemName");
            worksheet.Cell(row, 3).Value = GetString(dict, "CategoryName");
            worksheet.Cell(row, 4).Value = GetDateString(dict, "CreatedDate");
            worksheet.Cell(row, 5).Value = GetString(dict, "StatusName");
            worksheet.Cell(row, 6).Value = GetNullableString(dict, "CreatedBy");
            worksheet.Cell(row, 7).Value = GetDateString(dict, "UpdatedDate");
            worksheet.Cell(row, 8).Value = GetNullableString(dict, "Notes");
            row++;
        }

        worksheet.Columns().AdjustToContents();

        var stream = new MemoryStream();
        workbook.SaveAs(stream);
        stream.Position = 0;
        return stream;
    }

    private static string GetString(IDictionary<string, object> dict, string key)
        => dict.TryGetValue(key, out var value) && value != null ? value.ToString() ?? string.Empty : string.Empty;

    private static string GetNullableString(IDictionary<string, object> dict, string key)
        => dict.TryGetValue(key, out var value) && value != null ? value.ToString() ?? string.Empty : string.Empty;

    private static string GetDateString(IDictionary<string, object> dict, string key)
    {
        if (!dict.TryGetValue(key, out var value) || value == null) return string.Empty;
        return value switch
        {
            DateTimeOffset dto => dto.DateTime.ToString("yyyy-MM-dd"),
            DateTime dt => dt.ToString("yyyy-MM-dd"),
            _ => value.ToString() ?? string.Empty
        };
    }
}
```

### Endpoint

```csharp
using ANTA.Shared.Common;
using ANTA.Shared.Common.Api.Models;
using Microsoft.AspNetCore.Mvc;

public static class Export{Entity}Endpoint
{
    public static void Map(IEndpointRouteBuilder app)
    {
        app.MapGet("/items/export", Handle)
            .Produces<ApiResponse<Export{Entity}Response>>(StatusCodes.Status200OK)
            .ProducesProblem(StatusCodes.Status400BadRequest)
            .ProducesProblem(StatusCodes.Status500InternalServerError);
    }

    private static async Task<IResult> Handle(
        [AsParameters] Export{Entity}Request request,
        [FromServices] Export{Entity}Handler handler,
        [FromServices] HeaderToken headerToken,
        CancellationToken ct)
    {
        var currentUser = headerToken?.EmployeeId ?? "system";
        var currentRole = headerToken?.ProfileId ?? ProfileCodes.User;

        var result = await handler.HandleAsync(request, currentUser, currentRole, ct);

        return Results.Ok(ApiResponse<Export{Entity}Response>.Ok(result, "Exportacion generada exitosamente"));
    }
}
```

### Hook Frontend

```typescript
import { useHostServiceQuery } from '@/shared/adapters';
import { ItemsService } from '@/shared/utils/service-ids';

interface ExportFileData {
  fileBase64: string;
  fileName: string;
  contentType: string;
}

interface ExportResponse {
  success: boolean;
  data: ExportFileData;
  message: string | null;
}

interface ExportItemsParams {
  statusFilter?: number;
  searchFilter?: string;
  startDateFilter?: string;
  endDateFilter?: string;
  sortBy?: string;
  sortOrder?: string;
}

export function useExportItems(
  params: ExportItemsParams,
  enabled: boolean
) {
  const createQuery = useHostServiceQuery();

  return createQuery<ExportResponse, ExportItemsParams>(
    ItemsService.ExportItems,
    params,
    undefined,
    { enabled },
  );
}
```

### Logic Hook (fragmento)

```typescript
const [exportEnabled, setExportEnabled] = useState(false);

const exportItemsQuery = useExportItems(
  {
    statusFilter: filters.status ?? undefined,
    searchFilter: filters.search ?? undefined,
    startDateFilter: filters.startDate ?? undefined,
    endDateFilter: filters.endDate ?? undefined,
    sortBy: tableParams.sortBy,
    sortOrder: tableParams.sortOrder,
  },
  exportEnabled,
);

useEffect(() => {
  if (exportItemsQuery.data?.data && exportEnabled) {
    const { fileBase64, fileName, contentType } = exportItemsQuery.data.data;
    const blob = new Blob(
      [Uint8Array.from(atob(fileBase64), c => c.charCodeAt(0))],
      { type: contentType }
    );
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    a.click();
    URL.revokeObjectURL(url);
    setExportEnabled(false);
  }
}, [exportItemsQuery.data, exportEnabled]);

const handleExportItems = () => setExportEnabled(true);
```

### Boton en Page

```tsx
<AntaButton
  type="default"
  icon={<DownloadOutlined />}
  onClick={logic.handleExportItems}
  loading={logic.exportItemsQuery.isLoading}
>
  Exportar
</AntaButton>
```

---

## Notas de Implementacion

### Por que `string?` para fechas en Request

Dapper no puede serializar `DateOnly?` como parametro de SP. Usar `string?` y dejar que SQL Server haga la conversion implicita a `DATE`.

### Por que `GetDateString` con pattern matching

SQL Server puede retornar fechas como `DateTimeOffset` o `DateTime` dependiendo del tipo de columna. El pattern matching cubre ambos casos sin lanzar `InvalidCastException`.

### Por que `ParamIPage = 1, ParamIPageSize = 1` en export

Dapper mapea parametros por nombre. Si el SP declara `@ParamIPage` y `@ParamIPageSize`, Dapper los requiere en el objeto anonimo aunque el bloque export haga `RETURN` antes de usarlos.

### Por que `QueryAsync<dynamic>` y no `QueryMultipleAsync`

En modo export el SP retorna un solo ResultSet (sin TotalCount). `QueryMultipleAsync` espera multiples grids y fallaria.
