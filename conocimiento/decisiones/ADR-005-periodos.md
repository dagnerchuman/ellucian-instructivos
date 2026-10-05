---
id: ADR-005
titulo: Periodos de seis dígitos y tres periodos al año
estado: aceptado
fecha: 2026-09-26
fuentes: [C04, C45, S01]
temas: [periodos]
---
# ADR-005 · Periodos de seis dígitos y tres periodos al año

## Contexto
SEUSS usa 2026-0, 2026-I y 2026-II. Se llegó a suponer que un periodo duraba 3 meses, pero el usuario dijo «eso la verdad yo ni lo sé» (S01).

## Decisión
- Periodo = **año + 5 (Centros) + secuencia**: 1 verano, 4 semestre I, 6 semestre II.
- 2026-0 = `202651`, 2026-I = `202654`, 2026-II = `202656`, verano 2027 = `202751` (C04, C45).
- El periodo de un grupo lo decide la **fecha de inicio**, no la de fin.

## Alternativas descartadas
- **Periodos de 3 meses (S01):** no confirmado; no usar.
- **Un periodo por mes:** los meses se manejan con partes de periodo ([ADR-006](ADR-006-partes-de-periodo.md)).

## Consecuencias
- Un grupo que empieza en julio y termina en agosto pertenece a 202654.

## Criterio de salida
Que Registros Académicos defina otra codificación para 2027.

## Relacionado
- [ADR-006](ADR-006-partes-de-periodo.md) · U22 (partes del verano 2027)
