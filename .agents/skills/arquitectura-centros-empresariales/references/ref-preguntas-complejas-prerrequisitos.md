# Preguntas complejas: prerrequisito, correquisito y restricción por programa

Respuestas cortas para el asistente IA y para cualquier agente: qué hace Banner, por qué y con qué prueba (C##) o instructivo. Cada pregunta es un fragmento de la base del asistente. El detalle está en [ref-restricciones-y-prerrequisitos-por-programa.md](ref-restricciones-y-prerrequisitos-por-programa.md) y en el registro (C156 a C170).

### ¿Se puede poner el curso del centro (por ejemplo Basic I) como correquisito de un curso de pregrado (por ejemplo Anatomía I)?
**No.** El correquisito (SCADETL) obliga a llevar los dos cursos **en el mismo periodo** (instructivo 1.1.5, diap. 8 y 21; R22, R24). Pregrado usa periodos que terminan en 44 (202644) y los centros en 54 (202654); los centros tienen periodos propios (ADR-005). Por eso Nidia Beltrán indicó el **prerrequisito restrictivo en SCAPPRQ** (C159). Ellucian explorará un mismo periodo o partes de periodo (C168), pero choca con el ADR-005 y lo decide la USS (U51).

### ¿Cómo se exige la acreditación del centro para matricularse en un curso de pregrado?
Con un **prerrequisito restrictivo por programa en SCAPPRQ**: programa de pregrado (por ejemplo Medicina `1PCSP15`) y versión de catálogo. A cada curso del ciclo se le suma el curso del centro: **malla Y ( Basic I O Basic II O Basic III )** (C161). **Sin calificación** basta haberlo cursado; con calificación hay que aprobarlo con esa nota (C159). Banner lo revisa en la **historia académica** cuando se matricula en SFAREGS; no importa en qué periodo se llevó el curso del centro (C170).

### Un alumno está llevando Basic I en un periodo de centros (202656). ¿Puede matricularse en Anatomía I en 202744?
**No**, mientras la casilla **«En progreso»** esté sin marcar en el SOATERM de 202744. Banner ve el Basic I en curso y responde **«Prerequisite In Progress»** (Error fatal); no se guarda (C166, R10). Si Registros marcara «En progreso», el curso en curso contaría como cumplido, pero eso vale para **todos** los prerrequisitos del periodo (decisión pendiente, E31).

### El alumno ya aprobó Basic I, pero Banner no lo deja matricular en el curso de pregrado. ¿Qué reviso?
1. **La parte de la malla:** la regla es «malla **Y** Basic». Si le falta el curso de la malla (por ejemplo `ESEC 00055` para Anatomía I), Banner rechaza igual (C163).
2. **La versión:** Banner usa la versión de SCAPPRQ del **catálogo del alumno** (C170). Lea SCAPPRQ con el periodo de esa versión, no con el de la matrícula (C164).
3. **La historia:** en SHACRSE (ID y periodo vacío) confirme que el Basic esté en la historia, no solo inscrito. Si está en curso, el mensaje es «Prerequisite In Progress» (C166).
4. **La calificación:** si la fila tiene calificación mínima, la nota debe alcanzarla (C159).
El mensaje «Prerequisite and Test Score error» no dice qué fila falló y SSAPREQ del NRC sale vacío (C163).

### ¿Por qué la regla que configuró Nidia no se aplica a los alumnos que ingresaron en 2025 o 2026?
Porque Banner aplica la **versión de SCAPPRQ del catálogo del alumno**, no la del periodo de matrícula. Probado en C170: el alumno `A00010005` (catálogo 202444) no fue bloqueado por una fila de la versión 202644 y sí por una de la 202444. La regla de Nidia está solo en la versión **202444** (de 202444 a 202544) (C162). Hay que copiarla a las versiones **202544** y **202644**.

### ¿Qué diferencia hay entre SCAPREQ, SSAPREQ y SCAPPRQ?
- **SCAPREQ:** prerrequisitos del curso en el catálogo; valen para todos los que llevan el curso (instructivo 1.1.5).
- **SSAPREQ:** prerrequisitos de un NRC.
- **SCAPPRQ:** prerrequisitos por **programa**: el curso exige otro solo a los alumnos de ese programa y versión (C160). No está en los 83 instructivos.
En las pruebas, SSAPREQ del NRC estaba vacío y el bloqueo venía de SCAPPRQ (C163).

### ¿Qué significan «Y», «O» y los paréntesis en una regla de prerrequisitos?
«**Y**» exige las dos filas; «**O**» basta una; la primera fila no lleva conector; los **paréntesis** agrupan filas para que el conector de afuera valga para todo el grupo (instructivo 1.1.5, diap. 18 y 19; R25). Ejemplo: Anatomía I = `ESEC 00055` **Y** ( Basic I **O** Basic II **O** Basic III ): debe tener Bioquímica y además uno de los tres Basic (C161). Con «Y» en lugar de «O» tendría que haber llevado los tres.

### Si el alumno desaprueba Basic I, ¿puede llevar el curso de pregrado?
**Por confirmar con Ellucian** (E31, punto d). Lo dicho en la reunión: sin calificación en la fila basta haber cursado el curso; con calificación hay que aprobarlo con esa nota (C159). Dentro del centro, quien desaprueba Basic I no pasa a Basic II (prerrequisito Fatal, ADR-008).

### ¿Desde qué ciclo de pregrado se exige cada centro?
Según el resumen de Ellucian del 29/10 (C168): desde el **2.º ciclo** al menos un curso de Idiomas; desde el **5.º**, Computación; desde el **7.º**, Emprendimiento. Coincide con la Resolución Rectoral 175-2023 (U42). Falta que la USS defina nivel, cursos y nota (U49). En Computación la ruta es 3 cursos de 6 en cualquier orden (C125): no hay un curso único que exigir.

### ¿Cómo limito un NRC del centro (por ejemplo de una ruta XP) solo a ciertos programas?
**SSARRES** (un NRC) o **SCARRES** (el curso) › Grado y programa › **Incluir** el programa. Requiere **Programa en Fatal** en SOATERM; si está en «No verificar», no bloquea (C149). Quien no tiene el programa sale con «Program Restriction» (C156). También cuenta el currículo de pregrado del alumno (E29, C157).

### ¿Qué mensajes de error salen en la matrícula y qué significan?
- **«Prerequisite and Test Score error»:** no cumple la regla de SCAPPRQ (C163, C165).
- **«Prerequisite In Progress»:** solo cumpliría con un curso que está llevando y «En progreso» está sin marcar (C166).
- **«Program Restriction»:** el NRC está restringido a otros programas (C156).
- **«El estatus "DD" es inválido…»:** la parte de periodo no tiene DD en SFARSTS (C167).

### ¿Cómo pruebo en TEST si el prerrequisito bloquea?
Guía de restricciones, sección 2, pasos 7 a 10 (C165 a C170): fila temporal en SCAPPRQ con el programa y el periodo de la **versión del catálogo del alumno**; matrícula en SFAREGS; leer el mensaje; prueba de control sin la fila; borrar las filas temporales. El agente deja escrito y el usuario pulsa GUARDAR (guía de manejo de TEST de workflow-pruebas-test).

### ¿Se puede dar de baja una matrícula de prueba en 202744?
**No en la parte 1:** SFARSTS solo tiene RE (se ve en SFQRSTS) y un RE no se borra (C158, C167). Registros tendría que agregar DD a esa parte.

### ¿Primero se paga o primero se inscribe en los centros?
En la reunión de la tarde del 29/10 se confirmó que los centros seguirán el flujo de pregrado: **primero paga** (o la primera cuota, según la modalidad) **y luego se inscribe**; falta que Faber valide la configuración (C168, U50). Hoy Banner inscribe sin pago previo (C82).
