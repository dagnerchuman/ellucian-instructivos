# Recetas de TEST: NRC

Recetas probadas en Banner TEST (crear el NRC, horario y docente en SSASECT, regla de asistencia en SOAATRK). Antes, lee las reglas, cómo moverse en Banner y las incidencias en [manejo-banner-test.md](../manejo-banner-test.md): **nunca se guarda sin permiso del usuario**.

### Crear un NRC (SSASECT)
- Ver la guía [ref-restricciones-y-prerrequisitos-por-programa.md](../../../arquitectura-centros-empresariales/references/ref-restricciones-y-prerrequisitos-por-programa.md), paso 2 de la sección 2.

### Crear un NRC de un centro (SSASECT, C222)
Probada el 20/11/2026 con el **10047** (Emprendimiento). Periodo › Tab › **Crear NRC**. Materia › Tab › curso › Tab (Banner pone el título y las horas). Llenar **un campo a la vez y comprobar con zoom**: si un campo da error, el foco se queda ahí y lo que se escriba después cae en él. Copiar los valores de otro NRC del mismo curso: sección (la siguiente libre), campus `SCH`, estatus A, horario `TEO` (Banner propone método `SEMI`; cambiar a `VIRT`), **socio de integración `OPLMS`** (lista ••• › SELECCIONAR), modo de calificar V, sesión, parte (P06 trae fechas y semanas). Horas: crédito y cobro deben ser uno de los valores del curso cuando el indicador es O (ESGE 00117: crédito 0 o 4, cobro 0 o 1); contacto, teoría y laboratorio, los del curso. GUARDAR: Banner da el NRC. Comprobar en SSASECT › periodo › NRC › Ir. Todo en Experience, no en Banner Admin directo.

### Completar el horario y el docente de un NRC ya creado (SSASECT, C178, C180)
Probada el 30/10/2026 con el **NRC 10045** (202656, `ESEC 00701`, X06, sesión T), docente **100582059**, miércoles 15:30–17:10 según la hoja de NRC (C179, C180). El horario sale de la hoja del usuario; no se elige otro. El usuario mira el recorrido en su navegador; él inicia sesión con Google.
1. SSASECT › periodo `202656` › NRC `10045` › **Ir** (no «Crear NRC»). Comprobar con zoom que salen ESEC 00701, sección A y parte X06.
2. Pestaña **«Instructor y horas de reunión»** › subpestaña **«Fechas de reunión»** › **+** si no hay fila (en el 10045 ya estaba, con CLAS). Clic en «Hora de reunión» › Tab › Tab: Banner pone las fechas de la X06 (07-SEP a 31-OCT-2026). Casilla del día; rueda a la derecha; hora de inicio y fin en 24 h (`1530`, `1710`) con Tab; Indicador de sesión **01** (viene solo). Un Tab más lleva a **«Créditos y ubicación de reunión»**: Tab › edificio `SAUVIR` › Tab › salón `SALA-VIRT` › Tab › Tab › Tab › **O** en «Indicador de sobrepaso» (C97). 5.3, diap. 29.
3. El usuario guarda. Subpestaña «Créditos y ubicación de reunión»: Banner calcula las horas por semana (5.3, diap. 30).
4. Bloque **«Instructor»** de la sesión 01: clic en la fila › Tab › ID `100582059` › Tab. Banner trae el nombre, la carga 1.000, la responsabilidad 100, **Indicador de principal** marcado y porcentaje de sesión 100: solo se comprueba con la rueda a la derecha. 6.2.1, diap. 15 y 19.
5. El usuario guarda. Si sale «Conflicto de horario del instructor», el bloque choca con otro NRC suyo: se avisa y se revisa el Excel antes de marcar «Indicador de sobrepaso» (6.2.1, diap. 20; Script 17).
6. Comprobar: «Comenzar de nuevo» (a veces hay que pulsarlo dos veces) › Ir. Luego **SIAASGN** › `100582059` › 202656 › Ir: debe salir el 10045 (5.2 carga, diap. 24). Muestra una asignación por página: escribe el número de página en el cuadro de abajo y pulsa Intro. La alerta *«Reglas activas de carga de trabajo del docente no definidas para este periodo»* no impide consultar (C180).
7. Datos para la hoja de NRC (fila del 10045): PROGRAMA `CMEMC44`; LIB_AREA `MC44-01`, el área de la malla donde está el curso (C181; antes «no está en la malla», C178); CÓDIGO DOCENTE `100582059`; DOCENTE, el nombre completo; HORARIO y AMBIENTE, los que se guardaron. La tabla completa está en «Antes del NRC» de la Demostración 1.

### Regla de asistencia de un NRC (SOAATRK, C182)
1. SOAATRK › periodo › Ir: salen las reglas del periodo (en 202656, la 2 del 10044 y la 3 del 10045).
2. Clic en una fila › **+** del bloque › parte (X06) › Tab › materia › Tab › curso › Tab › NRC › Tab, esperando 1 a 2 s después de cada Tab. «Desplegar clase» y «Control de asistencia a clases» vienen marcadas.
3. «Unidad de control» es una lista con búsqueda: escriba «P» y elija **Presente/Ausente**. La flecha abajo no cambia la opción: crea una fila vacía, que se quita con **–**.
4. Las fechas las trae Banner de la parte. El usuario guarda; Banner pone el número de regla. Sin la regla, el NRC no sale en Faculty › Control de asistencia (C101).

### Asignar docente y, si choca, crear un docente de prueba (C225)
1. **SSASECT › Instructor y horas de reunión › bloque Instructor:** clic en la celda **ID** (no en «Indicador de sesión»: si el foco queda ahí, los números caen en la sesión y queda `10`; se corrige con End, Backspace y `01`). Tab valida el ID y Banner pone nombre, 100 % y principal ✓.
2. Si GUARDAR da **«Conflicto de horario del instructor»**, el docente ya dicta otro NRC a esa hora del periodo (lo ves en SIAASGN). No se marca «Sobrepaso» sin que el usuario lo pida; con su permiso se crea una persona de prueba:
   - **SPAIDEN** › botón **+** del ID (`GENERATED`) › Ir abre **GOAMTCH** › Origen `PERS_NATU` «Persona Natural» (lista •••; `PERS_JURI` es persona jurídica) › Ir › Apellido y Nombre (uno por vez, con zoom) › GUARDAR › «No se encontraron coincidencias; ¿crear nuevas?» › **SÍ** › Banner da el ID (`S009…`) y solo crea el registro de identificación.
   - **SIAINST** › ID y periodo › Ir («Query caused no records…» es normal) › Estatus `AC` › Tab (Banner pone la fecha) › casilla **Docente** › GUARDAR. Categoría, tipo de personal y regla de carga pueden quedar vacíos.
   - Vuelve a SSASECT y cambia el ID del instructor por el nuevo.
3. **Campo que borra lo escrito:** tras End + Backspace, a veces lo que escribes se pierde. Haz clic de nuevo en el campo, escribe, y revisa con zoom antes de Tab o Ir.

### ⚠ Carga de trabajo del docente: revisarla SIEMPRE (SIAASGN, C226 a C228)
- La carga no sale de las horas de clase: viene de **SCACRSE › Tipo de horario › Carga de trabajo** (en ESGE 00117, TEO 1.000 y PRA 2.000). El contacto semanal sí sale del horario, en horas de 50 minutos (09:00–11:00 = 2.4).
- **Regla del usuario:** la carga debe ser igual a las horas que dicta el docente. Si no lo es, en **SIAASGN** › ID › periodo › Ir › la asignación del NRC › **«Sobrepasar carga de trabajo»** con las horas reales › Tab (la carga calculada y el FTE se recalculan) › GUARDAR.
