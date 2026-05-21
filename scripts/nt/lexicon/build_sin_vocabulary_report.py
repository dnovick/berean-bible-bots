"""Generate sin-vocabulary frequency charts for the NT sin vocabulary report."""

import matplotlib
matplotlib.use('Agg')  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker as mticker  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from pathlib import Path  # noqa: E402

from bible_grammar import query  # noqa: E402

OUT_DIR = Path('output/charts/nt/sin-vocabulary')
OUT_DIR.mkdir(parents=True, exist_ok=True)

SIN_STRONGS = [
    'G0264',  # ἁμαρτάνω
    'G0265',  # ἁμάρτημα
    'G0266',  # ἁμαρτία
    'G0268',  # ἁμαρτωλός
    'G0458',  # ἀνομία
    'G0459',  # ἄνομος
    'G3900',  # παράπτωμα
    'G3847',  # παράβασις
    'G3848',  # παραβάτης
    'G0093',  # ἀδικία
    'G4189',  # πονηρία
]

NT_BOOK_ORDER = [
    'Mat', 'Mrk', 'Luk', 'Jhn', 'Act',
    'Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
    '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm',
    'Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev',
]
LABELS = {
    'Mat': 'Matthew', 'Mrk': 'Mark', 'Luk': 'Luke', 'Jhn': 'John', 'Act': 'Acts',
    'Rom': 'Romans', '1Co': '1 Cor', '2Co': '2 Cor', 'Gal': 'Galatians',
    'Eph': 'Ephesians', 'Php': 'Philippians', 'Col': 'Colossians',
    '1Th': '1 Thess', '2Th': '2 Thess', '1Ti': '1 Timothy', '2Ti': '2 Timothy',
    'Tit': 'Titus', 'Phm': 'Philemon', 'Heb': 'Hebrews', 'Jas': 'James',
    '1Pe': '1 Peter', '2Pe': '2 Peter', '1Jn': '1 John', '2Jn': '2 John',
    '3Jn': '3 John', 'Jud': 'Jude', 'Rev': 'Revelation',
}
SECTION_COLOR_MAP = {
    **{b: '#4e79a7' for b in ['Mat', 'Mrk', 'Luk', 'Jhn', 'Act']},
    **{b: '#f28e2b' for b in [
        'Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
        '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm']},
    **{b: '#59a14f' for b in ['Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev']},
}
SECTIONS = {
    'Gospels & Acts': ['Mat', 'Mrk', 'Luk', 'Jhn', 'Act'],
    'Pauline Epistles': ['Rom', '1Co', '2Co', 'Gal', 'Eph', 'Php', 'Col',
                         '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm'],
    'General Epistles': ['Heb', 'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev'],
}
SEC_COLORS = ['#4e79a7', '#f28e2b', '#59a14f']

df = query(testament='nt')
sin_mask = df['strongs'].fillna('').apply(lambda s: any(s.startswith(p) for p in SIN_STRONGS))
total_words = df.groupby('book_id').size().rename('total')
sin_words = df[sin_mask].groupby('book_id').size().rename('sin')
stats = pd.concat([total_words, sin_words], axis=1).fillna(0)
stats['pct'] = stats['sin'] / stats['total'] * 100
stats = stats.reindex(NT_BOOK_ORDER)

# ── Chart 1: Bar chart by book ────────────────────────────────────────────────
x = np.arange(len(NT_BOOK_ORDER))
pcts = stats['pct'].values
colors = [SECTION_COLOR_MAP[b] for b in NT_BOOK_ORDER]

fig, ax = plt.subplots(figsize=(15, 6))
bars = ax.bar(x, pcts, color=colors, width=0.7, edgecolor='white', linewidth=0.5)
for bar, val in zip(bars, pcts):
    if val >= 0.05:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f'{val:.1f}%', ha='center', va='bottom', fontsize=6.5, color='#333')
ax.set_xticks(x)
ax.set_xticklabels([LABELS[b] for b in NT_BOOK_ORDER], rotation=45, ha='right', fontsize=8.5)
ax.set_ylabel('Sin-vocabulary words as % of book total', fontsize=10)
ax.set_title(
    'Sin Vocabulary Frequency by NT Book\n'
    '(ἁμαρτία, ἁμαρτάνω, ἁμαρτωλός, ἀνομία, παράπτωμα, παράβασις, ἀδικία, πονηρία, and cognates)',
    fontsize=11, pad=12,
)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))
ax.set_ylim(0, pcts.max() * 1.18)
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.spines[['top', 'right']].set_visible(False)
legend_elements = [
    Patch(facecolor='#4e79a7', label='Gospels & Acts'),
    Patch(facecolor='#f28e2b', label='Pauline Epistles'),
    Patch(facecolor='#59a14f', label='General Epistles'),
]
ax.legend(handles=legend_elements, fontsize=9, loc='upper right')
for xv in [4.5, 17.5]:
    ax.axvline(xv, color='#aaa', linewidth=0.8, linestyle=':')
plt.tight_layout()
fig.savefig(OUT_DIR / 'nt-sin-vocabulary-by-book.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: nt-sin-vocabulary-by-book.png')

# ── Chart 2: Word group heatmap ───────────────────────────────────────────────
GROUPS = {
    'ἁμαρτία\n(sin)': ['G0264', 'G0265', 'G0266', 'G0268'],
    'ἀνομία\n(lawlessness)': ['G0458', 'G0459'],
    'παράπτωμα\n(trespass)': ['G3900', 'G3847', 'G3848'],
    'ἀδικία\n(unright.)': ['G0093'],
    'πονηρία\n(wickedness)': ['G4189'],
}

heat_data = {}
for label, prefixes in GROUPS.items():
    mask = df['strongs'].fillna('').apply(lambda s: any(s.startswith(p) for p in prefixes))
    counts = df[mask].groupby('book_id').size().reindex(NT_BOOK_ORDER, fill_value=0)
    heat_data[label] = (counts / stats['total'] * 1000).values

heat_df = pd.DataFrame(heat_data, index=[LABELS[b] for b in NT_BOOK_ORDER])

fig, ax = plt.subplots(figsize=(9, 10))
im = ax.imshow(heat_df.values, aspect='auto', cmap='YlOrRd', interpolation='nearest')
ax.set_xticks(range(len(GROUPS)))
ax.set_xticklabels(list(GROUPS.keys()), fontsize=9)
ax.set_yticks(range(len(NT_BOOK_ORDER)))
ax.set_yticklabels([LABELS[b] for b in NT_BOOK_ORDER], fontsize=8.5)
for i in range(len(NT_BOOK_ORDER)):
    for j in range(len(GROUPS)):
        val = heat_df.iloc[i, j]
        if val > 0.05:
            ax.text(j, i, f'{val:.1f}', ha='center', va='center',
                    fontsize=7, color='black' if val < 3 else 'white')
plt.colorbar(im, ax=ax, label='occurrences per 1,000 words', shrink=0.6)
ax.set_title('Sin Vocabulary Word Groups — NT Books\n(occurrences per 1,000 words)', fontsize=11, pad=10)
for yv in [4.5, 17.5]:
    ax.axhline(yv, color='#555', linewidth=1.2, linestyle='--')
plt.tight_layout()
fig.savefig(OUT_DIR / 'nt-sin-vocabulary-heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: nt-sin-vocabulary-heatmap.png')

# ── Chart 3: Section averages ─────────────────────────────────────────────────
group_avgs = {}
for sec_label, books in SECTIONS.items():
    sec_stats = stats.loc[books]
    group_avgs[sec_label] = sec_stats['sin'].sum() / sec_stats['total'].sum() * 100

fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(list(group_avgs.keys()), list(group_avgs.values()),
              color=SEC_COLORS, width=0.5, edgecolor='white')
for bar, val in zip(bars, group_avgs.values()):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
            f'{val:.2f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.set_ylabel('Sin-vocabulary as % of total words', fontsize=10)
ax.set_title('Sin Vocabulary Density by NT Corpus Section', fontsize=11)
ax.set_ylim(0, max(group_avgs.values()) * 1.25)
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
fig.savefig(OUT_DIR / 'nt-sin-vocabulary-by-section.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: nt-sin-vocabulary-by-section.png')

# ── CSV export ────────────────────────────────────────────────────────────────
csv_path = OUT_DIR / 'nt-sin-vocabulary-by-book.csv'
export = stats.copy()
export.index = [LABELS[b] for b in NT_BOOK_ORDER]
export.index.name = 'book'
export.columns = ['total_words', 'sin_vocab_words', 'pct_frequency']
export['pct_frequency'] = export['pct_frequency'].round(4)
export.to_csv(csv_path)
print(f'Saved: {csv_path}')

print('\nDone.')
