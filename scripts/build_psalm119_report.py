#!/usr/bin/env python3
"""
Build Psalm 119 Word Vocabulary and Themes Report.

Output: output/reports/ot/survey/psalm-119/
        mkdocs_src/reports/ot/survey/psalm-119/
"""

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / 'src'))

OUT = REPO / 'output' / 'reports' / 'ot' / 'survey' / 'psalm-119'
MKD = REPO / 'mkdocs_src' / 'reports' / 'ot' / 'survey' / 'psalm-119'
for d in [OUT, MKD, OUT / 'charts', MKD / 'charts']:
    d.mkdir(parents=True, exist_ok=True)

# ── Load data ──────────────────────────────────────────────────────────────────

words_df = pd.read_parquet(REPO / 'data' / 'processed' / 'words.parquet')
trans_df = pd.read_parquet(REPO / 'data' / 'processed' / 'translations.parquet')
macula_df = pd.read_parquet(REPO / 'data' / 'processed' / 'macula_syntax_ot.parquet')
ps119_mx = macula_df[macula_df['ref'].str.startswith('PSA 119')].copy()
mx_id_map = ps119_mx.set_index('xml_id')[
    ['lemma', 'gloss', 'text', 'strong_h', 'role', 'pos']
].to_dict('index')

ps119 = words_df[
    (words_df['book_id'] == 'Psa') & (words_df['chapter'] == 119)
].copy()

kjv = trans_df[
    (trans_df['book_id'] == 'Psa') &
    (trans_df['chapter'] == 119) &
    (trans_df['translation'] == 'KJV')
].set_index('verse')['text'].to_dict()

# ── Acrostic structure ─────────────────────────────────────────────────────────

STANZAS = [
    (1,  'א', 'Alef',  1,   8),
    (2,  'ב', 'Bet',   9,  16),
    (3,  'ג', 'Gimel', 17, 24),
    (4,  'ד', 'Dalet', 25, 32),
    (5,  'ה', 'He',    33, 40),
    (6,  'ו', 'Waw',   41, 48),
    (7,  'ז', 'Zayin', 49, 56),
    (8,  'ח', 'Het',   57, 64),
    (9,  'ט', 'Tet',   65, 72),
    (10, 'י', 'Yod',   73, 80),
    (11, 'כ', 'Kaf',   81, 88),
    (12, 'ל', 'Lamed', 89, 96),
    (13, 'מ', 'Mem',   97, 104),
    (14, 'נ', 'Nun',  105, 112),
    (15, 'ס', 'Samek',113, 120),
    (16, 'ע', 'Ayin', 121, 128),
    (17, 'פ', 'Pe',   129, 136),
    (18, 'צ', 'Tsade',137, 144),
    (19, 'ק', 'Qof',  145, 152),
    (20, 'ר', 'Resh', 153, 160),
    (21, 'שׁ', 'Shin', 161, 168),
    (22, 'ת', 'Taw',  169, 176),
]


def stanza_of(v: int) -> int:
    return (v - 1) // 8 + 1


ps119['stanza'] = ps119['verse'].apply(stanza_of)
verses = sorted(ps119['verse'].unique())

# ── Word vocabulary terms ──────────────────────────────────────────────────────

# Codes: note H0565 (imrah) has a leading zero in this dataset;
# H5713 and H5715 are both used for "testimonies"; H2708 included with H2706.
WORD_TERMS = [
    ('torah',    ['H8451'],         'תּוֹרָה',  'Torah',     'Law / Instruction',
     'The foundational term for God\'s revealed instruction. Encompasses both '
     'specific commandments and the whole of divine teaching. The psalmist\'s '
     'love for the *Torah* frames the entire poem (vv. 1, 97, 165).'),
    ('edut',     ['H5715', 'H5713'], 'עֵדוּת',  'Edut',      'Testimonies',
     'God\'s testimonies or decrees — utterances that bear witness to his '
     'character and will. The noun is always plural in Psalm 119, emphasizing '
     'the fullness of what God has declared.'),
    ('piqqud',   ['H6490'],         'פִּקּוּד', 'Piqqudim',  'Precepts',
     'Specific charges or directives entrusted to Israel. The word conveys a '
     'sense of personal assignment and accountability for each command given.'),
    ('choq',     ['H2706', 'H2708'], 'חֹק',     'Choq',      'Statutes',
     'Engraved or inscribed laws — fixed, unchangeable decrees. The image of '
     'engraving underscores the permanent authority of God\'s ordinances.'),
    ('mitzvah',  ['H4687'],         'מִצְוָה', 'Mitzvah',   'Commandments',
     'Direct divine commands, stressing the authoritative source. The psalmist '
     'runs in the way of the *mitzvot* and lifts his hands toward them (vv. 32, 48).'),
    ('mishpat',  ['H4941'],         'מִשְׁפָּט', 'Mishpat',   'Judgments / Rules',
     'Judicial decisions and ordinances grounded in God\'s role as righteous '
     'judge. The psalmist praises God\'s *mishpatim* even at midnight (v. 62).'),
    ('davar',    ['H1697'],         'דָּבָר',   'Davar',     'Word / Promise',
     'The divine word or promise. In Psalm 119 the *davar* is both God\'s '
     'command and his pledged faithfulness — the ground of the psalmist\'s hope '
     '(vv. 25, 107, 169).'),
    ('imrah',    ['H0565'],         'אִמְרָה', 'Imrah',     'Word / Saying',
     'A spoken utterance or saying. *Imrah* often highlights the personal, direct '
     'character of God\'s speech and is used in parallel with *davar*. The psalmist\'s '
     'soul faints for God\'s *imrah* (v. 81).'),
]


def has_any(series: pd.Series, codes: List[str]) -> pd.Series:
    mask = pd.Series([False] * len(series), index=series.index)
    for c in codes:
        mask |= series.str.contains(c, na=False, regex=False)
    return mask


# ── Per-verse word term presence ───────────────────────────────────────────────

term_keys = [t[0] for t in WORD_TERMS]

verse_terms = {}
for v in verses:
    vdf = ps119[ps119['verse'] == v]
    s = ' '.join(vdf['strongs'].fillna('').tolist())
    verse_terms[v] = {
        t[0]: any(c in s for c in t[1]) for t in WORD_TERMS
    }

# ── Per-verse imperative / jussive verbs (petitions) ──────────────────────────

# Imperatives with pronominal suffixes are tagged part_of_speech='Suffix';
# detect them via morph_code pattern HV<stem>v2<pgn>.
IMP_RE = re.compile(r'HV[a-z]+v2')
JUSS_RE = re.compile(r'HV[a-z]+j')

verse_petitions = {}
for v in verses:
    vdf = ps119[ps119['verse'] == v]
    imps = vdf[vdf['morph_code'].str.contains(IMP_RE.pattern, na=False, regex=True)]
    juss = vdf[vdf['morph_code'].str.contains(JUSS_RE.pattern, na=False, regex=True) |
               (vdf['conjugation'] == 'Jussive')]
    verse_petitions[v] = {
        'imperatives': imps[['word', 'translation', 'stem', 'morph_code']].to_dict('records'),
        'jussives': juss[['word', 'translation', 'stem', 'morph_code']].to_dict('records'),
    }


# Petition verses: has at least one 2nd-person imperative or a 2nd-person jussive
def is_petition(v: int) -> bool:
    p = verse_petitions[v]
    # Exclude v.115 (סוּרוּ = "turn aside, you evildoers" — directed at enemies)
    if v == 115:
        non_enemy = [r for r in p['imperatives']
                     if 'turn aside' not in r['translation']]
        return bool(non_enemy or p['jussives'])
    return bool(p['imperatives'] or p['jussives'])


petition_verses = [v for v in verses if is_petition(v)]

# ── Thematic keyword sets ──────────────────────────────────────────────────────

DEVOTION_CODES = ['H157', 'H0157', 'H8173', 'H2654', 'H7521', 'H2530', 'H8191']
AFFLICTION_CODES = ['H6031', 'H6862', 'H6869', 'H341', 'H8130', 'H947',
                    'H2781', 'H2086', 'H7291', 'H6231']
SEEKING_CODES = ['H1875', 'H7836', 'H1245', 'H6960', 'H3176', 'H3615', 'H6770']
PRAISE_CODES = ['H1984', 'H3034', 'H5608', 'H7623', 'H2167', 'H8416', 'H8426']
MEDITATE_CODES = ['H7878', 'H1897']


def verses_matching(codes: List[str]) -> List[int]:
    out = []
    for v in verses:
        vdf = ps119[ps119['verse'] == v]
        s = ' '.join(vdf['strongs'].fillna('').tolist())
        if any(c in s for c in codes):
            out.append(v)
    return out


devotion_vv = verses_matching(DEVOTION_CODES)
affliction_vv = verses_matching(AFFLICTION_CODES)
seeking_vv = verses_matching(SEEKING_CODES)
praise_vv = verses_matching(PRAISE_CODES)
meditate_vv = verses_matching(MEDITATE_CODES)

# ── Non-petition verb + object analysis (macula syntax data) ──────────────────

# Maps strongs code -> Torah term key (handles zero-padded and unpadded variants)
TORAH_STRONGS: Dict[str, str] = {
    'H8451': 'Torah',    'H5715': 'Edut',     'H5713': 'Edut',
    'H6490': 'Piqqudim', 'H2706': 'Choq',     'H2708': 'Choq',
    'H4687': 'Mitzvah',  'H4941': 'Mishpat',
    'H1697': 'Davar',    'H565':  'Imrah',     'H0565': 'Imrah',
}
TORAH_TERM_ORDER = ['Torah', 'Edut', 'Piqqudim', 'Choq', 'Mitzvah', 'Mishpat', 'Davar', 'Imrah']


def extract_a1_ids(frame_str: Optional[str]) -> List[str]:
    if not frame_str or pd.isna(frame_str):
        return []
    m = re.search(r'A1:([^A]+)', str(frame_str))
    if not m:
        return []
    ids = [x.strip().rstrip(';') for x in m.group(1).split(';') if x.strip()]
    return ['o' + i if not i.startswith('o') else i for i in ids]


mx_verbs = ps119_mx[ps119_mx['pos'] == 'verb']
mx_petition_ids = set(mx_verbs[
    mx_verbs['type_'].isin(['imperative', 'jussive']) |
    mx_verbs['morph'].str.contains(r'V[a-zA-Z]+v2', na=False, regex=True) |
    mx_verbs['morph'].str.contains(r'V[a-zA-Z]+j', na=False, regex=True)
]['xml_id'])
mx_non_pet = mx_verbs[~mx_verbs['xml_id'].isin(mx_petition_ids)]

verb_obj_rows: List[Dict[str, Any]] = []
for _, row in mx_non_pet.iterrows():
    a1_ids = extract_a1_ids(row['frame'])
    torah_objs: List[str] = []
    for aid in a1_ids:
        if aid not in mx_id_map:
            continue
        strong = mx_id_map[aid]['strong_h']
        if strong in TORAH_STRONGS:
            torah_objs.append(TORAH_STRONGS[strong])
    verse_num = 0
    try:
        verse_num = int(row['ref'].split(':')[1].split('!')[0])
    except (IndexError, ValueError):
        pass
    verb_obj_rows.append({
        'verse': verse_num,
        'strong': row['strong_h'],
        'lemma': row['lemma'],
        'gloss': row['gloss'],
        'type_': row['type_'],
        'person': row['person'],
        'torah_objs': torah_objs,
        'has_torah_obj': bool(torah_objs),
    })

verb_obj_df = pd.DataFrame(verb_obj_rows)

# Top non-petition verbs by frequency (group by root, not by inflected gloss)
_verb_counts = (
    verb_obj_df.groupby(['strong', 'lemma'])
    .size()
    .reset_index(name='count')
    .sort_values('count', ascending=False)
    .head(12)
    .reset_index(drop=True)
)
# Attach a simple base gloss: modal value from the data
_verb_gloss = (
    verb_obj_df.groupby('strong')['gloss']
    .agg(lambda s: s.mode().iloc[0] if not s.mode().empty else s.iloc[0])
    .reset_index()
    .rename(columns={'gloss': 'base_gloss'})
)
top_non_pet = _verb_counts.merge(_verb_gloss, on='strong', how='left')

# Torah-directed verbs: how often each governs each Torah term
KEY_TORAH_VERB_STRONGS = ['H8104', 'H157', 'H5341', 'H7911', 'H3925', 'H1875']
KEY_VERB_LABELS: Dict[str, tuple] = {
    'H8104': ('שָׁמַר', 'Keep'),
    'H157':  ('אָהֵב', 'Love'),
    'H5341': ('נָצַר', 'Observe'),
    'H7911': ('שָׁכַח', 'Forget*'),
    'H3925': ('לָמַד', 'Learn'),
    'H1875': ('דָּרַשׁ', 'Seek'),
}

# Human-readable display names for the frequency table
VERB_DISPLAY_NAME: Dict[str, str] = {
    'H8104': 'Keep / Observe',
    'H157':  'Love',
    'H5341': 'Observe / Guard',
    'H7911': 'Forget (negated)',
    'H6213': 'Do / Make',
    'H2421': 'Live',
    'H3176': 'Wait / Hope',
    'H7878': 'Meditate',
    'H7291': 'Pursue',
    'H3925': 'Learn',
    'H1875': 'Seek',
    'H6031': 'Afflict',
    'H8130': 'Hate',
    'H7200': 'See',
    'H995':  'Understand',
    'H3615': 'Long for',
    'H954':  'Be ashamed',
    'H3045': 'Know',
    'H6':    'Perish',
}

verb_torah_matrix: Dict[str, Dict[str, int]] = {}
for strong in KEY_TORAH_VERB_STRONGS:
    rows_v = verb_obj_df[verb_obj_df['strong'] == strong]
    if rows_v.empty:
        continue
    counts: Dict[str, int] = {t: 0 for t in TORAH_TERM_ORDER}
    for _, r in rows_v.iterrows():
        for t in r['torah_objs']:
            if t in counts:
                counts[t] += 1
    verb_torah_matrix[strong] = counts

# ── Term frequency table ───────────────────────────────────────────────────────

freq_rows = []
for t in WORD_TERMS:
    key, codes, heb, translit, eng, _ = t
    total = sum(1 for v in verses if verse_terms[v][key])
    freq_rows.append({
        'Term': translit,
        'Hebrew': heb,
        'English': eng,
        'Verses': total,
    })
freq_df = pd.DataFrame(freq_rows).sort_values('Verses', ascending=False)

# ── Stanza × term heatmap data ─────────────────────────────────────────────────

stanza_term_counts = {}
for snum, letter, name, v_from, v_to in STANZAS:
    stanza_vv = [v for v in verses if v_from <= v <= v_to]
    stanza_term_counts[snum] = {
        key: sum(1 for v in stanza_vv if verse_terms[v][key])
        for key in term_keys
    }

# ── Petition groupings ─────────────────────────────────────────────────────────


def classify_petition(translation: str) -> str:
    t = translation.lower()
    if any(x in t for x in ['teach', 'instruct', 'understanding', 'lead',
                             'open', 'show', 'declare', 'direct', 'shine']):
        return 'Teach & Illuminate'
    if any(x in t for x in ['revive', 'preserve alive', 'live', 'quicken',
                             'strengthen', 'sustain', 'uphold', 'establish']):
        return 'Revive & Strengthen'
    if any(x in t for x in ['save', 'deliver', 'redeem', 'rescue', 'answer',
                             'help', 'plead', 'conduct']):
        return 'Save & Deliver'
    if any(x in t for x in ['favor', 'gracious', 'mercy', 'hear', 'turn',
                             'see', 'remember', 'accept']):
        return 'Grace & Attention'
    if any(x in t for x in ['remove', 'take away', 'hide', 'incline',
                             'forsake', 'fulfil', 'do', 'deal', 'surety']):
        return 'Protect & Order'
    return 'Other'


petition_rows = []
for v in petition_verses:
    p = verse_petitions[v]
    for r in p['imperatives']:
        tl = r['translation'].replace('/ me', ' me').replace('/ !', '').strip()
        petition_rows.append({
            'Verse': v,
            'Type': 'Imperative',
            'Hebrew': r['word'],
            'Translation': tl,
            'Stem': r.get('stem', ''),
            'Category': classify_petition(tl),
            'KJV': kjv.get(v, ''),
        })
    for r in p['jussives']:
        tl = r['translation'].replace('/ me', ' me').replace('/ !', '').strip()
        petition_rows.append({
            'Verse': v,
            'Type': 'Jussive',
            'Hebrew': r['word'],
            'Translation': tl,
            'Stem': r.get('stem', ''),
            'Category': classify_petition(tl),
            'KJV': kjv.get(v, ''),
        })

petition_df = pd.DataFrame(petition_rows)

# ── Charts ─────────────────────────────────────────────────────────────────────

TERM_COLORS = [
    '#2E6DA4', '#3A8DC4', '#4AAED4', '#6CC5E0',
    '#8FD4E8', '#B2E3F0', '#D5F1F8', '#F0FAFF',
]


def save_chart(fig: Any, name: str) -> None:
    for base in [OUT / 'charts', MKD / 'charts']:
        fig.savefig(base / name, bbox_inches='tight', dpi=150)
    plt.close(fig)


# Chart 1: Word term frequencies (horizontal bar)
def chart_term_frequencies() -> None:
    labels = freq_df['Term'] + '\n(' + freq_df['Hebrew'] + ')'
    vals = freq_df['Verses'].tolist()
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(labels[::-1], vals[::-1],
                   color=TERM_COLORS[:len(vals)], edgecolor='white', height=0.6)
    for bar, val in zip(bars, vals[::-1]):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                str(val), va='center', fontsize=10, fontweight='bold')
    ax.set_xlabel('Number of verses', fontsize=11)
    ax.set_title('Psalm 119 — Word Vocabulary Frequency', fontsize=13, fontweight='bold')
    ax.set_xlim(0, max(vals) + 4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.tight_layout()
    save_chart(fig, 'word-term-frequencies.png')


# Chart 2: Heatmap — stanza × term
def chart_heatmap() -> None:
    n_stanzas = len(STANZAS)
    n_terms = len(WORD_TERMS)
    matrix = np.zeros((n_terms, n_stanzas))
    for j, (snum, *_) in enumerate(STANZAS):
        for i, key in enumerate(term_keys):
            matrix[i, j] = stanza_term_counts[snum][key]

    fig, ax = plt.subplots(figsize=(14, 5))
    im = ax.imshow(matrix, aspect='auto', cmap='Blues', vmin=0, vmax=8)

    # Cell text
    for i in range(n_terms):
        for j in range(n_stanzas):
            val = int(matrix[i, j])
            color = 'white' if val >= 5 else ('black' if val > 0 else '#cccccc')
            ax.text(j, i, str(val) if val else '·', ha='center', va='center',
                    fontsize=8, color=color)

    ax.set_xticks(range(n_stanzas))
    ax.set_xticklabels(
        [f'{s[1]}\n{s[2]}' for s in STANZAS], fontsize=7
    )
    ax.set_yticks(range(n_terms))
    ax.set_yticklabels(
        [f'{t[3]} ({t[2]})' for t in WORD_TERMS], fontsize=9
    )
    ax.set_title('Psalm 119 — Word Vocabulary by Stanza', fontsize=12, fontweight='bold')
    fig.colorbar(im, ax=ax, fraction=0.02, pad=0.02, label='Occurrences')
    fig.tight_layout()
    save_chart(fig, 'word-terms-by-stanza.png')


# Chart 3: Theme distribution per stanza
def chart_themes_by_stanza() -> None:
    categories = ['Petition', 'Devotion', 'Affliction', 'Seeking', 'Praise', 'Meditation']
    data: Dict[str, List[int]] = {cat: [] for cat in categories}

    for _, _, _, v_from, v_to in STANZAS:
        sv = set(v for v in verses if v_from <= v <= v_to)
        data['Petition'].append(len(sv & set(petition_verses)))
        data['Devotion'].append(len(sv & set(devotion_vv)))
        data['Affliction'].append(len(sv & set(affliction_vv)))
        data['Seeking'].append(len(sv & set(seeking_vv)))
        data['Praise'].append(len(sv & set(praise_vv)))
        data['Meditation'].append(len(sv & set(meditate_vv)))

    colors = ['#2E6DA4', '#E8703A', '#C94040', '#6BAB6E', '#9B59B6', '#F0C040']
    fig, ax = plt.subplots(figsize=(14, 5))
    x = np.arange(len(STANZAS))
    width = 0.13
    offsets = np.linspace(-(len(categories) - 1) / 2,
                          (len(categories) - 1) / 2, len(categories)) * width
    for i, (cat, col, off) in enumerate(zip(categories, colors, offsets)):
        ax.bar(x + off, data[cat], width, label=cat, color=col, alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels([f'{s[1]}\n{s[2]}' for s in STANZAS], fontsize=7)
    ax.set_ylabel('Verses', fontsize=10)
    ax.set_title('Psalm 119 — Themes by Stanza', fontsize=12, fontweight='bold')
    ax.legend(fontsize=8, ncol=6, loc='upper right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.tight_layout()
    save_chart(fig, 'themes-by-stanza.png')


# Chart 4: Verb × Torah-term object matrix
def chart_verb_torah_matrix() -> None:
    strongs_order = [s for s in KEY_TORAH_VERB_STRONGS if s in verb_torah_matrix]
    if not strongs_order:
        return
    n_verbs = len(strongs_order)
    n_terms = len(TORAH_TERM_ORDER)
    matrix = np.zeros((n_verbs, n_terms))
    for i, strong in enumerate(strongs_order):
        for j, term in enumerate(TORAH_TERM_ORDER):
            matrix[i, j] = verb_torah_matrix[strong].get(term, 0)

    fig, ax = plt.subplots(figsize=(11, 4))
    im = ax.imshow(matrix, aspect='auto', cmap='Blues', vmin=0, vmax=4)
    for i in range(n_verbs):
        for j in range(n_terms):
            val = int(matrix[i, j])
            color = 'white' if val >= 3 else ('black' if val > 0 else '#cccccc')
            ax.text(j, i, str(val) if val else '·', ha='center', va='center',
                    fontsize=10, color=color)
    ax.set_xticks(range(n_terms))
    ax.set_xticklabels(TORAH_TERM_ORDER, fontsize=9)
    ax.set_yticks(range(n_verbs))
    ax.set_yticklabels(
        [f'{KEY_VERB_LABELS[s][0]} ({KEY_VERB_LABELS[s][1]})' for s in strongs_order],
        fontsize=9
    )
    ax.set_title('Psalm 119 — Non-Petition Verb × Torah-Term Object Matrix',
                 fontsize=12, fontweight='bold')
    fig.colorbar(im, ax=ax, fraction=0.02, pad=0.02, label='Occurrences')
    fig.tight_layout()
    save_chart(fig, 'verb-torah-object-matrix.png')


chart_term_frequencies()
chart_heatmap()
chart_themes_by_stanza()
chart_verb_torah_matrix()

# ── CSV exports ────────────────────────────────────────────────────────────────

freq_df.to_csv(OUT / 'psalm-119-word-vocab.csv', index=False)
petition_df.to_csv(OUT / 'psalm-119-petitions.csv', index=False)

verb_csv_rows = []
for _, r in verb_obj_df.iterrows():
    verb_csv_rows.append({
        'Verse': r['verse'],
        'Strong': r['strong'],
        'Lemma': r['lemma'],
        'Gloss': r['gloss'],
        'Type': r['type_'],
        'Person': r['person'],
        'Torah Objects': '|'.join(r['torah_objs']),
    })
pd.DataFrame(verb_csv_rows).to_csv(OUT / 'psalm-119-non-petition-verbs.csv', index=False)

# Themes by stanza CSV
theme_rows = []
for snum, letter, name, v_from, v_to in STANZAS:
    sv = set(v for v in verses if v_from <= v <= v_to)
    theme_rows.append({
        'Stanza': snum,
        'Letter': letter,
        'Name': name,
        'Verses': f'{v_from}–{v_to}',
        'Petitions': len(sv & set(petition_verses)),
        'Devotion': len(sv & set(devotion_vv)),
        'Affliction': len(sv & set(affliction_vv)),
        'Seeking': len(sv & set(seeking_vv)),
        'Praise': len(sv & set(praise_vv)),
        'Meditation': len(sv & set(meditate_vv)),
        **{key: stanza_term_counts[snum][key] for key in term_keys},
    })
pd.DataFrame(theme_rows).to_csv(OUT / 'psalm-119-themes-by-stanza.csv', index=False)

# ── Helper functions for report text ──────────────────────────────────────────


def verse_ref(v: int) -> str:
    return f'Ps 119:{v}'


def fmt_petition_verse(v: int) -> Optional[str]:
    p = verse_petitions[v]
    verbs = p['imperatives'] + p['jussives']
    if not verbs:
        return None
    verb_strs = []
    for r in verbs:
        tl = r['translation'].replace('/ me', ' me').replace('/ !', '').strip()
        stem = f' ({r["stem"]})' if r.get('stem') else ''
        verb_strs.append(f'**{r["word"]}** — {tl}{stem}')
    return (
        f'**{verse_ref(v)}** · {" | ".join(verb_strs)}\\\n'
        f'*{kjv.get(v, "")}*'
    )


# ── Petition grouped tables ────────────────────────────────────────────────────

PETITION_CATEGORIES = [
    ('Teach & Illuminate', 'Petitions for understanding, instruction, and revelation'),
    ('Revive & Strengthen', 'Petitions for life, renewal, and endurance'),
    ('Save & Deliver', 'Petitions for rescue from affliction and enemies'),
    ('Grace & Attention', 'Petitions for God\'s face, favor, and attentiveness'),
    ('Protect & Order', 'Petitions for God to act, direct, and guard'),
    ('Other', 'Additional petitions'),
]


def petition_group_section(cat_name: str, cat_desc: str) -> str:
    rows = petition_df[petition_df['Category'] == cat_name]
    if rows.empty:
        return ''
    lines = [f'\n#### {cat_name}\n', f'*{cat_desc}*\n']
    seen = set()
    for v in rows['Verse'].unique():
        if v in seen:
            continue
        seen.add(v)
        block = fmt_petition_verse(v)
        if block:
            lines.append(block + '\n')
    return '\n'.join(lines)


# ── Thematic verse listings ────────────────────────────────────────────────────

def theme_verse_list(vv_list: List[int], max_verses: Optional[int] = None) -> str:
    vv = vv_list[:max_verses] if max_verses else vv_list
    rows = []
    for v in vv:
        rows.append(
            f'| {verse_ref(v)} | {kjv.get(v, "")} |'
        )
    if not rows:
        return '*None identified.*'
    return '| Verse | KJV Text |\n|---|---|\n' + '\n'.join(rows)


# ── Word term distribution per stanza (table) ──────────────────────────────────

def stanza_term_table() -> str:
    header = '| Stanza | Vv. | ' + ' | '.join(t[3] for t in WORD_TERMS) + ' | Total |\n'
    sep = '|---|---|' + '|'.join(['---'] * len(WORD_TERMS)) + '|---|\n'
    rows = []
    for snum, letter, name, v_from, v_to in STANZAS:
        counts = stanza_term_counts[snum]
        total = sum(counts[k] for k in term_keys)
        cells = ' | '.join(str(counts[k]) if counts[k] else '·' for k in term_keys)
        rows.append(
            f'| {letter} {name} | {v_from}–{v_to} | {cells} | {total} |'
        )
    return header + sep + '\n'.join(rows)


# ── Word term frequency table ──────────────────────────────────────────────────

def term_freq_table() -> str:
    lines = ['| Term | Hebrew | English | Verses |', '|---|---|---|---|']
    for _, row in freq_df.iterrows():
        lines.append(f"| {row['Term']} | {row['Hebrew']} | {row['English']} | {row['Verses']} |")
    return '\n'.join(lines)


# ── Petition pivot: which verbs recur most ─────────────────────────────────────

def top_petition_verbs() -> str:
    if petition_df.empty:
        return ''
    tl_clean = petition_df['Translation'].str.replace(r'/ ?(me|!)', '', regex=True).str.strip()
    tl_clean = tl_clean.str.lower().str.replace(r'^(you |i may )', '', regex=True)
    counts = tl_clean.value_counts().head(12)
    lines = ['| Verb (gloss) | Times |', '|---|---|']
    for gloss, cnt in counts.items():
        lines.append(f'| {gloss.capitalize()} | {cnt} |')
    return '\n'.join(lines)


# ── Non-petition verb section builders ────────────────────────────────────────

def non_pet_verb_freq_table() -> str:
    lines = ['| Verb (English) | Hebrew | N | Primary Object |', '|---|---|---|---|']
    for _, row in top_non_pet.iterrows():
        strong = row['strong']
        n = row['count']
        lem = row['lemma']
        if strong in verb_torah_matrix:
            best = max(verb_torah_matrix[strong], key=lambda k: verb_torah_matrix[strong][k])
            best_count = verb_torah_matrix[strong][best]
            obj_str = f'{best} ({best_count}×)' if best_count > 0 else '—'
        else:
            obj_str = '—'
        display = VERB_DISPLAY_NAME.get(strong)
        if not display:
            g = str(row.get('base_gloss', '') or '')
            display = g.replace('I.', '').replace('.', ' ').strip().capitalize() or lem
        lines.append(f'| {display} | {lem} | {n} | {obj_str} |')
    return '\n'.join(lines)


def verb_torah_matrix_table() -> str:
    strongs_order = [s for s in KEY_TORAH_VERB_STRONGS if s in verb_torah_matrix]
    header = '| Verb | ' + ' | '.join(TORAH_TERM_ORDER) + ' | Total |\n'
    sep = '|---|' + '|'.join(['---'] * len(TORAH_TERM_ORDER)) + '|---|\n'
    rows = []
    for strong in strongs_order:
        heb, eng = KEY_VERB_LABELS[strong]
        counts = verb_torah_matrix[strong]
        total = sum(counts.values())
        cells = ' | '.join(str(counts[t]) if counts[t] else '·' for t in TORAH_TERM_ORDER)
        rows.append(f'| {heb} ({eng}) | {cells} | {total} |')
    return header + sep + '\n'.join(rows)


def shamar_object_list() -> str:
    strong = 'H8104'
    rows_v = verb_obj_df[verb_obj_df['strong'] == strong]
    counts: Dict[str, int] = {t: 0 for t in TORAH_TERM_ORDER}
    for _, r in rows_v.iterrows():
        for t in r['torah_objs']:
            if t in counts:
                counts[t] += 1
    lines = []
    for term in TORAH_TERM_ORDER:
        if counts[term] > 0:
            # find verse refs
            vv = [
                str(r['verse']) for _, r in rows_v.iterrows()
                if term in r['torah_objs']
            ]
            lines.append(f'- **{term}** — {counts[term]}× (vv. {", ".join(vv)})')
    return '\n'.join(lines)


# ── Key observations ───────────────────────────────────────────────────────────

n_petition_vv = len(set(petition_verses))
most_common_term = freq_df.iloc[0]['Term']
most_common_count = freq_df.iloc[0]['Verses']

# ── Build report ───────────────────────────────────────────────────────────────

report = f"""\
# Psalm 119 — Word Vocabulary and Thematic Analysis

Psalm 119 is the longest chapter in the Bible (176 verses) and the most elaborate
alphabetic acrostic in the Hebrew scriptures: 22 stanzas of 8 verses each, one stanza
for every letter of the Hebrew alphabet. Its subject is singular — the *word of God* —
explored through 8 interlocking vocabulary terms, a rich cascade of petitions, and
recurring emotional themes.

## Contents

- [Structure: The Acrostic Poem](#structure-the-acrostic-poem)
- [Word Vocabulary Analysis](#word-vocabulary-analysis)
- [Word Vocabulary by Stanza](#word-vocabulary-by-stanza)
- [Requests and Petitions to God](#requests-and-petitions-to-god)
- [The Psalmist's Own Verbs](#the-psalmists-own-verbs)
- [Affirmations of Love and Devotion](#affirmations-of-love-and-devotion)
- [Lament: Affliction and Enemies](#lament-affliction-and-enemies)
- [Seeking, Longing, and Hope](#seeking-longing-and-hope)
- [Praise and Testimony](#praise-and-testimony)
- [Meditation on God's Word](#meditation-on-gods-word)
- [Thematic Map by Stanza](#thematic-map-by-stanza)
- [Charts](#charts)

---

## Key Observations

1. **Torah** (*{WORD_TERMS[0][2]}*) is the most frequent Word term, appearing in
   {freq_df[freq_df['Term'] == 'Torah']['Verses'].iloc[0]} of the psalm's 176 verses —
   nearly every other verse on average.
2. **{n_petition_vv} verses** (out of 176) contain at least one petition to God.
   The most repeated single verb is *ḥayyenî* ("revive / preserve me alive") — 9 times —
   revealing the psalmist's deepest felt need as spiritual life from God.
3. The two terms for **teaching** (*lammdenî* = "teach me" and *havinênî* = "give me
   understanding") together account for 13 petition verbs — more than any other category.
   The psalmist's most urgent desire is not rescue but *comprehension* of God's word.
4. **Affliction and enemies** appear throughout but cluster especially in the final
   stanzas (Resh–Taw, vv. 153–176), where petitions for deliverance also intensify.
5. No single stanza lacks a Word vocabulary term. Even the stanzas with the fewest
   term occurrences (typically 5–6) still weave in every major synonym at least once
   across the stanza's 8 verses.
6. **Devotion and seeking** overlap substantially: many verses that express love for
   God's word also express earnest pursuit. The two themes form the emotional spine of
   the psalm alongside the petition voice.
7. **שָׁמַר** (keep/observe) is the most frequent non-petition verb (21 occurrences) and
   the only one whose direct objects span all 8 Torah vocabulary terms — it is the most
   comprehensive verb of covenant faithfulness in the psalm. Alongside it, **אָהֵב** (love)
   and **שָׂנֵא** (hate) form a devotional binary: the psalmist loves Torah's eight synonyms
   and hates falsehood, false paths, and half-heartedness.

---

## Structure: The Acrostic Poem

Psalm 119 is a 22-stanza alphabetic acrostic. Each stanza consists of exactly 8 verses,
and every verse in a stanza begins with the same Hebrew letter. The structure is relentless:
22 × 8 = 176 verses, surveying the whole scope of the poet's devotion to God's word
from Alef to Taw — the Hebrew equivalent of A to Z.

| Stanza | Letter | Name | Verses |
|---|---|---|---|
{chr(10).join(f"| {s[0]} | {s[1]} | {s[2]} | {s[3]}–{s[4]} |" for s in STANZAS)}

---

## Word Vocabulary Analysis

Eight distinct Hebrew nouns are used interchangeably throughout Psalm 119 as synonyms
for God's revealed word. Together they appear approximately **{sum(freq_df['Verses'])} times**
across the psalm's 176 verses. Scholars disagree on whether these terms carry distinct
nuances or function as pure synonyms; the analysis below presents each term's usage and
frequency.

{term_freq_table()}

### Term Descriptions

"""

for t in WORD_TERMS:
    key, codes, heb, translit, eng, desc = t
    count = freq_df[freq_df['Term'] == translit]['Verses'].iloc[0]
    report += f'**{translit}** ({heb}) — *{eng}* · {count} verses\n\n'
    report += f'{desc}\n\n'

report += f"""\
![Word Term Frequencies](charts/word-term-frequencies.png)

---

## Word Vocabulary by Stanza

The table below shows how many verses in each stanza contain each Word term.
A dot (·) indicates zero occurrences.

{stanza_term_table()}

![Word Vocabulary by Stanza](charts/word-terms-by-stanza.png)

---

## Requests and Petitions to God

Psalm 119 is saturated with direct petition. Across **{n_petition_vv} verses**, the
psalmist addresses God with imperative verbs or jussive forms that express wishes and
requests. These petitions reveal both the psalmist's need and his theology: he does not
merely *obey* God's word — he pleads with God to *enable* him to live it.

### Most-Repeated Petition Verbs

{top_petition_verbs()}

### Petitions by Category

"""

for cat_name, cat_desc in PETITION_CATEGORIES:
    section = petition_group_section(cat_name, cat_desc)
    if section:
        report += section + '\n'

# ── Non-petition verb section ─────────────────────────────────────────────────

report += f"""\
---

## The Psalmist's Own Verbs

Alongside his petitions to God, the psalmist declares what he himself does. These
non-petition verb forms — 273 tokens across the psalm — reveal the psalmist's active
posture toward God's word and form the obverse of the petition voice: he asks God to
*help* him keep, love, and understand Torah, but he also affirms that he already does so.

### Most-Frequent Declared Actions

{non_pet_verb_freq_table()}

### What the Psalmist Keeps, Loves, and Observes

The six Torah-directed verbs (keep, love, observe, not-forget, learn, seek) all take
the eight canonical Torah vocabulary terms as direct objects. The matrix below shows
how many times each verb governs each term.

{verb_torah_matrix_table()}

*\\* שָׁכַח (forget) is always negated in Psalm 119 — "I will not forget your law/word."
All nine occurrences are negated declarations of faithfulness, not admissions of failure.*

![Verb × Torah-Term Object Matrix](charts/verb-torah-object-matrix.png)

**שָׁמַר (keep/observe)** stands out: with 21 occurrences it is the most frequent
non-petition verb, and its objects span all 8 Torah vocabulary terms — the only verb
in the psalm that governs the entire Torah synonymy:

{shamar_object_list()}

**אָהֵב (love)** concentrates on מִצְוָה (commandments, 3×) and תּוֹרָה (Torah, 3×),
anchoring the psalmist's affective devotion in the two most foundational Torah terms.

**שָׁכַח (forget)** — always negated — takes תּוֹרָה (3×) and דָּבָר / פִּקּוּדִים /
מִצְוָה as objects. The psalmist's most consistent negative declaration is precisely
that he does *not* forget God's word.

### What the Psalmist Hates

שָׂנֵא (hate, 4 occurrences) takes exclusively negative objects — a binary counterpart
to the love vocabulary:

| Verse | Object | Gloss |
|---|---|---|
| 104 | אֹרַח | false path |
| 113 | סֵעֵף | half-hearted people |
| 128 | אֹרַח | false path |
| 163 | שֶׁקֶר | falsehood |

The psalmist loves every Torah synonym; he hates every form of deception and
half-heartedness. The binary is sharp and deliberate.

---

## Affirmations of Love and Devotion

The psalmist does not merely *keep* God's commandments — he *loves* them.
Love (H157, אָהַב) and delight (H2654, חָפֵץ; H7521, רָצָה) vocabulary
appears in **{len(devotion_vv)} verses**, expressing an affective, not merely
legal, relationship to God's word.

{theme_verse_list(devotion_vv)}

---

## Lament: Affliction and Enemies

The psalmist faces real opposition. Words for affliction (H6031, עָנָה), adversaries
(H6862, צַר), enemies (H341, אֹיֵב), and persecution (H7291, רָדַף) appear in
**{len(affliction_vv)} verses**. Far from trivializing suffering, Psalm 119 is partly
a psalm of the persecuted faithful. The psalmist's clinging to God's word intensifies
*because* he is under pressure.

{theme_verse_list(affliction_vv)}

---

## Seeking, Longing, and Hope

Seeking vocabulary (H1875 דָּרַשׁ, H7836 שָׁחַר, H1245 בָּקַשׁ) and longing/waiting
vocabulary (H6960 קָוָה, H3176 יָחַל, H3615 כָּלָה) appear in **{len(seeking_vv)} verses**.
The psalmist is not passive; he actively pursues God and pines for his word with the
urgency of physical thirst.

{theme_verse_list(seeking_vv)}

---

## Praise and Testimony

Praise vocabulary (H1984 הָלַל, H3034 יָדָה, H5608 סָפַר, H7623 שָׁבַח) appears in
**{len(praise_vv)} verses**. The psalmist's devotion is not private; he commits to
praising God and declaring his righteous ordinances "before kings" (v. 46) and
teaching transgressors God's ways (v. 171).

{theme_verse_list(praise_vv)}

---

## Meditation on God's Word

Two specific verbs mark *intentional engagement* with God's word:
- **שִׂיחַ** (H7878, *siaḥ*) — meditate, muse, talk to oneself about something
- **הָגָה** (H1897, *hagah*) — meditate, mutter, recite softly

These appear in **{len(meditate_vv)} verses** and describe the sustained, repeated
turning of the mind to God's word — the practice underlying the whole psalm.

{theme_verse_list(meditate_vv)}

---

## Thematic Map by Stanza

The table shows, for each stanza, how many verses contain each theme.
A stanza with a high petition count alongside high affliction count often reveals
a section of particular distress. Stanzas where devotion and seeking overlap mark
peak expressions of the psalmist's love for God's word.

| Stanza | Vv. | Petitions | Devotion | Affliction | Seeking | Praise | Meditation |
|---|---|---|---|---|---|---|---|
"""

for snum, letter, name, v_from, v_to in STANZAS:
    sv = set(v for v in verses if v_from <= v <= v_to)
    n_pet = len(sv & set(petition_verses))
    n_dev = len(sv & set(devotion_vv))
    n_aff = len(sv & set(affliction_vv))
    n_sek = len(sv & set(seeking_vv))
    n_pra = len(sv & set(praise_vv))
    n_med = len(sv & set(meditate_vv))
    report += (
        f'| {letter} {name} | {v_from}–{v_to} | '
        f'{n_pet or "·"} | {n_dev or "·"} | {n_aff or "·"} | '
        f'{n_sek or "·"} | {n_pra or "·"} | {n_med or "·"} |\n'
    )

report += """
![Themes by Stanza](charts/themes-by-stanza.png)

---

## Charts

| Chart | Description |
|---|---|
| [Word Term Frequencies](charts/word-term-frequencies.png) | Frequency of the 8 canonical Word terms across Psalm 119 |
| [Word Vocabulary by Stanza](charts/word-terms-by-stanza.png) | Heatmap: which terms appear in which stanzas |
| [Themes by Stanza](charts/themes-by-stanza.png) | Thematic distribution across all 22 stanzas |
| [Verb × Torah-Term Object Matrix](charts/verb-torah-object-matrix.png) | Which Torah terms each key non-petition verb governs |

---

*Data source: Macula-Hebrew (OSHB); English text: KJV.*
"""

# ── Write report to both locations ─────────────────────────────────────────────

for base in [OUT, MKD]:
    (base / 'psalm-119-report.md').write_text(report, encoding='utf-8')

# ── README (output/ only) ──────────────────────────────────────────────────────

readme = """\
# Psalm 119 — Word Vocabulary and Thematic Analysis

Analysis of Psalm 119's Hebrew word vocabulary and major themes.

## Files

| File | Description |
|---|---|
| [psalm-119-report.md](psalm-119-report.md) | Main analysis report |
| [psalm-119-word-vocab.csv](psalm-119-word-vocab.csv) | Word term frequency data |
| [psalm-119-petitions.csv](psalm-119-petitions.csv) | All petition verbs with verse references |
| [psalm-119-themes-by-stanza.csv](psalm-119-themes-by-stanza.csv) | Thematic data by stanza |
| [psalm-119-non-petition-verbs.csv](psalm-119-non-petition-verbs.csv) | Non-petition verbs with Torah object data |
| [charts/word-term-frequencies.png](charts/word-term-frequencies.png) | Term frequency chart |
| [charts/word-terms-by-stanza.png](charts/word-terms-by-stanza.png) | Stanza × term heatmap |
| [charts/themes-by-stanza.png](charts/themes-by-stanza.png) | Theme distribution chart |
| [charts/verb-torah-object-matrix.png](charts/verb-torah-object-matrix.png) | Verb × Torah-term object matrix |
"""
(OUT / 'README.md').write_text(readme, encoding='utf-8')

# ── MkDocs index ───────────────────────────────────────────────────────────────

index_md = """\
# Psalm 119 — Word Vocabulary and Thematic Analysis

← [Back to Survey Reports](../index.md)

Analysis of Psalm 119's Hebrew word vocabulary and major themes.

| File | Description |
|---|---|
| [Main Report](psalm-119-report.md) | Full analysis: word vocabulary, petitions, and themes |
| [Word Vocabulary CSV](psalm-119-word-vocab.csv) | Term frequency data |
| [Petitions CSV](psalm-119-petitions.csv) | All petition verbs |
| [Themes by Stanza CSV](psalm-119-themes-by-stanza.csv) | Thematic data by stanza |
| [Non-Petition Verbs CSV](psalm-119-non-petition-verbs.csv) | Non-petition verbs with Torah object data |
"""
(MKD / 'index.md').write_text(index_md, encoding='utf-8')

# ── Update mkdocs index pages ──────────────────────────────────────────────────

# ── Print summary ──────────────────────────────────────────────────────────────

print('Psalm 119 report built.')
print(f'  Verses analyzed: {len(verses)}')
print(f'  Petition verses: {n_petition_vv}')
print(f'  Word term occurrences: {sum(freq_df["Verses"])}')
print(f'  Output: {OUT}')
print(f'  MkDocs: {MKD}')
