"""Behavioral tests for bible_grammar.nt.nt_verb_profile, requiring real
corpus data — data/processed/macula_syntax.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4;
broadened under issue #676 Phase 3).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt import nt_verb_profile as _mod
from bible_grammar.nt.nt_verb_profile import (
    nt_verb_data,
    nt_verb_top_lemmas,
    nt_verb_tense_profile,
    nt_verb_voice_profile,
    nt_verb_mood_profile,
    nt_verb_tense_voice,
    nt_verb_lemma_tense,
    nt_verb_book_distribution,
    nt_verb_genre_profile,
    print_nt_verb_overview,
    print_nt_verb_tense,
    print_nt_verb_voice,
    print_nt_verb_mood,
    print_nt_verb_tense_voice,
    print_nt_verb_top_lemmas,
    print_nt_verb_genre_profile,
    print_nt_verb_book_distribution,
    nt_verb_tense_chart,
    nt_verb_voice_chart,
    nt_verb_mood_chart,
    nt_verb_genre_heatmap,
    nt_verb_book_chart,
    nt_verb_tense_voice_heatmap,
)

_SYNTAX_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _SYNTAX_PARQUET.exists():
        pytest.skip(f"Data file not found: {_SYNTAX_PARQUET}")


class TestVerbProfile:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(nt_verb_data()) >= 27000   # observed: 28,357

    def test_eimi_is_top_lemma(self) -> None:
        # εἰμί ("to be") is the NT's single most frequent verb. Observed:
        # count 2457.
        _skip_if_missing()
        df = nt_verb_top_lemmas(5)
        top = df.iloc[0]
        assert top['lemma'] == 'εἰμί'
        assert top['count'] >= 2300

    def test_aorist_and_present_dominate_tense_profile(self) -> None:
        # Aorist (simple past narrative) and present are the NT's two
        # dominant tenses, together well over 3/4 of all verb tokens.
        # Observed: aorist 41.6%, present 40.8%.
        _skip_if_missing()
        df = nt_verb_tense_profile()
        top2_pct = df.sort_values('pct', ascending=False).head(2)['pct'].sum()
        assert top2_pct >= 75.0

    def test_active_voice_dominates(self) -> None:
        # Observed: active 20,742 (73.1%), including a 'middlepassive' form
        # (1,714, 6.0%) outside VOICE_ORDER's known categories.
        _skip_if_missing()
        df = nt_verb_voice_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'active'
        assert top['pct'] >= 65.0

    def test_indicative_dominates_mood_profile(self) -> None:
        # Observed: indicative 15,617 (55.1%), participle 6,653 (23.5%).
        _skip_if_missing()
        df = nt_verb_mood_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'indicative'
        assert top['pct'] >= 50.0

    def test_present_active_is_top_tense_voice_cell(self) -> None:
        # Observed: present/active 9,065, the largest single cell.
        _skip_if_missing()
        df = nt_verb_tense_voice()
        assert df.loc['present', 'active'] >= 8500
        assert df.loc['present', 'active'] == df.values.max()

    def test_eimi_lemma_tense_is_mostly_present(self) -> None:
        # εἰμί ("to be") has no aorist form (suppletive paradigm) — its
        # lemma x tense row should show 0 aorist. Observed: present 1812,
        # imperfect 455, aorist 0.
        _skip_if_missing()
        df = nt_verb_lemma_tense(['εἰμί'])
        row = df.loc['εἰμί']
        assert row['present'] >= 1700
        assert 'aorist' not in df.columns or row['aorist'] == 0

    def test_luke_has_the_most_verb_tokens(self) -> None:
        # Observed: Luk 4,501 verb tokens (15.9% of all GNT verbs).
        _skip_if_missing()
        df = nt_verb_book_distribution()
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['book'] == 'Luk'
        assert top['count'] >= 4000

    def test_gospels_and_acts_favor_aorist_narrative(self) -> None:
        # Observed: Gospels & Acts genre group, aorist 46.2% (vs. Pauline's
        # present-heavy 55.2%, reflecting narrative vs. epistolary register).
        _skip_if_missing()
        df = nt_verb_genre_profile()
        assert df.loc['Gospels & Acts', 'aorist'] >= 40.0


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_nt_verb_overview,
            print_nt_verb_tense,
            print_nt_verb_voice,
            print_nt_verb_mood,
            print_nt_verb_tense_voice,
            print_nt_verb_top_lemmas,
            print_nt_verb_genre_profile,
            print_nt_verb_book_distribution,
        )
        for fn in fns:
            capsys.readouterr()
            fn()
            out = capsys.readouterr().out
            assert len(out.strip()) > 50, f"{fn.__name__} produced no real output"


class TestChartFunctions:
    def test_chart_functions_produce_real_pngs(self, tmp_path, monkeypatch) -> None:
        # output/charts/ is a git-tracked directory in this repo (charts
        # are committed deliverables) — never let these write there in a
        # test, always redirect _CHART_DIR to a tmp path first.
        _skip_if_missing()
        monkeypatch.setattr(_mod, '_CHART_DIR', tmp_path)
        fns = (
            nt_verb_tense_chart,
            nt_verb_voice_chart,
            nt_verb_mood_chart,
            nt_verb_genre_heatmap,
            nt_verb_book_chart,
            nt_verb_tense_voice_heatmap,
        )
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn.__name__} returned None"
            assert Path(out).exists(), f"{fn.__name__} did not write a file"
            assert Path(out).stat().st_size > 0
