#!/usr/bin/env python3
"""Cuadros morados y números verdes en las capturas de TEST, como las láminas de Ellucian (pedido del usuario, C195).

Cada captura de `demostraciones › ejemplo_prueba_2 › pasos › capturas` puede traer `cuadros`:
    [{"n": 3, "caja": [x0, y0, x1, y1]}, ...]
en píxeles de la imagen original. `n` es el número de la fila de la tabla del paso (la misma de «Su guía»), así el
número verde de la imagen y el de la guía coinciden. La copia anotada se guarda en `<carpeta>/anotadas/<archivo>`;
la original no se toca. Colores tomados de las láminas: morado #8830E8 y verde #3A6C54.

Uso: python3 herramientas/diagramas/anotar_capturas.py   (generar.py lo llama antes de los diagramas)
"""
import hashlib
import io
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from centro import CENTROS, centros_disponibles, leer_json  # noqa: E402

MORADO = (136, 48, 232)
VERDE = (58, 108, 84)
GROSOR = 2
LADO = 18  # cuadrado del número
FUENTES = ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc",
           "C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")


def _fuente(tam):
    for f in FUENTES:
        if Path(f).exists():
            return ImageFont.truetype(f, tam)
    return ImageFont.load_default()


def _tinta(gris, r):
    """Cuántos píxeles oscuros (texto, bordes) quedarían debajo del número."""
    return sum(1 for v in gris.crop(r).getdata() if v < 170)


def _posicion_numero(caja, im, gris, ocupados):
    """El número va pegado al cuadro, en el lado donde tape menos: izquierda, derecha, arriba o abajo
    (en ese orden si empatan), sin salirse de la imagen ni pisar otro cuadro o número."""
    x0, y0, x1, y1 = caja
    cy = (y0 + y1) // 2 - LADO // 2
    mejor = None
    for orden, (x, y) in enumerate(((x0 - LADO - 3, cy), (x1 + 3, cy), (x0, y0 - LADO - 3), (x0, y1 + 3))):
        if x < 0 or y < 0 or x + LADO > im.width or y + LADO > im.height:
            continue
        r = (x, y, x + LADO, y + LADO)
        choca = any(not (r[2] <= o[0] or r[0] >= o[2] or r[3] <= o[1] or r[1] >= o[3]) for o in ocupados)
        puntaje = (choca, _tinta(gris, r) // 6, orden)
        if mejor is None or puntaje < mejor[0]:
            mejor = (puntaje, (x, y))
    return mejor[1] if mejor else (max(0, x0 - LADO - 3), max(0, cy))


def dibujar(origen, cuadros):
    """Imagen (bytes PNG) con los cuadros y sus números."""
    im = Image.open(origen).convert("RGB")
    gris = im.convert("L")
    d = ImageDraw.Draw(im)
    fuente = _fuente(12)
    ocupados = [tuple(c["caja"]) for c in cuadros]
    for c in cuadros:
        x0, y0, x1, y1 = c["caja"]
        d.rectangle((x0, y0, x1, y1), outline=MORADO, width=GROSOR)
    for c in cuadros:
        x, y = _posicion_numero(c["caja"], im, gris, ocupados)
        ocupados.append((x, y, x + LADO, y + LADO))
        d.rectangle((x, y, x + LADO, y + LADO), fill=VERDE)
        texto = str(c["n"])
        l, t, r, b = d.textbbox((0, 0), texto, font=fuente)
        d.text((x + (LADO - (r - l)) / 2 - l, y + (LADO - (b - t)) / 2 - t), texto, fill="white", font=fuente)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def _firma(origen, cuadros):
    """Huella de la captura y sus cuadros: si no cambió, no se vuelve a dibujar (comprimir el PNG es lento)."""
    h = hashlib.sha1(Path(origen).read_bytes())
    h.update(json.dumps(cuadros, sort_keys=True).encode())
    h.update(f"{MORADO}{VERDE}{GROSOR}{LADO}".encode())
    return h.hexdigest()


def anotar_todas():
    """Escribe las copias anotadas que cambiaron. Devuelve cuántas se escribieron y cuántas hay."""
    escritas = total = 0
    for id_centro in centros_disponibles():
        for demo in leer_json(CENTROS / id_centro / "datos.json").get("demostraciones", []):
            ej = demo.get("ejemplo_prueba_2")
            if not ej:
                continue
            carpeta = CENTROS / id_centro / "diagramas" / f"00-{demo['slug']}" / ej["carpeta"]
            ruta_firmas = carpeta / "anotadas" / "firmas.json"
            firmas = json.loads(ruta_firmas.read_text(encoding="utf-8")) if ruta_firmas.exists() else {}
            nuevas = {}
            for p in ej["pasos"]:
                for c in p.get("capturas", []):
                    if not c.get("cuadros"):
                        continue
                    total += 1
                    destino = carpeta / "anotadas" / c["archivo"]
                    firma = nuevas[c["archivo"]] = _firma(carpeta / c["archivo"], c["cuadros"])
                    if destino.exists() and firmas.get(c["archivo"]) == firma:
                        continue
                    destino.parent.mkdir(exist_ok=True)
                    destino.write_bytes(dibujar(carpeta / c["archivo"], c["cuadros"]))
                    escritas += 1
            if nuevas and nuevas != firmas:
                ruta_firmas.write_text(json.dumps(nuevas, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return escritas, total


if __name__ == "__main__":
    e, t = anotar_todas()
    print(f"{t} capturas con cuadros · {e} escritas")
