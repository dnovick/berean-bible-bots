"""
Speaker attribution for NT direct speech.

Combines two complementary strategies:
  1. Verse allowlists — hard-coded verse sets for titles where the self-
     referential instances are known and invariant (e.g. the 7 Johannine
     I AM predicate sayings).
  2. MACULA subjref — speech verbs (λέγω, φημί, …) whose subjref field
     links to a Jesus token (Strong 2424), giving a verse-level set of
     "Jesus-speaking" verses detected from the syntax tree.

Strategy 2 is built once and cached as a frozenset for the session.

Public API
──────────
is_jesus_speaking(book, chapter, verse) → bool
jesus_speaking_verse_set(books)         → frozenset of (book, ch, vs)

The christological_titles module uses both:
  • Allowlist titles bypass the strategy-2 filter (confidence='high' with
    an explicit self_ref_verses list).
  • For medium/low titles, filter the co-occurrence results to only verses
    where is_jesus_speaking() is True.
"""

from __future__ import annotations

_SPEAKING_CACHE: frozenset | None = None


# ── Curated verse allowlists ──────────────────────────────────────────────────
#
# Format: (book_id, chapter, verse)
# These are the specific verse references for each high-confidence title
# where Jesus is definitively the speaker.  Source: standard Gospel
# scholarship (UBS, NA28 apparatus, standard commentaries).

ALLOWLIST_VERSES: dict[str, frozenset[tuple[str, int, int]]] = {

    # Son of Man — every Gospel instance is Jesus speaking of himself.
    # Acts 7:56 (Stephen's vision) and Rev 1:13, 14:14 are not self-
    # reference, so excluded.
    'Son of Man': frozenset([
        ('Mat',  8, 20), ('Mat',  9,  6), ('Mat', 10, 23), ('Mat', 11, 19),
        ('Mat', 12,  8), ('Mat', 12, 32), ('Mat', 12, 40), ('Mat', 13, 37),
        ('Mat', 13, 41), ('Mat', 16, 13), ('Mat', 16, 27), ('Mat', 16, 28),
        ('Mat', 17,  9), ('Mat', 17, 12), ('Mat', 17, 22), ('Mat', 19, 28),
        ('Mat', 20, 18), ('Mat', 20, 28), ('Mat', 24, 27), ('Mat', 24, 30),
        ('Mat', 24, 37), ('Mat', 24, 39), ('Mat', 24, 44), ('Mat', 25, 31),
        ('Mat', 26, 24), ('Mat', 26, 45), ('Mat', 26, 64),
        ('Mrk',  2, 10), ('Mrk',  2, 28), ('Mrk',  8, 31), ('Mrk',  8, 38),
        ('Mrk',  9,  9), ('Mrk',  9, 12), ('Mrk',  9, 31), ('Mrk', 10, 33),
        ('Mrk', 10, 45), ('Mrk', 13, 26), ('Mrk', 14, 21), ('Mrk', 14, 41),
        ('Mrk', 14, 62),
        ('Luk',  5, 24), ('Luk',  6,  5), ('Luk',  6, 22), ('Luk',  7, 34),
        ('Luk',  9, 22), ('Luk',  9, 26), ('Luk',  9, 44), ('Luk',  9, 58),
        ('Luk', 11, 30), ('Luk', 12,  8), ('Luk', 12, 10), ('Luk', 12, 40),
        ('Luk', 17, 22), ('Luk', 17, 24), ('Luk', 17, 26), ('Luk', 17, 30),
        ('Luk', 18,  8), ('Luk', 18, 31), ('Luk', 19, 10), ('Luk', 21, 27),
        ('Luk', 21, 36), ('Luk', 22, 22), ('Luk', 22, 48), ('Luk', 22, 69),
        ('Jhn',  1, 51), ('Jhn',  3, 13), ('Jhn',  3, 14), ('Jhn',  5, 27),
        ('Jhn',  6, 27), ('Jhn',  6, 53), ('Jhn',  6, 62), ('Jhn',  8, 28),
        ('Jhn',  9, 35), ('Jhn', 12, 23), ('Jhn', 12, 34), ('Jhn', 13, 31),
    ]),

    # Johannine I AM predicate sayings — all are Jesus speaking.
    'I AM — Bread of Life': frozenset([
        ('Jhn', 6, 35), ('Jhn', 6, 41), ('Jhn', 6, 48), ('Jhn', 6, 51),
    ]),
    'I AM — Light of the World': frozenset([
        ('Jhn', 8, 12),
    ]),
    'I AM — the Door / Gate': frozenset([
        ('Jhn', 10, 7), ('Jhn', 10, 9),
    ]),
    'I AM — the Good Shepherd': frozenset([
        ('Jhn', 10, 11), ('Jhn', 10, 14),
    ]),
    'I AM — the Resurrection': frozenset([
        ('Jhn', 11, 25),
    ]),
    'I AM — the Way': frozenset([
        ('Jhn', 14, 6),
    ]),
    'I AM — the True Vine': frozenset([
        ('Jhn', 15, 1), ('Jhn', 15, 5),
    ]),

    # Bridegroom — Synoptic instances where Jesus speaks of himself as
    # the bridegroom.  Jhn 3:29 (John the Baptist speaking) excluded.
    'Bridegroom': frozenset([
        ('Mat', 9, 15), ('Mrk', 2, 19), ('Mrk', 2, 20),
        ('Luk', 5, 34), ('Luk', 5, 35),
    ]),
}


# ── MACULA subjref-based detection ────────────────────────────────────────────

def jesus_speaking_verse_set(
    books: list[str] | None = None,
    *,
    force_rebuild: bool = False,
) -> frozenset[tuple[str, int, int]]:
    """
    Return a frozenset of (book_id, chapter, verse) tuples where a
    speech-introducing verb has Jesus (Strong 2424) as its grammatical
    subject, as determined by MACULA's subjref links.

    Cached after first call; pass force_rebuild=True to re-derive.
    """
    global _SPEAKING_CACHE
    if _SPEAKING_CACHE is not None and not force_rebuild and books is None:
        return _SPEAKING_CACHE

    from ..core.syntax import jesus_speaking_verses
    result = frozenset(jesus_speaking_verses(books=books))

    if books is None:
        _SPEAKING_CACHE = result
    return result


def is_jesus_speaking(book: str, chapter: int, verse: int,
                      title: str | None = None) -> bool:
    """
    Return True if Jesus is the speaker in the given verse.

    Checks in order:
      1. If title is given and has an allowlist, use that (exact and fast).
      2. Otherwise fall back to MACULA subjref detection.
    """
    if title and title in ALLOWLIST_VERSES:
        return (book, chapter, verse) in ALLOWLIST_VERSES[title]

    speaking = jesus_speaking_verse_set()
    return (book, chapter, verse) in speaking


def filter_to_jesus_speech(
    verses: list[tuple[str, int, int]],
    title: str | None = None,
) -> list[tuple[str, int, int]]:
    """
    From a list of (book, chapter, verse) tuples, return only those where
    Jesus is speaking.  Uses allowlist if available, else MACULA subjref.
    """
    if title and title in ALLOWLIST_VERSES:
        allowed = ALLOWLIST_VERSES[title]
        return [v for v in verses if v in allowed]

    speaking = jesus_speaking_verse_set()
    return [v for v in verses if v in speaking]
