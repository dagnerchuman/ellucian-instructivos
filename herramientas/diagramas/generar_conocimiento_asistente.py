#!/usr/bin/env python3
"""Genera la base local recuperable del Asistente IA de Centros.

No incorpora claves ni hace llamadas de red. Lee las fuentes versionadas del
proyecto y las fragmenta para que el navegador envíe al modelo solo los pasajes
pertinentes a cada consulta, no toda la memoria del repositorio.
"""
import json
import re
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "herramientas/diagramas/assets/asistente_conocimiento.js"
REGISTRO = RAIZ / ".claude/skills/preguntas-y-dudas-centros/registro.md"
REFERENCIAS = RAIZ / ".claude/skills/arquitectura-centros-empresariales/references"
DATOS = [
    RAIZ / "centros/comun/datos.json",
    RAIZ / "centros/idiomas/datos.json",
    RAIZ / "centros/computacion/datos.json",
    RAIZ / "centros/emprendimiento/datos.json",
]
DECISIONES = RAIZ / "conocimiento/decisiones"
MAX_CARACTERES = 2_800


def relativo(ruta):
    return ruta.relative_to(RAIZ).as_posix()


def texto_fuente(ruta):
    if ruta.suffix == ".json":
        return json.dumps(json.loads(ruta.read_text(encoding="utf-8")), ensure_ascii=False, indent=2)
    return ruta.read_text(encoding="utf-8")


def fragmentos(texto):
    """Corta por líneas y conserva las tablas/encabezados Markdown legibles."""
    limpio = re.sub(r"\n{3,}", "\n\n", texto).strip()
    lineas = limpio.splitlines()
    salida, actual = [], []
    largo = 0
    for linea in lineas:
        linea = linea.rstrip()
        adicional = len(linea) + 1
        if actual and largo + adicional > MAX_CARACTERES:
            salida.append("\n".join(actual).strip())
            actual, largo = [], 0
        while len(linea) > MAX_CARACTERES:
            if actual:
                salida.append("\n".join(actual).strip())
                actual, largo = [], 0
            salida.append(linea[:MAX_CARACTERES])
            linea = linea[MAX_CARACTERES:]
        actual.append(linea)
        largo += len(linea) + 1
    if actual:
        salida.append("\n".join(actual).strip())
    return [trozo for trozo in salida if trozo]


def decisiones_aceptadas():
    """Incluye solo ADR vigentes como evidencia; las propuestas no son reglas."""
    aceptadas = []
    for ruta in sorted(DECISIONES.glob("ADR-*.md")):
        texto = ruta.read_text(encoding="utf-8")
        encabezado = texto.split("---", 2)
        if len(encabezado) == 3 and re.search(r"(?m)^estado:\s*aceptado\s*$", encabezado[1]):
            aceptadas.append(ruta)
    return aceptadas


def main():
    fuentes = [
        REGISTRO,
        *DATOS,
        *sorted(REFERENCIAS.glob("*.md")),
        *decisiones_aceptadas(),
    ]
    conocimiento = []
    for ruta in fuentes:
        if not ruta.is_file():
            raise FileNotFoundError(f"Fuente local de conocimiento no encontrada: {relativo(ruta)}")
        fuente = relativo(ruta)
        for indice, texto in enumerate(fragmentos(texto_fuente(ruta)), start=1):
            conocimiento.append({
                "id": f"{fuente}#{indice}",
                "fuente": fuente,
                "texto": texto,
            })

    serializado = json.dumps(conocimiento, ensure_ascii=False, separators=(",", ":"))
    # Evita que un eventual texto de fuente cierre la etiqueta script que lo contiene.
    serializado = serializado.replace("</", "<\\/")
    salida = (
        "/* Archivo generado: no editar a mano. Ejecuta "
        "python3 herramientas/diagramas/generar_conocimiento_asistente.py */\n"
        "window.CCEE_KNOWLEDGE = " + serializado + ";\n"
        "window.CCEE_KNOWLEDGE_META = {fragmentos: " + str(len(conocimiento))
        + ", generadoDesde: 'datos.json, registro.md, referencias operativas y ADR aceptados'};\n"
    )
    SALIDA.write_text(salida, encoding="utf-8")
    print(f"BASE {relativo(SALIDA)} · {len(conocimiento)} fragmentos")


if __name__ == "__main__":
    main()
