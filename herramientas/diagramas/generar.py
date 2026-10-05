#!/usr/bin/env python3
"""Genera los diagramas interactivos paso a paso de los Centros Empresariales.

Para cada centro (centros/<centro>/datos.json) y cada plantilla de plantillas.py:
  1. escribe la especificación Archify (<nombre>.workflow.json o .sequence.json);
  2. la compila con `archify finalize`, que valida esquema, geometría, textos y navegador;
  3. exporta <nombre>-claro.png, <nombre>-oscuro.png y <nombre>.svg con exportar.mjs.
Además genera el comparativo de los tres centros (centros/comun/diagramas) y los índices
centros/README.md, centros/index.html y centros/<centro>/README.md (indices.py).

Uso:
  python3 herramientas/diagramas/generar.py                       # todo
  python3 herramientas/diagramas/generar.py computacion           # un centro (sin el común)
  python3 herramientas/diagramas/generar.py comun                 # solo el comparativo
  python3 herramientas/diagramas/generar.py idiomas --solo 2 --solo 4
  python3 herramientas/diagramas/generar.py --sin-imagenes        # solo JSON + HTML

Requisitos: node >= 18, el motor Archify (bash herramientas/diagramas/instalar_archify.sh)
y Playwright con Chromium para la prueba en navegador y las imágenes.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

from centro import RAIZ, Centro, centros_disponibles  # noqa: E402
import plantillas  # noqa: E402
from indices import generar_indices  # noqa: E402

ARCHIFY = Path(os.environ.get("ARCHIFY_DIR", AQUI / ".archify" / "archify"))
CLI = ARCHIFY / "bin" / "archify.mjs"


def traducciones():
    """Textos de la interfaz del visor en español (catálogo incluido en Archify)."""
    return json.loads((ARCHIFY / "examples" / "locales" / "es.json").read_text(encoding="utf-8"))


def entorno():
    """Archify necesita Chrome o Chromium para su prueba en navegador (browser-check)."""
    env = dict(os.environ)
    if "ARCHIFY_CHROME" not in env:
        for candidato in sorted(Path("/opt/pw-browsers").glob("chromium-*/chrome-linux/chrome"), reverse=True):
            env["ARCHIFY_CHROME"] = str(candidato)
            break
    return env


def compilar(tipo, spec_rel, html_rel):
    """archify finalize: valida y produce el HTML. Devuelve (ok, salida)."""
    cmd = ["node", str(CLI), "finalize", tipo, spec_rel, html_rel, "--quality", "showcase", "--json"]
    r = subprocess.run(cmd, cwd=RAIZ, capture_output=True, text=True, env=entorno())
    return r.returncode == 0, (r.stdout.strip() or r.stderr.strip())


def resumen_fallas(salida):
    """Mensajes y arreglos sugeridos del recibo de finalize, en pocas líneas."""
    try:
        recibo = json.loads(salida)
    except json.JSONDecodeError:
        return salida[:2000]
    lineas = []
    for d in recibo.get("diagnostics", []):
        lineas.append(f"  - {d.get('message', '')[:300]}")
        for fix in d.get("supportedFixes", [])[:1]:
            lineas.append(f"    arreglo: {fix[:300]}")
    return "\n".join(lineas) or salida[:2000]


def limpiar_recibos(carpeta, nombre):
    """finalize deja recibos y evidencias junto al HTML; no forman parte del entregable."""
    for f in carpeta.glob(f"{nombre}.*.json"):
        if not f.name.endswith((".workflow.json", ".sequence.json", ".lifecycle.json")):
            f.unlink()
    for sub in ("browser-check", "visual-check", "review-2", "review-3"):
        shutil.rmtree(carpeta / sub, ignore_errors=True)


def limpiar_obsoletos(id_centro, numeros_slugs):
    """Borra las carpetas NN-tema de un centro que ya no corresponden a ninguna plantilla."""
    carpeta = RAIZ / "centros" / id_centro / "diagramas"
    vigentes = {f"{n:02d}-{s}" for n, s in numeros_slugs}
    for sub in sorted(carpeta.glob("[0-9][0-9]-*")):
        if sub.is_dir() and sub.name not in vigentes:
            shutil.rmtree(sub)
            print(f"BORRADO {sub.relative_to(RAIZ)} (ya no se genera)")


def generar(tipo, spec):
    html_rel = spec["meta"]["output"]
    carpeta_rel, archivo = html_rel.rsplit("/", 1)
    nombre = archivo[: -len(".html")]
    carpeta = RAIZ / carpeta_rel
    carpeta.mkdir(parents=True, exist_ok=True)
    spec_rel = f"{carpeta_rel}/{nombre}.{tipo}.json"
    (RAIZ / spec_rel).write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ok, salida = compilar(tipo, spec_rel, html_rel)
    limpiar_recibos(carpeta, nombre)
    return ok, html_rel, salida


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("centros", nargs="*", help="idiomas, computacion, emprendimiento o comun (por defecto, todo)")
    ap.add_argument("--solo", type=int, action="append", help="número de diagrama (se puede repetir)")
    ap.add_argument("--sin-imagenes", action="store_true", help="no exportar PNG ni SVG")
    args = ap.parse_args()

    if not CLI.exists():
        sys.exit(f"No encuentro Archify en {ARCHIFY}. Ejecuta: bash herramientas/diagramas/instalar_archify.sh")

    tr = traducciones()
    pedidos = args.centros or [*centros_disponibles(), "comun"]
    trabajos = []
    for id_centro in pedidos:
        if id_centro == "comun":
            centros = [Centro(i) for i in centros_disponibles()]
            trabajos += [(n, lambda f=f: f(centros, tr)) for n, _, f in plantillas.DIAGRAMAS_COMUNES]
        else:
            c = Centro(id_centro)
            c.tr = tr
            lista = plantillas.diagramas_de(c)
            if not args.solo:
                limpiar_obsoletos(c.id, [(n, s) for n, s, _ in lista])
            trabajos += [(n, lambda f=f, c=c: f(c)) for n, _, f in lista]

    hechos, fallas = [], []
    for numero, construir in trabajos:
        if args.solo and numero not in args.solo:
            continue
        ok, html_rel, salida = generar(*construir())
        if ok:
            hechos.append(html_rel)
            print(f"OK     {html_rel}")
        else:
            fallas.append(html_rel)
            print(f"FALLA  {html_rel}\n{resumen_fallas(salida)}")

    if hechos and not args.sin_imagenes:
        r = subprocess.run(["node", str(AQUI / "exportar.mjs"), *hechos], cwd=RAIZ)
        if r.returncode != 0:
            fallas.append("exportar.mjs")

    for ruta in generar_indices():
        print(f"ÍNDICE {ruta.relative_to(RAIZ)}")

    print(f"\n{len(hechos)} diagramas listos, {len(fallas)} con fallas.")
    sys.exit(1 if fallas else 0)


if __name__ == "__main__":
    main()
