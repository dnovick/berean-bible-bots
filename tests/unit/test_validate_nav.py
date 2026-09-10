"""Tests for scripts/validate_nav.py — mkdocs_nav.yml reference resolution.
Known-good/known-bad, per docs/policies/test-coverage.md's priority plan
(issue #662).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import validate_nav  # noqa: E402


class TestCollectPaths:
    def test_flattens_nested_nav_tree(self) -> None:
        nav = [
            {"Policies": [
                {"Autonomous Actions": "policies/autonomous-actions.md"},
                {"Test Coverage": "policies/test-coverage.md"},
            ]},
            "index.md",
        ]
        found: list[str] = []
        validate_nav._collect_paths(nav, found)
        assert set(found) == {
            "policies/autonomous-actions.md",
            "policies/test-coverage.md",
            "index.md",
        }


class TestMain:
    def _setup_nav(self, tmp_path: Path, monkeypatch, nav_yaml: str) -> None:
        docs_dir = tmp_path / "mkdocs_src"
        docs_dir.mkdir()
        nav_file = tmp_path / "mkdocs_nav.yml"
        nav_file.write_text(nav_yaml)
        monkeypatch.setattr(validate_nav, "_NAV_FILE", nav_file)
        monkeypatch.setattr(validate_nav, "_DOCS_DIR", docs_dir)
        monkeypatch.setattr(sys, "argv", ["validate_nav.py"])
        return docs_dir

    def test_all_referenced_files_present_passes(self, tmp_path, monkeypatch, capsys) -> None:
        docs_dir = self._setup_nav(tmp_path, monkeypatch, "- Home: index.md\n")
        (docs_dir / "index.md").write_text("# Home\n")

        exit_code = validate_nav.main()
        assert exit_code == 0
        assert "OK" in capsys.readouterr().out

    def test_missing_tracked_file_is_an_error(self, tmp_path, monkeypatch, capsys) -> None:
        self._setup_nav(tmp_path, monkeypatch, "- Missing: does-not-exist.md\n")
        # Not gitignored (tmp_path isn't inside a git repo at all — git
        # check-ignore returns a non-match, i.e. "not ignored").
        monkeypatch.setattr(validate_nav, "_is_gitignored", lambda path: False)

        exit_code = validate_nav.main()
        out = capsys.readouterr().out
        assert exit_code == 1
        assert "does-not-exist.md" in out
        assert "ERROR" in out

    def test_missing_gitignored_file_is_a_warning_not_an_error(
        self, tmp_path, monkeypatch, capsys
    ) -> None:
        self._setup_nav(tmp_path, monkeypatch, "- Generated: reports/foo.md\n")
        monkeypatch.setattr(validate_nav, "_is_gitignored", lambda path: True)

        exit_code = validate_nav.main()
        out = capsys.readouterr().out
        assert exit_code == 0
        assert "reports/foo.md" in out
        assert "WARN" in out
