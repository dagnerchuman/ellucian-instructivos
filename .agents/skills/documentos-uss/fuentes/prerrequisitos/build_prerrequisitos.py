# -*- coding: utf-8 -*-
"""«Prerrequisito y correquisito: lo resuelto» (PDF, 30/10/2026).

Resumen de las reuniones del 29/10/2026 con Ellucian (Nidia Beltrán, mañana; correo de Sandra Bolívar, tarde) y de
las pruebas en TEST del 28 al 30/10 (C156 a C170): cómo se amarran las acreditaciones de los tres centros a la
matrícula de pregrado. Usa el estilo de scripts/pdf/ejemplo_centros.py (tarjetas, tres centros, dudas al final y
glosario). Los datos salen del registro; no se agregan códigos de curso que no estén allí.

Uso: python3 build_prerrequisitos.py ["<salida>.pdf"]   (por defecto, en docs/capacitacion/)
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
import ejemplo_centros  # noqa: E402
from ejemplo_centros import CSS as CSS_EJEMPLO, bullets, ex, regla  # noqa: E402

NOMBRE = 'PRERREQUISITO Y CORREQUISITO - ACREDITACIONES EN PREGRADO - CENTROS EMPRESARIALES.pdf'
OUT = sys.argv[1] if len(sys.argv) > 1 else str(RAIZ / 'docs' / 'capacitacion' / NOMBRE)


def fmt(text):
    """fmt() de common más `código` en monoespaciado."""
    return re.sub(r'`([^`]+)`', r'<span class="code">\1</span>', _fmt(text))


ejemplo_centros.fmt = fmt   # bullets(), regla() y ex() del ejemplo también muestran `código` sin las comillas


# ------------------------------------------------------------------ 1. reuniones
REUNIONES = [
    ('Mañana · Nidia Beltrán (Ellucian)', 'C159 a C161', [
        'El **correquisito no sirve**: pregrado y centros van en periodos distintos.',
        '**La única forma es el prerrequisito restrictivo**, por programa de pregrado, en SCAPPRQ.',
        'Si solo se quiere que lo lleve, la regla va **sin calificación**: basta haberlo cursado.',
        'Configuró Medicina (`1PCSP15`): cada curso del ciclo pide su malla **Y** un Basic (I, II o III).',
    ]),
    ('Tarde · resumen de Sandra Bolívar (Ellucian)', 'C168', [
        'Prerrequisito **restrictivo** por ciclo: desde el **2.º** Idiomas, desde el **5.º** Computación y desde el **7.º** Emprendimiento.',
        'Ellucian **explorará** poner pregrado y centros en un mismo periodo o en partes de periodo para usar correquisitos.',
        'Matrícula como en pregrado: **primero paga** (o la primera cuota) **y luego se inscribe**.',
        'Pagos: contado con 5 % de descuento, 2 cuotas, pago al terminar con 5 % de recargo y regular en 3 cuotas.',
    ]),
]

# ------------------------------------------------------------------ 2. la decisión
CORREQUISITO = ('Correquisito: descartado',
                ['Los centros tienen **sus propios periodos**: 2026-0, 2026-I y 2026-II (en Banner, `202651`, `202654` y `202656`).'],
                ['El correquisito (SCADETL) obliga a llevar los dos cursos **en el mismo periodo**.',
                 'Pregrado termina en **44** (`202644`) y los centros en **54** (`202654`): nunca coinciden, así que no sirve.',
                 'Además es rígido: si desaprueba el curso del centro, tampoco puede llevar el de pregrado.',
                 'Ellucian explorará un mismo periodo o partes de periodo (C168). **Choca con el ADR-005**: lo decide la USS (U51).'],
                'Instructivo 1.1.5, diap. 8 y 21 · R22, R24 · C159, C168')

PRERREQUISITO = ('Prerrequisito restrictivo por programa: lo que rige',
                 ['Los cursos extracurriculares de los centros **se trabajan como prerrequisitos** (C159).',
                  'Idiomas, Computación y Emprendimiento son requisito para ser **egresado** (R08).'],
                 ['Se configura en **SCAPPRQ**: por programa de pregrado (Medicina `1PCSP15`) y por **versión de catálogo**.',
                  'A cada curso del ciclo se le suma el curso del centro: **malla Y ( Basic I O Basic II O Basic III )**.',
                  '**Sin calificación**, basta haberlo cursado; con calificación, hay que aprobarlo con esa nota.',
                  'Banner revisa la **historia académica**: no importa en qué periodo se llevó el curso del centro.'],
                 'Nidia Beltrán, 29/10 (C159 a C161, C168) · SCAPPRQ no está en los 83 instructivos; el más cercano es SCAPREQ (1.1.5)')

CADENA = [
    ('SCAPPRQ', 'regla por programa y versión'),
    ('SFAREGS', 'el alumno pide el curso'),
    ('Historia', 'Banner busca el curso del centro'),
    ('Resultado', 'se inscribe o sale error'),
]

# ------------------------------------------------------------------ 3. y, o, paréntesis
YO = [
    ('Y', 'Se exigen las dos filas.'),
    ('O', 'Basta una de las filas.'),
    ('( )', 'Agrupan filas: el conector de afuera vale para todo el grupo.'),
    ('1.ª fila', 'No lleva conector.'),
]
EJ_REGLA = [  # (texto, clase) para la figura de la regla de Anatomía I
    ('`ESEC 00055` (nota 11)', 'n'), ('Y', 'k'), ('(', 'k'), ('Basic I `02456`', 'p'), ('O', 'k'),
    ('Basic II `02457`', 'p'), ('O', 'k'), ('Basic III `02458`', 'p'), (')', 'k'),
]

# ------------------------------------------------------------------ 4. pruebas en TEST
PRUEBAS = [
    ('bad', 'No tiene el curso del centro', '«Prerequisite and Test Score error» (Error fatal): no se inscribe.', 'C163, C165'),
    ('bad', 'Lo está llevando en el centro', '«Prerequisite In Progress»: no se inscribe. Solo contaría si se marca «En progreso» en SOATERM.', 'C166, R10'),
    ('ok', 'Lo tiene en su historia', 'Basic I aprobado con 80 en 202646: **se inscribe**, aunque sea de otro periodo y otro nivel.', 'C170'),
    ('ok', 'Prueba de control', 'Sin la fila de Idiomas en SCAPPRQ, el mismo alumno **se inscribe**: el bloqueo venía de esa fila.', 'C167'),
    ('info', 'Qué versión aplica', 'La del **catálogo del alumno**, no la del periodo de matrícula. La regla de Nidia (202444) solo alcanza a los catálogos 2024.', 'C170, E32'),
    ('info', 'Dónde se ve el error', 'En SFAREGS, columna Mensaje. «Ver detalle de resultados» no dice qué curso falta y SSAPREQ del NRC queda vacío.', 'C163'),
]
RESTRICCION = ('Restricción por programa en el NRC (SSARRES)', [
    'Sirve para que un NRC del centro lo lleven **solo ciertos programas**, por ejemplo una ruta XP de Computación.',
    'Con la verificación de **Programa en Fatal** en SOATERM, quien no tiene el programa sale con «Program Restriction».',
    'También cuenta el currículo de **pregrado**: con Incluir `1PCSP15`, un alumno de Medicina entró al NRC del centro.',
], 'C156, C157 · R23, E29')

# ------------------------------------------------------------------ 5. ejemplos por centro
EJEMPLOS = [
    ('I-1', 'ing', 'Anatomía I en el 2.º ciclo de Medicina',
     'Regla de Nidia en SCAPPRQ: `ESEC 00055` **Y** ( Basic I **O** Basic II **O** Basic III ), sin calificación.',
     [('ell', 'Con el curso de la malla y un Basic en su historia, **se inscribe** (C170).'),
      ('ojo', 'Si está llevando el Basic en el periodo del centro, sale «Prerequisite In Progress» (C166).'),
      ('res', 'La regla tiene que estar en la versión del catálogo del alumno: hoy solo está en 202444 (C162, C170).')]),
    ('X-1', 'inf', 'Desde el 5.º ciclo (por confirmar)',
     'Según el resumen de Ellucian, desde el 5.º ciclo se exigirían cursos de Computación (C168).',
     [('ojo', 'La ruta es **3 cursos de 6** en cualquier orden (C125): no hay un único curso que pedir. Podría ir con «O» '
              'entre los cursos de la ruta o con el bloque de área de SCAPPRQ (E32).'),
      ('conf', 'Qué cursos y cuántos, y a qué cursos de pregrado se les pone (U49).')]),
    ('E-1', 'emp', 'Desde el 7.º ciclo (por confirmar)',
     'Según el resumen de Ellucian, desde el 7.º ciclo se exigirían cursos de Emprendimiento (C168).',
     [('ell', 'La misma regla: curso de la malla **Y** curso de Emprendimiento, en la versión del catálogo del alumno.'),
      ('conf', 'Qué curso de Emprendimiento y con qué nota (U49).')]),
]

# ------------------------------------------------------------------ 6. qué falta hacer
TAREAS = [
    ('Ellucian (Nidia)', 'Copiar la regla de la versión 202444 a las versiones **202544** y **202644**, para los catálogos 2025 y 2026 (C170).'),
    ('Registros', 'Decidir si se marca **«En progreso»** en el SOATERM de pregrado: vale para todos los prerrequisitos del periodo (C166).'),
    ('Registros', 'Agregar **DD** en SFARSTS a la parte 1 de 202744: sin DD, una matrícula de prueba no se puede dar de baja (C167).'),
    ('USS', 'Definir por centro el nivel, el curso, el ciclo y la nota que se exige (U49).'),
    ('USS', 'Decidir si se unifican los periodos de pregrado y centros (U51): hoy lo impide el ADR-005.'),
]

DUDAS_ELLUCIAN = [
    'Restricción por programa: ¿el currículo de pregrado sigue contando si el del centro está en **otro plan de estudios**? (E29)',
    '¿Conviene marcar **«En progreso»** en el periodo de pregrado? ¿Y qué pasa si después desaprueba el curso del centro? (E31)',
    'SCAPPRQ con **varias reglas** a la vez, la **calificación mínima** (75 en la captura) y el **bloque de área** para la ruta de Computación (E32).',
    '¿Banner soporta el **recargo del 5 %** al pagar al terminar? Si pregrado y centros comparten periodo, ¿cómo quedan las cuentas y los planes de pago? ¿El correquisito sirve entre **partes de periodo**? (E33)',
]
DUDAS_USS = [
    '¿Qué nivel de cada centro se exige, desde qué ciclo, a qué cursos de pregrado y con qué nota? (U49)',
    '¿Los centros matricularán como pregrado, **primero el pago y luego la inscripción**? Falta que Faber lo valide (U50).',
    '¿Se unifican los periodos para usar correquisitos? Habría que revisar el ADR-005, las partes de periodo y los planes de pago (U51).',
]


# ------------------------------------------------------------------ piezas
def reuniones():
    return explicar('<div class="pq-reu">' + ''.join(
        f'<div class="pq-rc"><div class="pq-rh"><b>{html.escape(t)}</b><span class="pq-ref">{html.escape(ref)}</span></div>'
        f'{bullets(items)}</div>' for t, ref, items in REUNIONES) + '</div>')


def cadena():
    return ('<div class="chain">' + ''.join(
        f'<div class="chev{" hi" if i == 0 else ""}"><b>{html.escape(t)}</b><span>{html.escape(q)}</span></div>'
        for i, (t, q) in enumerate(CADENA)) + '</div>')


def regla_yo():
    conectores = ''.join(f'<div class="pq-yo"><span class="pq-k">{html.escape(k)}</span><span>{html.escape(t)}</span></div>'
                         for k, t in YO)
    figura = '<div class="pq-fx">' + ''.join(f'<span class="pq-{c}">{fmt(t)}</span>' for t, c in EJ_REGLA) + '</div>'
    return explicar(
        '<div class="rule"><div class="rh"><span class="k">3</span>Cómo se lee la regla: Y, O y paréntesis</div>'
        f'<div class="blk ell"><div class="pq-yos">{conectores}</div>'
        '<div class="figcap">Ejemplo: Anatomía I (`ESEC 00017`) en la versión 202444</div>'.replace('`ESEC 00017`', '<span class="code">ESEC 00017</span>')
        + figura
        + '<p class="pq-nota">Se lee: debe tener Bioquímica <b>y</b> además <b>uno</b> de los tres Basic. Con «Y» en lugar de «O» '
          'tendría que haber llevado los tres.</p>'
          '<div class="src">Instructivo 1.1.5, diap. 18 y 19 · R25 · C161</div></div></div>')


def pruebas():
    tarjetas = ''.join(
        f'<div class="pq-tc {k}"><div class="pq-th"><b>{html.escape(t)}</b></div><div class="pq-tb">{fmt(d)}</div>'
        f'<div class="pq-src">{html.escape(ref)}</div></div>' for k, t, d, ref in PRUEBAS)
    return explicar(f'<div class="pq-tests">{tarjetas}</div>')


def restriccion():
    t, items, src = RESTRICCION
    return explicar(f'<div class="rule"><div class="rh"><span class="k">4</span>{html.escape(t)}</div>'
                    f'<div class="blk ell">{bullets(items)}<div class="src">{html.escape(src)}</div></div></div>')


def tareas():
    return explicar('<div class="pq-tasks">' + ''.join(
        f'<div class="pq-task"><span class="pq-who">{html.escape(q)}</span><div>{fmt(t)}</div></div>' for q, t in TAREAS) + '</div>')


def build():
    b = [header('Universidad Señor de Sipán · Centros Empresariales',
                'Prerrequisito y correquisito: lo resuelto',
                'Cómo se amarran las acreditaciones de Idiomas, Computación y Emprendimiento a la matrícula de pregrado. '
                'Reuniones con Ellucian del 29/10/2026 y pruebas en TEST',
                [('Elaborado por', AUTHOR), ('Fecha', '30 de octubre de 2026'),
                 ('Fuentes', 'Reuniones con Ellucian (29/10) · pruebas en TEST (C156 a C170) · instructivo 1.1.5'),
                 ('Estado', 'Probado en TEST; dudas al final')])]

    b.append(explicar(
        '<div class="lead"><b>La respuesta corta:</b> la acreditación se exige con un <b>prerrequisito restrictivo por programa</b> en '
        'SCAPPRQ. Si el alumno no tiene el curso del centro en su historia académica, Banner no lo deja inscribirse en el curso de '
        'pregrado. El <b>correquisito no sirve</b> mientras pregrado y centros tengan periodos distintos. Todo se probó en TEST; lo que '
        'falta decidir está al final.</div>'))

    b.append(section(1, 'Lo que se dijo en las reuniones del 29/10'))
    b.append(reuniones())

    b.append(section(2, 'Correquisito o prerrequisito'))
    b.append(regla(1, *CORREQUISITO))
    b.append(regla(2, *PRERREQUISITO))
    b.append('<div class="figcap">Cómo actúa en la matrícula</div>' + cadena())
    b.append(regla_yo())

    b.append(section(3, 'Lo probado en TEST', 'Alumnos de prueba de Medicina en el periodo 202744, del 28 al 30/10/2026.'))
    b.append(pruebas())
    b.append(restriccion())

    b.append(section(4, 'Ejemplos por centro'))
    for e in EJEMPLOS:
        b.append(ex(*e))

    b.append(section(5, 'Lo que falta hacer'))
    b.append(tareas())

    dudas = ('<div class="dudas"><div class="dc">' + explicar('<div class="dh">Para Ellucian</div><ol>'
             + ''.join(f'<li>{fmt(q)}</li>' for q in DUDAS_ELLUCIAN) + '</ol>') + '</div>'
             '<div class="dc uss">' + explicar(f'<div class="dh">Para la USS</div><ol start="{len(DUDAS_ELLUCIAN) + 1}">'
             + ''.join(f'<li>{fmt(q)}</li>' for q in DUDAS_USS) + '</ol>') + '</div></div>')

    b.append(section(6, 'Glosario', 'Qué significa cada palabra, sigla y página de Banner del documento.'))
    b.append('<div class="glos keep"><div class="gh">Palabras del tema</div><div class="gg">'
             '<div class="gi"><b>Prerrequisito</b><span>Curso que el alumno debe tener en su historia antes de inscribirse en otro.</span></div>'
             '<div class="gi"><b>Correquisito</b><span>Curso que se lleva en el mismo periodo que otro.</span></div>'
             '<div class="gi"><b>Restrictivo</b><span>Si no se cumple, Banner no deja inscribir (error fatal).</span></div>'
             '<div class="gi"><b>Versión</b><span>Regla de SCAPPRQ con su periodo de inicio; rige la del catálogo del alumno.</span></div>'
             '<div class="gi"><b>Catálogo</b><span>Periodo de catálogo del currículo del alumno (por ejemplo, 202444): fija qué versión le aplica.</span></div>'
             '<div class="gi"><b>En progreso</b><span>Casilla de SOATERM: un curso que está llevando cuenta como cumplido.</span></div>'
             '<div class="gi"><b>RE · DD</b><span>Inscrito · retirado (libera el cupo).</span></div>'
             '<div class="gi"><b>C## · E## · U##</b><span>Confirmado · duda para Ellucian · duda para la USS, en el registro.</span></div>'
             '</div></div>' + glosario_html(extra=('SSARRES',)))
    b.append(section(7, 'Dudas para confirmar'))
    b.append(dudas)
    return '\n'.join(b)


CSS = CSS_EJEMPLO + '''
.chain { margin: 2px 0 10px; }
.chev { padding: 7px 6px 7px 16px; }
.chev.hi { background: var(--p); color: #fff; }
.chev b { font-size: 8.4pt; } .chev span { font-size: 7.2pt; }
.rule .blk.ell { font-size: 8.8pt; }

/* reuniones */
.pq-reu { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 0 0 10px; break-inside: avoid; }
.pq-rc { border: 1px solid var(--line); border-radius: 10px; overflow: hidden; background: #fff; }
.pq-rh { display: flex; align-items: center; gap: 8px; padding: 6px 11px; background: var(--pl); border-bottom: 1px solid var(--pb); }
.pq-rh b { font-family: 'Montserrat', sans-serif; font-size: 9.2pt; flex: 1; }
.pq-ref { font-size: 7.4pt; font-weight: 700; color: var(--pd); background: #fff; border: 1px solid var(--pb); border-radius: 9px; padding: 0 7px; }
.pq-rc ul { margin: 6px 12px 7px 26px; padding: 0; font-size: 8.6pt; line-height: 1.45; } .pq-rc li { margin: 0 0 3px; }

/* y, o y paréntesis */
.pq-yos { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin: 0 0 8px; }
.pq-yo { border: 1px solid var(--line); border-radius: 8px; padding: 5px 8px; font-size: 8.2pt; line-height: 1.38; }
.pq-k { display: block; font-family: 'Montserrat', sans-serif; font-weight: 700; color: var(--pd); font-size: 10pt; }
.pq-fx { display: flex; flex-wrap: wrap; align-items: center; gap: 4px; margin: 0 0 4px; }
.pq-fx > span { border-radius: 6px; padding: 2px 7px; font-size: 8.4pt; }
.pq-n { background: var(--soft); } .pq-p { background: var(--pl); color: var(--pd); font-weight: 600; }
.pq-fx .pq-k { display: inline; background: var(--p); color: #fff; font-size: 8.2pt; padding: 2px 6px; }
.pq-nota { margin: 4px 0 2px; font-size: 8.3pt; line-height: 1.42; }

/* pruebas */
.pq-tests { display: grid; grid-template-columns: repeat(3, 1fr); gap: 7px; margin: 0 0 10px; }
.pq-tc { border: 1px solid var(--line); border-top: 4px solid var(--p); border-radius: 9px; background: #fff; display: flex;
         flex-direction: column; break-inside: avoid; }
.pq-tc.ok { border-top-color: var(--g); } .pq-tc.bad { border-top-color: #C62828; }
.pq-th { padding: 6px 10px 2px; font-family: 'Montserrat', sans-serif; font-size: 9pt; }
.pq-tb { padding: 2px 10px 6px; font-size: 8.3pt; line-height: 1.42; flex: 1; }
.pq-src { padding: 3px 10px 5px; font-size: 7.2pt; color: var(--mut); border-top: 1px solid var(--line); background: var(--pz); }

/* tareas */
.pq-tasks { border: 1px solid var(--line); border-radius: 10px; overflow: hidden; margin: 0 0 10px; break-inside: avoid; background: #fff; }
.pq-task { display: grid; grid-template-columns: 112px 1fr; align-items: baseline; gap: 8px; padding: 6px 12px; border-top: 1px solid var(--line);
           font-size: 8.7pt; line-height: 1.45; }
.pq-task:first-child { border-top: 0; }
.pq-who { font-size: 7.6pt; font-weight: 700; color: var(--pd); background: var(--pl); border-radius: 9px; padding: 1px 8px; text-align: center; }
.ex .r, .ex .case { grid-template-columns: 108px 1fr; }
.ex.emp { border-left-color: var(--emp); } .ex.emp .exn { background: var(--emp); }
.ex.emp .ctr { background: var(--empl); color: var(--emp); }
'''


if __name__ == '__main__':
    p = render('prerrequisitos', build(), CSS, 'Prerrequisito y correquisito: lo resuelto · Centros Empresariales', OUT,
               'Prerrequisito y correquisito: lo resuelto - Centros Empresariales',
               'Cómo se amarran las acreditaciones de los centros a la matrícula de pregrado: reuniones con Ellucian y pruebas en TEST')
    check_pdf(p, png_dir=os.environ.get('PNG_DIR'))
