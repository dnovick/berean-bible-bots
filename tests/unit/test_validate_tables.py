"""Tests for scripts/validate_tables.py — the bold-summary-row markdown table
check. Known-good/known-bad, per docs/policies/test-coverage.md's priority
plan (issue #662): the validate_*.py scripts are the actual CI-enforced
quality gate for all lesson/exercise content, and had zero test coverage.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import validate_tables  # noqa: E402


class TestBoldSummaryRow:
    def test_total_row_is_not_flagged(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(validate_tables, "_REPO", tmp_path)
        md = tmp_path / "good.md"
        md.write_text(
            "| Book | Count |\n"
            "|---|---|\n"
            "| Genesis | 15 |\n"
            "| **Total** | **237** |\n"
        )
        warnings: list[str] = []
        validate_tables.check_file(md, warnings)
        assert warnings == []

    def test_non_total_bold_row_is_flagged(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(validate_tables, "_REPO", tmp_path)
        md = tmp_path / "bad.md"
        md.write_text(
            "| Book | Count |\n"
            "|---|---|\n"
            "| Genesis | 15 |\n"
            "| **Jeremiah** | **31** |\n"
        )
        warnings: list[str] = []
        validate_tables.check_file(md, warnings)
        assert len(warnings) == 1
        assert "Jeremiah" in warnings[0]
        assert "bold-summary-row" in warnings[0]

    def test_partially_bold_row_is_not_flagged(self, tmp_path: Path, monkeypatch) -> None:
        # Only flag when EVERY cell in the row is bold — a row with one bold
        # cell (e.g. just emphasizing a value) is not a summary-row candidate.
        monkeypatch.setattr(validate_tables, "_REPO", tmp_path)
        md = tmp_path / "partial.md"
        md.write_text(
            "| Book | Count |\n"
            "|---|---|\n"
            "| Genesis | **15** |\n"
        )
        warnings: list[str] = []
        validate_tables.check_file(md, warnings)
        assert warnings == []
