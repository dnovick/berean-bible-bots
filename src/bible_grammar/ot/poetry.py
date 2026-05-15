"""
Hebrew poetry analysis: cola splitting, parallelism detection, and word-pair statistics.

Hebrew poetry is organized into poetic lines (verses) divided into cola (half-lines)
by the cantillation accent system embedded in the MT text. The Etnahta (U+0591)
marks the main mid-verse division (end of A-colon); the Silluq / Sof Pasuq marks
verse end (end of B- or final colon). Stronger disjunctive accents (Zaqef, Revia,
Tifha, Athnach) subdivide further, yielding C-cola in longer verses.

Parallelism types (after Lowth / Watson / Alter):
  synonymous  — A and B express the same idea with different words
  antithetic  — A and B express contrasting ideas
  synthetic   — B extends, intensifies, or completes A
  emblematic  — one colon is literal, one figurative (simile/metaphor)

This module detects cola boundaries from accents, extracts content-word pairs across
cola, scores lexical / semantic similarity, and classifies parallelism.

Public API
──────────
split_cola(verse_df)                → list[DataFrame] — one df per colon
verse_parallel_pairs(book, ch, vs) → DataFrame of A/B word pairs
parallelism_type(book, ch, vs)     → str classification
book_word_pairs(book)              → most common A/B parallel word pairs
print_verse_analysis(book, ch, vs) → formatted terminal output
parallel_word_pair_table(book)     → canonical parallel pair inventory
POETRY_BOOKS                       → list of primary Hebrew poetry books
"""

from __future__ import annotations
import unicodedata
from pathlib import Path

import pandas as pd

from ..core._utils import load_ot_data

# ── Constants ─────────────────────────────────────────────────────────────────

POETRY_BOOKS = ['Psa', 'Pro', 'Job', 'Sng', 'Lam', 'Ecc']

# Cantillation accent codepoints — disjunctive (clause-dividing) accents only
# Ordered roughly by strength (strongest first)
_ACCENT_NAMES = {
    0x0591: 'etnahta',       # main A/B divider — strongest mid-verse pause
    0x05C3: 'sof_pasuq',     # verse end
    0x0592: 'segolta',
    0x0593: 'shalshelet',
    0x0594: 'zaqef_qatan',
    0x0595: 'zaqef_gadol',
    0x0596: 'tifha',
    0x0597: 'revia',
    0x0598: 'zarqa',
    0x059A: 'yetiv',
    0x059B: 'tevir',
    0x059C: 'geresh',
    0x059D: 'geresh_muqdam',
    0x059E: 'gershayim',
    0x059F: 'qarney_para',
    0x05A0: 'telisha_gedola',
    0x05A1: 'pazer',
    0x05A3: 'munah',         # conjunctive (but sometimes marks sub-division)
    0x05A8: 'qadma',
    0x05A9: 'telisha_qetana',
    0x05AA: 'yerah_ben_yomo',
    0x05AB: 'ole',
    0x05AC: 'iluy',
    0x05AD: 'dehi',
    0x05AE: 'zinor',
    0x05AF: 'masora',
}

# Accents that mark primary (strong) cola boundaries
_PRIMARY_DIVIDERS = {0x0591}       # etnahta: always splits A from B
_VERSE_END = {0x05C3, 0x05BD}      # sof pasuq; meteg sometimes used at verse end

# Content-word parts of speech (exclude particles, conjunctions, prepositions)
_CONTENT_POS = {'noun', 'verb', 'adjective', 'adverb'}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _has_accent(text: str, codepoints: set[int]) -> bool:
    """Return True if the text contains any of the given accent codepoints."""
    return any(ord(c) in codepoints for c in text)


def _accent_in(text: str) -> set[int]:
    """Return set of accent codepoints present in the text."""
    return {ord(c) for c in text if ord(c) in _ACCENT_NAMES}


def _strip_cantillation(text: str) -> str:
    """Remove cantillation marks (but keep consonants and vowel points)."""
    return ''.join(c for c in text if unicodedata.category(c) != 'Mn'
                   or ord(c) < 0x0591 or ord(c) > 0x05C7)


def _is_content_word(pos: str) -> bool:
    return str(pos).lower() in _CONTENT_POS


def _load_macula() -> pd.DataFrame:
    return load_ot_data()


# ── Cola splitting ─────────────────────────────────────────────────────────────

def split_cola(verse_df: pd.DataFrame) -> list[pd.DataFrame]:
    """
    Split a verse DataFrame (one row per word) into cola based on cantillation
    accents embedded in the `text` column.

    Returns a list of DataFrames: [colon_A, colon_B] or [A, B, C] for longer
    verses. Each colon includes the word that carries the dividing accent.

    The primary split is at the Etnahta (U+0591). If no Etnahta is found,
    falls back to splitting on Zaqef Gadol (U+0595) or Revia (U+0597).
    Single-word or empty verses return [verse_df].
    """
    if verse_df.empty or len(verse_df) <= 1:
        return [verse_df]

    texts = verse_df['text'].tolist()

    # Find Etnahta position
    etnahta_idx = None
    for i, t in enumerate(texts):
        if _has_accent(t, _PRIMARY_DIVIDERS):
            etnahta_idx = i
            break

    if etnahta_idx is None:
        # Try secondary dividers: Zaqef Gadol, Revia, Tifha
        secondary = {0x0595, 0x0597, 0x0596}
        for i, t in enumerate(texts):
            if _has_accent(t, secondary) and i > 0:
                etnahta_idx = i
                break

    if etnahta_idx is None or etnahta_idx == len(texts) - 1:
        # No mid-verse split found or split is at last word
        return [verse_df]

    cola_a = verse_df.iloc[:etnahta_idx + 1].copy()
    remainder = verse_df.iloc[etnahta_idx + 1:].copy()

    # Check for a C-colon: secondary split in remainder (skip last word = verse end)
    c_idx = None
    for i, t in enumerate(remainder['text'].tolist()[:-1]):
        if _has_accent(t, {0x0595, 0x0597, 0x0596, 0x0594}):
            c_idx = i
            break

    if c_idx is not None and c_idx < len(remainder) - 1:
        cola_b = remainder.iloc[:c_idx + 1].copy()
        cola_c = remainder.iloc[c_idx + 1:].copy()
        return [cola_a, cola_b, cola_c]

    return [cola_a, remainder]


# ── Psalm superscription handling ────────────────────────────────────────────

# Psalms whose verse 1 in the Hebrew MT is a superscription (not poetry).
# English Bibles typically fold the superscription into the heading and number
# the actual poetry starting at English v.1 = Hebrew v.2.
# Psalms with no superscription (e.g. 1, 2, 10, 33…) are not affected.
#
# Rather than hardcode every psalm, we detect superscriptions heuristically:
# verse 1 of a psalm is likely a superscription if it contains לַמְנַצֵּחַ
# (to the choirmaster), מִזְמוֹר (psalm), שִׁיר (song), מַשְׂכִּיל (maskil),
# or similar liturgical lemmas — and has no Etnahta mid-verse split (i.e. it
# is a single short label rather than a bicolon).

_SUPERSCRIPTION_LEMMAS = {
    'נָצַח',     # lamnatstseak — to the choirmaster
    'מִזְמוֹר',  # mizmor — psalm
    'שִׁיר',     # shir — song
    'מַשְׂכִּיל',  # maskil
    'מִכְתָּם',  # miktam
    'תְּפִלָּה',  # tefillah — prayer
    'תְּהִלָּה',  # tehillah — praise
    'לְדָוִד',   # of David (used as marker)
    'דָּוִד',    # David
    'שְׁלֹמֹה',  # Solomon
    'אָסָף',     # Asaph
    'קֹרַח',     # Korah
    'הֵמָן',     # Heman
    'אֵיתָן',    # Ethan
    'מֹשֶׁה',    # Moses
}


def is_superscription(book: str, chapter: int, verse: int) -> bool:
    """
    Return True if this verse appears to be a Psalm superscription.

    A verse is considered a superscription if:
      - It is verse 1 of a Psalm chapter
      - The majority of its content words are superscription lemmas
      - The total word count is short (≤8 content words — headings are brief)

    Note: MACULA places an Etnahta between "To the choirmaster" and "A psalm of David",
    so the "no mid-verse split" heuristic is unreliable; we use lemma ratio instead.
    """
    if book != 'Psa' or verse != 1:
        return False
    df = _load_macula()
    v = df[(df['book'] == book) & (df['chapter'] == chapter) & (df['verse'] == verse)]
    if v.empty:
        return False
    cw = _content_words(v)
    if cw.empty:
        return True
    if len(cw) > 8:
        return False  # too long to be a heading
    sup_count = sum(1 for lemma in cw['lemma'] if lemma in _SUPERSCRIPTION_LEMMAS)
    return sup_count / len(cw) > 0.4


def verse_cola(book: str, chapter: int, verse: int) -> list[pd.DataFrame]:
    """Return the cola for a single verse."""
    df = _load_macula()
    v = df[(df['book'] == book) & (df['chapter'] == chapter) & (df['verse'] == verse)]
    return split_cola(v)


# ── Content-word extraction ───────────────────────────────────────────────────

def _content_words(colon_df: pd.DataFrame) -> pd.DataFrame:
    """Extract content words (nouns, verbs, adjectives) from a colon."""
    mask = colon_df['class_'].str.lower().isin({'noun', 'verb', 'adj', 'adv'})
    return colon_df[mask].copy()


# ── Semantic domain overlap ───────────────────────────────────────────────────

def _domains(colon_df: pd.DataFrame) -> set[str]:
    """Return the set of coredomain codes present in a colon's content words."""
    domains: set[str] = set()
    for raw in colon_df['coredomain'].dropna():
        for code in str(raw).split():
            if code.strip():
                domains.add(code.strip()[:3])  # top-level domain prefix
    return domains


def _lexical_overlap(a: pd.DataFrame, b: pd.DataFrame) -> float:
    """Fraction of lemmas shared between two cola (0.0–1.0)."""
    la = set(a['lemma'].dropna())
    lb = set(b['lemma'].dropna())
    if not la or not lb:
        return 0.0
    return len(la & lb) / len(la | lb)


def _domain_overlap(a: pd.DataFrame, b: pd.DataFrame) -> float:
    """Fraction of semantic domain codes shared between two cola."""
    da = _domains(a)
    db = _domains(b)
    if not da or not db:
        return 0.0
    return len(da & db) / len(da | db)


# ── Parallelism word pairs ─────────────────────────────────────────────────────

def verse_parallel_pairs(
    book: str,
    chapter: int,
    verse: int,
) -> pd.DataFrame:
    """
    Return a DataFrame of content-word pairs across cola A and B for a verse.

    For each content word in colon A, pairs it with each content word in colon B,
    yielding a row with:
      lemma_a, gloss_a, strong_a, lemma_b, gloss_b, strong_b,
      same_lemma (bool), domain_overlap (float), book, chapter, verse
    """
    cola = verse_cola(book, chapter, verse)
    if len(cola) < 2:
        return pd.DataFrame()

    a_words = _content_words(cola[0])
    b_words = _content_words(cola[1])

    if a_words.empty or b_words.empty:
        return pd.DataFrame()

    rows = []
    for _, wa in a_words.iterrows():
        for _, wb in b_words.iterrows():
            la = str(wa.get('lemma', ''))
            lb = str(wb.get('lemma', ''))
            da = set(str(wa.get('coredomain', '')).split())
            db = set(str(wb.get('coredomain', '')).split())
            dom_overlap = len(da & db) / len(da | db) if da | db else 0.0
            rows.append({
                'lemma_a':   la,
                'gloss_a':   str(wa.get('gloss', '')),
                'strong_a':  str(wa.get('strong_h', '')),
                'lemma_b':   lb,
                'gloss_b':   str(wb.get('gloss', '')),
                'strong_b':  str(wb.get('strong_h', '')),
                'same_lemma': la == lb and la != '',
                'domain_overlap': round(dom_overlap, 2),
                'book':    book,
                'chapter': chapter,
                'verse':   verse,
            })

    return pd.DataFrame(rows)


def book_word_pairs(
    book: str,
    *,
    min_count: int = 2,
    top_n: int = 40,
    content_only: bool = True,
) -> pd.DataFrame:
    """
    Most frequent A/B parallel word pairs across all verses in a book.

    Returns a DataFrame: lemma_a | gloss_a | lemma_b | gloss_b | count
    sorted by count descending.
    """
    df = _load_macula()
    verses = df[(df['book'] == book)][['chapter', 'verse']].drop_duplicates()

    all_pairs: list[pd.DataFrame] = []
    for _, row in verses.iterrows():
        try:
            pairs = verse_parallel_pairs(book, int(row['chapter']), int(row['verse']))
            if not pairs.empty:
                all_pairs.append(pairs)
        except Exception:
            pass

    if not all_pairs:
        return pd.DataFrame()

    combined = pd.concat(all_pairs, ignore_index=True)

    agg = (
        combined.groupby(['lemma_a', 'gloss_a', 'lemma_b', 'gloss_b'])
        .size().reset_index(name='count')
        .sort_values('count', ascending=False)
    )
    agg = agg[agg['count'] >= min_count]
    return agg.head(top_n).reset_index(drop=True)


# ── Parallelism classification ────────────────────────────────────────────────

def parallelism_type(
    book: str,
    chapter: int,
    verse: int,
) -> tuple[str, float]:
    """
    Classify the parallelism type for a verse.

    Returns (type_label, confidence_score) where type_label is one of:
      'synonymous'  — high lexical/domain overlap, same polarity
      'antithetic'  — low lexical overlap, antithetic markers present
      'synthetic'   — low overlap, no antithetic marker; B extends A
      'single_colon'— verse has only one colon (no split found)

    Confidence is 0.0–1.0; classifications below 0.3 are uncertain.

    This is a heuristic classifier — it captures the dominant type for clear
    cases and marks ambiguous ones as 'synthetic' (the catch-all).
    """
    cola = verse_cola(book, chapter, verse)
    if len(cola) < 2:
        return ('single_colon', 1.0)

    a_cw = _content_words(cola[0])
    b_cw = _content_words(cola[1])

    lex = _lexical_overlap(a_cw, b_cw)
    dom = _domain_overlap(a_cw, b_cw)

    # Antithetic markers: look for negation or antithetical conjunctions in B-colon
    ' '.join(cola[1]['text'].tolist())
    b_gloss = ' '.join(cola[1]['gloss'].fillna('').tolist()).lower()
    has_negation = any(neg in cola[1]['lemma'].tolist()
                       for neg in ['לֹא', 'אַל', 'בַּל'])
    has_antithetic_conj = 'but' in b_gloss or 'however' in b_gloss or 'yet' in b_gloss

    combined_score = (lex + dom) / 2

    if combined_score >= 0.35:
        return ('synonymous', round(combined_score, 2))
    elif has_negation or has_antithetic_conj:
        return ('antithetic', round(0.5 + combined_score, 2))
    else:
        return ('synthetic', round(0.4 - combined_score, 2))


# ── Book-level statistics ──────────────────────────────────────────────────────

def book_parallelism_stats(book: str) -> pd.DataFrame:
    """
    Count parallelism types across all verses in a book.

    Returns a DataFrame: type | count | pct
    """
    df = _load_macula()
    verses = df[(df['book'] == book)][['chapter', 'verse']].drop_duplicates()

    counts: dict[str, int] = {}
    for _, row in verses.iterrows():
        ptype, _ = parallelism_type(book, int(row['chapter']), int(row['verse']))
        counts[ptype] = counts.get(ptype, 0) + 1

    total = sum(counts.values())
    rows = [{'type': k, 'count': v, 'pct': round(v / total * 100, 1)}
            for k, v in sorted(counts.items(), key=lambda x: -x[1])]
    return pd.DataFrame(rows)


def compare_poetry_books(
    books: list[str] | None = None,
) -> pd.DataFrame:
    """
    Compare parallelism type distribution across multiple poetry books.
    Returns a pivot DataFrame: rows=type, cols=books, values=pct.
    """
    books = books or POETRY_BOOKS
    profiles: dict[str, pd.Series] = {}
    for b in books:
        try:
            stats = book_parallelism_stats(b)
            if not stats.empty:
                profiles[b] = stats.set_index('type')['pct']
        except Exception:
            pass

    if not profiles:
        return pd.DataFrame()

    result = pd.DataFrame(profiles).fillna(0).round(1)
    result['_avg'] = result.mean(axis=1)
    return result.sort_values('_avg', ascending=False).drop(columns='_avg')


# ── Terminal output ───────────────────────────────────────────────────────────

def print_verse_analysis(
    book: str,
    chapter: int,
    verse: int,
    *,
    show_accents: bool = False,
) -> None:
    """Print a formatted cola analysis for a single verse."""
    # Warn if this looks like a Psalm superscription
    if is_superscription(book, chapter, verse):
        print(f"\n  Note: {book} {chapter}:{verse} appears to be a superscription "
              f"(liturgical heading), not a poetic bicolon.")
        print("  Hebrew versification counts superscriptions as verse 1; "
              "English Bibles fold them into the heading.")
        print(f"  Try verse {verse + 1} for the first line of actual poetry.\n")

    cola = verse_cola(book, chapter, verse)
    ptype, conf = parallelism_type(book, chapter, verse)

    ref = f"{book} {chapter}:{verse}"
    w = 72
    print(f"\n{'═'*w}")
    print(f"  {ref}  —  Parallelism: {ptype.upper()}  (confidence {conf:.2f})")
    print(f"{'═'*w}")

    labels = ['A', 'B', 'C']
    for i, colon in enumerate(cola):
        label = labels[i] if i < len(labels) else str(i + 1)
        words = colon['text'].tolist()
        glosses = colon['gloss'].fillna('').tolist()
        lemmas = colon['lemma'].fillna('').tolist()
        hebrew = ' '.join(words)
        print(f"\n  Colon {label}:  {hebrew}")
        print(f"  {'─'*60}")
        print(f"  {'Word':<25} {'Lemma':<18} {'Gloss'}")
        print(f"  {'─'*24} {'─'*17} {'─'*20}")
        for word, lemma, gloss in zip(words, lemmas, glosses):
            _strip_cantillation(word)
            print(f"  {word:<25} {lemma:<18} {gloss}")
        cw = _content_words(colon)
        if not cw.empty:
            cw_lemmas = ' · '.join(cw['lemma'].dropna().tolist())
            print(f"  Content words: {cw_lemmas}")

    if len(cola) >= 2:
        a_cw = _content_words(cola[0])
        b_cw = _content_words(cola[1])
        lex = _lexical_overlap(a_cw, b_cw)
        dom = _domain_overlap(a_cw, b_cw)
        print(f"\n  Lexical overlap: {lex:.0%}   Domain overlap: {dom:.0%}")

        # Shared lemmas
        shared = set(a_cw['lemma'].dropna()) & set(b_cw['lemma'].dropna())
        if shared:
            print(f"  Shared lemmas: {' · '.join(shared)}")
    print()


def print_book_pairs(
    book: str,
    *,
    top_n: int = 20,
    min_count: int = 3,
) -> None:
    """Print the most frequent parallel word pairs in a poetry book."""
    df = book_word_pairs(book, top_n=top_n, min_count=min_count)
    w = 76
    print(f"\n{'═'*w}")
    print(f"  Most frequent A/B parallel word pairs: {book}")
    print(f"{'═'*w}")

    if df.empty:
        print("  No pairs found.")
        return

    print(f"  {'Colon A lemma':<18} {'Gloss A':<22} {'Colon B lemma':<18} {'Gloss B':<20} Count")
    print(f"  {'─'*17} {'─'*21} {'─'*17} {'─'*19} ─────")
    for _, row in df.iterrows():
        print(
            f"  {str(row['lemma_a']):<18} {str(row['gloss_a']):<22} "
            f"{str(row['lemma_b']):<18} {str(row['gloss_b']):<20} "
            f"{int(row['count']):>5}"
        )
    print()


def print_parallelism_stats(book: str) -> None:
    """Print parallelism type distribution for a book."""
    df = book_parallelism_stats(book)
    w = 50
    print(f"\n{'═'*w}")
    print(f"  Parallelism types: {book}")
    print(f"{'═'*w}")
    if df.empty:
        print("  No data.")
        return
    for _, row in df.iterrows():
        bar = '█' * int(row['pct'] / 2)
        print(f"  {str(row['type']):<14} {row['count']:>5}  {row['pct']:>5.1f}%  {bar}")
    print()


# ── Report ────────────────────────────────────────────────────────────────────

def poetry_report(
    book: str,
    *,
    output_dir: str = 'output/reports',
    top_n_pairs: int = 30,
) -> str:
    """
    Generate a Markdown report on the poetry of a book:
      - parallelism type distribution
      - top parallel word pairs
    Returns path to saved Markdown file.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    md_path = out / f'poetry-{book.lower()}.md'

    stats = book_parallelism_stats(book)
    pairs = book_word_pairs(book, top_n=top_n_pairs, min_count=2)

    lines = [
        f"# Hebrew Poetry Analysis: {book}",
        "",
        "## Parallelism Type Distribution",
        "",
        "| Type | Count | % |",
        "|---|---:|---:|",
    ]
    for _, r in stats.iterrows():
        lines.append(f"| {r['type']} | {r['count']} | {r['pct']}% |")

    lines += [
        "",
        f"## Top {top_n_pairs} Parallel Word Pairs",
        "",
        "| Colon A | Gloss A | Colon B | Gloss B | Count |",
        "|---|---|---|---|---:|",
    ]
    for _, r in pairs.iterrows():
        lines.append(
            f"| {r['lemma_a']} | {r['gloss_a']} | {r['lemma_b']} | {r['gloss_b']} | {r['count']} |"
        )

    lines += [
        "",
        "---",
        "_Sources: MACULA Hebrew WLC (Clear Bible, CC BY 4.0). "
        "Cola split by Etnahta cantillation accent (U+0591)._",
    ]

    md_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  Saved: {md_path}")
    return str(md_path)


# ═══════════════════════════════════════════════════════════════════════════════
# CHIASM DETECTION
# ═══════════════════════════════════════════════════════════════════════════════
#
# A chiasm (or chiasmus) is a rhetorical structure A B ... B' A' where the
# outer elements mirror the inner elements. In Hebrew poetry this often spans
# several verses.
#
# Detection approach:
#   1. Extract a lemma "fingerprint" for each verse (set of content-word lemmas).
#   2. Build a similarity matrix over the verse range.
#   3. Search for the anti-diagonal pattern: verse[i] ≅ verse[n-1-i].
#   4. Score by average pairwise Jaccard similarity of the mirrored pairs.
#   5. Also detect the optional central pivot (single verse with no mirror).
#
# This is heuristic — Hebrew scholars debate chiasm boundaries and significance.
# Treat output as a starting point for manual study, not a definitive verdict.
# ───────────────────────────────────────────────────────────────────────────────

def _verse_lemma_set(macula: pd.DataFrame, book: str, ch: int, vs: int) -> set[str]:
    """Return the set of content-word lemmas for one verse."""
    book_col = 'book_id' if 'book_id' in macula.columns else 'book'
    rows = macula[
        (macula[book_col] == book) &
        (macula['chapter'] == ch) &
        (macula['verse'] == vs)
    ]
    out: set[str] = set()
    for _, r in rows.iterrows():
        if _is_content_word(str(r.get('class_', ''))):
            lem = str(r.get('lemma', '') or r.get('lemma_id', '') or '')
            if lem:
                out.add(lem)
    return out


def _jaccard(a: set | frozenset, b: set | frozenset) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def detect_chiasm(
    book: str,
    chapter: int,
    start_verse: int,
    end_verse: int,
    *,
    min_score: float = 0.10,
) -> dict:
    """
    Detect chiastic (A B B' A') structure across a verse range.

    Parameters
    ----------
    book, chapter       : book ID and chapter number
    start_verse, end_verse : inclusive verse range (within one chapter)
    min_score           : minimum average mirror-pair Jaccard to report a hit

    Returns a dict with keys:
      pattern      : list of str labels e.g. ['A', 'B', 'B\'', 'A\'']
      verses       : list of (ch, vs) tuples in order
      pairs        : list of ((ch1,vs1), (ch2,vs2), score) for each mirror pair
      pivot        : (ch, vs) or None if even number of verses
      mean_score   : float — average Jaccard across mirror pairs
      is_chiasm    : bool — True if mean_score >= min_score
      lemma_sets   : dict mapping (ch,vs) → frozenset of lemmas
    """
    macula = _load_macula()
    verses = list(range(start_verse, end_verse + 1))
    n = len(verses)

    lemma_sets: dict[tuple, frozenset] = {}
    for vs in verses:
        ls = _verse_lemma_set(macula, book, chapter, vs)
        lemma_sets[(chapter, vs)] = frozenset(ls)

    pairs = []
    n_pairs = n // 2
    for i in range(n_pairs):
        v_outer = (chapter, verses[i])
        v_inner = (chapter, verses[n - 1 - i])
        score = _jaccard(lemma_sets[v_outer], lemma_sets[v_inner])
        pairs.append((v_outer, v_inner, score))

    pivot = (chapter, verses[n // 2]) if n % 2 == 1 else None
    mean_score = sum(s for _, _, s in pairs) / len(pairs) if pairs else 0.0

    # Build letter labels A, B, C …
    letters = [chr(ord('A') + i) for i in range(n_pairs)]
    pattern = []
    for i in range(n):
        mirror_idx = n - 1 - i
        pair_idx = min(i, mirror_idx)
        letter = letters[pair_idx] if pair_idx < len(letters) else '?'
        if i < n // 2:
            pattern.append(letter)
        elif n % 2 == 1 and i == n // 2:
            pattern.append('X')   # pivot
        else:
            pattern.append(letter + "'")

    return {
        'pattern': pattern,
        'verses': [(chapter, v) for v in verses],
        'pairs': pairs,
        'pivot': pivot,
        'mean_score': mean_score,
        'is_chiasm': mean_score >= min_score,
        'lemma_sets': lemma_sets,
    }


def print_chiasm(
    book: str,
    chapter: int,
    start_verse: int,
    end_verse: int,
    *,
    min_score: float = 0.10,
) -> None:
    """Print a formatted chiasm analysis for a verse range."""
    result = detect_chiasm(book, chapter, start_verse, end_verse,
                           min_score=min_score)
    n = len(result['verses'])
    label = f"{book} {chapter}:{start_verse}–{end_verse}"

    print()
    print('═' * 72)
    verdict = 'CHIASM DETECTED' if result['is_chiasm'] else 'weak / no chiasm'
    print(f"  Chiasm analysis: {label}  [{verdict}]")
    print(f"  Mirror-pair mean Jaccard: {result['mean_score']:.3f}")
    print('─' * 72)

    macula = _load_macula()
    book_col = 'book_id' if 'book_id' in macula.columns else 'book'
    for i, (ch, vs) in enumerate(result['verses']):
        label_tag = result['pattern'][i]
        rows = macula[
            (macula[book_col] == book) &
            (macula['chapter'] == ch) &
            (macula['verse'] == vs)
        ]
        words = ' '.join(str(r.get('text', '')) for _, r in rows.iterrows())
        result['lemma_sets'][(ch, vs)]
        shared = ''
        # find which pair this verse belongs to for overlap hint
        mirror_idx = n - 1 - i
        if i != mirror_idx:
            other_key = result['verses'][mirror_idx]
            overlap = result['lemma_sets'][(ch, vs)] & result['lemma_sets'][other_key]
            if overlap:
                shared = '  [shared: ' + ', '.join(sorted(overlap)[:4]) + ']'
        print(f"  {label_tag:<4} {book} {ch}:{vs:<4}  {words[:50]:<50}{shared}")

    print()
    print('  Mirror pairs:')
    for (ch1, vs1), (ch2, vs2), score in result['pairs']:
        bar = '█' * int(score * 20)
        print(f"    {book} {ch1}:{vs1} ↔ {book} {ch2}:{vs2}  "
              f"Jaccard={score:.3f}  {bar}")
    if result['pivot']:
        ch, vs = result['pivot']
        print(f"\n  Pivot (X): {book} {ch}:{vs}")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# ACROSTIC DETECTION
# ═══════════════════════════════════════════════════════════════════════════════
#
# An acrostic is a poem where successive verses (or stanzas) begin with
# successive letters of the Hebrew alphabet (aleph through tav = 22 letters).
#
# Known acrostics in the Hebrew Bible:
#   Psalm 9–10 (partial), 25, 34, 37, 111, 112, 119, 145
#   Proverbs 31:10–31 (the virtuous woman)
#   Lamentations 1, 2, 3 (triple acrostic), 4
#   Nahum 1:2–8 (partial)
#
# Detection: check whether the first consonant of the first word of each verse
# follows the Hebrew alphabet order. We strip vowel points and cantillation
# so only the leading consonant is compared.
# ───────────────────────────────────────────────────────────────────────────────

# Hebrew alphabet in order (consonantal)
_HEB_ALPHABET = list('אבגדהוזחטיכלמנסעפצקרשת')

# Map from first letter → alphabet position (0-based)
_HEB_LETTER_POS = {c: i for i, c in enumerate(_HEB_ALPHABET)}

# Known acrostics for reference (OSIS book + chapter or verse range)
KNOWN_ACROSTICS = {
    'Psa': [9, 10, 25, 34, 37, 111, 112, 119, 145],
    'Pro': ['31:10-31'],
    'Lam': [1, 2, 3, 4],
    'Nah': ['1:2-8'],
}


def _first_consonant(text: str) -> str | None:
    """Return the first Hebrew consonant in text (strip diacritics first)."""
    for ch in text:
        if ch in _HEB_LETTER_POS:
            return ch
    return None


def detect_acrostic(
    book: str,
    chapter: int,
    start_verse: int,
    end_verse: int,
    *,
    stanza_size: int = 1,
) -> dict:
    """
    Detect an alphabetic acrostic across a verse range.

    Parameters
    ----------
    book, chapter       : book and chapter
    start_verse, end_verse : inclusive verse range
    stanza_size         : verses per stanza (1 for most acrostics; 8 for Ps 119
                          where each stanza of 8 verses starts with the same letter)

    Returns dict with keys:
      hits        : list of (verse, expected_letter, actual_letter, match)
      match_count : int
      total       : int
      pct_match   : float
      is_acrostic : bool (match_count / total >= 0.75)
      pattern     : 'full' | 'partial' | 'none'
    """
    macula = _load_macula()
    book_col = 'book_id' if 'book_id' in macula.columns else 'book'
    verses = list(range(start_verse, end_verse + 1))

    hits = []
    alpha_pos = 0   # index into _HEB_ALPHABET

    for stanza_start_idx in range(0, len(verses), stanza_size):
        stanza_verses = verses[stanza_start_idx: stanza_start_idx + stanza_size]
        expected = _HEB_ALPHABET[alpha_pos] if alpha_pos < 22 else '?'

        for vs in stanza_verses:
            rows = macula[
                (macula[book_col] == book) &
                (macula['chapter'] == chapter) &
                (macula['verse'] == vs)
            ].sort_values('word_num' if 'word_num' in macula.columns else macula.columns[0])

            first_word_text = ''
            if not rows.empty:
                first_word_text = str(rows.iloc[0].get('text', ''))

            actual = _first_consonant(first_word_text)
            match = (actual == expected)
            hits.append({
                'verse': vs,
                'expected': expected,
                'actual': actual or '',
                'first_word': first_word_text,
                'match': match,
            })

        alpha_pos += 1

    match_count = sum(1 for h in hits if h['match'])
    total = len(hits)
    pct = match_count / total if total else 0.0

    if pct >= 0.85:
        pattern = 'full'
    elif pct >= 0.50:
        pattern = 'partial'
    else:
        pattern = 'none'

    return {
        'hits': hits,
        'match_count': match_count,
        'total': total,
        'pct_match': round(pct * 100, 1),
        'is_acrostic': pct >= 0.75,
        'pattern': pattern,
    }


def print_acrostic(
    book: str,
    chapter: int,
    start_verse: int,
    end_verse: int,
    *,
    stanza_size: int = 1,
) -> None:
    """Print an acrostic analysis for a verse range."""
    result = detect_acrostic(book, chapter, start_verse, end_verse,
                             stanza_size=stanza_size)
    ref = f"{book} {chapter}:{start_verse}–{end_verse}"

    print()
    print('═' * 72)
    verdict = f"ACROSTIC ({result['pattern'].upper()})" if result['is_acrostic'] else 'not acrostic'
    print(f"  Acrostic analysis: {ref}  [{verdict}]")
    print(f"  Matches: {result['match_count']}/{result['total']}  "
          f"({result['pct_match']}%)")
    print('─' * 72)
    print(f"  {'Verse':<7} {'Expected':<10} {'Actual':<10} {'First word':<30} {'✓'}")
    print('  ' + '─' * 60)
    for h in result['hits']:
        tick = '✓' if h['match'] else '✗'
        word_preview = h['first_word'][:28]
        print(f"  v{h['verse']:<6} {h['expected']:<10} {h['actual']:<10} "
              f"{word_preview:<30} {tick}")
    print()


def acrostic_known(book: str) -> list[int | str]:
    """Return list of known acrostic chapters/ranges for a book."""
    return KNOWN_ACROSTICS.get(book, [])  # type: ignore[return-value]


# ═══════════════════════════════════════════════════════════════════════════════
# METER / SYLLABLE COUNTING
# ═══════════════════════════════════════════════════════════════════════════════
#
# Hebrew meter is still debated, but the most influential model counts stressed
# syllables per colon (Ley-Sievers stress-counting). The "qinah" meter (3+2)
# is characteristic of laments (qinah = dirge). Psalms of praise often show 3+3.
#
# Syllable counting heuristic (without a full phonological parser):
#   - Each vowel letter (qamets, patah, tsere, etc.) or full vowel point counts
#     as one syllable.
#   - Shewa na (vocal shewa) adds half a syllable; we round conservatively.
#   - Maqeph-joined words count as one stress unit.
#
# This is an approximation. For rigorous metrical analysis, consult a full
# phonological tool. We provide it as a quick heuristic signal.
# ───────────────────────────────────────────────────────────────────────────────

# Hebrew vowel diacritics that each represent one syllable nucleus
_VOWEL_POINTS = {
    0x05B0,  # shewa (vocal when after consonant opening syllable)
    0x05B1,  # hataf segol
    0x05B2,  # hataf patah
    0x05B3,  # hataf qamets
    0x05B4,  # hiriq
    0x05B5,  # tsere
    0x05B6,  # segol
    0x05B7,  # patah
    0x05B8,  # qamets
    0x05B9,  # holam
    0x05BA,  # holam vav
    0x05BB,  # qubuts
    0x05BC,  # dagesh/mappiq (not a vowel — excluded below)
    0x05C7,  # qamets qatan
}
_NON_SYLLABIC = {0x05BC, 0x05BD, 0x05BF, 0x05C1, 0x05C2}  # dagesh, rafe, shin dot


def _count_syllables(text: str) -> int:
    """Estimate syllable count for one Hebrew word token."""
    count = 0
    for c in text:
        cp = ord(c)
        if cp in _VOWEL_POINTS and cp not in _NON_SYLLABIC:
            count += 1
    # Fallback: if no vowel points found (unvocalized text), count consonants/2
    if count == 0:
        consonants = sum(1 for c in text if 'א' <= c <= 'ת')
        count = max(1, consonants // 2)
    return max(1, count)


def _count_stresses(colon_df: pd.DataFrame) -> int:
    """
    Count stressed syllable units in a colon.

    MACULA tokenizes prefixed particles separately (הָ + עִיר = two tokens).
    Classical stress-counting ignores unaccented particles; we approximate by
    counting only content-word tokens (nouns, verbs, adjectives, adverbs).
    Maqeph-joined groups count as one stress unit.
    """
    if colon_df.empty:
        return 0

    has_class = 'class_' in colon_df.columns

    stresses = 0
    rows = colon_df.reset_index(drop=True)
    i = 0
    while i < len(rows):
        row = rows.iloc[i]
        text = str(row.get('text', ''))
        cls = str(row.get('class_', '')) if has_class else ''

        # Maqeph: absorb following tokens into this stress unit
        while '־' in text and i + 1 < len(rows):
            i += 1
            next_row = rows.iloc[i]
            text = text + str(next_row.get('text', ''))
            if not cls:
                cls = str(next_row.get('class_', ''))

        # Count only content-word tokens
        if _is_content_word(cls) or not has_class:
            stresses += 1
        i += 1

    return max(stresses, 0)


def verse_meter(book: str, chapter: int, verse: int) -> dict:
    """
    Estimate the meter pattern for one verse.

    Returns dict with:
      cola          : list of int — stress count per colon
      pattern       : str e.g. '3+2' or '3+3'
      syllables     : list of int — syllable count per colon
      meter_type    : 'qinah(3+2)' | 'balanced(3+3)' | 'other'
    """
    cola = verse_cola(book, chapter, verse)
    stress_counts = [_count_stresses(c) for c in cola]
    syllable_counts = [
        sum(_count_syllables(str(r['text'])) for _, r in c.iterrows())
        for c in cola
    ]

    pattern = '+'.join(str(s) for s in stress_counts)

    if stress_counts == [3, 2] or stress_counts == [3, 2, 2]:
        meter_type = 'qinah(3+2)'
    elif stress_counts == [3, 3]:
        meter_type = 'balanced(3+3)'
    elif stress_counts == [2, 2]:
        meter_type = 'balanced(2+2)'
    elif stress_counts == [4, 4] or stress_counts == [4, 3]:
        meter_type = 'longer(4+x)'
    else:
        meter_type = 'other'

    return {
        'cola': stress_counts,
        'pattern': pattern,
        'syllables': syllable_counts,
        'meter_type': meter_type,
    }


def book_meter_stats(book: str) -> pd.DataFrame:
    """
    Compute meter statistics for every verse in a book.

    Returns DataFrame with columns: chapter, verse, pattern, meter_type,
    stresses_a, stresses_b, syllables_a, syllables_b.
    """
    macula = _load_macula()
    book_col = 'book_id' if 'book_id' in macula.columns else 'book'
    book_rows = macula[macula[book_col] == book]
    refs = (book_rows[['chapter', 'verse']]
            .drop_duplicates()
            .sort_values(['chapter', 'verse'])
            .values.tolist())

    records = []
    for ch, vs in refs:
        m = verse_meter(book, int(ch), int(vs))
        rec = {
            'chapter': ch,
            'verse': vs,
            'pattern': m['pattern'],
            'meter_type': m['meter_type'],
        }
        for idx, (s, syl) in enumerate(zip(m['cola'], m['syllables'])):
            rec[f'stresses_{chr(ord("a")+idx)}'] = s
            rec[f'syllables_{chr(ord("a")+idx)}'] = syl
        records.append(rec)

    return pd.DataFrame(records)


def print_meter_stats(book: str) -> None:
    """Print a summary of meter patterns for a book."""
    df = book_meter_stats(book)
    total = len(df)
    counts = df['meter_type'].value_counts().reset_index()
    counts.columns = ['meter_type', 'count']
    counts['pct'] = (counts['count'] / total * 100).round(1)

    print()
    print('═' * 72)
    print(f"  Meter analysis: {book}  ({total} verses)")
    print('─' * 72)
    for _, row in counts.iterrows():
        bar = '█' * int(row['pct'] / 2)
        print(f"  {str(row['meter_type']):<20} {row['count']:>5}  "
              f"{row['pct']:>5.1f}%  {bar}")
    print()


def print_verse_meter(book: str, chapter: int, verse: int) -> None:
    """Print meter analysis for one verse."""
    m = verse_meter(book, chapter, verse)
    cola_list = verse_cola(book, chapter, verse)

    print()
    print(f"  Meter: {book} {chapter}:{verse}  pattern={m['pattern']}  "
          f"type={m['meter_type']}")
    labels = ['A', 'B', 'C']
    for i, (c_df, stresses, syls) in enumerate(
            zip(cola_list, m['cola'], m['syllables'])):
        words = ' '.join(str(r['text']) for _, r in c_df.iterrows())
        print(f"  Colon {labels[i]}: {stresses} stresses, ~{syls} syllables")
        print(f"           {words}")
    print()
