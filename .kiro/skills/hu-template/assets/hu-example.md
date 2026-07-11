# Example: HU de Creación de Caso (Frontend Domain)

```markdown
## 200-14889-001: Formulario creación de caso de contrato

**Epic:** Gestión de Casos
**Layer:** FRONT DOMAIN
**Repo:** 200-14889

### Historia

**Como** solicitante del área usuaria
**Quiero** crear un nuevo caso de contrato
**Para** iniciar el proceso de aprobación ante el comité

### Descripción

El solicitante necesita registrar un nuevo caso que será evaluado por el comité de contratos. Debe ingresar información general, documentos de soporte, proveedores involucrados y miembros del equipo.

### Criterios de Aceptación

- [ ] CA1: El formulario muestra todos los campos requeridos según el tipo de caso
- [ ] CA2: Se pueden adjuntar múltiples documentos (PDF, DOC, XLS)
- [ ] CA3: Se pueden agregar múltiples proveedores con RUC
- [ ] CA4: Se valida que al menos un miembro del equipo sea gerente
- [ ] CA5: El caso se crea en estado BORRADOR
- [ ] CA6: No se genera código hasta que se envíe a revisión

### Reglas de Negocio

| Regla | Descripción |
|-------|-------------|
| RN-001 | El nombre del caso es obligatorio |
| RN-002 | El tipo de caso determina los campos requeridos |
| RN-003 | El monto estimado debe ser mayor a 0 |
| RN-004 | Debe existir al menos un miembro del equipo |
| RN-005 | La unidad organizacional debe ser válida |

### Mockup/Prototipo

> Referencia: https://miro.com/app/board/xxx/crear-caso

### Datos de Prueba

| Escenario | Input | Output Esperado |
|-----------|-------|-----------------|
| Happy path | Nombre: "Contrato TI", Monto: 50000, Tipo: Licitación | Caso creado en DRAFT |
| Sin nombre | Nombre: "", resto válido | Error: "El nombre es requerido" |
| Monto cero | Monto: 0 | Error: "El monto debe ser mayor a 0" |

### Dependencias

- [ ] 200-14839-001: Endpoint POST /cases (Backend Domain)
- [ ] Catálogo: CASE_TYPES (tipos de caso)
- [ ] Catálogo: PROCESS_TYPES (tipos de proceso)
- [ ] Catálogo: CURRENCY_TYPES (monedas)
- [ ] 200-14840-001: GET /organizational-units (API Cross)

### Notas Técnicas

- Integración con Happy para obtener usuario actual
- Documentos se suben a S3 antes de crear el caso
- El código se genera con formato: {AÑO}-{SECUENCIA:5}

---

**Prioridad:** Alta
**Estimación:** L
**Sprint:** 1
```
