---
name: html-prototype
description: >
  Generates interactive HTML mockups that look like the final ANTA app using HTML + CSS + minimal JS.
  Trigger: After Requirements Analysis when stakeholder approval of screens is needed before API design.
metadata:
  author: anta
  version: "2.1"
  scope: [root]
  enforcement: optional
  auto_invoke: "prototipo, mockup, pantalla, wireframe, html prototype, aprobacion visual"
  phase: [inception]
  layer: null
  validates_with: validate_html_prototype
  validation_profile: prototype-gate
---

## Purpose

Generate interactive HTML mockups for stakeholder review after Requirements Analysis and before API
design. Each prototype represents one screen of the final application using HTML + CSS + a pre-built
interaction script — no custom JavaScript, no frameworks, no CDN dependencies.

Stakeholders open files directly in a browser and click through screens, toggle modals, switch tabs,
and see workflow state variations — all before any backend work begins.

**Interactivity model**: The agent writes `data-*` attributes. A pre-built `prototype-interactions.js`
handles all behavior. The agent NEVER writes custom JavaScript.

---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Use ONLY `anta-prototype.css` | ALWAYS | Single source of truth for ANTA visual style |
| Copy `anta-prototype.css` + `prototype-interactions.js` into output folder | ALWAYS | Prototype bundle is portable |
| Link CSS with `<link rel="stylesheet" href="./anta-prototype.css">` | ALWAYS | Relative to output file |
| Include `<script src="./prototype-interactions.js"></script>` before `</body>` | ALWAYS | Enables data-* interactivity |
| Zero CUSTOM JavaScript | NEVER | Agent writes data-* attributes only, never `<script>` blocks or inline JS |
| Zero external CDN references | NEVER | Must work offline without internet |
| Zero inline styles | NEVER | Use CSS classes from `anta-prototype.css` only |
| One HTML file per screen | ALWAYS | Keeps review granular and focused |
| Spanish labels and field names | ALWAYS | End users are Spanish-speaking |
| English for CSS class names and data-testid | ALWAYS | Code identifiers stay in English |
| Include `data-testid` on interactive elements | ALWAYS | QA team uses them in Playwright tests |
| Use ONLY classes defined in `anta-prototype.css` or listed in this skill's Component Catalog | ALWAYS | If a class doesn't exist, use existing utility classes. NEVER invent class names |
| Use ONLY CSS variables defined in `:root` of `anta-prototype.css` | ALWAYS | Use `var(--error)` not `var(--danger)`, `var(--bg-page)` not `var(--color-bg-page)` |
| Tab panels: NEVER use `hidden` attribute | ALWAYS | Use presence/absence of `.anta-visible` class — `hidden` overrides JS toggle and breaks tab switching |
| Card content MUST be wrapped in `.anta-card-body` | ALWAYS | `.anta-card` has zero padding — all padding comes from `.anta-card-body` |

---

## Interactivity API (data-* attributes)

The agent adds these attributes to HTML elements. `prototype-interactions.js` handles all behavior.

| Attribute | Element | Behavior | Example |
|-----------|---------|----------|---------|
| `data-navigate="./page.html"` | button, a | Click navigates to URL | `<button data-navigate="./employee-create.html">Nuevo</button>` |
| `data-toggle="#modalId"` | button | Click toggles `.anta-visible` on target | `<button data-toggle="#deleteModal">Eliminar</button>` |
| `data-dismiss="modal"` | button | Click hides closest `.anta-modal-overlay` | `<button data-dismiss="modal">Cancelar</button>` |
| `data-tab="name"` | button, a | Click activates tab within `data-tab-group` | `<a data-tab="personal">Datos Personales</a>` |
| `data-tab-panel="name"` | div | Shown when matching tab is active | `<div data-tab-panel="personal">...</div>` |
| `data-tab-group` | div | Container for tabs + panels | `<div data-tab-group>...</div>` |
| `data-state-select` | select | Drives visibility of `data-show-state` elements | `<select data-state-select>...</select>` |
| `data-show-state="DRAFT"` | any | Visible only when state-select matches | `<div data-show-state="DRAFT">...</div>` |
| `data-state-container` | div | Scopes state visibility to a section | `<div data-state-container>...</div>` |
| `data-validate-error` | input | Adds `.anta-field-error` to parent form-item | `<input data-validate-error>` |

### Modal Pattern

```html
<!-- Trigger button -->
<button data-toggle="#approveModal" class="btn btn-primary">Aprobar</button>

<!-- Modal (starts hidden — no .anta-visible class) -->
<div id="approveModal" class="anta-modal-overlay">
  <div class="anta-modal">
    <div class="anta-modal-header">
      <span class="anta-modal-title">Confirmar Aprobación</span>
      <button class="anta-modal-close" data-dismiss="modal">&times;</button>
    </div>
    <div class="anta-modal-body">
      <p>¿Confirma la aprobación de este registro?</p>
      <div class="anta-form-item">
        <label class="anta-form-label">Comentario (opcional)</label>
        <textarea class="anta-textarea" placeholder="Agregue un comentario..."></textarea>
      </div>
    </div>
    <div class="anta-modal-footer">
      <button class="btn btn-default" data-dismiss="modal">Cancelar</button>
      <button class="btn btn-primary">Confirmar</button>
    </div>
  </div>
</div>
```

### Workflow State Switcher Pattern

Use on detail pages to let stakeholders preview ALL workflow states in one screen:

```html
<div data-state-container>
  <select data-state-select class="anta-select mb-lg">
    <option value="DRAFT">Vista: Borrador</option>
    <option value="SUBMITTED">Vista: En Revisión</option>
    <option value="APPROVED">Vista: Aprobado</option>
    <option value="REJECTED">Vista: Rechazado</option>
  </select>

  <div data-show-state="DRAFT" class="anta-action-bar">
    <button class="btn btn-primary">Enviar a Aprobación</button>
    <button class="btn btn-default">Editar</button>
    <button class="btn btn-danger">Eliminar</button>
  </div>
  <div data-show-state="SUBMITTED" class="anta-action-bar">
    <button class="btn btn-primary" data-toggle="#approveModal">Aprobar</button>
    <button class="btn btn-danger" data-toggle="#rejectModal">Rechazar</button>
  </div>
  <div data-show-state="APPROVED" class="anta-action-bar">
    <span class="text-muted">Solo lectura — sin acciones disponibles</span>
  </div>
  <div data-show-state="REJECTED" class="anta-action-bar">
    <button class="btn btn-default">Editar</button>
    <button class="btn btn-primary">Devolver a Borrador</button>
  </div>
</div>
```

### Validation Error Pattern

```html
<div class="anta-form-item">
  <label class="anta-form-label">Email <span class="anta-form-required">*</span></label>
  <input type="email" class="anta-input" value="correo-invalido" data-validate-error>
  <span class="anta-form-error">Ingrese un email válido</span>
</div>
```

### Tab Pattern

```html
<div data-tab-group>
  <div class="anta-tabs">
    <div class="anta-tabs-nav" role="tablist">
      <a class="anta-tab anta-tab--active" data-tab="general" role="tab">General</a>
      <a class="anta-tab" data-tab="participants" role="tab">Participantes <span class="anta-badge anta-badge--gray">25</span></a>
      <a class="anta-tab" data-tab="history" role="tab">Historial</a>
    </div>
  </div>

  <!-- First panel: add .anta-visible to show by default -->
  <div data-tab-panel="general" class="anta-visible">
    <p>Contenido del tab General...</p>
  </div>

  <!-- Other panels: NO .anta-visible, NO hidden attribute -->
  <div data-tab-panel="participants">
    <p>Contenido del tab Participantes...</p>
  </div>
  <div data-tab-panel="history">
    <p>Contenido del tab Historial...</p>
  </div>
</div>
```

**CRITICAL**:
- Tab buttons use class `anta-tab` (NOT `anta-tabs-tab`)
- Active tab uses `anta-tab--active` (NOT `anta-tabs-tab--active`)
- Tab panels use `data-tab-panel` WITHOUT the `hidden` attribute
- First panel gets `.anta-visible`, others have no visibility class
- JS toggles `.anta-visible` — `hidden` attribute would override this

### Form Hint Pattern

```html
<div class="anta-form-item">
  <label class="anta-form-label" for="capacity">Capacidad <span class="anta-form-required">*</span></label>
  <input type="number" id="capacity" class="anta-input" min="1" value="30" />
  <span class="anta-form-hint">Numero maximo de participantes permitidos</span>
</div>
```

Use `anta-form-hint` for helper text below inputs. Do NOT use `anta-form-help` (does not exist).

### Card Pattern

```html
<!-- CORRECT: content inside .anta-card-body for proper padding -->
<div class="anta-card">
  <div class="anta-card-body">
    <h3>Titulo de seccion</h3>
    <p>Contenido con padding correcto.</p>
  </div>
</div>

<!-- With header -->
<div class="anta-card">
  <div class="anta-card-header">
    <span class="anta-card-title">Titulo</span>
  </div>
  <div class="anta-card-body">
    <p>Contenido...</p>
  </div>
</div>
```

**CRITICAL**: `.anta-card` has zero padding. ALL content must go inside `.anta-card-body` (or `.anta-card-header` for titles). Placing content directly inside `.anta-card` results in text touching the edges.

---

## Output Location

Save all generated prototypes to:

```
aidlc-docs/inception/prototypes/{screen-name}.html
```

Also copy the CSS file so stakeholders receive a self-contained folder:

```
aidlc-docs/inception/prototypes/
  anta-prototype.css              ← copy from config/skills/html-prototype/assets/
  prototype-interactions.js       ← copy from config/skills/html-prototype/assets/
  index.html
  lista-empleados.html
  crear-empleado.html
  detalle-empleado.html
```

Naming convention: `kebab-case` matching the feature.

---

## Page Types

### 1. List Page

Use when: Showing a paginated table of records with search and filters.

Structure:
- `.anta-layout` wrapping `.anta-sidebar` + `.anta-content`
- `.anta-header` with page title + icon + record count
- `.anta-toolbar` with primary action button ("Nuevo...") + secondary actions (Export)
- `.anta-filters` row with search input + filter selects
- `.anta-table` with striped rows, hover state, `.anta-badge` per status column
- `.anta-pagination` at the bottom

Minimum mock data: 5 rows with varied statuses (BORRADOR, EN_REVISION, APROBADO, RECHAZADO).

### 2. Form Page (Create / Edit)

Use when: Showing a form to create or update a record.

Structure:
- `.anta-layout` with sidebar + content
- `.anta-breadcrumb` (e.g., Inicio > Empleados > Nuevo Empleado)
- `.anta-page-header` with title
- `.anta-card` wrapping a `.anta-form`
- `.anta-form-row` for grouping fields side-by-side (2 columns max)
- `.anta-form-item` for each field: label + input/select/textarea
- Validation states: `.anta-form-item--error` with `.anta-form-error` message
- `.anta-form-actions` with Save (`.btn-primary`) + Cancel (`.btn-default`) buttons

Required field types to demonstrate: text input, email input, select/dropdown, date input,
textarea, number input.

### 3. Detail Page (View)

Use when: Showing a read-only view of a single record with status-dependent actions.

Structure:
- `.anta-layout` with sidebar + content
- `.anta-breadcrumb`
- `.anta-page-header` with title + `.anta-badge` showing current status
- `.anta-card` with `.anta-descriptions` grid (label-value pairs, 2 columns)
- `.anta-action-bar` with buttons appropriate to the record status:
  - BORRADOR: "Enviar a Revision" (primary) + "Editar" (default) + "Eliminar" (danger)
  - EN_REVISION: "Aprobar" (primary) + "Rechazar" (danger) — reviewer role only
  - APROBADO: "Archivar" (default)
  - RECHAZADO: "Corregir" (primary)

### 4. Dashboard Page

Use when: Showing KPIs, summary cards, or overview data.

Structure:
- `.anta-layout` with sidebar + content
- `.anta-page-header` with title
- `.anta-stats-grid` with `.anta-stat-card` items (`.anta-stat-label` + `.anta-stat-value` + `.anta-stat-subtext`)
- `.anta-card` for chart placeholders or data tables

### 5. Calendar / Schedule Page

Use when: Showing a date-based grid for scheduling, bookings, or availability.

Structure:
- `.anta-layout` with sidebar + content
- `.anta-page-header` with title + navigation (month prev/next)
- `.anta-filters` with selects (clinic, employee, category)
- Calendar grid: `.anta-table` with 7 columns (Lun-Dom), rows per week
  - Each cell: date number + colored `.anta-badge` chips for events/bookings
  - Empty cells: `.text-muted` date only
  - Use `data-toggle` on cells to open a day-detail modal
- Legend: `.d-flex .gap-sm` with `.anta-badge` samples explaining colors
- Day detail modal: `.anta-modal` showing events for the clicked date

Navigation pattern:
```html
<div class="d-flex align-center gap-sm mb-lg">
  <button class="btn btn-default btn-sm" data-navigate="?month=prev">&lsaquo;</button>
  <span class="text-bold">Junio 2026</span>
  <button class="btn btn-default btn-sm" data-navigate="?month=next">&rsaquo;</button>
</div>
```

### 6. Wizard Page (Multi-step Modal)

Use when: A creation flow requires 2+ steps with validation between them (e.g., Create Group: Basic Data → Associate Items → Configure Rules).

Structure:
- Trigger: `.btn btn-primary` that opens a wizard modal via `data-toggle`
- Modal: `.anta-modal` (wider: add `max-w-900` class or inline `style="max-width:800px"`)
- Steps indicator: ordered list or breadcrumb showing current step
- Step content: one `.anta-card-body` per step, only the active step visible
- Footer: "Anterior" (`.btn-default`) + "Siguiente" / "Crear" (`.btn-primary`)
- Use `data-state-select` + `data-show-state` to switch between steps

```html
<!-- Inside modal body -->
<div class="d-flex gap-sm mb-lg" style="border-bottom: 1px solid var(--border-light); padding-bottom: 12px;">
  <span class="anta-badge anta-badge--approved">1. Datos Basicos</span>
  <span class="anta-badge anta-badge--gray">2. Asociar Items</span>
  <span class="anta-badge anta-badge--gray">3. Configurar Reglas</span>
</div>

<div data-state-container>
  <select data-state-select class="anta-select mb-lg" data-testid="wizard-step">
    <option value="step1">Paso 1</option>
    <option value="step2">Paso 2</option>
    <option value="step3">Paso 3</option>
  </select>

  <div data-show-state="step1">
    <!-- Step 1 form fields -->
  </div>
  <div data-show-state="step2">
    <!-- Step 2 content -->
  </div>
  <div data-show-state="step3">
    <!-- Step 3 content -->
  </div>
</div>
```

### 7. Dual-Section Page

Use when: One page shows two independent data sets (e.g., "Mis Citas" + "Citas de Mi Equipo").

Structure:
- `.anta-layout` with sidebar + content
- `.anta-page-header` with title
- Section 1: `.anta-card` with own `.anta-card-header` + `.anta-card-body` containing filters + table
- Section 2: `.anta-card` (separate, with `mt-xl`) with own header + filters + table
- Each section has independent filters, pagination, and action modals

```html
<!-- Section 1 -->
<div class="anta-card">
  <div class="anta-card-header">
    <span class="anta-card-title">Mis Registros</span>
  </div>
  <div class="anta-card-body">
    <!-- filters + table + pagination -->
  </div>
</div>

<!-- Section 2 -->
<div class="anta-card mt-xl">
  <div class="anta-card-header">
    <span class="anta-card-title">Registros de Mi Equipo</span>
  </div>
  <div class="anta-card-body">
    <!-- independent filters + table + pagination -->
  </div>
</div>
```

### 8. Report Page (Tabbed Reports)

Use when: Multiple related reports share a tab navigation (e.g., Dashboard, Bookings, Schedule, History tabs).

Structure:
- `.anta-layout` with sidebar + content
- `.anta-page-header` with title
- Tab navigation: `.anta-tabs > .anta-tabs-nav` with one `.anta-tab` per report
- Each tab panel contains an independent report: filters + table + export button
- Use `data-tab-group` / `data-tab` / `data-tab-panel` for switching

```html
<div data-tab-group>
  <div class="anta-tabs">
    <div class="anta-tabs-nav">
      <a class="anta-tab anta-tab--active" data-tab="indicators">Indicadores</a>
      <a class="anta-tab" data-tab="bookings">Citas por Empleado</a>
      <a class="anta-tab" data-tab="schedule">Programacion Semanal</a>
      <a class="anta-tab" data-tab="history">Historial de Asistencia</a>
    </div>
  </div>

  <div data-tab-panel="indicators" class="anta-visible">
    <!-- Dashboard KPIs + charts -->
  </div>
  <div data-tab-panel="bookings">
    <!-- Filters + table + export -->
  </div>
  <div data-tab-panel="schedule">
    <!-- Filters + table + export -->
  </div>
  <div data-tab-panel="history">
    <!-- Filters + table + export -->
  </div>
</div>
```

### 9. Custom Page

Use when: The screen doesn't fit any of the above types (settings, notifications, kanban, etc.).

Structure:
- `.anta-layout` with sidebar + content (always — keeps ANTA shell consistent)
- `.anta-breadcrumb` + `.anta-page-header` (always)
- Compose freely using components from the Anta* Component Catalog above
- **CONSTRAINT**: Every CSS class MUST exist in `anta-prototype.css`. If a layout need isn't covered, combine utility classes (`.d-flex`, `.gap-*`, `.mt-*`, `.mb-*`, `.p-*`). Do NOT invent class names.

---

## Workflow

### Step 0: Check for Visual References (BEFORE generating)

**Ask the user**: "Do you have wireframes, sketches, or screenshots to use as reference? (photo, image file, Figma export, hand-drawn sketch on paper/whiteboard)"

- **If user provides image(s)**:
  1. Analyze each image to identify: layout structure, components, field labels, navigation, action buttons, status indicators
  2. Map what you see to ANTA components (table → `.anta-table`, form fields → `.anta-form-item`, badges → `.anta-badge`, etc.)
  3. Use the image as the PRIMARY source for layout and field placement — Requirements doc fills in data types and business rules
  4. If the image is ambiguous (hard to read, incomplete), ask the user to clarify specific parts before generating

- **If user has no images** (or declines):
  1. Infer screen layouts from the Requirements Document (fields → form, entities → list, detail views → detail page)
  2. Use the templates as starting points and adapt from requirements context

**Vision requirement**: Interpreting images requires a model with vision capability (Claude, GPT-4o, Gemini). If the model does not support vision, inform the user and proceed with the text-based inference path.

### Step 1: Read Inputs

1. **Read the Requirements Document** (`aidlc-docs/inception/requirements/requirements.md`)
2. **Read visual references** (if provided in Step 0) — photos, wireframes, sketches
3. **Identify screens** — list all pages the feature requires (list, create, edit, detail, etc.)

### Step 2: Plan Prototypes

1. Map each screen to a page type (List / Form / Detail)
2. If visual reference exists, note which elements from the image map to which ANTA classes
3. Present the screen plan to the user for confirmation before generating

### Step 2b: Map Screen Transitions

Before generating HTML, document the navigation flow:

```html
<!--
  FLOW: [Module Name]
  SCREENS:
  1. {entity}-list    → entry point
  2. {entity}-create  → form (from list btn Nueva)
  3. {entity}-detail  → view (from list btn Ver)
  4. {entity}-edit    → form (from list/detail btn Editar)

  TRANSITIONS:
  list → create  : "Nueva" button
  list → detail  : "Ver" button per row
  list → edit    : "Editar" button per row
  create → list  : Guardar / Cancelar
  detail → edit  : "Editar" button (conditional on state)
  edit → detail  : Guardar / Cancelar
-->
```

Include this block as an HTML comment at the top of `index.html`. Every clickable element must have a known destination.

### Step 3: Generate HTML Files

One per screen, starting from the template that matches the type:
- List page: base on `config/skills/html-prototype/assets/template-list.html`
- Form page: base on `config/skills/html-prototype/assets/template-form.html`
- Detail page: base on `config/skills/html-prototype/assets/template-detail.html`
- Calendar/Schedule page: base on `config/skills/html-prototype/assets/template-calendar.html`
- Wizard (multi-step modal): base on `config/skills/html-prototype/assets/template-wizard.html`
- Dual-Section page: base on `config/skills/html-prototype/assets/template-dual-section.html`
- Report/Tabbed page: base on `config/skills/html-prototype/assets/template-report.html`
- Dashboard page: base on `template-report.html` (use the KPI stats grid from tab 1)
- Custom page: no template — compose from components in the Anta* Component Catalog

### Step 4: Adapt Content

- Replace generic data with domain-specific fields, labels, and mock data from requirements
- If visual reference was provided, match the layout/order from the image as closely as possible

### Step 5: Save and Update

1. Save to output location — `aidlc-docs/inception/prototypes/{screen-name}.html`
2. Update Requirements Doc — add a Prototypes section listing generated files

---

## Sidebar Navigation

The sidebar must reflect the real ANTA application menu. Standard structure:

```html
<nav class="anta-sidebar">
  <div class="anta-sidebar-logo">
    <span class="anta-sidebar-logo-text">ANTA</span>
  </div>
  <ul class="anta-nav">
    <li class="anta-nav-item anta-nav-item--active">
      <a href="#" class="anta-nav-link" data-testid="nav-{module}">
        <span class="anta-nav-icon">{icon-char}</span>
        <span>{Module Name}</span>
      </a>
    </li>
    <!-- more items -->
  </ul>
</nav>
```

Active item: add `.anta-nav-item--active` to the current section.

---

## Status Badge Reference

Use `.anta-badge` + the appropriate modifier:

| Status key | Class | Spanish label |
|------------|-------|---------------|
| BORRADOR | `.anta-badge--draft` | Borrador |
| EN_REVISION | `.anta-badge--pending` | En Revision |
| EN_PROCESO | `.anta-badge--in-progress` | En Proceso |
| APROBADO | `.anta-badge--approved` | Aprobado |
| RECHAZADO | `.anta-badge--rejected` | Rechazado |

---

## Accessibility Requirements

- All form inputs must have a matching `<label>` with `for` attribute
- All images (if any) must have `alt` text
- Table headers must use `<th scope="col">`
- Buttons must have descriptive text (no icon-only buttons in prototypes)
- Use semantic HTML: `<nav>`, `<main>`, `<header>`, `<section>`, `<form>`

---

## data-testid Convention

| Element | Pattern | Example |
|---------|---------|---------|
| Navigation link | `nav-{module}` | `nav-empleados` |
| Primary action button | `btn-{action}` | `btn-nuevo-empleado` |
| Search input | `input-search` | `input-search` |
| Filter select | `select-{field}` | `select-estado` |
| Table row | `row-{id}` | `row-1234` |
| Form field | `field-{name}` | `field-nombre` |
| Submit button | `btn-submit` | `btn-submit` |
| Cancel button | `btn-cancel` | `btn-cancel` |
| Status badge | `badge-status` | `badge-status` |

---

## Ant Design Version

ANTA uses **Ant Design 6.0.1** with custom Anta* wrapper components. Key differences from antd 5.x:

- Default Input and Button size is `large` in all Anta* wrappers — match this sizing in prototypes
  by giving form inputs a height of ~40px (the `anta-input` class already does this)
- `bordered` prop replaced by `variant="outlined"` in many components
- CSS Variables enabled by default in antd 6

## Anta* Component Catalog (26 components)

These are the production wrapper components an agent MUST use when generating React code.
In HTML prototypes, imitate their visual output using `anta-prototype.css` classes.

| Anta* Component | CSS Equivalent |
|-----------------|----------------|
| AntaButton | `.btn .btn-primary / .btn-default / .btn-danger` |
| AntaInput | `.anta-input` (height ~40px, large) |
| AntaTextArea | `.anta-textarea` |
| AntaPassword | `.anta-input` (type="password") |
| AntaSearch | `.anta-search-wrapper > .anta-input` |
| AntaInputNumber | `.anta-input` (type="number") |
| AntaSelect | `.anta-select` |
| AntaDatePicker | `.anta-input` (type="date") |
| AntaForm | `.anta-form` |
| AntaFormItem | `.anta-form-item` (+ `.anta-form-label`, `.anta-form-required`, `.anta-form-hint`, `.anta-form-error`, `.anta-form-item--error`) |
| AntaModal | `.anta-modal-overlay > .anta-modal > .anta-modal-header + .anta-modal-title + .anta-modal-close / .anta-modal-body / .anta-modal-footer` |
| AntaTable | `.anta-table-wrapper > .anta-table` |
| AntaTypography | `h1-h3`, `.text-*` utilities |
| AntaTag / AntaBadge | `.anta-badge` + `--draft` / `--pending` / `--in-progress` / `--approved` / `--rejected` / `--gray` |
| AntaCard | `.anta-card` > `.anta-card-header` + `.anta-card-title` / `.anta-card-body` / `.anta-card-body--compact` |
| AntaTabs | `.anta-tabs` > `.anta-tabs-nav` > `.anta-tab` / `.anta-tab--active` |
| AntaSpace | `.d-flex .gap-*` |
| AntaSpin | (show `.anta-empty-state` as loading placeholder) |
| AntaAlert | `.anta-alert .anta-alert--*` |
| AntaSwitch | `<input type="checkbox">` |
| AntaRadio | `<input type="radio">` |
| AntaRow / AntaGrid / AntaCol | `.anta-form-row` |
| AntaAutoComplete | `.anta-input` |
| AntaAvatar | `.anta-avatar` |
| AntaDivider | `.anta-divider` |
| AntaDescriptions | `.anta-descriptions` |
| AntaDrawer | (use `.anta-modal` as side-panel substitute) |
| AntaEmptyInfo | `.anta-empty-state` |
| AntaUpload | `<input type="file">` |
| AntaCheckbox (+Group) | `<input type="checkbox">` (group: multiple checkboxes in a `.d-flex` container) |
| AntaPopconfirm | (use `.anta-modal` as substitute for confirmation popover) |
| AntaTimePicker | `<input type="time">` (default size: large, matches `.anta-input` height) |

---

## CSS Variable Quick Reference

**Note on spacing tokens**: Prototype CSS uses slightly more generous spacing than production (`--space-xl: 24px` vs production `20px`, `--space-2xl: 32px` vs `24px`). This is intentional — prototypes prioritize visual clarity for stakeholder review, not pixel-perfect matching. The final React app uses Ant Design 6 spacing which differs anyway.

Common token mistakes — use the LEFT column, never the RIGHT:

| Correct | WRONG (do not use) |
|---------|---------------------|
| `var(--error)` | `var(--danger)`, `var(--color-error)` |
| `var(--warning)` | `var(--color-warning)` |
| `var(--success)` | `var(--color-success)` |
| `var(--bg-page)` | `var(--color-bg-page)` |
| `var(--text-primary)` | `var(--color-text)` |
| `var(--primary)` | `var(--color-primary)` |
| `var(--text-muted)` | `var(--muted)` |

## Assets

| File | Purpose |
|------|---------|
| [`assets/anta-prototype.css`](assets/anta-prototype.css) | Master CSS — all ANTA tokens + components (v1.2) |
| [`assets/prototype-interactions.js`](assets/prototype-interactions.js) | Pre-built interactivity — agent NEVER modifies (v2.1) |
| [`assets/template-list.html`](assets/template-list.html) | Starting point for list/table pages |
| [`assets/template-form.html`](assets/template-form.html) | Starting point for create/edit forms |
| [`assets/template-detail.html`](assets/template-detail.html) | Starting point for detail/view pages |
| [`assets/template-calendar.html`](assets/template-calendar.html) | Starting point for calendar/schedule pages |
| [`assets/template-wizard.html`](assets/template-wizard.html) | Starting point for wizard (multi-step modal) |
| [`assets/template-dual-section.html`](assets/template-dual-section.html) | Starting point for dual-section pages |
| [`assets/template-report.html`](assets/template-report.html) | Starting point for tabbed report pages |

## Inspector Mode

All prototypes include a built-in inspector for stakeholder review.

**How to use**: Press the `?` key on any prototype page.

- All clickable elements (`data-navigate`, `data-toggle`, `data-tab`, `a[href]`) get a **pink dashed outline**
- Labels show the destination or action for each element
- Press `?` again to deactivate

**Tell stakeholders**: "Presione la tecla ? para ver que elementos son interactivos."

The inspector does not activate when focus is on an input, textarea, or select (to avoid interfering with form usage).
