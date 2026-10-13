"""Guías operativas paso a paso extraídas de Excel 1 y Excel 2 de Centros Empresariales.

Se inyectan directamente en el modal (Pasaporte semántico) de Archify al hacer clic
en cada nodo del flujo, evitando textos largos en las tarjetas al pie de página.
"""

# Guías para los diagramas base (Excel 1)
GUIAS_BASE = {
    "crear-el-nrc": {
        "s1": {
            "fase": "Paso 1: Encabezado (Bloque Clave)",
            "pantalla": "SSASECT",
            "hito": "Inicio de proceso · Indicador ADD temporal",
            "instrucciones": [
                {"campo": "Formulario", "valor": "SSASECT", "tipo": "Acceso inicial", "detalle": "Escribir SSASECT en la barra de búsqueda de Banner y presionar Enter."},
                {"campo": "Periodo", "valor": "202656 (o periodo lectivo)", "tipo": "Obligatorio", "detalle": "Ingresar periodo (202651: verano, 202654: sem I, 202656: sem II)."},
                {"campo": "NRC", "valor": "(DEJAR EN BLANCO)", "tipo": "Mandatorio", "detalle": "Dejar TOTALMENTE VACÍO para aperturar una nueva sección."},
                {"campo": "Botón de Creación", "valor": "Clic en «Crear NRC»", "tipo": "Acción del sistema", "detalle": "Hacer clic en el botón azul. El campo mostrará temporalmente ADD."}
            ]
        },
        "s2": {
            "fase": "Paso 2: Información de sección",
            "pantalla": "SSASECT",
            "hito": "⭐ ¡PRIMER GUARDADO! (NRC generado)",
            "instrucciones": [
                {"campo": "Materia", "valor": "ESEC (o ENGL, ESGE)", "tipo": "Obligatorio", "detalle": "Escribir directo en mayúsculas y presionar Tab. Evita abrir la lista si ya conoces la materia."},
                {"campo": "Número de curso", "valor": "00650 (ej. Word 365)", "tipo": "Obligatorio", "detalle": "Digitar y presionar Tab. El campo Título se autocompleta desde el catálogo."},
                {"campo": "Sección", "valor": "A (o correlativo: B, C, D...)", "tipo": "Obligatorio", "detalle": "Asignar letra única que no esté ocupada en ese curso y periodo."},
                {"campo": "Campus", "valor": "S (Sede Chiclayo)", "tipo": "Obligatorio", "detalle": "Digitar S o elegir de lista. Corresponde al campus operativo del centro."},
                {"campo": "Estatus", "valor": "A (Activo)", "tipo": "Mandatorio", "detalle": "Seleccionar 'Activo'; indispensable para permitir la posterior matrícula."},
                {"campo": "Tipo de horario", "valor": "TEO (Teórico)", "tipo": "Obligatorio", "detalle": "Digitar TEO o derivado del catálogo. El método educativo hereda VIRT."},
                {"campo": "Modo de calificar", "valor": "V (Vigesimal)", "tipo": "Obligatorio", "detalle": "Digitar V. Obligatorio según el plan curricular del centro."},
                {"campo": "Aprobación especial", "valor": "(DEJAR EN BLANCO)", "tipo": "Control operativo", "detalle": "Dejar vacía: no seleccionar nada para evitar bloqueos de asesor/decano."},
                {"campo": "Parte de periodo", "valor": "X07 (Computación) / I08 (Idiomas)", "tipo": "Obligatorio", "detalle": "En «Clase tradicional»: digitar y presionar Tab. Fechas inicio/fin se calculan solas."},
                {"campo": "¡PRIMER GUARDADO!", "valor": "Botón «Guardar» (F10)", "tipo": "Hito Crítico", "detalle": "MANDATORIO: Guardar (F10) aquí antes de cambiar de pestaña para evitar error 'Debe guardar antes de salir'. El ADD cambia al NRC oficial (ej. 1026)."}
            ]
        },
        "s3": {
            "fase": "Paso 3: Aforo de sección",
            "pantalla": "SSASECT",
            "hito": "⭐ ¡SEGUNDO GUARDADO! (Cupos confirmados)",
            "instrucciones": [
                {"campo": "Pestaña Ingreso de sección", "valor": "Clic en pestaña 2", "tipo": "Navegación", "detalle": "Ir a «Información de ingreso de sección» (Enrollment Details)."},
                {"campo": "Máximo (Cupos del aula)", "valor": "1, 2 (o aforo aula: 25, 30)", "tipo": "Obligatorio", "detalle": "Ingresar cantidad autorizada de vacantes para el NRC."},
                {"campo": "¡SEGUNDO GUARDADO!", "valor": "Botón «Guardar» (F10)", "tipo": "Hito Crítico", "detalle": "Guardar (F10) para fijar el cupo. El contador Restante se actualiza automáticamente al aforo."}
            ]
        },
        "s4": {
            "fase": "Paso 4: Horario, Aula y Docente",
            "pantalla": "SSASECT",
            "hito": "⭐ ¡TERCER GUARDADO! (Horario y Docente)",
            "instrucciones": [
                {"campo": "Pestaña Horario y reunión", "valor": "Clic en pestaña 3", "tipo": "Navegación", "detalle": "Ir a «Instructor y horas de reunión»."},
                {"campo": "Horario (Días y Horas)", "valor": "Tipo CLAS | 0800 a 1200 | Lunes y Mié", "tipo": "Obligatorio", "detalle": "En subpestaña «Fechas de reunión»: tipo CLAS, formato 24h y marcar casillas de días."},
                {"campo": "Ubicación (Edificio y Aula)", "valor": "Edificio SAUVIR | Salón SALA VIRT.", "tipo": "Obligatorio", "detalle": "En «Créditos y ubicación»: usar SAUVIR / SALA VIRT. (aula virtual oficial). Previene el *ERROR* Conflicto de salón."},
                {"campo": "Sobrepaso de Salón", "valor": "Casilla Indicador de sobrepaso", "tipo": "Contingencia", "detalle": "Si se usa salón físico con cruce, escribir O en la casilla rectangular para omitir conflicto."},
                {"campo": "Horas Semanales", "valor": "Calculado automático (ej. 9,60 h)", "tipo": "Informativo", "detalle": "Banner multiplica días/horas por el factor institucional de SIATERM."},
                {"campo": "Consistencia de Sesión", "valor": "Indicador de sesión: 01 (o 1)", "tipo": "Regla Crítica", "detalle": "REGLA DE ORO: El indicador de sesión de HORARIO debe ser idéntico al de INSTRUCTOR (ambos 01 o ambos 1)."},
                {"campo": "Docente Principal", "valor": "ID 100582059 | Principal ☑ | 100%", "tipo": "Obligatorio", "detalle": "En tabla «Instructor»: digitar ID (activo en SIAINST), presionar Tab, marcar Principal y colocar 100% responsabilidad y sesión."},
                {"campo": "Sobrepaso de Docente", "valor": "Casilla Indicador de sobrepaso", "tipo": "Contingencia", "detalle": "Si el docente ya tiene otro NRC a esa misma hora, marcar la casilla Indicador de sobrepaso ☑ para resolver conflicto de horario."},
                {"campo": "¡TERCER GUARDADO!", "valor": "Botón «Guardar» (F10)", "tipo": "Hito Crítico", "detalle": "Guardar (F10). Mensaje verde: ✓ Saved successfully. NRC listo con horario y profesor."}
            ]
        },
        "s5": {
            "fase": "Paso 5: Reserva de cupos (SSARRES)",
            "pantalla": "SSARRES",
            "hito": "⭐ ¡CUARTO GUARDADO! (Reservas activas)",
            "instrucciones": [
                {"campo": "Lugares Reservados", "valor": "Menú Relacionado → SSARRES", "tipo": "Navegación", "detalle": "Subpestaña «Lugares reservados» para blindar cupos por tipo de participante."},
                {"campo": "Regla Nula (Cupo General)", "valor": "Regla NULL | Cupo: 1", "tipo": "Mandatorio institucional", "detalle": "OBLIGATORIA: La fila con clave nula no se borra; asegura cupo a pregrado institucional."},
                {"campo": "Regla por Programa CCEE", "valor": "Programa: CMEMC38 | Cupo: 1", "tipo": "Condicional CCEE", "detalle": "Presionar +, seleccionar PROGRAMA y código CMEMC38 para reservar cupo exclusivo al centro."},
                {"campo": "¡CUARTO GUARDADO!", "valor": "Botón «Guardar» (F10)", "tipo": "Hito Crítico", "detalle": "Guardar reservas (F10). Previene el error fatal de inscripción *ERROR* Reserve Closed."}
            ]
        },
        "s6": {
            "fase": "Paso 6: Publicación y Auditoría",
            "pantalla": "SSASECQ",
            "hito": "🎯 NRC 100% PUBLICADO Y AUDITADO",
            "instrucciones": [
                {"campo": "Consulta en SSASECQ", "valor": "Transacción SSASECQ", "tipo": "Verificación Final", "detalle": "Entrar a SSASECQ con periodo 202656, materia ESEC y curso 00650."},
                {"campo": "Confirmación de Estado", "valor": "Activo (A) | Horario visible | Vacante libre", "tipo": "Control de Calidad", "detalle": "Confirmar que figure Activo (A), horario visible y vacante disponible sin bloqueos."}
            ]
        }
    },
    "carga-lectiva": {
        "k1": {
            "fase": "Paso 1: Activación y Habilitación Docente",
            "pantalla": "SIAINST",
            "hito": "Docente activo en facultad y periodo",
            "instrucciones": [
                {"campo": "Formulario", "valor": "SIAINST", "tipo": "Acceso inicial", "detalle": "Ingresar ID del docente (ej. 100582059) y verificar estatus en facultad."},
                {"campo": "Pestaña Facultad", "valor": "Status: Activo", "tipo": "Obligatorio", "detalle": "Comprobar que el docente tenga permisos vigentes para dictado en el periodo lectivo."}
            ]
        },
        "k2": {
            "fase": "Paso 2: Asignación al NRC",
            "pantalla": "SSASECT",
            "hito": "Docente principal asignado al 100%",
            "instrucciones": [
                {"campo": "Formulario", "valor": "SSASECT", "tipo": "Programación", "detalle": "En pestaña Horario e instructores, asignar ID con sesión 01 y 100% responsabilidad."},
                {"campo": "Indicador Principal", "valor": "Casilla Principal ☑", "tipo": "Mandatorio", "detalle": "Marcar como instructor principal para emisión de actas oficiales."}
            ]
        },
        "k3": {
            "fase": "Paso 3: Auditoría de Carga Docente",
            "pantalla": "SIAASGN",
            "hito": "Horas y FTE computados automáticamente",
            "instrucciones": [
                {"campo": "Formulario", "valor": "SIAASGN", "tipo": "Auditoría", "detalle": "Consultar con Periodo 202656 e ID del docente (100582059 Dagner Chuman)."},
                {"campo": "Secciones asignadas", "valor": "4 NRCs (1021, 1022, 1024, 1025)", "tipo": "Consolidación", "detalle": "Auditoría de carga lectiva en Computación y Emprendimiento."},
                {"campo": "Horas semanales", "valor": "9,60 h/semana (NRC 1021)", "tipo": "Cálculo", "detalle": "Multiplicación de horas y factor de duración institucional de SIATERM."},
                {"campo": "Horas acumuladas", "valor": "120 horas lectivas totales", "tipo": "Cálculo", "detalle": "Cómputo acumulado de la carga lectiva total del periodo."},
                {"campo": "Asignación de FTE", "valor": "FTE 0.02 por sección", "tipo": "Cálculo", "detalle": "Factor de dedicación académica generado automáticamente sustituyendo planillas Excel."}
            ]
        },
        "k4": {
            "fase": "Paso 4: Visto Bueno del Centro",
            "pantalla": "Intranet USS",
            "hito": "Oficio institucional tramitado",
            "instrucciones": [
                {"campo": "Trámite", "valor": "Oficio del Jefe de Centro", "tipo": "Administrativo", "detalle": "Remitir consolidado de carga lectiva auditada al Vicerrectorado Académico."}
            ]
        },
        "k5": {
            "fase": "Paso 5: Aprobación Oficial",
            "pantalla": "Resolución VRA",
            "hito": "Resolución de carga docente aprobada",
            "instrucciones": [
                {"campo": "Aprobación", "valor": "Resolución Vicerrectoral", "tipo": "Oficial", "detalle": "El Vicerrectorado Académico emite la resolución formal de aprobación de carga."}
            ]
        }
    },
    "persona-y-admision": {
        "a1": {
            "fase": "Paso 1: Búsqueda de Coincidencias",
            "pantalla": "GOAMTCH",
            "hito": "Verificación de homónimos y duplicados",
            "instrucciones": [
                {"campo": "Formulario", "valor": "GOAMTCH", "tipo": "Acceso inicial", "detalle": "Ingresar a GOAMTCH con ID GENERATED."},
                {"campo": "Origen coincidencia", "valor": "PERS_NATU", "tipo": "Mandatorio", "detalle": "Seleccionar Persona Natural para aplicar filtros de búsqueda de documento de identidad."},
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
            "fase": "Paso 3: Admisión Rápida (Bloque Clave)",
            "pantalla": "SAAQUIK",
            "hito": "Inicio de admisión rápida en el centro",
            "instrucciones": [
                {"campo": "Formulario", "valor": "SAAQUIK", "tipo": "Acceso", "detalle": "Ingresar ID generado (ej. S00581081) y Periodo lectivo (202656)."},
                {"campo": "Parámetros base", "valor": "Nivel C/I/M · Campus S · Escuela EM", "tipo": "Mandatorio", "detalle": "Nivel C (Computación), I (Idiomas) o M (Emprendimiento); Campus S (Chiclayo); Grado 000000."}
            ]
        },
        "a4": {
            "fase": "Paso 4: Asignación de Programa Curricular",
            "pantalla": "SAAQUIK",
            "hito": "Programa curricular activo (3 rows saved)",
            "instrucciones": [
                {"campo": "Programa", "valor": "CMEMC38 (o código del centro)", "tipo": "Obligatorio", "detalle": "Seleccionar programa; autocompleta Major ACXP, Depto EMCI y Malla MC38."},
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
    },
    "matricula-en-el-nrc": {
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
                {"campo": "Formulario", "valor": "SFAREGS", "tipo": "Bloque Clave", "detalle": "Ingresar Periodo 202656 e ID del alumno admitido. Clic en «Ir»."},
                {"campo": "Currícula", "valor": "Clic en casilla de plan (carga 1)", "tipo": "Mandatorio", "detalle": "Asignar estatus elegible EL y Guardar (F10) para desbloquear inscripción de cursos."}
            ]
        },
        "i3": {
            "fase": "Paso 3: Inscripción en el NRC",
            "pantalla": "SFAREGS",
            "hito": "Inscripción regular (código RE)",
            "instrucciones": [
                {"campo": "Información de curso", "valor": "Ingresar NRC oficial", "tipo": "Obligatorio", "detalle": "En bloque Course Registration, digitar el NRC en la casilla correspondiente."},
                {"campo": "Código de estatus", "valor": "RE (Web / Backoffice Registered)", "tipo": "Mandatorio", "detalle": "Digitar RE y presionar Guardar (F10). Mensaje: Estimación de cuota procesada."}
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
    },
    "notas-y-pase-a-historia": {
        "n1": {
            "fase": "Paso 1: Verificación de Escala y Modo",
            "pantalla": "SHAGRDE",
            "hito": "Modo V vigesimal configurado",
            "instrucciones": [
                {"campo": "Formulario", "valor": "SHAGRDE", "tipo": "Catálogo", "detalle": "Verificar que el nivel del alumno tenga el Modo V con escala vigesimal (00 a 20)."}
            ]
        },
        "n2": {
            "fase": "Paso 2: Plan de Evaluación",
            "pantalla": "SHAGCOM",
            "hito": "Pesos y componentes evaluativos",
            "instrucciones": [
                {"campo": "Formulario", "valor": "SHAGCOM", "tipo": "Configuración", "detalle": "Revisar componentes y ponderaciones de evaluación institucional."}
            ]
        },
        "n3": {
            "fase": "Paso 3: Registro de Asistencia e Inhabilitados",
            "pantalla": "SFASLST / Web",
            "hito": "Inhabilitados marcados con código INH",
            "instrucciones": [
                {"campo": "Asistencia", "valor": "Código INH", "tipo": "Control", "detalle": "Estudiantes con inasistencia excesiva son registrados como INH con nota 00."}
            ]
        },
        "n4": {
            "fase": "Paso 4: Registro de Calificaciones Finales",
            "pantalla": "SFASLST / Web",
            "hito": "Calificaciones docentes registradas",
            "instrucciones": [
                {"campo": "Ingreso de notas", "valor": "Nota final vigesimal (00 a 20)", "tipo": "Docencia", "detalle": "Aprobado: nota ≥ 11; Desaprobado: nota ≤ 10. Columna Rolled permanece en N."}
            ]
        },
        "n5": {
            "fase": "Paso 5: Cierre Batch y Pase a Historia",
            "pantalla": "GJAPCTL (SHRROLL)",
            "hito": "Pase a historia completado (Rolled = Y)",
            "instrucciones": [
                {"campo": "Proceso batch", "valor": "SHRROLL", "tipo": "Procesamiento", "detalle": "Ejecutar proceso SHRROLL con periodo y NRC. Revisar bitácora .lis en GJIREVO sin abortos."},
                {"campo": "Historial académico", "valor": "SHATERM / SHACRSE", "tipo": "Resultado", "detalle": "Verificar que las notas muestren estatus «Rolled to Academic History»."}
            ]
        },
        "n6": {
            "fase": "Paso 6: Auditoría Curricular CAPP",
            "pantalla": "SMARQCM / SMICRLT",
            "hito": "Créditos otorgados o cursos no usados",
            "instrucciones": [
                {"campo": "Auditoría CAPP", "valor": "SMICRLT", "tipo": "Auditoría", "detalle": "Aprobados acreditan créditos del plan; desaprobados van a «Cursos no usados»."}
            ]
        }
    }
}

# Guías para las casuísticas / scripts (Excel 2)
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
        "c2": {"fase": "Paso 2: Ajuste de Reserva de Cupo", "pantalla": "SSARRES", "hito": "Ampliación de cupo reservado de CMEMC38 de 1 a 2 vacantes en sección destino"},
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
