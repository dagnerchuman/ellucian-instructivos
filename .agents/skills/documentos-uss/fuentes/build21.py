# -*- coding: utf-8 -*-
"""2.1 Programación de asignaturas: correquisitos, prerrequisitos y restricciones (SSADETL, SSAPREQ, SSARRES)."""
import os
from ussdeck import *

SRC53 = os.path.join(HERE, '..', 'src53', 'x')
NAME = '2.1 PROGRAMACIÓN DE ASIGNATURAS - CORREQUISITOS, PRERREQUISITOS Y RESTRICCIONES'
OUT = os.path.join(HERE, 'entregables', NAME + '.pptx')

CFG = [
    (34, 'DETALLE DE SECCIÓN - SSADETL', [
        para('Una vez creado el NRC, su información se complementa en ', G('SSADETL'), '.'),
        para('Se ingresa desde la página principal de Experience o desde el ', G('Menú relacionado'),
             ' de SSASECT (ícono resaltado) › ', B('Detalle de sección de curso [SSADETL]'), '.'),
    ], 'ctr'),
    (35, 'DETALLE DE SECCIÓN - SSADETL', [
        para(G('1. '), 'Ingrese el ', G('Periodo'), '. (Requerido)'),
        para(G('2. '), 'Ingrese el ', G('NRC'), ' que desea configurar. (Requerido)'),
        para(G('3. '), 'Seleccione ', G('Ir'), '.'),
        para('Si ingresa desde el Menú relacionado, el sistema trae por defecto el último NRC trabajado.'),
    ], 'l'),
    (36, 'DETALLE DE SECCIÓN - SSADETL', [
        para(G('4. '), 'Pestaña ', G('Correquisitos y ligas de sección'), ': registre los ',
             B('NRC correquisito'), ' (se deben inscribir juntos) y el ', B('conector de liga'),
             ' cuando el curso trabaje con ligas.'),
        para('Si el catálogo ya los define, aparecen heredados. Guarde si realiza cambios.'),
    ], 'l'),
    (37, 'DETALLE DE SECCIÓN - SSADETL', [
        para(G('5. '), 'Pestaña ', G('Atributos de programa de grado'),
             ': muestra los atributos que el curso tiene definidos en el catálogo.'),
        para('Se pueden ajustar solo para este NRC. Guarde si realiza cambios.'),
    ], 'l'),
    (40, 'PRERREQUISITOS DE SECCIÓN - SSAPREQ', [
        para('Se ingresa igual que SSADETL: ', G('Menú relacionado'), ' de SSASECT › ',
             B('Prerrequisitos de horario [SSAPREQ]'), '.'),
        para(G('1. '), 'Ingrese el ', G('Periodo'), '. (Requerido)'),
        para(G('2. '), 'Ingrese el ', G('NRC'), ' que desea configurar. (Requerido)'),
        para(G('3. '), 'Seleccione ', G('Ir'), '.'),
    ], 'l'),
    (41, 'PRERREQUISITOS DE SECCIÓN - SSAPREQ', [
        para('En la pestaña ', G('Restricciones de puntaje de examen y de prerrequisitos de sección'),
             ' se muestran los prerrequisitos ', B('heredados del catálogo (SCAPREQ)'), '.'),
        para('Con las opciones ', G('Insertar, Eliminar o Copiar'), ' (resaltadas) se ajustan solo para este NRC.'),
    ], 'ctr'),
    (42, 'PRERREQUISITOS DE SECCIÓN - SSAPREQ', [
        para(G('4. '), 'Inserte el prerrequisito indicando ', B('Materia'), ', ', B('Número de curso'), ', ',
             B('Nivel'), ' y ', B('Calificación'), ' mínima. Para combinar varios use ', G('Y / O'),
             ' y paréntesis.'),
        para('En la imagen (referencial) se exige ACCT 0110 ', B('o'), ' ACC0 0400.'),
        para(G('Ejemplo Idiomas: '), 'en un NRC de ', B('BASIC II'), ' se registra ', B('BASIC I'), ' aprobado.'),
        para(G('5. '), B('Guarde'), ' la información.'),
    ], 'l'),
    (45, 'RESTRICCIONES DE SECCIÓN - SSARRES', [
        para('Desde el ', G('Menú relacionado'), ' de SSASECT › ', B('Restricciones de horario [SSARRES]'), '.'),
        para(G('1. '), 'Ingrese el ', G('Periodo'), '. (Requerido)'),
        para(G('2. '), 'Ingrese el ', G('NRC'), ' que desea configurar. (Requerido)'),
        para(G('3. '), 'Seleccione ', G('Ir'), '.'),
    ], 'l'),
    (46, 'RESTRICCIONES DE SECCIÓN - SSARRES', [
        para('Las restricciones del NRC se ', B('heredan del catálogo (SCARRES)'), ' y se pueden modificar aquí.'),
        para('En cada pestaña se elige ', G('Incluir'), ' (solo pueden inscribirse los indicados) o ',
             G('Excluir'), ' (pueden inscribirse todos, menos los indicados).'),
    ], 'ctr'),
    (47, 'RESTRICCIONES DE SECCIÓN - SSARRES', [
        para(G('4. '), 'Pestaña ', G('Clase y nivel'), ' › Restricciones de nivel: elija ', B('Incluir'),
             ' o ', B('Excluir'), '.'),
        para(G('5. '), 'Ingrese el código de ', G('Nivel'), '. Use + y – para agregar o quitar registros.'),
        para(G('6. '), B('Guarde'), ' la información.'),
    ], 'l'),
    (48, 'RESTRICCIONES DE SECCIÓN - SSARRES', [
        para(G('7. '), 'Pestaña ', G('Grado y programa'), ' › Restricciones de programa: elija ', B('Incluir'),
             ' o ', B('Excluir'), '.'),
        para(G('8. '), 'Ingrese el código del ', G('Programa'), ' autorizado para el NRC.'),
        para(G('9. '), B('Guarde'), ' la información.'),
    ], 'l'),
    (49, 'RESTRICCIONES DE SECCIÓN - SSARRES', [
        para(G('10. '), 'Pestaña ', G('Campus y escuela'), ' › Restricciones de campus: elija ', B('Incluir'),
             ' o ', B('Excluir'), '.'),
        para(G('11. '), 'Ingrese el código de ', G('Campus'), ' (sede) del NRC.'),
        para(G('12. '), B('Guarde'), ' la información.'),
    ], 'l'),
    (50, 'RESTRICCIONES DE SECCIÓN - SSARRES', [
        para(G('13. '), 'Pestaña ', G('Atributo y cohorte'), ' › Restricciones de atributo de alumno: elija ',
             B('Incluir'), ' o ', B('Excluir'), '.'),
        para(G('14. '), 'Ingrese el código de ', G('Atributo'), '.'),
        para(G('15. '), B('Guarde'), ' la información.'),
        para('Las restricciones de ', B('Cohorte'), ', en la misma pestaña, se registran de la misma forma.'),
    ], 'l'),
]

SECTIONS = {
    'SSADETL': ('DETALLE DE SECCIÓN (SSADETL)',
                'Complementa el NRC con correquisitos, ligas de sección y atributos heredados del catálogo.'),
    'SSAPREQ': ('PRERREQUISITOS DE SECCIÓN (SSAPREQ)',
                'Define qué cursos o puntajes de examen debe tener aprobados el alumno para inscribirse en el NRC.'),
    'SSARRES': ('RESTRICCIONES DE SECCIÓN (SSARRES)',
                'Define quién puede inscribirse en el NRC: nivel, programa, campus, atributo o cohorte.'),
}

PLAN = (['cover', 'flow', 'herencia', ('div', 'SSADETL')] + [('cfg', i) for i in range(0, 4)]
        + [('div', 'SSAPREQ')] + [('cfg', i) for i in range(4, 7)]
        + [('div', 'SSARRES')] + [('cfg', i) for i in range(7, 13)]
        + ['resumen', 'close'])
KIND = {'herencia': 'text', 'resumen': 'text'}


def build_herencia(slide_path):
    t = parse(slide_path)
    set_title(t, 'HERENCIA DESDE EL CATÁLOGO')
    spTree = t.find('.//p:spTree', NS)
    spTree.remove(shape_by_name(t, 'CuadroTexto 1'))
    sid = next_id(t)
    shapes = []
    intro = bullet_para(para('Al crear un NRC en ', B('SSASECT'), ', Banner copia la configuración vigente del ',
                             B('catálogo de cursos'), '. Después, cada NRC se puede ajustar en tres páginas, sin modificar el catálogo:'),
                        sz=1600, bullet=False, spc_aft=0)
    shapes.append(textbox_xml(sid, 431320, 930000, 11329360, 700000, intro)); sid += 1
    cols = [
        ('SSADETL', 'Detalle de sección', [para(B('Correquisitos: '), 'NRC que se deben inscribir juntos.'),
                                             para(B('Ligas '), 'de sección.'),
                                             para(B('Atributos '), 'del curso.')], 'SCADETL'),
        ('SSAPREQ', 'Prerrequisitos', [para('Cursos o puntajes de examen que el alumno debe tener ', B('aprobados'), '.'),
                                         para(G('Ejemplo Idiomas: '), 'BASIC II requiere BASIC I.')], 'SCAPREQ'),
        ('SSARRES', 'Restricciones', [para('Quién puede inscribirse en el NRC: ', B('nivel, programa, campus, atributo o cohorte'), '.'),
                                        para('Con ', B('Incluir'), ' o ', B('Excluir'), '.')], 'SCARRES'),
    ]
    gap, left, top = 300000, 431320, 1750000
    cw = (11329360 - 2 * gap) / 3
    for i, (code, name, items, src) in enumerate(cols):
        x = left + i * (cw + gap)
        head = (f'<a:p><a:pPr algn="ctr"/>{run_xml(code, "g", sz=2000)}</a:p>'
                f'<a:p><a:pPr algn="ctr"/>{run_xml(name, "b", sz=1600)}</a:p>')
        shapes.append(textbox_xml(sid, x, top, cw, 780000, head, anchor='ctr', fill=PURPLE, geom='roundRect')); sid += 1
        body = ''.join(bullet_para(it, sz=1600, spc_aft=600, algn='l') for it in items)
        body += bullet_para(para('Se hereda de: ', G(src)), sz=1600, bullet=False, spc_aft=0, algn='l')
        shapes.append(textbox_xml(sid, x, top + 860000, cw, 2250000, body, fill='F1E7FA', geom='roundRect',
                                  insets=' lIns="137160" tIns="137160" rIns="137160" bIns="91440"')); sid += 1
    note = bullet_para(para(G('Importante: '), 'el NRC toma la configuración del catálogo al momento de crearse. '
                            'Si después cambia el catálogo, el NRC no se actualiza solo: el ajuste se hace en estas páginas.'),
                       sz=1400, bullet=False, spc_aft=0, algn='l')
    shapes.append(textbox_xml(sid, 431320, 5000000, 11329360, 620000, note, anchor='ctr', line=GREEN,
                              geom='roundRect')); sid += 1
    for s in shapes:
        spTree.append(frag(s))
    save(t, slide_path)


def main():
    kinds = [(KIND.get(p, p) if isinstance(p, str) else p[0]) for p in PLAN]
    u, paths = build_structure(os.path.join(HERE, 'b21'), kinds)
    for item, path in zip(PLAN, paths):
        kind = item if isinstance(item, str) else item[0]
        if kind == 'cfg':
            n, title, paras, algn = CFG[item[1]]
            build_cfg(u, path, SRC53, n, title, paras, algn, tag='ssa')
        elif kind == 'div':
            build_div(path, *SECTIONS[item[1]])
        elif kind == 'cover':
            build_cover(path, 'PROGRAMACIÓN DE ASIGNATURAS', 'PARTE 2',
                        'Correquisitos, prerrequisitos y restricciones del NRC')
        elif kind == 'flow':
            set_flow_boxes(path, [
                ('Habilitación del periodo de programación académica', 'SOATERM'),
                ('Creación de NRC definiendo características básicas', 'SSASECT'),
                ('Definir cupos disponibles', 'SSASECT'),
                ('Definir horario de impartición y docente', 'SSASECT'),
                ('Definir correquisitos a nivel de sección', 'SSADETL'),
                ('Definir prerrequisitos a nivel de sección', 'SSAPREQ'),
                ('Definir restricciones de inscripción a nivel de sección', 'SSARRES'),
            ], note=[para('En esta presentación: pasos ', G('resaltados'), ' (SSADETL, SSAPREQ y SSARRES).'),
                     para('Los pasos anteriores están en ', B('«2. Programación de asignaturas»'),
                          '. La asignación del docente se ve en ', B('«3. Docentes»'), '.')],
               highlight=(4, 5, 6))
        elif kind == 'herencia':
            build_herencia(path)
        elif kind == 'resumen':
            build_bullets(path, 'RESUMEN', [
                para(B('SSADETL'), ': complementa el NRC con correquisitos, ligas de sección y atributos heredados del catálogo.'),
                para(B('SSAPREQ'), ': muestra los prerrequisitos heredados de SCAPREQ; se pueden insertar, eliminar o copiar solo para ese NRC.'),
                para(B('SSARRES'), ': define quién puede inscribirse en el NRC (nivel, programa, campus, atributo o cohorte) con Incluir o Excluir.'),
                para(B('Acceso'), ': desde el Menú relacionado de SSASECT o desde la búsqueda de Experience, indicando Periodo y NRC.'),
                para(B('Recuerde'), ': los cambios posteriores en el catálogo no se aplican a los NRC ya creados.'),
                para(B('Siguiente tema'), ': 3. Docentes (registro del docente, asignación al NRC y carga de trabajo).'),
            ])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    finalize(u, OUT, NAME)
    print('OK', OUT)


if __name__ == '__main__':
    main()
