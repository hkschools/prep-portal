#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Singapore K2-S2 MC suite: answer banks (+ online pages).

Content source of truth: the testgen-singapore skill's mc/content modules --
the same modules that render the PDFs -- so paper, page and bank cannot drift.
Hand-keying a bank off a finished paper is what left five IDAT tests silently
mis-grading students for months; see _builder/BUILD_NOTES.md.

    python3 build_mc_suite.py --banks            # banks only
    python3 build_mc_suite.py --banks --pages [SCRIPT_URL]

Test ids:  SG-<LEVEL>-T<n>-<SUBJ>          e.g. SG-P5-T1-MA
Banks:     test-banks/singapore-tests/mc/<subject>/<level>/test-<n>/bank.csv

The whole suite is multiple choice, so every row is auto=1 and auto_marks
equals marks: unlike the P4 entrance mocks there is nothing left to mark by
hand, and the online score IS the paper total.

The 简体 and 繁體 Chinese pages POST the same test id and share ONE bank --
the answers are option numbers, identical in both scripts.
"""
import argparse
import csv
import importlib
import os
import re
import sys

MC = os.path.expanduser("~/.claude/skills/testgen-singapore/engines/mc")
ENGINES = os.path.dirname(MC)
for p in (os.path.join(MC, "content"), MC, ENGINES):
    sys.path.insert(0, p)

HERE = os.path.dirname(os.path.abspath(__file__))
PORTAL = os.path.dirname(HERE)
BANKS = os.path.expanduser("~/Developer/work/test-banks")

SUBJECT_DIR = {"Mathematics": "math", "English": "english"}
SUBJECT_CODE = {"Mathematics": "MA", "English": "EN"}
OPT_SEP = " ||| "   # options are free text; this cannot occur inside one
BANK_HEAD = ["test_id", "q", "type", "category", "strand", "concept_tested",
             "correct", "marks", "auto_marks", "auto", "explanation", "note",
             # the marker's review needs to SHOW the question, not just its
             # number (Alex, 2026-09-02); and the Chinese editions share one
             # bank, so the 繁體 display text rides alongside rather than in a
             # second bank -- one file keeps the KEYS single-source, which is
             # the property that must never break.
             "stem", "options", "strand_tc", "stem_tc", "options_tc"]


def subject_of(meta):
    """Chinese modules declare 'Chinese 华文'/'Chinese'; normalise to one key."""
    s = meta["subject"]
    return "Chinese" if s.startswith("Chinese") else s


def plain(s):
    """Option text for the bank's explanation column, tags and svg stripped."""
    s = re.sub(r"<svg.*?</svg>", "[figure]", str(s), flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def modules():
    """Every content module, in level order, as (name, module)."""
    names = sorted(f[:-3] for f in os.listdir(os.path.join(MC, "content"))
                   if f.endswith(".py") and not f.startswith("_"))
    order = {"k2": 0, "p1": 1, "p2": 2, "p3": 3, "p4": 4,
             "p5": 5, "p6": 6, "s1": 7, "s2": 8}
    names.sort(key=lambda n: (order.get(n.split("_")[1], 99), n))
    return [(n, importlib.import_module(n)) for n in names]


def test_id(meta, form_n):
    subj = subject_of(meta)
    code = SUBJECT_CODE.get(subj, "ZH")
    return f"SG-{meta['level']}-T{form_n}-{code}"


def tc_form(form):
    """The 繁體 projection of a form, via the same converter the PDFs use."""
    sys.path.insert(0, ENGINES)
    import render_p4 as RP
    return RP.tc(form)


def bank_rows(meta, form, tform=None):
    """One row per item. Every item is a four-option MCQ, so every row is
    auto-gradable and carries the paper's own mark value.

    `tform` is the 繁體 projection of the same form (Chinese only); its stems
    and options are written into the *_tc columns so the marking review can be
    rendered in the script the candidate actually sat.
    """
    tid = test_id(meta, form["n"])
    rows = []
    titems = ([i for s in tform["sections"] for i in s["items"]]
              if tform else [])
    for sec in form["sections"]:
        for i in sec["items"]:
            rows.append({
                "test_id": tid,
                "q": str(i["q"]),
                "type": "mcq",
                "category": sec["id"],
                "strand": i["strand"] or sec["name"],
                "concept_tested": i["concept"],
                # The page renders options in bank order and posts A..D by
                # position, so the key is the correct option's INDEX, never
                # its text.
                "correct": "ABCD"[i["ans"]],
                "marks": str(i["marks"]),
                "auto_marks": str(i["marks"]),
                "auto": "1",
                "explanation": (i["explanation"]
                                or plain(i["options"][i["ans"]]))[:400],
                "note": "",
                "stem": plain(i["stem"])[:600],
                "options": OPT_SEP.join(plain(o)[:160] for o in i["options"]),
                "strand_tc": "", "stem_tc": "", "options_tc": "",
            })
            if titems:
                t = titems[len(rows) - 1]
                rows[-1]["strand_tc"] = plain(t["strand"] or sec["name"])
                rows[-1]["stem_tc"] = plain(t["stem"])[:600]
                rows[-1]["options_tc"] = OPT_SEP.join(
                    plain(o)[:160] for o in t["options"])
    return tid, rows


def write_banks(verbose=True):
    made, total_rows = 0, 0
    index = []
    for name, mod in modules():
        meta = mod.META
        subj = subject_of(meta)
        sdir = SUBJECT_DIR.get(subj, "chinese")
        tforms = ([tc_form(f) for f in mod.FORMS]
                  if subj == "Chinese" else [None] * len(mod.FORMS))
        for form, tform in zip(mod.FORMS, tforms):
            tid, rows = bank_rows(meta, form, tform)
            # every question numbered once, 1..N, and marks reconcile with META
            qs = [int(r["q"]) for r in rows]
            assert qs == list(range(1, len(qs) + 1)), f"{tid}: numbering broken"
            assert len(rows) == meta["nq"], \
                f"{tid}: {len(rows)} rows, META says {meta['nq']}"
            tot = sum(int(r["marks"]) for r in rows)
            assert tot == meta["total"], \
                f"{tid}: {tot} marks, META says {meta['total']}"
            assert all(r["correct"] in "ABCD" for r in rows), f"{tid}: bad key"

            d = os.path.join(BANKS, "singapore-tests", "mc", sdir,
                             meta["level"].lower(), f"test-{form['n']}")
            os.makedirs(d, exist_ok=True)
            path = os.path.join(d, "bank.csv")
            with open(path, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=BANK_HEAD)
                w.writeheader()
                for r in rows:
                    w.writerow(r)
            made += 1
            total_rows += len(rows)
            index.append((tid, os.path.relpath(path, BANKS), len(rows), tot))
            if verbose:
                print(f"  {tid:<16} {len(rows):>3} items  {tot:>3} marks  "
                      f"{os.path.relpath(path, BANKS)}")
    print(f"\n{made} banks, {total_rows} items -> {BANKS}/singapore-tests/mc/")
    return index


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--banks", action="store_true")
    ap.add_argument("--pages", action="store_true")
    ap.add_argument("script_url", nargs="?",
                    default="PASTE_YOUR_APPS_SCRIPT_URL_HERE")
    a = ap.parse_args()
    if not (a.banks or a.pages):
        ap.error("nothing to do: pass --banks and/or --pages")
    if a.banks:
        write_banks()
    if a.pages:
        import build_mc_pages                      # noqa: E402
        build_mc_pages.write_pages(a.script_url)
