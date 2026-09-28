# -*- coding: utf-8 -*-
"""CAPP explicado: qué es, cómo se ejecuta y por qué importa en la validación de la migración."""
import html
import os

from common import AUTHOR, HERE, chips, fmt, header, render, section, table

OUT = os.path.join(HERE, '..', 'entregables', 'CAPP EXPLICADO - CENTROS EMPRESARIALES.pdf')

ENTRADAS = [
    ('Historia académica', 'SHACRSE', 'Cursos aprobados, notas y créditos; también cursos en progreso, transferencias y equivalencias.'),
    ('El estudiante y su plan', 'SGASTDN', 'Programa y periodo de catálogo: indica qué versión de la malla le corresponde.'),
    ('Reglas del plan (malla)', 'SMAPROG, SMAAREA', 'Programa › áreas › reglas: qué cursos o créditos exige cada área.'),
]
CADENA = [
    ('Evaluar cumplimiento', 'SMARQCM', 'Individual. Masivo: SMRBCMP.'),
    ('Ver el resultado', 'SMICRLT', 'Cumple / No cumple por programa, área y regla.'),
    ('Proyectar cursos', 'SFPPROJ, SFAPROJ', 'Lista de cursos que le faltan y puede llevar.'),
    ('Inscribir', 'SFAREGS', 'Con «Restringir a cursos proyectados», solo lo proyectado.'),
]

EJEMPLO = [
    ('Nivel básico', 'BASIC I', 'Aprobado en 202651', 'ok'),
    ('Nivel básico', 'BASIC II', 'Aprobado en 202654', 'ok'),
    ('Nivel básico', 'BASIC III', 'Sin registro', 'no'),
    ('Nivel intermedio', 'INTERMEDIATE I – III', 'Sin registro', 'no'),
]

PASOS = [
    ('SMARQCM', 'Ingrese el **ID** del estudiante y presione Ir. Si tiene retenciones y debe sobrepasarlas, active la casilla.'),
    ('SMARQCM', 'Cree una **nueva solicitud** con «+». Toma los parámetros predefinidos **ONLINE** (SMADFLT).'),
    ('SMARQCM', '**Herramientas › Copiar desde registro de alumno**, elija su programa, presione Seleccionar y **guarde**.'),
    ('SMARQCM', '**Herramientas › Enviar para procesamiento**. Banner genera el **N° de solicitud**.'),
    ('SMICRLT', 'Menú relacionado › **Desplegar resultados de cumplimiento**: se abre con el ID y la solicitud.'),
    ('SMICRLT', 'Revise **programa y periodo de catálogo**, las columnas **Cumple / No cumple**, las áreas y reglas, y los cursos **usados** y **no usados**.'),
    ('SFPPROJ', 'Proyección (proceso desde GJAPCTL, impresora DATABASE). Necesita una ejecución de CAPP en el periodo.'),
    ('SFAPROJ', 'Con ID y periodo, vea los **cursos proyectados**. Se pueden ajustar con «+» y «–».'),
]

PREVIOS = [
    ('SGASTDN', 'La persona debe estar registrada como estudiante.'),
    ('SMAPROG', 'Programa activo, con áreas; para proyectar: modelo de inscripción «proyectada» y áreas con prioridad.'),
    ('SMAAREA', 'Áreas activas con sus reglas.'),
    ('STVCPRT, SMACPRT', 'Tipo de cumplimiento y sus reglas de impresión.'),
    ('SMADFLT', 'Parámetros predefinidos: ONLINE (individual) y BATCH (masivo).'),
    ('SHAGPAR', 'Reglas de despliegue del PGA (al menos para el periodo 000000).'),
    ('SFALPROJ', 'Por programa: cuántas áreas y créditos se proyectan.'),
]

CAUSAS = [
    ('Un curso aprobado aparece pendiente', 'El curso o la nota no se migraron, o el código cambió y no hay equivalencia.', 'SHACRSE, SMICRLT'),
    ('El curso figura en «no usados»', 'No pertenece a la malla del periodo de catálogo asignado (versión equivocada).', 'SGASTDN, SMAAREA'),
    ('El programa sale sin requisitos (íconos en gris)', 'El programa no tiene reglas CAPP configuradas.', 'SMAPROG'),
    ('Créditos o PGA distintos', 'Créditos o notas migrados diferentes, o reglas de PGA.', 'SHACRSE, SHATERM, SHAGPAR'),
    ('Proyección vacía o equivocada', 'Falta el CAPP del periodo, la prioridad de áreas o la configuración por programa.', 'SFAPROJ, SMAPROG, SFALPROJ'),
    ('Con dos programas evalúa solo uno', 'El currículo secundario (programas concurrentes) no está habilitado.', 'SGASTDN, SMAWCRL'),
]

GLOSARIO = [
    ('CAPP', 'Curriculum, Advising and Program Planning: el módulo de avance curricular de Banner.'),
    ('Evaluación de cumplimiento', 'Ejecución del CAPP para un estudiante; cada una genera un N° de solicitud.'),
    ('Área / regla', 'Bloques de la malla (ej. nivel básico) y lo que exige cada uno (cursos, créditos, atributos).'),
    ('Periodo de catálogo', 'Define qué versión de la malla se aplica al estudiante.'),
    ('Plan de equivalencia', 'Qué curso antiguo cuenta como qué curso nuevo cuando cambió la malla.'),
    ('Cursos usados / no usados', 'Los que cuentan para algún requisito y los que no encajan en la malla.'),
    ('Proyección', 'Lista de cursos pendientes que el estudiante puede inscribir en el periodo.'),
    ('PGA', 'Promedio ponderado, por periodo y acumulado.'),
    ('ONLINE / BATCH', 'Parámetros para la ejecución individual (SMARQCM) o masiva (SMRBCMP).'),
]


def build():
    b = [header('Universidad Señor de Sipán · Centros Empresariales', 'CAPP explicado',
                'Qué es, cómo se ejecuta y por qué es clave para validar la migración',
                [('Elaborado por', AUTHOR), ('Fecha', 'Septiembre 2026'),
                 ('Fuentes', 'Instructivos 7.2.4 CAPP y 5.4 Proyección · Estrategia de validación'),
                 ('Nivel', 'Para ponerse al día')])]

    b.append(section(1, 'En una frase'))
    b.append('<div class="lead"><b>CAPP es el auditor del plan de estudios en Banner.</b> Compara lo que el estudiante ya aprobó '
             '(su historia académica) con lo que exige su malla y dice <b>qué cumplió y qué le falta</b>. Banner lo usa en la '
             '<b>inscripción</b> (proyección de cursos), el cierre de periodo, la graduación y el ajuste de historia académica.</div>')

    b.append(section(2, 'Cómo funciona', 'Tres entradas, una evaluación y dos usos directos: la proyección y la inscripción.'))
    ins = ''.join(f'<div class="in"><div class="t">{html.escape(t)}</div>{chips(c)}<p>{fmt(d)}</p></div>' for t, c, d in ENTRADAS)
    cad = '<i class="ar">›</i>'.join(
        f'<div class="stp"><span class="k">{i}</span><div class="t">{html.escape(t)}</div>{chips(c)}<p>{fmt(d)}</p></div>'
        for i, (t, c, d) in enumerate(CADENA, 1))
    b.append(f'<div class="flow"><div class="ins">{ins}</div><div class="brace">›</div><div class="chain">{cad}</div></div>')

    b.append(section(3, 'Ejemplo en Centros Empresariales', 'Ilustrativo: depende de cómo estén configuradas en CAPP las reglas del programa de Idiomas.'))
    rows = [[f'<b>{a}</b>', c, h, '<span class="ap ok">Cumple</span>' if r == 'ok' else '<span class="ap bad">No cumple</span>']
            for a, c, h, r in EJEMPLO]
    ex = table([('Área', 26), ('Curso', 28), ('Historia académica', 26), ('CAPP', 20)], rows, 'ex')
    b.append('<div class="grid2 exg"><div>' + ex + '</div><div class="res">'
             '<div class="rr"><span class="k">Proyección</span><b>BASIC III</b></div>'
             '<div class="rr"><span class="k">Inscripción</span>Solo puede inscribirse en un NRC de <b>BASIC III</b> del grupo del mes.</div>'
             '<div class="rr"><span class="k">Si migró mal</span>Si BASIC II no llegó a la historia, CAPP lo marca pendiente, lo proyecta otra vez '
             'y el participante <b>no podrá avanzar</b>.</div></div></div>')

    b.append(section(4, 'Cómo se ejecuta', 'Procedimiento del instructivo 7.2.4 (individual) y del 5.4 (proyección).'))
    rows = [[f'<span class="n">{i}</span>', chips(p), fmt(t)] for i, (p, t) in enumerate(PASOS, 1)]
    b.append(table([('N°', 5), ('Página', 13), ('Qué hacer', 82)], rows, 'pasos'))
    b.append('<p class="foot">Masivo: SMRBCMP desde GJAPCTL (impresora DATABASE); el resultado se revisa en GJIREVO (archivo .lis).</p>')
    b.append('<h3 class="h3gap">Configuración previa <span class="eg">la hace el equipo funcional; si falta, CAPP no funciona</span></h3>')
    rows = [[chips(p), fmt(t)] for p, t in PREVIOS]
    b.append(table([('Página', 22), ('Qué debe estar listo', 78)], rows, 'prev'))

    b.append(section(5, 'CAPP en la validación de la migración',
                     'Si CAPP da el mismo resultado que el sistema anterior, la historia, la malla y las reglas migraron bien. '
                     'Se valida en TEST, en la etapa de Historia académica (revisión del 28 al 30 de octubre).'))
    steps = [('Elegir la muestra', 'Distintos niveles, programas y versiones de malla.'),
             ('Ejecutar CAPP', 'SMARQCM a cada estudiante de la muestra (3 min).'),
             ('Comparar el resultado', 'SMICRLT contra la situación en el sistema anterior (10 min).'),
             ('Proyectar', 'SFPPROJ (3 min) y revisar en SFAPROJ que ofrezca lo correcto (10 min).'),
             ('Registrar', 'Conforme u observación en la planilla; si difiere, al Issue log.')]
    b.append('<div class="steps5">' + '<i>›</i>'.join(
        f'<div><b>{i}</b><div class="t">{html.escape(t)}</div><p>{fmt(d)}</p></div>' for i, (t, d) in enumerate(steps, 1)) + '</div>')
    b.append('<p class="foot">Son 26 de los 42 minutos que Ellucian estima para revisar la historia académica de cada estudiante.</p>')
    b.append('<h3 class="h3gap">Si el resultado no coincide: causas probables</h3>')
    rows = [[f'<b>{html.escape(s)}</b>', fmt(c), chips(p)] for s, c, p in CAUSAS]
    b.append(table([('Lo que se ve', 30), ('Causa probable', 44), ('Dónde revisar', 26)], rows, 'causas'))

    b.append(section(6, 'Glosario para el Zoom'))
    half = (len(GLOSARIO) + 1) // 2
    parts = [table([('Término', 34), ('Significa', 66)], [[f'<b>{html.escape(t)}</b>', fmt(d)] for t, d in chunk], 'glo')
             for chunk in (GLOSARIO[:half], GLOSARIO[half:])]
    b.append(f'<div class="grid2">{parts[0]}{parts[1]}</div>')
    return '\n'.join(b)


CSS = '''
.flow { display: grid; grid-template-columns: 1fr 16px 2.25fr; gap: 6px; align-items: stretch; margin: 2px 0 6px; break-inside: avoid; }
.ins { display: grid; gap: 6px; }
.in { border: 1px solid var(--line); border-left: 4px solid var(--lime); border-radius: 8px; padding: 6px 9px; background: #fff; }
.in .t, .stp .t { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 8.3pt; margin-bottom: 2px; }
.in p, .stp p { margin: 3px 0 0; font-size: 7.8pt; color: #3A3A44; line-height: 1.35; }
.brace { align-self: center; text-align: center; color: var(--g); font-weight: 800; font-size: 20pt; }
.chain { display: flex; align-items: stretch; gap: 3px; }
.stp { flex: 1; border-radius: 9px; background: var(--pl); border: 1px solid var(--pb); padding: 7px 8px; position: relative; }
.stp .k { display: inline-block; width: 16px; height: 16px; border-radius: 8px; background: var(--p); color: #fff; font-weight: 700;
         font-size: 7.4pt; line-height: 16px; text-align: center; margin-bottom: 3px; }
.chain .ar { align-self: center; color: var(--g); font-style: normal; font-weight: 800; font-size: 12pt; }
.grid2.exg { grid-template-columns: 1.35fr 1fr; align-items: start; }
table.ex td:nth-child(4), table.ex th:nth-child(4) { text-align: center; }
table.ex td:first-child, table.ex th:first-child { text-align: left; }
.res { display: grid; gap: 6px; }
.rr { border: 1px solid var(--line); border-radius: 8px; padding: 6px 10px; font-size: 8.4pt; line-height: 1.4; background: #fff; }
.rr:nth-child(3) { background: #FFF8E8; border-color: #F2DDA4; }
.rr .k { display: block; font-size: 7pt; font-weight: 700; color: var(--mut); text-transform: uppercase; letter-spacing: .07em; margin-bottom: 1px; }
table.prev td:first-child, table.prev th:first-child, table.glo td:first-child, table.glo th:first-child,
table.causas td:first-child, table.causas th:first-child { text-align: left; }
.steps5 { display: flex; gap: 4px; align-items: stretch; margin: 2px 0 2px; break-inside: avoid; }
.steps5 > div { flex: 1; background: var(--p); color: #fff; border-radius: 8px; padding: 6px 8px; }
.steps5 > div b { display: inline-block; width: 16px; height: 16px; border-radius: 8px; background: #fff; color: var(--pd);
                  font-size: 7.4pt; line-height: 16px; text-align: center; }
.steps5 .t { font-weight: 700; font-size: 8.2pt; margin: 3px 0 2px; }
.steps5 p { margin: 0; font-size: 7.6pt; line-height: 1.35; color: #F1E7FA; }
.steps5 p .code { color: #fff; }
.steps5 > i { align-self: center; color: var(--g); font-style: normal; font-weight: 800; font-size: 12pt; }
'''


if __name__ == '__main__':
    p = render('capp', build(), CSS, 'CAPP explicado · Centros Empresariales', OUT,
               'CAPP explicado - Centros Empresariales', 'Qué es CAPP, cómo se ejecuta y su rol en la validación de la migración')
    print('OK', p)
