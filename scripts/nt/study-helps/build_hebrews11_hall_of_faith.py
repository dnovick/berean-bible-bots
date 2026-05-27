"""Build the Hebrews 11 Hall of Faith study-help table and chart image.

Outputs:
  output/study-helps/nt/hebrews-11-hall-of-faith/hebrews11-hall-of-faith.md
  output/study-helps/nt/hebrews-11-hall-of-faith/hebrews11-hall-of-faith-chart.png
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.patches as mpatches  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

REPORT_DIR = Path('output/study-helps/nt/hebrews-11-hall-of-faith')
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# (verses, person, what they did by faith) — KJV
ENTRIES: list[tuple[str, str, str]] = [
    (
        '4',
        'Abel',
        'Offered unto God a more excellent sacrifice than Cain, and obtained witness'
        ' that he was righteous, God testifying of his gifts.',
    ),
    (
        '5',
        'Enoch',
        'Was translated that he should not see death, and was not found because God'
        ' had translated him; for before his translation he had this testimony, that'
        ' he pleased God.',
    ),
    (
        '7',
        'Noah',
        'Being warned of God of things not seen as yet, moved with fear, prepared an'
        ' ark to the saving of his house; by the which he condemned the world and'
        ' became heir of the righteousness which is by faith.',
    ),
    (
        '8–10',
        'Abraham',
        'Obeyed when he was called to go out into a place which he should after'
        ' receive for an inheritance; went out, not knowing whither he went.'
        ' Sojourned in the land of promise as in a strange country, looking for a'
        ' city which hath foundations, whose builder and maker is God.',
    ),
    (
        '11',
        'Sarah',
        'Received strength to conceive seed and was delivered of a child when she'
        ' was past age, because she judged him faithful who had promised.',
    ),
    (
        '17–19',
        'Abraham',
        'Offered up Isaac when he was tried; accounted that God was able to raise'
        ' him up even from the dead, from whence also he received him in a figure.',
    ),
    (
        '20',
        'Isaac',
        'Blessed Jacob and Esau concerning things to come.',
    ),
    (
        '21',
        'Jacob',
        'Blessed both the sons of Joseph when he was a dying, and worshipped,'
        ' leaning upon the top of his staff.',
    ),
    (
        '22',
        'Joseph',
        'When he died, made mention of the departing of the children of Israel and'
        ' gave commandment concerning his bones.',
    ),
    (
        '23',
        "Moses' parents",
        'Hid Moses three months after he was born, because they saw he was a proper'
        ' child; and they were not afraid of the king\'s commandment.',
    ),
    (
        '24–26',
        'Moses',
        'Refused to be called the son of Pharaoh\'s daughter, choosing rather to'
        ' suffer affliction with the people of God than to enjoy the pleasures of'
        ' sin for a season; esteeming the reproach of Christ greater riches than the'
        ' treasures in Egypt.',
    ),
    (
        '27',
        'Moses',
        'Forsook Egypt, not fearing the wrath of the king; endured as seeing him'
        ' who is invisible.',
    ),
    (
        '28',
        'Moses',
        'Kept the passover and the sprinkling of blood, lest he that destroyed the'
        ' firstborn should touch them.',
    ),
    (
        '29',
        'Israel',
        'Passed through the Red sea as by dry land; which the Egyptians assaying to'
        ' do were drowned.',
    ),
    (
        '30',
        'Israel',
        'Compassed the walls of Jericho seven days; and the walls fell down.',
    ),
    (
        '31',
        'Rahab',
        'Perished not with them that believed not, when she had received the spies'
        ' with peace.',
    ),
    (
        '32–38',
        'Gideon, Barak, Samson, Jephthah,\nDavid, Samuel, and the prophets',
        'Subdued kingdoms, wrought righteousness, obtained promises, stopped the'
        ' mouths of lions, quenched the violence of fire, escaped the edge of the'
        ' sword, out of weakness were made strong, waxed valiant in fight, turned to'
        ' flight the armies of the aliens. Women received their dead raised to life'
        ' again; others were tortured, not accepting deliverance; some had trial of'
        ' cruel mockings and scourgings, of bonds and imprisonment; were stoned,'
        ' sawn asunder, slain with the sword; wandered about in sheepskins and'
        ' goatskins, being destitute, afflicted, tormented.',
    ),
]


def build_chart() -> Path:
    """Render the Hall of Faith table as a downloadable PNG image."""
    # Condensed deed text fits better in the chart than the full report text
    chart_entries: list[tuple[str, str, str]] = [
        ('4', 'Abel',
         'Offered unto God a more excellent sacrifice than Cain, and obtained'
         ' witness that he was righteous, God testifying of his gifts.'),
        ('5', 'Enoch',
         'Was translated that he should not see death; for before his translation'
         ' he had this testimony, that he pleased God.'),
        ('7', 'Noah',
         'Being warned of God of things not seen as yet, moved with fear, prepared'
         ' an ark to the saving of his house; condemned the world and became heir'
         ' of the righteousness which is by faith.'),
        ('8–10', 'Abraham',
         'Obeyed when called to go out to an inheritance; sojourned in the land of'
         ' promise as a stranger, looking for a city whose builder and maker is God.'),
        ('11', 'Sarah',
         'Received strength to conceive seed when past age, because she judged him'
         ' faithful who had promised.'),
        ('17–19', 'Abraham',
         'Offered up Isaac when tried; accounted that God was able to raise him from'
         ' the dead, from whence also he received him in a figure.'),
        ('20', 'Isaac', 'Blessed Jacob and Esau concerning things to come.'),
        ('21', 'Jacob',
         'Blessed both the sons of Joseph when dying, and worshipped, leaning upon'
         ' the top of his staff.'),
        ('22', 'Joseph',
         'Made mention of the departing of Israel and gave commandment concerning'
         ' his bones.'),
        ('23', "Moses' parents",
         'Hid Moses three months, because they saw he was a proper child, and were'
         " not afraid of the king's commandment."),
        ('24–26', 'Moses',
         "Refused to be called the son of Pharaoh's daughter, choosing affliction"
         ' with the people of God, esteeming the reproach of Christ greater riches'
         ' than the treasures in Egypt.'),
        ('27', 'Moses',
         'Forsook Egypt, not fearing the wrath of the king; endured as seeing him'
         ' who is invisible.'),
        ('28', 'Moses',
         'Kept the passover and the sprinkling of blood, lest he that destroyed the'
         ' firstborn should touch them.'),
        ('29', 'Israel',
         'Passed through the Red Sea as by dry land; which the Egyptians assaying'
         ' to do were drowned.'),
        ('30', 'Israel',
         'Compassed the walls of Jericho seven days; and the walls fell down.'),
        ('31', 'Rahab',
         'Perished not with them that believed not, when she had received the spies'
         ' with peace.'),
        ('32–38', 'Gideon, Barak, Samson,\nJephthah, David, Samuel,\nand the prophets',
         'Subdued kingdoms, wrought righteousness, obtained promises, stopped the'
         ' mouths of lions, quenched the violence of fire, escaped the sword, waxed'
         ' valiant in fight, turned to flight the armies of the aliens; others were'
         ' tortured, mocked, scourged, imprisoned, stoned, sawn asunder, slain with'
         ' the sword.'),
    ]

    DEED_WRAP = 70
    PERSON_WRAP = 18
    ROW_H_PER_LINE = 0.22
    HEADER_H = 0.40

    rows = []
    for v, p, d in chart_entries:
        p_wrapped = textwrap.fill(p, PERSON_WRAP)
        d_wrapped = textwrap.fill(d, DEED_WRAP)
        p_lines = len(p_wrapped.split('\n'))
        d_lines = len(d_wrapped.split('\n'))
        h = max(p_lines, d_lines, 1) * ROW_H_PER_LINE + 0.10
        rows.append((v, p_wrapped, d_wrapped, h))

    fig_w = 14.0
    title_h = 0.70
    footer_h = 0.25
    data_h = HEADER_H + sum(r[3] for r in rows)
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
    col_props = [0.065, 0.13, 0.805]
    col_x = [margin_l + sum(col_props[:i]) * usable_w for i in range(len(col_props) + 1)]

    def fig_frac(inches: float) -> float:
        return inches / fig_h

    fig.text(0.5, 1.0 - 0.18 / fig_h,
             'Hebrews 11 — Hall of Faith',
             ha='center', va='top', fontsize=16, fontweight='bold', color='#1A3A5C')
    fig.text(0.5, 1.0 - 0.46 / fig_h,
             'King James Version  ·  Hebrews 11:1–38',
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

    y_top = 1.0 - fig_frac(title_h)
    y = y_top
    h_h = fig_frac(HEADER_H)
    for i, label in enumerate(['Verse(s)', 'Person', 'What they did by faith']):
        draw_cell(col_x[i], col_x[i + 1], y - h_h, y, label,
                  HEADER_BG, HEADER_FG, fontsize=10, bold=True)
    y -= h_h

    for idx, (v, p, d, rh) in enumerate(rows):
        bg = ROW_BG_A if idx % 2 == 0 else ROW_BG_B
        rh_f = fig_frac(rh)
        draw_cell(col_x[0], col_x[1], y - rh_f, y, v, bg, '#111111', fontsize=9)
        draw_cell(col_x[1], col_x[2], y - rh_f, y, p, bg, '#111111', fontsize=9)
        draw_cell(col_x[2], col_x[3], y - rh_f, y, d, bg, '#222222', fontsize=8.5)
        y -= rh_f

    fig.text(0.5, footer_h / fig_h / 2, 'bereanbiblebots.com',
             ha='center', va='bottom', fontsize=8, color='#AAAAAA',
             transform=fig.transFigure)

    out = REPORT_DIR / 'hebrews11-hall-of-faith-chart.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'Saved {out}')
    return out


def build_report() -> Path:
    lines: list[str] = [
        '# Hebrews 11 — Hall of Faith',
        '',
        '**Text:** KJV · **Passage:** Hebrews 11:1–38',
        '',
        'The author of Hebrews opens the chapter by stating that "the elders'
        ' obtained a good report" through faith (v. 2), then surveys the'
        ' patriarchs and heroes of Israel as examples of what faith looks like'
        ' in practice. Each entry below notes the person, the verse(s) that'
        ' describe them, and what they did or endured "by faith."',
        '',
        '---',
        '',
        '| Verse(s) | Person | What they did by faith |',
        '|---|---|---|',
    ]

    for verses, person, deed in ENTRIES:
        # Collapse newlines in person field for the table cell
        person_cell = person.replace('\n', ' ')
        # Escape pipes in deed text
        deed_cell = deed.replace('|', '\\|')
        lines.append(f'| {verses} | {person_cell} | {deed_cell} |')

    lines += [
        '',
        '---',
        '',
        '## Downloadable Chart',
        '',
        'Right-click the image below and choose **Save image as…** to download'
        ' a high-resolution PNG suitable for printing or sharing.',
        '',
        '![Hebrews 11 Hall of Faith chart](hebrews11-hall-of-faith-chart.png)',
        '',
        '---',
        '',
        '*Text: King James Version (KJV).*',
        ' *Generated by'
        ' [scripts/nt/study-helps/build_hebrews11_hall_of_faith.py]'
        '(../../../../scripts/nt/study-helps/build_hebrews11_hall_of_faith.py).*',
    ]

    out = REPORT_DIR / 'hebrews11-hall-of-faith.md'
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Saved {out}')
    return out


if __name__ == '__main__':
    build_chart()
    build_report()
    print('Done.')
