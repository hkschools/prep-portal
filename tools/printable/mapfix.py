"""Shared helpers for patching the MAP papers and their answer banks.

Papers  : prep-portal/map-tests/<path>/index.html  -> const QUESTIONS = [...]
Keys    : test-banks/map-tests/<path>/bank.csv     -> one row per question
"""
import csv, json, os, re, io

# This file lives at <prep-portal>/tools/printable/, so the portal root is two
# levels up and test-banks is assumed to sit beside prep-portal. Override either
# with MAP_PORTAL / MAP_BANKS if the checkouts live somewhere else.
_HERE = os.path.dirname(os.path.abspath(__file__))
_PORTAL_REPO = os.path.dirname(os.path.dirname(_HERE))
PORTAL = os.environ.get("MAP_PORTAL", os.path.join(_PORTAL_REPO, "map-tests"))
BANKS = os.environ.get(
    "MAP_BANKS",
    os.path.join(os.path.dirname(_PORTAL_REPO), "test-banks", "map-tests"))


# ---------------------------------------------------------------- paper (html)

def _span(txt, name):
    """Return (start, end) of the JS literal assigned to `const <name> = `."""
    m = re.search(r"const %s = " % name, txt)
    if not m:
        raise KeyError(name)
    i = m.end()
    open_c = txt[i]
    close_c = {"[": "]", "{": "}"}[open_c]
    depth = 0
    instr = False
    esc = False
    j = i
    while j < len(txt):
        c = txt[j]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                instr = False
        else:
            if c == '"':
                instr = True
            elif c == open_c:
                depth += 1
            elif c == close_c:
                depth -= 1
                if depth == 0:
                    return i, j + 1
        j += 1
    raise ValueError("unbalanced %s" % name)


def paper_path(rel):
    return os.path.join(PORTAL, rel, "index.html")


def load_questions(rel):
    txt = open(paper_path(rel), encoding="utf-8").read()
    a, b = _span(txt, "QUESTIONS")
    return json.loads(txt[a:b])


def save_questions(rel, questions):
    """Re-serialise QUESTIONS, matching the file's existing JSON spacing."""
    p = paper_path(rel)
    txt = open(p, encoding="utf-8").read()
    a, b = _span(txt, "QUESTIONS")
    compact = '{"n": ' not in txt[a:a + 40]     # 17 papers use no-space separators
    seps = (",", ":") if compact else (", ", ": ")
    new = txt[:a] + json.dumps(questions, ensure_ascii=False, separators=seps) + txt[b:]
    open(p, "w", encoding="utf-8", newline="").write(new)


def get_q(questions, n):
    for q in questions:
        if q["n"] == n:
            return q
    raise KeyError("Q%s" % n)


def get_letters(rel):
    txt = open(paper_path(rel), encoding="utf-8").read()
    a, b = _span(txt, "LETTERS")
    return json.loads(txt[a:b])


def set_letters(rel, letters):
    p = paper_path(rel)
    txt = open(p, encoding="utf-8").read()
    a, b = _span(txt, "LETTERS")
    open(p, "w", encoding="utf-8").write(txt[:a] + json.dumps(letters) + txt[b:])


# ----------------------------------------------------------------- bank (csv)

def bank_path(rel):
    return os.path.join(BANKS, rel, "bank.csv")


def _bank_eol(rel):
    """These banks are CRLF; detect per file so a rewrite doesn't churn the diff."""
    with open(bank_path(rel), "rb") as f:
        head = f.read(4096)
    return "\r\n" if b"\r\n" in head else "\n"


def load_bank(rel):
    with open(bank_path(rel), encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


def save_bank(rel, fields, rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator=_bank_eol(rel))
    w.writeheader()
    for row in rows:
        w.writerow(row)
    open(bank_path(rel), "w", encoding="utf-8", newline="").write(buf.getvalue())


def bank_row(rows, n):
    for row in rows:
        if int(row["q"]) == n:
            return row
    raise KeyError("bank Q%s" % n)


# --------------------------------------------------------------------- logging

CHANGES = []


def log(rel, n, what, before, after):
    CHANGES.append((rel, n, what, before, after))
    print("  %-42s Q%-4s %-14s %r -> %r" % (rel, n, what, before, after))


def summary():
    print("\n%d change(s) applied" % len(CHANGES))
