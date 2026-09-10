"""Tests for scripts/validate_exercises.py — exercise content-quality checks.
Known-good/known-bad, per docs/policies/test-coverage.md's priority plan
(issue #662).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import validate_exercises  # noqa: E402


class TestCheckThreeFormats:
    def test_all_three_formats_present_has_no_errors(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        monkeypatch.setattr(validate_exercises, "_REPO", tmp_path)
        ex_dir = tmp_path / "ch99-test-exercise"
        ex_dir.mkdir()
        (ex_dir / "ch99-test-exercise.md").write_text("# Exercise\n")
        (ex_dir / "ch99-test-exercise.html").write_text("<html></html>\n")
        (ex_dir / "ch99-test-exercise.pdf").write_bytes(b"%PDF-1.4\n")

        errors: list[str] = []
        warnings: list[str] = []
        validate_exercises.check_three_formats(ex_dir, errors, warnings)
        assert errors == []

    def test_missing_pdf_is_an_error(self, tmp_path: Path, monkeypatch) -> None:
        # This is the exact rule from feedback_exercise_formats: every
        # exercise must always have all three formats — never just two.
        monkeypatch.setattr(validate_exercises, "_REPO", tmp_path)
        ex_dir = tmp_path / "ch99-test-exercise"
        ex_dir.mkdir()
        (ex_dir / "ch99-test-exercise.md").write_text("# Exercise\n")
        (ex_dir / "ch99-test-exercise.html").write_text("<html></html>\n")

        errors: list[str] = []
        warnings: list[str] = []
        validate_exercises.check_three_formats(ex_dir, errors, warnings)
        assert len(errors) == 1
        assert ".pdf" in errors[0]


class TestCheckAnswerRowEmpty:
    def test_answer_row_with_content_is_not_flagged(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        monkeypatch.setattr(validate_exercises, "_REPO", tmp_path)
        ex_dir = tmp_path / "ch99-test-exercise"
        ex_dir.mkdir()
        (ex_dir / "ch99-test-exercise.html").write_text(
            '<table><tr class="answer-row" id="a1">'
            "<td>Qal</td><td>Perfect</td></tr></table>"
        )

        errors: list[str] = []
        warnings: list[str] = []
        validate_exercises.check_answer_row_empty(ex_dir, errors, warnings)
        assert errors == []

    def test_answer_row_with_no_text_is_a_blocking_error(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        # Caught in production on ch34-function-sort.html before this check
        # existed — an answer row that reveals nothing when clicked.
        monkeypatch.setattr(validate_exercises, "_REPO", tmp_path)
        ex_dir = tmp_path / "ch99-test-exercise"
        ex_dir.mkdir()
        (ex_dir / "ch99-test-exercise.html").write_text(
            '<table><tr class="answer-row" id="a1">'
            '<td></td><td>   </td></tr></table>'
        )

        errors: list[str] = []
        warnings: list[str] = []
        validate_exercises.check_answer_row_empty(ex_dir, errors, warnings)
        assert len(errors) == 1
        assert "a1" in errors[0]
        assert "no text content" in errors[0]


class TestCheckAnswerRowAlignment:
    def test_matching_cell_counts_are_not_flagged(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        monkeypatch.setattr(validate_exercises, "_REPO", tmp_path)
        ex_dir = tmp_path / "ch99-test-exercise"
        ex_dir.mkdir()
        (ex_dir / "ch99-test-exercise.html").write_text(
            "<table>"
            "<tr><td>1</td><td>Verb</td><td>Stem</td></tr>"
            '<tr class="answer-row" id="a1"><td>Qal</td><td>Perfect</td><td>3ms</td></tr>'
            "</table>"
        )

        errors: list[str] = []
        warnings: list[str] = []
        validate_exercises.check_answer_row_alignment(ex_dir, errors, warnings)
        assert warnings == []

    def test_bunched_answer_cells_are_flagged(self, tmp_path: Path, monkeypatch) -> None:
        # The exact rule from feedback_answer_row_columns: every answer-row
        # <td> must align cell-for-cell — never bunch content into fewer cells.
        monkeypatch.setattr(validate_exercises, "_REPO", tmp_path)
        ex_dir = tmp_path / "ch99-test-exercise"
        ex_dir.mkdir()
        (ex_dir / "ch99-test-exercise.html").write_text(
            "<table>"
            "<tr><td>1</td><td>Verb</td><td>Stem</td></tr>"
            '<tr class="answer-row" id="a1"><td>Qal Perfect 3ms</td></tr>'
            "</table>"
        )

        errors: list[str] = []
        warnings: list[str] = []
        validate_exercises.check_answer_row_alignment(ex_dir, errors, warnings)
        assert len(warnings) == 1
        assert "a1" in warnings[0]
        assert "1 <td> cells" in warnings[0]
        assert "question row has 3" in warnings[0]
