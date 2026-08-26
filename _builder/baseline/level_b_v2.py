# -*- coding: utf-8 -*-
"""HKS Baseline Assessment · Years 5-6 (current Y5-Y6 / G4-G5), version 2. 45 min core.

Every MCQ's `concept` is curriculum-coded (UK-NC year + topic) so a wrong
answer maps straight to the syllabus area in the report's focus list.
Parallel form of level_b_v1: identical structure, all-new content.
"""
from figlib import *

BAND = "level-b"
BAND_LABEL = "Level B"
YEAR_SPAN = "Years 5-6"
YEARS = ["Year 5", "Year 6"]

SECTIONS = [
    {"name": "Verbal Reasoning", "minutes": 8},         # 16 Q at 30 s
    {"name": "Non-Verbal Reasoning", "minutes": 6},     # 12 Q at 30 s
    {"name": "Mathematics", "minutes": 10},             # 4 short + 6 story
    {"name": "Reading Comprehension", "minutes": 7},
    {"name": "Listening", "minutes": 6},                # 3 recordings, 10 Q
    {"name": "Writing", "minutes": 6},
    {"name": "Speaking", "minutes": 2},
    {"name": "中文閱讀 Chinese Reading", "minutes": 8, "opt": "chinese"},
    {"name": "中文聆聽 Chinese Listening", "minutes": 4, "opt": "chinese"},
    {"name": "中文口語 Chinese Speaking", "minutes": 3, "opt": "chspeak"},
]

INFO = {
    "Verbal Reasoning": "This section tests how well you understand words and language: similar and opposite meanings, word pairs, sentences with a missing word, and grammar. Work quickly; you have about half a minute per question.",
    "Non-Verbal Reasoning": "This section uses figures instead of words. In some questions, three pictures share a rule: choose the answer picture that follows the same rule. In others, a grid changes across the row: choose the picture that completes it. Work quickly; about half a minute per question.",
    "Mathematics": "Read each question carefully and choose the best answer. Some questions are short calculations; others are longer story problems with more than one step. You may use rough paper, but no calculator.",
    "Reading Comprehension": "Read each passage carefully, then answer the questions about it. The passage is shown with every question, so you can always re-read it.",
    "Listening": "There are three short recordings: a conversation, an announcement and a phone message. You may play each one up to two times. Answer the questions about each recording before moving on.",
    "Writing": "You will see two writing tasks. Choose ONE and type your answer in the box. Aim for about 80-130 words: plan briefly, write in clear paragraphs, and check your spelling and punctuation.",
    "Speaking": "In this final section you will record a short audio introduction of yourself. Find a quiet spot, allow microphone access when your browser asks, and speak clearly and naturally.",
    "中文聆聽 Chinese Listening": zh_blocks("現在是普通話聆聽部分。請按播放鍵，細心聆聽廣播，每段錄音最多可以播放兩次。", "现在是普通话聆听部分。请按播放键，细心聆听广播，每段录音最多可以播放两次。"),
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
_GR = "Choose the word or phrase that best completes the sentence."

# ---- Verbal Reasoning (16) --------------------------------------------------
VERBAL = [
    dict(stem=_SYN + "\n\nRELUCTANT", options=O(("A", "eager"), ("B", "unwilling"), ("C", "careless"), ("D", "slow")),
         correct="B", strand="Vocabulary: Synonyms", concept="Y5-6 Vocabulary · synonyms: reluctant = unwilling",
         explanation="Reluctant means unwilling to do something. Eager is the opposite."),
    dict(stem=_SYN + "\n\nDILIGENT", options=O(("A", "lazy"), ("B", "clever"), ("C", "obedient"), ("D", "hardworking")),
         correct="D", strand="Vocabulary: Synonyms", concept="Y5-6 Vocabulary · synonyms: diligent = hardworking",
         explanation="A diligent person works carefully and steadily, in other words hardworking. Lazy is the opposite."),
    dict(stem=_SYN + "\n\nVACANT", options=O(("A", "empty"), ("B", "noisy"), ("C", "occupied"), ("D", "tidy")),
         correct="A", strand="Vocabulary: Synonyms", concept="Y5-6 Vocabulary · synonyms: vacant = empty",
         explanation="Vacant means empty or not being used. Occupied is the opposite."),
    dict(stem=_ANT + "\n\nSHALLOW", options=O(("A", "narrow"), ("B", "muddy"), ("C", "deep"), ("D", "wide")),
         correct="C", strand="Vocabulary: Antonyms", concept="Y5-6 Vocabulary · antonyms: shallow vs deep",
         explanation="Shallow water does not go down far; deep water does. Narrow and wide describe distance across, not depth."),
    dict(stem=_ANT + "\n\nTEMPORARY", options=O(("A", "permanent"), ("B", "brief"), ("C", "sudden"), ("D", "fragile")),
         correct="A", strand="Vocabulary: Antonyms", concept="Y5-6 Vocabulary · antonyms: temporary vs permanent",
         explanation="Temporary means lasting a short time; permanent means lasting for ever. Brief is a near-synonym of temporary."),
    dict(stem=_ANT + "\n\nHUMBLE", options=O(("A", "modest"), ("B", "poor"), ("C", "quiet"), ("D", "boastful")),
         correct="D", strand="Vocabulary: Antonyms", concept="Y5-6 Vocabulary · antonyms: humble vs boastful",
         explanation="A humble person does not show off; a boastful person does. Modest is a synonym of humble."),
    dict(stem=_ANA + "\n\nPetal is to flower as page is to ______.",
         options=O(("A", "letter"), ("B", "ink"), ("C", "book"), ("D", "library")),
         correct="C", strand="Verbal Analogies", concept="Y5-6 Verbal Reasoning · analogies: part to whole",
         explanation="A petal is one part of a flower; a page is one part of a book. A library contains books but a page is not a part of it."),
    dict(stem=_ANA + "\n\nCarpenter is to saw as surgeon is to ______.",
         options=O(("A", "hospital"), ("B", "scalpel"), ("C", "patient"), ("D", "medicine")),
         correct="B", strand="Verbal Analogies", concept="Y5-6 Verbal Reasoning · analogies: worker to tool",
         explanation="A carpenter cuts with a saw; a surgeon cuts with a scalpel. A hospital is where a surgeon works, not a tool."),
    dict(stem=_ANA + "\n\nLitre is to capacity as kilogram is to ______.",
         options=O(("A", "distance"), ("B", "scales"), ("C", "water"), ("D", "mass")),
         correct="D", strand="Verbal Analogies", concept="Y5-6 Verbal Reasoning · analogies: unit to what it measures",
         explanation="A litre is a unit for measuring capacity; a kilogram is a unit for measuring mass. Scales are the instrument, not the thing measured."),
    dict(stem=_ANA + "\n\nWarm is to scorching as cool is to ______.",
         options=O(("A", "freezing"), ("B", "mild"), ("C", "damp"), ("D", "sunny")),
         correct="A", strand="Verbal Analogies", concept="Y5-6 Verbal Reasoning · analogies: weaker to stronger degree",
         explanation="Scorching is an extreme form of warm, so the answer must be an extreme form of cool: freezing."),
    dict(stem=_SC + "\n\nThe instructions were so ______ that even the teacher had to read them three times before she understood.",
         options=O(("A", "brief"), ("B", "confusing"), ("C", "helpful"), ("D", "familiar")),
         correct="B", strand="Sentence Completion", concept="Y5-6 Reading · sentence completion: context clues (ISEE style)",
         explanation="Needing three readings to understand shows the instructions were confusing, not helpful or familiar."),
    dict(stem=_SC + "\n\nAfter weeks without rain, the reservoir had ______ to less than half its usual level.",
         options=O(("A", "risen"), ("B", "frozen"), ("C", "shrunk"), ("D", "overflowed")),
         correct="C", strand="Sentence Completion", concept="Y5-6 Reading · sentence completion: context clues (ISEE style)",
         explanation="No rain means less water, so the reservoir had shrunk. Risen and overflowed would mean more water."),
    dict(stem=_SC + "\n\nThe audience grew ______ as the magician's final trick appeared to go wrong.",
         options=O(("A", "anxious"), ("B", "drowsy"), ("C", "generous"), ("D", "invisible")),
         correct="A", strand="Sentence Completion", concept="Y5-6 Reading · sentence completion: context clues (ISEE style)",
         explanation="Seeing a trick go wrong would make the audience worried, in other words anxious."),
    dict(stem=_GR + "\n\nWhile we ______ dinner, the lights suddenly went out.",
         options=O(("A", "eat"), ("B", "are eating"), ("C", "were eating"), ("D", "eaten")),
         correct="C", strand="Grammar & Cloze", concept="Y5 Grammar · past continuous for an interrupted action",
         explanation="'While' with a past interruption needs the past continuous: we were eating when the lights went out."),
    dict(stem=_GR + "\n\nThis puzzle is far ______ than the one we solved yesterday.",
         options=O(("A", "difficult"), ("B", "more difficult"), ("C", "most difficult"), ("D", "difficulter")),
         correct="B", strand="Grammar & Cloze", concept="Y5 Grammar · comparative adjectives with 'more'",
         explanation="Comparing two puzzles needs the comparative 'more difficult'. 'Difficulter' is not a real word, and 'most difficult' compares three or more."),
    dict(stem=_GR + "\n\nSara has played the violin ______ she was six years old.",
         options=O(("A", "for"), ("B", "while"), ("C", "from"), ("D", "since")),
         correct="D", strand="Grammar & Cloze", concept="Y6 Grammar · present perfect with 'since' + starting point",
         explanation="'Since' marks the starting point of an action that continues (since she was six). 'For' would need a length of time, such as 'for five years'."),
]

# ---- Non-Verbal Reasoning (12 = 9 CAT4-engine + 3 GL-style) -----------------
_SEQ = "Look at the four pictures in the top row. Work out the pattern, then choose the picture (A-E) that belongs in the empty box."
_CODE = "Each picture on the left has a two-letter code. Work out what each letter stands for, then choose the code for the picture marked '?'."

NONVERBAL = nvr_from_json("level-b", 2) + [
    dict(stem=_SEQ, correct="E", strand="Figure Series (GL style)",
         concept="Y5-6 Non-Verbal Reasoning (GL 11+ series style) · two rules: the square grows AND its filled half turns a quarter each step",
         explanation="Two rules run together: the square gets bigger each step AND the filled half turns a quarter clockwise (left, top, right, bottom). Next comes the biggest square with the LEFT half filled again. A is the right size but filled on the wrong side, B stopped growing, and D is filled completely.",
         fig=seq_fig([cell(halfsquare, 12, 0), cell(halfsquare, 15, 90), cell(halfsquare, 18, 180), cell(halfsquare, 21, 270)],
                     [cell(halfsquare, 24, 180), cell(halfsquare, 21, 0), cell(halfsquare, 24, 90), cell(square, 24), cell(halfsquare, 24, 0)])),
    dict(stem=_SEQ, correct="A", strand="Figure Series (GL style)",
         concept="Y5-6 Non-Verbal Reasoning (GL 11+ series style) · two rules: one more dot each step AND the dots swap black and white",
         explanation="Two rules run together: the number of dots inside the circle goes up by one each step AND the dots alternate black, white. After four white dots come FIVE BLACK dots. B has five dots but white, C has stopped counting, and D jumps to six.",
         fig=seq_fig([multi(cell(circle, 26, "none"), cell(dots, 1)),
                      multi(cell(circle, 26, "none"), cell(dots, 2, 5, "none")),
                      multi(cell(circle, 26, "none"), cell(dots, 3)),
                      multi(cell(circle, 26, "none"), cell(dots, 4, 5, "none"))],
                     [multi(cell(circle, 26, "none"), cell(dots, 5)),
                      multi(cell(circle, 26, "none"), cell(dots, 5, 5, "none")),
                      multi(cell(circle, 26, "none"), cell(dots, 4)),
                      multi(cell(circle, 26, "none"), cell(dots, 6)),
                      multi(cell(circle, 26, "none"), cell(dots, 3, 5, "none"))])),
    dict(stem=_CODE, correct="C", strand="Figure Codes (GL style)",
         concept="Y5-6 Non-Verbal Reasoning (GL/CEM codes style) · first letter = shape, second letter = shading",
         explanation="F means triangle and G means pentagon; X means black and Y means white. The mystery picture is a WHITE PENTAGON, so its code is GY.",
         fig=codes_fig([(cell(triangle, 18, INK), "FX"), (cell(triangle, 18, "none"), "FY"), (cell(pentagon, 18, INK), "GX")],
                       cell(pentagon, 18, "none")),
         options=O(("A", "FY"), ("B", "GX"), ("C", "GY"), ("D", "FX"), ("E", "HX"))),
]

# ---- Mathematics (10: 4 short + 6 story, 4 with diagrams) -------------------
MATHS = [
    # short form
    dict(stem="Round 47,562 to the nearest 1,000.",
         options=O(("A", "47,000"), ("B", "48,000"), ("C", "47,600"), ("D", "50,000")),
         correct="B", strand="Number & Place Value", concept="Y5 Number · rounding a 5-digit number to the nearest 1,000",
         explanation="The hundreds digit is 5, so round up: 48,000. Choosing 47,000 means the digits were simply cut off; 47,600 rounds to the nearest hundred and 50,000 to the nearest ten thousand."),
    dict(stem="The diagram shows angles meeting on a straight line. What is the size of angle x?",
         fig=angles_on_line([64, 37]),
         options=O(("A", "69°"), ("B", "116°"), ("C", "79°"), ("D", "101°")),
         correct="C", strand="Measurement & Geometry", concept="Y5 Geometry · angles on a straight line sum to 180",
         explanation="64 + 37 = 101, and 180 − 101 = 79°. Choosing 101° means the two known angles were added but never subtracted from 180; 116° ignores the 37° angle."),
    dict(stem="What is 7/10 + 1/5?",
         options=O(("A", "8/15"), ("B", "8/10"), ("C", "9/15"), ("D", "9/10")),
         correct="D", strand="Fractions & Decimals", concept="Y5 Fractions · adding fractions with related denominators",
         explanation="1/5 = 2/10, so 7/10 + 2/10 = 9/10. Choosing 8/10 means 1/5 was treated as 1/10; 8/15 adds the tops and the bottoms."),
    dict(stem="The diagram shows a grid of equal squares. What fraction of the grid is shaded, in its simplest form?",
         fig=fraction_grid(3, 4, 9),
         options=O(("A", "3/4"), ("B", "2/3"), ("C", "1/4"), ("D", "9/16")),
         correct="A", strand="Fractions & Decimals", concept="Y6 Fractions · fraction of a diagram, simplifying 9/12",
         explanation="9 of the 12 squares are shaded: 9/12 = 3/4. Choosing 1/4 gives the UNSHADED fraction, and 9/16 miscounts the grid as 16 squares."),
    # story form
    dict(stem="The bar chart shows the cups of lemonade a stall sold from Monday to Thursday. The stall's target for the four days was 250 cups. By how many cups did the stall MISS its target?",
         fig=bar_chart(["Mon", "Tue", "Wed", "Thu"], [60, 45, 30, 75], 90, 15, unit="cups"),
         options=O(("A", "210"), ("B", "45"), ("C", "40"), ("D", "50")),
         correct="C", strand="Problem Solving", concept="Y6 Statistics · reading a bar chart, totalling, then finding the shortfall",
         explanation="Read the bars: 60 + 45 + 30 + 75 = 210 cups sold, and 250 − 210 = 40 short. Choosing 210 gives the total sold, not the shortfall, and 45 is just Tuesday's bar."),
    dict(stem="The diagram shows a rectangular vegetable patch. What is the AREA of the patch?",
         fig=labelled_shape_fig(lambda out: out.extend([
             '<rect x="60" y="30" width="198" height="88" fill="#eef2f8" stroke="#1c2733" stroke-width="2.5"/>',
             svg_text(159, 20, "9 m"),
             svg_text(48, 78, "4 m", anchor="end")]), 300, 150),
         options=O(("A", "13 m²"), ("B", "26 m²"), ("C", "32 m²"), ("D", "36 m²")),
         correct="D", strand="Measurement & Geometry", concept="Y5 Measurement · area of a rectangle (length × width)",
         explanation="Area = 9 × 4 = 36 m². Choosing 26 m² gives the PERIMETER, and 13 m² just adds one length and one width."),
    dict(stem="A train leaves the station at 9:35 am. The journey normally takes 1 hour 45 minutes, but today the train is delayed by 25 minutes on the way. At what time does it arrive?",
         options=O(("A", "11:20 am"), ("B", "11:45 am"), ("C", "12:05 pm"), ("D", "11:10 am")),
         correct="B", strand="Measurement & Geometry", concept="Y5 Measurement · elapsed time with an extra step",
         explanation="9:35 am + 1 h 45 min = 11:20 am, then + 25 min delay = 11:45 am. 11:20 forgets the delay, and 12:05 adds a 45-minute delay instead of 25."),
    dict(stem="Juice boxes cost HK$7 each, or a pack of 5 boxes costs HK$30. Maya needs 10 boxes, so she buys 2 packs and pays with a HK$100 note. How much change does she receive?",
         options=O(("A", "HK$40"), ("B", "HK$30"), ("C", "HK$70"), ("D", "HK$60")),
         correct="A", strand="Problem Solving", concept="Y5 Money · best-buy pack price then change (two steps)",
         explanation="Two packs cost 2 × HK$30 = HK$60, so the change is HK$100 − HK$60 = HK$40. HK$30 prices the boxes singly (10 × HK$7 = HK$70), ignoring the pack offer; HK$70 subtracts only ONE pack; HK$60 is the cost, not the change."),
    dict(stem="A recipe for 4 people uses 300 g of flour. Priya cooks the same recipe for 10 people. How much flour does she need?",
         options=O(("A", "600 g"), ("B", "120 g"), ("C", "750 g"), ("D", "900 g")),
         correct="C", strand="Problem Solving", concept="Y6 Ratio · scaling a recipe (unitary method)",
         explanation="300 ÷ 4 = 75 g per person, and 75 × 10 = 750 g. Choosing 600 g doubles the recipe (for 8 people) and 900 g triples it (for 12)."),
    dict(stem="A stationery shop orders 15 boxes of pencils, with 24 pencils in each box. In the first week, 96 pencils are sold. How many pencils are left?",
         options=O(("A", "360"), ("B", "264"), ("C", "240"), ("D", "274")),
         correct="B", strand="Problem Solving", concept="Y5 Number · multi-step word problem (multiply, then subtract)",
         explanation="15 × 24 = 360 pencils, then 360 − 96 = 264 left. Choosing 360 forgets the subtraction, and 274 comes from taking away 86 instead of 96."),
]

# ---- Reading Comprehension (10) --------------------------------------------
PASSAGE_1 = (
    "<strong>The Try-Out</strong><br><br>"
    "All through the summer holidays, Jun practised football in the park below his flat: keepy-uppies before "
    "breakfast, passing drills against the wall after dinner. When try-outs for the school team were announced, "
    "he was sure his chance had finally come.<br><br>"
    "On Friday afternoon, the coach pinned the team list to the noticeboard. Jun ran his finger down the names, "
    "once, then again more slowly. His name was not there. His heart sank like a stone, and he stood in front of "
    "the board until the corridor emptied, so that nobody would see his face.<br><br>"
    "The next week, Coach Ho stopped him at the gate. “I watched you at the try-outs,” he said. “You kept "
    "encouraging the younger boys, and you explained that passing drill better than I do. The junior squad "
    "trains on Tuesdays. I need an assistant.”<br><br>"
    "Jun almost said no. But on Tuesday he found himself on the pitch, showing a small boy named Hin how to "
    "trap the ball with the inside of his foot. When Hin finally did it, he cheered as though he had scored in "
    "a cup final, and Jun felt something warm spread through his chest.<br><br>"
    "By December, Jun still hoped to make the team one day. Yet when Grandma asked him about football now, he "
    "did not talk about the list. He talked about Hin, and the junior squad, and how there is more than one way "
    "to belong to a team."
)

PASSAGE_2 = (
    "<strong>The Dance of the Honeybee</strong><br><br>"
    "A honeybee cannot speak, write or draw a map. Yet when a worker bee discovers a patch of flowers rich in "
    "nectar, she can tell her hivemates almost exactly where to find it. Her secret is a remarkable behaviour "
    "that scientists call the waggle dance.<br><br>"
    "Back on the honeycomb, the bee runs forward in a straight line, waggling her body rapidly from side to "
    "side, then circles back and repeats the run. Hidden in this little dance are precise directions. The angle "
    "of the run tells the other bees which direction to fly in relation to the sun. The length of the waggling "
    "run tells them how far away the flowers are: the longer the waggle, the longer the journey.<br><br>"
    "Other workers crowd around the dancer, touching her with their antennae and even sampling the nectar she "
    "has brought home, which tells them what the flowers smell like. Within minutes, the dancer recruits dozens "
    "of foragers, and they stream out of the hive towards a food source most of them have never seen.<br><br>"
    "The waggle dance was decoded in the 1940s by an Austrian scientist named Karl von Frisch, who later won a "
    "Nobel Prize for the discovery. Many researchers consider it one of the most sophisticated forms of "
    "communication in the animal kingdom: a wordless language, performed in the darkness of the hive, yet "
    "accurate enough to guide a bee across several kilometres of countryside."
)

_RC = "Y5-6 Reading · "
READING = [
    dict(passage=PASSAGE_1, stem="How did Jun feel after reading the team list?",
         options=O(("A", "Proud of his summer of practice"), ("B", "Disappointed and embarrassed"),
                   ("C", "Angry with Coach Ho"), ("D", "Relieved that the wait was over")),
         correct="B", strand="Reading: Fiction", concept=_RC + "character feelings at the start",
         explanation="His heart sank and he waited until the corridor was empty so nobody would see his face: he was disappointed and embarrassed, not angry at anyone."),
    dict(passage=PASSAGE_1, stem="What does the writer mean by “his heart sank like a stone”?",
         options=O(("A", "Jun suddenly felt unwell"), ("B", "Jun was frightened of the coach"),
                   ("C", "Jun's chest hurt from all the running"), ("D", "Jun was suddenly filled with heavy disappointment")),
         correct="D", strand="Reading: Fiction", concept=_RC + "interpreting figurative wording",
         explanation="A heart 'sinking like a stone' is a picture of sudden, heavy disappointment; nothing physically happened to Jun."),
    dict(passage=PASSAGE_1, stem="What can we infer about why Coach Ho asked Jun to help with the junior squad?",
         options=O(("A", "He had noticed Jun's patience and clear explanations at the try-outs"),
                   ("B", "He felt sorry for Jun and wanted to cheer him up"),
                   ("C", "No other student was willing to do the job"),
                   ("D", "Jun's grandmother had asked him to find Jun a role")),
         correct="A", strand="Reading: Fiction", concept=_RC + "inference about character",
         explanation="The coach says he watched Jun encourage the younger boys and explain the drill well: he chose Jun for those qualities, not out of pity."),
    dict(passage=PASSAGE_1, stem="According to the passage, what did Jun show Hin how to do?",
         options=O(("A", "Do keepy-uppies before breakfast"), ("B", "Score in a cup final"),
                   ("C", "Trap the ball with the inside of his foot"), ("D", "Read the team list on the noticeboard")),
         correct="C", strand="Reading: Fiction", concept=_RC + "locating a stated detail",
         explanation="Jun showed Hin 'how to trap the ball with the inside of his foot'. The keepy-uppies were Jun's own summer practice."),
    dict(passage=PASSAGE_1, stem="Which sentence best expresses the main message of the story?",
         options=O(("A", "Practising every day guarantees success"), ("B", "Coaches always know best"),
                   ("C", "Losing is easier when nobody sees your face"), ("D", "There is more than one way to belong to a team")),
         correct="D", strand="Reading: Fiction", concept=_RC + "main message and character change",
         explanation="The final paragraph states it directly: Jun learns there is more than one way to belong to a team."),
    dict(passage=PASSAGE_2, stem="What is the writer's main aim in this passage?",
         options=O(("A", "To explain how honeybees share the location of food"),
                   ("B", "To describe how to keep bees safely"),
                   ("C", "To tell the life story of Karl von Frisch"),
                   ("D", "To warn readers that bees are disappearing")),
         correct="A", strand="Reading: Non-fiction", concept=_RC + "identifying the main purpose",
         explanation="Every paragraph explains how the waggle dance passes on the location of food; von Frisch is mentioned only as the scientist who decoded it."),
    dict(passage=PASSAGE_2, stem="Who worked out what the waggle dance means?",
         options=O(("A", "A team of beekeepers"), ("B", "A French photographer"),
                   ("C", "Karl von Frisch"), ("D", "The worker bees themselves")),
         correct="C", strand="Reading: Non-fiction", concept=_RC + "locating a stated detail",
         explanation="The dance was decoded in the 1940s by the Austrian scientist Karl von Frisch."),
    dict(passage=PASSAGE_2, stem="In paragraph 3, the word “recruits” is closest in meaning to:",
         options=O(("A", "counts carefully"), ("B", "persuades to join"),
                   ("C", "pushes away"), ("D", "feeds slowly")),
         correct="B", strand="Reading: Non-fiction", concept=_RC + "vocabulary in context",
         explanation="The dancer 'recruits dozens of foragers' who then fly out with her: she persuades them to join the trip."),
    dict(passage=PASSAGE_2, stem="What does the LENGTH of the waggling run tell the other bees?",
         options=O(("A", "What the flowers smell like"), ("B", "Which direction to fly"),
                   ("C", "How much nectar is left"), ("D", "How far away the flowers are")),
         correct="D", strand="Reading: Non-fiction", concept=_RC + "understanding an explained fact",
         explanation="The longer the waggle, the longer the journey: the length gives the distance. Direction comes from the ANGLE of the run."),
    dict(passage=PASSAGE_2, stem="According to the passage, which of the following statements is FALSE?",
         options=O(("A", "The waggle dance is performed in bright sunlight"),
                   ("B", "Other bees sample the nectar the dancer brings home"),
                   ("C", "The angle of the run relates to the position of the sun"),
                   ("D", "Karl von Frisch won a Nobel Prize")),
         correct="A", strand="Reading: Non-fiction", concept=_RC + "checking statements against the text",
         explanation="The passage says the dance is performed in the DARKNESS of the hive, so 'in bright sunlight' is false. The other three statements are all stated in the text."),
]

# ---- Listening (3 recordings, 10 Q) ----------------------------------------
_LI = "Listen to the recording, then choose the best answer."
_A1, _A2, _A3 = "listening1.m4a", "listening2.m4a", "listening3.m4a"

AUDIO_TITLES = {
    "listening1.m4a": "The Museum Trip",
    "listening2.m4a": "The Talent Show",
    "listening3.m4a": "A Message about the Lesson",
    "listening-zh.m4a": "圖書義賣 The Book Sale",
}

AUDIO = {
    "listening-zh.m4a": [("zh-CN-XiaoxiaoNeural", "-10%", "各位同学请注意。原定星期五在课室举行的图书义卖，现在改在礼堂举行。义卖中午十二点半开始，两点结束，每本图书卖五元，请大家自备零钱。另外，欢迎同学把看过的旧图书在星期四之前交到图书馆。谢谢大家。")],
    _A1: [
        ("en-GB-RyanNeural", "-8%", "Hi Chloe. Did Mr Tan tell you about the museum trip?"),
        ("en-GB-MaisieNeural", "-8%", "No. Has something changed?"),
        ("en-GB-RyanNeural", "-8%", "It was going to be this Tuesday, but the Science Museum's main hall is closed for repairs, "
                        "so the trip has moved to Friday."),
        ("en-GB-MaisieNeural", "-8%", "Oh! Do we still meet in the classroom first?"),
        ("en-GB-RyanNeural", "-8%", "No. On Friday we meet at the school gate at a quarter past eight, "
                        "so the bus can leave straight away."),
        ("en-GB-MaisieNeural", "-8%", "Should I bring money for the museum cafe?"),
        ("en-GB-RyanNeural", "-8%", "There's no point. The cafe is closed too, so everyone has to bring a packed lunch "
                        "and a water bottle."),
        ("en-GB-MaisieNeural", "-8%", "Good thing you told me. My mum was going to give me lunch money."),
    ],
    _A2: [("en-GB-SoniaNeural", "-8%",
        "Attention, everyone. This is an announcement about this year's talent show. "
        "Auditions will be held next Wednesday at lunchtime in the music room. "
        "If you would like to take part, write your name and your act on the sign-up sheet "
        "outside the school office by Monday lunchtime. "
        "Each act may last three minutes at the most, so practise keeping to time. "
        "The best acts will perform on the hall stage at the Spring Fair, "
        "and every performer will receive a certificate.")],
    _A3: [("en-US-BrianNeural", "-8%",
        "Hello, this is Mr Chow with a message about Emma's piano lesson. "
        "I'm sorry, but I am playing in a concert on Thursday, so this week's lesson will move "
        "from Thursday afternoon to Saturday morning at half past ten. "
        "Please remember to bring the green practice book we started last week, not the old blue one; "
        "we will begin with the new scales on page six. "
        "One more thing: Room Two is being painted, so we will meet in Room Four, "
        "just along the corridor. Thank you, and see you on Saturday.")],
}

LISTENING = [
    dict(stem=_LI + "\n\nWhy has the museum trip been moved?", audio=_A1,
         options=O(("A", "The school bus broke down"), ("B", "The class teacher is unwell"),
                   ("C", "The museum's main hall is closed for repairs"), ("D", "Not enough parents can help")),
         correct="C", strand="Listening", concept="Y5 Listening · stated reason",
         explanation="The trip moved because the Science Museum's main hall is closed for repairs."),
    dict(stem=_LI + "\n\nWhen will the trip take place now?", audio=_A1,
         options=O(("A", "Friday"), ("B", "Tuesday"), ("C", "Monday"), ("D", "Saturday")),
         correct="A", strand="Listening", concept="Y5 Listening · key detail (new date); Tuesday is the OLD date trap",
         explanation="It was going to be Tuesday but has been moved to Friday."),
    dict(stem=_LI + "\n\nWhere should pupils meet on the morning of the trip?", audio=_A1,
         options=O(("A", "In the classroom"), ("B", "At the museum entrance"),
                   ("C", "In the school hall"), ("D", "At the school gate")),
         correct="D", strand="Listening", concept="Y5 Listening · changed arrangement; the classroom is the USUAL place trap",
         explanation="They no longer meet in the classroom: on Friday they meet at the school gate at a quarter past eight."),
    dict(stem=_LI + "\n\nWhy should pupils bring a packed lunch?", audio=_A1,
         options=O(("A", "The trip lasts until the evening"), ("B", "The museum cafe is closed"),
                   ("C", "The bus leaves before lunchtime"), ("D", "Mr Tan wants them to save money")),
         correct="B", strand="Listening", concept="Y6 Listening · inference (cafe closed, so lunch money is useless)",
         explanation="The museum cafe is closed as well, so lunch money would be no use: everyone brings a packed lunch."),
    dict(stem=_LI + "\n\nWhere will the talent show auditions be held?", audio=_A2,
         options=O(("A", "In the school hall"), ("B", "In the music room"), ("C", "On the Spring Fair stage"), ("D", "In the library")),
         correct="B", strand="Listening", concept="Y5 Listening · key detail (place); the hall is where WINNERS perform trap",
         explanation="Auditions are in the music room; the hall stage is where the best acts perform later, at the Spring Fair."),
    dict(stem=_LI + "\n\nBy when must students sign up?", audio=_A2,
         options=O(("A", "Next Wednesday"), ("B", "Friday afternoon"), ("C", "The day of the Spring Fair"), ("D", "Monday lunchtime")),
         correct="D", strand="Listening", concept="Y5 Listening · deadline; Wednesday is the AUDITION day trap",
         explanation="Names go on the sign-up sheet by Monday lunchtime; Wednesday is when the auditions happen."),
    dict(stem=_LI + "\n\nHow long may each act last, at most?", audio=_A2,
         options=O(("A", "Three minutes"), ("B", "Five minutes"), ("C", "Ten minutes"), ("D", "One minute")),
         correct="A", strand="Listening", concept="Y5 Listening · key detail (time limit)",
         explanation="Each act may last three minutes at the most."),
    dict(stem=_LI + "\n\nWhen will Emma's piano lesson be this week?", audio=_A3,
         options=O(("A", "Thursday at half past ten"), ("B", "Saturday at ten o'clock"),
                   ("C", "Saturday at half past ten"), ("D", "Thursday afternoon")),
         correct="C", strand="Listening", concept="Y5 Listening · changed day AND time; Thursday is the USUAL day trap",
         explanation="The lesson moves from Thursday afternoon to Saturday morning at half past ten."),
    dict(stem=_LI + "\n\nWhat must Emma remember to bring?", audio=_A3,
         options=O(("A", "The old blue practice book"), ("B", "Her metronome"),
                   ("C", "Spare sheet music"), ("D", "The green practice book")),
         correct="D", strand="Listening", concept="Y5 Listening · detail with a near trap (the blue book is the OLD one)",
         explanation="She must bring the green practice book they started last week, not the old blue one."),
    dict(stem=_LI + "\n\nWhere will the lesson take place?", audio=_A3,
         options=O(("A", "Room Four"), ("B", "Room Two"), ("C", "The concert hall"), ("D", "Mr Chow's home")),
         correct="A", strand="Listening", concept="Y5 Listening · changed arrangement (Room Two is being painted)",
         explanation="Room Two is being painted, so the lesson moves to Room Four along the corridor."),
]

# ---- Writing / Speaking / Chinese ------------------------------------------
CONTENT_WRITING = dict(
    type="writing",
    intro="Choose ONE of the two tasks below and type your answer in the box. Aim for about 80-130 words.",
    body=("Task 1: Describe a place in Hong Kong that is special to you. Use details of what you can see, hear "
          "and smell there, and explain why the place matters to you.\n\n"
          "Task 2: Some people think children should be allowed to bring mobile phones to school. What do you "
          "think? Give reasons and examples to support your opinion."),
    hint="Start by saying which task you chose. Plan briefly, write in clear paragraphs, and leave a minute to check your spelling and punctuation.",
    placeholder="Type your answer here; it will be saved for review…",
)

CONTENT_SPEAKING = dict(
    type="speaking",
    stem="Record a short spoken introduction of yourself (about 60-90 seconds).",
    body=("Speak about:\n"
          "• Your name, your age and your current school\n"
          "• A book or film you have enjoyed recently, and why\n"
          "• Something new you learned this year, in school or outside it\n"
          "• One thing you would like to try at your next school, and why\n\n"
          "Speak naturally; this is a chance for your future school to hear you, not a memory test."),
)

CH_PASSAGE_TRAD = (
    "運動會那天，我代表班級參加四人接力賽。輪到我接棒時，我跑得太急，腳一滑，重重地摔在跑道上。膝蓋火辣辣地痛，"
    "我真想坐在地上哭一場。就在這時，我聽見同學們在旁邊大聲喊：「加油！別放棄！」我咬緊牙關，撿起接力棒，"
    "一拐一拐地繼續向前跑。\n\n"
    "雖然我們最後只得了第四名，但同學們都跑過來扶住我，班主任也稱讚我：「你跌倒了還能站起來，這比獎牌更可貴。」\n\n"
    "回家的路上，媽媽幫我在膝蓋貼上藥水膠布。我發現，這一天我雖然沒有贏得比賽，卻贏得了更重要的東西。"
)
CH_PASSAGE_SIMP = (
    "运动会那天，我代表班级参加四人接力赛。轮到我接棒时，我跑得太急，脚一滑，重重地摔在跑道上。膝盖火辣辣地痛，"
    "我真想坐在地上哭一场。就在这时，我听见同学们在旁边大声喊：“加油！别放弃！”我咬紧牙关，捡起接力棒，"
    "一拐一拐地继续向前跑。\n\n"
    "虽然我们最后只得了第四名，但同学们都跑过来扶住我，班主任也称赞我：“你跌倒了还能站起来，这比奖牌更可贵。”\n\n"
    "回家的路上，妈妈帮我在膝盖贴上药水胶布。我发现，这一天我虽然没有赢得比赛，却赢得了更重要的东西。"
)

def _ch(stem_t, stem_s, opts_ts, correct, concept, explanation):
    return dict(
        passage=zh_blocks(CH_PASSAGE_TRAD.replace("\n\n", "<br><br>"), CH_PASSAGE_SIMP.replace("\n\n", "<br><br>")),
        stem=bilingual(stem_t, stem_s),
        options=O(*[(k, bilingual(t, s)) for k, (t, s) in opts_ts.items()]),
        correct=correct, strand="中文閱讀理解", concept="小五中文 · " + concept, explanation=explanation)

CHINESE = [
    _ch("接力賽中，「我」發生了什麼事？", "接力赛中，“我”发生了什么事？",
        {"A": ("忘記帶接力棒", "忘记带接力棒"), "B": ("跑錯了跑道", "跑错了跑道"),
         "C": ("接棒時滑倒受傷", "接棒时滑倒受伤"), "D": ("遲到了，趕不上比賽", "迟到了，赶不上比赛")},
        "C", "內容理解：事件", "文中寫道：輪到「我」接棒時跑得太急，腳一滑，摔在跑道上，膝蓋很痛。"),
    _ch("跌倒以後，「我」為什麼能繼續跑下去？", "跌倒以后，“我”为什么能继续跑下去？",
        {"A": ("因為聽到同學大聲為我打氣", "因为听到同学大声为我打气"),
         "B": ("因為老師把我扶了起來", "因为老师把我扶了起来"),
         "C": ("因為想拿第一名", "因为想拿第一名"),
         "D": ("因為膝蓋已經不痛了", "因为膝盖已经不痛了")},
        "A", "內容理解：人物動機", "「我」聽見同學們喊「加油！別放棄！」，便咬緊牙關繼續跑。扶住「我」是比賽結束後的事。"),
    _ch("文中「火辣辣」是形容什麼？", "文中“火辣辣”是形容什么？",
        {"A": ("天氣非常炎熱", "天气非常炎热"), "B": ("跑道被太陽曬得很燙", "跑道被太阳晒得很烫"),
         "C": ("心情非常緊張", "心情非常紧张"), "D": ("膝蓋像被火燒一樣痛", "膝盖像被火烧一样痛")},
        "D", "詞語理解", "「火辣辣」在文中形容摔倒後膝蓋灼熱的痛感，不是形容天氣或心情。"),
    _ch("「我們」最後得了第幾名？", "“我们”最后得了第几名？",
        {"A": ("第一名", "第一名"), "B": ("第四名", "第四名"),
         "C": ("第二名", "第二名"), "D": ("沒有完成比賽", "没有完成比赛")},
        "B", "內容理解：細節", "文中說：雖然我們最後只得了第四名。「我」帶傷跑完，並沒有退出比賽。"),
    _ch("班主任說「這比獎牌更可貴」，「這」指的是：", "班主任说“这比奖牌更可贵”，“这”指的是：",
        {"A": ("跑得最快的速度", "跑得最快的速度"), "B": ("全班同學的獎牌", "全班同学的奖牌"),
         "C": ("跌倒後仍堅持完成比賽的精神", "跌倒后仍坚持完成比赛的精神"), "D": ("同學送的禮物", "同学送的礼物")},
        "C", "內容理解：句意", "班主任稱讚的是「跌倒了還能站起來」，即跌倒後仍堅持跑完的精神，所以比獎牌更可貴。"),
    _ch("這篇文章主要想帶出什麼道理？", "这篇文章主要想带出什么道理？",
        {"A": ("面對挫折不放棄，比勝負更重要", "面对挫折不放弃，比胜负更重要"),
         "B": ("跑步前一定要做熱身運動", "跑步前一定要做热身运动"),
         "C": ("接力賽最重要的是速度", "接力赛最重要的是速度"),
         "D": ("受傷了就應該退出比賽", "受伤了就应该退出比赛")},
        "A", "主旨理解", "全文透過跌倒後堅持完賽的經過，帶出「不放棄比勝負更重要」的主題。"),
]

CH_LISTENING = [
    dict(stem=bilingual("聆聽錄音，然後回答問題。\n\n圖書義賣改在哪裡舉行？", "聆听录音，然后回答问题。\n\n图书义卖改在哪里举行？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("課室", "课室")), ("B", bilingual("禮堂", "礼堂")), ("C", bilingual("操場", "操场")), ("D", bilingual("圖書館", "图书馆"))),
         correct="B", strand="中文聆聽理解", concept="小五中文 · 聆聽：地點（課室是原地點陷阱）",
         explanation="廣播說原定在課室舉行的圖書義賣，現在改在禮堂舉行。"),
    dict(stem=bilingual("義賣幾點開始？", "义卖几点开始？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("十二點", "十二点")), ("B", bilingual("一點半", "一点半")), ("C", bilingual("兩點", "两点")), ("D", bilingual("十二點半", "十二点半"))),
         correct="D", strand="中文聆聽理解", concept="小五中文 · 聆聽：時間（兩點是結束時間陷阱）",
         explanation="義賣中午十二點半開始，兩點結束。"),
    dict(stem=bilingual("每本圖書賣多少錢？", "每本图书卖多少钱？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("五元", "五元")), ("B", bilingual("十元", "十元")), ("C", bilingual("兩元", "两元")), ("D", bilingual("八元", "八元"))),
         correct="A", strand="中文聆聽理解", concept="小五中文 · 聆聽：細節（價錢）",
         explanation="廣播說每本圖書賣五元，請大家自備零錢。"),
    dict(stem=bilingual("同學要在什麼時候之前，把舊圖書交到圖書館？", "同学要在什么时候之前，把旧图书交到图书馆？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("星期五", "星期五")), ("B", bilingual("星期三", "星期三")), ("C", bilingual("星期四", "星期四")), ("D", bilingual("星期二", "星期二"))),
         correct="C", strand="中文聆聽理解", concept="小五中文 · 聆聽：期限（星期五是義賣日陷阱）",
         explanation="舊圖書要在星期四之前交到圖書館；星期五是義賣舉行的日子。"),
]

CH_SPEAKING = dict(
    type="speaking", maxSeconds=120,
    stem=bilingual("請用普通話做一段自我介紹（大約60至90秒）。", "请用普通话做一段自我介绍（大约60至90秒）。"),
    body=zh_blocks("可以說一說：\n• 你的名字、年級和學校\n• 你的家人\n• 你最喜歡的運動或活動，為什麼\n• 一件讓你難忘的事",
                   "可以说一说：\n• 你的名字、年级和学校\n• 你的家人\n• 你最喜欢的运动或活动，为什么\n• 一件让你难忘的事"),
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
