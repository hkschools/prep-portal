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
import argparse, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.expanduser("~/.claude/skills/testgen-idat")
sys.path.insert(0, os.path.join(SKILL, "engines", "render"))
sys.path.insert(0, os.path.join(SKILL, "engines", "lib"))
sys.path.insert(0, os.path.join(SKILL, "references"))
from render_paper import figure_to_svg  # noqa: E402
from hs_paper import mathify  # noqa: E402  (same token expander the PDF uses)
import bankbuild  # noqa: E402

TEMPLATE = os.path.join(HERE, "templates", "idat_page.html")
FAM = {"critical-thinking": "CT", "logic": "LOGIC", "maths": "MATH",
       "english": "ENG", "grammar-vocab": "GV", "reading": "READ", "writing": "WRITE",
       "chinese": "CHI"}


def norm(s):
    return re.sub(r"\W+", "", (s or "")).lower()[:60]


def version_token(d):
    """The `version` the page POSTs.

    The deployed IDAT engine builds its bank path as
        idat-tests/<school>/stage<stage>/v<version>/bank.csv
    so the token IS the bank location. A drill therefore has to live in that
    same namespace or the engine 404s and the submission is silently dropped.
    """
    return f"{FAM[d['family']]}-D{d['drill']}"


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



# The online page injects our own test content as HTML, so the maths authoring
# tokens must be expanded exactly as the PDF renderer expands them, or the
# student reads a literal "b^{6}". This runs AFTER parity(), which matches page
# slots against the source stems and would not recognise a rewritten one.
_MATH_TEXT_FIELDS = ("stem", "passage", "intro", "body", "hint", "partA", "partB", "title")


def mathify_slots(slots):
    out = []
    for o in slots:
        o = dict(o)
        for k in _MATH_TEXT_FIELDS:
            if isinstance(o.get(k), str):
                o[k] = mathify(o[k])
        if isinstance(o.get("options"), dict):
            o["options"] = {k: mathify(v) if isinstance(v, str) else v
                            for k, v in o["options"].items()}
        out.append(o)
    return out


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
    """A/B/C/D spread, checked WITHIN each option-count group.

    A drill mixes 2-, 3- and 4-option items (Assumption is Yes/No, Deduction and
    Evaluation carry three). Pooling them makes D look starved when it simply
    cannot occur on a 3-option item, so group first.
    """
    from collections import Counter
    groups = {}
    for q in d.get("questions", []):
        n = len([v for v in q["options"].values() if str(v).strip()])
        groups.setdefault(n, []).append(q)
    for n, items in groups.items():
        if n < 3 or len(items) < 6:
            continue
        c = Counter(str(q["answer"]).upper() for q in items)
        for letter in [chr(65 + i) for i in range(n)]:
            c.setdefault(letter, 0)
        if max(c.values()) - min(c.values()) > max(2, len(items) // 4):
            errs.append(f"answer spread uneven across {n}-option items: {dict(c)}")


WG_OPTS = {"assumption": 2, "inference": 4, "interpretation": 4, "deduction": 3, "evaluation": 3}


def wg_check(d, errs):
    """Critical-thinking drills must use the official shape of each type."""
    if d.get("family") != "critical-thinking":
        return
    sys.path.insert(0, os.path.join(SKILL, "engines", "lib"))
    import selfcheck as sc
    seen = {}
    for q in d.get("questions", []):
        t = sc.wg_classify(q.get("stem"))
        seen[t] = seen.get(t, 0) + 1
        want = WG_OPTS.get(t)
        n = len([v for v in q["options"].values() if str(v).strip()])
        if want and n != want:
            errs.append(f"#{q.get('id')}: {t} item has {n} options, official format is {want}")
        if t == "interpretation" and sc.wg_conclusions(q.get("stem")) < 3:
            errs.append(f"#{q.get('id')}: interpretation item needs 3 numbered conclusions")
        if t == "other":
            errs.append(f"#{q.get('id')}: matches no Watson-Glaser type")
    for t in WG_OPTS:
        if not seen.get(t):
            errs.append(f"drill omits Watson-Glaser type {t!r}")



def sibling_dedup(d, path, errs):
    """No stem may repeat across drills in the same family and stage.

    A student works through drill 1 to 5 in sequence, so a repeated scenario is
    wasted practice. Compares against every sibling drill JSON beside this one.
    """
    import glob
    def toks(x):
        """Tokens for the overlap test.

        Whitespace splitting alone makes this gate INERT for Chinese: 中文 has no
        spaces, so a whole stem collapses to one token, the `len(ta) < 8` guard
        below skips it, and two identical CIS Chinese stems compare as unrelated.
        Character bigrams over each CJK run give those stems real content to
        compare. Latin text is unaffected.
        """
        s = re.sub(r"<[^>]+>", " ", str(x or "")).lower()
        out = set(s.split())
        for run in re.findall(r"[\u4e00-\u9fff]+", s):
            out |= {run[i:i + 2] for i in range(len(run) - 1)}
        return out
    def flat(x):
        """Normalised surface text, for comparing stems too short to score."""
        return " ".join(re.sub(r"<[^>]+>", " ", str(x or "")).split()).lower()

    mine = [q.get("stem", "") for q in d.get("questions", [])]
    mine += [q.get("stem", "") for p_ in d.get("passages", []) for q in p_["questions"]]
    for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(path)), "*.json"))):
        if os.path.abspath(f) == os.path.abspath(path):
            continue
        try:
            other = json.load(open(f))
        except Exception:
            continue
        theirs = [q.get("stem", "") for q in other.get("questions", [])]
        theirs += [q.get("stem", "") for p_ in other.get("passages", []) for q in p_["questions"]]
        for a in mine:
            ta = toks(a)
            if len(ta) < 8:
                # Too few tokens for a Jaccard score to mean anything, but an
                # IDENTICAL short stem is still wasted practice. This branch used
                # to just `continue`, which is how four of the five live HKIS
                # Stage 6 English drills came to ship the same five-token
                # "Which sentence is written correctly?" as their item 4.
                fa = flat(a)
                if fa and any(flat(b) == fa for b in theirs):
                    errs.append(f"stem repeats {os.path.basename(f)}: {fa[:70]!r}")
                continue
            for b in theirs:
                tb = toks(b)
                if not tb:
                    continue
                j = len(ta & tb) / len(ta | tb)
                if j > 0.7:
                    errs.append(f"stem repeats {os.path.basename(f)}: {re.sub(r'<[^>]+>',' ',a)[:70]!r}")
                    break


def render(d, slots):
    title = f"IDAT {d['school'].upper()}: Stage {d['stage']} {d['section']} Drill {d['drill']}"
    t = open(TEMPLATE).read()
    return (t.replace("{{TITLE}}", title).replace("{{SCHOOL}}", d["school"].upper())
             .replace("{{STAGE}}", str(d["stage"])).replace("{{VERSION}}", version_token(d))
             .replace("{{QUESTIONS}}", json.dumps(slots, ensure_ascii=False)))



MLBASE = os.path.expanduser("~/Library/CloudStorage/GoogleDrive-alex@hk-schools.com/"
                           "Shared drives/HK-Schools.com/Materials Library/IDAT")


def mlroot(d):
    """Materials Library root for THIS drill's school.

    This was hardcoded to .../IDAT/HKIS, which would have filed every CIS drill's
    PDFs into the HKIS tree, where no one would look for them and where they would
    collide with the HKIS drill of the same stage and number.
    """
    return os.path.join(MLBASE, d["school"].upper())


def publish(d, drill_path):
    """Render the branded PDFs and file them in the Materials Library.

    A drill without a PDF is not teaching material, so this runs as part of the
    build rather than as a later retrofit.
    """
    render = os.path.join(SKILL, "engines", "render", "hs_drill.py")
    subprocess.run([sys.executable, render, drill_path], check=True,
                   stdout=subprocess.DEVNULL)
    base = f"IDAT {d['school'].upper()} Stage {d['stage']} - {d['section']} Drill {d['drill']}"
    src = os.path.dirname(os.path.abspath(drill_path))
    dst = os.path.join(mlroot(d), f"Stage {d['stage']}", "Drills",
                       f"{d['section']} Drill {d['drill']}", "Shareable (PDF)")
    os.makedirs(dst, exist_ok=True)
    placed = 0
    for kind in ("Questions", "Answer Key"):
        f = os.path.join(src, f"{base} - {kind}.pdf")
        if os.path.exists(f):
            shutil.copy2(f, os.path.join(dst, os.path.basename(f)))
            placed += 1
    print(f"  pdf  -> {src}/{base} - Questions.pdf")
    print(f"  drive-> {dst}  ({placed} file(s))")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("drill"); b.add_argument("--out")
    b.add_argument("--no-pdf", action="store_true", help="skip PDF + Materials Library")
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
    wg_check(d, errs)
    sibling_dedup(d, a.drill, errs)
    if errs:
        print(f"BUILD ABORTED for {test_id(d)} - nothing written:")
        for e in errs:
            print(f"  ERROR {e}")
        sys.exit(1)
    rel = os.path.join("idat-tests", d["school"].lower(), f"stage{d['stage']}",
                       "drills", d["family"], f"drill-{d['drill']}")
    bankrel = os.path.join("idat-tests", d["school"].lower(), f"stage{d['stage']}",
                           f"v{version_token(d)}")
    out = a.out or os.path.join(HERE, "..", rel)
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "index.html"), "w").write(render(d, mathify_slots(slots)))
    bankdir = os.path.join(a.bank_root, bankrel)
    os.makedirs(bankdir, exist_ok=True)
    bankbuild.write_bank(bankdir, test_id(d), bank)
    os.rename(os.path.join(bankdir, f"{test_id(d)}.bank.csv"), os.path.join(bankdir, "bank.csv"))
    mcqs = sum(1 for r in bank if r["type"] == "mcq")
    print(f"{test_id(d)}: {mcqs} mcq + {len(bank)-mcqs} writing, {got}/{exp} figures, parity OK")
    print(f"  page -> {os.path.normpath(out)}/index.html")
    print(f"  bank -> {bankdir}/bank.csv")
    if not a.no_pdf:
        publish(d, a.drill)


if __name__ == "__main__":
    main()
