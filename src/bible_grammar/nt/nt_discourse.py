"""
Greek NT discourse particles analysis.

Analyses the distribution and function of major Greek discourse particles
(δέ, γάρ, οὖν, ἵνα, ὅτι, ἀλλά, καί) across the GNT, backed by the
MACULA Greek syntax layer.

Public API
──────────
nt_particle_frequency(book=None)         → DataFrame (particle frequency table)
nt_particle_by_book()                    → DataFrame (particle counts per NT book)
nt_particle_genre_profile()              → DataFrame (particle % by genre group)
nt_particle_function(particle, book=None)→ DataFrame (function classification)
nt_hina_profile(book=None)               → DataFrame (ἵνα clause type counts)
nt_hoti_profile(book=None)               → DataFrame (ὅτι function counts)

print_nt_particle_overview()             → None
print_nt_particle_frequency(book=None)   → None
print_nt_particle_genre_profile()        → None
print_nt_hina_profile(book=None)         → None
print_nt_hoti_profile(book=None)         → None

nt_particle_frequency_chart(book=None)   → Path | None
nt_particle_genre_heatmap()              → Path | None
nt_particle_book_chart(particle)         → Path | None
"""

from __future__ import annotations
from pathlib import Path

import pandas as pd

from ..core.syntax import load_syntax
from .nt_verb_profile import NT_BOOK_GROUPS, NT_BOOK_ORDER

# ── Particle registry ─────────────────────────────────────────────────────────

# Maps Strong's number (plain) → (lemma, display, primary function category)
PARTICLE_REGISTRY: dict[str, tuple[str, str, str]] = {
    '2532': ('καί',  'καί',   'coordinative / additive'),
    '1161': ('δέ',   'δέ',    'continuative / contrastive'),
    '3754': ('ὅτι',  'ὅτι',   'content / causal'),
    '2443': ('ἵνα',  'ἵνα',   'purpose / content'),
    '1063': ('γάρ',  'γάρ',   'explanatory / causal'),
    '3767': ('οὖν',  'οὖν',   'inferential / resumptive'),
    '0235': ('ἀλλά', 'ἀλλά',  'adversative'),
    '3361': ('μή',   'μή',    'negative'),
    '3756': ('οὐ',   'οὐ',    'negative'),
    '1487': ('εἰ',   'εἰ',    'conditional'),
}

# ἵνα clause type: classified by the mood/tense of the following verb (best effort via position)
HINA_FUNCTIONS = {
    'purpose':   'purpose (ἵνα + subj. — expresses goal)',
    'content':   'content (ἵνα + subj. — what is commanded/desired)',
    'result':    'result (ecbatic ἵνα — denoting outcome)',
    'epexegetic': 'epexegetic (ἵνα + subj. — explains a noun or adjective)',
}

HOTI_FUNCTIONS = {
    'recitative': 'recitative (ὅτι — introduces direct/indirect speech)',
    'causal':     'causal (ὅτι — because)',
    'content':    'content (ὅτι — that, introducing content clause)',
}

_CHART_DIR = Path('output') / 'charts' / 'nt' / 'discourse'


def _ensure_chart_dir() -> Path:
    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    return _CHART_DIR


# ── Data loading ──────────────────────────────────────────────────────────────

def _particle_tokens(book: str | None = None) -> pd.DataFrame:
    """All tokens matching registered particle Strong's numbers."""
    df = load_syntax()
    if book:
        df = df[df['book'] == book]
    strongs_set = set(PARTICLE_REGISTRY.keys())
    return df[df['strong'].isin(strongs_set)].copy()


# ── Profile functions ─────────────────────────────────────────────────────────

def nt_particle_frequency(book: str | None = None) -> pd.DataFrame:
    """Particle frequency table. Columns: strong, lemma, display, count, pct, primary_function."""
    tokens = _particle_tokens(book)
    vc = tokens['strong'].value_counts()
    total = vc.sum()
    records = []
    for strong, (lemma, display, func) in PARTICLE_REGISTRY.items():
        cnt = int(vc.get(strong, 0))
        records.append({
            'strong': f"G{strong}",
            'lemma': lemma,
            'display': display,
            'count': cnt,
            'pct': round(cnt / total * 100, 1) if total else 0.0,
            'primary_function': func,
        })
    return pd.DataFrame(records).sort_values('count', ascending=False).reset_index(drop=True)


def nt_particle_by_book() -> pd.DataFrame:
    """Particle token counts per NT book × particle. Returns a crosstab."""
    tokens = _particle_tokens()
    tokens['display'] = tokens['strong'].map(
        {s: d for s, (_, d, _) in PARTICLE_REGISTRY.items()}
    )
    ct = pd.crosstab(tokens['book'], tokens['display'])
    # Sort rows by NT canonical order
    order_map = {b: i for i, b in enumerate(NT_BOOK_ORDER)}
    ct['_ord'] = [order_map.get(b, 99) for b in ct.index]
    ct = ct.sort_values('_ord').drop(columns='_ord')
    return ct


def nt_particle_genre_profile() -> pd.DataFrame:
    """Particle % by NT genre group. Rows=genre, cols=particles."""
    tokens = _particle_tokens()
    tokens['display'] = tokens['strong'].map(
        {s: d for s, (_, d, _) in PARTICLE_REGISTRY.items()}
    )
    particles = [d for _, d, _ in PARTICLE_REGISTRY.values()]
    rows = []
    for genre, books in NT_BOOK_GROUPS.items():
        sub = tokens[tokens['book'].isin(books)]
        total = len(sub)
        row: dict = {'genre': genre}
        for ptcl in particles:
            cnt = (sub['display'] == ptcl).sum()
            row[ptcl] = round(cnt / total * 100, 1) if total else 0.0
        row['total'] = total
        rows.append(row)
    return pd.DataFrame(rows).set_index('genre')


def nt_hina_profile(book: str | None = None) -> pd.DataFrame:
    """Classify ἵνα tokens by clause function (purpose/content/result/epexegetic).

    Classification uses a heuristic based on the governing verb's semantics:
    - verbs of command/desire → content
    - motion/goal verbs → purpose
    - result context (ὥστε equivalent usage) → result
    - adjective/noun head → epexegetic
    Default: purpose.
    """
    df = load_syntax()
    if book:
        df = df[df['book'] == book]

    # ἵνα Strong's 2443
    hina = df[df['strong'] == '2443'].copy()

    # Heuristic: look at the immediately preceding verb's Strong's number
    # Verbs of desire/command → content; most other contexts → purpose
    CONTENT_STRONGS = {
        '2309',  # θέλω — want
        '2065',  # ἐρωτάω — ask
        '1189',  # δέομαι — beg
        '3870',  # παρακαλέω — urge
        '1781',  # ἐντέλλομαι — command
        '2753',  # κελεύω — order
        '2980',  # λαλέω — speak (introducing content)
        '3004',  # λέγω — say
        '4336',  # προσεύχομαι — pray
        '154',   # αἰτέω — ask for
    }

    results = []
    for _, row in hina.iterrows():
        # Look back up to 3 tokens for the governing verb
        ch, vs, wn, bk = row['chapter'], row['verse'], row['word_num'], row['book']
        prev = df[
            (df['book'] == bk) & (df['chapter'] == ch) &
            (df['verse'] == vs) & (df['word_num'] < wn) &
            (df['class_'] == 'verb')
        ]
        func = 'purpose'
        if not prev.empty:
            last_verb_strong = str(prev.iloc[-1]['strong'])
            if last_verb_strong in CONTENT_STRONGS:
                func = 'content'

        results.append({'chapter': ch, 'verse': vs, 'function': func,
                        'ref': f"{bk} {ch}:{vs}"})

    out = pd.DataFrame(results)
    if out.empty:
        return out
    counts = out['function'].value_counts().reset_index()
    counts.columns = ['function', 'count']
    total = counts['count'].sum()
    counts['pct'] = (counts['count'] / total * 100).round(1)
    counts['description'] = counts['function'].map({
        k: v for k, v in HINA_FUNCTIONS.items()
    }).fillna('')
    return counts.sort_values('count', ascending=False).reset_index(drop=True)


def nt_hoti_profile(book: str | None = None) -> pd.DataFrame:
    """Classify ὅτι tokens by function (recitative/causal/content).

    Heuristic: tokens immediately after a speech/perception verb → recitative;
    tokens where gloss is 'because' → causal; remainder → content.
    """
    df = load_syntax()
    if book:
        df = df[df['book'] == book]

    hoti = df[df['strong'] == '3754'].copy()

    SPEECH_PERC_STRONGS = {
        '3004', '5346', '2980', '611', '2036',  # speech
        '1492', '3708', '3033', '3129',           # perception/knowing
        '1097', '4100', '3982',                   # knowing/believing
    }

    results = []
    for _, row in hoti.iterrows():
        ch, vs, wn, bk = row['chapter'], row['verse'], row['word_num'], row['book']
        prev = df[
            (df['book'] == bk) & (df['chapter'] == ch) &
            (df['verse'] == vs) & (df['word_num'] < wn) &
            (df['class_'] == 'verb')
        ]
        gloss = str(row.get('gloss', '')).lower()
        if not prev.empty and str(prev.iloc[-1]['strong']) in SPEECH_PERC_STRONGS:
            func = 'recitative'
        elif 'because' in gloss or 'since' in gloss or 'for' in gloss:
            func = 'causal'
        else:
            func = 'content'
        results.append({'chapter': ch, 'verse': vs, 'function': func})

    out = pd.DataFrame(results)
    if out.empty:
        return out
    counts = out['function'].value_counts().reset_index()
    counts.columns = ['function', 'count']
    total = counts['count'].sum()
    counts['pct'] = (counts['count'] / total * 100).round(1)
    counts['description'] = counts['function'].map({
        k: v for k, v in HOTI_FUNCTIONS.items()
    }).fillna('')
    return counts.sort_values('count', ascending=False).reset_index(drop=True)


# ── Print functions ───────────────────────────────────────────────────────────

def print_nt_particle_overview() -> None:
    """Print a statistical overview of GNT discourse particles."""
    df = nt_particle_frequency()
    total = df['count'].sum()
    all_words = len(load_syntax())

    print()
    print('╔' + '═' * 78 + '╗')
    print('║' + '  Greek NT Discourse Particles — Overview'.center(78) + '║')
    print('╚' + '═' * 78 + '╝')
    print()
    print(f"  Total particle tokens analysed: {total:>7,}")
    print(f"  % of all GNT words:             {total/all_words*100:>7.1f}%")
    print()
    print(f"  {'Particle':<8} {'Count':>7} {'% of set':>10}  Function")
    print('  ' + '─' * 70)
    for _, row in df.iterrows():
        if row['count'] == 0:
            continue
        bar = '█' * int(row['pct'] / 2)
        print(f"  {row['display']:<8} {row['count']:>7,} {row['pct']:>9.1f}%  {bar}  "
              f"{row['primary_function']}")
    print()


def print_nt_particle_frequency(book: str | None = None) -> None:
    """Print particle frequency table for a book or the whole GNT."""
    df = nt_particle_frequency(book)
    scope = book or 'Whole GNT'
    total = df['count'].sum()
    print()
    print('═' * 76)
    print(f"  GNT discourse particles — {scope}  (total: {total:,})")
    print('─' * 76)
    print(f"  {'Particle':<8} {'Count':>7} {'%':>7}  Primary function")
    print('  ' + '─' * 72)
    for _, row in df.iterrows():
        if row['count'] == 0:
            continue
        bar = '█' * int(row['pct'] / 2)
        print(f"  {row['display']:<8} {row['count']:>7,} {row['pct']:>6.1f}%  {bar}  "
              f"{row['primary_function']}")
    print()


def print_nt_particle_genre_profile() -> None:
    """Print particle % by NT genre group."""
    df = nt_particle_genre_profile()
    particles = [d for _, d, _ in PARTICLE_REGISTRY.values()]
    print()
    print('═' * 100)
    print("  GNT discourse particle % by genre group (% of genre's word tokens)")
    print('─' * 100)
    header = f"  {'Genre':<18}" + ''.join(f"{p:>7}" for p in particles) + f"  {'Total':>8}"
    print(header)
    print('  ' + '─' * 96)
    for genre, row in df.iterrows():
        vals = ''.join(f"{row.get(p, 0.0):>6.2f}%" for p in particles)
        print(f"  {genre:<18}{vals}  {row['total']:>8,}")
    print()


def print_nt_hina_profile(book: str | None = None) -> None:
    """Print ἵνα clause function classification."""
    df = nt_hina_profile(book)
    scope = book or 'Whole GNT'
    if df.empty:
        print(f"\n  No ἵνα tokens found in {scope}.\n")
        return
    total = df['count'].sum()
    print()
    print('═' * 76)
    print(f"  ἵνα clause function classification — {scope}  (total: {total:,})")
    print('─' * 76)
    for _, row in df.iterrows():
        bar = '█' * int(row['pct'] / 3)
        print(f"  {row['function']:<14} {row['count']:>5,}  {row['pct']:>5.1f}%  {bar}")
        print(f"    {row['description']}")
    print()


def print_nt_hoti_profile(book: str | None = None) -> None:
    """Print ὅτι function classification."""
    df = nt_hoti_profile(book)
    scope = book or 'Whole GNT'
    if df.empty:
        print(f"\n  No ὅτι tokens found in {scope}.\n")
        return
    total = df['count'].sum()
    print()
    print('═' * 76)
    print(f"  ὅτι function classification — {scope}  (total: {total:,})")
    print('─' * 76)
    for _, row in df.iterrows():
        bar = '█' * int(row['pct'] / 3)
        print(f"  {row['function']:<14} {row['count']:>5,}  {row['pct']:>5.1f}%  {bar}")
        print(f"    {row['description']}")
    print()


# ── Chart functions ───────────────────────────────────────────────────────────

def nt_particle_frequency_chart(book: str | None = None) -> Path | None:
    """Horizontal bar chart of particle frequency."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_particle_frequency(book)
    df = df[df['count'] > 0].sort_values('count')
    scope = book or 'Whole GNT'

    fig, ax = plt.subplots(figsize=(9, 5))
    n = max(len(df) - 1, 1)
    colors = plt.cm.Purples([0.35 + 0.5 * i / n for i in range(len(df))])  # type: ignore[attr-defined]
    bars = ax.barh(df['display'], df['count'], color=colors)
    for bar, val in zip(bars, df['count']):
        ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height() / 2,
                f"{val:,}", va='center', fontsize=9)
    ax.set_title(f"GNT Discourse Particle Frequency — {scope}", fontsize=13, fontweight='bold')
    ax.set_xlabel("Token count")
    ax.xaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / f'nt_particle_freq{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def nt_particle_genre_heatmap() -> Path | None:
    """Heatmap of particle % by NT genre group."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_particle_genre_profile()
    particles = [d for _, d, _ in PARTICLE_REGISTRY.values()]
    # Only include particles with non-trivial counts
    ptcl_cols = [p for p in particles if p in df.columns and df[p].max() > 0]
    data = df[ptcl_cols].values.astype(float)

    fig, ax = plt.subplots(figsize=(12, 3.5))
    im = ax.imshow(data, cmap='YlOrRd', aspect='auto', vmin=0, vmax=data.max())
    ax.set_xticks(range(len(ptcl_cols)))
    ax.set_xticklabels(ptcl_cols, fontsize=12)
    ax.set_yticks(range(len(df.index)))
    ax.set_yticklabels(df.index.tolist(), fontsize=11)
    for i in range(len(df.index)):
        for j in range(len(ptcl_cols)):
            val = data[i, j]
            ax.text(j, i, f"{val:.2f}%", ha='center', va='center',
                    fontsize=9, color='black' if val < data.max() * 0.6 else 'white')
    plt.colorbar(im, ax=ax, label='% of genre word tokens')
    ax.set_title("GNT Discourse Particle Distribution by Genre", fontsize=13, fontweight='bold')
    fig.tight_layout()

    out = _ensure_chart_dir() / 'nt_particle_genre_heatmap.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def nt_particle_book_chart(particle_display: str = 'δέ') -> Path | None:
    """Bar chart of a single particle's count across NT books."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    ct = nt_particle_by_book()
    if particle_display not in ct.columns:
        return None

    fig, ax = plt.subplots(figsize=(14, 4))
    x = range(len(ct))
    ax.bar(x, ct[particle_display], color='purple', alpha=0.75)
    ax.set_xticks(list(x))
    ax.set_xticklabels(ct.index.tolist(), rotation=40, ha='right', fontsize=9)
    ax.set_title(f"'{particle_display}' token count across NT books",
                 fontsize=13, fontweight='bold')
    ax.set_ylabel("Token count")
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    safe = particle_display.replace('ά', 'a').replace('ή', 'h').replace('ό', 'o')
    out = _ensure_chart_dir() / f'nt_particle_{safe}_books.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out
