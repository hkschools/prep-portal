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

Options are presented in their original order and keep their own letters, so the
letter shown is the letter submitted. (Alex's call, 2026-08-27: no shuffling.)
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


def section_payload(sec, d, fams):
    """The per-section data the page engine consumes."""
    spec = cur.SECTIONS[sec]
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

    return {"code": sec, "name": SEC_NAME[sec], "minutes": spec["minutes"],
            "passages": build_passages(d), "questions": qs, "examples": exs}


def emit(sections, test_id, title, countline, outdir, script_url):
    page = (TEMPLATE
            .replace("__TITLE__", E(title))
            .replace("__COUNTLINE__", E(countline))
            .replace("__TESTID__", test_id)
            .replace("__SCRIPT_URL__", script_url)
            .replace("/*__SECTIONS_JSON__*/[]", json.dumps(sections, ensure_ascii=False)))

    # ---- self-checks: a leaked key or a stale placeholder must never ship ----
    assert "__TESTID__" not in page and "__TITLE__" not in page
    allq = [q for s in sections for q in s["questions"]]
    leaked = sorted({k for q in allq for k in q} & {"correct", "explanation", "answer"})
    assert not leaked, f"answer data leaked into the page: {leaked}"
    assert '"correct":' not in json.dumps(allq), "answer key leaked into the page"

    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "index.html").write_text(page, encoding="utf-8")
    nq = len(allq); nex = sum(len(s["examples"]) for s in sections)
    print(f"  {test_id:<19} {nq:>3} questions, {nex} example(s), "
          f"{len(page.encode())/1024:6.0f} KB -> {outdir.name or 'v1'}/index.html")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper", required=True)
    ap.add_argument("--version", type=int, default=1)
    ap.add_argument("--script-url", default="__SCRIPT_URL__")
    a = ap.parse_args()
    pdir = Path(a.paper); fams = families(); v = a.version
    root = PORTAL / "iseb-tests" / f"v{v}"

    payloads = {}
    for sec in cur.ORDER:
        fp = pdir / "json" / f"ISEB_{sec}.json"
        if fp.exists():
            payloads[sec] = section_payload(sec, json.load(open(fp)), fams)

    # 1. THE PAPER: all four tests in one sitting, ONE report at the end.
    #    A child sits one paper, so the tutor gets one result card.
    ordered = [payloads[s] for s in cur.ORDER if s in payloads]
    total_q = sum(len(s["questions"]) for s in ordered)
    total_m = sum(s["minutes"] for s in ordered)
    emit(ordered, f"ISEB-CPT-V{v}-ALL",
         f"ISEB Common Pre-Test v{v}",
         f'{len(ordered)} tests · {total_q} questions · {total_m} minutes in total',
         root, a.script_url)

    # 2. Single-test pages, for drilling one paper on its own.
    for sec, pl in payloads.items():
        emit([pl], f"ISEB-CPT-V{v}-{sec}",
             f'ISEB Common Pre-Test v{v} · {SEC_NAME[sec]}',
             f'{len(pl["questions"])} questions · {pl["minutes"]} minutes · '
             f'one question per screen · you cannot go back',
             root / SEC_SLUG[sec], a.script_url)


if __name__ == "__main__":
    main()
