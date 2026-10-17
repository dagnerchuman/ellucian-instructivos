"""Guía operativa (tabla de 6 columnas) de cada script de casuística, generada desde plantillas.py.

Fuente única de verdad: CASOS (situación, pasos, resultado) + EXTRA_CASOS (líneas
«Paso NN (CÓDIGO): Título — detalle»). Así los ids de la guía son SIEMPRE los que dibuja
plantillas.casuistica():  c0 (situación) · c1..cN (pasos) · cr (resultado).

Este módulo no importa nada del proyecto: se puede probar solo.
"""
import re

RE_LINEA = re.compile(r"^\s*Paso\s+(\d+)\s*\(([^)]*)\)\s*:\s*(.+?)\s+—\s+(.+?)\s*$", re.S)

# Valores «tecleables» que se reconocen dentro del detalle (primero = Valor, siguientes = Ejemplo).
_PATRONES = [
    (r"(?i:c[oó]digo)\s+(RE|DD|TT|INH|U\d{2})\b", "Código {}"),
    (r"\b[Ss]tatus:?\s*(AS|IS|EL|SU)\b", "Status {}"),
    (r"\bMaximum:?\s*(\d+(?:\s*→\s*\d+)?)", "Maximum {}"),
    (r"\bNRC\s+(\d{4})\b", "NRC {}"),
    (r"\bID:?\s*(S\d{8}|\d{9})\b", "ID {}"),
    (r"\bJob\s+(\d{4})\b", "Job {}"),
    (r"\b(?:Periodo[^.(]{0,12}\(ej\.?\s*)?(20\d{4})\b", "Periodo {}"),
    (r"\b(Remaining|Actual):?\s*(-?\d+(?:\s*→\s*\d+)?)", None),
    (r"\bModo:?\s*([VP])\b", "Modo {}"),
    (r"\b(F10)\b", "F10 (Guardar)"),
]

_VERIF = re.compile(r"verific|consulta|auditor|validaci|revisi|diagn|comprob|evaluaci[oó]n", re.I)
_CRITICO = re.compile(r"asentamiento|confirmaci[oó]n|exitos|reejecuci[oó]n|pase a historia|despacho|"
                      r"levantamiento|reactivaci[oó]n|liberaci[oó]n|cierre|bloqueo|asignaci[oó]n de c[oó]digo|ejecuci[oó]n", re.I)
_CAPTURA = re.compile(r"registro|ingreso|captura|creaci|configuraci|asignaci|ampliaci|ajuste|acceso|alineaci|activaci|autorizaci", re.I)


def parsear_linea(texto):
    """'Paso 02 (SFAREGS / SSASECT): Título — detalle' → dict. Si el formato se desvía, no se pierde la línea."""
    m = RE_LINEA.match(texto)
    if not m:
        return {"n": 0, "codes": [], "codes_up": set(), "titulo": texto[:60].strip(), "detalle": texto.strip()}
    n, codigos, titulo, detalle = m.groups()
    codes = [c.strip() for c in codigos.split("/") if c.strip()]
    return {"n": int(n), "codes": codes, "codes_up": {c.upper() for c in codes},
            "titulo": titulo.strip(), "detalle": detalle.strip()}


def clasificar_tipo(titulo):
    """El JS marca en verde las filas cuyo tipo contiene «crítico» o «guardado»."""
    if _VERIF.search(titulo):
        return "Verificación"
    if _CRITICO.search(titulo):
        return "Crítico (guardado)"
    if _CAPTURA.search(titulo):
        return "Captura"
    return "Acción"


def extraer_valor_ejemplo(detalle, pantalla):
    hallados = []
    for patron, plantilla in _PATRONES:
        for m in re.finditer(patron, detalle):
            if plantilla is None:  # Actual / Remaining: «Remaining -1»
                num = re.sub(r"\s+", " ", m.group(2))
                hallados.append((m.start(), m.group(1) + " " + num))
            else:
                hallados.append((m.start(), plantilla.format(re.sub(r"\s+", " ", m.group(1)))))
    hallados.sort()
    vistos = []
    for _, v in hallados:
        if v not in vistos:
            vistos.append(v)
    if not vistos:
        return (pantalla or "—"), "-"
    return vistos[0], (" · ".join(vistos[1:3]) if len(vistos) > 1 else "-")


def _asignar(lineas, codigos_nodo):
    """Reparte las líneas del Excel (5 a 7) entre los nodos del diagrama (4 pasos), sin cambiar el orden.

    Programación dinámica: cada línea va al mismo nodo o al siguiente que la anterior, todos los nodos
    quedan cubiertos y gana el reparto con más coincidencias de código (SFAREGS↔SFAREGS…);
    a igualdad, el más parejo.
    """
    n, m = len(codigos_nodo), len(lineas)
    if not n or not m:
        return []
    NEG = float("-inf")

    def pts(i, j):
        coincide = 3.0 if codigos_nodo[j - 1].upper() in lineas[i]["codes_up"] else 0.0
        return coincide - 0.05 * abs(j - (i + 1) * n / m)

    dp = [[NEG] * (n + 1) for _ in range(m)]
    previo = [[0] * (n + 1) for _ in range(m)]
    dp[0][1] = pts(0, 1)
    for i in range(1, m):
        for j in range(1, n + 1):
            quedarse = dp[i - 1][j]
            avanzar = dp[i - 1][j - 1] if j > 1 else NEG
            mejor, desde = (quedarse, j) if quedarse >= avanzar else (avanzar, j - 1)
            if mejor == NEG:
                continue
            dp[i][j] = mejor + pts(i, j)
            previo[i][j] = desde
    asign, j = [0] * m, min(n, m)
    for i in range(m - 1, -1, -1):
        asign[i] = j
        j = previo[i][j]
    return asign


def _fila(campo, valor, ejemplo, tipo, detalle):
    return {"campo": campo, "valor": valor, "ejemplo": ejemplo, "tipo": tipo, "detalle": detalle}


def construir_guia(situacion, pasos, resultado, lineas_extra, titulo_script=""):
    """situacion=(título, sub) · pasos=[(código, acción[, dato])] · resultado=(título, sub) · lineas_extra=[str]."""
    (sit, sit_sub), (res, res_sub) = situacion, resultado
    lineas = [parsear_linea(t) for t in (lineas_extra or [])]
    asign = _asignar(lineas, [p[0] for p in pasos])
    guia = {
        "c0": {
            "titulo": titulo_script, "pantalla": "CASO", "fase": f"Situación: {sit}", "hito": sit_sub,
            "instrucciones": [_fila("Situación inicial", sit, sit_sub, "Contexto",
                                    f"Punto de partida del script: {sit_sub}.")],
        }
    }
    for j, item in enumerate(pasos, start=1):
        codigo, accion = item[0], item[1]
        dato = item[2] if len(item) > 2 else ""
        filas = []
        for ln, destino in zip(lineas, asign):
            if destino != j:
                continue
            valor, ejemplo = extraer_valor_ejemplo(ln["detalle"], ln["codes"][0] if ln["codes"] else codigo)
            detalle = ln["detalle"]
            if ln["codes"] and codigo.upper() not in ln["codes_up"]:
                detalle = f"({' / '.join(ln['codes'])}) {detalle}"
            filas.append(_fila(ln["titulo"], valor, ejemplo, clasificar_tipo(ln["titulo"]), detalle))
        if not filas:  # nodo sin líneas en el Excel: al menos su acción y dato de TEST
            filas.append(_fila(accion, codigo, dato or "-", clasificar_tipo(accion), accion[0].upper() + accion[1:] + "."))
        guia[f"c{j}"] = {"titulo": titulo_script, "pantalla": codigo, "fase": f"Paso {j}: {accion}",
                         "hito": dato, "instrucciones": filas}
    guia["cr"] = {
        "titulo": titulo_script, "pantalla": "RESULTADO", "fase": f"Resultado: {res}", "hito": res_sub,
        "instrucciones": [_fila("Resultado esperado", res, res_sub, "Resultado",
                                "Estado final del caso una vez ejecutados todos los pasos anteriores.")],
    }
    return guia