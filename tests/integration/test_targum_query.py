"""Behavioral tests for bible_grammar.core.targum_query. The FileNotFoundError
path needs no data and always runs; the happy-path filtering tests need
data/processed/targum.parquet (built by scripts/fetch_targum_data.py, a live
Sefaria API fetch — not run automatically, so these skip if absent).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.core.targum_query import load_targum, COVERAGE

_TARGUM_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "targum.parquet"
)


def _skip_if_missing() -> None:
    if not _TARGUM_PARQUET.exists():
        pytest.skip(f"Data file not found: {_TARGUM_PARQUET}")


class TestLoadTargumMissingData:
    def test_raises_file_not_found_with_a_helpful_message(self, monkeypatch) -> None:
        # This test needs no real data — it verifies the real, unconditional
        # behavior when the cache is absent, by pointing _PARQUET at a path
        # that never exists.
        import bible_grammar.core.targum_query as _mod
        monkeypatch.setattr(_mod, '_PARQUET', Path('/nonexistent/targum.parquet'))
        with pytest.raises(FileNotFoundError, match='fetch_targum_data.py'):
            load_targum()


@pytest.mark.integration
class TestLoadTargumRealData:
    def test_every_row_belongs_to_a_book_declared_in_coverage(self) -> None:
        # Structural regression guard: every (targum, book_id) pair in the
        # real cached data must be one this module's own COVERAGE dict
        # declares — catches a fetch script drifting out of sync with the
        # documented coverage.
        _skip_if_missing()
        df = load_targum()
        assert not df.empty
        for targum, books in COVERAGE.items():
            sub = df[df['targum'] == targum]
            assert set(sub['book_id'].unique()) <= set(books)

    def test_filtering_by_targum_and_book_narrows_correctly(self) -> None:
        _skip_if_missing()
        onkelos_gen = load_targum('Onkelos', 'Gen')
        assert not onkelos_gen.empty
        assert (onkelos_gen['targum'] == 'Onkelos').all()
        assert (onkelos_gen['book_id'] == 'Gen').all()

    def test_filtering_to_an_uncovered_book_returns_empty(self) -> None:
        # Rev isn't in any COVERAGE list — filtering to it must return an
        # empty (not missing-key-error) result.
        _skip_if_missing()
        result = load_targum('Onkelos', 'Rev')
        assert result.empty
