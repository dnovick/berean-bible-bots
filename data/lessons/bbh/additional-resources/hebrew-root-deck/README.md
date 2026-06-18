# Hebrew Root Deck

← [Back to Additional Resources](../index.md)

A flashcard deck for the top 1000 Hebrew roots by OT frequency.
Each card front shows the consonantal root; the back shows the gloss, attested verbal stems, and derived nominals.

## Card Design

- **Front:** Consonantal root (e.g., אבד)
- **Back:** Vowel-pointed form, gloss, verbal stem frequencies, derived nominals
- **Frequency field:** Combined OT occurrence count (sum of all lemmata in the root family)

## Files

| File | Purpose |
|---|---|
| `hebrew-root-deck.txt` | Anki import — requires **Hebrew Root** notetype (3 fields: Front, Back, Frequency) |
| `hebrew-root-deck-fd-all.txt` | Flashcards Deluxe — all 1000 roots |
| `hebrew-root-deck-fd-100.txt` | Flashcards Deluxe — freq ≥ 100 |
| `hebrew-root-deck-fd-50.txt` | Flashcards Deluxe — freq 50–99 |
| `hebrew-root-deck-fd-10.txt` | Flashcards Deluxe — freq 10–49 |
| `hebrew-root-deck.md` | Summary report with top-50 table |

## Anki Setup

Before importing `hebrew-root-deck.txt`, create a note type named **Hebrew Root** with three fields in order:
1. **Front** — the question (consonantal root)
2. **Back** — the answer (HTML)
3. **Frequency** — numeric OT frequency (used for filtered decks, e.g., `Frequency:>100`)

## Filtering in Flashcards Deluxe

Use the band files to study by frequency tier:
- `fd-100.txt` — most common roots (≥ 100 occurrences)
- `fd-50.txt` — moderately common (50–99)
- `fd-10.txt` — less common (10–49)
- `fd-all.txt` — complete deck

## Data Sources

- **Root groupings:** OpenScriptures HebrewLexicon (HebrewStrong.xml)
- **Frequencies:** OSHB morphologically-tagged OT (words.parquet)
- **Top 1000 roots** ranked by combined root-family frequency
