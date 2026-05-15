"""Tests for bible_grammar.morphology — pure decode logic, no I/O."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.core.morphology import decode_hebrew, decode_greek, extract_greek_grammar


class TestDecodeHebrew:
    def test_verb_qal_perfect_3ms(self) -> None:
        result = decode_hebrew("HVqp3ms")
        assert result["language"] == "Hebrew"
        assert result["part_of_speech"] == "Verb"
        assert result["stem"] == "Qal"
        assert result["conjugation"] == "Perfect"
        assert result["person"] == "3rd"
        assert result["gender"] == "Masculine"
        assert result["number"] == "Singular"

    def test_verb_niphal_imperfect_3fs(self) -> None:
        result = decode_hebrew("HVNi3fs")
        assert result["stem"] == "Niphal"
        assert result["conjugation"] == "Imperfect"
        assert result["person"] == "3rd"
        assert result["gender"] == "Feminine"
        assert result["number"] == "Singular"

    def test_verb_hiphil_wayyiqtol_3ms(self) -> None:
        result = decode_hebrew("HVhq3ms")
        assert result["stem"] == "Hiphil"
        assert result["conjugation"] == "Consecutive Imperfect"

    def test_noun_common_masculine_singular_absolute(self) -> None:
        result = decode_hebrew("HNcmsa")
        assert result["part_of_speech"] == "Noun"
        assert result["noun_type"] == "Common"
        assert result["gender"] == "Masculine"
        assert result["number"] == "Singular"
        assert result["state"] == "Absolute"

    def test_noun_feminine_plural_construct(self) -> None:
        result = decode_hebrew("HNcfpc")
        assert result["gender"] == "Feminine"
        assert result["number"] == "Plural"
        assert result["state"] == "Construct"

    def test_noun_proper(self) -> None:
        result = decode_hebrew("HNpmsa")
        assert result["noun_type"] == "Proper"

    def test_prefix_chain_preposition_plus_noun(self) -> None:
        # HR/Ncfsa = preposition + noun
        result = decode_hebrew("HR/Ncfsa")
        assert result["part_of_speech"] == "Noun"
        assert "prefixes" in result
        assert "Preposition" in result["prefixes"]

    def test_aramaic_language(self) -> None:
        result = decode_hebrew("AVqp3ms")
        assert result["language"] == "Aramaic"

    def test_empty_string(self) -> None:
        assert decode_hebrew("") == {}

    def test_non_string(self) -> None:
        assert decode_hebrew(None) == {}  # type: ignore[arg-type]

    def test_adverb_no_crash(self) -> None:
        result = decode_hebrew("HD")
        assert result["part_of_speech"] == "Adverb"

    def test_particle_no_crash(self) -> None:
        result = decode_hebrew("HT")
        assert result["part_of_speech"] == "Particle"


class TestDecodeGreek:
    def test_noun_nominative_singular_feminine(self) -> None:
        result = decode_greek("N-NSF")
        assert result["part_of_speech"] == "Noun"
        assert result["case_"] == "Nominative"
        assert result["number"] == "Singular"
        assert result["gender"] == "Feminine"

    def test_noun_genitive_plural_masculine(self) -> None:
        result = decode_greek("N-GPM")
        assert result["case_"] == "Genitive"
        assert result["number"] == "Plural"
        assert result["gender"] == "Masculine"

    def test_verb_aorist_active_indicative_3s(self) -> None:
        result = decode_greek("V-AAI-3S")
        assert result["part_of_speech"] == "Verb"
        assert result["tense"] == "Aorist"
        assert result["voice"] == "Active"
        assert result["mood"] == "Indicative"
        assert result["person"] == "3rd"
        assert result["number"] == "Singular"

    def test_verb_present_active_participle(self) -> None:
        result = decode_greek("V-PAP-NSM")
        assert result["tense"] == "Present"
        assert result["voice"] == "Active"
        assert result["mood"] == "Participle"
        assert result["case_"] == "Nominative"
        assert result["number"] == "Singular"
        assert result["gender"] == "Masculine"

    def test_adverb(self) -> None:
        result = decode_greek("ADV")
        assert result["part_of_speech"] == "Adverb"

    def test_conjunction(self) -> None:
        result = decode_greek("CONJ")
        assert result["part_of_speech"] == "Conjunction"

    def test_preposition(self) -> None:
        result = decode_greek("PREP")
        assert result["part_of_speech"] == "Preposition"

    def test_article_dative_singular_neuter(self) -> None:
        result = decode_greek("T-DSN")
        assert result["part_of_speech"] == "Article"
        assert result["case_"] == "Dative"
        assert result["number"] == "Singular"
        assert result["gender"] == "Neuter"

    def test_pronoun_second_person(self) -> None:
        result = decode_greek("P-2GS")
        assert result["person"] == "2nd"
        assert result["case_"] == "Genitive"
        assert result["number"] == "Singular"

    def test_pronoun_third_person(self) -> None:
        result = decode_greek("P-GSM")
        assert result["person"] == "3rd"
        assert result["case_"] == "Genitive"

    def test_verb_perfect_active_indicative_1p(self) -> None:
        result = decode_greek("V-XAI-1P")
        assert result["tense"] == "Perfect"
        assert result["voice"] == "Active"
        assert result["mood"] == "Indicative"
        assert result["person"] == "1st"
        assert result["number"] == "Plural"

    def test_verb_2nd_aorist(self) -> None:
        result = decode_greek("V-2AAI-3S")
        assert result["tense"] == "2nd Aorist"
        assert result["person"] == "3rd"

    def test_empty_string(self) -> None:
        assert decode_greek("") == {}

    def test_case_insensitive(self) -> None:
        lower = decode_greek("n-nsf")
        upper = decode_greek("N-NSF")
        assert lower == upper


class TestExtractGreekGrammar:
    def test_with_equals(self) -> None:
        strongs, grammar = extract_greek_grammar("G0976=N-NSF")
        assert strongs == "G0976"
        assert grammar == "N-NSF"

    def test_without_equals(self) -> None:
        strongs, grammar = extract_greek_grammar("ADV")
        assert strongs == ""
        assert grammar == "ADV"

    def test_strips_whitespace(self) -> None:
        strongs, grammar = extract_greek_grammar(" G2316 = N-GSM ")
        assert strongs == "G2316"
        assert grammar == "N-GSM"

    def test_only_splits_first_equals(self) -> None:
        # In case grammar itself contains =
        strongs, grammar = extract_greek_grammar("G1234=V-AAI=3S")
        assert strongs == "G1234"
        assert grammar == "V-AAI=3S"
