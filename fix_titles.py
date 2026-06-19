#!/usr/bin/env python3
"""Fix test-page labels: make <title>, the start-screen heading, and the footer
match each page's own SCHOOL/STAGE/VERSION constants.

The bug this guards against: some generators hardcode the visible label to
"IDAT <SCHOOL>: Stage 3 (V1)" while the real stage/version lives only in the JS
constants, so every page displays the wrong stage/version.

Scans every index.html in the repo. Only touches files that declare
  const SCHOOL = "...", STAGE = "...", VERSION = "...";
(i.e. IDAT-style pages); anything else is left untouched.

Run from the repo root:  python3 fix_titles.py
Idempotent — safe to run on every commit/push."""
import re, glob, sys

CONST = re.compile(r'const\s+SCHOOL\s*=\s*"([^"]+)"\s*,\s*STAGE\s*=\s*"([^"]+)"\s*,\s*VERSION\s*=\s*"([^"]+)"')
# any "IDAT <SCHOOL>: Stage <n> (V<n>)" label, however wrong
LABEL = re.compile(r'IDAT\s+[A-Za-z]+:\s*Stage\s*\d+\s*\(V\d+\)')

changed = 0
for f in sorted(glob.glob("**/index.html", recursive=True)):
    src = open(f, encoding="utf-8").read()
    m = CONST.search(src)
    if not m:
        continue  # not an IDAT-style page; leave alone
    correct = f'IDAT {m.group(1)}: Stage {m.group(2)} (V{m.group(3)})'
    new = LABEL.sub(correct, src)
    if new != src:
        open(f, "w", encoding="utf-8").write(new)
        print(f"fixed: {f} -> {correct}")
        changed += 1

print(f"done. {changed} file(s) corrected.")
sys.exit(0)
