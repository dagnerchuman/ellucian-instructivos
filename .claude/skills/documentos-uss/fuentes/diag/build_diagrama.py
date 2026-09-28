# -*- coding: utf-8 -*-
"""Diagrama de inicio a fin: cómo usa Banner un Centro Empresarial (carriles por área, etapas en orden)."""
import html
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'entregables', 'DIAGRAMA DE INICIO A FIN - CENTROS EMPRESARIALES EN BANNER.pdf')
AUTHOR = 'Dagner Anibal Chuman Lluen'

# ------------------------------------------------------------------ modelo
LANES = [('Registros Académicos', 'RA'), ('Jefatura', 'JEF'), ('Finanzas', 'FIN'), ('Escuela / Centro Empresarial', 'CE'),
         ('Admisión', 'ADM'), ('Docente', 'DOC'), ('Participante', 'PAR')]
LI = {k: i for i, (_, k) in enumerate(LANES)}
PHASES = [('Preparar el periodo', '3 veces al año'), ('Programar el mes', 'cada mes'), ('Admitir', 'por participante'),
          ('Proyectar', 'CAPP'), ('Inscribir y cobrar', 'cada grupo'), ('Dictar clases', 'durante el curso'),
          ('Cerrar y avanzar', 'al terminar')]

# n, carril, etapa, título, páginas, nota, tipo (''|start|end|tbc)
STEPS = [
    (1, 'RA', 0, 'Abrir el periodo y sus partes', 'STVTERM, SOATERM, SSAEXCL', 'Tema 1', 'start'),
    (2, 'CE', 0, 'Diseñar catálogo y malla', 'SCACRSE, SMAPROG, SMAAREA', 'Catálogo mensual', ''),
    (3, 'CE', 1, 'Programar los NRC del grupo', 'SSASECT, SSAPREQ, SSARRES', 'Temas 2 y 2.1', ''),
    (4, 'RA', 1, 'Carga lectiva: docente al NRC', 'SIAINST, SSASECT, SIAASGN', 'Reemplaza el Excel · Tema 3', ''),
    (5, 'PAR', 2, 'Solicita llevar un curso', '', 'Idiomas, Computación o Emprendimiento', 'start'),
    (6, 'ADM', 2, 'Registrar al participante', 'GOAMTCH, SAAQUIK, SPAIDEN', 'Crea SAAADMS y SGASTDN', ''),
    (7, 'RA', 2, 'Asignar tutor', 'SIAINST, SGAADVR', 'Si aplica a los centros', 'tbc'),
    (8, 'RA', 3, 'CAPP y proyección', 'SMARQCM, SFPPROJ, SFAPROJ', 'Define qué nivel le toca', ''),
    (9, 'RA', 4, 'Inscribir en el NRC', 'SFAREGS', 'Solo lo proyectado · backoffice o autoservicio', ''),
    (10, 'JEF', 4, 'Aprobar excepciones', 'SFAROVR', 'Si la inscripción da error', 'tbc'),
    (11, 'FIN', 4, 'Cobro y pagos', 'SFARGFE, TSAAREV, TVACAJA', 'La inscripción genera el cobro', ''),
    (12, 'PAR', 4, 'Paga matrícula o pensión', '', 'Con deuda: retención SOAHOLD', ''),
    (13, 'RA', 5, 'Plan de evaluación del NRC', 'SHAGCOM', 'Antes de registrar notas', ''),
    (14, 'DOC', 5, 'Asistencia y calificaciones', 'Autoservicio', 'Por NRC y sesión', ''),
    (15, 'PAR', 5, 'Asiste y consulta', 'Autoservicio', 'Horario, asistencia y notas', ''),
    (16, 'RA', 6, 'Cerrar el periodo', 'SHRROLL, SMRBCMP', 'Notas a la historia y CAPP masivo', ''),
    (17, 'PAR', 6, 'Aprueba el nivel', 'SHACRSE', 'Siguiente nivel o certificado', 'end'),
]
SI = {s[0]: s for s in STEPS}

# conexiones: (desde, hasta, estilo, desplazamiento del carril vertical en el hueco)
EDGES = [(1, 2, 'solid', 0), (2, 3, 'solid', 0), (3, 4, 'solid', 0), (4, 5, 'solid', 0), (5, 6, 'solid', 0),
         (6, 7, 'dash', 0), (6, 8, 'solid', 0), (8, 9, 'solid', 0), (9, 10, 'dash', 0), (9, 11, 'side', -6),
         (11, 12, 'solid', 0), (12, 13, 'solid', 6), (13, 14, 'solid', 0), (14, 15, 'solid', 0), (15, 16, 'solid', 0),
         (16, 17, 'solid', 0)]

# ------------------------------------------------------------------ geometría (px CSS, A3 horizontal)
W = 1504
PH = 58                 # cabecera de etapas
LH = 118                # alto de carril
LW = 132                # ancho de la cabecera de carril
CW = (W - LW) / len(PHASES)
BW, BH = 166, 102
LOOP = 46               # espacio inferior para el ciclo
H = PH + LH * len(LANES) + LOOP


def box(n):
    _, lane, col, *_ = SI[n]
    x = LW + col * CW + (CW - BW) / 2
    y = PH + LI[lane] * LH + (LH - BH) / 2
    return x, y


def edge_path(a, b, style, off):
    ax, ay = box(a)
    bx, by = box(b)
    acx, acy, bcx, bcy = ax + BW / 2, ay + BH / 2, bx + BW / 2, by + BH / 2
    if style == 'side':                                   # misma columna, entra por la derecha
        gx = ax + BW + (CW - BW) / 2 + off
        return f'M{ax + BW:.1f} {acy:.1f} H{gx:.1f} V{bcy:.1f} H{bx + BW + 2:.1f}'
    if abs(ax - bx) < 1:                                  # misma columna: vertical
        if by > ay:
            return f'M{acx:.1f} {ay + BH:.1f} V{by - 2:.1f}'
        return f'M{acx:.1f} {ay:.1f} V{by + BH + 2:.1f}'
    if abs(ay - by) < 1:                                  # mismo carril: horizontal
        return f'M{ax + BW:.1f} {acy:.1f} H{bx - 2:.1f}'
    gx = ax + BW + (CW - BW) / 2 + off                    # por el hueco entre columnas
    return f'M{ax + BW:.1f} {acy:.1f} H{gx:.1f} V{bcy:.1f} H{bx - 2:.1f}'


def svg_overlay():
    s = (f'<svg class="ov" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
         '<defs>'
         '<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
         '<path d="M0 0 L10 5 L0 10 z" fill="#4A4A55"/></marker>'
         '<marker id="arg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
         '<path d="M0 0 L10 5 L0 10 z" fill="#3E8E22"/></marker></defs>')
    for a, b, style, off in EDGES:
        dash = ' stroke-dasharray="5 4"' if style == 'dash' else ''
        s += f'<path d="{edge_path(a, b, style, off)}" class="e"{dash} marker-end="url(#ar)"/>'
    # ciclo: del paso 17 (abajo) de vuelta a CAPP y proyección (paso 8)
    x17, y17 = box(17)
    x8, y8 = box(8)
    yb = PH + LH * len(LANES) + 22
    s += (f'<path d="M{x17 + BW / 2:.1f} {y17 + BH:.1f} V{yb} H{x8 + BW / 2:.1f} V{y8 + BH + 2:.1f}" class="loop" '
          f'marker-end="url(#arg)"/>')
    s += (f'<rect x="{(x8 + x17) / 2 + BW / 2 - 250:.1f}" y="{yb - 10}" width="500" height="20" rx="10" class="looplab"/>'
          f'<text x="{(x8 + x17) / 2 + BW / 2:.1f}" y="{yb + 4}" class="loopt" text-anchor="middle">'
          'Cada mes: el participante pasa al siguiente nivel y vuelve a CAPP y proyección</text>')
    return s + '</svg>'


def chip_html(codes):
    if not codes:
        return ''
    return ''.join(f'<span class="{"pg" if c != "Autoservicio" else "pg auto"}">{html.escape(c)}</span>' for c in codes.split(', '))


def diagram():
    d = [f'<div class="dg" style="width:{W}px;height:{H}px">']
    # carriles
    for i, (name, _) in enumerate(LANES):
        y = PH + i * LH
        d.append(f'<div class="lane l{i % 2}" style="top:{y}px;height:{LH}px;width:{W}px"></div>')
        d.append(f'<div class="lh" style="top:{y}px;height:{LH}px;width:{LW - 10}px"><span>{html.escape(name)}</span></div>')
    # etapas
    for c, (name, freq) in enumerate(PHASES):
        x = LW + c * CW
        d.append(f'<div class="ph" style="left:{x + 3:.1f}px;width:{CW - 6:.1f}px;height:{PH - 12}px">'
                 f'<b>{c + 1}. {html.escape(name)}</b><small>{html.escape(freq)}</small></div>')
        if c:
            d.append(f'<div class="vsep" style="left:{x:.1f}px;top:{PH - 4}px;height:{LH * len(LANES) + 4}px"></div>')
    d.append(svg_overlay())
    # cajas
    for n, lane, col, title, codes, note, kind in STEPS:
        x, y = box(n)
        tag = {'start': '<span class="tg start">Inicio</span>', 'end': '<span class="tg end">Fin del ciclo</span>',
               'tbc': '<span class="tg tbc">Por confirmar</span>'}.get(kind, '')
        d.append(f'<div class="bx {kind}" style="left:{x:.1f}px;top:{y:.1f}px;width:{BW}px;height:{BH}px">{tag}'
                 f'<div class="hd"><span class="nm">{n}</span><span class="tt">{html.escape(title)}</span></div>'
                 f'<div class="cd">{chip_html(codes)}</div><div class="nt">{html.escape(note)}</div></div>')
    d.append('</div>')
    return '\n'.join(d)


DETALLE = [
    (1, 'Preparar el periodo', 'Registros Académicos', 'Crear el periodo (verano, semestre I o II), sus partes de periodo (I01…, X01…, P01…), fechas web y feriados.',
     'STVTERM, SOATERM, SSAEXCL', '3 veces al año', 'Tema 1'),
    (2, 'Preparar el periodo', 'Escuela / Centro', 'Diseñar el catálogo de cursos del mes y la malla del programa (reglas CAPP).',
     'SCACRSE, SMAPROG, SMAAREA', 'Cada mes', 'Por confirmar la malla en CAPP'),
    (3, 'Programar el mes', 'Escuela / Centro', 'Crear los NRC del grupo en la parte de periodo del mes: cupo, horario y reglas.',
     'SSASECT, SSAPREQ, SSARRES', 'Cada mes', 'Temas 2 y 2.1'),
    (4, 'Programar el mes', 'Registros Académicos', 'Registrar al docente, asignarlo al NRC y revisar su carga.',
     'SIAINST, SSASECT, SIAASGN', 'Cada mes', 'Tema 3'),
    (5, 'Admitir', 'Participante', 'Solicita llevar un curso del centro.', '', 'Por participante', ''),
    (6, 'Admitir', 'Admisión', 'Buscar a la persona, registrarla y admitirla: crea la solicitud y el estudiante.',
     'GOAMTCH, SAAQUIK, SPAIDEN', 'Por participante', 'Tema 4'),
    (7, 'Admitir', 'Registros Académicos', 'Asignar tutor o asesor, si la tutoría aplica a los centros.', 'SIAINST, SGAADVR', 'Por participante', 'Por confirmar'),
    (8, 'Proyectar', 'Registros Académicos', 'Evaluar el avance con CAPP y generar la proyección: qué nivel le toca.',
     'SMARQCM, SFPPROJ, SFAPROJ', 'Cada grupo', 'PDF CAPP explicado'),
    (9, 'Inscribir y cobrar', 'Registros Académicos', 'Inscribir al participante en el NRC proyectado (o el participante por autoservicio).',
     'SFAREGS', 'Cada grupo', 'Quién inscribe: por confirmar'),
    (10, 'Inscribir y cobrar', 'Jefatura', 'Aprobar sobrepasos cuando la inscripción da error (cupo, cruce, prerrequisito).', 'SFAROVR', 'Si hay error', 'Por confirmar'),
    (11, 'Inscribir y cobrar', 'Finanzas', 'La inscripción genera el cobro en la cuenta corriente; se registran los pagos en caja.',
     'SFARGFE, TSAAREV, TVACAJA', 'Cada grupo', 'Capacidad 11'),
    (12, 'Inscribir y cobrar', 'Participante', 'Paga su matrícula o pensión. Con deuda, puede tener retención.', 'SOAHOLD', 'Cada grupo', ''),
    (13, 'Dictar clases', 'Registros Académicos', 'Cargar el plan de evaluación del NRC para que el docente registre notas.', 'SHAGCOM', 'Cada NRC', 'Capacidad 7'),
    (14, 'Dictar clases', 'Docente', 'Registrar asistencia y calificaciones por Autoservicio.', '', 'Durante el curso', 'Capacidad 7'),
    (15, 'Dictar clases', 'Participante', 'Asiste y consulta horario, asistencia y notas por Autoservicio.', '', 'Durante el curso', ''),
    (16, 'Cerrar y avanzar', 'Registros Académicos', 'Pasar las notas a la historia académica y ejecutar el CAPP masivo.', 'SHRROLL, SMRBCMP', 'Al terminar', 'Capacidad 7'),
    (17, 'Cerrar y avanzar', 'Participante', 'Aprueba el nivel: pasa al siguiente (vuelve al paso 8) o culmina y recibe su certificado.',
     'SHACRSE, SHADEGR', 'Al terminar', 'Certificado: por confirmar'),
]


def page2():
    rows = ''
    for n, et, q, t, p, f, ref in DETALLE:
        chips = ''.join(f'<span class="pg">{c}</span>' for c in p.split(', ')) if p else '<span class="mut">Autoservicio</span>' if n in (14, 15) else ''
        tbc = ' class="tbcrow"' if 'confirmar' in ref else ''
        rows += (f'<tr{tbc}><td><span class="n">{n}</span></td><td>{et}</td><td><b>{q}</b></td><td>{html.escape(t)}</td>'
                 f'<td>{chips}</td><td>{f}</td><td>{html.escape(ref)}</td></tr>')
    return ('<div class="p2"><div class="sec"><h2>Paso a paso</h2><span class="bar"></span></div>'
            '<table class="t det"><colgroup><col style="width:4%"><col style="width:12%"><col style="width:14%"><col style="width:36%">'
            '<col style="width:15%"><col style="width:9%"><col style="width:10%"></colgroup>'
            '<thead><tr><th>N°</th><th>Etapa</th><th>Quién</th><th>Qué se hace</th><th>Páginas</th><th>Cuándo</th><th>Referencia</th></tr></thead>'
            f'<tbody>{rows}</tbody></table>'
            '<div class="grid3">'
            '<div class="note"><b>Cómo leer el diagrama.</b> Cada carril es un área; las columnas son las etapas en orden. '
            'Las flechas marcan el paso siguiente y las punteadas, un paso que solo ocurre si aplica. La flecha verde es el ciclo mensual: '
            'al aprobar un nivel, el participante vuelve a CAPP y proyección para el siguiente grupo.</div>'
            '<div class="note warn"><b>Por confirmar con Ellucian y las áreas:</b> malla de los centros en CAPP; si la tutoría aplica; '
            'quién inscribe (Registros Académicos o el participante); qué aprueba la Jefatura; y si el certificado se registra como grado.</div>'
            '<div class="note"><b>Qué ya está documentado:</b> temas 1 a 4 (periodo, NRC, reglas, docentes, admisión). '
            '<b>Pendiente de documentar:</b> inscripción (5), tutoría (6), jefatura (7), docente (8) y finanzas (9).</div>'
            '</div></div>')


CSS = '''
@page { size: A3 landscape; }
.top { display: flex; align-items: center; gap: 18px; margin-bottom: 10px; }
.top img.u { height: 40px; } .top img.e { height: 24px; margin-left: auto; }
.top .tt1 { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 21pt; color: var(--ink); line-height: 1.1; }
.top .tt1 em { font-style: normal; color: var(--p); }
.top .st1 { font-size: 9.5pt; color: var(--mut); margin-top: 2px; }
.top .au { font-size: 8.5pt; color: var(--mut); text-align: right; margin-right: 14px; }
.top .au b { color: var(--pd); }
.dg { position: relative; margin: 0 auto; }
.lane { position: absolute; left: 0; } .lane.l0 { background: #FBF9FD; } .lane.l1 { background: #F4F0F9; }
.lh { position: absolute; left: 0; display: flex; align-items: center; justify-content: center; text-align: center;
      background: var(--pd); color: #fff; font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 10.5pt; line-height: 1.2;
      border-bottom: 2px solid #fff; padding: 0 8px; }
.ph { position: absolute; top: 4px; background: var(--p); color: #fff; border-radius: 8px; display: flex; flex-direction: column;
      justify-content: center; align-items: center; text-align: center; }
.ph b { font-family: 'Montserrat', sans-serif; font-size: 10.5pt; } .ph small { font-size: 8.3pt; color: #E7D6F6; font-weight: 600; margin-top: 1px; }
.vsep { position: absolute; width: 0; border-left: 1px dashed #D9CDE6; }
svg.ov { position: absolute; left: 0; top: 0; overflow: visible; }
svg .e { fill: none; stroke: #4A4A55; stroke-width: 1.6; }
svg .loop { fill: none; stroke: #3E8E22; stroke-width: 2; stroke-dasharray: 7 5; }
svg .looplab { fill: #EDF7E8; stroke: #BFE0B0; }
svg .loopt { font-family: 'InterStatic', sans-serif; font-size: 11px; font-weight: 700; fill: #2F6B1B; }
.bx { position: absolute; background: #fff; border: 1.6px solid var(--p); border-radius: 10px; padding: 7px 9px 6px;
      box-shadow: 0 1px 2px rgba(60, 20, 90, .10); display: flex; flex-direction: column; }
.bx.start, .bx.end { border-color: var(--g); border-width: 2px; }
.bx.end { background: #F4FAF0; }
.bx.tbc { border: 1.6px dashed #D99A00; background: #FFFCF3; }
.bx .hd { display: flex; gap: 6px; align-items: flex-start; }
.bx .nm { flex: none; width: 19px; height: 19px; border-radius: 10px; background: var(--p); color: #fff; font-weight: 700; font-size: 8.4pt;
          line-height: 19px; text-align: center; margin-top: 1px; }
.bx.start .nm, .bx.end .nm { background: var(--g); } .bx.tbc .nm { background: #D99A00; }
.bx .tt { font-weight: 700; font-size: 9.6pt; line-height: 1.22; color: var(--ink); }
.bx .cd { margin-top: 4px; line-height: 1.25; }
.bx .pg { font-size: 7.3pt; padding: 0 3px; margin: 1px 2px 0 0; }
.bx .pg.auto { background: var(--gl); color: var(--gd); border-color: #CFE7C3; }
.bx .nt { margin-top: auto; font-size: 7.6pt; color: var(--mut); line-height: 1.25; }
.tg { position: absolute; top: -9px; right: 8px; font-size: 7pt; font-weight: 700; border-radius: 8px; padding: 1px 7px; letter-spacing: .03em; }
.tg.start, .tg.end { background: var(--g); color: #fff; } .tg.tbc { background: #FFE8A8; color: #7A5200; }
.lg { display: flex; flex-wrap: wrap; gap: 20px; align-items: center; margin-top: 6px; font-size: 8.6pt; color: var(--mut); }
.lg span { display: inline-flex; align-items: center; gap: 6px; }
.lg i { display: inline-block; }
.lg .a { width: 28px; height: 0; border-top: 2px solid #4A4A55; }
.lg .d { width: 28px; height: 0; border-top: 2px dashed #4A4A55; }
.lg .l { width: 28px; height: 0; border-top: 2px dashed #3E8E22; }
.lg .b { width: 18px; height: 12px; border: 1.6px solid var(--p); border-radius: 3px; }
.lg .bt { width: 18px; height: 12px; border: 1.6px dashed #D99A00; border-radius: 3px; background: #FFFCF3; }
.lg .bs { width: 18px; height: 12px; border: 2px solid var(--g); border-radius: 3px; }
.p2 { break-before: page; }
.p2 .sec { margin-top: 0; }
table.det td { font-size: 9pt; padding: 6px 8px; } table.det th { font-size: 8.8pt; }
table.det td:nth-child(2), table.det th:nth-child(2), table.det td:nth-child(3), table.det th:nth-child(3),
table.det td:nth-child(4), table.det th:nth-child(4), table.det td:nth-child(7), table.det th:nth-child(7) { text-align: left; }
table.det td:nth-child(6), table.det th:nth-child(6) { text-align: center; }
table.det tr.tbcrow td:last-child { color: #8A5A00; font-weight: 600; }
.mut { color: var(--mut); font-size: 8pt; font-weight: 600; }
.grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 10px; }
.grid3 .note { margin: 0; font-size: 9pt; line-height: 1.45; }
.note.warn { border-left-color: #E0A100; background: #FFF8E8; }
'''


def build():
    top = ('<div class="top"><img class="u" src="uss.png" alt="USS"><div><div class="tt1">Centros Empresariales en Banner: '
           '<em>de inicio a fin</em></div><div class="st1">Cómo usarían el sistema Idiomas, Computación y Emprendimiento, '
           'desde abrir el periodo hasta aprobar el nivel</div></div>'
           f'<div class="au" style="margin-left:auto">Elaborado por: <b>{AUTHOR}</b><br>Septiembre 2026 · versión para validar</div>'
           '<img class="e" src="ellucian.png" alt="Ellucian" style="margin-left:0"></div>')
    legend = ('<div class="lg"><span><i class="a"></i>Paso siguiente</span><span><i class="d"></i>Solo si aplica</span>'
              '<span><i class="l"></i>Ciclo mensual</span><span><i class="b"></i>Paso</span><span><i class="bs"></i>Inicio o fin</span>'
              '<span><i class="bt"></i>Por confirmar</span><span>Códigos en morado: páginas de Banner · Autoservicio: portal web</span></div>')
    return top + diagram() + legend + page2()


def main():
    css = open(os.path.join(HERE, 'base.css'), encoding='utf8').read() + CSS
    doc = (f'<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>Centros Empresariales en Banner: de inicio a fin</title>'
           f'<style>{css}</style></head><body>{build()}</body></html>')
    hp, pp = os.path.join(HERE, 'diagrama.html'), os.path.join(HERE, 'diagrama.pdf')
    open(hp, 'w', encoding='utf8').write(doc)
    subprocess.run(['node', os.path.join(HERE, 'render.js'), hp, pp, 'Centros Empresariales en Banner: de inicio a fin'], check=True)
    import fitz
    d = fitz.open(pp)
    d.set_metadata({'title': 'Centros Empresariales en Banner: de inicio a fin', 'author': AUTHOR, 'creator': AUTHOR,
                    'subject': 'Diagrama de proceso de inicio a fin', 'producer': d.metadata.get('producer', '')})
    d.save(OUT, garbage=3, deflate=True)
    print('OK', len(d), 'pages')


if __name__ == '__main__':
    main()
