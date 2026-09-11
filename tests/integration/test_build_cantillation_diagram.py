"""Behavioral tests for scripts/build_cantillation_diagram.py, requiring
real corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #676, Phase 2).

Deliberately tests bible_grammar.ot.cantillation.render_verse_park()
directly with an explicit tmp output_path, rather than going through
build_one() (which hardcodes OUTPUT_ROOT = 'output/reports/ot/cantillation'
— real, git-TRACKED content per validate_links.py's convention that
output/reports/ is the committed source for reports, not gitignored like
most other generated dirs). Writing there from an automated test would
risk modifying tracked files.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from bible_grammar.ot.cantillation import render_verse_park  # noqa: E402
import build_cantillation_diagram as bcd  # noqa: E402

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestVerseRefs:
    def test_genesis_1_has_31_verses(self) -> None:
        _skip_if_missing()
        refs = list(bcd._verse_refs("Gen", 1, None))
        assert len(refs) == 31
        assert refs[0] == ("Gen", 1, 1)


class TestRenderVersePark:
    def test_genesis_1_1_produces_a_real_png(self, tmp_path) -> None:
        # No reportlab/font dependency here — render_verse_park uses
        # matplotlib (Agg backend), a hard, always-installed dependency,
        # unlike exercise_pdf/'s reportlab-based PDF generation.
        _skip_if_missing()
        out = tmp_path / "gen_1_1.png"
        result = render_verse_park("Gen", 1, 1, output_path=str(out))
        assert Path(result).exists()
        assert Path(result).stat().st_size > 1000
        with open(result, "rb") as f:
            assert f.read(8) == b"\x89PNG\r\n\x1a\n"
