"""Verb form profile, wayyiqtol chains, stem distribution, and aspect comparison."""
from __future__ import annotations
from pathlib import Path

import pandas as pd

from ._common import (
    VERB_FORM_ORDER, VERB_FORM_LABELS,
    _load_macula, _filter_book,
)

# Canonical stem order for display
_STEM_ORDER: list[str] = [
    'qal', 'niphal', 'piel', 'pual', 'hiphil', 'hophal', 'hithpael',
    'polel', 'hithpolel', 'pilpel', 'poel', 'hithpeel', 'peal',
    'pael', 'aphel', 'haphel', 'shaph',
]

# Pre-defined genre groupings for aspect_comparison convenience
GENRE_SETS: dict[str, list[str]] = {
    'narrative': ['Gen', 'Exod', 'Num', 'Josh', 'Judg', 'Rut', '1Sam', '2Sam',
                  '1Kgs', '2Kgs', '1Chr', '2Chr', 'Ezra', 'Neh', 'Esth', 'Jonah'],
    'law':       ['Lev', 'Deu'],
    'prophecy':  ['Isa', 'Jer', 'Eze', 'Hos', 'Joel', 'Amos', 'Mic', 'Zeph',
                  'Zech', 'Mal'],
    'poetry':    ['Psa', 'Pro', 'Job', 'Sng', 'Lam'],
    'wisdom':    ['Pro', 'Job', 'Ecc'],
}


# ─────────────────────────────────────────────────────────────────────────────
# Verb form profile
# ─────────────────────────────────────────────────────────────────────────────

def verb_form_profile(
    book: str,
    chapter: int | None = None,
) -> pd.DataFrame:
    """
    Count occurrences of each Hebrew verb conjugation type in a book or chapter.

    Returns a DataFrame with columns: form, count, pct.
    Rows are ordered by VERB_FORM_ORDER (wayyiqtol → inf.abs).
    """
    df = _load_macula()
    scope = _filter_book(df, book, chapter)
    verbs = scope[scope['class_'] == 'verb']

    counts: dict[str, int] = {f: 0 for f in VERB_FORM_ORDER}
    for t in verbs['type_']:
        t_str = str(t).strip()
        if t_str in counts:
            counts[t_str] += 1

    total = sum(counts.values())
    records = []
    for form in VERB_FORM_ORDER:
        n = counts[form]
        pct = round(n / total * 100, 1) if total else 0.0
        records.append({'form': form, 'count': n, 'pct': pct})

    return pd.DataFrame(records)


def print_verb_form_profile(book: str, chapter: int | None = None) -> None:
    """Print a formatted verb form profile for a book or chapter."""
    df = verb_form_profile(book, chapter)
    total = df['count'].sum()
    scope = f"{book} ch.{chapter}" if chapter else book

    print()
    print('═' * 72)
    print(f"  Verb form profile: {scope}  (total verb tokens: {total})")
    print('─' * 72)
    for _, row in df.iterrows():
        bar = '█' * int(row['pct'] / 2)
        print(f"  {row['form']:<22} {row['count']:>5}  {row['pct']:>5.1f}%  {bar}")
    print()


def verb_form_chart(
    book: str,
    chapter: int | None = None,
    *,
    output_path: str | None = None,
) -> Path | None:
    """Bar chart of verb form distribution. Returns Path or None."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed — cannot generate chart")
        return None

    df = verb_form_profile(book, chapter)
    df = df[df['count'] > 0]
    scope = f"{book} ch.{chapter}" if chapter else book

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = [plt.cm.get_cmap('tab20')(i / 20) for i in range(len(df))]
    ax.bar([VERB_FORM_LABELS.get(f, f) for f in df['form']], df['count'],
           color=colors, edgecolor='white', linewidth=0.5)
    ax.set_title(f"Hebrew Verb Form Distribution — {scope}", fontsize=13)
    ax.set_ylabel("Token count")
    ax.set_xlabel("Conjugation type")
    plt.xticks(rotation=30, ha='right', fontsize=9)
    plt.tight_layout()

    if output_path is None:
        slug = f"{book.lower()}-ch{chapter}" if chapter else book.lower()
        out = Path('output') / 'charts' / 'ot' / 'verbs'
        out.mkdir(parents=True, exist_ok=True)
        output_path = str(out / f'verb-forms-{slug}.png')

    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"  Saved chart: {output_path}")
    return Path(output_path)


# ─────────────────────────────────────────────────────────────────────────────
# Wayyiqtol chains
# ─────────────────────────────────────────────────────────────────────────────

def wayyiqtol_chains(book: str, chapter: int) -> list[dict]:
    """
    Identify wayyiqtol chains in a chapter.

    Returns a list of chain dicts, each with:
      start_verse, end_verse, length, verbs (list), break_type, break_form.
    """
    df = _load_macula()
    chap = _filter_book(df, book, chapter)
    verb_rows = chap[chap['role'] == 'v'].reset_index(drop=True)

    chains: list[dict] = []
    current: list[dict] = []

    for _, row in verb_rows.iterrows():
        form = str(row.get('type_', '')).strip()
        if form == 'wayyiqtol':
            current.append({
                'verse': int(row['verse']),
                'text':  str(row.get('text', '')),
                'lemma': str(row.get('lemma', '')),
                'stem':  str(row.get('stem', '')),
                'gloss': str(row.get('gloss', '')),
            })
        else:
            if len(current) >= 2:
                chains.append(_make_chain(current, form))
            current = []

    if len(current) >= 2:
        chains.append(_make_chain(current, 'end-of-chapter'))

    return chains


def _make_chain(verbs: list[dict], break_form: str) -> dict:
    if break_form == 'end-of-chapter':
        break_type = 'end of chapter'
    elif break_form in ('qatal', 'weqatal'):
        break_type = 'perfect / weqatal (summary or result)'
    elif break_form in ('yiqtol', 'jussive', 'cohortative'):
        break_type = 'modal/jussive (speech or wish)'
    elif 'participle' in break_form:
        break_type = 'participle (circumstantial/descriptive)'
    elif break_form == 'infinitive construct':
        break_type = 'infinitive construct (purpose clause)'
    elif break_form == 'infinitive absolute':
        break_type = 'infinitive absolute (intensification)'
    elif break_form == 'imperative':
        break_type = 'imperative (command)'
    else:
        break_type = f'other ({break_form})'

    return {
        'start_verse': verbs[0]['verse'],
        'end_verse':   verbs[-1]['verse'],
        'length':      len(verbs),
        'verbs':       verbs,
        'break_type':  break_type,
        'break_form':  break_form,
    }


def print_wayyiqtol_chains(book: str, chapter: int) -> None:
    """Print a formatted wayyiqtol chain analysis for a chapter."""
    chains = wayyiqtol_chains(book, chapter)
    total_wayy = sum(c['length'] for c in chains)

    print()
    print('═' * 72)
    print(f"  Wayyiqtol chains: {book} ch.{chapter}  "
          f"({len(chains)} chains, {total_wayy} wayyiqtol verbs total)")
    print('─' * 72)

    if not chains:
        print("  No wayyiqtol chains of length ≥ 2 found.")
        print()
        return

    for i, ch in enumerate(chains, 1):
        vref = (f"v{ch['start_verse']}" if ch['start_verse'] == ch['end_verse']
                else f"vv{ch['start_verse']}–{ch['end_verse']}")
        print(f"\n  Chain {i}  [{vref}]  length={ch['length']}  "
              f"→ breaks: {ch['break_type']}")
        for v in ch['verbs']:
            gloss = v['gloss'][:20] if v['gloss'] else ''
            print(f"    v{v['verse']}  {v['text']:<20}  {v['lemma']:<12}  "
                  f"{v['stem']:<12}  {gloss}")

    print()
    lengths = [c['length'] for c in chains]
    print(f"  Longest chain: {max(lengths)} verbs  |  "
          f"Mean length: {sum(lengths)/len(lengths):.1f}")
    break_counts: dict[str, int] = {}
    for c in chains:
        k = c['break_form']
        break_counts[k] = break_counts.get(k, 0) + 1
    print("  Chain-break forms:")
    for form, cnt in sorted(break_counts.items(), key=lambda x: -x[1]):
        print(f"    {form:<28} × {cnt}")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Stem distribution
# ─────────────────────────────────────────────────────────────────────────────

def stem_distribution(book: str) -> pd.DataFrame:
    """Count verb tokens by stem (binyan) for a book. Returns DataFrame: stem, count, pct."""
    df = _load_macula()
    book_df = _filter_book(df, book)
    verbs = book_df[book_df['class_'] == 'verb']

    counts = verbs['stem'].value_counts().reset_index()
    counts.columns = ['stem', 'count']
    total = counts['count'].sum()
    counts['pct'] = (counts['count'] / total * 100).round(1)
    return counts.sort_values('count', ascending=False).reset_index(drop=True)


def print_stem_distribution(book: str) -> None:
    """Print a formatted stem distribution for a book."""
    df = stem_distribution(book)
    total = df['count'].sum()

    print()
    print('═' * 72)
    print(f"  Verb stem distribution: {book}  (total: {total})")
    print('─' * 72)
    for _, row in df.iterrows():
        bar = '█' * int(row['pct'] / 2)
        print(f"  {str(row['stem']):<20} {row['count']:>5}  {row['pct']:>5.1f}%  {bar}")
    print()


def stem_chart(book: str, *, output_path: str | None = None) -> Path | None:
    """Horizontal bar chart of verb stem distribution. Returns Path or None."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed — cannot generate chart")
        return None

    df = stem_distribution(book)
    df = df[df['count'] >= 2]

    fig, ax = plt.subplots(figsize=(8, max(4, len(df) * 0.4)))
    colors = [plt.cm.get_cmap('tab20')(i / 20) for i in range(len(df))]
    ax.barh(df['stem'][::-1], df['count'][::-1],
            color=colors[::-1], edgecolor='white', linewidth=0.5)
    ax.set_title(f"Verb Stem Distribution — {book}", fontsize=12)
    ax.set_xlabel("Token count")
    plt.tight_layout()

    if output_path is None:
        out = Path('output') / 'charts' / 'ot' / 'verbs'
        out.mkdir(parents=True, exist_ok=True)
        output_path = str(out / f'stems-{book.lower()}.png')

    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"  Saved chart: {output_path}")
    return Path(output_path)


# ─────────────────────────────────────────────────────────────────────────────
# Aspect comparison across genres
# ─────────────────────────────────────────────────────────────────────────────

def aspect_comparison(
    books: list[str],
    chapter: int | None = None,
) -> pd.DataFrame:
    """
    Build a side-by-side verb form profile for multiple books.

    Returns a DataFrame indexed by verb form with one column per book (count, pct).
    """
    frames: dict[str, pd.DataFrame] = {}
    for book in books:
        df = verb_form_profile(book, chapter)
        frames[book] = df.set_index('form')

    combined = pd.concat(frames, axis=1)
    combined = combined.reindex(VERB_FORM_ORDER)
    combined = combined.fillna(0)
    return combined


def print_aspect_comparison(
    books: list[str],
    chapter: int | None = None,
    *,
    show_counts: bool = False,
) -> None:
    """Print a side-by-side verb form percentage comparison for multiple books."""
    df = aspect_comparison(books, chapter)
    scope = f" ch.{chapter}" if chapter else ''

    header_books = '  '.join(f"{b:>8}" for b in books)
    print()
    print('═' * (28 + 11 * len(books)))
    print(f"  Aspect / verb-form comparison{scope}: {' · '.join(books)}")
    print('─' * (28 + 11 * len(books)))
    print(f"  {'Form':<22}  {header_books}")
    print('  ' + '─' * (24 + 11 * len(books)))

    for form in VERB_FORM_ORDER:
        pcts = [df.loc[form, (b, 'pct')] if (b, 'pct') in df.columns else 0.0
                for b in books]
        if max(pcts) < 0.5:
            continue
        label = VERB_FORM_LABELS.get(form, form)
        cols = '  '.join(f"{p:>6.1f}%" for p in pcts)
        dom_idx = pcts.index(max(pcts))
        bar = '█' * int(max(pcts) / 3)
        print(f"  {label:<22}  {cols}   {bar} ← {books[dom_idx]}")

    print('  ' + '─' * (24 + 11 * len(books)))
    totals = []
    for book in books:
        if (book, 'count') in df.columns:
            totals.append(int(df[(book, 'count')].sum()))
        else:
            totals.append(0)
    total_str = '  '.join(f"{t:>8,}" for t in totals)
    print(f"  {'Total verbs':<22}  {total_str}")
    print()


def aspect_comparison_chart(
    books: list[str],
    chapter: int | None = None,
    *,
    output_path: str | None = None,
) -> Path | None:
    """Save a grouped bar chart comparing verb form percentages across books."""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        return None

    df = aspect_comparison(books, chapter)
    active_forms = [
        f for f in VERB_FORM_ORDER
        if any(
            df.loc[f, (b, 'pct')] > 1.0
            for b in books
            if (b, 'pct') in df.columns
        )
    ]
    labels = [VERB_FORM_LABELS.get(f, f) for f in active_forms]

    x = np.arange(len(active_forms))
    width = 0.8 / len(books)

    fig, ax = plt.subplots(figsize=(max(10, len(active_forms) * 1.4), 6))
    colors = plt.cm.tab10.colors

    for i, book in enumerate(books):
        pcts = [
            df.loc[form, (book, 'pct')] if (book, 'pct') in df.columns else 0.0
            for form in active_forms
        ]
        offset = (i - len(books) / 2 + 0.5) * width
        bars = ax.bar(x + offset, pcts, width, label=book, color=colors[i % 10])
        for bar, val in zip(bars, pcts):
            if val > 2:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.3,
                    f"{val:.0f}",
                    ha='center', va='bottom', fontsize=7,
                )

    scope_str = f" ch.{chapter}" if chapter else ''
    ax.set_title(f"Verb Form Distribution{scope_str}: {' vs. '.join(books)}")
    ax.set_ylabel('% of verbs')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha='right')
    ax.legend()
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    if output_path is None:
        out_dir = Path('output') / 'charts' / 'ot' / 'verbs'
        out_dir.mkdir(parents=True, exist_ok=True)
        slug = '_'.join(books)
        if chapter:
            slug += f'_ch{chapter}'
        output_path = str(out_dir / f'aspect_comparison_{slug}.png')

    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return Path(output_path)
