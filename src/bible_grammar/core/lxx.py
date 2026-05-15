"""
Load and export the CenterBLC/LXX (Rahlfs 1935) Septuagint via TextFabric.

Word-level features extracted:
  word, lemma, transliteration, gloss, strongs, part_of_speech,
  tense, voice, mood, person, number, gender, case_, morphology

Books are tagged as canonical (matching our OT book_id list) or
deuterocanonical.  Both are stored; callers can filter on is_deuterocanon.
"""

from __future__ import annotations
import pandas as pd

# Map CenterBLC/LXX book names -> our book_id codes (canonical OT books)
_LXX_TO_BOOK_ID: dict[str, str] = {
    "Gen":   "Gen", "Exod":  "Exo", "Lev":   "Lev", "Num":   "Num",
    "Deut":  "Deu", "Josh":  "Jos", "Judg":  "Jdg", "Ruth":  "Rut",
    "1Sam":  "1Sa", "2Sam":  "2Sa", "1Kgs":  "1Ki", "2Kgs":  "2Ki",
    "1Chr":  "1Ch", "2Chr":  "2Ch",
    # Ezra / Nehemiah — 2Esdr in LXX = Ezra + Nehemiah combined
    "2Esdr": "Ezr",
    "Esth":  "Est", "Job":   "Job", "Ps":    "Psa", "Prov":  "Pro",
    "Qoh":   "Ecc", "Cant":  "Sng", "Isa":   "Isa", "Jer":   "Jer",
    "Lam":   "Lam", "Ezek":  "Ezk", "Dan":   "Dan", "Hos":   "Hos",
    "Joel":  "Jol", "Amos":  "Amo", "Obad":  "Oba", "Jonah": "Jon",
    "Mic":   "Mic", "Nah":   "Nah", "Hab":   "Hab", "Zeph":  "Zep",
    "Hag":   "Hag", "Zech":  "Zec", "Mal":   "Mal",
}

# Deuterocanonical / Apocrypha books (keep but flag)
_DEUTEROCANON: set[str] = {
    "1Esdr", "Jdt", "TobBA", "TobS", "1Mac", "2Mac", "3Mac", "4Mac",
    "Od", "Wis", "Sir", "PsSol", "Bar", "EpJer", "Bel", "BelTh",
    "DanTh", "Sus", "SusTh",
}

# Normalise raw feature values to match the style used for TAGNT
_TENSE_MAP = {
    "Aor": "Aorist", "Pres": "Present", "Fut": "Future",
    "Imperf": "Imperfect", "Perf": "Perfect", "Pluperf": "Pluperfect",
}
_VOICE_MAP = {"Act": "Active", "Mid": "Middle", "Pass": "Passive", "Plur": "Plural"}
_MOOD_MAP = {
    "Ind": "Indicative", "Subj": "Subjunctive", "Opt": "Optative",
    "Imperative": "Imperative", "Infin": "Infinitive", "Part": "Participle",
    "Neut": "Neuter",
}
_CASE_MAP = {
    "Nom": "Nominative", "Gen": "Genitive", "Dat": "Dative",
    "Acc": "Accusative", "Voc": "Vocative", "Gen/Dat": "Genitive/Dative",
}
_NUM_MAP = {"Sing": "Singular", "Plur": "Plural", "Dual": "Dual"}
_GEN_MAP = {"Masc": "Masculine", "Fem": "Feminine", "Neut": "Neuter"}
_PER_MAP = {"1st": "1st", "2nd": "2nd", "3rd": "3rd"}

# sp values often contain extra description after a comma — normalise to first token
_SP_NORMALISE = {
    "verb": "Verb", "noun": "Noun", "adjective": "Adjective",
    "adverb": "Adverb", "conjunction": "Conjunction",
    "preposition": "Preposition", "particle": "Particle",
    "interjection": "Interjection", "pronoun, article": "Article",
    "pronoun, demonstrative": "Pronoun", "pronoun, personal/possessive": "Pronoun",
    "pronoun, relative": "Pronoun", "pronoun, interrogative/indefinite": "Pronoun",
    "indeclinable number": "Numeral",
}


def _norm_sp(raw: str) -> str:
    if not raw:
        return ""
    low = raw.lower()
    # exact match first
    if low in _SP_NORMALISE:
        return _SP_NORMALISE[low]
    # prefix match
    for k, v in _SP_NORMALISE.items():
        if low.startswith(k):
            return v
    return raw


def load_lxx() -> pd.DataFrame:
    """
    Load the CenterBLC/LXX Septuagint into a DataFrame.

    Requires TextFabric + GitHub access on first run (~200 MB download).
    Subsequent calls use the local TextFabric cache.
    """
    try:
        from tf.app import use as tf_use
    except ImportError:
        raise ImportError(
            "TextFabric is required for LXX support.\n"
            "Install with:  pip install 'text-fabric[github]'"
        )

    print("  Loading CenterBLC/LXX via TextFabric (downloads on first run)...")
    lxx = tf_use("CenterBLC/LXX", version="1935", hoist=globals(), silent="deep")
    if lxx is None:
        raise RuntimeError(
            "TextFabric failed to load CenterBLC/LXX. "
            "Check your internet connection and GitHub access."
        )

    api = lxx.api
    F = api.F
    L = api.L
    T = api.T

    rows: list[dict] = []
    for book_node in F.otype.s("book"):
        lxx_book = F.book.v(book_node)
        book_id = _LXX_TO_BOOK_ID.get(lxx_book, lxx_book)
        is_deut = lxx_book in _DEUTEROCANON

        for verse_node in L.d(book_node, "verse"):
            section = T.sectionFromNode(verse_node)
            chapter = int(section[1]) if section and section[1] else 0
            verse = int(section[2]) if section and section[2] else 0

            for word_num, word_node in enumerate(L.d(verse_node, "word"), start=1):
                sp_raw = F.sp.v(word_node) or ""
                tns_raw = F.tense.v(word_node) or ""
                vce_raw = F.voice.v(word_node) or ""
                mod_raw = F.mood.v(word_node) or ""
                cas_raw = F.case.v(word_node) or ""
                nu_raw = F.nu.v(word_node) or ""
                gn_raw = F.gn.v(word_node) or ""
                ps_raw = F.ps.v(word_node) or ""

                rows.append({
                    "source":           "LXX",
                    "book_id":          book_id,
                    "lxx_book":         lxx_book,
                    "chapter":          chapter,
                    "verse":            verse,
                    "word_num":         word_num,
                    "word":             F.word.v(word_node) or "",
                    "lemma":            F.lex_utf8.v(word_node) or "",
                    "lemma_translit":   F.lex.v(word_node) or "",
                    "transliteration":  F.translit_SBL.v(word_node) or "",
                    "translation":      F.gloss.v(word_node) or "",
                    "strongs":          F.strongs.v(word_node) or "",
                    "morph_code":       F.morphology.v(word_node) or "",
                    "language":         "Greek",
                    "part_of_speech":   _norm_sp(sp_raw),
                    "tense":            _TENSE_MAP.get(tns_raw, tns_raw),
                    "voice":            _VOICE_MAP.get(vce_raw, vce_raw),
                    "mood":             _MOOD_MAP.get(mod_raw, mod_raw),
                    "case_":            _CASE_MAP.get(cas_raw, cas_raw),
                    "number":           _NUM_MAP.get(nu_raw, nu_raw),
                    "gender":           _GEN_MAP.get(gn_raw, gn_raw),
                    "person":           _PER_MAP.get(ps_raw, ps_raw),
                    "is_deuterocanon":  is_deut,
                    # Hebrew-only fields left blank
                    "stem":             "",
                    "conjugation":      "",
                    "state":            "",
                    "noun_type":        "",
                    "prefixes":         "",
                })

    return pd.DataFrame(rows)
