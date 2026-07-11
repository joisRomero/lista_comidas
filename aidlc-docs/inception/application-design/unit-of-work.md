# Unidades de Trabajo — Ñami (ALIM-MOB)

**Fecha**: 2026-07-11  
**Arquitectura**: Monolito móvil (Single-Repo Flutter)  
**Total de unidades**: 8

---

## Modelo de descomposición

Ñami es una app Flutter monolítica — no hay microservicios ni repos separados. Las unidades de trabajo son **módulos funcionales** dentro de la misma base de código, cada uno completamente implementable de forma independiente (siempre que sus dependencias previas estén resueltas).

Cada unidad produce: modelos, repository, service, providers Riverpod, screens (list + form), y sus tests correspondientes de la QA Matrix.

---

## Unidad 1 — ALIM-MOB-001: Infraestructura Base

| Atributo | Valor |
|----------|-------|
| **HU** | ALIM-MOB-001 |
| **Epic** | Infraestructura Mobile |
| **Capa principal** | core/ (database, theme, navigation, shared widgets) |
| **Estimación** | M |
| **Prioridad** | Crítica — bloqueante para todas las demás |
| **Depende de** | Ninguna |
| **Bloquea** | Todas (U2–U8) |

**Entregables**:
- `DatabaseHelper` con DDL completo (6 tablas + índices) y sistema de migrations
- `BaseRepository<T>` genérico
- Bottom Navigation Bar con 5 tabs
- `app_theme.dart` con paleta Ñami (#53D669, #53D6AB, #53C0D6) + Material 3
- Shared widgets: `ConfirmDialog`, `EmptyState`, `SearchBarWidget`, `LoadingSkeleton`, `BottomSheetPicker`, `AppToast`
- Riverpod `ProviderScope` configurado en `main.dart`
- Arquitectura i18n (`AppLocalizations`) preparada — solo `es`
- `SeedDataService` — botón "Cargar datos de ejemplo" en Settings (23 unidades, 14 categorías, 75 ingredientes, 30 platos peruanos)
- Toggle tema claro/oscuro en Settings con `SharedPreferences`

---

## Unidad 2 — ALIM-MOB-002: CRUD Categorías

| Atributo | Valor |
|----------|-------|
| **HU** | ALIM-MOB-002 |
| **Epic** | Gestión de Catálogos |
| **Capa principal** | features/categories/ + core/repositories/category_repository.dart + core/services/category_service.dart |
| **Estimación** | S |
| **Prioridad** | Alta |
| **Depende de** | U1 |
| **Bloquea** | U4 (Ingredientes necesita categorías) |

**Entregables**:
- `Category` model
- `CategoryRepository` (getAll, search, existsByName, countIngredients, CRUD)
- `CategoryService` (validaciones RN-001/002/003, mensajes en español)
- Riverpod provider `categoriesNotifierProvider`
- `CategoryListScreen` (lista + búsqueda + pull-to-refresh + swipe-delete)
- `CategoryFormScreen` (crear/editar con validación en tiempo real)
- Tests: QA-002-001 a QA-002-012

---

## Unidad 3 — ALIM-MOB-003: CRUD Unidades de Medida

| Atributo | Valor |
|----------|-------|
| **HU** | ALIM-MOB-003 |
| **Epic** | Gestión de Catálogos |
| **Capa principal** | features/units/ + core/repositories/unit_repository.dart + core/services/unit_service.dart |
| **Estimación** | S |
| **Prioridad** | Alta |
| **Depende de** | U1 |
| **Bloquea** | U4 (Ingredientes necesita unidades) |
| **Paralelo con** | U2 (sin dependencia entre sí) |

**Entregables**:
- `Unit` model
- `UnitRepository` (getAll, search, existsByName, countIngredients, CRUD)
- `UnitService` (validaciones RN-001/002/003, símbolo requerido)
- Riverpod provider `unitsNotifierProvider`
- `UnitListScreen` (lista con badge de símbolo + búsqueda + swipe-delete)
- `UnitFormScreen` (crear/editar con campos nombre + símbolo)
- Tests: QA-003-001 a QA-003-006

---

## Unidad 4 — ALIM-MOB-004: CRUD Ingredientes

| Atributo | Valor |
|----------|-------|
| **HU** | ALIM-MOB-004 |
| **Epic** | Gestión de Ingredientes |
| **Capa principal** | features/ingredients/ + core/repositories/ingredient_repository.dart + core/services/ingredient_service.dart |
| **Estimación** | M |
| **Prioridad** | Alta |
| **Depende de** | U2 (categorías), U3 (unidades) |
| **Bloquea** | U5 (Platos necesita ingredientes) |

**Entregables**:
- `Ingredient` model (con campos de JOIN: unitName, unitSymbol, categoryName)
- `IngredientRepository` (getAll con JOIN, search con JOIN, existsByName, countDishUses, CRUD)
- `IngredientService` (reglas perecibilidad: RN-004/005, integridad: RN-006)
- Riverpod providers: `ingredientsNotifierProvider`, `ingredientByIdProvider`
- `IngredientListScreen` (badges de categoría + unidad + días maduración)
- `IngredientFormScreen` (BottomSheetPicker para unidad y categoría, campo condicional RipeningDays)
- Tests: QA-004-001 a QA-004-009

---

## Unidad 5 — ALIM-MOB-005: CRUD Platos

| Atributo | Valor |
|----------|-------|
| **HU** | ALIM-MOB-005 |
| **Epic** | Gestión de Platos |
| **Capa principal** | features/dishes/ + core/repositories/dish_repository.dart + core/services/dish_service.dart |
| **Estimación** | M |
| **Prioridad** | Alta |
| **Depende de** | U4 (ingredientes) |
| **Bloquea** | U6 (Planes necesita platos) |

**Entregables**:
- `Dish` model + `DishIngredient` model + `DishIngredientInput` value object
- `DishRepository` (getAll con COUNT, getByIdWithIngredients con JOIN, saveWithIngredients en transacción, updateWithIngredients en transacción, countMealPlanUses)
- `DishService` (≥1 ingrediente, cantidades >0, sin duplicados, integridad con planes)
- Riverpod providers: `dishesNotifierProvider`, `dishByIdProvider`
- `DishListScreen` (badge de MealType + conteo de ingredientes)
- `DishFormScreen` (lista dinámica de ingredientes con BottomSheetPicker + campo cantidad)
- Tests: QA-005-001 a QA-005-009

---

## Unidad 6 — ALIM-MOB-006: Planes de Comida

| Atributo | Valor |
|----------|-------|
| **HU** | ALIM-MOB-006 |
| **Epic** | Planificación de Comidas |
| **Capa principal** | features/meal_plans/ + core/repositories/meal_plan_repository.dart + core/services/meal_plan_service.dart |
| **Estimación** | L |
| **Prioridad** | Alta |
| **Depende de** | U5 (platos) |
| **Bloquea** | U7 (Lista de compras necesita planes) |

**Entregables**:
- `MealPlan` model + `MealPlanItem` model + `MealPlanItemInput` value object
- `MealPlanRepository` (getAll con COUNT, getByIdWithItems con JOIN, saveWithItems en transacción, updateWithItems en transacción)
- `MealPlanService` (validaciones fechas, ≥1 item, items dentro de rango, guard hasDishes)
- Riverpod providers: `mealPlansNotifierProvider`, `mealPlanDetailProvider(id)`
- `MealPlanListScreen` (badge PlanType + fechas + conteo items)
- `MealPlanFormScreen` (DatePickers, Picker MealTime de 5 valores, BottomSheetPicker platos, lista dinámica de items)
- `MealPlanDetailScreen` (items agrupados por fecha)
- Tests: QA-006-001 a QA-006-008

---

## Unidad 7 — ALIM-MOB-007: Lista de Compras + PDF

| Atributo | Valor |
|----------|-------|
| **HU** | ALIM-MOB-007 |
| **Epic** | Planificación de Comidas |
| **Capa principal** | features/shopping_list/ + core/services/shopping_list_service.dart |
| **Estimación** | M |
| **Prioridad** | Alta |
| **Depende de** | U6 (planes con items) |
| **Bloquea** | Nada |
| **Paralelo con** | U8 (sin dependencia entre sí) |

**Entregables**:
- `ShoppingListItem` model + `ShoppingListResult` value object
- `ShoppingListService.generate()` — algoritmo de agrupación + segmentación (semanal/mensual)
- `MealPlanRepository.getAggregatedIngredients()` — query JOIN con SUM y GROUP BY
- Riverpod provider `shoppingListProvider(mealPlanId)`
- `ShoppingListScreen` (secciones colapsables, botones regenerar y exportar PDF)
- Generación de PDF local (paquetes `pdf` + `printing`) con Share Sheet nativo
- Tests: QA-007-001 a QA-007-008

---

## Unidad 8 — ALIM-MOB-008: Backup y Restauración

| Atributo | Valor |
|----------|-------|
| **HU** | ALIM-MOB-008 |
| **Epic** | Infraestructura Mobile |
| **Capa principal** | features/settings/ + core/services/backup_service.dart |
| **Estimación** | S |
| **Prioridad** | Media |
| **Depende de** | U1 (DatabaseHelper) |
| **Bloquea** | Nada |
| **Paralelo con** | U7 (sin dependencia entre sí) |

**Entregables**:
- `BackupService` (exportar .db via Share Sheet, importar con validación de tablas, re-init BD)
- `SettingsScreen` completa (ya iniciada en U1, se expande con backup)
- Opción "Backup de datos" con export + import + ConfirmDialog
- Validación de archivo importado (6 tablas requeridas)
- Advertencia de desinstalación visible en Settings
- Tests: QA-008-001 a QA-008-005

---

## Resumen

| Unidad | HU | Estimación | Depende de | Bloquea |
|--------|----|-----------|-----------|---------|
| U1 | MOB-001 | M | — | U2,U3,U4,U5,U6,U7,U8 |
| U2 | MOB-002 | S | U1 | U4 |
| U3 | MOB-003 | S | U1 | U4 |
| U4 | MOB-004 | M | U2,U3 | U5 |
| U5 | MOB-005 | M | U4 | U6 |
| U6 | MOB-006 | L | U5 | U7 |
| U7 | MOB-007 | M | U6 | — |
| U8 | MOB-008 | S | U1 | — |
