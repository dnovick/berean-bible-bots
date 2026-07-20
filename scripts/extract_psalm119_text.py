"""Extract Psalm 119 full text from parquet files and save as YAML.

Outputs: data/studies/psalm-119/psalm-119-text.yaml
"""

import re
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
WORDS_PARQUET = REPO_ROOT / "data" / "processed" / "words.parquet"
TRANS_PARQUET = REPO_ROOT / "data" / "processed" / "translations.parquet"
OUT_DIR = REPO_ROOT / "data" / "studies" / "psalm-119"
OUT_YAML = OUT_DIR / "psalm-119-text.yaml"

# ---------------------------------------------------------------------------
# Unicode helpers
# ---------------------------------------------------------------------------
# Cantillation/trope marks only (not niqqud/vowel points)
_CANT_RE = re.compile(r"[֑-ֽ֯]")  # trope + meteg

# All Hebrew diacritics (cantillation + vowel points)
_ALL_DIAC_RE = re.compile(r"[֑-ׇ]")

# Hebrew consonant letters
_HEB_CONS_RE = re.compile(r"[א-ת]")

MAQQEF = "־"   # ־
SOF_PASUQ = "׃"  # ׃
PASEQ = "׀"    # ׀

# ---------------------------------------------------------------------------
# Stanza definitions: (num, letter, name, first_verse, last_verse)
# ---------------------------------------------------------------------------
STANZAS = [
    (1,  "א", "Alef",  1,   8),
    (2,  "ב", "Bet",   9,   16),
    (3,  "ג", "Gimel", 17,  24),
    (4,  "ד", "Dalet", 25,  32),
    (5,  "ה", "He",    33,  40),
    (6,  "ו", "Waw",   41,  48),
    (7,  "ז", "Zayin", 49,  56),
    (8,  "ח", "Ḥet",   57,  64),
    (9,  "ט", "Tet",   65,  72),
    (10, "י", "Yod",   73,  80),
    (11, "כ", "Kaf",   81,  88),
    (12, "ל", "Lamed", 89,  96),
    (13, "מ", "Mem",   97,  104),
    (14, "נ", "Nun",   105, 112),
    (15, "ס", "Samek", 113, 120),
    (16, "ע", "Ayin",  121, 128),
    (17, "פ", "Pe",    129, 136),
    (18, "צ", "Tsade", 137, 144),
    (19, "ק", "Qof",   145, 152),
    (20, "ר", "Resh",  153, 160),
    (21, "שׁ", "Shin",  161, 168),
    (22, "ת", "Taw",   169, 176),
]


# ---------------------------------------------------------------------------
# Word-level cleaning
# ---------------------------------------------------------------------------

def clean_tahot_word(raw: str) -> str:
    """Remove TAHOT-specific separators from a raw word field.

    TAHOT encodes:
      - backslash ``\\`` before maqqef / sof-pasuq as a separator
      - forward slash ``/`` between prefix morphemes and the stem

    After removal the word reads as a continuous Hebrew string.
    """
    return raw.replace("\\", "").replace("/", "").replace(PASEQ, "")


def strip_cantillation(word: str) -> str:
    """Strip trope (cantillation) marks and meteg, preserving niqqud."""
    return _CANT_RE.sub("", word)


def strip_all_diacritics(word: str) -> str:
    """Strip all Hebrew combining diacritics (niqqud + trope)."""
    return _ALL_DIAC_RE.sub("", word)


def consonant_length(word: str) -> int:
    """Count Hebrew consonant letters in *word* (after stripping diacritics)."""
    plain = strip_all_diacritics(word)
    return len(_HEB_CONS_RE.findall(plain))


# ---------------------------------------------------------------------------
# Verse-level reconstruction
# ---------------------------------------------------------------------------

def build_hebrew_text(raw_words: list[str]) -> str:
    """Reconstruct display Hebrew text from a list of TAHOT word strings.

    Words are cleaned and stripped of cantillation marks.  Words ending
    with maqqef are joined to the following word without an intervening
    space (the maqqef already serves as the connector).
    """
    words = [strip_cantillation(clean_tahot_word(w)) for w in raw_words]
    result = words[0] if words else ""
    for word in words[1:]:
        if result.endswith(MAQQEF):
            result += word
        else:
            result += " " + word
    return result


def get_key_words(raw_words: list[str], n: int = 3) -> list[str]:
    """Return up to *n* content words (consonant length ≥ 3), longest first.

    Uses the *display* form (cantillation stripped, vowels kept) as the
    return value, but filters by consonant count of the plain form.
    """
    candidates = []
    for raw in raw_words:
        display = strip_cantillation(clean_tahot_word(raw))
        # Strip sof pasuq from final word before evaluation
        plain = strip_all_diacritics(display).replace(SOF_PASUQ, "")
        clen = len(_HEB_CONS_RE.findall(plain))
        if clen >= 3:
            # Use display form (niqqud intact, sof pasuq stripped)
            candidates.append((clen, display.replace(SOF_PASUQ, "")))

    # Sort by consonant length descending, deduplicate, take top n
    candidates.sort(key=lambda x: -x[0])
    seen: set[str] = set()
    result = []
    for _, w in candidates:
        w = w.rstrip(MAQQEF)  # strip trailing maqqef connector
        if w not in seen:
            seen.add(w)
            result.append(w)
        if len(result) == n:
            break
    return result


def get_first_word(raw_words: list[str]) -> str:
    """Return the display form of the first word (no sof pasuq)."""
    w = strip_cantillation(clean_tahot_word(raw_words[0]))
    return w.replace(SOF_PASUQ, "")


def get_last_word(raw_words: list[str]) -> str:
    """Return the display form of the last word (no sof pasuq or maqqef)."""
    w = strip_cantillation(clean_tahot_word(raw_words[-1]))
    return w.replace(SOF_PASUQ, "").rstrip(MAQQEF)


# ---------------------------------------------------------------------------
# YAML serialisation helpers
# ---------------------------------------------------------------------------

class _LiteralStr(str):
    pass


def _literal_representer(dumper: yaml.Dumper, data: _LiteralStr) -> yaml.ScalarNode:
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


class _OrderedDumper(yaml.Dumper):
    pass


_OrderedDumper.add_representer(_LiteralStr, _literal_representer)


def _dump(data: object) -> str:
    return yaml.dump(
        data,
        Dumper=_OrderedDumper,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=120,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("Loading parquet files …")
    words_df = pd.read_parquet(WORDS_PARQUET)
    trans_df = pd.read_parquet(TRANS_PARQUET)

    # Filter to Psalm 119
    psa119_words = (
        words_df[(words_df["book_id"] == "Psa") & (words_df["chapter"] == 119)]
        .copy()
        .sort_values(["verse", "word_num"])
    )
    psa119_kjv = trans_df[
        (trans_df["book_id"] == "Psa")
        & (trans_df["chapter"] == 119)
        & (trans_df["translation"] == "KJV")
    ].set_index("verse")

    print(f"  Hebrew words: {len(psa119_words)}")
    print(f"  KJV verses  : {len(psa119_kjv)}")

    # Group words by verse
    verse_words: dict[int, list[str]] = {}
    for verse, grp in psa119_words.groupby("verse"):
        verse_words[int(verse)] = grp.sort_values("word_num")["word"].tolist()

    # Build stanza list
    stanzas = []
    for stanza_num, letter, name, v_start, v_end in STANZAS:
        verses = []
        for abs_num in range(v_start, v_end + 1):
            local_num = abs_num - v_start + 1
            raw_ws = verse_words.get(abs_num, [])
            if not raw_ws:
                print(f"  WARNING: no words found for verse {abs_num}", file=sys.stderr)
                continue

            hebrew = build_hebrew_text(raw_ws)
            kjv_text = ""
            if abs_num in psa119_kjv.index:
                kjv_text = str(psa119_kjv.loc[abs_num, "text"])
            else:
                print(f"  WARNING: no KJV text for verse {abs_num}", file=sys.stderr)

            verses.append({
                "num": local_num,
                "abs_num": abs_num,
                "hebrew": hebrew,
                "kjv": kjv_text,
                "first_word": get_first_word(raw_ws),
                "key_words": get_key_words(raw_ws, n=3),
                "line_endings": [get_last_word(raw_ws)],
            })

        stanzas.append({
            "num": stanza_num,
            "letter": letter,
            "name": name,
            "verses": verses,
        })

    document = {"stanzas": stanzas}

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_YAML.write_text(_dump(document), encoding="utf-8")
    print(f"\nWrote {OUT_YAML}")

    # Quick sanity-print of first 3 verses
    print("\n--- First 3 verses (stanza 1) ---")
    first_stanza: dict[str, Any] = stanzas[0]
    for v in first_stanza["verses"][:3]:
        print(f"  v{v['abs_num']}: {v['hebrew']}")
        print(f"       KJV: {v['kjv']}")
        print(f"       first_word: {v['first_word']}")
        print(f"       key_words: {v['key_words']}")
        print(f"       line_endings: {v['line_endings']}")
        print()


if __name__ == "__main__":
    main()
