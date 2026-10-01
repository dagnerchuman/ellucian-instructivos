# -*- coding: utf-8 -*-
"""Secciones 6 a 8 del PDF de validación: criterios, tiempos y cronograma, responsabilidades."""
from datetime import date
import html

HOY = date(2026, 9, 25)
C_CARGA, C_REV, C_OTRA = '#7030A0', '#eb6834', '#1baf7a'   # validados (dataviz, todos los pares)

CRITERIOS = [
    ('Integridad', 'Campos obligatorios completos según las reglas funcionales.', '99%',
     'Persona con documento, nombres y fecha de nacimiento completos.'),
    ('Exactitud', 'Valores en Banner iguales a la fuente de origen o a la evidencia.', '98%',
     'Apellidos, documento y nota de BASIC I iguales al sistema anterior.'),
    ('Consistencia', 'Datos relacionados coherentes entre módulos y registros.', '98%',
     'El programa del centro en SGASTDN coincide con su historia y su inscripción.'),
    ('Validez', 'Formatos, códigos, fechas y valores según los catálogos de Banner.', '99%',
     'Periodos 202651/54/56, partes I01…, X01…, P01… y fechas válidas.'),
    ('Unicidad', 'Sin duplicados de personas, estudiantes o inscripciones.', '99,5%',
     'Un solo ID aunque la persona sea alumno de pregrado, participante y docente.'),
    ('Integridad referencial', 'Relaciones íntegras y totales conciliados con el origen.', '99%',
     'Totales por centro iguales al sistema anterior; cada curso ligado a su participante y periodo.'),
]

# etapa, ambiente, carga (ini, fin), revisión (ini, fin), tipo, min/caso, muestra, aplica
CRONO = [
    ('Personas', 'PROD', (date(2026, 9, 7), date(2026, 9, 21)), (date(2026, 9, 24), date(2026, 9, 27)), 'e', 12, 48, 'Sí'),
    ('Documento de identidad', 'PROD', (date(2026, 9, 22), date(2026, 9, 25)), (date(2026, 9, 25), date(2026, 9, 27)), 'e', 2, 48, 'Sí'),
    ('Contacto de emergencia', 'PROD', (date(2026, 9, 22), date(2026, 9, 25)), (date(2026, 9, 25), date(2026, 9, 27)), 'e', 2, 48, 'Sí'),
    ('Docentes', 'PROD', (date(2026, 9, 28), date(2026, 9, 30)), (date(2026, 9, 30), date(2026, 10, 2)), 'e', 5, 10, 'Sí'),
    ('Carga LD01 con equivalencias', 'PROD', (date(2026, 9, 30), date(2026, 10, 2)), None, 'o', None, None, None),
    ('Matriz de seguridad', 'PROD', (date(2026, 9, 30), date(2026, 10, 2)), None, 'o', None, None, None),
    ('Clonación a TEST', '', (date(2026, 10, 5), date(2026, 10, 9)), None, 'o', None, None, None),
    ('Estudiantes', 'TEST', (date(2026, 10, 12), date(2026, 10, 16)), (date(2026, 10, 16), date(2026, 10, 21)), 'e', 7, 48, 'Sí'),
    ('Historia académica', 'TEST', (date(2026, 10, 19), date(2026, 10, 28)), (date(2026, 10, 28), date(2026, 10, 30)), 'e', 42, 48, 'Sí'),
    ('Egresados', 'TEST', (date(2026, 10, 29), date(2026, 11, 2)), (date(2026, 11, 2), date(2026, 11, 4)), 'e', 5, 15, 'Por confirmar'),
    ('Saldos', 'TEST', (date(2026, 11, 3), date(2026, 11, 6)), (date(2026, 11, 6), date(2026, 11, 13)), 'e', 5, 48, 'Sí'),
    ('Tesis', 'TEST', (date(2026, 11, 9), date(2026, 11, 10)), (date(2026, 11, 10), date(2026, 11, 13)), 'e', 3, 0, 'No aplica'),
    ('Escuela de procedencia', 'TEST', (date(2026, 11, 11), date(2026, 11, 13)), (date(2026, 11, 13), date(2026, 11, 16)), 'e', 3, 48, 'Por confirmar'),
    ('Pruebas integrales (USS)', 'TEST', None, (date(2026, 11, 16), date(2026, 12, 26)), 'p', None, None, None),
]

TIEMPOS = [
    ('01 Persona', 'SPAIDEN, SOAFOLK, GOAMEDI, SOAHOLD', '5 + 3 + 2 + 2', 12, 'Sí'),
    ('01a Datos adicionales', 'GVAADID', '2', 2, 'Sí'),
    ('01b Escuela de procedencia', 'SOAPCOL', '3', 3, 'Por confirmar'),
    ('01b Contacto de emergencia', 'SPAEMRG', '2', 2, 'Sí'),
    ('02 Estudiantes', 'SGASTDN, SGASADD', '5 + 2', 7, 'Sí'),
    ('03 Historia académica', 'SHACRSE, SHATCKN, SHATERM, SHAINST, SMARQCM, SMICRLT, SFPPROJ, SFAPROJ', '10 + 6 + 3 + 10 + 3 + 10', 42, 'Sí'),
    ('04 Docentes', 'SIAINST', '5 (por docente)', 5, 'Sí'),
    ('05 Saldos', 'TSAAREV', '5', 5, 'Sí'),
    ('06 Egresados', 'SGASTDN, SHADEGR', '5', 5, 'Por confirmar'),
    ('07 Tesis', 'SHAQPNO', '3', 3, 'No aplica'),
]

RESP = [
    ('Definir por plantilla los datos a revisar según la validación funcional.', 'Qué validar y prueba funcional por plantilla.', 'PDF · sección 4'),
    ('Consolidar una planilla Excel con los datos e IDs revisados.', 'Una fila por dato revisado, con listas desplegables.', 'Excel · Revisión'),
    ('Registrar cada error en un Issue log (definición conjunta con Ellucian).', 'Propuesta: severidad, evidencia, responsable y estado.', 'Excel · Issue log'),
    ('Respetar los plazos de revisión.', 'Personas, documento y contacto hasta el 27/09; Docentes del 30/09 al 02/10.', 'Excel · Cronograma'),
    ('La revisión se hace directamente en Banner Student.', 'Captura de pantalla como evidencia de cada error.', 'Issue log · Evidencia'),
    ('Calcular el % de correctitud para presentarlo al comité.', 'Automático por criterio, plantilla y centro frente al umbral.', 'Excel · Resumen'),
]


def dd(d):
    return f'{d.day:02d}/{d.month:02d}'


def situacion(e):
    if e[3] is None:
        return ''
    ini, fin = e[3]
    if e[7] == 'No aplica':
        return '<span class="ap na">No aplica</span>'
    if HOY < ini:
        return '<span class="ap soon">Próxima</span>'
    if HOY <= fin:
        return '<span class="ap now">En revisión</span>'
    return '<span class="ap na">Cerrada</span>'


def gantt_svg():
    W, L = 690, 170
    T0, T1 = date(2026, 9, 1), date(2027, 1, 1)
    span = (T1 - T0).days
    X = lambda d: L + (d - T0).days / span * (W - L - 46)
    top, rh, bh = 30, 15.5, 6.2
    H = top + len(CRONO) * rh + 10
    s = f'<svg viewBox="0 0 {W} {H:.0f}" class="viz" role="img" aria-label="Cronograma de carga y revisión Migración R2">'
    # ambientes
    prod = [i for i, e in enumerate(CRONO) if e[1] == 'PROD']
    test = [i for i, e in enumerate(CRONO) if e[1] == 'TEST']
    for name, idx, fill in (('PROD', prod, '#F6F2FA'), ('TEST', test, '#F3FAF6')):
        y0, y1 = top + idx[0] * rh, top + (idx[-1] + 1) * rh
        s += f'<rect x="{L - 4}" y="{y0:.1f}" width="{W - L + 4:.1f}" height="{y1 - y0:.1f}" fill="{fill}"/>'
        s += (f'<line x1="31" y1="{y0 + 2:.1f}" x2="31" y2="{y1 - 2:.1f}" stroke="#5C2193" stroke-width="2" stroke-linecap="round"/>'
              f'<text x="0" y="{(y0 + y1) / 2 + 3:.1f}" class="env">{name}</text>')
    # meses
    for m, lab in ((9, 'Setiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')):
        a = X(date(2026, m, 1))
        b = X(date(2026 + (m == 12), m % 12 + 1, 1))
        s += f'<line x1="{a:.1f}" y1="{top - 14}" x2="{a:.1f}" y2="{H - 6:.1f}" class="grid"/>'
        s += f'<text x="{(a + b) / 2:.1f}" y="{top - 17}" class="tick" text-anchor="middle">{lab}</text>'
        for day in (8, 15, 22):
            xd = X(date(2026, m, day))
            s += f'<line x1="{xd:.1f}" y1="{top - 6}" x2="{xd:.1f}" y2="{H - 6:.1f}" class="grid2"/>'
    for i, e in enumerate(CRONO):
        y = top + i * rh + rh / 2
        faded = e[7] == 'No aplica'
        op = ' opacity="0.35"' if faded else ''
        s += f'<text x="38" y="{y + 2.6:.1f}" class="gl{" mut" if faded else ""}">{html.escape(e[0])}</text>'
        if e[2]:
            a, b = e[2]
            col = C_OTRA if e[4] == 'o' else C_CARGA
            s += f'<rect x="{X(a):.1f}" y="{y - bh - 0.6:.1f}" width="{max(X(b) - X(a) + 2.2, 2.5):.1f}" height="{bh}" rx="2" fill="{col}"{op}/>'
        if e[3]:
            a, b = e[3]
            s += f'<rect x="{X(a):.1f}" y="{y + 0.6:.1f}" width="{max(X(b) - X(a) + 2.2, 2.5):.1f}" height="{bh}" rx="2" fill="{C_REV}"{op}/>'
            lab = 'No aplica a CE' if faded else f'{dd(a)} – {dd(b)}'
            s += f'<text x="{X(b) + 5:.1f}" y="{y + 6:.1f}" class="dur">{lab}</text>'
        elif e[2]:
            a, b = e[2]
            s += f'<text x="{X(b) + 5:.1f}" y="{y + 1.5:.1f}" class="dur">{dd(a)} – {dd(b)}</text>'
    xh = X(HOY) + 1
    s += (f'<line x1="{xh:.1f}" y1="{top - 8}" x2="{xh:.1f}" y2="{H - 4:.1f}" stroke="#1E1E24" stroke-width="1" stroke-dasharray="3 2"/>'
          f'<rect x="{xh - 17:.1f}" y="{top - 13.5}" width="34" height="10" rx="3" fill="#1E1E24"/>'
          f'<text x="{xh:.1f}" y="{top - 6.2}" class="hoy" text-anchor="middle">Hoy 25/09</text>')
    return s + '</svg>'


def sections(section, table, fmt, chips):
    b = []
    # 6. Criterios
    b.append(section(6, 'Criterios de aceptación',
                     'La revisión se acepta cuando los datos obligatorios están, los formatos son correctos, no hay duplicados ni '
                     'inconsistencias relevantes, las relaciones están íntegras y las conciliaciones están dentro de la tolerancia. '
                     'Toda excepción se documenta, justifica y aprueba antes de la aceptación final.'))
    rows = [[f'<span class="n">{i}</span>', f'<b>{c}</b>', fmt(q), f'<b class="umb">{u}</b>', fmt(e)]
            for i, (c, q, u, e) in enumerate(CRITERIOS, 1)]
    b.append(table([('N°', 5), ('Criterio', 16), ('Qué significa', 31), ('Umbral mínimo', 10), ('Ejemplo en Centros Empresariales', 38)], rows, 'crit'))
    b.append('<div class="grid2 calc"><div class="formula"><div class="fl">% de correctitud</div>'
             '<div class="fx"><span>datos conformes</span><i></i><span>datos revisados</span></div>'
             '<p>Los «Observado» no cuentan como correctos hasta que la excepción esté aprobada.</p></div>'
             '<div class="note">Con muestras pequeñas los umbrales casi no dejan margen. Con <b>48 participantes</b>, '
             '<b>Unicidad (mínimo 99,5%)</b> significa <b>cero duplicados</b>. Con 10 campos por participante (480 datos), '
             '<b>Exactitud (mínimo 98%)</b> admite como máximo <b>9 datos con error</b>, e Integridad (mínimo 99%), como máximo 4.</div></div>')

    # 7. Tiempos y cronograma
    b.append(section(7, 'Tiempos y cronograma de revisión',
                     'Ellucian estima 86 minutos por alumno (1,4 h). Sin tesis, en Centros Empresariales son 83 minutos por participante.'))
    rows = [[f'<b>{p}</b>', chips(g), t, f'<b>{m}</b>',
             '<span class="ap ok">Sí</span>' if a == 'Sí' else ('<span class="ap tbc">Por confirmar</span>' if a == 'Por confirmar' else '<span class="ap na">No aplica</span>')]
            for p, g, t, m, a in TIEMPOS]
    rows.append(['<b>Total</b>', '', 'Ellucian: 86 min (1,4 h)', '<b>83</b>', 'Sin tesis'])
    b.append(table([('Plantilla', 22), ('Páginas', 38), ('Minutos', 18), ('Min', 8), ('Aplica a CE', 14)], rows, 'tiem'))
    b.append('<h3 class="h3gap">Cronograma Migración R2 <span class="eg">carga Ellucian/USS y revisión USS; la muestra de CE es una propuesta</span></h3>')
    legend = ('<div class="legend">'
              f'<span><i style="background:{C_CARGA}"></i>Carga en Banner (Ellucian/USS)</span>'
              f'<span><i style="background:{C_REV}"></i>Revisión y pruebas (USS)</span>'
              f'<span><i style="background:{C_OTRA}"></i>Otras actividades</span></div>')
    b.append(f'<figure class="fig">{legend}{gantt_svg()}</figure>')
    rows, tot = [], 0
    for e in CRONO:
        if e[3] is None or e[4] == 'p':
            continue
        h = (e[5] * e[6] / 60) if e[7] != 'No aplica' else None
        tot += h or 0
        ini, fin = e[3]
        rows.append([f'<b>{e[0]}</b>', e[1], f'{dd(ini)} – {dd(fin)}', str(e[5]) if h is not None else '—',
                     str(e[6]) if h is not None else '—', f'<b>{h:.1f}</b>'.replace('.', ',') if h is not None else '—', situacion(e)])
    rows.append(['<b>Total</b>', '', '', '', '', f'<b>{tot:.1f}</b>'.replace('.', ','), ''])
    b.append(table([('Etapa', 26), ('Ambiente', 10), ('Revisión USS', 16), ('Min por caso', 12), ('Muestra CE', 11),
                    ('Horas CE', 10), ('Al 25/09', 15)], rows, 'plan'))
    b.append('<div class="note warn"><b>Punto crítico: Historia académica.</b> Son unas 34 horas de revisión en solo 3 días '
             '(28 al 30 de octubre), unas 11 horas por día. Conviene asignar desde ya al menos <b>2 revisores</b> a tiempo completo '
             'para Centros Empresariales. Muestra usada: 16 participantes × 3 centros = 48; 10 docentes; 5 egresados por centro.</div>')

    # 8. Responsabilidades
    b.append(section(8, 'Responsabilidades de la USS', 'Cómo las cumple Centros Empresariales con este documento y la planilla Excel que lo acompaña.'))
    rows = [[f'<span class="n">{i}</span>', fmt(r), fmt(c), f'<span class="tool">{h}</span>'] for i, (r, c, h) in enumerate(RESP, 1)]
    b.append(table([('N°', 5), ('Responsabilidad (Ellucian)', 40), ('Cómo se cumple en Centros Empresariales', 37), ('Dónde', 18)], rows, 'resp'))
    b.append('<div class="legend3">'
             '<div><span class="ap ok">Conforme</span>Igual al sistema anterior y funciona en Banner.</div>'
             '<div><span class="ap tbc">Observado</span>Diferencia menor o explicada; se documenta y se aprueba.</div>'
             '<div><span class="ap bad">No conforme</span>Falta, se duplica o bloquea un proceso: va al Issue log.</div>'
             '</div>')
    return b


CSS = '''
.fig { margin: 2px 0 6px; break-inside: avoid; }
svg.viz { width: 100%; height: auto; display: block; font-family: 'InterStatic', sans-serif; }
svg .grid { stroke: #E4E1E9; stroke-width: .6; }
svg .tick { font-size: 7px; fill: #5F5F6B; font-weight: 600; }
svg .gl { font-size: 6.8px; font-weight: 600; fill: #3A3A44; }
svg .dur { font-size: 6px; fill: #5F5F6B; }
.legend { display: flex; flex-wrap: wrap; gap: 14px; font-size: 7.8pt; color: var(--mut); margin: 0 0 4px 2px; }
.legend i { display: inline-block; width: 16px; height: 7px; border-radius: 2px; margin-right: 5px; vertical-align: 0; }
.status { display: grid; grid-template-columns: auto 1fr; gap: 0; margin: 10px 0 0; border: 1px solid #F3C9B4; border-radius: 9px;
          overflow: hidden; break-inside: avoid; }
.status .d { background: #eb6834; color: #fff; font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 8.4pt;
             padding: 8px 12px; display: flex; flex-direction: column; justify-content: center; line-height: 1.2; }
.status .d small { font-family: 'InterStatic', sans-serif; font-weight: 600; font-size: 7.2pt; opacity: .9; }
.status ul { margin: 0; padding: 7px 12px 7px 26px; background: #FFF6F1; font-size: 8.3pt; line-height: 1.45; }
.status li b { color: #A63F12; }
svg .env { font-family: 'Montserrat', sans-serif; font-size: 7.6px; font-weight: 700; fill: #5C2193; letter-spacing: .08em; }
svg .grid2 { stroke: #EEEAF2; stroke-width: .5; }
svg .gl.mut { fill: #A3A3AD; }
svg .hoy { font-size: 6.2px; font-weight: 700; fill: #fff; }
table.crit td:nth-child(2), table.crit th:nth-child(2), table.tiem td:first-child, table.tiem th:first-child,
table.plan td:first-child, table.plan th:first-child { text-align: left; }
table.crit td:nth-child(4), table.crit th:nth-child(4) { text-align: center; }
.umb { color: var(--pd); white-space: nowrap; }
table.tiem td:nth-child(3), table.tiem td:nth-child(4), table.tiem td:nth-child(5), table.tiem th:nth-child(n+3) { text-align: center; }
table.tiem tbody tr:last-child td, table.plan tbody tr:last-child td { background: var(--gl); border-top: 1px solid #D3EAC7; }
table.plan td, table.plan th { text-align: center; }
table.plan td:first-child { text-align: left; }
.ap.now { background: #FFE6DA; color: #A63F12; } .ap.soon { background: var(--pl); color: var(--pd); }
.grid2.calc { grid-template-columns: .9fr 1.5fr; align-items: stretch; margin-top: 8px; }
.formula { border: 1px solid var(--pb); background: var(--pl); border-radius: 8px; padding: 8px 12px; }
.formula .fl { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 8.4pt; color: var(--pd); }
.formula .fx { display: flex; flex-direction: column; align-items: center; margin: 5px 0 4px; font-weight: 700; font-size: 8.6pt; }
.formula .fx i { display: block; width: 70%; height: 1.5px; background: var(--ink); margin: 3px 0; }
.formula p { margin: 0; font-size: 7.6pt; color: var(--mut); text-align: center; }
.grid2.calc .note { margin: 0; }
.tool { display: inline-block; font-weight: 700; font-size: 7.6pt; color: var(--gd); background: var(--gl); border-radius: 5px; padding: 1px 6px; }
table.resp td:last-child, table.resp th:last-child { text-align: center; }
'''

STATUS = ('<div class="status"><div class="d">Situación<small>al 25/09/2026</small></div><ul>'
          '<li><b>En revisión (PROD):</b> Personas (24–27/09), Documento de identidad y Contacto de emergencia (25–27/09).</li>'
          '<li><b>Siguiente:</b> Docentes, carga 28–30/09 y revisión 30/09–02/10.</li>'
          '<li><b>Luego:</b> clonación a TEST (05–09/10), Estudiantes a Escuela de procedencia, y pruebas integrales (16/11–26/12).</li>'
          '</ul></div>')
