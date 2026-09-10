# Export

Export any analysis as a styled standalone HTML report and/or CSV data files.

**Usage:** `/export <type> [args]`

**Types:**
- `word-study <strongs>`        — HTML + CSV for a word study (e.g. H7965, G3056)
- `semantic-profile <strongs>`  — HTML + CSV for a semantic profile
- `genre-compare [OT|NT|all]`   — HTML + CSV for genre comparison heatmaps
- `divine-names`                — HTML + CSV for divine names analysis
- `all`                         — run all exporters (divine names, genre compare, key word studies)

**Output locations:**
- `output/exports/html/`  — self-contained HTML files (inline CSS + embedded charts)
- `output/exports/csv/`   — raw CSV files organised by analysis type

**Examples:**
- `/export word-study H7965`       — שָׁלוֹם word study
- `/export semantic-profile G3056` — λόγος semantic profile
- `/export genre-compare OT`       — OT genre comparison
- `/export divine-names`           — all three corpora
- `/export all`                    — everything

---

```python
import sys
sys.path.insert(0, 'src')
from bible_grammar import (export_word_study, export_semantic_profile,
                                   export_genre_compare, export_divine_names, export_all)

parts = "$ARGUMENTS".strip().split()
cmd   = parts[0].lower() if parts else 'all'
arg   = parts[1] if len(parts) > 1 else None

if cmd in ('word-study', 'word_study'):
    if not arg:
        print("Usage: /export word-study <strongs>  e.g. H7965 or G3056")
    else:
        export_word_study(arg)
elif cmd in ('semantic-profile', 'semantic_profile'):
    if not arg:
        print("Usage: /export semantic-profile <strongs>")
    else:
        export_semantic_profile(arg)
elif cmd in ('genre-compare', 'genre_compare'):
    corpus = (arg or 'all').upper()
    if corpus in ('OT', 'NT'):
        export_genre_compare(corpus)
    else:
        export_genre_compare('OT')
        export_genre_compare('NT')
elif cmd == 'divine-names':
    export_divine_names()
elif cmd == 'all':
    export_all()
else:
    print(f"Unknown export type: {cmd!r}")
    print("Types: word-study, semantic-profile, genre-compare, divine-names, all")
```
