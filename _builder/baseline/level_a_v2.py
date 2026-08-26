# -*- coding: utf-8 -*-
"""HKS Baseline Assessment · Years 3-4 (current Y3-Y4 / G2-G3), version 2. 30 min core.

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
_SC = "Choose the word that best completes the sentence."

# ---- Word Skills (8: 4 picture-based + 4 word-based) ------------------------
_PIC_ODD = "One of these pictures does not belong with the others. Choose the odd one out."

VERBAL = [
    dict(stem=_SYN + "\n\nHAPPY", options=O(("A", "sad"), ("B", "tall"), ("C", "glad"), ("D", "tired")),
         correct="C", strand="Vocabulary: Synonyms", concept="Y3 Vocabulary · synonyms: happy = glad",
         explanation="Happy and glad mean the same thing. Sad is the opposite of happy, not the same."),
    dict(stem=_SYN + "\n\nSHOUT", options=O(("A", "yell"), ("B", "whisper"), ("C", "sing"), ("D", "walk")),
         correct="A", strand="Vocabulary: Synonyms", concept="Y3 Vocabulary · synonyms: shout = yell",
         explanation="To shout is to yell, using a loud voice. Whisper is the opposite, a very quiet voice."),
    dict(stem=_ANT + "\n\nEMPTY", options=O(("A", "open"), ("B", "light"), ("C", "small"), ("D", "full")),
         correct="D", strand="Vocabulary: Antonyms", concept="Y3 Vocabulary · antonyms: empty vs full",
         explanation="The opposite of empty is full. An empty box has nothing inside; a full box cannot hold any more."),
    dict(stem=_SC + "\n\nBen wore his boots because the ground was very ______.",
         options=O(("A", "dry"), ("B", "muddy"), ("C", "sunny"), ("D", "clean")),
         correct="B", strand="Sentence Completion", concept="Y3 Reading · choosing the word that fits the sentence",
         explanation="Boots protect your feet from mud, so the ground was muddy. Dry and clean ground would not need boots."),
    dict(stem=_PIC_ODD + "\n\n🚗 &nbsp;&nbsp; 🚌 &nbsp;&nbsp; 🚂 &nbsp;&nbsp; 🏠",
         options=O(("A", "🚗 car"), ("B", "🚌 bus"), ("C", "🚂 train"), ("D", "🏠 house")),
         correct="D", strand="Word Groups", concept="Y3 Vocabulary · sorting into groups (things that travel vs a building), picture-based",
         explanation="The car, bus and train all move and carry people; the house is a building that stays still."),
    dict(stem=_PIC_ODD + "\n\n👕 &nbsp;&nbsp; 🍦 &nbsp;&nbsp; 🧦 &nbsp;&nbsp; 👟",
         options=O(("A", "👕 shirt"), ("B", "🍦 ice cream"), ("C", "🧦 socks"), ("D", "👟 shoes")),
         correct="B", strand="Word Groups", concept="Y3 Vocabulary · sorting into groups (clothes vs food), picture-based",
         explanation="The shirt, socks and shoes are all clothes you wear; the ice cream is food."),
    dict(stem="Which word matches the picture?\n\n🦒",
         options=O(("A", "giraffe"), ("B", "zebra"), ("C", "horse"), ("D", "elephant")),
         correct="A", strand="Vocabulary: Naming", concept="Y3 Vocabulary · naming words from a picture",
         explanation="The picture shows a giraffe, the animal with a very long neck. A zebra has stripes but a short neck."),
    dict(stem="Which word RHYMES with DOG?",
         options=O(("A", "dig"), ("B", "door"), ("C", "frog"), ("D", "cat")),
         correct="C", strand="Phonics & Rhyme", concept="Y3 Phonics · rhyming words (same ending sound)",
         explanation="Dog and frog both end with the '-og' sound. 'Dig' and 'door' start like dog but do not rhyme, and 'cat' is just another animal."),
]

# ---- Picture Puzzles (10 = 8 CAT4-engine + 2 GL-style series) ---------------
_SEQ = "Look at the four pictures in the top row. Work out the pattern, then choose the picture (A-E) that belongs in the empty box."

NONVERBAL = nvr_from_json("level-a", 2) + [
    dict(stem=_SEQ, correct="D", strand="Figure Series (GL style)",
         concept="Y3-4 Non-Verbal Reasoning (GL 11+ series style) · two rules: the square grows AND colours take turns",
         explanation="Two things change together: the square gets a little bigger each time, and the colour takes turns black, white, black, white. The next square must be the biggest one AND black. B is the right size but white, and A has stopped growing.",
         fig=seq_fig([cell(square, 8), lambda cx, cy: square(cx, cy, 11, "none"),
                      cell(square, 14), lambda cx, cy: square(cx, cy, 17, "none")],
                     [cell(square, 17), lambda cx, cy: square(cx, cy, 20, "none"),
                      cell(square, 14), cell(square, 20), lambda cx, cy: square(cx, cy, 8, "none")])),
    dict(stem=_SEQ, correct="E", strand="Figure Series (GL style)",
         concept="Y3-4 Non-Verbal Reasoning (GL 11+ series style) · quarter-turn ANTICLOCKWISE rotation with a mirror trap",
         explanation="The flag shape makes a quarter turn anticlockwise each time; after four turns it is back where it started, so the answer looks exactly like the first picture. C looks close but is a mirror image, and turning a shape can never make its mirror.",
         fig=seq_fig([cell(fshape, 10, 0), cell(fshape, 10, 270), cell(fshape, 10, 180), cell(fshape, 10, 90)],
                     [cell(fshape, 10, 90), cell(fshape, 10, 180), cell(fshape, 10, 0, mirror=True),
                      cell(fshape, 10, 270), cell(fshape, 10, 0)])),
]

# ---- Mathematics (8: 4 with diagrams + 4 story) ----------------------------
MATHS = [
    dict(stem="The pictogram shows how many stickers Mia and Kai collected this month. How many stickers did they collect ALTOGETHER?",
         fig=pictogram([("Mia", 4), ("Kai", 2)], 5, "Each circle"),
         options=O(("A", "6"), ("B", "10"), ("C", "20"), ("D", "30")),
         correct="D", strand="Data & Measure", concept="Y3 Statistics · pictogram where one symbol stands for 5, then adding",
         explanation="Mia has 4 circles (20 stickers) and Kai has 2 circles (10 stickers): 20 + 10 = 30. Choosing 6 means the key was ignored; 20 is Mia's stickers only."),
    dict(stem="The bar chart shows the drinks sold at the snack bar today. How many MORE cartons of milk than juice were sold?",
         fig=bar_chart(["Milk", "Juice", "Water"], [15, 5, 10], 20, 5),
         options=O(("A", "5"), ("B", "10"), ("C", "15"), ("D", "20")),
         correct="B", strand="Data & Measure", concept="Y3 Statistics · reading a bar chart, then finding the difference",
         explanation="Milk = 15 and juice = 5, so 15 − 5 = 10 more. 20 comes from ADDING milk and juice, and 15 is just the milk bar."),
    dict(stem="The diagram shows a SQUARE playground. Every side is the same length. What is the perimeter of the playground (the distance all the way round)?",
         fig=labelled_shape_fig(lambda out: out.extend([
             '<rect x="70" y="26" width="120" height="120" fill="#eef2f8" stroke="#1c2733" stroke-width="2.5"/>',
             svg_text(130, 16, "6 m")]), 260, 170),
         options=O(("A", "12 m"), ("B", "18 m"), ("C", "24 m"), ("D", "36 m")),
         correct="C", strand="Data & Measure", concept="Y3 Measurement · perimeter of a square (four equal sides)",
         explanation="A square has 4 equal sides: 6 + 6 + 6 + 6 = 24 m. 12 is only two sides, 18 is three sides, and 36 is 6 × 6, which is the area."),
    dict(stem="What fraction of this grid is shaded?",
         fig=fraction_grid(2, 5, 4),
         options=O(("A", "4/10"), ("B", "4/6"), ("C", "6/10"), ("D", "1/2")),
         correct="A", strand="Fractions", concept="Y3 Fractions · naming a fraction of a shape (tenths)",
         explanation="4 of the 10 squares are shaded, so 4/10 is shaded. 6/10 counts the UNSHADED squares, and 4/6 compares shaded with unshaded instead of the whole grid."),
    dict(stem="What is 63 − 28?",
         options=O(("A", "34"), ("B", "35"), ("C", "45"), ("D", "91")),
         correct="B", strand="Number", concept="Y3 Number · subtracting 2-digit numbers with exchanging (borrowing)",
         explanation="63 − 28 = 35. Choosing 45 means the smaller digit was taken from the bigger one in each column (8 − 3) instead of exchanging, and 91 comes from adding."),
    dict(stem="A spider has 8 legs. How many legs do 6 spiders have altogether?",
         options=O(("A", "14"), ("B", "40"), ("C", "42"), ("D", "48")),
         correct="D", strand="Number", concept="Y3 Number · 8 times table in a simple story",
         explanation="6 × 8 = 48. 14 comes from ADDING 6 and 8, 40 is 5 × 8, and 42 is 6 × 7."),
    dict(stem="A pencil costs HK$4 and a notebook costs HK$12. Anna pays with a HK$20 note. How much change does she get?",
         options=O(("A", "HK$4"), ("B", "HK$8"), ("C", "HK$16"), ("D", "HK$36")),
         correct="A", strand="Problem Solving", concept="Y3 Measurement · money (HK$) two-step story: add the cost, then find the change",
         explanation="The total cost is 4 + 12 = HK$16, so the change is 20 − 16 = HK$4. HK$16 is the total cost, not the change; HK$8 forgets the pencil; HK$36 adds everything including the note."),
    dict(stem="There are 24 grapes in a bowl. Tom eats one QUARTER of them. How many grapes does Tom eat?",
         options=O(("A", "3"), ("B", "4"), ("C", "6"), ("D", "12")),
         correct="C", strand="Fractions", concept="Y3 Fractions · finding a quarter of a number",
         explanation="A quarter of 24 is 24 ÷ 4 = 6. Choosing 12 means a HALF was found instead, 4 comes from thinking 'a quarter' always means 4, and 3 is 24 ÷ 8."),
]

# ---- Reading (4) ------------------------------------------------------------
PASSAGE_1 = (
    "<strong>The Yellow Umbrella</strong><br><br>"
    "Rain drummed on the roof of the wet market. Mei held her yellow umbrella tight as she "
    "followed Grandma past the fish stall.<br><br>"
    "By the doorway stood an old man. He was holding a newspaper over his head, and his "
    "shoulders were wet through. Mei looked up at Grandma, and Grandma nodded.<br><br>"
    "Mei hurried over and lifted her umbrella high, so it covered them both. The old man "
    "smiled, and his eyes twinkled. 'Thank you, little one,' he said. 'You are as kind as sunshine.'"
)

READING = [
    dict(passage=PASSAGE_1, stem="What did Mei hold tight as she walked through the market?",
         options=O(("A", "a newspaper"), ("B", "her yellow umbrella"), ("C", "a bag of fish"), ("D", "Grandma's hand")),
         correct="B", strand="Reading: Stories", concept="Y3 Reading · finding a detail in the story",
         explanation="The story says Mei held her yellow umbrella tight. The NEWSPAPER belonged to the old man."),
    dict(passage=PASSAGE_1, stem="How could Mei tell that the old man had no umbrella of his own?",
         options=O(("A", "He asked Mei for help"), ("B", "He was crying"),
                   ("C", "He was carrying heavy bags"), ("D", "He held a newspaper over his head and his shoulders were wet")),
         correct="D", strand="Reading: Stories", concept="Y3 Reading · putting story clues together",
         explanation="Two clues go together: he was using a newspaper instead of an umbrella, and he was already wet through. He never spoke until the end, so he did not ask for help."),
    dict(passage=PASSAGE_1, stem="How did the old man feel when Mei shared her umbrella?",
         options=O(("A", "happy and thankful"), ("B", "angry"), ("C", "frightened"), ("D", "sleepy")),
         correct="A", strand="Reading: Stories", concept="Y3 Reading · how a character feels",
         explanation="He smiled, his eyes twinkled, and he said thank you, so he felt happy and thankful."),
    dict(passage=PASSAGE_1, stem="What does 'you are as kind as sunshine' mean?",
         options=O(("A", "The rain had stopped"), ("B", "Mei was wearing yellow"),
                   ("C", "Mei's kind help made him feel warm and happy inside"), ("D", "He wanted to go home")),
         correct="C", strand="Reading: Stories", concept="Y3 Reading · understanding a comparison (simile)",
         explanation="It was still raining; he compares Mei's kindness to sunshine because her help made him feel warm and happy, the way sunshine does."),
]

# ---- Listening (3 recordings, 10 Q) ----------------------------------------
_LI = "Listen to the recording, then choose the best answer."
_A1, _A2, _A3 = "listening1.m4a", "listening2.m4a", "listening3.m4a"

AUDIO_TITLES = {
    "listening1.m4a": "Swimming Lesson News",
    "listening2.m4a": "A Special Visitor",
    "listening3.m4a": "PE Instructions",
}

AUDIO = {
    _A1: [("Samantha", 155,
        "Good morning, Class Three! Here is a reminder about swimming day on Thursday. "
        "Our lessons will be at the pool next to the library. "
        "The lesson starts at ten o'clock, so please be changed into your swimsuits by a quarter to ten. "
        "Remember to bring your goggles and a towel. "
        "You do not need to bring a swimming cap, because the school will give everyone a blue one. "
        "If you forget your towel, you can borrow one from the PE office.")],
    _A2: [("Samantha", 152,
        "Last Tuesday, a special visitor came to Tom's class. A vet called Dr Chan came to "
        "talk about caring for animals. She brought her little dog, Mochi, and showed the children "
        "her stethoscope, the special tool she uses to listen to an animal's heart. "
        "Everyone wanted to stroke Mochi, but Dr Chan said they must wash their hands first. "
        "Before she left, she told the class that pets need fresh water every single day.")],
    _A3: [("Daniel", 155,
        "Listen carefully. Here is what to do in PE today. "
        "First, put on your trainers and line up by the door. "
        "We are going to the playground to practise skipping. "
        "Each of you will take one skipping rope from the blue basket. "
        "When you hear two whistles, stop skipping and put your rope back. "
        "If it is too hot outside, we will have our lesson in the hall instead.")],
}

LISTENING = [
    dict(stem=_LI + "\n\nWhere will the swimming lessons be?", audio=_A1,
         options=O(("A", "at the pool next to the hall"), ("B", "at the beach"), ("C", "at the pool next to the library"), ("D", "at the sports centre")),
         correct="C", strand="Listening", concept="Y3 Listening · key detail (place)",
         explanation="The teacher says the lessons will be at the pool next to the library."),
    dict(stem=_LI + "\n\nWhat time does the swimming lesson start?", audio=_A1,
         options=O(("A", "9:45"), ("B", "10:00"), ("C", "10:15"), ("D", "10:30")),
         correct="B", strand="Listening", concept="Y3 Listening · key detail (time); 9:45 is the BE-CHANGED-BY time trap",
         explanation="The lesson starts at ten o'clock; a quarter to ten is when pupils must already be changed."),
    dict(stem=_LI + "\n\nWhat will the school give everyone?", audio=_A1,
         options=O(("A", "goggles"), ("B", "a towel"), ("C", "a swimsuit"), ("D", "a blue swimming cap")),
         correct="D", strand="Listening", concept="Y3 Listening · detail with a near trap (goggles and towel must be BROUGHT; the cap is given)",
         explanation="The school gives everyone a blue swimming cap. Goggles and a towel are things pupils must bring themselves."),
    dict(stem=_LI + "\n\nWhat can you do if you forget your towel?", audio=_A1,
         options=O(("A", "borrow one from the PE office"), ("B", "go home to get one"), ("C", "share with a friend"), ("D", "miss the lesson")),
         correct="A", strand="Listening", concept="Y3 Listening · condition (if you forget your towel)",
         explanation="The teacher says a forgotten towel can be borrowed from the PE office."),
    dict(stem=_LI + "\n\nWho visited Tom's class?", audio=_A2,
         options=O(("A", "a doctor"), ("B", "a dentist"), ("C", "a vet"), ("D", "a farmer")),
         correct="C", strand="Listening", concept="Y3 Listening · key detail (who); the stethoscope may suggest 'doctor'",
         explanation="A vet called Dr Chan visited. She uses a stethoscope like a doctor, but her job is caring for animals."),
    dict(stem=_LI + "\n\nWhat did the children have to do before stroking Mochi?", audio=_A2,
         options=O(("A", "put on gloves"), ("B", "wash their hands"), ("C", "sit in a circle"), ("D", "line up quietly")),
         correct="B", strand="Listening", concept="Y3 Listening · remembering an instruction",
         explanation="Dr Chan said they must wash their hands first."),
    dict(stem=_LI + "\n\nWhat did Dr Chan say pets need every day?", audio=_A2,
         options=O(("A", "a warm bath"), ("B", "new toys"), ("C", "a long walk"), ("D", "fresh water")),
         correct="D", strand="Listening", concept="Y3 Listening · key detail (what pets need)",
         explanation="Dr Chan said pets need fresh water every single day."),
    dict(stem=_LI + "\n\nWhat will the class practise in PE today?", audio=_A3,
         options=O(("A", "skipping"), ("B", "running"), ("C", "throwing"), ("D", "dancing")),
         correct="A", strand="Listening", concept="Y3 Listening · following instructions (task)",
         explanation="The teacher says the class is going to the playground to practise skipping."),
    dict(stem=_LI + "\n\nWhere do the skipping ropes come from?", audio=_A3,
         options=O(("A", "the PE office"), ("B", "the blue basket"), ("C", "the hall"), ("D", "the teacher's bag")),
         correct="B", strand="Listening", concept="Y3 Listening · following instructions (where)",
         explanation="Each pupil takes one skipping rope from the blue basket."),
    dict(stem=_LI + "\n\nWhat should you do when you hear TWO whistles?", audio=_A3,
         options=O(("A", "start skipping faster"), ("B", "line up by the door"), ("C", "stop skipping and put your rope back"), ("D", "swap ropes with a partner")),
         correct="C", strand="Listening", concept="Y3 Listening · following instructions; 'line up by the door' happens BEFORE the lesson (trap)",
         explanation="Two whistles mean stop skipping and put the rope back. Lining up by the door was the FIRST instruction, before going outside."),
]

# ---- Reading Aloud & Speaking ----------------------------------------------
CONTENT_SPEAKING = [
    dict(type="speaking", maxSeconds=90,
         stem="Part 1 of 2: Read this story aloud, clearly and with expression.",
         body=("\"One morning, Lily found a small snail on the classroom window. It moved slowly, leaving a "
               "shiny silver line behind it. 'You must be lost,' Lily whispered. At break time, she carried "
               "it gently to the garden and set it down under a big green leaf. 'There you are, little snail. "
               "Home at last!'\"\n\nWhen you have finished reading, press stop. The next page is a NEW recording."),
         strand="Speaking", concept="Y3 Speaking · reading aloud (decoding and fluency)"),
    dict(type="speaking", maxSeconds=90,
         stem="Part 2 of 2: Now tell us about yourself. This is a new recording.",
         body=("• Your name, your age and the name of your school\n"
               "• Your favourite animal, and why you like it\n"
               "• Something you are good at, and how you got better at it"),
         strand="Speaking", concept="Y3 Speaking · self-introduction"),
]

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
# their Primary Curriculum Handbook (G2 大量篇章和圖書閱讀 / 100-150 字寫作;
# G3 廣泛閱讀和詞彙積累 / 200-250 字寫作). Traditional leads, Simplified
# follows, NO pinyin (ISF policy). Two single-sentence word items ramp in
# before the ~180 字 passage so a non-immersion applicant still scores.
# ============================================================================

def _bi(trad, simp):
    return f"{trad}<br><i>{simp}</i>" if simp and simp != trad else trad



CH_PASSAGE_TRAD = (
    "上個星期天，爺爺帶我到公園放風箏。那是一隻紅色的蝴蝶風箏，上面的花紋是我自己畫的。<br><br>"
    "那天風很大，風箏飛得又高又穩，我開心得跳了起來。可是不知道甚麼時候，線忽然斷了。"
    "風箏越飛越遠，最後變成天上一個小紅點，不見了。<br><br>"
    "我站在草地上，眼睛有點酸。爺爺蹲下來，拍拍我的背說：「它去看別的地方了。」"
    "回家的路上，爺爺買了新的紙和竹枝，說明天教我做一隻更大的。我點點頭，心裏又暖起來。"
)
CH_PASSAGE_SIMP = (
    "上个星期天，爷爷带我到公园放风筝。那是一只红色的蝴蝶风筝，上面的花纹是我自己画的。<br><br>"
    "那天风很大，风筝飞得又高又稳，我开心得跳了起来。可是不知道什么时候，线忽然断了。"
    "风筝越飞越远，最后变成天上一个小红点，不见了。<br><br>"
    "我站在草地上，眼睛有点酸。爷爷蹲下来，拍拍我的背说：“它去看别的地方了。”"
    "回家的路上，爷爷买了新的纸和竹枝，说明天教我做一只更大的。我点点头，心里又暖起来。"
)
_CH_PASSAGE = zh_blocks(CH_PASSAGE_TRAD, CH_PASSAGE_SIMP)


def _chp(stem_t, stem_s, opts_ts, correct, concept, explanation):
    return dict(passage=_CH_PASSAGE, stem=_bi(stem_t, stem_s),
                options=O(*[(k, _bi(t, s)) for k, (t, s) in opts_ts.items()]),
                correct=correct, strand="中文閱讀理解",
                concept="小二至小三中文 · " + concept, explanation=explanation)


CHINESE_READING = [
    dict(stem=_bi("選出跟「立刻」意思最接近的詞語。", "选出跟“立刻”意思最接近的词语。"),
         options=O(("A", _bi("慢慢", "慢慢")), ("B", _bi("偶爾", "偶尔")),
                   ("C", _bi("從前", "从前")), ("D", _bi("馬上", "马上"))),
         correct="D", strand="中文詞語", concept="小二至小三中文 · 近義詞：立刻＝馬上",
         explanation="「立刻」和「馬上」都表示很快就做，一點也不等。「慢慢」和「從前」都不是這個意思。"),
    dict(stem=_bi("一______字典。哪一個量詞最合適？", "一______字典。哪一个量词最合适？"),
         options=O(("A", _bi("本", "本")), ("B", _bi("條", "条")),
                   ("C", _bi("張", "张")), ("D", _bi("輛", "辆"))),
         correct="A", strand="中文語法", concept="小二至小三中文 · 量詞：本（書冊）",
         explanation="書和字典一類的冊子用「本」，例如一本字典、一本故事書。「條」用於長條形的東西，「張」用於平面的東西，「輛」用於車。"),
    _chp("「我」的風箏是甚麼樣子的？", "“我”的风筝是什么样子的？",
         {"A": ("藍色的小鳥風箏", "蓝色的小鸟风筝"), "B": ("紅色的蝴蝶風箏", "红色的蝴蝶风筝"),
          "C": ("白色的飛機風箏", "白色的飞机风筝"), "D": ("黃色的金魚風箏", "黄色的金鱼风筝")},
         "B", "內容理解：細節",
         "文章第一段說：那是一隻紅色的蝴蝶風箏，上面的花紋是我自己畫的。"),
    _chp("風箏為甚麼飛走了？", "风筝为什么飞走了？",
         {"A": ("爺爺放手了", "爷爷放手了"), "B": ("下雨了", "下雨了"),
          "C": ("線忽然斷了", "线忽然断了"), "D": ("「我」跑得太快", "“我”跑得太快")},
         "C", "內容理解：因果",
         "文中寫道：不知道甚麼時候，線忽然斷了，風箏越飛越遠。"),
    _chp("「眼睛有點酸」表示「我」當時心裏怎樣？", "“眼睛有点酸”表示“我”当时心里怎样？",
         {"A": ("很想哭", "很想哭"), "B": ("很開心", "很开心"),
          "C": ("很生氣", "很生气"), "D": ("很害怕", "很害怕")},
         "A", "詞語理解：情感描寫",
         "風箏不見了，「眼睛有點酸」是快要流眼淚的樣子，表示難過、想哭。"),
    _chp("爺爺買新的紙和竹枝，是想做甚麼？", "爷爷买新的纸和竹枝，是想做什么？",
         {"A": ("送給別的小朋友", "送给别的小朋友"), "B": ("教「我」做一隻更大的風箏", "教“我”做一只更大的风筝"),
          "C": ("修理斷了的線", "修理断了的线"), "D": ("在家裏做手工功課", "在家里做手工功课")},
         "B", "內容理解：人物用意",
         "回家的路上爺爺買了新的紙和竹枝，說明天教我做一隻更大的，所以「我」心裏又暖起來。"),
]

_CH_LI = "聆聽錄音，然後回答問題。"
_CH_LI_S = "聆听录音，然后回答问题。"

CHINESE_LISTENING = [
    dict(stem=_bi(_CH_LI + "\n\n圖書館甚麼時候借書給同學？", _CH_LI_S + "\n\n图书馆什么时候借书给同学？"),
         audio="listening-zh.m4a",
         options=O(("A", _bi("星期一早上", "星期一早上")), ("B", _bi("星期三中午", "星期三中午")),
                   ("C", _bi("星期五下午", "星期五下午")), ("D", _bi("星期六上午", "星期六上午"))),
         correct="C", strand="中文聆聽理解", concept="小二至小三中文 · 聆聽：時間",
         explanation="廣播說：圖書館這個星期五下午會借書給大家。"),
    dict(stem=_bi("小明已經借了兩本書，他還可以再借嗎？", "小明已经借了两本书，他还可以再借吗？"),
         audio="listening-zh.m4a",
         options=O(("A", _bi("可以，再借一本", "可以，再借一本")), ("B", _bi("不可以，他已經借滿兩本了", "不可以，他已经借满两本了")),
                   ("C", _bi("可以，想借多少都行", "可以，想借多少都行")), ("D", _bi("可以，但要多付錢", "可以，但要多付钱"))),
         correct="B", strand="中文聆聽理解", concept="小二至小三中文 · 聆聽：應用規則（每人兩本）",
         explanation="廣播說每人可以借兩本。小明已經借滿兩本，所以不可以再借了。"),
    dict(stem=_bi("借書的時候要帶甚麼？", "借书的时候要带什么？"), audio="listening-zh.m4a",
         options=O(("A", _bi("學生證", "学生证")), ("B", _bi("零用錢", "零用钱")),
                   ("C", _bi("水壺", "水壶")), ("D", _bi("書包", "书包"))),
         correct="A", strand="中文聆聽理解", concept="小二至小三中文 · 聆聽：細節（物品）",
         explanation="廣播說：請記得帶學生證。"),
    dict(stem=_bi("如果書弄破了，應該怎樣做？", "如果书弄破了，应该怎样做？"), audio="listening-zh.m4a",
         options=O(("A", _bi("自己修好", "自己修好")), ("B", _bi("不要還書", "不要还书")),
                   ("C", _bi("買一本新的", "买一本新的")), ("D", _bi("告訴圖書館老師", "告诉图书馆老师"))),
         correct="D", strand="中文聆聽理解", concept="小二至小三中文 · 聆聽：指示",
         explanation="廣播說：如果書弄髒了或者弄破了，要告訴圖書館老師。"),
]

CHINESE_SPEAKING = [
    dict(type="speaking", maxSeconds=90,
         stem=_bi("請用普通話說一說你自己（大約一分鐘）。", "请用普通话说一说你自己（大约一分钟）。"),
         body=zh_blocks(
             "可以說一說：<br>• 你的名字和年級<br>• 你最好的朋友是誰<br>"
             "• 你最喜歡玩甚麼遊戲，為甚麼<br>• 週末你喜歡做甚麼",
             "可以说一说：<br>• 你的名字和年级<br>• 你最好的朋友是谁<br>"
             "• 你最喜欢玩什么游戏，为什么<br>• 周末你喜欢做什么"),
         strand="中文口語", concept="小二至小三中文 · 口語：自我介紹"),
]

AUDIO["listening-zh.m4a"] = [
    ("zh-CN-XiaoxiaoNeural", "-15%",
     "各位同學請注意。圖書館這個星期五下午會借書給大家。每人可以借兩本，"
     "兩個星期以後要還。請記得帶學生證。如果書弄髒了或者弄破了，要告訴圖書館老師。謝謝。")
]
AUDIO_TITLES["listening-zh.m4a"] = "圖書館通告 Library Notice"


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
        "現在是普通話聆聽部分。請按播放鍵，細心聆聽錄音，最多可以播放兩次。",
        "现在是普通话聆听部分。请按播放键，细心聆听录音，最多可以播放两次。"),
    "中文口語 Chinese Speaking": zh_blocks(
        "請用普通話說一說。找一個安靜的地方，說話清楚自然，不用背稿。",
        "请用普通话说一说。找一个安静的地方，说话清楚自然，不用背稿。"),
})

CONTENT["中文閱讀 Chinese Reading"] = CHINESE_READING
CONTENT["中文聆聽 Chinese Listening"] = CHINESE_LISTENING
CONTENT["中文口語 Chinese Speaking"] = CHINESE_SPEAKING
