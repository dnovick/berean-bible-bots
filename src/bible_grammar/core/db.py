"""Persist and load the word DataFrame to/from SQLite and Parquet."""

from __future__ import annotations
from pathlib import Path
import pandas as pd
from .reference import BOOKS

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PROCESSED = _REPO_ROOT / "data" / "processed"
DB_PATH = _PROCESSED / "bible_grammar.db"
PARQUET_PATH = _PROCESSED / "words.parquet"
TRANSLATIONS_PARQUET = _PROCESSED / "translations.parquet"
LXX_PARQUET = _PROCESSED / "lxx.parquet"

# Module-level caches — shared across all callers to avoid re-loading per module
_words_cache: pd.DataFrame | None = None
_lxx_cache: pd.DataFrame | None = None
_tr_cache: pd.DataFrame | None = None


def invalidate_cache() -> None:
    """Clear all in-memory DataFrame caches (call after rebuilding the database)."""
    global _words_cache, _lxx_cache, _tr_cache
    _words_cache = None
    _lxx_cache = None
    _tr_cache = None


# ── Load (cached) ─────────────────────────────────────────────────────────────

def load(parquet_path: Path = PARQUET_PATH) -> pd.DataFrame:
    """Load TAHOT/TAGNT words from Parquet (cached). Falls back to SQLite."""
    global _words_cache
    if _words_cache is None:
        if parquet_path.exists():
            _words_cache = pd.read_parquet(parquet_path)
        elif DB_PATH.exists():
            import sqlite3
            with sqlite3.connect(DB_PATH) as con:
                _words_cache = pd.read_sql("SELECT * FROM words", con)
        else:
            raise FileNotFoundError(
                f"No processed data found at {parquet_path} or {DB_PATH}.\n"
                "Run: python scripts/build_db.py"
            )
    return _words_cache


def load_lxx(parquet_path: Path = LXX_PARQUET) -> pd.DataFrame:
    """Load LXX word data from Parquet (cached). Falls back to SQLite."""
    global _lxx_cache
    if _lxx_cache is None:
        if parquet_path.exists():
            _lxx_cache = pd.read_parquet(parquet_path)
        elif DB_PATH.exists():
            import sqlite3
            with sqlite3.connect(DB_PATH) as con:
                _lxx_cache = pd.read_sql("SELECT * FROM lxx", con)
        else:
            raise FileNotFoundError(
                "No LXX data found. Run: python scripts/build_db.py"
            )
    return _lxx_cache


def load_translations(parquet_path: Path = TRANSLATIONS_PARQUET) -> pd.DataFrame:
    """Load translation verses from Parquet (cached). Falls back to SQLite."""
    global _tr_cache
    if _tr_cache is None:
        if parquet_path.exists():
            _tr_cache = pd.read_parquet(parquet_path)
        elif DB_PATH.exists():
            import sqlite3
            with sqlite3.connect(DB_PATH) as con:
                _tr_cache = pd.read_sql("SELECT * FROM translations", con)
        else:
            raise FileNotFoundError(
                "No translations data found. Run: python scripts/build_db.py"
            )
    return _tr_cache


# ── Save ──────────────────────────────────────────────────────────────────────

def _persist(
    df: pd.DataFrame,
    parquet_path: Path,
    db_path: Path,
    table_name: str,
    index_cols: list[str],
) -> None:
    """Write DataFrame to Parquet and SQLite with the given indexes."""
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(parquet_path, index=False)
    print(f"Saved Parquet: {parquet_path}  ({len(df):,} rows)")

    import sqlite3
    with sqlite3.connect(db_path) as con:
        df.to_sql(table_name, con, if_exists="replace", index=True, index_label="id")
        for col in index_cols:
            con.execute(
                f"CREATE INDEX IF NOT EXISTS idx_{table_name}_{col} "
                f"ON {table_name}({col})"
            )
    print(f"Saved SQLite table '{table_name}': {db_path}")


def save(df: pd.DataFrame, db_path: Path = DB_PATH,
         parquet_path: Path = PARQUET_PATH) -> None:
    """Write the words DataFrame to SQLite and Parquet."""
    _persist(df, parquet_path, db_path, "words",
             ["book_id", "part_of_speech", "stem", "conjugation", "source"])

    # books lookup table (kept separate from _persist — special shape)
    import sqlite3
    with sqlite3.connect(db_path) as con:
        books_df = pd.DataFrame(
            BOOKS,
            columns=["book_id", "name", "testament", "canonical_order", "chapter_count"],
        )
        books_df.to_sql("books", con, if_exists="replace", index=False)


def save_translations(df: pd.DataFrame, db_path: Path = DB_PATH,
                      parquet_path: Path = TRANSLATIONS_PARQUET) -> None:
    """Write the translations DataFrame to SQLite and Parquet."""
    _persist(df, parquet_path, db_path, "translations", ["book_id", "translation"])


def save_lxx(df: pd.DataFrame, db_path: Path = DB_PATH,
             parquet_path: Path = LXX_PARQUET) -> None:
    """Write the LXX DataFrame to SQLite and Parquet."""
    _persist(df, parquet_path, db_path, "lxx",
             ["book_id", "part_of_speech", "tense", "is_deuterocanon"])


def is_built() -> bool:
    return PARQUET_PATH.exists() or DB_PATH.exists()
