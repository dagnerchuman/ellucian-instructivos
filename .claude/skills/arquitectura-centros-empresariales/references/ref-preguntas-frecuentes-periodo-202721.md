# Preguntas frecuentes de operación: el periodo 202721 (producción 2027)

Respuestas cortas para el asistente IA y para cualquier agente, tomadas de lo visto en TEST el 24/11/2026 (por Experience, sin guardar), de los instructivos 1.1.1, 1.1.2 y 5.4 y del registro (C238). Cada pregunta es un fragmento de la base del asistente. Si la respuesta no está aquí ni en el registro, se dice «No lo sé» (ruta de escape).

Tema de este archivo: el periodo **202721**, el primero de producción de los centros, cómo está en TEST y qué falta confirmar. Qué son el periodo y la parte está en `ref-preguntas-frecuentes-periodos.md`; cómo se crea y se configura un periodo, en `ref-preguntas-frecuentes-periodos-configuracion.md`.

### ¿Qué es el periodo 202721, con el que empieza producción?
Es el **verano 2027 de Centros Empresariales** («Verano 2027 - Cent.Empresarial»), del **01-ENE al 31-MAR-2027**. Es el primer periodo de producción: lo de 2026 fue TEST (C238, ADR-026).
- Código: año 2027 + **2** (centros) + **1** (verano). «41» es pregrado de verano (202741).
- Lo comparten Idiomas, Computación y Emprendimiento. Cada grupo es una parte de periodo (ADR-006).

### ¿Quién crea el periodo 202721 y quién da sus partes y fechas?
- El periodo lo crea **Registros Académicos**, «como hasta ahora» (C238).
- Las partes y sus fechas las dan las **jefaturas**, desde sus mallas (C238). Falta confirmar cuándo las entregan y si las de TEST son las de producción (U58).
- Quién hace los demás pasos de la Capacidad 1 en producción está por confirmar (U57).
- El número inicial del NRC lo da el sistema (C238).

### ¿Qué datos tiene 202721 en STVTERM?
En TEST (instructivo 1.1.1, diap. 18 a 21; C238):
- Fechas: 01-ENE-2027 a 31-MAR-2027. Alojamiento: las mismas.
- Tipo de periodo **S** «Semestral» (STVTRMT no tiene tipo de verano) y casilla **Verano** sin marcar (E37).
- Año académico 2027 (STVACYR: 01-ENE a 31-DIC-2027). Año de ayuda financiera 2027.
- Periodos de ayuda financiera vacíos y «Requerido por el sistema» sin marcar.

En la misma lista está **202724** «2027-I Centro Empresariales», del 01-ABR al 31-JUL-2027; falta confirmar que sea el semestre I de producción (U56).

### ¿Qué partes tiene el periodo 202721?
En SOATERM de TEST hay **10 partes** (C238), con el censo uno igual a la fecha de inicio:

| Centro | Parte | Fechas 2027 | Semanas |
|---|---|---|---|
| Idiomas | I01 | 04-ENE a 28-FEB | 8 |
| Idiomas | I02 | 04-ENE a 31-MAR | 13 |
| Idiomas | I03 | 01-FEB a 31-MAR | 9 |
| Idiomas | I04 | 01-FEB a 30-ABR | 13 |
| Emprendimiento | P01 | 06-ENE a 14-MAR | 10 |
| Emprendimiento | P02 | 03-FEB a 11-ABR | 10 |
| Computación | X01 | 04-ENE a 27-FEB | 8 |
| Computación | X02 | 01-FEB a 27-MAR | 8 |
| Computación | X03 | 08-MAR a 03-ABR | 4 |
| Todos | 1 | 04-ENE a 31-MAR | 13 |

I04, P02 y X03 terminan después del 31-MAR-2027, fin del periodo (E34). El censo dos y las «últimas fechas» están vacíos (E38).

### ¿Cómo está la pestaña Inscripción de SOATERM en 202721?
(1.1.2, diap. 16 a 19; C238)
- NRC desde **10012**. **Permitir** y **Plan de estudios requerido** marcados.
- La contraseña de retención existe y no se publica (C182).
- Estimación en línea sin marcar (E23). Seguimiento por NRC, Permitir intercambio, Cuotas de sección por plan y Revertir cargos marcados. Corte del cargo: 01-ENE-2027.
- Modelo de inscripción **Básico** y **Proyectado**; Estructurado sin marcar.
- Título IV por fecha de periodo; cuota de autoservicio solo por lotes; control de periodo en web maestro marcado.

### ¿Qué verificación de errores de inscripción tiene 202721?
SOATERM › Verificación de errores de inscripción (5.4, inscripción por backoffice, diap. 14 a 16; C238):
- **Alumno:** Duplicados, Ligas, Correquisitos, Horas mínimas y Hora en Fatal; Prerrequisitos, Horas máximas y Exclusión mutua en No verificar.
- **Sección:** Aprobación, Capacidad, Campo de estudio, Escuela, Nivel, Clase y Retenciones en Fatal; Departamento, Horas repetidas, Límite de repetición, Campus, Grado, Programa, Atributo de alumno y Cohorte en No verificar.

Frente a 202656 (C149) pasaron de Fatal a No verificar Prerrequisitos, Horas repetidas, Límite de repetición y Campus. Si Prerrequisitos queda así, falta saber si se exigen los de SCAPPRQ (E36).

### ¿Dónde está la Web del docente y cómo está en 202721?
No está en «Controles de procesamiento web»: son columnas de cada parte en **Controles de inscripción de parte de periodo y web** (1.1.2, diap. 22).
- Calificaciones parciales, calificaciones finales y lista de espera: **sin marcar** en las 10 partes de 202721.
- La diap. 22 dice que deben estar marcadas para cargar notas por web: hay que confirmarlo con Ellucian (E35).
- **Sobrepaso de sección:** marcado en las 10 partes.

### ¿Qué fechas web y controles web tiene 202721?
- Inscripción web: **16-NOV-2026 a 14-MAR-2027**. Acceso de docente y asesor: **01-ENE a 06-JUN-2027**, con Menú y Selección de periodo (1.1.2, diap. 23 y 24).
- Controles de procesamiento web: despliegue de notas, horario y lista de clases, webcapp, catálogo y horario marcados; cambio de opción de clase y autorizaciones sin marcar; planificación abierta con 1 plan como máximo (diap. 25 a 32).

### ¿Qué tienen las pestañas Inscripción estructurada y proyectada de 202721?
- **Estructurada:** severidad de error Ninguno; Revisar historia académica No; Obligatorio, Opcional y Electivo sin activar (el modelo Estructurado está sin marcar).
- **Proyectada:** restricciones marcadas (periodo abierto para proyecciones, restringir a cursos proyectados y a proyecciones nulas); incluir y marcar cursos reprobados; Obligatorio y Electivo activos, sin claves de regla (5.4, proyección, diap. 16 y 17).

Si los centros usarán la proyección está por confirmar (E40).

### ¿Hay feriados de 2027 en SSAEXCL?
**No todavía.** SSAEXCL › año 2027 › parte 1 da «Query caused no records». El año 2026, parte 1, tiene 13 feriados, de Año nuevo a Navidad (C238). Los feriados se cargan por año y parte; «Predefinir exclusiones de horario» los copia de una parte a otra (1.1.2, diap. 34 a 37). Quién los carga y en qué partes, en E39.

### ¿Qué dudas de 202721 hay que preguntar a Ellucian?
E34 partes que terminan después del periodo · E35 Web del docente sin marcar · E36 Prerrequisitos en No verificar · E37 tipo S y casilla Verano · E38 fechas vacías de las partes · E39 feriados 2027 · E40 inscripción proyectada. A la USS: U56 (códigos 2027), U57 (quién hace cada paso) y U58 (partes y mallas de las jefaturas).

### ¿Qué sigue después de crear el periodo en la Capacidad 1?
En el orden de los instructivos: SSAEXCL (feriados) › STVMAJR, SMAPRLE y SOACURR (programa, 1.1.3) › SCACRSE (curso, 1.1.4) › SCADETL, SCAPPRQ y SCARRES (requisitos, 1.1.5 y 1.2.3) › SMAALIB, SMAAREA y SMAPROG (malla, 1.2.1) › copia de área y programa si la malla cambia (1.3.1) › SSASECT (NRC, Capacidad 5.3). Diagrama: `centros/comun/diagramas/02-capacidad-1-ruta-despues-del-periodo/`.

### ¿Dónde están los flujos BPM y las capturas de 202721?
- Paso a paso en TEST (13 pasos, 24 capturas con cuadros y números): `centros/comun/diagramas/01-capacidad-1-periodo-202721/`.
- Lo que sigue (16 pasos, de 1.1.1 a 1.3.1): `centros/comun/diagramas/02-capacidad-1-ruta-despues-del-periodo/`.
- Los datos de los dos están en `centros/comun/datos.json › recorridos`.
