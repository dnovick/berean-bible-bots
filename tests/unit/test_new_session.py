"""Tests for scripts/new_session.py's course-lookup and session-numbering
helpers. Per docs/policies/test-coverage.md's priority plan (issue #676,
Phase 2). Mostly tmp fixtures (via monkeypatching _COURSES_DIR); one
cross-check against the real data/courses/ tree.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import new_session as ns  # noqa: E402

_COURSES_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "courses"


class TestIsCourseDir:
    def test_true_for_dir_with_course_yml(self, tmp_path: Path) -> None:
        (tmp_path / "course.yml").write_text("name: Test\n")
        assert ns._is_course_dir(tmp_path) is True

    def test_true_for_dir_with_instance_yml(self, tmp_path: Path) -> None:
        (tmp_path / "instance.yml").write_text("id: test\n")
        assert ns._is_course_dir(tmp_path) is True

    def test_false_for_plain_directory(self, tmp_path: Path) -> None:
        assert ns._is_course_dir(tmp_path) is False

    def test_false_for_non_directory(self, tmp_path: Path) -> None:
        f = tmp_path / "not-a-dir.txt"
        f.write_text("x")
        assert ns._is_course_dir(f) is False


class TestFindCourseDirAndListCourseIds:
    def _make_grouped_course(self, tmp_path: Path) -> Path:
        group = tmp_path / "bbh"
        group.mkdir()
        (group / "course.yml").write_text("name: BBH\n")
        instance = group / "bbh-2026.1"
        instance.mkdir()
        (instance / "instance.yml").write_text("id: bbh-2026.1\n")
        return instance

    def test_finds_direct_ungrouped_course(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(ns, "_COURSES_DIR", tmp_path)
        course_dir = tmp_path / "solo-course"
        course_dir.mkdir()
        (course_dir / "instance.yml").write_text("id: solo-course\n")

        assert ns._find_course_dir("solo-course") == course_dir

    def test_missing_course_raises_systemexit_listing_available(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(ns, "_COURSES_DIR", tmp_path)
        course_dir = tmp_path / "solo-course"
        course_dir.mkdir()
        (course_dir / "instance.yml").write_text("id: solo-course\n")

        with pytest.raises(SystemExit, match="solo-course"):
            ns._find_course_dir("does-not-exist")

    def test_list_course_ids_returns_group_name_when_course_yml_present(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        # A group directory with its own course.yml (like the real
        # data/courses/bbh/) is itself listed, not descended into — the
        # group qualifies as a "course dir" on its own via _is_course_dir.
        monkeypatch.setattr(ns, "_COURSES_DIR", tmp_path)
        self._make_grouped_course(tmp_path)
        assert ns._list_course_ids() == "bbh"

    def test_list_course_ids_descends_into_ungrouped_subdirs(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        # Without a course.yml at the group level, descend one level to
        # find real instance directories.
        monkeypatch.setattr(ns, "_COURSES_DIR", tmp_path)
        group = tmp_path / "bbg"
        group.mkdir()
        instance = group / "bbg-2026.1"
        instance.mkdir()
        (instance / "instance.yml").write_text("id: bbg-2026.1\n")

        assert ns._list_course_ids() == "bbg-2026.1"


@pytest.mark.integration
class TestRealCoursesDirCrossCheck:
    def test_real_data_courses_lists_bbh(self) -> None:
        if not _COURSES_DATA_DIR.exists():
            pytest.skip(f"Data directory not found: {_COURSES_DATA_DIR}")
        assert "bbh" in ns._list_course_ids()


class TestNextSessionNumber:
    def test_first_session_when_no_existing_directories(self, tmp_path: Path) -> None:
        assert ns._next_session_number(tmp_path) == 1

    def test_derives_next_number_from_existing_session_dirs(self, tmp_path: Path) -> None:
        (tmp_path / "session-01").mkdir()
        (tmp_path / "session-02").mkdir()
        (tmp_path / "session-05").mkdir()
        assert ns._next_session_number(tmp_path) == 6

    def test_ignores_non_session_directories(self, tmp_path: Path) -> None:
        (tmp_path / "session-03").mkdir()
        (tmp_path / "common").mkdir()
        assert ns._next_session_number(tmp_path) == 4
