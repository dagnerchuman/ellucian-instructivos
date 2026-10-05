---
id: ADR-020
titulo: La carga de los docentes de Centros se mediría por contrato (SIAFLCT y SIACONA)
estado: propuesto
fecha: 2026-10-05
fuentes: [C53, C54, C55, R19, E20, U28]
temas: [carga, docentes, contratos]
---
# ADR-020 · La carga de los docentes de Centros se mediría por contrato (SIAFLCT y SIACONA)

## Contexto
En Centros Empresariales hay dos tipos de docente (C54):
- **especialistas**, a tiempo completo con **48 horas**;
- **facilitadores**, a tiempo parcial según su carga.

**Pregrado queda fuera:** sus docentes están en otros periodos (C55, [ADR-001](ADR-001-alcance-solo-centros.md)). Las reglas de carga y el factor FTE de SIATERM son **por periodo**, así que en los periodos de Centros (2026 5x) solo cuentan los NRC de Centros.

Banner ofrece dos formas de medir la carga, que el instructivo no hace excluyentes (R19):
- **por regla de carga:** el tipo de asignación (docente, investigador…); se configura en SIAFLRT y se ve en SIAASGN;
- **por contrato:** tiempo completo, tiempo parcial o por horas; se configura en SIAFLCT y se ve en SIACONA.

## Decisión (propuesta)
En los periodos de Centros, la carga se mide **por contrato**:
- **Especialista:** contrato a tiempo completo, con regla en SIAFLCT de «Total de carga de trabajo» de 48 a 48.
- **Facilitador:** contrato a tiempo parcial, con el rango de horas que defina la USS (U28).
- **SIATERM:** el factor FTE de cada periodo de Centros va en **48**, para que un especialista sea 1 FTE (por confirmar con Ellucian, E20).
- **SIAASGN:** cada NRC lleva el contrato del docente en «Tipo de contrato».
- **SIACONA:** muestra si cada docente está debajo (U) o encima (O) de su contrato.
- Los códigos los define la USS. En PROD ya existen el tipo `CE` (*Continuing Ed*) y la regla `PTCE` (*Part Time/Continuing Education*).

## Alternativas descartadas
- **Solo por regla de carga (SIAFLRT), con una regla de especialista y otra de facilitador:**
  - funcionaría;
  - pero el instructivo usa la regla para el *tipo de asignación* (docente, investigador) y el contrato para *tiempo completo o parcial* (5.2, diap. 7);
  - mezclarlos haría que la regla deje de servir para lo suyo.
- **Configurar las 40 horas de Pregrado junto a las de Centros:** Pregrado está en otros periodos y fuera del alcance (C55).

## Consecuencias
- Hay que configurar contratos y reglas en SIAINST, SIAFLCT y SIAFCTR, y elegir el contrato de cada NRC en SIAASGN.
- Si los especialistas también matriculan (C46), sus 48 horas incluirían «labor no educativa» en SIAASGN, con los tipos de STVNIST (U28-e).
- La regla de carga (SIAFLRT) puede seguir para el tipo de asignación, si la USS quiere las dos (E20).

## Criterio de salida
- La respuesta de la USS a U28 y la de Ellucian a E20.
- Con esas respuestas, este ADR pasa a `aceptado`, o a `descartado` si eligen medir solo por regla.

## Relacionado
- [ADR-011](ADR-011-carga-lectiva.md) · [ADR-010](ADR-010-usuarios-y-poblacion.md) · instructivo 5.2 Carga de trabajo docente
