# User Stories — Alimentación Mobile (BD Local)

**Proyecto:** ALIM-MOB (Alimentacion Mobile)
**Arquitectura:** App Standalone con SQLite local
**Sincronización:** Ninguna — datos viven solo en el dispositivo

---

## EPIC: Infraestructura Mobile | INFRA

---

## ALIM-MOB-001: Configuración Base del Proyecto Mobile

**Epic:** Infraestructura Mobile
**Layer:** FULL (Mobile)

### Historia

**Como** desarrollador mobile
**Quiero** tener el proyecto base configurado con BD local, navegación y tema visual
**Para** poder implementar las pantallas funcionales sobre una base sólida

### Criterios de Aceptación

- [ ] CA1: Proyecto creado con el framework elegido (Flutter / React Native / MAUI)
- [ ] CA2: SQLite configurado con esquema inicial (6 tablas + índices)
- [ ] CA3: Sistema de migraciones de BD implementado (versionado)
- [ ] CA4: Navegación por bottom tabs (Inicio, Catálogos, Recetas, Planes, Más)
- [ ] CA5: Tema global con paleta (#40E2D2, #40A1E2, #4050E2)
- [ ] CA6: Componentes base: Loader, Toast/Snackbar, ConfirmDialog, SearchBar, EmptyState
- [ ] CA7: Capa de Repository base con operaciones CRUD genéricas
- [ ] CA8: Manejo de errores centralizado (mostrar mensajes en español via toast)
- [ ] CA9: Pull-to-refresh como patrón global
- [ ] CA10: Interfaz completamente en español

### Notas Técnicas

- Crear `DatabaseHelper` que inicializa SQLite y ejecuta el DDL completo
- Implementar patrón Repository con interfaz genérica (getAll, getById, insert, update, delete)
- Clase base `BaseRepository<T>` para reutilizar operaciones comunes
- Inyección de dependencias para repositorios y servicios

---

**Prioridad:** Crítica (bloqueante)
**Estimación:** M

---

## EPIC: Gestión de Catálogos | CATALOGOS

---

## ALIM-MOB-002: CRUD de Categorías (Mobile)

**Epic:** Gestión de Catálogos
**Layer:** FULL (Mobile)

### Historia

**Como** usuario de la app móvil
**Quiero** gestionar categorías de ingredientes desde mi teléfono
**Para** clasificar mis ingredientes en cualquier momento

### Descripción

Pantalla de listado con búsqueda local (SQL LIKE) y formulario para crear/editar.
Eliminar con confirmación y validación de integridad referencial.

### Criterios de Aceptación

- [ ] CA1: Listado muestra todas las categorías ordenadas alfabéticamente
- [ ] CA2: Barra de búsqueda filtra por nombre (query local LIKE)
- [ ] CA3: FAB "+" navega a formulario de creación
- [ ] CA4: Tap en un item navega a formulario de edición (precargado)
- [ ] CA5: Swipe-left muestra opción "Eliminar" con dialog de confirmación
- [ ] CA6: Al crear: INSERT en BD + toast "Categoría creada correctamente"
- [ ] CA7: Al editar: UPDATE en BD + toast "Cambios guardados"
- [ ] CA8: Al eliminar exitoso: DELETE + toast "Categoría eliminada"
- [ ] CA9: Integridad: si tiene ingredientes → toast "No se puede eliminar..."
- [ ] CA10: Validación local: nombre requerido, max 100 chars, único
- [ ] CA11: Pull-to-refresh recarga desde BD

### Queries SQL (Repository)

```sql
-- Listar
SELECT * FROM Categories ORDER BY Name ASC;

-- Buscar
SELECT * FROM Categories WHERE Name LIKE '%term%' ORDER BY Name ASC;

-- Verificar unicidad antes de INSERT/UPDATE
SELECT COUNT(*) FROM Categories WHERE LOWER(Name) = LOWER(?);

-- Verificar integridad antes de DELETE
SELECT COUNT(*) FROM Ingredients WHERE CategoryId = ?;

-- CRUD
INSERT INTO Categories (Name, Description) VALUES (?, ?);
UPDATE Categories SET Name = ?, Description = ? WHERE Id = ?;
DELETE FROM Categories WHERE Id = ?;
```

### Datos de Prueba

| Escenario | Input | Output Esperado |
|-----------|-------|-----------------|
| Lista vacía | Sin categorías en BD | Empty state: "No hay categorías. ¡Crea la primera!" |
| Crear exitoso | Nombre: "Verduras" | Toast éxito, refrescar lista |
| Nombre vacío | Nombre: "" | Error local: "El nombre es requerido" |
| Duplicado | Nombre: "Verduras" (ya existe) | Error: "Ya existe una categoría con ese nombre" |
| Eliminar con hijos | Categoría con ingredientes | Error: "No se puede eliminar..." |

---

**Prioridad:** Alta
**Estimación:** S

---

## ALIM-MOB-003: CRUD de Unidades de Medida (Mobile)

**Epic:** Gestión de Catálogos
**Layer:** FULL (Mobile)

### Historia

**Como** usuario de la app móvil
**Quiero** gestionar unidades de medida desde mi teléfono
**Para** definir las unidades que uso en mis recetas

### Criterios de Aceptación

- [ ] CA1: Listado con nombre y símbolo (badge) ordenado alfabéticamente
- [ ] CA2: Búsqueda local por nombre o símbolo
- [ ] CA3: FAB "+" para crear, tap para editar, swipe para eliminar
- [ ] CA4: Formulario con campos: Nombre (requerido, max 50) y Símbolo (requerido, max 10)
- [ ] CA5: Validación de unicidad de nombre
- [ ] CA6: Protección de eliminación si referenciada por ingredientes
- [ ] CA7: Toast de confirmación en cada operación CRUD
- [ ] CA8: Pull-to-refresh

### Queries SQL (Repository)

```sql
-- Listar
SELECT * FROM Units ORDER BY Name ASC;

-- Verificar integridad antes de DELETE
SELECT COUNT(*) FROM Ingredients WHERE UnitId = ?;
```

### Datos de Prueba

| Escenario | Input | Output Esperado |
|-----------|-------|-----------------|
| Crear exitoso | "Kilogramo", "kg" | Toast éxito |
| Sin símbolo | "Test", "" | Error: "El símbolo es requerido" |
| Eliminar con hijos | Unidad usada en ingredientes | Error: "No se puede eliminar..." |

---

**Prioridad:** Alta
**Estimación:** S

---

## EPIC: Gestión de Ingredientes | INGREDIENTES

---

## ALIM-MOB-004: CRUD de Ingredientes (Mobile)

**Epic:** Gestión de Ingredientes
**Layer:** FULL (Mobile)

### Historia

**Como** usuario de la app móvil
**Quiero** registrar ingredientes con unidad, categoría y datos de maduración
**Para** tener mi inventario completo y que la lista de compras se genere correctamente

### Descripción

Listado con badges de categoría y tipo. Formulario con Bottom Sheets buscables
para seleccionar unidad y categoría desde la BD local. Campo condicional de maduración.

### Criterios de Aceptación

- [ ] CA1: Listado muestra: nombre, símbolo unidad (badge), categoría (badge), tipo, días maduración
- [ ] CA2: Búsqueda local por nombre, categoría o unidad (JOIN + LIKE)
- [ ] CA3: FAB "+" para crear, tap para editar, swipe para eliminar
- [ ] CA4: Formulario - Unidad via Bottom Sheet buscable (datos de tabla Units)
- [ ] CA5: Formulario - Categoría via Bottom Sheet buscable (datos de tabla Categories)
- [ ] CA6: Checkbox "Es perecible": si activo, muestra campo "Días de maduración"
- [ ] CA7: Validación: si perecible, días > 0; si no perecible, días = null
- [ ] CA8: Protección de eliminación si está en algún plato (DishIngredients)
- [ ] CA9: Toast de confirmación en cada operación
- [ ] CA10: Nombre único validado antes de INSERT/UPDATE

### Queries SQL (Repository)

```sql
-- Listar con JOINs
SELECT i.*, u.Name AS UnitName, u.Symbol AS UnitSymbol, c.Name AS CategoryName
FROM Ingredients i
JOIN Units u ON i.UnitId = u.Id
JOIN Categories c ON i.CategoryId = c.Id
ORDER BY i.Name ASC;

-- Buscar
SELECT i.*, u.Name AS UnitName, u.Symbol AS UnitSymbol, c.Name AS CategoryName
FROM Ingredients i
JOIN Units u ON i.UnitId = u.Id
JOIN Categories c ON i.CategoryId = c.Id
WHERE i.Name LIKE '%term%' OR c.Name LIKE '%term%' OR u.Name LIKE '%term%'
ORDER BY i.Name ASC;

-- Verificar integridad antes de DELETE
SELECT COUNT(*) FROM DishIngredients WHERE IngredientId = ?;
```

### Datos de Prueba

| Escenario | Input | Output Esperado |
|-----------|-------|-----------------|
| Perecible | Tomate, kg, Verduras, perecible, 5 días | Toast éxito |
| No perecible | Arroz, kg, Granos, no perecible | Toast éxito, maduración null |
| Perecible sin días | Leche, L, Lácteos, perecible, 0 | Error: "Días debe ser > 0" |
| En uso | Ingrediente en un plato | Error: "No se puede eliminar..." |

---

**Prioridad:** Alta
**Estimación:** M

---

## EPIC: Gestión de Platos | PLATOS

---

## ALIM-MOB-005: CRUD de Platos (Mobile)

**Epic:** Gestión de Platos
**Layer:** FULL (Mobile)

### Historia

**Como** usuario de la app móvil
**Quiero** crear y editar platos con sus ingredientes y cantidades
**Para** tener mis recetas listas y asignarlas al plan de comidas

### Descripción

Formulario con lista dinámica de ingredientes seleccionados desde Bottom Sheet.
Operación transaccional: INSERT/UPDATE Dish + DishIngredients en una transacción.

### Criterios de Aceptación

- [ ] CA1: Listado con nombre, tipo de comida (badge), cantidad de ingredientes
- [ ] CA2: Búsqueda por nombre y tipo de comida
- [ ] CA3: FAB "+" para crear, tap para editar, swipe para eliminar
- [ ] CA4: Formulario - Nombre, descripción (opcional), tipo de comida (Picker)
- [ ] CA5: Tipos de comida: Desayuno, Almuerzo, Cena, Snack, Postre (español)
- [ ] CA6: Lista de ingredientes dinámica con botón "Agregar ingrediente"
- [ ] CA7: Cada ingrediente: Bottom Sheet buscable + campo numérico cantidad
- [ ] CA8: Botón "X" para eliminar ingrediente de la lista
- [ ] CA9: Validación: al menos 1 ingrediente, cantidades > 0, sin duplicados
- [ ] CA10: Guardar usa TRANSACCIÓN: INSERT Dish → INSERT DishIngredients
- [ ] CA11: Editar: DELETE DishIngredients WHERE DishId → re-INSERT nuevos
- [ ] CA12: Protección eliminación si está en MealPlanItems
- [ ] CA13: Toast de confirmación

### Queries SQL (Repository)

```sql
-- Listar con conteo de ingredientes
SELECT d.*, COUNT(di.Id) AS IngredientCount
FROM Dishes d
LEFT JOIN DishIngredients di ON d.Id = di.DishId
GROUP BY d.Id
ORDER BY d.Name ASC;

-- Obtener plato con ingredientes
SELECT d.* FROM Dishes WHERE Id = ?;
SELECT di.*, i.Name AS IngredientName, u.Symbol AS UnitSymbol
FROM DishIngredients di
JOIN Ingredients i ON di.IngredientId = i.Id
JOIN Units u ON i.UnitId = u.Id
WHERE di.DishId = ?;

-- Protección de eliminación
SELECT COUNT(*) FROM MealPlanItems WHERE DishId = ?;

-- Transacción de creación
BEGIN TRANSACTION;
INSERT INTO Dishes (Name, Description, MealType) VALUES (?, ?, ?);
-- Obtener last_insert_rowid()
INSERT INTO DishIngredients (DishId, IngredientId, Quantity) VALUES (?, ?, ?);
-- Repetir por cada ingrediente
COMMIT;

-- Transacción de edición
BEGIN TRANSACTION;
UPDATE Dishes SET Name=?, Description=?, MealType=? WHERE Id=?;
DELETE FROM DishIngredients WHERE DishId = ?;
INSERT INTO DishIngredients (DishId, IngredientId, Quantity) VALUES (?, ?, ?);
COMMIT;
```

### Datos de Prueba

| Escenario | Input | Output Esperado |
|-----------|-------|-----------------|
| Crear exitoso | "Arroz con pollo", Almuerzo, 2 ingredientes | Toast éxito |
| Sin ingredientes | "Vacío", Almuerzo, 0 ingredientes | Error: "Al menos un ingrediente" |
| Cantidad cero | Ingrediente con cantidad 0 | Error: "Cantidad debe ser > 0" |
| En plan | Plato usado en un plan | Error: "No se puede eliminar..." |

---

**Prioridad:** Alta
**Estimación:** M

---

## EPIC: Planificación de Comidas | PLANIFICACION

---

## ALIM-MOB-006: Plan de Comidas Semanal/Mensual (Mobile)

**Epic:** Planificación de Comidas
**Layer:** FULL (Mobile)

### Historia

**Como** usuario de la app móvil
**Quiero** crear planes de comidas semanales o mensuales
**Para** organizar mis comidas directamente desde mi teléfono

### Descripción

Formulario con date pickers nativos y lista dinámica de items (fecha + momento + plato).
Vista de detalle con items agrupados por fecha.

### Criterios de Aceptación

- [ ] CA1: Listado con tipo (badge), fecha inicio/fin, cantidad de items
- [ ] CA2: Búsqueda por tipo de plan
- [ ] CA3: FAB "+" para crear, tap para ver detalle, swipe para eliminar
- [ ] CA4: Formulario - Tipo: Semanal / Mensual (Picker)
- [ ] CA5: Formulario - Fecha inicio y fin con Date Pickers nativos
- [ ] CA6: Lista de items: Fecha (DatePicker) + Momento (Picker) + Plato (Bottom Sheet)
- [ ] CA7: Botón "Agregar item" y "X" para eliminar
- [ ] CA8: Validación: fecha fin > inicio, al menos 1 item, fechas items dentro del rango
- [ ] CA9: Si no hay platos en BD: mensaje "No hay platos. Cree platos primero" con botón
- [ ] CA10: Guardar con TRANSACCIÓN: INSERT MealPlan → INSERT MealPlanItems
- [ ] CA11: Vista detalle: items agrupados por fecha, cada grupo muestra momento + plato
- [ ] CA12: Toast de confirmación

### Queries SQL (Repository)

```sql
-- Listar planes con conteo
SELECT mp.*, COUNT(mpi.Id) AS ItemCount
FROM MealPlans mp
LEFT JOIN MealPlanItems mpi ON mp.Id = mpi.MealPlanId
GROUP BY mp.Id
ORDER BY mp.StartDate DESC;

-- Obtener plan con items
SELECT mp.* FROM MealPlans WHERE Id = ?;
SELECT mpi.*, d.Name AS DishName, d.MealType AS DishMealType
FROM MealPlanItems mpi
JOIN Dishes d ON mpi.DishId = d.Id
WHERE mpi.MealPlanId = ?
ORDER BY mpi.Date ASC, mpi.MealTime ASC;

-- Verificar platos disponibles
SELECT COUNT(*) FROM Dishes;

-- Transacción de creación
BEGIN TRANSACTION;
INSERT INTO MealPlans (PlanType, StartDate, EndDate) VALUES (?, ?, ?);
INSERT INTO MealPlanItems (MealPlanId, DishId, Date, MealTime) VALUES (?, ?, ?, ?);
COMMIT;
```

### Datos de Prueba

| Escenario | Input | Output Esperado |
|-----------|-------|-----------------|
| Plan semanal | Tipo: Semanal, 7 días, 3 items | Toast éxito |
| Fecha inválida | Fin < Inicio | Error: "Fecha fin debe ser posterior" |
| Sin platos en BD | 0 platos | Mensaje + botón "Crear plato" |
| Plan vacío | 0 items | Error: "Debe tener al menos un item" |

---

**Prioridad:** Alta
**Estimación:** L

---

## ALIM-MOB-007: Lista de Compras Inteligente (Mobile)

**Epic:** Planificación de Comidas
**Layer:** FULL (Mobile)

### Historia

**Como** usuario de la app móvil
**Quiero** generar la lista de compras desde mi plan y llevarla al supermercado
**Para** comprar exactamente lo que necesito sin olvidar nada

### Descripción

Desde el detalle de un plan, botón "Generar Lista". Algoritmo de agrupación y
segmentación ejecutado localmente consultando la BD. Opción de exportar a PDF
y compartir via Share Sheet nativo.

### Criterios de Aceptación

- [ ] CA1: Botón "Generar Lista de Compras" en pantalla de detalle del plan
- [ ] CA2: Ejecuta algoritmo de agrupación localmente (query + lógica en Service)
- [ ] CA3: Planes mensuales: 3 secciones (Listos ≤7d, Verdes >7d, Otros no perecibles)
- [ ] CA4: Planes semanales: lista única sin segmentación
- [ ] CA5: Cada item muestra: nombre, cantidad total, unidad, categoría
- [ ] CA6: Secciones colapsables con contador
- [ ] CA7: Botón "Regenerar" para recalcular
- [ ] CA8: Botón "Exportar PDF" genera PDF localmente y abre Share Sheet
- [ ] CA9: Toast "Lista generada correctamente"
- [ ] CA10: Si plan sin items: mensaje "No hay ingredientes en este plan"

### Query SQL (Obtener ingredientes agrupados para un plan)

```sql
-- Obtener todos los ingredientes de un plan, agrupados y sumados
SELECT 
    i.Id,
    i.Name AS IngredientName,
    SUM(di.Quantity) AS TotalQuantity,
    u.Symbol AS UnitSymbol,
    c.Name AS CategoryName,
    i.IsPerishable,
    i.RipeningDays
FROM MealPlanItems mpi
JOIN DishIngredients di ON mpi.DishId = di.DishId
JOIN Ingredients i ON di.IngredientId = i.Id
JOIN Units u ON i.UnitId = u.Id
JOIN Categories c ON i.CategoryId = c.Id
WHERE mpi.MealPlanId = ?
GROUP BY i.Id, i.Name, u.Symbol, c.Name, i.IsPerishable, i.RipeningDays
ORDER BY c.Name ASC, i.Name ASC;
```

La segmentación se aplica en la capa de Service (no en SQL):
- `IsPerishable = 1 AND RipeningDays <= 7` → Listos para comer
- `IsPerishable = 1 AND RipeningDays > 7` → Comprar verdes
- `IsPerishable = 0` → Otros productos

### Datos de Prueba

| Escenario | Input | Output Esperado |
|-----------|-------|-----------------|
| Semanal con 3 platos | Plan semanal con items | Lista agrupada sin secciones |
| Mensual con perecibles | Plan con Tomate(5d), Papa(15d), Arroz | 3 secciones |
| Plan vacío | Plan sin items | Mensaje: "No hay ingredientes" |
| Exportar PDF | Click exportar | PDF generado + Share Sheet |
| Mismo ingrediente 2 platos | Arroz en 2 platos distintos | Cantidades sumadas |

---

**Prioridad:** Alta
**Estimación:** M

---

## ALIM-MOB-008: Backup y Restauración de Datos

**Epic:** Infraestructura Mobile
**Layer:** FULL (Mobile)

### Historia

**Como** usuario de la app móvil
**Quiero** poder hacer backup de mis datos y restaurarlos
**Para** no perder mi información si cambio de teléfono o reinstalo la app

### Criterios de Aceptación

- [ ] CA1: Pantalla "Más" → opción "Backup de datos"
- [ ] CA2: Botón "Exportar backup" copia el archivo .db y lo comparte via Share Sheet
- [ ] CA3: Botón "Importar backup" permite seleccionar archivo .db y reemplazar BD actual
- [ ] CA4: Confirmación antes de importar: "Esto reemplazará todos sus datos actuales"
- [ ] CA5: Toast de confirmación tras backup/restore exitoso
- [ ] CA6: Validación: el archivo importado debe ser una BD SQLite válida con las tablas esperadas

### Notas Técnicas

- El archivo de BD SQLite es un solo archivo (ej: `alimentacion.db`)
- Exportar = copiar archivo a directorio compartido o Share Sheet
- Importar = reemplazar archivo actual, reiniciar la app/conexión

---

**Prioridad:** Media
**Estimación:** S

---

## 9. Resumen de Estimación

| HU | Título | Estimación | Dependencias |
|----|--------|-----------|--------------|
| ALIM-MOB-001 | Configuración Base + BD | M | Ninguna |
| ALIM-MOB-002 | CRUD Categorías | S | MOB-001 |
| ALIM-MOB-003 | CRUD Unidades | S | MOB-001 |
| ALIM-MOB-004 | CRUD Ingredientes | M | MOB-002, MOB-003 |
| ALIM-MOB-005 | CRUD Platos | M | MOB-004 |
| ALIM-MOB-006 | Plan de Comidas | L | MOB-005 |
| ALIM-MOB-007 | Lista de Compras + PDF | M | MOB-006 |
| ALIM-MOB-008 | Backup / Restauración | S | MOB-001 |

### Orden de Implementación

```
MOB-001 (Base + BD SQLite)
    ↓
MOB-002 + MOB-003 (Catálogos - paralelo)
    ↓
MOB-004 (Ingredientes)
    ↓
MOB-005 (Platos)
    ↓
MOB-006 (Planes)
    ↓
MOB-007 (Lista de Compras + PDF)
    ↓
MOB-008 (Backup)
```

---

## 10. Checklist de Entrega por Sprint

### Sprint 1: Base + Catálogos
- [ ] Proyecto configurado con SQLite (MOB-001)
- [ ] Schema BD creado con 6 tablas + índices
- [ ] Navegación por tabs funcional
- [ ] Tema visual aplicado
- [ ] Componentes base creados
- [ ] CRUD Categorías completo (MOB-002)
- [ ] CRUD Unidades completo (MOB-003)

### Sprint 2: Ingredientes + Platos
- [ ] CRUD Ingredientes con Bottom Sheets (MOB-004)
- [ ] CRUD Platos con ingredientes dinámicos (MOB-005)
- [ ] Transacciones de BD verificadas

### Sprint 3: Planificación + Extras
- [ ] CRUD Planes de Comida (MOB-006)
- [ ] Lista de Compras con segmentación (MOB-007)
- [ ] Generación de PDF local
- [ ] Backup / Restauración (MOB-008)
- [ ] QA y correcciones finales
