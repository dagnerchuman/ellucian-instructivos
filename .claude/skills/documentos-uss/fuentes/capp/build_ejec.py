# -*- coding: utf-8 -*-
"""Migración R2: lo que entiendo. Resumen ejecutivo para ponerse al día (Centros Empresariales)."""
import html
import os

from common import AUTHOR, HERE, chips, fmt, header, render, section, table

OUT = os.path.join(HERE, '..', 'entregables', 'MIGRACIÓN R2 - LO QUE ENTIENDO - CENTROS EMPRESARIALES.pdf')

IDEAS = [
    ('Qué pasa', 'Ellucian y la USS están pasando los datos del sistema anterior a Banner por etapas (**Migración R2**): '
                 'primero personas y docentes en **PROD**; luego, en **TEST**, estudiantes, historia, egresados, saldos, tesis y escuela de procedencia.'),
    ('Qué hace la USS', 'Después de cada carga, la USS **revisa directamente en Banner Student** una muestra de casos, registra cada error '
                        'en un **Issue log** y consolida todo en una **planilla Excel**.'),
    ('Cuándo está bien', 'Cuando el **% de correctitud** supera los umbrales de Ellucian (98% a 99,5% según el criterio) y cada excepción '
                         'está documentada, justificada y aprobada por el **comité**.'),
    ('Por qué CAPP', 'Es la prueba más exigente: demuestra que la historia migrada, la malla del estudiante y las reglas del plan dan el '
                     '**mismo avance académico** que en el sistema anterior, y de eso depende la **inscripción** (proyección).'),
]

CRONO = [
    ('Personas', 'PROD', '24/09 – 27/09', 'now'),
    ('Documento de identidad · Contacto de emergencia', 'PROD', '25/09 – 27/09', 'now'),
    ('Docentes', 'PROD', '30/09 – 02/10', 'soon'),
    ('Carga LD01 con equivalencias · Matriz de seguridad', 'PROD', '30/09 – 02/10 (carga)', 'soon'),
    ('Clonación a TEST', '—', '05/10 – 09/10', 'soon'),
    ('Estudiantes', 'TEST', '16/10 – 21/10', 'soon'),
    ('Historia académica (incluye CAPP y proyección)', 'TEST', '28/10 – 30/10', 'crit'),
    ('Egresados', 'TEST', '02/11 – 04/11', 'soon'),
    ('Saldos', 'TEST', '06/11 – 13/11', 'soon'),
    ('Tesis · Escuela de procedencia', 'TEST', '10/11 – 16/11', 'soon'),
    ('Pruebas integrales', 'TEST', '16/11 – 26/12', 'soon'),
]

TOCA = [
    ('Asegurar que la muestra incluya participantes de los **3 centros** (propuesta: 16 por centro).', 'Excel · Cronograma'),
    ('Revisar en Banner Student y registrar cada dato revisado en la planilla.', 'Excel · Revisión'),
    ('Registrar cada error con su captura de pantalla.', 'Excel · Issue log'),
    ('Calcular el % de correctitud por criterio para el comité.', 'Excel · Resumen'),
    ('Preparar la revisión de **Historia académica**: CAPP y proyección (unas 34 horas en 3 días; al menos 2 revisores).', 'PDF · CAPP explicado'),
    ('Resolver los puntos abiertos con Ellucian (preguntas de la sección 5).', 'Este documento'),
]

CRITERIOS = [('Integridad', 'Obligatorios completos', '99%'), ('Exactitud', 'Igual al origen', '98%'),
             ('Consistencia', 'Coherente entre módulos', '98%'), ('Validez', 'Formatos y códigos válidos', '99%'),
             ('Unicidad', 'Sin duplicados', '99,5%'), ('Integridad referencial', 'Relaciones y totales cuadran', '99%')]

PREGUNTAS = [
    ('CAPP', '¿Los programas de Idiomas, Computación y Emprendimiento tienen sus reglas en CAPP (SMAPROG, SMAAREA)? '
             'Si no, ¿cómo funcionará la inscripción proyectada para los centros?'),
    ('Historia', '¿Se migra la historia de los centros? ¿A qué periodos de Banner van los cursos llevados en periodos de 3 meses?'),
    ('Equivalencias', '¿Qué incluye la «Carga LD01 con equivalencias»? ¿Contempla cursos de los centros?'),
    ('Muestra', '¿La muestra de validación incluye participantes de los centros? ¿Cuántos y quién los elige?'),
    ('Accesos', '¿Quién ejecuta SMARQCM y SFPPROJ en TEST: Ellucian o la USS? ¿Tenemos accesos a esas páginas?'),
    ('Egresados', '¿El certificado de los centros se registra como grado (SHADEGR)?'),
    ('Issue log', '¿Cuándo se define en conjunto el formato del Issue log? ¿Sirve la propuesta de la planilla?'),
    ('Totales', '¿Insight puede dar los totales separados por centro para conciliar con el sistema anterior?'),
]

DOCS = [
    ('0. Flujo general', 'Etapas, responsables y puntos a confirmar.'),
    ('Temas 1, 2, 2.1, 3 y 4', 'Periodos, programación de NRC, reglas del NRC, docentes y admisión (presentaciones).'),
    ('Resumen de procesos (temas 1 a 4)', 'Todo en tablas: pasos, páginas, cuándo se hace e índice de páginas.'),
    ('Periodo académico: antes y después', 'Periodo de 3 meses frente a periodos y partes de periodo en Banner.'),
    ('Validación de la migración', 'Estrategia de Ellucian aplicada a los centros, criterios, tiempos y cronograma.'),
    ('Planilla de revisión (Excel)', 'Revisión, Issue log, % de correctitud, cronograma y tiempos.'),
    ('CAPP explicado', 'Qué es, cómo se ejecuta y cómo se valida.'),
]


def build():
    b = [header('Universidad Señor de Sipán · Centros Empresariales', 'Migración R2: lo que entiendo',
                'Resumen para ponerse al día, con lo que toca a Centros Empresariales y las preguntas para Ellucian',
                [('Elaborado por', AUTHOR), ('Fecha', '25 de septiembre de 2026'),
                 ('Fuentes', 'Presentación de Ellucian en Zoom (diap. 3 a 12) e instructivos'), ('Estado', 'Borrador para validar')])]

    b.append(section(1, 'Lo esencial en cuatro ideas'))
    b.append('<div class="ideas">' + ''.join(
        f'<div class="idea"><span class="k">{i}</span><div class="t">{html.escape(t)}</div><p>{fmt(x)}</p></div>'
        for i, (t, x) in enumerate(IDEAS, 1)) + '</div>')

    b.append(section(2, 'Dónde estamos', 'Revisiones de la USS según el cronograma de Ellucian, al 25/09/2026.'))
    lab = {'now': '<span class="ap now">En revisión</span>', 'soon': '<span class="ap soon">Próxima</span>',
           'crit': '<span class="ap bad">Punto crítico</span>'}
    rows = [[f'<b>{html.escape(e)}</b>', a, f, lab[s]] for e, a, f, s in CRONO]
    b.append(table([('Etapa', 50), ('Ambiente', 12), ('Revisión (USS)', 22), ('Estado', 16)], rows, 'crono'))

    b.append(section(3, 'Qué le toca a Centros Empresariales'))
    rows = [[f'<span class="n">{i}</span>', fmt(t), f'<span class="tool">{h}</span>'] for i, (t, h) in enumerate(TOCA, 1)]
    b.append(table([('N°', 5), ('Tarea', 73), ('Herramienta', 22)], rows, 'toca'))

    b.append(section(4, 'Cómo se decide si la migración está bien'))
    rows = [[f'<b>{c}</b>', d, f'<b class="umb">{u}</b>'] for c, d, u in CRITERIOS]
    crit = table([('Criterio', 36), ('En pocas palabras', 44), ('Mínimo', 20)], rows, 'crit')
    b.append('<div class="grid2 dec"><div>' + crit + '</div><div class="side">'
             '<div class="formula"><div class="fl">% de correctitud</div><div class="fx"><span>datos conformes</span><i></i>'
             '<span>datos revisados</span></div></div>'
             '<div class="note">Con muestras pequeñas casi no hay margen: con 48 participantes, <b>Unicidad</b> exige '
             '<b>cero duplicados</b>. Los datos «Observado» solo cuentan como correctos cuando el comité aprueba la excepción.</div>'
             '</div></div>')

    b.append(section(5, 'Preguntas para el Zoom', 'En orden de prioridad para Centros Empresariales.'))
    rows = [[f'<span class="n">{i}</span>', f'<b>{t}</b>', fmt(q)] for i, (t, q) in enumerate(PREGUNTAS, 1)]
    b.append(table([('N°', 5), ('Tema', 15), ('Pregunta', 80)], rows, 'preg'))

    b.append(section(6, 'Material preparado hasta hoy'))
    rows = [[f'<b>{html.escape(d)}</b>', fmt(u)] for d, u in DOCS]
    b.append(table([('Documento', 34), ('Para qué sirve', 66)], rows, 'docs'))
    b.append('<p class="foot">Este resumen refleja lo entendido de la presentación de Ellucian y los instructivos; se actualizará con el resumen del Zoom.</p>')
    return '\n'.join(b)


CSS = '''
.ideas { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; break-inside: avoid; }
.idea { border: 1px solid var(--line); border-radius: 9px; padding: 8px 11px 9px; background: #fff; border-top: 4px solid var(--p); }
.idea:nth-child(4) { border-top-color: var(--lime); background: var(--gl); }
.idea .k { display: inline-block; width: 17px; height: 17px; border-radius: 9px; background: var(--p); color: #fff; font-weight: 700;
           font-size: 7.6pt; line-height: 17px; text-align: center; margin-right: 6px; vertical-align: 1px; }
.idea .t { display: inline; font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 9pt; }
.idea p { margin: 5px 0 0; font-size: 8.5pt; line-height: 1.45; color: #2E2E36; }
table.crono td:first-child, table.crono th:first-child, table.crit td:first-child, table.crit th:first-child,
table.docs td:first-child, table.docs th:first-child { text-align: left; }
table.crono td:nth-child(n+2), table.crono th:nth-child(n+2), table.crit td:nth-child(3), table.crit th:nth-child(3),
table.toca td:last-child, table.toca th:last-child { text-align: center; }
.tool { display: inline-block; font-weight: 700; font-size: 7.6pt; color: var(--gd); background: var(--gl); border-radius: 5px; padding: 1px 6px; }
.umb { color: var(--pd); }
.grid2.dec { grid-template-columns: 1.2fr 1fr; align-items: start; }
.side { display: grid; gap: 8px; }
.side .note { margin: 0; }
.formula { border: 1px solid var(--pb); background: var(--pl); border-radius: 8px; padding: 8px 12px; }
.formula .fl { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 8.4pt; color: var(--pd); }
.formula .fx { display: flex; flex-direction: column; align-items: center; margin: 5px 0 2px; font-weight: 700; font-size: 8.6pt; }
.formula .fx i { display: block; width: 60%; height: 1.5px; background: var(--ink); margin: 3px 0; }
'''


if __name__ == '__main__':
    p = render('ejec', build(), CSS, 'Migración R2: lo que entiendo · Centros Empresariales', OUT,
               'Migración R2: lo que entiendo - Centros Empresariales', 'Resumen ejecutivo de la migración R2 y su validación')
    print('OK', p)
