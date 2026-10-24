"""Inyecta guías operativas interactivas directamente en el modal (Pasaporte semántico) de los diagramas Archify.

Al hacer clic sobre cualquier nodo del flujo en el navegador, el contenedor 
despliega la ficha operativa completa en Vista Dividida (Flujo BPM arriba + Guía abajo al 100% de ancho)
o en modo flotante/lateral, manteniendo siempre visible y responsivo el diagrama BPM.
"""
# ======================= BLOQUE 1: imports y constantes (reemplaza las 5 primeras líneas de import) =======================
import html
import json
import os
import re
from pathlib import Path
import sys
from guias_operativas import obtener_guia, GUIAS_BASE, GUIAS_SCRIPTS, INSTRUCTIVOS
from plantillas import TITULOS, CAPACIDADES, guia_casuistica_de

# "plantillas": la guía de las casuísticas sale de plantillas.py (CASOS + EXTRA_CASOS) y pisa a GUIAS_SCRIPTS.
# "curada": manda GUIAS_SCRIPTS y solo se generan los nodos que le falten.
PRIORIDAD_CASUISTICAS = "plantillas"
SIN_GUIA_ESPERADO = ("tres-centros", "recorrido-completo")
ADVERTENCIAS = []

CENTROS_NAV = [
    ("idiomas", "Centro de Idiomas", "#8b5cf6"),
    ("computacion", "Centro de Computación", "#10b981"),
    ("emprendimiento", "Centro de Emprendimiento", "#f59e0b"),
    ("comun", "Los tres centros (común)", "#7030A0"),
]
RE_SCRIPT = re.compile(r"script-(\d{2}(?:-[a-z])?)-", re.I)
RE_PREFIJO = re.compile(r"^[a-z]+-\d{2}-")


# ==============================================================================
# ASSETS EXTERNOS (Separación estricta de arquitectura: CSS y JS independientes)
# ==============================================================================
ASSETS_DIR = Path(__file__).resolve().parent / "assets"

def _cargar_asset(nombre: str) -> str:
    ruta = ASSETS_DIR / nombre
    if not ruta.exists():
        raise FileNotFoundError(f"Asset no encontrado: {ruta}")
    return ruta.read_text(encoding="utf-8")

CSS_MODAL = _cargar_asset("modal_guia.css")
_JS_LOGIC = _cargar_asset("modal_guia.js")
CSS_AI = _cargar_asset("asistente_ia.css")
_JS_AI = _cargar_asset("asistente_ia.js")
HTML_AI = _cargar_asset("asistente_ia_snippet.html")

JS_SCRIPT_TEMPLATE = f"""<style>
/* ASISTENTE CCEE: bloque generado */
__CSS__

{CSS_AI}
</style>
{HTML_AI}
<script src="__KNOWLEDGE_SCRIPT__"></script>
<script>
{_JS_LOGIC}
{_JS_AI}
</script>"""

# ======================= BLOQUE 2: resolución de la guía (reemplaza obtener_guia_para_slug) =======================
def detectar_script(slug):
    """'computacion-09-script-18-b-tiene-deuda' → '18-B' (antes fallaba: buscaba 'script-18-B' en minúsculas)."""
    m = RE_SCRIPT.search(slug)
    return m.group(1).upper() if m else None


def ids_nodos_en_html(contenido):
    """Ids de los nodos del SVG, en orden. Llamar DESPUÉS de quitar la inyección previa: el JS también
    contiene la cadena data-node-id=" y contaminaría la lista."""
    ids = []
    for m in re.finditer(r'<g\b[^>]*\bdata-node-id="([^"]+)"', contenido):
        if m.group(1) not in ids:
            ids.append(m.group(1))
    return ids


def _guia_curada(slug, id_centro, sid):
    try:
        g = obtener_guia(slug, id_centro)
    except Exception:
        g = None
    if g:
        return g
    if sid:
        for k, v in GUIAS_SCRIPTS.items():
            if str(k).upper() == sid:
                return v
        return None
    limpio = RE_PREFIJO.sub("", slug)  # quita "<centro>-NN-"
    if limpio in GUIAS_BASE:
        return GUIAS_BASE[limpio]
    if slug in GUIAS_BASE:
        return GUIAS_BASE[slug]
    for k, v in GUIAS_BASE.items():
        if k in limpio:
            return v
    return None


def _normalizar(info):
    """Garantiza campo, tipo y detalle en cada fila (la tabla siempre pinta 6 columnas).
    No toca 'ejemplo': si falta, el JS lo deduce de 'valor'."""
    out = dict(info)
    filas = []
    for it in out.get("instrucciones") or []:
        f = dict(it)
        for k, defecto in (("campo", "—"), ("tipo", "Acción"), ("detalle", "—")):
            if not f.get(k):
                f[k] = defecto
        f.setdefault("valor", "")
        filas.append(f)
    out["instrucciones"] = filas
    return out


def _validar_y_ordenar(guia, ids_nodos, slug):
    """Deja solo nodos que existen en el SVG y los ordena como el recorrido (c0, c1… cr). Así el botón
    «Siguiente» nunca apunta a un paso sin nodo y el stepper no se queda trabado."""
    if not ids_nodos:
        return {k: _normalizar(v) for k, v in guia.items()}
    fuera = [k for k in guia if k not in ids_nodos]
    if fuera:
        ADVERTENCIAS.append(f"{slug}: nodos de la guía que no existen en el diagrama (se descartan): {fuera}")
    validas = [k for k in guia if k in ids_nodos]
    if guia and not validas:
        ADVERTENCIAS.append(f"{slug}: ningún nodo de la guía coincide con el diagrama; ids del diagrama: {ids_nodos}")
    elif validas:
        faltan = [n for n in ids_nodos if n not in guia]
        if faltan:
            ADVERTENCIAS.append(f"{slug}: nodos del diagrama sin guía: {faltan}")
    elif not any(s in slug for s in SIN_GUIA_ESPERADO):
        ADVERTENCIAS.append(f"{slug}: sin guía operativa; se verá el pasaporte nativo de Archify")

    def orden(k):
        m = re.search(r"(\d+)$", k)
        return (int(m.group(1)) if m else 10 ** 6, ids_nodos.index(k))

    return {k: _normalizar(guia[k]) for k in sorted(validas, key=orden)}


def obtener_guia_para_slug(slug, id_centro="", ids_nodos=None):
    """Guía {id_de_nodo: ficha} del flujo, validada contra los nodos reales del SVG."""
    sid = detectar_script(slug)
    guia = dict(_guia_curada(slug, id_centro, sid) or {})
    if sid:  # casuísticas: se completan (o se imponen) desde plantillas.py
        generada = guia_casuistica_de(id_centro, sid)
        for nid, info in generada.items():
            curada = guia.get(nid)
            if PRIORIDAD_CASUISTICAS == "plantillas" or not (curada and curada.get("instrucciones")):
                guia[nid] = info
    return _validar_y_ordenar(guia, ids_nodos, slug)


# ======================= BLOQUE 3: navegación (reemplaza construir_navegacion_flujos) =======================
def _listar_flujos(carpeta_diagramas):
    flujos = []
    if not carpeta_diagramas.is_dir():
        return flujos
    for s in sorted(p for p in carpeta_diagramas.glob("[0-9][0-9]-*") if p.is_dir()):
        htmls = sorted(s.glob("*.html"))
        if htmls:
            flujos.append((s, htmls[0]))
    return flujos


def _destino_en_centro(c_id, carpeta_actual, carpeta_centros):
    """Mismo flujo (por slug, no por número) en otro centro; si no existe, su primer flujo; si no, el índice.
    Antes se comparaba la carpeta completa «NN-slug» y, al cambiar la numeración (p. ej. por Ligas),
    caía siempre en el primer flujo: de ahí los saltos raros."""
    flujos = _listar_flujos(carpeta_centros / c_id / "diagramas")
    slug_actual = carpeta_actual.name[3:]
    for s, h in flujos:
        if s.name[3:] == slug_actual:
            return f"../../../{c_id}/diagramas/{s.name}/{h.name}"
    if flujos:
        s, h = flujos[0]
        return f"../../../{c_id}/diagramas/{s.name}/{h.name}"
    return f"../../../index.html#sec-{c_id}"


def _html_nav_bottom(flujo_ant, flujo_sig, url_centros):
    def tarjeta(f, clase, etiqueta):
        if not f:
            texto = "Primer flujo del centro" if clase == "prev" else "Último flujo del centro"
            return (f'<div class="flow-bottom-card {clase} placeholder"><span class="flow-card-badge">{etiqueta}</span>'
                    f'<span class="flow-card-title muted">{texto}</span></div>')
        acento = " primary-accent" if clase == "next" else ""
        meta = f'<span class="flow-card-meta">{html.escape(f["cap"])}</span>' if f["cap"] else ""
        titulo = html.escape(f["titulo"])
        return (f'<a href="{html.escape(f["url"])}" class="flow-bottom-card {clase}{acento}" title="{f["num"]:02d}. {titulo}">'
                f'<span class="flow-card-badge">{etiqueta}</span>'
                f'<span class="flow-card-num-title"><span class="flow-card-num">{f["num"]:02d}</span>'
                f'<span class="flow-card-title">{titulo}</span></span>{meta}</a>')

    return ('<!-- === FLOW NAV BOTTOM === -->\n'
            '<section class="flow-nav-bottom-section" aria-label="Navegación entre flujos">\n'
            '  <div class="flow-bottom-container">\n'
            f'    {tarjeta(flujo_ant, "prev", "← Flujo anterior")}\n'
            f'    <a href="{url_centros}" class="flow-bottom-hub-btn" title="Volver a la galería de Centros">🏛️ Volver a Centros</a>\n'
            f'    {tarjeta(flujo_sig, "next", "Flujo siguiente →")}\n'
            '  </div>\n'
            '</section>\n'
            '<!-- === /FLOW NAV BOTTOM === -->')


def construir_navegacion_flujos(ruta_html):
    """Barra superior, tarjetas inferiores y datos de anterior/siguiente.
    Ruta esperada: centros/<centro>/diagramas/NN-slug/<archivo>.html"""
    carpeta_diagrama = ruta_html.parent
    carpeta_centros = ruta_html.parents[3]
    nombre = ruta_html.parents[2].name
    nombres = {c[0]: c for c in CENTROS_NAV}
    id_centro = nombre if nombre in nombres else "comun"
    _, nombre_centro, color_centro = nombres[id_centro]
    url_centros = f"../../../index.html#sec-{id_centro}"

    opciones_centros = []
    for c_id, c_nom, _ in CENTROS_NAV:
        if c_id == id_centro:
            destino = f"../{carpeta_diagrama.name}/{ruta_html.name}"
        else:
            destino = _destino_en_centro(c_id, carpeta_diagrama, carpeta_centros)
        sel = ' selected="selected"' if c_id == id_centro else ""
        opciones_centros.append(f'<option value="{destino}"{sel}>{html.escape(c_nom)}</option>')
    select_centros = "\n            ".join(opciones_centros)

    flujos = []
    for s, h in _listar_flujos(carpeta_diagrama.parent):
        slug_s = s.name[3:]
        flujos.append({
            "num": int(s.name[:2]), "slug": slug_s,
            "titulo": TITULOS.get(slug_s, slug_s.replace("-", " ").capitalize()),
            "cap": CAPACIDADES.get(slug_s, ""),
            "url": f"../{s.name}/{h.name}",
            "is_curr": s.resolve() == carpeta_diagrama.resolve(),
        })
    curr_idx = next((i for i, f in enumerate(flujos) if f["is_curr"]), 0)
    total = len(flujos)
    flujo_ant = flujos[curr_idx - 1] if curr_idx > 0 else None
    flujo_sig = flujos[curr_idx + 1] if curr_idx < total - 1 else None

    opciones_flujos = []
    for f in flujos:
        sel = ' selected="selected"' if f["is_curr"] else ""
        opciones_flujos.append(f'<option value="{f["url"]}"{sel}>{f["num"]:02d}. {html.escape(f["titulo"])}</option>')
    select_flujos = "\n          ".join(opciones_flujos)

    chevron_izq = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"></polyline></svg>'
    chevron_der = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>'
    if flujo_ant:
        t = html.escape(flujo_ant["titulo"])
        btn_prev = (f'<a href="{flujo_ant["url"]}" class="flow-btn-top prev" title="Flujo anterior: {flujo_ant["num"]:02d}. {t}">'
                    f'{chevron_izq}<span class="flow-btn-num">{flujo_ant["num"]:02d}</span><span class="flow-btn-txt">{t}</span></a>')
    else:
        btn_prev = (f'<span class="flow-btn-top prev disabled" title="Primer flujo de este centro">{chevron_izq}'
                    '<span class="flow-btn-txt">Inicio</span></span>')
    if flujo_sig:
        t = html.escape(flujo_sig["titulo"])
        btn_next = (f'<a href="{flujo_sig["url"]}" class="flow-btn-top next primary" title="Siguiente flujo: {flujo_sig["num"]:02d}. {t}">'
                    f'<span class="flow-btn-num">{flujo_sig["num"]:02d}</span><span class="flow-btn-txt">{t}</span>{chevron_der}</a>')
    else:
        btn_next = ('<span class="flow-btn-top next disabled" title="Último flujo de este centro">'
                    f'<span class="flow-btn-txt">Fin</span>{chevron_der}</span>')

    nav_top = f'''<!-- === FLOW NAV TOP === -->
    <nav class="flow-nav-top" aria-label="Navegación entre flujos">
      <div class="flow-nav-left">
        <a href="{url_centros}" class="btn-flow-centros" title="Volver a la galería principal de Centros Empresariales">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
          <span>Volver a Centros</span>
        </a>
        <span class="flow-nav-sep">/</span>
        <div class="flow-nav-select-wrap flow-nav-select-center-wrap">
          <span class="flow-center-dot" style="position:absolute; left:0.65rem; top:50%; transform:translateY(-50%); z-index:2; pointer-events:none; background:{color_centro};"></span>
          <select class="flow-nav-select flow-nav-select-center" onchange="if(this.value) window.location.href=this.value" title="Cambiar a otro Centro Empresarial">
            {select_centros}
          </select>
          <span class="flow-nav-select-arrow">▾</span>
        </div>
        <span class="flow-nav-sep">/</span>
        <div class="flow-nav-select-wrap">
          <select class="flow-nav-select" onchange="if(this.value) window.location.href=this.value" title="Cambiar a otro flujo del centro">
            {select_flujos}
          </select>
          <span class="flow-nav-select-arrow">▾</span>
        </div>
      </div>
      <div class="flow-nav-right">
        {btn_prev}
        <span class="flow-nav-counter">Flujo <strong>{curr_idx + 1}</strong> de {total}</span>
        {btn_next}
      </div>
    </nav>
    <!-- === /FLOW NAV TOP === -->'''

    return {
        "nav_top": nav_top,
        "nav_bottom": _html_nav_bottom(flujo_ant, flujo_sig, url_centros),
        "flujo_ant": flujo_ant,
        "flujo_sig": flujo_sig,
        "url_centros": url_centros,
    }


# ======================= BLOQUE 4: inyección (reemplaza inyectar_en_html e inyectar_todos) =======================
def _limpiar_inyeccion_previa(contenido):
    contenido = re.sub(
        r"\s*<!-- === ASISTENTE CCEE INTEGRADO START === -->.*?<!-- === ASISTENTE CCEE INTEGRADO END === -->",
        "",
        contenido,
        flags=re.DOTALL,
    )
    contenido = re.sub(
        r"\s*<script\b(?![^>]*\bsrc=)[^>]*>(?:(?!</script>).)*?"
        r"ASISTENTE IA CENTROS EMPRESARIALES USS · BASE LOCAL \+ GROQ"
        r"(?:(?!</script>).)*?</script>",
        "",
        contenido,
        flags=re.DOTALL,
    )
    contenido = re.sub(r"\s*<style>\s*/\* === (?:DISEÑO RESPONSIVO|GUÍA OPERATIVA).*?</script>", "", contenido, flags=re.DOTALL)
    contenido = re.sub(r'\s*<style>(?:(?!</style>).)*?ASISTENTE IA CENTROS EMPRESARIALES USS · DISEÑO ULTRA-PREMIUM(?:(?!</style>).)*?</style>', "", contenido, flags=re.DOTALL)
    contenido = re.sub(r'\s*<script src="[^"]*asistente_conocimiento\.js"></script>', "", contenido)
    for marca in ("FLOW NAV TOP", "FLOW NAV BOTTOM"):
        contenido = re.sub(rf"\s*<!-- === {marca} === -->.*?<!-- === /{marca} === -->", "", contenido, flags=re.DOTALL)
    contenido = re.sub(r"\s*<!-- === ASISTENTE IA CENTROS EMPRESARIALES USS.*?<!-- === /ASISTENTE IA CENTROS EMPRESARIALES USS === -->", "", contenido, flags=re.DOTALL)
    # Limpiar cualquier residuo previo en etiquetas de nodos o flechas
    contenido = re.sub(r'\s+data-step-state="[^"]*"', '', contenido)
    contenido = re.sub(r'\s+data-ultimo-escogido="[^"]*"', '', contenido)
    contenido = re.sub(r'\s+data-step-edge="[^"]*"', '', contenido)
    return contenido


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import diapositivas  # noqa: E402  (herramientas/diapositivas.py)

RAIZ_REPO = Path(__file__).resolve().parents[2]
VISOR = RAIZ_REPO / "visor_instructivos" / "index.html"


def _sin_tildes(texto):
    import unicodedata
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()


GENERICAS = {"horario", "formulario", "docente", "ubicacion", "pestana", "consulta"}
COMILLAS = r"[\'‘’\"“”«»]([^\'‘’\"“”«»]{3,60})[\'‘’\"“”«»]"


def _claves_fila(fila):
    """Frases de una fila de la guía que pueden aparecer en el texto de la lámina."""
    campo = _sin_tildes(re.sub(r"\s*\(.*?\)", "", fila.get("campo", "")).strip())
    claves = [campo] if len(campo) >= 4 and campo not in GENERICAS else []
    claves += [_sin_tildes(c) for c in re.findall(r"«([^»]{4,})»", fila.get("valor", ""))]
    if "guardado" in campo:
        claves.append("guard")  # «Guardar la información», «Guarde la información»
    return claves


def _puntaje(clave, linea):
    """3: la lámina la nombra entre comillas · 2: al inicio del paso · 1: más adelante · 0: no aparece."""
    texto = _sin_tildes(linea["texto"])
    pos = texto.find(clave)
    if pos == -1:
        return 0
    if any(clave == _sin_tildes(c).strip() for c in re.findall(COMILLAS, linea["texto"])):
        return 3
    return 2 if pos < 40 else 1


def _marcas(filas, lineas, sin_marca=()):
    """{índice de fila: número de la lámina} cuando el campo de la guía es el de un paso numerado."""
    marcas = {}
    numeradas = [l for l in lineas if l["num"]]
    for i, fila in enumerate(filas):
        if fila.get("campo") in sin_marca:
            continue
        mejor = (0, None)
        usados = set(marcas.values())
        for clave in _claves_fila(fila):
            for linea in numeradas:
                p = _puntaje(clave, linea)
                if not (p >= 2 or len(clave) >= 14):
                    continue
                # A igual puntaje gana el paso que ninguna otra fila tomó todavía.
                if p > mejor[0] or (p == mejor[0] and mejor[1] in usados and linea["num"] not in usados):
                    mejor = (p, linea["num"])
        if mejor[1]:
            marcas[str(i)] = mejor[1]
    return marcas


def _resolver_diapositivas(guia, carpeta_html, slug):
    """Cambia {"instructivo", "n"} por rutas relativas al HTML (recorte, completa y visor)."""
    for paso, info in guia.items():
        lista = info.get("diapositivas")
        if not lista:
            continue
        resueltas = []
        for d in lista:
            inst = INSTRUCTIVOS[d["instructivo"]]
            recorte = diapositivas.recorte(inst["id"], d["n"], d.get("caja"))
            completa = diapositivas.diapositiva(inst["id"], d["n"])
            if not recorte:
                ADVERTENCIAS.append(f"{slug} · {paso}: falta la diapositiva {d['n']} de {inst['id']} (ejecuta herramientas/diapositivas.py)")
                continue
            rel = lambda ruta: os.path.relpath(RAIZ_REPO / ruta, carpeta_html).replace(os.sep, "/")
            resueltas.append({
                "src": rel(recorte), "completa": rel(completa),
                "visor": rel(VISOR.relative_to(RAIZ_REPO)) + f"?p={inst['id']}&d={d['n']}",
                "fuente": inst["titulo"], "n": d["n"], "texto": d.get("texto", ""),
                "lineas": [{"num": x["num"], "texto": x["texto"]} for x in diapositivas.texto_diapositiva(inst["id"], d["n"])],
            })
            resueltas[-1]["marcas"] = _marcas(info.get("instrucciones") or [], resueltas[-1]["lineas"], d.get("sin_marca", ()))
        info["diapositivas"] = resueltas


def _json_seguro(obj):
    """JSON para incrustar en <script>: «</» se escapa para que un texto no cierre el script."""
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def inyectar_en_html(ruta_html, slug):
    """Inyecta CSS, navegación superior/inferior y la guía operativa; se puede ejecutar varias veces."""
    nombre = ruta_html.parents[2].name
    id_centro = nombre if nombre in ("idiomas", "computacion", "emprendimiento") else ""
    nav = construir_navegacion_flujos(ruta_html)

    contenido = _limpiar_inyeccion_previa(ruta_html.read_text(encoding="utf-8"))
    nodo_ids = ids_nodos_en_html(contenido)
    guia = obtener_guia_para_slug(slug, id_centro, nodo_ids)
    _resolver_diapositivas(guia, ruta_html.parent, slug)
    conocimiento_script = os.path.relpath(
        ASSETS_DIR / "asistente_conocimiento.js",
        ruta_html.parent,
    ).replace(os.sep, "/")

    if re.search(r'<div class="header"', contenido):
        contenido = re.sub(r'(<div class="header"[^>]*>)', lambda m: nav["nav_top"] + "\n    " + m.group(1), contenido, count=1)
    else:
        ADVERTENCIAS.append(f"{slug}: no se encontró <div class=\"header\">; no se inyectó la barra superior")

    bloque = (
        "<!-- === ASISTENTE CCEE INTEGRADO START === -->\n"
        + JS_SCRIPT_TEMPLATE
        .replace("__CSS__", CSS_MODAL)
        .replace("__KNOWLEDGE_SCRIPT__", html.escape(conocimiento_script, quote=True))
        .replace("__GUIA_JSON__", _json_seguro(guia))
        .replace("__SIGUIENTE_FLUJO_JSON__", _json_seguro(nav["flujo_sig"]))
        .replace("__ANTERIOR_FLUJO_JSON__", _json_seguro(nav["flujo_ant"]))
        .replace("__VOLVER_CENTROS_URL__", nav["url_centros"])
        + "\n<!-- === ASISTENTE CCEE INTEGRADO END === -->"
    )
    extra = nav["nav_bottom"] + "\n" + bloque
    i = contenido.rfind("</body>")
    contenido = contenido[:i] + extra + "\n" + contenido[i:] if i != -1 else contenido + "\n" + extra

    ruta_html.write_text(contenido, encoding="utf-8")
    return True


def inyectar_todos():
    raiz = Path(__file__).resolve().parent.parent.parent
    cont = 0
    ADVERTENCIAS.clear()
    for html_file in sorted((raiz / "centros").glob("**/diagramas/**/*.html")):
        if inyectar_en_html(html_file, html_file.stem):
            cont += 1
    print(f"Inyección completada en {cont} diagramas HTML.")
    if ADVERTENCIAS:
        print(f"\n⚠ {len(ADVERTENCIAS)} advertencias de guías:")
        for a in ADVERTENCIAS:
            print("  -", a)
    return cont


if __name__ == "__main__":
    inyectar_todos()
