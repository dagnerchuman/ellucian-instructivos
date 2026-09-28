# -*- coding: utf-8 -*-
"""PPTX editables (formato USS) de los PDF: validación, CAPP explicado, lo que entiendo y diagrama de inicio a fin."""
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
for _d in ('valid', 'capp', 'diag'):
    sys.path.insert(0, os.path.join(HERE, _d))

import build_capp as C          # noqa: E402
import build_diagrama as D      # noqa: E402
import build_ejec as E          # noqa: E402
import build_valid as V         # noqa: E402
import new_sections as N        # noqa: E402
from pptlib import *            # noqa: E402,F401,F403
from ussdeck import G, build_cover, build_structure, finalize, para, parse, save, set_flow_boxes  # noqa: E402

OUTDIR = os.path.join(HERE, 'entregables')
HOY = date(2026, 9, 25)


def dd(d):
    return f'{d.day:02d}/{d.month:02d}'


def num(i):
    return {'text': str(i), 'algn': 'ctr', 'bold': True, 'color': PURD}


def aplica(a):
    fill, color = {'Sí': (GRNL, GRND), 'Por confirmar': (AMBP, AMBD), 'No aplica': (GRAYL, MUT), 'No': (GRAYL, MUT)}[a]
    return {'text': a, 'fill': fill, 'color': color, 'bold': True, 'algn': 'ctr'}


def formula(S, x, y, w, h, sz=1800):
    S.add(shape_xml(S.nid(), x, y, w, h, geom='roundRect', adj=6000, fill=PURL, line=PURB,
                    paras=p_xml('% de correctitud', 1400, color=PURD, bold=True, font='Montserrat'), ins=(160000, 130000, 160000, 80000)))
    mid = y + h * 0.53
    S.add(shape_xml(S.nid(), x, mid - 430000, w, 380000, paras=p_xml('datos conformes', sz, algn='ctr', bold=True), anchor='b', ins=(0, 0, 0, 0)))
    S.add(poly_xml(S.nid(), [(x + w * 0.18, mid), (x + w * 0.82, mid)], color=INK, w=19050, arrow=False))
    S.add(shape_xml(S.nid(), x, mid + 50000, w, 380000, paras=p_xml('datos revisados', sz, algn='ctr', bold=True), anchor='t', ins=(0, 0, 0, 0)))
    S.add(shape_xml(S.nid(), x, y + h - 420000, w, 360000,
                    paras=p_xml('Los «Observado» no cuentan como correctos hasta que la excepción esté aprobada.', 1000, algn='ctr', color=MUT),
                    anchor='ctr', ins=(150000, 0, 150000, 0)))


def results_legend(S, y=None, h=1150000):
    y = S.y if y is None else y
    res = [('Conforme', GRNL, GRND, 'Igual al sistema anterior y funciona en Banner.'),
           ('Observado', AMBP, AMBD, 'Diferencia menor o explicada; se documenta y se aprueba.'),
           ('No conforme', REDL, RED, 'Falta, se duplica o bloquea un proceso: va al Issue log.')]
    gap = 160000
    cw = (XW - 2 * gap) / 3
    for i, (lab, fl, col, desc) in enumerate(res):
        paras = p_xml(lab, 1550, color=col, bold=True, spc_after=400) + p_xml(desc, 1400, color=SOFT)
        S.add(shape_xml(S.nid(), X0 + i * (cw + gap), y, cw, h, geom='roundRect', adj=8000, fill=fl, line=LINE, paras=paras,
                        ins=(160000, 110000, 160000, 90000), name='Resultado'))
    S.y = y + h + 100000


def run_deck(name, work, plan, title):
    kinds = [k for k, _ in plan]
    u, paths = build_structure(os.path.join(HERE, work), kinds)
    for (kind, fn), path in zip(plan, paths):
        if fn:
            fn(path)
    out = os.path.join(OUTDIR, name + '.pptx')
    finalize(u, out, title)
    print('OK', out, len(paths), 'diapositivas')
    return out


# =================================================================== A. VALIDACIÓN DE LA MIGRACIÓN
def a_cover(p):
    build_cover(p, 'VALIDACIÓN DE LA MIGRACIÓN', 'CENTROS EMPRESARIALES',
                'Estrategia de Ellucian aplicada a Idiomas, Computación y Emprendimiento')


def a_situacion(p):
    S = Slide(p, 'SITUACIÓN AL 25/09/2026')
    S.text('Revisiones de la USS según el cronograma de la Migración R2 presentado por Ellucian.')
    cards = [('EN REVISIÓN · PROD', ORG, ['**Personas:** 24/09 – 27/09', '**Documento de identidad:** 25/09 – 27/09',
                                         '**Contacto de emergencia:** 25/09 – 27/09']),
             ('SIGUIENTE · PROD', PUR, ['**Docentes:** carga 28/09 – 30/09', '**Revisión de docentes:** 30/09 – 02/10',
                                       '**Carga LD01 y matriz de seguridad:** 30/09 – 02/10']),
             ('LUEGO · TEST', GRN, ['**Clonación a TEST:** 05/10 – 09/10', '**Estudiantes a Escuela de procedencia:** 12/10 – 16/11',
                                    '**Pruebas integrales:** 16/11 – 26/12'])]
    gap, hh, bh = 200000, 480000, 2250000
    cw = (XW - 2 * gap) / 3
    y = S.y + 60000
    for i, (h, col, lines) in enumerate(cards):
        x = X0 + i * (cw + gap)
        S.add(shape_xml(S.nid(), x, y, cw, hh, geom='roundRect', adj=18000, fill=col,
                        paras=p_xml(h, 1500, algn='ctr', color='FFFFFF', bold=True, font='Montserrat'), anchor='ctr'))
        body = ''.join(p_xml(t, 1600, spc_after=1000) for t in lines)
        S.add(shape_xml(S.nid(), x, y + hh + 60000, cw, bh, geom='roundRect', adj=6000, fill='FFFFFF', line=LINE, paras=body,
                        ins=(200000, 220000, 200000, 100000)))
    S.y = y + hh + 60000 + bh + 250000
    S.note('Detalle de fechas, horas y muestra en las diapositivas «Cronograma Migración R2» y «Plan de revisión de los centros».', sz=1350)
    S.save()


def a_principios(p):
    S = Slide(p, 'OBJETIVO Y PRINCIPIOS')
    S.note('La validación no busca solo comprobar que los datos se cargaron, sino demostrar que la información migrada '
           '**se comporta en Banner igual que en el sistema anterior**.', kind='purple', sz=1700, gap=250000)
    acc = [PUR, 'A7A1AF', PURD, '92D050']
    gap = 170000
    cw = (XW - 3 * gap) / 4
    for i, (n, t, q, x) in enumerate(V.PRINCIPIOS):
        S.card(X0 + i * (cw + gap), S.y, cw, 3250000, t, question=q, text=x, accent=acc[i], num=n, tsz=1850, sz=1650)
    S.save()


def a_legado(p):
    S = Slide(p, 'VALIDACIÓN CONTRA LEGADO')
    S.text('Primero se cuadran los totales: cuántos registros hay en el sistema anterior y cuántos en Banner.')
    S.chevrons([(t, None) for t in V.PASOS], h=560000, sz=1300)
    rows = [[f'**{v}**', q, g, aplica(a)] for v, q, g, a in V.TOTALES]
    S.table([18, 44, 22, 16], ['Validación', 'Qué se cuenta en Centros Empresariales', 'Dónde se ve en Banner', '¿Aplica?'], rows, reserve=950000)
    S.note('Separe los totales **por centro** (Idiomas, Computación, Emprendimiento) y **por estado** para ubicar rápido las diferencias. '
           'La USS puede obtener los totales de Banner con reportes de **Insight**. Si la diferencia no es cero, liste los ID faltantes o sobrantes.',
           sz=1250)
    S.save()


def a_poblacion(p):
    S = Slide(p, 'POBLACIÓN REPRESENTATIVA')
    S.text('Con quiénes probar: la muestra debe cubrir los casos reales de los centros.')
    rows = [[f'**{d}**', po, e, g] for d, po, e, g in V.POBLACION]
    S.table([15, 30, 31, 24], ['Dominio', 'Población en Centros Empresariales', 'Escenarios a cubrir', 'Páginas'], rows)
    S.save()


def a_muestra(p):
    S = Slide(p, 'MUESTRA PROPUESTA POR PROGRAMA')
    S.text('Tipos de participante a revisar en cada programa de los centros.')
    rows = [[t, {'text': str(c), 'algn': 'ctr', 'bold': True}] for t, c in V.MUESTRA]
    total = sum(c for _, c in V.MUESTRA)
    rows.append([{'text': '**Total por programa**', 'fill': GRNL}, {'text': str(total), 'algn': 'ctr', 'bold': True, 'fill': GRNL}])
    lw, y0 = 6300000, S.y
    S.table([80, 20], ['Tipo de participante', 'Cantidad'], rows, w=lw)
    rx, rw = X0 + lw + 300000, XW - lw - 300000
    S.note('Con 3 centros y 16 casos por programa, la muestra es pequeña pero cubre los riesgos principales. Use los **mismos '
           'participantes** para persona, estudiante, historia y saldos: así se validan también las relaciones entre datos.',
           x=rx, w=rw, y=y0, sz=1450, gap=250000)
    S.note('Las cantidades son una **propuesta** basada en el ejemplo de Ellucian; ajústelas al volumen real de cada programa.',
           kind='warn', x=rx, w=rw, sz=1450)
    S.save()


def a_funcional(part):
    def f(p):
        S = Slide(p, f'VALIDACIÓN FUNCIONAL ({part}/2)')
        if part == 1:
            S.text('Por plantilla de migración: qué revisar y qué prueba demuestra que el dato funciona.')
        chunk = V.FUNCIONAL[:4] if part == 1 else V.FUNCIONAL[4:]
        rows = [[f'**{pl}**', q, g, {'text': t, 'fill': 'F6FBF3'}] for pl, q, g, t in chunk]
        S.table([17, 31, 19, 33], ['Plantilla', '¿Qué se valida?', 'Páginas', {'text': 'Prueba funcional', 'fill': GRN}], rows,
                reserve=400000 if part == 2 else 0)
        if part == 2:
            S.text('07 · Tesis: no aplica a Centros Empresariales. Siempre se valida contra la información del sistema anterior.', sz=1250)
        S.save()
    return f


def a_capp(p):
    S = Slide(p, 'VALIDACIÓN POR ESCENARIOS: CAPP')
    S.text('Estudiantes + historia académica: se evalúa con CAPP y la proyección de cursos; luego se prueban los casos propios de los centros.')
    S.chevrons([('CAPP · evaluar cumplimiento', 'SMARQCM'), ('Resultados de cumplimiento', 'SMICRLT'),
                ('Proyección de cursos', 'SFPPROJ / SFAPROJ')], h=650000, sz=1350)
    rows = [[num(i), f'**{t}**', e, c] for i, (t, e, c) in enumerate(V.CAPP, 1)]
    S.table([5, 22, 34, 39], ['N°', 'Paso', 'Estrategia Ellucian', 'En Centros Empresariales'], rows)
    S.save()


def a_escenarios(p):
    S = Slide(p, 'ESCENARIOS PROPIOS DE LOS CENTROS')
    S.text('Casos de Centros Empresariales donde es más probable encontrar errores.')
    rows = [[num(i), f'**{e}**', r, c, g] for i, (e, r, c, g) in enumerate(V.ESCENARIOS, 1)]
    S.table([5, 24, 23, 28, 20], ['N°', 'Escenario', 'Qué puede fallar', 'Cómo se valida', 'Páginas'], rows)
    S.save()


def a_criterios(p):
    S = Slide(p, 'CRITERIOS DE ACEPTACIÓN')
    S.text('La revisión se acepta cuando los datos obligatorios están, los formatos son correctos, no hay duplicados ni inconsistencias '
           'relevantes, las relaciones están íntegras y las conciliaciones están dentro de la tolerancia. Toda excepción se documenta, '
           'justifica y aprueba antes de la aceptación final.', sz=1350)
    rows = [[num(i), f'**{c}**', q, {'text': u, 'algn': 'ctr', 'bold': True, 'color': PURD}, e]
            for i, (c, q, u, e) in enumerate(N.CRITERIOS, 1)]
    S.table([5, 16, 31, 11, 37], ['N°', 'Criterio', 'Qué significa', 'Umbral mínimo', 'Ejemplo en Centros Empresariales'], rows)
    S.save()


def a_correctitud(p):
    S = Slide(p, '% DE CORRECTITUD')
    y, fw, fh = S.y + 50000, 4300000, 2150000
    formula(S, X0, y, fw, fh)
    rx, rw = X0 + fw + 300000, XW - fw - 300000
    S.note(['Con muestras pequeñas los umbrales casi no dejan margen.',
            'Con **48 participantes**, **Unicidad (mínimo 99,5%)** significa **cero duplicados**.',
            'Con 10 campos por participante (480 datos), **Exactitud (mínimo 98%)** admite como máximo **9 datos con error**, '
            'e Integridad (mínimo 99%), como máximo 4.'], x=rx, w=rw, y=y, h=fh, sz=1500)
    S.y = y + fh + 250000
    S.text('Resultado de cada dato revisado', sz=1450, color=INK, bold=True, gap=80000)
    results_legend(S)
    S.save()


def a_tiempos(p):
    S = Slide(p, 'TIEMPOS DE VALIDACIÓN')
    S.text('Ellucian estima **86 minutos por alumno** (1,4 h). Sin tesis, en Centros Empresariales son **83 minutos por participante**.',
           color=INK)
    rows = [[f'**{pl}**', g, {'text': t, 'algn': 'ctr'}, {'text': str(m), 'algn': 'ctr', 'bold': True}, aplica(a)]
            for pl, g, t, m, a in N.TIEMPOS]
    rows.append([{'text': '**Total**', 'fill': GRNL}, {'text': '', 'fill': GRNL},
                 {'text': 'Ellucian: 86 min (1,4 h)', 'fill': GRNL, 'algn': 'ctr'},
                 {'text': '83', 'fill': GRNL, 'algn': 'ctr', 'bold': True}, {'text': 'Sin tesis', 'fill': GRNL, 'algn': 'ctr'}])
    S.table([22, 38, 18, 8, 14], ['Plantilla', 'Páginas', 'Minutos', 'Min', 'Aplica a CE'], rows)
    S.save()


def a_cronograma(p):
    S = Slide(p, 'CRONOGRAMA MIGRACIÓN R2')
    T0, T1 = date(2026, 9, 1), date(2027, 1, 1)
    span = (T1 - T0).days
    CX0, CX1 = X0 + 2950000, XR - 1050000
    DAY = (CX1 - CX0) / span

    def X(d):
        return CX0 + (d - T0).days * DAY

    lx, ly = X0, 880000
    for col, lab in ((PUR, 'Carga en Banner (Ellucian/USS)'), (ORG, 'Revisión y pruebas (USS)'), (AQU, 'Otras actividades')):
        S.add(shape_xml(S.nid(), lx, ly + 50000, 320000, 90000, geom='roundRect', adj=30000, fill=col, name='Leyenda'))
        tw = text_w(lab, 1100) + 120000
        S.add(shape_xml(S.nid(), lx + 380000, ly, tw, 190000, paras=p_xml(lab, 1100, color=MUT), anchor='ctr', ins=(0, 0, 0, 0)))
        lx += 380000 + tw + 250000
    for m, lab in ((9, 'Setiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')):
        a, b = X(date(2026, m, 1)), X(date(2026 + (m == 12), m % 12 + 1, 1))
        S.add(shape_xml(S.nid(), a, 1110000, b - a, 190000, paras=p_xml(lab, 1050, algn='ctr', color=MUT, bold=True), anchor='ctr',
                        ins=(0, 0, 0, 0)))
    RY0, RYE = 1480000, 5820000
    RH = (RYE - RY0) / len(N.CRONO)
    for name, env, fill in (('PROD', 'PROD', 'F6F2FA'), ('TEST', 'TEST', 'F3FAF6')):
        idx = [i for i, e in enumerate(N.CRONO) if e[1] == env]
        y0, y1 = RY0 + idx[0] * RH, RY0 + (idx[-1] + 1) * RH
        S.add(shape_xml(S.nid(), X0 + 560000, y0, XR - X0 - 560000, y1 - y0, fill=fill, name='Ambiente'))
        S.add(poly_xml(S.nid(), [(X0 + 500000, y0 + 40000), (X0 + 500000, y1 - 40000)], color=PURD, w=28575, arrow=False))
        S.add(shape_xml(S.nid(), X0, y0, 460000, y1 - y0, paras=p_xml(name, 1000, algn='ctr', color=PURD, bold=True, font='Montserrat'),
                        anchor='ctr', ins=(0, 0, 0, 0)))
    for d_ in (date(2026, 9, 1), date(2026, 10, 1), date(2026, 11, 1), date(2026, 12, 1), date(2027, 1, 1)):
        S.add(poly_xml(S.nid(), [(X(d_), 1320000), (X(d_), RYE)], color='E1D8EA', w=6350, arrow=False))
    bh = 95000
    for i, e in enumerate(N.CRONO):
        y = RY0 + i * RH
        cy = y + RH / 2
        faded = e[7] == 'No aplica'
        S.add(shape_xml(S.nid(), X0 + 600000, y, 2300000, RH, paras=p_xml(e[0], 1050, color='A3A3AD' if faded else INK, bold=not faded),
                        anchor='ctr', ins=(0, 0, 0, 0)))
        bars = []
        if e[2]:
            bars.append((e[2], AQU if e[4] == 'o' else PUR))
        if e[3]:
            bars.append((e[3], ORG))
        ys = [cy - bh - 12000, cy + 12000] if len(bars) == 2 else [cy - bh / 2]
        for ((a, b), col), by in zip(bars, ys):
            if faded:
                col = {PUR: 'D4BCEA', ORG: 'F7C3AE'}.get(col, col)
            x0, x1 = X(a), X(b) + DAY
            S.add(shape_xml(S.nid(), x0, by, max(x1 - x0, 40000), bh, geom='roundRect', adj=30000, fill=col, name='Barra'))
        rng = e[3] or e[2]
        lab = 'No aplica a CE' if faded else f'{dd(rng[0])} – {dd(rng[1])}'
        S.add(shape_xml(S.nid(), X(rng[1]) + DAY + 50000, ys[-1] + bh / 2 - 90000, 1000000, 180000, paras=p_xml(lab, 900, color=MUT),
                        anchor='ctr', ins=(0, 0, 0, 0)))
    xh = X(HOY) + DAY / 2
    S.add(poly_xml(S.nid(), [(xh, 1330000), (xh, RYE)], color=INK, w=12700, dash='dash', arrow=False))
    S.add(shape_xml(S.nid(), xh - 300000, 1320000, 600000, 140000, geom='roundRect', adj=30000, fill=INK,
                    paras=p_xml('Hoy 25/09', 700, algn='ctr', color='FFFFFF', bold=True), anchor='ctr', ins=(0, 0, 0, 0)))
    S.save()


def estado(e):
    if e[7] == 'No aplica':
        return {'text': 'No aplica', 'fill': GRAYL, 'color': MUT, 'bold': True, 'algn': 'ctr'}
    ini, fin = e[3]
    if HOY < ini:
        return {'text': 'Próxima', 'fill': PURL, 'color': PURD, 'bold': True, 'algn': 'ctr'}
    if HOY <= fin:
        return {'text': 'En revisión', 'fill': 'FFE6DA', 'color': 'A63F12', 'bold': True, 'algn': 'ctr'}
    return {'text': 'Cerrada', 'fill': GRAYL, 'color': MUT, 'bold': True, 'algn': 'ctr'}


def a_plan(p):
    S = Slide(p, 'PLAN DE REVISIÓN DE LOS CENTROS')
    S.text('Horas de revisión = minutos por caso × muestra. Muestra propuesta: 16 participantes × 3 centros = 48; 10 docentes; '
           '5 egresados por centro.', sz=1300)
    rows, tot = [], 0
    for e in N.CRONO:
        if e[3] is None or e[4] == 'p':
            continue
        h = (e[5] * e[6] / 60) if e[7] != 'No aplica' else None
        tot += h or 0
        ini, fin = e[3]
        c = lambda v: {'text': v, 'algn': 'ctr'}
        rows.append([f'**{e[0]}**', c(e[1]), c(f'{dd(ini)} – {dd(fin)}'), c(str(e[5]) if h is not None else '—'),
                     c(str(e[6]) if h is not None else '—'),
                     {'text': f'{h:.1f}'.replace('.', ',') if h is not None else '—', 'algn': 'ctr', 'bold': True}, estado(e)])
    g = {'fill': GRNL}
    rows.append([dict(g, text='**Total**'), dict(g, text=''), dict(g, text=''), dict(g, text=''), dict(g, text=''),
                 dict(g, text=f'{tot:.1f}'.replace('.', ','), algn='ctr', bold=True), dict(g, text='')])
    S.table([26, 10, 16, 12, 11, 10, 15], ['Etapa', 'Ambiente', 'Revisión USS', 'Min por caso', 'Muestra CE', 'Horas CE', 'Al 25/09'],
            rows, reserve=900000)
    S.note('**Punto crítico: Historia académica.** Son unas 34 horas de revisión en solo 3 días (28 al 30 de octubre), unas 11 horas '
           'por día. Conviene asignar desde ya al menos **2 revisores** a tiempo completo para Centros Empresariales.', kind='warn', sz=1250)
    S.save()


def a_resp(p):
    S = Slide(p, 'RESPONSABILIDADES DE LA USS')
    S.text('Cómo las cumple Centros Empresariales con esta presentación y la planilla Excel que la acompaña.')
    donde = {'PDF · sección 4': 'Validación funcional'}
    rows = [[num(i), r, c, {'text': donde.get(h, h), 'algn': 'ctr', 'bold': True, 'color': GRND, 'fill': GRNL}]
            for i, (r, c, h) in enumerate(N.RESP, 1)]
    S.table([5, 40, 37, 18], ['N°', 'Responsabilidad (Ellucian)', 'Cómo se cumple en Centros Empresariales', 'Dónde'], rows)
    S.save()


def deck_validacion():
    plan = [('cover', a_cover), ('text', a_situacion), ('text', a_principios), ('text', a_legado), ('text', a_poblacion),
            ('text', a_muestra), ('text', a_funcional(1)), ('text', a_funcional(2)), ('text', a_capp), ('text', a_escenarios),
            ('text', a_criterios), ('text', a_correctitud), ('text', a_tiempos), ('text', a_cronograma), ('text', a_plan),
            ('text', a_resp), ('close', None)]
    return run_deck('VALIDACIÓN DE LA MIGRACIÓN - CENTROS EMPRESARIALES', 'bA', plan, 'Validación de la migración - Centros Empresariales')


# =================================================================== B. CAPP EXPLICADO
def b_cover(p):
    build_cover(p, 'CAPP EXPLICADO', 'CENTROS EMPRESARIALES', 'Qué es, cómo se ejecuta y por qué es clave para validar la migración')


def b_frase(p):
    S = Slide(p, 'CAPP EN UNA FRASE')
    S.note(['**CAPP es el auditor del plan de estudios en Banner.**',
            'Compara lo que el estudiante ya aprobó (su historia académica) con lo que exige su malla y dice **qué cumplió y qué le falta**.'],
           kind='purple', sz=2000, gap=300000)
    S.text('Banner lo usa en:', sz=1600, color=INK, bold=True, gap=140000)
    usos = [('Inscripción de asignaturas', 'La proyección de cursos toma el resultado del CAPP.'),
            ('Cierre de periodo', 'Se ejecuta el CAPP masivo (SMRBCMP).'),
            ('Procesos de graduación', 'Se verifica que cumplió todo el plan.'),
            ('Ajuste de historia académica', 'Se revisa el avance después del ajuste.')]
    gap = 170000
    cw = (XW - 3 * gap) / 4
    for i, (t, x) in enumerate(usos):
        S.card(X0 + i * (cw + gap), S.y, cw, 1850000, t, text=x, num=i + 1, tsz=1550, sz=1450)
    S.y += 1850000 + 180000
    S.text('CAPP: Curriculum, Advising and Program Planning, el módulo de avance curricular de Banner.', sz=1200)
    S.save()


def b_flujo(p):
    t = parse(p)
    set_title2(t, 'CÓMO FUNCIONA CAPP')
    save(t, p)
    set_flow_boxes(p, [('Verificar la historia académica', 'SHACRSE'), ('Verificar programa y catálogo', 'SGASTDN'),
                       ('Reglas del plan en CAPP', 'SMAPROG, SMAAREA', 1300), ('Evaluar el cumplimiento', 'SMARQCM'),
                       ('Revisar el resultado', 'SMICRLT'), ('Proyectar los cursos', 'SFPPROJ, SFAPROJ', 1300),
                       ('Inscribir lo proyectado', 'SFAREGS')],
                   note=[para(G('Entradas (1 a 3):'), ' historia académica, plan del estudiante y reglas de la malla.'),
                         para(G('Evaluación y usos (4 a 7):'), ' resultado Cumple / No cumple, proyección e inscripción.')],
                   highlight=(3, 4))


def b_ejemplo(p):
    S = Slide(p, 'EJEMPLO EN CENTROS EMPRESARIALES')
    S.text('Ilustrativo: depende de cómo estén configuradas en CAPP las reglas del programa de Idiomas.')
    y0, lw = S.y, 6500000
    rows = [[f'**{a}**', c, h, {'text': 'Cumple' if r == 'ok' else 'No cumple', 'algn': 'ctr', 'bold': True,
                                  'color': GRND if r == 'ok' else RED, 'fill': GRNL if r == 'ok' else REDL}]
            for a, c, h, r in C.EJEMPLO]
    S.table([26, 28, 26, 20], ['Área', 'Curso', 'Historia académica', 'CAPP'], rows, w=lw, hi=1600)
    rx, rw = X0 + lw + 300000, XW - lw - 300000
    boxes = [('PROYECCIÓN', '**BASIC III**', 'purple'),
             ('INSCRIPCIÓN', 'Solo puede inscribirse en un NRC de **BASIC III** del grupo del mes.', 'purple'),
             ('SI MIGRÓ MAL', 'Si BASIC II no llegó a la historia, CAPP lo marca pendiente, lo proyecta otra vez y el participante '
                              '**no podrá avanzar**.', 'warn')]
    S.y = y0
    for lab, txt, kind in boxes:
        S.note([[(lab, True, MUT)], txt], kind=kind, x=rx, w=rw, sz=1450, gap=180000, anchor='t')
    S.save()


def b_ejecuta(p):
    S = Slide(p, 'CÓMO SE EJECUTA CAPP')
    S.text('Procedimiento del instructivo 7.2.4 (individual) y del 5.4 (proyección).')
    rows = [[num(i), {'text': g, 'algn': 'ctr'}, t] for i, (g, t) in enumerate(C.PASOS, 1)]
    S.table([5, 13, 82], ['N°', 'Página', 'Qué hacer'], rows, reserve=400000)
    S.text('Masivo: SMRBCMP desde GJAPCTL (impresora DATABASE); el resultado se revisa en GJIREVO (archivo .lis).', sz=1250)
    S.save()


def b_previa(p):
    S = Slide(p, 'CONFIGURACIÓN PREVIA DE CAPP')
    S.text('La hace el equipo funcional; si falta, CAPP no funciona.')
    S.table([22, 78], ['Página', 'Qué debe estar listo'], [[g, t] for g, t in C.PREVIOS], hi=1600)
    S.save()


def b_validacion(p):
    S = Slide(p, 'CAPP EN LA VALIDACIÓN')
    S.text('Si CAPP da el mismo resultado que el sistema anterior, la historia, la malla y las reglas migraron bien. Se valida en TEST, '
           'en la etapa de Historia académica (revisión del 28 al 30 de octubre).', sz=1450)
    steps = [('Elegir la muestra', 'Distintos niveles, programas y versiones de malla.'),
             ('Ejecutar CAPP', 'SMARQCM a cada estudiante de la muestra (3 min).'),
             ('Comparar el resultado', 'SMICRLT contra la situación en el sistema anterior (10 min).'),
             ('Proyectar', 'SFPPROJ (3 min) y revisar en SFAPROJ que ofrezca lo correcto (10 min).'),
             ('Registrar', 'Conforme u observación en la planilla; si difiere, al Issue log.')]
    y = S.y
    S.chevrons([(t, None) for t, _ in steps], h=580000, sz=1300)
    gap = 40000
    cw = (XW - 4 * gap) / 5
    for i, (_, d) in enumerate(steps):
        S.add(shape_xml(S.nid(), X0 + i * (cw + gap) + 30000, S.y, cw - 60000, 1950000, geom='roundRect', adj=8000, fill=PURL,
                        line=PURB, paras=p_xml(d, 1600), ins=(130000, 140000, 130000, 60000)))
    S.y += 1950000 + 250000
    S.note('Son **26 de los 42 minutos** que Ellucian estima para revisar la historia académica de cada estudiante.', sz=1450)
    S.save()


def b_causas(p):
    S = Slide(p, 'SI EL RESULTADO NO COINCIDE')
    S.text('Causas probables y dónde revisar.')
    S.table([30, 44, 26], ['Lo que se ve', 'Causa probable', 'Dónde revisar'], [[f'**{s}**', c, g] for s, c, g in C.CAUSAS])
    S.save()


def b_glosario(p):
    S = Slide(p, 'GLOSARIO PARA EL ZOOM')
    half = (len(C.GLOSARIO) + 1) // 2
    gw, y0 = (XW - 250000) / 2, S.y
    left = [[f'**{t}**', d] for t, d in C.GLOSARIO[:half]]
    right = [[f'**{t}**', d] for t, d in C.GLOSARIO[half:]]
    hd = ['Término', 'Significa']
    sz = min(fit_sz(gw, [34, 66], hd, left, y0, YB), fit_sz(gw, [34, 66], hd, right, y0, YB))
    S.table([34, 66], hd, left, w=gw, y=y0, sz=sz)
    S.table([34, 66], hd, right, x=X0 + gw + 250000, w=gw, y=y0, sz=sz)
    S.save()


def deck_capp():
    plan = [('cover', b_cover), ('text', b_frase), ('flow', b_flujo), ('text', b_ejemplo), ('text', b_ejecuta), ('text', b_previa),
            ('text', b_validacion), ('text', b_causas), ('text', b_glosario), ('close', None)]
    return run_deck('CAPP EXPLICADO - CENTROS EMPRESARIALES', 'bB', plan, 'CAPP explicado - Centros Empresariales')


# =================================================================== C. MIGRACIÓN R2: LO QUE ENTIENDO
def c_cover(p):
    build_cover(p, 'MIGRACIÓN R2', 'CENTROS EMPRESARIALES', 'Lo que entiendo: resumen para ponerse al día')


def c_ideas(p):
    S = Slide(p, 'LO ESENCIAL EN CUATRO IDEAS')
    gap = 200000
    cw = (XW - gap) / 2
    ch = (YB - S.y - gap - 50000) / 2
    y0 = S.y + 30000
    for i, (t, x) in enumerate(E.IDEAS):
        c, r = i % 2, i // 2
        S.card(X0 + c * (cw + gap), y0 + r * (ch + gap), cw, ch, t, text=x, accent=PUR if i < 3 else '92D050', num=i + 1,
               tsz=1800, sz=1600, fill='FFFFFF' if i < 3 else GRNL)
    S.save()


def c_donde(p):
    S = Slide(p, 'DÓNDE ESTAMOS')
    S.text('Revisiones de la USS según el cronograma de Ellucian, al 25/09/2026.')
    lab = {'now': ('En revisión', 'FFE6DA', 'A63F12'), 'soon': ('Próxima', PURL, PURD), 'crit': ('Punto crítico', REDL, RED)}
    rows = [[f'**{e}**', {'text': a, 'algn': 'ctr'}, {'text': f, 'algn': 'ctr'},
             {'text': lab[s][0], 'fill': lab[s][1], 'color': lab[s][2], 'bold': True, 'algn': 'ctr'}] for e, a, f, s in E.CRONO]
    S.table([50, 12, 22, 16], ['Etapa', 'Ambiente', 'Revisión (USS)', 'Estado'], rows)
    S.save()


def c_toca(p):
    S = Slide(p, 'QUÉ LE TOCA A LOS CENTROS')
    S.text('Tareas de Centros Empresariales en la validación de la migración.')
    tool = {'PDF · CAPP explicado': 'CAPP explicado', 'Este documento': 'Esta presentación'}
    rows = [[num(i), t, {'text': tool.get(h, h), 'algn': 'ctr', 'bold': True, 'color': GRND, 'fill': GRNL}]
            for i, (t, h) in enumerate(E.TOCA, 1)]
    S.table([5, 73, 22], ['N°', 'Tarea', 'Herramienta'], rows, hi=1600)
    S.save()


def c_decide(p):
    S = Slide(p, 'CÓMO SE DECIDE SI ESTÁ BIEN')
    S.text('La revisión se aprueba si cada criterio llega a su mínimo y las excepciones están aprobadas por el comité.')
    y0, lw = S.y, 6300000
    rows = [[f'**{c}**', d, {'text': u, 'algn': 'ctr', 'bold': True, 'color': PURD}] for c, d, u in E.CRITERIOS]
    th = S.table([36, 44, 20], ['Criterio', 'En pocas palabras', 'Mínimo'], rows, w=lw, hi=1600)
    rx, rw = X0 + lw + 300000, XW - lw - 300000
    formula(S, rx, y0, rw, 1750000, sz=1600)
    S.y = y0 + 1750000 + 150000
    S.note('Con 48 participantes, **Unicidad** exige **cero duplicados**. Los datos «Observado» solo cuentan como correctos '
           'cuando el comité aprueba la excepción.', x=rx, w=rw, sz=1350)
    S.save()


def c_preguntas(p):
    S = Slide(p, 'PREGUNTAS PARA EL ZOOM')
    S.text('En orden de prioridad para Centros Empresariales.')
    rows = [[num(i), f'**{t}**', q] for i, (t, q) in enumerate(E.PREGUNTAS, 1)]
    S.table([5, 15, 80], ['N°', 'Tema', 'Pregunta'], rows)
    S.save()


def c_material(p):
    S = Slide(p, 'MATERIAL PREPARADO HASTA HOY')
    rows = [[f'**{d}**', u] for d, u in E.DOCS] + [['**Diagrama de inicio a fin**', 'Cómo usarían Banner los centros, paso a paso.']]
    S.table([34, 66], ['Documento', 'Para qué sirve'], rows, reserve=400000)
    S.text('Este resumen refleja lo entendido de la presentación de Ellucian y los instructivos; se actualizará con el resumen del Zoom.',
           sz=1250)
    S.save()


def deck_ejec():
    plan = [('cover', c_cover), ('text', c_ideas), ('text', c_donde), ('text', c_toca), ('text', c_decide), ('text', c_preguntas),
            ('text', c_material), ('close', None)]
    return run_deck('MIGRACIÓN R2 - LO QUE ENTIENDO - CENTROS EMPRESARIALES', 'bC', plan,
                    'Migración R2: lo que entiendo - Centros Empresariales')


# =================================================================== D. DIAGRAMA DE INICIO A FIN
def d_cover(p):
    build_cover(p, 'DE INICIO A FIN', 'CENTROS EMPRESARIALES', 'Cómo usarían Banner Idiomas, Computación y Emprendimiento')


def d_diagrama(p):
    S = Slide(p, 'DE INICIO A FIN EN BANNER')
    LI = {k: i for i, (_, k) in enumerate(D.LANES)}
    SI = {s[0]: s for s in D.STEPS}
    LW, BW, BH = 950000, 1330000, 560000
    CW = (XW - LW) / len(D.PHASES)
    PHY, PHH, CORR = 870000, 330000, 1290000
    LY0, LH = 1370000, 640000
    off_k = (CW - BW) / (D.CW - D.BW)

    def box(n):
        _, lane, col, *_ = SI[n]
        return X0 + LW + col * CW + (CW - BW) / 2, LY0 + LI[lane] * LH + (LH - BH) / 2

    def pts(a, b, style, off):
        ax, ay = box(a)
        bx, by = box(b)
        acx, acy, bcx, bcy = ax + BW / 2, ay + BH / 2, bx + BW / 2, by + BH / 2
        gx = ax + BW + (CW - BW) / 2 + off * off_k
        if style == 'side':
            return [(ax + BW, acy), (gx, acy), (gx, bcy), (bx + BW, bcy)]
        if abs(ax - bx) < 1:
            return [(acx, ay + BH), (acx, by)] if by > ay else [(acx, ay), (acx, by + BH)]
        if abs(ay - by) < 1:
            return [(ax + BW, acy), (bx, bcy)]
        return [(ax + BW, acy), (gx, acy), (gx, bcy), (bx, bcy)]

    for i, (name, _) in enumerate(D.LANES):
        y = LY0 + i * LH
        S.add(shape_xml(S.nid(), X0, y, XW, LH, fill='FBF9FD' if i % 2 == 0 else 'F4F0F9', name='Carril'))
        S.add(shape_xml(S.nid(), X0, y + 8000, LW - 50000, LH - 16000, fill=PURD,
                        paras=p_xml(name, 950, algn='ctr', color='FFFFFF', bold=True, font='Montserrat'), anchor='ctr',
                        ins=(50000, 0, 50000, 0), name='Área'))
    for c, (name, freq) in enumerate(D.PHASES):
        x = X0 + LW + c * CW
        paras = p_xml(f'{c + 1}. {name}', 900, algn='ctr', color='FFFFFF', bold=True) + p_xml(freq, 750, algn='ctr', color='EDE0F8')
        S.add(shape_xml(S.nid(), x + 25000, PHY, CW - 50000, PHH, geom='roundRect', adj=18000, fill=PUR, paras=paras, anchor='ctr',
                        ins=(20000, 10000, 20000, 10000), name='Etapa'))
        if c:
            S.add(poly_xml(S.nid(), [(x, LY0), (x, LY0 + LH * len(D.LANES))], color='D9CDE6', w=6350, dash='dash', arrow=False))
    for a, b, style, off in D.EDGES:
        S.add(poly_xml(S.nid(), pts(a, b, style, off), color='4A4A55', w=15875, dash='dash' if style == 'dash' else None))
    x16, y16 = box(16)
    x8, y8 = box(8)
    S.add(poly_xml(S.nid(), [(x16 + BW / 2, y16), (x16 + BW / 2, CORR), (x8 + BW / 2, CORR), (x8 + BW / 2, y8)], color='3E8E22',
                   w=22225, dash='dash'))
    mid = (x8 + x16) / 2 + BW / 2
    S.pill(mid - 1550000, CORR - 72000, 3100000, 144000, 'Cada mes: siguiente nivel, de vuelta a CAPP y proyección', GRNL, GRND,
           sz=750, line=GRNB)
    for n, lane, col, title, codes, note, kind in D.STEPS:
        x, y = box(n)
        border, lw_, dash, fill = PUR, 15875, None, 'FFFFFF'
        if kind in ('start', 'end'):
            border, lw_ = GRN, 22225
            fill = 'F4FAF0' if kind == 'end' else 'FFFFFF'
        if kind == 'tbc':
            border, dash, fill = 'D99A00', 'dash', 'FFFCF3'
        paras = p_xml(title, 850, bold=True)
        if codes == 'Autoservicio':
            paras += p_xml([('Autoservicio', True, GRND)], 700)
        elif codes:
            paras += p_xml([(' · '.join(codes.split(', ')), True, PURD)], 700)
        S.add(shape_xml(S.nid(), x, y, BW, BH, geom='roundRect', adj=10000, fill=fill, line=border, line_w=lw_, dash=dash, paras=paras,
                        ins=(150000, 40000, 60000, 30000), name='Paso'))
        bc = {'start': GRN, 'end': GRN, 'tbc': 'D99A00'}.get(kind, PUR)
        S.add(shape_xml(S.nid(), x - 60000, y - 60000, 200000, 200000, geom='ellipse', fill=bc,
                        paras=p_xml(str(n), 750, algn='ctr', color='FFFFFF', bold=True), anchor='ctr', ins=(0, 0, 0, 0), name='Número'))
        if kind:
            txt, fl, colr = {'start': ('Inicio', GRN, 'FFFFFF'), 'end': ('Fin del ciclo', GRN, 'FFFFFF'),
                             'tbc': ('Por confirmar', 'FFE8A8', '7A5200')}[kind]
            tw = 420000 if kind == 'start' else 600000
            S.pill(x + BW - 30000 - tw, y - 72000, tw, 144000, txt, fl, colr, sz=600)
    S.save()


def d_pasos(part):
    def f(p):
        S = Slide(p, f'PASO A PASO ({part}/2)')
        chunk = D.DETALLE[:9] if part == 1 else D.DETALLE[9:]
        ref = {'PDF CAPP explicado': 'CAPP explicado'}
        rows = []
        for n, et, q, t, g, cu, r in chunk:
            r = ref.get(r, r)
            rows.append([num(n), et, f'**{q}**', t, g or ('Autoservicio' if n in (14, 15) else '—'), {'text': cu, 'algn': 'ctr'},
                         {'text': r, 'color': AMBD if 'confirmar' in r else INK, 'bold': 'confirmar' in r}])
        S.table([4, 12, 14, 34, 16, 10, 10], ['N°', 'Etapa', 'Quién', 'Qué se hace', 'Páginas', 'Cuándo', 'Referencia'], rows)
        S.save()
    return f


def d_leer(p):
    S = Slide(p, 'CÓMO LEERLO Y QUÉ FALTA')
    gap = 200000
    cw = (XW - 2 * gap) / 3
    y, h = S.y + 50000, 2700000
    notes = [('info', ['**Cómo leer el diagrama.**', 'Cada carril es un área; las columnas son las etapas en orden. Las flechas marcan el paso '
                       'siguiente y las punteadas, un paso que solo ocurre si aplica.',
                       'La flecha verde es el ciclo mensual: el participante vuelve a CAPP y proyección para el siguiente nivel.']),
             ('warn', ['**Por confirmar con Ellucian y las áreas:**', 'Malla de los centros en CAPP; si la tutoría aplica; quién inscribe '
                       '(Registros Académicos o el participante); qué aprueba la Jefatura; y si el certificado se registra como grado.']),
             ('purple', ['**Ya documentado:** temas 1 a 4 (periodo, NRC, reglas, docentes y admisión).',
                         '**Pendiente de documentar:** inscripción (5), tutoría (6), jefatura (7), docente (8) y finanzas (9).'])]
    for i, (kind, txt) in enumerate(notes):
        S.note(txt, kind=kind, x=X0 + i * (cw + gap), w=cw, y=y, h=h, sz=1450, anchor='t')
    ly = y + h + 350000
    S.text('Leyenda', sz=1200, color=INK, bold=True, y=ly, gap=60000)
    ly = S.y
    items = [('line', '4A4A55', None, 'Paso siguiente'), ('line', '4A4A55', 'dash', 'Solo si aplica'),
             ('line', '3E8E22', 'dash', 'Ciclo mensual'), ('box', PUR, None, 'Paso'), ('box', GRN, None, 'Inicio o fin'),
             ('box', 'D99A00', 'dash', 'Por confirmar')]
    x = X0
    for kind, col, dash, lab in items:
        if kind == 'line':
            S.add(poly_xml(S.nid(), [(x, ly + 110000), (x + 480000, ly + 110000)], color=col, w=19050, dash=dash))
        else:
            S.add(shape_xml(S.nid(), x, ly + 20000, 480000, 180000, geom='roundRect', adj=15000,
                            fill='FFFCF3' if dash else 'FFFFFF', line=col, line_w=19050, dash=dash))
        tw = text_w(lab, 1100) + 100000
        S.add(shape_xml(S.nid(), x + 560000, ly, tw, 220000, paras=p_xml(lab, 1100, color=MUT), anchor='ctr', ins=(0, 0, 0, 0)))
        x += 560000 + tw + 280000
    S.save()


def deck_diagrama():
    plan = [('cover', d_cover), ('text', d_diagrama), ('text', d_pasos(1)), ('text', d_pasos(2)), ('text', d_leer), ('close', None)]
    return run_deck('DIAGRAMA DE INICIO A FIN - CENTROS EMPRESARIALES EN BANNER', 'bD', plan,
                    'Centros Empresariales en Banner: de inicio a fin')


DECKS = {'A': deck_validacion, 'B': deck_capp, 'C': deck_ejec, 'D': deck_diagrama}

if __name__ == '__main__':
    for k in (sys.argv[1:] or DECKS):
        DECKS[k]()
