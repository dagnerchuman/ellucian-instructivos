---
id: ADR-021
titulo: El asistente de diagramas responde con conocimiento local y bloquea pantallas sin evidencia
estado: aceptado
fecha: 2026-10-23
fuentes: [C83, C108, C117, C231, C232, C233, C234, C236]
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
- **Memoria de la conversación (26/10/2026, C117):** el asistente recuerda lo conversado. Una pregunta de seguimiento («pero dime cuáles son», «¿y en Idiomas?») se busca junto con el tema anterior; también una pregunta muy corta que sola no encuentra evidencia. A Groq se le envían, además de la evidencia, los tres últimos turnos (pregunta y respuesta, sin la lista de fuentes). La evidencia recuperada sigue siendo la única fuente y el control de pantallas sin respaldo no cambia. En el modo local se muestran primero las líneas del fragmento que tratan lo preguntado. El botón «Nueva conversación» borra los mensajes y el contexto. Si la primera pregunta solo remite a algo anterior, sin nombrar un tema, el asistente pide el tema.

- **Todos los instructivos y búsqueda por raíces (23/11/2026, C231):** la base suma el texto de los 83 instructivos PPTX (un fragmento por pantalla, con su número de diapositiva) y las skills de los centros y de pruebas en TEST. La búsqueda usa raíces de palabras con peso por rareza (BM25), títulos, número de instructivo y código de Banner, y exige que el fragmento cubra al menos un tercio de lo preguntado. Si la base de la USS y el instructivo difieren, manda la de la USS. El banco `herramientas/diagramas/preguntas_prueba.json` se corre con `node herramientas/diagramas/probar_asistente.mjs` antes de cambiar la búsqueda.
- **Fuentes con nombre y diapositivas citadas (23/11/2026, C232):** cada instructivo se cita con el código y el nombre completo de `herramientas/diagramas/catalogo_instructivos.py`. Las fuentes van agrupadas en «Base de la USS» e «Instructivos de Ellucian», con enlace al visor; al modelo se le pasa el mismo rótulo, nunca la ruta. Si toda la evidencia es del manual de Ellucian, la respuesta lo dice con una etiqueta. Si la respuesta cita diapositivas fuera del índice curado, el asistente las muestra enteras.
- **Lo de la USS manda, con valores de ejemplo (23/11/2026, C233):** cuando la USS hace algo distinto del instructivo, la base de la USS tiene su pregunta frecuente y el asistente la pone primero; por ejemplo, los prerrequisitos van en SCAPPRQ (por programa), no en SCAPREQ (instructivo 1.1.5). En cada paso, el asistente da el valor que se usó o se probó (programa, periodo, curso, nivel, nota) con su C##, y nunca inventa uno. Desde C236 no nombra SCAPREQ ni SSAPREQ, ni muestra sus diapositivas, salvo que se pregunte por ellos; y cada valor de ejemplo va con su caso.

## Alternativas descartadas
- **Respuestas libres del modelo:** pueden inventar páginas, pasos o datos de los centros.
- **Incrustar toda la base en cada diagrama:** duplica el mismo conocimiento en cada HTML y agranda las salidas generadas.

## Consecuencias
- Las respuestas siguen disponibles sin Groq, pero el modo local presenta extractos y no una síntesis.
- Para refrescar el conocimiento se ejecuta `python3 herramientas/diagramas/generar_conocimiento_asistente.py`; el generador de diagramas lo ejecuta automáticamente antes de inyectar el asistente. El asistente (`asistente_ia.js` y `.css`) y su base se cargan como archivos: cambiarlos no regenera ninguna página (C234).
- Groq recibe la consulta, los fragmentos seleccionados y los últimos turnos de la conversación cuando el usuario configura su clave. No se deben ingresar datos reales de alumnos.

## Criterio de salida
Revisar si cambia el proveedor/modelo validado, la disponibilidad de la base local o el requisito de no inventar páginas.

## Relacionado
- [ADR-003](ADR-003-diagramas-generados.md) · [ADR-018](ADR-018-base-de-conocimiento.md) · [C83](../../.claude/skills/preguntas-y-dudas-centros/registro.md)
