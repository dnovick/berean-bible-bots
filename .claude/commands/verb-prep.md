# Verb Governance (Prepositions / Direct Object)

Find which preposition(s), if any, govern a Hebrew verb's complement — versus
a bare or אֵת-marked direct object, versus no complement at all. Extracted
from the MACULA lowfat constituency trees (clause-scoped sibling arguments,
not word-adjacency), so it correctly distinguishes a verb's true complement
from an unrelated adjunct in the same verse.

**Usage:** `/verb-prep <Strong's or Hebrew lemma> [stem] [book]`

- `Strong's or Hebrew lemma` — a Strong's number (`H0982`, `H982`, `982` all work) **or**
  a Hebrew root/lemma, pointed or unpointed (`בטח`, `בָּטַח`) — no need to know the
  Strong's number
- `stem`     — optional, restrict to one stem (`qal`, `niphal`, `piel`, `hiphil`, …)
- `book`     — optional, restrict to one OT book abbreviation (e.g. `Isa`)

**Examples:**
- `/verb-prep בטח`                 — same as H0982, by root instead of Strong's number
- `/verb-prep H0982`               — בטח (trust): full governance breakdown
- `/verb-prep H0982 hiphil`        — Hiphil בטח only — governance shifts to direct object
- `/verb-prep H3372`               — ירא (fear): preposition patterns
- `/verb-prep H7121 qal`           — קרא (call/read) in Qal — אֶל vs. לְ complement

**Output includes:**
- Summary table: every complement type this verb takes (each preposition,
  bare/marked direct object, no complement), with counts and % of occurrences
- Preposition-only distribution table
- Sample verses for spot-checking against the real text

---

```python
import sys
sys.path.insert(0, 'src')
from bible_grammar import print_verb_governance, resolve_strongs

raw = "$ARGUMENTS".strip().split()

if not raw:
    print("Usage: /verb-prep <Strong's or Hebrew lemma> [stem] [book]")
else:
    term = raw[0]
    resolved = resolve_strongs(term)
    if resolved:
        strongs = resolved
        # Only note the resolution when it wasn't already a plain Strong's number.
        if not term.upper().lstrip('H').isdigit():
            print(f"  Resolved {term!r} -> {resolved}")
    else:
        strongs = term  # fall back as-is (e.g. bare numeric Strong's like '982')

    stem = None
    book = None
    _STEMS = {'qal', 'niphal', 'piel', 'pual', 'hiphil', 'hophal', 'hithpael'}
    for part in raw[1:]:
        if part.lower() in _STEMS:
            stem = part.lower()
        else:
            book = part
    print_verb_governance(strongs, book=book, stem=stem)
```
