---
id: ADR-014
titulo: Las skills se editan en .claude y se copian a .agents
estado: aceptado
fecha: 2026-10-03
fuentes: [C40]
temas: [agentes, memoria]
---
# ADR-014 · Las skills se editan en .claude y se copian a .agents

## Contexto
El usuario trabaja con Claude Code y con Antigravity. Cada uno lee su carpeta de skills, y una sincronización en las dos direcciones podía perder cambios.

## Decisión
- Las skills se editan en **`.claude/skills/`** y se copian en espejo con `python3 herramientas/sincronizar_skills.py --desde claude`.
- Si las editó Antigravity, se usa `--desde agents`.
- `--check` comprueba que las dos carpetas sean iguales; el validador de conocimiento también lo revisa.

## Alternativas descartadas
- **Enlaces simbólicos:** fallan en Windows.
- **Sincronizar en las dos direcciones gana el más nuevo:** puede pisar cambios.

## Consecuencias
- Hay que acordarse de sincronizar. El validador avisa si no se hizo.

## Criterio de salida
Que las dos herramientas lean la misma carpeta.

## Relacionado
- [ADR-018](ADR-018-base-de-conocimiento.md)
