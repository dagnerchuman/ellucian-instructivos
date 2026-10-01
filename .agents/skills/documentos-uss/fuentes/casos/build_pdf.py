# -*- coding: utf-8 -*-
"""PDF: casuísticas para las pruebas integrales (estudiantes y docentes)."""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/ellucian-instructivos/.claude/skills/documentos-uss/scripts/pdf')
sys.path.insert(0, HERE)
from common import AUTHOR, check_pdf, explicar, fmt, glosario_html, header, render, section  # noqa: E402
import ejemplo_centros as E  # noqa: E402
import casos_data as D  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    HERE, '..', 'entregables', 'CASUÍSTICAS PARA LAS PRUEBAS INTEGRALES - ESTUDIANTES Y DOCENTES.pdf')

LAB = {'sit': 'Situación', 'ell': 'En Banner', 'res': 'Resultado esperado', 'fuera': 'Fuera de Banner', 'cen': 'En los centros'}


def row(kind, inner):
    return f'<div class="r {kind}"><span class="lab">{LAB[kind]}</span><div>{inner}</div></div>'


def caso(c):
    fam, cls = D.FAMILIAS[c['id'][0]]
    pasos = ('<ol class="steps1">' + ''.join(f'<li>{fmt(t)} <span class="cite">{"Instructivo " if k[0].isdigit() else ""}{k}</span></li>'
                                              for t, k in c['pasos']) + '</ol>')
    return explicar(f'<div class="ex {cls}"><div class="exh"><span class="exn">{c["id"]}</span><b>{html.escape(c["titulo"])}</b>'
                    f'<span class="ctr">{fam}</span></div>'
                    + row('sit', fmt(c['situacion'])) + row('ell', pasos) + row('res', fmt(c['resultado']))
                    + row('fuera', fmt(c['fuera'])) + row('cen', fmt(c['centros'])) + '</div>')


def build():
    b = [header('Universidad Señor de Sipán · Migración a Ellucian Banner', D.TITULO, D.SUBTITULO,
                [('Elaborado por', AUTHOR), ('Fecha', '28 de septiembre de 2026'),
                 ('Fuentes', 'Reuniones del 25 y 28/09 · Instructivos de Ellucian'), ('Estado', 'Para confirmar')])]
    b.append(explicar('<div class="lead">Una <b>casuística</b> es un caso real que se prueba de inicio a fin en Banner. Cada caso dice '
                      'qué pasa, qué se hace en Banner (con la cita del instructivo), qué resultado se espera y qué queda '
                      '<b>fuera de Banner</b> porque lo decide la USS. Las dudas están al final.</div>'))

    # 1. Muestra previa
    b.append(section(1, 'La muestra que ya teníamos',
                     'Sí: en «Validación de la migración» (25/09) se propusieron 16 participantes por programa y 8 escenarios de riesgo.'))
    tot = sum(n for _, n in D.MUESTRA)
    b.append(explicar('<div class="two2"><div class="mc"><div class="mh">Muestra por programa de cada centro</div>'
                      + ''.join(f'<div class="mr"><span>{fmt(t)}</span><b>{n}</b></div>' for t, n in D.MUESTRA)
                      + f'<div class="mr tot"><span>Total por programa</span><b>{tot}</b></div></div>'
                      '<div class="mc"><div class="mh">Escenarios de riesgo de la migración</div><ol class="esc">'
                      + ''.join(f'<li>{fmt(e)}</li>' for e in D.ESCENARIOS) + '</ol>'
                      '<div class="mnote">Estos casos prueban que <b>los datos migrados</b> estén bien. Las casuísticas nuevas '
                      'prueban <b>situaciones de la vida real</b> con estudiantes y docentes.</div></div></div>'))

    # 2. Casuísticas nuevas
    b.append(section(2, 'Casuísticas nuevas', 'Siete casos en tres grupos: docente, estudiante con dificultades, y queja o sanción.'))
    b.append('<div class="fams">' + ''.join(
        f'<div class="fam {cls}"><b>{fam}</b><span>{", ".join(c["id"] for c in D.CASOS if c["id"][0] == k)}</span></div>'
        for k, (fam, cls) in D.FAMILIAS.items()) + '</div>')
    for c in D.CASOS:
        b.append(caso(c))

    # 3. Qué hace y qué no
    b.append(section(3, 'Qué hace Ellucian y qué no'))
    si, no = D.SI_NO
    b.append(explicar('<div class="sino keep"><div class="si"><div class="sh">Banner lo hace</div><ul>'
                      + ''.join(f'<li>{fmt(x)}</li>' for x in si) + '</ul></div><div class="no"><div class="sh">Lo decide la USS, '
                      'fuera de Banner</div><ul>' + ''.join(f'<li>{fmt(x)}</li>' for x in no) + '</ul></div></div>'))

    # 4. Checklist
    b.append(section(4, 'Para las pruebas integrales (16/11 al 26/12)'))
    b.append('<div class="tests">' + ''.join(explicar(
        f'<div class="tc"><div class="tt"><span class="k">{c["id"]}</span>{html.escape(c["titulo"])}</div>'
        + ''.join(f'<div class="ti"><span class="bx"></span><div>{fmt(x)}</div></div>' for x in c['prueba']) + '</div>')
        for c in D.CASOS) + '</div>')

    dudas = ('<div class="dudas"><div class="dc">' + explicar('<div class="dh">Para Ellucian</div><ol>'
             + ''.join(f'<li>{fmt(q)}</li>' for q in D.DUDAS_E) + '</ol>') + '</div><div class="dc uss">'
             + explicar(f'<div class="dh">Para la USS</div><ol start="{len(D.DUDAS_E) + 1}">'
                        + ''.join(f'<li>{fmt(q)}</li>' for q in D.DUDAS_U) + '</ol>') + '</div></div>')
    b.append(section(5, 'Glosario'))
    b.append(glosario_html())
    b.append(section(6, 'Dudas para confirmar'))
    b.append(dudas)
    return '\n'.join(b)


CSS = E.CSS + '''
:root { --doc: #5C2193; --docl: #F1E7FA; --est: #0E8A5F; --estl: #E4F5EE; --que: #C2501C; --quel: #FDEDE4; }
.ex.doc { border-left-color: var(--doc); } .ex.doc .exn { background: var(--doc); } .ex.doc .ctr { background: var(--docl); color: var(--doc); }
.ex.est { border-left-color: var(--est); } .ex.est .exn { background: var(--est); } .ex.est .ctr { background: var(--estl); color: var(--est); }
.ex.que { border-left-color: var(--que); } .ex.que .exn { background: var(--que); } .ex.que .ctr { background: var(--quel); color: var(--que); }
.r.sit { background: var(--pz); } .r.sit .lab { color: var(--mut); }
.r.fuera { background: #FFF8E8; } .r.fuera .lab { color: #8A5A00; }
.r.cen { background: #fff; } .r.cen .lab { color: var(--mut); }
.r .lab { font-size: 6.6pt; }
.ex .r { grid-template-columns: 104px 1fr; }
.two2 { display: grid; grid-template-columns: 1fr 1fr; gap: 9px; break-inside: avoid; }
.mc { border: 1px solid var(--line); border-radius: 10px; overflow: hidden; background: #fff; }
.mh { background: var(--pl); color: var(--pd); font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 9pt; padding: 6px 12px; }
.mr { display: flex; justify-content: space-between; gap: 8px; padding: 4px 12px; border-top: 1px solid var(--line); font-size: 8.5pt; }
.mr b { color: var(--pd); } .mr.tot { background: var(--pl); font-weight: 700; }
ol.esc { margin: 6px 12px 4px 28px; padding: 0; } ol.esc li { font-size: 8.5pt; margin: 0 0 3px; }
.mnote { margin: 4px 10px 10px; padding: 6px 9px; background: var(--gl); border-radius: 7px; font-size: 8.3pt; line-height: 1.4; }
.fams { display: grid; grid-template-columns: repeat(3, 1fr); gap: 7px; margin: 0 0 9px; }
.fam { border-radius: 8px; padding: 6px 10px; display: flex; justify-content: space-between; align-items: center; font-size: 8.8pt; }
.fam.doc { background: var(--docl); color: var(--doc); } .fam.est { background: var(--estl); color: var(--est); }
.fam.que { background: var(--quel); color: var(--que); } .fam span { font-weight: 700; font-size: 8pt; }
.sino { display: grid; grid-template-columns: 1fr 1fr; gap: 9px; }
.si, .no { border-radius: 10px; overflow: hidden; border: 1px solid var(--line); }
.si { background: var(--gl); } .no { background: #FFF8E8; }
.sh { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 9.5pt; padding: 7px 12px; color: #fff; }
.si .sh { background: var(--gd); } .no .sh { background: #8A5A00; }
.si ul, .no ul { margin: 7px 12px 9px 26px; padding: 0; } .si li, .no li { font-size: 8.8pt; margin: 0 0 4px; line-height: 1.4; }
.tc .tt .k { width: auto; padding: 0 5px; border-radius: 6px; font-size: 7.4pt; }
'''


if __name__ == '__main__':
    p = render('casos', build(), CSS, 'Casuísticas para las pruebas integrales · Estudiantes y docentes', OUT,
               'Casuísticas para las pruebas integrales - Estudiantes y docentes',
               'Casos de docentes, estudiantes con dificultades, quejas y sanciones: qué hace Banner y qué queda fuera')
    check_pdf(p, png_dir=os.path.join(HERE, 'png'))
