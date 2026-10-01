# -*- coding: utf-8 -*-
"""Periodo académico: antes (periodo de 3 meses) y después (Banner) en Centros Empresariales."""
import html
import os
import re
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
AUTHOR = 'Dagner Anibal Chuman Lluen'
CODE = re.compile(r'\b([SGT][A-Z]{2}[A-Z0-9]{3,4})\b')

# Colores por centro (validados con dataviz/validate_palette.js, modo claro, todos los pares)
C_IDI, C_COM, C_EMP = '#7030A0', '#1baf7a', '#eb6834'
C_IDI_III = '#D4BCEA'   # misma serie, tramo de nivel III


def fmt(text):
    t = html.escape(text, quote=False)
    t = CODE.sub(r'<span class="code">\1</span>', t)
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)


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


def d(s):
    dd, mm, yy = (int(x) for x in s.split('/'))
    return date(yy, mm, dd)


# ------------------------------------------------------------------ datos (Tema 1, cronogramas 2026)
PERIODOS = [('202651', 'Ciclo de verano', date(2026, 1, 1), date(2026, 3, 31), 'ene – mar'),
            ('202654', 'Semestre I', date(2026, 4, 1), date(2026, 7, 31), 'abr – jul'),
            ('202656', 'Semestre II', date(2026, 8, 1), date(2026, 12, 31), 'ago – dic')]

# grupo, periodo, inicio, fin niveles I–II (sem), fin nivel III (sem)
IDIOMAS = [
    ('I01', '202651', '5/1/2026', '15/2/2026', 6, '31/3/2026', 12),
    ('I02', '202651', '2/2/2026', '29/3/2026', 8, '30/4/2026', 13),
    ('I03', '202651', '2/3/2026', '26/4/2026', 8, '31/5/2026', 13),
    ('I04', '202654', '6/4/2026', '31/5/2026', 8, '30/6/2026', 12),
    ('I05', '202654', '4/5/2026', '28/6/2026', 8, '31/7/2026', 13),
    ('I06', '202654', '1/6/2026', '26/7/2026', 8, '31/8/2026', 13),
    ('I07', '202654', '6/7/2026', '30/8/2026', 8, '30/9/2026', 13),
    ('I08', '202656', '3/8/2026', '27/9/2026', 8, '31/10/2026', 13),
    ('I09', '202656', '7/9/2026', '31/10/2026', 8, '30/11/2026', 12),
    ('I10', '202656', '5/10/2026', '29/11/2026', 8, '31/12/2026', 13),
    ('I11', '202656', '2/11/2026', '27/12/2026', 8, '31/1/2027', 13),
    ('I12', '202656', '7/12/2026', '31/1/2027', 8, '28/2/2027', 12),
]
COMPUTACION = [
    ('X01', '202651', '12/1/2026', '22/2/2026', 6), ('X02', '202651', '23/2/2026', '22/3/2026', 4),
    ('X03', '202654', '6/4/2026', '31/5/2026', 8), ('X04', '202654', '1/6/2026', '12/7/2026', 6),
    ('X05', '202656', '3/8/2026', '30/8/2026', 4), ('X06', '202656', '7/9/2026', '31/10/2026', 8),
    ('X07', '202656', '2/11/2026', '13/12/2026', 6),
]
EMPRENDIMIENTO = [
    ('P01', '202651', '7/1/2026', '15/3/2026', 10), ('P02', '202651', '4/2/2026', '12/4/2026', 10),
    ('P03', '202651', '11/3/2026', '17/5/2026', 10), ('P04', '202654', '6/5/2026', '12/7/2026', 10),
    ('P05', '202656', '5/8/2026', '11/10/2026', 10), ('P06', '202656', '30/9/2026', '6/12/2026', 10),
]

T0, T1 = date(2026, 1, 1), date(2027, 3, 1)
SPAN = (T1 - T0).days
MESES = ['E', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D', 'E', 'F']


# ------------------------------------------------------------------ gráficos SVG
def xmap(x0, w):
    return lambda dt: x0 + (dt - T0).days / SPAN * w


def month_axis(X, y, h, top_labels=True):
    out = ''
    for i in range(15):
        yy, mm = 2026 + (i // 12), i % 12 + 1
        x = X(date(yy, mm, 1))
        out += f'<line x1="{x:.1f}" y1="{y}" x2="{x:.1f}" y2="{y + h}" class="grid"/>'
        if i < 14 and top_labels:
            xm = X(date(yy, mm, 15))
            out += f'<text x="{xm:.1f}" y="{y - 4}" class="tick" text-anchor="middle">{MESES[i]}</text>'
    return out


def estructura_svg():
    """Dos filas: antes (4 × 3 meses) y ahora (3 periodos + inicios mensuales)."""
    W, L = 690, 118
    X = xmap(L, W - L - 6)
    y_a, y_b, bh = 26, 84, 30
    s = f'<svg viewBox="0 0 {W} 150" class="viz" role="img" aria-label="Estructura del año: antes y ahora">'
    # años
    s += f'<text x="{X(date(2026, 7, 1)):.1f}" y="9" class="yr" text-anchor="middle">2026</text>'
    s += f'<text x="{X(date(2027, 2, 1)):.1f}" y="9" class="yr" text-anchor="middle">2027</text>'
    s += month_axis(X, 22, 110)
    # antes
    s += f'<text x="0" y="{y_a + 13}" class="rowh">ANTES</text><text x="0" y="{y_a + 25}" class="rows">periodo = 3 meses</text>'
    for i in range(4):
        a, b = date(2026, 1 + 3 * i, 1), date(2026 + (i == 3), (4 + 3 * i - 1) % 12 + 1, 1)
        xa, xb = X(a) + 1, X(b) - 1
        s += (f'<rect x="{xa:.1f}" y="{y_a}" width="{xb - xa:.1f}" height="{bh}" rx="4" class="old"/>'
              f'<text x="{(xa + xb) / 2:.1f}" y="{y_a + 13}" class="blk" text-anchor="middle">Periodo {i + 1}</text>'
              f'<text x="{(xa + xb) / 2:.1f}" y="{y_a + 24}" class="blks" text-anchor="middle">3 meses</text>')
    # ahora
    s += f'<text x="0" y="{y_b + 13}" class="rowh">AHORA</text><text x="0" y="{y_b + 25}" class="rows">Banner</text>'
    for code, name, a, b, _ in PERIODOS:
        xa, xb = X(a) + 1, X(date(b.year + (b.month == 12), b.month % 12 + 1, 1)) - 1
        s += (f'<rect x="{xa:.1f}" y="{y_b}" width="{xb - xa:.1f}" height="{bh}" rx="4" class="new"/>'
              f'<text x="{(xa + xb) / 2:.1f}" y="{y_b + 13}" class="blk w" text-anchor="middle">{code}</text>'
              f'<text x="{(xa + xb) / 2:.1f}" y="{y_b + 24}" class="blks w" text-anchor="middle">{name}</text>')
    # inicios mensuales (partes de periodo)
    for m in range(12):
        x = X(date(2026, m + 1, 1)) + 5
        s += f'<path d="M{x:.1f} {y_b + bh + 3} l-3.2 5.5 h6.4 z" class="tri"/>'
    xn = X(date(2026, 1, 1))
    s += (f'<path d="M{xn + 3:.1f} {y_b + bh + 14} l-3.2 5.5 h6.4 z" class="tri"/>'
          f'<text x="{xn + 10:.1f}" y="{y_b + bh + 20}" class="note">'
          'cada mes inicia un grupo = una parte de periodo (I01…I12, X01…, P01…) con sus propias fechas</text>')
    s += '</svg>'
    return s


def gantt_svg():
    W, L = 690, 104
    X = xmap(L, W - L - 44)
    top, rh, bh, gap = 34, 12.5, 7.5, 9
    groups = [('Idiomas', C_IDI, IDIOMAS), ('Computación', C_COM, COMPUTACION), ('Emprendimiento', C_EMP, EMPRENDIMIENTO)]
    n_rows = sum(len(g[2]) for g in groups)
    H = top + n_rows * rh + gap * (len(groups) - 1) + 8
    s = f'<svg viewBox="0 0 {W} {H:.0f}" class="viz" role="img" aria-label="Cronograma 2026 por grupo">'
    # bandas de periodo
    for i, (code, name, a, b, _) in enumerate(PERIODOS):
        xa, xb = X(a), X(date(b.year + (b.month == 12), b.month % 12 + 1, 1))
        s += f'<rect x="{xa:.1f}" y="{top - 6}" width="{xb - xa:.1f}" height="{H - top}" class="band{i % 2}"/>'
        s += f'<text x="{(xa + xb) / 2:.1f}" y="10" class="bandt" text-anchor="middle">{code} · {name}</text>'
    xa = X(date(2027, 1, 1))
    s += f'<text x="{(xa + X(T1)) / 2:.1f}" y="10" class="bandt mut" text-anchor="middle">2027</text>'
    s += month_axis(X, top - 6, H - top, top_labels=False)
    for i in range(14):
        yy, mm = 2026 + (i // 12), i % 12 + 1
        s += f'<text x="{X(date(yy, mm, 15)):.1f}" y="{top - 11}" class="tick" text-anchor="middle">{MESES[i]}</text>'
    y = top
    for gi, (name, color, rows) in enumerate(groups):
        y0 = y
        for r in rows:
            code, per, ini = r[0], r[1], d(r[2])
            cy = y + rh / 2
            s += f'<text x="{L - 8}" y="{cy + 2.6:.1f}" class="gl" text-anchor="end">{code}</text>'
            if len(r) == 7:   # idiomas: I–II y nivel III
                f12, s12, f3, s3 = d(r[3]), r[4], d(r[5]), r[6]
                x1, x2, x3 = X(ini), X(f12) + W / SPAN * 0.9, X(f3) + W / SPAN * 0.9
                s += f'<rect x="{x2 + 1:.1f}" y="{cy - bh / 2:.1f}" width="{max(x3 - x2 - 1, 1):.1f}" height="{bh}" rx="2" fill="{C_IDI_III}"/>'
                s += f'<rect x="{x1:.1f}" y="{cy - bh / 2:.1f}" width="{x2 - x1:.1f}" height="{bh}" rx="2" fill="{color}"/>'
                s += f'<text x="{x3 + 4:.1f}" y="{cy + 2.5:.1f}" class="dur">{s12} · {s3} sem</text>'
            else:
                f, sem = d(r[3]), r[4]
                x1, x2 = X(ini), X(f) + W / SPAN * 0.9
                s += f'<rect x="{x1:.1f}" y="{cy - bh / 2:.1f}" width="{x2 - x1:.1f}" height="{bh}" rx="2" fill="{color}"/>'
                s += f'<text x="{x2 + 4:.1f}" y="{cy + 2.5:.1f}" class="dur">{sem} sem</text>'
            y += rh
        s += (f'<text x="0" y="{(y0 + y) / 2 + 3:.1f}" class="cl">{name}</text>'
              f'<line x1="{L - 28}" y1="{y0 + 2}" x2="{L - 28}" y2="{y - 2}" stroke="{color}" stroke-width="2.5" stroke-linecap="round"/>')
        y += gap
    s += '</svg>'
    return s


# ------------------------------------------------------------------ documento
def build():
    b = []
    b.append('<header class="cover">'
             '<div class="logos"><img src="uss.png" alt="USS"><img src="ellucian.png" alt="Ellucian"></div>'
             '<div class="band"><div class="kicker">Universidad Señor de Sipán · Centros Empresariales</div>'
             '<h1>Periodo académico: antes y después</h1>'
             '<div class="sub">Cómo cambia el manejo del periodo al pasar a Ellucian Banner, con el cronograma 2026</div></div>'
             '<div class="meta">'
             f'<div><span>Elaborado por</span>{AUTHOR}</div>'
             '<div><span>Fecha</span>Septiembre 2026</div>'
             '<div><span>Alcance</span>Idiomas, Computación y Emprendimiento</div>'
             '<div><span>Fuente</span>Tema 1. Periodos académicos · cronogramas 2026</div>'
             '</div></header>')

    # 1. La idea
    b.append(section(1, 'La diferencia en una frase'))
    b.append('<div class="vs">'
             '<div class="card old"><div class="lbl">Antes</div>'
             '<p>El periodo <b>era el ciclo de clases</b>: duraba <b>3 meses</b> y todo (fechas, programación y matrícula) '
             'se organizaba dentro de él.</p></div>'
             '<div class="arrow">›</div>'
             '<div class="card new"><div class="lbl">Ahora en Banner</div>'
             '<p>El periodo es un <b>contenedor institucional</b> (verano, semestre I, semestre II). Cada grupo que inicia en '
             'el mes es una <b>parte de periodo</b> con sus propias fechas, y el curso dura lo que necesita: <b>4 a 13 semanas</b>.</p></div>'
             '</div>')

    # 2. Estructura del año
    b.append(section(2, 'Estructura del año', 'Antes: 4 periodos de 3 meses (ilustrativo). Ahora: 3 periodos al año y un inicio de grupo cada mes.'))
    b.append(f'<figure class="fig">{estructura_svg()}</figure>')

    # 3. Comparación
    b.append(section(3, 'Comparación punto por punto'))
    comp = [
        ('¿Qué es el periodo?', 'El ciclo de clases de 3 meses.',
         'Un contenedor: **202651** Ciclo de verano, **202654** Semestre I, **202656** Semestre II.'),
        ('Periodos por año', '4 (uno cada 3 meses).', '**3**, los mismos códigos cada año (AAAA + nivel 5 + secuencia).'),
        ('Inicio de clases', 'Al inicio de cada periodo.', 'Cada mes, por grupo: **I01…I12** (Idiomas), **X01…** (Computación), **P01…** (Emprendimiento).'),
        ('Duración del curso', 'La del periodo: 3 meses.', 'La del grupo y su NRC: **4 a 13 semanas** según el curso.'),
        ('Fechas de clases', 'Las del periodo.', 'Cada parte de periodo tiene inicio, fin, semanas y censo propios (SOATERM).'),
        ('Curso que termina después', 'Debía terminar dentro de los 3 meses.',
         'Permitido: el grupo pertenece al periodo en que **inicia** (ej. I07 inicia en julio, 202654, y termina en setiembre).'),
        ('Configuración', 'Crear un periodo cada 3 meses.', 'Crear **3 periodos al año** (STVTERM, SOATERM) con sus partes, fechas web y feriados (SSAEXCL).'),
        ('Programación', 'Por periodo.', 'Cada NRC se asigna a la parte de periodo de su grupo (SSASECT).'),
    ]
    b.append(table([('Aspecto', 19), ('Antes · periodo de 3 meses', 29), ('Ahora · Banner', 52)],
                   [[f'<b>{fmt(a)}</b>', fmt(o), fmt(n)] for a, o, n in comp], 'cmp'))
    b.append('<p class="foot">Columna «Antes» según lo indicado por el área (periodo de 3 meses); validar con el calendario del sistema anterior.</p>')

    # 4. Cronograma 2026
    b.append(section(4, 'Así queda 2026 en Banner', 'Una barra por grupo, desde su inicio hasta su fin. El fondo marca el periodo al que pertenece cada grupo por su mes de inicio.'))
    legend = ('<div class="legend">'
              f'<span><i style="background:{C_IDI}"></i>Idiomas · niveles I y II</span>'
              f'<span><i style="background:{C_IDI_III}"></i>Idiomas · nivel III</span>'
              f'<span><i style="background:{C_COM}"></i>Computación</span>'
              f'<span><i style="background:{C_EMP}"></i>Emprendimiento</span></div>')
    b.append(f'<figure class="fig">{legend}{gantt_svg()}</figure>')

    rows = []
    for code, name, _, _, meses in PERIODOS:
        g = lambda L: [r[0] for r in L if r[1] == code]
        i, x, p = g(IDIOMAS), g(COMPUTACION), g(EMPRENDIMIENTO)
        rng = lambda L: (f'{L[0]} – {L[-1]}' if len(L) > 1 else L[0]) + f' <span class="cnt">({len(L)})</span>'
        rows.append([f'<span class="pg">{code}</span>', f'<b>{name}</b>', meses, rng(i), rng(x), rng(p)])
    rows.append(['', '<b>Total 2026</b>', '12 meses', '<b>12 grupos</b>', '<b>7 grupos</b>', '<b>6 grupos</b>'])
    b.append(table([('Periodo', 13), ('Nombre', 17), ('Inicio de grupos', 16), ('Idiomas', 18), ('Computación', 18),
                    ('Emprendimiento', 18)], rows, 'per'))

    # 5. Detalle
    b.append(section(5, 'Cronograma 2026 en detalle', 'Fechas de cada grupo (parte de periodo) según el tema 1.'))
    idi = [[f'<b>{g}</b>', f'<span class="pg">{p}</span>', a, f12, f'{s12}', f3, f'{s3}'] for g, p, a, f12, s12, f3, s3 in IDIOMAS]
    b.append('<h3>Idiomas <span class="eg">BASIC e INTERMEDIATE; niveles I–II y nivel III</span></h3>')
    b.append(table([('Grupo', 10), ('Periodo', 14), ('Inicio', 15), ('Fin I – II', 17), ('Sem.', 9), ('Fin III', 17), ('Sem.', 9)],
                   idi, 'det'))
    com = [[f'<b>{g}</b>', f'<span class="pg">{p}</span>', a, f, f'{s}'] for g, p, a, f, s in COMPUTACION]
    emp = [[f'<b>{g}</b>', f'<span class="pg">{p}</span>', a, f, f'{s}'] for g, p, a, f, s in EMPRENDIMIENTO]
    cols = [('Grupo', 15), ('Periodo', 23), ('Inicio', 22), ('Fin', 24), ('Sem.', 16)]
    b.append('<div class="grid2">'
             f'<div><h3>Computación <span class="eg">todos los cursos</span></h3>{table(cols, com, "det")}</div>'
             f'<div><h3>Emprendimiento <span class="eg">todos los cursos</span></h3>{table(cols, emp, "det")}</div></div>')

    # 6. Trabajo diario
    b.append(section(6, 'Qué se hace ahora y cuándo'))
    tareas = [
        ('3 veces al año', 'Abrir el periodo: crearlo, configurar su control con todas sus partes de periodo, las fechas web y los feriados.',
         'STVTERM, SOATERM, SSAEXCL'),
        ('Cada mes', 'Programar los NRC del grupo que inicia en su parte de periodo, asignar docentes y registrar a los participantes con el periodo del grupo.',
         'SSASECT, SIAINST, SAAQUIK'),
        ('Al cerrar la inscripción', 'Desactivar los accesos web del periodo.', 'SOATERM'),
    ]
    chips = lambda c: ' '.join(f'<span class="pg">{x}</span>' for x in c.split(', '))
    b.append(table([('Cuándo', 18), ('Qué se hace', 54), ('Páginas', 28)],
                   [[f'<b>{w}</b>', fmt(q), chips(p)] for w, q, p in tareas], 'when'))

    # 7. Reglas
    b.append(section(7, 'Reglas prácticas'))
    reglas = [
        'El grupo pertenece al periodo en el que **inicia**, aunque termine en el siguiente (ej. I11 inicia en noviembre y termina en enero).',
        'La duración la define la **parte de periodo y el NRC**, no el periodo.',
        'Cada periodo debe tener la **parte 1** (periodo completo) además de sus grupos.',
        'Para admitir o inscribir a un participante se usa el **periodo de su grupo** (ej. grupo I05: periodo 202654).',
        'Las fechas de inscripción web del periodo deben cubrir **todas sus partes** en un solo rango.',
        'Los códigos I01…I12 se usan uno por mes; en 2026, Computación usa X01–X07 y Emprendimiento P01–P06.',
    ]
    b.append('<ol class="rules">' + ''.join(f'<li>{fmt(r)}</li>' for r in reglas) + '</ol>')
    return '\n'.join(b)


CSS_EXTRA = '''
.vs { display: grid; grid-template-columns: 1fr 26px 1.35fr; align-items: stretch; gap: 6px; margin: 2px 0 4px; }
.vs .card { border-radius: 9px; padding: 9px 13px 10px; }
.vs .card p { margin: 3px 0 0; font-size: 9.2pt; line-height: 1.45; }
.vs .card.old { background: #F2F2F5; border: 1px solid #E1E1E6; }
.vs .card.new { background: var(--pl); border: 1px solid var(--pb); }
.vs .lbl { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 8pt; letter-spacing: .08em; text-transform: uppercase; }
.vs .old .lbl { color: #6B6B76; } .vs .new .lbl { color: var(--pd); }
.vs .arrow { align-self: center; text-align: center; color: var(--g); font-weight: 800; font-size: 20pt; }
.fig { margin: 2px 0 6px; break-inside: avoid; }
svg.viz { width: 100%; height: auto; display: block; font-family: 'InterStatic', sans-serif; }
svg .grid { stroke: #E4E1E9; stroke-width: .6; }
svg .tick { font-size: 7px; fill: #5F5F6B; font-weight: 600; }
svg .yr { font-size: 7.5px; fill: #1E1E24; font-weight: 700; letter-spacing: .06em; }
svg .rowh { font-family: 'Montserrat', sans-serif; font-size: 9px; font-weight: 700; fill: #1E1E24; }
svg .rows { font-size: 7.2px; fill: #5F5F6B; }
svg .old { fill: #E9E9EE; stroke: #C9C9D1; stroke-width: .8; }
svg .new { fill: #7030A0; }
svg .blk { font-size: 8px; font-weight: 700; fill: #3A3A44; }
svg .blks { font-size: 6.6px; fill: #5F5F6B; }
svg .w { fill: #fff; } svg .blks.w { fill: #EBDDF7; }
svg .tri { fill: #4EA72E; }
svg .note { font-size: 7.2px; fill: #2F6B1B; font-weight: 600; }
svg .band0 { fill: #F6F2FA; } svg .band1 { fill: #FFFFFF; }
svg .bandt { font-size: 7.4px; font-weight: 700; fill: #5C2193; } svg .bandt.mut { fill: #8C8C96; }
svg .gl { font-size: 6.8px; font-weight: 600; fill: #3A3A44; }
svg .cl { font-size: 7.4px; font-weight: 700; fill: #1E1E24; }
svg .dur { font-size: 6px; fill: #5F5F6B; }
.legend { display: flex; flex-wrap: wrap; gap: 14px; font-size: 7.8pt; color: var(--mut); margin: 0 0 4px 2px; }
.legend i { display: inline-block; width: 16px; height: 7px; border-radius: 2px; margin-right: 5px; vertical-align: 0; }
table.cmp td:nth-child(2) { color: #4A4A55; background: #F7F7F9; }
table.cmp tbody tr:nth-child(even) td:nth-child(2) { background: #F1F1F4; }
table.cmp th:nth-child(2) { background: #8A8A96; }
table.cmp td:first-child, table.cmp th:first-child,
table.per td:nth-child(2), table.per th:nth-child(2) { text-align: left; }
table.per td, table.per th, table.det td, table.det th { text-align: center; }
table.per td:nth-child(2), table.per th:nth-child(2) { text-align: left; }
table.per tbody tr:last-child td { background: var(--gl); border-top: 1px solid #D3EAC7; }
table.det td { padding: 3.2px 6px; font-variant-numeric: tabular-nums; }
.cnt { color: var(--mut); font-size: 7.4pt; }
ol.rules { margin: 2px 0 0; padding-left: 0; list-style: none; counter-reset: r; columns: 2; column-gap: 16px; }
ol.rules li { counter-increment: r; position: relative; padding: 5px 8px 5px 30px; margin: 0 0 6px; background: var(--pz);
              border: 1px solid var(--line); border-radius: 7px; break-inside: avoid; font-size: 8.5pt; }
ol.rules li::before { content: counter(r); position: absolute; left: 8px; top: 5px; width: 16px; height: 16px; border-radius: 8px;
                      background: var(--p); color: #fff; font-weight: 700; font-size: 7.4pt; line-height: 16px; text-align: center; }
.meta { grid-template-columns: 1.15fr .75fr 1.25fr 1.45fr; }
'''


def main():
    css = open(os.path.join(HERE, 'base.css'), encoding='utf8').read() + CSS_EXTRA
    doc = (f'<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>Periodo académico: antes y después</title>'
           f'<style>{css}</style></head><body data-palette="{C_IDI},{C_COM},{C_EMP}">{build()}</body></html>')
    open(os.path.join(HERE, 'antes.html'), 'w', encoding='utf8').write(doc)
    print('OK')


if __name__ == '__main__':
    main()
