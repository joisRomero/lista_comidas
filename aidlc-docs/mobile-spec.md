# Especificación Técnica — Alimentación Mobile

## 1. Resumen Ejecutivo

**Objetivo**: Replicar el sistema web "Alimentación" como aplicación móvil standalone con base de datos local, sin depender de ninguna API externa.

**Sistema origen**: Blazor WebAssembly (referencia funcional)  
**Enfoque mobile**: App **completamente autónoma** con BD local embebida. Toda la lógica de negocio se reimplementa en el dispositivo.  
**Autenticación**: Sin autenticación (proyecto personal monousuario)

---

## 2. Arquitectura

```
┌──────────────────────────────────────────┐
│            App Móvil Standalone           │
│                                          │
│  ┌──────────┐   ┌──────────┐   ┌─────┐  │
│  │  UI /    │   │ Lógica   │   │ BD  │  │
│  │ Screens  │ → │ Negocio  │ → │Local│  │
│  │          │   │ (Repos)  │   │     │  │
│  └──────────┘   └──────────┘   └─────┘  │
│                                          │
└──────────────────────────────────────────┘
```

**NO hay comunicación con servidores externos.** Todo vive en el dispositivo.

### Stack Recomendado (opciones)

| Opción | Framework | BD Local | Ventajas |
|--------|-----------|----------|----------|
| A | **Flutter** (Dart) | SQLite (sqflite / drift) | Cross-platform, rendimiento, gran ecosistema |
| B | **React Native** (TypeScript) | SQLite (expo-sqlite / WatermelonDB) | Reutiliza conocimiento web |
| C | **.NET MAUI** (C#) | SQLite (sqlite-net-pcl) | Mismo lenguaje que el sistema web, comparte DTOs |
| D | **Kotlin/Swift nativo** | Room (Android) / CoreData (iOS) | Performance nativa máxima |

### Base de Datos Local Recomendada

**SQLite** — embebida, sin servidor, ideal para apps móviles standalone.

### Estructura del Proyecto

```
alimentacion-mobile/
├── src/
│   ├── database/
│   │   ├── schema.sql            # Definición de tablas
│   │   ├── migrations/           # Migraciones incrementales
│   │   ├── DatabaseHelper.{ext}  # Conexión y setup
│   │   └── repositories/        # Acceso a datos por entidad
│   │       ├── CategoryRepository
│   │       ├── UnitRepository
│   │       ├── IngredientRepository
│   │       ├── DishRepository
│   │       └── MealPlanRepository
│   ├── models/                   # Entidades y DTOs
│   ├── services/                 # Lógica de negocio
│   │   ├── CategoryService
│   │   ├── UnitService
│   │   ├── IngredientService
│   │   ├── DishService
│   │   ├── MealPlanService
│   │   └── ShoppingListService
│   ├── screens/                  # Pantallas
│   │   ├── home/
│   │   ├── categories/
│   │   ├── units/
│   │   ├── ingredients/
│   │   ├── dishes/
│   │   ├── mealplans/
│   │   └── shopping-list/
│   ├── components/               # Componentes reutilizables
│   ├── navigation/               # Router / navegación
│   └── utils/                    # Helpers, constantes
├── assets/                       # Iconos, fuentes
└── tests/                        # Unit + Widget tests
```

---

## 3. Esquema de Base de Datos Local (SQLite)

### 3.1 Diagrama ER

```
Categories (1) ──────── (N) Ingredients (N) ──── (N) DishIngredients (N) ──── (1) Dishes
Units (1) ─────────────── (N) Ingredients
Dishes (1) ────────────── (N) MealPlanItems (N) ──── (1) MealPlans
```

### 3.2 DDL — Definición de Tablas

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

-- Índices para rendimiento
CREATE INDEX IX_Ingredients_CategoryId ON Ingredients(CategoryId);
CREATE INDEX IX_Ingredients_UnitId ON Ingredients(UnitId);
CREATE INDEX IX_DishIngredients_DishId ON DishIngredients(DishId);
CREATE INDEX IX_DishIngredients_IngredientId ON DishIngredients(IngredientId);
CREATE INDEX IX_MealPlanItems_MealPlanId ON MealPlanItems(MealPlanId);
CREATE INDEX IX_MealPlanItems_DishId ON MealPlanItems(DishId);
CREATE INDEX IX_MealPlanItems_Date ON MealPlanItems(Date);
```

### 3.3 Notas sobre SQLite

- `INTEGER` para booleanos (0 = false, 1 = true)
- `TEXT` para fechas en formato ISO 8601 (`2026-07-10T00:00:00`)
- `REAL` para decimales (cantidades)
- `ON DELETE CASCADE` en DishIngredients y MealPlanItems para limpiar hijos al eliminar padres
- **NO cascade** en Ingredients → Categories/Units (protección de eliminación por lógica de negocio)

---

## 4. Lógica de Negocio (reimplementar en mobile)

### 4.1 Reglas de Negocio por Entidad

#### Categorías
| Regla | Descripción | Implementar en |
|-------|-------------|----------------|
| RN-001 | Nombre obligatorio, max 100 chars | Validación UI + Repository |
| RN-002 | Nombre único (case-insensitive) | Repository (query antes de INSERT) |
| RN-003 | No eliminar si tiene ingredientes | Repository (COUNT antes de DELETE) |

#### Unidades
| Regla | Descripción | Implementar en |
|-------|-------------|----------------|
| RN-001 | Nombre obligatorio, max 50 chars | Validación UI + Repository |
| RN-002 | Símbolo obligatorio, max 10 chars | Validación UI |
| RN-003 | Nombre único | Repository |
| RN-004 | No eliminar si referenciada por ingredientes | Repository |

#### Ingredientes
| Regla | Descripción | Implementar en |
|-------|-------------|----------------|
| RN-001 | Nombre obligatorio, max 100 chars | Validación UI |
| RN-002 | UnitId debe existir en Units | Repository (FK) |
| RN-003 | CategoryId debe existir en Categories | Repository (FK) |
| RN-004 | Si IsPerishable = true → RipeningDays > 0 | Service / Validación UI |
| RN-005 | Si IsPerishable = false → RipeningDays = null | Service |
| RN-006 | No eliminar si está en DishIngredients | Repository |

#### Platos
| Regla | Descripción | Implementar en |
|-------|-------------|----------------|
| RN-001 | Nombre obligatorio, max 100 chars | Validación UI |
| RN-002 | MealType obligatorio (Desayuno/Almuerzo/Cena/Snack/Postre) | Validación UI |
| RN-003 | Al menos 1 ingrediente | Service |
| RN-004 | Cantidad de cada ingrediente > 0 | Validación UI + Service |
| RN-005 | No eliminar si está en MealPlanItems | Repository |
| RN-006 | Sin ingredientes duplicados en el mismo plato | Service |

#### Planes de Comida
| Regla | Descripción | Implementar en |
|-------|-------------|----------------|
| RN-001 | PlanType obligatorio (Semanal/Mensual) | Validación UI |
| RN-002 | StartDate y EndDate obligatorias | Validación UI |
| RN-003 | EndDate > StartDate | Service |
| RN-004 | Al menos 1 item | Service |
| RN-005 | Fechas de items dentro del rango del plan | Service |

### 4.2 Lógica de Lista de Compras (algoritmo)

```
FUNCIÓN GenerarListaDeCompras(mealPlanId):
    plan = obtenerPlanConItems(mealPlanId)
    
    // 1. Agregar todos los ingredientes de todos los platos del plan
    ingredientesAgrupados = {}
    
    PARA CADA item EN plan.items:
        plato = obtenerPlatoConIngredientes(item.dishId)
        PARA CADA di EN plato.dishIngredients:
            ingrediente = obtenerIngrediente(di.ingredientId)
            SI ingredientesAgrupados CONTIENE ingrediente.id:
                ingredientesAgrupados[ingrediente.id].cantidad += di.quantity
            SINO:
                ingredientesAgrupados[ingrediente.id] = {
                    nombre: ingrediente.name,
                    cantidad: di.quantity,
                    unidad: ingrediente.unit.symbol,
                    categoria: ingrediente.category.name,
                    esPerecible: ingrediente.isPerishable,
                    diasMaduracion: ingrediente.ripeningDays
                }
    
    // 2. Segmentar según tipo de plan
    SI plan.planType == "Mensual":
        listosParaComer = filtrar(esPerecible Y diasMaduracion <= 7)
        comprarVerdes = filtrar(esPerecible Y diasMaduracion > 7)
        otrosProductos = filtrar(NO esPerecible)
    SINO:  // Semanal
        listosParaComer = todos los ingredientes (sin segmentar)
        comprarVerdes = []
        otrosProductos = []
    
    RETORNAR { listosParaComer, comprarVerdes, otrosProductos }
```

### 4.3 Generación de PDF (en dispositivo)

Para generar el PDF localmente sin servidor:

| Framework | Librería Recomendada |
|-----------|---------------------|
| Flutter | `pdf` + `printing` (dart:pdf) |
| React Native | `react-native-html-to-pdf` o `expo-print` |
| .NET MAUI | `QuestPDF` o `iText` |
| Kotlin | `iText` o `Android PdfDocument` |

El PDF debe contener:
- Encabezado: nombre del plan + rango de fechas
- Tabla: ingrediente, cantidad, unidad, categoría
- Segmentación por secciones (si plan mensual)
- Encoding UTF-8 para español (ñ, tildes)

---

## 5. Paleta de Colores y Diseño

### Colores principales

| Variable | Hex | Uso |
|----------|-----|-----|
| Color primario | `#4050E2` | Headers, botones principales, acentos |
| Color secundario | `#40A1E2` | Links, badges, estados activos |
| Color terciario | `#40E2D2` | Éxito, highlights, bordes decorativos |

### UX Mobile

- **Bottom Tab Navigation**: 5 tabs (Inicio, Catálogos, Recetas, Planes, Más)
- **Pull-to-refresh**: en listados (refresca desde BD local)
- **Swipe-to-delete**: con confirmación dialog
- **Floating Action Button (FAB)**: para "Nuevo" en cada listado
- **Search bar**: búsqueda local con filtrado en memoria o query SQL LIKE
- **Toast/Snackbar**: nativo para feedback de operaciones
- **Bottom Sheet**: para selects con búsqueda (reemplaza dropdown)
- **Haptic feedback**: en acciones destructivas
- **Skeleton screens**: mientras carga datos de BD

---

## 6. Pantallas a Implementar

| # | Pantalla | Tipo | Descripción |
|---|----------|------|-------------|
| 1 | Home / Dashboard | Tab | Cards de acceso rápido a módulos |
| 2 | Categorías - Lista | Tab/Stack | Listado con búsqueda local |
| 3 | Categorías - Form | Stack | Crear / Editar categoría |
| 4 | Unidades - Lista | Tab/Stack | Listado con búsqueda local |
| 5 | Unidades - Form | Stack | Crear / Editar unidad |
| 6 | Ingredientes - Lista | Tab/Stack | Listado con badges + búsqueda |
| 7 | Ingredientes - Form | Stack | Crear / Editar con bottom sheets |
| 8 | Platos - Lista | Tab/Stack | Listado con badge de tipo |
| 9 | Platos - Form | Stack | Crear / Editar con ingredientes dinámicos |
| 10 | Planes - Lista | Tab/Stack | Listado con badge tipo + fechas |
| 11 | Planes - Form | Stack | Crear / Editar con selector de platos por día |
| 12 | Plan - Detalle | Stack | Items agrupados por fecha + generar lista |
| 13 | Lista de Compras | Stack | Segmentación visual + exportar/compartir PDF |

---

## 7. Navegación

```
Bottom Tabs
├── Inicio (Dashboard)
├── Catálogos
│   ├── Categorías (lista → form)
│   └── Unidades (lista → form)
├── Recetas
│   ├── Ingredientes (lista → form)
│   └── Platos (lista → form)
├── Planes
│   ├── Lista de planes → Detalle → Lista de Compras
│   └── Crear / Editar plan
└── Más (Configuración, Backup, About)
```

---

## 8. Consideraciones Técnicas

### Almacenamiento y Performance

- SQLite es extremadamente rápida para volúmenes de un usuario personal (< 10,000 registros)
- No necesita paginación server-side: la paginación puede ser en memoria o con `LIMIT/OFFSET` SQL
- Búsqueda con `LIKE '%term%'` es suficiente para el volumen esperado

### Backup / Exportación de Datos

- Ofrecer opción de **exportar BD** (copiar el archivo .db) como backup
- Opción de **importar BD** para restaurar datos
- Considerar export a JSON para portabilidad

### Migraciones de BD

- Versionar el schema con un número de versión
- Al actualizar la app, ejecutar migraciones incrementales
- Ejemplo: `onUpgrade(oldVersion, newVersion)` con scripts por versión

### Ciclo de Vida de Datos

- No hay sincronización con servidor — datos viven solo en el dispositivo
- Advertir al usuario si desinstala la app se pierden los datos
- Ofrecer funcionalidad de backup periódico

---
