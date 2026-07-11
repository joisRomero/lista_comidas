# Métodos de Componentes — Ñami (ALIM-MOB)

**Fecha**: 2026-07-11  
**Nota**: Las firmas aquí son de alto nivel. La lógica detallada de negocio se define en Functional Design (Construction).

---

## DatabaseHelper

```dart
class DatabaseHelper {
  // Singleton
  static DatabaseHelper get instance
  
  // Inicializa y retorna la BD (crea tablas si primera vez)
  Future<Database> get database
  
  // Ejecuta DDL completo (llamado en onCreate)
  Future<void> _createTables(Database db, int version)
  
  // Ejecuta migrations incrementales (llamado en onUpgrade)
  Future<void> _onUpgrade(Database db, int oldVersion, int newVersion)
  
  // Cierra la conexión
  Future<void> close()
}
```

---

## BaseRepository\<T\>

```dart
abstract class BaseRepository<T> {
  Future<List<T>> getAll()
  Future<T?> getById(int id)
  Future<int> insert(T entity)     // retorna el id insertado
  Future<int> update(T entity)     // retorna rows afectadas
  Future<int> delete(int id)       // retorna rows afectadas
  
  // Helper: Map<String,dynamic> → T (implementado por cada subclase)
  T fromMap(Map<String, dynamic> map)
  
  // Helper: T → Map<String,dynamic>
  Map<String, dynamic> toMap(T entity)
}
```

---

## CategoryRepository

```dart
class CategoryRepository extends BaseRepository<Category> {
  Future<List<Category>> getAll()
  Future<List<Category>> search(String term)
  Future<Category?> getById(int id)
  Future<bool> existsByName(String name, {int? excludeId})
  Future<int> countIngredients(int categoryId)   // para verificar integridad
  Future<int> insert(Category category)
  Future<int> update(Category category)
  Future<int> delete(int id)
}
```

---

## UnitRepository

```dart
class UnitRepository extends BaseRepository<Unit> {
  Future<List<Unit>> getAll()
  Future<List<Unit>> search(String term)
  Future<Unit?> getById(int id)
  Future<bool> existsByName(String name, {int? excludeId})
  Future<int> countIngredients(int unitId)        // para verificar integridad
  Future<int> insert(Unit unit)
  Future<int> update(Unit unit)
  Future<int> delete(int id)
}
```

---

## IngredientRepository

```dart
class IngredientRepository extends BaseRepository<Ingredient> {
  // Retorna ingredientes con datos de Unit y Category (JOIN)
  Future<List<Ingredient>> getAll()
  Future<List<Ingredient>> search(String term)   // JOIN + LIKE en nombre, categoría, unidad
  Future<Ingredient?> getById(int id)
  Future<bool> existsByName(String name, {int? excludeId})
  Future<int> countDishUses(int ingredientId)    // para verificar integridad
  Future<int> insert(Ingredient ingredient)
  Future<int> update(Ingredient ingredient)
  Future<int> delete(int id)
}
```

---

## DishRepository

```dart
class DishRepository extends BaseRepository<Dish> {
  // Retorna platos con conteo de ingredientes
  Future<List<Dish>> getAll()
  Future<List<Dish>> search(String term)
  Future<Dish?> getById(int id)
  
  // Retorna plato con lista completa de DishIngredients (JOIN a Ingredients + Units)
  Future<Dish?> getByIdWithIngredients(int id)
  
  Future<bool> existsByName(String name, {int? excludeId})
  Future<int> countMealPlanUses(int dishId)       // para verificar integridad
  
  // INSERT Dish + INSERT DishIngredients en transacción
  Future<int> saveWithIngredients(Dish dish, List<DishIngredient> ingredients)
  
  // UPDATE Dish + DELETE/re-INSERT DishIngredients en transacción
  Future<int> updateWithIngredients(Dish dish, List<DishIngredient> ingredients)
  
  Future<int> delete(int id)
}
```

---

## MealPlanRepository

```dart
class MealPlanRepository extends BaseRepository<MealPlan> {
  // Retorna planes con conteo de items
  Future<List<MealPlan>> getAll()
  Future<List<MealPlan>> search(String term)
  Future<MealPlan?> getById(int id)
  
  // Retorna plan completo con items y nombre de plato
  Future<MealPlan?> getByIdWithItems(int id)
  
  // INSERT MealPlan + INSERT MealPlanItems en transacción
  Future<int> saveWithItems(MealPlan plan, List<MealPlanItem> items)
  
  // UPDATE MealPlan + DELETE/re-INSERT MealPlanItems en transacción
  Future<int> updateWithItems(MealPlan plan, List<MealPlanItem> items)
  
  Future<int> delete(int id)
  
  // Query agrupada para lista de compras
  Future<List<ShoppingListItem>> getAggregatedIngredients(int mealPlanId)
}
```

---

## CategoryService

```dart
class CategoryService {
  CategoryService(this._repository)
  
  Future<List<Category>> getAll()
  Future<List<Category>> search(String term)
  
  // Valida + inserta. Lanza ServiceException si validación falla
  Future<ServiceResult<int>> create(String name, String? description)
  
  // Valida + actualiza
  Future<ServiceResult<void>> update(int id, String name, String? description)
  
  // Verifica integridad + elimina. Lanza ServiceException si tiene ingredientes
  Future<ServiceResult<void>> delete(int id)
}
```

---

## UnitService

```dart
class UnitService {
  UnitService(this._repository)
  
  Future<List<Unit>> getAll()
  Future<List<Unit>> search(String term)
  Future<ServiceResult<int>> create(String name, String symbol)
  Future<ServiceResult<void>> update(int id, String name, String symbol)
  Future<ServiceResult<void>> delete(int id)
}
```

---

## IngredientService

```dart
class IngredientService {
  IngredientService(this._repository)
  
  Future<List<Ingredient>> getAll()
  Future<List<Ingredient>> search(String term)
  
  Future<ServiceResult<int>> create({
    required String name,
    required int unitId,
    required int categoryId,
    required bool isPerishable,
    int? ripeningDays,
  })
  
  Future<ServiceResult<void>> update({
    required int id,
    required String name,
    required int unitId,
    required int categoryId,
    required bool isPerishable,
    int? ripeningDays,
  })
  
  Future<ServiceResult<void>> delete(int id)
}
```

---

## DishService

```dart
class DishService {
  DishService(this._repository)
  
  Future<List<Dish>> getAll()
  Future<List<Dish>> search(String term)
  Future<Dish?> getByIdWithIngredients(int id)
  
  Future<ServiceResult<int>> create({
    required String name,
    String? description,
    required MealType mealType,
    required List<DishIngredientInput> ingredients,  // {ingredientId, quantity}
  })
  
  Future<ServiceResult<void>> update({
    required int id,
    required String name,
    String? description,
    required MealType mealType,
    required List<DishIngredientInput> ingredients,
  })
  
  Future<ServiceResult<void>> delete(int id)
}
```

---

## MealPlanService

```dart
class MealPlanService {
  MealPlanService(this._repository, this._dishRepository)
  
  Future<List<MealPlan>> getAll()
  Future<MealPlan?> getByIdWithItems(int id)
  Future<bool> hasDishes()    // verifica que existen platos en BD
  
  Future<ServiceResult<int>> create({
    required PlanType planType,
    required DateTime startDate,
    required DateTime endDate,
    required List<MealPlanItemInput> items,  // {dishId, date, mealTime}
  })
  
  Future<ServiceResult<void>> update({
    required int id,
    required PlanType planType,
    required DateTime startDate,
    required DateTime endDate,
    required List<MealPlanItemInput> items,
  })
  
  Future<ServiceResult<void>> delete(int id)
}
```

---

## ShoppingListService

```dart
class ShoppingListService {
  ShoppingListService(this._mealPlanRepository)
  
  // Genera la lista de compras completa para un plan
  Future<ShoppingListResult> generate(int mealPlanId)
  
  // Aplica segmentación según tipo de plan
  ShoppingListResult _segment(List<ShoppingListItem> items, PlanType planType)
}

class ShoppingListResult {
  final List<ShoppingListItem> readyToEat;   // perecible ≤7d (solo mensual)
  final List<ShoppingListItem> buyGreen;     // perecible >7d (solo mensual)
  final List<ShoppingListItem> other;        // no perecible (solo mensual)
  final List<ShoppingListItem> all;          // todos (semanal)
  final PlanType planType;
}
```

---

## BackupService

```dart
class BackupService {
  BackupService(this._databaseHelper)
  
  // Obtiene la ruta del archivo .db y lanza Share Sheet
  Future<void> exportBackup()
  
  // Valida el archivo seleccionado y lo importa
  Future<ServiceResult<void>> importBackup(String filePath)
  
  // Verifica que el archivo tiene las 6 tablas esperadas
  Future<bool> _validateBackupFile(String filePath)
}
```

---

## SeedDataService

```dart
class SeedDataService {
  SeedDataService(this._db)
  
  // Verifica si la BD está vacía y carga los datos semilla
  Future<ServiceResult<void>> loadSeedData()
  
  // Verifica si ya hay datos (evitar duplicados)
  Future<bool> _isDatabaseEmpty()
}
```

---

## Modelos de Dominio

```dart
class Category { int id; String name; String? description; String createdAt; }

class Unit { int id; String name; String symbol; String createdAt; }

class Ingredient {
  int id; String name; int unitId; int categoryId;
  bool isPerishable; int? ripeningDays; String createdAt;
  // Datos de JOIN (nullable en insert/update)
  String? unitName; String? unitSymbol; String? categoryName;
}

class Dish {
  int id; String name; String? description; MealType mealType; String createdAt;
  int? ingredientCount;                    // de LEFT JOIN en listado
  List<DishIngredient>? dishIngredients;   // de JOIN en detalle
}

class DishIngredient {
  int id; int dishId; int ingredientId; double quantity;
  String? ingredientName; String? unitSymbol;
}

class MealPlan {
  int id; PlanType planType; String startDate; String endDate; String createdAt;
  int? itemCount;
  List<MealPlanItem>? items;
}

class MealPlanItem {
  int id; int mealPlanId; int dishId; String date; MealTime mealTime;
  String? dishName;
}

class ShoppingListItem {
  int ingredientId; String ingredientName; double totalQuantity;
  String unitSymbol; String categoryName; bool isPerishable; int? ripeningDays;
}

// Value objects / helpers
class ServiceResult<T> { bool success; T? data; String? errorMessage; }
class DishIngredientInput { int ingredientId; double quantity; }
class MealPlanItemInput { int dishId; DateTime date; MealTime mealTime; }
```

---

## Enumeraciones

```dart
enum MealType { desayuno, almuerzo, cena, snack, postre }
enum MealTime { desayuno, mediaManana, almuerzo, merienda, cena }
enum PlanType { semanal, mensual }
```

---
