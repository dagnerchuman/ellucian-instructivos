# Guía: crear un NRC desde cero (lo que se hizo en TEST el 28/09/2026)

El usuario creó su primer NRC en **TEST** (`experience-test.elluciancloud.com/ussipantest`, SSASECT 9.3.43) guiado paso a paso con capturas. Instructivo principal: **5.3 «Registrar la oferta horaria de los cursos»** (capacidad 5). Docente y salón: **6.2.1** (capacidad 6).

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
   - **GUARDAR:** «ADD» pasa a ser el número de NRC (diap. 26).
3. **Pestaña «Información de ingreso de sección»:** cupo máximo (diap. 27). Si hay lugares reservados, primero va la regla «nula» y luego las demás (diap. 28).
4. **Pestaña «Instructor y horas de reunión»:**
   - Fechas de reunión (diap. 29): tipo CLAS, hora de inicio y fin en 24 h, días, sesión 01.
   - Créditos y ubicación (diap. 30): horas por semana automáticas; edificio y salón (6.2.1 Espacios físicos, diap. 16 a 18).
   - Instructor (6.2.1, diap. 11 a 19): ID o SIAFAVL, casilla Principal, % de responsabilidad; si hay cruce, indicador de sobrepaso. Requisitos: el docente activo en SIAINST para el periodo y el NRC con al menos un bloque de horario guardado.
5. **Al final (menú relacionado):** SSADETL, SSAPREQ (prerrequisitos heredados), SSARRES. Verificar o buscar el NRC en **SSASECQ** (ver [guia-buscar-nrc.md](guia-buscar-nrc.md)).

## Datos reales vistos en TEST (capturas del 28/09 y 29/09)
- **Catálogo:** **ESEC 00650 «Ofimática Word 365»**. ESEC = «ESTUDIOS ESPECÍFICOS», escuela **EM**, vigente de 000000 a 999999. Existe también **ESEP 00650**, escuela **CE**. No se sabe qué son EM y CE (duda U18).
- **SMAAREA:**
  - Área **MC38-01 «Ciclo I»**, periodo 202454, nivel del alumno **C**, catálogo 2024.
  - Regla **ECOM-01 «Computación I»**, número de condiciones requerido **1**: la cumple **uno** de los cursos **ESEC 00650 a 00657**.
  - Computación no es un área aparte: es una regla dentro del área del ciclo.
- **SSASECQ (29/09):** En el periodo **202656**, parte de periodo **X07** (Computación), el NRC creado por el usuario corresponde exactamente al **1021** (**ESEC 00650**, sección **B**, cupo máximo 2). También figuran los NRCs 1015, 1016 y 1017. Para Idiomas (**I08**) figuran **1007**, **1008**, **1009**, **1010**, **1013** y **1014** (materia ESEP).
