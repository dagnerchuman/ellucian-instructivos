# Centro de Idiomas · Guía de pruebas en TEST

Elaborado por: Dagner Anibal Chuman Lluen · preparado el 05/10/2026

Las pruebas se hacen en **Banner TEST** con tu usuario (`100582059`); Claude no puede entrar a Banner. Esta guía las ordena para que, en una sola corrida, se cierren **los 20 scripts de Idiomas**. Se reutilizan los mismos NRC (Número de Referencia de Curso) y los mismos alumnos.

**Cómo usarla:** ve bloque por bloque. En cada ✅ mándame una captura con el mensaje de Banner y yo lo anoto en `datos.json`, en el registro y en los diagramas.

| Bloque | Qué haces | Scripts que cierra | Tiempo |
|---|---|---|---|
| 0 | Descubrir los códigos de Idiomas | ninguno, pero desbloquea todo (U25) | 15 min |
| 1 | Programar 5 NRC (uno es el club de conversación, con liga) | 11, 17, 18-A y la liga | 35 min |
| 2 | Crear 4 alumnos y admitirlos | 06, 07 (también el 07 de Computación) | 30 min |
| 3 | Matricular | 01 con la liga, 02, 04, 09, 15, 16, 18-B | 35 min |
| 4 | Notas y pase a historia | 08, 10, 12, 13, 14 | 20 min |
| 5 | Convalidación, egresados y solicitud | 03, 05, 18-C | 20 min |

**Inglés lleva liga:** cada curso tiene un **NRC teórico** y un **NRC de club de conversación**, que el alumno matricula juntos (C52, R18, ADR-019). Aquí se prueba con BASIC I (NRC A y su club); en la realidad, todos los cursos de Inglés lo llevan.

**Lo que ya existe y ayuda:**
- El periodo 202656 (II) y el 202751 (verano 2027) con la parte I01 (C45).
- La regla de sobrepaso `CAPACIDAD` en SFAROVR (permisos de sobrepaso de inscripción) para 202656 (C42).
- Tu docente `100582059`, ya activo.
- `S00581091`, que ya tiene Pregrado y Computación.

---

## Bloque 0 · Descubrir los códigos de Idiomas (U25)

Todavía no se sabe con qué códigos está Idiomas en TEST. Sin esto no se puede seguir.

- [ ] **SCACRSE (catálogo de cursos):** busca **BASIC I** y **BASIC II** por título. Anota:
  - la **materia y el número** de cada uno, y su **modo de calificación**;
  - en **«Tipo de horario»**, si BASIC I tiene **dos** tipos: Teoría (`TEO`) y el del club, por ejemplo Práctica (`PRA`). Sin dos tipos no se puede hacer la liga (U27).
- [ ] **SCAPREQ (prerrequisitos y puntajes de examen del catálogo)** de BASIC II: ¿pide BASIC I? ¿Tiene un **código de examen** con puntaje? *(instructivo 1.1.5, diap. 17 y 18)*
- [ ] **SOATERM (Control de periodo)** de 202656:
  - ¿existen las partes **I10** (05/10 – 29/11) e **I11** (02/11 – 27/12)? Si no, usa las partes I que existan y avísame;
  - en «Verificación de errores de inscripción», ¿**Prerrequisitos** y **Ligas** están en **Fatal**? *(5.4, diap. 14 y 15)*
- [ ] **SHAGRDE (códigos de calificación)** del **nivel I:**
  - ¿qué modos tiene?
  - ¿con qué nota aprueba?
  - Debe tener el mismo modo que el curso. Si no, el pase a historia falla, como pasó en Computación (U20).
- [ ] **STVTESC (códigos de examen):** ¿hay un examen de **suficiencia de inglés**? Anota su código.
- [ ] **Programa de Idiomas:** en SAAQUIK (admisión rápida), abre la lista del campo Programa y busca el de nivel **I**. Anota el código.

**Mándame:** los códigos, o una captura de cada pantalla.

**Si BASIC I o BASIC II no existen en SCACRSE, detente:** el catálogo de Idiomas no está cargado en TEST. Es un hallazgo para Registros Académicos y casi todo lo demás queda bloqueado.

---

## Bloque 1 · Programar los NRC (scripts 11, 17 y 18-A)

En SSASECT (Programar NRC) crea estos cinco NRC. Son de prueba: los horarios y cupos son **de ejemplo**.

| NRC | Curso | Periodo y parte | Cupo | Horario | Para qué |
|---|---|---|---|---|---|
| **A** | BASIC I · teórico | 202656 · I10 | **1** | lunes y miércoles 08:00–12:00 | Matrícula, cupo (15) y cruce (17) |
| **A-C** | BASIC I · club de conversación | 202656 · I10 | 5 | viernes 08:00–10:00 | Liga con A |
| **B** | BASIC I | 202656 · I10 | 5 | martes y jueves 08:00–12:00 | Traslado (16) |
| **C** | BASIC II | 202656 · I11 | 5 | martes y jueves 14:00–18:00 | Prerrequisito y suficiencia (04, 10) |
| **D** | BASIC I | 202751 · I01 | 5 | sin horario | Apertura de periodo (11) |

- [ ] **Docente:** `100582059`, principal al 100 %, en A, A-C, B y C.
- [ ] **Liga entre A y A-C** *(instructivo 5.3_4.1.4.1.9 Crear Ligas, diap. 12 a 18)*:
  - En **SSASECT**, pestaña «Información de sección de curso», bloque «Indicadores de clase»:
    - NRC A: **«Identificador de liga» `TE`**, con «Calificable» marcado;
    - NRC A-C: tipo de horario del club, **«Identificador de liga»** con 2 letras de ese tipo (por ejemplo `PR` si es Práctica), **0 horas crédito**, «Calificable» **sin** marcar y «Dispensa de colegiatura y cuotas» **marcada**.
  - En **SSADETL (detalle del NRC)**, pestaña «Correquisitos y ligas de sección», campo **«Conector de liga»**:
    - en el NRC A, la liga del club;
    - en el NRC A-C, `TE`.
- [ ] **Script 17 ✅:** el NRC **A** tiene el mismo horario que el **1026** de Computación. Al asignar al docente, Banner dirá «Conflicto de horario del instructor». Acepta el sobrepaso con **OK**.
- [ ] **Script 11 ✅:** el NRC **D** queda creado en 202751, parte I01.
- [ ] **Script 18-A ✅:** en SIAASGN (asignación de docente, su carga), con `100582059` y 202656, aparecen A, A-C, B y C con sus horas.

**Recuerda (lo aprendido en Computación):**
- campus `S`, estatus `A` y tipo de horario son obligatorios;
- guarda en cada pestaña;
- para pasar al bloque del docente usa **«Sección siguiente» (⤓)**;
- no pongas reservas de cupo: así solo cuenta el cupo general.

**Mándame:** el número de cada NRC (A, A-C, B, C y D), la captura de SSADETL con la liga y la de SIAASGN.

---

## Bloque 2 · Alumnos y admisión (scripts 06 y 07)

- [ ] En **GOAMTCH (búsqueda de personas para evitar duplicados)**, crea 4 personas con origen `PERS_NATU`. Los nombres son **de ejemplo**; cada una necesita dirección `PP`, teléfono `MOV` y correo `PER1` (C17, C32).

| Alumno | Nombre de ejemplo | Su papel en la prueba |
|---|---|---|
| **I-1** | IDIOMAS PRUEBA UNO | Aprueba BASIC I y pasa a BASIC II |
| **I-2** | IDIOMAS PRUEBA DOS | Cupo lleno, traslado y desaprueba |
| **I-3** | IDIOMAS PRUEBA TRES | Suspensión y examen de suficiencia |
| **I-4** | IDIOMAS PRUEBA CUATRO | Convalidación |

- [ ] **SAAQUIK:** admite a I-1, I-2, I-3 e I-4 en el **programa de Idiomas** (del bloque 0), periodo 202656, nivel `I`. Anota lo que Banner completa solo: mayor, departamento y estatus (U25).
- [ ] **Scripts 06 y 07 ✅:** admite también a **`S00581091`** en el programa de Idiomas. En SGASTDN (registro del estudiante) debe tener **tres programas**: Pregrado, Computación e Idiomas.
  - Con esto se cierra el **Script 07** de Idiomas **y el de Computación**, que estaba pendiente.
  - También queda el **06** de Idiomas: Pregrado + Idiomas.

**Mándame:** los IDs `S00…` de I-1 a I-4, y la captura de SGASTDN de `S00581091` con sus tres programas.

---

## Bloque 3 · Matrícula (scripts 01, 15, 18-B, 02, 16, 09 y 04)

Todo se hace en **SFAREGS (matrícula del alumno)**: plan `1`, estatus `EL`, guardar, ⤓ y luego el NRC con `RE`.

1. [ ] **Script 01 y liga ✅:** matricula a **I-1**:
   - primero **solo en A**. Si «Ligas» está en Fatal, Banner debe dar un **error de liga**;
   - después en **A y A-C** juntos: debe pasar. A queda lleno (cupo 1).
   - Si sale «Duplicate Course» al agregar A-C, mándame la captura. Sería un hallazgo, porque la liga existe justamente para llevar dos NRC del mismo curso.
   - **Desde aquí,** cada alumno que entre a A también va a A-C.
2. [ ] **Script 15 ✅:** intenta matricular a **I-2** en **A**:
   - sale «Closed»;
   - en SSASECT sube el cupo de A a **2**;
   - matricula a I-2 en A y A-C.
3. [ ] **Script 18-B ✅:** intenta matricular a **`S00581091`** en **A**. Debe salir «La persona tiene retenciones», por su retención TT.
4. [ ] **Libera la retención:** en SOAHOLD (retenciones) ponle **fecha de fin = hoy**. No se borra (R16).
5. [ ] **Script 02 ✅:** A está lleno (2/2). Matricula igual a `S00581091`:
   - en SFASRPO (sobrepasos del alumno) dale `CAPACIDAD` para el NRC A;
   - matricula en SFAREGS en A y A-C, sin error de cupo, como en Computación (C43). En «Plan de estudios de ingreso» elige su plan de **Idiomas**, porque tiene tres.
6. [ ] **Script 16 ✅:** traslada a **I-2** del NRC **A** al **B**:
   - primero `DD` en A y en A-C;
   - después `RE` en B, que no tiene club.
   Si lo haces al revés, Banner dice «Duplicate Course».
7. [ ] **Script 09 ✅** con **I-3:**
   - en SGASTDN cambia su estatus a `IS`;
   - en SFAREGS sale «El estatus del alumno impide la inscripción»;
   - vuelve a `AS`.
8. [ ] **Script 04 ✅** con **I-3:**
   - intenta matricularlo **directo en BASIC II** (NRC **C**). Debe salir el **error Fatal de prerrequisito**;
   - en **SOATEST (puntajes de examen del estudiante)** registra el examen de suficiencia: código del bloque 0 y un puntaje **de ejemplo** que alcance el mínimo de SCAPREQ;
   - reintenta en C: ahora debe matricularse.

> **Si en el paso 8 no sale ningún error:**
> - si SCAPREQ no tiene prerrequisito, el prerrequisito de BASIC II no está configurado;
> - si SOATERM no está en Fatal, la verificación no está activa.
>
> Mándame la captura igual: es un hallazgo para Registros Académicos (R09).

---

## Bloque 4 · Notas y pase a historia (scripts 13, 12, 14, 10 y 08)

1. [ ] **Script 13 ✅:** en **SFASLST (notas por backoffice)**:
   - en el NRC **A**, pon nota aprobatoria a **I-1** (por ejemplo 16) y a `S00581091`;
   - en el NRC **B**, pon a **I-2** una nota que **no apruebe** (por ejemplo 08).
   Usa la escala del nivel I del bloque 0. El club (A-C) no lleva nota, porque no es calificable.
2. [ ] **Scripts 12 y 14 ✅:** en **GJAPCTL (ejecutar procesos)** corre **SHRROLL (paso de notas a la historia académica)** para 202656, NRC A y B.
   - Si sale «No Substitute Grade Found», a la escala del nivel I le falta el modo del curso. Agrégalo en SHAGRDE, como en Computación (U20).
3. [ ] **Prerrequisito cumplido:** matricula a **I-1** en BASIC II (NRC **C**). Debe pasar, porque BASIC I ya está aprobado en su historia.
4. [ ] **Script 10 ✅:** intenta matricular a **I-2** en BASIC II (NRC **C**). Debe salir el **error Fatal de prerrequisito**, porque desaprobó BASIC I (ADR-008).
5. [ ] **Script 08 ✅:**
   - retira a **I-1** de C con `DD`;
   - en SSASECQ (consulta de NRC) el cupo restante de C sube en 1.

---

## Bloque 5 · Convalidación, egresados y solicitud (scripts 03, 05 y 18-C)

- [ ] **Script 03 ✅** con **I-4:** registra un certificado de inglés de otra institución. El nombre, el curso y la nota son **de ejemplo**:
  - en SHATRNS (institución de transferencia), la institución;
  - en SHATFAC (cursos de transferencia), el curso externo con su nota y su equivalencia a **BASIC I**.
  - Prueba extra: matricula a I-4 en BASIC II (NRC C). ¿Banner toma la convalidación como prerrequisito? *(capacidad 3.3; en Computación se hizo con el curso externo IST150, Script 03)*
- [ ] **Script 05 (egresados), solo si ya tienes la respuesta a U24:**
  - la nota sale de la plataforma, fuera de Banner;
  - en SSASECT se crea **un solo NRC**;
  - la nota se pasa a mano (ADR-012).
  - Antes falta saber en qué página se pasa la nota a cada BASIC.
- [ ] **Script 18-C:** el mecanismo ya se validó con Computación (`CER` en el Autoservicio, atendido en SVASVPR, administración de solicitudes de servicio). Dos opciones:
  - repetirlo con un alumno de Idiomas;
  - decirme que lo dé por validado con esa prueba. **Tú decides.**

---

## Al terminar

Mándame las capturas y yo:
- anoto en `centros/idiomas/datos.json`:
  - los códigos del bloque 0 (programa, materia, mayor, departamento, escala);
  - los NRC A, A-C, B, C y D y los alumnos I-1 a I-4;
  - cómo quedó la liga (identificadores y si Banner bloquea el teórico sin club);
  - la evidencia y el estado de cada script;
- registro lo confirmado (C##) y cierro U25;
- marco el Script 07 de Computación;
- regenero los diagramas y valido la base (`herramientas/validar_conocimiento.py`).
