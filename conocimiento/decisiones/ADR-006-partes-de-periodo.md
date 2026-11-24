---
id: ADR-006
titulo: Los grupos de cada centro son partes de periodo
estado: aceptado
fecha: 2026-09-28
fuentes: [C02, C15, C45, C140, C238]
temas: [periodos, nrc]
---
# ADR-006 · Los grupos de cada centro son partes de periodo

## Contexto
Los centros abren cursos cada mes (C02), pero Banner tiene pocos periodos al año: año + 5 en TEST 2026 ([ADR-005](ADR-005-periodos.md), reemplazado) y 202721 desde 2027 ([ADR-026](ADR-026-periodo-202721.md)).

## Decisión
Cada grupo del centro es una **parte de periodo** dentro del periodo, con sus fechas y semanas. El NRC se programa en esa parte:
- Idiomas: parte general `IGE`, `I01` a `I12`.
- Computación: `CGE`, `X01` a `X12`.
- Emprendimiento: `EGE`, `P01` a `P12`.

Los códigos están en STVPTRM (C140). En 202721, visto en TEST, se usan `I01` a `I04`, `P01` y `P02`, `X01` a `X03` y la parte `1` «Período Completo», que Banner pide siempre (C238).

## Alternativas descartadas
- **Un periodo por grupo:** multiplica los periodos y rompe la regla de seis dígitos.

## Consecuencias
- Las fechas de cada grupo se mantienen en SOATERM (partes) y se copian a `datos.json`. Las dan las jefaturas, desde sus mallas (C238, U58).
- En 202721, `I04`, `P02` y `X03` terminan después del 31-MAR-2027, fin del periodo: falta saber si Banner lo admite (E34).
- Si un nivel dura más que su parte (Idiomas nivel III, 12–13 semanas), hay que decidir si va en otra parte.

## Criterio de salida
Que la USS cambie el cronograma, o que 202721 en producción confirme otra estructura (U22, U58).

## Relacionado
- `centros/<centro>/datos.json › partes_2026`
