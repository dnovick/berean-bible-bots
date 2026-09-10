# Morphological Distribution Chart

Show how a root's grammatical forms distribute across books — as a table and stacked bar chart.

**Usage:** `/morph-chart <strongs>`

**Output includes:**
- Per-book table: count and % for each morphological form
- Stacked bar chart PNG saved to output/charts/

**What it shows by word type:**
- Hebrew verbs: stem × conjugation (Qal Perfect, Piel Imperfect, etc.)
- Greek verbs: tense × voice (Aorist Active, Present Passive, etc.)
- Greek nouns: case distribution (Nominative, Accusative, Genitive, Dative)

**Examples:**
- `/morph-chart H1696` — דָבַר (to speak) — overwhelmingly Piel across OT
- `/morph-chart H7307` — רוּחַ (spirit) — noun state distribution by book
- `/morph-chart G3056` — λόγος (word) — case distribution across NT books
- `/morph-chart G3004` — λέγω (to say) — tense/voice distribution in NT

---

```python
import sys
sys.path.insert(0, 'src')
from bible_grammar import resolve_strongs
from bible_grammar import print_morph_distribution, morph_chart

args = "$ARGUMENTS".strip().split()
if not args:
    print("Usage: /morph-chart <strongs>")
    print("Examples: /morph-chart H1696  |  /morph-chart G3056")
else:
    for a in args:
        s = resolve_strongs(a) or a.upper()
        print_morph_distribution(s)
        slug = s.lower().replace('/', '-')
        out = f'output/charts/{slug}-morph.png'
        morph_chart(s, output_path=out)
        print(f"Chart saved to {out}")
```
