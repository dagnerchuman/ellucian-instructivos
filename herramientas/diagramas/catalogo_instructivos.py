"""Catálogo de los 83 instructivos de Ellucian: código corto y nombre completo, revisados a mano.

Los nombres de archivo vienen cortados («Diseñar y crear los programas acade», «Ges ingreso Cal extraord de de
pasadas a HA») y las portadas no siempre coinciden con el archivo (la 3.2.6 dice «Evaluar» y es «Aprobar»; la
10.2 de comunicaciones está en inglés). Este catálogo es la fuente única del nombre que muestran el asistente,
sus fuentes y el mapa de instructivos. El código corto es el que se cita en el proyecto («instructivo 5.3,
diap. 23»); el código de procedimiento de Ellucian (4.1.4.1.6) queda aparte para distinguir los que comparten
código corto.

Uso: python3 herramientas/diagramas/catalogo_instructivos.py   (lista el catálogo y verifica que estén los 83)
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import diapositivas  # noqa: E402

# Archivo (sin .pptx) → (código corto, nombre completo)
NOMBRES = {
    "1.1.1 Definir la estructura de los periodos académicos": ("1.1.1", "Definir la estructura de los periodos académicos"),
    "1.1.2 Programar el inicio y finalización de per acad": ("1.1.2", "Programar el inicio y la finalización de los periodos académicos"),
    "1.1.3 Diseñar y crear los programas acade": ("1.1.3", "Diseñar y crear los programas académicos"),
    "1.1.4 Diseñar y crear los cursos": ("1.1.4", "Diseñar y crear los cursos"),
    "1.1.5 Asignar prerequ, corequis y restricci": ("1.1.5", "Asignar prerrequisitos, correquisitos y restricciones"),
    "1.2.1 Crear las mallas curriculares": ("1.2.1", "Crear las mallas curriculares"),
    "1.2.2 Crear las mallas curric-Atri de curso": ("1.2.2", "Crear las mallas curriculares con atributos de curso"),
    "1.2.3 Asignar equivalencias": ("1.2.3", "Asignar equivalencias"),
    "1.3.1 Actualizar las mallas curriculares": ("1.3.1", "Actualizar las mallas curriculares"),
    "3.1.1 Procedimiento Gestionar Solicitudes de Admisión": ("3.1.1", "Gestionar las solicitudes de admisión"),
    "3.2.1 Procedimiento Crear Solicitudes de Admisión": ("3.2.1", "Crear solicitudes de admisión"),
    "3.2.2 Procedimiento Validar los requisitos de admisión": ("3.2.2", "Validar los requisitos de admisión"),
    "3.2.3 Procedimiento Validar los documentos suplementarios": ("3.2.3", "Validar los documentos suplementarios"),
    "3.2.4 Procedimiento Evaluar la solicitud de admisión": ("3.2.4", "Evaluar la solicitud de admisión"),
    "3.2.6 Procedimiento Aprobar solicitud de admisión": ("3.2.6", "Aprobar la solicitud de admisión"),
    "3.2.7 Procedimiento Gestionar Reingresos": ("3.2.7", "Gestionar los reingresos"),
    "3.3.1 Gestionar homologación y convalidación": ("3.3.1", "Gestionar la homologación y la convalidación"),
    "4.1.1 Actualizar estado del estudiante": ("4.1.1", "Actualizar el estado del estudiante"),
    "4.1.2 Actualizar características del estudiante": ("4.1.2", "Actualizar las características del estudiante"),
    "4.1.3 Asignar o actualizar retenciones programa": ("4.1.3", "Asignar o actualizar retenciones del programa"),
    "4.3.1 Configuracion de Solicitudes de Servicio": ("4.3.1", "Configurar las solicitudes de servicio"),
    "4.3.2 Gestionar las solicitudes de servicios": ("4.3.2", "Gestionar las solicitudes de servicio de los estudiantes"),
    "5.1.1 Instructivo - Gestionar persona natural": ("5.1.1", "Gestionar persona natural"),
    "5.1.1 Instructivo - Gestionar persona natural_V2": ("5.1.1", "Gestionar persona natural (versión 2)"),
    "5.1.2 Instructivo - Gestionar persona juridica": ("5.1.2", "Gestionar persona jurídica"),
    "5.2.1 Instructivo - Gestionar retenciones de personas": ("5.2.1", "Gestionar retenciones de personas"),
    "5.2.2 Instructivo - Asignar o actualizar retenciones": ("5.2.2", "Asignar o actualizar retenciones"),
    "5.2_4.1.4.1 Instructivo - Información de Docentes": ("5.2", "Gestionar la información de los docentes"),
    "5.2_4.1.5.1 Instructivo - Carga de Trabajo Docente": ("5.2", "Gestionar la carga de trabajo docente"),
    "5.3_4.1.4.1.6_Instructivo_Registrar la oferta horaria de los cursos": ("5.3", "Registrar la oferta horaria de los cursos"),
    "5.3_4.1.4.1.8_Instructivo_Crear Listas Cruzadas": ("5.3", "Crear listas cruzadas"),
    "5.3_4.1.4.1.9_Instructivo_Crear Ligas": ("5.3", "Crear ligas"),
    "5.3_4.2.4.1.6_Instructivo_Gestionar los espacios físicos": ("5.3", "Gestionar los espacios físicos"),
    "5.4_4.1.4.1.12 Instructivo - Ejecu.la inscrip.de cursos por backoffice": ("5.4", "Ejecutar la inscripción de cursos por backoffice"),
    "5.4_4.1.4.1.14 Instructivo - Inscripción de cursos por Lista de Espera": ("5.4", "Ejecutar la inscripción de cursos por lista de espera"),
    "5.4_4.1.4.1.15 Instructivo - Gestionar los sobrepasos de inscripción": ("5.4", "Gestionar los sobrepasos de inscripción"),
    "5.4_4.1.4.1.16 Instructivo -  Gestionar retiro de cursos": ("5.4", "Gestionar el retiro de cursos"),
    "5.4_4.1.4.1.6 Instructivo - Ejecutar Proyección Académica": ("5.4", "Ejecutar la proyección académica"),
    "5.4_4.1.4.1.7 Instructivo - Ejecutar la planificación de cursos": ("5.4", "Ejecutar la planificación de cursos"),
    "6.1.1 Asignar Syllabus": ("6.1.1", "Asignar el syllabus (sílabo)"),
    "6.1.2 Asi atribu y propie especifi": ("6.1.2", "Asignar atributos y propiedades específicas"),
    "6.1.3 Asignar bibliografia": ("6.1.3", "Asignar bibliografía"),
    "6.2.1 Asig Esp Fisicos": ("6.2.1", "Asignar espacios físicos"),
    "6.2.1 Asignar Docentes": ("6.2.1", "Asignar docentes"),
    "6.2.3 Recursos Pedagógicos": ("6.2.3", "Asignar recursos pedagógicos"),
    "6.2.4 Asi Rec Vir-eLearning": ("6.2.4", "Asignar recursos virtuales (eLearning)"),
    "6.2.5 Gestiona la evaluación docente": ("6.2.5", "Gestionar la evaluación docente"),
    "7.1.0 Usar Componente Asistencia": ("7.1.0", "Usar el componente de asistencia"),
    "7.1.1 Gestionar la asistencia a clases": ("7.1.1", "Gestionar la asistencia a clases"),
    "7.1.10 Generar Selecciones de Población": ("7.1.10", "Generar selecciones de población"),
    "7.1.11 Gestionar Textos": ("7.1.11", "Gestionar textos"),
    "7.1.2 Revisar la asistencia a clases": ("7.1.2", "Revisar la asistencia a clases"),
    "7.1.3 Configurar escalas de calificación": ("7.1.3", "Configurar escalas de calificación"),
    "7.1.4 Ingresar calificaci autoservicio": ("7.1.4", "Ingresar calificaciones por Autoservicio"),
    "7.1.5 Revisar las calificaciones por autoser": ("7.1.5", "Revisar las calificaciones por Autoservicio"),
    "7.1.6 Ingresar calificac backoffice": ("7.1.6", "Ingresar calificaciones por backoffice"),
    "7.1.7 Gestionar calificaciones incompletas": ("7.1.7", "Gestionar calificaciones incompletas"),
    "7.1.8 Ges ingreso Cal extraord de de pasadas a HA": ("7.1.8", "Ingresar calificaciones extraordinarias después del pase a historia"),
    "7.1.9 Ejecutar procesos de cierre de per acadé": ("7.1.9", "Ejecutar los procesos de cierre del periodo académico"),
    "7.2.1 Gestionar la historia académica del estudiante": ("7.2.1", "Gestionar la historia académica del estudiante"),
    "7.2.2 Gestionar el promedio de estudiantes": ("7.2.2", "Gestionar el promedio de los estudiantes"),
    "7.2.3 Gestionar el estado académico": ("7.2.3", "Gestionar el estado académico"),
    "7.2.4 Ejecución del CAPP": ("7.2.4", "Ejecutar el CAPP"),
    "08_4.1.4.1.5 Inst. Validar el cumplimiento de los requisitos de graduación": ("8.1", "Validar el cumplimiento de los requisitos de graduación"),
    "08_4.1.4.2.6 Inst. Gestionar Solicitudes de Graduación": ("8.1", "Gestionar las solicitudes de graduación"),
    "08_4.2.4.1.6 Inst. Gestión de Eventos y ceremon.  de grado": ("8.2", "Gestionar los eventos y ceremonias de grado"),
    "08_4.3.4.1.6 Inst. Gestionar otros requisitos académicos": ("8.3", "Gestionar otros requisitos académicos (no cursos)"),
    "08_4.4.4.1.5 Inst. Gestionar el otorgam. y regist. de grado": ("8.4", "Gestionar el otorgamiento y el registro del grado"),
    "9.1.1 Definición y gestión de la asesoría de estudiantes": ("9.1.1", "Definir y gestionar la asesoría de estudiantes"),
    "9.2.1 Gestión Exp Formativa en Entor Laborales": ("9.2.1", "Gestionar las experiencias formativas en entornos laborales (prácticas)"),
    "10_4.1.4.1.6 Inst. Registrar y mantener información médica": ("10.1", "Registrar y mantener la información médica"),
    "10_4.2.4.1.6 Inst. Definir y Diseñar Eventos": ("10.2", "Definir y diseñar eventos"),
    "10_4.2.4.2.6 Inst. Gestionar encuestas generales hacia los estudiantes": ("10.2", "Gestionar encuestas generales hacia los estudiantes"),
    "10_4.2.4.3.5 Inst. Programar Comunicaciones Masivas": ("10.2", "Programar comunicaciones masivas"),
    "10_4.2.4.4.5 Inst. Configuración de Autoservicio": ("10.2", "Configurar el Autoservicio"),
    "11.1.1 - Gest. Config Cuenta Corriente": ("11.1.1", "Gestionar los conceptos de configuración de la cuenta corriente"),
    "11.1.2 -  Gestionar los beneficios": ("11.1.2", "Gestionar los beneficios"),
    "11.1.3 - Gestionar los planes de pago": ("11.1.3", "Gestionar los planes de pago"),
    "11.2.1 - Gestionar la matrícula": ("11.2.1", "Gestionar la matrícula (cargos)"),
    "11.2.2 - Gestionar los pagos": ("11.2.2", "Gestionar los pagos"),
    "11.2.3  Gestionar los documentos de venta": ("11.2.3", "Gestionar los documentos de venta"),
    "11.3.1 Gestionar la cuenta corriente": ("11.3.1", "Gestionar la cuenta corriente"),
    "11.3.2 -Gestionar la generación de transacciones": ("11.3.2", "Gestionar la generación de transacciones"),
}


def procedimiento(archivo):
    """Código de procedimiento de Ellucian del archivo («5.3_4.1.4.1.6_…» → «4.1.4.1.6»), o ''."""
    m = re.match(r"^\d+(?:\.\d+)?_(\d+(?:\.\d+)+)", archivo)
    return m.group(1) if m else ""


def catalogo():
    """{id del visor: {codigo, nombre, etiqueta, procedimiento, capacidad, path, diapositivas}} de los 83."""
    salida, faltan = {}, []
    indice = diapositivas.leer_indice()
    for id_, info in diapositivas.presentaciones().items():
        archivo = re.sub(r"\.pptx$", "", info["name"])
        if archivo not in NOMBRES:
            faltan.append(archivo)
            continue
        codigo, nombre = NOMBRES[archivo]
        salida[id_] = {
            "codigo": codigo,
            "nombre": nombre,
            "etiqueta": f"Instructivo {codigo} · {nombre}",
            "procedimiento": procedimiento(archivo),
            "capacidad": int(codigo.split(".")[0]),
            "path": info["path"],
            "diapositivas": (indice.get(id_) or {}).get("n") or 0,
        }
    if faltan:
        raise KeyError("Instructivos sin nombre en el catálogo: " + "; ".join(faltan))
    return salida


if __name__ == "__main__":
    cat = catalogo()
    for id_, c in sorted(cat.items(), key=lambda kv: [int(x) for x in re.findall(r"\d+", kv[1]["codigo"])]):
        print(f"{c['etiqueta']}" + (f"  ({c['procedimiento']})" if c["procedimiento"] else ""))
    print(f"\n{len(cat)} instructivos en el catálogo")
