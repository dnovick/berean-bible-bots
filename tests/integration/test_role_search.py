"""Behavioral tests for bible_grammar.names.role_search — backs both the
/role-search command (subject_verbs, verb_subjects) and /object-search
command (subject_objects, object_verbs), sharing one module. Requires the
real MACULA syntax data — data/processed/. Every expected value here was
directly observed by running the capability, not invented.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.names.role_search import (
    subject_verbs, verb_subjects, subject_objects, object_verbs,
    print_role_summary, print_object_summary, role_chart,
    divine_action_comparison, role_report,
)

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


# ── /role-search: who takes X as grammatical subject ──────────────────────────

class TestVerbSubjects:
    def test_bara_subject_is_predominantly_yahweh(self) -> None:
        # בָּרָא (create, H1254): the paradigm case for this capability —
        # creation-language subjects are overwhelmingly divine. Observed:
        # top row is Yahweh (H3068) at count 9, ahead of every other subject.
        _skip_if_missing()
        df = verb_subjects('H1254', corpus='OT')
        top = df.iloc[0]
        assert top['subject_strong'] == 'H3068'
        assert top['count'] >= 8

    def test_returns_expected_columns(self) -> None:
        _skip_if_missing()
        df = verb_subjects('H1254', corpus='OT')
        for col in ('subject_strong', 'subject_lemma', 'count'):
            assert col in df.columns


class TestSubjectVerbs:
    def test_yhwh_elohim_isaiah_non_empty_and_shaped(self) -> None:
        _skip_if_missing()
        df = subject_verbs(['H3068', 'H0430'], corpus='OT', books=['Isa'])
        assert len(df) > 0
        for col in ('lemma', 'strongnumberx', 'count'):
            assert col in df.columns
        assert (df['count'] > 0).all()


# ── /object-search: what does an entity act upon, what's done TO an entity ────

class TestSubjectObjects:
    def test_god_seeing_it_was_good_is_top_pair_in_genesis(self) -> None:
        # Genesis 1's refrain — "God saw that it was good" — recurs enough
        # to be the single most frequent (verb, object) pair for YHWH+Elohim
        # in Genesis. Observed: רָאָה (saw) / טוֹב (good), count 6.
        _skip_if_missing()
        df = subject_objects(['H3068', 'H0430'], corpus='OT', books=['Gen'])
        top = df.iloc[0]
        assert top['verb_lemma'] == 'רָאָה'
        assert top['obj_lemma'] == 'טוֹב'
        assert top['count'] >= 5


class TestObjectVerbs:
    def test_israel_is_predominantly_judged(self) -> None:
        # H3478 (Israel): שָׁפַט (judge) is the single most common verb
        # performed ON Israel across the OT. Observed: count 13.
        _skip_if_missing()
        df = object_verbs('H3478', corpus='OT')
        top = df.iloc[0]
        assert top['verb_lemma'] == 'שָׁפַט'
        assert top['count'] >= 10


# ── print_*, chart, comparison, and report wrappers ────────────────────────────

class TestPrintRoleSummary:
    def test_prints_real_output(self, capsys) -> None:
        _skip_if_missing()
        print_role_summary('H1254', 'OT')
        out = capsys.readouterr().out
        assert 'בָּרָא' in out or 'H1254' in out or 'Verbs with subject' in out
        assert len(out.strip()) > 50


class TestPrintObjectSummary:
    def test_prints_real_output(self, capsys) -> None:
        _skip_if_missing()
        print_object_summary(['H3068', 'H0430'], 'OT', books=['Gen'])
        out = capsys.readouterr().out
        assert 'רָאָה' in out
        assert len(out.strip()) > 50


class TestRoleChart:
    def test_produces_a_real_png(self, tmp_path: Path) -> None:
        # role_chart takes SUBJECT Strong's numbers (unlike verb_subjects,
        # which takes a verb) — H3068 is YHWH, the paradigm subject used
        # elsewhere in this file.
        _skip_if_missing()
        out = role_chart('H3068', 'OT', output_path=str(tmp_path / 'role.png'))
        assert Path(out).exists()
        assert Path(out).stat().st_size > 0


class TestDivineActionComparison:
    def test_yhwh_leads_ot_panel(self, tmp_path: Path) -> None:
        # Reuses the same H3068/H0430/H0136/H0410 default OT subjects as
        # the rest of this file's ground truth — the OT panel should be
        # real, non-empty data, not a placeholder.
        _skip_if_missing()
        ot_df, nt_df, chart_path = divine_action_comparison(
            output_path=str(tmp_path / 'compare.png'))
        assert not ot_df.empty
        assert Path(chart_path).exists()
        assert Path(chart_path).stat().st_size > 0


class TestRoleReport:
    def test_writes_a_real_markdown_report(self, tmp_path: Path) -> None:
        # role_report takes SUBJECT Strong's numbers (see TestRoleChart) —
        # H3068 (YHWH) is predominantly the subject of אָמַר ("said"),
        # observed count 162, far ahead of any other verb.
        _skip_if_missing()
        out = role_report('H3068', 'OT', output_dir=str(tmp_path))
        assert Path(out).exists()
        text = Path(out).read_text(encoding='utf-8')
        assert 'אָמַר' in text
        assert len(text) > 500
