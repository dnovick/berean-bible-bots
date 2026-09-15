"""Behavioral tests for bible_grammar.ot.prepositions, requiring real corpus
data — data/processed/words.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot.prepositions import (
    prep_frequency,
    prep_by_book,
    prep_distribution_table,
    prep_collocates,
    prep_object_types,
    compare_preps,
    find_governing_prep,
    inf_cst_by_prep,
    print_prep_frequency,
    print_prep_by_book,
    print_prep_distribution,
    print_prep_collocates,
    print_compare_preps,
    print_inf_cst_by_prep,
)
from bible_grammar.ot.prepositions import _df as _prep_df

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestPrepFrequency:
    def test_le_is_the_most_common_ot_preposition(self) -> None:
        # לְ ("to/for") is the OT's most frequent preposition. Observed:
        # count 20,430, 31.8%.
        _skip_if_missing()
        df = prep_frequency(top_n=5)
        top = df.iloc[0]
        assert top['lemma'] == 'לְ'
        assert top['pct'] >= 25.0


class TestPrepByBook:
    def test_genesis_leads_le_distribution(self) -> None:
        # Observed: Genesis has 1,335 לְ tokens (6.5% of all 20,430).
        _skip_if_missing()
        df = prep_by_book('לְ')
        gen = df[df['book'] == 'Gen'].iloc[0]
        assert gen['count'] >= 1200
        assert gen['pct_of_lemma'] >= 5.0


class TestPrepDistributionTable:
    def test_default_major_preps_shape_and_total(self) -> None:
        # Observed: default 7 major prepositions, 4 book-group rows plus a
        # Total row; לְ leads with 20,430 total tokens.
        _skip_if_missing()
        df = prep_distribution_table()
        assert list(df.columns) == ['לְ', 'בְּ', 'מִן', 'עַל', 'אֶל', 'כְּ', 'עַד']
        assert 'Total' in df.index
        assert df.loc['Total', 'לְ'] >= 19000


class TestPrepCollocates:
    def test_bet_top_collocate_is_the_conjunction_vav(self) -> None:
        # Observed: וְ ("and") is the single most common word immediately
        # following בְּ, count 2,593.
        _skip_if_missing()
        df = prep_collocates('בְּ', top_n=5)
        top = df.iloc[0]
        assert top['collocate'] == 'וְ'
        assert top['count'] >= 2000


class TestPrepObjectTypes:
    def test_le_is_mostly_followed_by_nouns(self) -> None:
        # Observed: noun 32.6% is the largest single POS category
        # following לְ.
        _skip_if_missing()
        df = prep_object_types('לְ')
        top = df.iloc[0]
        assert top['pos'] == 'noun'
        assert top['pct'] >= 25.0


class TestComparePreps:
    def test_le_leads_bet_on_the_conjunction_collocate(self) -> None:
        # Observed: וְ ("and") count 2,638 for לְ vs. 2,593 for בְּ — close,
        # but לְ leads on its own top collocate.
        _skip_if_missing()
        df = compare_preps('לְ', 'בְּ', top_n=5)
        row = df[df['collocate'] == 'וְ'].iloc[0]
        assert row['count_לְ'] >= 2000
        assert row['count_בְּ'] >= 2000


class TestFindGoverningPrep:
    def test_finds_a_real_governing_preposition_in_genesis(self) -> None:
        # Observed: Genesis 1 word 21 (פָּנֶה, "face") is governed by עַל
        # ("on/upon", diacritics-stripped to "על").
        _skip_if_missing()
        gen = _prep_df()
        gen = gen[gen['book'] == 'Gen'].reset_index(drop=True)
        assert find_governing_prep(gen, 21) == 'על'

    def test_returns_none_marker_when_no_governing_prep_nearby(self) -> None:
        _skip_if_missing()
        gen = _prep_df()
        gen = gen[gen['book'] == 'Gen'].reset_index(drop=True)
        assert find_governing_prep(gen, 0) == '(none)'


class TestInfCstByPrep:
    def test_lamed_dominates_infinitive_construct_governance(self) -> None:
        # Observed: לְ (ל after stripping) governs 69.4% of all infinitive
        # constructs OT-wide, count 4,584 — the standard purpose/result
        # construction (e.g. "in order to...").
        _skip_if_missing()
        df = inf_cst_by_prep()
        top = df.iloc[0]
        assert top['prep'] == 'ל'
        assert top['pct'] >= 60.0


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_prep_frequency,
            lambda: print_prep_by_book('לְ'),
            print_prep_distribution,
            lambda: print_prep_collocates('בְּ'),
            lambda: print_compare_preps('לְ', 'בְּ'),
            print_inf_cst_by_prep,
        )
        for fn in fns:
            capsys.readouterr()
            fn()
            out = capsys.readouterr().out
            assert len(out.strip()) > 30, f"{fn} produced no real output"
