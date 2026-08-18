# Online test-page builder — source of truth

Every online test page on prep.hk-schools.com (CAT4, IDAT, MAP, STAR, GL,
EnglishScore — and any new family) MUST be generated from the templates in
`_builder/templates/`. Do **not** hand-roll a template or copy an old page;
that is how the two recurring bugs below kept coming back.

## The two rules that must never regress

### 1. No access-code gate flash
The `#gate` overlay is unused (access codes were retired). In every template
it ships **hidden**:

```html
<div id="gate" style="display:none">
```

If you ever see a bare `<div id="gate">` (no `style="display:none"`), the page
will show a grey "Enter the access code" panel for a split second before the
JavaScript hides it. That is the flash. Keep the inline `display:none`.

### 2. Figure cropping — never a fixed rectangle, always verified
Figure images are cropped from the source Questions PDF. **Never clip to a
hardcoded rectangle**, and never ship a crop you have not checked.

Use `extract_figures.extract_question_images()` in this folder. It crops to the
page's real content (grey header band and the footer separator/Next Question
button removed, then trimmed tight to the ink) and then asserts that **no ink
touches the border of the result**. Ink on the border means the crop cut the
question, and it raises instead of shipping.

If you build a figure any other way, gate it before embedding:

```python
extract_figures.assert_not_clipped(png_bytes, label="g5 L1 D1 q13")
```

Do NOT reintroduce either historical clip:
- `Rect(48, bb[1]-22, 550, bb[3]+16)` — hardcoded x-range.
- a fixed-size rect such as the 746×552pt one used for the MAP maths drills.

**Why (2026-08-10 incident).** The MAP maths drills were built with a fixed
746×552pt rect on pages 1054×662pt, discarding ~29% of the width and ~17% of
the height. Because the vendor's answer options sit inside the screenshot, the
options were cut off. `grade-5/math/level-1/drill-1` q13 ("Which shape does not
contain a right angle?") shipped with two of its four shapes missing —
unanswerable. 143 figures across 30 deployed tests had to be rebuilt from
source. A fixed rectangle cannot know where the content ends.

Two further traps found while fixing it, both handled in `figure_crop.py`:
- The source PDFs are **not in question order** (in one 15-page quiz, pages
  5–15 are Q1–Q11 and pages 1–4 are Q12–Q15). Never map page index to question
  number; match by content.
- A few vendor pages are screenshots taken mid-scroll, so the question really
  is cut off in the source. That is unrecoverable — detect it (the page's own
  full-content crop is also clipped) and flag it rather than pretending.

## Templates
- `templates/figure_drill.html` — figure drills (images embedded as base64; POSTs `type:"figdrill"`).
- `templates/verbal_drill.html` — verbal / text drills (POSTs `type:"drill"`).
- `templates/test_page.html` — full-length tests.

All three: gate hidden, email **required**, one question per screen, practice-
mode review at the end. Replace `__LEVEL__`, `__DRILL__`, `__ACCESS_CODE__` (set
to empty string), the `SCRIPT_URL`, and the `/*__QUESTIONS_JSON__*/[]` payload.

## Quick self-check before uploading any generated page
- `grep -c '<div id="gate">' page.html` → must be **0**
- `grep -c 'id="gate" style="display:none"' page.html` → must be **1**
- Spot-check the first and last figure image: no leaked question numbers in the corners.

## IDAT pages — `build_idat.py`

IDAT test pages are GENERATED from the paper folder, never hand-assembled:

```
python3 _builder/build_idat.py build ~/Desktop/Claude/Test-Prep/IDAT/2026-08-18-hkis-s3-v4
python3 _builder/build_idat.py check idat-tests/hkis/stage3/v4/index.html <paper-dir>
```

`build` writes `idat-tests/<school>/stage<N>/v<V>/index.html` (school/stage/version
inferred from the paper folder name). Shell comes from `templates/idat_page.html`;
only title/SCHOOL/STAGE/VERSION and the QUESTIONS array vary per page.

**Why this exists.** The first v4/v5 pages were assembled by hand with figures taken
only from the maths section, so three Logic questions shipped without the figure they
depend on (count-the-triangles, shape sequence, figure analogy) — unanswerable online.
The same pass also emitted `"C": "", "D": ""` on 2-option Watson-Glaser items, which
the renderer drew as blank clickable buttons.

Both are now structurally impossible:

- every section's figures are built via `render_paper.figure_to_svg` (not just maths);
- a **parity check** compares page figures against the source `*-final.json` and
  ABORTS the build (or exits 1 in `check`) if any figure is missing or fails to build;
- empty option slots are dropped, so authentic 2/3-option items render correctly.

Section order mirrors the paper: English (grammar/vocab, then reading) → Writing →
Character → Maths → Global Knowledge/Logic. Listening & Speaking is platform-delivered
and deliberately not published online. Writing `intro`/`hint` come from the paper's own
`writing.framing` / `writing.instruction` fields.

Round-trip verified: rebuilding stage3 v4 and v5 reproduces the live pages byte for byte.
