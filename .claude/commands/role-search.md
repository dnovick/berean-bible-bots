# Syntactic Role Search

Find all verbs whose grammatical subject is a given person or entity —
resolved from the MACULA Hebrew/Greek `subjref` syntax tree links.

**Usage:** `/role-search <Strong's> [corpus] [book...]`

- `Strong's` — one or more Strong's numbers, comma-separated:
  `H3068,H0430` (YHWH+Elohim), `G2424` (Jesus), `G2316` (Theos)
- `corpus`    — `OT` (default) or `NT`
- `book...`   — optional book IDs to restrict scope (e.g. `Mat Mrk Luk Jhn`)

**Examples:**
- `/role-search H3068,H0430`                — What does God do in the OT?
- `/role-search G2424 NT Mat Mrk Luk Jhn`  — What does Jesus do in the Gospels?
- `/role-search G2316 NT`                   — What does God do in the NT?
- `/role-search H3068 OT Isa`              — YHWH's actions in Isaiah only

**Output includes:**
- Terminal table of top verbs by frequency
- For OT: inline LXX Greek equivalent per verb
- Bar chart PNG
- Markdown report with book distribution and cross-testament comparison

---

```python
import sys
sys.path.insert(0, 'src')
from bible_grammar import print_role_summary, role_report

raw = "$ARGUMENTS".strip().split()
strongs_raw = raw[0] if raw else 'H3068,H0430'
strongs = strongs_raw.split(',')

corpus = 'OT'
books = []
for part in raw[1:]:
    if part in ('OT', 'NT'):
        corpus = part
    else:
        books.append(part)

label = '+'.join(strongs)
print_role_summary(strongs, corpus, books=books or None, top_n=20, label=label)
report = role_report(strongs, corpus, books=books or None, label=label,
                     output_dir='output/reports',
                     include_cross_testament=(corpus == 'OT' and not books))
print(f"\nReport: {report}")
```
