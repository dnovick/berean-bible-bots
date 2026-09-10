# Word Study

Run a complete word study for a Hebrew or Greek term.

**Usage:** `/word-study <term>`

Where `<term>` is any of:
- A Strong's number: `H1285`, `G3056`
- A Hebrew lemma (with or without vowel points): `שָׁלוֹם`, `שלום`
- A Greek lemma: `λόγος`, `διαθήκη`

**Output includes:**
- Lexicon definition
- OT/NT occurrence count and distribution by book
- Morphological forms breakdown
- LXX translation equivalents (word-level alignment, Hebrew only)
- OT → LXX → NT trajectory
- Example verses with KJV text

---

Run the following, substituting `$ARGUMENTS` for the term:

```python
import sys
sys.path.insert(0, 'src')
from bible_grammar import resolve_strongs
from bible_grammar import print_word_study

term = "$ARGUMENTS".strip()
strongs = resolve_strongs(term)
if strongs is None:
    print(f"Could not resolve '{term}' to a Strong's number.")
    print("Try a Strong's number (H1285, G3056), a Hebrew lemma (שָׁלוֹם), or a Greek lemma (λόγος).")
else:
    print(f"Resolved '{term}' → {strongs}")
    print_word_study(strongs, example_verses=5)
```
