# Intertextuality Network

Given any OT verse, chapter, or book, find all NT verses that quote or allude
to it — scored by community vote confidence (scrollmapper / OpenBible.info).

**Usage:** `/intertextuality <OT-ref> [min_votes]`

OT reference formats:
  - `Isa 53`      — chapter scope (all verses in Isaiah 53)
  - `Isa 53:5`    — single verse
  - `Isa`         — full book (summarised at NT-book level)
  - `Psa 22`      — Psalm 22 chapter

Default min_votes: 20 (lower = more results, less certain; higher = fewer, very confident)

**Output includes:**
- NT book coverage summary (how many citations per book)
- Per-OT-verse breakdown with KJV text for both OT and NT sides
- Network graph PNG (OT verses → NT verses/books)
- Markdown report + CSV saved to `output/reports/`

**Examples:**
- `/intertextuality Isa 53`       — Isaiah 53 (the Servant Song)
- `/intertextuality Psa 22`       — Psalm 22 (My God My God)
- `/intertextuality Isa 53:5`     — single verse
- `/intertextuality Deu 6:4`      — the Shema
- `/intertextuality Isa 40`       — Voice in the wilderness
- `/intertextuality Gen 22 15`    — Binding of Isaac (lower threshold)

---

```python
import sys, re
sys.path.insert(0, 'src')
from bible_grammar import (print_intertextuality,
                                            intertextuality_graph,
                                            intertextuality_report)

raw = "$ARGUMENTS".strip()
parts = raw.split()

# Parse: Book [Chapter[:Verse]] [min_votes]
ot_book   = parts[0] if parts else None
chapter   = None
verse     = None
min_votes = 20

if not ot_book:
    print("Usage: /intertextuality <Book> [Chapter[:Verse]] [min_votes]")
    print("Examples:")
    print("  /intertextuality Isa 53")
    print("  /intertextuality Psa 22")
    print("  /intertextuality Isa 53:5")
else:
    if len(parts) >= 2:
        cv = parts[1]
        if ':' in cv:
            ch, vs = cv.split(':', 1)
            chapter, verse = int(ch), int(vs)
        elif cv.isdigit():
            chapter = int(cv)
        else:
            try:
                min_votes = int(cv)
            except ValueError:
                pass
    if len(parts) >= 3:
        try:
            min_votes = int(parts[2])
        except ValueError:
            pass

    print_intertextuality(ot_book, chapter=chapter, verse=verse, min_votes=min_votes)
    chart = intertextuality_graph(ot_book, chapter=chapter, verse=verse, min_votes=min_votes)
    report = intertextuality_report(ot_book, chapter=chapter, verse=verse, min_votes=min_votes)
    print(f"\nNetwork graph: {chart}")
    print(f"Full report:   {report}")
```
