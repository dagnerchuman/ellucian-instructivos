---
id: ADR-004
titulo: Un solo término por concepto y siglas con su significado
estado: aceptado
fecha: 2026-10-05
fuentes: [C12, C49]
temas: [lenguaje, entregables]
---
# ADR-004 · Un solo término por concepto y siglas con su significado

## Contexto
En los documentos se usaba «participante», «alumno» y «estudiante» para lo mismo; «sección», «grupo» y «NRC»; «inscripción» y «matrícula». El usuario pidió además que toda sigla lleve su significado entre paréntesis (C12).

## Decisión
Se usan siempre estos términos (lista viva en `TERMINOS` de `herramientas/diagramas/plantillas.py`):

| Término | No usar |
|---|---|
| alumno | participante, estudiante |
| NRC | sección, grupo |
| parte (de periodo), por ejemplo X07 | grupo, mes |
| matrícula / matricular | inscripción / inscribir |
| cupo | vacante, capacidad |
| pase a historia | cierre de actas |
| retención, retiro (DD), carga lectiva | — |

Toda sigla o código va con su significado entre paréntesis la primera vez: «NRC (Número de Referencia de Curso)».

## Alternativas descartadas
- **Usar el término de la pantalla de Banner** («Inscripción de curso»): los nombres oficiales de los scripts de la USS dicen «matrícula», igual que el usuario.

## Consecuencias
- Los mensajes de error de Banner se citan tal cual, aunque digan «inscripción».
- Las entradas viejas del registro conservan sus palabras, porque son históricas.

## Criterio de salida
Que la USS publique un glosario oficial distinto.

## Relacionado
- [ADR-003](ADR-003-diagramas-generados.md) · [ADR-017](ADR-017-formato-entregables-uss.md)
