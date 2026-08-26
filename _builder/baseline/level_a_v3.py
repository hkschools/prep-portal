# -*- coding: utf-8 -*-
"""HKS Baseline Assessment · Years 3-4 (current Y3-Y4 / G2-G3), version 3. 30 min core.

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
    dict(stem=_SYN + "\n\nSMALL", options=O(("A", "huge"), ("B", "little"), ("C", "wide"), ("D", "old")),
         correct="B", strand="Vocabulary: Synonyms", concept="Y3 Vocabulary · synonyms: small = little",
         explanation="Small and little mean the same thing. Huge is the opposite of small, not the same."),
    dict(stem=_SYN + "\n\nSHUT", options=O(("A", "open"), ("B", "push"), ("C", "lock"), ("D", "close")),
         correct="D", strand="Vocabulary: Synonyms", concept="Y3 Vocabulary · synonyms: shut = close",
         explanation="To shut a door is to close it. Open is the opposite, and you can lock a door only after you close it."),
    dict(stem=_ANT + "\n\nFAST", options=O(("A", "slow"), ("B", "quick"), ("C", "late"), ("D", "soft")),
         correct="A", strand="Vocabulary: Antonyms", concept="Y3 Vocabulary · antonyms: fast vs slow",
         explanation="The opposite of fast is slow. Quick means the SAME as fast, so it is the trap answer."),
    dict(stem=_SC + "\n\nIt was so ______ outside that Mia turned on the lamp to read her book.",
         options=O(("A", "bright"), ("B", "warm"), ("C", "dark"), ("D", "windy")),
         correct="C", strand="Sentence Completion", concept="Y3 Reading · choosing the word that fits the sentence",
         explanation="You turn on a lamp when it is dark. Bright is the opposite, and warm or windy weather would not need a lamp."),
    dict(stem=_PIC_ODD + "\n\n🎸 &nbsp;&nbsp; 🎹 &nbsp;&nbsp; 🥁 &nbsp;&nbsp; 🌂",
         options=O(("A", "🎸 guitar"), ("B", "🎹 piano"), ("C", "🥁 drum"), ("D", "🌂 umbrella")),
         correct="D", strand="Word Groups", concept="Y3 Vocabulary · sorting into groups (musical instruments vs not), picture-based",
         explanation="The guitar, piano and drum are all musical instruments; the umbrella keeps you dry and makes no music."),
    dict(stem=_PIC_ODD + "\n\n🦋 &nbsp;&nbsp; 🐢 &nbsp;&nbsp; 🚁 &nbsp;&nbsp; 🪁",
         options=O(("A", "🦋 butterfly"), ("B", "🐢 turtle"), ("C", "🚁 helicopter"), ("D", "🪁 kite")),
         correct="B", strand="Word Groups", concept="Y3 Vocabulary · sorting into groups (things that fly vs not), picture-based",
         explanation="The butterfly, helicopter and kite can all fly up in the sky; the turtle moves slowly on the ground."),
    dict(stem="Which word matches the picture?\n\n🐧",
         options=O(("A", "penguin"), ("B", "duck"), ("C", "owl"), ("D", "chicken")),
         correct="A", strand="Vocabulary: Naming", concept="Y3 Vocabulary · naming words from a picture",
         explanation="The picture shows a penguin, the black and white bird that swims but cannot fly. A duck can fly and is usually brown or white."),
    dict(stem="Which word RHYMES with STAR?",
         options=O(("A", "stamp"), ("B", "sun"), ("C", "car"), ("D", "tree")),
         correct="C", strand="Phonics & Rhyme", concept="Y3 Phonics · rhyming words (same ending sound)",
         explanation="Star and car both end with the '-ar' sound. 'Stamp' starts like star but does not rhyme, and the sun is just another thing in the sky."),
]

# ---- Picture Puzzles (10 = 8 CAT4-engine + 2 GL-style series) ---------------
_SEQ = "Look at the four pictures in the top row. Work out the pattern, then choose the picture (A-E) that belongs in the empty box."

def _ab(rot):
    """Arrow with a small ball riding on one side; the pair rotates TOGETHER."""
    dx, dy = {0: (0, -20), 90: (20, 0), 180: (0, 20), 270: (-20, 0)}[rot]
    return lambda cx, cy: arrow(cx, cy, 34, rot) + circle(cx + dx, cy + dy, 5, "none")

def _ab_mirror(cx, cy):
    """Mirror of the rot-0 pair: arrow LEFT but ball still on TOP (unreachable by rotation)."""
    return arrow(cx, cy, 34, 180) + circle(cx, cy - 20, 5, "none")

NONVERBAL = nvr_from_json("level-a", 3) + [
    dict(stem=_SEQ, correct="D", strand="Figure Series (GL style)",
         concept="Y3-4 Non-Verbal Reasoning (GL 11+ series style) · two rules: one more side each time AND colours take turns",
         explanation="Two things change together: each shape has one more side than the last (3, 4, 5, 6 sides) and the colour takes turns black, white, black, white. The next shape must have 7 sides AND be black. B has 7 sides but is white, and A is stuck on 6 sides.",
         fig=seq_fig([cell(triangle, 16), lambda cx, cy: square(cx, cy, 13, "none"),
                      cell(pentagon, 16), lambda cx, cy: hexagon(cx, cy, 16, "none")],
                     [cell(hexagon, 16), lambda cx, cy: heptagon(cx, cy, 16, "none"),
                      cell(pentagon, 16), cell(heptagon, 16), cell(star, 16)])),
    dict(stem=_SEQ, correct="E", strand="Figure Series (GL style)",
         concept="Y3-4 Non-Verbal Reasoning (GL 11+ series style) · quarter-turn clockwise rotation of a PAIR of shapes, with a mirror trap",
         explanation="The arrow and its little ball turn a quarter turn CLOCKWISE together each time (right, down, left, up), so next the arrow points right again with the ball on top. In C the arrow points left but the ball is still on top: that is a mirror picture, and turning can never make a mirror.",
         fig=seq_fig([_ab(0), _ab(90), _ab(180), _ab(270)],
                     [_ab(270), _ab(90), _ab_mirror, _ab(180), _ab(0)])),
]

# ---- Mathematics (8: 4 with diagrams + 4 story) ----------------------------
MATHS = [
    dict(stem="The pictogram shows how many laps Rosa and Ken swam this term. How many MORE laps did Ken swim than Rosa?",
         fig=pictogram([("Rosa", 3), ("Ken", 5)], 10, "Each circle"),
         options=O(("A", "2"), ("B", "20"), ("C", "50"), ("D", "80")),
         correct="B", strand="Data & Measure", concept="Y3 Statistics · pictogram where one symbol stands for 10",
         explanation="Ken has 2 more circles than Rosa, and each circle means 10 laps: 2 × 10 = 20 more laps. Choosing 2 means the key was ignored; 50 is Ken's total and 80 is BOTH children added."),
    dict(stem="The bar chart shows the pets chosen by children in Class 3. How many children chose cats or fish?",
         fig=bar_chart(["Cats", "Dogs", "Fish"], [6, 9, 3], 12, 3),
         options=O(("A", "3"), ("B", "6"), ("C", "9"), ("D", "18")),
         correct="C", strand="Data & Measure", concept="Y3 Statistics · reading a bar chart, then adding two bars",
         explanation="Cats = 6 and fish = 3, so 6 + 3 = 9 children. 3 is only the fish, 6 is only the cats, and 18 adds ALL three bars."),
    dict(stem="The diagram shows a rectangular flower bed. What is the perimeter of the flower bed (the distance all the way round)?",
         fig=labelled_shape_fig(lambda out: out.extend([
             '<rect x="44" y="56" width="228" height="58" fill="#eef2f8" stroke="#1c2733" stroke-width="2.5"/>',
             svg_text(158, 46, "8 m"), svg_text(32, 90, "2 m", "end")]), 300, 140),
         options=O(("A", "10 m"), ("B", "12 m"), ("C", "16 m"), ("D", "20 m")),
         correct="D", strand="Data & Measure", concept="Y3 Measurement · perimeter of a rectangle",
         explanation="Perimeter = 8 + 2 + 8 + 2 = 20 m. 10 is only two of the sides, 12 is three sides, and 16 is 8 × 2, which is the area."),
    dict(stem="What fraction of this grid is shaded?",
         fig=fraction_grid(2, 3, 5),
         options=O(("A", "5/6"), ("B", "1/6"), ("C", "6/5"), ("D", "1/2")),
         correct="A", strand="Fractions", concept="Y3 Fractions · naming a fraction of a shape (sixths)",
         explanation="5 of the 6 squares are shaded, so 5/6 is shaded. 1/6 is the UNSHADED part, and 6/5 puts the numbers upside down."),
    dict(stem="What is 38 + 45?",
         options=O(("A", "73"), ("B", "83"), ("C", "84"), ("D", "93")),
         correct="B", strand="Number", concept="Y3 Number · adding 2-digit numbers with carrying",
         explanation="38 + 45 = 83. Choosing 73 means the carried ten was forgotten, and 93 means an extra ten was carried."),
    dict(stem="Stickers come in packs of 7. Priya buys 4 packs. How many stickers does she get?",
         options=O(("A", "11"), ("B", "21"), ("C", "28"), ("D", "35")),
         correct="C", strand="Number", concept="Y3 Number · 7 times table in a simple story",
         explanation="4 × 7 = 28. 11 comes from ADDING 4 and 7, 21 is only 3 packs, and 35 is 5 packs."),
    dict(stem="The film starts at 4:30 and lasts 45 minutes. What time does the film finish?",
         options=O(("A", "4:45"), ("B", "4:75"), ("C", "5:00"), ("D", "5:15")),
         correct="D", strand="Problem Solving", concept="Y3 Measurement · time story problem (crossing the hour)",
         explanation="30 minutes takes us to 5:00, and the other 15 minutes takes us to 5:15. '4:75' forgets that 60 minutes make a new hour, 4:45 adds only 15 minutes, and 5:00 adds only 30."),
    dict(stem="A jug holds 900 mL of juice. Mum pours 3 glasses, and each glass holds 200 mL. How much juice is LEFT in the jug?",
         options=O(("A", "300 mL"), ("B", "600 mL"), ("C", "700 mL"), ("D", "900 mL")),
         correct="A", strand="Problem Solving", concept="Y3 Measurement · capacity (mL) two-step story: multiply, then subtract",
         explanation="3 × 200 = 600 mL poured out, so 900 − 600 = 300 mL is left. 600 is the amount POURED, not left; 700 subtracts only one glass; 900 forgets to pour anything."),
]

# ---- Reading (4) ------------------------------------------------------------
PASSAGE_1 = (
    "<strong>The Runaway Hat</strong><br><br>"
    "Jun and his little sister were eating noodles at their favourite stall when the wind "
    "snatched Grandpa's straw hat. It rolled down the street like a runaway wheel.<br><br>"
    "Jun jumped up so fast that his chair fell over. He chased the hat past the bakery and "
    "past the bus stop, and at last he trapped it under his foot.<br><br>"
    "The hat was a little dusty when he carried it back, but Grandpa laughed and laughed. "
    "'My hero!' he said, and he bought Jun an egg tart to say thank you."
)

READING = [
    dict(passage=PASSAGE_1, stem="What did the wind blow away?",
         options=O(("A", "Jun's noodles"), ("B", "a paper bag"), ("C", "Grandpa's straw hat"), ("D", "Grandpa's scarf")),
         correct="C", strand="Reading: Stories", concept="Y3 Reading · finding a detail in the story",
         explanation="The story says the wind snatched Grandpa's straw hat."),
    dict(passage=PASSAGE_1, stem="Which clue shows that Jun got up in a great hurry?",
         options=O(("A", "His chair fell over"), ("B", "He was eating noodles"),
                   ("C", "The hat was dusty"), ("D", "Grandpa laughed")),
         correct="A", strand="Reading: Stories", concept="Y3 Reading · putting story clues together",
         explanation="Jun jumped up SO fast that his chair fell over; a falling chair shows he moved in a great hurry. The dust and the laughing happen later in the story."),
    dict(passage=PASSAGE_1, stem="How did Grandpa feel when Jun brought the hat back?",
         options=O(("A", "cross about the dust"), ("B", "sad"), ("C", "worried"), ("D", "pleased and proud")),
         correct="D", strand="Reading: Stories", concept="Y3 Reading · how a character feels",
         explanation="Grandpa laughed, called Jun 'my hero' and bought him an egg tart, so he was pleased and proud. He did not mind the dust at all."),
    dict(passage=PASSAGE_1, stem="What does 'it rolled down the street like a runaway wheel' tell us about the hat?",
         options=O(("A", "The hat was broken"), ("B", "The hat was round and rolling away fast"),
                   ("C", "The hat was on a bicycle"), ("D", "The street was round")),
         correct="B", strand="Reading: Stories", concept="Y3 Reading · understanding a comparison (simile)",
         explanation="The hat is compared to a runaway wheel because it is round and it rolled away quickly, which is why Jun had to chase it."),
]

# ---- Listening (3 recordings, 10 Q) ----------------------------------------
_LI = "Listen to the recording, then choose the best answer."
_A1, _A2, _A3 = "listening1.m4a", "listening2.m4a", "listening3.m4a"

AUDIO_TITLES = {
    "listening1.m4a": "Sports Day News",
    "listening2.m4a": "A Special Visitor",
    "listening3.m4a": "Garden Lesson Instructions",
}

AUDIO = {
    _A1: [("Samantha", 155,
        "Good morning, Class Three! Here is some news about Sports Day next Tuesday. "
        "All the races will be on the school field. "
        "Please come to school wearing your house T-shirt and comfortable shoes. "
        "The first race begins at half past nine. "
        "Please do not bring sweets or fizzy drinks; there will be fruit and water for everyone. "
        "If the weather is very bad, Sports Day will move to Wednesday.")],
    _A2: [("Samantha", 152,
        "On Monday, a special visitor came to Anna's class. A baker called Mr Ho came to "
        "show the children how bread is made. He brought a big bag of flour, and he let everyone "
        "knead a small piece of dough. It felt soft and stretchy, like play dough. "
        "Mr Ho told the class that his work starts at four o'clock in the morning, "
        "while everyone else is still asleep. Before he left, he gave each child a little raisin roll.")],
    _A3: [("Daniel", 155,
        "Listen carefully. Here is what to do in our garden lesson today. "
        "First, collect a small pot and fill it with soil up to the line. "
        "Next, use one finger to make a hole, and drop in two sunflower seeds. "
        "Cover the seeds gently and add a little water, but not too much. "
        "Then write your name on a stick and push it into the soil. "
        "We will put all the pots on the sunny shelf by the window.")],
}

LISTENING = [
    dict(stem=_LI + "\n\nWhere will the Sports Day races be?", audio=_A1,
         options=O(("A", "at the sports centre"), ("B", "in the playground"), ("C", "in the park"), ("D", "on the school field")),
         correct="D", strand="Listening", concept="Y3 Listening · key detail (place)",
         explanation="The teacher says all the races will be on the school field."),
    dict(stem=_LI + "\n\nWhat time does the first race begin?", audio=_A1,
         options=O(("A", "8:30"), ("B", "9:00"), ("C", "9:30"), ("D", "10:30")),
         correct="C", strand="Listening", concept="Y3 Listening · key detail (time): 'half past nine'",
         explanation="The first race begins at half past nine, which is 9:30."),
    dict(stem=_LI + "\n\nWhat must pupils NOT bring?", audio=_A1,
         options=O(("A", "sweets and fizzy drinks"), ("B", "fruit and water"), ("C", "their house T-shirt"), ("D", "comfortable shoes")),
         correct="A", strand="Listening", concept="Y3 Listening · detail with a near trap (fruit and water are PROVIDED, not banned)",
         explanation="Pupils must not bring sweets or fizzy drinks. Fruit and water ARE mentioned, but the school provides them; the T-shirt and shoes must be worn."),
    dict(stem=_LI + "\n\nWhat happens if the weather is very bad?", audio=_A1,
         options=O(("A", "Sports Day will be cancelled"), ("B", "Sports Day will move to Wednesday"), ("C", "The races will move to the hall"), ("D", "The races will be shorter")),
         correct="B", strand="Listening", concept="Y3 Listening · condition (if the weather is very bad)",
         explanation="The teacher says Sports Day will move to Wednesday, not that it will be cancelled."),
    dict(stem=_LI + "\n\nWhat is Mr Ho's job?", audio=_A2,
         options=O(("A", "a chef in a restaurant"), ("B", "a farmer"), ("C", "a baker"), ("D", "a teacher")),
         correct="C", strand="Listening", concept="Y3 Listening · key detail (who)",
         explanation="Mr Ho is a baker who shows the children how bread is made. A chef cooks meals in a restaurant, which is close but not what the recording says."),
    dict(stem=_LI + "\n\nWhat did the children get to do?", audio=_A2,
         options=O(("A", "knead a piece of dough"), ("B", "bake a loaf of bread"), ("C", "weigh the flour"), ("D", "ice some cakes")),
         correct="A", strand="Listening", concept="Y3 Listening · detail with a near trap (the flour was only BROUGHT; the children kneaded dough)",
         explanation="Mr Ho let everyone knead a small piece of dough. He brought the flour himself, and nobody baked a whole loaf in class."),
    dict(stem=_LI + "\n\nWhat did Mr Ho give each child before he left?", audio=_A2,
         options=O(("A", "a bag of flour"), ("B", "a piece of dough"), ("C", "an egg tart"), ("D", "a little raisin roll")),
         correct="D", strand="Listening", concept="Y3 Listening · key detail (what he gave); the flour is a mentioned-but-wrong trap",
         explanation="He gave each child a little raisin roll. The bag of flour and the dough appear earlier in the story but were not gifts."),
    dict(stem=_LI + "\n\nHow many seeds go in each pot?", audio=_A3,
         options=O(("A", "one"), ("B", "two"), ("C", "three"), ("D", "five")),
         correct="B", strand="Listening", concept="Y3 Listening · following instructions (how many)",
         explanation="The teacher says to drop in two sunflower seeds."),
    dict(stem=_LI + "\n\nWhat should you write your name on?", audio=_A3,
         options=O(("A", "a stick"), ("B", "the pot"), ("C", "a sticker"), ("D", "the shelf")),
         correct="A", strand="Listening", concept="Y3 Listening · following instructions (where the name goes); 'the pot' is the guessable trap",
         explanation="The name goes on a stick, which is then pushed into the soil. Writing on the pot sounds sensible but is not what the teacher said."),
    dict(stem=_LI + "\n\nWhere will all the pots go?", audio=_A3,
         options=O(("A", "by the classroom door"), ("B", "on the sunny shelf by the window"), ("C", "on the teacher's desk"), ("D", "outside in the garden")),
         correct="B", strand="Listening", concept="Y3 Listening · following instructions (where); 'garden' is mentioned in the lesson name but is wrong",
         explanation="The pots go on the sunny shelf by the window. It is a GARDEN lesson, but the pots stay inside the classroom."),
]

# ---- Reading Aloud & Speaking ----------------------------------------------
CONTENT_SPEAKING = [
    dict(type="speaking", maxSeconds=90,
         stem="Part 1 of 2: Read this story aloud, clearly and with expression.",
         body=("\"On Sunday evening, Ben helped his dad cook dinner. He washed the rice until the water ran "
               "clear, and dropped the vegetables into the big pan. Soon the kitchen filled with a warm, "
               "tasty smell. When Mum took her first bite, she smiled and said, 'This is the best dinner "
               "I have ever had!'\"\n\nWhen you have finished reading, press stop. The next page is a NEW recording."),
         strand="Speaking", concept="Y3 Speaking · reading aloud (decoding and fluency)"),
    dict(type="speaking", maxSeconds=90,
         stem="Part 2 of 2: Now tell us about yourself. This is a new recording.",
         body=("• Your name, your age and who is in your family\n"
               "• Your favourite food, and why you like it\n"
               "• A place you love to visit at the weekend, and what you do there"),
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
    "每天早上，我都坐同一輛校車上學。我最喜歡靠窗的位子，可以看見路邊的大樹，"
    "還有早餐店冒出來的白煙。<br><br>"
    "有一天，車上上來一位阿姨，手裏抱着一個小妹妹。那時車廂裏已經沒有空位了。"
    "我猶豫了一下，還是站起來說：「阿姨，您坐這裏吧。」<br><br>"
    "阿姨笑着說謝謝，小妹妹也看着我笑。那天我一路站到學校，腿有點酸，"
    "可是心裏很輕鬆。原來把自己喜歡的東西讓給別人，也是一件開心的事。"
)
CH_PASSAGE_SIMP = (
    "每天早上，我都坐同一辆校车上学。我最喜欢靠窗的位子，可以看见路边的大树，"
    "还有早餐店冒出来的白烟。<br><br>"
    "有一天，车上上来一位阿姨，手里抱着一个小妹妹。那时车厢里已经没有空位了。"
    "我犹豫了一下，还是站起来说：“阿姨，您坐这里吧。”<br><br>"
    "阿姨笑着说谢谢，小妹妹也看着我笑。那天我一路站到学校，腿有点酸，"
    "可是心里很轻松。原来把自己喜欢的东西让给别人，也是一件开心的事。"
)
_CH_PASSAGE = zh_blocks(CH_PASSAGE_TRAD, CH_PASSAGE_SIMP)


def _chp(stem_t, stem_s, opts_ts, correct, concept, explanation):
    return dict(passage=_CH_PASSAGE, stem=_bi(stem_t, stem_s),
                options=O(*[(k, _bi(t, s)) for k, (t, s) in opts_ts.items()]),
                correct=correct, strand="中文閱讀理解",
                concept="小二至小三中文 · " + concept, explanation=explanation)


CHINESE_READING = [
    dict(stem=_bi("選出跟「粗心」意思相反的詞語。", "选出跟“粗心”意思相反的词语。"),
         options=O(("A", _bi("大方", "大方")), ("B", _bi("細心", "细心")),
                   ("C", _bi("快樂", "快乐")), ("D", _bi("安靜", "安静"))),
         correct="B", strand="中文詞語", concept="小二至小三中文 · 反義詞：粗心／細心",
         explanation="「粗心」是做事不小心，「細心」是做事很小心，兩個詞意思相反。"),
    dict(stem=_bi("一______褲子。哪一個量詞最合適？", "一______裤子。哪一个量词最合适？"),
         options=O(("A", _bi("隻", "只")), ("B", _bi("把", "把")),
                   ("C", _bi("條", "条")), ("D", _bi("座", "座"))),
         correct="C", strand="中文語法", concept="小二至小三中文 · 量詞：條（長條形）",
         explanation="長條形的東西用「條」，例如一條褲子、一條毛巾。「隻」用於動物，「把」用於有柄的東西，「座」用於山或建築物。"),
    _chp("「我」為甚麼最喜歡靠窗的位子？", "“我”为什么最喜欢靠窗的位子？",
         {"A": ("那裏比較涼快", "那里比较凉快"), "B": ("可以和朋友聊天", "可以和朋友聊天"),
          "C": ("那裏最快下車", "那里最快下车"), "D": ("沿途的景物很好看", "沿途的景物很好看")},
         "D", "內容理解：原因",
         "文章第一段寫「我」在窗邊看到的東西：路邊的大樹，還有早餐店冒出來的白煙，可見他喜歡沿途的景物。"),
    _chp("車上為甚麼沒有位子給那位阿姨？", "车上为什么没有位子给那位阿姨？",
         {"A": ("阿姨上錯了車", "阿姨上错了车"), "B": ("所有座位都有人坐了", "所有座位都有人坐了"),
          "C": ("司機不讓她坐", "司机不让她坐"), "D": ("阿姨自己想站着", "阿姨自己想站着")},
         "B", "內容理解：細節",
         "文中寫道：那時車廂裏已經沒有空位了。"),
    _chp("文中「猶豫」的意思最接近：", "文中“犹豫”的意思最接近：",
         {"A": ("一時拿不定主意", "一时拿不定主意"), "B": ("很快就決定了", "很快就决定了"),
          "C": ("覺得很生氣", "觉得很生气"), "D": ("覺得很害怕", "觉得很害怕")},
         "A", "詞語理解：猶豫",
         "「我」很喜歡那個位子，所以一時拿不定主意要不要讓出來，這就是「猶豫」。"),
    _chp("這篇文章主要想告訴我們甚麼？", "这篇文章主要想告诉我们什么？",
         {"A": ("坐校車要早一點出門", "坐校车要早一点出门"), "B": ("靠窗的位子最舒服", "靠窗的位子最舒服"),
          "C": ("為別人着想，自己也會快樂", "为别人着想，自己也会快乐"), "D": ("站着比坐着健康", "站着比坐着健康")},
         "C", "主旨理解",
         "文章最後一句點明：原來把自己喜歡的東西讓給別人，也是一件開心的事。"),
]

_CH_LI = "聆聽錄音，然後回答問題。"
_CH_LI_S = "聆听录音，然后回答问题。"

CHINESE_LISTENING = [
    dict(stem=_bi(_CH_LI + "\n\n生日會在甚麼時候舉行？", _CH_LI_S + "\n\n生日会在什么时候举行？"),
         audio="listening-zh.m4a",
         options=O(("A", _bi("星期五下午三點", "星期五下午三点")), ("B", _bi("星期六下午三點", "星期六下午三点")),
                   ("C", _bi("星期六上午十點", "星期六上午十点")), ("D", _bi("星期日下午四點", "星期日下午四点"))),
         correct="B", strand="中文聆聽理解", concept="小二至小三中文 · 聆聽：時間",
         explanation="錄音說：這個星期六下午三點，我們在課室開生日會。"),
    dict(stem=_bi("這次生日會是為誰慶祝的？", "这次生日会是为谁庆祝的？"), audio="listening-zh.m4a",
         options=O(("A", _bi("六月出生的同學", "六月出生的同学")), ("B", _bi("全班每一位同學", "全班每一位同学")),
                   ("C", _bi("老師", "老师")), ("D", _bi("一年級的新同學", "一年级的新同学"))),
         correct="A", strand="中文聆聽理解", concept="小二至小三中文 · 聆聽：對象（全班是過度概括陷阱）",
         explanation="錄音說：慶祝六月出生的同學生日。生日會全班都參加，但慶祝的對象只是六月出生的同學。"),
    dict(stem=_bi("為甚麼不用帶飲料？", "为什么不用带饮料？"), audio="listening-zh.m4a",
         options=O(("A", _bi("課室裏不可以喝東西", "课室里不可以喝东西")), ("B", _bi("飲料太重了", "饮料太重了")),
                   ("C", _bi("同學不喜歡喝", "同学不喜欢喝")), ("D", _bi("老師會準備果汁", "老师会准备果汁"))),
         correct="D", strand="中文聆聽理解", concept="小二至小三中文 · 聆聽：原因",
         explanation="錄音說：不要帶飲料，老師會準備果汁。"),
    dict(stem=_bi("生日會大約甚麼時候結束？", "生日会大约什么时候结束？"), audio="listening-zh.m4a",
         options=O(("A", _bi("三點", "三点")), ("B", _bi("三點半", "三点半")),
                   ("C", _bi("四點", "四点")), ("D", _bi("五點", "五点"))),
         correct="C", strand="中文聆聽理解", concept="小二至小三中文 · 聆聽：推斷時間（三點是開始時間陷阱）",
         explanation="生日會下午三點開始，大約一個小時，所以大約四點結束；錄音也說請爸爸媽媽四點來接。三點是開始的時間。"),
]

CHINESE_SPEAKING = [
    dict(type="speaking", maxSeconds=90,
         stem=_bi("請用普通話說一說你自己（大約一分鐘）。", "请用普通话说一说你自己（大约一分钟）。"),
         body=zh_blocks(
             "可以說一說：<br>• 你的名字和年級<br>• 你住在哪裏，怎樣上學<br>"
             "• 你最喜歡的科目，為甚麼<br>• 你長大以後想做甚麼",
             "可以说一说：<br>• 你的名字和年级<br>• 你住在哪里，怎样上学<br>"
             "• 你最喜欢的科目，为什么<br>• 你长大以后想做什么"),
         strand="中文口語", concept="小二至小三中文 · 口語：自我介紹"),
]

AUDIO["listening-zh.m4a"] = [
    ("zh-CN-XiaoxiaoNeural", "-15%",
     "小朋友們好。這個星期六下午三點，我們在課室開生日會，慶祝六月出生的同學生日。"
     "每人請帶一份小點心，不要帶飲料，老師會準備果汁。生日會大約一個小時，請爸爸媽媽四點來接你們。")
]
AUDIO_TITLES["listening-zh.m4a"] = "生日會通知 Birthday Party Notice"


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
