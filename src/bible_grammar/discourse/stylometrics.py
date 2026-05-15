"""
Register and style analysis — authorship stylometrics for the Hebrew OT and Greek NT.

Quantitative style metrics that capture lexical richness, syntactic register,
and morphological fingerprints for individual books or proposed authorial units.

Hebrew metrics
──────────────
  ttr                — type-token ratio (unique lemmas / total tokens)
  msttr              — mean segmental TTR (window-based, fair for cross-length comparison)
  hapax_density      — hapax lemma tokens / total tokens (%)
  wayyiqtol_density  — wayyiqtol tokens / total tokens (%)
  inf_construct_density — infinitive constructs per 1,000 tokens
  asher_density      — אֲשֶׁר (relative clause marker) per 1,000 tokens
  particle_density   — key discourse particles per 1,000 tokens
  verb_pct           — verbal tokens as % of total
  noun_pct           — nominal tokens as % of total

Greek metrics
─────────────
  ttr
  msttr
  hapax_density
  ptc_to_finite_ratio — participle tokens / finite verb tokens
  optative_density    — optative verbs per 1,000 tokens
  hina_density        — ἵνα per 1,000 tokens
  inf_density         — infinitive verbs per 1,000 tokens
  verb_pct
  noun_pct

Questions this answers
──────────────────────
  • Is Isaiah 1–39 stylistically different from Isaiah 40–66?
  • Which Pauline letters cluster together by style?
  • How does Mark's Greek compare to Luke's in participle usage?
  • Which OT books have the richest vocabulary (MSTTR)?

Public API
──────────
book_style_profile(book, lang)           → dict of all style metrics
style_comparison(books, lang)            → DataFrame (books × metrics)
msttr(book, lang, window)                → float

print_style_profile(book, lang)          → None
print_style_comparison(books, lang)      → None

style_radar_chart(books, lang)           → Path | None
style_heatmap(books, lang)               → Path | None
"""

from __future__ import annotations
from pathlib import Path

import pandas as pd

from ..core._utils import ensure_chart_dir

_CHART_DIR = Path('output') / 'charts' / 'stylometrics'

# Hebrew discourse particles tracked for density metric
_HEB_PARTICLES = {'כִּי', 'אֲשֶׁר', 'הִנֵּה', 'לָכֵן', 'גַּם', 'רַק', 'כִּי-אִם'}

# Hebrew SP values that count as "verbal"
_HEB_VERBAL_TYPES = {'wayyiqtol', 'qatal', 'yiqtol', 'imperative', 'cohortative',
                     'jussive', 'participle active', 'participle passive',
                     'infinitive construct', 'infinitive absolute'}

# Greek SP values
_GK_FINITE_MOODS = {'indicative', 'subjunctive', 'imperative', 'optative'}


# ── helpers ───────────────────────────────────────────────────────────────────

def _load_ot_h() -> pd.DataFrame:
    from ..core._utils import load_ot_h
    return load_ot_h()


def _load_nt() -> pd.DataFrame:
    from ..core._utils import load_nt
    return load_nt()


def _book_tokens(book: str, lang: str) -> pd.DataFrame:
    if lang == 'H':
        df = _load_ot_h()
    else:
        df = _load_nt()
    return df[df['book'] == book].reset_index(drop=True)


def _compute_msttr(lemmas: list[str], window: int) -> float:
    """Mean Segmental TTR: average TTR over non-overlapping windows of size `window`."""
    ttrs = []
    for i in range(0, len(lemmas) - window + 1, window):
        seg = lemmas[i:i + window]
        ttrs.append(len(set(seg)) / len(seg))
    return round(sum(ttrs) / len(ttrs), 4) if ttrs else 0.0


def _hapax_density_pct(df: pd.DataFrame) -> float:
    lemma_counts = df['lemma'].value_counts()
    hapax_lemmas = set(lemma_counts[lemma_counts == 1].index)
    hapax_tokens = df['lemma'].isin(hapax_lemmas).sum()
    return round(hapax_tokens / max(len(df), 1) * 100, 2)


# ── data functions ────────────────────────────────────────────────────────────

def msttr(book: str, *, lang: str = 'H', window: int = 1000) -> float:
    """Mean Segmental TTR for a book. Window default = 1,000 tokens."""
    df = _book_tokens(book, lang)
    return _compute_msttr(df['lemma'].tolist(), window)


def book_style_profile(book: str, *, lang: str = 'H') -> dict:
    """
    Compute all style metrics for a single book.

    Returns a dict keyed by metric name. All density values are
    per 1,000 tokens unless otherwise noted.
    """
    df = _book_tokens(book, lang)
    if df.empty:
        return {}

    total = len(df)
    lemmas = df['lemma'].tolist()
    ttr_val = round(len(set(lemmas)) / total, 4)
    msttr_val = _compute_msttr(lemmas, 1000)
    hapax = _hapax_density_pct(df)

    if lang == 'H':
        type_col = 'type_' if 'type_' in df.columns else None
        sp_col = 'sp' if 'sp' in df.columns else None

        wyy = (df['type_'] == 'wayyiqtol').sum() / total * 100 if type_col else 0.0
        inf_c = (df['type_'] == 'infinitive construct').sum() / total * 1000 if type_col else 0.0
        asher = (df['lemma'] == 'אֲשֶׁר').sum() / total * 1000
        particle = df['lemma'].isin(_HEB_PARTICLES).sum() / total * 1000
        verbal = (df['type_'].isin(_HEB_VERBAL_TYPES).sum() / total * 100
                  if type_col else 0.0)
        # noun/adj proxy: sp contains 'subs' or 'adjv' in MACULA
        if sp_col:
            noun_pct = df['sp'].isin({'subs', 'noun', 'adjv', 'nmpr'}).sum() / total * 100
        else:
            noun_pct = 0.0

        return {
            'book': book,
            'total_tokens': total,
            'ttr': ttr_val,
            'msttr_1k': msttr_val,
            'hapax_density_pct': hapax,
            'wayyiqtol_density_pct': round(wyy, 2),
            'inf_construct_per1k': round(inf_c, 2),
            'asher_per1k': round(asher, 2),
            'particle_per1k': round(particle, 2),
            'verbal_pct': round(verbal, 2),
            'noun_pct': round(noun_pct, 2),
        }

    else:  # Greek NT
        mood_col = 'mood' if 'mood' in df.columns else None

        if mood_col:
            ptc = (df['mood'] == 'participle').sum()
            finite = df['mood'].isin(_GK_FINITE_MOODS).sum()
            ptc_ratio = round(ptc / max(finite, 1), 4)
            opt = (df['mood'] == 'optative').sum() / total * 1000
            inf = (df['mood'] == 'infinitive').sum() / total * 1000
        else:
            ptc_ratio = opt = inf = 0.0

        hina = (df['lemma'] == 'ἵνα').sum() / total * 1000
        sp_col = 'sp' if 'sp' in df.columns else None
        if sp_col and mood_col:
            verbal_pct = df['mood'].notna().sum() / total * 100
            noun_pct = df['sp'].isin({'noun', 'det', 'pron'}).sum() / total * 100
        else:
            verbal_pct = noun_pct = 0.0

        return {
            'book': book,
            'total_tokens': total,
            'ttr': ttr_val,
            'msttr_1k': msttr_val,
            'hapax_density_pct': hapax,
            'ptc_to_finite_ratio': ptc_ratio,
            'optative_per1k': round(opt, 2),
            'hina_per1k': round(hina, 2),
            'inf_per1k': round(inf, 2),
            'verbal_pct': round(verbal_pct, 2),
            'noun_pct': round(noun_pct, 2),
        }


def style_comparison(
    books: list[str],
    *,
    lang: str = 'H',
) -> pd.DataFrame:
    """
    Style metrics for a list of books, side by side.

    Returns a DataFrame with books as rows and style metrics as columns.
    Counts are normalized per 1,000 tokens where applicable.
    """
    rows = [book_style_profile(b, lang=lang) for b in books]
    rows = [r for r in rows if r]
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).set_index('book')


# ── print functions ───────────────────────────────────────────────────────────

def print_style_profile(book: str, *, lang: str = 'H') -> None:
    p = book_style_profile(book, lang=lang)
    if not p:
        print(f"No data for {book} (lang={lang})")
        return
    lang_label = 'Hebrew' if lang == 'H' else 'Greek'
    w = 58
    print(f"\n{'═'*w}")
    print(f"  Style Profile — {book} ({lang_label})")
    print(f"{'═'*w}")
    print(f"  Total tokens         : {p['total_tokens']:>9,}")
    print(f"  Type-Token Ratio     : {p['ttr']:>9.4f}")
    print(f"  MSTTR (1k window)    : {p['msttr_1k']:>9.4f}")
    print(f"  Hapax density        : {p['hapax_density_pct']:>8.2f}%")
    if lang == 'H':
        print(f"  Wayyiqtol density    : {p['wayyiqtol_density_pct']:>8.2f}%")
        print(f"  Inf. construct/1k    : {p['inf_construct_per1k']:>9.2f}")
        print(f"  אֲשֶׁר per 1k          : {p['asher_per1k']:>9.2f}")
        print(f"  Particle density/1k  : {p['particle_per1k']:>9.2f}")
        print(f"  Verbal tokens        : {p['verbal_pct']:>8.2f}%")
        print(f"  Noun tokens          : {p['noun_pct']:>8.2f}%")
    else:
        print(f"  Ptc-to-finite ratio  : {p['ptc_to_finite_ratio']:>9.4f}")
        print(f"  Optative per 1k      : {p['optative_per1k']:>9.2f}")
        print(f"  ἵνα per 1k           : {p['hina_per1k']:>9.2f}")
        print(f"  Infinitive per 1k    : {p['inf_per1k']:>9.2f}")
        print(f"  Verbal tokens        : {p['verbal_pct']:>8.2f}%")
        print(f"  Noun tokens          : {p['noun_pct']:>8.2f}%")
    print()


def print_style_comparison(
    books: list[str],
    *,
    lang: str = 'H',
) -> None:
    df = style_comparison(books, lang=lang)
    if df.empty:
        print("No data.")
        return
    lang_label = 'Hebrew' if lang == 'H' else 'Greek'
    print(f"\nStyle Comparison ({lang_label})")
    print(f"  {'Metric':<26}" + ''.join(f"  {b:>8}" for b in df.index))
    print('  ' + '-' * (26 + 10 * len(df)))

    def _row(label: str, col: str) -> None:
        if col not in df.columns:
            return
        line = f"  {label:<26}"
        for val in df[col]:
            if isinstance(val, float):
                line += f"  {val:>8.3f}"
            else:
                line += f"  {val:>8}"
        print(line)

    _row('Total tokens', 'total_tokens')
    _row('TTR', 'ttr')
    _row('MSTTR (1k)', 'msttr_1k')
    _row('Hapax density %', 'hapax_density_pct')
    if lang == 'H':
        _row('Wayyiqtol %', 'wayyiqtol_density_pct')
        _row('Inf. construct/1k', 'inf_construct_per1k')
        _row('אֲשֶׁר per 1k', 'asher_per1k')
        _row('Particles/1k', 'particle_per1k')
        _row('Verbal %', 'verbal_pct')
        _row('Noun %', 'noun_pct')
    else:
        _row('Ptc/finite ratio', 'ptc_to_finite_ratio')
        _row('Optative/1k', 'optative_per1k')
        _row('ἵνα/1k', 'hina_per1k')
        _row('Infinitive/1k', 'inf_per1k')
        _row('Verbal %', 'verbal_pct')
        _row('Noun %', 'noun_pct')
    print()


# ── chart functions ───────────────────────────────────────────────────────────

_RADAR_METRICS_H = [
    'ttr', 'msttr_1k', 'hapax_density_pct',
    'wayyiqtol_density_pct', 'inf_construct_per1k',
    'asher_per1k', 'particle_per1k',
]
_RADAR_LABELS_H = [
    'TTR', 'MSTTR', 'Hapax %',
    'Wayyiqtol %', 'Inf. Constr./1k',
    'אֲשֶׁר/1k', 'Particles/1k',
]
_RADAR_METRICS_G = [
    'ttr', 'msttr_1k', 'hapax_density_pct',
    'ptc_to_finite_ratio', 'optative_per1k',
    'hina_per1k', 'inf_per1k',
]
_RADAR_LABELS_G = [
    'TTR', 'MSTTR', 'Hapax %',
    'Ptc/Finite', 'Optative/1k',
    'ἵνα/1k', 'Inf./1k',
]


def style_radar_chart(
    books: list[str],
    *,
    lang: str = 'H',
) -> Path | None:
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        return None

    df = style_comparison(books, lang=lang)
    if df.empty:
        return None

    metrics = _RADAR_METRICS_H if lang == 'H' else _RADAR_METRICS_G
    labels = _RADAR_LABELS_H if lang == 'H' else _RADAR_LABELS_G
    metrics = [m for m in metrics if m in df.columns]
    labels = labels[:len(metrics)]

    # Normalise each metric to 0–1
    mat = df[metrics].copy().astype(float)
    for col in mat.columns:
        rng = mat[col].max() - mat[col].min()
        mat[col] = (mat[col] - mat[col].min()) / rng if rng > 0 else 0.0

    n = len(metrics)
    angles = [i / n * 2 * np.pi for i in range(n)] + [0]

    ensure_chart_dir(_CHART_DIR)
    safe = '_'.join(books[:4])
    out = _CHART_DIR / f'radar_{safe}_{lang}.png'

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'polar': True})
    colors = plt.cm.tab10.colors  # type: ignore[attr-defined]
    for idx, (book, row) in enumerate(mat.iterrows()):
        vals = row[metrics].tolist() + [row[metrics[0]]]
        ax.plot(angles, vals, color=colors[idx % len(colors)], linewidth=2, label=book)
        ax.fill(angles, vals, color=colors[idx % len(colors)], alpha=0.08)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_yticklabels([])
    lang_label = 'Hebrew' if lang == 'H' else 'Greek'
    ax.set_title(f'Style Radar — {lang_label}', fontsize=13, pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    return out


def style_heatmap(
    books: list[str],
    *,
    lang: str = 'H',
) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = style_comparison(books, lang=lang)
    if df.empty:
        return None

    metrics = _RADAR_METRICS_H if lang == 'H' else _RADAR_METRICS_G
    labels = _RADAR_LABELS_H if lang == 'H' else _RADAR_LABELS_G
    metrics = [m for m in metrics if m in df.columns]
    labels = labels[:len(metrics)]

    # Z-score normalise columns for heatmap contrast
    mat = df[metrics].copy().astype(float)
    for col in mat.columns:
        std = mat[col].std()
        mat[col] = (mat[col] - mat[col].mean()) / std if std > 0 else 0.0

    ensure_chart_dir(_CHART_DIR)
    safe = '_'.join(books[:6])
    out = _CHART_DIR / f'heatmap_{safe}_{lang}.png'

    lang_label = 'Hebrew' if lang == 'H' else 'Greek'
    fig, ax = plt.subplots(figsize=(max(8, len(metrics) * 1.2), max(4, len(books) * 0.6)))
    im = ax.imshow(mat.values, aspect='auto', cmap='RdBu', vmin=-2, vmax=2)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=35, ha='right', fontsize=9)
    ax.set_yticks(range(len(mat.index)))
    ax.set_yticklabels(mat.index, fontsize=9)
    plt.colorbar(im, ax=ax, label='Z-score')
    ax.set_title(f'Style Heatmap ({lang_label}) — Z-normalised')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out
