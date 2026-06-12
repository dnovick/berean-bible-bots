#!/usr/bin/env python3
"""
Generate Anki flashcard decks for BBH chapters 1 and 2 from YAML source files.

Usage
-----
    python scripts/build_bbh_decks.py

Source data files (edit these to change card content):
    data/decks/bbh/ch1-alphabet-deck.yaml
    data/decks/bbh/ch2-vowels-deck.yaml

Output files (regenerated on every run):
    data/lessons/bbh/ch1/ch1-alphabet-deck.{md,txt,-fd.txt}
    data/lessons/bbh/ch2/ch2-vowels-deck.{md,txt,-fd.txt}

Formats
-------
.md      Human-readable card list in Markdown table format.
.txt     Anki import file (tab-separated, with #header directives).
-fd.txt  FlashDeck import file (tab-separated, deck name in column 3).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DECKS_DATA_DIR = _REPO_ROOT / "data" / "decks" / "bbh"
_LESSONS_DIR = _REPO_ROOT / "data" / "lessons" / "bbh"

_DECK_CONFIGS: list[tuple[str, str]] = [
    ("ch1-alphabet-deck.yaml", "ch1"),
    ("ch2-vowels-deck.yaml", "ch2"),
]


# ── Loading ───────────────────────────────────────────────────────────────────

def load_deck(yaml_path: Path) -> dict[str, Any]:
    with open(yaml_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _all_cards(deck: dict[str, Any]) -> list[dict[str, Any]]:
    """Flatten all cards across groups, injecting group-level tag."""
    cards = []
    for group in deck.get("groups", []):
        group_tag = group.get("tag", "")
        for card in group.get("cards", []):
            card_tags = list(card.get("tags") or [])
            if group_tag and group_tag not in card_tags:
                card_tags.insert(0, group_tag)
            cards.append({**card, "tags": card_tags})
    return cards


# ── Markdown (.md) ────────────────────────────────────────────────────────────

def render_md(deck: dict[str, Any]) -> str:
    meta = deck["deck"]
    lines = [
        f"# {meta['title']}",
        "",
        f"*{meta['description']}*  ",
        f"*Import `{meta['id']}.txt` directly into Anki (File → Import).*",
        "",
        "---",
        "",
        "## How to Use",
        "",
        "- **Front of card:** Hebrew character or syllable",
        "- **Back of card:** Name / transliteration / pronunciation",
        "- **Edit source:** `data/decks/bbh/{}.yaml`".format(meta["id"]),
        "- **Rebuild:** `python scripts/build_bbh_decks.py`",
        "",
        "---",
        "",
    ]

    for group in deck.get("groups", []):
        lines.append(f"## {group['name']}")
        lines.append("")
        desc = (group.get("description") or "").strip()
        if desc:
            lines.append(desc)
            lines.append("")
        lines += [
            "| # | Front (Hebrew) | Back |",
            "|---|---|---|",
        ]
        for i, card in enumerate(group.get("cards", []), 1):
            front = card["front"]
            back = card["back"].replace("|", "\\|")
            lines.append(f"| {i} | {front} | {back} |")
        lines.append("")

    return "\n".join(lines)


# ── Anki import (.txt) ────────────────────────────────────────────────────────

def render_anki_txt(deck: dict[str, Any]) -> str:
    meta = deck["deck"]
    prefix = meta["tags_prefix"]
    lines = [
        "#separator:tab",
        "#html:false",
        "#notetype:Basic",
        f"#deck:{meta['anki_deck']}",
        "#tags column:3",
        "",
    ]
    for card in _all_cards(deck):
        front = card["front"]
        back = card["back"]
        tags = [prefix] + [f"{prefix}-{t}" for t in card.get("tags", []) if t]
        lines.append(f"{front}\t{back}\t{' '.join(tags)}")
    return "\n".join(lines) + "\n"


# ── FlashDeck import (-fd.txt) ────────────────────────────────────────────────

def render_fd_txt(deck: dict[str, Any]) -> str:
    meta = deck["deck"]
    deck_name = meta["anki_deck"]
    lines = []
    for card in _all_cards(deck):
        lines.append(f"{card['front']}\t{card['back']}\t{deck_name}")
    return "\n".join(lines) + "\n"


# ── Main ──────────────────────────────────────────────────────────────────────

def build_deck(yaml_filename: str, chapter: str) -> None:
    yaml_path = _DECKS_DATA_DIR / yaml_filename
    deck = load_deck(yaml_path)
    deck_id = deck["deck"]["id"]
    out_dir = _LESSONS_DIR / chapter
    out_dir.mkdir(parents=True, exist_ok=True)

    md_path = out_dir / f"{deck_id}.md"
    txt_path = out_dir / f"{deck_id}.txt"
    fd_path = out_dir / f"{deck_id}-fd.txt"

    md_path.write_text(render_md(deck), encoding="utf-8")
    print(f"  Wrote {md_path.relative_to(_REPO_ROOT)}")

    txt_path.write_text(render_anki_txt(deck), encoding="utf-8")
    print(f"  Wrote {txt_path.relative_to(_REPO_ROOT)}")

    fd_path.write_text(render_fd_txt(deck), encoding="utf-8")
    print(f"  Wrote {fd_path.relative_to(_REPO_ROOT)}")

    total = sum(len(g.get("cards", [])) for g in deck.get("groups", []))
    print(f"    ({total} cards, {len(deck.get('groups', []))} groups)")


def main() -> None:
    print("Building BBH flashcard decks from YAML source files …")
    for yaml_filename, chapter in _DECK_CONFIGS:
        print(f"\n{yaml_filename}")
        build_deck(yaml_filename, chapter)
    print("\nDone.")


if __name__ == "__main__":
    main()
