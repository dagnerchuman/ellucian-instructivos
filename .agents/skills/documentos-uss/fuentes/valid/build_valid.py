# -*- coding: utf-8 -*-
"""Estrategia de validación de la migración (Ellucian) aplicada a Centros Empresariales."""
import html
import os
import re

import new_sections

HERE = os.path.dirname(os.path.abspath(__file__))
AUTHOR = 'Dagner Anibal Chuman Lluen'
CODE = re.compile(r'\b([SGT][A-Z]{2}[A-Z0-9]{3,4})\b')


def fmt(text):
    t = html.escape(text, quote=False)
    t = CODE.sub(r'<span class="code">\1</span>', t)
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)


def chips(codes):
    return ' '.join(f'<span class="pg">{html.escape(c)}</span>' for c in codes.split(', ')) if codes else ''


def section(num, title, intro=None):
    s = f'<div class="sec"><span class="num">{num}</span><h2>{html.escape(title)}</h2><span class="bar"></span></div>'
    return s + (f'<p class="intro">{fmt(intro)}</p>' if intro else '')


def table(cols, rows, cls=''):
    colgroup = ''.join(f'<col style="width:{w}%">' for _, w in cols)
    head = ''.join(f'<th>{c}</th>' for c, _ in cols)
    body = ''
    for r in rows:
        if isinstance(r, tuple) and r[0] == 'grp':
            body += f'<tr class="grp"><td colspan="{len(cols)}">{fmt(r[1])}</td></tr>'
        else:
            body += '<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>'
    return (f'<table class="t {cls}"><colgroup>{colgroup}</colgroup><thead><tr>{head}</tr></thead>'
            f'<tbody>{body}</tbody></table>')


def aplica(v):
    cls = {'Sí': 'ok', 'Por confirmar': 'tbc', 'No aplica': 'na'}[v]
    return f'<span class="ap {cls}">{v}</span>'


# ------------------------------------------------------------------ contenido
PRINCIPIOS = [
    ('1', 'Validación contra legado', '¿Están todos?',
     'Lo registrado en Banner corresponde con el sistema anterior: los totales cuadran.'),
    ('2', 'Población representativa', '¿Con quiénes probamos?',
     'Una muestra que cubra centros, programas, niveles, grupos y estados de los participantes.'),
    ('3', 'Validación funcional', '¿Funciona en Banner?',
     'El dato no solo existe: se consulta, se interpreta y lo usan los procesos (inscripción, carga, cobro).'),
    ('4', 'Validación por escenarios', '¿Qué puede fallar?',
     'Estudiantes + historia evaluados con CAPP y proyección, más los casos de riesgo propios de los centros.'),
]

TOTALES = [
    ('Personas', 'Participantes y docentes de Centros Empresariales', 'SPAIDEN', 'Sí'),
    ('Estudiantes', 'Participantes por centro, programa y estado', 'SGASTDN', 'Sí'),
    ('Historia académica', 'Cursos aprobados/desaprobados por periodo', 'SHACRSE, SHATCKN', 'Sí'),
    ('Docentes', 'Docentes que dictan en Centros Empresariales', 'SIAINST', 'Sí'),
    ('Saldos', 'Registros y montos pendientes de participantes', 'TSAAREV', 'Sí'),
    ('Egresados', 'Participantes que culminaron el programa (certificados)', 'SHADEGR', 'Por confirmar'),
    ('Tesis', 'No se generan tesis en Centros Empresariales', 'SHAQPNO', 'No aplica'),
]

PASOS = ['Plantilla / sistema anterior', 'Determinar total esperado', 'Obtener total en Banner', 'Comparar y explicar diferencias']

POBLACION = [
    ('Persona', 'Participantes externos, estudiantes de pregrado USS y docentes', 'Distintos tipos de persona y documento',
     'SPAIDEN, GVAADID, SPAEMRG, SOAHOLD'),
    ('Estudiantes', '10–20 participantes por programa de cada centro', 'Distintos niveles, grupos (I01…, X01…, P01…) y estados',
     'SGASTDN, SGASADD'),
    ('Estudiantes', 'Pregrado USS que también lleva Idiomas', 'Programas concurrentes: pregrado + centro', 'SGASTDN'),
    ('Estudiantes', 'Cambios de programa o de centro', 'Cambio dentro del mismo nivel (nivel 5)', 'SGASTDN'),
    ('Historia académica', 'La misma muestra de estudiantes', 'Cursos de periodos de 3 meses del sistema anterior, niveles aprobados y notas',
     'SHACRSE, SHATCKN, SHATERM'),
    ('Currículo', 'Participantes con distinta versión de plan', 'Cambio de versión de plan; equivalencias', 'SMARQCM, SMICRLT'),
    ('Saldos', '5–10 participantes por programa', 'Saldo cero y saldo pendiente', 'TSAAREV'),
    ('Docentes', '5–10 docentes', 'Solo centro y también pregrado; distintos contratos', 'SPAIDEN, SIAINST'),
    ('Egresados', '5–10 participantes que culminaron', 'Distintos programas y años', 'SGASTDN, SHADEGR'),
]

MUESTRA = [
    ('Participante regular, curso en progreso', 3),
    ('Participante nuevo (primer nivel, ej. BASIC I)', 2),
    ('Niveles avanzados (ej. INTERMEDIATE)', 3),
    ('Estudiante de pregrado USS que lleva el centro', 2),
    ('Cambio de programa o de curso', 1),
    ('Retirado o reincorporado', 1),
    ('Con saldo pendiente', 2),
    ('Culminó el programa (certificado)', 1),
    ('Caso particular: curso que empezó en el sistema anterior', 1),
]

FUNCIONAL = [
    ('01 · Persona', 'Identificación, nombres, datos biográficos, documento, direcciones, teléfonos y correos.',
     'SPAIDEN, GVAADID, SOAHOLD', 'Buscar por documento en GOAMTCH: debe encontrar a la persona y **no** permitir duplicarla.'),
    ('01a · Datos adicionales', 'Otros documentos de identidad (pasaporte, carné de extranjería).', 'GVAADID',
     'El documento adicional se ve en SPAIDEN y en GVAADID.'),
    ('01b · Contacto de emergencia', 'Nombre, relación y teléfono del contacto.', 'SPAEMRG', 'Se consulta desde la ficha de la persona.'),
    ('02 · Estudiantes', 'Programa del centro, nivel, campus, periodo de ingreso, estado y atributos; programas concurrentes.',
     'SGASTDN, SGASADD', 'Inscribir al participante en un NRC del periodo actual (SFAREGS) sin errores de programa o estado.'),
    ('03 · Historia académica', 'Cursos, periodos, notas y consistencia del historial; promedio por periodo y acumulado.',
     'SHACRSE, SHATCKN, SHATERM, SMARQCM, SFAPROJ', 'Con BASIC I aprobado: CAPP lo da por cumplido, la proyección ofrece BASIC II y la inscripción lo **permite**.'),
    ('04 · Docentes', 'Datos personales, estatus, tipo de personal, contrato y grados.', 'SPAIDEN, SIAINST',
     'Asignar al docente a un NRC (SSASECT) y ver su carga en SIAASGN.'),
    ('05 · Saldos', 'Conceptos, montos y correspondencia con el sistema anterior.', 'TSAAREV',
     'El saldo en TSAAREV es igual al del sistema anterior (casos con saldo cero y pendiente).'),
    ('06 · Egresados', 'Programa, fecha de culminación y consistencia con la historia.', 'SGASTDN, SHADEGR',
     'Por confirmar si el certificado del centro se registra como grado.'),
]

CAPP = [
    ('Seleccionar la muestra', 'Estudiantes de distintos ciclos, programas y versiones de malla.',
     'La muestra de la sección 3: niveles BASIC e INTERMEDIATE, distintos grupos y cambios de plan.'),
    ('Evaluar cumplimiento (SMARQCM)', 'Contrastar las reglas del plan con la historia migrada.',
     'Ejecutar CAPP a cada participante de la muestra.'),
    ('Analizar el resultado (SMICRLT)', 'Comparar con la situación esperada en el sistema anterior.',
     'Niveles cumplidos y pendientes iguales a los del sistema anterior.'),
    ('Programa, plan y versión', 'Que se aplique la estructura curricular que corresponde.',
     'El participante tiene el plan y la versión de su programa del centro (SGASTDN).'),
    ('Integridad de la historia', 'Cursos, notas y créditos frente a las reglas de equivalencia.',
     'Cursos de periodos de 3 meses bien ubicados, con nota y créditos correctos.'),
    ('Proyección (SFAPROJ)', 'Los cursos que el estudiante puede llevar.',
     'Ofrece el siguiente nivel. Con «Restringir a cursos proyectados» (SOATERM) solo se inscribe lo proyectado.'),
]

ESCENARIOS = [
    ('Curso llevado en un periodo de 3 meses del sistema anterior', 'Queda en un periodo equivocado, duplicado o se pierde.',
     'Comparar periodo y nota del curso: sistema anterior vs Banner.', 'SHACRSE, SHATCKN'),
    ('Nivel aprobado y siguiente nivel', 'El prerrequisito no se reconoce y bloquea la inscripción.',
     'La proyección ofrece el siguiente nivel (ej. BASIC II) y se inscribe en un NRC de prueba.', 'SFAPROJ, SSAPREQ, SFAREGS'),
    ('Estudiante de pregrado que lleva Idiomas', 'Se pisa el programa de pregrado o no se crea el del centro.',
     'Ambos programas activos en SGASTDN, cada uno con su nivel.', 'SGASTDN'),
    ('Curso en progreso al momento de migrar', 'El grupo inició en el sistema anterior y no aparece en Banner.',
     'Ubicar al participante en el NRC y la parte de periodo del grupo.', 'SSASECT, SFAREGS'),
    ('Participante retirado', 'Aparece activo y puede inscribirse.', 'Estado inactivo en SGASTDN; la inscripción debe rechazarse.',
     'SGASTDN, SFAREGS'),
    ('Participante con deuda', 'Saldo distinto o sin retención.', 'Mismo saldo que el sistema anterior; retención si corresponde.',
     'TSAAREV, SOAHOLD'),
    ('Misma persona como alumno, participante o docente', 'Dos IDs para la misma persona.', 'Búsqueda por documento: un solo ID.',
     'GOAMTCH, SPAIDEN'),
    ('Docente de pregrado que dicta en el centro', 'Dos registros o carga incompleta.', 'Un solo registro en SIAINST; carga con todos sus NRC.',
     'SIAINST, SIAASGN'),
]


# ------------------------------------------------------------------ documento
def build():
    b = ['<header class="cover">'
         '<div class="logos"><img src="uss.png" alt="USS"><img src="ellucian.png" alt="Ellucian"></div>'
         '<div class="band"><div class="kicker">Universidad Señor de Sipán · Centros Empresariales</div>'
         '<h1>Validación de la migración</h1>'
         '<div class="sub">Estrategia de Ellucian aplicada a Idiomas, Computación y Emprendimiento</div></div>'
         '<div class="meta">'
         f'<div><span>Elaborado por</span>{AUTHOR}</div>'
         '<div><span>Fecha</span>Septiembre 2026</div>'
         '<div><span>Fuente</span>Estrategia y cronograma R2 de Ellucian (diapositivas 3 a 12)</div>'
         '<div><span>Alcance</span>Datos migrados de Centros Empresariales</div>'
         '</div></header>', new_sections.STATUS]

    # 1. Principios
    b.append(section(1, 'Objetivo y principios'))
    b.append('<div class="quote">La validación no busca solo comprobar que los datos se cargaron, sino demostrar que la '
             'información migrada <b>se comporta en Banner igual que en el sistema anterior</b>.</div>')
    b.append('<div class="cards4">' + ''.join(
        f'<div class="pc"><div class="ph"><span class="pn">{n}</span>{html.escape(t)}</div>'
        f'<div class="pq">{html.escape(q)}</div><p>{fmt(x)}</p></div>' for n, t, q, x in PRINCIPIOS) + '</div>')

    # 2. Contra legado
    b.append(section(2, 'Validación contra legado', 'Primero se cuadran los totales: cuántos registros hay en el sistema anterior y cuántos en Banner.'))
    b.append('<div class="steps4">' + '<i>›</i>'.join(f'<span><b>{i}</b>{html.escape(p)}</span>' for i, p in enumerate(PASOS, 1)) + '</div>')
    rows = [[f'<b>{v}</b>', html.escape(q), chips(p), aplica(a)] for v, q, p, a in TOTALES]
    b.append(table([('Validación', 18), ('Qué se cuenta en Centros Empresariales', 44), ('Dónde se ve en Banner', 22),
                    ('¿Aplica?', 16)], rows, 'tot'))
    b.append('<div class="note">Separe los totales <b>por centro</b> (Idiomas, Computación, Emprendimiento) y <b>por estado</b> '
             'para ubicar rápido las diferencias. La USS puede obtener los totales de Banner con reportes de <b>Insight</b>. '
             'Si la diferencia no es cero, liste los ID faltantes o sobrantes.</div>')

    # 3. Población
    b.append(section(3, 'Población representativa', 'Con quiénes probar: la muestra debe cubrir los casos reales de los centros.'))
    rows = [[f'<b>{d}</b>', html.escape(p), html.escape(e), chips(g)] for d, p, e, g in POBLACION]
    b.append(table([('Dominio', 15), ('Población en Centros Empresariales', 30), ('Escenarios a cubrir', 31),
                    ('Páginas', 24)], rows, 'pob'))
    total = sum(c for _, c in MUESTRA)
    rows = [[html.escape(t), f'<b>{c}</b>'] for t, c in MUESTRA] + [['<b>Total por programa</b>', f'<b>{total}</b>']]
    b.append('<div class="grid2 sample"><div>'
             '<h3>Muestra propuesta <span class="eg">por programa de cada centro</span></h3>'
             f'{table([("Tipo de participante", 80), ("Cant.", 20)], rows, "mue")}</div>'
             '<div class="side">'
             '<div class="note">Con 3 centros y 16 casos por programa, la muestra es pequeña pero cubre los riesgos principales. '
             'Use los <b>mismos participantes</b> para persona, estudiante, historia y saldos: así se validan también las relaciones entre datos.</div>'
             '<div class="note warn">Las cantidades son una <b>propuesta</b> basada en el ejemplo de Ellucian; ajústelas al volumen real de cada programa.</div>'
             '</div></div>')

    # 4. Funcional
    b.append(section(4, 'Validación funcional', 'Por plantilla de migración: qué revisar y qué prueba demuestra que el dato funciona.'))
    rows = [[f'<b>{html.escape(p)}</b>', fmt(q), chips(g), fmt(t)] for p, q, g, t in FUNCIONAL]
    b.append(table([('Plantilla', 17), ('¿Qué se valida?', 31), ('Páginas', 19), ('Prueba funcional', 33)], rows, 'fun'))
    b.append('<p class="foot">07 · Tesis: no aplica a Centros Empresariales. Siempre se valida contra la información del sistema anterior.</p>')

    # 5. Escenarios
    b.append(section(5, 'Validación por escenarios', 'Estudiantes + historia académica: se evalúa con CAPP y la proyección de cursos, y luego se prueban los casos propios de los centros.'))
    b.append('<div class="steps4 capp">' + '<i>›</i>'.join(
        f'<span><b>{i}</b><em>{html.escape(t)}</em><small>{html.escape(c)}</small></span>'
        for i, (t, c) in enumerate([('CAPP · evaluar cumplimiento', 'SMARQCM'), ('Resultados de cumplimiento', 'SMICRLT'),
                                    ('Proyección de cursos', 'SFPPROJ / SFAPROJ')], 1)) + '</div>')
    rows = [[f'<span class="n">{i}</span>', f'<b>{fmt(t)}</b>', fmt(e), fmt(c)] for i, (t, e, c) in enumerate(CAPP, 1)]
    b.append(table([('N°', 5), ('Paso', 22), ('Estrategia Ellucian', 34), ('En Centros Empresariales', 39)], rows, 'cap'))
    b.append('<h3 class="h3gap">Escenarios propios de Centros Empresariales</h3>')
    rows = [[f'<span class="n">{i}</span>', f'<b>{html.escape(e)}</b>', fmt(r), fmt(c), chips(p)]
            for i, (e, r, c, p) in enumerate(ESCENARIOS, 1)]
    b.append(table([('N°', 5), ('Escenario', 24), ('Qué puede fallar', 23), ('Cómo se valida', 28), ('Páginas', 20)], rows, 'esc'))

    b.extend(new_sections.sections(section, table, fmt, chips))
    return '\n'.join(b)


CSS_EXTRA = '''
.meta { grid-template-columns: 1.15fr .75fr 1.5fr 1.2fr; }
.quote { border-left: 4px solid var(--p); background: var(--pl); border-radius: 7px; padding: 8px 12px; font-size: 9.4pt;
         line-height: 1.45; margin: 2px 0 8px; }
.cards4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; break-inside: avoid; }
.pc { border: 1px solid var(--line); border-radius: 9px; padding: 8px 10px 9px; background: #fff; border-top: 4px solid var(--p); }
.pc:nth-child(2) { border-top-color: #A7A1AF; } .pc:nth-child(3) { border-top-color: var(--pd); } .pc:nth-child(4) { border-top-color: var(--lime); }
.ph { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 8.6pt; line-height: 1.25; display: flex; gap: 6px; align-items: flex-start; }
.pn { flex: none; width: 17px; height: 17px; border-radius: 5px; background: var(--p); color: #fff; font-size: 8pt; line-height: 17px; text-align: center; }
.pq { color: var(--pd); font-weight: 700; font-size: 8.2pt; margin: 5px 0 2px; }
.pc p { margin: 0; font-size: 8.1pt; color: #3A3A44; line-height: 1.4; }
.steps4 { display: flex; align-items: center; gap: 5px; margin: 2px 0 7px; flex-wrap: nowrap; }
.steps4 span { flex: 1; background: var(--p); color: #fff; border-radius: 7px; padding: 5px 8px; font-size: 8pt; font-weight: 600;
               display: flex; align-items: center; gap: 6px; }
.steps4 span b { flex: none; width: 16px; height: 16px; border-radius: 8px; background: #fff; color: var(--pd); font-size: 7.4pt;
                 line-height: 16px; text-align: center; }
.steps4 i { color: var(--g); font-style: normal; font-weight: 800; font-size: 12pt; }
.ap { display: inline-block; border-radius: 9px; padding: 0 8px; font-size: 7.5pt; font-weight: 700; white-space: nowrap; }
.ap.ok { background: var(--gl); color: var(--gd); } .ap.tbc { background: #FFF3DC; color: #8A5A00; } .ap.na { background: var(--soft); color: #6B6B76; }
table.tot td:first-child, table.tot th:first-child, table.pob td:first-child, table.pob th:first-child,
table.fun td:first-child, table.fun th:first-child, table.mue td:first-child, table.mue th:first-child { text-align: left; }
table.tot td:last-child, table.tot th:last-child, table.mue td:last-child, table.mue th:last-child { text-align: center; }
table.mue tbody tr:last-child td { background: var(--gl); border-top: 1px solid #D3EAC7; }
table.fun td:last-child { background: #F6FBF3; }
table.fun tbody tr:nth-child(even) td:last-child { background: #EFF7EA; }
table.fun th:last-child { background: var(--g); }
table.reg td { height: 25px; }
.steps4.capp span { flex-direction: row; align-items: center; }
.steps4.capp em { font-style: normal; font-weight: 700; }
.steps4.capp small { margin-left: auto; font-size: 7.3pt; font-weight: 700; background: rgba(255,255,255,.18); border-radius: 4px; padding: 1px 5px; }
.h3gap { margin: 9px 0 4px; }
table.cap td:nth-child(2), table.cap th:nth-child(2) { text-align: left; }
table.reg tbody tr:nth-child(even) td { background: #FCFBFE; }
.grid2.sample { grid-template-columns: 1.25fr 1fr; align-items: start; margin-top: 8px; }
.side .note { margin: 22px 0 8px; }
.side .note + .note { margin-top: 0; }
.note.warn { border-left-color: #E0A100; background: #FFF8E8; }
.legend3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 7px; break-inside: avoid; }
.legend3 div { border: 1px solid var(--line); border-radius: 7px; padding: 6px 9px; font-size: 7.9pt; color: #3A3A44; line-height: 1.4; }
.legend3 .ap { display: table; margin-bottom: 3px; }
.ap.bad { background: #FDE7E7; color: #A11D1D; }
.cards4, .steps4, .quote { break-inside: avoid; }
'''


def main():
    css = open(os.path.join(HERE, 'base.css'), encoding='utf8').read() + CSS_EXTRA + new_sections.CSS
    doc = (f'<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>Validación de la migración</title>'
           f'<style>{css}</style></head><body>{build()}</body></html>')
    open(os.path.join(HERE, 'valid.html'), 'w', encoding='utf8').write(doc)
    print('OK')


if __name__ == '__main__':
    main()
