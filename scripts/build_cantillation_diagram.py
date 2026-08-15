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

Output is written to output/reports/ot/cantillation/<book>/<book>_<ch>_<vs>.png
A CSV index is written to output/reports/ot/cantillation/index.csv

Diagrams use Park's bracket/staircase format (Sung Jin Park, 2023).
"""

import argparse
import csv
import sys
from pathlib import Path

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.bible_grammar.ot.cantillation import (  # noqa: E402
    PROSE_BOOKS, AccentNode, parse_verse, render_verse_park,
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
        render_verse_park(book, chapter, verse, output_path=out)

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


_BOOK_NAMES: dict[str, str] = {
    'Gen': 'Genesis',     'Exo': 'Exodus',        'Lev': 'Leviticus',
    'Num': 'Numbers',     'Deu': 'Deuteronomy',   'Jos': 'Joshua',
    'Jdg': 'Judges',      'Rut': 'Ruth',          '1Sa': '1 Samuel',
    '2Sa': '2 Samuel',    '1Ki': '1 Kings',        '2Ki': '2 Kings',
    '1Ch': '1 Chronicles', '2Ch': '2 Chronicles', 'Ezr': 'Ezra',
    'Neh': 'Nehemiah',    'Est': 'Esther',         'Isa': 'Isaiah',
    'Jer': 'Jeremiah',    'Lam': 'Lamentations',   'Eze': 'Ezekiel',
    'Dan': 'Daniel',      'Hos': 'Hosea',           'Joe': 'Joel',
    'Amo': 'Amos',        'Oba': 'Obadiah',         'Jon': 'Jonah',
    'Mic': 'Micah',       'Nah': 'Nahum',           'Hab': 'Habakkuk',
    'Zep': 'Zephaniah',   'Hag': 'Haggai',          'Zec': 'Zechariah',
    'Mal': 'Malachi',     'Sng': 'Song of Solomon', 'Ecc': 'Ecclesiastes',
}


def write_index(rows: list[dict]) -> None:
    """Write/update the CSV index, merging with any previously built rows."""
    if not rows:
        return
    index_path = OUTPUT_ROOT / 'index.csv'
    fieldnames = ['book', 'chapter', 'verse', 'png', 'nodes', 'words']

    existing: dict[tuple[str, int, int], dict] = {}
    if index_path.exists():
        with open(index_path, newline='', encoding='utf-8') as fh:
            for r in csv.DictReader(fh):
                key = (r['book'], int(r['chapter']), int(r['verse']))
                existing[key] = r
    for r in rows:
        key = (r['book'], int(r['chapter']), int(r['verse']))
        existing[key] = r  # overwrite stale entry with fresh data

    all_rows = sorted(
        existing.values(),
        key=lambda r: (r['book'], int(r['chapter']), int(r['verse'])),
    )
    with open(index_path, 'w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)
    print(f'\nIndex written → {index_path}')


_PARK_BLURB = """\
Bracket/staircase accent-structure diagrams generated from the MACULA Hebrew WLC text,
following Sung Jin Park, *The Fundamentals of Hebrew Accents: Divisions and Exegetical
Roles Beyond Syntax* (2023).

Each verse is split into major domain panels (**a** = Athnach half, **b** = Silluq
half). Hebrew words appear in natural RTL order: the governing accent (D0) is leftmost;
earlier verse words extend rightward. Bracket lines step down as a staircase — D0 at
the top-left, progressively deeper domains lower and further right. D1f (near/final
branch) labels are shown in gray; accent names appear in italics below each word.

**Depth labels:** D0 = panel governor · D1f = near branch before D0 · D1 = far branch
· D2f/D2 = next level · C = conjunctive"""


def _write_md(path: Path, lines: list[str]) -> None:
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'  wrote → {path}')


def write_top_readme(all_rows: list[dict]) -> None:
    """Write cantillation/README.md — index of all books."""
    from collections import defaultdict
    by_book: dict[str, list[dict]] = defaultdict(list)
    for r in all_rows:
        by_book[r['book']].append(r)

    lines: list[str] = [
        '# Cantillation Diagrams',
        '',
        _PARK_BLURB,
        '',
        '## Books',
        '',
        '| Book | Chapters | Verses |',
        '|---|---|---|',
    ]
    for book in sorted(by_book):
        book_rows = by_book[book]
        chapters = sorted({int(r['chapter']) for r in book_rows})
        name = _BOOK_NAMES.get(book, book)
        lines.append(
            f'| [{name}]({book}/index.md) | {len(chapters)} | {len(book_rows)} |'
        )
    lines += ['', '---', '', '## Build', '',
              '```bash',
              'python scripts/build_cantillation_diagram.py Gen 1',
              '```', '',
              'See `index.csv` for a full inventory of generated files.']
    _write_md(OUTPUT_ROOT / 'README.md', lines)


def write_book_readme(book: str, book_rows: list[dict], book_dir: Path) -> None:
    """Write cantillation/<book>/README.md — chapter index for one book."""
    from collections import defaultdict
    by_chapter: dict[int, list[dict]] = defaultdict(list)
    for r in book_rows:
        by_chapter[int(r['chapter'])].append(r)

    name = _BOOK_NAMES.get(book, book)
    lines: list[str] = [
        f'# {name} — Cantillation Diagrams',
        '',
        f'Accent-structure diagrams for {name}, one page per chapter.',
        '',
        '| Chapter | Verses |',
        '|---|---|',
    ]
    for ch in sorted(by_chapter):
        n = len(by_chapter[ch])
        lines.append(f'| [Chapter {ch}](ch{ch:02d}.md) | {n} |')
    lines.append('')
    _write_md(book_dir / 'README.md', lines)


def write_chapter_page(
    book: str, chapter: int, ch_rows: list[dict], book_dir: Path,
) -> None:
    """Write cantillation/<book>/ch<N>.md — one page of verse diagrams."""
    name = _BOOK_NAMES.get(book, book)
    lines: list[str] = [f'# {name} {chapter} — Cantillation', '']
    for r in sorted(ch_rows, key=lambda r: int(r['verse'])):
        vs = int(r['verse'])
        png = f"{book}_{chapter:02d}_{vs:02d}.png"
        lines += [
            f'### {name} {chapter}:{vs}',
            '',
            f'![{name} {chapter}:{vs} cantillation]({png})',
            '',
        ]
    _write_md(book_dir / f'ch{chapter:02d}.md', lines)


def write_pages(rows: list[dict]) -> None:
    """Write top, book, and chapter pages using the full merged index."""
    index_path = OUTPUT_ROOT / 'index.csv'
    if not index_path.exists():
        return
    with open(index_path, newline='', encoding='utf-8') as fh:
        all_rows = list(csv.DictReader(fh))
    if not all_rows:
        return

    from collections import defaultdict
    by_book: dict[str, list[dict]] = defaultdict(list)
    for r in all_rows:
        by_book[r['book']].append(r)

    print('\nWriting site pages …')
    write_top_readme(all_rows)
    for book, book_rows in sorted(by_book.items()):
        book_dir = OUTPUT_ROOT / book
        write_book_readme(book, book_rows, book_dir)
        by_chapter: dict[int, list[dict]] = defaultdict(list)
        for r in book_rows:
            by_chapter[int(r['chapter'])].append(r)
        for ch, ch_rows in sorted(by_chapter.items()):
            write_chapter_page(book, ch, ch_rows, book_dir)


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
    write_pages(rows)
    print(f'\nDone. {len(rows)} diagram(s) written to {OUTPUT_ROOT}/')


if __name__ == '__main__':
    main()
