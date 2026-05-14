"""
Word-level Peshitta NT morphology via the ETCBC/syrnt Text-Fabric dataset.

Each row in the returned DataFrame represents one Syriac word token with:
  book, chapter, verse — location
  word          — Syriac script
  sp            — part of speech (noun, verb, prep, conj, pron, det, part, intj)
  gn            — gender (m, f, NA)
  nu            — number (s, p, NA)
  ps            — person (p1, p2, p3, NA)
  st            — state (emphatic, construct, absolute, NA)
  vs            — verbal stem (peal, pael, aphel, ethpeel, ethpaal, ettaphal, NA)
  vt            — verb tense / aspect (perf, impf, imptv, ptca, ptcp, inf, NA)
  stem_sedra    — Sedra transliteration of the word form
  root_sedra    — Sedra transliteration of the lexical root
  lexeme_sedra  — Sedra transliteration of the dictionary lemma
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SYRNT_TF = _REPO_ROOT / "syrnt" / "tf"
_VERSION = "0.1"

_FEATURES = (
    "book chapter verse word "
    "sp gn nu ps st vs vt "
    "stem_sedra root_sedra lexeme_sedra"
)

_BOOK_MAP = {
    "Matt": "Mat", "Mark": "Mrk", "Luke": "Luk", "John": "Jhn",
    "Acts": "Act", "Rom": "Rom", "1Cor": "1Co", "2Cor": "2Co",
    "Gal": "Gal", "Eph": "Eph", "Phil": "Php", "Col": "Col",
    "1Thess": "1Th", "2Thess": "2Th", "1Tim": "1Ti", "2Tim": "2Ti",
    "Tit": "Tit", "Phlm": "Phm", "Heb": "Heb", "Jas": "Jas",
    "1Pet": "1Pe", "2Pet": "2Pe", "1John": "1Jn", "2John": "2Jn",
    "3John": "3Jn", "Jude": "Jud", "Rev": "Rev",
}


def query_peshitta() -> pd.DataFrame:
    """Load and return all Peshitta NT word-level morphology as a DataFrame."""
    try:
        from tf.fabric import Fabric
    except ImportError as exc:
        raise ImportError(
            "text-fabric not installed. Run: pip install text-fabric"
        ) from exc

    loc = str(_SYRNT_TF.resolve())
    TF = Fabric(locations=loc, modules=_VERSION, silent=True)
    api = TF.load(_FEATURES, silent=True)
    F = api.F
    L = api.L

    rows = []
    for w in F.otype.s("word"):
        book_node = L.u(w, otype="book")[0]
        ch_node = L.u(w, otype="chapter")[0]
        vs_node = L.u(w, otype="verse")[0]
        tf_book = F.book.v(book_node)
        book_id = _BOOK_MAP.get(tf_book, tf_book)
        rows.append({
            "book": book_id,
            "chapter": int(F.chapter.v(ch_node)),
            "verse": int(F.verse.v(vs_node)),
            "word": F.word.v(w),
            "sp": F.sp.v(w),
            "gn": F.gn.v(w),
            "nu": F.nu.v(w),
            "ps": F.ps.v(w),
            "st": F.st.v(w),
            "vs": F.vs.v(w),
            "vt": F.vt.v(w),
            "stem_sedra": F.stem_sedra.v(w),
            "root_sedra": F.root_sedra.v(w),
            "lexeme_sedra": F.lexeme_sedra.v(w),
        })

    return pd.DataFrame(rows)
