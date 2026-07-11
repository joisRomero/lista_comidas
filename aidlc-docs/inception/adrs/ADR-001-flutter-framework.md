# ADR-001: Framework móvil — Flutter/Dart

## Status
Accepted

## Date
2026-07-11

## Context

Se necesita construir una app móvil standalone (sin servidor) para planificación de comidas personales. El proyecto ya existe inicializado como proyecto Flutter en el workspace. La app debe funcionar en Android e iOS, con soporte responsive para tablets. No hay equipo — es un proyecto personal de un desarrollador. El tiempo de desarrollo es un factor relevante.

## Decision

Utilizaremos **Flutter (Dart)** como framework móvil único para toda la aplicación.

## Alternatives Considered

### Opción A: Flutter/Dart ✅ (elegida)
- **Descripción**: Framework de Google para apps cross-platform con UI propia (no webview ni bridges nativos)
- **Pros**: Un solo codebase para Android + iOS + Web + Desktop; hot reload para desarrollo rápido; rendimiento cercano a nativo (Skia/Impeller); ecosistema maduro (pub.dev); proyecto ya inicializado en workspace; Material Design 3 nativo
- **Contras**: Dart es un lenguaje adicional a aprender; tamaño de APK mayor que nativo puro

### Opción B: React Native (TypeScript)
- **Descripción**: Framework de Meta usando React + bridge nativo
- **Pros**: Reutiliza conocimiento web/React; gran ecosistema npm
- **Contras**: Dependencia de bridge nativo puede causar inconsistencias; migración desde Expo a bare flow compleja; el proyecto ya está inicializado como Flutter — cambiar implicaría empezar de cero

### Opción C: .NET MAUI (C#)
- **Descripción**: Framework de Microsoft para apps cross-platform
- **Pros**: Mismo lenguaje que el sistema web origen (Blazor); comparte DTOs
- **Cons**: Ecosistema mobile más pequeño; peor soporte en macOS para desarrollo iOS; tooling más pesado

### Opción D: Kotlin/Swift nativo
- **Descripción**: Dos codebases separados, uno por plataforma
- **Pros**: Máximo rendimiento y acceso a APIs nativas
- **Cons**: Doble esfuerzo de desarrollo y mantenimiento; no práctico para proyecto personal

## Rationale

Flutter fue elegido porque:
1. El proyecto ya está inicializado como Flutter — cambiar de framework implicaría un costo sin beneficio
2. Cross-platform real con un solo codebase cubre Android + iOS + tablet sin esfuerzo adicional
3. Material Design 3 viene integrado, lo que acelera la implementación de la UI
4. El rendimiento es suficiente para una app con BD local de uso personal (< 10,000 registros)
5. Dart tiene una curva de aprendizaje baja para desarrolladores con experiencia en lenguajes tipados

## Consequences

### Positive
- Un solo codebase para todas las plataformas objetivo
- Hot reload acelera el desarrollo de UI
- Material Design 3 + tema personalizado sin librerías adicionales
- Compilación a código nativo (no interpretado en runtime)

### Negative
- APK/IPA más pesado que una app nativa equivalente (~10-15 MB adicionales del runtime Flutter)
- Dart no es tan ubicuo como TypeScript o C# — menor comunidad de ayuda

### Neutral
- Dart es similar a Java/TypeScript — la adopción es rápida para desarrolladores con experiencia en lenguajes OO
- Flutter gestiona las diferencias de UI entre plataformas automáticamente

## Related Decisions
- [ADR-002](ADR-002-sqlite-sqflite.md) — BD local usa paquete `sqflite` específico de Flutter
- [ADR-003](ADR-003-riverpod-state.md) — Estado usa Riverpod, ecosistema Flutter nativo

## References
- [flutter.dev](https://flutter.dev)
- Proyecto inicializado: `d:\proyectos\lista_comidas\pubspec.yaml`
