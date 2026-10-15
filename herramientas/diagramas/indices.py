"""Índices generados a partir de datos.json y de los diagramas que existen en disco:

- centros/README.md          índice de todos los diagramas (para GitHub)
- centros/index.html         galería para abrir en el navegador o en Netlify (/centros/)
- centros/<centro>/README.md ficha del centro: códigos, grupos, scripts, dudas y diagramas
"""
import html
from pathlib import Path

from centro import CENTROS, POR_CONFIRMAR, Centro, centros_disponibles
from plantillas import TITULOS, CAPACIDADES

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


def rel(ruta, desde):
    return ruta.relative_to(desde).as_posix()


def enlaces_md(base, desde):
    b = rel(base, desde)
    return f"[HTML]({b}.html) · [PNG claro]({b}-claro.png) · [PNG oscuro]({b}-oscuro.png) · [SVG]({b}.svg)"


def tabla_diagramas(carpeta, desde):
    filas = ["| N.º | Capacidad Banner | Diagrama | Archivos |", "|---|---|---|---|"]
    for numero, titulo, cap, base in diagramas_de(carpeta):
        cap_txt = cap if cap else "General"
        filas.append(f"| {numero} | {cap_txt} | {titulo} | {enlaces_md(base, desde)} |")
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
        *([f"**Guía de pruebas en TEST:** [`pruebas-test.md`](pruebas-test.md)", ""] if (carpeta / "pruebas-test.md").exists() else []),
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
        f"## Scripts de prueba ({resumen})",
        *scripts,
        "",
        "## Por confirmar",
        *[f"- **{x['id']}**: {x['texto']}" for x in d["dudas"]],
        "",
    ]
    (carpeta / "README.md").write_text("\n".join(partes), encoding="utf-8")


def galeria(ids):
    def tarjetas(carpeta, centro_id):
        t = []
        for numero, titulo, cap, base in diagramas_de(carpeta):
            b = html.escape(rel(base, CENTROS))
            cap_badge = f'<span class="cap">{html.escape(cap)}</span>' if cap else ""
            t.append(
                f'<article class="card" data-center="{html.escape(centro_id)}" data-title="{html.escape(titulo.lower())}" data-cap="{html.escape(cap.lower())}" data-num="{numero}">'
                f'<a class="thumb" href="{b}.html" title="Abrir diagrama interactivo"><img loading="lazy" src="{b}.svg" alt="{html.escape(titulo)}"></a>'
                f'<div class="meta"><span class="num">{numero}</span>{cap_badge}<a href="{b}.html" class="title-link">{html.escape(titulo)}</a></div>'
                f'<div class="files"><a href="{b}.html" class="file-btn primary">HTML interactivo</a><a href="{b}-claro.png" class="file-btn">PNG claro</a>'
                f'<a href="{b}-oscuro.png" class="file-btn">PNG oscuro</a><a href="{b}.svg" class="file-btn">SVG</a></div></article>')
        return "\n".join(t)

    secciones = [
        f'<section class="center-section" id="sec-comun" data-center="comun" style="--c:#5C2193">'
        f'<div class="sec-header"><h2>Los tres centros</h2><span class="sec-badge">Transversal</span></div>'
        f'<div class="grid">{tarjetas(CENTROS / "comun", "comun")}</div></section>'
    ]
    for i in ids:
        c = Centro(i)
        secciones.append(
            f'<section class="center-section" id="sec-{i}" data-center="{i}" style="--c:{c.d["color"]}">'
            f'<div class="sec-header"><div><h2>{html.escape(c.nombre)}</h2>'
            f'<p class="sub">{html.escape(c.subtitulo())} · <a href="{i}/README.md">ficha técnica</a></p></div>'
            f'<span class="sec-badge">{c.nivel} · {c.materia or "General"}</span></div>'
            f'<div class="grid">{tarjetas(CENTROS / i, i)}</div></section>'
        )
    autor = html.escape(Centro(ids[0]).autor)
    pagina = f"""<!DOCTYPE html>
{AVISO}
<html lang="es" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Diagramas de los Centros Empresariales · USS en Banner</title>
<script>
  (function () {{
    try {{
      var t = localStorage.getItem('archify-theme');
      if (!t) t = window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', t);
    }} catch (_) {{}}
  }})();
</script>
<style>
:root, [data-theme="dark"] {{
  --bg: #0b0813;
  --bg-card: #151022;
  --bg-card-hover: #1c152d;
  --fg: #f3f0f9;
  --muted: #a39bb8;
  --line: #29203d;
  --brand: #b98ae0;
  --brand-solid: #7030A0;
  --thumb-bg: #090610;
  --input-bg: #1c152b;
  --btn-bg: #231b36;
  --btn-hover: #32264d;
  --header-bg: rgba(11, 8, 19, 0.85);
}}

[data-theme="light"] {{
  --bg: #f8f6fb;
  --bg-card: #ffffff;
  --bg-card-hover: #ffffff;
  --fg: #1a1426;
  --muted: #645b7a;
  --line: #e4ddf0;
  --brand: #7030A0;
  --brand-solid: #7030A0;
  --thumb-bg: #fcfbfe;
  --input-bg: #ffffff;
  --btn-bg: #f0ecf7;
  --btn-hover: #e3dced;
  --header-bg: rgba(248, 246, 251, 0.9);
}}

* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  background: var(--bg);
  color: var(--fg);
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}}

/* Header Principal Responsivo */
.top-header {{
  position: sticky;
  top: 0;
  z-index: 40;
  background: var(--header-bg);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--line);
  padding: 1rem 1.25rem 0.85rem;
}}

.header-container {{
  max-width: 1400px;
  margin: 0 auto;
}}

.header-main-row {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 0.75rem 1rem;
}}

.title-wrap {{
  flex: 1 1 20rem;
  min-width: 0;
}}

h1 {{
  margin: 0;
  font-size: clamp(1.2rem, 2.5vw, 1.75rem);
  font-weight: 800;
  color: var(--brand);
  letter-spacing: -0.01em;
}}

.header-sub {{
  margin: 0.35rem 0 0;
  color: var(--muted);
  font-size: clamp(0.75rem, 1.3vw, 0.875rem);
  line-height: 1.45;
}}

.header-actions {{
  display: flex;
  align-items: center;
  gap: 0.5rem;
}}

.theme-toggle-btn {{
  background: var(--btn-bg);
  border: 1px solid var(--line);
  color: var(--fg);
  border-radius: 0.5rem;
  padding: 0.45rem 0.85rem;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  transition: all 0.15s ease;
}}
.theme-toggle-btn:hover {{
  background: var(--btn-hover);
  border-color: var(--brand);
}}

/* Barra de Filtros y Búsqueda */
.controls-bar {{
  margin-top: 0.85rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem 1rem;
  align-items: center;
  justify-content: space-between;
}}

.filter-chips {{
  display: flex;
  gap: 0.4rem;
  overflow-x: auto;
  padding-bottom: 0.25rem;
  scrollbar-width: thin;
  max-width: 100%;
}}

.filter-chip {{
  background: var(--btn-bg);
  border: 1px solid var(--line);
  color: var(--muted);
  border-radius: 999px;
  padding: 0.35rem 0.8rem;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s ease;
  user-select: none;
}}
.filter-chip:hover {{
  color: var(--fg);
  border-color: var(--brand);
}}
.filter-chip.active {{
  background: var(--brand-solid);
  color: #ffffff;
  border-color: var(--brand-solid);
}}

.search-box {{
  position: relative;
  flex: 1 1 16rem;
  max-width: 26rem;
}}
.search-input {{
  width: 100%;
  background: var(--input-bg);
  border: 1px solid var(--line);
  color: var(--fg);
  border-radius: 0.55rem;
  padding: 0.45rem 0.85rem 0.45rem 2.2rem;
  font-size: 0.8125rem;
  outline: none;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}}
.search-input:focus {{
  border-color: var(--brand);
  box-shadow: 0 0 0 3px rgba(112, 48, 160, 0.2);
}}
.search-icon {{
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--muted);
  pointer-events: none;
  font-size: 0.85rem;
}}

/* Contenido Principal y Secciones */
main {{
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.25rem 1.25rem 4rem;
}}

.center-section {{
  margin-top: 2rem;
  border-top: 3px solid var(--c);
  padding-top: 1.25rem;
}}
.center-section.hidden {{
  display: none !important;
}}

.sec-header {{
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 0.5rem 1rem;
  margin-bottom: 1rem;
}}
.sec-header h2 {{
  margin: 0;
  font-size: clamp(1.1rem, 2vw, 1.45rem);
  font-weight: 700;
  color: var(--c);
}}
.sec-header .sub {{
  margin: 0.25rem 0 0;
  color: var(--muted);
  font-size: 0.8125rem;
}}
.sec-header .sub a {{
  color: var(--c);
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 2px;
}}
.sec-badge {{
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.2rem 0.55rem;
  border-radius: 0.4rem;
  background: color-mix(in srgb, var(--c) 15%, transparent);
  color: var(--c);
  border: 1px solid color-mix(in srgb, var(--c) 30%, transparent);
}}

/* Cuadrícula de Tarjetas Responsiva */
.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(285px, 100%), 1fr));
  gap: 1.15rem;
}}

.card {{
  background: var(--bg-card);
  border: 1px solid var(--line);
  border-radius: 0.85rem;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease, border-color 0.2s ease;
}}
.card:hover {{
  transform: translateY(-3px);
  border-color: color-mix(in srgb, var(--c) 65%, var(--line));
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.22);
}}
.card.hidden {{
  display: none !important;
}}

.thumb {{
  display: block;
  aspect-ratio: 16 / 10;
  overflow: hidden;
  background: var(--thumb-bg);
  border-bottom: 1px solid var(--line);
  position: relative;
}}
.thumb img {{
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.25s ease;
}}
.card:hover .thumb img {{
  transform: scale(1.025);
}}

.meta {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem 0.65rem;
  align-items: center;
  padding: 0.85rem 1rem 0.4rem;
}}

.num {{
  background: var(--c);
  color: #ffffff;
  border-radius: 0.4rem;
  padding: 0.1rem 0.55rem;
  font-size: 0.75rem;
  font-weight: 700;
}}

.cap {{
  background: color-mix(in srgb, var(--c) 14%, transparent);
  color: var(--c);
  border: 1px solid color-mix(in srgb, var(--c) 28%, transparent);
  border-radius: 0.4rem;
  padding: 0.1rem 0.5rem;
  font-size: 0.6875rem;
  font-weight: 700;
  white-space: nowrap;
}}

.title-link {{
  text-decoration: none;
  color: var(--fg);
  font-size: 0.875rem;
  font-weight: 600;
  line-height: 1.35;
  width: 100%;
  margin-top: 0.2rem;
  transition: color 0.15s ease;
}}
.title-link:hover {{
  color: var(--brand);
  text-decoration: underline;
}}

.files {{
  margin-top: auto;
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem 0.55rem;
  padding: 0.6rem 1rem 0.9rem;
  border-top: 1px solid color-mix(in srgb, var(--line) 60%, transparent);
}}

.file-btn {{
  text-decoration: none;
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--muted);
  background: var(--btn-bg);
  border: 1px solid var(--line);
  padding: 0.25rem 0.6rem;
  border-radius: 0.4rem;
  transition: all 0.15s ease;
}}
.file-btn:hover {{
  color: var(--fg);
  background: var(--btn-hover);
  border-color: var(--brand);
}}
.file-btn.primary {{
  background: color-mix(in srgb, var(--brand-solid) 20%, transparent);
  color: var(--brand);
  border-color: color-mix(in srgb, var(--brand-solid) 40%, transparent);
}}
.file-btn.primary:hover {{
  background: var(--brand-solid);
  color: #ffffff;
}}

#no-results {{
  display: none;
  text-align: center;
  padding: 3rem 1rem;
  color: var(--muted);
}}
#no-results.visible {{
  display: block;
}}
</style>
</head>
<body>

<header class="top-header">
  <div class="header-container">
    <div class="header-main-row">
      <div class="title-wrap">
        <h1>Centros Empresariales en Banner: diagramas paso a paso</h1>
        <p class="header-sub">Idiomas, Computación y Emprendimiento · Universidad Señor de Sipán · Elaborado por: {autor}</p>
      </div>
      <div class="header-actions">
        <button type="button" class="theme-toggle-btn" id="theme-toggle" title="Alternar tema claro/oscuro">
          <span id="theme-icon">🌓</span> <span id="theme-txt">Tema</span>
        </button>
      </div>
    </div>

    <div class="controls-bar">
      <div class="filter-chips" role="tablist" aria-label="Filtrar por centro">
        <button type="button" class="filter-chip active" data-filter="all">Todos (45)</button>
        <button type="button" class="filter-chip" data-filter="comun">Los tres centros (1)</button>
        <button type="button" class="filter-chip" data-filter="idiomas">Idiomas (16)</button>
        <button type="button" class="filter-chip" data-filter="computacion">Computación (14)</button>
        <button type="button" class="filter-chip" data-filter="emprendimiento">Emprendimiento (14)</button>
      </div>

      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="search" class="search-input" id="search-input" placeholder="Buscar por título, número, capacidad..." autocomplete="off">
      </div>
    </div>
  </div>
</header>

<main>
  <div id="no-results">
    <h3>No se encontraron diagramas coincidentes</h3>
    <p>Prueba con otros términos de búsqueda o selecciona otro centro.</p>
  </div>
  {chr(10).join(secciones)}
</main>

<script>
(function() {{
  var themeBtn = document.getElementById('theme-toggle');
  var searchInput = document.getElementById('search-input');
  var chips = document.querySelectorAll('.filter-chip');
  var cards = document.querySelectorAll('.card');
  var sections = document.querySelectorAll('.center-section');
  var noResults = document.getElementById('no-results');

  // Alternar tema
  themeBtn.addEventListener('click', function() {{
    var cur = document.documentElement.getAttribute('data-theme') || 'dark';
    var next = cur === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try {{ localStorage.setItem('archify-theme', next); }} catch (_) {{}}
  }});

  var currentFilter = 'all';

  function aplicarFiltros() {{
    var q = (searchInput.value || '').trim().toLowerCase();
    var visibleTotal = 0;

    sections.forEach(function(sec) {{
      var centerId = sec.getAttribute('data-center');
      var secMatchesCenter = (currentFilter === 'all' || currentFilter === centerId);
      var visibleInSec = 0;

      var secCards = sec.querySelectorAll('.card');
      secCards.forEach(function(c) {{
        var title = c.getAttribute('data-title') || '';
        var cap = c.getAttribute('data-cap') || '';
        var num = c.getAttribute('data-num') || '';
        var matchesSearch = !q || title.indexOf(q) !== -1 || cap.indexOf(q) !== -1 || num === q;

        if (secMatchesCenter && matchesSearch) {{
          c.classList.remove('hidden');
          visibleInSec++;
          visibleTotal++;
        }} else {{
          c.classList.add('hidden');
        }}
      }});

      if (visibleInSec === 0) {{
        sec.classList.add('hidden');
      }} else {{
        sec.classList.remove('hidden');
      }}
    }});

    if (visibleTotal === 0) {{
      noResults.classList.add('visible');
    }} else {{
      noResults.classList.remove('visible');
    }}
  }}

  function setFilter(filterId, updateUrl) {{
    currentFilter = filterId || 'all';
    chips.forEach(function(c) {{
      if (c.getAttribute('data-filter') === currentFilter) {{
        c.classList.add('active');
      }} else {{
        c.classList.remove('active');
      }}
    }});
    aplicarFiltros();
    if (updateUrl) {{
      var newHash = (currentFilter === 'all') ? '' : '#sec-' + currentFilter;
      if (window.location.hash !== newHash) {{
        if (history.replaceState) {{
          history.replaceState(null, '', window.location.pathname + (newHash ? newHash : ''));
        }} else {{
          window.location.hash = newHash;
        }}
      }}
    }}
  }}

  function leerHash() {{
    var h = (window.location.hash || '').replace('#', '');
    if (h) {{
      var targetCenter = h.replace('sec-', '');
      var matchingChip = document.querySelector('.filter-chip[data-filter="' + targetCenter + '"]');
      if (matchingChip) {{
        setFilter(targetCenter, false);
        return;
      }}
    }}
    setFilter('all', false);
  }}

  chips.forEach(function(chip) {{
    chip.addEventListener('click', function() {{
      var f = chip.getAttribute('data-filter') || 'all';
      setFilter(f, true);
    }});
  }});

  searchInput.addEventListener('input', aplicarFiltros);
  window.addEventListener('hashchange', leerHash);
  leerHash();
}})();
</script>
</body>
</html>
"""
    (CENTROS / "index.html").write_text(pagina, encoding="utf-8")



def generar_indices():
    ids = centros_disponibles()
    for i in ids:
        ficha_centro(Centro(i))
    readme_general(ids)
    galeria(ids)
    return [CENTROS / "README.md", CENTROS / "index.html", *[CENTROS / i / "README.md" for i in ids]]
