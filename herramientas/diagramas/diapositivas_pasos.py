"""Qué diapositivas de los instructivos acompañan cada paso de las guías (ADR-022).

- INSTRUCTIVOS: clave corta → id del visor (visor_instructivos/data.js) y título legible.
- TEMAS: un tema = una lista de diapositivas {instructivo, n, texto}. «texto» es el pie que se ve.
- BASE: en los flujos base, el tema o la lista de cada nodo (s1, n3…).
- REGLAS: en las casuísticas (scripts), el tema sale de la página del paso y de palabras de su fase.

Las diapositivas se convierten con herramientas/diapositivas.py. Si una lámina lleva otro recorte,
agrega "caja": [izquierda, arriba, derecha, abajo]; si un número de la lámina no corresponde a la fila
de la guía que se llama igual, agrega "sin_marca": [campo].
"""
import re

INSTRUCTIVOS = {
    "1.1.1": {"id": "1.1.1_Definir_la_estructura_de_los_periodos_acade_micos", "titulo": "Instructivo 1.1.1 · Definir la estructura de los periodos académicos"},
    "1.1.2": {"id": "1.1.2_Programar_el_inicio_y_finalizacio_n_de_per_acad", "titulo": "Instructivo 1.1.2 · Programar el inicio y fin de los periodos"},
    "1.1.3": {"id": "1.1.3_Disen_ar_y_crear_los_programas_acade", "titulo": "Instructivo 1.1.3 · Diseñar y crear los programas académicos"},
    "1.1.5": {"id": "1.1.5_Asignar_prerequ__corequis_y_restricci", "titulo": "Instructivo 1.1.5 · Prerrequisitos, correquisitos y restricciones"},
    "1.2.1": {"id": "1.2.1_Crear_las_mallas_curriculares", "titulo": "Instructivo 1.2.1 · Crear las mallas curriculares (CAPP)"},
    "3.2.1": {"id": "3.2.1_Procedimiento_Crear_Solicitudes_de_Admisio_n", "titulo": "Instructivo 3.2.1 · Crear solicitudes de admisión"},
    "3.2.2": {"id": "3.2.2_Procedimiento_Validar_los_requisitos_de_admisio_n", "titulo": "Instructivo 3.2.2 · Validar los requisitos de admisión"},
    "3.3.1": {"id": "3.3.1_Gestionar_homologacio_n_y_convalidacio_n", "titulo": "Instructivo 3.3.1 · Gestionar homologación y convalidación"},
    "4.1.1": {"id": "4.1.1_Actualizar_estado_del_estudiante", "titulo": "Instructivo 4.1.1 · Actualizar el estado del estudiante"},
    "5.1.1": {"id": "5.1.1_Instructivo_-_Gestionar_persona_natural_V2", "titulo": "Instructivo 5.1.1 · Gestionar persona natural"},
    "5.2-docentes": {"id": "5.2_4.1.4.1_Instructivo_-_Informacio_n_de_Docentes", "titulo": "Instructivo 5.2 · Información de docentes"},
    "5.2-carga": {"id": "5.2_4.1.5.1_Instructivo_-_Carga_de_Trabajo_Docente", "titulo": "Instructivo 5.2 · Carga de trabajo docente"},
    "5.2.1": {"id": "5.2.1_Instructivo_-_Gestionar_retenciones_de_personas", "titulo": "Instructivo 5.2.1 · Gestionar retenciones de personas"},
    "5.3": {"id": "5.3_4.1.4.1.6_Instructivo_Registrar_la_oferta_horaria_de_los_cursos", "titulo": "Instructivo 5.3 · Registrar la oferta horaria de los cursos"},
    "5.3-ligas": {"id": "5.3_4.1.4.1.9_Instructivo_Crear_Ligas", "titulo": "Instructivo 5.3 · Crear ligas"},
    "5.4-inscripcion": {"id": "5.4_4.1.4.1.12_Instructivo_-_Ejecu.la_inscrip.de_cursos_por_backoffice", "titulo": "Instructivo 5.4 · Inscripción de cursos por backoffice"},
    "5.4-sobrepasos": {"id": "5.4_4.1.4.1.15_Instructivo_-_Gestionar_los_sobrepasos_de_inscripcio_n", "titulo": "Instructivo 5.4 · Gestionar los sobrepasos de inscripción"},
    "5.4-retiro": {"id": "5.4_4.1.4.1.16_Instructivo_-__Gestionar_retiro_de_cursos", "titulo": "Instructivo 5.4 · Gestionar el retiro de cursos"},
    "6.2.1": {"id": "6.2.1_Asignar_Docentes", "titulo": "Instructivo 6.2.1 · Asignar docentes"},
    "7.1.0": {"id": "7.1.0_Usar_Componente_Asistencia", "titulo": "Instructivo 7.1.0 · Usar el componente de asistencia"},
    "7.1.1": {"id": "7.1.1_Gestionar_la_asistencia_a_clases", "titulo": "Instructivo 7.1.1 · Gestionar la asistencia a clases"},
    "7.1.3": {"id": "7.1.3_Configurar_escalas_de_calificacio_n", "titulo": "Instructivo 7.1.3 · Configurar escalas de calificación"},
    "7.1.4": {"id": "7.1.4_Ingresar_calificaci_autoservicio", "titulo": "Instructivo 7.1.4 · Ingresar calificaciones por autoservicio"},
    "7.1.6": {"id": "7.1.6_Ingresar_calificac_backoffice", "titulo": "Instructivo 7.1.6 · Ingresar calificaciones por backoffice"},
    "7.1.9": {"id": "7.1.9_Ejecutar_procesos_de_cierre_de_per_acade_", "titulo": "Instructivo 7.1.9 · Procesos de cierre del periodo académico"},
    "7.2.4": {"id": "7.2.4_Ejecucio_n_del_CAPP", "titulo": "Instructivo 7.2.4 · Ejecución del CAPP"},
    "11.2.1": {"id": "11.2.1_-_Gestionar_la_matri_cula", "titulo": "Instructivo 11.2.1 · Gestionar la matrícula (cobros)"},
}


def _l(instructivo, *pares):
    """_l("5.3", (19, "texto"), (20, "texto")) → [{"instructivo", "n", "texto"}, …]"""
    return [{"instructivo": instructivo, "n": n, "texto": t} for n, t in pares]


TEMAS = {
    # Periodo, programas y mallas
    "periodo": _l("1.1.1", (18, "STVTERM: crear y definir el periodo académico")),
    "partes": _l("1.1.1", (14, "STVPTRM: código de la parte de periodo")),
    "soaterm": _l("1.1.2", (16, "SOATERM: ingresar el periodo creado en STVTERM"),
                  (20, "Partes de periodo: crear el registro de la parte"),
                  (21, "Semanas y fechas de censo de la parte"),
                  (23, "Fechas de inscripción web y de acceso docente")),
    "siaterm": _l("5.2-carga", (11, "SIATERM: periodo de la carga docente"), (12, "SIATERM: factor FTE del periodo")),
    "stvmajr": _l("1.1.3", (19, "STVMAJR: código de carrera"), (20, "STVMAJR: indicadores de carrera y especialidad")),
    "smaprle": _l("1.1.3", (22, "SMAPRLE: crear el código del programa"), (23, "SMAPRLE: reglas de currículum"),
                  (24, "SMAPRLE: campus y nivel del programa")),
    "soacurr": _l("1.1.3", (26, "SOACURR: regla de currícula base"), (27, "SOACURR: detalle de la regla"),
                  (29, "SOACURR: carreras y departamentos")),
    "smaprog": _l("1.2.1", (27, "SMAPROG: requerimientos del programa"), (28, "SMAPROG: requerimientos generales"),
                  (33, "SMAPROG: anexos de área del programa")),
    # NRC y docente
    "ssasect_crear": _l("5.3", (19, "Ingresar el periodo y pulsar «Crear NRC»"), (21, "Materia, curso, sección, campus y estatus")),
    "ssasect_cupo": _l("5.3", (27, "Detalles de ingreso: cupo del NRC"), (28, "Lugares reservados: regla nula y regla por criterio")),
    "ssasect_horario": _l("5.3", (29, "Fechas de reunión: horario de la sesión")) +
                       _l("6.2.1", (20, "Conflicto de horario del docente: indicador de sobrepaso")),
    "ssasect_docente": _l("6.2.1", (14, "Indicador de sesión del horario"), (15, "Bloque Instructor: ID del docente"),
                          (19, "Responsabilidad, docente principal y porcentaje de sesión")),
    "siainst": _l("5.2-docentes", (17, "SIAINST: docente y periodo"), (18, "SIAINST: estatus del docente"),
                  (19, "SIAINST: contrato y regla del docente"), (20, "SIAINST: atributos y guardar")),
    "siaasgn": _l("5.2-carga", (23, "SIAASGN: docente y periodo a analizar"), (24, "SIAASGN: carga de los NRC asignados"),
                  (26, "SIAASGN: resumen de la carga horaria"), (27, "SIAASGN: análisis por criterio de carga")),
    # Persona, admisión y alumno
    "goamtch": _l("5.1.1", (29, "GOAMTCH: origen de coincidencia"), (30, "GOAMTCH: criterios de búsqueda"),
                  (31, "GOAMTCH: personas que coinciden")),
    "spaiden": _l("5.1.1", (28, "SPAIDEN: crear la persona con coincidencia común"), (24, "SPAIDEN: apellidos y nombres"),
                  (25, "SPAIDEN: guardar y generar el ID")),
    "saaquik": _l("3.2.1", (21, "SAAQUIK: persona nueva o existente"), (22, "SAAQUIK: ID, periodo y nivel"),
                  (23, "SAAQUIK: tipo y estatus del alumno")),
    "saaquik_curr": _l("3.2.1", (25, "SAAQUIK: programa y currículo")),
    "sgastdn": _l("4.1.1", (14, "SGASTDN: alumno y periodo"), (15, "SGASTDN: estatus del alumno")),
    "sgastdn_doble": _l("4.1.1", (61, "Dos programas: pestaña Currículum"), (62, "Dos programas: elegir el nuevo programa"),
                        (63, "Dos programas: regla curricular"), (65, "Dos programas: planes de estudios activos")),
    # Matrícula
    "sfaregs_autorizar": _l("5.4-inscripcion", (35, "SFAREGS: periodo e ID del alumno"), (36, "SFAREGS: estatus de ingreso EL"),
                            (37, "SFAREGS: plan de estudios de ingreso y guardar")),
    "sfaregs_inscribir": _l("5.4-inscripcion", (38, "SFAREGS: ingresar el NRC"), (42, "SFAREGS: datos del NRC y plan de estudios"),
                            (43, "SFAREGS: guardar la inscripción")),
    "sfaregs_error": _l("5.4-inscripcion", (44, "SFAREGS: error de inscripción, DD o sobrepaso")),
    "sfaregs_retiro": _l("5.4-retiro", (42, "SFAREGS: código de retiro en el NRC"), (43, "SFAREGS: guardar el retiro"),
                         (44, "SFAREGS: recálculo de la cuenta")),
    "sfaregs_sobrepaso": _l("5.4-sobrepasos", (37, "SFAREGS: error de inscripción fatal"), (38, "SFAREGS: campo Sobrepasar"),
                            (39, "SFAREGS: guardar con sobrepaso")),
    "sfarovr": _l("5.4-sobrepasos", (19, "SFAROVR: permisos de sobrepaso del periodo"), (20, "SFAROVR: código y casillas del permiso")),
    "sfasrpo": _l("5.4-sobrepasos", (25, "SFASRPO: alumno y periodo"), (27, "SFASRPO: permiso y NRC")),
    "tsaarev": _l("11.2.1", (43, "SFAREGS: estimación de cuota procesada"), (44, "TSAAREV: conceptos de la estimación de cuota")),
    "tsaarev_retiro": _l("11.2.1", (92, "TSAAREV: cargo en negativo tras el retiro")),
    "soahold": _l("5.2.1", (13, "SOAHOLD: ID del alumno"), (14, "SOAHOLD: código de la retención"),
                  (15, "SOAHOLD: usuario que asigna y guardar")),
    "soatest": _l("3.2.2", (14, "SOATEST: código, puntaje y fecha del examen"), (15, "Requisito cumplido con el examen")),
    "scapreq": _l("1.1.5", (17, "SCAPREQ: acceso a las restricciones"), (18, "SCAPREQ: prerrequisitos del curso"),
                  (19, "SCAPREQ: detalle del prerrequisito")),
    "shatrns": _l("3.3.1", (33, "SHATRNS: formalizar la convalidación"), (34, "SHATRNS: número de periodo de asistencia"),
                  (35, "SHATRNS: institución de procedencia"), (36, "SHATRNS: periodo de asistencia"),
                  (37, "SHATAEQ: asignaturas convalidadas")),
    # Ligas
    "scacrse_ligas": _l("5.3-ligas", (11, "Premisa: el curso tiene más de un tipo de horario en SCACRSE"),
                        (12, "Premisa: horas crédito del NRC teórico")),
    "ssasect_liga": _l("5.3-ligas", (14, "SSASECT: nombre de la liga del NRC"), (15, "SSASECT: identificador de liga")),
    "ssadetl": _l("5.3-ligas", (16, "SSADETL: liga que se valida al inscribir"), (17, "SSADETL: conector de la liga"),
                  (18, "SSADETL: guardar la liga")),
    "ligas_inscripcion": _l("5.3-ligas", (24, "Inscripción por autoservicio con ligas")),
    # Notas, asistencia y cierre
    "shagrde": _l("7.1.3", (13, "SHAGRDE: crear el código de calificación"), (15, "SHAGRDE: contar en intentadas, aprobadas y ganadas"),
                  (16, "SHAGRDE: modos de calificación del código")),
    "shaegbc": _l("7.1.4", (40, "SHAEGBC: calendario del periodo"), (41, "SHAEGBC: fechas de ingreso de calificaciones")),
    "shagcom": _l("7.1.4", (43, "SHAGCOM: requisitos, periodo y NRC"), (44, "SHAGCOM: escala de calificación del plan"),
                  (45, "SHAGCOM: secuencia y nombre del componente"), (46, "SHAGCOM: descripción y peso"),
                  (48, "SHAGCOM: incluir en la calificación final")) +
               _l("7.1.0", (29, "ATTRGRD: peso 0, Debe aprobar y escala de asistencia")),
    "shagcom_attrgrd": _l("7.1.0", (29, "ATTRGRD: peso 0, Debe aprobar y escala de asistencia")) +
                       _l("7.1.4", (44, "SHAGCOM: escala de calificación del plan")),
    "soaatrk": _l("7.1.1", (34, "SOAATRK: periodo de las reglas"), (35, "SOAATRK: criterio de la regla"),
                  (36, "SOAATRK: materia y número de curso"), (37, "SOAATRK: Desplegar clase y control de asistencia")),
    "pasar_lista": _l("7.1.1", (44, "Autoservicio: «Pasar lista» del NRC y la sesión"), (45, "Registrar asistencia o ausencia"),
                      (46, "Marcas de presente y ausente"), (48, "Opciones de «Actualizar todo»"),
                      (56, "Pasar la asistencia a calificaciones"), (57, "Confirmar el paso del porcentaje al componente")),
    "libro": _l("7.1.4", (62, "Autoservicio: Libro de calificaciones"), (64, "Elegir el NRC y abrir Componentes"),
                (66, "Componentes del NRC"), (67, "Calificación de cada alumno"), (68, "Guardar las calificaciones"),
                (75, "Calificaciones compuestas")),
    "nota_final": _l("7.1.4", (77, "La nota calculada pasa a la lista de clase")) +
                  _l("7.1.6", (15, "SFASLST: periodo y NRC")),
    "sfaslst": _l("7.1.6", (15, "SFASLST: periodo y NRC"), (16, "SFASLST: calificaciones de cada alumno"),
                  (17, "SFASLST: comentario y guardar")),
    "sfaslst_lista": _l("7.1.6", (15, "SFASLST: periodo y NRC")),
    "shrroll": _l("7.1.9", (22, "GJAPCTL: proceso SHRROLL"), (23, "SHRROLL: impresora y parámetros"),
                  (25, "SHRROLL: enviar y guardar"), (27, "Revisar la salida en GJIREVO")),
    "smarqcm": _l("7.2.4", (30, "SMARQCM: ID del alumno"), (32, "SMARQCM: nueva solicitud de cumplimiento"),
                  (33, "SMARQCM: parámetros heredados de SMADFLT"), (41, "SMARQCM: abrir los resultados en SMICRLT")),
    "smicrlt": _l("7.1.9", (61, "SMICRLT: alumno y solicitud"), (63, "SMICRLT: resultados del CAPP"),
                  (80, "SMICRLT: cursos no usados")),
}

CREAR_NRC = {
    "s1": _l("5.3", (19, "Ingresar el periodo y pulsar «Crear NRC»"), (20, "El NRC queda en ADD hasta el primer guardado")),
    "s2": _l("5.3", (21, "Materia, número de curso, sección, campus y estatus"),
             (22, "Tipo de horario, método educativo, modo de calificar y sesión"),
             (23, "Parte de periodo y horas crédito"), (24, "Calificable, horas de cobro, sin dispensa, y guardar"),
             (26, "Al guardar, Banner asigna el número de NRC")),
    "s3": _l("5.3", (27, "Detalles de ingreso: cupo del NRC y guardar")),
    "s4": _l("5.3", (28, "Lugares reservados: regla nula y regla por criterio")),
    "s5": [{"instructivo": "5.3", "n": 29, "texto": "Fechas de reunión: horas, días e indicador de sesión", "caja": [0.034, 0.118, 0.0, 0.0]}] +
          _l("5.3", (30, "Créditos y ubicación: horas por semana calculadas")) +
          _l("6.2.1", (15, "Bloque Instructor: ID del docente")) +
          [{"instructivo": "6.2.1", "n": 19, "texto": "Responsabilidad, docente principal, sobrepaso y porcentaje de sesión",
            # El 4 de la lámina es el sobrepaso del docente; la fila de la guía es el del horario (aula virtual).
            "sin_marca": ["Indicador de sobrepaso (horario)"]}] +
          _l("6.2.1", (20, "Conflicto de horario del docente: indicador de sobrepaso")),
}

BASE = {
    "crear-el-nrc": CREAR_NRC,
    "carga-lectiva": {"k1": "siainst", "k2": "ssasect_docente", "k3": "siaasgn"},
    "persona-y-admision": {"a1": "goamtch", "a2": "spaiden", "a3": "saaquik", "a4": "saaquik_curr", "a5": "sgastdn"},
    "matricula-en-el-nrc": {"i2": "sfaregs_autorizar", "i3": "sfaregs_inscribir", "i4": "tsaarev", "i5": "sfaslst_lista"},
    "notas-y-pase-a-historia": {"n1": "shaegbc", "n2": "shagcom", "n3": "soaatrk", "n4": "pasar_lista",
                                "n5": "libro", "n6": "nota_final", "n7": "shrroll"},
    "ligas-teorico-y-club": {"g1": "scacrse_ligas", "g2": "ssasect_liga", "g3": "ssasect_liga", "g4": "ssadetl",
                             "g5": "ligas_inscripcion", "g6": "sfaslst_lista"},
}

# Casuísticas: (página, palabras de la fase, tema). Gana la primera regla que coincide.
REGLAS = [
    ("SFAREGS", r"reintento|exitosa|cruzada|multiescuela|directa|asignaci[oó]n de cupo", "sfaregs_inscribir"),
    ("SFAREGS", r"plan|autoriz|elegib|habilitar", "sfaregs_autorizar"),
    ("SFAREGS", r"rec[aá]lculo|financ", "tsaarev_retiro"),
    ("SFAREGS", r"retiro|\bdd\b|traslado|consulta", "sfaregs_retiro"),
    ("SFAREGS", r"permiso|sobrepaso", "sfaregs_sobrepaso"),
    ("SFAREGS", r"bloque|saturaci|error|fatal|intento", "sfaregs_error"),
    ("SFAREGS", r".", "sfaregs_inscribir"),
    ("SSASECT", r"horario|conflicto|asignar a secci", "ssasect_horario"),
    ("SSASECT", r"especial|crear", "ssasect_crear"),
    ("SSASECT", r".", "ssasect_cupo"),
    ("SGASTDN", r"curr[ií]cula|programa|nivel|triple|doble|expediente", "sgastdn_doble"),
    ("SGASTDN", r".", "sgastdn"),
    ("SHAGCOM", r"attrgrd", "shagcom_attrgrd"),
    ("TSAAREV", r".", "tsaarev"), ("SFASLST", r".", "sfaslst"), ("GJAPCTL", r".", "shrroll"),
    ("SHAGRDE", r".", "shagrde"), ("SHAEGBC", r".", "shaegbc"), ("SHAGCOM", r".", "shagcom"),
    ("STVTERM", r".", "periodo"), ("STVPTRM", r".", "partes"), ("SOATERM", r".", "soaterm"), ("SIATERM", r".", "siaterm"),
    ("STVMAJR", r".", "stvmajr"), ("SMAPRLE", r".", "smaprle"), ("SOACURR", r".", "soacurr"), ("SMAPROG", r".", "smaprog"),
    ("SHATRNS", r".", "shatrns"), ("SOAHOLD", r".", "soahold"), ("SMARQCM", r".", "smarqcm"), ("SMICRLT", r".", "smicrlt"),
    ("SOATEST", r".", "soatest"), ("SCAPREQ", r".", "scapreq"), ("SFAROVR", r".", "sfarovr"), ("SFASRPO", r".", "sfasrpo"),
    ("SIAASGN", r".", "siaasgn"), ("SIAINST", r".", "siainst"),
]


def para(slug, paso, info):
    """Lista de diapositivas {instructivo, n, texto…} para un paso de una guía; [] si no hay."""
    base = BASE.get(slug)
    if base is not None:
        valor = base.get(paso)
        return list(TEMAS[valor] if isinstance(valor, str) else (valor or []))
    if not slug.startswith("script-"):
        return []
    pantalla = (info.get("pantalla") or "").split()[0].upper() if info.get("pantalla") else ""
    fase = (info.get("fase", "") + " " + info.get("hito", "")).lower()
    for codigo, patron, tema in REGLAS:
        if pantalla == codigo and re.search(patron, fase):
            return list(TEMAS[tema])
    return []
