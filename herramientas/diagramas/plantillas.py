"""Plantillas de los diagramas paso a paso de cada centro (especificaciones Archify).

Cada plantilla recibe un Centro y las traducciones de la interfaz, y devuelve
(tipo, especificación). El flujo es el mismo para los tres centros; lo que cambia
(códigos, grupos, reglas propias, evidencia de TEST y dudas) sale de
centros/<centro>/datos.json. La ruta de salida va en spec["meta"]["output"].

Reglas de Archify que estas plantillas respetan (las valida `finalize`):
- columnas 0..5 en flujos (0..4 en estados) y un nodo por carril y columna,
  salvo pilas con yOffset;
- títulos de nodo de hasta unos 20 caracteres con ancho 140;
- ancho total ≤ 1240 px y ningún cruce ni corredor compartido entre flechas.
"""

TITULOS = {
    "tres-centros": "Los tres centros en Banner",
    "recorrido-completo": "Recorrido completo en Banner",
    "crear-nrc": "Crear un NRC paso a paso (SSASECT)",
    "persona-y-admision": "Persona y admisión paso a paso",
    "estados-de-la-matricula": "Estados de la matrícula en el NRC",
    "notas-y-cierre": "Notas, asistencia y cierre de actas",
    "casuisticas-de-matricula": "Casuísticas de matrícula",
    "casuisticas-de-notas-y-cierre": "Casuísticas de notas y cierre",
}

LEYENDA_FLUJO = {
    "mode": "auto",
    "entries": {
        "frontend": {"label": "Autoservicio web"},
        "backend": {"label": "Página de Banner (backoffice)"},
        "security": {"label": "Control, error o bloqueo"},
        "messagebus": {"label": "Proceso masivo (GJAPCTL)"},
        "database": {"label": "Historia académica y CAPP"},
        "cloud": {"label": "Cobro (Finanzas)"},
        "external": {"label": "Persona (participante o docente)"},
    },
}

LEYENDA_ESTADOS = {
    "mode": "auto",
    "entries": {
        "start": {"label": "Inicio"},
        "active": {"label": "En curso"},
        "waiting": {"label": "Bloqueo o espera"},
        "decision": {"label": "Validación de Banner"},
        "success": {"label": "Logrado"},
        "failure": {"label": "Salida"},
        "neutral": {"label": "Sin cambio"},
    },
}

CITAS = {
    "periodo": "Periodo y partes: instructivos 1.1.1 y 1.1.2",
    "catalogo": "Catálogo y prerrequisitos: instructivos 1.1.4 (SCACRSE) y 1.1.5 (SCAPREQ)",
    "nrc": "NRC en SSASECT: instructivo 5.3, diap. 19 a 32",
    "docente": "Docente en el NRC: instructivo 6.2.1, diap. 11 a 19",
    "persona": "Persona: instructivo 5.1.1 (GOAMTCH, SPAIDEN)",
    "admision": "Admisión rápida: instructivo 3.2.1 (SAAQUIK)",
    "estudiante": "Registro del estudiante: instructivo 4.1.1 (SGASTDN)",
    "inscripcion": "Inscripción: instructivo 5.4 (SFAREGS, sobrepasos y retiro)",
    "retencion": "Retenciones: SOAHOLD (instructivos 5.2.1 y 5.2.2)",
    "escala": "Escalas y modos: instructivo 7.1.3, diap. 16 (SHAGRDE)",
    "notas": "Plan de evaluación y notas: instructivos 7.1.4 (SHAGCOM) y 7.1.6 (SFASLST)",
    "cierre": "Pase a historia: instructivo 7.1.9 (SHRROLL)",
    "capp": "CAPP: instructivo 7.2.4, diap. 30 a 55",
    "convalidacion": "Convalidación: capacidad 3.3 (SHATRNS, SHATFAC)",
    "egreso": "Requisito de egreso de pregrado: instructivo 8 (diap. 13)",
}

ESTADO_TEXTO = {
    "validado": "validado en TEST",
    "pendiente": "pendiente en TEST",
    "por probar": "por probar en TEST",
    "no aplica": "no aplica",
    "por definir": "por definir",
}


# --------------------------------------------------------------------------- ayudas
def salida(c, numero, slug):
    """Ruta relativa del HTML: centros/<centro>/diagramas/NN-slug/<centro>-NN-slug.html"""
    return f"centros/{c.id}/diagramas/{numero:02d}-{slug}/{c.id}-{numero:02d}-{slug}.html"


def vista(id_, etiqueta, foco, nota):
    return {"id": id_, "label": etiqueta, "focus": foco, "note": nota}


def nodo(id_, carril, col, tipo, etiqueta, sub=None, tag=None, ancho=140, **extra):
    n = {"id": id_, "lane": carril, "col": col, "type": tipo, "label": etiqueta, "width": ancho}
    if sub:
        n["sublabel"] = sub
    if tag:
        n["tag"] = tag
    n.update(extra)
    return n


def estado(id_, carril, col, tipo, etiqueta, sub=None, tag=None, paso=None):
    s = {"id": id_, "lane": carril, "col": col, "type": tipo, "label": etiqueta}
    if sub:
        s["sublabel"] = sub
    if tag:
        s["tag"] = tag
    if paso:
        s["step"] = paso
    return s


def arista(desde, hasta, etiqueta=None, variante="default", **extra):
    e = {"id": f"e-{desde}-{hasta}", "from": desde, "to": hasta, "variant": variante}
    if etiqueta:
        e["label"] = etiqueta
    e.update(extra)
    return e


def transicion(desde, hasta, etiqueta=None, variante=None, **extra):
    t = {"id": f"t-{desde}-{hasta}", "from": desde, "to": hasta}
    if etiqueta:
        t["label"] = etiqueta
    if variante:
        t["variant"] = variante
    t.update(extra)
    return t


def tarjetas(c, probado, ellucian, propio=None):
    t = [
        {"dot": "emerald", "title": "Probado en TEST", "items": probado},
        {"dot": "cyan", "title": "En Ellucian (instructivos)", "items": ellucian},
    ]
    if propio:
        t.append({"dot": "violet", "title": f"Lo propio del {c.nombre}", "items": propio})
    t.append({"dot": "amber", "title": "Por confirmar", "items": c.dudas()})
    return t


def flujo(c, numero, slug, titulo, tr, vistas, carriles, nodos, aristas, cards, fases=None, camino=None):
    m = {
        "title": f"{c.nombre} · {numero}. {titulo}",
        "subtitle": c.subtitulo(),
        "locale": "es",
        "translations": tr,
        "output": salida(c, numero, slug),
        "quality_profile": "showcase",
        "legend": LEYENDA_FLUJO,
        "views": vistas,
    }
    spec = {"schema_version": 2, "diagram_type": "workflow", "meta": m, "lanes": carriles}
    if fases:
        spec["phases"] = fases
    if camino:
        m["animation"] = "trace"
        spec["mainPath"] = camino
    spec.update({"nodes": nodos, "edges": aristas, "cards": cards})
    return "workflow", spec


def evidencia(c, ids):
    """Evidencia de TEST de los scripts indicados (solo los validados)."""
    items = [f"Script {i}: {c.script(i)['evidencia']}" for i in ids if c.script(i)["estado"] == "validado"]
    return items or ["Ninguno de estos casos se probó todavía con este centro en TEST"]


# --------------------------------------------------------------------------- 1
def recorrido(c, tr):
    """De inicio a fin: preparar el periodo, programar, admitir, inscribir, dictar y cerrar."""
    d = c.d
    nrc = c.nrc_ejemplo
    tag_nrc = f"NRC {nrc} · parte {c.parte_ejemplo}" if nrc else f"parte {c.parte_ejemplo} (ejemplo)"
    if d["capp"]:
        tag_capp = f"área {d['capp']['area']} · regla {d['capp']['regla']}"
    elif c.prerrequisito_fatal:
        tag_capp = "BASIC I antes que BASIC II"
    else:
        tag_capp = "malla en CAPP por confirmar"
    tag_cat = {
        "computacion": f"{c.curso_ejemplo} · {d['capp']['regla']}" if d["capp"] else c.curso_ejemplo,
        "idiomas": "BASIC I … INTERMEDIATE III",
    }.get(c.id, c.curso_ejemplo)

    nodos = [
        nodo("periodo", "ra", 0, "backend", "1. Abrir el periodo", "STVTERM · SOATERM", f"{c.periodo_ejemplo} · {c.partes}"),
        nodo("catalogo", "ce", 0, "backend", "2. Catálogo y malla", "SCACRSE · SMAAREA", tag_cat),
        nodo("nrc", "ce", 1, "backend", "3. Programar el NRC", "SSASECT · SSARRES", tag_nrc),
        nodo("docente", "ra", 1, "backend", "4. Docente y carga", "SIAINST · SIAASGN", "principal al 100 %"),
        nodo("solicita", "par", 2, "external", "5. Pide el curso", "externo o de pregrado", "requisito de egreso"),
        nodo("admision", "adm", 2, "backend", "6. Persona y admisión", "GOAMTCH · SAAQUIK", f"programa {c.programa}"),
        nodo("capp", "ra", 2, "database", "7. CAPP y proyección", "SMARQCM · SFAPROJ", tag_capp),
        nodo("inscribe", "ra", 3, "backend", "8. Inscribir en NRC", "SFAREGS o autoservicio", "estatus EL → curso RE"),
        nodo("cobro", "fin", 3, "cloud", "9. Generar el cobro", "SFARGFE · TSAAREV", "al inscribir"),
        nodo("paga", "par", 3, "external", "10. Paga", "TVACAJA", "con deuda: retención"),
        nodo("notas", "doc", 4, "frontend", "11. Clases y notas", "SHAGCOM · autoservicio", c.escala),
        nodo("consulta", "par", 4, "frontend", "12. Asiste y consulta", "autoservicio del alumno"),
        nodo("rolar", "ra", 5, "messagebus", "13. Pase a historia", "GJAPCTL → SHRROLL", "cierre de actas", yOffset=-46),
        nodo("cappm", "ra", 5, "messagebus", "14. CAPP masivo", "GJAPCTL → SMRBCMP", "avance de todos", yOffset=46),
        nodo("resultado", "par", 5, "database", "15. Resultado", "SHACRSE · SMICRLT", "aprueba: sigue · desaprueba: repite"),
    ]
    aristas = [
        arista("periodo", "catalogo", None, fromSide="top", toSide="bottom", route="straight"),
        arista("catalogo", "nrc", "curso existe"),
        arista("nrc", "docente", "asigna docente"),
        arista("solicita", "admision", "solicitud", "emphasis"),
        arista("admision", "capp", "estudiante activo", "emphasis"),
        arista("capp", "inscribe", "su curso", "emphasis"),
        arista("nrc", "inscribe", "NRC con cupo", "dashed"),
        arista("inscribe", "cobro", "genera cobro"),
        arista("cobro", "paga", "deuda"),
        arista("inscribe", "notas", "lista del NRC", "emphasis", fromSide="right", toSide="top"),
        arista("notas", "consulta", "publica"),
        arista("notas", "rolar", "notas finales", "emphasis", fromSide="right", toSide="left"),
        arista("rolar", "cappm", "historia", "emphasis"),
        arista("cappm", "resultado", "avance", "emphasis"),
    ]
    probado = {
        "computacion": [
            "NRC 1021 y 1026 (ESEC 00650, parte X07, periodo 202656)",
            "Persona S00581108 creada en GOAMTCH y admitida con CMEMC38",
            "Notas 16, 10, 08 e INH; SHRROLL job 8114 exitoso",
            "CAPP: con nota 08 el curso queda «no usado» (script 10)",
        ],
        "idiomas": ["Todavía no hay un NRC de Idiomas en TEST",
                    "Lo validado en Computación sirve de guía, pero hay que probarlo con el nivel I"],
        "emprendimiento": ["NRC 1025 (ESGE 00117) en la carga del docente (SIAASGN)",
                           "Falta probar matrícula, notas y cierre con el nivel M"],
    }[c.id]
    return flujo(
        c, 1, "recorrido-completo", TITULOS["recorrido-completo"], tr,
        [
            vista("preparar", "Preparar y programar", ["periodo", "catalogo", "nrc", "docente"],
                  "Lo que debe existir antes de admitir a nadie: periodo, catálogo, NRC y docente."),
            vista("admitir", "Admitir, inscribir y cobrar", ["solicita", "admision", "capp", "inscribe", "cobro", "paga"],
                  "Del pedido del participante a su inscripción en el NRC y el cobro."),
            vista("cerrar", "Clases, notas y cierre", ["notas", "consulta", "rolar", "cappm", "resultado"],
                  "Notas del docente, pase a historia, CAPP y siguiente curso (detalle en el diagrama 5)."),
        ],
        [
            {"id": "ce", "label": f"Jefatura del {c.nombre}"},
            {"id": "ra", "label": "Registros Académicos"},
            {"id": "adm", "label": "Admisión"},
            {"id": "fin", "label": "Finanzas"},
            {"id": "doc", "label": "Docente"},
            {"id": "par", "label": "Participante"},
        ],
        nodos, aristas,
        tarjetas(c, probado, [CITAS["periodo"], CITAS["nrc"], CITAS["admision"], CITAS["capp"], CITAS["notas"],
                              CITAS["cierre"], CITAS["egreso"]], d["particularidades"]),
        fases=[
            {"id": "f0", "label": "Preparar el periodo", "fromCol": 0, "toCol": 0},
            {"id": "f1", "label": "Programar el grupo", "fromCol": 1, "toCol": 1},
            {"id": "f2", "label": "Admitir", "fromCol": 2, "toCol": 2, "variant": "emphasis"},
            {"id": "f3", "label": "Inscribir y cobrar", "fromCol": 3, "toCol": 3, "variant": "emphasis"},
            {"id": "f4", "label": "Dictar clases", "fromCol": 4, "toCol": 4},
            {"id": "f5", "label": "Cerrar y avanzar", "fromCol": 5, "toCol": 5, "variant": "dashed"},
        ],
        camino=["solicita", "admision", "capp", "inscribe", "notas", "rolar", "cappm", "resultado"],
    )


# --------------------------------------------------------------------------- 2
def crear_nrc(c, tr):
    """SSASECT paso a paso: requisitos, tres guardados, verificación y errores frecuentes."""
    n = c.nrc(c.nrc_ejemplo) if c.nrc_ejemplo else None
    seccion = n["seccion"] if n else "A (ejemplo)"
    tag_cupo = f"cupo {n['cupo']} · 2.º GUARDAR" if n and n.get("cupo") else "2.º GUARDAR"
    tag_curso = "BASIC I y su prerrequisito" if c.prerrequisito_fatal else c.curso_ejemplo
    nodos = [
        nodo("p1", "otras", 0, "backend", "1. Periodo y parte", "STVTERM · SOATERM", f"{c.periodo_ejemplo} · {c.parte_ejemplo}"),
        nodo("p2", "otras", 1, "backend", "2. Curso en catálogo", "SCACRSE · SCAPREQ", tag_curso),
        nodo("p3", "otras", 2, "backend", "3. Docente activo", "SIAINST en el periodo", "factor en SIATERM"),
        nodo("p4", "ssa", 2, "backend", "4. Crear NRC", "periodo + Crear NRC", "queda en ADD"),
        nodo("p5", "ssa", 3, "backend", "5. Datos de sección", f"{c.curso_ejemplo} · secc. {seccion}", "1.er GUARDAR → nº NRC"),
        nodo("p6", "ssa", 4, "backend", "6. Cupo y reservas", "Máximo · SSARRES", tag_cupo),
        nodo("p7", "ssa", 5, "backend", "7. Horario y docente", "SAUVIR · principal 100 %", "3.er GUARDAR"),
        nodo("p8", "otras", 5, "backend", "8. Verificar el NRC", "SSASECQ · SSAPREQ", "cupo real y restante"),
        nodo("e5", "err", 3, "security", "Sin guardar", "«Debe guardar antes de salir»", "GUARDAR antes de cambiar"),
        nodo("e6", "err", 4, "security", "Sección cerrada", "«Closed» al inscribir", "subir Máximo o reserva"),
        nodo("e7", "err", 5, "security", "Sesión sin horas", "sesión distinta", "01 en horario y docente"),
    ]
    aristas = [
        arista("p1", "p2", "parte lista"),
        arista("p2", "p3"),
        arista("p3", "p4", "requisitos listos", "emphasis"),
        arista("p4", "p5", None, "emphasis"),
        arista("p5", "p6", None, "emphasis"),
        arista("p6", "p7", None, "emphasis"),
        arista("p7", "p8", "NRC listo", "emphasis"),
        arista("p5", "e5", "si cambias de pestaña", "security"),
        arista("p6", "e6", "sin cupo", "security"),
        arista("p7", "e7", "si no coincide", "security"),
    ]
    probado = {
        "computacion": [
            "NRC 1021: ESEC 00650, sección B, parte X07, cupo 2 (28/09)",
            "NRC 1026: sección D, lunes y miércoles 08:00–12:00, aula SAUVIR, cupo 1 → 4 (02/10)",
            "Docente 100582059 como principal al 100 %",
            "Errores vistos y resueltos: «Debe guardar antes de salir», «Closed», «Sesión sin horas»",
        ],
        "idiomas": ["Todavía no hay un NRC de Idiomas en TEST",
                    "Los errores de abajo se vieron en Computación: sirven de aviso"],
        "emprendimiento": ["NRC 1025: ESGE 00117, sección A, con el docente en la sesión 02 (no principal)",
                           "Los errores de abajo se vieron en Computación: sirven de aviso"],
    }[c.id]
    propio = list(c.d["particularidades"])
    if c.id == "idiomas":
        propio.append("Duda: si el nivel III dura 12 o 13 semanas, ¿va en otra parte de periodo?")
    return flujo(
        c, 2, "crear-nrc", TITULOS["crear-nrc"], tr,
        [
            vista("requisitos", "Antes de SSASECT", ["p1", "p2", "p3"], "Sin periodo, curso en catálogo y docente activo no se puede programar el NRC."),
            vista("guardados", "Los tres guardados", ["p4", "p5", "p6", "p7"], "Sección de curso, ingreso (cupo) y horario con docente: se guarda en cada pestaña."),
            vista("errores", "Errores frecuentes", ["e5", "e6", "e7"], "Mensajes que salieron en TEST y cómo se resolvieron."),
        ],
        [
            {"id": "otras", "label": "Otras páginas de Banner"},
            {"id": "ssa", "label": "SSASECT (tres guardados)"},
            {"id": "err", "label": "Si sale un error", "variant": "exception"},
        ],
        nodos, aristas,
        tarjetas(c, probado, [CITAS["periodo"], CITAS["catalogo"], CITAS["nrc"], CITAS["docente"]], propio),
        camino=["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8"],
    )


# --------------------------------------------------------------------------- 3
def persona_admision(c, tr):
    """GOAMTCH (persona) y SAAQUIK (admisión), con los dos casos especiales."""
    id_nuevo = f"ID {c.d['persona_ejemplo']}" if c.d["persona_ejemplo"] else "ID S00… nuevo"
    if c.confirmado_en_test:
        tag_fin = f"mayor {c.mayor} · {c.departamento}"
    else:
        tag_fin = "mayor y depto. por confirmar"
    s06 = ESTADO_TEXTO[c.script("06")["estado"]]
    nodos = [
        nodo("a1", "per", 0, "backend", "1. Buscar persona", "GOAMTCH · PERS_NATU", "ID = GENERATED"),
        nodo("a2", "per", 1, "backend", "2. Datos mínimos", "apellidos A/B · DNI", "dirección PP · MOV · PER1"),
        nodo("a3", "per", 2, "backend", "3. Crear y guardar", "Marcar-Duplicar · Crear", id_nuevo),
        nodo("a4", "adm", 3, "backend", "4. Encabezado", f"{c.periodo_ejemplo} · nivel {c.nivel}", "alumno R · estatus AS"),
        nodo("a5", "adm", 4, "backend", "5. Programa", "currículo base", f"programa {c.programa}"),
        nodo("a6", "adm", 5, "database", "6. Guardar y revisar", "SGASTDN · Curricula", tag_fin),
        nodo("x1", "esp", 1, "security", "Ya existe", "mismo DNI o nombre", "usar su ID actual"),
        nodo("x2", "esp", 4, "external", "Ya es de pregrado", "segundo plan de estudios", f"Script 06 · {s06}"),
    ]
    aristas = [
        arista("a1", "a2", "no existe", "emphasis"),
        arista("a2", "a3", "datos", "emphasis"),
        arista("a3", "a4", "ID nuevo", "emphasis"),
        arista("a4", "a5", "Ir", "emphasis"),
        arista("a5", "a6", "OK", "emphasis"),
        arista("a1", "x1", "duplicado", "security"),
        arista("x1", "a4", "admitir con su ID", "dashed"),
        arista("a5", "x2", "si ya estudia", "dashed"),
    ]
    probado = {
        "computacion": [
            "Personas S00581081, S00581108 a S00581111 creadas en GOAMTCH",
            "Admisión con CMEMC38: se completan ACXP, EMCI e INPROGRESS",
            "S00581091 con pregrado y Computación a la vez (script 06)",
        ],
        "idiomas": ["Falta conocer el programa de Idiomas en TEST (por confirmar)",
                    "La creación de la persona es igual para los tres centros"],
        "emprendimiento": ["Falta conocer el programa de Emprendimiento en TEST (por confirmar)",
                           "La creación de la persona es igual para los tres centros"],
    }[c.id]
    return flujo(
        c, 3, "persona-y-admision", TITULOS["persona-y-admision"], tr,
        [
            vista("persona", "Crear la persona", ["a1", "a2", "a3", "x1"], "GOAMTCH evita duplicados: si ya existe, se usa su ID."),
            vista("admision", "Admitir al programa", ["a4", "a5", "a6", "x2"], "SAAQUIK asigna nivel y programa; SGASTDN queda activo."),
        ],
        [
            {"id": "per", "label": "Crear la persona (GOAMTCH)"},
            {"id": "adm", "label": "Admitir al programa (SAAQUIK)"},
            {"id": "esp", "label": "Casos especiales", "variant": "exception"},
        ],
        nodos, aristas,
        tarjetas(c, probado, [CITAS["persona"], CITAS["admision"], CITAS["estudiante"], CITAS["egreso"]]),
        fases=[
            {"id": "f0", "label": "Persona", "fromCol": 0, "toCol": 2},
            {"id": "f1", "label": "Admisión", "fromCol": 3, "toCol": 5, "variant": "emphasis"},
        ],
        camino=["a1", "a2", "a3", "a4", "a5", "a6"],
    )


# --------------------------------------------------------------------------- 4
def matricula(c, tr):
    """Estados de la inscripción del participante en el NRC (SFAREGS)."""
    def tag(i):
        return f"Script {i} · {c.script(i)['estado']}"

    nrc = f"NRC {c.nrc_ejemplo} + Tab" if c.nrc_ejemplo else "NRC + Tab"
    estados = [
        estado("admitido", "main", 0, "start", "Admitido", "SGASTDN · AS", paso="01"),
        estado("plan", "main", 1, "active", "Plan autorizado", "SFAREGS · EL", paso="02"),
        estado("ingresa", "main", 2, "decision", "Ingresa el NRC", nrc, "Banner valida", paso="03"),
        estado("inscrito", "main", 3, "success", "Inscrito (RE)", "cupo real +1", paso="04"),
        estado("lista", "main", 4, "success", "En la lista", "SFASLST · docente", paso="05"),
        estado("inactivo", "alumno", 0, "waiting", "Inactivo", "SGASTDN · IS o SU", tag("09")),
        estado("retencion", "alumno", 2, "waiting", "Con retención", "SOAHOLD · error fatal", tag("18-B")),
        estado("cerrada", "seccion", 2, "waiting", "Sección cerrada", "cupo lleno", tag("15")),
        estado("retirado", "terminal", 4, "failure", "Retirado (DD)", "libera el cupo", tag("08")),
    ]
    trans = [
        transicion("admitido", "plan", "autoriza plan"),
        transicion("plan", "ingresa", "NRC"),
        transicion("ingresa", "inscrito", "todo en orden", "emphasis"),
        transicion("inscrito", "lista"),
        transicion("admitido", "inactivo", "suspende", "security"),
        transicion("inactivo", "plan", "reactiva AS"),
        transicion("ingresa", "retencion", "con deuda", "security"),
        transicion("retencion", "inscrito", "paga y libera"),
        transicion("ingresa", "cerrada", "sin cupo", "security"),
        transicion("cerrada", "inscrito", "amplía cupo"),
        transicion("inscrito", "retirado", "retiro DD", "security"),
    ]
    if c.prerrequisito_fatal:
        estados.append(estado("prereq", "seccion", 3, "waiting", "Sin BASIC I", "prerrequisito Fatal", tag("04")))
        trans += [
            transicion("ingresa", "prereq", "BASIC II sin BASIC I", "security"),
            transicion("prereq", "inscrito", "suficiencia (SOATEST)"),
        ]
    probado = evidencia(c, ["01", "08", "09", "15", "16", "18-B"])
    propio = list(c.d["particularidades"])
    propio.append("Traslado de sección (script 16): DD en el NRC de origen y RE en el de destino")
    m = {
        "title": f"{c.nombre} · 4. {TITULOS['estados-de-la-matricula']}",
        "subtitle": c.subtitulo(),
        "locale": "es",
        "translations": tr,
        "output": salida(c, 4, "estados-de-la-matricula"),
        "quality_profile": "showcase",
        "animation": "trace",
        "legend": LEYENDA_ESTADOS,
        "views": [
            vista("normal", "Camino normal", ["admitido", "plan", "ingresa", "inscrito", "lista"], "Admitido, plan autorizado (EL), NRC ingresado e inscrito (RE)."),
            vista("bloqueos", "Bloqueos y cómo se liberan", [s["id"] for s in estados if s["lane"] in ("alumno", "seccion")], "Lo que impide inscribir y la acción que lo destraba."),
        ],
    }
    spec = {
        "schema_version": 2, "diagram_type": "lifecycle", "meta": m,
        "lanes": [
            {"id": "main", "label": "Camino normal (SFAREGS)"},
            {"id": "alumno", "label": "Bloqueos del alumno"},
            {"id": "seccion", "label": "Bloqueos de la sección o del curso"},
            {"id": "terminal", "label": "Salidas"},
        ],
        "states": estados, "transitions": trans,
        "cards": tarjetas(c, probado, [CITAS["inscripcion"], CITAS["retencion"], CITAS["estudiante"]]
                          + ([CITAS["catalogo"]] if c.prerrequisito_fatal else []), propio),
    }
    return "lifecycle", spec


# --------------------------------------------------------------------------- 5
def notas_cierre(c, tr):
    """Escala, plan de evaluación, asistencia y notas, pase a historia y resultado en CAPP."""
    e = c.d["escala"]
    tag_escala = f"nivel {c.nivel} · modo {e['modo']}" if e else f"nivel {c.nivel}: por confirmar"
    aprobo = f"nota {e['nota_minima']} o más" if e else "nota mínima por confirmar"
    if c.prerrequisito_fatal:
        tag_desaprobo = "no pasa a BASIC II"
    else:
        tag_desaprobo = f"repite · Script 10"
    nodos = [
        nodo("n1", "ra", 0, "backend", "1. Escala del nivel", "SHAGRDE", tag_escala),
        nodo("n2", "ra", 1, "backend", "2. Plan de evaluación", "SHAGCOM", "componentes y pesos"),
        nodo("n3", "doc", 2, "frontend", "3. Asistencia", "por sesión · autoservicio", "poca asistencia: INH"),
        nodo("n4", "doc", 3, "frontend", "4. Notas", "parciales y final", c.escala),
        nodo("n5", "proc", 4, "messagebus", "5. Pase a historia", "GJAPCTL → SHRROLL", "notas a SHACRSE"),
        nodo("x5", "err", 4, "security", "Escala sin el modo", "«No Substitute Grade»", "agregar modo en SHAGRDE"),
        nodo("r1", "par", 5, "database", "6. Aprobó", aprobo, "CAPP: cumple", yOffset=-46),
        nodo("r2", "par", 5, "database", "7. Desaprobó o INH", "curso no usado", tag_desaprobo, yOffset=46),
    ]
    aristas = [
        arista("n1", "n2", "escala lista", "emphasis"),
        arista("n2", "n3", "pesos", "emphasis"),
        arista("n3", "n4", "asistencia", "emphasis"),
        arista("n4", "n5", "actas", "emphasis"),
        arista("n5", "x5", "si falla", "security"),
        arista("n5", "r1", "aprobado", "emphasis"),
        arista("n5", "r2", "desaprobado", "security"),
    ]
    probado = evidencia(c, ["13", "12", "14", "10"])
    if c.id == "computacion":
        probado.append("U20: SHAGRDE del nivel C solo tenía modo P; al agregar V, SHRROLL pasó (job 8114)")
    else:
        probado.append("Lección de Computación (U20): revisar que SHAGRDE del nivel "
                       f"{c.nivel} tenga el modo de calificación del curso antes de cerrar")
    return flujo(
        c, 5, "notas-y-cierre", TITULOS["notas-y-cierre"], tr,
        [
            vista("preparar", "Antes de calificar", ["n1", "n2"], "La escala del nivel y el plan de evaluación del NRC."),
            vista("docente", "Lo que hace el docente", ["n3", "n4"], "Asistencia por sesión y notas por autoservicio (o SFASLST)."),
            vista("cierre", "Cierre y resultado", ["n5", "x5", "r1", "r2"], "SHRROLL pasa las notas a la historia; CAPP decide si avanza o repite."),
        ],
        [
            {"id": "ra", "label": "Registros Académicos"},
            {"id": "doc", "label": "Docente (autoservicio)"},
            {"id": "proc", "label": "Proceso masivo (GJAPCTL)"},
            {"id": "par", "label": "Participante y CAPP"},
            {"id": "err", "label": "Si falla el cierre", "variant": "exception"},
        ],
        nodos, aristas,
        tarjetas(c, probado, [CITAS["escala"], CITAS["notas"], CITAS["cierre"], CITAS["capp"]], c.d["particularidades"]),
        fases=[
            {"id": "f0", "label": "Preparar", "fromCol": 0, "toCol": 1},
            {"id": "f1", "label": "Dictar", "fromCol": 2, "toCol": 3, "variant": "emphasis"},
            {"id": "f2", "label": "Cerrar", "fromCol": 4, "toCol": 5, "variant": "dashed"},
        ],
        camino=["n1", "n2", "n3", "n4", "n5", "r1"],
    )


# --------------------------------------------------------------------------- 6 y 7
def caso(c, id_script):
    """Situación, pasos y resultado de un script (iguales para todos, con ajustes por centro)."""
    casos = {
        "01": (("Primera matrícula", "admitido en su programa"),
               [("SFAREGS", "plan 1 · estatus EL"), ("Ingresa el NRC", "curso en RE")],
               ("Inscrito", "cupo real +1")),
        "03": (("Curso externo", "aprobado en otra institución"),
               [("SHATRNS", "institución y curso"), ("SHATFAC", "nota y créditos"), ("SHRROLL", "pase a historia")],
               ("Convalidado", "CAPP lo cuenta")),
        "04": (("Ya sabe inglés", "quiere saltar BASIC I"),
               [("SOATEST", "puntaje del examen"), ("SFAREGS", "inscribe BASIC II")],
               ("En BASIC II", "puntaje mínimo: U01")),
        "08": (("Se retira", "antes de la fecha límite"),
               [("SFAREGS", "código DD"), ("SSASECQ", "revisar el cupo")],
               ("Vacante libre", "cupo restante +1")),
        "09": (("Suspendido", "estatus IS o SU"),
               [("SFAREGS", "bloquea la inscripción"), ("SGASTDN", "vuelve a AS")],
               ("Puede inscribirse", "elegible de nuevo")),
        "10": (("Desaprueba", "nota bajo el mínimo"),
               [("SFASLST", "nota final"), ("SHRROLL", "pase a historia"), ("SMARQCM", "CAPP → SMICRLT")],
               ("Curso no usado", "repite el curso")),
        "12": (("Cierre de actas", "fin del grupo"),
               [("SHAGRDE", "modo del curso"), ("GJAPCTL", "SHRROLL por NRC")],
               ("Notas en historia", "Rolled to History")),
        "13": (("Notas del nivel", f"nivel {c.nivel}"),
               [("SHAGRDE", "escala y modo"), ("SFASLST", "notas finales")],
               ("Aprueba o no", c.escala)),
        "15": (("Sección llena", "error «Closed»"),
               [("SSASECT", "subir el Máximo"), ("SSARRES", "reserva del programa")],
               ("Se inscribe", "cupo ampliado")),
        "16": (("Cambio de sección", "otro horario o grupo"),
               [("SFAREGS", "DD en el NRC origen"), ("SFAREGS", "RE en el NRC destino")],
               ("En el nuevo NRC", "revisar en SFASLST")),
        "18-B": (("Tiene deuda", "mora de cuota"),
                 [("SOAHOLD", "retención TT"), ("SFAREGS", "error: retenciones")],
                 ("No se inscribe", "hasta liberar")),
    }
    if c.id == "idiomas" and id_script == "10":
        return (("Desaprueba BASIC I", "nota bajo el mínimo"),
                [("SHRROLL", "nota a la historia"), ("SFAREGS", "BASIC II: error Fatal")],
                ("Repite BASIC I", "o rinde suficiencia"))
    if c.id == "emprendimiento" and id_script == "16":
        return (("Cambio de grupo", "P02 y P03 se cruzan"),
                [("SFAREGS", "DD en el grupo origen"), ("SFAREGS", "RE en el grupo destino")],
                ("En el nuevo grupo", "revisar en SFASLST"))
    return casos[id_script]


def casuisticas(c, tr, numero, slug, titulo, ids, nota):
    nodos, aristas, carriles, primero = [], [], [], None
    for k, i in enumerate(ids):
        (sit, sit_sub), pasos, (res, res_sub) = caso(c, i)
        lane = f"s{k}"
        estado_txt = ESTADO_TEXTO[c.script(i)["estado"]]
        carriles.append({"id": lane, "label": f"Script {i} · {c.nombre_script(i)}"})
        cadena = [f"{lane}_0"]
        nodos.append(nodo(f"{lane}_0", lane, 0, "security", sit, sit_sub, ancho=180))
        for j, (p, p_sub) in enumerate(pasos, start=1):
            tipo = "messagebus" if p in ("SHRROLL", "GJAPCTL") else "backend"
            nodos.append(nodo(f"{lane}_{j}", lane, j, tipo, p, p_sub, ancho=180))
            cadena.append(f"{lane}_{j}")
        nodos.append(nodo(f"{lane}_r", lane, 5, "database", res, res_sub, estado_txt, ancho=180))
        cadena.append(f"{lane}_r")
        for a, b in zip(cadena, cadena[1:]):
            aristas.append(arista(a, b, None, "emphasis" if k == 0 else "default"))
        primero = primero or cadena
    vistas = [vista(f"v{k}", f"Script {i}", [n["id"] for n in nodos if n["lane"] == f"s{k}"],
                    f"{c.nombre_script(i)}: {ESTADO_TEXTO[c.script(i)['estado']]}.")
              for k, i in enumerate(ids)][:5]
    por_probar = [f"Script {i}: {c.script(i)['evidencia']}" for i in ids if c.script(i)["estado"] != "validado"]
    cards = [
        {"dot": "emerald", "title": "Probado en TEST", "items": evidencia(c, ids)},
        {"dot": "cyan", "title": "En Ellucian (instructivos)", "items": nota},
    ]
    if por_probar:
        cards.append({"dot": "rose", "title": "Falta probar", "items": por_probar})
    cards.append({"dot": "amber", "title": "Por confirmar", "items": c.dudas()})
    return flujo(c, numero, slug, titulo, tr, vistas, carriles, nodos, aristas, cards, camino=primero)


def casuisticas_matricula(c, tr):
    return casuisticas(c, tr, 6, "casuisticas-de-matricula", TITULOS["casuisticas-de-matricula"],
                       c.d["casuisticas"]["matricula"],
                       [CITAS["inscripcion"], CITAS["nrc"], CITAS["estudiante"]])


def casuisticas_notas(c, tr):
    return casuisticas(c, tr, 7, "casuisticas-de-notas-y-cierre", TITULOS["casuisticas-de-notas-y-cierre"],
                       c.d["casuisticas"]["notas"],
                       [CITAS["convalidacion"], CITAS["escala"], CITAS["cierre"], CITAS["capp"], CITAS["retencion"]])


DIAGRAMAS = [
    (1, "recorrido-completo", recorrido),
    (2, "crear-nrc", crear_nrc),
    (3, "persona-y-admision", persona_admision),
    (4, "estados-de-la-matricula", matricula),
    (5, "notas-y-cierre", notas_cierre),
    (6, "casuisticas-de-matricula", casuisticas_matricula),
    (7, "casuisticas-de-notas-y-cierre", casuisticas_notas),
]


# --------------------------------------------------------------------------- 0 (común)
def tres_centros(centros, tr):
    """Comparativo: en qué se parecen y en qué se diferencian los tres centros."""
    nodos, aristas, carriles = [], [], []
    for c in centros:
        d = c.d
        validados = sum(1 for s in d["scripts"].values() if s["estado"] == "validado")
        nrcs = ", ".join(n["nrc"] for n in d["nrc_test"]) or "ninguno"
        if c.prerrequisito_fatal:
            avanzar, tag_av = "BASIC I antes que II", "Fatal"
        else:
            avanzar, tag_av = "orden por confirmar", d["prerrequisitos"].get("duda", "")
        sufi = {True: "suficiencia SOATEST", False: "sin suficiencia", None: "suficiencia: U21"}[c.suficiencia]
        cursos = {"idiomas": "BASIC I … INTERM. III", "computacion": "ESEC 00650 a 00657"}.get(
            c.id, d["cursos_conocidos"][0].split(" (")[0])
        duracion = {"idiomas": "8 y 12–13 semanas", "computacion": "4 a 8 semanas", "emprendimiento": "10 semanas"}[c.id]
        lane = c.id
        carriles.append({"id": lane, "label": f"{c.nombre} · nivel {c.nivel}"})
        fila = [
            ("programa", "backend", "Programa", c.programa, f"nivel {c.nivel}"),
            ("grupos", "backend", "Grupos 2026", f"{c.partes} ({d['parte_general']})", duracion),
            ("cursos", "backend", "Cursos", cursos, f"materia {c.materia}"),
            ("avanzar", "security", "Para avanzar", avanzar, f"{tag_av} · {sufi}"),
            ("notas", "frontend", "Notas", c.escala, "SHAGRDE"),
            ("test", "database", "En TEST", f"{validados} script{'s' if validados != 1 else ''} validado{'s' if validados != 1 else ''}", f"NRC: {nrcs}"),
        ]
        for k, (sufijo, tipo, etiqueta, sub, tag) in enumerate(fila):
            nodos.append(nodo(f"{lane}_{sufijo}", lane, k, tipo, etiqueta, sub, tag, ancho=150))
        for (a, *_), (b, *_) in zip(fila, fila[1:]):
            aristas.append(arista(f"{lane}_{a}", f"{lane}_{b}"))
    m = {
        "title": f"Centros Empresariales · 0. {TITULOS['tres-centros']}",
        "subtitle": "Idiomas, Computación y Emprendimiento · Escuela EM · Campus S · Elaborado por: "
                    + centros[0].autor,
        "locale": "es",
        "translations": tr,
        "output": "centros/comun/diagramas/00-tres-centros/centros-00-tres-centros.html",
        "quality_profile": "showcase",
        "legend": LEYENDA_FLUJO,
        "views": [vista(c.id, c.nombre, [n["id"] for n in nodos if n["lane"] == c.id], " · ".join(c.d["particularidades"])[:140])
                  for c in centros],
    }
    comun = centros[0].comun
    spec = {
        "schema_version": 2, "diagram_type": "workflow", "meta": m, "lanes": carriles,
        "nodes": nodos, "edges": aristas,
        "cards": [
            {"dot": "cyan", "title": "Igual en los tres", "items": [
                f"Escuela {comun['escuela']['codigo']} · campus {comun['campus']['codigo']} · grado {comun['grado']['codigo']} (no otorga grado)",
                "Periodos 202651 (2026-0), 202654 (2026-I) y 202656 (2026-II)",
                "Mismo recorrido: NRC → persona → admisión → matrícula → notas → SHRROLL → CAPP",
                CITAS["egreso"],
            ]},
            {"dot": "violet", "title": "Dónde se diferencian", "items": [
                "Idiomas: prerrequisito Fatal y examen de suficiencia",
                "Computación: sin suficiencia; escala del nivel C con modo V",
                "Emprendimiento: grupos de 10 semanas que se cruzan (P02 y P03)",
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
