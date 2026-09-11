"""Behavioral tests for bible_grammar.ot.ot_semantic_domains, requiring real
corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot import ot_semantic_domains as _mod
from bible_grammar.ot.ot_semantic_domains import (
    ot_domain_data,
    ot_top_domain_lemmas,
    ot_domain_frequency,
    ot_domain_book_distribution,
    ot_domain_genre_profile,
    ot_domain_comparison,
    ot_coredomain_profile,
    ot_theology_profile,
    print_ot_domain_overview,
    print_ot_domain_frequency,
    print_ot_domain_book_distribution,
    print_ot_domain_genre_profile,
    print_ot_domain_comparison,
    print_ot_theology_profile,
    ot_domain_frequency_chart,
    ot_domain_book_chart,
    ot_domain_genre_chart,
    ot_domain_heatmap,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestSpeechDomain:
    def test_domain_41_total(self) -> None:
        # Coredomain 41 = Speech/Utterance. Observed: 12,461 tokens.
        _skip_if_missing()
        assert len(ot_domain_data(41)) >= 12000

    def test_amar_leads_speech_domain(self) -> None:
        # אָמַר ("said") dominates the Speech/Utterance domain, as expected
        # for the OT's single most common speech verb. Observed: count
        # 2,127 for the "he.said" gloss variant alone.
        _skip_if_missing()
        df = ot_top_domain_lemmas(41, top_n=5)
        top = df.iloc[0]
        assert top['lemma'] == 'אָמַר'
        assert top['strong_h'] == 'H559'
        assert top['count'] >= 2000


class TestDomainFrequency:
    def test_object_marker_domains_lead_whole_ot(self) -> None:
        # Observed: codes 027 and 007 (both "Object Marker (et)" — the
        # untranslatable direct-object marker אֵת) are the two most
        # frequent domains OT-wide, ~15,900 and ~15,700 tokens.
        _skip_if_missing()
        df = ot_domain_frequency(top_n=5)
        top = df.iloc[0]
        assert top['domain_name'] == 'Object Marker (et)'
        assert top['count'] >= 15000

    def test_kinship_leads_in_genesis(self) -> None:
        # Observed: in Genesis specifically, Kinship/People (code 062)
        # leads with 1,667 tokens (9.0%) — genealogy-heavy narrative.
        _skip_if_missing()
        df = ot_domain_frequency(book='Gen', top_n=5)
        top = df.iloc[0]
        assert top['domain_name'] == 'Kinship/People'
        assert top['pct'] >= 7.0


class TestDomainBookDistribution:
    def test_jeremiah_leads_speech_domain(self) -> None:
        # Observed: Jer 1,280 tokens (10.3%) in the Speech/Utterance
        # domain — the largest of the prophetic books, unsurprising for a
        # book built around reported divine speech.
        _skip_if_missing()
        df = ot_domain_book_distribution(41)
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['book'] == 'Jer'
        assert top['count'] >= 1000


class TestDomainGenreProfile:
    def test_historical_books_lead_speech_domain(self) -> None:
        # Observed: Historical 4,259 (34.2%) — the largest genre share of
        # Speech/Utterance domain tokens (narrative dialogue).
        _skip_if_missing()
        df = ot_domain_genre_profile(41)
        top = df.sort_values('pct', ascending=False).iloc[0]
        assert top['genre'] == 'Historical'
        assert top['pct'] >= 25.0


class TestDomainComparison:
    def test_genesis_and_psalms_differ_on_kinship(self) -> None:
        # Observed: Genesis (genealogy-heavy) scores far higher on
        # Kinship/People (062) than Psalms (9.0% vs. 1.0%).
        _skip_if_missing()
        df = ot_domain_comparison(['Gen', 'Psa'], top_n=5)
        row = df.loc['062 Kinship/People']
        assert row['Gen'] > row['Psa']
        assert row['Gen'] >= 5.0


class TestCoredomainProfile:
    def test_matches_domain_frequency_for_the_same_book(self) -> None:
        # ot_coredomain_profile is a thin wrapper around ot_domain_frequency
        # — verify they agree exactly for the same book/top_n.
        _skip_if_missing()
        coredomain = ot_coredomain_profile('Gen', top_n=5)
        frequency = ot_domain_frequency(book='Gen', top_n=5)
        assert coredomain.equals(frequency)


class TestTheologyProfile:
    def test_hesed_and_achar_lead_covenant_group(self) -> None:
        # Observed: 667 rows total, count sum 2,562; חֶסֶד ("loyalty",
        # H2617) and אַחַר ("after", H310) tie for the top count at 130.
        _skip_if_missing()
        df = ot_theology_profile('Covenant')
        assert len(df) >= 600
        assert df['count'].max() >= 100
        top_lemmas = set(df[df['count'] == df['count'].max()]['lemma'])
        assert 'חֶסֶד' in top_lemmas

    def test_elohim_leads_divinity_group_in_genesis(self) -> None:
        # Observed: book='Gen' → top lemma אֱלֹהִים (H430), count 164.
        _skip_if_missing()
        df = ot_theology_profile('Divinity', book='Gen')
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['lemma'] == 'אֱלֹהִים'
        assert top['strong_h'] == 'H430'

    def test_unknown_group_raises_value_error(self) -> None:
        # Regression guard: an unrecognized theology group name must raise,
        # not silently return an empty/wrong profile.
        _skip_if_missing()
        with pytest.raises(ValueError):
            ot_theology_profile('NotARealGroup')


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_ot_domain_overview,
            lambda: print_ot_domain_frequency(top_n=5),
            lambda: print_ot_domain_book_distribution(41, top_n=5),
            lambda: print_ot_domain_genre_profile(41),
            lambda: print_ot_domain_comparison(['Gen', 'Psa'], top_n=5),
            lambda: print_ot_theology_profile('Covenant'),
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
        fns = (
            ot_domain_frequency_chart,
            lambda: ot_domain_book_chart(41),
            lambda: ot_domain_genre_chart(41),
            lambda: ot_domain_heatmap(['Gen', 'Psa']),
        )
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn} returned None"
            assert Path(out).exists(), f"{fn} did not write a file"
            assert Path(out).stat().st_size > 0
