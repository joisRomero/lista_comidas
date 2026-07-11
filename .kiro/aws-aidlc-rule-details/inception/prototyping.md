# Prototyping - Detailed Steps

## Purpose
**Generate static HTML mockups for stakeholder visual approval before API design**

Prototyping creates browser-viewable HTML files that look like the final ANTA application using the organization's design system. Stakeholders open the files locally, review layout/labels/flow, and approve before the team invests in API Contract Design.

**Note**: Prototypes use HTML + CSS + a pre-built interaction script (`prototype-interactions.js`). The agent writes `data-*` attributes for interactivity (modals, tabs, state switching) but NEVER writes custom JavaScript. They validate VISUAL design and NAVIGATION flow, not business logic.

## Prerequisites
- Requirements Analysis must be complete (screens identified)
- User Stories recommended (provides page context and acceptance criteria)

## When to Execute

**Execute IF**:
- Project has frontend screens (list, form, detail pages)
- Stakeholder needs visual approval before API design
- UX/UI validation is needed before construction
- Multiple screen types exist (reduces rework risk)

**Skip IF**:
- Backend-only project (no UI)
- Stakeholder prefers to review during Construction
- Simple changes to existing screens (not worth prototyping)
- Time pressure overrides visual approval need

**ASK BEFORE SKIPPING (MANDATORY)**:
If the project has User Stories with frontend screens (at least 1 screen identified) AND the user has NOT explicitly said "skip prototyping" or "no prototypes needed":
- **DO NOT skip silently.** Ask the user:
  > "El proyecto tiene pantallas frontend. Quieres que genere prototipos HTML para aprobacion visual antes de continuar con API Contract Design? (Los prototipos permiten validar layout y flujo antes de invertir en codigo.)"
- Only skip if the user explicitly declines
- Log the user's decision in `audit.md`

---

## Step-by-Step Execution

### Step 1: Load Prototype Skill

- [ ] Load `html-prototype` skill from `skills/html-prototype/SKILL.md`
- [ ] Read the ANTA design system tokens and component patterns
- [ ] Read template files from `skills/html-prototype/assets/` as reference

### Step 1b: Ask for Visual References

- [ ] **Ask the user**: "Tienes wireframes, sketches, capturas de pantalla o fotos de bocetos para usar como referencia visual? (foto de pizarra, papel, Figma, etc.)"
- [ ] **If user provides images**: save originals to `aidlc-docs/assets/references/` for traceability, then analyze layout, components, fields, and use as PRIMARY source for prototype generation
- [ ] **If user has no images**: proceed with inference from Requirements document
- [ ] **If model lacks vision**: inform user and proceed with text-based inference

### Step 2: Identify Screens from Requirements

- [ ] Review Requirements Analysis artifacts (requirements.md)
- [ ] Review User Stories (if available) for page-level acceptance criteria
- [ ] List all screens needed:
  - **List pages**: tables with filters, pagination, search
  - **Form pages**: create/edit forms with validation states
  - **Detail pages**: read-only views with status-based actions
  - **Dashboard pages**: summary cards, charts placeholders
- [ ] Document the screen inventory with one line per screen:

```markdown
| Screen | Type | Key Elements |
|--------|------|-------------|
| {Entity} List | List | Table, filters (status, {catalog}), search, pagination, "New" button |
| {Entity} Create | Form | Personal data, {catalog} data, save/cancel |
| {Entity} Detail | Detail | Read-only fields, status badge, action buttons by state |
```

### Step 3: Create Output Directory

- [ ] Create `aidlc-docs/inception/prototypes/`
- [ ] Copy `anta-prototype.css` AND `prototype-interactions.js` from the skill assets into this directory
- [ ] All HTML files will be generated alongside the CSS and JS (portable bundle)

### Step 4: Generate HTML Mockups

For each screen identified in Step 2:

- [ ] Start from the closest template in `skills/html-prototype/assets/`:
  - `template-list.html` for list/table pages
  - `template-form.html` for create/edit forms
  - `template-detail.html` for detail/view pages
- [ ] Customize with real field names, labels, and mock data from Requirements
- [ ] Ensure link `<link rel="stylesheet" href="./anta-prototype.css">` in `<head>`
- [ ] Ensure `<script src="./prototype-interactions.js"></script>` before `</body>`
- [ ] Use `data-*` attributes for interactivity (see SKILL.md Interactivity API): `data-toggle`, `data-dismiss`, `data-tab`, `data-state-select`, `data-show-state`
- [ ] Include `data-testid` on all interactive elements
- [ ] Use Spanish for labels, English for code identifiers
- [ ] Mock data should be realistic (real-looking names, dates, statuses)
- [ ] Include a mix of statuses in list pages (DRAFT, SUBMITTED, APPROVED, REJECTED)
- [ ] Save as `aidlc-docs/inception/prototypes/{screen-name}.html`

### Step 4b: Validate HTML Classes (GATE)

**Deterministic validation**: Run the automated validator first, then review the manual checklist below.

- [ ] Run `python config/validators/validate_html_prototype.py aidlc-docs/inception/prototypes/`
- [ ] If ERRORS → fix the HTML → re-run → repeat until clean
- [ ] If only WARNINGS → review each, proceed if acceptable

Before proceeding, verify that EVERY CSS class used in the generated HTML files exists in `anta-prototype.css`:

- [ ] For each generated HTML file:
  - Extract all `class="..."` values
  - Verify each class exists in `anta-prototype.css`
  - If ANY class is NOT defined: replace with the correct ANTA class (check SKILL.md Component Catalog)
  - Common mistakes to catch:
    - `anta-tabs-tab` → correct: `anta-tab`
    - `anta-form-help` → correct: `anta-form-hint`
    - `text-h1/h2/h3` → verify they exist (design-system v2.1+)
    - `anta-badge--gray` → verify it exists (design-system v2.1+)
- [ ] Verify all CSS variables reference tokens defined in `:root`:
  - `var(--error)` not `var(--danger)`
  - `var(--bg-page)` not `var(--color-bg-page)`
  - `var(--warning)` not `var(--color-warning)`
  - `var(--success)` not `var(--color-success)`
- [ ] Verify all `.anta-card` elements wrap content in `.anta-card-body` (not directly inside card)
- [ ] Verify tab panels use `.anta-visible` class (NOT `hidden` attribute)
- [ ] **GATE**: Do NOT present completion message if undefined classes or variables remain

### Step 5: Generate Navigation Index

- [ ] Create `aidlc-docs/inception/prototypes/index.html` with links to all screens:

```html
<html>
<head>
  <link rel="stylesheet" href="./anta-prototype.css">
  <title>Prototipos - [Module Name]</title>
</head>
<body style="background: var(--color-bg-page); padding: 40px;">
  <div class="anta-page">
    <h1>Prototipos - [Module Name]</h1>
    <p>Abra cada enlace para revisar el diseno de pantalla.</p>
    <ul>
     <li><a href="./{entity}-list.html">Listado de {entities}</a></li>
     <li><a href="./{entity}-create.html">Crear {Entity}</a></li>
     <li><a href="./{entity}-detail.html">Detalle de {Entity}</a></li>
    </ul>
  </div>
</body>
</html>
```

### Step 6: Update State and Audit

- [ ] Log stage completion in `audit.md`
- [ ] Update `aidlc-state.md` with prototyping status
- [ ] **SELF-CHECK GATE**: Verify audit.md AND aidlc-state.md are updated before presenting completion

### Step 7: Present Completion Message

```markdown
# Prototyping Complete

Prototipos HTML generados para revision visual:

- [List generated files with descriptions]

> **REVIEW REQUIRED:**
> Abra los archivos HTML en su navegador desde: `aidlc-docs/inception/prototypes/`
> Empiece por `index.html` para ver todos los prototipos.

> **WHAT'S NEXT?**
>
> **You may:**
>
> - **Request Changes** - Pida modificaciones al layout, campos, o flujo
> - **Approve & Continue** - Aprobar prototipos y continuar a **ISO 27001 Assessment**

---
```

### Step 8: Wait for Explicit Approval
- [ ] Do not proceed until user explicitly approves prototypes
- [ ] If changes requested, update HTML files and repeat approval
- [ ] Document approval in audit.md

---

## Critical Rules

### Output Rules
- **All files in `aidlc-docs/inception/prototypes/`** — never in skill assets or workspace root
- **CSS copied, not linked** — `anta-prototype.css` must be in the same directory as HTML files
- **Self-contained bundle** — stakeholder can open files without framework access

### Design Rules
- **Zero CUSTOM JavaScript** — agent writes `data-*` attributes only, never `<script>` blocks or inline JS. All interactivity comes from the pre-built `prototype-interactions.js`
- **Zero external dependencies** — no CDN links, no Google Fonts, no Font Awesome
- **ANTA design system only** — use `anta-prototype.css` tokens and classes
- **Input/Button size "large"** — matches ANTA production defaults
- **Realistic mock data** — use believable names, dates, and values
- **Include all statuses** — list pages should show mixed status badges

### Prototype Limitations (document for stakeholders)
- Native browser controls (select, date picker) will look different per OS
- Navigation works between screens, modals open/close, tabs switch, workflow states toggle
- Forms don't validate or submit to a server — visual only
- Layout is approximate — final React app will use Ant Design 6 components
- These are for VISUAL and FLOW approval, not business logic testing
