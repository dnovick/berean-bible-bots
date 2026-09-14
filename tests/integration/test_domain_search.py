"""Behavioral tests for bible_grammar.lexical.domain_search (/domain-search),
requiring real corpus data — data/processed/macula_syntax.parquet (MACULA
Greek NT with Louw-Nida domain codes).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.lexical.domain_search import (
    query_domain, top_domain_words, domain_profile,
    domain_role_search, domain_comparison,
    print_domain_summary, print_domain_role,
)

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


class TestDomainRoleSearch:
    def test_jesus_as_subject_of_communication_verbs_is_lego(self) -> None:
        # Jesus (G2424) as subject of Communication-domain (33) words:
        # λέγω ("say") dominates every gloss variant. Observed: top row
        # (gloss "I say") count 114.
        _skip_if_missing()
        df = domain_role_search(33, 'G2424', top_n=5)
        top = df.iloc[0]
        assert top['lemma'] == 'λέγω'
        assert top['strong_g'] == 'G3004'
        assert top['count'] >= 100


class TestDomainComparison:
    def test_communication_leads_both_romans_and_revelation(self) -> None:
        # Cross-check against TestDomainProfile: Communication (33) is the
        # top content-word domain in both Romans (11.5%) and Revelation
        # (8.8%, matching the single-book test above).
        _skip_if_missing()
        df = domain_comparison(['Rom', 'Rev'], top_n=5)
        top_label = df['Rom'].idxmax()
        assert top_label == '33: Communication'
        assert df.loc[top_label, 'Rom'] >= 10.0
        assert df.loc[top_label, 'Rev'] >= 7.0


class TestPrintDomainSummary:
    def test_prints_real_output(self, capsys) -> None:
        _skip_if_missing()
        print_domain_summary(12, top_n=5)
        out = capsys.readouterr().out
        assert 'θεός' in out
        assert len(out.strip()) > 100


class TestPrintDomainRole:
    def test_prints_real_output(self, capsys) -> None:
        _skip_if_missing()
        print_domain_role(33, 'G2424', top_n=5)
        out = capsys.readouterr().out
        assert 'λέγω' in out
        assert len(out.strip()) > 100
