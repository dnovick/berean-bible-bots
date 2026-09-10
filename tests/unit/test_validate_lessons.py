"""Tests for scripts/validate_lessons.py — chapter.yml / exercise structure
checks. Known-good/known-bad, per docs/policies/test-coverage.md's priority
plan (issue #662).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import validate_lessons  # noqa: E402

_MINIMAL_CHAPTER_YML = """\
chapter: 99
course: bbh
title: Test Chapter
focus: Testing
flashcards: []
exercises: []
"""


class TestCheckChapter:
    def test_minimal_valid_chapter_has_no_errors(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(validate_lessons, "_REPO", tmp_path)
        ch_dir = tmp_path / "ch99"
        ch_dir.mkdir()
        (ch_dir / "chapter.yml").write_text(_MINIMAL_CHAPTER_YML)
        (ch_dir / "lesson.md").write_text("# Chapter 99\n")

        errors: list[str] = []
        warnings: list[str] = []
        validate_lessons._check_chapter(ch_dir, errors, warnings)
        assert errors == []
        assert warnings == []

    def test_missing_required_field_and_lesson_md_are_errors(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        monkeypatch.setattr(validate_lessons, "_REPO", tmp_path)
        ch_dir = tmp_path / "ch99"
        ch_dir.mkdir()
        # 'focus' omitted; lesson.md not created.
        (ch_dir / "chapter.yml").write_text(
            "chapter: 99\ncourse: bbh\ntitle: Test Chapter\n"
            "flashcards: []\nexercises: []\n"
        )

        errors: list[str] = []
        warnings: list[str] = []
        validate_lessons._check_chapter(ch_dir, errors, warnings)
        assert any("focus" in e for e in errors)
        assert any("lesson.md" in e for e in errors)

    def test_missing_flashcards_and_exercises_keys_are_warnings(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        # Omitting the keys entirely (vs. an explicit []) is a "possibly
        # forgotten" signal — a warning, not an error.
        monkeypatch.setattr(validate_lessons, "_REPO", tmp_path)
        ch_dir = tmp_path / "ch99"
        ch_dir.mkdir()
        (ch_dir / "chapter.yml").write_text(
            "chapter: 99\ncourse: bbh\ntitle: Test Chapter\nfocus: Testing\n"
        )
        (ch_dir / "lesson.md").write_text("# Chapter 99\n")

        errors: list[str] = []
        warnings: list[str] = []
        validate_lessons._check_chapter(ch_dir, errors, warnings)
        assert errors == []
        assert any("flashcards" in w for w in warnings)
        assert any("exercises" in w for w in warnings)


class TestCheckExercise:
    def test_complete_exercise_has_no_errors(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(validate_lessons, "_REPO", tmp_path)
        ex_dir = tmp_path / "ch99-test-exercise"
        ex_dir.mkdir()
        (ex_dir / "exercise.yml").write_text(
            "name: Test Exercise\ndescription: A test exercise.\n"
        )
        (ex_dir / "ch99-test-exercise.md").write_text("# Exercise\n")
        (ex_dir / "ch99-test-exercise.html").write_text("<html></html>\n")
        (ex_dir / "ch99-test-exercise.pdf").write_bytes(b"%PDF-1.4\n")

        errors: list[str] = []
        warnings: list[str] = []
        validate_lessons._check_exercise(ex_dir, errors, warnings)
        assert errors == []

    def test_missing_exercise_yml_and_formats_are_errors(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        monkeypatch.setattr(validate_lessons, "_REPO", tmp_path)
        ex_dir = tmp_path / "ch99-empty-exercise"
        ex_dir.mkdir()

        errors: list[str] = []
        warnings: list[str] = []
        validate_lessons._check_exercise(ex_dir, errors, warnings)
        assert any("exercise.yml" in e for e in errors)
        assert any(".html" in e for e in errors)
        assert any(".pdf" in e for e in errors)
        assert any(".md" in e for e in errors)
