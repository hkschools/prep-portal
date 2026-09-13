"""Check every built page for content colliding with the page footer, or
running off the bottom of the sheet."""
import glob
import os, os, sys
import fitz

ROOT = os.environ.get("MAP_PDF_OUT", os.path.expanduser(
    "~/Desktop/Claude/Test-Prep/MAP/2026-09-13_Printable-Papers"))
GAP = 1.5          # pt of tolerance
problems, pages_seen, no_footer = [], 0, []

for pdf in sorted(glob.glob(ROOT + "/**/*.pdf", recursive=True)):
    rel = os.path.relpath(pdf, ROOT)
    doc = fitz.open(pdf)
    for pno, page in enumerate(doc, 1):
        pages_seen += 1
        H = page.rect.height
        blocks = page.get_text("blocks")
        # the footer is the band at the very bottom carrying the wordmark; match on
        # position too, or a passage that happens to say "Page 320" is mistaken for it
        foot = [b for b in blocks
                if b[1] > 0.88 * H and ("HK-Schools.com" in b[4] or "Page " in b[4])]
        if not foot:
            no_footer.append("%s p%d" % (rel, pno))
            continue
        ftop = min(b[1] for b in foot)
        fids = {id(b) for b in foot}
        # text intruding into the footer band
        for b in blocks:
            if id(b) in fids:
                continue
            if b[3] > ftop + GAP:
                problems.append(("TEXT-IN-FOOTER", rel, pno,
                                 round(b[3] - ftop, 1), b[4][:48].replace("\n", " ")))
        # vector art / images intruding
        for d in page.get_drawings():
            r = d["rect"]
            if r.width > 0.9 * page.rect.width and r.height > 0.9 * H:
                continue          # full-sheet background fill, not content
            if d.get("fill") == (1.0, 1.0, 1.0) and not d.get("color"):
                continue          # white-on-white, invisible
            if r.y1 > ftop + GAP and r.height > 1 and r.width > 1:
                problems.append(("ART-IN-FOOTER", rel, pno, round(r.y1 - ftop, 1), ""))
                break
        for im in [r for xr in page.get_images(full=True) for r in page.get_image_rects(xr[0])]:
            if im.y1 > ftop + GAP:
                problems.append(("IMG-IN-FOOTER", rel, pno, round(im.y1 - ftop, 1), ""))
                break
        # anything past the bottom edge
        for b in blocks:
            if b[3] > H + GAP:
                problems.append(("OFF-SHEET", rel, pno, round(b[3] - H, 1),
                                 b[4][:48].replace("\n", " ")))
    doc.close()

print("pages checked: %d" % pages_seen)
print("pages with no footer found: %d" % len(no_footer))
for n in no_footer[:10]:
    print("   ", n)
from collections import Counter
print("collisions: %d" % len(problems))
for k, v in Counter(p[0] for p in problems).most_common():
    print("   %-16s %d" % (k, v))
seen = set()
import collections
agg = collections.defaultdict(float)
for kind, rel, pno, over, txt in problems:
    agg[(rel,pno)] = max(agg[(rel,pno)], over)
print("\naffected pages: %d" % len(agg))
for (rel,pno),ov in sorted(agg.items(), key=lambda x:-x[1]):
    print("  %-58s p%-3d  worst +%.0fpt (%.0fmm)" % (rel,pno,ov,ov*25.4/72))
for kind, rel, pno, over, txt in []:
    print("  %-15s %-52s p%-3d  +%.1fpt  %s" % (kind, rel, pno, over, txt))
