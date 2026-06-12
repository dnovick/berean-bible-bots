"""Fix collapsed answer rows in HTML exercises.

Answer rows in interactive HTML exercises must have one <td> per question column
so that answers align visually under the input fields. This script finds and fixes
the two broken patterns:

  Pattern A — full collapse:
    <tr class="answer-row" id="aX"><td colspan="N">Field · Field · ... — Notes</td></tr>
    Fix: split by " · " and " — " into individual <td> cells.

  Pattern B — partial collapse (last two cells merged):
    <td colspan="2">content</td> at the end of an ans-row
    Fix: remove colspan, append an empty <td></td> for the button column.

Usage:
    python scripts/fix_collapsed_html_answers.py [--course bbh|bbg|bba] [--dry-run]

The mechanism to prevent future regressions: run this script in CI or before
committing any HTML exercise file. A zero-exit return means no collapsed rows
remain. Non-zero exit indicates files were fixed (or need fixing in dry-run mode).

CLAUDE.md standard (enforced here):
  Every answer row in an interactive exercise must use one <td> per question
  column — never a single <td colspan="N"> that collapses multiple answers.
  Answer row cells are: [item#/check] [Hebrew form] [field1] [field2] ... [empty]
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

# ── regex patterns ──────────────────────────────────────────────────────────

# Full-collapse: entire answer in one td with large colspan
_FULL_COLLAPSE = re.compile(
    r'(<tr\s+class="answer-row"[^>]*>)'
    r'\s*<td\s+colspan="(\d+)">(.*?)</td>\s*'
    r'(</tr>)',
    re.DOTALL,
)

# Partial collapse: last td in an ans-row has colspan="2"
_PARTIAL_COLLAPSE = re.compile(
    r'(<tr\s+class="ans-row"[^>]*>.*?)'
    r'<td\s+colspan="2">(.*?)</td>'
    r'(\s*</tr>)',
    re.DOTALL,
)


def _split_answer_text(text: str, n_input_cols: int) -> list[str]:
    """Split a collapsed answer string into a list of per-column strings.

    The format used across exercises is:
        Field1 · Field2 · ... · RootOrLast — Notes/explanation

    The number of · -delimited fields before the — matches the number of
    fillable input columns in the question row (n_input_cols).  Everything
    after the first — is the notes/explanation and goes in the last cell.
    """
    text = text.strip()
    # Split on " — " first to separate structured fields from free-text notes
    if ' — ' in text:
        fields_part, notes = text.split(' — ', 1)
    else:
        fields_part, notes = text, ''

    parts = [p.strip() for p in fields_part.split(' · ')]

    # Pad or truncate to exactly n_input_cols cells; notes go in the last slot
    if notes:
        # Combine last field with notes into the final cell
        if len(parts) >= n_input_cols:
            # Merge everything from n_input_cols-1 onward into the last cell
            last = ' · '.join(parts[n_input_cols - 1:]) + ' — ' + notes
            cells = parts[:n_input_cols - 1] + [last]
        else:
            cells = parts + [''] * (n_input_cols - len(parts) - 1) + [notes]
    else:
        cells = parts
        while len(cells) < n_input_cols:
            cells.append('')

    return cells[:n_input_cols]


def _count_input_cols(question_block: str) -> int:  # noqa: D103
    """Count <input> elements in the question block preceding an answer row."""
    return len(re.findall(r'<input\b', question_block))


def fix_full_collapse(html: str) -> tuple[str, int]:
    """Replace full-collapse answer rows with per-column cells.

    Returns (fixed_html, n_changes).
    """
    changes = 0

    def replace(m: re.Match) -> str:
        nonlocal changes
        prefix = m.group(1)
        # colspan = int(m.group(2))  # available but not needed for splitting
        inner = m.group(3).strip()
        suffix = m.group(4)

        # Find the preceding question row to count input columns
        start = m.start()
        preceding = html[:start]
        # Count inputs in the last <tr>...</tr> before this answer row
        last_tr = re.search(r'<tr(?!.*<tr)(.*?)</tr>', preceding, re.DOTALL)
        n_inputs = _count_input_cols(last_tr.group(0) if last_tr else '') if last_tr else 4

        cells = _split_answer_text(inner, n_inputs)
        td_cells = ''.join(f'<td>{c}</td>' for c in cells) + '<td></td>'
        changes += 1
        return f'{prefix}{td_cells}{suffix}'

    fixed = _FULL_COLLAPSE.sub(replace, html)
    return fixed, changes


def fix_partial_collapse(html: str) -> tuple[str, int]:
    """Remove colspan="2" from the last cell in ans-rows, adding an empty td."""
    changes = 0

    def replace(m: re.Match) -> str:
        nonlocal changes
        before = m.group(1)
        content = m.group(2)
        after = m.group(3)
        changes += 1
        return f'{before}<td>{content}</td><td></td>{after}'

    fixed = _PARTIAL_COLLAPSE.sub(replace, html)
    return fixed, changes


def process_file(path: Path, dry_run: bool) -> int:  # noqa: D103
    """Process one HTML file. Returns number of rows fixed."""
    original = path.read_text(encoding='utf-8')

    fixed, n1 = fix_full_collapse(original)
    fixed, n2 = fix_partial_collapse(fixed)
    total = n1 + n2

    if total and not dry_run:
        path.write_text(fixed, encoding='utf-8')
        print(f'  Fixed {total} answer row(s): {path.relative_to(ROOT)}')
    elif total and dry_run:
        print(f'  [dry-run] Would fix {total} answer row(s): {path.relative_to(ROOT)}')

    return total


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--course', choices=['bbh', 'bbg', 'bba', 'all'], default='bbh',
                        help='Which course to fix (default: bbh)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Report what would be fixed without writing files')
    args = parser.parse_args()

    courses = ['bbh', 'bbg', 'bba'] if args.course == 'all' else [args.course]

    course_dirs = {
        'bbh': ROOT / 'output' / 'lessons' / 'hebrew' / 'bbh',
        'bbg': ROOT / 'output' / 'lessons' / 'greek' / 'bbg',
        'bba': ROOT / 'output' / 'lessons' / 'aramaic' / 'bba',
    }

    total_fixed = 0
    for course in courses:
        base = course_dirs[course]
        if not base.exists():
            print(f'  [skip] {base} does not exist')
            continue
        html_files = sorted(base.rglob('*.html'))
        for f in html_files:
            total_fixed += process_file(f, args.dry_run)

    if total_fixed == 0:
        print('No collapsed answer rows found.')
    else:
        action = 'Would fix' if args.dry_run else 'Fixed'
        print(f'\n{action} {total_fixed} collapsed answer row(s) total.')

    # Non-zero exit if anything was (or would be) changed — useful for CI
    sys.exit(0 if total_fixed == 0 else 1)


if __name__ == '__main__':
    main()
