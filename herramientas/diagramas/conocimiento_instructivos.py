"""Texto de los instructivos de Ellucian (PPTX) como fragmentos de la base del asistente.

Un fragmento por pantalla o tema del instructivo: las diapositivas seguidas con el mismo título
(«Configuraciones: SCASYLB Syllabus de curso», diap. 9 a 12) van juntas, cada párrafo con su número
de diapositiva, para que el asistente cite «instructivo 6.1.1, diap. 10». Las portadas, «Overview»
vacíos y «Muchas gracias» no entran. Lo que se repite en muchas diapositivas es diseño (pie, logo).
"""
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import diapositivas  # noqa: E402

MAX_CARACTERES = 2_400
# Diapositivas sin contenido operativo: portada, agradecimiento, índice de capacidades.
RELLENO = re.compile(r"^(instructivo|consultor\.?|cargo|mes, a[nñ]o|muchas gracias|correo@ellucian\.com|overview|"
                     r"agenda|índice|indice|overview: mapa de capacidades|overview: región donde aplica|todo lac)$", re.I)
# Correos de los consultores (lámina de cierre: nombre y correo de Ellucian): no entran a la base, que se publica con
# el sitio. Los de ejemplo de un campo sí, como en validar_conocimiento.py (CORREOS_PERMITIDOS).
CORREO = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
CORREOS_DE_EJEMPLO = {"correo@ellucian.com", "correo@gmail.com"}


def _sin_correos(texto):
    return " ".join(CORREO.sub(lambda m: m.group(0) if m.group(0).lower() in CORREOS_DE_EJEMPLO else "", texto).split())


def _parrafos(pres):
    """Por diapositiva, sus párrafos con número de paso (si es lista numerada)."""
    from pptx.oxml.ns import qn
    por_lamina = []
    for lamina in pres.slides:
        parrafos = []
        formas = sorted((f for f in lamina.shapes if f.has_text_frame), key=lambda f: ((f.top or 0) // 200000, f.left or 0))
        for forma in formas:
            contador = None
            for p in forma.text_frame.paragraphs:
                ppr = p._p.pPr
                auto = ppr.find(qn("a:buAutoNum")) if ppr is not None else None
                if auto is not None:
                    contador = (contador + 1) if contador is not None else int(auto.get("startAt", "1"))
                for k, texto in enumerate(t for t in (" ".join(x.split()) for x in re.split(r"[\v\n]", p.text)) if t):
                    num = str(contador) if auto is not None and k == 0 else ""
                    parrafos.append((num, texto))
        # Las tablas también llevan pasos y valores.
        for forma in lamina.shapes:
            if getattr(forma, "has_table", False) and forma.has_table:
                for fila in forma.table.rows:
                    celdas = [" ".join(c.text.split()) for c in fila.cells]
                    celdas = [c for c in celdas if c]
                    if celdas:
                        parrafos.append(("", " | ".join(celdas)))
        por_lamina.append(parrafos)
    return por_lamina


def _titulo(parrafos):
    """Título de la diapositiva sin el contador «1/4»; vacío si no hay uno claro."""
    for num, texto in parrafos:
        if num or len(texto) > 110 or " | " in texto or texto.rstrip().endswith("."):
            continue
        if re.match(r"^(Tema|Configuraciones?|Procedimiento|Proceso|Overview|Resumen|Paso)\b|[A-Z]{6,8}", texto, re.I):
            return re.sub(r"\s*\d+\s*/\s*\d+\s*$", "", texto).strip(" –-:")
    return ""


PROPOSITO_GENERICO = re.compile(r"^Instructivo técnico oficial", re.I)
# Palabras en mayúsculas de las diapositivas que parecen páginas de Banner y no lo son.
NO_SON_PAGINAS = {"FAILED", "GESTION", "GRACIAS", "SIEMPRE", "SIMULA", "STUDENT", "TERMINAR", "TRABAJO"}
# Lámina de índice: «01 | Overview», «02 | Configuraciones»… No responde nada.
ITEM_INDICE = re.compile(r"^\d{2}\s*\|\s*\S")


def _codigos_banner(textos):
    """Páginas de Banner del instructivo, en orden de aparición. «GUARDAR» o «GENERAL» también salen en minúsculas
    en el mismo instructivo: son palabras, no páginas."""
    todo = "\n".join(textos)
    vistos = []
    for c in re.findall(r"\b[GSTF][A-Z]{5,7}\b", todo):
        if c in vistos or c in NO_SON_PAGINAS or re.search(r"\b" + c.capitalize() + r"\b|\b" + c.lower() + r"\b", todo):
            continue
        vistos.append(c)
    return vistos


def fragmentos_instructivo(id_, info, ficha):
    """[{texto, diaps, seccion}] del instructivo: primero su ficha (índice de temas y páginas), luego una por pantalla."""
    def leer():
        from pptx import Presentation
        return _parrafos(Presentation(diapositivas.RAIZ / info["path"]))
    # Párrafos del PPTX guardados en herramientas/.cache/pptx: se releen solo si cambia el PPTX o este archivo.
    laminas = [[(num, _sin_correos(t)) for num, t in ps]
               for ps in diapositivas.en_cache(id_, "parrafos", leer, codigo=__file__)]
    frecuencia = Counter(t for ps in laminas for t in {t for _, t in ps})
    limite = max(3, len(laminas) * 0.3)
    encabezado = f"# {ficha['etiqueta']} — manual de Ellucian"
    grupos, actual = [], None
    for n, ps in enumerate(laminas, start=1):
        utiles = [(num, t) for num, t in ps if frecuencia[t] < limite and len(t) > 2 and not RELLENO.match(t)]
        if not utiles or sum(len(t) for _, t in utiles) < 25:
            continue
        if sum(1 for _, t in utiles if ITEM_INDICE.match(t)) >= max(2, len(utiles) * 0.5):
            continue
        titulo = _titulo(utiles)
        lineas = [f"{num}. {t}" if num else t for num, t in utiles if t != titulo]
        texto = "\n".join(lineas)
        largo = len(texto)
        if actual and (titulo and titulo == actual["titulo"] or not titulo) and actual["largo"] + largo <= MAX_CARACTERES:
            actual["laminas"].append((n, texto))
            actual["largo"] += largo
            continue
        actual = {"titulo": titulo or (actual["titulo"] if actual and not titulo else ""), "laminas": [(n, texto)], "largo": largo}
        grupos.append(actual)
    secciones = []
    for g in grupos:
        if g["largo"] < 80:  # portada, índice u «Overview» sin contenido
            continue
        ns = [n for n, _ in g["laminas"]]
        rango = f"diap. {ns[0]}" if len(ns) == 1 else f"diap. {ns[0]} a {ns[-1]}"
        cuerpo = "\n".join(f"(diap. {n}) {t}" for n, t in g["laminas"])
        titulo = f"## {g['titulo']} · {rango}" if g["titulo"] else f"## {rango}"
        secciones.append({"texto": f"{encabezado}\n{titulo}\n{cuerpo}"[: MAX_CARACTERES + 400], "diaps": ns,
                          "seccion": g["titulo"], "rango": rango})

    # Ficha: de qué trata el instructivo, qué páginas usa y en qué diapositivas está cada tema.
    paginas = _codigos_banner([t for ps in laminas for _, t in ps])
    proposito = (info.get("purpose") or "").strip()
    lineas = [encabezado, "## Ficha del instructivo",
              f"Capacidad {ficha['capacidad']} · {ficha['diapositivas']} diapositivas"
              + (f" · procedimiento de Ellucian {ficha['procedimiento']}" if ficha["procedimiento"] else "")]
    if proposito and not PROPOSITO_GENERICO.match(proposito):
        lineas.append(f"Para qué sirve: {proposito}")
    if paginas:
        lineas.append("Páginas de Banner: " + ", ".join(paginas[:18]))
    # Un tema largo sale partido en varios fragmentos seguidos con el mismo título: en la ficha va una sola línea.
    temas, previo = [], None
    for sec in secciones:
        if not sec["seccion"]:
            continue
        if previo and previo["seccion"] == sec["seccion"]:
            previo["hasta"] = sec["diaps"][-1]
            continue
        previo = {"seccion": sec["seccion"], "desde": sec["diaps"][0], "hasta": sec["diaps"][-1]}
        temas.append(previo)
    temas = [f"- {t['seccion']} (diap. {t['desde']}" + (f" a {t['hasta']})" if t["hasta"] != t["desde"] else ")")
             for t in temas]
    if temas:
        lineas.append("Contenido:")
        lineas.extend(temas[:30])
    for regla in (info.get("rules") or [])[:6]:
        lineas.append(f"Regla: {regla}")
    return [{"texto": "\n".join(lineas)[: MAX_CARACTERES + 400], "diaps": [], "seccion": "Ficha del instructivo", "rango": ""}] + secciones


def todos():
    """[(fuente, ficha del catálogo, id, [fragmentos])] de los 83 instructivos, en el orden del visor."""
    from catalogo_instructivos import catalogo
    cat = catalogo()
    resultado = []
    for id_, info in diapositivas.presentaciones().items():
        ficha = cat[id_]
        try:
            resultado.append((info["path"], ficha, id_, fragmentos_instructivo(id_, info, ficha)))
        except Exception as error:  # noqa: BLE001 - un PPTX dañado no debe tumbar la base entera
            print(f"AVISO instructivo sin texto: {info['path']} ({error})")
    return resultado


if __name__ == "__main__":
    total = 0
    for fuente, ficha, _, fragmentos in todos():
        total += len(fragmentos)
        print(f"{len(fragmentos):3d} {ficha['etiqueta']}")
    print("fragmentos:", total)
