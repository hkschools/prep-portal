#!/usr/bin/env python3
"""Fail if any test page would show raw HTML markup to a student.

A page escapes some fields and renders others as HTML. When a field that the
page ESCAPES contains markup, the student sees the tag itself, e.g.
"raining hard.<br><br>Which word best joins..." (spotted on the MAP HKIS
language-usage pages, 2026-08-18).

This checks every page: for each visible field, does the page escape it, and
does the data carry markup? Both true is an error.

    python3 _builder/lint_markup.py            # scan the whole repo
"""
import glob, json, re, sys

FIELDS = ("stem", "intro", "body", "passage")
TAG = re.compile(r"<[a-zA-Z/][^>]{0,20}>")


def escapes(html, field):
    """True when the page passes this field through an escaping esc()."""
    m = re.search(r"function esc\s*\([^)]*\)\s*\{(.{0,400}?)\}", html, re.S)
    if not m or not re.search(r"&amp;|&lt;|replace\(/&/g", m.group(1)):
        return False          # esc() is a passthrough, markup renders as HTML
    if field == "options":
        return bool(re.search(r"esc\(\s*q\.options\[", html))
    return bool(re.search(r"esc\(\s*q\.%s\s*\)" % field, html))


def main():
    bad = []
    for f in sorted(glob.glob("**/index.html", recursive=True)):
        h = open(f, encoding="utf-8", errors="ignore").read()
        m = re.search(r"QUESTIONS\s*=\s*(\[.*?\]);", h, re.S)
        if not m:
            continue
        try:
            qs = json.loads(m.group(1))
        except Exception:
            continue
        for q in qs:
            if not isinstance(q, dict):
                continue
            for fld in FIELDS:
                v = q.get(fld)
                if isinstance(v, str) and TAG.search(v) and escapes(h, fld):
                    bad.append((f, q.get("n") or q.get("id"), fld, TAG.search(v).group(0)))
            o = q.get("options")
            vals = o.values() if isinstance(o, dict) else (o if isinstance(o, list) else [])
            for v in vals:
                if isinstance(v, str) and TAG.search(v) and escapes(h, "options"):
                    bad.append((f, q.get("n") or q.get("id"), "options", TAG.search(v).group(0)))
    for f, n, fld, tag in bad:
        print(f"  ERROR {f} q{n} {fld}: escaped field contains {tag!r}")
    print(f"RESULT: {'PASS' if not bad else 'FAIL'} ({len(bad)} leaking field(s))")
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
