#!/usr/bin/env python3
"""Genera los diagramas interactivos paso a paso de los Centros Empresariales.

Para cada centro (centros/<centro>/datos.json) y cada plantilla de plantillas.py:
  1. escribe la especificación Archify (<nombre>.workflow.json o .sequence.json);
  2. la compila con `archify finalize`, que valida esquema, geometría, textos y navegador;
  3. exporta <nombre>-claro.png, <nombre>-oscuro.png y <nombre>.svg con exportar.mjs.
Además genera el comparativo de los tres centros (centros/comun/diagramas) y los índices
centros/README.md, centros/index.html y centros/<centro>/README.md (indices.py).

Solo rehace lo que cambió (C234): Archify compila un diagrama únicamente si cambió su especificación (o
falta su HTML, o cambió el motor), y la inyección (guía, navegación, asistente) solo toca las páginas cuyo
contenido cambia. Lo que no cambió se salta; la cuenta final dice cuántas páginas se escribieron. La memoria
de cada página está en herramientas/.cache/paginas.json (no se sube). El asistente (assets/asistente_ia.js y
.css) y su base se cargan como archivos: si solo cambian ellos, no hay ninguna página que regenerar.

Uso:
  python3 herramientas/diagramas/generar.py                       # lo que cambió (JSON + HTML, sin imágenes)
  python3 herramientas/diagramas/generar.py --forzar              # todo de nuevo, aunque no haya cambiado
  python3 herramientas/diagramas/generar.py computacion           # un centro (sin el común)
  python3 herramientas/diagramas/generar.py comun                 # solo el comparativo
  python3 herramientas/diagramas/generar.py idiomas --solo 2 --solo 4
  python3 herramientas/diagramas/generar.py --con-imagenes        # opcional: exportar PNG y SVG (lento)

Requisitos: node >= 18 y el motor Archify (bash herramientas/diagramas/instalar_archify.sh).
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

from centro import RAIZ, Centro, centros_disponibles, escribir_si_cambia  # noqa: E402
import plantillas  # noqa: E402

ARCHIFY = Path(os.environ.get("ARCHIFY_DIR", AQUI / ".archify" / "archify"))
CLI = ARCHIFY / "bin" / "archify.mjs"
CACHE = RAIZ / "herramientas" / ".cache"
MANIFIESTO = CACHE / "paginas.json"


def _sha(*partes):
    h = hashlib.sha256()
    for p in partes:
        h.update(p if isinstance(p, bytes) else str(p).encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:20]


def _sha_archivo(ruta):
    try:
        return hashlib.sha256(ruta.read_bytes()).hexdigest()[:20]
    except OSError:
        return None


def firma_motor():
    """Versión de Archify: si se actualiza el motor, todo se vuelve a compilar."""
    return _sha(*[f.read_bytes() for f in (ARCHIFY / "package.json", CLI) if f.exists()])


def firma_entorno():
    """Lo que la inyección mete en cada página además de su diagrama: el código de los generadores, los assets
    que van dentro del HTML, los datos de los centros, el catálogo de diapositivas, la lista de páginas
    (navegación anterior/siguiente y selector de centro) y las capturas de TEST junto a cada página.
    No entran los assets que la página carga como archivo (el asistente y su base): si cambian, ninguna página cambia."""
    from inyectar_modales import ASSETS_EXTERNOS
    h = hashlib.sha256()
    archivos = sorted(AQUI.glob("*.py")) + [RAIZ / "herramientas" / "diapositivas.py"]
    archivos += sorted(p for p in (AQUI / "assets").rglob("*") if p.is_file() and p.name not in ASSETS_EXTERNOS)
    archivos += sorted((RAIZ / "centros").glob("*/datos.json"))
    archivos += [RAIZ / "visor_instructivos" / "data.js", RAIZ / "visor_instructivos" / "diapositivas" / "indice.js"]
    for f in archivos:
        h.update(f.relative_to(RAIZ).as_posix().encode("utf-8"))
        h.update(f.read_bytes() if f.exists() else b"-")
    for carpeta in sorted((RAIZ / "centros").glob("*/diagramas/[0-9][0-9]-*")):
        if not carpeta.is_dir():
            continue
        htmls = sorted(carpeta.glob("*.html"))
        h.update(f"{carpeta.relative_to(RAIZ).as_posix()}|{htmls[0].name if htmls else ''}".encode("utf-8"))
        for f in sorted(carpeta.rglob("*")):
            if f.is_file() and f.parent != carpeta:  # en subcarpetas: capturas de TEST y sus copias anotadas
                st = f.stat()
                h.update(f"{f.relative_to(RAIZ).as_posix()}|{st.st_size}|{st.st_mtime_ns}".encode("utf-8"))
    return h.hexdigest()[:20]


def leer_manifiesto():
    try:
        return json.loads(MANIFIESTO.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def guardar_manifiesto(manifiesto):
    vigente = {k: v for k, v in sorted(manifiesto.items()) if (RAIZ / k).exists()}
    CACHE.mkdir(parents=True, exist_ok=True)
    escribir_si_cambia(MANIFIESTO, json.dumps(vigente, ensure_ascii=False, indent=1) + "\n")


def traducciones():
    """Textos de la interfaz del visor en español (catálogo incluido en Archify)."""
    return json.loads((ARCHIFY / "examples" / "locales" / "es.json").read_text(encoding="utf-8"))


def entorno():
    """Archify necesita Chrome o Chromium para su prueba en navegador (browser-check)."""
    env = dict(os.environ)
    if "ARCHIFY_CHROME" not in env:
        for candidato in sorted(Path("/opt/pw-browsers").glob("chromium-*/chrome-linux*/chrome"), reverse=True):
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


def compilar_si_cambio(tipo, spec, motor, previa, forzar):
    """Pasada 1: Archify solo si cambió la especificación del diagrama, falta su HTML o cambió el motor.

    Si no, el HTML que ya está sirve de base: la inyección quita lo inyectado antes y lo vuelve a poner.
    Devuelve (estado, html_rel, nombre, firma_spec, salida) con estado «igual», «compilado» o «falla»."""
    html_rel = spec["meta"]["output"]
    carpeta_rel, archivo = html_rel.rsplit("/", 1)
    nombre = archivo[: -len(".html")]
    carpeta = RAIZ / carpeta_rel
    carpeta.mkdir(parents=True, exist_ok=True)
    spec_rel = f"{carpeta_rel}/{nombre}.{tipo}.json"
    ruta_spec, ruta_html = RAIZ / spec_rel, RAIZ / html_rel
    texto = json.dumps(spec, ensure_ascii=False, indent=2) + "\n"
    firma_spec = _sha(tipo, texto)
    previo_spec = ruta_spec.read_text(encoding="utf-8") if ruta_spec.exists() else None
    if not forzar and ruta_html.exists() and previo_spec == texto and previa.get("motor", motor) == motor:
        return "igual", html_rel, nombre, firma_spec, ""
    previo_html = ruta_html.read_bytes() if ruta_html.exists() else None
    ruta_spec.write_text(texto, encoding="utf-8")
    ok, salida = compilar(tipo, spec_rel, html_rel)
    limpiar_recibos(carpeta, nombre)
    if not ok:
        # Queda todo como estaba (la especificación anterior y su HTML): la próxima vez se vuelve a intentar.
        if previo_spec is None:
            ruta_spec.unlink(missing_ok=True)
        else:
            ruta_spec.write_text(previo_spec, encoding="utf-8")
        if previo_html is None:
            ruta_html.unlink(missing_ok=True)
        else:
            ruta_html.write_bytes(previo_html)
        return "falla", html_rel, nombre, firma_spec, salida
    return "compilado", html_rel, nombre, firma_spec, salida


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("centros", nargs="*", help="idiomas, computacion, emprendimiento o comun (por defecto, todo)")
    ap.add_argument("--solo", type=int, action="append", help="número de diagrama (se puede repetir)")
    ap.add_argument("--con-imagenes", action="store_true", help="exportar PNG y SVG con Chromium (por defecto desactivado)")
    ap.add_argument("--sin-imagenes", action="store_true", help="(obsoleto) no exportar imágenes; ahora es el comportamiento predeterminado")
    ap.add_argument("--forzar", action="store_true", help="compilar e inyectar todo, aunque no haya cambiado")
    args = ap.parse_args()
    inicio = time.time()

    if not CLI.exists():
        sys.exit(f"No encuentro Archify en {ARCHIFY}. Ejecuta: bash herramientas/diagramas/instalar_archify.sh")
    try:
        import pptx  # noqa: F401
    except ImportError:
        # diapositivas.py calla los errores del PPTX: sin python-pptx las láminas salen sin texto ni números
        # y los recortes cambian en todo el sitio (C184).
        sys.exit("Falta python-pptx: sin él las láminas quedan sin texto ni números verdes. "
                 "Ejecuta: python3 -m pip install --user python-pptx")

    from anotar_capturas import anotar_todas
    redibujadas, con_cuadros = anotar_todas()
    print(f"CAPTURAS {con_cuadros} con cuadros y números · {redibujadas} redibujadas")

    subprocess.run(
        [sys.executable, str(AQUI / "generar_conocimiento_asistente.py")],
        cwd=RAIZ,
        check=True,
    )
    from indices import generar_indices
    from diapositivas_pasos import escribir_indice_asistente

    ruta, n = escribir_indice_asistente()
    print(f"LÁMINAS {ruta.relative_to(RAIZ)} · {n} láminas para el asistente")

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

    from inyectar_modales import ADVERTENCIAS, inyectar_en_html
    manifiesto = leer_manifiesto()
    motor = firma_motor()
    listos, fallas, compilados = [], [], []
    for numero, construir in trabajos:
        if args.solo and numero not in args.solo:
            continue
        tipo, spec = construir()
        previa = manifiesto.get(spec["meta"]["output"], {})
        estado, html_rel, nombre, firma_spec, salida = compilar_si_cambio(tipo, spec, motor, previa, args.forzar)
        if estado == "falla":
            fallas.append(html_rel)
            print(f"FALLA  {html_rel}\n{resumen_fallas(salida)}")
            continue
        if estado == "compilado":
            compilados.append(html_rel)
            print(f"ARCHIFY {html_rel}")
        listos.append((html_rel, nombre, firma_spec))

    # Pasada 2: guía, navegación y asistente. Se salta la página si nada de lo que lleva dentro cambió.
    entorno = firma_entorno()
    escritas, avisos = [], []
    for html_rel, nombre, firma_spec in listos:
        ruta = RAIZ / html_rel
        firma = _sha(firma_spec, entorno, motor)
        previa = manifiesto.get(html_rel, {})
        if (not args.forzar and html_rel not in compilados and previa.get("firma") == firma
                and previa.get("salida") == _sha_archivo(ruta)):
            avisos += previa.get("avisos", [])
            continue
        antes = len(ADVERTENCIAS)
        if inyectar_en_html(ruta, nombre):
            escritas.append(html_rel)
            print(f"OK     {html_rel}")
        nuevos = ADVERTENCIAS[antes:]
        avisos += nuevos
        manifiesto[html_rel] = {"firma": firma, "salida": _sha_archivo(ruta), "motor": motor, "avisos": nuevos}
    guardar_manifiesto(manifiesto)

    if args.con_imagenes and not args.sin_imagenes:
        # PNG y SVG de las páginas que cambiaron o que aún no los tienen.
        exportar = [h for h, n, _ in listos if h in escritas or not (RAIZ / h).with_name(f"{n}-claro.png").exists()]
        if exportar:
            r = subprocess.run(["node", str(AQUI / "exportar.mjs"), *exportar], cwd=RAIZ)
            if r.returncode != 0:
                fallas.append("exportar.mjs")

    for ruta in generar_indices():
        print(f"ÍNDICE {ruta.relative_to(RAIZ)}")

    print(f"\n{len(listos)} diagramas listos, {len(fallas)} con fallas · {len(compilados)} compilados con Archify, "
          f"{len(escritas)} páginas actualizadas, {len(listos) - len(escritas)} sin cambios · {time.time() - inicio:.0f} s.")
    if avisos:
        print(f"\n⚠ {len(avisos)} advertencias de las guías:")
        for aviso in avisos:
            print("  -", aviso)
    sys.exit(1 if fallas else 0)


if __name__ == "__main__":
    main()
