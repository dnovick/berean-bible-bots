"""Build ἐπὶ τὸ αὐτό report charts and CSV data."""
import matplotlib; matplotlib.use('Agg')  # noqa: E702
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from pathlib import Path
from bidi.algorithm import get_display
from bible_grammar.lxx_query import query_lxx
from bible_grammar.syntax_ot import load_syntax_ot
from bible_grammar.syntax import load_syntax


def bidi_label(text: str) -> str:
    """Return display-ready text with the Hebrew portion bidi-reordered."""
    if '(' in text:
        heb, rest = text.split('(', 1)
        return get_display(heb.strip()) + ' (' + rest
    return get_display(text)


lxx = query_lxx(include_deuterocanon=True)
lxx_sorted = lxx.sort_values(['book_id', 'chapter', 'verse', 'word_num']).reset_index(drop=True)
ot = load_syntax_ot()
nt = load_syntax().sort_values(['book', 'chapter', 'verse', 'word_num'])

OUT = Path('output/reports/both/phrase_studies')
OUT.mkdir(parents=True, exist_ok=True)
CHART_DIR = Path('output/charts/both/phrase_studies')
CHART_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# NT TABLE
# ============================================================

nt_sorted = nt.sort_values(['book', 'chapter', 'verse', 'word_num']).reset_index(drop=True)

NT_BOOK_LABELS = {
    'Mat': 'Matthew', 'Mrk': 'Mark', 'Luk': 'Luke', 'Jhn': 'John',
    'Act': 'Acts', 'Rom': 'Romans', '1Co': '1 Corinthians', '2Co': '2 Corinthians',
}

NT_MEANINGS = {
    'Mat 22:34': ('assembled against',   'Pharisees gathered together [against Jesus]'),
    'Luk 17:35': ('same place',          'Two women grinding at the same place'),
    'Act 1:15':  ('assembled together',  'The ~120 disciples gathered'),
    'Act 2:1':   ('assembled together',  'All gathered together on Pentecost'),
    'Act 2:44':  ('community/together',  'All believers together held all things in common'),
    'Act 2:47':  ('community/together',  'Lord adding to the community daily'),
    'Act 4:26':  ('assembled against',   'Kings assembled against the Lord — cites LXX Ps 2:2'),
    '1Co 7:5':   ('conjugal reunion',    'Come together again [as husband and wife]'),
    '1Co 11:20': ('assembled to worship', "When you come together for the Lord's Supper"),
    '1Co 14:23': ('assembled to worship', 'If the whole church comes together'),
}

nt_results = []
for i, row in nt_sorted[nt_sorted['lemma'] == 'ἐπί'].iterrows():
    bk, ch, vs, wn = row['book'], row['chapter'], row['verse'], row['word_num']
    following = nt_sorted[
        (nt_sorted['book'] == bk) & (nt_sorted['chapter'] == ch) &
        (nt_sorted['verse'] == vs) & (nt_sorted['word_num'] > wn)
    ].head(4)
    if len(following) >= 2:
        lemmas = following['lemma'].tolist()
        if lemmas[0] == 'ὁ' and lemmas[1] == 'αὐτός':
            verse_tokens = nt_sorted[
                (nt_sorted['book'] == bk) & (nt_sorted['chapter'] == ch) & (nt_sorted['verse'] == vs)
            ]
            greek_text = ' '.join(verse_tokens['text'].tolist())
            ref = f'{bk} {ch}:{vs}'
            m = NT_MEANINGS.get(ref, ('—', ''))
            nt_results.append({
                'ref': ref,
                'book': bk,
                'book_label': NT_BOOK_LABELS.get(bk, bk),
                'chapter': ch,
                'verse': vs,
                'greek_verse': greek_text,
                'function': m[0],
                'notes': m[1],
            })

nt_df = pd.DataFrame(nt_results)
nt_df.to_csv(OUT / 'epi_to_auto_nt.csv', index=False)
print(f"NT occurrences: {len(nt_df)}")

# ============================================================
# LXX TABLE — full manual annotation
# ============================================================

# (mt_ref, heb_source, heb_gloss, function_category, notes)
LXX_DATA = {
    'Psa 2:2':    ('Ps 2:2',       'יַחַד',
                   'together',          'hostile assembly',
                   'Kings and rulers conspire together — quoted in Acts 4:26'),
    'Psa 4:9':    ('Ps 4:8',       'יַחְדָּו',
                   'together',          'peaceable rest',
                   'In peace I will lie down and sleep; LXX adds ἐπὶ τὸ αὐτό'),
    'Psa 18:10':  ('Ps 19:10',     '—',
                   '(no direct Hebrew)', 'emphatic totality',
                   'LXX expansionary; judgments of the Lord are true altogether'),
    'Psa 33:4':   ('Ps 34:3',      'יַחְדָּו',
                   'together',          'communal praise',
                   'Let us exalt his name together'),
    'Psa 36:38':  ('Ps 37:38',     'יַחְדָּו',
                   'together',          'hostile assembly',
                   'Transgressors destroyed together'),
    'Psa 40:8':   ('Ps 41:7',      'יַחַד',
                   'together',          'hostile assembly',
                   'Enemies whisper together against the psalmist'),
    'Psa 47:5':   ('Ps 48:4',      'יַחְדָּו',
                   'together',          'hostile assembly',
                   'Kings assembled together, then fled in panic'),
    'Psa 48:3':   ('Ps 49:2',      'יַחַד',
                   'together',          'universal address',
                   'Rich and poor together — all humanity addressed'),
    'Psa 48:11':  ('Ps 49:10',     'יַחַד',
                   'together',          'universal fate',
                   'Wise and fool perish together'),
    'Psa 54:15':  ('Ps 55:14',     'יַחְדָּו',
                   'together',          'former fellowship',
                   'We took sweet counsel together in the house of God'),
    'Psa 61:10':  ('Ps 62:9',      'יַחַד',
                   'together',          'emphatic totality',
                   'All humanity is vanity together on the scales'),
    'Psa 70:10':  ('Ps 71:10',     'יַחְדָּו',
                   'together',          'hostile assembly',
                   'Those who watch for my life plot together'),
    'Psa 73:6':   ('Ps 74:6',      'יַחַד',
                   'together',          'hostile assembly',
                   'They smash the carved work with axes together'),
    'Psa 73:8':   ('Ps 74:8',      'יַחַד',
                   'together',          'hostile assembly',
                   '"Let us destroy them together" — burn all meeting places'),
    'Psa 82:6':   ('Ps 83:5',      'יַחְדָּו',
                   'together',          'hostile assembly',
                   'They conspire with one heart together against you'),
    'Psa 97:8':   ('Ps 98:8',      'יַחַד',
                   'together',          'communal praise',
                   'Rivers clap, mountains sing together before the Lord'),
    'Psa 101:23': ('Ps 102:22',    'יַחְדָּו',
                   'together',          'communal worship',
                   'Peoples gathered together to serve the Lord'),
    'Psa 121:3':  ('Ps 122:3',     'יַחְדָּו',
                   'together',          'unity / dwelling',
                   'Jerusalem built as a city joined together'),
    'Psa 132:1':  ('Ps 133:1',     'יַחַד',
                   'together',          'unity / dwelling',
                   'How good for brothers to dwell together — Song of Ascents'),
    'Deu 12:15':  ('Dt 12:15',     'לְ בַּד',
                   'alone / separately', 'same place / freely',
                   'Slaughter and eat anywhere in your towns (free permission)'),
    'Deu 22:10':  ('Dt 22:10',     'יַחְדָּו',
                   'together',          'prohibition',
                   'Do not plow with ox and donkey together'),
    'Deu 25:5':   ('Dt 25:5',      'יַחְדָּו + אֶחָד',
                   'together; one',     'dwelling together',
                   'Brothers dwelling together (levirate marriage law)'),
    'Deu 25:11':  ('Dt 25:11',     'יַחְדָּו',
                   'together',          'physical proximity',
                   'Two men fighting together (same context, levirate section)'),
    'Ecc 11:6':   ('Ec 11:6',      'אֶחָד',
                   'one / alike',       'emphatic totality',
                   'Which will prosper, this or that, or both alike'),
    'Exo 26:9':   ('Ex 26:9',      'לְ בַּד',
                   'by itself / separately', 'physical joining',
                   'Join five curtains by themselves; six by themselves (tabernacle)'),
    'Ezr 4:3':    ('Ezr 4:3',      '—',
                   '(contextual)',      'hostile opposition',
                   'You have nothing to do with us — adversaries united in refusal'),
    'Hos 2:2':    ('Hos 2:1',      'יַחְדָּו',
                   'together',          'eschatological reunion',
                   'Sons of Judah and Israel gathered together under one head'),
    'Isa 66:17':  ('Is 66:17',     'אַחַת',
                   'one (together behind one)', 'idolatrous group',
                   'Consecrating themselves following one in their midst'),
    'Jer 3:18':   ('Jer 3:18',     'יַחְדָּו',
                   'together',          'eschatological reunion',
                   'Judah and Israel will come together from the north'),
    'Jer 6:12':   ('Jer 6:12',     'יַחְדָּו',
                   'together',          'total devastation',
                   'Houses, fields, and wives handed over together to others'),
    'Jer 26:12':  ('Jer 46:12 MT', 'יַחְדָּו',
                   'together',          'mutual destruction',
                   'Warrior stumbles on warrior; both fall together [LXX chapter order differs]'),
    'Jer 27:4':   ('Jer 50:4 MT',  'יַחְדָּו',
                   'together',          'eschatological reunion',
                   'Israel and Judah going together weeping and seeking the Lord'),
    'Jos 9:2':    ('Jos 9:2',
                   'יַחְדָּו + פֶּה אֶחָד',
                   'together; with one accord', 'hostile assembly',
                   'Kings gathered to fight Joshua with one accord'),
    'Jos 11:5':   ('Jos 11:5',     'יַחְדָּו',
                   'together',          'hostile assembly',
                   'All these kings came and encamped together at Waters of Merom'),
    'Mic 2:12':   ('Mic 2:12',     'יַחַד',
                   'together',          'eschatological gathering',
                   'I will surely assemble the remnant of Israel together'),
    'Nah 1:9':    ('Nah 1:9',      '—',
                   '(no direct Hebrew)', 'once-for-all',
                   'Affliction will not rise a second time — LXX renders "at once"'),
    'Amo 1:15':   ('Am 1:15',      'יַחְדָּו',
                   'together',          'total defeat',
                   'King and officials go into exile together'),
    'Amo 3:3':    ('Am 3:3',       'יַחְדָּו',
                   'together',          'purposeful meeting',
                   'Can two walk together unless they have agreed to meet?'),
    '2Sa 2:13':   ('2Sa 2:13',     'יַחְדָּו',
                   'together',          'physical meeting',
                   "Joab and David's men met together at the pool of Gibeon"),
    '2Sa 10:15':  ('2Sa 10:15',    'יַחַד',
                   'together',          'hostile assembly',
                   'Arameans gathered together [for a second attack] after defeat'),
    '2Sa 12:3':   ('2Sa 12:3',     'אַחַת',
                   'one',               'emphatic singularity',
                   'The poor man had only one ewe lamb'),
    '2Sa 21:9':   ('2Sa 21:9',     'יַחַד',
                   'together',          'collective death',
                   "Seven of Saul's sons fell together at harvest time"),
    '1Ch 10:6':   ('1Ch 10:6',     'יַחְדָּו',
                   'together',          'collective death',
                   'Saul and all his household died together'),
    'Dan 11:27':  ('Dan 11:27',    'אֶחָד',
                   'one',               'physical co-presence',
                   'Two kings sit at one table, both speaking lies'),
    'Ezr 14:2':   ('Neh 4:2',      'יַחְדָּו',
                   'together',          'hostile assembly',
                   'All the enemies conspired together to come and fight Jerusalem'),
    'Ezr 16:2':   ('Neh 6:2',      'יַחְדָּו',
                   'together',          'hostile meeting',
                   'Sanballat and Geshem invited Nehemiah to meet together in the plain'),
    'Ezr 16:7':   ('Neh 6:7',      '—',
                   '(no direct Hebrew)', 'conspiratorial counsel',
                   'LXX adds ἐπὶ τὸ αὐτό for "take counsel together" — no Hebrew equiv.'),
    # Deuterocanonical
    '3Mac 3:1':   ('3 Macc 3:1',   '—',
                   '(deuterocanon)',    'hostile assembly',
                   'The king and friends plotted together against the Jews'),
    'Bel 1:27':   ('Bel 1:27',     '—',
                   '(deuterocanon)',    'assembled together',
                   'The people gathered together'),
    'BelTh 1:27': ('Bel 1:27 Th',  '—',
                   '(deuterocanon)',    'assembled together',
                   'Bel and Dragon (Theodotion)'),
    'SusTh 1:14': ('Sus 1:14 Th',  '—',
                   '(deuterocanon)',    'hostile conspiracy',
                   'The two elders agreed together on the same day to watch her'),
}

# Jdg 6:25: the LXX text is doubled (two manuscript traditions merged); the token
# is ἐπ᾿ αὐτῷ ("upon it", dative), not ἐπὶ τὸ αὐτό — excluded as a false positive.
FALSE_POSITIVES = {'Jdg 6:25'}

epi_idx = lxx_sorted[lxx_sorted['strongs'] == 'G1909'].index

lxx_results = []
for i in epi_idx:
    row = lxx_sorted.loc[i]
    bk, ch, vs = row['book_id'], row['chapter'], row['verse']
    ref_check = f'{bk} {int(ch)}:{int(vs)}'
    if ref_check in FALSE_POSITIVES:
        continue
    following = lxx_sorted.iloc[i+1:i+5]
    following = following[
        (following['book_id'] == bk) & (following['chapter'] == ch) & (following['verse'] == vs)
    ]
    if len(following) >= 2:
        strongs_list = following['strongs'].tolist()
        texts = following['word'].tolist()
        if strongs_list[0] == 'G3588' and strongs_list[1] == 'G846':
            art = texts[0].lower().replace('ι', '').replace('ʼ', '').replace('ι', '')
            if art not in ['τὸ', 'το']:
                continue
            phrase = row['word'] + ' ' + texts[0] + ' ' + texts[1]
            verse_tokens = lxx_sorted[
                (lxx_sorted['book_id'] == bk) & (lxx_sorted['chapter'] == ch) & (lxx_sorted['verse'] == vs)
            ]
            lxx_verse = ' '.join(verse_tokens['word'].tolist())
            ref = f'{bk} {int(ch)}:{int(vs)}'
            data = LXX_DATA.get(ref, (ref, '?', '?', 'unknown', ''))
            lxx_results.append({
                'lxx_ref': ref,
                'mt_ref': data[0],
                'book': bk,
                'chapter': int(ch),
                'verse': int(vs),
                'phrase': phrase,
                'lxx_verse': lxx_verse[:180],
                'heb_source': data[1],
                'heb_gloss': data[2],
                'function': data[3],
                'notes': data[4],
                'is_deuterocanon': bool(row['is_deuterocanon']),
            })

lxx_df = pd.DataFrame(lxx_results)
lxx_df.to_csv(OUT / 'epi_to_auto_lxx.csv', index=False)
n_canon = (~lxx_df['is_deuterocanon']).sum()
n_deut = lxx_df['is_deuterocanon'].sum()
print(f"LXX (tau to auto only): {len(lxx_df)}  canonical={n_canon}  deuterocanon={n_deut}")

# ============================================================
# CHART 1: Distribution by book (canonical LXX)
# ============================================================
lxx_canon = lxx_df[~lxx_df['is_deuterocanon']].copy()

GENRE_MAP = {
    'Gen': 'Torah', 'Exo': 'Torah', 'Lev': 'Torah', 'Num': 'Torah', 'Deu': 'Torah',
    'Jos': 'Historical', 'Jdg': 'Historical', 'Rut': 'Historical',
    '1Sa': 'Historical', '2Sa': 'Historical', '1Ki': 'Historical', '2Ki': 'Historical',
    '1Ch': 'Historical', '2Ch': 'Historical', 'Ezr': 'Historical', 'Neh': 'Historical', 'Est': 'Historical',
    'Job': 'Wisdom', 'Psa': 'Psalms', 'Pro': 'Wisdom', 'Ecc': 'Wisdom', 'Sng': 'Wisdom',
    'Isa': 'Prophets', 'Jer': 'Prophets', 'Lam': 'Prophets', 'Ezk': 'Prophets', 'Dan': 'Prophets',
    'Hos': 'Prophets', 'Jol': 'Prophets', 'Amo': 'Prophets', 'Oba': 'Prophets', 'Jon': 'Prophets',
    'Mic': 'Prophets', 'Nam': 'Prophets', 'Hab': 'Prophets', 'Zep': 'Prophets',
    'Hag': 'Prophets', 'Zec': 'Prophets', 'Mal': 'Prophets',
}
GENRE_ORDER = ['Torah', 'Historical', 'Psalms', 'Wisdom', 'Prophets']
GENRE_COLORS = {
    'Torah': '#4292c6', 'Historical': '#fd8d3c',
    'Psalms': '#41ab5d', 'Wisdom': '#9e9ac8', 'Prophets': '#d62728',
}

lxx_canon['genre'] = lxx_canon['book'].map(GENRE_MAP).fillna('Other')
book_counts = lxx_canon.groupby(['book', 'genre']).size().reset_index(name='count')

genre_order_map = {g: i for i, g in enumerate(GENRE_ORDER)}
book_counts['genre_ord'] = book_counts['genre'].map(genre_order_map)
book_counts = book_counts.sort_values(['genre_ord', 'count'], ascending=[True, False])

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

ax1 = axes[0]
bks = book_counts['book'].tolist()
cnts = book_counts['count'].tolist()
gnrs = book_counts['genre'].tolist()
clrs = [GENRE_COLORS.get(g, 'gray') for g in gnrs]
bars = ax1.barh(bks, cnts, color=clrs, edgecolor='white', linewidth=0.5)
for bar, v in zip(bars, cnts):
    ax1.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
             str(v), va='center', fontsize=9)
ax1.set_xlabel('Occurrences', fontsize=10)
ax1.set_title('ἐπὶ τὸ αὐτό in the LXX\nDistribution by book (canonical)',
              fontsize=11, fontweight='bold')
ax1.xaxis.grid(True, linestyle='--', alpha=0.4)
ax1.set_axisbelow(True)
patches = [mpatches.Patch(color=c, label=g) for g, c in GENRE_COLORS.items()]
ax1.legend(handles=patches, loc='lower right', fontsize=8)

ax2 = axes[1]
func_counts = lxx_canon['function'].value_counts()
wedge_colors = [
    '#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
]
wedges, texts, autotexts = ax2.pie(
    func_counts.values,
    labels=func_counts.index,
    autopct='%1.0f%%',
    startangle=140,
    colors=wedge_colors[:len(func_counts)],
    explode=[0.04] * len(func_counts),
    textprops={'fontsize': 7.5},
)
for at in autotexts:
    at.set_fontsize(8)
ax2.set_title(f'Semantic function distribution\n(LXX canonical, n={n_canon})',
              fontsize=11, fontweight='bold')

fig.tight_layout(pad=2.5)
chart1_path = CHART_DIR / 'epi_to_auto_lxx_distribution.png'
fig.savefig(chart1_path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"Chart 1 saved: {chart1_path}")

# ============================================================
# CHART 2: Hebrew source word distribution
# ============================================================

# Normalize Hebrew source variants to display labels.
# Keys must match the exact Unicode stored in LXX_DATA['heb_source'].
yachdav = 'יַחְדָּו'  # יַחְדָּו with dagesh
yachad = 'יַחַד'
echad = 'אֶחָד'
achat = 'אַחַת'
levad = 'לְ בַּד'
dash = '—'

heb_norm = {
    yachad:                    f'{yachad} (yachad)',
    yachdav:                   f'{yachdav} (yachdav)',
    echad:                     f'{echad} (echad)',
    achat:                     f'{echad} (echad)',
    levad:                     f'{levad} (levad)',
    f'{yachdav} + {echad}':   f'{yachdav} (yachdav)',
    f'{yachdav} + פֶּה {echad}': f'{yachdav} (yachdav)',
    dash:                      'No direct Hebrew',
    '(contextual)':            'No direct Hebrew',
    '(no direct Hebrew)':      'No direct Hebrew',
    '(deuterocanon)':          'No direct Hebrew',
}

source_counts: dict = {}
for h in lxx_canon['heb_source']:
    n = heb_norm.get(h, h)
    source_counts[n] = source_counts.get(n, 0) + 1

labels = sorted(source_counts.keys(), key=lambda x: -source_counts[x])
vals = [source_counts[lbl] for lbl in labels]
display_labels = [bidi_label(lbl) for lbl in labels]

fig2, ax3 = plt.subplots(figsize=(9, 4))
bar_colors = ['#2b8cbe', '#7bccc4', '#f0a500', '#c2e699', '#aaaaaa']
bars2 = ax3.bar(range(len(labels)), vals, color=bar_colors[:len(labels)], edgecolor='white', linewidth=0.5)
ax3.set_xticks(range(len(labels)))
ax3.set_xticklabels(display_labels, fontsize=10)
ax3.set_ylabel('LXX occurrences', fontsize=10)
ax3.set_title(
    'Hebrew source words for ἐπὶ τὸ αὐτό\n(LXX canonical only)',
    fontsize=11, fontweight='bold')
ax3.yaxis.grid(True, linestyle='--', alpha=0.4)
ax3.set_axisbelow(True)
for bar, v in zip(bars2, vals):
    ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
             str(v), ha='center', fontsize=11, fontweight='bold')
fig2.tight_layout()
chart2_path = CHART_DIR / 'epi_to_auto_hebrew_sources.png'
fig2.savefig(chart2_path, dpi=150, bbox_inches='tight')
plt.close(fig2)
print(f"Chart 2 saved: {chart2_path}")

# ============================================================
# CHART 3: NT occurrences — book bar + semantic function pie
# ============================================================
NT_FUNC_COLORS = {
    'assembled together':  '#2ca02c',
    'assembled to worship': '#1f77b4',
    'assembled against':   '#d62728',
    'same place':          '#ff7f0e',
    'conjugal reunion':    '#9467bd',
    'community/together':  '#17becf',
}

nt_book_counts = nt_df.groupby(['book_label', 'function']).size().reset_index(name='count')
nt_book_order = nt_df.groupby('book_label').size().sort_values(ascending=False).index.tolist()

fig3, axes3 = plt.subplots(1, 2, figsize=(13, 5))

# Left: horizontal bar by book, coloured by function
ax4 = axes3[0]
book_totals = nt_df.groupby('book_label').size().reindex(nt_book_order)
nt_func_counts = nt_df['function'].value_counts()
func_colors_assigned = [
    NT_FUNC_COLORS.get(f, '#7f7f7f') for f in nt_func_counts.index
]

# Build stacked bars per book
bottoms = np.zeros(len(nt_book_order))
func_groups = nt_df.groupby('function')
legend_patches = []
for func, color in NT_FUNC_COLORS.items():
    sub = nt_df[nt_df['function'] == func]
    counts_by_book = sub.groupby('book_label').size().reindex(nt_book_order, fill_value=0)
    bars3 = ax4.barh(nt_book_order, counts_by_book.values, left=bottoms,
                     color=color, edgecolor='white', linewidth=0.5, label=func)
    bottoms += counts_by_book.values
    if sub.shape[0] > 0:
        legend_patches.append(mpatches.Patch(color=color, label=func))

for i, book in enumerate(nt_book_order):
    total = book_totals[book]
    ax4.text(total + 0.05, i, str(total), va='center', fontsize=9)

ax4.set_xlabel('Occurrences', fontsize=10)
ax4.set_title('ἐπὶ τὸ αὐτό in the NT\nDistribution by book (n=10)',
              fontsize=11, fontweight='bold')
ax4.xaxis.grid(True, linestyle='--', alpha=0.4)
ax4.set_axisbelow(True)
ax4.legend(handles=legend_patches, loc='lower right', fontsize=8)

# Right: semantic function pie
ax5 = axes3[1]
nt_func_vals = nt_df['function'].value_counts()
pie_colors = [NT_FUNC_COLORS.get(f, '#7f7f7f') for f in nt_func_vals.index]
wedges5, texts5, autotexts5 = ax5.pie(
    nt_func_vals.values,
    labels=nt_func_vals.index,
    autopct='%1.0f%%',
    startangle=140,
    colors=pie_colors,
    explode=[0.04] * len(nt_func_vals),
    textprops={'fontsize': 8},
)
for at in autotexts5:
    at.set_fontsize(8.5)
ax5.set_title('NT semantic function distribution\n(n=10)', fontsize=11, fontweight='bold')

fig3.tight_layout(pad=2.5)
chart3_path = CHART_DIR / 'epi_to_auto_nt_distribution.png'
fig3.savefig(chart3_path, dpi=150, bbox_inches='tight')
plt.close(fig3)
print(f"Chart 3 saved: {chart3_path}")

print("All data and charts generated.")
