#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the 6 CEM online test pages (prep-portal) + 6 answer banks (test-banks).

Content source of truth: the testgen-cem skill engines (same modules that build
the docx papers, so page and paper can never drift).

Usage:  python3 build_cem.py [SCRIPT_URL]
        (omit SCRIPT_URL to leave the paste-me placeholder)
"""
import base64, csv, html, json, os, sys, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
PORTAL = os.path.dirname(HERE)
BANKS = os.path.expanduser("~/Developer/work/test-banks")
ENGINES = os.path.expanduser("~/.claude/skills/testgen-cem/engines")
sys.path.insert(0, ENGINES)

SCRIPT_URL = sys.argv[1] if len(sys.argv) > 1 else "PASTE_YOUR_APPS_SCRIPT_URL_HERE"
TEMPLATE = open(os.path.join(HERE, "templates", "cem_test_page.html"), encoding="utf-8").read()

E = html.escape


# ------------------------------------------------------------- helpers
def img_tag(figdir, key):
    path = os.path.join(figdir, key + ".png")
    data = base64.b64encode(open(path, "rb").read()).decode()
    from PIL import Image
    w = Image.open(path).width // 3          # rendered at 3x
    return f'<img src="data:image/png;base64,{data}" width="{w}" alt="figure">'


def table_html(spec):
    if "caption" in spec:                     # pictogram
        rows = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in spec["rows"])
        return (f'<table class="dt">{rows}</table>'
                f'<div class="tcap">{E(spec["caption"])}</div>')
    head = "".join(f"<th>{E(h)}</th>" for h in spec["header"])
    body = "".join("<tr>" + "".join(f"<td>{E(c)}</td>" for c in row) + "</tr>"
                   for row in spec["rows"])
    return f'<table class="dt"><tr>{head}</tr>{body}</table>'


def pattern_html(word, given):
    cells = [word[i].upper() if i in given else "_" for i in range(len(word))]
    return '<div class="pattern">' + E(" ".join(cells)) + "</div>"


def passage_html(title, lines):
    out = [f'<div class="passage"><div class="ptitle">{E(title)}</div>']
    for i, line in enumerate(lines):
        n = str(i + 1) if (i + 1) % 5 == 0 else ""
        out.append(f'<div class="pl"><span class="ln">{n}</span><span>{E(line)}</span></div>')
    out.append("</div>")
    return "".join(out)


def qtext(t):
    return '<div class="qtext">' + E(str(t)).replace("\n", "<br>") + "</div>"


# ------------------------------------------------------------- English
def build_english(EN, mock):
    qs, bank = [], []
    n = 0

    def add(section, stem, *, opts=None, ans=None, inp=None, hint=None,
            btype=None, correct=None, concept="", expl="", qplain=""):
        nonlocal n
        n += 1
        label = str(n)
        q = dict(label=label, section=section, stem=stem)
        if opts is not None:
            q["options"] = opts
            qplain += "   " + "   ".join(f"{'ABCD'[i]} {o}" for i, o in enumerate(opts))
        else:
            q["input"] = True
            if hint: q["hint"] = hint
        qs.append(q)
        bank.append(dict(q=label, type=btype, category=section, strand=section,
                         concept_tested=concept, correct=correct, marks=1,
                         explanation=expl, question=qplain))

    p1 = passage_html(EN.P1_TITLE, EN.P1_LINES)
    for it in EN.P1_QUESTIONS:
        add("Part 1 · Comprehension", p1 + qtext(it["q"]), opts=it["opts"],
            qplain=f"[{EN.P1_TITLE}] " + it["q"],
            btype="mcq", correct="ABCD"[it["ans"]], concept="Reading comprehension",
            expl=it["opts"][it["ans"]])
    p2 = passage_html(EN.P2_TITLE, EN.P2_LINES)
    for it in EN.P2_QUESTIONS:
        add("Part 2 · Comprehension", p2 + qtext(it["q"]), opts=it["opts"],
            qplain=f"[{EN.P2_TITLE}] " + it["q"],
            btype="mcq", correct="ABCD"[it["ans"]], concept="Reading comprehension",
            expl=it["opts"][it["ans"]])
    for it in EN.P3_ITEMS:
        stem = (qtext("Complete the word so the sentence makes sense.  "
                      "Type the COMPLETE word.")
                + '<div class="qtext" style="font-weight:400">'
                + E(it["before"]) + " " + "&hellip; " + E(it["after"]) + "</div>"
                + pattern_html(it["word"], it["given"]))
        pat = " ".join(it["word"][i].upper() if i in it["given"] else "_"
                       for i in range(len(it["word"])))
        add("Part 3 · Complete the Words", stem, inp=True,
            qplain=f"Complete the word: {it['before']} … {it['after']}   [{pat}]",
            hint=f"Type the complete word ({len(it['word'])} letters).",
            btype="word", correct=it["word"], concept="Partial-words cloze",
            expl=it["word"])
    for it in EN.P4_ITEMS:
        stem = qtext("Choose the word that has a similar meaning to the words "
                     "in BOTH sets of brackets.") + \
               '<div class="pattern">(' + E(it["b1"]) + ")&nbsp;&nbsp;&nbsp;(" + E(it["b2"]) + ")</div>"
        add("Part 4 · Matching Words", stem, opts=it["opts"],
            qplain=f"Word fitting both ({it['b1']}) and ({it['b2']})",
            btype="mcq", correct="ABCD"[it["ans"]], concept="Double-bracket synonyms",
            expl=f"{it['opts'][it['ans']]} fits both ({it['b1']}) and ({it['b2']}).")
    for it in EN.P5_ITEMS:
        stem = qtext("Complete the word so that it means the OPPOSITE, or nearly "
                     "the opposite, of:") + \
               '<div class="pattern" style="letter-spacing:1px">' + E(it["prompt"]) + "</div>" + \
               pattern_html(it["word"], it["given"])
        pat = " ".join(it["word"][i].upper() if i in it["given"] else "_"
                       for i in range(len(it["word"])))
        add("Part 5 · Opposite Words", stem, inp=True,
            qplain=f"Opposite of '{it['prompt']}'   [{pat}]",
            hint=f"Type the complete word ({len(it['word'])} letters).",
            btype="word", correct=it["word"], concept="Antonym completion",
            expl=f"{it['word']} (opposite of {it['prompt']})")
    for it in EN.P6_ITEMS:
        stem = qtext("Choose the word that means the same, or nearly the same, as:") + \
               '<div class="pattern" style="letter-spacing:1px">' + E(it["prompt"]) + "</div>"
        add("Part 6 · Similar Words", stem, opts=it["opts"],
            qplain=f"Word meaning the same as '{it['prompt']}'",
            btype="mcq", correct="ABCD"[it["ans"]], concept="Synonym MCQ",
            expl=it["opts"][it["ans"]])
    return qs, bank


# ------------------------------------------------------------- Maths
# free-text alternates per (mock, label)
TEXT_ALTS = {
    (1, "B32"): "Envelopes",
    (1, "B36"): "1 hour|60 minutes|60 min|1 hr|one hour|1h",
    (1, "B40"): "Shop B|B",
    (2, "B32"): "Lychees",
    (2, "B40"): "Shop B|B",
    (3, "B32"): "Robots",
    (3, "B36"): "1 hour 10 minutes|70 minutes|70 min|1h10|1 hr 10 min|1 hour 10 min",
    (3, "B40"): "Shop B|B",
}


def classify_write(item, mock, label):
    key = str(item["key"])
    if item.get("ratio"):
        return "ratio", key.replace(" ", "")
    if any(c.isalpha() for c in key) or item.get("free") or item.get("boxes") == 0:
        alts = TEXT_ALTS.get((mock, label), key)
        return "text", alts
    if ":" in key:
        return "time", key
    if item.get("prefix") == "£":
        return "money", key
    return "num", key.replace(" ", "")


def build_maths(MA, figdir, mock):
    qs, bank = [], []

    # Shared context per cluster: every question in a cluster repeats the
    # cluster's intro + table + figure, because the online format shows one
    # question per screen with no way to look back.
    def cluster_context(items):
        ctx = {}
        for item in items:
            cl = item.get("cluster")
            if not cl:
                continue
            c = ctx.setdefault(cl, {"intro": None, "table": None, "fig": None})
            if item.get("intro") and not c["intro"]:
                c["intro"] = item["intro"]
            if item.get("table") and not c["table"]:
                c["table"] = item["table"]
            if item.get("fig") and not c["fig"]:
                c["fig"] = item["fig"]
        return ctx

    CTX = cluster_context(MA.SECTION_A + MA.SECTION_B)

    def add(sec_label, label, item):
        stem = ""
        cl = item.get("cluster")
        if cl:
            c = CTX[cl]
            if c["intro"]:
                stem += '<div class="intro">' + E(c["intro"]) + "</div>"
            if c["table"]:
                stem += table_html(MA.TABLES[c["table"]])
            if c["fig"]:
                stem += img_tag(figdir, c["fig"])
            stem += qtext(item["q"])
        else:
            if item.get("intro"):
                stem += '<div class="intro">' + E(item["intro"]) + "</div>"
            stem += qtext(item["q"])
            if item.get("table"):
                stem += table_html(MA.TABLES[item["table"]])
            if item.get("fig"):
                stem += img_tag(figdir, item["fig"])
        q = dict(label=label, section=sec_label, stem=stem)
        if item["kind"] == "mcq":
            q["options"] = list(item["opts"])
            btype, correct = "mcq", "ABCDE"[item["ans"]]
            hint = None
        else:
            q["input"] = True
            if item.get("prefix"): q["prefix"] = item["prefix"]
            if item.get("unit"):   q["unit"] = item["unit"]
            btype, correct = classify_write(item, mock, label)
            hint = {"time": "Write as a time with a colon, e.g. 9:30",
                    "ratio": "Write as a ratio, e.g. 5:4",
                    "money": "Numbers only, e.g. 12.50",
                    "num": "Numbers only",
                    "text": "Short answer"}[btype]
            q["hint"] = hint
        qs.append(q)
        qplain = ""
        _intro = (CTX[cl]["intro"] if cl else item.get("intro"))
        _table = (CTX[cl]["table"] if cl else item.get("table"))
        _fig   = (CTX[cl]["fig"] if cl else item.get("fig"))
        if _intro:
            qplain += _intro + "  "
        qplain += str(item["q"]).replace("\n", "  ")
        if _table:
            spec = MA.TABLES[_table]
            if "caption" in spec:
                qplain += "  [" + "; ".join(f"{a}: {b}" for a, b in spec["rows"]) + \
                          f" — {spec['caption']}]"
            else:
                qplain += "  [" + " | ".join(spec["header"]) + " ;; " + \
                          " ;; ".join(" | ".join(r) for r in spec["rows"]) + "]"
        if _fig:
            qplain += "  [see diagram in the online test]"
        if item["kind"] == "mcq":
            qplain += "   " + "   ".join(f"{'ABCDE'[i]} {o}" for i, o in enumerate(item["opts"]))
        bank.append(dict(q=label, type=btype, category=q["section"],
                         strand=q["section"], concept_tested="",
                         correct=correct, marks=1, explanation=item["work"],
                         question=qplain))

    for i, item in enumerate(MA.SECTION_A, 1):
        add("Section A · Quick Maths", f"A{i}", item)
    for i, item in enumerate(MA.SECTION_B, 1):
        add("Section B · Long Maths", f"B{i}", item)
    return qs, bank


# ------------------------------------------------------------- emit
def emit(qs, bank, test_id, title, shorttitle, countline, outdir, bankdir):
    page = (TEMPLATE
            .replace("__TITLE__", E(title))
            .replace("__SHORTTITLE__", E(shorttitle))
            .replace("__COUNTLINE__", E(countline))
            .replace("__TESTID__", test_id)
            .replace("__SCRIPT_URL__", SCRIPT_URL)
            .replace("/*__QUESTIONS_JSON__*/[]", json.dumps(qs, ensure_ascii=False)))
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "index.html"), "w", encoding="utf-8").write(page)
    os.makedirs(bankdir, exist_ok=True)
    with open(os.path.join(bankdir, "bank.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["test_id", "q", "type", "category", "strand", "concept_tested",
                    "correct", "marks", "explanation", "question"])
        for r in bank:
            w.writerow([test_id, r["q"], r["type"], r["category"], r["strand"],
                        r["concept_tested"], r["correct"], r["marks"], r["explanation"],
                        r["question"]])
    # self-checks (BUILD_NOTES rules)
    assert page.count('<div id="gate">') == 0
    assert page.count('id="gate" style="display:none"') == 1
    print(f"built {test_id}: {len(qs)} questions -> {outdir}")


def main():
    for mock in (1, 2, 3):
        suf = "" if mock == 1 else f"_v{mock}"
        EN = importlib.import_module(f"content_english{suf}")
        MA = importlib.import_module(f"content_maths{suf}")
        figdir = os.path.join(ENGINES, "figs" if mock == 1 else f"figs_v{mock}")

        qs, bank = build_english(EN, mock)
        emit(qs, bank, f"CEM-Y7-M{mock}-EN",
             f"CEM Practice Test — YCIS Year 7 Entry · Mock {mock} · English (Paper 1)",
             f"CEM Y7 Mock {mock} English",
             "80 questions · 6 parts · about 50 minutes · one question per screen.",
             os.path.join(PORTAL, "cem-tests", f"mock{mock}", "english"),
             os.path.join(BANKS, "cem-tests", f"mock{mock}", "english"))

        qs, bank = build_maths(MA, figdir, mock)
        emit(qs, bank, f"CEM-Y7-M{mock}-MA",
             f"CEM Practice Test — YCIS Year 7 Entry · Mock {mock} · Maths (Paper 2)",
             f"CEM Y7 Mock {mock} Maths",
             "75 questions · 2 sections · about 53 minutes · one question per screen.",
             os.path.join(PORTAL, "cem-tests", f"mock{mock}", "maths"),
             os.path.join(BANKS, "cem-tests", f"mock{mock}", "maths"))


if __name__ == "__main__":
    main()
