---
id: ADR-017
titulo: Los entregables siguen el formato USS y la estructura SEUSS / Ellucian / Resultado
estado: aceptado
fecha: 2026-09-26
fuentes: [C10, C12]
temas: [entregables]
---
# ADR-017 · Los entregables siguen el formato USS y la estructura SEUSS / Ellucian / Resultado

## Contexto
El usuario pidió entregables cortos, con pocas tablas, ejemplos de los tres centros, siglas con su significado y su autoría (C12). Lo que anota de SEUSS es lo que se hace hoy (C10).

## Decisión
- Estructura fija: **«Hoy en SEUSS»** (lo que dice el usuario, sin interpretar), **«En Ellucian»** (con cita del instructivo y la diapositiva) y **«Resultado»**.
- **Siempre** ejemplos de los tres centros. Todas las dudas al final, separadas en «Para Ellucian» y «Para la USS».
- Autor: «Elaborado por: Dagner Anibal Chuman Lluen».
- Paleta USS: morado #7030A0 / #5C2193 y verdes #4EA72E / #92D050. PDF por defecto; PPTX solo si lo pide.

## Alternativas descartadas
- **Documentos largos con muchas tablas:** «me pones varias tablas que me pierdo».

## Consecuencias
- Detalle y herramientas en las skills `documentos-uss` y `workflow-entregables-uss`.

## Criterio de salida
Que la USS entregue otra plantilla oficial.

## Relacionado
- [ADR-004](ADR-004-glosario-unico.md)
