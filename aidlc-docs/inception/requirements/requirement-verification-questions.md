# Preguntas de Verificación de Requisitos — ALIM-MOB

> Por favor responde cada pregunta llenando la letra elegida después del tag `[Answer]:`.
> Si ninguna opción se ajusta, elige la última opción (X/Otra) y describe tu preferencia.
> Avísame cuando termines.

---

## Pregunta 1
El spec menciona Flutter como opción preferida (Opción A) y el proyecto ya existe como proyecto Flutter. ¿Confirmamos Flutter/Dart como el framework definitivo?

A) Sí, Flutter/Dart — usar `sqflite` o `drift` para SQLite
B) Sí, Flutter/Dart — pero quiero que me sugieras cuál paquete SQLite usar
C) No, prefiero otro framework (indica cuál después de [Answer]:)

[Answer]: A

---

## Pregunta 2
Para el manejo de estado en Flutter, ¿tienes alguna preferencia?

A) `Riverpod` (moderno, type-safe, el más recomendado actualmente)
B) `Provider` (estable, ampliamente usado)
C) `BLoC/Cubit` (patrón más estructurado, verboso)
D) `GetX` (todo-en-uno: estado, rutas, inyección)
E) Sin preferencia — que lo decidas tú según el proyecto
X) Otro (describe después de [Answer]:)

[Answer]: A

---

## Pregunta 3
El spec menciona generación de PDF. ¿Qué importancia tiene esta funcionalidad para el MVP?

A) Crítica — debe estar en la primera versión junto con todo lo demás
B) Alta — debe estar en el Sprint 3 como dice el spec
C) Media — se puede dejar para una versión posterior si el tiempo apremia
D) Baja — es nice-to-have, podría empezar solo con "compartir texto" nativo

[Answer]: B

---

## Pregunta 4
Para la pantalla "Más" (tab 5), el spec menciona: Configuración, Backup y About. ¿Qué necesitas del MVP en esa sección?

A) Solo Backup/Restauración (MOB-008) y About básico
B) Backup + Configuración básica (por ejemplo, tema claro/oscuro)
C) Todo lo mencionado en el spec: Backup, Configuración completa, About
D) Solo About — el backup puede esperar
X) Otro (describe después de [Answer]:)

[Answer]: B

---

## Pregunta 5
Los "Momentos" del día en un plan de comidas (MealTime). El spec muestra el mismo valor que MealType del plato, pero podrían ser distintos. ¿Cómo se manejan?

A) El MealTime del plan item debe coincidir con el MealType del plato (mismo picker: Desayuno/Almuerzo/Cena/Snack/Postre)
B) El MealTime es independiente — el usuario elige cualquier momento sin importar el tipo del plato
C) Mostrar los platos del plan agrupados por MealType del plato (no del item)
X) Otro (describe después de [Answer]:)

[Answer]: B

---

## Pregunta 6
¿La app necesita soporte para tablet/iPad además de teléfonos?

A) Solo teléfonos (phones) — diseño mobile-first
B) Teléfonos y tablets — diseño responsive adaptativo
C) Sin preferencia — que quede bien en teléfonos; tablet es bonus

[Answer]: B

---

## Pregunta 7
Para el idioma/localización, ¿se requiere soporte multi-idioma en el futuro o siempre será solo español?

A) Siempre solo español — no vale la pena implementar i18n
B) Solo español ahora, pero quiero arquitectura lista para agregar idiomas después
C) No importa — lo que sea más rápido de implementar

[Answer]: B

---

## Pregunta 8
El spec menciona "Momentos" (MealTime) en los items del plan. ¿Los valores son los mismos que MealType o diferentes? Ejemplo de opciones posibles:

A) Mismos que MealType: Desayuno, Almuerzo, Cena, Snack, Postre
B) Solo los principales: Desayuno, Almuerzo, Cena (sin Snack/Postre)
C) Más granular: Desayuno, Media mañana, Almuerzo, Merienda, Cena
X) Otro (describe después de [Answer]:)

[Answer]: C

---

## Pregunta 9
Para el esquema SQLite, el spec tiene todas las tablas sin campos de auditoría (CreatedAt existe, pero no UpdatedAt). ¿Necesitas rastrear fecha de modificación en las entidades?

A) Sí, agregar `UpdatedAt` a todas las tablas principales
B) Solo `CreatedAt` como está en el spec — es suficiente para uso personal
C) No necesito ninguna fecha — simplifica el esquema

[Answer]: B

---

## Pregunta 10
¿Tienes datos de prueba o datos semilla que quieras cargar automáticamente la primera vez que se instale la app? (ej: categorías y unidades comunes pre-cargadas)

A) Sí, quiero datos semilla: algunas categorías y unidades comunes de ejemplo
B) No — la app arranca vacía, el usuario agrega todo desde cero
C) Opcional — que sea configurable (botón "Cargar datos de ejemplo")

[Answer]: C, que mencione que serán de comida peruana

---
