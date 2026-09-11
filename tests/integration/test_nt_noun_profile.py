"""Behavioral tests for bible_grammar.nt.nt_noun_profile, requiring real
corpus data — data/processed/macula_syntax.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4;
broadened under issue #676 Phase 3).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt import nt_noun_profile as _mod
from bible_grammar.nt.nt_noun_profile import (
    nt_noun_data,
    nt_noun_top_lemmas,
    nt_noun_case_profile,
    nt_noun_gender_profile,
    nt_noun_number_profile,
    nt_noun_case_gender,
    nt_noun_lemma_case,
    nt_noun_book_distribution,
    nt_noun_genre_profile,
    nt_article_stats,
    print_nt_noun_overview,
    print_nt_noun_case,
    print_nt_noun_gender,
    print_nt_noun_case_gender,
    print_nt_noun_top_lemmas,
    print_nt_noun_genre_profile,
    print_nt_noun_book_distribution,
    print_nt_article_stats,
    nt_noun_case_chart,
    nt_noun_gender_chart,
    nt_noun_genre_heatmap,
    nt_noun_case_gender_heatmap,
    nt_noun_book_chart,
)

_SYNTAX_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _SYNTAX_PARQUET.exists():
        pytest.skip(f"Data file not found: {_SYNTAX_PARQUET}")


class TestNounProfile:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(nt_noun_data()) >= 27000   # observed: 28,455

    def test_theos_is_top_lemma(self) -> None:
        # θεός (God) is the NT's most frequent noun lemma. Observed: count 1311.
        _skip_if_missing()
        df = nt_noun_top_lemmas(30)
        top = df.iloc[0]
        assert top['lemma'] == 'θεός'
        assert top['count'] >= 1200

    def test_top_lemmas_does_not_crash_on_null_gloss_lemmas(self) -> None:
        # Regression guard: nt_noun_top_lemmas() used to crash with
        # IndexError for any lemma whose every token has a null gloss (e.g.
        # δύσις/G1424, a single-occurrence word) — value_counts() drops NaN,
        # so a group that's entirely null has an EMPTY value_counts() even
        # though the group itself is non-empty; the old `if len(x) else ''`
        # guard checked the wrong thing. Run across the full top-30 (which
        # includes low-frequency lemmas) rather than just the top handful.
        # n=3000 comfortably covers all ~2,399 unique noun lemma groups,
        # including δύσις itself.
        _skip_if_missing()
        df = nt_noun_top_lemmas(3000)
        assert not df.empty
        assert 'top_gloss' in df.columns
        assert (df['lemma'] == 'δύσις').any()

    def test_accusative_leads_case_profile(self) -> None:
        # Observed: accusative 8,677 (30.5%), genitive 7,556 (26.6%),
        # nominative 7,356 (25.9%).
        _skip_if_missing()
        df = nt_noun_case_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'accusative'
        assert top['pct'] >= 25.0

    def test_masculine_leads_gender_profile(self) -> None:
        # Observed: masculine 13,891 (48.8%), feminine 9,805 (34.5%).
        _skip_if_missing()
        df = nt_noun_gender_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'masculine'
        assert top['pct'] >= 40.0

    def test_singular_dominates_number_profile(self) -> None:
        # Observed: singular 22,589 (79.4%).
        _skip_if_missing()
        df = nt_noun_number_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'singular'
        assert top['pct'] >= 70.0

    def test_nominative_masculine_is_top_case_gender_cell(self) -> None:
        # Observed: nominative/masculine 4,483, the largest cell.
        _skip_if_missing()
        df = nt_noun_case_gender()
        assert df.loc['nominative', 'masculine'] >= 4000
        assert df.loc['nominative', 'masculine'] == df.values.max()

    def test_theos_lemma_case_is_mostly_genitive(self) -> None:
        # Observed: θεός genitive 691, the largest single case for this
        # lemma (reflecting frequent possessive/attributive "of God").
        _skip_if_missing()
        df = nt_noun_lemma_case(['θεός'])
        row = df.loc['θεός']
        assert row['genitive'] >= 600
        assert row['genitive'] == row.max()

    def test_acts_has_the_most_noun_tokens(self) -> None:
        # Observed: Act 4,079 noun tokens (14.3% of all GNT nouns).
        _skip_if_missing()
        df = nt_noun_book_distribution()
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['book'] == 'Act'
        assert top['count'] >= 3800

    def test_gospels_and_acts_favor_accusative_in_genre_profile(self) -> None:
        # Observed: Gospels & Acts genre group, accusative 33.3%.
        _skip_if_missing()
        df = nt_noun_genre_profile()
        assert df.loc['Gospels & Acts', 'accusative'] >= 28.0

    def test_genitive_is_the_most_articular_case(self) -> None:
        # Observed: genitive with_article 4,051/7,556 = 53.6%; vocative is
        # never articular (0/565 = 0.0%).
        _skip_if_missing()
        df = nt_article_stats().set_index('case')
        assert df.loc['genitive', 'pct_articular'] >= 45.0
        assert df.loc['vocative', 'pct_articular'] == 0.0


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_nt_noun_overview,
            print_nt_noun_case,
            print_nt_noun_gender,
            print_nt_noun_case_gender,
            print_nt_noun_top_lemmas,
            print_nt_noun_genre_profile,
            print_nt_noun_book_distribution,
            print_nt_article_stats,
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
            nt_noun_case_chart,
            nt_noun_gender_chart,
            nt_noun_genre_heatmap,
            nt_noun_case_gender_heatmap,
            nt_noun_book_chart,
        )
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn.__name__} returned None"
            assert Path(out).exists(), f"{fn.__name__} did not write a file"
            assert Path(out).stat().st_size > 0
