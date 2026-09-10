# Divine Names Analysis

Analyze the major divine names and christological titles across the Hebrew OT,
Septuagint (LXX), and Greek NT — with frequency tables, section breakdowns, and charts.

**Usage:** `/divine-names [OT|NT|LXX|all]`

**Default:** generates a full report covering all three corpora.

**Output includes:**
- Overview table: name, script, Strongs, total count, % share, top books
- Distribution by canonical section (Torah / Historical / Wisdom / Prophets; or Gospels / Pauline / General)
- Stacked bar chart by book
- Heatmap by section
- Full by-book breakdown table

Saves a Markdown report + PNG charts to `output/reports/`.

**OT names tracked:** YHWH (H3068G), Elohim (H0430), Adonai (H0136), El (H0410), Yah (H3050), Shaddai (H7706)
**NT terms tracked:** Theos (G2316), Kyrios (G2962), Iesous (G2424G), Christos (G5547), Pater (G3962), Pneuma (G4151)
**LXX names tracked:** Kyrios (G2962), Theos (G2316)

**Examples:**
- `/divine-names`         — full report (OT + LXX + NT)
- `/divine-names OT`      — OT Hebrew divine names only
- `/divine-names NT`      — NT christological titles only
- `/divine-names LXX`     — LXX divine names only

---

```python
import sys
sys.path.insert(0, 'src')
from bible_grammar import (print_divine_names, divine_names_chart,
                                         divine_names_report)

arg = "$ARGUMENTS".strip().upper() or "ALL"

if arg == "ALL" or arg == "":
    path = divine_names_report()
    print(f"\nFull report saved to {path}")
elif arg in ("OT", "NT", "LXX"):
    print_divine_names(arg)
    bar  = divine_names_chart(arg, chart_type='stacked_bar')
    heat = divine_names_chart(arg, chart_type='heatmap')
    print(f"\nCharts saved:\n  {bar}\n  {heat}")
else:
    print(f"Unknown argument: {arg!r}")
    print("Usage: /divine-names [OT|NT|LXX|all]")
```
