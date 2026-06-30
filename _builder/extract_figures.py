"""
Canonical figure-image extractor for online test pages (CAT4 / IDAT / MAP /
STAR / GL / EnglishScore — any test whose question strips are rendered as one
image per question in the source Questions PDF).

RULE (do not change): clip each figure to its EXACT image bounding box.
Never add bottom/side padding — padding reaches into the neighbouring
question's number label (the "2." that used to appear in the lower-left
corner of a cropped figure).
"""
import fitz, base64


def extract_question_images(questions_pdf, matrix=2):
    """Return a list of PNG byte strings, one per question image, in reading
    order (top-to-bottom, page-by-page). Tight crop — no padding."""
    doc = fitz.open(questions_pdf)
    out = []
    for pg in range(doc.page_count):
        page = doc[pg]
        for info in sorted(page.get_image_info(), key=lambda i: i["bbox"][1]):
            bb = info["bbox"]
            # tight clip: image bbox only (1px breathing room, never more)
            clip = fitz.Rect(bb[0] - 1, bb[1] - 1, bb[2] + 1, bb[3] + 1)
            pix = page.get_pixmap(matrix=fitz.Matrix(matrix, matrix), clip=clip)
            out.append(pix.tobytes("png"))
    return out


def as_data_uri(png_bytes):
    return "data:image/png;base64," + base64.b64encode(png_bytes).decode()
