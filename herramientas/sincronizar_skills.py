#!/usr/bin/env python3
"""
Mantiene iguales las skills de Claude Code (.claude/skills) y de Antigravity (.agents/skills).

Uso:
    python3 herramientas/sincronizar_skills.py --check          # solo revisa; sale con 1 si difieren
    python3 herramientas/sincronizar_skills.py --desde claude   # espejo exacto .claude → .agents
    python3 herramientas/sincronizar_skills.py --desde agents   # espejo exacto .agents → .claude
    python3 herramientas/sincronizar_skills.py                  # en ambos sentidos: gana el más nuevo

El espejo (--desde) también borra en el destino lo que ya no existe en el origen; úsalo
después de renombrar o borrar una skill. El modo en ambos sentidos no borra nada (no sabe
qué lado borró) y avisa cuando un archivo existe solo en un lado.
"""
import argparse
import filecmp
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CARPETAS = {"claude": RAIZ / ".claude" / "skills", "agents": RAIZ / ".agents" / "skills"}
IGNORAR = {"__pycache__", ".DS_Store"}


def archivos(base):
    return {
        p.relative_to(base)
        for p in base.rglob("*")
        if p.is_file() and not IGNORAR.intersection(p.relative_to(base).parts)
    }


def diferencias(a, b):
    fa, fb = archivos(a), archivos(b)
    distintos = sorted(r for r in fa & fb if not filecmp.cmp(a / r, b / r, shallow=False))
    return sorted(fa - fb), sorted(fb - fa), distintos


def copiar(origen, destino):
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(origen, destino)


def espejo(origen, destino):
    solo_origen, solo_destino, distintos = diferencias(origen, destino)
    for r in solo_origen + distintos:
        copiar(origen / r, destino / r)
        print(f"[COPIADO] {r}")
    for r in solo_destino:
        (destino / r).unlink()
        print(f"[BORRADO] {r}")
    for carpeta in sorted((p for p in destino.rglob("*") if p.is_dir()), reverse=True):
        if not any(carpeta.iterdir()):
            carpeta.rmdir()
    return len(solo_origen) + len(distintos) + len(solo_destino)


def ambos_sentidos(a, b):
    solo_a, solo_b, distintos = diferencias(a, b)
    for r in distintos:
        origen, destino = (a, b) if (a / r).stat().st_mtime >= (b / r).stat().st_mtime else (b, a)
        copiar(origen / r, destino / r)
        print(f"[ACTUALIZADO] {destino.parent.name}/skills <- {origen.parent.name}/skills: {r}")
    for r in solo_a:
        copiar(a / r, b / r)
        print(f"[NUEVO] .agents <- .claude: {r}  (si lo borraste en .agents, usa --desde agents)")
    for r in solo_b:
        copiar(b / r, a / r)
        print(f"[NUEVO] .claude <- .agents: {r}  (si lo borraste en .claude, usa --desde claude)")
    return len(distintos) + len(solo_a) + len(solo_b)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="solo revisar, sin copiar")
    ap.add_argument("--desde", choices=CARPETAS, help="espejo exacto desde esta carpeta")
    args = ap.parse_args()

    a, b = CARPETAS["claude"], CARPETAS["agents"]
    if not a.exists() or not b.exists():
        sys.exit("Error: no encuentro .claude/skills y .agents/skills.")

    if args.check:
        solo_a, solo_b, distintos = diferencias(a, b)
        for r in solo_a:
            print(f"solo en .claude: {r}")
        for r in solo_b:
            print(f"solo en .agents: {r}")
        for r in distintos:
            print(f"distinto: {r}")
        total = len(solo_a) + len(solo_b) + len(distintos)
        print("Skills sincronizadas." if not total else f"{total} diferencia(s).")
        sys.exit(1 if total else 0)

    if args.desde:
        origen = CARPETAS[args.desde]
        destino = b if origen == a else a
        cambios = espejo(origen, destino)
    else:
        cambios = ambos_sentidos(a, b)
    print("Todo al día." if not cambios else f"Sincronización lista: {cambios} archivo(s).")


if __name__ == "__main__":
    main()
