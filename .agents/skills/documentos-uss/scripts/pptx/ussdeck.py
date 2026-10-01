# -*- coding: utf-8 -*-
"""Piezas comunes para presentaciones en el formato USS de Centros Empresariales.

Requisitos (no están en el repositorio):
- La plantilla PPTX del usuario («Ppt USS 2026», usada como '2. PROGRAMACIÓN DE ASIGNATURAS'): pídela al usuario y
  pon su ruta en la variable USS_PPT_TEMPLATE (o déjala como programacion.pptx junto a este archivo).
  Diapositivas base usadas: ver BASE.
- Los scripts de la skill «pptx» (add_slide.py, clean.py, office/soffice.py, validate.py): se buscan solos en
  ~/.claude/skills/**/pptx/scripts; si no, define PPTX_SKILL_SCRIPTS.
"""
import glob
import os, random, re, shutil, subprocess, sys, zipfile
from lxml import etree
from PIL import ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))


def _find_pptx_scripts():
    if os.environ.get('PPTX_SKILL_SCRIPTS'):
        return os.environ['PPTX_SKILL_SCRIPTS']
    hits = glob.glob(os.path.expanduser('~/.claude/skills/**/pptx/scripts/add_slide.py'), recursive=True)
    return os.path.dirname(hits[0]) if hits else ''


SK = _find_pptx_scripts()
TEMPLATE = os.environ.get('USS_PPT_TEMPLATE', os.path.join(HERE, 'programacion.pptx'))
AUTHOR = 'Dagner Anibal Chuman Lluen'
FOOTER_RE = re.compile(r'Elaborado por: [^<]*')   # el pie de la plantilla se reemplaza por el autor

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
NSDECL = ' '.join(f'xmlns:{k}="{v}"' for k, v in NS.items())
A = '{%s}' % NS['a']
P = '{%s}' % NS['p']
R = '{%s}' % NS['r']

PURPLE, DARK_PURPLE, LIGHT_GREEN, GREEN = '7030A0', '5C2193', '92D050', '4EA72E'
SLIDE_W = 12192000

# Diapositivas base dentro de la plantilla
BASE = {'cover': 'slide1.xml', 'flow': 'slide5.xml', 'text': 'slide3.xml', 'div': 'slide6.xml',
        'cfg': 'slide7.xml', 'close': 'slide23.xml'}


# ---------------------------------------------------------------- texto enriquecido
def para(*parts):
    return [p if isinstance(p, tuple) else (p, 'n') for p in parts]


G = lambda t: (t, 'g')   # negrita verde
B = lambda t: (t, 'b')   # negrita


# ---------------------------------------------------------------- XML
def parse(path):
    return etree.parse(path, etree.XMLParser(remove_blank_text=False))


def save(tree, path):
    tree.write(path, xml_declaration=True, encoding='UTF-8', standalone=True)


def frag(xml):
    return etree.fromstring(f'<root {NSDECL}>{xml}</root>')[0]


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def shape_by_name(tree, name):
    for el in tree.find('.//p:spTree', NS):
        c = el.find('.//p:cNvPr', NS)
        if c is not None and c.get('name') == name:
            return el
    raise KeyError(name)


def next_id(tree):
    return max(int(c.get('id')) for c in tree.iter(P + 'cNvPr')) + 1


def set_xfrm(el, x, y, w, h):
    xf = el.find('.//a:xfrm', NS)
    xf.find('a:off', NS).set('x', str(int(x)))
    xf.find('a:off', NS).set('y', str(int(y)))
    xf.find('a:ext', NS).set('cx', str(int(w)))
    xf.find('a:ext', NS).set('cy', str(int(h)))


def geo(el):
    xf = el.find('.//a:xfrm', NS)
    o, e = xf.find('a:off', NS), xf.find('a:ext', NS)
    return int(o.get('x')), int(o.get('y')), int(e.get('cx')), int(e.get('cy'))


def set_first_run_text(sp, text):
    runs = sp.findall('.//a:r', NS)
    runs[0].find('a:t', NS).text = text
    for r in runs[1:]:
        r.getparent().remove(r)


# ---------------------------------------------------------------- medidas
_MB = ImageFont.truetype(os.path.join(HERE, '..', 'pdf', 'fonts', 'Montserrat-Bold.ttf'), 1000)


def montserrat_bold_emu(text, pt):
    return _MB.getlength(text) / 1000 * pt * 12700


def est_lines(text, width_emu, pt, em=0.55):
    per_line = max(1, int((width_emu - 182880) / (pt * em * 12700)))
    lines, cur = 1, 0
    for w in text.split():
        add = len(w) + (1 if cur else 0)
        if cur + add > per_line:
            lines, cur = lines + 1, len(w)
        else:
            cur += add
    return lines


# ---------------------------------------------------------------- piezas USS
def run_xml(text, style, sz=1100, color_default='FFFFFF', green=LIGHT_GREEN):
    b = ' b="1"' if style in ('b', 'g') else ''
    color = green if style == 'g' else color_default
    return (f'<a:r><a:rPr lang="es-ES" sz="{sz}"{b} dirty="0"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'</a:rPr><a:t>{esc(text)}</a:t></a:r>')


def callout_xml(sid, x, y, w, h, paras, algn):
    ps = ''.join(f'<a:p><a:pPr algn="{algn}"><a:spcAft><a:spcPts val="300"/></a:spcAft></a:pPr>'
                 + ''.join(run_xml(t, s) for t, s in pr) + '</a:p>' for pr in paras)
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Globo {sid}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 7573"/></a:avLst></a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="{PURPLE}"/></a:solidFill></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" rtlCol="0" anchor="ctr"><a:noAutofit/></a:bodyPr><a:lstStyle/>{ps}</p:txBody></p:sp>')


def callout_height(paras, w):
    lines = sum(est_lines(''.join(t for t, _ in pr), w, 11) for pr in paras)
    return lines * 11 * 1.2 * 12700 + len(paras) * 3 * 12700 + 150000


def highlight_xml(sid, x, y, w, h):
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Marco {sid}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/>'
            f'<a:ln w="38100" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:srgbClr val="{DARK_PURPLE}"/></a:solidFill>'
            f'<a:prstDash val="solid"/><a:round/></a:ln></p:spPr>'
            f'<p:txBody><a:bodyPr rtlCol="0" anchor="ctr"/><a:lstStyle/><a:p><a:pPr algn="ctr"/><a:endParaRPr lang="es-PE"/></a:p></p:txBody></p:sp>')


def marker_xml(sid, cx, cy, label):
    w = 230000 if len(label) == 1 else 300000
    h = 230000
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Numero {sid}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{int(cx - w / 2)}" y="{int(cy - h / 2)}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
            f'<a:prstGeom prst="roundRect"><a:avLst/></a:prstGeom><a:solidFill><a:schemeClr val="accent6"/></a:solidFill>'
            f'<a:ln><a:solidFill><a:schemeClr val="accent3"/></a:solidFill></a:ln></p:spPr>'
            f'<p:txBody><a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="ctr"/><a:lstStyle/>'
            f'<a:p><a:pPr algn="ctr"/>{run_xml(label, "b")}</a:p></p:txBody></p:sp>')


def textbox_xml(sid, x, y, w, h, paras_xml, anchor='t', fill=None, line=None, geom='rect', insets=''):
    fill_xml = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else '<a:noFill/>'
    line_xml = f'<a:ln w="28575"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>' if line else ''
    avl = '<a:avLst><a:gd name="adj" fmla="val 8000"/></a:avLst>' if geom == 'roundRect' else '<a:avLst/>'
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Texto {sid}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="{geom}">{avl}</a:prstGeom>{fill_xml}{line_xml}</p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" rtlCol="0" anchor="{anchor}"{insets}><a:noAutofit/></a:bodyPr>'
            f'<a:lstStyle/>{paras_xml}</p:txBody></p:sp>')


def bullet_para(parts, sz=1800, color='000000', spc_aft=1200, bullet=True, algn='just'):
    bu = ('<a:buClr><a:schemeClr val="accent6"/></a:buClr><a:buFont typeface="Wingdings" panose="05000000000000000000" '
          'pitchFamily="2" charset="2"/><a:buChar char="§"/>') if bullet else '<a:buNone/>'
    mar = 'marL="285750" indent="-285750"' if bullet else 'marL="0" indent="0"'
    runs = ''
    for t, s in parts:
        b = ' b="1"' if s in ('b', 'g') else ''
        c = GREEN if s == 'g' else color
        runs += (f'<a:r><a:rPr lang="es-ES" sz="{sz}"{b} dirty="0"><a:solidFill><a:srgbClr val="{c}"/></a:solidFill></a:rPr>'
                 f'<a:t>{esc(t)}</a:t></a:r>')
    return f'<a:p><a:pPr {mar} algn="{algn}"><a:spcAft><a:spcPts val="{spc_aft}"/></a:spcAft>{bu}</a:pPr>{runs}</a:p>'


def set_title(tree, text):
    title = shape_by_name(tree, 'CuadroTexto 6')
    set_first_run_text(title, text)
    w = montserrat_bold_emu(text, 28) + 182880 + 30000
    title.find('.//a:xfrm', NS).find('a:ext', NS).set('cx', str(int(w)))
    bx = 431320 + w
    set_xfrm(shape_by_name(tree, 'Rectángulo 7'), bx, 241540, SLIDE_W - bx, 445583)


# ---------------------------------------------------------------- estructura
def build_structure(work, kinds):
    """Descomprime la plantilla y crea una diapositiva por cada 'kind' (en orden)."""
    u = os.path.join(work, 'u')
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(u)
    with zipfile.ZipFile(TEMPLATE) as z:
        z.extractall(u)
    created = []
    for kind in kinds:
        out = subprocess.run([sys.executable, os.path.join(SK, 'add_slide.py'), u, BASE[kind]],
                             capture_output=True, text=True, cwd=SK, check=True).stdout
        created.append(re.search(r'Created (ppt/slides/slide\d+\.xml)', out).group(1))
    pres_path = os.path.join(u, 'ppt/presentation.xml')
    rels = parse(os.path.join(u, 'ppt/_rels/presentation.xml.rels'))
    rid_of = {'ppt/' + r.get('Target').lstrip('/').replace('ppt/', ''): r.get('Id') for r in rels.getroot()}
    pres = parse(pres_path)
    lst = pres.find('.//p:sldIdLst', NS)
    by_rid = {s.get(R + 'id'): s for s in lst}
    for s in list(lst):
        lst.remove(s)
    for c in created:
        lst.append(by_rid[rid_of[c]])
    save(pres, pres_path)
    subprocess.run([sys.executable, os.path.join(SK, 'clean.py'), u], cwd=SK, check=True, capture_output=True)
    return u, [os.path.join(u, c) for c in created]


# ---------------------------------------------------------------- tipos de diapositiva
def src_slide(src_dir, n):
    pres = open(os.path.join(src_dir, 'ppt/presentation.xml'), encoding='utf8').read()
    rels = open(os.path.join(src_dir, 'ppt/_rels/presentation.xml.rels'), encoding='utf8').read()
    m = {re.search(r'Id="(rId\d+)"', r).group(1): re.search(r'Target="([^"]+)"', r).group(1)
         for r in re.findall(r'<Relationship [^>]*/>', rels)}
    ids = re.findall(r'<p:sldId [^>]*r:id="(rId\d+)"', pres)
    return os.path.join(src_dir, 'ppt', m[ids[n - 1]])


def build_cfg(u, slide_path, src_dir, n, title, paras, algn='l', tag='img', callout_at=None, pic_index=0,
              skip_marks=(), relabel=None):
    """Diapositiva de configuración: captura del instructivo + marcos/números trasladados + globo USS."""
    t = parse(slide_path)
    spTree = t.find('.//p:spTree', NS)
    keep = {'Imagen 2', 'Picture 4', 'CuadroTexto 6', 'Rectángulo 7', 'CuadroTexto 5', 'Imagen 4'}
    for el in list(spTree):
        c = el.find('.//p:cNvPr', NS)
        if c is not None and c.get('name') not in keep and etree.QName(el).localname in ('sp', 'pic', 'cxnSp', 'grpSp'):
            spTree.remove(el)
    set_title(t, title)

    sp_path = src_slide(src_dir, n)
    st = parse(sp_path)
    s_pics = [p for p in st.find('.//p:spTree', NS) if etree.QName(p).localname == 'pic']
    srels = parse(sp_path.replace('/slides/', '/slides/_rels/') + '.rels')
    rels_path = slide_path.replace('/slides/', '/slides/_rels/') + '.rels'
    rt = parse(rels_path)
    pic = shape_by_name(t, 'Imagen 4')
    my_rid = pic.find('.//a:blip', NS).get(R + 'embed')
    boxes = [geo(sp) for sp in s_pics]
    sx = min(b[0] for b in boxes)
    sy = min(b[1] for b in boxes)
    sw = max(b[0] + b[2] for b in boxes) - sx
    sh = max(b[1] + b[3] for b in boxes) - sy
    X0, Y0, W, HMAX = 420559, 1012723, 11483600, 4830000
    k = min(W / sw, HMAX / sh)
    px, py = X0 + (W - sw * k) / 2, Y0
    mp = lambda x, y: (px + (x - sx) * k, py + (y - sy) * k)
    template_pic = etree.fromstring(etree.tostring(pic))
    next_rid = max(int(r.get('Id')[3:]) for r in rt.getroot()) + 1
    for i, s_pic in enumerate(s_pics):
        rid = s_pic.find('.//a:blip', NS).get(R + 'embed')
        target = [r.get('Target') for r in srels.getroot() if r.get('Id') == rid][0]
        img_src = os.path.normpath(os.path.join(os.path.dirname(sp_path), target))
        media_name = f'{tag}_{n}_{i}{os.path.splitext(img_src)[1]}'
        shutil.copy(img_src, os.path.join(u, 'ppt/media', media_name))
        if i == 0:
            cur, cur_rid = pic, my_rid
            for r in rt.getroot():
                if r.get('Id') == my_rid:
                    r.set('Target', '../media/' + media_name)
        else:
            cur = etree.fromstring(etree.tostring(template_pic))
            cur_rid = f'rId{next_rid}'; next_rid += 1
            rel = etree.SubElement(rt.getroot(), '{http://schemas.openxmlformats.org/package/2006/relationships}Relationship')
            rel.set('Id', cur_rid)
            rel.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image')
            rel.set('Target', '../media/' + media_name)
            cur.find('.//p:cNvPr', NS).set('id', str(next_id(t)))
            cur.find('.//p:cNvPr', NS).set('name', f'Imagen extra {i}')
            cur.find('.//a:blip', NS).set(R + 'embed', cur_rid)
            pic.addnext(cur)
            pic = cur
        src_rect = s_pic.find('.//a:srcRect', NS)
        blipFill = cur.find('.//p:blipFill', NS)
        old = blipFill.find('a:srcRect', NS)
        if old is not None:
            blipFill.remove(old)
        if src_rect is not None and src_rect.attrib:
            blipFill.insert(1, frag('<a:srcRect ' + ' '.join(f'{k_}="{v}"' for k_, v in src_rect.attrib.items()) + '/>'))
        bx, by, bw, bh = geo(s_pic)
        mx, my = mp(bx, by)
        set_xfrm(cur, mx, my, bw * k, bh * k)
    save(rt, rels_path)

    nid = next_id(t)
    new, callout_geo = [], None
    pics_bottom = sy + sh
    for el in st.find('.//p:spTree', NS):
        if etree.QName(el).localname != 'sp' or el.find('.//p:ph', NS) is not None:
            continue
        if el.find('.//a:xfrm', NS) is None:
            continue
        prst = el.find('.//a:prstGeom', NS)
        prst = prst.get('prst') if prst is not None else ''
        text = ''.join(el.itertext()).strip()
        x, y, w, h = geo(el)
        outside = y > pics_bottom - 20000
        if outside and (not text or re.fullmatch(r'[a-z]|\d{1,2}', text)):
            continue
        if prst == 'rect' and not text:
            mx, my = mp(x, y)
            new.append(highlight_xml(nid, mx, my, w * k, h * k)); nid += 1
        elif re.fullmatch(r'[a-z]|\d{1,2}', text) and w < 700000 and h < 700000:
            if text in skip_marks:
                continue
            mx, my = mp(x + w / 2, y + h / 2)
            new.append(marker_xml(nid, mx, my, (relabel or {}).get(text, text))); nid += 1
        elif prst == 'roundRect' and len(text) > 20:
            if callout_geo is None or w * h > callout_geo[2] * callout_geo[3]:
                callout_geo = (x, y, w, h)
    if callout_at:
        mx, my, cw = callout_at
    else:
        cx, cy, cw0, ch0 = callout_geo
        mx, my = mp(cx, cy)
        cw = min(max(cw0 * k, 5200000), 10800000)
    mx = min(max(mx, 900000), 11700000 - cw)
    chh = callout_height(paras, cw)
    my = min(my, 5850000 - chh)
    new.append(callout_xml(nid, mx, my, cw, chh, paras, algn))
    for x in new:
        spTree.append(frag(x))
    save(t, slide_path)


def build_div(slide_path, title, desc):
    t = parse(slide_path)
    set_first_run_text(shape_by_name(t, 'CuadroTexto 16'), title)
    set_first_run_text(shape_by_name(t, 'CuadroTexto 3'), desc)
    save(t, slide_path)


def build_cover(slide_path, title, label, subtitle):
    t = parse(slide_path)
    set_first_run_text(shape_by_name(t, 'CuadroTexto 16'), title)
    sid = next_id(t)
    p = ('<a:p><a:r><a:rPr lang="es-ES" sz="2000" b="1" dirty="0"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>'
         f'<a:latin typeface="Montserrat" pitchFamily="2" charset="0"/></a:rPr><a:t>{esc(label)}</a:t></a:r></a:p>'
         '<a:p><a:r><a:rPr lang="es-ES" sz="1600" dirty="0"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>'
         f'<a:latin typeface="Montserrat" pitchFamily="2" charset="0"/></a:rPr><a:t>{esc(subtitle)}</a:t></a:r></a:p>')
    t.find('.//p:spTree', NS).append(frag(textbox_xml(sid, 481781, 5130000, 5525729, 760000, p)))
    save(t, slide_path)


def build_bullets(slide_path, title, items, sz=1800):
    """Diapositiva de texto (definiciones/resumen) con viñetas USS."""
    t = parse(slide_path)
    set_title(t, title)
    body = shape_by_name(t, 'CuadroTexto 1')
    txBody = body.find('p:txBody', NS)
    for p_ in txBody.findall('a:p', NS):
        txBody.remove(p_)
    for it in items:
        txBody.append(frag(bullet_para(it, sz=sz)))
    save(t, slide_path)


def set_flow_boxes(slide_path, steps, note=None, highlight=()):
    """Reutiliza el diagrama de flujo de la plantilla: 7 pasos (texto, código) en el orden del recorrido."""
    t = parse(slide_path)
    order = ['CuadroTexto 13', 'CuadroTexto 16', 'CuadroTexto 18', 'CuadroTexto 40',
             'CuadroTexto 42', 'CuadroTexto 44', 'CuadroTexto 46']
    try:
        tut = shape_by_name(t, 'CuadroTexto 14')
        tut.getparent().remove(tut)
    except KeyError:
        pass
    for name, step in zip(order, steps):
        text, code = step[0], step[1]
        sz = step[2] if len(step) > 2 else 1400
        sp = shape_by_name(t, name)
        p_ = sp.find('.//a:p', NS)
        for r in p_.findall('a:r', NS):
            p_.remove(r)
        end = p_.find('a:endParaRPr', NS)
        runs = [f'<a:r><a:rPr lang="es-ES" sz="{sz}" dirty="0"/><a:t>{esc(text)} (</a:t></a:r>',
                f'<a:r><a:rPr lang="es-ES" sz="{sz}" b="1" dirty="0"><a:solidFill><a:schemeClr val="accent5"/>'
                f'</a:solidFill></a:rPr><a:t>{esc(code)}</a:t></a:r>',
                f'<a:r><a:rPr lang="es-ES" sz="{sz}" dirty="0"/><a:t>)</a:t></a:r>']
        for r in runs:
            el = frag(r)
            if end is not None:
                end.addprevious(el)
            else:
                p_.append(el)
    if highlight:
        boxes = [el for el in t.find('.//p:spTree', NS)
                 if etree.QName(el).localname == 'sp' and el.find('.//a:prstGeom', NS) is not None
                 and el.find('.//a:prstGeom', NS).get('prst') == 'roundRect']
        for i in highlight:
            name = order[i]
            tx, ty, _, _ = geo(shape_by_name(t, name))
            best = min(boxes, key=lambda b: abs(geo(b)[0] - tx) + abs(geo(b)[1] - ty))
            spPr = best.find('p:spPr', NS)
            spPr.append(frag('<a:solidFill><a:srgbClr val="F1E7FA"/></a:solidFill>'))
            spPr.append(frag(f'<a:ln w="38100"><a:solidFill><a:srgbClr val="{PURPLE}"/></a:solidFill></a:ln>'))
    if note:
        sid = next_id(t)
        t.find('.//p:spTree', NS).append(frag(callout_xml(sid, 2500000, 3000000, 6300000, 800000, note, 'ctr')))
    save(t, slide_path)


# ---------------------------------------------------------------- cierre del paquete
def finalize(u, out_path, title):
    """Deja el paquete como lo escribe PowerPoint y lo comprime."""
    subprocess.run([sys.executable, os.path.join(SK, 'clean.py'), u], cwd=SK, check=True, capture_output=True)
    rnd = random.Random(title)
    slides_dir = os.path.join(u, 'ppt/slides')
    n_slides = 0
    used = set()
    for f in sorted(os.listdir(slides_dir)):
        if not f.endswith('.xml'):
            continue
        n_slides += 1
        path = os.path.join(slides_dir, f)
        s = open(path, encoding='utf8').read()
        s = FOOTER_RE.sub(f'Elaborado por: {AUTHOR}', s)
        s = s.replace(' xml:space="preserve"', '')

        def new_cid(m):
            while True:
                v = rnd.randint(10 ** 9, 4294967295)
                if v not in used:
                    used.add(v)
                    return f'{m.group(1)}{v}"'
        s = re.sub(r'(<p14:creationId [^>]*val=")\d+"', new_cid, s)
        open(path, 'w', encoding='utf8').write(s)
    # declaraciones XML con comillas dobles, como las escribe Office
    for root_dir, _, files in os.walk(u):
        for f in files:
            if f.endswith('.xml') or f.endswith('.rels'):
                path = os.path.join(root_dir, f)
                s = open(path, encoding='utf8').read()
                s = re.sub(r"^<\?xml version='1.0' encoding='UTF-8' standalone='yes'\?>",
                           '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', s)
                open(path, 'w', encoding='utf8').write(s)
    # propiedades del documento
    app = os.path.join(u, 'docProps/app.xml')
    s = open(app, encoding='utf8').read()
    s = re.sub(r'<HeadingPairs>.*?</HeadingPairs>', '', s, flags=re.S)
    s = re.sub(r'<TitlesOfParts>.*?</TitlesOfParts>', '', s, flags=re.S)
    s = re.sub(r'<Slides>\d+</Slides>', f'<Slides>{n_slides}</Slides>', s)
    s = re.sub(r'<Words>\d+</Words>', '', s)
    s = re.sub(r'<Paragraphs>\d+</Paragraphs>', '', s)
    s = re.sub(r'<TotalTime>\d+</TotalTime>', '', s)
    open(app, 'w', encoding='utf8').write(s)
    core = os.path.join(u, 'docProps/core.xml')
    s = open(core, encoding='utf8').read()
    s = re.sub(r'<dc:title>.*?</dc:title>', f'<dc:title>{esc(title)}</dc:title>', s)
    s = re.sub(r'<dc:creator>.*?</dc:creator>', f'<dc:creator>{AUTHOR}</dc:creator>', s)
    s = re.sub(r'<cp:lastModifiedBy>.*?</cp:lastModifiedBy>', f'<cp:lastModifiedBy>{AUTHOR}</cp:lastModifiedBy>', s)
    open(core, 'w', encoding='utf8').write(s)
    # ZIP: [Content_Types].xml primero, sin entradas de carpeta
    if os.path.exists(out_path):
        os.remove(out_path)
    files = []
    for root_dir, _, fs in os.walk(u):
        for f in fs:
            full = os.path.join(root_dir, f)
            files.append(os.path.relpath(full, u).replace(os.sep, '/'))
    order = ['[Content_Types].xml', '_rels/.rels']
    files = order + sorted(f for f in files if f not in order)
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(os.path.join(u, f), f)
    return out_path


def to_pdf(pptx_path, pdf_path):
    pptx_path, pdf_path = os.path.abspath(pptx_path), os.path.abspath(pdf_path)
    tmp = os.path.join(os.path.dirname(pdf_path), '_pdf_tmp')
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    shutil.copy(pptx_path, os.path.join(tmp, 'deck.pptx'))
    subprocess.run([sys.executable, os.path.join(SK, 'office/soffice.py'), '--headless', '--convert-to', 'pdf',
                    '--outdir', tmp, os.path.join(tmp, 'deck.pptx')], cwd=os.path.join(SK, 'office'),
                   check=True, capture_output=True)
    shutil.move(os.path.join(tmp, 'deck.pdf'), pdf_path)
    shutil.rmtree(tmp, ignore_errors=True)
    return pdf_path
