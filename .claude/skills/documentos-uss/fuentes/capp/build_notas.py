# -*- coding: utf-8 -*-
"""Notas de la reunión: respuestas con evidencia de los instructivos y pendientes (Centros Empresariales)."""
import html
import os

from common import AUTHOR, HERE, chips, fmt, header, render, section, table

OUT = os.path.join(HERE, '..', 'entregables', 'NOTAS DE LA REUNIÓN - RESPUESTAS - CENTROS EMPRESARIALES.pdf')

NOTAS = [
    ('Verificar', 'Horas: de **día**, la hora académica dura 40–45 min; de **noche**, 50 min. La hora de reloj es la hora cronológica. «Rectificar en Ellucian».'),
    ('Verificar', 'Inglés: si el alumno desaprueba **BASIC I** (ciclo II) y pasa al ciclo III, ¿da **examen de suficiencia** o pasa a BASIC II '
                  'automático sin examen?'),
    ('Pregunta', 'Docentes: ¿se pueden asignar **varios docentes a un curso** y **un docente a varios cursos**?'),
    ('Pregunta', 'Notas: ¿cómo es la **validación de notas** y la **vinculación con el aula virtual**? Debe permitir pasar las notas y sacar '
                 'su data y su programación de notas.'),
    ('Dato', 'Flujo: (1) Periodos › (2) Planes curriculares › (3) Carga lectiva y Registros Académicos (secciones = NRC, horarios) › '
             '(4) Matrícula › (5) Enseñanza-aprendizaje (notas, asistencia).'),
    ('Dato', 'Periodos de SEUSS en Ellucian: 2026-0 Verano = 202651 · 2026-I = 202654 · 2026-II = 202656 · el verano 2027 será 202751.'),
    ('Dato', 'Pruebas: periodos, generación de mallas y programas, creación de NRC, matrículas por backoffice y por autoservicio.'),
]

RESPUESTAS = [
    {
        't': 'Horas académicas y cronológicas',
        'ev': [('5.2 Carga de trabajo docente', 'En SIATERM, el **factor de duración** es la equivalencia en minutos de la hora académica '
                                                '(ejemplo del instructivo: 50 minutos). Se define **por periodo**.'),
               ('5.3 Oferta horaria', 'SSASECT calcula las horas por semana de cada sesión a partir del horario, «basado en una hora '
                                      'académica definida en SIATERM».'),
               ('Horario del NRC', 'La **hora cronológica** es la que se registra en el horario: hora de inicio y fin (24 h) en SSASECT.')],
        'con': 'Hay **un solo factor por periodo**. Si el día usa 40–45 minutos y la noche 50, un único factor no refleja los dos turnos.',
        'q': '¿Cómo se configuran dos duraciones de hora académica (día y noche) en el mismo periodo? ¿Se ajustan las horas del NRC a mano '
             'en SSASECT o hay otra regla?',
    },
    {
        't': 'Inglés: BASIC I desaprobado',
        'ev': [('1.1.5 Prerrequisitos', 'El «examen de curso» es un prerrequisito que no es curso; el ejemplo del instructivo es la '
                                        '**suficiencia en idioma**. En SCAPREQ (catálogo) y SSAPREQ (NRC) se combinan examen con puntaje mínimo '
                                        'y curso aprobado usando **Y / O**.'),
               ('Exámenes', 'El puntaje del examen se registra en SOATEST; el código del examen se crea en STVTESC.'),
               ('CAPP', 'Si BASIC I no está aprobado, CAPP lo marca pendiente y la proyección vuelve a ofrecer BASIC I.')],
        'con': '**Con examen:** BASIC II exige «BASIC I aprobado **o** examen de suficiencia con puntaje mínimo»; Banner lo soporta tal cual. '
               '**Automático sin examen:** los instructivos no traen una regla así; habría que quitar el prerrequisito o dar un sobrepaso '
               '(SFAROVR) caso por caso.',
        'q': '¿Cuál es la regla de la USS? Si el avance es automático, ¿cómo debe quedar en la historia académica y en CAPP?',
    },
    {
        't': 'Varios docentes por curso y un docente en varios cursos',
        'ev': [('6.2.1 Asignar docentes', '«En cada sesión se puede asociar uno o varios docentes», «pudiendo haber simultáneamente dos o tres '
                                          'docentes, pero siempre definiendo uno de ellos como el docente **principal**». Cada uno con % de '
                                          'responsabilidad y % de sesión.'),
               ('5.3 Oferta horaria', 'Si el NRC tiene más de un docente, cada uno va en una sesión con indicador distinto (01, 02, 03).'),
               ('Tema 3', 'Un docente puede estar en varios NRC: SIAASGN muestra todos sus NRC y su carga. Si hay cruce de horario, se usa el '
                          'indicador de sobrepaso en SSASECT.')],
        'con': '**Sí en los dos casos.** Un NRC admite 2 o 3 docentes (uno principal) y un docente puede dictar varios NRC; su carga se '
               'controla en SIAASGN.',
        'q': None,
    },
    {
        't': 'Validación de notas y aula virtual',
        'ev': [('6.2.4 Recursos virtuales', 'El NRC se vincula al aula virtual (LMS) con el campo **Socio de integración** en SSASECT '
                                            '(códigos en GTVINTP y reglas en GORINTG): la información del NRC se transfiere al LMS.'),
               ('Lo que no dicen', 'Los instructivos no describen que el aula virtual **devuelva las notas** a Banner ni cómo sale la '
                                   '«programación de notas».')],
        'con': 'El flujo de notas en Banner está documentado paso a paso (tabla siguiente). La salida de datos hacia el aula virtual está '
               'prevista; el regreso de notas desde el aula virtual **no está documentado**.',
        'q': '¿La integración con el aula virtual devuelve las notas al libro de calificaciones de Banner? ¿Qué datos salen: NRC, docentes, '
             'estudiantes y plan de evaluación?',
    },
]

FLUJO_NOTAS = [
    ('Escala de calificación', 'SHAGRDE, SHAGSCH', 'Códigos de nota y escala con el porcentaje mínimo de aprobación.', '7.1.3'),
    ('Plan de evaluación del NRC', 'SHAGCOM', 'Registros Académicos carga componentes y subcomponentes de cada NRC.', '7.1.4'),
    ('Fechas de carga', 'SOATERM', 'Fechas en las que el docente puede registrar notas, por periodo y parte de periodo.', '7.1.4'),
    ('El docente registra', 'Autoservicio', 'Libro de calificaciones: notas parciales y finales de sus NRC.', '7.1.4'),
    ('El estudiante consulta', 'SOATERM, SSAWSEC', 'Se habilita por periodo; se puede restringir para un NRC.', '7.1.5'),
    ('Correcciones', 'SFASLST, SHATCKN', 'Registros Académicos corrige por backoffice; si ya pasó a historia, en SHATCKN.', '7.1.6'),
    ('Incompletas', 'SHAGRDE, SHRCINC', 'Nota incompleta con fecha límite; luego se reemplaza por la definida.', '7.1.7'),
    ('Cierre', 'SHRROLL, SMRBCMP', 'Pasar las notas a la historia académica y ejecutar el CAPP masivo.', '7.1.9'),
    ('Después del cierre', 'SHAEGBC', 'El docente solo corrige si se le habilitan fechas de reestimación.', '7.1.8'),
]

PERIODOS = [
    ('2026-0', 'Verano', '202651', '2026 + nivel **5** (Centros Empresariales) + secuencia **1** (verano)'),
    ('2026-I', 'Primer periodo', '202654', '2026 + nivel **5** + secuencia **4** (semestre I)'),
    ('2026-II', 'Segundo periodo', '202656', '2026 + nivel **5** + secuencia **6** (semestre II)'),
    ('2027-0', 'Verano 2027', '202751', 'Mismo patrón: año 2027 + 5 + 1'),
]

FLUJO = [
    ('1', 'Periodos', 'STVTERM, SOATERM', 'Tema 1', 'ok'),
    ('2', 'Planes curriculares (mallas y programas)', 'SCACRSE, SMAPROG, SMAAREA', 'CAPP explicado (parcial)', 'part'),
    ('3', 'Carga lectiva y Registros Académicos: secciones (NRC) y horarios', 'SSASECT, SIAINST, SIAASGN', 'Temas 2, 2.1 y 3', 'ok'),
    ('4', 'Matrícula (backoffice y autoservicio)', 'SFAREGS, SFAPROJ', 'Tema 5 (siguiente)', 'pend'),
    ('5', 'Enseñanza-aprendizaje: notas y asistencia', 'SHAGCOM, SHRROLL', 'Pendiente (capacidad 7)', 'pend'),
]

PRUEBAS = [
    ('grp', 'Periodos'),
    ('Existen los periodos 202651, 202654 y 202656 con sus fechas.', 'Los tres periodos visibles y vigentes.', 'STVTERM'),
    ('Partes de periodo del centro (I01…, X01…, P01…).', 'Cada parte con fechas, semanas y censo.', 'SOATERM'),
    ('Fechas de inscripción web y de acceso docente.', 'Un rango que cubre todas las partes del periodo.', 'SOATERM'),
    ('grp', 'Mallas y programas'),
    ('El programa de Idiomas está activo con sus áreas y reglas.', 'Programa activo; áreas con prioridad.', 'SMAPROG, SMAAREA'),
    ('CAPP de un participante con BASIC I aprobado.', 'BASIC I cumple; BASIC II pendiente.', 'SMARQCM, SMICRLT'),
    ('grp', 'Creación de NRC'),
    ('Crear un NRC de BASIC II en la parte del mes, con cupo y horario.', 'Se genera el NRC con la secuencia del periodo.', 'SSASECT'),
    ('Prerrequisito: BASIC I o examen de suficiencia.', 'El NRC hereda la regla del catálogo.', 'SSAPREQ, SCAPREQ'),
    ('Asignar dos docentes (sesiones 01 y 02, uno principal).', 'Ambos asignados; carga visible en SIAASGN.', 'SSASECT, SIAASGN'),
    ('Horas por semana de un NRC de día y otro de noche.', 'Coinciden con la hora académica acordada.', 'SSASECT, SIATERM'),
    ('grp', 'Matrícula por backoffice'),
    ('Inscribir en BASIC II a un participante con BASIC I aprobado.', 'Inscripción sin errores.', 'SFAREGS'),
    ('Inscribir en BASIC II a un participante sin BASIC I.', 'Error de prerrequisito; solo pasa con sobrepaso aprobado.', 'SFAREGS, SFAROVR'),
    ('grp', 'Matrícula por autoservicio'),
    ('El participante entra en las fechas web y ve sus cursos proyectados.', 'Solo puede inscribir lo proyectado.', 'SFAPROJ'),
    ('La inscripción genera el cobro.', 'Cargo en la cuenta corriente del participante.', 'TSAAREV'),
]


def build():
    b = [header('Universidad Señor de Sipán · Centros Empresariales', 'Notas de la reunión: respuestas',
                'Lo que anotaste, qué dicen los instructivos de Ellucian y qué falta confirmar',
                [('Elaborado por', AUTHOR), ('Fecha', '26 de septiembre de 2026'),
                 ('Fuentes', 'Tus notas · Instructivos de las capacidades 1, 3, 5, 6 y 7'), ('Estado', 'Para validar con Ellucian')])]

    b.append(section(1, 'Lo que anotaste'))
    tipo = {'Verificar': 'tbc', 'Pregunta': 'soon', 'Dato': 'ok'}
    rows = [[f'<span class="n">{i}</span>', f'<span class="ap {tipo[t]}">{t}</span>', fmt(x)] for i, (t, x) in enumerate(NOTAS, 1)]
    b.append(table([('N°', 5), ('Tipo', 12), ('Nota', 83)], rows, 'notas'))

    b.append(section(2, 'Respuestas con lo que dicen los instructivos'))
    for i, r in enumerate(RESPUESTAS, 1):
        ev = ''.join(f'<tr><td class="src">{html.escape(s)}</td><td>{fmt(t)}</td></tr>' for s, t in r['ev'])
        q = (f'<div class="q"><span class="lab">Pregunta para Ellucian</span>{fmt(r["q"])}</div>' if r['q'] else
             '<div class="q ok"><span class="lab">Estado</span>Resuelto con los instructivos.</div>')
        b.append(f'<div class="ans"><div class="ah"><span class="k">{i}</span>{html.escape(r["t"])}</div>'
                 f'<table class="ev"><tbody>{ev}</tbody></table>'
                 f'<div class="con"><span class="lab">Conclusión</span>{fmt(r["con"])}</div>{q}</div>')
        if i == 4:
            rows = [[f'<span class="n">{j}</span>', f'<b>{html.escape(p)}</b>', chips(g), fmt(d), f'<span class="tag">{s}</span>']
                    for j, (p, g, d, s) in enumerate(FLUJO_NOTAS, 1)]
            b.append('<h3 class="h3gap">Flujo de notas en Banner <span class="eg">según los instructivos de la capacidad 7</span></h3>')
            b.append(table([('N°', 5), ('Paso', 20), ('Páginas', 19), ('Qué se hace', 46), ('Instructivo', 10)], rows, 'fn'))

    b.append(section(3, 'Periodos: SEUSS y Ellucian', 'Equivalencia anotada en la reunión, con la estructura del código del tema 1.'))
    rows = [[f'<b>{s}</b>', n, f'<span class="pg">{e}</span>', fmt(q)] for s, n, e, q in PERIODOS]
    b.append(table([('SEUSS', 14), ('Nombre', 20), ('Ellucian', 14), ('Cómo se lee el código', 52)], rows, 'per'))
    b.append('<div class="note warn"><b>Corrige un supuesto:</b> en el PDF «Periodo académico: antes y después» la columna «Antes» mostraba, '
             'de forma ilustrativa, cuatro periodos de 3 meses. Según esta equivalencia, en SEUSS también había <b>tres periodos al año</b>; '
             'lo que cambia en Banner es el código y que cada grupo mensual se maneja como una parte de periodo. Falta aclarar a qué se refería «un periodo de 3 meses» '
             '(¿el verano, o la duración del ciclo de clases?).</div>')

    b.append(section(4, 'Tu flujo y dónde está documentado'))
    est = {'ok': '<span class="ap ok">Documentado</span>', 'part': '<span class="ap tbc">Parcial</span>',
           'pend': '<span class="ap soon">Pendiente</span>'}
    rows = [[f'<span class="n">{n}</span>', f'<b>{html.escape(e)}</b>', chips(g), html.escape(d), est[s]] for n, e, g, d, s in FLUJO]
    b.append(table([('N°', 5), ('Etapa (tu hoja)', 35), ('Páginas', 24), ('Documento', 22), ('Estado', 14)], rows, 'flujo'))

    b.append(section(5, 'Casos de prueba para los centros', 'Según tu lista de pruebas: qué probar, qué debe pasar y dónde.'))
    rows = []
    n = 0
    for r in PRUEBAS:
        if r[0] == 'grp':
            rows.append(r)
            continue
        n += 1
        rows.append([f'<span class="n">{n}</span>', fmt(r[0]), fmt(r[1]), chips(r[2]), ''])
    b.append(table([('N°', 5), ('Caso', 36), ('Resultado esperado', 30), ('Páginas', 17), ('OK', 12)], rows, 'prue'))

    b.append(section(6, 'Para llevar a Ellucian'))
    qs = ['Hora académica de **día (40–45 min)** y de **noche (50 min)** en el mismo periodo, si SIATERM tiene un solo factor.',
          'Regla de inglés cuando se desaprueba BASIC I: **examen de suficiencia** (soportado) o **avance automático** (sin regla estándar).',
          'Integración con el aula virtual: si **devuelve las notas** a Banner y qué datos salen hacia el aula virtual.',
          'Dónde se configuran los **planes curriculares** de los centros en CAPP (SMAPROG, SMAAREA) y quién los carga.']
    b.append('<ol class="qs">' + ''.join(f'<li>{fmt(q)}</li>' for q in qs) + '</ol>')
    b.append('<p class="foot">Interno: aclarar qué significaba «un periodo de 3 meses» en SEUSS para corregir el PDF de antes y después.</p>')
    return '\n'.join(b)


CSS = '''
table.notas td:nth-child(3), table.notas th:nth-child(3) { text-align: left; }
table.notas td:nth-child(2) { text-align: center; }
.ans { border: 1px solid var(--line); border-radius: 10px; margin: 0 0 10px; overflow: hidden; break-inside: avoid; background: #fff; }
.ah { background: var(--pl); padding: 7px 12px; font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 10pt; color: var(--ink);
      display: flex; align-items: center; gap: 8px; border-bottom: 1px solid var(--pb); }
.ah .k { width: 20px; height: 20px; border-radius: 10px; background: var(--p); color: #fff; font-size: 8.5pt; line-height: 20px; text-align: center; }
table.ev { width: 100%; border-collapse: collapse; }
table.ev td { padding: 5px 12px; border-bottom: 1px solid var(--line); vertical-align: top; font-size: 8.6pt; }
table.ev td.src { width: 24%; font-weight: 700; color: var(--pd); font-size: 8.2pt; }
.con, .q { padding: 6px 12px; font-size: 8.8pt; line-height: 1.45; }
.con { background: var(--gl); }
.q { background: #FFF8E8; border-top: 1px solid #F2DDA4; }
.q.ok { background: #F4FAF0; border-top-color: #D3EAC7; }
.lab { display: inline-block; font-size: 7.2pt; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; margin-right: 8px;
       color: var(--mut); }
.con .lab { color: var(--gd); } .q .lab { color: #8A5A00; } .q.ok .lab { color: var(--gd); }
table.fn td:nth-child(2), table.fn th:nth-child(2), table.fn td:nth-child(4), table.fn th:nth-child(4),
table.per td:nth-child(2), table.per th:nth-child(2), table.per td:nth-child(4), table.per th:nth-child(4),
table.flujo td:nth-child(2), table.flujo th:nth-child(2), table.flujo td:nth-child(4), table.flujo th:nth-child(4),
table.prue td:nth-child(2), table.prue th:nth-child(2), table.prue td:nth-child(3), table.prue th:nth-child(3) { text-align: left; }
table.per td:first-child { text-align: left; } table.per td:nth-child(3) { text-align: center; }
table.fn td:last-child, table.flujo td:last-child { text-align: center; }
table.prue td:last-child { background: #fff; border-left: 1px solid var(--line); }
.tag { display: inline-block; background: var(--soft); border-radius: 9px; padding: 0 7px; font-weight: 600; font-size: 7.6pt; }
ol.qs { margin: 2px 0 4px; padding-left: 20px; }
ol.qs li { margin: 0 0 6px; padding: 6px 10px; background: var(--pz); border: 1px solid var(--line); border-radius: 7px; font-size: 9pt; }
'''


if __name__ == '__main__':
    p = render('notas', build(), CSS, 'Notas de la reunión: respuestas · Centros Empresariales', OUT,
               'Notas de la reunión: respuestas - Centros Empresariales', 'Respuestas a las notas de la reunión con evidencia de los instructivos')
    print('OK', p)
