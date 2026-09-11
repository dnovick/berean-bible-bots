"""Behavioral tests for bible_grammar.reporting.profiles, requiring real
corpus data — data/processed/words.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.reporting.profiles import book_profile

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestBookProfile:
    def test_genesis_profile(self) -> None:
        # Observed: 20,614 total words, 2,060 unique Strong's numbers,
        # 811 hapax legomena, type-token ratio 0.1. Top lemma is H0853,
        # the untranslatable direct-object marker אֵת — expected, since
        # it's the single most common "word" in Hebrew narrative prose
        # despite carrying no independent meaning of its own.
        _skip_if_missing()
        p = book_profile('Gen')
        assert p['book_id'] == 'Gen'
        assert p['testament'] == 'OT'
        assert p['total_words'] >= 20000
        assert p['unique_strongs'] >= 2000
        assert p['hapax_count'] >= 750
        top_lemma = max(p['top_lemmas'], key=p['top_lemmas'].get)
        assert top_lemma == 'H0853'
