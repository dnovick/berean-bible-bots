"""Behavioral tests for bible_grammar.lexical.wordstudy (/word-study), requiring
real corpus data — data/processed/. Every expected value here was directly
observed by running the capability, not invented.
"""

import sys
import unicodedata
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.lexical.wordstudy import (
    word_study, resolve_strongs, print_word_study, word_study_table,
)

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


class TestResolveStrongs:
    def test_direct_strongs_number_passes_through(self) -> None:
        _skip_if_missing()
        assert resolve_strongs('H7965') == 'H7965'

    def test_hebrew_lemma_resolves(self) -> None:
        _skip_if_missing()
        assert resolve_strongs('שָׁלוֹם') == 'H7965'

    def test_greek_lemma_resolves(self) -> None:
        _skip_if_missing()
        assert resolve_strongs('εἰρήνη') == 'G1515'

    def test_unknown_term_returns_none(self) -> None:
        _skip_if_missing()
        assert resolve_strongs('not_a_real_word_xyz') is None


class TestPrintWordStudy:
    def test_prints_real_output(self, capsys) -> None:
        _skip_if_missing()
        print_word_study('H7965')
        out = capsys.readouterr().out
        assert 'H7965' in out
        assert '237' in out
        assert len(out.strip()) > 200


class TestWordStudyTable:
    def test_returns_one_row_per_occurrence_with_context(self) -> None:
        # Same total as TestWordStudyOverview (237), reshaped into one row
        # per occurrence with KJV context text.
        _skip_if_missing()
        df = word_study_table('H7965')
        assert len(df) == 237
        for col in ('reference', 'book_id', 'word', 'context_text'):
            assert col in df.columns
        assert (df['book_id'] == 'Gen').sum() == 15
