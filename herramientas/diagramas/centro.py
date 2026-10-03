"""Lectura de centros/<centro>/datos.json y textos derivados para los diagramas.

Un valor null en datos.json se muestra como «por confirmar»: nunca se inventa un código.
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CENTROS = RAIZ / "centros"
POR_CONFIRMAR = "por confirmar"


def leer_json(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def codigo(valor, defecto=POR_CONFIRMAR):
    """Código de un campo de datos.json ({"codigo": ...} o texto); «por confirmar» si falta."""
    if isinstance(valor, dict):
        valor = valor.get("codigo")
    return valor if valor not in (None, "") else defecto


class Centro:
    """Datos de un centro con los textos cortos que usan las plantillas."""

    def __init__(self, id_centro):
        self.comun = leer_json(CENTROS / "comun" / "datos.json")
        self.d = leer_json(CENTROS / id_centro / "datos.json")
        self.id = self.d["id"]
        self.nombre = self.d["nombre"]
        self.autor = self.comun["autor"]

    # ---- identificadores -------------------------------------------------
    @property
    def nivel(self):
        return codigo(self.d["nivel"])

    @property
    def programa(self):
        return codigo(self.d["programa"])

    @property
    def materia(self):
        return codigo(self.d["materia"])

    @property
    def mayor(self):
        return codigo(self.d["mayor"])

    @property
    def departamento(self):
        return codigo(self.d["departamento"])

    @property
    def confirmado_en_test(self):
        """True si el centro ya tiene su programa verificado en TEST."""
        return self.d["programa"] is not None

    # ---- periodo y grupos ------------------------------------------------
    @property
    def partes(self):
        p = self.d["partes_2026"]
        return f"{p[0]['codigo']}–{p[-1]['codigo']}"

    @property
    def periodo_ejemplo(self):
        return self.d["periodo_ejemplo"]

    @property
    def parte_ejemplo(self):
        return self.d["parte_ejemplo"]

    @property
    def nrc_ejemplo(self):
        return self.d["nrc_ejemplo"]

    def nrc(self, numero):
        return next((n for n in self.d["nrc_test"] if n["nrc"] == numero), None)

    # ---- cursos y notas --------------------------------------------------
    @property
    def curso_ejemplo(self):
        c = self.d["curso_ejemplo"]
        if c["materia"] and c["numero"]:
            return f"{c['materia']} {c['numero']}"
        return c["titulo"] or POR_CONFIRMAR

    @property
    def escala(self):
        e = self.d["escala"]
        if not e:
            return "escala por confirmar"
        return f"modo {e['modo']} · aprueba con {e['nota_minima']}"

    @property
    def suficiencia(self):
        """True, False o None (por definir)."""
        return self.d["examen_suficiencia"]["aplica"]

    @property
    def prerrequisito_fatal(self):
        return self.d["prerrequisitos"]["estado"] == "confirmado"

    # ---- textos de cabecera ----------------------------------------------
    def subtitulo(self):
        partes = [f"Nivel {self.nivel}", f"Programa {self.programa}"]
        if self.d["materia"]:
            partes.append(f"Materia {self.materia}")
        partes.append(f"Grupos {self.partes} (2026)")
        return " · ".join(partes) + f" · Elaborado por: {self.autor}"

    def script(self, id_script):
        return self.d["scripts"][id_script]

    def nombre_script(self, id_script):
        return next(s["nombre"] for s in self.comun["scripts"] if s["id"] == id_script)

    def dudas(self):
        return [f"{d['id']}: {d['texto']}" for d in self.d["dudas"]]


def centros_disponibles():
    return leer_json(CENTROS / "comun" / "datos.json")["centros"]
