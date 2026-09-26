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
