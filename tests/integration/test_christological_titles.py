"""Behavioral tests for bible_grammar.names.christological_titles
(/christological-titles), requiring real corpus data — data/processed/words.parquet.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.names.christological_titles import title_counts

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestTitleCountsGospels:
    def test_son_of_man_is_high_confidence_and_frequent(self) -> None:
        # "Son of Man" (ὁ υἱὸς τοῦ ἀνθρώπου) is Jesus's own most
        # characteristic self-designation in the Gospels — the paradigm
        # high-confidence self-referential title. Observed: 88 occurrences.
        _skip_if_missing()
        df = title_counts(scope='gospels')
        row = df[df['title'] == 'Son of Man'].iloc[0]
        assert row['confidence'] == 'high'
        assert row['Total'] >= 80

    def test_kyrios_is_the_most_frequent_title(self) -> None:
        # "Lord" (κύριος) is the single most common title applied to
        # Jesus in the Gospels, though low self-reference confidence
        # (it's mostly applied by others, not self-claimed).
        _skip_if_missing()
        df = title_counts(scope='gospels')
        top = df.sort_values('Total', ascending=False).iloc[0]
        assert top['title'] == 'Lord (Kyrios)'
        assert top['Total'] >= 200
