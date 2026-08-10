#!/usr/bin/env python3
"""Content-aware figure cropper for MAP vendor screenshot PDFs.

Replaces the old hardcoded clip rect. Strategy:
  1. render the page
  2. cut the grey header band and the footer band (separator rule + pink
     Next Question / Submit test button)
  3. drop the content-card border rules so they don't dominate the bbox
  4. tight-crop to the remaining ink, with a fixed margin

Guarantees the whole question - stem, figure AND every option - survives,
because nothing is clipped by a fixed rectangle any more.
"""
import io
import numpy as np
from PIL import Image
import fitz

INK = 235          # < this = ink
MARGIN = 14        # px of white kept around content (at render scale)
MAX_W = 1600       # final downscale ceiling


def _render(page, scale):
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    return a[:, :, :3].astype(np.int16)


def _header_bottom(a):
    """First row below the grey title band (0 if there isn't one).

    Scans for a SUSTAINED white run rather than the first white row - the
    header contains light gaps between its rules, and stopping at the first
    one used to leave the vendor title sitting inside the crop.
    """
    H = a.shape[0]
    med = np.median(a.mean(axis=2), axis=1)
    run = 0
    for y in range(int(H * 0.15)):
        if med[y] >= 250:
            run += 1
            if run >= 8:
                return y - run + 1
        else:
            run = 0
    return 0


def _footer_top(a):
    """First row of the footer chrome (page height if there isn't one)."""
    H = a.shape[0]
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    # The Next Question / Submit test button is a wide solid CRIMSON block in the
    # bottom of the page. Constrain colour and position so magenta question
    # artwork (e.g. a pink triangle at (221,66,157)) is never mistaken for it.
    pink = (R > 150) & (G < 70) & (B > 40) & (B < 130)
    per = pink.sum(axis=1)
    per[:int(H * 0.75)] = 0
    ys = np.where(per >= 80)[0]
    if not len(ys):
        return H
    top = int(ys.min())
    # The footer is [separator rule][Question n/N + button]. Cut at the rule
    # nearest above the button. Walking up by whitespace instead used to stop
    # in the gap between two stacked answer figures and lop the last one off.
    med = np.median(a.mean(axis=2), axis=1)
    for y in range(top - 1, max(0, top - 260), -1):
        if med[y] < 250:
            return y
    return max(0, top - 24)


def _strip_rules(mask):
    """Zero out full-span horizontal/vertical rules (the content-card border)."""
    h, w = mask.shape
    if h == 0 or w == 0:
        return mask
    m = mask.copy()
    rows = mask.sum(axis=1) > 0.92 * w
    cols = mask.sum(axis=0) > 0.92 * h
    m[rows, :] = False
    m[:, cols] = False
    return m


def crop_question(page, scale=2.0, max_w=MAX_W):
    a = _render(page, scale)
    H, W, _ = a.shape
    top, bot = _header_bottom(a), _footer_top(a)
    if bot - top < 40:
        top, bot = 0, H
    # sanity: the kept region must hold real content, not just card borders.
    # (a full-span vertical rule contributes a constant few px per row)
    probe = _strip_rules(a[top:bot].mean(axis=2) < INK)
    if probe.sum() < 400:
        top, bot = _header_bottom(a), H
    region = a[top:bot]
    mask = region.mean(axis=2) < INK
    mask = _strip_rules(mask)
    ys, xs = np.where(mask)
    if len(ys) == 0:
        ys, xs = np.where(region.mean(axis=2) < INK)
    if len(ys) == 0:
        y0, y1, x0, x1 = 0, region.shape[0], 0, region.shape[1]
    else:
        y0, y1 = int(ys.min()), int(ys.max()) + 1
        x0, x1 = int(xs.min()), int(xs.max()) + 1
    y0 = max(0, y0 - MARGIN); x0 = max(0, x0 - MARGIN)
    y1 = min(region.shape[0], y1 + MARGIN); x1 = min(region.shape[1], x1 + MARGIN)
    out = _trim_edge_rules(region[y0:y1, x0:x1]).astype(np.uint8)
    im = Image.fromarray(out, "RGB")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    return im


def border_ink(im, edge=2, thresh=0.02):
    """Sides whose border pixels contain ink -> content was clipped."""
    g = np.asarray(im.convert("L")).astype(int)
    h, w = g.shape
    out = []
    for side, band in (("top", g[:edge, :]), ("bottom", g[-edge:, :]),
                       ("left", g[:, :edge]), ("right", g[:, -edge:])):
        if band.size and (band < INK).mean() > thresh:
            out.append(side)
    return out


def to_png(im, optimize=True):
    b = io.BytesIO()
    im.save(b, format="PNG", optimize=optimize)
    return b.getvalue()


def content_mask(a):
    """(ink mask with card rules removed, header_bottom, footer_top)."""
    top, bot = _header_bottom(a), _footer_top(a)
    if bot - top < 40:
        top, bot = 0, a.shape[0]
    m = np.zeros(a.shape[:2], bool)
    m[top:bot] = _strip_rules(a[top:bot].mean(axis=2) < INK)
    return m, top, bot


def grow_to_elements(mask, box, top, bot, iters=4):
    """Expand a crop box so it never cuts an element in half.

    Alternately snap the horizontal extent to every bit of ink on the rows the
    box spans, and the vertical extent to every bit of ink in those columns.
    A box that clipped option C therefore swallows option D too, instead of
    stopping in the white gutter between them.
    """
    H, W = mask.shape
    x0, y0, x1, y1 = box
    x0 = max(0, min(x0, W - 1)); x1 = max(x0 + 1, min(x1, W))
    y0 = max(top, min(y0, bot - 1)); y1 = max(y0 + 1, min(y1, bot))
    for _ in range(iters):
        band = mask[y0:y1, :]
        cols = np.where(band.any(axis=0))[0]
        if len(cols):
            nx0, nx1 = min(x0, int(cols.min())), max(x1, int(cols.max()) + 1)
        else:
            nx0, nx1 = x0, x1
        band2 = mask[top:bot, nx0:nx1]
        rows = np.where(band2.any(axis=1))[0]
        if len(rows):
            ny0 = min(y0, top + int(rows.min()))
            ny1 = max(y1, top + int(rows.max()) + 1)
        else:
            ny0, ny1 = y0, y1
        if (nx0, ny0, nx1, ny1) == (x0, y0, x1, y1):
            break
        x0, y0, x1, y1 = nx0, ny0, nx1, ny1
    return x0, y0, x1, y1


def _trim_edge_rules(a, limit=8):
    """Drop up to `limit` border rows/cols that are full-span card rules, so a
    leftover 1px frame line doesn't read as clipped content."""
    y0, y1, x0, x1 = 0, a.shape[0], 0, a.shape[1]
    for _ in range(limit):
        sub = a[y0:y1, x0:x1]
        if sub.shape[0] < 4 or sub.shape[1] < 4:
            break
        m = sub.mean(axis=2) < INK
        h, w = m.shape
        moved = False
        if m[0].mean() > 0.92:
            y0 += 1; moved = True
        if m[-1].mean() > 0.92:
            y1 -= 1; moved = True
        if m[:, 0].mean() > 0.92:
            x0 += 1; moved = True
        if m[:, -1].mean() > 0.92:
            x1 -= 1; moved = True
        if not moved:
            break
    return a[y0:y1, x0:x1]


def crop_located(page, box, scale, max_w=MAX_W, margin=MARGIN):
    """Re-crop a figure in place: keep the original framing, but grown until
    nothing is clipped, then trimmed tight to ink with a clean margin."""
    a = _render(page, scale)
    mask, top, bot = content_mask(a)
    x0, y0, x1, y1 = grow_to_elements(mask, box, top, bot)
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(ys):
        y0, y1 = y0 + int(ys.min()), y0 + int(ys.max()) + 1
        x0, x1 = x0 + int(xs.min()), x0 + int(xs.max()) + 1
    y0 = max(top, y0 - margin); x0 = max(0, x0 - margin)
    y1 = min(bot, y1 + margin); x1 = min(a.shape[1], x1 + margin)
    im = Image.fromarray(_trim_edge_rules(a[y0:y1, x0:x1]).astype(np.uint8), "RGB")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    return im
