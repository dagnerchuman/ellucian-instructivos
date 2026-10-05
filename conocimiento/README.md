# Base de conocimiento del proyecto

Memoria compartida de las personas y los agentes (Claude Code, Antigravity u otros) que trabajan en los **Centros Empresariales de la USS en Ellucian Banner**. Está versionada en git y se puede abrir en Obsidian: abre el repositorio como bóveda y usa la vista de grafo.

| Qué | Dónde | Para qué |
|---|---|---|
| **Manifest** | [`manifest.json`](manifest.json) | Fuente única de **qué existe**: centros, fuentes de datos, generadores, contratos entre piezas, sistemas, actores y skills |
| **Decisiones (ADR)** | [`decisiones/`](decisiones/) | **Por qué** se decidió cada cosa, qué se descartó y cuándo revisarlo |
| **Registro** | [`registro.md`](../.claude/skills/preguntas-y-dudas-centros/registro.md) | Qué se **confirmó** (C##), qué se **resolvió** con los instructivos (R##) y qué **dudas** siguen abiertas (E##, U##) |
| **Datos de cada centro** | `centros/<centro>/datos.json` | Códigos, partes, NRC de prueba y estado de los scripts |
| **Auditoría** | [`auditoria-2026-10-05.md`](auditoria-2026-10-05.md) | Contradicciones que aparecieron al escribir los ADR |

## Reglas para cualquier agente

1. **Antes de tocar nada, arma el contexto:**
   - lee este archivo y el `manifest.json`;
   - lee los ADR **aceptados** del tema de la tarea;
   - lee en el registro lo confirmado y las dudas abiertas.
2. **Un ADR aceptado es una restricción.** Si la tarea necesita contradecirlo, **detente y pide al usuario una revisión explícita**. Nunca lo pases por alto en silencio. Si el usuario cambia la decisión:
   - escribe un ADR nuevo;
   - marca el viejo `reemplazado`, con `reemplazado_por`.
3. **Al terminar, devuelve lo aprendido a la base:**
   - registro: C## (lo que confirmó el usuario), U## o E## (dudas nuevas);
   - un ADR nuevo cuando se decide algo con alternativas;
   - `datos.json` del centro (y regenera los diagramas);
   - el `manifest.json`, si apareció una pieza nueva.
4. **Valida** antes de subir:
   ```bash
   python3 herramientas/validar_conocimiento.py
   ```
   Revisa enlaces rotos, metadatos de los ADR, que las fuentes citadas existan en el registro, la consistencia del manifest y de los `datos.json`, el espejo de skills y que no se cuelen datos sensibles.

## Decisiones

| ADR | Decisión | Estado |
|---|---|---|
| [ADR-001](decisiones/ADR-001-alcance-solo-centros.md) | El alcance son solo los tres Centros Empresariales | aceptado |
| [ADR-002](decisiones/ADR-002-fuente-unica-por-centro.md) | Cada centro tiene una sola fuente de datos y nada se inventa | aceptado |
| [ADR-003](decisiones/ADR-003-diagramas-generados.md) | Diagramas generados: un flujo, un código, un término | aceptado |
| [ADR-004](decisiones/ADR-004-glosario-unico.md) | Un solo término por concepto y siglas con su significado | aceptado |
| [ADR-005](decisiones/ADR-005-periodos.md) | Periodos de seis dígitos y tres periodos al año | aceptado |
| [ADR-006](decisiones/ADR-006-partes-de-periodo.md) | Los grupos de cada centro son partes de periodo | aceptado |
| [ADR-007](decisiones/ADR-007-hora-de-clase.md) | La hora de clase es de 45 minutos de día y 50 de noche | aceptado |
| [ADR-008](decisiones/ADR-008-idiomas-prerrequisito-fatal.md) | En Idiomas, BASIC II exige BASIC I aprobado o examen de suficiencia | aceptado |
| [ADR-009](decisiones/ADR-009-computacion-escala-v.md) | Computación califica con el modo V (nota mínima 11) y no rinde suficiencia | aceptado |
| [ADR-010](decisiones/ADR-010-usuarios-y-poblacion.md) | Matriculan los jefes, especialistas y asistentes, a alumnos de la USS y externos | aceptado |
| [ADR-011](decisiones/ADR-011-carga-lectiva.md) | La carga lectiva se arma en Banner y se aprueba por oficio en la intranet | aceptado |
| [ADR-012](decisiones/ADR-012-egresados-idiomas.md) | Los egresados de Idiomas se califican con la nota de la plataforma, en un solo NRC | aceptado |
| [ADR-013](decisiones/ADR-013-quejas-como-solicitud.md) | Las quejas se atenderían como solicitudes de servicio | propuesto |
| [ADR-014](decisiones/ADR-014-skills-espejo.md) | Las skills se editan en .claude y se copian a .agents | aceptado |
| [ADR-015](decisiones/ADR-015-visor-y-rutas.md) | Las carpetas CAPACIDAD no se mueven | aceptado |
| [ADR-016](decisiones/ADR-016-confidencialidad-y-publicacion.md) | Netlify publica solo main, y en main se publica solo lo que pide el usuario | aceptado |
| [ADR-017](decisiones/ADR-017-formato-entregables-uss.md) | Los entregables siguen el formato USS y la estructura SEUSS / Ellucian / Resultado | aceptado |
| [ADR-018](decisiones/ADR-018-base-de-conocimiento.md) | El conocimiento del proyecto vive como código, y los ADR aceptados son restricciones | aceptado |
| [ADR-019](decisiones/ADR-019-ligas-ingles.md) | En Inglés, el NRC teórico y el club de conversación van unidos por una liga | aceptado |

Para una decisión nueva, copia [`decisiones/plantilla-adr.md`](decisiones/plantilla-adr.md).
