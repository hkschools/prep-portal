#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent drift audit: every printed answer key vs its online bank.

The bank is generated from the item data and so is the paper, which makes
drift structurally impossible -- but "impossible" is exactly what was believed
about the five IDAT tests that mis-graded students for months.  So this checks
the two ends of the pipeline against each other by reading the RENDERED PDF,
not the source: if a key sheet and a bank ever disagree about a single
question, this fails.

    python3 verify_mc_banks.py
"""
import glob
import os
import re
import subprocess
import sys

BANKS = os.path.expanduser(
    "~/Developer/work/test-banks/singapore-tests/mc")
PDFS = os.path.expanduser(
    "~/Desktop/Claude/Test-Prep/SIS/2026-09-02_MC-Suite-K2-S2")

SUBJ_PDF = {"math": "Mathematics", "english": "English",
            "chinese": "Chinese 华文"}
# English/maths keys print "12 (3) option text"; Chinese keys print "12 ③"
LATIN = re.compile(r"(?<![\d.])(\d{1,2})\s*\(([1-4])\)")
CJK = re.compile(r"(?<![\d.])(\d{1,2})\s*([①②③④])")
CIRCLED = {"①": 1, "②": 2, "③": 3, "④": 4}


def key_pdf(subject, level, form):
    """The printed answer key for one test (Chinese: the 简体 edition).

    Globbed, not composed: the Chinese modules disagree about whether the
    subject prints as "Chinese" or "Chinese 华文", and a composed name that
    misses would silently look like a missing paper."""
    word = {"math": "Mathematics", "english": "English",
            "chinese": "Chinese*"}[subject]
    lab = "*（简体）*" if subject == "chinese" else "*"
    hits = glob.glob(os.path.join(
        PDFS, level.upper(),
        f"Singapore {level.upper()} {word} - MC Test {form}{lab}"
        f"(Answer Key).pdf"))
    return hits[0] if hits else ""


def printed_answers(path):
    txt = subprocess.run(["pdftotext", "-layout", path, "-"],
                         capture_output=True, text=True).stdout
    out = {}
    for q, n in LATIN.findall(txt):
        out.setdefault(int(q), int(n))
    for q, c in CJK.findall(txt):
        out.setdefault(int(q), CIRCLED[c])
    return out


def bank_answers(path):
    rows = open(path, encoding="utf-8").read().strip().split("\n")[1:]
    out = {}
    for r in rows:
        cells = next(__import__("csv").reader([r]))
        out[int(cells[1])] = "ABCD".index(cells[6]) + 1
    return out


def main():
    fails, checked = [], 0
    for bank in sorted(glob.glob(os.path.join(BANKS, "*", "*", "*", "bank.csv"))):
        parts = bank.split(os.sep)
        subject, level, form = parts[-4], parts[-3], parts[-2].split("-")[1]
        pdf = key_pdf(subject, level, form)
        tid = f"{level.upper()}/{subject}/test-{form}"
        if not pdf:
            fails.append(f"{tid}: no printed answer key PDF found")
            continue
        want, got = bank_answers(bank), printed_answers(pdf)
        checked += 1
        missing = sorted(set(want) - set(got))
        if missing:
            fails.append(f"{tid}: key sheet has no answer for Q{missing}")
        bad = [q for q in sorted(want) if q in got and want[q] != got[q]]
        if bad:
            fails.append(f"{tid}: bank vs printed key differ at "
                         f"Q{bad} (bank {[want[q] for q in bad]}, "
                         f"key {[got[q] for q in bad]})")
    print(f"{checked} tests cross-checked, {len(fails)} mismatches")
    for f in fails:
        print("  FAIL ", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
