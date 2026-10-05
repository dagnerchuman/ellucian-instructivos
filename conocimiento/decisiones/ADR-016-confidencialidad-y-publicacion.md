---
id: ADR-016
titulo: Netlify publica solo main, y en main se publica solo lo que pide el usuario
estado: aceptado
fecha: 2026-10-05
fuentes: [C46]
temas: [publicacion, confidencialidad]
---
# ADR-016 · Netlify publica solo main, y en main se publica solo lo que pide el usuario

## Contexto
Netlify publica la rama `main` con `publish = "."`, así que todo lo que está en `main` queda visible en el sitio. La propuesta de usuarios finales es un borrador confidencial: «no enviar aún a Pedro Pérez Martinto».

## Decisión
- Se trabaja en una rama. A `main` se sube **solo cuando el usuario lo pide**.
- `docs/propuesta-usuarios-finales/` no va a `main` mientras sea un borrador. Si algún día hay que llevarla, primero se saca o se confirma con el usuario.
- Los datos sensibles (correos, DNI, contraseñas) no se escriben en `conocimiento/` ni en las skills; el validador lo revisa.

## Alternativas descartadas
- **Publicar todo en main:** expone borradores.

## Consecuencias
- Los diagramas nuevos se ven en Netlify solo cuando la rama se lleva a `main`.

## Criterio de salida
Que la propuesta se envíe oficialmente o que el sitio pase a ser privado.

## Relacionado
- [ADR-010](ADR-010-usuarios-y-poblacion.md) · [ADR-015](ADR-015-visor-y-rutas.md)
