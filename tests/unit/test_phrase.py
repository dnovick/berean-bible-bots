"""Tests for bible_grammar.phrase — normalisation and token resolution (no I/O)."""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.lexical.phrase import _norm_strongs, _query_strongs, _resolve_token


class TestNormStrongs:
    def test_braced_hebrew_strips_leading_zeros(self) -> None:
        assert _norm_strongs("{H0430}") == "H430"

    def test_braced_hebrew_keeps_variant_letter(self) -> None:
        assert _norm_strongs("{H0430G}") == "H430G"

    def test_braced_greek(self) -> None:
        assert _norm_strongs("{G2316}") == "G2316"

    def test_slash_joined_picks_content_word(self) -> None:
        # H9003 is a grammatical tag → skip; H1697I is the content word
        result = _norm_strongs("H9003/{H1697I}")
        assert result == "H1697I"

    def test_plain_greek_strips_leading_zeros(self) -> None:
        assert _norm_strongs("G0001") == "G1"

    def test_plain_hebrew(self) -> None:
        assert _norm_strongs("H7225") == "H7225"

    def test_already_normalised_passthrough(self) -> None:
        assert _norm_strongs("H1254") == "H1254"

    def test_uppercases(self) -> None:
        assert _norm_strongs("g3056") == "G3056"


class TestQueryStrongs:
    def test_strips_leading_zeros(self) -> None:
        assert _query_strongs("H0430") == "H430"

    def test_preserves_variant_letter(self) -> None:
        assert _query_strongs("H0430G") == "H430G"

    def test_greek(self) -> None:
        assert _query_strongs("G3056") == "G3056"

    def test_no_prefix_passthrough(self) -> None:
        # non-standard string passes through unchanged (uppercased)
        assert _query_strongs("shalom") == "SHALOM"

    def test_uppercase_normalisation(self) -> None:
        assert _query_strongs("h7225") == "H7225"


class TestResolveToken:
    def test_none_is_wildcard(self) -> None:
        assert _resolve_token(None) == {"wildcard": True}

    def test_star_is_wildcard(self) -> None:
        assert _resolve_token("*") == {"wildcard": True}

    def test_dict_passthrough(self) -> None:
        constraint = {"pos": "Noun", "number": "Plural"}
        assert _resolve_token(constraint) == constraint

    def test_strongs_number_hebrew(self) -> None:
        result = _resolve_token("H1254")
        assert result == {"strongs": "H1254"}

    def test_strongs_number_greek(self) -> None:
        result = _resolve_token("G3056")
        assert result == {"strongs": "G3056"}

    def test_strongs_strips_leading_zeros(self) -> None:
        result = _resolve_token("H0430")
        assert result == {"strongs": "H430"}

    def test_lemma_string_no_strongs(self) -> None:
        # resolve_strongs is imported lazily from wordstudy inside _resolve_token
        with patch("bible_grammar.wordstudy.resolve_strongs", return_value=None):
            result = _resolve_token("εἰρήνη")
        assert "lemma" in result

    def test_resolved_lemma_returns_strongs(self) -> None:
        with patch("bible_grammar.wordstudy.resolve_strongs", return_value="G1515"):
            result = _resolve_token("εἰρήνη")
        assert result == {"strongs": "G1515"}

    def test_unsupported_type_raises(self) -> None:
        with pytest.raises(TypeError):
            _resolve_token(42)  # type: ignore[arg-type]
