# Prueba de carga por contrato (ADR-020, propuesto)

Parte de la skill `workflow-pruebas-test` (el mapa está en su `SKILL.md`).

## 5. Prueba de carga por contrato (ADR-020, propuesto)
Cubre lo que falta del script 5.2: la labor no educativa y SIACONA. Sirve también para decidir si se mide por contrato o por regla de carga (U28-d).
1. **Tablas:**
   - en STVFCNT ya están `ES` y `FC` (C57);
   - en STVCNTR crea un código de regla para cada uno (6 caracteres; por ejemplo `ESP48` y `FAC23`, **de ejemplo**);
   - en STVNIST crea los tipos de labor no educativa (4 caracteres; por ejemplo `MATR` matrícula, `COOR` coordinación y `ATEN` atención a estudiantes, **de ejemplo**).
2. **SIATERM:** en el periodo de Centros (por ejemplo 202656), el factor FTE en 48.
3. **SIAFLCT (cómo llenarlo; instructivo 5.2 Carga de trabajo, diap. 29 a 32):**
   - **Antes:** el código de regla debe existir en STVCNTR, o SIAFLCT no lo acepta.
   - **Bloque llave:**
     - Periodo `202656`;
     - «Copiar «De periodo»» **vacío**: en SFAROVR, poner algo ahí dio error (C42);
     - Tipo de contrato `ES`;
     - **Ir**.
   - **Bloque «Reglas de periodo de contrato de docente»:** marca **Activo** y en **Código de regla de contrato** pon `ESP48`.
   - **Rangos:** solo **«Total de carga de trabajo»**, con Inferior 48 y Superior 48. Lo demás queda vacío; en el ejemplo del instructivo, el rango FTE va vacío. **GUARDAR.**
   - **Facilitador:**
     - vuelve al bloque llave con ⟲ y pon el tipo de contrato `FC`;
     - Activo y regla `FAC23`;
     - solo **«Horas de contacto semanal»**, con Inferior 14 y Superior 23. **GUARDAR.**
   - **Si Banner exige los demás rangos,** pon 0 en Inferior y el tope (48 o 23) en Superior.
   - **Siguiente pantalla:** **SIAFCTR**, para indicar qué periodos cuenta cada contrato (diap. 33 y 34).
4. **SIAINST:** al docente `100582059`, en el bloque «Contrato de docente», el contrato `ES` con su regla y la marca de predefinido.
5. **SIAASGN:**
   - en cada NRC, «Tipo de contrato» `ES`;
   - en la labor no educativa, una fila por función (`MATR`, `COOR`, `ATEN`), con su «Carga de trabajo» y su «Contacto semanal».
6. **SIACONA:** con contrato `ES`, el periodo y el docente:
   - ¿queda debajo (U), dentro o encima (O) de las 48 horas?
   - ¿la carga educativa que viene del catálogo cuadra con las horas por semana?
7. **Para comparar:** en SIAASGN mira también el análisis por regla de carga (SIAFLRT). Con las dos pantallas a la vista se decide cuál es más clara para el jefe, que revisa la carga y da el visto bueno (ADR-011).
