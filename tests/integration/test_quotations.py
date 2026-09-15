"""Behavioral tests for bible_grammar.intertextuality.quotations, requiring
the scrollmapper cross-reference data (a git submodule) plus real corpus
data — data/processed/words.parquet.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.intertextuality.quotations import (
    nt_quotations, verse_comparison, quotation_table, quotation_summary,
)

_XREF_FILE = (
    Path(__file__).resolve().parents[2] / "scrollmapper-data" / "sources_backup"
    / "extras" / "cross_references.txt"
)
_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _XREF_FILE.exists():
        pytest.skip(f"Data file not found: {_XREF_FILE}")
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestNtQuotations:
    def test_romans_8_29_jeremiah_1_5_is_the_top_vote_pair(self) -> None:
        # Observed: Rom 8:29 -> Jer 1:5 has 1,143 votes, the single most
        # attested NT->OT cross-reference at min_votes=50 (481 pairs total).
        _skip_if_missing()
        df = nt_quotations(min_votes=50)
        assert len(df) >= 400
        top = df.sort_values('votes', ascending=False).iloc[0]
        assert top['nt_book'] == 'Rom'
        assert top['ot_book'] == 'Jer'
        assert top['votes'] >= 1000


class TestVerseComparison:
    def test_hebrews_2_8_cites_psalm_8_and_daniel_7(self) -> None:
        # Observed: Heb 2:8 has 2 OT cross-references — Psa 8:6 (7 votes)
        # and Dan 7:14 (5 votes) — each with real nt/ot_words/lxx_words.
        _skip_if_missing()
        cmp = verse_comparison('Heb', 2, 8)
        assert cmp['nt_ref'] == 'Heb 2:8'
        assert len(cmp['nt']) > 0
        ot_refs = {r['ot_ref'] for r in cmp['refs']}
        assert 'Psa 8:6' in ot_refs
        assert 'Dan 7:14' in ot_refs
        psa_ref = next(r for r in cmp['refs'] if r['ot_ref'] == 'Psa 8:6')
        assert len(psa_ref['ot_words']) > 0
        assert len(psa_ref['lxx_words']) > 0


class TestQuotationTable:
    def test_hebrews_2_8_table_matches_verse_comparison(self) -> None:
        _skip_if_missing()
        df = quotation_table('Heb', 2, 8, min_votes=5)
        assert len(df) == 2
        assert set(df['ot_ref']) == {'Psa 8:6', 'Dan 7:14'}


class TestQuotationSummary:
    def test_matthew_has_the_most_quotations(self) -> None:
        # Observed: Matthew leads with 86 total references at min_votes=50,
        # mostly sourced from Psalms.
        _skip_if_missing()
        df = quotation_summary(min_votes=50)
        top = df.sort_values('total_references', ascending=False).iloc[0]
        assert top['nt_book'] == 'Mat'
        assert top['total_references'] >= 70
