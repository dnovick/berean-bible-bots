"""
Hebrew OT predicate-argument structure (semantic role labeling).

The MACULA Hebrew WLC dataset includes a `frame` column on verb tokens that
encodes semantic role structure — who does what to whom — using PropBank-style
argument labels:

  A0  — proto-agent (subject / initiator)
  A1  — proto-patient (object / affected entity)

Each argument value is one or more MACULA xml_id references pointing to the
actual token(s) that fill that role.

Format:  'A0:<xml_id>; A1:<xml_id1>;<xml_id2>;'
Example: 'A0:010010010031; A1:010010010052;010010010072;'
         → A0 = אֱלֹהִים (Gen 1:1), A1 = שָׁמַיִם + אֶרֶץ

Coverage: ~68,207 Hebrew verb tokens have frame data (out of ~475,911 total).
          ~27,395 have an A1 (patient) argument; ~40,812 have A0 only.

Questions this answers
──────────────────────
  • What does God (A0) do as agent in the Torah?
  • What gets created/destroyed/given (A1) across the OT?
  • Which verbs does YHWH appear as agent most often?
  • Which verbs take Israel/the people as patient most often?
  • What does the agent of a given verb profile look like?

Public API
──────────
ot_frame_data(book=None, lang='H')             → DataFrame (verb tokens with frame)
ot_agent_verbs(agent_lemma, top_n=20, ...)     → DataFrame (what agent does as A0)
ot_patient_verbs(patient_lemma, top_n=20, ...) → DataFrame (what acts on patient as A1)
ot_verb_agents(verb_lemma, top_n=20, ...)      → DataFrame (who is A0 of this verb)
ot_verb_patients(verb_lemma, top_n=20, ...)    → DataFrame (who is A1 of this verb)
ot_frame_pairs(book=None, top_n=20)            → DataFrame (most common A0,verb,A1 triples)

print_ot_agent_verbs(agent_lemma, ...)         → None
print_ot_patient_verbs(patient_lemma, ...)     → None
print_ot_verb_agents(verb_lemma, ...)          → None
print_ot_verb_patients(verb_lemma, ...)        → None
print_ot_frame_pairs(book=None, top_n=20)      → None

ot_agent_verbs_chart(agent_lemma, ...)         → Path | None
ot_patient_verbs_chart(patient_lemma, ...)     → Path | None
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd

from ..core._utils import load_ot_data

_CHART_DIR = Path('output') / 'charts' / 'ot' / 'predicate_args'


# ── helpers ───────────────────────────────────────────────────────────────────

def _parse_frame(frame_str: str) -> dict[str, list[str]]:
    """
    Parse 'A0:id1; A1:id2;id3;' → {'A0': ['id1'], 'A1': ['id2', 'id3']}.
    """
    result: dict[str, list[str]] = {}
    if not frame_str or not isinstance(frame_str, str):
        return result
    for part in frame_str.split(';'):
        part = part.strip()
        if ':' in part:
            role, refs = part.split(':', 1)
            role = role.strip()
            ids = [r.strip() for r in refs.split() if r.strip()]
            if ids:
                result[role] = result.get(role, []) + ids
    return result


def _normalise_xml_id(xml_id: str) -> str:
    """Strip leading 'o' prefix used in some MACULA xml_ids."""
    return xml_id.lstrip('o')


def _build_id_maps(df: pd.DataFrame) -> tuple[dict, dict]:
    """Build xml_id → lemma and xml_id → gloss lookup dicts."""
    id_to_lemma: dict[str, str] = {}
    id_to_gloss: dict[str, str] = {}
    for row in df[['xml_id', 'lemma', 'gloss']].itertuples(index=False):
        raw = _normalise_xml_id(str(row.xml_id))
        id_to_lemma[raw] = row.lemma
        id_to_gloss[raw] = row.gloss
    return id_to_lemma, id_to_gloss


# ── data access ───────────────────────────────────────────────────────────────

def ot_frame_data(
    book: str | list[str] | None = None,
    *,
    lang: str = 'H',
) -> pd.DataFrame:
    """
    All Hebrew verb tokens that have frame (A0/A1) data.

    Returns the original DataFrame rows plus resolved columns:
      a0_lemma, a0_gloss, a1_lemma, a1_gloss
    (using the first listed A0/A1 reference; semicolon-separated multiples
    are stored in a0_refs/a1_refs as raw lists).
    """
    df = load_ot_data()
    if lang:
        df = df[df['lang'] == lang]
    if book is not None:
        if isinstance(book, str):
            book = [book]
        df = df[df['book'].isin(book)]

    has_frame = df[df['frame'].notna() & (df['frame'] != '')].copy()
    if has_frame.empty:
        return has_frame

    id_to_lemma, id_to_gloss = _build_id_maps(df)

    a0_lemmas, a0_glosses, a1_lemmas, a1_glosses = [], [], [], []
    for frame_str in has_frame['frame']:
        parsed = _parse_frame(frame_str)
        a0_refs = parsed.get('A0', [])
        a1_refs = parsed.get('A1', [])
        a0_lemmas.append(id_to_lemma.get(a0_refs[0], '') if a0_refs else '')
        a0_glosses.append(id_to_gloss.get(a0_refs[0], '') if a0_refs else '')
        a1_lemmas.append(id_to_lemma.get(a1_refs[0], '') if a1_refs else '')
        a1_glosses.append(id_to_gloss.get(a1_refs[0], '') if a1_refs else '')

    has_frame = has_frame.copy()
    has_frame['a0_lemma'] = a0_lemmas
    has_frame['a0_gloss'] = a0_glosses
    has_frame['a1_lemma'] = a1_lemmas
    has_frame['a1_gloss'] = a1_glosses
    return has_frame.reset_index(drop=True)


def ot_agent_verbs(
    agent_lemma: str,
    *,
    top_n: int = 20,
    book: str | list[str] | None = None,
    lang: str = 'H',
) -> pd.DataFrame:
    """
    Verbs where the given lemma is the A0 (proto-agent / subject).

    Returns: lemma (verb), gloss, count.
    """
    df = ot_frame_data(book=book, lang=lang)
    subset = df[df['a0_lemma'] == agent_lemma]
    if subset.empty:
        return pd.DataFrame(columns=['lemma', 'gloss', 'count'])
    result = (
        subset.groupby(['lemma', 'gloss'])
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    return result


def ot_patient_verbs(
    patient_lemma: str,
    *,
    top_n: int = 20,
    book: str | list[str] | None = None,
    lang: str = 'H',
) -> pd.DataFrame:
    """
    Verbs where the given lemma is the A1 (proto-patient / object).

    Returns: lemma (verb), gloss, count.
    """
    df = ot_frame_data(book=book, lang=lang)
    subset = df[df['a1_lemma'] == patient_lemma]
    if subset.empty:
        return pd.DataFrame(columns=['lemma', 'gloss', 'count'])
    result = (
        subset.groupby(['lemma', 'gloss'])
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    return result


def ot_verb_agents(
    verb_lemma: str,
    *,
    top_n: int = 20,
    book: str | list[str] | None = None,
    lang: str = 'H',
) -> pd.DataFrame:
    """
    Who (A0) typically performs the given verb?

    Returns: a0_lemma, a0_gloss, count.
    """
    df = ot_frame_data(book=book, lang=lang)
    subset = df[(df['lemma'] == verb_lemma) & (df['a0_lemma'] != '')]
    if subset.empty:
        return pd.DataFrame(columns=['a0_lemma', 'a0_gloss', 'count'])
    result = (
        subset.groupby(['a0_lemma', 'a0_gloss'])
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    return result


def ot_verb_patients(
    verb_lemma: str,
    *,
    top_n: int = 20,
    book: str | list[str] | None = None,
    lang: str = 'H',
) -> pd.DataFrame:
    """
    What (A1) typically receives the given verb?

    Returns: a1_lemma, a1_gloss, count.
    """
    df = ot_frame_data(book=book, lang=lang)
    subset = df[(df['lemma'] == verb_lemma) & (df['a1_lemma'] != '')]
    if subset.empty:
        return pd.DataFrame(columns=['a1_lemma', 'a1_gloss', 'count'])
    result = (
        subset.groupby(['a1_lemma', 'a1_gloss'])
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    return result


def ot_frame_pairs(
    book: str | list[str] | None = None,
    *,
    top_n: int = 20,
    lang: str = 'H',
    require_a1: bool = True,
) -> pd.DataFrame:
    """
    Most common (A0, verb, A1) triples across the OT.

    Parameters
    ----------
    require_a1 : if True (default), only include rows where A1 is present.
    """
    df = ot_frame_data(book=book, lang=lang)
    if require_a1:
        df = df[df['a1_lemma'] != '']
    df = df[df['a0_lemma'] != '']

    if df.empty:
        return pd.DataFrame(columns=['a0_lemma', 'verb', 'a1_lemma', 'count'])

    result = (
        df.groupby(['a0_lemma', 'lemma', 'a1_lemma'])
        .size()
        .reset_index(name='count')
        .rename(columns={'lemma': 'verb'})
        .sort_values('count', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    return result


# ── print functions ───────────────────────────────────────────────────────────

def print_ot_frame_overview() -> None:
    df = load_ot_data()
    df_h = df[df['lang'] == 'H']
    has_frame = df_h[df_h['frame'].notna() & (df_h['frame'] != '')]
    has_a1 = has_frame[has_frame['frame'].str.contains('A1:', na=False)]
    w = 58
    print(f"\n{'═'*w}")
    print("  Hebrew OT Predicate-Argument Structure (Frame Data)")
    print(f"{'═'*w}")
    print(f"  Total Hebrew tokens   : {len(df_h):>9,}")
    print(f"  Verb tokens with frame: {len(has_frame):>9,} ({len(has_frame)/len(df_h)*100:.1f}%)")
    print(f"  Tokens with A1 patient: {len(has_a1):>9,} ({len(has_a1)/len(df_h)*100:.1f}%)")
    print(f"  Agent-only (A0 only)  : {len(has_frame)-len(has_a1):>9,}")
    print()


def print_ot_agent_verbs(
    agent_lemma: str,
    *,
    top_n: int = 20,
    book: str | list[str] | None = None,
    lang: str = 'H',
) -> None:
    scope = f" ({book})" if book else ""
    df = ot_agent_verbs(agent_lemma, top_n=top_n, book=book, lang=lang)
    w = 60
    print(f"\n{'═'*w}")
    print(f"  What {agent_lemma} does (A0 / agent){scope}")
    print(f"{'═'*w}")
    if df.empty:
        print("  No results found.")
        print()
        return
    print(f"  {'Verb':<14} {'Gloss':<28} {'Count':>6}")
    print(f"  {'-'*13} {'-'*27} {'-'*6}")
    for _, row in df.iterrows():
        print(f"  {str(row['lemma']):<14} {str(row['gloss']):<28} {row['count']:>6,}")
    print()


def print_ot_patient_verbs(
    patient_lemma: str,
    *,
    top_n: int = 20,
    book: str | list[str] | None = None,
    lang: str = 'H',
) -> None:
    scope = f" ({book})" if book else ""
    df = ot_patient_verbs(patient_lemma, top_n=top_n, book=book, lang=lang)
    w = 60
    print(f"\n{'═'*w}")
    print(f"  What acts on {patient_lemma} (A1 / patient){scope}")
    print(f"{'═'*w}")
    if df.empty:
        print("  No results found.")
        print()
        return
    print(f"  {'Verb':<14} {'Gloss':<28} {'Count':>6}")
    print(f"  {'-'*13} {'-'*27} {'-'*6}")
    for _, row in df.iterrows():
        print(f"  {str(row['lemma']):<14} {str(row['gloss']):<28} {row['count']:>6,}")
    print()


def print_ot_verb_agents(
    verb_lemma: str,
    *,
    top_n: int = 20,
    book: str | list[str] | None = None,
    lang: str = 'H',
) -> None:
    scope = f" ({book})" if book else ""
    df = ot_verb_agents(verb_lemma, top_n=top_n, book=book, lang=lang)
    w = 62
    print(f"\n{'═'*w}")
    print(f"  Who does {verb_lemma} (A0 agents){scope}")
    print(f"{'═'*w}")
    if df.empty:
        print("  No results found.")
        print()
        return
    print(f"  {'Agent':<16} {'Gloss':<26} {'Count':>6}")
    print(f"  {'-'*15} {'-'*25} {'-'*6}")
    for _, row in df.iterrows():
        print(f"  {str(row['a0_lemma']):<16} {str(row['a0_gloss']):<26} {row['count']:>6,}")
    print()


def print_ot_verb_patients(
    verb_lemma: str,
    *,
    top_n: int = 20,
    book: str | list[str] | None = None,
    lang: str = 'H',
) -> None:
    scope = f" ({book})" if book else ""
    df = ot_verb_patients(verb_lemma, top_n=top_n, book=book, lang=lang)
    w = 62
    print(f"\n{'═'*w}")
    print(f"  What {verb_lemma} acts on (A1 patients){scope}")
    print(f"{'═'*w}")
    if df.empty:
        print("  No results found.")
        print()
        return
    print(f"  {'Patient':<16} {'Gloss':<26} {'Count':>6}")
    print(f"  {'-'*15} {'-'*25} {'-'*6}")
    for _, row in df.iterrows():
        print(f"  {str(row['a1_lemma']):<16} {str(row['a1_gloss']):<26} {row['count']:>6,}")
    print()


def print_ot_frame_pairs(
    book: str | list[str] | None = None,
    *,
    top_n: int = 20,
    lang: str = 'H',
) -> None:
    scope = f" ({book})" if book else " (all OT)"
    df = ot_frame_pairs(book=book, top_n=top_n, lang=lang)
    w = 64
    print(f"\n{'═'*w}")
    print(f"  Most Common Agent–Verb–Patient Triples{scope}")
    print(f"{'═'*w}")
    if df.empty:
        print("  No results found.")
        print()
        return
    print(f"  {'Agent':<14} {'Verb':<12} {'Patient':<14} {'Count':>6}")
    print(f"  {'-'*13} {'-'*11} {'-'*13} {'-'*6}")
    for _, row in df.iterrows():
        print(f"  {str(row['a0_lemma']):<14} {str(row['verb']):<12} "
              f"{str(row['a1_lemma']):<14} {row['count']:>6,}")
    print()


# ── chart functions ───────────────────────────────────────────────────────────

def ot_agent_verbs_chart(
    agent_lemma: str,
    *,
    top_n: int = 15,
    book: str | list[str] | None = None,
    lang: str = 'H',
) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = ot_agent_verbs(agent_lemma, top_n=top_n, book=book, lang=lang)
    if df.empty:
        return None

    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    safe = agent_lemma.encode('ascii', 'ignore').decode() or 'agent'
    out = _CHART_DIR / f"agent_{safe}_verbs.png"

    labels = [f"{row['lemma']} ({row['gloss'][:18]})" for _, row in df.iterrows()]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(labels[::-1], df['count'][::-1], color='steelblue')
    scope = f" ({book})" if book else ""
    ax.set_xlabel('Count')
    ax.set_title(f'What {agent_lemma} does (A0 agent){scope}')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def ot_patient_verbs_chart(
    patient_lemma: str,
    *,
    top_n: int = 15,
    book: str | list[str] | None = None,
    lang: str = 'H',
) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    df = ot_patient_verbs(patient_lemma, top_n=top_n, book=book, lang=lang)
    if df.empty:
        return None

    _CHART_DIR.mkdir(parents=True, exist_ok=True)
    safe = patient_lemma.encode('ascii', 'ignore').decode() or 'patient'
    out = _CHART_DIR / f"patient_{safe}_verbs.png"

    labels = [f"{row['lemma']} ({row['gloss'][:18]})" for _, row in df.iterrows()]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(labels[::-1], df['count'][::-1], color='darkorange')
    scope = f" ({book})" if book else ""
    ax.set_xlabel('Count')
    ax.set_title(f'What acts on {patient_lemma} (A1 patient){scope}')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out
