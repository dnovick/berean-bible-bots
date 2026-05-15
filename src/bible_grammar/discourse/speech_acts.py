"""
Speech act classification for biblical direct discourse (OT Hebrew + NT Greek).

Applies a rule-based classifier based on Searle (1969) speech act taxonomy
to verses with direct speech, using morphological and lexical cues.

Speech act types
────────────────
  ASSERTIVE    — claims a state of affairs (predicate nominals, "I am YHWH")
  DIRECTIVE    — commands/requests (imperatives, negated yiqtol/jussive)
  COMMISSIVE   — commits speaker to future action (1st-person yiqtol + promise)
  EXPRESSIVE   — praise, lament, thanksgiving (interjections, doxological lemmas)
  DECLARATIVE  — changes reality by utterance (blessing, curse, naming, forgiveness)
  MIXED        — verse with multiple dominant types (most common in short verses)

Classification is probabilistic: the type with the highest cue score wins.
When no cue fires, the verse is classified 'unclassified'.

Notes
─────
  This is a lexical/morphological approximation. Full illocutionary analysis
  requires pragmatic context. Edge cases (rhetorical questions as directives,
  indirect speech) are not handled.

Questions this answers
──────────────────────
  • What speech act types dominate YHWH's speech in Isaiah vs. Jeremiah?
  • How does Jesus's directive frequency compare between Matthew and John?
  • Which Pauline letters have the most commissive (promise) content?
  • Are Deuteronomy's laws primarily directives or also declaratives?

Public API
──────────
SPEECH_ACT_TYPES                              → list of type labels
OT_SPEECH_CUE_WEIGHTS                         → dict of cue definitions (OT)
NT_SPEECH_CUE_WEIGHTS                         → dict of cue definitions (NT)

ot_speech_act_data(book, speaker)             → DataFrame (verses with type)
ot_speech_act_profile(speaker, book)          → DataFrame (type, count, pct)
nt_speech_act_data(book)                      → DataFrame
nt_speech_act_profile(book)                   → DataFrame

print_ot_speech_act_profile(speaker, book)    → None
print_nt_speech_act_profile(book)             → None
print_speech_act_comparison(speakers, lang)   → None

speech_act_chart(speaker_or_book, lang)       → Path | None
speech_act_heatmap(speakers, lang)            → Path | None
"""

from __future__ import annotations
from collections import Counter
from pathlib import Path

import pandas as pd

from ..core._utils import ensure_chart_dir

_CHART_DIR = Path('output') / 'charts' / 'speech_acts'

SPEECH_ACT_TYPES = ['assertive', 'directive', 'commissive', 'expressive', 'declarative']
_UNCLASSIFIED = 'unclassified'

# ── classifier cue sets ───────────────────────────────────────────────────────

# Hebrew cues: (column, operator, values/types, weight, speech_act_type)
_OT_DIRECTIVE_VERB_TYPES = {
    'imperative', 'cohortative', 'jussive',
    'infinitive absolute',  # imperatival inf. abs.
}
_OT_DIRECTIVE_LEMMAS = {'לֹא', 'אַל'}  # prohibition + jussive/imperfect
_OT_ASSERTIVE_LEMMAS = {'אֲנִי', 'אָנֹכִי', 'יְהוָה', 'אֱלֹהִים'}  # "I am YHWH" etc.
_OT_COMMISSIVE_MARKERS = {'שָׁבַע', 'נָדַר', 'כִּי'}  # oath, vow, כִּי-promise
_OT_EXPRESSIVE_LEMMAS = {
    'הָלַל', 'יָדָה', 'שִׁיר', 'רָנַן', 'הַלְלוּיָהּ',
    'אוֹי', 'הוֹי', 'אֲהָהּ', 'בָּכָה', 'קִינָה', 'אֵיכָה',
}
_OT_DECLARATIVE_LEMMAS = {
    'בָּרַךְ', 'אָרַר', 'קָרָא', 'שָׁלַח', 'סָלַח', 'מָחַל',
    'חָרַם', 'שׁוּב', 'נָשָׂא',  # forgiveness
}

# Greek cues
_NT_DIRECTIVE_MOODS = {'imperative'}
_NT_DIRECTIVE_PARTICLES = {'μή', 'οὐ', 'οὐχ', 'οὐκ'}  # prohibition with imp./subj.
_NT_ASSERTIVE_LEMMAS = {'ἐγώ', 'εἰμί'}  # ἐγώ εἰμι assertives
_NT_COMMISSIVE_LEMMAS = {'ὀμνύω', 'ἐπαγγέλλω', 'δίδωμι', 'ποιέω'}  # promise/commit
_NT_EXPRESSIVE_LEMMAS = {
    'δοξάζω', 'αἰνέω', 'εὐλογέω', 'εὐχαριστέω',
    'θρηνέω', 'κλαίω', 'πενθέω', 'ἀλαλάζω', 'ὠδή',
}
_NT_DECLARATIVE_LEMMAS = {
    'ἀφίημι', 'εὐλογέω', 'καταράομαι', 'ἐπικαλέω',
    'ὀνομάζω', 'καλέω',  # naming
}


def _score_ot(verse_df: pd.DataFrame) -> str:
    """Classify an OT verse's speech act type from its tokens."""
    scores: Counter = Counter()
    types = set(verse_df['type_'].dropna())
    lemmas = set(verse_df['lemma'].dropna())

    if types & _OT_DIRECTIVE_VERB_TYPES:
        scores['directive'] += 3
    if lemmas & _OT_DIRECTIVE_LEMMAS:
        scores['directive'] += 2

    if lemmas & _OT_ASSERTIVE_LEMMAS:
        scores['assertive'] += 2

    if lemmas & _OT_COMMISSIVE_MARKERS:
        scores['commissive'] += 2

    if lemmas & _OT_EXPRESSIVE_LEMMAS:
        scores['expressive'] += 3

    if lemmas & _OT_DECLARATIVE_LEMMAS:
        scores['declarative'] += 3

    if not scores:
        return _UNCLASSIFIED
    return scores.most_common(1)[0][0]


def _score_nt(verse_df: pd.DataFrame) -> str:
    """Classify a NT verse's speech act type from its tokens."""
    scores: Counter = Counter()
    moods = set(verse_df['mood'].dropna()) if 'mood' in verse_df.columns else set()
    lemmas = set(verse_df['lemma'].dropna())

    if moods & _NT_DIRECTIVE_MOODS:
        scores['directive'] += 3
    if lemmas & _NT_DIRECTIVE_PARTICLES:
        scores['directive'] += 1

    if lemmas & _NT_ASSERTIVE_LEMMAS:
        scores['assertive'] += 2

    if lemmas & _NT_COMMISSIVE_LEMMAS:
        scores['commissive'] += 2

    if lemmas & _NT_EXPRESSIVE_LEMMAS:
        scores['expressive'] += 3

    if lemmas & _NT_DECLARATIVE_LEMMAS:
        scores['declarative'] += 3

    if not scores:
        return _UNCLASSIFIED
    return scores.most_common(1)[0][0]


# ── helpers ───────────────────────────────────────────────────────────────────

def _load_ot_h() -> pd.DataFrame:
    from ..core._utils import load_ot_h
    return load_ot_h()


def _load_nt() -> pd.DataFrame:
    from ..core._utils import load_nt
    return load_nt()


# ── data functions ────────────────────────────────────────────────────────────

def ot_speech_act_data(
    book: str | None = None,
    *,
    speaker: str | None = None,
) -> pd.DataFrame:
    """
    OT verses classified by speech act type.

    Optionally filter by book and/or by speaker lemma
    (e.g., speaker='יְהוָה' for YHWH's speech).

    Returns: ref, book, chapter, verse, speech_act_type — one row per verse.
    """
    df = _load_ot_h()
    if book is not None:
        df = df[df['book'] == book]
    if speaker is not None:
        # Keep only verses where the speaker lemma appears
        verse_keys = set(zip(
            df[df['lemma'] == speaker]['book'],
            df[df['lemma'] == speaker]['chapter'],
            df[df['lemma'] == speaker]['verse'],
        ))
        if verse_keys:
            df = df[df.apply(
                lambda r: (r['book'], r['chapter'], r['verse']) in verse_keys, axis=1
            )]

    rows = []
    for (bk, ch, vs), grp in df.groupby(['book', 'chapter', 'verse'], sort=False):
        ref = grp['ref'].iloc[0] if 'ref' in grp.columns else f'{bk} {ch}:{vs}'
        act = _score_ot(grp)
        rows.append({'ref': ref, 'book': bk, 'chapter': int(ch), 'verse': int(vs),
                     'speech_act_type': act})
    if not rows:
        return pd.DataFrame(columns=['ref', 'book', 'chapter', 'verse', 'speech_act_type'])
    return pd.DataFrame(rows).reset_index(drop=True)


def ot_speech_act_profile(
    speaker: str | None = None,
    *,
    book: str | None = None,
) -> pd.DataFrame:
    """
    Distribution of speech act types for an OT book/speaker.

    Returns: speech_act_type, count, pct.
    """
    data = ot_speech_act_data(book=book, speaker=speaker)
    if data.empty:
        return pd.DataFrame(columns=['speech_act_type', 'count', 'pct'])
    total = len(data)
    counts = data['speech_act_type'].value_counts().reset_index()
    counts.columns = ['speech_act_type', 'count']
    counts['pct'] = (counts['count'] / total * 100).round(1)
    return counts.reset_index(drop=True)


def nt_speech_act_data(
    book: str | None = None,
) -> pd.DataFrame:
    """
    NT verses classified by speech act type.

    Returns: ref, book, chapter, verse, speech_act_type.
    """
    df = _load_nt()
    if book is not None:
        df = df[df['book'] == book]

    rows = []
    for (bk, ch, vs), grp in df.groupby(['book', 'chapter', 'verse'], sort=False):
        ref = grp['ref'].iloc[0] if 'ref' in grp.columns else f'{bk} {ch}:{vs}'
        act = _score_nt(grp)
        rows.append({'ref': ref, 'book': bk, 'chapter': int(ch), 'verse': int(vs),
                     'speech_act_type': act})
    if not rows:
        return pd.DataFrame(columns=['ref', 'book', 'chapter', 'verse', 'speech_act_type'])
    return pd.DataFrame(rows).reset_index(drop=True)


def nt_speech_act_profile(
    book: str | None = None,
) -> pd.DataFrame:
    """Distribution of speech act types for an NT book."""
    data = nt_speech_act_data(book=book)
    if data.empty:
        return pd.DataFrame(columns=['speech_act_type', 'count', 'pct'])
    total = len(data)
    counts = data['speech_act_type'].value_counts().reset_index()
    counts.columns = ['speech_act_type', 'count']
    counts['pct'] = (counts['count'] / total * 100).round(1)
    return counts.reset_index(drop=True)


def ot_speech_act_comparison(
    books: list[str],
    *,
    speaker: str | None = None,
) -> pd.DataFrame:
    """
    Side-by-side speech act type profiles for a list of OT books.

    Returns a pivot: rows=speech_act_type, cols=books, cells=% of book's verses.
    """
    profiles: dict[str, pd.Series] = {}
    for book in books:
        df = ot_speech_act_profile(speaker=speaker, book=book)
        if not df.empty:
            profiles[book] = df.set_index('speech_act_type')['pct']
    if not profiles:
        return pd.DataFrame()
    combined = pd.DataFrame(profiles).fillna(0).round(1)
    order = SPEECH_ACT_TYPES + [_UNCLASSIFIED]
    combined = combined.reindex([t for t in order if t in combined.index])
    return combined


def nt_speech_act_comparison(
    books: list[str],
) -> pd.DataFrame:
    """Side-by-side speech act profiles for a list of NT books."""
    profiles: dict[str, pd.Series] = {}
    for book in books:
        df = nt_speech_act_profile(book=book)
        if not df.empty:
            profiles[book] = df.set_index('speech_act_type')['pct']
    if not profiles:
        return pd.DataFrame()
    combined = pd.DataFrame(profiles).fillna(0).round(1)
    order = SPEECH_ACT_TYPES + [_UNCLASSIFIED]
    combined = combined.reindex([t for t in order if t in combined.index])
    return combined


# ── print functions ───────────────────────────────────────────────────────────

def print_ot_speech_act_profile(
    speaker: str | None = None,
    *,
    book: str | None = None,
) -> None:
    scope_parts = []
    if speaker:
        scope_parts.append(f"speaker={speaker}")
    if book:
        scope_parts.append(f"book={book}")
    scope = ' (' + ', '.join(scope_parts) + ')' if scope_parts else ''
    df = ot_speech_act_profile(speaker=speaker, book=book)
    w = 56
    print(f"\n{'═'*w}")
    print(f"  OT Speech Act Profile{scope}")
    print(f"{'═'*w}")
    if df.empty:
        print("  No data.")
        print()
        return
    print(f"  {'Type':<14} {'Count':>7} {'%':>6}  Bar")
    print('  ' + '-' * 50)
    for _, row in df.iterrows():
        bar = '█' * min(int(row['pct'] / 2), 30)
        print(f"  {row['speech_act_type']:<14} {row['count']:>7,} {row['pct']:>5.1f}%  {bar}")
    print()


def print_nt_speech_act_profile(
    book: str | None = None,
) -> None:
    scope = f" ({book})" if book else " (full NT)"
    df = nt_speech_act_profile(book=book)
    w = 56
    print(f"\n{'═'*w}")
    print(f"  NT Speech Act Profile{scope}")
    print(f"{'═'*w}")
    if df.empty:
        print("  No data.")
        print()
        return
    print(f"  {'Type':<14} {'Count':>7} {'%':>6}  Bar")
    print('  ' + '-' * 50)
    for _, row in df.iterrows():
        bar = '█' * min(int(row['pct'] / 2), 30)
        print(f"  {row['speech_act_type']:<14} {row['count']:>7,} {row['pct']:>5.1f}%  {bar}")
    print()


def print_speech_act_comparison(
    books: list[str],
    *,
    lang: str = 'H',
    speaker: str | None = None,
) -> None:
    if lang == 'H':
        df = ot_speech_act_comparison(books, speaker=speaker)
    else:
        df = nt_speech_act_comparison(books)
    if df.empty:
        print("No data.")
        return
    lang_label = 'Hebrew' if lang == 'H' else 'Greek'
    print(f"\nSpeech Act Comparison ({lang_label})")
    print(f"  {'Type':<14}" + ''.join(f"  {b:>7}" for b in df.columns))
    print('  ' + '-' * (14 + 9 * len(df.columns)))
    for act_type, row in df.iterrows():
        line = f"  {str(act_type):<14}"
        for val in row:
            line += f"  {val:>6.1f}%"
        print(line)
    print()


# ── chart functions ───────────────────────────────────────────────────────────

_TYPE_COLORS = {
    'assertive':   '#4e79a7',
    'directive':   '#f28e2b',
    'commissive':  '#59a14f',
    'expressive':  '#b07aa1',
    'declarative': '#e15759',
    'unclassified': '#bab0ac',
}


def speech_act_chart(
    books: list[str],
    *,
    lang: str = 'H',
    speaker: str | None = None,
) -> Path | None:
    """Stacked bar chart of speech act type percentages per book."""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        return None

    if lang == 'H':
        pivot = ot_speech_act_comparison(books, speaker=speaker)
    else:
        pivot = nt_speech_act_comparison(books)
    if pivot.empty:
        return None

    ensure_chart_dir(_CHART_DIR)
    safe_spk = f'_{speaker}' if speaker else ''
    out = _CHART_DIR / f'speech_acts_{"_".join(books[:5])}{safe_spk}_{lang}.png'

    lang_label = 'Hebrew' if lang == 'H' else 'Greek'
    x = np.arange(len(pivot.columns))
    bottom = np.zeros(len(pivot.columns))

    fig, ax = plt.subplots(figsize=(max(8, len(books) * 0.8), 5))
    for act_type in pivot.index:
        vals = pivot.loc[act_type].fillna(0).values.astype(float)
        color = _TYPE_COLORS.get(str(act_type), 'grey')
        ax.bar(x, vals, bottom=bottom, label=str(act_type), color=color)
        bottom += vals

    ax.set_xticks(x)
    ax.set_xticklabels(pivot.columns, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('% of classified verses')
    spk_label = f' ({speaker})' if speaker else ''
    ax.set_title(f'Speech Act Types — {lang_label}{spk_label}')
    ax.legend(loc='upper right', fontsize=8, bbox_to_anchor=(1.15, 1))
    plt.tight_layout()
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    return out


def speech_act_heatmap(
    books: list[str],
    *,
    lang: str = 'H',
    speaker: str | None = None,
) -> Path | None:
    """Heatmap of speech act percentages: rows=type, cols=books."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    if lang == 'H':
        pivot = ot_speech_act_comparison(books, speaker=speaker)
    else:
        pivot = nt_speech_act_comparison(books)
    if pivot.empty:
        return None

    ensure_chart_dir(_CHART_DIR)
    safe_spk = f'_{speaker}' if speaker else ''
    out = _CHART_DIR / f'speech_act_heatmap_{"_".join(books[:6])}{safe_spk}_{lang}.png'

    lang_label = 'Hebrew' if lang == 'H' else 'Greek'
    fig, ax = plt.subplots(figsize=(max(8, len(books) * 0.8), max(4, len(pivot) * 0.7)))
    im = ax.imshow(pivot.values.astype(float), aspect='auto', cmap='YlOrRd', vmin=0)
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, rotation=45, ha='right', fontsize=9)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=9)
    plt.colorbar(im, ax=ax, label='% of classified verses')
    spk_label = f' ({speaker})' if speaker else ''
    ax.set_title(f'Speech Act Heatmap — {lang_label}{spk_label}')
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out
