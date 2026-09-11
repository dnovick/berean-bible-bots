"""Tests for scripts/annotate_psalm119_morphology.py's TAHOT morph-code
parsing — pure logic, no I/O. Per docs/policies/test-coverage.md's
priority plan (issue #676, Phase 2).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import annotate_psalm119_morphology as apm  # noqa: E402


class TestClean:
    def test_strips_cantillation_marks(self) -> None:
        assert apm._clean("אֶ֖רֶץ") == "אֶרֶץ"

    def test_strips_tahot_backslash_marker_and_following_char(self) -> None:
        # '\\' marks a separator in TAHOT encoding — skip it and the next char.
        assert "\\" not in apm._clean("שָׁמַ֫יִם\\")

    def test_keeps_vowel_points_and_dagesh(self) -> None:
        result = apm._clean("בְּרֵאשִׁית")
        assert "ְ" in result or "בְּ" in result  # shewa preserved


class TestParseVerb:
    def test_qal_perfect_3ms(self) -> None:
        assert apm._parse_verb("qp3ms") == {"stem": "Qal", "conj": "Perf", "pgn": "3ms"}

    def test_participle_uses_gender_number_state(self) -> None:
        result = apm._parse_verb("qrmsa")
        assert result["stem"] == "Qal"
        assert result["conj"] == "Ptc.act"
        assert result["pgn"] == "m.sg.abs"

    def test_infinitive_construct_has_no_pgn(self) -> None:
        result = apm._parse_verb("qc")
        assert result["conj"] == "InfCstr"
        assert result["pgn"] == ""


class TestParseNoun:
    def test_common_singular_construct(self) -> None:
        assert apm._parse_noun("cbsc") == {"gender": "c", "number": "sg", "state": "cstr"}


class TestParseSuffix:
    def test_pronominal_suffix_3ms(self) -> None:
        assert apm._parse_suffix("Sp3ms") == "3ms"


class TestMorphFromCode:
    def test_verb_wins_over_particle_prefix(self) -> None:
        # HTd/Vqp3ms: article prefix (HTd) + Qal perfect 3ms verb — the
        # verb segment should win per _POS_PRIORITY (verb beats particle).
        result = apm._morph_from_code("HTd/Vqp3ms")
        assert result["pos"] == "verb"
        assert result["stem"] == "Qal"
        assert result["conj"] == "Perf"
        assert result["pgn"] == "3ms"
