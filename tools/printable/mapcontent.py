"""Turn a portal MAP paper into house-style paper content.

Source of truth is the live online test: prep-portal/map-tests/<path>/index.html
(the QUESTIONS array) joined to test-banks/map-tests/<path>/bank.csv for the key.
Nothing here rewrites a question; it only re-dresses it for print.
"""
import html as _html
import re

LET = "ABCDEFGH"

# the portal's stylesheet variables, resolved to the house palette
VARS = {
    "--line": "#c9d0dc",
    "--navy": "#14213a",
    "--blue": "#72afdb",
    "--light": "#f7f4ee",
    "--muted": "#566072",
    "--ink": "#1a2233",
}

SUBJECT = {"math": "Mathematics", "maths": "Mathematics",
           "reading": "Reading", "language-usage": "Language Usage"}


def resolve_vars(s):
    def rep(m):
        return VARS.get(m.group(1), "#c9d0dc")
    return re.sub(r"var\(\s*(--[a-z-]+)\s*\)", rep, s)


def inline_svg_paint(svg):
    """paper.css sets `svg { stroke:#14213A; stroke-width:2.4; fill:none }` for the
    house icon family. `fill` and `stroke` are inherited SVG properties, so that rule
    reaches every child of a portal diagram that does not set its own paint, and
    repaints it. Children carrying their own presentation attributes are safe (no CSS
    rule targets them), so restoring the SVG initial values on the root element alone
    is enough, and reproduces exactly what the diagram looks like online."""
    RESET = "fill:#000;stroke:none;stroke-width:1;"

    def fix(m):
        tag = m.group(0)
        if re.search(r'\bstyle="', tag):
            return re.sub(r'\bstyle="', 'style="%s' % RESET, tag, count=1)
        body = tag.rstrip()
        if body.endswith("/>"):
            return body[:-2].rstrip() + ' style="%s"/>' % RESET
        return body[:-1].rstrip() + ' style="%s">' % RESET

    return re.sub(r"<svg\b[^>]*>", fix, svg)


def crop_captures(s, options):
    """Some figures are captures of a whole source question: a line of question text,
    the diagram, then the platform's own option strip. In print the stem and the choices
    are already set as type underneath, so the picture repeats them. Crop to the
    artwork. Where the printed choices are bare labels ('Line A'), the little pictures
    ARE the answer set and are kept."""
    import base64
    try:
        from figcrop import crop_for_print
    except ImportError:
        return s

    def rep(m):
        try:
            raw = base64.b64decode(re.sub(r"\s", "", m.group(1)))
            cut = crop_for_print(raw, options)
        except Exception:
            return m.group(0)
        if not cut:
            return m.group(0)
        return "data:image/png;base64," + base64.b64encode(cut).decode()

    return re.sub(r"data:image/png;base64,([A-Za-z0-9+/=\s]+)", rep, s)


def clean_stimulus(s, options=None):
    """Strip the portal's on-screen chrome, keep the content."""
    if not s:
        return ""
    s = resolve_vars(s)
    if "data:image/png;base64," in s:
        s = crop_captures(s, options)
    # the portal wraps figures in styled divs for the web; drop the decoration
    s = re.sub(r'<div style="[^"]*"', '<div', s)
    s = re.sub(r'<img\s+([^>]*?)style="[^"]*"', r'<img \1', s)
    s = inline_svg_paint(s)
    # tables get the house hairline treatment
    s = re.sub(r"<table[^>]*>", '<table class="stab">', s)
    s = re.sub(r"<(td|th)[^>]*>", r"<\1>", s)
    return s.strip()


def looks_long(options):
    return any(len(re.sub(r"<[^>]+>", "", o)) > 24 for o in options)


def q_block(q, letters, show_key=None):
    """One question, as a block that must not be split across a page."""
    out = []
    opts_raw = q.get("options") or []
    stim = clean_stimulus(q.get("passage") or "", opts_raw)
    fig = clean_stimulus(q.get("fig") or "", opts_raw)
    img = clean_stimulus(q.get("img") or "", opts_raw)
    if stim:
        out.append('<div class="stim">%s</div>' % stim)
    if img:
        out.append('<div class="stim"><img src="%s" alt="figure"></div>' % img)
    if fig:
        out.append('<div class="stim">%s</div>' % fig)

    stem = (q.get("stem") or "")
    stem = _html.escape(stem)
    # the portal re-enables a fixed set of inline tags after escaping; match it
    stem = re.sub(r"&lt;(/?)(u|b|i|em|strong|sub|sup)&gt;", r"<\1\2>", stem)
    stem = stem.replace("\n", "<br>")

    opts = q.get("options") or []
    stack = looks_long(opts)
    rows = []
    for i, o in enumerate(opts):
        txt = _html.escape(o)
        txt = re.sub(r"&lt;(/?)(u|b|i|em|strong|sub|sup)&gt;", r"<\1\2>", txt)
        mark = ""
        if show_key is not None and i == show_key:
            mark = " key"
        rows.append('<div class="opt%s"><span class="L">%s</span>'
                    '<span class="w">%s</span></div>' % (mark, letters[i], txt))
    out.append('<div class="qtext">%s</div>' % stem)
    out.append('<div class="opts%s">%s</div>' % (" stack" if stack else "", "".join(rows)))

    return ('<div class="blk"><div class="q"><div class="qn">%d</div>'
            '<div class="qbody">%s</div></div></div>' % (q["n"], "".join(out)))


def paper_meta(rel, title, n_questions):
    """Cover text for this paper, derived from its path and portal title."""
    parts = rel.split("/")
    hkis = parts[0] == "HKIS"
    if hkis:
        grade = parts[1].replace("-", " ")
        subject = SUBJECT.get(parts[2].lower(), parts[2].title())
        # lead with "practice" so the paper never reads as the school's own material
        eyebrow = "MAP Practice Paper · HKIS Entry Assessment"
        name = "%s · %s" % (subject, grade)
        variant = "Practice Paper"
    else:
        grade = parts[0].replace("grade-", "Grade ")
        subject = SUBJECT.get(parts[1], parts[1].title())
        # MAP Growth is NWEA's assessment; this is practice material, not their paper
        eyebrow = "MAP Growth · Practice Paper"
        name = "%s · %s" % (subject, grade)
        if parts[2] == "full-length":
            variant = "Full Length Practice Test"
        else:
            lvl = parts[2].replace("level-", "Level ")
            drill = parts[3].replace("drill-", "Drill ")
            variant = "%s · %s" % (lvl, drill)
    # MAP is untimed and adaptive; give a realistic working estimate instead
    minutes = max(10, int(round(n_questions * 1.5 / 5.0) * 5))
    return eyebrow, name, variant, minutes


INSTRUCTIONS = [
    "Answer every question. There is one correct answer to each question.",
    "Circle the letter of the answer you choose.",
    "If you change your mind, cross out your first answer and circle the new one.",
    "You may write anywhere on this paper for working.",
    "If you finish early, go back and check your answers.",
]
