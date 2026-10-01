# Migración R2 y su validación (aplicada a Centros Empresariales)

**Fuentes:**
- Presentación de Ellucian en Zoom (diapositivas 3 a 12), que el usuario mandó en fotos el 25/09/2026.
- Entregables:
  - «VALIDACIÓN DE LA MIGRACIÓN» (PDF y PPTX);
  - «PLANILLA DE REVISIÓN - MIGRACIÓN R2» (Excel);
  - «CAPP EXPLICADO»;
  - «MIGRACIÓN R2 - LO QUE ENTIENDO».

## Qué es
Ellucian y la USS cargan los datos de SEUSS en Banner por etapas:
- Primero en **PROD**: personas y docentes.
- Luego se clona a **TEST**: estudiantes, historia académica, egresados, saldos, tesis y escuela de procedencia.

Después de cada carga, la USS **revisa directamente en Banner Student** una muestra, registra cada error en un **Issue log** y consolida todo en una planilla Excel. La migración se acepta si el **% de correctitud** supera los umbrales y el **comité** aprueba las excepciones.

## Cuatro principios de validación
1. **Contra el legado** (¿están todos?): los totales cuadran con SEUSS. Se determina el total esperado, se obtiene el total en Banner, se compara y se explica la diferencia.
2. **Población representativa** (¿con quiénes probamos?): la muestra cubre centros, programas, niveles, grupos y estados.
3. **Funcional** (¿funciona en Banner?): el dato se consulta y lo usan los procesos (inscripción, carga, cobro).
4. **Por escenarios** (¿qué puede fallar?): estudiantes e historia evaluados con CAPP y proyección, más los casos de riesgo de los centros.

## Criterios y umbrales mínimos
| Criterio | Qué mide | Mínimo |
|---|---|---|
| Integridad | Campos obligatorios completos | 99% |
| Exactitud | Igual al origen | 98% |
| Consistencia | Coherente entre módulos | 98% |
| Validez | Formatos y códigos válidos (periodos 2026x, partes I/X/P) | 99% |
| Unicidad | Sin duplicados (un solo ID por persona) | 99,5% |
| Integridad referencial | Relaciones y totales cuadran | 99% |

**% de correctitud** = datos conformes ÷ datos revisados. Un dato «Observado» cuenta como correcto solo si el comité aprueba la excepción. Con 48 participantes, Unicidad exige **cero duplicados**.

## Tiempo de revisión
- **Por estudiante:** 86 min; en Centros Empresariales, **83 min**, porque no hay tesis.
- **Historia académica:** 42 min por estudiante, contando CAPP y proyección. Es el punto crítico: unas 34 horas en 3 días, con al menos 2 revisores.
- **Muestra propuesta:** 16 participantes por centro, 48 en total (**por confirmar**).

## Cronograma 2026 (carga y revisión por la USS)
| Etapa | Ambiente | Carga | Revisión USS |
|---|---|---|---|
| Personas | PROD | 07–21/09 | 24–27/09 |
| Documento de identidad, Contacto de emergencia | PROD | 22–25/09 | 25–27/09 |
| Docentes | PROD | 28–30/09 | 30/09–02/10 |
| Carga LD01 con equivalencias, Matriz de seguridad | PROD | 30/09–02/10 | — |
| Clonación a TEST | — | 05–09/10 | — |
| Estudiantes | TEST | 12–16/10 | 16–21/10 |
| Historia académica (CAPP y proyección) | TEST | 19–28/10 | 28–30/10 |
| Egresados | TEST | 29/10–02/11 | 02–04/11 |
| Saldos | TEST | 03–06/11 | 06–13/11 |
| Tesis (no aplica a los centros) | TEST | 09–10/11 | 10–13/11 |
| Escuela de procedencia | TEST | 11–13/11 | 13–16/11 |
| Pruebas integrales (USS) | TEST | — | 16/11–26/12 |

## Escenarios de riesgo propios de los centros
- Un curso llevado en SEUSS que queda en un periodo equivocado, duplicado o que se pierde (SHACRSE, SHATCKN).
- Nivel aprobado que no se reconoce como prerrequisito, por ejemplo BASIC I para BASIC II (SFAPROJ, SSAPREQ, SFAREGS).
- Estudiante de pregrado que lleva Idiomas: los dos programas deben quedar activos en SGASTDN.
- Grupo que empezó en SEUSS y no aparece en Banner (SSASECT, SFAREGS).
- Participante retirado que aparece activo; participante con deuda sin retención (SGASTDN, TSAAREV, SOAHOLD).
- La misma persona como alumno, participante y docente con dos ID (GOAMTCH, SPAIDEN, SIAINST).

## Qué le toca a la USS
- Definir los datos a revisar por plantilla.
- Llenar la planilla: una fila por dato revisado.
- Registrar los errores en el Issue log con captura de pantalla.
- Respetar los plazos.
- Calcular el % de correctitud por criterio, plantilla y centro para el comité.
