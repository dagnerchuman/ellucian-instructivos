#!/usr/bin/env python3
"""Valida la base de conocimiento del proyecto (conocimiento/, skills y datos de los centros).

Revisa:
  1. enlaces rotos: [texto](ruta) y [[nota]] en los Markdown de la memoria;
  2. metadatos de los ADR: campos obligatorios, estado válido, id igual al nombre del archivo,
     secciones obligatorias y que `reemplazado_por` exista;
  3. fuentes de los ADR: cada C##, R##, E##, U## o S## citado existe en registro.md;
  4. el manifest: rutas que existen, centros iguales a centros/comun/datos.json, skills iguales a las carpetas;
  5. el contrato de datos.json: campos obligatorios, un estado válido por cada script del catálogo
     y dudas que existen en el registro;
  6. el espejo .claude/skills = .agents/skills;
  7. datos sensibles: correos, DNI, teléfonos, contraseñas o claves en las rutas del manifest.

Uso:
  python3 herramientas/validar_conocimiento.py           # errores y avisos; sale con 1 si hay errores
  python3 herramientas/validar_conocimiento.py --estricto # los avisos también cuentan como error
"""
import argparse
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONOCIMIENTO = RAIZ / "conocimiento"
DECISIONES = CONOCIMIENTO / "decisiones"
REGISTRO = RAIZ / ".claude" / "skills" / "preguntas-y-dudas-centros" / "registro.md"
MANIFEST = CONOCIMIENTO / "manifest.json"

ESTADOS_ADR = {"propuesto", "aceptado", "reemplazado", "descartado"}
CAMPOS_ADR = ["id", "titulo", "estado", "fecha", "fuentes", "temas"]
SECCIONES_ADR = ["## Contexto", "## Decisión", "## Alternativas descartadas", "## Consecuencias", "## Criterio de salida"]
ID_FUENTE = re.compile(r"\b([CREUS]\d{2})\b")

# Markdown que forman la memoria (donde se revisan los enlaces).
MEMORIA = ["conocimiento/**/*.md", "CLAUDE.md", "AGENTS.md", ".claude/skills/**/*.md", ".agents/rules/*.md",
           "centros/**/README.md", "herramientas/README.md", "docs/README.md"]

SENSIBLES = [
    ("correo", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("DNI", re.compile(r"\bDNI\D{0,6}\d{8}\b")),
    ("teléfono", re.compile(r"(?<![\w.])9\d{2}[ -]?\d{3}[ -]?\d{3}(?![\w.])")),
    ("contraseña", re.compile(r"(?i)\b(contraseña|password|passwd|clave)\s*[:=]\s*[`\"']?(?=[^\s*`|]*[A-Za-z0-9])[^\s*`|]{4,}")),
    ("token", re.compile(r"\b(ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9-]{20,}|AKIA[0-9A-Z]{16})\b")),
]
# Correos de ejemplo que aparecen en los instructivos y no identifican a nadie.
CORREOS_PERMITIDOS = {"correo@ellucian.com", "correo@gmail.com"}

errores, avisos = [], []


def rel(p):
    return p.relative_to(RAIZ).as_posix()


def error(donde, msg):
    errores.append(f"{donde}: {msg}")


def aviso(donde, msg):
    avisos.append(f"{donde}: {msg}")


def leer_json(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def ids_registro():
    texto = REGISTRO.read_text(encoding="utf-8")
    return set(re.findall(r"^\| ([CREUS]\d{2}) \|", texto, re.M))


# --------------------------------------------------------------------------- 1. enlaces
def archivos_memoria():
    vistos = set()
    for patron in MEMORIA:
        for p in sorted(RAIZ.glob(patron)):
            if p.is_file() and p not in vistos and "node_modules" not in p.parts:
                vistos.add(p)
                yield p


def revisar_enlaces():
    notas = {p.stem.lower() for p in RAIZ.glob("**/*.md") if ".git" not in p.parts and "node_modules" not in p.parts}
    enlace = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
    wiki = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
    for p in archivos_memoria():
        texto = p.read_text(encoding="utf-8")
        sin_codigo = re.sub(r"```.*?```", "", texto, flags=re.S)
        sin_codigo = re.sub(r"`[^`\n]*`", "", sin_codigo)
        for destino in enlace.findall(sin_codigo):
            if re.match(r"^[a-z]+:", destino) or destino.startswith("#"):
                continue
            ruta = destino.split("#")[0]
            if not ruta:
                continue
            ruta = re.sub(r"%20", " ", ruta)
            if not (p.parent / ruta).exists():
                error(rel(p), f"enlace roto → {destino}")
        for nombre in wiki.findall(sin_codigo):
            if Path(nombre.strip()).stem.lower() not in notas:
                error(rel(p), f"nota de Obsidian inexistente → [[{nombre}]]")


# --------------------------------------------------------------------------- 2 y 3. ADR
def frontmatter(texto):
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    if not m:
        return None
    datos = {}
    for linea in m.group(1).splitlines():
        if ":" not in linea:
            continue
        clave, valor = linea.split(":", 1)
        valor = valor.strip()
        if valor.startswith("[") and valor.endswith("]"):
            valor = [v.strip() for v in valor[1:-1].split(",") if v.strip()]
        datos[clave.strip()] = valor
    return datos


def revisar_adrs(registro):
    ids = {}
    adrs = sorted(DECISIONES.glob("ADR-*.md"))
    if not adrs:
        error("conocimiento/decisiones", "no hay ningún ADR")
    for p in adrs:
        texto = p.read_text(encoding="utf-8")
        fm = frontmatter(texto)
        if fm is None:
            error(rel(p), "falta el bloque de metadatos (--- … ---)")
            continue
        for campo in CAMPOS_ADR:
            if not fm.get(campo):
                error(rel(p), f"falta el metadato «{campo}»")
        id_ = fm.get("id", "")
        if not p.name.startswith(f"{id_}-"):
            error(rel(p), f"el id {id_} no coincide con el nombre del archivo")
        if id_ in ids:
            error(rel(p), f"id repetido: {id_} (también en {ids[id_]})")
        ids[id_] = rel(p)
        if fm.get("estado") not in ESTADOS_ADR:
            error(rel(p), f"estado inválido «{fm.get('estado')}» (usa {', '.join(sorted(ESTADOS_ADR))})")
        if fm.get("estado") == "reemplazado" and not fm.get("reemplazado_por"):
            error(rel(p), "un ADR reemplazado necesita «reemplazado_por»")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(fm.get("fecha", ""))):
            error(rel(p), "la fecha debe ser AAAA-MM-DD")
        for seccion in SECCIONES_ADR:
            if seccion not in texto:
                error(rel(p), f"falta la sección «{seccion}»")
        fuentes = fm.get("fuentes") or []
        for f in (fuentes if isinstance(fuentes, list) else [fuentes]):
            if ID_FUENTE.fullmatch(f) and f not in registro:
                error(rel(p), f"cita {f}, que no existe en registro.md")
    for p in adrs:
        fm = frontmatter(p.read_text(encoding="utf-8")) or {}
        sucesor = fm.get("reemplazado_por")
        if sucesor and sucesor not in ids:
            error(rel(p), f"reemplazado_por {sucesor}, que no existe")
    return ids


# --------------------------------------------------------------------------- 4 y 5. manifest y datos
def revisar_manifest(adrs, registro):
    if not MANIFEST.exists():
        error("conocimiento", "falta manifest.json")
        return
    m = leer_json(MANIFEST)
    comun = leer_json(RAIZ / "centros" / "comun" / "datos.json")

    def existe(ruta, donde):
        if not (RAIZ / ruta).exists():
            error("conocimiento/manifest.json", f"{donde}: no existe «{ruta}»")

    for c in m["centros"]:
        for clave in ("datos", "ficha", "diagramas", "guia_pruebas"):
            if clave in c or clave != "guia_pruebas":
                existe(c[clave], f"centro {c['id']}")
        if c["skill"] not in m["skills"]:
            error("conocimiento/manifest.json", f"centro {c['id']}: la skill {c['skill']} no está en «skills»")
    if [c["id"] for c in m["centros"]] != comun["centros"]:
        error("conocimiento/manifest.json", f"los centros no coinciden con centros/comun/datos.json ({comun['centros']})")
    for f in m["fuentes"]:
        existe(f["ruta"], f"fuente {f['id']}")
    for g in m["generadores"]:
        for ruta in g["entradas"] + g["salidas"]:
            existe(ruta, f"generador {g['id']}")
    for bloque in ("fuentes", "generadores", "contratos", "sistemas", "actores"):
        for item in m[bloque]:
            if item.get("adr") and item["adr"] not in adrs:
                error("conocimiento/manifest.json", f"{bloque}: cita {item['adr']}, que no existe")
    if m["proyecto"].get("alcance") not in adrs:
        error("conocimiento/manifest.json", "proyecto.alcance debe citar un ADR existente")
    for base in (".claude/skills", ".agents/skills"):
        en_disco = sorted(p.name for p in (RAIZ / base).iterdir() if p.is_dir())
        if en_disco != sorted(m["skills"]):
            error("conocimiento/manifest.json", f"«skills» no coincide con {base}: {en_disco}")

    contrato = next(c for c in m["contratos"] if c.get("campos"))
    estados = next(c for c in m["contratos"] if c.get("estados"))["estados"]
    catalogo = [s["id"] for s in comun["scripts"]]
    for c in m["centros"]:
        d = leer_json(RAIZ / c["datos"])
        donde = c["datos"]
        for campo in contrato["campos"]:
            if campo not in d:
                error(donde, f"falta el campo «{campo}» (contrato del manifest)")
        if d.get("id") != c["id"]:
            error(donde, f"id «{d.get('id')}» distinto del manifest «{c['id']}»")
        scripts = d.get("scripts", {})
        if sorted(scripts) != sorted(catalogo):
            error(donde, "los scripts no coinciden con el catálogo de centros/comun/datos.json")
        for sid, s in scripts.items():
            if s.get("estado") not in estados:
                error(donde, f"script {sid}: estado inválido «{s.get('estado')}»")
        for duda in d.get("dudas", []):
            if not ID_FUENTE.fullmatch(duda["id"]):
                aviso(donde, f"duda con id «{duda['id']}»: no es un ID del registro (C/R/E/U/S + 2 dígitos)")
            elif duda["id"] not in registro:
                error(donde, f"duda {duda['id']}, que no existe en registro.md")
        for lista in ("matricula", "notas"):
            for sid in d.get("casuisticas", {}).get(lista, []):
                if sid not in catalogo:
                    error(donde, f"casuística {sid}: no está en el catálogo")


# --------------------------------------------------------------------------- 6. espejo
def revisar_espejo():
    sys.path.insert(0, str(RAIZ / "herramientas"))
    from sincronizar_skills import CARPETAS, diferencias  # noqa: E402

    solo_claude, solo_agents, distintos = diferencias(CARPETAS["claude"], CARPETAS["agents"])
    for r in solo_claude:
        error(".agents/skills", f"falta {r} (ejecuta sincronizar_skills.py --desde claude)")
    for r in solo_agents:
        error(".claude/skills", f"falta {r} (¿lo editó Antigravity? --desde agents)")
    for r in distintos:
        error("skills", f"{r} difiere entre .claude y .agents")


# --------------------------------------------------------------------------- 7. sensibles
def revisar_sensibles():
    m = leer_json(MANIFEST)
    for base in m["datos_sensibles"]["revisar"]:
        raiz = RAIZ / base
        archivos = [raiz] if raiz.is_file() else [p for p in raiz.rglob("*") if p.is_file()]
        for p in archivos:
            if p.suffix.lower() not in {".md", ".json", ".py", ".txt", ".yml", ".yaml", ".mjs", ".sh", ".html"}:
                continue
            if any(x in p.parts for x in (".archify", "node_modules", "__pycache__", "fonts")):
                continue
            if p.suffix == ".html" and "diagramas" in p.parts:
                continue
            texto = p.read_text(encoding="utf-8", errors="ignore")
            for tipo, patron in SENSIBLES:
                for hallado in set(patron.findall(texto)):
                    valor = hallado if isinstance(hallado, str) else hallado[0]
                    if tipo == "correo" and valor.lower() in CORREOS_PERMITIDOS:
                        continue
                    error(rel(p), f"posible dato sensible ({tipo}): «{valor[:40]}»")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--estricto", action="store_true", help="los avisos también cuentan como error")
    args = ap.parse_args()

    registro = ids_registro()
    revisar_enlaces()
    adrs = revisar_adrs(registro)
    revisar_manifest(adrs, registro)
    revisar_espejo()
    revisar_sensibles()

    for e in errores:
        print(f"ERROR  {e}")
    for a in avisos:
        print(f"AVISO  {a}")
    print(f"\n{len(adrs)} ADR · {len(registro)} entradas del registro · {len(errores)} errores · {len(avisos)} avisos")
    sys.exit(1 if errores or (args.estricto and avisos) else 0)


if __name__ == "__main__":
    main()
