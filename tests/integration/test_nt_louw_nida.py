"""Behavioral tests for bible_grammar.nt.nt_louw_nida, requiring real corpus
data — data/processed/macula_syntax.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt import nt_louw_nida as _mod
from bible_grammar.nt.nt_louw_nida import (
    nt_ln_data,
    nt_ln_subdomain_frequency,
    nt_ln_top_lemmas,
    nt_ln_book_distribution,
    nt_ln_genre_profile,
    nt_ln_domain_breakdown,
    nt_ln_comparison,
    print_nt_ln_overview,
    print_nt_ln_subdomain_frequency,
    print_nt_ln_top_lemmas,
    print_nt_ln_book_distribution,
    print_nt_ln_domain_breakdown,
    print_nt_ln_comparison,
    nt_ln_subdomain_chart,
    nt_ln_book_chart,
    nt_ln_genre_heatmap,
)

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


class TestLnBookDistribution:
    def test_acts_and_romans_lead_subdomain_12_1(self) -> None:
        # Observed: Act leads with 154 (12.3%), Rom close second 151 (12.1%).
        _skip_if_missing()
        df = nt_ln_book_distribution('12.1')
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['book'] == 'Act'
        assert top['count'] >= 130


class TestLnGenreProfile:
    def test_pauline_leads_subdomain_12_1(self) -> None:
        # Observed: Pauline 535 (42.9%), Gospels & Acts 428 (34.3%).
        _skip_if_missing()
        df = nt_ln_genre_profile('12.1').set_index('genre')
        assert df.loc['Pauline', 'pct'] >= 35.0


class TestLnDomainBreakdown:
    def test_matches_subdomain_frequency(self) -> None:
        # nt_ln_domain_breakdown is a thin wrapper around
        # nt_ln_subdomain_frequency — verify they agree exactly.
        _skip_if_missing()
        breakdown = nt_ln_domain_breakdown(12, top_n=5)
        direct = nt_ln_subdomain_frequency(12, top_n=5)
        assert breakdown.equals(direct)


class TestLnComparison:
    def test_romans_has_the_highest_subdomain_12_1_pct(self) -> None:
        # Observed: row '12.1' — Rom=61.9%, 1Co=46.2%, Jhn=23.6% — Romans'
        # heavy theological vocabulary drives this far above the Gospel.
        _skip_if_missing()
        df = nt_ln_comparison(['Rom', '1Co', 'Jhn'], 12, top_n=5)
        row = df.loc['12.1']
        assert row['Rom'] >= 50.0
        assert row['Rom'] > row['Jhn']


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_nt_ln_overview,
            lambda: print_nt_ln_subdomain_frequency(12),
            lambda: print_nt_ln_top_lemmas('12.1'),
            lambda: print_nt_ln_book_distribution('12.1'),
            lambda: print_nt_ln_domain_breakdown(12),
            lambda: print_nt_ln_comparison(['Rom', '1Co', 'Jhn'], 12),
        )
        for fn in fns:
            capsys.readouterr()
            fn()
            out = capsys.readouterr().out
            assert len(out.strip()) > 50, f"{fn} produced no real output"


class TestChartFunctions:
    def test_chart_functions_produce_real_pngs(self, tmp_path, monkeypatch) -> None:
        _skip_if_missing()
        monkeypatch.setattr(_mod, '_CHART_DIR', tmp_path)
        fns = (
            lambda: nt_ln_subdomain_chart(12),
            lambda: nt_ln_book_chart('12.1'),
            lambda: nt_ln_genre_heatmap([12]),
        )
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn} returned None"
            assert Path(out).exists(), f"{fn} did not write a file"
            assert Path(out).stat().st_size > 0
