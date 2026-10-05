---
id: ADR-009
titulo: Computación califica con el modo V (nota mínima 11) y no rinde suficiencia
estado: aceptado
fecha: 2026-10-02
fuentes: [C27, C34, C35, C36, U20]
temas: [computacion, notas]
---
# ADR-009 · Computación califica con el modo V (nota mínima 11) y no rinde suficiencia

## Contexto
SHRROLL falló con «No Substitute Grade Found», porque el curso exige el modo **V** y la escala del nivel C solo tenía **P** (C34). Además, el usuario confirmó que Computación no tiene examen de suficiencia (C36).

## Decisión
- La escala del nivel **C** en SHAGRDE tiene el modo **V** (vigesimal regular): aprueba con **11**; 10 e INH no aprueban (C27, C35).
- Computación **no** rinde examen de suficiencia.

## Alternativas descartadas
- **Cambiar el curso al modo P:** el catálogo de la USS ya usa V.

## Consecuencias
- **Lección para los otros centros:** antes del primer pase a historia de Idiomas (I) y Emprendimiento (M), revisar que SHAGRDE tenga el modo de sus cursos (U20).

## Criterio de salida
Que la USS cambie la escala de los centros.

## Relacionado
- Skill `centro-computacion` · [ADR-008](ADR-008-idiomas-prerrequisito-fatal.md)
