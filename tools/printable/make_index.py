#!/usr/bin/env python3
"""Write an index of the printable MAP papers, and QA every PDF that was built."""
import glob
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mapfix as M            # noqa: E402
import mapcontent as C        # noqa: E402

ROOT = Path(os.environ.get(
    "MAP_PDF_OUT",
    Path.home() / "Desktop/Claude/Test-Prep/MAP/2026-09-13_Printable-Papers"))


def pages(pdf):
    d = pdf.read_bytes()
    return len(re.findall(rb"/Type\s*/Page[^s]", d))


def main():
    rels = sorted(os.path.relpath(os.path.dirname(p), M.PORTAL)
                  for p in glob.glob(M.PORTAL + "/**/index.html", recursive=True))
    rows, missing, empty = [], [], []
    total_pages = 0
    for rel in rels:
        slug = rel.replace("/", "_")
        paper = ROOT / rel / ("%s.pdf" % slug)
        key = ROOT / rel / ("%s_ANSWERS.pdf" % slug)
        n = len(M.load_questions(rel))
        if not paper.exists() or not key.exists():
            missing.append(rel)
            continue
        pp, kp = pages(paper), pages(key)
        if pp == 0 or kp == 0:
            empty.append(rel)
        total_pages += pp + kp
        rows.append((rel, n, pp, kp, paper.stat().st_size // 1024))

    groups = defaultdict(list)
    for rel, n, pp, kp, kb in rows:
        groups[rel.split("/")[0]].append((rel, n, pp, kp, kb))

    lines = [
        "MAP PRACTICE PAPERS - PRINTABLE EDITION",
        "=" * 64,
        "",
        "Built 13 September 2026 from the live online tests at prep.hk-schools.com.",
        "Each paper is generated straight from the test's own question data, so the",
        "printed paper and the screen version ask the same questions, in the same",
        "order, with the same answer choices under the same letters.",
        "",
        "For every test there are two files:",
        "",
        "  <name>.pdf            the paper a student sits",
        "  <name>_ANSWERS.pdf    the marker copy: correct letter, answer text and",
        "                        the working behind it, plus the letter spread",
        "",
        "%d papers, %d PDFs, %d pages in total." % (len(rows), len(rows) * 2, total_pages),
        "",
    ]
    for g in sorted(groups):
        lines.append("")
        lines.append(g.upper())
        lines.append("-" * 64)
        lines.append("  %-44s %4s %6s %5s" % ("PAPER", "Qs", "PAGES", "KEY"))
        for rel, n, pp, kp, kb in sorted(groups[g]):
            lines.append("  %-44s %4d %6d %5d" % (rel, n, pp, kp))
    lines += ["", "", "NOTES", "-" * 64,
              "Answer keys are separate files so a paper can be handed to a student",
              "without them. Question numbering matches the online test exactly.",
              "MAP itself is adaptive and untimed; the suggested time on each cover is",
              "a working estimate for a paper sitting, not an official limit.",
              ""]
    (ROOT / "README.txt").write_text("\n".join(lines), encoding="utf-8")

    print("index written: %s" % (ROOT / "README.txt"))
    print("papers: %d   PDFs: %d   pages: %d" % (len(rows), len(rows) * 2, total_pages))
    if missing:
        print("\nMISSING (%d):" % len(missing))
        for m in missing:
            print("   ", m)
    if empty:
        print("\nZERO-PAGE (%d):" % len(empty))
        for e in empty:
            print("   ", e)
    if not missing and not empty:
        print("every paper and key present, none empty")


if __name__ == "__main__":
    main()
