# Services — Ñami (ALIM-MOB)

**Fecha**: 2026-07-11

---

## Visión General de la Capa de Servicios

La capa Service actúa como la frontera de lógica de negocio. Ninguna regla de negocio existe fuera de esta capa (ni en UI ni en Repositories).

```
UI Screen
    │ llama provider
    ▼
Riverpod Provider
    │ llama service
    ▼
[XxxService]          ← reglas de negocio, validaciones
    │ llama repository
    ▼
[XxxRepository]       ← SQL puro
    │
    ▼
sqflite (SQLite)
```

---

## 1. CategoryService

**Rol**: Gestionar el ciclo de vida de categorías con sus reglas de negocio.

| Método | Input | Output | Reglas aplicadas |
|--------|-------|--------|-----------------|
| `getAll()` | — | `List<Category>` | — |
| `search(term)` | `String` | `List<Category>` | — |
| `create(name, description)` | `String, String?` | `ServiceResult<int>` | RN-001 (max 100), RN-002 (único case-insensitive) |
| `update(id, name, description)` | `int, String, String?` | `ServiceResult<void>` | RN-001, RN-002 (excluye id actual) |
| `delete(id)` | `int` | `ServiceResult<void>` | RN-003 (bloquea si tiene ingredientes) |

**Mensajes de error** (en español, para toast):
- `"El nombre es requerido"` — nombre vacío
- `"El nombre no puede superar 100 caracteres"`
- `"Ya existe una categoría con ese nombre"`
- `"No se puede eliminar: tiene ingredientes asociados"`

---

## 2. UnitService

**Rol**: Gestionar el ciclo de vida de unidades de medida.

| Método | Input | Output | Reglas aplicadas |
|--------|-------|--------|-----------------|
| `getAll()` | — | `List<Unit>` | — |
| `search(term)` | `String` | `List<Unit>` | — |
| `create(name, symbol)` | `String, String` | `ServiceResult<int>` | RN-001 (max 50/10), RN-002 (único) |
| `update(id, name, symbol)` | `int, String, String` | `ServiceResult<void>` | RN-001, RN-002 |
| `delete(id)` | `int` | `ServiceResult<void>` | RN-003 (bloquea si en ingredientes) |

**Mensajes de error**:
- `"El nombre es requerido"`
- `"El nombre no puede superar 50 caracteres"`
- `"El símbolo es requerido"`
- `"El símbolo no puede superar 10 caracteres"`
- `"Ya existe una unidad con ese nombre"`
- `"No se puede eliminar: está siendo usada por ingredientes"`

---

## 3. IngredientService

**Rol**: Gestionar ingredientes con lógica de perecibilidad.

| Método | Input | Output | Reglas aplicadas |
|--------|-------|--------|-----------------|
| `getAll()` | — | `List<Ingredient>` | — |
| `search(term)` | `String` | `List<Ingredient>` | — |
| `create(...)` | ver component-methods | `ServiceResult<int>` | RN-001 a RN-005 |
| `update(...)` | ver component-methods | `ServiceResult<void>` | RN-001 a RN-005 |
| `delete(id)` | `int` | `ServiceResult<void>` | RN-006 (bloquea si en platos) |

**Reglas de perecibilidad** (núcleo de la lógica):
```
if isPerishable == true && (ripeningDays == null || ripeningDays <= 0):
    → error: "Días de maduración debe ser mayor a 0 para ingredientes perecibles"

if isPerishable == false:
    → ripeningDays = null  (forzado automáticamente)
```

**Mensajes de error**:
- `"El nombre es requerido"`
- `"Ya existe un ingrediente con ese nombre"`
- `"Debe seleccionar una unidad"`
- `"Debe seleccionar una categoría"`
- `"Los días de maduración deben ser mayor a 0"`
- `"No se puede eliminar: está siendo usado en platos"`

---

## 4. DishService

**Rol**: Gestionar platos con su lista de ingredientes.

| Método | Input | Output | Reglas aplicadas |
|--------|-------|--------|-----------------|
| `getAll()` | — | `List<Dish>` | — |
| `search(term)` | `String` | `List<Dish>` | — |
| `getByIdWithIngredients(id)` | `int` | `Dish?` | — |
| `create(...)` | ver component-methods | `ServiceResult<int>` | RN-001 a RN-004 |
| `update(...)` | ver component-methods | `ServiceResult<void>` | RN-001 a RN-004 |
| `delete(id)` | `int` | `ServiceResult<void>` | RN-005 (bloquea si en planes) |

**Validaciones clave**:
```
if ingredients.isEmpty:
    → error: "El plato debe tener al menos un ingrediente"

if ingredients.any((i) => i.quantity <= 0):
    → error: "La cantidad de cada ingrediente debe ser mayor a 0"

if ingredients.map((i) => i.ingredientId).toSet().length != ingredients.length:
    → error: "No puede haber ingredientes duplicados en el plato"
```

---

## 5. MealPlanService

**Rol**: Gestionar planes de comida con sus items.

| Método | Input | Output | Reglas aplicadas |
|--------|-------|--------|-----------------|
| `getAll()` | — | `List<MealPlan>` | — |
| `getByIdWithItems(id)` | `int` | `MealPlan?` | — |
| `hasDishes()` | — | `bool` | Guard para UI |
| `create(...)` | ver component-methods | `ServiceResult<int>` | RN-001 a RN-005 |
| `update(...)` | ver component-methods | `ServiceResult<void>` | RN-001 a RN-005 |
| `delete(id)` | `int` | `ServiceResult<void>` | Sin restricción (cascade en BD) |

**Validaciones clave**:
```
if endDate <= startDate:
    → error: "La fecha fin debe ser posterior a la fecha inicio"

if items.isEmpty:
    → error: "El plan debe tener al menos un item"

if items.any((i) => i.date < startDate || i.date > endDate):
    → error: "Las fechas de los items deben estar dentro del rango del plan"
```

---

## 6. ShoppingListService

**Rol**: Algoritmo de generación y segmentación de la lista de compras.

### Flujo de generación

```
1. mealPlanRepository.getAggregatedIngredients(mealPlanId)
   → SQL: JOIN MealPlanItems → DishIngredients → Ingredients → Units → Categories
          WHERE mpi.MealPlanId = ?
          GROUP BY i.Id
          SELECT SUM(di.Quantity) AS TotalQuantity
   
2. if items.isEmpty:
   → return ShoppingListResult.empty()

3. Obtener planType del plan
   
4. if planType == Semanal:
   → ShoppingListResult(all: items, planType: semanal)
   
5. if planType == Mensual:
   → readyToEat  = items.where(isPerishable && ripeningDays <= 7)
   → buyGreen    = items.where(isPerishable && ripeningDays > 7)
   → other       = items.where(!isPerishable)
   → ShoppingListResult(readyToEat, buyGreen, other, planType: mensual)
```

**Ordenamiento**: Por `categoryName ASC`, luego `ingredientName ASC` dentro de cada sección.

---

## 7. BackupService

**Rol**: Operaciones de exportación e importación del archivo SQLite.

### Exportar
```
1. path_provider.getApplicationDocumentsDirectory()
2. Construir ruta: {dir}/ñami.db
3. share_plus.Share.shareXFiles([XFile(path)])
```

### Importar
```
1. file_picker.FilePicker.platform.pickFiles(type: FileType.any)
2. Validar: abrir el archivo como SQLite
3. Verificar existencia de tablas: Categories, Units, Ingredients, Dishes, DishIngredients, MealPlans, MealPlanItems
4. Si inválido → error: "El archivo seleccionado no es un backup válido de Ñami"
5. Si válido → ConfirmDialog: "Esto reemplazará TODOS tus datos actuales. ¿Continuar?"
6. Cerrar conexión BD actual
7. Copiar archivo importado sobre el .db actual
8. Re-inicializar DatabaseHelper
9. Toast: "Backup restaurado correctamente"
```

---

## 8. SeedDataService

**Rol**: Datos de muestra para facilitar el onboarding.

**Fuente de datos**: `aidlc-docs/assets/references/datos-alimentacion-recetas.md`

### Flujo
```
1. Verificar COUNT(*) en Categories → si > 0, retornar sin hacer nada
2. Ejecutar en transacción:
   a. INSERT 23 unidades
   b. INSERT 14 categorías
   c. INSERT 75 ingredientes con FK y datos de perecibilidad
   d. INSERT 30 platos con sus ingredientes (cada plato en su propia transacción)
3. Toast: "Datos de ejemplo cargados correctamente"
```

### Resumen de datos semilla
- **Unidades** (23): Kilogramo, Gramo, Libra, Onza, Litro, Mililitro, Unidad, Docena, Cucharada, Cucharadita, Taza, Diente, Atado, Lata, Botella, Paquete, Ramo, Pizca, Rodaja, Racimo, Frasco, Bolsa, Rama
- **Categorías** (14): Carnes, Aves, Pescados y Mariscos, Verduras, Frutas, Tubérculos, Lácteos, Abarrotes, Especias y Condimentos, Bebidas, Embutidos y Charcutería, Postres y Dulces, Panadería, Legumbres
- **Ingredientes** (75): Papa amarilla, Lomo fino, Corvina, Ají amarillo, Pollo, Cebolla, Ajo... (ver referencia completa)
- **Platos** (30): Ceviche Clásico, Lomo Saltado, Ají de Gallina, Causa Rellena, Papa a la Huancaína, Arroz con Pollo, Rocoto Relleno, Anticuchos, Suspiro Limeño, Seco de Res, Chupe de Camarones, Humita Dulce, Tacacho con Cecina, Carapulcra, Arroz con Mariscos, Juane de Pollo, Pachamanca, Cuy Chactado, Tallarines Verdes, Cau Cau, Chicharrón de Cerdo, Choros a la Chalaca, Tiradito, Pollo a la Brasa, Parihuela, Ocopa Arequipeña, Picante de Cuy, Mazamorra Morada, Picarones, Sancochado**Categorías**: Tubérculos y raíces, Cereales y granos, Carnes y aves, Mariscos y pescados, Verduras y hortalizas, Frutas, Lácteos y huevos, Especias y condimentos, Aceites y grasas, Legumbres

**Unidades**: Kilogramo (kg), Gramo (g), Litro (L), Mililitro (ml), Unidad (un), Taza (tz), Cucharada (cda), Cucharadita (cdta), Porción (por)

**Platos**: Lomo saltado, Ceviche de pescado, Ají de gallina, Arroz con leche, Papa a la huancaína

---

## Patrón ServiceResult

Todos los métodos de escritura devuelven `ServiceResult<T>` para comunicar éxito/error sin excepciones:

```dart
class ServiceResult<T> {
  final bool success;
  final T? data;          // datos en caso de éxito (ej: id insertado)
  final String? errorMessage;  // mensaje en español para toast

  const ServiceResult.success(this.data) : success = true, errorMessage = null;
  const ServiceResult.error(this.errorMessage) : success = false, data = null;
}
```

La UI lee `result.success` y muestra `result.errorMessage` en un toast si falla.

---
