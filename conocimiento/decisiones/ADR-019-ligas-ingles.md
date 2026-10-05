---
id: ADR-019
titulo: En Inglés, el NRC teórico y el club de conversación van unidos por una liga
estado: aceptado
fecha: 2026-10-05
fuentes: [C52, R18, U27]
temas: [idiomas, nrc, matricula]
---
# ADR-019 · En Inglés, el NRC teórico y el club de conversación van unidos por una liga

## Contexto
Cada curso de Inglés tiene una parte teórica y un club de conversación (C52). En Banner, un curso se programa como NRC, y un mismo curso puede tener varios NRC. El instructivo «5.3_4.1.4.1.9 Crear Ligas» explica cómo unir NRC del mismo curso para que el alumno los matricule juntos (R18).

## Decisión
- El **teórico** y el **club de conversación** son **dos NRC del mismo curso**, unidos por una **liga**.
- **En SSASECT:** cada NRC lleva su «Identificador de liga». El teórico usa `TE` (tipo de horario Teoría); el del club está por confirmar (U27).
- **En SSADETL:** cada NRC lleva, en «Conector de liga», la liga del otro.
- Según el instructivo, el teórico lleva los créditos, se califica y se cobra. El club va con 0 créditos, sin calificación y con «Dispensa de colegiatura y cuotas». La USS debe confirmarlo (U27).

## Alternativas descartadas
- **Un solo NRC con dos horarios:** el club no tendría su propio cupo ni su propio docente.
- **El club como curso aparte, con correquisito (SCADETL):** sería otro curso en el catálogo y en la historia, y el usuario dijo que es el mismo curso.

## Consecuencias
- Para cada curso de Inglés se programan al menos dos NRC: más trabajo en SSASECT, pero cupos y docentes separados.
- Si SOATERM tiene «Ligas» en **Fatal**, Banner no deja matricular el teórico sin el club; el sobrepaso es la casilla «Enlaces» de SFAROVR.
- En el Autoservicio, el alumno ve las «Secciones ligadas» y debe agregar las dos.

## Criterio de salida
- Que la USS confirme otra forma de programar el club.
- O que en TEST el curso no tenga dos tipos de horario en SCACRSE, que es la premisa de las ligas.

## Relacionado
- [ADR-008](ADR-008-idiomas-prerrequisito-fatal.md) · diagrama «Ligas» de Idiomas · `centros/idiomas/pruebas-test.md`
