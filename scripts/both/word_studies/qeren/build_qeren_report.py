"""Build קָרַן / קֶרֶן (qaran/qeren) word-study report, charts, and CSV data."""
import matplotlib; matplotlib.use('Agg')  # noqa: E702
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from pathlib import Path
from bidi.algorithm import get_display
from bible_grammar.core.syntax_ot import load_syntax_ot
from bible_grammar.core.lxx_query import query_lxx
from bible_grammar.core.translations import load_translations

OUT = Path('output/reports/both/word_studies')
OUT.mkdir(parents=True, exist_ok=True)
CHART_DIR = Path('output/charts/both/word_studies')
CHART_DIR.mkdir(parents=True, exist_ok=True)

ot = load_syntax_ot()
lxx = query_lxx(include_deuterocanon=False)
trans = load_translations()
vul = trans[trans['translation'] == 'VulgClementine']
kjv = trans[trans['translation'] == 'KJV']

# ============================================================
# RAW DATA
# ============================================================

verb = ot[ot['strong_h'] == 'H7160'].copy()
noun = ot[ot['strong_h'] == 'H7161'].copy()

# Vulgate Psalms use LXX numbering (1 behind MT from Ps 10 onward).
# The VulgClementine dataset here uses MT numbering, but only has
# Psa, not 1Sa/2Sa/1Ki/2Ki/1Ch/2Ch (those books absent from dataset).


def vul_text(book, ch, vs):
    r = vul[(vul['book_id'] == book) & (vul['chapter'] == ch) & (vul['verse'] == vs)]
    return r['text'].values[0] if len(r) else ''


def kjv_text(book, ch, vs):
    r = kjv[(kjv['book_id'] == book) & (kjv['chapter'] == ch) & (kjv['verse'] == vs)]
    return r['text'].values[0] if len(r) else ''


# ============================================================
# CHART 1: Noun distribution by genre / book
# ============================================================

GENRE_MAP = {
    'Gen': 'Torah', 'Exo': 'Torah', 'Lev': 'Torah', 'Num': 'Torah', 'Deu': 'Torah',
    'Jos': 'Historical', 'Jdg': 'Historical', '1Sa': 'Historical', '2Sa': 'Historical',
    '1Ki': 'Historical', '2Ki': 'Historical', '1Ch': 'Historical', '2Ch': 'Historical',
    'Ezr': 'Historical', 'Neh': 'Historical',
    'Job': 'Wisdom', 'Psa': 'Psalms', 'Pro': 'Wisdom', 'Ecc': 'Wisdom',
    'Isa': 'Prophets', 'Jer': 'Prophets', 'Lam': 'Prophets', 'Ezk': 'Prophets',
    'Dan': 'Prophets', 'Hos': 'Prophets', 'Amo': 'Prophets', 'Mic': 'Prophets',
    'Nah': 'Prophets', 'Hab': 'Prophets', 'Zec': 'Prophets', 'Mal': 'Prophets',
}
GENRE_ORDER = ['Torah', 'Historical', 'Psalms', 'Wisdom', 'Prophets']
GENRE_COLORS = {
    'Torah': '#4292c6', 'Historical': '#fd8d3c',
    'Psalms': '#41ab5d', 'Wisdom': '#9e9ac8', 'Prophets': '#d62728',
}

noun_g = noun.copy()
noun_g['genre'] = noun_g['book'].map(GENRE_MAP).fillna('Other')
book_counts = noun_g.groupby(['book', 'genre']).size().reset_index(name='count')
genre_order_map = {g: i for i, g in enumerate(GENRE_ORDER)}
book_counts['gord'] = book_counts['genre'].map(genre_order_map).fillna(99)
book_counts = book_counts.sort_values(['gord', 'count'], ascending=[True, False])

# Semantic usage annotation for noun
SEMANTIC_MAP = {
    'Gen': 'literal / animal', 'Exo': 'literal / altar',
    'Lev': 'literal / altar', 'Deu': 'literal + power',
    'Jos': 'instrumental', '1Sa': 'power / strength',
    '2Sa': 'power / strength', '1Ki': 'literal + power',
    '1Ch': 'music / power', '2Ch': 'power',
    'Job': 'lament / humility', 'Psa': 'power / strength',
    'Isa': 'figurative', 'Jer': 'power / destruction',
    'Lam': 'power / destruction', 'Ezk': 'literal + power',
    'Dan': 'apocalyptic', 'Amo': 'literal / altar',
    'Mic': 'power', 'Hab': 'radiance',
    'Zec': 'vision',
}

fig1, axes1 = plt.subplots(1, 2, figsize=(15, 7))

ax1 = axes1[0]
bks = book_counts['book'].tolist()
cnts = book_counts['count'].tolist()
gnrs = book_counts['genre'].tolist()
clrs = [GENRE_COLORS.get(g, 'gray') for g in gnrs]
bars = ax1.barh(bks, cnts, color=clrs, edgecolor='white', linewidth=0.5)
for bar, v in zip(bars, cnts):
    ax1.text(bar.get_width() + 0.08, bar.get_y() + bar.get_height() / 2,
             str(v), va='center', fontsize=8.5)
ax1.set_xlabel('Occurrences', fontsize=10)
ax1.set_title(
    get_display('Noun קֶרֶן (H7161) — Distribution by book') + '\n(n=75)',
    fontsize=11, fontweight='bold')
ax1.xaxis.grid(True, linestyle='--', alpha=0.4)
ax1.set_axisbelow(True)
patches = [mpatches.Patch(color=c, label=g) for g, c in GENRE_COLORS.items()]
ax1.legend(handles=patches, loc='lower right', fontsize=8)

# Pie: by genre
ax2 = axes1[1]
genre_totals = noun_g.groupby('genre').size()
genre_totals = genre_totals.reindex(GENRE_ORDER).dropna()
wedge_colors = [GENRE_COLORS[g] for g in genre_totals.index]
wedges, texts, autotexts = ax2.pie(
    genre_totals.values,
    labels=genre_totals.index,
    autopct='%1.0f%%',
    startangle=140,
    colors=wedge_colors,
    explode=[0.04] * len(genre_totals),
    textprops={'fontsize': 9},
)
for at in autotexts:
    at.set_fontsize(9)
ax2.set_title('Distribution by genre (noun only)', fontsize=11, fontweight='bold')

fig1.tight_layout(pad=2.5)
chart1_path = CHART_DIR / 'qeren_noun_distribution.png'
fig1.savefig(chart1_path, dpi=150, bbox_inches='tight')
plt.close(fig1)
print(f"Chart 1 saved: {chart1_path}")

# ============================================================
# CHART 2: LXX translation equivalents
# ============================================================

LXX_STRONG_LABELS = {
    '2768': 'κέρας / κέρατα (keras)',
    '3588': 'τά (article only)',
    '3599': 'ὀδόντας (teeth)',
    '': 'no alignment',
}

# Combine verb and noun LXX data
all_qeren = pd.concat([verb, noun], ignore_index=True)
gk_counts: dict = {}
for gs in all_qeren['greekstrong']:
    label = LXX_STRONG_LABELS.get(str(gs).strip(), f'G{gs}')
    gk_counts[label] = gk_counts.get(label, 0) + 1

# Also add the δεδόξασται verb occurrences manually (G1392)
gk_counts['δοξάζω (glorify)'] = 3   # Exo 34:29,30,35 verb

fig2, ax3 = plt.subplots(figsize=(10, 4))
lxx_labels = sorted(gk_counts.keys(), key=lambda x: -gk_counts[x])
lxx_vals = [gk_counts[lbl] for lbl in lxx_labels]
lxx_colors = ['#2b8cbe', '#7bccc4', '#f0a500', '#c2e699', '#d62728', '#aaaaaa']
bars2 = ax3.bar(range(len(lxx_labels)), lxx_vals,
                color=lxx_colors[:len(lxx_labels)], edgecolor='white', linewidth=0.5)
ax3.set_xticks(range(len(lxx_labels)))
ax3.set_xticklabels(lxx_labels, fontsize=9.5)
ax3.set_ylabel('OT tokens', fontsize=10)
ax3.set_title(
    get_display('LXX translation of קֶרֶן / קָרַן') + '\n(noun + verb combined)',
    fontsize=11, fontweight='bold')
ax3.yaxis.grid(True, linestyle='--', alpha=0.4)
ax3.set_axisbelow(True)
for bar, v in zip(bars2, lxx_vals):
    ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.4,
             str(v), ha='center', fontsize=11, fontweight='bold')
fig2.tight_layout()
chart2_path = CHART_DIR / 'qeren_lxx_translations.png'
fig2.savefig(chart2_path, dpi=150, bbox_inches='tight')
plt.close(fig2)
print(f"Chart 2 saved: {chart2_path}")

# ============================================================
# CHART 3: Semantic usage of noun (literal vs. figurative)
# ============================================================

SEMANTIC_CATEGORIES = {
    # Literal physical horns (animals)
    'Gen 22:13': 'literal / animal',
    'Hab 3:4':   'literal / radiance',
    # Altar horns (tabernacle / temple)
    'Exo 27:2': 'literal / altar', 'Exo 29:12': 'literal / altar',
    'Exo 30:2': 'literal / altar', 'Exo 30:3': 'literal / altar',
    'Exo 30:10': 'literal / altar', 'Exo 37:25': 'literal / altar',
    'Exo 37:26': 'literal / altar', 'Exo 38:2': 'literal / altar',
    'Lev 4:7': 'literal / altar', 'Lev 4:18': 'literal / altar',
    'Lev 4:25': 'literal / altar', 'Lev 4:30': 'literal / altar',
    'Lev 4:34': 'literal / altar', 'Lev 8:15': 'literal / altar',
    'Lev 9:9': 'literal / altar', 'Lev 16:18': 'literal / altar',
    'Amo 3:14': 'literal / altar',
    'Jer 17:1': 'literal / altar',
    'Ezk 43:15': 'literal / altar', 'Ezk 43:20': 'literal / altar',
    # Object (anointing horn)
    '1Sa 16:1': 'literal / object', '1Sa 16:13': 'literal / object',
    '1Ki 1:39': 'literal / object',
    # Instrument (horn of Jubilee, battle)
    'Jos 6:5': 'literal / instrument',
    # Metaphorical: power / strength
    'Deu 33:17': 'figurative / power', '1Sa 2:1': 'figurative / power',
    '1Sa 2:10': 'figurative / power', '2Sa 22:3': 'figurative / power',
    '1Ki 22:11': 'figurative / power', '2Ch 18:10': 'figurative / power',
    'Psa 18:3': 'figurative / power', 'Psa 75:5': 'figurative / power',
    'Psa 75:6': 'figurative / power', 'Psa 75:11': 'figurative / power',
    'Psa 89:18': 'figurative / power', 'Psa 89:25': 'figurative / power',
    'Psa 92:11': 'figurative / power', 'Psa 112:9': 'figurative / power',
    'Psa 132:17': 'figurative / power', 'Psa 148:14': 'figurative / power',
    'Jer 48:25': 'figurative / power', 'Lam 2:3': 'figurative / power',
    'Lam 2:17': 'figurative / power', 'Ezk 29:21': 'figurative / power',
    'Mic 4:13': 'figurative / power', '1Ch 25:5': 'figurative / power',
    # Metaphorical: divine glory (Exo 34 verb — separate)
    # Animal literal (altar context but on animal)
    'Ezk 34:21': 'literal / animal',
    # Metaphorical: Psalm altar
    'Psa 118:27': 'literal / altar',
    # Isa 5:1 (hill)
    'Isa 5:1': 'figurative / place',
    # Job
    'Job 16:15': 'figurative / power',
    # Zechariah vision
    'Zec 2:1': 'apocalyptic', 'Zec 2:2': 'apocalyptic', 'Zec 2:4': 'apocalyptic',
    # Daniel visions
    'Dan 8:3': 'apocalyptic', 'Dan 8:5': 'apocalyptic', 'Dan 8:6': 'apocalyptic',
    'Dan 8:7': 'apocalyptic', 'Dan 8:8': 'apocalyptic', 'Dan 8:9': 'apocalyptic',
    'Dan 8:20': 'apocalyptic', 'Dan 8:21': 'apocalyptic',
    # Ezk 27:15 — horns as trade goods (ivory)
    'Ezk 27:15': 'literal / trade',
    # Psa 22:22 — literal (bulls)
    'Psa 22:22': 'literal / animal',
    # 2Sa 22:3 already listed; 1Ki 1:50, 1:51, 2:28 are altar horns
    '1Ki 1:50': 'literal / altar', '1Ki 1:51': 'literal / altar',
    '1Ki 2:28': 'literal / altar',
}

noun['ref'] = noun['book'] + ' ' + noun['chapter'].astype(str) + ':' + noun['verse'].astype(str)
noun['semantic'] = noun['ref'].map(SEMANTIC_CATEGORIES).fillna('figurative / power')

sem_counts = noun['semantic'].value_counts()

SEM_COLORS = {
    'literal / altar':    '#4292c6',
    'literal / animal':   '#41ab5d',
    'literal / object':   '#a8ddb5',
    'literal / instrument': '#ccebc5',
    'literal / trade':    '#bfd3e6',
    'figurative / power': '#d62728',
    'figurative / place': '#ff7f0e',
    'apocalyptic':        '#9467bd',
}

fig3, ax4 = plt.subplots(figsize=(9, 5))
sem_labels = sem_counts.index.tolist()
sem_vals = sem_counts.values.tolist()
sem_clrs = [SEM_COLORS.get(lbl, '#aaaaaa') for lbl in sem_labels]
wedges3, texts3, autos3 = ax4.pie(
    sem_vals, labels=sem_labels, autopct='%1.0f%%',
    startangle=130, colors=sem_clrs,
    explode=[0.04] * len(sem_vals),
    textprops={'fontsize': 8.5},
)
for at in autos3:
    at.set_fontsize(9)
ax4.set_title(
    get_display('Semantic usage of קֶרֶן (noun, n=75)') + '\nby category',
    fontsize=11, fontweight='bold')
fig3.tight_layout()
chart3_path = CHART_DIR / 'qeren_semantic_categories.png'
fig3.savefig(chart3_path, dpi=150, bbox_inches='tight')
plt.close(fig3)
print(f"Chart 3 saved: {chart3_path}")

# ============================================================
# CHART 4: The Exodus 34 translation comparison bar
# ============================================================

TRANSLATIONS_EXO34 = {
    get_display('Hebrew MT\n(קָרַן)'): 'shone / radiated',
    'LXX\n(δεδόξασται)':     'glorified',
    'Peshitta':              'glorified',
    'Vulgate\n(cornuta)':    'horned',
    'Aquila\n(κεκερατωμένη)': 'horned',
    'KJV\n(shone)':           'shone',
    'ESV / NIV\n(radiant)':   'radiant / shining',
    'Douay-Rheims\n(horned)': 'horned',
}

fig4, ax5 = plt.subplots(figsize=(11, 4))
labels4 = list(TRANSLATIONS_EXO34.keys())
meanings4 = list(TRANSLATIONS_EXO34.values())
colors4 = []
for m in meanings4:
    if 'horn' in m:
        colors4.append('#d62728')
    elif 'glorif' in m or 'radiant' in m or 'shone' in m or 'shin' in m:
        colors4.append('#2b8cbe')
    else:
        colors4.append('#999999')

bars4 = ax5.bar(range(len(labels4)), [1] * len(labels4), color=colors4,
                edgecolor='white', linewidth=0.8, width=0.6)
ax5.set_xticks(range(len(labels4)))
ax5.set_xticklabels(labels4, fontsize=9)
ax5.set_yticks([])
ax5.set_title(
    get_display('Exodus 34:29–35 — How each tradition renders קָרַן') + '\n'
    '(blue = light/glory; red = horned)',
    fontsize=11, fontweight='bold')
ax5.spines['top'].set_visible(False)
ax5.spines['right'].set_visible(False)
ax5.spines['left'].set_visible(False)
for i, (bar, meaning) in enumerate(zip(bars4, meanings4)):
    ax5.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() / 2, meaning,
             ha='center', va='center', fontsize=9, color='white', fontweight='bold')

light_patch = mpatches.Patch(color='#2b8cbe', label='Renders as light / glory / radiance')
horn_patch = mpatches.Patch(color='#d62728', label='Renders as horned')
ax5.legend(handles=[light_patch, horn_patch], loc='lower right', fontsize=8.5)
fig4.tight_layout()
chart4_path = CHART_DIR / 'qeren_exo34_translations.png'
fig4.savefig(chart4_path, dpi=150, bbox_inches='tight')
plt.close(fig4)
print(f"Chart 4 saved: {chart4_path}")

# ============================================================
# CSV exports
# ============================================================

# Verb CSV
verb_rows = []
for _, r in verb.iterrows():
    b, c, v = r['book'], r['chapter'], r['verse']
    verb_rows.append({
        'ref': f'{b} {c}:{v}',
        'book': b, 'chapter': c, 'verse': v,
        'hebrew': r['text'],
        'morph': r['morph'],
        'gloss': r['gloss'],
        'lxx_strong': r['greekstrong'],
        'lxx_word': r['greek'],
        'vulgate': vul_text(b, c, v),
        'kjv': kjv_text(b, c, v),
    })
verb_df = pd.DataFrame(verb_rows)
verb_df.to_csv(OUT / 'qeren_verb.csv', index=False)
print(f"Verb CSV: {len(verb_df)} rows")

# Noun CSV
noun_rows = []
for _, r in noun.iterrows():
    b, c, v = r['book'], r['chapter'], r['verse']
    noun_rows.append({
        'ref': f'{b} {c}:{v}',
        'book': b, 'chapter': c, 'verse': v,
        'hebrew': r['text'],
        'morph': r['morph'],
        'gloss': r['gloss'],
        'semantic': r['semantic'],
        'lxx_strong': r['greekstrong'],
        'lxx_word': r['greek'],
        'vulgate': vul_text(b, c, v),
        'kjv': kjv_text(b, c, v),
    })
noun_df = pd.DataFrame(noun_rows)
noun_df.to_csv(OUT / 'qeren_noun.csv', index=False)
print(f"Noun CSV: {len(noun_df)} rows")

print("All charts and CSVs generated.")
