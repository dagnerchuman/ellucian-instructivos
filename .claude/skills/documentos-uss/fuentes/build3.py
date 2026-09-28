# -*- coding: utf-8 -*-
"""3. Docentes: configuración, registro del docente, asignación al NRC y carga de trabajo (resumido)."""
import os
from ussdeck import *

SRC = os.path.normpath(os.path.join(HERE, '..', 'src3'))
SA, SB, SC = (os.path.join(SRC, x) for x in ('A', 'B', 'C'))   # 5.2 Información de docentes, 5.2 Carga, 6.2.1 Asignar
NAME = '3. DOCENTES - REGISTRO, ASIGNACIÓN Y CARGA DE TRABAJO'
OUT = os.path.join(HERE, 'entregables', NAME + '.pptx')

REQ = ' (Requerido)'
CFG = {
    # ---------------- configuraciones
    'fcst': (SA, 10, 'ESTATUS DEL DOCENTE - STVFCST', [
        para('Define los ', G('estatus del docente'), ' que luego se eligen en SIAINST (ej. ', B('AC'), ' Activo, ',
             B('BA'), ' Baja).'),
        para(G('1. '), 'Presione ', G('Insertar (+)'), '.'),
        para(G('2. '), 'Ingrese el ', G('Código'), ': 2 caracteres.' + REQ),
        para(G('3. '), 'Ingrese la ', G('Descripción'), ': hasta 30 caracteres.' + REQ),
        para(G('4. '), B('Guarde'), ' la información.'),
    ]),
    'fstp': (SA, 11, 'TIPO DE PERSONAL - STVFSTP', [
        para('Define los ', G('tipos de personal docente'), ' que se eligen en SIAINST (ej. empleado, practicante).'),
        para(G('1. '), 'Presione ', G('Insertar (+)'), '.'),
        para(G('2. '), 'Ingrese el ', G('Código'), ': 4 caracteres.' + REQ),
        para(G('3. '), 'Ingrese la ', G('Descripción'), ': hasta 30 caracteres.' + REQ),
        para(G('4. '), B('Guarde'), ' la información.'),
    ]),
    'fcnt': (SA, 12, 'TIPO DE CONTRATO - STVFCNT', [
        para('Define los ', G('tipos de contrato del docente'), ' que se registran en SIAINST (ej. ', B('FT'),
             ' Full-Time Instructor).'),
        para(G('1. '), 'Presione ', G('Insertar (+)'), '.'),
        para(G('2. '), 'Ingrese el ', G('Código'), ': 2 caracteres.' + REQ),
        para(G('3. '), 'Ingrese la ', G('Descripción'), ': hasta 30 caracteres.' + REQ),
        para(G('4. '), B('Guarde'), ' la información.'),
    ]),
    # ---------------- registro del docente
    'spaiden': (SA, 16, 'PREMISA - SPAIDEN', [
        para('Antes de registrarlo como docente, la persona debe existir en Banner (', G('SPAIDEN'), ').'),
        para('El ', B('ID'), ' resaltado es el que se usa luego en SIAINST, SSASECT y SIAASGN.'),
    ]),
    'siainst1': (SA, 17, 'INFORMACIÓN DEL DOCENTE - SIAINST', [
        para(G('1. '), 'Ingrese el ', G('ID'), ' del docente y el ', G('Periodo'),
             ' desde el cual será vigente (ej. 202654, ver «1. Periodos académicos»).' + REQ),
        para(G('2. '), 'Seleccione ', G('Ir'), '.'),
    ]),
    'siainst2': (SA, 18, 'INFORMACIÓN DEL DOCENTE - SIAINST', [
        para(G('3. '), 'Ingrese el ', G('Estatus'), ' (STVFCST) y marque ', B('Docente'), ' y/o ', B('Asesor'), '.'),
        para(G('4. '), B('Sobrepasar seguridad de regla de proceso'), ': opcional; solo si también es asesor.'),
        para(G('5. '), 'Ingrese ', G('Categoría'), ', ', G('Tipo de personal'), ' (STVFSTP) y ',
             G('Regla de carga de trabajo'), ' (STVWKLD, ver carga de trabajo).'),
        para(G('6. '), B('Guarde'), '.  ', G('7. '), 'Pase al ', B('bloque siguiente'), '.'),
    ]),
    'siainst3': (SA, 19, 'INFORMACIÓN DEL DOCENTE - SIAINST', [
        para(G('8. '), 'Registre el ', G('Contrato'), ' (STVFCNT) y su regla. Deje al menos un registro con ',
             B('Indicador de predefinido'), ' activo.'),
        para(G('9. '), 'Registre la ', G('Escuela y departamento'), ' a los que pertenece el docente.'),
        para(G('10 y 11. '), B('Guarde'), ' y pase al bloque siguiente (atributos y comentarios, opcional).'),
    ]),
    'siainst4': (SA, 25, 'MANTENIMIENTO POR PERIODO - SIAINST', [
        para('Para cambiar datos del docente a partir de un ', G('nuevo periodo'), ': búsquelo con su ID y ese periodo, presione ',
             G('1. Mantenimiento'), ', actualice la información y ', B('guarde'), '.'),
        para('El cambio rige desde ese periodo; los periodos anteriores conservan sus datos.'),
    ], {'callout_at': (4300000, 3700000, 6900000)}),
    # ---------------- asignación al NRC
    'sesion': (SC, 14, 'ASIGNAR DOCENTE - SSASECT', [
        para('En SSASECT, pestaña ', G('Instructor y horas de reunión'), ' (ver «2. Programación de asignaturas»), cada horario tiene un ',
             G('Indicador de sesión'), ' (01 por defecto).'),
        para('Si el NRC tiene más de un docente, use ', B('02, 03…'), ' en la sesión de cada uno.'),
    ]),
    'instructor': (SC, 15, 'ASIGNAR DOCENTE - SSASECT', [
        para(G('1. '), 'En el bloque ', G('Instructor'), ', en la sesión que corresponda, ingrese el ', B('ID'),
             ' del docente si lo conoce, o búsquelo con ', G('Consultar docentes disponibles (SIAFAVL)'),
             ' desde el Menú relacionado.'),
    ]),
    'siafavl1': (SC, 16, 'DOCENTES DISPONIBLES - SIAFAVL', [
        para(G('a. '), 'Menú relacionado › ', G('Consultar docentes disponibles (SIAFAVL)'), '.'),
        para(G('b. '), 'Se abre con el ', B('periodo y NRC'), ' de SSASECT; presione ', G('Ir'),
             '. Opcional: filtrar por atributos del docente.'),
    ]),
    'siafavl2': (SC, 18, 'DOCENTES DISPONIBLES - SIAFAVL', [
        para(G('c. '), 'Se muestra la lista de docentes disponibles; haga clic en el que desea asignar.'),
        para(G('d. '), 'Presione ', G('Seleccionar'), ': el docente queda asignado al NRC.'),
    ], {'relabel': {'e': 'c', 'f': 'd'}}),
    'porcentajes': (SC, 19, 'ASIGNAR DOCENTE - SSASECT', [
        para(G('2. '), G('% de responsabilidad'), ': si hay más de un docente, reparta la carga del NRC.'),
        para(G('3. '), G('Indicador de principal'), ': solo para un docente del NRC.'),
        para(G('4. '), G('Indicador de sobrepaso'), ': márquelo solo si el docente tiene cruce de horario y aun así debe quedar asignado.'),
        para(G('5. '), G('% de sesión'), ': tiempo de la sesión que dicta el docente.'),
        para(G('6. '), B('Guarde'), ' la información.'),
    ]),
    # ---------------- carga de trabajo
    'siaterm': (SB, 12, 'CARGA DEL PERIODO - SIATERM', [
        para('Ingrese el ', G('Periodo'), ' y presione ', G('Ir'), '.'),
        para(G('1. '), G('Factor FTE'), ': horas que equivalen a una jornada completa (ej. 50 horas = 1 FTE).'),
        para(G('2. '), G('Factor de duración'), ': minutos de la hora académica (ej. 50).'),
        para(G('3. '), B('Guarde'), '. Si se dejan en blanco, SIAASGN no calcula la carga por FTE.'),
    ], {'relabel': {'3': '1', '4': '2', '5': '3'}}),
    'stvwkld': (SA, 28, 'CÓDIGOS DE REGLA DE CARGA - STVWKLD', [
        para('Define los ', G('códigos de regla de carga'), ' que se asignan al docente en SIAINST (ej. ', B('AP090'),
             ' = 90 horas académicas).'),
        para(G('1. '), 'Presione ', G('Insertar (+)'), '.'),
        para(G('2. '), 'Ingrese el ', G('Código'), ': 6 caracteres.' + REQ),
        para(G('3. '), 'Ingrese la ', G('Descripción'), ': hasta 30 caracteres.' + REQ),
        para(G('4. '), B('Guarde'), ' la información.'),
    ]),
    'siaflrt1': (SB, 17, 'REGLA DE CARGA - SIAFLRT', [
        para('Ingrese el ', G('Periodo'), ' y presione ', G('Ir'), '.'),
        para(G('1. '), 'Verifique que la regla esté ', G('Activa'), '.'),
        para(G('2. '), 'Elija el ', G('Código de regla de carga de trabajo'), ' (STVWKLD) que va a configurar.'),
    ], {'relabel': {'3': '1', '4': '2'}}),
    'siaflrt2': (SB, 18, 'REGLA DE CARGA - SIAFLRT', [
        para(G('3. '), 'Registre el rango ', G('Inferior – Superior'), ' que debe cumplir el docente en:'),
        para(B('Horas crédito'), ' (totales y generadas) · ', B('Horas de contacto'), ' (semanales y totales) · ',
             B('Carga de trabajo'), ' (educativa, no educativa y total) · ', B('Rango FTE'), '.'),
        para(B('Guarde'), ' la información.'),
    ], {'relabel': {'5': '3'}}),
    'siaasgn1': (SB, 24, 'CARGA DEL DOCENTE - SIAASGN', [
        para('Ingrese el ', G('ID'), ' del docente y el ', G('Periodo'), '; presione ', G('Ir'), '.'),
        para('Se listan los ', B('NRC asignados'), ' con su carga (créditos, horas, % de sesión y de responsabilidad); se pueden ajustar.'),
        para(G('1. '), B('Guarde'), ' si hizo cambios.  ', G('2. '), 'Pase al bloque siguiente.'),
    ], {'relabel': {'3': '1', '4': '2'}}),
    'siaasgn2': (SB, 27, 'CARGA DEL DOCENTE - SIAASGN', [
        para('En el análisis, cada criterio se compara con el rango de la regla (SIAFLRT): ', G('O'),
             ' = sobrecarga, ', G('U'), ' = subcarga. Sin letra, el docente está dentro del rango.'),
        para('Esta revisión reemplaza el control de carga que hoy se lleva en ', B('Excel'), '.'),
    ]),
}

PLAN = [
    ('cover',), ('flow',), ('conceptos',),
    ('div', 'CONFIGURACIONES', 'Tablas de validación del docente. Se crean una sola vez y luego se eligen en SIAINST.'),
    ('cfg', 'fcst'), ('cfg', 'fstp'), ('cfg', 'fcnt'),
    ('div', 'REGISTRO DEL DOCENTE', 'El docente debe existir como persona (SPAIDEN) y estar activo en SIAINST para el periodo del NRC.'),
    ('cfg', 'spaiden'), ('cfg', 'siainst1'), ('cfg', 'siainst2'), ('cfg', 'siainst3'), ('cfg', 'siainst4'),
    ('div', 'ASIGNACIÓN AL NRC', 'Se hace en SSASECT (pestaña Instructor y horas de reunión) cuando el NRC ya tiene horario y el docente está activo en SIAINST.'),
    ('cfg', 'sesion'), ('cfg', 'instructor'), ('cfg', 'siafavl1'), ('cfg', 'siafavl2'), ('cfg', 'porcentajes'),
    ('div', 'CARGA DE TRABAJO', 'Ellucian calcula la carga del docente con los NRC asignados y la compara con una regla. Reemplaza el control en Excel.'),
    ('cfg', 'siaterm'), ('cfg', 'stvwkld'), ('cfg', 'siaflrt1'), ('cfg', 'siaflrt2'), ('cfg', 'siaasgn1'), ('cfg', 'siaasgn2'),
    ('resumen',), ('close',),
]
KIND = {'conceptos': 'text', 'resumen': 'text'}


def build_conceptos(slide_path):
    t = parse(slide_path)
    set_title(t, 'CONCEPTOS CLAVE')
    spTree = t.find('.//p:spTree', NS)
    spTree.remove(shape_by_name(t, 'CuadroTexto 1'))
    sid = next_id(t)
    shapes = []
    intro = bullet_para(para('Para que un docente dicte un NRC y su carga se calcule en el sistema (en lugar de Excel), '
                             'se relacionan cuatro registros:'), sz=1600, bullet=False, spc_aft=0)
    shapes.append(textbox_xml(sid, 431320, 930000, 11329360, 520000, intro)); sid += 1
    cards = [
        ('SPAIDEN', 'Persona', [para('Datos personales del docente: ID, nombres, documento y contacto.')],
         'Se registra como cualquier persona.'),
        ('SIAINST', 'Docente', [para('Lo activa como docente desde un periodo: estatus, tipo de personal, contrato y regla de carga.')],
         'Usa las tablas de configuración.'),
        ('SSASECT', 'Asignación', [para('El docente se asigna a la sesión del NRC, en la pestaña Instructor.')],
         'Continúa «2. Programación de asignaturas».'),
        ('SIAASGN', 'Carga', [para('Suma créditos y horas de los NRC del docente y los compara con su regla de carga.')],
         'Reemplaza el control en Excel.'),
    ]
    gap, left, top = 240000, 431320, 1600000
    cw = (11329360 - 3 * gap) / 4
    for i, (code, name, items, rel) in enumerate(cards):
        x = left + i * (cw + gap)
        head = (f'<a:p><a:pPr algn="ctr"/>{run_xml(code, "g", sz=2000)}</a:p>'
                f'<a:p><a:pPr algn="ctr"/>{run_xml(name, "b", sz=1600)}</a:p>')
        shapes.append(textbox_xml(sid, x, top, cw, 780000, head, anchor='ctr', fill=PURPLE, geom='roundRect')); sid += 1
        body = ''.join(bullet_para(it, sz=1600, spc_aft=900, algn='l', bullet=False) for it in items)
        body += bullet_para(para(G(rel)), sz=1500, bullet=False, spc_aft=0, algn='l')
        shapes.append(textbox_xml(sid, x, top + 860000, cw, 2150000, body, fill='F1E7FA', geom='roundRect',
                                  insets=' lIns="137160" tIns="137160" rIns="137160" bIns="91440"')); sid += 1
    note = bullet_para(para(G('Periodo: '), 'en todas estas páginas se usa el mismo código definido en «1. Periodos académicos» '
                            '(ej. 202654 para 2026-I de Centros Empresariales).'),
                       sz=1400, bullet=False, spc_aft=0, algn='l')
    shapes.append(textbox_xml(sid, 431320, 4850000, 11329360, 560000, note, anchor='ctr', line=GREEN,
                              geom='roundRect')); sid += 1
    for s in shapes:
        spTree.append(frag(s))
    save(t, slide_path)


def main():
    kinds = [KIND.get(p[0], p[0]) for p in PLAN]
    u, paths = build_structure(os.path.join(HERE, 'b3'), kinds)
    for item, path in zip(PLAN, paths):
        kind = item[0]
        if kind == 'cfg':
            src, n, title, paras = CFG[item[1]][:4]
            extra = CFG[item[1]][4] if len(CFG[item[1]]) > 4 else {}
            build_cfg(u, path, src, n, title, paras, 'l', tag=os.path.basename(src).lower() + 'x', **extra)
        elif kind == 'div':
            build_div(path, item[1], item[2])
        elif kind == 'cover':
            build_cover(path, 'DOCENTES', 'CENTROS EMPRESARIALES',
                        'Registro del docente, asignación al NRC y carga de trabajo')
        elif kind == 'flow':
            t = parse(path)
            set_title(t, 'REGISTRAR Y ASIGNAR DOCENTES')
            save(t, path)
            set_flow_boxes(path, [
                ('Crear la persona', 'SPAIDEN'),
                ('Configurar tablas del docente', 'STVFCST, STVFSTP, STVFCNT', 1200),
                ('Registrar al docente en el periodo', 'SIAINST'),
                ('Asignar el docente al NRC', 'SSASECT'),
                ('Configurar la carga del periodo', 'SIATERM'),
                ('Definir la regla de carga', 'STVWKLD, SIAFLRT', 1300),
                ('Revisar la carga del docente', 'SIAASGN'),
            ], note=[para(G('Configuración'), ' (una vez o por periodo): tablas del docente, SIATERM, STVWKLD y SIAFLRT.'),
                     para(G('Por cada docente'), ': SPAIDEN, SIAINST, asignación en SSASECT y revisión en SIAASGN.')])
        elif kind == 'conceptos':
            build_conceptos(path)
        elif kind == 'resumen':
            build_bullets(path, 'RESUMEN', [
                para(B('Configuración'), ': STVFCST, STVFSTP, STVFCNT y STVWKLD se crean una vez; SIATERM y SIAFLRT se definen por periodo.'),
                para(B('Docente'), ': primero persona en SPAIDEN; luego activo en SIAINST desde el periodo. Los cambios posteriores se registran con Mantenimiento.'),
                para(B('Asignación'), ': en SSASECT, pestaña Instructor, con el ID o con SIAFAVL. Un solo docente principal por NRC.'),
                para(B('Carga'), ': SIAASGN compara créditos y horas con la regla de carga (O = sobrecarga, U = subcarga).'),
                para(B('Opcional'), ': grados del docente (SIAFDEG), labor no educativa (STVNIST) y reglas por contrato (SIAFLCT, SIACONA).'),
            ], sz=1700)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    finalize(u, OUT, NAME)
    print('OK', OUT)


if __name__ == '__main__':
    main()
