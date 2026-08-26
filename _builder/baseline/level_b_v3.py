# -*- coding: utf-8 -*-
"""HKS Baseline Assessment · Years 5-6 (current Y5-Y6 / G4-G5), version 3. 45 min core.

Every MCQ's `concept` is curriculum-coded (UK-NC year + topic) so a wrong
answer maps straight to the syllabus area in the report's focus list.
Parallel form of level_b_v1/v2: identical structure, all-new content.
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
    dict(stem=_SYN + "\n\nHAZARDOUS", options=O(("A", "safe"), ("B", "exciting"), ("C", "dangerous"), ("D", "distant")),
         correct="C", strand="Vocabulary: Synonyms", concept="Y5-6 Vocabulary · synonyms: hazardous = dangerous",
         explanation="Hazardous means full of danger. Safe is the opposite."),
    dict(stem=_SYN + "\n\nGLEAMING", options=O(("A", "shining"), ("B", "dull"), ("C", "melting"), ("D", "enormous")),
         correct="A", strand="Vocabulary: Synonyms", concept="Y5-6 Vocabulary · synonyms: gleaming = shining",
         explanation="Gleaming means shining brightly, like polished metal. Dull is the opposite."),
    dict(stem=_SYN + "\n\nTHRIVE", options=O(("A", "wither"), ("B", "struggle"), ("C", "arrive"), ("D", "flourish")),
         correct="D", strand="Vocabulary: Synonyms", concept="Y5-6 Vocabulary · synonyms: thrive = flourish",
         explanation="To thrive is to grow strongly and do well, in other words to flourish. Wither and struggle are close to opposites."),
    dict(stem=_ANT + "\n\nRIGID", options=O(("A", "stiff"), ("B", "flexible"), ("C", "solid"), ("D", "brittle")),
         correct="B", strand="Vocabulary: Antonyms", concept="Y5-6 Vocabulary · antonyms: rigid vs flexible",
         explanation="Something rigid cannot bend; something flexible bends easily. Stiff is a synonym of rigid."),
    dict(stem=_ANT + "\n\nCONCEAL", options=O(("A", "hide"), ("B", "cover"), ("C", "lose"), ("D", "reveal")),
         correct="D", strand="Vocabulary: Antonyms", concept="Y5-6 Vocabulary · antonyms: conceal vs reveal",
         explanation="To conceal is to hide something; to reveal is to show it. Hide and cover are synonyms of conceal."),
    dict(stem=_ANT + "\n\nVICTORY", options=O(("A", "defeat"), ("B", "triumph"), ("C", "battle"), ("D", "prize")),
         correct="A", strand="Vocabulary: Antonyms", concept="Y5-6 Vocabulary · antonyms: victory vs defeat",
         explanation="A victory is a win; a defeat is a loss. Triumph is a synonym of victory."),
    dict(stem=_ANA + "\n\nDoctor is to hospital as chef is to ______.",
         options=O(("A", "menu"), ("B", "kitchen"), ("C", "waiter"), ("D", "food")),
         correct="B", strand="Verbal Analogies", concept="Y5-6 Verbal Reasoning · analogies: worker to workplace",
         explanation="A doctor works in a hospital; a chef works in a kitchen. Food is what a chef makes, not where a chef works."),
    dict(stem=_ANA + "\n\nTadpole is to frog as caterpillar is to ______.",
         options=O(("A", "cocoon"), ("B", "leaf"), ("C", "butterfly"), ("D", "worm")),
         correct="C", strand="Verbal Analogies", concept="Y5-6 Verbal Reasoning · analogies: young form to adult form",
         explanation="A tadpole grows into a frog; a caterpillar grows into a butterfly. A cocoon is a stage on the way, not the adult form."),
    dict(stem=_ANA + "\n\nIsland is to water as oasis is to ______.",
         options=O(("A", "desert"), ("B", "palm tree"), ("C", "ocean"), ("D", "camel")),
         correct="A", strand="Verbal Analogies", concept="Y5-6 Verbal Reasoning · analogies: what surrounds it",
         explanation="An island is surrounded by water; an oasis is surrounded by desert. Palm trees and camels are found AT an oasis but do not surround it."),
    dict(stem=_ANA + "\n\nHelmet is to head as glove is to ______.",
         options=O(("A", "finger"), ("B", "arm"), ("C", "warmth"), ("D", "hand")),
         correct="D", strand="Verbal Analogies", concept="Y5-6 Verbal Reasoning · analogies: protection to body part",
         explanation="A helmet protects the head; a glove protects the hand. A glove covers the whole hand, not just one finger."),
    dict(stem=_SC + "\n\nThe old bridge was declared ______, so heavy lorries were no longer allowed to cross it.",
         options=O(("A", "spotless"), ("B", "spacious"), ("C", "unsafe"), ("D", "valuable")),
         correct="C", strand="Sentence Completion", concept="Y5-6 Reading · sentence completion: context clues (ISEE style)",
         explanation="Banning heavy lorries shows the bridge could no longer be trusted: it was declared unsafe."),
    dict(stem=_SC + "\n\nRavi is usually talkative, but he became strangely ______ whenever the missing library book was mentioned.",
         options=O(("A", "cheerful"), ("B", "silent"), ("C", "noisy"), ("D", "honest")),
         correct="B", strand="Sentence Completion", concept="Y5-6 Reading · sentence completion: contrast clue (ISEE style)",
         explanation="'But' signals a contrast with talkative, so the missing word must mean the opposite: silent."),
    dict(stem=_SC + "\n\nThe explorers' supplies were nearly ______, so they turned back before crossing the glacier.",
         options=O(("A", "exhausted"), ("B", "delicious"), ("C", "replaced"), ("D", "invisible")),
         correct="A", strand="Sentence Completion", concept="Y5-6 Reading · sentence completion: context clues (ISEE style)",
         explanation="Turning back suggests they were running out of food and fuel: their supplies were nearly exhausted, meaning used up."),
    dict(stem=_GR + "\n\nBy the time the bell rang, the children ______ their projects.",
         options=O(("A", "finish"), ("B", "had finished"), ("C", "will finish"), ("D", "finishing")),
         correct="B", strand="Grammar & Cloze", concept="Y6 Grammar · past perfect for the earlier of two past events",
         explanation="'By the time the bell rang' means the finishing happened even earlier, so the past perfect 'had finished' is needed."),
    dict(stem=_GR + "\n\nThe author ______ novel won the prize will visit our school in March.",
         options=O(("A", "who"), ("B", "which"), ("C", "whose"), ("D", "whom")),
         correct="C", strand="Grammar & Cloze", concept="Y6 Grammar · relative pronoun 'whose' for possession",
         explanation="The novel belongs to the author, so the possessive relative pronoun 'whose' is needed."),
    dict(stem=_GR + "\n\nTake a raincoat with you ______ the weather changes suddenly.",
         options=O(("A", "unless"), ("B", "so that"), ("C", "although"), ("D", "in case")),
         correct="D", strand="Grammar & Cloze", concept="Y5 Grammar · connectives: 'in case' for a possible future event",
         explanation="You take the raincoat as a precaution against a POSSIBLE change: 'in case' fits. 'Unless' would mean the opposite."),
]

# ---- Non-Verbal Reasoning (12 = 9 CAT4-engine + 3 GL-style) -----------------
_SEQ = "Look at the four pictures in the top row. Work out the pattern, then choose the picture (A-E) that belongs in the empty box."
_CODE = "Each picture on the left has a two-letter code. Work out what each letter stands for, then choose the code for the picture marked '?'."

NONVERBAL = nvr_from_json("level-b", 3) + [
    dict(stem=_SEQ, correct="E", strand="Figure Series (GL style)",
         concept="Y5-6 Non-Verbal Reasoning (GL 11+ series style) · two rules: one more side each step AND shading alternates",
         explanation="Two rules run together: the shape gains one side each step (triangle, square, pentagon, hexagon) AND the shading alternates black, white. Next comes a seven-sided shape, BLACK. B has seven sides but is white, A has stopped at six sides, and D is a star, not a seven-sided shape.",
         fig=seq_fig([cell(triangle, 18, INK), cell(square, 14, "none"), cell(pentagon, 17, INK), cell(hexagon, 17, "none")],
                     [cell(hexagon, 17, INK), cell(heptagon, 17, "none"), cell(pentagon, 17, INK), cell(star, 17, INK), cell(heptagon, 17, INK)])),
    dict(stem=_SEQ, correct="D", strand="Figure Series (GL style)",
         concept="Y5-6 Non-Verbal Reasoning (GL 11+ series style) · two rules: quarter-turn clockwise AND size alternates, with a mirror trap",
         explanation="Two rules run together: the L-shape makes a quarter turn clockwise each step AND its size alternates big, small. After four turns it faces the start way again, and after 'small' comes 'big', so the answer is the BIG upright L. C looks right but is a mirror image, and turning a shape can never make its mirror; A has turned too far, and B is the small size.",
         fig=seq_fig([cell(lshape, 9, 0), cell(lshape, 7, 90), cell(lshape, 9, 180), cell(lshape, 7, 270)],
                     [cell(lshape, 9, 90), cell(lshape, 7, 0), cell(lshape, 9, 0, mirror=True), cell(lshape, 9, 0), cell(lshape, 9, 180)])),
    dict(stem=_CODE, correct="B", strand="Figure Codes (GL style)",
         concept="Y5-6 Non-Verbal Reasoning (GL/CEM codes style) · first letter = shape, second letter = size",
         explanation="P means diamond and Q means star; Z means large and X means small. The mystery picture is a SMALL STAR, so its code is QX.",
         fig=codes_fig([(cell(diamond, 22, INK), "PZ"), (cell(diamond, 12, INK), "PX"), (cell(star, 22, INK), "QZ")],
                       cell(star, 12, INK)),
         options=O(("A", "PX"), ("B", "QX"), ("C", "QZ"), ("D", "PZ"), ("E", "RX"))),
]

# ---- Mathematics (10: 4 short + 6 story, 4 with diagrams) -------------------
MATHS = [
    # short form
    dict(stem="In the number 3.245, what is the VALUE of the digit 4?",
         options=O(("A", "4 units"), ("B", "4 tenths"), ("C", "4 hundredths"), ("D", "4 thousandths")),
         correct="C", strand="Number & Place Value", concept="Y5 Number · decimal place value (hundredths)",
         explanation="The 4 is two places after the decimal point, in the hundredths column: 4 hundredths, or 0.04. The 2 is the tenths digit and the 5 is the thousandths digit."),
    dict(stem="The diagram shows angles meeting on a straight line. What is the size of angle x?",
         fig=angles_on_line([42, 66]),
         options=O(("A", "72°"), ("B", "108°"), ("C", "138°"), ("D", "62°")),
         correct="A", strand="Measurement & Geometry", concept="Y5 Geometry · angles on a straight line sum to 180",
         explanation="42 + 66 = 108, and 180 − 108 = 72°. Choosing 108° means the two known angles were added but never subtracted from 180; 138° ignores the 66° angle."),
    dict(stem="Which of these numbers is the LARGEST?\n\n0.6, 5/8, 0.55, 1/2",
         options=O(("A", "0.6"), ("B", "5/8"), ("C", "0.55"), ("D", "1/2")),
         correct="B", strand="Fractions & Decimals", concept="Y6 Fractions · comparing fractions and decimals",
         explanation="Turn them all into decimals: 5/8 = 0.625, which is more than 0.6, 0.55 and 0.5. Choosing 0.6 means 5/8 was not converted."),
    dict(stem="The diagram shows a grid of equal squares. What fraction of the grid is shaded, in its simplest form?",
         fig=fraction_grid(2, 6, 8),
         options=O(("A", "1/3"), ("B", "3/4"), ("C", "5/6"), ("D", "2/3")),
         correct="D", strand="Fractions & Decimals", concept="Y6 Fractions · fraction of a diagram, simplifying 8/12",
         explanation="8 of the 12 squares are shaded: 8/12 = 2/3. Choosing 1/3 gives the UNSHADED fraction, and 3/4 miscounts the shaded squares as 9."),
    # story form
    dict(stem="Each pupil in Year 5 voted once for a favourite sport. The bar chart shows the votes. How many pupils voted altogether?",
         fig=bar_chart(["Football", "Swimming", "Tennis", "Athletics"], [35, 20, 25, 40], 45, 5, unit="votes"),
         options=O(("A", "80"), ("B", "115"), ("C", "125"), ("D", "120")),
         correct="D", strand="Problem Solving", concept="Y6 Statistics · reading a bar chart, then totalling all bars",
         explanation="Read the bars: 35 + 20 + 25 + 40 = 120 pupils. Choosing 80 leaves out the athletics bar, and 115 misreads football as 30."),
    dict(stem="The diagram shows a rectangular garden. A fence is to be built all the way round it. How many metres of fencing are needed?",
         fig=labelled_shape_fig(lambda out: out.extend([
             '<rect x="50" y="28" width="216" height="90" fill="#eef2f8" stroke="#1c2733" stroke-width="2.5"/>',
             svg_text(158, 18, "12 m"),
             svg_text(38, 78, "5 m", anchor="end")]), 310, 150),
         options=O(("A", "60 m"), ("B", "34 m"), ("C", "17 m"), ("D", "24 m")),
         correct="B", strand="Measurement & Geometry", concept="Y5 Measurement · perimeter of a rectangle",
         explanation="Perimeter = 12 + 5 + 12 + 5 = 34 m. Choosing 60 m gives the AREA (12 × 5), 17 m adds only one length and one width, and 24 m doubles the length only."),
    dict(stem="At the swimming gala, the first heat starts at 10:20 am, and each heat lasts 8 minutes, one straight after another. Ella swims in the FOURTH heat. At what time does her heat start?",
         options=O(("A", "10:52 am"), ("B", "10:28 am"), ("C", "10:44 am"), ("D", "10:36 am")),
         correct="C", strand="Measurement & Geometry", concept="Y6 Measurement · elapsed time with counting the right number of steps",
         explanation="Three full heats run before Ella's: 3 × 8 = 24 minutes, and 10:20 + 24 min = 10:44 am. Choosing 10:52 counts FOUR heats before hers, and 10:36 counts only two."),
    dict(stem="Cinema tickets cost HK$65 for an adult and HK$40 for a child. A family of 2 adults and 3 children pays with HK$300. How much change do they receive?",
         options=O(("A", "HK$50"), ("B", "HK$250"), ("C", "HK$90"), ("D", "HK$130")),
         correct="A", strand="Problem Solving", concept="Y5 Money · multi-step cost then change",
         explanation="2 × HK$65 = HK$130 and 3 × HK$40 = HK$120, so the total is HK$250 and the change is HK$300 − HK$250 = HK$50. HK$250 is the cost, not the change; HK$90 counts only two children; HK$130 is the adults' cost alone."),
    dict(stem="265 pupils are travelling to sports day by coach. Each coach seats 42 pupils. How many coaches does the school need?",
         options=O(("A", "6"), ("B", "5"), ("C", "7"), ("D", "8")),
         correct="C", strand="Problem Solving", concept="Y6 Number · division with remainder, rounding UP in context",
         explanation="265 ÷ 42 = 6 remainder 13, so 6 coaches are not enough: 13 pupils would be left behind. The school needs 7 coaches. Choosing 6 ignores the remainder."),
    dict(stem="A camera costs HK$430. Anna has already saved HK$180, and from now on she saves HK$25 each week. How many MORE weeks will it take her to afford the camera?",
         options=O(("A", "18"), ("B", "10"), ("C", "8"), ("D", "11")),
         correct="B", strand="Problem Solving", concept="Y6 Number · multi-step word problem (subtract, then divide)",
         explanation="She still needs 430 − 180 = HK$250, and 250 ÷ 25 = 10 weeks. Choosing 18 divides the FULL price by 25 (rounding up), forgetting the HK$180 already saved."),
]

# ---- Reading Comprehension (10) --------------------------------------------
PASSAGE_1 = (
    "<strong>Grandpa's Telescope</strong><br><br>"
    "When Maya's family moved to the village house where Grandpa lived, the thing she liked best stood under a "
    "dust sheet on the roof: a long brass telescope on a wooden tripod.<br><br>"
    "“Tonight we will look at Saturn,” Grandpa promised on her first evening. But when darkness fell, clouds "
    "rolled in from the sea and covered every star. The same thing happened the next night, and the night after "
    "that. “This is pointless,” Maya muttered, stamping back downstairs.<br><br>"
    "Grandpa did not argue. Instead, he showed her a battered notebook, its pages filled with dates and small "
    "sketches. “Every clear night I have ever had,” he said, “and every cloudy one too. Some of the best things "
    "in the sky made me wait for weeks. Waiting is part of looking.”<br><br>"
    "After that, Maya climbed to the roof with him anyway. On cloudy nights, Grandpa taught her the names of "
    "the constellations they would see one day, and how to line up the finder scope on a distant lamp post.<br><br>"
    "On the twelfth night, the clouds finally drew back like curtains. Grandpa aimed the telescope, made one "
    "tiny adjustment, and stepped aside without a word. Maya pressed her eye to the lens. Hanging in the "
    "darkness was a small golden globe, wrapped in perfect, impossible rings.<br><br>"
    "She did not shout. She simply watched, and understood why an old man would keep a notebook full of cloudy "
    "nights, and wait his whole life for skies like this."
)

PASSAGE_2 = (
    "<strong>The Hidden Network of the Forest</strong><br><br>"
    "Walk through a forest and the trees seem to stand alone, each one silent and separate. Underground, "
    "however, something surprising is going on. The roots of neighbouring trees are joined by threads of "
    "fungus so fine that a single pinch of soil can hold several kilometres of them.<br><br>"
    "The fungus and the trees trade with each other. The fungal threads gather water and minerals from the "
    "soil and pass them to the tree roots; in return, the trees send down sugar, which they make in their "
    "leaves using sunlight. As much as a quarter of a tree's sugar may go to feed its fungal partners.<br><br>"
    "The network does more than trade. Through it, a large old tree, sometimes called a mother tree, can pass "
    "sugar to young seedlings growing in deep shade, where there is too little light for them to make enough "
    "food of their own. Trees can even send signals through the network: when insects attack one tree, its "
    "neighbours may receive a chemical warning and begin making bitter substances in their leaves before a "
    "single insect has reached them.<br><br>"
    "Researchers who study forests now argue that a wood is less like a crowd of separate plants and more "
    "like a single community, sharing food and information underground. Protecting a forest, they say, means "
    "protecting not only the trees we can see, but also the hidden network beneath them."
)

_RC = "Y5-6 Reading · "
READING = [
    dict(passage=PASSAGE_1, stem="How did Maya feel during the first cloudy nights?",
         options=O(("A", "Afraid of the dark roof"), ("B", "Proud of Grandpa's telescope"),
                   ("C", "Impatient and frustrated"), ("D", "Too tired to care")),
         correct="C", strand="Reading: Fiction", concept=_RC + "character feelings at the start",
         explanation="She muttered 'this is pointless' and stamped downstairs: signs of impatience and frustration, not fear."),
    dict(passage=PASSAGE_1, stem="The writer says “the clouds finally drew back like curtains”. What does this suggest?",
         options=O(("A", "The sky slowly opened up, like a stage being revealed before a show"),
                   ("B", "Somebody closed the windows of the house"),
                   ("C", "The clouds were made of cloth"),
                   ("D", "It was about to start raining")),
         correct="A", strand="Reading: Fiction", concept=_RC + "interpreting figurative wording",
         explanation="Comparing the clouds to curtains being drawn back suggests the sky opened like a stage revealing a show: something special was about to appear."),
    dict(passage=PASSAGE_1, stem="What does Grandpa's notebook tell us about him?",
         options=O(("A", "He is forgetful and needs to write everything down"), ("B", "He prefers drawing to stargazing"),
                   ("C", "He is planning to sell the telescope"), ("D", "He is patient and has watched the sky for many years")),
         correct="D", strand="Reading: Fiction", concept=_RC + "inference about character",
         explanation="Recording every clear night AND every cloudy one, over years of waiting, shows his patience and long devotion to the sky."),
    dict(passage=PASSAGE_1, stem="What did Maya finally see through the telescope?",
         options=O(("A", "The Moon"), ("B", "A golden planet with rings"),
                   ("C", "A comet with a long tail"), ("D", "A distant lamp post")),
         correct="B", strand="Reading: Fiction", concept=_RC + "locating a stated detail",
         explanation="She saw a small golden globe wrapped in rings: Saturn, the planet Grandpa had promised. The lamp post was only for practising with the finder scope."),
    dict(passage=PASSAGE_1, stem="What lesson does the story teach us?",
         options=O(("A", "The most wonderful things are worth waiting for"), ("B", "Old telescopes work better than new ones"),
                   ("C", "Children should not stay up late"), ("D", "Cloudy nights are a waste of time")),
         correct="A", strand="Reading: Fiction", concept=_RC + "main message and character change",
         explanation="Maya finally understands why Grandpa waited his whole life: the story's message is that wonderful things are worth waiting for."),
    dict(passage=PASSAGE_2, stem="Why did the writer most likely write this passage?",
         options=O(("A", "To persuade readers to plant more trees"),
                   ("B", "To describe the life cycle of a fungus"),
                   ("C", "To explain how to find your way in a forest"),
                   ("D", "To explain how trees are connected and share things underground")),
         correct="D", strand="Reading: Non-fiction", concept=_RC + "identifying the main purpose",
         explanation="Every paragraph explains the underground network and what trees share through it; the fungus's own life cycle is never described."),
    dict(passage=PASSAGE_2, stem="What do the fungal threads pass to the tree roots?",
         options=O(("A", "Sugar and sunlight"), ("B", "Water and minerals"),
                   ("C", "Bitter substances"), ("D", "Seeds and leaves")),
         correct="B", strand="Reading: Non-fiction", concept=_RC + "locating a stated detail",
         explanation="The fungal threads gather water and minerals from the soil for the trees; SUGAR travels the other way, from the trees to the fungus."),
    dict(passage=PASSAGE_2, stem="In the last paragraph, the word “argue” is closest in meaning to:",
         options=O(("A", "quarrel angrily"), ("B", "doubt strongly"),
                   ("C", "put forward the idea"), ("D", "prove completely")),
         correct="C", strand="Reading: Non-fiction", concept=_RC + "vocabulary in context",
         explanation="Researchers 'argue that a wood is like a community': here 'argue' means to put forward an idea with reasons, not to quarrel."),
    dict(passage=PASSAGE_2, stem="According to the passage, how can a warning travel from one tree to another?",
         options=O(("A", "As a chemical signal through the underground network"),
                   ("B", "Through the wind shaking the branches"),
                   ("C", "By insects carrying messages"),
                   ("D", "Through birds calling in the canopy")),
         correct="A", strand="Reading: Non-fiction", concept=_RC + "understanding an explained fact",
         explanation="When insects attack one tree, a chemical warning can pass through the underground network, and neighbours start making bitter substances."),
    dict(passage=PASSAGE_2, stem="Which of these statements is NOT true, according to the passage?",
         options=O(("A", "A pinch of soil can hold several kilometres of fungal threads"),
                   ("B", "Trees send sugar down to the fungus"),
                   ("C", "Mother trees can pass sugar to shaded seedlings"),
                   ("D", "The fungus makes sugar for the trees")),
         correct="D", strand="Reading: Non-fiction", concept=_RC + "checking statements against the text",
         explanation="The TREES make the sugar in their leaves using sunlight; the fungus supplies water and minerals. The other three statements are all in the text."),
]

# ---- Listening (3 recordings, 10 Q) ----------------------------------------
_LI = "Listen to the recording, then choose the best answer."
_A1, _A2, _A3 = "listening1.m4a", "listening2.m4a", "listening3.m4a"

AUDIO_TITLES = {
    "listening1.m4a": "News from School",
    "listening2.m4a": "An Announcement",
    "listening3.m4a": "A Phone Message",
    "listening-zh.m4a": "學校通告 School Notice",
}

AUDIO = {
    "listening-zh.m4a": [("zh-CN-YunxiNeural", "-10%", "各位同学请注意。学校普通话朗诵比赛将在下星期二下午两点举行，地点由音乐室改为礼堂。想参加的同学，请在这个星期四放学之前，到教员室找王老师报名。比赛当天请穿整齐校服，并且带上学生证。谢谢大家。")],
    _A1: [
        ("en-GB-RyanNeural", "-8%", "Katie, have you heard? The bake sale has changed."),
        ("en-GB-MaisieNeural", "-8%", "Changed? It's on Friday in the playground, isn't it?"),
        ("en-GB-RyanNeural", "-8%", "Not any more. The forecast says heavy rain on Friday, so it will be on "
                        "Thursday instead, and it's moving inside, to the school hall."),
        ("en-GB-MaisieNeural", "-8%", "So where do our cakes go?"),
        ("en-GB-RyanNeural", "-8%", "Take them to the staff room before half past eight on Thursday morning. "
                        "Miss Lee will keep them safe until lunchtime."),
        ("en-GB-MaisieNeural", "-8%", "That's actually good news for me. I'm at the dentist on Friday afternoon; "
                          "I thought I was going to miss the whole thing."),
        ("en-GB-RyanNeural", "-8%", "Perfect. Just don't eat your own cakes before Thursday."),
    ],
    _A2: [("en-GB-SoniaNeural", "-8%",
        "Good morning, everyone. Here is a reminder about school photo day, which is next Tuesday. "
        "All pupils should wear full winter uniform, including their tie. "
        "Even if your class has PE that day, do not come in PE kit; bring it in your bag and change afterwards. "
        "This year the photographers will set up in the library, not in the hall as before, "
        "and classes will be called down one at a time. "
        "Finally, please hand your completed order form to your class teacher by Friday this week.")],
    _A3: [("en-US-AvaNeural", "-8%",
        "Hello, this is Miss Wong, the art teacher, with a message about the painting competition. "
        "The theme this year is My Hong Kong, so paint a place or a moment in the city that matters to you. "
        "Use the large white paper I gave out in class, and write your name and class on the back of your "
        "painting, not the front, so that the judges cannot see it. "
        "Paintings must reach the art room by Friday lunchtime; the winners will be announced at "
        "Monday's assembly. Good luck, everyone.")],
}

LISTENING = [
    dict(stem=_LI + "\n\nWhy has the bake sale been moved to Thursday?", audio=_A1,
         options=O(("A", "The hall is booked on Friday"), ("B", "Heavy rain is forecast for Friday"),
                   ("C", "The head teacher is away"), ("D", "Not enough cakes were ready")),
         correct="B", strand="Listening", concept="Y5 Listening · stated reason",
         explanation="The forecast says heavy rain on Friday, so the sale moves to Thursday and goes indoors."),
    dict(stem=_LI + "\n\nWhere will the bake sale be held now?", audio=_A1,
         options=O(("A", "In the playground"), ("B", "In the canteen"), ("C", "At the school gate"), ("D", "In the school hall")),
         correct="D", strand="Listening", concept="Y5 Listening · key detail (new place); the playground is the OLD place trap",
         explanation="It was going to be in the playground, but it is moving inside, to the school hall."),
    dict(stem=_LI + "\n\nWhere should pupils take their cakes on Thursday morning?", audio=_A1,
         options=O(("A", "To the staff room, before half past eight"), ("B", "Straight to the hall"),
                   ("C", "To their classroom"), ("D", "To the playground")),
         correct="A", strand="Listening", concept="Y5 Listening · instruction with time and place details",
         explanation="Cakes go to the staff room before half past eight, where Miss Lee keeps them until lunchtime."),
    dict(stem=_LI + "\n\nWhy is Katie pleased that the date has changed?", audio=_A1,
         options=O(("A", "She prefers baking on Wednesdays"), ("B", "She wants it to rain"),
                   ("C", "She is at the dentist on Friday, so now she will not miss the sale"), ("D", "She needs more time to bake")),
         correct="C", strand="Listening", concept="Y6 Listening · inference (dentist on Friday, sale now Thursday)",
         explanation="Katie is at the dentist on Friday afternoon; with the sale on Thursday, she no longer misses it."),
    dict(stem=_LI + "\n\nWhen is school photo day?", audio=_A2,
         options=O(("A", "Next Tuesday"), ("B", "Next Thursday"), ("C", "Tomorrow"), ("D", "Next Monday")),
         correct="A", strand="Listening", concept="Y5 Listening · key detail (date)",
         explanation="The announcement says photo day is next Tuesday."),
    dict(stem=_LI + "\n\nWhat should pupils wear on photo day?", audio=_A2,
         options=O(("A", "PE kit"), ("B", "Their house T-shirt"), ("C", "Full winter uniform"), ("D", "Their own clothes")),
         correct="C", strand="Listening", concept="Y5 Listening · requirement with a denial trap (NOT PE kit, even on a PE day)",
         explanation="Everyone wears full winter uniform with a tie; PE kit goes in the bag for changing afterwards."),
    dict(stem=_LI + "\n\nWhere will the photos be taken this year?", audio=_A2,
         options=O(("A", "In the hall, as usual"), ("B", "In each classroom"), ("C", "On the playground"), ("D", "In the library")),
         correct="D", strand="Listening", concept="Y5 Listening · changed arrangement; the hall is the LAST YEAR trap",
         explanation="This year the photographers set up in the library, not in the hall as before."),
    dict(stem=_LI + "\n\nWhat is the theme of the painting competition?", audio=_A3,
         options=O(("A", "My School"), ("B", "My Hong Kong"), ("C", "My Family"), ("D", "The Four Seasons")),
         correct="B", strand="Listening", concept="Y5 Listening · key detail (theme)",
         explanation="The theme this year is My Hong Kong: a place or moment in the city that matters to you."),
    dict(stem=_LI + "\n\nBy when must paintings reach the art room?", audio=_A3,
         options=O(("A", "Monday's assembly"), ("B", "Next Wednesday"), ("C", "Friday after school"), ("D", "Friday lunchtime")),
         correct="D", strand="Listening", concept="Y5 Listening · deadline; Monday is the WINNERS announcement trap",
         explanation="Paintings must reach the art room by Friday lunchtime; Monday's assembly is when the winners are announced."),
    dict(stem=_LI + "\n\nWhere should pupils write their name and class?", audio=_A3,
         options=O(("A", "On the back of the painting"), ("B", "On the front, at the bottom"),
                   ("C", "On a separate card"), ("D", "On the envelope")),
         correct="A", strand="Listening", concept="Y5 Listening · instruction with a denial trap (not the front)",
         explanation="Names go on the BACK of the painting, not the front, so the judges cannot see them."),
]

# ---- Writing / Speaking / Chinese ------------------------------------------
CONTENT_WRITING = dict(
    type="writing",
    intro="Choose ONE of the two tasks below and type your answer in the box. Aim for about 80-130 words.",
    body=("Task 1: Describe a festival or celebration that you enjoy with your family. Describe what you see, "
          "hear and taste, and explain what makes it special for your family.\n\n"
          "Task 2: Some schools want to replace printed textbooks with tablets. Do you think this is a good "
          "idea? Give reasons and examples to support your opinion."),
    hint="Start by saying which task you chose. Plan briefly, write in clear paragraphs, and leave a minute to check your spelling and punctuation.",
    placeholder="Type your answer here; it will be saved for review…",
)

CONTENT_SPEAKING = dict(
    type="speaking",
    stem="Record a short spoken introduction of yourself (about 60-90 seconds).",
    body=("Speak about:\n"
          "• Your name, your age and your current school\n"
          "• A place you would love to visit one day, and why\n"
          "• A time you helped someone, and how it made you feel\n"
          "• One question you would like to ask the teachers at your new school\n\n"
          "Speak naturally; this is a chance for your future school to hear you, not a memory test."),
)

CH_PASSAGE_TRAD = (
    "今年春天，爸爸帶回幾棵番茄苗，讓我在陽台上種。起初我覺得很麻煩：每天放學要澆水、鬆土，星期天還要施肥。"
    "有一次我偷懶，兩天沒有澆水，葉子便垂了下來，我嚇得連忙補救。\n\n"
    "從那天起，我每天都認真照顧它們，還把觀察到的變化記在小本子上：先開出小黃花，然後結出綠色的小果子，"
    "最後果子慢慢變紅。\n\n"
    "摘下第一批番茄那天，我送了幾個給隔壁的陳婆婆。她笑着說：「自己種的，一定特別甜。」我點點頭。原來耐心付出以後，"
    "收穫的不只是果實，還有分享的快樂。"
)
CH_PASSAGE_SIMP = (
    "今年春天，爸爸带回几棵番茄苗，让我在阳台上种。起初我觉得很麻烦：每天放学要浇水、松土，星期天还要施肥。"
    "有一次我偷懒，两天没有浇水，叶子便垂了下来，我吓得连忙补救。\n\n"
    "从那天起，我每天都认真照顾它们，还把观察到的变化记在小本子上：先开出小黄花，然后结出绿色的小果子，"
    "最后果子慢慢变红。\n\n"
    "摘下第一批番茄那天，我送了几个给隔壁的陈婆婆。她笑着说：“自己种的，一定特别甜。”我点点头。原来耐心付出以后，"
    "收获的不只是果实，还有分享的快乐。"
)

def _ch(stem_t, stem_s, opts_ts, correct, concept, explanation):
    return dict(
        passage=zh_blocks(CH_PASSAGE_TRAD.replace("\n\n", "<br><br>"), CH_PASSAGE_SIMP.replace("\n\n", "<br><br>")),
        stem=bilingual(stem_t, stem_s),
        options=O(*[(k, bilingual(t, s)) for k, (t, s) in opts_ts.items()]),
        correct=correct, strand="中文閱讀理解", concept="小五中文 · " + concept, explanation=explanation)

CHINESE = [
    _ch("「我」為什麼開始在陽台上種番茄？", "“我”为什么开始在阳台上种番茄？",
        {"A": ("因為老師佈置的作業", "因为老师布置的作业"), "B": ("因為爸爸帶回番茄苗讓「我」種", "因为爸爸带回番茄苗让“我”种"),
         "C": ("因為「我」想吃番茄", "因为“我”想吃番茄"), "D": ("因為陳婆婆送來種子", "因为陈婆婆送来种子")},
        "B", "內容理解：起因", "文章開首說明：爸爸帶回幾棵番茄苗，讓「我」在陽台上種。"),
    _ch("「我」偷懶兩天沒澆水，番茄苗變得怎樣？", "“我”偷懒两天没浇水，番茄苗变得怎样？",
        {"A": ("開出了小黃花", "开出了小黄花"), "B": ("長得更高了", "长得更高了"),
         "C": ("果子變紅了", "果子变红了"), "D": ("葉子垂了下來", "叶子垂了下来")},
        "D", "內容理解：因果", "文中寫道：兩天沒有澆水，葉子便垂了下來，「我」嚇得連忙補救。"),
    _ch("文中「補救」的意思最接近：", "文中“补救”的意思最接近：",
        {"A": ("設法把出了問題的事糾正過來", "设法把出了问题的事纠正过来"), "B": ("把植物拔掉重新再種", "把植物拔掉重新再种"),
         "C": ("向別人道歉", "向别人道歉"), "D": ("放棄不再理會", "放弃不再理会")},
        "A", "詞語理解", "「補救」指在事情出問題後想辦法糾正。文中「我」連忙澆水照顧，正是糾正自己偷懶造成的問題。"),
    _ch("番茄生長的次序是：", "番茄生长的次序是：",
        {"A": ("先結果子，再開花，最後變紅", "先结果子，再开花，最后变红"),
         "B": ("先變紅，再開花，最後結果子", "先变红，再开花，最后结果子"),
         "C": ("先開黃花，再結綠果子，最後變紅", "先开黄花，再结绿果子，最后变红"),
         "D": ("一種下去就結出紅果子", "一种下去就结出红果子")},
        "C", "內容理解：細節排序", "小本子記下的變化是：先開出小黃花，然後結出綠色的小果子，最後果子慢慢變紅。"),
    _ch("陳婆婆說「自己種的，一定特別甜」，意思是：", "陈婆婆说“自己种的，一定特别甜”，意思是：",
        {"A": ("陽台種的番茄品種特別好", "阳台种的番茄品种特别好"), "B": ("番茄加了糖，所以特別甜", "番茄加了糖，所以特别甜"),
         "C": ("婆婆從來沒有吃過番茄", "婆婆从来没有吃过番茄"), "D": ("親手付出得來的成果特別珍貴", "亲手付出得来的成果特别珍贵")},
        "D", "內容理解：句意", "婆婆的話並不是說味道真的不同，而是指親手栽種、用心付出得來的成果，感覺特別珍貴。"),
    _ch("作者寫這個故事，主要想告訴我們：", "作者写这个故事，主要想告诉我们：",
        {"A": ("耐心付出才有收穫，分享令快樂加倍", "耐心付出才有收获，分享令快乐加倍"),
         "B": ("種番茄一定要天天施肥", "种番茄一定要天天施肥"),
         "C": ("種植物太麻煩，不值得做", "种植物太麻烦，不值得做"),
         "D": ("寫觀察日記比種植更重要", "写观察日记比种植更重要")},
        "A", "主旨理解", "文末點明：耐心付出以後，收穫的不只是果實，還有分享的快樂。"),
]

CH_LISTENING = [
    dict(stem=bilingual("聆聽錄音，然後回答問題。\n\n朗誦比賽在哪裡舉行？", "聆听录音，然后回答问题。\n\n朗诵比赛在哪里举行？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("音樂室", "音乐室")), ("B", bilingual("操場", "操场")), ("C", bilingual("課室", "课室")), ("D", bilingual("禮堂", "礼堂"))),
         correct="D", strand="中文聆聽理解", concept="小五中文 · 聆聽：地點（音樂室是原地點陷阱）",
         explanation="廣播說比賽地點由音樂室改為禮堂。"),
    dict(stem=bilingual("朗誦比賽什麼時候舉行？", "朗诵比赛什么时候举行？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("下星期二下午兩點", "下星期二下午两点")), ("B", bilingual("這個星期四放學後", "这个星期四放学后")), ("C", bilingual("下星期二上午", "下星期二上午")), ("D", bilingual("下星期四下午", "下星期四下午"))),
         correct="A", strand="中文聆聽理解", concept="小五中文 · 聆聽：時間（星期四是報名截止陷阱）",
         explanation="比賽在下星期二下午兩點舉行；這個星期四是報名的截止時間。"),
    dict(stem=bilingual("想參加比賽的同學要怎樣報名？", "想参加比赛的同学要怎样报名？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("到禮堂找班主任", "到礼堂找班主任")), ("B", bilingual("在網上填寫表格", "在网上填写表格")), ("C", bilingual("星期四放學前到教員室找王老師", "星期四放学前到教员室找王老师")), ("D", bilingual("請家長打電話到學校", "请家长打电话到学校"))),
         correct="C", strand="中文聆聽理解", concept="小五中文 · 聆聽：報名方法",
         explanation="廣播說想參加的同學，要在星期四放學之前到教員室找王老師報名。"),
    dict(stem=bilingual("比賽當天，同學要帶什麼？", "比赛当天，同学要带什么？"), audio="listening-zh.m4a",
         options=O(("A", bilingual("課本", "课本")), ("B", bilingual("學生證", "学生证")), ("C", bilingual("水壺", "水壶")), ("D", bilingual("樂器", "乐器"))),
         correct="B", strand="中文聆聽理解", concept="小五中文 · 聆聽：要求物品",
         explanation="廣播提醒比賽當天要穿整齊校服，並且帶上學生證。"),
]

CH_SPEAKING = dict(
    type="speaking", maxSeconds=120,
    stem=bilingual("請用普通話介紹一下你自己（大約60至90秒）。", "请用普通话介绍一下你自己（大约60至90秒）。"),
    body=zh_blocks("可以說一說：\n• 你的名字、年級和學校\n• 你最喜歡的一本書或一個故事\n• 你週末通常做什麼\n• 你今年最想達成的一個小目標",
                   "可以说一说：\n• 你的名字、年级和学校\n• 你最喜欢的一本书或一个故事\n• 你周末通常做什么\n• 你今年最想达成的一个小目标"),
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
