"""Add the A/B/C/D letters to option pictures that have none.

A handful of maths questions show the answers as pictures ("Which solid could this
be?") while the choices are listed as "Solid A" ... "Solid E", and the pictures
carry no letters at all. The student has to guess that they run left to right.
Every other captured figure in the bank labels them, row by row, left to right;
this writes the same labels onto the ones that are missing.

  python3 label_options.py            report + preview sheets
  python3 label_options.py --apply    write the labelled figures back
"""
import base64, io, os, re, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mapfix as M
import figcrop as F
from PIL import Image, ImageDraw, ImageFont

APPLY = "--apply" in sys.argv
DATA = re.compile(r"data:image/png;base64,([A-Za-z0-9+/=\s]+)")

TARGETS = [
    ("grade-3/math/full-length", 16), ("grade-3/math/full-length", 20),
    ("grade-4/math/level-2/drill-1", 8),
    ("grade-4/math/level-2/drill-2", 8), ("grade-4/math/level-3/drill-1", 11),
    ("grade-5/math/level-1/drill-2", 7), ("grade-6/math/full-length", 12),
    ("grade-6/math/full-length", 37), ("grade-6/math/full-length", 41),
    ("grade-7/math/level-3/drill-2", 5), ("grade-8/math/full-length", 5),
    ("grade-8/math/full-length", 13), ("grade-8/math/level-1/drill-1", 6),
]


def clusters(gray, y0, y1, min_w=30, merge_frac=0.03):
    """Ink clusters across a band. Near-touching pieces are merged, so a pie chart
    and the legend beside it count as one picture, not two."""
    col = (gray[y0:y1] < 245).sum(axis=0)
    raw, start = [], None
    for x, v in enumerate(col):
        if v > 0 and start is None:
            start = x
        elif v == 0 and start is not None:
            raw.append((start, x))
            start = None
    if start is not None:
        raw.append((start, len(col)))
    gap = merge_frac * len(col)
    merged = []
    for c in raw:
        if merged and c[0] - merged[-1][1] < gap:
            merged[-1] = (merged[-1][0], c[1])
        else:
            merged.append(c)
    return [c for c in merged if c[1] - c[0] >= min_w]


def _own_labels(gray, cand, strip, width):
    """Does `cand` already hold this row's letters? Same alignment test as the
    print cropper, but a single picture with a single letter counts too."""
    if cand[1] - cand[0] > 45:
        return False
    a = [(c[0] + c[1]) / 2.0 for c in clusters(gray, cand[0], cand[1], min_w=2)]
    b = [(c[0] + c[1]) / 2.0 for c in clusters(gray, strip[0], strip[1], min_w=2)]
    if not a or not b or len(a) > 8:
        return False
    tol = 0.035 * width
    return all(any(abs(x - y) <= tol for y in b) for x in a)


def picture_rows(im, n_opts):
    """The bottom-most run of bands holding exactly n_opts pictures between them.
    Tries tight clustering first, then progressively merges near-touching pieces,
    so a pie chart sitting beside its legend can still count as one picture."""
    g = np.array(im.convert("L"))
    bs = [b for b in F.bands(g) if b[1] - b[0] >= 35]
    for frac in (0.0, 0.005, 0.012, 0.025, 0.04):
        rows = [(b, clusters(g, b[0], b[1], merge_frac=frac)) for b in bs]
        rows = [r for r in rows if r[1]]
        for start in range(len(rows)):
            tail = rows[start:]
            if sum(len(r[1]) for r in tail) != n_opts:
                continue
            # the answer pictures are all about the same width; a paragraph of
            # stem text is one wide cluster and is rejected here
            w = sorted(c[1] - c[0] for r in tail for c in r[1])
            med = w[len(w) // 2]
            if any(abs(x - med) > 0.45 * med for x in w):
                continue
            return tail
    return None


def font(sz):
    for p in ("/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def label(im, n_opts):
    rows = picture_rows(im, n_opts)
    if not rows:
        return None, "could not find %d pictures" % n_opts
    gap = max(26, int(im.height * 0.045))
    fs = max(16, int(gap * 0.72))
    f = font(fs)
    # rebuild the canvas with a white strip above each row of pictures
    out = Image.new("RGB", (im.width, im.height + gap * len(rows)), "white")
    d = ImageDraw.Draw(out)
    g = np.array(im.convert("L"))
    all_bands = F.bands(g)
    prev, shift, letters = 0, 0, iter("ABCDEFGH")
    placed = []
    for (b, cl) in rows:
        # a faint label row already sitting above the pictures is wiped, so the
        # new letters do not print on top of the old ones
        above = [x for x in all_bands if x[1] <= b[0]]
        if above and _own_labels(g, above[-1], b, im.width):
            wipe = above[-1]
            ImageDraw.Draw(im).rectangle([0, wipe[0] - 2, im.width, wipe[1] + 2],
                                         fill=(255, 255, 255))
        out.paste(im.crop((0, prev, im.width, b[0])), (0, prev + shift))
        shift += gap
        out.paste(im.crop((0, b[0], im.width, b[1])), (0, b[0] + shift))
        for (x0, x1) in cl:
            ch = next(letters)
            w = d.textlength(ch, font=f)
            d.text(((x0 + x1) / 2.0 - w / 2.0, b[0] + shift - gap + gap * 0.12),
                   ch, font=f, fill=(70, 70, 70))
            placed.append(ch)
        prev = b[1]
    out.paste(im.crop((0, prev, im.width, im.height)), (0, prev + shift))
    return out, "".join(placed)


def encode(im):
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


done, fails, previews = [], [], []
for rel, n in TARGETS:
    qs = M.load_questions(rel)
    q = [x for x in qs if x["n"] == n][0]
    nopt = len(q.get("options") or [])
    hit = False
    for fld in ("passage", "img", "fig"):
        v = q.get(fld) or ""
        m = DATA.search(v)
        if not m:
            continue
        im = Image.open(io.BytesIO(base64.b64decode(re.sub(r"\s", "", m.group(1))))).convert("RGB")
        new, info = label(im, nopt)
        if new is None:
            fails.append((rel, n, info))
        else:
            done.append((rel, n, nopt, info))
            previews.append((rel, n, new))
            if APPLY:
                q[fld] = DATA.sub(lambda _: encode(new), v, count=1)
                M.save_questions(rel, qs)
        hit = True
        break
    if not hit:
        fails.append((rel, n, "no embedded png"))

for rel, n, nopt, info in done:
    print("  %-38s Q%-3s %d options -> labelled %s" % (rel, n, nopt, info))
for rel, n, why in fails:
    print("  FAILED %-32s Q%-3s %s" % (rel, n, why))
print("\n%d labelled, %d failed (%s)" % (len(done), len(fails), "applied" if APPLY else "dry run"))

if previews and not APPLY:
    for i in range(0, len(previews), 5):
        ch = previews[i:i+5]
        ims = []
        for rel, n, im in ch:
            c = im.copy(); c.thumbnail((820, 260)); ims.append(("%s Q%d" % (rel, n), c))
        Ht = sum(x[1].height + 22 for x in ims) + 8
        W = max(x[1].width for x in ims) + 30
        sh = Image.new("RGB", (W, Ht), "white"); dd = ImageDraw.Draw(sh); y = 6
        for lab, img in ims:
            dd.text((12, y), lab, font=font(12), fill=(20, 60, 140))
            sh.paste(img, (18, y+14)); y += img.height + 22
            dd.line([8, y-5, W-8, y-5], fill=(225, 225, 225))
        sh.save("/tmp/lbl_%d.png" % (i//5+1)); print("/tmp/lbl_%d.png" % (i//5+1))
