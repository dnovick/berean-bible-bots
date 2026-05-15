"""Rebuild fasting word-study charts with corrected bidi titles."""
import sys
sys.path.insert(0, 'src')

import matplotlib  # noqa: E402
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patches as mpatches  # noqa: E402
from pathlib import Path  # noqa: E402
from bidi.algorithm import get_display  # noqa: E402
from bible_grammar.core.syntax_ot import load_syntax_ot  # noqa: E402
from bible_grammar.core.lxx_query import query_lxx  # noqa: E402
from bible_grammar.core._utils import load_nt  # noqa: E402
import unicodedata  # noqa: E402

CHART_DIR = Path('output/charts/both/word_studies/fasting')
CHART_DIR.mkdir(parents=True, exist_ok=True)

ot = load_syntax_ot()
lxx_df = query_lxx(include_deuterocanon=False)
nt = load_nt()


def nfc(s: object) -> str:
    return unicodedata.normalize('NFC', str(s))


ot_fast = ot[ot['strong_h'].isin(['H6684', 'H6685'])].copy()
verb = ot_fast[ot_fast['strong_h'] == 'H6684']
noun = ot_fast[ot_fast['strong_h'] == 'H6685']

BOOK_ORDER = [
    'Jdg', '1Sa', '2Sa', '1Ki', '1Ch', '2Ch', 'Ezr', 'Neh',
    'Est', 'Psa', 'Isa', 'Jer', 'Dan', 'Jol', 'Jon', 'Zec',
]

# ============================================================
# CHART 1: Hebrew OT by book (verb + noun grouped bar)
# ============================================================

verb_ct = verb['book'].value_counts()
noun_ct = noun['book'].value_counts()
books = [b for b in BOOK_ORDER if b in verb_ct or b in noun_ct]
v_vals = [verb_ct.get(b, 0) for b in books]
n_vals = [noun_ct.get(b, 0) for b in books]

x = range(len(books))
width = 0.38

fig1, ax1 = plt.subplots(figsize=(14, 5))
bars_v = ax1.bar([i - width / 2 for i in x], v_vals, width, color='#4393c3', label=get_display('Verb צוּם (H6684)'))
bars_n = ax1.bar([i + width / 2 for i in x], n_vals, width, color='#f4a582', label=get_display('Noun צוֹם (H6685)'))

for bar, v in zip(bars_v, v_vals):
    if v:
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                 str(v), ha='center', va='bottom', fontsize=9)
for bar, v in zip(bars_n, n_vals):
    if v:
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                 str(v), ha='center', va='bottom', fontsize=9)

ax1.set_xticks(list(x))
ax1.set_xticklabels(books, fontsize=9)
ax1.set_ylabel('Occurrences', fontsize=10)
ax1.yaxis.grid(True, linestyle='--', alpha=0.4)
ax1.set_axisbelow(True)
ax1.legend(fontsize=9)
# LTR prefix anchors direction for mixed-script title
ax1.set_title(
    'Hebrew OT Fasting Vocabulary by Book\n' +
    get_display('Verb צוּם (H6684) · Noun צוֹם (H6685)'),
    fontsize=12, fontweight='bold')

fig1.tight_layout()
p1 = CHART_DIR / 'fasting_hebrew_by_book.png'
fig1.savefig(p1, dpi=150, bbox_inches='tight')
plt.close(fig1)
print(f'Chart 1 saved: {p1}')

# ============================================================
# CHART 2: Hebrew verb conjugation distribution
# ============================================================

MORPH_LABELS = {
    'Vqw': 'Qal Consecutive Perfect (wayyiqtol)',
    'Vqi': 'Qal Imperfect (yiqtol)',
    'Vqp': 'Qal Perfect (qatal)',
    'Vqr': 'Qal Participle',
    'Vqv': 'Qal Imperative',
    'Vqa': 'Qal Infinitive absolute',
}


def morph_label(code: str) -> str:
    prefix = code[:3]
    return MORPH_LABELS.get(prefix, code)


verb2 = verb.copy()
verb2['label'] = verb2['morph'].apply(morph_label)
ct2 = verb2['label'].value_counts().sort_values()

colors2 = plt.cm.Blues([0.3 + 0.55 * i / max(len(ct2) - 1, 1) for i in range(len(ct2))])

fig2, ax2 = plt.subplots(figsize=(9, 5))
bars2 = ax2.barh(ct2.index, ct2.values, color=colors2)
for bar, v in zip(bars2, ct2.values):
    ax2.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
             str(v), va='center', fontsize=10)
ax2.set_xlabel('Occurrences', fontsize=10)
ax2.xaxis.grid(True, linestyle='--', alpha=0.4)
ax2.set_axisbelow(True)
# LTR prefix anchors direction
ax2.set_title(
    get_display('Conjugation Distribution — Hebrew צוּם (H6684)'),
    fontsize=12, fontweight='bold')
fig2.tight_layout()
p2 = CHART_DIR / 'fasting_hebrew_verb_morph.png'
fig2.savefig(p2, dpi=150, bbox_inches='tight')
plt.close(fig2)
print(f'Chart 2 saved: {p2}')

# ============================================================
# CHART 3: LXX by book
# ============================================================

lxx_targets = {nfc('νηστεύω'), nfc('νηστεία')}
lxx_fast = lxx_df[lxx_df['lemma'].apply(lambda x: nfc(x) in lxx_targets)].copy()
lxx_fast['pos'] = lxx_fast['lemma'].apply(lambda x: 'verb' if nfc(x) == nfc('νηστεύω') else 'noun')

LXX_BOOK_ORDER = [
    'Exo', 'Jdg', '1Sa', '2Sa', '1Ki', '1Ch', '2Ch', 'Ezr',
    'Est', 'Psa', 'Isa', 'Jer', 'Dan', 'Jol', 'Jon', 'Zec',
]
lxx_v = lxx_fast[lxx_fast['pos'] == 'verb']['book_id'].value_counts()
lxx_n = lxx_fast[lxx_fast['pos'] == 'noun']['book_id'].value_counts()
lxx_books = [b for b in LXX_BOOK_ORDER if b in lxx_v or b in lxx_n]
lxx_v_vals = [lxx_v.get(b, 0) for b in lxx_books]
lxx_n_vals = [lxx_n.get(b, 0) for b in lxx_books]

x3 = range(len(lxx_books))
fig3, ax3 = plt.subplots(figsize=(14, 5))
bv3 = ax3.bar(
    [i - width / 2 for i in x3], lxx_v_vals, width,
    color='#4393c3', label='νηστεύω verb (G3522)')
bn3 = ax3.bar(
    [i + width / 2 for i in x3], lxx_n_vals, width,
    color='#f4a582', label='νηστεία noun (G3521)')
for bar, v in zip(bv3, lxx_v_vals):
    if v:
        ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                 str(v), ha='center', va='bottom', fontsize=9)
for bar, v in zip(bn3, lxx_n_vals):
    if v:
        ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                 str(v), ha='center', va='bottom', fontsize=9)
ax3.set_xticks(list(x3))
ax3.set_xticklabels(lxx_books, fontsize=9)
ax3.set_ylabel('Occurrences', fontsize=10)
ax3.yaxis.grid(True, linestyle='--', alpha=0.4)
ax3.set_axisbelow(True)
ax3.legend(fontsize=9)
ax3.set_title(
    'LXX Fasting Vocabulary by Book\nνηστεύω (G3522) · νηστεία (G3521)',
    fontsize=12, fontweight='bold')
fig3.tight_layout()
p3 = CHART_DIR / 'fasting_lxx_by_book.png'
fig3.savefig(p3, dpi=150, bbox_inches='tight')
plt.close(fig3)
print(f'Chart 3 saved: {p3}')

# ============================================================
# CHART 4: Greek NT by book
# ============================================================

NT_STRONGS = {'G3522', 'G3521', 'G3523', 'G0776', 'G0777'}
nt_fast = nt[nt['strong_g'].isin(NT_STRONGS)].copy()

LEMMA_LABELS = {
    'G3522': 'νηστεύω (verb)',
    'G3521': 'νηστεία (noun)',
    'G3523': 'νῆστις (adj)',
    'G0776': 'ἀσιτία (noun)',
    'G0777': 'ἄσιτος (adj)',
}
NT_BOOK_ORDER = ['Mat', 'Mrk', 'Luk', 'Jhn', 'Act', '1Co', '2Co']
COLORS4 = ['#2b8cbe', '#f4a582', '#74c476', '#e6550d', '#9467bd']

fig4, ax4 = plt.subplots(figsize=(10, 5))
strongs_list = ['G3522', 'G3521', 'G3523', 'G0776', 'G0777']
n_groups = len(strongs_list)
w4 = 0.15
nt_books = [b for b in NT_BOOK_ORDER if b in nt_fast['book'].values]

for j, sg in enumerate(strongs_list):
    sub = nt_fast[nt_fast['strong_g'] == sg]['book'].value_counts()
    vals = [sub.get(b, 0) for b in nt_books]
    offsets = [i + (j - n_groups / 2 + 0.5) * w4 for i in range(len(nt_books))]
    bars4 = ax4.bar(offsets, vals, w4,
                    color=COLORS4[j], label=LEMMA_LABELS[sg])
    for bar, v in zip(bars4, vals):
        if v:
            ax4.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                     str(v), ha='center', va='bottom', fontsize=8)

ax4.set_xticks(list(range(len(nt_books))))
ax4.set_xticklabels(nt_books, fontsize=10)
ax4.set_ylabel('Occurrences', fontsize=10)
ax4.yaxis.grid(True, linestyle='--', alpha=0.4)
ax4.set_axisbelow(True)
ax4.legend(fontsize=9)
ax4.set_title('Greek NT Fasting Vocabulary by Book', fontsize=12, fontweight='bold')
fig4.tight_layout()
p4 = CHART_DIR / 'fasting_greek_nt_by_book.png'
fig4.savefig(p4, dpi=150, bbox_inches='tight')
plt.close(fig4)
print(f'Chart 4 saved: {p4}')

# ============================================================
# CHART 5: Cross-corpus summary
# ============================================================

labels5 = [
    'Heb OT\n(H6684 verb)', 'Heb OT\n(H6685 noun)', 'Aram OT\n(H2908 adv)',
    'LXX\n(G3522 verb)', 'LXX\n(G3521 noun)', 'LXX\n(ἀσιτέω/ἀσιτί)',
    'GK NT\n(G3522 verb)', 'GK NT\n(G3521 noun)', 'GK NT\n(G3523 adj)', 'GK NT\n(G776/777)',
]
counts5 = [21, 26, 1, 23, 27, 3, 21, 8, 2, 2]
corp_colors5 = (
    ['#4393c3'] * 2 +
    ['#6b3a1f'] +
    ['#f4a342'] * 3 +
    ['#41ab5d'] * 4
)
patches5 = [
    mpatches.Patch(color='#4393c3', label='Hebrew OT'),
    mpatches.Patch(color='#6b3a1f', label='Aramaic OT'),
    mpatches.Patch(color='#f4a342', label='LXX'),
    mpatches.Patch(color='#41ab5d', label='Greek NT'),
]

fig5, ax5 = plt.subplots(figsize=(13, 5))
bars5 = ax5.bar(range(len(labels5)), counts5, color=corp_colors5, edgecolor='white', linewidth=0.5)
for bar, v in zip(bars5, counts5):
    ax5.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
             str(v), ha='center', fontsize=11, fontweight='bold')
ax5.set_xticks(range(len(labels5)))
ax5.set_xticklabels(labels5, fontsize=9)
ax5.set_ylabel('Total Occurrences', fontsize=10)
ax5.yaxis.grid(True, linestyle='--', alpha=0.4)
ax5.set_axisbelow(True)
ax5.legend(handles=patches5, fontsize=9)
ax5.set_title('Fasting Vocabulary Across Biblical Corpora', fontsize=13, fontweight='bold')
fig5.tight_layout()
p5 = CHART_DIR / 'fasting_cross_corpus_summary.png'
fig5.savefig(p5, dpi=150, bbox_inches='tight')
plt.close(fig5)
print(f'Chart 5 saved: {p5}')

print('All fasting charts regenerated.')
