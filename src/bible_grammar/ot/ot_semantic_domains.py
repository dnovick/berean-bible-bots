"""
Hebrew OT semantic domain analysis (SDBH / coredomain / lexdomain).

The MACULA Hebrew WLC dataset carries three semantic annotation columns:

  coredomain   — 190 thematic categories from the MARBLE SDBH project
                 (e.g. 046=Deity, 042=Covenant, 189=Worship, 088=Justice)
                 Space-separated when a word spans multiple categories.
                 ~160,923 non-empty tokens.

  lexdomain    — Hierarchical SDBH code (up to 12 digits in groups of 3)
                 Top level: 001=Objects, 002=Events, 003=Referents, 004=Markers
                 ~244,721 non-empty tokens.

  sdbh         — Fine-grained 15-digit MARBLE lexical entry identifier.
                 ~244,734 non-empty tokens.

Questions this answers
──────────────────────
  • What are the most common semantic domains in Isaiah?
  • Which books have the most "Deity" (046) vocabulary?
  • What are the top lemmas in the "Covenant" (042) domain?
  • How does "Worship" vocabulary distribute across Torah vs. Prophets?
  • What coredomain categories cluster in Leviticus vs. Psalms?

Public API
──────────
ot_domain_data(domain=None, book=None, lang='H')   → DataFrame
ot_domain_frequency(book=None, top_n=30)           → DataFrame (domain counts)
ot_top_domain_lemmas(domain, top_n=20, book=None)  → DataFrame
ot_domain_book_distribution(domain)                → DataFrame
ot_domain_genre_profile(domain=None)               → DataFrame
ot_domain_comparison(books, top_n=15)              → pivot DataFrame
ot_coredomain_profile(book, top_n=20)              → DataFrame

print_ot_domain_overview()                         → None
print_ot_domain_frequency(book=None, top_n=30)     → None
print_ot_top_lemmas(domain, top_n=20, book=None)   → None
print_ot_domain_book_distribution(domain)          → None
print_ot_domain_genre_profile(domain)              → None
print_ot_domain_comparison(books, top_n=15)        → None

ot_domain_frequency_chart(book=None, top_n=25)     → Path | None
ot_domain_book_chart(domain, top_n=20)             → Path | None
ot_domain_genre_chart(domain)                      → Path | None
ot_domain_heatmap(books, top_n=15)                 → Path | None

COREDOMAIN_NAMES                                   → dict[str, str]
THEOLOGY_COREDOMAINS                               → dict[str, list[str]]
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd

from ..core._utils import load_ot_data

# ── domain name tables ────────────────────────────────────────────────────────

# Semantic category names for the MACULA Hebrew coredomain column.
# Codes are zero-padded 3-digit strings.  Derived empirically from the top
# glosses in the MACULA Hebrew WLC dataset (the codes do not correspond to
# the MARBLE SDBH domain-label-mapping-2.json numbering).
COREDOMAIN_NAMES: dict[str, str] = {
    '001': 'Ability',          '002': 'Access/Gate',      '004': 'Affection/Love',
    '005': 'Posterity/Son',    '006': 'Violence/Sword',   '007': 'Object Marker (et)',
    '008': 'Drunkenness',      '010': 'Livestock/Flock',  '011': 'Wool/Textile',
    '013': 'Vision',           '014': 'Assembly',         '015': 'Royalty/King',
    '016': 'Beauty/Stones',    '017': 'Ethics/Good-Evil', '018': 'Curse/Oath',
    '019': 'Eye/Sight',        '020': 'Dwelling/House',   '021': 'Burial',
    '023': 'Seed',             '024': 'Nurture',          '025': 'Census',
    '027': 'Object Marker (et)','028': 'Creation',        '030': 'Childbirth/Womb',
    '031': 'Circumcision',     '032': 'Sojourner/Alien',  '033': 'Clothing',
    '034': 'Darkness',         '035': 'Commerce/Trade',   '036': 'Compassion/Grace',
    '037': 'Race',             '038': 'Alone/Apart',      '039': 'Cleanness',
    '040': 'Bondage/Snare',    '041': 'Speech/Utterance', '043': 'Security/Fear',
    '044': 'Enemy/Conflict',   '045': 'Construction/Build','046': 'Covenant/berith',
    '047': 'Refuge',           '049': 'Whitewash/Paint',  '050': 'God/Deity',
    '052': 'Destruction',      '055': 'Divine Name/LORD', '056': 'Interpretation',
    '057': 'Drought',          '058': 'Angel/Messenger',  '059': 'Flesh',
    '061': 'Faithfulness/Hesed','062': 'Kinship/People',  '063': 'Famine/Hunger',
    '064': 'Fasting',          '066': 'Festival/Passover','067': 'Fire',
    '069': 'Food/Eating',      '070': 'Exile',            '071': 'Genealogy',
    '072': 'Hand/Evil',        '073': 'Direction/Place',  '074': 'Nations/Peoples',
    '076': 'Pestilence',       '077': 'Descent',          '078': 'Seeking/Ambush',
    '079': 'Holiness/Sanctuary','081': 'Camp/Settlement', '082': 'Servant/Slave',
    '083': 'Pride/Boasting',   '084': 'Net/Snare',        '085': 'Idols',
    '087': 'Way/Journey',      '090': 'Greatness/Size',   '092': 'Motion/Going',
    '093': 'Joy/Mourning',     '095': 'King/Justice',     '096': 'Lampstand/Light',
    '097': 'Land/Earth',       '098': 'Statutes/Law',     '099': 'Blood/Death',
    '100': 'Time of Day',      '101': 'Water/Liquids',    '102': 'Pledge/Surety',
    '103': 'Lot/Urim-Thummim', '104': 'Divination',       '105': 'Widow/Orphan',
    '106': 'Heart/Mind',       '107': 'Mine/Quarry',      '108': 'Corpse',
    '109': 'Mourning/Fasting', '110': 'Motion/Journey',   '111': 'Music/Psalm',
    '112': 'Nazirite',         '113': 'Naming/Call',      '114': 'Nations',
    '115': 'Wilderness/Mountain','116': 'Ark/Ships',      '117': 'Tent-Pitching',
    '118': 'Oath/Vow',         '120': 'Tablets/Writing',  '121': 'Kinship/People',
    '122': 'Washing/Purification','123': 'Plague/Frogs',  '124': 'Plans/Counsel',
    '125': 'Pasture/Land',     '126': 'Hand/Striking',    '127': 'Alliance/Treaty',
    '128': 'Pasture/Territory','129': 'Kinship/People',   '130': 'Praise/Thanks',
    '131': 'Prayer',           '132': 'Priesthood',       '134': 'Prophecy/Oracle',
    '136': 'Gallows',          '137': 'Moral Purity',     '138': 'Numbers/Counting',
    '139': 'Placing/Setting',  '140': 'Curse',            '142': 'Seeking/Assembly',
    '143': 'Memory/Remembrance','145': 'Sin/Blood',       '146': 'Ark/Cult Object',
    '147': 'Ritual Uncleanness','148': 'Throne/Kingdom',  '149': 'Altar/Sacrifice',
    '150': 'Tent/Tabernacle',  '152': 'Salvation/Rescue', '153': 'Theft/Hiding',
    '154': 'Sight/Vision',     '155': 'Love/Lying',       '156': 'Sharpening',
    '157': 'Sheep/Livestock',  '158': 'Siege/Mound',      '159': 'Signs/Wonders',
    '160': 'Other/Different',  '161': 'Measurement/Cubit','164': 'Sleep/Dream',
    '165': 'Tumult/Noise',     '166': 'Place/Location',   '167': 'Flight/Fleeing',
    '168': 'Beginning/Ending', '169': 'Leaping',          '170': 'Royalty/King',
    '171': 'Ark/Box',          '172': 'Strength/Wall',    '173': 'Futility/Vanity',
    '174': 'Tricks/Cunning',   '176': 'Anger/Wrath',      '177': 'Sun/Heat',
    '178': 'Tent-Pitching',    '180': 'Time/Day',         '181': 'Arrow/Weapon',
    '182': 'City/Town',        '184': 'Deceit/Falsehood', '185': 'Land/Earth',
    '186': 'Stone/Earthenware','187': 'Chariot/Harness',  '188': 'Battle/Warfare',
    '189': 'Water/Waters',     '190': 'Weights/Measures', '191': 'Scroll/Writing',
    '192': 'Wealth/Needy',     '193': 'Rain/Cloud',       '194': 'Weeping',
    '195': 'Well/Spring',      '196': 'Famine/Desire',    '197': 'Willingness/Rebellion',
    '198': 'Wind/Spirit',      '199': 'Wisdom/Knowledge', '200': 'Shepherd/Gatekeeper',
    '202': 'Wrestling',
}

# Top-level lexdomain categories (mapping-1)
LEXDOMAIN_TOP: dict[str, str] = {
    '001': 'Objects',
    '002': 'Events',
    '003': 'Referents',
    '004': 'Markers',
}

# Convenience groupings for theological/pedagogical queries
# Codes are validated against the empirical COREDOMAIN_NAMES table above
THEOLOGY_COREDOMAINS: dict[str, list[str]] = {
    'Divinity':      ['050', '055'],          # God/Deity + Divine Name/LORD
    'Covenant':      ['046', '061', '118'],   # Covenant/berith + Faithfulness/Hesed + Oath/Vow
    'Worship':       ['149', '111', '130', '131'],  # Altar/Sacrifice + Music + Praise + Prayer
    'Priesthood':    ['132', '147', '122', '079'],  # Priesthood + Ritual Uncleanness + Washing + Holiness
    'Prophecy':      ['134', '041', '159'],   # Prophecy/Oracle + Speech + Signs/Wonders
    'Wisdom':        ['199', '124', '184'],   # Wisdom/Knowledge + Plans/Counsel + Deceit/Falsehood
    'Kingship':      ['015', '148', '170', '095'],  # Royalty + Throne + King + Justice
    'Salvation':     ['152', '047', '143'],   # Salvation + Refuge + Memory/Remembrance
    'Creation':      ['028', '097', '185'],   # Creation + Land/Earth (both codes)
    'Warfare':       ['188', '006', '044', '158'],  # Battle + Violence + Enemy + Siege
    'Justice/Law':   ['098', '145', '017'],   # Statutes/Law + Sin/Blood + Ethics
    'Exile/Return':  ['070', '085', '097'],   # Exile + Idols + Land
}

OT_BOOK_GROUPS: dict[str, list[str]] = {
    'Torah':      ['Gen', 'Exo', 'Lev', 'Num', 'Deu'],
    'Historical': ['Jos', 'Jdg', 'Rut', '1Sa', '2Sa', '1Ki', '2Ki',
                   '1Ch', '2Ch', 'Ezr', 'Neh', 'Est'],
    'Wisdom':     ['Job', 'Psa', 'Pro', 'Ecc', 'Sng'],
    'Prophets':   ['Isa', 'Jer', 'Lam', 'Ezk', 'Dan', 'Hos', 'Jol',
                   'Amo', 'Oba', 'Jon', 'Mic', 'Nam', 'Hab', 'Zep',
                   'Hag', 'Zec', 'Mal'],
}

OT_BOOK_ORDER = (
    OT_BOOK_GROUPS['Torah'] + OT_BOOK_GROUPS['Historical'] +
    OT_BOOK_GROUPS['Wisdom'] + OT_BOOK_GROUPS['Prophets']
)

_CHART_DIR = Path('output') / 'charts' / 'ot' / 'semantic_domains'


# ── helpers ───────────────────────────────────────────────────────────────────

def _parse_coredomain(raw: str) -> list[str]:
    """Split a (possibly space-separated) coredomain string into individual codes."""
    if not raw or pd.isna(raw):
        return []
    return [c.strip().zfill(3) for c in raw.split() if c.strip()]


def _resolve_domain(domain: str | int) -> str:
    """Normalise a domain code or name to a 3-digit string key."""
    s = str(domain).strip()
    if s.isdigit():
        return s.zfill(3)
    # Try name match (case-insensitive)
    s_lower = s.lower()
    for code, name in COREDOMAIN_NAMES.items():
        if s_lower in name.lower():
            return code
    return s.zfill(3)


def _ot_hebrew(df: pd.DataFrame) -> pd.DataFrame:
    """Filter to Hebrew words only (exclude Aramaic)."""
    return df[df['lang'] == 'H']


# ── data access ───────────────────────────────────────────────────────────────

def ot_domain_data(
    domain: str | int | None = None,
    *,
    book: str | list[str] | None = None,
    lang: str = 'H',
) -> pd.DataFrame:
    """
    All Hebrew OT tokens, optionally filtered by coredomain and/or book.

    Parameters
    ----------
    domain : coredomain code (e.g. '46', 46, 'Deity') or None for all
    book   : book abbreviation or list of abbreviations
    lang   : 'H' (Hebrew, default) or 'A' (Aramaic) or None (all)
    """
    df = load_ot_data()
    if lang:
        df = df[df['lang'] == lang]

    if book is not None:
        if isinstance(book, str):
            book = [book]
        df = df[df['book'].isin(book)]

    if domain is not None:
        code = _resolve_domain(domain)
        df = df[df['coredomain'].notna() & (df['coredomain'] != '') &
                df['coredomain'].apply(lambda x: code in _parse_coredomain(x))]

    return df.copy().reset_index(drop=True)


def ot_domain_frequency(
    book: str | None = None,
    *,
    top_n: int = 30,
    lang: str = 'H',
    exclude_empty: bool = True,
) -> pd.DataFrame:
    """
    Count how many tokens fall in each coredomain category.

    Returns a DataFrame with: code, domain_name, count, pct.
    """
    df = load_ot_data()
    if lang:
        df = df[df['lang'] == lang]
    if book:
        df = df[df['book'] == book]
    if exclude_empty:
        df = df[df['coredomain'].notna() & (df['coredomain'] != '')]

    rows = []
    for raw in df['coredomain']:
        for code in _parse_coredomain(raw):
            rows.append(code)

    if not rows:
        return pd.DataFrame(columns=['code', 'domain_name', 'count', 'pct'])

    total = len(rows)
    from collections import Counter
    counts = Counter(rows)
    result = pd.DataFrame([
        {'code': k, 'domain_name': COREDOMAIN_NAMES.get(k, k), 'count': v}
        for k, v in counts.items()
    ])
    result['pct'] = (result['count'] / total * 100).round(1)
    return (
        result.sort_values('count', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def ot_top_domain_lemmas(
    domain: str | int,
    *,
    top_n: int = 20,
    book: str | None = None,
    lang: str = 'H',
) -> pd.DataFrame:
    """
    Most frequent lemmas in a given coredomain category.

    Returns: lemma, strong_h, gloss, count.
    """
    df = ot_domain_data(domain, book=book, lang=lang)
    if df.empty:
        return pd.DataFrame(columns=['lemma', 'strong_h', 'gloss', 'count'])

    result = (
        df.groupby(['lemma', 'strong_h', 'gloss'], dropna=False)
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    return result


def ot_domain_book_distribution(
    domain: str | int,
    *,
    lang: str = 'H',
) -> pd.DataFrame:
    """Book-by-book distribution of tokens in a given coredomain."""
    df = ot_domain_data(domain, lang=lang)
    if df.empty:
        return pd.DataFrame(columns=['book', 'count', 'pct'])

    total = len(df)
    counts = df['book'].value_counts().reset_index()
    counts.columns = ['book', 'count']
    counts['pct'] = (counts['count'] / total * 100).round(1)
    order = {b: i for i, b in enumerate(OT_BOOK_ORDER)}
    counts['_ord'] = counts['book'].map(order).fillna(999)
    return counts.sort_values('_ord').drop(columns='_ord').reset_index(drop=True)


def ot_domain_genre_profile(
    domain: str | int | None = None,
    *,
    lang: str = 'H',
) -> pd.DataFrame:
    """
    Genre distribution for a given domain (or all domains if None).

    Returns: genre, count, pct.
    """
    df = ot_domain_data(domain, lang=lang)
    if df.empty:
        return pd.DataFrame(columns=['genre', 'count', 'pct'])

    book_to_genre = {b: g for g, books in OT_BOOK_GROUPS.items() for b in books}
    df = df.copy()
    df['genre'] = df['book'].map(book_to_genre)
    counts = df['genre'].value_counts()
    pct = (counts / len(df) * 100).round(1)
    result = pd.DataFrame({'count': counts, 'pct': pct})
    order = list(OT_BOOK_GROUPS.keys())
    return result.reindex(order).reset_index().rename(columns={'index': 'genre'})


def ot_domain_comparison(
    books: list[str],
    *,
    top_n: int = 15,
    lang: str = 'H',
) -> pd.DataFrame:
    """
    Compare coredomain profiles across multiple OT books.

    Returns a pivot: rows=domain, cols=books, cells=% of book's coded tokens.
    """
    profiles: dict[str, pd.Series] = {}
    for book in books:
        p = ot_domain_frequency(book, top_n=100, lang=lang)
        if not p.empty:
            label = p['code'] + ' ' + p['domain_name']
            profiles[book] = p.set_index(label)['pct']

    if not profiles:
        return pd.DataFrame()

    combined = pd.DataFrame(profiles).fillna(0).round(1)
    combined['_avg'] = combined.mean(axis=1)
    return combined.sort_values('_avg', ascending=False).drop(columns='_avg').head(top_n)


def ot_coredomain_profile(
    book: str,
    *,
    top_n: int = 20,
    lang: str = 'H',
) -> pd.DataFrame:
    """Semantic domain fingerprint for a single OT book."""
    return ot_domain_frequency(book, top_n=top_n, lang=lang)


def ot_theology_profile(
    group: str,
    *,
    book: str | None = None,
) -> pd.DataFrame:
    """
    Token counts for a named theological domain group.

    Parameters
    ----------
    group : key in THEOLOGY_COREDOMAINS (e.g. 'Covenant', 'Worship')
    book  : optional book filter

    Returns lemma-level counts within that theological cluster.
    """
    codes = THEOLOGY_COREDOMAINS.get(group)
    if not codes:
        raise ValueError(f"Unknown theological group '{group}'. "
                         f"Valid: {list(THEOLOGY_COREDOMAINS.keys())}")

    df = load_ot_data()
    df = df[df['lang'] == 'H']
    if book:
        df = df[df['book'] == book]

    def _in_group(raw: str) -> bool:
        return any(c in codes for c in _parse_coredomain(raw))

    mask = df['coredomain'].notna() & (df['coredomain'] != '') & df['coredomain'].map(_in_group)
    subset = df[mask].copy()

    if subset.empty:
        return pd.DataFrame(columns=['lemma', 'strong_h', 'gloss', 'count'])

    result = (
        subset.groupby(['lemma', 'strong_h', 'gloss'], dropna=False)
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .reset_index(drop=True)
    )
    return result


# ── print functions ───────────────────────────────────────────────────────────

def print_ot_domain_overview() -> None:
    df = load_ot_data()
    heb = df[df['lang'] == 'H']
    has_core = heb[(heb['coredomain'].notna()) & (heb['coredomain'] != '')]
    has_lex  = heb[(heb['lexdomain'].notna())  & (heb['lexdomain'] != '')]
    w = 58
    print(f"\n{'═'*w}")
    print("  Hebrew OT Semantic Domain Coverage (SDBH / MARBLE)")
    print(f"{'═'*w}")
    print(f"  Total Hebrew tokens : {len(heb):>10,}")
    print(f"  coredomain coverage : {len(has_core):>10,} ({len(has_core)/len(heb)*100:.1f}%)")
    print(f"  lexdomain coverage  : {len(has_lex):>10,} ({len(has_lex)/len(heb)*100:.1f}%)")
    print(f"  Coredomain categories: {len(COREDOMAIN_NAMES):>7}")
    print()


def print_ot_domain_frequency(
    book: str | None = None,
    *,
    top_n: int = 30,
    lang: str = 'H',
) -> None:
    df = ot_domain_frequency(book, top_n=top_n, lang=lang)
    scope = f" ({book})" if book else " (all OT)"
    w = 62
    print(f"\n{'═'*w}")
    print(f"  Top {top_n} Semantic Domains (coredomain){scope}")
    print(f"{'═'*w}")
    print(f"  {'Code':<5} {'Domain Name':<24} {'Count':>7}  {'%':>5}")
    print(f"  {'-'*4} {'-'*23} {'-'*7}  {'-'*5}")
    for _, row in df.iterrows():
        print(f"  {row['code']:<5} {row['domain_name']:<24} {row['count']:>7,}  {row['pct']:>4.1f}%")
    print()


def print_ot_top_lemmas(
    domain: str | int,
    *,
    top_n: int = 20,
    book: str | None = None,
    lang: str = 'H',
) -> None:
    code = _resolve_domain(domain)
    name = COREDOMAIN_NAMES.get(code, code)
    scope = f" ({book})" if book else ""
    df = ot_top_domain_lemmas(domain, top_n=top_n, book=book, lang=lang)
    w = 68
    print(f"\n{'═'*w}")
    print(f"  Domain {code} — {name}{scope}")
    print(f"{'═'*w}")
    if df.empty:
        print("  No results found.")
        print()
        return
    print(f"  {'Lemma':<14} {'Strong':<8} {'Gloss':<26} {'Count':>6}")
    print(f"  {'-'*13} {'-'*7} {'-'*25} {'-'*6}")
    for _, row in df.iterrows():
        print(f"  {str(row['lemma']):<14} {str(row['strong_h']):<8} "
              f"{str(row['gloss']):<26} {row['count']:>6,}")
    print()


def print_ot_domain_book_distribution(
    domain: str | int,
    *,
    top_n: int = 20,
    lang: str = 'H',
) -> None:
    code = _resolve_domain(domain)
    name = COREDOMAIN_NAMES.get(code, code)
    df = ot_domain_book_distribution(domain, lang=lang).head(top_n)
    print(f"\nDomain {code} ({name}) — Book Distribution")
    print(f"  {'Book':<6} {'Count':>6} {'%':>6}")
    print('  ' + '-' * 22)
    for _, row in df.iterrows():
        print(f"  {row['book']:<6} {row['count']:>6,} {row['pct']:>5.1f}%")
    print()


def print_ot_domain_genre_profile(
    domain: str | int,
    *,
    lang: str = 'H',
) -> None:
    code = _resolve_domain(domain)
    name = COREDOMAIN_NAMES.get(code, code)
    df = ot_domain_genre_profile(domain, lang=lang)
    print(f"\nDomain {code} ({name}) — Genre Profile")
    print(f"  {'Genre':<12} {'Count':>6} {'%':>6}")
    print('  ' + '-' * 28)
    for _, row in df.iterrows():
        print(f"  {str(row['genre']):<12} {row['count']:>6,} {row['pct']:>5.1f}%")
    print()


def print_ot_domain_comparison(
    books: list[str],
    *,
    top_n: int = 15,
    lang: str = 'H',
) -> None:
    df = ot_domain_comparison(books, top_n=top_n, lang=lang)
    if df.empty:
        print("No domain data found for the specified books.")
        return
    print(f"\nDomain Comparison: {', '.join(books)}")
    print("  (% of each book's coredomain-tagged tokens)")
    print()
    header = f"  {'Domain':<28}" + ''.join(f" {b:>7}" for b in df.columns)
    print(header)
    print('  ' + '-' * (28 + 8 * len(df.columns)))
    for domain_label, row in df.iterrows():
        print(f"  {str(domain_label):<28}" + ''.join(f" {v:>6.1f}%" for v in row))
    print()


def print_ot_theology_profile(group: str, book: str | None = None) -> None:
    codes = THEOLOGY_COREDOMAINS.get(group, [])
    names = [COREDOMAIN_NAMES.get(c, c) for c in codes]
    scope = f" ({book})" if book else ""
    df = ot_theology_profile(group, book=book)
    w = 62
    print(f"\n{'═'*w}")
    print(f"  Theological Cluster: {group}{scope}")
    print(f"  Domains: {', '.join(f'{c} ({n})' for c, n in zip(codes, names))}")
    print(f"{'═'*w}")
    if df.empty:
        print("  No results found.")
        print()
        return
    print(f"  {'Lemma':<14} {'Strong':<8} {'Gloss':<26} {'Count':>6}")
    print(f"  {'-'*13} {'-'*7} {'-'*25} {'-'*6}")
    for _, row in df.head(25).iterrows():
        print(f"  {str(row['lemma']):<14} {str(row['strong_h']):<8} "
              f"{str(row['gloss']):<26} {row['count']:>6,}")
    print()


# ── chart functions ───────────────────────────────────────────────────────────

def ot_domain_frequency_chart(
    book: str | None = None,
    *,
    top_n: int = 25,
    lang: str = 'H',
) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = ot_domain_frequency(book, top_n=top_n, lang=lang)
    if df.empty:
        return None

    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    suffix = f"_{book}" if book else ""
    out = _CHART_DIR / f"domain_frequency{suffix}.png"

    labels = [f"{row['code']} {row['domain_name']}" for _, row in df.iterrows()]
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.barh(labels[::-1], df['count'][::-1], color='steelblue')
    scope = f" ({book})" if book else " — All OT"
    ax.set_xlabel('Token count')
    ax.set_title(f'Top {top_n} Semantic Domains{scope}')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def ot_domain_book_chart(
    domain: str | int,
    *,
    top_n: int = 20,
    lang: str = 'H',
) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    code = _resolve_domain(domain)
    name = COREDOMAIN_NAMES.get(code, code)
    df = ot_domain_book_distribution(domain, lang=lang).head(top_n)
    if df.empty:
        return None

    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    out = _CHART_DIR / f"domain_{code}_books.png"

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df['book'][::-1], df['count'][::-1], color='darkorange')
    ax.set_xlabel('Token count')
    ax.set_title(f'Domain {code} ({name}) — Top {top_n} Books')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def ot_domain_genre_chart(
    domain: str | int,
    *,
    lang: str = 'H',
) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    code = _resolve_domain(domain)
    name = COREDOMAIN_NAMES.get(code, code)
    df = ot_domain_genre_profile(domain, lang=lang).dropna(subset=['count'])
    if df.empty:
        return None

    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    out = _CHART_DIR / f"domain_{code}_genre.png"

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(df['genre'], df['count'], color='darkorange')
    ax.set_ylabel('Token count')
    ax.set_title(f'Domain {code} ({name}) — Genre Distribution')
    for i, (g, c) in enumerate(zip(df['genre'], df['count'])):
        if pd.notna(c):
            ax.text(i, c + 1, str(int(c)), ha='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def ot_domain_heatmap(
    books: list[str],
    *,
    top_n: int = 15,
    lang: str = 'H',
) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = ot_domain_comparison(books, top_n=top_n, lang=lang)
    if df.empty:
        return None

    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    out = _CHART_DIR / 'domain_heatmap.png'

    data = df.values.astype(float)
    fig, ax = plt.subplots(figsize=(max(8, len(books) * 1.2), max(6, top_n * 0.55)))
    im = ax.imshow(data, aspect='auto', cmap='YlOrRd')
    ax.set_xticks(range(len(df.columns)))
    ax.set_xticklabels(df.columns, rotation=45, ha='right')
    ax.set_yticks(range(len(df.index)))
    ax.set_yticklabels([str(s)[:30] for s in df.index], fontsize=8)
    plt.colorbar(im, ax=ax, label='% of book tokens')
    ax.set_title(f'Semantic Domain Heatmap — {", ".join(books)}')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out
