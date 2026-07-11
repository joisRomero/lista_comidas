# API First README Template

Use this template for `Documentacion/api-first/README.md`:

```markdown
# API First - Especificaciones

Documentacion detallada de las APIs del sistema {ProjectName}.

---

## APIs

| API | Documento | Endpoints | Puerto | Esquema |
|-----|-----------|-----------|--------|---------|
| {Module1} | [{MODULE1}.md]({MODULE1}.md) | {N} | {port} | {Schema} |
| {Module2} | [{MODULE2}.md]({MODULE2}.md) | {N} | {port} | {Schema} |

**Total:** {X} endpoints

---

## Estructura de Documentos

| Seccion | Descripcion |
|---------|-------------|
| Changelog | Ultimos cambios relevantes |
| Modelo de Datos | ERD y referencia a DDL |
| Catalogos | MasterTables requeridas |
| Flujo de Estados | Diagrama de transiciones |
| Endpoints REST | Detalle por subdomain |
| Stored Procedures | Mapeo endpoint → SP |
| DTOs | Modelos compartidos |
| Reglas de Negocio | Validaciones |
| Codigos de Error | Lista de errores |

---

## Convenciones

### URLs REST

| Elemento | Formato | Ejemplo |
|----------|---------|---------|
| Paths | `kebab-case` | `/team-members` |
| Route params | `camelCase` | `/{entityId}` |
| Query params | `camelCase` | `?pageSize=10` |

### Respuesta Estandar

\`\`\`json
{
  "success": true,
  "data": { ... },
  "message": "Operacion exitosa",
  "pagination": {
    "page": 1,
    "pageSize": 10,
    "totalRecords": 100,
    "totalPages": 10
  }
}
\`\`\`
```
