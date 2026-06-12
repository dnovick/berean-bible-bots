"""Build BBH Chapter 27 parsing exercises (3 HTML + MD formats).

Exercises generated:
  ch27-biconsig-drill       — Biconsonantal / Geminate Disambiguation Drill (24 items)
  ch27-niphal-hiphil-contrast — Niphal–Hiphil Contrast Drill (20 items)
  ch27-weak-form-id         — Hiphil Weak-Form Identification Drill (50 items)

Each exercise is built in two formats:
  .html  — interactive, with dropdowns for categorical columns and
           per-column answer rows (not a collapsed colspan string)
  .md    — static reference with answer key table

PDFs are generated via src.bible_grammar.exercise_pdf.bbh.

Usage:
    python3 scripts/ot/lessons/bbh/build_ch27_parsing_exercises.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, '.')
from src.bible_grammar.exercise_pdf.bbh import (  # noqa: E402
    build_ch27_bg_drill_exercise,
    build_ch27_nh_contrast_exercise,
    build_ch27_weak_form_id_exercise,
)

OUT_ROOT = Path('data/lessons/bbh/ch27/exercises')

# ── Shared HTML skeleton ──────────────────────────────────────────────────────

_CSS = """
body{font-family:Georgia,serif;max-width:960px;margin:2rem auto;padding:0 1rem}
h1{font-size:1.35rem}h2{font-size:1.05rem;margin-top:1.8rem;
border-bottom:1px solid #ccc;padding-bottom:.3rem}
.subtitle{color:#555;font-style:italic;margin-top:-.4rem}
.heb{font-size:1.15em;direction:rtl;unicode-bidi:embed}
table{width:100%;border-collapse:collapse;margin:.5rem 0;table-layout:fixed}
th,td{border:1px solid #ccc;padding:.3rem .45rem;font-size:.88rem;
vertical-align:middle}
th{background:#f0f0f0;font-weight:bold;white-space:nowrap}
select.pf,input.pf{width:100%;box-sizing:border-box;border:none;
font-family:inherit;font-size:.88rem;background:#fafafa;padding:2px}
select.pf:focus,input.pf:focus{outline:1px solid #888;background:#fff}
.ans-row{display:none}
.ans-row td{background:#e8f5e9!important;color:#1b5e20;font-size:.82rem}
.rev-btn{margin-top:.3rem;padding:.2rem .6rem;font-size:.82rem;cursor:pointer;
border:1px solid #999;background:#f5f5f5;border-radius:3px}
.rev-btn:hover{background:#e0e0e0}
.controls{margin:1rem 0;display:flex;gap:.5rem;flex-wrap:wrap}
.controls button{padding:.3rem .8rem;font-size:.85rem;cursor:pointer;
border:1px solid #999;background:#f5f5f5;border-radius:3px}
.controls button:hover{background:#e0e0e0}
.section-label{font-weight:bold;margin:1rem 0 .3rem;color:#333}
.disc-q{margin:.8rem 0 0;padding-left:1.2rem}
.note{background:#fffde7;border-left:3px solid #f9a825;padding:.4rem .6rem;
margin:.5rem 0;font-size:.88rem}
@media print{.controls,.rev-btn{display:none}
.pf{border-bottom:1px solid #333;background:transparent}
.ans-row{display:none!important}}
"""

_JS = """
function toggle(id){
  var r=document.getElementById(id);
  var btn=r.previousElementSibling;
  while(btn&&btn.tagName!=='TR'){btn=btn.previousElementSibling;}
  if(!btn){btn=r.parentElement.querySelector('[data-id="'+id+'"]');}
  if(r.style.display==='table-row'){
    r.style.display='none';
    if(btn)btn.querySelector('.rev-btn').textContent='►';
  }else{
    r.style.display='table-row';
    if(btn)btn.querySelector('.rev-btn').textContent='▼';
  }
}
function showAll(){
  document.querySelectorAll('.ans-row').forEach(function(r){r.style.display='table-row';});
  document.querySelectorAll('.rev-btn').forEach(function(b){b.textContent='▼';});
}
function hideAll(){
  document.querySelectorAll('.ans-row').forEach(function(r){r.style.display='none';});
  document.querySelectorAll('.rev-btn').forEach(function(b){b.textContent='►';});
}
function clearAll(){
  document.querySelectorAll('.pf').forEach(function(f){
    if(f.tagName==='SELECT')f.value='';else f.value='';
  });
}
"""

_CONTROLS = (
    '<div class="controls">'
    '<button onclick="showAll()">Show All Answers</button>'
    '<button onclick="hideAll()">Hide All Answers</button>'
    '<button onclick="clearAll()">Clear All Inputs</button>'
    '</div>'
)


def _wrap(title: str, subtitle: str, body: str) -> str:
    return (
        f'<!DOCTYPE html><html lang="en"><head>'
        f'<meta charset="UTF-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{title}</title>'
        f'<style>{_CSS}</style></head><body>'
        f'<h1>{title}</h1>'
        f'<p class="subtitle">{subtitle}</p>'
        f'{_CONTROLS}'
        f'{body}'
        f'<script>{_JS}</script>'
        f'</body></html>'
    )


def _sel(options: list[str], extra_css: str = '') -> str:
    opts = '<option value=""></option>' + ''.join(
        f'<option value="{o}">{o}</option>' for o in options
    )
    style = f' style="{extra_css}"' if extra_css else ''
    return f'<select class="pf"{style}>{opts}</select>'


def _inp(placeholder: str = '', rtl: bool = False) -> str:
    style = 'direction:rtl;unicode-bidi:embed;' if rtl else ''
    ph = f' placeholder="{placeholder}"' if placeholder else ''
    sty = f' style="{style}"' if style else ''
    return f'<input class="pf"{ph}{sty}>'


STEMS = ['Niphal', 'Hiphil', 'Hophal', 'Qal']
CONJS = ['Perfect', 'Imperfect', 'Wayyiqtol', 'Weqatal', 'Imperative',
         'Inf. Construct', 'Inf. Absolute', 'Participle']
PGNS = ['1cs', '1cp', '2ms', '2fs', '2mp', '2fp',
        '3ms', '3fs', '3mp', '3cp', 'ms', 'fs', 'mp', 'fp', '—']
CLASSES = ['I-guttural', 'III-ח/ע', 'III-א', 'III-ה',
           'I-נ', 'I-י', 'Biconsonantal', 'Geminate']


# ── Exercise 1: Biconsig Drill ────────────────────────────────────────────────

# (n, form, ref, ctx,  stem, conj, pgn, weak_class, root, note)
# Items interleaved: stem and class alternate so students must evaluate each form
# independently. Sequence: N/B, H/B, N/G, H/G, N/B(new), H/G(new), N/B, H/B,
# N/G, H/G, N/B(new), H/B(new), N/B, H/B, N/G, H/G, N/B, Hophal/B,
# N/G, H/B, N/B, H/G, Q/B, Q/B
_BG_DATA = [
    ('1',  'נָכוֹן',   'Gen 41:32',   'the thing is ___ by God',
     'Niphal', 'Perfect/Participle', '3ms / ms', 'Biconsonantal', 'כּוּן',
     'נָ prefix (qamets) = Niphal; medial ו vowel letter identifies Biconsonantal, not Geminate'),
    ('2',  'הֵקִים',   'Gen 6:18',    'I will ___ my covenant with you',
     'Hiphil', 'Perfect', '3ms', 'Biconsonantal', 'קוּם',
     'הֵ prefix (tsere) = Hiphil; chiriq-yod in stem = Biconsonantal; no R2=R3'),
    ('3',  'נָסַב',   '1 Kgs 7:24',  'the gourds ___ it, ten to a cubit',
     'Niphal', 'Perfect', '3ms', 'Geminate', 'סָבַב',
     'נָ prefix (qamets) = Niphal; R2=R3=ב identifies Geminate; compare Biconsonantal נָכוֹן'),
    ('4',  'הֵסֵב',   '2 Kgs 16:18', 'he ___ the king\'s entry',
     'Hiphil', 'Perfect', '3ms', 'Geminate', 'סָבַב',
     'הֵ prefix (tsere) = Hiphil; tsere in contracted stem, R2=R3=ב = Geminate'),
    ('5',  'נָמֹוג',  'Isa 14:31',   'all Philistia ___',
     'Niphal', 'Perfect', '3ms', 'Biconsonantal', 'מוּג',
     'נָ prefix + medial ו = Niphal Biconsonantal; root מוּג = to melt; same pattern as נָכוֹן'),
    ('6',  'הֵמַסּוּ', 'Deu 1:28',    'our brothers ___ our hearts',
     'Hiphil', 'Perfect', '3cp', 'Geminate', 'מסס',
     'הֵ prefix (tsere) = Hiphil; R2=R3=ס with dagesh forte = Geminate'),
    ('7',  'יִכּוֹן',  'Psa 93:2',    'your throne ___ from of old',
     'Niphal', 'Imperfect', '3ms', 'Biconsonantal', 'כּוּן',
     'יִ prefix + dagesh in כּ (Niphal imperfect) + contracted holem-vav root = Biconsonantal'),
    ('8',  'יָקִים',   'Deu 18:15',   'the LORD your God will ___ up a prophet',
     'Hiphil', 'Imperfect', '3ms', 'Biconsonantal', 'קוּם',
     'יָ prefix (qamets) = Hiphil Biconsonantal imperfect; chiriq-yod medial vowel letter'),
    ('9',  'יִסֹּב',   'Num 21:4',    'they traveled ___ Mount Edom',
     'Niphal', 'Imperfect', '3ms', 'Geminate', 'סָבַב',
     'יִ prefix + dagesh in סּ (R2=R3 doubled) + holem in contracted root = Geminate'),
    ('10', 'יָסֵב',    'Eccl 1:6',    'the wind ___ to the south',
     'Hiphil', 'Imperfect', '3ms', 'Geminate', 'סָבַב',
     'יָ prefix (qamets) = Hiphil; tsere in contracted root; R2=R3=ב = Geminate'),
    ('11', 'יָרֻם',    'Isa 52:13',   'my servant shall be high and ___ up',
     'Niphal', 'Imperfect', '3ms', 'Biconsonantal', 'רוּם',
     'יָ prefix + qibbutz under R2 (passive vowel) = Niphal Biconsonantal; contrast Hiphil יָרִים'),
    ('12', 'הֵרִים',   'Gen 14:22',   'I have ___ my hand to the LORD',
     'Hiphil', 'Perfect', '3ms', 'Biconsonantal', 'רוּם',
     'הֵ prefix (tsere) + chiriq-yod = Hiphil Biconsonantal perfect; causative — lifted up'),
    ('13', 'הֵכּוֹן',  'Psa 57:8',    'my heart is ___, O God',
     'Niphal', 'Perfect', '3ms', 'Biconsonantal', 'כּוּן',
     'הֵ prefix (tsere) + dagesh + contracted holem-vav = Niphal Biconsonantal perfect'),
    ('14', 'הָקֵם',    'Deu 27:26',   '"___ the words of this law"',
     'Hiphil', 'Imperative', '2ms', 'Biconsonantal', 'קוּם',
     'הָ prefix (qamets) = Hiphil Biconsonantal imperative; tsere final; chiriq in stem'),
    ('15', 'נָסֹב',    'Josh 15:3',   'the border ___ from the south',
     'Niphal', 'Perfect', '3ms', 'Geminate', 'סָבַב',
     'נָ prefix (qamets) = Niphal; holem in root shows contraction of R2=R3 = Geminate'),
    ('16', 'הָסֵב',    '2 Sam 2:22',  '___ from following me',
     'Hiphil', 'Imperative', '2ms', 'Geminate', 'סָבַב',
     'הָ prefix (qamets) = Hiphil; tsere in contracted R2=R3 stem = Geminate'),
    ('17', 'יָרֹם',    'Psa 99:2',    'great is the LORD, and ___ above all peoples',
     'Niphal', 'Imperfect', '3ms', 'Biconsonantal', 'רוּם',
     'יָ prefix + holem under R2 = Niphal Biconsonantal; compare Hiphil יָרִים (chiriq)'),
    ('18', 'הוּרַם',   'Lev 4:10',    'just as it is ___ from the ox of peace offerings',
     'Hophal', 'Perfect', '3ms', 'Biconsonantal', 'רוּם',
     'הוּ prefix (holem-vav) = Hophal (passive of Hiphil), not Niphal or Hiphil'),
    ('19', 'הִסֹּב',   '2 Sam 18:30', 'the king said, ___ and stand here',
     'Niphal', 'Imperative', '2ms', 'Geminate', 'סָבַב',
     'הִ prefix + dagesh forte in ב (R2=R3) = Niphal Geminate imperative'),
    ('20', 'מֵקִים',   '1 Sam 2:8',   'He ___ the poor from the dust',
     'Hiphil', 'Participle', 'ms', 'Biconsonantal', 'קוּם',
     'מֵ prefix (tsere) = Hiphil participle; chiriq-yod medial vowel letter = Biconsonantal'),
    ('21', 'תִּכּוֹן',  'Psa 5:3',     'in the morning I ___ my prayer',
     'Niphal', 'Imperfect', '2ms / 3fs', 'Biconsonantal', 'כּוּן',
     'תִּ prefix + dagesh in כּ + holem-vav = Niphal Biconsonantal imperfect'),
    ('22', 'מֵסֵב',    'Jer 21:4',    'turning around the weapons of war ___',
     'Hiphil', 'Participle', 'ms', 'Geminate', 'סָבַב',
     'מֵ prefix (tsere) = Hiphil participle; tsere in contracted R2=R3 = Geminate'),
    ('23', 'יָשׁוּב',  'Hos 14:8',    'they ___ in the shade',
     'Qal', 'Imperfect', '3ms', 'Biconsonantal', 'שׁוּב',
     'Qal Biconsonantal — no Niphal נ or Hiphil הֵ/מֵ marker; medial ו retained'),
    ('24', 'יָשֹׁב',   'Lam 1:11',    'all her people ___ to find bread',
     'Qal', 'Imperfect', '3ms', 'Biconsonantal', 'שׁוּב',
     'Qal Biconsonantal; holem vowel grade vs. shureq in יָשׁוּב — both Qal, not Niphal/Hiphil'),
]

_BG_DISC = [
    'Items 1 (<span class="heb">נָכוֹן</span>) and 3 (<span class="heb">נָסַב</span>) '
    'have the same prefix vowel (נָ, qamets) and nearly identical shapes. What is the only '
    'reliable way to know that <span class="heb">נָכוֹן</span> is Biconsonantal (root '
    '<span class="heb">כּוּן</span>) and <span class="heb">נָסַב</span> is Geminate '
    '(root <span class="heb">סָבַב</span>)?',

    'Items 2 (<span class="heb">הֵקִים</span>) and 4 (<span class="heb">הֵסֵב</span>) '
    'both have הֵ prefix (tsere). One retains a medial vowel letter and the other does not. '
    'Explain in one sentence how that difference reveals the class.',

    'Items 8 (<span class="heb">יָקִים</span>, Hiphil) and 11 '
    '(<span class="heb">יָרֻם</span>, Niphal) both begin with יָ (qamets). '
    'What vowel under R2 distinguishes the Hiphil from the Niphal in these imperfect forms?',

    'Item 18 (<span class="heb">הוּרַם</span>) is Hophal, not Niphal or Hiphil. '
    'What prefix vowel distinguishes Hophal from Hiphil in the perfect? '
    'How does it differ from the Niphal הֵ prefix seen in item 13?',

    'Items 23–24 (<span class="heb">יָשׁוּב</span> / <span class="heb">יָשֹׁב</span>) '
    'are both Qal. Neither has the standard Niphal or Hiphil prefix markers. '
    'What is the only vowel difference between them, and what does it tell you '
    'about the stem?',
]


def _bg_table(rows: list) -> str:
    # 9 columns, no Context — fits comfortably at 960px without overflow
    out = (
        '<table style="table-layout:auto"><thead><tr>'
        '<th style="width:3%;white-space:nowrap">#</th>'
        '<th style="width:13%">Form</th>'
        '<th style="width:11%">Reference</th>'
        '<th style="width:11%">Stem</th>'
        '<th style="width:14%">Conjugation</th>'
        '<th style="width:8%">PGN</th>'
        '<th style="width:12%">Weak Class</th>'
        '<th style="width:8%">Root</th>'
        '<th style="width:2%"></th>'
        '</tr></thead><tbody>'
    )
    for row in rows:
        n, form, ref, ctx, stem, conj, pgn, wclass, root, note = row
        rid = f'bg{n}'
        out += (
            f'<tr>'
            f'<td>{n}</td>'
            f'<td><span class="heb">{form}</span>'
            f'<br><small style="color:#666">{ref}</small></td>'
            f'<td style="display:none">{ref}</td>'
            f'<td>{_sel(STEMS)}</td>'
            f'<td>{_sel(CONJS)}</td>'
            f'<td>{_sel(PGNS)}</td>'
            f'<td>{_sel(CLASSES)}</td>'
            f'<td>{_inp("root…", rtl=True)}</td>'
            f'<td><button class="rev-btn" onclick="toggle(\'{rid}\')">&#9654;</button></td>'
            f'</tr>'
            f'<tr class="ans-row" id="{rid}">'
            f'<td></td>'
            f'<td><span class="heb">{form}</span></td>'
            f'<td style="display:none"></td>'
            f'<td><strong>{stem}</strong></td>'
            f'<td><strong>{conj}</strong></td>'
            f'<td><strong>{pgn}</strong></td>'
            f'<td><strong>{wclass}</strong></td>'
            f'<td style="direction:rtl;unicode-bidi:embed;"><strong>{root}</strong></td>'
            f'<td><em style="color:#666;font-size:.8em">{note}</em></td>'
            f'</tr>'
        )
    out += '</tbody></table>'
    return out


def build_bg_html() -> Path:
    body = (
        '<div class="note">'
        'All 24 forms are drawn from Biconsonantal and Geminate roots across '
        'all four stems (Niphal, Hiphil, Hophal, Qal). For each form: '
        'identify the <strong>stem</strong>, <strong>conjugation</strong>, '
        '<strong>PGN</strong>, <strong>weak class</strong> '
        '(Biconsonantal or Geminate), and <strong>root</strong>.'
        '</div>'
        '<h2>Mixed Drill — 24 Items</h2>'
    )
    body += _bg_table(_BG_DATA)
    body += '<h2>Discussion Questions</h2><ol class="disc-q">'
    for q in _BG_DISC:
        body += f'<li>{q}</li>'
    body += '</ol>'
    html = _wrap(
        'Chapter 27 — Biconsonantal / Geminate Disambiguation Drill',
        'BBH Chapters 25 &amp; 27 · Niphal and Hiphil Weak Verbs',
        body,
    )
    out = OUT_ROOT / 'ch27-biconsig-drill' / 'ch27-biconsig-drill.html'
    out.write_text(html, encoding='utf-8')
    print(f'  Saved {out}')
    return out


def build_bg_md() -> Path:
    lines = [
        '# Chapter 27 — Biconsonantal / Geminate Disambiguation Drill',
        '',
        '*BBH Chapters 25 & 27 · Niphal and Hiphil Weak Verbs*',
        '',
        '---',
        '',
        '## Instructions',
        '',
        'For each form: identify the **stem** (Niphal / Hiphil / Hophal / Qal), '
        '**conjugation**, **PGN**, **weak class** (Biconsonantal or Geminate), and **root**.',
        '',
        '## Mixed Drill — 24 Items',
        '',
        '| # | Form | Reference | Stem | Conj | PGN | Class | Root |',
        '|---|---|---|---|---|---|---|---|',
    ]
    for n, form, ref, ctx, *_ in _BG_DATA:
        lines.append(f'| {n} | {form} | {ref} | | | | | |')
    lines += ['', '---', '', '## Answer Key', '',
              '| # | Form | Stem | Conjugation | PGN | Weak Class | Root | Note |',
              '|---|---|---|---|---|---|---|---|']
    for n, form, ref, ctx, stem, conj, pgn, wclass, root, note in _BG_DATA:
        note_short = note[:70] + '…' if len(note) > 70 else note
        lines.append(
            f'| {n} | {form} | {stem} | {conj} | {pgn} | {wclass} | {root} | {note_short} |'
        )
    lines.append('')

    out = OUT_ROOT / 'ch27-biconsig-drill' / 'ch27-biconsig-drill.md'
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  Saved {out}')
    return out


# ── Exercise 2: Niphal–Hiphil Contrast Drill ──────────────────────────────────

# (n, form, ref, ctx, stem, conj, pgn, root, weak_class, note)
_NHC_DATA = [
    # Part A
    ('1',  'נִשְׁמַע',    'Est 1:20',   'the decree ___ throughout all the kingdom',
     'Niphal', 'Perfect', '3ms', 'שָׁמַע', 'III-ח/ע',
     'נִ prefix + patach furtive before final ע = Niphal III-ח/ע perfect'),
    ('2',  'הִשְׁמִיעַ',  '1 Kgs 15:22', 'Asa ___ this throughout all Judah',
     'Hiphil', 'Perfect', '3ms', 'שָׁמַע', 'III-ח/ע',
     'הִ prefix + chiriq-yod + patach furtive before ע = Hiphil III-ח/ע perfect'),
    ('3',  'יִמָּצֵא',   'Gen 44:10',  'only the one with whom it is found ___ my slave',
     'Niphal', 'Imperfect', '3ms', 'מָצָא', 'III-א',
     'יִמָּ cluster + tsere + silent final א = Niphal III-א imperfect'),
    ('4',  'הִמְצִיא',   'Neh 9:15',   'you ___ them bread from heaven',
     'Hiphil', 'Perfect', '3ms', 'מָצָא', 'III-א',
     'הִ prefix + chiriq-yod + silent final א = Hiphil III-א perfect'),
    ('5',  'נִגְלָה',    'Isa 40:5',   'the glory of the LORD will ___',
     'Niphal', 'Perfect', '3ms', 'גָּלָה', 'III-ה',
     'נִ prefix + final ָה = Niphal III-ה perfect'),
    ('6',  'הֶעֱלָה',    '1 Sam 12:6', 'the LORD who ___ Moses and Aaron',
     'Hiphil', 'Perfect', '3ms', 'עָלָה', 'III-ה + I-guttural',
     'הֶ prefix (seghol) + composite shewa = Hiphil III-ה + I-guttural perfect'),
    ('7',  'וַיִּגַּשׁ',  'Gen 44:18',  'Judah ___ close to him',
     'Niphal', 'Wayyiqtol', '3ms', 'נָגַשׁ', 'I-נ',
     'וַיִּ + dagesh in ג (R2) = Niphal I-נ wayyiqtol; נ has assimilated'),
    ('8',  'הִגִּישׁ',   '2 Sam 17:29', 'they ___ food to David',
     'Hiphil', 'Perfect', '3ms', 'נָגַשׁ', 'I-נ',
     'הִ prefix + dagesh forte in ג (R2) + chiriq = Hiphil I-נ perfect'),
    # Part B
    ('9',  'נוֹלַד',     'Gen 21:5',   'when Isaac was ___',
     'Niphal', 'Perfect', '3ms', 'יָלַד', 'I-י',
     'נוֹ prefix + patach under R2 = Niphal I-י perfect'),
    ('10', 'וַיּוֹלֶד',  'Gen 10:8',   'Cush ___ Nimrod',
     'Hiphil', 'Wayyiqtol', '3ms', 'יָלַד', 'I-י',
     'וַיּוֹ prefix (holem-vav) = Hiphil I-י wayyiqtol; contrast Niphal וַיִּוָּלֵד'),
    ('11', 'יִוָּלֵד',   'Gen 17:17',  'shall a child be born to a man who is 100 years old?',
     'Niphal', 'Imperfect', '3ms', 'יָלַד', 'I-י',
     'יִוָּ cluster = Niphal I-י imperfect; holem-vav prefix would be Hiphil'),
    ('12', 'יוֹרִיד',   '1 Sam 2:6',  'the LORD ___ to Sheol and raises up',
     'Hiphil', 'Imperfect', '3ms', 'יָרַד', 'I-י',
     'יוֹ prefix (holem-vav) = Hiphil I-י imperfect; chiriq-yod in root'),
    ('13', 'וַיִּוָּדַע', 'Est 2:22',   'the matter became known',
     'Niphal', 'Wayyiqtol', '3ms', 'יָדַע', 'I-י',
     'וַיִּוָּ = Niphal I-י wayyiqtol; patach under R2 (יָדַע class)'),
    ('14', 'הֵקִים',    'Gen 6:18',   'I will ___ my covenant with you',
     'Hiphil', 'Perfect', '3ms', 'קוּם', 'Biconsonantal',
     'הֵ prefix (tsere) + chiriq-yod = Hiphil Biconsonantal perfect'),
    ('15', 'נָכוֹן',    'Gen 41:32',  'the thing is ___ / fixed by God',
     'Niphal', 'Perfect / Participle', '3ms / ms', 'כּוּן', 'Biconsonantal',
     'נָ prefix (qamets) = Niphal Biconsonantal perfect or participle'),
    # Part C
    ('16', 'וַיַּעַל',   'Gen 8:20',   'and Noah ___ burnt offerings on the altar',
     'Hiphil', 'Wayyiqtol', '3ms', 'עָלָה', 'III-ה + I-guttural',
     'Apocopated: ה dropped; short patach under R2; also I-guttural composite shewa'),
    ('17', 'וַיִּגָּל',  'Num 24:4',   'the man whose eyes are unveiled',
     'Niphal', 'Wayyiqtol', '3ms', 'גָּלָה', 'III-ה',
     'Apocopated: ה dropped; וַיִּגָּ cluster = Niphal III-ה wayyiqtol'),
    ('18', 'הָסֵב',     '2 Sam 5:23', '___ around behind them',
     'Hiphil', 'Imperative', '2ms', 'סָבַב', 'Geminate',
     'הָ prefix (qamets) = Hiphil imperative; tsere in contracted R2=R3 = Geminate'),
    ('19', 'מַעֲמִידִים', 'Neh 4:7',   'those who ___ behind the whole house',
     'Hiphil', 'Participle', 'mp', 'עָמַד', 'I-guttural',
     'מַ + composite shewa under ע + chiriq + ים = Hiphil I-guttural participle mp'),
    ('20', 'הֵרָאֵה',   '1 Kgs 18:1', '___ yourself to Ahab',
     'Niphal', 'Imperative', '2ms', 'רָאָה', 'III-ה',
     'הֵ prefix (tsere; compensatory for ר) + final ֵה = Niphal III-ה imperative'),
]

_NHC_SECTIONS = [
    ('Part A — Roots with Contrasting Niphal and Hiphil Meanings', range(1, 9)),
    ('Part B — Shared Roots, Weak-Class Focus', range(9, 16)),
    ('Part C — Mixed Review', range(16, 21)),
]

_NHC_DISC = [
    'Items 1–2 (<span class="heb">שָׁמַע</span>) and items 3–4 (<span class="heb">מָצָא</span>): '
    'in each pair the Niphal and Hiphil forms share the same root but have opposite meanings. '
    'Pick one pair and explain in one sentence what the Niphal adds and what the Hiphil adds.',

    'Items 9–11 are all from the root <span class="heb">יָלַד</span> (I-י). '
    'Two are Niphal and one is Hiphil. Both stems use a holem-vav cluster, '
    'yet they are distinguishable. What is the precise difference between '
    '<span class="heb">וַיּוֹלֶד</span> (Hiphil) and <span class="heb">וַיִּוָּלֵד</span> (Niphal)?',

    'Items 16–17 both show apocopated wayyiqtol forms from III-ה roots. '
    'Item 16 is Hiphil and item 17 is Niphal. Without the prefix helping you, '
    'how do you determine the stem of an apocopated form?',

    'Items 18 (<span class="heb">הָסֵב</span>) and 20 (<span class="heb">הֵרָאֵה</span>) '
    'are both imperatives. One is Hiphil Geminate, the other is Niphal III-ה. '
    'What is the prefix vowel difference, and what does it signal in each case?',
]


def _nhc_table_section(section_range: range) -> str:
    out = (
        '<table><thead><tr>'
        '<th style="width:3%">#</th>'
        '<th style="width:11%">Form</th>'
        '<th style="width:11%">Reference</th>'
        '<th style="width:22%">Context</th>'
        '<th style="width:9%">Stem</th>'
        '<th style="width:12%">Conjugation</th>'
        '<th style="width:7%">PGN</th>'
        '<th style="width:9%">Root</th>'
        '<th style="width:11%">Weak Class</th>'
        '<th style="width:5%"></th>'
        '</tr></thead><tbody>'
    )
    for row in _NHC_DATA:
        n, form, ref, ctx, stem, conj, pgn, root, wclass, note = row
        if int(n) not in section_range:
            continue
        rid = f'nhc{n}'
        out += (
            f'<tr>'
            f'<td>{n}</td>'
            f'<td><span class="heb">{form}</span></td>'
            f'<td>{ref}</td>'
            f'<td>"{ctx}"</td>'
            f'<td>{_sel(["Niphal", "Hiphil", "Qal", "Hophal"])}</td>'
            f'<td>{_sel(CONJS)}</td>'
            f'<td>{_sel(PGNS)}</td>'
            f'<td>{_inp("root…", rtl=True)}</td>'
            f'<td>{_sel(CLASSES)}</td>'
            f'<td><button class="rev-btn" onclick="toggle(\'{rid}\')">&#9654;</button></td>'
            f'</tr>'
            f'<tr class="ans-row" id="{rid}">'
            f'<td></td>'
            f'<td><span class="heb">{form}</span></td>'
            f'<td>{ref}</td>'
            f'<td></td>'
            f'<td><strong>{stem}</strong></td>'
            f'<td><strong>{conj}</strong></td>'
            f'<td><strong>{pgn}</strong></td>'
            f'<td style="direction:rtl;unicode-bidi:embed;"><strong>{root}</strong></td>'
            f'<td><strong>{wclass}</strong></td>'
            f'<td><em style="color:#555;font-size:.8em;">{note}</em></td>'
            f'</tr>'
        )
    out += '</tbody></table>'
    return out


def build_nhc_html() -> Path:
    body = ''
    for section_title, section_range in _NHC_SECTIONS:
        body += f'<h2>{section_title}</h2>'
        body += _nhc_table_section(section_range)
    body += '<h2>Discussion Questions</h2><ol class="disc-q">'
    for q in _NHC_DISC:
        body += f'<li>{q}</li>'
    body += '</ol>'
    html = _wrap(
        'Chapter 27 — Niphal–Hiphil Contrast Drill',
        'BBH Chapters 25 &amp; 27 · Niphal and Hiphil Weak Verbs',
        body,
    )
    out = OUT_ROOT / 'ch27-niphal-hiphil-contrast' / 'ch27-niphal-hiphil-contrast.html'
    out.write_text(html, encoding='utf-8')
    print(f'  Saved {out}')
    return out


def build_nhc_md() -> Path:
    lines = [
        '# Chapter 27 — Niphal–Hiphil Contrast Drill',
        '',
        '*BBH Chapters 25 & 27 · Niphal and Hiphil Weak Verbs*',
        '',
        '---',
        '',
        '## Instructions',
        '',
        'For each form: identify the **stem** (Niphal / Hiphil / Qal / Hophal), '
        '**conjugation**, **PGN**, **root**, and **weak class**.',
        '',
    ]
    for section_title, section_range in _NHC_SECTIONS:
        lines += [f'## {section_title}', '',
                  '| # | Form | Reference | Context | Stem | Conj | PGN | Root | Class |',
                  '|---|---|---|---|---|---|---|---|---|']
        for row in _NHC_DATA:
            n, form, ref, ctx, *_ = row
            if int(n) in section_range:
                lines.append(f'| {n} | {form} | {ref} | "{ctx}" | | | | | |')
        lines.append('')
    lines += ['---', '', '## Answer Key', '',
              '| # | Form | Stem | Conjugation | PGN | Root | Class | Note |',
              '|---|---|---|---|---|---|---|---|']
    for n, form, ref, ctx, stem, conj, pgn, root, wclass, note in _NHC_DATA:
        note_short = note[:70] + '…' if len(note) > 70 else note
        lines.append(
            f'| {n} | {form} | {stem} | {conj} | {pgn} | {root} | {wclass} | {note_short} |'
        )
    lines.append('')
    out = OUT_ROOT / 'ch27-niphal-hiphil-contrast' / 'ch27-niphal-hiphil-contrast.md'
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  Saved {out}')
    return out


# ── Exercise 3: Hiphil Weak-Form Identification Drill ─────────────────────────

# Part A: (n, form, ref, conj, pgn, root, note)  — all Hiphil, class given by group
_WFI_GROUPS = [
    ('Group 1 — I-guttural', 'I-guttural', [
        ('1',  'הֶעֱמִיד',     '1 Chr 6:31', 'Perfect',      '3ms',   'עָמַד',
         'seghol under הֶ + hateph-seghol under ע are the twin I-guttural markers'),
        ('2',  'וַיַּעֲמֵד',   '2 Chr 8:14', 'Wayyiqtol',    '3ms',   'עָמַד',
         'patach prefix + composite shewa under ע + tsere final'),
        ('3',  'יַעֲמִיד',    'Pro 29:4',   'Imperfect',    '3ms',   'עָמַד',
         'patach prefix + composite shewa; no dagesh in ע (guttural rule)'),
        ('4',  'הַעֲמֵד',     'Isa 21:6',   'Imperative',   '2ms',   'עָמַד',
         'הַ + composite shewa under ע + tsere — he/composite-shewa pattern'),
        ('5',  'מַעֲמִיד',    '2 Chr 18:34', 'Participle',  'ms',    'עָמַד',
         'מַ + composite shewa under ע + chiriq — standard I-guttural participle'),
    ]),
    ('Group 2 — III-ח/ע', 'III-ח/ע', [
        ('6',  'הִשְׁמִיעַ',   '1 Kgs 15:22', 'Perfect',    '3ms',   'שָׁמַע',
         'chiriq-yod + patach furtive before final ע — patach not tsere'),
        ('7',  'וְהִשְׁמִיעַ', 'Isa 30:30',  'Imperfect',   '3ms (w/vav)', 'שָׁמַע',
         'patach furtive before final ע; vav + שׁ + chiriq-yod = standard III-ח/ע'),
        ('8',  'יַשְׁמִיעַ',   'Isa 42:2',   'Imperfect',   '3ms',   'שָׁמַע',
         'patach prefix (not tsere) + chiriq-yod + patach furtive before ע'),
        ('9',  'הַשְׁמִיעוּ',  'Isa 48:20',  'Imperative',  '2mp',   'שָׁמַע',
         'הַ + chiriq-yod + patach before ע + וּ plural ending = III-ח/ע imv 2mp'),
        ('10', 'מַשְׁמִיעַ',   'Isa 41:26',  'Participle',  'ms',    'שָׁמַע',
         'מַ + chiriq-yod + patach furtive before ע = III-ח/ע participle'),
    ]),
    ('Group 3 — III-א', 'III-א', [
        ('11', 'הֶחֱטִיא',    '1 Kgs 14:16', 'Perfect',    '3ms',   'חָטָא',
         'seghol under הֶ + composite shewa under ח = I-guttural + III-א; chiriq-yod + silent א'),
        ('12', 'וַיַּחֲטִא',  '2 Kgs 21:11', 'Wayyiqtol', '3ms',   'חָטָא',
         'patach prefix + composite shewa + tsere + silent final א = Hiphil III-א wayyiqtol'),
        ('13', 'יַחֲטִיאוּ',  'Exo 23:33',  'Imperfect',   '3mp',   'חָטָא',
         'patach prefix + composite shewa + chiriq-yod + silent א + וּ = III-א impf 3mp'),
        ('14', 'הַחֲטִיא',   'Jer 32:35',  'Inf. Construct', '—',  'חָטָא',
         'הַ + composite shewa + chiriq-yod + silent final א = III-א inf. construct'),
        ('15', 'מַחֲטִיאֵי',  'Isa 29:21',  'Participle',  'mp cstr', 'חָטָא',
         'מַ + composite shewa + chiriq-yod + silent א + ֵי = III-א ptc mp construct'),
    ]),
    ('Group 4 — III-ה', 'III-ה', [
        ('16', 'הֶעֱלָה',     '1 Sam 12:6', 'Perfect',     '3ms',   'עָלָה',
         'qamets + ה ending; seghol under הֶ; III-ה I-guttural combination'),
        ('17', 'וַיַּעַל',    'Gen 8:20',   'Wayyiqtol',   '3ms',   'עָלָה',
         'apocopated — ה dropped; short patach under R2; I-guttural composite shewa lost'),
        ('18', 'יַעֲלֶה',     'Exo 34:3',   'Imperfect',   '3ms',   'עָלָה',
         'seghol + ה ending; composite shewa under ע; standard III-ה Hiphil imperfect'),
        ('19', 'הַרְאֵנִי',   'Exo 33:18',  'Imperative',  '2ms + 1cs suffix', 'רָאָה',
         'tsere + ה retained (not apocopated) + suffix נִי; standard III-ה imperative'),
        ('20', 'מַרְאֶה',     'Gen 12:11',  'Participle',  'ms',    'רָאָה',
         'מַ + composite shewa + seghol (not chiriq) + ה = III-ה Hiphil participle'),
    ]),
    ('Group 5 — I-נ', 'I-נ', [
        ('21', 'הִפִּיל',     '1 Sam 3:19', 'Perfect',     '3ms',   'נָפַל',
         'dagesh forte in פּ (R2); נ assimilated; chiriq-yod = I-נ Hiphil'),
        ('22', 'וַיַּפֵּל',   'Gen 2:21',   'Wayyiqtol',   '3ms',   'נָפַל',
         'patach prefix + dagesh in R2 + tsere = I-נ Hiphil wayyiqtol'),
        ('23', 'יַפִּיל',     'Exo 21:27',  'Imperfect',   '3ms',   'נָפַל',
         'patach prefix + dagesh in R2 + chiriq = I-נ Hiphil imperfect'),
        ('24', 'הַגִּשָׁה',   'Gen 27:25',  'Imperative',  '2ms + ה', 'נָגַשׁ',
         'הַ + dagesh in ג + cohortative ה; נ assimilated into ג; I-נ imperative'),
        ('25', 'וּמַגִּישׁ',  'Mal 2:12',   'Participle',  'ms',    'נָגַשׁ',
         'מַ + dagesh in ג + chiriq = I-נ Hiphil participle; וּ is conjunction'),
    ]),
    ('Group 6 — I-י', 'I-י', [
        ('26', 'הוֹצִיא',     'Gen 14:18',  'Perfect',     '3ms',   'יָצָא',
         'הוֹ prefix (holem-vav) — the signature I-י/vav Hiphil marker'),
        ('27', 'וַיּוֹצֵא',   'Gen 15:5',   'Wayyiqtol',   '3ms',   'יָצָא',
         'וַיּוֹ prefix — dagesh in יּ + holem-vav uniquely identifies I-י Hiphil'),
        ('28', 'יוֹצִיא',     'Psa 25:15',  'Imperfect',   '3ms',   'יָצָא',
         'יוֹ prefix (holem-vav) = I-י Hiphil imperfect; chiriq-yod in root'),
        ('29', 'וַיּוֹרֶד',   'Jdg 7:5',    'Wayyiqtol',   '3ms',   'יָרַד',
         'וַיּוֹ prefix + seghol (apocopated ה) = I-י III-ה Hiphil wayyiqtol'),
        ('30', 'מוֹצִיא',     'Psa 68:6',   'Participle',  'ms',    'יָצָא',
         'מוֹ prefix (holem-vav) — not מַ; uniquely marks I-י Hiphil participle'),
    ]),
    ('Group 7 — Biconsonantal', 'Biconsonantal', [
        ('31', 'הֵקִים',      'Jos 4:9',    'Perfect',     '3ms',   'קוּם',
         'הֵ prefix (tsere) — not הִ (hiriq); chiriq-yod in medial = Biconsonantal'),
        ('32', 'וַיָּקֶם',    'Exo 40:18',  'Wayyiqtol',   '3ms',   'קוּם',
         'qamets prefix + apocopated seghol final = Biconsonantal Hiphil wayyiqtol'),
        ('33', 'יָקִים',      'Deu 18:15',  'Imperfect',   '3ms',   'קוּם',
         'qamets under prefix consonant (יָ) = Biconsonantal Hiphil imperfect'),
        ('34', 'הָקֵם',       '2 Sam 7:25', 'Imperative',  '2ms',   'קוּם',
         'הָ prefix (qamets) + tsere = Biconsonantal imperative'),
        ('35', 'מֵקִים',      '1 Sam 2:8',  'Participle',  'ms',    'קוּם',
         'מֵ prefix (tsere) — not מַ; uniquely marks Biconsonantal Hiphil participle'),
    ]),
    ('Group 8 — Geminate', 'Geminate', [
        ('36', 'הֵסֵב',       '2 Kgs 16:18', 'Perfect',   '3ms',   'סָבַב',
         'הֵ prefix (tsere) = Hiphil; R2=R3=ב; tsere in contracted stem = Geminate'),
        ('37', 'וַיַּסֵּב',   'Exo 13:18',  'Wayyiqtol',   '3ms',   'סָבַב',
         'patach prefix + dagesh forte in ב (R2=R3 doubled) + tsere = Geminate wayyiqtol'),
        ('38', 'יָסֵב',       'paradigm',   'Imperfect',   '3ms',   'סָבַב',
         'qamets under יָ (= Biconsonantal/Geminate pattern); tsere in contracted root'),
        ('39', 'הָסֵב',       '2 Sam 5:23', 'Imperative',  '2ms',   'סָבַב',
         'הָ prefix (qamets) + tsere in contracted R2=R3 = Geminate imperative'),
        ('40', 'מֵסֵב',       'Jer 21:4',   'Participle',  'ms',    'סָבַב',
         'מֵ prefix (tsere) + tsere in contracted R2=R3 = Geminate participle'),
    ]),
]

# Part B: (n, form, ref, ctx, weak_class, conj, pgn, root, note)
_WFI_B = [
    ('41', 'וַיַּשְׁמַע',   '1 Sam 15:14',
     'and he made heard',
     'III-ח/ע', 'Wayyiqtol', '3ms', 'שָׁמַע',
     'patach (not tsere) before final ע — guttural forces vowel lowering in shortened form'),
    ('42', 'הֵשִׂים',       'Gen 45:9',
     'he made / placed',
     'Biconsonantal', 'Perfect', '3ms', 'שִׂים',
     'הֵ prefix (tsere); root שׂ-י-מ with medial chiriq-yod = Biconsonantal'),
    ('43', 'וַיַּעַל',      'Gen 22:2',
     'and he offered up',
     'III-ה + I-guttural', 'Wayyiqtol', '3ms', 'עָלָה',
     'apocopated: ה dropped; short patach under R2; I-guttural composite shewa'),
    ('44', 'הִגִּישׁ',     'Amos 9:13',
     'he brought near',
     'I-נ', 'Perfect', '3ms', 'נָגַשׁ',
     'הִ prefix + dagesh forte in ג (R2); נ assimilated into R2 = I-נ Hiphil'),
    ('45', 'הָסֵב',        '2 Sam 5:23',
     'circle around behind them',
     'Geminate', 'Imperative', '2ms', 'סָבַב',
     'הָ prefix (qamets) — same as Biconsonantal הָקֵם; tsere from contracted R2=R3 = Geminate'),
    ('46', 'הֶרְאָה',      'Exo 25:9',
     'he showed',
     'III-ה', 'Perfect', '3ms', 'רָאָה',
     'qamets + ה ending; seghol under הֶ = III-ה Hiphil perfect'),
    ('47', 'וַיּוֹרֶד',    'Gen 42:38',
     'and he brought down',
     'I-י', 'Wayyiqtol', '3ms', 'יָרַד',
     'וַיּוֹ prefix uniquely identifies I-י Hiphil wayyiqtol'),
    ('48', 'מַעֲמִידִים',  'Neh 4:7',
     'those who station / prop up',
     'I-guttural', 'Participle', 'mp', 'עָמַד',
     'מַ + composite shewa under ע + chiriq + ים = I-guttural Hiphil participle mp'),
    ('49', 'הַמְצֵא',      'paradigm',
     'cause to find! (imperative)',
     'III-א', 'Imperative', '2ms', 'מָצָא',
     'הַ prefix (patach) + tsere + silent final א = III-א Hiphil imperative'),
    ('50', 'וָאָקִים',     'Exo 6:4',
     'and I established',
     'Biconsonantal', 'Wayyiqtol', '1cs', 'קוּם',
     'וָאָ (1cs wayyiqtol) + qamets + chiriq-yod = Biconsonantal 1cs wayyiqtol'),
]

_WFI_DISC = [
    'Compare <span class="heb">הִמְצִיא</span> (III-א perfect 3ms) and '
    '<span class="heb">הַמְצֵא</span> (III-א imperative 2ms). Both end with silent final א. '
    'How do you distinguish them? What is the key difference in the prefix vowel?',

    '<span class="heb">הַשְׁמִיעוּ</span> (III-ח/ע imperative 2mp) and '
    '<span class="heb">הַעֲמֵד</span> (I-guttural imperative 2ms) both begin with הַ. '
    'How does the vowel under R1 differ? What does that tell you about the class?',

    '<span class="heb">וַיַּשְׁלַח</span> (III-ח/ע wayyiqtol) and '
    '<span class="heb">וַיַּקְרֵא</span> (III-א wayyiqtol) both have patach under the '
    'wayyiqtol prefix. The difference is in the final vowel. Explain what happens to the '
    'Hiphil tsere in each case and why.',

    'Compare <span class="heb">הוֹרֵד</span> (I-י imperative 2ms) and '
    '<span class="heb">הָקֵם</span> (Biconsonantal imperative 2ms). Both have a long prefix '
    'vowel rather than the patach of the strong Hiphil imperative. What prefix vowel does each '
    'use, and how can you tell them apart?',

    'Items 36–40 (Geminate) and items 31–35 (Biconsonantal) share nearly identical vowel '
    'patterns in every conjugation. What is the only reliable way to determine whether a '
    'Hiphil form belongs to the Geminate class or the Biconsonantal class?',
]


def _wfi_group_table(group_label: str, wclass: str, items: list) -> str:
    out = (
        f'<div class="section-label">{group_label}</div>'
        '<table><thead><tr>'
        '<th style="width:3%">#</th>'
        '<th style="width:12%">Form</th>'
        '<th style="width:12%">Reference</th>'
        '<th style="width:16%">Conjugation</th>'
        '<th style="width:9%">PGN</th>'
        '<th style="width:10%">Root</th>'
        '<th style="width:3%"></th>'
        '</tr></thead><tbody>'
    )
    for n, form, ref, conj, pgn, root, note in items:
        rid = f'r{n}'
        out += (
            f'<tr>'
            f'<td>{n}</td>'
            f'<td><span class="heb">{form}</span></td>'
            f'<td>{ref}</td>'
            f'<td>{_sel(CONJS)}</td>'
            f'<td>{_sel(PGNS)}</td>'
            f'<td>{_inp("root…", rtl=True)}</td>'
            f'<td><button class="rev-btn" onclick="toggle(\'{rid}\')">&#9654;</button></td>'
            f'</tr>'
            f'<tr class="ans-row" id="{rid}">'
            f'<td></td>'
            f'<td><span class="heb">{form}</span></td>'
            f'<td>{ref}</td>'
            f'<td><strong>{conj}</strong></td>'
            f'<td><strong>{pgn}</strong></td>'
            f'<td style="direction:rtl;unicode-bidi:embed;"><strong>{root}</strong></td>'
            f'<td><em style="color:#555;font-size:.8em;">{note}</em></td>'
            f'</tr>'
        )
    out += '</tbody></table>'
    return out


def _wfi_b_table() -> str:
    out = (
        '<table><thead><tr>'
        '<th style="width:3%">#</th>'
        '<th style="width:11%">Form</th>'
        '<th style="width:11%">Reference</th>'
        '<th style="width:19%">Context</th>'
        '<th style="width:12%">Weak Class</th>'
        '<th style="width:13%">Conjugation</th>'
        '<th style="width:8%">PGN</th>'
        '<th style="width:9%">Root</th>'
        '<th style="width:4%"></th>'
        '</tr></thead><tbody>'
    )
    for n, form, ref, ctx, wclass, conj, pgn, root, note in _WFI_B:
        rid = f'rb{n}'
        out += (
            f'<tr>'
            f'<td>{n}</td>'
            f'<td><span class="heb">{form}</span></td>'
            f'<td>{ref}</td>'
            f'<td>"{ctx}"</td>'
            f'<td>{_sel(CLASSES)}</td>'
            f'<td>{_sel(CONJS)}</td>'
            f'<td>{_sel(PGNS)}</td>'
            f'<td>{_inp("root…", rtl=True)}</td>'
            f'<td><button class="rev-btn" onclick="toggle(\'{rid}\')">&#9654;</button></td>'
            f'</tr>'
            f'<tr class="ans-row" id="{rid}">'
            f'<td></td>'
            f'<td><span class="heb">{form}</span></td>'
            f'<td>{ref}</td>'
            f'<td></td>'
            f'<td><strong>{wclass}</strong></td>'
            f'<td><strong>{conj}</strong></td>'
            f'<td><strong>{pgn}</strong></td>'
            f'<td style="direction:rtl;unicode-bidi:embed;"><strong>{root}</strong></td>'
            f'<td><em style="color:#555;font-size:.8em;">{note}</em></td>'
            f'</tr>'
        )
    out += '</tbody></table>'
    return out


def build_wfi_html() -> Path:
    body = (
        '<div class="note">'
        '<strong>All Part A forms are Hiphil.</strong> The weak class is given by the group '
        'heading — your task is to identify the conjugation, PGN, and root. '
        '<strong>Part B</strong> mixes classes — identify the weak class first, then parse.'
        '</div>'
        '<h2>Part A — By Class</h2>'
    )
    for group_label, wclass, items in _WFI_GROUPS:
        body += _wfi_group_table(group_label, wclass, items)
    body += '<h2>Part B — Mixed</h2>'
    body += _wfi_b_table()
    body += '<h2>Discussion Questions</h2><ol class="disc-q">'
    for q in _WFI_DISC:
        body += f'<li>{q}</li>'
    body += '</ol>'
    html = _wrap(
        'Chapter 27 — Hiphil Weak-Form Identification Drill',
        'BBH Chapter 27 · Hiphil Weak Verbs',
        body,
    )
    out = OUT_ROOT / 'ch27-weak-form-id' / 'ch27-weak-form-id.html'
    out.write_text(html, encoding='utf-8')
    print(f'  Saved {out}')
    return out


def build_wfi_md() -> Path:
    lines = [
        '# Chapter 27 — Hiphil Weak-Form Identification Drill',
        '',
        '*BBH Chapter 27 · Hiphil Weak Verbs*',
        '',
        '---',
        '',
        '## Instructions',
        '',
        '**Part A:** All forms are Hiphil. The weak class is given by the group heading. '
        'Identify the conjugation, PGN, and root.',
        '',
        '**Part B:** Weak class is unknown. Identify the class first, then parse.',
        '',
        '---',
        '',
        '## Part A — By Class',
        '',
    ]
    for group_label, wclass, items in _WFI_GROUPS:
        lines += [f'### {group_label}', '',
                  '| # | Form | Reference | Conjugation | PGN | Root |',
                  '|---|---|---|---|---|---|']
        for n, form, ref, conj, pgn, root, note in items:
            lines.append(f'| {n} | {form} | {ref} | | | |')
        lines.append('')

    lines += ['---', '', '## Part B — Mixed', '',
              '| # | Form | Reference | Context | Weak Class | Conj | PGN | Root |',
              '|---|---|---|---|---|---|---|---|']
    for n, form, ref, ctx, wclass, conj, pgn, root, note in _WFI_B:
        lines.append(f'| {n} | {form} | {ref} | "{ctx}" | | | | |')
    lines.append('')

    lines += ['---', '', '## Answer Key', '', '### Part A', '']
    for group_label, wclass, items in _WFI_GROUPS:
        lines += [f'**{group_label}** — all Hiphil {wclass}', '',
                  '| # | Form | Conjugation | PGN | Root | Note |',
                  '|---|---|---|---|---|---|']
        for n, form, ref, conj, pgn, root, note in items:
            note_short = note[:65] + '…' if len(note) > 65 else note
            lines.append(f'| {n} | {form} | {conj} | {pgn} | {root} | {note_short} |')
        lines.append('')

    lines += ['### Part B', '',
              '| # | Form | Weak Class | Conj | PGN | Root | Note |',
              '|---|---|---|---|---|---|---|']
    for n, form, ref, ctx, wclass, conj, pgn, root, note in _WFI_B:
        note_short = note[:65] + '…' if len(note) > 65 else note
        lines.append(f'| {n} | {form} | {wclass} | {conj} | {pgn} | {root} | {note_short} |')
    lines.append('')

    out = OUT_ROOT / 'ch27-weak-form-id' / 'ch27-weak-form-id.md'
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  Saved {out}')
    return out


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('Building ch27-biconsig-drill...')
    build_bg_html()
    build_bg_md()
    build_ch27_bg_drill_exercise()

    print('Building ch27-niphal-hiphil-contrast...')
    build_nhc_html()
    build_nhc_md()
    build_ch27_nh_contrast_exercise()

    print('Building ch27-weak-form-id...')
    build_wfi_html()
    build_wfi_md()
    build_ch27_weak_form_id_exercise()

    print('Done.')
