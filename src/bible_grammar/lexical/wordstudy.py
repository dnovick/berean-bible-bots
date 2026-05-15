"""
Word study tool: one-stop profile for any Hebrew or Greek lemma.

Combines lexicon definitions (TBESH/TBESG), corpus statistics,
morphological form inventory, LXX translation equivalents (for Hebrew),
and example verses into a single structured result.

Usage
-----
from bible_grammar.lexical.wordstudy import word_study, print_word_study

# Hebrew word by Strong's
word_study('H1254')     # בָּרָא "to create"

# Greek word by Strong's
word_study('G4160')     # ποιέω "to do/make"

# Print formatted output
print_word_study('H1254')
print_word_study('G4160')
"""

from __future__ import annotations
import re
import pandas as pd
from ..core import db as _db
from ..core.reference import BOOKS, book_info
from .lexicon import lookup as _lex_lookup, lemma_index as _lemma_index

_BOOK_ORDER = {b[0]: b[3] for b in BOOKS}


def _words() -> pd.DataFrame:
    return _db.load()


def _lxx() -> pd.DataFrame:
    return _db.load_lxx()


def _translations() -> pd.DataFrame:
    return _db.load_translations()


def _build_lemma_index() -> tuple[dict, dict]:
    """Return (heb_lemma→strongs, grk_lemma→strongs) — delegates to lexicon module."""
    return _lemma_index('H'), _lemma_index('G')


def resolve_strongs(term: str) -> str | None:
    """
    Resolve a term to a Strong's number.

    Accepts:
      - A Strong's number directly: 'H1285', 'G3056'
      - A Hebrew lemma (with or without vowel points): 'שָׁלוֹם', 'שלום'
      - A Greek lemma: 'λόγος', 'εἰρήνη'

    Returns the Strong's number string, or None if not found.
    """
    import unicodedata
    term = term.strip()

    # Direct strongs number
    if re.match(r'^[HG]\d', term.upper()):
        return term.upper()

    nfc = unicodedata.normalize("NFC", term)
    heb_idx, grk_idx = _build_lemma_index()

    # Try Hebrew (with vowels, then without)
    result = heb_idx.get(nfc)
    if result:
        return result
    consonants = re.sub(r'[֑-ׇ]', '', nfc)
    result = heb_idx.get(consonants)
    if result:
        return result

    # Try Greek (case-insensitive)
    result = grk_idx.get(nfc.lower())
    if result:
        return result

    return None


def _lookup_lex(strongs: str) -> dict | None:
    """Look up a Strong's number — delegates to lexicon module."""
    clean = strongs.strip("{}").upper()
    entry = _lex_lookup(clean)
    if not entry:
        # Try zero-padded form
        m = re.match(r'^([HG])(\d+)([A-Z]?)$', clean)
        if m:
            padded = f"{m.group(1)}{int(m.group(2)):04d}{m.group(3)}"
            entry = _lex_lookup(padded)
    return entry or None


def _kjv_verse(book_id: str, chapter: int, verse: int) -> str:
    tr = _translations()
    row = tr[
        (tr["book_id"] == book_id) &
        (tr["chapter"] == chapter) &
        (tr["verse"] == verse) &
        (tr["translation"] == "KJV")
    ]
    return row.iloc[0]["text"] if not row.empty else ""


def word_study(strongs: str, *, example_verses: int = 5) -> dict:
    """
    Complete word study for a Strong's number.

    Parameters
    ----------
    strongs        : e.g. 'H1254', 'H1254A', 'G4160', 'G4160G'
    example_verses : Number of example verses to include (default 5)

    Returns a dict with keys:
      strongs, lemma, translit, gloss, pos_code, definition,
      total_occurrences, by_book (DataFrame),
      morphological_forms (DataFrame),
      translation_equivalents (OT Hebrew only, DataFrame),
      nt_usage (OT Hebrew only — NT occurrences if any),
      lxx_usage (OT Hebrew only — LXX Greek equivalent stats),
      examples (list of {reference, word, context} dicts)
    """
    clean = strongs.strip("{}").upper()
    is_hebrew = clean.startswith("H")

    # --- Lexicon ---
    lex = _lookup_lex(clean)
    if lex is None:
        lex = {"strongs": clean, "lemma": "", "translit": "",
               "gloss": "(not found in lexicon)", "definition": "", "pos_code": ""}

    result = {
        "strongs": clean,
        "lemma": lex["lemma"],
        "translit": lex["translit"],
        "gloss": lex["gloss"],
        "pos_code": lex["pos_code"],
        "definition": lex["definition"],
    }

    # --- Corpus occurrences ---
    df = _words()
    source = "TAHOT" if is_hebrew else "TAGNT"
    corpus = df[df["source"] == source]

    # Match on strongs column using a regex that anchors the number to avoid
    # false positives (e.g. H157 matching H1571, H1573 etc.)
    # Hebrew strongs are wrapped in curly braces: {H1254A}, H9003/{H1254A}
    # Greek strongs are plain: G4160, G4160G
    m_clean = re.match(r'^([HG])0*(\d+)([A-Z]?)$', clean)
    if m_clean:
        pfx, num, suf = m_clean.groups()
        # Match the number with optional leading zeros and optional trailing variant letter
        pat = rf'\{{{pfx}0*{num}[A-Z]?\}}' if is_hebrew else rf'\b{pfx}0*{num}[A-Z]?\b'
    else:
        pat = re.escape(clean)
    mask = corpus["strongs"].str.upper().str.contains(pat, regex=True, na=False)
    re.sub(r'[A-Z]$', '', clean)

    hits = corpus[mask].copy()
    result["total_occurrences"] = len(hits)

    if hits.empty:
        result.update({
            "by_book": pd.DataFrame(), "morphological_forms": pd.DataFrame(),
            "translation_equivalents": pd.DataFrame(), "examples": [],
        })
        return result

    # --- By book ---
    by_book = (
        hits.groupby("book_id").size()
        .reset_index(name="count")
        .assign(book_name=lambda d: d["book_id"].apply(
            lambda b: book_info(b)["name"] if b in {bk[0] for bk in BOOKS} else b))
        .assign(_order=lambda d: d["book_id"].map(_BOOK_ORDER).fillna(99))
        .sort_values("_order")
        .drop(columns="_order")
    )
    total = by_book["count"].sum()
    by_book["pct"] = (by_book["count"] / total * 100).round(1)
    result["by_book"] = by_book[["book_id", "book_name", "count", "pct"]].reset_index(drop=True)

    # --- Morphological forms ---
    if is_hebrew:
        form_cols = ["stem", "conjugation", "part_of_speech", "state"]
    else:
        form_cols = ["tense", "voice", "mood", "part_of_speech"]
    form_cols = [c for c in form_cols if c in hits.columns]

    morph = (
        hits.groupby(form_cols, dropna=False)
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    morph["pct"] = (morph["count"] / len(hits) * 100).round(1)
    result["morphological_forms"] = morph.reset_index(drop=True)

    # --- Translation equivalents (Hebrew OT → LXX) ---
    if is_hebrew:
        # Prefer word-level IBM Model 1 alignment; fall back to verse-level
        te = pd.DataFrame()
        try:
            from ..core.ibm_align import translation_equivalents_w
            te = translation_equivalents_w(heb_strongs=clean, top_n=15, min_count=1)
        except Exception:
            pass
        if te.empty:
            try:
                from ..core.alignment import translation_equivalents
                te = translation_equivalents(heb_strongs=clean, top_n=15, min_count=1)
            except Exception:
                pass
        result["translation_equivalents"] = te

        # NT usage of the primary LXX equivalent (OT → LXX → NT trajectory)
        nt_equiv: list[dict] = []
        if not te.empty:
            nt_df = df[df["source"] == "TAGNT"]
            for _, te_row in te.head(3).iterrows():
                g_strongs = te_row.get("lxx_strongs", "")
                if not g_strongs or g_strongs == "__NULL__":
                    continue
                # Strip trailing letter variant suffix (e.g. 'G1234A' → 'G1234')
                g_base = re.sub(r'[A-Z]$', '', g_strongs.upper())
                # Use exact match to avoid 'G25' matching 'G250', 'G251', etc.
                nt_hits = nt_df[nt_df["strongs"].str.upper() == g_base]
                if nt_hits.empty:
                    # Fallback: also try zero-padded variants (TAGNT may use G0025 or G25)
                    try:
                        num = int(g_base.lstrip('G'))
                        alt = f"G{num:04d}"
                        alt2 = f"G{num}"
                        nt_hits = nt_df[nt_df["strongs"].str.upper().isin({alt, alt2})]
                    except ValueError:
                        pass
                if nt_hits.empty:
                    continue
                nt_by_book = (
                    nt_hits.groupby("book_id").size()
                    .reset_index(name="count")
                    .assign(_order=lambda d: d["book_id"].map(_BOOK_ORDER).fillna(99))
                    .sort_values("_order").drop(columns="_order")
                )
                g_lemma = te_row.get("lxx_lemma", "")
                if not g_lemma:
                    entry = _lex_lookup(g_strongs)
                    if entry:
                        g_lemma = entry.get("lemma", "")
                nt_equiv.append({
                    "strongs": g_strongs,
                    "lemma": g_lemma,
                    "nt_total": len(nt_hits),
                    "nt_by_book": nt_by_book,
                })
        result["nt_lxx_equiv"] = nt_equiv
    else:
        result["translation_equivalents"] = pd.DataFrame()
        result["nt_lxx_equiv"] = []

    # --- Example verses ---
    hits_sorted = hits.copy()
    hits_sorted["_order"] = hits_sorted["book_id"].map(_BOOK_ORDER).fillna(99)
    hits_sorted = hits_sorted.sort_values(["_order", "chapter", "verse", "word_num"])

    examples = []
    seen_verses: set = set()
    for _, row in hits_sorted.iterrows():
        ref = (row["book_id"], int(row["chapter"]), int(row["verse"]))
        if ref in seen_verses:
            continue
        seen_verses.add(ref)
        kjv = _kjv_verse(*ref)
        examples.append({
            "reference": f"{row['book_id']} {row['chapter']}:{row['verse']}",
            "word": row["word"],
            "context": kjv,
        })
        if len(examples) >= example_verses:
            break

    result["examples"] = examples
    return result


def print_word_study(strongs: str, *, example_verses: int = 5) -> None:
    """Print a formatted word study to stdout."""
    ws = word_study(strongs, example_verses=example_verses)

    is_hebrew = ws["strongs"].startswith("H")
    lang = "Hebrew" if is_hebrew else "Greek"

    print(f"\n{'='*65}")
    print(f"  Word Study: {ws['strongs']}  —  {lang}")
    print(f"{'='*65}")
    if ws["lemma"]:
        print(f"  Lemma       : {ws['lemma']}")
    if ws["translit"]:
        print(f"  Translit    : {ws['translit']}")
    if ws["gloss"]:
        print(f"  Gloss       : {ws['gloss']}")
    if ws["pos_code"]:
        print(f"  POS code    : {ws['pos_code']}")
    print(f"  Occurrences : {ws['total_occurrences']:,}")
    print()

    if ws["definition"]:
        print("  Definition:")
        defn = ws["definition"]
        # Wrap at ~70 chars
        words = defn.split()
        line, out_lines = [], []
        for w in words:
            line.append(w)
            if len(" ".join(line)) > 68:
                out_lines.append("    " + " ".join(line[:-1]))
                line = [w]
        if line:
            out_lines.append("    " + " ".join(line))
        print("\n".join(out_lines))
        print()

    print("  Distribution by Book (top 15):")
    by_book = ws["by_book"].head(15)
    for _, row in by_book.iterrows():
        bar = "█" * min(int(row["pct"] / 2), 25)
        print(f"    {row['book_name']:<20} {row['count']:4d}  ({row['pct']:5.1f}%)  {bar}")

    print()
    print("  Morphological Forms (top 10):")
    morph = ws["morphological_forms"].head(10)
    print(morph.to_string(index=False))

    if is_hebrew and not ws["translation_equivalents"].empty:
        print()
        print("  LXX Translation Equivalents (word-level alignment, top 10):")
        te = ws["translation_equivalents"].head(10)
        print(te.to_string(index=False))

    if is_hebrew and ws.get("nt_lxx_equiv"):
        print()
        print("  OT → LXX → NT Trajectory:")
        for equiv in ws["nt_lxx_equiv"]:
            print(f"    {equiv['lemma']} ({equiv['strongs']})"
                  f"  —  {equiv['nt_total']:,} NT occurrences")
            nt_bb = equiv["nt_by_book"].head(8)
            for _, row in nt_bb.iterrows():
                print(f"      {row['book_id']:<10} {row['count']:4d}")

    print()
    print("  Example Verses:")
    for ex in ws["examples"]:
        print(f"    [{ex['reference']}]  {ex['word']}")
        if ex["context"]:
            ctx = ex["context"]
            if len(ctx) > 90:
                ctx = ctx[:87] + "..."
            print(f"      {ctx}")
    print()


def word_study_table(strongs: str) -> pd.DataFrame:
    """
    Compact tabular form of a word study — one row per occurrence,
    with reference, inflected form, morphology, and KJV verse.
    Equivalent to concordance() but with lexicon gloss in the header.
    """
    from .concordance import concordance
    clean = strongs.strip("{}").upper()
    is_hebrew = clean.startswith("H")
    corpus = "OT" if is_hebrew else "NT"

    df = concordance(strongs=clean, corpus=corpus, context="KJV")

    lex = _lookup_lex(clean)
    if lex:
        df.attrs["gloss"] = lex["gloss"]
        df.attrs["lemma"] = lex["lemma"]
        df.attrs["translit"] = lex["translit"]

    return df
