"""Generate charts for the שָׁם distributive repetition report (Isa 28:10, 13)."""

import matplotlib
matplotlib.use('Agg')  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from bidi.algorithm import get_display  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from pathlib import Path  # noqa: E402

from bible_grammar import query  # noqa: E402

OUT_DIR = Path('output/charts/ot/word_studies/sham-distributive')
OUT_DIR.mkdir(parents=True, exist_ok=True)

OT_BOOKS = [
    'Gen', 'Exo', 'Lev', 'Num', 'Deu',
    'Jos', 'Jdg', 'Rut', '1Sa', '2Sa', '1Ki', '2Ki',
    '1Ch', '2Ch', 'Ezr', 'Neh', 'Est',
    'Job', 'Psa', 'Pro', 'Ecc', 'Sol',
    'Isa', 'Jer', 'Lam', 'Ezk', 'Dan',
    'Hos', 'Joe', 'Amo', 'Oba', 'Jon', 'Mic', 'Nah', 'Hab', 'Zep', 'Hag', 'Zec', 'Mal',
]
LABELS = {
    'Gen': 'Gen', 'Exo': 'Exo', 'Lev': 'Lev', 'Num': 'Num', 'Deu': 'Deu',
    'Jos': 'Josh', 'Jdg': 'Judg', 'Rut': 'Ruth', '1Sa': '1 Sam', '2Sa': '2 Sam',
    '1Ki': '1 Kgs', '2Ki': '2 Kgs', '1Ch': '1 Chr', '2Ch': '2 Chr',
    'Ezr': 'Ezra', 'Neh': 'Neh', 'Est': 'Esth',
    'Job': 'Job', 'Psa': 'Psa', 'Pro': 'Pro', 'Ecc': 'Ecc', 'Sol': 'Song',
    'Isa': 'Isa', 'Jer': 'Jer', 'Lam': 'Lam', 'Ezk': 'Ezek', 'Dan': 'Dan',
    'Hos': 'Hos', 'Joe': 'Joel', 'Amo': 'Amos', 'Oba': 'Oba', 'Jon': 'Jon',
    'Mic': 'Mic', 'Nah': 'Nah', 'Hab': 'Hab', 'Zep': 'Zeph', 'Hag': 'Hag',
    'Zec': 'Zech', 'Mal': 'Mal',
}
SECTION_COLOR = {
    **{b: '#4e79a7' for b in ['Gen', 'Exo', 'Lev', 'Num', 'Deu']},
    **{b: '#f28e2b' for b in [
        'Jos', 'Jdg', 'Rut', '1Sa', '2Sa', '1Ki', '2Ki',
        '1Ch', '2Ch', 'Ezr', 'Neh', 'Est']},
    **{b: '#59a14f' for b in ['Job', 'Psa', 'Pro', 'Ecc', 'Sol']},
    **{b: '#e15759' for b in [
        'Isa', 'Jer', 'Lam', 'Ezk', 'Dan',
        'Hos', 'Joe', 'Amo', 'Oba', 'Jon', 'Mic', 'Nah', 'Hab', 'Zep', 'Hag', 'Zec', 'Mal']},
}

legend_elements = [
    Patch(facecolor='#4e79a7', label='Torah'),
    Patch(facecolor='#f28e2b', label='Historical'),
    Patch(facecolor='#59a14f', label='Wisdom/Poetry'),
    Patch(facecolor='#e15759', label='Prophets'),
]

df = query(testament='ot')
sham = df[df['strongs'].str.contains('H8033', na=False)].copy()

book_counts = sham.groupby('book_id').size().rename('sham_total')
book_words = df.groupby('book_id').size().rename('total_words')
stats = pd.concat([book_counts, book_words], axis=1).fillna(0)
stats['per_1000'] = stats['sham_total'] / stats['total_words'] * 1000
stats = stats.reindex(OT_BOOKS, fill_value=0)

verse_sham = sham.groupby(['book_id', 'chapter', 'verse']).size()
repeated = verse_sham[verse_sham >= 2]
rep_by_book = repeated.groupby(level='book_id').size().rename('repeated_verses')
rep_stats = rep_by_book.reindex(OT_BOOKS, fill_value=0)

x = np.arange(len(OT_BOOKS))
colors = [SECTION_COLOR.get(b, '#aaa') for b in OT_BOOKS]

# ── Chart 1: שם per 1,000 words by book ──────────────────────────────────────
pvals = stats['per_1000'].values
fig, ax = plt.subplots(figsize=(16, 5))
bars = ax.bar(x, pvals, color=colors, width=0.7, edgecolor='white', linewidth=0.4)
ax.set_xticks(x)
ax.set_xticklabels([LABELS[b] for b in OT_BOOKS], rotation=45, ha='right', fontsize=7)
ax.set_ylabel(get_display('Occurrences of שָׁם per 1,000 words'), fontsize=10)
ax.set_title(
    get_display('Frequency of שָׁם (H8033) Across the OT') + '\n(occurrences per 1,000 words per book)',
    fontsize=11, pad=10,
)
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.spines[['top', 'right']].set_visible(False)
isa_idx = OT_BOOKS.index('Isa')
bars[isa_idx].set_edgecolor('#222')
bars[isa_idx].set_linewidth(2)
ax.annotate('Isaiah', xy=(isa_idx, pvals[isa_idx]),
            xytext=(isa_idx + 1.5, pvals[isa_idx] + 0.3),
            fontsize=8, color='#222',
            arrowprops=dict(arrowstyle='->', color='#222', lw=1))
ax.legend(handles=legend_elements, fontsize=8, loc='upper right')
for xv in [4.5, 16.5, 21.5]:
    ax.axvline(xv, color='#bbb', linewidth=0.8, linestyle=':')
plt.tight_layout()
fig.savefig(OUT_DIR / 'sham-frequency-by-book.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: sham-frequency-by-book.png')

# ── Chart 2: Verses with repeated שם by book ─────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 4.5))
rbars = ax.bar(x, rep_stats.values, color=colors, width=0.7, edgecolor='white', linewidth=0.4)
ax.set_xticks(x)
ax.set_xticklabels([LABELS[b] for b in OT_BOOKS], rotation=45, ha='right', fontsize=7)
ax.set_ylabel(get_display('Verses with ≥2 occurrences of שָׁם'), fontsize=10)
ax.set_title(get_display('Verses Containing Repeated שָׁם (≥2 occurrences) by OT Book'), fontsize=11, pad=10)
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.spines[['top', 'right']].set_visible(False)
ax.legend(handles=legend_elements, fontsize=8, loc='upper right')
for i, v in enumerate(rep_stats.values):
    if v >= 5:
        ax.text(i, v + 0.1, str(int(v)), ha='center', va='bottom', fontsize=7, color='#333')
for xv in [4.5, 16.5, 21.5]:
    ax.axvline(xv, color='#bbb', linewidth=0.8, linestyle=':')
plt.tight_layout()
fig.savefig(OUT_DIR / 'sham-repeated-by-book.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: sham-repeated-by-book.png')

# ── CSV export ────────────────────────────────────────────────────────────────
csv = pd.DataFrame({
    'book': [LABELS[b] for b in OT_BOOKS],
    'sham_total': stats['sham_total'].values.astype(int),
    'total_words': stats['total_words'].values.astype(int),
    'per_1000_words': stats['per_1000'].round(3).values,
    'verses_with_repeated_sham': rep_stats.values.astype(int),
})
csv.to_csv(OUT_DIR / 'sham-frequency-by-book.csv', index=False)
print(f'Saved: {OUT_DIR}/sham-frequency-by-book.csv')

print('\nDone.')
