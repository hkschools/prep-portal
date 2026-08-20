#!/usr/bin/env python3
"""build_idat.py - generate (and verify) IDAT online test pages from a paper folder.

The v4/v5 pages were originally assembled by hand and silently lost every figure
that belonged to a Global Knowledge / Logic question, which left three items
unanswerable online. This builder derives the page from the paper's
`<subject>-final.json` files and REFUSES to write a page whose figures do not
match the source, so that class of bug cannot ship again.

    python3 build_idat.py build <paper-dir> [--out <dir>]   # write index.html
    python3 build_idat.py check <page.html> <paper-dir>      # audit only (exit 1 on drift)

<paper-dir> is a generated paper folder, e.g.
    ~/Desktop/Claude/Test-Prep/IDAT/2026-08-18-hkis-s3-v4
School / stage / version are read from its name unless given explicitly.

CIS and HKIS sit different papers and this builder now knows the difference.
Until 2026-08-21 it composed every paper as an HKIS one, which against a CIS
paper meant three defects at once: it never loaded `chinese`, so all 14 Chinese
items were dropped without an error; it emitted the HKIS section label
"Global Knowledge & Logic" where CIS's own FORMAT table names one combined
"Maths, Logic & Critical Thinking" section; and it read HKIS's writing cap out of
the manifest whatever the school. It had already overwritten two live CIS pages,
stripping Chinese from both. See spec/_analysis/cis-verification-2026-08.md.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.expanduser("~/.claude/skills/testgen-idat")
sys.path.insert(0, os.path.join(SKILL, "engines", "render"))
sys.path.insert(0, os.path.join(SKILL, "engines", "lib"))
from render_paper import figure_to_svg  # noqa: E402
from hs_paper import mathify, nodash  # noqa: E402  (the PDF's own expander)

TEMPLATE = os.path.join(HERE, "templates", "idat_page.html")
SECT_GK = "Global Knowledge & Logic"
SECT_MLC = "Maths, Logic & Critical Thinking"   # CIS's own name for its combined section
SECT_CHI = "\u4e2d\u6587 Chinese"
INFO = {
    "English": "Read each question and choose the best answer. This section covers grammar, vocabulary and reading comprehension.",
    "Character": "These questions help us understand how you like to learn. There are no right or wrong answers.",
    "Maths": "Read each question carefully and choose the best answer.",
    SECT_GK: "Read each question carefully and choose the best answer.",
    SECT_MLC: "One combined section. Read each question carefully and choose the best answer.",
    SECT_CHI: "\u9605\u8bfb\u4e0b\u9762\u7684\u77ed\u6587\uff0c\u7136\u540e\u56de\u7b54\u95ee\u9898\u3002Read the passage, then answer. (\u7e41\u9ad4 then \u7b80\u4f53.)",
}


def bilingual(trad, simp):
    """Traditional over Simplified, in markup that survives BOTH surfaces.

    The live CIS pages use <span style="color:#555">, which renders online and
    prints as literal markup in the PDF, because hs_paper.esc() restores only
    u b i p sup sub br and no attributes. <i> is on that list.
    """
    trad, simp = str(trad or ""), str(simp or "")
    return f"{trad}<br><i>{simp}</i>" if simp and simp != trad else trad


# Display fields in the QUESTIONS array. "fig" is already built SVG and "n" /
# "section" / "qnum" / "cnum" / "type" are structural, so neither is presented.
PRESENT_KEYS = ("stem", "passage", "title", "body", "intro", "hint",
                "label", "placeholder", "partA", "partB")


def present_text(s):
    """What the student should actually see.

    Two surfaces, one transform. The PDF gets this via hs_paper.txt(); the page
    had no equivalent, so it printed authoring tokens literally (a student saw
    `b^{6}`) and kept the em dashes the house style forbids. Fixing it in only
    one place is the mistake that shipped last time.
    """
    return nodash(mathify(s)) if isinstance(s, str) else s


def present(questions):
    """Apply it to every display field, AFTER parity has run on the raw slots."""
    for q in questions:
        for k in PRESENT_KEYS:
            if k in q:
                q[k] = present_text(q[k])
        if isinstance(q.get("options"), dict):
            q["options"] = {k: present_text(v) for k, v in q["options"].items()}
    return questions


def norm(s):
    return re.sub(r"\W+", "", (s or "")).lower()[:60]


def load(paper, name):
    p = os.path.join(paper, f"{name}-final.json")
    return json.load(open(p)) if os.path.exists(p) else None


def ident(paper, school=None, stage=None, version=None):
    b = os.path.basename(paper.rstrip("/")).lower()
    school = school or ("cis" if "cis" in b else "hkis")
    stage = stage or (re.search(r"s(?:tage)?-?([3-6])", b).group(1))
    version = version or (re.search(r"-v(\d+)$", b).group(1))
    return school.upper(), str(stage), str(version)


def fig_svg(q, where, errs):
    """Inline SVG for a question's figure ('' when it has none). A figure that
    cannot be built is an ERROR, never a silent omission."""
    f = q.get("figure") or {}
    if f.get("type", "none") == "none":
        return ""
    svg = figure_to_svg(f)
    if not svg:
        errs.append(f"{where}: figure {f.get('type')!r} failed to build")
        return ""
    return svg


def build_questions(paper, school, stage, errs):
    """Compose the page's QUESTIONS array, in the order that school's paper runs.

    HKIS: English -> Writing -> Character -> Maths -> Global Knowledge & Logic.
    CIS:  English -> Writing -> Maths, Logic & Critical Thinking (one combined
          section, as CIS's own FORMAT table names it) -> Chinese.
    CIS has no Character section and HKIS has no Chinese one.
    Listening & Speaking is platform-delivered and is intentionally not online.
    """
    cis = school.lower() == "cis"
    eng, mth = load(paper, "english"), load(paper, "maths")
    lg, ct = load(paper, "logic"), load(paper, "critical_thinking")
    ch, chi = load(paper, "character"), load(paper, "chinese")
    out, n = [], 1

    def add(o):
        nonlocal n
        out.append({"n": str(n), **o})   # "n" first, as on the existing pages
        n += 1

    def mcq(q, section, qnum, passage="", where="", stem=None, options=None):
        add({"type": "mcq", "section": section, "stem": q["stem"] if stem is None else stem,
             "options": {k: v for k, v in (q["options"] if options is None else options).items()
                         if str(v).strip()},
             "fig": fig_svg(q, where, errs), "passage": passage, "qnum": str(qnum)})

    # --- English
    add({"type": "info", "title": "English", "body": INFO["English"]})
    qn = 1
    for q in eng["grammar_vocab"]:
        mcq(q, "English", qn, where=f"english.gv#{q.get('id')}")
        qn += 1
    # A CIS Stage 4/5 reading task is a PAIR of texts to compare, so a question
    # on either text has to be shown BOTH. Set "paired": true on the english
    # file; otherwise each question carries only its own passage, as before.
    paired = bool(eng.get("paired"))
    def phtml(p):
        return f"<strong>{p.get('title','')}</strong><br>{p.get('text','')}"
    both = "<br><br>".join(phtml(p) for p in eng.get("passages", []))
    for p in eng.get("passages", []):
        html = both if paired else phtml(p)
        for q in p["questions"]:
            mcq(q, "English", qn, passage=html, where=f"english.passage#{q.get('id')}")
            qn += 1
    # --- Writing
    w = eng.get("writing") or {}
    prompt = w.get("prompt", "")
    intro = w.get("framing") or ""
    hint = w.get("instruction") or ""
    if cis:
        # CIS writing is ONE keyboard task, choose 1 of 2 topics: no cloze part.
        if not intro:
            intro = ("Writing section. Choose ONE of the two tasks and type your answer. "
                     "Your writing will be viewed by your future school.")
        if not hint:
            hint = ("Plan briefly, then write in clear paragraphs. Check your spelling, "
                    "punctuation and grammar before you finish.")
        add({"type": "writing", "section": "English Writing",
             "intro": intro, "label": "", "body": prompt, "hint": hint,
             "placeholder": "Type your answer here (it will be saved for review)\u2026",
             "partA": "", "partB": ""})
    else:
        # HKIS writing is two parts: Part 1 editing cloze + Part 2 paragraph.
        parts = re.split(r"\n(?=Part\s*2\s*[:.)])", prompt, maxsplit=1)
        cap = json.load(open(os.path.join(SKILL, "spec", "manifest.json"))) \
            ["hkis"][str(stage)]["english_rw"]["paragraph_sentence_cap"]
        intro = intro or (
            "Writing section, two parts: Part 1 is a drop-down editing task; Part 2 is one short paragraph. "
            "On the real online test, Part 1 appears as drop-down menus inside the passage.")
        hint = hint or (
            "This section has TWO parts and your writing will be viewed by your future school. Part 1: read the passage "
            "and, for each numbered bracket, choose the option (A, B or C) that makes the writing correct and clear. "
            f"Part 2: choose ONE of the two tasks and write a single paragraph of no more than {cap} sentences. "
            "Check your spelling, punctuation and grammar before you finish.")
        add({"type": "writing", "section": "English Writing",
             "intro": intro, "label": "", "body": "", "hint": hint,
             "placeholder": "Type your answer here (it will be saved for review)\u2026",
             "partA": parts[0].strip(),
             "partB": (parts[1].strip() if len(parts) == 2 else "")})

    if cis:
        # --- Maths + Logic + Critical Thinking, ONE combined section
        add({"type": "info", "title": SECT_MLC, "body": INFO[SECT_MLC]})
        i = 1
        for subj, data in (("maths", mth), ("logic", lg), ("critical_thinking", ct)):
            for q in (data or {}).get("questions", []):
                mcq(q, SECT_MLC, i, where=f"{subj}#{q.get('id')}")
                i += 1
        # --- Chinese (bilingual; Traditional over Simplified)
        if chi:
            add({"type": "info", "title": SECT_CHI, "body": INFO[SECT_CHI]})
            ptext = bilingual(chi.get("passage_trad", ""), chi.get("passage_simp", ""))
            for i, q in enumerate(chi.get("items", []), 1):
                ot, osi = q.get("options_trad", {}), q.get("options_simp", {})
                mcq(q, "Chinese", i, passage=(ptext if i == 1 else ""),
                    where=f"chinese#{q.get('id')}",
                    stem=bilingual(q.get("stem_trad", ""), q.get("stem_simp", "")),
                    options={k: bilingual(ot.get(k, ""), osi.get(k, "")) for k in ot})
        return out

    # --- Character (self-evaluation: no keys)
    if ch:
        add({"type": "info", "title": "Character", "body": INFO["Character"]})
        for i, q in enumerate(ch["questions"], 1):
            add({"type": "selfeval", "section": "Character", "stem": q["stem"],
                 "options": q["options"], "cnum": str(i)})
    # --- Maths
    add({"type": "info", "title": "Maths", "body": INFO["Maths"]})
    for i, q in enumerate(mth["questions"], 1):
        mcq(q, "Maths", i, where=f"maths#{q.get('id')}")
    # --- Global Knowledge / Logic (logic + critical thinking merged, as on the paper)
    add({"type": "info", "title": SECT_GK, "body": INFO[SECT_GK]})
    i = 1
    for subj, data in (("logic", lg), ("critical_thinking", ct)):
        for q in (data or {}).get("questions", []):
            mcq(q, SECT_GK, i, where=f"{subj}#{q.get('id')}")
            i += 1
    return out


def parity(questions, paper, errs, presented=False):
    """Every figure in the source paper must appear on the page. This is the
    check whose absence let the Logic figures go missing."""
    have = {norm(q["stem"]): bool(q.get("fig")) for q in questions if q.get("stem")}
    expected = 0
    for subj in ("maths", "logic", "critical_thinking"):
        d = load(paper, subj)
        for q in (d or {}).get("questions", []):
            if (q.get("figure") or {}).get("type", "none") == "none":
                continue
            expected += 1
            k = norm(present_text(q["stem"]) if presented else q["stem"])
            if k not in have:
                errs.append(f"{subj}#{q['id']}: question missing from page")
            elif not have[k]:
                errs.append(f"{subj}#{q['id']}: FIGURE MISSING on page ({q['stem'][:45]!r})")
    return expected, sum(1 for v in have.values() if v)


def render(paper, school, stage, version, questions):
    title = f"IDAT {school}: Stage {stage} (V{version})"
    t = open(TEMPLATE).read()
    return (t.replace("{{TITLE}}", title).replace("{{SCHOOL}}", school)
             .replace("{{STAGE}}", stage).replace("{{VERSION}}", version)
             .replace("{{QUESTIONS}}", json.dumps(questions, ensure_ascii=False)))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("paper"); b.add_argument("--out")
    b.add_argument("--school"); b.add_argument("--stage"); b.add_argument("--version")
    c = sub.add_parser("check"); c.add_argument("page"); c.add_argument("paper")
    a = ap.parse_args()

    if a.cmd == "check":
        html = open(a.page).read()
        qs = json.loads(re.search(r"QUESTIONS\s*=\s*(\[.*?\]);", html, re.S).group(1))
        errs = []
        exp, got = parity(qs, a.paper, errs, presented=True)
        print(f"{a.page}: {got} figure(s) on page, {exp} in source")
        for e in errs:
            print(f"  ERROR {e}")
        print("RESULT:", "PASS" if not errs else "FAIL")
        sys.exit(0 if not errs else 1)

    paper = os.path.abspath(a.paper.rstrip("/"))
    school, stage, version = ident(paper, a.school, a.stage, a.version)
    errs = []
    qs = build_questions(paper, school, stage, errs)
    exp, got = parity(qs, paper, errs)
    if errs:
        print(f"BUILD ABORTED for {os.path.basename(paper)} - page not written:")
        for e in errs:
            print(f"  ERROR {e}")
        sys.exit(1)
    qs = present(qs)
    out = a.out or os.path.join(HERE, "..", "idat-tests", school.lower(), f"stage{stage}", f"v{version}")
    os.makedirs(out, exist_ok=True)
    dest = os.path.join(out, "index.html")
    open(dest, "w").write(render(paper, school, stage, version, qs))
    print(f"{dest}\n  {len(qs)} blocks, {got}/{exp} figures, parity OK")


if __name__ == "__main__":
    main()
