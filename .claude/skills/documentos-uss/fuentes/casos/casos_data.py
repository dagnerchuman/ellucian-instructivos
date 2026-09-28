# -*- coding: utf-8 -*-
"""Datos de las casuísticas (compartidos por el PDF y el PPTX). Citas verificadas con buscar_instructivos.py."""

TITULO = 'Casuísticas para las pruebas integrales'
SUBTITULO = 'Estudiantes y docentes: qué hace Banner en cada caso y qué queda fuera del sistema'

# Muestra que ya se propuso en «VALIDACIÓN DE LA MIGRACIÓN» (25/09/2026), por programa de cada centro
MUESTRA = [('Participante regular, curso en progreso', 3), ('Participante nuevo (primer nivel, ej. BASIC I)', 2),
           ('Niveles avanzados (ej. INTERMEDIATE)', 3), ('Estudiante de pregrado USS que lleva el centro', 2),
           ('Cambio de programa o de curso', 1), ('Retirado o reincorporado', 1), ('Con saldo pendiente', 2),
           ('Culminó el programa (certificado)', 1), ('Curso que empezó en SEUSS y termina en Banner', 1)]
ESCENARIOS = ['Curso de SEUSS que queda en un periodo equivocado o se pierde', 'Nivel aprobado que no se reconoce como prerrequisito',
              'Pregrado que lleva Idiomas: dos programas activos', 'Grupo que empezó en SEUSS y no aparece en Banner',
              'Retirado que aparece activo', 'Deuda sin retención', 'Misma persona con dos ID', 'Docente de pregrado que dicta en el centro']

FAMILIAS = {'D': ('Docente', 'doc'), 'E': ('Estudiante con dificultades', 'est'), 'Q': ('Queja y sanción', 'que')}

# Cada caso: id, título, situación, pasos en Banner [(texto, cita)], resultado esperado, fuera de Banner, ejemplo en centros, pruebas
CASOS = [
    dict(id='D-1', titulo='El docente fallece a mitad del curso',
         situacion='En un grupo de la maestría en Educación falleció el docente. El grupo debe seguir con otro docente (reunión del 28/09).',
         pasos=[('En SPAIDEN, pestaña Biográfica: fecha de fallecimiento y casilla «Fallecido».', '5.1.1, diap. 40'),
                ('En SIAINST: cambiar el estatus del docente (códigos en STVFCST).', '5.2 Información de docentes, diap. 10 y 18'),
                ('En SSASECT: asignar al nuevo docente como **principal**, con su % de responsabilidad y de sesión.', '6.2.1, diap. 19 y 21'),
                ('Si PRIMINSTR está en «Y», solo el principal registra notas.', '7.1.4, diap. 24')],
         resultado='El NRC sigue con sus estudiantes y notas; el reemplazo registra lo que falta.',
         fuera='Los trámites con la familia y el contrato (Gobierno de Personas).',
         centros='Docente de BASIC II del grupo I06 de Inglés.',
         prueba=['El reemplazo registra notas en el NRC.', 'El NRC se cierra y la nota pasa a la historia académica.']),
    dict(id='D-2', titulo='«Profesor, hasta aquí no puede dictar clases»',
         situacion='La USS decide que un docente deja de dictar un NRC a mitad del curso.',
         pasos=[('Registros Académicos lo quita del NRC y asigna al reemplazo como **principal** en SSASECT.', '6.2.1, diap. 19 y 21'),
                ('Con la regla de acceso por relación, solo ve el NRC en el autoservicio el docente asignado: el anterior deja de '
                 'registrar notas y asistencia.', '7.1.4, diap. 21'),
                ('Si no volverá a dictar: cambiar su estatus en SIAINST.', '5.2 Información de docentes, diap. 18'),
                ('La carga del reemplazo se actualiza en SIAASGN.', '5.2 Carga de trabajo docente, diap. 18')],
         resultado='El docente separado ya no accede al NRC; el reemplazo sí.',
         fuera='La decisión y el proceso laboral o disciplinario con el docente: los hace Gobierno de Personas, no Banner Student.',
         centros='Docente de un NRC de Excel Básico (nombre de ejemplo) del grupo X06 de Informática.',
         prueba=['El docente separado ya no ve el NRC en el autoservicio.', 'El reemplazo sí lo ve y registra notas y asistencia.']),
    dict(id='E-1', titulo='Estudiante con problemas y el docente no lo apoya',
         situacion='Un estudiante tiene dificultades (notas bajas, faltas) y el docente no gestiona estrategias para ayudarlo.',
         pasos=[('El docente registra asistencia y notas en el autoservicio; el estudiante ve sus asistencias.', '7.1.1 y 7.1.4; 7.1.2, diap. 16'),
                ('Tutor asignado en SGAADVR; ve el perfil del estudiante según las reglas de SOAFACS.', '9.1.1, diap. 9, 10, 27 y 36'),
                ('El seguimiento se registra en SPACMNT, por tipo y fecha. Hoy la USS no tiene tipos de comentario definidos.',
                 '5.1.1, diap. 46'),
                ('Al cierre, el estado académico se aplica por promedio y horas (regla de dificultad académica).', '7.2.3, diap. 5 y 19'),
                ('Se puede enviar una comunicación a esa población con BCM.', '10.2 Comunicaciones masivas, diap. 102')],
         resultado='El estudiante queda identificado y con un registro de su seguimiento.',
         fuera='Banner no crea ni exige estrategias pedagógicas y no evalúa si el docente las aplica. Los instructivos no traen alertas '
               'tempranas: la estrategia la define la USS (tutoría, dirección académica).',
         centros='Participante de BASIC II con faltas seguidas en el grupo I06 de Inglés.',
         prueba=['El tutor ve las notas y la asistencia del estudiante.', 'Queda un comentario de seguimiento en SPACMNT.']),
    dict(id='E-2', titulo='Estudiante que falta mucho',
         situacion='Un estudiante tiene buenas notas pero llega a 65% de asistencia.',
         pasos=[('El plan de evaluación del NRC incluye el componente de asistencia ATTRGRD: peso 0 y «debe pasar».',
                 '7.1.0, diap. 29; 7.1.4, diap. 55'),
                ('La escala del componente fija el mínimo; en el ejemplo del instructivo es 70% y debajo sale INH.', '7.1.0, diap. 21 a 23')],
         resultado='Desaprueba por asistencia aunque sus notas le alcancen.',
         fuera='Definir el mínimo de asistencia de cada centro (política de la USS).',
         centros='Participante de un grupo de Emprendimiento (P05).',
         prueba=['Con 65% de asistencia, el curso sale desaprobado.']),
    dict(id='Q-1', titulo='«El profesor me desprecia»: queja del estudiante',
         situacion='Un estudiante quiere quejarse del trato de un docente.',
         pasos=[('Canal en Banner: una **solicitud de servicio**. El estudiante la presenta por autoservicio y puede agregar '
                 'comentarios mientras no esté cerrada.', '4.3.2, diap. 10 y 12'),
                ('El área la atiende en SVASVPR: estado, fecha estimada y comentarios internos que el estudiante no ve.',
                 '4.3.2, diap. 18 y 20'),
                ('Antes hay que crear el servicio: categoría (SVVSRCA), servicio (SVVSRVC), estados (SVVSRVS), roles (STVRADM) y a '
                 'quién va dirigido.', '4.3.1, diap. 10 a 19'),
                ('Aparte, la encuesta de evaluación docente da indicadores del docente por NRC; no es una queja.', '6.2.5, diap. 5 y 68')],
         resultado='La queja queda registrada con número, estado y seguimiento.',
         fuera='Los instructivos no traen un servicio de «queja contra un docente»: hay que diseñarlo. La investigación la hace la USS.',
         centros='Participante de un grupo de Emprendimiento (P05).',
         prueba=['El estudiante registra la queja y ve su número y estado.', 'Solo el área autorizada la ve y la atiende.']),
    dict(id='Q-2', titulo='¿La denuncia llega a Gobierno de Personas?',
         situacion='El estudiante quiere denunciar al docente ante Gobierno de Personas. ¿Eso lo genera Ellucian?',
         pasos=[('**Banner Student no genera ni envía la denuncia** a Gobierno de Personas por sí solo. Los instructivos de Banner '
                 'Student no cubren los procesos de personal.', 'capacidades 1 a 11'),
                ('Lo que sí hace: registra la solicitud de servicio y define para quién está disponible (tipo de persona o rol).',
                 '4.3.1, diap. 18, 19 y 22'),
                ('Si Gobierno de Personas debe atenderla, hay que definir con Ellucian cómo se le asigna.', 'duda para Ellucian')],
         resultado='La denuncia queda registrada en Banner; el proceso contra el docente sigue fuera de Banner Student.',
         fuera='La investigación, la sanción al docente y la protección del estudiante (Gobierno de Personas).',
         centros='Aplica igual a los tres centros.',
         prueba=['La solicitud llega a quien debe atenderla y no a otros.']),
    dict(id='Q-3', titulo='Estudiante sancionado por una falta disciplinaria',
         situacion='La USS sanciona a un estudiante: suspensión temporal o expulsión.',
         pasos=[('Estado del plan de estudios en SGASTDN: «Suspendido» (temporal) o «Expulsado» (definitivo). '
                 'Ninguno permite inscripción.', '3.2.7, diap. 9 y 42'),
                ('Retención en SOAHOLD (tipos en STVHLDD): puede impedir inscribirse y presentar solicitudes. No se borra: se le '
                 'pone fecha de fin.', '5.2.1, diap. 19; 4.3.1, diap. 21'),
                ('Para egresar no debe tener retenciones, como las sanciones disciplinarias.', '08_4.4.4.1.5, diap. 42')],
         resultado='Banner no lo deja inscribirse mientras dure la sanción.',
         fuera='La decisión disciplinaria (comité o tribunal de la USS).',
         centros='Aplica igual a los tres centros.',
         prueba=['Con la retención activa, la inscripción da error.', 'Al vencer la retención, puede inscribirse.']),
]

SI_NO = (
    ['Registra quién dicta cada NRC y cambia al docente principal.', 'Controla quién ve y registra notas y asistencia.',
     'Muestra notas y asistencia al tutor y al estudiante.', 'Aplica el estado académico por promedio.',
     'Recibe quejas como solicitudes de servicio, con estado y seguimiento.', 'Bloquea la inscripción con estados y retenciones.'],
    ['Decidir separar a un docente o sancionarlo.', 'Crear o exigir estrategias pedagógicas.',
     'Investigar una queja o denuncia.', 'Enviar la denuncia a Gobierno de Personas por sí solo.',
     'Alertas tempranas: no aparecen en los instructivos.', 'Proteger al estudiante que denuncia (política de la USS).'])

DUDAS_E = [
    '¿Las solicitudes de servicio pueden avisar por correo o asignarse a Gobierno de Personas? ¿Hay integración con su sistema?',
    '¿Cómo se define quién atiende cada servicio y quién puede ver una queja (confidencialidad)?',
    '¿Banner tiene alertas tempranas por faltas o notas bajas, o solo reportes y comunicaciones?',
    'Reemplazo o separación de un docente: ¿el anterior se deja en el NRC (historial y pago) o se elimina? (E14)',
]
DUDAS_U = [
    '¿Qué área recibe las quejas contra docentes y cómo se protege al estudiante?',
    '¿Se crea en Banner un servicio de «queja o denuncia», o se atiende fuera?',
    '¿Qué tipos de comentario de seguimiento (SPACMNT) usarán los tutores?',
    '¿Quién decide separar a un docente y cómo se avisa a Registros Académicos?',
    '¿Qué asistencia mínima y qué estados académicos aplican a los centros? (U03)',
]
