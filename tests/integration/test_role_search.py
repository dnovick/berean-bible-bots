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
