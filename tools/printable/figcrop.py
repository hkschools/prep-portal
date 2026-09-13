"""Crop captured figures down to the diagram, for print.

Used by the PDF builder only; the online test keeps its images as they are.

Several figures are captures of a whole source question: a line of question text, the
diagram, then the platform's own answer-option strip. The portal already shows the stem
and the options as real text underneath, so the picture repeats them, and where the
captured options disagree with the real ones it actively misleads (that is the fault
found at grade-3 maths Q21).

Split the image into horizontal content bands. The diagram is the tallest band; the
text lines and option strips are the short ones around it. Keep the tallest band.

  python3 crop_figures.py                 report, write before/after sheet
  python3 crop_figures.py --apply         crop in place
"""
import base64, glob, io, os, re, sys
import numpy as np
import mapfix as M
from PIL import Image

PAD = 10
MIN_GAP = 8
DATA = re.compile(r"data:image/png;base64,([A-Za-z0-9+/=\s]+)")


def bands(gray, thresh=245):
    ink = (gray < thresh).sum(axis=1)
    out, start = [], None
    for y, v in enumerate(ink):
        if v > 0 and start is None:
            start = y
        elif v == 0 and start is not None:
            if y - start > 0:
                out.append((start, y))
            start = None
    if start is not None:
        out.append((start, len(ink)))
    # merge bands separated by less than MIN_GAP (keeps a diagram in one piece)
    merged = []
    for b in out:
        if merged and b[0] - merged[-1][1] < MIN_GAP:
            merged[-1] = (merged[-1][0], b[1])
        else:
            merged.append(list(b) if False else (b[0], b[1]))
    return merged


def has_colour(rgb):
    """Strongly saturated pixels mean this band is artwork (a chart legend, a coloured
    key) rather than a line of question text. Measured on real figures: text
    anti-aliasing tops out around a spread of 40 and never reaches 70, while a legend
    swatch clears it by hundreds of pixels."""
    a = rgb.astype(int)
    spread = a.max(axis=2) - a.min(axis=2)
    return int((spread > 70).sum()) > 60


def is_option_strip(gray, y0, y1, H):
    """The source platform draws answer choices as a row of similar boxes. Three or
    more evenly sized clusters low in the image is that strip, not artwork."""
    if y0 < 0.35 * H:
        return False
    col = (gray[y0:y1] < 245).sum(axis=0)
    runs, start = [], None
    for x, v in enumerate(col):
        if v > 0 and start is None:
            start = x
        elif v == 0 and start is not None:
            if x - start > 6:
                runs.append(x - start)
            start = None
    if start is not None and len(col) - start > 6:
        runs.append(len(col) - start)
    if len(runs) < 3:
        return False
    med = sorted(runs)[len(runs) // 2]
    similar = [r for r in runs if abs(r - med) <= 0.45 * med]
    return len(similar) >= 3


LABEL_OPT = re.compile(
    r"^(option|figure|shape|graph|line|bar|solid|clock|point|table|passage|diagram|"
    r"number line|position|answer)?\s*[a-h]\s*(\(.*\))?$", re.I)


def options_are_pictures(options):
    """When the printed choices are bare labels ('Line A', 'Shape C'), the strip of
    little pictures in the capture IS the answer set and must be kept. When they carry
    real values ('22 in.'), that strip only repeats them."""
    if not options:
        return False
    plain = [re.sub(r"<[^>]+>", "", o).strip() for o in options]
    return sum(bool(LABEL_OPT.match(o)) for o in plain) >= max(2, len(plain) - 1)


def _centres(gray, y0, y1):
    """x-centres of the ink clusters in a horizontal band."""
    col = (gray[y0:y1] < 245).sum(axis=0)
    out, start = [], None
    for x, v in enumerate(col):
        if v > 0 and start is None:
            start = x
        elif v == 0 and start is not None:
            if x - start > 2:
                out.append((start + x) / 2.0)
            start = None
    if start is not None:
        out.append((start + len(col)) / 2.0)
    return out


def labels_row(gray, cand, strip, width):
    """Is `cand` the row of A/B/C/D letters belonging to the option pictures in
    `strip`? The letters sit centred over their own pictures, so their x-centres
    line up. Without this the letters are cropped away and the printed options
    ("Shape A") no longer say which picture is which."""
    if cand[1] - cand[0] > 45:
        return False
    a = _centres(gray, cand[0], cand[1])
    b = _centres(gray, strip[0], strip[1])
    # a label row is a handful of marks, every one of them sitting over a picture.
    # Counting only three would miss a 2-2-1 grid, whose top row carries just A and B.
    if not (2 <= len(a) <= 8) or len(b) < 2:
        return False
    tol = 0.035 * width
    hit = sum(1 for x in a if any(abs(x - y) <= tol for y in b))
    return hit == len(a)


def diagram_box(im, options=None):
    """Keep from the first piece of artwork to the last; drop the question text and
    the captured option strip around it."""
    g = np.array(im.convert("L"))
    rgb = np.array(im)
    bs = bands(g)
    if len(bs) < 3:
        return None
    H = im.height
    keep_strip = options_are_pictures(options)

    figure = []
    for (y0, y1) in bs:
        h = y1 - y0
        if not keep_strip and is_option_strip(g, y0, y1, H):
            figure.append(False)
        elif has_colour(rgb[y0:y1]):
            figure.append(True)           # legends and colour keys are artwork
        else:
            figure.append(h >= 60)        # tall monochrome band = a drawing
    if not any(figure):
        return None
    first = figure.index(True)
    last = len(figure) - 1 - figure[::-1].index(True)
    if first == 0 and last == len(bs) - 1:
        return None                       # nothing to trim

    # when the pictures are the answers, their letter row must come too
    if keep_strip and first > 0 and labels_row(g, bs[first - 1], bs[first], im.width):
        first -= 1

    top = max(0, bs[first][0] - PAD)
    bot = min(H, bs[last][1] + PAD)
    if (bot - top) < 0.28 * H:
        return None                       # would throw away too much
    if (bot - top) >= H - 2 * PAD:
        return None
    return top, bot



def crop_for_print(png_bytes, options):
    """Return cropped PNG bytes, or None when this figure should be left alone."""
    im = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    box = diagram_box(im, options)
    if not box:
        return None
    top, bot = box
    buf = io.BytesIO()
    im.crop((0, top, im.width, bot)).save(buf, format="PNG", optimize=True)
    return buf.getvalue()
