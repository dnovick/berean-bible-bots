"""Behavioral tests for bible_grammar.ot.ot_discourse, requiring real corpus
data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot.ot_discourse import ot_discourse_wayyiqtol_density

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestWayyiqtolDensity:
    def test_genesis_has_50_chapters_and_real_wayyiqtol_counts(self) -> None:
        # Observed: 50 chapters, 2,105 total wayyiqtol tokens across the book.
        _skip_if_missing()
        df = ot_discourse_wayyiqtol_density('Gen')
        assert len(df) == 50
        assert df['wayyiqtol_count'].sum() >= 2000
        assert (df['density'] >= 0).all()
        assert (df['density'] <= 100).all()
