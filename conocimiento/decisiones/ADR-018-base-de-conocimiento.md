---
id: ADR-018
titulo: El conocimiento del proyecto vive como código, y los ADR aceptados son restricciones
estado: aceptado
fecha: 2026-10-05
fuentes: [C51]
temas: [agentes, memoria]
---
# ADR-018 · El conocimiento del proyecto vive como código, y los ADR aceptados son restricciones

## Contexto
Cada agente (Claude Code, Antigravity) arrancaba de cero y deducía el contexto leyendo archivos. El «por qué» de cada decisión estaba disperso entre el registro, las skills, los commits y el chat. El usuario pidió una base de conocimiento como la de su equipo de agentes (C51).

## Decisión
- La base vive en **`conocimiento/`**, versionada en git y navegable en Obsidian:
  - `manifest.json` es la fuente única de qué existe: fuentes, generadores, contratos, sistemas, actores y skills;
  - `decisiones/` tiene los ADR.
- **Un ADR `aceptado` es una restricción.** Si una tarea necesita contradecirlo, el agente **se detiene y pide revisión explícita** al usuario. No lo pasa por alto en silencio.
- **Ciclo de cada tarea:** primero se arma el contexto (manifest, ADR del tema, registro). Al final se devuelve lo aprendido: registro (C##, U##…), un ADR nuevo o actualizado, `datos.json`, y se ejecuta `herramientas/validar_conocimiento.py`.
- El validador revisa enlaces rotos, metadatos de los ADR, la consistencia del manifest, las fuentes citadas, el espejo de skills y que no haya datos sensibles.

## Alternativas descartadas
- **Solo el registro:** dice qué se confirmó, pero no qué se descartó ni por qué.
- **Memoria en el chat:** se pierde al cerrar la sesión.

## Consecuencias
- Cada decisión nueva lleva un poco más de trabajo: registro + ADR.
- Al escribir los ADR aparecieron contradicciones; quedan en `auditoria-2026-10-05.md`.

## Criterio de salida
Que el proyecto termine o pase a otro equipo con otro método.

## Relacionado
- [README de la base](../README.md) · [ADR-014](ADR-014-skills-espejo.md)
