"""The two remaining figures put the stem text in a left column and the option
pictures in a right one. Find the gutter between them and label only the right."""
import base64, io, os, re, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mapfix as M
from PIL import Image, ImageDraw

APPLY = "--apply" in sys.argv
# label_options does its own pass at import time; never let it see --apply here,
# or it would label the already-labelled figures a second time
_argv, sys.argv = sys.argv[:], [sys.argv[0]]
from label_options import clusters, picture_rows, font, encode, DATA
sys.argv = _argv

TARGETS = [("grade-8/math/full-length", 5), ("grade-8/math/full-length", 13)]


def gutters(im):
    """Every run of fully blank columns in the middle of the image, widest first.
    The one that separates the stem text from the option pictures is among them."""
    g = np.array(im.convert("L"))
    ink = (g < 245).sum(axis=0)
    runs, start = [], None
    lo, hi = int(0.10 * im.width), int(0.90 * im.width)
    for x in range(lo, hi):
        if ink[x] == 0:
            if start is None:
                start = x
        elif start is not None:
            runs.append((start, x))
            start = None
    if start is not None:
        runs.append((start, hi))
    runs = [r for r in runs if r[1] - r[0] >= 0.01 * im.width]
    return sorted(runs, key=lambda r: r[0] - r[1])


def label_right(im, x0, rows, gap):
    """Insert the label strips into the picture column only. A full-width strip
    would slice the stem text sitting beside it and shift half of it down."""
    f = font(max(16, int(gap * 0.72)))
    out = Image.new("RGB", (im.width, im.height + gap * len(rows)), "white")
    d = ImageDraw.Draw(out)
    out.paste(im.crop((0, 0, x0, im.height)), (0, 0))          # left column intact
    prev, shift, letters, placed = 0, 0, iter("ABCDEFGH"), []
    for (bnd, cl) in rows:
        out.paste(im.crop((x0, prev, im.width, bnd[0])), (x0, prev + shift))
        shift += gap
        out.paste(im.crop((x0, bnd[0], im.width, bnd[1])), (x0, bnd[0] + shift))
        for (cx0, cx1) in cl:
            ch = next(letters); placed.append(ch)
            w = d.textlength(ch, font=f)
            d.text((x0 + (cx0 + cx1) / 2.0 - w / 2.0,
                    bnd[0] + shift - gap + gap * 0.12), ch, font=f, fill=(70, 70, 70))
        prev = bnd[1]
    out.paste(im.crop((x0, prev, im.width, im.height)), (x0, prev + shift))
    return out, "".join(placed)


out_imgs = []
for rel, n in TARGETS:
    qs = M.load_questions(rel)
    q = [x for x in qs if x["n"] == n][0]
    nopt = len(q.get("options") or [])
    for fld in ("passage", "img", "fig"):
        v = q.get(fld) or ""
        m = DATA.search(v)
        if not m:
            continue
        im = Image.open(io.BytesIO(base64.b64decode(re.sub(r"\s", "", m.group(1))))).convert("RGB")
        found = None
        for gut in gutters(im):
            rows = picture_rows(im.crop((gut[1], 0, im.width, im.height)), nopt)
            if rows:
                found = (gut[1], rows)
                break
        if not found:
            print("  %s Q%d: no column split yields %d pictures" % (rel, n, nopt))
            break
        x0, rows = found
        gap = max(26, int(im.height * 0.045))
        new, placed = label_right(im, x0, rows, gap)
        print("  %-34s Q%-3s gutter@%d -> labelled %s" % (rel, n, x0, "".join(placed)))
        out_imgs.append(("%s Q%d" % (rel, n), new))
        if APPLY:
            q[fld] = DATA.sub(lambda _: encode(new), v, count=1)
            M.save_questions(rel, qs)
        break

if out_imgs and not APPLY:
    ims = []
    for lab, im in out_imgs:
        c = im.copy(); c.thumbnail((860, 340)); ims.append((lab, c))
    H = sum(x[1].height + 22 for x in ims) + 8
    W = max(x[1].width for x in ims) + 30
    sh = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(sh); y = 6
    for lab, im in ims:
        d.text((12, y), lab, font=font(12), fill=(20, 60, 140))
        sh.paste(im, (18, y + 14)); y += im.height + 22
    sh.save("/tmp/lbl_rest.png"); print("/tmp/lbl_rest.png")
