# -*- coding: utf-8 -*-
"""Piezas comunes para los PDF (HTML impreso con Chromium)."""
import html
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
AUTHOR = 'Dagner Anibal Chuman Lluen'
CODE = re.compile(r'\b([SGT][A-Z]{2}[A-Z0-9]{3,4})\b')


def fmt(text):
    t = html.escape(text, quote=False)
    t = CODE.sub(r'<span class="code">\1</span>', t)
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)


def chips(codes):
    return ' '.join(f'<span class="pg">{html.escape(c)}</span>' for c in codes.split(', ')) if codes else ''


def section(num, title, intro=None):
    s = f'<div class="sec"><span class="num">{num}</span><h2>{html.escape(title)}</h2><span class="bar"></span></div>'
    return s + (f'<p class="intro">{fmt(intro)}</p>' if intro else '')


def table(cols, rows, cls=''):
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
    cells = ''.join(f'<div><span>{html.escape(k)}</span>{html.escape(v)}</div>' for k, v in meta)
    return ('<header class="cover"><div class="logos"><img src="uss.png" alt="USS"><img src="ellucian.png" alt="Ellucian"></div>'
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
table.left td, table.left th { text-align: left !important; }
'''


def render(name, body, css_extra, footer_title, out_pdf, meta_title, subject):
    css = open(os.path.join(HERE, 'base.css'), encoding='utf8').read() + COMMON_CSS + css_extra
    html_path = os.path.join(HERE, f'{name}.html')
    pdf_path = os.path.join(HERE, f'{name}.pdf')
    open(html_path, 'w', encoding='utf8').write(
        f'<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>{html.escape(meta_title)}</title>'
        f'<style>{css}</style></head><body>{body}</body></html>')
    subprocess.run(['node', os.path.join(HERE, 'render.js'), html_path, pdf_path, footer_title], check=True)
    import fitz
    d = fitz.open(pdf_path)
    d.set_metadata({'title': meta_title, 'author': AUTHOR, 'subject': subject, 'creator': AUTHOR,
                    'producer': d.metadata.get('producer', '')})
    d.save(out_pdf, garbage=3, deflate=True)
    return pdf_path
