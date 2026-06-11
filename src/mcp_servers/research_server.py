#!/usr/bin/env python3
"""
MCP server: research-library

Exposes two tools to Claude Code:
  - search_literature(query, top_k=5)  — semantic search over indexed PDFs
  - get_indexed_sources()              — list all works in the index

Run via .claude/settings.local.json mcpServers entry; do not invoke directly.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

_REPO_ROOT = Path(__file__).resolve().parents[2]
_RESEARCH_DIR = _REPO_ROOT / "data" / "research"
_CHROMA_DIR = _RESEARCH_DIR / ".chromadb"
_MANIFEST_PATH = _RESEARCH_DIR / ".index_manifest.json"

COLLECTION_NAME = "research_library"
EMBED_MODEL = "text-embedding-3-small"

app = Server("research-library")


def _get_collection() -> Any:
    import chromadb
    from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
    api_key = os.environ.get("OPENAI_API_KEY", "")
    ef = OpenAIEmbeddingFunction(api_key=api_key, model_name=EMBED_MODEL)
    client = chromadb.PersistentClient(path=str(_CHROMA_DIR))
    return client.get_or_create_collection(COLLECTION_NAME, embedding_function=ef)  # type: ignore[arg-type]


def _load_manifest() -> dict:
    if _MANIFEST_PATH.exists():
        with open(_MANIFEST_PATH) as f:
            return json.load(f)
    return {}


def _not_indexed_msg() -> str:
    return (
        "The research library has not been indexed yet. "
        "Run: python scripts/index_research_library.py"
    )


# ── Tool definitions ──────────────────────────────────────────────────────────

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_literature",
            description=(
                "Semantic search over the indexed biblical-studies research library "
                "(reference grammars, commentaries, journal articles). Returns ranked "
                "excerpts with source title, author, page number, and relevance score. "
                "Use this when writing lesson explanations, verifying grammatical claims, "
                "or finding relevant bibliography."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "Natural-language search query. May include Hebrew/Greek terms, "
                            "grammar terminology, or topic descriptions."
                        ),
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of results to return (default: 5, max: 20).",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="get_indexed_sources",
            description=(
                "Return the list of all works currently in the research library index, "
                "with title, author, year, and chunk count. Use this to know what "
                "sources are available before searching."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


# ── Tool handlers ─────────────────────────────────────────────────────────────

@app.call_tool()
async def call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    arguments = arguments or {}

    if name == "search_literature":
        return await _search_literature(
            query=str(arguments.get("query", "")),
            top_k=min(int(arguments.get("top_k", 5)), 20),
        )

    if name == "get_indexed_sources":
        return _get_indexed_sources()

    raise ValueError(f"Unknown tool: {name}")


async def _search_literature(query: str, top_k: int) -> list[types.TextContent]:
    if not _CHROMA_DIR.exists():
        return [types.TextContent(type="text", text=_not_indexed_msg())]

    if not query.strip():
        return [types.TextContent(type="text", text="ERROR: query must not be empty.")]

    try:
        collection = _get_collection()
        results = collection.query(query_texts=[query], n_results=top_k)
    except Exception as e:
        return [types.TextContent(type="text", text=f"Search error: {e}")]

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if not docs:
        return [types.TextContent(
            type="text",
            text="No results found. Try a different query or check that documents are indexed.",
        )]

    lines = [f'Search results for: "{query}"\n']
    for i, (doc, meta, dist) in enumerate(zip(docs, metas, distances), 1):
        # ChromaDB L2 distance → approximate similarity 0–1
        score = max(0.0, 1.0 - (dist / 2.0))
        title = meta.get("title", "Unknown")
        author = meta.get("author", "")
        page = meta.get("page", "?")
        year = meta.get("year", "")

        citation = title
        if author:
            citation += f" ({author}"
            if year:
                citation += f", {year}"
            citation += ")"
        citation += f" — p. {page}"

        excerpt = doc.strip().replace("\n", " ")
        if len(excerpt) > 400:
            excerpt = excerpt[:400] + "…"

        lines.append(f"[{i}] {citation}  [score: {score:.2f}]")
        lines.append(f'"{excerpt}"')
        lines.append("")

    return [types.TextContent(type="text", text="\n".join(lines))]


def _get_indexed_sources() -> list[types.TextContent]:
    manifest = _load_manifest()
    if not manifest:
        return [types.TextContent(type="text", text=_not_indexed_msg())]

    lines = [f"{len(manifest)} source(s) in the research library:\n"]
    for entry in manifest.values():
        title = entry.get("title", "Unknown")
        author = entry.get("author", "")
        year = entry.get("year", "")
        tags = entry.get("tags", "")
        chunks = entry.get("chunk_count", 0)
        filename = Path(entry.get("path", "")).name

        line = f"  • {title}"
        if author:
            line += f"  |  {author}"
        if year:
            line += f"  |  {year}"
        if tags:
            line += f"  |  [{tags}]"
        line += f"  |  {chunks} chunks  |  {filename}"
        lines.append(line)

    return [types.TextContent(type="text", text="\n".join(lines))]


# ── Entry point ───────────────────────────────────────────────────────────────

async def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        print(
            "ERROR: OPENAI_API_KEY environment variable is not set.",
            file=sys.stderr,
        )
        sys.exit(1)

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
