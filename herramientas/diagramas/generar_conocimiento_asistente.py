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
# Skills propias de los centros (SKILL.md y references/, recetas incluidas). Las de video, documentos o diseño no:
# no tratan de Banner ni de los centros.
SKILLS_CENTROS = ["centro-computacion", "centro-idiomas", "centro-emprendimiento", "workflow-pruebas-test",
                  "workflow-consultas-banner"]
MAX_CARACTERES = 2_800
# Instrucciones para agentes (cómo manejar el navegador o documentar capturas): no responden nada a quien pregunta.
EXCLUIDOS = {
    ".claude/skills/workflow-pruebas-test/SKILL.md",
    ".claude/skills/workflow-pruebas-test/references/documentar-prueba-con-capturas.md",
    ".claude/skills/workflow-consultas-banner/SKILL.md",
}
CENTROS = {
    "comun": "Datos comunes de los Centros Empresariales",
    "idiomas": "Datos del Centro de Idiomas",
    "computacion": "Datos del Centro de Computación",
    "emprendimiento": "Datos del Centro de Emprendimiento",
}
PREFIJO_TITULO = re.compile(r"^(?:Guía Oficial|Guía Operativa|Guía|Workflow)\s*:\s*", re.I)
ID_REGISTRO = re.compile(r"(?m)^(?:\|\s*|-\s+\*{1,2})([CUESRD]\d{2,3})\b")
# Secciones de plantilla que no dicen de qué trata el fragmento.
SIN_DETALLE = re.compile(r"^(Contexto|Decisión|Consecuencias|Alternativas.*|Mapa de la skill.*|Índice.*)$", re.I)
ENCABEZADO = re.compile(r"(?m)^#{2,3}\s+(.+?)\s*$")


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


def fragmentos_por_pregunta(texto):
    """Guías de preguntas (ref-preguntas-*.md): un fragmento por «### pregunta», con el título de la guía.

    Así el asistente recupera la respuesta exacta y no un trozo con varias preguntas mezcladas.
    """
    titulo = next((l for l in texto.splitlines() if l.startswith("# ")), "").strip()
    partes = re.split(r"(?m)^(?=### )", texto)
    salida = [f"{titulo}\n\n{parte.strip()}" for parte in partes[1:] if parte.strip()]
    return [trozo for p in salida for trozo in fragmentos(p)] or fragmentos(texto)


def titulo_de(ruta, texto):
    """Nombre con que el asistente cita la fuente: el título del documento, sin «Guía Oficial:» ni rutas."""
    if ruta == REGISTRO:
        return "Registro de decisiones y dudas"
    if ruta.name == "datos.json":
        return CENTROS.get(ruta.parent.name, "Datos de los centros")
    h1 = next((l[2:].strip() for l in texto.splitlines() if l.startswith("# ")), ruta.stem.replace("-", " "))
    h1 = PREFIJO_TITULO.sub("", h1)
    h1 = re.sub(r"\s*\(para cualquier agente\)|\s+—\s+Arquitectura Específica$", "", h1).strip()
    return h1[:1].upper() + h1[1:]


def _limpio(encabezado):
    texto = re.sub(r"[*`]", "", encabezado)
    texto = re.sub(r"^[^\wÁÉÍÓÚÑáéíóúñ¿¡(«]+", "", texto).strip()
    return texto if len(texto) <= 120 else texto[:117].rstrip() + "…"


def detalles(ruta, trozos):
    """Qué parte de la fuente es cada fragmento: los ID del registro o la sección donde empieza."""
    salida, ultimo = [], ""
    for trozo in trozos:
        if ruta == REGISTRO:
            ids = ID_REGISTRO.findall(trozo)
            grupos = {}
            for i in ids:
                grupos.setdefault(i[0], []).append(i)
            salida.append(" · ".join(g[0] if len(g) == 1 else f"{g[0]} a {g[-1]}" for g in grupos.values()))
            continue
        if ruta.parent == DECISIONES:  # el título del ADR ya lo dice todo
            salida.append("")
            continue
        encabezados = ENCABEZADO.findall(trozo)
        primera = next((l for l in trozo.splitlines() if l.strip() and not l.startswith("# ")), "")
        if ruta.name.startswith("ref-preguntas-") and encabezados:
            salida.append(_limpio(encabezados[0]))
        elif ENCABEZADO.match(primera):
            salida.append(_limpio(ENCABEZADO.match(primera).group(1)))
        else:
            salida.append(_limpio(ultimo or (encabezados[0] if encabezados else "")))
        if encabezados:
            ultimo = encabezados[-1]
    return ["" if SIN_DETALLE.match(d) else d for d in salida]


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
        *[r for skill in SKILLS_CENTROS for r in sorted((RAIZ / ".claude/skills" / skill).rglob("*.md"))],
    ]
    conocimiento = []
    for ruta in fuentes:
        if not ruta.is_file():
            raise FileNotFoundError(f"Fuente local de conocimiento no encontrada: {relativo(ruta)}")
        fuente = relativo(ruta)
        if fuente in EXCLUIDOS:
            continue
        completo = texto_fuente(ruta)
        titulo = titulo_de(ruta, completo)
        cortar = fragmentos_por_pregunta if ruta.name.startswith("ref-preguntas-") else fragmentos
        trozos = cortar(completo)
        for indice, (texto, detalle) in enumerate(zip(trozos, detalles(ruta, trozos)), start=1):
            fragmento = {"id": f"{fuente}#{indice}", "fuente": fuente, "texto": texto, "titulo": titulo, "grupo": "uss"}
            if detalle:
                fragmento["detalle"] = detalle
            conocimiento.append(fragmento)

    # Los 83 instructivos de Ellucian (PPTX): su ficha y un fragmento por pantalla o tema, con sus diapositivas.
    from conocimiento_instructivos import todos as instructivos
    catalogo = []
    for fuente, ficha, id_, trozos in instructivos():
        catalogo.append({"id": id_, "codigo": ficha["codigo"], "nombre": ficha["nombre"],
                         "procedimiento": ficha["procedimiento"], "diapositivas": ficha["diapositivas"]})
        for indice, trozo in enumerate(trozos, start=1):
            fragmento = {"id": f"{fuente}#{indice}", "fuente": fuente, "texto": trozo["texto"],
                         "titulo": ficha["etiqueta"], "grupo": "ellucian", "instructivo": id_}
            if trozo["seccion"]:
                fragmento["detalle"] = trozo["seccion"]
            if trozo["diaps"]:
                fragmento["diaps"] = trozo["diaps"]
            conocimiento.append(fragmento)

    serializado = json.dumps(conocimiento, ensure_ascii=False, separators=(",", ":"))
    # Evita que un eventual texto de fuente cierre la etiqueta script que lo contiene.
    serializado = serializado.replace("</", "<\\/")
    salida = (
        "/* Archivo generado: no editar a mano. Ejecuta "
        "python3 herramientas/diagramas/generar_conocimiento_asistente.py */\n"
        "window.CCEE_KNOWLEDGE = " + serializado + ";\n"
        "window.CCEE_INSTRUCTIVOS = " + json.dumps(catalogo, ensure_ascii=False, separators=(",", ":")) + ";\n"
        "window.CCEE_KNOWLEDGE_META = {fragmentos: " + str(len(conocimiento))
        + ", generadoDesde: 'datos.json, registro.md, referencias operativas, skills de los centros, ADR aceptados e instructivos PPTX'};\n"
    )
    from centro import escribir_si_cambia
    escribir_si_cambia(SALIDA, salida)
    print(f"BASE {relativo(SALIDA)} · {len(conocimiento)} fragmentos")


if __name__ == "__main__":
    main()
