"""
Theological term mapping: trace Hebrew roots across OT, LXX, and NT.

For a given set of Hebrew Strong's numbers, builds a structured table showing:
  - OT occurrence count and distribution
  - Primary LXX translation equivalent(s) with word-level alignment confidence
  - NT occurrence count of the primary LXX term

This replaces the verse-level co-occurrence approach in alignment.py with
IBM Model 1 word-level alignment for much higher precision.

Usage
-----
from bible_grammar.lexical.termmap import term_map, print_term_map, THEOLOGICAL_TERMS

# Single term
term_map('H1285')          # בְּרִית  "covenant"

# Batch — built-in set of key theological terms
df = term_map(THEOLOGICAL_TERMS)
print_term_map(df)

# Custom list
term_map(['H1285', 'H2617', 'H571'])
"""

from __future__ import annotations
import re
import pandas as pd
from ..core import db as _db
from .lexicon import _heb as _load_heb_lex, _grk as _load_grk_lex
from ..core.reference import BOOKS

# Key Hebrew theological roots organized by theme
THEOLOGICAL_TERMS: dict[str, list[str]] = {
    "Covenant / Faithfulness": ["H1285", "H2617", "H530", "H571"],
    "Holiness / Purity":       ["H6944", "H6918", "H2891", "H2930"],
    "Righteousness / Justice": ["H6664", "H4941", "H3477"],
    "Salvation / Redemption":  ["H3467", "H1350", "H6299", "H3444"],
    "Glory / Honour":          ["H3519", "H1935"],
    "Word / Speech":           ["H1697", "H565", "H6310"],
    "Spirit / Breath / Wind":  ["H7307"],
    "Knowledge / Wisdom":      ["H3045", "H2451", "H998"],
    "Love":                    ["H157", "H160"],
    "Peace":                   ["H7965"],
    "Fear / Awe":              ["H3372", "H3374"],
    "Repentance / Return":     ["H7725", "H5162"],
    "Praise / Worship":        ["H1984", "H7812", "H3034"],
    "Creation / Making":       ["H1254", "H6213"],
    "Sin / Transgression":     ["H2398", "H6588", "H5771"],
    "Atonement":               ["H3722"],
    "Blessing / Curse":        ["H1288", "H423"],
    "Faith / Trust":           ["H539", "H982"],
    "Wrath / Anger":           ["H639", "H2534"],
    "Mercy / Compassion":      ["H7356", "H2603"],
}

_ALL_TERMS: list[str] = [h for terms in THEOLOGICAL_TERMS.values() for h in terms]

_BOOK_IDS = {b[0] for b in BOOKS}


def _normalize_strongs_pat(strongs: str) -> str:
    """Build a regex pattern that matches strongs with or without leading zeros / variant suffixes."""  # noqa: E501
    m = re.match(r'^([HG])0*(\d+)([A-Z]?)$', strongs.upper())
    if m:
        prefix, num, suffix = m.groups()
        return rf'^{prefix}0*{num}{suffix}[A-Z]?$'
    return re.escape(strongs.upper())


def _nt_count_for_strongs(g_strongs: str, nt_df: pd.DataFrame) -> int:
    pat = _normalize_strongs_pat(g_strongs)
    return int(nt_df["strongs"].str.upper().str.match(pat, na=False).sum())


def term_map(
    strongs: str | list[str] | dict[str, list[str]] | None = None,
    *,
    min_alignment_count: int = 3,
    top_lxx: int = 3,
) -> pd.DataFrame:
    """
    Build a term-mapping table for one or more Hebrew Strong's numbers.

    Parameters
    ----------
    strongs             : Single strongs string, list of strings, or
                          dict {theme: [strongs, ...]} (defaults to THEOLOGICAL_TERMS)
    min_alignment_count : Minimum word-level alignment count to include an LXX equiv
    top_lxx             : How many top LXX equivalents to show per root

    Returns a DataFrame with columns:
      theme, heb_strongs, heb_lemma, heb_gloss,
      ot_count,
      lxx_lemma_1, lxx_strongs_1, lxx_pct_1, lxx_nt_count_1,
      lxx_lemma_2, lxx_strongs_2, lxx_pct_2, lxx_nt_count_2,
      lxx_lemma_3, lxx_strongs_3, lxx_pct_3, lxx_nt_count_3
    """
    from ..core.ibm_align import translation_equivalents_w

    if strongs is None:
        strongs = THEOLOGICAL_TERMS
    if isinstance(strongs, str):
        strongs = {"": [strongs]}
    elif isinstance(strongs, list):
        strongs = {"": strongs}

    heb_lex = _load_heb_lex()
    grk_lex = _load_grk_lex()

    words_df = _db.load()
    nt_df = words_df[words_df["source"] == "TAGNT"][["strongs"]].copy()
    ot_df = words_df[words_df["source"] == "TAHOT"]

    rows = []
    for theme, roots in strongs.items():
        for root in roots:
            clean = root.strip("{}").upper()
            base = re.sub(r'[A-Z]$', '', clean)

            # OT count
            _normalize_strongs_pat(base)
            ot_count = int(ot_df["strongs"].str.upper().str.contains(base, na=False).sum())

            # Lexicon — try clean, zero-padded, and base forms
            m_pad = re.match(r'^([HG])(\d+)([A-Z]?)$', clean)
            zero_padded = (f"{m_pad.group(1)}{int(m_pad.group(2)):04d}{m_pad.group(3)}"
                           if m_pad else clean)
            lex = heb_lex.get(clean) or heb_lex.get(zero_padded) or heb_lex.get(base) or {}

            # Word-level LXX equivalents
            te = translation_equivalents_w(
                heb_strongs=clean,
                min_count=min_alignment_count,
                top_n=top_lxx,
            )

            row: dict = {
                "theme":       theme,
                "heb_strongs": clean,
                "heb_lemma":   lex.get("lemma", ""),
                "heb_gloss":   lex.get("gloss", ""),
                "ot_count":    ot_count,
            }

            for i in range(1, top_lxx + 1):
                if i <= len(te):
                    te_row = te.iloc[i - 1]
                    g_strongs = te_row.get("lxx_strongs", "")
                    g_lemma = te_row.get("lxx_lemma", "")
                    if not g_lemma and g_strongs:
                        g_lemma = (grk_lex.get(g_strongs) or {}).get("lemma", "")
                    pct = te_row.get("pct", 0.0)
                    nt_cnt = _nt_count_for_strongs(g_strongs, nt_df) if g_strongs else 0
                    row[f"lxx_lemma_{i}"] = g_lemma
                    row[f"lxx_strongs_{i}"] = g_strongs
                    row[f"lxx_pct_{i}"] = pct
                    row[f"lxx_nt_count_{i}"] = nt_cnt
                else:
                    row[f"lxx_lemma_{i}"] = ""
                    row[f"lxx_strongs_{i}"] = ""
                    row[f"lxx_pct_{i}"] = 0.0
                    row[f"lxx_nt_count_{i}"] = 0

            rows.append(row)

    return pd.DataFrame(rows)


def print_term_map(
    df: pd.DataFrame | None = None,
    *,
    theme: str | None = None,
) -> None:
    """
    Print a formatted theological term mapping table.

    Parameters
    ----------
    df    : Output of term_map(). If None, runs term_map(THEOLOGICAL_TERMS).
    theme : Filter to a single theme (substring match, case-insensitive).
    """
    if df is None:
        df = term_map()

    if theme is not None:
        df = df[df["theme"].str.lower().str.contains(theme.lower())]

    current_theme = None
    for _, row in df.iterrows():
        if row["theme"] != current_theme:
            current_theme = row["theme"]
            print(f"\n{'─'*70}")
            print(f"  {current_theme}")
            print(f"{'─'*70}")
            print(
                f"  {'Root':<10} {'Lemma':<14} {'Gloss':<28} {'OT':>5}  {'LXX equivalents (word-level alignment)'}")  # noqa: E501
            print(f"  {'-'*9} {'-'*13} {'-'*27} {'-'*5}  {'-'*38}")

        lxx_parts = []
        for i in range(1, 4):
            lemma = row.get(f"lxx_lemma_{i}", "")
            pct = row.get(f"lxx_pct_{i}", 0.0)
            nt = row.get(f"lxx_nt_count_{i}", 0)
            if lemma:
                lxx_parts.append(f"{lemma} {pct:.0f}% [NT:{nt}]")
        lxx_str = "  |  ".join(lxx_parts) if lxx_parts else "(no word-level alignment)"

        gloss = str(row["heb_gloss"])[:27]
        print(
            f"  {row['heb_strongs']:<10} {str(row['heb_lemma']):<14} {gloss:<28} {row['ot_count']:>5}  {lxx_str}")  # noqa: E501

    print()


def term_map_table(
    strongs: str | list[str] | dict[str, list[str]] | None = None,
) -> pd.DataFrame:
    """
    Compact pivot: one row per (Hebrew root, LXX equivalent), suitable for
    display in a notebook or export to CSV.

    Returns columns: theme, heb_strongs, heb_lemma, heb_gloss, ot_count,
                     lxx_lemma, lxx_strongs, lxx_gloss, lxx_pct, nt_count
    """
    grk_lex = _load_grk_lex()
    raw = term_map(strongs)

    out_rows = []
    for _, row in raw.iterrows():
        for i in range(1, 4):
            g_lemma = row.get(f"lxx_lemma_{i}", "")
            g_strongs = row.get(f"lxx_strongs_{i}", "")
            pct = row.get(f"lxx_pct_{i}", 0.0)
            nt_cnt = row.get(f"lxx_nt_count_{i}", 0)
            if not g_lemma:
                continue
            g_gloss = (grk_lex.get(g_strongs) or {}).get("gloss", "")
            out_rows.append({
                "theme":       row["theme"],
                "heb_strongs": row["heb_strongs"],
                "heb_lemma":   row["heb_lemma"],
                "heb_gloss":   row["heb_gloss"],
                "ot_count":    row["ot_count"],
                "lxx_lemma":   g_lemma,
                "lxx_strongs": g_strongs,
                "lxx_gloss":   g_gloss,
                "lxx_pct":     pct,
                "nt_count":    nt_cnt,
            })

    return pd.DataFrame(out_rows)
