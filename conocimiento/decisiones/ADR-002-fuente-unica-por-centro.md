---
id: ADR-002
titulo: Cada centro tiene una sola fuente de datos y nada se inventa
estado: aceptado
fecha: 2026-10-03
fuentes: [C40]
temas: [datos, centros]
---
# ADR-002 · Cada centro tiene una sola fuente de datos y nada se inventa

## Contexto
Los diagramas de `diagramas_flujo/` mezclaban datos de Computación bajo el nombre de los tres centros, y los mismos códigos estaban copiados en muchos archivos (C40).

## Decisión
- Los datos de cada centro viven en **`centros/<centro>/datos.json`**; lo común, en `centros/comun/datos.json`.
- Un valor `null` significa **«por confirmar»** y se muestra así. Nunca se inventa un código de la USS. Un dato ilustrativo se marca «de ejemplo».
- Las fichas, los índices y los diagramas se **generan** desde esos archivos.

## Alternativas descartadas
- **Datos escritos en cada documento:** se desactualizan y se contradicen.
- **Rellenar con datos de Computación lo que falta en Idiomas o Emprendimiento:** confunde al lector y no es cierto.

## Consecuencias
- Para cambiar un dato se edita un solo archivo y se regenera.
- Los centros todavía sin probar se ven con muchos «por confirmar». Es correcto: muestra lo que falta.

## Criterio de salida
Que la USS entregue una fuente oficial, como un reporte de Banner o un API, que reemplace los `datos.json`.

## Relacionado
- [ADR-003](ADR-003-diagramas-generados.md) · [ADR-001](ADR-001-alcance-solo-centros.md)
