"""Behavioral tests for bible_grammar.nt.nt_participles, requiring real
corpus data — data/processed/macula_syntax.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4;
broadened under issue #676 Phase 3).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt import nt_participles as _mod
from bible_grammar.nt.nt_participles import (
    nt_participle_data,
    nt_participle_top_lemmas,
    nt_participle_tense_profile,
    nt_participle_voice_profile,
    nt_participle_tense_voice,
    nt_participle_role_profile,
    nt_participle_book_distribution,
    nt_participle_genre_profile,
    nt_genitive_absolutes,
    nt_perfect_participles,
    print_nt_participle_overview,
    print_nt_participle_tense,
    print_nt_participle_voice,
    print_nt_participle_tense_voice,
    print_nt_participle_role,
    print_nt_participle_top_lemmas,
    print_nt_participle_genre_profile,
    print_nt_genitive_absolutes,
    print_nt_perfect_participles,
    print_nt_participle_book_distribution,
    nt_participle_tense_chart,
    nt_participle_genre_heatmap,
    nt_participle_book_chart,
)

_SYNTAX_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _SYNTAX_PARQUET.exists():
        pytest.skip(f"Data file not found: {_SYNTAX_PARQUET}")


class TestParticiples:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(nt_participle_data()) >= 6400   # observed: 6,653

    def test_lego_is_top_lemma(self) -> None:
        # λέγω ("saying") is the NT's most frequent participle lemma —
        # the standard way of introducing direct speech. Observed: count
        # 494, present tense.
        _skip_if_missing()
        df = nt_participle_top_lemmas(5)
        top = df.iloc[0]
        assert top['lemma'] == 'λέγω'
        assert top['top_tense'] == 'present'
        assert top['count'] >= 450

    def test_present_dominates_tense_profile(self) -> None:
        # Observed: present 3,688 (55.4%), aorist 2,275 (34.2%).
        _skip_if_missing()
        df = nt_participle_tense_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'present'
        assert top['pct'] >= 45.0

    def test_active_dominates_voice_profile(self) -> None:
        # Observed: active 4,493 (67.5%).
        _skip_if_missing()
        df = nt_participle_voice_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'active'
        assert top['pct'] >= 60.0

    def test_present_active_is_top_tense_voice_cell(self) -> None:
        # Observed: present/active 2,675, the largest cell.
        _skip_if_missing()
        df = nt_participle_tense_voice()
        assert df.loc['present', 'active'] >= 2500
        assert df.loc['present', 'active'] == df.values.max()

    def test_main_verb_position_dominates_role_profile(self) -> None:
        # Observed: "main verb position" (role 'v') 6,045 (90.9%) —
        # circumstantial/adverbial participles dominate over adjectival or
        # substantival uses in this corpus's role tagging.
        _skip_if_missing()
        df = nt_participle_role_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['role'] == 'main verb position'
        assert top['pct'] >= 80.0

    def test_acts_has_the_most_participle_tokens(self) -> None:
        # Observed: Act 1,280 participle tokens (19.2% of all GNT
        # participles, 32.2% of that book's verbal tokens).
        _skip_if_missing()
        df = nt_participle_book_distribution()
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['book'] == 'Act'
        assert top['count'] >= 1200

    def test_gospels_and_acts_favor_present_in_genre_profile(self) -> None:
        # Observed: Gospels & Acts present 48.3%, aorist 42.7%.
        _skip_if_missing()
        df = nt_participle_genre_profile()
        assert df.loc['Gospels & Acts', 'present'] >= 40.0

    def test_genitive_absolutes_returns_real_rows(self) -> None:
        # Observed: 738 genitive absolute constructions across the GNT.
        _skip_if_missing()
        df = nt_genitive_absolutes()
        assert len(df) >= 700
        assert 'lemma' in df.columns

    def test_perfect_participles_oida_is_a_top_lemma(self) -> None:
        # Observed: 677 perfect participle tokens total; οἶδα (53) is the
        # most frequent lemma — perfect-only ("to know", stative) verb.
        _skip_if_missing()
        df = nt_perfect_participles()
        assert len(df) >= 650
        top_lemma = df['lemma'].value_counts().idxmax()
        assert top_lemma == 'οἶδα'


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_nt_participle_overview,
            print_nt_participle_tense,
            print_nt_participle_voice,
            print_nt_participle_tense_voice,
            print_nt_participle_role,
            print_nt_participle_top_lemmas,
            print_nt_participle_genre_profile,
            print_nt_genitive_absolutes,
            print_nt_perfect_participles,
            print_nt_participle_book_distribution,
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
        fns = (nt_participle_tense_chart, nt_participle_genre_heatmap, nt_participle_book_chart)
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn.__name__} returned None"
            assert Path(out).exists(), f"{fn.__name__} did not write a file"
            assert Path(out).stat().st_size > 0
