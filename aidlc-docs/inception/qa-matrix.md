# QA Matrix — Ñami (ALIM-MOB)

**Versión**: 1.0 | **Fecha**: 2026-07-11 | **Estado**: Pendiente de aprobación

> **Nota de adaptación**: App Flutter standalone sin API REST. Las columnas "Endpoint" mapean a operaciones de Service/Repository. Los layers son:
> - **Unit** — lógica de Service testeada de forma aislada (flutter_test, mocks)
> - **Widget** — comportamiento de pantalla/formulario (flutter_test + WidgetTester)
> - **Integration** — flujo completo con BD SQLite real en dispositivo (integration_test)

---

## 1. Traceability Table

### ALIM-MOB-001: Configuración Base

| HU ID | Operación | QA ID | Descripción | Layer | Tipo | Precondiciones | Test Data | Prioridad | Estado |
|-------|-----------|-------|-------------|-------|------|---------------|-----------|-----------|--------|
| MOB-001 | DatabaseHelper.init | QA-001-001 | BD se inicializa con 6 tablas en primera ejecución | Unit | Happy | App instalada, BD vacía | — | Alta | Pendiente |
| MOB-001 | DatabaseHelper.init | QA-001-002 | Migration de v1→v2 ejecuta sin errores | Unit | Happy | BD en versión 1 | — | Alta | Pendiente |
| MOB-001 | SeedDataService.load | QA-001-003 | Cargar datos semilla inserta categorías, unidades, ingredientes y platos | Integration | Happy | BD vacía | TD-001 | Media | Pendiente |
| MOB-001 | SeedDataService.load | QA-001-004 | Cargar datos semilla dos veces no duplica datos | Unit | Edge | BD con datos semilla ya cargados | TD-001 | Media | Pendiente |
| MOB-001 | BottomNavigation | QA-001-005 | Las 5 tabs navegan a sus pantallas correctas | Widget | Happy | App iniciada | — | Alta | Pendiente |
| MOB-001 | ThemeProvider | QA-001-006 | Toggle de tema claro/oscuro persiste tras reinicio | Integration | Happy | App iniciada en tema claro | — | Media | Pendiente |


### ALIM-MOB-002: CRUD Categorías

| HU ID | Operación | QA ID | Descripción | Layer | Tipo | Precondiciones | Test Data | Prioridad | Estado |
|-------|-----------|-------|-------------|-------|------|---------------|-----------|-----------|--------|
| MOB-002 | CategoryService.create | QA-002-001 | Crear categoría con datos válidos → retorna id | Unit | Happy | — | TD-002 | Alta | Pendiente |
| MOB-002 | CategoryService.create | QA-002-002 | Nombre vacío → error "El nombre es requerido" | Unit | Error | — | — | Alta | Pendiente |
| MOB-002 | CategoryService.create | QA-002-003 | Nombre > 100 chars → error de longitud | Unit | Error | — | TD-003 | Media | Pendiente |
| MOB-002 | CategoryService.create | QA-002-004 | Nombre duplicado (case-insensitive) → error unicidad | Unit | Error | Categoría "Verduras" existe | TD-002 | Alta | Pendiente |
| MOB-002 | CategoryService.update | QA-002-005 | Editar categoría existente → cambios persistidos | Unit | Happy | Categoría con id=1 existe | TD-004 | Alta | Pendiente |
| MOB-002 | CategoryService.delete | QA-002-006 | Eliminar categoría sin ingredientes → OK | Unit | Happy | Categoría sin hijos | — | Alta | Pendiente |
| MOB-002 | CategoryService.delete | QA-002-007 | Eliminar categoría con ingredientes → error integridad | Unit | Error | Categoría con ≥1 ingrediente | TD-005 | Alta | Pendiente |
| MOB-002 | CategoryListScreen | QA-002-008 | Lista muestra categorías ordenadas alfabéticamente | Widget | Happy | 3 categorías en BD | TD-006 | Alta | Pendiente |
| MOB-002 | CategoryListScreen | QA-002-009 | Lista vacía muestra EmptyState widget | Widget | Edge | BD sin categorías | — | Media | Pendiente |
| MOB-002 | CategoryListScreen | QA-002-010 | Búsqueda filtra resultados por nombre | Widget | Happy | 3 categorías en BD | TD-006 | Alta | Pendiente |
| MOB-002 | CategoryFormScreen | QA-002-011 | Formulario de creación muestra errores al enviar vacío | Widget | Error | Pantalla de creación abierta | — | Alta | Pendiente |
| MOB-002 | CategoryFormScreen | QA-002-012 | Formulario de edición precarga datos existentes | Widget | Happy | Categoría con id=1 existe | TD-004 | Alta | Pendiente |


### ALIM-MOB-003: CRUD Unidades

| HU ID | Operación | QA ID | Descripción | Layer | Tipo | Precondiciones | Test Data | Prioridad | Estado |
|-------|-----------|-------|-------------|-------|------|---------------|-----------|-----------|--------|
| MOB-003 | UnitService.create | QA-003-001 | Crear unidad con nombre y símbolo válidos | Unit | Happy | — | TD-007 | Alta | Pendiente |
| MOB-003 | UnitService.create | QA-003-002 | Símbolo vacío → error "El símbolo es requerido" | Unit | Error | — | — | Alta | Pendiente |
| MOB-003 | UnitService.create | QA-003-003 | Símbolo > 10 chars → error longitud | Unit | Error | — | TD-008 | Media | Pendiente |
| MOB-003 | UnitService.create | QA-003-004 | Nombre duplicado → error unicidad | Unit | Error | Unidad "Kilogramo" existe | TD-007 | Alta | Pendiente |
| MOB-003 | UnitService.delete | QA-003-005 | Eliminar unidad con ingredientes → error integridad | Unit | Error | Unidad usada en ≥1 ingrediente | TD-009 | Alta | Pendiente |
| MOB-003 | UnitListScreen | QA-003-006 | Lista muestra nombre + símbolo (badge) | Widget | Happy | 2 unidades en BD | TD-007 | Alta | Pendiente |

### ALIM-MOB-004: CRUD Ingredientes

| HU ID | Operación | QA ID | Descripción | Layer | Tipo | Precondiciones | Test Data | Prioridad | Estado |
|-------|-----------|-------|-------------|-------|------|---------------|-----------|-----------|--------|
| MOB-004 | IngredientService.create | QA-004-001 | Crear ingrediente perecible con días válidos | Unit | Happy | Unidad y categoría existen | TD-010 | Alta | Pendiente |
| MOB-004 | IngredientService.create | QA-004-002 | Crear ingrediente no perecible → RipeningDays=null | Unit | Happy | Unidad y categoría existen | TD-011 | Alta | Pendiente |
| MOB-004 | IngredientService.create | QA-004-003 | Perecible con días=0 → error "días debe ser > 0" | Unit | Error | — | TD-012 | Alta | Pendiente |
| MOB-004 | IngredientService.create | QA-004-004 | Perecible sin días → error días requeridos | Unit | Error | — | — | Alta | Pendiente |
| MOB-004 | IngredientService.create | QA-004-005 | Nombre duplicado → error unicidad | Unit | Error | Ingrediente "Tomate" existe | TD-010 | Alta | Pendiente |
| MOB-004 | IngredientService.delete | QA-004-006 | Eliminar ingrediente en uso en plato → error integridad | Unit | Error | Ingrediente en ≥1 DishIngredient | TD-013 | Alta | Pendiente |
| MOB-004 | IngredientListScreen | QA-004-007 | Lista muestra badges de categoría y unidad | Widget | Happy | 3 ingredientes en BD | TD-010 | Media | Pendiente |
| MOB-004 | IngredientFormScreen | QA-004-008 | Campo "Días maduración" aparece solo si perecible=true | Widget | Happy | Pantalla de creación abierta | — | Alta | Pendiente |
| MOB-004 | IngredientFormScreen | QA-004-009 | BottomSheetPicker de unidades muestra resultados buscables | Widget | Happy | ≥1 unidad en BD | TD-007 | Alta | Pendiente |


### ALIM-MOB-005: CRUD Platos

| HU ID | Operación | QA ID | Descripción | Layer | Tipo | Precondiciones | Test Data | Prioridad | Estado |
|-------|-----------|-------|-------------|-------|------|---------------|-----------|-----------|--------|
| MOB-005 | DishService.create | QA-005-001 | Crear plato con 2 ingredientes válidos → transacción OK | Unit | Happy | 2 ingredientes en BD | TD-014 | Alta | Pendiente |
| MOB-005 | DishService.create | QA-005-002 | Plato sin ingredientes → error "al menos un ingrediente" | Unit | Error | — | — | Alta | Pendiente |
| MOB-005 | DishService.create | QA-005-003 | Ingrediente con cantidad=0 → error cantidad | Unit | Error | 1 ingrediente en BD | TD-015 | Alta | Pendiente |
| MOB-005 | DishService.create | QA-005-004 | Ingrediente duplicado en el mismo plato → error | Unit | Error | 1 ingrediente en BD | TD-016 | Alta | Pendiente |
| MOB-005 | DishService.update | QA-005-005 | Editar plato actualiza Dish + reemplaza DishIngredients | Unit | Happy | Plato id=1 existe | TD-017 | Alta | Pendiente |
| MOB-005 | DishService.delete | QA-005-006 | Eliminar plato en uso en plan → error integridad | Unit | Error | Plato en ≥1 MealPlanItem | TD-018 | Alta | Pendiente |
| MOB-005 | DishService.delete | QA-005-007 | Eliminar plato libre → cascade elimina DishIngredients | Unit | Happy | Plato sin planes asociados | TD-014 | Alta | Pendiente |
| MOB-005 | DishFormScreen | QA-005-008 | Formulario permite agregar y quitar ingredientes dinámicamente | Widget | Happy | ≥2 ingredientes en BD | TD-014 | Alta | Pendiente |
| MOB-005 | DishFormScreen | QA-005-009 | Picker de MealType muestra 5 opciones (español) | Widget | Happy | Pantalla de creación abierta | — | Media | Pendiente |

### ALIM-MOB-006: Planes de Comida

| HU ID | Operación | QA ID | Descripción | Layer | Tipo | Precondiciones | Test Data | Prioridad | Estado |
|-------|-----------|-------|-------------|-------|------|---------------|-----------|-----------|--------|
| MOB-006 | MealPlanService.create | QA-006-001 | Crear plan semanal con items válidos → transacción OK | Unit | Happy | ≥1 plato en BD | TD-019 | Alta | Pendiente |
| MOB-006 | MealPlanService.create | QA-006-002 | EndDate ≤ StartDate → error fecha | Unit | Error | — | TD-020 | Alta | Pendiente |
| MOB-006 | MealPlanService.create | QA-006-003 | Item con fecha fuera del rango del plan → error | Unit | Error | — | TD-021 | Alta | Pendiente |
| MOB-006 | MealPlanService.create | QA-006-004 | Plan sin items → error "al menos un item" | Unit | Error | — | — | Alta | Pendiente |
| MOB-006 | MealPlanService.hasDishes | QA-006-005 | Sin platos en BD → retorna false | Unit | Edge | BD sin platos | — | Alta | Pendiente |
| MOB-006 | MealPlanFormScreen | QA-006-006 | Guard: sin platos muestra mensaje + botón "Crear plato" | Widget | Edge | BD sin platos | — | Alta | Pendiente |
| MOB-006 | MealPlanFormScreen | QA-006-007 | DatePicker de items respeta rango del plan | Widget | Happy | Plan con fechas definidas | TD-019 | Media | Pendiente |
| MOB-006 | MealPlanDetailScreen | QA-006-008 | Detalle muestra items agrupados por fecha | Widget | Happy | Plan con 3 items en 2 fechas | TD-022 | Alta | Pendiente |


### ALIM-MOB-007: Lista de Compras

| HU ID | Operación | QA ID | Descripción | Layer | Tipo | Precondiciones | Test Data | Prioridad | Estado |
|-------|-----------|-------|-------------|-------|------|---------------|-----------|-----------|--------|
| MOB-007 | ShoppingListService.generate | QA-007-001 | Plan semanal → lista única sin segmentación | Unit | Happy | Plan semanal con 2 platos | TD-023 | Alta | Pendiente |
| MOB-007 | ShoppingListService.generate | QA-007-002 | Plan mensual → 3 secciones (listos/verdes/otros) | Unit | Happy | Plan mensual con perecibles mixtos | TD-024 | Alta | Pendiente |
| MOB-007 | ShoppingListService.generate | QA-007-003 | Mismo ingrediente en 2 platos → cantidades sumadas | Unit | Happy | 2 platos con mismo ingrediente | TD-025 | Alta | Pendiente |
| MOB-007 | ShoppingListService.generate | QA-007-004 | Ingrediente perecible con 7 días → sección "Listos" | Unit | Edge | Plan mensual, ingrediente RipeningDays=7 | TD-026 | Alta | Pendiente |
| MOB-007 | ShoppingListService.generate | QA-007-005 | Ingrediente perecible con 8 días → sección "Verdes" | Unit | Edge | Plan mensual, ingrediente RipeningDays=8 | TD-026 | Alta | Pendiente |
| MOB-007 | ShoppingListService.generate | QA-007-006 | Plan sin items → resultado vacío | Unit | Edge | Plan sin MealPlanItems | — | Media | Pendiente |
| MOB-007 | ShoppingListScreen | QA-007-007 | Pantalla muestra secciones colapsables (plan mensual) | Widget | Happy | ShoppingListResult con 3 secciones | TD-024 | Alta | Pendiente |
| MOB-007 | ShoppingListScreen | QA-007-008 | Botón "Exportar PDF" genera archivo y abre Share Sheet | Integration | Happy | Lista generada con datos | TD-023 | Alta | Pendiente |

### ALIM-MOB-008: Backup y Restauración

| HU ID | Operación | QA ID | Descripción | Layer | Tipo | Precondiciones | Test Data | Prioridad | Estado |
|-------|-----------|-------|-------------|-------|------|---------------|-----------|-----------|--------|
| MOB-008 | BackupService.exportBackup | QA-008-001 | Exportar copia el .db y lanza Share Sheet | Integration | Happy | BD con datos | — | Alta | Pendiente |
| MOB-008 | BackupService.importBackup | QA-008-002 | Importar backup válido reemplaza datos actuales | Integration | Happy | Backup .db válido disponible | TD-027 | Alta | Pendiente |
| MOB-008 | BackupService.importBackup | QA-008-003 | Importar archivo no-SQLite → error "archivo no válido" | Unit | Error | Archivo .txt disponible | — | Alta | Pendiente |
| MOB-008 | BackupService.importBackup | QA-008-004 | Importar .db sin las 6 tablas → error "backup no válido" | Unit | Error | .db con solo 3 tablas | TD-028 | Alta | Pendiente |
| MOB-008 | SettingsScreen | QA-008-005 | Confirmar importación muestra ConfirmDialog con mensaje correcto | Widget | Happy | Archivo válido seleccionado | — | Alta | Pendiente |


---

## 2. Casos de Seguridad (ISO 27001)

| QA ID | Descripción | Control ISO | Layer | Precondiciones | Prioridad | Estado |
|-------|-------------|-------------|-------|---------------|-----------|--------|
| QA-SEC-001 | SQL injection en campo búsqueda no rompe BD | A.8.28 | Unit | BD inicializada | Alta | Pendiente |
| QA-SEC-002 | Input con `'; DROP TABLE --` es tratado como string literal | Unit | A.8.28 | BD inicializada | Alta | Pendiente |
| QA-SEC-003 | Importar backup inválido no corrompe BD actual | Unit | A.8.10 | BD con datos | Alta | Pendiente |
| QA-SEC-004 | Nombre > 100 chars es rechazado antes de llegar a BD | Unit | A.8.28 | — | Media | Pendiente |
| QA-SEC-005 | Archivo .db reside en directorio privado de la app | Integration | A.7.9 | App instalada | Media | Pendiente |

---

## 3. E2E User Flows

### E2E-001: Alta de ingrediente perecible completo

| Atributo | Valor |
|----------|-------|
| **Prioridad** | Alta |
| **HUs cubiertas** | MOB-002, MOB-003, MOB-004 |
| **Precondiciones** | App con BD vacía |
| **Test Data** | TD-002, TD-007, TD-010 |
| **Estado final esperado** | Ingrediente visible en lista con badges correctos |

| Paso | Acción | Pantalla | Resultado esperado | Valida QA |
|------|--------|----------|-------------------|-----------|
| 1 | Abrir tab Catálogos → Categorías | CategoryListScreen | EmptyState visible | QA-002-009 |
| 2 | Tap FAB "+" | CategoryFormScreen | Formulario vacío | — |
| 3 | Ingresar nombre "Verduras" y guardar | CategoryListScreen | Toast éxito, "Verduras" en lista | QA-002-001 |
| 4 | Ir a Unidades, tap FAB "+" | UnitFormScreen | Formulario vacío | — |
| 5 | Ingresar "Kilogramo" / "kg" y guardar | UnitListScreen | Toast éxito | QA-003-001 |
| 6 | Ir a Recetas → Ingredientes, tap FAB "+" | IngredientFormScreen | Formulario vacío | — |
| 7 | Seleccionar Categoría via BottomSheet | IngredientFormScreen | "Verduras" seleccionada | QA-004-009 |
| 8 | Seleccionar Unidad via BottomSheet | IngredientFormScreen | "Kilogramo (kg)" seleccionado | QA-004-009 |
| 9 | Activar "Es perecible", ingresar 5 días | IngredientFormScreen | Campo días visible | QA-004-008 |
| 10 | Guardar | IngredientListScreen | Toast éxito, ingrediente con badges | QA-004-001 |

---

### E2E-002: Crear plato y generar lista de compras semanal

| Atributo | Valor |
|----------|-------|
| **Prioridad** | Alta |
| **HUs cubiertas** | MOB-005, MOB-006, MOB-007 |
| **Precondiciones** | 2 ingredientes en BD (de E2E-001 o datos semilla) |
| **Test Data** | TD-014, TD-019, TD-023 |
| **Estado final esperado** | Lista de compras generada con cantidades sumadas |

| Paso | Acción | Pantalla | Resultado esperado | Valida QA |
|------|--------|----------|-------------------|-----------|
| 1 | Ir a Recetas → Platos, tap FAB "+" | DishFormScreen | Formulario vacío | — |
| 2 | Nombre "Arroz con pollo", tipo Almuerzo | DishFormScreen | Picker muestra 5 tipos | QA-005-009 |
| 3 | Agregar 2 ingredientes con cantidades | DishFormScreen | Lista dinámica con 2 items | QA-005-008 |
| 4 | Guardar | DishListScreen | Toast éxito, plato en lista | QA-005-001 |
| 5 | Ir a Planes, tap FAB "+" | MealPlanFormScreen | Formulario vacío | — |
| 6 | Tipo Semanal, fechas de 7 días | MealPlanFormScreen | DatePickers activos | — |
| 7 | Agregar 3 items con fechas y plato | MealPlanFormScreen | Lista de items dinámica | QA-006-007 |
| 8 | Guardar | MealPlanListScreen | Toast éxito, plan en lista | QA-006-001 |
| 9 | Tap en el plan → ver detalle | MealPlanDetailScreen | Items agrupados por fecha | QA-006-008 |
| 10 | Tap "Generar Lista de Compras" | ShoppingListScreen | Lista única (semanal) con cantidades | QA-007-001 |
| 11 | Tap "Exportar PDF" | Share Sheet nativo | PDF generado, Share Sheet abierto | QA-007-008 |

---

### E2E-003: Backup y restauración de datos

| Atributo | Valor |
|----------|-------|
| **Prioridad** | Media |
| **HUs cubiertas** | MOB-008 |
| **Precondiciones** | BD con al menos 1 categoría, 1 unidad, 1 ingrediente |
| **Test Data** | TD-027 |
| **Estado final esperado** | Datos restaurados visibles en la app |

| Paso | Acción | Pantalla | Resultado esperado | Valida QA |
|------|--------|----------|-------------------|-----------|
| 1 | Ir a tab Más → Backup de datos | SettingsScreen | Opciones de backup visibles | — |
| 2 | Tap "Exportar backup" | Share Sheet | .db compartido via Share Sheet | QA-008-001 |
| 3 | Tap "Importar backup", seleccionar .db válido | FilePicker | ConfirmDialog aparece | QA-008-005 |
| 4 | Confirmar importación | SettingsScreen | Toast "Backup restaurado correctamente" | QA-008-002 |
| 5 | Navegar a Categorías | CategoryListScreen | Datos restaurados visibles | QA-008-002 |

---

## 4. Catálogo de Test Data

| TD ID | Entidad | Propósito | Valores clave | Usado en | Tipo |
|-------|---------|-----------|--------------|---------|------|
| TD-001 | Seed data | Datos semilla peruanos | 10 categorías, 9 unidades, ~20 ingredientes, 5 platos | QA-001-003/004 | Seed |
| TD-002 | Category | Crear categoría válida | name: "Verduras" | QA-002-001/004 | Runtime |
| TD-003 | Category | Nombre demasiado largo | name: "A" × 101 chars | QA-002-003 | Runtime |
| TD-004 | Category | Editar categoría | id: 1, name: "Verduras Frescas" | QA-002-005/012 | Runtime |
| TD-005 | Category + Ingredient | Integridad referencial | Categoría con 1 ingrediente hijo | QA-002-007 | Seed |
| TD-006 | Categories list | Lista ordenada | ["Carnes", "Frutas", "Verduras"] | QA-002-008/010 | Seed |
| TD-007 | Unit | Crear unidad válida | name: "Kilogramo", symbol: "kg" | QA-003-001/004/006 | Runtime |
| TD-008 | Unit | Símbolo largo | symbol: "kilogramos" (11 chars) | QA-003-003 | Runtime |
| TD-009 | Unit + Ingredient | Integridad referencial | Unidad usada en 1 ingrediente | QA-003-005 | Seed |
| TD-010 | Ingredient | Perecible válido | name: "Tomate", isPerishable: true, ripeningDays: 5 | QA-004-001/005/007 | Runtime |
| TD-011 | Ingredient | No perecible | name: "Arroz", isPerishable: false | QA-004-002 | Runtime |
| TD-012 | Ingredient | Perecible días=0 | isPerishable: true, ripeningDays: 0 | QA-004-003 | Runtime |
| TD-013 | Ingredient + DishIngredient | Ingrediente en uso | Ingrediente en ≥1 plato | QA-004-006 | Seed |
| TD-014 | Dish | Plato válido con 2 ingredientes | name: "Arroz con pollo", mealType: almuerzo | QA-005-001/007/008 | Runtime |
| TD-015 | DishIngredient | Cantidad cero | ingredientId: 1, quantity: 0 | QA-005-003 | Runtime |
| TD-016 | DishIngredient | Ingrediente duplicado | 2 × ingredientId=1 en misma lista | QA-005-004 | Runtime |
| TD-017 | Dish update | Editar plato | Cambiar ingrediente del plato id=1 | QA-005-005 | Runtime |
| TD-018 | Dish + MealPlanItem | Plato en plan | Plato usado en ≥1 MealPlanItem | QA-005-006 | Seed |
| TD-019 | MealPlan semanal | Plan semanal válido | planType: semanal, 2026-07-14 → 2026-07-20, 3 items | QA-006-001/007 | Runtime |
| TD-020 | MealPlan | Fechas inválidas | startDate > endDate | QA-006-002 | Runtime |
| TD-021 | MealPlan | Item fuera de rango | Item con fecha fuera del plan | QA-006-003 | Runtime |
| TD-022 | MealPlan con items | Detalle agrupado | 3 items en 2 fechas distintas | QA-006-008 | Seed |
| TD-023 | MealPlan semanal completo | Lista de compras semanal | Plan con 2 platos, ingredientes mixtos | QA-007-001/008 | Seed |
| TD-024 | MealPlan mensual | Lista de compras mensual | Plan mensual con perecibles ≤7d, >7d y no perecibles | QA-007-002/007 | Seed |
| TD-025 | Mismo ingrediente 2 platos | Sumatoria de cantidades | Arroz en plato A (200g) + plato B (300g) = 500g | QA-007-003 | Seed |
| TD-026 | Ingrediente boundary | Segmentación exacta | RipeningDays=7 → Listos; =8 → Verdes | QA-007-004/005 | Runtime |
| TD-027 | Backup .db válido | Importación exitosa | Copia del .db con las 6 tablas | QA-008-002/005 | Seed |
| TD-028 | Backup .db inválido | Importación fallida | .db con solo 3 tablas (sin MealPlans) | QA-008-004 | Runtime |


---

## 5. Resumen de Cobertura

| Métrica | Valor |
|---------|-------|
| **Total HUs** | 8 |
| **Total casos de prueba** | 56 |
| — Unit layer | 35 |
| — Widget layer | 16 |
| — Integration layer | 5 |
| **Casos de seguridad (ISO)** | 5 |
| **E2E Flows** | 3 (27 pasos totales) |
| **Test Data entries** | 28 |
| **HUs sin tests** | Ninguna |
| **Operaciones sin HU** | Ninguna |

---

## 6. Distribución por HU

| HU ID | Total | Unit | Widget | Integration | Happy | Error | Edge | Seguridad |
|-------|-------|------|--------|-------------|-------|-------|------|-----------|
| MOB-001 | 6 | 2 | 1 | 3 | 4 | 0 | 2 | 0 |
| MOB-002 | 12 | 7 | 5 | 0 | 6 | 5 | 1 | 0 |
| MOB-003 | 6 | 5 | 1 | 0 | 3 | 3 | 0 | 0 |
| MOB-004 | 9 | 6 | 3 | 0 | 4 | 4 | 1 | 0 |
| MOB-005 | 9 | 7 | 2 | 0 | 4 | 4 | 0 | 0 |
| MOB-006 | 8 | 5 | 3 | 0 | 3 | 3 | 2 | 0 |
| MOB-007 | 8 | 6 | 1 | 1 | 3 | 0 | 3 | 0 |
| MOB-008 | 5 | 2 | 1 | 2 | 2 | 2 | 0 | 0 |
| **SEC** | **5** | **5** | **0** | **0** | **0** | **0** | **0** | **5** |
| **TOTAL** | **68** | **45** | **17** | **6** | **29** | **21** | **9** | **5** |

---

## 7. E2E Flow Index

| E2E ID | Nombre del Flujo | HUs Cubiertas | Pasos | Prioridad |
|--------|-----------------|--------------|-------|-----------|
| E2E-001 | Alta de ingrediente perecible completo | MOB-002, MOB-003, MOB-004 | 10 | Alta |
| E2E-002 | Crear plato y generar lista de compras semanal | MOB-005, MOB-006, MOB-007 | 11 | Alta |
| E2E-003 | Backup y restauración de datos | MOB-008 | 5 | Media |
