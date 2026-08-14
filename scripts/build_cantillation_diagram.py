"""
Build cantillation hierarchy diagrams for one or more verses.

Usage
-----
# One verse:
python scripts/build_cantillation_diagram.py Gen 1 1

# A chapter range (generates all verses in Gen 1):
python scripts/build_cantillation_diagram.py Gen 1

# A book (generates all verses in Genesis):
python scripts/build_cantillation_diagram.py Gen

# Multiple explicit references:
python scripts/build_cantillation_diagram.py Gen 1 1 Gen 1 2 Exo 20 1

Output is written to reports/ot/cantillation/<book>/<book>_<ch>_<vs>.png
A CSV index is written to reports/ot/cantillation/index.csv
"""

import argparse
import csv
import sys
from pathlib import Path

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.bible_grammar.ot.cantillation import (  # noqa: E402
    PROSE_BOOKS, AccentNode, parse_verse, render_verse,
)
from src.bible_grammar.core.syntax_ot import query_syntax_ot  # noqa: E402

OUTPUT_ROOT = Path('output/reports/ot/cantillation')


from typing import Generator, Tuple  # noqa: E402


def _verse_refs(
    book: str, chapter: int | None, verse: int | None
) -> Generator[Tuple[str, int, int], None, None]:
    """Yield (book, chapter, verse) tuples for the requested scope."""
    df = query_syntax_ot(book=book, chapter=chapter, verse=verse)
    if df.empty:
        scope = f'{book}'
        if chapter:
            scope += f' {chapter}'
        if verse:
            scope += f':{verse}'
        print(f'  WARNING: no data found for {scope}', file=sys.stderr)
        return
    for (b, ch, vs) in (
        df[['book', 'chapter', 'verse']].drop_duplicates().itertuples(index=False)
    ):
        yield str(b), int(ch), int(vs)


def build_one(book: str, chapter: int, verse: int) -> dict:
    """Build one diagram; return a dict row for the CSV index."""
    if book in {'Psa', 'Pro', 'Job'}:
        print(f'  SKIP {book} {chapter}:{verse} — poetic accent system')
        return {}
    out = OUTPUT_ROOT / book / f'{book}_{chapter:02d}_{verse:02d}.png'
    try:
        tree = parse_verse(book, chapter, verse)
        render_verse(book, chapter, verse, output_path=out)

        def _count(n: 'AccentNode', acc: int = 0) -> int:
            return acc + 1 + sum(_count(c) for c in n.children)
        node_count = _count(tree)
        word_count = sum(1 for _ in _collect_words_flat(tree))
        print(f'  OK  {book} {chapter}:{verse}  ({node_count} nodes, {word_count} words)')
        return {
            'book': book, 'chapter': chapter, 'verse': verse,
            'png': str(out), 'nodes': node_count, 'words': word_count,
        }
    except Exception as exc:
        print(f'  ERR {book} {chapter}:{verse} — {exc}', file=sys.stderr)
        return {}


def _collect_words_flat(node: AccentNode) -> Generator:
    yield from node.words
    for child in node.children:
        yield from _collect_words_flat(child)


def write_index(rows: list[dict]) -> None:
    if not rows:
        return
    index_path = OUTPUT_ROOT / 'index.csv'
    fieldnames = ['book', 'chapter', 'verse', 'png', 'nodes', 'words']
    with open(index_path, 'w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f'\nIndex written → {index_path}')


def write_readme(rows: list[dict]) -> None:
    """Write the top-level README with per-book sections embedding each diagram."""
    if not rows:
        return
    books_seen = sorted({r['book'] for r in rows})
    readme = OUTPUT_ROOT / 'README.md'

    # Group rows by book, then sort by chapter/verse within each book
    from collections import defaultdict
    by_book: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_book[r['book']].append(r)
    for b in by_book:
        by_book[b].sort(key=lambda r: (r['chapter'], r['verse']))

    lines = [
        '# Cantillation Diagrams',
        '',
        'Hierarchical accent structure diagrams generated from the MACULA WLC text,',
        'following J.D. Price, *The Syntax of Masoretic Accents in the Hebrew Bible*',
        '(Temple Baptist Seminary, 2nd ed., 1990/2010).',
        '',
        'Each diagram shows the verse\'s accent hierarchy rooted at **SOP** (Soph Pasuq).',
        'Words are displayed in right-to-left order matching Hebrew. Accent labels use',
        'Price\'s H1–H5 abbreviations; color coding: red=H1, orange=H2, amber=H3,',
        'green=H4, blue=H5, grey=conjunctive.',
        '',
        '## Contents',
        '',
    ]
    for b in books_seen:
        n = len(by_book[b])
        lines.append(f'- [{b}](#{b.lower()}) — {n} verse(s)')
    lines.append('')

    for b in books_seen:
        lines += [f'## {b}', '']
        for r in by_book[b]:
            ch, vs = r['chapter'], r['verse']
            png_rel = f'{b}/{b}_{ch:02d}_{vs:02d}.png'
            lines += [
                f'### {b} {ch}:{vs}',
                '',
                f'![{b} {ch}:{vs} cantillation diagram]({png_rel})',
                '',
            ]

    lines += [
        '---',
        '',
        '## Build',
        '',
        '```bash',
        '# One verse:',
        'python scripts/build_cantillation_diagram.py Gen 1 1',
        '# A chapter:',
        'python scripts/build_cantillation_diagram.py Gen 1',
        '# A whole book:',
        'python scripts/build_cantillation_diagram.py Gen',
        '```',
        '',
        'See `index.csv` for a machine-readable inventory of all generated files.',
    ]
    readme.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'README  written → {readme}')


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Generate cantillation hierarchy diagrams.',
    )
    parser.add_argument(
        'refs', nargs='*',
        help=(
            'Space-separated: BOOK [CHAPTER [VERSE]]. '
            'E.g. "Gen 1 1" or "Gen 1" or "Gen". '
            'Multiple sets can be listed one after another.'
        ),
    )
    args = parser.parse_args()

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    # Parse positional args into (book, chapter|None, verse|None) groups
    scopes: list[tuple[str, int | None, int | None]] = []
    tokens = args.refs
    i = 0
    while i < len(tokens):
        book = tokens[i]
        if book not in PROSE_BOOKS and book not in {'Psa', 'Pro', 'Job'}:
            parser.error(f'Unknown book: {book!r}')
        chapter: int | None = None
        verse: int | None = None
        if i + 1 < len(tokens) and tokens[i + 1].isdigit():
            chapter = int(tokens[i + 1])
            i += 1
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                verse = int(tokens[i + 1])
                i += 1
        scopes.append((book, chapter, verse))
        i += 1

    if not scopes:
        parser.print_help()
        sys.exit(0)

    rows: list[dict] = []
    for book, chapter, verse in scopes:
        print(f'Building: {book}' + (f' {chapter}' if chapter else '')
              + (f':{verse}' if verse else '') + ' …')
        for b, ch, vs in _verse_refs(book, chapter, verse):
            row = build_one(b, ch, vs)
            if row:
                rows.append(row)

    write_index(rows)
    write_readme(rows)
    print(f'\nDone. {len(rows)} diagram(s) written to {OUTPUT_ROOT}/')


if __name__ == '__main__':
    main()
