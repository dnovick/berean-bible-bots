"""Shared constants and helpers for all verbal_syntax sub-modules."""
from __future__ import annotations

import pandas as pd

from ..core._utils import strip_diacritics as _strip_diacritics  # noqa: F401 (re-exported)

# MACULA `type_` values for verbs — canonical display names
VERB_FORM_ORDER: list[str] = [
    'wayyiqtol',
    'qatal',
    'yiqtol',
    'weqatal',
    'participle active',
    'participle passive',
    'imperative',
    'jussive',
    'cohortative',
    'infinitive construct',
    'infinitive absolute',
]

# Short labels for charts
VERB_FORM_LABELS: dict[str, str] = {
    'wayyiqtol':            'wayyiqtol',
    'qatal':                'qatal',
    'yiqtol':               'yiqtol',
    'weqatal':              'weqatal',
    'participle active':    'ptc.act',
    'participle passive':   'ptc.pass',
    'imperative':           'impv',
    'jussive':              'juss',
    'cohortative':          'coh',
    'infinitive construct': 'inf.cst',
    'infinitive absolute':  'inf.abs',
}

# Governing-preposition lemmas (consonantal, diacritics stripped)
_PREP_DISPLAY: dict[str, str] = {
    'ל':    'lamed (purpose/result)',
    'ב':    'bet (temporal/instrumental)',
    'כ':    'kaf (comparative)',
    'מן':   'min (from)',
    'עד':   'ayin-dalet (until)',
    'על':   'ayin-lamed (upon)',
    'אחר':  'after',
    'בלת':  'without (neg. purpose)',
}


def _load_macula() -> pd.DataFrame:
    from ..core._utils import load_ot_data
    return load_ot_data()


def _filter_book(df: pd.DataFrame, book: str, chapter: int | None = None) -> pd.DataFrame:
    book_col = 'book_id' if 'book_id' in df.columns else 'book'
    result = df[df[book_col] == book]
    if chapter is not None:
        result = result[result['chapter'] == chapter]
    return result
