"""Build the Hebrews 12:22-24 "Ye Are Come To" study-help table and chart.

Outputs:
  output/study-helps/nt/hebrews-12-come-to/hebrews12-come-to.md
  output/study-helps/nt/hebrews-12-come-to/hebrews12-come-to-chart.png
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.patches as mpatches  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

REPORT_DIR = Path('output/study-helps/nt/hebrews-12-come-to')
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# (verse, greek_dative_phrase, head_lemma, strongs, kjv, note)
# Greek phrase: the dative expression as it appears in the text (TAGNT/TR).
# Head lemma: lemma of the primary dative noun(s); genitives that depend on
#   them are noted parenthetically where helpful.
ENTRIES: list[tuple[str, str, str, str, str, str]] = [
    (
        '22',
        'ὄρει Σιών',
        'ὄρος / Σιών',
        'G3735 / G4622',
        'mount Sion',
        'The heavenly dwelling of God; contrasted with earthly Mt. Sinai'
        ' (vv. 18–20), where Israel could not draw near.',
    ),
    (
        '22',
        'πόλει θεοῦ ζῶντος,\nἸερουσαλὴμ ἐπουρανίῳ',
        'πόλις / Ἰερουσαλήμ',
        'G4172 / G2419',
        'the city of the living God,\nthe heavenly Jerusalem',
        'Ἰερουσαλήμ ἐπουρανίῳ stands in apposition to πόλει. The city'
        ' Abraham sought, "whose builder and maker is God" (Heb 11:10).',
    ),
    (
        '22',
        'μυριάσιν ἀγγέλων',
        'μυριάς',
        'G3461',
        'an innumerable company of angels',
        'μυριάς = ten thousand; used for an uncountable multitude. The'
        ' angelic host that surrounds the throne of God.',
    ),
    (
        '23',
        'ἐκκλησίᾳ πρωτοτόκων\nἀπογεγραμμένων ἐν οὐρανοῖς',
        'ἐκκλησία / πρωτότοκος',
        'G1577 / G4416',
        'the general assembly and church\nof the firstborn, written in heaven',
        'ἐκκλησία = assembly/congregation. πρωτότοκοι bears the rights of'
        ' the firstborn (cf. Rom 8:29); their names are enrolled in heaven'
        ' (Luke 10:20).',
    ),
    (
        '23',
        'κριτῇ θεῷ πάντων',
        'κριτής / θεός',
        'G2923 / G2316',
        'God the Judge of all',
        'θεῷ stands in apposition to κριτῇ — both dative, identifying the'
        ' universal Judge as God himself.',
    ),
    (
        '23',
        'πνεύμασιν δικαίων\nτετελειωμένων',
        'πνεῦμα / δίκαιος',
        'G4151 / G1342',
        'the spirits of just men made perfect',
        'τετελειωμένων (perf. pass. ptc. of τελειόω) = those brought to'
        ' completion/maturity. The OT saints now perfected through Christ'
        ' (Heb 11:40).',
    ),
    (
        '24',
        'μεσίτῃ Ἰησοῦ\n(διαθήκης νέας)',
        'μεσίτης / Ἰησοῦς',
        'G3316 / G2424',
        'Jesus the mediator of the new covenant',
        'μεσίτης = one who stands between two parties. Jesus is the sole'
        ' mediator of the new covenant (1 Tim 2:5; Heb 8:6; 9:15).',
    ),
    (
        '24',
        'αἵματι ῥαντισμοῦ',
        'αἷμα / ῥαντισμός',
        'G0129 / G4473',
        'the blood of sprinkling',
        'Alludes to OT sprinkling rites (Exod 24:8; Lev 14); speaks "better'
        ' things than Abel" — Abel\'s blood cried for vengeance, Christ\'s'
        ' for forgiveness.',
    ),
]


def build_chart() -> Path:
    """Render the "Ye Are Come To" table as a downloadable PNG."""
    GREEK_WRAP = 28
    LEMMA_WRAP = 22
    KJV_WRAP = 32
    NOTE_WRAP = 44
    ROW_H_PER_LINE = 0.22
    HEADER_H = 0.40

    rows = []
    for verse, greek, lemma, strongs, kjv, note in ENTRIES:
        g_w = textwrap.fill(greek, GREEK_WRAP)
        l_w = textwrap.fill(lemma, LEMMA_WRAP)
        s_w = textwrap.fill(strongs, LEMMA_WRAP)
        k_w = textwrap.fill(kjv, KJV_WRAP)
        n_w = textwrap.fill(note, NOTE_WRAP)
        lines = max(
            len(g_w.split('\n')),
            len(l_w.split('\n')) + len(s_w.split('\n')),
            len(k_w.split('\n')),
            len(n_w.split('\n')),
            1,
        )
        h = lines * ROW_H_PER_LINE + 0.12
        rows.append((verse, g_w, l_w, s_w, k_w, n_w, h))

    fig_w = 15.0
    title_h = 0.70
    footer_h = 0.25
    data_h = HEADER_H + sum(r[6] for r in rows)
    fig_h = title_h + data_h + footer_h + 0.2

    fig = plt.figure(figsize=(fig_w, fig_h))
    fig.patch.set_facecolor('white')

    HEADER_BG = '#1A3A5C'
    HEADER_FG = 'white'
    ROW_BG_A = '#EAF1FB'
    ROW_BG_B = 'white'
    BORDER = '#AAAAAA'

    margin_l = 0.03
    margin_r = 0.03
    usable_w = 1.0 - margin_l - margin_r
    # Verse | Greek | Lemma/Strongs | KJV | Note
    col_props = [0.055, 0.215, 0.165, 0.225, 0.340]
    col_x = [margin_l + sum(col_props[:i]) * usable_w for i in range(len(col_props) + 1)]

    def fig_frac(inches: float) -> float:
        return inches / fig_h

    fig.text(0.5, 1.0 - 0.18 / fig_h,
             'Hebrews 12:22–24 — "Ye Are Come To"',
             ha='center', va='top', fontsize=16, fontweight='bold', color='#1A3A5C')
    fig.text(0.5, 1.0 - 0.46 / fig_h,
             'King James Version  ·  Objects of προσεληλύθατε (dative case)',
             ha='center', va='top', fontsize=10, color='#555555', style='italic')

    def draw_cell(x0: float, x1: float, y0: float, y1: float,
                  text: str, bg: str, fg: str,
                  fontsize: float = 9, bold: bool = False) -> None:
        rect = mpatches.FancyBboxPatch(
            (x0, y0), x1 - x0, y1 - y0,
            boxstyle='square,pad=0', linewidth=0.4,
            edgecolor=BORDER, facecolor=bg,
            transform=fig.transFigure, clip_on=False,
        )
        fig.add_artist(rect)
        fig.text((x0 + x1) / 2, (y0 + y1) / 2, text,
                 ha='center', va='center', fontsize=fontsize,
                 fontweight='bold' if bold else 'normal', color=fg,
                 multialignment='center', transform=fig.transFigure)

    def draw_lemma_cell(x0: float, x1: float, y0: float, y1: float,
                        lemma_text: str, strongs_text: str, bg: str) -> None:
        """Lemma cell: lemma on top in dark color, Strongs in smaller gray below."""
        rect = mpatches.FancyBboxPatch(
            (x0, y0), x1 - x0, y1 - y0,
            boxstyle='square,pad=0', linewidth=0.4,
            edgecolor=BORDER, facecolor=bg,
            transform=fig.transFigure, clip_on=False,
        )
        fig.add_artist(rect)

        cx = (x0 + x1) / 2
        line_h = fig_frac(ROW_H_PER_LINE)
        l_lines = len(lemma_text.split('\n'))
        s_lines = len(strongs_text.split('\n'))
        gap = line_h * 0.25
        total_h = l_lines * line_h + gap + s_lines * line_h
        center_y = (y0 + y1) / 2
        top_y = center_y + total_h / 2

        l_center = top_y - l_lines * line_h / 2
        fig.text(cx, l_center, lemma_text,
                 ha='center', va='center', fontsize=9,
                 fontweight='bold', color='#1A3A5C',
                 multialignment='center', transform=fig.transFigure)

        s_center = top_y - l_lines * line_h - gap - s_lines * line_h / 2
        fig.text(cx, s_center, strongs_text,
                 ha='center', va='center', fontsize=7.5,
                 fontweight='normal', color='#888888',
                 multialignment='center', transform=fig.transFigure)

    y_top = 1.0 - fig_frac(title_h)
    y = y_top
    h_h = fig_frac(HEADER_H)
    headers = ['Verse', 'Greek (dative)', 'Lemma / Strongs', 'KJV', 'Note']
    for i, label in enumerate(headers):
        draw_cell(col_x[i], col_x[i + 1], y - h_h, y, label,
                  HEADER_BG, HEADER_FG, fontsize=10, bold=True)
    y -= h_h

    for idx, (verse, g_w, l_w, s_w, k_w, n_w, rh) in enumerate(rows):
        bg = ROW_BG_A if idx % 2 == 0 else ROW_BG_B
        rh_f = fig_frac(rh)
        draw_cell(col_x[0], col_x[1], y - rh_f, y, verse, bg, '#111111', fontsize=9)
        draw_cell(col_x[1], col_x[2], y - rh_f, y, g_w, bg, '#1A3A5C', fontsize=9,
                  bold=True)
        draw_lemma_cell(col_x[2], col_x[3], y - rh_f, y, l_w, s_w, bg)
        draw_cell(col_x[3], col_x[4], y - rh_f, y, k_w, bg, '#222222', fontsize=8.5)
        draw_cell(col_x[4], col_x[5], y - rh_f, y, n_w, bg, '#444444', fontsize=8.0)
        y -= rh_f

    fig.text(0.5, footer_h / fig_h / 2, 'bereanbiblebots.com',
             ha='center', va='bottom', fontsize=8, color='#AAAAAA',
             transform=fig.transFigure)

    out = REPORT_DIR / 'hebrews12-come-to-chart.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'Saved {out}')
    return out


def build_report() -> Path:
    lines: list[str] = [
        '# Hebrews 12:22–24 — "Ye Are Come To"',
        '',
        '**Text:** KJV · **Passage:** Hebrews 12:22–24',
        '',
        'In verse 22 the author writes, *"But **ye are come** unto…"*'
        ' (ἀλλὰ **προσεληλύθατε**…). The verb is a 2nd-person perfect'
        ' active indicative, emphasizing a completed approach with present'
        ' effect. What follows is a series of eight dative objects — the'
        ' realities believers have already come to under the new covenant.'
        ' Each is listed below with its Greek form, head lemma(ta), Strongs'
        ' number(s), KJV rendering, and a brief explanatory note.',
        '',
        '---',
        '',
        '| Verse | Greek (dative) | Lemma | KJV | Note |',
        '|---|---|---|---|---|',
    ]

    for verse, greek, lemma, _strongs, kjv, note in ENTRIES:
        greek_cell = greek.replace('\n', ' ')
        lemma_cell = lemma
        kjv_cell = kjv.replace('\n', ' ')
        note_cell = note.replace('|', '\\|')
        lines.append(
            f'| {verse} | {greek_cell} | {lemma_cell} |'
            f' {kjv_cell} | {note_cell} |'
        )

    lines += [
        '',
        '---',
        '',
        '## Downloadable Chart',
        '',
        'Right-click the image below and choose **Save image as…** to download'
        ' a high-resolution PNG suitable for printing or sharing.',
        '',
        '![Hebrews 12 Come To chart](hebrews12-come-to-chart.png)',
        '',
        '---',
        '',
        '*Text: King James Version (KJV).*',
        ' *Greek data: TAGNT (Byzantine/Textus Receptus tradition).*',
        ' *Generated by'
        ' [scripts/nt/study-helps/build_hebrews12_come_to.py]'
        '(../../../../scripts/nt/study-helps/build_hebrews12_come_to.py).*',
    ]

    out = REPORT_DIR / 'hebrews12-come-to.md'
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Saved {out}')
    return out


if __name__ == '__main__':
    build_chart()
    build_report()
    print('Done.')
