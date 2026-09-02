#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the SIS P4 Entrance online pages (prep-portal) + answer banks (test-banks).

Content source of truth: the testgen-singapore skill's content modules -- the same
modules that render the PDFs -- so page, paper and bank can never drift.  Hand-keying
a bank from a finished paper is what left five IDAT tests silently mis-grading
students for months; see _builder/BUILD_NOTES.md.

Usage:  python3 build_singapore.py [SCRIPT_URL]
        (omit SCRIPT_URL to leave the paste-me placeholder)

Emits one page per form per subject, under
singapore-tests/{english,math,chinese-sc,chinese-tc}/p4/mock-{n}/, plus one bank per
subject per mock: the SC and TC Chinese pages POST the same test id and share a bank
-- the answers are option numbers, identical in both scripts, so a single key makes
it impossible for the two to disagree.  The mock numbers come from the content
modules, so a new form appears here as soon as it is written.
"""
import csv
import html
import io
import os
import re
import sys

SKILL = os.path.expanduser("~/.claude/skills/testgen-singapore/engines")
sys.path.insert(0, SKILL)

import paperlib as P            # noqa: E402
import p4layout as L            # noqa: E402
import render_p4 as R           # noqa: E402
import content_en_p4 as EN      # noqa: E402
import content_ma_p4 as MA      # noqa: E402
import content_zh_p4 as ZH      # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PORTAL = os.path.dirname(HERE)
BANKS = os.path.expanduser("~/Developer/work/test-banks")
HOUSE = os.path.expanduser("~/.claude/skills/house-style/engine")
TEMPLATE = open(os.path.join(HERE, "templates", "singapore_test_page.html"),
                encoding="utf-8").read()
SCRIPT_URL = sys.argv[1] if len(sys.argv) > 1 else "PASTE_YOUR_APPS_SCRIPT_URL_HERE"

N4 = ["(1)", "(2)", "(3)", "(4)"]
NUM3 = ["①", "②", "③"]
NUM6 = ["①", "②", "③", "④", "⑤", "⑥"]
E = html.escape

MANUAL_EN = "This question is marked by hand, not online. Answer it as fully as you can."
MANUAL_ZH = "本題由老師人手批改，不計入網上分數。請盡量作答。"
# Working cannot be shown on a screen, so the online form does not pretend to
# collect it (Alex, 2026-08-31): a Section C question is worth 2 marks online for
# the correct answer, and nothing is left over to be marked by hand. The PRINTED
# paper still asks for working and still carries the full 4 marks.


# --------------------------------------------------------------- page assets
# The paper's figures are line art: every icon, dial and diagram is a stroked path
# with no fill.  house-style's paper.css carries that rule; without it the browser
# fills each path black and a dial becomes an unreadable disc.  Keep in step with
# ~/.claude/skills/house-style/engine/paper.css.
SVG_LINEART = """
  .q svg { stroke:#14213a; stroke-width:2.4; fill:none; stroke-linecap:round; stroke-linejoin:round; }
  .q svg text { stroke:none; fill:#1a2233; }
  .q .mathsvg { display:block; margin:14px 0 10px; }
"""


def page_assets():
    """The paper's own CSS + SVG icon defs, so printed figures render identically online."""
    css = open(os.path.join(SKILL, "css", "extra.css"), encoding="utf-8").read()
    icons = open(os.path.join(HOUSE, "icons.html"), encoding="utf-8").read()
    icons = re.sub(r"<!--.*?-->", "", icons, flags=re.S).strip()
    return css + SVG_LINEART, icons + P.defs_block()


def passage(inner, title=None):
    t = f'<div class="ptitle">{title}</div>' if title else ""
    return f'<div class="passage">{t}{inner}</div>'


def online_of(i):
    """The item as the online form asks it, or None if it is paper-only.

    A hand-marked item (a composition, a sentence to combine, a character to
    write) carries an `online` variant: the same construct asked as a choice.
    The paper still asks the candidate to write it.
    """
    return i.get("online")


def bank_row(test_id, i, note=""):
    """One answer-bank row, keyed to how the ONLINE form asks the item.

    Items with no online variant are still recorded, with auto=0, so the bank
    stays a complete description of the paper and the marker sees the model
    answer for anything left to mark by hand."""
    o = online_of(i)
    typ = o["type"] if o else i["type"]
    ans = o["ans"] if o else i["ans"]
    auto = 0 if typ == "manual" else 1
    return {
        "test_id": test_id,
        "q": str(i["q"]),
        "type": typ,
        "category": i["sec"],
        "strand": i["strand"],
        "concept_tested": i["concept"],
        "correct": ("ABCDEFGH"[ans] if typ == "mcq"
                    else ("" if ans is None else str(ans))),
        "marks": str(i["marks"]),
        "auto_marks": str(i["auto_marks"] if auto else 0),
        "auto": str(auto),
        "explanation": i["explanation"],
        "note": note,
    }


# --------------------------------------------------------------- ENGLISH
def english_page_sap(f):
    """Section-driven English page, for a form that carries its own spec.

    Sections that share a text are emitted as ONE screen, not one screen per
    question. Two things forced this: a cloze passage was being reprinted once per
    blank (ten times for Section E, fifteen for Section G), and a shared stimulus --
    the flyer, the vocabulary passage, the story -- was attached only to the FIRST
    question of its section, so the other seven, four and nine questions arrived with
    nothing to read and could not be answered at all.

    Cloze and editing sections put a dropdown at each blank, inside the passage.
    Stimulus sections list their questions under the text. Either way the answer is
    picked, never typed, and the bank still carries one row per question.
    """
    out, bank = [], []
    tid = f"SG-P4-M{f['n']}-EN"
    A, spec = f["assets"], f["spec"]
    INLINE = {"bankcloze", "compcloze", "editing"}

    def row(i, note=""):
        bank.append(bank_row(tid, i, note))

    for sec in spec["sections"]:
        items = R.qs(f, sec["from"], sec["to"])
        kind = sec["kind"]
        label = f'Section {sec["id"]}'

        if kind in INLINE:
            passage = "".join(R.chunks(
                A, sec, sec["from"], sec["to"],
                lambda n: f'<span class="blank" data-q="{n}"></span>'))
            lead = {"bankcloze": "Choose the word that fits each blank.",
                    "compcloze": "Choose the word that best fits each blank.",
                    "editing": "Each underlined word is wrong. Choose the correct "
                               "form at each numbered blank."}[kind]
            out.append({"label": str(sec["from"]), "section": label, "mode": "inline",
                        "stem": f'<div class="qtext">{lead}</div>'
                                f'<div class="passage">{passage}</div>',
                        "parts": [{"label": str(i["q"]),
                                   "options": online_of(i)["options"]} for i in items]})
            for i in items:
                row(i)
            continue

        if sec.get("stimulus"):
            out.append({"label": str(sec["from"]), "section": label, "mode": "list",
                        "stem": A[sec["stimulus"]],
                        "parts": [{"label": str(i["q"]),
                                   "stem": (online_of(i) or i)["stem"],
                                   "options": (online_of(i) or i)["options"],
                                   "labels": N4} for i in items]})
            for i in items:
                row(i)
            continue

        for i in items:
            o = online_of(i)
            src = o if o else i
            out.append({"label": str(i["q"]), "section": label,
                        "stem": f'<div class="qtext">{src["stem"]}</div>',
                        "options": src["options"], "labels": N4})
            row(i)
    return tid, out, bank


def english_page(f):
    A, out, bank = f["assets"], [], []
    tid = f"SG-P4-M{f['n']}-EN"

    def add(i, stem, **kw):
        q = {"label": str(i["q"]), "section": f'Section {i["sec"]}', "stem": stem}
        q.update(kw)
        out.append(q)
        bank.append(bank_row(tid, i, kw.get("note", "")))

    for i in R.qs(f, 1, 8):
        add(i, i["stem"], options=i["options"], labels=N4)
    syn = passage(A["synpass"])
    for i in R.qs(f, 9, 11):
        add(i, syn + '<div class="qtext">Which word is closest in meaning to '
                     f'{i["stem"]}?</div>', options=i["options"], labels=N4)
    poster = L.notice_box(*A["notice"])
    for i in R.qs(f, 12, 15):
        add(i, poster + f'<div class="qtext">{i["stem"]}</div>',
            options=i["options"], labels=N4)

    bank8 = ('<div class="qtext" style="font-weight:400">' +
             " &nbsp; ".join(f"<b>({ltr})</b> {w}"
                             for ltr, w in zip("ABCDEFGH", A["bank8"])) + "</div>")
    for i in R.qs(f, 16, 20):
        body = R.fill_blanks(A["cloze"], 16, 20, lambda k: f"<b>({k})</b> ______")
        o = online_of(i)
        add(i, passage(body) +
               f'<div class="qtext">Which word belongs in blank ({i["q"]})?</div>',
            options=o["options"], labels=[f"({c})" for c in "ABCDEFGH"])
    for i in R.qs(f, 21, 23):
        add(i, f'<div class="qtext">{i["stem"]}</div>'
               '<div class="qtext" style="font-weight:400">Write the underlined word '
               'correctly.</div>', input=True)
    for i in R.qs(f, 24, 27):
        body = R.fill_blanks(A["ccloze"], 24, 27, lambda k: f"<b>({k})</b> ______")
        add(i, passage(body) +
               f'<div class="qtext">Blank ({i["q"]}) — write one suitable word.</div>',
            input=True)
    for i in R.qs(f, 28, 29):
        o = online_of(i)
        add(i, f'<div class="qtext">{o["stem"]}</div>',
            options=o["options"], labels=N4)
    story = passage(A["hpass"])
    for i in R.qs(f, 30, 34):
        o = online_of(i)
        add(i, story + f'<div class="qtext">{o["stem"]}</div>',
            options=o["options"], labels=N4)
    return tid, out, bank


# --------------------------------------------------------------- MATHS
def maths_page(f):
    """Section-driven, like the paper renderer.

    Mock 4 is a 100-mark SAP-standard paper with 20/20/5 sections, so the old
    literal question ranges (1-12, 13-24, 25-28) would have silently emitted a
    12-question page for a 45-question paper.
    """
    out, bank = [], []
    tid = f"SG-P4-M{f['n']}-MA"
    spec = f.get("spec") or R.DEFAULT_MA_SPEC

    def add(i, stem, **kw):
        q = {"label": str(i["q"]), "section": f'Section {i["sec"]}', "stem": stem}
        q.update(kw)
        out.append(q)
        bank.append(bank_row(tid, i, kw.get("note", "")))

    def short_item(i):
        # An item may carry an `online` variant, exactly as the Chinese paper does:
        # the paper asks the child to write it out, the form asks the same construct
        # in a way a matcher can score. Without this the fraction-ordering item put
        # the paper's three answer blanks on screen next to one input box.
        o = online_of(i)
        if o:
            if o["type"] == "mcq":
                add(i, f'<div class="qtext">{o["stem"]}</div>',
                    options=o["options"], labels=N4)
            else:
                kw = {"input": True}
                if o.get("unit"):
                    kw["unit"] = o["unit"]
                if o.get("hint"):
                    kw["hint"] = o["hint"]
                if o.get("prefix"):
                    kw["prefix"] = o["prefix"]
                add(i, f'<div class="qtext">{o["stem"]}</div>', **kw)
            return
        r, raw = i["render"], i["render"]["raw"]
        kind = r["kind"]
        stem, hint, unit = "", None, None
        # a shared table/diagram introduces its group of questions
        pre = r.get("preamble", "")
        if kind in ("words", "riddle"):
            stem = f'<div class="qtext">{raw[1]}</div>'
            hint = "Write the number in words." if kind == "words" else None
        elif kind == "cards":
            stem = f'<div class="qtext">{raw[3]}</div>' + L.digit_cards(raw[1])
        elif kind == "colsum":
            top, bot, res = raw[1]
            stem = ('<div class="qtext">Write the missing digit.</div>'
                    + L.colsum(top, bot, res))
            hint = "One digit only."
        elif kind == "colop":
            top, bot, res, op = raw[1]
            stem = ('<div class="qtext">Write the missing digit.</div>'
                    + L.colop(top, bot, res, op))
            hint = "One digit only."
        elif kind == "order":
            stem = (f'<div class="qtext">Arrange the numbers from <b>{raw[2]}</b>.</div>'
                    f'<div class="qtext" style="font-weight:400">{raw[1]}</div>')
            hint = "Separate the three numbers with commas."
        elif kind == "plain":
            stem = f'<div class="qtext">{raw[1]}</div>'
        elif kind == "text":
            stem = f'<div class="qtext">{raw[1]}</div>'
            unit = raw[2] if raw[2] and raw[2] != "$" else None
        elif kind == "fig":
            _, figure, qtext, funit = raw[:4]
            stem = f'<div class="qtext">{qtext}</div>' + figure
            unit = funit if funit and funit != "$" else None
        elif kind == "dial":
            stem = (f'<div class="qtext">What is the mass of {raw[2]} shown on the '
                    f'scale?</div>' + L.dial(raw[1], raw[2]))
            unit = "g"
        elif kind == "fracq":
            lead = f'<div class="qtext">{raw[2]}</div>' if raw[2] else ""
            stem = lead + f'<div class="qtext">{raw[1]}</div>'
            hint = "Write the fraction as, for example, 3/4."
        elif kind == "graph":
            rows, icon, per, gunit, qtext, au, _a = raw[1:]
            stem = (f'<div class="qtext">{qtext}</div>'
                    + L.pgraph(rows, icon, per, gunit))
            unit = au
        kw = {"input": True}
        if hint:
            kw["hint"] = hint
        if unit:
            kw["unit"] = unit
        if i["type"] == "money":
            kw["prefix"] = "$"
        add(i, pre + stem, **kw)

    for sec in spec["sections"]:
        for i in R.qs(f, sec["from"], sec["to"]):
            if sec["kind"] == "mcq":
                add(i, f'<div class="qtext">{i["stem"]}</div>',
                    options=i["options"], labels=N4)
            elif sec["kind"] == "short":
                short_item(i)
            else:
                kw = {"input": True}
                r = i["render"]
                o = online_of(i)
                stem = o["stem"] if o else i["stem"]
                unit = (o.get("unit") if o else None) or r["unit"]
                if unit == "$":
                    kw["prefix"] = "$"
                elif unit:
                    kw["unit"] = unit
                add(i, f'<div class="qtext">{stem}</div>{r.get("figure", "")}', **kw)
    return tid, out, bank


# --------------------------------------------------------------- CHINESE
def chinese_page(f, script):
    """Every section reaches the online form, but nothing is typed in Chinese.

    注音 / 写字 / 组词成句 / 阅读作答 are asked as choices (each item's `online`
    variant) rather than dropped: an IME on a shared laptop is a worse test than a
    pencil, but a child can still show whether they know which character, which
    pinyin and which word order is right.
    """
    is_tc = script == "tc"
    if is_tc:
        f = {"n": f["n"], "assets": R.tc(f["assets"]), "items": R.tc(f["items"])}
    A, out, bank = f["assets"], [], []
    tid = f"SG-P4-M{f['n']}-ZH"          # one bank for both scripts
    X = R.to_traditional if is_tc else (lambda s: s)

    def add(i, stem, **kw):
        q = {"label": str(i["q"]), "section": X("第") + i["sec"] + X("题"), "stem": stem}
        q.update(kw)
        out.append(q)
        bank.append(bank_row(tid, i, kw.get("note", "")))

    def labels_for(o):
        return NUM6[:len(o["options"])] if len(o["options"]) > 3 else NUM3

    # 一 选择音节
    for i in R.qs(f, 1, 4):
        add(i, f'<div class="qtext">{i["stem"]}</div>'
               f'<div class="qtext" style="font-weight:400">{X("圈出画线字的正确读音。")}</div>',
            options=i["options"], labels=NUM3)
    # 二 给汉字注音 -> choose the pinyin
    # 三 填写汉字   -> choose the character
    for i in R.qs(f, 5, 10):
        o = online_of(i)
        add(i, f'<div class="qtext">{o["stem"]}</div>',
            options=o["options"], labels=labels_for(o))
    # 四 辨字测验
    for i in R.qs(f, 11, 14):
        clean = re.sub(r"（[^）]+）", "（　　）", i["render"]["paper_stem"])
        add(i, f'<div class="qtext">{clean}</div>'
               f'<div class="qtext" style="font-weight:400">{X("选出正确的汉字。")}</div>',
            options=i["options"], labels=NUM3)
    # 五 词语搭配
    for i in R.qs(f, 15, 18):
        stem = i["render"]["paper_stem"].replace("#", "（　　）")
        add(i, f'<div class="qtext">{stem}</div>'
               f'<div class="qtext" style="font-weight:400">{X("选出正确的词语。")}</div>',
            options=i["options"], labels=NUM6)
    # 六 组词成句 -> choose the correctly ordered sentence
    for i in R.qs(f, 19, 21):
        o = online_of(i)
        chips = " &nbsp;·&nbsp; ".join(i["render"]["chips"])
        add(i, f'<div class="qtext" style="font-weight:400">{chips}</div>'
               f'<div class="qtext">{o["stem"]}</div>',
            options=o["options"], labels=labels_for(o))
    # 七 短文填空
    body = R.fill_blanks(A["S7"], 22, 25, lambda k: f"<b>（{k}）</b>（　　）")
    for i in R.qs(f, 22, 25):
        add(i, passage(body) +
               f'<div class="qtext">{X("第")}（{i["q"]}）{X("空 — 选出正确的词语。")}</div>',
            options=i["options"], labels=NUM6[:len(i["options"])])
    # 八 阅读理解 -- the MCQs as printed, the written questions as choices
    story = passage(A["S8"])
    for i in R.qs(f, 26, 27):
        add(i, story + f'<div class="qtext">{i["stem"]}</div>',
            options=i["options"], labels=NUM3)
    for i in R.qs(f, 28, 29):
        o = online_of(i)
        add(i, story + f'<div class="qtext">{o["stem"]}</div>',
            options=o["options"], labels=labels_for(o))
    return tid, out, bank


# --------------------------------------------------------------- UI strings
UI_EN = {
    "qcount": "Question {n} of {t}", "next": "Next →", "submit": "Submit test",
    "saved": "Auto-saved", "needName": "Please enter the student name first.",
    "needEmail": "Please enter a valid email address — it is required.",
    "typeAnswer": "Type your answer",
}
UI_ZH_SC = {
    "qcount": "第 {n} 题，共 {t} 题", "next": "下一题 →", "submit": "提交试卷",
    "saved": "已自动保存", "needName": "请先输入学生姓名。",
    "needEmail": "请输入有效的电邮地址（必填）。",
    "typeAnswer": "输入答案",
}
UI_ZH_TC = {
    "qcount": "第 {n} 題，共 {t} 題", "next": "下一題 →", "submit": "提交試卷",
    "saved": "已自動儲存", "needName": "請先輸入學生姓名。",
    "needEmail": "請輸入有效的電郵地址（必填）。",
    "typeAnswer": "輸入答案",
}
CHROME_EN = {
    "__LANG__": "en", "__UI_BEFORE__": "Before you begin",
    "__UI_NAME__": "Student name (required)", "__UI_EMAIL__": "Email (required)",
    "__UI_NAMEPH__": "Full name", "__UI_START__": "Start test →",
    "__UI_HOWTO__": ("Some questions are multiple choice; for others, type your answer in "
                     "the box. Answering each question is optional — press <b>Next</b> to "
                     "skip. Once you press <b>Next</b> you cannot return to a previous "
                     "question."),
    "__UI_DONE__": "Submission received ✔",
    "__UI_DONEMSG__": ("Thank you for taking the test. Your results have been sent to "
                       "HK-Schools.com for review. We will be in contact shortly."),
    "__UI_CLOSE__": "You may now close this page.",
}
CHROME_SC = {
    "__LANG__": "zh-Hans", "__UI_BEFORE__": "作答前请阅读", "__UI_NAME__": "学生姓名（必填）",
    "__UI_EMAIL__": "电邮地址（必填）", "__UI_NAMEPH__": "姓名", "__UI_START__": "开始作答 →",
    "__UI_HOWTO__": ("本网上试卷全部是选择题。按<b>下一题</b>继续；一旦进入下一题便不能返回。"
                     "纸本试卷仍会要求你亲手写出拼音、汉字和句子。"),
    "__UI_DONE__": "已收到你的答卷 ✔",
    "__UI_DONEMSG__": "多谢作答。成绩已发送给 HK-Schools.com，我们会尽快与你联络。",
    "__UI_CLOSE__": "你现在可以关闭这个页面。",
}
CHROME_TC = {k: (R.to_traditional(v) if k.startswith("__UI_") else v)
             for k, v in CHROME_SC.items()}
CHROME_TC["__LANG__"] = "zh-Hant"


# --------------------------------------------------------------- emit
def render_page(path, title, short, countline, tid, questions, ui, chrome):
    css, defs = page_assets()
    s = TEMPLATE
    for k, v in chrome.items():
        s = s.replace(k, v)
    s = (s.replace("__TITLE__", E(title)).replace("__SHORTTITLE__", E(short))
          .replace("__COUNTLINE__", E(countline)).replace("__TESTID__", tid)
          .replace("__SCRIPT_URL__", SCRIPT_URL))
    s = s.replace("</style>", css + "\n</style>")
    s = s.replace("<body>", "<body>\n" + defs)
    s = s.replace("/*__UI_JSON__*/{}", _json(ui))
    s = s.replace("/*__QUESTIONS_JSON__*/[]", _json(questions))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(s)

    assert s.count('<div id="gate">') == 0, "gate flash: bare #gate div"
    assert s.count('id="gate" style="display:none"') == 1, "gate must ship hidden"
    return path


def _json(o):
    import json
    return json.dumps(o, ensure_ascii=False)


BANK_COLS = ["test_id", "q", "type", "category", "strand", "concept_tested",
             "correct", "marks", "auto_marks", "auto", "explanation", "note"]


def write_bank(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=BANK_COLS, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)
    open(path, "w", encoding="utf-8").write(buf.getvalue())


SPECS = []
for _f in EN.FORMS:
    SPECS.append(("english", _f["n"], "EN",
                  english_page_sap if _f.get("spec") else english_page,
                  (_f,), UI_EN, CHROME_EN,
                  f"SIS P4 Entrance · English · Mock {_f['n']}", "English"))
for _f in MA.FORMS:
    SPECS.append(("math", _f["n"], "MA", maths_page, (_f,), UI_EN, CHROME_EN,
                  f"SIS P4 Entrance · Mathematics · Mock {_f['n']}", "Mathematics"))
for _f in ZH.FORMS:
    SPECS.append(("chinese-sc", _f["n"], "ZH", chinese_page, (_f, "sc"), UI_ZH_SC, CHROME_SC,
                  f"新加坡国际学校 小四入学评估 · 中文（简体）· 模拟试卷 {_f['n']}", "中文"))
    SPECS.append(("chinese-tc", _f["n"], "ZH", chinese_page, (_f, "tc"), UI_ZH_TC, CHROME_TC,
                  f"新加坡國際學校 小四入學評估 · 中文（繁體）· 模擬試卷 {_f['n']}", "中文"))


def main():
    banks = {}
    for slug, n, code, fn, args, ui, chrome, title, short in SPECS:
        tid, questions, bank = fn(*args)
        auto = sum(int(r["auto_marks"]) for r in bank if r["auto"] == "1")
        # The denominator is the WHOLE paper, not just what reached the page.  The
        # Chinese page carries only the selection items, so counting the bank would
        # advertise "20 of 20" for a 38-mark paper.
        # Per FORM, not per module: Mock 4 maths is a 100-mark paper while Mocks 1-3
        # are 64-mark papers, and a module-level total would mis-state both.
        form = next(x for x in {"EN": EN, "MA": MA, "ZH": ZH}[code].FORMS
                    if x["n"] == n)
        tot = form.get("total", {"EN": EN, "MA": MA, "ZH": ZH}[code].TOTAL_MARKS)
        if chrome is CHROME_EN:
            countline = f"{len(questions)} questions · {auto} marks"
        else:
            countline = f"共 {len(questions)} 题 · 满分 {auto} 分"
        if chrome is CHROME_TC:
            countline = R.to_traditional(countline)
        pchrome = dict(chrome)
        page = os.path.join(PORTAL, "singapore-tests", slug, "p4", f"mock-{n}", "index.html")
        render_page(page, title, short, countline, tid, questions, ui, pchrome)
        print(f"  page {os.path.relpath(page, PORTAL)}  ({len(questions)} q, {auto} marks)")
        banks.setdefault((slug.split("-")[0], n, tid), bank)

    for (subject, n, tid), bank in banks.items():
        path = os.path.join(BANKS, "singapore-tests", subject, "p4", f"mock-{n}", "bank.csv")
        write_bank(path, bank)
        print(f"  bank {os.path.relpath(path, BANKS)}  ({len(bank)} rows, id {tid})")


if __name__ == "__main__":
    main()
