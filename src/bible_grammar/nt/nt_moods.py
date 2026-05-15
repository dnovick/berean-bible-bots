"""
Greek NT mood usage analysis — subjunctive, infinitive, and imperative.

Provides distribution, construction type classification, and genre comparison
for the three non-indicative finite/non-finite moods taught in BBG ch31–33.

Public API
──────────
nt_mood_data(mood, book=None)               → DataFrame (tokens for one mood)
nt_mood_profile(book=None)                  → DataFrame (all mood distribution)
nt_subjunctive_profile(book=None)           → DataFrame (subj tense/voice)
nt_infinitive_profile(book=None)            → DataFrame (inf tense/voice)
nt_imperative_profile(book=None)            → DataFrame (imp tense/voice/person)
nt_subjunctive_constructions(book=None)     → DataFrame (purpose/conditional/hortatory)
nt_infinitive_constructions(book=None)      → DataFrame (complementary/articular/etc.)
nt_imperative_tense_comparison(book=None)   → DataFrame (present vs aorist imperatives)
nt_mood_genre_profile()                     → DataFrame (mood % by genre)
nt_mood_book_distribution(mood)             → DataFrame (count per NT book)

print_nt_mood_overview()                    → None
print_nt_subjunctive_profile(book=None)     → None
print_nt_infinitive_profile(book=None)      → None
print_nt_imperative_profile(book=None)      → None
print_nt_subjunctive_constructions(book=None) → None
print_nt_infinitive_constructions(book=None)→ None
print_nt_imperative_tense_comparison(book=None) → None
print_nt_mood_genre_profile()               → None

nt_mood_chart(book=None)                    → Path | None
nt_subjunctive_chart(book=None)             → Path | None
nt_imperative_chart(book=None)              → Path | None
nt_mood_genre_heatmap()                     → Path | None
"""

from __future__ import annotations
from pathlib import Path

import pandas as pd

from ..core.syntax import load_syntax
from .nt_verb_profile import NT_BOOK_GROUPS, NT_BOOK_ORDER, TENSE_ORDER, VOICE_ORDER

MOOD_ORDER = ['indicative', 'subjunctive', 'optative', 'imperative', 'infinitive', 'participle']

# ἵνα (2443) and ὅπως (3704) introduce purpose clauses
PURPOSE_PARTICLES = {'2443', '3704'}
# ἐάν (1437) introduces conditional subjunctive
COND_PARTICLES = {'1437', '0323'}
# μή + subjunctive = prohibitive; ἄν (0302) + subjunctive = indefinite
PROHIB_STRONGS = {'3361'}

_CHART_DIR = Path('output') / 'charts' / 'nt' / 'moods'


def _ensure_chart_dir() -> Path:
    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    return _CHART_DIR


# ── Data loading ──────────────────────────────────────────────────────────────

def nt_mood_data(mood: str, book: str | None = None) -> pd.DataFrame:
    """All tokens for a specific mood ('subjunctive', 'infinitive', 'imperative', etc.)."""
    df = load_syntax()
    mask = df['mood'].str.lower() == mood.lower()
    result = df[mask].copy()
    if book:
        result = result[result['book'] == book]
    return result


# ── Profile functions ─────────────────────────────────────────────────────────

def _count_profile(series: pd.Series, order: list[str]) -> pd.DataFrame:
    vc = series.str.lower().value_counts()
    total = vc.sum()
    records = []
    for form in order:
        cnt = int(vc.get(form, 0))
        if cnt > 0:
            records.append({'form': form, 'count': cnt,
                            'pct': round(cnt / total * 100, 1) if total else 0.0})
    for form, cnt in vc.items():
        if str(form).lower() not in order and int(cnt) > 0:
            records.append({'form': str(form), 'count': int(cnt),
                            'pct': round(int(cnt) / total * 100, 1) if total else 0.0})
    return pd.DataFrame(records)


def nt_mood_profile(book: str | None = None) -> pd.DataFrame:
    """All verb mood distribution. Returns DataFrame: form, count, pct."""
    df = load_syntax()
    if book:
        df = df[df['book'] == book]
    verbs = df[df['class_'] == 'verb']
    return _count_profile(verbs['mood'].dropna(), MOOD_ORDER)


def nt_subjunctive_profile(book: str | None = None) -> pd.DataFrame:
    """Subjunctive tense × voice distribution."""
    subj = nt_mood_data('subjunctive', book)
    sub = subj[subj['tense'].notna() & subj['voice'].notna()].copy()
    sub['tense'] = sub['tense'].str.lower()
    sub['voice'] = sub['voice'].str.lower()
    ct = pd.crosstab(sub['tense'], sub['voice'])
    ct = ct.reindex(
        index=[t for t in TENSE_ORDER if t in ct.index],
        columns=[v for v in VOICE_ORDER if v in ct.columns],
        fill_value=0,
    )
    return ct


def nt_infinitive_profile(book: str | None = None) -> pd.DataFrame:
    """Infinitive tense × voice distribution."""
    inf = nt_mood_data('infinitive', book)
    sub = inf[inf['tense'].notna() & inf['voice'].notna()].copy()
    sub['tense'] = sub['tense'].str.lower()
    sub['voice'] = sub['voice'].str.lower()
    ct = pd.crosstab(sub['tense'], sub['voice'])
    ct = ct.reindex(
        index=[t for t in TENSE_ORDER if t in ct.index],
        columns=[v for v in VOICE_ORDER if v in ct.columns],
        fill_value=0,
    )
    return ct


def nt_imperative_profile(book: str | None = None) -> pd.DataFrame:
    """Imperative tense × person distribution."""
    imp = nt_mood_data('imperative', book)
    sub = imp[imp['tense'].notna() & imp['person'].notna()].copy()
    sub['tense'] = sub['tense'].str.lower()
    sub['person'] = sub['person'].str.lower()
    ct = pd.crosstab(sub['tense'], sub['person'])
    col_order = [c for c in ['second', 'third'] if c in ct.columns]
    ct = ct.reindex(
        index=[t for t in TENSE_ORDER if t in ct.index],
        columns=col_order,
        fill_value=0,
    )
    return ct


def nt_subjunctive_constructions(book: str | None = None) -> pd.DataFrame:
    """Classify subjunctive tokens by construction type.

    Looks at the immediately preceding particle to classify:
    - ἵνα / ὅπως → purpose / content
    - ἐάν → conditional (3rd class condition)
    - μή → prohibitive (aorist subj. = negated command) or negative
    - ἄν → indefinite / general
    - no governing particle → hortatory (1st person) or other
    """
    df = load_syntax()
    if book:
        df = df[df['book'] == book]
    subj = df[df['mood'].str.lower() == 'subjunctive'].copy()

    results = []
    for _, row in subj.iterrows():
        ch, _, wn, bk = row['chapter'], row['verse'], row['word_num'], row['book']
        tense = str(row.get('tense', '')).lower()
        person = str(row.get('person', '')).lower()

        # Look back up to 3 tokens for a governing particle
        prev = df[
            (df['book'] == bk) & (df['chapter'] == ch) &
            (df['word_num'] >= max(1, wn - 4)) & (df['word_num'] < wn)
        ].sort_values('word_num')

        construction = 'other'
        for _, p in prev.iterrows():
            s = str(p['strong'])
            if s in PURPOSE_PARTICLES:
                construction = 'purpose / content (ἵνα/ὅπως)'
                break
            if s in COND_PARTICLES:
                construction = 'conditional (ἐάν)'
                break
            if s in PROHIB_STRONGS:
                construction = 'prohibitive (μή + subj.)'
                break

        if construction == 'other':
            if person == 'first':
                construction = 'hortatory (let us...)'
            else:
                construction = 'other / deliberative'

        results.append({'construction': construction, 'tense': tense, 'person': person})

    out = pd.DataFrame(results)
    if out.empty:
        return out
    counts = out['construction'].value_counts().reset_index()
    counts.columns = ['construction', 'count']
    total = counts['count'].sum()
    counts['pct'] = (counts['count'] / total * 100).round(1)
    return counts.sort_values('count', ascending=False).reset_index(drop=True)


def nt_infinitive_constructions(book: str | None = None) -> pd.DataFrame:
    """Classify infinitive tokens by construction type.

    Uses syntactic role ('role' column) and preceding article/particle:
    - role='o' or complementary context → complementary infinitive
    - preceded by article (G3588) → articular infinitive
    - preceded by preposition → prepositional infinitive phrase
    - role='s' → subject infinitive
    """
    df = load_syntax()
    if book:
        df = df[df['book'] == book]
    inf = df[df['mood'].str.lower() == 'infinitive'].copy()

    ARTICLE_STRONG = '3588'
    PREP_CLASS = 'prep'

    results = []
    for _, row in inf.iterrows():
        ch, _, wn, bk = row['chapter'], row['verse'], row['word_num'], row['book']
        role = str(row.get('role', '')).lower()

        prev = df[
            (df['book'] == bk) & (df['chapter'] == ch) &
            (df['word_num'] >= max(1, wn - 3)) & (df['word_num'] < wn)
        ].sort_values('word_num')

        construction = 'complementary'
        for _, p in prev.iterrows():
            if str(p.get('strong', '')) == ARTICLE_STRONG:
                construction = 'articular (τό + inf.)'
                break
            if str(p.get('class_', '')) == PREP_CLASS:
                construction = 'prepositional phrase'
                break

        if construction == 'complementary' and role == 's':
            construction = 'subject infinitive'

        results.append({'construction': construction})

    out = pd.DataFrame(results)
    if out.empty:
        return out
    counts = out['construction'].value_counts().reset_index()
    counts.columns = ['construction', 'count']
    total = counts['count'].sum()
    counts['pct'] = (counts['count'] / total * 100).round(1)
    return counts.sort_values('count', ascending=False).reset_index(drop=True)


def nt_imperative_tense_comparison(book: str | None = None) -> pd.DataFrame:
    """Present vs. aorist imperative comparison.

    The tense distinction is meaningful:
    - Present imperative = continue doing / do repeatedly
    - Aorist imperative (2nd person) = start doing / single command
    Returns DataFrame: tense, voice, person, count, pct.
    """
    imp = nt_mood_data('imperative', book)
    imp = imp.copy()
    imp['tense'] = imp['tense'].str.lower()
    imp['voice'] = imp['voice'].str.lower()
    imp['person'] = imp['person'].str.lower()

    grp = imp.groupby(['tense', 'voice', 'person']).size().reset_index(name='count')
    total = grp['count'].sum()
    grp['pct'] = (grp['count'] / total * 100).round(1)
    return grp.sort_values('count', ascending=False).reset_index(drop=True)


def nt_mood_genre_profile() -> pd.DataFrame:
    """Mood % by NT genre group (excluding indicative to show non-finite forms clearly)."""
    df = load_syntax()
    verbs = df[df['class_'] == 'verb'].copy()
    verbs['mood'] = verbs['mood'].str.lower()
    rows = []
    for genre, books in NT_BOOK_GROUPS.items():
        sub = verbs[verbs['book'].isin(books) & verbs['mood'].notna()]
        total = len(sub)
        row: dict = {'genre': genre}
        for m in MOOD_ORDER:
            cnt = (sub['mood'] == m).sum()
            row[m] = round(cnt / total * 100, 1) if total else 0.0
        row['total'] = total
        rows.append(row)
    return pd.DataFrame(rows).set_index('genre')


def nt_mood_book_distribution(mood: str) -> pd.DataFrame:
    """Token count per NT book for a specific mood."""
    tokens = nt_mood_data(mood)
    book_counts = tokens['book'].value_counts().reset_index()
    book_counts.columns = ['book', 'count']
    total = book_counts['count'].sum()
    book_counts['pct'] = (book_counts['count'] / total * 100).round(1)
    order_map = {b: i for i, b in enumerate(NT_BOOK_ORDER)}
    book_counts['_ord'] = book_counts['book'].map(order_map).fillna(99)
    return book_counts.sort_values('_ord').drop(columns='_ord').reset_index(drop=True)


# ── Print functions ───────────────────────────────────────────────────────────

def print_nt_mood_overview() -> None:
    """Print a statistical overview of GNT verb moods."""
    df = load_syntax()
    verbs = df[df['class_'] == 'verb']
    total = len(verbs)

    print()
    print('╔' + '═' * 78 + '╗')
    print('║' + '  Greek NT Verb Moods — Overview'.center(78) + '║')
    print('╚' + '═' * 78 + '╝')
    print()
    print(f"  Total GNT verb tokens: {total:>7,}")
    print()
    df_mood = nt_mood_profile()
    for _, row in df_mood.iterrows():
        if row['count'] == 0:
            continue
        bar = '█' * int(row['pct'] / 2)
        print(f"  {row['form']:<14} {row['count']:>6,}  ({row['pct']:>5.1f}%)  {bar}")
    print()


def _print_crosstab(ct: pd.DataFrame, label: str) -> None:
    total = ct.values.sum()
    print()
    print('═' * 72)
    print(f"  {label}  (total: {total:,})")
    print('─' * 72)
    header = f"  {'Tense':<14}" + ''.join(f"{c:>12}" for c in ct.columns) + f"  {'Row total':>10}"
    print(header)
    print('  ' + '─' * 68)
    for tense, row in ct.iterrows():
        rtotal = row.sum()
        vals = ''.join(f"{v:>12,}" for v in row)
        print(f"  {tense:<14}{vals}  {rtotal:>10,}")
    print()


def print_nt_subjunctive_profile(book: str | None = None) -> None:
    scope = book or 'Whole GNT'
    ct = nt_subjunctive_profile(book)
    _print_crosstab(ct, f"Subjunctive tense × voice — {scope}")


def print_nt_infinitive_profile(book: str | None = None) -> None:
    scope = book or 'Whole GNT'
    ct = nt_infinitive_profile(book)
    _print_crosstab(ct, f"Infinitive tense × voice — {scope}")


def print_nt_imperative_profile(book: str | None = None) -> None:
    scope = book or 'Whole GNT'
    ct = nt_imperative_profile(book)
    _print_crosstab(ct, f"Imperative tense × person — {scope}")


def print_nt_subjunctive_constructions(book: str | None = None) -> None:
    df = nt_subjunctive_constructions(book)
    scope = book or 'Whole GNT'
    total = df['count'].sum() if not df.empty else 0
    print()
    print('═' * 76)
    print(f"  Subjunctive construction types — {scope}  (total: {total:,})")
    print('─' * 76)
    for _, row in df.iterrows():
        bar = '█' * int(row['pct'] / 3)
        print(f"  {row['construction']:<40} {row['count']:>5,}  {row['pct']:>5.1f}%  {bar}")
    print()


def print_nt_infinitive_constructions(book: str | None = None) -> None:
    df = nt_infinitive_constructions(book)
    scope = book or 'Whole GNT'
    total = df['count'].sum() if not df.empty else 0
    print()
    print('═' * 72)
    print(f"  Infinitive construction types — {scope}  (total: {total:,})")
    print('─' * 72)
    for _, row in df.iterrows():
        bar = '█' * int(row['pct'] / 3)
        print(f"  {row['construction']:<36} {row['count']:>5,}  {row['pct']:>5.1f}%  {bar}")
    print()


def print_nt_imperative_tense_comparison(book: str | None = None) -> None:
    df = nt_imperative_tense_comparison(book)
    scope = book or 'Whole GNT'
    print()
    print('═' * 72)
    print(f"  Imperative tense breakdown — {scope}")
    print('  (present = ongoing/continuous; aorist = punctiliar command)')
    print('─' * 72)
    for _, row in df.iterrows():
        bar = '█' * int(row['pct'] / 2)
        print(f"  {row['tense']:<10} {row['voice']:<10} {row['person']:<8} "
              f"{row['count']:>5,}  {row['pct']:>5.1f}%  {bar}")
    print()


def print_nt_mood_genre_profile() -> None:
    df = nt_mood_genre_profile()
    print()
    print('═' * 90)
    print("  GNT verb mood % by genre group")
    print('─' * 90)
    moods = [m for m in MOOD_ORDER if m in df.columns]
    header = f"  {'Genre':<20}" + ''.join(f"{m:>12}" for m in moods) + f"  {'Total':>8}"
    print(header)
    print('  ' + '─' * 86)
    for genre, row in df.iterrows():
        vals = ''.join(f"{row.get(m, 0.0):>11.1f}%" for m in moods)
        print(f"  {genre:<20}{vals}  {row['total']:>8,}")
    print()


# ── Chart functions ───────────────────────────────────────────────────────────

def nt_mood_chart(book: str | None = None) -> Path | None:
    """Horizontal bar chart of mood distribution."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_mood_profile(book)
    df = df[df['count'] > 0].sort_values('pct')
    scope = book or 'Whole GNT'

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = plt.cm.Blues([0.3 + 0.5 * i / max(len(df) - 1, 1) for i in range(len(df))])  # type: ignore[attr-defined]
    bars = ax.barh(df['form'], df['pct'], color=colors)
    for bar, val in zip(bars, df['pct']):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va='center', fontsize=9)
    ax.set_title(f"GNT Verb Mood Distribution — {scope}", fontsize=13, fontweight='bold')
    ax.set_xlabel("% of verb tokens")
    ax.set_xlim(0, df['pct'].max() * 1.2)
    ax.xaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / f'nt_mood{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def nt_subjunctive_chart(book: str | None = None) -> Path | None:
    """Stacked bar chart of subjunctive constructions."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_subjunctive_constructions(book)
    if df.empty:
        return None
    scope = book or 'Whole GNT'

    fig, ax = plt.subplots(figsize=(9, 5))
    df_sorted = df.sort_values('count', ascending=True)
    colors = plt.cm.Purples([0.3 + 0.6 * i / max(len(df_sorted) - 1, 1)  # type: ignore[attr-defined]
                             for i in range(len(df_sorted))])
    bars = ax.barh(df_sorted['construction'], df_sorted['count'], color=colors)
    for bar, val in zip(bars, df_sorted['count']):
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height() / 2,
                f"{val:,}", va='center', fontsize=8)
    ax.set_title(f"Subjunctive Construction Types — {scope}", fontsize=13, fontweight='bold')
    ax.set_xlabel("Token count")
    ax.xaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / f'nt_subjunctive{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def nt_imperative_chart(book: str | None = None) -> Path | None:
    """Bar chart comparing present vs. aorist imperatives."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_imperative_tense_comparison(book)
    if df.empty:
        return None

    tense_totals = df.groupby('tense')['count'].sum().reset_index()
    scope = book or 'Whole GNT'

    fig, ax = plt.subplots(figsize=(7, 4))
    colors = {'present': '#1565C0', 'aorist': '#E65100', 'perfect': '#2E7D32'}
    for i, (_, row) in enumerate(tense_totals.iterrows()):
        ax.bar(row['tense'], row['count'],
               color=colors.get(row['tense'], '#888888'), alpha=0.85)
        ax.text(i, row['count'] + 5, f"{row['count']:,}", ha='center', fontsize=10)
    ax.set_title(f"Imperative Tense Distribution — {scope}", fontsize=13, fontweight='bold')
    ax.set_ylabel("Token count")
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    out = _ensure_chart_dir() / f'nt_imperative{"_"+book if book else ""}.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out


def nt_mood_genre_heatmap() -> Path | None:
    """Heatmap of mood % by NT genre group."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = nt_mood_genre_profile()
    moods = [m for m in MOOD_ORDER if m in df.columns]
    data = df[moods].values.astype(float)

    fig, ax = plt.subplots(figsize=(12, 3.5))
    im = ax.imshow(data, cmap='YlOrRd', aspect='auto', vmin=0, vmax=data.max())
    ax.set_xticks(range(len(moods)))
    ax.set_xticklabels(moods, fontsize=11)
    ax.set_yticks(range(len(df.index)))
    ax.set_yticklabels(df.index.tolist(), fontsize=11)
    for i in range(len(df.index)):
        for j in range(len(moods)):
            val = data[i, j]
            ax.text(j, i, f"{val:.1f}%", ha='center', va='center',
                    fontsize=10, color='black' if val < 25 else 'white')
    plt.colorbar(im, ax=ax, label='% of genre verb tokens')
    ax.set_title("GNT Verb Mood Distribution by Genre", fontsize=13, fontweight='bold')
    fig.tight_layout()

    out = _ensure_chart_dir() / 'nt_mood_genre_heatmap.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return out
