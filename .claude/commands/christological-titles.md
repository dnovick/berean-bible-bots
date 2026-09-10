# Christological Titles

Frequency table of titles Jesus used to refer to Himself in the Gospels
(and optionally across the full NT), counted by verse-level co-occurrence
of the relevant Greek Strong's numbers.

**Usage:** `/christological-titles [scope] [filter]`

- `scope`  — `gospels` (default) or `NT`
- `filter` — add `filter` to restrict to Jesus-speaking verses only
  (uses curated allowlists + MACULA subjref speaker attribution)

**Output includes:**
- Grouped frequency table by book (Matthew / Mark / Luke / John)
- Confidence rating (High/Medium/Low) per title
- Bar chart PNG saved to `output/charts/`
- Markdown report saved to `output/reports/`

**Groups covered:**
- **Son titles** — Son of Man, Son of God, Son / the Father, Son of David
- **I AM sayings** — absolute ego eimi + all 7 Johannine predicate I AM sayings
- **Other titles** — Lord (Kyrios), Christ/Messiah, Bridegroom, Prophet

**Examples:**
- `/christological-titles`         — Gospel counts
- `/christological-titles NT`      — Full NT (includes epistles)

> **Note on speaker attribution:** STEPBible TAGNT does not tag speakers.
> The confidence column indicates how reliably each pattern reflects
> Jesus's own self-designation.

---

```python
import sys
sys.path.insert(0, 'src')
from bible_grammar import (
    print_title_counts, title_chart, title_report
)

raw = "$ARGUMENTS".strip().split()
scope = 'gospels'
speaker_filter = False
for part in raw:
    if part in ('gospels', 'NT'):
        scope = part
    elif part == 'filter':
        speaker_filter = True

print_title_counts(scope=scope, speaker_filter=speaker_filter)
chart = title_chart(scope=scope)
report = title_report(output_dir='output/reports')
print(f"\nChart:  {chart}")
print(f"Report: {report}")
```
