# -*- coding: utf-8 -*-
"""EJEMPLO DE REFERENCIA: «Inglés, Informática y Emprendimiento en Ellucian» (10 páginas, versión del 26/09/2026).

Muestra el estilo que prefiere el usuario: «Hoy en SEUSS» frente a «En Ellucian», ejemplos por centro en tarjetas,
pocas tablas, el significado de cada sigla entre paréntesis (explicar) con glosario y todas las dudas al final.
Copia este archivo para un documento nuevo y cambia los datos.

Uso: python3 ejemplo_centros.py [salida.pdf]
"""
import html
import sys

from common import AUTHOR, GLOS_CSS, check_pdf, explicar, fmt, glosario_html, header, render, section

OUT = sys.argv[1] if len(sys.argv) > 1 else 'INGLÉS, INFORMÁTICA Y EMPRENDIMIENTO EN ELLUCIAN - EJEMPLOS - CENTROS EMPRESARIALES.pdf'

ARROW = ('<svg class="arr" viewBox="0 0 14 14" aria-hidden="true"><path d="M3 7h7M7 3.5 10.5 7 7 10.5" fill="none" '
         'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')

# ------------------------------------------------------------------ reglas comunes (SEUSS vs Ellucian)
REGLAS = [
    ('Periodos',
     ['Tres periodos al año: **2026-0** (verano), **2026-I** (primer periodo) y **2026-II** (segundo periodo).'],
     ['Los mismos tres periodos, con código de 6 dígitos: año + nivel **5** (Centros Empresariales) + secuencia: '
      '**202651**, **202654** y **202656**. El verano 2027 será 202751.',
      'Cada grupo que empieza en el mes es una **parte de periodo** con sus propias fechas: Inglés I01 a I12, Informática X01 a X12, Emprendimiento P01 a P12.'],
     'Instructivo 1.1.1 y Tema 1 · STVTERM, SOATERM'),
    ('Horas de clase',
     ['**Hora cronológica:** la hora de clase. De día dura **45 minutos** y de noche **50 minutos**; en los dos casos cuenta como 1 hora.',
      '**Hora pedagógica:** la hora presencial de **60 minutos**, como la hora de trabajo.'],
     ['La hora de clase se llama **hora académica**. Sus minutos se ponen en SIATERM, campo **Factor de duración** '
      '(el instructivo usa 50 minutos). Es **un solo valor por periodo**.',
      'Con ese valor, SSASECT calcula las horas por semana de cada NRC a partir del horario (hora de inicio y fin, formato 24 h).',
      'La carga docente usa esas horas y el factor FTE (en el instructivo, 50 horas = 1 tiempo completo). '
      'No aparece un campo aparte para la hora de 60 minutos.'],
     'Instructivos 5.2 Carga de trabajo docente y 5.3 Oferta horaria'),
    ('Docentes',
     ['La carga docente de los centros se arma en **Excel**.',
      'Se quiere saber si un curso puede tener varios docentes y si un docente puede tener varios cursos.'],
     ['Un NRC puede tener **2 o 3 docentes**; uno se marca como **principal**. Cada uno lleva su % de responsabilidad y su % de sesión.',
      'Un docente puede estar en **varios NRC**; SIAASGN muestra toda su carga.',
      'Si dos NRC del mismo docente se cruzan de horario, Banner no deja asignarlo, salvo que se marque el **indicador de sobrepaso**.'],
     'Instructivos 6.2.1 Asignar docentes y 5.3 Oferta horaria'),
    ('Notas, asistencia y aula virtual',
     ['Se quiere confirmar cómo se validan las notas, cómo se vincula el aula virtual y si las notas pasan de allí al sistema '
      'con su programación.'],
     ['Registros Académicos carga el **plan de evaluación** de cada NRC en SHAGCOM: componentes con su peso (%) y subcomponentes.',
      'El docente registra notas y asistencia por **autoservicio**, solo en las fechas abiertas en SOATERM.',
      'La asistencia puede decidir la aprobación: componente de asistencia con peso 0 y marcado «debe aprobar» '
      '(el instructivo usa un mínimo de 70%).',
      'Al cierre del periodo, SHRROLL pasa las notas finales a la historia académica.',
      'El NRC se vincula al aula virtual con el campo **Socio de integración** de SSASECT y sus datos se envían al aula virtual. '
      'Los instructivos **no dicen** que las notas regresen del aula virtual a Banner.'],
     'Instructivos 7.1.0, 7.1.4, 7.1.9 y 6.2.4'),
]

# grupos 2026 por periodo (cronograma del Tema 1)
GRUPOS = [
    ('202651', 'Ciclo de verano', '2026-0', 'ene – mar',
     [('I01', 'ene'), ('I02', 'feb'), ('I03', 'mar')], [('X01', 'ene'), ('X02', 'feb')], [('P01', 'ene'), ('P02', 'feb'), ('P03', 'mar')]),
    ('202654', 'Semestre I', '2026-I', 'abr – jul',
     [('I04', 'abr'), ('I05', 'may'), ('I06', 'jun'), ('I07', 'jul')], [('X03', 'abr'), ('X04', 'jun')], [('P04', 'may')]),
    ('202656', 'Semestre II', '2026-II', 'ago – dic',
     [('I08', 'ago'), ('I09', 'sep'), ('I10', 'oct'), ('I11', 'nov'), ('I12', 'dic')], [('X05', 'ago'), ('X06', 'sep'), ('X07', 'nov')], [('P05', 'ago'), ('P06', 'sep')]),
]

CURSOS_ING = [('BASIC I', '8 semanas'), ('BASIC II', '8 semanas'), ('BASIC III', '12–13 semanas'),
              ('INTERMEDIATE I', '8 semanas'), ('INTERMEDIATE II', '8 semanas'), ('INTERMEDIATE III', '12–13 semanas')]

GRUPOS_INF = [('X01', '12/1 – 22/2', '6'), ('X02', '23/2 – 22/3', '4'), ('X03', '6/4 – 31/5', '8'), ('X04', '1/6 – 12/7', '6'),
              ('X05', '3/8 – 30/8', '4'), ('X06', '7/9 – 31/10', '8'), ('X07', '2/11 – 13/12', '6')]

GRUPOS_EMP = [('P01', '7/1 – 15/3', '202651'), ('P02', '4/2 – 12/4', '202651'), ('P03', '11/3 – 17/5', '202651'),
              ('P04', '6/5 – 12/7', '202654'), ('P05', '5/8 – 11/10', '202656'), ('P06', '30/9 – 6/12', '202656')]

PRUEBAS = [
    ('Periodos', ['Existen 202651, 202654 y 202656 con sus fechas.',
                  'Partes de periodo I01 a I12, X01 a X07 y P01 a P06 con las fechas del cronograma.',
                  'Fechas web de inscripción y de ingreso de notas abiertas.']),
    ('Mallas y programas', ['El programa de Inglés tiene sus 6 cursos en orden.',
                            'Los programas de Informática y Emprendimiento tienen sus cursos.',
                            'El CAPP de un participante muestra lo aprobado y lo pendiente.']),
    ('Creación de NRC', ['Un NRC de Inglés de noche y uno de Informática de día: revisar las horas por semana.',
                         'Un NRC con dos docentes (uno principal).',
                         'Un docente en tres NRC, y el aviso de cruce de horario.',
                         'Dos grupos de Emprendimiento que se cruzan (P02 y P03) con el mismo docente.',
                         'Un NRC vinculado al aula virtual.']),
    ('Matrículas', ['Backoffice: inscribir en BASIC II con BASIC I aprobado (debe dejar) y desaprobado (debe salir error).',
                    'Con examen de suficiencia registrado, debe dejar inscribir en BASIC II.',
                    'Autoservicio: el participante se inscribe en las fechas web.',
                    'La inscripción genera el cobro en su cuenta.']),
    ('Notas', ['Plan de evaluación cargado en un NRC.',
               'El docente registra notas y asistencia por autoservicio.',
               'Un componente «debe aprobar» que desaprueba el curso.',
               'Cierre: las notas pasan a la historia académica.']),
]

DUDAS_ELLUCIAN = [
    'Hora de clase de **45 minutos de día** y **50 de noche** en el mismo periodo: ¿cómo se configura si SIATERM tiene un solo '
    'factor de duración? (ver ejemplos I-2 y X-3)',
    'Aula virtual: ¿las notas **regresan** a Banner? ¿Qué datos salen hacia el aula virtual: NRC, docente, participantes, plan de evaluación?',
    'Hora pedagógica de **60 minutos**: si se necesita (por ejemplo, para la carga o el pago del docente), ¿dónde se registra?',
    'Si un participante pasa a BASIC II con **examen de suficiencia**, ¿cómo queda BASIC I en su historia académica y en CAPP: '
    'pendiente o reconocido?',
    'Casilla **«En progreso»** de SOATERM: con grupos seguidos (I04 termina el 31/5 e I06 empieza el 1/6), ¿se marca? Si se marca y '
    'luego desaprueba BASIC I, ¿Banner lo retira de BASIC II o se hace a mano? (ver ejemplo I-4)',
    '¿Los programas de los tres centros tendrán su malla en CAPP (SMAPROG, SMAAREA) para ver el avance del participante?',
]
DUDAS_USS = [
    'Examen de suficiencia de Inglés: ¿qué **puntaje mínimo** se exige y quién lo registra en Banner?',
    '¿Quién podrá dar **sobrepasos** de prerrequisito en SFAROVR? En SEUSS ese camino no existe.',
    'Informática y Emprendimiento: ¿los cursos tienen orden (uno pide aprobar otro) o todos son independientes?',
    '¿Qué **asistencia mínima** se exige para aprobar en los centros? (el instructivo usa 70% como ejemplo)',
    '¿Quién carga el **plan de evaluación** de cada NRC: Registros Académicos (como dice el instructivo) o el centro?',
    'Nombres reales de los cursos de Informática y Emprendimiento, pesos de evaluación y nota aprobatoria (en este documento son de ejemplo).',
]


# ------------------------------------------------------------------ piezas
def bullets(items):
    return '<ul>' + ''.join(f'<li>{fmt(x)}</li>' for x in items) + '</ul>'


def regla(i, t, seuss, ell, src):
    return explicar(f'<div class="rule"><div class="rh"><span class="k">{i}</span>{html.escape(t)}</div><div class="rc">'
            f'<div class="blk seuss"><span class="lab">Hoy en SEUSS</span>{bullets(seuss)}</div>'
            f'<div class="blk ell"><span class="lab">En Ellucian</span>{bullets(ell)}<div class="src">{html.escape(src)}</div></div>'
            f'</div></div>')


def row(kind, text):
    lab = {'seuss': 'Hoy en SEUSS', 'conf': 'Qué confirmar', 'ell': 'En Ellucian', 'res': 'Resultado', 'ojo': 'Ojo'}[kind]
    return f'<div class="r {kind}"><span class="lab">{lab}</span><div>{text}</div></div>'


def ex(code, ctr, title, case, rows, extra=''):
    name = {'ing': 'Inglés', 'inf': 'Informática', 'emp': 'Emprendimiento'}[ctr]
    return explicar(f'<div class="ex {ctr}"><div class="exh"><span class="exn">{code}</span><b>{html.escape(title)}</b>'
            f'<span class="ctr">{name}</span></div><div class="case"><span class="lab">Caso</span><div>{fmt(case)}</div></div>'
            + ''.join(row(k, fmt(t) if isinstance(t, str) and not t.startswith('<') else t) for k, t in rows)
            + extra + '</div>')


def flow(items):
    return '<div class="flow">' + ARROW.join(f'<span class="{c}">{fmt(t)}</span>' for t, c in items) + '</div>'


def periodos_fig():
    cols = ''
    for code, name, seuss, meses, ing, inf, emp in GRUPOS:
        pi = ''.join(f'<span class="gp ing">{g}<i>{m}</i></span>' for g, m in ing)
        px = ''.join(f'<span class="gp inf">{g}<i>{m}</i></span>' for g, m in inf)
        pe = ''.join(f'<span class="gp emp">{g}<i>{m}</i></span>' for g, m in emp)
        cols += (f'<div class="pc"><div class="ph"><span class="pcode">{code}</span><span class="pn">{name} · {meses}</span>'
                 f'<span class="ps">SEUSS {seuss}</span></div>'
                 f'<div class="pr"><span class="pl">Inglés</span><div>{pi}</div></div>'
                 f'<div class="pr"><span class="pl">Informática</span><div>{px}</div></div>'
                 f'<div class="pr"><span class="pl">Emprendim.</span><div>{pe}</div></div></div>')
    return f'<div class="pfig">{cols}</div>'


def cursos_ing():
    return '<div class="chain">' + ''.join(
        f'<div class="chev{" lvl3" if "III" in c else ""}"><b>{c}</b><span>{d}</span></div>' for c, d in CURSOS_ING) + '</div>'


def grupos_inf():
    return '<div class="xg">' + ''.join(
        f'<div class="xc"><b>{g}</b><span>{f}</span><i>{s} semanas</i></div>' for g, f, s in GRUPOS_INF) + '</div>'


def factores():
    def cell(v, ok):
        return f'<td><b>{v}</b> <span class="ap {"ok" if ok else "bad"}">{"Coincide" if ok else "No coincide"}</span></td>'
    return ('<table class="fx"><thead><tr><th>Factor de duración en SIATERM</th><th>Día · 90 min<br><i>SEUSS: 2 horas</i></th>'
            '<th>Noche · 100 min<br><i>SEUSS: 2 horas</i></th></tr></thead><tbody>'
            f'<tr><td>45 minutos</td>{cell("2,0 horas", True)}{cell("2,2 horas", False)}</tr>'
            f'<tr><td>50 minutos</td>{cell("1,8 horas", False)}{cell("2,0 horas", True)}</tr></tbody></table>')


def caminos():
    items = [('A', 'Sin examen', 'Al inscribirlo en BASIC II, SFAREGS muestra el error de prerrequisito y **no lo inscribe**. '
                                 'Debe repetir BASIC I en el siguiente grupo.', 'ok', 'Igual que SEUSS'),
             ('B', 'Con examen de suficiencia', 'Registros Académicos registra su puntaje en SOATEST. Si llega al mínimo, Banner '
                                                '**sí** lo deja inscribirse en BASIC II.', 'ok', 'Igual que SEUSS'),
             ('C', 'Con sobrepaso', 'Un usuario con permiso puede dar un sobrepaso de prerrequisito en SFAROVR y saltar la regla. '
                                    'En SEUSS este camino no existe: debe darlo solo quien esté autorizado.', 'tbc', 'Controlar')]
    return '<div class="paths">' + ''.join(
        f'<div class="path {c}"><div class="pt"><span class="pk">{k}</span>{t}</div><p>{fmt(d)}</p>'
        f'<span class="ap {c}">{s}</span></div>' for k, t, d, c, s in items) + '</div>'


def config_prerreq():
    pasos = [('En SCAPREQ, BASIC II lleva el prerrequisito «BASIC I aprobado **o** examen de suficiencia con puntaje mínimo». '
              'Cada NRC de BASIC II lo hereda en SSAPREQ.', '1.1.5, diap. 18; 5.3, diap. 41 y 42'),
             ('En SOATERM, la verificación de «Prerrequisitos» se pone en **Fatal**: Banner no deja inscribir a quien no lo cumple.',
              '5.4 Inscripción por backoffice, diap. 14 y 15'),
             ('El puntaje del examen de suficiencia se registra en SOATEST.', '3.2.2, diap. 14'),
             ('La proyección (SFPPROJ) con verificación de prerrequisitos no le ofrece BASIC II.', '5.4 Proyección, diap. 34')]
    return ('<div><b>Sí, las dos cosas.</b> Se configura así:<ol class="steps1">'
            + ''.join(f'<li>{fmt(t)} <span class="cite">Instructivo {c}</span></li>' for t, c in pasos) + '</ol></div>')


def notas_calc():
    comp = [('Speaking', '30%', '16', '4,8'), ('Writing', '30%', '14', '4,2'), ('Examen final', '40%', '15', '6,0')]
    rows = ''.join(f'<div class="cr"><span>{n}</span><span>{p}</span><span>{v}</span><b>{r}</b></div>' for n, p, v, r in comp)
    return ('<div class="calc"><div class="cr ch"><span>Componente</span><span>Peso</span><span>Nota</span><span>Aporta</span></div>'
            f'{rows}<div class="cr tot"><span>Nota final</span><span>100%</span><span></span><b>15,0</b></div>'
            '<div class="cr att"><span>Asistencia</span><span>0% · debe aprobar</span><span>mín. 70%</span><b>—</b></div></div>')


def grupos_emp():
    return '<div class="xg eg6">' + ''.join(
        f'<div class="xc emp"><b>{g}</b><span>{f}</span><i>10 semanas · {p}</i></div>' for g, f, p in GRUPOS_EMP) + '</div>'


def notas_emp():
    comp = [('Avance del plan de negocio 1', '30%', '18', '5,4'), ('Avance del plan de negocio 2', '30%', '18', '5,4'),
            ('Pitch final · debe aprobar', '40%', '12', '4,8')]
    rows = ''.join(f'<div class="cr{" must" if "debe" in n else ""}"><span>{n}</span><span>{p}</span><span>{v}</span><b>{r}</b></div>'
                   for n, p, v, r in comp)
    return ('<div class="calc"><div class="cr ch"><span>Componente</span><span>Peso</span><span>Nota</span><span>Aporta</span></div>'
            f'{rows}<div class="cr tot"><span>Nota final</span><span>100%</span><span></span><b>15,6</b></div></div>')


def emprendimiento():
    b = ['<div class="keep">' + section(4, 'Emprendimiento: ejemplos')
         + '<div class="intro2">Cronograma 2026: seis grupos, P01 a P06, cada uno con todos los cursos del grupo y siempre de '
           '<b>10 semanas</b>. Varios grupos se dictan a la vez. Para egresar, los estudiantes de pregrado deben cumplir el '
           'requisito de emprendimiento (instructivo 8).</div>' + grupos_emp() + '</div>']
    b.append(ex('E-1', 'emp', 'Grupo que termina en otro semestre', 'Un grupo empieza el 11 de marzo de 2026 y termina el 17 de mayo.', [
        ('ell', flow([('Inicio 11/3/2026', 'n'), ('Periodo **202651**', 'p'), ('Parte de periodo **P03**', 'p'),
                      ('Clases hasta el 17/5', 'g')])),
        ('ojo', 'El periodo lo da la parte de periodo, no la fecha de fin: P03 sigue en **202651** aunque sus clases lleguen a mayo, '
                'cuando ya corre el semestre I (202654).'),
    ]))
    b.append(ex('E-2', 'emp', 'Dos grupos al mismo tiempo', 'P02 (4/2 al 12/4) y P03 (11/3 al 17/5) se dictan a la vez entre el 11 de marzo '
                'y el 12 de abril. El mismo docente tiene un NRC en cada grupo, los dos los martes de 19:00 a 20:40.', [
        ('ell', 'Los dos NRC son del periodo 202651 y sus fechas se cruzan. Al asignar el segundo NRC, Banner avisa del **cruce de horario** '
                'y no lo asigna, salvo que se marque el indicador de sobrepaso.'),
        ('res', 'Lo normal es cambiar el horario de uno de los NRC o asignar otro docente.'),
    ]))
    b.append(ex('E-3', 'emp', 'Horas de un curso de 10 semanas', 'NRC de noche, martes y jueves de 19:00 a 20:40, durante las 10 semanas del grupo.', [
        ('seuss', '2 horas por día, 4 por semana: **40 horas** en total.'),
        ('ell', 'Con el factor de duración en 50, SSASECT muestra **4 horas por semana**. Las 10 semanas vienen de las fechas de la parte de '
                'periodo en SOATERM: 4 × 10 = **40 horas**.'),
        ('res', '<span class="ap ok">Coincide</span> En el turno noche cuadra igual que en SEUSS.'),
    ]))
    b.append(ex('E-4', 'emp', 'Notas con un componente que debe aprobarse', 'Plan de evaluación con el pitch final marcado «debe aprobar». '
                'Pesos y nota aprobatoria de ejemplo: escala de 0 a 20, aprueba con 14.', [
        ('ell', 'En SHAGCOM cada componente puede marcarse para que **deba aprobarse** para aprobar el curso (instructivo 7.1.4).'),
    ], notas_emp() + row('res', 'El promedio es <b>15,6</b>, pero el pitch final (12) no llega a 14 y debe aprobarse: '
                                '<b>desaprueba</b>. Con 14 o más en el pitch, aprueba.')))
    b.append(ex('E-5', 'emp', 'Requisito para egresar', 'Carla, de pregrado, aprobó todos los cursos de su carrera, Inglés y Computación, '
                'pero le falta Emprendimiento.', [
        ('ell', 'Para pasar al estado **EG** debe cumplir su malla, idiomas, emprendimiento y computación. '
                'El cambio de estado es masivo (instructivo 8, otorgamiento de grado).'),
        ('res', 'Carla todavía no pasa a egresada. Cuando apruebe Emprendimiento, entra en el siguiente cambio masivo a EG.'),
    ]))
    return b


def build():
    b = [header('Universidad Señor de Sipán · Centros Empresariales', 'Inglés, Informática y Emprendimiento en Ellucian',
                'Lo que se hace hoy en SEUSS, lo que dice Ellucian y ejemplos de cada centro',
                [('Elaborado por', AUTHOR), ('Fecha', '26 de septiembre de 2026'),
                 ('Fuentes', 'Notas del Zoom (SEUSS) · Instructivos de Ellucian · Tema 1'), ('Estado', 'Para confirmar')])]

    b.append(explicar('<div class="lead">Cada tema tiene el mismo orden: <span class="tg seuss">Hoy en SEUSS</span> es lo que se hace ahora en SEUSS, '
             'según las notas del Zoom; <span class="tg ell">En Ellucian</span> es lo que dicen los instructivos; los '
             '<b>ejemplos</b> muestran cómo quedaría en cada centro. <b>Todas las dudas están al final</b> (sección 7).</div>'))

    # 1. Reglas comunes
    b.append(section(1, 'Lo que vale para los tres centros'))
    b.append(regla(1, *REGLAS[0]))
    b.append('<div class="figcap">Grupos 2026 de cada centro dentro de su periodo (cronograma del Tema 1)</div>' + periodos_fig())
    for i, r in enumerate(REGLAS[1:], 2):
        b.append(regla(i, *r))

    # 2. Inglés
    b.append(section(2, 'Inglés: ejemplos'))
    b.append(explicar('<div class="intro2">Cursos del cronograma 2026. Cada mes empieza un grupo (I01 a I12). Para egresar, los estudiantes '
             'de pregrado deben cumplir el requisito de idiomas (instructivo 8, requisitos de graduación).</div>') + cursos_ing())

    b.append(ex('I-1', 'ing', 'En qué periodo cae un grupo', 'Ana empieza **BASIC I** el lunes 6 de abril de 2026.', [
        ('seuss', 'Periodo **2026-I**.'),
        ('ell', flow([('Inicio 6/4/2026', 'n'), ('Periodo **202654**', 'p'), ('Parte de periodo **I04**', 'p'),
                      ('Clases del 6/4 al 31/5 · 8 semanas', 'g')])),
        ('ojo', 'Si empieza el 7 de diciembre (grupo **I12**), el periodo es **202656** aunque las clases terminen el 31/1/2027.'),
    ]))
    b.append(ex('I-2', 'ing', 'Horario de noche y horas', 'NRC de BASIC I de noche: lunes y miércoles de 19:00 a 20:40 (100 minutos por día).', [
        ('seuss', '100 minutos = **2 horas** de 50 minutos por día y **4 horas** por semana.'),
        ('ell', 'Con el factor de duración en **50**, SSASECT calcula 100 ÷ 50 = **2 horas** por día y **4 horas** por semana.'),
        ('res', '<span class="ap ok">Coincide</span> Con 50 minutos, el turno noche cuadra igual que en SEUSS.'),
    ]))
    b.append(ex('I-3', 'ing', 'Aprueba BASIC I', 'Ana aprueba **BASIC I** del grupo I04, que termina el 31 de mayo.', [
        ('ell', flow([('Aprueba BASIC I · I04', 'n'), ('Se inscribe en **BASIC II** · I06, desde el 1/6', 'p'),
                      ('Prerrequisito: **cumple**', 'g')])),
        ('res', 'Queda inscrita. En CAPP se ve BASIC I **cumplido** y BASIC II **en curso**.'),
    ]))
    b.append(ex('I-4', 'ing', 'Desaprueba BASIC I: ¿puede pasar a BASIC II?', 'Luis desaprueba **BASIC I** en el grupo I04 (termina el '
                '31/5) y quiere inscribirse en **BASIC II** del grupo I06 (empieza el 1/6).', [
        ('seuss', 'Sale **desaprobado** y **no puede pasar** a BASIC II. La única forma de pasar sin aprobar BASIC I es rendir un '
                  '**examen de suficiencia**.'),
        ('conf', '¿Ellucian tiene un requisito que revise la nota de BASIC I y no lo deje pasar a BASIC II si está desaprobado? '
                 '¿Y permite pasar con examen de suficiencia?'),
        ('ell', config_prerreq()),
    ], caminos() + row('ojo', fmt('Casilla «En progreso» de SOATERM: si se marca, BASIC I en curso cuenta como cumplido y Luis podría '
                                  'inscribirse en BASIC II antes de tener su nota; cuando se califica, Banner vuelve a revisar el '
                                  'prerrequisito (instructivo 1.1.2, diap. 19). Como los grupos son seguidos, hay que definir si se marca.'))
       + row('res', fmt('Banner puede funcionar **igual que SEUSS**: desaprobado no pasa a BASIC II; con examen de suficiencia '
                        'aprobado, sí.'))))
    b.append(ex('I-5', 'ing', 'Dos docentes en un NRC', 'BASIC II de noche con dos docentes: Docente A dicta lunes y miércoles; '
                'Docente B dicta el viernes (conversación).', [
        ('ell', '<div class="sess"><div><b>Sesión 01</b> · lunes y miércoles · Docente A · <span class="ap ok">Principal</span> · 67%</div>'
                '<div><b>Sesión 02</b> · viernes · Docente B · 33%</div></div>'),
        ('res', 'El NRC queda con los dos docentes y cada uno lo ve en su carga, en SIAASGN. Los porcentajes son de ejemplo.'),
    ]))
    b.append(ex('I-6', 'ing', 'Notas y asistencia', 'Plan de evaluación de un NRC de BASIC I. Pesos de ejemplo, escala de 0 a 20.', [
        ('ell', flow([('Registros Académicos carga el plan', 'n'), ('El docente registra por autoservicio', 'p'),
                      ('Cierre: la nota pasa a la historia', 'g')])
                + f'<div class="subn">{fmt("Registros Académicos carga el plan de evaluación del NRC en SHAGCOM; el docente registra notas y asistencia en el autoservicio; al cierre, SHRROLL pasa la nota final a la historia académica.")}</div>'),
    ], notas_calc() + row('res', '<b>Rosa</b> saca 16, 14 y 15 con 90% de asistencia: <b>aprueba con 15,0</b>. '
                                 '<b>Luis</b> saca las mismas notas pero tiene 65% de asistencia: <b>desaprueba</b> por asistencia '
                                 '(en el ejemplo del instructivo queda con la nota INH).')))

    # 3. Informática
    b.append('<div class="keep">' + section(3, 'Centro de Informática: ejemplos'))
    b.append(explicar('<div class="intro2">Cronograma 2026: siete grupos, X01 a X07; cada grupo incluye todos los cursos del mes. El catálogo lo '
             'diseña el centro. Para egresar, los estudiantes de pregrado deben cumplir el requisito de computación (instructivo 8).</div>')
             + grupos_inf() + '</div>')

    b.append(ex('X-1', 'inf', 'Grupo corto de agosto', 'Grupo de Informática de 4 semanas, del 3 al 30 de agosto de 2026.', [
        ('seuss', 'Periodo **2026-II**.'),
        ('ell', flow([('Inicio 3/8/2026', 'n'), ('Periodo **202656**', 'p'), ('Parte de periodo **X05**', 'p'),
                      ('Todos sus cursos toman esas fechas', 'g')])),
    ]))
    b.append(ex('X-2', 'inf', 'Crear un NRC del grupo X03', 'Curso **Excel Básico** (nombre de ejemplo), grupo X03 (6/4 al 31/5/2026), '
                'de día, 25 cupos.', [
        ('ell', '<ol class="steps"><li>En SSASECT: periodo <b>202654</b> y el curso del catálogo.</li>'
                '<li>Parte de periodo <b>X03</b>: las fechas se llenan solas.</li><li>Cupo máximo: <b>25</b>.</li>'
                '<li>Horario: días, hora de inicio y hora de fin.</li><li>Docente principal y salón.</li>'
                '<li>Socio de integración, si usará el aula virtual.</li></ol>'),
        ('res', 'Banner genera el número de NRC y el curso queda listo para la matrícula.'),
    ]))
    b.append(ex('X-3', 'inf', 'Horario de día y horas', 'El NRC de Excel Básico es de día: martes y jueves de 08:00 a 09:30 (90 minutos por día).', [
        ('seuss', '90 minutos = **2 horas** de 45 minutos por día y **4 horas** por semana.'),
        ('ell', 'Con el mismo factor de **50** del turno noche, SSASECT calcula 90 ÷ 50 = **1,8 horas** por día y **3,6** por semana.'),
        ('res', '<span class="ap bad">No coincide</span> Con un solo factor por periodo, siempre falla un turno:'),
    ], factores() + '<p class="fxn">Por eso es la primera duda para Ellucian (sección 7).</p>'))
    b.append(ex('X-4', 'inf', 'Un docente en tres NRC', 'El mismo docente dicta tres NRC en el grupo X03: mañana (08:00 a 09:30), '
                'tarde (15:00 a 16:30) y noche (19:00 a 20:40).', [
        ('ell', 'Se le asigna en cada NRC, en SSASECT. En **SIAASGN** aparecen los tres NRC con sus horas.'),
        ('ojo', 'Si se le intenta asignar otro NRC a las 08:00 del mismo día, Banner avisa del cruce y no lo asigna, '
                'salvo que se marque el **indicador de sobrepaso**.'),
    ]))
    b.append(ex('X-5', 'inf', 'Curso que pide otro', '**Excel Intermedio** pide haber aprobado **Excel Básico** (nombres de ejemplo).', [
        ('ell', 'Igual que en Inglés (ejemplo I-4): en SCAPREQ se pone Excel Básico como prerrequisito, o «Excel Básico **o** examen con puntaje mínimo».'),
        ('res', 'Quien ya sabe Excel rinde el examen (puntaje en SOATEST) y entra directo al intermedio. '
                'Si los cursos no tienen orden, no se configura nada.'),
    ]))
    b.append(ex('X-6', 'inf', 'Aula virtual', 'El NRC de Excel Básico usará el aula virtual.', [
        ('ell', 'En SSASECT se llena **Socio de integración** con el código del aula virtual (creado en GTVINTP y relacionado en GORINTG). '
                'Así los datos del NRC se envían al aula virtual.'),
        ('ojo', 'Falta confirmar si las notas del aula virtual **regresan** a Banner (sección 7).'),
    ]))
    b.append(ex('X-7', 'inf', 'Matrícula', 'Pedro se matricula en Excel Básico del grupo X06.', [
        ('ell', '<div class="two"><div><b class="twh">Backoffice</b>Registros Académicos lo inscribe por backoffice en <span class="code">SFAREGS</span>.</div>'
                '<div><b class="twh">Autoservicio</b>Pedro se inscribe solo por autoservicio, en las fechas web del periodo que fija <span class="code">SOATERM</span>.</div></div>'),
        ('res', 'En los dos casos Banner revisa cupo, prerrequisitos y cruces de horario. La inscripción genera el cobro según lo '
                'configurado en SFARGFE.'),
    ]))

    # 4. Emprendimiento
    b += emprendimiento()

    # 5. Qué probar
    b.append(section(5, 'Qué probar', 'Según la lista de pruebas del Zoom, con casos de los tres centros.'))
    b.append('<div class="tests">' + ''.join(explicar(
        f'<div class="tc"><div class="tt"><span class="k">{i}</span>{t}</div>'
        + ''.join(f'<div class="ti"><span class="bx"></span><div>{fmt(x)}</div></div>' for x in items) + '</div>')
        for i, (t, items) in enumerate(PRUEBAS, 1)) + '</div>')

    # 6. Dudas (se arman antes del glosario para que sus términos entren en él)
    dudas = ('<div class="dudas"><div class="dc">' + explicar('<div class="dh">Para Ellucian</div><ol>'
             + ''.join(f'<li>{fmt(q)}</li>' for q in DUDAS_ELLUCIAN) + '</ol>') + '</div>'
             f'<div class="dc uss">' + explicar(f'<div class="dh">Para la USS</div><ol start="{len(DUDAS_ELLUCIAN) + 1}">'
             + ''.join(f'<li>{fmt(q)}</li>' for q in DUDAS_USS) + '</ol>') + '</div></div>')

    # 6. Glosario
    b.append(section(6, 'Glosario', 'Qué significa cada sigla y cada página de Banner que aparece en el documento.'))
    b.append('<div class="glos keep"><div class="gh">Grupos y periodos</div><div class="gg">'
             '<div class="gi"><b>I01…I12</b><span>Partes de periodo (grupos del mes) de Idiomas.</span></div>'
             '<div class="gi"><b>X01…X12</b><span>Partes de periodo de Computación (Informática).</span></div>'
             '<div class="gi"><b>P01…P12</b><span>Partes de periodo de Emprendimiento.</span></div>'
             '<div class="gi"><b>2026 5 4</b><span>Código de periodo: año + nivel 5 (Centros Empresariales) + secuencia.</span></div>'
             '<div class="gi"><b>Fatal</b><span>Tipo de verificación que impide inscribir si no se cumple la regla.</span></div>'
             '<div class="gi"><b>Sobrepaso</b><span>Permiso para inscribir a pesar de un error de inscripción.</span></div>'
             '</div></div>' + glosario_html())

    # 7. Dudas
    b.append(section(7, 'Dudas para confirmar'))
    b.append(dudas)
    return '\n'.join(b)


CSS = GLOS_CSS + '''
:root { --ing: #7030A0; --inf: #0E8A5F; --infl: #E4F5EE; --sand: #FFF6E3; --sandb: #F1DDB0; --sandt: #8A5A00; }
.lead .tg { display: inline-block; border-radius: 5px; padding: 0 6px; font-weight: 700; font-size: 8.4pt; }
.tg.seuss { background: var(--sand); color: var(--sandt); border: 1px solid var(--sandb); }
.tg.ell { background: #fff; color: var(--pd); border: 1px solid var(--pb); }
.lab { display: block; font-size: 7pt; font-weight: 700; text-transform: uppercase; letter-spacing: .07em; margin-bottom: 3px; }

/* reglas comunes */
.rule { border: 1px solid var(--line); border-radius: 10px; overflow: hidden; margin: 0 0 9px; break-inside: avoid; background: #fff; }
.rh { background: var(--pl); padding: 6px 12px; font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 10pt;
      display: flex; align-items: center; gap: 8px; border-bottom: 1px solid var(--pb); }
.k { display: inline-block; width: 19px; height: 19px; border-radius: 10px; background: var(--p); color: #fff; font-size: 8pt;
     line-height: 19px; text-align: center; font-family: 'InterStatic', sans-serif; font-weight: 700; flex: none; }
.rc { display: grid; grid-template-columns: 1fr 1.45fr; }
.blk { padding: 7px 12px 8px; font-size: 8.7pt; line-height: 1.45; }
.blk ul { margin: 0; padding-left: 14px; } .blk li { margin: 0 0 3px; }
.blk.seuss { background: var(--sand); border-right: 1px solid var(--sandb); } .blk.seuss .lab { color: var(--sandt); }
.blk.ell .lab { color: var(--pd); }
.src { margin-top: 4px; font-size: 7.2pt; color: var(--mut); }

/* figura de periodos */
.figcap { font-size: 7.6pt; font-weight: 700; color: var(--mut); text-transform: uppercase; letter-spacing: .05em; margin: 2px 0 4px; }
.pfig { display: grid; grid-template-columns: 1fr 1fr 1.15fr; gap: 6px; margin: 0 0 10px; break-inside: avoid; }
.pc { border: 1px solid var(--line); border-radius: 9px; overflow: hidden; background: #fff; }
.ph { background: var(--p); color: #fff; padding: 5px 9px; display: flex; flex-wrap: wrap; align-items: baseline; gap: 2px 7px; }
.pcode { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 11pt; }
.pn { font-size: 7.6pt; opacity: .95; } .ps { font-size: 7.2pt; font-weight: 700; background: rgba(255,255,255,.2); border-radius: 4px; padding: 0 5px; }
.pr { display: grid; grid-template-columns: 58px 1fr; align-items: center; padding: 5px 8px; border-top: 1px solid var(--line); }
.ph + .pr { border-top: 0; }
.pl { font-size: 7.3pt; font-weight: 700; color: var(--mut); }
.gp { display: inline-block; border-radius: 5px; padding: 1px 5px; margin: 1px 2px 1px 0; font-weight: 700; font-size: 7.6pt; }
.gp i { font-style: normal; font-weight: 500; margin-left: 3px; opacity: .8; }
.gp.ing { background: var(--pl); color: var(--pd); } .gp.inf { background: var(--infl); color: var(--inf); }

/* intros de centro */
.intro2 { font-size: 8.8pt; line-height: 1.45; color: #2E2E36; margin: 0 0 6px; }
.chain { display: flex; gap: 0; margin: 0 0 10px; break-inside: avoid; }
.chev { flex: 1; background: var(--pl); color: var(--pd); padding: 6px 6px 6px 16px; margin-right: -6px; text-align: center;
        clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 50%, calc(100% - 10px) 100%, 0 100%, 10px 50%); }
.chev:first-child { clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 50%, calc(100% - 10px) 100%, 0 100%); padding-left: 8px; }
.chev.lvl3 { background: var(--ing); color: #fff; }
.chev b { display: block; font-size: 7.8pt; } .chev span { font-size: 7pt; }
.xg { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; margin: 0 0 10px; break-inside: avoid; }
.xc { border: 1px solid #BFE5D5; background: var(--infl); border-radius: 8px; padding: 5px 4px; text-align: center; }
.xc b { display: block; color: var(--inf); font-size: 9.5pt; font-family: 'Montserrat', sans-serif; }
.xc span { display: block; font-size: 7.2pt; font-weight: 600; } .xc i { display: block; font-style: normal; font-size: 7pt; color: var(--mut); }

/* ejemplos */
.ex { border: 1px solid var(--line); border-left: 5px solid var(--ing); border-radius: 9px; margin: 0 0 9px; background: #fff;
      break-inside: avoid; overflow: hidden; }
.ex.inf { border-left-color: var(--inf); }
.exh { display: flex; align-items: center; gap: 8px; padding: 6px 12px; border-bottom: 1px solid var(--line); font-size: 9.6pt; }
.exh b { font-family: 'Montserrat', sans-serif; flex: 1; }
.exn { font-weight: 700; font-size: 8pt; color: #fff; background: var(--ing); border-radius: 5px; padding: 1px 6px; }
.ex.inf .exn { background: var(--inf); }
.ctr { font-size: 7.4pt; font-weight: 700; border-radius: 9px; padding: 1px 8px; background: var(--pl); color: var(--pd); }
.ex.inf .ctr { background: var(--infl); color: var(--inf); }
.case { padding: 6px 12px; background: var(--pz); font-size: 8.9pt; display: grid; grid-template-columns: 88px 1fr; align-items: baseline; }
.case .lab { color: var(--mut); margin: 0; }
.r { display: grid; grid-template-columns: 88px 1fr; align-items: baseline; padding: 5px 12px; border-top: 1px solid var(--line);
     font-size: 8.8pt; line-height: 1.45; }
.r .lab { margin: 0; }
.r.seuss { background: var(--sand); } .r.seuss .lab { color: var(--sandt); }
.r.ell .lab { color: var(--pd); }
.r.res { background: var(--gl); } .r.res .lab { color: var(--gd); }
.r.ojo { background: #FFF8E8; } .r.ojo .lab { color: #8A5A00; }
.r .ap { margin-right: 6px; }
.flow { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 3px; }
.flow > span { border-radius: 6px; padding: 2px 7px; font-size: 8.3pt; }
.flow > .n { background: var(--soft); } .flow .p { background: var(--pl); color: var(--pd); } .flow .g { background: var(--gl); color: var(--gd); }
.arr { width: 12px; height: 12px; color: var(--mut); flex: none; }
.sess div { padding: 2px 0; }
.steps { margin: 0; padding-left: 18px; columns: 2; column-gap: 18px; } .steps li { margin: 0 0 2px; break-inside: avoid; }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.two > div { border: 1px solid var(--line); border-radius: 7px; padding: 5px 8px; }
.two b { display: block; font-size: 8pt; color: var(--pd); }

.paths { display: grid; grid-template-columns: repeat(3, 1fr); gap: 7px; padding: 7px 12px 9px; border-top: 1px solid var(--line); }
.path { border: 1px solid var(--line); border-radius: 8px; padding: 6px 9px 8px; display: flex; flex-direction: column; }
.path.ok { border-top: 3px solid var(--g); } .path.tbc { border-top: 3px solid #E0A100; }
.pt { font-weight: 700; font-size: 8.8pt; display: flex; align-items: center; gap: 6px; }
.pk { width: 16px; height: 16px; border-radius: 8px; background: var(--ink); color: #fff; font-size: 7.4pt; line-height: 16px; text-align: center; }
.path p { margin: 4px 0 6px; font-size: 8.2pt; line-height: 1.42; flex: 1; }
.path .ap { align-self: flex-start; }

.calc { margin: 0 12px 0 112px; border: 1px solid var(--line); border-radius: 7px; overflow: hidden; font-size: 8.4pt; }
.cr { display: grid; grid-template-columns: 1.4fr 1.3fr .8fr .7fr; padding: 3px 9px; border-top: 1px solid var(--line); }
.cr:first-child { border-top: 0; } .cr > *:not(:first-child) { text-align: center; }
.cr.ch { background: var(--soft); font-weight: 700; font-size: 7.4pt; color: var(--mut); text-transform: uppercase; letter-spacing: .04em; }
.cr.tot { background: var(--pl); font-weight: 700; } .cr.tot b { color: var(--pd); }
.cr.att { background: #FFF8E8; }
.ex .calc + .r { margin-top: 7px; }

table.fx { width: calc(100% - 124px); margin: 0 12px 0 112px; border-collapse: collapse; font-size: 8.3pt; }
table.fx th { background: var(--soft); font-size: 7.4pt; text-align: center; padding: 4px 6px; border: 1px solid var(--line); }
table.fx th i { font-style: normal; font-weight: 500; color: var(--mut); }
table.fx td { border: 1px solid var(--line); padding: 4px 8px; text-align: center; }
table.fx td:first-child { font-weight: 700; }
.fxn { margin: 4px 12px 8px 112px; font-size: 7.8pt; color: var(--mut); }

/* pruebas y dudas */
.tests { display: grid; grid-template-columns: repeat(3, 1fr); gap: 7px; break-inside: avoid; }
.tc { border: 1px solid var(--line); border-radius: 9px; padding: 7px 10px 8px; background: #fff; }
.tt { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 9pt; display: flex; gap: 7px; align-items: center; margin-bottom: 4px; }
.ti { display: grid; grid-template-columns: 15px 1fr; gap: 4px; font-size: 8.2pt; line-height: 1.4; margin: 3px 0; }
.bx { width: 10px; height: 10px; border: 1.4px solid var(--p); border-radius: 2px; margin-top: 2px; }
.keep { break-inside: avoid; }
.dudas { display: grid; grid-template-columns: 1fr 1fr; gap: 9px; break-inside: avoid; }
.dc { border: 1px solid var(--pb); border-radius: 10px; overflow: hidden; background: #fff; }
.dh { background: var(--p); color: #fff; font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 9.5pt; padding: 6px 12px; }
.dc.uss { border-color: var(--sandb); } .dc.uss .dh { background: var(--sandt); }
.dc ol { margin: 7px 12px 8px 30px; padding: 0; } .dc li { font-size: 8.6pt; line-height: 1.45; margin: 0 0 6px; }
:root { --emp: #C2501C; --empl: #FDEDE4; }
.gp.emp { background: var(--empl); color: var(--emp); }
.xg.eg6 { grid-template-columns: repeat(6, 1fr); }
.xc.emp { border-color: #F5C9B2; background: var(--empl); } .xc.emp b { color: var(--emp); }
.ex.emp { border-left-color: var(--emp); } .ex.emp .exn { background: var(--emp); } .ex.emp .ctr { background: var(--empl); color: var(--emp); }
.cr.must { background: #FFF3EC; } .cr.must span:first-child { font-weight: 700; }
.pr { grid-template-columns: 70px 1fr; }
.r.conf { background: #F4F1FA; } .r.conf .lab { color: var(--pd); }
.steps1 { margin: 4px 0 0; padding-left: 18px; } .steps1 li { margin: 0 0 3px; }
.cite { font-size: 7.3pt; color: var(--mut); white-space: nowrap; }
.subn { margin-top: 4px; font-size: 8.2pt; color: #2E2E36; }
.ti > div { min-width: 0; }
'''


if __name__ == '__main__':
    p = render('centros', build(), CSS, 'Inglés, Informática y Emprendimiento en Ellucian · Centros Empresariales', OUT,
               'Inglés, Informática y Emprendimiento en Ellucian - Centros Empresariales',
               'Hoy en SEUSS, lo que dice Ellucian y ejemplos para Inglés, Informática y Emprendimiento')
    check_pdf(p)
