"""Behavioral tests for bible_grammar.nt.nt_louw_nida, requiring real corpus
data — data/processed/macula_syntax.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt.nt_louw_nida import nt_ln_data, nt_ln_subdomain_frequency, nt_ln_top_lemmas

_SYNTAX_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _SYNTAX_PARQUET.exists():
        pytest.skip(f"Data file not found: {_SYNTAX_PARQUET}")


class TestLnData:
    def test_domain_12_total_matches_domain_search(self) -> None:
        # Cross-verification: this is a second, independent code path over
        # the same Louw-Nida domain data queried by domain_search.py's
        # query_domain() (tests/integration/test_domain_search.py) — both
        # should agree exactly on domain 12 (Supernatural Beings and
        # Powers). Observed: 3,127 tokens in both.
        _skip_if_missing()
        df = nt_ln_data(domain=12)
        assert len(df) >= 3000


class TestLnSubdomainFrequency:
    def test_theos_subdomain_leads_domain_12(self) -> None:
        # Subdomain 12.1 (θεός/God) is domain 12's largest subdomain.
        # Observed: count 1247, 39.8%.
        _skip_if_missing()
        df = nt_ln_subdomain_frequency(12, top_n=5)
        top = df.iloc[0]
        assert top['subdomain'] == '12.1'
        assert top['top_lemma'] == 'θεός'
        assert top['pct'] >= 35.0


class TestLnTopLemmas:
    def test_theos_is_the_lemma_for_subdomain_12_1(self) -> None:
        _skip_if_missing()
        df = nt_ln_top_lemmas('12.1', top_n=5)
        top = df.iloc[0]
        assert top['lemma'] == 'θεός'
        assert top['strong_g'] == 'G2316'
        assert top['count'] >= 600
