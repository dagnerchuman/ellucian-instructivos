# Idiomas: cursos, prerrequisitos y ligas

Parte de la skill `centro-idiomas` (el mapa está en su `SKILL.md`).

## Cursos conocidos (CONFIRMADOS en TEST y Programación — C11, C60)

| Nivel | Código Catálogo | Título Oficial | HT / HP | Malla Curricular | Prerrequisito |
|---|---|---|---|---|---|
| **BASIC I** | `ESEP 02456` | Basic I | 4 HT / 3 HP | `MI03-01` | Ninguno (ingreso) |
| **BASIC II** | `ESEP 02457` | Basic Ii | 4 HT / 3 HP | `MI03-01` | BASIC I aprobado o Suficiencia |
| **BASIC III** | `ESEP 02458` | Basic Iii | 4 HT / 3 HP | `MI03-01` | BASIC II aprobado |
| **INTERMEDIATE I** | `ESEP 02693` | Intermediate I | 4 HT / 3 HP | `MI03-02` | BASIC III aprobado |
| **INTERMEDIATE II** | `ESEP 02721` | Intermediate Ii | 4 HT / 3 HP | `MI03-02` | INTERMEDIATE I aprobado |
| **INTERMEDIATE III** | `ESEP 02997` | Intermediate Iii | 4 HT / 3 HP | `MI03-02` | INTERMEDIATE II aprobado |

> Modo de calificar oficial en catálogo SSASECT: **Modo `C` (Escala Centesimal)** (confirmado C60).

## Regla de prerrequisitos (CONFIRMADA — C11, R09)

En SEUSS, quien desaprueba BASIC I **NO puede pasar a BASIC II** salvo con examen de suficiencia. En Ellucian:

1. **SCAPREQ / SSAPREQ:** se configura el prerrequisito «BASIC I aprobado **o** examen de suficiencia con puntaje mínimo».
2. **SOATERM:** la verificación de prerrequisitos se pone en **Fatal** → SFAREGS bloquea la inscripción.
3. **SOATEST:** se registra el puntaje del examen de suficiencia.
4. **SFPPROJ:** la proyección con verificación de prerrequisitos **no ofrece** BASIC II si no hay BASIC I aprobado o examen.
5. **SFAROVR:** un sobrepaso administrativo puede saltar la regla.

**Idiomas como prerrequisito de pregrado (29/10, C159 a C168):** en **SCAPPRQ** del programa de pregrado (por ejemplo Medicina `1PCSP15`, versión 202444) Nidia Beltrán puso «malla **Y (** `ESEP 02456` **O** `02457` **O** `02458` **)**» (Basic I a III) y, más adelante, Intermediate I a III (`ESEP 02693`, `02721`, `02997`), sin nivel ni calificación: basta con haberlo cursado. Un Basic **en curso** en un periodo de centros no cuenta mientras «En progreso» esté sin marcar en el SOATERM de pregrado: sale «Prerequisite In Progress» (C166). Según el resumen de Ellucian, se exige **desde el 2.º ciclo** al menos un curso de Idiomas (C168, U49). Con el Basic en la historia, el alumno se inscribe; Banner usa la versión de SCAPPRQ de su **catálogo**, así que la regla debe estar en cada versión (C170). El correquisito no sirve, porque pregrado y centros van en periodos distintos. Guía y prueba en [ref-restricciones-y-prerrequisitos-por-programa.md](../../arquitectura-centros-empresariales/references/ref-restricciones-y-prerrequisitos-por-programa.md).

## Ligas: Teórico Virtual + 3 Opciones de Práctica (CONFIRMADO C60, R18, ADR-019)
- Cada curso de Idiomas se programa mediante un esquema **Uno a Muchos**: 1 sección teórica principal ligada a 3 secciones prácticas.
- **Teórico Principal (Sección `AT` · Virtual `SAUVIR`):**
  - Horas: 4 créditos totales.
  - Indicadores: **Calificable = Sí**, **Dispensa de colegiatura = No** (cobra la matrícula/cuota).
  - En `SSASECT`: Identificador de liga = **`TA`**.
  - En `SSADETL`: Conector de liga vinculado = **`PA`**.
- **Prácticas Asociadas (`AC1` Presencial Posgrado / `AC2` y `AC3` Virtuales):**
  - Horas: 0 créditos generados.
  - Indicadores: **Calificable = No**, **Dispensa de colegiatura = Sí** (no duplica el cobro).
  - En `SSASECT`: Identificador de liga = **`PA`**.
  - En `SSADETL`: Conector de liga vinculado = **`TA`**.
- **Comportamiento en Matrícula (`SFAREGS` y Autoservicio):**
  - Con ligas en **Fatal** en `SOATERM`, el estudiante debe inscribir obligatoriamente el teórico `AT` junto a **una de las tres opciones de práctica** (`AC1`, `AC2` o `AC3`).
  - Si intenta inscribir solo el teórico, Banner emite: `Error de enlace de sección: Requiere componente ligado (Link Error: PA Required)`.

### NRCs reales probados en TEST (202656 · Parte I10)
- **BASIC III (`ESEP 02458`):**
  - Teórico `10010` (AT · Virtual SAUVIR): Lunes 18:00–20:30 · Dagner Chuman (`100582059`). Liga `TA` $\rightarrow$ `PA`.
  - Práctica `10011` (AC1 · Presencial Posgrado A-31): Martes 20:00–23:20 · Jossymar Cabanillas (`S00912435`). Liga `PA` $\rightarrow$ `TA`.
  - Práctica `10013` (AC2 · Virtual SAUVIR): Sábado 18:00–20:30 · Arnold Vaca (`S00912438`). Liga `PA` $\rightarrow$ `TA`.
  - Práctica `10024` (AC3 · Virtual SAUVIR): Miércoles 08:00–11:20 · Willy Valverde (`S00912437`). Liga `PA` $\rightarrow$ `TA`.
- **INTERMEDIATE I (`ESEP 02693`):**
  - Teórico `10030` (AT · Virtual SAUVIR): Viernes 08:00–11:20 · Dagner Chuman (`100582059`). Liga `TA` $\rightarrow$ `PA`.
  - Práctica `10031` (AC1 · Presencial Posgrado A-31): Jueves 18:00–20:30 · Maria Puelles (`100122229`). Liga `PA` $\rightarrow$ `TA`.
  - Práctica `10032` (AC2 · Virtual SAUVIR): Domingo 14:00–17:20 · Arnold Vaca (`S00912438`). Liga `PA` $\rightarrow$ `TA`.
  - Práctica `10033` (AC3 · Virtual SAUVIR): Sábado 14:00–17:20 · Arnold Vaca (`S00912438`). Liga `PA` $\rightarrow$ `TA`.
- **INTERMEDIATE II (`ESEP 02721`):**
  - Teórico `10034` (AT · Virtual SAUVIR): Sábado 08:00–11:20 · Arnold Vaca (`S00912438`). Liga `TA` $\rightarrow$ `PA`.
  - Práctica `10035` (AC1 · Presencial Posgrado A-41): Viernes 18:00–20:30 · Jossymar Cabanillas (`S00912435`). Liga `PA` $\rightarrow$ `TA`.
  - Práctica `10036` (AC2 · Virtual SAUVIR): Miércoles 18:00–20:30 · Jossymar Cabanillas (`S00912435`). Liga `PA` $\rightarrow$ `TA`.
  - Práctica `10037` (AC3 · Virtual SAUVIR): Jueves 08:00–11:20 · Willy Valverde (`S00912437`). Liga `PA` $\rightarrow$ `TA`.
- **INTERMEDIATE III (`ESEP 02997`):**
  - Teórico `10038` (AT · Virtual SAUVIR): Lunes 14:00–17:20 · Dagner Chuman (`100582059`). Liga `TA` $\rightarrow$ `PA`.
  - Práctica `10039` (AC1 · Presencial Posgrado A-51): Sábado 08:00–11:20 · Rosa Ocampo (`100448074`). Liga `PA` $\rightarrow$ `TA`.
  - Práctica `10040` (AC2 · Virtual SAUVIR): Domingo 08:00–11:20 · Arnold Vaca (`S00912438`). Liga `PA` $\rightarrow$ `TA`.
  - Práctica `10041` (AC3 · Virtual SAUVIR): Viernes 14:00–17:30 · Jossymar Cabanillas (`S00912435`). Liga `PA` $\rightarrow$ `TA`.
