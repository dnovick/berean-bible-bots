"""Behavioral tests for bible_grammar.ot.ot_predicate_args, requiring real
corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot import ot_predicate_args as _mod
from bible_grammar.ot.ot_predicate_args import (
    ot_frame_data,
    ot_agent_verbs,
    ot_patient_verbs,
    ot_verb_agents,
    ot_verb_patients,
    ot_frame_pairs,
    print_ot_frame_overview,
    print_ot_agent_verbs,
    print_ot_patient_verbs,
    print_ot_verb_agents,
    print_ot_verb_patients,
    print_ot_frame_pairs,
    ot_agent_verbs_chart,
    ot_patient_verbs_chart,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestFrameData:
    def test_total_token_count(self) -> None:
        _skip_if_missing()
        assert len(ot_frame_data()) >= 65000   # observed: 68,207


class TestAgentVerbs:
    def test_elohim_most_common_agent_verb_is_said(self) -> None:
        # "God said" (Genesis 1's creation refrain, and many other verses)
        # makes אָמַר Elohim's most common agent-role verb.
        # Observed: count 60.
        _skip_if_missing()
        df = ot_agent_verbs('אֱלֹהִים', top_n=5)
        top = df.iloc[0]
        assert top['lemma'] == 'אָמַר'
        assert top['count'] >= 50


class TestPatientVerbs:
    def test_elohim_top_patient_verb_is_avad(self) -> None:
        # "Serve God/them" (עָבַד — serve/worship) is Elohim's most common
        # patient-role verb. Observed: 'you.will.serve' gloss, count 11.
        _skip_if_missing()
        df = ot_patient_verbs('אֱלֹהִים', top_n=5)
        top = df.iloc[0]
        assert top['lemma'] == 'עָבַד'
        assert top['count'] >= 8


class TestVerbAgents:
    def test_bara_top_agent_is_yhwh(self) -> None:
        # בָּרָא ("create") is predominantly a divine act — observed: יהוה
        # is the top agent (count 12), ahead of אֱלֹהִים (count 8).
        _skip_if_missing()
        df = ot_verb_agents('בָּרָא', top_n=5)
        top = df.iloc[0]
        assert top['a0_lemma'] == 'יהוה'
        assert top['count'] >= 8


class TestVerbPatients:
    def test_bara_top_patient_is_adam(self) -> None:
        # Observed: אָדָם ("humankind") is the top A1 patient of בָּרָא,
        # count 5.
        _skip_if_missing()
        df = ot_verb_patients('בָּרָא', top_n=5)
        top = df.iloc[0]
        assert top['a1_lemma'] == 'אָדָם'
        assert top['count'] >= 3


class TestFramePairs:
    def test_yhwh_natan_hu_is_the_top_frame_triple(self) -> None:
        # Observed: (יהוה, נָתַן "gave", הוּא) is the single most frequent
        # (agent, verb, patient) triple in the OT, count 131.
        _skip_if_missing()
        df = ot_frame_pairs(top_n=5)
        top = df.iloc[0]
        assert top['a0_lemma'] == 'יהוה'
        assert top['verb'] == 'נָתַן'
        assert top['count'] >= 100


class TestPrintFunctions:
    def test_print_functions_produce_real_output(self, capsys) -> None:
        _skip_if_missing()
        fns = (
            print_ot_frame_overview,
            lambda: print_ot_agent_verbs('אֱלֹהִים'),
            lambda: print_ot_patient_verbs('אֱלֹהִים'),
            lambda: print_ot_verb_agents('בָּרָא'),
            lambda: print_ot_verb_patients('בָּרָא'),
            print_ot_frame_pairs,
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
        assert ot_agent_verbs_chart('אֱלֹהִים') is not None
        assert ot_patient_verbs_chart('אֱלֹהִים') is not None
        for f in tmp_path.iterdir():
            assert f.stat().st_size > 0
