# -*- coding: utf-8 -*-
"""Resumen consolidado (temas 1 a 4) en HTML para imprimir a PDF con Chromium."""
import html
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
MEDIA = os.path.join(HERE, '..', 'prog_x', 'ppt', 'media')
AUTHOR = 'Dagner Anibal Chuman Lluen'

CODE = re.compile(r'\b([SGT][A-Z]{2}[A-Z0-9]{3,4})\b')


def fmt(text):
    """Texto plano → HTML: códigos Banner resaltados y **negrita**."""
    t = html.escape(text, quote=False)
    t = CODE.sub(r'<span class="code">\1</span>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    return t


def chips(codes):
    return ' '.join(f'<span class="pg">{html.escape(c)}</span>' for c in codes.split(', ')) if codes else ''


def section(num, title, intro=None):
    s = (f'<div class="sec"><span class="num">{num}</span><h2>{html.escape(title)}</h2><span class="bar"></span></div>')
    if intro:
        s += f'<p class="intro">{fmt(intro)}</p>'
    return s


def table(cols, rows, cls=''):
    """cols: [(título, ancho%)]; rows: listas de celdas HTML o ('grp', texto)."""
    colgroup = ''.join(f'<col style="width:{w}%">' for _, w in cols)
    head = ''.join(f'<th>{html.escape(c)}</th>' for c, _ in cols)
    body = ''
    for r in rows:
        if isinstance(r, tuple) and r[0] == 'grp':
            body += f'<tr class="grp"><td colspan="{len(cols)}">{fmt(r[1])}</td></tr>'
        else:
            body += '<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>'
    return (f'<table class="t {cls}"><colgroup>{colgroup}</colgroup><thead><tr>{head}</tr></thead>'
            f'<tbody>{body}</tbody></table>')


def steps(rows):
    """Tabla de pasos: (página(s), qué se hace, datos clave) o ('grp', texto)."""
    out, n = [], 0
    for r in rows:
        if r[0] == 'grp':
            out.append(r)
            continue
        n += 1
        pages, what, key = r
        out.append([f'<span class="n">{n}</span>', chips(pages), fmt(what), fmt(key)])
    return table([('N°', 5), ('Página', 19), ('Qué se hace', 28), ('Datos clave', 48)], out, 'steps')


def note(text, kind='info'):
    return f'<div class="note {kind}">{fmt(text)}</div>'


# ------------------------------------------------------------------ contenido
PANORAMA = [
    ('1', 'Periodos académicos', 'Crear el periodo, su calendario, partes de periodo y feriados.',
     'STVTERM, SOATERM, SSAEXCL', 'Registros Académicos', 'Cada periodo'),
    ('2', 'Programación de asignaturas', 'Crear los NRC con cupo, horario y docente.',
     'SSASECT', 'Escuelas', 'Cada mes (parte de periodo)'),
    ('2.1', 'Correquisitos, prerrequisitos y restricciones', 'Reglas de inscripción de cada NRC.',
     'SSADETL, SSAPREQ, SSARRES', 'Escuelas', 'Por NRC, si aplica'),
    ('3', 'Docentes', 'Registrar al docente, asignarlo al NRC y controlar su carga.',
     'SIAINST, SSASECT, SIAASGN', 'Registros Académicos', 'Por docente y periodo'),
    ('4', 'Admisión', 'Registrar al participante como estudiante.',
     'GOAMTCH, SAAQUIK, SGASTDN', 'Admisión', 'Por participante'),
]

SEQ = ['Periodo', 'NRC', 'Reglas del NRC', 'Docente', 'Participante', 'Inscripción']

PERIODOS = [
    ('grp', 'Configuración (una sola vez)'),
    ('STVPTRM', 'Crear las partes de periodo.', 'Código (3) y descripción (30). Debe existir la parte **1** (Periodo completo).'),
    ('STVACYR', 'Crear los años académicos.', 'Año (4) y descripción. Obligatorios **0000** y **9999**, los únicos con «Requerido por el sistema».'),
    ('STVTRMT', 'Crear los tipos de periodo.', 'Código (1): M, B, T, C, S, A (mensual a anual).'),
    ('grp', 'Por cada periodo'),
    ('STVTERM', 'Crear el periodo.', 'Código (6), ej. **202654**; descripción; fechas de inicio y fin; tipo de periodo; año académico. '
     'Fechas de alojamiento = las del periodo; año de ayuda financiera = año académico.'),
    ('SOATERM', 'Configurar el control del periodo.', 'NRC inicia en **1000**. Marcar: inscripción habilitada, plan de estudios requerido, '
     'estimación de cuotas en línea, modalidades Básico y Proyectado, control de periodo en web maestro.'),
    ('SOATERM', 'Verificación de errores de inscripción.', 'Poner en **Fatal** lo que se controla desde la programación o el catálogo.'),
    ('SOATERM', 'Controles de docente y asesor.', 'Marcar desplegar horario y lista de clases. **No** marcar aprobaciones/sobrepasos ni agregar/eliminar.'),
    ('SOATERM', 'Registrar las partes de periodo disponibles.', 'Parte 1 + partes del centro (ej. I01). Fechas, semanas y censo. '
     'Web del docente: calificaciones parciales y finales.'),
    ('SOATERM', 'Fechas de inscripción web y de acceso docente/asesor.', 'Un solo rango que englobe todas las partes. Sin fechas, no hay inscripción por autoservicio.'),
    ('SOATERM', 'Inscripción proyectada.', 'Periodo abierto para proyecciones; restringir a cursos proyectados y a proyecciones nulas.'),
    ('SSAEXCL', 'Registrar los feriados.', 'Por año y parte de periodo. Copiar a otra parte (vacía) con Herramientas › Predefinir exclusiones.'),
    ('SOATERM', 'Atajo: copiar el calendario.', 'Periodo nuevo + periodo origen › **Copiar**.'),
    ('grp', 'Al cerrar la inscripción'),
    ('SOATERM', 'Cerrar accesos web.', 'Desactivar control de periodo en web maestro, periodo de evaluación web y periodo de catálogo web.'),
]

PROGRAMACION = [
    ('grp', 'Tema 2 · Programación del NRC'),
    ('SSASECT', 'Crear el NRC.', 'Periodo; dejar el NRC en blanco › **Crear NRC**.'),
    ('SSASECT', 'Información de la sección.', 'Materia y número de curso, sección (letra **A** por ciclo y grupo), campus, estatus, '
     'tipo de horario, método educativo, modo de calificar (obligatorio) y sesión.'),
    ('SSASECT', 'Parte de periodo, horas y cobro.', 'Parte de periodo de SOATERM; verificar horas crédito y de cobro. '
     'TEO: calificable y con cobro. Otros tipos: dispensa de colegiatura (curso con créditos variables).'),
    ('SSASECT', 'Guardar.', 'Se genera el número de NRC según la secuencia de SOATERM.'),
    ('SSASECT', 'Cupos.', 'Detalles de ingreso: cupo máximo. Lugares reservados: regla nula obligatoria + una regla por nivel, campus, programa o atributo.'),
    ('SSASECT, STVMEET, GTVMTYP', 'Horario y docente.', 'Pestaña Instructor y horas de reunión: hora de reunión, tipo (CLAS), fechas, horas (24 h) y días. Docente: ver tema 3.'),
    ('grp', 'Tema 2.1 · Reglas del NRC (Menú relacionado de SSASECT)'),
    ('SSADETL', 'Correquisitos, ligas y atributos.', 'Hereda de **SCADETL**. Se ajusta solo para ese NRC.'),
    ('SSAPREQ', 'Prerrequisitos.', 'Hereda de **SCAPREQ**. Materia, curso, nivel y calificación mínima; combinar con Y / O. Ej.: BASIC II requiere BASIC I.'),
    ('SSARRES', 'Restricciones.', 'Hereda de **SCARRES**. **Incluir** o **Excluir** por nivel, programa, campus, atributo o cohorte.'),
]

DOCENTES = [
    ('grp', 'Configuración (una sola vez)'),
    ('STVFCST', 'Estatus del docente.', 'Código (2), ej. AC Activo.'),
    ('STVFSTP', 'Tipo de personal.', 'Código (4).'),
    ('STVFCNT', 'Tipo de contrato.', 'Código (2), ej. FT.'),
    ('STVWKLD', 'Códigos de regla de carga.', 'Código (6), ej. **AP090** = 90 horas académicas.'),
    ('grp', 'Por cada periodo'),
    ('SIATERM', 'Factores del periodo.', 'Factor FTE (ej. 50 h = 1 FTE) y factor de duración (ej. 50 min). Sin ellos, SIAASGN no calcula FTE.'),
    ('SIAFLRT', 'Regla de carga.', 'Activa; rangos inferior–superior de horas crédito, de contacto, de carga y FTE.'),
    ('grp', 'Por cada docente'),
    ('SPAIDEN', 'La persona debe existir.', 'Buscarla antes con GOAMTCH (ver tema 4).'),
    ('SIAINST', 'Activarlo como docente.', 'ID y periodo de vigencia; estatus, Docente/Asesor, categoría, tipo de personal, regla de carga, '
     'contrato (predefinido), escuela y departamento. Cambios: **Mantenimiento** desde el nuevo periodo.'),
    ('SSASECT, SIAFAVL', 'Asignarlo al NRC.', 'Sesión 01 (02, 03… si hay varios); ID o búsqueda en SIAFAVL; % de responsabilidad; '
     'un solo **principal**; sobrepaso solo por cruce de horario; % de sesión.'),
    ('SIAASGN', 'Revisar su carga.', 'NRC asignados y análisis: **O** = sobrecarga, **U** = subcarga. Reemplaza el control en Excel.'),
]

ADMISION = [
    ('grp', 'Configuración (una sola vez)'),
    ('STVADMT', 'Tipo de admisión.', 'Ej. DIRECTA.'),
    ('STVSTYP', 'Tipo de alumno.', 'Ej. N Nuevo. Queda en SGASTDN.'),
    ('STVAPDC', 'Decisión de admisión.', 'Solo una decisión con **aceptación** (de institución o de solicitante) crea al estudiante.'),
    ('STVRESD, STVAPST', 'Residencia y estatus de solicitud.', 'Requeridos. Estatus C (completa), D (decisión tomada) e I (incompleta).'),
    ('grp', 'Por cada participante'),
    ('SPAIDEN, GOAMTCH', 'Buscar antes de crear.', 'SPAIDEN (+) abre GOAMTCH con origen **PNATURAL**: apellidos, nombre y documento › Marcar-Duplicar › '
     'Seleccionar ID, Actualizar ID o Crear nuevo.'),
    ('SAAQUIK', 'Periodo y nivel.', 'ID de la persona, periodo (ej. 202654) y nivel › Ir.'),
    ('SAAQUIK', 'Datos del estudiante.', 'Tipo de alumno, estatus y residencia. **Crea el registro en SGASTDN.**'),
    ('SAAQUIK', 'Solicitud y decisión.', 'Marcar «Crear registro de solicitud»; tipo de admisión, estatus y decisión. **Crea la solicitud en SAAADMS.**'),
    ('SAAQUIK', 'Programa.', 'Trae la regla de currículo del programa. **Guardar.** Pestañas Dirección y Biográfica: se reflejan en SPAIDEN.'),
    ('SPAIDEN', 'Teléfono y correo.', 'Teléfono principal; correo **institucional** como Preferido.'),
    ('SAAADMS, SGASTDN', 'Verificar.', 'Solicitud con decisión, estudiante activo y programa correcto: listo para la inscripción (SFAREGS).'),
]

CUANDO = [
    ('Una sola vez', 'Tablas de validación', 'STVPTRM, STVACYR, STVTRMT, STVFCST, STVFSTP, STVFCNT, STVWKLD, STVADMT, STVSTYP, STVAPDC', '1 · 3 · 4'),
    ('Al abrir cada periodo', 'Periodo, calendario, feriados, factores y reglas de carga', 'STVTERM, SOATERM, SSAEXCL, SIATERM, SIAFLRT', '1 · 3'),
    ('Cada mes', 'NRC de la parte de periodo del mes y sus reglas', 'SSASECT, SSADETL, SSAPREQ, SSARRES', '2 · 2.1'),
    ('Por cada docente', 'Registro, asignación al NRC y control de carga', 'SPAIDEN, SIAINST, SSASECT, SIAASGN', '3'),
    ('Por cada participante', 'Persona, admisión y verificación', 'GOAMTCH, SAAQUIK, SPAIDEN, SAAADMS, SGASTDN', '4'),
    ('Al cerrar la inscripción', 'Cerrar los accesos web del periodo', 'SOATERM', '1'),
]

INDICE = [
    ('GOAMTCH', 'Coincidencia común', 'Buscar si la persona ya existe', '4'),
    ('GTVMTYP', 'Tipos de reunión', 'Categoría del horario (CLAS)', '2'),
    ('SAAADMS', 'Solicitud de admisión', 'Revisar o corregir la solicitud', '4'),
    ('SAAQUIK', 'Captura rápida', 'Admisión y estudiante en una sola página', '4'),
    ('SCACRSE', 'Catálogo de cursos', 'Curso base del NRC', '2'),
    ('SCADETL', 'Detalle de curso (catálogo)', 'Origen de correquisitos y atributos', '2.1'),
    ('SCAPREQ', 'Prerrequisitos (catálogo)', 'Origen de prerrequisitos', '2.1'),
    ('SCARRES', 'Restricciones (catálogo)', 'Origen de restricciones', '2.1'),
    ('SGASTDN', 'General de alumnos', 'Estatus, tipo y programa del estudiante', '4'),
    ('SIAASGN', 'Asignaciones del docente', 'Carga del docente y análisis O/U', '3'),
    ('SIAFAVL', 'Docentes disponibles', 'Buscar docente para el NRC', '3'),
    ('SIAFLRT', 'Reglas de carga del docente', 'Rangos de carga por periodo', '3'),
    ('SIAINST', 'Información del docente', 'Activar al docente desde un periodo', '3'),
    ('SIATERM', 'Periodo del docente', 'Factores FTE y de duración', '3'),
    ('SOATERM', 'Control de periodo', 'Calendario y reglas del periodo', '1'),
    ('SPAIDEN', 'Identificación de persona', 'Datos personales y de contacto', '3 · 4'),
    ('SSADETL', 'Detalle de sección', 'Correquisitos, ligas y atributos del NRC', '2.1'),
    ('SSAEXCL', 'Exclusión de horario (feriados)', 'Feriados', '1'),
    ('SSAPREQ', 'Prerrequisitos de sección', 'Prerrequisitos del NRC', '2.1'),
    ('SSARRES', 'Restricciones de sección', 'Quién puede inscribirse en el NRC', '2.1'),
    ('SSASECT', 'Sección (NRC)', 'Crear NRC, cupos, horario y docente', '2 · 3'),
    ('STVACYR', 'Años académicos', 'Años del periodo', '1'),
    ('STVADMT', 'Tipo de admisión', 'Tabla de validación', '4'),
    ('STVAPDC', 'Decisión de admisión', 'Qué hace cada decisión', '4'),
    ('STVAPST', 'Estatus de solicitud', 'Tabla de validación', '4'),
    ('STVFCNT', 'Tipo de contrato', 'Tabla de validación', '3'),
    ('STVFCST', 'Estatus del docente', 'Tabla de validación', '3'),
    ('STVFSTP', 'Tipo de personal', 'Tabla de validación', '3'),
    ('STVMEET', 'Horas de reunión', 'Módulos horarios predefinidos', '2'),
    ('STVPTRM', 'Partes de periodo', 'Tabla de validación', '1'),
    ('STVRESD', 'Residencia', 'Tabla de validación', '4'),
    ('STVSTYP', 'Tipo de alumno', 'Tabla de validación', '4'),
    ('STVTERM', 'Periodos', 'Crear el periodo', '1'),
    ('STVTRMT', 'Tipos de periodo', 'Tabla de validación', '1'),
    ('STVWKLD', 'Códigos de regla de carga', 'Tabla de validación', '3'),
]

CONFIRMAR = [
    ('Admisión en Centros Empresariales: ¿registro manual o como postulante (interfaz / CEPRE)?', 'Manual, con SAAQUIK'),
    ('¿Quién crea los NRC de Idiomas, Computación y Emprendimiento?', 'Las escuelas'),
    ('¿Quién asigna el docente al NRC y revisa su carga?', 'Registros Académicos'),
    ('Inscripción en NRC: no figura en el flujo. ¿Quién la hace?', 'Registros Académicos (SFAREGS)'),
    ('¿La tutoría aplica a Centros Empresariales?', 'Sí, con SGAADVR'),
    ('¿Qué aprueba o revisa la jefatura en el sistema?', 'Excepciones de inscripción (SFAROVR)'),
    ('¿El cobro de Finanzas se genera desde la inscripción?', 'Sí (TSAAREV)'),
]

SIGUIENTES = [
    ('5', 'Inscripción en NRC', 'SFAREGS, SFAROVR', 'Siguiente'),
    ('6', 'Tutoría', 'SIAINST, SGAADVR', 'Pendiente'),
    ('7', 'Jefatura', 'Por confirmar', 'Pendiente'),
    ('8', 'Docente: asistencia y calificaciones', 'Autoservicio del docente', 'Pendiente'),
    ('9', 'Finanzas', 'TSAAREV, TVACAJA', 'Pendiente'),
]


# ------------------------------------------------------------------ página
def build():
    b = []
    # Portada compacta
    b.append('<header class="cover">'
             '<div class="logos"><img src="uss.png" alt="USS"><img src="ellucian.png" alt="Ellucian"></div>'
             '<div class="band"><div class="kicker">Centros Empresariales · Idiomas, Computación (Informática) y Emprendimiento</div>'
             '<h1>Resumen de procesos en Banner</h1>'
             '<div class="sub">Temas 1 a 4: periodos, programación de asignaturas, docentes y admisión</div></div>'
             '<div class="meta">'
             f'<div><span>Elaborado por</span>{AUTHOR}</div>'
             '<div><span>Fecha</span>Septiembre 2026</div>'
             '<div><span>Fuentes</span>Resúmenes 1, 2, 2.1, 3 y 4 · Instructivos Ellucian</div>'
             '<div><span>Estado</span>Temas 1–4 listos · 5–9 pendientes</div>'
             '</div></header>')

    # 1. Panorama
    b.append(section(1, 'Panorama', 'Cada tema depende del anterior: sin periodo no hay NRC; sin NRC no hay docente ni inscripción.'))
    b.append('<div class="seq">' + '<i>›</i>'.join(
        f'<span class="{"next" if i == len(SEQ) - 1 else ""}">{s}</span>' for i, s in enumerate(SEQ)) + '</div>')
    rows = [[f'<span class="n">{n}</span>', f'<b>{html.escape(t)}</b>', fmt(q), chips(p), html.escape(r), html.escape(c)]
            for n, t, q, p, r, c in PANORAMA]
    b.append(table([('N°', 5), ('Tema', 17), ('¿Para qué?', 24), ('Páginas principales', 21), ('Responsable*', 16),
                    ('¿Cuándo?', 17)], rows, 'panorama'))
    b.append('<p class="foot">* Según el flujo institucional; pendiente de confirmación (sección 8).</p>')

    # 2. Datos de referencia
    b.append(section(2, 'Datos de referencia', 'Valores definidos para Centros Empresariales que se usan en todos los temas.'))
    per = table([('Posición', 22), ('Significa', 30), ('Valores', 48)], [
        ['<b>1–4</b>', 'Año', '2026'],
        ['<b>5</b>', 'Nivel académico', '<b>5</b> = Centros Empresariales'],
        ['<b>6</b>', 'Secuencia', '1 = Ciclo de verano<br>4 = Semestre I<br>6 = Semestre II'],
    ], 'mini')
    partes = table([('Centro', 30), ('General', 18), ('Grupos (uno por mes)', 52)], [
        ['<b>Idiomas</b>', '<span class="pg">IGE</span>', 'I01 … I12'],
        ['<b>Computación</b>', '<span class="pg">CGE</span>', 'X01 … X12'],
        ['<b>Emprendimiento</b>', '<span class="pg">EGE</span>', 'P01 … P12'],
    ], 'mini')
    b.append('<div class="grid2">'
             f'<div><h3>Código de periodo <span class="eg">ej. 202654 = 2026-I</span></h3>{per}</div>'
             f'<div><h3>Partes de periodo <span class="eg">+ parte 1 obligatoria</span></h3>{partes}</div></div>')
    otros = [
        ('Tipos de periodo', 'M mensual · B bimestral · T trimestral · C cuatrimestral · S semestral · A anual (STVTRMT)'),
        ('NRC', 'La secuencia inicia en **1000** (SOATERM). La sección es una letra (**A**) por ciclo y grupo.'),
        ('Tipo de horario', '**TEO**: calificable y con cobro. Otros tipos: dispensa de colegiatura.'),
        ('Carga docente', '1 FTE = ej. 50 horas; hora académica = ej. 50 min (SIATERM). Regla ej. **AP090** = 90 horas.'),
    ]
    b.append(table([('Dato', 20), ('Valor', 80)], [[f'<b>{fmt(k)}</b>', fmt(v)] for k, v in otros], 'kv'))

    # 3–6. Temas
    b.append(section(3, 'Tema 1 · Periodos académicos', 'Lo configura Registros Académicos antes de cualquier programación.'))
    b.append(steps(PERIODOS))
    b.append(section(4, 'Temas 2 y 2.1 · Programación de asignaturas', 'Cada NRC es una sección de un curso del catálogo en un periodo. Premisa: periodo configurado en SOATERM y curso creado en el catálogo (SCACRSE).'))
    b.append(steps(PROGRAMACION))
    b.append(note('**Recuerde:** el NRC copia las reglas del catálogo al crearse. Los cambios posteriores del catálogo no se aplican a los NRC ya creados.'))
    b.append(section(5, 'Tema 3 · Docentes', 'Registro del docente, asignación al NRC y carga de trabajo en el sistema (en lugar de Excel).'))
    b.append(steps(DOCENTES))
    b.append(section(6, 'Tema 4 · Admisión', 'Registro manual del participante: una sola página (SAAQUIK) crea la solicitud y el estudiante.'))
    b.append(steps(ADMISION))

    # 7. Cuándo
    b.append(section(7, '¿Cuándo se hace cada cosa?', 'Lista de control para el trabajo diario.'))
    rows = [[f'<b>{html.escape(m)}</b>', html.escape(q), chips(p), f'<span class="tag">{r}</span>'] for m, q, p, r in CUANDO]
    b.append(table([('Momento', 18), ('Qué se hace', 30), ('Páginas', 40), ('Tema', 12)], rows, 'when'))

    # 8. Pendientes
    b.append(section(8, 'Por confirmar y siguientes temas'))
    conf = table([('N°', 7), ('Punto a confirmar', 58), ('Propuesta', 35)],
                 [[f'<span class="n">{i}</span>', fmt(q), f'<b class="prop">{fmt(p)}</b>'] for i, (q, p) in enumerate(CONFIRMAR, 1)],
                 'confirm')
    sig = table([('N°', 12), ('Tema', 48), ('Páginas', 40)],
                [[f'<span class="n">{n}</span>',
                  f'<b>{html.escape(t)}</b>' + (' <span class="st sig">Siguiente</span>' if e == 'Siguiente' else ''),
                  chips(p) if re.fullmatch(r'[A-Z, ]+', p) else html.escape(p)] for n, t, p, e in SIGUIENTES], 'next')
    b.append(f'<div class="grid2 wide-left"><div><h3>Puntos a confirmar</h3>{conf}</div>'
             f'<div><h3>Siguientes temas</h3>{sig}</div></div>')

    # 9. Índice
    b.append(section(9, 'Índice de páginas de Banner', 'Orden alfabético. Tema = resumen donde se explica; el uso de cada página está en las secciones 3 a 6.'))
    half = (len(INDICE) + 1) // 2
    cols = [('Página', 25), ('Nombre', 62), ('Tema', 13)]
    parts = [table(cols, [[chips(c), f'<b>{html.escape(n)}</b>',
                           f'<span class="tag">{t}</span>'] for c, n, u, t in chunk], 'index')
             for chunk in (INDICE[:half], INDICE[half:])]
    b.append(f'<div class="grid2 index2"><div>{parts[0]}</div><div>{parts[1]}</div></div>')
    return '\n'.join(b)


CSS = open(os.path.join(HERE, 'resumen.css'), encoding='utf8').read()


def main():
    shutil.copy(os.path.join(MEDIA, 'image20.png'), os.path.join(HERE, 'uss.png'))
    shutil.copy(os.path.join(MEDIA, 'image23.png'), os.path.join(HERE, 'ellucian.png'))
    doc = (f'<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>Resumen de procesos en Banner</title>'
           f'<style>{CSS}</style></head><body>{build()}</body></html>')
    open(os.path.join(HERE, 'resumen.html'), 'w', encoding='utf8').write(doc)
    print('OK')


if __name__ == '__main__':
    main()
