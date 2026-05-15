"""
IBM Model 1 word-level alignment for Hebrew MT ↔ LXX.

Trains a statistical translation model on the full OT parallel corpus
(~23,000 verse pairs) using the EM algorithm. Produces token-level
P(Greek | Hebrew) and P(Hebrew | Greek) translation probabilities, then
applies the intersection heuristic to build a confident word-level
alignment.

Usage
-----
from bible_grammar.core.ibm_align import build_word_alignment, load_word_alignment

# Build and save (takes ~30s)
build_word_alignment()

# Query
df = load_word_alignment()
# df has: book_id, chapter, verse,
#         heb_word_num, heb_strongs, heb_word,
#         lxx_word_num, lxx_strongs, lxx_lemma,
#         p_h2g, p_g2h
"""

from __future__ import annotations
from collections import defaultdict
from pathlib import Path
import re
import pandas as pd
from . import db as _db

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PROCESSED = _REPO_ROOT / "data" / "processed"
WORD_ALIGN_PARQUET = _PROCESSED / "word_alignment.parquet"

# Content POS — used to build cleaner alignment but we train on all words
_HEB_CONTENT = {"Noun", "Verb", "Adjective", "Adverb"}
_LXX_CONTENT = {"Noun", "Verb", "Adjective", "Adverb"}

NULL = "__NULL__"


def _extract_heb_strongs(s: str) -> str:
    """Extract primary (content) Hebrew Strong's number from TAHOT strongs cell.
    TAHOT strongs cells may contain prefixes like H9003/{H1697G}+H9014.
    The content word is always in curly braces; H9xxx are grammatical tags."""
    if not isinstance(s, str):
        return NULL
    # Find all braced strongs numbers; prefer the first non-H9xxx one
    matches = re.findall(r'\{(H\d+[A-Z]?)\}', s)
    for m in matches:
        if not re.match(r'H9\d+', m):
            return m
    return matches[0] if matches else NULL


def _extract_lxx_strongs(s: str) -> str:
    """Extract Greek Strong's number from LXX strongs cell."""
    if not isinstance(s, str):
        return NULL
    m = re.match(r'^(G\d+)', s.strip())
    return m.group(1) if m else NULL


def _build_corpus(
    heb_df: pd.DataFrame,
    lxx_df: pd.DataFrame,
) -> list[tuple[list[str], list[str], str, int, int]]:
    """
    Build parallel verse corpus as list of (heb_tokens, lxx_tokens, book, ch, vs).
    Tokens are Strong's numbers.
    """
    heb = heb_df[heb_df["source"] == "TAHOT"].copy()
    lxx = lxx_df[~lxx_df["is_deuterocanon"]].copy()

    heb["tok"] = heb["strongs"].apply(_extract_heb_strongs)
    lxx["tok"] = lxx["strongs"].apply(_extract_lxx_strongs)

    # Group by verse
    heb_grouped = heb.groupby(["book_id", "chapter", "verse"])
    lxx_grouped = lxx.groupby(["book_id", "chapter", "verse"])

    lxx_dict = {k: list(g["tok"]) for k, g in lxx_grouped}

    corpus = []
    for (book, ch, vs), hg in heb_grouped:
        key = (book, ch, vs)
        if key not in lxx_dict:
            continue
        h_toks = list(hg["tok"])
        l_toks = lxx_dict[key]
        if h_toks and l_toks:
            corpus.append((h_toks, l_toks, book, ch, vs))
    return corpus


def _ibm1_em(
    src_sents: list[list[str]],
    tgt_sents: list[list[str]],
    n_iter: int = 5,
) -> dict[str, dict[str, float]]:
    """
    Train IBM Model 1: learn P(tgt | src) via EM.

    Returns t[src_tok][tgt_tok] = probability.
    """
    # Collect vocabularies
    tgt_vocab: set[str] = set()
    for sent in tgt_sents:
        tgt_vocab.update(sent)

    # Initialize uniformly
    t: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    uniform = 1.0 / max(len(tgt_vocab), 1)
    for src_sent, tgt_sent in zip(src_sents, tgt_sents):
        for s in src_sent + [NULL]:
            for tgt in tgt_sent:
                t[s][tgt] = uniform

    for iteration in range(n_iter):
        counts: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
        total: dict[str, float] = defaultdict(float)

        for src_sent, tgt_sent in zip(src_sents, tgt_sents):
            src_with_null = src_sent + [NULL]
            for tgt in tgt_sent:
                # Normalizing constant
                z = sum(t[s][tgt] for s in src_with_null)
                if z == 0:
                    continue
                for s in src_with_null:
                    delta = t[s][tgt] / z
                    counts[s][tgt] += delta
                    total[s] += delta

        # M-step
        t = defaultdict(lambda: defaultdict(float))
        for s, tgt_counts in counts.items():
            tot = total[s]
            if tot == 0:
                continue
            for tgt, c in tgt_counts.items():
                t[s][tgt] = c / tot

    return t


def build_word_alignment(
    n_iter: int = 5,
    min_prob: float = 0.1,
) -> pd.DataFrame:
    """
    Build word-level alignment using IBM Model 1 (intersection heuristic).

    Trains P(LXX | Hebrew) and P(Hebrew | LXX) independently, then keeps
    only alignments where both directions agree (intersection). This gives
    high-precision alignments at the cost of some recall.

    Parameters
    ----------
    n_iter   : EM iterations (5 is typically sufficient for IBM Model 1)
    min_prob : Minimum probability threshold for inclusion

    Returns a DataFrame saved to data/processed/word_alignment.parquet.
    """
    print("  Loading TAHOT + LXX data...")
    heb_df = _db.load()
    lxx_df = _db.load_lxx()

    print("  Building parallel verse corpus...")
    corpus = _build_corpus(heb_df, lxx_df)
    print(f"    {len(corpus):,} verse pairs")

    heb_sents = [c[0] for c in corpus]
    lxx_sents = [c[1] for c in corpus]

    print(f"  Training IBM Model 1 (Hebrew→Greek, {n_iter} iterations)...")
    t_h2g = _ibm1_em(heb_sents, lxx_sents, n_iter)

    print(f"  Training IBM Model 1 (Greek→Hebrew, {n_iter} iterations)...")
    t_g2h = _ibm1_em(lxx_sents, heb_sents, n_iter)

    print("  Building word-level alignment table...")

    # Precompute per-verse word data for looking up word forms and lemmas
    heb = heb_df[heb_df["source"] == "TAHOT"].copy()
    lxx = lxx_df[~lxx_df["is_deuterocanon"]].copy()
    heb["tok"] = heb["strongs"].apply(_extract_heb_strongs)
    lxx["tok"] = lxx["strongs"].apply(_extract_lxx_strongs)

    heb_by_verse = {
        k: g.reset_index(drop=True)
        for k, g in heb.groupby(["book_id", "chapter", "verse"])
    }
    lxx_by_verse = {
        k: g.reset_index(drop=True)
        for k, g in lxx.groupby(["book_id", "chapter", "verse"])
    }

    rows = []
    for h_toks, l_toks, book, ch, vs in corpus:
        key = (book, ch, vs)
        hg = heb_by_verse.get(key)
        lg = lxx_by_verse.get(key)
        if hg is None or lg is None:
            continue

        # For each Hebrew word, find best LXX alignment
        # h2g: best Greek for each Hebrew
        h2g: dict[int, int] = {}
        for hi, h_tok in enumerate(h_toks):
            best_j, best_p = -1, 0.0
            for lj, l_tok in enumerate(l_toks):
                p = t_h2g[h_tok].get(l_tok, 0)
                if p > best_p:
                    best_p, best_j = p, lj
            if best_p >= min_prob:
                h2g[hi] = best_j

        # g2h: best Hebrew for each Greek (reverse)
        g2h: dict[int, int] = {}
        for lj, l_tok in enumerate(l_toks):
            best_i, best_p = -1, 0.0
            for hi, h_tok in enumerate(h_toks):
                p = t_g2h[l_tok].get(h_tok, 0)
                if p > best_p:
                    best_p, best_i = p, hi
            if best_p >= min_prob:
                g2h[lj] = best_i

        # Intersection: keep only (hi, lj) pairs where both directions agree
        for hi, lj in h2g.items():
            if g2h.get(lj) == hi:
                h_row = hg.iloc[hi] if hi < len(hg) else None
                l_row = lg.iloc[lj] if lj < len(lg) else None
                if h_row is None or l_row is None:
                    continue
                rows.append({
                    "book_id":      book,
                    "chapter":      ch,
                    "verse":        vs,
                    "heb_word_num": int(h_row["word_num"]),
                    "heb_strongs":  _extract_heb_strongs(str(h_row["strongs"])),
                    "heb_word":     str(h_row["word"]),
                    "heb_pos":      str(h_row["part_of_speech"]),
                    "heb_stem":     str(h_row.get("stem", "")),
                    "lxx_word_num": int(l_row["word_num"]),
                    "lxx_strongs":  _extract_lxx_strongs(str(l_row["strongs"])),
                    "lxx_lemma":    str(l_row["lemma"]),
                    "lxx_pos":      str(l_row["part_of_speech"]),
                    "p_h2g":        round(t_h2g[h_toks[hi]].get(l_toks[lj], 0), 4),
                    "p_g2h":        round(t_g2h[l_toks[lj]].get(h_toks[hi], 0), 4),
                })

    df = pd.DataFrame(rows)
    df.to_parquet(WORD_ALIGN_PARQUET, index=False)
    print(f"    Saved word alignment: {WORD_ALIGN_PARQUET}  ({len(df):,} aligned pairs)")
    return df


def load_word_alignment() -> pd.DataFrame:
    if WORD_ALIGN_PARQUET.exists():
        return pd.read_parquet(WORD_ALIGN_PARQUET)
    raise FileNotFoundError(
        "No word alignment data found. Run: python scripts/build_word_alignment.py"
    )


def translation_equivalents_w(
    *,
    heb_strongs: str | None = None,
    heb_stem: str | None = None,
    heb_pos: str | None = None,
    book: str | list[str] | None = None,
    book_group: str | None = None,
    min_count: int = 2,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    Find LXX Greek lemmas that are word-level aligned to a Hebrew lemma/stem.
    Uses IBM Model 1 intersection alignment — much more precise than
    verse-level co-occurrence.

    Parameters match translation_equivalents() in alignment.py.
    """
    from .reference import book_ids_for_group
    import re as _re

    df = load_word_alignment()
    mask = pd.Series(True, index=df.index)

    if heb_strongs is not None:
        clean = heb_strongs.strip("{}").upper()
        # Normalize: strip variant suffix letter and leading zeros from the numeric part
        # so H530 matches H0530, H530A, H0530A etc.
        m = _re.match(r'^([HG])0*(\d+)([A-Z]?)$', clean)
        if m:
            prefix, num, suffix = m.groups()
            # Build a pattern matching H/G + optional leading zeros + number + optional letter
            pat = rf'^{prefix}0*{num}{suffix}[A-Z]?$'
        else:
            pat = clean
        mask &= df["heb_strongs"].str.upper().str.match(pat, na=False)
    if heb_stem is not None:
        mask &= df["heb_stem"].str.lower().str.contains(heb_stem.lower(), na=False)
    if heb_pos is not None:
        mask &= df["heb_pos"].str.lower().str.contains(heb_pos.lower(), na=False)
    if book is not None:
        vals = [book] if isinstance(book, str) else book
        mask &= df["book_id"].isin(vals)
    if book_group is not None:
        mask &= df["book_id"].isin(book_ids_for_group(book_group))

    filtered = df[mask]
    if filtered.empty:
        return pd.DataFrame(columns=["lxx_lemma", "lxx_strongs", "lxx_pos", "count", "pct"])

    counts = (
        filtered.groupby(["lxx_lemma", "lxx_strongs", "lxx_pos"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    # Deduplicate on lxx_strongs — keep highest count row per strongs
    counts = counts.sort_values("count", ascending=False).drop_duplicates(
        subset="lxx_strongs", keep="first")
    counts = counts[counts["count"] >= min_count].head(top_n)
    total = counts["count"].sum()
    counts["pct"] = (counts["count"] / total * 100).round(1)
    return counts.reset_index(drop=True)


def hebrew_sources_w(
    *,
    lxx_strongs: str | None = None,
    lxx_lemma: str | None = None,
    book: str | list[str] | None = None,
    min_count: int = 2,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    Reverse: given a Greek LXX lemma/strongs, find the Hebrew words it translates.
    Uses IBM Model 1 intersection alignment.
    """
    df = load_word_alignment()
    mask = pd.Series(True, index=df.index)

    if lxx_strongs is not None:
        mask &= df["lxx_strongs"].str.upper() == lxx_strongs.upper()
    if lxx_lemma is not None:
        mask &= df["lxx_lemma"].str.lower() == lxx_lemma.lower()
    if book is not None:
        vals = [book] if isinstance(book, str) else book
        mask &= df["book_id"].isin(vals)

    filtered = df[mask]
    if filtered.empty:
        return pd.DataFrame(columns=["heb_strongs", "heb_stem", "heb_pos", "count", "pct"])

    counts = (
        filtered.groupby(["heb_strongs", "heb_stem", "heb_pos"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    # Deduplicate on root strongs (strip trailing variant letter, e.g. H6213A → H6213)
    counts["_root"] = counts["heb_strongs"].str.replace(r'[A-Z]$', '', regex=True)
    counts = counts.drop_duplicates(subset="_root", keep="first").drop(columns=["_root"])
    counts = counts[counts["count"] >= min_count].head(top_n)
    total = counts["count"].sum()
    counts["pct"] = (counts["count"] / total * 100).round(1)
    return counts.reset_index(drop=True)
