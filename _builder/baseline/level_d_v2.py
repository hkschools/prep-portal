# -*- coding: utf-8 -*-
"""HKS Baseline Assessment · Years 9-10 (current Y9-Y10 / G8-G9), version 2. 75 min core.

Parallel form of level_d_v1: identical structure and timing, all-new content.
Top tier: ISEE-Upper/SSAT-level vocabulary, three double-blank completions,
four verbal-logic items, double-rule and interleaved NVR, and Y8-Y9 maths
(Pythagoras, simultaneous reasoning, rates, probability). Curriculum codes on
every item.
"""
from figlib import *

BAND = "level-d"
BAND_LABEL = "Level D"
YEAR_SPAN = "Years 9-10"
YEARS = ["Year 9", "Year 10"]

SECTIONS = [
    {"name": "Verbal Reasoning", "minutes": 13},        # 25 Q at ~30 s
    {"name": "Non-Verbal Reasoning", "minutes": 10},    # 20 Q at 30 s
    {"name": "Mathematics", "minutes": 17},             # 7 short + 8 story
    {"name": "Reading Comprehension", "minutes": 13},
    {"name": "Listening", "minutes": 6},                # 3 recordings, 10 Q
    {"name": "Writing", "minutes": 12},
    {"name": "Speaking", "minutes": 4},
    {"name": "中文閱讀 Chinese Reading", "minutes": 8, "opt": "chinese"},
    {"name": "中文聆聽 Chinese Listening", "minutes": 4, "opt": "chinese"},
    {"name": "中文口語 Chinese Speaking", "minutes": 3, "opt": "chspeak"},
]

INFO = {
    "Verbal Reasoning": "This section tests advanced vocabulary, word relationships, sentence completion, grammar and logical deduction. Work quickly; you have about half a minute per question.",
    "Non-Verbal Reasoning": "This section uses figures: classification (three figures share a rule), matrices (complete the grid), and hidden-shape questions where you must find the given shape, at its exact size and orientation, inside a more complex drawing. About half a minute per question.",
    "Mathematics": "Read each question carefully and choose the best answer. The later questions are multi-step story problems. You may use rough paper, but no calculator.",
    "Reading Comprehension": "Read each passage carefully, then answer the questions. The passage is shown with every question, so you can always re-read it.",
    "Listening": "There are three recordings: a talk, a discussion and a short lecture. You may play each one up to two times. The questions test detail, opinion and implied meaning; answer each recording's questions before moving on.",
    "Writing": "You will see two writing tasks. Choose ONE and type your answer. Aim for about 220-300 words: plan before you write, develop your ideas in structured paragraphs, and leave time to review.",
    "Speaking": "In this final section you will record a short audio response. Find a quiet spot, allow microphone access when your browser asks, and speak clearly and naturally.",
    "中文聆聽 Chinese Listening": zh_blocks("現在是普通話聆聽部分。請按播放鍵，細心聆聽短講，每段錄音最多可以播放兩次。題目考核細節、詞語和說話人的態度。", "现在是普通话聆听部分。请按播放键，细心聆听短讲，每段录音最多可以播放两次。题目考核细节、词语和说话人的态度。"),
    "中文口語 Chinese Speaking": zh_blocks("請用普通話錄一段自我介紹。找一個安靜的地方，說話清楚自然，盡量發展你的想法。", "请用普通话录一段自我介绍。找一个安静的地方，说话清楚自然，尽量发展你的想法。"),
    "中文閱讀 Chinese Reading": zh_blocks("細心閱讀下面的文章，然後回答問題。文章和題目以繁體為主，附簡體對照。", "细心阅读下面的文章，然后回答问题。文章和题目以繁体为主，附简体对照。"),
}

def O(*pairs):
    return {k: v for k, v in pairs}

def bilingual(trad, simp):
    return f"{trad}<br><i>{simp}</i>" if simp and simp != trad else trad

_SYN = "Choose the word that is closest in meaning to the word in capitals."
_ANT = "Choose the word that is most nearly OPPOSITE in meaning to the word in capitals."
_ANA = "Work out how the first pair of words go together, then complete the second pair."
_SC = "Choose the word that best completes the sentence."
_SC2 = "Choose the pair of words that best completes the sentence."
_GR = "Choose the word or phrase that best completes the sentence."
_LG = "Read the information carefully, then answer the question."

# ---- Verbal Reasoning (25) --------------------------------------------------
VERBAL = [
    dict(stem=_SYN + "\n\nINDIFFERENT", options=O(("A", "curious"), ("B", "different"), ("C", "unconcerned"), ("D", "passionate")),
         correct="C", strand="Vocabulary: Synonyms", concept="Y9-10 Vocabulary · synonyms: indifferent = unconcerned",
         explanation="Indifferent means showing no interest: unconcerned. 'Different' is a sound-alike trap; passionate is closer to the opposite."),
    dict(stem=_SYN + "\n\nLUCID", options=O(("A", "clear"), ("B", "lucky"), ("C", "shiny"), ("D", "loose")),
         correct="A", strand="Vocabulary: Synonyms", concept="Y9-10 Vocabulary · synonyms: lucid = clear",
         explanation="A lucid explanation is easy to understand: clear. Do not confuse 'lucid' with 'lucky' or with things that shine."),
    dict(stem=_SYN + "\n\nAUDACIOUS", options=O(("A", "noisy"), ("B", "daring"), ("C", "obedient"), ("D", "careful")),
         correct="B", strand="Vocabulary: Synonyms", concept="Y9-10 Vocabulary · synonyms: audacious = daring",
         explanation="Audacious means showing bold risk-taking: daring. 'Noisy' is a trap from the aud- root, which relates to hearing, not boldness."),
    dict(stem=_SYN + "\n\nCONCISE", options=O(("A", "sharp"), ("B", "rambling"), ("C", "precise"), ("D", "brief")),
         correct="D", strand="Vocabulary: Synonyms", concept="Y9-10 Vocabulary · synonyms: concise = brief",
         explanation="Concise means saying much in few words: brief. Rambling is the opposite, and 'precise' (exact) is a near-miss that means accurate rather than short."),
    dict(stem=_ANT + "\n\nSCARCE", options=O(("A", "rare"), ("B", "plentiful"), ("C", "hidden"), ("D", "expensive")),
         correct="B", strand="Vocabulary: Antonyms", concept="Y9-10 Vocabulary · antonyms: scarce vs plentiful",
         explanation="Scarce means in short supply; plentiful means existing in large amounts. Rare is a synonym of scarce, not its opposite."),
    dict(stem=_ANT + "\n\nADVERSITY", options=O(("A", "prosperity"), ("B", "hardship"), ("C", "courage"), ("D", "ambition")),
         correct="A", strand="Vocabulary: Antonyms", concept="Y9-10 Vocabulary · antonyms: adversity vs prosperity",
         explanation="Adversity means difficult times; prosperity means times of success and comfort. Hardship is a synonym of adversity, not its opposite."),
    dict(stem=_ANT + "\n\nCOMPLIANT", options=O(("A", "obedient"), ("B", "cheerful"), ("C", "defiant"), ("D", "anxious")),
         correct="C", strand="Vocabulary: Antonyms", concept="Y9-10 Vocabulary · antonyms: compliant vs defiant",
         explanation="Compliant means willing to obey; defiant means openly refusing to obey. Obedient is a synonym of compliant, not its opposite."),
    dict(stem=_ANT + "\n\nRECKLESS", options=O(("A", "rash"), ("B", "fearless"), ("C", "hopeless"), ("D", "cautious")),
         correct="D", strand="Vocabulary: Antonyms", concept="Y9-10 Vocabulary · antonyms: reckless vs cautious",
         explanation="Reckless means acting without thinking of the consequences; cautious means acting with great care. Rash is a synonym of reckless."),
    dict(stem=_ANA + "\n\nFlock is to birds as fleet is to ______.",
         options=O(("A", "sailors"), ("B", "ships"), ("C", "speed"), ("D", "oceans")),
         correct="B", strand="Verbal Analogies", concept="Y9-10 Verbal Reasoning · analogies: collection to member",
         explanation="A flock is a group of birds; a fleet is a group of ships. Sailors crew the ships but are not what a fleet is made of."),
    dict(stem=_ANA + "\n\nThermometer is to temperature as barometer is to ______.",
         options=O(("A", "weather"), ("B", "rainfall"), ("C", "pressure"), ("D", "altitude")),
         correct="C", strand="Verbal Analogies", concept="Y9-10 Verbal Reasoning · analogies: instrument to what it measures",
         explanation="A thermometer measures temperature; a barometer measures air pressure. 'Weather' is what the reading is used to predict, not what is measured."),
    dict(stem=_ANA + "\n\nMiserly is to generous as timid is to ______.",
         options=O(("A", "bold"), ("B", "shy"), ("C", "quiet"), ("D", "gentle")),
         correct="A", strand="Verbal Analogies", concept="Y9-10 Verbal Reasoning · analogies: opposites",
         explanation="Miserly and generous are opposites, so the answer is the opposite of timid: bold. Shy is a synonym of timid."),
    dict(stem=_ANA + "\n\nWhisper is to shout as glance is to ______.",
         options=O(("A", "blink"), ("B", "wink"), ("C", "see"), ("D", "stare")),
         correct="D", strand="Verbal Analogies", concept="Y9-10 Verbal Reasoning · analogies: intensity (mild to extreme)",
         explanation="A whisper is a quiet version of a shout; a glance is a brief version of a stare. Both pairs move from mild to intense."),
    dict(stem=_ANA + "\n\nAuthor is to novel as choreographer is to ______.",
         options=O(("A", "stage"), ("B", "dance"), ("C", "orchestra"), ("D", "audience")),
         correct="B", strand="Verbal Analogies", concept="Y9-10 Verbal Reasoning · analogies: creator to creation",
         explanation="An author creates a novel; a choreographer creates a dance. The stage and audience are where and for whom it happens, not what is created."),
    dict(stem=_SC + "\n\nThe evidence was so ______ that the jury needed only minutes to reach a verdict.",
         options=O(("A", "compelling"), ("B", "contradictory"), ("C", "tedious"), ("D", "scarce")),
         correct="A", strand="Sentence Completion", concept="Y9-10 Reading · sentence completion: cause-and-effect clue (ISEE style)",
         explanation="A quick, easy verdict is the effect of compelling evidence. Contradictory or scarce evidence would slow the jury down."),
    dict(stem=_SC + "\n\nOnce ______ across the entire region, the wetlands have now all but disappeared.",
         options=O(("A", "unknown"), ("B", "protected"), ("C", "widespread"), ("D", "flooded")),
         correct="C", strand="Sentence Completion", concept="Y9-10 Reading · sentence completion: contrast clue (ISEE style)",
         explanation="'Once … now all but disappeared' demands a contrast with disappearance: the wetlands were formerly widespread."),
    dict(stem=_SC2 + "\n\nAlthough the manual promised to ______ the installation, its instructions were so ______ that most users gave up.",
         options=O(("A", "simplify … convoluted"), ("B", "complicate … straightforward"), ("C", "shorten … concise"), ("D", "explain … helpful")),
         correct="A", strand="Sentence Completion", concept="Y9-10 Reading · double-blank with contrast signal (ISEE Upper style)",
         explanation="'Although' sets up a broken promise: the manual promised to simplify, yet its instructions were convoluted (confusingly complex), so users gave up."),
    dict(stem=_SC2 + "\n\nThe critics dismissed her theory as ______, yet decades later new data proved it remarkably ______.",
         options=O(("A", "brilliant … flawed"), ("B", "far-fetched … accurate"), ("C", "cautious … tentative"), ("D", "popular … famous")),
         correct="B", strand="Sentence Completion", concept="Y9-10 Reading · double-blank with reversal signal (ISEE Upper style)",
         explanation="'Yet' reverses the direction: what was dismissed as far-fetched turned out to be accurate. 'Dismissed' rules out a positive first word."),
    dict(stem=_SC2 + "\n\nFar from ______ the rumours, the spokesman's vague reply only ______ them.",
         options=O(("A", "spreading … silenced"), ("B", "confirming … proved"), ("C", "hearing … repeated"), ("D", "dispelling … fuelled")),
         correct="D", strand="Sentence Completion", concept="Y9-10 Reading · double-blank with reversal signal (ISEE Upper style)",
         explanation="'Far from' reverses the first word: instead of dispelling (clearing away) the rumours, the vague reply fuelled them, making them stronger."),
    dict(stem=_GR + "\n\nBy the time the guests arrived, the caterers ______ the tables.",
         options=O(("A", "already set"), ("B", "had already set"), ("C", "have already set"), ("D", "were already setting up of")),
         correct="B", strand="Grammar & Cloze", concept="Y10 Grammar · past perfect for the earlier of two past events",
         explanation="The setting happened before another past event (the guests arriving), so the past perfect 'had already set' is needed."),
    dict(stem=_GR + "\n\nThe committee, along with its two advisers, ______ meeting again tomorrow.",
         options=O(("A", "are"), ("B", "were"), ("C", "is"), ("D", "have been")),
         correct="C", strand="Grammar & Cloze", concept="Y9 Grammar · agreement: interrupting phrase does not change the subject",
         explanation="The subject is 'the committee' (singular); 'along with its two advisers' is an interrupting phrase and does not make it plural: is."),
    dict(stem=_GR + "\n\nShe is one of those students who ______ never satisfied with second place.",
         options=O(("A", "are"), ("B", "is"), ("C", "was"), ("D", "be")),
         correct="A", strand="Grammar & Cloze", concept="Y10 Grammar · relative clause agreement ('one of those … who' + plural)",
         explanation="'Who' refers back to 'those students' (plural), not to 'one', so the verb is plural: students who are never satisfied."),
    dict(stem=_LG + "\n\nNo insects have eight legs. All beetles are insects. Which statement MUST be true?",
         options=O(("A", "All insects are beetles"), ("B", "Some beetles have eight legs"),
                   ("C", "All eight-legged animals are spiders"), ("D", "No beetles have eight legs")),
         correct="D", strand="Verbal Logic", concept="Y9-10 Reasoning · syllogism with a negative premise",
         explanation="Beetles are insects, and no insects have eight legs, so no beetles have eight legs. The other statements go beyond the premises."),
    dict(stem=_LG + "\n\nFour students W, X, Y and Z each give a talk on a different day, Day 1 to Day 4. Z speaks on Day 1. X speaks on the day immediately before Y. W does not speak on Day 2. On which day does Y speak?",
         options=O(("A", "Day 2"), ("B", "Day 3"), ("C", "Day 4"), ("D", "It cannot be determined")),
         correct="B", strand="Verbal Logic", concept="Y9-10 Reasoning · scheduling deduction",
         explanation="Z takes Day 1, so X and Y (consecutive) fill Days 2-3 or Days 3-4. If X-Y took Days 3-4, W would be forced onto Day 2, which is not allowed. So X speaks Day 2 and Y speaks Day 3, leaving W on Day 4."),
    dict(stem=_LG + "\n\nAll violinists in the orchestra read music. Some students are violinists in the orchestra. Which statement MUST be true?",
         options=O(("A", "All students read music"), ("B", "Some students read music"),
                   ("C", "All musicians are students"), ("D", "Some violinists cannot read music")),
         correct="B", strand="Verbal Logic", concept="Y9-10 Reasoning · syllogism: some/all chains",
         explanation="The students who are violinists in the orchestra must read music, so at least some students read music. Nothing supports the stronger claims."),
    dict(stem=_LG + "\n\nIn a code, MOUNT is written as OQWPV. Using the same code, how is CLIFF written?",
         options=O(("A", "AJGDD"), ("B", "DMJGG"), ("C", "ENKHH"), ("D", "ENKGG")),
         correct="C", strand="Verbal Logic", concept="Y9-10 Reasoning · letter-shift code (two places forward)",
         explanation="Each letter moves forward two places (M to O, O to Q, U to W …), so CLIFF becomes ENKHH. AJGDD shifts two places backwards instead."),
]

# ---- Non-Verbal Reasoning (20 = 14 CAT4-engine + 6 GL-style) ----------------
_SEQ = "Look at the four pictures in the top row. Work out the pattern, then choose the picture (A-E) that belongs in the empty box."
_CODE = "Each picture on the left has a two-letter code. Work out what each letter stands for, then choose the code for the picture marked '?'."

NONVERBAL = nvr_from_json("level-d", 2) + [
    dict(stem=_SEQ, correct="B", strand="Figure Series (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM series style) · two rules: the pentagon shrinks AND the fill alternates",
         explanation="Two rules run together: the pentagon shrinks in equal steps (26, 22, 18, 14) AND the fill alternates black, white, black, white. Next: the smallest pentagon, filled black. A is the right size but white, and C is black but has stopped shrinking.",
         fig=seq_fig([cell(pentagon, 26), cell(pentagon, 22, "none"), cell(pentagon, 18), cell(pentagon, 14, "none")],
                     [cell(pentagon, 10, "none"), cell(pentagon, 10), cell(pentagon, 14),
                      cell(pentagon, 26), cell(pentagon, 18, "none")])),
    dict(stem=_SEQ, correct="D", strand="Figure Series (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM series style) · two interleaved series (alternating shapes, each with its own rotation)",
         explanation="Two series are interleaved: the triangles (positions 1 and 3) turn 90 degrees clockwise each time they appear, and the arrows (positions 2 and 4) do the same. Position 5 is a triangle, turned 90 degrees on from position 3: pointing down.",
         fig=seq_fig([cell(triangle, 20, INK, 0), cell(arrow, 30, 90), cell(triangle, 20, INK, 90), cell(arrow, 30, 180)],
                     [cell(arrow, 30, 270), cell(triangle, 20, INK, 90), cell(triangle, 20, INK, 270),
                      cell(triangle, 20, INK, 180), cell(triangle, 20, INK, 0)])),
    dict(stem=_SEQ, correct="A", strand="Figure Series (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM series style) · rotation of a chiral shape with a mirror trap",
         explanation="The L-shape turns 90 degrees clockwise each step (and after 270 it wraps round), so the next picture repeats the first: the quarter-turn position. C looks similar but is a mirror image, which no rotation can produce.",
         fig=seq_fig([cell(lshape, 8, 90), cell(lshape, 8, 180), cell(lshape, 8, 270), cell(lshape, 8, 0)],
                     [cell(lshape, 8, 90), cell(lshape, 8, 270), cell(lshape, 8, 90, mirror=True),
                      cell(lshape, 8, 180), cell(lshape, 8, 0)])),
    dict(stem=_CODE, correct="E", strand="Figure Codes (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM codes style) · first letter = shape family, second letter = shading",
         explanation="F means triangle and G means circle; X means black and Y means white. The mystery picture is a WHITE CIRCLE: GY.",
         fig=codes_fig([(cell(triangle, 16, INK), "FX"), (cell(triangle, 16, "none"), "FY"), (cell(circle, 13, INK), "GX")],
                       cell(circle, 13, "none")),
         options=O(("A", "FX"), ("B", "GX"), ("C", "FY"), ("D", "GZ"), ("E", "GY"))),
    dict(stem=_CODE, correct="C", strand="Figure Codes (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM codes style) · first letter = direction, second letter = size",
         explanation="M means pointing right, N pointing down and P pointing left; R means a large arrow and S a small one. The mystery picture is a LARGE arrow pointing DOWN: NR.",
         fig=codes_fig([(cell(arrow, 34, 0), "MR"), (cell(arrow, 22, 90), "NS"), (cell(arrow, 34, 180), "PR")],
                       cell(arrow, 34, 90)),
         options=O(("A", "MR"), ("B", "NS"), ("C", "NR"), ("D", "PR"), ("E", "MS"))),
    dict(stem=_CODE, correct="E", strand="Figure Codes (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM codes style) · first letter = shape family, second letter = shaded side",
         explanation="T means half-shaded square and V means half-shaded circle; D means shaded on the left, H shaded on top, E shaded on the bottom. The mystery picture is a circle shaded on TOP: VH.",
         fig=codes_fig([(cell(halfsquare, 16, 0), "TD"), (cell(halfsquare, 16, 90), "TH"),
                        (cell(halfcircle, 17, 270), "VE"), (cell(halfcircle, 17, 0), "VD")],
                       cell(halfcircle, 17, 90)),
         options=O(("A", "TH"), ("B", "VD"), ("C", "VE"), ("D", "TD"), ("E", "VH"))),
]

# ---- Mathematics (15: 7 short incl. 3 quantitative comparisons + 8 story) ---
_QC = ("Compare Quantity A and Quantity B, then choose:\n"
       "A) Quantity A is greater   B) Quantity B is greater\n"
       "C) The two quantities are equal   D) It cannot be determined from the information given\n\n")
_QC_OPTS = O(("A", "Quantity A is greater"), ("B", "Quantity B is greater"),
             ("C", "The two quantities are equal"), ("D", "It cannot be determined"))

MATHS = [
    # short form
    dict(stem="Work out 2<sup>6</sup> ÷ 2<sup>2</sup>",
         options=O(("A", "8"), ("B", "16"), ("C", "64"), ("D", "3")),
         correct="B", strand="Number", concept="Y8 Number · index laws: subtract the powers",
         explanation="2⁶ ÷ 2² = 2⁴ = 16. Dividing the indices (6 ÷ 2 = 3, giving 2³ = 8) is the classic error."),
    dict(stem="Solve 4(x − 2) = 3x + 7",
         options=O(("A", "x = −1"), ("B", "x = 9"), ("C", "x = 15"), ("D", "x = 1")),
         correct="C", strand="Algebra", concept="Y9 Algebra · expanding a bracket, x on both sides",
         explanation="4x − 8 = 3x + 7, so x = 15. Getting x = 9 comes from forgetting to multiply the 2 by 4 (writing 4x − 2)."),
    dict(stem="After a 15% discount, a jacket costs HK$102. What was the ORIGINAL price?",
         options=O(("A", "HK$86.70"), ("B", "HK$117.30"), ("C", "HK$120"), ("D", "HK$110")),
         correct="C", strand="Number", concept="Y9 Percentages · reverse percentage",
         explanation="HK$102 is 85% of the original, so the original is 102 ÷ 0.85 = HK$120. Adding 15% to 102 (HK$117.30) is the classic error."),
    dict(stem="What is the nth term of the sequence 7, 11, 15, 19, …?",
         options=O(("A", "4n + 3"), ("B", "3n + 4"), ("C", "n + 4"), ("D", "7n")),
         correct="A", strand="Algebra", concept="Y8 Sequences · nth term of a linear sequence",
         explanation="The sequence goes up in 4s, so the rule starts 4n; when n = 1 it must give 7, so it is 4n + 3. 3n + 4 mixes up the difference and the adjustment."),
    dict(stem=_QC + "Quantity A: 0.3²\nQuantity B: 0.3",
         options=_QC_OPTS,
         correct="B", strand="Quantitative Comparison", concept="Y8 Number · squaring a number between 0 and 1 (ISEE style)",
         explanation="0.3² = 0.09, which is SMALLER than 0.3. Squaring a number between 0 and 1 makes it smaller; assuming squaring always enlarges is the trap."),
    dict(stem=_QC + "n is a positive integer.\n\nQuantity A: (n + 1)²\nQuantity B: n² + 1",
         options=_QC_OPTS,
         correct="A", strand="Quantitative Comparison", concept="Y9 Algebra · expanding a bracket, quantitative comparison (ISEE style)",
         explanation="(n + 1)² = n² + 2n + 1. Since n is a positive integer, 2n > 0, so Quantity A exceeds Quantity B by 2n. Treating (n + 1)² as n² + 1 is the classic expansion error."),
    dict(stem=_QC + "x > 0\n\nQuantity A: x\nQuantity B: 1/x",
         options=_QC_OPTS,
         correct="D", strand="Quantitative Comparison", concept="Y9 Number · quantitative comparison with an unfixed variable (ISEE style)",
         explanation="If x = 2, Quantity A is greater (2 > 1/2). If x = 1/2, Quantity B is greater (1/2 < 2). If x = 1 they are equal. Since different allowed values give different verdicts, it cannot be determined."),
    # story form
    dict(stem="A 10-metre ladder leans against a vertical wall. Its foot rests on level ground 6 m from the base of the wall, as shown. How far UP the wall does the ladder reach?",
         fig=right_triangle_fig("6 m", "? m", "10 m"),
         options=O(("A", "4 m"), ("B", "8 m"), ("C", "11.7 m"), ("D", "16 m")),
         correct="B", strand="Problem Solving", concept="Y9 Geometry · Pythagoras' theorem (finding a shorter side)",
         explanation="10² − 6² = 100 − 36 = 64, and the square root of 64 is 8 m. Adding the squares instead of subtracting gives 11.7; 4 m comes from simply subtracting 6 from 10."),
    dict(stem="A pen costs HK$12 and a pencil costs HK$5. Maya buys 7 items in total and pays HK$63. How many PENS did she buy?",
         options=O(("A", "2"), ("B", "3"), ("C", "5"), ("D", "4")),
         correct="D", strand="Problem Solving", concept="Y9 Algebra · setting up simultaneous conditions",
         explanation="With p pens: 12p + 5(7 − p) = 63, so 7p + 35 = 63 and p = 4. Check: 4 pens (HK$48) + 3 pencils (HK$15) = HK$63."),
    dict(stem="A printer prints 45 pages in 3 minutes. At the same rate, how long will it take to print 120 pages?",
         options=O(("A", "6 minutes"), ("B", "7 minutes"), ("C", "8 minutes"), ("D", "9 minutes")),
         correct="C", strand="Problem Solving", concept="Y8 Ratio & Rates · unitary method (rate per minute)",
         explanation="45 pages in 3 minutes is 15 pages per minute, so 120 pages take 120 ÷ 15 = 8 minutes."),
    dict(stem="A phone plan costs HK$68 per month and includes 5 GB of data. Each EXTRA gigabyte costs HK$12. In March, Ken used 9 GB. What was his bill?",
         options=O(("A", "HK$96"), ("B", "HK$104"), ("C", "HK$176"), ("D", "HK$116")),
         correct="D", strand="Problem Solving", concept="Y9 Number · stepped-rate real-world problem (base charge plus usage)",
         explanation="Ken used 9 − 5 = 4 extra GB: 4 × HK$12 = HK$48, plus the HK$68 base gives HK$116. HK$176 charges for all 9 GB; HK$104 charges only 3 extra GB."),
    dict(stem="A shop buys a lamp for HK$500 and sells it for HK$420 in a clearance sale. What is the shop's percentage loss?",
         options=O(("A", "16%"), ("B", "19%"), ("C", "20%"), ("D", "8%")),
         correct="A", strand="Problem Solving", concept="Y9 Percentages · percentage loss on cost price",
         explanation="The loss is HK$80 on a cost of HK$500: 80/500 = 16%. Dividing by the selling price (80/420, about 19%) is the classic error."),
    dict(stem="The spinner shown has 12 equal sectors. What is the probability that one spin lands on a sector marked T?",
         fig=spinner([("S", 5, "#72AFDB"), ("T", 4, "#eef2f8"), ("W", 3, "#c9d6e4")]),
         options=O(("A", "1/4"), ("B", "1/3"), ("C", "4/8"), ("D", "1/2")),
         correct="B", strand="Problem Solving", concept="Y8 Probability · probability from a diagram",
         explanation="4 of the 12 equal sectors are marked T: 4/12 = 1/3. Choosing 1/4 comes from counting 4 as a quarter without checking the total of 12; 4/8 compares T with only the other sectors."),
    dict(stem="The graph shows a hiker's journey. Distance from the start (km) is plotted against time (hours). What was the hiker's speed during the FINAL hour?",
         fig=line_graph(["0", "1", "2", "3"], [0, 40, 40, 100], 100, 20, unit="km"),
         options=O(("A", "40 km/h"), ("B", "50 km/h"), ("C", "100 km/h"), ("D", "60 km/h")),
         correct="D", strand="Problem Solving", concept="Y9 Graphs · reading speed from a distance-time graph",
         explanation="Between hour 2 and hour 3 the distance rises from 40 km to 100 km: 60 km/h. 40 km/h is the FIRST hour's speed, and 100 km is the total distance, not a speed."),
    dict(stem="The bar chart shows the rainfall recorded in four months. What was the MEAN monthly rainfall over the four months?",
         fig=bar_chart(["May", "Jun", "Jul", "Aug"], [40, 60, 90, 50], 100, 20, unit="mm"),
         options=O(("A", "60 mm"), ("B", "50 mm"), ("C", "90 mm"), ("D", "240 mm")),
         correct="A", strand="Problem Solving", concept="Y8 Statistics · calculating a mean from a bar chart",
         explanation="Total rainfall is 40 + 60 + 90 + 50 = 240 mm over 4 months: mean = 240 ÷ 4 = 60 mm. 240 is the total (forgetting to divide), and 90 is just the highest bar."),
]

# ---- Reading Comprehension (12) --------------------------------------------
PASSAGE_1 = (
    "<strong>The String</strong><br><br>"
    "My father kept his kites in a long canvas bag behind the wardrobe, and on the first windy Saturday of "
    "every autumn the bag came out and we took the bus to the headland. He had built most of them himself: "
    "bamboo bones, paper skins, tails cut from an old bedsheet. The finest was a blue swallow with wings so "
    "thin the light came through them.<br><br>"
    "I was seven when he first let me hold the line. 'The wind does the flying,' he said, closing my fingers "
    "around the spool. 'Your job is to listen.' I did not understand him then. I only knew that the line "
    "trembled against my palm like a live thing, and that somewhere far above, the blue swallow was pulling "
    "at me.<br><br>"
    "As I grew, he let out more line. That was his way. Other fathers gave lectures; mine gave string. When I "
    "started secondary school across the harbour, when I stayed out late after rehearsals, when I chose "
    "subjects he would never have chosen, he said very little. But the spool in his hands kept turning, a few "
    "more metres every year, and the kite that was me flew further and further out over the water. Sometimes "
    "I drifted; sometimes I dived. He watched the sky, said nothing, and wound in a metre or two only when "
    "the line went slack.<br><br>"
    "Once, I asked whether he ever worried the line would snap. He considered the question seriously, as he "
    "considered everything. 'A line only snaps if you hold it too tight,' he said. 'Hold lightly. The holding "
    "is the important thing, not the tightness.'<br><br>"
    "He is older now, and his wrists ache in cold weather, so this autumn it was I who carried the bag up the "
    "headland while he sat on the bench with the thermos. The blue swallow is patched in three places, but it "
    "still climbs like a note in a song. Standing where he used to stand, I finally understood what I had "
    "been listening for all those years. Everything the kite feels travels down the line: every gust, every "
    "dip, every recovery. He had known each time I struggled, hundreds of metres away and small against the "
    "sky, not because he watched, but because he held.<br><br>"
    "I flew the kite until the light went, then wound the line in slowly, the way he taught me, and the blue "
    "swallow came home in wide, obedient circles. My father nodded, as though something had been said. "
    "Between us the string lay coiled in the bag: thin, patched, unbroken."
)

PASSAGE_2 = (
    "<strong>In Defence of Handwriting</strong><br><br>"
    "Ask a classroom of teenagers when they last wrote a full page by hand and you will mostly get the same "
    "answer: in an exam, because they had no choice. Everywhere else, typing has won. It is faster, neater, "
    "searchable and instantly shareable, and some schools have begun quietly cutting handwriting practice "
    "from the timetable to make room for keyboard skills. Before we finish the job, it is worth asking what "
    "we would be throwing away.<br><br>"
    "The case for the pen is not nostalgia; it is cognitive. In a widely cited series of experiments, "
    "university students who took lecture notes on laptops were compared with students who took notes by "
    "hand. The typists recorded far more words, yet performed worse when tested on the ideas. Because typing "
    "is fast, it tempts the writer into transcription: copying what is said without processing it. "
    "Handwriting is slow, and that slowness forces a choice about what matters, which is exactly where the "
    "learning happens. The laptop note-taker is a court stenographer, capturing everything and weighing "
    "nothing; the hand note-taker is an editor. Follow-up studies sharpened the point: even when the typists "
    "were warned about the trap in advance, the sheer speed of the keys kept luring them back into copying.<br><br>"
    "Something similar happens with memory. Brain-imaging studies show that forming letters by hand activates "
    "motor and visual regions that pressing identical plastic keys does not, and young children who learn "
    "letters by writing them recognise those letters faster than children who learn them on screens. The "
    "hand, it turns out, is not just an output device; it is part of the thinking.<br><br>"
    "None of this makes typing the enemy. For long documents, for editing, for anyone whose handwriting is a "
    "private code even to themselves, the keyboard is a gift, and nobody seriously proposes drafting every "
    "essay by candlelight out of principle. The argument is narrower: handwriting and typing do different "
    "jobs, and a school that teaches only one is training half a mind. Notes, first drafts, plans and "
    "workings belong to the pen; polishing and publishing belong to the keys.<br><br>"
    "So the next time you find yourself pasting a chapter summary straight into a document, try an "
    "experiment. Close the laptop, take a sheet of paper, and push the chapter through your own hand. It will "
    "be slower. It will also be yours. A typed copy is a photograph of someone else's thinking; a handwritten "
    "page is a drawing of your own, and nobody ever learned to see by taking photographs."
)

_RC = "Y9-10 Reading · "
READING = [
    dict(passage=PASSAGE_1, stem="Throughout the passage, what does the kite string chiefly represent?",
         options=O(("A", "The father's skill at building kites"), ("B", "The danger of flying in strong wind"),
                   ("C", "The connection between father and child"), ("D", "The narrator's fear of growing up")),
         correct="C", strand="Reading: Fiction", concept=_RC + "interpreting the controlling metaphor",
         explanation="The string stands for the bond between them: the father 'lets out more line' as the narrator grows, and the closing line calls it 'thin, patched, unbroken'."),
    dict(passage=PASSAGE_1, stem="'Other fathers gave lectures; mine gave string.' What does this sentence suggest about the father?",
         options=O(("A", "He guided his child by granting freedom rather than by talking"),
                   ("B", "He preferred kite-flying to conversation"),
                   ("C", "He did not care which subjects the narrator chose"),
                   ("D", "He was too shy to give advice")),
         correct="A", strand="Reading: Fiction", concept=_RC + "inferring character from a compressed contrast",
         explanation="Instead of words of instruction, he gave more line: trust and freedom. The passage shows him noticing everything, so indifference and shyness are wrong."),
    dict(passage=PASSAGE_1, stem="'A line only snaps if you hold it too tight.' Beyond kite-flying, what is the father really saying?",
         options=O(("A", "Cheap string should be replaced every autumn"), ("B", "Children should never be disciplined"),
                   ("C", "It is safest to let go of the line in a storm"), ("D", "A relationship breaks when one person grips too hard, so hold on gently")),
         correct="D", strand="Reading: Fiction", concept=_RC + "interpreting figurative dialogue",
         explanation="He is describing how to hold on to a person: keep the connection ('the holding is the important thing') but without controlling force ('not the tightness')."),
    dict(passage=PASSAGE_1, stem="According to the final paragraphs, how did the father know each time the narrator struggled?",
         options=O(("A", "He watched the narrator closely through binoculars"), ("B", "Teachers reported back to him"),
                   ("C", "Because he kept hold of the line, he could feel every gust and dip"), ("D", "The narrator told him everything")),
         correct="C", strand="Reading: Fiction", concept=_RC + "locating the pivotal explanation",
         explanation="Everything the kite feels travels down the line: he knew 'not because he watched, but because he held'."),
    dict(passage=PASSAGE_1, stem="Which best describes the narrator's tone when speaking of the father?",
         options=O(("A", "Resentful about a strict upbringing"), ("B", "Affectionate and admiring, with new understanding"),
                   ("C", "Mocking his old-fashioned hobby"), ("D", "Indifferent and detached")),
         correct="B", strand="Reading: Fiction", concept=_RC + "identifying tone",
         explanation="The loving detail (the patched swallow, the thermos, 'as he considered everything') and the narrator's dawning insight signal affection and admiration."),
    dict(passage=PASSAGE_1, stem="Why does the passage end with the string 'thin, patched, unbroken'?",
         options=O(("A", "To show the family cannot afford new string"), ("B", "To warn that the kite will soon be lost"),
                   ("C", "To suggest the father's memory is fading"), ("D", "To show their bond has been worn and mended by the years, yet still holds")),
         correct="D", strand="Reading: Fiction", concept=_RC + "understanding the closing image",
         explanation="The three adjectives describe the relationship as much as the string: fragile-looking, repaired after strains, but never broken."),
    dict(passage=PASSAGE_2, stem="Which statement best sums up the writer's central argument?",
         options=O(("A", "Handwriting has real cognitive value and should keep its place alongside typing"),
                   ("B", "Schools should ban laptops from every lesson"),
                   ("C", "Typing is always inferior to writing by hand"),
                   ("D", "Exams should stop requiring handwritten answers")),
         correct="A", strand="Reading: Non-fiction", concept=_RC + "identifying the thesis of an argument",
         explanation="The writer argues the pen does cognitive work typing cannot, while explicitly keeping a role for the keyboard: the two 'do different jobs'."),
    dict(passage=PASSAGE_2, stem="The writer includes the laptop-versus-longhand note-taking study in order to:",
         options=O(("A", "prove that laptop users type inaccurately"),
                   ("B", "show that students dislike taking notes"),
                   ("C", "provide research evidence that handwriting aids understanding where typing invites mere copying"),
                   ("D", "argue that lectures should be recorded instead")),
         correct="C", strand="Reading: Non-fiction", concept=_RC + "understanding the function of evidence",
         explanation="The typists wrote more but understood less: experimental support for the claim that typing tempts writers into transcription while handwriting forces processing."),
    dict(passage=PASSAGE_2, stem="The writer calls the laptop note-taker 'a court stenographer' and the hand note-taker 'an editor'. What is the point of this comparison?",
         options=O(("A", "Typists should consider careers in the law courts"),
                   ("B", "One records everything without judging it, while the other selects what matters"),
                   ("C", "Editors write more neatly than stenographers"),
                   ("D", "Both jobs are being replaced by machines")),
         correct="B", strand="Reading: Non-fiction", concept=_RC + "interpreting an analogy",
         explanation="A stenographer captures every word 'weighing nothing'; an editor chooses. The analogy contrasts mindless transcription with selective, thoughtful processing."),
    dict(passage=PASSAGE_2, stem="Which best describes the writer's attitude towards typing?",
         options=O(("A", "It is an enemy of education and should be resisted"),
                   ("B", "It is superior to handwriting in every respect"),
                   ("C", "It is a genuine gift for some jobs; the mistake is letting it do ALL the jobs"),
                   ("D", "It matters only for students with poor handwriting")),
         correct="C", strand="Reading: Non-fiction", concept=_RC + "identifying a nuanced position",
         explanation="The writer says typing is 'a gift' for long documents and editing; the narrower claim is that handwriting and typing do different jobs and both belong in school."),
    dict(passage=PASSAGE_2, stem="What does the writer mean by saying such a school 'is training half a mind'?",
         options=O(("A", "Only half of each lesson is spent on writing"),
                   ("B", "Teaching only one of the two skills develops only part of a student's thinking"),
                   ("C", "Schools employ too few teachers"),
                   ("D", "Students only remember half of what they type")),
         correct="B", strand="Reading: Non-fiction", concept=_RC + "evaluating a loaded phrase",
         explanation="Since pen and keyboard each do different cognitive jobs, a school teaching only keyboard skills leaves the pen's share of thinking untrained."),
    dict(passage=PASSAGE_2, stem="The passage closes: 'A typed copy is a photograph of someone else's thinking; a handwritten page is a drawing of your own.' What is the force of this final image?",
         options=O(("A", "Photographs are always less accurate than drawings"),
                   ("B", "Students should illustrate their notes with sketches"),
                   ("C", "Handwritten work looks more attractive than printed work"),
                   ("D", "Copying reproduces another person's thought, while writing by hand makes the ideas your own")),
         correct="D", strand="Reading: Non-fiction", concept=_RC + "understanding the closing image",
         explanation="A photograph merely reproduces; a drawing requires seeing and understanding. Pushing ideas 'through your own hand' turns them into your own thinking."),
]

# ---- Listening (3 recordings, 10 Q) ----------------------------------------
_LI = "Listen to the recording, then choose the best answer."
_A1, _A2, _A3 = "listening1.m4a", "listening2.m4a", "listening3.m4a"

AUDIO_TITLES = {
    "listening1.m4a": "The Neon Sign Makers",
    "listening2.m4a": "The Meat-Free Monday Debate",
    "listening3.m4a": "Shorebirds of the Flyway",
    "listening-zh.m4a": "短講一則 A Short Talk",
}

AUDIO = {
    "listening-zh.m4a": [("zh-CN-YunxiNeural", "-8%", "香港给人的印象总是高楼林立，其实全港约四成的土地属于郊野公园。周末走进山里，一个小时前你还在拥挤的地铁站，一个小时后已经站在山脊上，看着脚下的海湾。近年远足成了潮流，许多年轻人专程上山打卡，打卡的意思，就是拍照留念，再分享到网上。多一个人亲近山野，本来是好事，可是有人为了取景踩进草丛，也有人把垃圾留在山径上。山不会说话，它只是安静地包容着我们。我想说的是：欣赏风景之余，请记得把垃圾带走，也给野生动物留一点安静，让下一位上山的人，看到和你一样美的香港。")],
    _A1: [("en-GB-RyanNeural", "-6%",
        "If you look at old photographs of this city at night, the streets seem to burn: dragons, teapots and "
        "giant fish glowing above every road, written in bent tubes of coloured light. Neon signs were once so "
        "common here that pilots joked they could read the harbour like a menu. Each sign began as a drawing; "
        "then a craftsman heated a glass tube over a flame and bent it, curve by curve, entirely by hand. "
        "Today only a handful of these masters remain. Stricter building regulations have brought hundreds of "
        "ageing signs down, and shops that once ordered neon now choose LED panels, which are cheaper to run "
        "and easier to replace. So, one by one, the lights go out, and the city is quietly losing its "
        "handwriting. Some students have begun photographing the signs that survive, and museums now collect "
        "the best of them. A page of the city's diary is worth keeping, even after the ink has faded.")],
    _A2: [
        ("en-GB-RyanNeural", "-6%", "I think the canteen should go completely meat-free every Monday. Farming meat "
                        "produces a huge share of the world's greenhouse gases, and most of us eat more of it "
                        "than doctors recommend anyway. One day a week is a small change with a real effect."),
        ("en-US-AvaNeural", "-6%", "I understand the goal, but forcing it removes all choice. Some students train "
                          "after school and plan their meals carefully, and others will simply buy meat outside, "
                          "so the canteen loses money and nothing is gained. I would rather see a really good "
                          "plant-based dish on the menu every single day."),
        ("en-GB-RyanNeural", "-6%", "But if it is only ever an option, most people will walk straight past it. "
                        "Habits do not change by themselves."),
        ("en-US-AvaNeural", "-6%", "Then let us make the plant-based dish the featured meal, put it first in the "
                          "line, and price it a few dollars cheaper. Nudge people, without banning anything. We "
                          "could trial it for one term and survey students at the end."),
        ("en-GB-RyanNeural", "-6%", "A cheaper, featured plant-based dish every day, trialled for a term with a "
                        "survey. That I can support. If the numbers barely move, we revisit my Monday idea."),
    ],
    _A3: [("en-US-AvaNeural", "-6%",
        "Twice a year, one of the great migrations on Earth passes almost unnoticed over this city. Millions "
        "of shorebirds travel between the Arctic, where they breed, and Australia, where they winter, along a "
        "route scientists call a flyway. They cannot make the journey in one flight; they depend on a chain of "
        "coastal wetlands, and the mudflats here are one of the most important links. To a bird that has flown "
        "for days, a mudflat is a service station on a motorway: it offers food to refuel, and a safe place to "
        "rest before the next stage. Among the visitors is the black-faced spoonbill, a bird that was down to "
        "a few hundred individuals worldwide and, thanks to protection here and elsewhere, is slowly "
        "recovering. But the chain holds only while every link holds. Along the flyway, wetland after wetland "
        "has been drained or built over, and a migrating bird cannot simply choose a longer flight. Lose the "
        "stopovers, and we lose the migration; and a sky that has filled with wings every spring for thousands "
        "of years would, within our lifetime, simply empty.")],
}

LISTENING = [
    dict(stem=_LI + "\n\nWhat is the speaker's main point about the neon signs?", audio=_A1,
         options=O(("A", "They use too much electricity to be worth keeping"),
                   ("B", "A handcrafted part of the city's character is disappearing and deserves to be recorded"),
                   ("C", "They should all be replaced by LED panels as soon as possible"),
                   ("D", "They were mainly built to guide aircraft at night")),
         correct="B", strand="Listening", concept="Y9-10 Listening · main idea of a talk",
         explanation="The talk traces the craft and its decline, and closes by praising efforts to photograph and collect the signs: 'a page of the city's diary is worth keeping'."),
    dict(stem=_LI + "\n\nAccording to the speaker, why are the signs disappearing?", audio=_A1,
         options=O(("A", "Stricter building rules, and shops switching to cheaper LED panels"),
                   ("B", "Tourists have stopped visiting the old districts"),
                   ("C", "The glass tubes can no longer be imported"),
                   ("D", "Museums have taken most of them away")),
         correct="A", strand="Listening", concept="Y9-10 Listening · stated reason",
         explanation="The speaker names two causes: stricter building regulations bringing signs down, and shops choosing LED panels that are cheaper to run and easier to replace."),
    dict(stem=_LI + "\n\nHow was a neon sign made, according to the talk?", audio=_A1,
         options=O(("A", "Machines printed the tubes in a factory overnight"), ("B", "The tubes were carved from coloured ice-clear plastic"),
                   ("C", "A craftsman heated a glass tube over a flame and bent it by hand"),
                   ("D", "Painters coloured ordinary light bulbs by brush")),
         correct="C", strand="Listening", concept="Y9-10 Listening · supporting detail",
         explanation="Each sign began as a drawing, then a craftsman heated a glass tube over a flame and bent it 'curve by curve, entirely by hand'."),
    dict(stem=_LI + "\n\nWhat does the speaker mean by saying the city is 'losing its handwriting'?", audio=_A1,
         options=O(("A", "Schools no longer teach children to write neatly"),
                   ("B", "Street names are being repainted in a new typeface"),
                   ("C", "People now send messages instead of letters"),
                   ("D", "The hand-made signs that gave the city its distinctive look are vanishing")),
         correct="D", strand="Listening", concept="Y9-10 Listening · interpreting figurative language",
         explanation="Handwriting is personal and hand-made; as the hand-bent neon disappears, the city loses a signature look that machines cannot reproduce."),
    dict(stem=_LI + "\n\nWhat is the man's main reason for wanting a meat-free Monday?", audio=_A2,
         options=O(("A", "Meat has become too expensive for the canteen"),
                   ("B", "Most students have asked for vegetarian food"),
                   ("C", "Meat farming produces a large share of greenhouse gases, and we eat more meat than doctors advise"),
                   ("D", "The kitchen staff cannot cook meat safely")),
         correct="C", strand="Listening", concept="Y9-10 Listening · speaker's position in a discussion",
         explanation="He gives two reasons: farming meat produces a huge share of greenhouse gases, and most people eat more meat than doctors recommend."),
    dict(stem=_LI + "\n\nWhy does the woman oppose a compulsory meat-free day?", audio=_A2,
         options=O(("A", "It removes choice, and students would simply buy meat outside the school"),
                   ("B", "She believes meat is essential at every meal"),
                   ("C", "Plant-based dishes cost more to prepare"),
                   ("D", "The teachers would refuse to eat in the canteen")),
         correct="A", strand="Listening", concept="Y9-10 Listening · evaluating a counter-argument",
         explanation="She argues that forcing it removes all choice, and that students would buy meat outside, so the canteen loses money 'and nothing is gained'."),
    dict(stem=_LI + "\n\nWhat plan do the two speakers finally agree to try?", audio=_A2,
         options=O(("A", "Banning meat from the canteen completely"),
                   ("B", "A cheaper, featured plant-based dish every day, trialled for a term with a survey"),
                   ("C", "Leaving the menu exactly as it is"),
                   ("D", "Asking parents to vote on the menu")),
         correct="B", strand="Listening", concept="Y9-10 Listening · synthesis (the point of agreement)",
         explanation="They settle on her nudge: a featured plant-based dish, placed first and priced cheaper, for a one-term trial with a survey; his Monday idea returns only if the numbers barely move."),
    dict(stem=_LI + "\n\nAccording to the lecturer, what do the mudflats offer migrating birds?", audio=_A3,
         options=O(("A", "A place to build nests and raise chicks"),
                   ("B", "Warm water for the winter months"),
                   ("C", "Protection from birds of prey during breeding"),
                   ("D", "Food to refuel and a safe place to rest mid-journey")),
         correct="D", strand="Listening", concept="Y9-10 Listening · grouped details",
         explanation="The lecturer compares a mudflat to a motorway service station: it offers food to refuel and a safe place to rest before the next stage. Breeding happens in the Arctic, not here."),
    dict(stem=_LI + "\n\nWhat problem threatens the migration?", audio=_A3,
         options=O(("A", "Wetlands along the flyway are being drained or built over"),
                   ("B", "The birds are being hunted in the Arctic"),
                   ("C", "Climate change has made Australia too hot"),
                   ("D", "The spoonbills frighten away the smaller birds")),
         correct="A", strand="Listening", concept="Y9-10 Listening · identifying the central problem",
         explanation="The chain holds only while every link holds: along the flyway, 'wetland after wetland has been drained or built over', and the birds cannot fly further to compensate."),
    dict(stem=_LI + "\n\nWhich best describes the lecturer's attitude?", audio=_A3,
         options=O(("A", "Bored by a routine natural event"), ("B", "Confident that no action is needed"),
                   ("C", "Full of wonder at the migration, and urgent about protecting it"), ("D", "Hostile towards coastal development of any kind")),
         correct="C", strand="Listening", concept="Y9-10 Listening · speaker's tone and attitude",
         explanation="The lecture opens with awe ('one of the great migrations on Earth') and closes with urgency: lose the stopovers and the sky 'would, within our lifetime, simply empty'."),
]

# ---- Writing / Speaking / Chinese ------------------------------------------
CONTENT_WRITING = dict(
    type="writing",
    intro="Choose ONE of the two tasks below and type your answer in the box. Aim for about 220-300 words.",
    body=("Task 1: Write about a time you failed at something that genuinely mattered to you. Describe what "
          "happened, how you responded in the days that followed, and what the experience taught you about "
          "yourself.\n\n"
          "Task 2: 'Schools should make community service compulsory for every student.' To what extent do "
          "you agree? Develop a structured argument with clear reasons and examples, and acknowledge at "
          "least one point on the other side."),
    hint="Plan before you write: a clear introduction, developed paragraphs and a conclusion. Leave two minutes to review your accuracy and word choice.",
    placeholder="Type your answer here; it will be saved for review…",
)

CONTENT_SPEAKING = dict(
    type="speaking",
    stem="Record a short spoken response (about 2 minutes).",
    body=("Speak about:\n"
          "• Your name, your current school and year group\n"
          "• A subject or topic that fascinates you, and what first drew you to it\n"
          "• A time you worked with others to get something done, and your part in it\n"
          "• Something new you hope to try at your next school, and why\n\n"
          "Speak naturally and develop your points; this is a chance for your future school to hear how you think."),
)

CH_PASSAGE_TRAD = (
    "比賽落敗那天，隊友都哭了，教練只說了一句：「懂得贏之前，先要輸得起。」當時我很不服氣，如今回想，"
    "這句話竟成了我最重要的一課。\n\n"
    "我們從小被教導要追求勝利，卻很少有人教我們如何面對失敗。有人一輸就把責任推給隊友和裁判，有人從此"
    "不敢再站上賽場。這樣的人，其實不是輸給對手，而是輸給了自己，因為他們把失敗當成了終點，而不是路標。\n\n"
    "失敗像一面鏡子，它照出我們的不足，也照出我們的態度。願意直視它的人，能看清自己該往哪裏走；急着把"
    "它翻過去的人，往往在同一個地方跌倒第二次。鏡子不會說謊，怕照鏡子的人，只能一直帶着看不見的缺點上場。\n\n"
    "竹子破土之前，要先在黑暗的泥土裏扎根好幾年。那些看不見的日子，正是它日後節節上升的本錢。輸得起，"
    "不是甘於失敗，而是把每一次跌倒，都當成向下扎根的機會。能這樣想的人，總有一天，會贏得漂亮。"
)
CH_PASSAGE_SIMP = (
    "比赛落败那天，队友都哭了，教练只说了一句：“懂得赢之前，先要输得起。”当时我很不服气，如今回想，"
    "这句话竟成了我最重要的一课。\n\n"
    "我们从小被教导要追求胜利，却很少有人教我们如何面对失败。有人一输就把责任推给队友和裁判，有人从此"
    "不敢再站上赛场。这样的人，其实不是输给对手，而是输给了自己，因为他们把失败当成了终点，而不是路标。\n\n"
    "失败像一面镜子，它照出我们的不足，也照出我们的态度。愿意直视它的人，能看清自己该往哪里走；急着把"
    "它翻过去的人，往往在同一个地方跌倒第二次。镜子不会说谎，怕照镜子的人，只能一直带着看不见的缺点上场。\n\n"
    "竹子破土之前，要先在黑暗的泥土里扎根好几年。那些看不见的日子，正是它日后节节上升的本钱。输得起，"
    "不是甘于失败，而是把每一次跌倒，都当成向下扎根的机会。能这样想的人，总有一天，会赢得漂亮。"
)

def _ch(stem_t, stem_s, opts_ts, correct, concept, explanation):
    return dict(
        passage=zh_blocks(CH_PASSAGE_TRAD.replace("\n\n", "<br><br>"), CH_PASSAGE_SIMP.replace("\n\n", "<br><br>")),
        stem=bilingual(stem_t, stem_s),
        options=O(*[(k, bilingual(t, s)) for k, (t, s) in opts_ts.items()]),
        correct=correct, strand="中文閱讀理解", concept="高中中文 · " + concept, explanation=explanation)

CHINESE = [
    _ch("對教練那句「懂得贏之前，先要輸得起」，作者的態度經歷了怎樣的變化？", "对教练那句“懂得赢之前，先要输得起”，作者的态度经历了怎样的变化？",
        {"A": ("一直深信不疑", "一直深信不疑"), "B": ("起初不服氣，後來深深認同", "起初不服气，后来深深认同"),
         "C": ("起初認同，後來懷疑", "起初认同，后来怀疑"), "D": ("始終覺得與自己無關", "始终觉得与自己无关")},
        "B", "內容理解：作者態度的變化", "作者自言「當時我很不服氣」，但「如今回想，這句話竟成了我最重要的一課」，可見由抗拒轉為認同。"),
    _ch("「願意直視它的人，能看清自己該往哪裏走」一句中，「它」指的是：", "“愿意直视它的人，能看清自己该往哪里走”一句中，“它”指的是：",
        {"A": ("勝利", "胜利"), "B": ("對手", "对手"), "C": ("失敗", "失败"), "D": ("鏡子裏的自己", "镜子里的自己")},
        "C", "內容理解：代詞指代", "上文說「失敗像一面鏡子」，「直視它」承接這個比喻，指的是敢於面對失敗。"),
    _ch("作者把「失敗」比作甚麼？", "作者把“失败”比作什么？",
        {"A": ("一面鏡子", "一面镜子"), "B": ("一場比賽", "一场比赛"),
         "C": ("黑暗的泥土", "黑暗的泥土"), "D": ("一位嚴厲的教練", "一位严厉的教练")},
        "A", "修辭理解：比喻", "文中明言：「失敗像一面鏡子，它照出我們的不足，也照出我們的態度。」"),
    _ch("文中竹子的例子，主要說明甚麼道理？", "文中竹子的例子，主要说明什么道理？",
        {"A": ("植物生長需要陽光", "植物生长需要阳光"), "B": ("成功要靠好的環境", "成功要靠好的环境"),
         "C": ("凡事要爭分奪秒", "凡事要争分夺秒"), "D": ("看不見的積累，是日後成長的本錢", "看不见的积累，是日后成长的本钱")},
        "D", "內容理解：例證作用", "竹子破土前先在泥土裏扎根多年，比喻跌倒與磨練是「日後節節上升的本錢」。"),
    _ch("「輸得起，不是甘於失敗」，作者想辨明的是：", "“输得起，不是甘于失败”，作者想辨明的是：",
        {"A": ("輸得起等於不在乎輸贏", "输得起等于不在乎输赢"), "B": ("輸了就應該放棄比賽", "输了就应该放弃比赛"),
         "C": ("輸得起是把跌倒化作扎根的機會，不是安於失敗", "输得起是把跌倒化作扎根的机会，不是安于失败"),
         "D": ("只有常勝的人才輸得起", "只有常胜的人才输得起")},
        "C", "內容理解：辨析概念", "作者隨即解釋：輸得起是「把每一次跌倒，都當成向下扎根的機會」，與消極認命劃清界線。"),
    _ch("下面哪一項最能概括全文的主旨？", "下面哪一项最能概括全文的主旨？",
        {"A": ("批評教練的訓練方法", "批评教练的训练方法"),
         "B": ("敢於面對失敗、從失敗中積蓄力量的人，才走得遠", "敢于面对失败、从失败中积蓄力量的人，才走得远"),
         "C": ("比賽的勝負完全取決於運氣", "比赛的胜负完全取决于运气"),
         "D": ("種竹子比打比賽更有意義", "种竹子比打比赛更有意义")},
        "B", "主旨理解", "全文由落敗經歷引入，經鏡子與竹子兩個比喻，歸結出「輸得起」方能「贏得漂亮」的道理。"),
]

CH_LISTENING = [
    dict(stem=bilingual("聆聽短講，然後回答問題。\n\n說話人主要想帶出甚麼信息？", "聆听短讲，然后回答问题。\n\n说话人主要想带出什么信息？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("介紹香港的郊野，並呼籲大家愛護山野", "介绍香港的郊野，并呼吁大家爱护山野")),
                   ("B", bilingual("教大家選購遠足裝備", "教大家选购远足装备")),
                   ("C", bilingual("批評年輕人沉迷上網", "批评年轻人沉迷上网")),
                   ("D", bilingual("比較地鐵和巴士的優劣", "比较地铁和巴士的优劣"))),
         correct="A", strand="中文聆聽理解", concept="高中中文 · 聆聽：主旨",
         explanation="說話人由郊野公園的風景講到遠足潮流，最後呼籲大家帶走垃圾、愛護山野。"),
    dict(stem=bilingual("根據短講，香港約有多少土地屬於郊野公園？", "根据短讲，香港约有多少土地属于郊野公园？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("約一成", "约一成")), ("B", bilingual("約四分之一", "约四分之一")),
                   ("C", bilingual("約四成", "约四成")), ("D", bilingual("約七成", "约七成"))),
         correct="C", strand="中文聆聽理解", concept="高中中文 · 聆聽：細節（數字）",
         explanation="說話人說「全港約四成的土地屬於郊野公園」；「四分之一」是形近的干擾項。"),
    dict(stem=bilingual("短講中「打卡」的意思是：", "短讲中“打卡”的意思是："), audio="listening-zh.m4a",
         options=O(("A", bilingual("上班時記錄出勤", "上班时记录出勤")), ("B", bilingual("購買入場門票", "购买入场门票")),
                   ("C", bilingual("在山上露營過夜", "在山上露营过夜")), ("D", bilingual("拍照留念並分享到網上", "拍照留念并分享到网上"))),
         correct="D", strand="中文聆聽理解", concept="高中中文 · 聆聽：詞語理解（流行用語）",
         explanation="說話人解釋：「打卡的意思，就是拍照留念，再分享到網上」；記錄出勤是這個詞的本義陷阱。"),
    dict(stem=bilingual("說話人對遠足成為潮流的態度是：", "说话人对远足成为潮流的态度是："), audio="listening-zh.m4a",
         options=O(("A", bilingual("完全反對", "完全反对")), ("B", bilingual("樂見其成，但提醒大家自律", "乐见其成，但提醒大家自律")),
                   ("C", bilingual("漠不關心", "漠不关心")), ("D", bilingual("覺得不可思議", "觉得不可思议"))),
         correct="B", strand="中文聆聽理解", concept="高中中文 · 聆聽：說話人態度",
         explanation="他說「多一個人親近山野，本來是好事」，同時提醒大家帶走垃圾，是歡迎之餘帶着叮嚀。"),
]

CH_SPEAKING = dict(
    type="speaking", maxSeconds=150,
    stem=bilingual("請用普通話介紹自己（大約兩分鐘）。", "请用普通话介绍自己（大约两分钟）。"),
    body=zh_blocks("可以說一說：\n• 你的名字、年級和學校\n• 一個你最喜歡的科目，以及喜歡它的原因\n• 一次你和同學合作完成任務的經歷\n• 到了新學校，你最想嘗試的一件事",
                   "可以说一说：\n• 你的名字、年级和学校\n• 一个你最喜欢的科目，以及喜欢它的原因\n• 一次你和同学合作完成任务的经历\n• 到了新学校，你最想尝试的一件事"),
)

CONTENT = {
    "Verbal Reasoning": VERBAL,
    "Non-Verbal Reasoning": NONVERBAL,
    "Mathematics": MATHS,
    "Reading Comprehension": READING,
    "Listening": LISTENING,
    "Writing": CONTENT_WRITING,
    "Speaking": CONTENT_SPEAKING,
    "中文閱讀 Chinese Reading": CHINESE,
    "中文聆聽 Chinese Listening": CH_LISTENING,
    "中文口語 Chinese Speaking": CH_SPEAKING,
}
