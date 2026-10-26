# Dudas: preguntas en Word para responder y devolver

| Archivo | Qué es |
|---|---|
| `PREGUNTAS PARA ELLUCIAN - REUNIÓN 27-10 - CENTROS EMPRESARIALES.docx` | 26 preguntas para Ellucian, 19 para la USS y lo que falta para seguir aprendiendo (datos y pruebas pendientes en TEST), cada una con su recuadro «Respuesta» |

## Cómo se usa
1. En la reunión, escriba la respuesta en el recuadro de cada pregunta, quién respondió y el estado (☒ Resuelta, ☒ Sigue abierta o ☒ Lo revisa Ellucian).
2. Envíe el Word al asistente (Claude Code o Antigravity). Las respuestas se leen por código (E01, U32…):
   ```bash
   python3 .claude/skills/documentos-uss/fuentes/preguntas/leer_respuestas.py "docs/dudas/<archivo>.docx"
   ```
3. Cada respuesta pasa al registro (`C##`), se cierra o se actualiza la duda, se corrigen los `datos.json` y se regeneran los diagramas y la base del asistente.

## Cómo se genera
Las preguntas salen del registro de dudas (`.claude/skills/preguntas-y-dudas-centros/registro.md`), por su código; el generador solo las agrupa, les pone un título y agrega «Lo que ya sabemos»:
```bash
python3 .claude/skills/documentos-uss/fuentes/preguntas/build_preguntas.py "docs/dudas/<archivo>.docx"
```
Para una reunión nueva, cambie `FECHA_REUNION` y la lista de bloques en `build_preguntas.py`.
