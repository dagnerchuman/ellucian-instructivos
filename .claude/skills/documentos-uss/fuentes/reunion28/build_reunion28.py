# -*- coding: utf-8 -*-
"""Resumen de la reunión del 28/09/2026: reemplazo de docente, planes curriculares incompletos, tutores,
validación contra legado y escenarios para las pruebas integrales."""
import html
import os
import sys

SKILL = '/home/user/ellucian-instructivos/.claude/skills/documentos-uss/scripts/pdf'
sys.path.insert(0, SKILL)
from common import AUTHOR, GLOS_CSS, check_pdf, explicar, fmt, glosario_html, header, render, section  # noqa: E402
import ejemplo_centros as E  # noqa: E402  (reutiliza estilos y piezas del ejemplo de referencia)

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(__file__), '..', 'entregables', 'RESUMEN DE LA REUNIÓN 28-09 - PRUEBAS INTEGRALES Y PLANES CURRICULARES.pdf')

NOTAS = [
    ('Caso', 'En un grupo de la **maestría en Educación** falleció el docente a mitad del curso. ¿Qué se hace? Se reemplaza. '
             'Hay que tenerlo en las **pruebas integrales**.'),
    ('Riesgo', 'Capacidad 1: hay **programas en rediseño** sin tablas de equivalencia, sin cursos y sin la nueva versión del plan.'),
    ('Riesgo', '**Posgrado** envió su plan curricular, pero los cursos no están en los módulos de Registros Académicos. '
               '¿Cómo va a funcionar **20271** si no terminan sus planes curriculares?'),
    ('Riesgo', 'Se ofrece algo que no tiene información: impacta desde la **capacidad 3** (admisión) y todo termina en Registros Académicos.'),
    ('Pregunta', '¿Cómo van a trabajar los **tutores**?'),
    ('Pedido', 'Un **monto total** de la validación contra legado.'),
]


def card(code, title, tag, rows, extra=''):
    """Tarjeta como las del ejemplo de referencia; tag = (texto, clase de color)."""
    return explicar(f'<div class="ex {tag[1]}"><div class="exh"><span class="exn">{code}</span><b>{html.escape(title)}</b>'
                    f'<span class="ctr">{tag[0]}</span></div>'
                    + ''.join(E.row(k, fmt(t) if not t.startswith('<') else t) for k, t in rows) + extra + '</div>')


def pasos(items):
    return ('<ol class="steps1">' + ''.join(f'<li>{fmt(t)} <span class="cite">Instructivo {c}</span></li>' for t, c in items)
            + '</ol>')


CADENA = [('1', 'Cursos en el catálogo', 'SCACRSE', '1.1.4'), ('2', 'Malla y su versión', 'SMAPROG, SMAAREA', '1.2.1, 1.3.1'),
          ('3', 'Equivalencias', 'SCADETL o SMAAREA', '1.2.3'), ('4', 'Regla curricular activa', 'SOACURR', '1.1.3'),
          ('5', 'Admisión', 'SAAADMS, SAAQUIK', '3.2.1'), ('6', 'NRC e inscripción', 'SSASECT, SFAREGS', '5.3, 5.4'),
          ('7', 'Tutor y CAPP', 'SGAADVR, SMARQCM', '9.1.1, 7.2.4')]

LEGADO = [('Personas: participantes y docentes', 'SPAIDEN'), ('Estudiantes por programa y estado', 'SGASTDN'),
          ('Historia académica: cursos por periodo', 'SHACRSE'), ('Docentes', 'SIAINST'),
          ('Saldos: participantes con deuda', 'TSAAREV'), ('Saldos: monto total pendiente (S/)', 'TSAAREV'),
          ('Egresados o certificados (por confirmar)', 'SHADEGR')]

PRUEBAS = [
    ('Reemplazo de docente', ['Un docente con notas parciales registradas deja el NRC a mitad del curso.',
                              'Se asigna al reemplazo como principal y este registra las notas que faltan.',
                              'Se cierra el periodo y la nota final pasa a la historia académica.',
                              'También en los centros: docente de un grupo de Inglés (por ejemplo, I06).']),
    ('Plan en rediseño', ['Crear un NRC de un curso que no está en el catálogo: no debe dejar.',
                          'Cargar el curso y la nueva versión de la malla; volver a crear el NRC.',
                          'Estudiante con plan anterior: el CAPP reconoce las equivalencias.']),
    ('Admisión', ['Admitir a un programa con su regla curricular nueva: la solicitud trae el programa correcto.',
                  'Intentar admitir a un programa sin regla curricular activa: no debe aparecer.']),
    ('Tutores', ['Asignación masiva de tutores por programa.', 'El tutor ve el perfil y el avance de sus estudiantes por autoservicio.']),
    ('Contra legado', ['Antes de cada revisión, cuadrar los totales de SEUSS y Banner por centro o programa.']),
]

DUDAS_E = [
    'Reemplazo de docente: ¿el docente anterior se queda en el NRC con su porcentaje (para el historial y el pago) o se elimina? '
    '¿Qué pasa con las notas que ya registró y con la encuesta de evaluación docente del NRC?',
    '¿Qué se hace si un programa no tiene su plan completo (cursos, versión, equivalencias) cuando se abre 20271?',
    'Tutores: ¿qué ve el tutor en el autoservicio si el programa del estudiante no tiene su malla cargada?',
    '¿Insight puede dar los totales de la validación contra legado separados por centro y por programa? (E12)',
]
DUDAS_U = [
    '¿Quién termina los planes en rediseño y el de posgrado (cursos, nueva versión, equivalencias) y con qué fecha límite antes de 20271?',
    '«20271»: ¿es el primer periodo de 2027 de posgrado? ¿Cuál es su código de 6 dígitos en Banner?',
    '¿Quién saca los totales de SEUSS y con qué fecha de corte? (U11)',
    '¿La tutoría aplica también a Centros Empresariales? (U07)',
]


def build():
    b = [header('Universidad Señor de Sipán · Migración a Ellucian Banner', 'Resumen de la reunión del 28/09',
                'Reemplazo de docentes, planes curriculares incompletos, tutores, validación contra legado y pruebas integrales',
                [('Elaborado por', AUTHOR), ('Fecha', '28 de septiembre de 2026'),
                 ('Fuentes', 'Lo que contaste de la reunión · Instructivos de Ellucian'), ('Estado', 'Para confirmar')])]

    b.append(section(1, 'Lo que se contó'))
    tipo = {'Caso': 'now', 'Riesgo': 'bad', 'Pregunta': 'soon', 'Pedido': 'ok'}
    b.append(explicar('<div class="notes">' + ''.join(
        f'<div class="nt"><span class="ap {tipo[t]}">{t}</span><div>{fmt(x)}</div></div>' for t, x in NOTAS) + '</div>'))

    # 2. Docente
    b.append(section(2, 'Reemplazar a un docente a mitad del curso'))
    b.append(card('A', 'El docente de un NRC falleció', ('Maestría y centros', 'gen'), [
        ('conf', 'Qué hacer en Banner para que el grupo siga: nuevo docente, notas y carga.'),
        ('ell', pasos([
            ('En SPAIDEN, pestaña Biográfica: fecha de fallecimiento y casilla «Fallecido».', '5.1.1, diap. 40'),
            ('En SIAINST: cambiar el **estatus del docente** (códigos en STVFCST) para que no se le asigne más.',
             '5.2 Información de docentes, diap. 10 y 18'),
            ('En SSASECT: asignar al **nuevo docente** en la sesión del NRC y marcarlo como **principal**; ajustar el % de '
             'responsabilidad y de sesión. Un NRC admite 2 o 3 docentes, con un solo principal.', '6.2.1, diap. 19 y 21'),
            ('Notas y asistencia: el nuevo docente debe estar asignado al NRC para verlo en el autoservicio. Si la regla PRIMINSTR '
             'está en «Y», **solo el principal** registra notas.', '7.1.4, diap. 21 y 24'),
            ('Carga: el NRC aparece en SIAASGN del nuevo docente (horas semanales × semanas del NRC).', '5.2 Carga, diap. 18'),
        ])),
        ('ojo', 'Los instructivos **no dicen** si el docente anterior se deja en el NRC o se elimina, ni qué pasa con las notas que ya '
                'registró y con la encuesta de evaluación docente. Va a las dudas.'),
        ('res', 'Se puede reemplazar sin cerrar el NRC: el grupo sigue con sus participantes y sus notas. Es un escenario para las '
                'pruebas integrales (sección 6).'),
    ]))

    # 3. Planes curriculares
    b.append(section(3, 'Planes curriculares incompletos: por qué afecta a todo'))
    b.append('<div class="intro2">Cada paso necesita el anterior. Si falta el primero (cursos o plan), no se puede admitir, '
             'programar NRC ni asignar tutores para ese programa.</div>')
    b.append(explicar('<div class="chainv">' + ''.join(
        f'<div class="cv"><span class="k">{n}</span><b>{t}</b><span class="pgs">{fmt(p)}</span><i>{c}</i></div>'
        for n, t, p, c in CADENA) + '</div>'))
    b.append(card('B', 'Programas en rediseño y plan de posgrado', ('Capacidades 1, 3 y 5', 'gen'), [
        ('ell', pasos([
            ('Sin cursos en el catálogo no hay NRC: «Banner permite la programación académica (SSASECT) de las asignaturas que hayan '
             'sido definidas en el catálogo de curso (SCACRSE)».', '5.3, diap. 53'),
            ('Nueva versión del plan: rige desde un periodo. «Si la actualización implica nuevos cursos, éstos se deben crear antes de '
             'modificar los requerimientos de áreas»; una nueva área, antes de modificar el programa.', '1.3.1, diap. 5'),
            ('Equivalencias: «los cursos para agregar como equivalentes deben haberse creado previamente». Se cargan en SCADETL o en la '
             'malla (SMAAREA); Ellucian recomienda hacerlo por malla.', '1.2.3, diap. 6 y 15'),
            ('Admisión (capacidad 3): la solicitud trae la **regla de currículo** del programa. La regla define el periodo de inicio y '
             'debe estar activa para admisiones, gestión del alumno, historia académica y evaluación de grado.',
             '1.1.3, diap. 34; 3.2.1, diap. 15 y 25'),
        ])),
        ('res', 'Para 20271, el orden es: **cursos › malla y versión › equivalencias › regla curricular**, y recién después admisión, '
                'NRC y tutores. Si posgrado no termina su plan, ese programa se queda sin poder admitir ni programar.'),
        ('ojo', 'En Centros Empresariales pasa lo mismo cada mes: los cursos del grupo deben estar en SCACRSE antes de crear sus NRC.'),
    ]))

    # 4. Tutores
    b.append(section(4, 'Cómo trabajarán los tutores'))
    b.append(card('C', 'Tutores en Banner', ('Capacidad 9', 'gen'), [
        ('ell', pasos([
            ('El docente se habilita como **asesor** en SIAINST, vigente desde un periodo. Los tipos de asesor van en STVADVR.',
             '9.1.1, diap. 20 y 24'),
            ('Asignación: uno por uno en SGAADVR, o masiva con reglas en SGAAVRL y el proceso SGPADVA (por programa, cohorte o atributo).',
             '9.1.1, diap. 27 y 30 a 35'),
            ('Qué ve el tutor en el autoservicio (perfil del estudiante, notas, avance) lo definen las reglas de SOAFACS.',
             '9.1.1, diap. 9, 10 y 36'),
        ])),
        ('ojo', 'El tutor trabaja sobre el programa y el avance del estudiante. Si el plan del programa no está cargado, no tendrá '
                'avance que revisar. Va a las dudas.'),
    ]))

    # 5. Legado
    b.append(explicar(section(5, 'Validación contra legado: el total',
                     'No tengo los números: salen de SEUSS y de Banner (reportes de Insight). Este es el cuadro para llenarlos, uno '
                     'por centro o programa.')))
    rows = ''.join(f'<tr><td>{explicar(fmt(q))}</td><td>{fmt(p)}</td><td></td><td></td><td></td><td></td><td></td></tr>'
                   for q, p in LEGADO)
    b.append('<table class="leg"><thead><tr><th>Qué se cuenta</th><th>Página</th><th>SEUSS</th><th>Esperado</th><th>Banner</th>'
             '<th>Diferencia</th><th>¿Explicada?</th></tr></thead><tbody>' + rows + '</tbody></table>')
    b.append(explicar('<div class="note">Diferencia = Esperado − Banner. Si no es cero, se listan los ID que faltan o sobran y su '
                      'motivo; lo no explicado va al Issue log. En «Saldos» se compara también el <b>monto total en soles</b>, no solo '
                      'la cantidad de participantes.</div>'))

    # 6. Pruebas integrales
    b.append(section(6, 'Para las pruebas integrales (16/11 al 26/12)'))
    b.append('<div class="tests">' + ''.join(explicar(
        f'<div class="tc"><div class="tt"><span class="k">{i}</span>{t}</div>'
        + ''.join(f'<div class="ti"><span class="bx"></span><div>{fmt(x)}</div></div>' for x in items) + '</div>')
        for i, (t, items) in enumerate(PRUEBAS, 1)) + '</div>')

    dudas = ('<div class="dudas"><div class="dc">' + explicar('<div class="dh">Para Ellucian</div><ol>'
             + ''.join(f'<li>{fmt(q)}</li>' for q in DUDAS_E) + '</ol>') + '</div><div class="dc uss">'
             + explicar(f'<div class="dh">Para la USS</div><ol start="{len(DUDAS_E) + 1}">'
                        + ''.join(f'<li>{fmt(q)}</li>' for q in DUDAS_U) + '</ol>') + '</div></div>')
    b.append(section(7, 'Glosario'))
    b.append(glosario_html(extra=[p for _, p in LEGADO] + ['SCACRSE', 'SMAPROG', 'SMAAREA', 'SCADETL', 'SOACURR', 'SAAADMS',
                                                                  'SAAQUIK', 'SSASECT', 'SFAREGS', 'SGAADVR', 'SMARQCM']))
    b.append(section(8, 'Dudas para confirmar'))
    b.append(dudas)
    return '\n'.join(b)


CSS = E.CSS + '''
.ex.gen { border-left-color: var(--pd); } .ex.gen .exn { background: var(--pd); }
.notes { border: 1px solid var(--line); border-radius: 10px; overflow: hidden; background: #fff; }
.nt { display: grid; grid-template-columns: 70px 1fr; gap: 8px; align-items: baseline; padding: 6px 12px; border-top: 1px solid var(--line);
      font-size: 9pt; line-height: 1.45; }
.nt:first-child { border-top: 0; } .nt .ap { justify-self: start; }
.chainv { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; margin: 0 0 10px; break-inside: avoid; }
.cv { border: 1px solid var(--pb); background: var(--pz); border-radius: 8px; padding: 6px 6px 7px; text-align: center; position: relative; }
.cv .k { display: block; margin: 0 auto 3px; }
.cv b { display: block; font-size: 8pt; line-height: 1.25; } .cv .pgs { display: block; font-size: 7pt; margin-top: 2px; }
.cv i { display: block; font-style: normal; font-size: 6.8pt; color: var(--mut); margin-top: 2px; }
.cv .gls { display: none; }
table.leg { width: 100%; border-collapse: collapse; font-size: 8.4pt; margin: 2px 0 6px; break-inside: avoid; }
table.leg th { background: var(--p); color: #fff; font-size: 7.6pt; padding: 5px 6px; text-align: center; }
table.leg th:first-child { text-align: left; }
table.leg td { border: 1px solid var(--line); padding: 7px 6px; height: 26px; }
table.leg td:nth-child(n+3) { width: 11%; }
table.leg td:nth-child(2) { width: 12%; }
.tests { grid-template-columns: repeat(3, 1fr); }
'''


if __name__ == '__main__':
    p = render('reunion28', build(), CSS, 'Resumen de la reunión del 28/09 · Migración a Ellucian Banner', OUT,
               'Resumen de la reunión del 28-09 - Pruebas integrales y planes curriculares',
               'Reemplazo de docente, planes curriculares, tutores, validación contra legado y pruebas integrales')
    check_pdf(p, png_dir=os.path.join(os.path.dirname(__file__), 'png'))
