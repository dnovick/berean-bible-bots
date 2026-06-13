"""Build fire vocabulary word-study: CSV exports, charts, and markdown report.

Run from repo root:
    python scripts/both/word_studies/fire/build_fire_report.py
"""
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, 'src')

import matplotlib  # noqa: E402
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from bidi.algorithm import get_display  # noqa: E402
from bible_grammar.core.syntax_ot import load_syntax_ot  # noqa: E402
from bible_grammar.core.lxx_query import query_lxx  # noqa: E402
from bible_grammar.core._utils import load_nt  # noqa: E402
from bible_grammar.core.db import load_translations  # noqa: E402


def nfc(s: object) -> str:
    return unicodedata.normalize('NFC', str(s))


# ============================================================
# Output directories
# ============================================================
OUT = Path('output/reports/both/word_studies/fire')
CHART_OUT = Path('output/charts/both/word_studies/fire')
MK_OUT = Path('mkdocs_src/reports/both/word_studies/fire')
MK_CHART = Path('mkdocs_src/reports/charts/both/word_studies/fire')
for d in (OUT, CHART_OUT, MK_OUT, MK_CHART):
    d.mkdir(parents=True, exist_ok=True)

# ============================================================
# Semantic category constants
# ============================================================
MUNDANE = 'Mundane'
OFFERING = 'Offering by Fire'
THEOPHANY = 'Divine Presence / Theophany'
JUDGMENT = 'Divine Judgment / Wrath'
ESCHATOLOGICAL = 'Eschatological'
PURIFICATION = 'Purification / Refining'
SYMBOLIC = 'Symbolic / Metaphorical'
AMBIGUOUS = 'Ambiguous'

CATEGORIES_ORDER = [
    THEOPHANY, JUDGMENT, ESCHATOLOGICAL,
    PURIFICATION, SYMBOLIC, AMBIGUOUS, OFFERING, MUNDANE,
]

CAT_COLORS = {
    THEOPHANY: '#f7a600',
    JUDGMENT: '#d73027',
    ESCHATOLOGICAL: '#762a83',
    PURIFICATION: '#4393c3',
    SYMBOLIC: '#74c476',
    AMBIGUOUS: '#969696',
    OFFERING: '#8c6d31',
    MUNDANE: '#cccccc',
}

# ============================================================
# Strong's number sets
# ============================================================
OT_FIRE_STRONGS = {
    'H784': 'אֵשׁ',     # fire (primary noun)
    'H801': 'אִשֶּׁה',   # offering made by fire
    'H3857': 'לַהַב',   # flame
    'H3940': 'לַפִּיד',  # torch / flame
    'H5135': 'נוּר',    # Aramaic: fire (Daniel)
}

NT_FIRE_STRONGS = {
    'G4442': 'πῦρ',      # fire
    'G5395': 'φλόξ',     # flame
    'G4443': 'πυρά',     # bonfire / fire
    'G4448': 'πυρόω',    # to be on fire / burning
    'G4451': 'πύρωσις',  # fiery trial / burning
    'G2618': 'κατακαίω',  # to burn up (eschatological/judgment contexts)
}

LXX_FIRE_STRONGS = {'G4442', 'G5395', 'G4443'}

# ============================================================
# Genre map (book → genre)
# ============================================================
GENRE_MAP = {
    # Pentateuch
    'Gen': 'Pentateuch', 'Exo': 'Pentateuch', 'Lev': 'Pentateuch',
    'Num': 'Pentateuch', 'Deu': 'Pentateuch',
    # History
    'Jos': 'History', 'Jdg': 'History', 'Rut': 'History',
    '1Sa': 'History', '2Sa': 'History', '1Ki': 'History', '2Ki': 'History',
    '1Ch': 'History', '2Ch': 'History', 'Ezr': 'History',
    'Neh': 'History', 'Est': 'History',
    # Poetry / Wisdom
    'Job': 'Poetry / Wisdom', 'Psa': 'Poetry / Wisdom',
    'Pro': 'Poetry / Wisdom', 'Ecc': 'Poetry / Wisdom', 'Son': 'Poetry / Wisdom',
    # Major Prophets
    'Isa': 'Major Prophets', 'Jer': 'Major Prophets', 'Lam': 'Major Prophets',
    'Eze': 'Major Prophets', 'Dan': 'Major Prophets',
    # Minor Prophets
    'Hos': 'Minor Prophets', 'Jol': 'Minor Prophets', 'Amo': 'Minor Prophets',
    'Oba': 'Minor Prophets', 'Jon': 'Minor Prophets', 'Mic': 'Minor Prophets',
    'Nah': 'Minor Prophets', 'Hab': 'Minor Prophets', 'Zep': 'Minor Prophets',
    'Hag': 'Minor Prophets', 'Zec': 'Minor Prophets', 'Mal': 'Minor Prophets',
    # NT Gospels
    'Mat': 'Gospels', 'Mrk': 'Gospels', 'Luk': 'Gospels', 'Jhn': 'Gospels',
    # Acts
    'Act': 'Acts',
    # Pauline Epistles
    'Rom': 'Pauline Epistles', '1Co': 'Pauline Epistles', '2Co': 'Pauline Epistles',
    'Gal': 'Pauline Epistles', 'Eph': 'Pauline Epistles', 'Php': 'Pauline Epistles',
    'Col': 'Pauline Epistles', '1Th': 'Pauline Epistles', '2Th': 'Pauline Epistles',
    '1Ti': 'Pauline Epistles', '2Ti': 'Pauline Epistles', 'Tit': 'Pauline Epistles',
    'Phm': 'Pauline Epistles',
    # General Epistles
    'Heb': 'General Epistles', 'Jas': 'General Epistles',
    '1Pe': 'General Epistles', '2Pe': 'General Epistles',
    '1Jn': 'General Epistles', '2Jn': 'General Epistles',
    '3Jn': 'General Epistles', 'Jud': 'General Epistles',
    # Apocalyptic
    'Rev': 'Apocalyptic',
}

# ============================================================
# Verse-level categorization
# (book, chapter, verse) → category
# H801 (offering by fire) is always OFFERING regardless of this dict.
# Everything else not listed defaults to MUNDANE.
# ============================================================
VERSE_CATEGORY: dict = {

    # ---- DIVINE PRESENCE / THEOPHANY ----
    ('Gen', 15, 17): THEOPHANY,   # smoking fire pot between the pieces
    ('Exo', 3, 2): THEOPHANY,     # burning bush
    ('Exo', 13, 21): THEOPHANY,   # pillar of fire in wilderness
    ('Exo', 13, 22): THEOPHANY,
    ('Exo', 14, 24): THEOPHANY,   # LORD in pillar of fire
    ('Exo', 19, 18): THEOPHANY,   # Sinai enveloped in smoke (fire)
    ('Exo', 24, 17): THEOPHANY,   # glory of LORD like devouring fire
    ('Exo', 40, 38): THEOPHANY,   # fire in cloud over tabernacle at night
    ('Num', 9, 15): THEOPHANY,    # fire over tabernacle
    ('Num', 9, 16): THEOPHANY,
    ('Num', 14, 14): THEOPHANY,   # pillar of fire
    ('Deu', 1, 33): THEOPHANY,    # fire by night in exodus
    ('Deu', 4, 11): THEOPHANY,    # fire at Sinai
    ('Deu', 4, 12): THEOPHANY,
    ('Deu', 4, 15): THEOPHANY,
    ('Deu', 4, 24): THEOPHANY,    # God is a consuming fire
    ('Deu', 4, 33): THEOPHANY,
    ('Deu', 4, 36): THEOPHANY,
    ('Deu', 5, 4): THEOPHANY,     # face to face from fire
    ('Deu', 5, 5): THEOPHANY,
    ('Deu', 5, 22): THEOPHANY,
    ('Deu', 5, 23): THEOPHANY,
    ('Deu', 5, 24): THEOPHANY,
    ('Deu', 5, 25): THEOPHANY,
    ('Deu', 5, 26): THEOPHANY,
    ('Deu', 9, 3): THEOPHANY,     # God before you as consuming fire
    ('Deu', 9, 10): THEOPHANY,
    ('Deu', 9, 15): THEOPHANY,
    ('Deu', 10, 4): THEOPHANY,
    ('Deu', 33, 2): THEOPHANY,    # Sinai — fiery law from his right hand
    ('Jdg', 13, 20): THEOPHANY,   # angel ascending in flame of altar
    ('1Ki', 18, 38): THEOPHANY,   # fire from LORD consuming Elijah's sacrifice
    ('1Ki', 19, 12): THEOPHANY,   # fire, but LORD not in the fire
    ('2Ki', 2, 11): THEOPHANY,    # chariot and horses of fire
    ('2Ki', 6, 17): THEOPHANY,    # horses and chariots of fire (Elisha's vision)
    ('2Ch', 7, 1): THEOPHANY,     # fire from heaven consuming Solomon's sacrifice
    ('2Ch', 7, 3): THEOPHANY,
    ('Neh', 9, 12): THEOPHANY,    # pillar of fire in exodus narrative
    ('Neh', 9, 19): THEOPHANY,
    ('Psa', 78, 14): THEOPHANY,   # pillar of fire
    ('Psa', 97, 3): THEOPHANY,    # fire goes before him
    ('Psa', 105, 39): THEOPHANY,  # fire to give light by night
    ('Eze', 1, 4): THEOPHANY,     # fire in Ezekiel's throne vision
    ('Eze', 1, 13): THEOPHANY,
    ('Eze', 1, 27): THEOPHANY,
    ('Eze', 8, 2): THEOPHANY,     # figure of fire (divine vision)
    ('Eze', 10, 2): THEOPHANY,    # fire from cherubim's wheels
    ('Eze', 10, 6): THEOPHANY,
    ('Eze', 10, 7): THEOPHANY,
    ('Dan', 3, 19): THEOPHANY,    # fiery furnace — divine protection
    ('Dan', 3, 20): THEOPHANY,
    ('Dan', 3, 21): THEOPHANY,
    ('Dan', 3, 22): THEOPHANY,
    ('Dan', 3, 23): THEOPHANY,
    ('Dan', 3, 24): THEOPHANY,
    ('Dan', 3, 25): THEOPHANY,    # fourth figure like the Son of God
    ('Dan', 3, 26): THEOPHANY,
    ('Dan', 3, 27): THEOPHANY,
    ('Dan', 7, 9): THEOPHANY,     # Ancient of Days — fiery throne
    ('Dan', 7, 10): THEOPHANY,    # river of fire
    ('Zec', 2, 5): THEOPHANY,     # wall of fire protecting Jerusalem
    ('Mat', 3, 11): THEOPHANY,    # baptize with Holy Spirit and fire
    ('Luk', 3, 16): THEOPHANY,
    ('Act', 2, 3): THEOPHANY,     # tongues of fire at Pentecost
    ('Heb', 12, 18): THEOPHANY,   # burning fire at Sinai
    ('Heb', 12, 29): THEOPHANY,   # God is a consuming fire
    ('Rev', 1, 14): THEOPHANY,    # Christ's eyes like blazing fire
    ('Rev', 2, 18): THEOPHANY,
    ('Rev', 4, 5): THEOPHANY,     # seven torches of fire before throne
    ('Rev', 10, 1): THEOPHANY,    # angel with legs like pillars of fire
    ('Rev', 15, 2): THEOPHANY,    # sea of glass and fire (heavenly throne room)

    # ---- DIVINE JUDGMENT / WRATH ----
    ('Gen', 19, 24): JUDGMENT,    # fire and brimstone on Sodom and Gomorrah
    ('Lev', 10, 2): JUDGMENT,     # fire from LORD consuming Nadab and Abihu
    ('Num', 11, 1): JUDGMENT,     # fire of LORD consuming Taberah
    ('Num', 11, 3): JUDGMENT,
    ('Num', 16, 35): JUDGMENT,    # fire consuming Korah's company
    ('2Sa', 22, 9): JUDGMENT,     # fire from God's nostrils (David's psalm)
    ('2Sa', 22, 13): JUDGMENT,
    ('Psa', 18, 8): JUDGMENT,     # fire from God (parallel of 2 Sam 22)
    ('Psa', 18, 12): JUDGMENT,
    ('Psa', 18, 13): JUDGMENT,
    ('Psa', 50, 3): JUDGMENT,     # fire devours before him in judgment
    ('Psa', 83, 14): JUDGMENT,    # prayer for judgment — fire on enemies
    ('Isa', 5, 24): JUDGMENT,     # fire consuming chaff (judgment on Israel)
    ('Isa', 9, 18): JUDGMENT,     # fire of wrath burning through wickedness
    ('Isa', 9, 19): JUDGMENT,
    ('Isa', 10, 16): JUDGMENT,    # burning under his glory
    ('Isa', 10, 17): JUDGMENT,    # light of Israel becomes fire
    ('Isa', 29, 6): JUDGMENT,     # flame of devouring fire
    ('Isa', 30, 27): JUDGMENT,    # name of LORD burning with fire
    ('Isa', 30, 30): JUDGMENT,
    ('Isa', 30, 33): JUDGMENT,    # Tophet prepared — fire
    ('Isa', 31, 9): JUDGMENT,     # fire in Jerusalem — LORD's fire
    ('Isa', 33, 11): JUDGMENT,
    ('Isa', 33, 14): JUDGMENT,
    ('Isa', 34, 9): JUDGMENT,     # Edom — land burning with pitch
    ('Isa', 34, 10): JUDGMENT,
    ('Isa', 47, 14): JUDGMENT,    # fire consuming Babylon
    ('Isa', 50, 11): JUDGMENT,    # walking in fire of judgment
    ('Isa', 66, 15): JUDGMENT,    # LORD coming with fire
    ('Isa', 66, 16): JUDGMENT,
    ('Jer', 4, 4): JUDGMENT,      # fire of wrath — uncircumcised hearts
    ('Jer', 11, 16): JUDGMENT,    # fire on Judah (olive tree)
    ('Jer', 15, 14): JUDGMENT,    # fire of anger
    ('Jer', 17, 4): JUDGMENT,     # fire of anger kindled forever
    ('Jer', 17, 27): JUDGMENT,    # fire in Jerusalem's gates
    ('Jer', 21, 12): JUDGMENT,    # fire of wrath
    ('Jer', 21, 14): JUDGMENT,
    ('Jer', 22, 7): JUDGMENT,     # fire on cedar forests
    ('Jer', 43, 12): JUDGMENT,    # fire on Egypt
    ('Jer', 48, 45): JUDGMENT,    # fire from Sihon against Moab
    ('Jer', 49, 2): JUDGMENT,     # fire on Rabbah of Ammon
    ('Jer', 49, 27): JUDGMENT,    # fire on Damascus
    ('Jer', 50, 32): JUDGMENT,    # fire on Babylon
    ('Jer', 51, 32): JUDGMENT,
    ('Jer', 51, 58): JUDGMENT,
    ('Eze', 5, 2): JUDGMENT,      # fire — sword on Jerusalem
    ('Eze', 5, 4): JUDGMENT,
    ('Eze', 15, 4): JUDGMENT,     # vine wood given to fire (Israel in judgment)
    ('Eze', 15, 5): JUDGMENT,
    ('Eze', 15, 6): JUDGMENT,
    ('Eze', 15, 7): JUDGMENT,
    ('Eze', 19, 12): JUDGMENT,    # fire consuming Israel's king
    ('Eze', 19, 14): JUDGMENT,
    ('Eze', 20, 47): JUDGMENT,    # fire on southern forest (Jerusalem)
    ('Eze', 20, 48): JUDGMENT,
    ('Eze', 21, 3): JUDGMENT,     # sword = fire (judgment on Israel)
    ('Eze', 21, 4): JUDGMENT,
    ('Eze', 21, 5): JUDGMENT,
    ('Eze', 22, 20): JUDGMENT,    # smelted in furnace of judgment
    ('Eze', 22, 21): JUDGMENT,
    ('Eze', 22, 31): JUDGMENT,
    ('Eze', 24, 9): JUDGMENT,     # fire of God's judgment on Jerusalem
    ('Eze', 24, 10): JUDGMENT,
    ('Eze', 24, 11): JUDGMENT,
    ('Eze', 24, 12): JUDGMENT,
    ('Eze', 28, 14): JUDGMENT,    # fire from within (judgment on prince of Tyre)
    ('Eze', 28, 16): JUDGMENT,
    ('Eze', 28, 18): JUDGMENT,
    ('Eze', 30, 8): JUDGMENT,     # fire on Egypt
    ('Eze', 30, 14): JUDGMENT,
    ('Eze', 30, 16): JUDGMENT,
    ('Eze', 36, 5): JUDGMENT,     # fire of jealousy against enemies
    ('Eze', 38, 19): JUDGMENT,    # fire in judgment against Gog
    ('Eze', 38, 22): JUDGMENT,
    ('Eze', 39, 6): JUDGMENT,     # fire on Magog
    ('Amo', 1, 4): JUDGMENT,      # fire on Damascus
    ('Amo', 1, 7): JUDGMENT,      # fire on Gaza
    ('Amo', 1, 10): JUDGMENT,     # fire on Tyre
    ('Amo', 1, 12): JUDGMENT,     # fire on Edom
    ('Amo', 1, 14): JUDGMENT,     # fire on Ammon
    ('Amo', 2, 2): JUDGMENT,      # fire on Moab
    ('Amo', 2, 5): JUDGMENT,      # fire on Judah
    ('Nah', 1, 6): JUDGMENT,      # fire poured out in wrath
    ('Nah', 3, 13): JUDGMENT,     # fire on Nineveh's bars
    ('Nah', 3, 15): JUDGMENT,
    ('Zep', 1, 18): JUDGMENT,     # fire of jealousy consuming the whole earth
    ('Zep', 3, 8): JUDGMENT,
    ('Zec', 9, 4): JUDGMENT,      # fire consuming Tyre
    ('Zec', 11, 1): JUDGMENT,     # fire on Lebanon
    ('Zec', 12, 6): JUDGMENT,     # Jerusalem as burning torch consuming neighbors
    ('Mat', 3, 12): JUDGMENT,     # chaff burned with unquenchable fire
    ('Luk', 3, 17): JUDGMENT,
    ('Mat', 13, 40): JUDGMENT,    # tares thrown into furnace of fire
    ('Mat', 13, 42): JUDGMENT,
    ('Mat', 13, 50): JUDGMENT,
    ('Luk', 9, 54): JUDGMENT,     # disciples asking fire like Elijah (Jesus rebukes)
    ('2Th', 1, 7): JUDGMENT,      # Lord's return in flaming fire
    ('2Th', 1, 8): JUDGMENT,
    ('Heb', 10, 27): JUDGMENT,    # fearful expectation of fiery judgment
    ('Rev', 8, 5): JUDGMENT,      # fire cast to earth (altar)
    ('Rev', 8, 7): JUDGMENT,      # hail and fire (first trumpet)
    ('Rev', 8, 8): JUDGMENT,      # burning mountain cast into sea
    ('Rev', 9, 17): JUDGMENT,     # fire/smoke/sulfur from horses
    ('Rev', 9, 18): JUDGMENT,
    ('Rev', 11, 5): JUDGMENT,     # fire from prophets' mouths
    ('Rev', 14, 10): JUDGMENT,    # fire and sulfur (beast worshippers)
    ('Rev', 16, 8): JUDGMENT,     # scorching fire (fourth bowl)
    ('Rev', 17, 16): JUDGMENT,    # Babylon burned with fire
    ('Rev', 18, 8): JUDGMENT,
    ('Rev', 20, 9): JUDGMENT,     # fire from God consuming Gog and Magog

    # ---- ESCHATOLOGICAL ----
    ('Isa', 66, 24): ESCHATOLOGICAL,  # unquenched fire on the wicked (basis for Gehenna)
    ('Dan', 7, 11): ESCHATOLOGICAL,   # beast destroyed and given to the burning flame
    ('Mal', 4, 1): ESCHATOLOGICAL,    # day coming burning like a furnace
    ('Mat', 5, 22): ESCHATOLOGICAL,   # Gehenna of fire
    ('Mat', 18, 8): ESCHATOLOGICAL,   # eternal fire
    ('Mat', 18, 9): ESCHATOLOGICAL,   # Gehenna of fire
    ('Mat', 25, 41): ESCHATOLOGICAL,  # eternal fire prepared for devil and his angels
    ('Mrk', 9, 43): ESCHATOLOGICAL,   # unquenchable fire (Gehenna)
    ('Mrk', 9, 44): ESCHATOLOGICAL,
    ('Mrk', 9, 45): ESCHATOLOGICAL,
    ('Mrk', 9, 46): ESCHATOLOGICAL,
    ('Mrk', 9, 47): ESCHATOLOGICAL,
    ('Mrk', 9, 48): ESCHATOLOGICAL,
    ('Luk', 12, 5): ESCHATOLOGICAL,   # fear him who can throw into Gehenna
    ('Luk', 16, 24): ESCHATOLOGICAL,  # rich man in torment (fire)
    ('Jud', 1, 7): ESCHATOLOGICAL,    # eternal fire of Sodom as example
    ('Jud', 1, 23): ESCHATOLOGICAL,   # snatching some from fire
    ('2Pe', 3, 7): ESCHATOLOGICAL,    # earth reserved for fire at judgment
    ('2Pe', 3, 10): ESCHATOLOGICAL,   # elements burned up
    ('2Pe', 3, 12): ESCHATOLOGICAL,   # elements melting in fervent heat
    ('Rev', 19, 20): ESCHATOLOGICAL,  # beast thrown into lake of fire
    ('Rev', 20, 10): ESCHATOLOGICAL,  # devil in lake of fire
    ('Rev', 20, 14): ESCHATOLOGICAL,  # death and Hades cast into lake of fire
    ('Rev', 20, 15): ESCHATOLOGICAL,  # lake of fire — second death
    ('Rev', 21, 8): ESCHATOLOGICAL,   # lake of fire and brimstone

    # ---- PURIFICATION / REFINING ----
    ('Num', 31, 22): PURIFICATION,    # metals purified through fire
    ('Num', 31, 23): PURIFICATION,
    ('Psa', 12, 6): PURIFICATION,     # silver tried in furnace of earth
    ('Psa', 66, 10): PURIFICATION,    # tried as silver is tried
    ('Pro', 17, 3): PURIFICATION,     # furnace for gold — LORD tries hearts
    ('Pro', 27, 21): PURIFICATION,    # furnace for gold
    ('Isa', 1, 25): PURIFICATION,     # smelt away dross with lye
    ('Isa', 48, 10): PURIFICATION,    # refined in the furnace of affliction
    ('Jer', 6, 29): PURIFICATION,     # bellows blow, lead consumed by fire
    ('Eze', 22, 18): PURIFICATION,    # Israel as dross in furnace
    ('Eze', 22, 19): PURIFICATION,
    ('Zec', 13, 9): PURIFICATION,     # refined like silver, tested like gold
    ('Mal', 3, 2): PURIFICATION,      # refiner's fire
    ('Mal', 3, 3): PURIFICATION,
    ('1Co', 3, 13): PURIFICATION,     # fire testing each person's work
    ('1Co', 3, 14): PURIFICATION,
    ('1Co', 3, 15): PURIFICATION,
    ('1Pe', 1, 7): PURIFICATION,      # faith tested by fire more precious than gold
    ('Rev', 3, 18): PURIFICATION,     # buy gold refined by fire

    # ---- SYMBOLIC / METAPHORICAL ----
    ('Pro', 6, 27): SYMBOLIC,         # fire in bosom — metaphor for adultery
    ('Pro', 16, 27): SYMBOLIC,        # burning fire on lips of a worthless man
    ('Pro', 25, 22): SYMBOLIC,        # coals of fire on enemy's head
    ('Psa', 39, 3): SYMBOLIC,         # fire burning within (inner anguish / meditation)
    ('Psa', 69, 9): SYMBOLIC,         # zeal consuming (quoted in John 2:17)
    ('Son', 8, 6): SYMBOLIC,          # love with flashes of fire
    ('Jer', 20, 9): SYMBOLIC,         # God's word like fire shut up in bones
    ('Jer', 23, 29): SYMBOLIC,        # is not my word like fire
    ('Luk', 12, 49): SYMBOLIC,        # I came to cast fire on the earth
    ('Luk', 24, 32): SYMBOLIC,        # hearts burning within on road to Emmaus
    ('Jhn', 2, 17): SYMBOLIC,         # zeal consuming (quotes Ps 69:9)
    ('Jas', 3, 6): SYMBOLIC,          # the tongue is a fire
    ('Rom', 12, 20): SYMBOLIC,        # heap coals of fire on his head (quotes Prov 25:22)

    # ---- AMBIGUOUS ----
    ('Gen', 22, 6): AMBIGUOUS,        # Abraham carrying fire for the offering
    ('Gen', 22, 7): AMBIGUOUS,        # where is the fire? (anticipates sacrifice)
    ('Isa', 6, 6): AMBIGUOUS,         # live coal from altar (theophany + purification)
    ('Isa', 6, 7): AMBIGUOUS,
    ('Psa', 148, 8): AMBIGUOUS,       # fire and hail praising God (creation praise)
    ('Eze', 22, 18): PURIFICATION,    # already PURIFICATION above — dup handled by last-wins
    ('Jer', 5, 14): AMBIGUOUS,        # word of LORD like fire (judgment + symbolic)
}


def categorize(book: str, ch: int, vs: int, strong: str) -> str:
    """Return semantic category for a fire token."""
    if strong == 'H801':
        return OFFERING
    return VERSE_CATEGORY.get((book, ch, vs), MUNDANE)


# ============================================================
# Load data
# ============================================================
print('Loading data...')
ot = load_syntax_ot()
lxx_df = query_lxx(include_deuterocanon=False)
nt = load_nt()
trans = load_translations()
kjv = trans[trans['translation'] == 'KJV']
print('Data loaded.')


def kjv_text(book: str, ch: int, vs: int) -> str:
    r = kjv[(kjv['book_id'] == book) & (kjv['chapter'] == ch) & (kjv['verse'] == vs)]
    return r['text'].values[0] if len(r) else ''


# ============================================================
# Filter fire terms
# ============================================================
ot_fire = ot[ot['strong_h'].isin(OT_FIRE_STRONGS.keys())].copy()
nt_fire = nt[nt['strong_g'].isin(NT_FIRE_STRONGS.keys())].copy()
lxx_fire = lxx_df[lxx_df['strongs'].isin(LXX_FIRE_STRONGS)].copy()

print(f'OT fire tokens: {len(ot_fire)}')
print(f'NT fire tokens: {len(nt_fire)}')
print(f'LXX fire tokens: {len(lxx_fire)}')


# ============================================================
# Build OT rows with categorization
# ============================================================
ot_rows = []
for _, r in ot_fire.iterrows():
    b, c, v = r['book'], int(r['chapter']), int(r['verse'])
    strong = r['strong_h']
    cat = categorize(b, c, v, strong)
    ot_rows.append({
        'ref': f'{b} {c}:{v}',
        'testament': 'OT',
        'book': b,
        'chapter': c,
        'verse': v,
        'form': r['text'],
        'lemma': OT_FIRE_STRONGS.get(strong, r.get('lemma', '')),
        'strong_id': strong,
        'pos': r.get('pos', r.get('class_', '')),
        'morph': r.get('morph', ''),
        'gloss': r.get('gloss', ''),
        'lxx_word': r.get('greek', ''),
        'category': cat,
        'kjv': kjv_text(b, c, v),
    })

ot_df = pd.DataFrame(ot_rows)

# ============================================================
# Build NT rows with categorization
# ============================================================
nt_rows = []
for _, r in nt_fire.iterrows():
    b, c, v = r['book'], int(r['chapter']), int(r['verse'])
    strong = r['strong_g']
    cat = categorize(b, c, v, strong)
    nt_rows.append({
        'ref': f'{b} {c}:{v}',
        'testament': 'NT',
        'book': b,
        'chapter': c,
        'verse': v,
        'form': r['text'],
        'lemma': NT_FIRE_STRONGS.get(strong, r.get('lemma', '')),
        'strong_id': strong,
        'pos': r.get('class_', ''),
        'morph': r.get('morph', ''),
        'gloss': r.get('gloss', ''),
        'lxx_word': '',
        'category': cat,
        'kjv': kjv_text(b, c, v),
    })

nt_df = pd.DataFrame(nt_rows)

# Combined CSV
all_df = pd.concat([ot_df, nt_df], ignore_index=True)
csv_path = OUT / 'fire_all_references.csv'
all_df.to_csv(csv_path, index=False)
for p in (OUT / 'fire_all_references.csv', MK_OUT / 'fire_all_references.csv'):
    all_df.to_csv(p, index=False)
print(f'Combined CSV: {len(all_df)} rows → {csv_path}')

# ============================================================
# Summary counts
# ============================================================
ot_cat = ot_df.groupby('category').size().to_dict()
nt_cat = nt_df.groupby('category').size().to_dict()

ot_total = len(ot_df)
nt_total = len(nt_df)


# ============================================================
# Helper: deduplicate to verse level for category lookup
# (multiple tokens per verse should share same category row)
# ============================================================
def verse_level(df: pd.DataFrame) -> pd.DataFrame:
    """One row per (book, chapter, verse, category)."""
    return df.drop_duplicates(subset=['book', 'chapter', 'verse', 'strong_id'])


# ============================================================
# CHARTS
# ============================================================
print('Generating charts...')


def save_chart(fig: plt.Figure, name: str) -> None:
    for d in (CHART_OUT, MK_CHART):
        p = d / name
        fig.savefig(p, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Chart saved: {name}')


# --- Chart 1: OT category distribution (horizontal bar) ---
ot_cats = [(c, ot_cat.get(c, 0)) for c in CATEGORIES_ORDER if ot_cat.get(c, 0) > 0]
labels1, vals1 = zip(*ot_cats) if ot_cats else ([], [])
colors1 = [CAT_COLORS[c] for c in labels1]

fig1, ax1 = plt.subplots(figsize=(10, 5))
bars1 = ax1.barh(labels1, vals1, color=colors1, edgecolor='white')
for bar, v in zip(bars1, vals1):
    ax1.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
             str(v), va='center', fontsize=10, fontweight='bold')
ax1.set_xlabel('Occurrences', fontsize=10)
ax1.xaxis.grid(True, linestyle='--', alpha=0.4)
ax1.set_axisbelow(True)
ax1.set_title(
    get_display('OT Fire Vocabulary by Semantic Category — אֵשׁ and Related Terms'),
    fontsize=12, fontweight='bold')
fig1.tight_layout()
save_chart(fig1, 'fire_ot_categories.png')

# --- Chart 2: NT category distribution ---
nt_cats = [(c, nt_cat.get(c, 0)) for c in CATEGORIES_ORDER if nt_cat.get(c, 0) > 0]
labels2, vals2 = zip(*nt_cats) if nt_cats else ([], [])
colors2 = [CAT_COLORS[c] for c in labels2]

fig2, ax2 = plt.subplots(figsize=(10, 5))
bars2 = ax2.barh(labels2, vals2, color=colors2, edgecolor='white')
for bar, v in zip(bars2, vals2):
    ax2.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
             str(v), va='center', fontsize=10, fontweight='bold')
ax2.set_xlabel('Occurrences', fontsize=10)
ax2.xaxis.grid(True, linestyle='--', alpha=0.4)
ax2.set_axisbelow(True)
ax2.set_title(
    'NT Fire Vocabulary by Semantic Category — πῦρ and Related Terms',
    fontsize=12, fontweight='bold')
fig2.tight_layout()
save_chart(fig2, 'fire_nt_categories.png')

# --- Chart 3: OT distribution by book (top 15 books) ---
ot_book_ct = ot_df[ot_df['strong_id'] == 'H784']['book'].value_counts().nlargest(16)
OT_BOOK_ORDER = [
    'Gen', 'Exo', 'Lev', 'Num', 'Deu', 'Jdg', '1Sa', '2Sa', '1Ki', '2Ki',
    '2Ch', 'Psa', 'Pro', 'Isa', 'Jer', 'Eze', 'Dan', 'Amo', 'Zec',
]
ot_books3 = [b for b in OT_BOOK_ORDER if b in ot_book_ct.index]
vals3 = [ot_book_ct.get(b, 0) for b in ot_books3]

fig3, ax3 = plt.subplots(figsize=(14, 5))
bars3 = ax3.bar(range(len(ot_books3)), vals3, color='#e08d3c', edgecolor='white')
for bar, v in zip(bars3, vals3):
    if v:
        ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                 str(v), ha='center', va='bottom', fontsize=9, fontweight='bold')
ax3.set_xticks(range(len(ot_books3)))
ax3.set_xticklabels(ot_books3, fontsize=9)
ax3.set_ylabel('Occurrences', fontsize=10)
ax3.yaxis.grid(True, linestyle='--', alpha=0.4)
ax3.set_axisbelow(True)
ax3.set_title(
    get_display('OT Distribution of אֵשׁ (H784) by Book'),
    fontsize=12, fontweight='bold')
fig3.tight_layout()
save_chart(fig3, 'fire_ot_by_book.png')

# --- Chart 4: NT distribution by book ---
NT_BOOK_ORDER = ['Mat', 'Mrk', 'Luk', 'Jhn', 'Act', 'Rom', '1Co', '2Th', 'Heb', 'Jas',
                 '1Pe', '2Pe', 'Jud', 'Rev']
nt_book_ct = nt_df['book'].value_counts()
nt_books4 = [b for b in NT_BOOK_ORDER if b in nt_book_ct.index]
vals4 = [nt_book_ct.get(b, 0) for b in nt_books4]

fig4, ax4 = plt.subplots(figsize=(12, 5))
bars4 = ax4.bar(range(len(nt_books4)), vals4, color='#4393c3', edgecolor='white')
for bar, v in zip(bars4, vals4):
    if v:
        ax4.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                 str(v), ha='center', va='bottom', fontsize=9, fontweight='bold')
ax4.set_xticks(range(len(nt_books4)))
ax4.set_xticklabels(nt_books4, fontsize=9)
ax4.set_ylabel('Occurrences', fontsize=10)
ax4.yaxis.grid(True, linestyle='--', alpha=0.4)
ax4.set_axisbelow(True)
ax4.set_title('NT Fire Vocabulary by Book (πῦρ and related terms)',
              fontsize=12, fontweight='bold')
fig4.tight_layout()
save_chart(fig4, 'fire_nt_by_book.png')

# --- Chart 5: Genre distribution ---
all_df['genre'] = all_df['book'].map(GENRE_MAP).fillna('Other')
ot_genre = all_df[all_df['testament'] == 'OT']['genre'].value_counts()
nt_genre = all_df[all_df['testament'] == 'NT']['genre'].value_counts()

GENRE_ORDER = [
    'Pentateuch', 'History', 'Poetry / Wisdom',
    'Major Prophets', 'Minor Prophets',
    'Gospels', 'Acts', 'Pauline Epistles', 'General Epistles', 'Apocalyptic',
]
ot_g_vals = [ot_genre.get(g, 0) for g in GENRE_ORDER]
nt_g_vals = [nt_genre.get(g, 0) for g in GENRE_ORDER]
x5 = range(len(GENRE_ORDER))
w5 = 0.38

fig5, ax5 = plt.subplots(figsize=(14, 5))
barsA = ax5.bar([i - w5 / 2 for i in x5], ot_g_vals, w5, color='#e08d3c', label='OT')
barsB = ax5.bar([i + w5 / 2 for i in x5], nt_g_vals, w5, color='#4393c3', label='NT')
for bar, v in zip(barsA, ot_g_vals):
    if v:
        ax5.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                 str(v), ha='center', fontsize=8, fontweight='bold')
for bar, v in zip(barsB, nt_g_vals):
    if v:
        ax5.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                 str(v), ha='center', fontsize=8, fontweight='bold')
ax5.set_xticks(list(x5))
ax5.set_xticklabels(GENRE_ORDER, rotation=25, ha='right', fontsize=9)
ax5.set_ylabel('Occurrences', fontsize=10)
ax5.yaxis.grid(True, linestyle='--', alpha=0.4)
ax5.set_axisbelow(True)
ax5.legend(fontsize=10)
ax5.set_title('Fire Vocabulary Distribution by Genre', fontsize=12, fontweight='bold')
fig5.tight_layout()
save_chart(fig5, 'fire_genre_distribution.png')

print('All charts saved.')


# ============================================================
# Build markdown report
# ============================================================

def trunc(s: str, n: int = 100) -> str:
    s = str(s).replace('\n', ' ').strip()
    return s[:n] + '…' if len(s) > n else s


def ref_table_ot(df: pd.DataFrame) -> str:
    """Markdown table for OT category section."""
    seen: set = set()
    rows = []
    for _, r in df.iterrows():
        key = (r['book'], r['chapter'], r['verse'])
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            f"| {r['ref']} | {r['form']} | {r['lemma']} ({r['strong_id']}) "
            f"| {trunc(r['kjv'])} |"
        )
    header = '| Reference | Form | Lemma | KJV |\n|---|---|---|---|'
    return header + '\n' + '\n'.join(rows) if rows else '_No entries._'


def ref_table_nt(df: pd.DataFrame) -> str:
    """Markdown table for NT category section."""
    seen: set = set()
    rows = []
    for _, r in df.iterrows():
        key = (r['book'], r['chapter'], r['verse'])
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            f"| {r['ref']} | {r['form']} | {r['lemma']} ({r['strong_id']}) "
            f"| {trunc(r['kjv'])} |"
        )
    header = '| Reference | Form | Lemma | KJV |\n|---|---|---|---|'
    return header + '\n' + '\n'.join(rows) if rows else '_No entries._'


def section_counts(cat_dict: dict) -> str:
    total = sum(cat_dict.values())
    lines = []
    for c in CATEGORIES_ORDER:
        n = cat_dict.get(c, 0)
        if n:
            pct = 100 * n / total if total else 0
            lines.append(f'| {c} | {n} | {pct:.0f}% |')
    header = '| Category | Count | % of Total |\n|---|---|---|'
    return header + '\n' + '\n'.join(lines)


# Lexical overview table
ot_lemma_ct = ot_df.groupby(['lemma', 'strong_id']).size().reset_index(name='count')
ot_lemma_ct['lang'] = 'Hebrew OT'
nt_lemma_ct = nt_df.groupby(['lemma', 'strong_id']).size().reset_index(name='count')
nt_lemma_ct['lang'] = 'Greek NT'


def lexical_table() -> str:
    rows = []
    for _, r in ot_lemma_ct.sort_values('count', ascending=False).iterrows():
        rows.append(f"| {r['lemma']} | {r['lang']} | {r['strong_id']} | {r['count']} |")
    for _, r in nt_lemma_ct.sort_values('count', ascending=False).iterrows():
        rows.append(f"| {r['lemma']} | {r['lang']} | {r['strong_id']} | {r['count']} |")
    header = '| Lemma | Corpus | Strong\'s | Occurrences |\n|---|---|---|---|'
    return header + '\n' + '\n'.join(rows)


# Intertextual links table (hardcoded — exegetically established)
INTERTEXTUAL = [
    ('Exod 3:2', 'Burning bush', 'Acts 7:30',
     'Stephen quotes: "the angel in the flame of the burning bush"'),
    ('Ps 69:9', 'Zeal consuming me', 'John 2:17',
     'Disciples recall Ps 69:9 at temple cleansing'),
    ('Ps 69:9', 'Zeal consuming me', 'Rom 15:3',
     "Paul applies Ps 69:9 to Christ's self-denial"),
    ('Isa 66:24', 'Unquenched fire on corpses', 'Mark 9:48',
     'Jesus quotes: "where their worm does not die and fire is not quenched"'),
    ('Dan 7:9–10', 'River of fire from Ancient of Days', 'Rev 20:11–15',
     'Great White Throne judgment echoes Dan 7 imagery'),
    ('Mal 3:2', "Refiner's fire", 'Matt 3:11–12',
     "John's baptism of fire and Spirit echoes Malachi"),
    ('Mal 4:1', 'Day burning like furnace', 'Matt 13:42',
     'Furnace of fire at end of age'),
    ('Gen 19:24', 'Fire on Sodom', 'Jude 7',
     'Sodom as "example of eternal fire"'),
    ('Gen 19:24', 'Fire on Sodom', 'Luke 17:29',
     "Jesus references Sodom's destruction"),
    ('Prov 25:22', 'Coals of fire on head', 'Rom 12:20',
     'Paul quotes verbatim from LXX'),
    ('1 Kgs 18:38', "Fire from LORD on Elijah's altar", 'Luke 9:54',
     'Disciples ask Jesus to call fire like Elijah did'),
    ('Exod 13:21', 'Pillar of fire', 'Heb 12:18',
     'Hebrews contrasts Sinai fire with Mt. Zion'),
    ('Deu 4:24', 'God is a consuming fire', 'Heb 12:29',
     'Direct quotation'),
]


def intertextual_table() -> str:
    rows = [
        f'| {ot_ref} | {desc} | {nt_ref} | {connection} |'
        for ot_ref, desc, nt_ref, connection in INTERTEXTUAL
    ]
    header = '| OT Passage | Theme | NT Passage | Connection |\n|---|---|---|---|'
    return header + '\n' + '\n'.join(rows)


# Book distribution tables
def book_dist_table_ot() -> str:
    ct = ot_df.groupby('book').size().sort_values(ascending=False)
    rows = [f'| {b} | {n} |' for b, n in ct.items()]
    return '| Book | Count |\n|---|---|\n' + '\n'.join(rows)


def book_dist_table_nt() -> str:
    ct = nt_df.groupby('book').size().sort_values(ascending=False)
    rows = [f'| {b} | {n} |' for b, n in ct.items()]
    return '| Book | Count |\n|---|---|\n' + '\n'.join(rows)


# Category subsections
def cat_section_ot(cat: str, header_level: str = '###') -> str:
    sub = ot_df[ot_df['category'] == cat]
    n = len(sub)
    if n == 0:
        return ''
    lines = [f'\n{header_level} OT: {cat}\n']
    if cat in (MUNDANE, OFFERING):
        lines.append(f'**{n} occurrence{"s" if n != 1 else ""}** across '
                     f'{sub["book"].nunique()} book{"s" if sub["book"].nunique() != 1 else ""}.')
        if cat == MUNDANE:
            lines.append('\nThese are cooking fires, torches, burning of cities in warfare, '
                         'and other non-theological uses. Individual references are omitted; '
                         'see `fire_all_references.csv` for the complete list.')
        else:
            by_book = sub['book'].value_counts()
            lines.append('\n' + book_mini_table(by_book))
    else:
        lines.append(ref_table_ot(sub))
    return '\n'.join(lines)


def cat_section_nt(cat: str, header_level: str = '###') -> str:
    sub = nt_df[nt_df['category'] == cat]
    n = len(sub)
    lines = [f'\n{header_level} NT: {cat}\n']
    if n == 0:
        lines.append('_None identified within this study\'s term set._')
    elif cat == MUNDANE:
        lines.append(f'**{n} occurrence{"s" if n != 1 else ""}** across '
                     f'{sub["book"].nunique()} book{"s" if sub["book"].nunique() != 1 else ""}. '
                     'Includes campfire at Peter\'s denial (John 18:18) and Paul\'s fire on Malta '
                     '(Acts 28:2–3). See `fire_all_references.csv` for the complete list.')
    else:
        lines.append(ref_table_nt(sub))
    return '\n'.join(lines)


def book_mini_table(ct: pd.Series) -> str:
    rows = [f'| {b} | {n} |' for b, n in ct.items()]
    return '| Book | Count |\n|---|---|\n' + '\n'.join(rows)


# ============================================================
# Genre distribution table for report
# ============================================================
def genre_table() -> str:
    rows = []
    for g in GENRE_ORDER:
        ot_n = ot_genre.get(g, 0)
        nt_n = nt_genre.get(g, 0)
        if ot_n or nt_n:
            rows.append(f'| {g} | {ot_n or "—"} | {nt_n or "—"} |')
    return '| Genre | OT Occurrences | NT Occurrences |\n|---|---|---|\n' + '\n'.join(rows)


# ============================================================
# Assemble the report
# ============================================================
TODAY = '2026-06-13'

KEY_OBS = (
    "- **Fire dominates the prophets**: Ezekiel (OT) and Revelation (NT) contain the highest "
    "concentrations of fire language, reflecting their apocalyptic-judgment orientation.\n"
    "- **Judgment is the primary theological register**: Across both testaments, divine judgment "
    "accounts for the largest share of theologically significant fire references, followed closely "
    "by divine presence/theophany.\n"
    "- **The refining arc**: The OT refining/purification theme (Ps 12:6; Mal 3:2–3; Zech 13:9) "
    "finds direct NT application in 1 Cor 3:13–15 and 1 Pet 1:7, forming a coherent "
    "cross-testament thread.\n"
    "- **Eschatological fire is almost exclusively NT**: While Dan 7:9–11, Isa 66:24, and Mal 4:1 "
    "establish OT roots, the explicit Gehenna and lake-of-fire imagery is predominantly NT and "
    "concentrated in the Synoptics and Revelation.\n"
    "- **Pentateuch and Major Prophets dominate the OT**: The Pentateuch establishes fire as "
    "theophanic (Exod) and as cultic/offering (Lev), while the Major Prophets expand it into a "
    "vehicle for judgment oracles."
)

GENRE_NOTES = (
    "- Major Prophets (Isa, Jer, Eze, Dan) carry the heaviest OT fire load — primarily "
    "judgment oracles.\n"
    "- Apocalyptic (Revelation) dominates the NT, with Gehenna references spreading across "
    "the Gospels.\n"
    "- The Pentateuch's high count reflects both the theophanic fire of Sinai/Exodus narratives "
    "and the cultic אִשֶּּה (offering-by-fire) legislation "
    "of Leviticus."
)

SCRIPT_LINK = (
    "*Build script: [scripts/both/word_studies/fire/build_fire_report.py]"
    "(../../../../scripts/both/word_studies/fire/build_fire_report.py)*"
)

report = f"""# Fire in Scripture: A Semantic Study
## Hebrew OT · LXX · Greek NT

*Generated {TODAY}*

{SCRIPT_LINK}

---

## Contents

- [Key Observations](#key-observations)
- [Lexical Overview](#lexical-overview)
- [OT: Fire by Semantic Category](#ot-fire-by-semantic-category)
  - [Divine Presence / Theophany](#ot-divine-presence--theophany)
  - [Divine Judgment / Wrath](#ot-divine-judgment--wrath)
  - [Eschatological Fire](#ot-eschatological-fire)
  - [Purification / Refining](#ot-purification--refining)
  - [Symbolic / Metaphorical](#ot-symbolic--metaphorical)
  - [Ambiguous](#ot-ambiguous)
  - [Mundane Uses](#ot-mundane-uses-count-only)
  - [Offering by Fire](#ot-offering-by-fire-count-only)
- [NT: Fire by Semantic Category](#nt-fire-by-semantic-category)
  - [Divine Presence / Theophany](#nt-divine-presence--theophany)
  - [Divine Judgment / Wrath](#nt-divine-judgment--wrath)
  - [Eschatological Fire](#nt-eschatological-fire)
  - [Purification / Refining](#nt-purification--refining)
  - [Symbolic / Metaphorical](#nt-symbolic--metaphorical)
  - [Mundane Uses](#nt-mundane-uses-count-only)
  - [Ambiguous](#nt-ambiguous)
- [Genre Distribution](#genre-distribution)
- [OT → NT Intertextual Links](#ot--nt-intertextual-links)
- [Data Files](#data-files)

---

## Key Observations

{KEY_OBS}

---

## Lexical Overview

{lexical_table()}

**Terms included in this study:**

*Hebrew OT:* אֵשׁ H784 (fire), אִשֶּׁה H801 (offering by fire), לַהַב H3857 (flame), לַפִּיד H3940 (torch/flame), נוּר H5135 (Aramaic: fire — Daniel).  # noqa: E501

*Greek NT:* πῦρ G4442 (fire), φλόξ G5395 (flame), πυρά G4443 (bonfire), πυρόω G4448 (to be ablaze), πύρωσις G4451 (fiery trial/burning), κατακαίω G2618 (to burn up completely).  # noqa: E501

*Not included:* General burning verbs (H1197 בָּעַר, H3341 יָקַד, G2545 καίω) unless they appear in direct fire-noun constructions captured above.  # noqa: E501

---

## OT: Fire by Semantic Category

![OT fire by semantic category](../../../charts/both/word_studies/fire/fire_ot_categories.png)

{section_counts(ot_cat)}

{cat_section_ot(THEOPHANY)}

{cat_section_ot(JUDGMENT)}

{cat_section_ot(ESCHATOLOGICAL)}

{cat_section_ot(PURIFICATION)}

{cat_section_ot(SYMBOLIC)}

{cat_section_ot(AMBIGUOUS)}

{cat_section_ot(MUNDANE)}

{cat_section_ot(OFFERING)}

---

## OT Distribution by Book

![OT fire by book](../../../charts/both/word_studies/fire/fire_ot_by_book.png)

{book_dist_table_ot()}

---

## NT: Fire by Semantic Category

![NT fire by semantic category](../../../charts/both/word_studies/fire/fire_nt_categories.png)

{section_counts(nt_cat)}

{cat_section_nt(THEOPHANY)}

{cat_section_nt(JUDGMENT)}

{cat_section_nt(ESCHATOLOGICAL)}

{cat_section_nt(PURIFICATION)}

{cat_section_nt(SYMBOLIC)}

{cat_section_nt(MUNDANE)}

{cat_section_nt(AMBIGUOUS)}

---

## NT Distribution by Book

![NT fire by book](../../../charts/both/word_studies/fire/fire_nt_by_book.png)

{book_dist_table_nt()}

---

## Genre Distribution

![Genre distribution](../../../charts/both/word_studies/fire/fire_genre_distribution.png)

{genre_table()}

**Notes:**
{GENRE_NOTES}

---

## OT → NT Intertextual Links

{intertextual_table()}

---

## Data Files

| File | Contents |
|---|---|
| [fire_all_references.csv](fire_all_references.csv) | All OT + NT fire references: reference, form, lemma, Strong's, category, KJV text |  # noqa: E501
"""

# Write report to both output/ and mkdocs_src/
for dest in (OUT / 'fire_word_study.md', MK_OUT / 'fire_word_study.md'):
    dest.write_text(report, encoding='utf-8')
    print(f'Report written: {dest}')

print('Done.')
