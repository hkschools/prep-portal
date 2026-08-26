# -*- coding: utf-8 -*-
"""HKS Baseline Assessment · Years 5-6 (current Y5-Y6 / G4-G5), version 1. 45 min core.

Every MCQ's `concept` is curriculum-coded (UK-NC year + topic) so a wrong
answer maps straight to the syllabus area in the report's focus list.
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
    dict(stem=_SYN + "\n\nFRAGILE", options=O(("A", "sturdy"), ("B", "rough"), ("C", "heavy"), ("D", "delicate")),
         correct="D", strand="Vocabulary: Synonyms", concept="Y5-6 Vocabulary · synonyms: fragile = delicate",
         explanation="Fragile means easily broken, in other words delicate. Sturdy is the opposite."),
    dict(stem=_SYN + "\n\nABUNDANT", options=O(("A", "plentiful"), ("B", "scarce"), ("C", "tidy"), ("D", "distant")),
         correct="A", strand="Vocabulary: Synonyms", concept="Y5-6 Vocabulary · synonyms: abundant = plentiful",
         explanation="Abundant means existing in large amounts, in other words plentiful. Scarce is the opposite."),
    dict(stem=_SYN + "\n\nWEARY", options=O(("A", "cheerful"), ("B", "anxious"), ("C", "tired"), ("D", "careless")),
         correct="C", strand="Vocabulary: Synonyms", concept="Y5-6 Vocabulary · synonyms: weary = tired",
         explanation="Weary means very tired."),
    dict(stem=_ANT + "\n\nEXPAND", options=O(("A", "stretch"), ("B", "contract"), ("C", "explode"), ("D", "enlarge")),
         correct="B", strand="Vocabulary: Antonyms", concept="Y5-6 Vocabulary · antonyms: expand vs contract",
         explanation="To expand is to get bigger; to contract is to get smaller. Stretch and enlarge are near-synonyms of expand."),
    dict(stem=_ANT + "\n\nANCIENT", options=O(("A", "antique"), ("B", "historic"), ("C", "fragile"), ("D", "modern")),
         correct="D", strand="Vocabulary: Antonyms", concept="Y5-6 Vocabulary · antonyms: ancient vs modern",
         explanation="Ancient means very old; modern means of the present time. Antique and historic also mean old."),
    dict(stem=_ANT + "\n\nGENEROUS", options=O(("A", "selfish"), ("B", "wealthy"), ("C", "kindly"), ("D", "careful")),
         correct="A", strand="Vocabulary: Antonyms", concept="Y5-6 Vocabulary · antonyms: generous vs selfish",
         explanation="A generous person gives freely; a selfish person keeps things for themselves."),
    dict(stem=_ANA + "\n\nKitten is to cat as puppy is to ______.",
         options=O(("A", "kennel"), ("B", "bone"), ("C", "dog"), ("D", "bark")),
         correct="C", strand="Verbal Analogies", concept="Y5-6 Verbal Reasoning · analogies: young animal to adult",
         explanation="A kitten is a young cat; a puppy is a young dog."),
    dict(stem=_ANA + "\n\nAuthor is to novel as composer is to ______.",
         options=O(("A", "orchestra"), ("B", "symphony"), ("C", "piano"), ("D", "singer")),
         correct="B", strand="Verbal Analogies", concept="Y5-6 Verbal Reasoning · analogies: creator to creation",
         explanation="An author creates a novel; a composer creates a symphony. An orchestra performs music but is not the thing created."),
    dict(stem=_ANA + "\n\nThermometer is to temperature as scale is to ______.",
         options=O(("A", "fish"), ("B", "music"), ("C", "ruler"), ("D", "weight")),
         correct="D", strand="Verbal Analogies", concept="Y5-6 Verbal Reasoning · analogies: instrument to measurement",
         explanation="A thermometer measures temperature; a scale measures weight."),
    dict(stem=_ANA + "\n\nScarce is to plentiful as timid is to ______.",
         options=O(("A", "bold"), ("B", "shy"), ("C", "gentle"), ("D", "quiet")),
         correct="A", strand="Verbal Analogies", concept="Y5-6 Verbal Reasoning · analogies: opposites",
         explanation="Scarce and plentiful are opposites, so the answer must be the opposite of timid, which is bold. Shy is a synonym of timid."),
    dict(stem=_SC + "\n\nAlthough the storm had passed, the fishermen remained ______, refusing to sail until the coastguard declared the harbour safe.",
         options=O(("A", "reckless"), ("B", "cautious"), ("C", "cheerful"), ("D", "impatient")),
         correct="B", strand="Sentence Completion", concept="Y5-6 Reading · sentence completion: context clues (ISEE style)",
         explanation="Refusing to sail until it was declared safe shows care, in other words caution."),
    dict(stem=_SC + "\n\nThe museum's new exhibition proved so ______ that visitors queued around the block for hours.",
         options=O(("A", "ordinary"), ("B", "spacious"), ("C", "popular"), ("D", "fragile")),
         correct="C", strand="Sentence Completion", concept="Y5-6 Reading · sentence completion: context clues (ISEE style)",
         explanation="Long queues of visitors show the exhibition was popular."),
    dict(stem=_SC + "\n\nThe two witnesses gave ______ accounts of the accident, so the police could not work out what had really happened.",
         options=O(("A", "identical"), ("B", "detailed"), ("C", "conflicting"), ("D", "truthful")),
         correct="C", strand="Sentence Completion", concept="Y5-6 Reading · sentence completion: context clues (ISEE style)",
         explanation="The police could not work out the truth because the accounts disagreed: they were conflicting."),
    dict(stem=_GR + "\n\nYesterday, Tom ______ his homework before dinner.",
         options=O(("A", "finishes"), ("B", "finished"), ("C", "will finish"), ("D", "finishing")),
         correct="B", strand="Grammar & Cloze", concept="Y5 Grammar · past simple tense (MAP Language Usage style)",
         explanation="'Yesterday' places the action in the past, so the past simple 'finished' is needed."),
    dict(stem=_GR + "\n\nNeither of the boys ______ finished lunch yet.",
         options=O(("A", "has"), ("B", "have"), ("C", "are"), ("D", "were")),
         correct="A", strand="Grammar & Cloze", concept="Y6 Grammar · subject-verb agreement with 'neither'",
         explanation="'Neither' is singular, so it takes the singular verb 'has'."),
    dict(stem=_GR + "\n\nShe practised every day, ______ she still felt nervous before the concert.",
         options=O(("A", "because"), ("B", "so"), ("C", "unless"), ("D", "yet")),
         correct="D", strand="Grammar & Cloze", concept="Y5 Grammar · connectives: contrast",
         explanation="The two halves contrast (lots of practice, but still nervous), so the contrasting connective 'yet' fits."),
]

# ---- Non-Verbal Reasoning (12 = 9 CAT4-engine + 3 GL-style) -----------------
_SEQ = "Look at the four pictures in the top row. Work out the pattern, then choose the picture (A-E) that belongs in the empty box."
_CODE = "Each picture on the left has a two-letter code. Work out what each letter stands for, then choose the code for the picture marked '?'."

def _dotpos(pos, fill):
    off = {"TL": (-16, -16), "TR": (16, -16), "BR": (16, 16), "BL": (-16, 16), "C": (0, 0)}
    dx, dy = off[pos]
    return lambda cx, cy: square(cx, cy, 24, "none") + circle(cx + dx, cy + dy, 6, fill)

NONVERBAL = nvr_from_json("level-b", 1) + [
    dict(stem=_SEQ, correct="E", strand="Figure Series (GL style)",
         concept="Y5-6 Non-Verbal Reasoning (GL 11+ series style) · two rules: the arrow shrinks AND turns a quarter each step",
         explanation="Two rules run together: the arrow gets smaller each step AND turns 90 degrees clockwise (right, down, left, up). Next comes the smallest arrow pointing right again.",
         fig=seq_fig([cell(arrow, 34, 0), cell(arrow, 30, 90), cell(arrow, 26, 180), cell(arrow, 22, 270)],
                     [cell(arrow, 18, 90), cell(arrow, 22, 0), cell(arrow, 18, 180), cell(arrow, 26, 0), cell(arrow, 18, 0)])),
    dict(stem=_SEQ, correct="A", strand="Figure Series (GL style)",
         concept="Y5-6 Non-Verbal Reasoning (GL 11+ series style) · position cycles round the corners AND shading alternates",
         explanation="The dot moves one corner clockwise each step AND its shading alternates black, white. After (bottom-left, white) comes (top-left, black).",
         fig=seq_fig([_dotpos("TL", INK), _dotpos("TR", "none"), _dotpos("BR", INK), _dotpos("BL", "none")],
                     [_dotpos("TL", INK), _dotpos("TL", "none"), _dotpos("TR", INK), _dotpos("C", INK), _dotpos("BR", "none")])),
    dict(stem=_CODE, correct="C", strand="Figure Codes (GL style)",
         concept="Y5-6 Non-Verbal Reasoning (GL/CEM codes style) · first letter = shape, second letter = shading",
         explanation="K means square and M means circle; T means black and V means white. The mystery picture is a WHITE CIRCLE, so its code is MV.",
         fig=codes_fig([(cell(square, 16, INK), "KT"), (cell(square, 16, "none"), "KV"), (cell(circle, 16, INK), "MT")],
                       cell(circle, 16, "none")),
         options=O(("A", "KT"), ("B", "MT"), ("C", "MV"), ("D", "KV"), ("E", "NV"))),
]

# ---- Mathematics (10: 4 short + 6 story, 4 with diagrams) -------------------
MATHS = [
    # short form
    dict(stem="What is the value of the digit 7 in 274,586?",
         options=O(("A", "700"), ("B", "7,000"), ("C", "70,000"), ("D", "700,000")),
         correct="C", strand="Number & Place Value", concept="Y5 Number · place value in a 6-digit number",
         explanation="The 7 sits in the ten-thousands column: 70,000."),
    dict(stem="The diagram shows angles meeting on a straight line. What is the size of angle x?",
         fig=angles_on_line([58, 49]),
         options=O(("A", "63°"), ("B", "73°"), ("C", "83°"), ("D", "107°")),
         correct="B", strand="Measurement & Geometry", concept="Y5 Geometry · angles on a straight line sum to 180",
         explanation="58 + 49 = 107, and 180 − 107 = 73°. Choosing 107° means the two known angles were added but never subtracted from 180."),
    dict(stem="What is 3/5 of 45?",
         options=O(("A", "18"), ("B", "21"), ("C", "24"), ("D", "27")),
         correct="D", strand="Fractions & Decimals", concept="Y5 Fractions · fraction of an amount",
         explanation="45 divided by 5 is 9, and 9 times 3 is 27."),
    dict(stem="The diagram shows a grid of equal squares. What fraction of the grid is shaded, in its simplest form?",
         fig=fraction_grid(4, 4, 10),
         options=O(("A", "5/8"), ("B", "2/3"), ("C", "3/4"), ("D", "7/8")),
         correct="A", strand="Fractions & Decimals", concept="Y6 Fractions · fraction of a diagram, simplifying 10/16",
         explanation="10 of the 16 squares are shaded: 10/16 = 5/8 in its simplest form."),
    # story form
    dict(stem="The school library owns 1,240 books. This week 385 of them are out on loan, and a parent donates a box of 55 new books. How many books are on the shelves now?",
         options=O(("A", "855"), ("B", "900"), ("C", "910"), ("D", "965")),
         correct="C", strand="Problem Solving", concept="Y5 Number · two-step addition and subtraction problem",
         explanation="1,240 − 385 = 855 on the shelves, then 855 + 55 donated = 910. Choosing 855 means the donation was forgotten."),
    dict(stem="The diagram shows the floor plan of a games room. What is the perimeter of the room?",
         fig=perimeter_fig(),
         options=O(("A", "16 m"), ("B", "18 m"), ("C", "20 m"), ("D", "24 m")),
         correct="C", strand="Measurement & Geometry", concept="Y5 Measurement · perimeter of a compound (L-shaped) figure",
         explanation="Add all six sides: 6 + 2 + 3 + 2 + 3 + 4 = 20 m."),
    dict(stem="A film starts at 3:45 pm. The film itself lasts 1 hour 50 minutes, and there is also a 10-minute interval in the middle. At what time does it finish?",
         options=O(("A", "5:15 pm"), ("B", "5:25 pm"), ("C", "5:35 pm"), ("D", "5:45 pm")),
         correct="D", strand="Measurement & Geometry", concept="Y5 Measurement · elapsed time with an extra step",
         explanation="3:45 pm + 1 h 50 min = 5:35 pm, then + 10 min interval = 5:45 pm. 5:35 means the interval was forgotten."),
    dict(stem="Stickers normally cost HK$4.50 each, but a pack of 6 costs HK$24. Ken buys one pack of 6 and pays with a HK$50 note. How much change does he receive?",
         options=O(("A", "HK$26"), ("B", "HK$27"), ("C", "HK$29"), ("D", "HK$31")),
         correct="A", strand="Problem Solving", concept="Y5 Money · best-buy price then change (two steps)",
         explanation="The pack costs HK$24, so the change is HK$50 − HK$24 = HK$26. Paying 6 × HK$4.50 = HK$27 would ignore the pack price."),
    dict(stem="The bar chart shows the Sports Day points for two of the three houses. Altogether the three houses scored 900 points. How many points did Green House score?",
         fig=bar_chart(["Red", "Blue", "Green"], [350, 250, 0], 400, 50, unit="points", hide=2),
         options=O(("A", "250"), ("B", "300"), ("C", "350"), ("D", "400")),
         correct="B", strand="Problem Solving", concept="Y6 Statistics · reading a bar chart, then a missing-part calculation",
         explanation="Read Red = 350 and Blue = 250 from the chart: 350 + 250 = 600, and 900 − 600 = 300. The distractors are the other two bars' values."),
    dict(stem="In 2024, 36 pupils joined the coding club. In 2025, twice as many joined as in 2024. In 2026, 15 more pupils joined than in 2025. How many pupils joined in 2026?",
         options=O(("A", "72"), ("B", "87"), ("C", "96"), ("D", "102")),
         correct="B", strand="Problem Solving", concept="Y5 Number · multi-step word problem (double, then add)",
         explanation="2025: 36 × 2 = 72. 2026: 72 + 15 = 87."),
]

# ---- Reading Comprehension (10) --------------------------------------------
PASSAGE_1 = (
    "<strong>The Notebook</strong><br><br>"
    "When Mimi's grandmother asked her to help at the family's night-market stall during the school holidays, "
    "Mimi groaned. She had planned to spend her evenings playing games with her cousins, not stacking boxes of "
    "dried fish under buzzing lights.<br><br>"
    "On the first night, Grandma handed her a small notebook. “Every customer has a story,” she said. "
    "“Write down what you notice.” Mimi thought this was a strange kind of homework, but she was too "
    "polite to refuse.<br><br>"
    "By the third evening, the notebook was nearly full. There was Mr Leung, who bought the same soup packets "
    "every Tuesday because they reminded him of his mother's cooking. There were the twin sisters who argued "
    "about everything except their love of preserved plums. And there was a tired nurse who always arrived just "
    "before closing time, and for whom Grandma always saved one last discounted box.<br><br>"
    "When the holidays ended, Grandma asked if Mimi wanted to keep the notebook. Mimi shook her head. Then she "
    "surprised herself. “I'll come back on Saturdays,” she said. “It isn't finished yet.”<br><br>"
    "Later, Mimi's mother asked why she had given up her free Saturdays. Mimi struggled to explain. It was not "
    "the pocket money Grandma slipped her, and it was not really the stories either. It was the way Grandma made "
    "every customer feel like the most important person in the market."
)

PASSAGE_2 = (
    "<strong>The Surprising Octopus</strong><br><br>"
    "Most people do not expect a boneless sea creature to be clever. Yet scientists who study the octopus keep "
    "discovering behaviour that looks remarkably like intelligence.<br><br>"
    "In laboratories, octopuses have learned to unscrew jars to reach the food inside, and a few have even "
    "opened a jar from within. In aquariums, keepers tell of octopuses that squirt water at particular staff "
    "members they dislike, or that slip out of their tanks at night to raid a neighbouring tank for crabs, "
    "sliding home again before morning. One famous octopus in New Zealand, named Inky, escaped through a "
    "drainpipe and vanished into the ocean.<br><br>"
    "What makes this cleverness so surprising is the octopus's unusual body plan. Nearly two-thirds of its nerve "
    "cells are found not in its head but in its eight arms. Each arm can taste, touch, and even make some simple "
    "“decisions” on its own, while the central brain handles the bigger problems.<br><br>"
    "Octopuses also live remarkably short lives: most survive only one or two years. Some scientists believe "
    "this makes their problem-solving even more impressive: an octopus has very little time to learn, and no "
    "parents to teach it, yet it still works out how to open jars, escape tanks and outwit its keepers."
)

_RC = "Y5-6 Reading · "
READING = [
    dict(passage=PASSAGE_1, stem="At the beginning of the story, how did Mimi feel about helping at the stall?",
         options=O(("A", "Excited to earn some pocket money"), ("B", "Disappointed to lose time with her cousins"),
                   ("C", "Curious about the customers"), ("D", "Proud that Grandma had chosen her")),
         correct="B", strand="Reading: Fiction", concept=_RC + "character feelings at the start",
         explanation="She groaned because she had planned to spend her evenings playing games with her cousins."),
    dict(passage=PASSAGE_1, stem="Mimi thought the notebook was “a strange kind of homework”. Why does the writer call it homework?",
         options=O(("A", "Grandma used to be a teacher"), ("B", "Mimi had to hand it in at school"),
                   ("C", "It felt like a task an adult had set her"), ("D", "Mimi could only write it during lessons")),
         correct="C", strand="Reading: Fiction", concept=_RC + "interpreting figurative wording",
         explanation="It was not real schoolwork; it simply felt like a duty an adult had given her, which is why 'homework' is in the sentence."),
    dict(passage=PASSAGE_1, stem="What can we infer from Grandma saving a discounted box for the nurse?",
         options=O(("A", "The nurse always complained about prices"), ("B", "Grandma wanted to sell out quickly"),
                   ("C", "The boxes were nearly out of date"), ("D", "Grandma noticed and cared about her regular customers")),
         correct="D", strand="Reading: Fiction", concept=_RC + "inference about character",
         explanation="Saving something for a tired customer who comes late shows attention and kindness, the same quality Mimi admires at the end."),
    dict(passage=PASSAGE_1, stem="According to the passage, what was the ONE thing the twin sisters agreed about?",
         options=O(("A", "Their love of preserved plums"), ("B", "The best soup packets"),
                   ("C", "The price of dried fish"), ("D", "When the stall should close")),
         correct="A", strand="Reading: Fiction", concept=_RC + "locating a stated detail",
         explanation="They 'argued about everything except their love of preserved plums'."),
    dict(passage=PASSAGE_1, stem="Which sentence best explains why Mimi decided to come back on Saturdays?",
         options=O(("A", "Her mother told her she had to help"), ("B", "She wanted to earn more pocket money"),
                   ("C", "She had come to value how Grandma treated people"), ("D", "Her notebook had no empty pages left")),
         correct="C", strand="Reading: Fiction", concept=_RC + "main message and character change",
         explanation="The last paragraph says it was not the money or the stories, but the way Grandma made every customer feel important."),
    dict(passage=PASSAGE_2, stem="What is the main purpose of this passage?",
         options=O(("A", "To describe evidence that octopuses are surprisingly intelligent"),
                   ("B", "To explain how to care for an octopus in an aquarium"),
                   ("C", "To tell the life story of Inky the octopus"),
                   ("D", "To compare octopuses with other sea creatures")),
         correct="A", strand="Reading: Non-fiction", concept=_RC + "identifying the main purpose",
         explanation="Every paragraph gives examples or explanations of octopus intelligence; Inky is only one example."),
    dict(passage=PASSAGE_2, stem="How did Inky escape from the aquarium?",
         options=O(("A", "By hiding in a food jar"), ("B", "By squirting water at the keepers"),
                   ("C", "By climbing into a neighbouring tank"), ("D", "Through a drainpipe")),
         correct="D", strand="Reading: Non-fiction", concept=_RC + "locating a stated detail",
         explanation="Inky 'escaped through a drainpipe and vanished into the ocean'."),
    dict(passage=PASSAGE_2, stem="In paragraph 2, the word “raid” is closest in meaning to:",
         options=O(("A", "clean out and tidy"), ("B", "make a sudden attack on"),
                   ("C", "swim slowly around"), ("D", "guard carefully")),
         correct="B", strand="Reading: Non-fiction", concept=_RC + "vocabulary in context",
         explanation="The octopuses slip into the neighbouring tank to snatch crabs: a sudden attack to take something."),
    dict(passage=PASSAGE_2, stem="What is unusual about where an octopus keeps most of its nerve cells?",
         options=O(("A", "They are spread through its eight arms rather than its head"),
                   ("B", "They are all inside its central brain"),
                   ("C", "They are stored in its skin for camouflage"),
                   ("D", "They disappear as the octopus grows older")),
         correct="A", strand="Reading: Non-fiction", concept=_RC + "understanding an explained fact",
         explanation="Nearly two-thirds of its nerve cells are in its arms, not its head."),
    dict(passage=PASSAGE_2, stem="According to the passage, which statement is FALSE?",
         options=O(("A", "Some octopuses can open jars from the inside"),
                   ("B", "Octopuses usually live for many years"),
                   ("C", "Some octopuses have escaped from their tanks"),
                   ("D", "An octopus's arms can taste and touch")),
         correct="B", strand="Reading: Non-fiction", concept=_RC + "checking statements against the text",
         explanation="The passage says most octopuses survive only one or two years, which is remarkably SHORT."),
]

# ---- Listening (3 recordings, 10 Q) ----------------------------------------
_LI = "Listen to the recording, then choose the best answer."
_A1, _A2, _A3 = "listening1.m4a", "listening2.m4a", "listening3.m4a"

AUDIO_TITLES = {
    "listening1.m4a": "Sports Day News",
    "listening2.m4a": "The Book Week Competition",
    "listening3.m4a": "A Message from the Coach",
    "listening-zh.m4a": "校園廣播 School Announcement",
}

AUDIO = {
    "listening-zh.m4a": [("zh-CN-XiaoxiaoNeural", "-10%", "各位同学请注意。明天下午的课外活动改在音乐室进行，不再在操场。请大家记得带水壶和笔记本。活动三点开始，四点结束。结束以后，校车会在正门等大家。谢谢。")],
    _A1: [
        ("en-GB-RyanNeural", "-8%", "Hi Maya. Did you hear about Sports Day?"),
        ("en-GB-MaisieNeural", "-8%", "No. What happened?"),
        ("en-GB-RyanNeural", "-8%", "It was supposed to be this Thursday, but the field is flooded after the storm, "
                        "so they've moved it to next Monday."),
        ("en-GB-MaisieNeural", "-8%", "Oh! Does that mean training is cancelled?"),
        ("en-GB-RyanNeural", "-8%", "No, training still happens tomorrow, but in the hall instead of outside. "
                        "And we have to bring our own water, because the fountains are being repaired."),
        ("en-GB-MaisieNeural", "-8%", "Thanks, I'll tell Priya. She was worried her grandparents would miss it. "
                          "They arrive on Saturday."),
        ("en-GB-RyanNeural", "-8%", "Perfect timing, then. They'll be able to come after all."),
    ],
    _A2: [("en-GB-SoniaNeural", "-8%",
        "Attention, everyone. This is an announcement from the school library. "
        "To celebrate Book Week, we are holding a competition: design a bookmark for your favourite story. "
        "Entries must be handed to Mrs Chan at the library desk by Friday afternoon. "
        "The winner will be announced at Monday's assembly, and the prize is a fifty-dollar book voucher. "
        "One more thing: the library will stay open until five o'clock every day during Book Week, "
        "one hour later than usual.")],
    _A3: [("en-US-BrianNeural", "-8%",
        "Hello, this is Coach Lam with a message about Saturday's swimming lesson. "
        "The pool is hosting a gala in the morning, so our lesson will start at half past nine "
        "instead of ten o'clock. Please note that this week everyone must bring goggles AND a swim cap; "
        "no one will be allowed in the water without both. "
        "Also, the main entrance will be closed for the gala, so please come in through the side door "
        "on Nathan Road. See you on Saturday.")],
}

LISTENING = [
    dict(stem=_LI + "\n\nWhy has Sports Day been moved?", audio=_A1,
         options=O(("A", "The field is flooded after the storm"), ("B", "There are not enough teachers"),
                   ("C", "The hall is being repaired"), ("D", "The weather is too hot")),
         correct="A", strand="Listening", concept="Y5 Listening · stated reason",
         explanation="Jack says the field is flooded after the storm, so Sports Day has been moved."),
    dict(stem=_LI + "\n\nWhen will Sports Day take place now?", audio=_A1,
         options=O(("A", "This Thursday"), ("B", "Next Monday"), ("C", "This Saturday"), ("D", "Tomorrow")),
         correct="B", strand="Listening", concept="Y5 Listening · key detail (new date); Thursday is the OLD date trap",
         explanation="It was supposed to be Thursday but has been moved to next Monday."),
    dict(stem=_LI + "\n\nWhere will training happen tomorrow?", audio=_A1,
         options=O(("A", "On the field"), ("B", "It is cancelled"), ("C", "In the hall"), ("D", "At the pool")),
         correct="C", strand="Listening", concept="Y5 Listening · detail with a denial trap (training is NOT cancelled)",
         explanation="Training still happens, but in the hall instead of outside."),
    dict(stem=_LI + "\n\nWhy will Priya be pleased about the change?", audio=_A1,
         options=O(("A", "She dislikes sports"), ("B", "She can skip training"),
                   ("C", "Her team is sure to win"), ("D", "Her grandparents will be able to come")),
         correct="D", strand="Listening", concept="Y6 Listening · inference (grandparents arrive Saturday, before the new Monday date)",
         explanation="Her grandparents arrive on Saturday. Sports Day is now the following Monday, so they will no longer miss it."),
    dict(stem=_LI + "\n\nWhat must students design for the Book Week competition?", audio=_A2,
         options=O(("A", "a poster"), ("B", "a bookmark"), ("C", "a book cover"), ("D", "a badge")),
         correct="B", strand="Listening", concept="Y5 Listening · key detail (competition task)",
         explanation="The competition is to design a bookmark for your favourite story."),
    dict(stem=_LI + "\n\nWhen is the deadline for entries?", audio=_A2,
         options=O(("A", "Monday"), ("B", "Wednesday"), ("C", "Friday afternoon"), ("D", "Saturday")),
         correct="C", strand="Listening", concept="Y5 Listening · deadline; Monday is the ANNOUNCEMENT day trap",
         explanation="Entries go to Mrs Chan by Friday afternoon; Monday is when the winner is announced."),
    dict(stem=_LI + "\n\nWhat is the prize?", audio=_A2,
         options=O(("A", "a fifty-dollar book voucher"), ("B", "a free book"), ("C", "a library card"), ("D", "a trophy")),
         correct="A", strand="Listening", concept="Y5 Listening · key detail (prize)",
         explanation="The winner receives a fifty-dollar book voucher."),
    dict(stem=_LI + "\n\nWhat time does Saturday's swimming lesson start?", audio=_A3,
         options=O(("A", "9:00"), ("B", "9:30"), ("C", "10:00"), ("D", "10:30")),
         correct="B", strand="Listening", concept="Y5 Listening · changed time; 10:00 is the USUAL time trap",
         explanation="Because of the gala, the lesson starts at half past nine instead of the usual ten o'clock."),
    dict(stem=_LI + "\n\nWhat must every swimmer bring this week?", audio=_A3,
         options=O(("A", "only goggles"), ("B", "a towel and a snack"), ("C", "goggles and a swim cap"), ("D", "a kickboard")),
         correct="C", strand="Listening", concept="Y5 Listening · requirement (both items needed)",
         explanation="Everyone must bring goggles AND a swim cap; without both they cannot enter the water."),
    dict(stem=_LI + "\n\nHow should swimmers enter the pool building on Saturday?", audio=_A3,
         options=O(("A", "Through the main entrance"), ("B", "Through the pool gate"),
                   ("C", "Up the back stairs"), ("D", "Through the side door on Nathan Road")),
         correct="D", strand="Listening", concept="Y5 Listening · changed arrangement (main entrance closed)",
         explanation="The main entrance is closed for the gala, so swimmers use the side door on Nathan Road."),
]

# ---- Writing / Speaking / Chinese ------------------------------------------
CONTENT_WRITING = dict(
    type="writing",
    intro="Choose ONE of the two tasks below and type your answer in the box. Aim for about 80-130 words.",
    body=("Task 1: Write about a person who has made a difference in your life. Describe the person and explain, "
          "with examples, how they have changed the way you think or act.\n\n"
          "Task 2: Some schools give students homework every day, while others give almost none. What do you think "
          "schools should do? Give reasons and examples to support your opinion."),
    hint="Start by saying which task you chose. Plan briefly, write in clear paragraphs, and leave a minute to check your spelling and punctuation.",
    placeholder="Type your answer here; it will be saved for review…",
)

CONTENT_SPEAKING = dict(
    type="speaking",
    stem="Record a short spoken introduction of yourself (about 60-90 seconds).",
    body=("Speak about:\n"
          "• Your name, your age and your current school\n"
          "• A subject or hobby you enjoy, and why\n"
          "• One thing you have done that you are proud of\n"
          "• The kind of school you hope to join, and why\n\n"
          "Speak naturally; this is a chance for your future school to hear you, not a memory test."),
)

CH_PASSAGE_TRAD = (
    "媽媽生日那天，我決定親手為她做一份早餐。我學着影片裏的方法煎蛋，可是火開得太大，第一隻蛋很快就燒焦了，"
    "廚房裏冒出一陣黑煙。我有點想放棄，但想起媽媽平日天天早起為我準備早餐，從來沒有喊過一聲辛苦，"
    "便深深吸了一口氣，把火調小，再試一次。\n\n"
    "第二隻蛋終於煎得金黃。我把煎蛋、烤麵包和一杯熱牛奶放在托盤上，端到媽媽面前。媽媽看見早餐，先是一愣，"
    "然後笑得眼睛彎成了月牙。她嚐了一口，說：「這是我吃過最好吃的早餐。」\n\n"
    "其實我知道，煎蛋有一點鹹，麵包也烤得太硬。媽媽說「最好吃」，不是因為味道，而是因為她吃到了我的心意。"
)
CH_PASSAGE_SIMP = (
    "妈妈生日那天，我决定亲手为她做一份早餐。我学着影片里的方法煎蛋，可是火开得太大，第一只蛋很快就烧焦了，"
    "厨房里冒出一阵黑烟。我有点想放弃，但想起妈妈平日天天早起为我准备早餐，从来没有喊过一声辛苦，"
    "便深深吸了一口气，把火调小，再试一次。\n\n"
    "第二只蛋终于煎得金黄。我把煎蛋、烤面包和一杯热牛奶放在托盘上，端到妈妈面前。妈妈看见早餐，先是一愣，"
    "然后笑得眼睛弯成了月牙。她尝了一口，说：“这是我吃过最好吃的早餐。”\n\n"
    "其实我知道，煎蛋有一点咸，面包也烤得太硬。妈妈说“最好吃”，不是因为味道，而是因为她尝到了我的心意。"
)

def _ch(stem_t, stem_s, opts_ts, correct, concept, explanation):
    return dict(
        passage=zh_blocks(CH_PASSAGE_TRAD.replace("\n\n", "<br><br>"), CH_PASSAGE_SIMP.replace("\n\n", "<br><br>")),
        stem=bilingual(stem_t, stem_s),
        options=O(*[(k, bilingual(t, s)) for k, (t, s) in opts_ts.items()]),
        correct=correct, strand="中文閱讀理解", concept="小五中文 · " + concept, explanation=explanation)

CHINESE = [
    _ch("「我」為甚麼要親手做早餐？", "“我”为什么要亲手做早餐？",
        {"A": ("因為媽媽生病了", "因为妈妈生病了"), "B": ("因為那天是媽媽的生日", "因为那天是妈妈的生日"),
         "C": ("因為想學煎蛋", "因为想学煎蛋"), "D": ("因為媽媽叫我做", "因为妈妈叫我做")},
        "B", "內容理解：起因", "文章開首說明：媽媽生日那天，「我」決定親手為她做早餐。"),
    _ch("第一隻蛋燒焦後，「我」為甚麼沒有放棄？", "第一只蛋烧焦后，“我”为什么没有放弃？",
        {"A": ("想起媽媽天天早起為我做早餐的辛勞", "想起妈妈天天早起为我做早餐的辛劳"),
         "B": ("因為影片教我要再試一次", "因为影片教我要再试一次"),
         "C": ("因為媽媽在旁邊鼓勵我", "因为妈妈在旁边鼓励我"),
         "D": ("因為家裏只剩下一隻蛋", "因为家里只剩下一只蛋")},
        "A", "內容理解：人物動機", "文中寫道：想起媽媽天天早起準備早餐、從沒喊過辛苦，「我」便再試一次。"),
    _ch("文中「一愣」的意思最接近：", "文中“一愣”的意思最接近：",
        {"A": ("很生氣", "很生气"), "B": ("很傷心", "很伤心"),
         "C": ("一時感到意外", "一时感到意外"), "D": ("覺得好笑", "觉得好笑")},
        "C", "詞語理解", "「一愣」指一時呆住，表示突然感到意外，之後媽媽才笑起來。"),
    _ch("「我」做的早餐其實有甚麼問題？", "“我”做的早餐其实有什么问题？",
        {"A": ("牛奶涼了", "牛奶凉了"), "B": ("煎蛋燒焦了", "煎蛋烧焦了"),
         "C": ("麵包太軟", "面包太软"), "D": ("煎蛋有點鹹，麵包太硬", "煎蛋有点咸，面包太硬")},
        "D", "內容理解：細節", "最後一段說：煎蛋有一點鹹，麵包也烤得太硬。燒焦的是第一隻蛋，並沒有端給媽媽。"),
    _ch("媽媽說這是「最好吃的早餐」，是因為：", "妈妈说这是“最好吃的早餐”，是因为：",
        {"A": ("味道確實很好", "味道确实很好"), "B": ("她感受到「我」的心意", "她感受到“我”的心意"),
         "C": ("她很久沒有吃早餐", "她很久没有吃早餐"), "D": ("她不想批評「我」", "她不想批评“我”")},
        "B", "內容理解：句意", "文末點明：媽媽說「最好吃」，不是因為味道，而是因為她吃到了「我」的心意。"),
    _ch("這篇文章主要想告訴我們：", "这篇文章主要想告诉我们：",
        {"A": ("做早餐是一件很困難的事", "做早餐是一件很困难的事"), "B": ("煎蛋一定要用小火", "煎蛋一定要用小火"),
         "C": ("用心為家人付出，比結果完美更重要", "用心为家人付出，比结果完美更重要"),
         "D": ("生日一定要送禮物", "生日一定要送礼物")},
        "C", "主旨理解", "全文透過做早餐的經過，帶出「心意比成果重要」的主題。"),
]

CH_LISTENING = [
    dict(stem=bilingual("聆聽錄音，然後回答問題。\n\n明天的課外活動改在哪裡進行？", "聆听录音，然后回答问题。\n\n明天的课外活动改在哪里进行？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("禮堂", "礼堂")), ("B", bilingual("音樂室", "音乐室")), ("C", bilingual("操場", "操场")), ("D", bilingual("圖書館", "图书馆"))),
         correct="B", strand="中文聆聽理解", concept="小五中文 · 聆聽：地點（操場是原地點陷阱）",
         explanation="廣播說活動改在音樂室進行，不再在操場。"),
    dict(stem=bilingual("同學明天要帶什麼？", "同学明天要带什么？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("課本和文具", "课本和文具")), ("B", bilingual("雨傘", "雨伞")), ("C", bilingual("水壺和筆記本", "水壶和笔记本")), ("D", bilingual("零食", "零食"))),
         correct="C", strand="中文聆聽理解", concept="小五中文 · 聆聽：要求物品",
         explanation="廣播提醒大家記得帶水壺和筆記本。"),
    dict(stem=bilingual("活動幾點開始？", "活动几点开始？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("一點", "一点")), ("B", bilingual("兩點", "两点")), ("C", bilingual("兩點半", "两点半")), ("D", bilingual("三點", "三点"))),
         correct="D", strand="中文聆聽理解", concept="小五中文 · 聆聽：時間（四點是結束時間陷阱）",
         explanation="活動三點開始，四點結束。"),
    dict(stem=bilingual("活動結束後，校車在哪裡等大家？", "活动结束后，校车在哪里等大家？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("正門", "正门")), ("B", bilingual("後門", "后门")), ("C", bilingual("操場", "操场")), ("D", bilingual("音樂室", "音乐室"))),
         correct="A", strand="中文聆聽理解", concept="小五中文 · 聆聽：細節（校車位置）",
         explanation="廣播說結束以後，校車會在正門等大家。"),
]

CH_SPEAKING = dict(
    type="speaking", maxSeconds=120,
    stem=bilingual("請用普通話介紹自己（大約60至90秒）。", "请用普通话介绍自己（大约60至90秒）。"),
    body=zh_blocks("可以說一說：\n• 你的名字、年級和學校\n• 你最喜歡的科目，為什麼\n• 你的興趣或愛好\n• 你希望入讀怎樣的學校",
                   "可以说一说：\n• 你的名字、年级和学校\n• 你最喜欢的科目，为什么\n• 你的兴趣或爱好\n• 你希望入读怎样的学校"),
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
