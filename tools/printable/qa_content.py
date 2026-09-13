"""Every question and every option in the online test must appear in the printed
paper. Catches anything pagination dropped."""
import glob
import os, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fitz, mapfix as M

ROOT = os.environ.get("MAP_PDF_OUT", os.path.expanduser(
    "~/Desktop/Claude/Test-Prep/MAP/2026-09-13_Printable-Papers"))
def norm(s):
    """Fold to bare alphanumerics. Never used to strip tags: printed maths text
    contains < and > as real answer options, and tag-stripping eats from one to
    the next."""
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())

def src(s):
    """Source side only: the portal re-enables a few inline tags in stems."""
    return norm(re.sub(r"<[^>]+>", " ", s or ""))

rels = sorted(os.path.relpath(os.path.dirname(p), M.PORTAL)
              for p in glob.glob(M.PORTAL + "/**/index.html", recursive=True))
miss_q = miss_o = 0
tot_q = tot_o = 0
bad = []
for rel in rels:
    qs = M.load_questions(rel)
    pdf = os.path.join(ROOT, rel, rel.replace("/", "_") + ".pdf")
    d = fitz.open(pdf)
    txt = norm("".join(p.get_text() for p in d))
    d.close()
    for q in qs:
        tot_q += 1
        st = src(q.get("stem"))[:40]
        if st and st not in txt:
            miss_q += 1; bad.append(("STEM", rel, q["n"], (q.get("stem") or "")[:60]))
        for o in (q.get("options") or []):
            tot_o += 1
            on = src(o)[:40]
            if on and on not in txt:
                miss_o += 1; bad.append(("OPTION", rel, q["n"], o[:60]))
print("questions checked: %d   options checked: %d" % (tot_q, tot_o))
print("stems missing from print:   %d" % miss_q)
print("options missing from print: %d" % miss_o)
for k, rel, n, s in bad[:25]:
    print("  %-7s %-44s Q%-3s %s" % (k, rel, n, s))
