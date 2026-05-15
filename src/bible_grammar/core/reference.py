"""Book reference metadata: canonical order, names, testament, chapter counts."""

BOOKS = [
    # (book_id, full_name, testament, canonical_order, chapter_count)
    ("Gen", "Genesis", "OT", 1, 50),
    ("Exo", "Exodus", "OT", 2, 40),
    ("Lev", "Leviticus", "OT", 3, 27),
    ("Num", "Numbers", "OT", 4, 36),
    ("Deu", "Deuteronomy", "OT", 5, 34),
    ("Jos", "Joshua", "OT", 6, 24),
    ("Jdg", "Judges", "OT", 7, 21),
    ("Rut", "Ruth", "OT", 8, 4),
    ("1Sa", "1 Samuel", "OT", 9, 31),
    ("2Sa", "2 Samuel", "OT", 10, 24),
    ("1Ki", "1 Kings", "OT", 11, 22),
    ("2Ki", "2 Kings", "OT", 12, 25),
    ("1Ch", "1 Chronicles", "OT", 13, 29),
    ("2Ch", "2 Chronicles", "OT", 14, 36),
    ("Ezr", "Ezra", "OT", 15, 10),
    ("Neh", "Nehemiah", "OT", 16, 13),
    ("Est", "Esther", "OT", 17, 10),
    ("Job", "Job", "OT", 18, 42),
    ("Psa", "Psalms", "OT", 19, 150),
    ("Pro", "Proverbs", "OT", 20, 31),
    ("Ecc", "Ecclesiastes", "OT", 21, 12),
    ("Sng", "Song of Songs", "OT", 22, 8),
    ("Isa", "Isaiah", "OT", 23, 66),
    ("Jer", "Jeremiah", "OT", 24, 52),
    ("Lam", "Lamentations", "OT", 25, 5),
    ("Ezk", "Ezekiel", "OT", 26, 48),
    ("Dan", "Daniel", "OT", 27, 12),
    ("Hos", "Hosea", "OT", 28, 14),
    ("Jol", "Joel", "OT", 29, 3),
    ("Amo", "Amos", "OT", 30, 9),
    ("Oba", "Obadiah", "OT", 31, 1),
    ("Jon", "Jonah", "OT", 32, 4),
    ("Mic", "Micah", "OT", 33, 7),
    ("Nah", "Nahum", "OT", 34, 3),
    ("Hab", "Habakkuk", "OT", 35, 3),
    ("Zep", "Zephaniah", "OT", 36, 3),
    ("Hag", "Haggai", "OT", 37, 2),
    ("Zec", "Zechariah", "OT", 38, 14),
    ("Mal", "Malachi", "OT", 39, 4),
    ("Mat", "Matthew", "NT", 40, 28),
    ("Mrk", "Mark", "NT", 41, 16),
    ("Luk", "Luke", "NT", 42, 24),
    ("Jhn", "John", "NT", 43, 21),
    ("Act", "Acts", "NT", 44, 28),
    ("Rom", "Romans", "NT", 45, 16),
    ("1Co", "1 Corinthians", "NT", 46, 16),
    ("2Co", "2 Corinthians", "NT", 47, 13),
    ("Gal", "Galatians", "NT", 48, 6),
    ("Eph", "Ephesians", "NT", 49, 6),
    ("Php", "Philippians", "NT", 50, 4),
    ("Col", "Colossians", "NT", 51, 4),
    ("1Th", "1 Thessalonians", "NT", 52, 5),
    ("2Th", "2 Thessalonians", "NT", 53, 3),
    ("1Ti", "1 Timothy", "NT", 54, 6),
    ("2Ti", "2 Timothy", "NT", 55, 4),
    ("Tit", "Titus", "NT", 56, 3),
    ("Phm", "Philemon", "NT", 57, 1),
    ("Heb", "Hebrews", "NT", 58, 13),
    ("Jas", "James", "NT", 59, 5),
    ("1Pe", "1 Peter", "NT", 60, 5),
    ("2Pe", "2 Peter", "NT", 61, 3),
    ("1Jn", "1 John", "NT", 62, 5),
    ("2Jn", "2 John", "NT", 63, 1),
    ("3Jn", "3 John", "NT", 64, 1),
    ("Jud", "Jude", "NT", 65, 1),
    ("Rev", "Revelation", "NT", 66, 22),
]

_by_id = {b[0]: b for b in BOOKS}
_by_name = {b[1].lower(): b for b in BOOKS}

PAULINE = {"Rom", "1Co", "2Co", "Gal", "Eph", "Php", "Col",
           "1Th", "2Th", "1Ti", "2Ti", "Tit", "Phm"}
TORAH = {"Gen", "Exo", "Lev", "Num", "Deu"}
PROPHETS = {"Isa", "Jer", "Lam", "Ezk", "Dan", "Hos", "Jol", "Amo",
            "Oba", "Jon", "Mic", "Nah", "Hab", "Zep", "Hag", "Zec", "Mal"}
WRITINGS = {"Job", "Psa", "Pro", "Ecc", "Sng", "Rut", "Est",
            "Ezr", "Neh", "1Ch", "2Ch"}
GOSPELS = {"Mat", "Mrk", "Luk", "Jhn"}


_GROUPS: dict[str, set[str]] = {
    'torah': TORAH,
    'pentateuch': TORAH,
    'prophets': PROPHETS,
    'writings': WRITINGS,
    'gospels': GOSPELS,
    'pauline': PAULINE,
}


def book_ids_for_group(group: str) -> list[str]:
    """Return book IDs in canonical order for a named group (e.g. 'torah', 'pauline')."""
    key = group.lower()
    if key not in _GROUPS:
        raise ValueError(
            f"Unknown book_group {group!r}. Valid: {sorted(_GROUPS)}"
        )
    ids = _GROUPS[key]
    return [b[0] for b in BOOKS if b[0] in ids]


def book_info(book_id: str) -> dict:
    row = _by_id.get(book_id)
    if row is None:
        raise KeyError(f"Unknown book id: {book_id!r}")
    return {"book_id": row[0], "name": row[1], "testament": row[2],
            "canonical_order": row[3], "chapter_count": row[4]}


def all_book_ids(testament: str | None = None) -> list[str]:
    rows = BOOKS if testament is None else [b for b in BOOKS if b[2] == testament]
    return [b[0] for b in rows]
