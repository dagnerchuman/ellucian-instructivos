# -*- coding: utf-8 -*-
"""Piezas comunes para los PDF con formato USS (HTML impreso con Chromium).

Uso típico en un script generador:
    from common import AUTHOR, chips, fmt, header, render, section, table
    html = header(...) + section(1, 'Título') + table(...)
    render('nombre', html, CSS_EXTRA, 'Pie de página', 'SALIDA.pdf', 'Título del PDF', 'Asunto')
"""
import html
import os
import re
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
AUTHOR = 'Dagner Anibal Chuman Lluen'
CODE = re.compile(r'\b([SGT][A-Z]{2}[A-Z0-9]{3,4})\b')   # páginas de Banner: SSASECT, GOAMTCH, TSAAREV…


def _url(*parts):
    return 'file://' + os.path.join(HERE, *parts)


FONT_FACE = ''.join(
    f"@font-face {{ font-family: '{fam}'; font-weight: {w}; src: url('{_url('fonts', f)}'); }}\n"
    for fam, w, f in [('InterStatic', 400, 'InterStatic-Regular.ttf'), ('InterStatic', 500, 'InterStatic-Medium.ttf'),
                      ('InterStatic', 600, 'InterStatic-SemiBold.ttf'), ('InterStatic', 700, 'InterStatic-Bold.ttf'),
                      ('Montserrat', 400, 'Montserrat-Regular.ttf'), ('Montserrat', 700, 'Montserrat-Bold.ttf')])


def fmt(text):
    """Escapa HTML, resalta páginas de Banner y convierte **negrita**."""
    t = html.escape(text, quote=False)
    t = CODE.sub(r'<span class="code">\1</span>', t)
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)


def chips(codes):
    return ' '.join(f'<span class="pg">{html.escape(c)}</span>' for c in codes.split(', ')) if codes else ''


def section(num, title, intro=None):
    s = f'<div class="sec"><span class="num">{num}</span><h2>{html.escape(title)}</h2><span class="bar"></span></div>'
    return s + (f'<p class="intro">{fmt(intro)}</p>' if intro else '')


def table(cols, rows, cls=''):
    """cols = [(encabezado, ancho %)], rows = [[celdas html]] o ('grp', 'título de grupo')."""
    colgroup = ''.join(f'<col style="width:{w}%">' for _, w in cols)
    head = ''.join(f'<th>{c}</th>' for c, _ in cols)
    body = ''
    for r in rows:
        if isinstance(r, tuple) and r[0] == 'grp':
            body += f'<tr class="grp"><td colspan="{len(cols)}">{fmt(r[1])}</td></tr>'
        else:
            body += '<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>'
    return (f'<table class="t {cls}"><colgroup>{colgroup}</colgroup><thead><tr>{head}</tr></thead>'
            f'<tbody>{body}</tbody></table>')


def header(kicker, title, sub, meta):
    """Portada compacta: logos USS y Ellucian, banda morada y 4 datos (Elaborado por, Fecha, Fuentes, Estado)."""
    cells = ''.join(f'<div><span>{html.escape(k)}</span>{html.escape(v)}</div>' for k, v in meta)
    return (f'<header class="cover"><div class="logos"><img src="{_url("img", "uss.png")}" alt="USS">'
            f'<img src="{_url("img", "ellucian.png")}" alt="Ellucian"></div>'
            f'<div class="band"><div class="kicker">{html.escape(kicker)}</div><h1>{html.escape(title)}</h1>'
            f'<div class="sub">{html.escape(sub)}</div></div><div class="meta">{cells}</div></header>')


COMMON_CSS = '''
.meta { grid-template-columns: 1.15fr .75fr 1.55fr 1.1fr; }
.lead { border-left: 4px solid var(--p); background: var(--pl); border-radius: 8px; padding: 9px 13px; font-size: 9.6pt;
        line-height: 1.5; margin: 2px 0 6px; break-inside: avoid; }
.ap { display: inline-block; border-radius: 9px; padding: 0 8px; font-size: 7.5pt; font-weight: 700; white-space: nowrap; }
.ap.ok { background: var(--gl); color: var(--gd); } .ap.tbc { background: #FFF3DC; color: #8A5A00; }
.ap.na { background: var(--soft); color: #6B6B76; } .ap.bad { background: #FDE7E7; color: #A11D1D; }
.ap.now { background: #FFE6DA; color: #A63F12; } .ap.soon { background: var(--pl); color: var(--pd); }
.note.warn { border-left-color: #E0A100; background: #FFF8E8; }
.h3gap { margin: 10px 0 4px; }
.keep { break-inside: avoid; }
table.left td, table.left th { text-align: left !important; }
'''


def render(name, body, css_extra, footer_title, out_pdf, meta_title, subject):
    """Escribe el HTML en una carpeta temporal, lo imprime con Chromium (render.js) y fija los metadatos del PDF."""
    css = FONT_FACE + open(os.path.join(HERE, 'base.css'), encoding='utf8').read() + COMMON_CSS + css_extra
    work = tempfile.mkdtemp(prefix=f'uss_{name}_')
    html_path, pdf_path = os.path.join(work, f'{name}.html'), os.path.join(work, f'{name}.pdf')
    open(html_path, 'w', encoding='utf8').write(
        f'<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>{html.escape(meta_title)}</title>'
        f'<style>{css}</style></head><body>{body}</body></html>')
    subprocess.run(['node', os.path.join(HERE, 'render.js'), html_path, pdf_path, footer_title], check=True)
    import pymupdf
    d = pymupdf.open(pdf_path)
    d.set_metadata({'title': meta_title, 'author': AUTHOR, 'subject': subject, 'creator': AUTHOR,
                    'producer': d.metadata.get('producer', '')})
    os.makedirs(os.path.dirname(os.path.abspath(out_pdf)), exist_ok=True)
    d.save(out_pdf, garbage=3, deflate=True)
    return out_pdf


def check_pdf(path, png_dir=None, dpi=80):
    """Control de calidad: páginas, fuentes de reemplazo (glifos que Inter no tiene) y PNG por página para revisar."""
    import pymupdf
    d = pymupdf.open(path)
    problems = []
    for i, p in enumerate(d):
        for b in p.get_text('rawdict')['blocks']:
            for ln in b.get('lines', []):
                for sp in ln['spans']:
                    if 'Inter' not in sp['font'] and 'Montserrat' not in sp['font']:
                        problems.append((i + 1, sp['font'], ''.join(c['c'] for c in sp['chars'])))
        if png_dir:
            os.makedirs(png_dir, exist_ok=True)
            p.get_pixmap(dpi=dpi).save(os.path.join(png_dir, f'pag_{i + 1}.png'))
    print(f'{path}: {d.page_count} páginas; autor: {d.metadata.get("author")}')
    for pg, font, txt in problems:
        print(f'  Página {pg}: «{txt}» usa {font} (cámbialo: Inter no tiene ese glifo)')
    return d.page_count, problems


# ------------------------------------------------------------------ siglas y páginas: significado entre paréntesis
# Regla del usuario (26/09/2026): toda sigla o código lleva su significado entre paréntesis. explicar() lo agrega
# solo la primera vez que aparece en cada tarjeta y glosario_html() arma el glosario final con lo que se usó.
# Nombres de páginas tomados de los instructivos (ver arquitectura-centros-empresariales/references/glosario.md).
SIGLAS = {
    'NRC': ('Número de Referencia de Curso', 'Número de Referencia de Curso: identifica un grupo o sección de un curso en un '
            'periodo, con su horario y sus docentes.'),
    'SEUSS': ('sistema académico actual de la USS', 'Sistema académico que la USS usa hoy y que se reemplaza por Banner.'),
    'CAPP': ('evaluación del avance en la malla', 'Curriculum, Advising and Program Planning: compara la historia académica con la '
             'malla y muestra qué cursos cumplió el estudiante y cuáles le faltan.'),
    'FTE': ('equivalente a tiempo completo', 'Full-Time Equivalent: cuántas horas equivalen a un docente a tiempo completo.'),
    'LMS': ('plataforma del aula virtual', 'Learning Management System: plataforma del aula virtual.'),
    'ATTRGRD': ('componente de asistencia', 'Nombre obligatorio del componente de asistencia en el plan de evaluación del NRC.'),
    'INH': ('nota de desaprobado por asistencia', 'Código de nota de desaprobado por asistencia en el ejemplo del instructivo 7.1.0.'),
    'EG': ('Egresado', 'Estado de Egresado del estudiante de pregrado.'),
    'backoffice': ('páginas internas de Banner que usa el personal', 'Páginas internas de Banner que usa el personal administrativo.'),
    'autoservicio': ('portal web de Banner para docentes y estudiantes', 'Portal web de Banner para docentes y estudiantes.'),
    'pitch': ('presentación corta del proyecto', 'Presentación corta del proyecto o plan de negocio.'),
}
PAGINAS = {
    'STVTERM': 'códigos de periodo', 'STVPTRM': 'códigos de parte de periodo', 'SOATERM': 'Control de periodo',
    'SSAEXCL': 'feriados y excepciones de clases', 'SIATERM': 'Control de periodo de carga docente',
    'SIAINST': 'datos del docente', 'SIAASGN': 'Asignación de docente, su carga', 'SIAFAVL': 'disponibilidad del docente',
    'SIAFLRT': 'reglas de carga docente', 'SCACRSE': 'catálogo de cursos', 'SCAPREQ': 'prerrequisitos y puntajes de examen del catálogo',
    'SCADETL': 'detalle del curso: correquisitos y equivalentes', 'SCARRES': 'restricciones de inscripción del curso',
    'SSASECT': 'Programar NRC', 'SSADETL': 'detalle del NRC', 'SSAPREQ': 'prerrequisitos del NRC',
    'SSARRES': 'restricciones de inscripción del NRC', 'SSAWSEC': 'consulta web de notas por NRC', 'SLQMEET': 'salones disponibles',
    'SMAPROG': 'requerimientos del programa: la malla', 'SMAAREA': 'requerimientos de área de la malla',
    'SMARQCM': 'CAPP de un estudiante', 'SMRBCMP': 'CAPP masivo', 'SMICRLT': 'resultado del CAPP',
    'SFPPROJ': 'proceso de proyección académica', 'SFAPROJ': 'proyección del estudiante', 'SFAREGS': 'Inscripción de curso del alumno',
    'SFAROVR': 'permisos de sobrepaso de inscripción', 'STVROVR': 'códigos de sobrepaso', 'SFARGFE': 'reglas de cobro de la inscripción',
    'TSAAREV': 'cuenta corriente del estudiante', 'TVACAJA': 'caja', 'SOAHOLD': 'retenciones', 'SOATEST': 'puntajes de examen del estudiante',
    'STVTESC': 'códigos de examen', 'GOAMTCH': 'búsqueda de personas para evitar duplicados', 'SPAIDEN': 'datos de la persona',
    'SAAQUIK': 'admisión rápida', 'SAAADMS': 'solicitud de admisión', 'SGASTDN': 'registro del estudiante',
    'SGAADVR': 'tutor o asesor del estudiante', 'SHAGRDE': 'códigos de calificación', 'SHAGSCH': 'escalas de calificación',
    'SHAGCOM': 'plan de evaluación del NRC', 'SFASLST': 'notas por backoffice', 'SHATCKN': 'notas ya en la historia académica',
    'SHRCINC': 'notas incompletas', 'SHAEGBC': 'fechas de corrección extemporánea de notas',
    'SHRROLL': 'paso de notas a la historia académica', 'SHACRSE': 'historia académica por curso', 'SHADEGR': 'grado del estudiante',
    'GTVINTP': 'códigos de socio de integración', 'GORINTG': 'reglas de socio de integración',
}
# Clases donde no se agrega significado: etiquetas, títulos de tarjetas, píldoras y encabezados.
_NO_EXPLICAR = ('lab', 'tg', 'exh', 'rh', 'tt', 'dh', 'gh', 'ap', 'sec', 'flow', 'twh', 'cite', 'src', 'pcode', 'ps', 'pl', 'k', 'num', 'gls')
# Términos que el lector ya conoce: se explican una sola vez en todo el documento.
UNA_VEZ = {'SEUSS'}
_VISTOS_DOC = set()
_VACIOS = ('br', 'img', 'col', 'path', 'input', 'hr', 'meta', 'line', 'rect', 'circle')
_TERM_RE = re.compile(r'\b(' + '|'.join(sorted(list(PAGINAS) + [k for k in SIGLAS if k.isupper()], key=len, reverse=True))
                      + r')\b|\b(backoffice|autoservicio|pitch)\b', re.I)
USADOS = set()


def _meaning(term):
    key = term if term in PAGINAS or term in SIGLAS else term.lower()
    if key in PAGINAS:
        return key, PAGINAS[key]
    return key, SIGLAS[key][0]


def explicar(html_str, seen=None):
    """Agrega «(significado)» a la primera aparición de cada sigla o página de Banner en el fragmento HTML.

    Si el término ya está dentro de un paréntesis, usa «término: significado» para no anidar paréntesis.
    """
    seen = set() if seen is None else seen
    out, stack, pending, depth = [], [], [], 0
    for tok in re.split(r'(<[^>]+>)', html_str):
        if tok.startswith('<'):
            name = re.match(r'</?\s*([a-zA-Z0-9]+)', tok)
            name = name.group(1).lower() if name else ''
            if tok.startswith('</'):
                out.append(tok)
                if stack:
                    stack.pop()
                if pending and len(stack) < pending[-1][0]:
                    out.append(pending.pop()[1])
            elif tok.endswith('/>') or name in _VACIOS:
                out.append(tok)
            else:
                cls = re.search(r'class="([^"]*)"', tok)
                excl = (stack[-1] if stack else False) or bool(cls and set(cls.group(1).split()) & set(_NO_EXPLICAR))
                stack.append(excl)
                out.append(tok)
            continue
        if stack and stack[-1]:
            out.append(tok)
            continue

        def rep(m):
            nonlocal depth
            term = m.group(0)
            if term.isupper() is False and m.group(2) is None:
                return term
            key, mean = _meaning(term)
            if key in seen or key in _VISTOS_DOC:
                return term
            seen.add(key)
            if key in UNA_VEZ:
                _VISTOS_DOC.add(key)
            USADOS.add(key)
            d = depth + tok[:m.start()].count('(') - tok[:m.start()].count(')')
            txt = f': {mean}' if d > 0 else f' ({mean})'
            span = f'<span class="gls">{html.escape(txt)}</span>'
            if tok.strip() == term and stack:        # el término es todo el contenido de su etiqueta (p. ej. <span class="code">)
                pending.append((len(stack), span))
                return term
            return term + span
        new = _TERM_RE.sub(rep, tok)
        depth += tok.count('(') - tok.count(')')
        out.append(new)
    return ''.join(out)


def glosario_html(extra=()):
    """Glosario con los términos usados en el documento (y los extra que se pidan)."""
    keys = USADOS | set(extra)
    sig = sorted((k for k in keys if k in SIGLAS), key=str.lower)
    pag = sorted(k for k in keys if k in PAGINAS)
    def item(t, d):
        return f'<div class="gi"><b>{html.escape(t)}</b><span>{html.escape(d)}</span></div>'
    s = ('<div class="glos keep"><div class="gh">Siglas y palabras</div><div class="gg">'
         + ''.join(item(k.capitalize() if k.islower() else k, SIGLAS[k][1]) for k in sig) + '</div></div>')
    if pag:
        s += ('<div class="glos keep"><div class="gh">Páginas de Banner</div><div class="gg">'
              + ''.join(item(k, PAGINAS[k][0].upper() + PAGINAS[k][1:] + '.') for k in pag) + '</div></div>')
    return s


GLOS_CSS = '''
.gls { color: var(--mut); font-weight: 400; }
.code + .gls, b > .gls { font-weight: 400; }
.glos { border: 1px solid var(--line); border-radius: 10px; overflow: hidden; margin: 0 0 9px; background: #fff; }
.gh { background: var(--pl); color: var(--pd); font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 9pt; padding: 5px 12px; }
.gg { display: grid; grid-template-columns: 1fr 1fr; }
.gi { display: grid; grid-template-columns: 78px 1fr; gap: 6px; padding: 4px 12px; border-top: 1px solid var(--line); font-size: 8.2pt;
      line-height: 1.4; }
.gi b { color: var(--pd); }
'''
