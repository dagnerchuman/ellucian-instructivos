"""Índices generados a partir de datos.json y de los diagramas que existen en disco:

- centros/README.md          índice de todos los diagramas (para GitHub)
- centros/index.html         galería para abrir en el navegador o en Netlify (/centros/)
- centros/<centro>/README.md ficha del centro: códigos, grupos, scripts, dudas y diagramas
"""
import html
from pathlib import Path

from centro import CENTROS, POR_CONFIRMAR, Centro, centros_disponibles
from plantillas import TITULOS, CAPACIDADES, FASES_CASUISTICAS, slug_script
ASSETS_DIR = Path(__file__).resolve().parent / "assets"
TEMPLATE_GALERIA = (ASSETS_DIR / "indice_galeria.html").read_text(encoding="utf-8")
CSS_GALERIA = (ASSETS_DIR / "indice_galeria.css").read_text(encoding="utf-8")
JS_GALERIA = (ASSETS_DIR / "indice_galeria.js").read_text(encoding="utf-8")
CSS_AI = (ASSETS_DIR / "asistente_ia.css").read_text(encoding="utf-8")
JS_AI = (ASSETS_DIR / "asistente_ia.js").read_text(encoding="utf-8")
HTML_AI = (ASSETS_DIR / "asistente_ia_snippet.html").read_text(encoding="utf-8")
CSS_ZOOM = (ASSETS_DIR / "zoom_imagen.css").read_text(encoding="utf-8")
JS_ZOOM = (ASSETS_DIR / "zoom_imagen.js").read_text(encoding="utf-8")
SCRIPT_CONOCIMIENTO_AI = ('<script src="../herramientas/diagramas/assets/asistente_conocimiento.js"></script>\n'
                          '  <script src="../herramientas/diagramas/assets/asistente_diapositivas.js"></script>')

AVISO = "<!-- Archivo generado por herramientas/diagramas/generar.py: no lo edites a mano. -->"


def diagramas_de(carpeta):
    """[(numero, titulo, capacidad, base)] de cada subcarpeta NN-tema con su HTML; base = ruta sin extensión."""
    salida = []
    for sub in sorted((carpeta / "diagramas").glob("[0-9][0-9]-*")):
        html_ = next(sub.glob("*.html"), None)
        if not html_:
            continue
        numero = int(sub.name[:2])
        slug_ = sub.name[3:]
        titulo = TITULOS.get(slug_, slug_.replace("-", " ").capitalize())
        cap = CAPACIDADES.get(slug_, "")
        salida.append((numero, titulo, cap, html_.with_suffix("")))
    return salida


FASE_BASE = "Flujos base"
FASE_DEMO = "Demostraciones para la reunión"


def fases_de(carpeta, centro_id=None):
    """[(fase, [diagramas])] en el orden del proceso: flujos base, abrir el periodo, matrícula, notas y cierre."""
    diags = diagramas_de(carpeta)
    if not centro_id or centro_id == "comun":
        return [(None, diags)]
    c = Centro(centro_id)
    fase_por_slug = {slug_script(i): nombre for clave, nombre in FASES_CASUISTICAS
                     for i in c.d["casuisticas"].get(clave, [])}
    grupos = {}
    for item in diags:
        slug_ = item[3].parent.name[3:]
        fase = FASE_DEMO if slug_.startswith("demostracion-") else fase_por_slug.get(slug_, FASE_BASE)
        grupos.setdefault(fase, []).append(item)
    orden = [FASE_DEMO, FASE_BASE] + [nombre for _, nombre in FASES_CASUISTICAS]
    return [(f, grupos[f]) for f in orden if f in grupos]


def rel(ruta, desde):
    return ruta.relative_to(desde).as_posix()


def enlaces_md(base, desde):
    b = rel(base, desde)
    partes = [f"[HTML]({b}.html)"]
    if (base.parent / f"{base.name}-claro.png").exists():
        partes.append(f"[PNG claro]({b}-claro.png)")
    if (base.parent / f"{base.name}-oscuro.png").exists():
        partes.append(f"[PNG oscuro]({b}-oscuro.png)")
    if (base.parent / f"{base.name}.svg").exists():
        partes.append(f"[SVG]({b}.svg)")
    return " · ".join(partes)


def tabla_diagramas(carpeta, desde, centro_id=None):
    filas = ["| N.º | Fase | Capacidad Banner | Diagrama | Archivos |", "|---|---|---|---|---|"]
    for fase, diags in fases_de(carpeta, centro_id):
        for numero, titulo, cap, base in diags:
            cap_txt = cap if cap else "General"
            filas.append(f"| {numero} | {fase or 'Comparativo'} | {cap_txt} | {titulo} | {enlaces_md(base, desde)} |")
    return "\n".join(filas)


def readme_general(ids):
    partes = [
        AVISO,
        "# Centros Empresariales: diagramas paso a paso",
        "",
        "Diagramas interactivos de cómo trabaja cada centro en Ellucian Banner, hechos con "
        "[Archify](https://github.com/tt-a1i/archify).",
        "",
        "**Cada diagrama tiene cinco archivos:**",
        "- **HTML** interactivo: modo claro u oscuro, animación, vistas guiadas, búsqueda y menú «Exportar». "
        "Ábrelo con doble clic, o desde Netlify en `/centros/` cuando esté en `main`.",
        "- **PNG claro** y **PNG oscuro**, en alta resolución, para documentos y presentaciones.",
        "- **SVG** vectorial: cambia solo entre claro y oscuro.",
        "- **`.json`**: la especificación que se compiló. No se edita a mano; ver `herramientas/diagramas`.",
        "",
        "La galería con todos los diagramas está en [`index.html`](index.html).",
        "",
        "## Comparativo de los tres centros",
        tabla_diagramas(CENTROS / "comun", CENTROS),
    ]
    for i in ids:
        c = Centro(i)
        partes += ["", f"## {c.nombre}", f"Ficha del centro: [`{i}/README.md`]({i}/README.md) · datos: [`{i}/datos.json`]({i}/datos.json)", "",
                   tabla_diagramas(CENTROS / i, CENTROS, i)]
    partes += ["", "## Cómo regenerarlos", "```bash",
               "bash herramientas/diagramas/instalar_archify.sh",
               "python3 herramientas/diagramas/generar.py", "```",
               "Detalle en la skill `workflow-diagramas-archify`.", ""]
    (CENTROS / "README.md").write_text("\n".join(partes), encoding="utf-8")


def ficha_centro(c):
    d = c.d
    carpeta = CENTROS / c.id
    comun = c.comun

    def fila(concepto, valor, nota=""):
        return f"| {concepto} | {valor} | {nota} |"

    ids_tabla = [
        "| Concepto | Código | Nota |", "|---|---|---|",
        fila("Nivel (STVLEVL)", f"`{c.nivel}`", d["nivel"]["nombre"]),
        fila("Escuela", f"`{comun['escuela']['codigo']}`", comun["escuela"]["nombre"]),
        fila("Campus", f"`{comun['campus']['codigo']}`", comun["campus"]["nombre"]),
        fila("Grado", f"`{comun['grado']['codigo']}`", comun["grado"]["nombre"]),
        fila("Programa", f"`{c.programa}`" if d["programa"] else POR_CONFIRMAR, (d["programa"] or {}).get("nombre", "")),
        fila("Mayor", f"`{c.mayor}`" if d["mayor"] else POR_CONFIRMAR, (d["mayor"] or {}).get("nombre", "")),
        fila("Departamento", f"`{c.departamento}`" if d["departamento"] else POR_CONFIRMAR, (d["departamento"] or {}).get("nombre", "")),
        fila("Materia", f"`{c.materia}`" if d["materia"] else POR_CONFIRMAR, (d["materia"] or {}).get("nombre", "")),
        fila("Escala de notas", c.escala, (d["escala"] or {}).get("fuente", "")),
        fila("Parte general", f"`{d['parte_general']}`", f"grupos {c.partes} en 2026"),
    ]
    grupos = ["| Grupo | Periodo | Fechas | Semanas |", "|---|---|---|---|"]
    for p in d["partes_2026"]:
        extra = f" (nivel III: {p['nivel_iii']})" if p.get("nivel_iii") else ""
        grupos.append(f"| {p['codigo']} | {p['periodo']} | {p['fechas']}{extra} | {p['semanas']} |")
    conteo = {}
    for s in d["scripts"].values():
        conteo[s["estado"]] = conteo.get(s["estado"], 0) + 1
    resumen = " · ".join(f"{v} {k}" for k, v in sorted(conteo.items(), key=lambda kv: -kv[1]))
    scripts = ["| Script | Nombre | Estado | Evidencia o pendiente |", "|---|---|---|---|"]
    for s in comun["scripts"]:
        e = d["scripts"][s["id"]]
        scripts.append(f"| {s['id']} | {s['nombre']} | {e['estado']} | {e['evidencia']} |")
    nrcs = [f"- NRC **{n['nrc']}**: {n['curso']}, sección {n['seccion']}" + (f", parte {n['parte']}" if n.get("parte") else "")
            + f". {n['uso']}." for n in d["nrc_test"]] or ["- Todavía no hay NRC de este centro en TEST."]
    partes = [
        AVISO,
        f"# {c.nombre}" + (f" ({d['alias']})" if d.get("alias") else ""),
        "",
        "Ficha generada desde [`datos.json`](datos.json), que es la fuente única de los datos de este centro. "
        f"Lo marcado «{POR_CONFIRMAR}» todavía no se verificó en TEST.",
        "",
        *([f"**Guía de pruebas en TEST:** [`pruebas-test.md`](pruebas-test.md)", ""] if (carpeta / "pruebas-test.md").exists() else []),
        "## Diagramas paso a paso",
        tabla_diagramas(carpeta, carpeta, c.id),
        "",
        "## Códigos en Banner",
        *ids_tabla,
        "",
        "## Lo propio de este centro",
        *[f"- {x}" for x in d["particularidades"]],
        "",
        f"## Grupos 2026 ({d['duracion']})",
        *grupos,
        "",
        "## NRC en TEST",
        *nrcs,
        "",
        f"## Scripts de prueba ({resumen})",
        *scripts,
        "",
        "## Por confirmar",
        *[f"- **{x['id']}**: {x['texto']}" for x in d["dudas"]],
        "",
    ]
    (carpeta / "README.md").write_text("\n".join(partes), encoding="utf-8")


def galeria(ids):
    def tarjeta(numero, titulo, cap, base, centro_id):
        b = html.escape(rel(base, CENTROS))
        cap_badge = f'<span class="cap">{html.escape(cap)}</span>' if cap else ""
        return (
            f'<article class="card" data-center="{html.escape(centro_id)}" data-title="{html.escape(titulo.lower())}" data-cap="{html.escape(cap.lower())}" data-num="{numero}">'
            f'<a class="thumb" href="{b}.html" title="Abrir diagrama interactivo"><img loading="lazy" src="{b}.svg" alt="{html.escape(titulo)}"></a>'
            f'<div class="meta"><span class="num">{numero}</span>{cap_badge}<a href="{b}.html" class="title-link">{html.escape(titulo)}</a></div>'
            f'<div class="files"><a href="{b}.html" class="file-btn primary">HTML interactivo</a><a href="{b}-claro.png" class="file-btn">PNG claro</a>'
            f'<a href="{b}-oscuro.png" class="file-btn">PNG oscuro</a><a href="{b}.svg" class="file-btn">SVG</a></div></article>')

    def tarjetas(carpeta, centro_id):
        bloques = []
        for fase, diags in fases_de(carpeta, centro_id):
            grid = '<div class="grid">' + "\n".join(tarjeta(*d, centro_id) for d in diags) + '</div>'
            if fase is None:
                bloques.append(grid)
            else:
                n = len(diags)
                bloques.append(
                    f'<div class="phase-group"><h3 class="phase-title">{html.escape(fase)}'
                    f'<span class="phase-count">{n} {"diagrama" if n == 1 else "diagramas"}</span></h3>{grid}</div>')
        return "\n".join(bloques)

    secciones = [
        f'<section class="center-section" id="sec-comun" data-center="comun" style="--c:#5C2193">'
        f'<div class="sec-header"><h2>Los tres centros</h2><span class="sec-badge">Transversal</span></div>'
        f'{tarjetas(CENTROS / "comun", "comun")}</section>'
    ]
    for i in ids:
        c = Centro(i)
        secciones.append(
            f'<section class="center-section" id="sec-{i}" data-center="{i}" style="--c:{c.d["color"]}">'
            f'<div class="sec-header"><div><h2>{html.escape(c.nombre)}</h2>'
            f'<p class="sub">{html.escape(c.subtitulo())} · <a href="{i}/README.md">ficha técnica</a></p></div>'
            f'<span class="sec-badge">{c.nivel} · {c.materia or "General"}</span></div>'
            f'{tarjetas(CENTROS / i, i)}</section>'
        )

    autor = html.escape(Centro(ids[0]).autor)
    test = Centro(ids[0]).comun["ambiente_test"]
    url_test = html.escape(test if test.startswith("http") else "https://" + test)
    pagina = (
        TEMPLATE_GALERIA
        .replace("/*__CSS__*/", CSS_GALERIA + "\n\n" + CSS_AI + "\n\n" + CSS_ZOOM)
        .replace("/*__JS__*/", JS_ZOOM + "\n\n" + JS_GALERIA + "\n\n" + JS_AI)
        .replace("<!--__KNOWLEDGE_SCRIPT__-->", SCRIPT_CONOCIMIENTO_AI)
        .replace("{autor}", autor)
        .replace("{url_test}", url_test)
        .replace("{secciones}", "\n".join(secciones))
        .replace("{asistente_ia_html}", HTML_AI)
    )
    (CENTROS / "index.html").write_text(pagina, encoding="utf-8")

def generar_indices():
    ids = centros_disponibles()
    for i in ids:
        ficha_centro(Centro(i))
    readme_general(ids)
    galeria(ids)
    return [CENTROS / "README.md", CENTROS / "index.html", *[CENTROS / i / "README.md" for i in ids]]
