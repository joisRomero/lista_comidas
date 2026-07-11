# ADR-002: Base de datos local — SQLite via sqflite

## Status
Accepted

## Date
2026-07-11

## Context

La app Ñami requiere persistencia local de datos estructurados relacionales: categorías, unidades, ingredientes, platos (con lista de ingredientes N:N), planes de comida e items. Los datos deben sobrevivir reinicios de la app, soportar queries con JOINs y agregaciones (SUM para lista de compras), y permitir transacciones para operaciones multi-tabla (platos + ingredientes, planes + items).

La app es 100% offline — sin sincronización con servidor.

## Decision

Utilizaremos **SQLite** como motor de BD embebida, accedida vía el paquete **`sqflite`** de Flutter.

## Alternatives Considered

### Opción A: sqflite (SQLite) ✅ (elegida)
- **Descripción**: Paquete Flutter oficial para SQLite embebido. SQLite es el motor de BD relacional más usado en mobile.
- **Pros**: Soporte nativo en Android e iOS sin dependencias externas; queries SQL completas (JOINs, transacciones, índices); pub.dev score alto; documentación extensa; simplicidad de backup (un archivo `.db`)
- **Cons**: API de bajo nivel — requiere mapeo manual de resultados a objetos Dart; sin type-safety en queries SQL (strings)

### Opción B: Drift (antes Moor)
- **Descripción**: ORM type-safe para Flutter/Dart sobre SQLite
- **Pros**: Queries type-safe generadas por código; migrations declarativas; API más ergonómica
- **Cons**: Requiere code generation (`build_runner`) — agrega complejidad de toolchain; curva de aprendizaje mayor; el modelo de queries es diferente al SQL estándar; overhead para un proyecto personal

### Opción C: Hive / Isar (NoSQL)
- **Descripción**: Bases de datos NoSQL key-value o de documentos para Flutter
- **Pros**: Muy rápidas para lecturas simples; sin schema rígido
- **Cons**: No soportan JOINs ni queries relacionales complejas; el modelo de datos de Ñami es relacional (FK entre 6 tablas); agregar cantidades entre platos requeriría lógica Dart en lugar de SQL

### Opción D: SharedPreferences
- **Descripción**: Almacenamiento key-value simple
- **Pros**: Muy sencillo para configuraciones
- **Cons**: No apto para datos estructurados relacionales; no soporta queries ni transacciones

## Rationale

sqflite fue elegido sobre drift porque:
1. La app es personal y el volumen de datos es pequeño (< 10,000 registros) — no se justifica la complejidad de un ORM
2. sqflite expone SQL directo, lo que permite reutilizar exactamente las queries documentadas en `mobile-user-stories.md`
3. Las queries de la lista de compras requieren JOINs y GROUP BY — SQLite las maneja nativamente
4. El backup es trivial: copiar el archivo `.db` (requisito MOB-008)
5. Sin code generation adicional — el proyecto es más simple de mantener

## Consequences

### Positive
- Queries SQL exactas del spec (`mobile-user-stories.md`) implementables sin traducción
- Backup/Restore = copiar un solo archivo `.db`
- Transacciones ACID para operaciones multi-tabla (platos + ingredientes)
- Índices explícitos para optimizar búsquedas (IX_Ingredients_CategoryId, etc.)
- Sin dependencias adicionales de toolchain

### Negative
- Mapeo manual de `Map<String, dynamic>` → objetos Dart en cada Repository
- Sin type-safety en queries SQL — errores detectados en runtime, no en compilación
- Las migrations deben escribirse manualmente con scripts SQL

### Neutral
- Schema versionado con `onUpgrade` — patrón estándar de SQLite mobile

## Related Decisions
- [ADR-001](ADR-001-flutter-framework.md) — sqflite es el paquete SQLite estándar del ecosistema Flutter
- [ADR-004](ADR-004-arquitectura-capas.md) — El patrón Repository encapsula el acceso a sqflite

## References
- [sqflite pub.dev](https://pub.dev/packages/sqflite)
- Schema DDL: `aidlc-docs/inception/requirements/requirements.md` §6
