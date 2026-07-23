# Hebrew Root Flashcard Deck

← [Back to Additional Resources](../index.md)

A flashcard deck for the top 1000 Hebrew roots by OT frequency.
Each card front shows the consonantal root; the back shows the gloss, attested verbal stems, and derived nominals.

## Card Design

- **Front:** Consonantal root (e.g., אבד)
- **Back:** Vowel-pointed form; table of verbal stems with individual glosses and frequencies; table of derived nominals with POS, gloss, and frequency
- **Frequency field:** Combined OT occurrence count (sum of all lemmata in the root family)

## Files

| File | Purpose |
|---|---|
| [hebrew-root-deck.txt](hebrew-root-deck.txt) | Anki import — requires **Hebrew Root** notetype (3 fields: Front, Back, Frequency) |
| [hebrew-root-deck-fd-all.txt](hebrew-root-deck-fd-all.txt) | Flashcards Deluxe — all 1000 roots |
| [hebrew-root-deck-fd-100.txt](hebrew-root-deck-fd-100.txt) | Flashcards Deluxe — freq ≥ 100 |
| [hebrew-root-deck-fd-50.txt](hebrew-root-deck-fd-50.txt) | Flashcards Deluxe — freq 50–99 |
| [hebrew-root-deck-fd-10.txt](hebrew-root-deck-fd-10.txt) | Flashcards Deluxe — freq 10–49 |
| [hebrew-root-deck.md](hebrew-root-deck.md) | Summary report with top-50 table |

## Anki Setup

### Step 1 — Create the note type

1. Open **Tools → Manage Note Types**
2. Click **Add**, choose **Add: Basic**, and name it **Hebrew Root**
3. Click **Fields…** and confirm the fields are in this exact order:

| # | Field | Purpose |
|---|---|---|
| 1 | **Front** | Consonantal root (the question) |
| 2 | **Back** | HTML answer (stems, nominals) |
| 3 | **Frequency** | OT occurrence count — enables filtered decks (e.g., `Frequency:>100`) |

### Step 2 — Set the card templates

Click **Cards…** in the Manage Note Types dialog and enter the following:

**Front Template:**
```html
<div style="font-size:2.5em; direction:rtl; text-align:center;">{{Front}}</div>
```

**Back Template:**
```html
{{FrontSide}}
<hr>
{{Back}}
```

**Styling** (optional — adds borders and centering to the stem and nominal tables):
```css
.card {
  font-family: Arial, sans-serif;
  font-size: 16px;
  text-align: center;
}

table {
  margin: 8px auto;
  border-collapse: collapse;
}

th, td {
  padding: 3px 10px;
  border: 1px solid #ccc;
}
```

### Step 3 — Import the deck

With the **Hebrew Root** note type in place, import via **File → Import** and select `hebrew-root-deck.txt`.

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
