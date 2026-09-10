"""Behavioral tests for bible_grammar.intertextuality.intertextuality
(/intertextuality), requiring the scrollmapper cross-reference data —
scrollmapper-data/sources_backup/extras/cross_references.txt (a git submodule).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.intertextuality.intertextuality import intertextuality

_XREF_FILE = (
    Path(__file__).resolve().parents[2] / "scrollmapper-data" / "sources_backup"
    / "extras" / "cross_references.txt"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _XREF_FILE.exists():
        pytest.skip(f"Data file not found: {_XREF_FILE}")


class TestIntertextuality:
    def test_psalm_110_1_is_the_most_quoted_verse(self) -> None:
        # Psalm 110:1 ("The LORD said unto my Lord...") is the single
        # most-quoted OT verse in the NT — cited in Matthew, Mark
        # (twice), Luke, Acts, and Hebrews. Observed: 6 links at
        # min_votes=20, with Matthew 22:44 the top-voted (34).
        _skip_if_missing()
        df = intertextuality('Psa', chapter=110, min_votes=20, include_kjv=False)
        assert len(df) >= 5
        assert (df['ot_ref'] == 'Psalms 110:1').any()
        top = df.iloc[0]
        assert top['nt_ref'] == 'Matthew 22:44'
        assert top['votes'] >= 30
