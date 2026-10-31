# Cómo manejar Banner TEST con el navegador (para cualquier agente)

Método con el que se hicieron las pruebas del 28 y 29/10/2026 (C153 a C167) en `experience-test.elluciancloud.com/ussipantest`. Sirve igual para Claude (navegador integrado) y para Antigravity (su navegador): las acciones son las mismas, clic, escribir, tecla, captura y zoom. Si una pantalla no se comporta como aquí, se toma una captura y se dice lo que se ve, sin suponer.

## 1. Reglas de trabajo con el usuario
1. **El agente deja escrito, el usuario guarda.** El agente abre la página, llena los campos y se detiene. Escribe: «Dagner, haz esto: pulsa GUARDAR» y lo que debe salir. El usuario guarda y responde «Ya guardé» o «Salió error». No se cierra el navegador entre pasos (C165).
2. **Nunca guardar sin permiso.** El usuario lo pidió desde la primera prueba («pregúntame ¿prosigo? antes de cada guardado»). En SCAPPRQ, además, el control de permisos le bloquea el guardado a Claude (C164).
3. **Después de cada «Ya guardé», captura.** Se lee el aviso de arriba a la derecha: verde *Saved successfully (n rows saved)* o *Los alumnos ya están inscritos*; rojo *\*ERROR\**. Se le dice al usuario si guardó o no y por qué.
4. **Se anota en el registro** lo que pasó (C##) con el mensaje exacto de Banner; las filas temporales se apuntan para borrarlas al final.

## 2. Por qué sale rápido
- **Encadenar acciones** en un solo lote: clic → esperar 1 s → escribir → Tab → esperar 3 s → captura. Banner valida cada campo al salir de él: tras Tab o Ir, esperar 2 a 5 s antes de la captura.
- **Capturas pequeñas y zoom.** Para comprobar un campo basta un zoom de esa franja; no hace falta leer la página entera. El texto de Banner está dentro de un marco: «leer el texto de la página» devuelve casi nada, así que se lee con capturas.
- **Dejar que Banner llene.** En SFAREGS basta escribir el NRC y pulsar Tab: Banner trae materia, curso, sección, estatus RE, nivel, parte de periodo, método y campus, y salta solo al plan de estudios.
- **Tener a mano los datos de prueba** (sección 6), para no buscarlos cada vez.

## 3. Moverse en una página de Banner 9

| Acción | Cómo |
|---|---|
| Abrir una página | Lupa de arriba a la derecha › escribir el código (SFAREGS, SCAPPRQ…) › clic en el resultado. Con el enlace directo (`…/BannerAdmin?form=SFAREGS…`) a veces pide SOADEST (sección 5) |
| Llenar el bloque clave | En el orden de la pantalla (C86, C87): en SFAREGS, periodo → ID → plan. Clic en el campo siguiente para que valide y luego **Ir** (arriba a la derecha) |
| Campo que no toma lo escrito | Clic › esperar 1 s › Fin › retroceso varias veces › esperar › escribir › comprobar con zoom antes de seguir |
| Volver al bloque clave | El mismo botón de arriba a la derecha (flecha circular, «Comenzar de nuevo») |
| Pasar al bloque siguiente o anterior | Botones **⏬** y **⏫** de abajo a la izquierda. Un clic en una fila no siempre mueve el foco al bloque: usar ⏬ |
| Agregar una fila | Con el foco en el bloque, **+** de su encabezado: la fila nueva queda debajo de la actual |
| Borrar una fila | Seleccionarla › **–** de su encabezado: desaparece y el contador baja; se aplica al GUARDAR. Primero el detalle y luego el maestro, cada uno con su guardado (SCAPPRQ: el prerrequisito y después el curso, C167) |
| Ver columnas ocultas | Rueda horizontal sobre la tabla (Estatus, Parte de periodo, Plan, Mensaje) |
| Ver el error de una fila | Clic en la fila: debajo salen «Bandera de error», «Tipo de estatus» y «Mensaje». «Ver detalle de resultados» casi nunca dice más (C163, C166) |
| Lista de valores | **•••** del campo. Doble clic también la abre. **Intro** dentro de la lista elige la primera fila, aunque no sea la buscada (C164). **ANULAR** cierra sin elegir |
| Cerrar un aviso | Clic sobre el aviso |

Referencia en una ventana de 800 × 670 (comprobar siempre con captura): Ir y «Comenzar de nuevo» ≈ (767, 102); ⏬ ≈ (67, 657); ⏫ ≈ (21, 657); GUARDAR ≈ (760, 657); en SFAREGS, + del bloque «Información de curso» ≈ (695, 406).

## 4. Recetas probadas

### Matricular a un alumno en un NRC (SFAREGS)
1. SFAREGS › periodo › ID › Ir.
2. ⏬ dos veces hasta «Información de curso» › **+** › NRC › Tab › plan de estudios (el que tenga registro en «Plan de estudios de ingreso»; si no, sale *«No existe el registro del estatus del ingreso para este plan de estudios»*, C166) › Tab.
3. Si queda una fila vacía al final, se deja: no se guarda.
4. El usuario guarda. Correcto: *«Los alumnos ya están inscritos»*. Para comprobarlo, volver a abrir con Ir.
5. Error: *«El horario del alumno tiene errores»*; el motivo está en la columna Mensaje («Program Restriction», «Prerequisite and Test Score error», «Prerequisite In Progress»). Esa fila ya no se puede quitar: recargar la página y esperar el candado (sección 5).

### Dar de baja (SFAREGS)
- ⏬ hasta «Información de curso» (un clic en la tabla no siempre mueve el foco) › columna Estatus › DD › Tab › el usuario guarda: *«Estimación de cuota procesada»* y *«Los alumnos ya están inscritos»*. Probado con Arnold en el 10045, X06 (C189). Si sale *«El estatus “DD” es inválido…»*, la parte de periodo no tiene DD en SFARSTS. Con ••• en Estatus se abre SFQRSTS con los estatus permitidos (en 202744, parte 1, solo RE). Un RE no se borra (C158, C167).

### Agregar el programa del centro a un alumno (SFAREGS › Currículos)
- Fila nueva › programa desde **••• › «Reglas de currículo base por programa»** › fila del campus › OK; campo de estudio y departamento. Escribir el programa a mano y pulsar Intro arrastra datos de otro currículo (C153, C166).

### Leer o cambiar SCAPPRQ
- Programa + **periodo de la versión** (202444, 202644), no el de la matrícula (C164) › Ir › clic en el curso › ⏬ al bloque de prerrequisitos. Agregar: **+** › materia, curso, sin nivel ni calificación si basta haberlo cursado.

### Buscar un alumno con un curso en su historia (SHACRSE)
- SHACRSE › ID › **periodo vacío** › Ir: todos sus cursos con periodo, NRC, nota y modo. Así se encontró a `A00010005` con Basic I (C170). Solo consulta.

### Ver una malla (SMAPROG y SMAAREA, solo consulta)
- **SMAPROG** › programa (por ejemplo `CMEMC44`) › periodo (el de la prueba) › Ir: versión, modelo y totales. Sus áreas están en el bloque «Anexos de área de programa» (⏬ unas 8 veces).
- **SMAAREA** › área (por ejemplo `MC44-01`) › periodo › Ir › **⏫ una vez** desde el primer bloque lleva directo a «Anexo de curso/atributo de área» (las reglas). Con una regla seleccionada, botón **Regla**: el detalle muestra materia y curso de cada condición; **Regresar** vuelve. Si la tabla quedó corrida a la derecha, desplázala a la izquierda para ver Materia y curso (C172).
- Para cambiar de área: «Comenzar de nuevo» (arriba a la derecha) › borrar el área › escribir la nueva › Tab › Ir.
- **Agregar un curso a una regla** (C173): SMAAREA con el **periodo de la versión** (por ejemplo 202454, no el de la matrícula) › Anexo › regla › **Regla** › clic en una fila de Detalles › **+** de Detalles › Materia › Tab › curso › Tab › el usuario guarda. La columna «Condición» se numera sola al guardar.
- **Varios cursos en una regla** (C174): un **+** por cada curso; la fila nueva sale debajo de la última (cada fila, unos 18 px más abajo). Después de cada Tab, espera 2 s a que Banner valide el curso. Antes de pedir el guardado, revisa con zoom que estén todas las filas («Registro n de n»). Una regla por guardado.
- **Quitar un curso de una regla:** clic en la fila › **–** de Detalles (al lado del +) › el usuario guarda. Sin probar todavía: es lo que falta en `MC42-01` › `ECOM-04` (C174).
- **Comprobar:** después de guardar, «Comenzar de nuevo» › misma área y periodo de la versión › Ir › regla › Regla. Si el usuario recargó la página, hay que volver a entrar a SMAAREA. También sirve **Regresar** › la misma regla › **Regla** (C181).
- **El periodo se escribe a mano:** un doble o triple clic en el campo abre la lista «Códigos de periodos del catálogo», y su Intro elige la primera fila (999999). Clic › Fin › borrar › escribir (C181).

### Regla de asistencia de un NRC (SOAATRK, C182)
1. SOAATRK › periodo › Ir: salen las reglas del periodo (en 202656, la 2 del 10044 y la 3 del 10045).
2. Clic en una fila › **+** del bloque › parte (X06) › Tab › materia › Tab › curso › Tab › NRC › Tab, esperando 1 a 2 s después de cada Tab. «Desplegar clase» y «Control de asistencia a clases» vienen marcadas.
3. «Unidad de control» es una lista con búsqueda: escriba «P» y elija **Presente/Ausente**. La flecha abajo no cambia la opción: crea una fila vacía, que se quita con **–**.
4. Las fechas las trae Banner de la parte. El usuario guarda; Banner pone el número de regla. Sin la regla, el NRC no sale en Faculty › Control de asistencia (C101).

### Pasar lista y enviar la asistencia al libro (Autoservicio docente, C186)
1. Abra `https://facultyssb-test.usspesaas.elluciancloud.com:8100/FacultySelfService/ssb/facultyAttendanceTracking` (el botón «Ingresar asistencia» abre una ventana aparte) › **Pasar lista** del NRC.
2. Solo se marca la **columna de la fecha elegida** (resaltada a la derecha): pulse su encabezado o ‹ › y luego el círculo. Cada clic se guarda solo; el usuario autoriza las marcas antes.
3. Clase › «Actualizar la asistencia en el libro de calificaciones» › el usuario pulsa **Sí**.
4. Comprobar en `…/FacultySelfService/ssb/gradeEntry#/gradebook` › NRC › Componentes › ATTRGRD › Lista de alumnos.
5. **Notas (C187):** en el libro, buscar el NRC (la lista se duplica al recargar) › Componentes › componente › esperar a que se active «Lista de alumnos» › puntaje › Guardar (con permiso). La calificación sale al guardar. Para el siguiente componente: atrás y otra vez. Al final, «Calificaciones compuestas» muestra el porcentaje y la nota final.

### Cargar la fórmula de un NRC (SHAGCOM, C181)
1. SHAGCOM › periodo y NRC › Ir. Si el plan está vacío, Banner pide primero la escala: «Ingresar la escala de calificación antes de continuar».
2. Arriba, «Escala de calificación» **`VIG_11`** (no `AST_70`: con ella la final sale APRO, C120 y C123) › Tab › el usuario guarda.
3. Clic en Secuencia de la primera fila. Por cada componente: secuencia › Tab › nombre › Tab › descripción › Tab › peso › Tab, **esperando 1 a 2 s después de cada Tab**. Si se escribe seguido, Banner corre los campos. Un clic en otra celda no mueve el foco: Tab o Shift+Tab y, para reemplazar, Cmd+A.
4. Siga con Tab por la fila hasta «Nota aprobatoria»: la escala la hereda de arriba y la aprobatoria se llena sola (55 con `VIG_11`). El siguiente componente se agrega con el **+** del bloque.
5. `ATTRGRD`: peso 0, «Debe aprobar» con la barra espaciadora, escala `AST_70` (Cmd+A y escribir); la aprobatoria pasa sola a 70.
6. El usuario guarda: *Saved successfully (5 rows saved)* y «Total de peso final» 1.00. Plan del 10044 y del 10045: TA1 0.15, TA2 0.15, PA 0.40, EF 0.30 (C98).

### Crear un NRC (SSASECT)
- Ver la guía [ref-restricciones-y-prerrequisitos-por-programa.md](../../arquitectura-centros-empresariales/references/ref-restricciones-y-prerrequisitos-por-programa.md), paso 2 de la sección 2.

### Completar el horario y el docente de un NRC ya creado (SSASECT, C178, C180)
Probada el 30/10/2026 con el **NRC 10045** (202656, `ESEC 00701`, X06, sesión T), docente **100582059**, miércoles 15:30–17:10 según la hoja de NRC (C179, C180). El horario sale de la hoja del usuario; no se elige otro. El usuario mira el recorrido en su navegador; él inicia sesión con Google.
1. SSASECT › periodo `202656` › NRC `10045` › **Ir** (no «Crear NRC»). Comprobar con zoom que salen ESEC 00701, sección A y parte X06.
2. Pestaña **«Instructor y horas de reunión»** › subpestaña **«Fechas de reunión»** › **+** si no hay fila (en el 10045 ya estaba, con CLAS). Clic en «Hora de reunión» › Tab › Tab: Banner pone las fechas de la X06 (07-SEP a 31-OCT-2026). Casilla del día; rueda a la derecha; hora de inicio y fin en 24 h (`1530`, `1710`) con Tab; Indicador de sesión **01** (viene solo). Un Tab más lleva a **«Créditos y ubicación de reunión»**: Tab › edificio `SAUVIR` › Tab › salón `SALA-VIRT` › Tab › Tab › Tab › **O** en «Indicador de sobrepaso» (C97). 5.3, diap. 29.
3. El usuario guarda. Subpestaña «Créditos y ubicación de reunión»: Banner calcula las horas por semana (5.3, diap. 30).
4. Bloque **«Instructor»** de la sesión 01: clic en la fila › Tab › ID `100582059` › Tab. Banner trae el nombre, la carga 1.000, la responsabilidad 100, **Indicador de principal** marcado y porcentaje de sesión 100: solo se comprueba con la rueda a la derecha. 6.2.1, diap. 15 y 19.
5. El usuario guarda. Si sale «Conflicto de horario del instructor», el bloque choca con otro NRC suyo: se avisa y se revisa el Excel antes de marcar «Indicador de sobrepaso» (6.2.1, diap. 20; Script 17).
6. Comprobar: «Comenzar de nuevo» (a veces hay que pulsarlo dos veces) › Ir. Luego **SIAASGN** › `100582059` › 202656 › Ir: debe salir el 10045 (5.2 carga, diap. 24). Muestra una asignación por página: escribe el número de página en el cuadro de abajo y pulsa Intro. La alerta *«Reglas activas de carga de trabajo del docente no definidas para este periodo»* no impide consultar (C180).
7. Datos para la hoja de NRC (fila del 10045): PROGRAMA `CMEMC44`; LIB_AREA `MC44-01`, el área de la malla donde está el curso (C181; antes «no está en la malla», C178); CÓDIGO DOCENTE `100582059`; DOCENTE, el nombre completo; HORARIO y AMBIENTE, los que se guardaron. La tabla completa está en «Antes del NRC» de la Demostración 1.

## 5. Incidencias y salida
- **SOADEST** al abrir SFAREGS en una sesión nueva: DATABASE en los cinco campos (Horarios, Facturas, Históricos académicos, Ingresos, Cumplimiento) y abrir SFAREGS otra vez desde la lupa. **No hace falta guardar** (GUARDAR da «Función inválida», C158; probado sin guardar en C185).
- **«Otra sesión de inscripción está en progreso»:** alguien recargó con cambios pendientes; se esperan unos minutos (C158).
- **«Llave inválida… LIMPIAR DATOS»** al volver al bloque clave con algo a medio cambiar: recargar la página sin guardar (se pierde solo lo no guardado) y esperar el candado si sale.
- **Tras guardar en SFAREGS** la página puede volver sola al bloque clave con el aviso de inscritos: es normal.
- **«El uso de la página de inscripciones está prohibida para este periodo…»** al abrir SFAREGS: arrastró el periodo de la página anterior (por ejemplo 202444 de SCAPPRQ) y lo vació. Escribir el periodo de matrícula.
- **«La persona no es alumno, no se puede inscribir»** con un ID correcto: el ID no se validó (no sale el nombre al lado). Clic en el ID, borrar el último carácter, escribirlo y Tab.
- **Con «Ver currículos actuales/activos» marcado** desaparece el bloque «Plan de estudios de ingreso» y la fila nueva puede quedar **sin plan**: revisar la columna Plan de estudios antes de pedir el guardado (C170).
- **Sesión de Banner vencida:** pide iniciar sesión con Google; lo hace el usuario, nunca el agente.

## 6. Datos de prueba en TEST (29/10/2026)
- **Alumno:** Arnold Vaca `S00912438` (Medicina `1PCSP15`, plan 1; `CMEMC38`; `IMEMI03` en el plan 4). En 202744 tiene los NRC 10001 a 10008 de otra persona: **no se tocan**.
- **Otro alumno:** `100582059` (`CMEMC44`). **Alumno de Nidia:** `A00010005` (catálogo 202444; Basic I con 80 en 202646; en 202744 tiene 10023, 10024, 10022 y 10007; avisar a Nidia antes de usarlo).
- **NRC:** 10045 (202656, X06, Computación; miércoles 15:30–17:10, SAUVIR / SALA-VIRT, docente 100582059, malla `MC44-01` › `ECOM-03`, fórmula en SHAGCOM y regla 3 de SOAATRK desde el 30/10, C180 a C182)
- **SOATERM 202656** (solo consulta, C182): En progreso sin marcar, Permitir ✓, Plan de estudios requerido ✓; las demás casillas sin marcar; secuencia de inicio de NRC 10046., 10042 y 10043 (Basic I, 202656, I10), 10020 a 10022 (202744, T1, pregrado).
- **Acceso a TEST:** https://experience-test.elluciancloud.com/ussipantest, también en el botón «Banner TEST» de la galería y del visor del sitio (C178). Cada persona entra con su cuenta de Google.
- Lo que quedó en TEST y falta limpiar: sección 4 de la guía de restricciones y C167.
