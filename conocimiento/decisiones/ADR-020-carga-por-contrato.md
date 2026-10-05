---
id: ADR-020
titulo: La carga de los docentes de Centros se mediría por contrato (SIAFLCT y SIACONA)
estado: propuesto
fecha: 2026-10-05
fuentes: [C46, C53, C54, C55, C56, R19, E20, U28]
temas: [carga, docentes, contratos]
---
# ADR-020 · La carga de los docentes de Centros se mediría por contrato (SIAFLCT y SIACONA)

## Contexto
En Centros Empresariales hay dos tipos de docente (C54, C56):
- **especialista (`ES`):** a tiempo completo, con **48 horas**. También matricula (C46) y tiene **otras funciones administrativas**;
- **facilitador (`FC`):** a tiempo parcial, de **14 a 23 horas**, según su carga.

Pregrado queda fuera porque está en otros periodos (C55). Las reglas de carga y el factor FTE de SIATERM son **por periodo**, así que en los periodos de Centros solo cuentan los NRC de Centros.

Banner ofrece dos formas de medir la carga, que el instructivo no hace excluyentes (R19):
- **por regla de carga:** el tipo de asignación (docente, investigador…), en SIAFLRT, y se ve en SIAASGN;
- **por contrato:** tiempo completo o parcial, en SIAFLCT, y se ve en SIACONA.

## Decisión (propuesta)
En los periodos de Centros, la carga se mide **por contrato**:

| Contrato | Regla en SIAFLCT | Qué cuenta |
|---|---|---|
| `ES` especialista | «Total de carga de trabajo» de **48 a 48** | Sus NRC (carga educativa) + sus funciones administrativas (labor no educativa) |
| `FC` facilitador | **14 a 23 horas** (por confirmar si son «Horas de contacto semanal», U28-b) | Sus NRC |

- **Labor no educativa:** las funciones administrativas del especialista, como la matrícula, se registran en SIAASGN con los tipos de STVNIST que defina la USS (U28-c).
- **SIATERM:** el factor FTE de cada periodo de Centros va en **48**, para que un especialista sea 1 FTE (E20).
- **SIAASGN:** cada NRC lleva el contrato del docente en «Tipo de contrato».
- **SIACONA:** muestra si cada docente está debajo (U) o encima (O) de su contrato. Por ejemplo, un facilitador con 10 horas sale U.

## Alternativas descartadas
- **Solo por regla de carga (SIAFLRT), con una regla `ES` y otra `FC`:**
  - funcionaría;
  - pero el instructivo usa la regla para el *tipo de asignación* y el contrato para *tiempo completo o parcial* (5.2, diap. 7);
  - mezclarlos haría que la regla deje de servir para lo suyo.
- **Configurar las 40 horas de Pregrado junto a las de Centros:** Pregrado está en otros periodos y fuera del alcance (C55).

## Consecuencias
- Hay que crear o verificar:
  - en STVFCNT, los tipos de contrato `ES` y `FC` (no aparecen en la lista de PROD del 18/07, U28-a);
  - en STVCNTR, sus reglas;
  - en STVNIST, los tipos de labor no educativa.
- Luego se configuran SIAINST, SIAFLCT y SIAFCTR, y en SIAASGN se elige el contrato de cada NRC.
- Con esto se pueden probar las partes pendientes del script 5.2: labor no educativa y SIACONA.

## Criterio de salida
- Que la USS acepte medir por contrato (U28-d) y confirme las tablas y las horas (U28-a y b).
- Que Ellucian responda E20.
- Con eso, este ADR pasa a `aceptado`.

## Relacionado
- [ADR-011](ADR-011-carga-lectiva.md) · [ADR-010](ADR-010-usuarios-y-poblacion.md) · instructivo 5.2 Carga de trabajo docente
