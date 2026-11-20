# Preguntas frecuentes de operación: Matrícula e inscripción

Respuestas cortas para el asistente IA y para cualquier agente, tomadas de lo probado en TEST (NRC 10044 y 10045) y del registro. Cada pregunta es un fragmento de la base del asistente (C197). Si la respuesta no está aquí ni en el registro, se dice «No lo sé» (ruta de escape).

Tema de este archivo: SFAREGS, baja DD, prerrequisitos por programa, proyección SFPPROJ y turnos. Los otros temas están en los demás `ref-preguntas-frecuentes-*.md` (índice en el `SKILL.md` de esta skill).

### En SFAREGS sale «No se ha completado la configuración requerida». ¿Qué hago?
Banner pide **SOADEST** la primera vez que se abre SFAREGS en una sesión nueva. Escriba **DATABASE** en los cinco campos (Horarios, Facturas, Históricos académicos, Ingresos y Cumplimiento) y abra SFAREGS otra vez desde la lupa, **sin guardar SOADEST**: así entra (C185). Si pulsa GUARDAR en SOADEST, Banner responde «\*ERROR\* Función inválida»; no hace falta guardar (C158).

### ¿Cómo doy de baja a un alumno de un NRC con DD y hasta cuándo se puede?
SFAREGS › periodo › ID › **Ir** (si sale SOADEST, ver la pregunta anterior). Baje con **⏬** hasta «Información de curso» (un clic en la tabla no mueve el foco), cambie el **Estatus** del NRC de **RE a DD** y pulse Tab: las horas bajan a 0.000. Al guardar salen «Estimación de cuota procesada» y «Los alumnos ya están inscritos…»; al reabrir, el NRC queda en DD (C189). El DD vale mientras la **parte de periodo** lo permita en SFARSTS: en 202656, la **X06** tiene DD, DW, RE y RW del **07-SEP al 31-OCT-2026** y la X07 no tiene reglas (C156). Si sale «El estatus "DD" es inválido…», esa parte no tiene DD. Un RE no se borra: se cambia a DD.

### ¿Qué hace SFPPROJ? ¿Simula la proyección del alumno?
No es solo una simulación: **calcula y guarda** la proyección. Con el último **CAPP** del periodo (SMRBCMP o SMARQCM), SFPPROJ arma para cada alumno la lista de cursos que aún no aprobó y que puede inscribir en ese periodo según su avance curricular. La lista queda en **SFAPROJ**, donde se consulta y se puede corregir (+ y −). Esa lista es la que el alumno ve en la pestaña Proyecciones de la planificación y la inscripción por autoservicio; si SOATERM tiene «Restringir a cursos proyectados», solo puede inscribir esos cursos (instructivo 5.4 «Ejecutar la proyección académica», diap. 10, 47 y 51; C205).

Antes de correrla (diap. 14 a 27): el CAPP del periodo ya ejecutado; en **SOATERM**, la casilla «Proyección» del periodo y la pestaña «Inscripción proyectada»; en **SMAPROG**, el modelo de inscripción «proyectada» del plan y las áreas con prioridad; en **GTVSDAX**, PRIADJFAC del grupo REGPROJSTRUCT; y en **SFALPROJ**, el máximo de áreas y créditos por programa.

Pasos (diap. 30 a 40): **GJAPCTL** › **SFPPROJ** (Proc. de proyección del alumno) › **Ir** › impresora **DATABASE** › los 15 parámetros › **Enviar** › **Guardar** › **GJIREVO** › `.lis` (si aún corre, sale el aviso de error «No hay salidas guardadas…»).

| N.º | Parámetro | En TEST, 19/11/2026 (C205) | Qué dice el instructivo (diap. 33 y 34) |
|---|---|---|---|
| 01 | Periodo de inscripción | `202744` | periodo de la proyección (R) |
| 02 | Periodo de horario | `202744` | vacío o el mismo del 01 |
| 03 | Identificador de selección | `POB_CICLO_B` | selección de población (O) |
| 04 | Aplicación de selección | `STUDENT` | (O) |
| 05 | ID de creador de selección | el creador de la selección | (O) |
| 06 | ID de usuario de selección | el usuario | (O) |
| 07 | Número de ID | vacío | un solo alumno (O) |
| 08 | Escuela | vacío | todos los de esa escuela (SMAPRLE) (O) |
| 09 | Carrera | vacío | todos los de esa carrera en SGASTDN (O) |
| 10 | Tipo de alumno | vacío | todos los de ese tipo en SGASTDN (O) |
| 11 | Currículo | por confirmar | **P** currículo principal o **A** todos los currículos del alumno (R) |
| 12 | Incluir cursos ofrecidos | por confirmar | **Y** solo cursos con **NRC** programado en el periodo de horario; **N** todos los del catálogo |
| 13 | ¿Verif. de prerrequisito? | por confirmar | Y o N |
| 14 | ¿Verif. de correquisito? | por confirmar | Y o N |
| 15 | Campus | por confirmar | solo para verificar prerrequisitos y correquisitos, no filtra alumnos |

**Resultado en TEST** (C207): proceso 8399; en GJIREVO, `sfpproj_<job>.lis`, `sfpproj_<job>.log` y `gjrjlis_<job>.log`. El .lis «Registration Projection Process» dice «Projections processed for compliance records read from CAPP.» y da, por alumno, el programa y **Records Projected** (cuántos cursos se le proyectaron: de 2 a 15 en la prueba, 11 alumnos). Si un alumno no tiene CAPP del periodo o falla algo, sale en «Comments».

07 a 10 van **vacíos** porque la corrida es general sobre la selección (usuario, C205). Ojo con el 12: según el instructivo, **Y** es «solo cursos con NRC» y **N** es «todo el catálogo»; A y P son del parámetro 11.

### ¿Dónde se activa la verificación de prerrequisitos por programa (SOACTRL)?
En **SOACTRL** (Control de reglas de currículo) › pestaña **«Prerrequisito por programa»** › Restricciones › casilla **«Realizar verificación de prerrequisito por programa»**; al lado está «Restricción de periodo». En TEST, el 19/11/2026, estaba marcada y «Restricción de periodo» no (C206). Es una configuración de toda la institución, no de un periodo.

Registros la vio activa al correr la proyección (SFPPROJ) y comentó que la apagarían y que solo importa para la inscripción por autoservicio. **Por confirmar (U55):** el prerrequisito por programa de **SCAPPRQ** es el que se probó para las acreditaciones de los centros (C159 a C167); si se apaga esta casilla, esa verificación podría dejar de funcionar para los centros. Antes de apagarla, hay que confirmarlo con Registros y Ellucian.

### ¿Cómo se configuran los turnos de inscripción (SFARCTT, SFARCTL, SFARGRP, SFRGRUP)?
1. **SFARCTT** (Control de prioridad de inscripción): periodo › «+» › fecha y hora de inicio y fin (HHMM, 24 horas) › **número de prioridad** único › guardar. Una prioridad puede tener varios rangos.
2. **SFARCTL** (Control de grupo de inscripción): periodo › «+» › prioridad › **código de grupo** (hasta 10 caracteres) › guardar. El **«Conteo de grupo»** dice cuántos alumnos tienen el grupo: si está en **0** es porque aún no se asignó a ningún alumno.
3. Asignar el grupo al alumno: **uno por uno en SFARGRP** (ID y periodo › elegir el grupo › abajo salen sus fechas y horas › guardar) o **en masa con SFRGRUP** desde GJAPCTL (impresora DATABASE; 01 periodo, 02 grupo, 11 a 14 la selección de población, 15 modo A auditar o U actualizar; con selección solo van 01, 02 y 11 a 15; resultado en GJIREVO).

Fuente: instructivo 5.4 «Inscripción de cursos por lista de espera», diap. 50 a 60 y 76 a 88. **Aún no se prueba en TEST:** queda para más tarde, con los datos de la hoja «Est Ciclo Cierre» del plan V7 (prioridades 2 y 3 del 19/11 al 20/11/2026, de 00:00 a 20:00, `GRUPO_1` y `GRUPO_2`; C209).

### ¿Cómo se registra un pago en caja (TVACAJA)?
**No es tarea de los centros:** la caja es de Finanzas (Capacidad 11); los centros son la Capacidad 1 (C217). El cajero abre **TVACAJA** (si Banner pide **TOADEST**, pone `DATABASE` en Facturas, Recibos y Resumen de alumno y cierra), escribe periodo e ID y pulsa Ir: salen todos los cargos con saldo del alumno, de todos sus periodos. Marca los cargos, en «Total de monto a pagar» pone el código de pago (por ejemplo `M001` Efectivo, `M004` POS Niubiz, `M018` Ventanilla BCP) y el monto, guarda y confirma con OK; Banner da el **número de recibo** y se imprime con «Imprimir recibo». En TSAAREV el cargo y el pago quedan unidos por ese recibo (instructivo 11.2.2, diap. 40 a 45). Solo cobra quien tiene perfil en **TGAUPRF** (diap. 13 a 18); en TEST el usuario de Dagner no lo tiene. Revisado en TEST solo en consulta (C217); el código de pago de los centros está por confirmar con Finanzas.
