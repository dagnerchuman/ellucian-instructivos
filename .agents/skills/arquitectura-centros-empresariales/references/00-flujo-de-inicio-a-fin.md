# Flujo de inicio a fin en Banner (Centros Empresariales)

Versión del «Diagrama de inicio a fin» entregado en PDF A3, PNG y PPTX. Los pasos marcados **(por confirmar)** son supuestos abiertos; ver `preguntas-y-dudas-centros`.

**Carriles (quién hace cada paso):**
- Registros Académicos (RA)
- Jefatura (JEF)
- Finanzas (FIN)
- Escuela o Centro Empresarial (CE)
- Admisión (ADM)
- Docente (DOC)
- Participante (PAR)

## Fases y pasos
| # | Fase (cuándo) | Quién | Paso | Páginas | Nota |
|---|---|---|---|---|---|
| 1 | Preparar el periodo (3 veces al año) | RA | Abrir el periodo, sus partes (I01…, X01…, P01…), fechas web y feriados | STVTERM, SOATERM, SSAEXCL | Tema 1 |
| 2 | Preparar el periodo (cada mes) | CE | Diseñar el catálogo de cursos del mes y la malla del programa (reglas CAPP) | SCACRSE, SMAPROG, SMAAREA | Malla en CAPP (por confirmar) |
| 3 | Programar el mes | CE | Crear los NRC del grupo en su parte de periodo: cupo, horario, reglas | SSASECT, SSAPREQ, SSARRES | Temas 2 y 2.1 |
| 4 | Programar el mes | RA | Carga lectiva: registrar al docente, asignarlo al NRC y revisar su carga (reemplaza el Excel) | SIAINST, SSASECT, SIAASGN | Tema 3 |
| 5 | Admitir | PAR | Solicita llevar un curso del centro | — | |
| 6 | Admitir | ADM | Buscar, registrar y admitir a la persona; crea la solicitud y el estudiante | GOAMTCH, SAAQUIK, SPAIDEN (crea SAAADMS y SGASTDN) | Tema 4 |
| 7 | Admitir | RA | Asignar tutor o asesor | SIAINST, SGAADVR | ¿Aplica a los centros? (por confirmar) |
| 8 | Proyectar (CAPP) | RA | Evaluar el avance con CAPP y generar la proyección: qué nivel le toca | SMARQCM, SFPPROJ, SFAPROJ | PDF «CAPP explicado» |
| 9 | Inscribir y cobrar | RA o PAR | Inscribir en el NRC proyectado, por backoffice o autoservicio | SFAREGS | Quién inscribe (por confirmar) |
| 10 | Inscribir y cobrar | JEF | Aprobar sobrepasos cuando la inscripción da error (cupo, cruce, prerrequisito) | SFAROVR | (por confirmar) |
| 11 | Inscribir y cobrar | FIN | La inscripción genera el cobro; los pagos se registran en caja | SFARGFE, TSAAREV, TVACAJA | Capacidad 11 |
| 12 | Inscribir y cobrar | PAR | Paga la matrícula o pensión; con deuda puede tener retención | SOAHOLD | |
| 13 | Dictar clases | RA | Cargar el plan de evaluación del NRC | SHAGCOM | Capacidad 7 |
| 14 | Dictar clases | DOC | Registrar asistencia y calificaciones por autoservicio | Autoservicio | |
| 15 | Dictar clases | PAR | Consulta horario, asistencia y notas | Autoservicio | |
| 16 | Cerrar y avanzar | RA | Pasar las notas a la historia académica y ejecutar el CAPP masivo | SHRROLL, SMRBCMP | Capacidad 7 |
| 17 | Cerrar y avanzar | PAR | Aprueba el nivel: pasa al siguiente (vuelve al paso 8) o culmina y recibe su certificado | SHACRSE, SHADEGR | Certificado como grado (por confirmar) |

**Ciclo:** del paso 17 se vuelve al 8 mientras le queden niveles. Así funciona Inglés, de BASIC I a INTERMEDIATE III.

## Correspondencia con el flujo del usuario
| Flujo del usuario | Pasos |
|---|---|
| 1 Periodos y carga lectiva (RA) | 1, 4 |
| Planes curriculares (hoja del Zoom) | 2 |
| 2 Admisión (postulantes CEPRE → estudiantes) | 5, 6 |
| 3 Tutoría (RA) | 7 |
| 4 NRC = secciones, las registran las escuelas | 3 |
| 5 Jefatura | 10 |
| 6 Cada docente | 14 |
| 7 Finanzas | 11, 12 |
| Matrícula | 8, 9 |
| Enseñanza-aprendizaje (notas, asistencia) | 13 a 16 |
