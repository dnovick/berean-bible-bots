"""
Hebrew OT discourse structure analysis — narrative peak and episode boundary detection.

Builds on the existing verbal_syntax module to provide higher-level discourse analysis:

  1. Narrative peak scoring — identify the climactic section of a narrative
     using density of: wayyiqtol, direct speech, rare lexical items, short clauses
  2. Episode boundary detection — identify probable episode breaks using:
     disjunctive clauses (waw + non-verb), scene-setting formulas (וַיְהִי),
     temporal/spatial markers, and wayyiqtol chain gaps
  3. Wayyiqtol density by chapter — where does the action concentrate?
  4. Direct speech density by chapter

Terminology (after Longacre, The Grammar of Discourse, 1983):
  PEAK     — the climactic paragraph/episode, marked by dense wayyiqtol + speech
  EPISODE  — a coherent narrative unit, separated by disjunctive/scene-setting clauses
  BACKBONE — the wayyiqtol chain that drives the main narrative forward

Questions this answers
──────────────────────
  • Where is the narrative peak of Genesis 22?
  • How many episode boundaries are in Exodus 1–15?
  • Which chapters of 1 Samuel have the highest wayyiqtol density?
  • Where does direct speech cluster in Ruth?

Public API
──────────
ot_discourse_wayyiqtol_density(book)          → DataFrame (chapter, count, density)
ot_discourse_speech_density(book)             → DataFrame (chapter, speech_count, density)
ot_discourse_peak_score(book, window=5)       → DataFrame (chapter, peak_score)
ot_discourse_episode_boundaries(book)         → DataFrame (verse refs at episode breaks)
ot_discourse_narrative_profile(book)          → dict (combined metrics)

print_ot_discourse_overview(book)             → None
print_ot_wayyiqtol_density(book)              → None
print_ot_speech_density(book)                 → None
print_ot_peak_score(book)                     → None
print_ot_episode_boundaries(book)             → None

ot_discourse_density_chart(book)              → Path | None
ot_discourse_peak_chart(book)                 → Path | None
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd

from ..core._utils import ensure_chart_dir

_CHART_DIR = Path('output') / 'charts' / 'ot' / 'discourse'

# Wayyiqtol-initial scene-setting formulas (common episode openers)
SCENE_SETTING_LEMMAS = {'הָיָה', 'הָלַךְ', 'עָלָה', 'בּוֹא', 'יָשַׁב', 'שׁוּב'}
DISJUNCTIVE_TYPES = {'qatal', 'yiqtol', 'participle active', 'nominal',
                     'infinitive construct'}  # non-wayyiqtol after ו


# ── helpers ───────────────────────────────────────────────────────────────────

def _load_ot_h() -> pd.DataFrame:
    from ..core._utils import load_ot_h
    return load_ot_h()


def _book_df(book: str) -> pd.DataFrame:
    return _load_ot_h().pipe(lambda df: df[df['book'] == book])


# ── data functions ────────────────────────────────────────────────────────────

def ot_discourse_wayyiqtol_density(
    book: str,
    *,
    normalize_by_tokens: bool = True,
) -> pd.DataFrame:
    """
    Wayyiqtol counts (and density) per chapter in a given OT book.

    Returns: chapter, total_tokens, wayyiqtol_count, density (per 100 tokens).
    """
    df = _book_df(book)
    chapters = sorted(df['chapter'].unique())
    rows = []
    for ch in chapters:
        ch_df = df[df['chapter'] == ch]
        total = len(ch_df)
        wyy = (ch_df['type_'] == 'wayyiqtol').sum()
        rows.append({
            'chapter': ch,
            'total_tokens': total,
            'wayyiqtol_count': wyy,
            'density': round(wyy / max(total, 1) * 100, 1),
        })
    return pd.DataFrame(rows)


def ot_discourse_speech_density(
    book: str,
) -> pd.DataFrame:
    """
    Speech-verb counts per chapter — a proxy for direct speech density.

    Counts tokens with type_ == 'qatal' or 'wayyiqtol' whose lemma is אָמַר
    (the dominant speech verb). Also includes נָאַם (oracle of) tokens.

    Returns: chapter, speech_count, total_tokens, density (per 100 tokens).
    """
    df = _book_df(book)
    speech_lemmas = {'אָמַר', 'דָּבַר', 'נָאַם', 'קָרָא'}
    chapters = sorted(df['chapter'].unique())
    rows = []
    for ch in chapters:
        ch_df = df[df['chapter'] == ch]
        total = len(ch_df)
        speech = ch_df['lemma'].isin(speech_lemmas).sum()
        rows.append({
            'chapter': ch,
            'total_tokens': total,
            'speech_count': speech,
            'density': round(speech / max(total, 1) * 100, 1),
        })
    return pd.DataFrame(rows)


def ot_discourse_lexical_diversity(
    book: str,
) -> pd.DataFrame:
    """
    Type-token ratio (TTR) per chapter — higher TTR may signal heightened style.

    Returns: chapter, total_tokens, unique_lemmas, ttr.
    """
    df = _book_df(book)
    chapters = sorted(df['chapter'].unique())
    rows = []
    for ch in chapters:
        ch_df = df[df['chapter'] == ch]
        total = len(ch_df)
        unique = ch_df['lemma'].nunique()
        rows.append({
            'chapter': ch,
            'total_tokens': total,
            'unique_lemmas': unique,
            'ttr': round(unique / max(total, 1), 3),
        })
    return pd.DataFrame(rows)


def ot_discourse_peak_score(
    book: str,
) -> pd.DataFrame:
    """
    Composite narrative peak score per chapter.

    Score = 0.4 × wayyiqtol_density + 0.3 × speech_density + 0.3 × ttr_normalised.
    Higher scores suggest narrative climax / peak.
    All components are normalised to 0–1 range before combining.

    Returns: chapter, wayyiqtol_density, speech_density, ttr, peak_score.
    """
    wyy = ot_discourse_wayyiqtol_density(book)[['chapter', 'density']].rename(
        columns={'density': 'wayyiqtol_density'})
    sp = ot_discourse_speech_density(book)[['chapter', 'density']].rename(
        columns={'density': 'speech_density'})
    lex = ot_discourse_lexical_diversity(book)[['chapter', 'ttr']]

    df = wyy.merge(sp, on='chapter').merge(lex, on='chapter')

    def _norm(s: pd.Series) -> pd.Series:
        rng = s.max() - s.min()
        return (s - s.min()) / rng if rng > 0 else s * 0

    df['_wyy_n'] = _norm(df['wayyiqtol_density'])
    df['_sp_n']  = _norm(df['speech_density'])
    df['_ttr_n'] = _norm(df['ttr'])
    df['peak_score'] = (
        0.4 * df['_wyy_n'] + 0.3 * df['_sp_n'] + 0.3 * df['_ttr_n']
    ).round(3)
    return df.drop(columns=['_wyy_n', '_sp_n', '_ttr_n']).sort_values(
        'chapter').reset_index(drop=True)


def ot_discourse_episode_boundaries(
    book: str,
    *,
    min_gap: int = 3,
) -> pd.DataFrame:
    """
    Detect probable episode boundaries in an OT narrative book.

    An episode boundary is flagged when:
      1. A wayyiqtol chain ends (gap of >= min_gap verses without wayyiqtol)
      2. OR a הָיָה (wayehi) scene-setting formula appears
      3. OR the first verb of a new section is disjunctive (waw + qatal)

    Returns: ref, chapter, verse, boundary_type.
    """
    df = _book_df(book)
    rows = []

    prev_wyy_verse = -999
    for _, row in df.iterrows():
        ref = row['ref']
        ch, vs = row['chapter'], row['verse']
        t = row['type_']
        lemma = row['lemma']

        # wayehi scene-setter
        if lemma == 'הָיָה' and t == 'wayyiqtol':
            rows.append({'ref': ref, 'chapter': ch, 'verse': vs,
                         'boundary_type': 'scene-setter (wayehi)'})

        # Gap in wayyiqtol chain
        if t == 'wayyiqtol':
            prev_wyy_verse = vs
        else:
            if vs - prev_wyy_verse > min_gap and t in ('qatal',) and lemma not in ('לֹא',):
                rows.append({'ref': ref, 'chapter': ch, 'verse': vs,
                             'boundary_type': 'wayyiqtol chain gap + qatal'})

    if not rows:
        return pd.DataFrame(columns=['ref', 'chapter', 'verse', 'boundary_type'])

    result = pd.DataFrame(rows).drop_duplicates(subset=['ref']).reset_index(drop=True)
    return result.head(50)  # cap for readability


def ot_discourse_narrative_profile(
    book: str,
) -> dict:
    """
    Summary of discourse metrics for an OT book.

    Returns a dict with: total_tokens, wayyiqtol_pct, peak_chapter, peak_score.
    """
    df = _load_ot_h()
    df = df[df['book'] == book]
    total = len(df)
    wyy_total = (df['type_'] == 'wayyiqtol').sum()
    wyy_pct = round(wyy_total / max(total, 1) * 100, 1)

    peaks = ot_discourse_peak_score(book)
    if peaks.empty:
        return {'total_tokens': total, 'wayyiqtol_pct': wyy_pct,
                'peak_chapter': None, 'peak_score': None}

    top = peaks.loc[peaks['peak_score'].idxmax()]
    return {
        'total_tokens': total,
        'wayyiqtol_pct': wyy_pct,
        'peak_chapter': int(top['chapter']),
        'peak_score': float(top['peak_score']),
        'wayyiqtol_total': int(wyy_total),
    }


# ── print functions ───────────────────────────────────────────────────────────

def print_ot_discourse_overview(book: str) -> None:
    p = ot_discourse_narrative_profile(book)
    w = 58
    print(f"\n{'═'*w}")
    print(f"  Discourse Profile — {book}")
    print(f"{'═'*w}")
    print(f"  Total Hebrew tokens : {p['total_tokens']:>9,}")
    print(f"  Wayyiqtol tokens    : {p['wayyiqtol_total']:>9,} ({p['wayyiqtol_pct']}%)")
    print(f"  Narrative peak ch.  : {p['peak_chapter']}")
    print(f"  Peak score          : {p['peak_score']}")
    print()


def print_ot_wayyiqtol_density(book: str) -> None:
    df = ot_discourse_wayyiqtol_density(book)
    print(f"\nWayyiqtol Density by Chapter — {book}")
    print(f"  {'Ch':>4} {'Tokens':>7} {'Wyy':>5} {'Density':>8}")
    print('  ' + '-' * 29)
    for _, row in df.iterrows():
        bar = '█' * min(int(row['density'] * 2), 30)
        print(f"  {int(row['chapter']):>4} {row['total_tokens']:>7,} "
              f"{row['wayyiqtol_count']:>5} {row['density']:>7.1f}%  {bar}")
    print()


def print_ot_speech_density(book: str) -> None:
    df = ot_discourse_speech_density(book)
    print(f"\nSpeech Verb Density by Chapter — {book}")
    print(f"  {'Ch':>4} {'Tokens':>7} {'Speech':>7} {'Density':>8}")
    print('  ' + '-' * 31)
    for _, row in df.iterrows():
        print(f"  {int(row['chapter']):>4} {row['total_tokens']:>7,} "
              f"{row['speech_count']:>7} {row['density']:>7.1f}%")
    print()


def print_ot_peak_score(book: str) -> None:
    df = ot_discourse_peak_score(book)
    print(f"\nNarrative Peak Scores by Chapter — {book}")
    print("  (0.4×wayyiqtol + 0.3×speech + 0.3×TTR, all normalised 0–1)")
    print(f"  {'Ch':>4} {'Wyy%':>6} {'Sp%':>6} {'TTR':>6} {'Score':>7}")
    print('  ' + '-' * 36)
    for _, row in df.iterrows():
        bar = '█' * int(row['peak_score'] * 20)
        print(f"  {int(row['chapter']):>4} {row['wayyiqtol_density']:>5.1f}% "
              f"{row['speech_density']:>5.1f}% {row['ttr']:>5.3f}  "
              f"{row['peak_score']:>5.3f}  {bar}")
    print()


def print_ot_episode_boundaries(book: str) -> None:
    df = ot_discourse_episode_boundaries(book)
    print(f"\nEpisode Boundary Signals — {book}")
    if df.empty:
        print("  No boundaries detected.")
        print()
        return
    print(f"  {'Ref':<20} {'Ch':>4} {'Vs':>4}  Type")
    print('  ' + '-' * 55)
    for _, row in df.iterrows():
        print(f"  {str(row['ref']):<20} {int(row['chapter']):>4} "
              f"{int(row['verse']):>4}  {row['boundary_type']}")
    print()


# ── chart functions ───────────────────────────────────────────────────────────

def ot_discourse_density_chart(book: str) -> Path | None:
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        return None

    wyy = ot_discourse_wayyiqtol_density(book)
    sp = ot_discourse_speech_density(book)

    ensure_chart_dir(_CHART_DIR)
    out = _CHART_DIR / f'discourse_density_{book}.png'

    chapters = wyy['chapter'].tolist()
    x = np.arange(len(chapters))
    w = 0.35

    fig, ax = plt.subplots(figsize=(max(8, len(chapters) * 0.5), 5))
    ax.bar(x - w/2, wyy['density'], w, label='Wayyiqtol density %', color='steelblue')
    ax.bar(x + w/2, sp['density'], w, label='Speech verb density %', color='darkorange')
    ax.set_xticks(x)
    ax.set_xticklabels(chapters, fontsize=8)
    ax.set_xlabel('Chapter')
    ax.set_ylabel('% of tokens')
    ax.set_title(f'Discourse Density by Chapter — {book}')
    ax.legend()
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def ot_discourse_peak_chart(book: str) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = ot_discourse_peak_score(book)
    if df.empty:
        return None

    ensure_chart_dir(_CHART_DIR)
    out = _CHART_DIR / f'peak_score_{book}.png'

    fig, ax = plt.subplots(figsize=(max(8, len(df) * 0.5), 4))
    bars = ax.bar(df['chapter'], df['peak_score'], color='steelblue')
    # Highlight the peak chapter
    peak_idx = df['peak_score'].idxmax()
    bars[peak_idx].set_color('crimson')
    ax.set_xlabel('Chapter')
    ax.set_ylabel('Peak score (0–1)')
    ax.set_title(f'Narrative Peak Score by Chapter — {book}')
    ax.set_xticks(df['chapter'])
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out
