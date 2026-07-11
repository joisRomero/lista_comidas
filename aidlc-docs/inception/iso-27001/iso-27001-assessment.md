# ISO 27001:2022 Assessment — Ñami (ALIM-MOB)

**Versión**: 1.0  
**Fecha**: 2026-07-11  
**Profundidad**: Minimal  
**Estado**: Pendiente de aprobación

---

## 1. Perfil de Seguridad del Proyecto

| Atributo | Valor |
|----------|-------|
| Tipo de datos | Datos personales de planificación de comidas (no sensibles) |
| PII / datos financieros | ❌ No — datos de ingredientes, platos y planes |
| Exposición | Local — datos 100% en dispositivo, sin transmisión a red |
| Autenticación | ❌ Sin autenticación — app monousuario personal |
| API externa | ❌ Ninguna |
| Contexto regulatorio | Ninguno — app personal, no empresarial |
| Nivel de riesgo general | **Bajo** |

**Conclusión**: Ñami no procesa datos sensibles, no transmite información a servidores, y no tiene múltiples usuarios. El riesgo de seguridad es inherentemente bajo. El assessment se centra en proteger los datos locales del usuario y asegurar prácticas de desarrollo correctas.

---

## 2. Dominios de Control Aplicables

| Control ISO 27001:2022 | Relevancia | Justificación |
|------------------------|-----------|---------------|
| **A.5.8** Seguridad de la información en gestión de proyectos | ✅ Aplicable | Proyecto de desarrollo de software |
| **A.7.9** Seguridad de activos fuera de las instalaciones | ✅ Aplicable | BD SQLite reside en dispositivo móvil del usuario |
| **A.7.10** Medios de almacenamiento | ✅ Aplicable | Archivo `.db` SQLite como medio de almacenamiento de datos |
| **A.7.14** Eliminación segura o reutilización de equipos | ⚠️ Parcial | Datos quedan en dispositivo al desinstalar — advertir al usuario |
| **A.8.10** Eliminación de información | ✅ Aplicable | Función de eliminación de datos (backup/restore, desinstalación) |
| **A.8.13** Copia de seguridad de información | ✅ Aplicable | MOB-008 — funcionalidad de backup implementada |
| **A.8.25** Ciclo de vida de desarrollo seguro | ✅ Aplicable | Prácticas de código seguro en Flutter/Dart |
| **A.8.28** Codificación segura | ✅ Aplicable | Validación de inputs, manejo de errores, SQL injection en sqflite |

**Controles NO aplicables** (descartados por arquitectura):
- A.5.15/A.5.16/A.5.17 — Gestión de acceso/identidad: sin usuarios ni autenticación
- A.5.19-A.5.23 — Seguridad de proveedores/cloud: sin servicios externos
- A.8.2/A.8.3/A.8.5 — Acceso privilegiado / autenticación segura: monousuario
- A.8.20-A.8.24 — Seguridad de red: app totalmente offline
- A.6 (People Controls) — Sin equipo ni onboarding/offboarding en alcance

---

## 3. Mapping de Controles → Requisitos

| Control | Requisito Vinculado | Consideración de Implementación |
|---------|--------------------|---------------------------------|
| A.5.8 | RF-001 (Infraestructura base) | Arquitectura de capas limpia; separación DB/Service/UI |
| A.7.9 | RF-008 (Backup) | Archivo `.db` en directorio de app; acceso restringido por OS |
| A.7.10 | RF-008 (Backup) | Exportar backup a directorio seguro; advertir al usuario sobre datos en el `.db` |
| A.7.14 | RNF-008 (Persistencia) | Mostrar aviso en Settings: "Al desinstalar la app, los datos se eliminan. Haz un backup primero." |
| A.8.10 | RF-008 (Backup/Restore) | Al importar backup: confirmar destrucción de datos actuales antes de reemplazar |
| A.8.13 | RF-008 (Backup/Restauración) | Funcionalidad completa en MOB-008; sin backup automático en cloud |
| A.8.25 | RF-001 (Base) | Dependencias con versiones fijadas en `pubspec.yaml`; sin dependencias abandonadas |
| A.8.28 | RF-002 a RF-007 | Validación de todos los inputs antes de escribir en BD; sqflite usa queries parametrizadas (previene SQL injection) |

---

## 4. Consideraciones de Seguridad para Development

### 4.1 Protección del archivo SQLite (A.7.9, A.7.10)
- El archivo `.db` debe almacenarse en el directorio privado de la app (`getApplicationDocumentsDirectory()` via `path_provider`)
- En Android, este directorio no es accesible sin root
- En iOS, está dentro del sandbox de la app
- **No** exponer la ruta del archivo en logs o mensajes de error

### 4.2 SQL Injection — sqflite (A.8.28)
- sqflite usa queries parametrizadas por defecto con `?` placeholders
- **Nunca** concatenar strings para construir queries SQL
- Todos los Repositories deben usar la API de sqflite con parámetros separados: `db.query(table, where: 'Name = ?', whereArgs: [name])`
- La búsqueda con `LIKE '%?%'` también debe usar parámetros: `whereArgs: ['%$term%']`

### 4.3 Validación de Inputs (A.8.28)
- Validar en capa Service **antes** de cualquier operación de BD
- Sanitizar strings: trim() antes de comparaciones de unicidad
- Validar tipos: cantidades numéricas > 0, fechas coherentes (EndDate > StartDate)
- El archivo importado en backup debe validarse como SQLite válido con las 6 tablas esperadas antes de reemplazar datos

### 4.4 Eliminación de Datos (A.8.10, A.7.14)
- Mostrar `ConfirmDialog` con texto claro antes de: eliminar registros, importar backup, borrar todos los datos
- En Settings: advertencia visible — "Si desinstalas Ñami sin hacer backup, perderás todos tus datos"
- La función de importar backup debe hacer copia del archivo actual antes de reemplazar (rollback de emergencia)

### 4.5 Dependencias del proyecto (A.8.25)
- Fijar versiones exactas o con rango mínimo en `pubspec.yaml` (evitar `any`)
- Usar solo paquetes con pub.dev score > 90 y mantenimiento activo
- Verificar licencias compatibles (MIT, BSD, Apache 2.0) antes de agregar dependencias
- Ejecutar `flutter pub outdated` periódicamente

### 4.6 Ciclo de desarrollo seguro (A.8.25)
- Código fuente en repositorio Git privado
- No commitear el archivo `.db` de datos reales (agregar a `.gitignore`)
- No hardcodear rutas absolutas ni datos personales en el código

---

## 5. Testing de Seguridad Recomendado (para Build & Test)

| Test | Qué verificar |
|------|--------------|
| SQL Injection | Inputs con `'; DROP TABLE --` no deben romper la BD |
| Validación de límites | Strings >100 chars rechazados antes de INSERT |
| Integridad referencial | DELETE con hijos lanza el error correcto (no crashea) |
| Backup inválido | Importar un archivo `.txt` o `.db` corrupto muestra error sin reemplazar datos |
| Datos de fecha | EndDate = StartDate → error; EndDate anterior → error |

---

## 6. Open Items

| ID | Descripción | Etapa para resolver |
|----|-------------|---------------------|
| ISO-OI-01 | Evaluar cifrado del archivo `.db` si el usuario solicita mayor seguridad (ej: `sqflite_sqlcipher`) — fuera del alcance MVP | Post-MVP / Change Management |
| ISO-OI-02 | Política de retención: definir si ofrecer "Borrar todos los datos" desde Settings | Construction — MOB-008 |

---
