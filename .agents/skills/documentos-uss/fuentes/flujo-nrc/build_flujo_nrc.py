# -*- coding: utf-8 -*-
"""«Del periodo al alumno: periodo, curso o NRC, docente, fórmula y cambio de sección» (PDF, 28/10/2026).

Repaso para la reunión del 29/10/2026: el orden de los pasos en Banner, quién hace cada uno, por qué el centro
crea el NRC y no el curso, la fórmula de notas del NRC 10044 y el cambio de sección. Cada paso lleva la lámina
del instructivo que lo muestra. Usa el estilo de scripts/pdf/ejemplo_centros.py (tarjetas, tres centros, dudas
al final y glosario).

Uso: python3 build_flujo_nrc.py ["<salida>.pdf"]   (por defecto, en docs/capacitacion/)
"""
import html
import os
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[4]
sys.path.insert(0, str(AQUI.parents[1] / 'scripts' / 'pdf'))

from common import AUTHOR, check_pdf, explicar, glosario_html, header, render, section  # noqa: E402
from common import fmt as _fmt  # noqa: E402
from ejemplo_centros import ARROW, CSS as CSS_EJEMPLO, bullets, regla  # noqa: E402

NOMBRE = 'FLUJO DEL NRC - PERIODO, CURSO, DOCENTE, FÓRMULA Y ALUMNO - CENTROS EMPRESARIALES.pdf'
OUT = sys.argv[1] if len(sys.argv) > 1 else str(RAIZ / 'docs' / 'capacitacion' / NOMBRE)
DIAPOS = RAIZ / 'visor_instructivos' / 'diapositivas'


def fmt(text):
    """fmt() de common más `código` en monoespaciado."""
    return re.sub(r'`([^`]+)`', r'<span class="code">\1</span>', _fmt(text))


def lamina(carpeta, n, pie):
    """Recorte de la diapositiva n del instructivo (generado por herramientas/diapositivas.py)."""
    ruta = DIAPOS / carpeta / 'recortes' / f'{n:03d}.webp'
    if not ruta.exists():
        sys.exit(f'Falta {ruta}: ejecuta herramientas/diapositivas.py')
    return (f'<figure class="fn-lam"><img src="file://{ruta}" alt=""><figcaption>{fmt(pie)}</figcaption></figure>')


def flow(items):
    return '<div class="flow">' + ARROW.join(f'<span class="{c}">{fmt(t)}</span>' for t, c in items) + '</div>'


def paso(n, titulo, quien, pasos, fig, probado=None, centros=None, ojo=None):
    """Tarjeta de un paso: lista numerada a la izquierda, lámina a la derecha y filas de abajo."""
    filas = ''
    if centros:
        filas += ('<div class="r fn-tres"><span class="lab">Tres centros</span><div class="fn-c3">'
                  + ''.join(f'<div class="fn-cc {k}"><span class="fn-ccn">{nom}</span><div>{fmt(t)}</div></div>' for k, nom, t in centros)
                  + '</div></div>')
    if probado:
        filas += f'<div class="r res"><span class="lab">Probado en TEST</span><div>{fmt(probado)}</div></div>'
    if ojo:
        filas += f'<div class="r ojo"><span class="lab">Ojo</span><div>{fmt(ojo)}</div></div>'
    return explicar(
        f'<div class="fn-pas"><div class="fn-top"><div class="fn-head"><span class="fn-num">{n}</span><b>{html.escape(titulo)}</b>'
        f'<span class="fn-quien">{html.escape(quien)}</span></div>'
        f'<ol class="fn-steps">{"".join(f"<li>{fmt(x)}</li>" for x in pasos)}</ol></div>{fig}{filas}</div>')


# ------------------------------------------------------------------ 1. el flujo
CADENA = [
    ('1', 'Periodo', 'Registros Académicos'),
    ('2', 'Curso', 'solo si no existe'),
    ('3', 'NRC (sección)', 'el centro'),
    ('4', 'Docente', 'jefe del centro'),
    ('5', 'Fórmula', 'Registros Académicos'),
    ('6', 'Alumno', 'el centro'),
    ('7', 'Cambio de sección', 'si hace falta'),
]

ORDEN = [
    '**Curso antes que NRC:** Banner programa NRC solo de cursos que ya están en el catálogo (SCACRSE). Sin curso no hay NRC '
    '(instructivo 5.3, diap. 53).',
    '**Docente antes que alumno:** para asignar al docente, el NRC debe tener su horario (6.2.1, diap. 12). Su carga pasa por el '
    'visto bueno del jefe y la aprobación del Vicerrectorado Académico antes de las clases (C47, C48). El alumno no hace falta para eso.',
    '**Fórmula antes de calificar:** el plan de notas del NRC se carga antes de que el docente registre notas, y se revisa la escala de '
    'arriba (C123).',
    '**Alumno al final:** se matricula en un NRC que ya existe y tiene cupo (5.4). Se puede matricular mientras se aprueba la carga '
    'del docente: lo único obligatorio es que el NRC exista.',
]

# ------------------------------------------------------------------ 2. curso frente a NRC
CURSO_VS_NRC = (
    'Curso y NRC no son lo mismo',
    ['Los periodos y la carga lectiva los ve **Registros Académicos**; las **secciones (NRC) las registran las escuelas** (C06).',
     'El curso es el mismo todos los ciclos; lo que cambia cada ciclo es la sección: horario, cupo y docente.'],
    ['**Curso** = la asignatura del **catálogo** (SCACRSE). Se crea **una vez** y sirve para todos los periodos. Lo usan la malla '
     '(SMAAREA) y el CAPP. Su instructivo (1.1.4) es de la Capacidad 1, **Diseño curricular**: «se crearán y mantendrán los cursos '
     'que son ofertados en la institución» (diap. 6).',
     '**NRC** = la **sección** de ese curso en un periodo (SSASECT): sección, parte de periodo, horario, cupo y docente. Se crea '
     '**cada periodo**. Su instructivo (5.3) es de la Capacidad 5, **Programación académica** «de cada periodo» (diap. 6).',
     '**Por eso el centro crea el NRC y no el curso:** un curso mal creado afecta la malla y el CAPP de todos los programas que lo '
     'usan. En Banner, el catálogo lo mantiene el área de diseño curricular; en la USS, quién crea un curso nuevo **está por '
     'confirmar** (U40).'],
    'Instructivos 1.1.4 (diap. 6) y 5.3 (diap. 6 y 53); C06',
)

EJ_CURSO_NRC = [
    ('ing', 'Inglés', '**ESEP 02458** BASIC III, del catálogo', '**10010**: sección AT, parte I10, lunes 18:00–20:30, aula SAUVIR, liga TA'),
    ('inf', 'Informática', '**ESEC 00684** Diseño Web, del catálogo', '**10044**: sección A, parte X06, 202656, docente 100582059'),
    ('emp', 'Emprendimiento', '**ESGE 00117** Emprendimiento I, del catálogo', '**1025**: sección A, 202656'),
]

# ------------------------------------------------------------------ pasos
PASO_PERIODO = dict(
    n='1', titulo='Crear el periodo', quien='Registros Académicos (C06)',
    pasos=['**STVTERM:** `+`, código de 6 dígitos (año + 5 + secuencia), descripción, fechas de inicio y fin, año académico y tipo. '
           'Las fechas de alojamiento y el año de ayuda financiera también se llenan. Guardar (1.1.1, diap. 18–21).',
           '**SOATERM:** el periodo › Ir. Lo más rápido: «Copiar De periodo» con uno ya configurado › COPIAR (1.1.2, diap. 16).',
           '**SOATERM:** número inicial de NRC e inscripción **Permitir** marcada (diap. 17–18).',
           '**SOATERM › Partes de periodo:** `+` por cada parte, con fechas, semanas y censo (diap. 20–21).',
           '**SOATERM › Web:** fechas de inscripción web y de acceso docente; calificaciones parciales y finales marcadas (diap. 22–24).',
           '**SSAEXCL:** los feriados de cada parte (diap. 34–35).'],
    fig=lamina('1.1.2_Programar_el_inicio_y_finalizacio_n_de_per_acad', 16, '1.1.2, diap. 16 · SOATERM: periodo y «Copiar De periodo»'),
    centros=[('ing', 'Inglés', 'partes **I01 a I12**'), ('inf', 'Informática', 'partes **X01 a X07**'),
             ('emp', 'Emprendimiento', 'partes **P01 a P06**')],
    probado='Script 11: periodo **202751** (verano 2027), primer NRC 1000, inscripción web del 20-SEP-2026 al 15-MAR-2027, acceso '
            'docente del 03-ENE al 05-ABR-2027 y parte X01 del 12-ENE al 22-FEB-2027 (6 semanas). Falta la X02 (U22).',
)

PASO_CURSO = dict(
    n='2a', titulo='Crear el curso (solo si no está en el catálogo)', quien='Diseño curricular o Registros (por confirmar, U40)',
    pasos=['**SCACRSE**, encabezado: materia, **número nuevo** (revisar el último que existe) y periodo **000000**: los cursos del catálogo '
           'quedan del periodo 000000 al 999999. Lo más seguro: **Copiar** de un curso real del mismo centro (1.1.4, diap. 20).',
           '**Detalles:** título, escuela `EM`, departamento del centro y estatus activo (diap. 21).',
           '**Horas:** créditos y cobro **variables** (inferior 0, indicador «O», superior: Basic I 0 O 1, Emprendimiento I 0 O 4); '
           'teoría y laboratorio, las del sílabo (Emprendimiento I fijas 1 y 2; Basic I variables 0 O 4 y 0 O 3); el contacto lo suma Banner (diap. 22).',
           '**Nivel** del centro y **modo de calificar** predefinido (diap. 23–24).',
           '**Tipo de horario** y método educativo; la carga de trabajo es la que verá el docente (diap. 25).',
           '**SCADETL:** la cuota del curso, si la tiene.',
           '**SMAAREA:** poner el curso en el área de la **malla** de cada programa que lo lleva (1.2.1, diap. 23–25). El curso se crea '
           '**antes** de tocar el área (1.3.1, diap. 5).'],
    fig=lamina('1.1.4_Disen_ar_y_crear_los_cursos', 20, '1.1.4, diap. 20 · SCACRSE: materia, curso, periodo y «Copiar»'),
    centros=[('ing', 'Inglés', 'nivel `I`, depto. `EMID`, modo `C` (0–100)'), ('inf', 'Informática', 'nivel `C`, depto. `EMCI`, modo `V` (0–20)'),
             ('emp', 'Emprendimiento', 'nivel `M`, depto. `EMEM`, modo `V` (0–20)')],
    ojo='En TEST el número de curso más alto conocido de Informática es ESEC 00700. Si el curso ya existe, este paso **no se hace**.',
)

PASO_NRC = dict(
    n='2b', titulo='Crear el NRC, que es la sección', quien='El centro',
    pasos=['**SOATERM:** que la parte de periodo esté habilitada para programar (5.3, diap. 15–16).',
           '**SSASECT**, encabezado: periodo, NRC vacío › **Crear NRC** (o «Copiar NRC») (5.3, diap. 19).',
           '**Información de sección:** materia y número, sección, campus `S`, estatus activo, tipo de horario, modo, parte de periodo, '
           'horas crédito y de cobro; Calificable sin dispensa. **Guardar** antes de cambiar de pestaña: Banner da el NRC (diap. 20–26).',
           '**Información de ingreso:** cupo máximo y **Proyectado** (antes de «Lugares reservados»). Guardar (diap. 27–28).',
           '**Instructor y horas de reunión:** días y horario en 24 h, sesión 01, aula. Con `SAUVIR` / `SALA-VIRT` va siempre `O` en '
           '«Indicador de sobrepaso» (diap. 29–30).',
           '**SSARRES**, solo si hay que limitar quién se matricula (restricciones; no asigna programas) (diap. 44–51).'],
    fig=lamina('5.3_4.1.4.1.6_Instructivo_Registrar_la_oferta_horaria_de_los_cursos', 21,
               '5.3, diap. 21 · SSASECT: materia, curso, sección, campus y estatus'),
    centros=[('ing', 'Inglés', 'sección **AT** (teórico) con liga **TA**, y los prácticos **AC1, AC2…** con liga **PA**'),
             ('inf', 'Informática', 'sección **A**, sin ligas'), ('emp', 'Emprendimiento', 'sección **A**, sin ligas')],
    probado='NRC **10044** (ESEC 00684 Diseño Web): 202656, sección A, campus S, TEO, VIRT, modo V, parte X06 (07-SEP al 31-OCT), '
            '1 crédito, cupo y proyectado 40 (C97).',
)

PASO_DOCENTE = dict(
    n='3', titulo='Asignar el docente', quien='Jefe del centro; aprueba el Vicerrectorado Académico',
    pasos=['**SIAINST:** el docente debe estar activo en el periodo, con su contrato y regla (5.2, diap. 17–20). Si no lo está, lo '
           'registra quien administra a los docentes.',
           '**SSASECT › Instructor y horas de reunión:** en el bloque Instructor, el **ID** del docente para la sesión 01 '
           '(6.2.1, diap. 14–15).',
           'Marcar **docente principal** y 100 % de responsabilidad; si hay dos, repartir el porcentaje (diap. 19).',
           'Si choca con otro NRC suyo, Banner no lo deja; se marca el **indicador de sobrepaso** del docente (diap. 20).',
           '**SIAASGN:** revisar su carga: NRC, horas y sobrecarga (5.2, diap. 23–27).',
           '**Oficio** por la intranet con el visto bueno del jefe › **resolución** del Vicerrectorado Académico (fuera de Banner, C47, C48).'],
    fig=lamina('6.2.1_Asignar_Docentes', 15, '6.2.1, diap. 15 · SSASECT: ID del docente en el bloque Instructor'),
    probado='NRC 10044 con el docente **100582059** como principal. Script 18-A: SIAASGN muestra la carga de los NRC 1021, 1022, 1024 '
            'y 1025 (Informática y Emprendimiento).',
)

PASO_FORMULA = dict(
    n='4', titulo='Cargar la fórmula de notas (plan de evaluación)', quien='Registros Académicos (C64)',
    pasos=['**SHAEGBC:** el calendario del libro de calificaciones del periodo (fecha abierta y de corte). Sin esto, SHAGCOM da error '
           '(7.1.4, diap. 40–41; C91).',
           '**SHAGCOM:** periodo y NRC › Ir (diap. 43).',
           'Arriba, en «Asignación de escala de calificación», la **escala del curso** (en Informática `VIG_11`), **no** la de asistencia '
           '(diap. 44; C123).',
           'Un componente por cada nota del sílabo: secuencia, nombre, descripción y **peso**; «Incluir en la calificación final» '
           '(diap. 45–48).',
           'La asistencia va como **ATTRGRD**: peso **0.00**, «**Debe aprobar**» y su escala de asistencia (7.1.0, diap. 29).',
           '**SOAATRK:** la regla de control de asistencia del periodo, parte o curso (7.1.1, diap. 34–37).'],
    fig=lamina('7.1.4_Ingresar_calificaci_autoservicio', 45, '7.1.4, diap. 45 · SHAGCOM: secuencia y nombre de cada componente'),
    centros=[('ing', 'Inglés', 'escala de 0 a 100, aprueba con **70**; código de escala por confirmar (E22)'),
             ('inf', 'Informática', '`VIG_11`: de 0 a 20, aprueba con **11**'),
             ('emp', 'Emprendimiento', 'de 0 a 20, aprueba con **11**; código de escala por confirmar (E22)')],
    ojo='En el NRC 10044 la nota final salió **APRO** porque arriba quedó `AST_70` (la escala de asistencia). Se corrigió después del '
        'pase a historia en SHATCKN (C120 a C124).',
)

FORMULA = [  # NRC 10044, sílabo de Diseño Web (C96, C98)
    ('TA1', 'Taller Online TA1', '15 %', '16', '2.40'),
    ('TA2', 'Taller Online TA2', '15 %', '14', '2.10'),
    ('PA', 'Participación en aula', '40 %', '17', '6.80'),
    ('EF', 'Examen final', '30 %', '15', '4.50'),
    ('ATTRGRD', 'Asistencia (debe aprobar, mínimo 70 %)', '0 %', '85 %', 'aprueba'),
]

PASO_ALUMNO = dict(
    n='5', titulo='Matricular al alumno', quien='El centro (asistente o especialista)',
    pasos=['**GOAMTCH**, solo si la persona no existe en Banner. Un alumno de pregrado ya existe.',
           '**SAAQUIK:** ID, periodo y nivel › Ir; tipo y estatus; en Currículo, el **programa del centro** con «Reglas de currículo base '
           'por programa». Otra vía: **SFAREGS › Currículos**, `+` y el programa (C100).',
           '**SFAREGS:** periodo › ID › plan de estudios (no asumir el 1) › Ir; estatus `EL` en «Información de ingreso» y en el plan; '
           'Guardar (5.4, diap. 35–37).',
           '**Información de curso:** el NRC › Tab › Guardar: queda `RE` (diap. 38–43). Si sale error: `DD` o sobrepaso (diap. 44).',
           '**TSAAREV:** el cargo del curso en la cuenta del alumno.'],
    fig=lamina('5.4_4.1.4.1.12_Instructivo_-_Ejecu.la_inscrip.de_cursos_por_backoffice', 38,
               '5.4, diap. 38 · SFAREGS: ingresar el NRC en «Información de curso»'),
    centros=[('ing', 'Inglés', 'programa **IMEMI03**'), ('inf', 'Informática', 'programa de su ruta: **CMEMC38** (XP 01) a **CMEMC44** (XP 07)'),
             ('emp', 'Emprendimiento', 'programa **MMEMM01**')],
    probado='El alumno 100582059 matriculado en el NRC 10044 con el currículo `CMEMC44` agregado desde SFAREGS › Currículos (C100).',
)

PASO_CAMBIO = dict(
    n='6', titulo='Cambio de sección: el alumno pasa a otro NRC', quien='El centro (por confirmar, U44)',
    pasos=['**SSASECT** del NRC destino: que tenga cupo. Si el cupo está reservado por programa, ampliar «Lugares reservados» (5.3, diap. 28).',
           '**SFAREGS:** periodo › ID › plan › Ir (5.4 retiro, diap. 39–41).',
           'En «Información de curso», al NRC de **origen** ponerle `DD` (diap. 42)…',
           '…y en la misma grabación agregar el NRC de **destino**, que queda `RE`. **Guardar** (diap. 43; 5.4, diap. 38–43).',
           '**SFASLST:** el alumno aparece en la lista del NRC nuevo y el cupo del origen se liberó.'],
    fig=lamina('5.4_4.1.4.1.16_Instructivo_-__Gestionar_retiro_de_cursos', 42,
               '5.4 retiro, diap. 42 · SFAREGS: código de retiro en el NRC de origen'),
    centros=[('ing', 'Inglés', 'con ligas, se cambian **juntos** el teórico y su práctico (la liga se valida al inscribir)'),
             ('inf', 'Informática', 'de la sección del NRC 1026 a la del 1021'),
             ('emp', 'Emprendimiento', 'grupos que se superponen, por ejemplo P02 y P03')],
    probado='Script 16: la alumna S00581109 pasó del NRC 1026 (`DD`) al 1021 (`RE`). Salió «Reserve Closed» y se resolvió ampliando la '
            'reserva del programa de 1 a 2 en SSASECT (C38).',
    ojo='Si lo que cambia es el **horario** del NRC (la sesión) y no el alumno: SSASECT › Instructor y horas de reunión › Fechas de '
        'reunión (5.3, diap. 29). El indicador de sesión une ese horario con su docente (6.2.1, diap. 14).',
)

DUDAS_ELLUCIAN = [
    '**E22:** ¿qué código de escala y modo de calificar van en SHAGCOM y SHAGRDE para Idiomas (0 a 100) y Emprendimiento (0 a 20)?',
    '**E26:** si el alumno cambia de NRC a mitad del curso, ¿sus notas parciales y su asistencia pasan al NRC nuevo o se vuelven a '
    'ingresar?',
]
DUDAS_USS = [
    '**U40:** cuando hace falta un curso nuevo, ¿quién lo crea en SCACRSE y lo pone en la malla: el centro o Registros Académicos?',
    '**U26:** ¿Registros Académicos solo abre el periodo, o también revisa la carga lectiva del docente?',
    '**U44:** ¿quién hace el cambio de sección (el centro o Registros Académicos) y hasta qué fecha del curso se permite?',
]


def cadena():
    return ('<div class="chain">' + ''.join(
        f'<div class="chev{" hi" if n in ("3", "4") else ""}"><b>{n}. {html.escape(t)}</b><span>{html.escape(q)}</span></div>'
        for n, t, q in CADENA) + '</div>')


def ejemplos_curso_nrc():
    return explicar('<div class="fn-cn">' + ''.join(
        f'<div class="fn-cnc {k}"><div class="fn-cnh">{nom}</div>'
        f'<div class="fn-cnr"><span class="lab">Curso</span>{fmt(c)}</div>'
        f'<div class="fn-cnr"><span class="lab">NRC</span>{fmt(s)}</div></div>'
        for k, nom, c, s in EJ_CURSO_NRC) + '</div>')


def formula():
    filas = ''.join(
        f'<div class="cr{" must" if c == "ATTRGRD" else ""}"><span><b>{c}</b> · {html.escape(d)}</span><span>{p}</span>'
        f'<span>{n}</span><span>{v}</span></div>' for c, d, p, n, v in FORMULA)
    return explicar(
        '<div class="fn-fx keep"><div class="fn-fxh">La fórmula del NRC 10044 (sílabo de Diseño Web, C96 y C98)</div>'
        '<div class="fn-fxe">Nota final = 0.15 × TA1 + 0.15 × TA2 + 0.40 × PA + 0.30 × EF · y si la asistencia es menor que 70 %, '
        'queda <b>INH</b></div>'
        '<div class="fn-calc"><div class="cr ch"><span>Componente</span><span>Peso</span><span>Nota de ejemplo</span><span>Aporte</span></div>'
        + filas +
        '<div class="cr tot"><span>Nota final</span><span>100 %</span><span></span><span><b>15.80</b></span></div></div>'
        '<p class="fn-nota">Las notas son <b>de ejemplo</b>. Con 60 % de asistencia, la misma nota da <b>INH</b>: la asistencia no suma '
        'puntos (peso 0), pero hay que aprobarla. El redondeo y la nota que se ve los da la escala del curso.</p></div>')


def build():
    b = [header('Universidad Señor de Sipán · Centros Empresariales',
                'Del periodo al alumno: periodo, NRC, docente y fórmula',
                'Pasos en Banner, quién hace cada uno y por qué el centro crea el NRC y no el curso. Reunión del 29/10/2026',
                [('Elaborado por', AUTHOR), ('Fecha', '28 de octubre de 2026'),
                 ('Fuentes', 'Instructivos 1.1, 5.2, 5.3, 5.4, 6.2.1 y 7.1 · pruebas en TEST'), ('Estado', 'Probado en TEST; dudas al final')])]

    b.append(explicar(
        '<div class="lead"><b>La respuesta corta:</b> el orden es <b>curso › NRC › docente › fórmula › alumno</b>. El centro <b>no crea '
        'cursos</b>: crea <b>NRC</b>, que son las <b>secciones</b> de un curso que ya existe en el catálogo. Cada paso trae la lámina '
        'del instructivo donde se ve. Las dudas están al final.</div>'))

    # 1. El flujo
    b.append(section(1, 'El flujo y quién hace cada paso'))
    b.append(cadena())
    b.append(explicar('<div class="rule"><div class="rh"><span class="k">?</span>¿Curso, docente o alumno primero?</div>'
                      f'<div class="blk ell">{bullets(ORDEN)}</div></div>'))

    # 2. Curso frente a NRC
    b.append(section(2, 'Por qué el centro crea el NRC y no el curso'))
    b.append(regla(1, *CURSO_VS_NRC))
    b.append('<div class="figcap">El mismo curso, su NRC en 202656</div>' + ejemplos_curso_nrc())

    # 3 a 8. Pasos
    b.append(section(3, 'Paso 1 · El periodo'))
    b.append(paso(**PASO_PERIODO))
    b.append(section(4, 'Paso 2 · El curso, si falta, y el NRC'))
    b.append(paso(**PASO_CURSO))
    b.append(paso(**PASO_NRC))
    b.append(section(5, 'Paso 3 · El docente'))
    b.append(paso(**PASO_DOCENTE))
    b.append(section(6, 'Paso 4 · La fórmula de notas'))
    b.append(paso(**PASO_FORMULA))
    b.append(formula())
    b.append(section(7, 'Paso 5 · El alumno'))
    b.append(paso(**PASO_ALUMNO))
    b.append(section(8, 'Paso 6 · Cambio de sección'))
    b.append(paso(**PASO_CAMBIO))

    # Dudas antes del glosario, para que sus términos entren en él
    dudas = ('<div class="dudas"><div class="dc">' + explicar('<div class="dh">Para Ellucian</div><ol>'
             + ''.join(f'<li>{fmt(q)}</li>' for q in DUDAS_ELLUCIAN) + '</ol>') + '</div>'
             '<div class="dc uss">' + explicar(f'<div class="dh">Para la USS</div><ol start="{len(DUDAS_ELLUCIAN) + 1}">'
             + ''.join(f'<li>{fmt(q)}</li>' for q in DUDAS_USS) + '</ol>') + '</div></div>')

    b.append(section(9, 'Glosario', 'Qué significa cada sigla y cada página de Banner del documento.'))
    b.append('<div class="glos keep"><div class="gh">Palabras del flujo</div><div class="gg">'
             '<div class="gi"><b>Curso</b><span>Asignatura del catálogo (SCACRSE); vale para todos los periodos.</span></div>'
             '<div class="gi"><b>NRC o sección</b><span>El curso ofrecido en un periodo, con horario, cupo y docente (SSASECT).</span></div>'
             '<div class="gi"><b>Fórmula</b><span>Plan de evaluación del NRC: componentes y pesos (SHAGCOM).</span></div>'
             '<div class="gi"><b>RE · DD · EL</b><span>Inscrito · retirado (libera el cupo) · elegible para inscribir.</span></div>'
             '<div class="gi"><b>INH</b><span>Inhabilitado: desaprueba por asistencia menor que 70 %.</span></div>'
             '<div class="gi"><b>Sobrepaso</b><span>Permiso para guardar a pesar de un error (cruce, cupo, aula).</span></div>'
             '</div></div>' + glosario_html())
    b.append(section(10, 'Dudas para confirmar'))
    b.append(dudas)
    return '\n'.join(b)


CSS = CSS_EJEMPLO + '''
.chain { margin: 2px 0 10px; }
.chev { padding: 7px 6px 7px 16px; }
.chev.hi { background: var(--p); color: #fff; }
.chev b { font-size: 8pt; } .chev span { font-size: 7pt; }
.rule .blk.ell { font-size: 8.8pt; }

/* curso frente a NRC */
.fn-cn { display: grid; grid-template-columns: repeat(3, 1fr); gap: 7px; margin: 0 0 6px; break-inside: avoid; }
.fn-cnc { border: 1px solid var(--line); border-top: 4px solid var(--ing); border-radius: 8px; padding: 6px 9px 7px; background: #fff; }
.fn-cnc.inf { border-top-color: var(--inf); } .fn-cnc.emp { border-top-color: var(--emp); }
.fn-cnh { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 9pt; margin-bottom: 3px; }
.fn-cnr { font-size: 8.2pt; line-height: 1.4; margin-top: 3px; }
.fn-cnr .lab { display: inline; margin-right: 5px; color: var(--mut); }

/* tarjeta de cada paso: cabecera y lista juntas; la lámina y las filas pueden pasar a la página siguiente */
.fn-pas { border: 1px solid var(--line); border-radius: 10px; overflow: hidden; margin: 0 0 10px; background: #fff; }
.fn-top { break-inside: avoid; }
.fn-head { display: flex; align-items: center; gap: 8px; padding: 6px 12px; background: var(--pl); border-bottom: 1px solid var(--pb); }
.fn-head b { font-family: 'Montserrat', sans-serif; font-size: 10.2pt; flex: 1; }
.fn-num { background: var(--p); color: #fff; border-radius: 6px; padding: 1px 7px; font-weight: 700; font-size: 8.6pt; }
.fn-quien { font-size: 7.6pt; font-weight: 700; color: var(--pd); background: #fff; border: 1px solid var(--pb); border-radius: 9px;
            padding: 1px 8px; white-space: nowrap; }
.fn-steps { margin: 0; padding: 8px 14px 6px 30px; font-size: 8.7pt; line-height: 1.45; font-weight: 400; }
.fn-steps li { margin: 0 0 3px; }
.fn-lam { margin: 2px 12px 9px; border: 1px solid var(--line); border-radius: 7px; overflow: hidden; background: #fff; break-inside: avoid; }
.fn-lam img { display: block; width: 100%; max-height: 72mm; object-fit: contain; background: #fff; }
.fn-lam figcaption { font-size: 7.2pt; color: var(--mut); padding: 3px 8px 4px; border-top: 1px solid var(--line); background: var(--pz); }
.fn-pas .r { grid-template-columns: 92px 1fr; break-inside: avoid; }
.r.fn-tres { background: #FAFAFC; }
.fn-c3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
.fn-cc { font-size: 8pt; line-height: 1.38; border-left: 3px solid var(--ing); padding-left: 6px; }
.fn-ccn { display: block; font-size: 7.4pt; font-weight: 700; color: var(--ing); }
.fn-cc.inf { border-left-color: var(--inf); } .fn-cc.inf .fn-ccn { color: var(--inf); }
.fn-cc.emp { border-left-color: var(--emp); } .fn-cc.emp .fn-ccn { color: var(--emp); }

/* fórmula */
.fn-fx { border: 1px solid var(--line); border-radius: 10px; padding: 8px 12px 6px; margin: 0 0 10px; background: #fff; }
.fn-fxh { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 9.6pt; margin-bottom: 4px; }
.fn-fxe { background: var(--pl); color: var(--pd); border-radius: 7px; padding: 5px 9px; font-size: 8.7pt; font-weight: 600; margin-bottom: 6px; }
.fn-calc { border: 1px solid var(--line); border-radius: 7px; overflow: hidden; font-size: 8.4pt; }
.fn-calc .cr { grid-template-columns: 2.4fr .7fr .9fr .7fr; }
.fn-nota { margin: 5px 0 0; font-size: 7.8pt; color: var(--mut); line-height: 1.4; }
'''


if __name__ == '__main__':
    p = render('flujo_nrc', build(), CSS, 'Del periodo al alumno: periodo, NRC, docente y fórmula · Centros Empresariales', OUT,
               'Del periodo al alumno: periodo, NRC, docente y fórmula - Centros Empresariales',
               'Pasos en Banner para crear el periodo, el NRC, asignar el docente, cargar la fórmula, matricular y cambiar de sección')
    check_pdf(p, png_dir=os.environ.get('PNG_DIR'))
