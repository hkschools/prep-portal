#!/usr/bin/env python3
"""build_iseb.py — ISEB Common Pre-Test online pages for prep.hk-schools.com.

Four separate pages, one per section, because the four ISEB tests are sittable
separately and most candidates sit them in separate settings.

    python3 build_iseb.py --paper <paper_dir> --version 1 [--script-url URL]

Reads the SAME paper JSON the PDFs are built from (testgen-iseb), so the online
test and the printed paper can never drift apart. Banks are exported separately
by testgen-iseb/engines/export_bank.py and must be pushed to test-banks BEFORE
these pages go live: the grader reads the private repo through the authenticated
GitHub API.

Option order is NOT baked into the page: the template shuffles at run time and
submits each option's ORIGINAL letter. See the shuffle note in iseb_page.html.
"""
import argparse, base64, html, json, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PORTAL = HERE.parent
SKILL = Path.home() / ".claude" / "skills" / "testgen-iseb" / "engines"
sys.path.insert(0, str(SKILL))
import curriculum as cur

TEMPLATE = (HERE / "templates" / "iseb_page.html").read_text(encoding="utf-8")
SEC_SLUG = {"EN": "english", "MA": "maths", "VR": "verbal", "NVR": "nonverbal"}
SEC_NAME = {"EN": "English", "MA": "Mathematics",
            "VR": "Verbal Reasoning", "NVR": "Non-Verbal Reasoning"}
E = lambda s: html.escape(str(s), quote=False)


def nodash(s):
    return (str(s).replace(" — ", " · ").replace(" – ", " · ")
            .replace("—", "·").replace("–", "-"))


def svg_uri(svg):
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode("ascii")


def families():
    f = {}
    for pools, names in ((cur.VR_POOLS, cur.VR_FAMILIES), (cur.NVR_POOLS, cur.NVR_FAMILIES)):
        for pi, pool in enumerate(pools):
            for t in pool:
                f[t] = names[pi]
    return f


def group_of(sec, it, spec, fams):
    if sec == "EN":
        parts = {b: n for n, bl in spec.get("parts", []) for b in bl}
        return parts.get(it.get("block"), "")
    if sec == "MA":
        return "Mathematics"
    lbl = {"VR": cur.VR_TYPES, "NVR": cur.NVR_TYPES}[sec].get(
        it.get("format"), it.get("format")).split(" (")[0]
    fam = fams.get(it.get("format"))
    return f"Group {it.get('block')} · {fam} · {lbl}" if fam else f"Group {it.get('block')} · {lbl}"


def build_passages(d):
    out = []
    for p in d.get("passages", []):
        poetry = p.get("genre") == "poetry"
        blocks = [b.strip() for b in p["text"].split("\n\n") if b.strip()]
        entry = {"id": p["id"], "title": f'Passage {p["id"]} · {p.get("title","")}',
                 "poetry": poetry}
        if poetry:
            entry["verses"] = [v.split("\n") for v in blocks]
        else:
            entry["paras"] = blocks
        out.append(entry)
    return out


def build_section(sec, d, version, script_url):
    spec = cur.SECTIONS[sec]
    fams = families()
    qs, first_of_group = [], {}
    for it in d["items"]:
        g = group_of(sec, it, spec, fams)
        first_of_group.setdefault(g, it["n"])
        opts = it["options"]
        fig_answers = set(map(str, opts.values())) == {"figure"}
        q = {"n": it["n"], "group": g, "stem": nodash(it["stem"]),
             "figureAnswers": fig_answers,
             "options": [] if fig_answers else
                        [{"L": L, "t": nodash(v)} for L, v in opts.items()]}
        if it.get("figure_svg"):
            q["figure"] = svg_uri(it["figure_svg"])
        if it.get("passage_id"):
            q["passage_id"] = it["passage_id"]
        qs.append(q)

    exs = []
    for x in d.get("examples", []):
        g = group_of(sec, {"block": x["block"], "format": x["format"]}, spec, fams)
        if g not in first_of_group:
            continue
        fa = set(map(str, x["options"].values())) == {"figure"}
        exs.append({"group": g, "first": first_of_group[g],
                    "stem": nodash(x["stem"]),
                    "figure": svg_uri(x["figure_svg"]) if x.get("figure_svg") else "",
                    "answer": x["correct"] if fa else
                              f'{x["correct"]} · {nodash(x["options"][x["correct"]])}',
                    "why": nodash(x["walkthrough"])})

    test_id = f"ISEB-CPT-V{version}-{sec}"
    title = f'ISEB Common Pre-Test v{version} · {SEC_NAME[sec]}'
    countline = (f'{len(qs)} questions · {spec["minutes"]} minutes · '
                 f'one question per screen · you cannot go back')
    page = (TEMPLATE
            .replace("__TITLE__", E(title))
            .replace("__COUNTLINE__", E(countline))
            .replace("__TESTID__", test_id)
            .replace("__MINUTES__", str(spec["minutes"]))
            .replace("__SCRIPT_URL__", script_url)
            .replace("/*__PASSAGES_JSON__*/[]", json.dumps(build_passages(d), ensure_ascii=False))
            .replace("/*__QUESTIONS_JSON__*/[]", json.dumps(qs, ensure_ascii=False))
            .replace("/*__EXAMPLES_JSON__*/[]", json.dumps(exs, ensure_ascii=False)))

    # ---- self-checks: a leaked key or a stale placeholder must never ship ----
    assert "__TESTID__" not in page and "__MINUTES__" not in page
    # Precise key checks, NOT substring searches: EN Q5's options legitimately
    # contain the word "explanation" ("An explanation of how a design fault
    # was found"), and a naive `"explanation" not in json` fired on it.
    leaked = sorted({k for q in qs for k in q} & {"correct", "explanation", "answer"})
    assert not leaked, f"answer data leaked into the page: {leaked}"
    assert '"correct":' not in json.dumps(qs), "answer key leaked into the page"
    return test_id, title, page, len(qs), len(exs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper", required=True)
    ap.add_argument("--version", type=int, default=1)
    ap.add_argument("--script-url", default="__SCRIPT_URL__")
    a = ap.parse_args()
    pdir = Path(a.paper)

    for sec in cur.ORDER:
        fp = pdir / "json" / f"ISEB_{sec}.json"
        if not fp.exists():
            continue
        d = json.load(open(fp))
        test_id, title, page, nq, nex = build_section(sec, d, a.version, a.script_url)
        outdir = PORTAL / "iseb-tests" / f"v{a.version}" / SEC_SLUG[sec]
        outdir.mkdir(parents=True, exist_ok=True)
        (outdir / "index.html").write_text(page, encoding="utf-8")
        size = len(page.encode()) / 1024
        print(f"  {test_id:<18} {nq:>3} questions, {nex} example(s), "
              f"{size:6.0f} KB -> {outdir.relative_to(PORTAL)}/index.html")


if __name__ == "__main__":
    main()
