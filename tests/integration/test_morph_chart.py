"""Behavioral tests for bible_grammar.lexical.morph_chart (/morph-chart),
requiring real corpus data — data/processed/.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.lexical.morph_chart import morph_distribution

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestMorphDistributionNoun:
    def test_shalom_dimensions_are_pos_and_state(self) -> None:
        # שָׁלוֹם (peace, H7965) is a noun — its two morphological
        # dimensions are part-of-speech and grammatical state, not stem/conj.
        _skip_if_missing()
        d = morph_distribution('H7965')
        assert d['pos'] == 'Noun'
        assert d['dim2'] == 'part_of_speech'


class TestMorphDistributionVerb:
    def test_bara_dimensions_are_stem_and_conjugation(self) -> None:
        # בָּרָא (create, H1254) is a verb — dimensions are stem × conjugation.
        # Observed: 32 total tokens across the pivot table, Isaiah's Qal
        # Participle the single largest cell (10).
        _skip_if_missing()
        d = morph_distribution('H1254')
        assert d['pos'] == 'Verb'
        assert d['dim1'] == 'stem'
        assert d['dim2'] == 'conjugation'
        pivot = d['pivot']
        assert int(pivot.values.sum()) == 32
        assert int(pivot.loc['Isaiah', 'Qal Participle']) == 10
