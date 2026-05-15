"""Build fasting word-study CSV data exports (Hebrew OT, Aramaic, LXX, Greek NT)."""
import sys
import unicodedata

sys.path.insert(0, 'src')

import pandas as pd  # noqa: E402
from pathlib import Path  # noqa: E402
from bible_grammar.core.syntax_ot import load_syntax_ot  # noqa: E402
from bible_grammar.core.lxx_query import query_lxx  # noqa: E402
from bible_grammar.core._utils import load_nt  # noqa: E402
from bible_grammar.core.db import load_translations  # noqa: E402


def nfc(s: object) -> str:
    return unicodedata.normalize('NFC', str(s))


OUT = Path('output/reports/both/word_studies/fasting')
OUT.mkdir(parents=True, exist_ok=True)

ot = load_syntax_ot()
lxx = query_lxx(include_deuterocanon=False)
nt = load_nt()
trans = load_translations()
kjv = trans[trans['translation'] == 'KJV']


def kjv_text(book: str, ch: int, vs: int) -> str:
    r = kjv[(kjv['book_id'] == book) & (kjv['chapter'] == ch) & (kjv['verse'] == vs)]
    return r['text'].values[0] if len(r) else ''


# ============================================================
# Hebrew OT: H6684 (verb צוּם) + H6685 (noun צוֹם)
# ============================================================

ot_fast = ot[ot['strong_h'].isin(['H6684', 'H6685'])].copy()
ot_fast['pos'] = ot_fast['strong_h'].map({'H6684': 'verb', 'H6685': 'noun'})

ot_rows = []
for _, r in ot_fast.iterrows():
    b, c, v = r['book'], int(r['chapter']), int(r['verse'])
    ot_rows.append({
        'ref': f"{b} {c}:{v}",
        'book': b,
        'chapter': c,
        'verse': v,
        'hebrew': r['text'],
        'strong_h': r['strong_h'],
        'pos': r['pos'],
        'morph': r['morph'],
        'stem': r.get('stem', ''),
        'gloss': r['gloss'],
        'lxx_word': r.get('greek', ''),
        'lxx_strong': r.get('greekstrong', ''),
        'kjv': kjv_text(b, c, v),
    })

ot_df = pd.DataFrame(ot_rows)
ot_out = OUT / 'fasting_hebrew_ot.csv'
ot_df.to_csv(ot_out, index=False)
print(f"Hebrew OT CSV: {len(ot_df)} rows → {ot_out}")

# ============================================================
# Aramaic OT: H2908 (טְוָת, Dan 6:18)
# ============================================================

aram_fast = ot[ot['strong_h'] == 'H2908'].copy()
aram_rows = []
for _, r in aram_fast.iterrows():
    b, c, v = r['book'], int(r['chapter']), int(r['verse'])
    aram_rows.append({
        'ref': f"{b} {c}:{v}",
        'book': b,
        'chapter': c,
        'verse': v,
        'aramaic': r['text'],
        'strong_h': r['strong_h'],
        'pos': 'adverb',
        'morph': r['morph'],
        'gloss': r['gloss'],
        'lxx_word': r.get('greek', ''),
        'lxx_strong': r.get('greekstrong', ''),
        'kjv': kjv_text(b, c, v),
    })

aram_df = pd.DataFrame(aram_rows)
aram_out = OUT / 'fasting_aramaic_ot.csv'
aram_df.to_csv(aram_out, index=False)
print(f"Aramaic OT CSV: {len(aram_df)} rows → {aram_out}")

# ============================================================
# LXX: νηστεύω (G3522) + νηστεία (G3521)
# ============================================================

# Core fasting terms: νηστεύω (G3522) / νηστεία (G3521)
_lxx_targets = {nfc('νηστεύω'), nfc('νηστεία')}
lxx_fast = lxx[lxx['lemma'].apply(lambda x: nfc(x) in _lxx_targets)].copy()

# Related ἀσιτ- terms (verb ἀσιτέω and adverb ἀσιτί; only in Deuterocanon/LXX pluses)
from bible_grammar.core.lxx_query import query_lxx as _query_lxx_full  # noqa: E402
lxx_full = _query_lxx_full(include_deuterocanon=True)
_asit_targets = {nfc('ἀσιτέω'), nfc('ἀσιτί')}
lxx_asit = lxx_full[lxx_full['lemma'].apply(lambda x: nfc(x) in _asit_targets)].copy()

lxx_rows = []
for _, r in pd.concat([lxx_fast, lxx_asit], ignore_index=True).iterrows():
    b, c, v = r['book_id'], int(r['chapter']), int(r['verse'])
    lem = nfc(r['lemma'])
    if lem == nfc('νηστεύω'):
        pos = 'verb'
    elif lem == nfc('νηστεία'):
        pos = 'noun'
    elif lem == nfc('ἀσιτέω'):
        pos = 'verb'
    else:
        pos = 'adverb'
    lxx_rows.append({
        'ref': f"{b} {c}:{v}",
        'book': b,
        'chapter': c,
        'verse': v,
        'greek': r['word'],
        'lemma': r['lemma'],
        'strong_g': r['strongs'],
        'pos': pos,
        'morph': r['morph_code'],
        'kjv': kjv_text(b, c, v),
    })

lxx_df = pd.DataFrame(lxx_rows)
lxx_out = OUT / 'fasting_lxx.csv'
lxx_df.to_csv(lxx_out, index=False)
print(f"LXX CSV: {len(lxx_df)} rows → {lxx_out}")

# ============================================================
# Greek NT: G3522, G3521, G3523, G0776, G0777
# ============================================================

nt_strongs = {'G3522', 'G3521', 'G3523', 'G0776', 'G0777'}
nt_fast = nt[nt['strong_g'].isin(nt_strongs)].copy()

nt_rows = []
for _, r in nt_fast.iterrows():
    b, c, v = r['book'], int(r['chapter']), int(r['verse'])
    nt_rows.append({
        'ref': f"{b} {c}:{v}",
        'book': b,
        'chapter': c,
        'verse': v,
        'greek': r['text'],
        'lemma': r['lemma'],
        'strong_g': r['strong_g'],
        'pos': r['class_'],
        'morph': r['morph'],
        'tense': r.get('tense', ''),
        'voice': r.get('voice', ''),
        'mood': r.get('mood', ''),
        'gloss': r['gloss'],
        'kjv': kjv_text(b, c, v),
    })

nt_df = pd.DataFrame(nt_rows)
nt_out = OUT / 'fasting_greek_nt.csv'
nt_df.to_csv(nt_out, index=False)
print(f"Greek NT CSV: {len(nt_df)} rows → {nt_out}")

print("Done. All fasting CSVs generated.")
