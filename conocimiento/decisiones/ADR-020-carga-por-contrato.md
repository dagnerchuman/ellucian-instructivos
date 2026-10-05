---
id: ADR-020
titulo: La carga de los docentes de Centros se mediría por contrato (SIAFLCT y SIACONA)
estado: propuesto
fecha: 2026-10-05
fuentes: [C53, C54, R19, E20, U28]
temas: [carga, docentes, contratos]
---
# ADR-020 · La carga de los docentes de Centros se mediría por contrato (SIAFLCT y SIACONA)

## Contexto
En la USS, el docente a tiempo completo de **Pregrado** tiene **40 horas**. En **Centros Empresariales** hay dos tipos (C54):
- **especialistas**, a tiempo completo con **48 horas**;
- **facilitadores**, a tiempo parcial según su carga.

Un mismo docente puede dictar en Pregrado y en Centros. Banner ofrece dos formas de medir la carga, que el instructivo no hace excluyentes (R19):
- **por regla de carga de trabajo:** una por docente; se configura en SIAFLRT y se ve en SIAASGN;
- **por contrato:** el docente puede tener varios; se configura en SIAFLCT y se ve en SIACONA.

## Decisión (propuesta)
Medir la carga **por contrato**:
- **Un contrato por tipo de docente,** cada uno con su regla en SIAFLCT:
  - Pregrado a tiempo completo: «Total de carga de trabajo» de 40 a 40;
  - especialista de Centros: de 48 a 48;
  - facilitador: el rango que defina la USS (U28).
- **Cada NRC tributa a su contrato:** se elige en el campo «Tipo de contrato» de SIAASGN. Así, un docente de Pregrado que también dicta en Centros tiene su carga separada.
- **SIACONA** muestra si cada docente está debajo (U) o encima (O) de su contrato.
- Los códigos de contrato y de regla los define la USS. En PROD ya existen el tipo `CE` (*Continuing Ed*) y la regla `PTCE` (*Part Time/Continuing Education*).

## Alternativas descartadas
- **Solo por regla de carga (SIAFLRT):** hay una sola regla por docente y suma todos sus NRC. No separa Pregrado de Centros ni distingue 40 de 48 horas si el docente tiene las dos funciones.
- **Diferenciar 40 y 48 con el factor FTE de SIATERM:** es uno solo por periodo y vale para todos los docentes.

## Consecuencias
- Hay que configurar contratos y reglas en SIAINST, SIAFLCT y SIAFCTR, y elegir el contrato de cada NRC en SIAASGN.
- Si los especialistas también matriculan (C46), sus 48 horas incluirían «labor no educativa» en SIAASGN, con los tipos de STVNIST (U28-e).
- La regla de carga (SIAFLRT) puede seguir para el tipo de asignación (docente, investigador), si la USS quiere las dos (E20).

## Criterio de salida
- La respuesta de la USS a U28 y la de Ellucian a E20.
- Con esas respuestas, este ADR pasa a `aceptado`, o a `descartado` si eligen medir solo por regla.

## Relacionado
- [ADR-011](ADR-011-carga-lectiva.md) · [ADR-010](ADR-010-usuarios-y-poblacion.md) · instructivo 5.2 Carga de trabajo docente
