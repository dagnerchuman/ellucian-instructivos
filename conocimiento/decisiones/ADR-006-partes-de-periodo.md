---
id: ADR-006
titulo: Los grupos de cada centro son partes de periodo
estado: aceptado
fecha: 2026-09-28
fuentes: [C02, C15, C45]
temas: [periodos, nrc]
---
# ADR-006 · Los grupos de cada centro son partes de periodo

## Contexto
Los centros abren cursos cada mes (C02), pero Banner tiene solo tres periodos al año ([ADR-005](ADR-005-periodos.md)).

## Decisión
Cada grupo del centro es una **parte de periodo** dentro del periodo, con sus fechas y semanas. El NRC se programa en esa parte:
- Idiomas: parte general `IGE`, `I01` a `I12`.
- Computación: `CGE`, `X01` a `X07`.
- Emprendimiento: `EGE`, `P01` a `P06`.

## Alternativas descartadas
- **Un periodo por grupo:** multiplica los periodos y rompe la regla de seis dígitos.

## Consecuencias
- Las fechas de cada grupo se mantienen en SOATERM (partes) y se copian a `datos.json`.
- Si un nivel dura más que su parte (Idiomas nivel III, 12–13 semanas), hay que decidir si va en otra parte.

## Criterio de salida
Que la USS cambie el cronograma, o que 202751 confirme otra estructura (U22).

## Relacionado
- `centros/<centro>/datos.json › partes_2026`
