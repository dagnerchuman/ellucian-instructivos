---
id: ADR-010
titulo: Matriculan los jefes, especialistas y asistentes, a alumnos de la USS y externos
estado: aceptado
fecha: 2026-10-05
fuentes: [C46]
temas: [usuarios, matricula, propuesta]
---
# ADR-010 · Matriculan los jefes, especialistas y asistentes, a alumnos de la USS y externos

## Contexto
Pedro Pérez Martinto pidió identificar a los usuarios finales por niveles (A, B, C y D) para el plan de capacitación.

## Decisión
- **Usuarios administrativos:** jefes, especialistas y asistentes de cada centro, o quien tenga permisos en Banner. **Todos matriculan,** incluidos los jefes, así que son Nivel A.
- Los **especialistas** (`ES`) son además docentes a tiempo completo de 48 horas, con funciones administrativas (C56, [ADR-020](ADR-020-carga-por-contrato.md)).
- **Población que se matricula:** alumnos de la USS (Pregrado y Posgrado) y **externos**, que no son de la USS o vienen de otras universidades.
- La matrícula se hace en el backoffice: GOAMTCH → SAAQUIK → SFAREGS.

## Alternativas descartadas
- **Jefes solo de consulta (Nivel B):** el usuario confirmó que también matriculan.

## Consecuencias
- Los jefes reciben la capacitación avanzada (backoffice).
- La duda U06 (quién matricula) queda resuelta en parte por esta decisión.

## Criterio de salida
Que la USS cambie los roles o habilite la matrícula por autoservicio para los centros.

## Relacionado
- `docs/propuesta-usuarios-finales/` · [ADR-011](ADR-011-carga-lectiva.md) · [ADR-016](ADR-016-confidencialidad-y-publicacion.md)
