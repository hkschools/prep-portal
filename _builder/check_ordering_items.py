#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fails any ordering item whose correct answer is not unique.

Found the hard way.  IDAT CIS Stage 3 v3 Q19 asked a student to order
0.6, 1/2, 0.55, 3/5 from least to greatest and offered both

    A  1/2, 0.55, 0.6, 3/5
    B  1/2, 0.55, 3/5, 0.6

as separate answers.  3/5 IS 0.6, so A and B are the same ordering and both
are right; the key marked A, and every student who noticed the equality had a
coin-flip chance of being marked wrong for understanding the maths.  The bank
explanation even said "0.6 and 3/5 are equal" one sentence before calling B a
distractor for failing to notice they are equal.

Prose review does not catch this -- the item reads fine, and the flaw only
appears once you evaluate the options as numbers.  So evaluate them as
numbers.  For every item whose stem asks for an ordering, each option is
decoded into a tuple of values and counted as correct if it is sorted in the
direction the stem asks for.  Exactly one option must be sorted:

    0 sorted  -> no correct answer exists
    2+ sorted -> the key punishes a defensible answer (the bug above)

Items carrying units (2.4 km vs 850 m), a figure, or any token that will not
parse are reported as SKIPPED rather than guessed at, so the count of what was
NOT machine-checked stays visible.

    python3 _builder/check_ordering_items.py            # published pages
    python3 _builder/check_ordering_items.py --banks    # + bank.csv keys
    python3 _builder/check_ordering_items.py --json out.json
"""
import argparse
import csv
import glob
import json
import os
import re
import sys
from fractions import Fraction

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANKS = os.path.expanduser("~/Developer/work/test-banks")

# Stems that ask for a sequence.  Kept deliberately broad: a false positive
# costs one SKIPPED line, a false negative ships another Q19.
ORDERING = re.compile(
    r"least to greatest|greatest to least|smallest to largest"
    r"|largest to smallest|lowest to highest|highest to lowest"
    r"|ascending|descending|increasing order|decreasing order"
    r"|order (?:these|the|them|from)|arrange (?:these|the|them)"
    r"|put (?:these|the|them).{0,40}\bin order\b"
    r"|\bin order (?:of size|from)\b|rank (?:these|the|them)",
    re.I)

# "Which of these equals 3/8?" legitimately offers equal values; it is an
# equivalence item, not an ordering, and must not be flagged.
EQUIVALENCE = re.compile(
    r"equal to|equals|equivalent|same value|same as|worth the same", re.I)

DESCENDING = re.compile(
    r"greatest to least|largest to smallest|highest to lowest"
    r"|descending|decreasing order", re.I)

TAGS = re.compile(r"<[^>]+>")

# The pages render fractions two ways, and stripping the tags off either one
# silently welds numerator to denominator: 7/12 becomes "712", which parses as
# a number and quietly makes a sound item look broken.  Rebuild "a/b" first.
FRAC_SPAN = re.compile(
    r'<span class="frac">\s*<span class="num">\s*(-?[\d.]+)\s*</span>\s*'
    r'<span class="den">\s*(-?[\d.]+)\s*</span>\s*</span>', re.I)
FRAC_SUP = re.compile(
    r"<sup>\s*(-?[\d.]+)\s*</sup>\s*(?:&frasl;|&#8260;|⁄|/)?\s*"
    r"<sub>\s*(-?[\d.]+)\s*</sub>", re.I)
# 5,049 is one number; "5409, 5904" is two.  Only a comma with exactly three
# digits behind it and no space in front is a thousands separator.
THOUSANDS = re.compile(r"(?<=\d),(?=\d{3}(?!\d))")


def clean(text):
    """Markup -> the string a student actually sees, numbers left parseable."""
    t = FRAC_SPAN.sub(r"\1/\2", text or "")
    t = FRAC_SUP.sub(r"\1/\2", t)
    t = re.sub(r"<br\s*/?>", " ", t, flags=re.I)
    t = TAGS.sub("", t)
    t = t.replace("&nbsp;", " ").replace("&minus;", "−")
    return THOUSANDS.sub("", t)


def parse_value(tok):
    """One numeric token -> Fraction, or None if it is not plain a number.

    Fraction, not float: 1/3 vs 0.333 must not collide through rounding, and
    exact arithmetic is what makes "3/5 == 0.6" provable rather than close.
    """
    t = clean(tok).strip().strip(".,;:")
    t = t.replace("−", "-").replace(",", "")  # unicode minus, 1,250
    if not t:
        return None
    neg = t.startswith("-")
    if neg:
        t = t[1:].strip()
    v = None
    try:
        if t.endswith("%"):
            v = Fraction(t[:-1].strip()) / 100
        elif " " in t and "/" in t:  # mixed number: 1 1/2
            whole, frac = t.split(None, 1)
            v = Fraction(whole) + Fraction(frac)
        else:
            v = Fraction(t)  # handles "3/5", "0.6", "7"
    except (ValueError, ZeroDivisionError):
        return None
    return -v if neg else v


def parse_sequence(text):
    """An option like "1/2, 0.55, 0.6, 3/5" -> [Fraction, ...] or None.

    None means "do not judge this item" -- a unit, a word, anything unparsed.
    """
    body = clean(text).strip()
    if not body:
        return None
    parts = re.split(r"\s*(?:,|;|<|>|→|->)\s*", body)
    parts = [p for p in parts if p.strip()]
    if len(parts) < 2:
        return None
    vals = [parse_value(p) for p in parts]
    return None if any(v is None for v in vals) else vals


def is_sorted(vals, descending):
    pairs = zip(vals, vals[1:])
    return all(a >= b for a, b in pairs) if descending \
        else all(a <= b for a, b in pairs)


def check_item(stem, options):
    """-> (status, detail).  status in ok / BROKEN / SKIPPED / not-ordering."""
    flat = clean(stem)
    if not ORDERING.search(flat):
        return "not-ordering", ""
    if EQUIVALENCE.search(flat):
        return "not-ordering", ""

    seqs = {k: parse_sequence(v) for k, v in options.items()}
    unparsed = [k for k, v in seqs.items() if v is None]
    if unparsed:
        return "SKIPPED", "options not numeric: " + ",".join(sorted(unparsed))

    lengths = {len(v) for v in seqs.values()}
    if len(lengths) != 1:
        return "SKIPPED", "options list different counts of values"

    desc = bool(DESCENDING.search(flat))
    correct = sorted(k for k, v in seqs.items() if is_sorted(v, desc))

    # Two options that decode to the same tuple are the same answer printed
    # twice -- the exact Q19 signature, worth naming explicitly.
    dupes = []
    keys = sorted(seqs)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if seqs[a] == seqs[b]:
                dupes.append(f"{a}={b}")

    if len(correct) == 1 and not dupes:
        return "ok", correct[0]
    if not correct:
        return "BROKEN", "no option is in the requested order"
    if len(correct) > 1:
        d = f" (identical once evaluated: {', '.join(dupes)})" if dupes else ""
        return "BROKEN", f"{len(correct)} options are correct: " \
                         f"{', '.join(correct)}{d}"
    return "BROKEN", f"duplicate values across options: {', '.join(dupes)}"


def pages():
    """Every published test page, as (label, [item dicts])."""
    for path in sorted(glob.glob(os.path.join(REPO, "**", "index.html"),
                                 recursive=True)):
        try:
            src = open(path, encoding="utf-8").read()
        except OSError:
            continue
        m = re.search(r"const QUESTIONS\s*=\s*(\[.*?\]);", src, re.S)
        if not m:
            continue
        try:
            items = json.loads(m.group(1))
        except json.JSONDecodeError:
            print(f"  ! unparsable QUESTIONS: {path}", file=sys.stderr)
            continue
        yield os.path.relpath(path, REPO), items


def bank_keys():
    """test_id -> {q: correct letter}, so a fix to a page that leaves the
    key behind is visible."""
    keys = {}
    for path in glob.glob(os.path.join(BANKS, "**", "bank.csv"),
                          recursive=True):
        try:
            rows = list(csv.DictReader(open(path, encoding="utf-8")))
        except OSError:
            continue
        for row in rows:
            if row.get("test_id") and row.get("q"):
                keys.setdefault(row["test_id"], {})[row["q"]] = \
                    (row.get("correct", ""), path)
    return keys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--banks", action="store_true",
                    help="also compare each verdict with the bank.csv key")
    ap.add_argument("--json", metavar="PATH", help="write findings as JSON")
    args = ap.parse_args()

    keys = bank_keys() if args.banks else {}
    broken, skipped, checked, scanned = [], [], 0, 0

    for label, items in pages():
        scanned += 1
        test_id = ""
        for it in items:
            if it.get("type") != "mcq":
                continue
            opts = it.get("options") or {}
            if len(opts) < 2:
                continue
            status, detail = check_item(it.get("stem", ""), opts)
            if status == "not-ordering":
                continue
            qnum = it.get("qnum") or it.get("n")
            rec = {"page": label, "qnum": qnum, "n": it.get("n"),
                   "stem": clean(it.get("stem", ""))[:180],
                   "options": opts, "detail": detail}
            if status == "SKIPPED":
                skipped.append(rec)
                continue
            checked += 1
            if status == "BROKEN":
                if keys:
                    # label like idat-tests/cis/stage3/v3/index.html
                    parts = label.split("/")
                    guess = "-".join(p.upper() for p in parts[1:-1])
                    rec["bank_key"] = next(
                        (v[0] for tid, qs in keys.items()
                         for q, v in qs.items()
                         if q == str(it.get("n")) and tid.replace("-", "")
                         in guess.replace("-", "")), "")
                broken.append(rec)

    print(f"Scanned {scanned} published pages.")
    print(f"Ordering items machine-checked: {checked}")
    print(f"Ordering items skipped (units/words/figures): {len(skipped)}")
    print(f"BROKEN: {len(broken)}\n")

    for r in broken:
        print(f"BROKEN  {r['page']}  Q{r['qnum']} (item {r['n']})")
        print(f"        {r['stem']}")
        for k in sorted(r["options"]):
            print(f"          {k}  {clean(r['options'][k])}")
        print(f"        -> {r['detail']}")
        if r.get("bank_key"):
            print(f"        bank key says: {r['bank_key']}")
        print()

    if skipped and os.environ.get("SHOW_SKIPPED"):
        print("--- skipped (need a human) ---")
        for r in skipped:
            print(f"SKIP    {r['page']}  Q{r['qnum']}: {r['stem'][:90]}")
            print(f"        {r['detail']}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"scanned_pages": scanned, "checked": checked,
                       "broken": broken, "skipped": skipped}, fh, indent=2)
        print(f"wrote {args.json}")

    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
