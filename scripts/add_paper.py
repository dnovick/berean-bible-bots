#!/usr/bin/env python3
"""
Add a research paper to the library.

Steps
-----
1. Extract text from the PDF (first 6 pages).
2. Use Claude (Haiku) to infer metadata: title, author, year, journal, tags, url.
3. Confirm or edit each field interactively (skip with --yes).
4. Append the entry to data/research/bibliography.json.
5. Index the PDF for semantic search (index_research_library.py).
6. Rebuild the research website page (build_research_page.py).

Usage
-----
    python scripts/add_paper.py paper.pdf          # interactive
    python scripts/add_paper.py paper.pdf --yes    # auto-accept inferred metadata
    python scripts/add_paper.py --scan             # process all un-registered PDFs
    python scripts/add_paper.py --scan --yes       # fully automatic batch
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[1]
_RESEARCH_DIR = _REPO_ROOT / "data" / "research"
_BIBLIO_PATH = _RESEARCH_DIR / "bibliography.json"

# Maximum characters of PDF text sent to Claude for metadata inference.
_INFER_CHARS = 4000
# Pages to read for metadata inference.
_INFER_PAGES = 6


# ── Bibliography helpers ───────────────────────────────────────────────────────

def _load_biblio() -> List[Dict[str, Any]]:
    if _BIBLIO_PATH.exists():
        with open(_BIBLIO_PATH, encoding="utf-8") as f:
            return json.load(f)
    return []


def _save_biblio(entries: List[Dict[str, Any]]) -> None:
    entries_sorted = sorted(entries, key=lambda e: e.get("filename", ""))
    with open(_BIBLIO_PATH, "w", encoding="utf-8") as f:
        json.dump(entries_sorted, f, indent=2, ensure_ascii=False)


def _registered_filenames(entries: List[Dict[str, Any]]) -> set:
    return {e["filename"] for e in entries if "filename" in e}


# ── PDF text extraction ────────────────────────────────────────────────────────

def _extract_text(pdf_path: Path, max_pages: int = _INFER_PAGES) -> str:
    """Return up to max_pages pages of text from the PDF."""
    try:
        import fitz  # noqa: PLC0415
    except ImportError:
        print("ERROR: PyMuPDF not installed (pip install pymupdf)", file=sys.stderr)
        sys.exit(1)

    parts: List[str] = []
    with fitz.open(str(pdf_path)) as doc:
        for i, page in enumerate(doc):
            if i >= max_pages:
                break
            text = page.get_text()
            if text.strip():
                parts.append(text)
    return "\n".join(parts)


# ── Metadata inference via Claude ──────────────────────────────────────────────

_SYSTEM_PROMPT = (
    "You are a bibliographic metadata extractor. "
    "Given the first few pages of an academic paper, return a JSON object with these fields: "
    "title, author (Last, First or Last, F. format; multiple authors comma-separated), "
    "year (4-digit string or empty), journal (journal/book/publisher name or empty), "
    "tags (comma-separated lowercase keywords from: phonology, morphology, syntax, semantics, "
    "discourse, verbal, grammar, hebrew, aramaic, greek, lexical, diachronic, accents, "
    "cantillation, pedagogy, typology, northwest-semitic, and any other relevant terms), "
    "url (a stable public URL for the paper if you are confident, else empty string). "
    "Return ONLY the JSON object, no explanation."
)


def _infer_metadata(text: str) -> Dict[str, str]:
    """Call Claude Haiku to infer paper metadata from extracted text."""
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("WARNING: ANTHROPIC_API_KEY not set — metadata inference skipped.")
        return {}

    client = anthropic.Anthropic(api_key=api_key)
    snippet = text[:_INFER_CHARS]

    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": snippet}],
        )
        block = msg.content[0]
        raw = getattr(block, "text", "").strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw) if raw else {}
    except Exception as exc:
        print(f"WARNING: metadata inference failed ({exc}) — using empty values.")
        return {}


# ── Interactive confirmation ───────────────────────────────────────────────────

_FIELDS = ["title", "author", "year", "journal", "tags", "url"]


def _prompt_field(field: str, suggested: str) -> str:
    """Show suggested value and let user accept (Enter) or type a replacement."""
    display = suggested or "(none)"
    print(f"  {field}: {display}")
    raw = input(f"    → keep / edit [{field}]: ").strip()
    return raw if raw else suggested


def _confirm_metadata(
    suggested: Dict[str, Any], auto: bool
) -> Dict[str, str]:
    result: Dict[str, str] = {}
    print()
    print("  Inferred metadata:")
    if auto:
        for field in _FIELDS:
            result[field] = str(suggested.get(field, "") or "")
            print(f"    {field}: {result[field] or '(none)'}")
    else:
        print("  Press Enter to accept each value, or type a replacement.")
        print()
        for field in _FIELDS:
            result[field] = _prompt_field(field, str(suggested.get(field, "") or ""))
    return result


# ── Pipeline steps ─────────────────────────────────────────────────────────────

def _run_indexer(pdf_path: Path) -> bool:
    """Run index_research_library.py for the given PDF. Returns True on success."""
    script = _REPO_ROOT / "scripts" / "index_research_library.py"
    result = subprocess.run(
        [sys.executable, str(script), "--add", str(pdf_path)],
        capture_output=False,
    )
    return result.returncode == 0


def _run_page_builder() -> bool:
    """Run build_research_page.py. Returns True on success."""
    script = _REPO_ROOT / "scripts" / "build_research_page.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=False,
    )
    return result.returncode == 0


# ── Main processing function ───────────────────────────────────────────────────

def process_paper(pdf_path: Path, auto: bool = False) -> bool:
    """
    Full pipeline for one PDF.  Returns True if the paper was newly added.
    """
    biblio = _load_biblio()
    if pdf_path.name in _registered_filenames(biblio):
        print(f"  Already in bibliography — skipping: {pdf_path.name}")
        return False

    print(f"\n{'=' * 60}")
    print(f"Processing: {pdf_path.name}")
    print(f"{'=' * 60}")

    # 1. Extract text
    print("  Extracting text …")
    text = _extract_text(pdf_path)
    if not text.strip():
        print("  WARNING: no text extracted (scanned PDF?). Fill in metadata manually.")
        text = ""

    # 2. Infer metadata
    print("  Inferring metadata via Claude …")
    suggested = _infer_metadata(text) if text else {}

    # 3. Confirm / edit
    meta = _confirm_metadata(suggested, auto)
    meta["filename"] = pdf_path.name

    # 4. Add to bibliography
    biblio.append(meta)
    _save_biblio(biblio)
    print("\n  ✓ Added to bibliography.json")

    # 5. Semantic index
    print("\n  Running semantic indexer …")
    ok = _run_indexer(pdf_path)
    if not ok:
        print("  WARNING: indexer returned non-zero exit code.")

    # 6. Rebuild page
    print("\n  Rebuilding research page …")
    ok = _run_page_builder()
    if not ok:
        print("  WARNING: page builder returned non-zero exit code.")

    print(f"\n  ✓ Done: {pdf_path.name}")
    return True


def scan_and_process(auto: bool = False) -> None:
    """Process all PDFs in data/research/ not yet in bibliography.json."""
    biblio = _load_biblio()
    registered = _registered_filenames(biblio)
    pdfs = sorted(_RESEARCH_DIR.glob("*.pdf"))

    new_pdfs = [p for p in pdfs if p.name not in registered]
    if not new_pdfs:
        print("All PDFs already registered. Nothing to do.")
        return

    print(f"Found {len(new_pdfs)} unregistered PDF(s).")
    for pdf in new_pdfs:
        process_paper(pdf, auto=auto)

    print("\nScan complete.")


# ── CLI ────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add a research paper to the Berean Bible Bots library.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "pdf",
        nargs="?",
        metavar="PDF",
        help="Path to the PDF file to add (omit with --scan)",
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Auto-accept inferred metadata without prompting",
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Process all PDFs in data/research/ not yet in bibliography.json",
    )
    args = parser.parse_args()

    if args.scan:
        scan_and_process(auto=args.yes)
    elif args.pdf:
        pdf_path = Path(args.pdf).expanduser().resolve()
        if not pdf_path.exists():
            print(f"ERROR: file not found: {pdf_path}", file=sys.stderr)
            sys.exit(1)
        process_paper(pdf_path, auto=args.yes)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
