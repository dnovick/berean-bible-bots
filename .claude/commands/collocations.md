# Collocation Statistics

Find words that significantly co-occur with a target Hebrew or Greek root —
words appearing nearby more often than chance predicts.

**Usage:** `/collocations <strongs> [window=5] [corpus=OT|NT]`

**Output includes:**
- Observed co-occurrence count vs expected (under independence)
- PMI (Pointwise Mutual Information) — how surprising the pairing is
- G² log-likelihood — statistical confidence (more reliable for rare words)
- Sorted by G² descending

**Examples:**
- `/collocations H7307` — רוּחַ (spirit) in OT — finds east-wind, breath, tempest, prophesy
- `/collocations G3056` — λόγος (word) in NT — finds hear, sow, God, speak
- `/collocations H1697` — דָּבָר (word) in OT
- `/collocations H2617` — חֶסֶד (lovingkindness) in OT

---

```python
import sys, re
sys.path.insert(0, 'src')
from bible_grammar import resolve_strongs
from bible_grammar import print_collocations

raw = "$ARGUMENTS".strip()
# Parse optional keyword args: window=N corpus=X
window = 5
corpus = 'OT'
tokens = []
for tok in raw.split():
    m = re.match(r'window=(\d+)', tok)
    if m:
        window = int(m.group(1))
        continue
    m = re.match(r'corpus=(\w+)', tok, re.I)
    if m:
        corpus = m.group(1).upper()
        continue
    tokens.append(tok)

if not tokens:
    print("Usage: /collocations <strongs> [window=5] [corpus=OT|NT]")
else:
    for tok in tokens:
        s = resolve_strongs(tok) or tok.upper()
        # Auto-detect corpus from strongs prefix
        if corpus == 'OT' and s.startswith('G'):
            corpus = 'NT'
        print_collocations(s, window=window, corpus=corpus)
```
