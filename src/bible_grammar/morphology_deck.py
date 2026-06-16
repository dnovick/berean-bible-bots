"""
Reusable morphology flashcard deck generator.

Produces three output formats from a single list of DeckCard objects:
  .md       — static reference table with answer key
  .txt      — Anki tab-separated import (verbose back)
  -fd.txt   — Foreign Deck format (structured back)

Usage from a chapter script:
    from bible_grammar.morphology_deck import DeckCard, DeckConfig, MorphologyDeckWriter
    cards = [DeckCard(...), ...]
    config = DeckConfig(...)
    MorphologyDeckWriter(config, cards).write_all(
        Path("data/lessons/bbh/ch29"), "ch29-morphology-deck"
    )
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


@dataclass
class DeckCard:
    num: int
    front: str      # pointed Hebrew form (no ref suffix)
    ref: str        # OT reference or "paradigm"
    root: str       # unpointed root, or "—" for contrast cards
    stem: str       # e.g. "Hophal"
    conj: str       # e.g. "Perfect", "Formula", "—"
    pgn: str        # e.g. "3ms", "—"
    gloss: str      # English gloss
    section: str    # section heading for .md grouping (e.g. "PERFECT")
    tag: str        # space-separated Anki tags
    back_txt: str   # narrative back text for .txt import
    back_fd: str    # structured back text for -fd.txt import


@dataclass
class DeckConfig:
    chapter: int
    stem: str
    quality: str            # e.g. "Strong" or "Weak"
    deck_name: str          # e.g. "BBH Chapter 29 — Hophal Weak"
    description: str        # multi-line .md header block
    diagnostics: List[Tuple[str, str]]   # (front-label, back-text) for summary table
    coverage: List[dict]    # {conj, detail, cards} rows for coverage table


class MorphologyDeckWriter:
    def __init__(self, config: DeckConfig, cards: List[DeckCard]) -> None:
        self.config = config
        self.cards = cards

    def _grouped(self) -> List[Tuple[str, List[DeckCard]]]:
        seen: dict = {}
        order: List[str] = []
        for card in self.cards:
            if card.section not in seen:
                seen[card.section] = []
                order.append(card.section)
            seen[card.section].append(card)
        return [(s, seen[s]) for s in order]

    def write_md(self, path: Path) -> None:
        c = self.config
        lines = [
            f"# Chapter {c.chapter} — {c.stem} {c.quality} Verb Morphology Deck",
            "",
        ]
        lines += c.description.strip().splitlines()
        lines += [
            "",
            "---",
            "",
            "## Key Diagnostic Summary",
            "",
            "| Card Front | Expected Back |",
            "|---|---|",
        ]
        for front, back in c.diagnostics:
            lines.append(f"| {front} | {back} |")
        lines += [
            "",
            "---",
            "",
            "## Card List",
            "",
            "| # | Front — Pointed Form | Reference | Root | Stem | Conjugation | PGN | Gloss |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for section, group in self._grouped():
            lines.append(f"| **{section}** | | | | | | | |")
            for card in group:
                lines.append(
                    f"| {card.num} | {card.front} | {card.ref} | "
                    f"{card.root} | {card.stem} | {card.conj} | {card.pgn} | {card.gloss} |"
                )
        lines += [
            "",
            "---",
            "",
            "## Conjugation / Class Coverage",
            "",
            "| Conjugation | Weak classes / roots drilled | Cards |",
            "|---|---|---|",
        ]
        for row in c.coverage:
            lines.append(f"| {row['conj']} | {row['detail']} | {row['cards']} |")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_txt(self, path: Path) -> None:
        c = self.config
        lines = [
            "#separator:tab",
            "#html:false",
            "#notetype:Basic",
            f"#deck:{c.deck_name}",
            "#tags column:3",
            "",
        ]
        for card in self.cards:
            front = f"{card.front} ({card.ref})"
            lines.append(f"{front}\t{card.back_txt}\t{card.tag}")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_fd(self, path: Path) -> None:
        c = self.config
        lines = [
            "#separator:tab",
            "#html:false",
            "#notetype:Basic",
            f"#deck:{c.deck_name}",
            "#tags column:3",
            "",
        ]
        for card in self.cards:
            front = f"{card.front} ({card.ref})"
            lines.append(f"{front}\t{card.back_fd}\t{c.deck_name}")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_all(self, out_dir: Path, prefix: str) -> None:
        """Write .md, .txt, and -fd.txt to out_dir with the given filename prefix."""
        out_dir.mkdir(parents=True, exist_ok=True)
        self.write_md(out_dir / f"{prefix}.md")
        self.write_txt(out_dir / f"{prefix}.txt")
        self.write_fd(out_dir / f"{prefix}-fd.txt")
        print(f"Wrote {out_dir}/{prefix}.[md,txt,-fd.txt]")
