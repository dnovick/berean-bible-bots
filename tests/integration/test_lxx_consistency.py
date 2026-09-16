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

from bible_grammar.intertextuality.lxx_consistency import (
    lxx_consistency,
    print_lxx_consistency,
    consistency_heatmap,
    batch_consistency,
)


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


class TestPrintLxxConsistency:
    def test_prints_real_output_with_divergent_books(self, capsys) -> None:
        _skip_if_missing()
        print_lxx_consistency('H6664')
        out = capsys.readouterr().out
        assert _nfc('δικαιοσύνη') in _nfc(out)
        assert 'Deu' in out
        assert 'Job' in out

    def test_no_alignment_data_prints_a_clear_message(self, capsys) -> None:
        # An invalid/unresolvable Strong's number should hit the
        # total_aligned == 0 branch and print a clear message, not crash.
        _skip_if_missing()
        print_lxx_consistency('H99999')
        out = capsys.readouterr().out
        assert 'No word-level alignment data found' in out


class TestConsistencyHeatmap:
    def test_produces_a_real_png_for_multiple_roots(self, tmp_path: Path) -> None:
        _skip_if_missing()
        out_path = str(tmp_path / 'heatmap.png')
        consistency_heatmap(['H7965', 'H6664'], output_path=out_path)
        assert Path(out_path).exists()
        assert Path(out_path).stat().st_size > 0

    def test_single_root_string_input_also_works(self, tmp_path: Path) -> None:
        _skip_if_missing()
        out_path = str(tmp_path / 'single.png')
        consistency_heatmap('H7965', output_path=out_path)
        assert Path(out_path).exists()


class TestBatchConsistency:
    def test_shalom_and_tsedeq_summary_matches_individual_results(self) -> None:
        # batch_consistency() is a thin wrapper around lxx_consistency() —
        # verify its summary row values agree with the individual calls
        # already verified above, and that it's sorted by consistency
        # descending (שָׁלוֹם at 100% ahead of צֶדֶק at ~75.7%).
        _skip_if_missing()
        df = batch_consistency(['H6664', 'H7965'])
        assert list(df['strongs']) == ['H7965', 'H6664']
        shalom_row = df[df['strongs'] == 'H7965'].iloc[0]
        assert shalom_row['overall_consistency'] == 100.0
        assert shalom_row['n_divergent_books'] == 0
        tsedeq_row = df[df['strongs'] == 'H6664'].iloc[0]
        assert tsedeq_row['n_divergent_books'] == 2
