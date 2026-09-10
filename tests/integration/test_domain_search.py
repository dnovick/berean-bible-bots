"""Behavioral tests for bible_grammar.lexical.domain_search (/domain-search),
requiring real corpus data — data/processed/macula_syntax.parquet (MACULA
Greek NT with Louw-Nida domain codes).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.lexical.domain_search import query_domain, top_domain_words, domain_profile

_SYNTAX_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _SYNTAX_PARQUET.exists():
        pytest.skip(f"Data file not found: {_SYNTAX_PARQUET}")


class TestQueryDomain:
    def test_supernatural_beings_domain_total(self) -> None:
        # Louw-Nida domain 12 (Supernatural Beings and Powers): observed
        # 3,127 NT tokens.
        _skip_if_missing()
        df = query_domain(12)
        assert len(df) >= 3000


class TestTopDomainWords:
    def test_theos_leads_supernatural_beings_domain(self) -> None:
        # θεός (God, G2316) is by far the most frequent lemma in domain 12.
        # Observed: 682 occurrences under gloss "God" alone.
        _skip_if_missing()
        df = top_domain_words(12, top_n=5)
        top = df.iloc[0]
        assert top['lemma'] == 'θεός'
        assert top['strong_g'] == 'G2316'
        assert top['count'] >= 600


class TestDomainProfile:
    def test_revelation_top_domain_is_communication(self) -> None:
        # Revelation's most frequent content-word domain is Communication
        # (33) — driven by its heavy use of speech/proclamation verbs.
        # Observed: 389 tokens, 8.8% of the book's domain-tagged vocabulary.
        _skip_if_missing()
        df = domain_profile('Rev', top_n=5)
        top = df.iloc[0]
        assert top['domain_num'] == 33
        assert top['domain_name'] == 'Communication'
        assert top['pct'] >= 7.0
