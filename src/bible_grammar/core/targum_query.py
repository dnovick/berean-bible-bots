"""
Load cached Targum verse texts downloaded by scripts/fetch_targum_data.py.

Coverage:
  Targum Onkelos    — Gen, Exo, Lev, Num, Deu
  Targum Jonathan   — Jos, Jdg, Isa, Jer, Ezk, Hos, Amo, Mic, Nah, Hab, Zec
  Targum to Psalms  — Psa

Each row: targum, book_id, chapter, verse, text (Aramaic).

Usage:
    from bible_grammar.core.targum_query import load_targum
    tg = load_targum()
    onkelos_gen = tg[(tg.targum == 'Onkelos') & (tg.book_id == 'Gen')]
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PARQUET = _REPO_ROOT / "data" / "processed" / "targum.parquet"


def load_targum(targum: str | None = None, book_id: str | None = None) -> pd.DataFrame:
    """Load Targum data; optionally filter by targum name and/or book_id.

    Parameters
    ----------
    targum : str, optional
        One of 'Onkelos', 'Jonathan', 'Psalms'. None returns all.
    book_id : str, optional
        OSIS book code (e.g. 'Gen', 'Isa', 'Psa'). None returns all.

    Raises
    ------
    FileNotFoundError
        If the parquet cache is missing — run ``scripts/fetch_targum_data.py`` first.
    """
    if not _PARQUET.exists():
        raise FileNotFoundError(
            f"Targum data not found at {_PARQUET}.\n"
            "Run: python scripts/fetch_targum_data.py"
        )
    df = pd.read_parquet(_PARQUET)
    if targum is not None:
        df = df[df["targum"] == targum]
    if book_id is not None:
        df = df[df["book_id"] == book_id]
    return df.reset_index(drop=True)


COVERAGE: dict[str, list[str]] = {
    "Onkelos": ["Gen", "Exo", "Lev", "Num", "Deu"],
    "Jonathan": ["Jos", "Jdg", "Isa", "Jer", "Ezk", "Hos", "Amo", "Mic", "Nah", "Hab", "Zec"],
    "Psalms": ["Psa"],
}
