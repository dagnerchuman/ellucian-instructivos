"""Plantillas de los diagramas paso a paso de cada centro (especificaciones Archify).

Tres reglas de diseño, iguales en todos los diagramas:
1. **Un solo flujo por diagrama.** Los pasos van en una sola línea, de izquierda a derecha
   (o de arriba abajo en el recorrido, que es una secuencia). No hay ramas ni casos
   paralelos: los errores y las variantes van en las tarjetas, y cada casuística tiene
   su propio diagrama.
2. **Un solo código por paso.** El título del paso es una sola página de Banner
   (SSASECT, SFAREGS…) o, si el paso ocurre fuera de Banner, un solo término (Oficio,
   Autoservicio). Debajo va la acción en pocas palabras y, en la etiqueta, el dato de TEST.
3. **Un solo término por concepto.** Se usan siempre las palabras de TERMINOS: alumno,
   NRC, parte, matrícula, cupo, pase a historia… Nunca sus sinónimos.

Cada plantilla recibe un Centro y las traducciones de la interfaz, y devuelve
(tipo, especificación). Lo que cambia por centro sale de centros/<centro>/datos.json.

Reglas de Archify que estas plantillas respetan (las valida `finalize`):
- columnas 0..5 en flujos y un nodo por carril y columna;
- títulos de nodo cortos (un código) y etiquetas de hasta unos 38 caracteres;
- ancho total ≤ 1240 px; en la secuencia, relación ancho/alto de 1,55 o más.
"""
import re
import unicodedata

from centro import leer_json, CENTROS, Centro, centros_disponibles

# --------------------------------------------------------------------------- términos
TERMINOS = {
    "alumno": "Persona admitida en un programa del centro, de la USS o externa. No se dice «participante» ni «estudiante».",
    "persona": "Registro en GOAMTCH, antes de admitirla. Al admitirla pasa a ser alumno.",
    "NRC": "Curso programado en un periodo y una parte. No se dice «sección» ni «grupo».",
    "parte": "Parte de periodo (X07, I08, P06…), con sus fechas y semanas.",
    "matrícula": "El alumno queda en el NRC con RE en SFAREGS. No se dice «inscripción».",
    "retiro": "DD en SFAREGS: el alumno sale del NRC y libera el cupo.",
    "cupo": "Máximo de alumnos del NRC. No se dice «vacante» ni «capacidad».",
    "carga lectiva": "Horas del docente en sus NRC, que se ven en SIAASGN.",
    "pase a historia": "SHRROLL lleva las notas a la historia académica. No se dice «cierre de actas».",
    "retención": "Bloqueo en SOAHOLD que impide la matrícula.",
    "INH": "Nota de inhabilitado: asistencia menor al mínimo. No aprueba ni da créditos, aunque el promedio apruebe.",
    "liga": "Unión de dos o más NRC del mismo curso que el alumno matricula juntos, como el NRC teórico y el club de conversación de Inglés. Es el término de Banner en español.",
}

ESTADO_TEXTO = {
    "validado": "validado en TEST",
    "pendiente": "pendiente en TEST",
    "por probar": "por probar en TEST",
    "no aplica": "no aplica",
    "por definir": "por definir",
}

CITAS = {
    "periodo": "Periodo y partes: instructivos 1.1.1 y 1.1.2",
    "mallas": "Programas y mallas: instructivos 1.1.3 (STVMAJR, SOACURR) y 1.2.1 (SMAPROG, SMAAREA)",
    "catalogo": "Catálogo y prerrequisitos: instructivos 1.1.4 (SCACRSE) y 1.1.5 (SCAPREQ)",
    "nrc": "NRC en SSASECT: instructivo 5.3, diap. 19 a 32",
    "docente": "Docente en SIAINST: instructivo 5.2 Información de docentes, diap. 16 a 20",
    "carga": "Carga lectiva en SIAASGN: instructivo 5.2 Carga de trabajo, diap. 21 a 27",
    "contrato": "Análisis por contrato en SIACONA: instructivo 5.2 Carga de trabajo, diap. 36 a 42",
    "persona": "Persona: instructivo 5.1.1 (GOAMTCH)",
    "admision": "Admisión rápida: instructivo 3.2.1 (SAAQUIK)",
    "estudiante": "Registro del alumno: instructivo 4.1.1 (SGASTDN)",
    "matricula": "Matrícula, sobrepasos y retiro: instructivo 5.4 (SFAREGS)",
    "retencion": "Retenciones: instructivos 5.2.1 y 5.2.2 (SOAHOLD)",
    "escala": "Escalas y modos: instructivo 7.1.3, diap. 16 (SHAGRDE)",
    "notas": "Plan de evaluación y notas: instructivos 7.1.4 (SHAGCOM) y 7.1.6 (SFASLST)",
    "calendario": "Calendario de ingreso de calificaciones: instructivo 7.1.4, diap. 40–43 (SHAEGBC)",
    "asistencia_componente": "Componente ATTRGRD: instructivo 7.1.0, diap. 29–30; 7.1.4, diap. 55",
    "asistencia_regla": "Regla de asistencia y Pasar lista: instructivo 7.1.1, diap. 34–48 (SOAATRK, Autoservicio)",
    "asistencia_envio": "Envío de la asistencia al libro: instructivo 7.1.0, diap. 11–26 (GORICCR, GORRSQL, STVGCHG)",
    "cierre": "Pase a historia: instructivo 7.1.9 (SHRROLL)",
    "capp": "CAPP: instructivo 7.2.4, diap. 30 a 55",
    "convalidacion": "Convalidación y homologación: capacidad 3.3.1, diap. 33 a 36 (SHATRNS) y diap. 47 a 56 (SHATFAC)",
    "egreso": "Requisito de egreso de Pregrado: instructivo 8, diap. 13",
    "ligas": "Ligas: instructivo 5.3_4.1.4.1.9 Crear Ligas, diap. 9 a 24; verificación «Ligas» en SOATERM: 5.4_4.1.4.1.12, diap. 15",
    "solicitudes": "Solicitudes de servicio: instructivo 4.3.2, diap. 10 a 15 (Autoservicio) y 17 a 21 (SVASVPR); servicios en 4.3.1",
}

LEYENDA_FLUJO = {
    "mode": "auto",
    "entries": {
        "backend": {"label": "Banner: se registra"},
        "database": {"label": "Banner: se consulta"},
        "frontend": {"label": "Autoservicio (web)"},
        "messagebus": {"label": "Proceso masivo"},
        "cloud": {"label": "Cobro (Finanzas)"},
        "external": {"label": "Fuera de Banner"},
        "security": {"label": "Situación o bloqueo"},
    },
}

LEYENDA_SECUENCIA = {
    "mode": "auto",
    "entries": {
        "emphasis": {"label": "Paso en Banner"},
        "default": {"label": "Trámite entre personas"},
        "return": {"label": "Lo que recibe"},
    },
}


def slug(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


SCRIPTS_COMUN = leer_json(CENTROS / "comun" / "datos.json")["scripts"]
CATALOGO = {s["id"]: s["nombre"] for s in SCRIPTS_COMUN}


def slug_script(id_script):
    return f"script-{id_script.lower()}-{slug(CATALOGO[id_script])}"


TITULOS = {
    "tres-centros": "El mismo flujo en los tres centros",
    "recorrido-completo": "Recorrido completo en Banner",
    "crear-el-nrc": "Crear el NRC",
    "carga-lectiva": "Script 18-A · Carga lectiva del docente",
    "persona-y-admision": "Persona y admisión",
    "matricula-en-el-nrc": "Script 01 · Matrícula en el NRC",
    "notas-y-pase-a-historia": "Scripts 13 y 14 · Notas y pase a historia",
    "ligas-teorico-y-club": "Ligas: NRC teórico + club de conversación",
    **{slug_script(i): f"Script {i} · {n}" for i, n in CATALOGO.items()},
}

CAPACIDADES = {
    "tres-centros": "Capacidades 1 a 8",
    "recorrido-completo": "Capacidades 1 a 8",
    "crear-el-nrc": "Capacidades 1 y 5",
    "carga-lectiva": "Capacidad 5",
    "persona-y-admision": "Capacidades 3, 4 y 5",
    "matricula-en-el-nrc": "Capacidades 5 y 11",
    "notas-y-pase-a-historia": "Capacidades 7 y 8",
    "ligas-teorico-y-club": "Capacidad 5",
    **{slug_script(s["id"]): s.get("capacidad", "") for s in SCRIPTS_COMUN},
}

# Demostraciones para reuniones (datos.json › demostraciones de cada centro): su título y capacidad.
DEMOSTRACIONES = {d["slug"]: d for _id in centros_disponibles()
                  for d in leer_json(CENTROS / _id / "datos.json").get("demostraciones", [])}
TITULOS.update({k: d["titulo"] for k, d in DEMOSTRACIONES.items()})
CAPACIDADES.update({k: d.get("capacidad", "") for k, d in DEMOSTRACIONES.items()})

CAPACIDADES_DETALLE = {
    "tres-centros": "Capacidades 1 a 8 · Visión comparativa integral",
    "recorrido-completo": "Capacidades 1 a 8 · Ciclo integral en Banner",
    "crear-el-nrc": "Capacidad 1.1 (Catálogo) y 5.3 (Programar NRC)",
    "carga-lectiva": "Capacidad 5.2 · Carga de trabajo docente",
    "persona-y-admision": "Capacidad 5.1 (Persona) y 3.2 (Admisión)",
    "matricula-en-el-nrc": "Capacidad 5.4 (Inscripción) y 11.1 (Cobranzas)",
    "notas-y-pase-a-historia": "Capacidad 7.1 (Calificaciones) y 8 (CAPP)",
    "ligas-teorico-y-club": "Capacidad 5.3 · Crear Ligas (SSADETL)",
    **{slug_script(s["id"]): s.get("capacidad_nombre", "") for s in SCRIPTS_COMUN},
}


# --------------------------------------------------------------------------- ayudas
def salida(c, numero, slug_):
    """Ruta relativa del HTML: centros/<centro>/diagramas/NN-slug/<centro>-NN-slug.html"""
    return f"centros/{c.id}/diagramas/{numero:02d}-{slug_}/{c.id}-{numero:02d}-{slug_}.html"


def vista(id_, etiqueta, foco, nota):
    return {"id": id_, "label": etiqueta, "focus": foco, "note": nota}


def paso(id_, carril, col, codigo, accion, dato=None, tipo="backend", icono=None, ancho=150):
    """Un paso = un código (o un término) + la acción + el dato de TEST."""
    n = {"id": id_, "lane": carril, "col": col, "type": tipo, "label": codigo, "sublabel": accion, "width": ancho}
    if dato:
        n["tag"] = dato
    if icono:
        n["icon"] = icono
    return n


def encadenar(nodos):
    """Flechas del único flujo: cada paso con el siguiente."""
    return [{"id": f"e-{a['id']}-{b['id']}", "from": a["id"], "to": b["id"], "variant": "emphasis"}
            for a, b in zip(nodos, nodos[1:])]


def tarjetas(c, probado, ellucian, extra=None):
    t = [{"dot": "emerald", "title": "Probado en TEST", "items": probado}]
    if extra:
        t += extra
    t.append({"dot": "cyan", "title": "En Ellucian (instructivos)", "items": ellucian})
    t.append({"dot": "amber", "title": "Por confirmar", "items": c.dudas()})
    return t


def tarjeta_terminos(*claves):
    return {"dot": "violet", "title": "Términos", "items": [f"{k}: {TERMINOS[k]}" for k in claves]}


def flujo(c, numero, slug_, carriles, nodos, cards, fases=None, vistas=None, title_override=None, subtitle_override=None):
    cap = CAPACIDADES.get(slug_, "")
    cap_sufijo = f" ({cap})" if cap and not slug_.startswith("script-") else ""
    title = title_override or f"{c.nombre} · {numero}. {TITULOS[slug_]}{cap_sufijo}"
    subtitle = subtitle_override or c.subtitulo(CAPACIDADES_DETALLE.get(slug_))
    m = {
        "title": title,
        "subtitle": subtitle,
        "locale": "es",
        "translations": c.tr,
        "output": salida(c, numero, slug_),
        "quality_profile": "showcase",
        "animation": "trace",
        "legend": LEYENDA_FLUJO,
    }
    if vistas:
        m["views"] = vistas
    spec = {"schema_version": 2, "diagram_type": "workflow", "meta": m, "lanes": carriles}
    if fases:
        spec["phases"] = fases
    spec["mainPath"] = [n["id"] for n in nodos]
    spec.update({"nodes": nodos, "edges": encadenar(nodos), "cards": cards})
    return "workflow", spec


def evidencia(c, ids):
    """Evidencia de TEST de los scripts indicados (solo los validados)."""
    items = [f"Script {i}: {c.script(i)['evidencia']}" for i in ids if c.script(i)["estado"] == "validado"]
    return items or ["Este flujo todavía no se probó con este centro en TEST"]


def dato_nrc(c, prefijo=""):
    return f"{prefijo}NRC {c.nrc_ejemplo}" if c.nrc_ejemplo else f"{prefijo}NRC por crear"


# --------------------------------------------------------------------------- 1
def actores_recorrido(c):
    """(participantes, tramos) del recorrido completo; tramo = (nombre, [(de, a, página, variante, qué hace)])."""
    participantes = [
        {"id": "alumno", "type": "external", "label": "Alumno", "sublabel": "USS o externo", "icon": "person"},
        {"id": "asistente", "type": "backend", "label": "Asistente", "sublabel": "o especialista", "icon": "briefcase"},
        {"id": "jefe", "type": "backend", "label": "Jefe del centro", "sublabel": c.d.get("alias") or c.nombre.split()[-1], "icon": "briefcase"},
        {"id": "banner", "type": "database", "label": "Banner", "sublabel": f"TEST · {c.periodo_ejemplo}"},
        {"id": "docente", "type": "frontend", "label": "Docente", "sublabel": "autoservicio", "icon": "person"},
        {"id": "registros", "type": "messagebus", "label": "Registros", "sublabel": "Académicos"},
        {"id": "vra", "type": "external", "label": "Vicerrectorado", "sublabel": "Académico", "icon": "flag"},
    ]
    tramos = [
        ("Preparar", [
            ("registros", "banner", "SOATERM", "emphasis", f"crea periodo en STVTERM, valida malla y abre parte {c.parte_ejemplo}"),
            ("jefe", "banner", "SSASECT", "emphasis", f"crea el NRC y asigna al docente ({dato_nrc(c)})"),
            ("jefe", "banner", "SIAASGN", "emphasis", "revisa la carga lectiva del docente"),
            ("jefe", "vra", "Oficio", "default", "envía la carga con su visto bueno por la intranet"),
            ("vra", "jefe", "Resolución", "return", "el Vicerrector aprueba la carga lectiva"),
        ]),
        ("Matricular", [
            ("alumno", "asistente", "Solicitud", "default", "el alumno pide el curso (USS o externo)"),
            ("asistente", "banner", "GOAMTCH", "emphasis", "busca o crea a la persona"),
            ("asistente", "banner", "SAAQUIK", "emphasis", f"admite al alumno en el programa {c.programa}"),
            ("asistente", "banner", "SFAREGS", "emphasis", "matricula al alumno en el NRC (RE)"),
            ("banner", "alumno", "TSAAREV", "return", "el alumno recibe el cobro en su cuenta"),
        ]),
        ("Dictar y cerrar", [
            ("docente", "banner", "Autoservicio", "emphasis", "el docente pasa lista y registra las notas en el libro; Registros carga antes el plan (SHAGCOM) y la regla de asistencia (SOAATRK)"),
            ("registros", "banner", "SHRROLL", "emphasis", "revisa la nota final en SFASLST y hace el pase a historia"),
            ("banner", "alumno", "SMICRLT", "return", "el alumno ve su avance en CAPP"),
        ]),
    ]
    return participantes, tramos


def guia_recorrido(c):
    """Guía de cada actor del recorrido: los pasos que hace o recibe, en orden, con las láminas de sus páginas."""
    from guias_operativas import _fila
    from diapositivas_pasos import para_recorrido
    participantes, tramos = actores_recorrido(c)
    nombre = {p["id"]: p["label"] for p in participantes}
    guia = {}
    for p in participantes:
        filas, paginas, n = [], [], 0
        for tramo, pasos in tramos:
            for de, a, etiqueta, _, explica in pasos:
                n += 1
                if p["id"] not in (de, a):
                    continue
                hace = p["id"] == de
                filas.append(_fila(f"{n}. {etiqueta}", explica[:1].upper() + explica[1:],
                                   f"{'Hace' if hace else 'Recibe'} · {tramo}", "Acción" if hace else "Verificación",
                                   f"Paso {n} del recorrido ({tramo}): {nombre[de]} → {nombre[a]}."))
                if hace or p["id"] in ("alumno", "banner"):
                    paginas.append(etiqueta)
        guia[p["id"]] = {"titulo": TITULOS["recorrido-completo"], "pantalla": p["label"],
                         "fase": f"{p['label']}: qué hace en el recorrido", "hito": p.get("sublabel", ""),
                         "instrucciones": filas,
                         "diapositivas": para_recorrido(paginas, 1 if p["id"] == "banner" else 2)}
    return guia


def recorrido(c):
    """Secuencia: quién hace cada paso, de abrir el periodo al avance en CAPP."""
    participantes, tramos = actores_recorrido(c)
    mensajes, segmentos, vistas, que_hace = [], [], [], []
    y = 182
    for k, (nombre, pasos) in enumerate(tramos):
        if k:
            y += 24
        inicio, ids = y, []
        for de, a, etiqueta, variante, explica in pasos:
            mid = f"m{len(mensajes) + 1}"
            mensajes.append({"id": mid, "from": de, "to": a, "y": y, "label": etiqueta, "variant": variante})
            que_hace.append(f"{len(mensajes)}. {etiqueta}: {explica}")
            ids.append(mid)
            y += 28
        segmentos.append({"from": inicio - 16, "to": y - 14, "label": nombre})
        vistas.append(vista(f"v{k}", nombre, ids, " · ".join(p[2] for p in pasos)))
    probado = {
        "computacion": [
            "SOATERM: 202656 con X01–X07 y 202751 con X01 (Script 11)",
            "SSASECT: NRC 1021, 1024 y 1026; SIAASGN: 4 NRC del docente 100582059",
            "GOAMTCH y SAAQUIK: S00581081 y S00581108 a S00581111 con CMEMC38",
            "SFAREGS: matrícula, retiro, traslado y sobrepasos (Scripts 01, 02, 08, 16)",
            "Autoservicio: Pasar lista y libro de calificaciones con el NRC 10044 (asistencia 43 % → INH en SFASLST)",
            "SFASLST y SHRROLL: notas 16, 10, 08 e INH; job 8114 exitoso",
        ],
        "idiomas": ["Todavía no hay un NRC de Idiomas en TEST",
                    "El flujo es el mismo que se validó en Computación; falta probarlo con el nivel I"],
        "emprendimiento": ["SIAASGN: NRC 1025 (ESGE 00117) en la carga del docente",
                           "Falta probar matrícula, notas y pase a historia con el nivel M"],
    }[c.id]
    m = {
        "title": f"{c.nombre} · 1. {TITULOS['recorrido-completo']} (Capacidades 1 a 8)",
        "subtitle": c.subtitulo(CAPACIDADES_DETALLE["recorrido-completo"]),
        "locale": "es",
        "translations": c.tr,
        "output": salida(c, 1, "recorrido-completo"),
        "quality_profile": "showcase",
        "animation": "trace",
        "column_fit": "spread",
        "viewBox": [1080, y + 96],
        "legend": LEYENDA_SECUENCIA,
        "views": vistas,
    }
    spec = {
        "schema_version": 1, "diagram_type": "sequence", "meta": m,
        "participants": participantes, "segments": segmentos, "messages": mensajes,
        "cards": [
            {"dot": "violet", "title": "Qué hace cada paso", "items": que_hace},
            *tarjetas(c, probado, [CITAS["periodo"], CITAS["nrc"], CITAS["carga"], CITAS["admision"],
                                   CITAS["matricula"], CITAS["cierre"], CITAS["capp"], CITAS["egreso"]],
                      [{"dot": "rose", "title": "Lo propio del centro", "items": c.d["particularidades"]}]),
        ],
    }
    return "sequence", spec


# --------------------------------------------------------------------------- 2
def crear_nrc(c):
    """SSASECT: sección, cupo, lugares reservados y horario/docente; auditoría en SSASECQ."""
    n = c.nrc(c.nrc_ejemplo) if c.nrc_ejemplo else None
    cupo = f" · cupo {n['cupo'].split(' (')[0]}" if n and n.get("cupo") else ""
    nrc_num = c.nrc_ejemplo or "1026"
    nodos = [
        paso("s1", "nrc", 0, "SSASECT", "bloque clave", f"{c.periodo_ejemplo} · ADD en blanco", icono="start"),
        paso("s2", "nrc", 1, "SSASECT", "info de sección", f"1.er guardar · NRC {nrc_num}", icono="database"),
        paso("s3", "nrc", 2, "SSASECT", "definir el cupo", "Proyectado (ej. 40)", icono="success"),
        paso("s4", "nrc", 3, "SSASECT", "reservar cupos", "Lugares reservados · botón +", tipo="security", icono="security"),
        paso("s5", "nrc", 4, "SSASECT", "horario y docente", "guardar · SAUVIR y profesor", icono="clock"),
        paso("s6", "nrc", 5, "SSASECQ", "publicar y auditar", "NRC activo y publicado", tipo="database", icono="success"),
    ]
    probado = {
        "computacion": [
            "NRC 1021: ESEC 00650, sección B, parte X07 (28/09)",
            "NRC 1026: sección D, lunes y miércoles 08:00–12:00, aula SAUVIR, cupo 1 → 4 (02/10)",
            "NRC de prueba ESEC 00650 A en 202751, parte X01 (Script 11, 05/10)",
            "NRC 10044: ESEC 00684 Diseño Web, sección A, X06, cupo 40, SAUVIR / SALA-VIRT con sobrepaso O (23/10)",
        ],
        "idiomas": ["Todavía no hay un NRC de Idiomas en TEST"],
        "emprendimiento": ["NRC 1025: ESGE 00117, sección A, con el docente en la sesión 02 (no principal)"],
    }[c.id]
    errores = {"dot": "rose", "title": "Si sale un error", "items": [
        "«Debe guardar antes de salir»: guarda en cada pestaña antes de pasar a la siguiente",
        "«Closed» al matricular: el NRC está lleno; sube el cupo (Script 15)",
        "«Sesión sin horas»: usa la misma sesión (01) en el horario y en el docente",
        "«Conflicto de salón» con SAUVIR / SALA-VIRT: pon la letra O en «Indicador de sobrepaso» del horario (C97)",
        "«Proyectado» es obligatorio: llénalo antes de abrir «Lugares reservados» (C97)",
        "Al crear un NRC nuevo, campus, estatus y tipo de horario son obligatorios",
        "Para pasar al bloque del docente usa «Sección siguiente»; el clic directo da error",
    ]}
    reservas = {"dot": "violet", "title": "Cupos reservados: dónde y cómo", "items": [
        "En SSASECT > Información de ingreso de sección > Detalles de ingreso: escribir el cupo total en Proyectado (ejemplo: 40)",
        "En SSASECT > Lugares reservados: conservar la regla nula; usar + para una fila con criterio y Máximo reservado (ejemplo: 40)",
        "La fila puede filtrar por nivel, campus, escuela, grado, programa, campo de estudio, departamento, currículo, clase, atributo, cohorte o periodos",
        "SSARRES no reserva cupos: restringe quién puede matricularse en el NRC",
        "Para un alumno identificado se usa un sobrepaso de capacidad en SFAROVR/SFASRPO; no es una reserva previa",
    ]}
    return flujo(
        c, 2, "crear-el-nrc",
        [{"id": "nrc", "label": "Programar el NRC"}],
        nodos,
        tarjetas(c, probado, [CITAS["periodo"], CITAS["catalogo"], CITAS["nrc"]],
                 [reservas, errores, tarjeta_terminos("NRC", "parte", "cupo")]),
        fases=[
            {"id": "f0", "label": "SSASECT: Bloque y Sección", "fromCol": 0, "toCol": 1},
            {"id": "f1", "label": "SSASECT: Cupo, Reserva, Horario y Docente", "fromCol": 2, "toCol": 4, "variant": "emphasis"},
            {"id": "f2", "label": "Consulta oficial", "fromCol": 5, "toCol": 5},
        ],
    )


# --------------------------------------------------------------------------- 3
def carga_lectiva(c):
    """SIAINST → SSASECT → SIAASGN en Banner; oficio y resolución en la intranet (C47, C48)."""
    docente = c.d.get("docente_test")
    nodos = [
        paso("k1", "jefe", 0, "SIAINST", "activar al docente", docente["id"] if docente else "docente por definir", icono="person"),
        paso("k2", "jefe", 1, "SSASECT", "asignar al NRC", "principal al 100 %"),
        paso("k3", "jefe", 2, "SIAASGN", "revisar la carga", "horas y FTE por NRC", "database", icono="clock"),
        paso("k4", "jefe", 3, "Oficio", "dar el visto bueno", "intranet · n.º de oficio", "external", icono="flag"),
        paso("k5", "vra", 4, "Resolución", "aprobar la carga", "la emite el Vicerrector", "external", icono="success"),
    ]
    probado = {
        "computacion": ["SIAASGN: docente 100582059 con 4 NRC (1021, 1022, 1024 y 1025), horas y FTE (Script 18-A, 02/10)",
                        "El oficio y la resolución se tramitan fuera de Banner (C48)"],
        "idiomas": ["Todavía no hay un docente de Idiomas en TEST"],
        "emprendimiento": ["SIAASGN: el NRC 1025 aparece en la carga del docente 100582059 (Script 18-A)"],
    }[c.id]
    falta = {"dot": "rose", "title": "Falta del script 5.2", "items": [
        "Labor no educativa del docente en SIAASGN (pendiente)",
        "Análisis por contrato en SIACONA (pendiente; responsable: Pedro Martinto)",
    ]}
    return flujo(
        c, 3, "carga-lectiva",
        [{"id": "jefe", "label": "Jefe del centro"}, {"id": "vra", "label": "Vicerrectorado Académico"}],
        nodos,
        tarjetas(c, probado, [CITAS["docente"], CITAS["nrc"], CITAS["carga"], CITAS["contrato"]],
                 [falta, tarjeta_terminos("carga lectiva", "NRC")]),
        fases=[
            {"id": "f0", "label": "En Banner", "fromCol": 0, "toCol": 2, "variant": "emphasis"},
            {"id": "f1", "label": "En la intranet", "fromCol": 3, "toCol": 4, "variant": "dashed"},
        ],
    )


# --------------------------------------------------------------------------- 4
def persona_admision(c):
    """GOAMTCH (persona) → SAAQUIK (admisión) → SGASTDN (alumno activo)."""
    id_nuevo = c.d["persona_ejemplo"] or "ID S00… nuevo"
    revisar = f"estatus AS · mayor {c.mayor}" if c.confirmado_en_test else "estatus AS"
    nodos = [
        paso("a1", "asis", 0, "GOAMTCH", "buscar a la persona", "evitar duplicados", icono="person"),
        paso("a2", "asis", 1, "GOAMTCH", "crear a la persona", id_nuevo, icono="person"),
        paso("a3", "asis", 2, "SAAQUIK", "admitir al programa", f"{c.periodo_ejemplo} · nivel {c.nivel}"),
        paso("a4", "asis", 3, "SAAQUIK", "elegir el programa", f"programa {c.programa}"),
        paso("a5", "asis", 4, "SGASTDN", "revisar al alumno", revisar, "database"),
    ]
    probado = {
        "computacion": ["Personas S00581081 y S00581108 a S00581111 creadas en GOAMTCH",
                        "Admisión con CMEMC38: se completan ACXP, EMCI e INPROGRESS",
                        "S00581110 admitido el 05/10 para el Script 02"],
        "idiomas": ["Falta conocer el programa de Idiomas en TEST"],
        "emprendimiento": ["Falta conocer el programa de Emprendimiento en TEST"],
    }[c.id]
    casos = {"dot": "rose", "title": "Si pasa esto", "items": [
        "La persona ya existe (mismo DNI o nombre): usa su ID actual y salta a SAAQUIK",
        f"Ya es alumno de Pregrado: se le agrega el programa del centro como segundo plan (Script 06, {ESTADO_TEXTO[c.script('06')['estado']]})",
        "Sirve igual para alumnos de la USS (Pregrado y Posgrado) y para externos",
    ]}
    return flujo(
        c, 4, "persona-y-admision",
        [{"id": "asis", "label": "Asistente o especialista"}],
        nodos,
        tarjetas(c, probado, [CITAS["persona"], CITAS["admision"], CITAS["estudiante"], CITAS["egreso"]],
                 [casos, tarjeta_terminos("persona", "alumno")]),
        fases=[
            {"id": "f0", "label": "Persona", "fromCol": 0, "toCol": 1},
            {"id": "f1", "label": "Admisión", "fromCol": 2, "toCol": 4, "variant": "emphasis"},
        ],
    )


# --------------------------------------------------------------------------- 5
def matricula(c):
    """SSASECQ → SFAREGS (EL, RE) → TSAAREV → SFASLST."""
    nodos = [
        paso("i1", "asis", 0, "SSASECQ", "revisar el cupo", dato_nrc(c), "database"),
        paso("i2", "asis", 1, "SFAREGS", "autorizar el plan", "estatus EL"),
        paso("i3", "asis", 2, "SFAREGS", "matricular en el NRC", "curso RE · cupo +1"),
        paso("i4", "asis", 3, "TSAAREV", "revisar el cobro", "cuenta del alumno", "cloud"),
        paso("i5", "asis", 4, "SFASLST", "revisar la lista", "lista del docente", "database"),
    ]
    bloqueos = {"dot": "rose", "title": "Si no deja matricular", "items": [
        f"Retención en SOAHOLD (Script 18-B, {ESTADO_TEXTO[c.script('18-B')['estado']]})",
        f"Estatus del alumno IS o SU en SGASTDN (Script 09, {ESTADO_TEXTO[c.script('09')['estado']]})",
        f"NRC lleno, error «Closed» (Script 15, {ESTADO_TEXTO[c.script('15')['estado']]})",
        "Mismo curso en otro NRC del periodo: «Duplicate Course with Section»",
        "El alumno no tiene currículo del nivel del curso: agrégalo en SFAREGS › Currículos y autoriza ese plan con EL (C100)",
        "Conflicto de horario con otro NRC del alumno: cambia el horario del NRC o elige otro",
    ] + (["BASIC II sin BASIC I: prerrequisito Fatal (Script 04)"] if c.prerrequisito_fatal else [])}
    return flujo(
        c, 5, "matricula-en-el-nrc",
        [{"id": "asis", "label": "Asistente o especialista"}],
        nodos,
        tarjetas(c, evidencia(c, ["01", "02", "15", "16"]), [CITAS["matricula"], CITAS["retencion"], CITAS["estudiante"]],
                 [bloqueos, tarjeta_terminos("matrícula", "retiro", "cupo", "retención")]),
        fases=[
            {"id": "f0", "label": "Antes", "fromCol": 0, "toCol": 0},
            {"id": "f1", "label": "SFAREGS", "fromCol": 1, "toCol": 2, "variant": "emphasis"},
            {"id": "f2", "label": "Después", "fromCol": 3, "toCol": 4},
        ],
    )


# --------------------------------------------------------------------------- 6
def notas(c):
    """SHAEGBC → SHAGCOM → SOAATRK → Autoservicio (asistencia, notas) → SFASLST → SHRROLL."""
    e = c.d["escala"]
    minimo = e["nota_minima"] if e else None
    asistencia = c.comun.get("asistencia_minima_porcentaje", {}).get("valor")
    asist_txt = f"{asistencia} %" if asistencia is not None else "por confirmar"
    prueba = c.d.get("flujo_notas_test")
    nrc = prueba["nrc"] if prueba else None
    nodos = [
        paso("n1", "ra", 0, "SHAEGBC", "abrir el calendario", f"{c.periodo_ejemplo} · fechas de notas"),
        paso("n2", "ra", 1, "SHAGCOM", "cargar el plan",
             f"NRC {nrc} · notas + ATTRGRD" if nrc else "componentes + ATTRGRD peso 0"),
        paso("n3", "ra", 2, "SOAATRK", "activar la asistencia", "regla del NRC · Presente/Ausente"),
        paso("n4", "doc", 3, "Autoservicio", "pasar lista",
             f"mínimo {asist_txt} de asistencia", "frontend"),
        paso("n5", "doc", 4, "Autoservicio", "notas por componente",
             "libro → nota compuesta", "frontend"),
        paso("n6", "ra", 5, "SFASLST", "revisar la nota final",
             f"aprueba con {minimo} · si no, INH" if minimo else "nota final o INH", "database"),
        paso("n7", "ra", 5, "SHRROLL", "pase a historia", "GJAPCTL · notas a la historia", "messagebus"),
    ]
    nodos[5]["yOffset"] = -46
    nodos[6]["yOffset"] = 46
    probado = (prueba["evidencia"] if prueba else []) + evidencia(c, ["13", "12", "14"])
    antes = {"dot": "violet", "title": "Antes de empezar", "items": [
        f"SHAGRDE: la escala del nivel {c.nivel} con el modo del curso ({c.escala}) y el código INH",
        f"Escala de asistencia para ATTRGRD con aprobatoria {asist_txt} (en Computación, AST_70)",
        "SSASECT: docente principal al 100 % en la sesión del horario",
        "SFAREGS: alumno con currículo del nivel del curso y matrícula RE en el NRC",
    ]}
    falla = {"dot": "rose", "title": "Si algo falla", "items": [
        "SHAGCOM pide «controles del libro de calificaciones»: configura antes SHAEGBC (C91)",
        "Pasar lista no muestra el NRC: falta la regla del NRC en SOAATRK (C101)",
        "El libro no muestra el NRC: debe tener docente, plan y alumnos matriculados (7.1.4, diap. 58)",
        "«Calificaciones finales» sin alumnos: es normal con libro; la nota pasa sola a SFASLST (C106)",
        "ATTRGRD vacío o viejo: el docente no lo envió; en Pasar lista, Clase › «Actualizar la asistencia en el libro» (C119)",
        "«No Substitute Grade» en el pase a historia: falta el modo del curso en SHAGRDE (U20)",
        f"Con asistencia menor a {asist_txt}, ATTRGRD (Debe aprobar) deja la nota final en INH aunque el promedio apruebe",
    ]}
    return flujo(
        c, 6, "notas-y-pase-a-historia",
        [{"id": "ra", "label": "Registros Académicos"}, {"id": "doc", "label": "Docente (Autoservicio)"}],
        nodos,
        tarjetas(c, probado, [CITAS["calendario"], CITAS["notas"], CITAS["asistencia_regla"],
                              CITAS["asistencia_componente"], CITAS["asistencia_envio"], CITAS["cierre"]],
                 [antes, falla, tarjeta_terminos("pase a historia", "INH", "alumno")]),
        fases=[
            {"id": "f0", "label": "Preparar el NRC", "fromCol": 0, "toCol": 2},
            {"id": "f1", "label": "Dictar y calificar", "fromCol": 3, "toCol": 4, "variant": "emphasis"},
            {"id": "f2", "label": "Cerrar", "fromCol": 5, "toCol": 5, "variant": "dashed"},
        ],
    )


# --------------------------------------------------------------------------- casuísticas
CASOS = {
    "01": (("Primera matrícula", "alumno admitido y activo"),
           [("SFAREGS", "autorizar plan", "casilla currícula · estatus EL"),
            ("SFAREGS", "inscribir en NRC", "código RE en asignatura"),
            ("SSASECT", "balance de cupos", "Actual +1 · Remaining -1"),
            ("TSAAREV", "auditoría cobros", "cálculo automático aranceles")],
           ("Matriculado al 100%", "cupo ocupado en NRC"), "matricula"),
    "03": (("Curso externo", "aprobado en otra institución"),
           [("SHATRNS", "materia externa", "ID S00581111 · IST150 (nota 16)"),
            ("SHATFAC", "acreditación facultad", "articulación y aprobación"),
            ("GJAPCTL", "pase a historia", "proceso SHRROLL · Job 8113"),
            ("SHASMRY", "historial y grado", "Rolled · Deg Created")],
           ("Convalidado al 100%", "CAPP acredita créditos"), "convalidacion"),
    "04": (("Suficiencia", "conocimientos previos"),
           [("SOATEST", "registrar puntaje", "código U01 · nota aprobatoria"),
            ("SCAPREQ", "validar prerrequisito", "equivalencia a BASIC I"),
            ("SFAREGS", "inscripción directa", "matrícula en BASIC II"),
            ("SFAREGS", "asignación de cupo", "código RE en sección")],
           ("En BASIC II", "prerrequisito superado"), "catalogo"),
    "05": (("Curso especial", "egresado USS"),
           [("SSASECT", "sección especial", "NRC para egresados"),
            ("SFAREGS", "inscripción backoffice", "tarifa diferenciada"),
            ("Plataforma", "instrucción intensiva", "evaluación externa"),
            ("SHRROLL", "pase a historia", "reconocimiento en CAPP")],
           ("Requisito acreditado", "apto para titulación"), "egreso"),
    "08": (("Retiro de curso", "dentro de plazo lectivo"),
           [("SFAREGS", "consulta matrícula", "Periodo 202656 · ID S00581091"),
            ("SFAREGS", "código de retiro DD", "Drop/Delete en NRC 1021"),
            ("SFAREGS", "recálculo financiero", "estimación de cuota procesada"),
            ("SSASECT", "liberación de vacante", "Actual 2 → 1 · Remaining 0 → 1")],
           ("Cupo liberado (+1)", "retiro procesado"), "matricula"),
    "09": (("Suspendido", "estatus inactivo IS"),
           [("SGASTDN", "verificación estatus", "expediente con Status IS"),
            ("SFAREGS", "intento bloqueado", "motor impide inscripción"),
            ("SGASTDN", "reactivación alumno", "actualización a Status AS"),
            ("SFAREGS", "matrícula exitosa", "código RE · asignación vacante")],
           ("Puede matricularse", "alumno activo AS"), "estudiante"),
    "10": (("Desaprueba curso", "nota 08 en historia"),
           [("SMARQCM", "solicitud CAPP", "auditoría malla CMEMC38"),
            ("SMIPOUT", "regla nota mínima", "exige Nota ≥ 11 en área"),
            ("SMICRLT", "segregación cursos", "ESEC 00650 a «Cursos no usados»"),
            ("SMARQCM", "dictamen NO CUMPLE", "retorno obligatorio a cursar")],
           ("Curso no usado", "repite la asignatura"), "capp"),
    "11": (("Apertura de periodo", "nuevo ciclo lectivo"),
           [("STVTERM", "crear periodo base", "año 202656 · fechas oficiales"),
            ("STVPTRM", "partes de periodo", "subperiodos (ej. X01, I01, P01)"),
            ("SOATERM", "control de periodo", "secuencia NRC (10001) y reglas"),
            ("SIATERM", "duración académica", "factor minutos por hora")],
           ("Periodo habilitado", "listo para programar NRCs"), "periodo"),
    "11-B": (("Diseño curricular", "carrera, programa y malla"),
             [("STVMAJR", "código de carrera", "carrera / major según centro"),
              ("SMAPRLE", "código de programa", "nivel, escuela EM y grado"),
              ("SOACURR", "regla de currículo", "vincular programa + campus + major"),
              ("SMAPROG", "malla del programa", "anexar áreas SMAAREA y créditos")],
             ("Malla aprobada", "lista para admisión y CAPP"), "mallas"),
    "12": (("Fin de periodo", "calificaciones listas"),
           [("SFASLST", "ingreso de notas", "S00581109 (16), S00581108 (08), INH"),
            ("SHAGRDE", "alineación modo V", "diagnóstico y resolución U20"),
            ("GJAPCTL", "reejecución SHRROLL", "Job 8114 exitoso (100 %)"),
            ("SHATERM", "historial y acta", "Rolled = Y · acta cerrada")],
           ("Actas cerradas", "notas en historia"), "cierre"),
    "13": (("Notas del nivel", "notas finales del NRC"),
           [("SHAGRDE", "escala vigesimal", "modo V · nota mínima 11"),
            ("SFASLST", "ingreso en lista", "calificaciones docentes"),
            ("GJAPCTL", "pase a historia", "corrida SHRROLL"),
            ("SHATERM", "asentamiento notas", "historial académico")],
           ("Aprueba o no", "según la nota mínima"), "notas"),
    "15": (("NRC saturado", "capacidad 1/1 vacantes"),
           [("SSASECT", "capacidad inicial", "aforo: 1 vacante máxima"),
            ("SFAREGS", "saturación y bloqueo", "código RE · Closed Section"),
            ("SSASECT", "ampliación aforo", "Maximum 1 → 4 vacantes"),
            ("SFAREGS", "reintento inscripción", "código RE · Actual 2, Remaining 2")],
           ("Aforo ampliado", "vacantes disponibles"), "nrc"),
    "16": (("Traslado de grupo", "reubicación de sección"),
           [("SFAREGS", "matrícula origen", "NRC 1026 (Sec. D) activo"),
            ("SSASECT", "ampliar reserva", "Lugares reservados: CMEMC38 1 → 2"),
            ("SFAREGS", "traslado simultáneo", "NRC 1026: DD · NRC 1021: RE"),
            ("SFASLST", "auditoría lista clase", "alta en lista de nueva sección")],
           ("Traslado exitoso", "vacante origen liberada"), "matricula"),
    "18-A": (("Asignación docente", "horas y secciones lectivas"),
             [("SIAASGN", "consulta docente", "Periodo 202656 · ID 100582059"),
              ("SIAASGN", "auditoría secciones", "4 NRCs: 1021, 1022, 1024, 1025"),
              ("SIAASGN", "cómputo de horas", "9.6 h/sem · 120 h totales"),
              ("SIAASGN", "asignación de FTE", "FTE 0.02 · reemplaza Excel")],
             ("Carga auditada", "reemplaza planillas Excel"), "carga"),
    "18-B": (("Tiene deuda", "cuota vencida o mora"),
             [("SOAHOLD", "registro retención", "código TT por mora"),
              ("SFAREGS", "bloqueo fatal", "error por retención activa"),
              ("TSAAREV", "regularización caja", "pago en caja institucional"),
              ("SFAREGS", "matrícula exitosa", "código RE · cupo asignado")],
             ("Bloqueo fatal garantizado", "hasta regularizar"), "retencion"),
    "02": (("Cupo lleno", "NRC saturado (2/2 vacantes)"),
           [("SFAROVR", "reglas de sobrepaso", "regla CAPACIDAD en periodo"),
            ("SFASRPO", "autorizar sobrepaso", "permiso alumno S00581110"),
            ("SFAREGS", "matrícula con permiso", "código RE sobrecupo"),
            ("SSASECT", "cupo excedido", "Actual 3 / Max 2 vacantes")],
           ("Inscrito con sobrepaso", "cupo superado con permiso"), "matricula"),
    "06": (("Doble programa", "Pregrado + Centros en paralelo"),
           [("SGASTDN", "currícula primaria", "orden 1 (Pregrado activo)"),
            ("SGASTDN", "currícula secundaria", "orden 2 (CMEMC38 Centros)"),
            ("SFAREGS", "elegibilidad de planes", "autorización estatus EL"),
            ("SFAREGS", "inscripción cruzada", "NRC carrera + NRC centros")],
           ("Doble programa activo", "trazabilidad independiente"), "estudiante"),
    "07": (("Triple programa", "Pregrado + Idiomas + Computación"),
           [("SGASTDN", "alta curricular triple", "3 expedientes simultáneos"),
            ("SGASTDN", "niveles académicos", "Nivel 1 + Nivel I + Nivel C"),
            ("SFAREGS", "habilitar transacciones", "código EL en 3 programas"),
            ("SFAREGS", "matrícula multiescuela", "NRCs por centro y pregrado")],
           ("3 programas vigentes", "sin conflicto curricular"), "estudiante"),
    "17": (("Conflicto horario", "mismo bloque y docente"),
           [("SSASECT", "horario sección A", "NRC 1021 · L-M 08:00–12:00"),
            ("SSASECT", "asignar a sección B", "NRC 1026 mismo bloque docente"),
            ("SSASECT", "alerta de conflicto", "alerta cruce horario instructor"),
            ("SSASECT", "crear sobrepaso", "Indicador de sobrepaso docente")],
           ("Conflicto resuelto", "docente con sobrepaso"), "nrc"),
    "14": (("Fin del curso", "el NRC terminó sus clases"),
           [("SFASLST", "revisar notas finales", "todos los alumnos con nota"),
            ("GJAPCTL", "pase a historia", "proceso SHRROLL"),
            ("SFASLST", "verificar «Pasada»", "nota ya en la historia")],
           ("NRC cerrado", "notas en la historia"), "cierre"),
    "18-C": (("Solicitud o queja", "el alumno pide un servicio"),
             [("Autoservicio", "crear la solicitud", "servicio CER (no hay de queja)"),
              ("SVASVPR", "buscar la solicitud", "número, servicio y estatus"),
              ("SVASVPR", "atender y responder", "estatus y comentarios")],
             ("Solicitud atendida", "queja: falta su servicio (U14)"), "solicitudes"),
    "19": (("Asistencia y notas", "preparar el libro del NRC"),
           [("SHAEGBC", "calendario del periodo", "202656 · fechas autorizadas"),
            ("SHAGCOM", "asignar ATTRGRD", "NRC 10026 · ESEC 00697 · X06")],
           ("Criterios confirmados", "nota ≥11 · asistencia ≥70%"), "asistencia_componente"),
}

EXTRA_CASOS = {
    "01": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Excel TEST · Capacidad 5.4)",
        "items": [
            "Paso 01 (SFAREGS): Acceso a Pantalla — Formulario con Periodo lectivo (ej. 202656) e ID del estudiante admitido.",
            "Paso 02 (SFAREGS): Autorización Curricular — Bloque Curricula: clic en plan de estudios y cambio a estatus elegible EL (F10).",
            "Paso 03 (SFAREGS): Captura de Asignatura — Bloque Course Registration: ingreso manual del NRC asignado a la sección.",
            "Paso 04 (SFAREGS): Asignación de Código RE — Registro con código RE (Register) para formalizar inscripción y calcular tasa.",
            "Paso 05 (SSASECT / SSASECQ): Auditoría de Cupos — Descuento automático de vacante (Remaining -1) y actualización en tiempo real.",
            "Paso 06 (TSAAREV): Evaluación Financiera — Comprobación de aplicación de tarifas institucionales en cuenta corriente.",
            "Paso 07 (SFASLST): Lista Oficial de Clase — Aparición formal en lista del docente con estatus registrado.",
        ],
    },
    "03": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Excel TEST · Capacidad 3.3)",
        "items": [
            "Paso 01 (SHATRNS): Registro de Asignatura Externa — ID: S00581111, Institución procedencia, Asignatura IST150 (Nota: 16, Modo: P).",
            "Paso 02 (SHATRNS): Articulación y Equivalencia — Bloque Transfer Course Articulation, mapeo curricular con plan local.",
            "Paso 03 (SHATFAC): Acreditación en Facultad — Revisión de articulación y registro de aprobación académica oficial.",
            "Paso 04 (GJAPCTL): Ejecución de Pase a Historia — Proceso batch SHRROLL (Job 8113), procesando asignaturas a historia.",
            "Paso 05 (SHATERM / SHATRNS): Validación de Estatus — Confirmación de estatus «Rolled to Academic History» con créditos oficiales.",
            "Paso 06 (SHADEGR): Creación de Registro de Grado — Expediente curricular institucional generado satisfactoriamente (Deg Created).",
            "Paso 07 (SHASMRY): Auditoría Final de Historial — Transcript consolidado validado al 100 % sin requerir cursado regular.",
        ],
    },
    "04": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Excel TEST · Capacidad 1.2 y 5.4)",
        "items": [
            "Paso 01 (SOAINST): Verificación de Evaluación — Consulta de código de examen de suficiencia institucional.",
            "Paso 02 (SOATEST): Registro de Calificación — Ingreso de ID del alumno, código de prueba (U01) y puntaje aprobatorio.",
            "Paso 03 (SCAPREQ): Evaluación de Prerrequisitos — El motor valida el examen como prerrequisito equivalente de BASIC I.",
            "Paso 04 (SFAREGS): Matrícula en Nivel Siguiente — Inscripción directa en BASIC II sin bloqueo fatal.",
            "Paso 05 (SFAREGS): Asentamiento de Matrícula — Código RE guardado y vacante asignada en el NRC de destino.",
        ],
    },
    "05": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Excel TEST · Capacidad 5.3)",
        "items": [
            "Paso 01 (SSASECT): Creación de Sección Especial — Configuración de NRC con indicador de egresados y cupos específicos.",
            "Paso 02 (SFAREGS): Inscripción Administrativa — Registro del alumno egresado con arancel y tarifa diferenciada.",
            "Paso 03 (Plataforma): Activación y Evaluación — Asignación de credenciales en plataforma externa y cómputo de notas.",
            "Paso 04 (SFASLST): Registro de Nota Final — Vaciado de calificación aprobatoria en lista oficial de clase de Banner.",
            "Paso 05 (GJAPCTL / SHRROLL): Pase a Historia — Rolado formal a historial académico para reconocimiento en CAPP de egreso.",
        ],
    },
    "08": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Excel TEST · Capacidad 5.4 y 11.1)",
        "items": [
            "Paso 01 (SFAREGS): Consulta de Inscripción — Acceso con Periodo 202656 e ID del estudiante (S00581091).",
            "Paso 02 (SFAREGS): Asignación de Código DD — Ingreso del código Drop/Delete en el registro del curso NRC 1021.",
            "Paso 03 (SFAREGS): Procesamiento Financiero — Transacción ejecutada con «Estimación de cuota procesada» y recálculo de cobro.",
            "Paso 04 (SSASECT): Liberación Automática de Cupo — Aforo actualizado en tiempo real: Actual 2 → 1 y Remaining 0 → 1.",
            "Paso 05 (SFASLST): Auditoría de Lista de Clase — Verificación de exclusión del estudiante de la lista oficial del docente.",
        ],
    },
    "09": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Excel TEST · Capacidad 4.1 y 5.4)",
        "items": [
            "Paso 01 (SGASTDN): Verificación de Estatus Suspendido — ID: S00581109, pestaña Curricula, Status: IS (Inactivo).",
            "Paso 02 (SFAREGS): Intento de Inscripción con IS — Intento de alta de NRC bloqueado por condición inactiva.",
            "Paso 03 (SFAREGS): Validación de Restricción — Notificación de control indicando que el estudiante no es elegible.",
            "Paso 04 (SGASTDN): Reactivación Académica — Modificación de registro a Status: AS (Activo) y guardado en base de datos.",
            "Paso 05 (SFAREGS): Reintento de Inscripción — Habilitación de captura de asignaturas en el periodo lectivo.",
            "Paso 06 (SFAREGS): Confirmación de Asignaturas — Guardado con estatus RE, asignando vacante y actualizando carga.",
            "Paso 07 (SGASTDN / SHACRSE): Auditoría Final de Expediente — Trazabilidad integral de estatus y récord académico.",
        ],
    },
    "10": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Excel TEST · Capacidad 7.1 y 8)",
        "items": [
            "Paso 01 (SMARQCM): Solicitud de Auditoría Curricular — ID: S00581108, Programa: CMEMC38, inicio de auditoría general CAPP.",
            "Paso 02 (SMIPOUT): Evaluación de Regla de Calificación Mínima — Validación de nota mínima aprobatoria (Nota ≥ 11).",
            "Paso 03 (SMICRLT): Segregación a Cursos No Usados — Desplazamiento de ESEC 00650 al bloque de cursos no usados / reprobados.",
            "Paso 04 (SMIPOUT): Cómputo de Créditos y Avance — Requerimiento 0/4 cursos, registrando 0,000 créditos acumulados.",
            "Paso 05 (SMARQCM): Determinación de Cumplimiento — Dictamen curricular del área y requisitos en estado «NO CUMPLE».",
            "Paso 06 (SMIPOUT / CAPP): Activación de Retorno Obligatorio — Bloqueo de avance a siguientes ciclos y exigencia de recursado.",
            "Paso 07 (SMARQCM): Auditoría Final y Dictamen CAPP — Reporte consolidado confirmando rechazo de créditos y plan incompleto.",
        ],
    },
    "11": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Capacidad 1.1 · Instructivos 1.1.1 y 1.1.2)",
        "items": [
            "Paso 01 (STVACYR / STVTRMT): Tablas Previas — Validación del año académico institucional y tipo de periodo (Semestral, Verano).",
            "Paso 02 (STVTERM): Periodo Base — Código alfanumérico (ej. 202656), descripción, fechas de inicio/fin y fechas de alojamiento obligatorias.",
            "Paso 03 (STVPTRM): Catálogo de Partes — Creación de subperiodos con descripción institucional (ej. X01-X07, I01-I12, P01-P06).",
            "Paso 04 (SOATERM): Control de Periodo — Secuencia inicial de NRCs (ej. 10001), activar inscripción (Permitir) y casillas de prerrequisitos En Progreso.",
            "Paso 05 (SOATERM): Partes de Periodo — Configuración de cada subperiodo con fechas exactas, semanas de duración y fecha de censo 1 obligatoria.",
            "Paso 06 (SIATERM): Factor de Duración — Asignación de minutos por hora académica para el cálculo lectivo del periodo.",
        ],
    },
    "11-B": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Capacidad 1.1 y 1.2 · Instructivos 1.1.3 y 1.2.1)",
        "items": [
            "Paso 01 (STVMAJR): Código de Carrera / Major — Creación del Major institucional y activación de la casilla Carrera.",
            "Paso 02 (SMAPRLE): Definición de Programa — Código del programa (12 caracteres), nivel académico, grado 000000 y escuela EM.",
            "Paso 03 (SOACURR): Regla Curricular — Vinculación del programa con Campus S, periodo de inicio, Major de STVMAJR y departamento institucional.",
            "Paso 04 (SMAALIB): Biblioteca de Áreas — Definición del código de área curricular con casilla Cumplimiento activada para auditoría CAPP.",
            "Paso 05 (SMAAREA): Requerimientos de Área — Reglas de asignaturas del catálogo (SCACRSE), condiciones y nota mínima aprobatoria (Modo V, 11).",
            "Paso 06 (SMAPROG): Malla Oficial del Programa — Requerimientos generales, créditos totales requeridos y anexo formal de áreas curriculares.",
        ],
    },
    "12": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Excel TEST · Capacidad 7.1 y 8)",
        "items": [
            "Paso 01 (SFASLST): Ingreso de Calificaciones — Periodo 202656, NRC 1026: S00581109 (16 V), S00581108 (08 V), S00581111 (INH V).",
            "Paso 02 (GJAPCTL): Ejecución Inicial Pase a Historia — Proceso SHRROLL, corrida preliminar para evaluar población.",
            "Paso 03 (SHAGRDE / Catálogo): Diagnóstico Incidencia U20 — Discrepancia entre Modo V en SCACRSE vs Modo P en SHAGRDE Nivel C.",
            "Paso 04 (SHAGRDE): Alineación de Modo de Calificación — Homologación de Modo V a nivel curso y estudiante para SHRROLL.",
            "Paso 05 (GJAPCTL): Reejecución de Proceso Batch — SHRROLL Job 8114 exitoso con 100 % de estudiantes rolados a historia.",
            "Paso 06 (SHATERM / SHASMRY): Validación en Historial — Estatus «Rolled to Academic History» confirmado en los expedientes.",
            "Paso 07 (SFASLST / SHAGRDE): Cierre Formal y Bloqueo de Acta — Indicador Grade Roll Status = Y impidiendo ediciones posteriores.",
        ],
    },
    "13": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Excel TEST · Capacidad 7.1)",
        "items": [
            "Paso 01 (SHAGRDE): Verificación de Escala — Modo V con escala vigesimal (00-20), nota aprobatoria mínima 11.",
            "Paso 02 (SFASLST): Captura de Calificaciones — Registro de notas finales por lista de clase (o Autoservicio docente).",
            "Paso 03 (SFASLST): Inasistencias e Inhabilitados — Asignación de código INH con nota 00 a participantes inhabilitados.",
            "Paso 04 (SFASLST): Auditoría de Pre-Cierre — Verificación de columna Rolled en estado N antes del proceso batch.",
            "Paso 05 (GJAPCTL): Despacho SHRROLL — Pase oficial de calificaciones para asentar historial del periodo.",
        ],
    },
    "15": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Excel TEST · Capacidad 1.1 y 5.3)",
        "items": [
            "Paso 01 (SSASECT): Configuración Inicial de Capacidad — NRC 1026, Maximum: 1, Actual: 0 (1 cupo disponible).",
            "Paso 02 (SFAREGS): Saturación de Capacidad (Alumno 1) — ID: S00581091, código RE, ocupando la única vacante.",
            "Paso 03 (SFAREGS): Intento de Sobrecupo (Alumno 2) — ID: S00582045, código RE, motor detecta aforo lleno.",
            "Paso 04 (SFAREGS): Emisión de Error Fatal — Notificación explícita de «Closed Section» bloqueando inscripción.",
            "Paso 05 (SSASECT): Ampliación de Aforo — Bloque Enrollment: Maximum 1 → 4 vacantes, recalculando Remaining a 3.",
            "Paso 06 (SFAREGS): Reintento de Inscripción (Alumno 2) — ID: S00582045, código RE, inscripción regular permitida.",
            "Paso 07 (SSASECT): Auditoría Final de Balance — NRC 1026: Actual 2, Remaining 2; revisión de cupo y lugares reservados.",
        ],
    },
    "16": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Excel TEST · Capacidad 5.3 y 5.4)",
        "items": [
            "Paso 01 (SFAREGS): Verificación de Matrícula Origen — ID: S00581109, Periodo: 202656, NRC 1026 (Sec. D) activo.",
            "Paso 02 (SSASECT): Verificación de Cupo Destino — NRC 1021 (Sec. B), bloque Enrollment Information.",
            "Paso 03 (SFAREGS): Intento de Traslado y Alerta — NRC 1026 con DD y NRC 1021 con RE, alerta de reserva de cupo.",
            "Paso 04 (SSASECT): Ajuste de Reserva de Cupo — En Lugares reservados, ampliar CMEMC38 de 1 a 2 para permitir reubicación.",
            "Paso 05 (SFAREGS): Ejecución Exitosa de Traslado — Transacción simultánea: retiro de origen (DD) e inscripción en destino (RE).",
            "Paso 06 (SFASLST): Auditoría de Lista de Clase — Aparición oficial en el roster de la sección B con aforo actualizado.",
            "Paso 07 (SFAREGS / TSAAREV): Validación de Récord y Finanzas — Sin duplicidad de cargos ni afectación de créditos acumulados.",
        ],
    },
    "18-A": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Excel TEST · Capacidad 5.2)",
        "items": [
            "Paso 01 (SIAASGN): Acceso a Carga Docente — Formulario con Periodo 202656 y docente 100582059 (Dagner Chuman).",
            "Paso 02 (SIAASGN): Auditoría de 4 NRCs — Verificación de secciones 1021, 1022, 1024 y 1025 en Computación y Emprendimiento.",
            "Paso 03 (SIAASGN): Horas Semanales — Cálculo automático de 9.6 horas de contacto semanales para el NRC 1021.",
            "Paso 04 (SIAASGN): Horas Totales — Cómputo de 120 horas lectivas totales programadas en el periodo.",
            "Paso 05 (SIAASGN): Asignación de FTE — Determinación de factor FTE 0.02 por dedicación académica.",
            "Paso 06 (SIAASGN): Roles de Instrucción — Registro de rol primario (100 %) y roles secundarios en co-docencia.",
            "Paso 07 (SIAASGN): Consolidación Institucional — Sustitución integral y automática de las planillas Excel.",
        ],
    },
    "18-B": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Excel TEST · Capacidad 4.1 y 5.4)",
        "items": [
            "Paso 01 (SOAHOLD): Asignación de Retención — Registro de retención TT (Cobranzas) por cuota vencida o mora.",
            "Paso 02 (STVHLDD): Verificación de Reglas — Comprobación de flags de afectación de matrícula y servicios.",
            "Paso 03 (SFAREGS): Intento de Matrícula — Captura de asignaturas en el formulario de inscripción.",
            "Paso 04 (SFAREGS): Bloqueo Fatal Transaccional — Notificación de error bloqueando la asignación del código RE.",
            "Paso 05 (TSAAREV / TVACAJA): Regularización de Deuda — Pago de saldos pendientes en caja institucional.",
            "Paso 06 (SOAHOLD): Levantamiento de Retención — Registro de fecha de liberación desactivando la retención.",
            "Paso 07 (SFAREGS): Inscripción Exitosa — Confirmación de matrícula con estatus RE y asignación de vacante.",
        ],
    },
    "02": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Excel TEST · Capacidad 5.4)",
        "items": [
            "Paso 01 (SFAROVR): Verificación de Regla — Habilitación de sobrepaso CAPACIDAD en periodo 202656.",
            "Paso 02 (SSASECT): Confirmación de Aforo Lleno — NRC 1021 con Maximum 2 y Actual 2 (Remaining 0).",
            "Paso 03 (SFASRPO): Otorgamiento de Permiso — Ingreso del ID S00581110 y selección de sobrepaso CAPACIDAD.",
            "Paso 04 (SFAREGS): Matrícula Especial — Captura de NRC 1021 con código RE sin rechazo de Closed Section.",
            "Paso 05 (SSASECT / SFASLST): Auditoría Final — Actual 3/2 vacantes y alumno registrado en lista de clase.",
        ],
    },
    "06": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Excel TEST · Capacidad 4.1 y 5.4)",
        "items": [
            "Paso 01 (SGASTDN): Expediente Pregrado — Verificación de currícula primaria (Orden 1, nivel Pregrado).",
            "Paso 02 (SGASTDN): Anexo de Programa Centros — Inserción de currícula secundaria (Orden 2, nivel C, programa CMEMC38).",
            "Paso 03 (SFAREGS): Selección de Plan — Alternancia de planes en bloque Curricula marcando ambos con estatus EL.",
            "Paso 04 (SFAREGS): Inscripción Multiescuela — Registro independiente de asignatura de carrera y módulo de centros.",
            "Paso 05 (SHATERM / CAPP): Trazabilidad de Avance — Los créditos y notas tributan al historial del programa respectivo.",
        ],
    },
    "07": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Excel TEST · Capacidad 4.1 y 5.4)",
        "items": [
            "Paso 01 (SGASTDN): Alta Curricular Triple — Expediente del alumno S00581091 con tres planes activos: Pregrado, Idiomas y Computación.",
            "Paso 02 (SGASTDN): Validación de Niveles — Nivel 1 (Pregrado), Nivel I (Idiomas) y Nivel C (Computación) con grado 000000.",
            "Paso 03 (SFAREGS): Habilitación Transaccional — Autorización curricular EL en los tres programas académicos.",
            "Paso 04 (SFAREGS): Inscripción de NRCs — Alta secuencial de NRCs de cada centro sin conflicto de incompatibilidad.",
            "Paso 05 (SFASLST / CAPP): Auditoría de Listas — Presencia en las actas de cada escuela con auditoría independiente.",
        ],
    },
    "17": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Excel TEST · Capacidad 5.3)",
        "items": [
            "Paso 01 (SSASECT): Horario Sección Origen — Programación del NRC 1021 con bloque Lunes y Miércoles 08:00–12:00, docente 100582059.",
            "Paso 02 (SSASECT): Asignación a Sección Destino — Apertura de NRC 1026 en el mismo horario e ingreso del mismo docente.",
            "Paso 03 (SSASECT): Detección de Conflicto — Banner emite alerta: «ERROR: Conflicto de horario del instructor para 100582059. ¿Crear sobrepaso?».",
            "Paso 04 (SSASECT): Autorización de Sobrepaso — Aceptación con OK, marcando automáticamente el «Indicador de sobrepaso».",
            "Paso 05 (SIAASGN): Auditoría de Carga — Verificación de horas simultáneas asignadas al docente sin duplicidad de FTE.",
        ],
    },
    "14": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Capacidad 7.1 · Instructivos 7.1.6 y 7.1.9)",
        "items": [
            "Paso 01 (SFASLST): Notas completas — Periodo y NRC; todos los alumnos del NRC deben tener su calificación final antes del cierre (7.1.6, diap. 15–16).",
            "Paso 02 (GJAPCTL): Pase a historia — Proceso SHRROLL con sus parámetros y la opción Enviar (7.1.9, diap. 22–27). En Computación se validó junto con el Script 12.",
            "Paso 03 (SFASLST): Verificación final — La casilla «Pasada» marcada indica que la nota ya está en la historia académica (7.1.6, diap. 16). El script también pide pasar el estatus de la sección a cerrado en SSASECT; eso no se ha probado en TEST.",
        ],
    },
    "18-C": {
        "dot": "violet",
        "title": "Guía Operativa Paso a Paso (Capacidad 4.3 · Instructivo 4.3.2)",
        "items": [
            "Paso 01 (Autoservicio): Solicitud del alumno — El alumno elige la categoría y el servicio y pulsa Continuar (4.3.2, diap. 10). En TEST no hay servicio de queja (U14); el mecanismo se probó con CER (Certificado).",
            "Paso 02 (SVASVPR): Búsqueda — Ingrese al menos un criterio (ID, servicio, estatus) para ver las solicitudes; el número es el mismo que ve el alumno (4.3.2, diap. 17–18).",
            "Paso 03 (SVASVPR): Atención — Actualice el estatus según avance el servicio y registre el comentario interno y el comentario de respuesta (4.3.2, diap. 19–20). SVASVPR no deja crear la solicitud («Función inválida»): la crea el alumno.",
        ],
    },
    "19": {
        "dot": "violet",
        "title": "Script 19 · Configurar calificaciones y asistencia (TEST)",
        "items": [
            "SHAEGBC (Calendario): para 202656, definir y guardar las fechas de apertura y corte autorizadas. No inventar fechas ni dar por requerido el corte final sin confirmación.",
            "SHAGCOM (Plan de evaluación): ejemplo TEST, periodo 202656, NRC 10026, materia ESEC, curso 00697, parte X06.",
            "Agregar ATTRGRD con peso 0.00, marcar Debe Pasar y seleccionar la escala propia de asistencia que corresponda al mínimo institucional de 70 %.",
            "En Computación, mantener el modo V con nota mínima aprobatoria 11. Son dos criterios: nota ≥11 y asistencia ≥70 %.",
            "Computación, NRC 10026: Script 19 validado en TEST por confirmación del usuario (C95).",
        ],
    },
}


# Datos de las pruebas de Computación en TEST (alumnos, NRC, programa, jobs, docente). En otro centro
# no se muestran como propios: la etiqueta del paso se quita y la guía los presenta como referencia.
RE_DATO_COMPUTACION = re.compile(
    r"S005\d{5}|\b10[0-2]\d\b|CMEMC\d+|\bJob \d+|IST150|\bESEC\b|100582059|FTE 0\.|h/sem|L-M \d")
# La escala de Computación (vigesimal, modo V, aprueba con 11) solo vale donde la escala es la misma.
RE_ESCALA_V = re.compile(r"vigesimal|[Mm]odo V\b|≥ ?11\b|m[ií]nima 11\b|\(\d\d V\)")
# Casos que en ese centro son otra cosa: no llevan la guía de Computación.
CASO_PROPIO = {("idiomas", "02"), ("idiomas", "05"), ("idiomas", "10")}


def escala_de(c):
    """(modo, nota aprobatoria) del centro, de datos.json › escala_calificacion."""
    e = c.d.get("escala_calificacion") or {}
    return e.get("modo") or "por confirmar", e.get("aprobatoria") or "por confirmar"


def es_de_computacion(c, texto):
    """True si el texto trae datos de las pruebas de Computación que no son de este centro."""
    if c.id == "computacion" or not texto:
        return False
    return bool(RE_DATO_COMPUTACION.search(texto) or (escala_de(c) != ("V", 11) and RE_ESCALA_V.search(texto)))


def _etiqueta_del_centro(c, etiqueta):
    """La etiqueta de un paso; None si en este centro sería un dato de las pruebas de Computación."""
    return None if es_de_computacion(c, etiqueta) else etiqueta


def caso(c, id_script):
    """Situación, pasos y resultado de un script, con los ajustes de cada centro."""
    sit, pasos, res, cita = _caso(c, id_script)
    pasos = [(p[0], p[1]) + ((et,) if (et := _etiqueta_del_centro(c, p[2] if len(p) > 2 else None)) else ())
             for p in pasos]
    return sit, pasos, res, cita


def referencia_computacion(c, id_script, extra):
    """La guía de Excel del script para este centro: en otro centro se presenta como referencia de Computación."""
    if not extra or (c.id, id_script) in CASO_PROPIO:
        return None
    if id_script == "11-B":  # guía de los instructivos: solo cambia la escala del ejemplo
        modo, aprobatoria = escala_de(c)
        return {**extra, "items": [i.replace("(Modo V, 11)", f"(Modo {modo}, {aprobatoria})") for i in extra["items"]]}
    if not any(es_de_computacion(c, item) for item in extra.get("items", [])):
        return extra
    estado = Centro("computacion").script(id_script)["estado"]
    titulo = ("Referencia: así se probó en Computación (TEST)" if estado == "validado"
              else "Referencia: guía preparada para Computación")
    return {**extra, "title": titulo}


def _caso(c, id_script):
    if c.id == "idiomas" and id_script == "02":
        return (("Sin prerrequisito", "no aprobó el nivel anterior"),
                [("SFAROVR", "regla de sobrepaso", "sobrepaso de prerrequisito"),
                 ("SFASRPO", "permiso al alumno", "quién lo autoriza: U10"),
                 ("SFAREGS", "matrícula con permiso", "código RE")],
                ("Inscrito con sobrepaso", "prerrequisito sobrepasado"), "matricula")
    if c.id == "idiomas" and id_script == "05":
        return (("Egresado", "no lleva el curso regular"),
                [("Plataforma", "activar y rendir en plataforma", "instrucción intensiva"),
                 ("SSASECT", "crear un solo NRC especial", "sección para egresados"),
                 ("Nota manual", "pasar nota a Banner", "calificación docente"),
                 ("GJAPCTL", "pase a historia SHRROLL", "reconocimiento CAPP")],
                ("BASIC I, II…", "la misma nota en todos"), "egreso")
    if c.id == "idiomas" and id_script == "10":
        return (("Desaprueba BASIC I", "nota bajo el mínimo (≤10)"),
                [("SFASLST", "nota final docente", "nota reprobatoria"),
                 ("GJAPCTL", "pase a historia", "proceso SHRROLL"),
                 ("SFAREGS", "intento en BASIC II", "error Fatal prerrequisito"),
                 ("SOATEST", "alternativa suficiencia", "examen de suficiencia")],
                ("Repite BASIC I", "o rinde suficiencia"), "capp")
    if c.id == "emprendimiento" and id_script == "16":
        return (("Cambio de NRC", "P02 y P03 se superponen"),
                [("SFAREGS", "verificar origen", "grupo activo en curso"),
                 ("SSASECT", "verificar destino", "aforo en sección alterna"),
                 ("SFAREGS", "traslado simultáneo", "DD en origen · RE en destino"),
                 ("SFASLST", "auditoría lista", "alta en nueva sección")],
                ("En el nuevo NRC", "lista actualizada"), "matricula")
    if id_script == "11":
        return (("Apertura periodo", f"ciclo {c.periodo_ejemplo}"),
                [("STVTERM", "crear periodo base", f"{c.periodo_ejemplo} · fechas oficiales"),
                 ("STVPTRM", "partes de periodo", f"subperiodos {c.partes}"),
                 ("SOATERM", "control de periodo", "secuencia NRC y reglas"),
                 ("SIATERM", "duración académica", "hora académica")],
                ("Periodo activo", "listo para programar NRCs"), "periodo")
    if id_script == "11-B":
        area = c.d.get("capp", {}).get("area") or c.d.get("capp", {}).get("codigo") or "malla base"
        return (("Diseño curricular", f"programa {c.programa}"),
                [("STVMAJR", "código de carrera", f"Major {c.d['mayor']['codigo']}"),
                 ("SMAPRLE", "código de programa", f"Programa {c.programa} · nivel {c.nivel}"),
                 ("SOACURR", "regla de currículo", f"Campus S · {c.d['departamento']['codigo']}"),
                 ("SMAPROG", "malla del programa", f"Área {area} · regla CAPP")],
                ("Malla aprobada", "lista para admisión y CAPP"), "mallas")
    sit, pasos, res, cita = CASOS[id_script]
    modo, aprobatoria = escala_de(c)
    if id_script == "13":
        tipo = (c.d.get("escala_calificacion") or {}).get("tipo", "del centro").lower()
        pasos = [("SHAGRDE", f"escala {tipo}", f"modo {modo} · nota mínima {aprobatoria}")] + pasos[1:]
        res = (res[0], f"aprueba con {aprobatoria}")
    if id_script == "19":
        res = (res[0], f"nota ≥{aprobatoria} · asistencia ≥{c.comun['asistencia_minima_porcentaje']['valor']}%")
    return sit, pasos, res, cita


def casuistica(c, numero, id_script):
    (sit, sit_sub), pasos, (res, res_sub), cita = caso(c, id_script)
    s = c.script(id_script)
    cap = c.capacidad_script(id_script)
    cap_det = c.capacidad_detalle_script(id_script)
    nodos = [paso("c0", "caso", 0, sit, sit_sub, tipo="security", ancho=170)]
    for j, item in enumerate(pasos, start=1):
        codigo, accion = item[0], item[1]
        tag = item[2] if len(item) > 2 else None
        tipo = {"SHRROLL": "messagebus", "SSASECQ": "database", "SMARQCM": "database", "Plataforma": "external"}.get(codigo, "backend")
        nodos.append(paso(f"c{j}", "caso", j, codigo, accion, dato=tag, tipo=tipo, ancho=170))
    nodos.append(paso("cr", "caso", len(pasos) + 1, res, res_sub, ESTADO_TEXTO[s["estado"]], "database", "success", ancho=170))
    estado = ESTADO_TEXTO[s["estado"]]
    probado = [s["evidencia"]] if s["estado"] == "validado" else [f"{estado[:1].upper()}{estado[1:]}: {s['evidencia']}"]
    lane_label = f"{cap} · Situación → pasos → resultado" if cap else "Situación → pasos → resultado"
    extra = referencia_computacion(c, id_script, EXTRA_CASOS.get(id_script))
    if extra:
        extra = extra if isinstance(extra, list) else [extra]
    return flujo(
        c, numero, slug_script(id_script),
        [{"id": "caso", "label": lane_label}],
        nodos,
        tarjetas(c, probado, [CITAS[cita]], extra=extra),
        title_override=f"{c.nombre} · {cap} · Script {id_script} · {c.nombre_script(id_script)}" if cap else None,
        subtitle_override=c.subtitulo(cap_det) if cap_det else None,
    )


def guia_casuistica_de(id_centro, sid):
    """Guía operativa de un script para un centro, construida desde CASOS y EXTRA_CASOS."""
    from guias_operativas import construir_guia
    c = Centro(id_centro) if id_centro in ("idiomas", "computacion", "emprendimiento") else Centro("computacion")
    id_script = sid
    if id_script not in CASOS:
        for k in CASOS:
            if k.upper() == str(sid).upper():
                id_script = k
                break
    if id_script not in CASOS:
        return {}
    (sit, sit_sub), pasos, (res, res_sub), _ = caso(c, id_script)
    extra = referencia_computacion(c, id_script, EXTRA_CASOS.get(id_script)) or {}
    items = extra.get("items", []) if isinstance(extra, dict) else (extra if isinstance(extra, list) else [extra])
    titulo = TITULOS.get(slug_script(id_script)) or f"Script {id_script}"  # ya dice «Script NN · …»
    if extra and extra is not EXTRA_CASOS.get(id_script):
        titulo += " · referencia: prueba de Computación"
    return construir_guia((sit, sit_sub), pasos, (res, res_sub), items, titulo)


FASES_CASUISTICAS = [("periodo", "Abrir el periodo"), ("matricula", "Matrícula"), ("notas", "Notas y cierre")]


def casuisticas_de(c, inicio=7):
    ids = [i for clave, _ in FASES_CASUISTICAS for i in c.d["casuisticas"].get(clave, [])]
    return [(inicio + k, slug_script(i), lambda c, i=i, n=inicio + k: casuistica(c, n, i)) for k, i in enumerate(ids)]


# --------------------------------------------------------------------------- ligas (solo si el centro las usa)
def ligas(c, numero):
    """SCACRSE → SSASECT (teórico) → SSASECT (club) → SSADETL → SFAREGS: dos NRC del mismo curso, juntos."""
    lg = c.d["ligas"]
    sec = lg["secundaria"]
    curso = "BASIC I" if c.id == "idiomas" else c.curso_ejemplo
    liga_sec = f"liga {sec['identificador']}" if sec["identificador"] else "su liga: por confirmar"
    nodos = [
        paso("g1", "nrc", 0, "SCACRSE", "revisar tipos de horario", f"{curso}: TEO y PRA", icono="calendar"),
        paso("g2", "nrc", 1, "SSASECT", "NRC teórico virtual", f"sección AT · liga {lg['principal']['identificador']} · cobro"),
        paso("g3", "nrc", 2, "SSASECT", "NRCs prácticos", f"liga {sec['identificador']} · prácticas (dispensa)"),
        paso("g4", "nrc", 3, "SSADETL", "unir las ligas", f"conector cruzado {lg['principal']['identificador']} ↔ {sec['identificador']}"),
        paso("g5", "nrc", 4, "SFAREGS", "matricular los dos", "teórico + práctica juntos"),
        paso("g6", "nrc", 5, "Matriculado", "en el teórico y la práctica", ESTADO_TEXTO[lg["estado"]], "database", "success"),
    ]
    escenarios = {"dot": "rose", "title": "Reglas de Ligas confirmadas", "items": [
        "Curso principal: Virtual y Teórico (sección AT, aula SAUVIR, calificable=SÍ, dispensa=NO, liga TA)",
        "Segundo curso: Presencial y Práctico (sección AC1, aula SPOSGR posgrado, calificable=NO, dispensa=SÍ, liga PA)",
        "Resto de cursos prácticos: Virtuales (secciones AC2, AC3, aula SAUVIR, calificable=NO, dispensa=SÍ, liga PA)",
        "Vinculación en SSADETL: Teórico lleva conector PA; Prácticos llevan conector TA (muchos a muchos con restricción)",
        "Si SOATERM tiene «Ligas» en Fatal, el estudiante debe inscribir ambos simultáneamente en SFAREGS o Autoservicio",
    ]}
    probado = ["Todavía no se probó en TEST: ver el bloque 1 de la guía de pruebas del centro"] \
        if lg["estado"] != "validado" else [lg.get("evidencia", "Validado en TEST")]
    return flujo(
        c, numero, "ligas-teorico-y-club",
        [{"id": "nrc", "label": "Programar y matricular con liga"}],
        nodos,
        tarjetas(c, probado, [CITAS["ligas"], CITAS["nrc"], CITAS["matricula"]],
                 [escenarios, tarjeta_terminos("liga", "NRC")]),
        fases=[
            {"id": "f0", "label": "Catálogo", "fromCol": 0, "toCol": 0},
            {"id": "f1", "label": "Programar", "fromCol": 1, "toCol": 3, "variant": "emphasis"},
            {"id": "f2", "label": "Matricular", "fromCol": 4, "toCol": 5},
        ],
    )


# --------------------------------------------------------------------------- demostraciones
CARRILES_DEMO = {"ra": "Registros Académicos", "centro": "El centro", "doc": "Docente (Autoservicio)"}


def demostracion(c, d):
    """Un caso real de TEST para mostrar en una reunión, en el orden curso › NRC › docente › fórmula › alumno (C133).

    Los pasos van en columnas 0 a 5; si hay 7, los dos últimos comparten la columna 5 en carriles distintos."""
    carriles = list(dict.fromkeys(p["carril"] for p in d["pasos"]))
    orden = ["ra", "centro", "doc"]
    carriles.sort(key=orden.index)
    nodos = [paso(p["id"], p["carril"], min(i, 5), p["codigo"], p["accion"], p["dato"], p.get("tipo", "backend"))
             for i, p in enumerate(d["pasos"])]
    nodos[0]["icon"] = "start"
    nodos[-1]["icon"] = "success"
    cards = tarjetas(c, [d["caso"], d["resultado"]], [CITAS["periodo"], CITAS["nrc"], CITAS["docente"], CITAS["carga"],
                                                     CITAS["calendario"], CITAS["notas"], CITAS["asistencia_regla"],
                                                     CITAS["cierre"]],
                     [{"dot": "violet", "title": "Guion para la reunión", "items": [f"{i}. {t}" for i, t in enumerate(d["guion"], 1)]},
                      {"dot": "rose", "title": "Lo que aprendimos en TEST", "items": d["aprendido"]}])
    return flujo(
        c, 0, d["slug"],
        [{"id": k, "label": CARRILES_DEMO[k]} for k in carriles],
        nodos, cards,
        fases=[{"id": "f0", "label": "Preparar el NRC: periodo, sección, docente y fórmula", "fromCol": 0, "toCol": 3},
               {"id": "f1", "label": "Matricular, dictar y cerrar", "fromCol": 4, "toCol": 5, "variant": "emphasis"}],
        title_override=f"{c.nombre} · {d['titulo']}",
        subtitle_override=c.subtitulo(d.get("capacidad")),
    )


def guia_demostracion(c, slug_):
    """Guía de cada paso de la demostración, con sus láminas (temas de diapositivas_pasos.py o listas)."""
    from diapositivas_pasos import TEMAS
    d = DEMOSTRACIONES[slug_]
    guia = {}
    for p in d["pasos"]:
        laminas = []
        for x in p["laminas"]:
            laminas += TEMAS[x] if isinstance(x, str) else [x]
        guia[p["id"]] = {"titulo": d["titulo"], "pantalla": p["codigo"], "fase": f"{p['codigo']}: {p['accion']}",
                         "hito": f"{p['quien']} · {p['dato']}", "instrucciones": p["filas"], "diapositivas": laminas}
    return guia


def demostraciones_de(c):
    """Las demostraciones del centro van primero (00-…), antes de los flujos base."""
    return [(0, d["slug"], lambda c, d=d: demostracion(c, d)) for d in c.d.get("demostraciones", [])]


DIAGRAMAS_BASE = [
    (1, "recorrido-completo", recorrido),
    (2, "crear-el-nrc", crear_nrc),
    (3, "carga-lectiva", carga_lectiva),
    (4, "persona-y-admision", persona_admision),
    (5, "matricula-en-el-nrc", matricula),
    (6, "notas-y-pase-a-historia", notas),
]


def diagramas_de(c):
    """[(número, slug, función(c))]: los 6 flujos base, los propios del centro y una casuística por diagrama."""
    propios = [(7, "ligas-teorico-y-club", lambda c: ligas(c, 7))] if c.d.get("ligas") and c.d["ligas"].get("secundaria") else []
    return demostraciones_de(c) + DIAGRAMAS_BASE + propios + casuisticas_de(c, 7 + len(propios))


# --------------------------------------------------------------------------- 0 (común)
def tres_centros(centros, tr):
    """El mismo flujo en los tres centros: cada fila es un centro, cada columna un código."""
    nodos, carriles = [], []
    for c in centros:
        d = c.d
        validados = sum(1 for s in d["scripts"].values() if s["estado"] == "validado")
        total = sum(1 for s in d["scripts"].values() if s["estado"] != "no aplica")
        if c.prerrequisito_fatal:
            avanzar, tag_av = "BASIC I antes que II", "prerrequisito Fatal"
        else:
            avanzar, tag_av = "orden por confirmar", d["prerrequisitos"].get("duda", "")
        cursos = {"idiomas": "BASIC I … INTERM. III", "computacion": "ESEC 00650 a 00657"}.get(
            c.id, d["cursos_conocidos"][0].split(" (")[0])
        duracion = {"idiomas": "8 y 12–13 semanas", "computacion": "4 a 8 semanas", "emprendimiento": "10 semanas"}[c.id]
        lane = c.id
        carriles.append({"id": lane, "label": f"{c.nombre} · nivel {c.nivel}"})
        fila = [
            ("SOATERM", f"partes {c.partes}", duracion, "backend", "calendar"),
            ("SSASECT", cursos, f"materia {c.materia}", "backend", None),
            ("SAAQUIK", f"programa {c.programa}", f"nivel {c.nivel}", "backend", None),
            ("SFAREGS", avanzar, tag_av, "backend", None),
            ("SHAGRDE", c.escala, "nota final", "backend", None),
            ("En TEST", f"{validados} de {total} scripts", "validados", "database", "success"),
        ]
        fila_nodos = [paso(f"{lane}_{k}", lane, k, cod, sub, tag, tipo, icono, ancho=150)
                      for k, (cod, sub, tag, tipo, icono) in enumerate(fila)]
        nodos += fila_nodos
    aristas = []
    for c in centros:
        fila = [n for n in nodos if n["lane"] == c.id]
        aristas += [{"id": f"e-{a['id']}-{b['id']}", "from": a["id"], "to": b["id"], "variant": "default"}
                    for a, b in zip(fila, fila[1:])]
    m = {
        "title": f"Centros Empresariales · 0. {TITULOS['tres-centros']} (Capacidades 1 a 8)",
        "subtitle": "Capacidades 1 a 8 · Idiomas, Computación y Emprendimiento · Escuela EM · Campus S · Elaborado por: " + centros[0].autor,
        "locale": "es",
        "translations": tr,
        "output": "centros/comun/diagramas/00-tres-centros/centros-00-tres-centros.html",
        "quality_profile": "showcase",
        "legend": LEYENDA_FLUJO,
        "views": [vista(c.id, c.nombre, [n["id"] for n in nodos if n["lane"] == c.id],
                        " · ".join(c.d["particularidades"])[:140]) for c in centros],
    }
    comun = centros[0].comun
    spec = {
        "schema_version": 2, "diagram_type": "workflow", "meta": m, "lanes": carriles,
        "nodes": nodos, "edges": aristas,
        "cards": [
            {"dot": "cyan", "title": "Igual en los tres", "items": [
                f"Escuela {comun['escuela']['codigo']} · campus {comun['campus']['codigo']} · grado {comun['grado']['codigo']} (no otorga grado)",
                "Periodos 202651 (2026-0), 202654 (2026-I) y 202656 (2026-II)",
                "Mismo flujo: SOATERM → SSASECT → SAAQUIK → SFAREGS → SHAGRDE → SHRROLL",
                "Matriculan alumnos de la USS (Pregrado y Posgrado) y externos",
                CITAS["egreso"],
            ]},
            {"dot": "violet", "title": "Dónde se diferencian", "items": [
                "Idiomas: prerrequisito Fatal y examen de suficiencia",
                "Computación: sin suficiencia; escala del nivel C con modo V",
                "Emprendimiento: partes de 10 semanas que se cruzan (P02 y P03)",
            ]},
            {"dot": "amber", "title": "Por confirmar", "items": [
                "Programa, materia y escala de Idiomas y de Emprendimiento (verificar en TEST)",
                "U02: orden de los cursos de Computación y Emprendimiento",
                "U21: ¿Emprendimiento rinde suficiencia?",
            ]},
        ],
    }
    return "workflow", spec


DIAGRAMAS_COMUNES = [
    (0, "tres-centros", tres_centros),
]
