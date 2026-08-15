"""
Verse accentuation diagrams — hierarchical structure of Masoretic cantillation.

Implements Price's prose accent hierarchy from:
  J.D. Price, "The Syntax of Masoretic Accents in the Hebrew Bible"
  Temple Baptist Seminary, 2nd ed., 1990/2010.

Price's Law of Continuous Dichotomy: each disjunctive accent governs a domain
that splits into a near segment (words immediately preceding the governor) and
a remote segment (words farther preceding it), recursively.  The rightmost
sub-disjunctive in a domain is its "near" sub-governor; everything to its left
forms the sub-governor's own domain.

Hierarchy levels (prose):
  H1  Soph Pasuq  — verse terminator
  H2  Silluq, Athnach  — primary verse dividers
  H3  Tiphcha, Little/Great Zaqeph, Segolta, Shalsheleth
  H4  Tebir, Pashta/Yethib, Zarqa, Rebia
  H5  Geresh, Garshaim, Pazer/Great Telisha/Great Pazer, Legarmeh

Key Unicode notes (both names are INVERTED in the Unicode standard):
  U+05AE  named "ZINOR"   → actually prose Zarqa  (H4 disjunctive)
  U+0598  named "ZARQA"   → actually Tsinnorit    (used only in poetic books)
  U+05BD  named "METEG"   → functions as Silluq when on the last word of a verse
  U+05A3+U+05C0 (Munach+Paseq on same word) → Legarmeh (H5 disjunctive)

Public API
──────────
parse_verse(book, chapter, verse) → AccentNode
render_verse(book, chapter, verse, output_path, style='bracket') → Path
PROSE_BOOKS  — set of prose OT book IDs
POETRY_BOOKS — set of poetic OT book IDs (use poetry.py for these)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


# ── Book classification ────────────────────────────────────────────────────────

POETRY_BOOKS: set[str] = {'Psa', 'Pro', 'Job'}

PROSE_BOOKS: set[str] = {
    'Gen', 'Exo', 'Lev', 'Num', 'Deu',
    'Jos', 'Jdg', 'Rut', '1Sa', '2Sa', '1Ki', '2Ki',
    '1Ch', '2Ch', 'Ezr', 'Neh', 'Est',
    'Isa', 'Jer', 'Lam', 'Eze', 'Dan',
    'Hos', 'Joe', 'Amo', 'Oba', 'Jon', 'Mic',
    'Nah', 'Hab', 'Zep', 'Hag', 'Zec', 'Mal',
    'Sng', 'Ecc',
}

# ── Unicode codepoint table ────────────────────────────────────────────────────

_CP: dict[str, Optional[int]] = {
    # ── Verse terminator ──────────────────────────────────────────────────────
    'SOP':   0x05C3,   # Soph Pasuq (punctuation, not a musical accent)

    # ── H2 disjunctives ──────────────────────────────────────────────────────
    'SIL':   0x05BD,   # Silluq — disambiguated: Meteg (U+05BD) on last word before SOP
    'ATH':   0x0591,   # Athnach (Unicode: "ETNAHTA")

    # ── H3 disjunctives ──────────────────────────────────────────────────────
    'TIP':   0x0596,   # Tiphcha (Unicode: "TIPEHA")
    'ZAQ':   0x0594,   # Little Zaqeph (Unicode: "ZAQEF QATAN")
    'GZAQ':  0x0595,   # Great Zaqeph — substitutes ZAQ when ZAQ domain = one short word
    'SEG':   0x0592,   # Segolta
    'SHAL':  0x0593,   # Shalsheleth — substitutes SEG when SEG domain is empty

    # ── H4 disjunctives ──────────────────────────────────────────────────────
    'TEB':   0x059B,   # Tebir (Unicode: "TEVIR")
    'PASH':  0x0599,   # Pashta
    'YETH':  0x059A,   # Yethib — substitutes PASH on short/milra words
    # ZAR = U+05AE; Unicode calls it "ZINOR" — grammar usage is inverted
    'ZAR':   0x05AE,   # Zarqa (H4 disjunctive; Unicode "ZINOR")
    'REB':   0x0597,   # Rebia (Unicode: "REVIA")

    # ── H5 disjunctives ──────────────────────────────────────────────────────
    'GER':   0x059C,   # Geresh
    'GER2':  0x059E,   # Garshaim (Unicode: "GERSHAYIM")
    'PAZ':   0x05A1,   # Pazer
    'GTEL':  0x05A0,   # Great Telisha (Unicode: "TELISHA GEDOLA")
    'GPAZ':  0x059F,   # Great Pazer (Unicode: "QARNEY PARA")
    'LEG':   None,     # Legarmeh: detected as MUN+PAS on same word

    # ── Conjunctives ─────────────────────────────────────────────────────────
    'MUN':   0x05A3,   # Munach — also base of Legarmeh
    'MER':   0x05A5,   # Mereka
    'MER2':  0x05A6,   # Double Mereka (very rare, before TIP)
    'MAH':   0x05A4,   # Mahpak (rank I before PASH)
    'DAR':   0x05A7,   # Darga
    'AZL':   0x05A8,   # Azla (Unicode: "QADMA")
    'LTEL':  0x05A9,   # Little Telisha (Unicode: "TELISHA QETANA")
    'GAL':   0x05AB,   # Galgal (very rare, before GPAZ; Unicode: "OLE")

    # ── Diacritics used for context-dependent detection ───────────────────────
    'PAS':   0x05C0,   # Paseq — marks Legarmeh when combined with MUN
    # TSIN = U+0598; Unicode "ZARQA" — grammar usage is inverted; not a prose accent
    'TSIN':  0x0598,
}

# Codepoint → accent name (for all accents except the context-dependent combination marks)
_CP_TO_NAME: dict[int, str] = {
    cp: name
    for name, cp in _CP.items()
    if cp is not None and name not in ('LEG', 'PAS', 'TSIN', 'SOP')
}

# Disjunctive accent sets by hierarchy level
DISJUNCTIVES: dict[str, set[str]] = {
    'H2': {'SIL', 'ATH'},
    'H3': {'TIP', 'ZAQ', 'GZAQ', 'SEG', 'SHAL'},
    'H4': {'TEB', 'PASH', 'YETH', 'ZAR', 'REB'},
    'H5': {'GER', 'GER2', 'PAZ', 'GTEL', 'GPAZ', 'LEG'},
}

ALL_DISJUNCTIVES: set[str] = set().union(*DISJUNCTIVES.values())

CONJUNCTIVES: set[str] = {'MUN', 'MER', 'MER2', 'MAH', 'DAR', 'AZL', 'LTEL', 'GAL'}

# Hierarchy level number (lower number = stronger/higher in tree)
_LEVEL: dict[str, int] = {'SOP': 1}   # SOP is H1 root
for _lvl_name, _acc_set in DISJUNCTIVES.items():
    _n = int(_lvl_name[1:])
    for _a in _acc_set:
        _LEVEL[_a] = _n

# ── Data structures ────────────────────────────────────────────────────────────


@dataclass
class Word:
    """One Hebrew word with its accent classification."""
    position: int          # 1-based word_num in verse
    text: str              # full cantillated Unicode text
    accent_name: str       # e.g. 'ATH', 'MUN', 'NONE'
    is_legarmeh: bool = False
    is_silluq: bool = False


@dataclass
class AccentNode:
    """One node in the hierarchical accent tree (Price's dichotomy model).

    Per the Law of Continuous Dichotomy, each disjunctive governor has at most
    one direct child node: the rightmost sub-disjunctive in its domain (the
    "near" sub-governor).  That child's domain then contains the next-rightmost
    sub-disjunctive as ITS child, and so on — producing a right-leaning chain.

    ``words`` holds the governor word itself plus any conjunctive words that
    immediately precede it (between the near sub-governor and this governor).
    """
    accent: str
    words: list[Word] = field(default_factory=list)
    children: list['AccentNode'] = field(default_factory=list)

    @property
    def level(self) -> int:
        return _LEVEL.get(self.accent, 0)

    @property
    def label(self) -> str:
        return self.accent

    @property
    def governor_word(self) -> Optional[Word]:
        """The actual disjunctive word (last in self.words)."""
        return self.words[-1] if self.words else None


# ── Accent detection ───────────────────────────────────────────────────────────


def _codepoints(text: str) -> set[int]:
    return {ord(ch) for ch in text}


def _classify_word(text: str, is_last_word: bool) -> tuple[str, bool, bool]:
    """Return (accent_name, is_legarmeh, is_silluq) for a Hebrew word.

    Silluq (H2): U+05BD (Meteg) on the last word of the verse.
    Legarmeh (H5): U+05A3 (Munach) + U+05C0 (Paseq) on the same word.
    All others: first match in _CP_TO_NAME scanning for disjunctives, then conjunctives.
    """
    cps = _codepoints(text)

    # Legarmeh: Munach + Paseq on same word
    is_leg = (_CP['MUN'] in cps) and (_CP['PAS'] in cps)
    if is_leg:
        return 'LEG', True, False

    # Silluq: Meteg on last word
    is_sil = is_last_word and (_CP['SIL'] in cps)
    if is_sil:
        return 'SIL', False, True

    # Disjunctives take priority over conjunctives
    for cp, name in _CP_TO_NAME.items():
        if cp in cps and name in ALL_DISJUNCTIVES:
            return name, False, False

    # Conjunctives
    for cp, name in _CP_TO_NAME.items():
        if cp in cps and name in CONJUNCTIVES:
            return name, False, False

    return 'NONE', False, False


def _build_word_list(verse_df: Any) -> list[Word]:
    """Convert a verse DataFrame into an ordered list of Word objects.

    MACULA splits prefixes into separate rows sharing a word_num; we join them.
    The Soph Pasuq (U+05C3) may appear as the sole content of the last entry;
    we drop such punctuation-only entries so the last real word carries Silluq.
    """
    grouped = (
        verse_df.groupby('word_num', sort=True)['text']
        .apply(lambda parts: ''.join(str(p) for p in parts))
    )
    words_raw = [(int(wn), str(txt)) for wn, txt in grouped.items()]

    # Drop trailing Soph-Pasuq-only words (punctuation entries)
    sop_cp = _CP['SOP']
    while words_raw:
        _, txt = words_raw[-1]
        non_sop = {ord(c) for c in txt if not c.isspace()} - {sop_cp}
        if not non_sop:
            words_raw.pop()
        else:
            break

    if not words_raw:
        return []

    last_idx = len(words_raw) - 1
    result: list[Word] = []
    for i, (wnum, txt) in enumerate(words_raw):
        acc, is_leg, is_sil = _classify_word(txt, i == last_idx)
        result.append(Word(
            position=wnum,
            text=txt,
            accent_name=acc,
            is_legarmeh=is_leg,
            is_silluq=is_sil,
        ))
    return result


# ── Tree builder (Price's Law of Continuous Dichotomy) ────────────────────────
#
# For a span words[start:end] whose governor is words[end-1]:
#   1. Collect conjunctive words immediately before the governor into node.words.
#   2. Find the rightmost (near) sub-disjunctive in what remains.
#   3. That sub-disjunctive becomes the single child; recurse into its sub-span.
#
# This produces a right-leaning chain reflecting Price's near-first dichotomy:
#   ATH → TIP → ZAQ → PASH → ... (each links to the next-nearest sub-domain)


def _parse_domain(words: list[Word], start: int, end: int) -> AccentNode:
    """Parse words[start:end] as a domain governed by words[end-1].

    Args:
        words: The full ordered word list for the verse.
        start: Inclusive start index.
        end:   Exclusive end index.  words[end-1] is the governing word.

    Returns:
        AccentNode whose accent matches words[end-1].accent_name.
    """
    gov = words[end - 1]
    node = AccentNode(accent=gov.accent_name)

    if start >= end - 1:
        # Only the governor word; no sub-domain
        node.words = [gov]
        return node

    # Find the rightmost sub-disjunctive in [start, end-1)
    near_idx = -1
    for i in range(end - 2, start - 1, -1):
        if words[i].accent_name in ALL_DISJUNCTIVES:
            near_idx = i
            break

    if near_idx == -1:
        # No sub-disjunctives: all words in [start, end) are conjunctives + governor
        node.words = list(words[start:end])
        return node

    # Governor's own words: conjunctives from near_idx+1 to end-1, plus governor
    node.words = list(words[near_idx + 1:end])   # includes gov at end-1

    # Single child: the sub-domain [start, near_idx+1) whose governor is words[near_idx]
    child = _parse_domain(words, start, near_idx + 1)
    node.children = [child]

    return node


def parse_verse(book: str, chapter: int, verse: int) -> AccentNode:
    """Parse a prose verse into a hierarchical AccentNode tree (Price's system).

    The root node has accent 'SOP'.  Its children are (if ATH is present):
    an ATH subtree (first half of verse) and a SIL subtree (second half);
    or just a SIL subtree if ATH is absent.

    Args:
        book:    Canonical book ID (e.g. 'Gen', 'Exo').
        chapter: 1-based chapter number.
        verse:   1-based verse number.

    Returns:
        AccentNode rooted at 'SOP'.

    Raises:
        ValueError: if the book uses the poetic accent system.
        LookupError: if the verse is not found in the data.
    """
    if book in POETRY_BOOKS:
        raise ValueError(
            f"'{book}' uses the poetic accent system; "
            "Price's prose hierarchy does not apply."
        )

    from ..core.syntax_ot import query_syntax_ot
    verse_df = query_syntax_ot(book=book, chapter=chapter, verse=verse)

    if verse_df.empty:
        raise LookupError(f"Verse not found: {book} {chapter}:{verse}")

    words = _build_word_list(verse_df)

    root = AccentNode(accent='SOP')

    if not words:
        return root

    # Find ATH (Athnach) — primary H2 boundary dividing verse into two segments.
    ath_idx = next(
        (i for i, w in enumerate(words) if w.accent_name == 'ATH'),
        None,
    )

    if ath_idx is not None:
        # Remote segment: words[0 : ath_idx+1] — governed by ATH
        root.children.append(_parse_domain(words, 0, ath_idx + 1))
        # Near segment: words[ath_idx+1 : end] — governed by SIL
        if ath_idx + 1 < len(words):
            root.children.append(_parse_domain(words, ath_idx + 1, len(words)))
    else:
        # No ATH: whole verse is a single SIL domain
        root.children.append(_parse_domain(words, 0, len(words)))

    return root


# ── Diagram renderer ───────────────────────────────────────────────────────────


def _collect_words(node: AccentNode) -> list[Word]:
    """Return all words in the subtree, ordered by word position."""
    result = list(node.words)
    for child in node.children:
        result.extend(_collect_words(child))
    return sorted(result, key=lambda w: w.position)


def _display_text(text: str) -> str:
    """Strip cantillation accent marks (U+0591–U+05AF) for display.

    Vowels (U+05B0–U+05BD) are kept; accent type is shown in label boxes.
    Returns a bidi-processed string ready for matplotlib rendering.
    """
    from bidi.algorithm import get_display
    stripped = ''.join(c for c in text if not (0x0591 <= ord(c) <= 0x05AF))
    return get_display('‫' + stripped + '‬')


def render_verse(
    book: str,
    chapter: int,
    verse: int,
    output_path: Optional[str | Path] = None,
    style: str = 'bracket',
) -> Path:
    """Render a cantillation hierarchy diagram and save as PNG.

    Produces a matplotlib figure (bracket-style, mirroring Price's hierarchy
    diagrams) with Hebrew text at the bottom and accent labels in boxes above,
    connected by lines.  Hebrew words are displayed RTL using python-bidi.

    Args:
        book:        Canonical book ID (e.g. 'Gen').
        chapter:     1-based chapter number.
        verse:       1-based verse number.
        output_path: Destination PNG.  Defaults to
                     reports/ot/cantillation/<book>/<book>_<ch>_<vs>.png
        style:       Currently only 'bracket' is supported.

    Returns:
        Path to the saved PNG.
    """
    import warnings
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import matplotlib.font_manager as _fm
    from bidi.algorithm import get_display

    # Use Arial Hebrew (macOS system font) for Hebrew glyphs; fall back gracefully
    _hebrew_fonts = ['Arial Hebrew', 'Raanana', 'New Peninim MT', 'SBL Hebrew',
                     'Ezra SIL', 'DejaVu Sans']
    _heb_prop = None
    for _fn in _hebrew_fonts:
        try:
            _heb_prop = _fm.FontProperties(family=_fn)
            break
        except Exception:
            continue

    tree = parse_verse(book, chapter, verse)

    if output_path is None:
        out_dir = Path('reports/ot/cantillation') / book
        out_dir.mkdir(parents=True, exist_ok=True)
        output_path = out_dir / f'{book}_{chapter:02d}_{verse:02d}.png'
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    all_words = sorted(_collect_words(tree), key=lambda w: w.position)
    if not all_words:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, f'{book} {chapter}:{verse} — no accent data',
                ha='center', va='center', transform=ax.transAxes)
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return output_path

    # Hebrew is RTL: word 1 is rightmost on page.
    # We mirror x so position 1 appears at the right of the plot.
    max_pos = max(w.position for w in all_words)
    min_pos = min(w.position for w in all_words)

    def mirror(pos: int) -> float:
        return float(max_pos + min_pos - pos)

    # Compute node centre-x as mean of mirrored word positions in its subtree
    # y-coordinates: H1 (SOP) at top → words at bottom
    # Level 1=SOP, 2=SIL/ATH, 3=TIP/ZAQ, 4=TEB/PASH, 5=GER/PAZ
    LEVEL_Y = {1: 7.0, 2: 5.8, 3: 4.6, 4: 3.4, 5: 2.2, 0: 1.4}
    WORD_Y = 0.3

    LEVEL_COLORS = {
        1: '#c62828',   # H1 — deep red
        2: '#e65100',   # H2 — orange
        3: '#f9a825',   # H3 — amber
        4: '#2e7d32',   # H4 — green
        5: '#1565c0',   # H5 — blue
        0: '#616161',   # conjunctive / NONE — grey
    }

    # Layout: assign (x, y) to each node based on mean position of subtree words
    node_layout: dict[int, tuple[float, float]] = {}
    _nid = [0]

    def _assign_id(node: AccentNode) -> int:
        _nid[0] += 1
        return _nid[0]

    node_ids: dict[int, int] = {}  # id(node) → int

    def _layout(node: AccentNode) -> None:
        nid = _assign_id(node)
        node_ids[id(node)] = nid
        sub_words = _collect_words(node)
        cx = sum(mirror(w.position) for w in sub_words) / max(1, len(sub_words))
        lvl = _LEVEL.get(node.accent, 0)
        cy = LEVEL_Y.get(lvl, 0.8)
        node_layout[nid] = (cx, cy)
        for child in node.children:
            _layout(child)

    _layout(tree)

    n_words = max_pos - min_pos + 1
    fig_width = max(10, n_words * 1.4)
    fig, ax = plt.subplots(figsize=(fig_width, 9))
    ax.set_xlim(mirror(max_pos) - 0.7, mirror(min_pos) + 0.7)
    ax.set_ylim(-0.5, 8.0)
    ax.axis('off')

    ref_str = f'{book} {chapter}:{verse}'
    ax.set_title(
        get_display(f'Cantillation Structure: {ref_str}'),
        fontsize=13, pad=12,
    )

    def _draw(node: AccentNode) -> None:
        nid = node_ids[id(node)]
        nx, ny = node_layout[nid]
        lvl = _LEVEL.get(node.accent, 0)
        color = LEVEL_COLORS.get(lvl, '#616161')

        # Draw accent label box
        ax.text(nx, ny, node.accent,
                ha='center', va='center', fontsize=8, color=color,
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                          edgecolor=color, linewidth=1.5),
                zorder=3)

        # Draw governor's words at bottom (Hebrew, RTL, accent marks stripped)
        for w in node.words:
            wx = mirror(w.position)
            acc_lvl = _LEVEL.get(w.accent_name, 0)
            acc_color = LEVEL_COLORS.get(acc_lvl, '#616161')
            heb = _display_text(w.text)
            txt_kwargs: dict = dict(
                ha='center', va='bottom', fontsize=9, color='#1a237e',
            )
            if _heb_prop is not None:
                txt_kwargs['fontproperties'] = _heb_prop
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                ax.text(wx, WORD_Y + 0.15, heb, **txt_kwargs)
            # Small accent label under Hebrew
            ax.text(wx, WORD_Y - 0.3, w.accent_name,
                    ha='center', va='top', fontsize=6, color=acc_color)
            # Line from node box down to word
            ax.plot([nx, wx], [ny - 0.22, WORD_Y + 0.6],
                    color=color, lw=0.8, alpha=0.6, zorder=1)

        # Lines to children
        for child in node.children:
            cnid = node_ids[id(child)]
            cx2, cy2 = node_layout[cnid]
            ax.annotate(
                '', xy=(cx2, cy2 + 0.22), xytext=(nx, ny - 0.22),
                arrowprops=dict(arrowstyle='-', color=color, lw=1.2,
                                connectionstyle='arc3,rad=0.05'),
                zorder=2,
            )
            _draw(child)

    _draw(tree)

    # Legend
    legend_handles = [
        mpatches.Patch(facecolor='white', edgecolor=LEVEL_COLORS[1],
                       label='H1 — Soph Pasuq'),
        mpatches.Patch(facecolor='white', edgecolor=LEVEL_COLORS[2],
                       label='H2 — Silluq / Athnach'),
        mpatches.Patch(facecolor='white', edgecolor=LEVEL_COLORS[3],
                       label='H3 — Tiphcha / Zaqeph / Segolta'),
        mpatches.Patch(facecolor='white', edgecolor=LEVEL_COLORS[4],
                       label='H4 — Tebir / Pashta / Zarqa / Rebia'),
        mpatches.Patch(facecolor='white', edgecolor=LEVEL_COLORS[5],
                       label='H5 — Geresh / Pazer / Legarmeh'),
        mpatches.Patch(facecolor='white', edgecolor=LEVEL_COLORS[0],
                       label='Conjunctive'),
    ]
    ax.legend(handles=legend_handles, loc='upper right', fontsize=7,
              framealpha=0.9, ncol=2, title='Accent hierarchy (Price)',
              title_fontsize=7)

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        plt.tight_layout()
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return output_path


# ── Park-format renderer ───────────────────────────────────────────────────────
#
# Source: Sung Jin Park, "The Fundamentals of Hebrew Accents: Divisions and
#         Exegetical Roles Beyond Syntax" (2023).
#
# Layout: horizontal bracket/staircase (one panel per H2 domain).
# RTL word order: D0 governor appears LEFTMOST; earlier verse words extend right.
# Chain mapping (Price → Park depth labels):
#   chain idx  0  1    2   3    4   5    6   ...
#   Park label D0 D1f  D1  D2f  D2  D3f  D3
#   Meaning    governor  near  far  near  far  ...
#   ("f" = final/near branch at that depth)

_ACCENT_DISPLAY: dict[str, str] = {
    'ATH': 'Athnach',    'SIL': 'Silluq',      'TIP': 'Tiphcha',
    'ZAQ': 'Zaqeph',     'GZAQ': 'Gt. Zaqeph', 'SEG': 'Segolta',
    'SHAL': 'Shalsheleth', 'TEB': 'Tebir',     'PASH': 'Pashta',
    'YETH': 'Yethib',    'ZAR': 'Zarqa',       'REB': 'Rebia',
    'GER': 'Geresh',     'GER2': 'Garshaim',   'PAZ': 'Pazer',
    'GTEL': 'Gt. Telisha', 'GPAZ': 'Gt. Pazer', 'LEG': 'Legarmeh',
    'MUN': 'Munach',     'MER': 'Mereka',       'MER2': 'Dbl. Mereka',
    'MAH': 'Mahpak',     'DAR': 'Darga',        'AZL': 'Azla',
    'LTEL': 'Lt. Telisha', 'GAL': 'Galgal',     'NONE': '',
}


def _park_label(chain_idx: int) -> str:
    """Park depth-label for Price chain position i.

    i=0→D0, i=1→D1f, i=2→D1, i=3→D2f, i=4→D2, i=5→D3f, i=6→D3, …
    """
    if chain_idx == 0:
        return 'D0'
    if chain_idx % 2 == 1:
        return f'D{(chain_idx + 1) // 2}f'
    return f'D{chain_idx // 2}'


def _get_park_chain(
    panel_node: AccentNode,
) -> list[tuple[AccentNode, str]]:
    """Walk Price's right-leaning chain and return [(node, park_label), ...]."""
    chain: list[tuple[AccentNode, str]] = []
    current: Optional[AccentNode] = panel_node
    i = 0
    while current is not None:
        chain.append((current, _park_label(i)))
        current = current.children[0] if current.children else None
        i += 1
    return chain


def render_verse_park(
    book: str,
    chapter: int,
    verse: int,
    output_path: Optional[str | Path] = None,
) -> Path:
    """Render a Park-format bracket/staircase cantillation diagram as PNG.

    One panel per H2 domain (ATH half = 'a', SIL half = 'b').
    Governer (D0) appears leftmost; earlier verse words extend rightward (RTL).
    Bracket lines step down like a staircase: D0 at top-left, deeper domains
    lower and further right.  D1f labels are grayed (near/final branch role).
    Accent names shown in italics below each governing word.

    Source: Sung Jin Park, "The Fundamentals of Hebrew Accents" (2023).
    """
    import warnings
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as _fm
    from bidi.algorithm import get_display

    _hebrew_fonts = ['Arial Hebrew', 'Raanana', 'New Peninim MT',
                     'SBL Hebrew', 'Ezra SIL', 'DejaVu Sans']
    _heb_prop = None
    for _fn in _hebrew_fonts:
        try:
            _heb_prop = _fm.FontProperties(family=_fn)
            break
        except Exception:
            continue

    tree = parse_verse(book, chapter, verse)

    if output_path is None:
        out_dir = Path('output/reports/ot/cantillation') / book
        out_dir.mkdir(parents=True, exist_ok=True)
        output_path = out_dir / f'{book}_{chapter:02d}_{verse:02d}.png'
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    panels = tree.children
    if not panels:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.text(0.5, 0.5, f'{book} {chapter}:{verse} — no accent data',
                ha='center', va='center', transform=ax.transAxes)
        fig.savefig(Path(output_path), dpi=150, bbox_inches='tight')
        plt.close(fig)
        return Path(output_path)

    # ── Layout constants ────────────────────────────────────────────────────
    COL_W: float = 2.2       # x-units per word column
    BRACKET_H: float = 0.85  # y-units per bracket depth step (0 = deepest)
    WORD_Y: float = -0.15    # Hebrew word text centre y
    PLABEL_Y: float = -0.62  # Park label top y  (below word)
    ACCENT_Y: float = -0.98  # accent name top y (italic, below Park label)
    BOT_Y: float = -1.35     # bottom of the word area
    LEFT_MARGIN: float = 1.8  # x-space left of col 0 for bracket labels

    # ── Collect per-panel data ──────────────────────────────────────────────
    panel_names = ['a' if p.accent == 'ATH' else 'b' for p in panels]
    chains = [_get_park_chain(p) for p in panels]
    all_words_per_panel = [
        sorted(_collect_words(p), key=lambda w: -w.position)
        for p in panels
    ]
    overall_max_depth = max(len(c) for c in chains)
    max_cols = max(len(wl) for wl in all_words_per_panel)

    bracket_top: float = overall_max_depth * BRACKET_H
    panel_h: float = bracket_top - BOT_Y + 0.4
    n_panels = len(panels)
    fig_w = max(10.0, LEFT_MARGIN + max_cols * COL_W + 0.6)
    fig_h = max(4.0, n_panels * panel_h + 1.0)

    fig = plt.figure(figsize=(fig_w, fig_h))
    ref_str = f'{book} {chapter}:{verse}'
    fig.suptitle(
        get_display(f'Cantillation (Park): {ref_str}'),
        fontsize=13, y=0.99,
    )

    for p_idx in range(n_panels):
        chain = chains[p_idx]
        all_words = all_words_per_panel[p_idx]
        pname = panel_names[p_idx]
        n_cols = len(all_words)

        ax = fig.add_subplot(n_panels, 1, p_idx + 1)
        ax.set_xlim(-LEFT_MARGIN, n_cols * COL_W + 0.5)
        ax.set_ylim(BOT_Y - 0.1, bracket_top + 0.4)
        ax.axis('off')

        # Panel half-label (a / b) top-left
        ax.text(-LEFT_MARGIN + 0.1, bracket_top + 0.3, pname,
                ha='left', va='top', fontsize=10, style='italic', color='#555')

        # pos → column index (0 = leftmost = latest word in verse)
        pos_to_col: dict[int, int] = {w.position: i for i, w in enumerate(all_words)}

        # Assign Park label to every word in the panel
        word_park_label: dict[int, str] = {}
        for node, plabel in chain:
            gov = node.governor_word
            if gov is not None:
                word_park_label[gov.position] = plabel
            for w in node.words[:-1]:   # conjunctives before governor
                word_park_label[w.position] = 'C'

        # ── Vertical column separators ──────────────────────────────────────
        for c in range(n_cols + 1):
            ax.plot([c * COL_W, c * COL_W], [BOT_Y, 0.0],
                    color='#cccccc', lw=0.5, zorder=0)

        # ── Hebrew words + labels ───────────────────────────────────────────
        for w in all_words:
            cx: float = pos_to_col[w.position] * COL_W + COL_W / 2
            heb = _display_text(w.text)
            txt_kw: dict = dict(ha='center', va='center',
                                fontsize=11, color='#1a237e')
            if _heb_prop is not None:
                txt_kw['fontproperties'] = _heb_prop
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                ax.text(cx, WORD_Y, heb, **txt_kw)

            plabel = word_park_label.get(w.position, 'C')
            is_final = plabel.endswith('f')
            lbl_col = '#999999' if is_final else '#222222'
            ax.text(cx, PLABEL_Y, plabel,
                    ha='center', va='top', fontsize=8, color=lbl_col)

            if w.accent_name in ALL_DISJUNCTIVES or w.is_silluq or w.is_legarmeh:
                acc = _ACCENT_DISPLAY.get(w.accent_name, w.accent_name)
                ax.text(cx, ACCENT_Y, acc,
                        ha='center', va='top', fontsize=7,
                        style='italic', color='#666666')

        # ── Bracket staircase ───────────────────────────────────────────────
        for chain_idx, (node, plabel) in enumerate(chain):
            gov = node.governor_word
            if gov is None:
                continue

            bk_y: float = bracket_top - chain_idx * BRACKET_H
            lx: float = pos_to_col[gov.position] * COL_W   # left edge of governor col

            sub = _collect_words(node)
            earliest = min(sub, key=lambda w: w.position)
            rx: float = (pos_to_col[earliest.position] + 1) * COL_W  # right edge

            is_final = plabel.endswith('f')
            bk_col = '#aaaaaa' if is_final else '#333333'
            bk_lw: float = 1.0 if is_final else 1.6

            # Horizontal bracket line
            ax.plot([lx, rx], [bk_y, bk_y],
                    color=bk_col, lw=bk_lw, solid_capstyle='butt', zorder=3)

            # Left vertical drop from bracket to word area
            ax.plot([lx, lx], [0.0, bk_y],
                    color=bk_col, lw=bk_lw * 0.75, zorder=2)

            # Park label to the left of the governor column
            fw = 'normal' if is_final else 'bold'
            ax.text(lx - 0.12, bk_y + 0.06, plabel,
                    ha='right', va='bottom', fontsize=8,
                    color=bk_col, fontweight=fw)

            # Accent name in italics below the Park label (left side)
            acc = _ACCENT_DISPLAY.get(gov.accent_name, '')
            if acc:
                ax.text(lx - 0.12, bk_y - 0.08, acc,
                        ha='right', va='top', fontsize=7,
                        style='italic', color=bk_col)

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        plt.tight_layout(rect=(0, 0, 1, 0.97))
        fig.savefig(Path(output_path), dpi=150, bbox_inches='tight')
    plt.close(fig)
    return Path(output_path)
