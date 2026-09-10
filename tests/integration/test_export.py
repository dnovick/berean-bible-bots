"""Behavioral tests for bible_grammar.reporting.export (/export), requiring
real corpus data — data/processed/. Writes to output/exports/ (gitignored),
the same location the capability writes to in normal use.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.reporting.export import export_word_study

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestExportWordStudy:
    def test_shalom_export_produces_all_four_files(self) -> None:
        # export_word_study returns real, on-disk paths for HTML plus three
        # CSVs (by-book, morphology, collocates). The collocates CSV
        # requires collocations() to actually return data — before the
        # collocation.py homonym-letter fix this key was always None for
        # Hebrew OT words (see test_collocation.py).
        _skip_if_missing()
        result = export_word_study('H7965')
        for key in ('html', 'csv_by_book', 'csv_morphology', 'csv_collocates'):
            path = result[key]
            assert path is not None, f"{key} was not generated"
            assert path.exists(), f"{key} path does not exist on disk: {path}"
