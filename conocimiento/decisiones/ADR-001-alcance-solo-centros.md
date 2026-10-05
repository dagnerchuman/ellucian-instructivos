---
id: ADR-001
titulo: El alcance son solo los tres Centros Empresariales
estado: aceptado
fecha: 2026-09-26
fuentes: [C01, C13]
temas: [alcance]
---
# ADR-001 · El alcance son solo los tres Centros Empresariales

## Contexto
El usuario trabaja en los Centros Empresariales de la USS: «somos de idiomas, informática y emprendimiento» (C01). En las reuniones aparecen temas de toda la universidad, como posgrado, programas en rediseño o el docente fallecido (C13).

## Decisión
El proyecto documenta y prueba solo **Idiomas, Computación y Emprendimiento**. Los temas de otras áreas se anotan en el registro como contexto o duda, pero no se convierten en entregables.

## Alternativas descartadas
- **Documentar toda la USS:** el usuario no tiene ese encargo ni esos datos, y el trabajo se diluye.

## Consecuencias
- Todo entregable y todo diagrama dice de qué centro es, y los ejemplos incluyen siempre los tres.
- Los casos generales (docente fallecido, quejas) se prueban con datos de los centros.

## Criterio de salida
Que la USS le encargue al usuario otra capacidad o área.

## Relacionado
- [ADR-002](ADR-002-fuente-unica-por-centro.md) · `centros/`
