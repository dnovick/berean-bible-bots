"""Behavioral tests for bible_grammar.lexical.termmap (/term-map), requiring
the word-level Hebrew<->LXX alignment (data/processed/word_alignment.parquet,
built via scripts/build_word_alignment.py).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.lexical.termmap import term_map, THEOLOGICAL_TERMS

_WORD_ALIGNMENT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "word_alignment.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORD_ALIGNMENT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORD_ALIGNMENT_PARQUET}")


class TestTermMapSingleRoot:
    def test_shalom_row(self) -> None:
        # Observed: ot_count 237, primary LXX equivalent G1515 (eirene)
        # at 100%, appearing 92 times in the NT.
        _skip_if_missing()
        df = term_map('H7965')
        row = df.iloc[0]
        assert row['ot_count'] == 237
        assert row['lxx_strongs_1'] == 'G1515'
        assert row['lxx_pct_1'] == 100.0
        assert row['lxx_nt_count_1'] >= 80


class TestTermMapDefault:
    def test_default_covers_all_themes(self) -> None:
        # With no argument, term_map() builds the full THEOLOGICAL_TERMS
        # table — one row per Hebrew root, grouped under 20 themes.
        _skip_if_missing()
        df = term_map()
        assert set(df['theme']) == set(THEOLOGICAL_TERMS.keys())
        assert len(df) >= 40
