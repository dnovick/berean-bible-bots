"""Behavioral tests for bible_grammar.nt.nt_discourse, requiring real corpus
data — data/processed/macula_syntax.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).

Found and fixed a real bug while gathering ground truth for this file:
PARTICLE_REGISTRY keyed ἀλλά ("but") as '0235' (zero-padded), but the raw
`strong` column in the MACULA data stores it unpadded as '235' — every
other registry entry happens to be a 4-digit number that doesn't need
padding, so only this one particle was silently reported as 0 occurrences.
Fixed by dropping the leading zero to match the raw data format (see
nt_discourse.py's PARTICLE_REGISTRY).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt import nt_discourse as _mod
from bible_grammar.nt.nt_discourse import (
    nt_particle_frequency,
    nt_kai_profile,
    nt_particle_by_book,
    nt_particle_genre_profile,
    nt_hina_profile,
    nt_hoti_profile,
    nt_kai_by_book,
    nt_kai_instances,
    print_nt_particle_overview,
    print_nt_particle_frequency,
    print_nt_particle_genre_profile,
    print_nt_hina_profile,
    print_nt_hoti_profile,
    print_nt_kai_profile,
    nt_particle_frequency_chart,
    nt_particle_genre_heatmap,
    nt_particle_book_chart,
    nt_kai_function_chart,
    nt_kai_book_heatmap,
)

_SYNTAX_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _SYNTAX_PARQUET.exists():
        pytest.skip(f"Data file not found: {_SYNTAX_PARQUET}")


class TestParticleFrequency:
    def test_kai_dominates(self) -> None:
        # καί ("and") is the NT's most common particle by a wide margin.
        # Observed: count 8978, 47.0%.
        _skip_if_missing()
        df = nt_particle_frequency()
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['lemma'] == 'καί'
        assert top['count'] >= 8500

    def test_alla_is_not_zero(self) -> None:
        # Regression guard for the PARTICLE_REGISTRY '0235' vs '235' bug
        # described in this file's module docstring. Observed: count 638.
        _skip_if_missing()
        df = nt_particle_frequency()
        alla = df[df['lemma'] == 'ἀλλά'].iloc[0]
        assert alla['count'] >= 600


class TestKaiProfile:
    def test_additive_is_the_dominant_function(self) -> None:
        # Observed: additive (plain coordination) 8060 tokens, 89.8% —
        # by far καί's most common discourse function.
        _skip_if_missing()
        df = nt_kai_profile()
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['function'] == 'additive'
        assert top['pct'] >= 85.0


class TestParticleByBook:
    def test_luke_has_the_most_particle_tokens(self) -> None:
        # Observed: Luk 2,760 particle tokens, the most of any NT book.
        _skip_if_missing()
        ct = nt_particle_by_book()
        totals = ct.sum(axis=1)
        assert totals.idxmax() == 'Luk'
        assert totals.max() >= 2500


class TestParticleGenreProfile:
    def test_general_and_revelation_has_the_highest_kai_pct(self) -> None:
        # Observed: 'General & Rev' καί=59.2% vs. 'Pauline' καί=33.1% —
        # Pauline epistles favor δέ/γάρ-style subordination over plain καί
        # coordination.
        _skip_if_missing()
        df = nt_particle_genre_profile()
        assert df.loc['General & Rev', 'καί'] >= 50.0
        assert df.loc['General & Rev', 'καί'] > df.loc['Pauline', 'καί']


class TestHinaProfile:
    def test_purpose_dominates_whole_nt(self) -> None:
        # Observed: purpose 593 (88.6%) of all ἵνα tokens.
        _skip_if_missing()
        df = nt_hina_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['pct'] >= 80.0


class TestHotiProfile:
    def test_recitative_and_causal_dominate(self) -> None:
        # Observed: recitative 529 (40.9%), causal 383 (29.6%), content 381
        # (29.5%) — roughly a three-way split.
        _skip_if_missing()
        df = nt_hoti_profile()
        top2_pct = df.sort_values('pct', ascending=False).head(2)['pct'].sum()
        assert top2_pct >= 60.0


class TestKaiByBook:
    def test_additive_dominates_every_book_column_total(self) -> None:
        # Observed: additive column total 8,060, far above the next
        # (adjunctive 684).
        _skip_if_missing()
        ct = nt_kai_by_book()
        totals = ct.sum(axis=0)
        assert totals.idxmax() == 'additive'
        assert totals.max() >= 7500


class TestKaiInstances:
    def test_default_matches_total_kai_count(self) -> None:
        # Observed: default (no function/book filter) returns 8,978 rows,
        # matching the raw καί token count.
        _skip_if_missing()
        df = nt_kai_instances()
        assert len(df) >= 8500
        assert 'ref' in df.columns and 'gloss' in df.columns

    def test_ascensive_filter_returns_a_real_subset(self) -> None:
        # Observed: function='ascensive' returns 118 rows, a proper subset
        # of the full 8,978.
        _skip_if_missing()
        df = nt_kai_instances(function='ascensive')
        assert 50 <= len(df) < 500


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_nt_particle_overview,
            print_nt_particle_frequency,
            print_nt_particle_genre_profile,
            print_nt_hina_profile,
            print_nt_hoti_profile,
            print_nt_kai_profile,
        )
        for fn in fns:
            capsys.readouterr()
            fn()
            out = capsys.readouterr().out
            assert len(out.strip()) > 50, f"{fn.__name__} produced no real output"


class TestChartFunctions:
    def test_chart_functions_produce_real_pngs(self, tmp_path, monkeypatch) -> None:
        _skip_if_missing()
        monkeypatch.setattr(_mod, '_CHART_DIR', tmp_path)
        fns = (
            nt_particle_frequency_chart,
            nt_particle_genre_heatmap,
            nt_particle_book_chart,
            nt_kai_function_chart,
            nt_kai_book_heatmap,
        )
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn.__name__} returned None"
            assert Path(out).exists(), f"{fn.__name__} did not write a file"
            assert Path(out).stat().st_size > 0
