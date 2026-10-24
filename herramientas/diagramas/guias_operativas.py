"""Guías operativas paso a paso de los Centros Empresariales USS en Banner Student.

Se inyectan directamente en el modal interactivo (Pasaporte semántico) de Archify
al hacer clic sobre cualquier nodo del flujo en el navegador, adaptadas de forma
100% específica para cada centro (Idiomas, Computación y Emprendimiento).
"""

# ===========================================================================
# 1. CREACIÓN DE NRC (SSASECT / SSASECQ) - POR CENTRO
# ===========================================================================

GUIA_CREAR_NRC_IDIOMAS = {
    "s1": {
        "fase": "Paso 1: Encabezado (Bloque Clave)",
        "pantalla": "SSASECT",
        "hito": "Inicio de proceso · Indicador ADD temporal",
        "instrucciones": [
            {"campo": "Formulario", "valor": "SSASECT", "tipo": "Acceso inicial", "detalle": "Escribir SSASECT en la barra de búsqueda de Banner y presionar Enter."},
            {"campo": "Periodo", "valor": "202656 (o periodo lectivo vigente)", "tipo": "Obligatorio", "detalle": "Ingresar periodo académico (202651: verano, 202654: semestre I, 202656: semestre II)."},
            {"campo": "NRC", "valor": "(DEJAR EN BLANCO)", "tipo": "Obligatorio", "detalle": "Dejar vacío para aperturar una nueva sección en el Centro de Idiomas."},
            {"campo": "Botón de Creación", "valor": "Clic en «Crear NRC»", "tipo": "Acción del sistema", "detalle": "Hacer clic en el botón azul. El campo mostrará temporalmente el indicador ADD."}
        ]
    },
    "s2": {
        "fase": "Paso 2: Información de sección (Centro de Idiomas)",
        "pantalla": "SSASECT",
        "hito": "Primer guardado: NRC generado",
        "instrucciones": [
            {"campo": "Materia", "valor": "ESEP (Estudios de Especialidad)", "tipo": "Obligatorio", "detalle": "Confirmado: Digitar ESEP para cursos del Centro de Idiomas (Inglés y Portugués Posgrado)."},
            {"campo": "Número de curso", "valor": "02458 (Basic III) o 02456 (Basic I)", "tipo": "Obligatorio", "detalle": "Digitar número de curso oficial de catálogo (ej. 02458 Basic III, 02456 Basic I, 02693 Intermediate I)."},
            {"campo": "Sección", "valor": "AT (Teórico) / AC1 (Presencial) / AC2, AC3 (Virtual)", "tipo": "Obligatorio", "detalle": "Regla USS: Sección AT para teoría virtual; AC1 para práctica presencial; AC2 y AC3 para prácticas virtuales."},
            {"campo": "Campus", "valor": "S (Sede de Chiclayo)", "tipo": "Obligatorio", "detalle": "Digitar S o elegir de lista. Corresponde al campus operativo del centro."},
            {"campo": "Estatus", "valor": "A (Activo)", "tipo": "Obligatorio", "detalle": "Seleccionar 'Activo'; indispensable para permitir la posterior matrícula."},
            {"campo": "Tipo de horario", "valor": "TEO (Teórico para AT) / PRA (Práctico para AC1-AC3)", "tipo": "Obligatorio", "detalle": "TEO para el NRC principal teórico; PRA para las secciones prácticas ligadas."},
            {"campo": "Modo de calificar", "valor": "C (Escala Centesimal 00 a 100)", "tipo": "Obligatorio", "detalle": "Confirmado en TEST: Modo C (Escala Centesimal 00 a 100) en catálogo de SSASECT para ESEP 02458 (nota aprobatoria ≥ 70)."},
            {"campo": "Parte de periodo", "valor": "I10 (05-OCT-2026 a 31-DIC-2026 · 13 semanas)", "tipo": "Obligatorio", "detalle": "En «Clase tradicional»: digitar I10 (o grupos I01 a I12 en 2026). Fechas de inicio/fin se calculan automáticamente."},
            {"campo": "Ligas y Cobro", "valor": "AT: TA (con cobro) | AC1-AC3: PA (dispensado)", "tipo": "Regla Crítica", "detalle": "Solo Idiomas usa ligas. En Indicadores de clase: Para AT (Teórico Virtual) marcar Calificable ☑ y desmarcar Dispensa ☐ con Liga TA. Para AC1 (Práctico Presencial en Posgrado) y AC2/AC3 (Prácticos Virtuales) desmarcar Calificable ☐ y marcar Dispensa ☑ con Liga PA."},
            {"campo": "Primer guardado", "valor": "Botón «Guardar» (F10)", "tipo": "Hito Crítico", "detalle": "Obligatorio: Guardar (F10) aquí antes de cambiar de pestaña. El ADD cambia al NRC oficial generado (ej. 10024, 10010, 10001)."}
        ]
    },
    "s3": {
        "fase": "Paso 3: Información de ingreso de sección",
        "pantalla": "SSASECT",
        "hito": "Segundo guardado: Aforo y Reservas",
        "instrucciones": [
            {"campo": "Pestaña Ingreso de sección", "valor": "Clic en pestaña 2", "tipo": "Navegación", "detalle": "Ir a «Información de ingreso de sección» (Enrollment Details)."},
            {"campo": "Aforo Máximo y Proyectado", "valor": "Máximo: 40 | Proyectado: 40", "tipo": "Obligatorio", "detalle": "En subpestaña «Detalles de ingreso»: ingresar 40 en Máximo y 40 en Proyectado (o 25 en salón presencial AC1)."},
            {"campo": "Indicador de Reservado", "valor": "Casilla «Reservado» ☑", "tipo": "Obligatorio", "detalle": "Marcar check Reservado para habilitar la subpestaña «Lugares reservados»."},
            {"campo": "Códigos de Autorización", "valor": "Casilla «Códigos activos» ☑", "tipo": "Control", "detalle": "Verificar marcado para control de permisos de inscripción en la sección."},
            {"campo": "Créditos Generados", "valor": "AT: 4.000 cr | AC1-AC3: 0.000 cr", "tipo": "Control Cobro", "detalle": "La teoría genera 4 créditos; las prácticas asociadas generan 0 créditos por estar dispensadas."},
            {"campo": "Subpestaña Lugares Reservados", "valor": "Regla nula (0) + Regla Centro (40)", "tipo": "Blindaje", "detalle": "En subpestaña «Lugares reservados»: Fila 1 regla NULL con cupo 0; Fila 2 regla por programa IMEMI03 con Máximo reservado: 40."},
            {"campo": "Segundo guardado", "valor": "Botón «Guardar» (F10)", "tipo": "Hito Crítico", "detalle": "Guardar (F10) para fijar el cupo. Los contadores Total reservado y Restante se actualizan a 40."}
        ]
    },
    "s4": {
        "fase": "Paso 4: Instructor y horas de reunión",
        "pantalla": "SSASECT",
        "hito": "Tercer guardado: Horario, Aula y Docente",
        "instrucciones": [
            {"campo": "Pestaña Horario y reunión", "valor": "Clic en pestaña 3", "tipo": "Navegación", "detalle": "Ir a «Instructor y horas de reunión» (Meeting Times and Faculty)."},
            {"campo": "Fechas de reunión (Horario)", "valor": "Tipo CLAS | 05-OCT-2026 a 26-NOV-2026", "tipo": "Obligatorio", "detalle": "En subpestaña «Fechas de reunión»: tipo CLAS, vigencia de ciclo según parte de periodo I10."},
            {"campo": "Días y Horas según Sección", "valor": "Múltiples opciones reales configuradas:", "tipo": "Opciones TEST", "detalle": "• AT (Teoría 10010): Lunes 18:00–20:30 (SAUVIR)\n• AC1 (Presencial 10011): Martes 20:00–23:20 (SPOSGR A-31)\n• AC2 (Virtual 10013): Sábado 18:00–20:30 (SAUVIR)\n• AC3 (Virtual 10024): Miércoles 08:00–11:20 (SAUVIR)"},
            {"campo": "Créditos y Ubicación", "valor": "Edificio SA / SPOSGR | Tipo PRA / TEO", "tipo": "Obligatorio", "detalle": "En subpestaña «Créditos y ubicación»: Edificio SA / SAUVIR (Virtual) o SPOSGR (Presencial). Horas por semana: 4.00. Créditos sesión: 4.000 para AT y 0.000 para AC1-AC3."},
            {"campo": "Consistencia de Sesión", "valor": "Indicador de sesión: 01 en ambos", "tipo": "Regla Crítica", "detalle": "Regla clave: El campo «Indicador de sesión» del bloque HORARIO debe ser exactamente igual al de INSTRUCTOR (ambos 01)."},
            {"campo": "Docente Asignado (Múltiples)", "valor": "ID Docente | Principal ☑ | 100% resp", "tipo": "Obligatorio", "detalle": "• AT (10010): 100582059 (Dagner Anibal Chuman Lluen)\n• AC1 (10011): S00912435 (Jossymar Cabanillas)\n• AC2 (10013): S00912438 (Arnold Vaca)\n• AC3 (10024): S00912437 (Willy Valverde)\nMarcar Principal ☑, 100% responsabilidad, 100% sesión y carga 4.000 (AT) o 3.000 (AC)."},
            {"campo": "Tercer guardado", "valor": "Botón «Guardar» (F10)", "tipo": "Hito Crítico", "detalle": "Guardar (F10). Mensaje superior Banner: ✓ Saved successfully (1 rows saved)."}
        ]
    },
    "s5": {
        "fase": "Paso 5: Ligas de Sección y Detalle (SSADETL)",
        "pantalla": "SSADETL",
        "hito": "Cuarto guardado: Ligas cruzadas TA ↔ PA",
        "instrucciones": [
            {"campo": "Acceso a SSADETL", "valor": "Menú Relacionados → SSADETL", "tipo": "Navegación", "detalle": "Desde SSASECT, ir a Relacionados → SSADETL (Detalle de horario de sección) con Periodo y NRC."},
            {"campo": "Pestaña Correquisitos y Ligas", "valor": "Subpestaña «Ligas de sección»", "tipo": "Configuración", "detalle": "Ir al bloque inferior donde se define el conector vinculado para armar el bloque de matrícula obligatoria."},
            {"campo": "En NRC Teórico (10010 · TA)", "valor": "Conector vinculado: PA", "tipo": "Enlace TA→PA", "detalle": "El teórico con Identificador TA se enlaza con el conector de liga PA. Exige cualquiera de las prácticas asociadas."},
            {"campo": "En NRCs Prácticos (10011, 10013, 10024 · PA)", "valor": "Conector vinculado: TA", "tipo": "Enlace PA→TA", "detalle": "Cada práctica con Identificador PA se enlaza con el conector TA del curso teórico."},
            {"campo": "Alcance de la Liga", "valor": "Estricto por Materia y Curso", "tipo": "Regla clave", "detalle": "Regla confirmada: La liga solo actúa dentro de la misma materia y curso (ESEP 02458). Puedes reutilizar TA y PA en Basic I, Basic II, Intermedios, etc., sin cruces. Solo se usa TB/PB si dentro del mismo curso abres una segunda teoría (BT)."},
            {"campo": "Cuarto guardado", "valor": "Botón «Guardar» (F10)", "tipo": "Hito Crítico", "detalle": "Guardar (F10) en cada NRC. En SFAREGS, Banner impedirá inscribir el teórico sin su práctica ligada."}
        ]
    },
    "s6": {
        "fase": "Paso 6: Publicación y Auditoría",
        "pantalla": "SSASECQ",
        "hito": "NRC publicado y verificado",
        "instrucciones": [
            {"campo": "Consulta en SSASECQ", "valor": "Transacción SSASECQ", "tipo": "Verificación Final", "detalle": "Entrar a SSASECQ con periodo 202656, materia ESEP y curso 02458 (Basic III)."},
            {"campo": "Confirmación de Secciones", "valor": "4 NRCs activos (10010, 10011, 10013, 10024)", "tipo": "Control de Calidad", "detalle": "Comprobar que figuren visibles la teoría (AT) y las 3 opciones de práctica (AC1 presencial, AC2 y AC3 virtuales), con cupos de 40 y docentes asignados."}
        ]
    }
}

GUIA_CREAR_NRC_COMPUTACION = {
    "s1": {
        "fase": "Paso 1: Encabezado (Bloque Clave)",
        "pantalla": "SSASECT",
        "hito": "Inicio de proceso · Indicador ADD temporal",
        "instrucciones": [
            {"campo": "Formulario", "valor": "SSASECT", "tipo": "Acceso inicial", "detalle": "Escribir SSASECT en la barra de búsqueda de Banner y presionar Enter."},
            {"campo": "Periodo", "valor": "202656 (o periodo lectivo vigente)", "tipo": "Obligatorio", "detalle": "Ingresar periodo (202651: verano, 202654: sem I, 202656: sem II)."},
            {"campo": "NRC", "valor": "(DEJAR EN BLANCO)", "tipo": "Obligatorio", "detalle": "Dejar vacío para aperturar una nueva sección de Computación."},
            {"campo": "Botón de Creación", "valor": "Clic en «Crear NRC»", "tipo": "Acción del sistema", "detalle": "Hacer clic en el botón azul. El campo mostrará temporalmente ADD."}
        ]
    },
    "s2": {
        "fase": "Paso 2: Información de sección (Centro de Computación)",
        "pantalla": "SSASECT",
        "hito": "Primer guardado: NRC generado",
        "instrucciones": [
            {"campo": "Materia", "valor": "ESEC (Estudios Específicos)", "tipo": "Obligatorio", "detalle": "Confirmado: Escribir ESEC en mayúsculas y presionar Tab (materia oficial del Centro de Computación / Informática)."},
            {"campo": "Número de curso", "valor": "00678 (Word 365) / 00679 (Excel 365) / 00650", "tipo": "Obligatorio", "detalle": "Digitar número de curso oficial. El campo Título autocompleta: OFIMÁTICA WORD 365 / OFIMÁTICA EXCEL 365."},
            {"campo": "Sección", "valor": "A (o correlativo: B, C, D...)", "tipo": "Obligatorio", "detalle": "Asignar letra única para la sección del curso (ej. Sección A en NRC 10018 y NRC 10019)."},
            {"campo": "Campus", "valor": "S (Sede Chiclayo)", "tipo": "Obligatorio", "detalle": "Digitar S o elegir de lista. Corresponde al campus operativo del centro."},
            {"campo": "Estatus", "valor": "A (Activo)", "tipo": "Obligatorio", "detalle": "Seleccionar 'Activo'; indispensable para permitir la posterior matrícula."},
            {"campo": "Tipo de horario", "valor": "TEO (Teórico)", "tipo": "Obligatorio", "detalle": "Digitar TEO o derivado del catálogo. El método educativo hereda VIRT."},
            {"campo": "Modo de calificar", "valor": "V (Vigesimal 00 a 20)", "tipo": "Obligatorio", "detalle": "Digitar V (Vigesimal regular 00 a 20). Nota mínima aprobatoria 11 (resuelto U20 en SHAGRDE)."},
            {"campo": "Parte de periodo", "valor": "X06 / X07 (grupos X01 a X07 en 2026)", "tipo": "Obligatorio", "detalle": "En «Clase tradicional»: digitar X06 o X07. Fechas inicio/fin se calculan solas."},
            {"campo": "Ligas", "valor": "(Sin ligas)", "tipo": "Regla", "detalle": "En Computación NO se configuran ligas. El curso se inscribe con su NRC único en sección A con cobro regular."},
            {"campo": "Primer guardado", "valor": "Botón «Guardar» (F10)", "tipo": "Hito Crítico", "detalle": "Obligatorio: Guardar (F10) aquí antes de cambiar de pestaña. El ADD cambia al NRC oficial (ej. 10018, 10019, 1026)."}
        ]
    },
    "s3": {
        "fase": "Paso 3: Definir el cupo",
        "pantalla": "SSASECT",
        "hito": "Segundo guardado: Cupo proyectado",
        "instrucciones": [
            {"campo": "Pestaña Ingreso de sección", "valor": "Clic en pestaña 2", "tipo": "Navegación", "detalle": "Ir a «Información de ingreso de sección» (Enrollment Details)."},
            {"campo": "Detalles de ingreso", "valor": "Subpestaña «Detalles de ingreso»", "tipo": "Navegación", "detalle": "Ubicar el campo «Proyectado» dentro de la información de ingreso de sección."},
            {"campo": "Proyectado", "valor": "40", "tipo": "Obligatorio", "detalle": "Escriba el cupo proyectado del NRC (ejemplo: 40). Es obligatorio y debe llenarse antes de abrir «Lugares reservados» (C97)."},
            {"campo": "Segundo guardado", "valor": "Botón «Guardar» (F10)", "tipo": "Hito Crítico", "detalle": "Guardar (F10) para registrar el cupo proyectado antes de configurar reservas."}
        ]
    },
    "s4": {
        "fase": "Paso 4: Lugares reservados",
        "pantalla": "SSASECT",
        "hito": "Tercer guardado: Reservas activas",
        "instrucciones": [
            {"campo": "Subpestaña Lugares reservados", "valor": "SSASECT → Información de ingreso de sección", "tipo": "Navegación", "detalle": "Abrir la subpestaña «Lugares reservados». No se configura en SSARRES: ese formulario es para restricciones de matrícula."},
            {"campo": "Regla nula", "valor": "Máximo reservado: 0", "tipo": "Regla base", "detalle": "Conservar la fila sin criterio y dejar su Máximo reservado en 0 cuando toda la capacidad se reserva mediante la regla específica."},
            {"campo": "Añadir regla", "valor": "Botón +", "tipo": "Acción", "detalle": "Presionar + para añadir una fila de reserva y elegir el criterio requerido: nivel, campus, escuela, grado, programa, tipo o código de campo de estudio, departamento, currículos, clase, atributo, cohorte, período de admisión o período de matrícula."},
            {"campo": "Ejemplo de criterio", "valor": "Programa: CMEMC38", "tipo": "Ejemplo Computación", "detalle": "Si la reserva es exclusiva para Computación, seleccionar Programa y CMEMC38. También se puede reservar por los demás criterios disponibles en esta pantalla."},
            {"campo": "Máximo reservado", "valor": "40", "tipo": "Obligatorio", "detalle": "En la fila añadida escribir el máximo reservado. Para el ejemplo: 40; Total reservado y Restante se actualizan a 40."},
            {"campo": "Tercer guardado", "valor": "Botón «Guardar» (F10)", "tipo": "Hito Crítico", "detalle": "Guardar (F10) las reglas de reserva antes de continuar con horario y docente."}
        ]
    },
    "s5": {
        "fase": "Paso 5: Horario, Aula y Docente",
        "pantalla": "SSASECT",
        "hito": "Cuarto guardado: Horario y Docente",
        "instrucciones": [
            {"campo": "Pestaña Horario y reunión", "valor": "Clic en pestaña 3", "tipo": "Navegación", "detalle": "Ir a «Instructor y horas de reunión»."},
            {"campo": "Horario (Días y Horas)", "valor": "Tipo CLAS | Formato 24h", "tipo": "Obligatorio", "detalle": "Ejemplo: Martes 08:00 AM – 09:40 AM (Word) o Miércoles 07:40 PM – 09:20 PM (Excel)."},
            {"campo": "Ubicación (Edificio y Aula)", "valor": "Edificio SAUVIR | Salón SALA-VIRT", "tipo": "Obligatorio", "detalle": "Aula virtual oficial del campus S."},
            {"campo": "Indicador de sobrepaso (horario)", "valor": "O", "tipo": "Regla clave", "detalle": "Con el aula virtual, ponga siempre la letra O: todos los NRC comparten SAUVIR / SALA-VIRT y, sin ella, Banner muestra «Conflicto de salón» (C97)."},
            {"campo": "Consistencia de Sesión", "valor": "Indicador de sesión: 01", "tipo": "Regla Crítica", "detalle": "Regla clave: El indicador de sesión de HORARIO debe ser idéntico al de INSTRUCTOR (ambos 01)."},
            {"campo": "Docente Principal", "valor": "ID 100582059 (Dagner Chuman) | Principal ☑ | 100%", "tipo": "Obligatorio", "detalle": "Digitar ID institucional, marcar Principal y colocar 100% responsabilidad."},
            {"campo": "Cuarto guardado", "valor": "Botón «Guardar» (F10)", "tipo": "Hito Crítico", "detalle": "Guardar (F10). Mensaje verde: ✓ Saved successfully. NRC listo con horario y profesor."}
        ]
    },
    "s6": {
        "fase": "Paso 6: Publicación y Auditoría",
        "pantalla": "SSASECQ",
        "hito": "NRC publicado y verificado",
        "instrucciones": [
            {"campo": "Consulta en SSASECQ", "valor": "Transacción SSASECQ", "tipo": "Verificación Final", "detalle": "Entrar a SSASECQ con periodo 202656, materia ESEC y curso (00678 / 00679 / 00650)."},
            {"campo": "Confirmación de Estado", "valor": "Activo (A) | Horario visible | Vacante libre", "tipo": "Control de Calidad", "detalle": "Confirmar que figure Activo (A), horario visible y vacante disponible sin bloqueos."}
        ]
    }
}

GUIA_CREAR_NRC_EMPRENDIMIENTO = {
    "s1": {
        "fase": "Paso 1: Encabezado (Bloque Clave)",
        "pantalla": "SSASECT",
        "hito": "Inicio de proceso · Indicador ADD temporal",
        "instrucciones": [
            {"campo": "Formulario", "valor": "SSASECT", "tipo": "Acceso inicial", "detalle": "Escribir SSASECT en la barra de búsqueda de Banner y presionar Enter."},
            {"campo": "Periodo", "valor": "202656 (o periodo lectivo vigente)", "tipo": "Obligatorio", "detalle": "Ingresar periodo (202651: verano, 202654: sem I, 202656: sem II)."},
            {"campo": "NRC", "valor": "(DEJAR EN BLANCO)", "tipo": "Obligatorio", "detalle": "Dejar vacío para aperturar una nueva sección de Emprendimiento."},
            {"campo": "Botón de Creación", "valor": "Clic en «Crear NRC»", "tipo": "Acción del sistema", "detalle": "Hacer clic en el botón azul. El campo mostrará temporalmente ADD."}
        ]
    },
    "s2": {
        "fase": "Paso 2: Información de sección (Centro de Emprendimiento)",
        "pantalla": "SSASECT",
        "hito": "Primer guardado: NRC generado",
        "instrucciones": [
            {"campo": "Materia", "valor": "ESGE (Estudios Generales - Emprendimiento)", "tipo": "Obligatorio", "detalle": "Confirmado: Escribir ESGE en mayúsculas y presionar Tab (materia oficial del Centro de Emprendimiento)."},
            {"campo": "Número de curso", "valor": "00117 (Emprendimiento I) / 00118 (II) / 00119 (III)", "tipo": "Obligatorio", "detalle": "Digitar número de curso oficial (00117, 00118 o 00119) y presionar Tab. El campo Título autocompleta desde el catálogo."},
            {"campo": "Sección", "valor": "A (o correlativo: B, C...)", "tipo": "Obligatorio", "detalle": "Asignar letra única para la sección del periodo (ej. Sección A en NRC 10007, 10012, 10014)."},
            {"campo": "Campus", "valor": "S (Sede Chiclayo)", "tipo": "Obligatorio", "detalle": "Digitar S o elegir de lista. Campus operativo del centro."},
            {"campo": "Estatus", "valor": "A (Activo)", "tipo": "Obligatorio", "detalle": "Seleccionar 'Activo'; indispensable para permitir la posterior matrícula."},
            {"campo": "Tipo de horario", "valor": "TEO (Teórico)", "tipo": "Obligatorio", "detalle": "Digitar TEO o derivado del catálogo."},
            {"campo": "Modo de calificar", "valor": "V (Vigesimal 00 a 20)", "tipo": "Obligatorio", "detalle": "Digitar V (Vigesimal regular 00 a 20). Nota mínima aprobatoria 11 según plan curricular institucional."},
            {"campo": "Parte de periodo", "valor": "P01 a P06 (duración fija de 10 semanas)", "tipo": "Obligatorio", "detalle": "En «Clase tradicional»: digitar grupo P01 a P06 (ej. P06). Todos los grupos de Emprendimiento duran 10 semanas fijas (P02 y P03 se superponen)."},
            {"campo": "Ligas", "valor": "(Sin ligas)", "tipo": "Regla", "detalle": "En Emprendimiento NO se configuran ligas. El curso se inscribe con su NRC único en sección A con cobro regular."},
            {"campo": "Primer guardado", "valor": "Botón «Guardar» (F10)", "tipo": "Hito Crítico", "detalle": "Obligatorio: Guardar (F10) aquí antes de cambiar de pestaña. El ADD cambia al NRC oficial (ej. 10007, 10012, 10014, 1025)."}
        ]
    },
    "s3": {
        "fase": "Paso 3: Aforo de sección",
        "pantalla": "SSASECT",
        "hito": "Segundo guardado: Cupos confirmados",
        "instrucciones": [
            {"campo": "Pestaña Ingreso de sección", "valor": "Clic en pestaña 2", "tipo": "Navegación", "detalle": "Ir a «Información de ingreso de sección» (Enrollment Details)."},
            {"campo": "Máximo (Cupos del aula)", "valor": "40 (o aforo aula: 30, 35)", "tipo": "Obligatorio", "detalle": "Ingresar cantidad autorizada de vacantes para el NRC."},
            {"campo": "Segundo guardado", "valor": "Botón «Guardar» (F10)", "tipo": "Hito Crítico", "detalle": "Guardar (F10) para fijar el cupo."}
        ]
    },
    "s4": {
        "fase": "Paso 4: Horario, Aula y Docente",
        "pantalla": "SSASECT",
        "hito": "Tercer guardado: Horario y Docente",
        "instrucciones": [
            {"campo": "Pestaña Horario y reunión", "valor": "Clic en pestaña 3", "tipo": "Navegación", "detalle": "Ir a «Instructor y horas de reunión»."},
            {"campo": "Horario (Días y Horas)", "valor": "Tipo CLAS | Formato 24h", "tipo": "Obligatorio", "detalle": "Definir días y horas de la sesión según cronograma de 10 semanas."},
            {"campo": "Ubicación (Edificio y Aula)", "valor": "Edificio SAUVIR | Salón SALA VIRT.", "tipo": "Obligatorio", "detalle": "Usar aula virtual oficial SAUVIR."},
            {"campo": "Consistencia de Sesión", "valor": "Indicador de sesión: 01", "tipo": "Regla Crítica", "detalle": "Indicador de sesión de Horario idéntico al de Instructor."},
            {"campo": "Docente Asignado", "valor": "ID Docente | Principal ☑ | 100%", "tipo": "Obligatorio", "detalle": "ID activo en SIAINST con 100% responsabilidad."},
            {"campo": "Tercer guardado", "valor": "Botón «Guardar» (F10)", "tipo": "Hito Crítico", "detalle": "Guardar (F10). NRC listo con horario y profesor."}
        ]
    },
    "s5": {
        "fase": "Paso 5: Reserva de cupos (SSARRES)",
        "pantalla": "SSARRES",
        "hito": "Cuarto guardado: Reservas activas",
        "instrucciones": [
            {"campo": "Lugares Reservados", "valor": "Menú Relacionado → SSARRES", "tipo": "Navegación", "detalle": "Subpestaña «Lugares reservados» para blindar cupos."},
            {"campo": "Regla Nula (Cupo General)", "valor": "Regla NULL | Cupo: 1", "tipo": "Mandatorio institucional", "detalle": "Asegura cupo general."},
            {"campo": "Regla por Nivel M", "valor": "Nivel: M (Emprendimiento)", "tipo": "Condicional CCEE", "detalle": "Reserva de cupos para estudiantes del nivel M."},
            {"campo": "Cuarto guardado", "valor": "Botón «Guardar» (F10)", "tipo": "Hito Crítico", "detalle": "Guardar reservas (F10)."}
        ]
    },
    "s6": {
        "fase": "Paso 6: Publicación y Auditoría",
        "pantalla": "SSASECQ",
        "hito": "NRC publicado y verificado",
        "instrucciones": [
            {"campo": "Consulta en SSASECQ", "valor": "Transacción SSASECQ", "tipo": "Verificación Final", "detalle": "Entrar a SSASECQ con periodo 202656, materia ESGE y curso 00117."},
            {"campo": "Confirmación de Estado", "valor": "Activo (A) | Horario visible | Vacante libre", "tipo": "Control de Calidad", "detalle": "Confirmar que figure Activo (A)."}
        ]
    }
}

# ===========================================================================
# 2. LIGAS: TEÓRICO + CLUB DE CONVERSACIÓN (SSASECT / SSADETL / SFAREGS)
# ===========================================================================

GUIA_LIGAS = {
    "g1": {
        "fase": "Paso 1: Catálogo y Horarios (SCACRSE)",
        "pantalla": "SCACRSE",
        "hito": "Asignatura configurada con Teoría y Práctica en el catálogo",
        "instrucciones": [
            {"campo": "Formulario", "valor": "SCACRSE", "tipo": "Catálogo base", "detalle": "Comprobar que el curso de Idiomas (ej. ESEP 02456 BASIC I, 02457 BASIC II, 02458 BASIC III) tenga dos tipos de horario: TEO (Teoría) y PRA (Práctica)."},
            {"campo": "Créditos y Horas", "valor": "HT: 4 | HP: 3 | 4 Créditos", "tipo": "Estructura académica", "detalle": "La teoría concentra la carga académica evaluable; la práctica es el espacio complementario de conversación."}
        ]
    },
    "g2": {
        "fase": "Paso 2: NRC Principal Teórico Virtual (SSASECT)",
        "pantalla": "SSASECT",
        "hito": "Sección AT · Liga TA · Calificable ☑ · Sin Dispensa ☐",
        "instrucciones": [
            {"campo": "Encabezado", "valor": "Periodo 202656 | Materia ESEP | Curso 02458", "tipo": "Identificación", "detalle": "Crear sección AT (ej. NRC 10010 de Basic III)."},
            {"campo": "Tipo de horario", "valor": "TEO (Teórico)", "tipo": "Horario principal", "detalle": "Método educativo: VIRT (Virtual). Aula: SAUVIR / SALA-VIRT."},
            {"campo": "Horas y Créditos", "valor": "4.000 créditos / 4.000 cobro", "tipo": "Obligatorio", "detalle": "Lleva los créditos completos de la asignatura."},
            {"campo": "Indicadores de Clase", "valor": "Calificable ☑ | Dispensa ☐", "tipo": "Regla obligatoria", "detalle": "Calificable MARCADO y Dispensa de colegiatura DESMARCADA para liquidar el cobro regular."},
            {"campo": "Identificador de liga", "valor": "TA (Teoría Sección A)", "tipo": "Clave de Liga", "detalle": "Ingresar código TA en campo Identificador de liga de SSASECT. Guardar (F10)."}
        ]
    },
    "g3": {
        "fase": "Paso 3: NRCs Secundarios Prácticos (SSASECT)",
        "pantalla": "SSASECT",
        "hito": "Secciones AC1 (Presencial) y AC2/AC3 (Virtual) · Liga PA · No Calificable ☐ · Dispensa ☑",
        "instrucciones": [
            {"campo": "Segundo curso (AC1)", "valor": "Presencial y Práctico (SPOSGR)", "tipo": "Regla Institucional", "detalle": "Regla confirmada: El segundo curso (sección AC1, ej. 10011) es PRESENCIAL en aulas de Posgrado (SPOSGR A-21 / A-11 / A-31)."},
            {"campo": "Resto de cursos (AC2, AC3)", "valor": "Virtual y Práctico (SAUVIR)", "tipo": "Regla Institucional", "detalle": "Regla confirmada: Las demás secciones de práctica (AC2, AC3, ej. 10013, 10024) son VIRTUALES en SAUVIR SALA-VIRT."},
            {"campo": "Tipo de horario", "valor": "PRA (Práctico)", "tipo": "Horario secundario", "detalle": "Asignado a las sesiones de práctica / club de conversación."},
            {"campo": "Créditos y Cobro", "valor": "0 créditos (o con dispensa)", "tipo": "Configuración", "detalle": "Horas crédito y cobro con dispensa para no duplicar el costo de la matrícula."},
            {"campo": "Indicadores de Clase", "valor": "Calificable ☐ | Dispensa ☑", "tipo": "Regla obligatoria", "detalle": "Calificable DESMARCADO y Dispensa de colegiatura y cuotas MARCADA."},
            {"campo": "Identificador de liga", "valor": "PA (Práctica Sección A)", "tipo": "Clave de Liga", "detalle": "Ingresar código PA en campo Identificador de liga de SSASECT. Guardar (F10)."}
        ]
    },
    "g4": {
        "fase": "Paso 4: Vinculación Bidireccional (SSADETL)",
        "pantalla": "SSADETL",
        "hito": "Vinculación completa en ambos sentidos",
        "instrucciones": [
            {"campo": "Acceso", "valor": "Menú Relacionados → SSADETL", "tipo": "Navegación", "detalle": "Desde SSASECT ir a SSADETL con el periodo y el NRC cargado."},
            {"campo": "Pestaña", "valor": "Correquisitos y ligas de sección", "tipo": "Configuración", "detalle": "Ir a la pestaña 2 de SSADETL."},
            {"campo": "En el NRC Teórico (TA)", "valor": "Conector de liga: PA", "tipo": "Enlace", "detalle": "En el NRC de Teoría (ej. 10010), colocar PA en el campo Conector de liga y Guardar (F10)."},
            {"campo": "En los NRC Prácticos (PA)", "valor": "Conector de liga: TA", "tipo": "Enlace", "detalle": "En cada NRC de Práctica (ej. 10011, 10013, 10024), colocar TA en Conector de liga y Guardar (F10)."},
            {"campo": "Escenario", "valor": "Muchos a muchos con restricción", "tipo": "Lógica", "detalle": "Al elegir el teórico sección AT (TA), el estudiante debe escoger obligatoriamente una de las prácticas PA (AC1 presencial o AC2/AC3 virtual)."}
        ]
    },
    "g5": {
        "fase": "Paso 5: Inscripción Conjunta Obligatoria",
        "pantalla": "SFAREGS / Web",
        "hito": "Matrícula exigida de Teórico + Práctico juntos",
        "instrucciones": [
            {"campo": "Control SOATERM", "valor": "Verificación Ligas en Fatal", "tipo": "Restricción", "detalle": "Banner bloquea la inscripción si el alumno solo ingresa el teórico sin su práctica ligada."},
            {"campo": "Inscripción Backoffice", "valor": "Digitar Teórico + Práctico (código RE)", "tipo": "Inscripción", "detalle": "Ingresar en SFAREGS el NRC teórico (ej. 10010) junto al práctico seleccionado (ej. 10011 o 10024) y Guardar (F10)."},
            {"campo": "Autoservicio Web", "valor": "Panel «Secciones ligadas»", "tipo": "Autoservicio", "detalle": "El alumno marca su clase teórica y el autoservicio le despliega para elegir el grupo de práctica correspondiente."},
            {"campo": "Tasación", "valor": "Estimación de cuota procesada", "tipo": "Financiero", "detalle": "Solo se liquidan los 4 créditos del NRC teórico principal; la práctica queda dispensada."}
        ]
    },
    "g6": {
        "fase": "Paso 6: Participante Matriculado",
        "pantalla": "SFASLST / SSASECT",
        "hito": "Alumno matriculado en ambos NRC",
        "instrucciones": [
            {"campo": "Estado de Matrícula", "valor": "Estatus RE en ambos NRCs", "tipo": "Verificación", "detalle": "El estudiante figura formalmente matriculado en la teoría y en su grupo práctico."},
            {"campo": "Listas de Clase (SFASLST)", "valor": "Listas docentes independientes", "tipo": "Académico", "detalle": "Docente de teoría evalúa la nota final; docente de práctica supervisa asistencia y avance."},
            {"campo": "Aforo SSASECT", "valor": "Vacantes descontadas en ambos", "tipo": "Control", "detalle": "El contador Actual suma 1 y Remaining resta 1 en cada sección involucrada."}
        ]
    }
}

# ===========================================================================
# 3. CARGA LECTIVA (SIAINST / SSASECT / SIAASGN / INTRANET USS)
# ===========================================================================

GUIA_CARGA_LECTIVA = {
    "k1": {
        "fase": "Paso 1: Activación y Habilitación Docente",
        "pantalla": "SIAINST",
        "hito": "Docente activo en facultad y periodo",
        "instrucciones": [
            {"campo": "Formulario", "valor": "SIAINST", "tipo": "Acceso inicial", "detalle": "Ingresar ID del docente (ej. 100582059 Dagner Chuman) y verificar estatus en facultad."},
            {"campo": "Pestaña Facultad", "valor": "Status: Activo", "tipo": "Obligatorio", "detalle": "Comprobar que el docente tenga permisos vigentes para dictado en el periodo lectivo."},
            {"campo": "Contrato Docente", "valor": "ES (Especialista) / FC (Facilitador)", "tipo": "Régimen CCEE", "detalle": "Régimen docente confirmado: Especialista ES (48h/sem con funciones administrativas) o Facilitador FC (14 a 23h/sem)."}
        ]
    },
    "k2": {
        "fase": "Paso 2: Asignación al NRC",
        "pantalla": "SSASECT",
        "hito": "Docente principal asignado al 100%",
        "instrucciones": [
            {"campo": "Formulario", "valor": "SSASECT", "tipo": "Programación", "detalle": "En pestaña Horario e instructores, asignar ID con sesión 01 y 100% responsabilidad."},
            {"campo": "Indicador Principal", "valor": "Casilla Principal ☑", "tipo": "Obligatorio", "detalle": "Marcar como instructor principal para emisión de actas oficiales."},
            {"campo": "Sobrepaso de Horario", "valor": "Indicador de sobrepaso ☑", "tipo": "Contingencia", "detalle": "Si el docente tiene otro NRC a la misma hora, marcar sobrepaso para salvar el cruce."}
        ]
    },
    "k3": {
        "fase": "Paso 3: Auditoría de Carga Docente",
        "pantalla": "SIAASGN",
        "hito": "Horas y FTE computados automáticamente",
        "instrucciones": [
            {"campo": "Formulario", "valor": "SIAASGN", "tipo": "Auditoría", "detalle": "Consultar con Periodo 202656 e ID del docente (100582059 Dagner Chuman)."},
            {"campo": "Secciones asignadas", "valor": "Carga consolidada del periodo", "tipo": "Consolidación", "detalle": "Auditoría de todas las secciones asignadas al docente en el periodo."},
            {"campo": "Horas semanales", "valor": "Calculadas según factor SIATERM", "tipo": "Cálculo", "detalle": "Multiplicación de horas y factor de duración institucional de SIATERM."},
            {"campo": "Horas acumuladas", "valor": "Cómputo total del periodo", "tipo": "Cálculo", "detalle": "Cómputo acumulado de la carga lectiva total del periodo."},
            {"campo": "Asignación de FTE", "valor": "FTE generado automáticamente", "tipo": "Cálculo", "detalle": "Factor de dedicación académica generado automáticamente sustituyendo planillas Excel."}
        ]
    },
    "k4": {
        "fase": "Paso 4: Visto Bueno del Centro",
        "pantalla": "Intranet USS",
        "hito": "Oficio institucional tramitado",
        "instrucciones": [
            {"campo": "Trámite", "valor": "Oficio del Jefe de Centro", "tipo": "Administrativo", "detalle": "El jefe de centro valida la carga lectiva y genera oficio con asunto, detalle y adjunto en la intranet USS."}
        ]
    },
    "k5": {
        "fase": "Paso 5: Aprobación Oficial",
        "pantalla": "Resolución VRA",
        "hito": "Resolución de carga docente aprobada",
        "instrucciones": [
            {"campo": "Aprobación", "valor": "Resolución Vicerrectoral", "tipo": "Oficial", "detalle": "El Vicerrectorado Académico revisa y emite la resolución formal de aprobación de carga."}
        ]
    }
}

# ===========================================================================
# 4. PERSONA Y ADMISIÓN (GOAMTCH / SAAQUIK / SGASTDN) - POR CENTRO
# ===========================================================================

def obtener_guia_persona_admision(id_centro):
    prog = "IMEMI03 (Acreditación Idiomas)" if id_centro == "idiomas" else ("CMEMC38 (Computación)" if id_centro == "computacion" else "Programa de Emprendimiento")
    dept = "EMID (Idiomas)" if id_centro == "idiomas" else ("EMCI (Computación)" if id_centro == "computacion" else "Escuela EM")
    mayor = "MI03-01 / MI03-02" if id_centro == "idiomas" else ("ACXP (Malla MC38-01)" if id_centro == "computacion" else "Emprendimiento")
    nivel = "I (Idiomas)" if id_centro == "idiomas" else ("C (Computación)" if id_centro == "computacion" else "M (Emprendimiento)")

    return {
        "a1": {
            "fase": "Paso 1: Búsqueda de Coincidencias",
            "pantalla": "GOAMTCH",
            "hito": "Verificación de homónimos y duplicados",
            "instrucciones": [
                {"campo": "Formulario", "valor": "GOAMTCH", "tipo": "Acceso inicial", "detalle": "Ingresar a GOAMTCH con ID GENERATED."},
                {"campo": "Origen coincidencia", "valor": "PERS_NATU", "tipo": "Obligatorio", "detalle": "Seleccionar Persona Natural para aplicar filtros de búsqueda de documento de identidad."},
                {"campo": "Búsqueda DNI", "valor": "DNI y Apellidos", "tipo": "Control", "detalle": "Clic en «Marcar-Duplicar» para verificar si la persona ya existe en Banner."}
            ]
        },
        "a2": {
            "fase": "Paso 2: Creación de Persona e Identificación",
            "pantalla": "GOAMTCH",
            "hito": "Generación de ID oficial (ej. S00581081)",
            "instrucciones": [
                {"campo": "Creación nueva", "valor": "Clic en «Crear nuevo»", "tipo": "Acción", "detalle": "Si no existe duplicado, generar ID institucional con prefijo S."},
                {"campo": "Dirección", "valor": "Tipo PP (Permanente)", "tipo": "Obligatorio", "detalle": "Registrar dirección permanente del estudiante."},
                {"campo": "Teléfono", "valor": "Tipo MOV (Móvil)", "tipo": "Obligatorio", "detalle": "Registrar número de teléfono móvil para contacto institucional."},
                {"campo": "Correo", "valor": "Tipo PER1 (Personal)", "tipo": "Obligatorio", "detalle": "Registrar correo electrónico personal y guardar (F10)."}
            ]
        },
        "a3": {
            "fase": f"Paso 3: Admisión Rápida (Nivel {nivel})",
            "pantalla": "SAAQUIK",
            "hito": "Inicio de admisión rápida en el centro",
            "instrucciones": [
                {"campo": "Formulario", "valor": "SAAQUIK", "tipo": "Acceso", "detalle": "Ingresar ID generado y Periodo lectivo (202656)."},
                {"campo": "Parámetros base", "valor": f"Nivel {nivel} · Campus S · Escuela EM", "tipo": "Obligatorio", "detalle": f"Nivel {nivel}; Campus S (Chiclayo); Escuela EM (Centros Empresariales); Grado 000000."}
            ]
        },
        "a4": {
            "fase": "Paso 4: Asignación de Programa Curricular",
            "pantalla": "SAAQUIK",
            "hito": f"Programa {prog} activo",
            "instrucciones": [
                {"campo": "Programa", "valor": prog, "tipo": "Obligatorio", "detalle": f"Seleccionar {prog}; autocompleta Departamento {dept} y Mayor {mayor}."},
                {"campo": "Guardar", "valor": "Guardar (F10)", "tipo": "Transacción", "detalle": "Mensaje verde: 3 rows saved. Registro admitido exitosamente."}
            ]
        },
        "a5": {
            "fase": "Paso 5: Auditoría General de Alumno",
            "pantalla": "SGASTDN",
            "hito": "Expediente activo (AS) listo para matrícula",
            "instrucciones": [
                {"campo": "Formulario", "valor": "SGASTDN", "tipo": "Auditoría", "detalle": "Consultar ID en SGASTDN con periodo vigente."},
                {"campo": "Estatus académico", "valor": "Status: AS (Activo)", "tipo": "Verificación", "detalle": "Confirmar que figure Activo y con currícula vigente sin bloqueos."}
            ]
        }
    }

# ===========================================================================
# 5. MATRÍCULA EN EL NRC (SFAREGS / TSAAREV / SFASLST)
# ===========================================================================

def obtener_guia_matricula(id_centro):
    nrc_desc = "NRC Teórico AT + NRC Práctico AC1/AC3" if id_centro == "idiomas" else ("NRC oficial de Computación (ej. 10018 / 1026)" if id_centro == "computacion" else "NRC oficial de Emprendimiento (ej. 1025)")

    return {
        "i1": {
            "fase": "Paso 1: Consulta Previa de Vacantes",
            "pantalla": "SSASECQ",
            "hito": "Verificación de cupo disponible",
            "instrucciones": [
                {"campo": "Formulario", "valor": "SSASECQ", "tipo": "Consulta", "detalle": "Ingresar periodo 202656, materia y NRC para comprobar vacantes en Remaining."}
            ]
        },
        "i2": {
            "fase": "Paso 2: Autorización Curricular",
            "pantalla": "SFAREGS",
            "hito": "Plan autorizado con estatus elegible (EL)",
            "instrucciones": [
                {"campo": "Encabezado", "valor": "Periodo → ID del alumno → plan de estudios", "tipo": "Bloque clave", "detalle": "Ingrese primero el periodo (202656), luego el ID y al final el plan de estudios; pulse «Ir». Si el plan se ingresa antes, puede aparecer «no existe la tabla o vista» (C86)."},
                {"campo": "Plan de estudios de ingreso", "valor": "Plan del programa del alumno · estatus EL", "tipo": "Obligatorio", "detalle": "No asuma que el plan es 1. Si el alumno no tiene currículo del nivel del curso, agréguelo en la pestaña «Currículos» (+, programa, Tab, Guardar) (C100). Guarde."}
            ]
        },
        "i3": {
            "fase": "Paso 3: Inscripción en el NRC",
            "pantalla": "SFAREGS",
            "hito": "Inscripción regular (código RE)",
            "instrucciones": [
                {"campo": "Información de curso", "valor": nrc_desc, "tipo": "Obligatorio", "detalle": "En bloque Course Registration, digitar el o los NRCs según corresponda (en Idiomas ingresar Teórico + Práctico juntos por regla de ligas)."},
                {"campo": "Código de estatus", "valor": "RE (Web / Backoffice Registered)", "tipo": "Obligatorio", "detalle": "Digite RE y guarde. Mensaje esperado: «Estimación de cuota procesada»."},
                {"campo": "Nivel del curso", "valor": "Debe coincidir con el currículo (C para Computación)", "tipo": "Control", "detalle": "Si choca con el horario de otro NRC del alumno, Banner muestra conflicto: ajuste el horario o elija otro NRC."}
            ]
        },
        "i4": {
            "fase": "Paso 4: Auditoría Financiera",
            "pantalla": "TSAAREV",
            "hito": "Cargos y cuotas aplicados correctamente",
            "instrucciones": [
                {"campo": "Formulario", "valor": "TSAAREV", "tipo": "Cobranzas", "detalle": "Consultar cuenta corriente del alumno para verificar la tasación automática del curso."}
            ]
        },
        "i5": {
            "fase": "Paso 5: Lista Oficial de Clase",
            "pantalla": "SFASLST",
            "hito": "Alumno matriculado en lista del docente",
            "instrucciones": [
                {"campo": "Formulario", "valor": "SFASLST", "tipo": "Verificación", "detalle": "Abrir lista de clase con periodo y NRC; confirmar que el alumno figure como matriculado."}
            ]
        }
    }

# ===========================================================================
# 6. NOTAS Y PASE A HISTORIA (SHAGRDE / SFASLST / GJAPCTL / CAPP)
# ===========================================================================

def obtener_guia_notas(id_centro):
    """Flujo probado en TEST con el NRC 10044 (Computación, 23–24/10/2026): C91, C97–C107."""
    comp = id_centro == "computacion"
    periodo = "202656"
    nrc = "10044" if comp else "(NRC del centro)"
    escala = "VIG_11 (aprobatoria 55 de 100, equivale a 11)" if comp else "Escala regular del centro (por confirmar)"
    escala_asist = "AST_70 (aprobatoria 70)" if comp else "Escala de asistencia con el mínimo institucional (70 %)"

    return {
        "n1": {
            "fase": "Paso 1: Calendario de calificaciones",
            "pantalla": "SHAEGBC",
            "hito": "Fechas de ingreso de notas abiertas para el periodo",
            "instrucciones": [
                {"campo": "Periodo", "valor": periodo, "tipo": "Bloque clave", "detalle": "Ingrese el periodo y pulse «Ir»."},
                {"campo": "Fecha abierta para puntaje", "valor": "Fecha autorizada por Registros Académicos", "tipo": "Obligatorio", "detalle": "Use las fechas institucionales; no las invente. En TEST se vio 01-SEP-2026 (C92)."},
                {"campo": "Fecha de corte", "valor": "Fecha autorizada", "tipo": "Obligatorio", "detalle": "Guarde. Sin este calendario, SHAGCOM muestra «Debe configurar los controles del libro de calificaciones en SHAEGBC» (C91)."},
            ]
        },
        "n2": {
            "fase": "Paso 2: Plan de evaluación del NRC",
            "pantalla": "SHAGCOM",
            "hito": "Componentes con peso final 1.00 y ATTRGRD aparte",
            "instrucciones": [
                {"campo": "Periodo y NRC", "valor": f"{periodo} · {nrc}", "tipo": "Bloque clave", "detalle": "Ingrese periodo y NRC y pulse «Ir»."},
                {"campo": "Escala de calificación (bloque superior)", "valor": escala.split(" (")[0], "tipo": "Obligatorio", "detalle": "Es la escala que predomina en los componentes (7.1.4, diap. 44). Guarde antes de pasar al bloque de componentes."},
                {"campo": "Componentes del sílabo", "valor": "TA1 0.15 · TA2 0.15 · PA 0.40 · EF 0.30" if comp else "Según el sílabo aprobado", "tipo": "Obligatorio", "detalle": "Secuencia, nombre, descripción, peso, calificadas de 100, incluir en FINAL y escala " + escala + ". La suma de pesos debe ser 1.00."},
                {"campo": "Componente de asistencia", "valor": "ATTRGRD · peso 0.00 · Debe aprobar", "tipo": "Regla institucional", "detalle": "Nombre obligatorio ATTRGRD, escala " + escala_asist + " (7.1.4, diap. 55)."},
                {"campo": "Verificación", "valor": "Total de peso final 1.00", "tipo": "Control", "detalle": "Salga y vuelva a consultar el NRC para confirmar que las filas quedaron guardadas."},
            ]
        },
        "n3": {
            "fase": "Paso 3: Regla de control de asistencia",
            "pantalla": "SOAATRK",
            "hito": "El NRC aparece en «Pasar lista» del docente",
            "instrucciones": [
                {"campo": "Periodo", "valor": periodo, "tipo": "Bloque clave", "detalle": "Ingrese el periodo y pulse «Ir»."},
                {"campo": "Parte, materia, curso y NRC", "valor": "X06 · ESEC · 00684 · 10044" if comp else "Datos del NRC", "tipo": "Obligatorio", "detalle": "La regla puede ser por parte, curso o NRC (7.1.1, diap. 34–38)."},
                {"campo": "Desplegar clase y Control de asistencia", "valor": "Ambas casillas marcadas", "tipo": "Obligatorio", "detalle": "Sin esta regla, el NRC no aparece en el control de asistencia de Autoservicio (C101)."},
                {"campo": "Unidad de control y fechas", "valor": "Presente/Ausente · 07-SEP-2026 a 31-OCT-2026" if comp else "Unidad y fechas de la parte", "tipo": "Obligatorio", "detalle": "Use las fechas de la parte de periodo. Guarde."},
            ]
        },
        "n4": {
            "fase": "Paso 4: Pasar lista",
            "pantalla": "Autoservicio docente",
            "hito": "Porcentaje de asistencia calculado por alumno",
            "instrucciones": [
                {"campo": "Ruta", "valor": "Control de asistencia › Lista de cursos › Pasar lista", "tipo": "Navegación", "detalle": "Seleccione el NRC y la fecha de la sesión."},
                {"campo": "Marca por alumno", "valor": "Presente (✓) o Ausente (−)", "tipo": "Registro", "detalle": "Solo se registran fechas pasadas. Banner calcula el porcentaje de asistencia (7.1.1, diap. 44–48)."},
                {"campo": "Resultado en TEST", "valor": "43 % (prueba de INH)" if comp else "Por probar", "tipo": "Evidencia", "detalle": "Alumno 100582059 en el NRC 10044 (C104)." if comp else "Este centro aún no lo ha probado."},
            ]
        },
        "n5": {
            "fase": "Paso 5: Notas por componente",
            "pantalla": "Autoservicio docente",
            "hito": "Nota compuesta calculada",
            "instrucciones": [
                {"campo": "Ruta", "valor": "Captura de calificaciones › Libro de calificaciones › Componentes", "tipo": "Navegación", "detalle": "Seleccione el NRC; solo aparece si tiene docente, plan y alumnos matriculados (7.1.4, diap. 58)."},
                {"campo": "Puntaje", "valor": "85 de 100 → calificación 17" if comp else "Puntaje sobre 100", "tipo": "Registro", "detalle": "Banner propone la calificación según la escala. Razón: «Captura Original - OE». Guarde cada componente."},
                {"campo": "ATTRGRD", "valor": "Porcentaje de asistencia", "tipo": "Control", "detalle": "Si no llega solo desde Pasar lista, revise GORICCR, GORRSQL y STVGCHG (U32)."},
                {"campo": "Calificaciones compuestas", "valor": "Porcentaje 85 · ATTRGRD 43 → INH" if comp else "Nota final calculada", "tipo": "Resultado", "detalle": "Con asistencia bajo el mínimo, «Debe aprobar» deja la nota final en INH aunque el promedio apruebe (C105)."},
            ]
        },
        "n6": {
            "fase": "Paso 6: Nota final en el backoffice",
            "pantalla": "SFASLST",
            "hito": "La nota del libro pasó a la lista de clase",
            "instrucciones": [
                {"campo": "Periodo y NRC", "valor": f"{periodo} · {nrc}", "tipo": "Bloque clave", "detalle": "Pulse «Ir»."},
                {"campo": "Nota final", "valor": "INH (prueba del NRC 10044)" if comp else "Nota final o INH", "tipo": "Verificación", "detalle": "Con libro de calificaciones no se escribe la nota en «Calificaciones finales»: la calculada pasa sola (7.1.4, diap. 18 y 77; C106, C107)."},
            ]
        },
        "n7": {
            "fase": "Paso 7: Pase a historia",
            "pantalla": "SHRROLL (GJAPCTL)",
            "hito": "Notas en la historia académica",
            "instrucciones": [
                {"campo": "Proceso", "valor": "SHRROLL desde GJAPCTL", "tipo": "Proceso masivo", "detalle": "Ejecute con periodo y NRC; revise que el job termine sin errores (Scripts 12 y 14)."},
                {"campo": "Si falla", "valor": "«No Substitute Grade Found»", "tipo": "Diagnóstico", "detalle": "Agregue en SHAGRDE el modo del curso para el nivel (U20)."},
                {"campo": "Después", "valor": "CAPP (SMICRLT)", "tipo": "Seguimiento", "detalle": "El curso aprobado suma; con nota bajo el mínimo o INH queda «no usado» (Script 10)."},
            ]
        },
    }

# ===========================================================================
# 7. CASUÍSTICAS / SCRIPTS (Excel 2)
# ===========================================================================

GUIAS_SCRIPTS = {
    "01": {
        "c0": {"fase": "Condición Previa", "pantalla": "SAAQUIK / SGASTDN", "hito": "Participante admitido y con estatus activo AS"},
        "c1": {"fase": "Paso 1: Autorización Curricular", "pantalla": "SFAREGS", "hito": "Plan de estudios autorizado con estatus elegible (EL) mediante F10"},
        "c2": {"fase": "Paso 2: Registro en Asignatura", "pantalla": "SFAREGS", "hito": "Ingreso de NRC con código de inscripción regular RE"},
        "c3": {"fase": "Paso 3: Balance de Vacantes", "pantalla": "SSASECT / SSASECQ", "hito": "Actualización automática de cupos: Actual suma 1 y Remaining descuenta 1"},
        "c4": {"fase": "Paso 4: Auditoría Financiera", "pantalla": "TSAAREV", "hito": "Tasación automática de cuotas y aparición en lista oficial de SFASLST"},
        "cr": {"fase": "Resultado Validado", "pantalla": "TEST USS", "hito": "Matrícula regular 100% procesada con éxito"}
    },
    "03": {
        "c0": {"fase": "Condición Previa", "pantalla": "Estudios Previos", "hito": "Estudiante con asignatura aprobada en entidad externa (S00581111 - IST150 nota 16)"},
        "c1": {"fase": "Paso 1: Registro Asignatura Externa", "pantalla": "SHATRNS", "hito": "ID S00581111, Institución de procedencia y asignatura externa IST150 (Nota 16, Modo P)"},
        "c2": {"fase": "Paso 2: Articulación y Acreditación", "pantalla": "SHATFAC", "hito": "Mapeo curricular con curso oficial local y registro de aprobación académica oficial"},
        "c3": {"fase": "Paso 3: Pase a Historia Académica", "pantalla": "GJAPCTL (SHRROLL)", "hito": "Ejecución de proceso batch SHRROLL (Job 8113) con código de éxito 0"},
        "c4": {"fase": "Paso 4: Confirmación en Historial", "pantalla": "SHASMRY / SHADEGR", "hito": "Estatus «Rolled to Academic History», expediente Deg Created y transcript convalidado"},
        "cr": {"fase": "Resultado Validado", "pantalla": "TEST USS", "hito": "Acreditación y convalidación culminada al 100% sin cursado regular"}
    },
    "04": {
        "c0": {"fase": "Condición Previa", "pantalla": "Idiomas USS", "hito": "Estudiante con dominio previo que busca exonerar BASIC I para cursar BASIC II"},
        "c1": {"fase": "Paso 1: Registro de Calificación", "pantalla": "SOATEST", "hito": "Ingreso de código de prueba U01 con puntaje aprobatorio del estudiante"},
        "c2": {"fase": "Paso 2: Validación de Prerrequisito", "pantalla": "SCAPREQ", "hito": "El motor de reglas valida el examen como prerrequisito equivalente de BASIC I"},
        "c3": {"fase": "Paso 3: Matrícula Directa en BASIC II", "pantalla": "SFAREGS", "hito": "Inscripción en NRC de BASIC II permitida sin error fatal de prerrequisito"},
        "c4": {"fase": "Paso 4: Asignación de Vacante", "pantalla": "SFAREGS", "hito": "Guardado con código RE y consumo regular de cupo en la sección"},
        "cr": {"fase": "Resultado Validado", "pantalla": "TEST USS", "hito": "Matrícula por suficiencia validada y habilitada al 100%"}
    },
    "05": {
        "c0": {"fase": "Condición Previa", "pantalla": "Egresados USS", "hito": "Egresado que requiere acreditar requisito de titulación mediante modalidad intensiva"},
        "c1": {"fase": "Paso 1: Apertura de NRC Especial", "pantalla": "SSASECT", "hito": "Creación de sección especial con indicador de egresados y fechas específicas"},
        "c2": {"fase": "Paso 2: Inscripción Administrativa", "pantalla": "SFAREGS", "hito": "Inscripción del alumno bajo arancel diferenciado para egresados"},
        "c3": {"fase": "Paso 3: Evaluación y Plataforma", "pantalla": "Plataforma Externa", "hito": "Instrucción intensiva externa y reporte de calificación final obtenida"},
        "c4": {"fase": "Paso 4: Cierre y Pase a Historia", "pantalla": "SFASLST → SHRROLL", "hito": "Asentamiento docente de notas y pase a historia para CAPP de titulación"},
        "cr": {"fase": "Resultado Validado", "pantalla": "TEST USS", "hito": "Requisito de egreso culminado y reconocido curricularmente"}
    },
    "08": {
        "c0": {"fase": "Condición Previa", "pantalla": "Matrícula Activa", "hito": "Alumno solicita retiro regular dentro del plazo (S00581091 en NRC 1021)"},
        "c1": {"fase": "Paso 1: Consulta de Inscripción", "pantalla": "SFAREGS", "hito": "Acceso al formulario con Periodo 202656 e ID del estudiante matriculado"},
        "c2": {"fase": "Paso 2: Asignación de Código DD", "pantalla": "SFAREGS", "hito": "Ingreso del código Drop/Delete (DD) en el registro del curso NRC 1021"},
        "c3": {"fase": "Paso 3: Recálculo Financiero", "pantalla": "SFAREGS", "hito": "Transacción procesada con «Estimación de cuota procesada» y ajuste de cobros"},
        "c4": {"fase": "Paso 4: Liberación de Cupo en Vivo", "pantalla": "SSASECT / SSASECQ", "hito": "Aforo actualizado automáticamente: Actual disminuye de 2 a 1 y Remaining suma 1"},
        "cr": {"fase": "Resultado Validado", "pantalla": "TEST USS", "hito": "Retiro procesado al 100% y vacante liberada de inmediato"}
    },
    "09": {
        "c0": {"fase": "Condición Previa", "pantalla": "Expediente Alumno", "hito": "Estudiante con estatus académico inactivo (S00581109 con Status IS)"},
        "c1": {"fase": "Paso 1: Intento de Inscripción IS", "pantalla": "SFAREGS", "hito": "El motor de inscripción bloquea cualquier alta de NRC por condición inactiva"},
        "c2": {"fase": "Paso 2: Alerta de Restricción", "pantalla": "SFAREGS", "hito": "Emisión de mensaje de notificación indicando estatus no elegible"},
        "c3": {"fase": "Paso 3: Reactivación Académica", "pantalla": "SGASTDN", "hito": "Modificación de estatus general a Activo (AS) en pestaña Curricula y guardado"},
        "c4": {"fase": "Paso 4: Matrícula Reanudada", "pantalla": "SFAREGS", "hito": "Captura de NRC habilitada; registro exitoso con código RE y asignación de cupo"},
        "cr": {"fase": "Resultado Validado", "pantalla": "TEST USS", "hito": "Restitución de derechos de matrícula validada al 100%"}
    },
    "10": {
        "c0": {"fase": "Condición Previa", "pantalla": "Historia Académica", "hito": "Estudiante con calificación reprobatoria rolada (S00581108 nota 08 en ESEC 00650)"},
        "c1": {"fase": "Paso 1: Solicitud de Auditoría CAPP", "pantalla": "SMARQCM", "hito": "Generación de evaluación curricular contra la malla del programa CMEMC38"},
        "c2": {"fase": "Paso 2: Regla de Calificación Mínima", "pantalla": "SMIPOUT", "hito": "Validación de nota mínima aprobatoria (Nota ≥ 11); la nota 08 es rechazada"},
        "c3": {"fase": "Paso 3: Segregación a Cursos No Usados", "pantalla": "SMICRLT", "hito": "La asignatura reprobada es enviada al bloque de cursos no usados (0 créditos)"},
        "c4": {"fase": "Paso 4: Dictamen y Retorno Obligatorio", "pantalla": "SMARQCM / SMIPOUT", "hito": "Dictamen oficial «NO CUMPLE» (0/4 cursos); bloqueo de avance y retorno obligatorio"},
        "cr": {"fase": "Resultado Validado", "pantalla": "TEST USS", "hito": "Bloqueo por desaprobado y auditoría CAPP validados al 100%"}
    },
    "12": {
        "c0": {"fase": "Condición Previa", "pantalla": "Fin de Periodo", "hito": "Periodo 202656 culminado con notas finales listas en NRC 1026"},
        "c1": {"fase": "Paso 1: Ingreso de Notas Finales", "pantalla": "SFASLST", "hito": "Captura de notas: S00581109 (16 V), S00581108 (08 V), S00581111 (INH V)"},
        "c2": {"fase": "Paso 2: Diagnóstico y Resolución U20", "pantalla": "SHAGRDE", "hito": "Alineación de Modo V en catálogo y nivel C para resolver incompatibilidad con SHRROLL"},
        "c3": {"fase": "Paso 3: Corrida Batch SHRROLL", "pantalla": "GJAPCTL", "hito": "Job 8114 exitoso con 100% de estudiantes rolados a la historia académica"},
        "c4": {"fase": "Paso 4: Bloqueo Formal de Acta", "pantalla": "SFASLST / SHATERM", "hito": "Indicador Grade Roll Status = Y; acta cerrada impidiendo ediciones no autorizadas"},
        "cr": {"fase": "Resultado Validado", "pantalla": "TEST USS", "hito": "Cierre de actas y resolución institucional U20 validados al 100%"}
    },
    "13": {
        "c0": {"fase": "Condición Previa", "pantalla": "Evaluación Continua", "hito": "Docente finaliza el ciclo y dispone de las calificaciones finales de la sección"},
        "c1": {"fase": "Paso 1: Verificación de Escala", "pantalla": "SHAGRDE", "hito": "Modo V con escala vigesimal (00-20) y nota aprobatoria mínima 11"},
        "c2": {"fase": "Paso 2: Registro en Lista de Clase", "pantalla": "SFASLST", "hito": "Captura de calificaciones y asignación de código INH a participantes inhabilitados"},
        "c3": {"fase": "Paso 3: Auditoría Previa a Rolado", "pantalla": "SFASLST", "hito": "Comprobación de columna Rolled en estado N antes del proceso batch"},
        "c4": {"fase": "Paso 4: Pase Oficial a Historia", "pantalla": "GJAPCTL (SHRROLL)", "hito": "Ejecución de SHRROLL transfiriendo las notas a la historia académica definitiva"},
        "cr": {"fase": "Resultado Validado", "pantalla": "TEST USS", "hito": "Procesamiento de calificaciones validado al 100%"}
    },
    "15": {
        "c0": {"fase": "Condición Previa", "pantalla": "Aforo Reducido", "hito": "Sección con cupo inicial de 1 sola vacante (NRC 1026 en SSASECT)"},
        "c1": {"fase": "Paso 1: Capacidad Inicial Saturada", "pantalla": "SSASECT → SFAREGS", "hito": "Alumno 1 (S00581091) se inscribe con RE ocupando el único cupo disponible"},
        "c2": {"fase": "Paso 2: Intento y Bloqueo de Alumno 2", "pantalla": "SFAREGS", "hito": "Alumno 2 (S00582045) intenta inscribirse y el sistema emite error fatal Closed Section"},
        "c3": {"fase": "Paso 3: Ampliación de Aforo", "pantalla": "SSASECT", "hito": "En bloque Enrollment, la capacidad máxima se amplía de 1 a 4 vacantes (Remaining: 3)"},
        "c4": {"fase": "Paso 4: Matrícula Exitosa y Balance", "pantalla": "SFAREGS → SSASECT", "hito": "Alumno 2 se inscribe con RE satisfactoriamente; balance final: Actual 2, Remaining 2"},
        "cr": {"fase": "Resultado Validado", "pantalla": "TEST USS", "hito": "Ampliación de cupos y control de sobrecupo validados al 100%"}
    },
    "16": {
        "c0": {"fase": "Condición Previa", "pantalla": "Reubicación Horaria", "hito": "Estudiante matriculado en NRC 1026 (Sec. D) solicita traslado a NRC 1021 (Sec. B)"},
        "c1": {"fase": "Paso 1: Verificación de Origen y Destino", "pantalla": "SFAREGS → SSASECT", "hito": "Comprobar matrícula activa en origen y disponibilidad de cupo en la sección destino"},
        "c2": {"fase": "Paso 2: Ajuste de Reserva de Cupo", "pantalla": "SSASECT > Lugares reservados", "hito": "Ajustar la regla de reserva de CMEMC38 y su Máximo reservado en la sección destino"},
        "c3": {"fase": "Paso 3: Transacción Simultánea", "pantalla": "SFAREGS", "hito": "Guardar en un solo paso: NRC 1026 con código DD y NRC 1021 con código RE"},
        "c4": {"fase": "Paso 4: Auditoría de Lista y Cobros", "pantalla": "SFASLST / TSAAREV", "hito": "Aparición en nueva lista oficial; vacante origen liberada y sin cobro duplicado"},
        "cr": {"fase": "Resultado Validado", "pantalla": "TEST USS", "hito": "Traslado entre secciones paralelas validado al 100%"}
    },
    "18-A": {
        "c0": {"fase": "Condición Previa", "pantalla": "Asignación Docente", "hito": "Docente asignado a secciones lectivas del periodo (100582059 Dagner Chuman)"},
        "c1": {"fase": "Paso 1: Consulta en SIAASGN", "pantalla": "SIAASGN", "hito": "Acceso con Periodo 202656 e ID del docente para visualizar la carga consolidada"},
        "c2": {"fase": "Paso 2: Auditoría de 4 NRCs", "pantalla": "SIAASGN", "hito": "Verificación de secciones 1021, 1022, 1024 y 1025 en Computación y Emprendimiento"},
        "c3": {"fase": "Paso 3: Cómputo de Horas", "pantalla": "SIAASGN", "hito": "Cálculo automático de 9,60 h/semana y 120 horas totales para el NRC 1021"},
        "c4": {"fase": "Paso 4: Factor FTE y Reemplazo Excel", "pantalla": "SIAASGN", "hito": "FTE 0.02 computado con roles primario/secundario, sustituyendo planillas Excel"},
        "cr": {"fase": "Resultado Validado", "pantalla": "TEST USS", "hito": "Auditoría de carga docente consolidada al 100%"}
    },
    "18-B": {
        "c0": {"fase": "Condición Previa", "pantalla": "Cobranzas USS", "hito": "Estudiante mantiene deuda vencida o cuota impaga antes del periodo lectivo"},
        "c1": {"fase": "Paso 1: Asignación de Retención TT", "pantalla": "SOAHOLD", "hito": "Registro de retención con código TT (Cobranzas) por causal de mora económica"},
        "c2": {"fase": "Paso 2: Intento de Inscripción y Bloqueo", "pantalla": "SFAREGS", "hito": "Intento de captura de NRC rechazado con error fatal por retención activa"},
        "c3": {"fase": "Paso 3: Regularización en Caja", "pantalla": "TSAAREV / TVACAJA", "hito": "Cancelación de la obligación económica en caja institucional"},
        "c4": {"fase": "Paso 4: Levantamiento y Matrícula", "pantalla": "SOAHOLD → SFAREGS", "hito": "Retención desactivada; matrícula permitida de inmediato con código RE"},
        "cr": {"fase": "Resultado Validado", "pantalla": "TEST USS", "hito": "Bloqueo fatal y desbloqueo por mora validados al 100%"}
    }
}

# ===========================================================================
# 8. FUNCIÓN DESPACHADORA PRINCIPAL
# ===========================================================================

def obtener_guia(slug, id_centro=""):
    """Devuelve la guía operativa paso a paso adaptada de forma 100% específica al centro."""
    slug_limpio = slug.lower()
    centro = id_centro.lower() if id_centro else ("idiomas" if "idiomas" in slug_limpio else ("computacion" if "computacion" in slug_limpio else ("emprendimiento" if "emprendimiento" in slug_limpio else "comun")))

    # 1. Crear el NRC
    if "crear-el-nrc" in slug_limpio:
        if centro == "idiomas":
            return GUIA_CREAR_NRC_IDIOMAS
        elif centro == "computacion":
            return GUIA_CREAR_NRC_COMPUTACION
        elif centro == "emprendimiento":
            return GUIA_CREAR_NRC_EMPRENDIMIENTO
        return GUIA_CREAR_NRC_COMPUTACION

    # 2. Ligas
    if "ligas-teorico-y-club" in slug_limpio or "ligas" in slug_limpio:
        return GUIA_LIGAS

    # 3. Carga Lectiva
    if "carga-lectiva" in slug_limpio:
        return GUIA_CARGA_LECTIVA

    # 4. Persona y Admisión
    if "persona-y-admision" in slug_limpio:
        return obtener_guia_persona_admision(centro)

    # 5. Matrícula en el NRC
    if "matricula-en-el-nrc" in slug_limpio:
        return obtener_guia_matricula(centro)

    # 6. Notas y Cierre
    if "notas-y-pase-a-historia" in slug_limpio:
        return obtener_guia_notas(centro)

    # 7. Scripts / Casuísticas
    for s_id, s_map in GUIAS_SCRIPTS.items():
        if f"script-{s_id}" in slug_limpio or f"script_{s_id}" in slug_limpio:
            return s_map

    return None

# Compatibilidad retrospectiva con código previo
GUIAS_BASE = {
    "crear-el-nrc": GUIA_CREAR_NRC_COMPUTACION,
    "carga-lectiva": GUIA_CARGA_LECTIVA,
    "ligas-teorico-y-club": GUIA_LIGAS
}

###########################################################################
# GENERADOR DINÁMICO DE CASUÍSTICAS DESDE plantillas.py (CASOS + EXTRA_CASOS)
###########################################################################

"""Guía operativa (tabla de 6 columnas) de cada script de casuística, generada desde plantillas.py.

Fuente única de verdad: CASOS (situación, pasos, resultado) + EXTRA_CASOS (líneas
«Paso NN (CÓDIGO): Título — detalle»). Así los ids de la guía son SIEMPRE los que dibuja
plantillas.casuistica():  c0 (situación) · c1..cN (pasos) · cr (resultado).

Este módulo no importa nada del proyecto: se puede probar solo.
"""
import re

RE_LINEA = re.compile(r"^\s*Paso\s+(\d+)\s*\(([^)]*)\)\s*:\s*(.+?)\s+—\s+(.+?)\s*$", re.S)

# Valores «tecleables» que se reconocen dentro del detalle (primero = Valor, siguientes = Ejemplo).
_PATRONES = [
    (r"(?i:c[oó]digo)\s+(RE|DD|TT|INH|U\d{2})\b", "Código {}"),
    (r"\b[Ss]tatus:?\s*(AS|IS|EL|SU)\b", "Status {}"),
    (r"\bMaximum:?\s*(\d+(?:\s*→\s*\d+)?)", "Maximum {}"),
    (r"\bNRC\s+(\d{4})\b", "NRC {}"),
    (r"\bID:?\s*(S\d{8}|\d{9})\b", "ID {}"),
    (r"\bJob\s+(\d{4})\b", "Job {}"),
    (r"\b(?:Periodo[^.(]{0,12}\(ej\.?\s*)?(20\d{4})\b", "Periodo {}"),
    (r"\b(Remaining|Actual):?\s*(-?\d+(?:\s*→\s*\d+)?)", None),
    (r"\bModo:?\s*([VP])\b", "Modo {}"),
    (r"\b(F10)\b", "F10 (Guardar)"),
]

_VERIF = re.compile(r"verific|consulta|auditor|validaci|revisi|diagn|comprob|evaluaci[oó]n", re.I)
_CRITICO = re.compile(r"asentamiento|confirmaci[oó]n|exitos|reejecuci[oó]n|pase a historia|despacho|"
                      r"levantamiento|reactivaci[oó]n|liberaci[oó]n|cierre|bloqueo|asignaci[oó]n de c[oó]digo|ejecuci[oó]n", re.I)
_CAPTURA = re.compile(r"registro|ingreso|captura|creaci|configuraci|asignaci|ampliaci|ajuste|acceso|alineaci|activaci|autorizaci", re.I)


def parsear_linea(texto):
    """'Paso 02 (SFAREGS / SSASECT): Título — detalle' → dict. Si el formato se desvía, no se pierde la línea."""
    m = RE_LINEA.match(texto)
    if not m:
        return {"n": 0, "codes": [], "codes_up": set(), "titulo": texto[:60].strip(), "detalle": texto.strip()}
    n, codigos, titulo, detalle = m.groups()
    codes = [c.strip() for c in codigos.split("/") if c.strip()]
    return {"n": int(n), "codes": codes, "codes_up": {c.upper() for c in codes},
            "titulo": titulo.strip(), "detalle": detalle.strip()}


def clasificar_tipo(titulo):
    """El JS marca en verde las filas cuyo tipo contiene «crítico» o «guardado»."""
    if _VERIF.search(titulo):
        return "Verificación"
    if _CRITICO.search(titulo):
        return "Crítico (guardado)"
    if _CAPTURA.search(titulo):
        return "Captura"
    return "Acción"


def extraer_valor_ejemplo(detalle, pantalla):
    hallados = []
    for patron, plantilla in _PATRONES:
        for m in re.finditer(patron, detalle):
            if plantilla is None:  # Actual / Remaining: «Remaining -1»
                num = re.sub(r"\s+", " ", m.group(2))
                hallados.append((m.start(), m.group(1) + " " + num))
            else:
                hallados.append((m.start(), plantilla.format(re.sub(r"\s+", " ", m.group(1)))))
    hallados.sort()
    vistos = []
    for _, v in hallados:
        if v not in vistos:
            vistos.append(v)
    if not vistos:
        return (pantalla or "—"), "-"
    return vistos[0], (" · ".join(vistos[1:3]) if len(vistos) > 1 else "-")


def _asignar(lineas, codigos_nodo):
    """Reparte las líneas del Excel (5 a 7) entre los nodos del diagrama (4 pasos), sin cambiar el orden.

    Programación dinámica: cada línea va al mismo nodo o al siguiente que la anterior, todos los nodos
    quedan cubiertos y gana el reparto con más coincidencias de código (SFAREGS↔SFAREGS…);
    a igualdad, el más parejo.
    """
    n, m = len(codigos_nodo), len(lineas)
    if not n or not m:
        return []
    NEG = float("-inf")

    def pts(i, j):
        coincide = 3.0 if codigos_nodo[j - 1].upper() in lineas[i]["codes_up"] else 0.0
        return coincide - 0.05 * abs(j - (i + 1) * n / m)

    dp = [[NEG] * (n + 1) for _ in range(m)]
    previo = [[0] * (n + 1) for _ in range(m)]
    dp[0][1] = pts(0, 1)
    for i in range(1, m):
        for j in range(1, n + 1):
            quedarse = dp[i - 1][j]
            avanzar = dp[i - 1][j - 1] if j > 1 else NEG
            mejor, desde = (quedarse, j) if quedarse >= avanzar else (avanzar, j - 1)
            if mejor == NEG:
                continue
            dp[i][j] = mejor + pts(i, j)
            previo[i][j] = desde
    asign, j = [0] * m, min(n, m)
    for i in range(m - 1, -1, -1):
        asign[i] = j
        j = previo[i][j]
    return asign


def _fila(campo, valor, ejemplo, tipo, detalle):
    return {"campo": campo, "valor": valor, "ejemplo": ejemplo, "tipo": tipo, "detalle": detalle}


def construir_guia(situacion, pasos, resultado, lineas_extra, titulo_script=""):
    if isinstance(lineas_extra, dict):
        lineas_extra = lineas_extra.get("items", [])
    elif not isinstance(lineas_extra, list):
        lineas_extra = [lineas_extra] if lineas_extra else []
    """situacion=(título, sub) · pasos=[(código, acción[, dato])] · resultado=(título, sub) · lineas_extra=[str]."""
    (sit, sit_sub), (res, res_sub) = situacion, resultado
    lineas = [parsear_linea(t) for t in (lineas_extra or [])]
    asign = _asignar(lineas, [p[0] for p in pasos])
    guia = {
        "c0": {
            "titulo": titulo_script, "pantalla": "CASO", "fase": f"Situación: {sit}", "hito": sit_sub,
            "instrucciones": [_fila("Situación inicial", sit, sit_sub, "Contexto",
                                    f"Punto de partida del script: {sit_sub}.")],
        }
    }
    for j, item in enumerate(pasos, start=1):
        codigo, accion = item[0], item[1]
        dato = item[2] if len(item) > 2 else ""
        filas = []
        for ln, destino in zip(lineas, asign):
            if destino != j:
                continue
            valor, ejemplo = extraer_valor_ejemplo(ln["detalle"], ln["codes"][0] if ln["codes"] else codigo)
            detalle = ln["detalle"]
            if ln["codes"] and codigo.upper() not in ln["codes_up"]:
                detalle = f"({' / '.join(ln['codes'])}) {detalle}"
            filas.append(_fila(ln["titulo"], valor, ejemplo, clasificar_tipo(ln["titulo"]), detalle))
        if not filas:  # nodo sin líneas en el Excel: al menos su acción y dato de TEST
            filas.append(_fila(accion, codigo, dato or "-", clasificar_tipo(accion), accion[0].upper() + accion[1:] + "."))
        guia[f"c{j}"] = {"titulo": titulo_script, "pantalla": codigo, "fase": f"Paso {j}: {accion}",
                         "hito": dato, "instrucciones": filas}
    guia["cr"] = {
        "titulo": titulo_script, "pantalla": "RESULTADO", "fase": f"Resultado: {res}", "hito": res_sub,
        "instrucciones": [_fila("Resultado esperado", res, res_sub, "Resultado",
                                "Estado final del caso una vez ejecutados todos los pasos anteriores.")],
    }
    return guia
