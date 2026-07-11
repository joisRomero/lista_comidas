# Story Map — Ñami (ALIM-MOB)

**Fecha**: 2026-07-11

---

## Mapa HU → Unidad → Capas → Tests

| HU ID | Título | Unidad | Epic | Capas afectadas | QA IDs | Estimación |
|-------|--------|--------|------|----------------|--------|-----------|
| MOB-001 | Configuración Base | U1 | Infraestructura | core/database, core/theme, core/providers, shared/widgets, main.dart | QA-001-001..006 | M |
| MOB-002 | CRUD Categorías | U2 | Catálogos | core/models/category.dart, core/repositories/category_repository, core/services/category_service, features/categories/ | QA-002-001..012 | S |
| MOB-003 | CRUD Unidades | U3 | Catálogos | core/models/unit.dart, core/repositories/unit_repository, core/services/unit_service, features/units/ | QA-003-001..006 | S |
| MOB-004 | CRUD Ingredientes | U4 | Ingredientes | core/models/ingredient.dart, core/repositories/ingredient_repository, core/services/ingredient_service, features/ingredients/ | QA-004-001..009 | M |
| MOB-005 | CRUD Platos | U5 | Platos | core/models/dish.dart + dish_ingredient.dart, core/repositories/dish_repository, core/services/dish_service, features/dishes/ | QA-005-001..009 | M |
| MOB-006 | Planes de Comida | U6 | Planificación | core/models/meal_plan.dart + meal_plan_item.dart, core/repositories/meal_plan_repository, core/services/meal_plan_service, features/meal_plans/ | QA-006-001..008 | L |
| MOB-007 | Lista de Compras + PDF | U7 | Planificación | core/models/shopping_list_item.dart, core/services/shopping_list_service, features/shopping_list/ | QA-007-001..008 | M |
| MOB-008 | Backup y Restauración | U8 | Infraestructura | core/services/backup_service.dart, features/settings/ | QA-008-001..005 | S |

---

## Mapa por Sprint (propuesto)

### Sprint 1 — Base + Catálogos
```
U1: MOB-001  Infraestructura Base
U2: MOB-002  CRUD Categorías         (paralelo con U3 tras U1)
U3: MOB-003  CRUD Unidades           (paralelo con U2 tras U1)
```
**Entregables del Sprint 1**:
- App con navegación y tema funcionando
- CRUD completo de Categorías y Unidades
- BD inicializada con schema versión 1
- Datos semilla cargables desde Settings

### Sprint 2 — Ingredientes + Platos
```
U4: MOB-004  CRUD Ingredientes
U5: MOB-005  CRUD Platos
```
**Entregables del Sprint 2**:
- Ingredientes con selección via BottomSheetPicker
- Platos con lista dinámica de ingredientes
- Transacciones multi-tabla verificadas

### Sprint 3 — Planificación + Extras
```
U6: MOB-006  Planes de Comida
U7: MOB-007  Lista de Compras + PDF  (paralelo con U8 tras U6)
U8: MOB-008  Backup y Restauración   (paralelo con U7, solo requiere U1)
```
**Entregables del Sprint 3**:
- Planes semanales y mensuales completos
- Lista de compras con segmentación y exportación PDF
- Backup / Restauración del archivo .db

---

## Cobertura de Criterios de Aceptación

| HU ID | CAs totales | CAs cubiertas por tests | % cobertura |
|-------|------------|------------------------|-------------|
| MOB-001 | 10 | 6 | 60% (infra base — cobertura en integration) |
| MOB-002 | 11 | 12 | 100% |
| MOB-003 | 8 | 6 | 75% |
| MOB-004 | 10 | 9 | 90% |
| MOB-005 | 13 | 9 | 69% (transacciones cubiertas en integration) |
| MOB-006 | 12 | 8 | 67% (DatePicker nativo difícil de testear en Widget) |
| MOB-007 | 10 | 8 | 80% |
| MOB-008 | 6 | 5 | 83% |
| **TOTAL** | **80** | **63** | **~79%** |

---

## Archivos a crear por unidad

### U1 — core/
```
lib/core/database/database_helper.dart
lib/core/database/schema.dart
lib/core/database/repositories/base_repository.dart
lib/core/models/           (vacíos, se llenan en U2-U8)
lib/core/services/         (vacíos, se llenan en U2-U8)
lib/core/providers/providers.dart
lib/core/theme/app_theme.dart
lib/core/l10n/app_es.arb
lib/core/utils/constants.dart
lib/core/utils/service_result.dart
lib/shared/widgets/app_scaffold.dart
lib/shared/widgets/confirm_dialog.dart
lib/shared/widgets/empty_state.dart
lib/shared/widgets/search_bar_widget.dart
lib/shared/widgets/loading_skeleton.dart
lib/shared/widgets/bottom_sheet_picker.dart
lib/shared/widgets/app_toast.dart
lib/app.dart
lib/main.dart
```

### U2 — features/categories/
```
lib/core/models/category.dart
lib/core/database/repositories/category_repository.dart
lib/core/services/category_service.dart
lib/features/categories/category_list_screen.dart
lib/features/categories/category_form_screen.dart
```

### U3 — features/units/
```
lib/core/models/unit.dart
lib/core/database/repositories/unit_repository.dart
lib/core/services/unit_service.dart
lib/features/units/unit_list_screen.dart
lib/features/units/unit_form_screen.dart
```

### U4 — features/ingredients/
```
lib/core/models/ingredient.dart
lib/core/database/repositories/ingredient_repository.dart
lib/core/services/ingredient_service.dart
lib/features/ingredients/ingredient_list_screen.dart
lib/features/ingredients/ingredient_form_screen.dart
```

### U5 — features/dishes/
```
lib/core/models/dish.dart
lib/core/models/dish_ingredient.dart
lib/core/database/repositories/dish_repository.dart
lib/core/services/dish_service.dart
lib/features/dishes/dish_list_screen.dart
lib/features/dishes/dish_form_screen.dart
```

### U6 — features/meal_plans/
```
lib/core/models/meal_plan.dart
lib/core/models/meal_plan_item.dart
lib/core/database/repositories/meal_plan_repository.dart
lib/core/services/meal_plan_service.dart
lib/features/meal_plans/meal_plan_list_screen.dart
lib/features/meal_plans/meal_plan_form_screen.dart
lib/features/meal_plans/meal_plan_detail_screen.dart
```

### U7 — features/shopping_list/
```
lib/core/models/shopping_list_item.dart
lib/core/services/shopping_list_service.dart
lib/features/shopping_list/shopping_list_screen.dart
```

### U8 — features/settings/
```
lib/core/services/backup_service.dart
lib/core/utils/seed_data.dart
lib/features/settings/settings_screen.dart
```
