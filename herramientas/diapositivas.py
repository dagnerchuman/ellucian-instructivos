#!/usr/bin/env python3
"""Convierte los instructivos PPTX en imágenes WebP, una por diapositiva.

El visor (visor_instructivos/) y las guías paso a paso de los diagramas muestran estas
imágenes en lugar de leer el PPTX en el navegador.

    python3 herramientas/diapositivas.py                 # convierte los que faltan o cambiaron
    python3 herramientas/diapositivas.py --solo 5.3_4.1.4.1.6 --solo 6.2.1_Asignar
    python3 herramientas/diapositivas.py --forzar        # vuelve a convertir todo

Salida:
    visor_instructivos/diapositivas/<id>/NNN.webp           diapositiva completa
    visor_instructivos/diapositivas/<id>/recortes/NNN.webp  recorte sin título ni banda lateral (guías)
    visor_instructivos/diapositivas/indice.js               window.DIAPOSITIVAS = {id: {n, ancho, alto, bytes}}

Necesita LibreOffice (soffice), pdftoppm (poppler) y Pillow con WebP. Los <id> son los de
visor_instructivos/data.js; las carpetas CAPACIDAD n/ no se mueven (ADR-015).
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parents[1]
DATA_JS = RAIZ / "visor_instructivos" / "data.js"
SALIDA = RAIZ / "visor_instructivos" / "diapositivas"
INDICE = SALIDA / "indice.js"
ANCHO = 1600
CALIDAD = 72
# Proporciones que se quitan en los recortes: banda lateral izquierda y título superior (diseño Ellucian).
CAJA_RECORTE = (0.034, 0.118, 0.0, 0.075)


def presentaciones():
    """{id: {path, sizeBytes, title…}} leído de visor_instructivos/data.js."""
    texto = DATA_JS.read_text(encoding="utf-8")
    marca = "var PRESENTATIONS = window.PRESENTATIONS = "
    i = texto.index(marca) + len(marca)
    j = texto.index("\n};", i) + 2
    return json.loads(texto[i:j])


def leer_indice():
    if not INDICE.exists():
        return {}
    texto = INDICE.read_text(encoding="utf-8")
    return json.loads(texto[texto.index("{"):texto.rindex("}") + 1])


def escribir_indice(indice):
    ordenado = dict(sorted(indice.items()))
    INDICE.write_text(
        "// Archivo generado por herramientas/diapositivas.py: no lo edites a mano.\n"
        "window.DIAPOSITIVAS = " + json.dumps(ordenado, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8",
    )


def nombre_diapositiva(n):
    return f"{n:03d}.webp"


def convertir_uno(id_, pres, tmp):
    pptx = RAIZ / pres["path"]
    destino = SALIDA / id_
    perfil = Path(tmp) / "perfil"
    pdf_dir = Path(tmp) / "pdf"
    png_dir = Path(tmp) / "png"
    for d in (pdf_dir, png_dir):
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
    subprocess.run(
        ["soffice", f"-env:UserInstallation=file://{perfil}", "--headless", "--norestore",
         "--convert-to", "pdf", "--outdir", str(pdf_dir), str(pptx)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600,
    )
    pdf = next(pdf_dir.glob("*.pdf"))
    subprocess.run(["pdftoppm", "-scale-to-x", str(ANCHO), "-scale-to-y", "-1", "-png", str(pdf), str(png_dir / "d")],
                   check=True, timeout=600)
    pngs = sorted(png_dir.glob("d-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
    shutil.rmtree(destino, ignore_errors=True)
    destino.mkdir(parents=True)
    ancho = alto = 0
    for n, png in enumerate(pngs, start=1):
        with Image.open(png) as im:
            ancho, alto = im.size
            im.convert("RGB").save(destino / nombre_diapositiva(n), "WEBP", quality=CALIDAD, method=6)
    return {"n": len(pngs), "ancho": ancho, "alto": alto, "bytes": pptx.stat().st_size}


def convertir(filtros=None, forzar=False):
    if not shutil.which("soffice") or not shutil.which("pdftoppm"):
        sys.exit("Faltan soffice (LibreOffice) o pdftoppm (poppler).")
    SALIDA.mkdir(parents=True, exist_ok=True)
    pres = presentaciones()
    indice = leer_indice()
    elegidos = [i for i in pres if not filtros or any(f in i for f in filtros)]
    hechos = 0
    with tempfile.TemporaryDirectory() as tmp:
        for k, id_ in enumerate(elegidos, start=1):
            previo = indice.get(id_)
            completo = previo and previo.get("bytes") == (RAIZ / pres[id_]["path"]).stat().st_size and \
                len(list((SALIDA / id_).glob("*.webp"))) == previo.get("n")
            if completo and not forzar:
                continue
            try:
                indice[id_] = convertir_uno(id_, pres[id_], tmp)
            except (subprocess.SubprocessError, StopIteration, OSError) as e:
                print(f"FALLA  {id_}: {e}")
                continue
            hechos += 1
            print(f"OK     [{k}/{len(elegidos)}] {id_}: {indice[id_]['n']} diapositivas")
            escribir_indice(indice)
    escribir_indice(indice)
    print(f"\n{hechos} instructivos convertidos; {len(indice)} en el índice.")


def recorte(id_, n, caja=None):
    """Ruta (relativa a la raíz) del recorte de la diapositiva n; lo crea si falta. None si no existe la diapositiva."""
    origen = SALIDA / id_ / nombre_diapositiva(n)
    if not origen.exists():
        return None
    destino = SALIDA / id_ / "recortes" / nombre_diapositiva(n)
    caja = tuple(caja or CAJA_RECORTE)
    if not destino.exists() or destino.stat().st_mtime < origen.stat().st_mtime:
        destino.parent.mkdir(exist_ok=True)
        with Image.open(origen) as im:
            w, h = im.size
            izq, sup, der, inf = caja
            im.crop((round(w * izq), round(h * sup), round(w * (1 - der)), round(h * (1 - inf)))).save(
                destino, "WEBP", quality=CALIDAD, method=6)
    return destino.relative_to(RAIZ).as_posix()


def diapositiva(id_, n):
    """Ruta (relativa a la raíz) de la diapositiva completa, o None si no se ha convertido."""
    ruta = SALIDA / id_ / nombre_diapositiva(n)
    return ruta.relative_to(RAIZ).as_posix() if ruta.exists() else None


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--solo", action="append", help="convierte solo los id que contengan este texto (se puede repetir)")
    ap.add_argument("--forzar", action="store_true", help="vuelve a convertir aunque ya existan")
    args = ap.parse_args()
    convertir(args.solo, args.forzar)
