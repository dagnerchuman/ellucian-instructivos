---
id: ADR-008
titulo: En Idiomas, BASIC II exige BASIC I aprobado o examen de suficiencia
estado: aceptado
fecha: 2026-09-26
fuentes: [C11, R03, R09, S03, U01]
temas: [idiomas, prerrequisitos]
---
# ADR-008 · En Idiomas, BASIC II exige BASIC I aprobado o examen de suficiencia

## Contexto
En SEUSS, quien desaprueba BASIC I no pasa a BASIC II, salvo con un examen de suficiencia (C11). Se llegó a pensar que pasaba automáticamente (S03, descartado).

## Decisión
En Banner, el prerrequisito «BASIC I aprobado **o** examen de suficiencia con puntaje mínimo» va en **SCAPREQ** (lo hereda el NRC en SSAPREQ), con la verificación en **Fatal** en SOATERM. El puntaje se registra en **SOATEST** (R03, R09).

## Alternativas descartadas
- **Pase automático (S03):** no es lo que hace SEUSS.
- **Control manual en la matrícula:** depende de la memoria de quien matricula.

## Consecuencias
- Un sobrepaso en SFAROVR puede saltar la regla; quién lo autoriza está por definir (U10).
- Falta el puntaje mínimo (U01) y cómo queda BASIC I en la historia y en CAPP (E04).

## Criterio de salida
Que la USS cambie la política de avance en Inglés.

## Relacionado
- [ADR-012](ADR-012-egresados-idiomas.md) · skill `centro-idiomas`
