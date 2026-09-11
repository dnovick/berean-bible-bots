"""Behavioral tests for bible_grammar.ot.ot_noun_profile, requiring real
corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot import ot_noun_profile as _mod
from bible_grammar.ot.ot_noun_profile import (
    ot_noun_data,
    ot_noun_top_lemmas,
    ot_noun_state_profile,
    ot_adj_data,
    ot_noun_number_profile,
    ot_noun_gender_state,
    ot_noun_lemma_state,
    ot_noun_book_distribution,
    ot_noun_genre_profile,
    ot_article_usage,
    ot_construct_top_lemmas,
    print_ot_noun_overview,
    print_ot_noun_gender,
    print_ot_noun_state,
    print_ot_noun_top_lemmas,
    print_ot_construct_top_lemmas,
    print_ot_noun_genre_profile,
    print_ot_noun_book_distribution,
    print_ot_article_usage,
    ot_noun_state_chart,
    ot_noun_gender_chart,
    ot_noun_genre_heatmap,
    ot_noun_book_chart,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestNounData:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(ot_noun_data()) >= 140000   # observed: 143,975

    def test_yhwh_is_top_lemma(self) -> None:
        # יהוה is the OT's single most frequent noun-tagged lemma.
        # Observed: count 6,521 — consistent (same order of magnitude) with
        # divine_names.py's independent YHWH count of 6,513
        # (tests/integration/test_divine_names.py).
        _skip_if_missing()
        df = ot_noun_top_lemmas(5)
        top = df.iloc[0]
        assert top['lemma'] == 'יהוה'
        assert top['count'] >= 6000


class TestNounStateProfile:
    def test_hebrew_has_no_determined_state(self) -> None:
        # Unlike Aramaic (see test_aramaic_nominal.py), Hebrew marks
        # definiteness with a prefixed article, not a distinct
        # "determined" noun state — the state profile should show 0%
        # determined.
        _skip_if_missing()
        df = ot_noun_state_profile()
        determined = df[df['form'] == 'determined'].iloc[0]
        assert determined['count'] == 0


class TestAdjData:
    def test_genesis_has_real_adjective_tokens(self) -> None:
        # Observed: 9,558 adjective tokens OT-wide, 623 in Genesis.
        _skip_if_missing()
        assert len(ot_adj_data()) >= 9000
        assert len(ot_adj_data('Gen')) >= 500


class TestNounNumberProfile:
    def test_singular_dominates(self) -> None:
        # Observed: singular 78,959 (71.6%), plural 29,318 (26.6%).
        _skip_if_missing()
        df = ot_noun_number_profile()
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['form'] == 'singular'
        assert top['pct'] >= 65.0


class TestNounGenderState:
    def test_masculine_construct_and_absolute_are_close(self) -> None:
        # Observed: masculine/absolute 35,743, masculine/construct 37,918 —
        # Hebrew nouns split roughly evenly between the two states overall.
        _skip_if_missing()
        df = ot_noun_gender_state()
        assert df.loc['masculine', 'absolute'] >= 30000
        assert df.loc['masculine', 'construct'] >= 30000


class TestNounLemmaState:
    def test_yhwh_never_takes_construct_state(self) -> None:
        # The divine name never appears in construct (it can't be "of"
        # anything) — observed: absolute 0, construct 0 (it's simply not
        # state-marked at all, unlike ordinary nouns).
        _skip_if_missing()
        df = ot_noun_lemma_state(top_n=5)
        row = df.loc['יהוה']
        assert row['absolute'] == 0
        assert row['construct'] == 0

    def test_kol_is_overwhelmingly_construct(self) -> None:
        # Observed: כֹּל ("all/every") construct 5,016 vs. absolute 396 —
        # this word is used almost exclusively as a construct-chain head.
        _skip_if_missing()
        df = ot_noun_lemma_state(top_n=5)
        row = df.loc['כֹּל']
        assert row['construct'] >= 4500
        assert row['construct'] > row['absolute']


class TestNounBookDistribution:
    def test_genesis_share_of_ot_nouns(self) -> None:
        # Observed: Gen 9,249 noun tokens (6.4% of the whole OT), 28.6% of
        # Genesis's own word count.
        _skip_if_missing()
        df = ot_noun_book_distribution().set_index('book')
        assert df.loc['Gen', 'count'] >= 9000
        assert df.loc['Gen', 'pct_of_book_words'] >= 25.0


class TestNounGenreProfile:
    def test_no_genre_shows_determined_state(self) -> None:
        # Observed: every genre's 'determined' column is 0.0% — confirms
        # the whole-OT finding (Hebrew has no distinct determined state)
        # holds at the genre level too, not just in aggregate.
        _skip_if_missing()
        df = ot_noun_genre_profile()
        assert (df['determined'] == 0.0).all()


class TestArticleUsage:
    def test_torah_is_the_most_articular_genre(self) -> None:
        # Observed: Torah 24.2% articular, the highest of the 4 genres.
        _skip_if_missing()
        df = ot_article_usage()
        top = df.sort_values('pct_articular', ascending=False).iloc[0]
        assert top['scope'] == 'Torah'
        assert top['pct_articular'] >= 20.0

    def test_book_filter_narrows_to_one_scope_row(self) -> None:
        # Observed: book='Gen' → 9,249 nouns, 1,807 articles, 19.5% articular.
        _skip_if_missing()
        df = ot_article_usage(book='Gen')
        assert len(df) == 1
        assert df.iloc[0]['scope'] == 'Gen'
        assert df.iloc[0]['nouns'] >= 9000


class TestConstructTopLemmas:
    def test_kol_leads_construct_top_lemmas(self) -> None:
        # Observed: כֹּל leads with construct_count 5,016, pct_construct 92.7%.
        _skip_if_missing()
        df = ot_construct_top_lemmas(5)
        top = df.iloc[0]
        assert top['lemma'] == 'כֹּל'
        assert top['pct_construct'] >= 85.0


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_ot_noun_overview,
            lambda: print_ot_noun_gender('Gen'),
            print_ot_noun_state,
            lambda: print_ot_noun_top_lemmas(10, 'Gen'),
            lambda: print_ot_construct_top_lemmas(10),
            print_ot_noun_genre_profile,
            print_ot_noun_book_distribution,
            print_ot_article_usage,
        )
        for fn in fns:
            capsys.readouterr()
            fn()
            out = capsys.readouterr().out
            assert len(out.strip()) > 30, f"{fn} produced no real output"


class TestChartFunctions:
    def test_chart_functions_produce_real_pngs(self, tmp_path, monkeypatch) -> None:
        _skip_if_missing()
        monkeypatch.setattr(_mod, '_CHART_DIR', tmp_path)
        fns = (ot_noun_state_chart, ot_noun_gender_chart, ot_noun_genre_heatmap, ot_noun_book_chart)
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn.__name__} returned None"
            assert Path(out).exists(), f"{fn.__name__} did not write a file"
            assert Path(out).stat().st_size > 0
