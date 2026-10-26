---
id: ADR-023
titulo: Cada tipo de archivo tiene su carpeta y la raíz solo guarda instrucciones y publicación
estado: aceptado
fecha: 2026-10-26
fuentes: [C118]
temas: [repositorio, carpetas, documentos]
---
# ADR-023 · Estructura del repositorio

## Contexto
El usuario pidió ordenar el proyecto: «no quiero que todo esté desordenado, revisa la arquitectura» (C118). En la raíz había una copia vieja de las skills de video (`agent/`), una carpeta suelta con un PPTX (`nueva ppt/`) y ningún README. En `docs/` estaban todos los archivos juntos, con un `.txt` idéntico a su `.md`. Los CSV de la guía operativa estaban dentro de `herramientas/`, aunque no son código.

## Decisión
- **Raíz:** solo las instrucciones (`README.md`, `CLAUDE.md`, `AGENTS.md`), la publicación del sitio (`index.html`, `_redirects`, `netlify.toml`), `skills-lock.json` y las carpetas de trabajo.
- **`CAPACIDAD n/`** no cambia ([ADR-015](ADR-015-visor-y-rutas.md)).
- **`centros/`**, datos y diagramas de cada centro ([ADR-002](ADR-002-fuente-unica-por-centro.md), [ADR-003](ADR-003-diagramas-generados.md)); **`conocimiento/`**, manifest, ADR y auditorías ([ADR-018](ADR-018-base-de-conocimiento.md)); **`visor_instructivos/`**, el sitio.
- **`herramientas/`** guarda solo código que genera o revisa algo. Los datos de entrada van a `docs/fuentes/`.
- **`docs/`** se ordena por tipo: `dudas/` (preguntas en Word para responder y devolver), `afiches/`, `capacitacion/`, `arquitectura/`, `presentaciones/`, `fuentes/` y `propuesta-usuarios-finales/` (sin cambios por [ADR-016](ADR-016-confidencialidad-y-publicacion.md)).
- **Skills:** las del proyecto en `.claude/skills/` con espejo en `.agents/skills/` ([ADR-014](ADR-014-skills-espejo.md)). Las de terceros (HyperFrames, para el piloto de video) quedan solo en `.agents/skills/`; se quitó la copia `agent/`.
- **Generadores de entregables:** en `.claude/skills/documentos-uss/fuentes/`, uno por entregable.

## Alternativas descartadas
- **Mover los instructivos a `docs/instructivos/`:** rompe el visor y las citas (ADR-015).
- **Ordenar `docs/` por fecha:** cuesta encontrar un documento; por tipo se ubica con el nombre.
- **Mover el piloto de video a `docs/`:** su estado de HyperFrames guarda rutas absolutas de `herramientas/videos/`; se deja donde está.

## Consecuencias
- El README de la raíz tiene el mapa y la tabla «Dónde va algo nuevo».
- Antes de crear una carpeta en la raíz, se revisa este ADR.

## Criterio de salida
Revisar si se cambia el sitio de publicación, si el visor deja de depender de las rutas de `CAPACIDAD n/` o si aparece un tipo de documento que no cabe en `docs/`.

## Relacionado
- [ADR-014](ADR-014-skills-espejo.md) · [ADR-015](ADR-015-visor-y-rutas.md) · [ADR-016](ADR-016-confidencialidad-y-publicacion.md) · [ADR-018](ADR-018-base-de-conocimiento.md)
