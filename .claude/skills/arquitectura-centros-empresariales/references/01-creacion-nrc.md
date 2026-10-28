# Guía: crear un NRC desde cero (lo que se hizo en TEST el 28/09/2026)

El usuario creó su primer NRC en **TEST** (`experience-test.elluciancloud.com/ussipantest`, SSASECT 9.3.43) guiado paso a paso con capturas. Instructivo principal: **5.3 «Registrar la oferta horaria de los cursos»** (capacidad 5). Docente y salón: **6.2.1** (capacidad 6).

> **Orden de Banner:** sigue los pasos y el orden de campos descritos para cada pantalla. No adelantes campos ni cambies la secuencia; si un orden no está documentado, confírmalo antes de indicarlo.

## El NRC no es lo primero: orden
0. **Códigos base:** STVPTRM (partes de periodo), STVACYR, STVTRMT. *(1.1.1)*
1. **Periodo:** STVTERM y SOATERM, con fechas, partes de periodo habilitadas para programar (5.3, diap. 16), número inicial de NRC (5.3, diap. 15) y fechas web. Feriados en SSAEXCL.
2. **Catálogo:** curso en SCACRSE (1.1.4) y prerrequisitos en SCAPREQ (1.1.5). Sin el curso no hay NRC (5.3, diap. 53).
3. **Programa y malla:** SOACURR y SMAPROG/SMAAREA. No bloquean el NRC, pero sí la admisión y el CAPP.
4. **Docente:** SPAIDEN, SIAINST (activo en el periodo) y el factor de SIATERM.
5. **NRC:** SSASECT.

## Qué periodo poner
Se decide por la **fecha de inicio del grupo**:

| Grupos que empiezan… | Periodo |
|---|---|
| enero a marzo 2026 | 202651 |
| abril a julio 2026 | 202654 |
| agosto a diciembre 2026 | 202656 |
| enero a marzo 2027 | 202751 |

En TEST existe **202656** (el usuario lo usó).

## SSASECT campo por campo (5.3, diap. 19 a 32)
1. **Encabezado:** Periodo (con «•••» se ve la lista) · NRC vacío · botón **«Crear NRC»**. El NRC queda en «ADD» hasta guardar. «Copiar NRC» duplica uno que ya existe.
2. **Pestaña «Información de sección de curso»:**
   - **Materia / Número de curso:** en «•••», la opción «cursos existentes» abre el catálogo; la opción «horas crédito» busca por créditos.
   - Sección: letra (A, B…) no repetida. Con «•••» se abre SSASECQ, que sirve para ver las secciones que ya existen.
   - **Campus:** el de dictado. En la lista, elige por la descripción; los códigos de la USS no están confirmados.
   - **Estatus:** Activo.
   - **Tipo de horario:** del catálogo (Teoría). El método educativo se llena solo.
   - **Modo de calificar:** obligatorio.
   - **Sesión:** jornada.
   - Aprobación especial, duración, socio de integración y lista cruzada: vacíos, salvo que se usen.
   - **Clase tradicional › Parte de periodo:** el grupo del mes (Informática en 202656: X05, X06, **X07**). Las fechas se llenan solas. «Clase de aprendizaje abierto» va vacía.
   - **Horas crédito** (5.3, diap. 23 a 25):
     - Vienen del catálogo; no se inventan. Con créditos fijos se dejan igual; solo se cambian si el curso tiene créditos variables en SCACRSE.
     - Se revisan también las **horas de cobro**.
     - Con tipo **Teoría**: casilla **Calificable** marcada, horas de cobro incluidas y **sin** marcar «Dispensa de colegiatura y cuotas».
     - Las horas crédito **no son** las horas por semana: esas se calculan después con el horario y el factor de SIATERM.
    - **GUARDAR:** «ADD» pasa a ser el número de NRC (diap. 26). **Crítico:** No intentar cambiar de pestaña antes de presionar Guardar, o Banner bloqueará con `*ERROR* Debe guardar antes de salir de la información de sección`. Aprobación especial debe quedar vacía.
3. **Pestaña «Información de ingreso de sección»:** en «Detalles de ingreso», escribir el cupo total en **Proyectado** (por ejemplo, 40; diap. 27). Es obligatorio: hay que llenarlo **antes** de ir a «Lugares reservados» (C97). «Fecha de congelamiento» del censo uno también es obligatoria; en el NRC 10044 Banner la llenó con 14-SEP-2026. En «Lugares reservados», conservar la regla «nula» y pulsar `+` para agregar una fila por cada criterio; allí se escribe el **Máximo reservado** (por ejemplo, 40; diap. 28). Guardar. La reserva se configura en **SSASECT**, no en SSARRES.
4. **Pestaña «Instructor y horas de reunión»:**
   - Fechas de reunión (diap. 29): tipo CLAS, hora de inicio y fin en 24 h, días, sesión 01.
   - Créditos y ubicación (diap. 30): horas por semana automáticas; edificio y salón oficial virtual de campus S: **`SAUVIR`** y **`SALA VIRT.`**. Con el aula virtual **siempre** hay que poner la letra `O` en `Indicador de sobrepaso` de la grilla HORARIO: todos los NRC comparten `SAUVIR` / `SALA-VIRT` y, sin la `O`, Banner da `*ERROR* Conflicto de salón` (C97). Pasa lo mismo con un salón físico que tenga cruce.
   - Instructor (6.2.1, diap. 11 a 19): ID o SIAFAVL, casilla Principal, % de responsabilidad (100%) y sesión (100%). **Regla de oro:** El `Indicador de sesión` de HORARIO debe coincidir idénticamente con el de INSTRUCTOR (ambos `01` o ambos `1`), de lo contrario arroja `*ERROR* Sesión no tiene horas de reunión definidas`. Si el docente tiene cruce, marcar la casilla `Indicador de sobrepaso` de la grilla de instructor.
   - Presionar Guardar (3er guardado).
5. **Al final (menú relacionado):** SSADETL, SSAPREQ (prerrequisitos heredados) y SSARRES. **SSARRES no reserva cupos:** sirve para incluir o excluir quién puede matricularse en el NRC mediante restricciones. Verificar o buscar el NRC en **SSASECQ** (ver [ref-busqueda-nrc.md](ref-busqueda-nrc.md)).

## Datos reales vistos en TEST (capturas del 28/09, 29/09, 02/10 y 23/10/2026)
- **NRC 10045 (28/10, prueba de restricciones, C151):** `ESEC 00701` «Google», 202656, sección A, campus S, estatus A, TEO, VIRT, socio de integración OPLMS, modo V, sesión T «Tarde», parte X07 (02-NOV a 13-DIC-2026, 6 semanas); horas crédito 1 (curso variable 0 «O» 1), cobro 1, teoría 1, laboratorio 1; Máximo y Proyectado 10, censo uno con fecha de congelamiento 09-NOV-2026; Lugares reservados: regla general 10. Sin horario ni docente.
- **NRC 10044 (23/10):** `ESEC 00684` «Diseño Web», periodo 202656, sección A, campus S, estatus A, tipo de horario TEO, método educativo VIRT (socio de integración OPLMS), modo V «Vigesimal Estándar», sesión M «Mañana», parte X06 (07-SEP a 31-OCT-2026, 8 semanas). Horas crédito 1, horas de cobro 1, contacto 2 (teoría 1, laboratorio 1), Calificable marcado y sin dispensa. Máximo y proyectado 40. Aula SAUVIR / SALA-VIRT.
- **Catálogo:** **ESEC 00650 «Ofimática Word 365»**. ESEC = «ESTUDIOS ESPECÍFICOS», escuela **EM**, vigente de 000000 a 999999. Existe también **ESEP 00650**, escuela **CE**. No se sabe qué son EM y CE (duda U18).
- **SMAAREA:**
  - Área **MC38-01 «Ciclo I»**, periodo 202454, nivel del alumno **C**, catálogo 2024.
  - Regla **ECOM-01 «Computación I»**, número de condiciones requerido **1**: la cumple **uno** de los cursos **ESEC 00650 a 00657**.
  - Computación no es un área aparte: es una regla dentro del área del ciclo.
- **SSASECQ (29/09 y 02/10):** 
  - NRC **1021** (28/09): `ESEC 00650`, sección `B`, periodo `202656`, parte `X07`, aforo 2/2, docente Dagner Chuman (`100582059`).
  - NRC **1026** (02/10): `ESEC 00650`, sección `D`, periodo `202656`, parte `X07`, aforo 1, horario Lunes/Miércoles 08:00 a 12:00, aula virtual `SAUVIR` / `SALA VIRT.` (9,6 h/sem calculadas), docente Dagner Chuman (`100582059`, 100% resp). Creado para casuísticas CCEE.
