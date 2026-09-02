#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a REVIEW SHEET for a Singapore online test: every question on one page.

    python3 preview_singapore.py <subject> <mock> [OUT.html]
    e.g.  python3 preview_singapore.py math 4

The live page shows one question at a time, which is right for a candidate and
useless for reviewing a 45-question paper. This stacks them all.

It reuses the PAGE'S OWN markup and stylesheet verbatim -- same `<div class="q">`
wrapper, same `.stem` / `.opts` / `.ansrow` / `.anshint` / `.qnote` structure -- and
adds nothing but page-level layout. That is not tidiness, it is correctness: the
house SVG line-art rule is scoped `.q svg { ... fill:none }`, so a preview that
invents its own wrapper classes loses it and every dial, clock and scale renders as
a SOLID BLACK DISC. That has now happened twice (see BUILD_NOTES.md); a preview
that re-declares the page's CSS will do it a third time.
"""
import html as _html
import json
import os
import re
import sys

PORTAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TITLES = {"math": "Mathematics", "english": "English",
          "chinese-sc": "中文（简体）", "chinese-tc": "中文（繁體）"}


def build(subject, mock, out=None):
    page = os.path.join(PORTAL, "singapore-tests", subject, "p4", f"mock-{mock}",
                        "index.html")
    src = open(page, encoding="utf-8").read()
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", src, re.S))
    qs = json.loads(re.search(r"const QUESTIONS\s*=\s*(\[.*?\]);", src, re.S).group(1))
    title = re.search(r"<title>(.*?)</title>", src, re.S)
    title = title.group(1) if title else f"{subject} mock {mock}"

    def render_part(p, j, mode):
        if mode == "inline":
            return ""
        opts = "".join(
            f'<label><input type="radio" name="g{j}_{p["label"]}">'
            f'<span><b>{_html.escape(str((p.get("labels") or "ABCDEFGH")[i]))}</b>'
            f'&nbsp;&nbsp;{o}</span></label>' for i, o in enumerate(p["options"]))
        return (f'<div class="subq"><div class="sqstem">{p["label"]}. {p["stem"]}</div>'
                f'<div class="opts">{opts}</div></div>')

    def inline_selects(stem, parts):
        """Swap each blank marker for a real dropdown, as the live page does in JS."""
        for p in parts:
            sel = ('<option value="" selected>(%s)</option>' % p["label"]) + "".join(
                f'<option>{_html.escape(re.sub("<[^>]+>", "", o))}</option>'
                for o in p["options"])
            stem = stem.replace(f'<span class="blank" data-q="{p["label"]}"></span>',
                                f'<span class="blank"><select>{sel}</select></span>')
        return stem

    cards = []
    for k, q in enumerate(qs):
        if q.get("parts"):
            stem = q["stem"]
            if q.get("mode") == "inline":
                stem = inline_selects(stem, q["parts"])
            body = "".join(render_part(p, k, q.get("mode")) for p in q["parts"])
            span = f'{q["parts"][0]["label"]}–{q["parts"][-1]["label"]}'
            cards.append(f'<div class="qwrap"><div class="qtag">'
                         f'{_html.escape(q["section"])} · questions {span} · '
                         f'text shown once</div>'
                         f'<div class="q"><div class="stem groupstem">{stem}</div>'
                         f'{body}</div></div>')
            continue
        # exactly what renderQuestion() emits, minus the live event handlers
        stem = f'<div class="stem">{q["label"]}. {q["stem"]}</div>'
        if q.get("options"):
            body = '<div class="opts">'
            for i, o in enumerate(q["options"]):
                mark = (q.get("labels") or "ABCDEFGH")[i]
                body += (f'<label><input type="radio" name="q{k}">'
                         f'<span><b>{_html.escape(str(mark))}</b>&nbsp;&nbsp;{o}</span>'
                         f'</label>')
            body += "</div>"
        elif q.get("multiline"):
            body = '<textarea rows="4" placeholder="Type your answer"></textarea>'
        else:
            body = ('<div class="ansrow">'
                    + (f'<span class="pfx">{_html.escape(q["prefix"])}</span>'
                       if q.get("prefix") else "")
                    + '<input type="text" placeholder="Type your answer">'
                    + (f'<span class="pfx">{_html.escape(q["unit"])}</span>'
                       if q.get("unit") else "")
                    + "</div>")
        if q.get("hint"):
            body += f'<div class="anshint">{_html.escape(q["hint"])}</div>'
        note = (f'<div class="qnote">{_html.escape(q["note"])}</div>'
                if q.get("note") else "")
        # the page's own stem already prints "11." -- the tag carries the section only
        cards.append(f'<div class="qwrap"><div class="qtag">'
                     f'{_html.escape(q["section"])}</div>'
                     f'<div class="q">{stem}{body}{note}</div></div>')

    # count the QUESTIONS, not the screens: a grouped screen carries many
    asked = [p for q in qs for p in (q["parts"] if q.get("parts") else [q])]
    mcq = sum(1 for p in asked if p.get("options"))
    typed = len(asked) - mcq
    screens = len(qs)
    # Layout only. Nothing here may touch svg, .q, .stem, .opts or their children.
    layout = """
    body{background:#eef1f6;margin:0;padding:22px 16px 60px}
    .sheet{max-width:880px;margin:0 auto}
    .hd{background:#14213a;color:#fff;border-radius:14px;padding:20px 26px}
    .hd h1{margin:0 0 5px;font-size:1.15rem}
    .hd p{margin:0;font-size:.86rem;opacity:.85;line-height:1.6}
    .chips{display:flex;gap:8px;flex-wrap:wrap;margin:13px 0 4px}
    .chip{background:#fff;border:1px solid #d3dae6;border-radius:999px;padding:5px 13px;
      font-size:.78rem;color:#3d4a5e}
    .chip b{color:#14213a}
    .qwrap{margin:16px 0}
    .qtag{display:flex;align-items:center;gap:9px;margin:0 0 7px 4px;font-size:.72rem;
      letter-spacing:.5px;text-transform:uppercase;color:#78859a}
    .qtag{font-weight:700}
    .qtag span{font-weight:600}
    """
    doc = (f"<!doctype html><html><head><meta charset='utf-8'>"
           f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
           f"<title>{title} — review sheet</title><style>{css}\n{layout}</style></head>"
           f"<body><div class='sheet'><div class='hd'>"
           f"<h1>{title}</h1>"
           f"<p>Every question exactly as the online form asks it, stacked so the whole "
           f"paper reads in one scroll. The live page shows these one at a time. "
           f"Answer fields are live; nothing is submitted.</p></div>"
           f"<div class='chips'><span class='chip'><b>{len(asked)}</b> questions</span>"
           f"<span class='chip'><b>{mcq}</b> multiple choice</span>"
           f"<span class='chip'><b>{typed}</b> typed answer</span>"
           f"<span class='chip'><b>{screens}</b> screens</span></div>"
           + "".join(cards) + "</div></body></html>")

    out = out or os.path.join(PORTAL, "_builder",
                              f"review-{subject}-p4-mock{mock}.html")
    open(out, "w", encoding="utf-8").write(doc)

    # The whole point of reusing the page's markup: prove the scoped rule reaches
    # the figures. Every <svg> must sit inside an element with class "q".
    stray = len(re.findall(r"<svg", doc)) - len(re.findall(
        r'<div class="q">(?:(?!</div></div>).)*?<svg', doc, re.S))
    figs = len(re.findall(r"<svg", doc))
    print(f"  {out}  ({len(asked)} questions on {screens} screens, {figs} figures)")
    if 'class="q"' not in doc or ".q svg" not in css:
        sys.exit("  FAIL: the .q wrapper or the .q svg line-art rule is missing — "
                 "figures would render as solid black")
    return out


if __name__ == "__main__":
    subject = sys.argv[1] if len(sys.argv) > 1 else "math"
    mock = sys.argv[2] if len(sys.argv) > 2 else "4"
    build(subject, mock, sys.argv[3] if len(sys.argv) > 3 else None)
