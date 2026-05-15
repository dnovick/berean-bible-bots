"""Parse STEPBible TAHOT and TAGNT TSV files into pandas DataFrames."""

import re
from pathlib import Path
import pandas as pd
from .morphology import decode_hebrew, decode_greek, extract_greek_grammar

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DATA_DIR = _REPO_ROOT / "stepbible-data" / "Translators Amalgamated OT+NT"

_TAHOT_FILES = [
    "TAHOT Gen-Deu - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt",
    "TAHOT Jos-Est - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt",
    "TAHOT Job-Sng - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt",
    "TAHOT Isa-Mal - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt",
]

_TAGNT_FILES = [
    "TAGNT Mat-Jhn - Translators Amalgamated Greek NT - STEPBible.org CC-BY.txt",
    "TAGNT Act-Rev - Translators Amalgamated Greek NT - STEPBible.org CC-BY.txt",
]

# Regex to match a reference like Gen.1.1#01=L, Psa.8.0(8.1)#01=L, or Mat.1.1#01=NKO
# The optional (?:\(\d+\.\d+\)) handles Psalm lines with parenthetical Hebrew verse numbers
_REF_RE = re.compile(r'^([1-3]?[A-Za-z]+)\.(\d+)\.(\d+)(?:\(\d+\.\d+\))?#(\d+)')


def _parse_ref(ref: str) -> tuple[str, int, int, int] | None:
    """Return (book_id, chapter, verse, word_num) or None."""
    m = _REF_RE.match(ref)
    if not m:
        return None
    return m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))


def _is_data_line(line: str) -> bool:
    """True if the line looks like a word-data row (starts with a ref)."""
    return bool(_REF_RE.match(line))


def load_tahot(data_dir: Path = _DATA_DIR) -> pd.DataFrame:
    """Load and parse all TAHOT files into a single DataFrame."""
    rows = []
    for fname in _TAHOT_FILES:
        path = data_dir / fname
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not _is_data_line(line):
                    continue
                cols = line.split("\t")
                # Columns (0-indexed):
                # 0: Ref  1: Hebrew  2: Transliteration  3: Translation
                # 4: dStrongs  5: Grammar  6: Meaning Variants  7: Spelling Variants
                # 8: Root dStrong  9: Alt Strongs  10: Conjoin  11: Expanded
                if len(cols) < 6:
                    continue
                ref_cell = cols[0].strip()
                parsed = _parse_ref(ref_cell)
                if parsed is None:
                    continue
                book_id, chapter, verse, word_num = parsed

                word = cols[1].strip() if len(cols) > 1 else ""
                transliteration = cols[2].strip() if len(cols) > 2 else ""
                translation = cols[3].strip() if len(cols) > 3 else ""
                dstrongs = cols[4].strip() if len(cols) > 4 else ""
                morph_code = cols[5].strip() if len(cols) > 5 else ""

                morph = decode_hebrew(morph_code)

                rows.append({
                    "source": "TAHOT",
                    "book_id": book_id,
                    "chapter": chapter,
                    "verse": verse,
                    "word_num": word_num,
                    "word": word,
                    "transliteration": transliteration,
                    "translation": translation,
                    "strongs": dstrongs,
                    "morph_code": morph_code,
                    "language": morph.get("language", "Hebrew"),
                    "part_of_speech": morph.get("part_of_speech", ""),
                    "stem": morph.get("stem", ""),
                    "conjugation": morph.get("conjugation", ""),
                    "person": morph.get("person", ""),
                    "gender": morph.get("gender", ""),
                    "number": morph.get("number", ""),
                    "state": morph.get("state", ""),
                    "noun_type": morph.get("noun_type", ""),
                    "prefixes": morph.get("prefixes", ""),
                    # Greek-only fields (empty for OT)
                    "tense": "",
                    "voice": "",
                    "mood": "",
                    "case_": "",
                })
    return pd.DataFrame(rows)


def load_tagnt(data_dir: Path = _DATA_DIR) -> pd.DataFrame:
    """Load and parse all TAGNT files into a single DataFrame."""
    rows = []
    for fname in _TAGNT_FILES:
        path = data_dir / fname
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not _is_data_line(line):
                    continue
                cols = line.split("\t")
                # Columns (0-indexed):
                # 0: Word & Type  1: Greek  2: English  3: dStrongs=Grammar
                # 4: Dict form=Gloss  5: Editions  6: Meaning variants
                # 7: Spelling variants  8: Spanish  9: Sub-meaning
                # 10: Conjoin word  11: sStrong+Instance  12: Alt Strongs
                if len(cols) < 4:
                    continue
                ref_cell = cols[0].strip()
                parsed = _parse_ref(ref_cell)
                if parsed is None:
                    continue
                book_id, chapter, verse, word_num = parsed

                word = cols[1].strip() if len(cols) > 1 else ""
                # strip transliteration in parens
                word = re.sub(r'\s*\([^)]+\)', '', word).strip()
                translation = cols[2].strip() if len(cols) > 2 else ""
                dstrongs_grammar = cols[3].strip() if len(cols) > 3 else ""
                dict_gloss = cols[4].strip() if len(cols) > 4 else ""

                strongs, grammar_code = extract_greek_grammar(dstrongs_grammar)
                morph = decode_greek(grammar_code)

                gloss_parts = dict_gloss.split("=", 1)
                gloss_parts[0].strip() if gloss_parts else ""
                gloss_parts[1].strip() if len(gloss_parts) > 1 else ""

                rows.append({
                    "source": "TAGNT",
                    "book_id": book_id,
                    "chapter": chapter,
                    "verse": verse,
                    "word_num": word_num,
                    "word": word,
                    "transliteration": "",
                    "translation": translation,
                    "strongs": strongs,
                    "morph_code": grammar_code,
                    "language": "Greek",
                    "part_of_speech": morph.get("part_of_speech", ""),
                    "stem": "",
                    "conjugation": "",
                    "person": morph.get("person", ""),
                    "gender": morph.get("gender", ""),
                    "number": morph.get("number", ""),
                    "state": "",
                    "noun_type": "",
                    "prefixes": "",
                    "tense": morph.get("tense", ""),
                    "voice": morph.get("voice", ""),
                    "mood": morph.get("mood", ""),
                    "case_": morph.get("case_", ""),
                })
    return pd.DataFrame(rows)


def load_all(data_dir: Path = _DATA_DIR) -> pd.DataFrame:
    """Load TAHOT + TAGNT and return a single combined DataFrame."""
    ot = load_tahot(data_dir)
    nt = load_tagnt(data_dir)
    return pd.concat([ot, nt], ignore_index=True)
