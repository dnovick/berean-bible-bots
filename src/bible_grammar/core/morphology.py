"""
Decode STEPBible morphology codes into structured fields.

Hebrew/Aramaic (TAHOT) Grammar column examples:
  HVqp3ms  = Hebrew Verb Qal Perfect 3ms
  HNcmsa   = Hebrew Noun common masc sing absolute
  HR/Ncfsa = two tokens joined (prefix / main word)
  HC/Td/Ncfsa = three tokens joined

Greek (TAGNT) dStrongs+Grammar column examples (after splitting on '='):
  N-NSF    = Noun Nominative Singular Feminine
  V-AAI-3S = Verb Aorist Active Indicative 3rd Singular
  ADV      = Adverb
  CONJ     = Conjunction
  T-ASM    = Article Accusative Singular Masculine
"""

import re

# ── Hebrew / Aramaic ──────────────────────────────────────────────────────────

_HEB_LANGUAGE = {"H": "Hebrew", "A": "Aramaic"}

_HEB_FUNCTION = {
    "V": "Verb", "N": "Noun", "A": "Adjective", "R": "Preposition",
    "C": "Conjunction", "D": "Adverb", "T": "Particle", "P": "Pronoun",
    "S": "Suffix",
}

_HEB_STEM = {
    "q": "Qal", "N": "Niphal", "p": "Piel", "P": "Pual",
    "h": "Hiphil", "H": "Hophal", "t": "Hithpael", "o": "Polal",
    "T": "Hitpoel", "D": "Nithpael", "e": "Shaphel", "c": "Tiphil",
    "v": "Haphel", "A": "Aphel", "a": "Pael", "b": "Peal",
    "B": "Peil", "i": "Hishtaphel", "O": "Hothpaal", "s": "Hitpaal",
}

_HEB_FORM = {
    "p": "Perfect", "i": "Imperfect", "w": "Consecutive Perfect",
    "q": "Consecutive Imperfect", "v": "Imperative", "r": "Participle",
    "s": "Participle passive", "a": "Infinitive absolute",
    "c": "Infinitive construct",
    # cohortative / jussive moods encoded in form for imperfect
    "h": "Cohortative", "j": "Jussive",
}

_HEB_PERSON = {"1": "1st", "2": "2nd", "3": "3rd"}
_HEB_GENDER = {"m": "Masculine", "f": "Feminine", "c": "Common", "b": "Both"}
_HEB_NUMBER = {"s": "Singular", "p": "Plural", "d": "Dual"}
_HEB_STATE = {"a": "Absolute", "c": "Construct", "d": "Definite"}
_HEB_NOUN_GENDER = {"m": "Masculine", "f": "Feminine", "c": "Common", "b": "Both"}
_HEB_NOUN_TYPE = {"c": "Common", "p": "Proper", "g": "Gentilic"}


def _decode_hebrew_token(code: str) -> dict:
    """Decode a single Hebrew/Aramaic morphology token (no '/' separators)."""
    result: dict = {}
    if not code:
        return result

    # Tokens that follow a '/' often drop the language prefix (H/A).
    # Detect by checking whether position 0 is a language code.
    if code[0] in _HEB_LANGUAGE:
        lang_char = code[0]
        result["language"] = _HEB_LANGUAGE[lang_char]
        func_char = code[1] if len(code) > 1 else ""
        rest = code[2:]
    else:
        # No language prefix — function is at position 0
        func_char = code[0]
        rest = code[1:]

    result["part_of_speech"] = _HEB_FUNCTION.get(func_char, func_char)

    if func_char == "V" and rest:
        stem_char = rest[0] if rest else ""
        result["stem"] = _HEB_STEM.get(stem_char, stem_char)
        form_char = rest[1] if len(rest) > 1 else ""
        result["conjugation"] = _HEB_FORM.get(form_char, form_char)
        person_char = rest[2] if len(rest) > 2 else ""
        result["person"] = _HEB_PERSON.get(person_char, person_char)
        gender_char = rest[3] if len(rest) > 3 else ""
        result["gender"] = _HEB_GENDER.get(gender_char, gender_char)
        number_char = rest[4] if len(rest) > 4 else ""
        result["number"] = _HEB_NUMBER.get(number_char, number_char)

    elif func_char == "N" and rest:
        type_char = rest[0] if rest else ""
        result["noun_type"] = _HEB_NOUN_TYPE.get(type_char, type_char)
        gender_char = rest[1] if len(rest) > 1 else ""
        result["gender"] = _HEB_NOUN_GENDER.get(gender_char, gender_char)
        number_char = rest[2] if len(rest) > 2 else ""
        result["number"] = _HEB_NUMBER.get(number_char, number_char)
        state_char = rest[3] if len(rest) > 3 else ""
        result["state"] = _HEB_STATE.get(state_char, state_char)

    elif func_char == "A" and rest:
        gender_char = rest[1] if len(rest) > 1 else ""
        result["gender"] = _HEB_NOUN_GENDER.get(gender_char, gender_char)
        number_char = rest[2] if len(rest) > 2 else ""
        result["number"] = _HEB_NUMBER.get(number_char, number_char)
        state_char = rest[3] if len(rest) > 3 else ""
        result["state"] = _HEB_STATE.get(state_char, state_char)

    return result


def decode_hebrew(morph_code: str) -> dict:
    """
    Decode a full TAHOT Grammar cell which may contain slash-joined tokens.
    Returns fields for the main (last/rightmost) content word; prefix fields
    are stored under 'prefixes'.
    """
    if not isinstance(morph_code, str) or not morph_code.strip():
        return {}

    # strip trailing backslash-punctuation markers like \H9016
    morph_code = re.sub(r'\\[^\s/]+', '', morph_code).strip()

    parts = morph_code.split("/")
    decoded_parts = [_decode_hebrew_token(p.strip()) for p in parts if p.strip()]

    if not decoded_parts:
        return {}

    # The main word is the last token; prefixes are the rest
    main = decoded_parts[-1]
    if len(decoded_parts) > 1:
        prefix_pos = [d.get("part_of_speech", "") for d in decoded_parts[:-1]]
        main["prefixes"] = "+".join(p for p in prefix_pos if p)

    return main


# ── Greek ─────────────────────────────────────────────────────────────────────

_GRK_FUNCTION = {
    "N": "Noun", "V": "Verb", "A": "Adjective", "ADV": "Adverb",
    "T": "Article", "CONJ": "Conjunction", "PREP": "Preposition",
    "PRT": "Particle", "P": "Pronoun", "COND": "Conditional",
    "INJ": "Interjection",
}

_GRK_TENSE = {
    "P": "Present", "I": "Imperfect", "F": "Future", "A": "Aorist",
    "X": "Perfect", "Y": "Pluperfect", "2A": "2nd Aorist",
    "2F": "2nd Future", "2X": "2nd Perfect", "2Y": "2nd Pluperfect",
}

_GRK_VOICE = {
    "A": "Active", "M": "Middle", "P": "Passive",
    "E": "Middle or Passive", "D": "Deponent",
    "O": "Middle Deponent", "Q": "Passive Deponent",
}

_GRK_MOOD = {
    "I": "Indicative", "S": "Subjunctive", "O": "Optative",
    "M": "Imperative", "N": "Infinitive", "P": "Participle",
}

_GRK_CASE = {
    "N": "Nominative", "G": "Genitive", "D": "Dative",
    "A": "Accusative", "V": "Vocative",
}

_GRK_NUMBER = {"S": "Singular", "P": "Plural", "D": "Dual"}
_GRK_GENDER = {"M": "Masculine", "F": "Feminine", "N": "Neuter"}
_GRK_PERSON = {"1": "1st", "2": "2nd", "3": "3rd"}


def decode_greek(grammar_field: str) -> dict:
    """
    Decode the grammar portion of a TAGNT dStrongs+Grammar cell.
    The input should be just the grammar part (after stripping 'G1234=').

    Examples:
      'N-NSF'       -> Noun Nominative Singular Feminine
      'V-AAI-3S'    -> Verb Aorist Active Indicative 3rd Singular
      'V-PAP-DPM'   -> Verb Present Active Participle Dative Plural Masculine
      'ADV'         -> Adverb
      'CONJ'        -> Conjunction
    """
    if not isinstance(grammar_field, str) or not grammar_field.strip():
        return {}

    code = grammar_field.strip().upper()
    result: dict = {}

    # Simple non-inflected codes
    if code in ("ADV", "CONJ", "PREP", "PRT", "INJ", "COND", "PRT-N"):
        result["part_of_speech"] = _GRK_FUNCTION.get(code.split("-")[0], code)
        return result

    parts = code.split("-")
    func = parts[0]
    result["part_of_speech"] = _GRK_FUNCTION.get(func, func)

    if func == "V":
        # V-<tense><voice><mood>[-<person><number>[-<case><number><gender>]]
        if len(parts) >= 2:
            tvm = parts[1]  # e.g. "AAI", "PAP", "2AAI"
            # handle 2-char tense prefix
            if tvm.startswith("2"):
                tense_key = tvm[:2]
                tvm_rest = tvm[2:]
            else:
                tense_key = tvm[0] if tvm else ""
                tvm_rest = tvm[1:]
            result["tense"] = _GRK_TENSE.get(tense_key, tense_key)
            result["voice"] = _GRK_VOICE.get(tvm_rest[0], tvm_rest[0]) if tvm_rest else ""
            result["mood"] = _GRK_MOOD.get(tvm_rest[1], tvm_rest[1]) if len(tvm_rest) > 1 else ""
        if len(parts) >= 3:
            pn = parts[2]  # e.g. "3S", "DPM"
            if pn and pn[0].isdigit():
                result["person"] = _GRK_PERSON.get(pn[0], pn[0])
                result["number"] = _GRK_NUMBER.get(pn[1], pn[1]) if len(pn) > 1 else ""
            else:
                # participle case-number-gender in part 2
                result["case_"] = _GRK_CASE.get(pn[0], pn[0]) if pn else ""
                result["number"] = _GRK_NUMBER.get(pn[1], pn[1]) if len(pn) > 1 else ""
                result["gender"] = _GRK_GENDER.get(pn[2], pn[2]) if len(pn) > 2 else ""
        if len(parts) >= 4:
            cng = parts[3]
            result["case_"] = _GRK_CASE.get(cng[0], cng[0]) if cng else ""
            result["number"] = _GRK_NUMBER.get(cng[1], cng[1]) if len(cng) > 1 else ""
            result["gender"] = _GRK_GENDER.get(cng[2], cng[2]) if len(cng) > 2 else ""

    elif func == "P":
        # Pronouns have two patterns:
        #   1st/2nd person: P-{person}{case}{number}  e.g. P-2GS, P-1NP
        #   3rd person/demonstrative: P-{case}{number}{gender}  e.g. P-GSM, P-NPM
        if len(parts) >= 2:
            cng = parts[1].split(" + ")[0]  # strip compound tokens like "1NS + G2532=CONJ"
            if cng and cng[0] in ("1", "2"):
                result["person"] = _GRK_PERSON.get(cng[0], cng[0])
                result["case_"] = _GRK_CASE.get(cng[1], cng[1]) if len(cng) > 1 else ""
                result["number"] = _GRK_NUMBER.get(cng[2], cng[2]) if len(cng) > 2 else ""
            else:
                result["person"] = "3rd"
                result["case_"] = _GRK_CASE.get(cng[0], cng[0]) if cng else ""
                result["number"] = _GRK_NUMBER.get(cng[1], cng[1]) if len(cng) > 1 else ""
                result["gender"] = _GRK_GENDER.get(cng[2], cng[2]) if len(cng) > 2 else ""

    else:
        # Nouns, adjectives, articles: <func>-<case><number><gender>
        if len(parts) >= 2:
            cng = parts[1]
            result["case_"] = _GRK_CASE.get(cng[0], cng[0]) if cng else ""
            result["number"] = _GRK_NUMBER.get(cng[1], cng[1]) if len(cng) > 1 else ""
            result["gender"] = _GRK_GENDER.get(cng[2], cng[2]) if len(cng) > 2 else ""

    return result


def extract_greek_grammar(dstrongs_grammar: str) -> tuple[str, str]:
    """
    Split a TAGNT 'dStrongs = Grammar' cell into (strongs, grammar_code).
    E.g. 'G0976=N-NSF' -> ('G0976', 'N-NSF')
    """
    if "=" in dstrongs_grammar:
        strongs, grammar = dstrongs_grammar.split("=", 1)
        return strongs.strip(), grammar.strip()
    return "", dstrongs_grammar.strip()
