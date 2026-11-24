# Preguntas frecuentes de operación: Crear y configurar periodos en Banner

Respuestas cortas para el asistente IA y para cualquier agente, tomadas de los instructivos 1.1.1 y 1.1.2 (Capacidad 1), de lo visto en TEST y del registro. Cada pregunta es un fragmento de la base del asistente (C197, C237, C238). Producción empieza con 202721 (ADR-026): lo de 2026 fue TEST. Si la respuesta no está aquí ni en el registro, se dice «No lo sé» (ruta de escape).

Tema de este archivo: crear, configurar y editar un periodo y sus partes en Banner (STVTERM, STVPTRM, STVACYR, STVTRMT, SOATERM, SFARSTS, SSAEXCL). Qué son y cuáles usan los centros está en `ref-preguntas-frecuentes-periodos.md`; el periodo 202721 tal como está en TEST, en `ref-preguntas-frecuentes-periodo-202721.md`; la tabla de pestañas de SOATERM y el cronograma 2026, en `ref-periodos-y-cronograma.md`.

### ¿Cómo se crea y se configura un periodo académico nuevo en Banner?
Primero el código en STVTERM y después la configuración en SOATERM (C141).
1. **STVTERM** › Insertar (+). Complete **Periodo** (6 dígitos, por ejemplo `202721`), **Descripción** (hasta 30 caracteres), **Fecha de inicio y fin** y **Año académico** (de STVACYR). El **Tipo de periodo** (de STVTRMT) es opcional (1.1.1, diap. 18 y 19).
2. Complete las **fechas de alojamiento** (las mismas del periodo) y el **año de ayuda financiera**: son obligatorios aunque no se usen. Pulse Guardar (diap. 19 a 21).
3. **SOATERM** › Periodo › **Ir**. Para partir de uno anterior, escríbalo en **Copiar De periodo** y pulse COPIAR (1.1.2, diap. 16; U22).
4. Pestaña **Inscripción**: número de inicio de NRC y casillas como Permitir y Plan de estudios requerido (diap. 17 y 18).
5. Pestaña **Controles de inscripción de parte de periodo y web**: agregue con + cada parte y la parte 1, con inicio, fin, semanas y censo uno; en la misma fila están el sobrepaso de sección y la Web del docente (diap. 22). Ponga las fechas de inscripción web y de acceso docente, y pulse Guardar (diap. 20 a 24).

Las demás pestañas: Verificación de errores de inscripción (5.4, diap. 14 a 16), Controles de procesamiento web (1.1.2, diap. 25 a 32) e Inscripción estructurada y proyectada (5.4, proyección, diap. 16 y 17). Así quedó 202721 en TEST, con capturas: `centros/comun/diagramas/01-capacidad-1-periodo-202721/`.

### ¿Cómo agrego las partes de periodo a un periodo?
1. Si el código de la parte no existe, créelo en **STVPTRM**: hasta 3 caracteres y una descripción (1.1.1, diap. 14).
2. Abra **SOATERM** › periodo › Ir › pestaña **Controles de inscripción de parte de periodo y web**.
3. En el bloque **Parte de periodo base**, pulse + y complete la parte, la **fecha de inicio y fin**, el **número de semanas** y la **fecha de censo uno**. Pulse Guardar (1.1.2, diap. 20 y 21).

La parte **1** («Periodo completo») siempre debe estar (diap. 20). Agregue solo las partes que usará el periodo, porque SSASECT ofrece solo esas (C141).

### ¿Qué se configura antes del NRC y en qué orden?
Este es el orden (C141, C144):
1. **STVTERM**: el código del periodo, solo si no existe.
2. **STVPTRM**: el código de la parte, solo si no existe.
3. **SOATERM** › Controles de inscripción de parte de periodo y web: las partes del periodo, con fechas, semanas y censo uno.
4. **SCACRSE**: el curso del catálogo, solo si no existe (1.1.4, diap. 20 a 25).
5. **SSASECT**: el NRC, en su parte (5.3, diap. 23).

Además, **SFARSTS** debe tener los estatus de inscripción de esa parte. Sin ellos, SFAREGS no matricula (C154).

### ¿Cómo edito un periodo que ya existe?
El código (por ejemplo `202721`) no se edita en ninguna página (C143).
- **STVTERM:** se cambian la descripción, las fechas, el año académico, el tipo de periodo y las fechas de alojamiento; luego se guarda (1.1.1, diap. 18 y 19).
- **SOATERM** › periodo › Ir, según la pestaña:
  - **Inscripción:** secuencia de NRC y casillas (1.1.2, diap. 17 y 18).
  - **Controles de inscripción de parte de periodo y web:** partes, sobrepaso y Web del docente de cada parte, fechas web y acceso docente (diap. 20 a 23).
  - **Controles de procesamiento web:** lo que el alumno, el docente y el asesor ven y hacen en el autoservicio (diap. 25 a 32).

El periodo de los centros (202721 desde 2027) es compartido: si el cambio es para un solo grupo, cambie la parte. Falta confirmar si cambiar las fechas de una parte actualiza los NRC ya creados (E27).

### ¿Para qué sirve SOATERM?
Es el **control de periodo**: habilita el periodo creado en STVTERM (1.1.2). Ahí se configuran:
- El número de inicio de NRC y las casillas de inscripción, como Permitir, En progreso y Plan de estudios requerido (diap. 17 y 18).
- Las partes de periodo, con sus fechas (diap. 20 y 21).
- La Web del docente, como columnas de cada parte (diap. 22), y los controles web del alumno, el docente y el asesor (diap. 25 a 32).
- La **verificación de errores de inscripción**: Fatal o No verificar para prerrequisitos, duplicados, programa y otras verificaciones (C149).

Si **Permitir** no está marcada, nadie se matricula en el periodo (C182).

### ¿Qué casillas de SOATERM tienen marcadas los centros?
En **202721** (TEST, 24/11/2026; C238) la pestaña Inscripción tiene marcadas Permitir y Plan de estudios requerido; el NRC empieza en 10012 (lo da el sistema), el modelo es Básico y Proyectado y la Estimación en línea está sin marcar (E23). Detalle en `ref-preguntas-frecuentes-periodo-202721.md`.

Esto mostraba SOATERM 202656 en TEST 2026, pestaña Inscripción (C182):
- **Permitir:** marcada. Sin ella nadie se matricula.
- **Plan de estudios requerido:** marcada. Obliga a matricular con un plan (C86).
- **En progreso:** sin marcar. Un curso en curso no cuenta para el prerrequisito hasta que se califica (R10). Siguen abiertas E13 y E31.
- **Sin marcar:** Calcular estatus de hora, Incluir horas intentadas, Periodos futuros para repeticiones y Eliminación calculada.
- **Readmitir:** vacío.
- **Secuencia de NRC:** en 10046.
- **Contraseña de retención:** tiene una, pero no se publica.

### ¿Qué páginas se usan para configurar los periodos?
- **STVTERM:** códigos de periodo (1.1.1, diap. 18 a 21).
- **STVPTRM:** códigos de parte de periodo. La parte 1 es obligatoria (diap. 14).
- **STVACYR:** años académicos. 0000 y 9999 son obligatorios (diap. 15).
- **STVTRMT:** tipos de periodo (diap. 16). En TEST hay A Anual, B Bimestral, C Cuatrimestral, M Mensual, S Semestral y T Trimestral; 202721 usa S (C238, E37).
- **SOATERM:** control de periodo: inscripción, partes con fechas, web y verificación de errores (1.1.2, diap. 16 a 32).
- **SSAEXCL:** feriados y días sin clase, por año y parte de periodo (1.1.2, diap. 34 a 37).

### ¿Dónde se configuran las fechas del periodo y de sus partes?
- **Inicio y fin del periodo:** STVTERM (1.1.1, diap. 18).
- **Inicio, fin, semanas y censo de cada parte:** SOATERM › Controles de inscripción de parte de periodo y web (1.1.2, diap. 20 y 21).
- **Inscripción web y acceso docente:** SOATERM, en la misma pestaña (diap. 23 y 24). En 202721: web del 16-NOV-2026 al 14-MAR-2027 y acceso docente del 01-ENE al 06-JUN-2027 (C238).
- **Estatus de inscripción de cada parte (RE, DD, RW y DW):** SFARSTS, con sus fechas (C154).
- **Feriados:** SSAEXCL (1.1.2, diap. 34 a 37).

El NRC toma las fechas de su parte al elegirla en SSASECT (5.3, diap. 23).

### ¿Qué necesita una parte de periodo para matricular en sus NRC?
- Que la parte esté en el SOATERM del periodo. Si no está, SSASECT no la ofrece (C141).
- Que **SFARSTS** tenga los estatus de inscripción de ese periodo y esa parte, con fechas: RE y DD por backoffice, RW y DW por autoservicio.

Sin esos estatus, SFAREGS da «Las reglas del estatus de inscripción al curso no están definidas para la parte de periodo» (C154). En 202656, X06 los tiene y X07 no (C156; U48).

### ¿Qué pasa si cambio las fechas de una parte de periodo?
Las fechas se cambian por periodo en SOATERM › Partes de periodo (1.1.2, diap. 20 y 21). El NRC las toma al elegir la parte en SSASECT (5.3, diap. 23).
- **Por confirmar (E27):** si el cambio llega solo a los NRC ya creados o si hay que elegir de nuevo la parte en cada uno.
- **Visto en TEST:** al pasar el NRC 10045 de X07 a X06, el censo uno cambió solo a 14-SEP-2026 (C156).

### ¿Dónde se registran los feriados del periodo?
En **SSAEXCL** (reglas de exclusión de horario):
1. Ingrese el año y la parte de periodo, y pulse Ir.
2. Pulse Insertar y complete la fecha y la descripción. Banner calcula el día.
3. Pulse Guardar.

Con «Predefinir exclusiones de horario» se copian los feriados de una parte a otra (1.1.2, diap. 34 a 37). En el flujo, los registra Registros Académicos al abrir el periodo (paso 1). En TEST, 2027 todavía no tiene feriados en la parte 1; 2026 tiene 13 (C238, E39).
