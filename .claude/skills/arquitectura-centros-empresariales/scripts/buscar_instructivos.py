#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Busca texto en los instructivos PPTX del repositorio y cita instructivo y diapositiva.

Uso:
  python3 buscar_instructivos.py "factor de duración"
  python3 buscar_instructivos.py "SOATEST|suficiencia" --archivo 1.1.5 --max 5
  python3 buscar_instructivos.py --diapositiva "5.2_4.1.5.1" 12      # texto completo de una diapositiva
  python3 buscar_instructivos.py --listar                              # instructivos y número de diapositivas

El índice se guarda en la carpeta temporal y se regenera si cambia algún PPTX.
El número de diapositiva sigue el orden de la presentación (el que ve el usuario en PowerPoint).
"""
import argparse
import glob
import json
import os
import re
import sys
import tempfile
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
CACHE = os.path.join(tempfile.gettempdir(), 'instructivos_idx.json')
T_RE = re.compile(r'<a:t>([^<]*)</a:t>')
P_RE = re.compile(r'</a:p>')


def slide_order(z):
    """Rutas de las diapositivas en el orden de ppt/presentation.xml."""
    pres = z.read('ppt/presentation.xml').decode('utf8')
    rels = z.read('ppt/_rels/presentation.xml.rels').decode('utf8')
    target = {m.group(1): m.group(2) for m in re.finditer(r'<Relationship [^>]*Id="([^"]+)"[^>]*Target="([^"]+)"', rels)}
    target.update({m.group(2): m.group(1) for m in re.finditer(r'<Relationship [^>]*Target="([^"]+)"[^>]*Id="([^"]+)"', rels)})
    ids = re.findall(r'<p:sldId [^>]*r:id="([^"]+)"', pres)
    return ['ppt/' + target[i].lstrip('/').replace('ppt/', '') for i in ids if i in target]


def slide_text(xml):
    xml = P_RE.sub('\n', xml)
    parts = []
    for line in xml.split('\n'):
        t = ''.join(T_RE.findall(line)).strip()
        if t:
            parts.append(t)
    txt = ' '.join(parts)
    for a, b in (('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'")):
        txt = txt.replace(a, b)
    return txt


def files():
    return sorted(glob.glob(os.path.join(ROOT, 'CAPACIDAD*', '**', '*.pptx'), recursive=True))


def build_index():
    fl = files()
    sig = [(os.path.relpath(f, ROOT), os.path.getmtime(f)) for f in fl]
    if os.path.exists(CACHE):
        try:
            data = json.load(open(CACHE, encoding='utf8'))
            if data.get('sig') == sig and data.get('root') == ROOT:
                return data['slides']
        except (ValueError, KeyError):
            pass
    slides = []
    for f in fl:
        rel = os.path.relpath(f, ROOT)
        try:
            with zipfile.ZipFile(f) as z:
                for n, path in enumerate(slide_order(z), 1):
                    slides.append({'f': os.path.basename(f)[:-5], 'path': rel, 'n': n,
                                   't': slide_text(z.read(path).decode('utf8'))})
        except (zipfile.BadZipFile, KeyError) as e:
            print(f'Aviso: no se pudo leer {rel}: {e}', file=sys.stderr)
    json.dump({'root': ROOT, 'sig': sig, 'slides': slides}, open(CACHE, 'w', encoding='utf8'), ensure_ascii=False)
    return slides


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('patron', nargs='?', help='Expresión regular (sin distinguir mayúsculas)')
    ap.add_argument('--archivo', help='Solo instructivos cuyo nombre empiece así (ej. 7.1.4 o 5.3_)')
    ap.add_argument('--max', type=int, default=15, help='Máximo de resultados (15)')
    ap.add_argument('--contexto', type=int, default=220, help='Caracteres alrededor de la coincidencia (220)')
    ap.add_argument('--diapositiva', nargs=2, metavar=('ARCHIVO', 'N'), help='Muestra el texto completo de una diapositiva')
    ap.add_argument('--listar', action='store_true', help='Lista los instructivos y su número de diapositivas')
    a = ap.parse_args()
    slides = build_index()

    if a.listar:
        count = {}
        for s in slides:
            count.setdefault(s['path'], 0)
            count[s['path']] += 1
        for p, c in count.items():
            print(f'{c:4d}  {p}')
        return
    if a.diapositiva:
        pref, n = a.diapositiva[0], int(a.diapositiva[1])
        for s in slides:
            if s['f'].startswith(pref) and s['n'] == n:
                print(f"== {s['f']} · diap. {n}\n{s['t']}\n")
        return
    if not a.patron:
        ap.error('Indica un patrón, --diapositiva o --listar')
    rx = re.compile(a.patron, re.I)
    shown = 0
    for s in slides:
        if a.archivo and not s['f'].startswith(a.archivo):
            continue
        m = rx.search(s['t'])
        if not m:
            continue
        i, j = max(0, m.start() - a.contexto), min(len(s['t']), m.end() + a.contexto)
        print(f"== {s['f']} · diap. {s['n']}\n   …{s['t'][i:j]}…\n")
        shown += 1
        if shown >= a.max:
            print(f'(se muestran {a.max}; usa --max para ver más)')
            break
    if not shown:
        print('Sin resultados.')


if __name__ == '__main__':
    main()
