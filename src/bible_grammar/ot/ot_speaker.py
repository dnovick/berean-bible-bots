"""
OT speaker attribution — who speaks in the Hebrew Bible.

Uses MACULA Hebrew `subjref` links on speech verb tokens to resolve
which entity is the grammatical subject of each speech act.

Questions this answers
──────────────────────
  • What does YHWH say in Isaiah?
  • How many verses in each OT book contain divine speech?
  • What does Moses say vs. what does God say in Deuteronomy?
  • Who speaks in Job — God, Job, the friends, the narrator?
  • What proportion of Jeremiah is direct divine speech?

Public API
──────────
speaker_verses(speaker_strongs, corpus_df, ...)   → DataFrame of speech-verb tokens
divine_speech_by_book(...)                        → per-book divine speech counts
print_speaker_summary(speaker_strongs, ...)       → terminal table
speaker_report(speaker_strongs, ...)              → Markdown report

OT speech verbs tracked
───────────────────────
  אָמַר  H0559  say
  דָּבַר  H1696  speak
  קָרָא  H7121  call / proclaim
  עָנָה  H6030  answer
  צָוָה  H6680  command
  שָׁלַח H7971  send (indirect speech)
  נָאַם  H5001  declare (prophetic formula: 'oracle of YHWH')
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd

from ..core._utils import load_ot_data

# Hebrew speech verbs by Strong's number (zero-padded, no prefix)
SPEECH_VERB_STRONGS: set[str] = {
    '0559',  # אָמַר  — say
    '1696',  # דָּבַר  — speak
    '7121',  # קָרָא  — call, proclaim, read aloud
    '6030',  # עָנָה  — answer, respond
    '6680',  # צָוָה  — command, charge
    '7971',  # שָׁלַח — send (often with messenger speech)
    '5001',  # נָאַם  — declare (prophetic "oracle of YHWH")
}

# Convenience sets — same format as role_search.py
GOD_OT_SPEECH = {'H0430', 'H3068', 'H0136', 'H0410'}   # Elohim, YHWH, Adonai, El


def _load_ot() -> pd.DataFrame:
    return load_ot_data()


def _ot_id_to_info(df: pd.DataFrame) -> dict[str, dict]:
    """Map stripped xml_id → {strongnumberx, lemma, gloss} for the OT."""
    return (
        df.set_index(df['xml_id'].str.lstrip('o'))
        [['strongnumberx', 'lemma', 'gloss', 'strong_h']]
        .to_dict('index')
    )


def _normalise_strongs_ot(strongs: list[str]) -> set[str]:
    """Normalise Strong's numbers to OT zero-padded 4-digit format."""
    result = set()
    for s in strongs:
        s = s.strip().upper().lstrip('H')
        digits = s.rstrip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        suffix = s[len(digits):]
        try:
            result.add(f"{int(digits):04d}{suffix}")
        except ValueError:
            result.add(s)
    return result


def speaker_verses(
    speaker_strongs: list[str] | str,
    *,
    books: list[str] | None = None,
    speech_verbs: set[str] | None = None,
    include_tokens: bool = False,
    top_n: int | None = None,
) -> pd.DataFrame:
    """
    Return speech-verb tokens whose grammatical subject resolves to the
    given Strong's number(s).

    Parameters
    ----------
    speaker_strongs : Strong's number(s) for the speaker, e.g. ['H3068','H0430']
    books           : restrict to specific book_ids
    speech_verbs    : set of Strong's numbers for speech verbs to check
                      (default: SPEECH_VERB_STRONGS)
    include_tokens  : if True, return full token rows; if False, return
                      aggregated (verb_lemma, gloss, book, count) summary
    top_n           : return top N results (aggregated mode only)

    Returns a DataFrame sorted by count descending.
    """
    if isinstance(speaker_strongs, str):
        speaker_strongs = [speaker_strongs]

    targets = _normalise_strongs_ot(speaker_strongs)
    sv_set = speech_verbs or SPEECH_VERB_STRONGS

    df = _load_ot()
    id_map = df.set_index(df['xml_id'].str.lstrip('o'))['strongnumberx'].to_dict()

    sv_tokens = df[
        (df['pos'] == 'verb') &
        (df['strongnumberx'].isin(sv_set)) &
        df['subjref'].notna()
    ].copy()

    if books:
        sv_tokens = sv_tokens[sv_tokens['book'].isin(books)]

    matched = sv_tokens[
        sv_tokens['subjref'].map(lambda x: id_map.get(x, '') in targets)
    ].copy()

    if include_tokens:
        return matched.reset_index(drop=True)

    if matched.empty:
        return pd.DataFrame(columns=['verb_lemma', 'gloss', 'book', 'count'])

    agg = (
        matched.groupby(['lemma', 'gloss', 'book'])
        .size().reset_index(name='count')
        .rename(columns={'lemma': 'verb_lemma'})
        .sort_values('count', ascending=False)
    )
    if top_n:
        agg = agg.head(top_n)
    return agg.reset_index(drop=True)


def divine_speech_by_book(
    speaker_strongs: list[str] | str | None = None,
    *,
    count_mode: str = 'verses',
) -> pd.DataFrame:
    """
    Per-book count of divine speech events.

    Parameters
    ----------
    speaker_strongs : Strong's for the speaker (default: GOD_OT_SPEECH)
    count_mode      : 'verses' (distinct ref strings) or 'tokens' (raw verb count)

    Returns a DataFrame with columns: book, count, pct_of_total.
    The pct column is percentage of all speech-verb tokens in that book
    attributed to the given speaker.
    """
    if speaker_strongs is None:
        speaker_strongs = list(GOD_OT_SPEECH)
    if isinstance(speaker_strongs, str):
        speaker_strongs = [speaker_strongs]

    df = _load_ot()
    targets = _normalise_strongs_ot(speaker_strongs)
    id_map = df.set_index(df['xml_id'].str.lstrip('o'))['strongnumberx'].to_dict()

    all_sv = df[
        (df['pos'] == 'verb') & (df['strongnumberx'].isin(SPEECH_VERB_STRONGS))
    ]
    divine_sv = all_sv[
        all_sv['subjref'].notna() &
        all_sv['subjref'].map(lambda x: id_map.get(x, '') in targets)
    ]

    if count_mode == 'verses':
        divine_counts = divine_sv.groupby('book')['ref'].nunique().reset_index(name='count')
        total_counts = all_sv.groupby('book')['ref'].nunique().reset_index(name='total')
    else:
        divine_counts = divine_sv.groupby('book').size().reset_index(name='count')
        total_counts = all_sv.groupby('book').size().reset_index(name='total')

    result = divine_counts.merge(total_counts, on='book', how='left')
    result['pct'] = (result['count'] / result['total'] * 100).round(1)

    # Sort by canonical OT book order
    from ..core.syntax_ot import MACULA_OT_BOOK_MAP
    order = {v: i for i, v in enumerate(MACULA_OT_BOOK_MAP.values())}
    result['_ord'] = result['book'].map(lambda b: order.get(b, 999))
    return (
        result.sort_values('_ord')
        .drop(columns='_ord')
        .reset_index(drop=True)
    )


def who_speaks(
    book: str,
    *,
    top_n: int = 15,
) -> pd.DataFrame:
    """
    For a single OT book, show a breakdown of ALL speakers by frequency —
    how many speech-verb tokens does each entity take as subject?

    Useful for character studies: who dominates dialogue in Job? in Genesis?

    Returns a DataFrame with columns: speaker_strong, speaker_lemma,
    speaker_gloss, verb_count.
    """
    df = _load_ot()
    id_info = _ot_id_to_info(df)

    sv_tokens = df[
        (df['pos'] == 'verb') &
        (df['strongnumberx'].isin(SPEECH_VERB_STRONGS)) &
        df['subjref'].notna() &
        (df['book'] == book)
    ]

    rows = []
    for _, row in sv_tokens.iterrows():
        info = id_info.get(row['subjref'])
        if info:
            rows.append({
                'speaker_strong': info['strong_h'],
                'speaker_lemma':  info['lemma'],
                'speaker_gloss':  info['gloss'],
            })

    if not rows:
        return pd.DataFrame()

    result = pd.DataFrame(rows)
    return (
        result.groupby(['speaker_strong', 'speaker_lemma', 'speaker_gloss'])
        .size().reset_index(name='verb_count')
        .sort_values('verb_count', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def divine_speech_verses(
    book: str,
    speaker_strongs: list[str] | str | None = None,
    *,
    verb_lemma: str | None = None,
) -> list[str]:
    """
    Return sorted list of verse refs where the given speaker takes a
    speech verb as subject in the specified book.

    Useful for: list all verses in Isaiah where YHWH speaks directly.
    """
    if speaker_strongs is None:
        speaker_strongs = list(GOD_OT_SPEECH)
    tokens = speaker_verses(
        speaker_strongs, books=[book], include_tokens=True
    )
    if tokens.empty:
        return []
    if verb_lemma:
        tokens = tokens[tokens['lemma'] == verb_lemma]
    return sorted(tokens['ref'].unique().tolist())


def print_speaker_summary(
    speaker_strongs: list[str] | str,
    *,
    books: list[str] | None = None,
    top_n: int = 20,
    label: str | None = None,
) -> None:
    """Print a formatted table of speech verbs attributed to the given speaker."""
    if isinstance(speaker_strongs, str):
        speaker_strongs = [speaker_strongs]

    df = speaker_verses(speaker_strongs, books=books, top_n=top_n)
    display_label = label or '/'.join(speaker_strongs)
    scope = f" ({', '.join(books)})" if books else ''
    w = 72

    print(f"\n{'═'*w}")
    print(f"  Speech acts by: {display_label}{scope}  [OT]")
    print(f"{'═'*w}")

    if df.empty:
        print("  No results found.")
        print()
        return

    print(f"  {'Verb':<16} {'Gloss':<24} {'Book':<8} Count")
    print(f"  {'-'*15} {'-'*23} {'-'*7} -----")
    for _, row in df.iterrows():
        print(f"  {str(row['verb_lemma']):<16} {str(row['gloss']):<24} "
              f"{str(row['book']):<8} {row['count']:>5}")

    total = df['count'].sum()
    print(f"\n  Total speech-verb tokens: {total:,}")
    print()


def print_divine_speech_by_book(
    speaker_strongs: list[str] | str | None = None,
    *,
    label: str | None = None,
    min_count: int = 1,
) -> None:
    """Print per-book divine speech verse counts with percentage."""
    if speaker_strongs is None:
        speaker_strongs = list(GOD_OT_SPEECH)
    if isinstance(speaker_strongs, str):
        speaker_strongs = [speaker_strongs]

    df = divine_speech_by_book(speaker_strongs)
    df = df[df['count'] >= min_count]

    display_label = label or '/'.join(speaker_strongs)
    w = 60
    print(f"\n{'═'*w}")
    print(f"  Divine speech by book: {display_label}  [OT]")
    print(f"{'═'*w}")
    print(f"  {'Book':<8} {'Verses':>8} {'Of Total':>10}  {'Pct':>6}")
    print(f"  {'-'*7} {'-'*8} {'-'*10}  {'-'*6}")
    for _, row in df.iterrows():
        print(f"  {row['book']:<8} {int(row['count']):>8} {int(row['total']):>10}  {row['pct']:>5.1f}%")  # noqa: E501
    print()


def speaker_report(
    speaker_strongs: list[str] | str,
    *,
    books: list[str] | None = None,
    top_n: int = 30,
    label: str | None = None,
    output_dir: str = 'output/reports',
) -> str:
    """
    Generate a Markdown report of speech acts by the given speaker.

    Returns path to saved Markdown file.
    """
    if isinstance(speaker_strongs, str):
        speaker_strongs = [speaker_strongs]

    display_label = label or '/'.join(speaker_strongs)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = display_label.replace('/', '-').replace(' ', '').lower()
    scope_str = f"-{'-'.join(books)}" if books else ''
    md_path = out_dir / f'speaker-{slug}{scope_str}-ot.md'

    df_sv = speaker_verses(speaker_strongs, books=books, top_n=top_n)
    df_by_book = divine_speech_by_book(speaker_strongs)
    df_by_book = df_by_book[df_by_book['count'] > 0]

    scope_label = f" in {', '.join(books)}" if books else ''

    lines = [
        f"# OT Speaker Attribution: {display_label}{scope_label}",
        "",
        f"Speech-verb tokens whose grammatical subject is **{display_label}**, "
        f"resolved via MACULA Hebrew `subjref` links.",
        "",
        "> **Method:** MACULA Hebrew tags each speech verb token with a `subjref` "
        "attribute pointing to its grammatical subject. This analysis finds all "
        "speech-verb tokens (אָמַר, דָּבַר, קָרָא, עָנָה, צָוָה, שָׁלַח, נָאַם) "
        "where that subject resolves to the given Strong's number(s).",
        "",
        "## Speech Verbs by Book",
        "",
        "| Book | Speech Verses | Of All Speech | Pct |",
        "|---|---:|---:|---:|",
    ]
    for _, row in df_by_book.iterrows():
        lines.append(
            f"| {row['book']} | {int(row['count'])} | {int(row['total'])} | {row['pct']}% |"
        )

    lines += [
        "",
        "## Top Speech-Verb Instances",
        "",
        "| Verb | Gloss | Book | Count |",
        "|---|---|---|---:|",
    ]
    for _, row in df_sv.iterrows():
        lines.append(f"| {row['verb_lemma']} | {row['gloss']} | {row['book']} | {row['count']} |")

    # Who speaks section — for scoped reports, show character dialogue breakdown
    if books:
        lines += ["", "## All Speakers (for comparison)", ""]
        for book in books:
            ws = who_speaks(book, top_n=10)
            if ws.empty:
                continue
            lines += [f"### {book}", "", "| Speaker | Lemma | Gloss | Verb Count |",
                      "|---|---|---|---:|"]
            for _, row in ws.iterrows():
                lines.append(
                    f"| {row['speaker_strong']} | {row['speaker_lemma']} "
                    f"| {row['speaker_gloss']} | {row['verb_count']} |"
                )
            lines.append("")

    lines += [
        "---",
        "",
        "_Source: MACULA Hebrew WLC (CC BY 4.0, Clear Bible). "
        "Syntactic subject resolved via `subjref` attribute in the MACULA "
        "lowfat syntax trees. Speech verbs: H0559 אָמַר, H1696 דָּבַר, "
        "H7121 קָרָא, H6030 עָנָה, H6680 צָוָה, H7971 שָׁלַח, H5001 נָאַם._",
    ]

    md_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  Saved: {md_path}")
    return str(md_path)
