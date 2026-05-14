"""
Load English/Latin translation texts from scrollmapper bible_databases JSON files.
Stores verse-level rows in the `translations` SQLite table and a separate Parquet file.
"""

from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCROLL_ROOT = _REPO_ROOT / "scrollmapper-data" / "sources"

_SOURCES = {
    "KJV":            _SCROLL_ROOT / "en" / "KJV" / "KJV.json",
    "VulgClementine": _SCROLL_ROOT / "la" / "VulgClementine" / "VulgClementine.json",
    "Peshitta":       _SCROLL_ROOT / "syr" / "Peshitta" / "Peshitta.json",
}

# scrollmapper uses full English book names; map them to our book_id codes
_NAME_TO_ID: dict[str, str] = {
    "Genesis": "Gen", "Exodus": "Exo", "Leviticus": "Lev", "Numbers": "Num",
    "Deuteronomy": "Deu", "Joshua": "Jos", "Judges": "Jdg", "Ruth": "Rut",
    "1 Samuel": "1Sa", "2 Samuel": "2Sa", "1 Kings": "1Ki", "2 Kings": "2Ki",
    "1 Chronicles": "1Ch", "2 Chronicles": "2Ch", "Ezra": "Ezr",
    "Nehemiah": "Neh", "Esther": "Est", "Job": "Job", "Psalms": "Psa",
    "Proverbs": "Pro", "Ecclesiastes": "Ecc", "Song of Solomon": "Sng",
    "Isaiah": "Isa", "Jeremiah": "Jer", "Lamentations": "Lam",
    "Ezekiel": "Ezk", "Daniel": "Dan", "Hosea": "Hos", "Joel": "Jol",
    "Amos": "Amo", "Obadiah": "Oba", "Jonah": "Jon", "Micah": "Mic",
    "Nahum": "Nah", "Habakkuk": "Hab", "Zephaniah": "Zep", "Haggai": "Hag",
    "Zechariah": "Zec", "Malachi": "Mal",
    "Matthew": "Mat", "Mark": "Mrk", "Luke": "Luk", "John": "Jhn",
    "Acts": "Act", "Romans": "Rom", "1 Corinthians": "1Co",
    "2 Corinthians": "2Co", "Galatians": "Gal", "Ephesians": "Eph",
    "Philippians": "Php", "Colossians": "Col", "1 Thessalonians": "1Th",
    "2 Thessalonians": "2Th", "1 Timothy": "1Ti", "2 Timothy": "2Ti",
    "Titus": "Tit", "Philemon": "Phm", "Hebrews": "Heb", "James": "Jas",
    "1 Peter": "1Pe", "2 Peter": "2Pe", "1 John": "1Jn", "2 John": "2Jn",
    "3 John": "3Jn", "Jude": "Jud", "Revelation": "Rev",
    # Peshitta scrollmapper uses Roman numerals for NT books
    "I Corinthians": "1Co", "II Corinthians": "2Co",
    "I Thessalonians": "1Th", "II Thessalonians": "2Th",
    "I Timothy": "1Ti", "II Timothy": "2Ti",
    "I Peter": "1Pe", "II Peter": "2Pe",
    "I John": "1Jn", "II John": "2Jn", "III John": "3Jn",
    "Revelation of John": "Rev",
}


def _load_json(path: Path, translation: str, language: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    rows = []
    for book in data["books"]:
        book_name = book["name"]
        book_id = _NAME_TO_ID.get(book_name)
        if book_id is None:
            # Apocrypha / deuterocanonical books not in our canonical list — skip
            continue
        for chapter in book["chapters"]:
            ch_num = int(chapter["chapter"])
            for verse in chapter["verses"]:
                text = verse["text"].strip()
                if not text:
                    continue
                rows.append({
                    "translation": translation,
                    "language": language,
                    "book_id": book_id,
                    "chapter": ch_num,
                    "verse": int(verse["verse"]),
                    "text": text,
                })
    return rows


def load_translations() -> pd.DataFrame:
    """Load KJV, Vulgate Clementine, and Peshitta NT into a single DataFrame."""
    all_rows: list[dict] = []
    configs = [
        ("KJV", "English"),
        ("VulgClementine", "Latin"),
        ("Peshitta", "Syriac"),
    ]
    for key, lang in configs:
        path = _SOURCES[key]
        if not path.exists():
            print(f"  WARNING: {path} not found, skipping {key}")
            continue
        rows = _load_json(path, key, lang)
        all_rows.extend(rows)
        print(f"  {key}: {len(rows):,} verses")
    return pd.DataFrame(all_rows)
