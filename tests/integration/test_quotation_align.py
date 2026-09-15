"""Behavioral tests for bible_grammar.intertextuality.quotation_align,
requiring the scrollmapper cross-reference data (a git submodule) plus real
corpus data — data/processed/words.parquet, lxx.parquet, and
word_alignment.parquet.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.intertextuality.quotation_align import (
    quotation_align, print_quotation_align, batch_align,
)

_XREF_FILE = (
    Path(__file__).resolve().parents[2] / "scrollmapper-data" / "sources_backup"
    / "extras" / "cross_references.txt"
)
_WORD_ALIGNMENT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "word_alignment.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _XREF_FILE.exists():
        pytest.skip(f"Data file not found: {_XREF_FILE}")
    if not _WORD_ALIGNMENT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORD_ALIGNMENT_PARQUET}")


class TestQuotationAlign:
    def test_matthew_4_4_deuteronomy_8_3_follows_lxx(self) -> None:
        # Observed: Mat 4:4 has 10 OT cross-references; the top-voted one
        # (Deu 8:3, 349 votes) is classified 'follows LXX' at 75% content
        # words following the LXX rendering.
        _skip_if_missing()
        results = quotation_align('Mat', 4, 4)
        assert len(results) >= 8
        top = max(results, key=lambda r: r['votes'])
        assert top['ot_ref'] == 'Deu 8:3'
        assert top['summary'] == 'follows LXX'
        assert top['lxx_following_pct'] >= 60.0

    def test_verse_with_no_quotations_returns_empty_list(self) -> None:
        # Genesis 1:1 has no NT cross-references at all (it's OT, not NT).
        _skip_if_missing()
        assert quotation_align('Gen', 1, 1) == []


class TestPrintQuotationAlign:
    def test_prints_real_output(self, capsys) -> None:
        _skip_if_missing()
        print_quotation_align('Mat', 4, 4)
        out = capsys.readouterr().out
        assert 'Deu 8:3' in out
        assert len(out.strip()) > 200


class TestBatchAlign:
    def test_hebrews_high_vote_quotations_are_mt_leaning(self) -> None:
        # Observed: batch_align(nt_book='Heb', min_votes=50) returns 67
        # rows; the top-voted pair (Heb 8:10 -> Ezk 36:26, 321 votes) is
        # classified 'MT-leaning'.
        _skip_if_missing()
        df = batch_align(nt_book='Heb', min_votes=50)
        assert len(df) >= 50
        top = df.sort_values('votes', ascending=False).iloc[0]
        assert top['nt_ref'] == 'Heb 8:10'
        assert top['ot_ref'] == 'Ezk 36:26'
        assert top['summary'] == 'MT-leaning'
