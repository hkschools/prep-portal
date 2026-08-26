# -*- coding: utf-8 -*-
"""HKS Baseline Assessment · Years 3-4 (current Y3-Y4 / G2-G3), version 1. 30 min core.

Junior format: shorter, simpler language, larger reliance on pictures. No typed
writing (6-8 year olds cannot type fluently); instead the Speaking section asks
the child to READ A SHORT PASSAGE ALOUD and then introduce themselves, so the
recording captures both decoding/fluency and spoken English.
"""
from figlib import *

BAND = "level-a"
BAND_LABEL = "Level A"
YEAR_SPAN = "Years 3-4"
YEARS = ["Year 3", "Year 4"]
RECORD_MAX_S = 180

SECTIONS = [
    {"name": "Word Skills", "minutes": 4},          # 8 Q, half picture-based
    {"name": "Picture Puzzles", "minutes": 5},      # 10 Q at 30 s
    {"name": "Mathematics", "minutes": 7},          # 8 Q, half with diagrams
    {"name": "Reading", "minutes": 3},              # 4 Q
    {"name": "Listening", "minutes": 7},            # 3 recordings, 10 Q
    {"name": "Reading Aloud & Speaking", "minutes": 6},   # two 90 s recordings need room
]

INFO = {
    "Word Skills": "Let's look at some words! Choose the best answer for each question. If you are not sure, choose the answer you think is best and keep going.",
    "Picture Puzzles": "These puzzles use pictures. In some, three pictures go together in the same way: choose the picture that belongs with them. In others, look at how the top pictures change, and choose the picture that completes the grid.",
    "Mathematics": "Read each question carefully and choose the best answer. You can use rough paper for working out.",
    "Reading": "Read the short story carefully, then answer the questions. The story stays on the screen with every question.",
    "Listening": "Now let's listen! There are three short recordings. Press play and listen carefully; you may play each one up to two times. Answer the questions about each recording before moving on.",
    "Reading Aloud & Speaking": "This is the last part! There are TWO short recordings, and each one has its own page. On this page you will read a story aloud. On the NEXT page you will tell us about yourself. Do not try to do both in one recording. Ask a grown-up to help you allow the microphone when the browser asks.",
}

def O(*pairs):
    return {k: v for k, v in pairs}

_SYN = "Choose the word that means the SAME as the word in capitals."
_ANT = "Choose the word that means the OPPOSITE of the word in capitals."
_ODDW = "One of these words does not belong with the others. Choose the odd one out."
_SC = "Choose the word that best completes the sentence."

# ---- Word Skills (8: 4 picture-based + 4 word-based) ------------------------
_PIC_ODD = "One of these pictures does not belong with the others. Choose the odd one out."

VERBAL = [
    dict(stem=_SYN + "\n\nBIG", options=O(("A", "tiny"), ("B", "large"), ("C", "thin"), ("D", "low")),
         correct="B", strand="Vocabulary: Synonyms", concept="Y3 Vocabulary · synonyms: big = large",
         explanation="Big and large mean the same thing."),
    dict(stem=_SYN + "\n\nBEGIN", options=O(("A", "stop"), ("B", "end"), ("C", "start"), ("D", "rest")),
         correct="C", strand="Vocabulary: Synonyms", concept="Y3 Vocabulary · synonyms: begin = start",
         explanation="To begin something is to start it. Stop and end are opposites."),
    dict(stem=_ANT + "\n\nHOT", options=O(("A", "warm"), ("B", "wet"), ("C", "dry"), ("D", "cold")),
         correct="D", strand="Vocabulary: Antonyms", concept="Y3 Vocabulary · antonyms: hot vs cold",
         explanation="The opposite of hot is cold. Warm is close in meaning to hot, not opposite."),
    dict(stem=_SC + "\n\nThe baby was so ______ that she slept all afternoon.",
         options=O(("A", "tired"), ("B", "hungry"), ("C", "loud"), ("D", "fast")),
         correct="A", strand="Sentence Completion", concept="Y3 Reading · choosing the word that fits the sentence",
         explanation="Sleeping all afternoon tells us the baby was tired."),
    dict(stem=_PIC_ODD + "\n\n<span style='font-size:46px;letter-spacing:14px'>🍎 🍌 🥕 🍇</span>",
         options=O(("A", "<span style='font-size:26px'>🍎</span>&nbsp; apple"), ("B", "<span style='font-size:26px'>🍌</span>&nbsp; banana"),
                   ("C", "<span style='font-size:26px'>🥕</span>&nbsp; carrot"), ("D", "<span style='font-size:26px'>🍇</span>&nbsp; grapes")),
         correct="C", strand="Word Groups", concept="Y3 Vocabulary · sorting into groups (fruit vs vegetable), picture-based",
         explanation="The apple, banana and grapes are fruits; the carrot is a vegetable."),
    dict(stem=_PIC_ODD + "\n\n<span style='font-size:46px;letter-spacing:14px'>🐟 🐦 🐝 🌳</span>",
         options=O(("A", "<span style='font-size:26px'>🐟</span>&nbsp; fish"), ("B", "<span style='font-size:26px'>🐦</span>&nbsp; bird"),
                   ("C", "<span style='font-size:26px'>🐝</span>&nbsp; bee"), ("D", "<span style='font-size:26px'>🌳</span>&nbsp; tree")),
         correct="D", strand="Word Groups", concept="Y3 Vocabulary · living-thing groups (animals vs plant), picture-based",
         explanation="The fish, bird and bee are all animals; the tree is a plant."),
    dict(stem="Which word matches the picture?\n\n<span style='font-size:64px'>🚒</span>",
         options=O(("A", "ambulance"), ("B", "fire engine"), ("C", "tractor"), ("D", "aeroplane")),
         correct="B", strand="Vocabulary: Naming", concept="Y3 Vocabulary · naming words from a picture",
         explanation="The picture shows a fire engine. An ambulance carries sick people and is usually white."),
    dict(stem="Which word RHYMES with CAT?",
         options=O(("A", "hat"), ("B", "dog"), ("C", "cup"), ("D", "can")),
         correct="A", strand="Phonics & Rhyme", concept="Y3 Phonics · rhyming words (same ending sound)",
         explanation="Cat and hat both end with the '-at' sound. 'Can' starts the same but does not rhyme."),
]

# ---- Picture Puzzles (10 = 8 CAT4-engine + 2 GL-style series) ---------------
_SEQ = "Look at the four pictures in the top row. Work out the pattern, then choose the picture (A-E) that belongs in the empty box."

NONVERBAL = nvr_from_json("level-a", 1) + [
    dict(stem=_SEQ, correct="D", strand="Figure Series (GL style)",
         concept="Y3-4 Non-Verbal Reasoning (GL 11+ series style) · two rules: one more circle AND colours take turns",
         explanation="Two things change together: the number of circles goes 1, 2, 3, 4 and the colour takes turns black, white, black, white. The next picture must have 5 BLACK circles.",
         fig=seq_fig([cell(dots, 1, 6), lambda cx, cy: dots(cx, cy, 2, 6, "none"),
                      cell(dots, 3, 6), lambda cx, cy: dots(cx, cy, 4, 6, "none")],
                     [cell(dots, 4, 6), lambda cx, cy: dots(cx, cy, 5, 6, "none"),
                      cell(dots, 6, 6), cell(dots, 5, 6), lambda cx, cy: dots(cx, cy, 4, 6, "none")])),
    dict(stem=_SEQ, correct="E", strand="Figure Series (GL style)",
         concept="Y3-4 Non-Verbal Reasoning (GL 11+ series style) · quarter-turn rotation with a mirror trap",
         explanation="The L-shape makes a quarter turn clockwise each time (up, right, down, left), so next it returns to the start. C is a mirror image, which turning can never make.",
         fig=seq_fig([cell(lshape, 12, 0), cell(lshape, 12, 90), cell(lshape, 12, 180), cell(lshape, 12, 270)],
                     [cell(lshape, 12, 90), cell(lshape, 12, 180), cell(lshape, 12, 0, mirror=True),
                      cell(lshape, 12, 270), cell(lshape, 12, 0)])),
]

# ---- Mathematics (8: 4 with diagrams + 4 story) ----------------------------
MATHS = [
    dict(stem="The pictogram shows how many books Amy and Ben read this term. How many MORE books did Ben read than Amy?",
         fig=pictogram([("Amy", 3), ("Ben", 5)], 2, "Each circle"),
         options=O(("A", "1"), ("B", "2"), ("C", "4"), ("D", "10")),
         correct="C", strand="Data & Measure", concept="Y3 Statistics · pictogram where one symbol stands for 2",
         explanation="Ben has 2 more circles than Amy, and each circle means 2 books: 2 × 2 = 4 more books. Choosing 2 means the key was ignored."),
    dict(stem="The bar chart shows the fruit sold at the tuck shop today. How many apples and oranges were sold altogether?",
         fig=bar_chart(["Apples", "Bananas", "Oranges"], [8, 6, 4], 10, 2),
         options=O(("A", "10"), ("B", "12"), ("C", "14"), ("D", "18")),
         correct="B", strand="Data & Measure", concept="Y3 Statistics · reading a bar chart, then adding",
         explanation="Apples = 8 and oranges = 4, so 8 + 4 = 12. 14 comes from adding apples and bananas."),
    dict(stem="The diagram shows a swimming pool. What is the perimeter of the pool (the distance all the way round)?",
         fig=labelled_shape_fig(lambda out: out.extend([
             '<rect x="40" y="30" width="200" height="120" fill="#eef2f8" stroke="#1c2733" stroke-width="2.5"/>',
             svg_text(140, 20, "5 m"), svg_text(24, 96, "3 m", "end")]), 300, 175),
         options=O(("A", "8 m"), ("B", "15 m"), ("C", "16 m"), ("D", "20 m")),
         correct="C", strand="Data & Measure", concept="Y3 Measurement · perimeter of a rectangle",
         explanation="Perimeter = 5 + 3 + 5 + 3 = 16 m. 15 is 5 × 3, which is the area, and 8 is only two of the sides."),
    dict(stem="What fraction of this grid is shaded?",
         fig=fraction_grid(2, 4, 3),
         options=O(("A", "3/8"), ("B", "1/2"), ("C", "5/8"), ("D", "3/4")),
         correct="A", strand="Fractions", concept="Y3 Fractions · naming a fraction of a shape",
         explanation="3 of the 8 squares are shaded, so 3/8 of the grid is shaded."),
    dict(stem="What is 47 + 26?",
         options=O(("A", "63"), ("B", "71"), ("C", "72"), ("D", "73")),
         correct="D", strand="Number", concept="Y3 Number · adding 2-digit numbers with carrying",
         explanation="47 + 26 = 73. Choosing 63 means the carried ten was forgotten."),
    dict(stem="What is half of 18?",
         options=O(("A", "9"), ("B", "10"), ("C", "12"), ("D", "36")),
         correct="A", strand="Fractions", concept="Y3 Fractions · finding half of a number",
         explanation="Half of 18 is 9, because 9 + 9 = 18. 36 is double, not half."),
    dict(stem="School starts at 8:30. The bus ride to school takes 20 minutes. What time must Ben get on the bus to arrive exactly on time?",
         options=O(("A", "8:00"), ("B", "8:10"), ("C", "8:20"), ("D", "8:50")),
         correct="B", strand="Problem Solving", concept="Y3 Measurement · time story problem (working backwards)",
         explanation="Count back 20 minutes from 8:30 to get 8:10. 8:50 is 20 minutes AFTER school starts."),
    dict(stem="Lily has 24 stickers. She gives 8 stickers to her brother, and then buys 5 more. How many stickers does Lily have now?",
         options=O(("A", "11"), ("B", "13"), ("C", "16"), ("D", "21")),
         correct="D", strand="Problem Solving", concept="Y3 Number · two-step story problem (take away, then add)",
         explanation="24 − 8 = 16, then 16 + 5 = 21. Choosing 16 means the 5 new stickers were forgotten."),
]

# ---- Reading (4) ------------------------------------------------------------
PASSAGE_1 = (
    "<strong>The Red Mitten</strong><br><br>"
    "On a windy morning, Max the dog found a red mitten by the park gate. It smelled of biscuits. "
    "Max picked it up gently with his teeth and trotted along the path, sniffing left and right.<br><br>"
    "Near the swings, a small girl was crying. Her hands were cold, and one of them was bare. "
    "Max dropped the mitten at her feet and wagged his tail.<br><br>"
    "“My mitten!” she laughed, pulling it on. She patted Max on the head, and he felt as warm as "
    "summer, even in the cold wind."
)

READING = [
    dict(passage=PASSAGE_1, stem="What did Max find by the park gate?",
         options=O(("A", "a biscuit"), ("B", "a red mitten"), ("C", "a ball"), ("D", "a scarf")),
         correct="B", strand="Reading: Stories", concept="Y3 Reading · finding a detail in the story",
         explanation="The story says Max found a red mitten by the park gate."),
    dict(passage=PASSAGE_1, stem="How did Max know someone might be looking for the mitten?",
         options=O(("A", "He heard the girl call his name"), ("B", "He saw a sign on the gate"),
                   ("C", "He read about it at school"), ("D", "He found a girl whose hand was bare")),
         correct="D", strand="Reading: Stories", concept="Y3 Reading · putting story clues together",
         explanation="The girl was crying and one hand was bare, so the mitten was probably hers."),
    dict(passage=PASSAGE_1, stem="How did the girl feel at the END of the story?",
         options=O(("A", "happy"), ("B", "cold and sad"), ("C", "angry"), ("D", "sleepy")),
         correct="A", strand="Reading: Stories", concept="Y3 Reading · how a character feels",
         explanation="At the end she laughed and patted Max, so she was happy. She was sad at the start."),
    dict(passage=PASSAGE_1, stem="What does “he felt as warm as summer” tell us about Max?",
         options=O(("A", "The sun had come out"), ("B", "Max was wearing the mitten"),
                   ("C", "Helping the girl made Max feel good inside"), ("D", "Max wanted to go home")),
         correct="C", strand="Reading: Stories", concept="Y3 Reading · understanding a comparison (simile)",
         explanation="It was still cold and windy; the warm feeling came from being kind and helping the girl."),
]

# ---- Listening (3 recordings, 10 Q) ----------------------------------------
_LI = "Listen to the recording, then choose the best answer."
_A1, _A2, _A3 = "listening1.m4a", "listening2.m4a", "listening3.m4a"

AUDIO = {
    _A1: [("en-GB-SoniaNeural", "-14%",
        "Good morning, Class Three! Here is some news about our trip on Friday. "
        "We are going to the Science Museum. The bus will leave school at nine o'clock, "
        "so please arrive by half past eight. Remember to bring a water bottle and a hat. "
        "You do not need to bring money, because the museum is free on Fridays. "
        "If it rains, we will visit the library instead. "
        "Please give your permission slip to Miss Lee by Wednesday.")],
    _A2: [("en-US-AvaNeural", "-14%",
        "Yesterday, a special visitor came to Lily's class. A firefighter called Mr Wong "
        "came to talk about his job. He showed the children his shiny yellow helmet, and he "
        "let them try on his big gloves. They were much too large, and everybody laughed. "
        "Before he left, Mr Wong told the class two important things: never play with matches, "
        "and if you ever see smoke, tell a grown-up straight away.")],
    _A3: [("en-GB-ThomasNeural", "-14%",
        "Listen carefully. Here is what to do in art class today. "
        "First, take out your paintbrush and one pot of paint. "
        "Today, everyone will paint a picture of their family. "
        "When you have finished, wash your brush, and put your picture on the windowsill to dry. "
        "If you finish early, you may choose a book and read quietly at your desk.")],
}

LISTENING = [
    dict(stem=_LI + "\n\nWhere is the class going on Friday?", audio=_A1,
         options=O(("A", "the library"), ("B", "the Science Museum"), ("C", "the park"), ("D", "the swimming pool")),
         correct="B", strand="Listening", concept="Y3 Listening · key detail (place)",
         explanation="The teacher says: 'We are going to the Science Museum.'"),
    dict(stem=_LI + "\n\nWhat time does the bus leave school?", audio=_A1,
         options=O(("A", "8:00"), ("B", "8:30"), ("C", "9:00"), ("D", "9:30")),
         correct="C", strand="Listening", concept="Y3 Listening · key detail (time); 8:30 is the ARRIVAL time trap",
         explanation="The bus leaves at nine o'clock; half past eight is the time pupils must arrive at school."),
    dict(stem=_LI + "\n\nWhat should pupils bring?", audio=_A1,
         options=O(("A", "a water bottle and a hat"), ("B", "money and a snack"), ("C", "an umbrella"), ("D", "a library book")),
         correct="A", strand="Listening", concept="Y3 Listening · key detail (items); money is explicitly NOT needed",
         explanation="Pupils must bring a water bottle and a hat. The teacher says money is not needed because the museum is free on Fridays."),
    dict(stem=_LI + "\n\nWhat will the class do if it rains?", audio=_A1,
         options=O(("A", "stay at school"), ("B", "go on another day"), ("C", "cancel the trip"), ("D", "visit the library instead")),
         correct="D", strand="Listening", concept="Y3 Listening · condition (if it rains)",
         explanation="The teacher says: 'If it rains, we will visit the library instead.'"),
    dict(stem=_LI + "\n\nWho came to visit Lily's class?", audio=_A2,
         options=O(("A", "a doctor"), ("B", "a police officer"), ("C", "a firefighter"), ("D", "a vet")),
         correct="C", strand="Listening", concept="Y3 Listening · key detail (who)",
         explanation="A firefighter called Mr Wong came to talk about his job."),
    dict(stem=_LI + "\n\nWhat did the children try on?", audio=_A2,
         options=O(("A", "his gloves"), ("B", "his helmet"), ("C", "his boots"), ("D", "his jacket")),
         correct="A", strand="Listening", concept="Y3 Listening · detail with a near trap (he SHOWED the helmet, they tried the gloves)",
         explanation="Mr Wong showed the children his helmet, but what they tried on was his big gloves."),
    dict(stem=_LI + "\n\nWhat should you do if you see smoke?", audio=_A2,
         options=O(("A", "hide under a table"), ("B", "pour water on it"), ("C", "shout loudly"), ("D", "tell a grown-up straight away")),
         correct="D", strand="Listening", concept="Y3 Listening · remembering an instruction",
         explanation="Mr Wong said: if you ever see smoke, tell a grown-up straight away."),
    dict(stem=_LI + "\n\nWhat will everyone paint today?", audio=_A3,
         options=O(("A", "their school"), ("B", "their family"), ("C", "a firefighter"), ("D", "the sea")),
         correct="B", strand="Listening", concept="Y3 Listening · following instructions (task)",
         explanation="The teacher says everyone will paint a picture of their family."),
    dict(stem=_LI + "\n\nWhere should the finished pictures go?", audio=_A3,
         options=O(("A", "on the shelf"), ("B", "in a drawer"), ("C", "on the windowsill"), ("D", "on the classroom door")),
         correct="C", strand="Listening", concept="Y3 Listening · following instructions (where)",
         explanation="Finished pictures go on the windowsill to dry."),
    dict(stem=_LI + "\n\nWhat may you do if you finish early?", audio=_A3,
         options=O(("A", "read quietly at your desk"), ("B", "go outside to play"), ("C", "paint another picture"), ("D", "help wash the brushes")),
         correct="A", strand="Listening", concept="Y3 Listening · following instructions (if you finish early)",
         explanation="Early finishers may choose a book and read quietly at their desk."),
]

# ---- Reading Aloud & Speaking (TWO separate recordings) ---------------------
CONTENT_SPEAKING = [
    dict(type="speaking", maxSeconds=90,
         stem="Part 1 of 2: Read this story aloud, clearly and with expression.",
         body=("“On Saturday, Tom and his sister took the ferry across the harbour. "
               "The sea sparkled in the sun, and a white bird flew beside the boat all the way. "
               "When they reached the pier, Tom waved goodbye to the bird and said, "
               "'See you next time, little friend!'”"),
         strand="Speaking", concept="Y3 Speaking · reading aloud (decoding and fluency)"),
    dict(type="speaking", maxSeconds=90,
         stem="Part 2 of 2: Now tell us about yourself. This is a new recording.",
         body=("• Your name, your age and your class\n"
               "• Your favourite book, toy or game, and why you like it\n"
               "• Something fun you did with your family recently"),
         strand="Speaking", concept="Y3 Speaking · self-introduction"),
]

AUDIO_TITLES = {
    "listening1.m4a": "The Friday Trip",
    "listening2.m4a": "A Special Visitor",
    "listening3.m4a": "Art Class Instructions",
}

CONTENT = {
    "Word Skills": VERBAL,
    "Picture Puzzles": NONVERBAL,
    "Mathematics": MATHS,
    "Reading": READING,
    "Listening": LISTENING,
    "Reading Aloud & Speaking": CONTENT_SPEAKING,
}

# ============================================================================
# 中文 (Bilingual edition only) · calibrated to the ISF 弘立 G2-G3 spine from
# their Primary Curriculum Handbook: G2 "大量篇章和圖書閱讀", writing 100-150 字;
# G3 "廣泛閱讀和詞彙積累", writing 200-250 字. So a Y3-4 child at ISF standard
# reads a ~180 字 narrative comfortably. Traditional leads, Simplified follows,
# NO pinyin (ISF policy). Difficulty ramps: two single-sentence word items
# first, then the passage, so a non-immersion applicant still scores something.
# ============================================================================

def _bi(trad, simp):
    return f"{trad}<br><i>{simp}</i>" if simp and simp != trad else trad


CH_PASSAGE_TRAD = (
    "星期三放學的時候，天忽然下起大雨。小明沒有帶雨傘，只好站在校門口等。<br><br>"
    "過了一會兒，同班的美美走過來，把雨傘舉高一點，說：「我們一起走吧，我家就在你家旁邊。」"
    "兩個人擠在一把小雨傘下面，肩膀都濕了一半，卻一路笑個不停。<br><br>"
    "第二天早上，小明從書包裏拿出一包餅乾，放在美美的桌子上。美美問他為甚麼，"
    "小明說：「因為昨天的雨傘。」美美笑着說：「一把雨傘而已。」"
    "小明搖搖頭：「不是雨傘，是你肯陪我一起走。」"
)
CH_PASSAGE_SIMP = (
    "星期三放学的时候，天忽然下起大雨。小明没有带雨伞，只好站在校门口等。<br><br>"
    "过了一会儿，同班的美美走过来，把雨伞举高一点，说：“我们一起走吧，我家就在你家旁边。”"
    "两个人挤在一把小雨伞下面，肩膀都湿了一半，却一路笑个不停。<br><br>"
    "第二天早上，小明从书包里拿出一包饼干，放在美美的桌子上。美美问他为什么，"
    "小明说：“因为昨天的雨伞。”美美笑着说：“一把雨伞而已。”"
    "小明摇摇头：“不是雨伞，是你肯陪我一起走。”"
)
_CH_PASSAGE = zh_blocks(CH_PASSAGE_TRAD, CH_PASSAGE_SIMP)


def _chp(stem_t, stem_s, opts_ts, correct, concept, explanation):
    """Passage-linked reading item."""
    return dict(passage=_CH_PASSAGE, stem=_bi(stem_t, stem_s),
                options=O(*[(k, _bi(t, s)) for k, (t, s) in opts_ts.items()]),
                correct=correct, strand="中文閱讀理解",
                concept="小二至小三中文 · " + concept, explanation=explanation)


CHINESE_READING = [
    dict(stem=_bi("選出跟「安靜」意思最接近的詞語。", "选出跟“安静”意思最接近的词语。"),
         options=O(("A", _bi("熱鬧", "热闹")), ("B", _bi("寧靜", "宁静")),
                   ("C", _bi("忙碌", "忙碌")), ("D", _bi("整齊", "整齐"))),
         correct="B", strand="中文詞語", concept="小二至小三中文 · 近義詞：安靜＝寧靜",
         explanation="「安靜」和「寧靜」都表示沒有吵鬧的聲音。「熱鬧」是相反的意思。"),
    dict(stem=_bi("一______樹。哪一個量詞最合適？", "一______树。哪一个量词最合适？"),
         options=O(("A", _bi("隻", "只")), ("B", _bi("條", "条")),
                   ("C", _bi("張", "张")), ("D", _bi("棵", "棵"))),
         correct="D", strand="中文語法", concept="小二至小三中文 · 量詞：棵（植物）",
         explanation="植物用「棵」，例如一棵樹、一棵草。「隻」用於動物，「條」用於長條形的東西，「張」用於平面的東西。"),
    _chp("小明放學的時候遇到甚麼問題？", "小明放学的时候遇到什么问题？",
         {"A": ("他找不到書包", "他找不到书包"), "B": ("他忘了做功課", "他忘了做功课"),
          "C": ("下大雨，他沒有帶雨傘", "下大雨，他没有带雨伞"), "D": ("他錯過了校車", "他错过了校车")},
         "C", "內容理解：起因",
         "文章開首說：天忽然下起大雨，小明沒有帶雨傘，只好站在校門口等。"),
    _chp("文中「擠」字，說明兩個人怎樣？", "文中“挤”字，说明两个人怎样？",
         {"A": ("靠得很近", "靠得很近"), "B": ("走得很快", "走得很快"),
          "C": ("吵起架來", "吵起架来"), "D": ("站得很遠", "站得很远")},
         "A", "詞語理解：擠",
         "一把小雨傘下面要容下兩個人，所以他們靠得很近，肩膀都濕了一半。"),
    _chp("小明第二天為甚麼把餅乾放在美美桌子上？", "小明第二天为什么把饼干放在美美桌子上？",
         {"A": ("他不喜歡吃餅乾", "他不喜欢吃饼干"), "B": ("為了多謝美美", "为了多谢美美"),
          "C": ("老師叫他這樣做", "老师叫他这样做"), "D": ("美美向他要餅乾", "美美向他要饼干")},
         "B", "內容理解：人物動機",
         "美美問他為甚麼，小明說「因為昨天的雨傘」，可見餅乾是用來道謝的。"),
    _chp("小明說「不是雨傘，是你肯陪我一起走」，他最想多謝美美甚麼？",
         "小明说“不是雨伞，是你肯陪我一起走”，他最想多谢美美什么？",
         {"A": ("借給他一把新雨傘", "借给他一把新雨伞"), "B": ("送他回家的路很近", "送他回家的路很近"),
          "C": ("美美願意關心他、陪着他", "美美愿意关心他、陪着他"), "D": ("美美的雨傘很漂亮", "美美的雨伞很漂亮")},
         "C", "句意理解：主旨句",
         "小明搖搖頭，說重要的不是雨傘這件東西，而是美美願意分一半雨傘、陪他一起走，那份關心才最珍貴。"),
]

_CH_LI = "聆聽錄音，然後回答問題。"
_CH_LI_S = "聆听录音，然后回答问题。"

CHINESE_LISTENING = [
    dict(stem=_bi(_CH_LI + "\n\n同學們下午要練習甚麼？", _CH_LI_S + "\n\n同学们下午要练习什么？"),
         audio="listening-zh.m4a",
         options=O(("A", _bi("跳繩", "跳绳")), ("B", _bi("游泳", "游泳")),
                   ("C", _bi("跑步", "跑步")), ("D", _bi("打球", "打球"))),
         correct="A", strand="中文聆聽理解", concept="小二至小三中文 · 聆聽：主要事件",
         explanation="廣播說：今天下午第三節課，我們會到操場練習跳繩。"),
    dict(stem=_bi("同學們要準備甚麼？", "同学们要准备什么？"), audio="listening-zh.m4a",
         options=O(("A", _bi("泳衣", "泳衣")), ("B", _bi("水壺", "水壶")),
                   ("C", _bi("運動鞋", "运动鞋")), ("D", _bi("雨傘", "雨伞"))),
         correct="C", strand="中文聆聽理解", concept="小二至小三中文 · 聆聽：細節（物品）",
         explanation="廣播說：請大家穿好運動鞋。"),
    dict(stem=_bi("如果下雨，練習會改在哪裡？", "如果下雨，练习会改在哪里？"), audio="listening-zh.m4a",
         options=O(("A", _bi("操場", "操场")), ("B", _bi("禮堂", "礼堂")),
                   ("C", _bi("課室", "教室")), ("D", _bi("圖書館", "图书馆"))),
         correct="B", strand="中文聆聽理解", concept="小二至小三中文 · 聆聽：條件（操場是原地點陷阱）",
         explanation="廣播說：如果下雨，就改在禮堂。操場是不下雨時的地點。"),
    dict(stem=_bi("這段廣播最可能在甚麼時候播出？", "这段广播最可能在什么时候播出？"), audio="listening-zh.m4a",
         options=O(("A", _bi("午飯的時候", "午饭的时候")), ("B", _bi("放學以後", "放学以后")),
                   ("C", _bi("星期六早上", "星期六早上")), ("D", _bi("早上上課之前", "早上上课之前"))),
         correct="D", strand="中文聆聽理解", concept="小二至小三中文 · 聆聽：推斷（時間線索）",
         explanation="廣播用「各位同學早安」開始，又說「今天下午第三節課」還沒有發生，所以是早上上課之前播出的。"),
]

CHINESE_SPEAKING = [
    dict(type="speaking", maxSeconds=90,
         stem=_bi("請用普通話說一說你自己（大約一分鐘）。", "请用普通话说一说你自己（大约一分钟）。"),
         body=zh_blocks(
             "可以說一說：<br>• 你的名字和年級<br>• 你家裏有甚麼人<br>"
             "• 你最喜歡的動物或食物，為甚麼<br>• 你昨天做了甚麼",
             "可以说一说：<br>• 你的名字和年级<br>• 你家里有什么人<br>"
             "• 你最喜欢的动物或食物，为什么<br>• 你昨天做了什么"),
         strand="中文口語", concept="小二至小三中文 · 口語：自我介紹"),
]

SECTIONS.extend([
    {"name": "中文閱讀 Chinese Reading", "minutes": 6, "opt": "chinese"},
    {"name": "中文聆聽 Chinese Listening", "minutes": 4, "opt": "chinese"},
    {"name": "中文口語 Chinese Speaking", "minutes": 3, "opt": "chspeak"},
])

INFO.update({
    "中文閱讀 Chinese Reading": zh_blocks(
        "首兩題是詞語和量詞題，跟短文沒有關係；其餘各題請根據短文回答。"
        "題目以繁體為主，附簡體對照。",
        "首两题是词语和量词题，跟短文没有关系；其余各题请根据短文回答。"
        "题目以繁体为主，附简体对照。"),
    "中文聆聽 Chinese Listening": zh_blocks(
        "現在是普通話聆聽部分。請按播放鍵，細心聆聽廣播，錄音最多可以播放兩次。",
        "现在是普通话聆听部分。请按播放键，细心聆听广播，录音最多可以播放两次。"),
    "中文口語 Chinese Speaking": zh_blocks(
        "請用普通話說一說你自己。找一個安靜的地方，說話清楚自然，不用背稿。",
        "请用普通话说一说你自己。找一个安静的地方，说话清楚自然，不用背稿。"),
})

AUDIO["listening-zh.m4a"] = [
    ("zh-CN-XiaoxiaoNeural", "-15%",
     "各位同學早安。今天下午第三節課，我們會到操場練習跳繩，請大家準備好運動鞋。"
     "如果下雨，就改在禮堂。練習大約四十分鐘，結束以後請把跳繩交回體育老師。謝謝大家。")
]
AUDIO_TITLES["listening-zh.m4a"] = "校園廣播 School Announcement"

CONTENT["中文閱讀 Chinese Reading"] = CHINESE_READING
CONTENT["中文聆聽 Chinese Listening"] = CHINESE_LISTENING
CONTENT["中文口語 Chinese Speaking"] = CHINESE_SPEAKING
