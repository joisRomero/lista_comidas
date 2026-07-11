---
inclusion: always
---

# Documento Zero — Carga automática

Al iniciar cualquier workflow AI-DLC, **antes de ejecutar Requirements Analysis**, busca un archivo de brief del proyecto en estas ubicaciones (en orden):

1. `aidlc-docs/documento-zero.md`
2. `documento-zero.md` (raíz del workspace)

Si el archivo existe:

- Léelo completo y úsalo como **input pre-cargado** para Requirements Analysis.
- Las secciones que estén llenas son **HARD CONSTRAINTS** — no vuelvas a preguntar lo que ya está respondido.
- Las secciones que estén vacías o digan "pendiente" son **preguntas abiertas** — inclúyelas en las clarifying questions de Requirements Analysis.
- La sección "Lo que ya sé que no está claro" (§8) debe tratarse como **ambigüedades declaradas** — resolverlas tiene prioridad sobre descubrir nuevas.

Si el archivo NO existe:

- Continúa normalmente con Requirements Analysis. El agente preguntará todo desde cero.
- No menciones el documento zero ni sugieras crearlo — el usuario sabe que existe como opción.

## Referencia del template

El template está en `docs/templates/documento-zero-template.md` dentro del repo Framework-IA. El usuario lo copia al proyecto y lo llena antes de arrancar AI-DLC.
