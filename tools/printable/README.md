# Printable MAP papers

Builds a print-ready PDF of every online MAP test, plus a separate answer key.

The paper is generated from the test's own `QUESTIONS` array and the matching
`bank.csv`, so the printed paper and the screen version ask the same questions,
in the same order, with the same choices under the same letters. Nothing here
rewrites a question; it only re-dresses it for print. Edit a question online and
rebuild, and the paper follows.

## Use

    python3 build_map_pdf.py --rel grade-3/math/level-1/drill-1
    python3 build_map_pdf.py --all              # all 131 papers, ~1h
    python3 build_map_pdf.py --all --no-keys

    python3 make_index.py                       # README.txt index + presence check
    python3 qa_footers.py                       # page-by-page pagination check
    python3 qa_content.py                       # every stem and option reached print

Output goes to `~/Desktop/Claude/Test-Prep/MAP/<dated folder>/<rel>/`, two files
per paper: `<slug>.pdf` and `<slug>_ANSWERS.pdf`.

## Paths

Resolved from this file's location: the portal is two levels up, and `test-banks`
is assumed to sit beside `prep-portal`. Override with environment variables:

    MAP_PORTAL    <prep-portal>/map-tests
    MAP_BANKS     <test-banks>/map-tests
    MAP_PDF_OUT   where the PDFs are written

## Needs

- the `house-style` skill at `~/.claude/skills/house-style` - `engine/hs_render.py`
  does the rendering and owns the look; `map-paper.css` only extends `paper.css`
- Google Chrome (headless, driven by hs_render)
- `pip install pymupdf numpy pillow`

## Files

| | |
|---|---|
| `build_map_pdf.py` | the builder, and the paginator that runs inside the render browser |
| `mapcontent.py`    | turns a portal question into house-style paper content |
| `figcrop.py`       | trims captured figures down to the artwork, at print time only |
| `mapfix.py`        | reads/writes `QUESTIONS` and `bank.csv` without churning the file |
| `map-paper.css`    | additions to the house paper stylesheet |
| `make_index.py`    | writes the index and checks every paper and key exists |
| `qa_footers.py`    | no text or artwork over the footer, nothing off the sheet |
| `qa_content.py`    | every stem and every option in the online test reached print |

## Two things worth knowing before changing this

**Pagination is done in JavaScript, in the render browser, not by CSS page breaks.**
It measures real laid-out heights and packs blocks into explicit A4 sheets. Two
traps, both already hit and fixed: heights are only true once figures have
*decoded* (an undecoded image measures zero and the sheet gets over-filled), and
a block taller than a sheet must be *divided*, never allowed to grow - a sheet
taller than A4 spills over the footer onto the next printed page. Run
`qa_footers.py` after any change here.

**`figcrop.py` decides what to throw away, so it fails dangerously.** Some figures
are captures of a whole source question: text, diagram, and that platform's own
option strip. The stem and choices are set as type underneath, so the picture
repeats them - but three things in those captures must survive, and each one was
a real bug before its guard existed:

- a coloured chart legend (a key saying which bar is which)
- the option strip itself, when the printed choices are bare labels ("Line A") -
  then the little pictures *are* the answer set
- the row of A/B/C/D letters above those pictures - without it the paper lists
  "Shape A" against five unlabelled shapes

Cropping happens at print time only. The images in the repo are untouched.
