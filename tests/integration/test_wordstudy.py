"""Behavioral tests for bible_grammar.lexical.wordstudy (/word-study), requiring
real corpus data — data/processed/. Every expected value here was directly
observed by running the capability, not invented.
"""

import sys
import unicodedata
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.lexical.wordstudy import word_study

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestWordStudyOverview:
    def test_shalom_total_occurrences(self) -> None:
        # שָׁלוֹם (peace, H7965): observed 237 OT occurrences.
        _skip_if_missing()
        ws = word_study('H7965')
        assert ws['total_occurrences'] == 237

    def test_shalom_top_book_is_jeremiah(self) -> None:
        # by_book is in canonical book order, not frequency order — sort
        # to find the actual top book. Observed: Jeremiah 31 (13.1%).
        _skip_if_missing()
        ws = word_study('H7965')
        top = ws['by_book'].sort_values('count', ascending=False).iloc[0]
        assert top['book_id'] == 'Jer'
        assert top['count'] >= 28


class TestWordStudyMorphology:
    def test_shalom_is_overwhelmingly_absolute_noun(self) -> None:
        # Observed: Noun/Absolute 211 occurrences, 89.0% of all uses.
        _skip_if_missing()
        ws = word_study('H7965')
        top = ws['morphological_forms'].iloc[0]
        assert top['part_of_speech'] == 'Noun'
        assert top['state'] == 'Absolute'
        assert top['pct'] >= 85.0


class TestWordStudyTranslationEquivalents:
    def test_shalom_lxx_equivalent_is_eirene(self) -> None:
        # Word-level IBM Model 1 alignment (data/processed/word_alignment.parquet)
        # gives a clean, semantically correct primary equivalent (Greek "peace")
        # at 100% — the verse-level fallback alignment is noisier (articles,
        # function words) and should never be the observed top row here.
        # NFC-normalize before comparing — the corpus stores this lemma in a
        # polytonic (non-NFC) Unicode form.
        _skip_if_missing()
        ws = word_study('H7965')
        te = ws['translation_equivalents']
        top = te.iloc[0]
        assert unicodedata.normalize('NFC', top['lxx_lemma']) == unicodedata.normalize('NFC', 'εἰρήνη')
        assert top['lxx_strongs'] == 'G1515'
        assert top['pct'] >= 90.0
