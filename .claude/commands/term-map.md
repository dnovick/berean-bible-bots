# Theological Term Map

Print the theological term mapping table showing Hebrew roots → LXX equivalents → NT counts.

**Usage:**
- `/term-map` — print all 20 themes
- `/term-map covenant` — filter to a theme by keyword (case-insensitive substring match)

Themes available: Covenant / Faithfulness, Holiness / Purity, Righteousness / Justice,
Salvation / Redemption, Glory / Honour, Word / Speech, Spirit / Breath / Wind,
Knowledge / Wisdom, Love, Peace, Fear / Awe, Repentance / Return, Praise / Worship,
Creation / Making, Sin / Transgression, Atonement, Blessing / Curse, Faith / Trust,
Wrath / Anger, Mercy / Compassion

---

Run the following, substituting `$ARGUMENTS` for the optional theme filter:

```python
import sys
sys.path.insert(0, 'src')
from bible_grammar import print_term_map, term_map

theme_filter = "$ARGUMENTS".strip() or None
df = term_map()
print_term_map(df, theme=theme_filter)
```
