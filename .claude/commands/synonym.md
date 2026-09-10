# Synonym Comparison

Compare two or more near-synonym Hebrew or Greek roots side by side.

**Usage:** `/synonym <term1> <term2> [term3 ...]`

Each term may be a Strong's number or a Hebrew/Greek lemma.

**Output includes:**
- Frequency comparison with bar chart
- LXX translation equivalents for each root (with † marking shared renderings)
- OT → LXX → NT trajectory
- Distribution by book (top 5)
- Morphological forms breakdown

**Examples:**
- `/synonym H157 H2836` — אָהַב vs חָשַׁק (love vs desire)
- `/synonym H7307 H5397` — רוּחַ vs נְשָׁמָה (spirit vs breath)
- `/synonym H1697 H565` — דָּבָר vs אִמְרָה (word/speech)
- `/synonym G26 G5368` — ἀγάπη vs φιλέω (NT love words)
- `/synonym אָהַב חָשַׁק` — using Hebrew lemmas directly

---

```python
import sys
sys.path.insert(0, 'src')
from bible_grammar import resolve_strongs
from bible_grammar import print_synonym_comparison

args = "$ARGUMENTS".strip().split()
if len(args) < 2:
    print("Usage: /synonym <term1> <term2> [term3 ...]")
    print("Examples: /synonym H157 H2836  |  /synonym אָהַב חָשַׁק  |  /synonym G26 G5368")
else:
    print_synonym_comparison(args)
```
