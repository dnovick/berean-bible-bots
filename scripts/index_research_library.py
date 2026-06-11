#!/usr/bin/env python3
"""
Index PDF documents in data/research/ into a ChromaDB vector store
using OpenAI text-embedding-3-small embeddings.

Usage
-----
# Scan data/research/ and index any new PDFs:
    python scripts/index_research_library.py

# Index a single file with rich metadata (recommended for major reference works):
    python scripts/index_research_library.py \
        --add path/to/gkc.pdf \
        --title "Gesenius' Hebrew Grammar" \
        --author "Gesenius, W. / Kautzsch, E." \
        --year 1910 \
        --tags "grammar,hebrew,morphology"
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import textwrap
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[1]
_RESEARCH_DIR = _REPO_ROOT / "data" / "research"
_CHROMA_DIR = _RESEARCH_DIR / ".chromadb"
_MANIFEST_PATH = _RESEARCH_DIR / ".index_manifest.json"

COLLECTION_NAME = "research_library"
EMBED_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 900       # characters
CHUNK_OVERLAP = 120    # characters


# ── Helpers ───────────────────────────────────────────────────────────────────

def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()[:20]


def _load_manifest() -> dict:
    if _MANIFEST_PATH.exists():
        with open(_MANIFEST_PATH) as f:
            return json.load(f)
    return {}


def _save_manifest(manifest: dict) -> None:
    with open(_MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)


def _chunk_text(text: str) -> list[str]:
    """Split text into overlapping character chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def _extract_pages(pdf_path: Path) -> list[tuple[int, str]]:
    """Return list of (page_number, text) for each page."""
    import fitz  # PyMuPDF
    pages = []
    with fitz.open(str(pdf_path)) as doc:
        for i, page in enumerate(doc, 1):
            text = page.get_text()
            if text.strip():
                pages.append((i, text))
    return pages


# ── Core indexing ─────────────────────────────────────────────────────────────

def _get_collection(api_key: str) -> Any:
    import chromadb
    from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
    client = chromadb.PersistentClient(path=str(_CHROMA_DIR))
    ef = OpenAIEmbeddingFunction(api_key=api_key, model_name=EMBED_MODEL)
    return client.get_or_create_collection(COLLECTION_NAME, embedding_function=ef)  # type: ignore[arg-type]


def index_file(
    pdf_path: Path,
    title: str | None = None,
    author: str | None = None,
    year: int | None = None,
    tags: str | None = None,
    api_key: str | None = None,
    force: bool = False,
) -> int:
    """Index a single PDF. Returns number of chunks added (0 if already indexed)."""
    api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    manifest = _load_manifest()
    file_hash = _sha256(pdf_path)

    if file_hash in manifest and not force:
        print(f"  Already indexed: {pdf_path.name} — skipping (use --force to re-index)")
        return 0

    title = title or pdf_path.stem
    author = author or ""
    year_str = str(year) if year else ""
    tags = tags or ""

    print(f"  Extracting text from {pdf_path.name} …")
    pages = _extract_pages(pdf_path)
    if not pages:
        print(f"  WARNING: no text extracted from {pdf_path.name} — may be a scanned PDF")
        return 0

    collection = _get_collection(api_key)

    # Remove old chunks for this file if re-indexing
    if file_hash in manifest and force:
        old_ids = [f"{file_hash}_{i}" for i in range(manifest[file_hash]["chunk_count"])]
        collection.delete(ids=old_ids)

    documents, metadatas, ids = [], [], []
    chunk_idx = 0
    for page_num, page_text in pages:
        for chunk in _chunk_text(page_text):
            doc_id = f"{file_hash}_{chunk_idx}"
            documents.append(chunk)
            metadatas.append({
                "title":    title,
                "author":   author,
                "year":     year_str,
                "tags":     tags,
                "page":     page_num,
                "filename": pdf_path.name,
                "file_hash": file_hash,
            })
            ids.append(doc_id)
            chunk_idx += 1

    # ChromaDB add in batches of 100 to stay within API rate limits
    batch = 100
    for i in range(0, len(documents), batch):
        collection.add(
            documents=documents[i:i + batch],
            metadatas=metadatas[i:i + batch],
            ids=ids[i:i + batch],
        )
        print(f"    Embedded chunks {i + 1}–{min(i + batch, len(documents))} / {len(documents)}")

    manifest[file_hash] = {
        "path":        str(pdf_path),
        "title":       title,
        "author":      author,
        "year":        year_str,
        "tags":        tags,
        "chunk_count": chunk_idx,
    }
    _save_manifest(manifest)
    print(f"  Done: {chunk_idx} chunks indexed for '{title}'")
    return chunk_idx


def scan_and_index(api_key: str | None = None) -> None:
    """Scan data/research/ for PDFs and index any not yet in the manifest."""
    pdfs = sorted(_RESEARCH_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found in {_RESEARCH_DIR}")
        print("Drop PDF files there and re-run.")
        return

    manifest = _load_manifest()
    new_count = 0
    for pdf in pdfs:
        file_hash = _sha256(pdf)
        if file_hash in manifest:
            print(f"  Skipping (already indexed): {pdf.name}")
        else:
            print(f"Indexing: {pdf.name}")
            index_file(pdf, api_key=api_key)
            new_count += 1

    if new_count == 0:
        print("All PDFs already indexed. Nothing to do.")
    else:
        print(f"\nDone. {new_count} new document(s) indexed.")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(__doc__ or ""),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--add",    metavar="PATH", help="Path to PDF to index")
    parser.add_argument("--title",  help="Title of the work (default: filename)")
    parser.add_argument("--author", help="Author(s)")
    parser.add_argument("--year",   type=int, help="Publication year")
    parser.add_argument("--tags",   help="Comma-separated tags (e.g. grammar,hebrew)")
    parser.add_argument("--force",  action="store_true", help="Re-index even if already present")
    parser.add_argument("--list",   action="store_true", help="List indexed sources and exit")
    args = parser.parse_args()

    if args.list:
        manifest = _load_manifest()
        if not manifest:
            print("No documents indexed yet.")
        else:
            for entry in manifest.values():
                print(f"  {entry['title']}")
                if entry.get("author"):
                    print(f"    Author : {entry['author']}")
                if entry.get("year"):
                    print(f"    Year   : {entry['year']}")
                print(f"    Chunks : {entry['chunk_count']}")
                print(f"    File   : {Path(entry['path']).name}")
                print()
        return

    if args.add:
        pdf_path = Path(args.add).expanduser().resolve()
        if not pdf_path.exists():
            print(f"ERROR: file not found: {pdf_path}", file=sys.stderr)
            sys.exit(1)
        print(f"Indexing: {pdf_path.name}")
        index_file(
            pdf_path,
            title=args.title,
            author=args.author,
            year=args.year,
            tags=args.tags,
            force=args.force,
        )
    else:
        scan_and_index()


if __name__ == "__main__":
    main()
