# ADR-004: Arquitectura de capas — Repository + Service Pattern

## Status
Accepted

## Date
2026-07-11

## Context

La app Ñami tiene lógica de negocio no trivial: validaciones de integridad referencial antes de eliminar, algoritmo de lista de compras con segmentación, transacciones multi-tabla para platos y planes, y reglas condicionales (IsPerishable → RipeningDays). Necesitamos una arquitectura que:
- Separe el acceso a datos de la lógica de negocio
- Permita testear las reglas de negocio de forma aislada
- Sea coherente entre los 8 módulos (categorías, unidades, ingredientes, platos, planes, lista de compras, backup, settings)

## Decision

Implementaremos una **arquitectura de 4 capas**: UI (Screens/Widgets) → Providers (Riverpod) → Services (lógica de negocio) → Repositories (acceso a BD).

## Alternatives Considered

### Opción A: Repository + Service (4 capas) ✅ (elegida)
- **Descripción**: UI llama providers → providers llaman services → services llaman repositories → repositories ejecutan SQL
- **Pros**: Separación clara de responsabilidades; testeable por capa; reglas de negocio centralizadas en Services; SQL encapsulado en Repositories; patrón reconocible
- **Cons**: Más archivos por feature (4 capas vs 2); puede parecer over-engineered para features simples como CRUD de categorías

### Opción B: Repository directo desde UI (2 capas)
- **Descripción**: UI llama directamente a los Repositories sin capa Service
- **Pros**: Menos archivos; más directo para CRUD simple
- **Cons**: Las reglas de negocio (RN-003: no eliminar con hijos, RN-004: perecible requiere días) quedan en la UI o mezcladas con el acceso a BD; algoritmo de lista de compras no tiene capa clara

### Opción C: BLoC per feature (UI → BLoC → Repository)
- **Descripción**: Cada feature tiene un BLoC que gestiona estado y lógica
- **Pros**: Patrón estándar en muchos proyectos Flutter
- **Cons**: Ya descartado en ADR-003 por verbosidad; mezcla estado y lógica de negocio en la misma capa

## Rationale

El patrón Repository + Service fue elegido porque:
1. El algoritmo de lista de compras (`ShoppingListService`) tiene lógica compleja que no pertenece ni a la UI ni al acceso a BD
2. Las validaciones de integridad referencial (COUNT antes de DELETE) son lógica de negocio — van en Services, no en Repositories
3. Riverpod providers actúan como la capa de orquestación que conecta Services con la UI — encajan naturalmente como la 3ra capa
4. El patrón `BaseRepository<T>` reduce duplicación entre los 6 repositories (CRUD genérico)
5. Testear `ShoppingListService.generateList()` de forma aislada (con mocks de Repository) es trivial con esta arquitectura

## Responsibilities por Capa

| Capa | Responsabilidad | Ejemplos |
|------|----------------|---------|
| **UI (Screens/Widgets)** | Presentación, navegación, capturar input usuario | `CategoryListScreen`, `DishFormScreen` |
| **Providers (Riverpod)** | Estado async, invalidación de cache, DI | `categoriesProvider`, `dishByIdProvider` |
| **Services** | Reglas de negocio, validaciones, algoritmos | `CategoryService.delete()` (verifica hijos), `ShoppingListService.generate()` |
| **Repositories** | SQL puro: SELECT/INSERT/UPDATE/DELETE | `CategoryRepository.getAll()`, `DishRepository.saveWithIngredients()` |

### Regla de dependencias (unidireccional)
```
UI → Providers → Services → Repositories → sqflite
```
- UI nunca llama directamente a Repositories
- Services nunca conocen Providers ni Widgets
- Repositories nunca conocen lógica de negocio

## Consequences

### Positive
- Lógica de negocio (validaciones, algoritmos) testeables con unit tests puros — sin BD real
- SQL encapsulado en Repositories — cambiar de sqflite a drift en el futuro afecta solo esa capa
- `BaseRepository<T>` con métodos `getAll`, `getById`, `insert`, `update`, `delete` elimina duplicación
- Cada módulo sigue el mismo patrón — consistencia entre los 8 features

### Negative
- Features simples como CRUD de Categorías tienen 4 archivos (screen + provider + service + repository) en lugar de 2
- Mayor número de archivos totales en el proyecto

### Neutral
- La estructura de carpetas sigue `lib/core/` para capas compartidas y `lib/features/` para UI por feature
- Inyección de dependencias vía Riverpod providers (no un contenedor DI separado)

## Related Decisions
- [ADR-002](ADR-002-sqlite-sqflite.md) — Repositories encapsulan sqflite
- [ADR-003](ADR-003-riverpod-state.md) — Providers Riverpod conectan Services con UI

## References
- Estructura de proyecto detallada: `aidlc-docs/inception/requirements/requirements.md` §5
- Reglas de negocio: `aidlc-docs/inception/requirements/requirements.md` §12
