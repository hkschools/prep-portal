"""
Canonical figure-image extractor for online test pages (CAT4 / IDAT / MAP /
STAR / GL / EnglishScore — any test whose question strips are rendered as one
image per question in the source Questions PDF).

RULE (do not change): NEVER clip a figure to a fixed rectangle, and never trust
a clip without checking it. Crop to the page's real content and then PROVE
nothing was cut by asserting no ink touches the border.

Why this file is paranoid — 2026-08-10 incident:
an earlier build cropped every MAP maths figure with a hardcoded rect. On pages
1054pt wide it kept ~746pt, so the right-hand answer options were silently
thrown away. Questions like "Which shape does not contain a right angle?" — the
options ARE the picture — shipped to students with options C and D missing and
were impossible to answer. 143 figures across 30 deployed tests had to be
rebuilt from source. A fixed rectangle cannot know where the content ends; only
the pixels can tell you.
"""
import base64

import fitz

import figure_crop


def extract_question_images(questions_pdf, scale=2.8, strict=True):
    """Return a list of PNG byte strings, one per question page, in page order.

    Each image is cropped to the question's real content: the vendor's grey
    header band and the footer (separator rule + Next Question button) are
    removed, then the crop is trimmed tight to the ink with a clean margin.

    With strict=True (the default) a figure whose border still carries ink
    raises, because that means content was cut off. Pass strict=False only for
    sources whose own page is genuinely cut mid-scroll, and log what you skip.
    """
    doc = fitz.open(questions_pdf)
    out = []
    for pg in range(doc.page_count):
        im = figure_crop.crop_question(doc[pg], scale=scale)
        clipped = figure_crop.border_ink(im)
        if clipped and strict:
            raise ValueError(
                f"{questions_pdf} p{pg + 1}: content touches the "
                f"{'/'.join(clipped)} edge — the crop is cutting the question. "
                f"Fix the crop; do not ship it.")
        out.append(figure_crop.to_png(im))
    return out


def assert_not_clipped(png_bytes, label=""):
    """Gate any figure — however it was produced — before it is embedded."""
    import io

    from PIL import Image
    sides = figure_crop.border_ink(Image.open(io.BytesIO(png_bytes)))
    if sides:
        raise ValueError(f"figure {label} is clipped on: {', '.join(sides)}")


def as_data_uri(png_bytes):
    return "data:image/png;base64," + base64.b64encode(png_bytes).decode()
