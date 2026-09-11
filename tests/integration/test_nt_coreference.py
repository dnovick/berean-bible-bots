"""Behavioral tests for bible_grammar.nt.nt_coreference, requiring real
corpus data — data/processed/macula_syntax.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.nt import nt_coreference as _mod
from bible_grammar.nt.nt_coreference import (
    nt_referent_data,
    nt_referent_frequency,
    nt_entity_chain,
    nt_pronoun_referents,
    nt_book_entity_density,
    nt_entity_chapter_distribution,
    KNOWN_ENTITIES,
    print_nt_referent_overview,
    print_nt_entity_chain,
    print_nt_pronoun_referents,
    print_nt_book_entity_density,
    nt_referent_book_chart,
    nt_entity_density_chart,
)

_SYNTAX_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration

_JESUS_JHN = KNOWN_ENTITIES['Jesus (Jhn)']


def _skip_if_missing() -> None:
    if not _SYNTAX_PARQUET.exists():
        pytest.skip(f"Data file not found: {_SYNTAX_PARQUET}")


class TestReferentData:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(nt_referent_data()) >= 14000   # observed: 14,471


class TestReferentFrequency:
    def test_paulos_is_top_referent(self) -> None:
        # Παῦλος (Paul) leads NT referent chains — unsurprising given how
        # much of the NT is Pauline epistle, with Paul as author and
        # frequent self-referent. Observed: top chain has ref_count 151,
        # anchored at Rom 1:1 (Paul's self-introduction).
        _skip_if_missing()
        df = nt_referent_frequency(top_n=5)
        top = df.iloc[0]
        assert top['antecedent_lemma'] == 'Παῦλος'
        assert top['ref_count'] >= 140


class TestEntityChain:
    def test_jesus_in_john_returns_real_references(self) -> None:
        # Observed: 79 pronominal references to Jesus within John.
        _skip_if_missing()
        df = nt_entity_chain(_JESUS_JHN, book='Jhn')
        assert len(df) >= 70

    def test_book_filter_matches_unfiltered_for_a_single_book_entity(self) -> None:
        # This entity's xml_id is Jhn-specific, so filtering by book='Jhn'
        # should return the same rows as no filter at all.
        _skip_if_missing()
        unfiltered = nt_entity_chain(_JESUS_JHN)
        filtered = nt_entity_chain(_JESUS_JHN, book='Jhn')
        assert len(unfiltered) == len(filtered)


class TestPronounReferents:
    def test_autos_top_antecedent_is_jesus(self) -> None:
        # Observed: top antecedent for αὐτός ("he/it") is Ἰησοῦς, anchored
        # at Mrk 6:30!7, count 39.
        _skip_if_missing()
        df = nt_pronoun_referents('αὐτός', top_n=5)
        top = df.iloc[0]
        assert top['antecedent_lemma'] == 'Ἰησοῦς'
        assert top['count'] >= 30


class TestBookEntityDensity:
    def test_paul_dominates_romans_entity_density(self) -> None:
        # Observed: top row Παῦλος, ref_count 151, chapter_spread 16 (Paul
        # is referenced throughout every chapter of Romans).
        _skip_if_missing()
        df = nt_book_entity_density('Rom', top_n=5)
        top = df.iloc[0]
        assert top['antecedent_lemma'] == 'Παῦλος'
        assert top['ref_count'] >= 140
        assert top['chapter_spread'] >= 14


class TestEntityChapterDistribution:
    def test_jesus_in_john_spans_multiple_chapters(self) -> None:
        # Observed: 3 chapters (14, 15, 16) with counts 16, 46, 17.
        _skip_if_missing()
        df = nt_entity_chapter_distribution(_JESUS_JHN, 'Jhn')
        assert len(df) >= 2
        assert df['count'].sum() >= 70


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_nt_referent_overview,
            lambda: print_nt_entity_chain(_JESUS_JHN, book='Jhn'),
            lambda: print_nt_pronoun_referents('αὐτός'),
            lambda: print_nt_book_entity_density('Rom'),
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
        fns = (nt_referent_book_chart, lambda: nt_entity_density_chart('Rom'))
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn} returned None"
            assert Path(out).exists(), f"{fn} did not write a file"
            assert Path(out).stat().st_size > 0
