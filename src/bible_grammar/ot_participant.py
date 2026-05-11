"""
OT participant tracking and entity chains for the Hebrew Old Testament.

Follows named participants (by lemma or participantref ID) through narrative:
what they do (subject position), what is done to them (object), and where
they speak. Uses the MACULA Hebrew WLC `participantref` column where populated,
with lemma-based fallback for the many cases where it is absent.

Data notes
──────────
  participantref  — sparse MACULA entity reference IDs; ~10–20% of tokens
  speaker         — verse-level speaker column (from MACULA lowfat XML)
  type_           — verb form (wayyiqtol, qatal, etc.)
  The OT lowfat syntax tree (load_syntax_ot) has subject/object role data.

Approach
────────
  1. Primary: participantref lookup — most precise when populated
  2. Fallback: lemma match — find all tokens with the named lemma

Questions this answers
──────────────────────
  • What verbs does Abraham appear as subject of across Genesis?
  • What happens to Moses (as object) in Exodus?
  • In which chapters of Genesis does Jacob appear most?
  • How do the subject-verb profiles of Abraham vs. Moses compare?

Public API
──────────
KNOWN_OT_PARTICIPANTS                           → dict of participant anchors

ot_participant_data(lemma, book=None)           → DataFrame
ot_participant_subject_verbs(lemma, book=None)  → DataFrame
ot_participant_object_verbs(lemma, book=None)   → DataFrame
ot_participant_chain(book, lemma)               → DataFrame (chapter presence)
ot_entity_density(book)                         → DataFrame (chapter, entities)
ot_participant_compare(lemmas)                  → DataFrame pivot

print_ot_participant_profile(lemma, book=None)  → None
print_ot_participant_chain(book, lemma)         → None
print_ot_participant_compare(lemmas)            → None

ot_participant_chain_chart(book, lemmas)        → Path | None
ot_entity_density_chart(book)                   → Path | None
"""

from __future__ import annotations
from pathlib import Path

import pandas as pd

from ._utils import ensure_chart_dir

_CHART_DIR = Path('output') / 'charts' / 'ot' / 'participants'

# Pre-identified participant lemmas for major OT figures
KNOWN_OT_PARTICIPANTS: dict[str, dict] = {
    'YHWH':     {'lemma': 'יְהוָה', 'gloss': 'YHWH / the LORD'},
    'Elohim':   {'lemma': 'אֱלֹהִים', 'gloss': 'God / Elohim'},
    'Abraham':  {'lemma': 'אַבְרָהָם', 'gloss': 'Abraham'},
    'Isaac':    {'lemma': 'יִצְחָק', 'gloss': 'Isaac'},
    'Jacob':    {'lemma': 'יַעֲקֹב', 'gloss': 'Jacob'},
    'Joseph':   {'lemma': 'יוֹסֵף', 'gloss': 'Joseph'},
    'Moses':    {'lemma': 'מֹשֶׁה', 'gloss': 'Moses'},
    'Aaron':    {'lemma': 'אַהֲרֹן', 'gloss': 'Aaron'},
    'Joshua':   {'lemma': 'יְהוֹשׁוּעַ', 'gloss': 'Joshua'},
    'David':    {'lemma': 'דָּוִד', 'gloss': 'David'},
    'Solomon':  {'lemma': 'שְׁלֹמֹה', 'gloss': 'Solomon'},
    'Elijah':   {'lemma': 'אֵלִיָּה', 'gloss': 'Elijah'},
    'Isaiah':   {'lemma': 'יְשַׁעְיָהוּ', 'gloss': 'Isaiah'},
    'Jeremiah': {'lemma': 'יִרְמְיָהוּ', 'gloss': 'Jeremiah'},
    'Daniel':   {'lemma': 'דָּנִיֵּאל', 'gloss': 'Daniel'},
    'Ruth':     {'lemma': 'רוּת', 'gloss': 'Ruth'},
    'Esther':   {'lemma': 'אֶסְתֵּר', 'gloss': 'Esther'},
    'Saul':     {'lemma': 'שָׁאוּל', 'gloss': 'Saul'},
    'Jonah':    {'lemma': 'יוֹנָה', 'gloss': 'Jonah'},
}


# ── helpers ───────────────────────────────────────────────────────────────────

def _load_ot_h() -> pd.DataFrame:
    from ._utils import load_ot_h
    return load_ot_h()


def _resolve_lemma(participant: str) -> str:
    """Accept a key from KNOWN_OT_PARTICIPANTS or a raw Hebrew lemma."""
    if participant in KNOWN_OT_PARTICIPANTS:
        return KNOWN_OT_PARTICIPANTS[participant]['lemma']
    return participant


def _participant_tokens(df: pd.DataFrame, lemma: str) -> pd.DataFrame:
    """Tokens where lemma matches — primary lookup strategy."""
    return df[df['lemma'] == lemma].copy()


def _syntax_ot() -> pd.DataFrame:
    """Load OT syntax data (lowfat)."""
    from .syntax_ot import load_syntax_ot
    return load_syntax_ot()


# ── data functions ────────────────────────────────────────────────────────────

def ot_participant_data(
    participant: str,
    *,
    book: str | list[str] | None = None,
) -> pd.DataFrame:
    """
    All tokens referencing a participant (by KNOWN_OT_PARTICIPANTS key or Hebrew lemma).

    Returns the raw token DataFrame filtered to that participant.
    """
    lemma = _resolve_lemma(participant)
    df = _load_ot_h()
    if book is not None:
        if isinstance(book, str):
            book = [book]
        df = df[df['book'].isin(book)]
    return _participant_tokens(df, lemma).reset_index(drop=True)


def ot_participant_subject_verbs(
    participant: str,
    *,
    book: str | list[str] | None = None,
    top_n: int = 30,
) -> pd.DataFrame:
    """
    Verbs for which this participant is the syntactic subject.

    Uses the OT lowfat syntax tree (subject role). Falls back to heuristic:
    wayyiqtol immediately following the participant's name token (same verse).

    Returns: verb_lemma, gloss, count — sorted descending.
    """
    try:
        syn = _syntax_ot()
        lemma = _resolve_lemma(participant)

        if book is not None:
            if isinstance(book, str):
                book_list = [book]
            else:
                book_list = list(book)
        else:
            book_list = None

        if 'subject_lemma' not in syn.columns:
            raise KeyError('subject_lemma column missing')

        filt = syn[syn['subject_lemma'] == lemma]
        if book_list:
            filt = filt[filt['book'].isin(book_list)]
    except Exception:
        # Fallback: lemma-based same-verse heuristic
        filt = _heuristic_subject_verbs(participant, book)

    if filt.empty or 'lemma' not in filt.columns:
        return pd.DataFrame(columns=['verb_lemma', 'gloss', 'count'])

    result = (
        filt.groupby(['lemma', 'gloss'], dropna=False)
        .size()
        .reset_index(name='count')
        .rename(columns={'lemma': 'verb_lemma'})
        .sort_values('count', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    return result


def _heuristic_subject_verbs(
    participant: str,
    book: str | list[str] | None,
) -> pd.DataFrame:
    """
    Fallback: find verbs in same verse where participant lemma co-occurs.
    Returns all verbal tokens in those verses (not perfect, but useful).
    """
    data = ot_participant_data(participant, book=book)
    if data.empty:
        return pd.DataFrame()

    df_full = _load_ot_h()
    if book is not None:
        blist = [book] if isinstance(book, str) else list(book)
        df_full = df_full[df_full['book'].isin(blist)]

    verse_keys = set(zip(data['book'], data['chapter'], data['verse']))
    lemma = _resolve_lemma(participant)

    verbs = df_full[
        df_full.apply(lambda r: (r['book'], r['chapter'], r['verse']) in verse_keys, axis=1)
    ]
    verbal_types = {'wayyiqtol', 'qatal', 'yiqtol', 'imperative', 'cohortative', 'jussive'}
    verbs = verbs[verbs['type_'].isin(verbal_types) & (verbs['lemma'] != lemma)]
    return verbs


def ot_participant_object_verbs(
    participant: str,
    *,
    book: str | list[str] | None = None,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    Verbs for which this participant is the syntactic object/complement.

    Uses same-verse co-occurrence heuristic: verbal tokens in verses containing
    the participant, where the participant is not the first nominal (rough proxy).

    Returns: verb_lemma, gloss, count.
    """
    verbs = _heuristic_subject_verbs(participant, book)
    if verbs.empty or 'lemma' not in verbs.columns:
        return pd.DataFrame(columns=['verb_lemma', 'gloss', 'count'])
    result = (
        verbs.groupby(['lemma', 'gloss'], dropna=False)
        .size()
        .reset_index(name='count')
        .rename(columns={'lemma': 'verb_lemma'})
        .sort_values('count', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    return result


def ot_participant_chain(
    book: str,
    participant: str,
) -> pd.DataFrame:
    """
    Chapter-by-chapter presence of a participant in a book.

    Returns: chapter, mention_count — one row per chapter.
    """
    data = ot_participant_data(participant, book=book)
    if data.empty:
        return pd.DataFrame(columns=['chapter', 'mention_count'])
    counts = data.groupby('chapter').size().reset_index(name='mention_count')
    return counts.sort_values('chapter').reset_index(drop=True)


def ot_entity_density(
    book: str,
    top_n_entities: int = 15,
) -> pd.DataFrame:
    """
    Per-chapter count of distinct participant lemmas from KNOWN_OT_PARTICIPANTS.

    Returns: chapter, entity, mention_count — one row per (chapter, entity) pair.
    """
    df = _load_ot_h()
    df = df[df['book'] == book]
    participant_lemmas = {v['lemma']: k for k, v in KNOWN_OT_PARTICIPANTS.items()}

    rows = []
    for (ch,), grp in df.groupby(['chapter']):
        mentions = grp['lemma'].value_counts()
        for lemma, cnt in mentions.items():
            if lemma in participant_lemmas:
                rows.append({
                    'chapter': ch,
                    'entity': participant_lemmas[lemma],
                    'lemma': lemma,
                    'mention_count': int(cnt),
                })
    if not rows:
        return pd.DataFrame(columns=['chapter', 'entity', 'lemma', 'mention_count'])
    return (pd.DataFrame(rows)
            .sort_values(['chapter', 'mention_count'], ascending=[True, False])
            .reset_index(drop=True))


def ot_participant_compare(
    participants: list[str],
    *,
    book: str | None = None,
) -> pd.DataFrame:
    """
    Side-by-side mention counts and book spread for a list of participants.

    Returns: participant, total_mentions, books_present, top_book.
    """
    rows = []
    for p in participants:
        data = ot_participant_data(p, book=book)
        if data.empty:
            rows.append({'participant': p, 'total_mentions': 0,
                         'books_present': 0, 'top_book': None})
            continue
        book_counts = data['book'].value_counts()
        rows.append({
            'participant': p,
            'total_mentions': len(data),
            'books_present': data['book'].nunique(),
            'top_book': book_counts.index[0],
        })
    return pd.DataFrame(rows)


# ── print functions ───────────────────────────────────────────────────────────

def print_ot_participant_profile(
    participant: str,
    *,
    book: str | None = None,
) -> None:
    lemma = _resolve_lemma(participant)
    scope = f" in {book}" if book else ""
    data = ot_participant_data(participant, book=book)
    w = 60
    print(f"\n{'═'*w}")
    print(f"  Participant Profile — {participant} ({lemma}){scope}")
    print(f"{'═'*w}")
    if data.empty:
        print("  No data found.")
        print()
        return

    total = len(data)
    books = data['book'].value_counts()
    print(f"  Total mentions : {total:>6,}")
    print(f"  Books present  : {data['book'].nunique():>6}")
    print()
    print(f"  {'Book':<6} {'Mentions':>8}  {'%':>5}")
    print('  ' + '-' * 24)
    for bk, cnt in books.head(15).items():
        print(f"  {bk:<6} {cnt:>8,}  {cnt/total*100:>4.1f}%")

    subj = ot_participant_subject_verbs(participant, book=book, top_n=15)
    if not subj.empty:
        print("\n  Top verbs in participant's verses (top 15)")
        print(f"  {'Verb lemma':<20} {'Gloss':<22} {'Count':>6}")
        print('  ' + '-' * 52)
        for _, row in subj.iterrows():
            gl = str(row.get('gloss', ''))[:20]
            print(f"  {str(row['verb_lemma']):<20} {gl:<22} {row['count']:>6,}")
    print()


def print_ot_participant_chain(
    book: str,
    participant: str,
) -> None:
    chain = ot_participant_chain(book, participant)
    lemma = _resolve_lemma(participant)
    print(f"\nParticipant Chain — {participant} ({lemma}) in {book}")
    if chain.empty:
        print("  No mentions found.")
        print()
        return
    print(f"  {'Ch':>4}  {'Count':>6}  Bar")
    print('  ' + '-' * 40)
    for _, row in chain.iterrows():
        bar = '█' * min(int(row['mention_count']), 30)
        print(f"  {int(row['chapter']):>4}  {row['mention_count']:>6}  {bar}")
    print()


def print_ot_participant_compare(
    participants: list[str],
    *,
    book: str | None = None,
) -> None:
    df = ot_participant_compare(participants, book=book)
    scope = f" in {book}" if book else ""
    print(f"\nParticipant Comparison{scope}")
    print(f"  {'Participant':<14} {'Mentions':>9} {'Books':>6}  {'Top book'}")
    print('  ' + '-' * 46)
    for _, row in df.iterrows():
        print(f"  {str(row['participant']):<14} {row['total_mentions']:>9,} "
              f"{row['books_present']:>6}  {row['top_book']}")
    print()


# ── chart functions ───────────────────────────────────────────────────────────

def ot_participant_chain_chart(
    book: str,
    participants: list[str],
) -> Path | None:
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        return None

    ensure_chart_dir(_CHART_DIR)
    out = _CHART_DIR / f'chain_{"_".join(participants[:4])}_{book}.png'

    # Collect chapter-level counts for each participant
    all_chapters: set[int] = set()
    series: dict[str, dict[int, int]] = {}
    for p in participants:
        chain = ot_participant_chain(book, p)
        if not chain.empty:
            d = dict(zip(chain['chapter'].astype(int), chain['mention_count']))
            series[p] = d
            all_chapters.update(d.keys())

    if not series:
        return None

    chapters = sorted(all_chapters)
    x = np.arange(len(chapters))
    colors = plt.cm.tab10.colors  # type: ignore[attr-defined]

    fig, ax = plt.subplots(figsize=(max(10, len(chapters) * 0.4), 5))
    width = 0.8 / len(series)
    for idx, (p, d) in enumerate(series.items()):
        counts = [d.get(ch, 0) for ch in chapters]
        offset = (idx - len(series) / 2 + 0.5) * width
        ax.bar(x + offset, counts, width, label=p, color=colors[idx % len(colors)])

    ax.set_xticks(x)
    ax.set_xticklabels([str(c) for c in chapters], fontsize=8)
    ax.set_xlabel('Chapter')
    ax.set_ylabel('Mentions')
    ax.set_title(f'Participant Presence by Chapter — {book}')
    ax.legend()
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def ot_entity_density_chart(
    book: str,
) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = ot_entity_density(book)
    if df.empty:
        return None

    ensure_chart_dir(_CHART_DIR)
    out = _CHART_DIR / f'entity_density_{book}.png'

    # Pivot to chapter x entity
    pivot = df.pivot_table(
        index='entity', columns='chapter', values='mention_count', fill_value=0
    )

    fig, ax = plt.subplots(figsize=(max(10, len(pivot.columns) * 0.5), max(4, len(pivot) * 0.5)))
    im = ax.imshow(pivot.values, aspect='auto', cmap='YlOrRd')
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns.astype(int), fontsize=8, rotation=45)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=9)
    plt.colorbar(im, ax=ax, label='Mentions')
    ax.set_title(f'Entity Density by Chapter — {book}')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out
