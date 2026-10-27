---
id: ADR-024
titulo: Las skills se eligen con una tabla de enrutamiento y se cargan por partes
estado: aceptado
fecha: 2026-10-27
fuentes: [C130]
temas: [agentes, memoria]
---
# ADR-024 · Las skills se eligen con una tabla de enrutamiento y se cargan por partes

## Contexto
`CLAUDE.md` pedía usar las 11 skills del proyecto antes de trabajar, y varias se pisaban: `documentos-uss` y `workflow-entregables-uss`, `preguntas-y-dudas-centros` y `workflow-procesar-reunion`, `arquitectura-centros-empresariales` y `workflow-consultas-banner`. Además, sus descripciones decían qué hacían, pero no cuándo no usarlas. El usuario trajo un «Prompt Maestro» de enrutamiento con carga progresiva (*progressive disclosure*) para que el agente elija la skill correcta sin cargarlas todas (C130).

## Decisión
- `CLAUDE.md` y `AGENTS.md` tienen una **tabla de enrutamiento**: intención del usuario → **una skill principal** → la que se encadena después. La regla de Antigravity (`.agents/rules/centros-empresariales.md`) remite a esa tabla.
- El `SKILL.md` se lee solo al ejecutar el flujo, y de `references/` o `scripts/` solo el archivo de la subtarea.
- El `description` de cada skill del proyecto sigue la fórmula **«Qué hace… Cuándo usarla… Cuándo no usarla…»**, con las palabras que usa el usuario.
- Se adaptó el prompt al proyecto: la validación final es `validar_conocimiento.py` y la de la skill usada (no tipado, linter ni pruebas de software), y los enlaces son relativos al repositorio (no `file:///`).

## Alternativas descartadas
- **Cargar todas las skills al empezar (lo de antes):** gasta contexto y mezcla reglas de skills que no vienen al caso.
- **Copiar el prompt tal cual:** hablaba de un «agente de desarrollo», de linter y tests, y de rutas `file:///`, que aquí no aplican.
- **Fusionar las skills que se pisan:** rompería las rutas que usan otros archivos y el espejo de Antigravity (ADR-014); basta con marcar el límite en la descripción.

## Consecuencias
- Cada skill nueva necesita una fila en la tabla y su «Cuándo no usarla».
- La base de conocimiento (manifest, ADR del tema y registro) se sigue leyendo antes de trabajar (ADR-018), pero solo lo del tema.

## Criterio de salida
Que el agente siga eligiendo mal la skill o que la tabla deje de reflejar las skills que existen.

## Relacionado
- [ADR-014](ADR-014-skills-espejo.md) · [ADR-018](ADR-018-base-de-conocimiento.md)
