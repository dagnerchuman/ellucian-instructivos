# -*- coding: utf-8 -*-
"""Piezas nativas (editables) para diapositivas USS: texto enriquecido, tablas, tarjetas, chevrones y conectores."""
import re

from ussdeck import (NS, SLIDE_W, est_lines, esc, frag, montserrat_bold_emu, next_id, parse, save, set_first_run_text,
                     set_xfrm, shape_by_name)

X0, XW = 431320, 11329360
XR = X0 + XW
YT, YB = 900000, 5850000

INK, MUT, SOFT = '1E1E24', '5F5F6B', '3A3A44'
PUR, PURD, PURL, PURB, ZEB, LINE = '7030A0', '5C2193', 'F1E7FA', 'DCC8EE', 'FBF8FD', 'E4DFEA'
GRN, GRND, GRNL, GRNB = '4EA72E', '2F6B1B', 'EDF7E8', 'BFE0B0'
AMB, AMBD, AMBL, AMBP = 'E0A100', '8A5A00', 'FFF8E8', 'FFF3DC'
RED, REDL, ORG, AQU = 'A11D1D', 'FDE7E7', 'EB6834', '1BAF7A'
GRAYL = 'F2F2F5'

CODE_RE = re.compile(r'\b([SGT][A-Z]{2}[A-Z0-9]{3,5})\b')


# ------------------------------------------------------------------ texto
def rich(text, color=INK, bold=False, code_color=PURD):
    """'texto con **negrita** y CÓDIGOS' -> [(texto, negrita, color)]."""
    out = []
    for part in re.split(r'(\*\*.+?\*\*)', text):
        if not part:
            continue
        b = bold
        if part.startswith('**') and part.endswith('**'):
            part, b = part[2:-2], True
        pos = 0
        for m in CODE_RE.finditer(part):
            if m.start() > pos:
                out.append((part[pos:m.start()], b, color))
            out.append((m.group(1), True, code_color))
            pos = m.end()
        if pos < len(part):
            out.append((part[pos:], b, color))
    return out


def r_xml(t, sz, bold=False, color=INK, font=None, italic=False):
    b = ' b="1"' if bold else ''
    i = ' i="1"' if italic else ''
    latin = f'<a:latin typeface="{font}"/>' if font else ''
    return (f'<a:r><a:rPr lang="es-PE" sz="{int(sz)}"{b}{i} dirty="0"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'{latin}</a:rPr><a:t>{esc(t)}</a:t></a:r>')


def p_xml(items, sz, algn='l', color=INK, bold=False, font=None, spc_after=0, code_color=PURD, italic=False):
    runs = rich(items, color, bold, code_color) if isinstance(items, str) else items
    body = ''.join(r_xml(t, sz, b, c, font, italic) for t, b, c in runs)
    spc = f'<a:spcAft><a:spcPts val="{spc_after}"/></a:spcAft>' if spc_after else ''
    return (f'<a:p><a:pPr algn="{algn}">{spc}<a:buNone/></a:pPr>{body}'
            f'<a:endParaRPr lang="es-PE" sz="{int(sz)}" dirty="0"/></a:p>')


def plain(text):
    if isinstance(text, list):          # párrafo dado como lista de runs
        text = ''.join(t for t, *_ in text)
    return re.sub(r'\*\*', '', text)


def text_h(texts, w, sz, em=0.55, ls=1.2):
    """Alto estimado (EMU) de uno o varios párrafos en un ancho útil w."""
    if isinstance(texts, str):
        texts = [texts]
    lines = sum(est_lines(plain(t), w + 182880, sz / 100, em) for t in texts)
    return int(lines * sz / 100 * ls * 12700)


def text_w(text, sz, em=0.52):
    return int(len(plain(text)) * sz / 100 * em * 12700)


# ------------------------------------------------------------------ formas
def shape_xml(sid, x, y, w, h, geom='rect', fill=None, line=None, line_w=12700, dash=None, paras='', anchor='t',
              ins=(91440, 45720, 91440, 45720), adj=None, name='Forma'):
    av = f'<a:avLst><a:gd name="adj" fmla="val {int(adj)}"/></a:avLst>' if adj is not None else '<a:avLst/>'
    fill_xml = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else '<a:noFill/>'
    if line:
        d = f'<a:prstDash val="{dash}"/>' if dash else ''
        ln = f'<a:ln w="{int(line_w)}"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill>{d}</a:ln>'
    else:
        ln = '<a:ln><a:noFill/></a:ln>'
    l, t, r, b = (int(v) for v in ins)
    body = paras or '<a:p><a:endParaRPr lang="es-PE" dirty="0"/></a:p>'
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="{name} {sid}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="{geom}">{av}</a:prstGeom>{fill_xml}{ln}</p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" lIns="{l}" tIns="{t}" rIns="{r}" bIns="{b}" rtlCol="0" anchor="{anchor}">'
            f'<a:noAutofit/></a:bodyPr><a:lstStyle/>{body}</p:txBody></p:sp>')


def poly_xml(sid, pts, color='4A4A55', w=15875, dash=None, arrow=True):
    """Línea poligonal abierta (forma libre) con punta de flecha al final."""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    pad = 6350
    if maxx - minx < 2 * pad:
        minx, maxx = minx - pad, maxx + pad
    if maxy - miny < 2 * pad:
        miny, maxy = miny - pad, maxy + pad
    W, H = int(maxx - minx), int(maxy - miny)
    path = f'<a:moveTo><a:pt x="{int(pts[0][0] - minx)}" y="{int(pts[0][1] - miny)}"/></a:moveTo>'
    path += ''.join(f'<a:lnTo><a:pt x="{int(x - minx)}" y="{int(y - miny)}"/></a:lnTo>' for x, y in pts[1:])
    d = f'<a:prstDash val="{dash}"/>' if dash else ''
    tail = '<a:tailEnd type="triangle" w="med" len="med"/>' if arrow else ''
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Conector {sid}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{int(minx)}" y="{int(miny)}"/><a:ext cx="{W}" cy="{H}"/></a:xfrm>'
            f'<a:custGeom><a:avLst/><a:gdLst/><a:ahLst/><a:cxnLst/><a:rect l="0" t="0" r="r" b="b"/>'
            f'<a:pathLst><a:path w="{W}" h="{H}" fill="none">{path}</a:path></a:pathLst></a:custGeom>'
            f'<a:noFill/><a:ln w="{int(w)}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>{d}<a:round/>{tail}</a:ln>'
            f'</p:spPr></p:sp>')


# ------------------------------------------------------------------ tablas
def tbl_xml(sid, x, y, widths, header, rows, sz=1050, hsz=None, zebra=True, hfill=PUR):
    """widths: EMU por columna. Celdas: texto o dict(text, fill, color, bold, algn, sz). Devuelve (xml, alto)."""
    hsz = hsz or sz
    mar_lr, mar_tb = 64008, 36576

    def norm(c):
        return c if isinstance(c, dict) else {'text': c}

    def row_h(cells, head):
        h = 0
        for c, w in zip(cells, widths):
            c = norm(c)
            s = c.get('sz', hsz if head else sz)
            t = c.get('text', '')
            h = max(h, text_h(t if isinstance(t, list) else [t], w - 2 * mar_lr, s))
        return int(h + 2 * mar_tb + 30000)

    def tc(c, head, ri):
        c = norm(c)
        text = c.get('text', '')
        fill = c.get('fill') or (hfill if head else (ZEB if zebra and ri % 2 == 1 else 'FFFFFF'))
        color = c.get('color', 'FFFFFF' if head else INK)
        bold = c.get('bold', head)
        algn = c.get('algn', 'l')
        s = c.get('sz', hsz if head else sz)
        paras = text if isinstance(text, list) else [text]
        body = ''.join(p_xml(p, s, algn=algn, color=color, bold=bold, code_color='FFFFFF' if head else PURD) for p in paras)
        lines = ''.join(f'<a:{e} w="9525"><a:solidFill><a:srgbClr val="{LINE}"/></a:solidFill></a:{e}>'
                        for e in ('lnL', 'lnR', 'lnT', 'lnB'))
        return (f'<a:tc><a:txBody><a:bodyPr/><a:lstStyle/>{body}</a:txBody>'
                f'<a:tcPr marL="{mar_lr}" marR="{mar_lr}" marT="{mar_tb}" marB="{mar_tb}" anchor="ctr">{lines}'
                f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill></a:tcPr></a:tc>')

    grid = ''.join(f'<a:gridCol w="{int(w)}"/>' for w in widths)
    hh = row_h(header, True)
    trs = f'<a:tr h="{hh}">' + ''.join(tc(c, True, 0) for c in header) + '</a:tr>'
    total = hh
    for ri, r in enumerate(rows):
        rh = row_h(r, False)
        total += rh
        trs += f'<a:tr h="{rh}">' + ''.join(tc(c, False, ri) for c in r) + '</a:tr>'
    xml = (f'<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="{sid}" name="Tabla {sid}"/>'
           f'<p:cNvGraphicFramePr><a:graphicFrameLocks noGrp="1"/></p:cNvGraphicFramePr><p:nvPr/></p:nvGraphicFramePr>'
           f'<p:xfrm><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(sum(widths))}" cy="{int(total)}"/></p:xfrm>'
           f'<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">'
           f'<a:tbl><a:tblPr firstRow="1" bandRow="1"/><a:tblGrid>{grid}</a:tblGrid>{trs}</a:tbl>'
           f'</a:graphicData></a:graphic></p:graphicFrame>')
    return xml, total


def fit_sz(w, perc, header, rows, y, limit, lo=1000, hi=1500, step=50, hfill=PUR):
    """Mayor tamaño de letra con el que la tabla cabe entre y y limit."""
    ws = cols(w, perc)
    for s in range(hi, lo - 1, -step):
        _, h = tbl_xml(0, 0, 0, ws, header, rows, sz=s, hsz=s, hfill=hfill)
        if y + h <= limit:
            return s
    return lo


def cols(total, perc):
    s = sum(perc)
    ws = [int(total * p / s) for p in perc]
    ws[-1] += int(total) - sum(ws)
    return ws


# ------------------------------------------------------------------ diapositiva
def set_title2(tree, text):
    """Título USS; reduce el tamaño si el texto no cabe y ubica la barra degradada a continuación."""
    title = shape_by_name(tree, 'CuadroTexto 6')
    set_first_run_text(title, text)
    pt = 28
    while montserrat_bold_emu(text, pt) + 212880 > 10900000 and pt > 16:
        pt -= 1
    rpr = title.find('.//a:r/a:rPr', NS)
    rpr.set('sz', str(pt * 100))
    w = montserrat_bold_emu(text, pt) + 212880
    title.find('.//a:xfrm', NS).find('a:ext', NS).set('cx', str(int(w)))
    bx = min(431320 + w, SLIDE_W - 600000)
    set_xfrm(shape_by_name(tree, 'Rectángulo 7'), bx, 241540, SLIDE_W - bx, 445583)


class Slide:
    def __init__(self, path, title=None, keep_body=False):
        self.path = path
        self.t = parse(path)
        self.tree = self.t.find('.//p:spTree', NS)
        if title:
            set_title2(self.t, title)
        if not keep_body:
            try:
                self.tree.remove(shape_by_name(self.t, 'CuadroTexto 1'))
            except KeyError:
                pass
        self.sid = next_id(self.t)
        self.y = YT

    def nid(self):
        self.sid += 1
        return self.sid - 1

    def add(self, xml):
        self.tree.append(frag(xml))

    def save(self):
        save(self.t, self.path)

    # ---- bloques de uso frecuente
    def text(self, text, sz=1400, color=MUT, x=X0, w=XW, y=None, gap=90000, algn='l', bold=False):
        y = self.y if y is None else y
        h = text_h(text, w, sz) + 20000
        self.add(shape_xml(self.nid(), x, y, w, h, paras=p_xml(text, sz, algn=algn, color=color, bold=bold), ins=(0, 0, 0, 0)))
        self.y = y + h + gap
        return h

    def note(self, text, kind='info', x=X0, w=XW, y=None, sz=1300, gap=90000, h=None, anchor='ctr'):
        fill, line = {'info': (GRNL, GRNB), 'warn': (AMBL, 'F2DDA4'), 'purple': (PURL, PURB)}[kind]
        y = self.y if y is None else y
        paras = text if isinstance(text, list) else [text]
        h = h or text_h(paras, w - 2 * 137160, sz) + 2 * 64008 + 50000
        body = ''.join(p_xml(p, sz, color=INK, spc_after=300 if len(paras) > 1 else 0) for p in paras)
        self.add(shape_xml(self.nid(), x, y, w, h, geom='roundRect', adj=9000, fill=fill, line=line, paras=body,
                           anchor=anchor, ins=(137160, 64008, 137160, 64008), name='Nota'))
        self.y = y + h + gap
        return h

    def table(self, perc, header, rows, x=X0, w=XW, y=None, sz=None, hsz=None, gap=100000, hfill=PUR, zebra=True, reserve=0,
              lo=1000, hi=1500):
        y = self.y if y is None else y
        if sz is None:
            sz = fit_sz(w, perc, header, rows, y, YB - reserve, lo, hi, hfill=hfill)
        xml, h = tbl_xml(self.nid(), x, y, cols(w, perc), header, rows, sz=sz, hsz=hsz or sz, hfill=hfill, zebra=zebra)
        self.add(xml)
        self.y = y + h + gap
        return h

    def chevrons(self, items, y=None, h=560000, sz=1100, fill=PUR, gap=40000, x=X0, w=XW):
        """items: (título, subtítulo). Primera flecha 'homePlate', luego 'chevron'."""
        y = self.y if y is None else y
        n = len(items)
        cw = (w - (n - 1) * gap) / n
        for i, (title, sub) in enumerate(items):
            paras = p_xml([(f'{i + 1}  ', True, 'FFFFFF'), (title, True, 'FFFFFF')], sz)
            if sub:
                paras += p_xml(sub, sz - 150, color='EDE0F8', code_color='FFFFFF')
            self.add(shape_xml(self.nid(), x + i * (cw + gap), y, cw, h, geom='homePlate' if i == 0 else 'chevron', adj=28000,
                               fill=fill, paras=paras, anchor='ctr', ins=(110000 if i == 0 else 230000, 20000, 170000, 20000),
                               name='Paso'))
        self.y = y + h + 110000

    def card(self, x, y, w, h, title, question=None, text=None, accent=PUR, num=None, fill='FFFFFF', tsz=1300, sz=1100,
             line=LINE):
        paras = p_xml(([(f'{num}  ', True, accent)] if num else []) + [(title, True, INK)], tsz, font='Montserrat', spc_after=400)
        if question:
            paras += p_xml(question, sz, color=PURD, bold=True, spc_after=300)
        if text:
            for t in (text if isinstance(text, list) else [text]):
                paras += p_xml(t, sz, color=SOFT, spc_after=300)
        self.add(shape_xml(self.nid(), x, y, w, h, geom='roundRect', adj=5000, fill=fill, line=line, paras=paras,
                           ins=(137160, 150000, 137160, 91440), name='Tarjeta'))
        self.add(shape_xml(self.nid(), x + 70000, y, w - 140000, 55000, fill=accent, name='Acento'))

    def pill(self, x, y, w, h, text, fill, color, sz=900, line=None):
        self.add(shape_xml(self.nid(), x, y, w, h, geom='roundRect', adj=50000, fill=fill, line=line,
                           paras=p_xml(text, sz, algn='ctr', color=color, bold=True), anchor='ctr', ins=(20000, 0, 20000, 0),
                           name='Etiqueta'))
