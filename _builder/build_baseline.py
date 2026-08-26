#!/usr/bin/env python3
"""build_baseline.py — generate an HKS Baseline Assessment page + answer bank.

    python3 build_baseline.py build --band level-b [--version 1] [--script-url URL]
    python3 build_baseline.py build --all      [--script-url URL]

Levels: level-a (Y3-4), level-b (Y5-6), level-c (Y7-8), level-d (Y9-10);
level-e (Y11-12) is on hold. Content modules live at
_builder/baseline/<band with _>_v<V>.py and must define:

    BAND, BAND_LABEL, YEARS, SECTIONS, INFO, CONTENT   (+ optional RECORD_MAX_S)

CONTENT maps each SECTIONS name to either a list of MCQ dicts
(stem/options/correct/strand/concept/explanation, optional fig/passage) or a
single writing/speaking dict. Output:

  prep-portal/baseline-tests/<band>/v<V>/index.html   (NO answer keys)
  ../test-banks/baseline-tests/<band>/v<V>/bank.csv   (the keys)

The deployed grader resolves the bank from (band, version) in the payload, so
that pair must stay unique. Validation aborts the build on a missing/invalid
correct letter or a key field leaking into the page JSON, and prints the
answer-letter distribution per section for the QA pass.
"""
import argparse
import csv
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "templates", "baseline_page.html")
PORTAL = os.path.dirname(HERE)
BANKS = os.path.join(os.path.dirname(PORTAL), "test-banks")
PLACEHOLDER_URL = "PASTE_DEPLOYED_EXEC_URL"
BANDS = ["level-a", "level-b", "level-c", "level-d"]


def load_content(band, version):
    p = os.path.join(HERE, "baseline", f"{band.replace('-', '_')}_v{version}.py")
    if not os.path.exists(p):
        sys.exit(f"No content module at {p}")
    if os.path.join(HERE, "baseline") not in sys.path:
        sys.path.insert(0, os.path.join(HERE, "baseline"))
    spec = importlib.util.spec_from_file_location(f"baseline_{band}_{version}", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_LISTEN_PREFIX = re.compile(r"^[^\n]*(?:choose the best answer\.|回答問題。|回答问题。)\s*\n+\s*")


def _strip_listen_prefix(stem):
    """Grouped pages carry one shared player, so per-question 'listen to the
    recording' openers are redundant. Handles bilingual trad<br><i>simp</i>."""
    parts = str(stem).split("<br><i>")
    parts = [_LISTEN_PREFIX.sub("", part, count=1) for part in parts]
    return "<br><i>".join(parts)


def group_listening(out, mod):
    """Merge consecutive MCQs that share one audio file into a single 'lgroup'
    page item (one screen per recording, child-friendly player, exercise
    title). Bank rows and question numbering are untouched."""
    titles = getattr(mod, "AUDIO_TITLES", {})
    grouped, i, g = [], 0, 0
    while i < len(out):
        q = out[i]
        if q.get("type") == "mcq" and q.get("audio"):
            j = i
            items = []
            while j < len(out) and out[j].get("type") == "mcq" and out[j].get("audio") == q["audio"]                     and out[j]["section"] == q["section"]:
                sub = out[j]
                items.append({"n": sub["n"], "qnum": sub["qnum"],
                              "stem": _strip_listen_prefix(sub["stem"]),
                              "options": sub["options"]})
                j += 1
            g += 1
            grouped.append({"n": f"g{g}", "type": "lgroup", "section": q["section"],
                            "audio": q["audio"],
                            "title": titles.get(q["audio"], "Listening"),
                            "items": items})
            i = j
        else:
            grouped.append(q)
            i += 1
    return grouped


def assemble(mod, test_id, include=None, group=True):
    """Info cards carry 'i<k>' ids; ONLY real questions take 1..N, so the bank,
    the review PDF and the vetting PDF all number continuously from Q1.
    include: optional predicate over SECTIONS entries (edition filtering)."""
    out, bank, errs = [], [], []
    n = 0
    ninfo = 0

    def nxt():
        nonlocal n
        n += 1
        return str(n)

    for sec in mod.SECTIONS:
        if include and not include(sec):
            continue
        name = sec["name"]
        if name in getattr(mod, "INFO", {}):
            ninfo += 1
            out.append({"n": f"i{ninfo}", "type": "info", "section": name,
                        "title": name, "body": mod.INFO[name]})
        content = mod.CONTENT[name]
        if isinstance(content, dict):
            content = [content]
        if content and isinstance(content[0], dict) and content[0].get("type") in ("writing", "speaking"):
            for task in content:                            # one or more task items
                item = {"n": nxt(), "type": task["type"], "section": name}
                for k in ("stem", "intro", "body", "hint", "placeholder", "maxSeconds"):
                    if k in task:
                        item[k] = task[k]
                out.append(item)
            continue
        for i, q in enumerate(content, 1):                 # MCQs
            num = nxt()
            opts = q.get("options") or {k: "" for k in "ABCDE"}
            if q["correct"] not in opts:
                errs.append(f"q{num} ({name} #{i}): correct '{q['correct']}' not an option")
            item = {"n": num, "type": "mcq", "section": name, "qnum": str(i),
                    "stem": q["stem"], "options": opts,
                    "fig": q.get("fig", ""), "passage": q.get("passage", "")}
            if q.get("audio"):
                item["audio"] = q["audio"]
            out.append(item)
            bank.append({"test_id": test_id, "q": num, "type": "mcq", "category": name,
                         "strand": q["strand"], "concept_tested": q["concept"],
                         "correct": q["correct"], "marks": 1, "explanation": q["explanation"]})
    if group:
        out = group_listening(out, mod)
    return out, bank, errs


def nodash(s):
    """House rule: no em/en dashes in client-facing text (mirrors hs_paper.nodash)."""
    if not isinstance(s, str):
        return s
    s = re.sub(r"\s*——?\s*", " · ", s)
    s = re.sub(r"\s+–\s+", " · ", s)
    return s


_DISPLAY = ("stem", "title", "body", "intro", "hint", "placeholder", "passage")


_CJK = re.compile(r"[\u4e00-\u9fff]")
_EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\U0001F1E6-\U0001F1FF]")
_EMOJI_ONLY_SPAN = re.compile(r"<span[^>]*font-size[^>]*>(.*?)</span>", re.S)


def normalise_emoji(questions):
    """Give every emoji the same size, from one place.

    Level A leans on pictures, but the versions carried their own ad-hoc inline
    sizes: v1 wrapped its emoji in 46px/26px spans while v2 and v3 had no span
    at all and printed them at body size. Strip any span that wraps nothing but
    emoji and tag each emoji with .emo instead, so a single CSS rule sets the
    size on the page and in the vetting PDF alike.
    """
    def strip_span(m):
        inner = m.group(1)
        bare = _EMOJI.sub("", inner).replace("&nbsp;", "").strip()
        return inner if (not bare and _EMOJI.search(inner)) else m.group(0)

    def tag(text):
        s = _EMOJI_ONLY_SPAN.sub(strip_span, str(text))
        if not _EMOJI.search(s):
            return s
        out, parts = [], re.split(r"(<[^>]+>)", s)
        for chunk in parts:
            if chunk.startswith("<") or not _EMOJI.search(chunk):
                out.append(chunk)
            else:
                out.append(_EMOJI.sub(lambda m: f'<span class="emo">{m.group(0)}</span>', chunk))
        return "".join(out)

    for q in questions:
        for k in ("stem", "body", "intro", "hint"):
            if k in q and q[k]:
                q[k] = tag(q[k])
        if isinstance(q.get("options"), dict):
            q["options"] = {k: tag(v) for k, v in q["options"].items()}


def even_bilingual_options(questions):
    """Give every option in a bilingual question the same two-line shape.

    bilingual()/_bi() drop the Simplified line when it is identical to the
    Traditional (e.g. 漂亮), so in a question where the other options DO differ
    between scripts, that option is the only single-line one on the page. A
    child who spots the odd shape can pick it without reading any Chinese, and
    it lands on the key as often as not. Repeat the line instead: the column
    stays uniform and nothing is given away.
    """
    for q in questions:
        opts = q.get("options")
        if not isinstance(opts, dict):
            continue
        vals = [str(v) for v in opts.values() if str(v).strip()]
        if not vals or not any(_CJK.search(v) for v in vals):
            continue
        glossed = ["<br><i>" in v for v in vals]
        if not any(glossed) or all(glossed):
            continue
        q["options"] = {k: (v if ("<br><i>" in str(v) or not str(v).strip())
                            else f"{v}<br><i>{v}</i>")
                        for k, v in opts.items()}


def apply_house_text(questions, bank):
    even_bilingual_options(questions)
    normalise_emoji(questions)
    for q in questions:
        for k in _DISPLAY:
            if k in q:
                q[k] = nodash(q[k])
        if isinstance(q.get("options"), dict):
            q["options"] = {k: nodash(v) for k, v in q["options"].items()}
    for row in bank:
        row["explanation"] = nodash(row["explanation"])


def check_distribution(bank):
    per = {}
    for row in bank:
        per.setdefault(row["category"], []).append(row["correct"])
    print("  Answer-letter distribution:")
    for sec, letters in per.items():
        counts = {ch: letters.count(ch) for ch in "ABCDE" if letters.count(ch)}
        print(f"    {sec} ({len(letters)}): " + "  ".join(f"{k}={v}" for k, v in sorted(counts.items())))


def build_edition(mod, band, version, script_url, edition):
    """edition: 'en' (opt sections removed) or 'bilingual' (all sections core).
    The bilingual edition publishes under <band>-bilingual with its own bank."""
    if edition == "en":
        slug, label = band, mod.BAND_LABEL
        include = lambda sec: not sec.get("opt")
    else:
        slug, label = band + "-bilingual", mod.BAND_LABEL + " Bilingual"
        include = None
    test_id = f"BASELINE-{slug.upper()}-V{version}"
    questions, bank, errs = assemble(mod, test_id, include=include)
    if errs:
        print(f"BUILD ABORTED ({slug}):")
        for e in errs:
            print("  ERROR " + e)
        sys.exit(1)

    apply_house_text(questions, bank)
    page_json = json.dumps(questions, ensure_ascii=False)
    if '"correct"' in page_json or '"explanation"' in page_json:
        sys.exit(f"BUILD ABORTED ({slug}): answer-key field leaked into the page JSON")

    sections = [dict(sec) for sec in mod.SECTIONS if (include is None or include(sec))]
    for sec in sections:
        sec.pop("opt", None)
        sec.pop("chinese", None)
    total = sum(sec["minutes"] for sec in sections)
    title = f"HKS Baseline Assessment · {label} (V{version})"
    year_span = getattr(mod, "YEAR_SPAN", "")
    html = (open(TEMPLATE).read()
            .replace("{{TITLE}}", title)
            .replace("{{BAND_LABEL}}", label)
            .replace("{{YEAR_SPAN}}", year_span)
            .replace("{{BAND}}", slug)
            .replace("{{VERSION}}", str(version))
            .replace("{{SCRIPT_URL}}", script_url)
            .replace("{{YEARS}}", json.dumps(mod.YEARS, ensure_ascii=False))
            .replace("{{RECORD_MAX_S}}", str(getattr(mod, "RECORD_MAX_S", 120)))
            .replace("{{SECTIONS}}", json.dumps(sections, ensure_ascii=False))
            .replace("{{QUESTIONS}}", page_json))

    out_dir = os.path.join(PORTAL, "baseline-tests", slug, f"v{version}")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "index.html")
    open(dest, "w").write(html)

    bank_dir = os.path.join(BANKS, "baseline-tests", slug, f"v{version}")
    os.makedirs(bank_dir, exist_ok=True)
    bank_path = os.path.join(bank_dir, "bank.csv")
    with open(bank_path, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=["test_id", "q", "type", "category", "strand",
                                           "concept_tested", "correct", "marks", "explanation"])
        wr.writeheader()
        wr.writerows(bank)

    n_mcq = sum(len(q["items"]) if q["type"] == "lgroup" else (1 if q["type"] == "mcq" else 0)
                for q in questions)
    print(f"{slug} v{version}: {total} min · {n_mcq} MCQ · {dest}")
    check_distribution(bank)
    if script_url == PLACEHOLDER_URL:
        print("  NOTE: SCRIPT_URL is a placeholder; rebuild with --script-url before publishing.")


def build_band(band, version, script_url):
    mod = load_content(band, version)
    build_edition(mod, band, version, script_url, "en")
    if any(sec.get("opt") for sec in mod.SECTIONS):
        build_edition(mod, band, version, script_url, "bilingual")


CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def vet_band(band, version, out_dir):
    """Internal VETTING PDF: every question with figures + audio transcripts,
    then the full answer key with curriculum codes. Rendered via headless
    Chrome so emoji and embedded PNGs come out correctly."""
    import subprocess
    import tempfile
    mod = load_content(band, version)
    test_id = f"BASELINE-{band.upper()}-V{version}"
    questions, bank, errs = assemble(mod, test_id)
    if errs:
        sys.exit(f"VET ABORTED ({band}): " + "; ".join(errs))
    apply_house_text(questions, bank)
    key = {row["q"]: row for row in bank}
    css = """
      body{font-family:-apple-system,Arial,sans-serif;color:#1c2733;margin:34px 40px;font-size:13px;line-height:1.5}
      h1{color:#14213A;font-size:22px;margin:0 0 2px} .sub{color:#6b7280;margin:0 0 18px}
      h2{color:#14213A;font-size:16px;border-bottom:2px solid #72AFDB;padding-bottom:3px;margin:22px 0 10px;page-break-after:avoid}
      .q{margin:0 0 14px;padding:10px 12px;border:1px solid #dce3ea;border-radius:8px;page-break-inside:avoid}
      .qh{font-weight:700;color:#14213A;margin-bottom:4px}
      .stem{white-space:pre-line;margin:0 0 6px}
      .passage{background:#eef3f9;border:1px solid #dce3ea;border-radius:6px;padding:9px 11px;margin:6px 0;white-space:pre-line;font-size:12px}
      .opt{margin:2px 0 2px 14px} .opt b{display:inline-block;width:20px}
      .fig{margin:6px 0} .fig img,.fig svg{max-width:640px}
      .aud{color:#b7791f;font-size:12px;margin:4px 0}
      .meta{color:#6b7280;font-size:11px;margin-top:5px;font-style:italic}
      table{border-collapse:collapse;width:100%;font-size:12px}
      th{background:#14213A;color:#fff;text-align:left;padding:6px 9px}
      td{border:1px solid #dce3ea;padding:5px 9px;vertical-align:top}
      .ok{color:#1a7f37;font-weight:700}
      .pagebreak{page-break-before:always}
    """
    parts = [f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>",
             f"<h1>HKS Baseline Assessment · {mod.BAND_LABEL} (V{version}) · VETTING COPY</h1>",
             f"<p class='sub'>{getattr(mod, 'YEAR_SPAN', '')} · internal review copy, answer key at the end · not for distribution</p>"]
    cur = None
    for q in questions:
        if q["section"] != cur:
            cur = q["section"]
            mins = next((s["minutes"] for s in mod.SECTIONS if s["name"] == cur), "?")
            parts.append(f"<h2>{cur} · {mins} min</h2>")
        if q["type"] == "info":
            parts.append(f"<div class='q'><div class='qh'>Section instructions</div><div class='stem'>{q['body']}</div></div>")
            continue
        if q["type"] in ("writing", "speaking"):
            body = "<br><br>".join(x for x in (q.get("intro"), q.get("stem"), q.get("body"), q.get("hint")) if x)
            parts.append(f"<div class='q'><div class='qh'>{q['type'].title()} task</div><div class='stem'>{body}</div></div>")
            continue
        k = key[q["n"]]
        opts = "".join(f"<div class='opt'><b>{L})</b> {v if v else '<i style=color:#9aa6b4>(in figure)</i>'}</div>"
                       for L, v in q["options"].items())
        aud = f"<div class='aud'>AUDIO: {q['audio']}</div>" if q.get("audio") else ""
        psg = f"<div class='passage'>{q['passage']}</div>" if q.get("passage") else ""
        fig = f"<div class='fig'>{q['fig']}</div>" if q.get("fig") else ""
        parts.append(f"<div class='q'><div class='qh'>Q{q['n']} · {k['strand']}</div>"
                     f"{aud}{psg}<div class='stem'>{q['stem']}</div>{fig}{opts}"
                     f"<div class='meta'>{k['concept_tested']}</div></div>")
    parts.append("<div class='pagebreak'></div><h2>Answer key</h2><table><tr><th>Q</th><th>Key</th><th>Explanation</th><th>Curriculum code</th></tr>")
    for row in bank:
        parts.append(f"<tr><td>{row['q']}</td><td class='ok'>{row['correct']}</td>"
                     f"<td>{row['explanation']}</td><td>{row['concept_tested']}</td></tr>")
    parts.append("</table></body></html>")
    os.makedirs(out_dir, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write("".join(parts))
        tmp = f.name
    pdf = os.path.join(out_dir, f"Baseline_{mod.BAND_LABEL.replace(' ', '')}_V{version}_Vetting.pdf")
    subprocess.run([CHROME, "--headless", "--disable-gpu", f"--print-to-pdf={pdf}",
                    "--no-pdf-header-footer", "file://" + tmp],
                   check=True, capture_output=True)
    os.unlink(tmp)
    print(f"{band}: {pdf}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--band", choices=BANDS)
    b.add_argument("--all", action="store_true")
    b.add_argument("--version", default="1")
    b.add_argument("--script-url", default=PLACEHOLDER_URL)
    v = sub.add_parser("vet")
    v.add_argument("--band", choices=BANDS)
    v.add_argument("--all", action="store_true")
    v.add_argument("--version", default="1")
    v.add_argument("--out", default=os.path.expanduser("~/Desktop/Claude/Test-Prep/Baseline"))
    a = ap.parse_args()
    if a.cmd == "vet":
        import datetime
        out_dir = os.path.join(a.out, f"{datetime.date.today().isoformat()}_Vetting")
        for band in (BANDS if a.all else [a.band] if a.band else []):
            mod_path = os.path.join(HERE, "baseline", f"{band.replace('-', '_')}_v{a.version}.py")
            if os.path.exists(mod_path):
                vet_band(band, a.version, out_dir)
        return
    if not a.band and not a.all:
        sys.exit("Pass --band <band> or --all")
    for band in (BANDS if a.all else [a.band]):
        mod_path = os.path.join(HERE, "baseline", f"{band.replace('-', '_')}_v{a.version}.py")
        if a.all and not os.path.exists(mod_path):
            print(f"{band}: no content module yet, skipped")
            continue
        build_band(band, a.version, a.script_url)


if __name__ == "__main__":
    main()
