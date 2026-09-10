# Daily Grammar Nugget

Generate one daily SMS-ready example sentence highlighting the Hebrew verbal stem
currently being studied. Each nugget is appended to a persistent Markdown file in
`output/nuggets/` so students can refer back to the full collection.

**Usage:** `/nugget <stem> [subtype]`

- `stem` — the stem being studied: `hiphil`, `niphal`, `piel`, `pual`, `hithpael`, `qal`
- `subtype` *(optional)* — narrow focus: `strong`, `weak`, `i-nun`, `iii-he`, etc.

**Examples:**
- `/nugget hiphil strong`
- `/nugget niphal`
- `/nugget piel`

---

## Output file

Each stem has its own file under `output/nuggets/`:

| Stem | File |
|---|---|
| Hiphil strong | `output/nuggets/hiphil-strong-nuggets.md` |
| Hiphil weak | `output/nuggets/hiphil-weak-nuggets.md` |
| Niphal | `output/nuggets/niphal-nuggets.md` |
| Piel | `output/nuggets/piel-nuggets.md` |
| Pual | `output/nuggets/pual-nuggets.md` |
| Hithpael | `output/nuggets/hithpael-nuggets.md` |
| Qal | `output/nuggets/qal-nuggets.md` |

If the file does not exist, create it with the appropriate header.

---

## What to generate

1. **Query the database** for Hiphil (or relevant stem) tokens in Deuteronomy, Psalms, and
   Proverbs — in that priority order. For strong-verb days, prefer roots with no weak
   consonants (no I-נ, I-י, III-ה, biconsonantal, I-א). Vary the conjugation day to day
   (check the existing nuggets in the file and pick a conjugation not recently used).

2. **Select one example** that is:
   - From a theologically rich or familiar passage
   - Clear and unambiguous as a stem example
   - Short enough for an SMS (verse snippet, not the whole verse)

3. **Append to the file** in this Markdown format:

```markdown
## Nugget N — YYYY-MM-DD

**form** (Ref)

> Hebrew snippet
> *"English translation."*

**Form:** [Conjugation] [PGN] of [root] — [morphological diagnostic note]
**Function:** [Causative / Declarative / Factitive / Simple action] — one sentence
**Why it matters:** 2–3 sentences connecting form to meaning, familiar passage, or teaching point

---
```

4. **Print the SMS-ready version** to the conversation (plain text, no markdown):

```
[Stem] nugget — [Conjugation] of [root]
[Ref]: [Hebrew snippet]
"[English]"
Form: [diagnostic]
Function: [one line]
[one memorable teaching sentence]
```

### SMS-safe Hebrew formatting rules

These rules prevent display problems when pasting into Messages or other SMS apps:

- **Use bare consonantal Hebrew only in SMS output** — strip ALL diacritics: both
  cantillation marks (U+0591–U+05AF) and vowel points (U+05B0–U+05BD). Combining
  characters cause extra spacing in SMS renderers even when individually invisible.
- The markdown file (appended to `output/nuggets/`) **may retain full pointing**
  (vowels only, no cantillation) so students have the correct reading form on file.
- **Never mix Hebrew characters inline with Latin prose.** The Unicode bidi algorithm
  reorders the line — "הִ prefix" renders as "tprefix הִ". Instead write the Latin
  equivalent: "hi-prefix", "dagesh in dalet", etc.
- **Hebrew appears only on its own dedicated lines**: the bold heading form+reference,
  and the verse lines. Nowhere else.
- When naming diagnostics in the Form/Function/Why prose, spell out all morphological
  terms in Latin (e.g. "patah under he", "dagesh forte in tav", "tsere holem").

5. **Today's date** is available from the system. Use it for the nugget heading.

---

## Data queries

```python
import sys
sys.path.insert(0, 'src')
from bible_grammar.core.db import load
import pandas as pd

df = load()
heb = df[df['source'] == 'TAHOT']
hi = heb[heb['stem'] == 'Hiphil'].copy()  # change stem name as needed

pref_books = ['Deu', 'Psa', 'Pro']
sub = hi[hi['book_id'].isin(pref_books)]

conj_map = {
    'Vhq': 'Perfect', 'Vhw': 'Wayyiqtol', 'Vhi': 'Imperfect',
    'Vhp': 'Weqatal',  'Vhv': 'Imperative', 'Vhc': 'Inf. Construct',
    'Vha': 'Inf. Absolute', 'Vhrm': 'Participle',
}
# Stem morph prefixes: Hiphil=Vh, Niphal=VN, Piel=Vp, Pual=VP, Hithpael=Vt
def m2c(m, prefix='Vh'):
    for k,v in conj_map.items():
        if str(m).startswith(k): return v
    return None
sub = sub.copy()
sub['conj'] = sub['morph_code'].apply(m2c)
```

**Stem column values:** `'Hiphil'`, `'Niphal'`, `'Piel'`, `'Pual'`, `'Hithpael'`, `'Qal'`
