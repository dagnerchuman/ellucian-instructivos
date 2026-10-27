# -*- coding: utf-8 -*-
"""PPTX (plantilla USS): repaso para la reunión con el jefe del Centro de Informática (27/10/2026).

Inscribir a un alumno en su ruta de aprendizaje, crear el NRC (viendo antes a qué malla va el alumno) y asignar los
programas al NRC, con el BPM «ve a tal página», los enlaces del sitio y prompts para el asistente IA. Correcciones del
jefe (C127): «crear NRC» en vez de «curso nuevo», «asignar programas» en vez de «asignar escuelas»; las escuelas a las
rutas las asigna Pregrado.
La plantilla es «docs/presentaciones/2. PROGRAMACIÓN DE ASIGNATURAS.pptx» (la de ussdeck).

    python3 build_ruta.py ["<salida>.pptx"]
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
USS = os.path.dirname(os.path.dirname(HERE))   # raíz de la skill documentos-uss
RAIZ = os.path.abspath(os.path.join(USS, '..', '..', '..'))
os.environ.setdefault('USS_PPT_TEMPLATE', os.path.join(RAIZ, 'docs', 'presentaciones', '2. PROGRAMACIÓN DE ASIGNATURAS.pptx'))
sys.path.insert(0, os.path.join(USS, 'scripts', 'pptx'))
sys.path.insert(0, os.path.join(USS, 'scripts', 'pdf'))
import common as GL  # noqa: E402  (glosario: PAGINAS, SIGLAS, _TERM_RE)
from pptlib import *  # noqa: E402,F401,F403
from ussdeck import build_cover, build_div, build_structure, finalize  # noqa: E402

OUT = os.path.join(RAIZ, 'docs', 'presentaciones',
                   'RUTA DE APRENDIZAJE - INSCRIPCIÓN, NRC Y PROGRAMAS - CENTRO DE INFORMÁTICA.pptx')
SITIO = 'centros-empresariales-ellucian.vercel.app'


def ex(text, seen):
    """Agrega «(significado)» a la primera aparición de cada página o sigla en la diapositiva."""
    out, last = [], 0
    for m in GL._TERM_RE.finditer(text):
        term = m.group(0)
        if m.group(2) is None and not term.isupper():
            continue
        key, mean = GL._meaning(term)
        if key in seen or key in ('SEUSS', 'NRC', 'ID', 'CAPP', 'TEST'):
            continue
        seen.add(key)
        pre = text[:m.start()]
        d = pre.count('(') - pre.count(')')
        out.append(text[last:m.end()] + (f': {mean}' if d > 0 else f' ({mean})'))
        last = m.end()
    out.append(text[last:])
    return ''.join(out)


def para(runs, spc_after=0, algn='l'):
    body = ''
    for t, sz, b, c in runs:
        for tt, bb, cc in rich(t, c, b):
            body += r_xml(tt, sz, bb, cc)
    spc = f'<a:spcAft><a:spcPts val="{spc_after}"/></a:spcAft>' if spc_after else ''
    return f'<a:p><a:pPr algn="{algn}">{spc}<a:buNone/></a:pPr>{body}<a:endParaRPr lang="es-PE" dirty="0"/></a:p>'


def box(S, x, y, w, h, paras, fill='FFFFFF', line=LINE, anchor='t', ins=(150000, 110000, 150000, 90000), name='Bloque'):
    S.add(shape_xml(S.nid(), x, y, w, h, geom='roundRect', adj=6000, fill=fill, line=line, paras=paras, anchor=anchor, ins=ins,
                    name=name))


def columnas(S, bloques, y=None, gap=180000, sz=1250, titulo_sz=1400):
    """bloques: [(título, [líneas], relleno, color del título)] en columnas iguales hasta el pie."""
    y = S.y if y is None else y
    n = len(bloques)
    cw = (XW - (n - 1) * gap) / n
    for i, (tit, lineas, fill, col) in enumerate(bloques):
        ps = para([(tit, titulo_sz, True, col)], spc_after=500)
        ps += ''.join(para([(t, sz, False, INK)], spc_after=350) for t in lineas)
        box(S, X0 + i * (cw + gap), y, cw, YB - y, ps, fill=fill, line=fill)


# ------------------------------------------------------------------ contenido
RUTAS = [
    ('1 · XP 01 (CMEMC38)', 'Salud: Enfermería, Estomatología, Medicina Humana, Tecnología Médica',
     'Word 365 · Excel 365 · Canva · Excel Asociado · SPSS · Base de datos científicos'),
    ('2', 'Derecho, Psicología, Trabajo Social', 'Word 365 · Excel 365 · Canva · Word Asociado · Excel Asociado · SPSS'),
    ('3', 'Administración (y Emprendimiento, Marketing), Contabilidad (y Finanzas), Negocios Internacionales, Turismo, '
          'Agroindustrial', 'Word 365 · Excel 365 · Canva · Excel Asociado · Project · Power BI'),
    ('4', 'Arquitectura, Ingeniería Civil, Diseño de Interiores', 'Excel Asociado · AutoCAD 2D · AutoCAD 3D · Sketchup · Project · Revit'),
    ('5', 'Ingeniería de Sistemas, de Software, Industrial', 'Excel Asociado · AutoCAD 2D · AutoCAD 3D · Bizagi · Diseño Web · Power BI'),
    ('6', 'Ingeniería Mecánica Eléctrica, Civil, Arquitectura', 'Excel Asociado · AutoCAD 2D · AutoCAD 3D · SolidWorks · MatLab · '
                                                              'Diseño Mecánico'),
    ('7 · XP 07 (CMEMC44)', 'Artes y Diseño Gráfico, Ciencias de la Comunicación, Ingeniería de Sistemas, de Software',
     'Word 365 · Excel 365 · Canva · Word Asociado · Excel Asociado · Diseño Web'),
]

PROMPTS = [
    '¿Qué cursos tiene la ruta de aprendizaje de Ingeniería de Software?',
    '¿Cómo admito a un alumno de pregrado en su ruta de Computación con SAAQUIK?',
    '¿Cuál es el orden del encabezado de SFAREGS y qué estatus pongo?',
    '¿Cómo se matricula el alumno por Autoservicio en un curso de su ruta?',
    '¿Cómo creo un NRC de Computación en SSASECT, paso a paso?',
    '¿Cómo veo si un curso está en la malla del programa del alumno (SMAAREA)?',
    '¿Cómo asigno los programas que pueden matricularse en un NRC con SSARRES?',
    '¿Cuánto cuesta un curso y un taller en Chiclayo y en filiales?',
    '¿Qué hago si sale «El modo de calificar no es válido para la calificación ingresada»?',
    '¿Qué dudas siguen abiertas sobre las rutas de aprendizaje?',
]


def s_cover(p):
    build_cover(p, 'RUTA DE APRENDIZAJE', 'INSCRIPCIÓN, NRC Y PROGRAMAS · CENTRO DE INFORMÁTICA',
                'Repaso para la reunión con el Ing. Daniel Salazar · 27/10/2026')


def s_agenda(p):
    S = Slide(p, 'LO QUE VAMOS A VER')
    S.note('Hoy con el jefe del Centro de Informática: **cómo se inscribe un alumno en su ruta de aprendizaje** y **cómo se crea el '
           'NRC y se le asignan los programas**. Todo lo de aquí está probado en TEST o citado del instructivo.', kind='purple',
           sz=1500)
    S.chevrons([('Rutas', 'Qué son y cuántas'), ('Inscribir', 'Alumno en su ruta'), ('Crear el NRC', 'Malla y programación'),
                ('Programas', 'Asignar al NRC'), ('Repaso', 'Sitio y asistente IA')], h=760000, sz=1400)
    seen = set()
    columnas(S, [
        ('Hoy en SEUSS', [ex('Campus Virtual › Procesos en línea › Matrícula en línea › logo del Centro de Informática › modalidad › '
                             'curso y sección › modalidad de pago.', seen)], GRAYL, MUT),
        ('En Banner', [ex('El alumno se **admite en el programa XP de su ruta** (SAAQUIK) y se matricula en el NRC (SFAREGS o '
                          'Autoservicio).', seen),
                       ex('El NRC se crea en SSASECT para un curso que está en la **malla del programa** (SMAAREA) y se le '
                          '**asignan los programas** que pueden matricularse (SSARRES).', seen)],
         PURL, PURD),
    ], sz=1500, titulo_sz=1600)
    S.save()


def s_rutas(p):
    S = Slide(p, 'QUÉ ES UNA RUTA DE APRENDIZAJE')
    S.note('Se acredita en **5.º y 6.º ciclo** con **3 cursos de su ruta**, en el orden que quiera y en paralelo, **+ 1 Taller de '
           'Certificación Internacional**. Cada ruta es un **programa XP** en Banner.', kind='info', sz=1400)
    rows = [[{'text': r, 'bold': True, 'color': PURD}, e, c] for r, e, c in RUTAS]
    S.table([17, 41, 42], ['Ruta', 'Escuelas profesionales', 'Cursos (y el taller)'], rows, lo=950, hi=1250, reserve=420000)
    S.text('Fuente: carpeta acreditaciones-uss (láminas 5 a 8, 2026). Códigos de las rutas 2 a 6: por confirmar (U37).',
           sz=1100, y=YB - 300000)
    S.save()


def s_bpm_inscripcion(p):
    S = Slide(p, 'BPM: INSCRIBIR AL ALUMNO EN SU RUTA')
    S.text('Dagner, ve en este orden:', sz=1500, color=INK, bold=True)
    S.chevrons([('Ruta', 'según su escuela'), ('GOAMTCH', 'persona, si no existe'), ('SAAQUIK', 'admitir en el XP'),
                ('SGASTDN', 'ver el plan'), ('SFAREGS', 'matricular el NRC'), ('TSAAREV', 'cargo y pago')], h=820000, sz=1250)
    seen = set()
    columnas(S, [
        ('Si ya es alumno de pregrado', [ex('No va a GOAMTCH: ya existe. Se le agrega el currículo del centro en SAAQUIK o en '
                                            'SFAREGS › Currículos con «+» (C100).', seen),
                                         ex('En SFAREGS se elige el **plan de estudios del centro**, no el 1 (C86).', seen)],
         PURL, PURD),
        ('Por Autoservicio (el alumno)', ['Elige su plan del centro › pestaña **Proyecciones** › agrega el NRC › **Enviar**.',
                                          'Queda **RW**, inscrito por autoservicio (C71).'], GRNL, GRND),
        ('Al terminar', [ex('SMARQCM: el CAPP muestra el curso dentro del área de su programa XP.', seen),
                         'El cargo sale en la cuenta corriente; el pago sigue la modalidad elegida.'], GRAYL, MUT),
    ], sz=1450, titulo_sz=1550)
    S.save()


def s_saaquik(p):
    S = Slide(p, 'PASO A PASO: ADMITIR EN LA RUTA (SAAQUIK)')
    seen = set()
    rows = [
        ['1', 'Encabezado', ex('ID del alumno, periodo 202656, nivel **C** › **Ir**', seen)],
        ['2', 'Detalles', 'Tipo de alumno R o I · estatus **AS** · residencia **R**'],
        ['3', 'Currículo, prioridad 1', 'Programa › ••• › «**Reglas de currículo base por programa**» › el **programa XP de su ruta** › OK'],
        ['4', 'Lo pone Banner', 'Mayor **ACXP** · departamento **EMCI** · campus **S** · estatus INPROGRESS'],
        ['5', 'Guardar', '«Saved successfully (3 rows saved)»'],
        ['6', 'Verificar', ex('SGASTDN: el plan del centro está activo junto al de pregrado', seen)],
    ]
    S.table([7, 22, 71], ['N.º', 'Bloque', 'Qué pones'], rows, lo=1100, hi=1500, reserve=900000)
    S.note('Ejemplo: alumno de **Ingeniería de Software** que quiere **Diseño Web** → ruta **7** → programa **CMEMC44** (XP 07), como '
           'el alumno del NRC 10044 (C125).', kind='info', sz=1300)
    S.save()


def s_sfaregs(p):
    S = Slide(p, 'PASO A PASO: MATRICULAR EN UN CURSO DE SU RUTA')
    seen = set()
    rows = [
        ['1', ex('SFAREGS · encabezado', seen), 'Periodo → ID → **plan de estudios al final** (no asumas 1) › **Ir**'],
        ['2', 'Información de ingreso', 'Estatus **EL** · en el plan de estudios de ingreso, el plan y **EL** › **Guardar**'],
        ['3', 'Cursos', 'Botón **⤓** (sección siguiente) › NRC › **Tab** › **Guardar**'],
        ['4', 'Resultado', 'El curso queda **RE**; el cupo del NRC baja en SSASECQ'],
        ['5', ex('TSAAREV', seen), 'Aparece el cargo (S/ 420 en Chiclayo; S/ 240 en filiales)'],
    ]
    S.table([7, 25, 68], ['N.º', 'Dónde', 'Qué haces'], rows, lo=1100, hi=1500, reserve=1300000)
    columnas(S, [
        ('Si sale un error', ['«Closed»: sin cupo (Script 15) · «Duplicate Course»: ya lleva ese curso · «tiene retenciones»: '
                              'SOAHOLD (Script 18-B).'], AMBL, AMBD),
        ('Pago (hoy)', ['Contado −5 % (paga antes) · 3 cuotas (paga la 1.ª) · 2 cuotas · diferido +5 %. No se anula una vez '
                        'programado.'], GRAYL, MUT),
    ], sz=1450, titulo_sz=1500)
    S.save()


def s_bpm_nrc(p):
    S = Slide(p, 'BPM: CREAR EL NRC')
    S.text('Dagner, ve en este orden (primero mira **a qué malla va el alumno**):', sz=1500, color=INK, bold=True)
    S.chevrons([('Malla', 'el curso en el XP'), ('SOATERM', 'periodo y parte'), ('SSASECT', 'crear el NRC'),
                ('SSASECT', 'cupo, horario, docente'), ('SSARRES', 'asignar programas'), ('SFAREGS', 'matricular')],
               h=820000, sz=1250)
    seen = set()
    columnas(S, [
        ('Primero, la malla', [ex('El curso del NRC tiene que estar en la **malla del programa XP** del alumno (SMAPROG y SMAAREA). Si no '
                                  'está, **hay que hacer la malla y la programación** antes de crear el NRC.', seen)], PURL, PURD),
        ('Lo hace Pregrado', ['Asignar las **escuelas** a las **rutas** lo hace Pregrado. El centro **asigna los programas** al NRC.'],
         AMBL, AMBD),
        ('Ejemplo real', ['NRC **10044** Diseño Web (ESEC 00684, X06, cupo 40), para el alumno con el programa **CMEMC44** (XP 07).'],
         GRAYL, MUT),
    ], sz=1400, titulo_sz=1500)
    S.save()


def s_ssasect(p):
    S = Slide(p, 'PASO A PASO: CREAR EL NRC (SSASECT)')
    rows = [
        ['1', 'Encabezado', 'Periodo **202656** · NRC vacío · **Crear NRC** (o **Copiar NRC** de uno que ya existe)'],
        ['2', 'Información de sección', 'Materia **ESEC** y número del curso · sección (A, B…) · campus **S** · estatus activo · tipo de '
                                        'horario · modo **V** · parte de periodo (**X05 a X07**) · **Guardar**: «ADD» pasa a número'],
        ['3', 'Información de ingreso', 'Cupo en **Proyectado** (por ejemplo, 40) antes de «Lugares reservados» · **Guardar**'],
        ['4', 'Instructor y horas', 'CLAS, horario en 24 h, días, sesión 01 · **SAUVIR / SALA VIRT.** con **O** en sobrepaso · docente '
                                    'principal al 100 % · **Guardar**'],
        ['5', 'Verificar', 'SSASECQ: el NRC aparece con su cupo'],
    ]
    S.table([7, 22, 71], ['N.º', 'Pestaña', 'Qué pones'], rows, lo=1100, hi=1450, reserve=900000)
    S.note('Instructivo **5.3 Registrar la oferta horaria**, diapositivas 19 a 32; probado con el NRC 10044 (C97). No cambies de '
           'pestaña sin **Guardar**: sale «Debe guardar antes de salir de la información de sección».', kind='info', sz=1250)
    S.save()


def s_malla(p):
    S = Slide(p, 'SI EL CURSO NO ESTÁ EN LA MALLA')
    S.text('Antes del NRC hay que **hacer la malla y la programación**. Quién la hace está por confirmar (U40).', sz=1450,
           color=INK)
    seen = set()
    rows = [
        ['1', ex('SMAAREA', seen), 'Abrir el área del **programa XP** (por ejemplo MC38-01) y ver si el curso está en su regla', '1.2.1 diap. 23–25'],
        ['2', ex('SCACRSE', seen), 'Si el curso no existe: crearlo (materia ESEC, número nuevo, escuela EM, departamento EMCI, nivel C, modo V; '
                                   'mejor **Copiar** uno parecido)', '1.1.4 diap. 20–25'],
        ['3', 'SMAAREA', 'En la regla del área: **Insertar** ESEC y el número; si cambia la malla, **Copiar** al periodo nuevo', '1.3.1 diap. 10–13'],
        ['4', ex('SMAPROG', seen), 'El área sigue en la malla del programa, con su calificación mínima', '1.2.1 diap. 31'],
    ]
    S.table([6, 22, 52, 20], ['N.º', 'Página', 'Qué haces', 'Instructivo'], rows, lo=1050, hi=1400)
    S.save()


def s_programas(p):
    S = Slide(p, 'ASIGNAR PROGRAMAS AL NRC (SSARRES)')
    S.chevrons([('Escuela', 'la asigna Pregrado'), ('Ruta', 'agrupación 1 a 7'), ('Programa XP', 'CMEMC38 … 44'),
                ('NRC', 'SSARRES')], h=700000, sz=1300, fill=GRND)
    seen = set()
    rows = [
        ['1', ex('SSARRES: desde el menú relacionado de SSASECT o desde Experience', seen), '5.3 diap. 44'],
        ['2', 'Pestaña **Grado y Programa** › Restricción **Incluir** › el **programa XP** (o los programas) que llevan el curso › '
              '**Guardar**: solo esos alumnos podrán matricularse', '5.3 diap. 48'],
        ['3', 'Si hace falta: **Clase y Nivel** (nivel C) y **Campus** (S)', '5.3 diap. 47 y 49'],
        ['4', 'Lo que venga del catálogo (SCARRES) aparece aquí y se puede ajustar', '5.3 diap. 46'],
        ['5', 'Probar: un alumno de otro programa no debe poder matricularse en SFAREGS', 'Por probar'],
    ]
    S.table([6, 70, 24], ['N.º', 'Qué haces', 'Instructivo'], rows, lo=1100, hi=1400)
    S.save()


def s_sitio(p):
    S = Slide(p, 'DÓNDE LO VES EN MI SITIO')
    S.note(f'Sitio: **{SITIO}** (se publica desde la rama main). Cada diagrama tiene la guía paso a paso y la diapositiva del '
           'instructivo en cada paso.', kind='purple', sz=1350)
    base = '/centros/computacion/diagramas/'
    rows = [
        ['Galería de diagramas', '/centros/index.html'],
        ['Persona y admisión', base + '04-persona-y-admision/'],
        ['Matrícula en el NRC', base + '05-matricula-en-el-nrc/'],
        ['Diseño de mallas y programas (Script 11-B)', base + '08-script-11-b-diseno-de-mallas-y-programas/'],
        ['Matrícula regular (Script 01)', base + '11-script-01-matricula-regular/'],
        ['Visor de instructivos (1.1.4, 1.1.5, 1.2.1, 1.3.1)', '/visor_instructivos/'],
    ]
    S.table([38, 62], ['Qué', 'Ruta en el sitio'], [[{'text': a, 'bold': True}, {'text': b, 'color': PURD}] for a, b in rows],
            lo=1100, hi=1400)
    S.save()


def s_prompts(p):
    S = Slide(p, 'PROMPTS PARA EL ASISTENTE IA')
    S.text('Abre el asistente en cualquier diagrama del sitio y copia la pregunta. Si responde algo incompleto, sigue con «¿y cuáles '
           'son?»: recuerda la conversación.', sz=1300)
    gap = 220000
    cw = (XW - gap) / 2
    y0 = S.y
    for i in range(2):
        items = PROMPTS[i * 5:(i + 1) * 5]
        ps = ''.join(para([(f'{i * 5 + k}.  ', 1550, True, PURD), (q, 1550, False, INK)], spc_after=1100)
                     for k, q in enumerate(items, 1))
        box(S, X0 + i * (cw + gap), y0, cw, YB - y0, ps, fill=PURL if i == 0 else GRNL, line=PURL if i == 0 else GRNL,
            ins=(200000, 180000, 200000, 120000))
    S.save()


def s_errores(p):
    S = Slide(p, 'SI ALGO SALE MAL')
    rows = [
        ['«no existe la tabla o vista» en SFAREGS', 'Pusiste el plan antes del periodo y el ID', 'Periodo → ID → plan (C86)'],
        ['«Closed» al matricular', 'El NRC no tiene cupo', 'Subir el cupo en SSASECT o sobrepaso (Scripts 15 y 02)'],
        ['«La persona tiene retenciones»', 'Retención activa', 'SOAHOLD: fecha de fin = hoy (Script 18-B)'],
        ['«Debe guardar antes de salir de la información de sección»', 'Cambiaste de pestaña en SSASECT sin guardar', 'Guardar primero (C97)'],
        ['«Conflicto de salón» en SSASECT', 'Todos los NRC virtuales usan SAUVIR', 'Poner O en sobrepaso (C97)'],
        ['El curso no cuenta en el CAPP', 'No está en el área del programa XP', 'Agregarlo en SMAAREA (1.2.1)'],
        ['«El modo de calificar no es válido…»', 'La nota no tiene modo V en SHAGRDE', 'Agregar V a esa nota (C124)'],
        ['La nota final sale APRO', 'Arriba de SHAGCOM está AST_70', 'Poner VIG_11 arriba (C123)'],
    ]
    S.table([34, 30, 36], ['Mensaje o síntoma', 'Causa', 'Qué hacer'], rows, lo=1100, hi=1400)
    S.save()


def s_dudas(p):
    S = Slide(p, 'PARA PREGUNTAR EN LA REUNIÓN')
    qs = [
        '**U37** ¿Qué código tiene cada ruta (CMEMC39 a CMEMC43)? (Las escuelas a las rutas las asigna Pregrado.)',
        '**U40** Cuando un curso no está en la malla, ¿quién hace la malla y la programación (SCACRSE, SMAAREA): el centro o Registros?',
        '**U41** En SSARRES, ¿un NRC se abre a todos los programas XP que llevan el curso, o se crea un NRC por ruta?',
        '**U35** ¿Se acredita con 4 talleres (lámina 2026) o con un 4.º curso (PDF 2025)?',
        '**U38** Si el retiro está prohibido (Acuerdo 0453-2013), ¿se bloquea en Banner?',
    ]
    seen = set()
    ps = ''.join(para([(f'{i}.  ', 1700, True, PURD), (ex(q, seen), 1700, False, INK)], spc_after=1300) for i, q in enumerate(qs, 1))
    box(S, X0, S.y, XW, YB - S.y, ps, fill=PURL, line=PURL, ins=(250000, 220000, 250000, 120000))
    S.save()


def main():
    plan = [('cover', s_cover), ('text', s_agenda), ('text', s_rutas),
            ('div', lambda p: build_div(p, '1. INSCRIBIR AL ALUMNO EN SU RUTA',
                                        'Admitirlo en el programa XP de su ruta y matricularlo en un curso de esa ruta.')),
            ('text', s_bpm_inscripcion), ('text', s_saaquik), ('text', s_sfaregs),
            ('div', lambda p: build_div(p, '2. CREAR EL NRC Y ASIGNAR PROGRAMAS',
                                        'Ver a qué malla va el alumno, programar el NRC y abrirlo a los programas de la ruta.')),
            ('text', s_bpm_nrc), ('text', s_ssasect), ('text', s_malla), ('text', s_programas),
            ('div', lambda p: build_div(p, '3. REPASO', 'Dónde verlo en el sitio, qué preguntarle al asistente y qué dudas llevar.')),
            ('text', s_sitio), ('text', s_prompts), ('text', s_errores), ('text', s_dudas)]
    u, paths = build_structure(tempfile.mkdtemp(prefix='deck_ruta_'), [k for k, _ in plan])
    for (kind, fn), path in zip(plan, paths):
        if fn:
            fn(path)
    out = sys.argv[1] if len(sys.argv) > 1 else OUT
    finalize(u, out, 'Ruta de aprendizaje: inscripción y cursos nuevos - Centro de Informática')
    print('OK', out, len(paths), 'diapositivas')


if __name__ == '__main__':
    main()
