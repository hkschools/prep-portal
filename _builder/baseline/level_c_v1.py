# -*- coding: utf-8 -*-
"""HKS Baseline Assessment · Years 7-8 (current Y7-Y8 / G6-G7), version 1. 60 min core.

Harder tier: ISEE-style single and double-blank sentence completions, MAP-style
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
    dict(stem=_SYN + "\n\nHASTY", options=O(("A", "careful"), ("B", "hurried"), ("C", "clumsy"), ("D", "brave")),
         correct="B", strand="Vocabulary: Synonyms", concept="Y7-8 Vocabulary · synonyms: hasty = hurried",
         explanation="Hasty means done quickly, in other words hurried. Careful is closer to the opposite."),
    dict(stem=_SYN + "\n\nVIGILANT", options=O(("A", "sleepy"), ("B", "violent"), ("C", "brave"), ("D", "watchful")),
         correct="D", strand="Vocabulary: Synonyms", concept="Y7-8 Vocabulary · synonyms: vigilant = watchful",
         explanation="Vigilant means keeping careful watch for danger: watchful. 'Violent' is a sound-alike trap and sleepy is closer to the opposite."),
    dict(stem=_SYN + "\n\nVIVID", options=O(("A", "dull"), ("B", "faint"), ("C", "striking"), ("D", "ordinary")),
         correct="C", strand="Vocabulary: Synonyms", concept="Y7-8 Vocabulary · synonyms: vivid = striking",
         explanation="A vivid description is bright, clear and striking. Dull and faint are opposites."),
    dict(stem=_ANT + "\n\nTIMID", options=O(("A", "bold"), ("B", "shy"), ("C", "quiet"), ("D", "small")),
         correct="A", strand="Vocabulary: Antonyms", concept="Y7-8 Vocabulary · antonyms: timid vs bold",
         explanation="Timid means lacking courage; bold means confident and daring. Shy is a synonym of timid, not its opposite."),
    dict(stem=_ANT + "\n\nTRANSPARENT", options=O(("A", "clear"), ("B", "shiny"), ("C", "opaque"), ("D", "fragile")),
         correct="C", strand="Vocabulary: Antonyms", concept="Y7-8 Vocabulary · antonyms: transparent vs opaque",
         explanation="Transparent means you can see through it; opaque means you cannot. Clear is a synonym, not an opposite."),
    dict(stem=_ANT + "\n\nHOSTILE", options=O(("A", "fierce"), ("B", "friendly"), ("C", "angry"), ("D", "distant")),
         correct="B", strand="Vocabulary: Antonyms", concept="Y7-8 Vocabulary · antonyms: hostile vs friendly",
         explanation="Hostile means unfriendly or aggressive, so the opposite is friendly. Fierce and angry are near-synonyms."),
    dict(stem=_ANA + "\n\nDrought is to rain as famine is to ______.",
         options=O(("A", "water"), ("B", "crops"), ("C", "hunger"), ("D", "food")),
         correct="D", strand="Verbal Analogies", concept="Y7-8 Verbal Reasoning · analogies: lack of something",
         explanation="A drought is a serious lack of rain; a famine is a serious lack of food. Hunger is the RESULT of famine, not the missing thing."),
    dict(stem=_ANA + "\n\nSculptor is to statue as playwright is to ______.",
         options=O(("A", "play"), ("B", "theatre"), ("C", "actor"), ("D", "poem")),
         correct="A", strand="Verbal Analogies", concept="Y7-8 Verbal Reasoning · analogies: creator to creation",
         explanation="A sculptor creates a statue; a playwright writes a play. A poem is written by a poet."),
    dict(stem=_ANA + "\n\nReluctant is to eager as scarce is to ______.",
         options=O(("A", "rare"), ("B", "empty"), ("C", "abundant"), ("D", "tiny")),
         correct="C", strand="Verbal Analogies", concept="Y7-8 Verbal Reasoning · analogies: opposites",
         explanation="Reluctant and eager are opposites, so the answer must be the opposite of scarce, which is abundant. Rare is a synonym of scarce."),
    dict(stem=_ANA + "\n\nGill is to fish as lung is to ______.",
         options=O(("A", "mammal"), ("B", "air"), ("C", "water"), ("D", "heart")),
         correct="A", strand="Verbal Analogies", concept="Y7-8 Verbal Reasoning · analogies: organ to creature",
         explanation="A fish breathes with gills; a mammal breathes with lungs. Air is what the lung uses, not the creature it belongs to."),
    dict(stem=_SC + "\n\nDespite hours of rehearsal, the actor still felt ______ about performing in front of such a large audience.",
         options=O(("A", "confident"), ("B", "apprehensive"), ("C", "indifferent"), ("D", "prepared")),
         correct="B", strand="Sentence Completion", concept="Y7-8 Reading · sentence completion: contrast signal 'despite' (ISEE style)",
         explanation="'Despite hours of rehearsal' signals a contrast, so the actor felt nervous: apprehensive."),
    dict(stem=_SC + "\n\nThe judge's decision was completely ______: she favoured neither one side nor the other.",
         options=O(("A", "harsh"), ("B", "sudden"), ("C", "popular"), ("D", "impartial")),
         correct="D", strand="Sentence Completion", concept="Y7-8 Reading · sentence completion: definition clue (ISEE style)",
         explanation="Favouring neither side is the definition of impartial."),
    dict(stem=_SC2 + "\n\nThe hikers were ______ by the sudden fog, and their ______ only grew when the path disappeared entirely.",
         options=O(("A", "reassured … calm"), ("B", "bewildered … anxiety"), ("C", "delighted … joy"), ("D", "exhausted … strength")),
         correct="B", strand="Sentence Completion", concept="Y7-8 Reading · double-blank sentence completion (ISEE style)",
         explanation="Sudden fog and a vanishing path confuse and worry the hikers: bewildered, with growing anxiety."),
    dict(stem=_SC2 + "\n\nAlthough the essay was ______, the teacher praised its ______ argument.",
         options=O(("A", "brief … persuasive"), ("B", "lengthy … rambling"), ("C", "polished … weak"), ("D", "careless … sloppy")),
         correct="A", strand="Sentence Completion", concept="Y7-8 Reading · double-blank with contrast signal (ISEE style)",
         explanation="'Although' needs a contrast: the essay was short, YET its argument was persuasive. The other pairs do not contrast."),
    dict(stem=_GR + "\n\nBy the time we arrived at the stadium, the match ______.",
         options=O(("A", "had already started"), ("B", "has already started"), ("C", "already starts"), ("D", "will already start")),
         correct="A", strand="Grammar & Cloze", concept="Y7 Grammar · past perfect tense (MAP Language Usage style)",
         explanation="An action completed before another past action takes the past perfect: 'had already started'."),
    dict(stem=_GR + "\n\nThe number of visitors to the museum ______ growing every year.",
         options=O(("A", "are"), ("B", "is"), ("C", "were"), ("D", "be")),
         correct="B", strand="Grammar & Cloze", concept="Y7 Grammar · subject-verb agreement: 'the number of' is singular",
         explanation="The subject is 'the number', which is singular: the number IS growing."),
    dict(stem=_GR + "\n\nThe service at the restaurant was slow; ______, the food was disappointing.",
         options=O(("A", "however"), ("B", "instead"), ("C", "moreover"), ("D", "otherwise")),
         correct="C", strand="Grammar & Cloze", concept="Y8 Grammar · linking adverbs: adding a second negative",
         explanation="Both halves are complaints, so we ADD a second problem with 'moreover'. 'However' would need a contrast."),
    dict(stem=_GR + "\n\nShe spoke so ______ that everyone in the hall could hear her.",
         options=O(("A", "clear"), ("B", "clearest"), ("C", "clearly"), ("D", "clearness")),
         correct="C", strand="Grammar & Cloze", concept="Y7 Grammar · adverbs modify verbs",
         explanation="'Spoke' is a verb, so it needs the adverb 'clearly'."),
    dict(stem=_LG + "\n\nAll members of the chess club are students. Some members of the chess club wear glasses. Which statement MUST be true?",
         options=O(("A", "All students play chess"), ("B", "All chess club members wear glasses"),
                   ("C", "No teachers wear glasses"), ("D", "Some students wear glasses")),
         correct="D", strand="Verbal Logic", concept="Y7-8 Reasoning · syllogism: what must follow",
         explanation="The glasses-wearing club members are all students, so at least some students wear glasses. The other statements go beyond the information given."),
    dict(stem=_LG + "\n\nFive runners finish a race. Kim finishes before Lee but after Maya. Noah finishes last. Oscar finishes before Maya. Who finishes SECOND?",
         options=O(("A", "Kim"), ("B", "Oscar"), ("C", "Lee"), ("D", "Maya")),
         correct="D", strand="Verbal Logic", concept="Y7-8 Reasoning · ordering deduction",
         explanation="The order is Oscar, Maya, Kim, Lee, Noah. So Maya finishes second."),
]

# ---- Non-Verbal Reasoning (16 = 12 CAT4-engine + 4 GL-style) ----------------
_SEQ = "Look at the four pictures in the top row. Work out the pattern, then choose the picture (A-E) that belongs in the empty box."
_CODE = "Each picture on the left has a two-letter code. Work out what each letter stands for, then choose the code for the picture marked '?'."

def _nshapes(fn, n, r, fill=INK):
    return lambda cx, cy: "".join(fn(cx + dx, cy + dy, r, fill) for dx, dy in
                                  {1: [(0, 0)], 2: [(-12, 0), (12, 0)], 3: [(-16, 0), (0, 0), (16, 0)],
                                   4: [(-12, -12), (12, -12), (-12, 12), (12, 12)],
                                   5: [(-16, -12), (0, -12), (16, -12), (-8, 12), (8, 12)]}[n])

NONVERBAL = nvr_from_json("level-c", 1) + [
    dict(stem=_SEQ, correct="C", strand="Figure Series (GL style)",
         concept="Y7-8 Non-Verbal Reasoning (GL 11+ series style) · two rules: count increases AND the shape alternates",
         explanation="Two rules run together: the count goes 1, 2, 3, 4 and the shape alternates square, circle. The fifth picture must be 5 SQUARES.",
         fig=seq_fig([_nshapes(square, 1, 8), _nshapes(circle, 2, 8), _nshapes(square, 3, 7), _nshapes(circle, 4, 7)],
                     [_nshapes(circle, 5, 6), _nshapes(square, 4, 7), _nshapes(square, 5, 6),
                      _nshapes(circle, 4, 7), _nshapes(square, 3, 7)])),
    dict(stem=_SEQ, correct="D", strand="Figure Series (GL style)",
         concept="Y7-8 Non-Verbal Reasoning (GL 11+ series style) · 45-degree rotation AND shading alternates",
         explanation="The arrow turns 45 degrees clockwise each step AND the shading alternates black, white. After (135 degrees, white) comes (180 degrees, BLACK): pointing left, filled.",
         fig=seq_fig([cell(arrow, 32, 0), cell(arrow, 32, 45, "none"), cell(arrow, 32, 90), cell(arrow, 32, 135, "none")],
                     [cell(arrow, 32, 180, "none"), cell(arrow, 32, 225), cell(arrow, 32, 135),
                      cell(arrow, 32, 180), cell(arrow, 32, 0, "none")])),
    dict(stem=_CODE, correct="E", strand="Figure Codes (GL style)",
         concept="Y7-8 Non-Verbal Reasoning (GL/CEM codes style) · first letter = shape, second letter = size",
         explanation="R means triangle and S means star; G means large and H means small. The mystery picture is a SMALL STAR: SH.",
         fig=codes_fig([(cell(triangle, 22, INK), "RG"), (cell(triangle, 12, INK), "RH"), (cell(star, 20, INK), "SG")],
                       cell(star, 11, INK)),
         options=O(("A", "RH"), ("B", "SG"), ("C", "RG"), ("D", "TG"), ("E", "SH"))),
    dict(stem=_CODE, correct="B", strand="Figure Codes (GL style)",
         concept="Y7-8 Non-Verbal Reasoning (GL/CEM codes style) · first letter = shape, second letter = shading",
         explanation="A means pentagon and B means hexagon; X means black and Y means white. The mystery picture is a WHITE HEXAGON: BY.",
         fig=codes_fig([(cell(pentagon, 18, INK), "AX"), (cell(pentagon, 18, "none"), "AY"), (cell(hexagon, 18, INK), "BX")],
                       cell(hexagon, 18, "none")),
         options=O(("A", "BX"), ("B", "BY"), ("C", "AY"), ("D", "AX"), ("E", "CY"))),
]

# ---- Mathematics (15: 7 short incl. 2 quantitative comparisons + 8 story) ---
_QC = ("Compare Quantity A and Quantity B, then choose:\n"
       "A) Quantity A is greater   B) Quantity B is greater\n"
       "C) The two quantities are equal   D) It cannot be determined from the information given\n\n")
_QC_OPTS = O(("A", "Quantity A is greater"), ("B", "Quantity B is greater"),
             ("C", "The two quantities are equal"), ("D", "It cannot be determined"))

MATHS = [
    # short form
    dict(stem="Work out 3 + 4 × 5",
         options=O(("A", "23"), ("B", "27"), ("C", "35"), ("D", "60")),
         correct="A", strand="Number", concept="Y6 Number · order of operations",
         explanation="Multiply first: 4 × 5 = 20, then 3 + 20 = 23. 35 comes from adding first."),
    dict(stem="Work out −7 + 12",
         options=O(("A", "−19"), ("B", "−5"), ("C", "0"), ("D", "5")),
         correct="D", strand="Number", concept="Y7 Number · adding with negative numbers",
         explanation="Start at −7 and count up 12: the answer is 5."),
    dict(stem="Work out 3/4 ÷ 3",
         options=O(("A", "1/12"), ("B", "1/4"), ("C", "1/3"), ("D", "9/4")),
         correct="B", strand="Fractions & Percentages", concept="Y6 Fractions · dividing a fraction by a whole number",
         explanation="Sharing 3/4 into 3 equal parts gives 1/4 each."),
    dict(stem="What is 15% of 240?",
         options=O(("A", "24"), ("B", "30"), ("C", "32"), ("D", "36")),
         correct="D", strand="Fractions & Percentages", concept="Y7 Percentages · percentage of an amount",
         explanation="10% of 240 = 24 and 5% = 12, so 15% = 24 + 12 = 36."),
    dict(stem="Solve 3x + 5 = 26",
         options=O(("A", "x = 6"), ("B", "x = 7"), ("C", "x = 8"), ("D", "x = 9")),
         correct="B", strand="Algebra", concept="Y7 Algebra · solving a two-step linear equation",
         explanation="3x = 26 − 5 = 21, so x = 7."),
    dict(stem=_QC + "Quantity A: 3/5 of 40\nQuantity B: 40% of 60",
         options=_QC_OPTS,
         correct="C", strand="Quantitative Comparison", concept="Y7 Fractions & Percentages · quantitative comparison (ISEE style)",
         explanation="Quantity A: 3/5 of 40 = 24. Quantity B: 40% of 60 = 24. The quantities are equal."),
    dict(stem=_QC + "x = 5\n\nQuantity A: 3x + 2\nQuantity B: 20 − x",
         options=_QC_OPTS,
         correct="A", strand="Quantitative Comparison", concept="Y7 Algebra · substitution, quantitative comparison (ISEE style)",
         explanation="Quantity A: 3(5) + 2 = 17. Quantity B: 20 − 5 = 15. Quantity A is greater."),
    # story form
    dict(stem="A jacket normally costs HK$260. In a sale everything is 25% off, and club members get a further HK$15 off the sale price. How much does a member pay for the jacket?",
         options=O(("A", "HK$180"), ("B", "HK$185"), ("C", "HK$195"), ("D", "HK$230")),
         correct="A", strand="Problem Solving", concept="Y7 Percentages · multi-step discount problem",
         explanation="25% off HK$260 leaves 0.75 × 260 = HK$195, then HK$195 − HK$15 = HK$180. HK$195 means the member discount was forgotten."),
    dict(stem="Five friends have a mean quiz score of exactly 82. Four of them scored 78, 84, 80 and 86. What did the fifth friend score?",
         options=O(("A", "78"), ("B", "80"), ("C", "82"), ("D", "86")),
         correct="C", strand="Problem Solving", concept="Y7 Statistics · working backwards from the mean",
         explanation="The five scores must total 5 × 82 = 410. The four given scores total 328, so the fifth is 410 − 328 = 82."),
    dict(stem="A cyclist rides 24 km in 1 hour 30 minutes. What is her average speed in kilometres per hour?",
         options=O(("A", "12 km/h"), ("B", "14 km/h"), ("C", "16 km/h"), ("D", "36 km/h")),
         correct="C", strand="Problem Solving", concept="Y8 Measures · speed = distance divided by time",
         explanation="1 hour 30 minutes is 1.5 hours, and 24 ÷ 1.5 = 16 km/h."),
    dict(stem="The diagram shows a triangular sail. What is the area of the sail?",
         fig=right_triangle_fig("8 m", "5 m"),
         options=O(("A", "13 m²"), ("B", "20 m²"), ("C", "40 m²"), ("D", "80 m²")),
         correct="B", strand="Problem Solving", concept="Y7 Geometry · area of a triangle (half base times height)",
         explanation="Area = 1/2 × 8 × 5 = 20 m². 40 comes from forgetting the half."),
    dict(stem="Amy and Ben share HK$240 between them in the ratio 3 : 5. How much does Ben receive?",
         options=O(("A", "HK$90"), ("B", "HK$120"), ("C", "HK$150"), ("D", "HK$160")),
         correct="C", strand="Problem Solving", concept="Y7 Ratio · sharing in a given ratio",
         explanation="There are 3 + 5 = 8 parts, each worth HK$30. Ben gets 5 × 30 = HK$150; HK$90 is Amy's share."),
    dict(stem="The bar chart shows the number of visitors to the school fair each day. How many more visitors came on the busiest day than the MEAN daily number of visitors?",
         fig=bar_chart(["Mon", "Tue", "Wed", "Thu", "Fri"], [120, 150, 90, 180, 160], 200, 20, unit="visitors"),
         options=O(("A", "40"), ("B", "50"), ("C", "60"), ("D", "90")),
         correct="A", strand="Problem Solving", concept="Y7 Statistics · reading a chart, then mean and comparison (multi-step)",
         explanation="The five days total 700, so the mean is 140. The busiest day (Thursday) had 180 visitors: 180 − 140 = 40."),
    dict(stem="The diagram shows angles meeting on a straight line. What is the size of angle x?",
         fig=angles_on_line([38, 74]),
         options=O(("A", "58°"), ("B", "68°"), ("C", "102°"), ("D", "112°")),
         correct="B", strand="Problem Solving", concept="Y7 Geometry · angles on a straight line sum to 180",
         explanation="38 + 74 = 112, and 180 − 112 = 68°. 112° is the sum of the two known angles, not x."),
    dict(stem="A tap fills a paddling pool at 4 litres per minute. The pool holds 600 litres and already contains 120 litres. How many minutes will it take to fill the pool completely?",
         options=O(("A", "105"), ("B", "110"), ("C", "115"), ("D", "120")),
         correct="D", strand="Problem Solving", concept="Y7 Number · rate problem with a starting amount",
         explanation="The pool still needs 600 − 120 = 480 litres, and 480 ÷ 4 = 120 minutes."),
]

# ---- Reading Comprehension (10) --------------------------------------------
PASSAGE_1 = (
    "<strong>The Try-Out</strong><br><br>"
    "Jonah had been first in line when the basketball try-out list went up, and last to leave every practice "
    "since. So when Coach Fung read out the final squad on Friday afternoon and Jonah's name was not on it, "
    "the gym seemed suddenly very loud and very small at the same time.<br><br>"
    "He took the long way home, past the harbour, where the evening ferries were stitching their white lines "
    "across the water. His phone buzzed with messages from his friends: bad luck, so unfair, the coach is blind. "
    "Jonah did not answer any of them. Deep down, in the honest part of himself that he usually kept for "
    "emergencies, he knew the truth. Marcus was quicker. Dev read the game better. Jonah had wanted a place on "
    "the squad; the others had earned one.<br><br>"
    "On Saturday morning he was back at the outdoor court by the estate, alone, before the sun had cleared the "
    "rooftops. He set up his phone against his water bottle and filmed his own free throws: fifty of them, then "
    "fifty more. That evening he watched the videos twice, wincing at his footwork, and wrote two words on a "
    "sticky note that he pressed onto his desk lamp: <em>next year</em>.<br><br>"
    "When his mother asked at dinner whether he was disappointed, Jonah surprised himself. “I was,” he said, "
    "reaching for the rice. “Now I'm busy.”"
)

PASSAGE_2 = (
    "<strong>Signals in the Sky</strong><br><br>"
    "Every child in Hong Kong learns to read one particular set of numbers long before any maths lesson: the "
    "typhoon warning signals. When the Observatory raises Signal No. 1, a tropical cyclone is centred within "
    "about 800 kilometres of the city: a distant watchfulness, nothing more. Signal No. 3 warns of strong winds, "
    "and kindergartens close their doors. But the number every student secretly hopes for is 8. When Signal "
    "No. 8 is hoisted, gale-force winds are expected, offices empty, ferries return to their moorings, and "
    "schools across the city fall silent.<br><br>"
    "The system is more than a century old. In its early days, before radio was widespread, the Observatory "
    "really did hoist physical signals: black symbols of bamboo and canvas raised on harbourside masts, with "
    "cannon and, later, explosive bombs fired to announce the strongest winds. The word “hoisted” survives in "
    "Hong Kong English to this day, long after the last mast was retired: people still say a signal is hoisted, "
    "even though it now travels by app and television rather than up a pole.<br><br>"
    "Visitors sometimes ask why the numbers jump from 3 straight to 8. The answer is history: signals 5, 6 and 7 "
    "once marked gales from different directions, and were replaced in 1973 by the single Signal No. 8 to avoid "
    "confusion. The gaps in the sequence are fossils, left behind by an older system.<br><br>"
    "For all its age, the system endures because it does one thing supremely well: it turns a complicated storm "
    "into a single number that a whole city, in any language, can understand at a glance."
)

_RC = "Y7-8 Reading · "
READING = [
    dict(passage=PASSAGE_1, stem="Why did the gym seem “suddenly very loud and very small” to Jonah?",
         options=O(("A", "The crowd had started cheering for the new squad"),
                   ("B", "He was overwhelmed by disappointment when his name was not read out"),
                   ("C", "The try-out had moved to a smaller hall"),
                   ("D", "Coach Fung was shouting the names too loudly")),
         correct="B", strand="Reading: Fiction", concept=_RC + "interpreting figurative description of emotion",
         explanation="The description shows how the moment of disappointment felt from inside, not a real change in the gym."),
    dict(passage=PASSAGE_1, stem="Why did Jonah not reply to his friends' messages?",
         options=O(("A", "His phone battery had died"),
                   ("B", "He was angry with his friends"),
                   ("C", "He privately knew the coach's decision was fair"),
                   ("D", "He had already forgotten about the try-out")),
         correct="C", strand="Reading: Fiction", concept=_RC + "inference from character behaviour",
         explanation="The honest part of himself knew Marcus and Dev had earned their places, so the sympathetic messages rang false."),
    dict(passage=PASSAGE_1, stem="What does the sticky note saying “next year” tell us about Jonah?",
         options=O(("A", "He plans to try again and is turning disappointment into a goal"),
                   ("B", "He has decided to give up basketball until next year"),
                   ("C", "He is reminding himself when the squad list will be published"),
                   ("D", "He wants to change schools next year")),
         correct="A", strand="Reading: Fiction", concept=_RC + "understanding a symbolic detail",
         explanation="Together with the dawn practice and the videos, the note shows determination aimed at the next try-out."),
    dict(passage=PASSAGE_1, stem="“I was,” he said. “Now I'm busy.” What does Jonah mean?",
         options=O(("A", "He is too busy with homework to feel anything"),
                   ("B", "He no longer cares about basketball"),
                   ("C", "He is pretending to be fine so his mother will not worry"),
                   ("D", "He has replaced feeling sorry for himself with working to improve")),
         correct="D", strand="Reading: Fiction", concept=_RC + "interpreting dialogue and character change",
         explanation="He admits the disappointment was real ('I was') but he has channelled it into practice: he is busy improving."),
    dict(passage=PASSAGE_1, stem="Which word best describes how Jonah deals with his setback by the end of the story?",
         options=O(("A", "resentful"), ("B", "carefree"), ("C", "resilient"), ("D", "boastful")),
         correct="C", strand="Reading: Fiction", concept=_RC + "evaluating character: vocabulary of traits",
         explanation="He faces the truth, keeps working and sets a goal: the definition of resilience."),
    dict(passage=PASSAGE_2, stem="What is the main purpose of this passage?",
         options=O(("A", "To warn readers about the dangers of typhoons"),
                   ("B", "To explain Hong Kong's typhoon signal system and its history"),
                   ("C", "To argue that the signal numbers should be changed"),
                   ("D", "To describe one famous typhoon in detail")),
         correct="B", strand="Reading: Non-fiction", concept=_RC + "identifying the main purpose",
         explanation="The passage explains what the signals mean, where they came from, and why the numbering looks odd."),
    dict(passage=PASSAGE_2, stem="According to the passage, what happens when Signal No. 8 is issued?",
         options=O(("A", "Only kindergartens close"), ("B", "A cyclone is within 800 km of Hong Kong"),
                   ("C", "Cannon are fired across the harbour"), ("D", "Schools close and ferries stop running")),
         correct="D", strand="Reading: Non-fiction", concept=_RC + "locating and combining stated details",
         explanation="At Signal 8, offices empty, ferries return to their moorings and schools fall silent. The 800 km figure belongs to Signal 1."),
    dict(passage=PASSAGE_2, stem="Why do Hong Kong people still say a signal is “hoisted”?",
         options=O(("A", "The Observatory still raises canvas symbols on masts"),
                   ("B", "The word survives from the days when physical signals were raised on masts"),
                   ("C", "It is the official legal term required by law"),
                   ("D", "Television stations invented the word in 1973")),
         correct="B", strand="Reading: Non-fiction", concept=_RC + "understanding word origins from context",
         explanation="The passage says the word survives from the era of bamboo-and-canvas signals, long after the masts were retired."),
    dict(passage=PASSAGE_2, stem="The writer calls the gaps in the numbering “fossils” because they are:",
         options=O(("A", "extremely old and made of stone"),
                   ("B", "dangerous leftovers that should be removed"),
                   ("C", "traces of an older system preserved in the current one"),
                   ("D", "impossible for scientists to explain")),
         correct="C", strand="Reading: Non-fiction", concept=_RC + "interpreting a metaphor",
         explanation="Like fossils, the missing numbers 5, 6 and 7 are remains of something older (the direction-based gale signals) preserved inside today's system."),
    dict(passage=PASSAGE_2, stem="According to the passage, why has the signal system lasted so long?",
         options=O(("A", "It turns a complex storm into one number everyone can understand"),
                   ("B", "It is too expensive to replace"),
                   ("C", "The government refuses to modernise it"),
                   ("D", "Hong Kong rarely experiences typhoons")),
         correct="A", strand="Reading: Non-fiction", concept=_RC + "identifying the writer's conclusion",
         explanation="The final paragraph says it endures because it does one thing supremely well: one number, understood at a glance, in any language."),
]

# ---- Listening (3 recordings, 10 Q) ----------------------------------------
_LI = "Listen to the recording, then choose the best answer."
_A1, _A2, _A3 = "listening1.m4a", "listening2.m4a", "listening3.m4a"

AUDIO_TITLES = {
    "listening1.m4a": "The Water Bottle Scheme",
    "listening2.m4a": "Planning the Project",
    "listening3.m4a": "This Week's Sports Report",
    "listening-zh.m4a": "週末計劃 Weekend Plans",
}

AUDIO = {
    "listening-zh.m4a": [("zh-CN-YunxiNeural", "-8%", "小美，我们这个星期六去科学馆做专题研究，好吗？"),
        ("zh-CN-XiaoxiaoNeural", "-8%", "好啊。几点见面？"),
        ("zh-CN-YunxiNeural", "-8%", "上午十点，在地铁站A出口等你，别迟到啊。"),
        ("zh-CN-XiaoxiaoNeural", "-8%", "没问题。要带什么吗？"),
        ("zh-CN-YunxiNeural", "-8%", "记得带学生证，凭学生证买门票有折扣。对了，如果星期六下雨，我们就改去中央图书馆，在那里也能找到资料。"),
        ("zh-CN-XiaoxiaoNeural", "-8%", "明白了，星期六见！")],
    _A1: [("en-GB-ThomasNeural", "-6%",
        "This is an announcement for all students. From next Monday, the school canteen will no longer "
        "sell drinks in plastic bottles. Instead, every student will receive a free steel water bottle, "
        "which you can refill at the new filling stations beside the library and the gym. "
        "The change follows a survey by the Green Committee, which found that our school threw away "
        "more than two thousand plastic bottles every month. "
        "Money previously spent on bottled drinks will now go towards new filters for the swimming pool. "
        "The canteen will still sell fresh juice, but you must bring your own cup. "
        "Students who lose their steel bottle can buy a replacement at the school office for twenty dollars.")],
    _A2: [
        ("en-GB-MaisieNeural", "-6%", "Ben, we still haven't picked a topic for the history project. It's due in three weeks."),
        ("en-GB-RyanNeural", "-6%", "I know. I liked your idea about the Kowloon Walled City, but half the class has chosen it already."),
        ("en-GB-MaisieNeural", "-6%", "True. What about the history of the trams? My uncle works at the tram depot, "
                          "and the museum has a whole photo archive we could use."),
        ("en-GB-RyanNeural", "-6%", "That settles it, then. The photos will make the display board much stronger. "
                        "When should we meet?"),
        ("en-GB-MaisieNeural", "-6%", "Thursday lunchtime in the library? I can borrow the tram book from my uncle before then."),
        ("en-GB-RyanNeural", "-6%", "Perfect. I'll bring my laptop and we can plan the sections."),
    ],
    _A3: [("en-US-ChristopherNeural", "-6%",
        "Here is this week's sports report. Congratulations to the swimming team, who finished second "
        "out of twelve schools at the inter-school championships on Saturday. "
        "Team captain Chloe Ng broke the school record in the one hundred metre butterfly, "
        "a record that had stood for nine years. "
        "Coach Fung praised the squad's commitment, saying the result was built on their early-morning "
        "training sessions, three times a week since January. "
        "The team now moves on to the regional finals in November. Well done, everyone.")],
}

LISTENING = [
    dict(stem=_LI + "\n\nWhat is the main purpose of the first announcement?", audio=_A1,
         options=O(("A", "To advertise the canteen's fresh juice"), ("B", "To report the results of a swimming gala"),
                   ("C", "To explain a new water-bottle scheme"), ("D", "To recruit members for the Green Committee")),
         correct="C", strand="Listening", concept="Y7-8 Listening · identifying the main purpose",
         explanation="The announcement explains that plastic bottles are ending and every student will receive a steel bottle."),
    dict(stem=_LI + "\n\nWhere are the new filling stations?", audio=_A1,
         options=O(("A", "Beside the library and the gym"), ("B", "In the canteen and the office"),
                   ("C", "Beside the hall and the pool"), ("D", "In every classroom")),
         correct="A", strand="Listening", concept="Y7-8 Listening · key detail (locations)",
         explanation="The filling stations are beside the library and the gym."),
    dict(stem=_LI + "\n\nWhat did the Green Committee's survey find?", audio=_A1,
         options=O(("A", "Fresh juice was unpopular"), ("B", "Over two thousand plastic bottles were thrown away each month"),
                   ("C", "The water fountains were broken"), ("D", "The pool filters needed replacing")),
         correct="B", strand="Listening", concept="Y7-8 Listening · supporting evidence (the survey figure)",
         explanation="The survey found the school threw away more than two thousand plastic bottles every month."),
    dict(stem=_LI + "\n\nWhat should a student do if they lose their steel bottle?", audio=_A1,
         options=O(("A", "Ask the canteen for a free one"), ("B", "Bring their own cup instead"),
                   ("C", "Report it to the Green Committee"), ("D", "Buy a replacement at the school office")),
         correct="D", strand="Listening", concept="Y7-8 Listening · specific instruction (HK$20 replacement)",
         explanation="Lost bottles can be replaced at the school office for twenty dollars. Bringing a cup applies to juice, not lost bottles."),
    dict(stem=_LI + "\n\nWhich topic do the students choose for their project?", audio=_A2,
         options=O(("A", "The Kowloon Walled City"), ("B", "The history of the trams"),
                   ("C", "The tram depot workers"), ("D", "The history of the museum")),
         correct="B", strand="Listening", concept="Y7-8 Listening · outcome of a discussion; Walled City is the REJECTED option trap",
         explanation="They drop the Walled City because half the class chose it, and settle on the history of the trams."),
    dict(stem=_LI + "\n\nWhat makes the tram topic attractive to Ben?", audio=_A2,
         options=O(("A", "The museum's photo archive will strengthen their display"), ("B", "It needs no research"),
                   ("C", "The teacher suggested it"), ("D", "He rides the tram to school")),
         correct="A", strand="Listening", concept="Y7-8 Listening · stated reason for a decision",
         explanation="Ben agrees because the photo archive will make the display board much stronger."),
    dict(stem=_LI + "\n\nWhen will the students meet?", audio=_A2,
         options=O(("A", "Monday after school"), ("B", "Tuesday lunchtime"),
                   ("C", "Thursday after school"), ("D", "Thursday lunchtime")),
         correct="D", strand="Listening", concept="Y7-8 Listening · arrangement detail with a near trap (Thursday, but LUNCHTIME)",
         explanation="They agree to meet on Thursday at lunchtime in the library."),
    dict(stem=_LI + "\n\nWhere did the swimming team finish at the championships?", audio=_A3,
         options=O(("A", "First"), ("B", "Second"), ("C", "Third"), ("D", "Fourth")),
         correct="B", strand="Listening", concept="Y7-8 Listening · key detail (result)",
         explanation="The team finished second out of twelve schools."),
    dict(stem=_LI + "\n\nIn which event did the captain break the school record?", audio=_A3,
         options=O(("A", "100 m freestyle"), ("B", "200 m backstroke"), ("C", "100 m butterfly"), ("D", "the relay")),
         correct="C", strand="Listening", concept="Y7-8 Listening · key detail (event)",
         explanation="Chloe Ng broke the school record in the one hundred metre butterfly."),
    dict(stem=_LI + "\n\nWhat does Coach Fung credit for the team's success?", audio=_A3,
         options=O(("A", "Early-morning training three times a week"), ("B", "A new training pool"),
                   ("C", "A change of diet"), ("D", "Luck on the day")),
         correct="A", strand="Listening", concept="Y7-8 Listening · attributed opinion (the coach's explanation)",
         explanation="Coach Fung says the result was built on early-morning training sessions, three times a week since January."),
]

# ---- Writing / Speaking / Chinese ------------------------------------------
CONTENT_WRITING = dict(
    type="writing",
    intro="Choose ONE of the two tasks below and type your answer in the box. Aim for about 130-180 words.",
    body=("Task 1: Write about a time you failed at something that mattered to you, and what you did next. "
          "Describe what happened and reflect honestly on what it taught you.\n\n"
          "Task 2: Some people believe students should be allowed to use their phones at school; others believe "
          "phones should be banned during the school day. What is your view? Support your opinion with clear "
          "reasons and examples."),
    hint="Start by saying which task you chose. Plan for a minute, organise your ideas into paragraphs, and leave time to check your accuracy.",
    placeholder="Type your answer here; it will be saved for review…",
)

CONTENT_SPEAKING = dict(
    type="speaking",
    stem="Record a short spoken response (about 90-120 seconds).",
    body=("Speak about:\n"
          "• Your name, your current school and year group\n"
          "• A subject you find genuinely interesting, and what makes it interesting to you\n"
          "• A challenge you have faced, in or out of school, and how you dealt with it\n"
          "• What you hope to contribute to your next school\n\n"
          "Speak naturally; this is a chance for your future school to hear how you think, not a memory test."),
)

CH_PASSAGE_TRAD = (
    "香港的夏天，總離不開一碗涼茶。放學路上，我常常經過街角那間老涼茶舖。深褐色的木櫃檯後面，一排黃銅大壺"
    "終日冒着熱氣，空氣裏混着廿四味的苦香。老闆娘梁姨在這裏站了三十多年，客人一推門，她往往不用開口，便知道"
    "對方要甚麼：熬夜的上班族來一碗夏枯草，喉嚨沙啞的老師來一碗羅漢果，貪吃煎炸食物的學生，自然是一碗廿四味。\n\n"
    "有人說，涼茶舖遲早會被連鎖飲品店取代。梁姨卻不太擔心。她說，涼茶賣的從來不只是那碗茶，還有一句"
    "「最近睡得好嗎」的問候。飲品店的餐牌再長，也印不下這一句。\n\n"
    "上星期經過，我看見梁姨的兒子辭了寫字樓的工作，回來學熬茶。他把每一種藥材的名字、分量和火候，"
    "一筆一筆記在小本子上，就像小學生抄生字一樣認真。爐火映在兩代人的臉上，我忽然覺得，這間小小的舖頭，"
    "大概還會一直開下去。"
)
CH_PASSAGE_SIMP = (
    "香港的夏天，总离不开一碗凉茶。放学路上，我常常经过街角那间老凉茶铺。深褐色的木柜台后面，一排黄铜大壶"
    "终日冒着热气，空气里混着廿四味的苦香。老板娘梁姨在这里站了三十多年，客人一推门，她往往不用开口，便知道"
    "对方要什么：熬夜的上班族来一碗夏枯草，喉咙沙哑的老师来一碗罗汉果，贪吃煎炸食物的学生，自然是一碗廿四味。\n\n"
    "有人说，凉茶铺迟早会被连锁饮品店取代。梁姨却不太担心。她说，凉茶卖的从来不只是那碗茶，还有一句"
    "“最近睡得好吗”的问候。饮品店的餐牌再长，也印不下这一句。\n\n"
    "上星期经过，我看见梁姨的儿子辞了写字楼的工作，回来学熬茶。他把每一种药材的名字、分量和火候，"
    "一笔一笔记在小本子上，就像小学生抄生字一样认真。炉火映在两代人的脸上，我忽然觉得，这间小小的铺头，"
    "大概还会一直开下去。"
)

def _ch(stem_t, stem_s, opts_ts, correct, concept, explanation):
    return dict(
        passage=zh_blocks(CH_PASSAGE_TRAD.replace("\n\n", "<br><br>"), CH_PASSAGE_SIMP.replace("\n\n", "<br><br>")),
        stem=bilingual(stem_t, stem_s),
        options=O(*[(k, bilingual(t, s)) for k, (t, s) in opts_ts.items()]),
        correct=correct, strand="中文閱讀理解", concept="初中中文 · " + concept, explanation=explanation)

CHINESE = [
    _ch("梁姨往往不用客人開口，便知道對方要甚麼，這說明她：", "梁姨往往不用客人开口，便知道对方要什么，这说明她：",
        {"A": ("記性比別人好", "记性比别人好"), "B": ("與街坊相熟，了解每位客人", "与街坊相熟，了解每位客人"),
         "C": ("只賣一種涼茶", "只卖一种凉茶"), "D": ("不喜歡與客人交談", "不喜欢与客人交谈")},
        "B", "內容理解：人物特點", "她站了三十多年，對常客的需要瞭如指掌，可見她與街坊相熟、用心了解客人。"),
    _ch("文中「餐牌再長，也印不下這一句」中的「這一句」是指：", "文中“餐牌再长，也印不下这一句”中的“这一句”是指：",
        {"A": ("涼茶的價錢", "凉茶的价钱"), "B": ("藥材的名字", "药材的名字"),
         "C": ("「最近睡得好嗎」的問候", "“最近睡得好吗”的问候"), "D": ("涼茶舖的地址", "凉茶铺的地址")},
        "C", "詞句理解：指代", "上文明確寫道：涼茶賣的還有一句「最近睡得好嗎」的問候。"),
    _ch("面對連鎖飲品店的競爭，梁姨的態度是：", "面对连锁饮品店的竞争，梁姨的态度是：",
        {"A": ("十分憂慮", "十分忧虑"), "B": ("打算結業", "打算结业"),
         "C": ("並不太擔心", "并不太担心"), "D": ("決定減價", "决定减价")},
        "C", "內容理解：態度", "文中直接寫道「梁姨卻不太擔心」，因為她相信涼茶舖賣的不只是茶。"),
    _ch("作者把兒子記筆記的樣子比作「小學生抄生字」，是想突出他：", "作者把儿子记笔记的样子比作“小学生抄生字”，是想突出他：",
        {"A": ("認真、謙虛地從頭學起", "认真、谦虚地从头学起"), "B": ("字體寫得端正", "字体写得端正"),
         "C": ("學歷不高", "学历不高"), "D": ("動作十分緩慢", "动作十分缓慢")},
        "A", "修辭理解：比喻作用", "比喻強調他放下身段、一筆一筆認真記錄，像初學者一樣謙虛用心。"),
    _ch("結尾「爐火映在兩代人的臉上」暗示了甚麼？", "结尾“炉火映在两代人的脸上”暗示了什么？",
        {"A": ("涼茶舖快要拆卸", "凉茶铺快要拆卸"), "B": ("天氣十分炎熱", "天气十分炎热"),
         "C": ("母子二人正在爭執", "母子二人正在争执"), "D": ("手藝有人承傳，涼茶舖可以延續下去", "手艺有人承传，凉茶铺可以延续下去")},
        "D", "內容理解：含意", "兒子回來學熬茶，兩代人同守爐火，正好呼應下句「這間小小的舖頭，大概還會一直開下去」。"),
    _ch("這篇文章主要想表達：", "这篇文章主要想表达：",
        {"A": ("涼茶比連鎖飲品店的飲品健康", "凉茶比连锁饮品店的饮品健康"),
         "B": ("傳統小店承載人情味與承傳，值得珍惜", "传统小店承载人情味与承传，值得珍惜"),
         "C": ("年輕人不應該辭職", "年轻人不应该辞职"), "D": ("夏天應該多喝涼茶", "夏天应该多喝凉茶")},
        "B", "主旨理解", "全文寫涼茶舖的人情與兩代承傳，帶出傳統小店的價值，並非比較飲品好壞。"),
]

CH_LISTENING = [
    dict(stem=bilingual("聆聽對話，然後回答問題。\n\n兩位同學星期六原本打算去哪裡？", "聆听对话，然后回答问题。\n\n两位同学星期六原本打算去哪里？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("博物館", "博物馆")), ("B", bilingual("圖書館", "图书馆")), ("C", bilingual("科學館", "科学馆")), ("D", bilingual("太空館", "太空馆"))),
         correct="C", strand="中文聆聽理解", concept="初中中文 · 聆聽：目的地（圖書館是雨天備案陷阱）",
         explanation="他們打算去科學館做專題研究；圖書館只是下雨時的備選。"),
    dict(stem=bilingual("他們約在什麼時間、什麼地方見面？", "他们约在什么时间、什么地方见面？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("九點在科學館正門", "九点在科学馆正门")), ("B", bilingual("十點在地鐵站A出口", "十点在地铁站A出口")), ("C", bilingual("十點在科學館門口", "十点在科学馆门口")), ("D", bilingual("十一點在地鐵站A出口", "十一点在地铁站A出口"))),
         correct="B", strand="中文聆聽理解", concept="初中中文 · 聆聽：時間與地點的組合",
         explanation="約定上午十點在地鐵站A出口見面。"),
    dict(stem=bilingual("為什麼要帶學生證？", "为什么要带学生证？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("買門票有折扣", "买门票有折扣")), ("B", bilingual("需要登記進場", "需要登记进场")), ("C", bilingual("可以借書", "可以借书")), ("D", bilingual("乘車半價", "乘车半价"))),
         correct="A", strand="中文聆聽理解", concept="初中中文 · 聆聽：原因",
         explanation="憑學生證買門票有折扣。"),
    dict(stem=bilingual("如果星期六下雨，他們會怎樣？", "如果星期六下雨，他们会怎样？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("改天再去", "改天再去")), ("B", bilingual("照原定計劃去", "照原定计划去")), ("C", bilingual("取消活動", "取消活动")), ("D", bilingual("改去中央圖書館", "改去中央图书馆"))),
         correct="D", strand="中文聆聽理解", concept="初中中文 · 聆聽：條件安排",
         explanation="下雨的話就改去中央圖書館找資料。"),
]

CH_SPEAKING = dict(
    type="speaking", maxSeconds=120,
    stem=bilingual("請用普通話介紹自己（大約90秒）。", "请用普通话介绍自己（大约90秒）。"),
    body=zh_blocks("可以說一說：\n• 你的名字、年級和學校\n• 你最感興趣的科目，為什麼\n• 一個你參加過的活動或比賽\n• 你為什麼想入讀新學校",
                   "可以说一说：\n• 你的名字、年级和学校\n• 你最感兴趣的科目，为什么\n• 一个你参加过的活动或比赛\n• 你为什么想入读新学校"),
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
