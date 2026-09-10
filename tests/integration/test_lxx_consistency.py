"""Behavioral tests for bible_grammar.intertextuality.lxx_consistency
(/lxx-consistency), requiring real corpus data — the word-level Hebrew<->LXX
alignment (data/processed/word_alignment.parquet, built via
scripts/build_word_alignment.py).
"""

import sys
import unicodedata
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.intertextuality.lxx_consistency import lxx_consistency


def _nfc(s: str) -> str:
    return unicodedata.normalize('NFC', s)

_WORD_ALIGNMENT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "word_alignment.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORD_ALIGNMENT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORD_ALIGNMENT_PARQUET}")


class TestConsistentRendering:
    def test_shalom_is_perfectly_consistent(self) -> None:
        # שָׁלוֹם (peace, H7965) renders as εἰρήνη 100% of the time,
        # across every book with enough occurrences to measure — no
        # divergent books.
        _skip_if_missing()
        # NFC-normalize — the corpus stores these lemmas in a polytonic
        # (non-NFC) Unicode form.
        r = lxx_consistency('H7965')
        assert _nfc(r['corpus_primary']) == _nfc('εἰρήνη')
        assert r['overall_consistency'] == 100.0
        assert r['divergent_books'] == []
        assert r['total_aligned'] >= 100


class TestDivergentRendering:
    def test_tsedeq_diverges_in_deuteronomy_and_job(self) -> None:
        # צֶדֶק (righteousness, H6664) is a real example of inconsistent
        # LXX rendering — usually δικαιοσύνη (abstract noun) but rendered
        # as the adjective δίκαιος in Deuteronomy and Job. Observed:
        # corpus primary δικαιοσύνη at 60.9%, overall consistency 75.7%,
        # with Deu and Job flagged as divergent books.
        _skip_if_missing()
        r = lxx_consistency('H6664')
        assert _nfc(r['corpus_primary']) == _nfc('δικαιοσύνη')
        assert 50.0 <= r['corpus_primary_pct'] <= 70.0
        assert r['overall_consistency'] < 90.0
        assert set(r['divergent_books']) == {'Deu', 'Job'}

        by_book = {b['book_id']: b for b in r['books']}
        assert _nfc(by_book['Deu']['primary_lemma']) == _nfc('δίκαιος')
        assert by_book['Deu']['diverges'] is True
        assert _nfc(by_book['Job']['primary_lemma']) == _nfc('δίκαιος')
        assert by_book['Job']['diverges'] is True
        assert by_book['Isa']['diverges'] is False
