# ADR-003: Gestión de estado — Riverpod

## Status
Accepted

## Date
2026-07-11

## Context

La app Ñami necesita gestión de estado para: listas de datos cargadas desde BD, estado de formularios con campos condicionales (IsPerishable → RipeningDays), estado de carga/error en operaciones async de sqflite, y compartir datos entre pantallas (ej: lista de ingredientes disponibles para el formulario de platos). La app no tiene autenticación ni estado global complejo de sesión.

## Decision

Utilizaremos **Riverpod** (`flutter_riverpod` + `riverpod_annotation`) como solución de gestión de estado.

## Alternatives Considered

### Opción A: Riverpod ✅ (elegida)
- **Descripción**: Librería de gestión de estado type-safe para Flutter. Evolución de Provider con mejor compile-time safety.
- **Pros**: Type-safe en compile time; no requiere `BuildContext` para acceder al estado; soporte nativo para async (AsyncValue); testing sencillo con `ProviderContainer`; `riverpod_annotation` reduce boilerplate con code gen; activamente mantenido (Remi Rousselet)
- **Cons**: Requiere `build_runner` para code generation (aunque opcional con la API manual); curva de aprendizaje inicial

### Opción B: Provider
- **Descripción**: Wrapper de InheritedWidget, predecesor de Riverpod
- **Pros**: Muy conocido; documentación abundante; sin code generation
- **Cons**: Riverpod es su sucesor oficial — Provider está en modo mantenimiento; menos type-safe; requiere BuildContext en todos los accesos

### Opción C: BLoC / Cubit
- **Descripción**: Business Logic Component pattern con streams
- **Pros**: Separación clara de UI y lógica; patrón muy estructurado
- **Cons**: Verboso — cada feature requiere Event + State + Bloc/Cubit; sobre-ingenierizando para una app personal; boilerplate significativo

### Opción D: GetX
- **Descripción**: Todo-en-uno: estado, rutas, inyección de dependencias
- **Pros**: Mínimo boilerplate; todo integrado
- **Cons**: Anti-pattern de mezclar responsabilidades; difícil de testear; no recomendado por la comunidad Flutter para proyectos medianos+; opiniones divididas sobre calidad del código generado

### Opción E: setState + InheritedWidget (vanilla Flutter)
- **Descripción**: Sin librería externa, gestión manual
- **Pros**: Sin dependencias externas; control total
- **Cons**: No escala bien con múltiples pantallas y datos compartidos; prop drilling entre pantallas

## Rationale

Riverpod fue elegido porque:
1. El usuario lo confirmó explícitamente (Q2=A en preguntas de clarificación)
2. Es el estándar actual recomendado en la comunidad Flutter (2024-2026)
3. `AsyncValue` maneja el estado loading/error/data de operaciones sqflite de forma elegante
4. Type-safe en compile time — los errores de providers se detectan antes de ejecutar
5. No requiere BuildContext para leer providers — simplifica acceso desde Services y Repositories
6. Testing con `ProviderContainer` permite testear lógica sin widget tree

## Consequences

### Positive
- Estado async de BD gestionado limpiamente con `AsyncValue<List<T>>`
- Providers pueden depender de otros providers (ej: `ingredientsProvider` puede depender de `databaseProvider`)
- `ref.invalidate()` para refrescar listas tras operaciones CRUD
- Testeable de forma aislada sin Flutter framework

### Negative
- `riverpod_annotation` requiere `build_runner` para code generation — paso adicional en el workflow de desarrollo
- Los desarrolladores nuevos necesitan entender el modelo mental de Riverpod (providers como dependencias)

### Neutral
- La app usa `ConsumerWidget` y `ConsumerStatefulWidget` en lugar de `StatelessWidget`/`StatefulWidget`
- `ProviderScope` envuelve el `MaterialApp` en `main.dart`

## Related Decisions
- [ADR-001](ADR-001-flutter-framework.md) — Riverpod es específico del ecosistema Flutter
- [ADR-004](ADR-004-arquitectura-capas.md) — Los providers Riverpod exponen los Services a la UI

## References
- [riverpod.dev](https://riverpod.dev)
- [riverpod_annotation pub.dev](https://pub.dev/packages/riverpod_annotation)
