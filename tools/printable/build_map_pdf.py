#!/usr/bin/env python3
"""Build house-style PDF papers from the live online MAP tests.

One PDF per paper (what the student sits) plus one answer key PDF (what the tutor
marks from). Content comes straight from the portal's QUESTIONS array and the
bank's key, so the paper and the online test cannot drift apart.

  python3 build_map_pdf.py --rel grade-3/math/level-1/drill-1
  python3 build_map_pdf.py --all
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mapfix as M                                        # noqa: E402
import mapcontent as C                                    # noqa: E402

HS = Path.home() / ".claude/skills/house-style"
RENDER = HS / "engine/hs_render.py"
EXTRA_CSS = Path(__file__).resolve().parent / "map-paper.css"
OUTROOT = Path(os.environ.get(
    "MAP_PDF_OUT",
    Path.home() / "Desktop/Claude/Test-Prep/MAP/2026-09-13_Printable-Papers"))

# Runs inside the render Chrome, before it prints: measures real laid-out heights
# and packs the blocks into explicit A4 sheets. The recipe forbids relying on CSS
# page breaks; this does the pagination the recipe asks for, from live metrics.
PAGINATOR = r"""
<script>
(function () {
  var MM = 96 / 25.4;
  // Heights are only true once every figure has decoded. Measuring at parse time
  // reports an undecoded image as zero-height, so a sheet gets over-filled and the
  // passage later pushes the questions over the footer. Image load events all fire
  // before window.onload, which is what Chrome waits for before printing.
  function whenFiguresReady(run) {
    var pending = Array.prototype.slice.call(document.images)
                       .filter(function (im) { return !im.complete; });
    if (!pending.length) { run(); return; }
    var left = pending.length;
    function done() { if (--left === 0) run(); }
    pending.forEach(function (im) {
      im.addEventListener('load', done);
      im.addEventListener('error', done);
    });
  }
  var BUDGET = 256.5 * MM;              // 296.5mm sheet less 14mm top and 26mm bottom
  var flow = document.getElementById('flow');
  var doc = document.getElementById('doc');
  var queue = Array.prototype.slice.call(flow.children);
  var sheets = [], sheet = null, sc = null;

  var repeatable = null;                  // e.g. the answer-key column header

  function newSheet(carry) {
    sheet = document.createElement('div');
    sheet.className = 'sheet';
    sc = document.createElement('div');
    sc.className = 'sc';
    sheet.appendChild(sc);
    doc.appendChild(sheet);
    sheets.push(sheet);
    if (carry && repeatable) sc.appendChild(repeatable.cloneNode(true));
    return sheet;
  }

  // the block is the only real content on this sheet (a carried-over repeating
  // header does not count as company)
  function alone() {
    var n = sc.children.length;
    if (n === 1) return true;
    return n === 2 && repeatable && sc.children[0].dataset
           && sc.children[0].dataset.repeat;
  }

  // split an element into two, by handing its children to two clones of itself
  function halve(el) {
    if (!el) return null;
    var kids = Array.prototype.slice.call(el.children);
    if (kids.length < 2) return null;
    var mid = Math.ceil(kids.length / 2);
    var a = el.cloneNode(false), b = el.cloneNode(false);
    for (var i = 0; i < kids.length; i++) (i < mid ? a : b).appendChild(kids[i]);
    return [a, b];
  }

  // A question taller than one sheet must be divided, not allowed to grow: a
  // sheet taller than A4 spills over the footer and onto the next printed page.
  // Divide at the seams that already exist - passage, then question and options -
  // and only halve a passage's own contents if one passage is itself that long.
  function split(b) {
    if (!b.classList || !b.classList.contains('blk')) return halve(b);
    var body = b.querySelector('.qbody');
    var numEl = b.querySelector('.qn');
    if (!body) return halve(b);
    var kids = Array.prototype.slice.call(body.children);
    if (kids.length < 2) {
      var inner = halve(kids[0]);
      if (!inner) return null;
      kids = inner;
    }
    var groups = [], cur = [];
    for (var k = 0; k < kids.length; k++) {
      if (kids[k].classList && kids[k].classList.contains('stim')) {
        if (cur.length) { groups.push(cur); cur = []; }
        groups.push([kids[k]]);
      } else {
        cur.push(kids[k]);
      }
    }
    if (cur.length) groups.push(cur);
    if (groups.length < 2) return null;

    var num = numEl ? numEl.textContent.trim() : '';
    var out = [];
    for (var g = 0; g < groups.length; g++) {
      var blk = document.createElement('div');
      blk.className = 'blk';
      var q = document.createElement('div');
      q.className = 'q';
      var qn = document.createElement('div');
      qn.className = 'qn';
      qn.innerHTML = (g === 0 && numEl) ? numEl.innerHTML : '';
      var nb = document.createElement('div');
      nb.className = 'qbody';
      if (g > 0) {
        var c = document.createElement('div');
        c.className = 'cont';
        c.textContent = 'Question ' + num + ', continued';
        nb.appendChild(c);
      }
      for (var m = 0; m < groups[g].length; m++) nb.appendChild(groups[g][m]);
      q.appendChild(qn);
      q.appendChild(nb);
      blk.appendChild(q);
      out.push(blk);
    }
    return out;
  }

  whenFiguresReady(function () {
  newSheet(false);
  var i = 0;
  while (i < queue.length) {
    var b = queue[i];
    if (b.dataset && b.dataset.repeat) repeatable = b;
    sc.appendChild(b);
    if (sc.scrollHeight > BUDGET) {
      if (alone()) {
        var parts = split(b);
        if (parts) {
          sc.removeChild(b);
          queue.splice.apply(queue, [i, 1].concat(parts));
          continue;                     // retry, starting with the first piece
        }
        // indivisible (a single full-page figure): shrink it rather than let it
        // run over the footer
        var z = 100;
        while (sc.scrollHeight > BUDGET && z > 50) {
          z -= 4;
          b.style.zoom = (z / 100);
        }
        newSheet(true);
      } else {
        // move it to a fresh sheet and weigh it again there: a block that is
        // itself taller than a sheet still has to be divided
        newSheet(true);
        continue;
      }
    }
    i++;
  }
  flow.parentNode.removeChild(flow);

  // a trailing sheet with nothing on it would print as a blank page
  if (sc.children.length === 0 || (repeatable && alone() && sc.children[0].dataset
      && sc.children[0].dataset.repeat)) {
    doc.removeChild(sheet);
    sheets.pop();
  }

  var total = sheets.length;
  for (var s = 0; s < total; s++) {
    var f = document.createElement('div');
    f.className = 'foot';
    f.innerHTML = '<span>HK-Schools.com</span>'
                + '<span class="mid">' + doc.dataset.docid + '</span>'
                + '<span>Page ' + (s + 1) + ' of ' + total + '</span>';
    sheets[s].appendChild(f);
  }
  });
})();
</script>
"""


def esc(s):
    return html.escape(str(s), quote=True)


def strand_table(order, groups):
    """MAP is one continuous adaptive sequence, so the paper keeps the online order
    and reports its strand mix here instead of cutting the questions into sections."""
    if len(order) < 2:
        return ""
    rows = "".join(
        '<tr><td>%s</td><td class="n">%d</td></tr>' % (esc(s), len(groups[s]))
        for s in order)
    return ('<div class="strands"><h3>What this paper covers</h3>'
            '<table><tr><th>Strand</th><th class="n">Questions</th></tr>%s</table></div>'
            % rows)


def cover(eyebrow, name, variant, minutes, marks, order, groups):
    return (
        '<div class="blk">'
        '<div class="mast">'
        '<div class="eyebrow">%s</div>'
        '<h1>%s</h1>'
        '<div class="meta">Suggested time <b>%d minutes</b> &nbsp;&middot;&nbsp; '
        'Total <b>%d marks</b> &nbsp;&middot;&nbsp; <b>%d</b> questions</div>'
        '<div class="rule"></div>'
        '</div>'
        '<div class="cand">'
        '<div class="cell"><span class="k">Candidate name</span><div class="line"></div></div>'
        '<div class="cell"><span class="k">Date</span><div class="line"></div></div>'
        '</div>'
        '<div class="inst"><h3>Instructions to candidates</h3><ol>%s</ol></div>'
        '%s'
        '</div>'
        % (esc(eyebrow), esc(name + " · " + variant), minutes, marks, marks,
           "".join("<li>%s</li>" % esc(i) for i in C.INSTRUCTIONS),
           strand_table(order, groups)))


def section_head(letter, title, marks):
    return ('<div class="sec"><h2><span class="sl">%s</span>%s</h2>'
            '<span class="marks">%d marks</span></div><div class="sec-rule"></div>'
            % (letter, esc(title), marks))


def build_paper(rel):
    qs = M.load_questions(rel)
    letters = M.get_letters(rel)
    src = open(M.paper_path(rel), encoding="utf-8").read()
    m = re.search(r'const TEST_ID = "([^"]+)"', src)
    doc_id = m.group(1) if m else rel

    n = len(qs)
    eyebrow, name, variant, minutes = C.paper_meta(rel, None, n)

    # group by the section each question already carries
    order, groups = [], {}
    for q in qs:
        s = (q.get("section") or "").strip() or "Questions"
        if s not in groups:
            groups[s] = []
            order.append(s)
        groups[s].append(q)
    body = [cover(eyebrow, name, variant, minutes, n, order, groups)]
    # questions stay in the order the online test asks them, so a student can sit the
    # paper and the screen version and meet the same question at the same number
    for q in qs:
        body.append(C.q_block(q, letters))
    body.append('<div class="blk"><div class="endp">End of paper</div></div>')

    return doc_id, eyebrow, name, variant, "".join(body), n, order, groups


def build_key(rel, doc_id, eyebrow, name, variant, order, groups):
    _, rows = M.load_bank(rel)
    by_n = {int(r["q"]): r for r in rows}
    qs = M.load_questions(rel)
    letters = M.get_letters(rel)

    dist = Counter(by_n[q["n"]]["correct"].strip() for q in qs if q["n"] in by_n)
    chips = "".join('<div class="d">%s <b>%d</b></div>' % (k, dist[k])
                    for k in sorted(dist))

    head = (
        '<div class="blk">'
        '<div class="mast">'
        '<div class="eyebrow">%s</div>'
        '<h1>%s</h1>'
        '<div class="meta">Answer key &nbsp;&middot;&nbsp; <b>%d</b> questions</div>'
        '<div class="rule"></div></div>'
        '<div class="note">Marker copy. Every question carries one mark. '
        'The working shown is the reasoning a student should be able to give, '
        'not a required form of words.</div>'
        '<div class="dist">%s</div>'
        '</div>'
        % (esc(eyebrow), esc(name + " · " + variant), len(qs), chips))

    out = [head]
    out.append('<div class="blk" data-repeat="keyhead"><table class="keytab"><tr>'
               '<th>Q</th><th>Ans</th><th>Answer text</th><th>Why</th></tr></table></div>')
    for q in qs:
        r = by_n.get(q["n"])
        if not r:
            continue
        if True:
            k = r["correct"].strip()
            ci = C.LET.index(k) if k in C.LET else -1
            opts = q.get("options") or []
            atext = re.sub(r"<[^>]+>", "", opts[ci]) if 0 <= ci < len(opts) else ""
            why = re.sub(r"<[^>]+>", "", r.get("explanation") or "")
            out.append('<div class="blk"><table class="keytab"><tr>'
                       '<td class="kq">%d</td><td class="ka"><span>%s</span></td>'
                       '<td class="ks">%s</td><td class="kx">%s</td>'
                       '</tr></table></div>'
                       % (q["n"], esc(k), esc(atext), esc(why)))
    return "".join(out)


def render(body_html, out_pdf, title, doc_id):
    doc = ('<div id="doc" data-docid="%s"></div>'
           '<div class="flow" id="flow">%s</div>%s'
           % (esc(doc_id), body_html, PAGINATOR))
    tmp = Path(tempfile.mkdtemp()) / "body.html"
    tmp.write_text(doc, encoding="utf-8")
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    res = subprocess.run(
        [sys.executable, str(RENDER), "--mode", "paper", "--body", str(tmp),
         "--out", str(out_pdf), "--title", title, "--css", str(EXTRA_CSS)],
        capture_output=True, text=True)
    if res.returncode != 0 or not out_pdf.exists():
        raise RuntimeError("render failed for %s\n%s" % (out_pdf, res.stderr[-1500:]))
    return out_pdf


def slug(rel):
    return rel.replace("/", "_")


def do(rel, keys=True):
    doc_id, eyebrow, name, variant, body, n, order, groups = build_paper(rel)
    outdir = OUTROOT / rel
    title = "%s %s" % (name.replace(" · ", " "), variant)
    p = render(body, outdir / ("%s.pdf" % slug(rel)), title, doc_id)
    made = [p]
    if keys:
        kbody = build_key(rel, doc_id, eyebrow, name, variant, order, groups)
        k = render(kbody, outdir / ("%s_ANSWERS.pdf" % slug(rel)),
                   title + " Answer Key", doc_id + " · KEY")
        made.append(k)
    return made, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rel", action="append", default=[])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--no-keys", action="store_true")
    a = ap.parse_args()

    rels = a.rel
    if a.all:
        import glob
        rels = sorted(os.path.relpath(os.path.dirname(p), M.PORTAL)
                      for p in glob.glob(M.PORTAL + "/**/index.html", recursive=True))
    if not rels:
        ap.error("give --rel or --all")

    ok = fail = 0
    for rel in rels:
        try:
            made, n = do(rel, keys=not a.no_keys)
            ok += 1
            print("  %-42s %2d q  ->  %s" % (rel, n, made[0].name))
        except Exception as e:
            fail += 1
            print("  FAIL %-40s %s" % (rel, e))
    print("\n%d built, %d failed" % (ok, fail))


if __name__ == "__main__":
    main()
