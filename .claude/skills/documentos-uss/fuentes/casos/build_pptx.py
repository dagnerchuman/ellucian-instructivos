# -*- coding: utf-8 -*-
"""PPTX (plantilla USS): casuísticas para las pruebas integrales. Mismo contenido que el PDF."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
USS = os.path.dirname(HERE)
sys.path.insert(0, USS)
sys.path.insert(0, HERE)
sys.path.insert(1, '/home/user/ellucian-instructivos/.claude/skills/documentos-uss/scripts/pdf')
import common as GL  # noqa: E402  (glosario: SIGLAS, PAGINAS, _TERM_RE)
import casos_data as D  # noqa: E402
from pptlib import *  # noqa: E402,F401,F403
from ussdeck import build_cover, build_structure, finalize  # noqa: E402

OUT = os.path.join(USS, 'entregables', 'CASUÍSTICAS PARA LAS PRUEBAS INTEGRALES - ESTUDIANTES Y DOCENTES.pptx')
USADOS = set()
UNA_VEZ = set()
FAM_COL = {'D': (PURD, PURL), 'E': ('0E8A5F', 'E4F5EE'), 'Q': ('C2501C', 'FDEDE4')}


def ex(text, seen):
    """Agrega «(significado)» a la primera aparición de cada sigla o página en la diapositiva."""
    out, last = [], 0
    for m in GL._TERM_RE.finditer(text):
        term = m.group(0)
        if m.group(2) is None and not term.isupper():
            continue
        key, mean = GL._meaning(term)
        if key in seen or key in UNA_VEZ:
            continue
        seen.add(key)
        USADOS.add(key)
        if key == 'SEUSS':
            UNA_VEZ.add(key)
        pre = text[:m.start()]
        d = pre.count('(') - pre.count(')')
        out.append(text[last:m.end()] + (f': {mean}' if d > 0 else f' ({mean})'))
        last = m.end()
    out.append(text[last:])
    return ''.join(out)


def para(runs, spc_after=0, algn='l'):
    """runs: [(texto, tamaño, negrita, color)]; el texto admite **negrita** y códigos coloreados."""
    body = ''
    for t, sz, b, c in runs:
        for tt, bb, cc in rich(t, c, b):
            body += r_xml(tt, sz, bb, cc)
    spc = f'<a:spcAft><a:spcPts val="{spc_after}"/></a:spcAft>' if spc_after else ''
    return f'<a:p><a:pPr algn="{algn}">{spc}<a:buNone/></a:pPr>{body}<a:endParaRPr lang="es-PE" dirty="0"/></a:p>'


def box(S, x, y, w, h, paras, fill='FFFFFF', line=LINE, anchor='t', ins=(150000, 110000, 150000, 90000), name='Bloque'):
    S.add(shape_xml(S.nid(), x, y, w, h, geom='roundRect', adj=6000, fill=fill, line=line, paras=paras, anchor=anchor, ins=ins,
                    name=name))


def fits(texts, w, sz, avail, extra=0):
    return text_h(texts, w, sz) + extra <= avail


# ------------------------------------------------------------------ diapositivas
def s_cover(p):
    build_cover(p, 'CASUÍSTICAS', 'PRUEBAS INTEGRALES: ESTUDIANTES Y DOCENTES',
                'Qué hace Banner en cada caso y qué queda fuera del sistema')


def s_que_es(p):
    S = Slide(p, '¿QUÉ ES UNA CASUÍSTICA?')
    seen = set()
    S.note(ex('Un **caso real** que se prueba de inicio a fin en Banner, antes de salir a producción. Cada caso se revisa con los mismos '
              'cinco pasos:', seen), kind='purple', sz=1500)
    S.chevrons([('Situación', 'Qué pasa'), ('En Banner', 'Páginas y cita'), ('Resultado', 'Lo que se espera'),
                ('Fuera de Banner', 'Lo decide la USS'), ('En los centros', 'Ejemplo')], h=720000, sz=1250)
    gap = 180000
    cw = (XW - 2 * gap) / 3
    y = S.y + 60000
    for i, (k, (fam, _)) in enumerate(D.FAMILIAS.items()):
        col, light = FAM_COL[k]
        casos = [c for c in D.CASOS if c['id'][0] == k]
        paras = para([(fam, 1700, True, col)], spc_after=600)
        paras += ''.join(para([(c['id'] + '  ', 1350, True, col), (c['titulo'], 1350, False, INK)], spc_after=400) for c in casos)
        box(S, X0 + i * (cw + gap), y, cw, YB - y, paras, fill=light, line=light, name='Grupo')
    S.save()


def s_muestra(p):
    S = Slide(p, 'LA MUESTRA QUE YA TENÍAMOS')
    seen = set()
    S.text('Propuesta en «Validación de la migración» (25/09): 16 participantes por programa de cada centro y 8 escenarios de riesgo.',
           sz=1400)
    lw = XW * 0.5
    y0 = S.y
    rows = [[ex(t, seen), {'text': str(n), 'algn': 'ctr', 'bold': True, 'color': PURD}] for t, n in D.MUESTRA]
    rows.append([{'text': 'Total por programa', 'bold': True, 'fill': PURL},
                 {'text': str(sum(n for _, n in D.MUESTRA)), 'algn': 'ctr', 'bold': True, 'color': PURD, 'fill': PURL}])
    S.table([82, 18], ['Tipo de participante', 'Cant.'], rows, w=lw, hi=1400)
    rx, rw = X0 + lw + 220000, XW - lw - 220000
    items = [ex(e, seen) for e in D.ESCENARIOS]
    paras = para([('Escenarios de riesgo de la migración', 1450, True, PURD)], spc_after=500)
    paras += ''.join(para([(f'{i}.  ', 1250, True, PURD), (t, 1250, False, INK)], spc_after=250) for i, t in enumerate(items, 1))
    h1 = YB - y0 - 1000000
    box(S, rx, y0, rw, h1, paras)
    box(S, rx, y0 + h1 + 120000, rw, 880000,
        para([('Estos casos prueban que los **datos migrados** estén bien. Las casuísticas nuevas prueban **situaciones de la vida '
               'real** con estudiantes y docentes.', 1300, False, INK)]), fill=GRNL, line=GRNB, anchor='ctr', name='Nota')
    S.save()


def s_caso(c):
    def fn(p):
        col, light = FAM_COL[c['id'][0]]
        S = Slide(p, f'{c["id"]} · {c["titulo"].upper()}')
        seen = set()
        sit = ex(c['situacion'], seen)
        S.note([[('Situación:  ', True, col)] + rich(sit)], kind='purple', sz=1450, gap=140000)
        y0 = S.y
        lw = XW * 0.58
        rx, rw = X0 + lw + 200000, XW - lw - 200000
        avail = YB - y0
        pasos = [(ex(t, seen), k) for t, k in c['pasos']]
        right = [('Resultado esperado', ex(c['resultado'], seen), GRNL, GRND),
                 ('Fuera de Banner', ex(c['fuera'], seen), AMBL, AMBD),
                 ('En los centros', ex(c['centros'], seen), GRAYL, MUT)]
        # tamaño de letra que cabe
        for sz in range(1700, 1049, -50):
            lt = [f'{i}. {t}  {("Instructivo " if k[0].isdigit() else "") + k}' for i, (t, k) in enumerate(pasos, 1)]
            hl = text_h(['En Banner'] + lt, lw - 300000, sz) + len(lt) * 700 * 127 + 420000
            hr = sum(text_h([lab, t], rw - 300000, sz) + 330000 for lab, t, _, _ in right) + 2 * 120000
            if hl <= avail and hr <= avail:
                break
        paras = para([('En Banner', sz + 150, True, PURD)], spc_after=500)
        for i, (t, k) in enumerate(pasos, 1):
            cite = ('Instructivo ' if k[0].isdigit() else '') + k
            paras += para([(f'{i}.  ', sz, True, col), (t, sz, False, INK), (f'   {cite}', sz - 300, False, MUT)], spc_after=700)
        box(S, X0, y0, lw, avail, paras)
        hs = [text_h([lab, t], rw - 300000, sz) + 330000 for lab, t, _, _ in right]
        extra = (avail - sum(hs) - 2 * 120000) / 3
        y = y0
        for (lab, t, fill, tc), h in zip(right, hs):
            h = h + extra
            box(S, rx, y, rw, h, para([(lab, sz - 100, True, tc)], spc_after=300) + para([(t, sz, False, INK)]),
                fill=fill, line=fill, anchor='ctr', name=lab)
            y += h + 120000
        S.save()
    return fn


def s_sino(p):
    S = Slide(p, 'QUÉ HACE ELLUCIAN Y QUÉ NO')
    seen = set()
    si, no = D.SI_NO
    gap = 220000
    cw = (XW - gap) / 2
    y0 = YT + 60000
    for i, (tit, items, fill, head) in enumerate([('Banner lo hace', si, GRNL, GRND),
                                                   ('Lo decide la USS, fuera de Banner', no, AMBL, AMBD)]):
        x = X0 + i * (cw + gap)
        S.add(shape_xml(S.nid(), x, y0, cw, 560000, geom='roundRect', adj=12000, fill=head,
                        paras=p_xml(tit, 1700, color='FFFFFF', bold=True, font='Montserrat'), anchor='ctr',
                        ins=(180000, 0, 180000, 0), name='Encabezado'))
        paras = ''.join(para([('›  ', 1650, True, head), (ex(t, seen), 1650, False, INK)], spc_after=1000) for t in items)
        box(S, x, y0 + 640000, cw, YB - y0 - 640000, paras, fill=fill, line=fill, ins=(200000, 200000, 200000, 120000))
    S.save()


def s_check(p):
    S = Slide(p, 'PARA LAS PRUEBAS INTEGRALES (16/11 AL 26/12)')
    seen = set()
    rows = []
    for c in D.CASOS:
        col, light = FAM_COL[c['id'][0]]
        for j, x in enumerate(c['prueba']):
            first = j == 0
            rows.append([{'text': [[(c['id'] + '  ', True, col)] + rich(c['titulo'])] if first else '', 'fill': 'FFFFFF'},
                         {'text': ex(x, seen), 'fill': 'FFFFFF'}, {'text': '', 'fill': 'FFFFFF'}])
    S.table([34, 56, 10], ['Caso', 'Qué probar y qué debe pasar', 'OK'], rows, zebra=False, lo=950, hi=1300)
    S.save()


def s_glosario(p):
    S = Slide(p, 'GLOSARIO')
    items = [(k if not k.islower() else k.capitalize(), GL.SIGLAS[k][0]) for k in sorted((k for k in USADOS if k in GL.SIGLAS), key=str.lower)]
    items += [(k, GL.PAGINAS[k]) for k in sorted(k for k in USADOS if k in GL.PAGINAS)]
    half = (len(items) + 1) // 2
    left, right = items[:half], items[half:]
    rows = []
    for i in range(half):
        a = left[i]
        b = right[i] if i < len(right) else ('', '')
        rows.append([{'text': a[0], 'bold': True, 'color': PURD}, a[1][0].upper() + a[1][1:],
                     {'text': b[0], 'bold': True, 'color': PURD}, (b[1][0].upper() + b[1][1:]) if b[1] else ''])
    S.table([13, 37, 13, 37], ['Sigla o página', 'Significado', 'Sigla o página', 'Significado'], rows, lo=900, hi=1500)
    S.save()


def s_dudas(p):
    S = Slide(p, 'DUDAS PARA CONFIRMAR')
    gap = 220000
    cw = (XW - gap) / 2
    y0 = YT + 60000
    n = 1
    for i, (tit, items, head, fill) in enumerate([('Para Ellucian', D.DUDAS_E, PUR, PURL), ('Para la USS', D.DUDAS_U, AMBD, AMBL)]):
        seen = set()
        x = X0 + i * (cw + gap)
        S.add(shape_xml(S.nid(), x, y0, cw, 520000, geom='roundRect', adj=12000, fill=head,
                        paras=p_xml(tit, 1700, color='FFFFFF', bold=True, font='Montserrat'), anchor='ctr',
                        ins=(180000, 0, 180000, 0), name='Encabezado'))
        for sz in range(1700, 999, -50):
            if text_h([ex(q, set()) for q in items], cw - 400000, sz) + len(items) * sz * 7 <= YB - y0 - 800000:
                break
        paras = ''
        for q in items:
            paras += para([(f'{n}.  ', sz, True, head), (ex(q, seen), sz, False, INK)], spc_after=700)
            n += 1
        box(S, x, y0 + 600000, cw, YB - y0 - 600000, paras, fill=fill, line=fill, ins=(200000, 180000, 200000, 120000))
    S.save()


def main():
    plan = [('cover', s_cover), ('text', s_que_es), ('text', s_muestra)]
    plan += [('text', s_caso(c)) for c in D.CASOS]
    plan += [('text', s_sino), ('text', s_check), ('text', s_glosario), ('text', s_dudas), ('close', None)]
    u, paths = build_structure(os.path.join(HERE, 'deck'), [k for k, _ in plan])
    later = []
    for (kind, fn), path in zip(plan, paths):
        if fn is s_glosario:          # el glosario va al final, cuando ya se conocen todos los términos usados
            later.append((fn, path))
        elif fn:
            fn(path)
    for fn, path in later:
        fn(path)
    finalize(u, OUT, 'Casuísticas para las pruebas integrales - Estudiantes y docentes')
    print('OK', OUT, len(paths), 'diapositivas')


if __name__ == '__main__':
    main()
