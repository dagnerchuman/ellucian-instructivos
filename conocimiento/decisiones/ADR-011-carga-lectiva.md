---
id: ADR-011
titulo: La carga lectiva se arma en Banner y se aprueba por oficio en la intranet
estado: aceptado
fecha: 2026-10-05
fuentes: [R17, R19, C29, C47, C48, C53]
temas: [carga, docentes, aprobacion]
---
# ADR-011 · La carga lectiva se arma en Banner y se aprueba por oficio en la intranet

## Contexto
Hoy la carga docente se hace en Excel (C03). El instructivo 5.2 explica cómo se calcula en Banner, pero no tiene ningún paso de aprobación.

## Decisión
1. **En Banner** (R17): SIAINST (activar al docente) → SSASECT (asignarlo al NRC) → SIAASGN (revisar la carga lectiva). El análisis por contrato va en SIACONA.
2. El **jefe del centro** asigna a los docentes y da su **visto bueno** (C47).
3. **Fuera de Banner** (C48): el jefe envía un oficio por la **intranet de la USS** (asunto, detalle, observación y la carga adjunta), que genera un número de oficio. El **Vicerrector Académico** revisa y emite la **resolución**.

## Alternativas descartadas
- **Aprobar dentro de Banner:** el instructivo 5.2 no trae ese paso.
- **Seguir con Excel:** es lo que la implementación quiere reemplazar (C03).

## Consecuencias
- El Vicerrectorado Académico es Nivel B (consulta en SIAASGN).
- Del script 5.2 faltan la labor no educativa y SIACONA; el responsable es Pedro Martinto.
- Falta decidir **cómo se mide** la carga: por regla (SIAFLRT, en SIAASGN), por contrato (SIAFLCT, en SIACONA) o con las dos. En Centros, los especialistas tienen 48 horas y los facilitadores van según su carga (C54); Pregrado queda fuera porque está en otros periodos (C55). La propuesta es medir por contrato, en [ADR-020](ADR-020-carga-por-contrato.md).

## Criterio de salida
Que la USS decida registrar la aprobación en Banner, por ejemplo con un flujo de Workflow o un campo propio.

## Relacionado
- Diagrama 3 de cada centro · [ADR-010](ADR-010-usuarios-y-poblacion.md)
