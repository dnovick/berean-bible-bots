"""Tests for scripts/validate_courses.py — course instance.yml structure
checks. Known-good/known-bad, per docs/policies/test-coverage.md's priority
plan (issue #662).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import validate_courses  # noqa: E402


class TestCheckInstanceYml:
    def test_all_required_fields_present_has_no_errors(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        monkeypatch.setattr(validate_courses, "_REPO", tmp_path)
        instance_dir = tmp_path / "bbh-2026.1"
        instance_dir.mkdir()
        instance_yml = instance_dir / "instance.yml"
        instance_yml.write_text(
            "id: bbh-2026.1\nname: BBH Fall 2026\ntextbook: bbh\n"
        )

        errors: list[str] = []
        warnings: list[str] = []
        validate_courses._check_instance_yml(instance_yml, errors, warnings)
        assert errors == []

    def test_missing_required_field_is_an_error(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        monkeypatch.setattr(validate_courses, "_REPO", tmp_path)
        instance_dir = tmp_path / "bbh-2026.1"
        instance_dir.mkdir()
        instance_yml = instance_dir / "instance.yml"
        # 'textbook' omitted.
        instance_yml.write_text("id: bbh-2026.1\nname: BBH Fall 2026\n")

        errors: list[str] = []
        warnings: list[str] = []
        validate_courses._check_instance_yml(instance_yml, errors, warnings)
        assert len(errors) == 1
        assert "textbook" in errors[0]

    def test_malformed_yaml_is_an_error(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(validate_courses, "_REPO", tmp_path)
        instance_dir = tmp_path / "bbh-2026.1"
        instance_dir.mkdir()
        instance_yml = instance_dir / "instance.yml"
        instance_yml.write_text("id: [unclosed\n")

        errors: list[str] = []
        warnings: list[str] = []
        validate_courses._check_instance_yml(instance_yml, errors, warnings)
        assert len(errors) == 1
        assert "YAML parse error" in errors[0]
