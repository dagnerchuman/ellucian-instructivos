# -*- coding: utf-8 -*-
"""4. Admisión: registrar al participante como estudiante con la captura rápida SAAQUIK (resumido)."""
import os
from ussdeck import *

SRC = os.path.normpath(os.path.join(HERE, '..', 'src4'))
# Q 3.2.1 Crear solicitudes, P 5.1.1 Persona natural V2, C 3.1.1 Gestionar solicitudes, S 4.1.1 Estado del estudiante
SQ, SP, SC, SS = (os.path.join(SRC, x) for x in ('Q', 'P', 'C', 'S'))
NAME = '4. ADMISIÓN - REGISTRO DEL PARTICIPANTE COMO ESTUDIANTE'
OUT = os.path.join(HERE, 'entregables', NAME + '.pptx')

CFG = {
    # ---------------- configuraciones
    'stvadmt': (SC, 11, 'TIPO DE ADMISIÓN - STVADMT', [
        para('Define los ', G('tipos de admisión'), ' que se eligen en SAAQUIK y SAAADMS (ej. ', B('DIRECTA'), ').'),
        para(G('1. '), 'Ingrese el ', G('Código'), ' del tipo de admisión.'),
        para(G('2. '), 'Ingrese la ', G('Descripción'), ' y ', B('guarde'), '.'),
    ]),
    'stvstyp': (SC, 12, 'TIPO DE ALUMNO - STVSTYP', [
        para('Define los ', G('tipos de alumno'), ' (ej. ', B('N'), ' Nuevo). Se eligen en SAAQUIK y quedan en SGASTDN.'),
        para(G('1. '), 'Ingrese el ', G('Código'), '.  ', G('2. '), 'Ingrese la ', G('Descripción'), '.  ',
             G('3. '), B('Guarde'), '.'),
    ], {'callout_at': (900000, 4500000, 5500000)}),
    'stvapdc': (SC, 25, 'DECISIÓN DE ADMISIÓN - STVAPDC', [
        para('Define las ', G('decisiones de admisión'), '. Las casillas marcadas indican qué hace cada decisión:'),
        para(G('Aceptación de institución'), ' o ', G('de solicitante'), ': ', B('crea el registro de estudiante'),
             ' (SGASTDN).'),
        para(G('Decisión significativa'), ': pasa la solicitud a estatus ', B('D'), ' (decisión tomada); aún no crea estudiante.'),
        para(G('Rechazado'), ' o ', G('Solicitud inactiva'), ': no deja al participante como estudiante.'),
        para('En SAAQUIK use una decisión con ', B('aceptación'), '.'),
    ]),
    # ---------------- persona
    'goamtch1': (SP, 30, 'BUSCAR PERSONA - GOAMTCH', [
        para('En ', G('SPAIDEN'), ' presione ', G('Insertar (+)'), ': se abre ', G('GOAMTCH'), ' con el origen ',
             B('PNATURAL'), '; presione ', B('Ir'), '.'),
        para(G('1. '), 'Ingrese ', B('apellidos'), ' (separados por /), ', B('nombre'), ' y ', B('número de documento'),
             '. Fecha de nacimiento, sexo, teléfono y correo son opcionales.'),
        para(G('2. '), 'Presione ', G('Marcar-Duplicar'), ': Banner busca si la persona ya existe.'),
    ], {'relabel': {'5': '1', '6': '2'}}),
    'goamtch2': (SP, 31, 'BUSCAR PERSONA - GOAMTCH', [
        para(G('3. '), 'En ', B('Coincidencia'), ' se muestran las personas que se parecen a los datos ingresados.'),
        para(G('4. '), 'Elija: ', G('Seleccionar ID'), ' (ya existe, se usa ese ID), ', G('Actualizar ID'),
             ' (ya existe y se actualizan sus datos) o ', G('Crear nuevo'), ' (no existe: se genera el ID en SPAIDEN).'),
        para('Con ese ', B('ID'), ' continúe en SAAQUIK.'),
    ], {'relabel': {'7': '3', '8': '4'}}),
    # ---------------- admisión rápida
    'quik1': (SQ, 22, 'ADMISIÓN RÁPIDA - SAAQUIK', [
        para(G('1. '), 'Ingrese el ', G('ID'), ' de la persona (el encontrado o creado en GOAMTCH).'),
        para(G('2. '), 'Ingrese el ', G('Periodo'), ' de admisión (ej. 202654, ver «1. Periodos académicos»).'),
        para(G('3. '), 'Ingrese el ', G('Nivel'), ' y presione ', B('Ir'), '.'),
        para('Si la persona no existe, también puede crearla aquí con ', B('+'), ' junto al ID.'),
    ]),
    'quik2': (SQ, 23, 'ADMISIÓN RÁPIDA - SAAQUIK', [
        para('En el bloque ', G('Detalles'), ' ingrese los campos obligatorios:'),
        para(G('1. '), G('Tipo de alumno'), ' (STVSTYP).  ', G('2. '), G('Estatus de alumno'), '.  ',
             G('3. '), G('Residencia'), '.'),
        para('Con estos datos se crea el ', B('registro de estudiante en SGASTDN'), '.'),
    ]),
    'quik3': (SQ, 24, 'ADMISIÓN RÁPIDA - SAAQUIK', [
        para('En el bloque ', G('Información de solicitud y reclutamiento'), ':'),
        para(G('1. '), 'Marque ', G('Crear registro de solicitud'), '.'),
        para(G('2. '), G('Tipo de admisión'), ' (STVADMT).  ', G('3. '), G('Estatus de solicitud'), '.  ',
             G('4. '), G('Decisión de admisión'), ' (STVAPDC).'),
        para('Con estos datos se crea la ', B('solicitud de admisión en SAAADMS'), '.'),
    ]),
    'quik4': (SQ, 25, 'ADMISIÓN RÁPIDA - SAAQUIK', [
        para(G('1. '), 'En el bloque ', G('Currículo'), ' elija el ', G('Programa'),
             ': Banner completa los datos de su regla de currículo (escuela, grado y campo de estudio).'),
        para(G('2. '), B('Guarde'), ' el registro.'),
    ]),
    'quik5': (SQ, 26, 'ADMISIÓN RÁPIDA - DIRECCIÓN', [
        para('En la pestaña ', G('Dirección'), ' registre una o más direcciones del participante; se muestran en SPAIDEN.'),
        para(G('1. '), 'Elija el ', G('Tipo de dirección'), ', complete los datos y ', B('guarde'), '.'),
    ]),
    'quik6': (SQ, 27, 'ADMISIÓN RÁPIDA - BIOGRÁFICA', [
        para('En la pestaña ', G('Biográfica'), ' registre fecha de nacimiento, sexo legal, estado civil y ciudadanía, '
             'entre otros; se muestran en SPAIDEN.'),
        para(B('Guarde'), ' la información.'),
    ]),
    # ---------------- completar y verificar
    'tel': (SP, 39, 'TELÉFONO - SPAIDEN', [
        para('Complete el contacto en ', G('SPAIDEN'), ', pestaña ', G('Teléfono'), ':'),
        para(G('1. '), G('Tipo de teléfono'), '.  ', G('2. '), G('Número'), ' (y anexo, si aplica).'),
        para(G('3. '), 'Indique si es el teléfono ', B('principal'), ' y ', B('guarde'), '.'),
    ]),
    'correo': (SP, 42, 'CORREO ELECTRÓNICO - SPAIDEN', [
        para('En la pestaña ', G('Correo electrónico'), ':'),
        para(G('1. '), G('Tipo de correo'), ' (personal o institucional).  ', G('2. '), G('Dirección de correo'), '.'),
        para(G('3. '), 'Marque como ', B('Preferido'), ' el correo ', B('institucional'), ' y ', B('guarde'), '.'),
    ]),
    'saaadms': (SQ, 11, 'VERIFICAR SOLICITUD - SAAADMS', [
        para(G('1. '), 'Ingrese el ', G('ID'), '.  ', G('2. '), 'Ingrese el ', G('Periodo'), '.  ',
             G('3. '), 'Presione ', G('Ir'), '.'),
        para('Revise la solicitud que creó SAAQUIK: tipo de admisión, programa, estatus y decisión. '
             'Aquí también se corrige.'),
    ]),
    'sgastdn': (SS, 15, 'VERIFICAR ESTUDIANTE - SGASTDN', [
        para('Ingrese el ', G('ID'), ' y el ', G('Periodo'), '; presione ', G('Ir'), '.'),
        para(G('1. '), 'En la pestaña ', G('Estudiante'), ' revise el ', B('estatus'), ', el tipo de alumno y el ',
             B('programa'), ' en el resumen de currículo.'),
        para('Si todo está correcto, el participante ya puede ', B('inscribirse en los NRC'), ' (SFAREGS).'),
    ], {'relabel': {'4': '1'}, 'skip_marks': ('5',)}),
}

PLAN = [
    ('cover',), ('flow',), ('conceptos',),
    ('div', 'CONFIGURACIONES', 'Códigos que se eligen en SAAQUIK. Se crean una sola vez; verifique que existan los de Centros Empresariales.'),
    ('cfg', 'stvadmt'), ('cfg', 'stvstyp'), ('cfg', 'stvapdc'),
    ('div', 'BUSCAR O CREAR LA PERSONA', 'Antes de registrar a un participante, busque si ya existe en Banner (exalumno, docente o postulante) para no duplicarlo.'),
    ('cfg', 'goamtch1'), ('cfg', 'goamtch2'),
    ('div', 'ADMISIÓN RÁPIDA', 'En una sola página, SAAQUIK, se crea la solicitud de admisión (SAAADMS) y el registro de estudiante (SGASTDN).'),
    ('cfg', 'quik1'), ('cfg', 'quik2'), ('cfg', 'quik3'), ('cfg', 'quik4'), ('cfg', 'quik5'), ('cfg', 'quik6'),
    ('div', 'COMPLETAR Y VERIFICAR', 'Datos de contacto en SPAIDEN y revisión de la solicitud y del estudiante antes de la inscripción.'),
    ('cfg', 'tel'), ('cfg', 'correo'), ('cfg', 'saaadms'), ('cfg', 'sgastdn'),
    ('resumen',), ('close',),
]
KIND = {'conceptos': 'text', 'resumen': 'text'}


def build_cards(slide_path, title, intro, cards, note):
    """Diapositiva de conceptos: introducción, cuatro tarjetas (código, nombre, texto, relación) y nota."""
    t = parse(slide_path)
    set_title(t, title)
    spTree = t.find('.//p:spTree', NS)
    spTree.remove(shape_by_name(t, 'CuadroTexto 1'))
    sid = next_id(t)
    shapes = [textbox_xml(sid, 431320, 930000, 11329360, 520000,
                          bullet_para(intro, sz=1600, bullet=False, spc_aft=0))]
    sid += 1
    gap, left, top = 240000, 431320, 1600000
    cw = (11329360 - 3 * gap) / 4
    for i, (code, name, text, rel) in enumerate(cards):
        x = left + i * (cw + gap)
        head = (f'<a:p><a:pPr algn="ctr"/>{run_xml(code, "g", sz=2000)}</a:p>'
                f'<a:p><a:pPr algn="ctr"/>{run_xml(name, "b", sz=1600)}</a:p>')
        shapes.append(textbox_xml(sid, x, top, cw, 780000, head, anchor='ctr', fill=PURPLE, geom='roundRect')); sid += 1
        body = bullet_para(text, sz=1600, spc_aft=900, algn='l', bullet=False)
        body += bullet_para(para(G(rel)), sz=1500, bullet=False, spc_aft=0, algn='l')
        shapes.append(textbox_xml(sid, x, top + 860000, cw, 2150000, body, fill='F1E7FA', geom='roundRect',
                                  insets=' lIns="137160" tIns="137160" rIns="137160" bIns="91440"')); sid += 1
    shapes.append(textbox_xml(sid, 431320, 4850000, 11329360, 560000,
                              bullet_para(note, sz=1400, bullet=False, spc_aft=0, algn='l'),
                              anchor='ctr', line=GREEN, geom='roundRect'))
    for s in shapes:
        spTree.append(frag(s))
    save(t, slide_path)


def main():
    kinds = [KIND.get(p[0], p[0]) for p in PLAN]
    u, paths = build_structure(os.path.join(HERE, 'b4'), kinds)
    for item, path in zip(PLAN, paths):
        kind = item[0]
        if kind == 'cfg':
            src, n, title, paras = CFG[item[1]][:4]
            extra = CFG[item[1]][4] if len(CFG[item[1]]) > 4 else {}
            build_cfg(u, path, src, n, title, paras, 'l', tag='adm' + os.path.basename(src).lower(), **extra)
        elif kind == 'div':
            build_div(path, item[1], item[2])
        elif kind == 'cover':
            build_cover(path, 'ADMISIÓN', 'CENTROS EMPRESARIALES',
                        'Registro del participante como estudiante')
        elif kind == 'flow':
            t = parse(path)
            set_title(t, 'REGISTRAR AL PARTICIPANTE')
            save(t, path)
            set_flow_boxes(path, [
                ('Buscar o crear la persona', 'GOAMTCH, SPAIDEN', 1300),
                ('Periodo y nivel de admisión', 'SAAQUIK'),
                ('Tipo y estatus de alumno', 'SAAQUIK'),
                ('Solicitud y decisión', 'SAAQUIK'),
                ('Programa del participante', 'SAAQUIK'),
                ('Completar teléfono y correo', 'SPAIDEN'),
                ('Verificar solicitud y estudiante', 'SAAADMS, SGASTDN', 1200),
            ], note=[para(G('Configuración'), ' (una vez): tipos de admisión y de alumno, y decisiones.'),
                     para(G('Por cada participante'), ': buscar la persona, SAAQUIK, contacto en SPAIDEN y verificación.')],
                highlight=(1, 2, 3, 4))
        elif kind == 'conceptos':
            build_cards(path, 'CONCEPTOS CLAVE',
                        para('Para que un participante pueda inscribirse en un NRC, Banner relaciona cuatro registros:'),
                        [('SPAIDEN', 'Persona', para('Datos personales: ID, nombres, documento, dirección, teléfono y correo.'),
                          'Se busca antes de crear (GOAMTCH).'),
                         ('SAAQUIK', 'Admisión rápida', para('Una sola página para periodo, programa, tipo de alumno y decisión.'),
                          'Crea SAAADMS y SGASTDN.'),
                         ('SAAADMS', 'Solicitud', para('Solicitud de admisión: tipo, programa, estatus y decisión.'),
                          'Se revisa o corrige aquí.'),
                         ('SGASTDN', 'Estudiante', para('Estatus, tipo de alumno y programa del estudiante por periodo.'),
                          'Requisito para inscribir (SFAREGS).')],
                        para(G('Pregrado: '), 'las solicitudes de postulantes llegan a Banner por interfaz. ',
                             G('Registro manual: '), 'SAAQUIK lo resuelve en una sola página.'))
        elif kind == 'resumen':
            build_bullets(path, 'RESUMEN', [
                para(B('Configuración'), ': STVADMT, STVSTYP y STVAPDC (con STVRESD y STVAPST) se crean una vez. '
                     'La decisión debe tener «aceptación» para crear al estudiante.'),
                para(B('Persona'), ': búsquela en GOAMTCH antes de crearla; si ya existe, use su ID.'),
                para(B('Admisión'), ': SAAQUIK registra la solicitud (SAAADMS) y el estudiante (SGASTDN), '
                     'con dirección y datos biográficos.'),
                para(B('Contacto'), ': teléfono y correo preferido (institucional) en SPAIDEN.'),
                para(B('Verificación'), ': SAAADMS y SGASTDN. Luego el participante puede inscribirse en los NRC (SFAREGS).'),
                para(B('Opcional'), ': SAADCRV cambia la decisión de una solicitud; SAAMAPP actualiza varias solicitudes a la vez.'),
            ], sz=1600)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    finalize(u, OUT, NAME)
    print('OK', OUT)


if __name__ == '__main__':
    main()
