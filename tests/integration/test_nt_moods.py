"""Behavioral tests for bible_grammar.nt.nt_moods, requiring real corpus
data — data/processed/macula_syntax.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4;
broadened under issue #676 Phase 3).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt import nt_moods as _mod
from bible_grammar.nt.nt_moods import (
    nt_mood_data,
    nt_mood_profile,
    nt_subjunctive_profile,
    nt_infinitive_profile,
    nt_imperative_profile,
    nt_subjunctive_constructions,
    nt_infinitive_constructions,
    nt_imperative_tense_comparison,
    nt_mood_genre_profile,
    nt_mood_book_distribution,
    print_nt_mood_overview,
    print_nt_subjunctive_profile,
    print_nt_infinitive_profile,
    print_nt_imperative_profile,
    print_nt_subjunctive_constructions,
    print_nt_infinitive_constructions,
    print_nt_imperative_tense_comparison,
    print_nt_mood_genre_profile,
    nt_mood_chart,
    nt_subjunctive_chart,
    nt_imperative_chart,
    nt_mood_genre_heatmap,
)

_SYNTAX_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _SYNTAX_PARQUET.exists():
        pytest.skip(f"Data file not found: {_SYNTAX_PARQUET}")


class TestMoodProfile:
    def test_indicative_dominates(self) -> None:
        # The indicative (statement of fact) is the NT's overwhelmingly
        # dominant mood/form — narrative and epistolary prose alike.
        # Observed: 15,617 tokens, 55.1%.
        _skip_if_missing()
        df = nt_mood_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'indicative'
        assert top['pct'] >= 50.0


class TestSubjunctiveProfile:
    def test_aorist_active_is_top_cell(self) -> None:
        # Observed: aorist/active count 948, the largest single cell in
        # the tense x voice crosstab.
        _skip_if_missing()
        df = nt_subjunctive_profile()
        assert df.loc['aorist', 'active'] >= 900
        assert df.loc['aorist', 'active'] == df.values.max()

    def test_mood_data_filters_to_requested_mood(self) -> None:
        # Observed: nt_mood_data('subjunctive') returns 1,856 rows, matching
        # the raw subjunctive count from nt_mood_profile.
        _skip_if_missing()
        df = nt_mood_data('subjunctive')
        assert len(df) >= 1800
        assert (df['mood'] == 'subjunctive').all()

    def test_aorist_active_dominates_infinitive_profile(self) -> None:
        # Observed: aorist/active 959 is the top cell in the infinitive
        # tense x voice crosstab.
        _skip_if_missing()
        df = nt_infinitive_profile()
        assert df.loc['aorist', 'active'] >= 900
        assert df.loc['aorist', 'active'] == df.values.max()

    def test_aorist_second_person_dominates_imperative_profile(self) -> None:
        # Observed: aorist/second 913 is the top cell in the imperative
        # tense x person crosstab.
        _skip_if_missing()
        df = nt_imperative_profile()
        assert df.loc['aorist', 'second'] >= 850
        assert df.loc['aorist', 'second'] == df.values.max()

    def test_prohibitive_and_purpose_dominate_subjunctive_constructions(self) -> None:
        # Observed: prohibitive (μή + subj.) 660 (35.6%) and purpose/content
        # (ἵνα/ὅπως) 637 (34.3%) together are ~70% of all subjunctive uses.
        _skip_if_missing()
        df = nt_subjunctive_constructions()
        top2_pct = df.sort_values('pct', ascending=False).head(2)['pct'].sum()
        assert top2_pct >= 65.0

    def test_articular_infinitive_dominates_infinitive_constructions(self) -> None:
        # Observed: articular (τό + inf.) 1,374 (60.1%) is the single most
        # common infinitive construction.
        _skip_if_missing()
        df = nt_infinitive_constructions()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['pct'] >= 50.0

    def test_aorist_active_second_dominates_imperative_tense_comparison(self) -> None:
        # Observed: aorist/active/second 587 (31.3%) is the top row.
        _skip_if_missing()
        df = nt_imperative_tense_comparison()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['pct'] >= 25.0

    def test_gospels_and_acts_favor_indicative_in_genre_profile(self) -> None:
        # Observed: Gospels & Acts indicative 57.0% (vs. Pauline's 51.2%).
        _skip_if_missing()
        df = nt_mood_genre_profile()
        assert df.loc['Gospels & Acts', 'indicative'] >= 50.0

    def test_john_has_the_most_subjunctive_tokens(self) -> None:
        # Observed: Jhn 295 subjunctive tokens (15.9% of all GNT
        # subjunctives), narrowly ahead of Mat's 282 (15.2%).
        _skip_if_missing()
        df = nt_mood_book_distribution('subjunctive')
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['book'] == 'Jhn'
        assert top['count'] >= 250


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_nt_mood_overview,
            print_nt_subjunctive_profile,
            print_nt_infinitive_profile,
            print_nt_imperative_profile,
            print_nt_subjunctive_constructions,
            print_nt_infinitive_constructions,
            print_nt_imperative_tense_comparison,
            print_nt_mood_genre_profile,
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
        fns = (nt_mood_chart, nt_subjunctive_chart, nt_imperative_chart, nt_mood_genre_heatmap)
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn.__name__} returned None"
            assert Path(out).exists(), f"{fn.__name__} did not write a file"
            assert Path(out).stat().st_size > 0
