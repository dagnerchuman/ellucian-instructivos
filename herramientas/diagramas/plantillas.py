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

from centro import leer_json, CENTROS

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
    "cierre": "Pase a historia: instructivo 7.1.9 (SHRROLL)",
    "capp": "CAPP: instructivo 7.2.4, diap. 30 a 55",
    "convalidacion": "Convalidación: capacidad 3.3 (SHATRNS, SHATFAC)",
    "egreso": "Requisito de egreso de Pregrado: instructivo 8, diap. 13",
}

LEYENDA_FLUJO = {
    "mode": "auto",
    "entries": {
        "backend": {"label": "Banner: se registra"},
        "database": {"label": "Banner: se consulta"},
        "frontend": {"label": "Autoservicio (web)"},
        "messagebus": {"label": "Proceso masivo"},
        "cloud": {"label": "Cobro (Finanzas)"},
        "external": {"label": "Fuera de Banner (intranet)"},
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


CATALOGO = {s["id"]: s["nombre"] for s in leer_json(CENTROS / "comun" / "datos.json")["scripts"]}


def slug_script(id_script):
    return f"script-{id_script.lower()}-{slug(CATALOGO[id_script])}"


TITULOS = {
    "tres-centros": "El mismo flujo en los tres centros",
    "recorrido-completo": "Recorrido completo en Banner",
    "crear-el-nrc": "Crear el NRC",
    "carga-lectiva": "Carga lectiva del docente",
    "persona-y-admision": "Persona y admisión",
    "matricula-en-el-nrc": "Matrícula en el NRC",
    "notas-y-pase-a-historia": "Notas y pase a historia",
    **{slug_script(i): f"Script {i} · {n}" for i, n in CATALOGO.items()},
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


def flujo(c, numero, slug_, carriles, nodos, cards, fases=None, vistas=None):
    m = {
        "title": f"{c.nombre} · {numero}. {TITULOS[slug_]}",
        "subtitle": c.subtitulo(),
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
def recorrido(c):
    """Secuencia: quién hace cada paso, de abrir el periodo al avance en CAPP."""
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
            ("registros", "banner", "SOATERM", "emphasis", f"abre el periodo {c.periodo_ejemplo} y la parte {c.parte_ejemplo}"),
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
            ("docente", "banner", "Autoservicio", "emphasis", "el docente registra asistencia y notas"),
            ("registros", "banner", "SHRROLL", "emphasis", "pase a historia de las notas"),
            ("banner", "alumno", "SMICRLT", "return", "el alumno ve su avance en CAPP"),
        ]),
    ]
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
            "Autoservicio y SHRROLL: notas 16, 10, 08 e INH; job 8114 exitoso",
        ],
        "idiomas": ["Todavía no hay un NRC de Idiomas en TEST",
                    "El flujo es el mismo que se validó en Computación; falta probarlo con el nivel I"],
        "emprendimiento": ["SIAASGN: NRC 1025 (ESGE 00117) en la carga del docente",
                           "Falta probar matrícula, notas y pase a historia con el nivel M"],
    }[c.id]
    m = {
        "title": f"{c.nombre} · 1. {TITULOS['recorrido-completo']}",
        "subtitle": c.subtitulo(),
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
    """SSASECT con sus tres guardados, entre la revisión del periodo y la del NRC."""
    n = c.nrc(c.nrc_ejemplo) if c.nrc_ejemplo else None
    cupo = f" · cupo {n['cupo'].split(' (')[0]}" if n and n.get("cupo") else ""
    curso = "BASIC I" if c.id == "idiomas" else c.curso_ejemplo
    nodos = [
        paso("s1", "nrc", 0, "SOATERM", "revisar el periodo", f"{c.periodo_ejemplo} · parte {c.parte_ejemplo}", icono="calendar"),
        paso("s2", "nrc", 1, "SCACRSE", "revisar el curso", curso),
        paso("s3", "nrc", 2, "SSASECT", "crear el NRC", "1.er guardar" + (f" · NRC {c.nrc_ejemplo}" if c.nrc_ejemplo else "")),
        paso("s4", "nrc", 3, "SSASECT", "fijar el cupo", "2.º guardar" + cupo),
        paso("s5", "nrc", 4, "SSASECT", "horario y docente", "3.er guardar · principal 100 %"),
        paso("s6", "nrc", 5, "SSASECQ", "revisar el NRC", "cupo real y restante", "database"),
    ]
    probado = {
        "computacion": [
            "NRC 1021: ESEC 00650, sección B, parte X07 (28/09)",
            "NRC 1026: sección D, lunes y miércoles 08:00–12:00, aula SAUVIR, cupo 1 → 4 (02/10)",
            "NRC de prueba ESEC 00650 A en 202751, parte X01 (Script 11, 05/10)",
        ],
        "idiomas": ["Todavía no hay un NRC de Idiomas en TEST"],
        "emprendimiento": ["NRC 1025: ESGE 00117, sección A, con el docente en la sesión 02 (no principal)"],
    }[c.id]
    errores = {"dot": "rose", "title": "Si sale un error", "items": [
        "«Debe guardar antes de salir»: guarda en cada pestaña antes de pasar a la siguiente",
        "«Closed» al matricular: el NRC está lleno; sube el cupo (Script 15)",
        "«Sesión sin horas»: usa la misma sesión (01) en el horario y en el docente",
        "Al crear un NRC nuevo, campus, estatus y tipo de horario son obligatorios",
        "Para pasar al bloque del docente usa «Sección siguiente»; el clic directo da error",
    ]}
    return flujo(
        c, 2, "crear-el-nrc",
        [{"id": "nrc", "label": "Programar el NRC"}],
        nodos,
        tarjetas(c, probado, [CITAS["periodo"], CITAS["catalogo"], CITAS["nrc"]],
                 [errores, tarjeta_terminos("NRC", "parte", "cupo")]),
        fases=[
            {"id": "f0", "label": "Antes", "fromCol": 0, "toCol": 1},
            {"id": "f1", "label": "SSASECT: tres guardados", "fromCol": 2, "toCol": 4, "variant": "emphasis"},
            {"id": "f2", "label": "Después", "fromCol": 5, "toCol": 5},
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
    """SHAGRDE → SHAGCOM → Autoservicio (docente) → SHRROLL → SMICRLT."""
    e = c.d["escala"]
    escala = f"nivel {c.nivel} · modo {e['modo']}" if e else f"nivel {c.nivel}: por confirmar"
    aprueba = f"aprueba con {e['nota_minima']}" if e else "nota mínima por confirmar"
    nodos = [
        paso("n1", "ra", 0, "SHAGRDE", "revisar la escala", escala),
        paso("n2", "ra", 1, "SHAGCOM", "plan de evaluación", "componentes y pesos"),
        paso("n3", "doc", 2, "Autoservicio", "registrar asistencia", "poca asistencia: INH", "frontend"),
        paso("n4", "doc", 3, "Autoservicio", "registrar notas", aprueba, "frontend"),
        paso("n5", "ra", 4, "SHRROLL", "pase a historia", "notas a la historia", "messagebus"),
        paso("n6", "ra", 5, "SMICRLT", "revisar el avance", "CAPP: cumple o no", "database"),
    ]
    probado = evidencia(c, ["13", "12", "14", "10"])
    leccion = {"dot": "rose", "title": "Si falla el pase a historia", "items": [
        "«No Substitute Grade»: la escala del nivel no tiene el modo del curso; agrégalo en SHAGRDE (U20)",
        "Con nota bajo el mínimo o INH, CAPP deja el curso «no usado» y el alumno lo repite (Script 10)",
    ]}
    return flujo(
        c, 6, "notas-y-pase-a-historia",
        [{"id": "ra", "label": "Registros Académicos"}, {"id": "doc", "label": "Docente"}],
        nodos,
        tarjetas(c, probado, [CITAS["escala"], CITAS["notas"], CITAS["cierre"], CITAS["capp"]],
                 [leccion, tarjeta_terminos("pase a historia", "alumno")]),
        fases=[
            {"id": "f0", "label": "Preparar", "fromCol": 0, "toCol": 1},
            {"id": "f1", "label": "Dictar", "fromCol": 2, "toCol": 3, "variant": "emphasis"},
            {"id": "f2", "label": "Cerrar", "fromCol": 4, "toCol": 5, "variant": "dashed"},
        ],
    )


# --------------------------------------------------------------------------- casuísticas
CASOS = {
    "01": (("Primera matrícula", "alumno admitido"),
           [("SFAREGS", "autorizar el plan · EL"), ("SFAREGS", "matricular en el NRC · RE")],
           ("Matriculado", "cupo real +1"), "matricula"),
    "03": (("Curso externo", "aprobado en otra institución"),
           [("SHATRNS", "registrar la institución"), ("SHATFAC", "registrar la nota"), ("SHRROLL", "pase a historia")],
           ("Convalidado", "CAPP lo cuenta"), "convalidacion"),
    "04": (("Ya sabe inglés", "quiere saltar BASIC I"),
           [("SOATEST", "registrar el puntaje"), ("SFAREGS", "matricular en BASIC II")],
           ("En BASIC II", "puntaje mínimo: U01"), "catalogo"),
    "08": (("Se retira", "antes de la fecha límite"),
           [("SFAREGS", "retirar con DD"), ("SSASECQ", "revisar el cupo")],
           ("Cupo libre", "cupo restante +1"), "matricula"),
    "09": (("Suspendido", "estatus IS o SU"),
           [("SFAREGS", "no deja matricular"), ("SGASTDN", "reactivar con AS")],
           ("Puede matricularse", "alumno activo"), "estudiante"),
    "10": (("Desaprueba", "nota bajo el mínimo"),
           [("SFASLST", "nota final"), ("SHRROLL", "pase a historia"), ("SMARQCM", "evaluar en CAPP")],
           ("Curso no usado", "repite el curso"), "capp"),
    "12": (("Fin del periodo", "notas finales listas"),
           [("SHAGRDE", "revisar el modo"), ("SHRROLL", "pase a historia")],
           ("En la historia", "Rolled to History"), "cierre"),
    "13": (("Notas del nivel", "notas finales del NRC"),
           [("SHAGRDE", "revisar la escala"), ("SFASLST", "registrar notas finales")],
           ("Aprueba o no", "según la nota mínima"), "notas"),
    "15": (("NRC lleno", "error «Closed»"),
           [("SSASECT", "subir el cupo"), ("SSARRES", "reservar para el programa")],
           ("Se matricula", "cupo ampliado"), "nrc"),
    "16": (("Cambio de NRC", "otro horario"),
           [("SFAREGS", "DD en el NRC de origen"), ("SFAREGS", "RE en el NRC de destino")],
           ("En el nuevo NRC", "lista actualizada"), "matricula"),
    "18-B": (("Tiene deuda", "cuota vencida"),
             [("SOAHOLD", "retención TT"), ("SFAREGS", "no deja matricular")],
             ("Sin matrícula", "hasta pagar"), "retencion"),
}


def caso(c, id_script):
    """Situación, pasos y resultado de un script, con los ajustes de cada centro."""
    if c.id == "idiomas" and id_script == "10":
        return (("Desaprueba BASIC I", "nota bajo el mínimo"),
                [("SHRROLL", "pase a historia"), ("SFAREGS", "BASIC II: error Fatal")],
                ("Repite BASIC I", "o rinde suficiencia"), "capp")
    if c.id == "emprendimiento" and id_script == "16":
        return (("Cambio de NRC", "P02 y P03 se cruzan"),
                [("SFAREGS", "DD en el NRC de origen"), ("SFAREGS", "RE en el NRC de destino")],
                ("En el nuevo NRC", "lista actualizada"), "matricula")
    sit, pasos, res, cita = CASOS[id_script]
    if id_script == "13" and c.d["escala"]:
        res = (res[0], f"aprueba con {c.d['escala']['nota_minima']}")
    return sit, pasos, res, cita


def casuistica(c, numero, id_script):
    (sit, sit_sub), pasos, (res, res_sub), cita = caso(c, id_script)
    s = c.script(id_script)
    nodos = [paso("c0", "caso", 0, sit, sit_sub, tipo="security", ancho=170)]
    for j, (codigo, accion) in enumerate(pasos, start=1):
        tipo = "messagebus" if codigo == "SHRROLL" else ("database" if codigo in ("SSASECQ", "SMARQCM") else "backend")
        nodos.append(paso(f"c{j}", "caso", j, codigo, accion, tipo=tipo, ancho=170))
    nodos.append(paso("cr", "caso", len(pasos) + 1, res, res_sub, ESTADO_TEXTO[s["estado"]], "database", "success", ancho=170))
    probado = [s["evidencia"]] if s["estado"] == "validado" else [f"{ESTADO_TEXTO[s['estado']].capitalize()}: {s['evidencia']}"]
    return flujo(
        c, numero, slug_script(id_script),
        [{"id": "caso", "label": "Situación → pasos → resultado"}],
        nodos,
        tarjetas(c, probado, [CITAS[cita]]),
    )


def casuisticas_de(c):
    ids = c.d["casuisticas"]["matricula"] + c.d["casuisticas"]["notas"]
    return [(7 + k, slug_script(i), lambda c, i=i, n=7 + k: casuistica(c, n, i)) for k, i in enumerate(ids)]


DIAGRAMAS_BASE = [
    (1, "recorrido-completo", recorrido),
    (2, "crear-el-nrc", crear_nrc),
    (3, "carga-lectiva", carga_lectiva),
    (4, "persona-y-admision", persona_admision),
    (5, "matricula-en-el-nrc", matricula),
    (6, "notas-y-pase-a-historia", notas),
]


def diagramas_de(c):
    """[(número, slug, función(c))]: los 6 flujos base y una casuística por diagrama."""
    return DIAGRAMAS_BASE + casuisticas_de(c)


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
        "title": f"Centros Empresariales · 0. {TITULOS['tres-centros']}",
        "subtitle": "Idiomas, Computación y Emprendimiento · Escuela EM · Campus S · Elaborado por: " + centros[0].autor,
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
