# -*- coding: utf-8 -*-
"""HKS Baseline Assessment · Years 7-8 (current Y7-Y8 / G6-G7), version 2. 60 min core.

Parallel form of level-c: same section structure and timing as v1 with all-new
content. ISEE-style single and double-blank sentence completions, MAP-style
grammar/cloze, verbal logic, double-rule NVR, and Y6-Y7 maths with multi-step
story problems. Curriculum codes on every item.
"""
from figlib import *

BAND = "level-c"
BAND_LABEL = "Level C"
YEAR_SPAN = "Years 7-8"
YEARS = ["Year 7", "Year 8"]

SECTIONS = [
    {"name": "Verbal Reasoning", "minutes": 10},        # 20 Q at 30 s
    {"name": "Non-Verbal Reasoning", "minutes": 8},     # 16 Q at 30 s
    {"name": "Mathematics", "minutes": 15},             # 7 short + 8 story
    {"name": "Reading Comprehension", "minutes": 10},
    {"name": "Listening", "minutes": 6},                # 3 recordings, 10 Q
    {"name": "Writing", "minutes": 7},
    {"name": "Speaking", "minutes": 4},
    {"name": "中文閱讀 Chinese Reading", "minutes": 8, "opt": "chinese"},
    {"name": "中文聆聽 Chinese Listening", "minutes": 4, "opt": "chinese"},
    {"name": "中文口語 Chinese Speaking", "minutes": 3, "opt": "chspeak"},
]

INFO = {
    "Verbal Reasoning": "This section tests vocabulary, word relationships, sentence completion, grammar and verbal logic. Work quickly; you have about half a minute per question.",
    "Non-Verbal Reasoning": "This section uses figures. In classification questions, three figures share a rule: choose the answer figure that follows the same rule. In matrix questions, work out how the figures change across the grid and choose the one that completes it. About half a minute per question.",
    "Mathematics": "Read each question carefully and choose the best answer. The later questions are longer story problems with several steps. You may use rough paper, but no calculator.",
    "Reading Comprehension": "Read each passage carefully, then answer the questions. The passage is shown with every question, so you can always re-read it.",
    "Listening": "There are three short recordings: an announcement, a conversation and a sports report. You may play each one up to two times. Answer the questions about each recording before moving on.",
    "Writing": "You will see two writing tasks. Choose ONE and type your answer. Aim for about 130-180 words: plan briefly, organise your ideas into paragraphs, and check your accuracy.",
    "Speaking": "In this final section you will record a short audio response. Find a quiet spot, allow microphone access when your browser asks, and speak clearly and naturally.",
    "中文聆聽 Chinese Listening": zh_blocks("現在是普通話聆聽部分。請按播放鍵，細心聆聽對話，每段錄音最多可以播放兩次。", "现在是普通话聆听部分。请按播放键，细心聆听对话，每段录音最多可以播放两次。"),
    "中文口語 Chinese Speaking": zh_blocks("請用普通話錄一段自我介紹。找一個安靜的地方，說話清楚自然。", "请用普通话录一段自我介绍。找一个安静的地方，说话清楚自然。"),
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

# ---- Verbal Reasoning (20) --------------------------------------------------
VERBAL = [
    dict(stem=_SYN + "\n\nPERPLEXED", options=O(("A", "certain"), ("B", "confused"), ("C", "annoyed"), ("D", "delighted")),
         correct="B", strand="Vocabulary: Synonyms", concept="Y7-8 Vocabulary · synonyms: perplexed = confused",
         explanation="Perplexed means puzzled or confused. Certain is closer to the opposite."),
    dict(stem=_SYN + "\n\nCOLOSSAL", options=O(("A", "tiny"), ("B", "ancient"), ("C", "heavy"), ("D", "enormous")),
         correct="D", strand="Vocabulary: Synonyms", concept="Y7-8 Vocabulary · synonyms: colossal = enormous",
         explanation="Colossal means extremely large: enormous. Tiny is the opposite, and heavy confuses size with weight."),
    dict(stem=_SYN + "\n\nGENUINE", options=O(("A", "authentic"), ("B", "fake"), ("C", "generous"), ("D", "polite")),
         correct="A", strand="Vocabulary: Synonyms", concept="Y7-8 Vocabulary · synonyms: genuine = authentic",
         explanation="Genuine means real, not an imitation: authentic. Fake is the opposite."),
    dict(stem=_ANT + "\n\nASCEND", options=O(("A", "climb"), ("B", "wander"), ("C", "descend"), ("D", "arrive")),
         correct="C", strand="Vocabulary: Antonyms", concept="Y7-8 Vocabulary · antonyms: ascend vs descend",
         explanation="To ascend is to go up; to descend is to go down. Climb is a synonym of ascend, not its opposite."),
    dict(stem=_ANT + "\n\nVAGUE", options=O(("A", "unclear"), ("B", "gentle"), ("C", "hollow"), ("D", "precise")),
         correct="D", strand="Vocabulary: Antonyms", concept="Y7-8 Vocabulary · antonyms: vague vs precise",
         explanation="Vague means not clearly expressed; precise means exact and clear. Unclear is a synonym of vague, not its opposite."),
    dict(stem=_ANT + "\n\nGRACEFUL", options=O(("A", "clumsy"), ("B", "elegant"), ("C", "cheerful"), ("D", "slender")),
         correct="A", strand="Vocabulary: Antonyms", concept="Y7-8 Vocabulary · antonyms: graceful vs clumsy",
         explanation="Graceful means moving smoothly and elegantly; clumsy means awkward. Elegant is a synonym of graceful, not its opposite."),
    dict(stem=_ANA + "\n\nThermometer is to temperature as scales are to ______.",
         options=O(("A", "kitchen"), ("B", "heavy"), ("C", "weight"), ("D", "metal")),
         correct="C", strand="Verbal Analogies", concept="Y7-8 Verbal Reasoning · analogies: instrument to what it measures",
         explanation="A thermometer measures temperature; scales measure weight. 'Heavy' describes a result, not the quantity measured."),
    dict(stem=_ANA + "\n\nCub is to bear as foal is to ______.",
         options=O(("A", "goat"), ("B", "horse"), ("C", "stable"), ("D", "colt")),
         correct="B", strand="Verbal Analogies", concept="Y7-8 Verbal Reasoning · analogies: young animal to adult animal",
         explanation="A cub is a young bear; a foal is a young horse. A colt is another word for a young horse, not the adult."),
    dict(stem=_ANA + "\n\nBee is to hive as spider is to ______.",
         options=O(("A", "web"), ("B", "insect"), ("C", "silk"), ("D", "fly")),
         correct="A", strand="Verbal Analogies", concept="Y7-8 Verbal Reasoning · analogies: creature to the home it builds",
         explanation="A bee lives in the hive it helps build; a spider lives in its web. Silk is the material, not the structure."),
    dict(stem=_ANA + "\n\nWhisper is to shout as glance is to ______.",
         options=O(("A", "blink"), ("B", "eye"), ("C", "wink"), ("D", "stare")),
         correct="D", strand="Verbal Analogies", concept="Y7-8 Verbal Reasoning · analogies: weak form to strong form",
         explanation="A whisper is a quiet, brief version of a shout; a glance is a quick, light version of a stare."),
    dict(stem=_SC + "\n\nAlthough the instructions seemed ______ at first, they became clear once we followed them step by step.",
         options=O(("A", "simple"), ("B", "baffling"), ("C", "helpful"), ("D", "brief")),
         correct="B", strand="Sentence Completion", concept="Y7-8 Reading · sentence completion: contrast signal 'although' (ISEE style)",
         explanation="'Although' sets up a contrast with 'became clear', so the instructions first seemed confusing: baffling."),
    dict(stem=_SC + "\n\nEngineers designed the new bridge to ______ even the strongest typhoon winds.",
         options=O(("A", "attract"), ("B", "create"), ("C", "withstand"), ("D", "predict")),
         correct="C", strand="Sentence Completion", concept="Y7-8 Reading · sentence completion: purpose clue (ISEE style)",
         explanation="A bridge must survive strong winds without failing: withstand them."),
    dict(stem=_SC2 + "\n\nThe critics ______ the film, but audiences ______ it, packing cinemas for weeks.",
         options=O(("A", "dismissed … adored"), ("B", "praised … avoided"), ("C", "ignored … forgot"), ("D", "admired … enjoyed")),
         correct="A", strand="Sentence Completion", concept="Y7-8 Reading · double-blank sentence completion with contrast (ISEE style)",
         explanation="'But' plus packed cinemas needs a contrast: critics dismissed it while audiences adored it. 'Admired … enjoyed' has no contrast, and 'praised … avoided' contradicts the full cinemas."),
    dict(stem=_SC2 + "\n\nBecause the witnesses' accounts were ______, the jury struggled to reach a ______ verdict.",
         options=O(("A", "identical … swift"), ("B", "clear … fair"), ("C", "contradictory … unanimous"), ("D", "detailed … written")),
         correct="C", strand="Sentence Completion", concept="Y7-8 Reading · double-blank with cause-effect signal (ISEE style)",
         explanation="'Because' plus 'struggled' needs a cause of difficulty: contradictory accounts make a unanimous verdict hard. Identical or clear accounts would make it easy."),
    dict(stem=_GR + "\n\nNeither of the twins ______ willing to admit the mistake.",
         options=O(("A", "were"), ("B", "was"), ("C", "are"), ("D", "being")),
         correct="B", strand="Grammar & Cloze", concept="Y7 Grammar · subject-verb agreement: 'neither of' takes a singular verb",
         explanation="The subject is 'neither', which is singular: neither WAS willing."),
    dict(stem=_GR + "\n\nIf it rains tomorrow, the sports day ______ to next week.",
         options=O(("A", "will be postponed"), ("B", "postponed"), ("C", "is postponing"), ("D", "has postponed")),
         correct="A", strand="Grammar & Cloze", concept="Y7 Grammar · first conditional with a passive result clause",
         explanation="A real future condition takes 'will' in the result, and the sports day is postponed BY someone, so the passive 'will be postponed' is needed."),
    dict(stem=_GR + "\n\nShe has lived in Hong Kong ______ 2019.",
         options=O(("A", "for"), ("B", "during"), ("C", "from"), ("D", "since")),
         correct="D", strand="Grammar & Cloze", concept="Y7 Grammar · present perfect with 'since' + a starting point",
         explanation="With the present perfect, a starting point in time takes 'since'. 'For' would need a length of time, such as 'for six years'."),
    dict(stem=_GR + "\n\nThe museum, ______ opened last spring, has already welcomed a million visitors.",
         options=O(("A", "that"), ("B", "which"), ("C", "what"), ("D", "who")),
         correct="B", strand="Grammar & Cloze", concept="Y8 Grammar · non-defining relative clause takes 'which'",
         explanation="A clause between commas adding extra information needs 'which'; 'that' cannot follow a comma in this way."),
    dict(stem=_LG + "\n\nNo reptiles are warm-blooded. All snakes are reptiles. Which statement MUST be true?",
         options=O(("A", "All reptiles are snakes"), ("B", "Some snakes are warm-blooded"),
                   ("C", "No snakes are warm-blooded"), ("D", "All cold-blooded animals are snakes")),
         correct="C", strand="Verbal Logic", concept="Y7-8 Reasoning · syllogism: what must follow",
         explanation="Every snake is a reptile, and no reptile is warm-blooded, so no snake can be warm-blooded. The other statements go beyond the information given."),
    dict(stem=_LG + "\n\nIn a spelling contest, Ada scores higher than Ben. Cleo scores lower than Ben but higher than Dev. Who has the SECOND LOWEST score?",
         options=O(("A", "Ada"), ("B", "Ben"), ("C", "Dev"), ("D", "Cleo")),
         correct="D", strand="Verbal Logic", concept="Y7-8 Reasoning · ordering deduction",
         explanation="The order from highest is Ada, Ben, Cleo, Dev. Dev is lowest, so Cleo has the second lowest score."),
]

# ---- Non-Verbal Reasoning (16 = 12 CAT4-engine + 4 GL-style) ----------------
_SEQ = "Look at the four pictures in the top row. Work out the pattern, then choose the picture (A-E) that belongs in the empty box."
_CODE = "Each picture on the left has a two-letter code. Work out what each letter stands for, then choose the code for the picture marked '?'."

def _row(fn, n, r, fill=INK):
    return lambda cx, cy: "".join(fn(cx + dx, cy + dy, r, fill) for dx, dy in
                                  {1: [(0, 0)], 2: [(-11, 0), (11, 0)], 3: [(-15, 0), (0, 0), (15, 0)],
                                   4: [(-11, -11), (11, -11), (-11, 11), (11, 11)],
                                   5: [(-15, -11), (0, -11), (15, -11), (-8, 11), (8, 11)]}[n])

NONVERBAL = nvr_from_json("level-c", 2) + [
    dict(stem=_SEQ, correct="D", strand="Figure Series (GL style)",
         concept="Y7-8 Non-Verbal Reasoning (GL 11+ series style) · two rules: quarter-turn clockwise AND the square shrinks",
         explanation="Two rules run together: the shaded half makes a quarter turn clockwise each step (left, top, right, bottom) and the square gets smaller each step. Next comes the smallest square with the LEFT half shaded again.",
         fig=seq_fig([cell(halfsquare, 20, 0), cell(halfsquare, 17, 90), cell(halfsquare, 14, 180), cell(halfsquare, 11, 270)],
                     [cell(halfsquare, 8, 90), cell(halfsquare, 8, 270), cell(halfsquare, 11, 0),
                      cell(halfsquare, 8, 0), cell(halfsquare, 8, 180)])),
    dict(stem=_SEQ, correct="C", strand="Figure Series (GL style)",
         concept="Y7-8 Non-Verbal Reasoning (GL 11+ series style) · two rules: the count falls by one AND shading alternates",
         explanation="Two rules run together: the number of triangles falls 5, 4, 3, 2 and the shading alternates black, white, black, white. The fifth picture must be ONE BLACK triangle.",
         fig=seq_fig([_row(triangle, 5, 6), _row(triangle, 4, 7, "none"), _row(triangle, 3, 7), _row(triangle, 2, 8, "none")],
                     [_row(triangle, 1, 8, "none"), _row(triangle, 2, 8), _row(triangle, 1, 8),
                      _row(triangle, 3, 7, "none"), _row(triangle, 2, 8, "none")])),
    dict(stem=_CODE, correct="B", strand="Figure Codes (GL style)",
         concept="Y7-8 Non-Verbal Reasoning (GL/CEM codes style) · first letter = shading, second letter = direction",
         explanation="J means black and K means white; R means pointing right and D means pointing down. The mystery arrow is WHITE and points DOWN: KD.",
         fig=codes_fig([(cell(arrow, 32, 0), "JR"), (cell(arrow, 32, 0, "none"), "KR"), (cell(arrow, 32, 90), "JD")],
                       cell(arrow, 32, 90, "none")),
         options=O(("A", "JR"), ("B", "KD"), ("C", "JD"), ("D", "KR"), ("E", "LD"))),
    dict(stem=_CODE, correct="E", strand="Figure Codes (GL style)",
         concept="Y7-8 Non-Verbal Reasoning (GL/CEM codes style) · first letter = shape, second letter = how many",
         explanation="V means circles and W means squares; M means two and N means three. The mystery picture shows THREE SQUARES: WN.",
         fig=codes_fig([(counted(circle, 2, 7), "VM"), (counted(circle, 3, 7), "VN"), (counted(square, 2, 7), "WM")],
                       counted(square, 3, 7)),
         options=O(("A", "VN"), ("B", "WM"), ("C", "VM"), ("D", "XN"), ("E", "WN"))),
]

# ---- Mathematics (15: 7 short incl. 2 quantitative comparisons + 8 story) ---
_QC = ("Compare Quantity A and Quantity B, then choose:\n"
       "A) Quantity A is greater   B) Quantity B is greater\n"
       "C) The two quantities are equal   D) It cannot be determined from the information given\n\n")
_QC_OPTS = O(("A", "Quantity A is greater"), ("B", "Quantity B is greater"),
             ("C", "The two quantities are equal"), ("D", "It cannot be determined"))

MATHS = [
    # short form
    dict(stem="Work out 24 ÷ (2 + 4) × 3",
         options=O(("A", "4"), ("B", "12"), ("C", "18"), ("D", "48")),
         correct="B", strand="Number", concept="Y6 Number · order of operations with brackets",
         explanation="Brackets first: 2 + 4 = 6, then 24 ÷ 6 = 4, then 4 × 3 = 12. 4 comes from stopping after the division, and 48 comes from ignoring the brackets and working left to right."),
    dict(stem="Work out −4 − 9",
         options=O(("A", "−13"), ("B", "−5"), ("C", "5"), ("D", "13")),
         correct="A", strand="Number", concept="Y7 Number · subtracting from a negative number",
         explanation="Start at −4 and count down another 9: the answer is −13. −5 comes from working out 4 − 9 and keeping only one sign."),
    dict(stem="Work out 1/2 + 2/5",
         options=O(("A", "1/10"), ("B", "3/7"), ("C", "7/10"), ("D", "9/10")),
         correct="D", strand="Fractions & Percentages", concept="Y6 Fractions · adding fractions with different denominators",
         explanation="Use tenths: 5/10 + 4/10 = 9/10. 3/7 comes from adding tops and bottoms, and 7/10 comes from converting only one of the fractions."),
    dict(stem="Increase 80 by 35%.",
         options=O(("A", "28"), ("B", "52"), ("C", "108"), ("D", "115")),
         correct="C", strand="Fractions & Percentages", concept="Y7 Percentages · percentage increase",
         explanation="35% of 80 is 28, so the increased amount is 80 + 28 = 108. 28 is the increase alone, 52 is a DECREASE, and 115 adds 35 instead of 35%."),
    dict(stem="Solve 5x − 7 = 3x + 9",
         options=O(("A", "x = 1"), ("B", "x = 2"), ("C", "x = 8"), ("D", "x = 16")),
         correct="C", strand="Algebra", concept="Y7 Algebra · linear equation with x on both sides",
         explanation="5x − 3x = 9 + 7 gives 2x = 16, so x = 8. x = 2 comes from wrongly collecting to 8x = 16, and x = 16 forgets the final division by 2."),
    dict(stem=_QC + "Quantity A: 25% of 120\nQuantity B: one third of 96",
         options=_QC_OPTS,
         correct="B", strand="Quantitative Comparison", concept="Y7 Fractions & Percentages · quantitative comparison (ISEE style)",
         explanation="Quantity A: 25% of 120 = 30. Quantity B: 96 ÷ 3 = 32. Quantity B is greater."),
    dict(stem=_QC + "n is a whole number greater than 1.\n\nQuantity A: 2n\nQuantity B: n²",
         options=_QC_OPTS,
         correct="D", strand="Quantitative Comparison", concept="Y7 Algebra · testing cases, quantitative comparison (ISEE style)",
         explanation="Try n = 2: 2n = 4 and n² = 4, so they are equal. Try n = 3: 2n = 6 and n² = 9, so B is greater. Different values give different answers, so it cannot be determined."),
    # story form
    dict(stem="After a 20% price rise, a video game costs HK$288. What did the game cost BEFORE the rise?",
         options=O(("A", "HK$230.40"), ("B", "HK$240"), ("C", "HK$268"), ("D", "HK$345.60")),
         correct="B", strand="Problem Solving", concept="Y8 Percentages · reverse percentage (finding the original amount)",
         explanation="The new price is 120% of the original, so the original is 288 ÷ 1.2 = HK$240. HK$230.40 wrongly takes 20% OFF the new price, and HK$268 just subtracts 20 dollars."),
    dict(stem="After four tests, Priya's mean score is 73. What must she score on her fifth test to make her mean for all five tests exactly 75?",
         options=O(("A", "75"), ("B", "77"), ("C", "83"), ("D", "85")),
         correct="C", strand="Problem Solving", concept="Y7 Statistics · adjusting a mean (working with totals)",
         explanation="Five tests at a mean of 75 need a total of 375. Her four tests total 4 × 73 = 292, so she needs 375 − 292 = 83. Scoring 75 (the target mean itself) would leave her mean below 75."),
    dict(stem="A coach travels 90 km in 1 hour 15 minutes. What is its average speed in kilometres per hour?",
         options=O(("A", "72 km/h"), ("B", "75 km/h"), ("C", "90 km/h"), ("D", "112.5 km/h")),
         correct="A", strand="Problem Solving", concept="Y8 Measures · speed = distance divided by time",
         explanation="1 hour 15 minutes is 1.25 hours, and 90 ÷ 1.25 = 72 km/h. 90 just repeats the distance, and 112.5 multiplies by 1.25 instead of dividing."),
    dict(stem="The bar chart shows the rainfall recorded each month. What is the MEDIAN monthly rainfall?",
         fig=bar_chart(["Jan", "Feb", "Mar", "Apr", "May"], [20, 50, 30, 60, 45], 60, 5, unit="mm"),
         options=O(("A", "30 mm"), ("B", "40 mm"), ("C", "41 mm"), ("D", "45 mm")),
         correct="D", strand="Problem Solving", concept="Y7 Statistics · reading a chart, then finding the median (values must be ordered first)",
         explanation="Ordered, the values are 20, 30, 45, 50, 60, so the middle value is 45 mm. 30 mm is the middle bar as drawn (unordered), and 41 mm is the mean, not the median."),
    dict(stem="The spinner has 8 equal sectors. Zara spins it 40 times. How many times should she EXPECT it to land on G?",
         fig=spinner([("R", 3, "#e3a498"), ("B", 4, "#72AFDB"), ("G", 1, "#b9d8a2")]),
         options=O(("A", "5"), ("B", "8"), ("C", "13"), ("D", "20")),
         correct="A", strand="Problem Solving", concept="Y8 Probability · expected frequency = probability × number of trials",
         explanation="P(G) = 1/8, so expect 40 × 1/8 = 5. 8 is the number of sectors, 13 shares the 40 spins equally among the three letters, and 20 is half the spins."),
    dict(stem="The line graph shows the number of visitors inside a country park at different times. Between which two times did the number of visitors increase the FASTEST?",
         fig=line_graph(["06:00", "09:00", "12:00", "15:00", "18:00"], [10, 20, 25, 45, 40], 50, 10, unit="visitors"),
         options=O(("A", "Between 06:00 and 09:00"), ("B", "Between 09:00 and 12:00"),
                   ("C", "Between 12:00 and 15:00"), ("D", "Between 15:00 and 18:00")),
         correct="C", strand="Problem Solving", concept="Y7 Statistics · interpreting a line graph (steepest rise = fastest increase)",
         explanation="The rises are +10, +5, +20 and then a FALL of 5. The steepest climb, +20, is between 12:00 and 15:00. The 15:00 to 18:00 section changes quickly but goes DOWN."),
    dict(stem="Mortar is mixed from cement and sand in the ratio 2 : 7. A builder uses 6 kg of cement. How much sand does he need?",
         options=O(("A", "11 kg"), ("B", "21 kg"), ("C", "27 kg"), ("D", "42 kg")),
         correct="B", strand="Problem Solving", concept="Y7 Ratio · scaling one part of a ratio",
         explanation="6 kg of cement is 3 times the '2', so the sand is 3 × 7 = 21 kg. 11 kg treats the ratio as 'add 5', 27 kg is the TOTAL mix, and 42 kg multiplies 6 by 7."),
    dict(stem="Cinema tickets cost HK$95 for an adult and HK$55 for a child. A family of 2 adults and 3 children pays with a HK$400 note. How much change do they get?",
         options=O(("A", "HK$45"), ("B", "HK$100"), ("C", "HK$150"), ("D", "HK$355")),
         correct="A", strand="Problem Solving", concept="Y7 Number · multi-step money problem (multiply, add, then subtract)",
         explanation="Adults: 2 × 95 = 190. Children: 3 × 55 = 165. Total 355, so the change is 400 − 355 = HK$45. HK$100 counts only 2 children, and HK$355 gives the total cost instead of the change."),
]

# ---- Reading Comprehension (10) --------------------------------------------
PASSAGE_1 = (
    "<strong>The Understudy</strong><br><br>"
    "For six weeks, Talia had learned every line of the play from the second row of the rehearsal room. "
    "She was the understudy: the just-in-case, the spare key nobody expects to use. The lead role of the "
    "Storm Queen belonged to Vivienne, who had a voice like a bell and a framed poster of herself from "
    "last year's show.<br><br>"
    "Talia mouthed the words each night anyway, at the bus stop, in the shower, until the corners of her "
    "script went as soft as cloth. Her brother teased her for rehearsing a part she would never play. "
    "“Somebody guards the goal all season and never touches the ball,” she told him. “You don't laugh at him.”<br><br>"
    "On the afternoon of the performance, Ms Odaro found Talia by the costume rail. Vivienne had lost her "
    "voice entirely; the doctor had ordered two full days of silence. “The role is yours tonight,” said "
    "Ms Odaro, “if you want it.” The room tilted slightly. There were four hundred seats in the hall, and "
    "Talia's mind sat a stranger in every single one of them.<br><br>"
    "What happened next surprised her. In the wings, in the itchy silver cloak, with her heart drumming its "
    "warning, Talia felt the six quiet weeks rise up beneath her like water lifting a boat. She knew where "
    "every pause lived. She knew which line came after the thunder, and how long to hold the silence before "
    "the final storm.<br><br>"
    "When the curtain fell, the applause was long and real. Vivienne stood at the side of the stage clapping "
    "too, mouthing “you were brilliant” with her doctor-forbidden voice. Later, at home, Talia's brother "
    "asked what it had felt like out there. She thought about it properly, the way she now thought about most "
    "things. “Like being the goalkeeper,” she said, “on the one night the shots finally came.”"
)

PASSAGE_2 = (
    "<strong>The Dance That Draws a Map</strong><br><br>"
    "A honeybee returning from a rich patch of flowers has a problem: how can she tell thousands of "
    "nestmates where to go, in the darkness of a crowded hive? Her solution is one of the strangest "
    "languages in nature. She dances.<br><br>"
    "The returning bee walks in a straight line across the honeycomb, waggling her body rapidly from side "
    "to side, then circles back and repeats the run, again and again. Other bees crowd around in the dark, "
    "touching her with their antennae, reading the message with their bodies rather than their eyes.<br><br>"
    "The dance is astonishingly precise. The direction of the waggle run tells the others which way to fly: "
    "a run straight upwards on the comb means “fly towards the sun”, while a run angled forty degrees to "
    "the left means “fly forty degrees to the left of the sun”. The length of the run signals the distance: "
    "roughly, the longer the waggle, the further the flowers. Quality matters too. The richer the nectar the "
    "bee has found, the longer and more energetically she dances, recruiting more and more followers to "
    "her discovery.<br><br>"
    "The Austrian scientist Karl von Frisch spent decades decoding this behaviour, patiently marking "
    "individual bees with dots of paint and recording where they flew. His work earned a Nobel Prize in "
    "1973. At first, some scientists refused to believe him: the idea that an insect with a brain smaller "
    "than a grain of rice could communicate compass directions seemed impossible. Later experiments, "
    "including some that used tiny robotic bees, confirmed the essentials of his map.<br><br>"
    "It is worth pausing on what the waggle dance really is: a symbol standing for something far away. The "
    "dance is not the flowers, any more than the word “dinner” is a meal. That is what makes it so "
    "remarkable, and why some researchers describe it, carefully and with caveats, as the closest thing to "
    "a true language outside humankind."
)

_RC = "Y7-8 Reading · "
READING = [
    dict(passage=PASSAGE_1, stem="Talia is called “the spare key nobody expects to use”. What does this comparison tell us about being an understudy?",
         options=O(("A", "The school kept losing the keys to the rehearsal room"),
                   ("B", "Talia was often forgetful and unprepared"),
                   ("C", "An understudy must be ready, but is only needed if something goes wrong"),
                   ("D", "Talia was locked out of the performance")),
         correct="C", strand="Reading: Fiction", concept=_RC + "interpreting a figurative comparison",
         explanation="A spare key is kept ready but only used in an emergency; an understudy is prepared for a role she may never perform."),
    dict(passage=PASSAGE_1, stem="Why does Talia mention the goalkeeper to her brother?",
         options=O(("A", "To show that preparing seriously matters, even if you are never called on"),
                   ("B", "To prove she prefers football to acting"),
                   ("C", "Because her brother is a goalkeeper"),
                   ("D", "To explain why she wants to quit the play")),
         correct="A", strand="Reading: Fiction", concept=_RC + "inference: understanding a character's argument",
         explanation="Her point is that a goalkeeper trains all season even if the shots never come, just as she rehearses a part she may never play."),
    dict(passage=PASSAGE_1, stem="“The room tilted slightly.” What does this description show?",
         options=O(("A", "The costume rail had fallen over"),
                   ("B", "The school hall was badly built"),
                   ("C", "Ms Odaro was leaning towards her"),
                   ("D", "Talia felt a sudden rush of shock and nerves")),
         correct="D", strand="Reading: Fiction", concept=_RC + "interpreting figurative description of emotion",
         explanation="The room does not really move; the sentence shows how the shocking news made the moment feel from inside."),
    dict(passage=PASSAGE_1, stem="The six weeks “rise up beneath her like water lifting a boat”. What does this image suggest?",
         options=O(("A", "Talia felt she was drowning in fear"),
                   ("B", "All her quiet preparation now carried and supported her"),
                   ("C", "The stage had been flooded before the show"),
                   ("D", "She wished she were sailing instead of acting")),
         correct="B", strand="Reading: Fiction", concept=_RC + "interpreting a simile",
         explanation="Water lifting a boat supports it; in the same way, her weeks of rehearsal held her up when she finally performed."),
    dict(passage=PASSAGE_1, stem="What does Talia mean by “the one night the shots finally came”?",
         options=O(("A", "The night finally tested everything she had practised for"),
                   ("B", "She wished she had played football that evening"),
                   ("C", "She blamed Vivienne for falling ill"),
                   ("D", "The performance went badly wrong")),
         correct="A", strand="Reading: Fiction", concept=_RC + "interpreting the closing metaphor",
         explanation="Returning to her goalkeeper comparison, she means her long, unseen preparation was at last called on, and it held."),
    dict(passage=PASSAGE_2, stem="What is the main purpose of this passage?",
         options=O(("A", "To warn that honeybees are disappearing"),
                   ("B", "To explain how honeybees communicate through the waggle dance"),
                   ("C", "To describe how honey is made in the hive"),
                   ("D", "To argue that robots should replace scientists")),
         correct="B", strand="Reading: Non-fiction", concept=_RC + "identifying the main purpose",
         explanation="The passage explains what the dance is, what its direction and length mean, and how it was decoded."),
    dict(passage=PASSAGE_2, stem="According to the passage, what does the DIRECTION of the waggle run tell the other bees?",
         options=O(("A", "How sweet the nectar is"), ("B", "How far away the flowers are"),
                   ("C", "How many bees should fly out"), ("D", "Which way to fly, relative to the sun")),
         correct="D", strand="Reading: Non-fiction", concept=_RC + "locating a stated detail (direction vs distance)",
         explanation="The direction of the run gives the direction of flight relative to the sun; it is the LENGTH of the run that signals distance."),
    dict(passage=PASSAGE_2, stem="Why does the writer mention the experiments with tiny robotic bees?",
         options=O(("A", "To suggest real bees may soon be replaced"),
                   ("B", "To show that scientists enjoy building machines"),
                   ("C", "To show that later evidence confirmed von Frisch's findings"),
                   ("D", "To prove the dance is impossible to study")),
         correct="C", strand="Reading: Non-fiction", concept=_RC + "understanding the function of evidence",
         explanation="The robotic-bee experiments are given as later confirmation of the dance map that some scientists had doubted."),
    dict(passage=PASSAGE_2, stem="In the passage, “recruiting more and more followers” most nearly means:",
         options=O(("A", "attracting more bees to join the trip to the flowers"),
                   ("B", "hiring worker bees for the queen"),
                   ("C", "pushing other bees out of the hive"),
                   ("D", "teaching young bees to dance")),
         correct="A", strand="Reading: Non-fiction", concept=_RC + "vocabulary in context: 'recruiting'",
         explanation="A longer, livelier dance persuades more nestmates to fly out to the flowers she found; 'recruiting' here means winning them over to join."),
    dict(passage=PASSAGE_2, stem="Which statement best describes the writer's position in the final paragraph?",
         options=O(("A", "The dance proves bees talk exactly as humans do"),
                   ("B", "Von Frisch's Nobel Prize was undeserved"),
                   ("C", "The dance is interesting but not really communication"),
                   ("D", "The dance is remarkable, though calling it a language needs caution")),
         correct="D", strand="Reading: Non-fiction", concept=_RC + "identifying a nuanced position",
         explanation="The writer is clearly impressed, but notes the language comparison is made 'carefully and with caveats': admiration with caution, not a claim that bees talk like humans."),
]

# ---- Listening (3 recordings, 10 Q) ----------------------------------------
_LI = "Listen to the recording, then choose the best answer."
_A1, _A2, _A3 = "listening1.m4a", "listening2.m4a", "listening3.m4a"

AUDIO_TITLES = {
    "listening1.m4a": "Sports Day Moves Indoors",
    "listening2.m4a": "Planning the Charity Stall",
    "listening3.m4a": "Robotics Team Report",
    "listening-zh.m4a": "合買禮物 Buying a Gift",
}

AUDIO = {
    "listening-zh.m4a": [("zh-CN-XiaoxiaoNeural", "-10%", "小杰，下个星期三是小华的生日，我们一起给她买份礼物，好吗？"),
        ("zh-CN-YunxiNeural", "-10%", "好啊。她最近一直说想要那套漫画的最后一册。"),
        ("zh-CN-XiaoxiaoNeural", "-10%", "那我们星期天下午两点，在商场正门见面，先去三楼的书店看看。"),
        ("zh-CN-YunxiNeural", "-10%", "行。我们每人出五十块，够吗？"),
        ("zh-CN-XiaoxiaoNeural", "-10%", "应该够了。对了，要是书店把那套漫画卖完了，我们就去旁边的文具店，给她买一套彩色笔。"),
        ("zh-CN-YunxiNeural", "-10%", "没问题，星期天见！")],
    _A1: [("en-GB-ThomasNeural", "-6%",
        "Good morning, everyone. Here are the arrangements for Sports Day this Friday. "
        "Because the running track is being resurfaced, all events will take place at the indoor "
        "sports arena on Wing On Road instead of the school field. "
        "Buses leave from the main gate at eight fifteen, and the first race starts at nine o'clock sharp. "
        "Please wear your house T-shirt: red for Phoenix, yellow for Dragon, and green for Lion. "
        "The water fountains at the arena are out of order, so every student must bring a filled water bottle. "
        "Finally, parents are very welcome to watch, but they must collect a visitor sticker at the arena entrance.")],
    _A2: [
        ("en-GB-MaisieNeural", "-6%", "Ryan, we still need to decide what our class stall will sell at the charity fair."),
        ("en-GB-RyanNeural", "-6%", "I thought we'd agreed on a bake sale?"),
        ("en-GB-MaisieNeural", "-6%", "That was the plan, but three other classes have already signed up to sell cakes. "
                          "We would all be competing for the same customers."),
        ("en-GB-RyanNeural", "-6%", "Fair point. What about a second-hand book stall? Everyone has books at home "
                        "they've finished with."),
        ("en-GB-MaisieNeural", "-6%", "I like it. My cousin ran one at her school last year and raised over eight hundred dollars."),
        ("en-GB-RyanNeural", "-6%", "Let's ask everyone to bring in books by Wednesday, then. Shall we meet to sort them "
                        "on Friday lunchtime, in our classroom?"),
        ("en-GB-MaisieNeural", "-6%", "Friday lunchtime works, but let's use the art room instead. The tables in there "
                          "are much bigger for sorting."),
        ("en-GB-RyanNeural", "-6%", "The art room it is. I'll bring sticky labels for the prices."),
    ],
    _A3: [("en-US-AvaNeural", "-6%",
        "Now for this week's news from the science department. Our senior robotics team took home "
        "the gold medal at the regional championships on Sunday, beating sixteen other schools. "
        "Their robot, nicknamed Turtle, sorted forty recycling items in under two minutes, "
        "the fastest time of the whole day. "
        "Team captain Anjali Rao said the win belonged to the entire team, who have met every Tuesday "
        "and Saturday since September to rebuild the robot's gripper. "
        "The team will now represent our region at the national finals in March. "
        "Come and see Turtle in action at Thursday's assembly.")],
}

LISTENING = [
    dict(stem=_LI + "\n\nWhy will Sports Day take place at the indoor arena?", audio=_A1,
         options=O(("A", "The school field is flooded"), ("B", "The running track is being resurfaced"),
                   ("C", "The arena is closer to the school"), ("D", "The weather forecast is bad")),
         correct="B", strand="Listening", concept="Y7-8 Listening · identifying the stated reason",
         explanation="The announcement says the running track is being resurfaced, so events move to the arena."),
    dict(stem=_LI + "\n\nWhat time do the buses leave the main gate?", audio=_A1,
         options=O(("A", "8:15"), ("B", "8:45"), ("C", "9:00"), ("D", "9:15")),
         correct="A", strand="Listening", concept="Y7-8 Listening · key time with a near-value trap (9:00 is the FIRST RACE, not the buses)",
         explanation="The buses leave at eight fifteen; nine o'clock is when the first race starts."),
    dict(stem=_LI + "\n\nWhy must every student bring a filled water bottle?", audio=_A1,
         options=O(("A", "The buses have no air conditioning"), ("B", "The canteen will be closed"),
                   ("C", "Drinks at the arena are expensive"), ("D", "The arena's water fountains are out of order")),
         correct="D", strand="Listening", concept="Y7-8 Listening · cause and instruction",
         explanation="Students must bring water because the arena's fountains are out of order."),
    dict(stem=_LI + "\n\nWhat must parents do at the arena?", audio=_A1,
         options=O(("A", "Stay in the school hall"), ("B", "Sign up by Friday"),
                   ("C", "Collect a visitor sticker at the entrance"), ("D", "Wear a house T-shirt")),
         correct="C", strand="Listening", concept="Y7-8 Listening · specific instruction for visitors",
         explanation="Parents are welcome but must collect a visitor sticker at the arena entrance. House T-shirts are for students."),
    dict(stem=_LI + "\n\nWhat will the class stall sell at the charity fair?", audio=_A2,
         options=O(("A", "Cakes"), ("B", "Second-hand books"),
                   ("C", "Sticky labels"), ("D", "Art supplies")),
         correct="B", strand="Listening", concept="Y7-8 Listening · outcome of a discussion; the bake sale is the REJECTED option trap",
         explanation="They drop the bake sale because three other classes are selling cakes, and settle on a second-hand book stall."),
    dict(stem=_LI + "\n\nWhy do the students give up the bake sale idea?", audio=_A2,
         options=O(("A", "Three other classes are already selling cakes"), ("B", "Baking costs too much"),
                   ("C", "The school has banned food stalls"), ("D", "Nobody in the class can bake")),
         correct="A", strand="Listening", concept="Y7-8 Listening · stated reason for rejecting an option",
         explanation="Maisie explains that three other classes have signed up to sell cakes, so they would all be competing."),
    dict(stem=_LI + "\n\nWhere will they meet on Friday lunchtime?", audio=_A2,
         options=O(("A", "In their classroom"), ("B", "In the library"),
                   ("C", "At the school gate"), ("D", "In the art room")),
         correct="D", strand="Listening", concept="Y7-8 Listening · arrangement detail with a near trap (the classroom was suggested first, then changed)",
         explanation="Ryan suggests their classroom, but Maisie switches the meeting to the art room for its bigger tables."),
    dict(stem=_LI + "\n\nWhat did the robotics team win on Sunday?", audio=_A3,
         options=O(("A", "Silver at the national finals"), ("B", "Gold at the national finals"),
                   ("C", "Gold at the regional championships"), ("D", "Second place out of sixteen")),
         correct="C", strand="Listening", concept="Y7-8 Listening · key detail (result); the NATIONAL finals are still to come",
         explanation="The team won gold at the regional championships; the national finals are in March."),
    dict(stem=_LI + "\n\nWhat did the robot Turtle do at the competition?", audio=_A3,
         options=O(("A", "Sorted forty recycling items in under two minutes"), ("B", "Sorted twenty items in four minutes"),
                   ("C", "Carried sixteen items across the hall"), ("D", "Rebuilt its own gripper")),
         correct="A", strand="Listening", concept="Y7-8 Listening · key figures with near-value traps (16 schools vs 40 items)",
         explanation="Turtle sorted forty recycling items in under two minutes, the fastest time of the day. Sixteen is the number of schools beaten."),
    dict(stem=_LI + "\n\nWhat does the team captain say the win was built on?", audio=_A3,
         options=O(("A", "A brand new robot bought by the school"), ("B", "The whole team's practice every Tuesday and Saturday"),
                   ("C", "Luck on the day"), ("D", "Help from another school")),
         correct="B", strand="Listening", concept="Y7-8 Listening · attributed opinion (the captain's explanation)",
         explanation="Captain Anjali Rao credits the entire team, who met every Tuesday and Saturday since September."),
]

# ---- Writing / Speaking / Chinese ------------------------------------------
CONTENT_WRITING = dict(
    type="writing",
    intro="Choose ONE of the two tasks below and type your answer in the box. Aim for about 130-180 words.",
    body=("Task 1: Write about a time you tried something for the first time even though you were nervous. "
          "Describe what happened and reflect honestly on what the experience taught you about yourself.\n\n"
          "Task 2: Some people believe every student should be required to join at least one sports team or club "
          "at school; others believe free time after lessons should belong to students. What is your view? "
          "Support your opinion with clear reasons and examples."),
    hint="Start by saying which task you chose. Plan for a minute, organise your ideas into paragraphs, and leave time to check your accuracy.",
    placeholder="Type your answer here; it will be saved for review…",
)

CONTENT_SPEAKING = dict(
    type="speaking",
    stem="Record a short spoken response (about 90-120 seconds).",
    body=("Speak about:\n"
          "• Your name, your current school and year group\n"
          "• A book, film or game that made you think, and what it made you think about\n"
          "• A time you worked with others to get something done, and the part you played\n"
          "• One thing you would like to try at your next school\n\n"
          "Speak naturally and take your time; there are no right answers, only your own."),
)

CH_PASSAGE_TRAD = (
    "我住的大廈有一位看更陳伯，在大堂那張舊木桌後面，一坐就是二十多年。桌上放着一本厚厚的簿子，誰家的包裹到了、"
    "誰家的水電師傅幾點上門，他都一筆一筆記下。放學回來，他常常隔着玻璃門提醒我：「你媽媽說今晚加班，記得先吃飯。」"
    "落雨之前，他總會把一桶雨傘放在大門口，讓忘記帶傘的街坊借用。\n\n"
    "有人說，大廈裝了智能閘機和攝影機，看更這一行遲早會被取代。陳伯聽了，只是笑一笑：機器認得住戶的臉，"
    "卻認不得誰最近搬了家、誰家的孩子病了。\n\n"
    "上個月陳伯六十五歲生日，信箱旁邊貼滿了住戶寫的心意卡。他把卡片一張一張小心收好，說這是他當看更以來，"
    "收過最貴重的「工資」。"
)
CH_PASSAGE_SIMP = (
    "我住的大厦有一位看更陈伯，在大堂那张旧木桌后面，一坐就是二十多年。桌上放着一本厚厚的簿子，谁家的包裹到了、"
    "谁家的水电师傅几点上门，他都一笔一笔记下。放学回来，他常常隔着玻璃门提醒我：“你妈妈说今晚加班，记得先吃饭。”"
    "落雨之前，他总会把一桶雨伞放在大门口，让忘记带伞的街坊借用。\n\n"
    "有人说，大厦装了智能闸机和摄影机，看更这一行迟早会被取代。陈伯听了，只是笑一笑：机器认得住户的脸，"
    "却认不得谁最近搬了家、谁家的孩子病了。\n\n"
    "上个月陈伯六十五岁生日，信箱旁边贴满了住户写的心意卡。他把卡片一张一张小心收好，说这是他当看更以来，"
    "收过最贵重的“工资”。"
)

def _ch(stem_t, stem_s, opts_ts, correct, concept, explanation):
    return dict(
        passage=zh_blocks(CH_PASSAGE_TRAD.replace("\n\n", "<br><br>"), CH_PASSAGE_SIMP.replace("\n\n", "<br><br>")),
        stem=bilingual(stem_t, stem_s),
        options=O(*[(k, bilingual(t, s)) for k, (t, s) in opts_ts.items()]),
        correct=correct, strand="中文閱讀理解", concept="初中中文 · " + concept, explanation=explanation)

CHINESE = [
    _ch("陳伯把包裹和師傅上門的時間都一筆一筆記在簿子上，這說明他：", "陈伯把包裹和师傅上门的时间都一笔一笔记在簿子上，这说明他：",
        {"A": ("喜歡寫作", "喜欢写作"), "B": ("做事細心，把住戶的事放在心上", "做事细心，把住户的事放在心上"),
         "C": ("記性不好，怕自己忘記", "记性不好，怕自己忘记"), "D": ("想向管理公司邀功", "想向管理公司邀功")},
        "B", "內容理解：人物特點", "簿子記的全是住戶的大小事，可見他細心盡責，把每家每戶都放在心上，並非為了表現自己。"),
    _ch("「你媽媽說今晚加班，記得先吃飯」這句話，說明陳伯與住戶的關係：", "“你妈妈说今晚加班，记得先吃饭”这句话，说明陈伯与住户的关系：",
        {"A": ("只在節日往來", "只在节日往来"), "B": ("經常發生爭執", "经常发生争执"),
         "C": ("互不相識", "互不相识"), "D": ("十分熟絡，互相信任", "十分熟络，互相信任")},
        "D", "內容理解：含意", "媽媽放心把口信交託陳伯轉達，陳伯又主動關心孩子吃飯，可見雙方熟絡而且互相信任。"),
    _ch("對「看更遲早會被取代」的說法，陳伯的態度是：", "对“看更迟早会被取代”的说法，陈伯的态度是：",
        {"A": ("十分憤怒", "十分愤怒"), "B": ("非常擔心", "非常担心"),
         "C": ("一笑置之，並不在意", "一笑置之，并不在意"), "D": ("決定提早退休", "决定提早退休")},
        "C", "內容理解：態度", "文中寫他「只是笑一笑」，因為他相信機器代替不了人與人之間的了解和關心。"),
    _ch("「機器認得住戶的臉，卻認不得誰最近搬了家」這句話的意思是：", "“机器认得住户的脸，却认不得谁最近搬了家”这句话的意思是：",
        {"A": ("機器沒有人情味，代替不了人與人之間的關心", "机器没有人情味，代替不了人与人之间的关心"), "B": ("攝影機的畫質不清楚", "摄影机的画质不清楚"),
         "C": ("陳伯不懂得使用機器", "陈伯不懂得使用机器"), "D": ("住戶不喜歡拍照", "住户不喜欢拍照")},
        "A", "修辭理解：對比作用", "一句之內把「認得臉」與「認不得人情世事」對比，突出機器只能辨認外表，做不到看更那份關心。"),
    _ch("文末「最貴重的『工資』」指的是：", "文末“最贵重的‘工资’”指的是：",
        {"A": ("加班費", "加班费"), "B": ("生日蛋糕", "生日蛋糕"),
         "C": ("住戶寫的心意卡", "住户写的心意卡"), "D": ("管理公司的獎金", "管理公司的奖金")},
        "C", "詞句理解：指代", "上文寫信箱旁貼滿住戶的心意卡，他把卡片小心收好，這些心意卡就是他所說最貴重的「工資」。"),
    _ch("這篇文章主要想表達：", "这篇文章主要想表达：",
        {"A": ("智能科技終會取代所有工作", "智能科技终会取代所有工作"),
         "B": ("平凡崗位上的人情味值得珍惜", "平凡岗位上的人情味值得珍惜"),
         "C": ("看更的工作十分輕鬆", "看更的工作十分轻松"), "D": ("大廈應該加裝更多攝影機", "大厦应该加装更多摄影机")},
        "B", "主旨理解", "全文寫陳伯的細心、住戶的信任和心意卡，帶出平凡崗位上人與人之間的情誼最可貴。"),
]

CH_LISTENING = [
    dict(stem=bilingual("聆聽對話，然後回答問題。\n\n他們為甚麼要買禮物？", "聆听对话，然后回答问题。\n\n他们为什么要买礼物？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("小華生病了", "小华生病了")), ("B", bilingual("小華快過生日", "小华快过生日")), ("C", bilingual("小華要轉校", "小华要转校")), ("D", bilingual("小華比賽得獎", "小华比赛得奖"))),
         correct="B", strand="中文聆聽理解", concept="初中中文 · 聆聽：目的",
         explanation="對話開頭說下星期三是小華的生日，所以他們要一起買禮物。"),
    dict(stem=bilingual("他們約在甚麼時間、甚麼地方見面？", "他们约在什么时间、什么地方见面？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("星期三下午兩點在商場正門", "星期三下午两点在商场正门")), ("B", bilingual("星期天下午兩點在書店門口", "星期天下午两点在书店门口")), ("C", bilingual("星期天下午三點在商場正門", "星期天下午三点在商场正门")), ("D", bilingual("星期天下午兩點在商場正門", "星期天下午两点在商场正门"))),
         correct="D", strand="中文聆聽理解", concept="初中中文 · 聆聽：時間與地點的組合（星期三是生日，不是見面日）",
         explanation="他們約星期天下午兩點在商場正門見面，再一起上三樓的書店。"),
    dict(stem=bilingual("每人打算出多少錢？", "每人打算出多少钱？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("五十元", "五十元")), ("B", bilingual("十五元", "十五元")), ("C", bilingual("一百元", "一百元")), ("D", bilingual("二十元", "二十元"))),
         correct="A", strand="中文聆聽理解", concept="初中中文 · 聆聽：數字細節",
         explanation="對話中說每人出五十塊。"),
    dict(stem=bilingual("如果書店把那套漫畫賣完了，他們會怎樣？", "如果书店把那套漫画卖完了，他们会怎样？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("改天再買", "改天再买")), ("B", bilingual("上網訂購", "上网订购")), ("C", bilingual("到旁邊的文具店買一套彩色筆", "到旁边的文具店买一套彩色笔")), ("D", bilingual("請小華自己挑選", "请小华自己挑选"))),
         correct="C", strand="中文聆聽理解", concept="初中中文 · 聆聽：條件安排（陷阱題）",
         explanation="如果漫畫賣完了，他們就到旁邊的文具店，改買一套彩色筆。"),
]

CH_SPEAKING = dict(
    type="speaking", maxSeconds=120,
    stem=bilingual("請用普通話介紹自己（大約90秒）。", "请用普通话介绍自己（大约90秒）。"),
    body=zh_blocks("可以說一說：\n• 你的名字、年級和學校\n• 你最喜歡的一項活動或運動\n• 一次你幫助別人的經歷\n• 你對新學校有甚麼期望",
                   "可以说一说：\n• 你的名字、年级和学校\n• 你最喜欢的一项活动或运动\n• 一次你帮助别人的经历\n• 你对新学校有什么期望"),
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
