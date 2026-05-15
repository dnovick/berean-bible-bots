"""
Per-book language profile reports.

Generates standardized one-page statistical summaries for any Bible book:
  - Word count, vocabulary richness (type-token ratio)
  - Part-of-speech distribution vs. corpus average
  - Verb stem breakdown (OT) or tense/voice distribution (NT)
  - Top 20 most frequent lemmas (Strong's numbers)
  - Hapax legomena count (words appearing only once in the book)

Usage
-----
from bible_grammar.reporting.profiles import book_profile, print_profile, save_profile_report

# In-memory dict of stats
profile = book_profile('Gen')

# Print a formatted text summary to console
print_profile('Gen')

# Save a markdown report
save_profile_report('Gen', 'reports/profiles/Gen_profile.md')

# Batch: all OT books
from bible_grammar.core.reference import all_book_ids
for book_id in all_book_ids('OT'):
    save_profile_report(book_id)
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd
from ..core import db as _db
from ..core.reference import BOOKS, book_info, all_book_ids

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PROFILES_DIR = _REPO_ROOT / "output" / "reports" / "ot" / "survey"

_BOOK_ORDER = {b[0]: b[3] for b in BOOKS}


def _words() -> pd.DataFrame:
    return _db.load()


def _lxx() -> pd.DataFrame:
    return _db.load_lxx()


# --- Corpus-level baselines (computed once, cached) ---
_ot_baseline: dict | None = None
_nt_baseline: dict | None = None


def _get_baseline(testament: str) -> dict:
    global _ot_baseline, _nt_baseline
    if testament == "OT" and _ot_baseline is not None:
        return _ot_baseline
    if testament == "NT" and _nt_baseline is not None:
        return _nt_baseline

    source = "TAHOT" if testament == "OT" else "TAGNT"
    df = _words()
    corpus = df[df["source"] == source]

    pos_pct = (corpus["part_of_speech"].value_counts(normalize=True) * 100).round(1)
    result = {"pos_pct": pos_pct.to_dict()}

    if testament == "OT":
        verbs = corpus[corpus["part_of_speech"] == "Verb"]
        result["stem_pct"] = (
            verbs["stem"].value_counts(normalize=True) * 100).round(1).to_dict()
    else:
        verbs = corpus[corpus["part_of_speech"] == "Verb"]
        result["tense_pct"] = (
            verbs["tense"].value_counts(normalize=True) * 100).round(1).to_dict()
        result["voice_pct"] = (
            verbs["voice"].value_counts(normalize=True) * 100).round(1).to_dict()

    if testament == "OT":
        _ot_baseline = result
    else:
        _nt_baseline = result
    return result


def book_profile(book_id: str) -> dict:
    """
    Compute a complete statistical profile for a single Bible book.

    Returns a dict with keys:
      book_id, book_name, testament, canonical_order,
      total_words, unique_strongs, hapax_count, ttr,
      pos_distribution, verb_detail,
      top_lemmas, baseline_delta
    """
    info = book_info(book_id)
    testament = info["testament"]
    source = "TAHOT" if testament == "OT" else "TAGNT"

    df = _words()
    book_df = df[(df["book_id"] == book_id) & (df["source"] == source)]

    if book_df.empty:
        return {
            "book_id": book_id, "book_name": info["name"],
            "testament": testament, "error": "No data found",
        }

    total_words = len(book_df)

    # Extract lexical Strong's numbers.
    # TAHOT uses braces: {H1234}, {H1234A} — extract bracketed values, skip H9xxx markers
    # TAGNT uses plain values: G1234, G1234G — use the column directly
    if testament == "OT":
        strongs_clean = book_df["strongs"].str.findall(r'\{(H\d+[A-Z]?)\}').explode()
        strongs_clean = strongs_clean.dropna()
        strongs_clean = strongs_clean[~strongs_clean.str.match(r'H9\d{3}')]
    else:
        strongs_clean = book_df["strongs"].dropna()
        strongs_clean = strongs_clean[strongs_clean.str.match(r'^G\d+')]

    unique_strongs = strongs_clean.nunique()
    ttr = round(unique_strongs / total_words, 3) if total_words > 0 else 0

    # Hapax legomena within this book (lemmas appearing exactly once)
    strongs_counts = strongs_clean.value_counts()
    hapax_count = int((strongs_counts == 1).sum())

    # POS distribution
    pos_counts = book_df["part_of_speech"].value_counts()
    pos_pct = (pos_counts / total_words * 100).round(1)
    pos_dist = pos_pct.head(10).to_dict()

    # Verb detail
    verbs = book_df[book_df["part_of_speech"] == "Verb"]
    verb_count = len(verbs)
    if testament == "OT":
        stem_counts = verbs["stem"].value_counts()
        stem_pct = (stem_counts / verb_count * 100).round(1) if verb_count else pd.Series()
        verb_detail = {
            "total_verbs": verb_count,
            "stem_distribution": stem_pct.head(10).to_dict(),
        }
    else:
        tense_counts = verbs["tense"].value_counts()
        voice_counts = verbs["voice"].value_counts()
        mood_counts = verbs["mood"].value_counts()
        verb_detail = {
            "total_verbs": verb_count,
            "tense_distribution": (tense_counts / verb_count * 100).round(1).head(8).to_dict() if verb_count else {},  # noqa: E501
            "voice_distribution": (voice_counts / verb_count * 100).round(1).head(6).to_dict() if verb_count else {},  # noqa: E501
            "mood_distribution":  (mood_counts / verb_count * 100).round(1).head(6).to_dict() if verb_count else {},  # noqa: E501
        }

    # Top lemmas (most frequent lexical roots)
    top_lemmas = strongs_counts.head(20).to_dict()

    # Baseline delta: how does this book compare to corpus average?
    baseline = _get_baseline(testament)
    baseline_pos = baseline["pos_pct"]
    delta = {}
    for pos, pct in pos_dist.items():
        corp_pct = baseline_pos.get(pos, 0)
        delta[pos] = round(pct - corp_pct, 1)

    return {
        "book_id": book_id,
        "book_name": info["name"],
        "testament": testament,
        "canonical_order": info["canonical_order"],
        "chapter_count": info["chapter_count"],
        "total_words": total_words,
        "unique_strongs": unique_strongs,
        "hapax_count": hapax_count,
        "ttr": ttr,
        "pos_distribution": pos_dist,
        "verb_detail": verb_detail,
        "top_lemmas": top_lemmas,
        "baseline_delta": delta,
        "baseline": baseline,
    }


def _fmt_pct_table(data: dict, baseline: dict | None = None,
                   label: str = "Category") -> str:
    lines = [f"| {label:<22} | Count% | vs. Corpus |",
             f"|{'-'*24}|--------|------------|"]
    for k, v in sorted(data.items(), key=lambda x: -x[1]):
        delta = ""
        if baseline is not None:
            d = round(v - baseline.get(k, 0), 1)
            delta = f"{d:+.1f}%" if d != 0 else "  —  "
        lines.append(f"| {str(k):<22} | {v:5.1f}% | {delta:>10} |")
    return "\n".join(lines)


def print_profile(book_id: str) -> None:
    """Print a formatted profile to stdout."""
    p = book_profile(book_id)
    if "error" in p:
        print(f"ERROR: {p['error']}")
        return

    testament_label = "Old Testament" if p["testament"] == "OT" else "New Testament"
    print(f"\n{'='*60}")
    print(f"  {p['book_name']} ({book_id})  —  {testament_label}")
    print(f"{'='*60}")
    print(f"  Words: {p['total_words']:,}  |  Unique lemmas: {p['unique_strongs']:,}  "
          f"|  TTR: {p['ttr']:.3f}  |  Hapax: {p['hapax_count']:,}")
    print(f"  Chapters: {p['chapter_count']}")

    print("\n  Part-of-Speech Distribution (top 8):")
    baseline_pos = p["baseline"]["pos_pct"]
    for pos, pct in sorted(p["pos_distribution"].items(), key=lambda x: -x[1]):
        delta = round(pct - baseline_pos.get(pos, 0), 1)
        bar = "█" * int(pct / 2)
        sign = "+" if delta > 0 else ""
        print(f"    {pos:<16} {pct:5.1f}%  ({sign}{delta:+.1f}% vs corpus)  {bar}")

    vd = p["verb_detail"]
    print(f"\n  Verbs: {vd['total_verbs']:,} total")
    if p["testament"] == "OT":
        print("  Stem Distribution:")
        baseline_stem = p["baseline"].get("stem_pct", {})
        for stem, pct in sorted(vd["stem_distribution"].items(), key=lambda x: -x[1]):
            delta = round(pct - baseline_stem.get(stem, 0), 1)
            sign = "+" if delta > 0 else ""
            print(f"    {stem:<14} {pct:5.1f}%  ({sign}{delta:+.1f}% vs corpus)")
    else:
        print("  Tense Distribution:")
        for tense, pct in sorted(vd["tense_distribution"].items(), key=lambda x: -x[1]):
            print(f"    {tense:<14} {pct:5.1f}%")
        print("  Voice Distribution:")
        for voice, pct in sorted(vd["voice_distribution"].items(), key=lambda x: -x[1]):
            print(f"    {voice:<14} {pct:5.1f}%")

    print("\n  Top 10 Lexical Lemmas (Strong's):")
    for strongs, cnt in list(p["top_lemmas"].items())[:10]:
        print(f"    {strongs:<20} {cnt:4d} occurrences")

    print()


def save_profile_report(
    book_id: str,
    output_path: str | Path | None = None,
) -> Path:
    """
    Save a markdown profile report for a single book.

    Parameters
    ----------
    book_id     : Bible book ID (e.g. 'Gen', 'Rom')
    output_path : Custom output path; defaults to reports/profiles/{book_id}_profile.md

    Returns the path where the file was saved.
    """
    p = book_profile(book_id)
    if "error" in p:
        raise ValueError(f"Cannot generate profile for {book_id}: {p['error']}")

    if output_path is None:
        sub = 'ot' if p['testament'] == 'OT' else 'nt'
        profile_dir = _REPO_ROOT / 'output' / 'reports' / sub / 'survey'
        profile_dir.mkdir(parents=True, exist_ok=True)
        output_path = profile_dir / f"{book_id}_profile.md"
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    testament_label = "Old Testament" if p["testament"] == "OT" else "New Testament"
    lines = [
        f"# {p['book_name']} ({book_id}) — Language Profile",
        "",
        f"**{testament_label}** | Canonical order: {p['canonical_order']} | Chapters: {p['chapter_count']}",  # noqa: E501
        "",
        "---",
        "",
        "## Summary Statistics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total word tokens | {p['total_words']:,} |",
        f"| Unique lexical lemmas | {p['unique_strongs']:,} |",
        f"| Type-token ratio (TTR) | {p['ttr']:.3f} |",
        f"| Hapax legomena (once-only) | {p['hapax_count']:,} ({p['hapax_count']/p['unique_strongs']*100:.1f}% of vocab) |",  # noqa: E501
        "",
        "---",
        "",
        "## Part-of-Speech Distribution",
        "",
        "*Δ = difference from corpus average for this testament.*",
        "",
        "| Part of Speech | This Book | Corpus Avg | Δ |",
        "|----------------|-----------|------------|---|",
    ]

    baseline_pos = p["baseline"]["pos_pct"]
    for pos, pct in sorted(p["pos_distribution"].items(), key=lambda x: -x[1]):
        corp = baseline_pos.get(pos, 0)
        delta = round(pct - corp, 1)
        sign = "+" if delta > 0 else ""
        lines.append(f"| {pos} | {pct:.1f}% | {corp:.1f}% | {sign}{delta:.1f}% |")

    lines += ["", "---", "", "## Verb Analysis", ""]

    vd = p["verb_detail"]
    verb_pct = round(vd["total_verbs"] / p["total_words"] * 100, 1)
    lines.append(f"**Total verbs:** {vd['total_verbs']:,} ({verb_pct:.1f}% of words)")
    lines.append("")

    if p["testament"] == "OT":
        lines += [
            "### Stem (Binyan) Distribution",
            "",
            "| Stem | This Book | Corpus Avg | Δ |",
            "|------|-----------|------------|---|",
        ]
        baseline_stem = p["baseline"].get("stem_pct", {})
        for stem, pct in sorted(vd["stem_distribution"].items(), key=lambda x: -x[1]):
            corp = baseline_stem.get(stem, 0)
            delta = round(pct - corp, 1)
            sign = "+" if delta > 0 else ""
            lines.append(f"| {stem} | {pct:.1f}% | {corp:.1f}% | {sign}{delta:.1f}% |")
    else:
        lines += [
            "### Tense Distribution",
            "",
            "| Tense | This Book | Corpus Avg | Δ |",
            "|-------|-----------|------------|---|",
        ]
        baseline_tense = p["baseline"].get("tense_pct", {})
        for tense, pct in sorted(vd["tense_distribution"].items(), key=lambda x: -x[1]):
            corp = baseline_tense.get(tense, 0)
            delta = round(pct - corp, 1)
            sign = "+" if delta > 0 else ""
            lines.append(f"| {tense} | {pct:.1f}% | {corp:.1f}% | {sign}{delta:.1f}% |")

        lines += [
            "",
            "### Voice Distribution",
            "",
            "| Voice | This Book | Corpus Avg | Δ |",
            "|-------|-----------|------------|---|",
        ]
        baseline_voice = p["baseline"].get("voice_pct", {})
        for voice, pct in sorted(vd["voice_distribution"].items(), key=lambda x: -x[1]):
            corp = baseline_voice.get(voice, 0)
            delta = round(pct - corp, 1)
            sign = "+" if delta > 0 else ""
            lines.append(f"| {voice} | {pct:.1f}% | {corp:.1f}% | {sign}{delta:.1f}% |")

    lines += [
        "",
        "---",
        "",
        "## Top 20 Most Frequent Lexical Lemmas",
        "",
        "| Rank | Strong's | Occurrences | % of Book |",
        "|------|----------|-------------|-----------|",
    ]
    for rank, (strongs, cnt) in enumerate(p["top_lemmas"].items(), start=1):
        pct_book = round(cnt / p["total_words"] * 100, 2)
        lines.append(f"| {rank} | {strongs} | {cnt:,} | {pct_book:.2f}% |")

    lines += [
        "",
        "---",
        "",
        "*Generated by berean-bible-bots. Source: STEPBible TAHOT/TAGNT (CC BY).*",
    ]

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def batch_profiles(
    testament: str | None = None,
    book_ids: list[str] | None = None,
    output_dir: str | Path | None = None,
) -> list[Path]:
    """
    Generate profile reports for multiple books.

    Parameters
    ----------
    testament : 'OT', 'NT', or None for all books
    book_ids  : Explicit list of book IDs (overrides testament)
    output_dir: Directory for reports (default: reports/profiles/)

    Returns list of saved file paths.
    """
    if book_ids is None:
        book_ids = all_book_ids(testament)

    if output_dir is None:
        output_dir = _PROFILES_DIR
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = []
    for book_id in book_ids:
        try:
            path = save_profile_report(book_id, output_dir / f"{book_id}_profile.md")
            paths.append(path)
            print(f"  Saved: {path.name}")
        except Exception as e:
            print(f"  SKIP {book_id}: {e}")
    return paths
