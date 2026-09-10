# Genre Comparison

Compare morphological patterns across canonical literary sections of the OT
or NT — verb stems, conjugations, tense, voice, mood, and POS distribution.

**Usage:** `/genre-compare [OT|NT|all] [feature]`

**OT features:** `verb_stem`, `verb_conjugation`, `pos`, `noun_state`
**NT features:** `verb_tense`, `verb_voice`, `verb_mood`, `pos`

**Default:** generates a full report covering all features for both corpora.

**Output includes:**
- Heatmap chart (rows=genres, cols=categories, colour-scaled by relative intensity)
- Markdown table with % values per genre
- Interpretive notes for each feature

Saves a Markdown report + PNG heatmaps to `output/reports/`.

**Examples:**
- `/genre-compare`                  — full report (OT + NT)
- `/genre-compare OT verb_stem`     — OT verb stem heatmap + table
- `/genre-compare NT verb_tense`    — NT verb tense heatmap + table
- `/genre-compare OT verb_conjugation` — narrative vs. poetry conjugation contrast

---

```python
import sys
sys.path.insert(0, 'src')
from bible_grammar import (print_genre_compare, genre_heatmap,
                                          genre_report)

parts = "$ARGUMENTS".strip().split()
corpus  = parts[0].upper() if parts else "ALL"
feature = parts[1].lower() if len(parts) > 1 else None

if corpus == "ALL" or corpus == "":
    path = genre_report()
    print(f"\nFull report saved to {path}")
elif corpus in ("OT", "NT"):
    if feature:
        print_genre_compare(corpus, feature=feature)
        p = genre_heatmap(corpus, feature=feature)
        print(f"\nChart saved to {p}")
    else:
        # Print all features for this corpus
        features = (['verb_stem','verb_conjugation','pos'] if corpus == 'OT'
                    else ['verb_tense','verb_voice','verb_mood','pos'])
        for f in features:
            print_genre_compare(corpus, feature=f)
            genre_heatmap(corpus, feature=f)
        print(f"\nCharts saved to output/reports/")
else:
    print(f"Unknown argument: {corpus!r}")
    print("Usage: /genre-compare [OT|NT|all] [feature]")
```
