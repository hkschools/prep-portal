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

### 2. Tight figure cropping
Figure images are cropped from the source Questions PDF. Clip each figure to
its **exact image bounding box** — never bounding-box + padding. Padding below
a figure reaches into the next question's number label, so a stray "2." (etc.)
appears in the lower-left corner of the cropped image.

Use `extract_figures.extract_question_images()` in this folder. It already does
the tight clip:

```python
clip = fitz.Rect(bb[0]-1, bb[1]-1, bb[2]+1, bb[3]+1)   # image bbox only
```

Do NOT reintroduce the old loose clip (`Rect(48, bb[1]-22, 550, bb[3]+16)`).

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
