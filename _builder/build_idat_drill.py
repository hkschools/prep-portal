#!/usr/bin/env python3
"""build_idat_drill.py - generate IDAT DRILL pages + answer banks from a drill JSON.

A drill isolates ONE skill (the mock merges Logic and Critical Thinking; drills
split them). Same page template, same figure-parity discipline as build_idat.py:
a figure that cannot be built aborts the build rather than shipping an
unanswerable item.

    python3 build_idat_drill.py build <drill.json> [--out <dir>] [--bank-root <dir>]
    python3 build_idat_drill.py check <page.html> <drill.json>

Drill JSON shape (see testgen-idat/spec/drills.md):
    {"school":"HKIS","stage":"3","family":"critical-thinking","drill":1,
     "section":"Critical Thinking","intro":"...",
     "questions":[{"id":1,"stem":..,"options":{"A":..},"answer":"A",
                   "explanation":..,"strand":..,"concept":..,"figure":{...}}],
     "passages":[{"title":..,"text":..,"questions":[...]}],      # reading
     "writing":[{"intro":..,"partA":..,"partB":..,"hint":..}]}   # writing
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.expanduser("~/.claude/skills/testgen-idat")
sys.path.insert(0, os.path.join(SKILL, "engines", "render"))
sys.path.insert(0, os.path.join(SKILL, "engines", "lib"))
sys.path.insert(0, os.path.join(SKILL, "references"))
from render_paper import figure_to_svg  # noqa: E402
import bankbuild  # noqa: E402

TEMPLATE = os.path.join(HERE, "templates", "idat_page.html")
FAM = {"critical-thinking": "CT", "logic": "LOGIC", "maths": "MATH",
       "grammar-vocab": "GV", "reading": "READ", "writing": "WRITE"}


def norm(s):
    return re.sub(r"\W+", "", (s or "")).lower()[:60]


def test_id(d):
    return f"{d['school'].upper()}-S{d['stage']}-{FAM[d['family']]}-D{d['drill']}"


def fig_svg(q, where, errs):
    f = q.get("figure") or {}
    if f.get("type", "none") == "none":
        return ""
    svg = figure_to_svg(f)
    if not svg:
        errs.append(f"{where}: figure {f.get('type')!r} failed to build")
        return ""
    return svg


def build(d, errs):
    """Page slots + bank rows, from one ordered item list so they cannot drift."""
    tid, section = test_id(d), d["section"]
    slots, bank, n = [], [], [0]

    def add(o):
        n[0] += 1
        slots.append({"n": str(n[0]), **o})

    def mcq(q, qnum, passage="", where=""):
        opts = {k: v for k, v in q["options"].items() if str(v).strip()}
        add({"type": "mcq", "section": section, "stem": q["stem"], "options": opts,
             "fig": fig_svg(q, where, errs), "passage": passage, "qnum": str(qnum)})
        ans = str(q.get("answer", "")).strip().upper()
        if ans not in opts:
            errs.append(f"{where}: answer {ans!r} is not one of the options {sorted(opts)}")
        if not str(q.get("explanation", "")).strip():
            errs.append(f"{where}: no explanation")
        bank.append({"test_id": tid, "q": n[0], "type": "mcq", "category": section,
                     "strand": q.get("strand", ""), "concept_tested": q.get("concept", ""),
                     "correct": ans, "marks": 1,
                     "explanation": re.sub(r"\s+", " ", str(q.get("explanation", ""))).strip()})

    add({"type": "info", "title": section, "body": d.get("intro", "")})
    qn = 1
    for q in d.get("questions", []):
        mcq(q, qn, where=f"{d['family']}#{q.get('id', qn)}")
        qn += 1
    for p in d.get("passages", []):
        html = f"<strong>{p.get('title','')}</strong><br>{p.get('text','')}"
        for i, q in enumerate(p["questions"]):
            mcq(q, qn, passage=(html if i == 0 else html),
                where=f"passage:{norm(p.get('title'))}#{q.get('id', qn)}")
            qn += 1
    for w in d.get("writing", []):
        add({"type": "writing", "section": section, "intro": w.get("intro", ""),
             "label": "", "body": w.get("body", ""), "hint": w.get("hint", ""),
             "placeholder": "Type your answer here (it will be saved for review)…",
             "partA": w.get("partA", ""), "partB": w.get("partB", "")})
        bank.append({"test_id": tid, "q": n[0], "type": "writing", "category": "Writing",
                     "strand": "", "concept_tested": "", "correct": "", "marks": "",
                     "explanation": ""})
    return slots, bank


def parity(slots, d, errs):
    """Every figure in the source must reach the page."""
    have = {norm(q["stem"]): bool(q.get("fig")) for q in slots if q.get("stem")}
    exp = 0
    src = list(d.get("questions", [])) + [q for p in d.get("passages", []) for q in p["questions"]]
    for q in src:
        if (q.get("figure") or {}).get("type", "none") == "none":
            continue
        exp += 1
        k = norm(q["stem"])
        if k not in have:
            errs.append(f"#{q.get('id')}: question missing from page")
        elif not have[k]:
            errs.append(f"#{q.get('id')}: FIGURE MISSING on page ({q['stem'][:45]!r})")
    return exp, sum(1 for v in have.values() if v)


def balance(d, errs):
    """A/B/C/D spread across the 4-option items; 2-option items counted apart."""
    from collections import Counter
    four = [q for q in d.get("questions", []) if len(
        [v for v in q["options"].values() if str(v).strip()]) > 2]
    if len(four) >= 8:
        c = Counter(str(q["answer"]).upper() for q in four)
        lo, hi = min(c.values(), default=0), max(c.values(), default=0)
        if hi - lo > max(2, len(four) // 6):
            errs.append(f"answer spread uneven across 4-option items: {dict(c)}")


def render(d, slots):
    title = f"IDAT {d['school'].upper()}: Stage {d['stage']} {d['section']} Drill {d['drill']}"
    t = open(TEMPLATE).read()
    return (t.replace("{{TITLE}}", title).replace("{{SCHOOL}}", d["school"].upper())
             .replace("{{STAGE}}", str(d["stage"])).replace("{{VERSION}}", f"{FAM[d['family']]}D{d['drill']}")
             .replace("{{QUESTIONS}}", json.dumps(slots, ensure_ascii=False)))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("drill"); b.add_argument("--out")
    b.add_argument("--bank-root", default=os.path.expanduser("~/Developer/work/test-banks"))
    c = sub.add_parser("check"); c.add_argument("page"); c.add_argument("drill")
    a = ap.parse_args()
    d = json.load(open(a.drill))

    if a.cmd == "check":
        html = open(a.page).read()
        qs = json.loads(re.search(r"QUESTIONS\s*=\s*(\[.*?\]);", html, re.S).group(1))
        errs = []
        exp, got = parity(qs, d, errs)
        print(f"{a.page}: {got} figure(s) on page, {exp} in source")
        for e in errs:
            print(f"  ERROR {e}")
        print("RESULT:", "PASS" if not errs else "FAIL")
        sys.exit(0 if not errs else 1)

    errs = []
    slots, bank = build(d, errs)
    exp, got = parity(slots, d, errs)
    balance(d, errs)
    if errs:
        print(f"BUILD ABORTED for {test_id(d)} - nothing written:")
        for e in errs:
            print(f"  ERROR {e}")
        sys.exit(1)
    rel = os.path.join("idat-tests", d["school"].lower(), f"stage{d['stage']}",
                       "drills", d["family"], f"drill-{d['drill']}")
    out = a.out or os.path.join(HERE, "..", rel)
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "index.html"), "w").write(render(d, slots))
    bankdir = os.path.join(a.bank_root, rel)
    os.makedirs(bankdir, exist_ok=True)
    bankbuild.write_bank(bankdir, test_id(d), bank)
    os.rename(os.path.join(bankdir, f"{test_id(d)}.bank.csv"), os.path.join(bankdir, "bank.csv"))
    mcqs = sum(1 for r in bank if r["type"] == "mcq")
    print(f"{test_id(d)}: {mcqs} mcq + {len(bank)-mcqs} writing, {got}/{exp} figures, parity OK")
    print(f"  page -> {os.path.normpath(out)}/index.html")
    print(f"  bank -> {bankdir}/bank.csv")


if __name__ == "__main__":
    main()
