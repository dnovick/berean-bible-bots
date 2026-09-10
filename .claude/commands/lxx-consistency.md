# LXX Translation Consistency

Measure how uniformly LXX translators render a given Hebrew root across books.

**Usage:** `/lxx-consistency <strongs> [strongs2 ...]`

**Output includes:**
- Corpus-wide primary LXX rendering and percentage
- Overall weighted consistency score (0–100%)
- Per-book table: tokens, primary rendering, consistency %, alt renderings
- Divergent books marked with ←
- Optional heatmap PNG

**Examples:**
- `/lxx-consistency H7307` — רוּחַ (spirit/wind) — split between πνεῦμα and ἄνεμος
- `/lxx-consistency H1697` — דָּבָר (word) — highest divergence among major theological terms
- `/lxx-consistency H6944` — קֹדֶשׁ (holiness) — perfectly consistent (100%)
- `/lxx-consistency H4941` — מִשְׁפָּט (justice) — high divergence across books

---

```python
import sys
sys.path.insert(0, 'src')
from bible_grammar import resolve_strongs
from bible_grammar import print_lxx_consistency, consistency_heatmap

args = "$ARGUMENTS".strip().split()
if not args:
    print("Usage: /lxx-consistency <strongs> [strongs2 ...]")
    print("Examples: /lxx-consistency H7307  |  /lxx-consistency H1697 H565")
else:
    resolved = []
    for a in args:
        s = resolve_strongs(a) or a.upper()
        resolved.append(s)
        print_lxx_consistency(s)
    if len(resolved) > 1:
        print("\nGenerating multi-root heatmap...")
        consistency_heatmap(resolved, output_path='output/charts/lxx-consistency-multi.png')
```
