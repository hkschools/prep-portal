#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Drift audit for the Singapore K2-S2 MC suite: page == bank == content module.

    python3 check_mc_pages.py               # all 108 pages
    python3 check_mc_pages.py --sample 8    # a spread across subjects and levels

The failure this exists to catch is the documented one (BUILD_NOTES.md): a page
regenerated without its bank -- or options reordered on the page -- serves
different questions than it grades, and nothing looks wrong until students are
silently mis-marked.  The page posts A/B/C/D BY POSITION, so the bank's key is
only correct while the page's option ORDER is the content module's.

Per page:
  1. the page's test id is the bank's test id
  2. the page carries exactly the bank's questions, same numbers, same order
  3. every question offers exactly 4 options
  4. the page's options are the content module's, in the module's order
  5. the option at the bank's `correct` index IS the module's correct option
  6. the bank is fully auto-graded and its marks reconcile with META
  7. the two BUILD_NOTES gate rules (no access-code flash)
"""
import argparse
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_mc_suite as S                                       # noqa: E402
import build_mc_pages as B                                       # noqa: E402

sys.path.insert(0, os.path.expanduser(
    "~/.claude/skills/testgen-singapore/engines"))
import render_p4 as R                                            # noqa: E402

PORTAL = os.path.dirname(HERE)
BANKS = os.path.expanduser("~/Developer/work/test-banks")

fails = []


def bad(where, msg):
    fails.append(f"{where}: {msg}")


def read_page(slug, level, n):
    p = os.path.join(PORTAL, "singapore-tests", "mc", slug, level,
                     f"test-{n}", "index.html")
    s = open(p, encoding="utf-8").read()
    qs = json.loads(re.search(r"const QUESTIONS = (\[.*?\]);\n", s, re.S).group(1))
    tid = re.search(r'const TEST_ID = "([^"]+)"', s).group(1)
    # flatten: a stimulus screen carries several real questions
    flat = []
    for q in qs:
        for part in (q["parts"] if q.get("parts") else [q]):
            flat.append(part)
    return p, s, tid, flat


def read_bank(subject, level, n):
    p = os.path.join(BANKS, "singapore-tests", "mc", subject, level,
                     f"test-{n}", "bank.csv")
    with open(p, encoding="utf-8") as fh:
        return p, list(csv.DictReader(fh))


def audit(mod, form, slug, script):
    meta = mod.META
    subject = S.SUBJECT_DIR.get(S.subject_of(meta), "chinese")
    level, n = meta["level"].lower(), form["n"]
    tag = f"{slug}/{level}/test-{n}"

    path, src, page_tid, qs = read_page(slug, level, n)
    _, rows = read_bank(subject, level, n)
    tid = S.test_id(meta, n)

    # 1 -- one id, posted by the page, keyed by the bank
    if page_tid != tid:
        bad(tag, f"page posts {page_tid}, expected {tid}")
    if any(r["test_id"] != tid for r in rows):
        bad(tag, "bank rows carry a different test id")

    # 2 -- same questions, same order
    if len(qs) != len(rows):
        bad(tag, f"{len(qs)} questions on the page, {len(rows)} bank rows")
    if [q["label"] for q in qs] != [r["q"] for r in rows]:
        bad(tag, "page question numbers differ from the bank's")

    # the module's items, in paper order, converted for the 繁體 edition exactly
    # as the page converts them
    f = R.tc(form) if script == "tc" else form
    items = [i for s_ in f["sections"] for i in s_["items"]]
    if len(items) != len(rows):
        bad(tag, f"{len(items)} items in the module, {len(rows)} bank rows")

    for q, r, i in zip(qs, rows, items):
        where = f"{tag} Q{r['q']}"
        # 3 -- four options, always
        if len(q["options"]) != 4:
            bad(where, f"{len(q['options'])} options on the page, expected 4")
            continue
        # 4 -- the module's options, in the module's order
        if list(q["options"]) != list(i["options"]):
            bad(where, "page options differ from the content module's "
                       "(order or text)")
            continue
        # 5 -- the bank's key points at the module's correct option
        if r["correct"] not in "ABCD":
            bad(where, f"bank key {r['correct']!r} is not A-D")
            continue
        k = "ABCD".index(r["correct"])
        if q["options"][k] != i["options"][i["ans"]]:
            bad(where, f"bank says {r['correct']} = {q['options'][k]!r}, "
                       f"module's answer is {i['options'][i['ans']]!r}")
        if k != i["ans"]:
            bad(where, f"bank index {k} != module ans {i['ans']}")
        # 6 -- nothing left to mark by hand
        if r["auto"] != "1" or r["auto_marks"] != r["marks"]:
            bad(where, "row is not fully auto-graded")

    if sum(int(r["marks"]) for r in rows) != meta["total"]:
        bad(tag, "bank marks do not reconcile with META total")

    # 7 -- BUILD_NOTES gate rules
    if src.count('<div id="gate">'):
        bad(tag, "bare #gate div (access-code flash)")
    if src.count('id="gate" style="display:none"') != 1:
        bad(tag, "#gate does not ship hidden")
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=0,
                    help="audit only N pages, spread across subjects/levels")
    a = ap.parse_args()

    jobs = []
    for _name, mod in S.modules():
        for form in mod.FORMS:
            for slug, script, _c, _u in B.editions(mod):
                jobs.append((mod, form, slug, script))
    if a.sample:
        step = max(1, len(jobs) // a.sample)
        jobs = jobs[::step][:a.sample]

    for mod, form, slug, script in jobs:
        before = len(fails)
        path = audit(mod, form, slug, script)
        mark = "ok  " if len(fails) == before else "FAIL"
        print(f"  {mark} {os.path.relpath(path, PORTAL)}")

    print(f"\n{len(jobs)} pages audited, {len(fails)} problems")
    for f in fails:
        print("  FAIL ", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
