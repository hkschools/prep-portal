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

TEMPLATE = os.path.join(HERE, "templates", "idat_page.html")
SECT_GK = "Global Knowledge & Logic"
INFO = {
    "English": "Read each question and choose the best answer. This section covers grammar, vocabulary and reading comprehension.",
    "Character": "These questions help us understand how you like to learn. There are no right or wrong answers.",
    "Maths": "Read each question carefully and choose the best answer.",
    SECT_GK: "Read each question carefully and choose the best answer.",
}


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


def build_questions(paper, stage, errs):
    """Compose the page's QUESTIONS array. Order mirrors the paper:
    English (grammar/vocab then reading) -> Writing -> Character -> Maths -> GK/Logic.
    Listening & Speaking is platform-delivered and is intentionally not online."""
    eng, mth = load(paper, "english"), load(paper, "maths")
    lg, ct, ch = load(paper, "logic"), load(paper, "critical_thinking"), load(paper, "character")
    out, n = [], 1

    def add(o):
        nonlocal n
        out.append({"n": str(n), **o})   # "n" first, as on the existing pages
        n += 1

    def mcq(q, section, qnum, passage="", where=""):
        add({"type": "mcq", "section": section, "stem": q["stem"],
             "options": {k: v for k, v in q["options"].items() if str(v).strip()},
             "fig": fig_svg(q, where, errs), "passage": passage, "qnum": str(qnum)})

    # --- English
    add({"type": "info", "title": "English", "body": INFO["English"]})
    qn = 1
    for q in eng["grammar_vocab"]:
        mcq(q, "English", qn, where=f"english.gv#{q.get('id')}")
        qn += 1
    for p in eng.get("passages", []):
        html = f"<strong>{p.get('title','')}</strong><br>{p.get('text','')}"
        for q in p["questions"]:
            mcq(q, "English", qn, passage=html, where=f"english.passage#{q.get('id')}")
            qn += 1
    # --- Writing (Part 1 editing cloze + Part 2 paragraph)
    w = eng.get("writing") or {}
    prompt = w.get("prompt", "")
    parts = re.split(r"\n(?=Part\s*2\s*[:.)])", prompt, maxsplit=1)
    cap = json.load(open(os.path.join(SKILL, "spec", "manifest.json")))["hkis"][str(stage)]["english_rw"]["paragraph_sentence_cap"]
    intro = w.get("framing") or (
        "Writing section, two parts: Part 1 is a drop-down editing task; Part 2 is one short paragraph. "
        "On the real online test, Part 1 appears as drop-down menus inside the passage.")
    hint = w.get("instruction") or (
        "This section has TWO parts and your writing will be viewed by your future school. Part 1: read the passage "
        "and, for each numbered bracket, choose the option (A, B or C) that makes the writing correct and clear. "
        f"Part 2: choose ONE of the two tasks and write a single paragraph of no more than {cap} sentences. "
        "Check your spelling, punctuation and grammar before you finish.")
    add({"type": "writing", "section": "English Writing",
         "intro": intro, "label": "", "body": "", "hint": hint,
         "placeholder": "Type your answer here (it will be saved for review)…",
         "partA": parts[0].strip(),
         "partB": (parts[1].strip() if len(parts) == 2 else "")})
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


def parity(questions, paper, errs):
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
            k = norm(q["stem"])
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
        exp, got = parity(qs, a.paper, errs)
        print(f"{a.page}: {got} figure(s) on page, {exp} in source")
        for e in errs:
            print(f"  ERROR {e}")
        print("RESULT:", "PASS" if not errs else "FAIL")
        sys.exit(0 if not errs else 1)

    paper = os.path.abspath(a.paper.rstrip("/"))
    school, stage, version = ident(paper, a.school, a.stage, a.version)
    errs = []
    qs = build_questions(paper, stage, errs)
    exp, got = parity(qs, paper, errs)
    if errs:
        print(f"BUILD ABORTED for {os.path.basename(paper)} - page not written:")
        for e in errs:
            print(f"  ERROR {e}")
        sys.exit(1)
    out = a.out or os.path.join(HERE, "..", "idat-tests", school.lower(), f"stage{stage}", f"v{version}")
    os.makedirs(out, exist_ok=True)
    dest = os.path.join(out, "index.html")
    open(dest, "w").write(render(paper, school, stage, version, qs))
    print(f"{dest}\n  {len(qs)} blocks, {got}/{exp} figures, parity OK")


if __name__ == "__main__":
    main()
