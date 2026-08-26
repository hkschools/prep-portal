# -*- coding: utf-8 -*-
"""HKS Baseline Assessment · Years 7-8 (current Y7-Y8 / G6-G7), version 3. 60 min core.

Third parallel form of level-c: same section structure and timing as v1/v2 with
all-new content. ISEE-style single and double-blank sentence completions,
MAP-style grammar/cloze, verbal logic, double-rule NVR, and Y6-Y7 maths with
multi-step story problems. Curriculum codes on every item.
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
    dict(stem=_SYN + "\n\nOBSTINATE", options=O(("A", "stubborn"), ("B", "flexible"), ("C", "clumsy"), ("D", "noisy")),
         correct="A", strand="Vocabulary: Synonyms", concept="Y7-8 Vocabulary · synonyms: obstinate = stubborn",
         explanation="An obstinate person refuses to change their mind: stubborn. Flexible is the opposite."),
    dict(stem=_SYN + "\n\nTRANQUIL", options=O(("A", "stormy"), ("B", "crowded"), ("C", "peaceful"), ("D", "distant")),
         correct="C", strand="Vocabulary: Synonyms", concept="Y7-8 Vocabulary · synonyms: tranquil = peaceful",
         explanation="A tranquil place is calm and peaceful. Stormy is the opposite."),
    dict(stem=_SYN + "\n\nENDEAVOUR", options=O(("A", "abandon"), ("B", "attempt"), ("C", "achieve"), ("D", "refuse")),
         correct="B", strand="Vocabulary: Synonyms", concept="Y7-8 Vocabulary · synonyms: endeavour = attempt",
         explanation="To endeavour is to try hard: to attempt. Achieve is what may follow an attempt, not the attempt itself."),
    dict(stem=_ANT + "\n\nFLIMSY", options=O(("A", "weak"), ("B", "light"), ("C", "narrow"), ("D", "sturdy")),
         correct="D", strand="Vocabulary: Antonyms", concept="Y7-8 Vocabulary · antonyms: flimsy vs sturdy",
         explanation="Flimsy means weakly made and easily broken; sturdy means strong and solid. Weak is a synonym of flimsy, not its opposite."),
    dict(stem=_ANT + "\n\nARRIVAL", options=O(("A", "journey"), ("B", "departure"), ("C", "welcome"), ("D", "entrance")),
         correct="B", strand="Vocabulary: Antonyms", concept="Y7-8 Vocabulary · antonyms: arrival vs departure",
         explanation="An arrival is reaching a place; a departure is leaving it. Entrance and welcome are associated with arriving, not its opposite."),
    dict(stem=_ANT + "\n\nCAUTIOUS", options=O(("A", "reckless"), ("B", "careful"), ("C", "slow"), ("D", "watchful")),
         correct="A", strand="Vocabulary: Antonyms", concept="Y7-8 Vocabulary · antonyms: cautious vs reckless",
         explanation="A cautious person avoids risks; a reckless person takes them without thinking. Careful and watchful are near-synonyms of cautious."),
    dict(stem=_ANA + "\n\nLibrary is to books as gallery is to ______.",
         options=O(("A", "artists"), ("B", "walls"), ("C", "visitors"), ("D", "paintings")),
         correct="D", strand="Verbal Analogies", concept="Y7-8 Verbal Reasoning · analogies: place to what it houses",
         explanation="A library houses books; a gallery houses paintings. Artists make the paintings but are not what the gallery keeps."),
    dict(stem=_ANA + "\n\nChapter is to novel as verse is to ______.",
         options=O(("A", "poem"), ("B", "letter"), ("C", "writer"), ("D", "chorus")),
         correct="A", strand="Verbal Analogies", concept="Y7-8 Verbal Reasoning · analogies: part to whole",
         explanation="A chapter is one section of a novel; a verse is one section of a poem. A chorus is another PART of a song, not the whole."),
    dict(stem=_ANA + "\n\nScissors are to cutting as needle is to ______.",
         options=O(("A", "sharpening"), ("B", "pinning"), ("C", "sewing"), ("D", "knitting")),
         correct="C", strand="Verbal Analogies", concept="Y7-8 Verbal Reasoning · analogies: tool to its function",
         explanation="Scissors are used for cutting; a needle is used for sewing. Knitting uses knitting needles, but 'a needle' with thread sews."),
    dict(stem=_ANA + "\n\nGenerous is to stingy as courageous is to ______.",
         options=O(("A", "brave"), ("B", "cowardly"), ("C", "careful"), ("D", "strong")),
         correct="B", strand="Verbal Analogies", concept="Y7-8 Verbal Reasoning · analogies: opposites",
         explanation="Generous and stingy are opposites, so the answer must be the opposite of courageous: cowardly. Brave is a synonym."),
    dict(stem=_SC + "\n\nThe climb was so ______ that even experienced hikers stopped twice to rest.",
         options=O(("A", "gentle"), ("B", "scenic"), ("C", "brief"), ("D", "arduous")),
         correct="D", strand="Sentence Completion", concept="Y7-8 Reading · sentence completion: result clue 'so … that' (ISEE style)",
         explanation="'So … that even experienced hikers stopped' signals great difficulty: the climb was arduous."),
    dict(stem=_SC + "\n\nThe lawyer presented such a ______ argument that even her opponents nodded in agreement.",
         options=O(("A", "compelling"), ("B", "feeble"), ("C", "lengthy"), ("D", "hesitant")),
         correct="A", strand="Sentence Completion", concept="Y7-8 Reading · sentence completion: result clue (ISEE style)",
         explanation="An argument that wins over even opponents must be convincing: compelling."),
    dict(stem=_SC2 + "\n\nThe old lighthouse, ______ for decades, was finally ______ by a team of volunteers.",
         options=O(("A", "admired … demolished"), ("B", "maintained … abandoned"), ("C", "neglected … restored"), ("D", "painted … lost")),
         correct="C", strand="Sentence Completion", concept="Y7-8 Reading · double-blank sentence completion (ISEE style)",
         explanation="'Finally' suggests the volunteers put right a long-standing problem: the lighthouse had been neglected, and they restored it. The other pairs do not fit together logically."),
    dict(stem=_SC2 + "\n\nFar from being ______, the desert was ______ with life once the sun set.",
         options=O(("A", "empty … silent"), ("B", "lifeless … teeming"), ("C", "dangerous … glowing"), ("D", "fertile … crowded")),
         correct="B", strand="Sentence Completion", concept="Y7-8 Reading · double-blank with contrast signal 'far from' (ISEE style)",
         explanation="'Far from being' demands a contrast: not lifeless, but teeming with life. 'Empty … silent' gives two similar ideas, not a contrast."),
    dict(stem=_GR + "\n\nEach of the players ______ given a medal after the final.",
         options=O(("A", "were"), ("B", "have been"), ("C", "was"), ("D", "are")),
         correct="C", strand="Grammar & Cloze", concept="Y7 Grammar · subject-verb agreement: 'each of' takes a singular verb",
         explanation="The subject is 'each', which is singular: each WAS given a medal."),
    dict(stem=_GR + "\n\nBy next June, the builders ______ the new library.",
         options=O(("A", "finish"), ("B", "finished"), ("C", "are finishing"), ("D", "will have finished")),
         correct="D", strand="Grammar & Cloze", concept="Y8 Grammar · future perfect with 'by' + a future time",
         explanation="An action completed before a future point ('by next June') takes the future perfect: will have finished."),
    dict(stem=_GR + "\n\nThe results were far better ______ we had expected.",
         options=O(("A", "than"), ("B", "then"), ("C", "as"), ("D", "that")),
         correct="A", strand="Grammar & Cloze", concept="Y7 Grammar · comparatives take 'than'",
         explanation="A comparative ('better') is followed by 'than'. 'Then' refers to time, not comparison."),
    dict(stem=_GR + "\n\n______ the heavy traffic, the bus arrived on time.",
         options=O(("A", "Because"), ("B", "Although"), ("C", "Despite"), ("D", "However")),
         correct="C", strand="Grammar & Cloze", concept="Y8 Grammar · 'despite' + noun phrase vs 'although' + clause",
         explanation="Before a noun phrase like 'the heavy traffic' we need 'despite'; 'although' would need a full clause with a verb."),
    dict(stem=_LG + "\n\nAll the paintings in the exhibition are for sale. Some of the paintings in the exhibition are watercolours. Which statement MUST be true?",
         options=O(("A", "All watercolours everywhere are for sale"), ("B", "Some paintings for sale are not watercolours"),
                   ("C", "All the paintings for sale are in the exhibition"), ("D", "Some watercolours are for sale")),
         correct="D", strand="Verbal Logic", concept="Y7-8 Reasoning · syllogism: what must follow",
         explanation="The watercolours in the exhibition are all for sale, so at least some watercolours are for sale. The other statements claim more than the information given."),
    dict(stem=_LG + "\n\nLeo, Mia and Noah each play exactly one of football, tennis and hockey. Leo does not play tennis. Mia plays neither football nor tennis. Which sport does Leo play?",
         options=O(("A", "Tennis"), ("B", "Football"), ("C", "Hockey"), ("D", "It cannot be determined")),
         correct="B", strand="Verbal Logic", concept="Y7-8 Reasoning · elimination grid deduction",
         explanation="Mia must play hockey. Tennis is then left for Noah, since Leo does not play it. So Leo plays football."),
]

# ---- Non-Verbal Reasoning (16 = 12 CAT4-engine + 4 GL-style) ----------------
_SEQ = "Look at the four pictures in the top row. Work out the pattern, then choose the picture (A-E) that belongs in the empty box."
_CODE = "Each picture on the left has a two-letter code. Work out what each letter stands for, then choose the code for the picture marked '?'."

NONVERBAL = nvr_from_json("level-c", 3) + [
    dict(stem=_SEQ, correct="E", strand="Figure Series (GL style)",
         concept="Y7-8 Non-Verbal Reasoning (GL 11+ series style) · two rules: quarter-turn ANTICLOCKWISE AND size alternates",
         explanation="Two rules run together: the arrow makes a quarter turn anticlockwise each step (right, up, left, down) and its size alternates large, small. Next comes a LARGE arrow pointing RIGHT, back where the cycle began.",
         fig=seq_fig([cell(arrow, 34, 0), cell(arrow, 22, 270), cell(arrow, 34, 180), cell(arrow, 22, 90)],
                     [cell(arrow, 34, 180), cell(arrow, 22, 0), cell(arrow, 34, 90),
                      cell(arrow, 22, 180), cell(arrow, 34, 0)])),
    dict(stem=_SEQ, correct="A", strand="Figure Series (GL style)",
         concept="Y7-8 Non-Verbal Reasoning (GL 11+ series style) · two rules: one more side each step AND the shape shrinks",
         explanation="Two rules run together: the shape gains one side each step (3, 4, 5, 6 sides) and gets smaller each step. The fifth picture must be a 7-sided shape, smaller still.",
         fig=seq_fig([cell(triangle, 22), cell(square, 18), cell(pentagon, 15), cell(hexagon, 12)],
                     [cell(heptagon, 9), cell(hexagon, 9), cell(heptagon, 12),
                      cell(star, 9), cell(pentagon, 9)])),
    dict(stem=_CODE, correct="C", strand="Figure Codes (GL style)",
         concept="Y7-8 Non-Verbal Reasoning (GL/CEM codes style) · first letter = which half is shaded, second letter = size",
         explanation="F means the left half is shaded and M means the top half is shaded; G means large and H means small. The mystery picture is a SMALL square with its TOP half shaded: MH.",
         fig=codes_fig([(cell(halfsquare, 20, 0), "FG"), (cell(halfsquare, 20, 90), "MG"), (cell(halfsquare, 11, 0), "FH")],
                       cell(halfsquare, 11, 90)),
         options=O(("A", "FH"), ("B", "MG"), ("C", "MH"), ("D", "FG"), ("E", "KH"))),
    dict(stem=_CODE, correct="D", strand="Figure Codes (GL style)",
         concept="Y7-8 Non-Verbal Reasoning (GL/CEM codes style) · first letter = size, second letter = shading",
         explanation="K means large and L means small; X means black and Y means white. The mystery picture is a SMALL WHITE pentagon: LY.",
         fig=codes_fig([(cell(pentagon, 20, INK), "KX"), (cell(pentagon, 20, "none"), "KY"), (cell(pentagon, 12, INK), "LX")],
                       cell(pentagon, 12, "none")),
         options=O(("A", "KX"), ("B", "KY"), ("C", "LX"), ("D", "LY"), ("E", "JY"))),
]

# ---- Mathematics (15: 7 short incl. 2 quantitative comparisons + 8 story) ---
_QC = ("Compare Quantity A and Quantity B, then choose:\n"
       "A) Quantity A is greater   B) Quantity B is greater\n"
       "C) The two quantities are equal   D) It cannot be determined from the information given\n\n")
_QC_OPTS = O(("A", "Quantity A is greater"), ("B", "Quantity B is greater"),
             ("C", "The two quantities are equal"), ("D", "It cannot be determined"))

MATHS = [
    # short form
    dict(stem="Work out 5 + 3 × 2²",
         options=O(("A", "11"), ("B", "17"), ("C", "32"), ("D", "41")),
         correct="B", strand="Number", concept="Y7 Number · order of operations with an index",
         explanation="The index first: 2² = 4, then 3 × 4 = 12, then 5 + 12 = 17. 11 forgets the square, and 32 adds 5 + 3 before multiplying."),
    dict(stem="Work out (−6) × (−3)",
         options=O(("A", "−18"), ("B", "−9"), ("C", "9"), ("D", "18")),
         correct="D", strand="Number", concept="Y7 Number · multiplying two negative numbers",
         explanation="A negative times a negative is positive: 18. −18 keeps a wrong minus sign, and −9 ADDS the numbers instead."),
    dict(stem="Work out 4/5 ÷ 2/3",
         options=O(("A", "8/15"), ("B", "5/6"), ("C", "6/5"), ("D", "15/8")),
         correct="C", strand="Fractions & Percentages", concept="Y6 Fractions · dividing by a fraction (multiply by the reciprocal)",
         explanation="Flip the SECOND fraction: 4/5 × 3/2 = 12/10 = 6/5. 8/15 multiplies without flipping, and 5/6 flips the first fraction instead."),
    dict(stem="What is 12.5% of 320?",
         options=O(("A", "4"), ("B", "25"), ("C", "32"), ("D", "40")),
         correct="D", strand="Fractions & Percentages", concept="Y7 Percentages · percentage of an amount (12.5% = one eighth)",
         explanation="12.5% is one eighth, and 320 ÷ 8 = 40. 32 is 10%, and 4 misplaces the decimal point."),
    dict(stem="Solve 4(x − 3) = 20",
         options=O(("A", "x = 2"), ("B", "x = 5"), ("C", "x = 8"), ("D", "x = 32")),
         correct="C", strand="Algebra", concept="Y7 Algebra · equation with brackets",
         explanation="Divide both sides by 4: x − 3 = 5, so x = 8. x = 5 forgets the − 3, and x = 2 subtracts 12 on the wrong side."),
    dict(stem=_QC + "Quantity A: the perimeter of a square with sides 6 cm\nQuantity B: the perimeter of an equilateral triangle with sides 8 cm",
         options=_QC_OPTS,
         correct="C", strand="Quantitative Comparison", concept="Y7 Geometry · perimeter, quantitative comparison (ISEE style)",
         explanation="Quantity A: 4 × 6 = 24 cm. Quantity B: 3 × 8 = 24 cm. The perimeters are equal."),
    dict(stem=_QC + "x + y = 10 and x is greater than y.\n\nQuantity A: x\nQuantity B: 5",
         options=_QC_OPTS,
         correct="A", strand="Quantitative Comparison", concept="Y7 Algebra · reasoning about inequalities, quantitative comparison (ISEE style)",
         explanation="If x and y were both 5 they would be equal, but x is greater than y, so x must take MORE than half of 10. Quantity A is always greater than 5."),
    # story form
    dict(stem="A recipe for 4 people uses 300 g of flour. How much flour is needed for 10 people?",
         options=O(("A", "306 g"), ("B", "750 g"), ("C", "1,200 g"), ("D", "3,000 g")),
         correct="B", strand="Problem Solving", concept="Y7 Ratio · proportional scaling (unitary method)",
         explanation="One person needs 300 ÷ 4 = 75 g, so 10 people need 750 g. 306 g wrongly ADDS the 6 extra people as grams, and 3,000 g multiplies by 10 without dividing first."),
    dict(stem="A tablet priced at HK$3,200 is reduced by 15% in a sale. At the checkout a further 10% is taken off the sale price. What is the final price?",
         options=O(("A", "HK$2,400"), ("B", "HK$2,448"), ("C", "HK$2,720"), ("D", "HK$2,880")),
         correct="B", strand="Problem Solving", concept="Y8 Percentages · successive percentage decreases (multiply, do not add)",
         explanation="After 15% off: 0.85 × 3,200 = HK$2,720. After another 10% off: 0.9 × 2,720 = HK$2,448. HK$2,400 wrongly takes 25% off in one go, and HK$2,720 stops after the first discount."),
    dict(stem="The diagram shows a ramp. Its horizontal base is 12 m and its vertical rise is 5 m. How long is the sloping side?",
         fig=right_triangle_fig("12 m", "5 m", "?"),
         options=O(("A", "7 m"), ("B", "13 m"), ("C", "17 m"), ("D", "60 m")),
         correct="B", strand="Problem Solving", concept="Y8 Geometry · Pythagoras' theorem (finding the hypotenuse)",
         explanation="12² + 5² = 144 + 25 = 169, and the square root of 169 is 13 m. 17 just ADDS the two sides, and 7 subtracts them."),
    dict(stem="The diagram shows angles meeting on a straight line. What is the size of angle x?",
         fig=angles_on_line([24, 38]),
         options=O(("A", "14°"), ("B", "62°"), ("C", "118°"), ("D", "156°")),
         correct="C", strand="Problem Solving", concept="Y7 Geometry · angles on a straight line sum to 180",
         explanation="24 + 38 = 62, and 180 − 62 = 118°. 62° is the sum of the two known angles, not x."),
    dict(stem="The line graph shows a coach journey. What was the coach's average speed for the WHOLE journey?",
         fig=line_graph(["09:00", "10:00", "11:00", "12:00", "13:00"], [0, 30, 30, 70, 90], 90, 10, unit="km"),
         options=O(("A", "22.5 km/h"), ("B", "30 km/h"), ("C", "40 km/h"), ("D", "90 km/h")),
         correct="A", strand="Problem Solving", concept="Y8 Statistics & Measures · distance-time graph, average speed over the full journey",
         explanation="The coach covers 90 km between 09:00 and 13:00, so 90 ÷ 4 = 22.5 km/h. 30 is the FIRST hour's speed, 40 is the fastest hour, and 90 is the distance, not a speed."),
    dict(stem="In a school choir, the ratio of boys to girls is 4 : 5. There are 45 girls. How many members does the choir have ALTOGETHER?",
         options=O(("A", "9"), ("B", "36"), ("C", "45"), ("D", "81")),
         correct="D", strand="Problem Solving", concept="Y7 Ratio · from one part to the whole (multi-step)",
         explanation="45 girls is 5 parts, so one part is 9 and the boys are 4 × 9 = 36. Altogether: 36 + 45 = 81. 36 is only the boys, and 9 is one part."),
    dict(stem="A full 600-litre water tank drains at a steady 8 litres per minute. How much water has DRAINED after 25 minutes?",
         options=O(("A", "200 litres"), ("B", "400 litres"), ("C", "575 litres"), ("D", "600 litres")),
         correct="A", strand="Problem Solving", concept="Y7 Number · rate problem (read carefully: drained, not remaining)",
         explanation="8 × 25 = 200 litres have drained. 400 litres is the water still LEFT in the tank, and 575 subtracts the minutes instead of the litres."),
    dict(stem="Stickers are sold only in packs of 8, at HK$18 per pack. Lena needs at least 60 stickers for her class. How much must she spend?",
         options=O(("A", "HK$144"), ("B", "HK$162"), ("C", "HK$480"), ("D", "HK$1,080")),
         correct="A", strand="Problem Solving", concept="Y7 Number · division with rounding UP in context, then money",
         explanation="60 ÷ 8 = 7.5, so she must buy 8 whole packs: 8 × 18 = HK$144. HK$162 buys one pack too many, and HK$1,080 multiplies all 60 stickers by the pack price."),
]

# ---- Reading Comprehension (10) --------------------------------------------
PASSAGE_1 = (
    "<strong>The Window Seat</strong><br><br>"
    "When Dad's new job moved the family to the city in July, Rafael made himself a promise: he would not "
    "like it. The promise was easy to keep at first. The new flat was on the fourteenth floor, the air "
    "smelled of buses, and the night was never properly dark; the city glowed at the edges like a screen "
    "that would not switch off.<br><br>"
    "His bedroom had one good thing, a deep window seat, and Rafael claimed it the way a cat claims a "
    "chair. From there he watched the street below and kept score against his new home. Point against: the "
    "clatter of the morning market. Point against: nobody here knew that, back home, he had been the "
    "fastest swimmer in his year.<br><br>"
    "It was from the window seat, one evening in August, that he first noticed the old man on the opposite "
    "roof. Every day at six, the man climbed up with a watering can and moved slowly along rows of buckets "
    "and basins, each one crowded with green. A roof, Rafael realised, could be a farm. He began to watch "
    "for him the way you watch for a favourite character.<br><br>"
    "Then one evening the man looked up, saw the boy in the window, and held up a tomato, small and bright "
    "as a traffic light. He pointed at Rafael, then at the tomato, then at the stairwell door on his roof.<br><br>"
    "Ten minutes later, Rafael stood among the buckets, breathing in the peppery smell of tomato leaves "
    "while the whole city rumbled softly below. The man spoke little. He simply handed Rafael the watering "
    "can and pointed at the basil.<br><br>"
    "Rafael still keeps score from the window seat, but the game has changed without his permission. Point "
    "in favour: the man on the roof waves now. Point in favour: from the fourteenth floor, you can watch "
    "the harbour turn pink before anyone down on the ground knows the day is ending."
)

PASSAGE_2 = (
    "<strong>Eight Arms and Three Hearts</strong><br><br>"
    "If you set out to design an animal as different from a human as possible, you might well end up with "
    "an octopus. It has three hearts, blue-green blood, no bones at all, and a soft body that can pour "
    "itself through a gap the size of a coin. Two thirds of its nerve cells sit not in its head but in its "
    "eight arms, so each arm can taste, touch and explore partly on its own. Yet the strangest thing about "
    "the octopus is not how it is built. It is how it behaves.<br><br>"
    "In aquariums around the world, octopuses have unscrewed jars from the inside to reach a crab, "
    "squirted water at light switches they disliked, and slipped out of their tanks at night to visit "
    "their neighbours. In one famous case, a New Zealand octopus named Inky apparently escaped through a "
    "drainpipe and returned to the sea. Such feats have convinced many scientists that the octopus is "
    "among the cleverest of all invertebrates, the vast group of animals without backbones.<br><br>"
    "Its camouflage is even more astonishing. Thousands of tiny colour-changing organs in its skin let an "
    "octopus melt into a rock or a patch of weed in less than a second, changing not just its colour but "
    "the very texture of its skin. Strangest of all, studies of octopus eyes suggest they may not see "
    "colour the way we do, and researchers still puzzle over how the animal matches surroundings it may "
    "not fully see.<br><br>"
    "There is a catch to this brilliance: most octopus species live only a year or two. Whatever an "
    "octopus learns, it has little time to use and no way to pass on.<br><br>"
    "Perhaps that is the real wonder. Intelligence, we assume, looks like us. The octopus, with its "
    "distributed brain and its shape-shifting skin, quietly suggests that nature can arrive at cleverness "
    "by an entirely different road."
)

_RC = "Y7-8 Reading · "
READING = [
    dict(passage=PASSAGE_1, stem="The city “glowed at the edges like a screen that would not switch off”. What does this suggest?",
         options=O(("A", "Rafael spent too long playing computer games"),
                   ("B", "The city was never completely dark or still, even at night"),
                   ("C", "The flat's lights were broken"),
                   ("D", "There was a cinema opposite the flat")),
         correct="B", strand="Reading: Fiction", concept=_RC + "interpreting a simile about setting",
         explanation="The comparison to a screen that never switches off shows the city's lights and activity never fully stop."),
    dict(passage=PASSAGE_1, stem="Why does Rafael “keep score against his new home”?",
         options=O(("A", "He is practising for a maths competition"),
                   ("B", "His father asked him to write a report about the city"),
                   ("C", "He wants to win an argument with the old man"),
                   ("D", "He promised himself not to like the city, so he collects reasons against it")),
         correct="D", strand="Reading: Fiction", concept=_RC + "inference: linking behaviour to motive",
         explanation="He vowed not to like the city, and listing 'points against' is his way of keeping that promise."),
    dict(passage=PASSAGE_1, stem="Rafael claimed the window seat “the way a cat claims a chair”. This means he:",
         options=O(("A", "made it his own special place"),
                   ("B", "was too lazy to leave his room"),
                   ("C", "shared it with the family cat"),
                   ("D", "scratched and damaged it")),
         correct="A", strand="Reading: Fiction", concept=_RC + "interpreting a comparison of behaviour",
         explanation="A cat settles on a chair as if it owns it; Rafael took possession of the window seat in the same complete, comfortable way."),
    dict(passage=PASSAGE_1, stem="Why does the old man hold up the tomato and point at the stairwell door?",
         options=O(("A", "To warn Rafael to stop staring at him"),
                   ("B", "To sell Rafael some vegetables"),
                   ("C", "To invite Rafael to come up and join him on the roof"),
                   ("D", "To show that his tomatoes had been stolen")),
         correct="C", strand="Reading: Fiction", concept=_RC + "inference from gesture (wordless invitation)",
         explanation="Pointing at Rafael, the tomato and then the door is a silent invitation, which Rafael accepts ten minutes later."),
    dict(passage=PASSAGE_1, stem="At the end, “the game has changed without his permission”. What does this tell us?",
         options=O(("A", "The old man has taken over the scoring"),
                   ("B", "Rafael has started to like the city, despite his promise not to"),
                   ("C", "Rafael has stopped sitting in the window seat"),
                   ("D", "The family has decided to move home again")),
         correct="B", strand="Reading: Fiction", concept=_RC + "interpreting the resolution: change against intention",
         explanation="He now counts points IN FAVOUR of the city; his feelings have shifted even though he never meant to let them."),
    dict(passage=PASSAGE_2, stem="Which statement best sums up the main idea of the passage?",
         options=O(("A", "Octopuses are dangerous and should not be kept in aquariums"),
                   ("B", "Octopuses live short lives and learn very little"),
                   ("C", "Octopuses would be more intelligent with longer lives"),
                   ("D", "The octopus is remarkable for both its unusual body and its intelligent behaviour")),
         correct="D", strand="Reading: Non-fiction", concept=_RC + "identifying the main idea",
         explanation="The passage moves from the octopus's strange body to its problem-solving, camouflage and what its cleverness means."),
    dict(passage=PASSAGE_2, stem="Why does the writer describe octopuses unscrewing jars and escaping from tanks?",
         options=O(("A", "To give evidence of their problem-solving intelligence"),
                   ("B", "To show that aquariums are badly built"),
                   ("C", "To prove that octopuses dislike crabs"),
                   ("D", "To explain how camouflage works")),
         correct="A", strand="Reading: Non-fiction", concept=_RC + "understanding the function of evidence",
         explanation="The jar-opening and escapes are examples supporting the claim that the octopus is among the cleverest invertebrates."),
    dict(passage=PASSAGE_2, stem="The octopus can “pour itself through a gap the size of a coin”. The word “pour” suggests that its body:",
         options=O(("A", "is full of sea water"),
                   ("B", "cannot stop moving"),
                   ("C", "moves like a liquid because it has no bones"),
                   ("D", "melts in warm water")),
         correct="C", strand="Reading: Non-fiction", concept=_RC + "vocabulary in context: figurative 'pour'",
         explanation="'Pour' is used for liquids; applied to the boneless octopus, it shows how its soft body flows through tiny spaces."),
    dict(passage=PASSAGE_2, stem="What do researchers still find puzzling about octopus camouflage?",
         options=O(("A", "Why the octopus only changes colour at night"),
                   ("B", "How it matches colours in surroundings it may not fully see"),
                   ("C", "Why its skin cannot change texture"),
                   ("D", "Why predators are never fooled by it")),
         correct="B", strand="Reading: Non-fiction", concept=_RC + "combining details: the camouflage-vision puzzle",
         explanation="Octopus eyes may not see colour the way ours do, yet the animal matches its surroundings; how it does so is still not fully understood."),
    dict(passage=PASSAGE_2, stem="Which statement best describes the writer's view in the final paragraph?",
         options=O(("A", "Octopus intelligence is really just instinct, not cleverness"),
                   ("B", "Octopuses think in exactly the same way humans do"),
                   ("C", "Scientists have wasted their time studying octopuses"),
                   ("D", "Octopus intelligence is genuine, but built along a completely different path from ours")),
         correct="D", strand="Reading: Non-fiction", concept=_RC + "identifying a nuanced position",
         explanation="The writer argues we assume intelligence must look human, while the octopus shows nature 'can arrive at cleverness by an entirely different road'."),
]

# ---- Listening (3 recordings, 10 Q) ----------------------------------------
_LI = "Listen to the recording, then choose the best answer."
_A1, _A2, _A3 = "listening1.m4a", "listening2.m4a", "listening3.m4a"

AUDIO_TITLES = {
    "listening1.m4a": "New Morning Shuttle Routes",
    "listening2.m4a": "The Magazine Interview",
    "listening3.m4a": "Drama Club Report",
    "listening-zh.m4a": "運動會準備 Team Practice",
}

AUDIO = {
    "listening-zh.m4a": [("zh-CN-YunxiNeural", "-10%", "小雨，运动会下个月就到了，我们的接力队还没练好交棒呢。"),
        ("zh-CN-XiaoxiaoNeural", "-10%", "是啊，上次练习我们就掉了一次棒。那我们星期三放学后加练一次，好不好？"),
        ("zh-CN-YunxiNeural", "-10%", "好。下午四点半在操场入口集合，别忘了穿运动鞋。"),
        ("zh-CN-XiaoxiaoNeural", "-10%", "知道了。要带水吗？"),
        ("zh-CN-YunxiNeural", "-10%", "当然要，每人带一瓶水。对了，要是那天操场被高年级借用了，我们就改到学校旁边的公园练习。"),
        ("zh-CN-XiaoxiaoNeural", "-10%", "明白，星期三见！")],
    _A1: [("en-GB-ThomasNeural", "-6%",
        "Attention, all students. From the first of next month, the school will run two new morning "
        "shuttle buses. Route One leaves Ocean Bay Plaza at seven twenty and stops at Hilltop Estate. "
        "Route Two leaves Greenfield Station at seven forty. "
        "Both buses arrive at school by five past eight, in good time for registration at eight twenty. "
        "To ride the shuttle, you must register your student card at the school office by this Friday; "
        "an unregistered card will not open the bus door. The shuttle is free for the whole of the first term. "
        "One last thing: if a black rainstorm warning is issued before seven in the morning, the shuttles "
        "will not run, and the school hall will open from seven thirty for students who arrive early.")],
    _A2: [
        ("en-GB-MaisieNeural", "-6%", "Ryan, our magazine article is due in two weeks and we still haven't chosen anyone to interview."),
        ("en-GB-RyanNeural", "-6%", "What about the principal? Everyone reads those interviews."),
        ("en-GB-MaisieNeural", "-6%", "That's exactly the problem. The December issue already had a long interview with her. "
                          "We'd just be repeating it."),
        ("en-GB-RyanNeural", "-6%", "True. You know who nobody has ever interviewed? Mr Ho, the school gardener. "
                        "He's worked here for thirty years, since before the science block was even built."),
        ("en-GB-MaisieNeural", "-6%", "That's a brilliant idea. He could tell us how the whole campus has changed."),
        ("en-GB-RyanNeural", "-6%", "I'll ask him tomorrow. Can you book somewhere quiet to record it?"),
        ("en-GB-MaisieNeural", "-6%", "I'll book the small room beside the music room, for Tuesday after school."),
        ("en-GB-RyanNeural", "-6%", "Perfect. I'll draft the questions tonight and send them over for you to check."),
    ],
    _A3: [("en-US-ChristopherNeural", "-6%",
        "Here is this week's arts report. The drama club's production of an original play, The Lantern "
        "Maker, ran for three nights last week, and every single performance sold out. "
        "The play was directed by Year Ten student Marco Silva, the first student director in the "
        "school's history. Marco thanked the twelve members of the backstage crew, saying the audience "
        "never sees the people who matter most. "
        "Ticket sales raised six thousand five hundred dollars, which the club will donate to a "
        "children's reading charity. "
        "Auditions for the spring musical will be held in the hall on the second Monday of January.")],
}

LISTENING = [
    dict(stem=_LI + "\n\nWhen will the new shuttle buses start running?", audio=_A1,
         options=O(("A", "This Friday"), ("B", "Next Monday"),
                   ("C", "On the first of next month"), ("D", "On the first of this month")),
         correct="C", strand="Listening", concept="Y7-8 Listening · key date with a near trap (Friday is the REGISTRATION deadline)",
         explanation="The shuttles begin on the first of next month; this Friday is the deadline for registering your card."),
    dict(stem=_LI + "\n\nWhat must students do by this Friday?", audio=_A1,
         options=O(("A", "Buy a bus ticket"), ("B", "Register their student card at the school office"),
                   ("C", "Choose a seat on the bus"), ("D", "Pay for the first term")),
         correct="B", strand="Listening", concept="Y7-8 Listening · required action (the card must be registered to open the door)",
         explanation="Students must register their student card at the school office by Friday; the shuttle itself is free for the first term."),
    dict(stem=_LI + "\n\nWhat time does Route Two leave Greenfield Station?", audio=_A1,
         options=O(("A", "7:20"), ("B", "8:05"), ("C", "8:20"), ("D", "7:40")),
         correct="D", strand="Listening", concept="Y7-8 Listening · key time among several near values (7:20 is Route ONE; 8:05 is arrival; 8:20 is registration)",
         explanation="Route Two leaves at seven forty. Seven twenty is Route One's departure time."),
    dict(stem=_LI + "\n\nWhat happens if a black rainstorm warning is issued before seven?", audio=_A1,
         options=O(("A", "The shuttles will not run, and the hall opens from 7:30"), ("B", "The shuttles leave earlier than usual"),
                   ("C", "School is cancelled for the day"), ("D", "Students must wait at the bus stops")),
         correct="A", strand="Listening", concept="Y7-8 Listening · conditional arrangement",
         explanation="Under a black rainstorm warning before seven, the shuttles are cancelled and the school hall opens from seven thirty."),
    dict(stem=_LI + "\n\nWho do the students decide to interview?", audio=_A2,
         options=O(("A", "The principal"), ("B", "A Year Ten student"),
                   ("C", "Mr Ho, the school gardener"), ("D", "The music teacher")),
         correct="C", strand="Listening", concept="Y7-8 Listening · outcome of a discussion; the principal is the REJECTED option trap",
         explanation="They drop the principal, who was interviewed in December, and choose Mr Ho, the gardener of thirty years."),
    dict(stem=_LI + "\n\nWhy do they decide NOT to interview the principal?", audio=_A2,
         options=O(("A", "She refused to take part"), ("B", "The December issue already carried a long interview with her"),
                   ("C", "She is leaving the school soon"), ("D", "She is too busy to meet them")),
         correct="B", strand="Listening", concept="Y7-8 Listening · stated reason for rejecting an option",
         explanation="Maisie points out the December issue already had a long interview with the principal, so they would be repeating it."),
    dict(stem=_LI + "\n\nWhere and when will they record the interview?", audio=_A2,
         options=O(("A", "Tuesday lunchtime, in the music room"), ("B", "Monday after school, beside the hall"),
                   ("C", "Tuesday after school, in the music room"), ("D", "Tuesday after school, in the small room beside the music room")),
         correct="D", strand="Listening", concept="Y7-8 Listening · arrangement detail with a near trap (the room BESIDE the music room, not the music room)",
         explanation="Maisie books the small room beside the music room for Tuesday after school."),
    dict(stem=_LI + "\n\nWhat was special about the play's director?", audio=_A3,
         options=O(("A", "He was the school's first student director"), ("B", "He wrote the play in a single night"),
                   ("C", "He also played the main role"), ("D", "He is the school's youngest teacher")),
         correct="A", strand="Listening", concept="Y7-8 Listening · key detail (a first in the school's history)",
         explanation="Marco Silva, a Year Ten student, was the first student director in the school's history."),
    dict(stem=_LI + "\n\nWho did Marco especially thank?", audio=_A3,
         options=O(("A", "The audience"), ("B", "The twelve members of the backstage crew"),
                   ("C", "The ticket sellers"), ("D", "His drama teacher")),
         correct="B", strand="Listening", concept="Y7-8 Listening · attributed detail (who was credited)",
         explanation="Marco thanked the twelve backstage crew members, the people the audience never sees."),
    dict(stem=_LI + "\n\nWhat will happen to the money from ticket sales?", audio=_A3,
         options=O(("A", "It will pay for the spring musical"), ("B", "It will buy new stage lights"),
                   ("C", "It will be donated to a children's reading charity"), ("D", "It will be shared among the cast")),
         correct="C", strand="Listening", concept="Y7-8 Listening · key detail (use of the funds)",
         explanation="The six thousand five hundred dollars raised will be donated to a children's reading charity."),
]

# ---- Writing / Speaking / Chinese ------------------------------------------
CONTENT_WRITING = dict(
    type="writing",
    intro="Choose ONE of the two tasks below and type your answer in the box. Aim for about 130-180 words.",
    body=("Task 1: Write about a promise that was hard to keep, or a time you helped someone when it was not "
          "convenient for you. Describe what happened and reflect honestly on what you learned.\n\n"
          "Task 2: Some people think schools should replace printed textbooks with tablets and e-books; others "
          "think printed books still matter. What is your view? Support your opinion with clear reasons "
          "and examples."),
    hint="Start by saying which task you chose. Plan for a minute, organise your ideas into paragraphs, and leave time to check your accuracy.",
    placeholder="Type your answer here; it will be saved for review…",
)

CONTENT_SPEAKING = dict(
    type="speaking",
    stem="Record a short spoken response (about 90-120 seconds).",
    body=("Speak about:\n"
          "• Your name, your current school and year group\n"
          "• A place in your city you would show a visitor, and why you would choose it\n"
          "• Something you used to find difficult and improved at through practice\n"
          "• A question you would like to ask the teachers at your next school\n\n"
          "Speak naturally and take your time; there are no right answers, only your own."),
)

CH_PASSAGE_TRAD = (
    "每天早上，我都乘電車上學。電車不快，叮叮兩聲，慢慢地沿着軌道前行。車廂裏，有讀報的老伯，有低頭溫習的學生；"
    "司機叔叔會向每一位上車的乘客點一點頭，像老朋友打招呼一樣。\n\n"
    "同學常笑我傻：地鐵十分鐘的路程，電車偏偏要走半小時。可是我喜歡坐在上層靠窗的位置，看街市的菜販開檔，"
    "看茶樓的蒸籠冒出白煙，看整條街慢慢醒過來。有一次我忘記帶車費，正着急時，司機叔叔擺擺手說：「明天補回吧。」"
    "第二天我把車費補上，他卻早已忘了這回事。\n\n"
    "有人說，電車是這座城市的一根針線，把一條條街道細細縫在一起。我想，它縫住的不只是街道，"
    "還有車廂裏那些互相點頭的陌生人。"
)
CH_PASSAGE_SIMP = (
    "每天早上，我都乘电车上学。电车不快，叮叮两声，慢慢地沿着轨道前行。车厢里，有读报的老伯，有低头温习的学生；"
    "司机叔叔会向每一位上车的乘客点一点头，像老朋友打招呼一样。\n\n"
    "同学常笑我傻：地铁十分钟的路程，电车偏偏要走半小时。可是我喜欢坐在上层靠窗的位置，看街市的菜贩开档，"
    "看茶楼的蒸笼冒出白烟，看整条街慢慢醒过来。有一次我忘记带车费，正着急时，司机叔叔摆摆手说：“明天补回吧。”"
    "第二天我把车费补上，他却早已忘了这回事。\n\n"
    "有人说，电车是这座城市的一根针线，把一条条街道细细缝在一起。我想，它缝住的不只是街道，"
    "还有车厢里那些互相点头的陌生人。"
)

def _ch(stem_t, stem_s, opts_ts, correct, concept, explanation):
    return dict(
        passage=zh_blocks(CH_PASSAGE_TRAD.replace("\n\n", "<br><br>"), CH_PASSAGE_SIMP.replace("\n\n", "<br><br>")),
        stem=bilingual(stem_t, stem_s),
        options=O(*[(k, bilingual(t, s)) for k, (t, s) in opts_ts.items()]),
        correct=correct, strand="中文閱讀理解", concept="初中中文 · " + concept, explanation=explanation)

CHINESE = [
    _ch("「它縫住的不只是街道」中的「它」指的是：", "“它缝住的不只是街道”中的“它”指的是：",
        {"A": ("地鐵", "地铁"), "B": ("針線", "针线"),
         "C": ("電車", "电车"), "D": ("街市", "街市")},
        "C", "詞句理解：指代", "上文把電車比作城市的針線，所以「它」指的就是電車。"),
    _ch("把電車比作「城市的一根針線」，作用是：", "把电车比作“城市的一根针线”，作用是：",
        {"A": ("形象地寫出電車把一條條街道連接起來", "形象地写出电车把一条条街道连接起来"), "B": ("說明電車的車身又細又長", "说明电车的车身又细又长"),
         "C": ("諷刺電車已經破舊不堪", "讽刺电车已经破旧不堪"), "D": ("說明電車的車費便宜", "说明电车的车费便宜")},
        "A", "修辭理解：比喻作用", "針線把布縫合起來，比喻電車沿街行走，把一條條街道串連在一起，形象生動。"),
    _ch("對電車的「慢」，作者的態度是：", "对电车的“慢”，作者的态度是：",
        {"A": ("十分不滿", "十分不满"), "B": ("覺得應該加快", "觉得应该加快"),
         "C": ("感到無可奈何", "感到无可奈何"), "D": ("欣賞，認為慢有慢的好處", "欣赏，认为慢有慢的好处")},
        "D", "內容理解：態度", "作者說「可是我喜歡」，並細寫沿途風景，可見他欣賞電車的慢，認為慢讓人看見更多。"),
    _ch("司機叔叔「擺擺手」讓作者第二天才補車費，表現他：", "司机叔叔“摆摆手”让作者第二天才补车费，表现他：",
        {"A": ("粗心大意", "粗心大意"), "B": ("寬容隨和，信任乘客", "宽容随和，信任乘客"),
         "C": ("害怕電車遲到", "害怕电车迟到"), "D": ("不喜歡收車費", "不喜欢收车费")},
        "B", "內容理解：人物特點", "他不但不為難忘記帶車費的學生，事後更不放在心上，可見他寬容隨和，信任乘客。"),
    _ch("同學笑作者「傻」，是因為：", "同学笑作者“傻”，是因为：",
        {"A": ("作者常常坐過站", "作者常常坐过站"), "B": ("作者不會乘地鐵", "作者不会乘地铁"),
         "C": ("電車的車費太貴", "电车的车费太贵"), "D": ("地鐵十分鐘的路程，作者卻花半小時乘電車", "地铁十分钟的路程，作者却花半小时乘电车")},
        "D", "內容理解：原因", "文中明確寫道：地鐵十分鐘的路程，電車偏偏要走半小時，同學因此笑作者傻。"),
    _ch("這篇文章主要想表達：", "这篇文章主要想表达：",
        {"A": ("在急促的城市裏，慢下來反而看見風景與人情", "在急促的城市里，慢下来反而看见风景与人情"),
         "B": ("電車已經過時，應該被淘汰", "电车已经过时，应该被淘汰"),
         "C": ("乘地鐵比乘電車更方便", "乘地铁比乘电车更方便"), "D": ("上學不應該遲到", "上学不应该迟到")},
        "A", "主旨理解", "全文寫電車的慢、沿途的風景和車廂裏的人情，帶出慢下來才看得見城市的美好，並非比較交通工具的優劣。"),
]

CH_LISTENING = [
    dict(stem=bilingual("聆聽對話，然後回答問題。\n\n他們星期三要練習甚麼？", "聆听对话，然后回答问题。\n\n他们星期三要练习什么？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("跳遠", "跳远")), ("B", bilingual("短跑起步", "短跑起步")), ("C", bilingual("游泳", "游泳")), ("D", bilingual("接力交棒", "接力交棒"))),
         correct="D", strand="中文聆聽理解", concept="初中中文 · 聆聽：活動內容",
         explanation="他們的接力隊上次掉了棒，所以星期三要加練交棒。"),
    dict(stem=bilingual("他們約在甚麼時間、甚麼地方集合？", "他们约在什么时间、什么地方集合？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("星期三四點在操場入口", "星期三四点在操场入口")), ("B", bilingual("星期三四點半在操場入口", "星期三四点半在操场入口")), ("C", bilingual("星期五四點半在公園", "星期五四点半在公园")), ("D", bilingual("星期三四點半在學校門口", "星期三四点半在学校门口"))),
         correct="B", strand="中文聆聽理解", concept="初中中文 · 聆聽：時間與地點的組合（四點是陷阱）",
         explanation="他們約星期三下午四點半在操場入口集合。"),
    dict(stem=bilingual("每人要帶甚麼？", "每人要带什么？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("運動鞋和一瓶水", "运动鞋和一瓶水")), ("B", bilingual("只帶運動鞋", "只带运动鞋")), ("C", bilingual("接力棒和毛巾", "接力棒和毛巾")), ("D", bilingual("課本和水", "课本和水"))),
         correct="A", strand="中文聆聽理解", concept="初中中文 · 聆聽：要帶的物品（兩項都要）",
         explanation="對話提到要穿運動鞋，每人還要帶一瓶水，兩樣都不能少。"),
    dict(stem=bilingual("如果操場被高年級借用了，他們會怎樣？", "如果操场被高年级借用了，他们会怎样？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("取消練習", "取消练习")), ("B", bilingual("改在課室休息", "改在课室休息")), ("C", bilingual("改到學校旁邊的公園練習", "改到学校旁边的公园练习")), ("D", bilingual("改到星期四再練", "改到星期四再练"))),
         correct="C", strand="中文聆聽理解", concept="初中中文 · 聆聽：條件安排（陷阱題）",
         explanation="如果操場被借用，他們就改到學校旁邊的公園練習，而不是取消。"),
]

CH_SPEAKING = dict(
    type="speaking", maxSeconds=120,
    stem=bilingual("請用普通話介紹自己（大約90秒）。", "请用普通话介绍自己（大约90秒）。"),
    body=zh_blocks("可以說一說：\n• 你的名字、年級和學校\n• 一本你喜歡的書或一部電影，為甚麼喜歡\n• 你的一個優點，並舉一個例子\n• 你想在新學校參加甚麼活動",
                   "可以说一说：\n• 你的名字、年级和学校\n• 一本你喜欢的书或一部电影，为什么喜欢\n• 你的一个优点，并举一个例子\n• 你想在新学校参加什么活动"),
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
