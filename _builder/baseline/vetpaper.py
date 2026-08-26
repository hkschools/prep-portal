#!/usr/bin/env python3
"""House-style vetting PDFs for the HKS Baseline Assessment.

    python3 vetpaper.py [--band level-b] [--version 1] [--all-versions]

Per paper, renders TWO branded PDFs through the mandatory house-style engine
(~/.claude/skills/house-style/engine/hs_render.py), reusing the CAT4
drillpaper's calibrated geometry and pagination:

  Baseline_<Label>_V<n>_Questions.pdf   (paper mode: navy masthead, candidate
                                         strip, circled options, .sheet pages)
  Baseline_<Label>_V<n>_AnswerKey.pdf   (report mode: flowing key with pills,
                                         explanations, curriculum codes, and
                                         the full listening transcripts)

Output: ~/Desktop/Claude/Test-Prep/Baseline/<date>_Vetting/
"""
import argparse
import base64
import datetime
import io as _io
import os
import re
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))          # _builder (for build_baseline)
sys.path.insert(0, os.path.expanduser("~/.claude/skills/testgen-cat4/engines"))
import drillpaper as dp                            # noqa: E402  (geometry + hs_render path)

import importlib.util


def _load(band, version):
    p = os.path.join(HERE, f"{band.replace('-', '_')}_v{version}.py")
    if not os.path.exists(p):
        return None
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    spec = importlib.util.spec_from_file_location(f"vet_{band}_{version}", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _assemble(mod, band, version):
    """Reuse the builder's assemble() so numbering/nodash match the live page."""
    import build_baseline as bb
    test_id = f"BASELINE-{band.upper()}-V{version}"
    questions, bank, errs = bb.assemble(mod, test_id, group=False)
    if errs:
        sys.exit(f"vetpaper: assemble errors: {errs}")
    bb.apply_house_text(questions, bank)
    return questions, bank


VET_CSS = """
.passage { border: 0.4pt solid #c9d0dc; border-left: 1.1mm solid #72afdb;
           border-radius: 1.5mm; padding: 3mm 4mm; margin: 0 0 4mm;
           font-size: 10pt; line-height: 1.5; color: #1a2233; }
.audnote { font-size: 9pt; color: #8a6d1f; margin: 0 0 3mm; }
.tasks { border: 0.4pt solid #c9d0dc; border-radius: 1.5mm; padding: 3mm 4mm;
         margin: 0 0 5mm; font-size: 10pt; line-height: 1.55; white-space: pre-wrap; }
.tasks .th { font-weight: 700; color: #14213a; margin-bottom: 1.5mm; }
.qtext { white-space: pre-wrap; }
.qtext i { color: #566072; }
.infig { font-size: 8.5pt; color: #8a93a5; margin: 1mm 0 0; }
.q { page-break-inside: avoid; }
.emo { font-size: 42pt; line-height: 1.3; margin: 0 3mm; vertical-align: middle; }
.opt .w .emo { font-size: 25pt; margin: 0 2mm; }
.zh, .zh * { font-family: "Helvetica Neue", "PingFang TC", "PingFang SC", sans-serif; }
"""

AK_EXTRA_CSS = dp.REPORT_CSS + """
.tscript { border: 0.4pt solid #c9d0dc; border-left: 1.1mm solid #72afdb;
           border-radius: 1.5mm; padding: 3mm 4mm; margin: 2mm 0 4mm;
           font-size: 9.5pt; line-height: 1.55; color: #3c4759; page-break-inside: avoid; }
.tscript .tf { font-weight: 700; color: #14213a; margin-bottom: 1mm; }
.tscript .v { color: #72afdb; font-weight: 700; }
.zh, .zh * { font-family: "Helvetica Neue", "PingFang TC", "PingFang SC", sans-serif; }
"""


def _strip(html_s):
    return re.sub(r"<[^>]+>", "", str(html_s))


def _svg_img(fig):
    """Inline <svg> -> data-URI <img>.

    Chrome's print path rasterises SVG <text> into Type 3 bitmap glyphs, which
    print as blurred, over-heavy blobs ("38" reads as "36"). The same SVG behind
    an <img> goes through the image path and keeps crisp vector text, so every
    figure in the PDF is wrapped this way. Width is the SVG's own px size in mm
    (96 dpi), capped to the content column.
    """
    if not fig or not fig.lstrip().startswith("<svg"):
        return fig
    m = re.search(r'<svg[^>]*width="([\d.]+)"[^>]*height="([\d.]+)"', fig)
    w_mm = min(float(m.group(1)) * 0.2646, dp.CONTENT_W) if m else dp.CONTENT_W
    b64 = base64.b64encode(fig.encode("utf-8")).decode()
    return f'<img src="data:image/svg+xml;base64,{b64}" style="width:{w_mm:.1f}mm">'


def _fig_height(fig):
    m = re.search(r'src="data:image/png;base64,([^"]+)"', fig)
    if m:
        try:
            from PIL import Image
            img = Image.open(_io.BytesIO(base64.b64decode(m.group(1))))
            w, h = img.size
            return dp.CONTENT_W * h / w + dp.H_QGAP
        except Exception:
            return 60.0
    m = re.search(r'<svg[^>]*width="([\d.]+)"[^>]*height="([\d.]+)"', fig)
    if m:
        w, h = float(m.group(1)), float(m.group(2))
        disp_w = min(w * 0.2646, dp.CONTENT_W)      # px -> mm at 96 dpi
        return disp_w * h / w + dp.H_QGAP + 2
    return 60.0


def _q_block(q):
    """One question -> html. Options render as house circles.

    No height is estimated here: _paginate() measures every block in Chrome at
    the real sheet width. Character-count estimates were what pushed bilingual
    Chinese questions through the footer.
    """
    opts_items = [(L, v) for L, v in q["options"].items()]
    has_text_opts = any(str(v).strip() for _, v in opts_items)
    zh = ' zh' if re.search(r"[一-鿿]", _strip(q["stem"])) else ""
    fig = _svg_img(q.get("fig", ""))
    parts = [f'<div class="q{" img" if fig and not has_text_opts else ""}{zh}">',
             f'<div class="qn">{q["n"]}</div><div class="qbody">']
    if q.get("audio"):
        parts.append(f'<div class="audnote">Listening · recording {q["audio"]} (transcript in the answer key)</div>')
    parts.append(f'<div class="qtext">{q["stem"]}</div>')
    if fig:
        parts.append(f'<div class="figwrap">{fig}</div>')
    if has_text_opts:
        opts = "".join(f'<div class="opt"><span class="L">{L}</span><span class="w">{v}</span></div>'
                       for L, v in opts_items)
        parts.append(f'<div class="opts">{opts}</div>')
    else:
        opts = "".join(f'<div class="opt"><span class="L">{L}</span></div>' for L, _ in opts_items)
        parts.append(f'<div class="opts">{opts}</div>'
                     '<div class="infig">The answer choices are labelled A to E inside the figure.</div>')
    parts.append("</div></div>")
    return "".join(parts)


def _passage_block(p_html):
    zh = ' zh' if re.search(r"[一-鿿]", _strip(p_html)) else ""
    return f'<div class="passage{zh}">{p_html}</div>'


def _task_block(title, q):
    body = "\n\n".join(x for x in (q.get("intro"), q.get("stem"), q.get("body"), q.get("hint")) if x)
    return f'<div class="tasks"><div class="th">{title}</div>{body}</div>'


# --------------------------------------------------------------- measurement
MEASURE_JS = """
<pre id="HSMEASURE" style="display:none"></pre>
<script>
function hsMeasure() {
  // Height is the distance to the NEXT block's top, not the block's own box:
  // the inner .q/.passage margins collapse through the wrapper, so a plain
  // getBoundingClientRect() reports a block shorter than the space it occupies
  // and the last question on a page ends up printed over the footer.
  var els = Array.prototype.slice.call(document.querySelectorAll('[data-mi]'));
  var tops = els.map(function (el) { return el.getBoundingClientRect().top; });
  var out = els.map(function (el, i) {
    var h;
    if (i + 1 < els.length) {
      h = tops[i + 1] - tops[i];
    } else {
      var r = el.getBoundingClientRect();
      h = r.height + parseFloat(getComputedStyle(el).marginBottom || 0);
    }
    return [+el.dataset.mi, h * 25.4 / 96];
  });
  document.getElementById('HSMEASURE').textContent = 'HS' + JSON.stringify(out) + 'HS';
}
window.addEventListener('load', function () {
  // colour-emoji glyphs and data-URI figures settle a frame after load
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () { requestAnimationFrame(hsMeasure); });
  } else {
    requestAnimationFrame(hsMeasure);
  }
});
</script>
"""


def _measure(frags, css):
    """Real rendered height in mm for each fragment, via headless Chrome.

    Blocks are laid out in a sheet-width column with the same stylesheet the
    PDF uses, then each one reports its own box. Returns [] if the measuring
    pass fails, so the caller can fall back to a conservative estimate.
    """
    wrapped = "".join(f'<div data-mi="{i}">{f}</div>' for i, f in enumerate(frags))
    body = ('<div class="sheet" style="height:auto;overflow:visible;'
            'page-break-after:auto">' + wrapped + "</div>" + MEASURE_JS)
    with tempfile.NamedTemporaryFile("w", suffix=".css", delete=False) as f:
        f.write(css)
        css_path = f.name
    doc = _hs_wrap("paper", body, "measure", None, [css_path])
    tmpdir = tempfile.mkdtemp(prefix="hs-measure-")
    html = os.path.join(tmpdir, "m.html")
    with open(html, "w") as f:
        f.write(doc)
    profile = tempfile.mkdtemp(prefix="hs-chrome-m-")
    dump = os.path.join(tmpdir, "dom.html")
    # Chrome does not exit on this machine (see hs_render), so --dump-dom would
    # hang forever on communicate(). Poll its stdout file for the marker and
    # stop the process ourselves, the same way hs_render waits for the PDF.
    proc = None
    try:
        with open(dump, "wb") as sink:
            proc = subprocess.Popen([dp_chrome(), "--headless=new", "--disable-gpu",
                                     "--no-first-run", "--no-default-browser-check",
                                     f"--user-data-dir={profile}",
                                     "--virtual-time-budget=20000", "--dump-dom",
                                     f"file://{html}"],
                                    stdout=sink, stderr=subprocess.DEVNULL)
            deadline = time.time() + 120
            payload = None
            while time.time() < deadline:
                try:
                    text = open(dump, encoding="utf-8", errors="ignore").read()
                except OSError:
                    text = ""
                m = re.search(r"HS(\[.*?\])HS", text, re.S)
                if m:
                    payload = m.group(1)
                    break
                if proc.poll() is not None:
                    break
                time.sleep(0.25)
        if payload is None:
            return []
        import json as _json
        pairs = _json.loads(payload)
        heights = [0.0] * len(frags)
        for i, h in pairs:
            heights[int(i)] = float(h)
        return heights
    except Exception:
        return []
    finally:
        if proc and proc.poll() is None:
            proc.kill()
        os.unlink(css_path)


def dp_chrome():
    import importlib
    hs = importlib.machinery.SourceFileLoader("hs_render_mod", str(dp.RENDER)).load_module()
    return hs.CHROME


def _hs_wrap(mode, body, title, footer_mid, css_files):
    import importlib
    hs = importlib.machinery.SourceFileLoader("hs_render_mod", str(dp.RENDER)).load_module()
    return hs.wrap(mode, body, title, footer_mid, css_files)


def _paginate(blocks, docid, css):
    """blocks: [(html, is_section_head)] -> sheet HTML.

    Every section head starts a fresh page (Alex's rule), and packing uses the
    measured heights so nothing runs into the footer.
    """
    frags = [b[0] for b in blocks]
    # A measuring pass can lose a race with Chrome start-up when papers render
    # back to back. Retry rather than fall back: the old fallback quietly put
    # one block on each page and shipped an 85-page Level B.
    heights = []
    for attempt in range(3):
        heights = _measure(frags, css)
        if len(heights) == len(frags) and sum(heights) > 0:
            break
        print(f"  ! measuring pass {attempt + 1} failed, retrying")
        time.sleep(2)
    else:
        sys.exit("vetpaper: could not measure block heights after 3 attempts; "
                 "no PDF written (a silent fallback would mis-paginate the paper)")
    avail = dp.AVAIL - 4.0                              # tolerance above the footer
    pages, cur, used = [], [], 0.0
    for (frag, is_sec), h in zip(blocks, heights):
        starts_page = is_sec and cur                    # section head: new page
        if starts_page or (cur and used + h > avail):
            pages.append(cur)
            cur, used = [], 0.0
        cur.append(frag)
        used += h
    if cur:
        pages.append(cur)
    total = len(pages)
    return "\n".join(f'<div class="sheet">{"".join(p)}{dp._foot(docid, i + 1, total)}</div>'
                     for i, p in enumerate(pages))


def questions_pdf(mod, band, version, questions, out_dir):
    total_min = sum(s["minutes"] for s in mod.SECTIONS if not s.get("opt") and not s.get("chinese"))
    nq = sum(1 for q in questions if q["type"] == "mcq")
    docid = f"HKS Baseline · {mod.BAND_LABEL} · V{version} · Vetting"
    blocks = [(dp._mast("HKS Baseline Assessment · Internal Vetting Copy",
                        f"{mod.BAND_LABEL} · {mod.YEAR_SPAN}",
                        [("Questions", nq), ("Core time", f"{total_min} min"), ("Version", f"V{version}")])
               + dp._cand()
               + dp._inst(["Internal review copy: answers and curriculum codes are in the separate Answer Key.",
                           "Listening recordings play on the online test page; transcripts are in the Answer Key.",
                           "Section times shown match the online timer.",
                           "Not for distribution to families."]),
               False)]
    letters = iter("ABCDEFGHIJ")
    cur_sec, last_passage, last_audio = None, None, None
    for q in questions:
        if q["section"] != cur_sec:
            cur_sec = q["section"]
            mins = next((s["minutes"] for s in mod.SECTIONS if s["name"] == cur_sec), "?")
            nsec = sum(1 for x in questions if x["section"] == cur_sec and x["type"] == "mcq")
            zh = ' class="zh"' if re.search(r"[一-鿿]", cur_sec) else ""
            sec_html = dp._sec(next(letters), cur_sec,
                               f"{nsec} Q · {mins} min" if nsec else f"{mins} min").replace(" marks</span>", "</span>")
            blocks.append((f'<div{zh}>' + sec_html + "</div>", True))
            # the child reads a short instruction card before each section; the
            # vetting copy dropped it entirely, so the paper was being reviewed
            # without the wording the candidate actually sees
            info_html = getattr(mod, "INFO", {}).get(cur_sec)
            if info_html:
                blocks.append((f'<div{zh}><div class="rubric">{info_html}</div></div>', False))
            last_passage, last_audio = None, None
        if q["type"] == "info":
            continue
        if q["type"] in ("writing", "speaking"):
            blocks.append((_task_block(f"{q['type'].title()} task", q), False))
            continue
        if q.get("audio") and q["audio"] != last_audio:
            last_audio = q["audio"]
        if q.get("passage") and q["passage"] != last_passage:
            last_passage = q["passage"]
            blocks.append((_passage_block(q["passage"]), False))
        blocks.append((_q_block(q), False))
    body = _paginate(blocks, docid, VET_CSS)
    out = os.path.join(out_dir, f"Baseline_{mod.BAND_LABEL.replace(' ', '')}_V{version}_Questions.pdf")
    _render("paper", body, out, docid)
    return out


def answerkey_pdf(mod, band, version, questions, bank, out_dir):
    key = {row["q"]: row for row in bank}
    parts = [f'<h1 style="font-size:16pt;color:#14213a;margin:0 0 1mm">HKS Baseline Assessment · '
             f'{dp.E(mod.BAND_LABEL)} (V{version}) · Answer Key</h1>',
             f'<div style="font-size:9pt;color:#8a93a5;margin-bottom:4mm">{dp.E(mod.YEAR_SPAN)} · '
             'internal vetting copy · answers, explanations, curriculum codes and listening transcripts</div>']
    cur_sec = None
    audio_done = set()
    for q in questions:
        if q["type"] == "info":
            continue
        if q["section"] != cur_sec:
            cur_sec = q["section"]
            zh = ' class="zh"' if re.search(r"[一-鿿]", cur_sec) else ""
            parts.append(f'<div{zh}><div class="akhead"><h2><span class="sl">&#9632;</span>{dp.E(cur_sec)}</h2></div>'
                         '<div class="akrule"></div></div>')
        if q["type"] in ("writing", "speaking"):
            parts.append(f'<div class="akrow"><div class="qn">·</div><div class="akb">'
                         f'<div class="akwhy"><b>{q["type"].title()} task:</b> open response, '
                         f'{"Claude-marked + tutor review" if q["type"] == "writing" else "tutor review of the recording"}.</div></div></div>')
            continue
        if q.get("audio") and q["audio"] not in audio_done:
            audio_done.add(q["audio"])
            lines = getattr(mod, "AUDIO", {}).get(q["audio"], [])
            tx = "<br>".join(f'<span class="v">{dp.E(v)}:</span> {dp.E(t)}' for v, _, t in lines)
            parts.append(f'<div class="tscript"><div class="tf">Transcript · {dp.E(q["audio"])}</div>{tx}</div>')
        k = key[q["n"]]
        opt_txt = q["options"].get(k["correct"], "")
        ans = k["correct"] + (f" · {opt_txt}" if str(opt_txt).strip() else "")
        zhq = ' zh' if re.search(r"[一-鿿]", _strip(q["stem"]) + _strip(str(opt_txt))) else ""
        parts.append(f'<div class="akrow{zhq}"><div class="qn">{q["n"]}</div><div class="akb">'
                     f'<div class="akstem">{_strip(q["stem"])[:150]}</div>'
                     f'<div class="akans"><span class="pill">{k["correct"]}</span>{ans if str(opt_txt).strip() else ""}</div>'
                     f'<div class="akwhy">{dp.E(k["explanation"])}</div>'
                     f'<div class="akcon">{dp.E(k["concept_tested"])}</div></div></div>')
    out = os.path.join(out_dir, f"Baseline_{mod.BAND_LABEL.replace(' ', '')}_V{version}_AnswerKey.pdf")
    _render("report", "".join(parts), out, f"HKS Baseline · {mod.BAND_LABEL} · V{version} · Answer Key")
    return out


def _render(mode, body_html, out_pdf, title):
    css = VET_CSS if mode == "paper" else AK_EXTRA_CSS
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(body_html)
        tmp_body = f.name
    with tempfile.NamedTemporaryFile("w", suffix=".css", delete=False) as f:
        f.write(css)
        tmp_css = f.name
    r = subprocess.run([sys.executable, str(dp.RENDER), "--mode", mode, "--body", tmp_body,
                        "--out", out_pdf, "--title", title, "--css", tmp_css,
                        "--footer-mid", "Internal vetting copy"],
                       capture_output=True, text=True)
    os.unlink(tmp_body)
    os.unlink(tmp_css)
    if r.returncode != 0:
        print(f"  ! hs_render failed for {os.path.basename(out_pdf)}: {r.stderr.strip()[:300]}")
    else:
        print(f"  {out_pdf}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--band", default=None)
    ap.add_argument("--version", default=None)
    a = ap.parse_args()
    out_dir = os.path.expanduser(
        f"~/Desktop/Claude/Test-Prep/Baseline/{datetime.date.today().isoformat()}_Vetting")
    os.makedirs(out_dir, exist_ok=True)
    bands = [a.band] if a.band else ["level-a", "level-b", "level-c", "level-d"]
    versions = [a.version] if a.version else ["1", "2", "3"]
    for band in bands:
        for ver in versions:
            mod = _load(band, ver)
            if not mod:
                continue
            questions, bank = _assemble(mod, band, ver)
            questions_pdf(mod, band, ver, questions, out_dir)
            answerkey_pdf(mod, band, ver, questions, bank, out_dir)


if __name__ == "__main__":
    main()
