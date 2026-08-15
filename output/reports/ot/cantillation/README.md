# Cantillation Diagrams

Bracket/staircase accent-structure diagrams generated from the MACULA Hebrew WLC text,
following Sung Jin Park, *The Fundamentals of Hebrew Accents: Divisions and Exegetical
Roles Beyond Syntax* (2023).

Each verse is split into major domain panels (**a** = Athnach half, **b** = Silluq
half). Hebrew words appear in natural RTL order: the governing accent (D0) is leftmost;
earlier verse words extend rightward. Bracket lines step down as a staircase — D0 at
the top-left, progressively deeper domains lower and further right. D1f (near/final
branch) labels are shown in gray; accent names appear in italics below each word.

**Depth labels:** D0 = panel governor · D1f = near branch before D0 · D1 = far branch
· D2f/D2 = next level · C = conjunctive

## Books

| Book | Chapters | Verses |
|---|---|---|
| [Genesis](Gen/index.md) | 1 | 31 |

---

## Build

```bash
python scripts/build_cantillation_diagram.py Gen 1
```

See `index.csv` for a full inventory of generated files.
