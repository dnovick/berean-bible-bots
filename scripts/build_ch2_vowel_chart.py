#!/usr/bin/env python3
"""Build BBH Ch2 Hebrew Vowel Chart — landscape single-page PDF.

Output: data/lessons/bbh/ch2/ch2-vowel-chart.pdf
Run:    python scripts/build_ch2_vowel_chart.py
"""

import os
from typing import Any, Dict, List, Optional, Tuple, cast

from bidi.algorithm import get_display
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import landscape, LETTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# ── Output path ─────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.normpath(
    os.path.join(SCRIPT_DIR, '..', 'data', 'lessons', 'bbh', 'ch2',
                 'ch2-vowel-chart.pdf')
)

# ── Fonts ────────────────────────────────────────────────────────────────────

FONT_TTC = '/System/Library/Fonts/ArialHB.ttc'
FONT_HEB = 'ArialHebrew'
FONT_HEB_BOLD = 'ArialHebrewBold'
FONT_LATIN = 'Helvetica'
FONT_LATIN_BOLD = 'Helvetica-Bold'
FONT_LATIN_OBLIQUE = 'Helvetica-Oblique'


def _register_fonts() -> None:
    pdfmetrics.registerFont(TTFont(FONT_HEB, FONT_TTC, subfontIndex=0))
    pdfmetrics.registerFont(TTFont(FONT_HEB_BOLD, FONT_TTC, subfontIndex=1))


def _heb(s: str) -> str:
    """Apply bidi algorithm so RTL Hebrew renders correctly in ReportLab."""
    return str(get_display(s))


# ── Colors ───────────────────────────────────────────────────────────────────

C_HEADER_BG = HexColor('#2c4a7c')
C_HEADER_TEXT = white
C_SUBHDR_BG = HexColor('#4a6fa5')
C_CLASS_BG = HexColor('#dce8f5')
C_LONG_P_BG = HexColor('#fffbe6')
C_LONG_M_BG = HexColor('#fff0b3')
C_SHORT_BG = HexColor('#e8f5e9')
C_REDUCED_BG = HexColor('#fce4ec')
C_BORDER = HexColor('#888888')
C_INNER = HexColor('#cccccc')
C_TEXT = HexColor('#111111')
C_FOOTNOTE = HexColor('#555555')

# ── Page and layout ──────────────────────────────────────────────────────────

PAGE_W, PAGE_H = landscape(LETTER)   # 792 × 612
MARGIN_L = 36
MARGIN_R = 36
MARGIN_T = 26
MARGIN_B = 22

# Column x-positions and widths
TABLE_X = MARGIN_L
TABLE_W = PAGE_W - MARGIN_L - MARGIN_R   # 720

COL_WIDTHS = [55, 132, 190, 162, 181]    # sum = 720
COL_KEYS = ['class', 'long_plain', 'long_mater', 'short', 'reduced']
COL_COLORS = [C_CLASS_BG, C_LONG_P_BG, C_LONG_M_BG, C_SHORT_BG, C_REDUCED_BG]

# Compute cumulative x positions
COL_X = []
x = TABLE_X
for w in COL_WIDTHS:
    COL_X.append(x)
    x += w

# Font sizes
FS_TITLE = 16
FS_SUBTITLE = 10
FS_HEADER = 10
FS_SUBHDR = 8
FS_CLASS_LBL = 13
FS_HEB = 18
FS_NAME = 6.5
FS_FOOTNOTE = 7

# Cell layout metrics
CELL_PAD_V = 5     # top and bottom padding inside each data cell
HEB_H = 26         # approximate visual height of Hebrew glyph at FS_HEB
NAME_H = 8         # name text height at FS_NAME
HEB_NAME_GAP = 5   # gap between glyph baseline and name top
ENTRY_H = HEB_H + HEB_NAME_GAP + NAME_H   # ~35 pt per sub-entry
ENTRY_GAP = 5      # vertical gap between consecutive sub-entries in one cell

HDR_ROW_H = 24     # main header row height
SUBHDR_ROW_H = 16  # sub-header row height (Plain / Vowel Letter)

# ── Vowel data ───────────────────────────────────────────────────────────────────────────
# Each entry is (hebrew_unicode_str, 'Vowel Name')
# Shureq uses precomposed U+FB35 (WAW WITH DAGESH) for reliable dot placement.

ROWS = [
    {
        'class': 'a',
        'long_plain': [('בָּ', 'Qamets¹')],
        'long_mater': [('בָּה', 'Qamets He')],
        'short':      [('בַּ', 'Pathach')],
        'reduced':    [('בֲּ', 'Hateph Pathach')],
    },
    {
        'class': 'e',
        'long_plain': [('בֵּ', 'Tsere')],
        'long_mater': [
            ('בֵּה', 'Tsere He'),
            ('בֶּה', 'Seghol He'),
            ('בֵּי', 'Tsere Yod'),
            ('בֶּי', 'Seghol Yod'),
        ],
        'short':      [('בֶּ', 'Seghol')],
        'reduced':    [('בֱּ', 'Hateph Seghol')],
    },
    {
        'class': 'i',
        'long_plain': [],
        'long_mater': [('בִּי', 'Hireq Yod')],
        'short':      [('בִּ', 'Hireq')],
        'reduced':    [],
    },
    {
        'class': 'o',
        'long_plain': [('בֹּ', 'Holem')],
        'long_mater': [
            ('בּוֹ', 'Holem Vav'),
            ('בֹּה', 'Holem He'),
        ],
        'short':      [('בָּ', 'Qamets Hatuf¹')],
        'reduced':    [('בֳּ', 'Hateph Qamets')],
    },
    {
        'class': 'u',
        'long_plain': [],
        'long_mater': [('בּוּ', 'Shureq')],
        'short':      [('בֻּ', 'Qibbuts')],
        'reduced':    [],
    },
    {
        'class': '—',  # em-dash
        'long_plain': [],
        'long_mater': [],
        'short':      [],
        'reduced':    [('בְּ', 'Shewa²')],
    },
]


def _row_height(row: Dict[str, Any]) -> int:
    """Compute the height of a data row from its entries."""
    max_entries = max(
        len(row['long_plain']),
        len(row['long_mater']),
        len(row['short']),
        len(row['reduced']),
        1,
    )
    if max_entries == 1:
        return 2 * CELL_PAD_V + ENTRY_H
    return 2 * CELL_PAD_V + max_entries * ENTRY_H + (max_entries - 1) * ENTRY_GAP


# ── Drawing helpers ───────────────────────────────────────────────────────────

def _rect(c: Any, x: float, y: float, w: float, h: float,
          fill_color: Optional[Any] = None,
          stroke_color: Optional[Any] = None) -> None:
    """Draw a filled/stroked rectangle. y is ReportLab bottom-left y."""
    if fill_color:
        c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
    c.rect(x, y, w, h,
           fill=1 if fill_color else 0,
           stroke=1 if stroke_color else 0)


def _draw_entries(c: Any, entries: List[Tuple[str, str]],
                  cell_x: float, cell_w: float,
                  cell_top_y: float, cell_h: float,
                  bg_color: Any, is_class_col: bool = False,
                  class_label: Optional[str] = None) -> None:
    """Fill one cell background and draw its sub-entries (glyph + name).

    cell_top_y is the ReportLab y of the top of the cell.
    """
    cell_bottom_y = cell_top_y - cell_h

    # Background
    _rect(c, cell_x, cell_bottom_y, cell_w, cell_h, fill_color=bg_color)

    cell_cx = cell_x + cell_w / 2.0  # horizontal center

    if is_class_col:
        # Bold class letter(s) centered vertically
        c.setFillColor(HexColor('#2c4a7c'))
        c.setFont(FONT_LATIN_BOLD, FS_CLASS_LBL)
        label = class_label if class_label else ''
        text_y = cell_bottom_y + (cell_h - FS_CLASS_LBL) / 2.0 - 2
        c.drawCentredString(cell_cx, text_y, label)
        return

    if not entries:
        # Empty cell: draw a small em-dash
        c.setFillColor(HexColor('#bbbbbb'))
        c.setFont(FONT_LATIN, FS_NAME)
        c.drawCentredString(cell_cx, cell_bottom_y + cell_h / 2.0 - 3, '—')
        return

    # Calculate total block height for vertical centering
    n = len(entries)
    block_h = n * ENTRY_H + (n - 1) * ENTRY_GAP
    # Start y for first entry's Hebrew glyph top (ReportLab coords)
    start_y = cell_bottom_y + (cell_h + block_h) / 2.0   # top of first glyph

    for i, (heb_str, name) in enumerate(entries):
        entry_top = start_y - i * (ENTRY_H + ENTRY_GAP)

        # Hebrew glyph: baseline is entry_top - HEB_H + descender_adjust
        # ReportLab drawString y = baseline position
        glyph_baseline = entry_top - HEB_H + 5   # 5pt descender compensation
        c.setFillColor(C_TEXT)
        c.setFont(FONT_HEB, FS_HEB)
        c.drawCentredString(cell_cx, glyph_baseline, _heb(heb_str))

        # Name below the glyph
        name_y = glyph_baseline - HEB_NAME_GAP - NAME_H
        c.setFont(FONT_LATIN, FS_NAME)
        c.drawCentredString(cell_cx, name_y, name)


def _draw_cell_border(c: Any, x: float, y_bottom: float, w: float, h: float,
                      outer: bool = False) -> None:
    """Draw cell border lines."""
    lw = 1.2 if outer else 0.5
    c.setStrokeColor(C_BORDER if outer else C_INNER)
    c.setLineWidth(lw)
    c.rect(x, y_bottom, w, h, fill=0, stroke=1)


# ── Main build function ───────────────────────────────────────────────────────

def build() -> None:
    _register_fonts()

    c = canvas.Canvas(OUT_PATH, pagesize=landscape(LETTER))
    c.setTitle('BBH Chapter 2 — Hebrew Vowel Chart')
    c.setAuthor('Berean Bible Bots')

    # ── Title block ──────────────────────────────────────────────────────────
    title_y = PAGE_H - MARGIN_T - FS_TITLE
    c.setFillColor(HexColor('#2c4a7c'))
    c.setFont(FONT_LATIN_BOLD, FS_TITLE)
    c.drawCentredString(PAGE_W / 2.0, title_y, 'Hebrew Vowel Chart')

    sub_y = title_y - FS_TITLE - 2
    c.setFillColor(HexColor('#444444'))
    c.setFont(FONT_LATIN_OBLIQUE, FS_SUBTITLE)
    c.drawCentredString(PAGE_W / 2.0, sub_y,
                        'BBH Chapter 2  —  All Vowels by Class and Type')

    # ── Compute row heights and starting y ───────────────────────────────────
    row_heights = [_row_height(r) for r in ROWS]
    # Top of table: below title block
    table_top = sub_y - 10

    # ── Header row 1: main column labels ────────────────────────────────────
    hdr_top = table_top
    hdr_bottom = hdr_top - HDR_ROW_H

    header_labels = [
        (0, 1, 'Class'),
        (1, 2, 'Long Vowels'),
        (3, 1, 'Short Vowels'),
        (4, 1, 'Reduced Vowels'),
    ]

    for col_start, span, label in header_labels:
        x = COL_X[col_start]
        w = sum(COL_WIDTHS[col_start:col_start + span])
        _rect(c, x, hdr_bottom, w, HDR_ROW_H, fill_color=C_HEADER_BG)
        c.setFillColor(C_HEADER_TEXT)
        c.setFont(FONT_LATIN_BOLD, FS_HEADER)
        c.drawCentredString(x + w / 2.0, hdr_bottom + (HDR_ROW_H - FS_HEADER) / 2.0 - 1, label)

    # Outer border for header row 1
    c.setStrokeColor(C_BORDER)
    c.setLineWidth(1.0)
    c.rect(TABLE_X, hdr_bottom, TABLE_W, HDR_ROW_H, fill=0, stroke=1)
    # Inner separator between Long (span=2) and Short
    c.setLineWidth(0.5)
    c.setStrokeColor(C_INNER)
    c.line(COL_X[3], hdr_bottom, COL_X[3], hdr_top)
    c.line(COL_X[4], hdr_bottom, COL_X[4], hdr_top)
    c.line(COL_X[1], hdr_bottom, COL_X[1], hdr_top)

    # ── Header row 2: sub-labels ────────────────────────────────────────────
    subhdr_top = hdr_bottom
    subhdr_bottom = subhdr_top - SUBHDR_ROW_H

    subhdr_labels = [
        (0, ''),
        (1, 'Changeable'),
        (2, 'Vowel Letter (Mater Lectionis)'),
        (3, ''),
        (4, ''),
    ]
    for col_i, label in subhdr_labels:
        x = COL_X[col_i]
        w = COL_WIDTHS[col_i]
        bg = C_SUBHDR_BG if col_i in (1, 2) else C_HEADER_BG
        _rect(c, x, subhdr_bottom, w, SUBHDR_ROW_H, fill_color=bg)
        if label:
            c.setFillColor(C_HEADER_TEXT)
            c.setFont(FONT_LATIN_OBLIQUE, FS_SUBHDR)
            c.drawCentredString(x + w / 2.0,
                                subhdr_bottom + (SUBHDR_ROW_H - FS_SUBHDR) / 2.0 - 1,
                                label)

    c.setStrokeColor(C_BORDER)
    c.setLineWidth(1.0)
    c.rect(TABLE_X, subhdr_bottom, TABLE_W, SUBHDR_ROW_H, fill=0, stroke=1)
    c.setLineWidth(0.5)
    c.setStrokeColor(C_INNER)
    for ci in range(1, 5):
        c.line(COL_X[ci], subhdr_bottom, COL_X[ci], subhdr_top)

    # ── Data rows ────────────────────────────────────────────────────────────
    row_top = subhdr_bottom

    for row_idx, (row, rh) in enumerate(zip(ROWS, row_heights)):
        row_bottom = row_top - rh

        # Draw each column cell
        row_class: str = str(row['class'])
        class_lbl = row_class + '-class' if row_class != '—' else '—'
        for col_i, key in enumerate(COL_KEYS):
            cx = COL_X[col_i]
            cw = COL_WIDTHS[col_i]
            bg = COL_COLORS[col_i]

            if col_i == 0:
                _draw_entries(c, [], cx, cw, row_top, rh,
                              bg, is_class_col=True,
                              class_label=class_lbl)
            else:
                cell_entries = cast(List[Tuple[str, str]], row[key])
                _draw_entries(c, cell_entries, cx, cw, row_top, rh, bg)

        # Draw row borders
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(1.0)
        c.rect(TABLE_X, row_bottom, TABLE_W, rh, fill=0, stroke=1)
        c.setLineWidth(0.5)
        c.setStrokeColor(C_INNER)
        for ci in range(1, 5):
            c.line(COL_X[ci], row_bottom, COL_X[ci], row_top)

        row_top = row_bottom

    # ── Outer table border ───────────────────────────────────────────────────
    table_bottom = row_top
    c.setStrokeColor(HexColor('#333333'))
    c.setLineWidth(1.8)
    c.rect(TABLE_X, table_bottom,
           TABLE_W, table_top - table_bottom, fill=0, stroke=1)

    # ── Footnotes ────────────────────────────────────────────────────────────
    fn_y = table_bottom - 16   # 16 pt gap below table

    def _fn_segments(c: Any, x: float, y: float, segments: List[Tuple[Any, ...]]) -> None:
        """Draw mixed-font footnote text. segments: list of (text, font, size)."""
        cur_x = x
        for text, font, size in segments:
            c.setFont(font, size)
            c.drawString(cur_x, y, text)
            cur_x += c.stringWidth(text, font, size)

    c.setFillColor(C_FOOTNOTE)
    _fn_segments(c, TABLE_X, fn_y, [
        ('¹ Qamets Hatuf (', FONT_LATIN, FS_FOOTNOTE),
        ('בָּ', FONT_HEB, FS_FOOTNOTE + 1),
        (') has the same visual shape as Qamets but is a short o-class vowel; '
         'context determines which is intended.', FONT_LATIN, FS_FOOTNOTE),
    ])
    _fn_segments(c, TABLE_X, fn_y - 10, [
        ('² Shewa (', FONT_LATIN, FS_FOOTNOTE),
        ('בְּ', FONT_HEB, FS_FOOTNOTE + 1),
        (') has no vowel class; vocal Shewa is a reduced vowel, silent Shewa '
         'has zero value.', FONT_LATIN, FS_FOOTNOTE),
    ])

    c.save()
    print(f'Saved: {OUT_PATH}')


if __name__ == '__main__':
    build()
