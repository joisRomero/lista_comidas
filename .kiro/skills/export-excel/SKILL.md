---
name: export-excel
description: >
  Patron completo de exportacion a Excel en ANTA: SP con @ParamIIsExport, handler ClosedXML,
  endpoint GET, hook frontend. Cubre todos los archivos necesarios fullstack.
  Trigger: Cuando se implementa exportacion a Excel, descarga de datos, boton Exportar.
metadata:
  author: anta
  version: "1.0"
  scope: [root]
  auto_invoke: "export, exportar, Excel, ClosedXML, download, descargar, IsExport, FileBase64"
  phase: [construction]
  layer: [database, backend, frontend]
  validates_with: null
  validation_profile: null
---

## Reglas Criticas

| Regla | Tipo | Razon |
|-------|------|-------|
| Reutilizar el SP de listado existente con @ParamIIsExport BIT = 0 | SIEMPRE | No crear SP separado |
| El bloque export va ANTES del paginado en el SP | SIEMPRE | Evita OFFSET/FETCH en export |
| Pasar ParamIPage = 1, ParamIPageSize = 1 desde el handler | SIEMPRE | Dapper requiere todos los params declarados |
| Usar string? para fechas en el Request C# | SIEMPRE | Dapper no soporta DateOnly? |
| Usar GetDateString con pattern matching para fechas en el handler | SIEMPRE | Maneja DateTimeOffset y DateTime |
| Usar QueryAsync<dynamic> (no QueryMultipleAsync) para export | SIEMPRE | SP retorna un solo ResultSet sin TotalCount |
| Verificar error en list[0] antes de generar Excel | SIEMPRE | SP puede retornar error code |
| Usings del endpoint: ANTA.Shared.Common + ANTA.Shared.Common.Api.Models | SIEMPRE | NO usar ANTA.Shared.Auth |
| Usar [AsParameters] en el request del endpoint | SIEMPRE | Binding de query params |
| Usar ProfileCodes.User como fallback del rol | SIEMPRE | Consistencia con otros endpoints |
| Registrar handler y endpoint en {Module}Module.cs | SIEMPRE | Sin registro no funciona |
| Agregar constante en {Module}StoredProcedures.cs | SIEMPRE | Centraliza nombres de SP |

---

## Flujo de Implementacion

1. SP: Agregar @ParamIIsExport al SP existente + bloque export antes del paginado
2. Backend: Request -> Response -> Handler (ClosedXML) -> Endpoint -> Module registration
3. Frontend: service-ids.ts -> hook -> logic hook -> boton en Page

---

## 1. SP - Modificacion del SP de Listado

Agregar el parametro y el bloque export ANTES del bloque paginado.
El bloque export usa RETURN para salir sin ejecutar el paginado.

Patron SQL:

    CREATE OR ALTER PROCEDURE [Schema].[ListItems]
        -- params existentes ...
        @ParamIIsExport BIT = 0
    AS
    BEGIN
        SET NOCOUNT ON;
        BEGIN TRY
            -- validaciones y filtros existentes ...

            -- BLOQUE EXPORT va ANTES del paginado
            IF @ParamIIsExport = 1
            BEGIN
                SELECT col1, col2, col3
                FROM [Schema].[Item] i WITH(NOLOCK)
                -- mismos JOINs y WHERE del listado
                ORDER BY col1 DESC;
                RETURN;
            END

            -- bloque paginado existente con OFFSET/FETCH
        END TRY
        BEGIN CATCH
            EXEC [Log].[GetErrorInfo];
        END CATCH
    END

---

## 2. StoredProcedures Constants

La constante de export apunta al MISMO SP del listado:

    public static class {Module}StoredProcedures
    {
        private const string Schema = "{Schema}";

        public const string ListItems = $"{Schema}.ListItems";
        public const string Export{Entity} = $"{Schema}.ListItems"; // mismo SP, flag IsExport
    }

---

## 3. Request

Fechas como string? - Dapper no soporta DateOnly?:

    public class Export{Entity}Request
    {
        public int? StatusFilter { get; set; }
        public string? SearchFilter { get; set; }
        public string? StartDateFilter { get; set; }  // string?, NO DateOnly?
        public string? EndDateFilter { get; set; }    // string?, NO DateOnly?
        public string? SortBy { get; set; }
        public string? SortOrder { get; set; }
    }

---

## 4. Response

    public class Export{Entity}Response
    {
        public string FileBase64 { get; set; } = string.Empty;
        public string FileName { get; set; } = string.Empty;
        public string ContentType { get; set; } = string.Empty;
    }

---

## 5. Handler (ClosedXML)

Usings requeridos: ANTA.Shared.Common.Data.Helpers, ClosedXML.Excel, Dapper, System.Data

    public class Export{Entity}Handler
    {
        private readonly IDbConnection _db;

        public Export{Entity}Handler(IDbConnection db) { _db = db; }

        public async Task<Export{Entity}Response> HandleAsync(
            Export{Entity}Request request, string employeeId, string role, CancellationToken ct = default)
        {
            var command = new CommandDefinition(
                {Module}StoredProcedures.Export{Entity},
                new {
                    ParamIEmployeeId = employeeId,
                    ParamIRole = role,
                    ParamIStatusFilter = request.StatusFilter,
                    ParamISearchFilter = request.SearchFilter,
                    ParamIStartDateFilter = request.StartDateFilter,
                    ParamIEndDateFilter = request.EndDateFilter,
                    ParamIPage = 1,        // requerido por Dapper aunque IsExport=1
                    ParamIPageSize = 1,    // requerido por Dapper aunque IsExport=1
                    ParamISortBy = request.SortBy ?? "DefaultColumn",
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
            var fileName = $"export-{DateTime.Now:yyyyMMdd-HHmmss}.xlsx";

            return new Export{Entity}Response
            {
                FileBase64 = Convert.ToBase64String(bytes),
                FileName = fileName,
                ContentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            };
        }

        private static MemoryStream GenerateExcel(List<dynamic> rows)
        {
            using var workbook = new XLWorkbook();
            var worksheet = workbook.Worksheets.Add("Sheet1");

            var headers = new[] { "Col1", "Col2", "Col3" };
            for (var i = 0; i < headers.Length; i++)
                worksheet.Cell(1, i + 1).Value = headers[i];

            var headerRange = worksheet.Range(1, 1, 1, headers.Length);
            headerRange.Style.Font.Bold = true;
            headerRange.Style.Fill.BackgroundColor = XLColor.LightGray;

            var row = 2;
            foreach (var r in rows)
            {
                var dict = (IDictionary<string, object>)r;
                worksheet.Cell(row, 1).Value = GetString(dict, "Column1");
                worksheet.Cell(row, 2).Value = GetDateString(dict, "DateColumn");
                worksheet.Cell(row, 3).Value = GetNullableString(dict, "NullableColumn");
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

        // OBLIGATORIO para fechas - evita error "DateOnly cannot be used as a parameter value"
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

---

## 6. Endpoint

Usings: ANTA.Shared.Common + ANTA.Shared.Common.Api.Models + Microsoft.AspNetCore.Mvc
NO usar ANTA.Shared.Auth

    public static class Export{Entity}Endpoint
    {
        public static void Map(IEndpointRouteBuilder app)
        {
            app.MapGet("/{route}/export", Handle)
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

---

## 7. Registro en Module

    services.AddScoped<Export{Entity}Handler>();
    Export{Entity}Endpoint.Map(app);

---

## 8. Frontend - service-ids.ts

    export const {Module}Service = {
      // IDs existentes ...
      Export{Entity}: 87017,
    };

---

## 9. Frontend - Hook de Export

    export function useExport{Entity}(params: Export{Entity}Params, enabled: boolean) {
      const createQuery = useHostServiceQuery();
      return createQuery<ExportResponse, Export{Entity}Params>(
        {Module}Service.Export{Entity},
        params,
        undefined,
        { enabled },
      );
    }

---

## 10. Frontend - Logic Hook (trigger de descarga)

    const [exportEnabled, setExportEnabled] = useState(false);

    const exportQuery = useExport{Entity}(filters, exportEnabled);

    useEffect(() => {
      if (exportQuery.data?.data && exportEnabled) {
        const { fileBase64, fileName, contentType } = exportQuery.data.data;
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
    }, [exportQuery.data, exportEnabled]);

    const handleExport = () => setExportEnabled(true);

---

## 11. Frontend - Boton en Page

    <AntaButton type="default" icon={<DownloadOutlined />} onClick={logic.handleExport} loading={logic.exportQuery.isLoading}>
      Exportar
    </AntaButton>

---

## Checklist

- [ ] SP: @ParamIIsExport BIT = 0 agregado al SP existente
- [ ] SP: Bloque export ANTES del bloque paginado con RETURN
- [ ] Constante export en {Module}StoredProcedures.cs (apunta al mismo SP)
- [ ] Request: fechas como string? (no DateOnly?)
- [ ] Handler: QueryAsync<dynamic> (no QueryMultipleAsync)
- [ ] Handler: SpResultHelper.ThrowIfError(list[0]) antes de generar Excel
- [ ] Handler: GetDateString con pattern matching para todas las fechas
- [ ] Handler: ParamIPage = 1, ParamIPageSize = 1 en el CommandDefinition
- [ ] Endpoint: usings ANTA.Shared.Common + ANTA.Shared.Common.Api.Models
- [ ] Endpoint: [AsParameters] en el request
- [ ] Endpoint: ProfileCodes.User como fallback del rol
- [ ] Module: handler y endpoint registrados
- [ ] Frontend: service ID en service-ids.ts
- [ ] Frontend: hook con enabled flag
- [ ] Frontend: efecto de descarga en logic hook
- [ ] Frontend: boton con loading state

## Documentacion Detallada

| Tema | Asset |
|------|-------|
| Ejemplos completos implementados | [implementation-guide.md](assets/implementation-guide.md) |

---

## Al finalizar la implementacion

Siempre mostrar al usuario:

```
ServiceId: {ID}
Path:      /api/v1/{module}/export   (ruta relativa, sin host ni prefijo de gateway)
```

Ejemplo:
```
ServiceId: 87018
Path:      /api/v1/items/export
```

Esto permite registrar el servicio en la tabla Service de la BD del Host.
