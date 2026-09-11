"""Tests for scripts/build_research_page.py's pure logic — sorting,
tag extraction, and HTML row rendering for the research library index page.
Per docs/policies/test-coverage.md's priority plan (issue #676, Phase 2).
No I/O — all functions take plain dicts.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import build_research_page as brp  # noqa: E402


class TestSortKey:
    def test_sorts_by_author_last_name_then_year_then_title(self) -> None:
        papers = [
            {"author": "Waltke, B.", "year": "1990", "title": "Syntax"},
            {"author": "Andersen, F.", "year": "1970", "title": "Verbless Clauses"},
            {"author": "Waltke, B.", "year": "1985", "title": "Earlier Work"},
        ]
        ordered = sorted(papers, key=brp.sort_key)
        assert [p["title"] for p in ordered] == [
            "Verbless Clauses", "Earlier Work", "Syntax",
        ]

    def test_missing_author_sorts_last(self) -> None:
        papers = [
            {"author": "", "year": "2000", "title": "Anonymous"},
            {"author": "Andersen, F.", "year": "1970", "title": "Verbless Clauses"},
        ]
        ordered = sorted(papers, key=brp.sort_key)
        assert ordered[0]["title"] == "Verbless Clauses"
        assert ordered[1]["title"] == "Anonymous"


class TestBuildTagSet:
    def test_collects_unique_sorted_tags_across_papers(self) -> None:
        papers = [
            {"tags": "hebrew, syntax"},
            {"tags": "greek"},
            {"tags": "hebrew, poetry"},
        ]
        assert brp.build_tag_set(papers) == ["greek", "hebrew", "poetry", "syntax"]

    def test_handles_missing_or_empty_tags(self) -> None:
        papers = [{"tags": ""}, {}, {"tags": "aramaic"}]
        assert brp.build_tag_set(papers) == ["aramaic"]


class TestPaperRowHtml:
    def test_renders_linked_title_when_url_present(self) -> None:
        paper = {
            "title": "The Syntax of Masoretic Accents", "author": "Price, J.D.",
            "year": "1990", "journal": "Temple Baptist Seminary",
            "url": "https://example.com/paper.pdf", "tags": "hebrew, cantillation",
        }
        html = brp.paper_row_html(paper, 0)
        assert '<a href="https://example.com/paper.pdf"' in html
        assert "The Syntax of Masoretic Accents" in html
        assert 'data-tag="hebrew"' in html
        assert 'data-tag="cantillation"' in html
        assert 'data-lang="hebrew"' in html

    def test_renders_plain_title_when_no_url(self) -> None:
        paper = {"title": "Untitled Paper", "tags": "greek"}
        html = brp.paper_row_html(paper, 0)
        assert "<a href=" not in html
        assert "Untitled Paper" in html
        assert 'data-lang="greek"' in html

    def test_missing_title_falls_back_to_untitled(self) -> None:
        html = brp.paper_row_html({}, 0)
        assert "(untitled)" in html
        assert 'data-lang="other"' in html


class TestBuildPage:
    def test_produces_markdown_page_with_all_paper_titles_and_count(self) -> None:
        papers = [
            {"title": "Paper One", "author": "A, B", "year": "2000", "tags": "hebrew"},
            {"title": "Paper Two", "author": "C, D", "year": "2001", "tags": "greek"},
        ]
        page = brp.build_page(papers, brp.build_tag_set(papers))
        assert page.startswith("# Research Library")
        assert "Paper One" in page
        assert "Paper Two" in page
        assert "2 papers indexed" in page
