#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Drift audit: page == bank == content module, for the SIS Singapore tests.

    python3 check_singapore.py

The failure this exists to catch is the documented one: a page regenerated
without its bank (or the reverse) serves different questions than it grades, and
nothing looks wrong until students are silently mis-marked.  Run after every
build and before publishing.

Checks, per page:
  1. every question on the page has a bank row, and vice versa where gradable
  2. the option count and the printed option markers match the content module
  3. the bank's `correct` letter points at the content module's answer text
  4. mark totals reconcile to the paper
  5. the two BUILD_NOTES gate rules (no access-code flash)
"""
import json
import os
import re
import sys

SKILL = os.path.expanduser("~/.claude/skills/testgen-singapore/engines")
sys.path.insert(0, SKILL)
import content_en_p4 as EN     # noqa: E402
import content_ma_p4 as MA     # noqa: E402
import content_zh_p4 as ZH     # noqa: E402
import render_p4 as R          # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PORTAL = os.path.dirname(HERE)
BANKS = os.path.expanduser("~/Developer/work/test-banks")

fails = []


def bad(where, msg):
    fails.append(f"{where}: {msg}")
    print(f"  FAIL {msg}")


def read_bank(subject, n):
    import csv
    p = os.path.join(BANKS, "singapore-tests", subject, "p4", f"mock-{n}", "bank.csv")
    with open(p, encoding="utf-8") as fh:
        return {r["q"]: r for r in csv.DictReader(fh)}


def read_page(slug, n):
    p = os.path.join(PORTAL, "singapore-tests", slug, "p4", f"mock-{n}", "index.html")
    s = open(p, encoding="utf-8").read()
    qs = json.loads(re.search(r"const QUESTIONS = (\[.*?\]);\n", s, re.S).group(1))
    return s, qs


PAGES = [("english", "english", EN, "EN"), ("math", "math", MA, "MA"),
         ("chinese-sc", "chinese", ZH, "ZH"), ("chinese-tc", "chinese", ZH, "ZH")]

# Mock numbers come from the content modules.  A hard-coded (1, 2, 3) silently
# skipped Mock 4 the day it was written: the audit stayed green while an unaudited
# page and bank sat on disk.  Never enumerate forms by literal.
checked = 0
for slug, subject, mod, code in PAGES:
    for n in [f["n"] for f in mod.FORMS]:
        where = f"{slug}/mock-{n}"
        print(f"\n{where}")
        html, page = read_page(slug, n)
        bank = read_bank(subject, n)
        form = [f for f in mod.FORMS if f["n"] == n][0]
        # The Traditional page must be EXACTLY the OpenCC conversion of the same
        # items -- checking that is the point, so convert the reference too rather
        # than exempting the page from the comparison.
        src_items = R.tc(form["items"]) if slug.endswith("-tc") else form["items"]
        items = {str(i["q"]): i for i in src_items}

        # 1 -- gate rules from BUILD_NOTES
        if html.count('<div id="gate">'):
            bad(where, "bare #gate div: access-code panel will flash")
        if html.count('id="gate" style="display:none"') != 1:
            bad(where, "gate is not shipped hidden")

        # 2 -- page vs bank
        # A screen may carry several questions: a cloze passage shown once with a
        # dropdown per blank, or a flyer with its eight questions listed under it.
        # Flatten the screens to the questions they actually ask before comparing.
        def asked(scr):
            return ([{"label": p["label"], "options": p.get("options"),
                      "labels": p.get("labels"), "stem": p.get("stem", scr["stem"]),
                      "screen": scr} for p in scr["parts"]]
                    if scr.get("parts") else [dict(scr, screen=scr)])
        page = [q for scr in page for q in asked(scr)]
        plabels = [q["label"] for q in page]
        if len(set(plabels)) != len(plabels):
            bad(where, "duplicate question labels on the page")
        for lab in plabels:
            if lab not in bank:
                bad(where, f"Q{lab} is on the page but has no bank row")
        for q, row in bank.items():
            if row["auto"] == "1" and q not in plabels:
                bad(where, f"Q{q} is gradable in the bank but absent from the page")

        # 3 -- page/bank vs the content module
        for q in page:
            lab = q["label"]
            it, row = items.get(lab), bank.get(lab)
            if it is None:
                bad(where, f"Q{lab} is on the page but not in the content module")
                continue
            # A hand-marked item is asked online through its `online` variant, so
            # that is what the page and bank must match -- not the paper's wording.
            # An `online` variant need not be multiple choice: Section C's kg-and-g
            # item is asked online as a plain number, so it carries no options.
            src_opts = (it["online"].get("options") if it.get("online")
                        else it.get("options"))
            src_ans = (it["online"]["ans"] if it.get("online") else it["ans"])
            if q.get("options"):
                if q["options"] != src_opts:
                    bad(where, f"Q{lab} page options differ from the content module")
                # A dropdown carries no visible option markers -- the option text
                # IS the choice -- so the marker count only applies to listed options.
                inline = (q.get("screen") or {}).get("mode") == "inline"
                if not inline and len(q.get("labels") or []) != len(q["options"]):
                    bad(where, f"Q{lab} has {len(q['options'])} options but "
                               f"{len(q.get('labels', []))} markers")
                if row and row["type"] == "mcq":
                    want = "ABCDEFGH"[src_ans]
                    if row["correct"] != want:
                        bad(where, f"Q{lab} bank key {row['correct']} != module answer {want}")
            elif row and row["auto"] == "1" and not (q.get("input") or q.get("multiline")):
                bad(where, f"Q{lab} is gradable but offers no way to answer")
            # a gradable item must never be flagged as hand-marked, and vice versa
            hand = bool(q.get("note")) and "marked by hand, not online" in q.get("note", "")
            if row and (row["auto"] == "0") != hand:
                bad(where, f"Q{lab} hand-marked note disagrees with bank auto={row['auto']}")

        # 4 -- marks reconcile
        paper = sum(int(r["marks"]) for r in bank.values())
        online = sum(int(r["auto_marks"]) for r in bank.values() if r["auto"] == "1")
        # per FORM: Mock 4 maths is a 100-mark SAP-standard paper
        expect_paper = form.get("total", mod.TOTAL_MARKS)
        if paper != expect_paper:
            bad(where, f"bank marks total {paper}, expected {expect_paper}")
        # The house SVG line-art rule is SCOPED (".q svg { ... fill:none }"). A
        # figure rendered outside that wrapper loses it and paints as a solid black
        # disc -- the mass-scale and clock items then have no readable needle at
        # all. This has bitten twice; assert the rule exists and that the page
        # actually renders questions inside that class.
        if "<svg" in html:
            m = re.search(r"([^{}]*\bsvg\b[^{}]*)\{([^}]*fill\s*:\s*none[^}]*)\}",
                          html)
            if not m:
                bad(where, "page draws figures but carries no svg line-art rule "
                           "(fill:none): dials and clocks will render solid black")
            else:
                scope = m.group(1).strip().split()[0]
                if scope.startswith(".") and f'class=\\"{scope[1:]}\\"' not in html \
                        and f'class="{scope[1:]}"' not in html:
                    bad(where, f"line-art rule is scoped to {scope}, but nothing on "
                               f"the page carries that class")
        # A typed WORD cannot be marked. A number can (canon_ strips units, currency
        # and spacing), and a choice obviously can. Alex, 2026-09-01: "there are some
        # sections where it is free writing or free fill in for the words which we
        # cannot grade." So on a spec-driven paper, free-word answers are a failure,
        # not a judgement call -- 37 of the English paper's 95 marks were once
        # ungradeable this way, including "fill in one suitable word", where any
        # alternatives list marks some correct answers wrong.
        if form.get("spec"):
            free = [r for r in bank.values() if r["auto"] == "1"
                    and r["type"] in ("word", "text")]
            if free:
                qq = ", ".join(f"Q{r['q']}" for r in free[:8])
                bad(where, f"{len(free)} online answers are free-typed words "
                           f"({qq}{'...' if len(free) > 8 else ''}) — a matcher "
                           f"cannot mark these; ask them as choices")
        print(f"    {len(page)} questions · {online} marked online · bank {len(bank)} rows")
        checked += 1

print()
if fails:
    print(f"{len(fails)} FAILURES")
    sys.exit(1)
print(f"PAGE == BANK == CONTENT for all {checked} pages")
