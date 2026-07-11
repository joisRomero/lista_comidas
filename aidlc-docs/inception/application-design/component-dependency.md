# Dependencias de Componentes — Ñami (ALIM-MOB)

**Fecha**: 2026-07-11

---

## 1. Diagrama de Dependencias

```
┌────────────────────────────────────────────────────────────────┐
│                         UI Layer                               │
│  HomeScreen  CategoryListScreen  IngredientFormScreen  ...     │
│         └──────────────────────────────────────────┐          │
│                    Shared Widgets                   │          │
│  ConfirmDialog  EmptyState  BottomSheetPicker  ...  │          │
└────────────────────────────────────┬───────────────┘          │
                                     │ ref.watch / ref.read
┌────────────────────────────────────▼───────────────────────────┐
│                      Providers (Riverpod)                      │
│  categoriesProvider  dishesProvider  shoppingListProvider  ... │
└─────┬──────┬──────┬──────┬──────┬──────┬──────┬───────────────┘
      │      │      │      │      │      │      │  llaman a:
┌─────▼──┐ ┌─▼────┐ ┌▼───────┐ ┌─▼────┐ ┌▼──────────────┐ ┌──▼──────┐
│Category│ │Unit  │ │Ingredi-│ │Dish  │ │MealPlan       │ │Backup  │
│Service │ │Service│ │ent     │ │Service│ │Service        │ │Service │
│        │ │       │ │Service │ │       │ │               │ │        │
└───┬────┘ └──┬───┘ └───┬────┘ └──┬───┘ └──────┬────────┘ └───┬────┘
    │          │          │         │             │               │
    │          │          │    ┌────▼───┐    ┌───▼────────┐     │
    │          │          │    │Shopping│    │MealPlan    │     │
    │          │          │    │List    │    │Repository  │     │
    │          │          │    │Service │    │            │     │
    │          │          │    └───┬────┘    └───┬────────┘     │
    │          │          │        │              │               │
┌───▼──┐ ┌────▼──┐ ┌──────▼──┐    │    ┌─────────┘              │
│Categ-│ │Unit   │ │Ingredi- │    │    │                        │
│ory   │ │Reposi-│ │ent      │    │    │                        │
│Reposi│ │tory   │ │Reposit- │    │    │                        │
│tory  │ │       │ │ory      │    │    │                        │
└──┬───┘ └───┬───┘ └────┬────┘    │    │         ┌──────────────┘
   │          │           │        │    │         │  path_provider
   └──────────┴───────────┴────────┴────┘         │  file_picker
                          │                       │  share_plus
                    ┌─────▼───────────────────┐   │
                    │      DatabaseHelper      ◄───┘
                    │      (sqflite)           │
                    └─────────────────────────┘
```

---

## 2. Matriz de Dependencias

| Componente | Depende de |
|-----------|-----------|
| **HomeScreen** | `categoriesProvider`, `unitsProvider`, `ingredientsProvider`, `dishesProvider`, `mealPlansProvider` (conteos) |
| **CategoryListScreen** | `categoriesProvider` |
| **CategoryFormScreen** | `categoriesProvider` (invalidar tras CRUD) |
| **UnitListScreen** | `unitsProvider` |
| **UnitFormScreen** | `unitsProvider` |
| **IngredientListScreen** | `ingredientsProvider` |
| **IngredientFormScreen** | `unitsProvider`, `categoriesProvider`, `ingredientsProvider` |
| **DishListScreen** | `dishesProvider` |
| **DishFormScreen** | `ingredientsProvider`, `dishesProvider` |
| **MealPlanListScreen** | `mealPlansProvider` |
| **MealPlanFormScreen** | `dishesProvider`, `mealPlansProvider` |
| **MealPlanDetailScreen** | `mealPlanDetailProvider` (con id) |
| **ShoppingListScreen** | `shoppingListProvider` (con mealPlanId) |
| **SettingsScreen** | `themeProvider`, `BackupService`, `SeedDataService` |
| **BottomSheetPicker** | Provider del recurso a seleccionar (passed as param) |
| — | — |
| **categoriesProvider** | `CategoryService` |
| **unitsProvider** | `UnitService` |
| **ingredientsProvider** | `IngredientService` |
| **dishesProvider** | `DishService` |
| **mealPlansProvider** | `MealPlanService` |
| **shoppingListProvider** | `ShoppingListService` |
| — | — |
| **CategoryService** | `CategoryRepository` |
| **UnitService** | `UnitRepository` |
| **IngredientService** | `IngredientRepository` |
| **DishService** | `DishRepository` |
| **MealPlanService** | `MealPlanRepository`, `DishRepository` (hasDishes check) |
| **ShoppingListService** | `MealPlanRepository` |
| **BackupService** | `DatabaseHelper`, `share_plus`, `file_picker`, `path_provider` |
| **SeedDataService** | `CategoryRepository`, `UnitRepository`, `IngredientRepository`, `DishRepository` |
| — | — |
| **CategoryRepository** | `DatabaseHelper` |
| **UnitRepository** | `DatabaseHelper` |
| **IngredientRepository** | `DatabaseHelper` |
| **DishRepository** | `DatabaseHelper` |
| **MealPlanRepository** | `DatabaseHelper` |

---

## 3. Flujo de Datos — Operación CRUD Típica (Crear Categoría)

```
UI: CategoryFormScreen
  → usuario presiona "Guardar"
  → ref.read(categoryServiceProvider).create(name, description)
      → CategoryService.create()
          → _repository.existsByName(name)       // verificar unicidad
          → if existe → return ServiceResult.error("Ya existe...")
          → _repository.insert(category)         // INSERT SQL
          → return ServiceResult.success(id)
  → if result.success:
      → ref.invalidate(categoriesProvider)       // refrescar lista
      → AppToast.show("Categoría creada correctamente")
      → Navigator.pop()
  → else:
      → AppToast.showError(result.errorMessage)
```

---

## 4. Flujo de Datos — Lista de Compras

```
UI: MealPlanDetailScreen
  → usuario presiona "Generar Lista de Compras"
  → Navigator.push(ShoppingListScreen(mealPlanId: id))

UI: ShoppingListScreen
  → ref.watch(shoppingListProvider(mealPlanId))
      → ShoppingListService.generate(mealPlanId)
          → MealPlanRepository.getById(mealPlanId) // obtener planType
          → MealPlanRepository.getAggregatedIngredients(mealPlanId)
              SQL: JOIN MealPlanItems→DishIngredients→Ingredients→Units→Categories
                   GROUP BY ingredientId, SUM(quantity)
          → ShoppingListService._segment(items, planType)
              if semanal: return ShoppingListResult(all: items)
              if mensual: segmentar en 3 listas
          → return ShoppingListResult
  → UI renderiza secciones según planType
```

---

## 5. Flujo de Datos — Backup Import

```
UI: SettingsScreen
  → usuario presiona "Importar backup"
  → FilePicker selecciona archivo
  → BackupService.importBackup(filePath)
      → _validateBackupFile(filePath)       // abrir DB, verificar tablas
      → if inválido → ServiceResult.error("Archivo no válido")
      → if válido → ConfirmDialog en UI (confirmación del usuario)
          → DatabaseHelper.close()
          → File.copy(filePath → dbPath)
          → DatabaseHelper.reinitialize()
          → return ServiceResult.success(null)
  → Toast: "Backup restaurado correctamente"
  → ref.invalidate(allProviders)  // refrescar toda la app
```

---

## 6. Flujo de Riverpod Providers

```dart
// Providers de estado (AsyncNotifierProvider para listas con operaciones CRUD)

@riverpod
class CategoriesNotifier extends _$CategoriesNotifier {
  @override
  Future<List<Category>> build() async {
    return ref.read(categoryServiceProvider).getAll();
  }
  
  Future<void> create(String name, String? description) async {
    final result = await ref.read(categoryServiceProvider).create(name, description);
    if (result.success) ref.invalidateSelf();
    // La UI lee el result para mostrar toast
  }
}

// Provider simple (read-only) para selects en formularios
@riverpod
Future<List<Unit>> units(UnitsRef ref) async {
  return ref.read(unitServiceProvider).getAll();
}

// Provider con parámetro (detalle del plan)
@riverpod
Future<MealPlan?> mealPlanDetail(MealPlanDetailRef ref, int id) async {
  return ref.read(mealPlanServiceProvider).getByIdWithItems(id);
}

// Provider con parámetro (lista de compras)
@riverpod
Future<ShoppingListResult> shoppingList(ShoppingListRef ref, int mealPlanId) async {
  return ref.read(shoppingListServiceProvider).generate(mealPlanId);
}
```

---

## 7. Inyección de Dependencias (Riverpod)

```dart
// database_provider.dart
@riverpod
DatabaseHelper databaseHelper(DatabaseHelperRef ref) => DatabaseHelper.instance;

// repository_providers.dart
@riverpod
CategoryRepository categoryRepository(CategoryRepositoryRef ref) =>
    CategoryRepository(ref.watch(databaseHelperProvider));

// service_providers.dart
@riverpod
CategoryService categoryService(CategoryServiceRef ref) =>
    CategoryService(ref.watch(categoryRepositoryProvider));

// La UI consume:
ref.read(categoryServiceProvider).create(...)
ref.watch(categoriesProvider)   // AsyncValue<List<Category>>
```

---
