"""Behavioral tests for bible_grammar.discourse.speech_acts, requiring
real corpus data — data/processed/macula_syntax_ot.parquet and
macula_syntax.parquet. Per docs/policies/test-coverage.md's priority plan
(issue #676, Phase 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.discourse import speech_acts as _mod
from bible_grammar.discourse.speech_acts import (
    ot_speech_act_profile,
    nt_speech_act_profile,
    ot_speech_act_data,
    nt_speech_act_data,
    ot_speech_act_comparison,
    nt_speech_act_comparison,
    print_ot_speech_act_profile,
    print_nt_speech_act_profile,
    print_speech_act_comparison,
    speech_act_chart,
    speech_act_heatmap,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)
_MACULA_NT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_ot_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


def _skip_if_nt_missing() -> None:
    if not _MACULA_NT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_NT_PARQUET}")


class TestOtSpeechActProfile:
    def test_genesis_is_dominated_by_unclassified_and_directive(self) -> None:
        # Observed (post _OT_ASSERTIVE_LEMMAS fix below): 1,533 verses
        # total. unclassified 42.7% (654), directive 26.7% (409) — Genesis
        # narrative is mostly non-speech description plus commands (e.g.
        # "let there be...", divine/patriarchal orders).
        _skip_if_ot_missing()
        df = ot_speech_act_profile(book='Gen')
        by_type = df.set_index('speech_act_type')
        assert df['count'].sum() == 1533
        assert by_type.loc['unclassified', 'pct'] >= 35.0
        assert by_type.loc['directive', 'pct'] >= 20.0

    def test_yhwh_divine_name_cue_is_not_silently_dead(self) -> None:
        # Regression guard: _OT_ASSERTIVE_LEMMAS used the pointed form
        # 'יְהוָה', which matches only 1 stray token corpus-wide (this
        # corpus stores the name unpointed, 'יהוה' — same root cause as
        # the formulaic.py HEBREW_FORMULAS fix). This silently dropped the
        # divine-name cue for ~1,795 verses that name YHWH but have no
        # other assertive-triggering lemma, classifying them
        # 'unclassified' instead of 'assertive'. Gen 4:1 ("I have gotten a
        # man with YHWH") is one such verse — names YHWH, no other
        # assertive/directive/commissive/expressive/declarative cue fires.
        _skip_if_ot_missing()
        data = ot_speech_act_data(book='Gen')
        row = data[(data['chapter'] == 4) & (data['verse'] == 1)]
        assert not row.empty
        assert row.iloc[0]['speech_act_type'] == 'assertive'

    def test_speaker_filter_uses_the_unpointed_divine_name(self) -> None:
        # ot_speech_act_data(speaker=...) filters by lemma; the corpus
        # stores YHWH's lemma unpointed. Observed: book='Isa',
        # speaker='יהוה' -> 372 verses (a real, meaningful subset of
        # Isaiah's 1,291 total verses) — a stale/pointed speaker argument
        # would silently match nothing and fall back to returning every
        # verse in the book unfiltered (see the module's speaker_verse_keys
        # fallback), which this test would catch via the row count.
        _skip_if_ot_missing()
        filtered = ot_speech_act_data(book='Isa', speaker='יהוה')
        unfiltered = ot_speech_act_data(book='Isa')
        assert 0 < len(filtered) < len(unfiltered)
        assert len(filtered) >= 300


class TestNtSpeechActProfile:
    def test_matthew_directive_and_assertive_are_prominent(self) -> None:
        # Observed: 1,068 verses total. unclassified 33.1% (354), directive
        # 33.0% (352), assertive 23.2% (248) — Matthew's teaching discourse
        # (commands, declarations) contrasts with Genesis's narrative mix.
        _skip_if_nt_missing()
        df = nt_speech_act_profile(book='Mat')
        by_type = df.set_index('speech_act_type')
        assert df['count'].sum() == 1068
        assert by_type.loc['directive', 'pct'] >= 25.0
        assert by_type.loc['assertive', 'pct'] >= 15.0


class TestSpeechActData:
    def test_ot_data_returns_one_row_per_verse(self) -> None:
        _skip_if_ot_missing()
        df = ot_speech_act_data(book='Gen')
        assert len(df) == 1533
        for col in ('ref', 'book', 'chapter', 'verse', 'speech_act_type'):
            assert col in df.columns

    def test_nt_data_returns_one_row_per_verse(self) -> None:
        _skip_if_nt_missing()
        df = nt_speech_act_data(book='Mat')
        assert len(df) == 1068


class TestSpeechActComparison:
    def test_deuteronomy_has_more_assertive_and_directive_than_genesis(self) -> None:
        # Deuteronomy is Moses's extended speech (law + covenant renewal),
        # so it skews far more assertive/directive than Genesis's mostly
        # third-person narrative. Observed: Gen assertive 10.7%/directive
        # 26.7% vs. Deu assertive 24.9%/directive 39.6%.
        _skip_if_ot_missing()
        df = ot_speech_act_comparison(['Gen', 'Deu'])
        assert df.loc['assertive', 'Deu'] > df.loc['assertive', 'Gen']
        assert df.loc['directive', 'Deu'] > df.loc['directive', 'Gen']

    def test_romans_has_more_assertive_content_than_matthew(self) -> None:
        # Observed: Rom assertive 36.3% vs. Mat assertive 23.2% — Paul's
        # doctrinal exposition leans assertive; Matthew's narrated teaching
        # leans more directive (33.0% vs. Rom's 23.1%).
        _skip_if_nt_missing()
        df = nt_speech_act_comparison(['Mat', 'Rom'])
        assert df.loc['assertive', 'Rom'] > df.loc['assertive', 'Mat']
        assert df.loc['directive', 'Mat'] > df.loc['directive', 'Rom']

    def test_unknown_book_is_silently_dropped(self) -> None:
        _skip_if_ot_missing()
        df = ot_speech_act_comparison(['Gen', 'NotARealBook'])
        assert list(df.columns) == ['Gen']


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_ot_missing()
        _skip_if_nt_missing()
        fns = (
            lambda: print_ot_speech_act_profile(book='Gen'),
            lambda: print_nt_speech_act_profile(book='Mat'),
            lambda: print_speech_act_comparison(['Gen', 'Deu'], lang='H'),
            lambda: print_speech_act_comparison(['Mat', 'Rom'], lang='G'),
        )
        for fn in fns:
            capsys.readouterr()
            fn()
            out = capsys.readouterr().out
            assert len(out.strip()) > 30, f"{fn} produced no real output"


class TestChartFunctions:
    def test_chart_functions_produce_real_pngs(self, tmp_path, monkeypatch) -> None:
        _skip_if_ot_missing()
        _skip_if_nt_missing()
        monkeypatch.setattr(_mod, '_CHART_DIR', tmp_path)
        out1 = speech_act_chart(['Gen', 'Deu'], lang='H')
        assert out1 is not None
        assert Path(out1).exists()
        assert Path(out1).stat().st_size > 0

        out2 = speech_act_heatmap(['Mat', 'Rom'], lang='G')
        assert out2 is not None
        assert Path(out2).exists()
        assert Path(out2).stat().st_size > 0
