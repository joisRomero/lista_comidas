---
name: design-system
description: >
  ANTA visual design system: colors, typography, spacing, components.
  Trigger: When styling components, choosing colors, or applying visual patterns.
metadata:
  author: anta
  version: "2.1"
  scope: [root]
  enforcement: mandatory
  auto_invoke: "color, estilo, CSS, diseño, Ant Design, tipografia, theme, tokens"
  phase: [inception, construction]
  layer: [frontend]
  validates_with: validate_react_shared
  validation_profile: build-component
---

## Critical Rules

| Rule | Type | Rationale |
|------|------|-----------|
| Use CSS Modules | ALWAYS | Scoped styles |
| Use design tokens (not raw values) | ALWAYS | Consistency |
| Use Ant Design Icons | ALWAYS | Visual consistency |
| Use hardcoded colors outside tokens | NEVER | Maintainability |
| ALWAYS use Anta* wrappers, never import antd directly | ALWAYS | Consistent styling |
| ALWAYS wrap new antd components following the Anta* pattern | ALWAYS | Design consistency |
| New microfrontend: COPY `shared/` from existing child | ALWAYS | Anta* wrappers are NOT generated — they are COPIED from a reference child app |

---

## Colors

### Primary
| Name | Hex | Use |
|------|-----|-----|
| Primary | `#007788` | Brand color, highlighted icons |
| Primary Hover | `#5b8def` | Interactive hover |
| Link/Action | `#1890ff` | Links, badges, actions |

### Semantic
| State | Background | Text/Border |
|-------|------------|-------------|
| Success | `#f6ffed` | `#52c41a` / `#389e0d` |
| Warning | `#fff7e6` | `#fa8c16` / `#d46b08` |
| Error | `#fff2f0` | `#ff4d4f` / `#ff7875` |
| Info | `#e6f7ff` | `#1890ff` |

### Text (Grays)
| Name | Hex | Use |
|------|-----|-----|
| Title | `#262626` | Titles, primary text |
| Primary | `#4a5568` | Content text |
| Secondary | `#595959` | Descriptions |
| Muted | `#8c8c8c` | Labels, placeholders |
| Disabled | `#bfbfbf` | Disabled text |

### UI (Grays)
| Name | Hex | Use |
|------|-----|-----|
| Background Page | `#f5f5f5` | Page background |
| Background Card | `#ffffff` | Card background |
| Border Default | `#d9d9d9` | Input borders |
| Border Light | `#e8e8e8` | Subtle borders |

### Status Badges
| Status | Background | Text |
|--------|------------|------|
| Draft | `#e5e7eb` | `#374151` |
| Pending | `#fef3c7` | `#92400e` |
| In Progress | `#dbeafe` | `#1e40af` |
| Approved | `#d1fae5` | `#065f46` |
| Rejected | `#fee2e2` | `#991b1b` |

---

## Typography

| Name | Size | Weight | Use |
|------|------|--------|-----|
| H1 | `24px` | `600` | Page title |
| H2 | `20px` | `600` | Section title |
| H3 | `16px` | `600` | Card title |
| Body | `14px` | `400` | Main text |
| Small | `13px` | `400` | Secondary text |
| Caption | `12px` | `400` | Labels, metadata |

---

## Spacing (base 4px)

| Token | Value | Use |
|-------|-------|-----|
| xs | `4px` | Minimum spacing |
| sm | `8px` | Small element gap |
| md | `12px` | Standard card gap |
| lg | `16px` | Section gap |
| xl | `24px` | Card/modal padding |

---

## Borders & Shadows

### Border Radius
| Token | Value | Use |
|-------|-------|-----|
| sm | `4px` | Badges, tags |
| md | `8px` | Cards, inputs |
| full | `50%` | Avatars |

### Shadows
```css
box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);   /* Card */
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);   /* Hover */
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);  /* Elevated */
```

---

## Sidebar & Layout Tokens

| Token | Value | Use |
|-------|-------|-----|
| Sidebar gradient start | `#007788` | Top of sidebar gradient |
| Sidebar gradient end | `#004650` | Bottom of sidebar gradient |
| Sidebar gradient | `linear-gradient(135deg, #078, #004650)` | Full gradient |
| Menu hover bg | `#96d3d133` | Semi-transparent teal on hover |
| Menu selected bg | `#96d3d180` | More opaque teal for selected item |
| Menu selected text | `#ffe34c` | Yellow text for active menu item |
| Menu selected border | `3px solid rgba(255,255,255,0.5)` | Left border on active item |
| Header height | `56px` (prototype) / `70px` (production) | Top bar height |
| Sidebar width | `220px` (prototype) / `300px` (production, collapsible to 80px) | Sidebar width |
| Footer bg | `#f9fafb` | Footer background |
| Border layout | `#dfe7ef` | Sidebar/content border |

## Ant Design 6 Theme (ConfigProvider)

The production app configures the theme at the AppLayout level:

```tsx
<ConfigProvider theme={{ token: { colorPrimary: '#007788' } }}>
  {children}
</ConfigProvider>
```

This single token propagates through all Ant Design components (buttons, links, focus rings, etc.). No other theme tokens are overridden — everything else uses Ant Design 6 defaults.

## Icons (@ant-design/icons)

| Context | Size | Color |
|---------|------|-------|
| In button | `inherit` | inherit |
| Page title | `20px` | `#007788` |
| Icon container | `24px` | `#007788` |
| Empty state | `80px` | `#d9d9d9` |
| Delete hover | - | `#ff4d4f` |

---

## Quick Reference

```css
/* Most used */
--text-title: #262626;
--text-muted: #8c8c8c;
--bg-card: #ffffff;
--border-light: #e8e8e8;
--primary: #007788;
--error: #ff4d4f;  /* NOT --danger */

/* Quick spacing */
gap: 8px;       /* Small items */
gap: 16px;      /* Cards */
padding: 24px;  /* Cards, modals */

/* Quick card */
background: white;
border: 1px solid #e8e8e8;
border-radius: 8px;
padding: 24px;
```

---

## Anta* Component Catalog

| Anta* Wrapper | Wraps (antd) | forwardRef | Default Size | CSS Module | Special |
|---------------|-------------|------------|--------------|------------|---------|
| AntaButton | Button | Yes | large | Yes | - |
| AntaInput | Input | Yes | large | Yes | autoComplete="off" |
| AntaTextArea | Input.TextArea | Yes | large | Yes | Via AntaInput file |
| AntaPassword | Input.Password | Yes | - | Yes | Via AntaInput file |
| AntaSearch | Input.Search | Yes | - | Yes | Via AntaInput file |
| AntaSelect | Select | Yes | large | Yes | Exposes .Option |
| AntaForm | Form | No | - | Yes | Exports useAntaForm, useAntaFormWatch |
| AntaFormItem | Form.Item | No | - | Yes | - |
| AntaInputNumber | InputNumber | Yes | large | Yes | Needs `ref as unknown as Ref<never>` cast (antd v6) |
| AntaDatePicker | DatePicker | No | - | Yes | - |
| AntaUpload | Upload | No | - | Yes | - |
| AntaModal | Modal | No | - | Yes | - |
| AntaAutoComplete | AutoComplete | Yes | - | Yes | - |
| AntaTag | Tag | No | - | Yes | - |
| AntaAlert | Alert | No | - | Yes | - |
| AntaTabs | Tabs | No | - | Yes | - |
| AntaCard | Card | No | - | Yes | - |
| AntaSwitch | Switch | Yes | - | Yes | - |
| AntaRadio | Radio | No | - | Yes | - |
| AntaTable | Table | No | - | Yes | Generic `<T extends object>` |
| AntaSpace | Space | No | - | Yes | - |
| AntaTypography | Typography | Mixed | - | Yes | Namespace: { Title, Text, Paragraph, Link } |
| AntaDrawer | Drawer | Yes | - | Yes | - |
| AntaSpin | Spin | No | - | Yes | - |
| AntaDescriptions | Descriptions | No | - | Yes | - |
| AntaRow / AntaCol | Row / Col | No | - | Yes | In AntaGrid.tsx |
| AntaDivider | Divider | No | - | Yes | - |
| AntaAvatar | Avatar | No | - | Yes | - |
| AntaEmptyInfo | Custom empty | No | - | Yes | Custom component |
| AntaCheckbox | Checkbox | No | - | Yes | Exposes .Group compound |
| AntaPopconfirm | Popconfirm | No | - | Yes | - |
| AntaTimePicker | TimePicker | No | large | Yes | - |

**Anta* Wrapper Creation Pattern**:
```typescript
// Standard pattern for new wrappers
import { forwardRef } from 'react';
import { ComponentName } from 'antd';
import type { ComponentNameProps } from 'antd';
import styles from './AntaComponentName.module.css';

export interface AntaComponentNameProps extends ComponentNameProps {}

export const AntaComponentName = forwardRef<HTMLElement, AntaComponentNameProps>(
  ({ className, size = 'large', ...props }, ref) => (
    <ComponentName
      ref={ref}
      size={size}
      className={`${styles.componentName} ${className ?? ''}`}
      {...props}
    />
  )
);
AntaComponentName.displayName = 'AntaComponentName';
```

**antd v6 Ref Type Incompatibilities** (CRITICAL):

Some antd v6 components have internal ref types that DON'T match standard HTML element types.
When `forwardRef<HTMLElement | HTMLInputElement, Props>` causes a type error on `ref={ref}`,
use the safe cast pattern: `ref={ref as unknown as Ref<never>}`.

```typescript
// AntaInputNumber — antd v6 uses InputNumberRef internally, NOT HTMLInputElement
import { InputNumber } from 'antd';
import type { InputNumberProps } from 'antd';
import { forwardRef, type Ref } from 'react';
import styles from './AntaInputNumber.module.css';

export interface AntaInputNumberProps extends InputNumberProps {}

export const AntaInputNumber = forwardRef<HTMLInputElement, AntaInputNumberProps>(
  ({ className, size = 'large', ...props }, ref) => {
    return (
      <InputNumber
        ref={ref as unknown as Ref<never>}
        size={size}
        className={`${styles.inputNumber} ${className ?? ''}`}
        {...props}
      />
    );
  }
);
AntaInputNumber.displayName = 'AntaInputNumber';
```

| Component | Ref Issue | Fix |
|-----------|-----------|-----|
| `InputNumber` | Internal `InputNumberRef` ≠ `HTMLInputElement` | `ref as unknown as Ref<never>` |
| `DatePicker` | Internal `PickerRef` ≠ `HTMLElement` | `ref as unknown as Ref<never>` |
| `AutoComplete` | Internal ref ≠ `HTMLElement` | `ref as unknown as Ref<never>` |

> **Rule**: If `ref={ref}` causes a TS error on an antd component, import `type Ref` from `react` and cast `ref as unknown as Ref<never>`. NEVER use `@ts-ignore`.

**AntaTypography special pattern** (namespace with sub-components):
```typescript
import { forwardRef } from 'react';
import { Typography } from 'antd';
import styles from './AntaTypography.module.css';

const AntaTitle = forwardRef<HTMLElement, TypographyTitleProps>(...);
const AntaText = forwardRef<HTMLElement, TypographyTextProps>(...);
const AntaParagraph = forwardRef<HTMLElement, TypographyParagraphProps>(...);

export const AntaTypography = { Title: AntaTitle, Text: AntaText, Paragraph: AntaParagraph };
```

## Antd 6 Notes
- antd 6 uses CSS Variables by default
- `bordered` prop replaced by `variant="outlined" | "filled" | "borderless"` in many components
- `message` prop renamed to `title` in Alert/Notification
- `Space` `direction` renamed to `orientation`
- `@ant-design/icons` must be v6+ (project uses 6.1.0)
- Tag trailing margin removed by default
- Modal/Drawer mask blur effect enabled by default

## Child Base Copy Checklist (New Microfrontends)

New child microfrontends MUST copy these files from an existing child (e.g., Front-Mantenimiento). They are NOT generated — they must be copied and adapted.

### 1. Anta* Wrappers — `src/shared/components/`

Copy the entire `shared/components/` directory. Each wrapper has: `.tsx` + `.module.css` + `index.ts`.

| Component | Must Copy |
|-----------|-----------|
| AntaButton/ | ✅ |
| AntaForm/ | ✅ |
| AntaInput/ | ✅ (includes AntaTextArea, AntaPassword, AntaSearch) |
| AntaInputNumber/ | ✅ |
| AntaModal/ | ✅ |
| AntaSelect/ | ✅ |
| AntaSpace/ | ✅ |
| AntaSpin/ | ✅ |
| AntaTable/ | ✅ |
| AntaTag/ | ✅ |
| AntaTypography/ | ✅ |
| index.ts (barrel) | ✅ |

> **Note**: The base child may have additional wrappers (AntaDrawer, AntaAlert, etc.). Copy ALL that exist in `shared/components/`.

### 2. Auth Adapter — `src/shared/adapters/useHostAuth.ts`

Hook that consumes host authentication. Exposes `getProcessById` and other host-provided functions.

### 3. Shared Utils — `src/shared/utils/`

| File | Purpose |
|------|---------|
| `constants.ts` | React Query config, debug intervals, service path IDs, domain constants |
| `generateVersionFile.ts` | Rsbuild plugin that writes `dist/version.json` on build |
| `service-ids.ts` | Service identifiers for microfrontend communication |
| `types.ts` | API response wrapper (`ResponseApi<T>`), pagination interfaces, error types |

#### `constants.ts` — Base Structure

```typescript
// React Query global config (MANDATORY — same across all children)
export const QUERY_CONFIG = {
  STALE_TIME: 1000 * 60 * 5,       // 5 minutes
  GC_TIME: 1000 * 60 * 10,         // 10 minutes
  RETRY_DELAY: 1000,               // 1 second
  MAX_RETRIES: 2,
};

// Debug protection (prevents double-mount issues in StrictMode)
export const DEBUG_PROTECTION_INTERVAL = 4000;

// Service path IDs (PROJECT-SPECIFIC — map Lion process IDs to readable names)
export const PATHS = {
  FIND_ALL: 4001,
  CREATE: 1004,
  UPDATE: 2004,
  DELETE: 3004,
  FILTER_BY: 4007,
  EXPORT: 5001,
};

// Domain constants (PROJECT-SPECIFIC — add as needed)
export const PAGE_SIZE = 10;
export const DATE_FORMAT = "DD/MM/YYYY";
export const TIME_FORMAT = "HH:mm";
```

> **Copy rule**: Keep `QUERY_CONFIG` and `DEBUG_PROTECTION_INTERVAL` unchanged. Replace `PATHS` and domain constants per project.

#### `types.ts` — Base Structure

```typescript
// API response envelope (MANDATORY — matches backend ApiResponse<T>)
export interface ResponseApi<T> {
  success: boolean;
  data: T;
  message: string;
  errors: ApiError[] | null;
  pagination: PaginationResult | null;
  metadata: Record<string, unknown> | null;
}

export interface ApiError {
  code: string;
  message: string;
  field?: string;
}

// Pagination (MANDATORY — matches backend pagination shape)
export interface PaginationResult {
  page: number;
  pageSize: number;
  totalRecords: number;
  totalPages: number;
  hasNext: boolean;
  hasPrevious: boolean;
}

export interface PaginationParams {
  page: number;
  pageSize: number;
}
```

> **Copy rule**: Keep all interfaces unchanged — they mirror the backend `ApiResponse<T>` contract exactly.

### 4. Version Metadata — `public/version.json`

```json
{
  "name": "{service-name}",
  "version": "1.0.0",
  "buildDate": "2026-01-01T00:00:00.000Z"
}
```

Update `name` and `version` for the new microfrontend.

### Copy Checklist

```
[ ] Copy src/shared/components/ (all Anta* wrappers + index.ts)
[ ] Copy src/shared/adapters/useHostAuth.ts
[ ] Copy src/shared/utils/ (4 files)
[ ] Copy public/version.json → update name and version
[ ] Verify barrel exports in shared/components/index.ts
[ ] Verify useHostAuth imports match host contract
```

---

## Custom Shared Components

Projects typically create reusable components in `shared/components/` beyond the Anta* wrappers. Follow these naming patterns:

| Type | Naming Pattern | Purpose | Example |
|------|---------------|---------|---------|
| Entity Card | `{Entity}Card` | Display entity summary (default + compact variants) | MemberCard, CaseCard |
| Info Card | `{Entity}InfoCard` | Read-only entity detail display | OrderInfoCard |
| Config Form | `{Entity}ConfigForm` | Reusable form for entity configuration | SessionConfigForm |
| Confirmation Modal | `{Action}ConfirmationModal` | Confirmation dialogs for destructive actions | RemoveConfirmationModal |
| Empty State | `AntaEmptyInfo` | Custom empty state with icon and message | AntaEmptyInfo |

> All custom shared components follow the same folder structure: `shared/components/{ComponentName}/{ComponentName}.tsx` + `.module.css` + `index.ts`

## New Microfrontend — MANDATORY Copy from Base Child

When creating a new child microfrontend, **COPY these folders/files as-is** from an existing child app in the workspace (e.g., Front-Mantenimiento). Do NOT regenerate them:

```
shared/
├── components/              # ALL Anta* wrappers (copy entire folder)
│   ├── index.ts             # Barrel export
│   ├── AntaButton/
│   ├── AntaForm/
│   ├── AntaInput/
│   ├── AntaInputNumber/
│   ├── AntaModal/
│   ├── AntaSelect/
│   ├── AntaSpace/
│   ├── AntaSpin/
│   ├── AntaTable/
│   ├── AntaTag/
│   └── AntaTypography/
├── adapters/
│   ├── index.ts
│   ├── useHostApi.ts
│   └── useHostAuth.ts
└── utils/
    ├── constants.ts
    ├── types.ts
    ├── service-ids.ts        # UPDATE with new module's service IDs
    └── generateVersionFile.ts

public/
└── version.json              # UPDATE name and version for new module
```

**Rules:**
- `shared/components/` → copy ALL, do not cherry-pick
- `shared/adapters/` → copy ALL
- `shared/utils/` → copy ALL, then UPDATE `service-ids.ts` with new IDs and `version.json` with new module name
- `App.css` → copy from base child

## Avatar Gradient
```typescript
import { generateAvatarGradient } from '@/shared/utils/avatarColors';
// Returns: "linear-gradient(135deg, hsl(...), hsl(...))"
// Uses hash function + colorCache Map for memoization
```

---

## Detailed Documentation

| Topic | Asset |
|-------|-------|
| Component styles (Card, List, Empty, etc.) | [components.css](assets/components.css) |
| Avatar gradient generator | [avatar-gradient.ts](assets/avatar-gradient.ts) |

## Consumers (skills that reference this design system)

| Skill | How it consumes |
|-------|----------------|
| `html-prototype` | Translates tokens to `anta-prototype.css` for static HTML prototypes. Note: prototype spacing is slightly more generous (xl=24px vs production 20px) — intentional for stakeholder review clarity. |
| `agent-frontend` | Uses Anta* wrappers + ConfigProvider theme in React code generation |
| `api-first-frontend` | References component names for TypeScript service/hook generation |

**Single source of truth**: If a token value changes, update this skill FIRST, then propagate to consumers. Do NOT change `anta-prototype.css` tokens without updating here.

## Resources

- [Ant Design](https://ant.design/)
- [Ant Design Icons](https://ant.design/components/icon)
