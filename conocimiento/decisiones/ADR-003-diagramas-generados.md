---
id: ADR-003
titulo: Los diagramas se generan con Archify y tienen un solo flujo, un código por paso y un término por concepto
estado: aceptado
fecha: 2026-10-05
fuentes: [C40, C49]
temas: [diagramas]
---
# ADR-003 · Diagramas generados: un flujo, un código, un término

## Contexto
La primera versión tenía nodos con dos códigos («SCACRSE · SMAAREA»), varias casuísticas en paralelo y sinónimos mezclados. El usuario pidió que quedaran «hermosos y específicos, un solo flujo, un solo código o término» (C49).

## Decisión
- Los diagramas se generan con **Archify** desde `herramientas/diagramas/plantillas.py` y los `datos.json`. **No se editan a mano.**
- **Un solo flujo por diagrama**, sin ramas. Los errores y las variantes van en las tarjetas, y cada casuística tiene su propio diagrama.
- **Un solo código por paso:** una página de Banner o, fuera de Banner, un solo término (Oficio, Plataforma).
- **Un solo término por concepto,** según [ADR-004](ADR-004-glosario-unico.md).
- El recorrido completo es una **secuencia** que muestra quién hace cada paso.
- Todo diagrama pasa la validación `showcase` de Archify antes de subirse.

## Alternativas descartadas
- **Diagramas a mano** (draw.io, PowerPoint): se desactualizan cuando cambia un dato.
- **Un diagrama grande con todos los casos:** se ve recargado y no enseña nada concreto.

## Consecuencias
- Hay 14 diagramas por centro, más el comparativo. Son más archivos, pero cada uno es una lección.
- Los errores frecuentes no se ven en el PNG, solo en las tarjetas del HTML.

## Criterio de salida
Que Archify deje de mantenerse o que la USS imponga otra herramienta de diagramas.

## Relacionado
- Skill `workflow-diagramas-archify` · [ADR-002](ADR-002-fuente-unica-por-centro.md)
