#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Online test pages for the Singapore K2-S2 MC suite (prep-portal).

Called by build_mc_suite.py, which emits the answer banks from the SAME content
modules:

    python3 build_mc_suite.py --banks --pages [SCRIPT_URL]
    python3 build_mc_pages.py [SCRIPT_URL]          # pages only

One page per test, at
singapore-tests/mc/{english,math,chinese-sc,chinese-tc}/<level>/test-<n>/,
9 levels x 3 forms x (English + Mathematics + Chinese SC + Chinese TC) = 108.

The suite is 100% MCQ: nothing is typed, nothing is marked by hand, and the
online score IS the paper total.

THE ONE INVARIANT.  Options are rendered in the content module's own order and
the page posts A/B/C/D BY POSITION; the bank's key is the correct option's
INDEX ("ABCD"[ans]).  Never sort, shuffle or dedupe `i["options"]` here -- do
that and every test in the suite mis-grades, silently.  check_mc_pages.py
audits exactly this.

The 简体 and 繁體 pages POST THE SAME test id (SG-<L>-T<n>-ZH) and share one
bank: the answers are option numbers, identical in both scripts.  The TC
edition converts DATA through render_p4.tc / to_traditional, the way
mc/render.py does for the printed paper.
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# The banks builder owns the content-module list, the subject map and the test
# ids.  Importing it (rather than re-deriving any of that) is what makes it
# impossible for a page to be built for a test id the bank does not use.  It
# writes nothing on import.
import build_mc_suite as S                                       # noqa: E402

SKILL = os.path.expanduser("~/.claude/skills/testgen-singapore/engines")
HOUSE = os.path.expanduser("~/.claude/skills/house-style/engine")
sys.path.insert(0, SKILL)
import render_p4 as R                                            # noqa: E402
import paperlib as P                                             # noqa: E402

PORTAL = os.path.dirname(HERE)
TEMPLATE = open(os.path.join(HERE, "templates", "singapore_test_page.html"),
                encoding="utf-8").read()

N4 = ["(1)", "(2)", "(3)", "(4)"]      # English / Mathematics
NUM4 = ["①", "②", "③", "④"]           # Chinese, as the printed paper numbers them
CN = "一二三四五六七八"
E = html.escape


# --------------------------------------------------------------- page assets
# The suite's figures are line art: icons, dials, shapes and graphs are stroked
# paths carrying no fill of their own.  house-style's paper.css supplies that
# rule for the PDF; without the same rule here the browser fills every path
# black and a clock face becomes a disc.  Kept in step with build_singapore.py
# (which is where this came from) and with house-style/engine/paper.css.
SVG_LINEART = """
  .q svg { stroke:#14213a; stroke-width:2.4; fill:none; stroke-linecap:round; stroke-linejoin:round; }
  .q svg text { stroke:none; fill:#1a2233; }
  .q .mathsvg { display:block; margin:14px 0 10px; }
  /* extra.css (print) restyles .passage as a bare left rule sized in mm.  The
     MC suite's passages are long -- a P6 comprehension text runs 700 words --
     so the screen keeps the template's boxed, scrollable panel. */
  .q .passage { background:#f7faff; border:1px solid #e2ebf7; border-left:4px solid var(--blue);
                border-radius:10px; padding:14px 20px; margin:0 0 20px; max-height:340px;
                overflow:auto; font-size:1rem; font-weight:400; line-height:1.6; color:var(--ink); }
"""


def page_assets():
    """The paper's own CSS + SVG icon defs, so figures render as they print."""
    css = open(os.path.join(SKILL, "css", "extra.css"), encoding="utf-8").read()
    icons = open(os.path.join(HOUSE, "icons.html"), encoding="utf-8").read()
    icons = re.sub(r"<!--.*?-->", "", icons, flags=re.S).strip()
    return css + SVG_LINEART, icons + P.defs_block()


# --------------------------------------------------------------- rubrics
# The printed rubric tells the candidate to CIRCLE a number.  On screen there is
# nothing to circle, so the same sentence is restated for the medium.  Only the
# instruction to circle changes: what to read, what to choose and how many marks
# it carries are the paper's own words, untouched.
EN_FIX = [
    (re.compile(r"[,]? then circle the number of your answer", re.I), ""),
    (re.compile(r"[,]? then circle its number", re.I), ""),
    (re.compile(r" and circle its number", re.I), ""),
    (re.compile(r"\s*Circle its number\.", re.I), ""),
    (re.compile(r"Circle the number of", re.I),
     lambda m: "Choose" if m.group(0)[0] == "C" else "choose"),
]
# Chinese, longest phrase first (圈出正确答案的号码 must not be reached by the
# bare 圈出 rule).  Written in 简体 and converted for the 繁體 edition, so one
# table serves both scripts.
ZH_FIX = [("圈出正确答案的号码", "选出正确的答案"),
          ("，圈出号码", ""),
          ("圈出", "选出")]


def online_rubric(text, zh, X):
    if zh:
        for a, b in ZH_FIX:
            text = text.replace(X(a), X(b))
        return text
    for pat, rep in EN_FIX:
        text = pat.sub(rep, text)
    return re.sub(r"\s{2,}", " ", text).strip()


# --------------------------------------------------------------- questions
def stem_of(i):
    """Stem + figure, the figure a BLOCK under the text.

    A tall inline svg drops the stem to the bottom of its line box and the
    picture reads first; mc/render.py wraps figures for the same reason, and
    already-wrapped figures are left alone."""
    fig = i["fig"] or ""
    if fig and not fig.startswith('<span style="display:block"'):
        fig = f'<span style="display:block">{fig}</span>'
    return str(i["stem"]) + fig


def questions_for(form, zh, X):
    """The page's QUESTIONS array: one screen per item, one screen per
    stimulus section.

    A section that shares a text -- a passage, a flyer, a comment thread, a
    matchstick pattern -- is emitted as ONE screen carrying the text once and
    all of its questions under it.  Per-question screens would either reprint
    the text a dozen times or (the bug the P4 pages were built to fix) attach
    it to the first question only and leave the rest unanswerable.
    """
    labels = NUM4 if zh else N4
    out = []
    for s in form["sections"]:
        sid = s["id"]
        badge = (f'{X("第")}{sid}{X("部分")} · {s["name"]}' if zh
                 else f'Section {sid} · {s["name"]}')
        items = s["items"]
        if s.get("stimulus"):
            lead = online_rubric(s["rubric"], zh, X)
            out.append({
                "label": str(items[0]["q"]),
                "section": badge,
                "mode": "list",
                "stem": f'<div class="qtext">{lead}</div>{s["stimulus"]}',
                "parts": [{"label": str(i["q"]), "stem": stem_of(i),
                           "options": list(i["options"]), "labels": labels}
                          for i in items],
            })
            continue
        for i in items:
            out.append({"label": str(i["q"]), "section": badge,
                        "stem": f'<div class="qtext">{stem_of(i)}</div>',
                        "options": list(i["options"]), "labels": labels})
    return out


# --------------------------------------------------------------- UI strings
UI_EN = {"qcount": "Question {n} of {t}", "next": "Next →",
         "submit": "Submit test", "saved": "Auto-saved",
         "needName": "Please enter the student name first.",
         "needEmail": "Please enter a valid email address — it is required.",
         "typeAnswer": "Type your answer"}
UI_SC = {"qcount": "第 {n} 题，共 {t} 题", "next": "下一题 →", "submit": "提交试卷",
         "saved": "已自动保存", "needName": "请先输入学生姓名。",
         "needEmail": "请输入有效的电邮地址（必填）。", "typeAnswer": "输入答案"}
UI_TC = {k: R.to_traditional(v) for k, v in UI_SC.items()}

CHROME_EN = {
    "__LANG__": "en", "__UI_BEFORE__": "Before you begin",
    "__UI_NAME__": "Student name (required)", "__UI_EMAIL__": "Email (required)",
    "__UI_NAMEPH__": "Full name", "__UI_START__": "Start test →",
    "__UI_HOWTO__": ("Every question is multiple choice: choose one option, then "
                     "press <b>Next</b>. Answering each question is optional — press "
                     "<b>Next</b> to skip. Once you press <b>Next</b> you cannot "
                     "return to a previous question."),
    "__UI_DONE__": "Submission received ✔",
    "__UI_DONEMSG__": ("Thank you for taking the test. Your results have been sent to "
                       "HK-Schools.com for review. We will be in contact shortly."),
    "__UI_CLOSE__": "You may now close this page.",
}
CHROME_SC = {
    "__LANG__": "zh-Hans", "__UI_BEFORE__": "作答前请阅读",
    "__UI_NAME__": "学生姓名（必填）", "__UI_EMAIL__": "电邮地址（必填）",
    "__UI_NAMEPH__": "姓名", "__UI_START__": "开始作答 →",
    "__UI_HOWTO__": ("本卷全部是选择题：选出一个答案，然后按<b>下一题</b>。每题都可以先跳过，"
                     "但一旦进入下一题便不能返回。"),
    "__UI_DONE__": "已收到你的答卷 ✔",
    "__UI_DONEMSG__": "多谢作答。成绩已发送给 HK-Schools.com，我们会尽快与你联络。",
    "__UI_CLOSE__": "你现在可以关闭这个页面。",
}
CHROME_TC = {k: (R.to_traditional(v) if k.startswith("__UI_") else v)
             for k, v in CHROME_SC.items()}
CHROME_TC["__LANG__"] = "zh-Hant"


# --------------------------------------------------------------- emit
def _json(o):
    import json
    return json.dumps(o, ensure_ascii=False)


def render_page(path, title, short, countline, tid, questions, ui, chrome,
                script_url):
    css, defs = page_assets()
    s = TEMPLATE
    for k, v in chrome.items():
        s = s.replace(k, v)
    s = (s.replace("__TITLE__", E(title)).replace("__SHORTTITLE__", E(short))
          .replace("__COUNTLINE__", E(countline)).replace("__TESTID__", tid)
          .replace("__SCRIPT_URL__", script_url))
    s = s.replace("</style>", css + "\n</style>")
    s = s.replace("<body>", "<body>\n" + defs)
    s = s.replace("/*__UI_JSON__*/{}", _json(ui))
    s = s.replace("/*__QUESTIONS_JSON__*/[]", _json(questions))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(s)

    # BUILD_NOTES rule 1: the retired access-code gate must ship hidden, or it
    # flashes a grey "Enter the access code" panel before the JS hides it.
    assert s.count('<div id="gate">') == 0, f"{path}: gate flash: bare #gate div"
    assert s.count('id="gate" style="display:none"') == 1, \
        f"{path}: gate must ship hidden"
    return path


def editions(mod):
    """Every page this content module produces: (slug, script, chrome, ui)."""
    subj = S.subject_of(mod.META)
    if subj == "Chinese":
        return [("chinese-sc", "sc", CHROME_SC, UI_SC),
                ("chinese-tc", "tc", CHROME_TC, UI_TC)]
    return [(S.SUBJECT_DIR[subj], None, CHROME_EN, UI_EN)]


def titles(meta, form, script):
    """Page title, tab-sized short title and the count line, from META."""
    n = form["n"]
    nq, total = meta["nq"], meta["total"]
    if script is None:
        return (f'Singapore {meta["level"]} · {meta["subject"]} · '
                f'Multiple-Choice Test {n}',
                meta["subject"],
                f'{nq} questions · {total} marks · {meta["time"]}')
    X = R.to_traditional if script == "tc" else (lambda s: s)
    mark = X("繁体") if script == "tc" else "简体"
    return (X(f'新加坡课程 {meta["level_cn"]} · {meta["subject_cn"]}') +
            f'（{mark}）' + X(f' · 选择题测验{CN[n - 1]}'),
            X(meta["subject_cn"]),
            X(f'共 {nq} 题 · 满分 {total} 分 · 时限 {meta["time_cn"]}'))


def write_pages(script_url="PASTE_YOUR_APPS_SCRIPT_URL_HERE", verbose=True):
    made = []
    for _name, mod in S.modules():
        meta = mod.META
        for form in mod.FORMS:
            tid = S.test_id(meta, form["n"])
            for slug, script, chrome, ui in editions(mod):
                zh = script is not None
                X = R.to_traditional if script == "tc" else (lambda s: s)
                # DATA is converted, never the rendered page: markup between
                # characters destroys the phrase context OpenCC needs.  Same
                # call, same order, as mc/render.py.
                f = R.tc(form) if script == "tc" else form
                qs = questions_for(f, zh, X)
                nq = sum(len(q["parts"]) if q.get("parts") else 1 for q in qs)
                assert nq == meta["nq"], \
                    f"{tid} {slug}: page carries {nq} questions, META says {meta['nq']}"
                title, short, countline = titles(meta, form, script)
                path = os.path.join(PORTAL, "singapore-tests", "mc", slug,
                                    meta["level"].lower(), f"test-{form['n']}",
                                    "index.html")
                render_page(path, title, short, countline, tid, qs, ui, chrome,
                            script_url)
                made.append(path)
                if verbose:
                    print(f"  page {os.path.relpath(path, PORTAL):<52} "
                          f"{tid:<16} {nq:>3} q · {len(qs):>3} screens")
    print(f"\n{len(made)} pages -> {PORTAL}/singapore-tests/mc/")
    return made


if __name__ == "__main__":
    write_pages(sys.argv[1] if len(sys.argv) > 1
                else "PASTE_YOUR_APPS_SCRIPT_URL_HERE")
