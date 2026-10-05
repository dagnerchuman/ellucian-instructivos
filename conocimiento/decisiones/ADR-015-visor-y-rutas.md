---
id: ADR-015
titulo: Las carpetas CAPACIDAD no se mueven
estado: aceptado
fecha: 2026-10-03
fuentes: [C40]
temas: [visor, estructura]
---
# ADR-015 · Las carpetas CAPACIDAD no se mueven

## Contexto
El visor web (`visor_instructivos/data.js`) apunta a cada instructivo por su ruta dentro de `CAPACIDAD n/`.

## Decisión
Los instructivos y los scripts de prueba se quedan en `CAPACIDAD n/` con sus nombres originales. Lo nuevo va en `centros/`, `herramientas/`, `docs/` y `conocimiento/`.

## Alternativas descartadas
- **Reordenarlos por centro:** rompe el visor y los enlaces publicados.

## Consecuencias
- La organización por centro vive en `centros/` y en los `datos.json`, no en las carpetas de instructivos.

## Criterio de salida
Que el visor se regenere a partir de un índice que no dependa de las rutas.

## Relacionado
- [ADR-016](ADR-016-confidencialidad-y-publicacion.md)
