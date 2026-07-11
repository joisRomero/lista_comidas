# API-First Spec Section Templates

## 1. Alcance

```markdown
## 1. Alcance

### Incluido

| Funcionalidad | Descripcion |
|---------------|-------------|
| CRUD {Entity} | Crear, listar, ver detalle, actualizar, eliminar |
| {SubEntity} | Agregar, listar, eliminar |

### Excluido (Ver API {OtherModule})

- {Feature handled by other API}
```

---

## 2. Modelo de Datos

```markdown
## 2. Modelo de Datos

### 2.1 Diagrama ER

\`\`\`mermaid
erDiagram
    {MainEntity} ||--o{ {SubEntity1} : tiene
    {MainEntity} ||--o{ {SubEntity2} : tiene
    
    {MainEntity} {
        int {MainEntity}Id PK
        varchar Code UK
        nvarchar Name
        int StatusId FK
    }
    
    {SubEntity1} {
        int {SubEntity1}Id PK
        int {MainEntity}Id FK
        nvarchar FieldName
    }
\`\`\`

### 2.2 Tablas Principales

| Tabla | Descripcion | Script |
|-------|-------------|--------|
| {Schema}.{MainEntity} | Datos principales | /database/{Schema}/ |
| {Schema}.{SubEntity1} | {description} | /database/{Schema}/ |
```

---

## 3. Catalogos Requeridos

```markdown
## 3. Catalogos Requeridos

| Catalogo | Codigo | Campo | Uso |
|----------|--------|-------|-----|
| Tipos de {Entity} | {ENTITY}_TYPES | {Entity}TypeId | {description} |
| Estados | {ENTITY}_STATUSES | StatusId | {description} |
```

---

## 4. Flujo de Estados

```markdown
## 4. Flujo de Estados

### 4.1 Estados

| Estado | Codigo | Tipo | Descripcion |
|--------|--------|------|-------------|
| Borrador | DRAFT | INITIAL | En edicion |
| Pendiente | PENDING | TRANSITION | Esperando accion |
| En Proceso | IN_PROGRESS | PROCESS | Siendo procesado |
| Completado | COMPLETED | FINAL | Finalizado |

### 4.2 Acciones por Estado

| Estado Actual | Acciones Permitidas | Estado Resultante |
|---------------|---------------------|-------------------|
| DRAFT | Submit | PENDING |
| DRAFT | Update, Delete | DRAFT |
| PENDING | Approve | COMPLETED |
| PENDING | Reject | REJECTED |
```

---

## 5. Endpoint Documentation Templates

### 5.1 List Endpoint (Paginated)

```markdown
#### GET /{resource}

**Listar {entities} con paginacion y filtros**

**Query Parameters:**

| Parametro | Tipo | Requerido | Default | Descripcion |
|-----------|------|-----------|---------|-------------|
| page | int | No | 1 | Numero de pagina |
| pageSize | int | No | 10 | Items por pagina (max 50) |
| search | string | No | - | Busqueda por {fields} |
| {filterId} | int | No | - | Filtrar por {field} |
| sortBy | string | No | {default} | Campo de ordenamiento |
| sortOrder | string | No | DESC | ASC o DESC |

**Response:** `200 OK`

\`\`\`json
{
  "success": true,
  "data": {
    "items": [
      {
        "{entityId}": 1,
        "code": "XXX-2025-001",
        "name": "...",
        "status": { "masterTableId": 100, "name": "DRAFT", "value": "Borrador" }
      }
    ]
  },
  "pagination": {
    "page": 1,
    "pageSize": 10,
    "totalRecords": 25,
    "totalPages": 3
  },
  "message": "{Entities} obtenidos exitosamente"
}
\`\`\`

**SP:** `{Schema}.List{Entity}`
```

---

### 5.2 Get Detail Endpoint

```markdown
#### GET /{resource}/{entityId}

**Obtener detalle completo de {entity}**

**Response:** `200 OK`

\`\`\`json
{
  "success": true,
  "data": {
    "item": {
      "{entityId}": 1,
      "code": "XXX-2025-001",
      "name": "...",
      "status": { "masterTableId": 100, "name": "DRAFT", "value": "Borrador" },
      "{subEntities}": [ ... ],
      "summary": {
        "total{SubEntities}": 5,
        "totalAmount": 150000.00
      }
    }
  },
  "message": "{Entity} obtenido exitosamente"
}
\`\`\`

**SP:** `{Schema}.Get{Entity}`
```

---

### 5.3 Create Endpoint

```markdown
#### POST /{resource}

**Crear nuevo {entity}**

**Request:**

\`\`\`json
{
  "name": "...",
  "{fieldId}": 100,
  "{subEntities}": [
    { "{subEntityId}": 1, "order": 1 }
  ]
}
\`\`\`

**Response:** `201 Created`

\`\`\`json
{
  "success": true,
  "data": {
    "item": {
      "{entityId}": 1,
      "code": "XXX-2025-001",
      "name": "...",
      "status": { "masterTableId": 100, "name": "DRAFT", "value": "Borrador" }
    }
  },
  "message": "{Entity} creado exitosamente"
}
\`\`\`

**Reglas:**
- Estado inicial: DRAFT
- {field} es requerido
- {uniqueField} debe ser unico

**SP:** `{Schema}.Create{Entity}`
```

---

### 5.4 Update Endpoint

```markdown
#### PUT /{resource}/{entityId}

**Actualizar {entity}**

**Request:**

\`\`\`json
{
  "name": "...",
  "{fieldId}": 101
}
\`\`\`

**Response:** `200 OK`

\`\`\`json
{
  "success": true,
  "data": {
    "item": {
      "{entityId}": 1,
      "name": "...",
      "status": { "masterTableId": 100, "name": "DRAFT", "value": "Borrador" }
    }
  },
  "message": "{Entity} actualizado exitosamente"
}
\`\`\`

**Reglas:**
- Solo en estado DRAFT puede editarse

**SP:** `{Schema}.Update{Entity}`
```

---

### 5.5 Delete Endpoint

```markdown
#### DELETE /{resource}/{entityId}

**Eliminar {entity}**

**Response:** `200 OK`

\`\`\`json
{
  "success": true,
  "data": {
    "result": "SUCCESS",
    "deleted{EntityId}": 1,
    "deletedCode": "XXX-2025-001",
    "message": "{Entity} eliminado"
  },
  "message": "{Entity} eliminado exitosamente"
}
\`\`\`

**Reglas:**
- Solo en estado DRAFT puede eliminarse
- Soft delete (RecordStatus = 0)

**SP:** `{Schema}.Delete{Entity}`
```

---

### 5.6 Operation Endpoint (State Transition)

```markdown
#### POST /{resource}/{entityId}/{verb}

**{ActionDescription}**

**Request:** (optional, depends on operation)

\`\`\`json
{
  "{requiredField}": "value"
}
\`\`\`

**Response:** `200 OK`

\`\`\`json
{
  "success": true,
  "data": {
    "item": {
      "{entityId}": 1,
      "code": "XXX-2025-001",
      "status": { "masterTableId": 101, "name": "{NEW_STATE}", "value": "{NewStateName}" },
      "{transitionDate}": "2025-01-20T10:00:00Z"
    }
  },
  "message": "{Entity} {actionVerb} exitosamente"
}
\`\`\`

**Reglas:**
- Solo en estado {REQUIRED_STATE}
- {preconditions}

**SP:** `{Schema}.{Verb}{Entity}`
```

**Common operations pattern:**

| Operation | Verb | Typical Preconditions |
|-----------|------|----------------------|
| Submit | `/submit` | Must have required data complete |
| Approve | `/approve` | Must be in PENDING state |
| Reject | `/reject` | Must be in PENDING state, requires reason |
| Cancel | `/cancel` | Not in COMPLETED/CANCELLED state |
| Start | `/start` | Must be in SCHEDULED state |
| End | `/end` | Must be in IN_PROGRESS state, all items resolved |

---

### 5.7 Remove Sub-entity Endpoint

```markdown
#### POST /{resource}/{entityId}/{subResource}/{subEntityId}/remove

**Remover {subEntity}**

**Request:**

\`\`\`json
{
  "justification": "Motivo de la remocion"
}
\`\`\`

**Response:** `200 OK`

\`\`\`json
{
  "success": true,
  "data": {
    "result": "SUCCESS",
    "removed{SubEntityId}": 3,
    "remainingCount": 5,
    "message": "{SubEntity} removido"
  },
  "message": "{SubEntity} removido exitosamente"
}
\`\`\`

**Reglas:**
- Requiere justificacion
- Solo en estados {ALLOWED_STATES}
- {SubEntity} debe pertenecer al {entity} especificado en la URL

**SP:** `{Schema}.Remove{SubEntity}`
```

---

### 5.8 Reorder Endpoint

```markdown
#### PUT /{resource}/{entityId}/{subResource}/reorder

**Reordenar {subEntities}**

**Request:**

\`\`\`json
{
  "items": [
    { "{subEntityId}": 2, "order": 1 },
    { "{subEntityId}": 1, "order": 2 }
  ]
}
\`\`\`

**Response:** `200 OK`

\`\`\`json
{
  "success": true,
  "data": {
    "items": [
      { "{subEntityId}": 2, "order": 1 },
      { "{subEntityId}": 1, "order": 2 }
    ]
  },
  "message": "{SubEntities} reordenados exitosamente"
}
\`\`\`

**SP:** `{Schema}.Reorder{SubEntities}`
```

---

### 5.9 Search / Autocomplete Endpoint

```markdown
#### GET /{resource}

**Buscar {entities} (autocomplete)**

**Query Parameters:**

| Parametro | Tipo | Requerido | Default | Descripcion |
|-----------|------|-----------|---------|-------------|
| search | string | No | - | Busqueda tokenizada por {fields} |
| {filterId} | string | No | - | Filtrar por {field} |
| limit | int | No | 20 | Maximo de resultados (max 50) |

**Response:** `200 OK`

\`\`\`json
{
  "success": true,
  "data": {
    "items": [
      {
        "{entityId}": "E001",
        "name": "...",
        "{groupField}": "..."
      }
    ]
  },
  "message": "{Entities} obtenidos exitosamente"
}
\`\`\`

**SP:** `{Schema}.List{Entities}`
```

---

## 6. Stored Procedures

```markdown
## 6. Stored Procedures

### 6.1 Mapeo Endpoint -> SP

| Endpoint | Metodo | SP |
|----------|--------|-----|
| / | GET | {Schema}.List{Entity} |
| / | POST | {Schema}.Create{Entity} |
| /{id} | GET | {Schema}.Get{Entity} |
| /{id} | PUT | {Schema}.Update{Entity} |
| /{id} | DELETE | {Schema}.Delete{Entity} |
| /{id}/{subentities} | GET | {Schema}.List{SubEntity} |
| /{id}/{subentities} | POST | {Schema}.Add{SubEntity} |
| /{id}/{subentities}/{subId} | DELETE | {Schema}.Delete{SubEntity} |

### 6.2 Ubicacion de Scripts

\`\`\`
{ApiFolder}/database/{Schema}/StoredProcedures/
\`\`\`
```

---

## 7. DTOs Compartidos

```markdown
## 7. DTOs Compartidos

### 7.1 Modelos Compartidos

\`\`\`csharp
// MasterTable - Item de catalogo
public class MasterTable
{
    public int MasterTableId { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Value { get; set; } = string.Empty;
}

// StatusItem - Estado con colores para UI
public class StatusItem
{
    public int MasterTableId { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Value { get; set; } = string.Empty;
    public string? BackgroundColor { get; set; }
    public string? TextColor { get; set; }
}
\`\`\`

### 7.2 Referencia Completa

- **Swagger:** http://localhost:{port}/swagger
- **Codigo:** `{ApiFolder}/src/{Project}.Api/Modules/{Module}/Features/*/`
```

---

## 8. Reglas de Negocio

```markdown
## 8. Reglas de Negocio

### 8.1 Creacion

| Regla | Descripcion |
|-------|-------------|
| RN-001 | {Entity} se crea en estado DRAFT |
| RN-002 | {field} es requerido |

### 8.2 Edicion

| Regla | Descripcion |
|-------|-------------|
| RN-010 | Solo en estado DRAFT puede editarse |
| RN-011 | Solo en estado DRAFT puede eliminarse |

### 8.3 Permisos por Rol

| Accion | {Role1} | {Role2} |
|--------|---------|---------|
| Create | Si | No |
| Approve | No | Si |
```

---

## 9. Codigos de Error

```markdown
## 9. Codigos de Error

### 9.1 Errores de Validacion (VAL_xxx)

| Codigo | Campo | Mensaje |
|--------|-------|---------|
| VAL_001 | {field} | {field} es requerido |
| VAL_002 | {field} | {field} no existe en catalogo |

### 9.2 Errores de Negocio (BUS_xxx)

| Codigo | Mensaje |
|--------|---------|
| BUS_001 | No esta en estado valido para esta operacion |
| BUS_002 | No tiene permisos para esta operacion |

### 9.3 Errores de Recurso (NOT_FOUND)

| Codigo | Mensaje |
|--------|---------|
| NOT_FOUND | {Entity} no encontrado |
```
