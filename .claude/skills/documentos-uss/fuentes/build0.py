# -*- coding: utf-8 -*-
"""0. Flujo general de Centros Empresariales: tabla de etapas y puntos a confirmar."""
import os
from ussdeck import *

NAME = '0. FLUJO GENERAL - CENTROS EMPRESARIALES'
OUT = os.path.join(HERE, 'entregables', NAME + '.pptx')

LISTO, SIGUE, PEND = ('Listo', 'E2F0D9', GREEN), ('Siguiente', 'F1E7FA', PURPLE), ('Pendiente', 'F2F2F2', '7F7F7F')

# N°, etapa, paso del flujo institucional, responsable, qué se hace, páginas, (resumen, estado)
FLUJO = [
    ('1', 'Periodos académicos', '1', 'Registros Académicos', 'Crear el periodo y sus fechas', 'STVTERM, SOATERM', ('1', LISTO)),
    ('2', 'Programación de NRC (secciones)', '4', 'Escuelas', 'Crear el NRC con horario, cupo y reglas', 'SSASECT, SSADETL, SSAPREQ, SSARRES', ('2 y 2.1', LISTO)),
    ('3', 'Carga lectiva', '1', 'Registros Académicos', 'Registrar al docente, asignarlo al NRC y revisar su carga', 'SIAINST, SSASECT, SIAASGN', ('3', LISTO)),
    ('4', 'Admisión', '2', 'Admisión', 'Registrar a la persona y dejarla como estudiante', 'GOAMTCH, SAAQUIK, SGASTDN', ('4', LISTO)),
    ('5', 'Inscripción en NRC', '—', 'Por confirmar', 'Inscribir al estudiante en sus NRC', 'SFAREGS', ('5', SIGUE)),
    ('6', 'Tutoría', '3', 'Registros Académicos', 'Asignar el tutor (asesor) al estudiante', 'SIAINST, SGAADVR', ('6', PEND)),
    ('7', 'Jefatura', '5', 'Jefatura', 'Aprobar excepciones de inscripción (por confirmar)', 'SFAROVR', ('7', PEND)),
    ('8', 'Docente', '6', 'Cada docente', 'Registrar asistencia y calificaciones', 'Autoservicio del docente', ('8', PEND)),
    ('9', 'Finanzas', '7', 'Finanzas', 'Cobrar matrícula y pensión, y registrar pagos', 'TSAAREV, TVACAJA', ('9', PEND)),
]

CONFIRMAR = [
    ('1', 'Admisión en Centros Empresariales: ¿registro manual o como postulante (interfaz / CEPRE)?', 'Manual, con SAAQUIK'),
    ('2', '¿Quién crea los NRC de Idiomas, Informática y Emprendimiento?', 'Las escuelas'),
    ('3', '¿Quién asigna el docente al NRC y revisa su carga?', 'Registros Académicos'),
    ('4', 'Inscripción en NRC: no figura en el flujo. ¿Quién la hace?', 'Registros Académicos (SFAREGS)'),
    ('5', '¿La tutoría aplica a Centros Empresariales?', 'Sí, con SGAADVR'),
    ('6', '¿Qué aprueba o revisa la jefatura en el sistema?', 'Excepciones de inscripción (SFAROVR)'),
    ('7', '¿El cobro de Finanzas se genera desde la inscripción?', 'Sí (TSAAREV)'),
]

LINE = '<a:ln w="9525"><a:solidFill><a:srgbClr val="BFBFBF"/></a:solidFill></a:ln>'


def cell_xml(text, sz=1100, bold=False, color='000000', fill=None, algn='l'):
    b = ' b="1"' if bold else ''
    run = (f'<a:r><a:rPr lang="es-ES" sz="{sz}"{b} dirty="0"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
           f'</a:rPr><a:t>{esc(text)}</a:t></a:r>') if text else f'<a:endParaRPr lang="es-ES" sz="{sz}" dirty="0"/>'
    borders = ''.join(LINE.replace('a:ln ', f'a:{s} ').replace('</a:ln>', f'</a:{s}>') for s in ('lnL', 'lnR', 'lnT', 'lnB'))
    fill_xml = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else '<a:noFill/>'
    return (f'<a:tc><a:txBody><a:bodyPr/><a:lstStyle/><a:p><a:pPr algn="{algn}"/>{run}</a:p></a:txBody>'
            f'<a:tcPr marL="64008" marR="64008" marT="36576" marB="36576" anchor="ctr">{borders}{fill_xml}</a:tcPr></a:tc>')


def table_xml(sid, x, y, widths, head_h, row_h, header, rows):
    """rows: lista de listas de dicts para cell_xml."""
    grid = ''.join(f'<a:gridCol w="{int(w)}"/>' for w in widths)
    trs = f'<a:tr h="{int(head_h)}">' + ''.join(
        cell_xml(h, bold=True, color='FFFFFF', fill=PURPLE, algn='ctr') for h in header) + '</a:tr>'
    for r in rows:
        trs += f'<a:tr h="{int(row_h)}">' + ''.join(cell_xml(**c) for c in r) + '</a:tr>'
    h = head_h + row_h * len(rows)
    return (f'<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="{sid}" name="Tabla {sid}"/>'
            f'<p:cNvGraphicFramePr><a:graphicFrameLocks noGrp="1"/></p:cNvGraphicFramePr><p:nvPr/></p:nvGraphicFramePr>'
            f'<p:xfrm><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(sum(widths))}" cy="{int(h)}"/></p:xfrm>'
            f'<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">'
            f'<a:tbl><a:tblPr firstRow="1" bandRow="1"/><a:tblGrid>{grid}</a:tblGrid>{trs}</a:tbl>'
            f'</a:graphicData></a:graphic></p:graphicFrame>')


def table_slide(slide_path, title, intro, table):
    t = parse(slide_path)
    set_title(t, title)
    spTree = t.find('.//p:spTree', NS)
    spTree.remove(shape_by_name(t, 'CuadroTexto 1'))
    sid = next_id(t)
    if intro:
        spTree.append(frag(textbox_xml(sid, 431320, 860000, 11329360, 380000,
                                       bullet_para(intro, sz=1400, bullet=False, spc_aft=0, algn='l'))))
        sid += 1
    spTree.append(frag(table(sid)))
    save(t, slide_path)


def flujo_table(sid):
    widths = [420000, 1900000, 800000, 1750000, 2900000, 2000000, 1560000]
    header = ['N°', 'Etapa', 'Paso del flujo', 'Responsable', '¿Qué se hace en Banner?', 'Páginas', 'Resumen']
    rows = []
    for n, etapa, paso, resp, que, pags, (res, (est, fill, col)) in FLUJO:
        rows.append([
            dict(text=n, bold=True, algn='ctr'),
            dict(text=etapa, bold=True),
            dict(text=paso, algn='ctr'),
            dict(text=resp, color=PURPLE if resp == 'Por confirmar' else '000000', bold=resp == 'Por confirmar'),
            dict(text=que),
            dict(text=pags, sz=1000),
            dict(text=f'{res} · {est}', bold=True, color=col, fill=fill, algn='ctr'),
        ])
    return table_xml(sid, 431320, 1290000, widths, 380000, 470000, header, rows)


def confirmar_table(sid):
    widths = [420000, 5400000, 3100000, 2410000]
    header = ['N°', 'Punto a confirmar', 'Propuesta', 'Confirmado / ajuste']
    rows = [[dict(text=n, bold=True, algn='ctr'), dict(text=q, sz=1200), dict(text=p, sz=1200, bold=True, color=PURPLE),
             dict(text='', fill='F2F2F2')] for n, q, p in CONFIRMAR]
    return table_xml(sid, 431320, 1290000, widths, 380000, 580000, header, rows)


def main():
    u, paths = build_structure(os.path.join(HERE, 'b0'), ['cover', 'text', 'text', 'close'])
    build_cover(paths[0], 'FLUJO GENERAL', 'CENTROS EMPRESARIALES',
                'Etapas, responsables y páginas de Banner, para confirmar')
    table_slide(paths[1], 'FLUJO Y RESPONSABLES',
                para('Orden según el sistema: sin periodo no hay NRC; sin NRC no hay carga ni inscripción. ',
                     G('«Paso del flujo»'), ' = número en el flujo institucional.'),
                flujo_table)
    table_slide(paths[2], 'PUNTOS A CONFIRMAR',
                para('Marque cada propuesta como confirmada o anote el ajuste.'),
                confirmar_table)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    finalize(u, OUT, NAME)
    print('OK', OUT)


if __name__ == '__main__':
    main()
