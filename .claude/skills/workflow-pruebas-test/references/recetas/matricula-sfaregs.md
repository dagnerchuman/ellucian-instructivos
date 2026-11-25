# Recetas de TEST: Matrícula en SFAREGS

Recetas probadas en Banner TEST (matricular, dar de baja, agregar el programa del centro). Antes, lee las reglas, cómo moverse en Banner y las incidencias en [manejo-banner-test.md](../manejo-banner-test.md): **nunca se guarda sin permiso del usuario**.

### Matricular a un alumno en un NRC (SFAREGS)
1. SFAREGS › periodo › ID › Ir.
2. ⏬ dos veces hasta «Información de curso» › **+** › NRC › Tab › plan de estudios (el que tenga registro en «Plan de estudios de ingreso»; si no, sale *«No existe el registro del estatus del ingreso para este plan de estudios»*, C166) › Tab.
3. Si queda una fila vacía al final, se deja: no se guarda.
4. El usuario guarda. Correcto: *«Los alumnos ya están inscritos»*. Para comprobarlo, volver a abrir con Ir.
5. Error: *«El horario del alumno tiene errores»*; el motivo está en la columna Mensaje («Program Restriction», «Prerequisite and Test Score error», «Prerequisite In Progress»). Esa fila ya no se puede quitar: recargar la página y esperar el candado (sección 5 de [manejo-banner-test.md](../manejo-banner-test.md)).

6. **Alumno recién admitido (C247):** al bajar a cursos, Banner crea el «Plan de estudios de ingreso» (`EL`) y pide guardarlo antes del bloque de curso; se guarda (2 rows) y recién se pone el NRC.
7. **«Closed Section» (Error fatal):** el NRC no tiene cupo. SSASECT › Información de ingreso de sección › Máximo y Proyectado (40, C97) › guardar; luego esperar el candado de SFAREGS (unos 2 minutos) y volver a poner el NRC (C33, C247).

### Dar de baja (SFAREGS)
- ⏬ hasta «Información de curso» (un clic en la tabla no siempre mueve el foco) › columna Estatus › DD › Tab › el usuario guarda: *«Estimación de cuota procesada»* y *«Los alumnos ya están inscritos»*. Probado con Arnold en el 10045, X06 (C189). Si sale *«El estatus “DD” es inválido…»*, la parte de periodo no tiene DD en SFARSTS. Con ••• en Estatus se abre SFQRSTS con los estatus permitidos (en 202744, parte 1, solo RE). Un RE no se borra (C158, C167).

### Agregar el programa del centro a un alumno (SFAREGS › Currículos)
- Fila nueva › programa desde **••• › «Reglas de currículo base por programa»** › fila del campus › OK; campo de estudio y departamento. Escribir el programa a mano y pulsar Intro arrastra datos de otro currículo (C153, C166).
