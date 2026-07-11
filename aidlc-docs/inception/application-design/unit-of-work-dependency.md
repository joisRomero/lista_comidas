# Dependencias entre Unidades — Ñami (ALIM-MOB)

**Fecha**: 2026-07-11

---

## Matriz de Dependencias

| | U1-Base | U2-Categ | U3-Units | U4-Ingred | U5-Dishes | U6-Plans | U7-Shopping | U8-Backup |
|--|---------|---------|---------|---------|---------|---------|----------|---------|
| **U1-Base** | — | provee | provee | provee | provee | provee | provee | provee |
| **U2-Categ** | requiere | — | — | provee | — | — | — | — |
| **U3-Units** | requiere | — | — | provee | — | — | — | — |
| **U4-Ingred** | requiere | requiere | requiere | — | provee | — | — | — |
| **U5-Dishes** | requiere | — | — | requiere | — | provee | — | — |
| **U6-Plans** | requiere | — | — | — | requiere | — | provee | — |
| **U7-Shopping** | requiere | — | — | — | — | requiere | — | — |
| **U8-Backup** | requiere | — | — | — | — | — | — | — |

---

## Diagrama de dependencias

```
                    U1 — Infraestructura Base
                   /   \         \
                  /     \         \
              U2          U3      U8
           Categorías   Unidades  Backup
               \        /
                \      /
                 U4
              Ingredientes
                  |
                  U5
                Platos
                  |
                  U6
             Planes de Comida
                  |
                  U7
           Lista de Compras + PDF
```

---

## Camino crítico

```
U1 → U2/U3 (paralelo) → U4 → U5 → U6 → U7
```

**Duración del camino crítico**: 6 unidades en secuencia (U2 y U3 paralelas reducen 1 paso).

---

## Oportunidades de paralelismo

| Sprint / Fase | Unidades ejecutables en paralelo |
|--------------|----------------------------------|
| Fase 1 | U1 (bloqueante — debe completarse sola) |
| Fase 2 | U2 + U3 (sin dependencia entre sí) |
| Fase 3 | U4 (requiere U2 y U3 completadas) |
| Fase 4 | U5 (requiere U4) |
| Fase 5 | U6 (requiere U5) |
| Fase 6 | U7 + U8 (U7 requiere U6; U8 solo requiere U1 — pueden ir en paralelo) |

---

## Tipo de dependencia por par

| Dependencia | Tipo | Descripción |
|-------------|------|-------------|
| U1 → U2..U8 | **Hard** | DatabaseHelper y BaseRepository son requisito de todos |
| U2 → U4 | **Data** | CategoryRepository es FK requerida para insertar ingredientes |
| U3 → U4 | **Data** | UnitRepository es FK requerida para insertar ingredientes |
| U4 → U5 | **Data** | IngredientRepository es FK y BottomSheetPicker en DishForm |
| U5 → U6 | **Data** | DishRepository es FK y BottomSheetPicker en MealPlanForm |
| U6 → U7 | **Data** | MealPlanRepository.getAggregatedIngredients() requiere planes con items |
| U1 → U8 | **Hard** | DatabaseHelper.close/reinit requerido para backup import |
