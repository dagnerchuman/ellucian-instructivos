"""Índices generados a partir de datos.json y de los diagramas que existen en disco:

- centros/README.md          índice de todos los diagramas (para GitHub)
- centros/index.html         galería para abrir en el navegador o en Netlify (/centros/)
- centros/<centro>/README.md ficha del centro: códigos, grupos, scripts, dudas y diagramas
"""
import html
from pathlib import Path

from centro import CENTROS, POR_CONFIRMAR, Centro, centros_disponibles
from plantillas import TITULOS

AVISO = "<!-- Archivo generado por herramientas/diagramas/generar.py: no lo edites a mano. -->"


def diagramas_de(carpeta):
    """[(numero, titulo, base)] de cada subcarpeta NN-tema con su HTML; base = ruta sin extensión."""
    salida = []
    for sub in sorted((carpeta / "diagramas").glob("[0-9][0-9]-*")):
        html_ = next(sub.glob("*.html"), None)
        if not html_:
            continue
        numero = int(sub.name[:2])
        titulo = TITULOS.get(sub.name[3:], sub.name[3:].replace("-", " ").capitalize())
        salida.append((numero, titulo, html_.with_suffix("")))
    return salida


def rel(ruta, desde):
    return ruta.relative_to(desde).as_posix()


def enlaces_md(base, desde):
    b = rel(base, desde)
    return f"[HTML]({b}.html) · [PNG claro]({b}-claro.png) · [PNG oscuro]({b}-oscuro.png) · [SVG]({b}.svg)"


def tabla_diagramas(carpeta, desde):
    filas = ["| N.º | Diagrama | Archivos |", "|---|---|---|"]
    for numero, titulo, base in diagramas_de(carpeta):
        filas.append(f"| {numero} | {titulo} | {enlaces_md(base, desde)} |")
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
                   tabla_diagramas(CENTROS / i, CENTROS)]
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
        "## Diagramas paso a paso",
        tabla_diagramas(carpeta, carpeta),
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
        f"## Los 18 scripts ({resumen})",
        *scripts,
        "",
        "## Por confirmar",
        *[f"- **{x['id']}**: {x['texto']}" for x in d["dudas"]],
        "",
    ]
    (carpeta / "README.md").write_text("\n".join(partes), encoding="utf-8")


def galeria(ids):
    def tarjetas(carpeta):
        t = []
        for numero, titulo, base in diagramas_de(carpeta):
            b = html.escape(rel(base, CENTROS))
            t.append(
                f'<article class="card"><a class="thumb" href="{b}.html"><img loading="lazy" src="{b}.svg" alt="{html.escape(titulo)}"></a>'
                f'<div class="meta"><span class="num">{numero}</span><a href="{b}.html">{html.escape(titulo)}</a></div>'
                f'<div class="files"><a href="{b}.html">HTML</a><a href="{b}-claro.png">PNG claro</a>'
                f'<a href="{b}-oscuro.png">PNG oscuro</a><a href="{b}.svg">SVG</a></div></article>')
        return "\n".join(t)

    secciones = [f'<section style="--c:#5C2193"><h2>Los tres centros</h2><div class="grid">{tarjetas(CENTROS / "comun")}</div></section>']
    for i in ids:
        c = Centro(i)
        secciones.append(
            f'<section style="--c:{c.d["color"]}"><h2>{html.escape(c.nombre)}</h2>'
            f'<p class="sub">{html.escape(c.subtitulo())} · <a href="{i}/README.md">ficha</a></p>'
            f'<div class="grid">{tarjetas(CENTROS / i)}</div></section>')
    autor = html.escape(Centro(ids[0]).autor)
    pagina = f"""<!DOCTYPE html>
{AVISO}
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Diagramas de los Centros Empresariales</title>
<style>
:root {{ --bg:#f6f4fa; --fg:#1d1530; --muted:#5d5670; --card:#fff; --line:#e3ddef; --brand:#7030A0; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#120d1c; --fg:#f1edf8; --muted:#b4abc7; --card:#1c1529; --line:#2f2642; --brand:#b98ae0; }} }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif; }}
header {{ padding:28px 16px 8px; max-width:1200px; margin:auto; }}
h1 {{ margin:0; font-size:26px; color:var(--brand); }}
header p {{ margin:6px 0 0; color:var(--muted); }}
main {{ max-width:1200px; margin:auto; padding:0 16px 40px; }}
section {{ margin-top:28px; border-top:4px solid var(--c); padding-top:12px; }}
h2 {{ margin:0; font-size:20px; color:var(--c); }}
.sub {{ margin:4px 0 0; color:var(--muted); font-size:13px; }}
a {{ color:inherit; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:14px; margin-top:14px; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:12px; overflow:hidden; display:flex; flex-direction:column; }}
.thumb {{ display:block; aspect-ratio:16/10; overflow:hidden; background:#fff; border-bottom:1px solid var(--line); }}
.thumb img {{ display:block; width:100%; height:100%; object-fit:contain; }}
.meta {{ display:flex; gap:8px; align-items:center; padding:10px 12px 4px; font-weight:600; }}
.meta a {{ text-decoration:none; }}
.num {{ background:var(--c); color:#fff; border-radius:6px; padding:0 7px; font-size:13px; }}
.files {{ display:flex; flex-wrap:wrap; gap:6px 12px; padding:4px 12px 12px; font-size:13px; color:var(--muted); }}
</style></head><body>
<header><h1>Centros Empresariales en Banner: diagramas paso a paso</h1>
<p>Idiomas, Computación y Emprendimiento · Universidad Señor de Sipán · Elaborado por: {autor}</p></header>
<main>
{chr(10).join(secciones)}
</main></body></html>
"""
    (CENTROS / "index.html").write_text(pagina, encoding="utf-8")


def generar_indices():
    ids = centros_disponibles()
    for i in ids:
        ficha_centro(Centro(i))
    readme_general(ids)
    galeria(ids)
    return [CENTROS / "README.md", CENTROS / "index.html", *[CENTROS / i / "README.md" for i in ids]]
