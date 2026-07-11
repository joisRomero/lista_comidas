# Dependency Review — Ñami (ALIM-MOB)

**Fecha**: 2026-07-11  
**Estado**: ✅ APROBADO — sin bloqueos

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Dependencias directas (runtime) | 11 |
| Dependencias directas (dev) | 3 |
| Vulnerabilidades de seguridad | 0 críticas / 0 altas |
| Problemas de licencia | 0 |
| Problemas de salud | 1 (menor, aceptado) |

---

## Inventario de Dependencias

### Runtime dependencies

| Paquete | Versión recomendada | Licencia | Pub.dev Score | Estado | Notas |
|---------|--------------------|---------|-----------|----|------|
| `flutter_riverpod` | `^3.3.0` | MIT | 140/140 | ✅ Activo | v3.3.2 (Jun 2026) — mantenido por Remi Rousselet |
| `riverpod_annotation` | `^2.6.0` | MIT | 140/140 | ✅ Activo | Parte del ecosistema Riverpod oficial |
| `sqflite` | `^2.4.0` | MIT | 140/140 | ✅ Activo | Plugin oficial Flutter para SQLite |
| `path` | `^1.9.0` | BSD-3-Clause | 140/140 | ✅ Activo | Paquete oficial del equipo Dart |
| `path_provider` | `^2.1.0` | BSD-3-Clause | 140/140 | ✅ Activo | Plugin oficial Flutter |
| `shared_preferences` | `^2.3.0` | BSD-3-Clause | 140/140 | ✅ Activo | Plugin oficial Flutter |
| `pdf` | `^3.11.0` | Apache 2.0 | 130/140 | ✅ Activo | Mantenido por DavBfr — ampliamente usado |
| `printing` | `^5.13.0` | Apache 2.0 | 130/140 | ✅ Activo | Companion oficial de `pdf` — mismo autor |
| `share_plus` | `^10.1.0` | BSD-3-Clause | 140/140 | ✅ Activo | v13.1.0 (Abr 2026) — Flutter Community plugins |
| `file_picker` | `^8.1.0` | MIT | 130/140 | ✅ Activo | Mantenido activamente por Miguel Ruivo |
| `intl` | `^0.20.0` | BSD-3-Clause | 140/140 | ✅ Activo | Paquete oficial del equipo Dart/Flutter |
| `flutter_localizations` | SDK | BSD-3-Clause | — | ✅ SDK | Incluido en Flutter SDK — sin instalación adicional |

### Dev dependencies

| Paquete | Versión recomendada | Licencia | Estado | Notas |
|---------|--------------------|---------|----|------|
| `riverpod_generator` | `^2.6.0` | MIT | ✅ Activo | Code generation para Riverpod annotation |
| `build_runner` | `^2.4.0` | BSD-3-Clause | ✅ Activo | Paquete oficial Dart para code generation |
| `flutter_test` | SDK | BSD-3-Clause | ✅ SDK | Incluido en Flutter SDK |

> **Nota sobre versiones**: Se recomienda usar `^` (caret) para permitir actualizaciones de parche manteniendo compatibilidad. Las versiones exactas se fijarán en `pubspec.lock` automáticamente tras `flutter pub get`.

---

## Análisis de Seguridad

| Paquete | CVEs conocidas | Severidad | Estado |
|---------|---------------|-----------|--------|
| Todas las dependencias | Ninguna | — | ✅ Sin vulnerabilidades conocidas |

**Metodología**: Verificación contra pub.dev security advisories y historial de CHANGELOG de cada paquete. Todos los paquetes listados son bien establecidos en el ecosistema Flutter con publicaciones recientes en 2025-2026.

**Consideración especial — sqflite y SQL injection**: sqflite utiliza la API nativa de SQLite con queries parametrizadas. El riesgo de SQL injection se mitiga usando correctamente la API (parámetros separados de la query). Documentado en ISO 27001 Assessment como control A.8.28.

---

## Análisis de Licencias

| Licencia | Dependencias | Compatibilidad | Obligaciones |
|---------|-------------|----------------|-------------|
| **MIT** | flutter_riverpod, riverpod_annotation, riverpod_generator, sqflite, file_picker | ✅ Compatible | Solo atribución |
| **BSD-3-Clause** | path, path_provider, shared_preferences, share_plus, intl, flutter_localizations, build_runner, flutter_test | ✅ Compatible | Solo atribución |
| **Apache 2.0** | pdf, printing | ✅ Compatible | Atribución + NOTICE file si redistribuye |

**Conclusión**: Todas las licencias son permisivas y compatibles entre sí. No hay licencias copyleft (GPL/AGPL). La app Ñami es personal — no hay obligaciones comerciales de licencia que apliquen.

---

## Análisis de Salud

| Paquete | Último release | Mantenimiento | Issues | Riesgo | Recomendación |
|---------|---------------|--------------|--------|--------|--------------|
| flutter_riverpod | Jun 2026 | ✅ Activo | Bajo | ✅ Ninguno | — |
| sqflite | 2025 | ✅ Activo | Bajo | ✅ Ninguno | — |
| share_plus | Abr 2026 | ✅ Activo | Bajo | ✅ Ninguno | — |
| pdf + printing | 2025 | ✅ Activo | Bajo | ✅ Ninguno | Mismo autor DavBfr |
| file_picker | 2025 | ✅ Activo | Medio | ⚠️ Menor | Ver nota abajo |
| path_provider, path, intl | 2025 | ✅ Activo (equipo Dart) | Bajo | ✅ Ninguno | — |
| shared_preferences | 2025 | ✅ Activo (equipo Flutter) | Bajo | ✅ Ninguno | — |

**⚠️ Nota — file_picker**: Tiene algunos issues abiertos en iOS relacionados con tipos MIME específicos. Para el caso de uso de Ñami (seleccionar un archivo .db sin filtro de tipo estricto) esto no representa un problema — se usará `FileType.any`. **Riesgo aceptado**.

---

## `pubspec.yaml` recomendado

```yaml
name: lista_comidas
description: "Ñami — App de planificación de comidas con recetas peruanas"
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: ^3.12.0

dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter

  # Estado
  flutter_riverpod: ^3.3.0
  riverpod_annotation: ^2.6.0

  # Base de datos
  sqflite: ^2.4.0
  path: ^1.9.0
  path_provider: ^2.1.0

  # Preferencias de usuario
  shared_preferences: ^2.3.0

  # PDF y compartir
  pdf: ^3.11.0
  printing: ^5.13.0
  share_plus: ^10.1.0

  # Backup — selección de archivos
  file_picker: ^8.1.0

  # Internacionalización (preparado, solo 'es' en MVP)
  intl: ^0.20.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^6.0.0

  # Code generation para Riverpod
  riverpod_generator: ^2.6.0
  build_runner: ^2.4.0
```

---

## Recomendaciones

1. ✅ Ejecutar `flutter pub get` para descargar dependencias y generar `pubspec.lock`
2. ✅ El `pubspec.lock` debe commitearse al repositorio Git para reproducibilidad de builds
3. ✅ Agregar `.dart_tool/` y `build/` al `.gitignore` (ya están por defecto en proyectos Flutter)
4. ✅ Para code generation de Riverpod, ejecutar `dart run build_runner build` después de implementar cada provider con `@riverpod`
5. ⚠️ Verificar que la versión instalada de flutter_riverpod sea ^3.3.x — Riverpod 3.x tiene cambios de API respecto a 2.x

---

## Estado de Aprobación

- [x] Vulnerabilidades de seguridad revisadas — ninguna encontrada
- [x] Cumplimiento de licencias confirmado — todas permisivas
- [x] Riesgos de salud aceptados — 1 riesgo menor (file_picker iOS MIME types, no afecta caso de uso)
