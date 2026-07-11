# Componentes — Ñami (ALIM-MOB)

**Fecha**: 2026-07-11  
**Arquitectura**: 4 capas — UI → Providers → Services → Repositories → sqflite

---

## Capa 1: Database

### DatabaseHelper
**Propósito**: Singleton que gestiona el ciclo de vida de la conexión SQLite.

**Responsabilidades**:
- Inicializar la BD en primera ejecución (ejecutar DDL completo)
- Gestionar versión del schema y ejecutar migrations (`onUpgrade`)
- Proveer la instancia `Database` a todos los Repositories
- Cerrar la conexión al destruir el app

---

## Capa 2: Repositories (acceso a datos)

Todos extienden `BaseRepository<T>`. Responsabilidad única: traducir operaciones de dominio a SQL y mapear resultados a modelos Dart.

### BaseRepository\<T\>
**Propósito**: Clase abstracta genérica con operaciones CRUD comunes.

**Responsabilidades**:
- Definir contrato: `getAll()`, `getById()`, `insert()`, `update()`, `delete()`
- Proveer helper para mapeo `Map<String,dynamic> → T`

### CategoryRepository
**Propósito**: Acceso a datos de la tabla `Categories`.

**Responsabilidades**:
- Listar categorías ordenadas alfabéticamente
- Buscar por nombre (LIKE)
- Verificar unicidad de nombre antes de INSERT/UPDATE
- Verificar si tiene ingredientes asociados (COUNT) antes de DELETE
- CRUD estándar

### UnitRepository
**Propósito**: Acceso a datos de la tabla `Units`.

**Responsabilidades**:
- Listar unidades ordenadas alfabéticamente
- Buscar por nombre o símbolo (LIKE)
- Verificar unicidad de nombre
- Verificar si tiene ingredientes asociados antes de DELETE
- CRUD estándar

### IngredientRepository
**Propósito**: Acceso a datos de la tabla `Ingredients` con JOINs a `Units` y `Categories`.

**Responsabilidades**:
- Listar ingredientes con datos de unidad y categoría (JOIN)
- Buscar con JOIN por nombre, categoría o unidad (LIKE)
- Verificar unicidad de nombre
- Verificar si está en algún `DishIngredients` antes de DELETE
- CRUD estándar

### DishRepository
**Propósito**: Acceso a datos de `Dishes` y `DishIngredients`.

**Responsabilidades**:
- Listar platos con conteo de ingredientes (LEFT JOIN + COUNT)
- Buscar por nombre y tipo
- Obtener plato completo con sus `DishIngredients` (JOIN a Ingredients + Units)
- Guardar plato con ingredientes en transacción (BEGIN/COMMIT)
- Actualizar plato: DELETE + re-INSERT de DishIngredients en transacción
- Verificar si está en `MealPlanItems` antes de DELETE
- DELETE cascade automático en DishIngredients (ON DELETE CASCADE)

### MealPlanRepository
**Propósito**: Acceso a datos de `MealPlans` y `MealPlanItems`.

**Responsabilidades**:
- Listar planes con conteo de items (LEFT JOIN + COUNT)
- Obtener plan completo con items (JOIN a Dishes)
- Guardar plan con items en transacción
- Actualizar plan: DELETE + re-INSERT de MealPlanItems en transacción
- DELETE cascade automático en MealPlanItems (ON DELETE CASCADE)

---

## Capa 3: Services (lógica de negocio)

Reciben Repositories por inyección. Contienen las reglas de negocio y validaciones.

### CategoryService
**Propósito**: Orquesta la lógica de negocio de Categorías.

**Responsabilidades**:
- Validar nombre (requerido, max 100, único case-insensitive)
- Verificar integridad antes de eliminar (bloquear si tiene ingredientes)
- Delegar CRUD al Repository

### UnitService
**Propósito**: Orquesta la lógica de negocio de Unidades.

**Responsabilidades**:
- Validar nombre (max 50) y símbolo (requerido, max 10)
- Verificar unicidad de nombre
- Verificar integridad antes de eliminar
- Delegar CRUD al Repository

### IngredientService
**Propósito**: Orquesta la lógica de negocio de Ingredientes.

**Responsabilidades**:
- Validar nombre (requerido, max 100, único)
- Aplicar regla: `IsPerishable=true → RipeningDays > 0`
- Aplicar regla: `IsPerishable=false → RipeningDays = null`
- Verificar integridad antes de eliminar (en DishIngredients)
- Delegar CRUD al Repository

### DishService
**Propósito**: Orquesta la lógica de negocio de Platos.

**Responsabilidades**:
- Validar nombre (requerido, max 100)
- Validar MealType (valor válido del enum)
- Verificar al menos 1 ingrediente
- Verificar que no hay ingredientes duplicados
- Verificar cantidades > 0 para cada ingrediente
- Verificar integridad antes de eliminar (en MealPlanItems)
- Delegar guardado transaccional al Repository

### MealPlanService
**Propósito**: Orquesta la lógica de negocio de Planes de Comida.

**Responsabilidades**:
- Validar PlanType (Semanal/Mensual)
- Validar fechas: StartDate y EndDate requeridas, EndDate > StartDate
- Verificar al menos 1 item
- Verificar que fechas de items estén dentro del rango del plan
- Verificar que existan platos disponibles en BD
- Delegar guardado transaccional al Repository

### ShoppingListService
**Propósito**: Genera la lista de compras a partir de un plan de comidas.

**Responsabilidades**:
- Obtener todos los ingredientes del plan via JOIN (MealPlanItems → DishIngredients → Ingredients)
- Agregar y sumar cantidades por ingrediente
- Segmentar según tipo de plan:
  - Mensual: Listos (perecible ≤7d) / Comprar verdes (perecible >7d) / Otros (no perecible)
  - Semanal: lista única sin segmentación
- Generar `List<ShoppingListItem>` con secciones
- Delegar la query de agrupación al MealPlanRepository

### BackupService
**Propósito**: Gestiona la exportación e importación del archivo SQLite.

**Responsabilidades**:
- Exportar: obtener ruta del archivo `.db` y compartir via Share Sheet
- Importar: validar archivo seleccionado (es SQLite con las 6 tablas esperadas)
- Reemplazar BD actual con archivo importado (tras confirmación)
- Cerrar y re-abrir conexión a BD post-importación

### SeedDataService
**Propósito**: Carga datos semilla de comida peruana en la BD.

**Responsabilidades**:
- Verificar que la BD está vacía antes de insertar (para no duplicar)
- Insertar categorías base (Tubérculos, Cereales, Carnes, etc.)
- Insertar unidades base (kg, g, L, ml, un, tz, cda, cdta)
- Insertar ingredientes peruanos de muestra con sus FK
- Insertar platos típicos peruanos de muestra con sus ingredientes

---

## Capa 4: UI — Shared Widgets

Componentes visuales reutilizables en todos los features.

### AppScaffold
Scaffold base con AppBar configurado, tema Ñami.

### ConfirmDialog
Dialog de confirmación para operaciones destructivas (eliminar, importar backup).

### EmptyState
Widget para mostrar cuando una lista está vacía — icono + mensaje + botón opcional.

### SearchBarWidget
Barra de búsqueda con debounce para filtrado local en listas.

### LoadingSkeleton
Placeholder animado (shimmer) mientras carga datos de BD.

### BottomSheetPicker
Bottom sheet modal con lista buscable para seleccionar un item (unidad, categoría, ingrediente, plato).

### AppToast
Helper para mostrar Snackbar estandarizado (éxito/error/info) desde cualquier parte.

---

## Capa 4: UI — Feature Screens

Cada feature tiene: `ListScreen` + `FormScreen` (excepto ShoppingList y Settings).

| Feature | Screens |
|---------|---------|
| Home | `HomeScreen` — dashboard con cards de acceso rápido |
| Categories | `CategoryListScreen`, `CategoryFormScreen` |
| Units | `UnitListScreen`, `UnitFormScreen` |
| Ingredients | `IngredientListScreen`, `IngredientFormScreen` |
| Dishes | `DishListScreen`, `DishFormScreen` |
| MealPlans | `MealPlanListScreen`, `MealPlanFormScreen`, `MealPlanDetailScreen` |
| ShoppingList | `ShoppingListScreen` |
| Settings | `SettingsScreen` (tema, backup, about, seed data) |

---
