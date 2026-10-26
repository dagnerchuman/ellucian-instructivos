# -*- coding: utf-8 -*-
"""Afiche de una hoja: los términos de Banner en el orden del flujo de los Centros Empresariales.

Uso: python3 build_afiche.py "/ruta/TÉRMINOS DE BANNER - AFICHE PARA ESTUDIAR - CENTROS EMPRESARIALES.pdf"
Fuentes: TERMINOS de herramientas/diagramas/plantillas.py, glosario (references/ref-glosario.md),
centros/<centro>/datos.json y lo validado en TEST (registro C65, C91, C95, C97, C100, C101, C105, C107).
"""
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', 'scripts', 'pdf'))
from common import AUTHOR, _url, check_pdf, fmt, render, table  # noqa: E402

# Marcas de centro: fmt() escapa el HTML, así que van como marcas y se cambian por etiquetas después.
I, C, E = '[[i]]', '[[c]]', '[[e]]'
ETIQUETAS = {'[[i]]': '<span class="cx i">Idiomas</span>', '[[c]]': '<span class="cx c">Computación</span>',
             '[[e]]': '<span class="cx e">Emprendimiento</span>'}


def con_centros(texto):
    """fmt() y luego cada centro con su dato en un bloque que no se parte (la línea corta entre centros)."""
    html = fmt(texto)
    return re.sub(r'(\[\[[ice]\]\])\s*([^\[]*?)\s*(?=\[\[|$)',
                  lambda m: f'<span class="par">{ETIQUETAS[m.group(1)]} {m.group(2)}</span> ', html).rstrip()

FLUJO = [
    ('Abrir el periodo', 'Registros Académicos'),
    ('Crear el NRC', 'Jefe del centro'),
    ('Carga lectiva', 'Jefe y Vicerrectorado'),
    ('Persona y admisión', 'Asistente o especialista'),
    ('Matrícula', 'Asistente o especialista'),
    ('Asistencia y notas', 'Registros y docente'),
    ('Pase a historia', 'Registros Académicos'),
]

# (fase, [(término, significado corto, definición)]). La definición pasa por fmt(): resalta códigos y **negrita**.
TERMINOS = [
    (0, [
        ('Periodo', 'STVTERM', 'Año + **5** (Centros) + secuencia: 1 verano, 4 semestre I, 6 semestre II. '
         'Ej.: **202656** = 2026-II de SEUSS.'),
        ('Parte de periodo', 'STVPTRM', 'Tramo con fechas y semanas: ' + f'{I} I01–I12 {C} X01–X07 {E} P01–P06'),
        ('SOATERM', 'Control de periodo', 'Abre el periodo y sus partes: fechas, acceso docente y controles '
         '(**Fatal** impide matricular).'),
    ]),
    (1, [
        ('NRC', 'Número de Referencia de Curso', 'Curso programado en una parte, con horario, cupo y docente. '
         'No se dice «sección» ni «grupo».'),
        ('SSASECT', 'Programar NRC', 'Crea y edita el NRC. Materia: '
         f'{I} ESEP {C} ESEC {E} ESGE'),
        ('Cupo', 'máximo del NRC', 'Máximo de alumnos del NRC, en SSASECT. No se dice «vacante» ni «capacidad».'),
        ('Lugares reservados', 'reserva', 'Parte del cupo del NRC apartada para un programa o criterio (SSASECT).'),
        ('Sobrepaso', 'permiso', 'Permiso para pasar un control: cruce de horario (SSASECT) o error de '
         'matrícula (permisos en SFAROVR y SFASRPO).'),
        ('Liga', 'NRC unidos', 'Dos NRC del mismo curso que se matriculan juntos (SSADETL). Solo en Idiomas: '
         'teórico + club.'),
    ]),
    (2, [
        ('SIAINST', 'Datos del docente', 'Registra al docente en el periodo: estatus, contrato (**ES** especialista, '
         '**FC** facilitador) y regla de carga.'),
        ('SIAASGN', 'Asignación del docente', 'Muestra la carga del docente: sus NRC, horas semanales y FTE (equivalente a '
         'tiempo completo).'),
        ('Carga lectiva', 'horas del docente', 'Horas del docente en sus NRC. El jefe la envía por oficio y el Vicerrectorado '
         'la aprueba con resolución.'),
    ]),
    (3, [
        ('ID', 'código de la persona', 'Código único de cada persona en Banner. Ej.: **S00581081**.'),
        ('GOAMTCH', 'Buscar persona', 'Busca a la persona para no duplicarla y, si no existe, la crea (aún es **persona**).'),
        ('SAAQUIK', 'Admisión rápida', 'Admite a la persona en el programa del centro: desde ahí es **alumno**.'),
        ('Programa', 'plan del centro', f'Programa del alumno: {I} IMEMI03 {C} CMEMC38 {E} MMEMM01'),
        ('SGASTDN', 'Registro del estudiante', 'Estatus del alumno (**AS** activo, **IS** inactivo) y sus programas (currículos).'),
        ('Alumno', 'admitido', 'Persona admitida en un programa del centro. No se dice «participante» '
         'ni «estudiante».'),
    ]),
    (4, [
        ('SFAREGS', 'Matrícula del alumno', 'Matricula al alumno en el NRC. Encabezado: periodo, ID y al final plan de '
         'estudios (no asumir 1).'),
        ('EL', 'autorizado', 'Estatus que autoriza al alumno a matricularse en el periodo (SFAREGS).'),
        ('Matrícula', 'RE', 'El alumno queda en el NRC con **RE**. No se dice «inscripción».'),
        ('Retiro', 'DD', '**DD** en SFAREGS: el alumno sale del NRC y libera el cupo.'),
        ('Retención', 'SOAHOLD', 'Bloqueo que impide la matrícula; por ejemplo, **TT** por cuota vencida.'),
        ('TSAAREV', 'Cuenta corriente', 'Muestra el cobro que generó la matrícula.'),
    ]),
    (5, [
        ('SHAEGBC', 'Calendario de notas', 'Fechas en que el docente puede registrar notas. Va **antes** que SHAGCOM.'),
        ('SHAGCOM', 'Plan de evaluación', 'Componentes de la nota del NRC y sus pesos; suman 1.'),
        ('ATTRGRD', 'Asistencia', 'Componente de asistencia del plan: peso 0, «Debe aprobar» y exige **70 %**.'),
        ('SOAATRK', 'Regla de asistencia', 'Regla de asistencia del NRC. Sin ella, «Pasar lista» no muestra el NRC.'),
        ('Autoservicio', 'portal web', 'Portal de Banner del docente y del alumno: **Pasar lista** y **Libro de calificaciones**.'),
        ('Escala', 'nota aprobatoria', f'{I} modo C: 70 de 100 {C} modo V: 11 de 20 {E} modo V: 11 de 20'),
        ('INH', 'Inhabilitado', 'Asistencia menor al 70 %: no aprueba ni da créditos, aunque el promedio apruebe.'),
        ('SFASLST', 'Lista de clase y notas', 'Nota final de cada alumno del NRC. Con libro de calificaciones, llega sola.'),
    ]),
    (6, [
        ('SHRROLL', 'Pase a historia', 'Lleva las notas a la historia académica (se ejecuta en GJAPCTL). No se dice '
         '«cierre de actas».'),
        ('CAPP', 'avance en la malla', 'Compara la historia con la malla: qué cumplió el alumno y qué le falta '
         '(SMARQCM y SMICRLT).'),
        ('Malla', 'SMAPROG', 'Requerimientos del programa que el alumno debe cumplir para aprobarlo.'),
    ]),
]

DIGA = [('participante', 'alumno'), ('sección o grupo', 'NRC'), ('inscripción', 'matrícula'),
        ('vacante', 'cupo'), ('cierre de actas', 'pase a historia')]

CSS = '''
@page { size: A4; }
.cover .logos img:first-child { height: 28px; }
.cover .logos img:last-child { height: 18px; }
.cover .logos { margin-bottom: 5px; }
.band { padding: 11px 18px 13px; }
.band { padding: 8px 16px 10px; }
.band h1 { font-size: 15.5pt; margin: 2px 0 1px; }
.band .sub { font-size: 8.4pt; }
.band .firma { font-size: 7.2pt; margin-top: 4px; color: #E9DCF5; }
.band .firma b { color: #fff; }
.flujo { display: flex; gap: 2px; margin: 8px 0 6px; }
.paso { flex: 1; position: relative; display: flex; align-items: center; background: var(--pl); color: var(--pd);
        padding: 4px 8px 4px 14px; min-height: 27px;
        clip-path: polygon(0 0, calc(100% - 9px) 0, 100% 50%, calc(100% - 9px) 100%, 0 100%, 9px 50%); }
.paso:first-child { clip-path: polygon(0 0, calc(100% - 9px) 0, 100% 50%, calc(100% - 9px) 100%, 0 100%);
                    padding-left: 7px; }
.paso:nth-child(odd) { background: #E9DAF6; }
.paso .n { flex: none; width: 15px; height: 15px; border-radius: 50%; background: var(--p); color: #fff;
           font: 700 7.4pt/15px 'Montserrat', sans-serif; text-align: center; margin-right: 4px; }
.paso .t { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 7.4pt; line-height: 1.15; }
.paso .q { display: block; font-size: 6.4pt; color: var(--mut); margin-top: 2px; }
table.afiche { font-size: 7.45pt; line-height: 1.27; }
table.afiche td { padding: 1.9px 6px; vertical-align: middle; }
table.afiche th { padding: 3.5px 6px; font-size: 7.4pt; }
table.afiche tr.grp td { padding: 2.6px 6px; font-size: 7pt; text-align: left; }
table.afiche td:nth-child(2) b { font-size: 7.9pt; }
.tm { color: var(--mut); font-size: 6.9pt; }
.cx { display: inline-block; border-radius: 7px; padding: 0 5px; margin: 0 2px 0 3px; color: #fff; font-size: 6.5pt;
      font-weight: 600; line-height: 1.45; }
.par { white-space: nowrap; }
.cx.i { background: #7030A0; } .cx.c { background: #0E8A5F; } .cx.e { background: #C2501C; }
.diga { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 10px; margin-top: 6px; padding: 6px 9px;
        border-left: 4px solid var(--g); background: var(--gl); border-radius: 7px; font-size: 7.4pt; }
.diga .tit { font-weight: 700; color: var(--gd); text-transform: uppercase; letter-spacing: .05em; font-size: 6.9pt; }
.diga s { color: #A11D1D; text-decoration: line-through; }
.diga b { color: var(--gd); }
'''


def construir():
    flujo = ''.join(f'<div class="paso"><span class="n">{k}</span><span class="t">{t}</span></div>'
                    for k, (t, _) in enumerate(FLUJO, start=1))
    filas, n = [], 0
    for fase, terminos in TERMINOS:
        nombre, quien = FLUJO[fase]
        filas.append(('grp', f'{fase + 1} · {nombre} — {quien}'))
        for termino, corto, definicion in terminos:
            n += 1
            filas.append([str(n), f'<b>{termino}</b> <span class="tm">({corto})</span>', con_centros(definicion)])
    tabla = table([('#', 4), ('Término', 25), ('Qué significa', 71)], filas, 'afiche left')
    diga = '<div class="diga"><span class="tit">Diga así</span>' + ''.join(
        f'<span><s>{mal}</s> › <b>{bien}</b></span>' for mal, bien in DIGA) + '</div>'
    cab = (f'<header class="cover"><div class="logos"><img src="{_url("img", "uss.png")}" alt="USS">'
           f'<img src="{_url("img", "ellucian.png")}" alt="Ellucian"></div><div class="band">'
           '<div class="kicker">Afiche para estudiar · Banner Student · Idiomas, Computación y Emprendimiento</div>'
           '<h1>Términos de Banner en el flujo de Centros Empresariales</h1>'
           '<div class="sub">En el orden en que ocurren: del periodo al pase a historia.</div>'
           f'<div class="firma">Elaborado por: <b>{AUTHOR}</b> · 26/10/2026 · Fuentes: instructivos de Ellucian y '
           'pruebas en TEST de la USS</div></div></header>')
    return cab + f'<div class="flujo">{flujo}</div>' + tabla + diga, n


if __name__ == '__main__':
    salida = sys.argv[1]
    cuerpo, n = construir()
    render('afiche_terminos', cuerpo, CSS, 'Términos de Banner · Centros Empresariales', salida,
           'Términos de Banner en el flujo de Centros Empresariales', f'Afiche de estudio: {n} términos en orden del flujo')
    check_pdf(salida, png_dir=os.path.join(os.path.dirname(os.path.abspath(salida)), 'png_afiche'), dpi=110)
