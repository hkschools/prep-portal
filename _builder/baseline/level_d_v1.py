# -*- coding: utf-8 -*-
"""HKS Baseline Assessment · Years 9-10 (current Y9-Y10 / G8-G9), version 1. 75 min core.

Top tier: ISEE-Upper/SSAT-level vocabulary, three double-blank completions,
four verbal-logic items, double-rule and overlay NVR, and Y8-Y9 maths
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
    dict(stem=_SYN + "\n\nMETICULOUS", options=O(("A", "careless"), ("B", "painstaking"), ("C", "rapid"), ("D", "generous")),
         correct="B", strand="Vocabulary: Synonyms", concept="Y9-10 Vocabulary · synonyms: meticulous = painstaking",
         explanation="Meticulous means showing great attention to detail: painstaking. Careless is the opposite."),
    dict(stem=_SYN + "\n\nAMBIGUOUS", options=O(("A", "unclear"), ("B", "obvious"), ("C", "ambitious"), ("D", "generous")),
         correct="A", strand="Vocabulary: Synonyms", concept="Y9-10 Vocabulary · synonyms: ambiguous = unclear",
         explanation="Ambiguous means open to more than one interpretation: unclear. Do not confuse it with 'ambitious'."),
    dict(stem=_SYN + "\n\nTENACIOUS", options=O(("A", "fragile"), ("B", "temporary"), ("C", "persistent"), ("D", "cautious")),
         correct="C", strand="Vocabulary: Synonyms", concept="Y9-10 Vocabulary · synonyms: tenacious = persistent",
         explanation="A tenacious person holds on and refuses to give up: persistent."),
    dict(stem=_SYN + "\n\nBENEVOLENT", options=O(("A", "wealthy"), ("B", "ancient"), ("C", "violent"), ("D", "kind-hearted")),
         correct="D", strand="Vocabulary: Synonyms", concept="Y9-10 Vocabulary · synonyms: benevolent = kind-hearted",
         explanation="Benevolent means well-meaning and kindly. The 'bene-' root means good."),
    dict(stem=_ANT + "\n\nFRUGAL", options=O(("A", "thrifty"), ("B", "extravagant"), ("C", "hungry"), ("D", "modest")),
         correct="B", strand="Vocabulary: Antonyms", concept="Y9-10 Vocabulary · antonyms: frugal vs extravagant",
         explanation="Frugal means careful with money; extravagant means spending freely. Thrifty is a synonym of frugal."),
    dict(stem=_ANT + "\n\nPROFOUND", options=O(("A", "deep"), ("B", "serious"), ("C", "superficial"), ("D", "mysterious")),
         correct="C", strand="Vocabulary: Antonyms", concept="Y9-10 Vocabulary · antonyms: profound vs superficial",
         explanation="Profound means deep or far-reaching; superficial means shallow, on the surface only."),
    dict(stem=_ANT + "\n\nCANDID", options=O(("A", "evasive"), ("B", "honest"), ("C", "cheerful"), ("D", "rude")),
         correct="A", strand="Vocabulary: Antonyms", concept="Y9-10 Vocabulary · antonyms: candid vs evasive",
         explanation="Candid means frank and direct; evasive means avoiding giving a straight answer. Honest is a synonym of candid."),
    dict(stem=_ANT + "\n\nAMPLIFY", options=O(("A", "enlarge"), ("B", "broadcast"), ("C", "repeat"), ("D", "diminish")),
         correct="D", strand="Vocabulary: Antonyms", concept="Y9-10 Vocabulary · antonyms: amplify vs diminish",
         explanation="To amplify is to make larger or stronger; to diminish is to make smaller."),
    dict(stem=_ANA + "\n\nArchipelago is to islands as constellation is to ______.",
         options=O(("A", "planets"), ("B", "stars"), ("C", "telescopes"), ("D", "clouds")),
         correct="B", strand="Verbal Analogies", concept="Y9-10 Verbal Reasoning · analogies: collection to member",
         explanation="An archipelago is a group of islands; a constellation is a group of stars."),
    dict(stem=_ANA + "\n\nScalpel is to surgeon as chisel is to ______.",
         options=O(("A", "sculptor"), ("B", "hammer"), ("C", "stone"), ("D", "hospital")),
         correct="A", strand="Verbal Analogies", concept="Y9-10 Verbal Reasoning · analogies: tool to user",
         explanation="A surgeon works with a scalpel; a sculptor works with a chisel. Stone is the material, not the user."),
    dict(stem=_ANA + "\n\nEphemeral is to permanent as transparent is to ______.",
         options=O(("A", "invisible"), ("B", "clear"), ("C", "fragile"), ("D", "opaque")),
         correct="D", strand="Verbal Analogies", concept="Y9-10 Verbal Reasoning · analogies: opposites",
         explanation="Ephemeral and permanent are opposites, so the answer is the opposite of transparent: opaque."),
    dict(stem=_ANA + "\n\nFamished is to hungry as elated is to ______.",
         options=O(("A", "exhausted"), ("B", "surprised"), ("C", "happy"), ("D", "proud")),
         correct="C", strand="Verbal Analogies", concept="Y9-10 Verbal Reasoning · analogies: intensity (extreme to mild)",
         explanation="Famished is an extreme degree of hungry; elated is an extreme degree of happy."),
    dict(stem=_ANA + "\n\nDrought is to water as vacuum is to ______.",
         options=O(("A", "cleanliness"), ("B", "space"), ("C", "sound"), ("D", "matter")),
         correct="D", strand="Verbal Analogies", concept="Y9-10 Verbal Reasoning · analogies: absence of",
         explanation="A drought is an absence of water; a vacuum is an absence of matter."),
    dict(stem=_SC + "\n\nHer argument was so ______ that even her fiercest critics conceded the point.",
         options=O(("A", "persuasive"), ("B", "lengthy"), ("C", "hesitant"), ("D", "familiar")),
         correct="A", strand="Sentence Completion", concept="Y9-10 Reading · sentence completion: cause-and-effect clue (ISEE style)",
         explanation="Critics conceding the point is the effect of a persuasive argument."),
    dict(stem=_SC + "\n\nThe results of the experiment were ______, offering clear support to neither theory.",
         options=O(("A", "decisive"), ("B", "inconclusive"), ("C", "fraudulent"), ("D", "predictable")),
         correct="B", strand="Sentence Completion", concept="Y9-10 Reading · sentence completion: definition clue (ISEE style)",
         explanation="Supporting neither theory is the definition of inconclusive results."),
    dict(stem=_SC2 + "\n\nFar from being ______, the review was so ______ that the author considered abandoning the sequel altogether.",
         options=O(("A", "harsh … encouraging"), ("B", "brief … detailed"), ("C", "gentle … scathing"), ("D", "late … punctual")),
         correct="C", strand="Sentence Completion", concept="Y9-10 Reading · double-blank with reversal signal (ISEE Upper style)",
         explanation="'Far from being' reverses the first word: the review was not gentle but scathing, crushing enough to make the author consider giving up."),
    dict(stem=_SC2 + "\n\nThe scientist remained ______ about the early results, insisting that further trials were needed before any ______ conclusions could be drawn.",
         options=O(("A", "ecstatic … cautious"), ("B", "skeptical … firm"), ("C", "confident … tentative"), ("D", "indifferent … hasty")),
         correct="B", strand="Sentence Completion", concept="Y9-10 Reading · double-blank with logical consistency (ISEE Upper style)",
         explanation="Demanding further trials shows doubt (skeptical) and an unwillingness to draw firm conclusions yet."),
    dict(stem=_SC2 + "\n\nAlthough the village appeared ______ at first glance, closer inspection revealed a community ______ with quiet activity.",
         options=O(("A", "deserted … humming"), ("B", "crowded … bursting"), ("C", "ancient … crumbling"), ("D", "prosperous … thriving")),
         correct="A", strand="Sentence Completion", concept="Y9-10 Reading · double-blank with contrast signal (ISEE Upper style)",
         explanation="'Although' demands a contrast: it looked deserted, yet was actually humming with activity. The other pairs do not contrast."),
    dict(stem=_GR + "\n\nNeither the students nor the teacher ______ aware of the timetable change.",
         options=O(("A", "were"), ("B", "are"), ("C", "was"), ("D", "have been")),
         correct="C", strand="Grammar & Cloze", concept="Y9 Grammar · agreement with 'neither … nor' (nearest subject)",
         explanation="With 'neither … nor', the verb agrees with the nearer subject, 'the teacher', which is singular: was."),
    dict(stem=_GR + "\n\n______ the rain had stopped hours earlier, the pitch remained waterlogged.",
         options=O(("A", "Because"), ("B", "Although"), ("C", "Unless"), ("D", "Whenever")),
         correct="B", strand="Grammar & Cloze", concept="Y9 Grammar · subordinating conjunctions: concession",
         explanation="The two facts contrast (rain stopped, pitch still wet), so the concessive 'Although' fits."),
    dict(stem=_GR + "\n\nIf she ______ harder last term, she would have passed the examination.",
         options=O(("A", "studied"), ("B", "studies"), ("C", "would study"), ("D", "had studied")),
         correct="D", strand="Grammar & Cloze", concept="Y10 Grammar · third conditional (unreal past)",
         explanation="An unreal past condition takes the past perfect: 'if she had studied … she would have passed'."),
    dict(stem=_LG + "\n\nNo reptiles are warm-blooded. All snakes are reptiles. Which statement MUST be true?",
         options=O(("A", "All reptiles are snakes"), ("B", "Some snakes are warm-blooded"),
                   ("C", "No snakes are warm-blooded"), ("D", "All warm-blooded animals are mammals")),
         correct="C", strand="Verbal Logic", concept="Y9-10 Reasoning · syllogism with a negative premise",
         explanation="Snakes are reptiles, and no reptiles are warm-blooded, so no snakes are warm-blooded."),
    dict(stem=_LG + "\n\nFour classes P, Q, R and S each use the hall in a different period, 1 to 4. Q is immediately after P. R is not in period 1. S is in period 4. In which period is R?",
         options=O(("A", "Period 1"), ("B", "Period 2"), ("C", "Period 3"), ("D", "It cannot be determined")),
         correct="C", strand="Verbal Logic", concept="Y9-10 Reasoning · scheduling deduction",
         explanation="S takes period 4, so P and Q (consecutive) must be periods 1 and 2, leaving R in period 3. R cannot be in period 1 anyway."),
    dict(stem=_LG + "\n\nSome athletes are musicians. All musicians are dedicated. Which statement MUST be true?",
         options=O(("A", "Some athletes are dedicated"), ("B", "All athletes are dedicated"),
                   ("C", "All dedicated people are musicians"), ("D", "Some musicians are not athletes")),
         correct="A", strand="Verbal Logic", concept="Y9-10 Reasoning · syllogism: some/all chains",
         explanation="The athletes who are musicians must be dedicated, so at least some athletes are dedicated. The other statements go beyond the premises."),
    dict(stem=_LG + "\n\nIn a code, DELTA is written as EFMUB. Using the same code, how is RIVER written?",
         options=O(("A", "QHUDQ"), ("B", "SJWFS"), ("C", "SJWDS"), ("D", "RJVFR")),
         correct="B", strand="Verbal Logic", concept="Y9-10 Reasoning · letter-shift code (CAT4 verbal style)",
         explanation="Each letter moves forward one place (D to E, E to F, L to M …), so RIVER becomes SJWFS."),
]

# ---- Non-Verbal Reasoning (20 = 14 CAT4-engine + 6 GL-style) ----------------
_SEQ = "Look at the four pictures in the top row. Work out the pattern, then choose the picture (A-E) that belongs in the empty box."
_CODE = "Each picture on the left has a two-letter code. Work out what each letter stands for, then choose the code for the picture marked '?'."

def _hexdots(hr, n):
    return lambda cx, cy: hexagon(cx, cy, hr, "none") + dots(cx, cy, n, 3.4)

def _npoly(fn, n, r, fill=INK):
    return lambda cx, cy: "".join(fn(cx + dx, cy + dy, r, fill) for dx, dy in
                                  {2: [(-12, 0), (12, 0)], 3: [(-16, 0), (0, 0), (16, 0)]}[n])

NONVERBAL = nvr_from_json("level-d", 1) + [
    dict(stem=_SEQ, correct="E", strand="Figure Series (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM series style) · two rules: the hexagon shrinks AND gains a dot each step",
         explanation="Two rules run together: the hexagon shrinks in equal steps (24, 20, 16, 12) AND the dots inside increase 1, 2, 3, 4. Next: the smallest hexagon with 5 dots.",
         fig=seq_fig([_hexdots(24, 1), _hexdots(20, 2), _hexdots(16, 3), _hexdots(12, 4)],
                     [_hexdots(12, 5), _hexdots(8, 4), _hexdots(24, 5), _hexdots(8, 6), _hexdots(8, 5)])),
    dict(stem=_SEQ, correct="A", strand="Figure Series (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM series style) · two interleaved series (alternating shapes, each with its own rotation)",
         explanation="Two series are interleaved: the arrows (positions 1 and 3) turn 90 degrees each time they appear, and the half-circles (positions 2 and 4) do the same. Position 5 is an arrow, turned 90 degrees on from position 3: pointing left.",
         fig=seq_fig([cell(arrow, 30, 0), cell(halfcircle, 16, 0), cell(arrow, 30, 90), cell(halfcircle, 16, 90)],
                     [cell(arrow, 30, 180), cell(halfcircle, 16, 180), cell(arrow, 30, 90),
                      cell(arrow, 30, 270), cell(halfcircle, 16, 270)])),
    dict(stem=_SEQ, correct="B", strand="Figure Series (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM series style) · rotation of a chiral shape with a mirror trap",
         explanation="The flag shape turns 90 degrees clockwise each step, so after 270 degrees it returns to the start position. D is a mirror image, which no rotation can produce.",
         fig=seq_fig([cell(fshape, 9, 0), cell(fshape, 9, 90), cell(fshape, 9, 180), cell(fshape, 9, 270)],
                     [cell(fshape, 9, 90), cell(fshape, 9, 0), cell(fshape, 9, 180),
                      cell(fshape, 9, 0, mirror=True), cell(fshape, 9, 270)])),
    dict(stem=_CODE, correct="C", strand="Figure Codes (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM codes style) · first letter = shape family, second letter = orientation",
         explanation="P means half-shaded square and Q means half-shaded circle; K means shaded on the left, L shaded on top, N shaded on the bottom. The mystery picture is a square shaded on TOP: PL.",
         fig=codes_fig([(cell(halfsquare, 16, 0), "PK"), (cell(halfsquare, 16, 270), "PN"),
                        (cell(halfcircle, 17, 90), "QL"), (cell(halfcircle, 17, 0), "QK")],
                       cell(halfsquare, 16, 90)),
         options=O(("A", "PK"), ("B", "QL"), ("C", "PL"), ("D", "PN"), ("E", "QN"))),
    dict(stem=_CODE, correct="D", strand="Figure Codes (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM codes style) · first letter = count, second letter = shape",
         explanation="D means two shapes and E means three; T means triangle and W means circle. The mystery picture is THREE CIRCLES: EW.",
         fig=codes_fig([(_npoly(triangle, 2, 11), "DT"), (_npoly(triangle, 3, 10), "ET"), (_npoly(circle, 2, 9), "DW")],
                       _npoly(circle, 3, 8)),
         options=O(("A", "DT"), ("B", "DW"), ("C", "ET"), ("D", "EW"), ("E", "FW"))),
    dict(stem=_CODE, correct="E", strand="Figure Codes (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM codes style) · first letter = shape, second letter = shading",
         explanation="G means square and H means diamond; Z means black and Y means white. The mystery picture is a WHITE DIAMOND: HY.",
         fig=codes_fig([(cell(square, 15, INK), "GZ"), (cell(square, 15, "none"), "GY"), (cell(diamond, 19, INK), "HZ")],
                       cell(diamond, 19, "none")),
         options=O(("A", "GY"), ("B", "HZ"), ("C", "GZ"), ("D", "HX"), ("E", "HY"))),
]

# ---- Mathematics (15: 7 short incl. 3 quantitative comparisons + 8 story) ---
_QC = ("Compare Quantity A and Quantity B, then choose:\n"
       "A) Quantity A is greater   B) Quantity B is greater\n"
       "C) The two quantities are equal   D) It cannot be determined from the information given\n\n")
_QC_OPTS = O(("A", "Quantity A is greater"), ("B", "Quantity B is greater"),
             ("C", "The two quantities are equal"), ("D", "It cannot be determined"))

MATHS = [
    # short form
    dict(stem="Work out 2<sup>3</sup> × 2<sup>4</sup>",
         options=O(("A", "128"), ("B", "144"), ("C", "2048"), ("D", "4096")),
         correct="A", strand="Number", concept="Y8 Number · index laws: add the powers",
         explanation="2³ × 2⁴ = 2⁷ = 128. Multiplying the powers (2¹² = 4096) is the classic error."),
    dict(stem="Solve 5x − 3 = 2x + 12",
         options=O(("A", "x = 2"), ("B", "x = 3"), ("C", "x = 4"), ("D", "x = 5")),
         correct="D", strand="Algebra", concept="Y8 Algebra · equations with x on both sides",
         explanation="5x − 2x = 12 + 3, so 3x = 15 and x = 5."),
    dict(stem="After a 20% increase, a price is HK$144. What was the ORIGINAL price?",
         options=O(("A", "HK$110"), ("B", "HK$115.20"), ("C", "HK$120"), ("D", "HK$126")),
         correct="C", strand="Number", concept="Y9 Percentages · reverse percentage",
         explanation="144 is 120% of the original, so the original is 144 ÷ 1.2 = HK$120. Taking 20% off 144 (HK$115.20) is the classic error."),
    dict(stem="What is the nth term of the sequence 5, 8, 11, 14, …?",
         options=O(("A", "n + 3"), ("B", "5n"), ("C", "2n + 3"), ("D", "3n + 2")),
         correct="D", strand="Algebra", concept="Y8 Sequences · nth term of a linear sequence",
         explanation="The sequence goes up in 3s, so the rule starts 3n; when n = 1 it must give 5, so it is 3n + 2."),
    dict(stem=_QC + "x² = 25\n\nQuantity A: x\nQuantity B: 5",
         options=_QC_OPTS,
         correct="D", strand="Quantitative Comparison", concept="Y9 Algebra · quantitative comparison with two possible roots (ISEE style)",
         explanation="x could be 5 or −5. If x = 5 the quantities are equal; if x = −5, Quantity B is greater. It cannot be determined."),
    dict(stem=_QC + "Quantity A: 1/3 + 1/4\nQuantity B: 2/7",
         options=_QC_OPTS,
         correct="A", strand="Quantitative Comparison", concept="Y8 Fractions · comparison; adding tops and bottoms is the trap (ISEE style)",
         explanation="1/3 + 1/4 = 7/12, which is more than half. 2/7 is less than half. Quantity A is greater; 2/7 is what the classic wrong method (adding numerators and denominators) produces."),
    dict(stem=_QC + "a and b are positive numbers.\n\nQuantity A: a² + b²\nQuantity B: (a + b)²",
         options=_QC_OPTS,
         correct="B", strand="Quantitative Comparison", concept="Y9 Algebra · expanding a bracket, quantitative comparison (ISEE style)",
         explanation="(a + b)² = a² + 2ab + b². Since a and b are positive, 2ab > 0, so Quantity B is always greater."),
    # story form
    dict(stem="A 13-metre support wire runs from the top of a vertical pole to a hook on level ground, as shown. How far is the hook from the base of the pole?",
         fig=right_triangle_fig("? m", "12 m", "13 m"),
         options=O(("A", "5 m"), ("B", "11 m"), ("C", "17.7 m"), ("D", "25 m")),
         correct="A", strand="Problem Solving", concept="Y9 Geometry · Pythagoras' theorem (finding a shorter side)",
         explanation="13² − 12² = 169 − 144 = 25, and the square root of 25 is 5 m. Adding instead of subtracting gives 17.7."),
    dict(stem="Adult tickets cost HK$90 and child tickets cost HK$50. A family buys 5 tickets in total and pays HK$330. How many CHILD tickets did they buy?",
         options=O(("A", "1"), ("B", "2"), ("C", "3"), ("D", "4")),
         correct="C", strand="Problem Solving", concept="Y9 Algebra · setting up simultaneous conditions",
         explanation="With c children: 90(5 − c) + 50c = 330, so 450 − 40c = 330 and c = 3. Check: 2 adults (HK$180) + 3 children (HK$150) = HK$330."),
    dict(stem="A taxi charges HK$27 for the first 2 km, then HK$1.90 for every additional 200 m. How much does a 5 km journey cost?",
         options=O(("A", "HK$47.50"), ("B", "HK$55.50"), ("C", "HK$74.50"), ("D", "HK$84.00")),
         correct="B", strand="Problem Solving", concept="Y9 Number · stepped-rate real-world problem (HK taxi fare)",
         explanation="The extra 3 km is 15 steps of 200 m: 15 × HK$1.90 = HK$28.50, plus HK$27 gives HK$55.50."),
    dict(stem="Mr Chan invests HK$8,000 at 4% simple interest per year. How much INTEREST does he earn over 3 years?",
         options=O(("A", "HK$320"), ("B", "HK$960"), ("C", "HK$1,280"), ("D", "HK$8,960")),
         correct="B", strand="Problem Solving", concept="Y9 Percentages · simple interest over several years",
         explanation="4% of HK$8,000 is HK$320 per year, so 3 years earn 3 × 320 = HK$960. HK$8,960 is the final balance, not the interest."),
    dict(stem="A circular fish pond has a radius of 7 m. Taking π as 22/7, what is the AREA of the pond?",
         options=O(("A", "44 m²"), ("B", "77 m²"), ("C", "154 m²"), ("D", "616 m²")),
         correct="C", strand="Problem Solving", concept="Y9 Geometry · area of a circle",
         explanation="Area = πr² = 22/7 × 49 = 154 m². 44 m² is the circumference calculation, not the area."),
    dict(stem="A trader buys a watch for HK$250 and sells it for HK$320. What is her percentage profit?",
         options=O(("A", "12%"), ("B", "22%"), ("C", "25%"), ("D", "28%")),
         correct="D", strand="Problem Solving", concept="Y9 Percentages · percentage profit on cost price",
         explanation="Profit is HK$70 on a cost of HK$250: 70/250 = 28%. Dividing by the selling price (70/320, about 22%) is the classic error."),
    dict(stem="The spinner shown has 8 equal sectors. What is the probability that one spin lands on a sector marked R?",
         fig=spinner([("R", 3, "#72AFDB"), ("B", 4, "#eef2f8"), ("G", 1, "#c9d6e4")]),
         options=O(("A", "1/3"), ("B", "3/8"), ("C", "3/5"), ("D", "5/8")),
         correct="B", strand="Problem Solving", concept="Y8 Probability · probability from a diagram",
         explanation="3 of the 8 equal sectors are marked R: 3/8. Comparing R with B only (3/5 or 3/4-style reasoning) is the trap."),
    dict(stem="The graph shows a cyclist's journey. Distance from home (km) is plotted against time (hours). What was the cyclist's speed during the FIRST hour?",
         fig=line_graph(["0", "1", "2", "3"], [0, 60, 60, 120], 120, 30, unit="km"),
         options=O(("A", "20 km/h"), ("B", "40 km/h"), ("C", "60 km/h"), ("D", "120 km/h")),
         correct="C", strand="Problem Solving", concept="Y9 Graphs · reading speed from a distance-time graph",
         explanation="In the first hour the distance rises from 0 to 60 km, so the speed is 60 km/h. The flat section afterwards is a rest: speed 0. 40 km/h is the average over the whole 3 hours, not the first hour."),
]

# ---- Reading Comprehension (12) --------------------------------------------
PASSAGE_1 = (
    "<strong>The Map Collector</strong><br><br>"
    "My grandfather never trusted the blue dot. Long after everyone else had surrendered their sense of "
    "direction to a glowing screen, he continued to draw his own maps: bus routes inked in red, noodle shops "
    "marked with tiny stars, the steep ladder streets of Sheung Wan rendered in careful cross-hatching. His "
    "desk drawer held forty years of Hong Kong, folded into squares.<br><br>"
    "As a child I found the habit charming. As a teenager, I found it faintly embarrassing. “The phone knows "
    "where everything is,” I told him once, waving my screen at him like a winning card. He looked at it "
    "politely, the way you might look at a stranger's holiday photos. “The phone knows,” he agreed. “You don't.”<br><br>"
    "I understood him, finally, the summer he was ill. Sent to collect his medicine, I plotted the fastest "
    "route and followed my dot faithfully through streets I had walked a hundred times and could not have "
    "described to save my life. Waiting at the dispensary, I realised I did not know the name of a single shop "
    "I had passed. I had travelled like a parcel: delivered, but absent.<br><br>"
    "That evening I asked him to show me the drawer. He spread the maps across his bed like a dealer fanning "
    "cards, and talked for two hours: about the pier that became a highway, the theatre that became a bank, "
    "the alley where he had first held my grandmother's hand in the rain. None of it was on my phone. The city "
    "the phone showed me was accurate, up to date, and utterly without memory.<br><br>"
    "He is gone now, and the maps are mine. I have started adding to them, badly, in pencil: my school, my "
    "own noodle shop, the corner where my friends wait on Saturday mornings. My hand is clumsy and my stars "
    "are lopsided, but I am learning what he knew all along: that a place is not truly yours until you have "
    "paid it the compliment of attention."
)

PASSAGE_2 = (
    "<strong>In Praise of Boredom</strong><br><br>"
    "It has never been easier to avoid boredom. The moment a queue lengthens or a lesson drags, a universe of "
    "entertainment sits one thumb-swipe away. In an average day, many teenagers do not experience a single "
    "unfilled minute between waking and sleeping. This might sound like progress. A growing number of "
    "psychologists suspect it is quietly costing us something valuable.<br><br>"
    "Boredom, they argue, is not an absence but a signal: the mind announcing that it is under-occupied and "
    "ready to wander. And wandering minds do remarkable work. In studies where volunteers were given "
    "deliberately dull tasks, such as copying numbers from a telephone directory, they later produced markedly "
    "more creative ideas than volunteers who had been kept busy. The bored brain, starved of stimulation, "
    "begins to generate its own: daydreams, connections, plans, questions. Many writers and scientists have "
    "described their best ideas arriving not at the desk but in the shower, on a long walk, or staring out of "
    "a bus window: precisely the empty moments a smartphone now colonises.<br><br>"
    "None of this means screens are villains. The problem is not that entertainment exists, but that it has "
    "become the automatic response to the first flicker of restlessness, so the mind never reaches the "
    "productive stage of boredom at all. It is rescued too soon, like a muscle never allowed to tire and "
    "therefore never allowed to grow.<br><br>"
    "The remedy proposed is modest: not a digital detox or a return to some imagined simpler age, but the "
    "deliberate protection of small pockets of emptiness. A journey without headphones. A queue without a "
    "phone. Ten minutes on the sofa with nothing at all. In an economy that competes ferociously for every "
    "spare second of our attention, choosing occasionally to be bored may be less a failure of imagination "
    "than an act of quiet rebellion, and one of the cheapest investments a student can make in their own mind."
)

_RC = "Y9-10 Reading · "
READING = [
    dict(passage=PASSAGE_1, stem="What does the “blue dot” in the opening line represent?",
         options=O(("A", "The grandfather's drawing style"), ("B", "GPS navigation on a smartphone"),
                   ("C", "A landmark on the harbour"), ("D", "The narrator's school badge")),
         correct="B", strand="Reading: Fiction", concept=_RC + "interpreting a symbolic reference",
         explanation="The blue dot is the user's position on a phone map: the screen everyone else has 'surrendered' their direction-finding to."),
    dict(passage=PASSAGE_1, stem="“You don't.” What point is the grandfather making with these two words?",
         options=O(("A", "The narrator is too young to travel alone"),
                   ("B", "The phone's maps contain mistakes"),
                   ("C", "Relying on the phone means the narrator has no knowledge of their own"),
                   ("D", "He refuses to learn how to use new technology")),
         correct="C", strand="Reading: Fiction", concept=_RC + "inferring meaning from minimal dialogue",
         explanation="He concedes the phone 'knows', then points out that the knowledge belongs to the device, not to his grandchild."),
    dict(passage=PASSAGE_1, stem="Why does the narrator say “I had travelled like a parcel”?",
         options=O(("A", "They arrived efficiently but noticed nothing along the way"),
                   ("B", "They were carrying a package of medicine"),
                   ("C", "The journey was uncomfortable and crowded"),
                   ("D", "They got lost despite following the route")),
         correct="A", strand="Reading: Fiction", concept=_RC + "interpreting a simile",
         explanation="A parcel is delivered without awareness of its route: 'delivered, but absent' captures arriving without having truly seen anything."),
    dict(passage=PASSAGE_1, stem="What is the narrator's key criticism of the phone's map of the city?",
         options=O(("A", "It is often out of date"), ("B", "It drains the battery too quickly"),
                   ("C", "It misses the small streets of Sheung Wan"), ("D", "It is accurate but holds no memories")),
         correct="D", strand="Reading: Fiction", concept=_RC + "locating the pivotal contrast",
         explanation="The phone's city is 'accurate, up to date, and utterly without memory': its flaw is not error but emptiness."),
    dict(passage=PASSAGE_1, stem="Why does the narrator describe their own additions to the maps as “badly, in pencil”?",
         options=O(("A", "To show they regret inheriting the maps"),
                   ("B", "To show they are a humble beginner continuing the tradition"),
                   ("C", "To show pencil is better than ink for maps"),
                   ("D", "To show the maps are no longer useful")),
         correct="B", strand="Reading: Fiction", concept=_RC + "understanding tone and self-deprecation",
         explanation="The clumsy pencil marks show a beginner honestly taking up the grandfather's practice, not perfecting it."),
    dict(passage=PASSAGE_1, stem="Which statement best expresses the passage's central idea?",
         options=O(("A", "Technology should be banned for young people"),
                   ("B", "Old maps are more accurate than digital ones"),
                   ("C", "Truly knowing a place requires paying it real attention"),
                   ("D", "Grandparents and grandchildren rarely understand each other")),
         correct="C", strand="Reading: Fiction", concept=_RC + "identifying the theme",
         explanation="The final line states it directly: a place is not yours until you have 'paid it the compliment of attention'."),
    dict(passage=PASSAGE_2, stem="What is the writer's main argument?",
         options=O(("A", "Boredom is valuable and worth deliberately protecting"),
                   ("B", "Smartphones should be banned in schools"),
                   ("C", "Teenagers today are lazier than previous generations"),
                   ("D", "Entertainment is harmful to creativity")),
         correct="A", strand="Reading: Non-fiction", concept=_RC + "identifying the thesis of an argument",
         explanation="The passage argues boredom triggers creative thinking and recommends protecting 'small pockets of emptiness'."),
    dict(passage=PASSAGE_2, stem="The writer includes the telephone-directory study in order to:",
         options=O(("A", "show how boring life was before smartphones"),
                   ("B", "prove that copying tasks improve handwriting"),
                   ("C", "criticise psychologists' research methods"),
                   ("D", "provide research evidence that boredom boosts creative thinking")),
         correct="D", strand="Reading: Non-fiction", concept=_RC + "understanding the function of evidence",
         explanation="The dull-task volunteers later produced more creative ideas: experimental support for the boredom-creativity link."),
    dict(passage=PASSAGE_2, stem="In paragraph 2, “colonises” suggests that the smartphone:",
         options=O(("A", "politely shares the empty moments"), ("B", "makes the empty moments more enjoyable"),
                   ("C", "takes over territory that once belonged to daydreaming"), ("D", "creates new empty moments")),
         correct="C", strand="Reading: Non-fiction", concept=_RC + "evaluating a loaded word choice",
         explanation="'Colonise' means to occupy and take over: the phone seizes the mental territory where wandering thought used to happen."),
    dict(passage=PASSAGE_2, stem="What does the muscle comparison in paragraph 3 illustrate?",
         options=O(("A", "Exercise is as important as mental rest"),
                   ("B", "A mind rescued from boredom too quickly never develops its creative strength"),
                   ("C", "Being bored is physically tiring"),
                   ("D", "Entertainment makes the brain stronger")),
         correct="B", strand="Reading: Non-fiction", concept=_RC + "interpreting an analogy",
         explanation="A muscle must tire to grow; a mind must sit with restlessness to reach the productive stage of boredom."),
    dict(passage=PASSAGE_2, stem="Which of these best describes the writer's attitude to screens?",
         options=O(("A", "They are villains that must be removed from daily life"),
                   ("B", "They are harmless and the concern is exaggerated"),
                   ("C", "They are fine in themselves; the problem is using them at the first flicker of restlessness"),
                   ("D", "They are only a problem for teenagers")),
         correct="C", strand="Reading: Non-fiction", concept=_RC + "identifying a nuanced position",
         explanation="The writer explicitly says screens are not villains; the issue is the automatic reach for them, which prevents boredom doing its work."),
    dict(passage=PASSAGE_2, stem="Why does the writer call choosing to be bored “an act of quiet rebellion”?",
         options=O(("A", "Because schools forbid students from being bored"),
                   ("B", "Because it defies an economy built on capturing every second of attention"),
                   ("C", "Because parents disapprove of idle teenagers"),
                   ("D", "Because rebellion is always quiet")),
         correct="B", strand="Reading: Non-fiction", concept=_RC + "understanding the closing image",
         explanation="In an attention economy competing for every spare second, refusing to hand over those seconds is a small act of defiance."),
]

# ---- Listening (3 recordings, 10 Q) ----------------------------------------
_LI = "Listen to the recording, then choose the best answer."
_A1, _A2, _A3 = "listening1.m4a", "listening2.m4a", "listening3.m4a"

AUDIO_TITLES = {
    "listening1.m4a": "The Star Ferry",
    "listening2.m4a": "A Debate about AI Homework",
    "listening3.m4a": "Bamboo Scaffolding",
    "listening-zh.m4a": "短講一則 A Short Talk",
}

AUDIO = {
    "listening-zh.m4a": [("zh-CN-YunxiNeural", "-6%", "有人说，要认识香港，先要走进一间茶餐厅。茶餐厅被称为香港的平民食堂：一份餐蛋面、一杯丝袜奶茶，几十块钱就能吃得饱足。这里的食物东西合璧：菠萝包里其实没有菠萝，只是因为烤好的外皮像菠萝才得了这个名字；鸳鸯，是把咖啡和奶茶混在一起。茶餐厅还有自己的一套语言，比如走冰，意思就是不要冰。伙计写单快，上菜快，客人吃得也快，正好配合这个城市的节奏。在我看来，茶餐厅不只是吃饭的地方，它把香港人的灵活、效率和东西文化的融合，都盛在一个碟子里。")],
    _A1: [("en-GB-RyanNeural", "-4%",
        "Few journeys in the world offer so much for so little. The Star Ferry has carried passengers "
        "across Victoria Harbour for well over a century, and for many years it was the only practical way "
        "to cross between Hong Kong Island and Kowloon. Today, of course, the harbour can be crossed in "
        "minutes by tunnel or by train, and the ferry is no longer the fastest option. Yet millions of "
        "people still choose it every year. Some are tourists, but many are commuters who simply prefer "
        "ten minutes of sea air and skyline to a crowded carriage underground. "
        "The fleet itself has changed remarkably little. The double-ended boats still wear their green "
        "and white paint, and sailors still catch the mooring ropes with long poles, just as their "
        "grandfathers did. In a city famous for tearing down and rebuilding, the ferry has become "
        "something more than transport. It is a floating piece of memory.")],
    _A2: [
        ("en-US-AndrewNeural", "-4%", "I still think the school should simply ban AI tools for homework. If a chatbot writes "
                        "your essay, you have not learned to think; you have learned to copy. By the time exams "
                        "come, students who leaned on it will not be able to build an argument on their own."),
        ("en-US-AvaNeural", "-4%", "A ban sounds clean, but it is unenforceable; students will just use it secretly, "
                          "and the honest ones will be the only ones disadvantaged. I would rather we teach "
                          "people to use it responsibly: let it explain a concept or check your grammar, but "
                          "the thinking and the first draft must be your own."),
        ("en-US-AndrewNeural", "-4%", "So you would allow it with limits. How would a teacher ever know the limits were respected?"),
        ("en-US-AvaNeural", "-4%", "The same way we handle sources now: you declare it. A short note saying what you used "
                          "the tool for. Dishonesty is possible with any rule, but a clear declaration makes the "
                          "expectation visible."),
        ("en-US-AndrewNeural", "-4%", "On that we can agree. Whatever the policy allows, students should state openly when "
                        "and how they used the tool."),
    ],
    _A3: [("en-GB-SoniaNeural", "-4%",
        "Look up at almost any building site in Hong Kong and you will see something that has vanished from "
        "most modern cities: scaffolding made not of steel, but of bamboo. To many visitors it looks fragile, "
        "even alarming. In fact, bamboo scaffolding is light, inexpensive, and remarkably resilient; it "
        "flexes in typhoon winds where rigid structures crack, and a skilled team can wrap a building in it "
        "at astonishing speed. That skill, however, is precisely the problem. A master scaffolder trains for "
        "years, tying thousands of joints by hand, and fewer and fewer young workers are choosing to learn. "
        "The average age of the workforce climbs every year. Unless that changes, a craft that has shaped "
        "this city's skyline for generations may, within a single generation more, exist only in photographs. "
        "It would be a quiet loss, and, I would argue, an avoidable one.")],
}

LISTENING = [
    dict(stem=_LI + "\n\nWhat is the speaker's main point about the Star Ferry?", audio=_A1,
         options=O(("A", "It is still the fastest way to cross the harbour"),
                   ("B", "It endures because it offers something beyond mere transport"),
                   ("C", "It should be replaced by more tunnels"),
                   ("D", "It is mainly kept running for tourists")),
         correct="B", strand="Listening", concept="Y9-10 Listening · main idea of a talk",
         explanation="The speaker stresses that faster crossings exist, yet millions still choose the ferry: it has become 'a floating piece of memory', more than transport."),
    dict(stem=_LI + "\n\nAccording to the speaker, why do many commuters still choose the ferry?", audio=_A1,
         options=O(("A", "They prefer sea air and the skyline to a crowded carriage"),
                   ("B", "It is faster at rush hour"),
                   ("C", "It is free for regular passengers"),
                   ("D", "The trains stop running in the evening")),
         correct="A", strand="Listening", concept="Y9-10 Listening · stated reason",
         explanation="Many commuters 'simply prefer ten minutes of sea air and skyline to a crowded carriage underground'."),
    dict(stem=_LI + "\n\nWhich detail shows the fleet has changed very little?", audio=_A1,
         options=O(("A", "The boats now have electric engines"), ("B", "The piers have been rebuilt"),
                   ("C", "The boats keep their green and white paint, and ropes are still caught with poles"),
                   ("D", "The sailors wear modern uniforms")),
         correct="C", strand="Listening", concept="Y9-10 Listening · supporting detail",
         explanation="The speaker mentions the green and white paint and sailors catching mooring ropes with long poles, 'just as their grandfathers did'."),
    dict(stem=_LI + "\n\nWhat does the speaker mean by calling the ferry “a floating piece of memory”?", audio=_A1,
         options=O(("A", "The boats are old and slow"), ("B", "Passengers often forget their belongings"),
                   ("C", "The ferry only carries tourists now"),
                   ("D", "In a fast-changing city, the ferry keeps the past alive")),
         correct="D", strand="Listening", concept="Y9-10 Listening · interpreting figurative language",
         explanation="In 'a city famous for tearing down and rebuilding', the unchanged ferry preserves a piece of Hong Kong's past."),
    dict(stem=_LI + "\n\nWhat is the man's main concern about AI tools?", audio=_A2,
         options=O(("A", "They are too expensive for most students"), ("B", "They give wrong answers"),
                   ("C", "Students who rely on them will not learn to think for themselves"),
                   ("D", "They breach students' privacy")),
         correct="C", strand="Listening", concept="Y9-10 Listening · speaker's position in a discussion",
         explanation="He argues that if a chatbot writes the essay, the student learns to copy rather than to think, and will struggle in exams."),
    dict(stem=_LI + "\n\nWhy does the woman oppose an outright ban?", audio=_A2,
         options=O(("A", "She thinks AI writes better essays than students"),
                   ("B", "A ban would be unenforceable and would penalise only the honest"),
                   ("C", "Teachers voted against it"),
                   ("D", "The school cannot afford detection software")),
         correct="B", strand="Listening", concept="Y9-10 Listening · evaluating a counter-argument",
         explanation="She says a ban is unenforceable: students would use it secretly, leaving only the honest ones disadvantaged."),
    dict(stem=_LI + "\n\nWhat do the two speakers finally agree on?", audio=_A2,
         options=O(("A", "Students should declare when and how they used AI tools"),
                   ("B", "AI tools should be banned completely"),
                   ("C", "AI tools should be allowed without any rules"),
                   ("D", "Only teachers should use AI tools")),
         correct="A", strand="Listening", concept="Y9-10 Listening · synthesis (the point of agreement)",
         explanation="Both accept a disclosure rule: whatever the policy, students should state openly when and how they used the tool."),
    dict(stem=_LI + "\n\nWhich advantages of bamboo scaffolding does the lecturer mention?", audio=_A3,
         options=O(("A", "It is stronger than steel and lasts longer"),
                   ("B", "It never needs skilled workers"),
                   ("C", "It looks more attractive to visitors"),
                   ("D", "It is light, inexpensive, and flexes in typhoon winds")),
         correct="D", strand="Listening", concept="Y9-10 Listening · grouped details",
         explanation="The lecturer calls it light, inexpensive and remarkably resilient, flexing in typhoon winds where rigid structures crack."),
    dict(stem=_LI + "\n\nWhat problem threatens the craft's future?", audio=_A3,
         options=O(("A", "A shortage of bamboo"), ("B", "Fewer and fewer young workers are learning it"),
                   ("C", "New safety laws have banned it"), ("D", "It is too slow for modern building sites")),
         correct="B", strand="Listening", concept="Y9-10 Listening · identifying the central problem",
         explanation="A master trains for years, and fewer young workers are choosing to learn, so the workforce ages every year."),
    dict(stem=_LI + "\n\nWhich best describes the lecturer's attitude towards bamboo scaffolding?", audio=_A3,
         options=O(("A", "Alarmed by its danger"), ("B", "Dismissive of an outdated method"),
                   ("C", "Admiring, and concerned that the craft may be lost"), ("D", "Neutral and purely factual")),
         correct="C", strand="Listening", concept="Y9-10 Listening · speaker's tone and attitude",
         explanation="The lecturer praises the craft's qualities and calls its possible disappearance 'a quiet loss, and an avoidable one': admiration mixed with concern."),
]

# ---- Writing / Speaking / Chinese ------------------------------------------
CONTENT_WRITING = dict(
    type="writing",
    intro="Choose ONE of the two tasks below and type your answer in the box. Aim for about 220-300 words.",
    body=("Task 1: Write about a belief or opinion you once held strongly and later changed your mind about. "
          "Explain what you used to think, what changed, and what the experience taught you about how you form "
          "your views.\n\n"
          "Task 2: 'Social media does more harm than good for teenagers.' To what extent do you agree? Develop "
          "a structured argument with clear reasons and examples, and acknowledge at least one point on the "
          "other side."),
    hint="Plan before you write: a clear introduction, developed paragraphs and a conclusion. Leave two minutes to review your accuracy and word choice.",
    placeholder="Type your answer here; it will be saved for review…",
)

CONTENT_SPEAKING = dict(
    type="speaking",
    stem="Record a short spoken response (about 2 minutes).",
    body=("Speak about:\n"
          "• Your name, your current school and year group\n"
          "• A book, idea or experience that has genuinely changed the way you think, and how\n"
          "• An achievement you worked hard for, and what it took\n"
          "• What you would contribute to your next school, inside and outside the classroom\n\n"
          "Speak naturally and develop your points; this is a chance for your future school to hear how you think."),
)

CH_PASSAGE_TRAD = (
    "朋友的日程表排得密密麻麻：清晨游泳，放學補習，晚上還有網課。問他為甚麼把自己迫得這樣緊，他理直氣壯："
    "「停下來，就是浪費時間。」\n\n"
    "我卻想起中國畫裏的「留白」。高明的畫家從不把宣紙填滿，山與山之間留一段雲霧，魚與魚之間留一片清水。"
    "那些空白不是偷懶，而是讓整幅畫呼吸的地方。看畫的人站在空白前，反而看見了最多的東西。\n\n"
    "人的日子，恐怕也是同一個道理。腦袋需要空隙，新的念頭才有地方發芽；心情需要空隙，白天的經歷才能慢慢"
    "沉澱成自己的想法。整天被課表推着走的人，就像一幅塗得密不透風的畫，筆筆都用力，偏偏看不出重點。\n\n"
    "留白不等於躺平。畫家落筆前，心裏早有丘壑；懂得休息的人，也不是放棄努力，而是明白張弛有度，路才走得遠。"
    "真正的從容，是在該用力的地方用力，也敢在該留白的地方，安心地留一片白。"
)
CH_PASSAGE_SIMP = (
    "朋友的日程表排得密密麻麻：清晨游泳，放学补习，晚上还有网课。问他为什么把自己迫得这样紧，他理直气壮："
    "“停下来，就是浪费时间。”\n\n"
    "我却想起中国画里的“留白”。高明的画家从不把宣纸填满，山与山之间留一段云雾，鱼与鱼之间留一片清水。"
    "那些空白不是偷懒，而是让整幅画呼吸的地方。看画的人站在空白前，反而看见了最多的东西。\n\n"
    "人的日子，恐怕也是同一个道理。脑袋需要空隙，新的念头才有地方发芽；心情需要空隙，白天的经历才能慢慢"
    "沉淀成自己的想法。整天被课表推着走的人，就像一幅涂得密不透风的画，笔笔都用力，偏偏看不出重点。\n\n"
    "留白不等于躺平。画家落笔前，心里早有丘壑；懂得休息的人，也不是放弃努力，而是明白张弛有度，路才走得远。"
    "真正的从容，是在该用力的地方用力，也敢在该留白的地方，安心地留一片白。"
)

def _ch(stem_t, stem_s, opts_ts, correct, concept, explanation):
    return dict(
        passage=zh_blocks(CH_PASSAGE_TRAD.replace("\n\n", "<br><br>"), CH_PASSAGE_SIMP.replace("\n\n", "<br><br>")),
        stem=bilingual(stem_t, stem_s),
        options=O(*[(k, bilingual(t, s)) for k, (t, s) in opts_ts.items()]),
        correct=correct, strand="中文閱讀理解", concept="高中中文 · " + concept, explanation=explanation)

CHINESE = [
    _ch("朋友認為「停下來，就是浪費時間」，作者對這句話的態度是：", "朋友认为“停下来，就是浪费时间”，作者对这句话的态度是：",
        {"A": ("完全同意", "完全同意"), "B": ("不以為然，另有看法", "不以为然，另有看法"),
         "C": ("羨慕朋友的自律", "羡慕朋友的自律"), "D": ("覺得與自己無關", "觉得与自己无关")},
        "B", "內容理解：作者態度", "作者隨即以「我卻想起」帶出留白的道理，可見他並不認同朋友的說法。"),
    _ch("畫家在畫中「留白」，作者認為那些空白的作用是：", "画家在画中“留白”，作者认为那些空白的作用是：",
        {"A": ("節省筆墨和顏料", "节省笔墨和颜料"), "B": ("掩飾技巧不足", "掩饰技巧不足"),
         "C": ("讓整幅畫有呼吸的空間", "让整幅画有呼吸的空间"), "D": ("方便日後補畫", "方便日后补画")},
        "C", "內容理解：關鍵語句", "文中明言：那些空白不是偷懶，而是讓整幅畫呼吸的地方。"),
    _ch("作者把「整天被課表推着走的人」比作甚麼？", "作者把“整天被课表推着走的人”比作什么？",
        {"A": ("一幅塗得密不透風的畫", "一幅涂得密不透风的画"), "B": ("山間的雲霧", "山间的云雾"),
         "C": ("水裏的魚", "水里的鱼"), "D": ("落筆前的畫家", "落笔前的画家")},
        "A", "修辭理解：比喻", "文中寫道：就像一幅塗得密不透風的畫，筆筆都用力，偏偏看不出重點。"),
    _ch("第三段指出，腦袋和心情需要「空隙」，是為了：", "第三段指出，脑袋和心情需要“空隙”，是为了：",
        {"A": ("有時間玩樂放鬆", "有时间玩乐放松"), "B": ("讓新念頭發芽，讓經歷沉澱成想法", "让新念头发芽，让经历沉淀成想法"),
         "C": ("減少功課壓力", "减少功课压力"), "D": ("爭取更多睡眠", "争取更多睡眠")},
        "B", "內容理解：段意", "原文：腦袋需要空隙，新的念頭才有地方發芽；心情需要空隙，經歷才能沉澱成自己的想法。"),
    _ch("「留白不等於躺平」一句，作者想澄清的是：", "“留白不等于躺平”一句，作者想澄清的是：",
        {"A": ("躺平也是一種留白", "躺平也是一种留白"), "B": ("畫家其實不需要休息", "画家其实不需要休息"),
         "C": ("休息越多越好", "休息越多越好"), "D": ("懂得休息不是放棄努力，而是張弛有度", "懂得休息不是放弃努力，而是张弛有度")},
        "D", "內容理解：辨析概念", "作者隨後解釋：懂得休息的人不是放棄努力，而是明白張弛有度，路才走得遠。"),
    _ch("這篇文章的主旨是：", "这篇文章的主旨是：",
        {"A": ("學習中國畫需要天分", "学习中国画需要天分"),
         "B": ("日程排得越滿，成就越大", "日程排得越满，成就越大"),
         "C": ("生活如作畫，要懂得適當留白，張弛有度", "生活如作画，要懂得适当留白，张弛有度"),
         "D": ("補習和網課沒有意義", "补习和网课没有意义")},
        "C", "主旨理解", "全文由畫的留白推及生活，主張在用力與休息之間取得平衡，並非否定努力或補習。"),
]

CH_LISTENING = [
    dict(stem=bilingual("聆聽短講，然後回答問題。\n\n這段短講的主旨是什麼？", "聆听短讲，然后回答问题。\n\n这段短讲的主旨是什么？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("教大家做菠蘿包", "教大家做菠萝包")), ("B", bilingual("批評茶餐廳的服務", "批评茶餐厅的服务")), ("C", bilingual("介紹茶餐廳以及它反映的香港文化", "介绍茶餐厅以及它反映的香港文化")), ("D", bilingual("比較中西餐廳的優劣", "比较中西餐厅的优劣"))),
         correct="C", strand="中文聆聽理解", concept="高中中文 · 聆聽：主旨",
         explanation="說話人由茶餐廳的食物、語言和節奏，帶出它反映香港文化的看法。"),
    dict(stem=bilingual("關於菠蘿包，說話人說了什麼？", "关于菠萝包，说话人说了什么？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("裏面有菠蘿餡", "里面有菠萝馅")), ("B", bilingual("因外皮像菠蘿而得名", "因外皮像菠萝而得名")), ("C", bilingual("是從外國傳入的", "是从外国传入的")), ("D", bilingual("只在早上出售", "只在早上出售"))),
         correct="B", strand="中文聆聽理解", concept="高中中文 · 聆聽：細節（有菠蘿餡是常見誤解陷阱）",
         explanation="菠蘿包裏其實沒有菠蘿，只因烤好的外皮像菠蘿才得名。"),
    dict(stem=bilingual("短講中「走冰」的意思是：", "短讲中“走冰”的意思是："), audio="listening-zh.m4a",
         options=O(("A", bilingual("加多些冰", "加多些冰")), ("B", bilingual("邊走邊喝", "边走边喝")), ("C", bilingual("少放糖", "少放糖")), ("D", bilingual("不要冰", "不要冰"))),
         correct="D", strand="中文聆聽理解", concept="高中中文 · 聆聽：詞語理解（行業用語）",
         explanation="說話人解釋「走冰」的意思就是不要冰。"),
    dict(stem=bilingual("說話人對茶餐廳的態度是：", "说话人对茶餐厅的态度是："), audio="listening-zh.m4a",
         options=O(("A", bilingual("欣賞而親切", "欣赏而亲切")), ("B", bilingual("批評和不滿", "批评和不满")), ("C", bilingual("冷淡疏離", "冷淡疏离")), ("D", bilingual("半信半疑", "半信半疑"))),
         correct="A", strand="中文聆聽理解", concept="高中中文 · 聆聽：說話人態度",
         explanation="說話人以「平民食堂」、「盛在一個碟子裏」等語句流露欣賞和親切之情。"),
]

CH_SPEAKING = dict(
    type="speaking", maxSeconds=150,
    stem=bilingual("請用普通話介紹自己（大約兩分鐘）。", "请用普通话介绍自己（大约两分钟）。"),
    body=zh_blocks("可以說一說：\n• 你的名字、年級和學校\n• 一次你克服困難的經歷，你學到了什麼\n• 一本影響過你的書，或一個你關心的話題\n• 你希望在新學校有怎樣的發展",
                   "可以说一说：\n• 你的名字、年级和学校\n• 一次你克服困难的经历，你学到了什么\n• 一本影响过你的书，或一个你关心的话题\n• 你希望在新学校有怎样的发展"),
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
