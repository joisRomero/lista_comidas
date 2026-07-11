# Documento de Requisitos — Ñami (ALIM-MOB)

**Versión**: 1.1  
**Fecha**: 2026-07-11  
**Estado**: Aprobado

---

## 1. Resumen del Análisis de Intención

| Atributo | Valor |
|----------|-------|
| **Tipo de solicitud** | New Project (app mobile completa) |
| **Alcance estimado** | System-wide — 8 módulos, 13 pantallas, BD local |
| **Complejidad** | Moderate — app standalone sin API externa, lógica de negocio en dispositivo |
| **Stack confirmado** | Flutter / Dart + SQLite (sqflite) + Riverpod |
| **Plataformas objetivo** | Android e iOS (primary) + tablet/responsive |
| **Autenticación** | Ninguna — app personal monousuario |

---

## 2. Descripción del Proyecto

Aplicación móvil standalone que replica el sistema web "Alimentación" (Blazor WebAssembly) como app completamente autónoma. Toda la lógica de negocio y los datos viven en el dispositivo — no hay comunicación con servidores externos.

**Proyecto Jira / ID**: ALIM-MOB  
**Usuario objetivo**: Personal (monousuario) — sin autenticación requerida

---

## 3. Estándares Organizacionales

> **HARD CONSTRAINTS** — no renegociar en etapas posteriores.

| Constraint | Valor |
|-----------|-------|
| Framework | Flutter (Dart) — proyecto ya inicializado |
| Base de datos | SQLite via paquete `sqflite` |
| Estado | Riverpod (flutter_riverpod) |
| Idioma UI | Español — arquitectura i18n preparada (AppLocalizations) pero solo `es` en MVP |
| Diseño | Material Design 3 + paleta ALIM-MOB (ver sección 7) |
| Soporte de dispositivos | Teléfonos + tablets (responsive adaptativo) |
| Datos semilla | Configurable: botón "Cargar datos de ejemplo" (comida peruana) |
| Generación PDF | Sprint 3 — paquetes `pdf` + `printing` |

---

## 4. Arquitectura del Sistema

```
┌───────────────────────────────────────────────────┐
│                App Móvil Standalone                │
│                                                   │
│  ┌──────────┐   ┌──────────┐   ┌───────────────┐  │
│  │  UI /    │   │ Services │   │  Repositories │  │
│  │ Screens  │ → │(Lógica   │ → │  (SQLite /    │  │
│  │(Riverpod)│   │Negocio)  │   │   sqflite)    │  │
│  └──────────┘   └──────────┘   └───────────────┘  │
│                                                   │
│           NO comunicación con servidores           │
└───────────────────────────────────────────────────┘
```

**Capas**:
1. **UI Layer** — Screens + Widgets (Flutter, Riverpod `ConsumerWidget`)
2. **Service Layer** — Lógica de negocio, validaciones, algoritmos
3. **Repository Layer** — Acceso a datos SQLite (patrón Repository genérico)
4. **Database Layer** — `DatabaseHelper` + migrations + schema DDL

---

## 5. Estructura de Proyecto Flutter

```
lib/
├── main.dart
├── app.dart                    # MaterialApp, rutas, tema
├── core/
│   ├── database/
│   │   ├── database_helper.dart     # Singleton SQLite, init, migrations
│   │   ├── schema.dart              # DDL como constantes String
│   │   └── repositories/
│   │       ├── base_repository.dart
│   │       ├── category_repository.dart
│   │       ├── unit_repository.dart
│   │       ├── ingredient_repository.dart
│   │       ├── dish_repository.dart
│   │       └── meal_plan_repository.dart
│   ├── models/
│   │   ├── category.dart
│   │   ├── unit.dart
│   │   ├── ingredient.dart
│   │   ├── dish.dart
│   │   ├── dish_ingredient.dart
│   │   ├── meal_plan.dart
│   │   ├── meal_plan_item.dart
│   │   └── shopping_list_item.dart
│   ├── services/
│   │   ├── category_service.dart
│   │   ├── unit_service.dart
│   │   ├── ingredient_service.dart
│   │   ├── dish_service.dart
│   │   ├── meal_plan_service.dart
│   │   └── shopping_list_service.dart
│   ├── providers/              # Riverpod providers
│   │   └── providers.dart
│   ├── theme/
│   │   └── app_theme.dart
│   ├── l10n/                   # i18n preparado
│   │   └── app_es.arb
│   └── utils/
│       ├── constants.dart      # Enums, constantes globales
│       └── seed_data.dart      # Datos semilla (comida peruana)
├── features/
│   ├── home/
│   ├── categories/
│   ├── units/
│   ├── ingredients/
│   ├── dishes/
│   ├── meal_plans/
│   ├── shopping_list/
│   └── settings/               # Backup, tema, about
└── shared/
    └── widgets/
        ├── app_scaffold.dart
        ├── confirm_dialog.dart
        ├── empty_state.dart
        ├── search_bar_widget.dart
        ├── loading_skeleton.dart
        └── bottom_sheet_picker.dart
```

---

## 6. Esquema de Base de Datos (SQLite)

### 6.1 Tablas

```sql
-- Categorías de ingredientes
CREATE TABLE Categories (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE,
    Description TEXT,
    CreatedAt TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Unidades de medida
CREATE TABLE Units (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE,
    Symbol TEXT NOT NULL,
    CreatedAt TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Ingredientes
CREATE TABLE Ingredients (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE,
    UnitId INTEGER NOT NULL,
    CategoryId INTEGER NOT NULL,
    IsPerishable INTEGER NOT NULL DEFAULT 0,
    RipeningDays INTEGER,
    CreatedAt TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (UnitId) REFERENCES Units(Id),
    FOREIGN KEY (CategoryId) REFERENCES Categories(Id)
);

-- Platos / Recetas
CREATE TABLE Dishes (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE,
    Description TEXT,
    MealType TEXT NOT NULL,
    CreatedAt TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Ingredientes de un plato (relación N:N)
CREATE TABLE DishIngredients (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    DishId INTEGER NOT NULL,
    IngredientId INTEGER NOT NULL,
    Quantity REAL NOT NULL,
    FOREIGN KEY (DishId) REFERENCES Dishes(Id) ON DELETE CASCADE,
    FOREIGN KEY (IngredientId) REFERENCES Ingredients(Id)
);

-- Planes de comida
CREATE TABLE MealPlans (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    PlanType TEXT NOT NULL,
    StartDate TEXT NOT NULL,
    EndDate TEXT NOT NULL,
    CreatedAt TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Items del plan (plato asignado a un día/momento)
CREATE TABLE MealPlanItems (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    MealPlanId INTEGER NOT NULL,
    DishId INTEGER NOT NULL,
    Date TEXT NOT NULL,
    MealTime TEXT NOT NULL,
    FOREIGN KEY (MealPlanId) REFERENCES MealPlans(Id) ON DELETE CASCADE,
    FOREIGN KEY (DishId) REFERENCES Dishes(Id)
);
```

### 6.2 Índices

```sql
CREATE INDEX IX_Ingredients_CategoryId ON Ingredients(CategoryId);
CREATE INDEX IX_Ingredients_UnitId ON Ingredients(UnitId);
CREATE INDEX IX_DishIngredients_DishId ON DishIngredients(DishId);
CREATE INDEX IX_DishIngredients_IngredientId ON DishIngredients(IngredientId);
CREATE INDEX IX_MealPlanItems_MealPlanId ON MealPlanItems(MealPlanId);
CREATE INDEX IX_MealPlanItems_DishId ON MealPlanItems(DishId);
CREATE INDEX IX_MealPlanItems_Date ON MealPlanItems(Date);
```

### 6.3 Convenciones SQLite
- `INTEGER` para booleanos (0 = false, 1 = true)
- `TEXT` en formato ISO 8601 para fechas (`2026-07-11T00:00:00`)
- `REAL` para cantidades decimales
- `ON DELETE CASCADE` solo en DishIngredients y MealPlanItems
- **Sin** `UpdatedAt` — `CreatedAt` es suficiente para uso personal

---

## 7. Paleta de Colores y Tema

| Token | CSS Var | Hex | Uso |
|-------|---------|-----|-----|
| Primary | `--color-1` | `#53D669` | Botones primarios, FAB, acentos principales |
| Secondary | `--color-2` | `#53D6AB` | Badges, estados activos, highlights |
| Tertiary | `--color-3` | `#53C0D6` | Links, bordes decorativos, íconos secundarios |

**Notas de implementación en Material 3**:
- El `ColorScheme` se genera con `ColorScheme.fromSeed(seedColor: Color(0xFF53D669))`
- Sobrescribir `primary`, `secondary`, `tertiary` con los valores exactos de la paleta
- Tema claro y oscuro comparten la misma paleta base (ajuste automático de tonos via Material 3)
- **Tema claro/oscuro** togglable desde pestaña "Más", persistido en `SharedPreferences`

---

## 8. Navegación

```
Bottom Navigation Bar (5 tabs)
├── 🏠 Inicio        → HomeScreen
├── 📦 Catálogos     → CatalogosScreen (nested tabs: Categorías | Unidades)
├── 🍽️ Recetas       → RecetasScreen (nested tabs: Ingredientes | Platos)
├── 📅 Planes        → PlanesScreen (lista → detalle → lista de compras)
└── ⚙️ Más          → SettingsScreen (tema, backup, about)
```

**Navegación stack dentro de cada tab**:
- Lista → Form (crear/editar) via `Navigator.push`
- Plan lista → Plan detalle → Lista de compras

---

## 9. Enumeraciones (Constantes)

### MealType (tipo del plato)
`Desayuno | Almuerzo | Cena | Snack | Postre`

### MealTime (momento del item en el plan)
`Desayuno | MediaMañana | Almuerzo | Merienda | Cena`

> **Nota**: MealTime es independiente del MealType del plato — el usuario elige libremente el momento al agregar un item al plan.

### PlanType
`Semanal | Mensual`

---

## 10. Requisitos Funcionales

### RF-001 — Infraestructura Base (ALIM-MOB-001)
- El proyecto arranca con SQLite inicializado (schema completo, 6 tablas + índices)
- Sistema de migraciones versionado (`DatabaseHelper.onUpgrade`)
- Bottom Navigation con 5 tabs funcionales
- Tema visual aplicado (paleta + Material 3)
- Componentes base: `LoadingSkeleton`, `ConfirmDialog`, `SearchBarWidget`, `EmptyState`, `BottomSheetPicker`
- Capa Repository con `BaseRepository<T>` genérico
- Riverpod configurado como gestión de estado
- Arquitectura i18n preparada (AppLocalizations) — solo `es` en MVP
- Botón "Cargar datos de ejemplo" en pantalla de bienvenida/settings (datos de comida peruana)

### RF-002 — CRUD Categorías (ALIM-MOB-002)
- Listado alfabético con búsqueda local (`LIKE`)
- FAB crear, tap editar, swipe-left eliminar (con `ConfirmDialog`)
- Validaciones: nombre requerido (max 100), único (case-insensitive)
- Protección eliminación: bloquear si tiene ingredientes asociados
- Feedback: Toast/Snackbar en cada operación
- Pull-to-refresh

### RF-003 — CRUD Unidades (ALIM-MOB-003)
- Listado con nombre + símbolo (badge)
- Validaciones: nombre requerido (max 50), símbolo requerido (max 10), nombre único
- Protección eliminación: bloquear si tiene ingredientes asociados

### RF-004 — CRUD Ingredientes (ALIM-MOB-004)
- Listado con badges de categoría, símbolo unidad, días maduración
- Selección de Unidad y Categoría via `BottomSheetPicker` buscable
- Campo "Días de maduración" condicional (visible solo si `IsPerishable = true`)
- Validación: si perecible → días > 0; si no perecible → días = null
- Protección eliminación: bloquear si está en algún `DishIngredients`
- Búsqueda con JOIN (nombre, categoría, unidad)

### RF-005 — CRUD Platos (ALIM-MOB-005)
- Listado con tipo (badge), conteo de ingredientes
- Formulario: nombre, descripción (opcional), MealType (Picker)
- Lista dinámica de ingredientes: `BottomSheetPicker` + campo cantidad
- Botón "X" para quitar ingrediente
- Validaciones: ≥1 ingrediente, cantidades > 0, sin ingredientes duplicados
- Guardar/editar en transacción SQLite (BEGIN/COMMIT)
- Protección eliminación: bloquear si está en `MealPlanItems`

### RF-006 — Plan de Comidas (ALIM-MOB-006)
- Listado con tipo (badge), fechas, conteo de items
- Formulario: PlanType Picker, DatePicker inicio/fin
- Lista dinámica de items: fecha (DatePicker) + MealTime (Picker) + Plato (BottomSheetPicker)
- Validaciones: EndDate > StartDate, ≥1 item, fechas de items dentro del rango
- Guard: si no hay platos → mostrar mensaje + botón "Crear plato primero"
- Vista detalle: items agrupados por fecha
- Guardar en transacción

### RF-007 — Lista de Compras (ALIM-MOB-007)
- Botón "Generar Lista" en pantalla detalle del plan
- Algoritmo de agrupación ejecutado localmente (Service layer)
- Planes mensuales: 3 secciones (Listos ≤7d, Comprar verdes >7d, Otros no perecibles)
- Planes semanales: lista única sin segmentación
- Cada item: nombre, cantidad total, unidad, categoría
- Secciones colapsables con contador
- Botón "Regenerar"
- Botón "Exportar PDF" → genera PDF localmente + Share Sheet nativo
- PDF: encabezado (nombre plan + rango fechas), tabla con secciones, UTF-8

### RF-008 — Backup y Restauración (ALIM-MOB-008)
- Pantalla "Más" → opción "Backup de datos"
- Exportar: copia el archivo `.db` vía Share Sheet
- Importar: file picker → confirmar ("Esto reemplazará todos sus datos") → reemplazar BD
- Validación: archivo importado debe ser SQLite válido con las 6 tablas esperadas

---

## 11. Requisitos No Funcionales

| ID | Categoría | Requisito |
|----|-----------|-----------|
| RNF-001 | Performance | Respuesta UI < 300ms para operaciones de lista (< 10,000 registros) |
| RNF-002 | Usabilidad | Haptic feedback en acciones destructivas (eliminar, importar backup) |
| RNF-003 | Usabilidad | Skeleton screens mientras carga desde BD |
| RNF-004 | Usabilidad | Pull-to-refresh en todos los listados |
| RNF-005 | Usabilidad | Swipe-to-delete con `ConfirmDialog` en todos los listados |
| RNF-006 | Responsive | Layouts adaptativos para teléfonos y tablets |
| RNF-007 | i18n | Arquitectura AppLocalizations lista; solo `es` en MVP |
| RNF-008 | Persistencia | Datos viven exclusivamente en dispositivo — sin sincronización |
| RNF-009 | Migración BD | Schema versionado — `onUpgrade` ejecuta scripts incrementales |
| RNF-010 | Offline | App 100% offline — cero dependencias de red |

---

## 12. Reglas de Negocio Confirmadas

### Categorías
- RN-001: Nombre obligatorio, max 100 chars
- RN-002: Nombre único (case-insensitive)
- RN-003: No eliminar si tiene ingredientes

### Unidades
- RN-001: Nombre obligatorio, max 50 chars; Símbolo obligatorio, max 10 chars
- RN-002: Nombre único
- RN-003: No eliminar si referenciada por ingredientes

### Ingredientes
- RN-001: Nombre obligatorio, max 100 chars, único
- RN-002/003: FK UnitId y CategoryId deben existir
- RN-004: IsPerishable=true → RipeningDays > 0
- RN-005: IsPerishable=false → RipeningDays = null
- RN-006: No eliminar si está en DishIngredients

### Platos
- RN-001: Nombre obligatorio, max 100 chars
- RN-002: MealType obligatorio (Desayuno/Almuerzo/Cena/Snack/Postre)
- RN-003: Al menos 1 ingrediente
- RN-004: Cantidad de cada ingrediente > 0
- RN-005: No eliminar si está en MealPlanItems
- RN-006: Sin ingredientes duplicados en el mismo plato

### Planes de Comida
- RN-001: PlanType obligatorio (Semanal/Mensual)
- RN-002: StartDate y EndDate obligatorias
- RN-003: EndDate > StartDate
- RN-004: Al menos 1 item
- RN-005: Fechas de items dentro del rango del plan

### Lista de Compras (Algoritmo)
- Agrupación y suma de cantidades por ingrediente
- Segmentación (solo planes mensuales): Listos ≤7d / Verdes >7d / No perecibles
- Lógica en Service layer (no en SQL)

---

## 13. Pantallas

| # | Pantalla | Tipo | HU |
|---|----------|------|----|
| 1 | Home / Dashboard | Tab | MOB-001 |
| 2 | Catálogos hub | Tab | MOB-001 |
| 3 | Categorías — Lista | Stack | MOB-002 |
| 4 | Categorías — Form | Stack | MOB-002 |
| 5 | Unidades — Lista | Stack | MOB-003 |
| 6 | Unidades — Form | Stack | MOB-003 |
| 7 | Ingredientes — Lista | Stack | MOB-004 |
| 8 | Ingredientes — Form | Stack | MOB-004 |
| 9 | Platos — Lista | Stack | MOB-005 |
| 10 | Platos — Form | Stack | MOB-005 |
| 11 | Planes — Lista | Stack | MOB-006 |
| 12 | Planes — Form | Stack | MOB-006 |
| 13 | Plan — Detalle | Stack | MOB-006/007 |
| 14 | Lista de Compras | Stack | MOB-007 |
| 15 | Más (Settings) | Tab | MOB-001/008 |

---

## 14. Datos Semilla (Comida Peruana)

Accesibles vía botón "Cargar datos de ejemplo" en Settings. No se cargan automáticamente.

**Categorías sugeridas**: Tubérculos, Cereales y granos, Carnes, Aves, Mariscos, Verduras, Frutas, Lácteos, Especias y condimentos, Aceites y grasas

**Unidades sugeridas**: Kilogramo (kg), Gramo (g), Litro (L), Mililitro (ml), Unidad (un), Taza (tz), Cucharada (cda), Cucharadita (cdta), Porción (por)

**Ingredientes semilla (muestra)**: Papa amarilla, Camote, Yuca, Arroz blanco, Quinua, Pollo, Carne de res, Limón, Ají amarillo, Ají panca, Culantro, etc.

**Platos semilla (muestra)**: Lomo saltado, Ceviche, Ají de gallina, Arroz con leche, etc.

---

## 15. Dependencias Flutter (pubspec.yaml)

| Paquete | Versión | Uso |
|---------|---------|-----|
| `flutter_riverpod` | ^2.6.x | Estado global |
| `riverpod_annotation` | ^2.6.x | Code generation providers |
| `sqflite` | ^2.4.x | Base de datos SQLite |
| `path` | ^1.9.x | Rutas de archivos (BD) |
| `path_provider` | ^2.1.x | Directorio de BD en dispositivo |
| `shared_preferences` | ^2.3.x | Preferencia de tema |
| `pdf` | ^3.11.x | Generación PDF local |
| `printing` | ^5.13.x | Share / imprimir PDF |
| `share_plus` | ^10.x | Share Sheet nativo |
| `file_picker` | ^8.x | Importar backup .db |
| `intl` | ^0.19.x | Formato fechas + i18n |
| `flutter_localizations` | SDK | AppLocalizations |

**Dev dependencies**:
| Paquete | Uso |
|---------|-----|
| `riverpod_generator` | Code gen para providers |
| `build_runner` | Code generation |
| `flutter_test` | Unit + Widget tests |

---

## 16. Orden de Implementación (HUs)

```
ALIM-MOB-001 (Base + BD + Navegación + Tema)
         ↓
ALIM-MOB-002 + ALIM-MOB-003 (Catálogos — paralelo)
         ↓
ALIM-MOB-004 (Ingredientes)
         ↓
ALIM-MOB-005 (Platos)
         ↓
ALIM-MOB-006 (Planes de Comida)
         ↓
ALIM-MOB-007 (Lista de Compras + PDF)
         ↓
ALIM-MOB-008 (Backup / Restauración)
```

---

## 17. Fuera de Alcance (MVP)

- Sincronización con servidor / nube
- Múltiples usuarios / perfiles
- Notificaciones push
- Integración con calendarios externos
- Imágenes de platos o ingredientes
- Historial de planes ejecutados
- Calculadora nutricional
- Autenticación de cualquier tipo

---
