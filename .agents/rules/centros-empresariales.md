# Reglas de Trabajo: Centros Empresariales USS en Ellucian Banner

## 1. Identidad y Contexto
- **Usuario:** Dagner Anibal Chuman Lluen.
- **Área:** Centros Empresariales de la Universidad Señor de Sipán (USS):
  - **Idiomas** (Inglés: BASIC I..III, INTERMEDIATE I..III).
  - **Computación** (Informática: ESEC/ESEP).
  - **Emprendimiento**.
- **Proyecto:** Migración del sistema legado **SEUSS** a **Ellucian Banner Student**.
- **Idioma:** Español directo, claro y sin rodeos.

## 2. Separación Estricta de Fuentes de Verdad
1. **«Hoy en SEUSS»**: Lo que dice el usuario que se hace actualmente. No reinterpretarlo.
2. **«En Ellucian»**: Lo que dicen los 83 instructivos oficiales del repositorio. Citar siempre instructivo y diapositiva: «instructivo X.X [Nombre], diap. YY».
3. **«Duda abierta»**: Todo lo que no esté en los instructivos ni confirmado por el usuario. Registrar en `.claude/skills/preguntas-y-dudas-centros/registro.md` (E## para Ellucian, U## para USS).
4. **Prohibido inventar datos de la USS**: Códigos de campus, escuelas, programas o nombres de cursos no confirmados no deben inventarse. Si se usa un dato ilustrativo, marcar claramente como «de ejemplo».

## 3. Modelo Académico de los Centros
- **Periodos (6 dígitos):** Año + 5 (Centros) + Secuencia (1 = verano, 4 = semestre I, 6 = semestre II).
  - 2026-0 = `202651` | 2026-I = `202654` | 2026-II = `202656` | 2027-0 = `202751`.
  - **No usar** «periodos de 3 meses» (supuesto descartado S01).
- **Partes de periodo:**
  - Idiomas: `IGE` / `I01` a `I12`.
  - Computación: `CGE` / `X01` a `X07`.
  - Emprendimiento: `EGE` / `P01` a `P06`.
- **Cursos y NRCs:**
  - El curso del catálogo (**SCACRSE**) se programa como NRC en una parte de periodo en **SSASECT**.
  - Horas crédito y horas cobro se heredan del catálogo.
  - La hora académica se calcula con el factor de duración de **SIATERM** (minutos fijos por periodo).
- **Prerrequisitos en Inglés:**
  - Si desaprueba BASIC I, no pasa a BASIC II salvo con examen de suficiencia en **SOATEST**. En Banner se implementa con regla en **SCAPREQ** / **SSAPREQ** y verificación en **Fatal** en **SOATERM**.

## 4. Estándar de Documentos y Entregables
- Siempre incluir ejemplos de los **tres centros** (Idiomas, Computación, Emprendimiento).
- Estructura fija: «Hoy en SEUSS» / «En Ellucian» / «Resultado».
- Pocas tablas; preferir tarjetas por tema y diagramas de flujo.
- Siglas y nombres de páginas siempre con su significado entre paréntesis en la primera mención: «NRC (Número de Referencia de Curso)», «SSASECT (Programar NRC)».
- Todas las dudas al final, separadas en «Para Ellucian» y «Para la USS».
- Autor obligatorio: «Elaborado por: Dagner Anibal Chuman Lluen».
- Paleta USS: Morado `#7030A0` / `#5C2193`, Verdes `#4EA72E` y `#92D050`. Colores por centro: Idiomas `#7030A0`, Informática `#0E8A5F`, Emprendimiento `#C2501C`.
- En presentaciones PPTX: deben abrir limpiamente en PowerPoint sin requerir reparación.
- En hojas Excel: fórmulas dinámicas verificadas con 0 errores.
