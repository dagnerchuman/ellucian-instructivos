---
id: ADR-012
titulo: Los egresados de Idiomas se califican con la nota de la plataforma, en un solo NRC
estado: aceptado
fecha: 2026-10-05
fuentes: [C50, U24]
temas: [idiomas, egresados]
---
# ADR-012 · Los egresados de Idiomas se califican con la nota de la plataforma, en un solo NRC

## Contexto
El Script 05 («Curso especial para egresados») no tenía definición. El usuario consultó con Idiomas (C50).

## Decisión
- El egresado **no se matricula en un curso:** se le activa la plataforma de inglés, fuera de Banner.
- La nota de la plataforma se pone **igual en BASIC I, BASIC II, etc.**, como un examen de suficiencia. El costo del servicio es distinto.
- En Banner se crea **un solo NRC** y la nota se pasa **a mano**.

## Alternativas descartadas
- **Un NRC intensivo por nivel:** no es lo que hace Idiomas.

## Consecuencias
- Falta definir en qué página se pasa la nota a cada BASIC, el nombre de la plataforma y el servicio de cobro (U24).
- Falta saber si Computación y Emprendimiento hacen lo mismo con sus egresados (U24). Hasta entonces, su Script 05 sigue pendiente.

## Criterio de salida
Las respuestas a U24, o que la plataforma se integre con Banner.

## Relacionado
- [ADR-008](ADR-008-idiomas-prerrequisito-fatal.md) · diagrama «Script 05» de Idiomas
