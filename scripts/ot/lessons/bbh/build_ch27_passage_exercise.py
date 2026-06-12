"""Build BBH Chapter 27 — "Spot the Hiphil" Passage Exercise.

Generates all three output formats:
  data/lessons/bbh/ch27/exercises/ch27-passage-exercise/ch27-passage-exercise.md
  data/lessons/bbh/ch27/exercises/ch27-passage-exercise/ch27-passage-exercise.html
  data/lessons/bbh/ch27/exercises/ch27-passage-exercise/ch27-passage-exercise.pdf

Usage:
    python3 scripts/ot/lessons/bbh/build_ch27_passage_exercise.py

All 21 verb forms are verified against TAHOT. No adapted or fabricated
references — every form appears verbatim in the cited verse.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, '.')
from src.bible_grammar.exercise_pdf.bbh import build_ch27_exercise  # noqa: E402

OUT_DIR = Path(
    'data/lessons/bbh/ch27/exercises/ch27-passage-exercise'
)
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Item data ─────────────────────────────────────────────────────────────────
# Each tuple: (num, form, ref, hebrew_context, kjv_context,
#              hiphil, conjugation, pgn, root, weak_class, gloss)

ITEMS_A = [
    ('1',  'הֶחֱטִיא',      '1 Kgs 14:16',
     'יַחֲטִיא אֶת־יִשְׂרָאֵל וַאֲשֶׁר **הֶחֱטִיא**',
     '"because of his sins by which he caused Israel to sin"',
     'Yes', 'Perfect', '3ms', 'חָטָא', 'III-א',
     'he caused to sin'),

    ('2',  'וַהֲקִמֹתִי',   'Gen 6:18',
     'וַ**הֲקִמֹתִי** אֶת־בְּרִיתִי אִתְּךָ',
     '"but I will establish my covenant with you"',
     'Yes', 'Weqatal', '1cs', 'קוּם', 'Biconsonantal',
     'I will establish'),

    ('3',  'הֶעֱלָה',        '1 Sam 12:6',
     'יְהוָה אֲשֶׁר **הֶעֱלָה** אֶת־מֹשֶׁה וְאֶת־אַהֲרֹן',
     '"the LORD who brought up Moses and Aaron"',
     'Yes', 'Perfect', '3ms', 'עָלָה', 'III-ה + I-guttural',
     'he brought up'),

    ('4',  'הוֹצֵאתִיךָ',   'Gen 15:7',
     'אֲנִי יְהוָה אֲשֶׁר **הוֹצֵאתִיךָ** מֵאוּר כַּשְׂדִּים',
     '"I am the LORD who brought you out of Ur of the Chaldeans"',
     'Yes', 'Perfect', '1cs + 2ms suffix', 'יָצָא', 'I-י',
     'I brought you out'),

    ('5',  'וַיַּעַל',       'Gen 8:20',
     'וַיִּבֶן נֹחַ מִזְבֵּחַ לַיהוָה … **וַיַּעַל** עֹלֹת עַל הַמִּזְבֵּחַ',
     '"And Noah … offered burnt offerings on the altar"',
     'Yes', 'Wayyiqtol', '3ms', 'עָלָה', 'III-ה (apocopated)',
     'he offered up'),

    ('6',  'וַיַּפֵּל',      'Gen 2:21',
     'וַ**יַּפֵּל** יְהוָה אֱלֹהִים תַּרְדֵּמָה עַל הָאָדָם',
     '"the LORD God caused a deep sleep to fall upon the man"',
     'Yes', 'Wayyiqtol', '3ms', 'נָפַל', 'I-נ',
     'he caused to fall'),

    ('7',  'הֶעֱמַדְתִּיךָ', 'Exo 9:16',
     'בַּעֲבוּר זֹאת **הֶעֱמַדְתִּיךָ** לְהַרְאֹתְךָ אֶת־כֹּחִי',
     '"for this purpose I have raised you up, to show you my power"',
     'Yes', 'Perfect', '1cs + 2ms suffix', 'עָמַד', 'I-guttural',
     'I raised you up / stationed you'),

    ('8',  'הוֹצֵאתִיךָ',   'Exo 20:2',
     'אָנֹכִי יְהוָה אֱלֹהֶיךָ אֲשֶׁר **הוֹצֵאתִיךָ** מֵאֶרֶץ מִצְרַיִם',
     '"I am the LORD your God, who brought you out of the land of Egypt"',
     'Yes', 'Perfect', '1cs + 2ms suffix', 'יָצָא', 'I-י',
     'I brought you out'),

    ('9',  'הַרְאֵנִי',      'Exo 33:18',
     'וַיֹּאמַר **הַרְאֵנִי** נָא אֶת־כְּבֹדֶךָ',
     '"And he said, Show me your glory, please"',
     'Yes', 'Imperative', '2ms + 1cs suffix', 'רָאָה', 'III-ה',
     'show me'),

    ('10', 'הָקֵם',          '2 Sam 7:25',
     '**הָקֵם** עַד עוֹלָם אֶת הַדָּבָר אֲשֶׁר דִּבַּרְתָּ',
     '"Confirm forever the word that you have spoken"',
     'Yes', 'Imperative', '2ms', 'קוּם', 'Biconsonantal',
     'confirm / establish'),
]

ITEMS_B = [
    ('11', 'הַעֲמֵד',        'Isa 21:6',
     '**הַעֲמֵד** הַמְּצַפֶּה אֲשֶׁר יִרְאֶה יַגִּיד',
     '"Go, set a watchman; let him declare what he sees"',
     'Yes', 'Imperative', '2ms', 'עָמַד', 'I-guttural',
     'post / station a watchman'),

    ('12', 'יָקִים',         'Deu 18:15',
     'נָבִיא מִקִּרְבְּךָ **יָקִים** לְךָ יְהוָה אֱלֹהֶיךָ',
     '"A prophet … the LORD your God will raise up for you"',
     'Yes', 'Imperfect', '3ms', 'קוּם', 'Biconsonantal',
     'he will raise up'),

    ('13', 'הַשְׁמִיעוּ',    'Isa 48:20',
     '**הַשְׁמִיעוּ** זֹאת הַגִּידוּהָ עַד קְצֵה הָאָרֶץ',
     '"Declare this, announce it to the ends of the earth"',
     'Yes', 'Imperative', '2mp', 'שָׁמַע', 'III-ח/ע',
     'cause this to be heard'),

    ('14', 'הוֹצִיאֲךָ',    'Deu 16:1',
     'כִּי בְּחֹדֶשׁ הָאָבִיב **הוֹצִיאֲךָ** יְהוָה אֱלֹהֶיךָ מִמִּצְרַיִם',
     '"for in the month of Abib the LORD your God brought you out of Egypt"',
     'Yes', 'Perfect', '3ms + 2ms suffix', 'יָצָא', 'I-י',
     'he brought you out'),

    ('15', 'הַמּוֹצִיאֲךָ',  'Deu 8:14',
     'הַ**מּוֹצִיאֲךָ** מֵאֶרֶץ מִצְרַיִם מִבֵּית עֲבָדִים',
     '"the one who brought you out of the land of Egypt, out of the house of slavery"',
     'Yes', 'Participle', 'ms + article + 2ms suffix', 'יָצָא', 'I-י',
     'the one who brought you out (substantival ptc)'),

    ('16', 'וְהֵקִים',       'Num 30:14',
     'אִם הַחֲרֵשׁ יַחֲרִישׁ לָהּ … **וְהֵקִים** אֶת כָּל נְדָרֶיהָ',
     '"if her husband says nothing … he thereby confirms all her vows"',
     'Yes', 'Weqatal', '3ms', 'קוּם', 'Biconsonantal',
     'he confirms / establishes'),

    ('17', 'לְהַעֲלוֹת',    '1 Sam 10:8',
     'וְאַחַר כֵּן תָּבוֹא אֵלַי **לְהַעֲלוֹת** עֹלָה',
     '"after that you will come to me to offer up a burnt offering"',
     'Yes', 'Inf. Construct', '—', 'עָלָה', 'III-ה + I-guttural',
     'to offer up'),

    ('18', 'אַשְׁמִיע',      'Isa 42:9',
     'חֲדָשׁוֹת אֲנִי מַגִּיד … **אַשְׁמִיע** אֶתְכֶם',
     '"new things I declare … before they arise I announce them to you"',
     'Yes', 'Imperfect', '1cs', 'שָׁמַע', 'III-ח/ע',
     'I cause to hear / announce'),
]

ITEMS_C = [
    ('19', 'וַיֵּלֶךְ',      'Gen 22:3',
     'וַיַּשְׁכֵּם אַבְרָהָם בַּבֹּקֶר **וַיֵּלֶךְ** אֶל הַמָּקוֹם',
     '"And Abraham rose early and went to the place"',
     'No', 'Wayyiqtol', '3ms', 'הָלַךְ', 'I-ה (Qal)',
     'NOT Hiphil — Qal: and he went; no הִ/הַ prefix'),

    ('20', 'נוֹלַד',         'Gen 21:3',
     'אֶת שֶׁם בְּנוֹ אֲשֶׁר **נוֹלַד** לוֹ',
     '"the name of his son who was born to him"',
     'No', 'Perfect', '3ms', 'יָלַד', 'I-י (Niphal)',
     'NOT Hiphil — Niphal passive: was born; נוֹ- = Niphal I-י'),

    ('21', 'תָּמוּת',        'Gen 2:17',
     'כִּי בְּיוֹם אֲכָלְךָ מִמֶּנּוּ מוֹת **תָּמוּת**',
     '"for in the day you eat of it you shall surely die"',
     'No', 'Imperfect', '2ms', 'מוּת', 'Biconsonantal (Qal)',
     'NOT Hiphil — Qal: you will die; תָּ- = Qal 2ms; no הַ- prefix'),
]

ALL_ITEMS = ITEMS_A + ITEMS_B + ITEMS_C


# ── Markdown ──────────────────────────────────────────────────────────────────

def _item_md(num, form, ref, heb, kjv, is_hiphil,
             conj, pgn, root, wclass, gloss,
             show_answers: bool) -> str:
    lines = [
        f'**{num}.** {heb}',
        f'*({ref})* — {kjv}',
        '',
        '| Hiphil? | Conjugation | PGN | Root | Weak class | Causative gloss |',
        '|---|---|---|---|---|---|',
    ]
    if show_answers:
        lines.append(
            f'| {is_hiphil} | {conj} | {pgn} | {root} | {wclass} | {gloss} |'
        )
    else:
        lines.append('| | | | | | |')
    lines.append('')
    return '\n'.join(lines)


def build_md() -> Path:
    out = OUT_DIR / 'ch27-passage-exercise.md'

    answer_rows = []
    for num, form, ref, heb, kjv, h, c, pgn, root, wclass, gloss in ALL_ITEMS:
        answer_rows.append(
            f'| {num} | {form} | {h} | {c} | {pgn} | {root} | {wclass} | {gloss} |'
        )

    lines = [
        '# "Spot the Hiphil" — Passage Exercise',
        '',
        '*BBH Chapter 27 · Hiphil Weak Verbs*',
        '',
        '---',
        '',
        '## Instructions',
        '',
        'Parts A and B contain Hiphil weak verbs. For each:',
        '',
        '1. **Hiphil?** — Yes or No',
        '2. **Conjugation** — Perfect / Imperfect / Wayyiqtol / Weqatal / Imperative / '
        'Inf. Construct / Inf. Absolute / Participle',
        '3. **PGN** — Person-Gender-Number (e.g., 3ms, 2mp, 1cs)',
        '4. **Root** — three-letter root (lexical form)',
        '5. **Weak class** — I-guttural / III-ח/ע / III-א / III-ה / I-נ / I-י / Biconsonantal',
        '6. **Causative gloss** — brief English rendering of the Hiphil meaning in context',
        '',
        '**Part C** contains three distractor verbs. These are **not** Hiphil.'
        ' Answer "No" and complete the full parse.',
        '',
        '---',
        '',
        '## Part A — Kings, Genesis, Samuel, and Exodus (items 1–10)',
        '',
    ]

    for item in ITEMS_A:
        lines.append(_item_md(*item, show_answers=False))
        lines.append('---')
        lines.append('')

    lines += [
        '## Part B — Numbers, Deuteronomy, Isaiah, and Samuel (items 11–18)',
        '',
    ]
    for item in ITEMS_B:
        lines.append(_item_md(*item, show_answers=False))
        lines.append('---')
        lines.append('')

    lines += [
        '## Part C — Distractor Check',
        '',
        'These three verbs are **not** Hiphil. Answer "No" and complete the full parse.',
        '',
    ]
    for item in ITEMS_C:
        lines.append(_item_md(*item, show_answers=False))
        lines.append('---')
        lines.append('')

    lines += [
        '## Answer Key',
        '',
        '| # | Form | Hiphil? | Conjugation | PGN | Root | Weak class | Gloss |',
        '|---|---|---|---|---|---|---|---|',
    ] + answer_rows + ['']

    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  Saved {out}')
    return out


# ── HTML ──────────────────────────────────────────────────────────────────────

def _item_html(num: str, form: str, ref: str, heb: str, kjv: str,
               is_hiphil: str, conj: str, pgn: str, root: str,
               wclass: str, gloss: str) -> str:
    ans_html = (
        f'<tr class="answer-row" id="ans-{num}" style="display:none;background:#e8f5e9;">'
        f'<td><strong>{is_hiphil}</strong></td>'
        f'<td>{conj}</td>'
        f'<td>{pgn}</td>'
        f'<td style="direction:rtl;unicode-bidi:embed;">{root}</td>'
        f'<td>{wclass}</td>'
        f'<td>{gloss}</td>'
        f'</tr>'
    )
    return f'''
<div class="item" id="item-{num}">
  <p><strong>{num}.</strong> <span style="font-size:1.2em;direction:rtl;unicode-bidi:embed;">{heb}</span></p>
  <p><span class="ref">{ref}</span> — {kjv}</p>
  <table class="parse-table">
    <thead>
      <tr>
        <th>Hiphil?</th>
        <th>Conjugation</th>
        <th>PGN</th>
        <th>Root</th>
        <th>Weak class</th>
        <th>Causative gloss</th>
      </tr>
    </thead>
    <tbody>
      <tr class="input-row">
        <td><select class="hiphil-select"><option value=""></option><option value="Yes">Yes</option><option value="No">No</option></select></td>  # noqa: E501
        <td><select class="parse-field"><option value=""></option><option value="Perfect">Perfect</option><option value="Imperfect">Imperfect</option><option value="Wayyiqtol">Wayyiqtol</option><option value="Weqatal">Weqatal</option><option value="Imperative">Imperative</option><option value="Inf. Construct">Inf. Construct</option><option value="Participle">Participle</option></select></td>  # noqa: E501
        <td><select class="parse-field"><option value=""></option><option value="3ms">3ms</option><option value="3ms + 2ms suffix">3ms + 2ms suffix</option><option value="2ms">2ms</option><option value="2ms + 1cs suffix">2ms + 1cs suffix</option><option value="2mp">2mp</option><option value="1cs">1cs</option><option value="1cs + 2ms suffix">1cs + 2ms suffix</option><option value="ms + article + 2ms suffix">ms + article + 2ms suffix</option><option value="ms">ms</option><option value="—">—</option></select></td>  # noqa: E501
        <td><input class="parse-field" type="text" style="direction:rtl;unicode-bidi:embed;"></td>
        <td><select class="parse-field"><option value=""></option><option value="I-guttural">I-guttural</option><option value="III-ח/ע">III-ח/ע</option><option value="III-א">III-א</option><option value="III-ה">III-ה</option><option value="III-ה + I-guttural">III-ה + I-guttural</option><option value="III-ה (apocopated)">III-ה (apocopated)</option><option value="I-נ">I-נ</option><option value="I-י">I-י</option><option value="Biconsonantal">Biconsonantal</option><option value="Biconsonantal (Qal)">Biconsonantal (Qal)</option><option value="I-ה (Qal)">I-ה (Qal)</option><option value="I-י (Niphal)">I-י (Niphal)</option></select></td>  # noqa: E501
        <td><input class="parse-field" type="text"></td>
      </tr>
      {ans_html}
    </tbody>
  </table>
  <button class="reveal-btn" onclick="toggleAnswer('{num}')">&#9654; Answer</button>
</div>
<hr>
'''


def build_html() -> Path:
    out = OUT_DIR / 'ch27-passage-exercise.html'

    items_a_html = ''.join(_item_html(*item) for item in ITEMS_A)
    items_b_html = ''.join(_item_html(*item) for item in ITEMS_B)
    items_c_html = ''.join(_item_html(*item) for item in ITEMS_C)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BBH Ch27 — Spot the Hiphil Passage Exercise</title>
<style>
  body {{ font-family: Georgia, serif; max-width: 860px; margin: 2rem auto; padding: 0 1rem; }}
  h1 {{ font-size: 1.4rem; }}
  h2 {{ font-size: 1.1rem; margin-top: 2rem; border-bottom: 1px solid #ccc; padding-bottom: 0.3rem; }}
  .ref {{ font-style: italic; color: #555; }}
  .item {{ margin: 1.5rem 0; }}
  .parse-table {{ width: 100%; border-collapse: collapse; margin: 0.5rem 0; table-layout: fixed; }}
  .parse-table th, .parse-table td {{ border: 1px solid #ccc; padding: 0.35rem 0.5rem;
    font-size: 0.9rem; vertical-align: middle; }}
  .parse-table th {{ background: #f0f0f0; font-weight: bold; white-space: nowrap; }}
  .parse-field {{ width: 100%; box-sizing: border-box; border: none; font-family: inherit;
    font-size: 0.9rem; background: #fafafa; padding: 2px; }}
  .parse-field:focus {{ outline: 1px solid #888; background: #fff; }}
  .hiphil-select {{ width: 100%; box-sizing: border-box; border: none; font-family: inherit;
    font-size: 0.9rem; background: #fafafa; padding: 2px; }}
  .reveal-btn {{ margin-top: 0.4rem; padding: 0.25rem 0.7rem; font-size: 0.85rem;
    cursor: pointer; border: 1px solid #999; background: #f5f5f5; border-radius: 3px; }}
  .reveal-btn:hover {{ background: #e0e0e0; }}
  .answer-row td {{ background: #e8f5e9 !important; }}
  .controls {{ margin: 1rem 0; display: flex; gap: 0.5rem; flex-wrap: wrap; }}
  .controls button {{ padding: 0.3rem 0.8rem; font-size: 0.85rem; cursor: pointer;
    border: 1px solid #999; background: #f5f5f5; border-radius: 3px; }}
  .controls button:hover {{ background: #e0e0e0; }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 1rem 0; }}
  @media print {{
    .reveal-btn, .controls {{ display: none; }}
    .parse-field {{ border-bottom: 1px solid #333; background: transparent; }}
    .hiphil-select {{ border-bottom: 1px solid #333; background: transparent; }}
    .answer-row {{ display: none !important; }}
  }}
</style>
</head>
<body>

<h1>"Spot the Hiphil" — Passage Exercise</h1>
<p><em>BBH Chapter 27 · Hiphil Weak Verbs</em></p>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<h2>Instructions</h2>
<p>Parts A and B contain Hiphil weak verbs. For each bold/highlighted form:</p>
<ol>
  <li><strong>Hiphil?</strong> — select Yes or No</li>
  <li><strong>Conjugation</strong> — Perfect / Imperfect / Wayyiqtol / Weqatal / Imperative / Inf. Construct / Participle</li>  # noqa: E501
  <li><strong>PGN</strong> — Person-Gender-Number (e.g., 3ms, 2mp, 1cs)</li>
  <li><strong>Root</strong> — three-letter lexical root</li>
  <li><strong>Weak class</strong> — I-guttural / III-ח/ע / III-א / III-ה / I-נ / I-י / Biconsonantal</li>
  <li><strong>Causative gloss</strong> — brief English rendering in context</li>
</ol>
<p><strong>Part C</strong> contains three distractor verbs. These are <strong>not</strong> Hiphil — select "No" and parse fully.</p>  # noqa: E501

<h2>Part A — Kings, Genesis, Samuel, and Exodus (items 1–10)</h2>
{items_a_html}

<h2>Part B — Numbers, Deuteronomy, Isaiah, and Samuel (items 11–18)</h2>
{items_b_html}

<h2>Part C — Distractor Check</h2>
<p>These three verbs are <strong>not</strong> Hiphil. Select "No" and complete the full parse.</p>
{items_c_html}

<script>
function toggleAnswer(num) {{
  var row = document.getElementById('ans-' + num);
  var btn = row.closest('.item').querySelector('.reveal-btn');
  if (row.style.display === 'none') {{
    row.style.display = '';
    btn.textContent = '\\u25BC Answer';
  }} else {{
    row.style.display = 'none';
    btn.textContent = '\\u25BA Answer';
  }}
}}
function showAll() {{
  document.querySelectorAll('.answer-row').forEach(function(r) {{ r.style.display = ''; }});
  document.querySelectorAll('.reveal-btn').forEach(function(b) {{ b.textContent = '\\u25BC Answer'; }});
}}
function hideAll() {{
  document.querySelectorAll('.answer-row').forEach(function(r) {{ r.style.display = 'none'; }});
  document.querySelectorAll('.reveal-btn').forEach(function(b) {{ b.textContent = '\\u25BA Answer'; }});
}}
function clearAll() {{
  document.querySelectorAll('.parse-field').forEach(function(f) {{ f.value = ''; }});
  document.querySelectorAll('.hiphil-select').forEach(function(s) {{ s.value = ''; }});
}}
</script>
</body>
</html>'''

    out.write_text(html, encoding='utf-8')
    print(f'  Saved {out}')
    return out


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('Building ch27 passage exercise...')
    build_md()
    build_html()
    print('Building PDF...')
    build_ch27_exercise()
    print('Done.')
