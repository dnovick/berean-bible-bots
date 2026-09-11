"""Tests for scripts/build_bbg_exercises.py's pure column-classification
and HTML input-widget builders. Per docs/policies/test-coverage.md's
priority plan (issue #676, Phase 2). This is the exact rule from
feedback_use_dropdowns: finite fields must use <select>, not free-text.

build_bbg_exercises.py imports bible_grammar.exercise_pdf at module level
(to introspect exercise classes), which imports reportlab unconditionally
via _base.py — deliberately not installed in CI (see review-pr.yml's
install-step comment and tests/integration/test_exercise_pdf.py). The
functions tested here don't touch PDF generation at all, but the import
chain still requires reportlab, so this file needs the same
collection-safety guard: try the import, and skip every test (not just
deselect — collection itself must not raise) if it's unavailable.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

try:
    import build_bbg_exercises as bbg
    _AVAILABLE = True
except ImportError:
    bbg = None  # type: ignore[assignment]
    _AVAILABLE = False


def _skip_if_missing() -> None:
    if not _AVAILABLE:
        pytest.skip("reportlab not installed (build_bbg_exercises.py imports bible_grammar.exercise_pdf)")


class TestDetermineInputs:
    def test_columns_with_a_small_distinct_value_set_become_dropdowns(self) -> None:
        _skip_if_missing()
        hdrs = ["#", "Form", "Case", "Number"]
        rows = [["1", "x", "Nom", "Sg"], ["2", "y", "Acc", "Pl"], ["3", "z", "Nom", "Sg"]]
        result = bbg._determine_inputs(hdrs, rows)
        assert result == ["select:Acc|Nom", "select:Pl|Sg"]

    def test_registered_free_text_columns_are_never_dropdowns(self) -> None:
        # "translation" is explicitly in _FREE_TEXT_COLS — must stay a
        # free-text <input> even if (as here) it happens to have few
        # distinct values across the sample rows.
        _skip_if_missing()
        hdrs = ["#", "Form", "Translation"]
        rows = [["1", "x", "he said"], ["2", "y", "he said"]]
        result = bbg._determine_inputs(hdrs, rows)
        assert result == ["input"]

    def test_too_few_distinct_values_falls_back_to_free_text(self) -> None:
        # Not in _FREE_TEXT_COLS, but only 1 distinct value across all
        # rows — below the 2-value minimum for a dropdown to be useful.
        _skip_if_missing()
        hdrs = ["#", "Form", "Note"]
        rows = [["1", "x", "same note"]]
        result = bbg._determine_inputs(hdrs, rows)
        assert result == ["input"]


class TestSel:
    def test_renders_select_with_blank_option_first(self) -> None:
        _skip_if_missing()
        html = bbg._sel(["Nom", "Acc"])
        assert html.startswith('<select class="pf">')
        assert '<option value=""></option>' in html
        assert '<option value="Nom">Nom</option>' in html
        assert '<option value="Acc">Acc</option>' in html


class TestInp:
    def test_ltr_input_has_no_direction_style(self) -> None:
        _skip_if_missing()
        assert bbg._inp(rtl=False) == '<input class="pf" type="text">'

    def test_rtl_input_includes_direction_style(self) -> None:
        _skip_if_missing()
        html = bbg._inp(rtl=True)
        assert "direction:rtl" in html
