# -*- coding: utf-8 -*-
"""HKS Baseline Assessment · Years 9-10 (current Y9-Y10 / G8-G9), version 3. 75 min core.

Parallel form of level_d_v1/v2: identical structure and timing, all-new content.
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
    dict(stem=_SYN + "\n\nPRUDENT", options=O(("A", "cautious"), ("B", "proud"), ("C", "reckless"), ("D", "wealthy")),
         correct="A", strand="Vocabulary: Synonyms", concept="Y9-10 Vocabulary · synonyms: prudent = cautious",
         explanation="Prudent means acting with care and thought for the future: cautious. Reckless is the opposite, and 'proud' is a sound-alike trap."),
    dict(stem=_SYN + "\n\nARDUOUS", options=O(("A", "passionate"), ("B", "gruelling"), ("C", "simple"), ("D", "lengthy")),
         correct="B", strand="Vocabulary: Synonyms", concept="Y9-10 Vocabulary · synonyms: arduous = gruelling",
         explanation="An arduous task demands great effort: gruelling. 'Passionate' confuses arduous with ardent, and a task can be lengthy without being hard."),
    dict(stem=_SYN + "\n\nELOQUENT", options=O(("A", "elegant"), ("B", "talkative"), ("C", "silent"), ("D", "articulate")),
         correct="D", strand="Vocabulary: Synonyms", concept="Y9-10 Vocabulary · synonyms: eloquent = articulate",
         explanation="Eloquent means expressing ideas fluently and persuasively: articulate. Being merely talkative says nothing about speaking well."),
    dict(stem=_SYN + "\n\nOMINOUS", options=O(("A", "reassuring"), ("B", "enormous"), ("C", "threatening"), ("D", "famous")),
         correct="C", strand="Vocabulary: Synonyms", concept="Y9-10 Vocabulary · synonyms: ominous = threatening",
         explanation="Ominous means suggesting that something bad is coming: threatening. Reassuring is closer to the opposite; 'enormous' is a sound-alike trap."),
    dict(stem=_ANT + "\n\nLETHARGIC", options=O(("A", "sluggish"), ("B", "energetic"), ("C", "peaceful"), ("D", "gloomy")),
         correct="B", strand="Vocabulary: Antonyms", concept="Y9-10 Vocabulary · antonyms: lethargic vs energetic",
         explanation="Lethargic means lacking energy; energetic means full of it. Sluggish is a synonym of lethargic, not its opposite."),
    dict(stem=_ANT + "\n\nNOVICE", options=O(("A", "beginner"), ("B", "student"), ("C", "expert"), ("D", "champion")),
         correct="C", strand="Vocabulary: Antonyms", concept="Y9-10 Vocabulary · antonyms: novice vs expert",
         explanation="A novice is someone new to a skill; an expert has mastered it. Beginner is a synonym of novice, not its opposite."),
    dict(stem=_ANT + "\n\nSOMBRE", options=O(("A", "cheerful"), ("B", "gloomy"), ("C", "formal"), ("D", "silent")),
         correct="A", strand="Vocabulary: Antonyms", concept="Y9-10 Vocabulary · antonyms: sombre vs cheerful",
         explanation="Sombre means dark and gloomy in mood; cheerful means bright and happy. Gloomy is a synonym of sombre, not its opposite."),
    dict(stem=_ANT + "\n\nACCELERATE", options=O(("A", "hasten"), ("B", "brake"), ("C", "swerve"), ("D", "decelerate")),
         correct="D", strand="Vocabulary: Antonyms", concept="Y9-10 Vocabulary · antonyms: accelerate vs decelerate",
         explanation="To accelerate is to speed up; to decelerate is to slow down. Hasten is a synonym of accelerate, and 'brake' is an action, not the precise opposite word."),
    dict(stem=_ANA + "\n\nAnthology is to poems as atlas is to ______.",
         options=O(("A", "countries"), ("B", "maps"), ("C", "explorers"), ("D", "globes")),
         correct="B", strand="Verbal Analogies", concept="Y9-10 Verbal Reasoning · analogies: collection to member",
         explanation="An anthology is a collection of poems; an atlas is a collection of maps. Countries are what maps show, not what an atlas contains."),
    dict(stem=_ANA + "\n\nArid is to desert as humid is to ______.",
         options=O(("A", "umbrella"), ("B", "drought"), ("C", "rainforest"), ("D", "temperature")),
         correct="C", strand="Verbal Analogies", concept="Y9-10 Verbal Reasoning · analogies: characteristic to place",
         explanation="Arid (dry) is the defining condition of a desert; humid (moist) is the defining condition of a rainforest."),
    dict(stem=_ANA + "\n\nReticent is to talkative as lethargic is to ______.",
         options=O(("A", "energetic"), ("B", "sleepy"), ("C", "sluggish"), ("D", "medical")),
         correct="A", strand="Verbal Analogies", concept="Y9-10 Verbal Reasoning · analogies: opposites",
         explanation="Reticent and talkative are opposites, so the answer is the opposite of lethargic (sluggish and tired): energetic. Sleepy and sluggish are synonyms of lethargic."),
    dict(stem=_ANA + "\n\nTerrified is to afraid as furious is to ______.",
         options=O(("A", "calm"), ("B", "frightened"), ("C", "violent"), ("D", "annoyed")),
         correct="D", strand="Verbal Analogies", concept="Y9-10 Verbal Reasoning · analogies: intensity (extreme to mild)",
         explanation="Terrified is an extreme degree of afraid; furious is an extreme degree of annoyed."),
    dict(stem=_ANA + "\n\nTributary is to river as branch is to ______.",
         options=O(("A", "leaf"), ("B", "forest"), ("C", "tree"), ("D", "root")),
         correct="C", strand="Verbal Analogies", concept="Y9-10 Verbal Reasoning · analogies: part to whole",
         explanation="A tributary is a smaller stream joined to a river; a branch is a smaller limb joined to a tree. A leaf grows on the branch itself."),
    dict(stem=_SC + "\n\nThe footbridge was declared ______ after the typhoon and closed until engineers could inspect it.",
         options=O(("A", "spacious"), ("B", "hazardous"), ("C", "ornamental"), ("D", "efficient")),
         correct="B", strand="Sentence Completion", concept="Y9-10 Reading · sentence completion: cause-and-effect clue (ISEE style)",
         explanation="Closing the bridge until inspection is the effect of declaring it hazardous (dangerous). The other words give no reason to close it."),
    dict(stem=_SC + "\n\nHer answer was deliberately ______, leaving the reporters unsure of her true intentions.",
         options=O(("A", "vague"), ("B", "precise"), ("C", "truthful"), ("D", "loud")),
         correct="A", strand="Sentence Completion", concept="Y9-10 Reading · sentence completion: definition clue (ISEE style)",
         explanation="Leaving listeners unsure of her meaning is the definition of a vague answer. A precise answer would do the opposite."),
    dict(stem=_SC2 + "\n\nThe drought left the reservoir so ______ that officials imposed ______ limits on water use.",
         options=O(("A", "full … generous"), ("B", "murky … flexible"), ("C", "depleted … strict"), ("D", "cold … seasonal")),
         correct="C", strand="Sentence Completion", concept="Y9-10 Reading · double-blank with logical consistency (ISEE Upper style)",
         explanation="A drought would leave the reservoir depleted (drained), and the natural response to scarce water is strict limits. The other pairs break the cause-and-effect chain."),
    dict(stem=_SC2 + "\n\nAlthough his tone throughout the meeting was ______, the content of his letter was anything but ______.",
         options=O(("A", "courteous … polite"), ("B", "angry … furious"), ("C", "formal … written"), ("D", "hesitant … uncertain")),
         correct="A", strand="Sentence Completion", concept="Y9-10 Reading · double-blank with contrast signal (ISEE Upper style)",
         explanation="'Although' plus 'anything but' demands a contrast: his spoken tone was courteous, yet the letter was not polite at all. The other pairs give no contrast."),
    dict(stem=_SC2 + "\n\nRather than ______ the criticism, the architect ______ it, rebuilding the design from the ground up.",
         options=O(("A", "accepting … rejected"), ("B", "dismissing … embraced"), ("C", "inviting … welcomed"), ("D", "publishing … printed")),
         correct="B", strand="Sentence Completion", concept="Y9-10 Reading · double-blank with reversal signal (ISEE Upper style)",
         explanation="'Rather than' opposes the two verbs: instead of dismissing the criticism she embraced it, which fits rebuilding the design entirely. Accepting/rejected reverses the logic of the sentence."),
    dict(stem=_GR + "\n\nNeither of the two answers ______ correct, so the point was awarded to no one.",
         options=O(("A", "were"), ("B", "are"), ("C", "was"), ("D", "have been")),
         correct="C", strand="Grammar & Cloze", concept="Y9 Grammar · agreement: 'neither of' + singular verb",
         explanation="'Neither' is the subject and is singular; 'of the two answers' is a prepositional phrase: neither … was correct."),
    dict(stem=_GR + "\n\nHardly ______ the match begun when rain stopped play.",
         options=O(("A", "has"), ("B", "did"), ("C", "would"), ("D", "had")),
         correct="D", strand="Grammar & Cloze", concept="Y10 Grammar · inversion after 'hardly' with the past perfect",
         explanation="'Hardly … when' takes inversion with the past perfect: Hardly had the match begun when rain stopped play."),
    dict(stem=_GR + "\n\nThe number of applicants ______ risen sharply since the new campus opened.",
         options=O(("A", "have"), ("B", "has"), ("C", "are"), ("D", "were")),
         correct="B", strand="Grammar & Cloze", concept="Y10 Grammar · 'the number of' is singular",
         explanation="'The number of applicants' takes a singular verb: the number has risen. ('A number of applicants have…' would be plural.)"),
    dict(stem=_LG + "\n\nNo metals are transparent. All the coins in this box are metal. Which statement MUST be true?",
         options=O(("A", "No coin in this box is transparent"), ("B", "Some coins in this box are transparent"),
                   ("C", "All transparent objects are glass"), ("D", "Every metal object is a coin")),
         correct="A", strand="Verbal Logic", concept="Y9-10 Reasoning · syllogism with a negative premise",
         explanation="The coins are metal, and no metals are transparent, so no coin in the box is transparent. The other statements go beyond the premises."),
    dict(stem=_LG + "\n\nFour clubs K, L, M and N each rehearse on a different day from Monday to Thursday. M rehearses on the day immediately before N. L rehearses on Thursday. K does not rehearse on Monday. On which day does K rehearse?",
         options=O(("A", "Monday"), ("B", "Tuesday"), ("C", "Wednesday"), ("D", "It cannot be determined")),
         correct="C", strand="Verbal Logic", concept="Y9-10 Reasoning · scheduling deduction",
         explanation="L takes Thursday, so M and N (consecutive) fit Monday-Tuesday or Tuesday-Wednesday. If they took Tuesday-Wednesday, K would be forced onto Monday, which is not allowed. So M is Monday, N is Tuesday, and K rehearses on Wednesday."),
    dict(stem=_LG + "\n\nSome paintings in the gallery are watercolours. All watercolours in the gallery are framed. Which statement MUST be true?",
         options=O(("A", "All paintings in the gallery are framed"), ("B", "Some framed works are oil paintings"),
                   ("C", "No oil paintings are framed"), ("D", "Some paintings in the gallery are framed")),
         correct="D", strand="Verbal Logic", concept="Y9-10 Reasoning · syllogism: some/all chains",
         explanation="The paintings that are watercolours must be framed, so at least some paintings in the gallery are framed. Nothing is known about the rest."),
    dict(stem=_LG + "\n\nIn a code, GARDEN is written as FZQCDM. Using the same code, how is PLANT written?",
         options=O(("A", "QMBOU"), ("B", "OKZMS"), ("C", "OKZNS"), ("D", "PKZMS")),
         correct="B", strand="Verbal Logic", concept="Y9-10 Reasoning · letter-shift code (one place backwards)",
         explanation="Each letter moves back one place (G to F, A to Z, R to Q …), so PLANT becomes OKZMS. QMBOU shifts forward one place instead."),
]

# ---- Non-Verbal Reasoning (20 = 14 CAT4-engine + 6 GL-style) ----------------
_SEQ = "Look at the four pictures in the top row. Work out the pattern, then choose the picture (A-E) that belongs in the empty box."
_CODE = "Each picture on the left has a two-letter code. Work out what each letter stands for, then choose the code for the picture marked '?'."

def _encl(kind, n):
    """Outline square or circle enclosing n small dots."""
    def draw(cx, cy):
        outline = square(cx, cy, 24, "none") if kind == "s" else circle(cx, cy, 24, "none")
        return outline + dots(cx, cy, n, 3.4)
    return draw

def _trio(n, fill):
    """A row of n small triangles with the given fill."""
    xs = {2: (-12, 12), 3: (-17, 0, 17)}[n]
    r = 11 if n == 2 else 10
    return lambda cx, cy: "".join(triangle(cx + dx, cy, r, fill) for dx in xs)

NONVERBAL = nvr_from_json("level-d", 3) + [
    dict(stem=_SEQ, correct="E", strand="Figure Series (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM series style) · two rules: the outline alternates square/circle AND the dots decrease",
         explanation="Two rules run together: the outline alternates square, circle, square, circle (so next is a SQUARE) AND the dots inside decrease 6, 5, 4, 3 (so next holds 2). Only E has both: a square with 2 dots. A has the right dots in the wrong outline.",
         fig=seq_fig([_encl("s", 6), _encl("c", 5), _encl("s", 4), _encl("c", 3)],
                     [_encl("c", 2), _encl("s", 3), _encl("s", 1), _encl("c", 3), _encl("s", 2)])),
    dict(stem=_SEQ, correct="A", strand="Figure Series (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM series style) · two interleaved series (alternating shapes, each with its own rotation)",
         explanation="Two series are interleaved: the half-shaded squares (positions 1 and 3) turn 90 degrees clockwise each time they appear (shaded left, then top), and the half-shaded circles (positions 2 and 4) do the same (shaded right, then bottom). Position 5 is a square, turned 90 degrees on from position 3: shaded on the RIGHT.",
         fig=seq_fig([cell(halfsquare, 16, 0), cell(halfcircle, 17, 180), cell(halfsquare, 16, 90), cell(halfcircle, 17, 270)],
                     [cell(halfsquare, 16, 180), cell(halfcircle, 17, 0), cell(halfsquare, 16, 270),
                      cell(halfsquare, 16, 0), cell(halfcircle, 17, 90)])),
    dict(stem=_SEQ, correct="C", strand="Figure Series (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM series style) · anticlockwise rotation of a chiral shape with a mirror trap",
         explanation="The flag shape turns 90 degrees ANTICLOCKWISE each step (180, 90, 0, 270), so the next picture wraps back to 180. D looks like the answer but is a mirror image, which no rotation can ever produce.",
         fig=seq_fig([cell(fshape, 9, 180), cell(fshape, 9, 90), cell(fshape, 9, 0), cell(fshape, 9, 270)],
                     [cell(fshape, 9, 270), cell(fshape, 9, 0), cell(fshape, 9, 180),
                      cell(fshape, 9, 180, mirror=True), cell(fshape, 9, 90)])),
    dict(stem=_CODE, correct="D", strand="Figure Codes (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM codes style) · first letter = count, second letter = shading",
         explanation="J means two triangles and K means three; U means black and W means white. The mystery picture is THREE BLACK triangles: KU.",
         fig=codes_fig([(_trio(2, INK), "JU"), (_trio(3, "none"), "KW"), (_trio(2, "none"), "JW")],
                       _trio(3, INK)),
         options=O(("A", "JU"), ("B", "JW"), ("C", "KW"), ("D", "KU"), ("E", "KV"))),
    dict(stem=_CODE, correct="B", strand="Figure Codes (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM codes style) · first letter = shape family, second letter = size",
         explanation="R means pentagon and S means hexagon; F means large and G means small. The mystery picture is a LARGE HEXAGON: SF.",
         fig=codes_fig([(cell(pentagon, 22, "none"), "RF"), (cell(hexagon, 14, "none"), "SG"), (cell(pentagon, 14, "none"), "RG")],
                       cell(hexagon, 22, "none")),
         options=O(("A", "RF"), ("B", "SF"), ("C", "RG"), ("D", "SG"), ("E", "TF"))),
    dict(stem=_CODE, correct="E", strand="Figure Codes (GL style)",
         concept="Y9-10 Non-Verbal Reasoning (GL/CEM codes style) · first letter = shading, second letter = direction",
         explanation="L means a black triangle and M means a white one; X means pointing up, Y pointing right, Z pointing down. The mystery picture is a WHITE triangle pointing DOWN: MZ.",
         fig=codes_fig([(cell(triangle, 16, INK, 0), "LX"), (cell(triangle, 16, "none", 90), "MY"),
                        (cell(triangle, 16, INK, 180), "LZ"), (cell(triangle, 16, "none", 0), "MX")],
                       cell(triangle, 16, "none", 180)),
         options=O(("A", "LZ"), ("B", "MX"), ("C", "MY"), ("D", "LX"), ("E", "MZ"))),
]

# ---- Mathematics (15: 7 short incl. 3 quantitative comparisons + 8 story) ---
_QC = ("Compare Quantity A and Quantity B, then choose:\n"
       "A) Quantity A is greater   B) Quantity B is greater\n"
       "C) The two quantities are equal   D) It cannot be determined from the information given\n\n")
_QC_OPTS = O(("A", "Quantity A is greater"), ("B", "Quantity B is greater"),
             ("C", "The two quantities are equal"), ("D", "It cannot be determined"))

MATHS = [
    # short form
    dict(stem="Work out 5<sup>3</sup> × 5",
         options=O(("A", "125"), ("B", "625"), ("C", "15"), ("D", "3125")),
         correct="B", strand="Number", concept="Y8 Number · index laws: add the powers (5 = 5¹)",
         explanation="5³ × 5¹ = 5⁴ = 625. Multiplying the indices (3 × 1 = 3, giving 125) is the classic error; 3125 is 5⁵."),
    dict(stem="Solve x/3 + 5 = 11",
         options=O(("A", "x = 2"), ("B", "x = 6"), ("C", "x = 18"), ("D", "x = 48")),
         correct="C", strand="Algebra", concept="Y8 Algebra · two-step equation with a fraction",
         explanation="x/3 = 6, so x = 18. Getting x = 2 comes from dividing 6 by 3 instead of multiplying; 48 comes from adding 5 before multiplying."),
    dict(stem="HK$180 is shared between two sisters in the ratio 4 : 5. How much is the SMALLER share?",
         options=O(("A", "HK$80"), ("B", "HK$90"), ("C", "HK$100"), ("D", "HK$45")),
         correct="A", strand="Number", concept="Y8 Ratio · sharing in a given ratio",
         explanation="There are 9 parts, each worth 180 ÷ 9 = HK$20, so the shares are HK$80 and HK$100. HK$90 splits the money in half and ignores the ratio; HK$100 is the LARGER share."),
    dict(stem="What is the nth term of the sequence 20, 17, 14, 11, …?",
         options=O(("A", "3n + 17"), ("B", "20 − 3n"), ("C", "n − 3"), ("D", "23 − 3n")),
         correct="D", strand="Algebra", concept="Y8 Sequences · nth term of a decreasing linear sequence",
         explanation="The sequence goes DOWN in 3s, so the rule involves −3n; when n = 1 it must give 20, so it is 23 − 3n. Checking 3n + 17 at n = 1 gives 20 but at n = 2 gives 23, not 17."),
    dict(stem=_QC + "Quantity A: 20% of 45\nQuantity B: 45% of 20",
         options=_QC_OPTS,
         correct="C", strand="Quantitative Comparison", concept="Y8 Percentages · a% of b equals b% of a (ISEE style)",
         explanation="20% of 45 = 9 and 45% of 20 = 9: the quantities are equal, because a% of b and b% of a are both ab/100. Assuming the bigger percentage must win is the trap."),
    dict(stem=_QC + "a < b < 0\n\nQuantity A: a × b\nQuantity B: 0",
         options=_QC_OPTS,
         correct="A", strand="Quantitative Comparison", concept="Y8 Number · multiplying two negative numbers (ISEE style)",
         explanation="a and b are both negative, and the product of two negative numbers is positive, so a × b > 0. Assuming that numbers less than zero give a product less than zero is the trap."),
    dict(stem=_QC + "The mean of a and b is 10.\n\nQuantity A: a\nQuantity B: 10",
         options=_QC_OPTS,
         correct="D", strand="Quantitative Comparison", concept="Y9 Statistics · quantitative comparison with an unfixed value (ISEE style)",
         explanation="Only a + b = 20 is known. If a = 15 and b = 5, Quantity A is greater; if a = 5 and b = 15, Quantity B is greater; if a = b = 10 they are equal. It cannot be determined."),
    # story form
    dict(stem="A rectangular park measures 12 m by 9 m. A straight path runs corner to corner, as shown. How long is the path?",
         fig=right_triangle_fig("12 m", "9 m", "? m"),
         options=O(("A", "10.5 m"), ("B", "15 m"), ("C", "21 m"), ("D", "225 m")),
         correct="B", strand="Problem Solving", concept="Y9 Geometry · Pythagoras' theorem (finding the hypotenuse)",
         explanation="12² + 9² = 144 + 81 = 225, and the square root of 225 is 15 m. Adding the two sides gives 21 m (walking round the edge), and 225 forgets the square root."),
    dict(stem="Concert tickets cost HK$150 for adults and HK$80 for children. A group buys 6 tickets in total and pays HK$760. How many CHILD tickets did they buy?",
         options=O(("A", "2"), ("B", "3"), ("C", "4"), ("D", "5")),
         correct="A", strand="Problem Solving", concept="Y9 Algebra · setting up simultaneous conditions",
         explanation="With a adults: 150a + 80(6 − a) = 760, so 70a + 480 = 760 and a = 4. That leaves 6 − 4 = 2 children. Check: HK$600 + HK$160 = HK$760."),
    dict(stem="A 1.5 kg bag of rice costs HK$27. At the same price per kilogram, how much would 4 kg cost?",
         options=O(("A", "HK$40.50"), ("B", "HK$54"), ("C", "HK$72"), ("D", "HK$108")),
         correct="C", strand="Problem Solving", concept="Y8 Ratio & Rates · unitary method (price per kg)",
         explanation="27 ÷ 1.5 = HK$18 per kg, so 4 kg costs 4 × 18 = HK$72. HK$108 treats HK$27 as the price of ONE kilogram; HK$54 only doubles the bag (3 kg)."),
    dict(stem="Mrs Wong invests HK$12,000 at 3.5% simple interest per year. How much INTEREST does she earn over 2 years?",
         options=O(("A", "HK$420"), ("B", "HK$12,840"), ("C", "HK$1,680"), ("D", "HK$840")),
         correct="D", strand="Problem Solving", concept="Y9 Percentages · simple interest over several years",
         explanation="3.5% of HK$12,000 is HK$420 per year, so 2 years earn 2 × 420 = HK$840. HK$12,840 is the final balance, not the interest, and HK$1,680 doubles the interest again."),
    dict(stem="A circular helipad has a radius of 14 m. Taking π as 22/7, what is the CIRCUMFERENCE of the helipad?",
         options=O(("A", "44 m"), ("B", "616 m"), ("C", "88 m"), ("D", "28 m")),
         correct="C", strand="Problem Solving", concept="Y9 Geometry · circumference of a circle",
         explanation="Circumference = 2πr = 2 × 22/7 × 14 = 88 m. 616 is the AREA calculation (πr²), 44 stops at πr, and 28 is just the diameter."),
    dict(stem="The spinner shown has 9 equal sectors. What is the probability that one spin lands on a sector marked Y?",
         fig=spinner([("G", 2, "#c9d6e4"), ("Y", 4, "#eef2f8"), ("P", 3, "#72AFDB")]),
         options=O(("A", "4/9"), ("B", "4/5"), ("C", "1/3"), ("D", "5/9")),
         correct="A", strand="Problem Solving", concept="Y8 Probability · probability from a diagram",
         explanation="4 of the 9 equal sectors are marked Y: 4/9. 4/5 compares Y with only the non-Y sectors, 1/3 counts the three LABELS instead of the sectors, and 5/9 is the probability of NOT landing on Y."),
    dict(stem="The graph shows a delivery van's journey. Distance from the depot (km) is plotted against time (hours). What was the van's speed during the SECOND hour?",
         fig=line_graph(["0", "1", "2", "3"], [0, 30, 90, 90], 100, 20, unit="km"),
         options=O(("A", "30 km/h"), ("B", "90 km/h"), ("C", "45 km/h"), ("D", "60 km/h")),
         correct="D", strand="Problem Solving", concept="Y9 Graphs · reading speed from a distance-time graph",
         explanation="Between hour 1 and hour 2 the distance rises from 30 km to 90 km: 60 km/h. 30 km/h is the FIRST hour's speed, 90 km is a distance reading, and the flat final section means the van was parked."),
    dict(stem="The bar chart shows how many books four classes read in a term. How many MORE books did the top class read than the class that read fewest?",
         fig=bar_chart(["8A", "8B", "8C", "8D"], [24, 32, 16, 28], 40, 8),
         options=O(("A", "8"), ("B", "16"), ("C", "48"), ("D", "24")),
         correct="B", strand="Problem Solving", concept="Y8 Statistics · reading a bar chart, then finding the range",
         explanation="The most is 8B with 32 and the fewest is 8C with 16: 32 − 16 = 16. 48 ADDS the two bars instead of subtracting, and 8 compares the wrong pair of classes."),
]

# ---- Reading Comprehension (12) --------------------------------------------
PASSAGE_1 = (
    "<strong>The Watch Mender</strong><br><br>"
    "The sign above my grandfather's shop said 'Watch Repairs' in gold letters that had half flaked away, "
    "which was fitting, because his customers were half gone too. Phones told the time now, he said, the way "
    "vending machines made tea: accurately, and without caring.<br><br>"
    "I was sent to help him on Saturdays the year I turned thirteen, a punishment, I assumed, for my report "
    "card. The shop was narrow as a corridor and smelled of oil and old carpet. All day, men and women his "
    "age brought him watches that had stopped: wedding watches, retirement watches, watches with initials on "
    "the back worn almost to nothing.<br><br>"
    "At first I thought the work was about the watches. It took me months to see my mistake. When Mrs Leung "
    "brought in her late husband's watch, my grandfather spent four days on a repair he priced at eighty "
    "dollars. I had seen the parts list; the parts alone cost more. When I pointed this out, with all my "
    "thirteen-year-old confidence, he did not look up from the bench. 'I am not charging her for the parts,' "
    "he said. 'I am charging her what she can pay. The ticking is worth more than either.' Then he bent back "
    "over the movement, as though the matter were settled, and for him it was.<br><br>"
    "His bench was a city of small drawers, and he worked under a lamp with a loupe screwed into one eye, his "
    "big hands turning suddenly delicate. Customers rarely hurried him; they seemed to understand they were "
    "paying for the one thing no factory could supply, which was time taken over something that mattered. "
    "A watch, he told me once, is a heart you can open. Everything "
    "inside it wants to run down; the art is in the winding, the small daily attention. People, he said, were "
    "not so different.<br><br>"
    "I did not become a watchmaker. Nobody does, any more. But I noticed, that year, that he never once asked "
    "about my grades, and that my marks rose anyway, in the shop's unhurried air, my homework spread at the "
    "end of his bench while rain ticked on the awning. Attention, it turned out, was contagious.<br><br>"
    "His own watch came to me two winters later. It is nothing special: steel, scratched, older than my "
    "mother. It loses a minute a week, and any shop could correct that, but I have learned what a minute is "
    "worth. Every morning I wind it seven half-turns, the way he did, and for as long as it ticks on my "
    "wrist, some small, stubborn part of him keeps time."
)

PASSAGE_2 = (
    "<strong>The Myth of Multitasking</strong><br><br>"
    "Somewhere between the group chat, the lecture video, the playlist and the half-written essay, the "
    "modern student has arrived at a flattering belief: that we are a generation of multitaskers, able to "
    "run four tasks at once the way a computer runs four programs. Psychologists have spent two decades "
    "testing this belief. Their verdict is inconvenient.<br><br>"
    "Strictly speaking, the brain does not multitask; it switches. Attention is less like a floodlight than "
    "a spotlight, swinging from one task to another, and each swing has a price that researchers call the "
    "switching cost: a moment of blankness while the brain reloads the rules of the task it has just "
    "returned to. In laboratory studies, people who alternate between two problems consistently take longer, "
    "and make more errors, than people who finish one and then start the other. One widely quoted estimate "
    "puts the time lost to heavy task-switching as high as forty per cent. What multitaskers experience as "
    "busyness is often just the friction of turning around. The cost is easy to miss, because each single "
    "switch feels instant; only the total, measured across an evening of homework, shows how much of the hour "
    "has quietly leaked away.<br><br>"
    "The more troubling finding concerns practice. It seems reasonable that heavy multitaskers should at "
    "least become good at it, and researchers at one American university expected to find exactly that. They "
    "found the opposite. The heaviest media multitaskers performed WORST at filtering out irrelevant "
    "information, and worse even at switching itself. The habit does not train the skill; it erodes it.<br><br>"
    "To be fair, not every kind of doubling-up deserves the lecture. Music while jogging, a podcast while "
    "washing dishes: when one task is automatic, the spotlight is not really being asked to split. The "
    "costly combinations are the ones that compete for the same beam: messaging while reading, video while "
    "writing, anything at all while revising. A fair test is honesty about which task is truly automatic: if "
    "both of them need words, both of them need the beam.<br><br>"
    "The remedy is unfashionably simple. Choose one thing; give it twenty or thirty undivided minutes; let "
    "the phone wait in another room, where its silence cannot be checked at a glance. Students who try this "
    "usually discover the same secret: the work takes less time, not more, because none of it is spent "
    "turning around. In an age that treats a divided attention as proof of importance, the undivided hour "
    "has become a kind of superpower, and it is available, unusually for superpowers, to absolutely anyone."
)

_RC = "Y9-10 Reading · "
READING = [
    dict(passage=PASSAGE_1, stem="'A watch is a heart you can open.' In the passage as a whole, what idea does this image carry?",
         options=O(("A", "Watch repair is a dangerous and delicate trade"), ("B", "Old watches are more valuable than new ones"),
                   ("C", "Like hearts, watches and people are kept going by small daily acts of attention"), ("D", "Doctors and watchmakers need the same training")),
         correct="C", strand="Reading: Fiction", concept=_RC + "interpreting the controlling metaphor",
         explanation="The grandfather extends the image himself: everything wants to run down, 'the art is in the winding, the small daily attention', and 'people were not so different'."),
    dict(passage=PASSAGE_1, stem="What does the Mrs Leung episode chiefly reveal about the grandfather?",
         options=O(("A", "He was careless with money and often made losses"), ("B", "He valued what the watch meant to her far above any profit"),
                   ("C", "He preferred difficult repairs to simple ones"), ("D", "He wanted to impress his grandchild with his generosity")),
         correct="B", strand="Reading: Fiction", concept=_RC + "understanding the function of an anecdote",
         explanation="He knowingly charged less than the parts cost, 'charging her what she can pay', because 'the ticking is worth more than either': the watch's meaning outweighed the money."),
    dict(passage=PASSAGE_1, stem="The grandfather says phones tell the time 'accurately, and without caring'. What point is he making?",
         options=O(("A", "Phones frequently show the wrong time"), ("B", "Accuracy is not the only thing that matters; care and meaning matter more"),
                   ("C", "Old people cannot learn to use new devices"), ("D", "Watches keep better time than phones")),
         correct="B", strand="Reading: Fiction", concept=_RC + "inferring meaning from a compressed remark",
         explanation="He concedes the phones' accuracy; his objection is what they lack. Like the vending-machine tea, the result is correct but empty of care."),
    dict(passage=PASSAGE_1, stem="Why, according to the narrator, did their school marks rise that year?",
         options=O(("A", "The grandfather checked their homework every Saturday"), ("B", "They were frightened of another punishment"),
                   ("C", "They had extra tuition after the shop closed"), ("D", "Working in the shop's calm, attentive atmosphere rubbed off on them")),
         correct="D", strand="Reading: Fiction", concept=_RC + "locating the pivotal explanation",
         explanation="He 'never once asked about my grades, and my marks rose anyway, in the shop's unhurried air': the narrator concludes that 'attention, it turned out, was contagious'."),
    dict(passage=PASSAGE_1, stem="Which best describes the narrator's tone in the passage?",
         options=O(("A", "Fond and quietly grieving, looking back with understanding"), ("B", "Bitter about wasted Saturdays"),
                   ("C", "Amused and mocking towards an eccentric old man"), ("D", "Detached and strictly factual")),
         correct="A", strand="Reading: Fiction", concept=_RC + "identifying tone",
         explanation="The loving detail, the gentle humour about the punishment, and the ending after his death combine affection, loss and adult understanding."),
    dict(passage=PASSAGE_1, stem="The narrator could have the watch's slow timekeeping corrected, but chooses not to. Why does the passage end this way?",
         options=O(("A", "Repairs have become too expensive since the shop closed"), ("B", "The narrator never learned how to adjust a watch"),
                   ("C", "Winding the imperfect watch daily keeps the grandfather's habit of care, and so his memory, alive"), ("D", "The watch is too fragile to be opened again")),
         correct="C", strand="Reading: Fiction", concept=_RC + "understanding the closing image",
         explanation="'I have learned what a minute is worth': the daily seven half-turns repeat the grandfather's ritual of attention, so 'some small, stubborn part of him keeps time'."),
    dict(passage=PASSAGE_2, stem="Which best states the writer's overall thesis?",
         options=O(("A", "Computers are better at multitasking than people"),
                   ("B", "Students today are lazier than earlier generations"),
                   ("C", "Multitasking is largely an illusion: switching between tasks costs time, errors and skill"),
                   ("D", "Phones should be banned from schools entirely")),
         correct="C", strand="Reading: Non-fiction", concept=_RC + "identifying the thesis of an argument",
         explanation="The passage argues the brain switches rather than multitasks, that switching carries costs, and that single-tasking is the remedy."),
    dict(passage=PASSAGE_2, stem="The writer describes attention as 'less like a floodlight than a spotlight'. What does this comparison show?",
         options=O(("A", "Attention lights up everything around us at once"),
                   ("B", "Attention is narrow and can only truly cover one thing at a time"),
                   ("C", "Studying is easier in a brightly lit room"),
                   ("D", "Some people naturally have wider attention than others")),
         correct="B", strand="Reading: Non-fiction", concept=_RC + "interpreting an analogy",
         explanation="A floodlight covers everything; a spotlight picks out one spot and must swing to reach another. The image explains why 'multitasking' is really rapid switching."),
    dict(passage=PASSAGE_2, stem="The writer includes the study of heavy media multitaskers in order to:",
         options=O(("A", "show that practising multitasking makes people worse at it, not better"),
                   ("B", "prove that American universities set too much homework"),
                   ("C", "suggest that some people are born multitaskers"),
                   ("D", "demonstrate that laboratory studies cannot be trusted")),
         correct="A", strand="Reading: Non-fiction", concept=_RC + "understanding the function of evidence",
         explanation="The researchers expected practice to improve the skill and 'found the opposite': the heaviest multitaskers filtered and switched worst. 'The habit does not train the skill; it erodes it.'"),
    dict(passage=PASSAGE_2, stem="Which best captures the writer's position on listening to music while jogging?",
         options=O(("A", "It is exactly as harmful as messaging while reading"),
                   ("B", "It should be saved as a reward for finished work"),
                   ("C", "It is acceptable, because an automatic task does not compete for the same attention"),
                   ("D", "It is the main cause of sporting injuries")),
         correct="C", strand="Reading: Non-fiction", concept=_RC + "identifying a nuanced position",
         explanation="The writer explicitly exempts pairings where one task is automatic: 'the spotlight is not really being asked to split'. Only combinations competing for the same beam are costly."),
    dict(passage=PASSAGE_2, stem="What does the writer mean by 'the friction of turning around'?",
         options=O(("A", "The physical strain of sitting badly at a desk"),
                   ("B", "The wasted effort of repeatedly switching attention between tasks"),
                   ("C", "The difficulty of restarting a computer"),
                   ("D", "The noise of a busy classroom")),
         correct="B", strand="Reading: Non-fiction", concept=_RC + "evaluating a loaded phrase",
         explanation="'Turning around' is the spotlight swinging between tasks; the 'friction' is the switching cost, the moment of blankness that makes busyness feel like work while producing nothing."),
    dict(passage=PASSAGE_2, stem="The passage ends by calling the undivided hour 'a kind of superpower … available, unusually for superpowers, to absolutely anyone'. What is the effect of this closing image?",
         options=O(("A", "It suggests only gifted students can concentrate deeply"),
                   ("B", "It warns that concentration is dangerous in large doses"),
                   ("C", "It argues that comic-book heroes are poor role models"),
                   ("D", "It makes sustained attention sound both rare and precious, yet within every reader's reach")),
         correct="D", strand="Reading: Non-fiction", concept=_RC + "understanding the closing image",
         explanation="Calling focus a superpower elevates it above ordinary habits in a distracted age, while the twist ('available … to absolutely anyone') turns the essay's argument into an invitation."),
]

# ---- Listening (3 recordings, 10 Q) ----------------------------------------
_LI = "Listen to the recording, then choose the best answer."
_A1, _A2, _A3 = "listening1.m4a", "listening2.m4a", "listening3.m4a"

AUDIO_TITLES = {
    "listening1.m4a": "Above the City",
    "listening2.m4a": "The Later Start Debate",
    "listening3.m4a": "Coral Gardening",
    "listening-zh.m4a": "短講一則 A Short Talk",
}

AUDIO = {
    "listening-zh.m4a": [("zh-CN-XiaoxiaoNeural", "-8%", "在香港岛，有一种交通工具已经行驶了一百多年，那就是电车。因为开动的时候，车上的铃铛会发出叮叮的声音，人们都亲切地叫它叮叮。电车不快，从西环到铜锣湾，可能要用差不多一个小时，但票价便宜，上层靠窗的位置最受欢迎：街市、旧楼、霓虹招牌，一一在窗外慢慢退后，就像看一部关于香港的电影。有人说，电车太慢，早就应该淘汰了。我倒觉得，在一个什么都讲求快的城市里，正需要这样一种慢。它提醒着匆忙的我们：路上的风景，本身就值得好好看一看。")],
    _A1: [("en-US-AvaNeural", "-6%",
        "I started hiking, honestly, by accident. Two years ago I signed up for a charity walk because my "
        "friends had, and I trained on the trail behind our estate, complaining the whole way up. The walk "
        "came and went. The complaining stopped; the walking did not. What keeps me going back is hard to "
        "explain to anyone who has not stood on a ridge at seven in the morning. The city I live in is loud, "
        "vertical and always in a hurry, but from six hundred metres up, the whole skyline lowers its voice. "
        "The towers I worry about all week shrink into a model village, and my problems seem to shrink with "
        "them. People assume the hills are far away, but that is the secret: from many front doors here, a "
        "trailhead is a short bus ride away, and forty minutes of climbing buys you a different city. I still "
        "check my phone at the top. But I have noticed I take longer, each time, to switch it back on.")],
    _A2: [
        ("en-GB-MaisieNeural", "-6%", "Our first lesson starts at eight, and honestly, half my class is asleep in it. "
                        "There is real research on this: in the teenage years the body clock shifts later, so "
                        "we fall asleep later and need mornings back. Schools that moved the first bell even "
                        "half an hour saw better attendance and better marks. I think we should start at nine."),
        ("en-GB-RyanNeural", "-6%", "I do not doubt the science, but a school is not only a timetable. Our buses "
                          "are shared with two other schools, most parents leave for work before eight, and "
                          "if we finish later instead, sports teams lose their training slots and the younger "
                          "students travel home in the dark half the year."),
        ("en-GB-MaisieNeural", "-6%", "I am not asking for eleven o'clock. Even forty-five minutes would help, and "
                        "the first period could be private study, so anyone who has to arrive early still has "
                        "somewhere quiet to work."),
        ("en-GB-RyanNeural", "-6%", "That is more workable. Here is what I can take to the principal: a trial, one "
                          "term long, with a nine o'clock start on Tuesdays and Thursdays, keeping the early "
                          "room open, and we track attendance, marks and the clubs' numbers."),
        ("en-GB-MaisieNeural", "-6%", "And if the data says it works, we extend it. Agreed. Let the numbers decide, "
                        "not the adults' habits and not my sleep either."),
    ],
    _A3: [("en-GB-RyanNeural", "-6%",
        "Beneath the surface of this city's eastern waters, something remarkable is being rebuilt, one "
        "fragment at a time. Corals here survived decades of dredging and murky harbours, but a warming sea "
        "is a different enemy: when the water stays too hot for too long, corals expel the tiny algae that "
        "feed them and turn bone white, a process called bleaching. A bleached coral is not dead, but it is "
        "starving. Marine scientists have responded with what they cheerfully call coral gardening. Broken "
        "fragments, which storms would once have ground into sand, are rescued and raised in underwater "
        "nurseries on racks, like seedlings in a greenhouse, then planted back onto the reef once they are "
        "strong. The early results are encouraging: on some restored patches, fish have returned in a single "
        "season. And the reef is worth the trouble, for a healthy reef is three things at once: a nursery "
        "for young fish, a larder for the creatures that eat there, and a breakwater that softens storm "
        "waves before they reach the shore. Gardening, though, is slower than destruction. The nurseries buy "
        "time; they do not buy forgiveness. Unless the warming itself slows, we will be replanting faster "
        "and faster simply to stand still.")],
}

LISTENING = [
    dict(stem=_LI + "\n\nWhat is the speaker's main point about hiking?", audio=_A1,
         options=O(("A", "It is the cheapest way to train for charity events"),
                   ("B", "It should be compulsory for all students"),
                   ("C", "It gives her distance from city pressures, and it is closer to home than people think"),
                   ("D", "It is only worthwhile in the early morning")),
         correct="C", strand="Listening", concept="Y9-10 Listening · main idea of a talk",
         explanation="She describes how the hills shrink her worries and reveals 'the secret' that a trailhead is a short bus ride from many front doors: escape is close at hand."),
    dict(stem=_LI + "\n\nWhy did the speaker originally start hiking?", audio=_A1,
         options=O(("A", "Her doctor recommended more exercise"), ("B", "She signed up for a charity walk because her friends had"),
                   ("C", "She wanted photographs for her classmates"), ("D", "Her school made it part of PE")),
         correct="B", strand="Listening", concept="Y9-10 Listening · stated reason",
         explanation="She says she started 'by accident': she signed up for a charity walk because her friends had, and trained on the trail behind her estate."),
    dict(stem=_LI + "\n\nWhat detail shows the speaker has not completely escaped her phone?", audio=_A1,
         options=O(("A", "She still checks it at the top, though she waits longer each time to switch it back on"),
                   ("B", "She uses it to navigate the trails"), ("C", "She calls her friends from the ridge"),
                   ("D", "She listens to music while climbing")),
         correct="A", strand="Listening", concept="Y9-10 Listening · supporting detail",
         explanation="She admits: 'I still check my phone at the top. But I have noticed I take longer, each time, to switch it back on.'"),
    dict(stem=_LI + "\n\nWhat does the speaker mean by saying 'the whole skyline lowers its voice'?", audio=_A1,
         options=O(("A", "Sound cannot travel to a height of six hundred metres"), ("B", "The city switches off its lights in the early morning"),
                   ("C", "Hikers are asked to speak quietly on the ridge"), ("D", "From above, the city feels calmer and its pressures lose their force")),
         correct="D", strand="Listening", concept="Y9-10 Listening · interpreting figurative language",
         explanation="A lowered voice suggests the loud, hurried city losing its power over her: the towers 'shrink into a model village, and my problems seem to shrink with them'."),
    dict(stem=_LI + "\n\nWhat is the student's main argument for a later school start?", audio=_A2,
         options=O(("A", "Teachers arrive too early to prepare lessons well"),
                   ("B", "Teenage body clocks shift later, and schools that delayed the first bell saw better attendance and marks"),
                   ("C", "The school buses are always late anyway"),
                   ("D", "Students need more time for breakfast")),
         correct="B", strand="Listening", concept="Y9-10 Listening · speaker's position in a discussion",
         explanation="She cites the research: teenage body clocks shift later, and schools that moved the first bell even half an hour saw better attendance and better marks."),
    dict(stem=_LI + "\n\nWhich of these is one of the teacher's objections?", audio=_A2,
         options=O(("A", "The research on teenage sleep has been disproved"),
                   ("B", "Students would only use the extra time for gaming"),
                   ("C", "Finishing later would cost sports teams their training slots"),
                   ("D", "The canteen cannot serve lunch any later")),
         correct="C", strand="Listening", concept="Y9-10 Listening · evaluating a counter-argument",
         explanation="He accepts the science but raises practical costs: shared buses, parents leaving before eight, teams losing training slots, and younger students travelling home in the dark."),
    dict(stem=_LI + "\n\nWhat arrangement do the two speakers agree to in the end?", audio=_A2,
         options=O(("A", "A one-term trial of nine o'clock starts on two days a week, judged by the data"),
                   ("B", "Moving the start to nine o'clock every day immediately"),
                   ("C", "Keeping the timetable exactly as it is"),
                   ("D", "Asking parents to drive students to school")),
         correct="A", strand="Listening", concept="Y9-10 Listening · synthesis (the point of agreement)",
         explanation="They settle on a one-term trial: nine o'clock starts on Tuesdays and Thursdays, an early room kept open, with attendance, marks and club numbers tracked. 'Let the numbers decide.'"),
    dict(stem=_LI + "\n\nAccording to the lecturer, what three things does a healthy reef provide?", audio=_A3,
         options=O(("A", "Sand for beaches, coral for jewellery, and diving sites for tourists"),
                   ("B", "A nursery for young fish, a feeding ground, and protection from storm waves"),
                   ("C", "Oxygen, fresh water, and building materials"),
                   ("D", "Warm water, shelter for ships, and fishing quotas")),
         correct="B", strand="Listening", concept="Y9-10 Listening · grouped details",
         explanation="The lecturer lists three roles: 'a nursery for young fish, a larder for the creatures that eat there, and a breakwater that softens storm waves'."),
    dict(stem=_LI + "\n\nWhat happens when a coral bleaches?", audio=_A3,
         options=O(("A", "It is dissolved by polluted water"), ("B", "It is ground into sand by storms"),
                   ("C", "It expels the algae that feed it and begins to starve, though it is not yet dead"),
                   ("D", "It immediately dies and turns to stone")),
         correct="C", strand="Listening", concept="Y9-10 Listening · understanding a defined process",
         explanation="In prolonged heat the coral expels the tiny algae that feed it and turns white: 'a bleached coral is not dead, but it is starving'. Saying it dies immediately is the trap."),
    dict(stem=_LI + "\n\nWhich best describes the lecturer's attitude towards coral gardening?", audio=_A3,
         options=O(("A", "Dismissive: it is a waste of research money"), ("B", "Neutral: simply reporting the facts"),
                   ("C", "Triumphant: the problem has been solved"), ("D", "Encouraged by the results, but clear that it cannot succeed unless warming slows")),
         correct="D", strand="Listening", concept="Y9-10 Listening · speaker's tone and attitude",
         explanation="He calls the early results encouraging, then warns that 'the nurseries buy time; they do not buy forgiveness': hope balanced against a hard condition."),
]

# ---- Writing / Speaking / Chinese ------------------------------------------
CONTENT_WRITING = dict(
    type="writing",
    intro="Choose ONE of the two tasks below and type your answer in the box. Aim for about 220-300 words.",
    body=("Task 1: Write about a place you have returned to again and again, at different ages. Describe the "
          "place, explain what draws you back, and reflect on how it, or your view of it, has changed as you "
          "have grown.\n\n"
          "Task 2: 'Competitive sport does more good than harm for teenagers.' To what extent do you agree? "
          "Develop a structured argument with clear reasons and examples, and acknowledge at least one point "
          "on the other side."),
    hint="Plan before you write: a clear introduction, developed paragraphs and a conclusion. Leave two minutes to review your accuracy and word choice.",
    placeholder="Type your answer here; it will be saved for review…",
)

CONTENT_SPEAKING = dict(
    type="speaking",
    stem="Record a short spoken response (about 2 minutes).",
    body=("Speak about:\n"
          "• Your name, your current school and year group\n"
          "• An activity, event or project you helped to organise, and what your role was\n"
          "• A person who has influenced the way you think or behave, and how\n"
          "• One goal you have set yourself for the next two years, inside or outside the classroom\n\n"
          "Speak naturally and develop your points; this is a chance for your future school to hear how you think."),
)

CH_PASSAGE_TRAD = (
    "每逢星期天，外婆家的廚房總是霧氣騰騰。天還沒亮，她就把排骨、粟米、紅蘿蔔放進瓦煲，用小火慢慢地煨。"
    "我問她，用電磁爐不是快得多嗎？她笑着搖頭：「湯是急不來的。火太猛，味道就出不來了。」\n\n"
    "那時我不懂，只知道湯很鮮甜。後來離家讀書，喝過各式各樣的湯：餐廳的例湯、便利店的即沖湯，卻總覺得"
    "欠了點甚麼。那點甚麼，說不出名字，卻在每個想家的夜晚隱隱作痛。直到一個下雨的黃昏，我在宿舍用小鍋笨拙地學煲湯，看着霧氣慢慢升起，忽然鼻子一酸："
    "原來欠的不是味道，而是那雙守在爐火旁的手。\n\n"
    "一煲湯，煨的是時間，盛的是心意。外婆從來不說「我愛你」這三個字，她只是幾十年如一日，把最好的"
    "材料、最多的耐心，都熬進湯裏，讓我們喝下去，暖到心裏。\n\n"
    "如今每次回家，我總搶着把湯捧上桌。外婆坐在老位置，笑瞇瞇地看着我們喝。湯還是那鍋湯，我卻終於讀懂了，"
    "霧氣背後，那雙一直含着笑意的眼睛。"
)
CH_PASSAGE_SIMP = (
    "每逢星期天，外婆家的厨房总是雾气腾腾。天还没亮，她就把排骨、粟米、红萝卜放进瓦煲，用小火慢慢地煨。"
    "我问她，用电磁炉不是快得多吗？她笑着摇头：“汤是急不来的。火太猛，味道就出不来了。”\n\n"
    "那时我不懂，只知道汤很鲜甜。后来离家读书，喝过各式各样的汤：餐厅的例汤、便利店的即冲汤，却总觉得"
    "欠了点什么。那点什么，说不出名字，却在每个想家的夜晚隐隐作痛。直到一个下雨的黄昏，我在宿舍用小锅笨拙地学煲汤，看着雾气慢慢升起，忽然鼻子一酸："
    "原来欠的不是味道，而是那双守在炉火旁的手。\n\n"
    "一煲汤，煨的是时间，盛的是心意。外婆从来不说“我爱你”这三个字，她只是几十年如一日，把最好的"
    "材料、最多的耐心，都熬进汤里，让我们喝下去，暖到心里。\n\n"
    "如今每次回家，我总抢着把汤捧上桌。外婆坐在老位置，笑眯眯地看着我们喝。汤还是那锅汤，我却终于读懂了，"
    "雾气背后，那双一直含着笑意的眼睛。"
)

def _ch(stem_t, stem_s, opts_ts, correct, concept, explanation):
    return dict(
        passage=zh_blocks(CH_PASSAGE_TRAD.replace("\n\n", "<br><br>"), CH_PASSAGE_SIMP.replace("\n\n", "<br><br>")),
        stem=bilingual(stem_t, stem_s),
        options=O(*[(k, bilingual(t, s)) for k, (t, s) in opts_ts.items()]),
        correct=correct, strand="中文閱讀理解", concept="高中中文 · " + concept, explanation=explanation)

CHINESE = [
    _ch("外婆說「湯是急不來的」，反映她怎樣的態度？", "外婆说“汤是急不来的”，反映她怎样的态度？",
        {"A": ("怕用新的電器", "怕用新的电器"), "B": ("捨不得花錢", "舍不得花钱"),
         "C": ("做事拖拉，不講效率", "做事拖拉，不讲效率"), "D": ("願意付出時間和耐心，把事情做好", "愿意付出时间和耐心，把事情做好")},
        "D", "內容理解：人物態度", "外婆堅持小火慢煨，是相信好味道需要時間醞釀，體現她的耐心和用心，並非怕電器或拖拉。"),
    _ch("「原來欠的不是味道，而是那雙守在爐火旁的手」，「那雙手」代表甚麼？", "“原来欠的不是味道，而是那双守在炉火旁的手”，“那双手”代表什么？",
        {"A": ("外婆的關愛與付出", "外婆的关爱与付出"), "B": ("煮食的技巧", "煮食的技巧"),
         "C": ("名貴的湯料", "名贵的汤料"), "D": ("宿舍簡陋的爐具", "宿舍简陋的炉具")},
        "A", "內容理解：意象指代", "「守在爐火旁的手」象徵外婆日復一日的守候與關愛；作者發現自己想念的是人，不是湯的味道。"),
    _ch("「煨的是時間，盛的是心意」一句，作者想表達甚麼？", "“煨的是时间，盛的是心意”一句，作者想表达什么？",
        {"A": ("煲湯要嚴格計算時間", "煲汤要严格计算时间"), "B": ("這鍋湯凝聚了外婆的耐心和愛", "这锅汤凝聚了外婆的耐心和爱"),
         "C": ("湯碗的款式很講究", "汤碗的款式很讲究"), "D": ("時間過得太快", "时间过得太快")},
        "B", "修辭理解：語句深層意思", "表面說湯，實際說情：慢火煨湯的每一分鐘，盛載的都是外婆的心意。"),
    _ch("外婆「從來不說『我愛你』這三個字」，下面哪項理解最恰當？", "外婆“从来不说‘我爱你’这三个字”，下面哪项理解最恰当？",
        {"A": ("外婆性格冷淡，不關心家人", "外婆性格冷淡，不关心家人"), "B": ("外婆不懂得表達自己", "外婆不懂得表达自己"),
         "C": ("外婆用行動代替言語去愛家人", "外婆用行动代替言语去爱家人"), "D": ("外婆覺得說這句話不吉利", "外婆觉得说这句话不吉利")},
        "C", "內容理解：辨析人物情感", "下文緊接「她只是幾十年如一日……熬進湯裏」，可見她的愛全在行動之中，而非冷淡或不懂表達。"),
    _ch("作者最初是在哪一刻醒悟到外婆的心意？", "作者最初是在哪一刻醒悟到外婆的心意？",
        {"A": ("小時候喝湯覺得鮮甜時", "小时候喝汤觉得鲜甜时"), "B": ("在餐廳喝到例湯時", "在餐厅喝到例汤时"),
         "C": ("下雨的黃昏，自己在宿舍笨拙地煲湯時", "下雨的黄昏，自己在宿舍笨拙地煲汤时"),
         "D": ("回家把湯捧上桌時", "回家把汤捧上桌时")},
        "C", "內容理解：關鍵情節", "作者自己動手煲湯、看着霧氣升起的一刻「忽然鼻子一酸」，才驚覺想念的是外婆的守候。"),
    _ch("本文主要想說明的道理是：", "本文主要想说明的道理是：",
        {"A": ("親人的愛往往藏在日常的細節裏，要用心才讀得懂", "亲人的爱往往藏在日常的细节里，要用心才读得懂"),
         "B": ("傳統瓦煲比電磁爐好用", "传统瓦煲比电磁炉好用"),
         "C": ("學生應該學會自己煮食", "学生应该学会自己煮食"),
         "D": ("香港的湯水文化歷史悠久", "香港的汤水文化历史悠久")},
        "A", "主旨理解", "全文以一鍋老火湯為線索，寫外婆無言的愛，以及作者由「不懂」到「讀懂」的成長，主旨在親情而非炊具或湯水文化。"),
]

CH_LISTENING = [
    dict(stem=bilingual("聆聽短講，然後回答問題。\n\n這段錄音主要介紹甚麼？", "聆听短讲，然后回答问题。\n\n这段录音主要介绍什么？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("建議政府增加電車班次", "建议政府增加电车班次")),
                   ("B", bilingual("介紹電車，並藉它帶出「慢」的價值", "介绍电车，并借它带出“慢”的价值")),
                   ("C", bilingual("比較各種交通工具的票價", "比较各种交通工具的票价")),
                   ("D", bilingual("回憶自己第一次坐電車的經歷", "回忆自己第一次坐电车的经历"))),
         correct="B", strand="中文聆聽理解", concept="高中中文 · 聆聽：主旨",
         explanation="說話人由電車的歷史、速度講到「城市正需要這樣一種慢」，主旨是借電車肯定慢的價值。"),
    dict(stem=bilingual("根據短講，人們叫電車做「叮叮」，是因為：", "根据短讲，人们叫电车做“叮叮”，是因为："), audio="listening-zh.m4a",
         options=O(("A", bilingual("車身上寫着這兩個字", "车身上写着这两个字")), ("B", bilingual("車站的廣播這樣稱呼它", "车站的广播这样称呼它")),
                   ("C", bilingual("開動時車上的鈴鐺發出叮叮聲", "开动时车上的铃铛发出叮叮声")), ("D", bilingual("它只在叮叮街行駛", "它只在叮叮街行驶"))),
         correct="C", strand="中文聆聽理解", concept="高中中文 · 聆聽：詞語理解（名稱由來）",
         explanation="說話人解釋：開動的時候，車上的鈴鐺會發出叮叮的聲音，人們便親切地叫它叮叮。"),
    dict(stem=bilingual("有人認為電車應該淘汰，理由是：", "有人认为电车应该淘汰，理由是："), audio="listening-zh.m4a",
         options=O(("A", bilingual("電車太慢", "电车太慢")), ("B", bilingual("票價太貴", "票价太贵")),
                   ("C", bilingual("路線太少", "路线太少")), ("D", bilingual("車廂太舊", "车厢太旧"))),
         correct="A", strand="中文聆聽理解", concept="高中中文 · 聆聽：細節（他人觀點）",
         explanation="短講提到：「有人說，電車太慢，早就應該淘汰了。」票價方面說話人反而說便宜。"),
    dict(stem=bilingual("說話人對電車的態度是：", "说话人对电车的态度是："), audio="listening-zh.m4a",
         options=O(("A", bilingual("認同它已經過時", "认同它已经过时")), ("B", bilingual("只當它是遊客玩意", "只当它是游客玩意")),
                   ("C", bilingual("無可無不可", "无可无不可")), ("D", bilingual("欣賞它，認為它的「慢」正是城市需要的", "欣赏它，认为它的“慢”正是城市需要的"))),
         correct="D", strand="中文聆聽理解", concept="高中中文 · 聆聽：說話人態度",
         explanation="說話人以「我倒覺得」反駁淘汰之說，指出快節奏的城市「正需要這樣一種慢」，是欣賞和肯定的態度。"),
]

CH_SPEAKING = dict(
    type="speaking", maxSeconds=150,
    stem=bilingual("請用普通話介紹自己（大約兩分鐘）。", "请用普通话介绍自己（大约两分钟）。"),
    body=zh_blocks("可以說一說：\n• 你的名字、年級和學校\n• 一位你敬佩的人，以及他或她怎樣影響了你\n• 一項你堅持了很久的課外興趣\n• 你期望的中學生活是怎樣的",
                   "可以说一说：\n• 你的名字、年级和学校\n• 一位你敬佩的人，以及他或她怎样影响了你\n• 一项你坚持了很久的课外兴趣\n• 你期望的中学生活是怎样的"),
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
