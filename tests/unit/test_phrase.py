"""Tests for bible_grammar.phrase — normalisation and token resolution (no I/O),
plus behavioral tests for phrase_search() itself requiring real corpus data.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.lexical.phrase import (
    _norm_strongs, _query_strongs, _resolve_token, phrase_search,
    proximity_search, print_proximity_results, print_phrase_results,
)

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


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
        with patch("bible_grammar.lexical.wordstudy.resolve_strongs", return_value=None):
            result = _resolve_token("εἰρήνη")
        assert "lemma" in result

    def test_resolved_lemma_returns_strongs(self) -> None:
        with patch("bible_grammar.lexical.wordstudy.resolve_strongs", return_value="G1515"):
            result = _resolve_token("εἰρήνη")
        assert result == {"strongs": "G1515"}

    def test_unsupported_type_raises(self) -> None:
        with pytest.raises(TypeError):
            _resolve_token(42)  # type: ignore[arg-type]


@pytest.mark.integration
class TestPhraseSearchBehavioral:
    def test_word_of_the_lord_total_occurrences(self) -> None:
        # דְּבַר יְהוָה "word of the LORD" (H1697 H3068): the paradigm
        # prophetic-formula phrase. Observed: 252 occurrences OT-wide.
        _skip_if_missing()
        df = phrase_search(['H1697', 'H3068'])
        assert len(df) == 252

    def test_word_of_the_lord_jeremiah_subset(self) -> None:
        # Observed: 58 occurrences restricted to Jeremiah, including the
        # book's opening formula at Jer 1:2.
        _skip_if_missing()
        df = phrase_search(['H1697', 'H3068'], book='Jer')
        assert len(df) == 58
        assert 'Jer 1:2' in set(df['reference'])


@pytest.mark.integration
class TestProximitySearchBehavioral:
    def test_emunah_chesed_within_5_words_is_mostly_psalms(self) -> None:
        # אֱמוּנָה (faithfulness, H0530) and חֶסֶד (kindness, H2617) paired
        # within 5 words — the classic OT hendiadys "faithfulness and
        # lovingkindness". Observed: 13 matches, 12 in Psalms + 1 in Hosea.
        _skip_if_missing()
        df = proximity_search(['H0530', 'H2617'], within=5)
        assert len(df) == 13
        assert df['book_id_1'].value_counts()['Psa'] == 12


@pytest.mark.integration
class TestPrintFunctions:
    def test_print_proximity_results_prints_real_output(self, capsys) -> None:
        _skip_if_missing()
        df = proximity_search(['H0530', 'H2617'], within=5)
        print_proximity_results(df, max_rows=3)
        out = capsys.readouterr().out
        assert 'Psa' in out
        assert len(out.strip()) > 50

    def test_print_phrase_results_prints_real_output(self, capsys) -> None:
        _skip_if_missing()
        df = phrase_search(['H1697', 'H3068'], book='Jer')
        print_phrase_results(df, max_rows=3)
        out = capsys.readouterr().out
        assert 'Jer 1:2' in out
        assert len(out.strip()) > 50
