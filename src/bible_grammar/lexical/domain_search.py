"""
Louw-Nida semantic domain search for the Greek NT (MACULA Greek).

Each word token in the MACULA Greek NT carries a `domain` column
(e.g. '033006') and an `ln` column (e.g. '33.69'), both referencing
the Louw-Nida Greek-English Lexicon of the New Testament.

Domain format
─────────────
  domain:  zero-padded 6-digit string  '033006'  (domain 33, subdomain 6)
  ln:      dot-separated decimal       '33.69'    (domain 33, section 69)

  Top-level domains 1–93; subdomains further classify meaning.
  A single word may carry multiple domain entries (space-separated).

Questions this answers
──────────────────────
  • What Communication-domain verbs does God use in the NT?
  • Which Supernatural-Being words cluster in the book of Revelation?
  • What Moral/Ethical-quality terms appear in Paul?
  • Which Judgment-domain verbs does Jesus take as subject in the Gospels?
  • What is the domain profile of Hebrews vs Romans?

Public API
──────────
query_domain(domain, ...)              → filtered token DataFrame
domain_profile(book, ...)             → domain distribution for a book
domain_role_search(domain, subject_strongs, ...) → domain words where entity is subject
top_domain_words(domain, ...)         → most frequent words in a domain
print_domain_summary(domain, ...)     → terminal summary
DOMAIN_NAMES                          → dict mapping domain number → name
"""

from __future__ import annotations
import pandas as pd

# Louw-Nida top-level domain names (all 93)
DOMAIN_NAMES: dict[int, str] = {
    1:  'Geographical Objects and Features',
    2:  'Natural Substances',
    3:  'Plants',
    4:  'Animals',
    5:  'Foods and Condiments',
    6:  'Artifacts',
    7:  'Constructions',
    8:  'Body, Body Parts, Body Products',
    9:  'People',
    10: 'Kinship Terms',
    11: 'Groups and Classes of Persons',
    12: 'Supernatural Beings and Powers',
    13: 'Be, Become, Exist, Happen',
    14: 'Physical Events and States',
    15: 'Linear Movement',
    16: 'Non-Linear Movement',
    17: 'Stances and Events of Lying, Sitting, Standing',
    18: 'Attachment',
    19: 'Physical Impact',
    20: 'Violence, Harm, Destroy, Kill',
    21: 'Danger, Risk, Safe, Save',
    22: 'Trouble, Hardship, Relief, Favorable',
    23: 'Physiological Processes and States',
    24: 'Sensory Events and States',
    25: 'Attitudes and Emotions',
    26: 'Psychological Faculties',
    27: 'Learn',
    28: 'Know',
    29: 'Memory and Recall',
    30: 'Think',
    31: 'Hold a View, Believe, Trust',
    32: 'Understand',
    33: 'Communication',
    34: 'Association',
    35: 'Help, Care For',
    36: 'Guide, Discipline, Follow',
    37: 'Control, Rule',
    38: 'Punish, Reward',
    39: 'Reconciliation, Forgiveness',
    40: 'Reconciliation, Forgiveness',
    41: 'Moral and Ethical Qualities and Related Behavior',
    42: 'Perform, Do',
    43: 'Agriculture and Horticulture',
    44: 'Animal Husbandry, Fishing',
    45: 'Building, Constructing',
    46: 'Household Activities',
    47: 'Commercial Activities',
    48: 'Monetary',
    49: 'Physical Events Involving Liquids or Masses',
    50: 'HERE/THERE, MOVEMENT',
    51: 'Spacial Dimensions',
    52: 'Spacial Orientations',
    53: 'Religious Activities',
    54: 'Maritime Activities',
    55: 'Military Activities',
    56: 'Courts and Legal Procedures',
    57: 'Possess, Transfer, Exchange',
    58: 'Nature, Class, Example',
    59: 'Quantity',
    60: 'Number',
    61: 'Sequence',
    62: 'Arrange, Organize',
    63: 'Whole, Unite, Part, Divide',
    64: 'Comparison',
    65: 'Value',
    66: 'Proper, Improper',
    67: 'Time',
    68: 'Aspect',
    69: 'Affirmation, Negation',
    70: 'Real, Unreal',
    71: 'Mode',
    72: 'True, False',
    73: 'Genuine, Phony',
    74: 'Able, Capable',
    75: 'Adequate, Qualified',
    76: 'Cause',
    77: 'Change of State',
    78: 'Nature of an Event',
    79: 'Features of Objects',
    80: 'Weight',
    81: 'Measure',
    82: 'Location',
    83: 'Discourse Markers',
    84: 'Discourse Markers',
    85: 'Discourse Markers',
    86: 'Discourse Markers',
    87: 'Status',
    88: 'Moral and Ethical Qualities',
    89: 'Relations',
    90: 'Case',
    91: 'Discourse Connectives',
    92: 'Discourse Markers',
    93: 'Proper Names',
}

# Theological domain groupings — convenience sets
THEOLOGY_DOMAINS: dict[str, list[int]] = {
    'God / Supernatural':    [12],
    'Communication':         [33],
    'Moral / Ethics':        [41, 88],
    'Forgiveness':           [39, 40],
    'Punishment / Judgment': [38, 56],
    'Religious Activity':    [53],
    'Belief / Trust':        [31],
    'Salvation / Safety':    [21],
    'Death / Violence':      [20, 23],
    'Knowledge / Wisdom':    [27, 28, 32],
    'Kinship':               [10],
    'Time / Aspect':         [67, 68],
    'Cause / Effect':        [76, 77],
}


def _load_nt() -> pd.DataFrame:
    from ..core.syntax import load_syntax
    return load_syntax()


def _parse_domain_codes(raw: str) -> list[str]:
    """
    Parse a (possibly space-separated) domain string into individual codes.
    e.g. '010002 033003' → ['010002', '033003']
    e.g. '033006' → ['033006']
    """
    if not raw or pd.isna(raw):
        return []
    return [x.strip() for x in raw.split() if x.strip()]


def _domain_prefix(domain_number: int | str) -> str:
    """Return the 3-digit zero-padded prefix for a top-level domain number."""
    return f"{int(str(domain_number).split('.')[0]):03d}"


def query_domain(
    domain: int | str | list[int | str],
    *,
    book: str | list[str] | None = None,
    part_of_speech: str | None = None,
    subdomain: str | None = None,
    exact_ln: str | None = None,
    has_subjref: bool = False,
) -> pd.DataFrame:
    """
    Return all NT tokens belonging to the given Louw-Nida domain(s).

    Parameters
    ----------
    domain    : top-level domain number(s) e.g. 33, '33', [12, 33]
                or a domain name that will be matched against DOMAIN_NAMES
    book      : restrict to specific book(s)
    part_of_speech : filter by word class ('verb', 'noun', etc.)
    subdomain : 6-digit domain code to match exactly, e.g. '033006'
    exact_ln  : exact Louw-Nida reference, e.g. '33.69'
    has_subjref : if True, only return tokens that have a subjref link
    """
    df = _load_nt()

    # Resolve domain to list of 3-digit prefixes
    if isinstance(domain, (int, str)) and not isinstance(domain, list):
        domain = [domain]

    prefixes = set()
    for d in domain:
        d_str = str(d)
        if d_str.isdigit():
            prefixes.add(_domain_prefix(int(d_str)))
        else:
            # Try name match
            for num, name in DOMAIN_NAMES.items():
                if d_str.lower() in name.lower():
                    prefixes.add(_domain_prefix(num))
            # Also try as a raw prefix
            if len(d_str) >= 3:
                prefixes.add(d_str[:3].zfill(3))

    # Filter: any domain code starts with any of our prefixes
    def _matches(raw: str) -> bool:
        if not raw:
            return False
        for code in _parse_domain_codes(raw):
            if code[:3] in prefixes:
                return True
        return False

    mask = df['domain'].notna() & df['domain'].map(_matches)

    if subdomain:
        mask &= df['domain'].str.contains(subdomain, na=False)
    if exact_ln:
        mask &= df['ln'].notna() & df['ln'].str.contains(exact_ln, na=False)

    result = df[mask].copy()

    if book is not None:
        if isinstance(book, str):
            book = [book]
        result = result[result['book'].isin(book)]

    if part_of_speech:
        result = result[result['class_'].str.lower() == part_of_speech.lower()]

    if has_subjref:
        result = result[result['subjref'].notna()]

    return result.reset_index(drop=True)


def top_domain_words(
    domain: int | str | list[int | str],
    *,
    book: str | list[str] | None = None,
    part_of_speech: str | None = None,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    Most frequent lemmas in a given Louw-Nida domain.

    Returns a DataFrame with columns: lemma, strong_g, gloss, ln, count.
    """
    df = query_domain(domain, book=book, part_of_speech=part_of_speech)
    if df.empty:
        return pd.DataFrame()

    agg = (
        df.groupby(['lemma', 'strong_g', 'gloss', 'ln'], dropna=False)
        .size().reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(top_n)
    )
    return agg.reset_index(drop=True)


def domain_profile(
    book: str,
    *,
    top_n: int = 20,
    exclude_discourse: bool = True,
) -> pd.DataFrame:
    """
    Semantic domain profile for a single NT book — what percentage of its
    vocabulary falls in each top-level Louw-Nida domain?

    Parameters
    ----------
    book              : NT book_id (e.g. 'Rom', 'Rev')
    top_n             : return top N domains by token count
    exclude_discourse : if True, exclude domains 83–92 (discourse markers,
                        particles, pronouns) for a cleaner content-word profile
    """
    df = _load_nt()
    book_df = df[(df['book'] == book) & df['domain'].notna() & (df['domain'] != '')]

    rows = []
    for _, row in book_df.iterrows():
        for code in _parse_domain_codes(row['domain']):
            prefix = int(code[:3])
            if exclude_discourse and 83 <= prefix <= 92:
                continue
            rows.append({'domain_num': prefix, 'lemma': row['lemma']})

    if not rows:
        return pd.DataFrame()

    result_df = pd.DataFrame(rows)
    counts = result_df.groupby('domain_num').size().reset_index(name='count')
    counts['domain_name'] = counts['domain_num'].map(DOMAIN_NAMES)
    counts['pct'] = (counts['count'] / counts['count'].sum() * 100).round(1)
    return (
        counts.sort_values('count', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def domain_role_search(
    domain: int | str | list[int | str],
    subject_strongs: list[str] | str,
    corpus: str = 'NT',
    *,
    books: list[str] | None = None,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    Find tokens in the given Louw-Nida domain(s) where the grammatical
    subject is one of the given Strong's number(s).

    Combines domain filtering with syntactic role search — e.g.:
      "all Communication-domain verbs where God is the subject"
      "all Judgment-domain words where Jesus is the agent"

    Parameters
    ----------
    domain          : Louw-Nida domain number(s)
    subject_strongs : Strong's number(s) for the subject
    corpus          : 'NT' only (OT domain data uses different taxonomy)
    books           : restrict to specific books
    top_n           : return top N lemmas by count

    Returns a DataFrame with lemma, gloss, ln, count columns.
    """
    if isinstance(subject_strongs, str):
        subject_strongs = [subject_strongs]

    # Normalise NT strong numbers (plain int strings)
    targets = set()
    for s in subject_strongs:
        s = s.strip().upper().lstrip('G')
        try:
            targets.add(str(int(s)))
        except ValueError:
            targets.add(s)

    df = _load_nt()
    id_map = df.set_index('xml_id')['strong'].to_dict()

    # Get domain tokens
    domain_df = query_domain(domain, book=books)

    # Filter to those with matching subject
    matched = domain_df[
        domain_df['subjref'].notna() &
        domain_df['subjref'].map(lambda x: id_map.get(x, '') in targets)
    ]

    if matched.empty:
        return pd.DataFrame()

    agg = (
        matched.groupby(['lemma', 'strong_g', 'gloss', 'ln'], dropna=False)
        .size().reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(top_n)
    )
    return agg.reset_index(drop=True)


def domain_comparison(
    books: list[str],
    *,
    top_n: int = 15,
    exclude_discourse: bool = True,
) -> pd.DataFrame:
    """
    Compare domain profiles across multiple NT books.

    Returns a pivot table: rows=domain, cols=books, cells=% of book's tokens.
    """
    profiles = {}
    for book in books:
        p = domain_profile(book, top_n=100, exclude_discourse=exclude_discourse)
        if not p.empty:
            # Use "num: name" as index to avoid duplicate-name collisions
            p['label'] = p['domain_num'].astype(str) + ': ' + p['domain_name'].fillna('')
            profiles[book] = p.set_index('label')['pct']

    if not profiles:
        return pd.DataFrame()

    combined = pd.DataFrame(profiles).fillna(0).round(1)
    combined['_avg'] = combined.mean(axis=1)
    combined = combined.sort_values('_avg', ascending=False).drop(columns='_avg')
    return combined.head(top_n)


def print_domain_summary(
    domain: int | str | list[int | str],
    *,
    book: str | list[str] | None = None,
    top_n: int = 20,
    label: str | None = None,
) -> None:
    """Print a formatted table of the top words in a Louw-Nida domain."""
    # Resolve display name
    if isinstance(domain, list):
        nums = domain
    else:
        nums = [domain]
    domain_label = label
    if not domain_label:
        names = [DOMAIN_NAMES.get(int(str(n).split('.')[0]), str(n)) for n in nums]
        domain_label = ' / '.join(names)

    df = top_domain_words(domain, book=book, top_n=top_n)
    scope = f" ({', '.join(book) if isinstance(book, list) else book})" if book else ''

    w = 76
    print(f"\n{'═'*w}")
    print(f"  Louw-Nida Domain {nums[0] if len(nums) == 1 else nums}: {domain_label}{scope}")
    print(f"{'═'*w}")

    if df.empty:
        print("  No results found.")
        print()
        return

    print(f"  {'Lemma':<18} {'Gloss':<30} {'LN':<10} Count")
    print(f"  {'-'*17} {'-'*29} {'-'*9} -----")
    for _, row in df.iterrows():
        print(f"  {str(row['lemma']):<18} {str(row['gloss']):<30} "
              f"{str(row.get('ln', '')):<10} {row['count']:>5}")

    print(f"\n  Total tokens in domain: {df['count'].sum():,}")
    print()


def print_domain_role(
    domain: int | str | list[int | str],
    subject_strongs: list[str] | str,
    *,
    books: list[str] | None = None,
    top_n: int = 20,
    label: str | None = None,
    subject_label: str | None = None,
) -> None:
    """Print a formatted table: domain words with given entity as subject."""
    if isinstance(subject_strongs, str):
        subject_strongs = [subject_strongs]
    if isinstance(domain, list):
        nums = domain
    else:
        nums = [domain]

    domain_label = label or DOMAIN_NAMES.get(int(str(nums[0]).split('.')[0]), str(nums[0]))
    subj_label = subject_label or '/'.join(subject_strongs)
    scope = f" ({', '.join(books)})" if books else ''

    df = domain_role_search(domain, subject_strongs, books=books, top_n=top_n)
    w = 76
    print(f"\n{'═'*w}")
    print(f"  Domain {nums[0] if len(nums) == 1 else nums} ({domain_label}){scope}")
    print(f"  Subject: {subj_label}")
    print(f"{'═'*w}")

    if df.empty:
        print("  No results found.")
        print()
        return

    print(f"  {'Lemma':<18} {'Gloss':<32} {'LN':<10} Count")
    print(f"  {'-'*17} {'-'*31} {'-'*9} -----")
    for _, row in df.iterrows():
        print(f"  {str(row['lemma']):<18} {str(row['gloss']):<32} "
              f"{str(row.get('ln', '')):<10} {row['count']:>5}")
    print()
