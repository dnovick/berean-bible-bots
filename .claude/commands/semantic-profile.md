# Semantic Profile

Generate a complete semantic profile for any Hebrew or Greek root — combining
lexicon entry, frequency, morphology, LXX equivalents, collocations, and example
verses into a single unified report.

**Usage:** `/semantic-profile <strongs>`

**Output includes:**
- Lemma, transliteration, gloss, full definition
- Frequency and book distribution (table + bar chart)
- Morphological form breakdown
- LXX translation equivalents and consistency score (Hebrew only)
- OT → LXX → NT trajectory (Hebrew only)
- Top collocates (statistically significant neighbors, scored by G²)
- Example verses (KJV)

Saves a Markdown report + PNG chart to `output/reports/`.

**Examples:**
- `/semantic-profile H7965` — שָׁלוֹם (peace)
- `/semantic-profile H1285` — בְּרִית (covenant)
- `/semantic-profile H7307` — רוּחַ (spirit/wind)
- `/semantic-profile G3056` — λόγος (word)
- `/semantic-profile G26`   — ἀγάπη (love)

---

```python
import sys
sys.path.insert(0, 'src')
from bible_grammar import resolve_strongs
from bible_grammar import print_semantic_profile, save_semantic_profile

args = "$ARGUMENTS".strip().split()
if not args:
    print("Usage: /semantic-profile <strongs>")
    print("Examples: /semantic-profile H7965  |  /semantic-profile G3056")
else:
    for a in args:
        s = resolve_strongs(a) or a.upper()
        print_semantic_profile(s)
        save_semantic_profile(s, output_dir='output/reports')
        print(f"\nMarkdown report saved to output/reports/{s.lower()}-semantic-profile.md")
```
