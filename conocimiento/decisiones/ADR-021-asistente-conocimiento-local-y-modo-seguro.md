---
id: ADR-021
titulo: El asistente de diagramas responde con conocimiento local y bloquea pantallas sin evidencia
estado: aceptado
fecha: 2026-10-23
fuentes: [C83, C108]
temas: [asistente, diagramas, conocimiento]
---
# ADR-021 · Asistente con conocimiento local y modo seguro

## Contexto
El usuario pidió integrar el asistente en las páginas de diagramas con Groq y el modelo Qwen validado, una base de conocimiento local y un modo seguro que no invente pantallas Banner (C83).

## Decisión
- Cada respuesta remota recupera fragmentos de las fuentes locales del proyecto y envía solo esa evidencia a Groq; sin evidencia suficiente no consulta al modelo.
- El conocimiento se genera localmente desde el registro, los datos de los tres centros, las referencias operativas y los ADR aceptados. La base se carga como un asset compartido en las páginas generadas.
- Si la respuesta de Qwen menciona un código de pantalla Banner ausente de la evidencia recuperada, no se muestra la respuesta del modelo y se presenta el extracto local con sus fuentes.
- Se conserva el modo local, que muestra evidencia sin pedir redacción al modelo.
- **Formato profesional (24/10/2026, C108):** el asistente usa tono institucional y trato de usted, sin emojis ni exclamaciones. Responde primero en una o dos oraciones; si es un procedimiento, agrega «Pasos» numerados que empiezan con la página de Banner, y luego «Validado en TEST», «Según el instructivo» y «Por confirmar» solo cuando correspondan. El modo local presenta los extractos limpios, con el nombre de cada fuente.

## Alternativas descartadas
- **Respuestas libres del modelo:** pueden inventar páginas, pasos o datos de los centros.
- **Incrustar toda la base en cada diagrama:** duplica el mismo conocimiento en cada HTML y agranda las salidas generadas.

## Consecuencias
- Las respuestas siguen disponibles sin Groq, pero el modo local presenta extractos y no una síntesis.
- Para refrescar el conocimiento se ejecuta `python3 herramientas/diagramas/generar_conocimiento_asistente.py`; el generador de diagramas lo ejecuta automáticamente antes de inyectar el asistente.
- Groq recibe la consulta y los fragmentos seleccionados cuando el usuario configura su clave. No se deben ingresar datos reales de alumnos.

## Criterio de salida
Revisar si cambia el proveedor/modelo validado, la disponibilidad de la base local o el requisito de no inventar páginas.

## Relacionado
- [ADR-003](ADR-003-diagramas-generados.md) · [ADR-018](ADR-018-base-de-conocimiento.md) · [C83](../../.claude/skills/preguntas-y-dudas-centros/registro.md)
