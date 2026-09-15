"""Behavioral tests for bible_grammar.ot.ot_participant, requiring real
corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot import ot_participant as _mod
from bible_grammar.ot.ot_participant import (
    ot_participant_data,
    ot_participant_subject_verbs,
    ot_participant_object_verbs,
    ot_participant_chain,
    ot_entity_density,
    ot_participant_compare,
    print_ot_participant_profile,
    print_ot_participant_chain,
    print_ot_participant_compare,
    ot_participant_chain_chart,
    ot_entity_density_chart,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestParticipantData:
    def test_moses_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(ot_participant_data('Moses')) >= 700   # observed: 766


class TestParticipantSubjectVerbs:
    def test_moses_most_common_subject_verb_is_said(self) -> None:
        # Moses's most common subject-verb pairing is אָמַר ("said") —
        # consistent with his role as the one who relays God's words to
        # Israel throughout the Torah. Observed: count 182.
        _skip_if_missing()
        df = ot_participant_subject_verbs('Moses', top_n=5)
        top = df.iloc[0]
        assert top['verb_lemma'] == 'אָמַר'
        assert top['count'] >= 150


class TestParticipantObjectVerbs:
    def test_moses_object_verbs_use_the_same_verse_heuristic(self) -> None:
        # object_verbs uses the same same-verse co-occurrence heuristic as
        # subject_verbs's fallback (per the module's own docstring, this is
        # a "rough proxy", not a true syntactic-object detector) — so its
        # top result is the same verb. Observed: אָמַר ("said"), count 182.
        _skip_if_missing()
        df = ot_participant_object_verbs('Moses', top_n=5)
        top = df.iloc[0]
        assert top['verb_lemma'] == 'אָמַר'
        assert top['count'] >= 150


class TestParticipantChain:
    def test_jacob_peaks_in_genesis_31(self) -> None:
        # Observed: Jacob's highest single-chapter mention count in Genesis
        # is chapter 31 (the flight from Laban), 25 mentions.
        _skip_if_missing()
        df = ot_participant_chain('Gen', 'Jacob')
        top = df.sort_values('mention_count', ascending=False).iloc[0]
        assert int(top['chapter']) == 31
        assert top['mention_count'] >= 20


class TestEntityDensity:
    def test_elohim_dominates_genesis_1(self) -> None:
        # Observed: Elohim (אֱלֹהִים) appears 32 times in Genesis 1 — the
        # creation account, unsurprisingly God-dense.
        _skip_if_missing()
        df = ot_entity_density('Gen', top_n_entities=15)
        ch1 = df[(df['chapter'] == 1) & (df['entity'] == 'Elohim')].iloc[0]
        assert ch1['mention_count'] >= 25


class TestParticipantCompare:
    def test_moses_has_more_total_mentions_than_abraham(self) -> None:
        # Observed: Moses 766 total mentions across 19 books (top: Exodus);
        # Abraham 175 across 16 books (top: Genesis).
        _skip_if_missing()
        df = ot_participant_compare(['Moses', 'Abraham']).set_index('participant')
        assert df.loc['Moses', 'total_mentions'] >= 700
        assert df.loc['Moses', 'top_book'] == 'Exo'
        assert df.loc['Abraham', 'top_book'] == 'Gen'


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            lambda: print_ot_participant_profile('Moses'),
            lambda: print_ot_participant_chain('Gen', 'Jacob'),
            lambda: print_ot_participant_compare(['Moses', 'Abraham']),
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
            lambda: ot_participant_chain_chart('Gen', ['Jacob', 'Abraham']),
            lambda: ot_entity_density_chart('Gen'),
        )
        for fn in fns:
            out = fn()
            assert out is not None, f"{fn} returned None"
            assert Path(out).exists(), f"{fn} did not write a file"
            assert Path(out).stat().st_size > 0
