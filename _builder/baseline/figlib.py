"""Shared SVG figure library for HKS Baseline Assessment NVR/maths figures.

Hand-specified puzzles built from parametric shapes: every content module
imports from here so geometry stays consistent and auditable. All layouts
return ONE self-contained <svg> string (sequence/grid + lettered answer row),
so the page's svgToPng/figs path works unchanged.
"""
import math

INK = "#1c2733"
GREY = "#9aa6b4"
FRAME = "#94a3b4"

# ---------------------------------------------------------------- primitives
def _g(cx, cy, rot, inner, mirror=False):
    t = f"translate({cx},{cy})" + (f" rotate({rot})" if rot else "") + (" scale(-1,1)" if mirror else "")
    return f'<g transform="{t}">{inner}</g>'

def circle(cx, cy, r, fill=INK):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2"/>'

def halfcircle(cx, cy, r, rot=0):
    """Left half filled, right half white; rotate for orientation."""
    return _g(cx, cy, rot,
              f'<circle cx="0" cy="0" r="{r}" fill="none" stroke="{INK}" stroke-width="2"/>'
              f'<path d="M0,{-r} A{r},{r} 0 0 0 0,{r} Z" fill="{INK}"/>')

def square(cx, cy, r, fill=INK, rot=0):
    return _g(cx, cy, rot, f'<rect x="{-r}" y="{-r}" width="{2*r}" height="{2*r}" fill="{fill}" stroke="{INK}" stroke-width="2"/>')

def halfsquare(cx, cy, r, rot=0):
    """Left half filled square; rotate for orientation."""
    return _g(cx, cy, rot,
              f'<rect x="{-r}" y="{-r}" width="{2*r}" height="{2*r}" fill="none" stroke="{INK}" stroke-width="2"/>'
              f'<rect x="{-r}" y="{-r}" width="{r}" height="{2*r}" fill="{INK}"/>')

def rect(cx, cy, w, h, fill=INK):
    return f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" fill="{fill}" stroke="{INK}" stroke-width="2"/>'

def triangle(cx, cy, r, fill=INK, rot=0):
    pts = f"0,{-r} {round(r*0.87,1)},{round(r*0.5,1)} {round(-r*0.87,1)},{round(r*0.5,1)}"
    return _g(cx, cy, rot, f'<polygon points="{pts}" fill="{fill}" stroke="{INK}" stroke-width="2"/>')

def diamond(cx, cy, r, fill=INK):
    return square(cx, cy, round(r*0.8, 1), fill, rot=45)

def _ngon(n, r, rot_deg=0.0):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n - math.pi / 2 + math.radians(rot_deg)
        pts.append(f"{round(r*math.cos(a),1)},{round(r*math.sin(a),1)}")
    return " ".join(pts)

def pentagon(cx, cy, r, fill=INK):
    return _g(cx, cy, 0, f'<polygon points="{_ngon(5, r)}" fill="{fill}" stroke="{INK}" stroke-width="2"/>')

def hexagon(cx, cy, r, fill=INK):
    return _g(cx, cy, 0, f'<polygon points="{_ngon(6, r)}" fill="{fill}" stroke="{INK}" stroke-width="2"/>')

def heptagon(cx, cy, r, fill=INK):
    return _g(cx, cy, 0, f'<polygon points="{_ngon(7, r)}" fill="{fill}" stroke="{INK}" stroke-width="2"/>')

def star(cx, cy, r, fill=INK):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        a = math.pi * i / 5 - math.pi / 2
        pts.append(f"{round(rr*math.cos(a),1)},{round(rr*math.sin(a),1)}")
    return _g(cx, cy, 0, f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{INK}" stroke-width="2"/>')

def trapezium(cx, cy, r, fill=INK):
    pts = f"{-r},{round(r*0.6,1)} {r},{round(r*0.6,1)} {round(r*0.55,1)},{round(-r*0.6,1)} {round(-r*0.55,1)},{round(-r*0.6,1)}"
    return _g(cx, cy, 0, f'<polygon points="{pts}" fill="{fill}" stroke="{INK}" stroke-width="2"/>')

def arrow(cx, cy, ln, rot=0, fill=INK):
    """Arrow pointing RIGHT at rot=0; rot in degrees clockwise."""
    h = round(ln * 0.28, 1); head = round(ln * 0.42, 1); tail = round(ln / 2, 1)
    pts = (f"{-tail},{-h/2} {tail-head},{-h/2} {tail-head},{-h} {tail},0 "
           f"{tail-head},{h} {tail-head},{h/2} {-tail},{h/2}")
    return _g(cx, cy, rot, f'<polygon points="{pts}" fill="{fill}" stroke="{INK}" stroke-width="2"/>')

def cross(cx, cy, r):
    return (f'<line x1="{cx-r}" y1="{cy-r}" x2="{cx+r}" y2="{cy+r}" stroke="{INK}" stroke-width="2.5"/>'
            f'<line x1="{cx-r}" y1="{cy+r}" x2="{cx+r}" y2="{cy-r}" stroke="{INK}" stroke-width="2.5"/>')

def plus(cx, cy, r):
    return (f'<line x1="{cx-r}" y1="{cy}" x2="{cx+r}" y2="{cy}" stroke="{INK}" stroke-width="2.5"/>'
            f'<line x1="{cx}" y1="{cy-r}" x2="{cx}" y2="{cy+r}" stroke="{INK}" stroke-width="2.5"/>')

def lshape(cx, cy, u, rot=0, mirror=False):
    """L-tetromino from unit squares of side u; mirror via scale(-1,1)."""
    pts = f"0,0 {u},0 {u},{2*u} {2*u},{2*u} {2*u},{3*u} 0,{3*u}"
    sc = " scale(-1,1)" if mirror else ""
    return (f'<g transform="translate({cx},{cy}) rotate({rot}){sc}">'
            f'<g transform="translate({-u},{round(-1.5*u,1)})">'
            f'<polygon points="{pts}" fill="{INK}" stroke="{INK}" stroke-width="1"/></g></g>')

def fshape(cx, cy, u, rot=0, mirror=False):
    """F-pentomino-ish chiral flag shape (stronger mirror discrimination)."""
    pts = f"0,0 {2*u},0 {2*u},{u} {u},{u} {u},{2*u} {2*u},{2*u} {2*u},{3*u} {u},{3*u} {u},{4*u} 0,{4*u}"
    return (f'<g transform="translate({cx},{cy}) rotate({rot}){" scale(-1,1)" if mirror else ""}">'
            f'<g transform="translate({-u},{-2*u})">'
            f'<polygon points="{pts}" fill="{INK}" stroke="{INK}" stroke-width="1"/></g></g>')

_DOTS = {0: [], 1: [(0, 0)], 2: [(-12, -12), (12, 12)], 3: [(-12, -12), (0, 0), (12, 12)],
         4: [(-12, -12), (12, -12), (-12, 12), (12, 12)],
         5: [(-12, -12), (12, -12), (0, 0), (-12, 12), (12, 12)],
         6: [(-12, -14), (12, -14), (-12, 0), (12, 0), (-12, 14), (12, 14)],
         7: [(-12, -14), (12, -14), (-12, 0), (0, 0), (12, 0), (-12, 14), (12, 14)]}

def dots(cx, cy, n, r=5, fill=INK):
    return "".join(circle(cx + dx, cy + dy, r, fill) for dx, dy in _DOTS[n])

# ------------------------------------------------------------- cell layouts
CELL = 64
GAP = 10

def _frame(x, y, s=CELL, qmark=False):
    out = f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="6" fill="#fff" stroke="{FRAME}" stroke-width="1.5"/>'
    if qmark:
        out += (f'<text x="{x+s/2}" y="{y+s/2+9}" text-anchor="middle" font-family="Arial" '
                f'font-size="26" font-weight="bold" fill="{GREY}">?</text>')
    return out

def _letter(x, y, ch):
    return (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Arial" '
            f'font-size="13" font-weight="bold" fill="{INK}">{ch}</text>')

def _optrow(out, opt_cells, x0, y2):
    for i, ch in enumerate("ABCDE"):
        x = x0 + i * (CELL + GAP)
        out.append(_frame(x, y2))
        out.append(opt_cells[i](x + CELL / 2, y2 + CELL / 2))
        out.append(_letter(x + CELL / 2, y2 + CELL + 16, ch))

def seq_fig(seq_cells, opt_cells):
    """Row 1: 4 given cells + '?'. Row 2: options A-E. Each cell = fn(cx,cy)->svg."""
    w = 5 * CELL + 4 * GAP + 12
    h = 2 * CELL + 46
    x0, y1, y2 = 6, 4, CELL + 26
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    for i in range(5):
        x = x0 + i * (CELL + GAP)
        out.append(_frame(x, y1, qmark=(i == 4)))
        if i < 4:
            out.append(seq_cells[i](x + CELL / 2, y1 + CELL / 2))
    _optrow(out, opt_cells, x0, y2)
    out.append("</svg>")
    return "".join(out)

def row_fig(opt_cells):
    """Odd-one-out: single row of 5 labelled cells."""
    w = 5 * CELL + 4 * GAP + 12
    h = CELL + 26
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    _optrow(out, opt_cells, 6, 2)
    out.append("</svg>")
    return "".join(out)

def matrix_fig(grid_cells, opt_cells):
    """3x3 grid (last cell '?') + options row A-E beneath."""
    MC = 56
    gw = 3 * MC + 2 * 8
    w = max(gw, 5 * CELL + 4 * GAP) + 12
    gx = (w - gw) / 2
    h = 3 * MC + 2 * 8 + CELL + 56
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    for i in range(9):
        r, c = divmod(i, 3)
        x = gx + c * (MC + 8); y = 4 + r * (MC + 8)
        out.append(_frame(x, y, MC, qmark=(i == 8)))
        if i < 8:
            out.append(grid_cells[i](x + MC / 2, y + MC / 2))
    _optrow(out, opt_cells, 6, 4 + 3 * MC + 2 * 8 + 18)
    out.append("</svg>")
    return "".join(out)

def analogy_fig(a_cell, b_cell, c_cell, opt_cells):
    """A is to B as C is to ? — top row [A][B]  :  [C][?], options beneath."""
    w = 5 * CELL + 4 * GAP + 12
    h = 2 * CELL + 46
    y1, y2 = 4, CELL + 26
    xs = [6, 6 + CELL + GAP]
    xr = [6 + 3 * (CELL + GAP) - 20, 6 + 4 * (CELL + GAP) - 20]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    out.append(_frame(xs[0], y1)); out.append(a_cell(xs[0] + CELL / 2, y1 + CELL / 2))
    out.append(_frame(xs[1], y1)); out.append(b_cell(xs[1] + CELL / 2, y1 + CELL / 2))
    mid = (xs[1] + CELL + xr[0]) / 2
    out.append(f'<text x="{mid}" y="{y1+CELL/2+6}" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold" fill="{GREY}">&#8594;</text>')
    out.append(_frame(xr[0], y1)); out.append(c_cell(xr[0] + CELL / 2, y1 + CELL / 2))
    out.append(_frame(xr[1], y1, qmark=True))
    _optrow(out, opt_cells, 6, y2)
    out.append("</svg>")
    return "".join(out)

def perimeter_fig():
    """L-shaped room, all six sides labelled. Perimeter = 6+2+3+2+3+4 = 20 m."""
    s = 34  # px per metre
    x0, y0 = 44, 20
    pts = [(0, 4), (6, 4), (6, 2), (3, 2), (3, 0), (0, 0)]
    poly = " ".join(f"{x0+x*s},{y0+y*s}" for x, y in pts)
    def lab(x, y, t, anchor="middle"):
        return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Arial" '
                f'font-size="14" fill="{INK}">{t}</text>')
    w, h = x0 + 6 * s + 44, y0 + 4 * s + 28
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<polygon points="{poly}" fill="#eef2f8" stroke="{INK}" stroke-width="2.5"/>'
            + lab(x0 + 3 * s, y0 + 4 * s + 18, "6 m")
            + lab(x0 + 6 * s + 8, y0 + 3 * s + 5, "2 m", "start")
            + lab(x0 + 4.5 * s, y0 + 2 * s - 8, "3 m")
            + lab(x0 + 3 * s + 8, y0 + 1 * s + 5, "2 m", "start")
            + lab(x0 + 1.5 * s, y0 - 6, "3 m")
            + lab(x0 - 8, y0 + 2 * s + 5, "4 m", "end")
            + "</svg>")

def labelled_shape_fig(draw, w, h):
    """Escape hatch for custom maths diagrams: draw(list_out, helpers)."""
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    draw(out)
    out.append("</svg>")
    return "".join(out)

def svg_text(x, y, t, size=14, anchor="middle", bold=False, fill=INK):
    wt = ' font-weight="bold"' if bold else ""
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Arial" '
            f'font-size="{size}"{wt} fill="{fill}">{t}</text>')

def zh_blocks(trad, simp):
    """Traditional and Simplified as separately headed blocks (Alex's rule)."""
    return (f'<div class="zhblk"><div class="zhh">繁體中文</div><div>{trad}</div></div>'
            f'<div class="zhblk"><div class="zhh">簡體中文</div><div>{simp}</div></div>')

def codes_fig(examples, target):
    """GL/CEM-style figure codes: example cells each labelled with a two-letter
    code, then a target cell marked '?'. The five OPTIONS are text codes, so
    every letter value needed for the target must appear among the examples."""
    n = len(examples)
    w = 6 + (n + 1) * (CELL + GAP) + 34
    h = CELL + 44
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    x = 6
    for fn, code in examples:
        out.append(_frame(x, 4))
        out.append(fn(x + CELL / 2, 4 + CELL / 2))
        out.append(svg_text(x + CELL / 2, 4 + CELL + 18, code, 14, bold=True))
        x += CELL + GAP
    out.append(f'<line x1="{x+2}" y1="4" x2="{x+2}" y2="{4+CELL+22}" stroke="{FRAME}" stroke-width="1.5"/>')
    x += 18
    out.append(_frame(x, 4))
    out.append(target(x + CELL / 2, 4 + CELL / 2))
    out.append(svg_text(x + CELL / 2, 4 + CELL + 18, "?", 16, bold=True, fill="#c0392b"))
    out.append("</svg>")
    return "".join(out)

# ---------------------------------------------------- CAT4-engine NVR loader
def nvr_from_json(band, version=1):
    """Load the pre-generated CAT4-engine NVR items (see gen_nvr.py)."""
    import json as _json
    import os as _os
    p = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), f"nvr_{band}_v{version}.json")
    out = []
    for it in _json.load(open(p)):
        out.append(dict(
            stem=it["instruction"],
            fig=f'<img src="{it["img"]}" style="width:100%;min-width:620px" alt="figure question">',
            options={k: "" for k in "ABCDE"},
            correct=it["answer"],
            strand=it["battery"],
            concept=f'CAT4 {it["subtype"]} (Level {it["gl_band"]}) · {it["rule"]}',
            explanation=it["rule"]))
    return out

# ---------------------------------------------------------- maths diagrams
def bar_chart(labels, values, ymax, ystep, unit="", hide=None, bar_fill="#72AFDB"):
    """Vertical bar chart. hide=index -> that bar renders as a '?' (missing bar)."""
    n = len(labels)
    bw, gap, x0, y0 = 46, 26, 56, 16
    ch = 180
    w = x0 + n * (bw + gap) + 24
    h = y0 + ch + 44
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    v = y0 + ch
    for yv in range(0, ymax + 1, ystep):
        yy = v - ch * yv / ymax
        out.append(f'<line x1="{x0-6}" y1="{yy}" x2="{w-16}" y2="{yy}" stroke="#dce3ea" stroke-width="1"/>')
        out.append(svg_text(x0 - 10, yy + 4, str(yv), 11, "end", fill="#5b6b7a"))
    out.append(f'<line x1="{x0-6}" y1="{y0-4}" x2="{x0-6}" y2="{v}" stroke="{INK}" stroke-width="1.5"/>')
    out.append(f'<line x1="{x0-6}" y1="{v}" x2="{w-16}" y2="{v}" stroke="{INK}" stroke-width="1.5"/>')
    for i, (lab, val) in enumerate(zip(labels, values)):
        x = x0 + i * (bw + gap)
        if hide == i:
            out.append(f'<rect x="{x}" y="{y0}" width="{bw}" height="{ch}" fill="none" stroke="{GREY}" stroke-width="1.5" stroke-dasharray="5,4" rx="3"/>')
            out.append(svg_text(x + bw / 2, y0 + ch / 2 + 8, "?", 24, bold=True, fill=GREY))
        else:
            bh = ch * val / ymax
            out.append(f'<rect x="{x}" y="{v-bh}" width="{bw}" height="{bh}" fill="{bar_fill}" stroke="{INK}" stroke-width="1.2"/>')
        out.append(svg_text(x + bw / 2, v + 18, lab, 12))
    if unit:
        out.append(svg_text(8, v + 18, unit, 11, "start", fill="#5b6b7a"))
    out.append("</svg>")
    return "".join(out)

def pictogram(rows, per, symbol_label):
    """rows = [(label, n_symbols)]; each symbol = `per` units."""
    x0, rh = 96, 34
    maxn = max(n for _, n in rows)
    w = x0 + maxn * 26 + 30
    h = 30 + len(rows) * rh + 8
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    out.append(svg_text(8, 18, f"{symbol_label} = {per}", 13, "start", bold=True))
    for r, (lab, n) in enumerate(rows):
        y = 30 + r * rh + rh / 2
        out.append(svg_text(x0 - 10, y + 4, lab, 13, "end"))
        for i in range(n):
            out.append(circle(x0 + 12 + i * 26, y, 9, "#72AFDB"))
        out.append(f'<line x1="{x0-4}" y1="{30 + r * rh}" x2="{x0-4}" y2="{30 + (r+1) * rh}" stroke="#dce3ea"/>')
    out.append("</svg>")
    return "".join(out)

def angles_on_line(known, colors=("#72AFDB", "#eef2f8")):
    """Angles on a straight line: rays from a point; angles labelled, last = x."""
    import math as _m
    cx, cy, R = 170, 128, 96
    w, h = 340, 150
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    out.append(f'<line x1="{cx-150}" y1="{cy}" x2="{cx+150}" y2="{cy}" stroke="{INK}" stroke-width="2"/>')
    angles = known + ["x"]
    total = 0
    vals = [a for a in known]
    xval = 180 - sum(vals)
    spans = vals + [xval]
    for i, (a, span) in enumerate(zip(angles, spans)):
        a0, a1 = total, total + span
        mid = _m.radians(180 - (a0 + a1) / 2)
        r0, r1 = _m.radians(180 - a0), _m.radians(180 - a1)
        arc_r = 34 + i * 12
        out.append(f'<path d="M {cx + arc_r*_m.cos(r0)} {cy - arc_r*_m.sin(r0)} A {arc_r} {arc_r} 0 0 1 {cx + arc_r*_m.cos(r1)} {cy - arc_r*_m.sin(r1)}" fill="none" stroke="{INK}" stroke-width="1.4"/>')
        lab = f"{a}°" if a != "x" else "x°"
        lr = arc_r + 16
        out.append(svg_text(cx + lr * _m.cos(mid), cy - lr * _m.sin(mid) + 4, lab, 14, bold=(a == "x")))
        if i < len(spans) - 1:
            re = _m.radians(180 - a1)
            out.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + R*_m.cos(re)}" y2="{cy - R*_m.sin(re)}" stroke="{INK}" stroke-width="2"/>')
        total = a1
    out.append("</svg>")
    return "".join(out)

def right_triangle_fig(base_label, height_label, hyp_label=""):
    """Right triangle, right angle at bottom-left; optional hypotenuse label."""
    x0, y0 = 40, 20
    b, ht = 240, 140
    w, h = x0 + b + 60, y0 + ht + 40
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    out.append(f'<polygon points="{x0},{y0+ht} {x0+b},{y0+ht} {x0},{y0}" fill="#eef2f8" stroke="{INK}" stroke-width="2.5"/>')
    out.append(f'<rect x="{x0}" y="{y0+ht-16}" width="16" height="16" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    out.append(svg_text(x0 + b / 2, y0 + ht + 22, base_label, 14))
    out.append(svg_text(x0 - 10, y0 + ht / 2, height_label, 14, "end"))
    if hyp_label:
        out.append(svg_text(x0 + b / 2 + 26, y0 + ht / 2 - 14, hyp_label, 14, "start"))
    out.append("</svg>")
    return "".join(out)

def spinner(sectors):
    """sectors = [(label, count, fill)]; draws count INDIVIDUAL equal slices per
    entry, each outlined and labelled, so '8 equal sectors' is countable."""
    import math as _m
    total = sum(c for _, c, _ in sectors)
    cx, cy, R = 110, 100, 82
    w, h = 320, 200
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    a0 = -90.0
    step = 360.0 / total
    for lab, cnt, fill in sectors:
        for _ in range(cnt):
            a1 = a0 + step
            x1, y1 = cx + R * _m.cos(_m.radians(a0)), cy + R * _m.sin(_m.radians(a0))
            x2, y2 = cx + R * _m.cos(_m.radians(a1)), cy + R * _m.sin(_m.radians(a1))
            out.append(f'<path d="M {cx} {cy} L {x1} {y1} A {R} {R} 0 0 1 {x2} {y2} Z" fill="{fill}" stroke="{INK}" stroke-width="1.6"/>')
            mid = _m.radians((a0 + a1) / 2)
            out.append(svg_text(cx + R * 0.62 * _m.cos(mid), cy + R * 0.62 * _m.sin(mid) + 4, lab, 12, bold=True))
            a0 = a1
    out.append(f'<polygon points="{cx-7},{cy-R-12} {cx+7},{cy-R-12} {cx},{cy-R+4}" fill="{INK}"/>')
    out.append("</svg>")
    return "".join(out)

def fraction_grid(rows, cols, shaded):
    """rows x cols grid with `shaded` cells filled."""
    s = 34
    x0, y0 = 8, 8
    w, h = x0 * 2 + cols * s, y0 * 2 + rows * s
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    k = 0
    for r in range(rows):
        for c in range(cols):
            fill = "#72AFDB" if k < shaded else "#fff"
            out.append(f'<rect x="{x0+c*s}" y="{y0+r*s}" width="{s}" height="{s}" fill="{fill}" stroke="{INK}" stroke-width="1.6"/>')
            k += 1
    out.append("</svg>")
    return "".join(out)

def line_graph(xlabels, values, ymax, ystep, unit=""):
    """Simple line graph (e.g. distance-time)."""
    n = len(xlabels)
    x0, y0, cw, ch = 56, 16, 300, 180
    w, h = x0 + cw + 30, y0 + ch + 44
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    v = y0 + ch
    for yv in range(0, ymax + 1, ystep):
        yy = v - ch * yv / ymax
        out.append(f'<line x1="{x0-6}" y1="{yy}" x2="{x0+cw}" y2="{yy}" stroke="#dce3ea"/>')
        out.append(svg_text(x0 - 10, yy + 4, str(yv), 11, "end", fill="#5b6b7a"))
    out.append(f'<line x1="{x0-6}" y1="{y0-4}" x2="{x0-6}" y2="{v}" stroke="{INK}" stroke-width="1.5"/>')
    out.append(f'<line x1="{x0-6}" y1="{v}" x2="{x0+cw}" y2="{v}" stroke="{INK}" stroke-width="1.5"/>')
    pts = []
    for i, val in enumerate(values):
        x = x0 + cw * i / (n - 1)
        y = v - ch * val / ymax
        pts.append(f"{x},{y}")
        out.append(circle(x, y, 4, INK))
        out.append(svg_text(x, v + 18, xlabels[i], 11))
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#14213A" stroke-width="2.2"/>')
    if unit:
        out.append(svg_text(8, v + 18, unit, 11, "start", fill="#5b6b7a"))
    out.append("</svg>")
    return "".join(out)

# convenience cell factories -------------------------------------------------
def cell(fn, *args, **kw):
    """cell(triangle, 20, INK, rot=90) -> lambda cx,cy: triangle(cx,cy,20,INK,rot=90)"""
    return lambda cx, cy: fn(cx, cy, *args, **kw)

def multi(*fns):
    """Compose several cell fns into one cell."""
    return lambda cx, cy: "".join(f(cx, cy) for f in fns)

def offset(fn, dx, dy):
    return lambda cx, cy: fn(cx + dx, cy + dy)

def counted(fn, n, r, spread=15, **kw):
    """n small shapes in a row inside one cell."""
    def c(cx, cy):
        if n == 1: xs = [0]
        elif n == 2: xs = [-spread * .75, spread * .75]
        elif n == 3: xs = [-spread, 0, spread]
        else: xs = [-spread, 0, spread, 0]
        out = "".join(fn(cx + x, cy, r, **kw) for x in xs[:min(n, 3)])
        if n >= 4:
            out += fn(cx, cy - spread, r, **kw)
        return out
    return c
