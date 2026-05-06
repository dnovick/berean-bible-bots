"""
Generate fillable PDF passage exercises from structured exercise data.

Produces an AcroForm PDF with:
- Hebrew passage text (RTL, vowel-pointed, Arial Hebrew font)
- English translation line
- One AcroForm text field per parse cell (Conjugation, PGN, Root, Function)
- Correct answers embedded as hidden field default values, revealed via
  a "Show Answers" button (JavaScript AcroForm action)

Usage:
    from bible_grammar.exercise_pdf import ExercisePDF
    pdf = ExercisePDF(title, subtitle)
    pdf.add_passage(ref, hebrew, english)
    pdf.add_verb_table(verbs)   # list of VerbEntry
    pdf.add_section_break()
    pdf.save(output_path)

Or use build_ch26_exercise() to regenerate the Chapter 26 exercise directly.
"""

from dataclasses import dataclass
from typing import Optional
import os

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from bidi.algorithm import get_display

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
_FONTS_REGISTERED = False


def _register_fonts():
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return
    pdfmetrics.registerFont(TTFont('ArialHebrew',     '/System/Library/Fonts/ArialHB.ttc', subfontIndex=2))
    pdfmetrics.registerFont(TTFont('ArialHebrewBold', '/System/Library/Fonts/ArialHB.ttc', subfontIndex=3))
    _FONTS_REGISTERED = True


def _heb(text: str) -> str:
    """Apply bidi algorithm so ReportLab draws Hebrew glyphs left-to-right."""
    return get_display(text)


# ---------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------
C_HEADER_BG  = HexColor('#e8e8e8')
C_ANSWER_BG  = HexColor('#f0faf0')
C_ANSWER_FG  = HexColor('#2a6e2a')
C_WATCHOUT   = HexColor('#fff8e1')
C_WATCHOUT_B = HexColor('#f0a500')
C_FIELD_BG   = HexColor('#fafff8')
C_RULE       = HexColor('#cccccc')
C_HEADING    = HexColor('#333333')
C_REF        = HexColor('#444444')
C_NOTE_BG    = HexColor('#fff8e8')
C_NOTE_B     = HexColor('#e0c060')
C_SCORE_BG   = HexColor('#f5f0ff')
C_SCORE_B    = HexColor('#c0a8e8')

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class VerbEntry:
    num: str          # "1", "B1", etc.
    verb: str         # pointed Hebrew
    conj: str         # answer
    pgn:  str         # answer
    root: str         # answer (Hebrew)
    func: str         # answer


@dataclass
class PassageBlock:
    ref:     str
    hebrew:  str
    english: str
    watchout: Optional[str] = None   # optional warning note


@dataclass
class ContrastEntry:
    num:         str   # "1", "9", etc.
    root:        str   # Hebrew root
    qal:         str   # Qal gloss (Latin)
    hiphil_form: str   # Hebrew Hiphil form
    hiphil_conj: str   # conjugation label
    ref:         str
    translation: str   # answer: English translation
    function:    str   # answer: Causative / Factitive / Declarative / Simple Action
    answer_note: str   # one-line explanation


@dataclass
class NHEntry:
    num:         str   # item number
    heb:         str   # Hebrew form
    ref:         str   # reference
    context:     str   # fill-in-blank sentence
    stem:        str   # Niphal / Hiphil (answer)
    conj:        str   # conjugation (answer)
    pgn:         str   # person-gender-number (answer)
    root_class:  str   # "root · weak class" (answer)
    translation: str   # English translation (answer)
    note:        str   # one-line diagnostic note (answer)


@dataclass
class BGEntry:
    num:         str   # item number
    heb:         str   # Hebrew form
    ref:         str   # reference
    context:     str   # fill-in-blank sentence
    stem:        str   # Niphal / Hiphil (answer)
    conj:        str   # conjugation (answer)
    pgn:         str   # person-gender-number (answer)
    bg_class:    str   # Biconsonantal / Geminate (answer)
    root:        str   # root (answer)
    translation: str   # English translation (answer)
    note:        str   # one-line diagnostic note (answer)


@dataclass
class SortEntry:
    num:         str   # "1"–"24"
    heb:         str   # Hebrew form
    conj:        str   # conjugation label
    ref:         str
    gloss:       str   # contextual gloss
    function:    str   # answer: C / F / D / SA
    root:        str   # Hebrew root (unused in PDF answer; kept for reference)
    explanation: str   # one-line answer explanation

# ---------------------------------------------------------------------------
# Core PDF builder
# ---------------------------------------------------------------------------


class ExercisePDF:
    PAGE_W, PAGE_H = LETTER
    MARGIN_L = 0.75 * inch
    MARGIN_R = 0.75 * inch
    MARGIN_T = 0.85 * inch
    MARGIN_B = 0.75 * inch

    # Column widths for the parse table (proportional, sum = usable width)
    COL_RATIOS = [0.06, 0.13, 0.20, 0.10, 0.14, 0.30, 0.07]
    COL_HEADERS = ['#', 'Verb', 'Conjugation', 'PGN', 'Root', 'Function', '']

    ROW_H       = 0.30 * inch   # input row height
    ANSWER_H    = 0.26 * inch   # answer row height
    HEADER_H    = 0.22 * inch
    FIELD_PAD   = 3             # pts inside field border

    HEB_SIZE    = 13
    ENG_SIZE    = 9.5
    BODY_SIZE   = 9
    HEAD_SIZE   = 11
    SUBH_SIZE   = 9.5
    LABEL_SIZE  = 8

    def __init__(self, title: str, subtitle: str = ''):
        _register_fonts()
        self.title    = title
        self.subtitle = subtitle
        self._canvas  = None
        self._path    = None
        self._y       = 0.0
        self._page    = 0
        self._fields  = []   # (name, x, y, w, h, default_value, answer_value)
        self._field_idx = 0

    # ------------------------------------------------------------------ pages
    def _usable_w(self):
        return self.PAGE_W - self.MARGIN_L - self.MARGIN_R

    def _col_widths(self):
        w = self._usable_w()
        return [r * w for r in self.COL_RATIOS]

    def _new_page(self):
        if self._page > 0:
            self._canvas.showPage()
        self._page += 1
        self._y = self.PAGE_H - self.MARGIN_T
        self._draw_header()

    def _draw_header(self):
        c = self._canvas
        if self._page == 1:
            c.setFont('Helvetica-Bold', 14)
            c.setFillColor(C_HEADING)
            c.drawString(self.MARGIN_L, self._y, self.title)
            self._y -= 0.22 * inch
            if self.subtitle:
                c.setFont('Helvetica-Oblique', 9)
                c.setFillColor(HexColor('#666666'))
                c.drawString(self.MARGIN_L, self._y, self.subtitle)
                self._y -= 0.18 * inch
            # horizontal rule
            c.setStrokeColor(C_RULE)
            c.setLineWidth(1)
            c.line(self.MARGIN_L, self._y, self.PAGE_W - self.MARGIN_R, self._y)
            self._y -= 0.15 * inch
        else:
            c.setFont('Helvetica', 8)
            c.setFillColor(HexColor('#888888'))
            c.drawString(self.MARGIN_L, self._y, f'{self.title}  —  continued')
            c.drawRightString(self.PAGE_W - self.MARGIN_R, self._y, f'page {self._page}')
            self._y -= 0.22 * inch

    def _check_space(self, needed: float):
        if self._y - needed < self.MARGIN_B:
            self._new_page()

    # ---------------------------------------------------------------- helpers
    def _hline(self, y, color=C_RULE, width=0.5):
        self._canvas.setStrokeColor(color)
        self._canvas.setLineWidth(width)
        self._canvas.line(self.MARGIN_L, y, self.PAGE_W - self.MARGIN_R, y)

    def _wrapped_height(self, text: str, font: str, size: float, max_w: float) -> float:
        lines = simpleSplit(text, font, size, max_w)
        return len(lines) * (size + 2)

    def _draw_wrapped(self, text: str, font: str, size: float,
                       x: float, y: float, max_w: float, color=black) -> float:
        """Draw wrapped text, return new y (lower)."""
        c = self._canvas
        c.setFont(font, size)
        c.setFillColor(color)
        lines = simpleSplit(text, font, size, max_w)
        line_h = size + 2
        for line in lines:
            c.drawString(x, y, line)
            y -= line_h
        return y

    # -------------------------------------------------------- public sections
    def add_instructions(self, text: str):
        self._check_space(1.0 * inch)
        c = self._canvas
        w = self._usable_w()
        h = self._wrapped_height(text, 'Helvetica', self.BODY_SIZE, w - 0.2 * inch) + 0.2 * inch
        # box
        c.setFillColor(HexColor('#f8f8f0'))
        c.setStrokeColor(HexColor('#bbbbbb'))
        c.setLineWidth(0.5)
        c.rect(self.MARGIN_L, self._y - h, w, h, fill=1, stroke=1)
        self._y -= 0.1 * inch
        self._y = self._draw_wrapped(text, 'Helvetica', self.BODY_SIZE,
                                     self.MARGIN_L + 0.1 * inch, self._y,
                                     w - 0.2 * inch)
        self._y -= 0.15 * inch

    def add_section_heading(self, text: str):
        self._check_space(0.5 * inch)
        self._y -= 0.12 * inch
        self._canvas.setFont('Helvetica-Bold', self.HEAD_SIZE)
        self._canvas.setFillColor(C_HEADING)
        self._canvas.drawString(self.MARGIN_L, self._y, text)
        self._y -= (self.HEAD_SIZE + 4)
        self._hline(self._y + 2, color=HexColor('#aaaaaa'), width=0.75)
        self._y -= 0.08 * inch

    def add_section_break(self):
        self._check_space(0.3 * inch)
        self._y -= 0.12 * inch
        c = self._canvas
        c.setStrokeColor(HexColor('#cccccc'))
        c.setLineWidth(0.5)
        c.setDash(4, 4)
        c.line(self.MARGIN_L, self._y, self.PAGE_W - self.MARGIN_R, self._y)
        c.setDash()
        self._y -= 0.15 * inch

    def add_passage(self, block: PassageBlock):
        """Draw ref + Hebrew + English (+ optional watchout)."""
        c = self._canvas
        w = self._usable_w()

        # Estimate height needed
        heb_h = self._wrapped_height(_heb(block.hebrew), 'ArialHebrew',
                                      self.HEB_SIZE, w) + 4
        eng_h = self._wrapped_height(block.english, 'Helvetica-Oblique',
                                      self.ENG_SIZE, w) + 2
        wo_h  = 0
        if block.watchout:
            wo_h = self._wrapped_height(block.watchout, 'Helvetica',
                                         self.SUBH_SIZE, w - 0.2*inch) + 0.18*inch
        needed = 0.18*inch + heb_h + eng_h + wo_h + 0.1*inch
        self._check_space(needed)

        # Reference
        c.setFont('Helvetica-Bold', self.SUBH_SIZE)
        c.setFillColor(C_REF)
        c.drawString(self.MARGIN_L, self._y, block.ref)
        self._y -= (self.SUBH_SIZE + 3)

        # Hebrew — right-aligned RTL block
        heb_display = _heb(block.hebrew)
        lines = simpleSplit(heb_display, 'ArialHebrew', self.HEB_SIZE, w)
        line_h = self.HEB_SIZE + 4
        c.setFont('ArialHebrew', self.HEB_SIZE)
        c.setFillColor(black)
        for line in lines:
            c.drawRightString(self.MARGIN_L + w, self._y, line)
            self._y -= line_h
        self._y -= 2

        # English
        c.setFont('Helvetica-Oblique', self.ENG_SIZE)
        c.setFillColor(HexColor('#555555'))
        lines = simpleSplit(block.english, 'Helvetica-Oblique', self.ENG_SIZE, w)
        for line in lines:
            c.drawString(self.MARGIN_L, self._y, line)
            self._y -= (self.ENG_SIZE + 2)
        self._y -= 4

        # Watchout box
        if block.watchout:
            wo_lines = simpleSplit(block.watchout, 'Helvetica', self.SUBH_SIZE,
                                   w - 0.2*inch)
            box_h = len(wo_lines) * (self.SUBH_SIZE + 2) + 0.14*inch
            c.setFillColor(C_WATCHOUT)
            c.setStrokeColor(C_WATCHOUT_B)
            c.setLineWidth(2)
            c.rect(self.MARGIN_L, self._y - box_h, w, box_h, fill=1, stroke=0)
            c.setLineWidth(2)
            c.setStrokeColor(C_WATCHOUT_B)
            c.line(self.MARGIN_L, self._y - box_h,
                   self.MARGIN_L, self._y)
            self._y -= 0.07*inch
            c.setFont('Helvetica', self.SUBH_SIZE)
            c.setFillColor(black)
            for line in wo_lines:
                c.drawString(self.MARGIN_L + 0.1*inch, self._y, line)
                self._y -= (self.SUBH_SIZE + 2)
            self._y -= 0.08*inch

    def add_verb_table(self, verbs: list[VerbEntry], show_answers: bool = True):
        """Draw the parse table for one or more verbs."""
        cw = self._col_widths()
        x0 = self.MARGIN_L

        needed = self.HEADER_H + len(verbs) * (self.ROW_H + (self.ANSWER_H if show_answers else 0)) + 0.08*inch
        self._check_space(needed)

        c = self._canvas

        # Header row
        y = self._y
        c.setFillColor(C_HEADER_BG)
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.4)
        c.rect(x0, y - self.HEADER_H, sum(cw), self.HEADER_H, fill=1, stroke=1)
        cx = x0
        c.setFont('Helvetica-Bold', self.LABEL_SIZE)
        c.setFillColor(black)
        for i, (hdr, w) in enumerate(zip(self.COL_HEADERS, cw)):
            if hdr:
                c.drawString(cx + 3, y - self.HEADER_H + 5, hdr)
            cx += w
        y -= self.HEADER_H

        for verb in verbs:
            self._check_space(self.ROW_H + (self.ANSWER_H if show_answers else 0))
            # --- input row ---
            c.setStrokeColor(C_RULE)
            c.setLineWidth(0.4)
            c.rect(x0, y - self.ROW_H, sum(cw), self.ROW_H, fill=0, stroke=1)

            cx = x0
            c.setFont('Helvetica-Bold', self.LABEL_SIZE)
            c.setFillColor(HexColor('#666666'))
            c.drawCentredString(cx + cw[0]/2, y - self.ROW_H + 8, str(verb.num))
            cx += cw[0]

            c.setFont('ArialHebrewBold', self.HEB_SIZE - 1)
            c.setFillColor(black)
            c.drawRightString(cx + cw[1] - 3, y - self.ROW_H + 7, _heb(verb.verb))
            cx += cw[1]

            field_cols = [
                (cw[2], 'conj', verb.conj),
                (cw[3], 'pgn',  verb.pgn),
                (cw[4], 'root', verb.root),
                (cw[5], 'func', verb.func),
            ]
            for (fw, fname, fanswer) in field_cols:
                fid = f'{verb.num}-{fname}-{self._field_idx}'
                self._field_idx += 1
                fx = cx + self.FIELD_PAD
                fy = y - self.ROW_H + self.FIELD_PAD
                fw2 = fw - self.FIELD_PAD * 2
                fh  = self.ROW_H - self.FIELD_PAD * 2
                c.setFillColor(C_FIELD_BG)
                c.setStrokeColor(HexColor('#bbbbbb'))
                c.setLineWidth(0.5)
                c.rect(fx, fy, fw2, fh, fill=1, stroke=1)
                c.acroForm.textfield(
                    name=fid,
                    tooltip=f'{verb.num} {fname}',
                    x=fx, y=fy, width=fw2, height=fh,
                    borderStyle='underlined',
                    borderColor=HexColor('#bbbbbb'),
                    fillColor=C_FIELD_BG,
                    textColor=black,
                    fontSize=self.LABEL_SIZE,
                    fontName='Helvetica',
                    value='',
                    fieldFlags='',
                )
                cx += fw

            # col 6: hint label only when answers are inline
            if show_answers:
                c.setFont('Helvetica', 7)
                c.setFillColor(HexColor('#2a6e2a'))
                c.drawCentredString(cx + cw[6]/2, y - self.ROW_H + 8, 'see ↓')

            y -= self.ROW_H

            if show_answers:
                # --- answer row ---
                c.setFillColor(C_ANSWER_BG)
                c.setStrokeColor(C_RULE)
                c.setLineWidth(0.4)
                c.rect(x0, y - self.ANSWER_H, sum(cw), self.ANSWER_H, fill=1, stroke=1)

                cx = x0
                c.setFont('Helvetica-Bold', self.LABEL_SIZE)
                c.setFillColor(C_ANSWER_FG)
                c.drawCentredString(cx + cw[0]/2, y - self.ANSWER_H + 6, '✓')
                cx += cw[0]

                c.setFont('ArialHebrew', self.LABEL_SIZE)
                c.setFillColor(C_ANSWER_FG)
                c.drawRightString(cx + cw[1] - 3, y - self.ANSWER_H + 6, _heb(verb.verb))
                cx += cw[1]

                answers = [
                    (cw[2], verb.conj, False),
                    (cw[3], verb.pgn,  False),
                    (cw[4], verb.root, True),
                    (cw[5], verb.func, False),
                ]
                for (aw, atext, is_heb) in answers:
                    if is_heb:
                        c.setFont('ArialHebrew', self.LABEL_SIZE)
                        c.drawRightString(cx + aw - 3, y - self.ANSWER_H + 6, _heb(atext))
                    else:
                        c.setFont('Helvetica', self.LABEL_SIZE)
                        lines = simpleSplit(atext, 'Helvetica', self.LABEL_SIZE, aw - 6)
                        c.drawString(cx + 3, y - self.ANSWER_H + 6,
                                     lines[0] if lines else atext)
                    cx += aw

                y -= self.ANSWER_H

        self._y = y - 0.1 * inch

    def add_generic_table(self, headers: list, rows: list,
                          col_ratios: list = None,
                          heb_cols: list = None,
                          show_answers: bool = True,
                          answer_rows: list = None):
        """
        Draw a generic parse table with arbitrary columns.

        headers: column header strings
        rows: list of row data (each row is a list of strings, same length as headers)
        col_ratios: proportional widths (must sum to ~1.0); if None, equal widths
        heb_cols: indices of columns that contain Hebrew text (right-aligned, ArialHebrew font)
        show_answers: if True, draw green answer rows below each input row
        answer_rows: if show_answers, the answer data (same shape as rows); if None, answers = rows
        """
        if col_ratios is None:
            col_ratios = [1.0 / len(headers)] * len(headers)
        if heb_cols is None:
            heb_cols = []

        w = self._usable_w()
        cw = [r * w for r in col_ratios]
        x0 = self.MARGIN_L

        answer_data = answer_rows if answer_rows is not None else rows

        needed = self.HEADER_H + len(rows) * (self.ROW_H + (self.ANSWER_H if show_answers else 0)) + 0.08 * inch
        self._check_space(needed)

        c = self._canvas

        # Header row
        y = self._y
        c.setFillColor(C_HEADER_BG)
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.4)
        c.rect(x0, y - self.HEADER_H, sum(cw), self.HEADER_H, fill=1, stroke=1)
        cx = x0
        c.setFont('Helvetica-Bold', self.LABEL_SIZE)
        c.setFillColor(black)
        for hdr, col_w in zip(headers, cw):
            if hdr:
                c.drawString(cx + 3, y - self.HEADER_H + 5, hdr)
            cx += col_w
        y -= self.HEADER_H

        for row_idx, row in enumerate(rows):
            self._check_space(self.ROW_H + (self.ANSWER_H if show_answers else 0))

            # Input row
            c.setStrokeColor(C_RULE)
            c.setLineWidth(0.4)
            c.rect(x0, y - self.ROW_H, sum(cw), self.ROW_H, fill=0, stroke=1)

            cx = x0
            for col_idx, (cell, col_w) in enumerate(zip(row, cw)):
                if col_idx in heb_cols:
                    # Hebrew column — display text (no field), right-aligned
                    c.setFont('ArialHebrew', self.HEB_SIZE - 2)
                    c.setFillColor(black)
                    c.drawRightString(cx + col_w - 3, y - self.ROW_H + 7, _heb(cell))
                elif col_idx == 0:
                    # First column (usually item number) — display only
                    c.setFont('Helvetica-Bold', self.LABEL_SIZE)
                    c.setFillColor(HexColor('#666666'))
                    c.drawCentredString(cx + col_w / 2, y - self.ROW_H + 8, str(cell))
                else:
                    # Input field
                    fid = f'r{row_idx}-c{col_idx}-{self._field_idx}'
                    self._field_idx += 1
                    fx = cx + self.FIELD_PAD
                    fy = y - self.ROW_H + self.FIELD_PAD
                    fw2 = col_w - self.FIELD_PAD * 2
                    fh = self.ROW_H - self.FIELD_PAD * 2
                    c.setFillColor(C_FIELD_BG)
                    c.setStrokeColor(HexColor('#bbbbbb'))
                    c.setLineWidth(0.5)
                    c.rect(fx, fy, fw2, fh, fill=1, stroke=1)
                    c.acroForm.textfield(
                        name=fid,
                        tooltip=f'{headers[col_idx]} row {row_idx + 1}',
                        x=fx, y=fy, width=fw2, height=fh,
                        borderStyle='underlined',
                        borderColor=HexColor('#bbbbbb'),
                        fillColor=C_FIELD_BG,
                        textColor=black,
                        fontSize=self.LABEL_SIZE,
                        fontName='Helvetica',
                        value='',
                        fieldFlags='',
                    )
                cx += col_w

            y -= self.ROW_H

            if show_answers and answer_data:
                ans_row = answer_data[row_idx]
                c.setFillColor(C_ANSWER_BG)
                c.setStrokeColor(C_RULE)
                c.setLineWidth(0.4)
                c.rect(x0, y - self.ANSWER_H, sum(cw), self.ANSWER_H, fill=1, stroke=1)

                cx = x0
                for col_idx, (cell, col_w) in enumerate(zip(ans_row, cw)):
                    if col_idx == 0:
                        c.setFont('Helvetica-Bold', self.LABEL_SIZE)
                        c.setFillColor(C_ANSWER_FG)
                        c.drawCentredString(cx + col_w / 2, y - self.ANSWER_H + 6, '✓')
                    elif col_idx in heb_cols:
                        c.setFont('ArialHebrew', self.LABEL_SIZE)
                        c.setFillColor(C_ANSWER_FG)
                        c.drawRightString(cx + col_w - 3, y - self.ANSWER_H + 6, _heb(cell))
                    else:
                        c.setFont('Helvetica', self.LABEL_SIZE)
                        c.setFillColor(C_ANSWER_FG)
                        lines = simpleSplit(cell, 'Helvetica', self.LABEL_SIZE, col_w - 6)
                        c.drawString(cx + 3, y - self.ANSWER_H + 6, lines[0] if lines else cell)
                    cx += col_w

                y -= self.ANSWER_H

        self._y = y - 0.1 * inch

    def add_note(self, text: str):
        """Draw a note/info box."""
        c = self._canvas
        w = self._usable_w()
        h = self._wrapped_height(text, 'Helvetica', self.LABEL_SIZE,
                                  w - 0.2*inch) + 0.18*inch
        self._check_space(h + 0.1*inch)
        c.setFillColor(C_NOTE_BG)
        c.setStrokeColor(C_NOTE_B)
        c.setLineWidth(0.5)
        c.rect(self.MARGIN_L, self._y - h, w, h, fill=1, stroke=1)
        self._y -= 0.07*inch
        self._y = self._draw_wrapped(text, 'Helvetica', self.LABEL_SIZE,
                                     self.MARGIN_L + 0.1*inch, self._y,
                                     w - 0.2*inch, color=HexColor('#333333'))
        self._y -= 0.1*inch

    def add_score(self, text: str):
        c = self._canvas
        w = self._usable_w()
        h = 0.32 * inch
        self._check_space(h + 0.1*inch)
        c.setFillColor(C_SCORE_BG)
        c.setStrokeColor(C_SCORE_B)
        c.setLineWidth(0.5)
        c.rect(self.MARGIN_L, self._y - h, w, h, fill=1, stroke=1)
        self._y -= 0.09*inch
        c.setFont('Helvetica-Bold', self.BODY_SIZE)
        c.setFillColor(black)
        c.drawString(self.MARGIN_L + 0.1*inch, self._y, text)
        self._y -= (h - 0.09*inch + 0.1*inch)

    def add_coverage_table(self, rows: list[tuple[str, str]]):
        """Draw a simple 2-col coverage table."""
        c = self._canvas
        cw = [2.2*inch, self._usable_w() - 2.2*inch]
        row_h = 0.2*inch
        needed = row_h * (len(rows) + 1) + 0.2*inch
        self._check_space(needed)
        x0 = self.MARGIN_L
        y = self._y
        # header
        c.setFillColor(HexColor('#ddeeff'))
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.4)
        c.rect(x0, y - row_h, sum(cw), row_h, fill=1, stroke=1)
        c.setFont('Helvetica-Bold', self.LABEL_SIZE)
        c.setFillColor(black)
        c.drawString(x0+3, y-row_h+5, 'Conjugation')
        c.drawString(x0+cw[0]+3, y-row_h+5, 'Verbs')
        y -= row_h
        for conj, verbs in rows:
            c.setFillColor(white)
            c.setStrokeColor(C_RULE)
            c.rect(x0, y-row_h, sum(cw), row_h, fill=1, stroke=1)
            c.setFont('Helvetica', self.LABEL_SIZE)
            c.setFillColor(black)
            c.drawString(x0+3, y-row_h+5, conj)
            c.drawString(x0+cw[0]+3, y-row_h+5, verbs)
            y -= row_h
        self._y = y - 0.1*inch

    def add_contrast_table(self, entries: list['ContrastEntry'], show_answers: bool = True):
        """Draw a Qal-Hiphil contrast table with fillable Translation and Function columns."""
        c = self._canvas
        w = self._usable_w()
        # Columns: #, Root, Qal, Hiphil Form, Ref, Translation (field), Function (field)
        ratios = [0.05, 0.10, 0.22, 0.15, 0.10, 0.22, 0.16]
        cw = [r * w for r in ratios]
        headers = ['#', 'Root', 'Qal Meaning', 'Hiphil Form', 'Ref', 'Translation', 'Function']

        1 + (1 if show_answers else 0)
        needed = self.HEADER_H + len(entries) * (self.ROW_H + (self.ANSWER_H if show_answers else 0)) + 0.08*inch
        self._check_space(needed)
        y = self._y
        x0 = self.MARGIN_L

        # Header
        c.setFillColor(C_HEADER_BG)
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.4)
        c.rect(x0, y - self.HEADER_H, sum(cw), self.HEADER_H, fill=1, stroke=1)
        cx = x0
        c.setFont('Helvetica-Bold', self.LABEL_SIZE)
        c.setFillColor(black)
        for hdr, col_w in zip(headers, cw):
            c.drawString(cx + 3, y - self.HEADER_H + 5, hdr)
            cx += col_w
        y -= self.HEADER_H

        for e in entries:
            self._check_space(self.ROW_H + (self.ANSWER_H if show_answers else 0))
            # Input row
            c.setStrokeColor(C_RULE)
            c.setLineWidth(0.4)
            c.rect(x0, y - self.ROW_H, sum(cw), self.ROW_H, fill=0, stroke=1)
            cx = x0
            # #
            c.setFont('Helvetica-Bold', self.LABEL_SIZE)
            c.setFillColor(HexColor('#666666'))
            c.drawCentredString(cx + cw[0]/2, y - self.ROW_H + 8, e.num)
            cx += cw[0]
            # Root (Hebrew)
            c.setFont('ArialHebrewBold', self.HEB_SIZE - 2)
            c.setFillColor(black)
            c.drawRightString(cx + cw[1] - 3, y - self.ROW_H + 7, _heb(e.root))
            cx += cw[1]
            # Qal meaning
            c.setFont('Helvetica', self.LABEL_SIZE)
            c.setFillColor(black)
            lines = simpleSplit(e.qal, 'Helvetica', self.LABEL_SIZE, cw[2] - 6)
            c.drawString(cx + 3, y - self.ROW_H + 8, lines[0] if lines else e.qal)
            cx += cw[2]
            # Hiphil form (Hebrew)
            c.setFont('ArialHebrew', self.HEB_SIZE - 2)
            c.drawRightString(cx + cw[3] - 3, y - self.ROW_H + 8, _heb(e.hiphil_form))
            cx += cw[3]
            # Ref
            c.setFont('Helvetica', self.LABEL_SIZE)
            c.setFillColor(HexColor('#555555'))
            c.drawString(cx + 3, y - self.ROW_H + 8, e.ref)
            cx += cw[4]
            # Translation and Function fields
            for fname, fw in [('trans', cw[5]), ('func', cw[6])]:
                fid = f'ctr-{e.num}-{fname}-{self._field_idx}'
                self._field_idx += 1
                fx = cx + self.FIELD_PAD
                fy = y - self.ROW_H + self.FIELD_PAD
                fw2 = fw - self.FIELD_PAD * 2
                fh = self.ROW_H - self.FIELD_PAD * 2
                c.setFillColor(C_FIELD_BG)
                c.setStrokeColor(HexColor('#bbbbbb'))
                c.setLineWidth(0.5)
                c.rect(fx, fy, fw2, fh, fill=1, stroke=1)
                c.acroForm.textfield(
                    name=fid, tooltip=f'{e.num} {fname}',
                    x=fx, y=fy, width=fw2, height=fh,
                    borderStyle='underlined', borderColor=HexColor('#bbbbbb'),
                    fillColor=C_FIELD_BG, textColor=black,
                    fontSize=self.LABEL_SIZE, fontName='Helvetica',
                    value='', fieldFlags='',
                )
                cx += fw
            y -= self.ROW_H

            if show_answers:
                # Answer row immediately below
                c.setFillColor(C_ANSWER_BG)
                c.setStrokeColor(C_RULE)
                c.setLineWidth(0.4)
                c.rect(x0, y - self.ANSWER_H, sum(cw), self.ANSWER_H, fill=1, stroke=1)
                cx = x0
                c.setFont('Helvetica-Bold', self.LABEL_SIZE)
                c.setFillColor(C_ANSWER_FG)
                c.drawCentredString(cx + cw[0]/2, y - self.ANSWER_H + 6, '✓')
                cx += cw[0]
                c.setFont('ArialHebrew', self.LABEL_SIZE)
                c.drawRightString(cx + cw[1] - 3, y - self.ANSWER_H + 6, _heb(e.root))
                cx += cw[1]
                c.setFont('Helvetica', self.LABEL_SIZE)
                c.drawString(cx + 3, y - self.ANSWER_H + 6, e.qal[:28])
                cx += cw[2]
                c.setFont('ArialHebrew', self.LABEL_SIZE)
                c.drawRightString(cx + cw[3] - 3, y - self.ANSWER_H + 6, _heb(e.hiphil_form))
                cx += cw[3]
                c.setFont('Helvetica', self.LABEL_SIZE)
                c.setFillColor(C_ANSWER_FG)
                c.drawString(cx + 3, y - self.ANSWER_H + 6, e.ref)
                cx += cw[4]
                lines = simpleSplit(e.translation, 'Helvetica', self.LABEL_SIZE, cw[5] - 6)
                c.drawString(cx + 3, y - self.ANSWER_H + 6, lines[0] if lines else e.translation)
                cx += cw[5]
                lines = simpleSplit(e.function, 'Helvetica-Bold', self.LABEL_SIZE, cw[6] - 6)
                c.setFont('Helvetica-Bold', self.LABEL_SIZE)
                c.drawString(cx + 3, y - self.ANSWER_H + 6, lines[0] if lines else e.function)
                y -= self.ANSWER_H

        self._y = y - 0.08 * inch

    def add_answer_key_contrast(self, entries: list['ContrastEntry']):
        """Draw a compact answer key page for the contrast drill."""
        self._new_page()
        c = self._canvas
        w = self._usable_w()
        c.setFont('Helvetica-Bold', self.HEAD_SIZE)
        c.setFillColor(C_HEADING)
        c.drawString(self.MARGIN_L, self._y, 'Answer Key')
        self._y -= (self.HEAD_SIZE + 8)
        self._hline(self._y + 2, color=HexColor('#aaaaaa'), width=0.75)
        self._y -= 0.1*inch

        # Compact table: #, Root, Translation, Function, Explanation
        ratios = [0.05, 0.10, 0.25, 0.16, 0.44]
        cw = [r * w for r in ratios]
        headers = ['#', 'Root', 'Translation', 'Function', 'Explanation']
        row_h = 0.22 * inch

        c.setFillColor(C_HEADER_BG)
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.4)
        c.rect(self.MARGIN_L, self._y - self.HEADER_H, sum(cw), self.HEADER_H, fill=1, stroke=1)
        cx = self.MARGIN_L
        c.setFont('Helvetica-Bold', self.LABEL_SIZE)
        c.setFillColor(black)
        for hdr, col_w in zip(headers, cw):
            c.drawString(cx + 3, self._y - self.HEADER_H + 5, hdr)
            cx += col_w
        self._y -= self.HEADER_H

        for i, e in enumerate(entries):
            self._check_space(row_h)
            bg = C_ANSWER_BG if i % 2 == 0 else white
            c.setFillColor(bg)
            c.setStrokeColor(C_RULE)
            c.setLineWidth(0.3)
            c.rect(self.MARGIN_L, self._y - row_h, sum(cw), row_h, fill=1, stroke=1)
            cx = self.MARGIN_L
            c.setFont('Helvetica-Bold', self.LABEL_SIZE)
            c.setFillColor(C_ANSWER_FG)
            c.drawCentredString(cx + cw[0]/2, self._y - row_h + 6, e.num)
            cx += cw[0]
            c.setFont('ArialHebrew', self.LABEL_SIZE)
            c.drawRightString(cx + cw[1] - 3, self._y - row_h + 6, _heb(e.root))
            cx += cw[1]
            c.setFont('Helvetica', self.LABEL_SIZE)
            c.setFillColor(black)
            lines = simpleSplit(e.translation, 'Helvetica', self.LABEL_SIZE, cw[2] - 6)
            c.drawString(cx + 3, self._y - row_h + 6, lines[0] if lines else e.translation)
            cx += cw[2]
            c.setFont('Helvetica-Bold', self.LABEL_SIZE)
            c.setFillColor(C_ANSWER_FG)
            c.drawString(cx + 3, self._y - row_h + 6, e.function)
            cx += cw[3]
            c.setFont('Helvetica', self.LABEL_SIZE)
            c.setFillColor(HexColor('#444444'))
            lines = simpleSplit(e.answer_note, 'Helvetica', self.LABEL_SIZE, cw[4] - 6)
            c.drawString(cx + 3, self._y - row_h + 6, lines[0] if lines else e.answer_note)
            self._y -= row_h

        self._y -= 0.1 * inch

    def add_answer_key_sort(self, entries: list['SortEntry']):
        """Draw a compact answer key page for the function-sort exercise."""
        self._new_page()
        c = self._canvas
        w = self._usable_w()
        c.setFont('Helvetica-Bold', self.HEAD_SIZE)
        c.setFillColor(C_HEADING)
        c.drawString(self.MARGIN_L, self._y, 'Answer Key')
        self._y -= (self.HEAD_SIZE + 8)
        self._hline(self._y + 2, color=HexColor('#aaaaaa'), width=0.75)
        self._y -= 0.1*inch

        # Compact table: #, Hebrew, Ref, Function, Explanation
        ratios = [0.05, 0.12, 0.09, 0.10, 0.64]
        cw = [r * w for r in ratios]
        headers = ['#', 'Hebrew', 'Ref', 'Fn', 'Explanation']
        row_h = 0.20 * inch

        c.setFillColor(C_HEADER_BG)
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.4)
        c.rect(self.MARGIN_L, self._y - self.HEADER_H, sum(cw), self.HEADER_H, fill=1, stroke=1)
        cx = self.MARGIN_L
        c.setFont('Helvetica-Bold', self.LABEL_SIZE)
        c.setFillColor(black)
        for hdr, col_w in zip(headers, cw):
            c.drawString(cx + 3, self._y - self.HEADER_H + 5, hdr)
            cx += col_w
        self._y -= self.HEADER_H

        for i, e in enumerate(entries):
            self._check_space(row_h)
            bg = C_ANSWER_BG if i % 2 == 0 else white
            c.setFillColor(bg)
            c.setStrokeColor(C_RULE)
            c.setLineWidth(0.3)
            c.rect(self.MARGIN_L, self._y - row_h, sum(cw), row_h, fill=1, stroke=1)
            cx = self.MARGIN_L
            c.setFont('Helvetica-Bold', self.LABEL_SIZE)
            c.setFillColor(C_ANSWER_FG)
            c.drawCentredString(cx + cw[0]/2, self._y - row_h + 5, e.num)
            cx += cw[0]
            c.setFont('ArialHebrew', self.LABEL_SIZE)
            c.drawRightString(cx + cw[1] - 3, self._y - row_h + 5, _heb(e.heb))
            cx += cw[1]
            c.setFont('Helvetica', self.LABEL_SIZE)
            c.setFillColor(HexColor('#555555'))
            c.drawString(cx + 3, self._y - row_h + 5, e.ref)
            cx += cw[2]
            c.setFont('Helvetica-Bold', self.LABEL_SIZE)
            c.setFillColor(C_ANSWER_FG)
            c.drawCentredString(cx + cw[3]/2, self._y - row_h + 5, e.function)
            cx += cw[3]
            c.setFont('Helvetica', self.LABEL_SIZE)
            c.setFillColor(HexColor('#444444'))
            lines = simpleSplit(e.explanation, 'Helvetica', self.LABEL_SIZE, cw[4] - 6)
            c.drawString(cx + 3, self._y - row_h + 5, lines[0] if lines else e.explanation)
            self._y -= row_h

        self._y -= 0.1 * inch

    def add_sort_table(self, entries: list['SortEntry'], show_answers: bool = True):
        """Draw a semantic-function sorting table with a single fillable Function column."""
        c = self._canvas
        w = self._usable_w()
        # Columns: #, Hebrew, Conjugation, Ref, Gloss, Function (field)
        ratios = [0.05, 0.12, 0.18, 0.09, 0.46, 0.10]
        cw = [r * w for r in ratios]
        headers = ['#', 'Hebrew', 'Conjugation', 'Ref', 'Contextual Gloss', 'Function']

        needed = self.HEADER_H + len(entries) * (self.ROW_H + (self.ANSWER_H if show_answers else 0)) + 0.08*inch
        self._check_space(needed)
        y = self._y
        x0 = self.MARGIN_L

        # Header
        c.setFillColor(C_HEADER_BG)
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.4)
        c.rect(x0, y - self.HEADER_H, sum(cw), self.HEADER_H, fill=1, stroke=1)
        cx = x0
        c.setFont('Helvetica-Bold', self.LABEL_SIZE)
        c.setFillColor(black)
        for hdr, col_w in zip(headers, cw):
            c.drawString(cx + 3, y - self.HEADER_H + 5, hdr)
            cx += col_w
        y -= self.HEADER_H

        for e in entries:
            self._check_space(self.ROW_H + self.ANSWER_H)
            # Input row
            c.setStrokeColor(C_RULE)
            c.setLineWidth(0.4)
            c.rect(x0, y - self.ROW_H, sum(cw), self.ROW_H, fill=0, stroke=1)
            cx = x0
            c.setFont('Helvetica-Bold', self.LABEL_SIZE)
            c.setFillColor(HexColor('#666666'))
            c.drawCentredString(cx + cw[0]/2, y - self.ROW_H + 8, e.num)
            cx += cw[0]
            # Hebrew form
            c.setFont('ArialHebrewBold', self.HEB_SIZE - 2)
            c.setFillColor(black)
            c.drawRightString(cx + cw[1] - 3, y - self.ROW_H + 7, _heb(e.heb))
            cx += cw[1]
            # Conjugation
            c.setFont('Helvetica', self.LABEL_SIZE)
            lines = simpleSplit(e.conj, 'Helvetica', self.LABEL_SIZE, cw[2] - 6)
            c.drawString(cx + 3, y - self.ROW_H + 8, lines[0] if lines else e.conj)
            cx += cw[2]
            # Ref
            c.setFillColor(HexColor('#555555'))
            c.drawString(cx + 3, y - self.ROW_H + 8, e.ref)
            cx += cw[3]
            # Gloss
            c.setFillColor(black)
            lines = simpleSplit(e.gloss, 'Helvetica', self.LABEL_SIZE, cw[4] - 6)
            c.drawString(cx + 3, y - self.ROW_H + 8, lines[0] if lines else e.gloss)
            cx += cw[4]
            # Function field
            fid = f'sort-{e.num}-func-{self._field_idx}'
            self._field_idx += 1
            fx = cx + self.FIELD_PAD
            fy = y - self.ROW_H + self.FIELD_PAD
            fw2 = cw[5] - self.FIELD_PAD * 2
            fh = self.ROW_H - self.FIELD_PAD * 2
            c.setFillColor(C_FIELD_BG)
            c.setStrokeColor(HexColor('#bbbbbb'))
            c.setLineWidth(0.5)
            c.rect(fx, fy, fw2, fh, fill=1, stroke=1)
            c.acroForm.textfield(
                name=fid, tooltip=f'{e.num} function',
                x=fx, y=fy, width=fw2, height=fh,
                borderStyle='underlined', borderColor=HexColor('#bbbbbb'),
                fillColor=C_FIELD_BG, textColor=black,
                fontSize=self.LABEL_SIZE, fontName='Helvetica',
                value='', fieldFlags='',
            )
            y -= self.ROW_H

            if show_answers:
                c.setFillColor(C_ANSWER_BG)
                c.setStrokeColor(C_RULE)
                c.setLineWidth(0.4)
                c.rect(x0, y - self.ANSWER_H, sum(cw), self.ANSWER_H, fill=1, stroke=1)
                cx = x0
                c.setFont('Helvetica-Bold', self.LABEL_SIZE)
                c.setFillColor(C_ANSWER_FG)
                c.drawCentredString(cx + cw[0]/2, y - self.ANSWER_H + 6, '✓')
                cx += cw[0]
                c.setFont('ArialHebrew', self.LABEL_SIZE)
                c.drawRightString(cx + cw[1] - 3, y - self.ANSWER_H + 6, _heb(e.heb))
                cx += cw[1]
                c.setFont('Helvetica', self.LABEL_SIZE)
                c.drawString(cx + 3, y - self.ANSWER_H + 6, e.conj[:22])
                cx += cw[2]
                c.setFillColor(C_ANSWER_FG)
                c.drawString(cx + 3, y - self.ANSWER_H + 6, e.ref)
                cx += cw[3]
                lines = simpleSplit(e.explanation, 'Helvetica', self.LABEL_SIZE, cw[4] - 6)
                c.setFillColor(C_ANSWER_FG)
                c.drawString(cx + 3, y - self.ANSWER_H + 6, lines[0] if lines else e.explanation)
                cx += cw[4]
                c.setFont('Helvetica-Bold', self.LABEL_SIZE)
                c.drawString(cx + 3, y - self.ANSWER_H + 6, e.function)
                y -= self.ANSWER_H

        self._y = y - 0.08 * inch

    def add_nh_table(self, entries: list['NHEntry'], show_answers: bool = True):
        """Draw a Niphal-Hiphil contrast table with fillable Stem/Conjugation/PGN/Root columns."""
        c = self._canvas
        w = self._usable_w()
        ratios = [0.04, 0.10, 0.08, 0.28, 0.10, 0.14, 0.08, 0.18]
        cw = [r * w for r in ratios]
        headers = ['#', 'Form', 'Ref', 'Context', 'Stem', 'Conjugation', 'PGN', 'Root / Class']

        needed = self.HEADER_H + len(entries) * (self.ROW_H + (self.ANSWER_H if show_answers else 0)) + 0.08*inch
        self._check_space(needed)
        y = self._y
        x0 = self.MARGIN_L

        c.setFillColor(C_HEADER_BG)
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.4)
        c.rect(x0, y - self.HEADER_H, sum(cw), self.HEADER_H, fill=1, stroke=1)
        cx = x0
        c.setFont('Helvetica-Bold', self.LABEL_SIZE)
        c.setFillColor(black)
        for hdr, col_w in zip(headers, cw):
            c.drawString(cx + 3, y - self.HEADER_H + 5, hdr)
            cx += col_w
        y -= self.HEADER_H

        for e in entries:
            self._check_space(self.ROW_H + (self.ANSWER_H if show_answers else 0))
            c.setStrokeColor(C_RULE)
            c.setLineWidth(0.4)
            c.rect(x0, y - self.ROW_H, sum(cw), self.ROW_H, fill=0, stroke=1)
            cx = x0
            c.setFont('Helvetica-Bold', self.LABEL_SIZE)
            c.setFillColor(HexColor('#666666'))
            c.drawCentredString(cx + cw[0]/2, y - self.ROW_H + 8, e.num)
            cx += cw[0]
            c.setFont('ArialHebrewBold', self.HEB_SIZE - 2)
            c.setFillColor(black)
            c.drawRightString(cx + cw[1] - 3, y - self.ROW_H + 7, _heb(e.heb))
            cx += cw[1]
            c.setFont('Helvetica', self.LABEL_SIZE)
            c.setFillColor(HexColor('#555555'))
            c.drawString(cx + 3, y - self.ROW_H + 8, e.ref)
            cx += cw[2]
            c.setFillColor(black)
            lines = simpleSplit(e.context, 'Helvetica', self.LABEL_SIZE, cw[3] - 6)
            c.drawString(cx + 3, y - self.ROW_H + 8, lines[0] if lines else e.context)
            cx += cw[3]
            for col_w in cw[4:]:
                fid = f'nh-{e.num}-{self._field_idx}'
                self._field_idx += 1
                fx = cx + self.FIELD_PAD
                fy = y - self.ROW_H + self.FIELD_PAD
                fw2 = col_w - self.FIELD_PAD * 2
                fh = self.ROW_H - self.FIELD_PAD * 2
                c.setFillColor(C_FIELD_BG)
                c.setStrokeColor(HexColor('#bbbbbb'))
                c.setLineWidth(0.5)
                c.rect(fx, fy, fw2, fh, fill=1, stroke=1)
                c.acroForm.textfield(
                    name=fid, tooltip=fid,
                    x=fx, y=fy, width=fw2, height=fh,
                    borderStyle='underlined', borderColor=HexColor('#bbbbbb'),
                    fillColor=C_FIELD_BG, textColor=black,
                    fontSize=self.LABEL_SIZE, fontName='Helvetica',
                    value='', fieldFlags='',
                )
                cx += col_w
            y -= self.ROW_H

            if show_answers:
                c.setFillColor(C_ANSWER_BG)
                c.setStrokeColor(C_RULE)
                c.setLineWidth(0.4)
                c.rect(x0, y - self.ANSWER_H, sum(cw), self.ANSWER_H, fill=1, stroke=1)
                cx = x0
                c.setFont('Helvetica-Bold', self.LABEL_SIZE)
                c.setFillColor(C_ANSWER_FG)
                c.drawCentredString(cx + cw[0]/2, y - self.ANSWER_H + 6, '✓')
                cx += cw[0]
                c.setFont('ArialHebrew', self.LABEL_SIZE)
                c.drawRightString(cx + cw[1] - 3, y - self.ANSWER_H + 6, _heb(e.heb))
                cx += cw[1] + cw[2]
                c.setFont('Helvetica', self.LABEL_SIZE)
                answer_text = f'{e.stem} · {e.conj} · {e.pgn} · {e.root_class} — {e.translation}'
                lines = simpleSplit(answer_text, 'Helvetica', self.LABEL_SIZE, sum(cw[3:]) - 6)
                c.drawString(cx + 3, y - self.ANSWER_H + 6, lines[0] if lines else answer_text)
                y -= self.ANSWER_H

        self._y = y - 0.08 * inch

    def add_bg_table(self, entries: list['BGEntry'], show_answers: bool = True):
        """Draw a Biconsonantal/Geminate drill table with 5 fillable fields per row."""
        c = self._canvas
        w = self._usable_w()
        ratios = [0.04, 0.10, 0.08, 0.24, 0.10, 0.12, 0.08, 0.12, 0.12]
        cw = [r * w for r in ratios]
        headers = ['#', 'Form', 'Ref', 'Context', 'Stem', 'Conjugation', 'PGN', 'Class', 'Root']

        needed = self.HEADER_H + len(entries) * (self.ROW_H + (self.ANSWER_H if show_answers else 0)) + 0.08*inch
        self._check_space(needed)
        y = self._y
        x0 = self.MARGIN_L

        c.setFillColor(C_HEADER_BG)
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.4)
        c.rect(x0, y - self.HEADER_H, sum(cw), self.HEADER_H, fill=1, stroke=1)
        cx = x0
        c.setFont('Helvetica-Bold', self.LABEL_SIZE)
        c.setFillColor(black)
        for hdr, col_w in zip(headers, cw):
            c.drawString(cx + 3, y - self.HEADER_H + 5, hdr)
            cx += col_w
        y -= self.HEADER_H

        for e in entries:
            self._check_space(self.ROW_H + (self.ANSWER_H if show_answers else 0))
            c.setStrokeColor(C_RULE)
            c.setLineWidth(0.4)
            c.rect(x0, y - self.ROW_H, sum(cw), self.ROW_H, fill=0, stroke=1)
            cx = x0
            c.setFont('Helvetica-Bold', self.LABEL_SIZE)
            c.setFillColor(HexColor('#666666'))
            c.drawCentredString(cx + cw[0]/2, y - self.ROW_H + 8, e.num)
            cx += cw[0]
            c.setFont('ArialHebrewBold', self.HEB_SIZE - 2)
            c.setFillColor(black)
            c.drawRightString(cx + cw[1] - 3, y - self.ROW_H + 7, _heb(e.heb))
            cx += cw[1]
            c.setFont('Helvetica', self.LABEL_SIZE)
            c.setFillColor(HexColor('#555555'))
            c.drawString(cx + 3, y - self.ROW_H + 8, e.ref)
            cx += cw[2]
            c.setFillColor(black)
            lines = simpleSplit(e.context, 'Helvetica', self.LABEL_SIZE, cw[3] - 6)
            c.drawString(cx + 3, y - self.ROW_H + 8, lines[0] if lines else e.context)
            cx += cw[3]
            for col_w in cw[4:]:
                fid = f'bg-{e.num}-{self._field_idx}'
                self._field_idx += 1
                fx = cx + self.FIELD_PAD
                fy = y - self.ROW_H + self.FIELD_PAD
                fw2 = col_w - self.FIELD_PAD * 2
                fh = self.ROW_H - self.FIELD_PAD * 2
                c.setFillColor(C_FIELD_BG)
                c.setStrokeColor(HexColor('#bbbbbb'))
                c.setLineWidth(0.5)
                c.rect(fx, fy, fw2, fh, fill=1, stroke=1)
                c.acroForm.textfield(
                    name=fid, tooltip=fid,
                    x=fx, y=fy, width=fw2, height=fh,
                    borderStyle='underlined', borderColor=HexColor('#bbbbbb'),
                    fillColor=C_FIELD_BG, textColor=black,
                    fontSize=self.LABEL_SIZE, fontName='Helvetica',
                    value='', fieldFlags='',
                )
                cx += col_w
            y -= self.ROW_H

            if show_answers:
                c.setFillColor(C_ANSWER_BG)
                c.setStrokeColor(C_RULE)
                c.setLineWidth(0.4)
                c.rect(x0, y - self.ANSWER_H, sum(cw), self.ANSWER_H, fill=1, stroke=1)
                cx = x0
                c.setFont('Helvetica-Bold', self.LABEL_SIZE)
                c.setFillColor(C_ANSWER_FG)
                c.drawCentredString(cx + cw[0]/2, y - self.ANSWER_H + 6, '✓')
                cx += cw[0]
                c.setFont('ArialHebrew', self.LABEL_SIZE)
                c.drawRightString(cx + cw[1] - 3, y - self.ANSWER_H + 6, _heb(e.heb))
                cx += cw[1] + cw[2]
                c.setFont('Helvetica', self.LABEL_SIZE)
                answer_text = f'{e.stem} · {e.conj} · {e.pgn} · {e.bg_class} · {e.root} — {e.translation}'
                lines = simpleSplit(answer_text, 'Helvetica', self.LABEL_SIZE, sum(cw[3:]) - 6)
                c.drawString(cx + 3, y - self.ANSWER_H + 6, lines[0] if lines else answer_text)
                y -= self.ANSWER_H

        self._y = y - 0.08 * inch

    def add_reflection(self, questions: list[str]):
        self._check_space(0.4*inch)
        c = self._canvas
        w = self._usable_w()
        c.setFont('Helvetica-Bold', self.HEAD_SIZE)
        c.setFillColor(C_HEADING)
        c.drawString(self.MARGIN_L, self._y, 'Reflection Questions')
        self._y -= (self.HEAD_SIZE + 6)
        for i, q in enumerate(questions, 1):
            needed = self._wrapped_height(q, 'Helvetica', self.BODY_SIZE,
                                           w - 0.3*inch) + 6
            self._check_space(needed)
            c.setFont('Helvetica-Bold', self.BODY_SIZE)
            c.setFillColor(black)
            c.drawString(self.MARGIN_L, self._y, f'{i}.')
            self._y = self._draw_wrapped(q, 'Helvetica', self.BODY_SIZE,
                                          self.MARGIN_L + 0.2*inch, self._y,
                                          w - 0.3*inch)
            self._y -= 6

    # -------------------------------------------------------- save
    def save(self, path: str):
        self._path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._canvas = canvas.Canvas(path, pagesize=LETTER)
        self._canvas.setTitle(self.title)
        self._canvas.setAuthor('Bible Grammar Stats')
        self._canvas.setSubject('Biblical Hebrew Passage Exercise')
        self._page = 0
        self._y = 0.0
        self._field_idx = 0
        self._new_page()
        self._build()
        self._canvas.save()
        return path

    def _build(self):
        raise NotImplementedError('Subclass must implement _build()')


# ---------------------------------------------------------------------------
# PassageExercise — shared "Spot the Stem" exercise scaffold
#
# Subclasses must:
#   • set  _instructions: str  (class attribute)
#   • implement  _render_passages(self, show_answers: bool)
#
# _build() is final: instructions → question pass → answer-key page → answer pass.
# ---------------------------------------------------------------------------
class PassageExercise(ExercisePDF):
    _instructions: str = ''

    def _render_passages(self, show_answers: bool):
        raise NotImplementedError('Subclass must implement _render_passages()')

    def _build(self):
        self.add_instructions(self._instructions)
        self._render_passages(show_answers=False)

        self._new_page()
        c = self._canvas
        c.setFont('Helvetica-Bold', 14)
        c.setFillColor(C_HEADING)
        c.drawString(self.MARGIN_L, self._y, 'Answer Key')
        self._y -= 0.22 * inch
        c.setFont('Helvetica-Oblique', 9)
        c.setFillColor(HexColor('#666666'))
        c.drawString(self.MARGIN_L, self._y,
                     'Passages with correct answers shown in the green row below each verb.')
        self._y -= 0.18 * inch
        c.setStrokeColor(C_RULE)
        c.setLineWidth(1)
        c.line(self.MARGIN_L, self._y, self.PAGE_W - self.MARGIN_R, self._y)
        self._y -= 0.15 * inch
        self._render_passages(show_answers=True)


# ---------------------------------------------------------------------------
# Chapter 26 exercise
# ---------------------------------------------------------------------------
class Ch26Exercise(PassageExercise):
    _instructions = (
        'Most highlighted verbs are Hiphil forms. For each one, first answer '
        'Is it Hiphil? (Yes / No). If Yes: fill in Conjugation, PGN, Root, and Function. '
        'If No: identify the correct stem and parse fully. '
        'Distractor verbs D1–D3 are not Hiphil — drawn from Qal and Niphal already studied. '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool):
        """Render all passages and verb tables; called twice (questions-only, then with answers)."""

        # ── Passage A ────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Genesis 6:12–20')

        self.add_passage(PassageBlock(
            '6:12',
            'וַיַּרְא אֱלֹהִים אֶת־הָאָרֶץ וְהִנֵּה נִשְׁחָתָה כִּי־הִשְׁחִית כָּל־בָּשָׂר אֶת־דַּרְכּוֹ עַל־הָאָרֶץ',
            '"And God saw the earth, and behold, it [D1] ____; for all flesh had [1] ____ its way upon the earth."'))
        self.add_verb_table([
            VerbEntry('D1', 'נִשְׁחָתָה', 'Weqatal', '3fs', 'שָׁחַת', 'NOT Hiphil — Niphal passive: it was corrupt; נִ- prefix = Niphal, not הִ- Hiphil'),
            VerbEntry('1', 'הִשְׁחִית', 'Perfect (qatal)', '3ms', 'שָׁחַת', 'Causative — had corrupted'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock(
            '6:13',
            'הִנְנִי מַשְׁחִיתָם עִם־הָאָרֶץ',
            '"Behold, I am [2] ____ them with the earth."'))
        self.add_verb_table([VerbEntry('2', 'מַשְׁחִיתָם', 'Participle + 3mp suffix', 'ms', 'שָׁחַת', 'Causative — destroying them')], show_answers=show_answers)

        self.add_passage(PassageBlock(
            '6:17',
            'וַאֲנִי הִנְנִי מֵבִיא אֶת־הַמַּבּוּל מַיִם עַל־הָאָרֶץ',
            '"As for me, behold, I am [3] ____ the flood of waters upon the earth."'))
        self.add_verb_table([VerbEntry('3', 'מֵבִיא', 'Participle', 'ms', 'בּוֹא', 'Causative — bringing')], show_answers=show_answers)

        self.add_passage(PassageBlock(
            '6:18',
            'וַהֲקִמֹתִי אֶת־בְּרִיתִי אִתָּךְ',
            '"But I will [4] ____ my covenant with you."'))
        self.add_verb_table([VerbEntry('4', 'וַהֲקִמֹתִי', 'Weqatal', '1cs', 'קוּם', 'Factitive — I will establish')], show_answers=show_answers)

        self.add_passage(PassageBlock(
            '6:19',
            'מִכָּל־בָּשָׂר שְׁנַיִם מִכֹּל תָּבִיא אֶל־הַתֵּבָה',
            '"Of every living thing you shall [5] ____ two of every kind into the ark."'))
        self.add_verb_table([VerbEntry('5', 'תָּבִיא', 'Imperfect', '2ms', 'בּוֹא', 'Causative — you shall bring')], show_answers=show_answers)

        self.add_passage(PassageBlock(
            '6:19–20',
            'לְהַחֲיֹת אִתָּךְ … לְהַחֲיוֹת',
            '"to [6] ____ them alive with you … to [7] ____ them"'))
        self.add_verb_table([
            VerbEntry('6', 'לְהַחֲיֹת', 'Inf. Construct', '—', 'חָיָה', 'Causative — to keep alive'),
            VerbEntry('7', 'לְהַחֲיוֹת', 'Inf. Construct', '—', 'חָיָה', 'Causative — to keep alive'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Genesis 7:4')

        self.add_passage(PassageBlock(
            '7:4',
            'כִּי לְיָמִים עוֹד שִׁבְעָה אָנֹכִי מַמְטִיר עַל־הָאָרֶץ אַרְבָּעִים יוֹם',
            '"For in seven days I will [8] ____ rain on the earth forty days."'))
        self.add_verb_table([VerbEntry('8', 'מַמְטִיר', 'Participle', 'ms', 'מָטַר', 'Causative/Denominative — causing rain')], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Genesis 8:1–21')

        self.add_passage(PassageBlock('8:1', 'וַיַּעֲבֵר אֱלֹהִים רוּחַ עַל־הָאָרֶץ',
            '"And God [9] ____ a wind over the earth."'))
        self.add_verb_table([VerbEntry('9', 'וַיַּעֲבֵר', 'Wayyiqtol', '3ms', 'עָבַר', 'Causative — caused to pass over')], show_answers=show_answers)

        self.add_passage(PassageBlock('8:9', 'וַיָּבֵא אֹתָהּ אֵלָיו אֶל־הַתֵּבָה',
            '"And he [10] ____ her back to him into the ark."'))
        self.add_verb_table([VerbEntry('10', 'וַיָּבֵא', 'Wayyiqtol', '3ms', 'בּוֹא', 'Causative — brought')], show_answers=show_answers)

        self.add_passage(PassageBlock('8:13', 'וַיָּסַר נֹחַ אֶת־מִכְסֵה הַתֵּבָה',
            '"And Noah [11] ____ the covering of the ark."'))
        self.add_verb_table([VerbEntry('11', 'וַיָּסַר', 'Wayyiqtol', '3ms', 'סוּר', 'Causative — removed')], show_answers=show_answers)

        self.add_passage(PassageBlock('8:17', 'הַיְצֵא אִתָּךְ כָּל־הַחַיָּה',
            '"[12] ____ with you every living thing."'))
        self.add_verb_table([VerbEntry('12', 'הַיְצֵא', 'Imperative', '2ms', 'יָצָא', 'Causative — bring out!')], show_answers=show_answers)

        self.add_passage(PassageBlock('8:20', 'וַיַּעַל עֹלֹת בַּמִּזְבֵּחַ',
            '"And he [13] ____ burnt offerings on the altar."'))
        self.add_verb_table([VerbEntry('13', 'וַיַּעַל', 'Wayyiqtol', '3ms', 'עָלָה', 'Causative — offered up')], show_answers=show_answers)

        self.add_passage(PassageBlock('8:21', 'לֹא־אֹסִף לְהַכֹּת אֶת־כָּל־חַי',
            '"I will never again [14] ____ every living thing."'))
        self.add_verb_table([VerbEntry('14', 'לְהַכֹּת', 'Inf. Construct', '—', 'נָכָה', 'Causative — to strike down')], show_answers=show_answers)

        self.add_section_break()

        # ── Passage D ────────────────────────────────────────────────────────
        self.add_section_heading('Passage D — Genesis 22:17  (Infinitive Absolute)')

        self.add_passage(PassageBlock(
            '22:17',
            'כִּי בָרֵךְ אֲבָרֶכְךָ וְהַרְבָּה אַרְבֶּה אֶת־זַרְעֲךָ כְּכוֹכְבֵי הַשָּׁמַיִם',
            '"For I will surely bless you, and I will [15] ____ [16] ____ your offspring as the stars of heaven."',
            watchout='Watch out: בָּרֵךְ and אֲבָרֶכְךָ are Piel forms of בָּרַךְ ("to bless") — not Hiphil. Parse only verbs 15–16.'))
        self.add_verb_table([
            VerbEntry('15', 'וְהַרְבָּה', 'Inf. Absolute', '—', 'רָבָה', 'Causative — emphatic modifier (surely/multiplying)'),
            VerbEntry('16', 'אַרְבֶּה',  'Imperfect',   '1cs', 'רָבָה', 'Causative — I will multiply'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage E ────────────────────────────────────────────────────────
        self.add_section_heading('Passage E — Deuteronomy 7:2  (Weqatal + Emphatic Pair)')

        self.add_passage(PassageBlock(
            '7:2',
            'וּנְתָנָם יְהוָה אֱלֹהֶיךָ לְפָנֶיךָ וְהִכִּיתָם הַכֵּה תַכֶּה לֹא־תִכְרֹת לָהֶם בְּרִית',
            '"When the LORD your God [D2] ____ them over, you shall [17] ____ them — [18] ____ [19] ____ them — [D3] ____ no covenant with them."'))
        self.add_verb_table([
            VerbEntry('D2', 'וּנְתָנָם', 'Weqatal',      '3ms', 'נָתַן', 'NOT Hiphil — Qal: and he gives/gives over; וּ + Qal perfect/weqatal; no הִ- prefix'),
            VerbEntry('17', 'וְהִכִּיתָם', 'Weqatal',    '2ms', 'נָכָה', 'Causative — and you shall strike them'),
            VerbEntry('18', 'הַכֵּה',    'Inf. Absolute', '—', 'נָכָה', 'Causative — emphatic modifier (certainly)'),
            VerbEntry('19', 'תַכֶּה',    'Imperfect',    '2ms', 'נָכָה', 'Causative — you shall strike'),
            VerbEntry('D3', 'תִכְרֹת',  'Imperfect',    '2ms', 'כָּרַת', 'NOT Hiphil — Qal: you shall cut (covenant); plain Qal imperfect; no הַ- Hiphil prefix'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Bonus ─────────────────────────────────────────────────────────────
        self.add_section_heading('Bonus — Genesis 6:1, 6:10')

        self.add_passage(PassageBlock('6:1', 'כִּי־הֵחֵל הָאָדָם לָרֹב', '"When man began to multiply…"'))
        self.add_passage(PassageBlock('6:10', 'וַיּוֹלֶד נֹחַ שְׁלֹשָׁה בָנִים', '"And Noah fathered three sons."'))
        self.add_verb_table([
            VerbEntry('B1', 'הֵחֵל',    'Perfect (qatal)', '3ms', 'חָלַל', 'Causative — began (Hiphil of חָלַל = to begin)'),
            VerbEntry('B2', 'וַיּוֹלֶד', 'Wayyiqtol',      '3ms', 'יָלַד', 'Causative — fathered / begat'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Notes + Score ─────────────────────────────────────────────────────
        self.add_note(
            'Note: #1 (הִשְׁחִית) and B1 (הֵחֵל) are Perfect (qatal), not Weqatal — both follow כִּי '
            'with no waw prefix. #15–16 and #18–19 illustrate the emphatic inf. absolute + imperfect '
            'construction: the inf. absolute intensifies the finite verb ("shall certainly strike"). '
            'D1 (נִשְׁחָתָה) is Niphal of the same root as #1 — compare: Niphal נִ- vs. Hiphil הִ-.'
        )
        self.add_score(
            'Score: 19 main + 2 bonus = 21 total.  '
            '18–21 = excellent  |  13–17 = review the paradigm  |  below 13 = revisit §26.3–26.13'
        )

        # ── Coverage table ────────────────────────────────────────────────────
        self.add_section_heading('Conjugation Coverage')
        self.add_coverage_table([
            ('Wayyiqtol (5)',      '#9, #10, #11, #13, B2'),
            ('Inf. Construct (3)', '#6, #7, #14'),
            ('Participle (3)',     '#2, #3, #8'),
            ('Imperfect (3)',      '#5, #16, #19'),
            ('Perfect / qatal (2)', '#1, B1'),
            ('Weqatal (2)',        '#4, #17'),
            ('Inf. Absolute (2)',  '#15, #18'),
            ('Imperative (1)',     '#12'),
            ('Distractors (3)',    'D1 (Niphal Weqatal 3fs), D2 (Qal Weqatal 3ms), D3 (Qal Imperfect 2ms)'),
        ])

        # ── Reflection (only on question pages, not repeated in key) ──────────
        if not show_answers:
            self.add_reflection([
                'Wayyiqtol dominates in Gen 6–8 but is absent from Passages D and E. What does this tell '
                'you about how genre — narrative vs. divine oracle (Gen 22) vs. legal instruction (Deut 7) '
                '— shapes conjugation choice in the Hiphil?',
                'Both Passage D (Gen 22:17) and Passage E (Deut 7:2) use the emphatic inf. absolute + '
                'imperfect pattern. What does the inf. absolute add beyond a plain imperfect? Are the two '
                'contexts — promise and command — using the emphasis for the same rhetorical purpose?',
                'In Gen 6–8, God is the subject of nearly every Hiphil; Noah appears as subject only at '
                '#11 and #13. What does this distribution of agency tell you about the theological '
                'architecture of the flood narrative?',
            ])


# ---------------------------------------------------------------------------
# Chapter 26 — Qal–Hiphil Contrast Drill
# ---------------------------------------------------------------------------
class Ch26ContrastExercise(ExercisePDF):

    _ENTRIES_A = [
        ContrastEntry('1', 'בּוֹא', 'to go in, come',   'יָּבֵא',      'Wayyiqtol 3ms', 'Gen 2:19',  'he brought (them)',          'Causative',      'God caused the animals to come to Adam'),
        ContrastEntry('2', 'יָצָא', 'to go out',        'תּוֹצֵא',     'Wayyiqtol 3fs', 'Gen 1:12',  'it brought forth',           'Causative',      'Earth caused vegetation to come out'),
        ContrastEntry('3', 'שׁוּב', 'to return',        'הֵשִׁיב',     'Weqatal 3ms',   'Gen 14:16', 'he brought back',            'Causative',      'Abraham caused Lot to return'),
        ContrastEntry('4', 'עָלָה', 'to go up',         'הַעֲלֵה',     'Imperative 2ms', 'Gen 22:2',  'offer up! / bring up!',      'Causative',      'Cause Isaac to go up as an offering'),
        ContrastEntry('5', 'יָרַד', 'to go down',       'תֹּרֶד',      'Wayyiqtol 3fs', 'Gen 24:18', 'she lowered (her jar)',       'Causative',      'Rebekah caused the jar to go down'),
        ContrastEntry('6', 'מוּת',  'to die',           'הָמִית',      'Inf. Constr.',  'Gen 18:25', 'to put to death / to kill',  'Causative',      'Causing someone to die'),
        ContrastEntry('7', 'יָלַד', 'to give birth',    'יּוֹלֶד',     'Wayyiqtol 3ms', 'Gen 5:3',   'he fathered / begat',        'Causative',      'Adam caused a son to be born'),
        ContrastEntry('8', 'שָׁקָה', 'to drink',        'הִשְׁקָה',    'Perfect 3ms',   'Gen 2:6',   'it watered',                 'Causative',      'Mist caused the ground to receive water'),
    ]
    _ENTRIES_B = [
        ContrastEntry('9',  'כָּבֵד', 'to be heavy/honored', 'יַּכְבֵּד',   'Wayyiqtol 3ms', 'Exo 8:28', 'he hardened (his heart)',         'Factitive',   'Caused heart to be in state of stubbornness'),
        ContrastEntry('10', 'גָּדַל', 'to be great',         'תַּגְדֵּל',   'Wayyiqtol 2ms', 'Gen 19:19', 'you have made great (your mercy)', 'Factitive',   'Caused kindness to be great'),
        ContrastEntry('11', 'רָשָׁע', 'to be wicked',        'הִרְשִׁיעוּ', 'Perfect 3cp',    'Deu 25:1', 'they condemned as guilty',         'Declarative', 'Legal verdict: declaring guilty party as guilty'),
    ]
    _ENTRIES_C = [
        ContrastEntry('12', 'נָכָה', 'no Qal in BH', 'הַכּוֹת',      'Inf. Construct', 'Gen 4:15',  'to strike / smite',  'Simple Action', 'Hiphil is primary form; no causative layer'),
        ContrastEntry('13', 'שָׁמַד', 'no Qal in BH', 'הִשְׁמַדְתִּי', 'Perfect 1cs',    'Lev 26:30', 'I will destroy',      'Simple Action', 'Niphal of same root = "to be destroyed"'),
        ContrastEntry('14', 'נָגַד', 'rare Qal',      'יַּגֵּד',      'Wayyiqtol 3ms', 'Gen 9:22',  'he told / reported', 'Simple Action', 'Root idea = place before someone'),
    ]

    def _build(self):
        self.add_instructions(
            'For each item: (1) write an English translation of the Hiphil form in the Translation '
            'column; (2) write the semantic function (Causative / Factitive / Declarative / Simple '
            'Action) in the Function column. Answer key is on the last page.'
        )

        self.add_section_heading('Part A — Motion Verbs (Causative)')
        self.add_note('These roots describe motion in the Qal. The Hiphil makes someone else do the moving.')
        self.add_contrast_table(self._ENTRIES_A, show_answers=False)

        self.add_section_heading('Part B — Stative Verbs (Factitive and Declarative)')
        self.add_note(
            'Factitive: the Hiphil causes an object to be in a state (make heavy, make great). '
            'Declarative: the Hiphil declares/treats something as being in that state (declare guilty).'
        )
        self.add_contrast_table(self._ENTRIES_B, show_answers=False)

        self.add_section_heading('Part C — Verbs with No Common Qal')
        self.add_note('Hiphil is the standard/primary form of these roots. No Qal "base" to compare against.')
        self.add_contrast_table(self._ENTRIES_C, show_answers=False)

        self.add_reflection([
            'For the motion verbs in Part A, describe the pattern in one sentence: what does the '
            'Hiphil consistently do to the Qal meaning?',
            'Which of Part B\'s three verbs is Factitive and which is Declarative? How did you decide?',
            'Does the lack of a Qal counterpart (Part C) affect how you translate the Hiphil? Why or why not?',
        ])

        self.add_answer_key_contrast(self._ENTRIES_A + self._ENTRIES_B + self._ENTRIES_C)


def build_ch26_contrast_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch26', 'exercises',
                               'ch26-qal-hiphil-contrast')
    path = os.path.join(out_dir, 'ch26-qal-hiphil-contrast.pdf')
    ex = Ch26ContrastExercise(
        title='Chapter 26 — Qal–Hiphil Contrast Drill',
        subtitle='BBH Chapter 26 · Hiphil Strong Verbs',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Chapter 26 — Semantic Function Sorting
# ---------------------------------------------------------------------------
class Ch26FunctionSortExercise(ExercisePDF):

    _ENTRIES = [
        SortEntry('1',  'יָּבֵא',        'Wayyiqtol 3ms',  'Gen 2:19',  '"he brought them to the man"',                     'C',  'בּוֹא',  'Qal = to come; Hiphil = cause to come'),
        SortEntry('2',  'תּוֹצֵא',       'Wayyiqtol 3fs',  'Gen 1:12',  '"the earth brought forth vegetation"',              'C',  'יָצָא',  'Qal = to go out; Hiphil = cause to come out'),
        SortEntry('3',  'הֵשִׁיב',       'Weqatal 3ms',    'Gen 14:16', '"he brought back his brother Lot"',                 'C',  'שׁוּב',  'Qal = to return; Hiphil = cause to return'),
        SortEntry('4',  'הִשְׁקָה',      'Perfect 3ms',    'Gen 2:6',   '"a mist watered the whole surface"',                'C',  'שָׁקָה', 'Qal = to drink; Hiphil = cause to drink/water'),
        SortEntry('5',  'יּוֹלֶד',       'Wayyiqtol 3ms',  'Gen 5:3',   '"Adam fathered a son"',                            'C',  'יָלַד',  'Qal = to give birth; Hiphil = cause to be born'),
        SortEntry('6',  'הַעֲלֵה',       'Imperative 2ms', 'Gen 22:2',  '"offer him as a burnt offering"',                   'C',  'עָלָה',  'Qal = to go up; Hiphil = cause to go up/offer'),
        SortEntry('7',  'תֹּרֶד',        'Wayyiqtol 3fs',  'Gen 24:18', '"she lowered her jar to give him a drink"',         'C',  'יָרַד',  'Qal = to go down; Hiphil = cause to go down'),
        SortEntry('8',  'הֵסִיר',        'Wayyiqtol 3ms',  'Gen 30:35', '"he removed the streaked goats"',                   'C',  'סוּר',   'Qal = to turn aside; Hiphil = cause to depart'),
        SortEntry('9',  'יַּגֵּד',       'Wayyiqtol 3ms',  'Gen 9:22',  '"Ham told his two brothers"',                      'SA', 'נָגַד',  'Rare Qal; Hiphil is operative form: to tell'),
        SortEntry('10', 'הִגִּיד',       'Weqatal 3ms',    'Gen 3:11',  '"who told you that you were naked?"',               'SA', 'נָגַד',  'Same root as #9; Hiphil = standard form'),
        SortEntry('11', 'תַּשְׁלֵךְ',   'Wayyiqtol 3fs',  'Gen 21:15', '"she threw the child under a bush"',                'SA', 'שָׁלַךְ', 'No common Qal; Hiphil = to throw/cast'),
        SortEntry('12', 'הִזְכַּרְתָּ', 'Perfect 2ms',    'Gen 40:14', '"mention me to Pharaoh"',                           'C',  'זָכַר',  'Qal = to remember; Hiphil = cause to remember'),
        SortEntry('13', 'מַזְכִּיר',    'Participle ms',  'Gen 41:9',  '"I am bringing my faults to mind"',                 'C',  'זָכַר',  'Causing something to be remembered'),
        SortEntry('14', 'הָמִית',        'Inf. Constr.',   'Gen 18:25', '"far be it from you to put…to death"',              'C',  'מוּת',   'Qal = to die; Hiphil = cause to die'),
        SortEntry('15', 'הַכּוֹת',       'Inf. Constr.',   'Gen 4:15',  '"lest anyone who found him strike him"',            'SA', 'נָכָה',  'No Qal; Hiphil = primary form: to strike'),
        SortEntry('16', 'הִשְׁמַדְתִּי', 'Perfect 1cs',   'Lev 26:30', '"I will destroy your high places"',                 'SA', 'שָׁמַד', 'No Qal; Niphal = "be destroyed"'),
        SortEntry('17', 'תַּשְׁמִידוּ', 'Imperfect 2mp',  'Num 33:52', '"you shall demolish their figured stones"',          'SA', 'שָׁמַד', 'Same root as #16; conquest context'),
        SortEntry('18', 'יַּכְבֵּד',    'Wayyiqtol 3ms',  'Exo 8:28',  '"Pharaoh hardened his heart this time also"',        'F',  'כָּבֵד', 'Qal = be heavy; Hiphil = make/cause heaviness'),
        SortEntry('19', 'הַכְבֵּד',     'Inf. Absolute',  'Exo 8:11',  '"he made his heart stubborn" (intensified)',         'F',  'כָּבֵד', 'Inf. Abs. intensifies the factitive action'),
        SortEntry('20', 'תַּגְדֵּל',    'Wayyiqtol 2ms',  'Gen 19:19', '"you have shown great kindness to me"',             'F',  'גָּדַל', 'Qal = be great; Hiphil = cause greatness'),
        SortEntry('21', 'הִרְשִׁיעוּ', 'Perfect 3cp',    'Deu 25:1',  '"acquit the innocent and condemn the guilty"',       'D',  'רָשָׁע', 'Legal verdict; declaring — not causing — guilt'),
        SortEntry('22', 'יַרְשִׁיעֻ',  'Imperfect 3mp',  'Exo 22:8',  '"the judges shall declare him guilty"',              'D',  'רָשָׁע', 'Same root; judicial pronouncement'),
        SortEntry('23', 'יַּעַל',       'Wayyiqtol 3ms',  'Gen 8:20',  '"Noah offered burnt offerings on the altar"',        'C',  'עָלָה',  'Qal = go up; Hiphil = cause to go up/offer'),
        SortEntry('24', 'הָמִית',        'Inf. Constr.',   'Gen 37:18', '"they conspired against him to kill him"',           'C',  'מוּת',   'Same form as #14; different context'),
        SortEntry('25', 'מַמְטִיר',    'Participle ms',  'Gen 7:4',   '"I am about to send rain on the earth"',             'DN', 'מָטַר',  'Noun: מָטָר (rain); Hiphil = to cause rain / send rain'),
        SortEntry('26', 'יַּשְׁכֵּם', 'Wayyiqtol 3ms',  'Gen 22:3',  '"Abraham rose early in the morning"',               'DN', 'שָׁכַם', 'Noun: שְׁכֶם (shoulder); to shoulder up = rise early'),
        SortEntry('27', 'הַאְזִינוּ', 'Imperative 2mp', 'Deu 32:1',  '"give ear, O heavens, and I will speak"',           'DN', 'אָזַן',  'Noun: אֹזֶן (ear); to ear = give ear / listen'),
    ]

    def _build(self):
        self.add_instructions(
            'Classify each Hiphil verb as C (Causative), F (Factitive), D (Declarative), '
            'SA (Simple Action), or DN (Denominative). Write your answer in the Function column. '
            'Answer key is on the last page.'
        )

        self.add_note(
            'C = Causative (subject causes another to act/experience)  |  '
            'F = Factitive (subject causes object to be in a state)  |  '
            'D = Declarative (subject declares something as being in a state)  |  '
            'SA = Simple Action (Hiphil is the standard form; no common Qal)  |  '
            'DN = Denominative (Hiphil derived from a noun; not in BBH)'
        )

        self.add_sort_table(self._ENTRIES, show_answers=False)

        self.add_reflection([
            'Items 18–19 both come from the root for "be heavy" (Exo 8). How does the Hiphil meaning '
            'connect to the Qal? Is this Factitive or Causative — and why?',
            'Items 21–22 are both Declarative (not Factitive), even though רָשָׁע has a clear stative '
            'Qal. What is the difference between making someone wicked and declaring someone wicked? '
            'What makes Deu 25:1 and Exo 22:8 clearly Declarative?',
            'Items 12–13 (זָכַר, "to remember") are classified as Causative. How does "mention me to '
            'Pharaoh" (Gen 40:14) fit the Causative definition? Does that reading change the translation?',
        ])

        self.add_answer_key_sort(self._ENTRIES)


def build_ch26_function_sort_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch26', 'exercises',
                               'ch26-function-sort')
    path = os.path.join(out_dir, 'ch26-function-sort.pdf')
    ex = Ch26FunctionSortExercise(
        title='Chapter 26 — Semantic Function Sorting',
        subtitle='BBH Chapter 26 · Hiphil Strong Verbs',
    )
    return ex.save(path)


def build_ch26_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch26', 'exercises',
                               'ch26-passage-exercise')
    path = os.path.join(out_dir, 'ch26-passage-exercise.pdf')
    ex = Ch26Exercise(
        title='Chapter 26 — "Spot the Hiphil" Passage Exercise',
        subtitle='Genesis 6–8  ·  Genesis 22  ·  Deuteronomy 7',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Chapter 25 — "Spot the Niphal" Passage Exercise
# ---------------------------------------------------------------------------
class Ch25Exercise(PassageExercise):
    _instructions = (
        'Most highlighted verbs are Niphal forms. For each one, first answer '
        'Is it Niphal? (Yes / No). If Yes: parse conjugation, PGN, and root, '
        'then state the semantic function (Passive / Reflexive / Middle / Simple Action). '
        'If No: identify the correct stem and parse fully. '
        'Part C contains distractor verbs — not Niphal. '
        'Answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool):

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Genesis 3:5–10')

        self.add_passage(PassageBlock('3:5',
            'וִֽהְיִיתֶם֙ כֵּֽאלֹהִ֔ים יֹדְעֵ֖י טוֹב וָרָ֑ע כִּ֣י יֹדֵ֔עַ אֱלֹהִ֕ים כִּ֗י בְּיֹ֛ום אֲכָלְכֶ֥ם מִמֶּ֖נּוּ וְנִפְקְח֖וּ עֵינֵיכֶ֑ם',
            '"…for God knows that in the day you eat of it your eyes will [1] ____."'))
        self.add_verb_table([VerbEntry('1', 'וְנִפְקְחוּ', 'Weqatal', '3cp', 'פָּקַח', 'Middle — will be opened')], show_answers=show_answers)

        self.add_passage(PassageBlock('3:6',
            'וְנֶחְמָ֤ד הָעֵץ֙ לְהַשְׂכִּ֔יל',
            '"…and that the tree was desirable to make one wise."'))
        self.add_verb_table([VerbEntry('2', 'וְנֶחְמָד', 'Participle ms', 'ms', 'חָמַד', 'Passive — desirable (substantival ptc.)')], show_answers=show_answers)

        self.add_passage(PassageBlock('3:7',
            'וַתִּפָּקַ֙חְנָה֙ עֵינֵ֣י שְׁנֵיהֶ֔ם',
            '"Then the eyes of both of them [3] ____."'))
        self.add_verb_table([VerbEntry('3', 'וַתִּפָּקַחְנָה', 'Wayyiqtol', '3fp', 'פָּקַח', 'Middle — they were opened')], show_answers=show_answers)

        self.add_passage(PassageBlock('3:10',
            'וָאִירָ֛א כִּֽי־עֵירֹ֥ם אָנֹ֖כִי וָאֵחָבֵֽא',
            '"I was afraid, because I was naked, and [4] ____."'))
        self.add_verb_table([VerbEntry('4', 'וָאֵחָבֵא', 'Wayyiqtol', '1cs', 'חָבָא', 'Reflexive — I hid myself')], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Genesis 6:6–12')

        self.add_passage(PassageBlock('6:6',
            'וַיִּנָּ֣חֶם יְהוָ֔ה כִּֽי־עָשָׂ֥ה אֶת־הָאָדָ֖ם בָּאָ֑רֶץ',
            '"And the LORD [5] ____ that he had made man on the earth."'))
        self.add_verb_table([VerbEntry('5', 'וַיִּנָּחֶם', 'Wayyiqtol', '3ms', 'נָחַם', 'Simple Action (Niphal-only) — relented')], show_answers=show_answers)

        self.add_passage(PassageBlock('6:7',
            'נִחַ֖מְתִּי כִּ֥י עֲשִׂיתִֽם',
            '"I [6] ____ that I made them."'))
        self.add_verb_table([VerbEntry('6', 'נִחַמְתִּי', 'Weqatal', '1cs', 'נָחַם', 'Simple Action (Niphal-only) — I regret')], show_answers=show_answers)

        self.add_passage(PassageBlock('6:11',
            'וַתִּשָּׁחֵ֥ת הָאָ֖רֶץ … וַתִּמָּלֵ֥א הָאָ֖רֶץ חָמָֽס',
            '"The earth [7] ____ … and the earth [8] ____ with violence."'))
        self.add_verb_table([
            VerbEntry('7', 'וַתִּשָּׁחֵת', 'Wayyiqtol', '3fs', 'שָׁחַת', 'Passive — it was corrupted'),
            VerbEntry('8', 'וַתִּמָּלֵא', 'Wayyiqtol', '3fs', 'מָלֵא', 'Passive — it was filled'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('6:12',
            'וְהִנֵּ֥ה נִשְׁחָ֑תָה כִּֽי־הִשְׁחִ֧ית כָּל־בָּשָׂ֛ר',
            '"and behold, it [9] ____, for all flesh had corrupted its way."'))
        self.add_verb_table([VerbEntry('9', 'נִשְׁחָתָה', 'Weqatal', '3fs', 'שָׁחַת', 'Passive — it was corrupt')], show_answers=show_answers)

        self.add_passage(PassageBlock('6:21',
            'וְהָיָ֥ה לְךָ֖ וְלָהֶ֥ם לְאָכְלָֽה יֵֽאָכֵ֔ל',
            '"it shall be food for you and for them — it shall [10] ____."'))
        self.add_verb_table([VerbEntry('10', 'יֵאָכֵל', 'Imperfect', '3ms', 'אָכַל', 'Passive — it shall be eaten')], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Genesis 21:23–31')

        self.add_passage(PassageBlock('21:23',
            'הִשָּׁ֨בְעָ֜ה לִּ֗י בֵּאלֹהִ֛ים הֵ֖נָּה',
            '"[11] ____ to me by God here."'))
        self.add_verb_table([VerbEntry('11', 'הִשָּׁבְעָה', 'Imperative', '2ms', 'שָׁבַע', 'Reflexive — Swear! (bind yourself by oath)')], show_answers=show_answers)

        self.add_passage(PassageBlock('21:24',
            'וַיֹּ֙אמֶר֙ אַבְרָהָ֔ם אָנֹכִ֖י אִשָּׁבֵֽעַ',
            '"And Abraham said, \'I [12] ____.\'"'))
        self.add_verb_table([VerbEntry('12', 'אִשָּׁבֵעַ', 'Imperfect', '1cs', 'שָׁבַע', 'Reflexive — I will swear')], show_answers=show_answers)

        self.add_passage(PassageBlock('21:31',
            'כִּ֛י שָׁ֥ם נִשְׁבְּע֖וּ שְׁנֵיהֶֽם',
            '"For there [13] ____ both of them."'))
        self.add_verb_table([VerbEntry('13', 'נִשְׁבְּעוּ', 'Weqatal', '3mp', 'שָׁבַע', 'Reflexive — they swore (bound themselves by oath)')], show_answers=show_answers)

        self.add_section_break()

        # ── Bonus ─────────────────────────────────────────────────────────────
        self.add_section_heading('Bonus — Genesis 21:3, 21:8')

        self.add_passage(PassageBlock('21:3', 'אֲשֶׁר־נּֽוֹלַד־לֹ֛ו', '"who had been born to him"'))
        self.add_passage(PassageBlock('21:8', 'וַיִּגְדַּ֤ל הַיֶּ֙לֶד֙ וַיִּגָּמַ֑ל', '"And the child grew and was weaned."'))
        self.add_verb_table([
            VerbEntry('B1', 'נּוֹלַד',  'Weqatal',   '3ms', 'יָלַד', 'Passive — who had been born'),
            VerbEntry('B2', 'וַיִּגָּמַל', 'Wayyiqtol', '3ms', 'גָּמַל', 'Passive — was weaned'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Part C — Distractors ───────────────────────────────────────────────
        self.add_section_heading('Part C — Distractor Check')
        self.add_note(
            'These three verbs come from the same passages. None are Niphal. '
            'Answer "No" for Niphal? and complete the full parse.'
        )

        self.add_passage(PassageBlock('3:6',
            'וַתֵּרֶא הָאִשָּׁה כִּי טוֹב הָעֵץ לְמַאֲכָל',
            '"So when the woman [D1] ____ that the tree was good for food."'))
        self.add_verb_table([VerbEntry('D1', 'וַתֵּרֶא', 'Wayyiqtol', '3fs', 'רָאָה', 'NOT Niphal — Qal: and she saw; III-ה Qal wayyiqtol; no נ-/תִ- Niphal marker')], show_answers=show_answers)

        self.add_passage(PassageBlock('6:6',
            'כִּי עָשָׂה אֶת־הָאָדָם בָּאָרֶץ',
            '"that he [D2] ____ mankind on the earth."'))
        self.add_verb_table([VerbEntry('D2', 'עָשָׂה', 'Perfect', '3ms', 'עָשָׂה', 'NOT Niphal — Qal: he made/did; III-ה Qal perfect; contrast Niphal וַיִּנָּחֶם earlier in the verse')], show_answers=show_answers)

        self.add_passage(PassageBlock('21:8',
            'וַיִּגְדַּל הַיֶּלֶד',
            '"And [D3] ____ the child."'))
        self.add_verb_table([VerbEntry('D3', 'וַיִּגְדַּל', 'Wayyiqtol', '3ms', 'גָּדַל', 'NOT Niphal — Qal: and he grew; plain Qal wayyiqtol; contrast Niphal וַיִּגָּמַל in same verse')], show_answers=show_answers)

        self.add_section_break()

        self.add_note(
            'Items 5–6 (וַיִּנָּחֶם / נִחַמְתִּי) are both from נָחַם, a verb that occurs almost exclusively '
            'in the Niphal. Items 11–13 all parse as Reflexive from שָׁבַע — '
            'notice how Imperative, Imperfect, and Weqatal all express the same oath-swearing action.'
        )
        self.add_score(
            'Score: 13 main + 2 bonus = 15 total.  '
            '13–15 = excellent  |  9–12 = review the paradigm  |  below 9 = revisit §23.3–23.13'
        )

        self.add_section_heading('Conjugation Coverage')
        self.add_coverage_table([
            ('Wayyiqtol (5)', '#3, #5, #7, #8, B2'),
            ('Weqatal (5)',   '#1, #6, #9, #13, B1'),
            ('Imperfect (2)', '#10, #12'),
            ('Participle (1)', '#2'),
            ('Imperative (1)', '#11'),
            ('Distractors (3)', 'D1 (Qal Wayyiqtol 3fs), D2 (Qal Perfect 3ms), D3 (Qal Wayyiqtol 3ms)'),
        ])

        if not show_answers:
            self.add_reflection([
                'Every Niphal in Passage A (Gen 3) involves eyes, hiding, or desire. What does the '
                'Niphal contribute to the theological message of the Fall narrative?',
                'In Gen 6:6–7, God is the subject of a Niphal-only verb (נָחַם). What does this choice '
                'tell us about how the narrator portrays God\'s emotional response?',
                'Compare Gen 3:5 (וְנִפְקְחוּ — "will be opened," Middle/Tolerative) with Gen 3:7 '
                '(וַתִּפָּקַחְנָה — "were opened," Middle). Is the function identical in both? '
                'What difference in nuance, if any, does the shift from weqatal to wayyiqtol suggest?',
            ])


def build_ch25_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch25', 'exercises',
                               'ch25-passage-exercise')
    path = os.path.join(out_dir, 'ch25-passage-exercise.pdf')
    ex = Ch25Exercise(
        title='Chapter 25 — "Spot the Niphal" Passage Exercise',
        subtitle='Genesis 3, 6, and 21  ·  The Garden, the Flood Prelude, and Beersheba',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Chapter 24 — "Spot the Niphal" Passage Exercise
# ---------------------------------------------------------------------------
class Ch24Exercise(PassageExercise):
    _instructions = (
        'Most highlighted verbs are Niphal forms. For each one, first answer '
        'Is it Niphal? (Yes / No). If Yes: parse conjugation, PGN, and root, '
        'then state the semantic function (Passive / Reflexive / Simple Action). '
        'If No: identify the correct stem and parse fully. '
        'Part C contains distractor verbs — not Niphal. '
        'Answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool):

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Genesis 37:7, 36')

        self.add_passage(PassageBlock('37:7',
            'וְהִנֵּה קָמָה אֲלֻמָּתִי וְגַם נִצָּבָה',
            '"and behold, my sheaf arose and [1] ____."'))
        self.add_verb_table([VerbEntry('1', 'נִצָּבָה', 'Perfect', '3fs', 'נָצַב', 'Reflexive — it stood upright (stationed itself)')], show_answers=show_answers)

        self.add_passage(PassageBlock('37:36',
            'וְהַמְּדָנִים מָכְרוּ אֹתוֹ … וַיִּמָּכֵר יוֹסֵף אֶל־מִצְרָיִם',
            '"Now the Midianites had sold him … and Joseph [2] ____ into Egypt."'))
        self.add_verb_table([VerbEntry('2', 'וַיִּמָּכֵר', 'Wayyiqtol', '3ms', 'מָכַר', 'Passive — he was sold')], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Genesis 44:9–20')

        self.add_passage(PassageBlock('44:9',
            'אֲשֶׁר יִמָּצֵא אִתּוֹ מֵעֲבָדֶיךָ וָמֵת',
            '"With whichever of your servants [3] ____ [the cup] shall die."'))
        self.add_verb_table([VerbEntry('3', 'יִמָּצֵא', 'Imperfect', '3ms', 'מָצָא', 'Passive — is found')], show_answers=show_answers)

        self.add_passage(PassageBlock('44:12',
            'וַיִּמָּצֵא הַגָּבִיעַ בְּאַמְתַּחַת בִּנְיָמִן',
            '"And the cup [4] ____ in Benjamin\'s sack."'))
        self.add_verb_table([VerbEntry('4', 'וַיִּמָּצֵא', 'Wayyiqtol', '3ms', 'מָצָא', 'Passive — was found')], show_answers=show_answers)

        self.add_passage(PassageBlock('44:20',
            'יֶשׁ לָנוּ אָב זָקֵן וְיֶלֶד זְקֻנִים קָטָן וְאָחִיו מֵת וַיִּוָּתֵר הוּא',
            '"We have an aged father … his brother is dead, and he alone [5] ____."'))
        self.add_verb_table([VerbEntry('5', 'וַיִּוָּתֵר', 'Wayyiqtol', '3ms', 'יָתַר', 'Passive/Middle — was left, remained')], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Genesis 45:1, 16')

        self.add_passage(PassageBlock('45:1',
            'וְלֹא־יָכֹל יוֹסֵף לְהִתְאַפֵּק לְכֹל הַנִּצָּבִים עָלָיו',
            '"Joseph could no longer control himself before all those [6] ____ near him."'))
        self.add_verb_table([VerbEntry('6', 'הַנִּצָּבִים', 'Participle', 'mp', 'נָצַב', 'Reflexive — those standing (stationed themselves)')], show_answers=show_answers)

        self.add_passage(PassageBlock('45:16',
            'וְהַקֹּל נִשְׁמַע בֵּית פַּרְעֹה לֵאמֹר בָּאוּ אֲחֵי־יוֹסֵף',
            '"And the report [7] ____ in Pharaoh\'s household, \'Joseph\'s brothers have come.\'"'))
        self.add_verb_table([VerbEntry('7', 'נִשְׁמַע', 'Perfect', '3ms', 'שָׁמַע', 'Passive — was heard')], show_answers=show_answers)

        self.add_section_break()

        # ── Passage D ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage D — Genesis 47:14, 31')

        self.add_passage(PassageBlock('47:14',
            'וַיְלַקֵּט יוֹסֵף אֶת־כָּל־הַכֶּסֶף הַנִּמְצָא בְאֶרֶץ־מִצְרַיִם',
            '"And Joseph collected all the silver [8] ____ in the land of Egypt."'))
        self.add_verb_table([VerbEntry('8', 'הַנִּמְצָא', 'Participle', 'ms', 'מָצָא', 'Passive — that was found')], show_answers=show_answers)

        self.add_passage(PassageBlock('47:31',
            'הִשָּׁבְעָה לִי וַיִּשָּׁבַע לוֹ',
            '"[9] ____ to me." And he [10] ____ to him."'))
        self.add_verb_table([
            VerbEntry('9', 'הִשָּׁבְעָה', 'Imperative', '2ms', 'שָׁבַע', 'Reflexive — swear! (bind yourself by oath)'),
            VerbEntry('10', 'וַיִּשָּׁבַע', 'Wayyiqtol', '3ms', 'שָׁבַע', 'Reflexive — he swore (bound himself by oath)'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage E ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage E — Genesis 49:1, 29, 33')

        self.add_passage(PassageBlock('49:1',
            'הֵאָסְפוּ וְאַגִּידָה לָכֶם',
            '"[11] ____ and I will tell you."'))
        self.add_verb_table([VerbEntry('11', 'הֵאָסְפוּ', 'Imperative', '2mp', 'אָסַף', 'Passive — gather yourselves!')], show_answers=show_answers)

        self.add_passage(PassageBlock('49:29',
            'אֲנִי נֶאֱסָף אֶל־עַמִּי',
            '"I am [12] ____ to my people."'))
        self.add_verb_table([VerbEntry('12', 'נֶאֱסָף', 'Participle', 'ms', 'אָסַף', 'Passive — am about to be gathered (die)')], show_answers=show_answers)

        self.add_passage(PassageBlock('49:33',
            'וַיֵּאָסֶף אֶל־עַמָּיו',
            '"and he was [13] ____ to his people."'))
        self.add_verb_table([VerbEntry('13', 'וַיֵּאָסֶף', 'Wayyiqtol', '3ms', 'אָסַף', 'Passive — was gathered (died)')], show_answers=show_answers)

        self.add_section_break()

        # ── Bonus ─────────────────────────────────────────────────────────────
        self.add_section_heading('Bonus — Exodus 19:12')

        self.add_passage(PassageBlock('19:12',
            'וְהִשָּׁמַרְתֶּם … הִשָּׁמְרוּ לָכֶם',
            '"And you shall [B1] ____ … [B2] ____ for yourselves."'))
        self.add_verb_table([
            VerbEntry('B1', 'וְהִשָּׁמַרְתֶּם', 'Weqatal',   '2mp', 'שָׁמַר', 'Reflexive — take heed for yourselves'),
            VerbEntry('B2', 'הִשָּׁמְרוּ',      'Imperative', '2mp', 'שָׁמַר', 'Reflexive — take heed! (guard yourselves)'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Part C — Distractors ───────────────────────────────────────────────
        self.add_section_heading('Part C — Distractor Check')
        self.add_note(
            'These three verbs come from the same passages. None are Niphal. '
            'Answer "No" for Niphal? and complete the full parse.'
        )

        self.add_passage(PassageBlock('37:7',
            'וְהִנֵּה קָמָה אֲלֻמָּתִי',
            '"and behold, my sheaf [D1] ____."'))
        self.add_verb_table([VerbEntry('D1', 'קָמָה', 'Perfect', '3fs', 'קוּם', 'NOT Niphal — Qal: she/it arose (no נ- prefix; plain Qal of hollow verb)')], show_answers=show_answers)

        self.add_passage(PassageBlock('37:36',
            'וְהַמְּדָנִים מָכְרוּ אֹתוֹ',
            '"Now the Midianites [D2] ____ him."'))
        self.add_verb_table([VerbEntry('D2', 'מָכְרוּ', 'Perfect', '3cp', 'מָכַר', 'NOT Niphal — Qal: they sold; no נִ- prefix; contrast with Niphal וַיִּמָּכֵר in same verse')], show_answers=show_answers)

        self.add_passage(PassageBlock('45:1',
            'וְלֹא־יָכֹל יוֹסֵף לְהִתְאַפֵּק',
            '"Joseph [D3] ____ no longer control himself."'))
        self.add_verb_table([VerbEntry('D3', 'יָכֹל', 'Perfect', '3ms', 'יָכֹל', 'NOT Niphal — Qal: he was able; Qal-only verb; לֹא יָכֹל = could not')], show_answers=show_answers)

        self.add_section_break()

        self.add_note(
            'Items 12–13 (נֶאֱסָף / וַיֵּאָסֶף) are both from אָסַף — the euphemism "gathered to '
            'one\'s people" means death. Items 9–10 both parse as Reflexive from שָׁבַע — '
            'notice Imperative followed by Wayyiqtol in the same verse (Gen 47:31).'
        )
        self.add_score(
            'Score: 13 main + 2 bonus = 15 total.  '
            '13–15 = excellent  |  9–12 = review the paradigm  |  below 9 = revisit §24.3–24.13'
        )

        self.add_section_heading('Conjugation Coverage')
        self.add_coverage_table([
            ('Wayyiqtol (5)',  '#2, #4, #5, #10, #13'),
            ('Participle (3)', '#6, #8, #12'),
            ('Imperfect (1)',  '#3'),
            ('Perfect (2)',    '#1, #7'),
            ('Imperative (3)', '#9, #11, B2'),
            ('Weqatal (1)',    'B1'),
            ('Distractors (3)', 'D1 (Qal Perf 3fs), D2 (Qal Perf 3cp), D3 (Qal Perf 3ms)'),
        ])

        if not show_answers:
            self.add_reflection([
                'Several Niphal forms of אָסַף in this passage describe Jacob\'s death (Gen 49:29, 33). '
                'What does the passive "to be gathered to one\'s people" suggest about ancient Israelite '
                'views of death?',
                'In Gen 47:31, both הִשָּׁ֣בְעָה (imperative) and וַיִּשָּׁבַע (wayyiqtol) appear together. '
                'How does the narrative sequence reinforce the solemnity of Jacob\'s deathbed request?',
                'Compare נִצָּבָה in Gen 37:7 (Reflexive — sheaf stands itself upright) with הַנִּצָּבִים '
                'in Gen 45:1 (Reflexive participle — servants stationed before Joseph). Is the reflexive '
                'force the same in both? What does each communicate about agency?',
            ])


def build_ch24_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch24', 'exercises',
                               'ch24-passage-exercise')
    path = os.path.join(out_dir, 'ch24-passage-exercise.pdf')
    ex = Ch24Exercise(
        title='Chapter 24 — "Spot the Niphal" Passage Exercise',
        subtitle='Genesis 37, 44, 45, 47, 49  ·  The Joseph Narrative',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Chapter 24 — Qal–Niphal Contrast Drill
# ---------------------------------------------------------------------------
class Ch24ContrastExercise(ExercisePDF):

    _ENTRIES_A = [
        ContrastEntry('1',  'מָכַר', 'to sell',            'וַיִּמָּכֵר',      'Wayyiqtol 3ms',  'Gen 37:36', 'he was sold into Egypt',         'Passive',       'The object of selling (Joseph) becomes the subject'),
        ContrastEntry('2',  'מָצָא', 'to find',            'יִמָּצֵא',         'Imperfect 3ms',  'Gen 44:9',  'is found (with the cup)',         'Passive',       'The thing found becomes the subject; finder absent'),
        ContrastEntry('3',  'שָׁמַע', 'to hear',           'נִשְׁמַע',         'Perfect 3ms',    'Gen 45:16', 'was heard (in Pharaoh\'s house)', 'Passive',       'The report receives the hearing — it becomes audible'),
        ContrastEntry('4',  'אָסַף', 'to gather',          'וַיֵּאָסֶף',       'Wayyiqtol 3ms',  'Gen 49:33', 'was gathered to his people',      'Passive',       'Jacob receives the action of being gathered in (die)'),
        ContrastEntry('5',  'כָּרַת', 'to cut off',        'וְנִכְרְתָה',      'Weqatal 3fs',    'Exo 12:15', 'will be cut off from Israel',     'Passive',       'The person receives covenant-exclusion penalty'),
        ContrastEntry('6',  'נָתַן', 'to give',            'נִתְּנוּ',         'Perfect 3mp',    'Gen 9:2',   'they are given into your hand',   'Passive',       'Animals receive the action of being given/placed'),
        ContrastEntry('7',  'אָכַל', 'to eat',             'יֵאָכֵל',          'Imperfect 3ms',  'Exo 12:46', 'it shall be eaten',               'Passive',       'Passover lamb receives the action of eating'),
        ContrastEntry('8',  'שָׁמַר', 'to keep / guard',  'הִשָּׁמְרוּ',      'Imperative 2mp', 'Exo 19:12', 'take heed for yourselves!',       'Reflexive',     'Guard yourself — subject directs action back on itself'),
    ]
    _ENTRIES_B = [
        ContrastEntry('9',  'נָצַב', 'to be stationed',    'נִצָּבָה',         'Perfect 3fs',    'Gen 37:7',  'it stood upright',                'Reflexive',     'The sheaf stations itself in the standing position'),
        ContrastEntry('10', 'יָתַר', 'to remain',          'וַיִּוָּתֵר',      'Wayyiqtol 3ms',  'Gen 44:20', 'he alone was left',               'Passive/Middle', 'State of being-left fell upon him; middle nuance'),
        ContrastEntry('11', 'שָׁאַר', 'to remain',         'נִשְׁאַר',         'Perfect 3ms',    'Exo 14:28', 'not one of them remained',        'Middle',        'Soldiers were in the state of having been left'),
    ]
    _ENTRIES_C = [
        ContrastEntry('12', 'לָחַם', 'no standard Qal',    'הִלָּחֵם',         'Imperative 2ms', 'Exo 17:9',  'fight against Amalek!',           'Simple action', 'Niphal is the base form; no causative layer'),
        ContrastEntry('13', 'נָחַם', 'no standard Qal',    'וַיִּנָּחֶם',      'Wayyiqtol 3ms',  'Gen 6:6',   'the LORD regretted / relented',   'Simple action', 'Niphal is the base form; to regret/relent/be comforted'),
        ContrastEntry('14', 'שָׁבַע', 'to seven/complete', 'הִשָּׁבְעָה',      'Imperative 2ms', 'Gen 47:31', 'swear to me!',                    'Reflexive',     'Bind yourself by oath; reflexive oath-taking'),
    ]

    def _build(self):
        self.add_instructions(
            'For each item: (1) write an English translation of the Niphal form in the Translation '
            'column; (2) write the semantic function (Passive / Reflexive / Simple Action) in the '
            'Function column. Answer key is on the last page.'
        )

        self.add_section_heading('Part A — Transitive Roots (Qal acts on an object)')
        self.add_note('These roots take a direct object in the Qal. The Niphal turns the object into the subject — the classic passive pattern.')
        self.add_contrast_table(self._ENTRIES_A, show_answers=False)

        self.add_section_heading('Part B — Stative / Intransitive Roots')
        self.add_note('These roots describe states. Their Niphal expresses the subject coming into or remaining in a state.')
        self.add_contrast_table(self._ENTRIES_B, show_answers=False)

        self.add_section_heading('Part C — Roots with No Standard Qal')
        self.add_note('These roots occur almost exclusively in the Niphal. The Niphal form is the standard lexical entry.')
        self.add_contrast_table(self._ENTRIES_C, show_answers=False)

        self.add_reflection([
            'For the transitive roots in Part A, describe the pattern in one sentence: what does the '
            'Niphal consistently do to the Qal meaning?',
            'Items 9–11 all involve verbs of position or remaining (נָצַב, יָתַר, שָׁאַר). How does '
            '"reflexive" vs. "middle" vs. "passive" help explain the subtle difference in agency?',
            'לָחַם (item 12) and נָחַם (item 13) are both "lexical Niphal" roots. How does a student '
            'recognize this? What should they look for in a dictionary entry?',
        ])

        self.add_answer_key_contrast(self._ENTRIES_A + self._ENTRIES_B + self._ENTRIES_C)


def build_ch24_contrast_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch24', 'exercises',
                               'ch24-qal-niphal-contrast')
    path = os.path.join(out_dir, 'ch24-qal-niphal-contrast.pdf')
    ex = Ch24ContrastExercise(
        title='Chapter 24 — Qal–Niphal Contrast Drill',
        subtitle='BBH Chapter 24 · Niphal Strong Verbs',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Chapter 24 — Semantic Function Sorting
# ---------------------------------------------------------------------------
class Ch24FunctionSortExercise(ExercisePDF):

    _ENTRIES = [
        SortEntry('1',  'וַיִּמָּכֵר',      'Wayyiqtol 3ms',  'Gen 37:36', '"and Joseph was sold into Egypt"',              'P',  'מָכַר',  'Joseph receives the action of being sold'),
        SortEntry('2',  'נִצָּבָה',         'Perfect 3fs',    'Gen 37:7',  '"my sheaf stood upright"',                      'R',  'נָצַב',  'Sheaf stations itself (acts on itself)'),
        SortEntry('3',  'וַיִּנָּחֶם',      'Wayyiqtol 3ms',  'Gen 6:6',   '"the LORD regretted"',                          'SA', 'נָחַם',  'Niphal-only: no standard Qal; to regret/relent'),
        SortEntry('4',  'יֵאָכֵל',          'Imperfect 3ms',  'Exo 12:46', '"it shall be eaten"',                           'P',  'אָכַל',  'Passover lamb receives the action of eating'),
        SortEntry('5',  'הִשָּׁמְרוּ',      'Imperative 2mp', 'Exo 19:12', '"take heed for yourselves!"',                   'R',  'שָׁמַר', 'Guard yourself — subject directs action back on self'),
        SortEntry('6',  'נִשְׁמַע',         'Perfect 3ms',    'Gen 45:16', '"the report was heard"',                        'P',  'שָׁמַע', 'Report receives the hearing — it becomes audible'),
        SortEntry('7',  'הִשָּׁבְעָה',      'Imperative 2ms', 'Gen 47:31', '"swear to me!"',                                'R',  'שָׁבַע', 'Bind yourself by oath (reflexive oath-taking)'),
        SortEntry('8',  'הַנִּמְצָא',       'Participle ms',  'Gen 47:14', '"the silver that was found"',                   'P',  'מָצָא',  'Silver was discovered (received the finding action)'),
        SortEntry('9',  'וְנִכְרְתָה',      'Weqatal 3fs',    'Exo 12:15', '"that person will be cut off"',                 'P',  'כָּרַת', 'Person receives covenant-exclusion penalty'),
        SortEntry('10', 'נִצָּבִים',        'Participle mp',  'Exo 5:20',  '"standing before Pharaoh"',                     'R',  'נָצַב',  'Overseers have stationed themselves before Pharaoh'),
        SortEntry('11', 'אִוָּעֵד',         'Imperfect 1cs',  'Exo 29:42', '"I will meet with you there"',                  'RC', 'יָעַד',  'God and Israel meet one another at the tent'),
        SortEntry('12', 'וַיִּשָּׁבַע',     'Wayyiqtol 3ms',  'Gen 47:31', '"and he swore to him"',                         'R',  'שָׁבַע', 'Jacob binds himself by oath at Joseph\'s request'),
        SortEntry('13', 'וַיֵּאָסֶף',       'Wayyiqtol 3ms',  'Gen 49:33', '"and he was gathered to his people"',           'P',  'אָסַף',  'Jacob is gathered in (brought to ancestors — die)'),
        SortEntry('14', 'יִלָּחֵם',         'Imperfect 3ms',  'Exo 14:14', '"the LORD will fight for you"',                 'SA', 'לָחַם',  'Niphal-only: to fight is the base meaning'),
        SortEntry('15', 'נִשְׁבְּעוּ',      'Weqatal 3mp',    'Gen 21:31', '"both of them swore"',                          'R',  'שָׁבַע', 'Each binds himself individually — reflexive, not reciprocal'),
        SortEntry('16', 'תִּכָּרֵת',        'Imperfect 3fs',  'Gen 41:36', '"the land will not be cut off"',                'P',  'כָּרַת', 'Land receives the action of being cut off (depleted)'),
        SortEntry('17', 'נִלְחָם',          'Participle ms',  'Exo 14:25', '"the LORD is fighting for them"',               'SA', 'לָחַם',  'Niphal-only: the LORD fights (no Qal to contrast)'),
        SortEntry('18', 'הֵאָסְפוּ',        'Imperative 2mp', 'Gen 49:1',  '"gather yourselves!"',                          'P',  'אָסַף',  'Passive imperative: be gathered (assemble)'),
        SortEntry('19', 'וְנוֹעֲדוּ',       'Weqatal 3mp',    'Num 10:3',  '"all the congregation shall assemble"',         'RC', 'יָעַד',  'Congregation assembles mutually together'),
        SortEntry('20', 'נִחַמְתִּי',       'Weqatal 1cs',    'Gen 6:7',   '"I regret that I made them"',                   'SA', 'נָחַם',  'Niphal-only: I regret is the base meaning'),
        SortEntry('21', 'נְמַלְתֶּם',       'Weqatal 2mp',    'Gen 17:11', '"you shall be circumcised"',                    'P',  'מוּל',   'Males receive the action of circumcision'),
        SortEntry('22', 'נִצַּבְתָּ',       'Perfect 2ms',    'Exo 7:15',  '"station yourself to meet him"',                'R',  'נָצַב',  'Moses positions himself at the Nile'),
        SortEntry('23', 'לְהִלָּחֵם',       'Inf. Construct', 'Exo 17:10', '"to fight against Amalek"',                     'SA', 'לָחַם',  'Niphal-only: to fight — the inf. construct form'),
        SortEntry('24', 'יִמָּצֵא',         'Imperfect 3ms',  'Gen 44:9',  '"whoever is found [with the cup]"',             'P',  'מָצָא',  'Person discovered with cup — receives the finding'),
        SortEntry('25', 'הִמָּצֵא יִמָּצֵא', 'Inf. Abs. + Impl', 'Exo 22:3', '"if it is actually found in his possession"',  'P',  'מָצָא',  'Emphatic passive; doubling stresses the discovery'),
    ]

    def _build(self):
        self.add_instructions(
            'Classify each Niphal verb as P (Passive), R (Reflexive), RC (Reciprocal), '
            'or SA (Simple Action). Write your answer in the Function column. '
            'Answer key is on the last page.'
        )

        self.add_note(
            'P = Passive (subject receives the action)  |  '
            'R = Reflexive (subject acts on/for itself)  |  '
            'RC = Reciprocal (subjects act on one another)  |  '
            'SA = Simple Action (Niphal-only root; no distinct Qal meaning)'
        )

        self.add_sort_table(self._ENTRIES, show_answers=False)

        self.add_reflection([
            'Items 3, 14, 17, 20, and 23 are all Simple Action (לָחַם and נָחַם). What is the practical '
            'difference between a Niphal-only root and a root that simply lacks a Qal in the OT corpus?',
            'Compare items 7 and 12 (both שָׁבַע). The imperative and wayyiqtol appear in the same verse '
            '(Gen 47:31). How does the sequential narrative create a scene of formal oath-taking?',
            'Item 18 (הֵאָסְפוּ) is Passive, yet it is an imperative. Explain how a Niphal imperative '
            'can be both a command and passive in force.',
        ])

        self.add_answer_key_sort(self._ENTRIES)


def build_ch24_function_sort_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch24', 'exercises',
                               'ch24-function-sort')
    path = os.path.join(out_dir, 'ch24-function-sort.pdf')
    ex = Ch24FunctionSortExercise(
        title='Chapter 24 — Semantic Function Sorting',
        subtitle='BBH Chapter 24 · Niphal Strong Verbs',
    )
    return ex.save(path)


class Ch25WeakFormIdExercise(ExercisePDF):
    """Weak-Form Identification Drill — 52 items across 8 weak classes."""

    # (num, hebrew, conjugation, pgn, ref, gloss, class_label, root, note)
    _PART_A = [
        # Group 1 — III-א
        SortEntry('1',  'נִמְצָא',          'Perfect',          'Gen 44:12', '"it was found"',                         'III-א', 'מָצָא', 'Perfect 3ms — silent final א'),
        SortEntry('2',  'יִמָּצֵא',         'Imperfect',        'Gen 44:10', '"let it be found"',                      'III-א', 'מָצָא', 'Imperfect 3ms — tsere + silent א'),
        SortEntry('3',  'וַיִּמָּצֵא',      'Wayyiqtol',        'Gen 44:12', '"and it was found"',                     'III-א', 'מָצָא', 'Wayyiqtol 3ms — dagesh + final silent א'),
        SortEntry('4',  'הִמָּצֵא',         'Inf. Abs.',        'Exo 22:3',  '"actually found" (emph.)',               'III-א', 'מָצָא', 'Inf. Absolute (= inf. construct form)'),
        SortEntry('5',  'הַנִּמְצָא',       'Participle ms',    'Gen 47:14', '"that which was found"',                 'III-א', 'מָצָא', 'Participle ms — article + נִ + silent final א'),
        # Group 2 — III-ה
        SortEntry('6',  'נִגְלָה',          'Perfect',          'Isa 40:5',  '"it was revealed"',                      'III-ה', 'גָּלָה', 'Perfect 3ms — final ָה'),
        SortEntry('7',  'יִגָּלֶה',         'Imperfect',        'Isa 53:1',  '"it will be revealed"',                  'III-ה', 'גָּלָה', 'Imperfect 3ms — final ֶה (not tsere)'),
        SortEntry('8',  'וַיִּגָּל',        'Wayyiqtol',        'Num 24:4',  '"whose eyes are unveiled"',              'III-ה', 'גָּלָה', 'Wayyiqtol 3ms — apocopated (ה dropped)'),
        SortEntry('9',  'לְהִגָּלוֹת',      'Inf. Construct',   'Isa 49:9',  '"to show themselves"',                   'III-ה', 'גָּלָה', 'Inf. Construct — וֹת suffix'),
        SortEntry('10', 'וַיֵּרָא',         'Wayyiqtol',        'Gen 12:7',  '"and the LORD appeared"',               'III-ה', 'רָאָה', 'Wayyiqtol 3ms — apocopated + ר compensatory tsere'),
        # Group 3 — I-guttural
        SortEntry('11', 'נֶאֱמַר',          'Perfect',          'Exo 5:13',  '"it was said"',                          'I-guttural', 'אָמַר', 'Perfect 3ms — נֶ prefix + composite shewa'),
        SortEntry('12', 'יֵאָמֵר',          'Imperfect',        'Num 21:14', '"it is said"',                           'I-guttural', 'אָמַר', 'Imperfect 3ms — יֵ prefix; no dagesh in א'),
        SortEntry('13', 'וַיֵּאָמֵר',       'Wayyiqtol',        'Gen 10:9',  '"and it was said of him"',              'I-guttural', 'אָמַר', 'Wayyiqtol 3ms — וַיֵּ (not וַיִּ)'),
        SortEntry('14', 'הֵעָמֵד',          'Inf. Construct',   'Exo 9:16',  '"for this purpose I let you stand"',    'I-guttural', 'עָמַד', 'Inf. Construct — הֵ prefix; no dagesh in ע'),
        SortEntry('15', 'נֶאֱמָן',          'Participle ms',    'Deu 7:9',   '"faithful, trustworthy"',               'I-guttural', 'אָמַן', 'Participle ms — נֶ prefix + qamets under R2'),
        # Group 4 — I-נ
        SortEntry('16', 'נִגַּשׁ',          'Perfect',          'Gen 44:18', '"he drew near"',                         'I-נ', 'נָגַשׁ', 'Perfect 3ms — dagesh forte in ג (R2)'),
        SortEntry('17', 'וַיִּגַּשׁ',       'Wayyiqtol',        'Gen 44:18', '"and he drew near"',                     'I-נ', 'נָגַשׁ', 'Wayyiqtol 3ms — dagesh in ג (R2)'),
        SortEntry('18', 'נִצַּלְתֶּם',      'Perfect',          'Exo 12:27', '"you were delivered"',                   'I-נ', 'נָצַל', 'Perfect 2mp — dagesh in צ (R2)'),
        SortEntry('19', 'הִנָּצֵל',         'Imperative',       'Prov 6:3',  '"deliver yourself!"',                    'I-נ', 'נָצַל', 'Imperative 2ms — dagesh in נּ (R2)'),
        SortEntry('20', 'וַיִּנָּצֵל',      'Wayyiqtol',        'Gen 32:31', '"and Jacob was delivered"',              'I-נ', 'נָצַל', 'Wayyiqtol 3ms — dagesh in נּ (R2)'),
        # Group 5 — I-י
        SortEntry('21', 'נוֹלַד',           'Perfect',          'Gen 21:3',  '"he was born"',                          'I-י', 'יָלַד', 'Perfect 3ms — נוֹ prefix + patach under R2'),
        SortEntry('22', 'וַיִּוָּלֵד',      'Wayyiqtol',        'Gen 4:18',  '"and he was born"',                      'I-י', 'יָלַד', 'Wayyiqtol 3ms — וַיִּוָּ cluster'),
        SortEntry('23', 'יִוָּלֵד',         'Imperfect',        'Gen 17:17', '"shall a child be born?"',               'I-י', 'יָלַד', 'Imperfect 3ms — יִוָּ cluster + tsere'),
        SortEntry('24', 'בְּהִוָּלֶד',      'Inf. Construct',   'Gen 21:5',  '"when he was born"',                     'I-י', 'יָלַד', 'Inf. Construct — הִוָּ prefix + בְּ'),
        SortEntry('25', 'נוֹלָד',           'Participle ms',    '1 Kgs 13:2', '"one who will be born"',                 'I-י', 'יָלַד', 'Participle ms — נוֹ prefix + qamets (vs. patach in perfect)'),
        # Group 6 — III-ח/ע
        SortEntry('26', 'נִשְׁמַע',         'Perfect',          'Est 1:20',  '"it was heard"',                         'III-ch/ayin', 'שָׁמַע', 'Perfect 3ms — patach furtive before final ע'),
        SortEntry('27', 'יִשָּׁמַע',        'Imperfect',        'Exo 28:35', '"it shall be heard"',                    'III-ch/ayin', 'שָׁמַע', 'Imperfect 3ms — patach (not tsere) before ע; dagesh in R1'),
        SortEntry('28', 'וַיִּשָּׁמַע',     'Wayyiqtol',        'Gen 45:2',  '"and it was heard"',                     'III-ch/ayin', 'שָׁמַע', 'Wayyiqtol 3ms — patach before ע; no furtive'),
        SortEntry('29', 'הִשָּׁמַע',        'Inf. Construct',   'Deu 4:32',  '"to be heard"',                          'III-ch/ayin', 'שָׁמַע', 'Inf. Construct (= Imperative form) — patach before ע'),
        SortEntry('30', 'נִשְׁמָע',         'Participle ms',    'Ecc 12:13', '"that which is heard"',                  'III-ch/ayin', 'שָׁמַע', 'Participle ms — qamets + patach furtive before ע'),
        # Group 7 — Biconsonantal
        SortEntry('31', 'נָכוֹן',           'Perfect',          'Gen 41:32', '"it is established"',                    'Biconsonantal', 'כּוּן', 'Perfect 3ms — נָ prefix (qamets) + medial וֹ'),
        SortEntry('32', 'יִכּוֹן',          'Imperfect',        'Psa 93:2',  '"it is established"',                    'Biconsonantal', 'כּוּן', 'Imperfect 3ms — dagesh in R1 (Niphal assimilation) + contracted root'),
        SortEntry('33', 'נָכוֹן',           'Participle ms',    'Psa 57:8',  '"steadfast, firm"',                      'Biconsonantal', 'כּוּן', 'Participle ms — נָ prefix + vocalic structure = identical to perfect'),
        SortEntry('34', 'וַיִּקּוֹם',       'Wayyiqtol',        '(expected)', '"and it was established"',              'Biconsonantal', 'קוּם', 'Wayyiqtol 3ms — וַיִּ + dagesh in R1 + contracted root'),
        SortEntry('35', 'הִקּוֹם',          'Imperative',       '(expected)', '"be established!"',                     'Biconsonantal', 'קוּם', 'Imperative 2ms — הִ + dagesh in R1 + contracted root'),
        # Group 8 — Geminate
        SortEntry('36', 'נָסַב',            'Perfect',          'Josh 15:3', '"it went around"',                       'Geminate', 'סָבַב', 'Perfect 3ms — נָ prefix (qamets), same as Biconsonantal; root ס-ב-ב has R2=R3'),
        SortEntry('37', 'וַיִּסֹּב',        'Wayyiqtol',        '1 Sam 7:16', '"and he went on circuit"',               'Geminate', 'סָבַב', 'Wayyiqtol 3ms — dagesh forte in ב (R2=R3 doubled)'),
        SortEntry('38', 'יִסֹּב',           'Imperfect',        'Josh 19:34', '"it turns around"',                      'Geminate', 'סָבַב', 'Imperfect 3ms — dagesh forte in ב; holem in contracted root'),
        SortEntry('39', 'הִסֹּב',           'Imperative',       '2 Sam 18:30', '"turn aside!"',                         'Geminate', 'סָבַב', 'Imperative 2ms — הִ + dagesh forte in ב'),
        SortEntry('40', 'נָסַב',            'Participle ms',    'Psa 26:6',  '"going around" (participial)',            'Geminate', 'סָבַב', 'Participle ms — נָ prefix, identical to perfect 3ms; context determines'),
    ]

    _PART_B = [
        SortEntry('41', 'תֵרָאֶה',          'Imperfect/Jussive', 'Gen 1:9',   '"let it appear"',                        'III-ה',         'רָאָה', '3fs — ר compensatory + final ֶה'),
        SortEntry('42', 'וַיִּוָּדַע',      'Wayyiqtol',        'Est 2:22',  '"the matter became known"',             'I-י',           'יָדַע', '3ms — וַיִּוָּ; patach under R2 (יָדַע class)'),
        SortEntry('43', 'נֶעֱמַד',          'Perfect',          '1 Sam 17:16', '"he took his stand"',                  'I-guttural',    'עָמַד', '3ms — נֶ prefix + composite shewa under ע'),
        SortEntry('44', 'וַיִּמָּצְאוּ',    'Wayyiqtol',        'Gen 47:14', '"all the silver was gathered"',          'III-א',         'מָצָא', '3mp — dagesh + 3mp ending + silent א'),
        SortEntry('45', 'נוֹדַע',           'Perfect',          'Gen 41:21', '"it was not known"',                     'I-י',           'יָדַע', '3ms — נוֹ prefix + patach (perfect, not participle)'),
        SortEntry('46', 'וַיִּגַּשׁ',       'Wayyiqtol',        'Gen 44:18', '"Judah drew near"',                      'I-נ',           'נָגַשׁ', '3ms — dagesh in ג (R2); root נ invisible'),
        SortEntry('47', 'הֵרָאֵה',          'Imperative',       '1 Kgs 18:1', '"show yourself!"',                       'III-ה',         'רָאָה', '2ms — הֵ compensatory + final ֵה (imperative)'),
        SortEntry('48', 'נִשְׁלַח',         'Perfect',          'Est 3:13',  '"letters were sent"',                    'III-ch/ayin',   'שָׁלַח', '3ms — patach furtive before final ח'),
        SortEntry('49', 'נָכוֹן',           'Perfect/Participle', 'Exo 34:2', '"be ready"',                             'Biconsonantal', 'כּוּן', 'נָ prefix (qamets) is the biconsonantal Niphal marker'),
        SortEntry('50', 'וַיִּסֹּב',        'Wayyiqtol',        '2 Sam 5:23', '"and he circled behind them"',          'Geminate',      'סָבַב', '3ms — וַיִּ + dagesh forte in ב (R2=R3); root ס-ב-ב is Geminate, not hollow'),
        SortEntry('51', 'נִמְצְאוּ',        'Perfect',          'Exo 12:19', '"whoever is found"',                     'III-א',         'מָצָא', '3cp — 3cp ending + final silent א'),
        SortEntry('52', 'יֵעָמְדוּ',        'Imperfect',        'Num 27:22', '"they shall stand before"',              'I-guttural',    'עָמַד', '3mp — יֵ prefix; no dagesh in ע; 3mp ending'),
    ]

    def _build(self):
        self.add_instructions(
            'Part A (1–40): forms are grouped by weak class. Identify class, parse conjugation + PGN, '
            'and give the root. '
            'Part B (41–52): mixed classes — identify the class first, then parse. '
            'Answer key is on the last page.'
        )

        self.add_note(
            'Classes: III-א (silent final א)  |  III-ה (final ָה / ֶה / וֹת / apocopated)  |  '
            'III-ch/ayin (patach furtive before ח/ע; patach in short forms)  |  '
            'I-guttural (נֶ / יֵ / הֵ prefix; no dagesh in R1)  |  '
            'I-נ (dagesh forte in R2; root נ invisible)  |  '
            'I-י (נוֹ prefix in perfect/ptc; יִוָּ / הִוָּ in impf/wayyiqtol/imv/inf)  |  '
            'Biconsonantal (נָ prefix in perfect/ptc; dagesh in R1 elsewhere)  |  '
            'Geminate (נָ prefix in perfect/ptc — same as Biconsonantal!; dagesh forte in R2/R3 elsewhere; R2=R3 is the class marker)'
        )

        self.add_section_heading('Part A — By Class')
        self.add_sort_table(self._PART_A, show_answers=False)

        self.add_section_heading('Part B — Mixed')
        self.add_sort_table(self._PART_B, show_answers=False)

        self.add_reflection([
            'Items 1 and 5 (III-א) are both pointed נִמְצָא — perfect 3ms and participle ms are identical. '
            'What contextual or syntactic clues allow you to distinguish them in a real text?',
            'Compare items 8 (וַיִּגָּל, III-ה) and 17 (וַיִּגַּשׁ, I-נ). Both show a short form after '
            'וַיִּ with a dagesh. How do you tell them apart?',
            'Items 10 (וַיֵּרָא) and 13 (וַיֵּאָמֵר) both use the prefix וַיֵּ instead of the expected '
            'וַיִּ. Is this the same phonological rule in both cases?',
            'Items 21 (נוֹלַד) and 25 (נוֹלָד) differ only in the vowel under R2. Which is the perfect '
            'and which is the participle, and how would each behave differently in a clause?',
            'Items 26 (נִשְׁמַע, III-ח/ע) and item 1 (נִמְצָא, III-א) both begin with נִ. What '
            'distinguishes them visually, and why does the patach furtive appear before שָׁמַע but not מָצָא?',
            'Items 31 and 33 both show נָכוֹן (Biconsonantal). How does this perfect/participle ambiguity '
            'parallel the III-א problem in question 1, and what does it reveal about the general challenge '
            'of Niphal weak forms?',
            'Items 36 and 40 (Geminate) are both pointed נָסַב — perfect 3ms and participle ms are '
            'identical in the Geminate class, just like the Biconsonantal class (items 31/33). '
            'Given a form like נָסַב, how do you even know whether the root is Geminate (ס-ב-ב) '
            'or Biconsonantal (a hollow root)? What information outside the vocalization must you use?',
        ])

        self.add_answer_key_sort(self._PART_A + self._PART_B)


def build_ch25_weak_form_id_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch25', 'exercises',
                               'ch25-weak-form-id')
    path = os.path.join(out_dir, 'ch25-weak-form-id.pdf')
    ex = Ch25WeakFormIdExercise(
        title='Chapter 25 — Niphal Weak-Form Identification Drill',
        subtitle='BBH Chapter 25 · Niphal Weak Verbs',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Chapter 27 — Hiphil Weak Verbs
# ---------------------------------------------------------------------------

class Ch27Exercise(ExercisePDF):
    """Passage exercise — 18 Hiphil weak verbs from Gen, Exo, Num, Deu."""

    def _render_passages(self, show_answers: bool):

        self.add_section_heading('Part A — Genesis and Exodus (items 1–10)')

        self.add_passage(PassageBlock('Gen 1:5',
            'וַיִּקְרָא אֱלֹהִים לָאוֹר יוֹם וַיַּקְרֵא לַחֹשֶׁךְ לָיְלָה',
            '"and he [1] ____ the darkness Night"'))
        self.add_verb_table([VerbEntry('1', 'וַיַּקְרֵא', 'Wayyiqtol', '3ms', 'קָרָא', 'III-א — he called / proclaimed')], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 6:18',
            'וַהֲקִמֹתִי אֶת־בְּרִיתִי אִתְּךָ',
            '"but I [2] ____ my covenant with you"'))
        self.add_verb_table([VerbEntry('2', 'וַהֲקִמֹתִי', 'Weqatal', '1cs', 'קוּם', 'Biconsonantal — I will establish')], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 8:20',
            'הֶעֱלָה נֹחַ עֹלֹת עַל הַמִּזְבֵּחַ',
            '"Noah [3] ____ burnt offerings on the altar"'))
        self.add_verb_table([VerbEntry('3', 'הֶעֱלָה', 'Perfect', '3ms', 'עָלָה', 'III-ה + I-guttural — he offered up')], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 15:7',
            'אֲנִי יְהוָה אֲשֶׁר הוֹצֵאתִיךָ מֵאוּר כַּשְׂדִּים',
            '"I am the LORD who [4] ____ from Ur of the Chaldeans"'))
        self.add_verb_table([VerbEntry('4', 'הוֹצֵאתִיךָ', 'Perfect', '1cs + 2ms', 'יָצָא', 'I-י — I brought you out')], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 22:2',
            'וַיַּעַל שָׁם עֹלָה',
            '"and he [5] ____ a burnt offering there"'))
        self.add_verb_table([VerbEntry('5', 'וַיַּעַל', 'Wayyiqtol', '3ms', 'עָלָה', 'III-ה — he offered up (apocopated)')], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 2:21',
            'וַיַּפֵּל יְהוָה אֱלֹהִים תַּרְדֵּמָה עַל הָאָדָם',
            '"the LORD God [6] ____ a deep sleep upon the man"'))
        self.add_verb_table([VerbEntry('6', 'וַיַּפֵּל', 'Wayyiqtol', '3ms', 'נָפַל', 'I-נ — he caused to fall / cast')], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 9:16',
            'וְאוּלָם בַּעֲבוּר זֹאת הֶעֱמַדְתִּיךָ',
            '"but for this purpose I [7] ____ you"'))
        self.add_verb_table([VerbEntry('7', 'הֶעֱמַדְתִּיךָ', 'Perfect', '1cs + 2ms', 'עָמַד', 'I-guttural — I raised you up / stationed you')], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 20:2',
            'אָנֹכִי יְהוָה אֱלֹהֶיךָ אֲשֶׁר הוֹצֵאתִיךָ מֵאֶרֶץ מִצְרַיִם',
            '"I am the LORD your God, who [8] ____ of the land of Egypt"'))
        self.add_verb_table([VerbEntry('8', 'הוֹצֵאתִיךָ', 'Perfect', '1cs + 2ms', 'יָצָא', 'I-י — I brought you out')], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 33:18',
            'וַיֹּאמַר הַרְאֵנִי נָא אֶת־כְּבֹדֶךָ',
            '"and he said, [9] ____ your glory, please"'))
        self.add_verb_table([VerbEntry('9', 'הַרְאֵנִי', 'Imperative', '2ms + 1cs', 'רָאָה', 'III-ה — show me')], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 40:2',
            'הָקֵם אֶת־מִשְׁכַּן אֹהֶל מוֹעֵד',
            '"[10] ____ the tabernacle of the tent of meeting"'))
        self.add_verb_table([VerbEntry('10', 'הָקֵם', 'Imperative', '2ms', 'קוּם', 'Biconsonantal — set up / erect')], show_answers=show_answers)

        self.add_section_break()
        self.add_section_heading('Part B — Numbers and Deuteronomy (items 11–18)')

        self.add_passage(PassageBlock('Num 27:19',
            'הַעֲמֵד אֹתוֹ לִפְנֵי אֶלְעָזָר הַכֹּהֵן',
            '"[11] ____ him before Eleazar the priest"'))
        self.add_verb_table([VerbEntry('11', 'הַעֲמֵד', 'Imperative', '2ms', 'עָמַד', 'I-guttural — set him / station him')], show_answers=show_answers)

        self.add_passage(PassageBlock('Deu 18:15',
            'נָבִיא מִקִּרְבְּךָ יָקִים לְךָ יְהוָה אֱלֹהֶיךָ',
            '"a prophet like me the LORD [12] ____ for you"'))
        self.add_verb_table([VerbEntry('12', 'יָקִים', 'Imperfect', '3ms', 'קוּם', 'Biconsonantal — will raise up')], show_answers=show_answers)

        self.add_passage(PassageBlock('Deu 4:10',
            'הַשְׁמַע אֶת־הָעָם אֶת־דִּבְרֵי',
            '"[13] ____ the people these words"'))
        self.add_verb_table([VerbEntry('13', 'הַשְׁמַע', 'Imperative', '2ms', 'שָׁמַע', 'III-ח/ע — make them hear')], show_answers=show_answers)

        self.add_passage(PassageBlock('Deu 8:14',
            'אֲשֶׁר הוֹצִיאֲךָ מֵאֶרֶץ מִצְרַיִם',
            '"who [14] ____ of the land of Egypt"'))
        self.add_verb_table([VerbEntry('14', 'הוֹצִיאֲךָ', 'Perfect', '3ms + 2ms', 'יָצָא', 'I-י — he brought you out')], show_answers=show_answers)

        self.add_passage(PassageBlock('Deu 8:14',
            'הַמּוֹצִיאֲךָ מֵאֶרֶץ מִצְרַיִם',
            '"[15] ____ of the land of Egypt (substantival participle)"'))
        self.add_verb_table([VerbEntry('15', 'הַמּוֹצִיאֲךָ', 'Participle', 'ms', 'יָצָא', 'I-י — the one who brought you out')], show_answers=show_answers)

        self.add_passage(PassageBlock('Num 1:51',
            'וְהֵקִים אֶת־הַמִּשְׁכָּן',
            '"and [16] ____ the tabernacle"'))
        self.add_verb_table([VerbEntry('16', 'וְהֵקִים', 'Weqatal', '3ms', 'קוּם', 'Biconsonantal — he shall set up')], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 3:17',
            'לְהַעֲלוֹת אֶתְכֶם מֵעֳנִי מִצְרַיִם',
            '"[17] ____ you out of the affliction of Egypt"'))
        self.add_verb_table([VerbEntry('17', 'לְהַעֲלוֹת', 'Inf. Construct', '—', 'עָלָה', 'III-ה + I-guttural — to bring up')], show_answers=show_answers)

        self.add_passage(PassageBlock('Isa 48:6',
            'מֵעַתָּה אַשְׁמִיעֲכֶם חֲדָשׁוֹת',
            '"from now on [18] ____ new things"'))
        self.add_verb_table([VerbEntry('18', 'אַשְׁמִיעֲכֶם', 'Imperfect', '1cs + 2mp', 'שָׁמַע', 'III-ח/ע — I announce to you')], show_answers=show_answers)

        self.add_section_break()
        self.add_section_heading('Part C — Distractor Check')
        self.add_note(
            'These three verbs are drawn from the same corpus. None are Hiphil. '
            'Answer "No" for Hiphil? and complete the full parse.'
        )

        self.add_passage(PassageBlock('Gen 22:3',
            'וַיַּשְׁכֵּם אַבְרָהָם בַּבֹּקֶר וַיֵּלֶךְ אֶל הַמָּקוֹם',
            '"And Abraham rose early in the morning and [D1] ____ to the place."'))
        self.add_verb_table([VerbEntry('D1', 'וַיֵּלֶךְ', 'Wayyiqtol', '3ms', 'הָלַךְ', 'NOT Hiphil — Qal: and he went; no הִ/הַ prefix; plain Qal of הָלַךְ')], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 21:3',
            'וַיִּקְרָא אַבְרָהָם אֶת שֶׁם בְּנוֹ אֲשֶׁר נוֹלַד לוֹ',
            '"And Abraham called the name of his son who [D2] ____ to him."'))
        self.add_verb_table([VerbEntry('D2', 'נוֹלַד', 'Perfect', '3ms', 'יָלַד', 'NOT Hiphil — Niphal passive: was born; נוֹ- prefix = Niphal of I-י root')], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 2:17',
            'כִּי בְּיוֹם אֲכָלְךָ מִמֶּנּוּ מוֹת תָּמוּת',
            '"for in the day you eat of it you shall surely [D3] ____."'))
        self.add_verb_table([VerbEntry('D3', 'תָּמוּת', 'Imperfect', '2ms', 'מוּת', 'NOT Hiphil — Qal: you will die; תָּ- prefix = Qal imperfect 2ms; no הַ- Hiphil prefix')], show_answers=show_answers)

    def _build(self):
        self.add_instructions(
            'Most highlighted verbs are Hiphil forms. For each: (1) Is it Hiphil? (Yes / No); '
            '(2) parse — conjugation, person-gender-number, root; '
            '(3) state the weak class '
            '(I-guttural / III-ch/ayin / III-aleph / III-he / Pe-Nun / Pe-Yod / Biconsonantal); '
            '(4) give a brief causative gloss in context. '
            'Part C contains distractor verbs — not Hiphil. Answer "No" and parse fully.'
        )
        self._render_passages(show_answers=False)
        self.add_section_heading('Answer Key')
        self._render_passages(show_answers=True)


def build_ch27_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch27', 'exercises',
                               'ch27-passage-exercise')
    path = os.path.join(out_dir, 'ch27-passage-exercise.pdf')
    ex = Ch27Exercise(
        title='Chapter 27 — "Spot the Hiphil" Passage Exercise',
        subtitle='BBH Chapter 27 · Hiphil Weak Verbs',
    )
    return ex.save(path)


class Ch27WeakFormIdExercise(ExercisePDF):
    """Weak-Form Identification Drill — 50 items across 8 weak classes."""

    _PART_A = [
        # Group 1 — I-guttural
        SortEntry('1',  'הֶעֱמִיד',      'Perfect',      '1 Kgs 7:21', '"he set up"',              'I-guttural',    'עָמַד', 'seghol under הֶ + hateph-seghol under ע'),
        SortEntry('2',  'וַיַּעֲמֵד',    'Wayyiqtol',    '2 Chr 4:4',  '"and he set it"',           'I-guttural',    'עָמַד', 'patach prefix + composite shewa under ע'),
        SortEntry('3',  'יַעֲמִיד',      'Imperfect',    'Psa 107:29', '"he causes to stand"',      'I-guttural',    'עָמַד', 'patach prefix + composite shewa; no dagesh'),
        SortEntry('4',  'הַעֲמֵד',       'Imperative',   'Num 27:19',  '"set him before"',          'I-guttural',    'עָמַד', 'הַ + composite shewa under ע + tsere'),
        SortEntry('5',  'מַעֲמִיד',      'Participle',   'Neh 4:7',    '"one who stations"',        'I-guttural',    'עָמַד', 'מַ + composite shewa under ע + chiriq'),
        # Group 2 — III-ח/ע
        SortEntry('6',  'הִשְׁמִיעַ',    'Perfect',      'Isa 48:6',   '"he caused to hear"',       'III-ch/ayin',   'שָׁמַע', 'patach furtive before final ע in 3ms'),
        SortEntry('7',  'וַיַּשְׁלַח',   'Wayyiqtol',    'Gen 3:23',   '"and he sent out"',         'III-ch/ayin',   'שָׁלַח', 'patach (not tsere) before final ח'),
        SortEntry('8',  'יַשְׁמִיעַ',    'Imperfect',    'Isa 42:2',   '"he will cause to hear"',   'III-ch/ayin',   'שָׁמַע', 'patach furtive before final ע'),
        SortEntry('9',  'הַשְׁמַע',      'Imperative',   'Deu 4:10',   '"make them hear"',          'III-ch/ayin',   'שָׁמַע', 'patach before final ע (not tsere)'),
        SortEntry('10', 'מַשְׁמִיעַ',    'Participle',   'Isa 41:26',  '"one who announces"',       'III-ch/ayin',   'שָׁמַע', 'מַ + chiriq-yod + patach furtive before ע'),
        # Group 3 — III-א
        SortEntry('11', 'הִמְצִיא',      'Perfect',      'Neh 9:15',   '"he provided"',             'III-aleph',     'מָצָא', 'chiriq-yod + silent final א'),
        SortEntry('12', 'וַיַּמְצֵא',    'Wayyiqtol',    '2 Chr 2:13', '"and he provided"',         'III-aleph',     'מָצָא', 'tsere + silent final א'),
        SortEntry('13', 'יַמְצִיא',      'Imperfect',    'Pro 8:35',   '"he will cause to find"',   'III-aleph',     'מָצָא', 'chiriq-yod + silent final א'),
        SortEntry('14', 'וַיַּקְרֵא',    'Wayyiqtol',    'Gen 1:5',    '"and he called"',           'III-aleph',     'קָרָא', 'tsere + silent final א'),
        SortEntry('15', 'מַקְרִיא',      'Participle',   'Neh 8:3',    '"one who reads aloud"',     'III-aleph',     'קָרָא', 'מַ + chiriq-yod + silent final א'),
        # Group 4 — III-ה
        SortEntry('16', 'הֶעֱלָה',       'Perfect',      'Gen 8:20',   '"he offered up"',           'III-he',        'עָלָה', 'qamets + ה ending; seghol under הֶ'),
        SortEntry('17', 'וַיַּעַל',      'Wayyiqtol',    'Gen 22:2',   '"and he went up"',          'III-he',        'עָלָה', 'apocopated — ה dropped; short patach under R2'),
        SortEntry('18', 'יַעֲלֶה',       'Imperfect',    'Lev 14:20',  '"he shall offer up"',       'III-he',        'עָלָה', 'seghol + ה ending'),
        SortEntry('19', 'הַרְאֵה',       'Imperative',   'Exo 33:18',  '"show me"',                 'III-he',        'רָאָה', 'tsere + ה retained (not apocopated)'),
        SortEntry('20', 'לְהַעֲלוֹת',   'Inf. Construct', 'Exo 3:17',  '"to bring up"',             'III-he',        'עָלָה', 'ends in וֹת — strong III-ה marker'),
        # Group 5 — I-נ
        SortEntry('21', 'הִפִּיל',       'Perfect',      'Gen 2:21',   '"he caused to fall"',       'I-nun',         'נָפַל', 'dagesh forte in R2 (פ); נ assimilated'),
        SortEntry('22', 'וַיַּפֵּל',     'Wayyiqtol',    'Gen 2:21',   '"and he cast"',             'I-nun',         'נָפַל', 'patach prefix + dagesh in R2 + tsere'),
        SortEntry('23', 'יַפִּיל',       'Imperfect',    'Pro 19:15',  '"causes to fall"',          'I-nun',         'נָפַל', 'patach prefix + dagesh in R2 + chiriq'),
        SortEntry('24', 'הַגֵּשׁ',       'Imperative',   'Gen 27:25',  '"bring near"',              'I-nun',         'נָגַשׁ', 'הַ + dagesh forte in R2 (ג) + tsere'),
        SortEntry('25', 'מַגִּישׁ',      'Participle',   'Mal 1:7',    '"one who brings near"',     'I-nun',         'נָגַשׁ', 'מַ + dagesh in R2 + chiriq'),
        # Group 6 — I-י
        SortEntry('26', 'הוֹצִיא',       'Perfect',      'Gen 15:7',   '"he brought out"',          'I-yod',         'יָצָא', 'הוֹ prefix (holem-vav) — I-yod/vav signature'),
        SortEntry('27', 'וַיּוֹצֵא',     'Wayyiqtol',    'Gen 1:12',   '"and it brought forth"',    'I-yod',         'יָצָא', 'וַיּוֹ prefix — dagesh in יּ + holem-vav'),
        SortEntry('28', 'יוֹרִיד',       'Imperfect',    '1 Sam 2:6',  '"he brings down"',          'I-yod',         'יָרַד', 'יוֹ prefix (holem-vav)'),
        SortEntry('29', 'הוֹרֵד',        'Imperative',   'Gen 42:38',  '"bring down"',              'I-yod',         'יָרַד', 'הוֹ prefix (not הַ) + tsere'),
        SortEntry('30', 'מוֹצִיא',       'Participle',   'Deu 8:14',   '"the one who brings out"',  'I-yod',         'יָצָא', 'מוֹ prefix (holem-vav) — not מַ'),
        # Group 7 — Biconsonantal
        SortEntry('31', 'הֵקִים',        'Perfect',      'Gen 6:18',   '"he established"',          'Biconsonantal', 'קוּם', 'הֵ prefix (tsere) — not הִ (hiriq)'),
        SortEntry('32', 'וַיָּקֶם',      'Wayyiqtol',    'Gen 23:20',  '"and it was confirmed"',    'Biconsonantal', 'קוּם', 'qamets prefix + apocopated seghol final'),
        SortEntry('33', 'יָקִים',        'Imperfect',    'Deu 18:15',  '"he will raise up"',        'Biconsonantal', 'קוּם', 'qamets under prefix consonant (יָ)'),
        SortEntry('34', 'הָקֵם',         'Imperative',   'Exo 40:2',   '"set up"',                  'Biconsonantal', 'קוּם', 'הָ prefix (qamets) + tsere'),
        SortEntry('35', 'מֵקִים',        'Participle',   '1 Sam 2:8',  '"one who raises up"',       'Biconsonantal', 'קוּם', 'מֵ prefix (tsere) — not מַ'),
        # Group 8 — Geminate
        SortEntry('36', 'הֵסֵב',         'Perfect',      '1 Kgs 21:4', '"he turned his face"',      'Geminate', 'סָבַב', 'הֵ prefix (tsere) — same as Biconsonantal הֵקִים; root ס-ב-ב has R2=R3'),
        SortEntry('37', 'וַיָּסֶב',      'Wayyiqtol',    'Josh 6:14',  '"and they marched around"', 'Geminate', 'סָבַב', 'qamets prefix + apocopated seghol — same pattern as Biconsonantal וַיָּקֶם'),
        SortEntry('38', 'יָסֵב',         'Imperfect',    'Isa 44:20',  '"it leads astray"',         'Geminate', 'סָבַב', 'qamets under prefix (יָ) — same as Biconsonantal יָקִים; root knowledge required'),
        SortEntry('39', 'הָסֵב',         'Imperative',   '2 Sam 2:22', '"turn aside!"',             'Geminate', 'סָבַב', 'הָ prefix (qamets) — same as Biconsonantal הָקֵם; only root distinguishes'),
        SortEntry('40', 'מֵסֵב',         'Participle',   '(expected)', '"one who surrounds"',       'Geminate', 'סָבַב', 'מֵ prefix (tsere) — same as Biconsonantal מֵקִים; Geminate class requires root knowledge'),
    ]

    _PART_B = [
        SortEntry('41', 'וַיַּשְׁמַע',   'Wayyiqtol',    '1 Sam 15:14', '"and he made heard"',       'III-ch/ayin',   'שָׁמַע', 'patach before final ע (not tsere) — guttural forces lowering'),
        SortEntry('42', 'הֵשִׂים',        'Perfect',       'Gen 45:9',    '"he made / placed"',        'Biconsonantal', 'שִׂים',  'הֵ prefix (tsere); root שׂ-י-מ contains medial hireq-yod vowel letter = Biconsonantal'),
        SortEntry('43', 'וַיַּעַל',       'Wayyiqtol',     'Gen 22:2',    '"and he went up"',          'III-he',        'עָלָה', 'apocopated: ה dropped'),
        SortEntry('44', 'הִגִּישׁ',       'Perfect',       'Amos 9:13',   '"he brought near"',         'I-nun',         'נָגַשׁ', 'dagesh forte in R2 (ג)'),
        SortEntry('45', 'הָסֵב',          'Imperative',    '2 Sam 5:23',  '"circle around behind them"', 'Geminate',     'סָבַב', 'הָ prefix (qamets) — looks exactly like Biconsonantal הָקֵם; root ס-ב-ב has R2=R3 = Geminate'),
        SortEntry('46', 'הֶרְאָה',        'Perfect',       'Exo 25:9',    '"he showed"',               'III-he',        'רָאָה', 'qamets + ה ending; seghol under הֶ'),
        SortEntry('47', 'וַיּוֹרֶד',      'Wayyiqtol',     'Gen 42:38',   '"and he brought down"',     'I-yod',         'יָרַד', 'וַיּוֹ prefix uniquely identifies I-yod Hiphil'),
        SortEntry('48', 'מַעֲמִידִים',    'Participle mp', 'Neh 4:7',     '"those who station"',       'I-guttural',    'עָמַד', 'מַ + composite shewa under ע + chiriq + ים'),
        SortEntry('49', 'הַמְצֵא',        'Imperative',    '(expected)',  '"cause to find"',           'III-aleph',     'מָצָא', 'tsere + silent final א; הַ prefix (patach)'),
        SortEntry('50', 'וָאָקִים',       'Wayyiqtol',     'Exo 6:4',     '"and I established"',       'Biconsonantal', 'קוּם', 'וָאָ (1cs wayyiqtol) + qamets + chiriq-yod medial vowel letter = Biconsonantal'),
    ]

    def _build(self):
        self.add_instructions(
            'Part A (1–40): forms are grouped by weak class (5 per class). '
            'Identify conjugation + PGN, and give the root. '
            'Part B (41–50): mixed classes — identify the class first, then parse. '
            'Answer key is on the last page.'
        )

        self.add_note(
            'Classes: I-guttural (he prefix seghol; composite shewa under R1)  |  '
            'III-ch/ayin (patach furtive before final guttural)  |  '
            'III-aleph (silent final aleph; chiriq-yod or tsere before it)  |  '
            'III-he (qamets+he perfect; seghol+he impf/ptc; apocopated wayyiqtol; vot inf.cstr)  |  '
            'I-nun (dagesh forte in R2 throughout)  |  '
            'I-yod (ho/yo/mo prefix pattern)  |  '
            'Biconsonantal (he+tsere perfect; qamets impf/wayyiqtol; ha+qamets imv/inf; me+tsere ptc)  |  '
            'Geminate (same prefixes as Biconsonantal! R2=R3 is the only distinguishing feature; requires root knowledge)'
        )

        self.add_section_heading('Part A — By Class')
        self.add_sort_table(self._PART_A, show_answers=False)

        self.add_section_heading('Part B — Mixed')
        self.add_sort_table(self._PART_B, show_answers=False)

        self.add_reflection([
            'Compare הִמְצִיא (III-aleph perfect 3ms) and הַמְצֵא (III-aleph imperative 2ms). '
            'Both end with silent final aleph. How do you distinguish them? '
            'What is the key difference in the prefix vowel?',
            'הַשְׁמַע (III-ch/ayin imperative) and הַעֲמֵד (I-guttural imperative) both begin '
            'with the ha- prefix. How does the vowel under R1 differ? What does that tell you about the class?',
            'וַיַּשְׁלַח (III-ch/ayin wayyiqtol) and וַיַּקְרֵא (III-aleph wayyiqtol) both have '
            'patach under the wayyiqtol prefix. The difference is in the final vowel. '
            'Explain what happens to the Hiphil tsere in each case and why.',
            'Compare הוֹרֵד (I-yod imperative 2ms) and הָקֵם (Biconsonantal imperative 2ms). '
            'Both have a long prefix vowel rather than the patach of the strong Hiphil imperative. '
            'What prefix vowel does each use, and how can you tell them apart?',
            'Items 36-40 (Geminate) and items 31-35 (Biconsonantal) share nearly identical vowel '
            'patterns in every conjugation: he+tsere perfect, qamets imperfect/wayyiqtol, '
            'ha+qamets imperative, me+tsere participle. What is the only reliable way to determine '
            'whether a Hiphil form belongs to the Geminate class or the Biconsonantal class? '
            'Why can the vocalization alone not always resolve this question?',
        ])

        self.add_answer_key_sort(self._PART_A + self._PART_B)


def build_ch27_weak_form_id_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch27', 'exercises',
                               'ch27-weak-form-id')
    path = os.path.join(out_dir, 'ch27-weak-form-id.pdf')
    ex = Ch27WeakFormIdExercise(
        title='Chapter 27 — Hiphil Weak-Form Identification Drill',
        subtitle='BBH Chapter 27 · Hiphil Weak Verbs',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Chapter 27 — Niphal–Hiphil Contrast Drill
# ---------------------------------------------------------------------------

class Ch27NHContrastExercise(ExercisePDF):
    """Niphal–Hiphil Contrast Drill — 20 items across both stems."""

    _PART_A = [
        NHEntry('1',  'נִשְׁמַע',     'Est 1:20',  '"the decree ___ throughout the kingdom"',   'Niphal', 'Perfect',    '3ms', 'שָׁמַע · III-ח/ע',         'was heard',              'נִ prefix + patach furtive before ע = Niphal III-ח/ע perfect'),
        NHEntry('2',  'הִשְׁמִיעַ',   'Isa 48:6',  '"I ___ you new things"',                    'Hiphil', 'Perfect',    '3ms', 'שָׁמַע · III-ח/ע',         'caused to hear / announced', 'הִ + chiriq-yod + patach furtive before ע = Hiphil III-ח/ע perfect'),
        NHEntry('3',  'יִמָּצֵא',     'Gen 44:10', '"he with whom it is ___ shall be my servant"', 'Niphal', 'Imperfect', '3ms', 'מָצָא · III-א',            'is found',               'יִמָּ (dagesh in מ = Niphal assimilation) + tsere + silent א'),
        NHEntry('4',  'הִמְצִיא',     'Neh 9:15',  '"You ___ them bread from heaven"',           'Hiphil', 'Perfect',    '3ms', 'מָצָא · III-א',            'provided / caused to find', 'הִ + chiriq-yod + silent final א = Hiphil III-א perfect'),
        NHEntry('5',  'נִגְלָה',      'Isa 40:5',  '"the glory of the LORD shall ___"',          'Niphal', 'Perfect',    '3ms', 'גָּלָה · III-ה',           'was revealed',           'נִ prefix + final ָה = Niphal III-ה perfect'),
        NHEntry('6',  'הֶעֱלָה',      'Gen 8:20',  '"Noah ___ burnt offerings on the altar"',    'Hiphil', 'Perfect',    '3ms', 'עָלָה · III-ה + I-gutt.', 'offered up',             'הֶ prefix + hateph-seghol under ע + qamets + ה = Hiphil III-ה perfect'),
        NHEntry('7',  'וַיִּגַּשׁ',   'Gen 44:18', '"Judah ___ him and said"',                  'Niphal', 'Wayyiqtol',  '3ms', 'נָגַשׁ · I-נ',             'drew near (reflexive)',   'וַיִּ + dagesh in ג (Niphal I-נ assimilation) without הִ prefix'),
        NHEntry('8',  'הִגִּישׁ',     'Amos 9:13', '"the one who ___ grain offering"',           'Hiphil', 'Perfect',    '3ms', 'נָגַשׁ · I-נ',             'brought near',           'הִ prefix + dagesh in ג (R2); contrast Niphal וַיִּגַּשׁ'),
    ]

    _PART_B = [
        NHEntry('9',  'נוֹלַד',       'Gen 21:3',  '"a son ___ to Abraham"',                    'Niphal', 'Perfect',    '3ms', 'יָלַד · I-י',              'was born',               'נוֹ prefix = Niphal I-י perfect; patach under R2 (not qamets of participle)'),
        NHEntry('10', 'יּוֹלֶד',      'Gen 5:3',   '"Adam ___ a son in his own likeness"',      'Hiphil', 'Wayyiqtol',  '3ms', 'יָלַד · I-י',              'fathered / begat',       'וַיּוֹ prefix (dagesh in יּ + holem-vav) = Hiphil I-י wayyiqtol'),
        NHEntry('11', 'יִוָּלֵד',     'Gen 17:17', '"shall a child ___ to a man of 100 years?"', 'Niphal', 'Imperfect',  '3ms', 'יָלַד · I-י',              'shall be born',          'יִוָּ cluster (dagesh in ו) = Niphal I-י imperfect; contrast Hiphil יוֹ'),
        NHEntry('12', 'יוֹרִיד',      '1 Sam 2:6', '"the LORD ___ to Sheol and raises up"',     'Hiphil', 'Imperfect',  '3ms', 'יָרַד · I-י',              'brings down',            'יוֹ prefix (holem-vav, no dagesh in ו) = Hiphil I-י imperfect'),
        NHEntry('13', 'וַיִּוָּדַע',  'Est 2:22',  '"the matter ___ to Mordecai"',              'Niphal', 'Wayyiqtol',  '3ms', 'יָדַע · I-י',              'became known',           'וַיִּוָּ cluster = Niphal I-י wayyiqtol'),
        NHEntry('14', 'הֵקִים',       'Gen 6:18',  '"I will ___ my covenant with you"',         'Hiphil', 'Perfect',    '3ms', 'קוּם · Biconsonantal',     'established',            'הֵ prefix (tsere) = Hiphil Biconsonantal perfect; contrast Niphal נָ (qamets)'),
        NHEntry('15', 'נָכוֹן',       'Gen 41:32', '"the thing is ___ by God"',                 'Niphal', 'Perfect',    '3ms', 'כּוּן · Biconsonantal',    'is established / firm',  'נָ prefix (qamets) = Niphal Biconsonantal perfect; context confirms passive sense'),
    ]

    _PART_C = [
        NHEntry('16', 'וַיַּעַל',     'Gen 22:2',  '"and he ___ him as a burnt offering"',      'Hiphil', 'Wayyiqtol',  '3ms', 'עָלָה · III-ה + I-gutt.', 'offered up (apocopated)', 'patach prefix (יַ) + composite shewa + apocopated = Hiphil; contrast Niphal וַיֵּ'),
        NHEntry('17', 'וַיִּגָּל',    'Num 24:4',  '"who sees the vision, ___ eyes"',           'Niphal', 'Wayyiqtol',  '3ms', 'גָּלָה · III-ה',           'were uncovered (apocopated)', 'וַיִּ + dagesh in ג (Niphal assimilation) + apocopated = Niphal'),
        NHEntry('18', 'הָסֵב',        '2 Sam 2:22', '"___ from following me"',                   'Hiphil', 'Imperative', '2ms', 'סָבַב · Geminate',         'turn aside!',            'הָ prefix (qamets) = Hiphil Biconsonantal/Geminate imperative; root R2=R3'),
        NHEntry('19', 'מַעֲמִידִים',  'Neh 4:7',   '"we who were ___ guard over them"',         'Hiphil', 'Participle', 'mp',  'עָמַד · I-guttural',       'stationing / standing guard', 'מַ + composite shewa under ע = Hiphil I-guttural participle; contrast Niphal נֶ'),
        NHEntry('20', 'הֵרָאֵה',      '1 Kgs 18:1', '"Go, ___ yourself to Ahab"',                'Niphal', 'Imperative', '2ms', 'רָאָה · III-ה',            'show yourself!',         'הֵ prefix (ר compensatory) + final ֵה retained = Niphal III-ה imperative'),
    ]

    def _build(self):
        self.add_instructions(
            'For each form: (1) identify the stem (Niphal or Hiphil); (2) parse — conjugation, PGN; '
            '(3) give the root and weak class; (4) translate in context. '
            'Answer key is on the last page.'
        )

        self.add_note(
            'Niphal markers: נִ prefix (perfect/participle); יִמָּ / וַיִּמָּ (imperfect/wayyiqtol — assimilation); '
            'נוֹ (I-י perfect/ptc); יִוָּ (I-י imperfect); נָ (Biconsonantal perfect/ptc).  '
            'Hiphil markers: הִ prefix (perfect); יַ (imperfect); הַ (imperative/inf.); מַ (participle) — '
            'modified for weak classes: הֶ (I-gutt.), הוֹ / יוֹ / מוֹ (I-י), הֵ / יָ / הָ / מֵ (Biconsonantal/Geminate).'
        )

        self.add_section_heading('Part A — Contrasting Niphal and Hiphil (same root)')
        self.add_note('Niphal = passive/reflexive. Hiphil = causative. Same root, opposite semantic direction.')
        self.add_nh_table(self._PART_A, show_answers=False)

        self.add_section_heading('Part B — Weak-Class Focus (I-י and Biconsonantal)')
        self.add_note(
            'I-י: Niphal perfect/ptc = נוֹ; imperfect = יִוָּ (dagesh in ו). '
            'Hiphil perfect = הוֹ; imperfect = יוֹ (no dagesh in ו). '
            'Biconsonantal: Niphal perfect/ptc = נָ (qamets); Hiphil perfect = הֵ (tsere).'
        )
        self.add_nh_table(self._PART_B, show_answers=False)

        self.add_section_heading('Part C — Mixed Review')
        self.add_nh_table(self._PART_C, show_answers=False)

        self.add_reflection([
            'Items 1–2 (שָׁמַע) and 3–4 (מָצָא): pick one pair and explain in one sentence '
            'what the Niphal adds and what the Hiphil adds to the basic Qal meaning.',
            'Items 9–11 are all from יָלַד (I-י). Both stems use a holem-vav cluster. '
            'What is the precise difference between Niphal perfect נוֹלַד and Hiphil wayyiqtol וַיּוֹלֶד?',
            'Items 16 and 17 are both apocopated III-ה wayyiqtol forms. '
            'What vowel under the prefix consonant is decisive in distinguishing Niphal from Hiphil?',
            'Items 18 (הָסֵב, Hiphil Geminate imperative) and 20 (הֵרָאֵה, Niphal III-ה imperative) '
            'both have a long prefix vowel rather than the expected strong הַ/הִ. '
            'Explain the phonological reason for the long vowel in each case.',
        ])

        self.add_answer_key_nh(self._PART_A + self._PART_B + self._PART_C)

    def add_answer_key_nh(self, entries: list['NHEntry']):
        self.add_section_heading('Answer Key')
        c = self._canvas
        w = self._usable_w()
        ratios = [0.04, 0.10, 0.10, 0.76]
        cw = [r * w for r in ratios]
        headers = ['#', 'Form', 'Stem', 'Answer']

        self._check_space(self.HEADER_H + len(entries) * self.ANSWER_H + 0.1*inch)
        y = self._y
        x0 = self.MARGIN_L

        c.setFillColor(C_HEADER_BG)
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.4)
        c.rect(x0, y - self.HEADER_H, sum(cw), self.HEADER_H, fill=1, stroke=1)
        cx = x0
        c.setFont('Helvetica-Bold', self.LABEL_SIZE)
        c.setFillColor(black)
        for hdr, col_w in zip(headers, cw):
            c.drawString(cx + 3, y - self.HEADER_H + 5, hdr)
            cx += col_w
        y -= self.HEADER_H

        for e in entries:
            self._check_space(self.ANSWER_H)
            c.setFillColor(C_ANSWER_BG)
            c.setStrokeColor(C_RULE)
            c.setLineWidth(0.4)
            c.rect(x0, y - self.ANSWER_H, sum(cw), self.ANSWER_H, fill=1, stroke=1)
            cx = x0
            c.setFont('Helvetica-Bold', self.LABEL_SIZE)
            c.setFillColor(C_ANSWER_FG)
            c.drawCentredString(cx + cw[0]/2, y - self.ANSWER_H + 6, e.num)
            cx += cw[0]
            c.setFont('ArialHebrew', self.LABEL_SIZE)
            c.drawRightString(cx + cw[1] - 3, y - self.ANSWER_H + 6, _heb(e.heb))
            cx += cw[1]
            c.setFont('Helvetica-Bold', self.LABEL_SIZE)
            c.drawString(cx + 3, y - self.ANSWER_H + 6, e.stem)
            cx += cw[2]
            c.setFont('Helvetica', self.LABEL_SIZE)
            answer = f'{e.conj} · {e.pgn} · {e.root_class} — "{e.translation}" — {e.note}'
            lines = simpleSplit(answer, 'Helvetica', self.LABEL_SIZE, cw[3] - 6)
            c.drawString(cx + 3, y - self.ANSWER_H + 6, lines[0] if lines else answer)
            y -= self.ANSWER_H

        self._y = y - 0.08 * inch


def build_ch27_nh_contrast_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch27', 'exercises',
                               'ch27-niphal-hiphil-contrast')
    path = os.path.join(out_dir, 'ch27-niphal-hiphil-contrast.pdf')
    ex = Ch27NHContrastExercise(
        title='Chapter 27 — Niphal–Hiphil Contrast Drill',
        subtitle='BBH Chapters 25 & 27 · Niphal and Hiphil Weak Verbs',
    )
    return ex.save(path)


class Ch27BGDrillExercise(ExercisePDF):
    """Biconsonantal / Geminate Disambiguation Drill — 24 items in Niphal and Hiphil."""

    _PART_A = [
        BGEntry('1',  'נָכוֹן',    'Gen 41:32',  '"the thing is ___ by God"',                    'Niphal', 'Perfect/Ptc', '3ms/ms', 'Biconsonantal', 'כּוּן',  'is established / firm',       'נָ prefix (qamets); medial ו vowel letter = Biconsonantal'),
        BGEntry('2',  'נָסַב',     '1 Kgs 7:24', '"the gourds ___ it, ten to a cubit"',          'Niphal', 'Perfect',     '3ms',    'Geminate',      'סָבַב',  'encircled / went around',     'נָ prefix (qamets); R2=R3=ב = Geminate; no medial vowel letter'),
        BGEntry('3',  'יִכּוֹן',   'Psa 93:2',   '"your throne ___ from of old"',                'Niphal', 'Imperfect',   '3ms',    'Biconsonantal', 'כּוּן',  'is established',              'יִ + dagesh in כּ + holem-vav = Niphal Biconsonantal imperfect'),
        BGEntry('4',  'יִסֹּב',    'Num 21:4',   '"they traveled ___ Mount Edom"',               'Niphal', 'Imperfect',   '3ms',    'Geminate',      'סָבַב',  'went around',                 'יִ + dagesh in סּ (R2=R3 doubled) + holem = Niphal Geminate imperfect'),
        BGEntry('5',  'הֵכּוֹן',   'Psa 57:8',   '"my heart is ___, O God"',                     'Niphal', 'Perfect',     '3ms',    'Biconsonantal', 'כּוּן',  'is ready / prepared',         'הֵ + dagesh + holem-vav = Niphal Biconsonantal; context confirms passive sense'),
        BGEntry('6',  'הֵסֹּב',    'Num 34:4',   '"your border ___ from the south"',             'Niphal', 'Perfect',     '3ms',    'Geminate',      'סָבַב',  'turned / went around',        'הֵ + dagesh in סּ (R2=R3) + holem = Niphal Geminate perfect'),
        BGEntry('7',  'נָשׁוּב',   'Lam 3:40',   '"let us examine and ___ to the LORD"',         'Niphal', 'Cohortative', '1cp',    'Biconsonantal', 'שׁוּב',  'let us return',               'נָ prefix + medial ו = Niphal Biconsonantal; cohortative force from context'),
        BGEntry('8',  'נָתֹם',     '1 Sam 3:12', '"when I ___ what I have spoken"',              'Niphal', 'Inf. Const.', '—',      'Geminate',      'תָּמַם', 'to be completed / finished',  'נָ prefix + holem = Niphal Geminate inf. construct; root R2=R3=מ'),
    ]

    _PART_B = [
        BGEntry('9',  'הֵקִים',    'Gen 6:18',   '"I will ___ my covenant with you"',            'Hiphil', 'Perfect',     '3ms',    'Biconsonantal', 'קוּם',  'established / raised up',     'הֵ prefix (tsere) = Hiphil; medial ו vowel letter = Biconsonantal'),
        BGEntry('10', 'הֵסֵב',     '2 Sam 2:22', '"___ from following me"',                      'Hiphil', 'Perfect',     '3ms',    'Geminate',      'סָבַב', 'turned aside',                'הֵ prefix (tsere) = Hiphil; no medial vowel letter, R2=R3=ב = Geminate'),
        BGEntry('11', 'יָקִים',    'Deut 18:15', '"the LORD will ___ a prophet"',                'Hiphil', 'Imperfect',   '3ms',    'Biconsonantal', 'קוּם',  'will raise up',               'יָ prefix (qamets) = Hiphil Biconsonantal imperfect; medial ו retained'),
        BGEntry('12', 'יָסֵב',     'Eccl 1:6',   '"the wind ___ to the south"',                  'Hiphil', 'Imperfect',   '3ms',    'Geminate',      'סָבַב', 'causes to go around / turns', 'יָ prefix (qamets) = Hiphil; no medial vowel letter = Geminate'),
        BGEntry('13', 'הָקֵם',     'Deut 27:26', '"\'___ the words of this law\'"',              'Hiphil', 'Imperative',  '2ms',    'Biconsonantal', 'קוּם',  'raise up! / confirm!',        'הָ prefix (qamets) = Hiphil imperative; Biconsonantal: no R2=R3 doubling'),
        BGEntry('14', 'הָסֵב',     '2 Sam 2:22', '"___ from following me"',                      'Hiphil', 'Imperative',  '2ms',    'Geminate',      'סָבַב', 'turn aside!',                 'הָ prefix (qamets) = Hiphil imperative; same vowels as Biconsonantal; root R2=R3=ב'),
        BGEntry('15', 'מֵקִים',    '1 Sam 2:8',  '"He ___ the poor from the dust"',              'Hiphil', 'Participle',  'ms',     'Biconsonantal', 'קוּם',  'one who raises up',           'מֵ prefix (tsere) = Hiphil participle; medial ו retained = Biconsonantal'),
        BGEntry('16', 'מֵסֵב',     'Ezek 41:7',  '"the structure ___ upward"',                   'Hiphil', 'Participle',  'ms',     'Geminate',      'סָבַב', 'going around / surrounding',  'מֵ prefix (tsere) = Hiphil participle; no medial vowel letter = Geminate'),
    ]

    _PART_C = [
        BGEntry('17', 'נָמֹוג',    'Isa 14:31',  '"all Philistia ___"',                          'Niphal', 'Perfect',     '3ms',    'Biconsonantal', 'מוּג',  'melted / dissolved',          'נָ prefix + medial ו = Niphal Biconsonantal; root מוּג = to melt'),
        BGEntry('18', 'הֵמַס',     'Josh 2:11',  '"the LORD ___ our hearts"',                    'Hiphil', 'Perfect',     '3ms',    'Geminate',      'מסס',   'caused to melt',              'הֵ prefix (tsere) = Hiphil; R2=R3=ס = Geminate; patach under contracted stem'),
        BGEntry('19', 'יָרֻם',     'Isa 52:13',  '"my servant shall be high and ___ up"',        'Niphal', 'Imperfect',   '3ms',    'Biconsonantal', 'רוּם',  'will be exalted / lifted up', 'יָ prefix + qibbutz under R2 (passive) = Niphal Biconsonantal; contrast Hiphil יָרִים'),
        BGEntry('20', 'יָרֹם',     'Psa 99:2',   '"great is the LORD, ___ above all peoples"',   'Niphal', 'Imperfect',   '3ms',    'Biconsonantal', 'רוּם',  'is exalted / high',           'יָ prefix + holem under R2 = Niphal Biconsonantal; compare Hiphil יָרִים (chiriq)'),
        BGEntry('21', 'הֵרִים',    'Gen 14:22',  '"I have ___ my hand to the LORD"',             'Hiphil', 'Perfect',     '3ms',    'Biconsonantal', 'רוּם',  'lifted up / swore an oath',   'הֵ prefix (tsere) + chiriq-yod = Hiphil Biconsonantal perfect; causative sense'),
        BGEntry('22', 'הוּרַם',    'Lev 4:10',   '"just as it is ___ from the peace offerings"', 'Hophal', 'Perfect',     '3ms',    'Biconsonantal', 'רוּם',  'was lifted off / removed',    'הוּ prefix (holem-vav) = Hophal (passive of Hiphil), not Niphal or Hiphil'),
        BGEntry('23', 'יָשׁוּב',   'Hos 14:8',   '"they ___ in the shade"',                      'Qal',    'Imperfect',   '3ms',    'Biconsonantal', 'שׁוּב', 'will dwell / return',         'Qal Biconsonantal — no Niphal נ or Hiphil הֵ/מֵ marker; medial ו retained'),
        BGEntry('24', 'יָשֹׁב',    'Lam 1:11',   '"all her people ___ to find bread"',           'Qal',    'Imperfect',   '3ms',    'Biconsonantal', 'שׁוּב', 'returned / went around',      'Qal Biconsonantal; holem vowel grade vs. shureq in יָשׁוּב — both Qal, not Niphal/Hiphil'),
    ]

    def _build(self):
        self.add_instructions(
            'For each form: (1) identify the stem (Niphal or Hiphil); (2) parse — conjugation, PGN; '
            '(3) identify the weak class (Biconsonantal or Geminate); (4) give the root and translate. '
            'Biconsonantal and Geminate forms are vocally identical — root knowledge is required. '
            'Answer key is on the last page.'
        )

        self.add_note(
            'Biconsonantal (II-י/ו): medial vowel letter ו or י retained in stem (e.g. קוּם, שׁוּב, כּוּן). '
            'Geminate (R2=R3): same consonant at R2 and R3; no medial vowel letter (e.g. סָבַב, תָּמַם). '
            'Both classes share: Niphal perfect נָ (qamets); Hiphil perfect הֵ (tsere); '
            'Hiphil imperfect יָ (qamets); Hiphil imperative הָ (qamets); Hiphil participle מֵ (tsere).'
        )

        self.add_section_heading('Part A — Niphal: Biconsonantal vs. Geminate')
        self.add_note(
            'All forms are Niphal. Identify whether each is Biconsonantal (medial ו/י) or Geminate (R2=R3). '
            'The prefix vowel pattern (נָ in perfect; יִ in imperfect) is identical for both classes.'
        )
        self.add_bg_table(self._PART_A, show_answers=False)

        self.add_section_heading('Part B — Hiphil: Biconsonantal vs. Geminate')
        self.add_note(
            'All forms are Hiphil. Hiphil prefix patterns: הֵ (perfect) · יָ (imperfect) · הָ (imperative) · מֵ (participle). '
            'These are identical for Biconsonantal and Geminate — root knowledge is the only distinguisher.'
        )
        self.add_bg_table(self._PART_B, show_answers=False)

        self.add_section_heading('Part C — Mixed: Stem and Class Both Unknown')
        self.add_note(
            'Identify both the stem (Niphal/Hiphil/Qal/Hophal) and the class. '
            'Part C includes Qal and Hophal forms as distractors — not every Biconsonantal form is Niphal or Hiphil.'
        )
        self.add_bg_table(self._PART_C, show_answers=False)

        self.add_reflection([
            'Items 1 (נָכוֹן) and 2 (נָסַב) have the same נָ prefix. What is the only reliable way '
            'to identify נָכוֹן as Biconsonantal (root כּוּן) and נָסַב as Geminate (root סָבַב)?',
            'Items 9 (הֵקִים) and 10 (הֵסֵב) both have הֵ prefix (tsere). One retains a medial vowel '
            'letter; the other shows a contracted stem. Describe precisely what the medial position '
            'of each form looks like and how that reflects the root structure.',
            'Items 11 (יָקִים) and 12 (יָסֵב) are both Hiphil imperfect 3ms. You encounter an unknown '
            'form יָדֵל. What question must you ask to determine if it is Biconsonantal or Geminate?',
            'Items 19 (יָרֻם) and 21 (הֵרִים) come from the same root (רוּם) but differ in stem. '
            'What vowel under R2 distinguishes the Niphal imperfect from the Hiphil perfect?',
            'Item 22 (הוּרַם) was classified as Hophal. How does the Hophal Biconsonantal prefix (הוּ) '
            'differ from Niphal (נָ) and Hiphil (הֵ), and what does it tell you about the semantics?',
        ])

        self.add_answer_key_bg(self._PART_A + self._PART_B + self._PART_C)

    def add_answer_key_bg(self, entries: list['BGEntry']):
        self.add_section_heading('Answer Key')
        c = self._canvas
        w = self._usable_w()
        ratios = [0.04, 0.10, 0.10, 0.76]
        cw = [r * w for r in ratios]
        headers = ['#', 'Form', 'Stem', 'Answer']

        self._check_space(self.HEADER_H + len(entries) * self.ANSWER_H + 0.1*inch)
        y = self._y
        x0 = self.MARGIN_L

        c.setFillColor(C_HEADER_BG)
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.4)
        c.rect(x0, y - self.HEADER_H, sum(cw), self.HEADER_H, fill=1, stroke=1)
        cx = x0
        c.setFont('Helvetica-Bold', self.LABEL_SIZE)
        c.setFillColor(black)
        for hdr, col_w in zip(headers, cw):
            c.drawString(cx + 3, y - self.HEADER_H + 5, hdr)
            cx += col_w
        y -= self.HEADER_H

        for e in entries:
            self._check_space(self.ANSWER_H)
            c.setFillColor(C_ANSWER_BG)
            c.setStrokeColor(C_RULE)
            c.setLineWidth(0.4)
            c.rect(x0, y - self.ANSWER_H, sum(cw), self.ANSWER_H, fill=1, stroke=1)
            cx = x0
            c.setFont('Helvetica-Bold', self.LABEL_SIZE)
            c.setFillColor(C_ANSWER_FG)
            c.drawCentredString(cx + cw[0]/2, y - self.ANSWER_H + 6, e.num)
            cx += cw[0]
            c.setFont('ArialHebrew', self.LABEL_SIZE)
            c.drawRightString(cx + cw[1] - 3, y - self.ANSWER_H + 6, _heb(e.heb))
            cx += cw[1]
            c.setFont('Helvetica-Bold', self.LABEL_SIZE)
            c.drawString(cx + 3, y - self.ANSWER_H + 6, e.stem)
            cx += cw[2]
            c.setFont('Helvetica', self.LABEL_SIZE)
            answer = f'{e.conj} · {e.pgn} · {e.bg_class} · {e.root} — "{e.translation}" — {e.note}'
            lines = simpleSplit(answer, 'Helvetica', self.LABEL_SIZE, cw[3] - 6)
            c.drawString(cx + 3, y - self.ANSWER_H + 6, lines[0] if lines else answer)
            y -= self.ANSWER_H

        self._y = y - 0.08 * inch


def build_ch27_bg_drill_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch27', 'exercises',
                               'ch27-biconsig-drill')
    path = os.path.join(out_dir, 'ch27-biconsig-drill.pdf')
    ex = Ch27BGDrillExercise(
        title='Chapter 27 — Biconsonantal / Geminate Disambiguation Drill',
        subtitle='BBH Chapters 25 & 27 · Niphal and Hiphil Weak Verbs',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Chapter 30 — "Spot the Piel" Passage Exercise (Piel Strong)
# ---------------------------------------------------------------------------
class Ch30PielExercise(PassageExercise):
    _instructions = (
        'Each numbered verb belongs to one of the stems you have already studied '
        '(Qal, Niphal, Hiphil, Hophal, or Piel). '
        'For each one, fill in: Piel? (Yes/No), Conjugation, PGN, Root, and Stem/Function. '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool):

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Genesis 1:22, 28')

        self.add_passage(PassageBlock('1:22',
            'וַיְבָ֧רֶךְ אֹתָ֛ם אֱלֹהִ֖ים לֵאמֹ֑ר פְּר֥וּ וּרְב֛וּ',
            '"And God blessed them, saying, \'Be fruitful and multiply…\'"'))
        self.add_verb_table([
            VerbEntry('1', 'וַיְבָרֶךְ', 'Wayyiqtol', '3ms', 'בָּרַךְ', 'Intensive — God\'s blessing; Piel Wayyiqtol וַיְ prefix'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('1:28',
            'וַיְבָ֣רֶךְ אֹתָ֖ם אֱלֹהִ֑ים',
            '"And God blessed them."'))
        self.add_verb_table([
            VerbEntry('2', 'וַיְבָרֶךְ', 'Wayyiqtol', '3ms', 'בָּרַךְ', 'Intensive — same form; R2=ר rejects dagesh; Piel marked by vowel pattern'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Exodus 19:10–14')

        self.add_passage(PassageBlock('19:10',
            'וְקִדַּשְׁתָּ֥ אֹתָ֛ם הַיּ֥וֹם וּמָחָ֑ר וְכִבְּס֖וּ שִׂמְלֹתָֽם',
            '"…consecrate them today and tomorrow, and let them wash their garments."'))
        self.add_verb_table([
            VerbEntry('3', 'וְקִדַּשְׁתָּ', 'Weqatal', '2ms', 'קָדַשׁ', 'Factitive — cause to become holy; Weqatal = consequential command'),
            VerbEntry('4', 'וְכִבְּסוּ', 'Weqatal', '3cp', 'כָּבַס', 'Intensive — wash/launder; roots almost exclusively Piel OT-wide'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('19:14',
            'וַיְקַדֵּ֖שׁ אֶת־הָעָ֑ם וַיְכַבְּס֖וּ שִׂמְלֹתָֽם',
            '"…and he consecrated the people, and they washed their garments."'))
        self.add_verb_table([
            VerbEntry('5', 'וַיְקַדֵּשׁ', 'Wayyiqtol', '3ms', 'קָדַשׁ', 'Factitive — narrative fulfillment of command (v.10); same root'),
            VerbEntry('6', 'וַיְכַבְּסוּ', 'Wayyiqtol', '3mp', 'כָּבַס', 'Intensive — Wayyiqtol 3mp; contrast with Weqatal 3cp above'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('19:25',
            'וַיְדַבֵּ֥ר מֹשֶׁ֖ה אֶל־הָעָ֑ם',
            '"And Moses spoke to the people."'))
        self.add_verb_table([
            VerbEntry('7', 'וַיְדַבֵּר', 'Wayyiqtol', '3ms', 'דָּבַר', 'Denominative — from דָּבָר (word); 1,090x in OT; Piel is the standard form'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B insert — Exo 19:13 (Hophal distractor) ─────────────────
        self.add_passage(PassageBlock('19:13',
            'סָקוֹל יִסָּקֵל אוֹ יָרֹה יִיָּרֶה אִם בְּהֵמָה אִם אִישׁ לֹא יִחְיֶה',
            '"Whether beast or man, he shall not live — he shall be stoned or shot."'))
        self.add_verb_table([
            VerbEntry('8', 'יִסָּקֵל', 'Niphal Impf.', '3ms', 'סָקַל', 'NOT Piel — Niphal passive: "shall be stoned"; נִ-prefix contracts to יִ + dagesh; passive of Qal'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Numbers 22:6–8, 17 (with Qal/Hophal distractors)')

        self.add_passage(PassageBlock('22:6',
            'לְכָה נָּא אָרָה לִּי אֶת הָעָם הַזֶּה כִּי יָדַעְתִּי אֵת אֲשֶׁר תְּבָרֵךְ מְבֹרָךְ [not numbered — Ch32] וַאֲשֶׁר תָּאֹר יוּאָר',
            '"Come now, curse this people for me… he whom you bless is blessed [Ch32 Pual — not numbered], and he whom you curse is cursed."'))
        self.add_verb_table([
            VerbEntry('9',  'אָרָה',     'Qal Jussive',  '1cs', 'אָרַר', 'NOT Piel — Qal jussive (curse); no dagesh in R2'),
            VerbEntry('10', 'תְּבָרֵךְ', 'Imperfect',    '2ms', 'בָּרַךְ', 'Intensive (Piel) — תְּ prefix + patach + tsere; R2=ר rejects dagesh'),
            VerbEntry('11', 'יוּאָר',   'Hophal Impf.', '3ms', 'אָרַר', 'NOT Piel — Hophal (shall be cursed); יוּ prefix = u-class vowel under prefix = Hophal marker'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('22:8',
            'יְדַבֵּר יְהוָה אֵלָי וְדִבַּרְתִּי אֲלֵיכֶם',
            '"The LORD will speak to me, and I will speak to you."'))
        self.add_verb_table([
            VerbEntry('12', 'יְדַבֵּר',    'Imperfect', '3ms', 'דָּבַר', 'Denominative — יְ prefix + dagesh in בּ; standard Piel Imperfect'),
            VerbEntry('13', 'וְדִבַּרְתִּי', 'Weqatal',   '1cs', 'דָּבַר', 'Denominative — Weqatal; Hireq under R1 + dagesh + 1cs suffix תִּי'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('22:17',
            'כִּי כַבֵּד אֲכַבֶּדְךָ מְאֹד וּלְכָה נָּא קָבָה לִי אֶת הָעָם הַזֶּה',
            '"For I will surely honor you greatly; come now, curse this people for me."'))
        self.add_verb_table([
            VerbEntry('14', 'כַּבֵּד',    'Inf. Absolute', '—',  'כָּבֵד', 'Intensive (Piel Inf.Abs.) — cognate construction כַּבֵּד אֲכַבֶּד'),
            VerbEntry('15', 'אֲכַבֶּדְךָ', 'Imperfect',    '1cs', 'כָּבֵד', 'Factitive — אֲ prefix + dagesh in בּ; Piel of "heavy" = to honor'),
            VerbEntry('16', 'קָבָה',      'Qal Impv.',    '2ms', 'קָבַב',  'NOT Piel — Qal imperative (curse geminate root); no dagesh in R2'),
        ], show_answers=show_answers)



def build_ch30_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch30', 'exercises',
                               'ch30-passage-exercise')
    path = os.path.join(out_dir, 'ch30-passage-exercise.pdf')
    ex = Ch30PielExercise(
        title='Chapter 30 — "Spot the Piel" Passage Exercise',
        subtitle='Gen 1  ·  Exo 19  ·  Num 22',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Chapter 28 — "Spot the Hophal" Passage Exercise (correct: Hophal Strong)
# ---------------------------------------------------------------------------
class Ch28HophalExercise(PassageExercise):
    _instructions = (
        'Each numbered verb belongs to one of the stems you have already studied '
        '(Qal, Niphal, Hiphil, or Hophal). '
        'For each one, fill in: Hophal? (Yes/No), Conjugation, PGN, Root, and Stem/Function. '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool):

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Genesis 22:20')

        self.add_passage(PassageBlock('22:20',
            'וַיְהִ֗י אַֽחֲרֵי֙ הַדְּבָרִ֣ים הָאֵ֔לֶּה וַיֻּגַּ֥ד לְאַבְרָהָ֖ם לֵאמֹֽר',
            '"Now after these things it was told to Abraham, saying…"'))
        self.add_verb_table([
            VerbEntry('1', 'וַיֻּגַּד', 'Wayyiqtol', '3ms', 'נָגַד', 'Hiphil הִגִּיד = to tell/declare → Hophal = it was reported'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Exodus 5:14–16 (with Niphal distractor)')

        self.add_passage(PassageBlock('5:14',
            'וַיֻּכּ֗וּ שֹׁטְרֵי֙ בְּנֵ֣י יִשְׂרָאֵ֔ל אֲשֶׁר־שָׂ֣מוּ עֲלֵהֶ֔ם נֹגְשֵׂ֥י פַרְעֹ֖ה',
            '"And the overseers of the people of Israel were beaten…"'))
        self.add_verb_table([
            VerbEntry('2', 'וַיֻּכּוּ', 'Wayyiqtol', '3mp', 'נָכָה', 'Hiphil הִכָּה = to strike/kill → Hophal = were beaten'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('5:16',
            'תֶּ֗בֶן אֵ֤ין נִתָּן֙ לַעֲבָדֶ֔יךָ וְהִנֵּ֧ה עֲבָדֶ֛יךָ מֻכִּ֖ים',
            '"No straw is given to your servants, and behold, your servants are being beaten…"'))
        self.add_verb_table([
            VerbEntry('3', 'נִתָּן', 'Niphal Ptc.', 'ms', 'נָתַן', 'NOT Hophal — Niphal passive of Qal נָתַן (given); נ prefix'),
            VerbEntry('4', 'מֻכִּים', 'Participle', 'mp', 'נָכָה', 'Hophal — מֻ prefix (Qibbuts) = u-class vowel; passive of Hiphil הִכָּה'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Numbers 35:16–18, 30–31 (Qal distractors)')

        self.add_passage(PassageBlock('35:16',
            'וְאִם בִּכְלִי בַרְזֶל הִכָּהוּ וַיָּמֹת מוֹת־יוּמַת הָרֹצֵֽחַ',
            '"If he struck him with iron and he died — the murderer shall surely be put to death."'))
        self.add_verb_table([
            VerbEntry('5', 'יוּמַת', 'Imperfect', '3ms', 'מוּת', 'Hophal — יוּ prefix (Shureq); Hiphil הֵמִית = to put to death'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('35:17',
            'וְאִם בְּאֶבֶן יָד אֲשֶׁר־יָמוּת בָּהּ הִכָּהוּ וַיָּמֹת מוֹת־יוּמַת הָרֹצֵֽחַ',
            '"If with a stone that could kill he struck him and he died — the murderer shall be put to death."'))
        self.add_verb_table([
            VerbEntry('6', 'יָמוּת', 'Qal Impf.', '3ms', 'מוּת', 'NOT Hophal — Qal intransitive "to die"; יָ prefix (Patach) ≠ Hophal'),
            VerbEntry('7', 'יוּמַת', 'Imperfect', '3ms', 'מוּת', 'Hophal — יוּ prefix (Shureq); same formula as verb 5'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('35:30–31',
            'עַל־פִּי עֵדִים יֵרָצֵחַ הָרֹצֵחַ … כִּי־מוֹת יוּמָת',
            '"On the testimony of witnesses the murderer shall be put to death… for he shall surely be put to death."'))
        self.add_verb_table([
            VerbEntry('8', 'יֵרָצֵחַ', 'Niphal Impf.', '3ms', 'רָצַח', 'NOT Hophal — Niphal (passive of Qal murder); יֵ prefix, no u-vowel'),
            VerbEntry('9', 'יוּמַת', 'Imperfect', '3ms', 'מוּת', 'Hophal — יוּ prefix (Shureq); death penalty formula'),
        ], show_answers=show_answers)


def build_ch28_hophal_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch28', 'exercises',
                               'ch28-passage-exercise')
    path = os.path.join(out_dir, 'ch28-passage-exercise.pdf')
    ex = Ch28HophalExercise(
        title='Chapter 28 — "Spot the Hophal" Passage Exercise',
        subtitle='Genesis 22  ·  Exodus 5  ·  Numbers 35',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Chapter 34 — "Spot the Hithpael" Passage Exercise (Strong Verbs)
# ---------------------------------------------------------------------------
class Ch34HithpaelExercise(PassageExercise):
    _instructions = (
        'Each numbered verb belongs to one of the stems you have already studied '
        '(Qal, Niphal, Hiphil, Hophal, Piel, Pual, or Hithpael). '
        'Focus: strong roots in the Hithpael stem. '
        'For each one, fill in: Hithpael? (Yes/No), Conjugation, PGN, Root, and Stem/Function. '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool):

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — 1 Kings 8:28–30 · Genesis 20:7')

        self.add_passage(PassageBlock('8:28',
            'וְאֶל־הַתְּפִלָּה אֲשֶׁר עַבְדְּךָ מִתְפַּלֵּל לְפָנֶיךָ הַיּוֹם',
            '"…and to the prayer that your servant is praying before you today."'))
        self.add_verb_table([
            VerbEntry('1', 'מִתְפַּלֵּל', 'Participle', 'ms', 'פלל',
                      'Denominative — "praying"; מִתְ- prefix marks Hithpael participle; root פלל has no Qal in OT'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('8:30',
            'אֲשֶׁר יִתְפַּלְּלוּ אֶל הַמָּקוֹם הַזֶּה',
            '"…when they pray toward this place."'))
        self.add_verb_table([
            VerbEntry('2', 'יִתְפַּלְּלוּ', 'Imperfect', '3mp', 'פלל',
                      'Denominative — "they pray"; יִתְ- prefix + dagesh forte in doubled ל ל (geminate root)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('20:7',
            'כִּי נָבִיא הוּא וְיִתְפַּלֵּל בַּעַדְךָ',
            '"…for he is a prophet, and he will pray for you."'))
        self.add_verb_table([
            VerbEntry('3', 'יִתְפַּלֵּל', 'Imperfect', '3ms', 'פלל',
                      'Denominative — "he will pray"; יִתְ- prefix + patach under R1 + dagesh forte in ל ל'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('20:7',
            'הִתְפַּלֵּל אֶל יְהוָה',
            '"Pray to the LORD."'))
        self.add_verb_table([
            VerbEntry('4', 'הִתְפַּלֵּל', 'Imperative', '2ms', 'פלל',
                      'Denominative — "Pray!"; הִתְ- prefix + patach under R1 + tsere + ל ל; same form as perfect 3ms in isolation'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 29:36',
            'וְטִהֲרוֹ לְכַפֵּר עָלָיו',
            '"…and purify it to make atonement for it." [Piel distractor — no הִתְ prefix]'))
        self.add_verb_table([
            VerbEntry('5', 'וְטִהֲרוֹ', 'Weqatal', '3ms', 'טהר',
                      'NOT Hithpael — Piel: Factitive "shall purify it"; Hireq under R1 + guttural ה (rejects dagesh); no הִתְ prefix'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Joshua 3:5 · Exodus 19:22')

        self.add_passage(PassageBlock('Jos 3:5',
            'הִתְקַדְּשׁוּ כִּי מָחָר יַעֲשֶׂה יְהוָה בְּקִרְבְּכֶם נִפְלָאוֹת',
            '"Consecrate yourselves, for tomorrow the LORD will do wonders among you."'))
        self.add_verb_table([
            VerbEntry('6', 'הִתְקַדְּשׁוּ', 'Imperative', '2mp', 'קדש',
                      'Reflexive — "consecrate yourselves!"; הִתְ- prefix + patach + dagesh forte in R2 (דּ) + 2mp suffix וּ'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 19:22',
            'וְגַם הַכֹּהֲנִים הַנִּגָּשִׁים אֶל יְהוָה יִתְקַדָּשׁוּ פֶּן יִפְרֹץ בָּהֶם',
            '"And also let the priests who come near to the LORD consecrate themselves, lest the LORD break out against them."'))
        self.add_verb_table([
            VerbEntry('7', 'יִתְקַדָּשׁוּ', 'Imperfect', '3mp', 'קדש',
                      'Reflexive — "let them consecrate themselves"; יִתְ- prefix + patach + lengthened R2 vowel (qamets) + 3mp suffix וּ'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Lev 8:15',
            'קֻדַּשׁ הַמִּזְבֵּחַ',
            '"The altar was consecrated." [Pual distractor — u-class vowel under R1]'))
        self.add_verb_table([
            VerbEntry('8', 'קֻדַּשׁ', 'Perfect', '3ms', 'קדש',
                      'NOT Hithpael — Pual Passive: "was consecrated"; Qibbuts (u-class) under R1 (קֻ) = Pual marker; no הִתְ prefix'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Genesis 22:17–18 · 2 Samuel 10:12')

        self.add_passage(PassageBlock('Gen 22:18',
            'וְהִתְבָּרֲכוּ בְזַרְעֲךָ כֹּל גּוֹיֵי הָאָרֶץ',
            '"…and in your offspring all the nations of the earth shall bless themselves."'))
        self.add_verb_table([
            VerbEntry('9', 'וְהִתְבָּרֲכוּ', 'Weqatal', '3cp', 'ברך',
                      'Reflexive/Estimative — "shall bless themselves"; הִתְ- + R2=ר rejects dagesh (compensatory lengthening); 3cp suffix וּ'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('2 Sam 10:12',
            'חֲזַק וְנִתְחַזְּקָה בְּעַד עַמֵּנוּ',
            '"Be strong, and let us be courageous for our people."'))
        self.add_verb_table([
            VerbEntry('10', 'וְנִתְחַזְּקָה', 'Cohortative', '1cp', 'חזק',
                      'Reflexive — "let us strengthen ourselves"; נִתְ- (cohortative Hithpael 1cp) + dagesh forte in R2 (זּ) + ה cohortative'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Prov 17:15',
            'הִצְדִּיק אֶת הָרָשָׁע',
            '"He declared the wicked righteous." [Hiphil distractor — הִ- with no תְ]'))
        self.add_verb_table([
            VerbEntry('11', 'הִצְדִּיק', 'Perfect', '3ms', 'צדק',
                      'NOT Hithpael — Hiphil Declarative: "declared righteous"; הִ- prefix (no תְ) + Hireq-Yod under R2 = Hiphil pattern'),
        ], show_answers=show_answers)


def build_ch34_hithpael_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch34', 'exercises',
                               'ch34-passage-exercise')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'ch34-passage-exercise.pdf')
    ex = Ch34HithpaelExercise(
        title='Chapter 34 — "Spot the Hithpael" Passage Exercise',
        subtitle='(Strong Verbs)  ·  1 Kgs 8  ·  Gen 20  ·  Jos 3  ·  Exo 19  ·  Gen 22  ·  2 Sam 10',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Chapter 35 — "Spot the Hithpael" Passage Exercise (Weak Verbs)
# ---------------------------------------------------------------------------
class Ch35HithpaelWeakExercise(PassageExercise):
    _instructions = (
        'Each numbered verb belongs to one of the stems you have already studied '
        '(Qal, Niphal, Hiphil, Hophal, Piel, Pual, or Hithpael). '
        'Focus: weak roots in the Hithpael stem — watch for metathesis (I-צ/ז/שׁ) and III-ה forms. '
        'For each one, fill in: Hithpael? (Yes/No), Conjugation, PGN, Root, and Stem/Function. '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool):

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Gen 22:5 · Gen 18:2 · Exo 20:5 · Psa 95:6')

        self.add_passage(PassageBlock('Gen 24:26',
            'וַיִּשְׁתַּחוּ לַיהוָה',
            '"And he bowed down before the LORD."'))
        self.add_verb_table([
            VerbEntry('1', 'וַיִּשְׁתַּחוּ', 'Wayyiqtol', '3ms', 'שחה',
                      'Reflexive — "and he bowed down"; I-שׁ metathesis: הִתְ+שׁ → הִשְׁתַּ; III-ה short form (וּ ending in Wayyiqtol 3ms)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 22:5',
            'וְנִשְׁתַּחֲוֶה וְנָשׁוּבָה אֲלֵיכֶם',
            '"…and we will worship and we will come back to you."'))
        self.add_verb_table([
            VerbEntry('2', 'וְנִשְׁתַּחֲוֶה', 'Cohortative', '1cp', 'שחה',
                      'Reflexive — "let us worship"; I-שׁ metathesis: הִתְ+שׁ → הִשְׁתַּ; cohortative prefix נ; III-ה ending ֶה'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 18:2',
            'וַיִּשְׁתַּחוּ אָרְצָה',
            '"And he bowed down to the ground."'))
        self.add_verb_table([
            VerbEntry('3', 'וַיִּשְׁתַּחוּ', 'Wayyiqtol', '3ms', 'שחה',
                      'Reflexive — "and he bowed down"; Wayyiqtol: וַיִּ + שְׁתַּחוּ; I-שׁ metathesis; III-ה short form (וּ ending in Wayyiqtol 3ms)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 20:5',
            'לֹא תִשְׁתַּחְוֶה לָהֶם',
            '"You shall not bow down to them."'))
        self.add_verb_table([
            VerbEntry('4', 'תִשְׁתַּחְוֶה', 'Imperfect', '2ms', 'שחה',
                      'Reflexive — "you shall not bow down"; תִ- (2ms prefix) + שְׁתַּחְוֶה; I-שׁ metathesis; III-ה imperfect ending ֶה'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Psa 95:6',
            'בֹּאוּ נִשְׁתַּחֲוֶה וְנִכְרָעָה נִבְרְכָה לִפְנֵי יְהוָה עֹשֵׂנוּ',
            '"Come, let us bow down and kneel; let us kneel before the LORD our maker." [Qal distractor — נִבְרְכָה]'))
        self.add_verb_table([
            VerbEntry('5', 'נִבְרְכָה', 'Cohortative', '1cp', 'ברך',
                      'NOT Hithpael — Qal: "let us kneel/bless"; נ = 1cp cohortative prefix (not הִתְ); no dagesh forte in R2'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Genesis 35:7 · 1 Samuel 10:6, 11')

        self.add_passage(PassageBlock('Gen 35:7',
            'כִּי שָׁם נִגְלוּ אֵלָיו הָאֱלֹהִים',
            '"…because there God had revealed himself to him." [Niphal distractor]'))
        self.add_verb_table([
            VerbEntry('6', 'נִגְלוּ', 'Perfect', '3cp', 'גלה',
                      'NOT Hithpael — Niphal: "revealed themselves / were revealed"; נִ- prefix = Niphal; III-ה Niphal perfect 3cp (ה drops before וּ)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('1 Sam 10:6',
            'וְהִתְנַבִּיתָ עִמָּם וְנֶהְפַּכְתָּ לְאִישׁ אַחֵר',
            '"…and you will prophesy with them and be turned into another man."'))
        self.add_verb_table([
            VerbEntry('7', 'וְהִתְנַבִּיתָ', 'Weqatal', '2ms', 'נבא',
                      'Denominative/Iterative — "you will prophesy"; I-נ (no assimilation in Hithpael); הִתְ- + נַ + בִּי + 2ms suffix תָ; III-א'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('1 Sam 10:11',
            'וַיִּתְנַבְּאוּ עַד בּוֹא הַמִּנְחָה',
            '"And they prophesied until the offering of the evening sacrifice."'))
        self.add_verb_table([
            VerbEntry('8', 'וַיִּתְנַבְּאוּ', 'Wayyiqtol', '3mp', 'נבא',
                      'Denominative/Iterative — "and they prophesied"; יִתְ- prefix; I-נ (no assimilation); III-א with 3mp suffix אוּ'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Genesis 44:16 · 2 Kings 8:29')

        self.add_passage(PassageBlock('Gen 44:16',
            'מַה נֹּאמַר לַאדֹנִי מַה נְּדַבֵּר וּמַה נִּצְטַדָּק',
            '"What shall we say? What shall we speak? How can we justify ourselves?"'))
        self.add_verb_table([
            VerbEntry('9', 'נִצְטַדָּק', 'Imperfect', '1cp', 'צדק',
                      'Reflexive/Estimative — "how can we justify ourselves?"; I-צ metathesis: הִתְצ → הִצְטַ (ת voices to ט); 1cp prefix נ'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('2 Kgs 8:29',
            'וַיָּשָׁב יוֹרָם הַמֶּלֶךְ לְהִתְרַפֵּא בְיִזְרְעֶאל',
            '"And King Joram returned to be healed in Jezreel."'))
        self.add_verb_table([
            VerbEntry('10', 'לְהִתְרַפֵּא', 'Inf. Construct', '—', 'רפא',
                      'Reflexive — "to be healed / to seek healing"; הִתְ- prefix; III-א root; לְ-preposition marks infinitive construct'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('2 Kgs 8:29',
            'כִּי הוּשַׁב הַמֶּלֶךְ',
            '"…that the king had returned." [Hophal distractor — הוּ- prefix]'))
        self.add_verb_table([
            VerbEntry('11', 'הוּשַׁב', 'Perfect', '3ms', 'שוב',
                      'NOT Hithpael — Hophal Passive: "was returned"; הוּ- prefix (u-class = Hophal); biconsonantal root שׁוּב; no הִתְ infix'),
        ], show_answers=show_answers)


def build_ch35_hithpael_weak_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch35', 'exercises',
                               'ch35-passage-exercise')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'ch35-passage-exercise.pdf')
    ex = Ch35HithpaelWeakExercise(
        title='Chapter 35 — "Spot the Hithpael" Passage Exercise',
        subtitle='(Weak Verbs)  ·  Gen 22/18  ·  Exo 20  ·  Psa 95  ·  Gen 35/44  ·  1 Sam 10  ·  2 Kgs 8',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Chapter 29 — "Spot the Hophal Weak" Passage Exercise
# ---------------------------------------------------------------------------
class Ch29HophalWeakExercise(PassageExercise):
    _instructions = (
        'Each numbered verb belongs to one of the stems you have already studied '
        '(Qal, Niphal, Hiphil, or Hophal). '
        'Focus: weak roots in the Hophal stem. '
        'For each one, fill in: Hophal? (Yes/No), Conjugation, PGN, Root, and Stem/Function. '
        'Key diagnostic: Hophal prefix vowel is always u-class (hu- Perfect, yu-/qu- Imperfect, mu- Participle). '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool):

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Genesis 39:1 + 43:18 (Joseph narrative)')

        self.add_passage(PassageBlock('Gen 39:1a',
            'הוּרַד יוֹסֵף מִצְרָיְמָה וַיִּקְנֵהוּ פּוֹטִיפַר',
            '"Now Joseph had been brought down to Egypt, and Potiphar bought him."'))
        self.add_verb_table([
            VerbEntry('1', 'הוּרַד', 'Perfect', '3ms', 'יָרַד',
                      'Hophal — was brought down (I-yod; Hiphil horid = to bring down)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 39:1b',
            'הוּבָא יוֹסֵף מִצְרָיְמָה',
            '"Joseph was brought to Egypt."'))
        self.add_verb_table([
            VerbEntry('2', 'הוּבָא', 'Perfect', '3ms', 'בּוֹא',
                      'Hophal — was brought (I-yod; Hiphil hebi = to bring)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 43:18a',
            'עַל דְּבַר הַכֶּסֶף הַשָּׁב בְּאַמְתְּחֹתֵינוּ אֲנַחְנוּ מוּבָאִים',
            '"because of the silver that was returned in our sacks, we are being brought in."'))
        self.add_verb_table([
            VerbEntry('3', 'הַשָּׁב', 'Participle', 'ms', 'שׁוּב',
                      'Hophal Ptc. — (money) that was returned (biconsonantal; Hiphil heshiv)'),
            VerbEntry('D1', 'מוּבָאִים', 'Participle', 'mp', 'בּוֹא',
                      'Hophal Ptc. mp — being brought in (mu- prefix; same root as #2)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 43:18b',
            'כִּי יוּבָא אִתָּנוּ אֶל בֵּיתוֹ',
            '"because we are being brought into his house."'))
        self.add_verb_table([
            VerbEntry('4', 'יוּבָא', 'Imperfect', '3ms', 'בּוֹא',
                      'Hophal — will be brought (yu- prefix = Hophal Impf.; I-yod)'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Exodus 40:17 + Numbers 9:15-17 (Tabernacle)')

        self.add_passage(PassageBlock('Exo 40:17',
            'וַיְהִי בַּחֹדֶשׁ הָרִאשׁוֹן בַּשָּׁנָה הַשֵּׁנִית הוּקַם הַמִּשְׁכָּן',
            '"In the first month of the second year — the tabernacle was set up."'))
        self.add_verb_table([
            VerbEntry('5', 'הוּקַם', 'Perfect', '3ms', 'קוּם',
                      'Hophal — was set up (biconsonantal; Hiphil heqim = to set up/establish)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Num 9:15',
            'וּבְיוֹם הָקִים אֶת הַמִּשְׁכָּן כִּסָּה הֶעָנָן אֶת הַמִּשְׁכָּן',
            '"And on the day he set up the tabernacle, the cloud covered the tabernacle."'))
        self.add_verb_table([
            VerbEntry('D2', 'הָקִים', 'Perfect', '3ms', 'קוּם',
                      'NOT Hophal — Hiphil active: "he set up" (ha- prefix, i-class; contrast huqam)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Num 9:17',
            'בְּהֵעָלֹת הֶעָנָן מֵעַל הַמִּשְׁכָּן יִסְעוּ בְּנֵי יִשְׂרָאֵל',
            '"Whenever the cloud lifted, the people of Israel set out."'))
        self.add_verb_table([
            VerbEntry('D3', 'יִסְעוּ', 'Qal Impf.', '3mp', 'נָסַע',
                      'NOT Hophal — Qal Impf. 3mp (I-nun assimilation; yi- prefix, not yu-)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Num 9:15 context',
            'וְאִם לֹא יֻקַּם הַמִּשְׁכָּן',
            '"And if the tabernacle was not set up…"'))
        self.add_verb_table([
            VerbEntry('6', 'יֻקַּם', 'Imperfect', '3ms', 'קוּם',
                      'Hophal — will be set up (Qibbuts yu variant; biconsonantal; same root as #5)'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Genesis 43:12 + 38:25 + Exodus 14:5')

        self.add_passage(PassageBlock('Gen 43:12',
            'וְאֶת הַכֶּסֶף הַמּוּשָׁב בְּפִי אַמְתְּחֹתֵיכֶם הוּשַׁב תָּשִׁיבוּ',
            '"and the money that was returned in the mouth of your sacks — bring it back."'))
        self.add_verb_table([
            VerbEntry('7', 'הוּשַׁב', 'Perfect', '3ms', 'שׁוּב',
                      'Hophal — was returned/brought back (biconsonantal; Hiphil heshiv)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 38:25',
            'הִוא מוּצֵאת וְהִיא שָׁלְחָה אֶל חָמִיהָ לֵאמֹר',
            '"She was being brought out, and she sent word to her father-in-law, saying…"'))
        self.add_verb_table([
            VerbEntry('8', 'מוּצֵאת', 'Participle', 'fs', 'יָצָא',
                      'Hophal Ptc. fs — being brought out (I-yod; mu- prefix; Hiphil hotzi)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 38:20',
            'וַיִּשְׁלַח יְהוּדָה אֶת גְּדִי הָעִזִּים וְלֹא מְצָאָהּ',
            '"And Judah sent the young goat, but he did not find her."'))
        self.add_verb_table([
            VerbEntry('D4', 'מְצָאָהּ', 'Qal Pf.', '3ms + 3fs', 'מָצָא',
                      'NOT Hophal — Qal Pf. 3ms + 3fs obj. suffix (me = Qal, not Hophal mu-)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 5 context',
            'הוּצָא הַחוֹמֶר מֵהֶם',
            '"The straw was taken away from them."'))
        self.add_verb_table([
            VerbEntry('9', 'הוּצָא', 'Perfect', '3ms', 'יָצָא',
                      'Hophal — was brought out (I-yod; hu- prefix; Hiphil hotzi = to bring out)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 14:5',
            'הֻגַּד לְמֶלֶךְ מִצְרַיִם כִּי בָרַח הָעָם',
            '"It was told to the king of Egypt that the people had fled."'))
        self.add_verb_table([
            VerbEntry('10', 'הֻגַּד', 'Perfect', '3ms', 'נָגַד',
                      'Hophal — it was told (I-nun assimilation + Qibbuts; Hiphil higgid = to tell)'),
        ], show_answers=show_answers)


def build_ch29_hophal_weak_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch29', 'exercises',
                               'ch29-passage-exercise')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'ch29-passage-exercise.pdf')
    ex = Ch29HophalWeakExercise(
        title='Chapter 29 — "Spot the Hophal Weak" Passage Exercise',
        subtitle='Genesis 39-43  /  Exodus 40 + Numbers 9  /  Genesis 38 + Exodus 14',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Chapter 31 — "Spot the Piel Weak" Passage Exercise
# ---------------------------------------------------------------------------
class Ch31PielWeakExercise(PassageExercise):
    _instructions = (
        'Each numbered verb belongs to one of the stems you have already studied '
        '(Qal, Niphal, Hiphil, Hophal, or Piel). '
        'Focus: weak roots in the Piel stem, especially III-he roots. '
        'For each one, fill in: Piel? (Yes/No), Conjugation, PGN, Root, and Stem/Function. '
        'Distractor verbs D1-D3 are not Piel — drawn from Hiphil and Hophal. '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool):

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Genesis 2:16; 3:11, 17 (Garden commands)')

        self.add_passage(PassageBlock('Gen 2:16',
            'וַיְצַו יְהוָה אֱלֹהִים עַל הָאָדָם לֵאמֹר',
            '"And the LORD God commanded the man, saying…"'))
        self.add_verb_table([
            VerbEntry('1', 'וַיְצַו', 'Wayyiqtol', '3ms', 'צָוָה',
                      'Denominative — "commanded"; III-he apocopated in Wayyiqtol: vayyetsav'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 3:11',
            'הֲמִן הָעֵץ אֲשֶׁר צִוִּיתִיךָ לְבִלְתִּי אֲכָל מִמֶּנּוּ',
            '"Have you eaten from the tree of which I commanded you not to eat?"'))
        self.add_verb_table([
            VerbEntry('2', 'צִוִּיתִיךָ', 'Perfect', '1cs + 2ms', 'צָוָה',
                      'Denominative — "I commanded you"; Hireq + dagesh in R2 + 1cs + 2ms obj.'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 3:17',
            'כִּי שָׁמַעְתָּ לְקוֹל אִשְׁתֶּךָ אֲשֶׁר צִוִּיתִיךָ לֵאמֹר',
            '"because you listened to your wife about the tree which I commanded you…"'))
        self.add_verb_table([
            VerbEntry('3', 'צִוִּיתִיךָ', 'Perfect', '1cs + 2ms', 'צָוָה',
                      'Denominative — same form as #2; God repeats in verdict speech'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Genesis 6:18-20 + 18:19 + Exodus 1:17')

        self.add_passage(PassageBlock('Gen 6:18-19',
            'וַהֲקִמֹתִי אֶת בְּרִיתִי אִתָּךְ לְהַחֲיוֹת אִתָּךְ',
            '"and I will establish my covenant with you, to keep alive with you…"'))
        self.add_verb_table([
            VerbEntry('D1', 'לְהַחֲיוֹת', 'Hiphil Inf.Const.', '—', 'חָיָה',
                      'NOT Piel — Hiphil Inf. Const. (leha- prefix); "to keep alive" (causative)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 6:19',
            'חִיָּה אֶת אֲשֶׁר בָּאָרֶץ',
            '"Keep alive what is on the earth."'))
        self.add_verb_table([
            VerbEntry('4', 'חִיָּה', 'Perfect', '3ms', 'חָיָה',
                      'Factitive — "kept alive"; III-he: Hireq + dagesh in R2 + qamets-he'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 18:19',
            'לְמַעַן אֲשֶׁר יְצַוֶּה אֶת בָּנָיו וְאֶת בֵּיתוֹ אַחֲרָיו',
            '"so that he will command his sons and his household after him…"'))
        self.add_verb_table([
            VerbEntry('5', 'יְצַוֶּה', 'Imperfect', '3ms', 'צָוָה',
                      'Denominative — III-he Impf. 3ms: ye- prefix + patach + dagesh in R2 + tsere-he'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 1:17',
            'וַיְחַיּוּ אֶת יַלְדֵי הַנָּשִׁים הָעִבְרִיּוֹת',
            '"and they kept alive the male children of the Hebrew women." (the midwives)'))
        self.add_verb_table([
            VerbEntry('6', 'וַיְחַיּוּ', 'Wayyiqtol', '3mp', 'חָיָה',
                      'Factitive — III-he Wayyiqtol 3mp: vayyeh + cha + yod (dagesh in yod) + u suffix'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Genesis 16:6 + Deuteronomy 8:2-3 (Humbling)')

        self.add_passage(PassageBlock('Gen 16:6',
            'עִנָּה אֹתָהּ שָׂרַי',
            '"Sarai afflicted / humbled her."'))
        self.add_verb_table([
            VerbEntry('7', 'עִנָּה', 'Perfect', '3ms', 'עָנָה',
                      'Factitive — "she afflicted/humbled"; III-he: Hireq + dagesh in R2 + qamets-he'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Deu 8:2',
            'לְמַעַן עַנֹּתְךָ לְנַסֹּתְךָ',
            '"to humble you and to test you…"'))
        self.add_verb_table([
            VerbEntry('8', 'עַנֹּתְךָ', 'Inf. Construct', '— + 2ms', 'עָנָה',
                      'Factitive — III-he Inf. Const. + 2ms suffix: patach + dagesh in nun + tav'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Deu 8:3',
            'לְמַעַן הוֹדִיעֲךָ כִּי לֹא עַל הַלֶּחֶם לְבַדּוֹ יִחְיֶה הָאָדָם',
            '"in order to make you know that man does not live by bread alone."'))
        self.add_verb_table([
            VerbEntry('D2', 'הוֹדִיעֲךָ', 'Hiphil Inf.Const.', '— + 2ms', 'יָדַע',
                      'NOT Piel — Hiphil Inf. Const. of I-yod root yada (ho- prefix); "to make known"'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Deu 8:2 parallel',
            'יְעַנֶּה יְהוָה אֱלֹהֶיךָ אֹתְךָ בַּמִּדְבָּר',
            '"The LORD your God will humble you in the wilderness."'))
        self.add_verb_table([
            VerbEntry('9', 'יְעַנֶּה', 'Imperfect', '3ms', 'עָנָה',
                      'Factitive — III-he Impf. 3ms: ye- + patach + dagesh in nun + tsere-he ending'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage D ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage D — Amos 3:7 + Genesis 50:16 + Deuteronomy 8:1')

        self.add_passage(PassageBlock('Amos 3:7',
            'כִּי לֹא יַעֲשֶׂה אֲדֹנָי יְהוִה דָּבָר כִּי אִם גִּלָּה סוֹדוֹ אֶל עֲבָדָיו הַנְּבִיאִים',
            '"For the Lord GOD does nothing without revealing his secret to his servants the prophets."'))
        self.add_verb_table([
            VerbEntry('10', 'גִּלָּה', 'Perfect', '3ms', 'גָּלָה',
                      'Declarative/Intensive — "revealed"; III-he: Hireq + dagesh in lamed + qamets-he'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 50:16',
            'וַיְצַוּוּ אֶל יוֹסֵף לֵאמֹר אָבִיךָ צִוָּה לִפְנֵי מוֹתוֹ',
            '"They sent a command to Joseph, saying, Your father gave orders before his death…"'))
        self.add_verb_table([
            VerbEntry('11', 'וַיְצַוּוּ', 'Wayyiqtol', '3mp', 'צָוָה',
                      'Denominative — Wayyiqtol 3mp of tsavah III-he; "they commanded"'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Deu 8:1',
            'כָּל הַמִּצְוָה אֲשֶׁר אָנֹכִי מְצַוְּךָ הַיּוֹם תִּשְׁמְרוּן לַעֲשׂוֹת',
            '"All the commandment that I am commanding you today, you shall be careful to do."'))
        self.add_verb_table([
            VerbEntry('12', 'מְצַוְּךָ', 'Participle', 'ms + 2ms', 'צָוָה',
                      'Denominative — Piel Ptc. ms + 2ms suffix: me- + patach + dagesh in R2'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Gen 39:1 (review)',
            'הוּבָא יוֹסֵף מִצְרָיְמָה',
            '"Joseph was brought to Egypt." (Cross-stem review — compare Ch29)'))
        self.add_verb_table([
            VerbEntry('D3', 'הוּבָא', 'Hophal Pf.', '3ms', 'בּוֹא',
                      'NOT Piel — Hophal Pf. 3ms (hu- prefix = u-class = Hophal passive); "was brought"'),
        ], show_answers=show_answers)


def build_ch31_piel_weak_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch31', 'exercises',
                               'ch31-passage-exercise')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'ch31-passage-exercise.pdf')
    ex = Ch31PielWeakExercise(
        title='Chapter 31 — "Spot the Piel Weak" Passage Exercise',
        subtitle='Gen 2-3, 6, 16, 18  /  Exo 1  /  Deu 8  /  Amos 3  /  Gen 50',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Chapter 32 — "Spot the Pual" Passage Exercise (Pual Strong)
# ---------------------------------------------------------------------------
class Ch32PualExercise(PassageExercise):
    _instructions = (
        'Each numbered verb belongs to one of the stems you have already studied '
        '(Qal, Niphal, Hiphil, Hophal, or Piel/Pual). '
        'For each one, fill in: Pual? (Yes/No), Conjugation, PGN, Root, and Stem/Function. '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool):

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Numbers 22:6, 12; 23:8, 20 (Balaam cycle)')

        self.add_passage(PassageBlock('22:6',
            'כִּי יָדַעְתִּי אֵת אֲשֶׁר תְּבָרֵךְ מְבֹרָךְ וַאֲשֶׁר תָּאֹר יוּאָר',
            '"…for I know that he whom you bless is blessed, and he whom you curse is cursed."'))
        self.add_verb_table([
            VerbEntry('1', 'תְּבָרֵךְ', 'Imperfect',  '2ms', 'בָּרַךְ', 'NOT Pual — Piel Intensive: "you bless"; tsere under R2 = Piel active'),
            VerbEntry('2', 'מְבֹרָךְ',  'Participle', 'ms',  'בָּרַךְ', 'Passive — Pual Ptc. ms; Qamets under R1 (compensatory for ר rejecting dagesh)'),
            VerbEntry('3', 'יוּאָר',    'Imperfect',  '3ms', 'אָרַר',   'NOT Pual — Hophal: "shall be cursed"; יוּ prefix = u-class on preformative = Hophal Impf. marker'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('22:12',
            'לֹא תֵלֵךְ עִמָּהֶם לֹא תָאֹר אֶת הָעָם כִּי בָרוּךְ הוּא',
            '"You shall not go with them. You shall not curse the people, for they are blessed."'))
        self.add_verb_table([
            VerbEntry('4', 'תָאֹר',   'Imperfect', '2ms', 'אָרַר', 'NOT Pual — Qal: "you shall curse"; no u-class vowel under R1 with Dagesh in R2'),
            VerbEntry('5', 'בָּרוּךְ', 'Participle', 'ms', 'בָּרַךְ', 'Passive — Pual Ptc. ms (substantival: "blessed one"); Qamets = compensatory for ר'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('23:8',
            'מַה אֶקֹּב לֹא קַבֹּה אֵל וּמַה אֶזְעֹם לֹא זָעַם יְהוָה',
            '"How shall I curse what God has not cursed, and how shall I denounce what the LORD has not denounced?"'))
        self.add_verb_table([
            VerbEntry('6', 'קַבֹּה', 'Qal Inf.Abs.', '—',  'קָבַב', 'NOT Pual — Qal Inf. Abs.; geminate root; no Qibbuts + R2 dagesh'),
            VerbEntry('7', 'זָעַם',  'Perfect',      '3ms', 'זָעַם', 'NOT Pual — Qal Perf. 3ms; Qamets-Patach = Qal pattern; no u-class under R1'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('23:20',
            'הִנֵּה בָרֵךְ לָקָחְתִּי וּבֵרַךְ וְלֹא אֲשִׁיבֶנָּה',
            '"Behold, I have received a command to bless; he has blessed, and I cannot revoke it."'))
        self.add_verb_table([
            VerbEntry('8', 'בָרֵךְ', 'Inf. Absolute', '—', 'בָּרַךְ', 'NOT Pual — Piel Inf. Abs.: "to bless"; tsere under R2 = Piel active'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Exodus 29:36–37 (Consecration of the Altar)')

        self.add_passage(PassageBlock('29:36',
            'וּמָשַׁחְתָּ אֹתוֹ לְקַדְּשׁוֹ',
            '"…and you shall anoint it to consecrate it."'))
        self.add_verb_table([
            VerbEntry('9', 'וּמָשַׁחְתָּ', 'Weqatal', '2ms', 'מָשַׁח', 'NOT Pual — Qal Weqatal: "and you shall anoint"; no u-class under R1'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('29:37',
            'שִׁבְעַת יָמִים תְּכַפֵּר עַל הַמִּזְבֵּחַ וְקִדַּשְׁתָּ אֹתוֹ וְהָיָה הַמִּזְבֵּחַ קֹדֶשׁ קָדָשִׁים כָּל הַנֹּגֵעַ בַּמִּזְבֵּחַ יִקְדָּשׁ',
            '"Seven days you shall make atonement for the altar and consecrate it, and the altar shall be most holy; whatever touches the altar shall be consecrated."'))
        self.add_verb_table([
            VerbEntry('10', 'וְקִדַּשְׁתָּ', 'Weqatal',     '2ms', 'קָדַשׁ', 'NOT Pual — Piel Factitive: "and you shall consecrate"; Hireq under R1 (קִ) = Piel'),
            VerbEntry('11', 'וְהָיָה',       'Weqatal',     '3ms', 'הָיָה',  'NOT Pual — Qal Weqatal: "and it shall be"; III-ה Qal'),
            VerbEntry('12', 'יִקְדָּשׁ',      'Niphal Impf.', '3ms', 'קָדַשׁ', 'NOT Pual — Niphal passive/reflexive: "shall be consecrated"; יִ + dagesh in R1 = Niphal; compare Pual: יְקֻדַּשׁ'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Exodus 14:4; Isaiah 43:23; Exodus 40:17 (Pual of כבד + Hophal distractor)')

        self.add_passage(PassageBlock('Exo 14:4',
            'וְכָבַדְתִּי בְּפַרְעֹה וּבְכָל חֵילוֹ',
            '"And I will get glory through Pharaoh and all his host."'))
        self.add_verb_table([
            VerbEntry('13', 'וְכָבַדְתִּי', 'Weqatal', '1cs', 'כָּבֵד', 'NOT Pual — Niphal reflexive: "I will be glorified / get glory"; contracted Niphal prefix; no Qibbuts under R1'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Isa 43:23',
            'לֹא כֻבַּדְתַּנִי בְּקָרְבָּנֶיךָ',
            '"You have not honored me with your offerings."'))
        self.add_verb_table([
            VerbEntry('14', 'כֻּבַּדְתַּנִי', 'Perfect', '2ms', 'כָּבֵד', 'Passive — Pual: "you have not honored me"; Qibbuts under R1 (כֻ) + Dagesh in R2 (בּ) = Pual diagnostic'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Exo 40:17',
            'הוּקַם הַמִּשְׁכָּן בְּיוֹם הַחֹדֶשׁ הָרִאשׁוֹן',
            '"The tabernacle was set up on the first day of the first month."'))
        self.add_verb_table([
            VerbEntry('15', 'הוּקַם', 'Perfect', '3ms', 'קוּם', 'NOT Pual — Hophal: "was set up/raised"; הוּ prefix = Hophal Perf. marker; hollow root has no R2 for dagesh; contrast Pual: קֻטַּל pattern'),
        ], show_answers=show_answers)

        if not show_answers:
            self.add_reflection([
                'In Passage A, verbs 1 (Piel) and 2 (Pual) come from the same root ברך. The root has R2=ר, '
                'which rejects Dagesh Forte. How does the Pual compensate for the missing dagesh, and why does '
                'this make the Pual and Piel of ברך harder to distinguish than strong-root counterparts?',
                'Verb 3 (יוּאָר, Hophal) and verb 14 (כֻּבַּדְתַּנִי, Pual) both express passive meaning. '
                'What is the key visual feature that distinguishes a Hophal from a Pual? '
                'What does each stem tell you about the corresponding active stem?',
                'Verbs 10 (Piel Weqatal) and 12 (Niphal Impf.) from Exo 29:37 use the same root קדש. '
                'The priest actively consecrates (Piel); then whatever touches becomes holy (Niphal). '
                'How does this passage illustrate the Piel-as-cause / Niphal-as-resulting-state distinction?',
            ])


def build_ch32_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch32', 'exercises',
                               'ch32-passage-exercise')
    path = os.path.join(out_dir, 'ch32-passage-exercise.pdf')
    ex = Ch32PualExercise(
        title='Chapter 32 — "Spot the Pual" Passage Exercise',
        subtitle='Num 22–23  ·  Exo 29  ·  Isa 43',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Chapter 33 — "Spot the Pual" Passage Exercise (Pual Weak)
# ---------------------------------------------------------------------------
class Ch33PualWeakExercise(PassageExercise):
    _instructions = (
        'Each numbered verb belongs to one of the stems you have already studied '
        '(Qal, Niphal, Hiphil, Hophal, Piel, or Pual). '
        'For each one, fill in: Pual? (Yes/No), Conjugation, PGN, Root, and Stem/Function. '
        'For each Pual form, also identify the weak-root type (I-י, I-נ, III-ה, or R2=ר). '
        'The answer key begins on the page marked "Answer Key".'
    )

    def _render_passages(self, show_answers: bool):

        # ── Passage A ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage A — Genesis Genealogies (Gen 4:18; 4:26; 46:22; 6:1)')

        self.add_passage(PassageBlock('4:18',
            'וְעִירָד יָלַד אֶת מְחוּיָאֵל',
            '"And Irad fathered Mehujael."'))
        self.add_verb_table([
            VerbEntry('1', 'יָלַד', 'Perfect', '3ms', 'יָלַד', 'NOT Pual — Qal: "fathered/begat" (active); Qal Perf 3ms vowel pattern; no Qibbuts under R1'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('4:26',
            'אָז הוּחַל לִקְרֹא בְּשֵׁם יְהוָה',
            '"At that time people began to call upon the name of the LORD."'))
        self.add_verb_table([
            VerbEntry('2', 'הוּחַל', 'Perfect', '3ms', 'חָלַל', 'NOT Pual — Hophal: "was begun"; הוּ prefix = Hophal Perf. marker; geminate root; no Qibbuts under R1'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('46:22',
            'אֵלֶּה בְּנֵי רָחֵל אֲשֶׁר יֻלַּד לְיַעֲקֹב',
            '"These are the sons of Rachel who were born to Jacob."'))
        self.add_verb_table([
            VerbEntry('3', 'יֻלַּד', 'Perfect', '3ms', 'יָלַד', 'Passive — Pual; I-י root: "was born/begotten"; Qibbuts under R1 (יֻ) + Dagesh in R2 (לּ); Piel = "to beget" → Pual = "to be born"'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('6:1',
            'וַיִּוָּלְדוּ לָהֶם בָנִים',
            '"And sons were born to them."'))
        self.add_verb_table([
            VerbEntry('4', 'וַיִּוָּלְדוּ', 'Wayyiqtol', '3mp', 'יָלַד', 'NOT Pual — Niphal Wayyiqtol 3mp: "were born"; יִוָּ = Niphal with I-י (yod assimilates with dagesh); compare Pual יֻלַּד: Qibbuts vs. Niphal יִ'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage B ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage B — Leviticus 7:36; Numbers 3:9 (I-נ root נתן)')

        self.add_note('I-נ Pual: unlike Qal Imperfect where נ assimilates (יִתֵּן), '
                      'in the Pual the נ stays as R1 and takes Qibbuts. '
                      'Dagesh Forte falls on R2 (ת), not on an assimilated consonant.')

        self.add_passage(PassageBlock('Lev 7:36',
            'אֲשֶׁר צִוָּה יְהוָה לָתֵת לָהֶם',
            '"…which the LORD commanded to give to them."'))
        self.add_verb_table([
            VerbEntry('5', 'צִוָּה', 'Perfect', '3ms', 'צָוָה', 'NOT Pual — Piel active: "commanded"; Hireq under R1 (צִ) = Piel i-class; Pual passive would be צֻוָּה'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Num 3:9',
            'וְנָתַתָּ אֶת הַלְוִיִּם לְאַהֲרֹן וּלְבָנָיו נְתֻנִים נְתֻנִים הֵמָּה',
            '"And you shall give the Levites to Aaron and his sons; they are given, given."'))
        self.add_verb_table([
            VerbEntry('6', 'וְנָתַתָּ',  'Weqatal',   '2ms', 'נָתַן', 'NOT Pual — Qal Weqatal: "and you shall give"; no u-class under R1'),
            VerbEntry('7', 'נְתֻנִים',   'Participle', 'mp',  'נָתַן', 'Passive — Pual Ptc. mp; I-נ root: "given" (substantival); Qibbuts under תֻ; נ retained as R1 (does not assimilate in Pual)'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Num 3:9b',
            'נֻתְּנוּ לִי הֵמָּה מִתּוֹךְ בְּנֵי יִשְׂרָאֵל',
            '"They were given to me from among the people of Israel."'))
        self.add_verb_table([
            VerbEntry('8', 'נֻתְּנוּ', 'Perfect', '3cp', 'נָתַן', 'Passive — Pual; I-נ root: "were given"; Qibbuts under R1 (נֻ) + Dagesh in R2 (תּ) + 3cp suffix וּ'),
        ], show_answers=show_answers)

        self.add_section_break()

        # ── Passage C ─────────────────────────────────────────────────────────
        self.add_section_heading('Passage C — Leviticus 8:35; Numbers 22:6; Psalm 72:17 (III-ה and R2=ר)')

        self.add_passage(PassageBlock('Lev 8:35',
            'כַּאֲשֶׁר צֻוֵּיתִי אֲנִי כֵּן צֻוֵּיתֶם',
            '"As I was commanded, so you were commanded."'))
        self.add_verb_table([
            VerbEntry('9',  'צֻוֵּיתִי', 'Perfect', '1cs', 'צָוָה', 'Passive — Pual; III-ה root: "I was commanded"; Qibbuts under R1 (צֻ) + Dagesh in R2 (וּ) + III-ה Perfect 1cs suffix יתִי'),
            VerbEntry('10', 'צֻוֵּיתֶם', 'Perfect', '2mp', 'צָוָה', 'Passive — Pual; III-ה root: "you were commanded"; same Pual diagnostic; 2mp suffix יתֶם'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Num 22:6',
            'כִּי יָדַעְתִּי אֵת אֲשֶׁר תְּבָרֵךְ מְבֹרָךְ וַאֲשֶׁר תָּאֹר יוּאָר',
            '"…for I know that he whom you bless is blessed, and he whom you curse is cursed."'))
        self.add_verb_table([
            VerbEntry('11', 'תְּבָרֵךְ', 'Imperfect',  '2ms', 'בָּרַךְ', 'NOT Pual — Piel Intensive: "you bless" (active); tsere under R2; R2=ר rejects dagesh but this is Piel'),
            VerbEntry('12', 'מְבֹרָךְ',  'Participle', 'ms',  'בָּרַךְ', 'Passive — Pual Ptc. ms; R2=ר (weak): Qamets under R1 (compensatory for ר rejecting dagesh)'),
            VerbEntry('13', 'יוּאָר',    'Imperfect',  '3ms', 'אָרַר',   'NOT Pual — Hophal: "shall be cursed"; יוּ prefix = u-class on preformative = Hophal Impf. marker'),
        ], show_answers=show_answers)

        self.add_passage(PassageBlock('Psa 72:17',
            'יְבֹרַךְ שְׁמוֹ לְעוֹלָם יִתְנַהֵל לִפְנֵי שֶׁמֶשׁ שְׁמוֹ',
            '"May his name be blessed forever; may his name endure before the sun."'))
        self.add_verb_table([
            VerbEntry('14', 'יְבֹרַךְ',   'Imperfect', '3ms', 'בָּרַךְ', 'Passive — Pual Impf.: "may his name be blessed"; R2=ר; Qamets under R1 (compensatory); jussive expressing prayer'),
            VerbEntry('15', 'יִתְנַהֵל', 'Imperfect', '3ms', 'נָהַל',  'NOT Pual — Hithpael: "may endure/continue"; יִתְ prefix = Hithpael marker; no Qibbuts under R1'),
        ], show_answers=show_answers)

        if not show_answers:
            self.add_reflection([
                'Verb 3 (יֻלַּד, I-י Pual Perfect) and verb 4 (וַיִּוָּלְדוּ, Niphal Wayyiqtol) '
                'both come from ילד and both express passive meaning. What visual feature most '
                'immediately distinguishes the Pual from the Niphal in these I-י forms?',
                'Verbs 7–8 (נְתֻנִים / נֻתְּנוּ, I-נ Pual) show that in the Pual, נ stays as R1 '
                'and takes Qibbuts rather than assimilating as in the Qal Imperfect (יִתֵּן). '
                'What grammatical principle causes the different behavior between stems?',
                'Verbs 9–10 (צֻוֵּיתִי / צֻוֵּיתֶם, III-ה Pual) parallel verb 5 (צִוָּה, Piel active). '
                'What single vowel under R1 most quickly identifies Piel vs. Pual? '
                'How does this i/u distinction work in the strong paradigm (קִטֵּל vs. קֻטַּל)?',
            ])


def build_ch33_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch33', 'exercises',
                               'ch33-passage-exercise')
    path = os.path.join(out_dir, 'ch33-passage-exercise.pdf')
    ex = Ch33PualWeakExercise(
        title='Chapter 33 — "Spot the Pual" Passage Exercise (Weak Roots)',
        subtitle='Gen 4  ·  Lev 7–8  ·  Num 3, 22  ·  Psa 72',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Ch1–Ch6 builders
# ---------------------------------------------------------------------------

class Ch1LetterRecognitionExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each Hebrew letter shown, provide: (1) Letter Name, '
            '(2) Transliteration, (3) Sound, (4) Any special category '
            '(guttural / begadkephat / sofit form / normal).\n'
            'Items 1–22 cover all standard letters in canonical order. '
            'Items 23–27 cover the five sofit (final) forms. '
            'Items 28–30 show three begadkephat letters with dagesh lene.'
        )
        self.add_section_heading('Part A — Standard Letters (1–22)')
        rows_a = [
            ['1', 'א', '', '', '', ''],
            ['2', 'ב', '', '', '', ''],
            ['3', 'ג', '', '', '', ''],
            ['4', 'ד', '', '', '', ''],
            ['5', 'ה', '', '', '', ''],
            ['6', 'ו', '', '', '', ''],
            ['7', 'ז', '', '', '', ''],
            ['8', 'ח', '', '', '', ''],
            ['9', 'ט', '', '', '', ''],
            ['10', 'י', '', '', '', ''],
            ['11', 'כ', '', '', '', ''],
            ['12', 'ל', '', '', '', ''],
            ['13', 'מ', '', '', '', ''],
            ['14', 'נ', '', '', '', ''],
            ['15', 'ס', '', '', '', ''],
            ['16', 'ע', '', '', '', ''],
            ['17', 'פ', '', '', '', ''],
            ['18', 'צ', '', '', '', ''],
            ['19', 'ק', '', '', '', ''],
            ['20', 'ר', '', '', '', ''],
            ['21', 'שׁ', '', '', '', ''],
            ['22', 'ת', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'א', 'Aleph', 'ʾ', 'Silent/glottal stop', 'Guttural; quiescent'],
            ['2', 'ב', 'Beth', 'b / v', 'b (hard) or v (soft)', 'Begadkephat'],
            ['3', 'ג', 'Gimel', 'g / gh', 'g (hard) or gh (soft)', 'Begadkephat'],
            ['4', 'ד', 'Dalet', 'd / dh', 'd (hard) or dh (soft)', 'Begadkephat'],
            ['5', 'ה', 'He', 'h', 'h', 'Guttural; quiescent word-finally'],
            ['6', 'ו', 'Waw', 'w', 'w (consonantal)', 'Also mater lectionis'],
            ['7', 'ז', 'Zayin', 'z', 'z', 'Normal'],
            ['8', 'ח', 'Cheth', 'ḥ', 'ch as in German Bach', 'Guttural'],
            ['9', 'ט', 'Teth', 'ṭ', 'emphatic t', 'Normal (emphatic)'],
            ['10', 'י', 'Yod', 'y', 'y (consonantal)', 'Also mater lectionis'],
            ['11', 'כ', 'Kaph', 'k / kh', 'k (hard) or kh (soft)', 'Begadkephat; has sofit form'],
            ['12', 'ל', 'Lamed', 'l', 'l', 'Normal'],
            ['13', 'מ', 'Mem', 'm', 'm', 'Normal; has sofit form'],
            ['14', 'נ', 'Nun', 'n', 'n', 'Normal; has sofit form'],
            ['15', 'ס', 'Samech', 's', 's', 'Normal'],
            ['16', 'ע', 'Ayin', 'ʿ', 'Silent/pharyngeal', 'Guttural'],
            ['17', 'פ', 'Pe', 'p / f', 'p (hard) or f (soft)', 'Begadkephat; has sofit form'],
            ['18', 'צ', 'Tsade', 'ṣ', 'emphatic ts', 'Normal (emphatic); has sofit form'],
            ['19', 'ק', 'Qoph', 'q', 'q (uvular k)', 'Normal'],
            ['20', 'ר', 'Resh', 'r', 'r (uvular)', 'Behaves like guttural in some contexts'],
            ['21', 'שׁ', 'Shin', 'š', 'sh as in sheep', 'Normal (shin dot on right)'],
            ['22', 'ת', 'Taw', 't / th', 't (hard) or th (soft)', 'Begadkephat'],
        ]
        self.add_generic_table(
            headers=['#', 'Letter', 'Name', 'Transliteration', 'Sound', 'Special Category'],
            rows=rows_a,
            col_ratios=[0.05, 0.08, 0.12, 0.12, 0.14, 0.49],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans_a,
        )
        self.add_section_heading('Part B — Final (Sofit) Forms (23–27)')
        rows_b = [
            ['23', 'ך', '', '', '', ''],
            ['24', 'ם', '', '', '', ''],
            ['25', 'ן', '', '', '', ''],
            ['26', 'ף', '', '', '', ''],
            ['27', 'ץ', '', '', '', ''],
        ]
        ans_b = [
            ['23', 'ך', 'Kaph sofit', 'k / kh', 'k (hard) or kh (soft)', 'Sofit form of כ; occurs word-finally only'],
            ['24', 'ם', 'Mem sofit', 'm', 'm', 'Sofit form of מ; occurs word-finally only'],
            ['25', 'ן', 'Nun sofit', 'n', 'n', 'Sofit form of נ; occurs word-finally only'],
            ['26', 'ף', 'Pe sofit', 'p / f', 'p (hard) or f (soft)', 'Sofit form of פ; occurs word-finally only'],
            ['27', 'ץ', 'Tsade sofit', 'ṣ', 'emphatic ts', 'Sofit form of צ; occurs word-finally only'],
        ]
        self.add_generic_table(
            headers=['#', 'Letter', 'Name', 'Transliteration', 'Sound', 'Special Category'],
            rows=rows_b,
            col_ratios=[0.05, 0.08, 0.12, 0.12, 0.14, 0.49],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans_b,
        )
        self.add_section_heading('Part C — Begadkephat with Dagesh Lene (28–30)')
        rows_c = [
            ['28', 'בּ', '', '', '', ''],
            ['29', 'כּ', '', '', '', ''],
            ['30', 'פּ', '', '', '', ''],
        ]
        ans_c = [
            ['28', 'בּ', 'Beth (dagesh lene)', 'b', 'b as in boy — hard stop', 'Begadkephat — hard pronunciation'],
            ['29', 'כּ', 'Kaph (dagesh lene)', 'k', 'k as in king — hard stop', 'Begadkephat — hard pronunciation'],
            ['30', 'פּ', 'Pe (dagesh lene)', 'p', 'p as in pan — hard stop', 'Begadkephat — hard pronunciation'],
        ]
        self.add_generic_table(
            headers=['#', 'Letter', 'Name', 'Transliteration', 'Sound', 'Special Category'],
            rows=rows_c,
            col_ratios=[0.05, 0.08, 0.12, 0.12, 0.14, 0.49],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans_c,
        )


def build_ch1_letter_recognition(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch1', 'exercises',
                               'ch1-letter-recognition')
    path = os.path.join(out_dir, 'ch1-letter-recognition.pdf')
    ex = Ch1LetterRecognitionExercise(
        title='Chapter 1 — Hebrew Letter Recognition Exercise',
        subtitle='Hebrew Alphabet — Letter Identification',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch2VowelIdentificationExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each Hebrew form shown, identify: (1) Vowel Name, '
            '(2) Vowel Class (A / E / I / O / U / Reduced), '
            '(3) Quantity (Long / Short / Reduced), '
            '(4) Notes (e.g., mater lectionis present, composite sheva, dagesh forte).\n'
            'Items 1–5: A-class. 6–10: E-class. 11–13: I-class. '
            '14–17: O-class. 18–19: U-class. 20–21: Simple Sheva. '
            '22–24: Hatef Shevas. 25: Dagesh Forte.'
        )
        rows = [
            ['1', 'מָ', '', '', '', ''],
            ['2', 'מַ', '', '', '', ''],
            ['3', 'מָ (closed, unaccented)', '', '', '', ''],
            ['4', 'מֲ', '', '', '', ''],
            ['5', 'דָּבָר', '', '', '', ''],
            ['6', 'מֵ', '', '', '', ''],
            ['7', 'מֶ', '', '', '', ''],
            ['8', 'מֵי', '', '', '', ''],
            ['9', 'מֱ', '', '', '', ''],
            ['10', 'בֵּן', '', '', '', ''],
            ['11', 'מִ', '', '', '', ''],
            ['12', 'מִי', '', '', '', ''],
            ['13', 'כִּי', '', '', '', ''],
            ['14', 'מֹ', '', '', '', ''],
            ['15', 'מוֹ', '', '', '', ''],
            ['16', 'מָ (= Qamets Hatuf)', '', '', '', ''],
            ['17', 'מֳ', '', '', '', ''],
            ['18', 'מֻ', '', '', '', ''],
            ['19', 'מוּ', '', '', '', ''],
            ['20', 'מְ (word-initial)', '', '', '', ''],
            ['21', 'מְ (word-final)', '', '', '', ''],
            ['22', 'הֲ', '', '', '', ''],
            ['23', 'הֱ', '', '', '', ''],
            ['24', 'הֳ', '', '', '', ''],
            ['25', 'מַּ (dagesh forte + patah)', '', '', '', ''],
        ]
        ans = [
            ['1', 'מָ', 'Qamets', 'A', 'Long', 'Standard long A; T-bar shape below consonant'],
            ['2', 'מַ', 'Patah', 'A', 'Short', 'Standard short A; horizontal bar below consonant'],
            ['3', 'מָ (closed, unaccented)', 'Qamets Hatuf', 'O', 'Short', 'Same shape as Qamets; O-class in closed unaccented syllable'],
            ['4', 'מֲ', 'Hatef Patah', 'A', 'Reduced', 'Composite sheva; A-class; used under gutturals'],
            ['5', 'דָּבָר', 'Qamets × 2', 'A', 'Long', 'Both vowels Qamets (long A); Dagesh Forte in dalet'],
            ['6', 'מֵ', 'Tsere', 'E', 'Long', 'Standard long E; two dots horizontally below consonant'],
            ['7', 'מֶ', 'Seghol', 'E', 'Short', 'Standard short E; three dots (inverted triangle)'],
            ['8', 'מֵי', 'Tsere Yod', 'E', 'Long', 'Tsere with yod mater lectionis; yod is quiescent'],
            ['9', 'מֱ', 'Hatef Seghol', 'E', 'Reduced', 'Composite sheva; E-class; used under gutturals'],
            ['10', 'בֵּן', 'Tsere', 'E', 'Long', 'Long E under bet; dagesh lene in bet; final nun closes'],
            ['11', 'מִ', 'Hireq', 'I', 'Short', 'Standard short I; single dot below consonant'],
            ['12', 'מִי', 'Hireq Yod', 'I', 'Long', 'Hireq with yod mater lectionis; yod is quiescent'],
            ['13', 'כִּי', 'Hireq Yod', 'I', 'Long', 'Long I with yod mater; dagesh lene in kaph'],
            ['14', 'מֹ', 'Holem', 'O', 'Long', 'Long O; single dot above the letter to the upper left'],
            ['15', 'מוֹ', 'Holem Vav', 'O', 'Long', 'Holem with vav mater lectionis; vav is quiescent'],
            ['16', 'מָ (= Qamets Hatuf)', 'Qamets Hatuf', 'O', 'Short', 'O-class, short; same glyph as Qamets; closed unaccented syllable'],
            ['17', 'מֳ', 'Hatef Qamets', 'O', 'Reduced', 'Composite sheva; O-class; least common hatef sheva'],
            ['18', 'מֻ', 'Qibbuts', 'U', 'Short', 'Short U; three diagonal dots below consonant'],
            ['19', 'מוּ', 'Shureq', 'U', 'Long', 'Long U; vav with a dot in its center; vav is mater'],
            ['20', 'מְ (word-initial)', 'Vocal Sheva', 'Reduced', 'Reduced', 'Vocal — word must begin with a vowel sound; /ə/'],
            ['21', 'מְ (word-final)', 'Silent Sheva', '—', '—', 'Silent — marks the close of the final syllable'],
            ['22', 'הֲ', 'Hatef Patah', 'A', 'Reduced', 'Composite sheva; most common hatef; under א and ע'],
            ['23', 'הֱ', 'Hatef Seghol', 'E', 'Reduced', 'Composite sheva; E-class; less common than Hatef Patah'],
            ['24', 'הֳ', 'Hatef Qamets', 'O', 'Reduced', 'Composite sheva; O-class; least common of the three'],
            ['25', 'מַּ (dagesh forte + patah)', 'Patah', 'A', 'Short', 'Patah under mem; dot inside mem is Dagesh Forte'],
        ]
        self.add_generic_table(
            headers=['#', 'Form', 'Vowel Name', 'Class', 'Quantity', 'Notes'],
            rows=rows,
            col_ratios=[0.05, 0.10, 0.14, 0.08, 0.10, 0.53],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans,
        )


def build_ch2_vowel_identification(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch2', 'exercises',
                               'ch2-vowel-identification')
    path = os.path.join(out_dir, 'ch2-vowel-identification.pdf')
    ex = Ch2VowelIdentificationExercise(
        title='Chapter 2 — Vowel Identification Exercise',
        subtitle='Hebrew Vowels — Identification and Classification',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch3SyllableDivisionExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each word: (1) divide into syllables using hyphens, '
            '(2) label each syllable O (open) or C (closed), '
            '(3) mark the stressed syllable with an asterisk (*), '
            '(4) note any Qamets Hatuf (write QH in that column, or — if none).'
        )
        rows = [
            ['1', 'אֱלֹהִים', '', '', '', ''],
            ['2', 'בְּרֵאשִׁית', '', '', '', ''],
            ['3', 'הָאָרֶץ', '', '', '', ''],
            ['4', 'שָׁמַיִם', '', '', '', ''],
            ['5', 'יְרוּשָׁלַיִם', '', '', '', ''],
            ['6', 'דָּבָר', '', '', '', ''],
            ['7', 'מֶלֶךְ', '', '', '', ''],
            ['8', 'בְּרִית', '', '', '', ''],
            ['9', 'שָׁבַת', '', '', '', ''],
            ['10', 'נָבִיא', '', '', '', ''],
            ['11', 'אֲדֹנָי', '', '', '', ''],
            ['12', 'יִשְׂרָאֵל', '', '', '', ''],
            ['13', 'כֹּהֵן', '', '', '', ''],
            ['14', 'מִשְׁפָּט', '', '', '', ''],
            ['15', 'תּוֹרָה', '', '', '', ''],
            ['16', 'שָׁלוֹם', '', '', '', ''],
            ['17', 'חֶסֶד', '', '', '', ''],
            ['18', 'קֹדֶשׁ', '', '', '', ''],
            ['19', 'אֶרֶץ', '', '', '', ''],
            ['20', 'עַם', '', '', '', ''],
        ]
        ans = [
            ['1', 'אֱלֹהִים', 'אֱ-לֹ-הִים', 'O-O-C', 'הִים*', '—'],
            ['2', 'בְּרֵאשִׁית', 'בְּ-רֵא-שִׁית', 'O-O-C', 'שִׁית*', '—'],
            ['3', 'הָאָרֶץ', 'הָ-אָ-רֶץ', 'O-O-C', 'רֶץ*', '—'],
            ['4', 'שָׁמַיִם', 'שָׁ-מַ-יִם', 'O-O-C', 'יִם*', '—'],
            ['5', 'יְרוּשָׁלַיִם', 'יְ-רוּ-שָׁ-לַ-יִם', 'O-O-O-O-C', 'יִם*', '—'],
            ['6', 'דָּבָר', 'דָּ-בָר', 'O-O', 'בָר*', '—'],
            ['7', 'מֶלֶךְ', 'מֶ-לֶךְ', 'O-C', 'לֶךְ*', '—'],
            ['8', 'בְּרִית', 'בְּ-רִית', 'O-C', 'רִית*', '—'],
            ['9', 'שָׁבַת', 'שָׁ-בַת', 'O-C', 'בַת*', '—'],
            ['10', 'נָבִיא', 'נָ-בִיא', 'O-O', 'בִיא*', '—'],
            ['11', 'אֲדֹנָי', 'אֲ-דֹ-נָי', 'O-O-O', 'נָי*', '—'],
            ['12', 'יִשְׂרָאֵל', 'יִשׂ-רָ-אֵל', 'C-O-C', 'אֵל*', '—'],
            ['13', 'כֹּהֵן', 'כֹּ-הֵן', 'O-C', 'הֵן*', '—'],
            ['14', 'מִשְׁפָּט', 'מִשׁ-פָּט', 'C-C', 'פָּט*', '—'],
            ['15', 'תּוֹרָה', 'תּוֹ-רָה', 'O-O', 'רָה*', '—'],
            ['16', 'שָׁלוֹם', 'שָׁ-לוֹם', 'O-C', 'לוֹם*', '—'],
            ['17', 'חֶסֶד', 'חֶ-סֶד', 'O-C', 'סֶד*', '—'],
            ['18', 'קֹדֶשׁ', 'קֹ-דֶשׁ', 'O-C', 'דֶשׁ*', '—'],
            ['19', 'אֶרֶץ', 'אֶ-רֶץ', 'O-C', 'רֶץ*', '—'],
            ['20', 'עַם', 'עַם', 'C', 'עַם*', '—'],
        ]
        self.add_generic_table(
            headers=['#', 'Word', 'Syllable Division', 'Types (O/C)', 'Stress', 'Qamets Hatuf?'],
            rows=rows,
            col_ratios=[0.05, 0.12, 0.20, 0.14, 0.10, 0.39],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans,
        )


def build_ch3_syllable_division(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch3', 'exercises',
                               'ch3-syllable-division')
    path = os.path.join(out_dir, 'ch3-syllable-division.pdf')
    ex = Ch3SyllableDivisionExercise(
        title='Chapter 3 — Syllable Division Exercise',
        subtitle='Hebrew Syllables — Open, Closed, Stress, Qamets Hatuf',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch4NounParsingExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form, give: (1) Gender (m./f.), (2) Number (s./pl./du.), '
            '(3) State (abs./cstr.), (4) Lexical Form (dictionary form), (5) Gloss.'
        )
        rows = [
            ['1', 'מֶלֶךְ', '', '', '', '', ''],
            ['2', 'מְלָכִים', '', '', '', '', ''],
            ['3', 'מַלְכֵי', '', '', '', '', ''],
            ['4', 'תּוֹרָה', '', '', '', '', ''],
            ['5', 'תּוֹרוֹת', '', '', '', '', ''],
            ['6', 'דְּבָרִים', '', '', '', '', ''],
            ['7', 'דִּבְרֵי', '', '', '', '', ''],
            ['8', 'בָּנִים', '', '', '', '', ''],
            ['9', 'בָּנוֹת', '', '', '', '', ''],
            ['10', 'אֲנָשִׁים', '', '', '', '', ''],
            ['11', 'נָשִׁים', '', '', '', '', ''],
            ['12', 'יָדַיִם', '', '', '', '', ''],
            ['13', 'עֵינַיִם', '', '', '', '', ''],
            ['14', 'עָרִים', '', '', '', '', ''],
            ['15', 'בָּתִּים', '', '', '', '', ''],
            ['16', 'יָמִים', '', '', '', '', ''],
            ['17', 'נֶפֶשׁ', '', '', '', '', ''],
            ['18', 'נְפָשׁוֹת', '', '', '', '', ''],
            ['19', 'סְפָרִים', '', '', '', '', ''],
            ['20', 'שָׁנָה', '', '', '', '', ''],
            ['21', 'שָׁנָתַיִם', '', '', '', '', ''],
            ['22', 'אֲרָצוֹת', '', '', '', '', ''],
            ['23', 'בְּנֵי', '', '', '', '', ''],
            ['24', 'מַלְכַּת', '', '', '', '', ''],
            ['25', 'שְׁנַת', '', '', '', '', ''],
        ]
        ans = [
            ['1', 'מֶלֶךְ', 'm.', 's.', 'abs.', 'מֶלֶךְ', 'king'],
            ['2', 'מְלָכִים', 'm.', 'pl.', 'abs.', 'מֶלֶךְ', 'kings'],
            ['3', 'מַלְכֵי', 'm.', 'pl.', 'cstr.', 'מֶלֶךְ', 'kings of'],
            ['4', 'תּוֹרָה', 'f.', 's.', 'abs.', 'תּוֹרָה', 'law, instruction'],
            ['5', 'תּוֹרוֹת', 'f.', 'pl.', 'abs./cstr.', 'תּוֹרָה', 'laws'],
            ['6', 'דְּבָרִים', 'm.', 'pl.', 'abs.', 'דָּבָר', 'words, things'],
            ['7', 'דִּבְרֵי', 'm.', 'pl.', 'cstr.', 'דָּבָר', 'words of'],
            ['8', 'בָּנִים', 'm.', 'pl.', 'abs.', 'בֵּן', 'sons'],
            ['9', 'בָּנוֹת', 'f.', 'pl.', 'abs.', 'בַּת', 'daughters'],
            ['10', 'אֲנָשִׁים', 'm.', 'pl.', 'abs.', 'אִישׁ', 'men'],
            ['11', 'נָשִׁים', 'f.', 'pl.', 'abs.', 'אִשָּׁה', 'women'],
            ['12', 'יָדַיִם', 'f.', 'du.', 'abs.', 'יָד', 'two hands'],
            ['13', 'עֵינַיִם', 'f.', 'du.', 'abs.', 'עַיִן', 'two eyes'],
            ['14', 'עָרִים', 'f.', 'pl.', 'abs.', 'עִיר', 'cities'],
            ['15', 'בָּתִּים', 'm.', 'pl.', 'abs.', 'בַּיִת', 'houses'],
            ['16', 'יָמִים', 'm.', 'pl.', 'abs.', 'יוֹם', 'days'],
            ['17', 'נֶפֶשׁ', 'f.', 's.', 'abs.', 'נֶפֶשׁ', 'soul, life'],
            ['18', 'נְפָשׁוֹת', 'f.', 'pl.', 'abs.', 'נֶפֶשׁ', 'souls'],
            ['19', 'סְפָרִים', 'm.', 'pl.', 'abs.', 'סֵפֶר', 'books'],
            ['20', 'שָׁנָה', 'f.', 's.', 'abs.', 'שָׁנָה', 'year'],
            ['21', 'שָׁנָתַיִם', 'f.', 'du.', 'abs.', 'שָׁנָה', 'two years'],
            ['22', 'אֲרָצוֹת', 'f.', 'pl.', 'abs.', 'אֶרֶץ', 'lands, earth'],
            ['23', 'בְּנֵי', 'm.', 'pl.', 'cstr.', 'בֵּן', 'sons of'],
            ['24', 'מַלְכַּת', 'f.', 's.', 'cstr.', 'מַלְכָּה', 'queen of'],
            ['25', 'שְׁנַת', 'f.', 's.', 'cstr.', 'שָׁנָה', 'year of'],
        ]
        self.add_generic_table(
            headers=['#', 'Form', 'Gender', 'Number', 'State', 'Lexical Form', 'Gloss'],
            rows=rows,
            col_ratios=[0.05, 0.13, 0.08, 0.08, 0.08, 0.14, 0.44],
            heb_cols=[1, 5],
            show_answers=True,
            answer_rows=ans,
        )


def build_ch4_noun_parsing(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch4', 'exercises',
                               'ch4-noun-parsing')
    path = os.path.join(out_dir, 'ch4-noun-parsing.pdf')
    ex = Ch4NounParsingExercise(
        title='Chapter 4 — Noun Parsing Drill',
        subtitle='Hebrew Nouns — Gender, Number, State, Lexical Form',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch5ArticleAndVavExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each Hebrew word or phrase: '
            '(1) Article? — Yes/No; '
            '(2) Article Form — if yes, what form? '
            '(3) Conj. ו? — Yes/No; '
            '(4) Conj. Form — if yes, what form? '
            '(5) Translation.'
        )
        hdrs = ['#', 'Hebrew', 'Article?', 'Article Form', 'Conj. ו?', 'Conj. Form', 'Translation']
        cr = [0.05, 0.12, 0.08, 0.16, 0.10, 0.12, 0.37]
        hc = [1]

        self.add_section_heading('Part A — Article Before Normal Consonants (1–8)')
        rows_a = [
            ['1', 'הַמֶּלֶךְ', '', '', '', '', ''],
            ['2', 'הַבַּיִת', '', '', '', '', ''],
            ['3', 'הַיּוֹם', '', '', '', '', ''],
            ['4', 'הַדָּבָר', '', '', '', '', ''],
            ['5', 'הַלַּיְלָה', '', '', '', '', ''],
            ['6', 'הַבֵּן', '', '', '', '', ''],
            ['7', 'הַסֵּפֶר', '', '', '', '', ''],
            ['8', 'הַנָּבִיא', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'הַמֶּלֶךְ', 'Yes', 'הַ + dagesh forte', 'No', '—', 'the king'],
            ['2', 'הַבַּיִת', 'Yes', 'הַ + dagesh forte', 'No', '—', 'the house'],
            ['3', 'הַיּוֹם', 'Yes', 'הַ + dagesh forte', 'No', '—', 'the day'],
            ['4', 'הַדָּבָר', 'Yes', 'הַ + dagesh forte', 'No', '—', 'the word / the thing'],
            ['5', 'הַלַּיְלָה', 'Yes', 'הַ + dagesh forte', 'No', '—', 'the night'],
            ['6', 'הַבֵּן', 'Yes', 'הַ + dagesh forte', 'No', '—', 'the son'],
            ['7', 'הַסֵּפֶר', 'Yes', 'הַ + dagesh forte', 'No', '—', 'the book / the scroll'],
            ['8', 'הַנָּבִיא', 'Yes', 'הַ + dagesh forte', 'No', '—', 'the prophet'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Part B — Article Before Gutturals (9–13)')
        rows_b = [
            ['9', 'הָאִישׁ', '', '', '', '', ''],
            ['10', 'הָאָרֶץ', '', '', '', '', ''],
            ['11', 'הֶעָם', '', '', '', '', ''],
            ['12', 'הָהָר', '', '', '', '', ''],
            ['13', 'הָרוּחַ', '', '', '', '', ''],
        ]
        ans_b = [
            ['9', 'הָאִישׁ', 'Yes', 'הָ (qamets; no dagesh)', 'No', '—', 'the man'],
            ['10', 'הָאָרֶץ', 'Yes', 'הָ (qamets; no dagesh)', 'No', '—', 'the land / the earth'],
            ['11', 'הֶעָם', 'Yes', 'הֶ (segol; no dagesh)', 'No', '—', 'the people'],
            ['12', 'הָהָר', 'Yes', 'הָ (qamets; no dagesh)', 'No', '—', 'the mountain'],
            ['13', 'הָרוּחַ', 'Yes', 'הָ (qamets; no dagesh)', 'No', '—', 'the spirit / the wind'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Part C — Conjunction Only (14–18)')
        rows_c = [
            ['14', 'וְדָבָר', '', '', '', '', ''],
            ['15', 'וּמֶלֶךְ', '', '', '', '', ''],
            ['16', 'וּבֵן', '', '', '', '', ''],
            ['17', 'וְאִישׁ', '', '', '', '', ''],
            ['18', 'וָאֹמַר', '', '', '', '', ''],
        ]
        ans_c = [
            ['14', 'וְדָבָר', 'No', '—', 'Yes', 'וְ (sheva)', 'and a word'],
            ['15', 'וּמֶלֶךְ', 'No', '—', 'Yes', 'וּ (shureq)', 'and a king'],
            ['16', 'וּבֵן', 'No', '—', 'Yes', 'וּ (shureq)', 'and a son'],
            ['17', 'וְאִישׁ', 'No', '—', 'Yes', 'וְ (sheva)', 'and a man'],
            ['18', 'וָאֹמַר', 'No', '—', 'Yes', 'וָ (qamets)', 'and I said / then I said'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Part D — Both Article and Conjunction (19–23)')
        rows_d = [
            ['19', 'וְהַמֶּלֶךְ', '', '', '', '', ''],
            ['20', 'וְהָאָרֶץ', '', '', '', '', ''],
            ['21', 'וְהָאִישׁ', '', '', '', '', ''],
            ['22', 'וְהַיּוֹם', '', '', '', '', ''],
            ['23', 'וְהֶעָם', '', '', '', '', ''],
        ]
        ans_d = [
            ['19', 'וְהַמֶּלֶךְ', 'Yes', 'הַ + dagesh forte', 'Yes', 'וְ (sheva)', 'and the king'],
            ['20', 'וְהָאָרֶץ', 'Yes', 'הָ (qamets; no dagesh)', 'Yes', 'וְ (sheva)', 'and the land / and the earth'],
            ['21', 'וְהָאִישׁ', 'Yes', 'הָ (qamets; no dagesh)', 'Yes', 'וְ (sheva)', 'and the man'],
            ['22', 'וְהַיּוֹם', 'Yes', 'הַ + dagesh forte', 'Yes', 'וְ (sheva)', 'and the day'],
            ['23', 'וְהֶעָם', 'Yes', 'הֶ (segol; no dagesh)', 'Yes', 'וְ (sheva)', 'and the people'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)

        self.add_section_heading('Part E — Neither (24–25)')
        rows_e = [
            ['24', 'מֶלֶךְ', '', '', '', '', ''],
            ['25', 'דָּבָר', '', '', '', '', ''],
        ]
        ans_e = [
            ['24', 'מֶלֶךְ', 'No', '—', 'No', '—', 'a king'],
            ['25', 'דָּבָר', 'No', '—', 'No', '—', 'a word / a thing'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_e, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_e)


def build_ch5_article_and_vav(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch5', 'exercises',
                               'ch5-article-and-vav')
    path = os.path.join(out_dir, 'ch5-article-and-vav.pdf')
    ex = Ch5ArticleAndVavExercise(
        title='Chapter 5 — Definite Article and Conjunction ו',
        subtitle='BBH Chapter 5 · 25 items',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch6PrepositionParsingExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each Hebrew prepositional phrase: '
            '(1) identify the preposition as it appears, '
            '(2) give the base (dictionary) form of the preposition, '
            '(3) describe any vowel change and explain why it occurred, '
            '(4) identify the object noun, '
            '(5) translate the phrase.'
        )
        hdrs = ['#', 'Hebrew', 'Preposition', 'Base Form', 'Change / Reason', 'Object', 'Translation']
        cr = [0.05, 0.12, 0.10, 0.08, 0.22, 0.10, 0.33]
        hc = [1]

        self.add_section_heading('Part A — Inseparable Prepositions: Standard/Sheva Rules (1–8)')
        rows_a = [
            ['1', 'בְּדָבָר', '', '', '', '', ''],
            ['2', 'לְמֶלֶךְ', '', '', '', '', ''],
            ['3', 'כְּאִישׁ', '', '', '', '', ''],
            ['4', 'בִּשְׁמוּאֵל', '', '', '', '', ''],
            ['5', 'לִשְׁלֹמֹה', '', '', '', '', ''],
            ['6', 'בֶּאֱמֶת', '', '', '', '', ''],
            ['7', 'לֵאלֹהִים', '', '', '', '', ''],
            ['8', 'כֶּחָכְמָה', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'בְּדָבָר', 'בְּ', 'בְּ', 'None — default sheva', 'דָּבָר', 'in a word'],
            ['2', 'לְמֶלֶךְ', 'לְ', 'לְ', 'None — default sheva', 'מֶלֶךְ', 'to a king / for a king'],
            ['3', 'כְּאִישׁ', 'כְּ', 'כְּ', 'None — default sheva', 'אִישׁ', 'like a man'],
            ['4', 'בִּשְׁמוּאֵל', 'בִּ', 'בְּ', 'Sheva → hireq: two consecutive shevas', 'שְׁמוּאֵל', 'in/with Samuel'],
            ['5', 'לִשְׁלֹמֹה', 'לִ', 'לְ', 'Sheva → hireq: two consecutive shevas', 'שְׁלֹמֹה', 'to Solomon'],
            ['6', 'בֶּאֱמֶת', 'בֶּ', 'בְּ', 'Composite sheva: אֱ (hateph seghol) → prep takes seghol', 'אֱמֶת', 'in truth'],
            ['7', 'לֵאלֹהִים', 'לֵ', 'לְ', 'Composite sheva matching + lengthening before א to tsere', 'אֱלֹהִים', 'to God'],
            ['8', 'כֶּחָכְמָה', 'כֶּ', 'כְּ', 'Composite sheva matching; prep takes seghol by assimilation', 'חָכְמָה', 'like wisdom'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Part B — Inseparable Prepositions Fused with Article (9–16)')
        rows_b = [
            ['9', 'בַּמֶּלֶךְ', '', '', '', '', ''],
            ['10', 'לַשָּׁמַיִם', '', '', '', '', ''],
            ['11', 'כַּיּוֹם', '', '', '', '', ''],
            ['12', 'בַּבַּיִת', '', '', '', '', ''],
            ['13', 'לָהָר', '', '', '', '', ''],
            ['14', 'בָּאָרֶץ', '', '', '', '', ''],
            ['15', 'לָעָם', '', '', '', '', ''],
            ['16', 'כָּהָאִישׁ', '', '', '', '', ''],
        ]
        ans_b = [
            ['9', 'בַּמֶּלֶךְ', 'בַּ', 'בְּ', 'Article fusion: הַ drops; patach transfers; dagesh forte in מ', 'מֶלֶךְ', 'in the king'],
            ['10', 'לַשָּׁמַיִם', 'לַ', 'לְ', 'Article fusion: הַ drops; patach transfers; dagesh forte in שׁ', 'שָּׁמַיִם', 'to the heavens'],
            ['11', 'כַּיּוֹם', 'כַּ', 'כְּ', 'Article fusion: הַ drops; patach transfers; dagesh forte in י', 'יּוֹם', 'like the day'],
            ['12', 'בַּבַּיִת', 'בַּ', 'בְּ', 'Article fusion: הַ drops; patach transfers; dagesh forte in ב', 'בַּיִת', 'in the house'],
            ['13', 'לָהָר', 'לָ', 'לְ', 'Article fusion (guttural): ה rejects dagesh; patach lengthens → qamets', 'הָר', 'to the mountain'],
            ['14', 'בָּאָרֶץ', 'בָּ', 'בְּ', 'Article fusion (guttural): א rejects dagesh; patach → qamets', 'אָרֶץ', 'in the earth / in the land'],
            ['15', 'לָעָם', 'לָ', 'לְ', 'Article fusion (guttural): ע rejects dagesh; patach → qamets', 'עָם', 'to the people'],
            ['16', 'כָּהָאִישׁ', 'כָּ', 'כְּ', 'Article fusion (guttural): א rejects dagesh; qamets under כָּ', 'אִישׁ', 'like the man'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Part C — מִן: Independent, Prefixed, and Compensatory (17–21)')
        rows_c = [
            ['17', 'מִן הַמֶּלֶךְ', '', '', '', '', ''],
            ['18', 'מִמֶּלֶךְ', '', '', '', '', ''],
            ['19', 'מִיַּד', '', '', '', '', ''],
            ['20', 'מֵהָאָרֶץ', '', '', '', '', ''],
            ['21', 'מֵאֱלֹהִים', '', '', '', '', ''],
        ]
        ans_c = [
            ['17', 'מִן הַמֶּלֶךְ', 'מִן', 'מִן', 'No change — independent before article', 'הַמֶּלֶךְ', 'from the king'],
            ['18', 'מִמֶּלֶךְ', 'מִ', 'מִן', 'Nun assimilates; dagesh forte in מ', 'מֶלֶךְ', 'from a king'],
            ['19', 'מִיַּד', 'מִ', 'מִן', 'Nun assimilates; dagesh forte in י', 'יָד', 'from the hand'],
            ['20', 'מֵהָאָרֶץ', 'מֵ', 'מִן', 'Compensatory: ה (guttural) rejects dagesh; hireq → tsere', 'הָאָרֶץ', 'from the earth'],
            ['21', 'מֵאֱלֹהִים', 'מֵ', 'מִן', 'Compensatory: א (guttural) rejects dagesh; hireq → tsere', 'אֱלֹהִים', 'from God'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Part D — Independent Prepositions (22–25)')
        rows_d = [
            ['22', 'אֶל הָעִיר', '', '', '', '', ''],
            ['23', 'עַל הַשָּׁמַיִם', '', '', '', '', ''],
            ['24', 'עִם הָעַם', '', '', '', '', ''],
            ['25', 'אֵת הַמֶּלֶךְ', '', '', '', '', ''],
        ]
        ans_d = [
            ['22', 'אֶל הָעִיר', 'אֶל', 'אֶל', 'None — independent preposition', 'הָעִיר', 'to the city'],
            ['23', 'עַל הַשָּׁמַיִם', 'עַל', 'עַל', 'None — independent preposition', 'הַשָּׁמַיִם', 'upon the heavens'],
            ['24', 'עִם הָעַם', 'עִם', 'עִם', 'None — independent preposition', 'הָעַם', 'with the people'],
            ['25', 'אֵת הַמֶּלֶךְ', 'אֵת (DOM)', 'אֵת', 'None — direct object marker', 'הַמֶּלֶךְ', '[marks the king as definite direct object]'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)


def build_ch6_preposition_parsing(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch6', 'exercises',
                               'ch6-preposition-parsing')
    path = os.path.join(out_dir, 'ch6-preposition-parsing.pdf')
    ex = Ch6PrepositionParsingExercise(
        title='Chapter 6 — Preposition Parsing Drill',
        subtitle='Hebrew Prepositions — Inseparable, Article Fusion, מִן, Independent',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Ch7–Ch12 builders
# ---------------------------------------------------------------------------

class Ch7AdjectiveUsageExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each Hebrew phrase: '
            '(1) Use — Identify: Attributive (Def./Indef.) / Predicate / Substantival / Comparative / Superlative; '
            '(2) Adjective — give the adjective form shown; '
            '(3) Agreement — gender and number (ms/fs/mp/fp) and note whether it agrees; '
            '(4) Translation.'
        )
        hdrs = ['#', 'Hebrew', 'Use', 'Adjective', 'Agreement', 'Translation']
        cr = [0.05, 0.17, 0.15, 0.15, 0.22, 0.26]
        hc = [1, 3]

        self.add_section_heading('Part A — Attributive Adjectives (Definite) (1–5)')
        rows_a = [
            ['1', 'הַמֶּלֶךְ הַגָּדוֹל', '', '', '', ''],
            ['2', 'הָאִשָּׁה הַטּוֹבָה', '', '', '', ''],
            ['3', 'הָעִיר הַגְּדוֹלָה', '', '', '', ''],
            ['4', 'הָאֲנָשִׁים הַגִּבּוֹרִים', '', '', '', ''],
            ['5', 'הַדְּבָרִים הַטּוֹבִים', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'הַמֶּלֶךְ הַגָּדוֹל', 'Attributive (def.)', 'הַגָּדוֹל', 'ms; agrees with מֶלֶךְ (ms)', 'the great king'],
            ['2', 'הָאִשָּׁה הַטּוֹבָה', 'Attributive (def.)', 'הַטּוֹבָה', 'fs; agrees with אִשָּׁה (fs)', 'the good woman'],
            ['3', 'הָעִיר הַגְּדוֹלָה', 'Attributive (def.)', 'הַגְּדוֹלָה', 'fs; agrees with עִיר (fs)', 'the great city'],
            ['4', 'הָאֲנָשִׁים הַגִּבּוֹרִים', 'Attributive (def.)', 'הַגִּבּוֹרִים', 'mp; agrees with אֲנָשִׁים (mp)', 'the mighty men'],
            ['5', 'הַדְּבָרִים הַטּוֹבִים', 'Attributive (def.)', 'הַטּוֹבִים', 'mp; agrees with דְּבָרִים (mp)', 'the good words/things'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Part B — Attributive Adjectives (Indefinite) (6–10)')
        rows_b = [
            ['6', 'מֶלֶךְ גָּדוֹל', '', '', '', ''],
            ['7', 'אִשָּׁה טוֹבָה', '', '', '', ''],
            ['8', 'אֶרֶץ גְּדוֹלָה', '', '', '', ''],
            ['9', 'עַם קָדוֹשׁ', '', '', '', ''],
            ['10', 'דָּבָר חָדָשׁ', '', '', '', ''],
        ]
        ans_b = [
            ['6', 'מֶלֶךְ גָּדוֹל', 'Attributive (indef.)', 'גָּדוֹל', 'ms; agrees with מֶלֶךְ (ms)', 'a great king'],
            ['7', 'אִשָּׁה טוֹבָה', 'Attributive (indef.)', 'טוֹבָה', 'fs; agrees with אִשָּׁה (fs)', 'a good woman'],
            ['8', 'אֶרֶץ גְּדוֹלָה', 'Attributive (indef.)', 'גְּדוֹלָה', 'fs; agrees with אֶרֶץ (fs)', 'a great land'],
            ['9', 'עַם קָדוֹשׁ', 'Attributive (indef.)', 'קָדוֹשׁ', 'ms; agrees with עַם (ms)', 'a holy people'],
            ['10', 'דָּבָר חָדָשׁ', 'Attributive (indef.)', 'חָדָשׁ', 'ms; agrees with דָּבָר (ms)', 'a new word/thing'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Part C — Predicate Adjectives (11–18)')
        rows_c = [
            ['11', 'הַמֶּלֶךְ גָּדוֹל', '', '', '', ''],
            ['12', 'גָּדוֹל הַמֶּלֶךְ', '', '', '', ''],
            ['13', 'הָאִשָּׁה טוֹבָה', '', '', '', ''],
            ['14', 'טוֹב הַדָּבָר', '', '', '', ''],
            ['15', 'הָאָרֶץ טוֹבָה', '', '', '', ''],
            ['16', 'הַגִּבּוֹרִים חֲזָקִים', '', '', '', ''],
            ['17', 'יָשָׁר הַדֶּרֶךְ', '', '', '', ''],
            ['18', 'כָּבֵד הַדָּבָר', '', '', '', ''],
        ]
        ans_c = [
            ['11', 'הַמֶּלֶךְ גָּדוֹל', 'Predicate', 'גָּדוֹל', 'ms; agrees with מֶלֶךְ; no article', 'The king is great'],
            ['12', 'גָּדוֹל הַמֶּלֶךְ', 'Predicate', 'גָּדוֹל', 'ms; adj-first word order; no article', 'The king is great'],
            ['13', 'הָאִשָּׁה טוֹבָה', 'Predicate', 'טוֹבָה', 'fs; agrees with אִשָּׁה; no article', 'The woman is good'],
            ['14', 'טוֹב הַדָּבָר', 'Predicate', 'טוֹב', 'ms; adj-first; no article', 'The word/matter is good'],
            ['15', 'הָאָרֶץ טוֹבָה', 'Predicate', 'טוֹבָה', 'fs; agrees with אֶרֶץ; no article', 'The land is good'],
            ['16', 'הַגִּבּוֹרִים חֲזָקִים', 'Predicate', 'חֲזָקִים', 'mp; agrees with גִּבּוֹרִים; no article', 'The warriors are strong'],
            ['17', 'יָשָׁר הַדֶּרֶךְ', 'Predicate', 'יָשָׁר', 'ms; adj-first; no article', 'The way is straight/upright'],
            ['18', 'כָּבֵד הַדָּבָר', 'Predicate', 'כָּבֵד', 'ms; adj-first (stative pattern); no article', 'The matter is heavy/serious'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Part D — Substantival Adjectives (19–22)')
        rows_d = [
            ['19', 'הַטּוֹב', '', '', '', ''],
            ['20', 'הָרָע', '', '', '', ''],
            ['21', 'הַקְּדֹשִׁים', '', '', '', ''],
            ['22', 'רַבִּים', '', '', '', ''],
        ]
        ans_d = [
            ['19', 'הַטּוֹב', 'Substantival', 'הַטּוֹב', 'ms with article', 'the good (one/thing)'],
            ['20', 'הָרָע', 'Substantival', 'הָרָע', 'ms with article', 'the evil (one/thing)'],
            ['21', 'הַקְּדֹשִׁים', 'Substantival', 'הַקְּדֹשִׁים', 'mp with article', 'the holy ones; the saints'],
            ['22', 'רַבִּים', 'Substantival', 'רַבִּים', 'mp without article', 'many (people); a multitude'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)

        self.add_section_heading('Part E — Comparative and Superlative (23–25)')
        rows_e = [
            ['23', 'טוֹב מִדְּבַשׁ', '', '', '', ''],
            ['24', 'הַקָּטֹן', '', '', '', ''],
            ['25', 'עָרוּם מִכֹּל חַיַּת הַשָּׂדֶה', '', '', '', ''],
        ]
        ans_e = [
            ['23', 'טוֹב מִדְּבַשׁ', 'Comparative', 'טוֹב', 'ms; compared via מִן', 'better than honey'],
            ['24', 'הַקָּטֹן', 'Superlative', 'הַקָּטֹן', 'ms with article; no head noun', 'the youngest; the smallest'],
            ['25', 'עָרוּם מִכֹּל חַיַּת הַשָּׂדֶה', 'Comparative (superlative in context)', 'עָרוּם', 'ms; compared via מִכֹּל', 'more crafty than any beast of the field'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_e, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_e)


def build_ch7_adjective_usage(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch7', 'exercises',
                               'ch7-adjective-usage')
    path = os.path.join(out_dir, 'ch7-adjective-usage.pdf')
    ex = Ch7AdjectiveUsageExercise(
        title='Chapter 7 — Adjective Usage Drill',
        subtitle='Hebrew Adjectives — Attributive, Predicate, and Substantival Uses',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch8PronounIdentificationExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each item: (1) Identify the pronoun type '
            '(Personal / Demonstrative / Relative / Interrogative), '
            '(2) Isolate the pronoun, '
            '(3) Parse it — give Person, Gender, Number (PGN) where applicable; '
            'for Relative and Interrogative write "indecl.", '
            '(4) Translate the full phrase.'
        )
        rows = [
            ['1', 'אֲנִי יְהוָה אֱלֹהֵיכֶם', '', '', '', ''],
            ['2', 'אַתָּה עַבְדִּי', '', '', '', ''],
            ['3', 'הוּא הַכֹּהֵן', '', '', '', ''],
            ['4', 'הִיא הַמַּלְכָּה', '', '', '', ''],
            ['5', 'אֲנַחְנוּ עֲבָדֶיךָ', '', '', '', ''],
            ['6', 'אַתֶּם עֵדַי', '', '', '', ''],
            ['7', 'אָנֹכִי הָאִישׁ', '', '', '', ''],
            ['8', 'הֵם הַכֹּהֲנִים', '', '', '', ''],
            ['9', 'הָאִישׁ הַזֶּה', '', '', '', ''],
            ['10', 'הָאִשָּׁה הַזֹּאת', '', '', '', ''],
            ['11', 'הַדְּבָרִים הָאֵלֶּה', '', '', '', ''],
            ['12', 'זֶה הָאִישׁ', '', '', '', ''],
            ['13', 'זֹאת הָאָרֶץ', '', '', '', ''],
            ['14', 'בַּיּוֹם הַהוּא', '', '', '', ''],
            ['15', 'בָּעֵת הַהִיא', '', '', '', ''],
            ['16', 'הָאִישׁ אֲשֶׁר בָּא', '', '', '', ''],
            ['17', 'הָאִשָּׁה אֲשֶׁר רָאִיתִי', '', '', '', ''],
            ['18', 'הָאָרֶץ אֲשֶׁר נָתַן יְהוָה לָנוּ', '', '', '', ''],
            ['19', 'הָאִישׁ אֲשֶׁר עָבַד אֶת יְהוָה', '', '', '', ''],
            ['20', 'הַמִּצְוָה אֲשֶׁר צִוִּיתִיךָ', '', '', '', ''],
            ['21', 'הַדָּבָר אֲשֶׁר שָׁמַעְתָּ', '', '', '', ''],
            ['22', 'מִי אַתָּה', '', '', '', ''],
            ['23', 'מַה זֶּה', '', '', '', ''],
            ['24', 'מִי הָאִישׁ הַזֶּה', '', '', '', ''],
            ['25', 'מַה עָשִׂיתָ', '', '', '', ''],
        ]
        ans = [
            ['1', 'אֲנִי יְהוָה אֱלֹהֵיכֶם', 'Personal', 'אֲנִי', '1cs', 'I am the LORD your God'],
            ['2', 'אַתָּה עַבְדִּי', 'Personal', 'אַתָּה', '2ms', 'You are my servant'],
            ['3', 'הוּא הַכֹּהֵן', 'Personal', 'הוּא', '3ms', 'He is the priest'],
            ['4', 'הִיא הַמַּלְכָּה', 'Personal', 'הִיא', '3fs', 'She is the queen'],
            ['5', 'אֲנַחְנוּ עֲבָדֶיךָ', 'Personal', 'אֲנַחְנוּ', '1cp', 'We are your servants'],
            ['6', 'אַתֶּם עֵדַי', 'Personal', 'אַתֶּם', '2mp', 'You are my witnesses'],
            ['7', 'אָנֹכִי הָאִישׁ', 'Personal', 'אָנֹכִי', '1cs', 'I am the man'],
            ['8', 'הֵם הַכֹּהֲנִים', 'Personal', 'הֵם', '3mp', 'They are the priests'],
            ['9', 'הָאִישׁ הַזֶּה', 'Demonstrative', 'הַזֶּה', 'ms (near)', 'this man'],
            ['10', 'הָאִשָּׁה הַזֹּאת', 'Demonstrative', 'הַזֹּאת', 'fs (near)', 'this woman'],
            ['11', 'הַדְּבָרִים הָאֵלֶּה', 'Demonstrative', 'הָאֵלֶּה', 'cp (near)', 'these words/things'],
            ['12', 'זֶה הָאִישׁ', 'Demonstrative', 'זֶה', 'ms (near)', 'This is the man'],
            ['13', 'זֹאת הָאָרֶץ', 'Demonstrative', 'זֹאת', 'fs (near)', 'This is the land'],
            ['14', 'בַּיּוֹם הַהוּא', 'Demonstrative', 'הַהוּא', 'ms (far)', 'on that day'],
            ['15', 'בָּעֵת הַהִיא', 'Demonstrative', 'הַהִיא', 'fs (far)', 'at that time'],
            ['16', 'הָאִישׁ אֲשֶׁר בָּא', 'Relative', 'אֲשֶׁר', 'indecl.', 'the man who came'],
            ['17', 'הָאִשָּׁה אֲשֶׁר רָאִיתִי', 'Relative', 'אֲשֶׁר', 'indecl.', 'the woman whom I saw'],
            ['18', 'הָאָרֶץ אֲשֶׁר נָתַן יְהוָה לָנוּ', 'Relative', 'אֲשֶׁר', 'indecl.', 'the land that the LORD gave to us'],
            ['19', 'הָאִישׁ אֲשֶׁר עָבַד אֶת יְהוָה', 'Relative', 'אֲשֶׁר', 'indecl.', 'the man who served the LORD'],
            ['20', 'הַמִּצְוָה אֲשֶׁר צִוִּיתִיךָ', 'Relative', 'אֲשֶׁר', 'indecl.', 'the commandment that I commanded you'],
            ['21', 'הַדָּבָר אֲשֶׁר שָׁמַעְתָּ', 'Relative', 'אֲשֶׁר', 'indecl.', 'the word/thing that you heard'],
            ['22', 'מִי אַתָּה', 'Interrogative', 'מִי', 'indecl.', 'Who are you?'],
            ['23', 'מַה זֶּה', 'Interrogative', 'מַה', 'indecl.', 'What is this?'],
            ['24', 'מִי הָאִישׁ הַזֶּה', 'Interrogative', 'מִי', 'indecl.', 'Who is this man?'],
            ['25', 'מַה עָשִׂיתָ', 'Interrogative', 'מַה', 'indecl.', 'What have you done?'],
        ]
        self.add_generic_table(
            headers=['#', 'Hebrew', 'Pronoun Type', 'Pronoun', 'Parse (PGN)', 'Translation'],
            rows=rows,
            col_ratios=[0.05, 0.22, 0.14, 0.12, 0.10, 0.37],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans,
        )


def build_ch8_pronoun_identification(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch8', 'exercises',
                               'ch8-pronoun-identification')
    path = os.path.join(out_dir, 'ch8-pronoun-identification.pdf')
    ex = Ch8PronounIdentificationExercise(
        title='Chapter 8 — Pronoun Identification Drill',
        subtitle='Personal, Demonstrative, Relative, and Interrogative Pronouns',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch9SuffixParsingExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each Hebrew form below: '
            '(1) Base Word — identify the underlying noun, preposition, or particle; '
            '(2) Suffix — write the suffix element only; '
            '(3) Parse (PGN) — Person-Gender-Number of the suffix; '
            '(4) Translation — full translation of the suffixed form.'
        )
        rows = [
            ['1', 'סוּסוֹ', '', '', '', ''],
            ['2', 'דְּבָרִי', '', '', '', ''],
            ['3', 'מַלְכְּכֶם', '', '', '', ''],
            ['4', 'אָחִיהָ', '', '', '', ''],
            ['5', 'בֵּיתְךָ', '', '', '', ''],
            ['6', 'עַמֵּנוּ', '', '', '', ''],
            ['7', 'אֲדֹנֵיכֶם', '', '', '', ''],
            ['8', 'בְּנָהּ', '', '', '', ''],
            ['9', 'שְׁמֵיהֶם', '', '', '', ''],
            ['10', 'אַרְצָם', '', '', '', ''],
            ['11', 'לִי', '', '', '', ''],
            ['12', 'לְךָ', '', '', '', ''],
            ['13', 'לָהּ', '', '', '', ''],
            ['14', 'לָנוּ', '', '', '', ''],
            ['15', 'לָכֶם', '', '', '', ''],
            ['16', 'בָּהּ', '', '', '', ''],
            ['17', 'בָּם', '', '', '', ''],
            ['18', 'עִמִּי', '', '', '', ''],
            ['19', 'אֵלֶיךָ', '', '', '', ''],
            ['20', 'עָלָיו', '', '', '', ''],
            ['21', 'אֹתִי', '', '', '', ''],
            ['22', 'אֹתוֹ', '', '', '', ''],
            ['23', 'אֹתָהּ', '', '', '', ''],
            ['24', 'אֹתָנוּ', '', '', '', ''],
            ['25', 'אֹתָם', '', '', '', ''],
        ]
        ans = [
            ['1', 'סוּסוֹ', 'סוּס (horse)', 'וֹ', '3ms', 'his horse'],
            ['2', 'דְּבָרִי', 'דָּבָר (word)', 'ִי', '1cs', 'my word'],
            ['3', 'מַלְכְּכֶם', 'מֶלֶךְ (king)', 'כֶם', '2mp', 'your (mp) king'],
            ['4', 'אָחִיהָ', 'אָח (brother)', 'הָ', '3fs', 'her brother'],
            ['5', 'בֵּיתְךָ', 'בַּיִת (house)', 'ְךָ', '2ms', 'your (ms) house'],
            ['6', 'עַמֵּנוּ', 'עַם (people)', 'ֵנוּ', '1cp', 'our people'],
            ['7', 'אֲדֹנֵיכֶם', 'אָדוֹן (lord/master)', 'ֵיכֶם', '2mp', 'your (mp) lord/masters'],
            ['8', 'בְּנָהּ', 'בֵּן (son)', 'הָ', '3fs', 'her son'],
            ['9', 'שְׁמֵיהֶם', 'שָׁמַיִם (heavens)', 'ֵיהֶם', '3mp', 'their (m) heavens'],
            ['10', 'אַרְצָם', 'אֶרֶץ (land/earth)', 'ָם', '3mp', 'their (m) land'],
            ['11', 'לִי', 'לְ (to/for)', 'ִי', '1cs', 'to/for me'],
            ['12', 'לְךָ', 'לְ (to/for)', 'ְךָ', '2ms', 'to/for you (ms)'],
            ['13', 'לָהּ', 'לְ (to/for)', 'הָ', '3fs', 'to/for her'],
            ['14', 'לָנוּ', 'לְ (to/for)', 'ֵנוּ', '1cp', 'to/for us'],
            ['15', 'לָכֶם', 'לְ (to/for)', 'כֶם', '2mp', 'to/for you (mp)'],
            ['16', 'בָּהּ', 'בְּ (in/with)', 'הָ', '3fs', 'in/with her'],
            ['17', 'בָּם', 'בְּ (in/with)', 'ָם', '3mp', 'in/with them (m)'],
            ['18', 'עִמִּי', 'עִם (with)', 'ִי', '1cs', 'with me'],
            ['19', 'אֵלֶיךָ', 'אֶל (to/toward)', 'ְךָ', '2ms', 'to/toward you (ms)'],
            ['20', 'עָלָיו', 'עַל (upon/over)', 'ָיו', '3ms', 'upon/over him'],
            ['21', 'אֹתִי', 'אֵת (DOM)', 'ִי', '1cs', 'me (direct object)'],
            ['22', 'אֹתוֹ', 'אֵת (DOM)', 'וֹ', '3ms', 'him (direct object)'],
            ['23', 'אֹתָהּ', 'אֵת (DOM)', 'הָ', '3fs', 'her (direct object)'],
            ['24', 'אֹתָנוּ', 'אֵת (DOM)', 'ֵנוּ', '1cp', 'us (direct object)'],
            ['25', 'אֹתָם', 'אֵת (DOM)', 'ָם', '3mp', 'them (m, direct object)'],
        ]
        self.add_generic_table(
            headers=['#', 'Hebrew', 'Base Word', 'Suffix', 'Parse (PGN)', 'Translation'],
            rows=rows,
            col_ratios=[0.05, 0.12, 0.18, 0.10, 0.10, 0.45],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans,
        )


def build_ch9_suffix_parsing(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch9', 'exercises',
                               'ch9-suffix-parsing')
    path = os.path.join(out_dir, 'ch9-suffix-parsing.pdf')
    ex = Ch9SuffixParsingExercise(
        title='Chapter 9 — Hebrew Pronominal Suffix Parsing Drill',
        subtitle='Pronominal Suffixes on Nouns, Prepositions, and the DOM',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch10ConstructChainExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each item: (1) identify the construct noun (nomen regens) and its form type, '
            '(2) identify the absolute noun (nomen rectum), '
            '(3) state whether the chain is definite or indefinite, '
            '(4) translate into natural English.'
        )
        hdrs = ['#', 'Hebrew', 'Construct Noun', 'Absolute Noun', 'Definite?', 'Translation']
        cr = [0.05, 0.20, 0.22, 0.18, 0.08, 0.27]
        hc = [1]

        self.add_section_heading('Part A — Simple 2-Link Chains (Indefinite) (1–8)')
        rows_a = [
            ['1', 'דְּבַר מֶלֶךְ', '', '', '', ''],
            ['2', 'בֵּית אִישׁ', '', '', '', ''],
            ['3', 'כְּבוֹד עָם', '', '', '', ''],
            ['4', 'עֶבֶד מֶלֶךְ', '', '', '', ''],
            ['5', 'בְּנֵי אָדָם', '', '', '', ''],
            ['6', 'סֵפֶר תּוֹרָה', '', '', '', ''],
            ['7', 'כֹּהֵן אֱלֹהִים', '', '', '', ''],
            ['8', 'רוּחַ אָדָם', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'דְּבַר מֶלֶךְ', 'דְּבַר (ms cstr of דָּבָר)', 'מֶלֶךְ', 'No', 'a word of a king'],
            ['2', 'בֵּית אִישׁ', 'בֵּית (ms cstr of בַּיִת)', 'אִישׁ', 'No', "a man's house"],
            ['3', 'כְּבוֹד עָם', 'כְּבוֹד (ms cstr of כָּבוֹד)', 'עָם', 'No', 'glory of a people'],
            ['4', 'עֶבֶד מֶלֶךְ', 'עֶבֶד (ms cstr; segolate, unchanged)', 'מֶלֶךְ', 'No', 'a servant of a king'],
            ['5', 'בְּנֵי אָדָם', 'בְּנֵי (mp cstr of בֵּן; ִים → ֵי)', 'אָדָם', 'No', 'sons of man / humankind'],
            ['6', 'סֵפֶר תּוֹרָה', 'סֵפֶר (ms cstr; segolate, unchanged)', 'תּוֹרָה', 'No', 'a book of the law'],
            ['7', 'כֹּהֵן אֱלֹהִים', 'כֹּהֵן (ms cstr; unchanged)', 'אֱלֹהִים', 'No', 'a priest of God'],
            ['8', 'רוּחַ אָדָם', 'רוּחַ (fs cstr of רוּחַ; unchanged)', 'אָדָם', 'No', 'the spirit of man'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Part B — Simple 2-Link Chains (Definite) (9–16)')
        rows_b = [
            ['9', 'דְּבַר יְהוָה', '', '', '', ''],
            ['10', 'בֵּית יְהוָה', '', '', '', ''],
            ['11', 'כְּבוֹד יְהוָה', '', '', '', ''],
            ['12', 'שֵׁם יְהוָה', '', '', '', ''],
            ['13', 'בֵּית הַמֶּלֶךְ', '', '', '', ''],
            ['14', 'מֶלֶךְ יִשְׂרָאֵל', '', '', '', ''],
            ['15', 'עִיר דָּוִד', '', '', '', ''],
            ['16', 'בְּנֵי יִשְׂרָאֵל', '', '', '', ''],
        ]
        ans_b = [
            ['9', 'דְּבַר יְהוָה', 'דְּבַר (ms cstr; propretonic reduction)', 'יְהוָה (proper)', 'Yes', 'the word of the LORD'],
            ['10', 'בֵּית יְהוָה', 'בֵּית (ms cstr of בַּיִת)', 'יְהוָה (proper)', 'Yes', 'the house of the LORD'],
            ['11', 'כְּבוֹד יְהוָה', 'כְּבוֹד (ms cstr of כָּבוֹד)', 'יְהוָה (proper)', 'Yes', 'the glory of the LORD'],
            ['12', 'שֵׁם יְהוָה', 'שֵׁם (ms cstr; unchanged)', 'יְהוָה (proper)', 'Yes', 'the name of the LORD'],
            ['13', 'בֵּית הַמֶּלֶךְ', 'בֵּית (ms cstr)', 'הַמֶּלֶךְ (definite art.)', 'Yes', "the king's house"],
            ['14', 'מֶלֶךְ יִשְׂרָאֵל', 'מֶלֶךְ (ms cstr; segolate, unchanged)', 'יִשְׂרָאֵל (proper)', 'Yes', 'the king of Israel'],
            ['15', 'עִיר דָּוִד', 'עִיר (fs cstr; unchanged)', 'דָּוִד (proper)', 'Yes', 'the city of David'],
            ['16', 'בְּנֵי יִשְׂרָאֵל', 'בְּנֵי (mp cstr; ִים → ֵי)', 'יִשְׂרָאֵל (proper)', 'Yes', 'the sons/children of Israel'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Part C — Extended 3-Link Chains (17–21)')
        rows_c = [
            ['17', 'דְּבַר תּוֹרַת יְהוָה', '', '', '', ''],
            ['18', 'בֵּית אֱלֹהֵי יִשְׂרָאֵל', '', '', '', ''],
            ['19', 'מֶלֶךְ מַלְכֵי הַמְּלָכִים', '', '', '', ''],
            ['20', 'שֵׁם יְהוָה אֱלֹהֵינוּ', '', '', '', ''],
            ['21', 'עֶבֶד עַבְדֵי הַמֶּלֶךְ', '', '', '', ''],
        ]
        ans_c = [
            ['17', 'דְּבַר תּוֹרַת יְהוָה', 'דְּבַר, תּוֹרַת (both construct)', 'יְהוָה (proper)', 'Yes', 'the word of the law of the LORD'],
            ['18', 'בֵּית אֱלֹהֵי יִשְׂרָאֵל', 'בֵּית, אֱלֹהֵי (both construct)', 'יִשְׂרָאֵל (proper)', 'Yes', 'the house of the God of Israel'],
            ['19', 'מֶלֶךְ מַלְכֵי הַמְּלָכִים', 'מֶלֶךְ, מַלְכֵי (both construct)', 'הַמְּלָכִים (def. art.)', 'Yes', 'the king of kings of the kings'],
            ['20', 'שֵׁם יְהוָה אֱלֹהֵינוּ', 'שֵׁם (construct)', 'יְהוָה אֱלֹהֵינוּ (proper + appositive)', 'Yes', 'the name of the LORD our God'],
            ['21', 'עֶבֶד עַבְדֵי הַמֶּלֶךְ', 'עֶבֶד, עַבְדֵי (both construct)', 'הַמֶּלֶךְ (def. art.)', 'Yes', 'servant of the servants of the king'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Part D — Feminine Construct Nouns (22–25)')
        rows_d = [
            ['22', 'תּוֹרַת מֹשֶׁה', '', '', '', ''],
            ['23', 'תּוֹרַת יְהוָה', '', '', '', ''],
            ['24', 'מַלְכַּת שְׁבָא', '', '', '', ''],
            ['25', 'בִּרְכַּת יְהוָה', '', '', '', ''],
        ]
        ans_d = [
            ['22', 'תּוֹרַת מֹשֶׁה', 'תּוֹרַת (fs cstr; תּוֹרָה → תּוֹרַת)', 'מֹשֶׁה (proper)', 'Yes', 'the law/Torah of Moses'],
            ['23', 'תּוֹרַת יְהוָה', 'תּוֹרַת (fs cstr)', 'יְהוָה (proper)', 'Yes', 'the law/Torah of the LORD'],
            ['24', 'מַלְכַּת שְׁבָא', 'מַלְכַּת (fs cstr; מַלְכָּה → מַלְכַּת)', 'שְׁבָא (proper)', 'Yes', 'the queen of Sheba'],
            ['25', 'בִּרְכַּת יְהוָה', 'בִּרְכַּת (fs cstr; בְּרָכָה → בִּרְכַּת)', 'יְהוָה (proper)', 'Yes', 'the blessing of the LORD'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)


def build_ch10_construct_chain(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch10', 'exercises',
                               'ch10-construct-chain')
    path = os.path.join(out_dir, 'ch10-construct-chain.pdf')
    ex = Ch10ConstructChainExercise(
        title='Chapter 10 — Construct Chain Drill',
        subtitle='BBH Chapter 10 — Hebrew Construct Chain',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch11NumberIdentificationExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each Hebrew number-noun phrase: '
            '(1) identify the number word, '
            '(2) give its numeric value, '
            '(3) note the gender polarity situation (if applicable), '
            '(4) provide a translation.\n'
            'Gender Polarity: write "Yes — [noun gender] noun + [form used]" where polarity applies; '
            '"N/A (tens)" for multiples of ten; "N/A (1–2)" for ones and twos; '
            '"N/A (ordinal)" for ordinals.'
        )
        rows = [
            ['1', 'שִׁבְעָה יָמִים', '', '', '', ''],
            ['2', 'שָׁלֹשׁ נָשִׁים', '', '', '', ''],
            ['3', 'אַרְבָּעִים שָׁנָה', '', '', '', ''],
            ['4', 'שְׁנֵי אֲנָשִׁים', '', '', '', ''],
            ['5', 'עֶשֶׂר עָרִים', '', '', '', ''],
            ['6', 'חֲמִשָּׁה שְׁבָטִים', '', '', '', ''],
            ['7', 'שְׁתַּיִם עֶשְׂרֵה שָׁנָה', '', '', '', ''],
            ['8', 'שִׁשָּׁה בָּנִים', '', '', '', ''],
            ['9', 'שְׁלֹשִׁים אִישׁ', '', '', '', ''],
            ['10', 'תִּשְׁעָה אֲנָשִׁים', '', '', '', ''],
            ['11', 'שְׁנֵים עָשָׂר שֵׁבֶט', '', '', '', ''],
            ['12', 'אַרְבַּע בָּנוֹת', '', '', '', ''],
            ['13', 'חֲמִשָּׁה עָשָׂר אִישׁ', '', '', '', ''],
            ['14', 'שִׁבְעִים זָקֵן', '', '', '', ''],
            ['15', 'שֵׁשׁ שָׁנִים', '', '', '', ''],
            ['16', 'שְׁלֹשׁ עֶשְׂרֵה עִיר', '', '', '', ''],
            ['17', 'בַּיּוֹם הַשְּׁבִיעִי', '', '', '', ''],
            ['18', 'בַּחֹדֶשׁ הָרִאשׁוֹן', '', '', '', ''],
            ['19', 'הַשַּׁעַר הַשֵּׁנִי', '', '', '', ''],
            ['20', 'הַיּוֹם הָעֲשִׂירִי', '', '', '', ''],
        ]
        ans = [
            ['1', 'שִׁבְעָה יָמִים', 'שִׁבְעָה', '7', 'Yes — masc. noun + ה-form', 'seven days'],
            ['2', 'שָׁלֹשׁ נָשִׁים', 'שָׁלֹשׁ', '3', 'Yes — fem. noun + non-ה-form', 'three women'],
            ['3', 'אַרְבָּעִים שָׁנָה', 'אַרְבָּעִים', '40', 'N/A (tens — no polarity)', 'forty years'],
            ['4', 'שְׁנֵי אֲנָשִׁים', 'שְׁנֵי', '2', 'N/A (1–2 agree normally)', 'two men'],
            ['5', 'עֶשֶׂר עָרִים', 'עֶשֶׂר', '10', 'Yes — fem. noun + non-ה-form', 'ten cities'],
            ['6', 'חֲמִשָּׁה שְׁבָטִים', 'חֲמִשָּׁה', '5', 'Yes — masc. noun + ה-form', 'five tribes'],
            ['7', 'שְׁתַּיִם עֶשְׂרֵה שָׁנָה', 'שְׁתַּיִם עֶשְׂרֵה', '12', 'N/A (teens — 12 uses dual form)', 'twelve years'],
            ['8', 'שִׁשָּׁה בָּנִים', 'שִׁשָּׁה', '6', 'Yes — masc. noun + ה-form', 'six sons'],
            ['9', 'שְׁלֹשִׁים אִישׁ', 'שְׁלֹשִׁים', '30', 'N/A (tens — invariable)', 'thirty men'],
            ['10', 'תִּשְׁעָה אֲנָשִׁים', 'תִּשְׁעָה', '9', 'Yes — masc. noun + ה-form', 'nine men'],
            ['11', 'שְׁנֵים עָשָׂר שֵׁבֶט', 'שְׁנֵים עָשָׂר', '12', 'N/A (teens with masc. noun)', 'twelve tribes'],
            ['12', 'אַרְבַּע בָּנוֹת', 'אַרְבַּע', '4', 'Yes — fem. noun + non-ה-form', 'four daughters'],
            ['13', 'חֲמִשָּׁה עָשָׂר אִישׁ', 'חֲמִשָּׁה עָשָׂר', '15', 'Yes (unit) — masc. noun + ה-form unit', 'fifteen men'],
            ['14', 'שִׁבְעִים זָקֵן', 'שִׁבְעִים', '70', 'N/A (tens — invariable)', 'seventy elders'],
            ['15', 'שֵׁשׁ שָׁנִים', 'שֵׁשׁ', '6', 'Yes — fem. noun + non-ה-form', 'six years'],
            ['16', 'שְׁלֹשׁ עֶשְׂרֵה עִיר', 'שְׁלֹשׁ עֶשְׂרֵה', '13', 'Yes (unit) — fem. noun + non-ה-form unit', 'thirteen cities'],
            ['17', 'בַּיּוֹם הַשְּׁבִיעִי', 'הַשְּׁבִיעִי', '7th', 'N/A (ordinal; agrees as adj.)', 'on the seventh day'],
            ['18', 'בַּחֹדֶשׁ הָרִאשׁוֹן', 'הָרִאשׁוֹן', '1st', 'N/A (ordinal; agrees as adj.)', 'in the first month'],
            ['19', 'הַשַּׁעַר הַשֵּׁנִי', 'הַשֵּׁנִי', '2nd', 'N/A (ordinal; agrees as adj.)', 'the second gate'],
            ['20', 'הַיּוֹם הָעֲשִׂירִי', 'הָעֲשִׂירִי', '10th', 'N/A (ordinal; agrees as adj.)', 'the tenth day'],
        ]
        self.add_generic_table(
            headers=['#', 'Hebrew Phrase', 'Number Word', 'Value', 'Gender Polarity?', 'Translation'],
            rows=rows,
            col_ratios=[0.05, 0.22, 0.16, 0.07, 0.18, 0.32],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans,
        )


def build_ch11_number_identification(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch11', 'exercises',
                               'ch11-number-identification')
    path = os.path.join(out_dir, 'ch11-number-identification.pdf')
    ex = Ch11NumberIdentificationExercise(
        title='Chapter 11 — Number Identification Drill',
        subtitle='Hebrew Numbers — Cardinals, Teens, Tens, and Ordinals',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch12VerbOverviewExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'Part A: For each Hebrew verb form and its gloss, identify: '
            '(1) the stem, (2) whether it expresses Active, Passive, or Reflexive meaning, '
            '(3) the three-letter root.\n'
            'Part B: For each English description of an action, identify which stem would be '
            'used in Hebrew and explain briefly why.\n'
            'Note: You do not need to parse conjugation or PGN yet.'
        )
        self.add_section_heading('Part A — Stem Identification (1–12)')
        rows_a = [
            ['1', 'שָׁמַר', '"he guarded"', '', '', ''],
            ['2', 'כָּתַב', '"he wrote"', '', '', ''],
            ['3', 'נָתַן', '"he gave"', '', '', ''],
            ['4', 'הָלַךְ', '"he walked"', '', '', ''],
            ['5', 'נִשְׁמַר', '"he was guarded / he kept himself"', '', '', ''],
            ['6', 'נִכְתַּב', '"it was written"', '', '', ''],
            ['7', 'הִשְׁמִיר', '"he caused to guard"', '', '', ''],
            ['8', 'הוֹלִיךְ', '"he caused to walk / he led"', '', '', ''],
            ['9', 'כִּתֵּב', '"he wrote (intensively / repeatedly)"', '', '', ''],
            ['10', 'שִׁמֵּר', '"he kept carefully / he tended"', '', '', ''],
            ['11', 'כֻּתַּב', '"it was written (intensive passive)"', '', '', ''],
            ['12', 'הִתְהַלֵּךְ', '"he walked about / he walked to and fro"', '', '', ''],
        ]
        ans_a = [
            ['1', 'שָׁמַר', '"he guarded"', 'Qal', 'Active', 'שמר'],
            ['2', 'כָּתַב', '"he wrote"', 'Qal', 'Active', 'כתב'],
            ['3', 'נָתַן', '"he gave"', 'Qal', 'Active', 'נתן'],
            ['4', 'הָלַךְ', '"he walked"', 'Qal', 'Active', 'הלך'],
            ['5', 'נִשְׁמַר', '"he was guarded / he kept himself"', 'Niphal', 'Passive/Reflexive', 'שמר'],
            ['6', 'נִכְתַּב', '"it was written"', 'Niphal', 'Passive', 'כתב'],
            ['7', 'הִשְׁמִיר', '"he caused to guard"', 'Hiphil', 'Active (causative)', 'שמר'],
            ['8', 'הוֹלִיךְ', '"he caused to walk / he led"', 'Hiphil', 'Active (causative)', 'הלך'],
            ['9', 'כִּתֵּב', '"he wrote (intensively)"', 'Piel', 'Active (intensive)', 'כתב'],
            ['10', 'שִׁמֵּר', '"he kept carefully"', 'Piel', 'Active (intensive)', 'שמר'],
            ['11', 'כֻּתַּב', '"it was written (intensive passive)"', 'Pual', 'Passive', 'כתב'],
            ['12', 'הִתְהַלֵּךְ', '"he walked about / to and fro"', 'Hithpael', 'Reflexive', 'הלך'],
        ]
        self.add_generic_table(
            headers=['#', 'Verb', 'Gloss', 'Stem', 'Active/Passive/Reflexive', 'Root'],
            rows=rows_a,
            col_ratios=[0.05, 0.12, 0.24, 0.12, 0.20, 0.27],
            heb_cols=[1],
            show_answers=True,
            answer_rows=ans_a,
        )
        self.add_section_heading('Part B — Meaning to Stem (1–8)')
        rows_b = [
            ['1', 'God caused Abraham to go out from Ur', '', ''],
            ['2', 'The letter was written by the scribe (simple passive)', '', ''],
            ['3', 'David walked around in his palace repeatedly', '', ''],
            ['4', 'The king was caused to reign (someone put him on the throne)', '', ''],
            ['5', 'She kept/guarded herself (simple reflexive)', '', ''],
            ['6', 'He wrote intensively / inscribed over and over (intensive passive)', '', ''],
            ['7', 'He killed himself thoroughly / destroyed himself (reflexive intensive)', '', ''],
            ['8', 'Moses guarded (base meaning, simple active)', '', ''],
        ]
        ans_b = [
            ['1', 'God caused Abraham to go out from Ur', 'Hiphil', 'Hiphil is causative active — subject causes another to perform the action.'],
            ['2', 'The letter was written (simple passive)', 'Niphal', 'Niphal is the simple passive (and reflexive) of the Qal.'],
            ['3', 'David walked around repeatedly', 'Hithpael', 'Hithpael is reflexive-intensive; הִתְהַלֵּךְ = "walk about/to and fro."'],
            ['4', 'The king was caused to reign', 'Hophal', 'Hophal is the causative passive — passive counterpart of the Hiphil.'],
            ['5', 'She kept/guarded herself (simple reflexive)', 'Niphal', 'Niphal doubles as reflexive for simple actions.'],
            ['6', 'He wrote intensively / inscribed over and over (intensive passive)', 'Pual', 'Pual is the passive counterpart of the Piel (intensive passive).'],
            ['7', 'He killed himself thoroughly (reflexive intensive)', 'Hithpael', 'Hithpael is reflexive and intensive — combines thoroughness with self-direction.'],
            ['8', 'Moses guarded (simple active)', 'Qal', 'Qal is the base, simple active stem.'],
        ]
        self.add_generic_table(
            headers=['#', 'Description', 'Stem', 'Explanation'],
            rows=rows_b,
            col_ratios=[0.05, 0.30, 0.12, 0.53],
            heb_cols=[],
            show_answers=True,
            answer_rows=ans_b,
        )


def build_ch12_verb_overview(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch12', 'exercises',
                               'ch12-verb-overview')
    path = os.path.join(out_dir, 'ch12-verb-overview.pdf')
    ex = Ch12VerbOverviewExercise(
        title='Chapter 12 — Verb Overview Exercise',
        subtitle='BBH Chapter 12 · 20 items',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Ch13–Ch15 builders
# ---------------------------------------------------------------------------

class Ch13ParsingDrillExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form, give: (a) Person, (b) Number, (c) Gender, '
            '(d) Root (3ms lexical form).\n'
            'Part C only: also identify the stative type '
            '(B = tsere, C = holem).'
        )
        hdrs_ab = ['#', 'Form', 'Person', 'Number', 'Gender', 'Root']
        cr_ab = [0.05, 0.16, 0.10, 0.10, 0.10, 0.49]
        hc = [1]

        self.add_section_heading('Part A — Clear Suffix Pattern (1–10)')
        rows_a = [
            ['1', 'שָׁמַרְתָּ', '', '', '', ''],
            ['2', 'כָּתַבְתִּי', '', '', '', ''],
            ['3', 'שָׁמְרוּ', '', '', '', ''],
            ['4', 'פָּקַדְנוּ', '', '', '', ''],
            ['5', 'מָשַׁלְתְּ', '', '', '', ''],
            ['6', 'בָּחַרְתֶּם', '', '', '', ''],
            ['7', 'זָכַרְתִּי', '', '', '', ''],
            ['8', 'לָמַד', '', '', '', ''],
            ['9', 'שָׁמַרְתֶּן', '', '', '', ''],
            ['10', 'חָפַרְתָּ', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'שָׁמַרְתָּ', '2', 's', 'm', 'שמר'],
            ['2', 'כָּתַבְתִּי', '1', 's', 'c', 'כתב'],
            ['3', 'שָׁמְרוּ', '3', 'p', 'c', 'שמר'],
            ['4', 'פָּקַדְנוּ', '1', 'p', 'c', 'פקד'],
            ['5', 'מָשַׁלְתְּ', '2', 's', 'f', 'משל'],
            ['6', 'בָּחַרְתֶּם', '2', 'p', 'm', 'בחר'],
            ['7', 'זָכַרְתִּי', '1', 's', 'c', 'זכר'],
            ['8', 'לָמַד', '3', 's', 'm', 'למד'],
            ['9', 'שָׁמַרְתֶּן', '2', 'p', 'f', 'שמר'],
            ['10', 'חָפַרְתָּ', '2', 's', 'm', 'חפר'],
        ]
        self.add_generic_table(headers=hdrs_ab, rows=rows_a, col_ratios=cr_ab, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Part B — Vowel Reduction Forms (11–20)')
        rows_b = [
            ['11', 'כָּתְבוּ', '', '', '', ''],
            ['12', 'שְׁמַרְתֶּם', '', '', '', ''],
            ['13', 'פָּקְדָה', '', '', '', ''],
            ['14', 'בָּחְרוּ', '', '', '', ''],
            ['15', 'מְשַׁלְתֶּן', '', '', '', ''],
            ['16', 'זָכַר', '', '', '', ''],
            ['17', 'חָפְרָה', '', '', '', ''],
            ['18', 'לָמְדוּ', '', '', '', ''],
            ['19', 'שְׁמַרְתֶּן', '', '', '', ''],
            ['20', 'פָּקַדְתְּ', '', '', '', ''],
        ]
        ans_b = [
            ['11', 'כָּתְבוּ', '3', 'p', 'c', 'כתב'],
            ['12', 'שְׁמַרְתֶּם', '2', 'p', 'm', 'שמר'],
            ['13', 'פָּקְדָה', '3', 's', 'f', 'פקד'],
            ['14', 'בָּחְרוּ', '3', 'p', 'c', 'בחר'],
            ['15', 'מְשַׁלְתֶּן', '2', 'p', 'f', 'משל'],
            ['16', 'זָכַר', '3', 's', 'm', 'זכר'],
            ['17', 'חָפְרָה', '3', 's', 'f', 'חפר'],
            ['18', 'לָמְדוּ', '3', 'p', 'c', 'למד'],
            ['19', 'שְׁמַרְתֶּן', '2', 'p', 'f', 'שמר'],
            ['20', 'פָּקַדְתְּ', '2', 's', 'f', 'פקד'],
        ]
        self.add_generic_table(headers=hdrs_ab, rows=rows_b, col_ratios=cr_ab, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Part C — Stative Roots (21–25)')
        rows_c = [
            ['21', 'כָּבַדְתָּ', '', '', '', '', ''],
            ['22', 'גָּדְלָה', '', '', '', '', ''],
            ['23', 'יָכֹלְתִּי', '', '', '', '', ''],
            ['24', 'זָקַנְתֶּם', '', '', '', '', ''],
            ['25', 'מָלְאָה', '', '', '', '', ''],
        ]
        ans_c = [
            ['21', 'כָּבַדְתָּ', '2', 's', 'm', 'כָּבֵד', 'B (tsere)'],
            ['22', 'גָּדְלָה', '3', 's', 'f', 'גָּדֵל', 'B (tsere)'],
            ['23', 'יָכֹלְתִּי', '1', 's', 'c', 'יָכֹל', 'C (holem)'],
            ['24', 'זָקַנְתֶּם', '2', 'p', 'm', 'זָקֵן', 'B (tsere)'],
            ['25', 'מָלְאָה', '3', 's', 'f', 'מָלֵא', 'B (tsere) / III-א'],
        ]
        self.add_generic_table(
            headers=['#', 'Form', 'Person', 'Number', 'Gender', 'Root (3ms)', 'Stative Type'],
            rows=rows_c,
            col_ratios=[0.05, 0.14, 0.09, 0.09, 0.09, 0.20, 0.34],
            heb_cols=hc,
            show_answers=True,
            answer_rows=ans_c,
        )


def build_ch13_parsing_drill(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch13', 'exercises',
                               'ch13-parsing-drill')
    path = os.path.join(out_dir, 'ch13-parsing-drill.pdf')
    ex = Ch13ParsingDrillExercise(
        title='Chapter 13 — Parsing Drill: Qal Perfect Strong Verbs',
        subtitle='BBH Chapter 13',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch13PassageExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'Parse each Qal Perfect verb. Give: '
            '(a) Person, (b) Number, (c) Gender, (d) Root (3ms lexical form), '
            '(e) Usage Type (Simple Past / Perfect of Experience / Stative / Prophetic Perfect).'
        )
        hdrs = ['#', 'Form', 'Person', 'Number', 'Gender', 'Root', 'Usage Type']
        cr = [0.05, 0.16, 0.09, 0.09, 0.09, 0.14, 0.38]
        hc = [1]

        self.add_section_heading('Passage A — Genesis 1:1–5 (1–2)')
        rows_a = [['1', 'בָּרָא', '', '', '', '', ''], ['2', 'הָיְתָה', '', '', '', '', '']]
        ans_a = [
            ['1', 'בָּרָא', '3', 's', 'm', 'ברא', 'Simple Past'],
            ['2', 'הָיְתָה', '3', 's', 'f', 'היה', 'Simple Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Passage B — Genesis 2:15–17 (3–4)')
        rows_b = [['3', 'אָכֹל', '', '', '', '', ''], ['4', 'אֲכָלְךָ', '', '', '', '', '']]
        ans_b = [
            ['3', 'אָכֹל', 'Inf. Abs.', '—', '—', 'אכל', 'Not a Perfect — Inf. Abs.'],
            ['4', 'אֲכָלְךָ', '2', 's', 'm', 'אכל', 'Simple Past + 2ms suffix'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Passage C — Genesis 3:6–13 (5–7)')
        rows_c = [
            ['5', 'נָתַתָּה', '', '', '', '', ''],
            ['6', 'נָתְנָה', '', '', '', '', ''],
            ['7', 'עָשִׂית', '', '', '', '', ''],
        ]
        ans_c = [
            ['5', 'נָתַתָּה', '2', 's', 'm', 'נתן', 'Simple Past'],
            ['6', 'נָתְנָה', '3', 's', 'f', 'נתן', 'Simple Past'],
            ['7', 'עָשִׂית', '2', 's', 'f', 'עשה', 'Simple Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Passage D — Genesis 4:1–10 (8–9)')
        rows_d = [['8', 'יָדַע', '', '', '', '', ''], ['9', 'יָדַעְתִּי', '', '', '', '', '']]
        ans_d = [
            ['8', 'יָדַע', '3', 's', 'm', 'ידע', 'Simple Past'],
            ['9', 'יָדַעְתִּי', '1', 's', 'c', 'ידע', 'Perfect of Experience'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)

        self.add_section_heading('Passage E — Additional Forms (10–15)')
        rows_e = [
            ['10', 'כָּבֵד', '', '', '', '', ''],
            ['11', 'שָׁמַעְנוּ', '', '', '', '', ''],
            ['12', 'קָטַלְתֶּם', '', '', '', '', ''],
            ['13', 'בָּרַכְתָּ', '', '', '', '', ''],
            ['14', 'יָשַׁבְנוּ', '', '', '', '', ''],
            ['15', 'קָרְאָה', '', '', '', '', ''],
        ]
        ans_e = [
            ['10', 'כָּבֵד', '3', 's', 'm', 'כבד', 'Stative'],
            ['11', 'שָׁמַעְנוּ', '1', 'p', 'c', 'שמע', 'Simple Past'],
            ['12', 'קָטַלְתֶּם', '2', 'p', 'm', 'קטל', 'Simple Past'],
            ['13', 'בָּרַכְתָּ', '2', 's', 'm', 'ברך', 'Simple Past'],
            ['14', 'יָשַׁבְנוּ', '1', 'p', 'c', 'ישב', 'Simple Past'],
            ['15', 'קָרְאָה', '3', 's', 'f', 'קרא', 'Simple Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_e, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_e)


def build_ch13_passage_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch13', 'exercises',
                               'ch13-passage-exercise')
    path = os.path.join(out_dir, 'ch13-passage-exercise.pdf')
    ex = Ch13PassageExercise(
        title='Chapter 13 — Passage Exercise: Qal Perfect Strong Verbs',
        subtitle='BBH Chapter 13',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch14PassageExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'Parse each highlighted Qal Perfect form. Give: '
            '(a) Person, (b) Number, (c) Gender, (d) Root (3ms lexical form), '
            '(e) Weak Class, (f) Usage Type.'
        )
        hdrs = ['#', 'Form', 'Person', 'Number', 'Gender', 'Root', 'Weak Class', 'Usage Type']
        cr = [0.05, 0.13, 0.08, 0.08, 0.08, 0.12, 0.14, 0.32]
        hc = [1]

        self.add_section_heading('Passage A — Genesis 3:1–13 (1–4)')
        rows_a = [
            ['1', 'הָיָה', '', '', '', '', '', ''],
            ['2', 'אָמַר', '', '', '', '', '', ''],
            ['3', 'אָכַלְנוּ', '', '', '', '', '', ''],
            ['4', 'עָשִׂית', '', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'הָיָה', '3', 's', 'm', 'היה', 'III-ה', 'Stative'],
            ['2', 'אָמַר', '3', 's', 'm', 'אמר', 'I-gutt.', 'Simple Past'],
            ['3', 'אָכַלְנוּ', '1', 'p', 'c', 'אכל', 'I-gutt.', 'Simple Past'],
            ['4', 'עָשִׂית', '2', 's', 'f', 'עשה', 'III-ה', 'Simple Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Passage B — Genesis 6:9–22 (5–8)')
        rows_b = [
            ['5', 'הָיָה', '', '', '', '', '', ''],
            ['6', 'בָּא', '', '', '', '', '', ''],
            ['7', 'מָלְאָה', '', '', '', '', '', ''],
            ['8', 'צִוָּה', '', '', '', '', '', ''],
        ]
        ans_b = [
            ['5', 'הָיָה', '3', 's', 'm', 'היה', 'III-ה', 'Stative'],
            ['6', 'בָּא', '3', 's', 'm', 'בוא', 'Biconsonantal', 'Simple Past'],
            ['7', 'מָלְאָה', '3', 's', 'f', 'מלא', 'III-א', 'Simple Past'],
            ['8', 'צִוָּה', '3', 's', 'm', 'צוה', 'III-ה', 'Simple Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Passage C — Genesis 22:1–12 (9–12)')
        rows_c = [
            ['9', 'נִסָּה', '', '', '', '', '', ''],
            ['10', 'אָהַבְתָּ', '', '', '', '', '', ''],
            ['11', 'יָדַעְתִּי', '', '', '', '', '', ''],
            ['12', 'חָשַׂכְתָּ', '', '', '', '', '', ''],
        ]
        ans_c = [
            ['9', 'נִסָּה', '3', 's', 'm', 'נסה', 'III-ה', 'Simple Past'],
            ['10', 'אָהַבְתָּ', '2', 's', 'm', 'אהב', 'I-gutt.', 'Perf. of Experience'],
            ['11', 'יָדַעְתִּי', '1', 's', 'c', 'ידע', 'I-י', 'Perf. of Experience'],
            ['12', 'חָשַׂכְתָּ', '2', 's', 'm', 'חשך', 'III-gutt.', 'Simple Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Passage D — Exodus 1:17–21 (13–14)')
        rows_d = [
            ['13', 'עָשׂוּ', '', '', '', '', '', ''],
            ['14', 'עֲשִׂיתֶן', '', '', '', '', '', ''],
        ]
        ans_d = [
            ['13', 'עָשׂוּ', '3', 'p', 'c', 'עשה', 'III-ה', 'Simple Past'],
            ['14', 'עֲשִׂיתֶן', '2', 'p', 'f', 'עשה', 'III-ה', 'Simple Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)

        self.add_section_heading('Passage E — Additional Forms (15–20)')
        rows_e = [
            ['15', 'שָׁמַעְנוּ', '', '', '', '', '', ''],
            ['16', 'בָּאוּ', '', '', '', '', '', ''],
            ['17', 'קָמָה', '', '', '', '', '', ''],
            ['18', 'יָלְדוּ', '', '', '', '', '', ''],
            ['19', 'נָתְנָה', '', '', '', '', '', ''],
            ['20', 'תַּמּוּ', '', '', '', '', '', ''],
        ]
        ans_e = [
            ['15', 'שָׁמַעְנוּ', '1', 'p', 'c', 'שמע', 'III-gutt.', 'Simple Past'],
            ['16', 'בָּאוּ', '3', 'p', 'c', 'בוא', 'Biconsonantal', 'Simple Past'],
            ['17', 'קָמָה', '3', 's', 'f', 'קום', 'Biconsonantal', 'Simple Past'],
            ['18', 'יָלְדוּ', '3', 'p', 'c', 'ילד', 'I-י', 'Simple Past'],
            ['19', 'נָתְנָה', '3', 's', 'f', 'נתן', 'I-נ', 'Simple Past'],
            ['20', 'תַּמּוּ', '3', 'p', 'c', 'תמם', 'Geminate', 'Simple Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_e, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_e)


def build_ch14_passage_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch14', 'exercises',
                               'ch14-passage-exercise')
    path = os.path.join(out_dir, 'ch14-passage-exercise.pdf')
    ex = Ch14PassageExercise(
        title='Chapter 14 — Passage Exercise: Qal Perfect Weak Verbs',
        subtitle='BBH Chapter 14',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch14WeakFormIdExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form, give: (a) Weak Class, (b) Person, (c) Number, '
            '(d) Gender, (e) Root (3ms lexical form).'
        )
        hdrs = ['#', 'Form', 'Weak Class', 'Person', 'Number', 'Gender', 'Root']
        cr = [0.05, 0.14, 0.15, 0.09, 0.09, 0.09, 0.39]
        hc = [1]
        groups = [
            ('Group 1: III-ה (1–5)', [
                ['1', 'עָשָׂה', '', '', '', '', ''],
                ['2', 'רָאִיתָ', '', '', '', '', ''],
                ['3', 'גָּלְתָה', '', '', '', '', ''],
                ['4', 'עָשׂוּ', '', '', '', '', ''],
                ['5', 'עֲלִיתֶם', '', '', '', '', ''],
            ], [
                ['1', 'עָשָׂה', 'III-ה', '3', 's', 'm', 'עשה'],
                ['2', 'רָאִיתָ', 'III-ה', '2', 's', 'm', 'ראה'],
                ['3', 'גָּלְתָה', 'III-ה', '3', 's', 'f', 'גלה'],
                ['4', 'עָשׂוּ', 'III-ה', '3', 'p', 'c', 'עשה'],
                ['5', 'עֲלִיתֶם', 'III-ה', '2', 'p', 'm', 'עלה'],
            ]),
            ('Group 2: III-א (6–10)', [
                ['6', 'מָצָא', '', '', '', '', ''],
                ['7', 'קָרְאָה', '', '', '', '', ''],
                ['8', 'חָטָאתִי', '', '', '', '', ''],
                ['9', 'מָצְאוּ', '', '', '', '', ''],
                ['10', 'מְצָאתֶם', '', '', '', '', ''],
            ], [
                ['6', 'מָצָא', 'III-א', '3', 's', 'm', 'מצא'],
                ['7', 'קָרְאָה', 'III-א', '3', 's', 'f', 'קרא'],
                ['8', 'חָטָאתִי', 'III-א', '1', 's', 'c', 'חטא'],
                ['9', 'מָצְאוּ', 'III-א', '3', 'p', 'c', 'מצא'],
                ['10', 'מְצָאתֶם', 'III-א', '2', 'p', 'm', 'מצא'],
            ]),
            ('Group 3: III-gutt. Lamed-Guttural (11–15)', [
                ['11', 'שָׁמַע', '', '', '', '', ''],
                ['12', 'שָׁלַח', '', '', '', '', ''],
                ['13', 'שָׁמַעְתִּי', '', '', '', '', ''],
                ['14', 'שָׁמְעוּ', '', '', '', '', ''],
                ['15', 'שְׁלַחְתֶּם', '', '', '', '', ''],
            ], [
                ['11', 'שָׁמַע', 'III-gutt.', '3', 's', 'm', 'שמע'],
                ['12', 'שָׁלַח', 'III-gutt.', '3', 's', 'm', 'שלח'],
                ['13', 'שָׁמַעְתִּי', 'III-gutt.', '1', 's', 'c', 'שמע'],
                ['14', 'שָׁמְעוּ', 'III-gutt.', '3', 'p', 'c', 'שמע'],
                ['15', 'שְׁלַחְתֶּם', 'III-gutt.', '2', 'p', 'm', 'שלח'],
            ]),
            ('Group 4: I-guttural / Pe-Guttural (16–20)', [
                ['16', 'אָמַר', '', '', '', '', ''],
                ['17', 'עָמַדְתָּ', '', '', '', '', ''],
                ['18', 'אָמַרְתִּי', '', '', '', '', ''],
                ['19', 'אֲמַרְתֶּם', '', '', '', '', ''],
                ['20', 'עָמְדוּ', '', '', '', '', ''],
            ], [
                ['16', 'אָמַר', 'I-gutt.', '3', 's', 'm', 'אמר'],
                ['17', 'עָמַדְתָּ', 'I-gutt.', '2', 's', 'm', 'עמד'],
                ['18', 'אָמַרְתִּי', 'I-gutt.', '1', 's', 'c', 'אמר'],
                ['19', 'אֲמַרְתֶּם', 'I-gutt.', '2', 'p', 'm', 'אמר'],
                ['20', 'עָמְדוּ', 'I-gutt.', '3', 'p', 'c', 'עמד'],
            ]),
            ('Group 5: I-נ and I-י (21–25)', [
                ['21', 'נָתַן', '', '', '', '', ''],
                ['22', 'נָתְנָה', '', '', '', '', ''],
                ['23', 'יָלַדְתָּ', '', '', '', '', ''],
                ['24', 'יָלְדוּ', '', '', '', '', ''],
                ['25', 'יָדַעְתִּי', '', '', '', '', ''],
            ], [
                ['21', 'נָתַן', 'I-נ', '3', 's', 'm', 'נתן'],
                ['22', 'נָתְנָה', 'I-נ', '3', 's', 'f', 'נתן'],
                ['23', 'יָלַדְתָּ', 'I-י', '2', 's', 'm', 'ילד'],
                ['24', 'יָלְדוּ', 'I-י', '3', 'p', 'c', 'ילד'],
                ['25', 'יָדַעְתִּי', 'I-י', '1', 's', 'c', 'ידע'],
            ]),
            ('Group 6: Biconsonantal (26–30)', [
                ['26', 'קָם', '', '', '', '', ''],
                ['27', 'שָׁבָה', '', '', '', '', ''],
                ['28', 'בָּאתָ', '', '', '', '', ''],
                ['29', 'קָמוּ', '', '', '', '', ''],
                ['30', 'שַׁבְתֶּם', '', '', '', '', ''],
            ], [
                ['26', 'קָם', 'Biconsonantal', '3', 's', 'm', 'קום'],
                ['27', 'שָׁבָה', 'Biconsonantal', '3', 's', 'f', 'שוב'],
                ['28', 'בָּאתָ', 'Biconsonantal', '2', 's', 'm', 'בוא'],
                ['29', 'קָמוּ', 'Biconsonantal', '3', 'p', 'c', 'קום'],
                ['30', 'שַׁבְתֶּם', 'Biconsonantal', '2', 'p', 'm', 'שוב'],
            ]),
            ('Group 7: Geminate (31–35)', [
                ['31', 'סָבַב', '', '', '', '', ''],
                ['32', 'תַּמּוּ', '', '', '', '', ''],
                ['33', 'סַבֹּתָ', '', '', '', '', ''],
                ['34', 'תָּם', '', '', '', '', ''],
                ['35', 'סָבָּה', '', '', '', '', ''],
            ], [
                ['31', 'סָבַב', 'Geminate', '3', 's', 'm', 'סבב'],
                ['32', 'תַּמּוּ', 'Geminate', '3', 'p', 'c', 'תמם'],
                ['33', 'סַבֹּתָ', 'Geminate', '2', 's', 'm', 'סבב'],
                ['34', 'תָּם', 'Geminate', '3', 's', 'm', 'תמם'],
                ['35', 'סָבָּה', 'Geminate', '3', 's', 'f', 'סבב'],
            ]),
        ]
        for heading, rows, ans in groups:
            self.add_section_heading(heading)
            self.add_generic_table(headers=hdrs, rows=rows, col_ratios=cr, heb_cols=hc,
                                   show_answers=True, answer_rows=ans)

        self.add_section_heading('Part B — Mixed (36–40)')
        rows_b = [
            ['36', 'הָיִיתִי', '', '', '', '', ''],
            ['37', 'נָפְלָה', '', '', '', '', ''],
            ['38', 'מָת', '', '', '', '', ''],
            ['39', 'בָּאנוּ', '', '', '', '', ''],
            ['40', 'שָׁמְעָה', '', '', '', '', ''],
        ]
        ans_b = [
            ['36', 'הָיִיתִי', 'III-ה', '1', 's', 'c', 'היה'],
            ['37', 'נָפְלָה', 'I-נ', '3', 's', 'f', 'נפל'],
            ['38', 'מָת', 'Biconsonantal', '3', 's', 'm', 'מות'],
            ['39', 'בָּאנוּ', 'Biconsonantal', '1', 'p', 'c', 'בוא'],
            ['40', 'שָׁמְעָה', 'III-gutt.', '3', 's', 'f', 'שמע'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)


def build_ch14_weak_form_id(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch14', 'exercises',
                               'ch14-weak-form-id')
    path = os.path.join(out_dir, 'ch14-weak-form-id.pdf')
    ex = Ch14WeakFormIdExercise(
        title='Chapter 14 — Weak-Form Identification Drill: Qal Perfect Weak Verbs',
        subtitle='BBH Chapter 14',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch15ParsingDrillExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form, give: (a) Person, (b) Number, (c) Gender, '
            '(d) Root (3ms lexical form).\n'
            'Part C: also identify whether the form is a Jussive or Cohortative.'
        )
        hdrs_ab = ['#', 'Form', 'Person', 'Number', 'Gender', 'Root']
        cr_ab = [0.05, 0.16, 0.10, 0.10, 0.10, 0.49]
        hc = [1]

        self.add_section_heading('Part A — A-Class (Holem): Clear Prefix Pattern (1–10)')
        rows_a = [
            ['1', 'יִשְׁמֹר', '', '', '', ''],
            ['2', 'תִּכְתְּבוּ', '', '', '', ''],
            ['3', 'נִפְקֹד', '', '', '', ''],
            ['4', 'תִּלְמְדִי', '', '', '', ''],
            ['5', 'יִזְכְּרוּ', '', '', '', ''],
            ['6', 'אֶשְׁמֹר', '', '', '', ''],
            ['7', 'תִּמְשֹׁל', '', '', '', ''],
            ['8', 'יִכְתְּבוּ', '', '', '', ''],
            ['9', 'תִּשְׁמֹרְנָה', '', '', '', ''],
            ['10', 'אֶבְחַר', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'יִשְׁמֹר', '3', 's', 'm', 'שמר'],
            ['2', 'תִּכְתְּבוּ', '2', 'p', 'm', 'כתב'],
            ['3', 'נִפְקֹד', '1', 'p', 'c', 'פקד'],
            ['4', 'תִּלְמְדִי', '2', 's', 'f', 'למד'],
            ['5', 'יִזְכְּרוּ', '3', 'p', 'm', 'זכר'],
            ['6', 'אֶשְׁמֹר', '1', 's', 'c', 'שמר'],
            ['7', 'תִּמְשֹׁל', '3/2', 's', 'f/m', 'משל'],
            ['8', 'יִכְתְּבוּ', '3', 'p', 'm', 'כתב'],
            ['9', 'תִּשְׁמֹרְנָה', '3/2', 'p', 'f', 'שמר'],
            ['10', 'אֶבְחַר', '1', 's', 'c', 'בחר'],
        ]
        self.add_generic_table(headers=hdrs_ab, rows=rows_a, col_ratios=cr_ab, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Part B — B-Class (Patach) and Disambiguation (11–20)')
        rows_b = [
            ['11', 'יִשְׁמַע', '', '', '', ''],
            ['12', 'תִּשְׁמַע', '', '', '', ''],
            ['13', 'תִּשְׁמְעִי', '', '', '', ''],
            ['14', 'יִכְבַּד', '', '', '', ''],
            ['15', 'תִּגְדַּל', '', '', '', ''],
            ['16', 'יִכְבְּדוּ', '', '', '', ''],
            ['17', 'תִּשְׁמַעְנָה', '', '', '', ''],
            ['18', 'אֶשְׁמַע', '', '', '', ''],
            ['19', 'נִשְׁמַע', '', '', '', ''],
            ['20', 'יִגְדַּל', '', '', '', ''],
        ]
        ans_b = [
            ['11', 'יִשְׁמַע', '3', 's', 'm', 'שמע'],
            ['12', 'תִּשְׁמַע', '3/2', 's', 'f/m', 'שמע'],
            ['13', 'תִּשְׁמְעִי', '2', 's', 'f', 'שמע'],
            ['14', 'יִכְבַּד', '3', 's', 'm', 'כבד'],
            ['15', 'תִּגְדַּל', '3/2', 's', 'f/m', 'גדל'],
            ['16', 'יִכְבְּדוּ', '3', 'p', 'm', 'כבד'],
            ['17', 'תִּשְׁמַעְנָה', '3/2', 'p', 'f', 'שמע'],
            ['18', 'אֶשְׁמַע', '1', 's', 'c', 'שמע'],
            ['19', 'נִשְׁמַע', '1', 'p', 'c', 'שמע'],
            ['20', 'יִגְדַּל', '3', 's', 'm', 'גדל'],
        ]
        self.add_generic_table(
            headers=['#', 'Form', 'Person', 'Number', 'Gender', 'Root', 'Notes'],
            rows=[[r[0], r[1], r[2], r[3], r[4], r[5], ''] for r in rows_b],
            col_ratios=[0.05, 0.14, 0.09, 0.09, 0.09, 0.16, 0.38],
            heb_cols=hc,
            show_answers=True,
            answer_rows=[[r[0], r[1], r[2], r[3], r[4], r[5], ''] for r in ans_b],
        )

        self.add_section_heading('Part C — Jussive and Cohortative Forms (21–25)')
        rows_c = [
            ['21', 'יִשְׁמְרָה', '', '', '', '', ''],
            ['22', 'נִשְׁמְרָה', '', '', '', '', ''],
            ['23', 'יִשְׁמֹר', '', '', '', '', ''],
            ['24', 'תִּשְׁמֹר', '', '', '', '', ''],
            ['25', 'אֶשְׁמְרָה', '', '', '', '', ''],
        ]
        ans_c = [
            ['21', 'יִשְׁמְרָה', '3', 's', 'm', 'שמר', 'Jussive/Energic'],
            ['22', 'נִשְׁמְרָה', '1', 'p', 'c', 'שמר', 'Cohortative'],
            ['23', 'יִשְׁמֹר', '3', 's', 'm', 'שמר', 'Jussive (= Imperfect for strong)'],
            ['24', 'תִּשְׁמֹר', '3/2', 's', 'f/m', 'שמר', 'Jussive (= Imperfect for strong)'],
            ['25', 'אֶשְׁמְרָה', '1', 's', 'c', 'שמר', 'Cohortative'],
        ]
        self.add_generic_table(
            headers=['#', 'Form', 'Person', 'Number', 'Gender', 'Root', 'Form Type'],
            rows=rows_c,
            col_ratios=[0.05, 0.14, 0.09, 0.09, 0.09, 0.14, 0.40],
            heb_cols=hc,
            show_answers=True,
            answer_rows=ans_c,
        )


def build_ch15_parsing_drill(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch15', 'exercises',
                               'ch15-parsing-drill')
    path = os.path.join(out_dir, 'ch15-parsing-drill.pdf')
    ex = Ch15ParsingDrillExercise(
        title='Chapter 15 — Parsing Drill: Qal Imperfect Strong Verbs',
        subtitle='BBH Chapter 15',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch15PassageExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'Parse each highlighted Qal Imperfect form. Give: '
            '(a) Person, (b) Number, (c) Gender, (d) Root (3ms lexical form), '
            '(e) Usage Type.'
        )
        hdrs = ['#', 'Form', 'Person', 'Number', 'Gender', 'Root', 'Usage Type']
        cr = [0.05, 0.16, 0.09, 0.09, 0.09, 0.14, 0.38]
        hc = [1]

        self.add_section_heading('Passage A — Exodus 3:1–12 (1–4)')
        rows_a = [
            ['1', 'אֵלֵךְ', '', '', '', '', ''],
            ['2', 'אֶרְאֶה', '', '', '', '', ''],
            ['3', 'תִקְרַב', '', '', '', '', ''],
            ['4', 'אֶהְיֶה', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'אֵלֵךְ', '1', 's', 'c', 'הלך', 'Cohortative'],
            ['2', 'אֶרְאֶה', '1', 's', 'c', 'ראה', 'Cohortative'],
            ['3', 'תִקְרַב', '2', 's', 'm', 'קרב', 'Prohibition'],
            ['4', 'אֶהְיֶה', '1', 's', 'c', 'היה', 'Simple Future'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Passage B — Exodus 3:13–20 (5–8)')
        rows_b = [
            ['5', 'אֵלֵךְ', '', '', '', '', ''],
            ['6', 'אוֹצִיא', '', '', '', '', ''],
            ['7', 'אֶשְׁלַח', '', '', '', '', ''],
            ['8', 'יִשְׁמְעוּ', '', '', '', '', ''],
        ]
        ans_b = [
            ['5', 'אֵלֵךְ', '1', 's', 'c', 'הלך', 'Modal'],
            ['6', 'אוֹצִיא', '1', 's', 'c', 'יצא', 'Modal/Future (Hiphil)'],
            ['7', 'אֶשְׁלַח', '1', 's', 'c', 'שלח', 'Simple Future'],
            ['8', 'יִשְׁמְעוּ', '3', 'p', 'm', 'שמע', 'Simple Future'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Passage C — Exodus 20:13–17, Decalogue (9–13)')
        rows_c = [
            ['9', 'תִּרְצָח', '', '', '', '', ''],
            ['10', 'תִנְאָף', '', '', '', '', ''],
            ['11', 'תִּגְנֹב', '', '', '', '', ''],
            ['12', 'תַעֲנֶה', '', '', '', '', ''],
            ['13', 'תַחְמֹד', '', '', '', '', ''],
        ]
        ans_c = [
            ['9', 'תִּרְצָח', '2', 's', 'm', 'רצח', 'Prohibition (לֹא)'],
            ['10', 'תִנְאָף', '2', 's', 'm', 'נאף', 'Prohibition (לֹא)'],
            ['11', 'תִּגְנֹב', '2', 's', 'm', 'גנב', 'Prohibition (לֹא)'],
            ['12', 'תַעֲנֶה', '2', 's', 'm', 'ענה', 'Prohibition (לֹא)'],
            ['13', 'תַחְמֹד', '2', 's', 'm', 'חמד', 'Prohibition (לֹא)'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Passage D — Genesis 1:3, 9, 11 (14–15)')
        rows_d = [
            ['14', 'יְהִי', '', '', '', '', ''],
            ['15', 'יִקָּווּ', '', '', '', '', ''],
        ]
        ans_d = [
            ['14', 'יְהִי', '3', 's', 'm', 'היה', 'Jussive'],
            ['15', 'יִקָּווּ', '3', 'p', 'm', 'קוה', 'Jussive/Command (Niphal)'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)


def build_ch15_passage_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch15', 'exercises',
                               'ch15-passage-exercise')
    path = os.path.join(out_dir, 'ch15-passage-exercise.pdf')
    ex = Ch15PassageExercise(
        title='Chapter 15 — Passage Exercise: Qal Imperfect Strong Verbs',
        subtitle='BBH Chapter 15',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Ch16–Ch18 builders
# ---------------------------------------------------------------------------

class Ch16PassageExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'Parse each highlighted verb. Give: '
            '(a) Person, (b) Number, (c) Gender, (d) Root (3ms lexical form), '
            '(e) Weak Class, (f) Form Type (Imperfect / Wayyiqtol / Jussive), '
            '(g) Usage Type.'
        )
        hdrs = ['#', 'Form', 'Person', 'Number', 'Gender', 'Root', 'Weak Class', 'Form Type', 'Usage Type']
        cr = [0.05, 0.12, 0.07, 0.07, 0.07, 0.11, 0.12, 0.10, 0.29]
        hc = [1]

        self.add_section_heading('Passage A — III-ה and III-א (Gen 1:3–11; Gen 3:1) (1–4)')
        rows_a = [
            ['1', 'יְהִי', '', '', '', '', '', '', ''],
            ['2', 'יַעֲשֶׂה', '', '', '', '', '', '', ''],
            ['3', 'יִהְיוּ', '', '', '', '', '', '', ''],
            ['4', 'תֹּאכְלוּ', '', '', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'יְהִי', '3', 's', 'm', 'היה', 'III-ה', 'Jussive', 'Volitional'],
            ['2', 'יַעֲשֶׂה', '3', 's', 'm', 'עשה', 'III-ה + I-gutt.', 'Jussive', 'Volitional'],
            ['3', 'יִהְיוּ', '3', 'p', 'm', 'היה', 'III-ה', 'Imperfect', 'Jussive/Volitional'],
            ['4', 'תֹּאכְלוּ', '2', 'p', 'm', 'אכל', 'I-gutt. (א)', 'Imperfect', 'Prohibition (לֹא)'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Passage B — III-Guttural and I-Guttural (Gen 3–4; Exo 20) (5–8)')
        rows_b = [
            ['5', 'יֹאמַר', '', '', '', '', '', '', ''],
            ['6', 'וַיִּשְׁמַע', '', '', '', '', '', '', ''],
            ['7', 'תַּחְמֹד', '', '', '', '', '', '', ''],
            ['8', 'וַיַּעֲמֹד', '', '', '', '', '', '', ''],
        ]
        ans_b = [
            ['5', 'יֹאמַר', '3', 's', 'm', 'אמר', 'I-gutt. (א)', 'Imperfect', 'Simple Future'],
            ['6', 'וַיִּשְׁמַע', '3', 's', 'm', 'שמע', 'III-gutt. (ע)', 'Wayyiqtol', 'Sequential Past'],
            ['7', 'תַּחְמֹד', '2', 's', 'm', 'חמד', 'I-gutt. (ח)', 'Imperfect', 'Prohibition (לֹא)'],
            ['8', 'וַיַּעֲמֹד', '3', 's', 'm', 'עמד', 'I-gutt. (ע)', 'Wayyiqtol', 'Sequential Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Passage C — I-נ and I-י (Gen 3–4; 9; Num 10) (9–12)')
        rows_c = [
            ['9', 'וַיִּתֵּן', '', '', '', '', '', '', ''],
            ['10', 'וַיֵּדַע', '', '', '', '', '', '', ''],
            ['11', 'יִתֵּן', '', '', '', '', '', '', ''],
            ['12', 'וַיֵּצֵא', '', '', '', '', '', '', ''],
        ]
        ans_c = [
            ['9', 'וַיִּתֵּן', '3', 's', 'm', 'נתן', 'I-נ', 'Wayyiqtol', 'Sequential Past'],
            ['10', 'וַיֵּדַע', '3', 's', 'm', 'ידע', 'I-י', 'Wayyiqtol', 'Sequential Past'],
            ['11', 'יִתֵּן', '3', 's', 'm', 'נתן', 'I-נ', 'Imperfect', 'Simple Future'],
            ['12', 'וַיֵּצֵא', '3', 's', 'm', 'יצא', 'I-י', 'Wayyiqtol', 'Sequential Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Passage D — Biconsonantal and Geminate (Gen 19–22) (13–16)')
        rows_d = [
            ['13', 'וַיָּבֹאוּ', '', '', '', '', '', '', ''],
            ['14', 'וַיָּקׇם', '', '', '', '', '', '', ''],
            ['15', 'יָשׁוּב', '', '', '', '', '', '', ''],
            ['16', 'וַיָּסׇּב', '', '', '', '', '', '', ''],
        ]
        ans_d = [
            ['13', 'וַיָּבֹאוּ', '3', 'p', 'm', 'בוא', 'Biconsonantal', 'Wayyiqtol', 'Sequential Past'],
            ['14', 'וַיָּקׇם', '3', 's', 'm', 'קום', 'Biconsonantal', 'Wayyiqtol', 'Sequential Past'],
            ['15', 'יָשׁוּב', '3', 's', 'm', 'שוב', 'Biconsonantal', 'Imperfect', 'Simple Future'],
            ['16', 'וַיָּסׇּב', '3', 's', 'm', 'סבב', 'Geminate', 'Wayyiqtol', 'Sequential Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)


def build_ch16_passage_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch16', 'exercises',
                               'ch16-passage-exercise')
    path = os.path.join(out_dir, 'ch16-passage-exercise.pdf')
    ex = Ch16PassageExercise(
        title='Chapter 16 — Passage Exercise: Qal Imperfect Weak Verbs',
        subtitle='BBH Chapter 16',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch16WeakFormIdExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form, identify: (a) Weak Class, (b) Person, (c) Number, '
            '(d) Gender, (e) Root.\n'
            'Part A: forms are grouped by class. Part B: forms are mixed — identify the class first.'
        )
        hdrs = ['#', 'Form', 'Weak Class', 'Person', 'Number', 'Gender', 'Root']
        cr = [0.05, 0.14, 0.15, 0.09, 0.09, 0.09, 0.39]
        hc = [1]
        groups = [
            ('Group 1: III-ה (Lamed-He) (1–5)', [
                ['1', 'יִבְנֶה', '', '', '', '', ''],
                ['2', 'תַּעֲשֶׂה', '', '', '', '', ''],
                ['3', 'יִהְיֶה', '', '', '', '', ''],
                ['4', 'תִּרְאֶה', '', '', '', '', ''],
                ['5', 'יִבֶּן', '', '', '', '', ''],
            ], [
                ['1', 'יִבְנֶה', 'III-ה', '3', 's', 'm', 'בנה'],
                ['2', 'תַּעֲשֶׂה', 'III-ה', '3/2', 's', 'f/m', 'עשה'],
                ['3', 'יִהְיֶה', 'III-ה', '3', 's', 'm', 'היה'],
                ['4', 'תִּרְאֶה', 'III-ה', '3/2', 's', 'f/m', 'ראה'],
                ['5', 'יִבֶּן', 'III-ה', '3', 's', 'm', 'בנה'],
            ]),
            ('Group 2: III-א (Lamed-Aleph) (6–10)', [
                ['6', 'יִמְצָא', '', '', '', '', ''],
                ['7', 'תִּקְרָא', '', '', '', '', ''],
                ['8', 'אֶמְצָא', '', '', '', '', ''],
                ['9', 'יִמְצְאוּ', '', '', '', '', ''],
                ['10', 'נִקְרָא', '', '', '', '', ''],
            ], [
                ['6', 'יִמְצָא', 'III-א', '3', 's', 'm', 'מצא'],
                ['7', 'תִּקְרָא', 'III-א', '3/2', 's', 'f/m', 'קרא'],
                ['8', 'אֶמְצָא', 'III-א', '1', 's', 'c', 'מצא'],
                ['9', 'יִמְצְאוּ', 'III-א', '3', 'p', 'm', 'מצא'],
                ['10', 'נִקְרָא', 'III-א', '1', 'p', 'c', 'קרא'],
            ]),
            ('Group 3: III-gutt. Lamed-Guttural (11–15)', [
                ['11', 'יִשְׁלַח', '', '', '', '', ''],
                ['12', 'תִּשְׁמַע', '', '', '', '', ''],
                ['13', 'וַיִּשְׁמַע', '', '', '', '', ''],
                ['14', 'יִשְׁלְחוּ', '', '', '', '', ''],
                ['15', 'אֶשְׁמַע', '', '', '', '', ''],
            ], [
                ['11', 'יִשְׁלַח', 'III-gutt.', '3', 's', 'm', 'שלח'],
                ['12', 'תִּשְׁמַע', 'III-gutt.', '3/2', 's', 'f/m', 'שמע'],
                ['13', 'וַיִּשְׁמַע', 'III-gutt.', '3', 's', 'm', 'שמע'],
                ['14', 'יִשְׁלְחוּ', 'III-gutt.', '3', 'p', 'm', 'שלח'],
                ['15', 'אֶשְׁמַע', 'III-gutt.', '1', 's', 'c', 'שמע'],
            ]),
            ('Group 4: I-Guttural (Pe-Guttural) (16–20)', [
                ['16', 'יַעֲמֹד', '', '', '', '', ''],
                ['17', 'תַּחֲלֹם', '', '', '', '', ''],
                ['18', 'יֹאמַר', '', '', '', '', ''],
                ['19', 'תַּעַמְדוּ', '', '', '', '', ''],
                ['20', 'נַעֲמֹד', '', '', '', '', ''],
            ], [
                ['16', 'יַעֲמֹד', 'I-gutt.', '3', 's', 'm', 'עמד'],
                ['17', 'תַּחֲלֹם', 'I-gutt.', '3/2', 's', 'f/m', 'חלם'],
                ['18', 'יֹאמַר', 'I-gutt. (א)', '3', 's', 'm', 'אמר'],
                ['19', 'תַּעַמְדוּ', 'I-gutt.', '2', 'p', 'm', 'עמד'],
                ['20', 'נַעֲמֹד', 'I-gutt.', '1', 'p', 'c', 'עמד'],
            ]),
            ('Group 5: I-נ (Pe-Nun) (21–25)', [
                ['21', 'יִתֵּן', '', '', '', '', ''],
                ['22', 'תִּתֵּן', '', '', '', '', ''],
                ['23', 'וַיִּתֵּן', '', '', '', '', ''],
                ['24', 'יִפֹּל', '', '', '', '', ''],
                ['25', 'תִּתְּנוּ', '', '', '', '', ''],
            ], [
                ['21', 'יִתֵּן', 'I-נ', '3', 's', 'm', 'נתן'],
                ['22', 'תִּתֵּן', 'I-נ', '3/2', 's', 'f/m', 'נתן'],
                ['23', 'וַיִּתֵּן', 'I-נ', '3', 's', 'm', 'נתן'],
                ['24', 'יִפֹּל', 'I-נ', '3', 's', 'm', 'נפל'],
                ['25', 'תִּתְּנוּ', 'I-נ', '2', 'p', 'm', 'נתן'],
            ]),
            ('Group 6: I-י (Pe-Yod) (26–30)', [
                ['26', 'יֵדַע', '', '', '', '', ''],
                ['27', 'תֵּשֵׁב', '', '', '', '', ''],
                ['28', 'וַיֵּלֶד', '', '', '', '', ''],
                ['29', 'יֵצֵא', '', '', '', '', ''],
                ['30', 'אֵלֵד', '', '', '', '', ''],
            ], [
                ['26', 'יֵדַע', 'I-י', '3', 's', 'm', 'ידע'],
                ['27', 'תֵּשֵׁב', 'I-י', '3/2', 's', 'f/m', 'ישב'],
                ['28', 'וַיֵּלֶד', 'I-י', '3', 's', 'm', 'ילד'],
                ['29', 'יֵצֵא', 'I-י', '3', 's', 'm', 'יצא'],
                ['30', 'אֵלֵד', 'I-י', '1', 's', 'c', 'ילד'],
            ]),
            ('Group 7: Biconsonantal (II-י/ו) (31–35)', [
                ['31', 'יָקוּם', '', '', '', '', ''],
                ['32', 'תָּבוֹא', '', '', '', '', ''],
                ['33', 'וַיָּבֹא', '', '', '', '', ''],
                ['34', 'יָמוּת', '', '', '', '', ''],
                ['35', 'וַיָּקׇם', '', '', '', '', ''],
            ], [
                ['31', 'יָקוּם', 'Biconsonantal', '3', 's', 'm', 'קום'],
                ['32', 'תָּבוֹא', 'Biconsonantal', '3/2', 's', 'f/m', 'בוא'],
                ['33', 'וַיָּבֹא', 'Biconsonantal', '3', 's', 'm', 'בוא'],
                ['34', 'יָמוּת', 'Biconsonantal', '3', 's', 'm', 'מות'],
                ['35', 'וַיָּקׇם', 'Biconsonantal', '3', 's', 'm', 'קום'],
            ]),
            ('Group 8: Geminate (Ayin-Doubled) (36–40)', [
                ['36', 'יָסֹב', '', '', '', '', ''],
                ['37', 'יִסֹּב', '', '', '', '', ''],
                ['38', 'וַיָּסׇּב', '', '', '', '', ''],
                ['39', 'תָּסֹב', '', '', '', '', ''],
                ['40', 'יִסֹּבּוּ', '', '', '', '', ''],
            ], [
                ['36', 'יָסֹב', 'Geminate', '3', 's', 'm', 'סבב'],
                ['37', 'יִסֹּב', 'Geminate', '3', 's', 'm', 'סבב'],
                ['38', 'וַיָּסׇּב', 'Geminate', '3', 's', 'm', 'סבב'],
                ['39', 'תָּסֹב', 'Geminate', '3/2', 's', 'f/m', 'סבב'],
                ['40', 'יִסֹּבּוּ', 'Geminate', '3', 'p', 'm', 'סבב'],
            ]),
        ]
        for heading, rows, ans in groups:
            self.add_section_heading(heading)
            self.add_generic_table(headers=hdrs, rows=rows, col_ratios=cr, heb_cols=hc,
                                   show_answers=True, answer_rows=ans)

        self.add_section_heading('Part B — Mixed Forms (41–50)')
        rows_b = [
            ['41', 'וַיָּקׇם', '', '', '', '', ''],
            ['42', 'יִבְנֶה', '', '', '', '', ''],
            ['43', 'יִתֵּן', '', '', '', '', ''],
            ['44', 'יַעֲשֶׂה', '', '', '', '', ''],
            ['45', 'תֵּדַע', '', '', '', '', ''],
            ['46', 'וַיִּשְׁמַע', '', '', '', '', ''],
            ['47', 'יִמְצָא', '', '', '', '', ''],
            ['48', 'וַיָּבֹאוּ', '', '', '', '', ''],
            ['49', 'תִּתֵּן', '', '', '', '', ''],
            ['50', 'יֵצֵא', '', '', '', '', ''],
        ]
        ans_b = [
            ['41', 'וַיָּקׇם', 'Biconsonantal', '3', 's', 'm', 'קום'],
            ['42', 'יִבְנֶה', 'III-ה', '3', 's', 'm', 'בנה'],
            ['43', 'יִתֵּן', 'I-נ', '3', 's', 'm', 'נתן'],
            ['44', 'יַעֲשֶׂה', 'III-ה', '3', 's', 'm', 'עשה'],
            ['45', 'תֵּדַע', 'I-י', '3/2', 's', 'f/m', 'ידע'],
            ['46', 'וַיִּשְׁמַע', 'III-gutt.', '3', 's', 'm', 'שמע'],
            ['47', 'יִמְצָא', 'III-א', '3', 's', 'm', 'מצא'],
            ['48', 'וַיָּבֹאוּ', 'Biconsonantal', '3', 'p', 'm', 'בוא'],
            ['49', 'תִּתֵּן', 'I-נ', '3/2', 's', 'f/m', 'נתן'],
            ['50', 'יֵצֵא', 'I-י', '3', 's', 'm', 'יצא'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)


def build_ch16_weak_form_id(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch16', 'exercises',
                               'ch16-weak-form-id')
    path = os.path.join(out_dir, 'ch16-weak-form-id.pdf')
    ex = Ch16WeakFormIdExercise(
        title='Chapter 16 — Weak Form ID Drill: Qal Imperfect Weak Verbs',
        subtitle='BBH Chapter 16',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch17ParsingDrillExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form, give: (a) Form Type (Wayyiqtol / Weqatal / Imperfect / Perfect), '
            '(b) Person, (c) Number, (d) Gender, (e) Root (3ms lexical form).'
        )
        hdrs_a = ['#', 'Form', 'Form Type', 'Person', 'Number', 'Gender', 'Root']
        cr_a = [0.05, 0.14, 0.14, 0.09, 0.09, 0.09, 0.40]
        hdrs_b = ['#', 'Form', 'Form Type', 'Person', 'Number', 'Gender', 'Root', 'Weak Class']
        cr_b = [0.05, 0.13, 0.12, 0.08, 0.08, 0.08, 0.14, 0.32]
        hc = [1]

        self.add_section_heading('Part A — Wayyiqtol: Strong and Common Weak Roots (1–10)')
        rows_a = [
            ['1', 'וַיֹּאמֶר', '', '', '', '', ''],
            ['2', 'וַתֹּאמֶר', '', '', '', '', ''],
            ['3', 'וַיֵּלֶךְ', '', '', '', '', ''],
            ['4', 'וַיִּקְטֹל', '', '', '', '', ''],
            ['5', 'וַיִּכְתְּבוּ', '', '', '', '', ''],
            ['6', 'וַתִּשְׁמֹרְנָה', '', '', '', '', ''],
            ['7', 'וָאֶקְטֹל', '', '', '', '', ''],
            ['8', 'וַנִּקְטֹל', '', '', '', '', ''],
            ['9', 'וַיִּתֵּן', '', '', '', '', ''],
            ['10', 'וַיָּבֹא', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'וַיֹּאמֶר', 'Wayyiqtol', '3', 's', 'm', 'אמר'],
            ['2', 'וַתֹּאמֶר', 'Wayyiqtol', '3', 's', 'f', 'אמר'],
            ['3', 'וַיֵּלֶךְ', 'Wayyiqtol', '3', 's', 'm', 'הלך'],
            ['4', 'וַיִּקְטֹל', 'Wayyiqtol', '3', 's', 'm', 'קטל'],
            ['5', 'וַיִּכְתְּבוּ', 'Wayyiqtol', '3', 'p', 'm', 'כתב'],
            ['6', 'וַתִּשְׁמֹרְנָה', 'Wayyiqtol', '3/2', 'p', 'f', 'שמר'],
            ['7', 'וָאֶקְטֹל', 'Wayyiqtol', '1', 's', 'c', 'קטל'],
            ['8', 'וַנִּקְטֹל', 'Wayyiqtol', '1', 'p', 'c', 'קטל'],
            ['9', 'וַיִּתֵּן', 'Wayyiqtol', '3', 's', 'm', 'נתן'],
            ['10', 'וַיָּבֹא', 'Wayyiqtol', '3', 's', 'm', 'בוא'],
        ]
        self.add_generic_table(headers=hdrs_a, rows=rows_a, col_ratios=cr_a, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Part B — Wayyiqtol: Weak Roots (11–20)')
        rows_b = [
            ['11', 'וַיַּרְא', '', '', '', '', '', ''],
            ['12', 'וַיְהִי', '', '', '', '', '', ''],
            ['13', 'וַיַּעַשׂ', '', '', '', '', '', ''],
            ['14', 'וַיָּקׇם', '', '', '', '', '', ''],
            ['15', 'וַיָּבֹאוּ', '', '', '', '', '', ''],
            ['16', 'וַיָּסׇּב', '', '', '', '', '', ''],
            ['17', 'וַיֵּדַע', '', '', '', '', '', ''],
            ['18', 'וַיֵּצֵא', '', '', '', '', '', ''],
            ['19', 'וַיִּבֶן', '', '', '', '', '', ''],
            ['20', 'וַיָּשׇׁב', '', '', '', '', '', ''],
        ]
        ans_b = [
            ['11', 'וַיַּרְא', 'Wayyiqtol', '3', 's', 'm', 'ראה', 'III-ה'],
            ['12', 'וַיְהִי', 'Wayyiqtol', '3', 's', 'm', 'היה', 'III-ה'],
            ['13', 'וַיַּעַשׂ', 'Wayyiqtol', '3', 's', 'm', 'עשה', 'III-ה + I-gutt.'],
            ['14', 'וַיָּקׇם', 'Wayyiqtol', '3', 's', 'm', 'קום', 'Biconsonantal'],
            ['15', 'וַיָּבֹאוּ', 'Wayyiqtol', '3', 'p', 'm', 'בוא', 'Biconsonantal'],
            ['16', 'וַיָּסׇּב', 'Wayyiqtol', '3', 's', 'm', 'סבב', 'Geminate'],
            ['17', 'וַיֵּדַע', 'Wayyiqtol', '3', 's', 'm', 'ידע', 'I-י'],
            ['18', 'וַיֵּצֵא', 'Wayyiqtol', '3', 's', 'm', 'יצא', 'I-י + III-א'],
            ['19', 'וַיִּבֶן', 'Wayyiqtol', '3', 's', 'm', 'בנה', 'III-ה'],
            ['20', 'וַיָּשׇׁב', 'Wayyiqtol', '3', 's', 'm', 'שוב', 'Biconsonantal'],
        ]
        self.add_generic_table(headers=hdrs_b, rows=rows_b, col_ratios=cr_b, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Part C — Weqatal and Disambiguation (21–30)')
        rows_c = [
            ['21', 'וְשָׁמַרְתָּ', '', '', '', '', ''],
            ['22', 'וְאָהַבְתָּ', '', '', '', '', ''],
            ['23', 'שָׁמַרְתָּ', '', '', '', '', ''],
            ['24', 'וּשְׁמַרְתֶּם', '', '', '', '', ''],
            ['25', 'וְנָתַתָּ', '', '', '', '', ''],
            ['26', 'יִשְׁמֹר', '', '', '', '', ''],
            ['27', 'וְשָׁמְרוּ', '', '', '', '', ''],
            ['28', 'שָׁמְרוּ', '', '', '', '', ''],
            ['29', 'וְעָשִׂיתָ', '', '', '', '', ''],
            ['30', 'וָאֹמַר', '', '', '', '', ''],
        ]
        ans_c = [
            ['21', 'וְשָׁמַרְתָּ', 'Weqatal', '2', 's', 'm', 'שמר'],
            ['22', 'וְאָהַבְתָּ', 'Weqatal', '2', 's', 'm', 'אהב'],
            ['23', 'שָׁמַרְתָּ', 'Perfect', '2', 's', 'm', 'שמר'],
            ['24', 'וּשְׁמַרְתֶּם', 'Weqatal', '2', 'p', 'm', 'שמר'],
            ['25', 'וְנָתַתָּ', 'Weqatal', '2', 's', 'm', 'נתן'],
            ['26', 'יִשְׁמֹר', 'Imperfect', '3', 's', 'm', 'שמר'],
            ['27', 'וְשָׁמְרוּ', 'Weqatal', '3', 'p', 'c', 'שמר'],
            ['28', 'שָׁמְרוּ', 'Perfect', '3', 'p', 'c', 'שמר'],
            ['29', 'וְעָשִׂיתָ', 'Weqatal', '2', 's', 'm', 'עשה'],
            ['30', 'וָאֹמַר', 'Wayyiqtol', '1', 's', 'c', 'אמר'],
        ]
        self.add_generic_table(headers=hdrs_a, rows=rows_c, col_ratios=cr_a, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)


def build_ch17_parsing_drill(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch17', 'exercises',
                               'ch17-parsing-drill')
    path = os.path.join(out_dir, 'ch17-parsing-drill.pdf')
    ex = Ch17ParsingDrillExercise(
        title='Chapter 17 — Parsing Drill: Wayyiqtol and Weqatal',
        subtitle='BBH Chapter 17',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch17PassageExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each highlighted form, give: '
            '(a) Form Type (Wayyiqtol / Weqatal / Imperfect / Perfect), '
            '(b) Person, (c) Number, (d) Gender, (e) Root (3ms lexical form), '
            '(f) Usage Note.'
        )
        hdrs = ['#', 'Form', 'Form Type', 'Person', 'Number', 'Gender', 'Root', 'Usage Note']
        cr = [0.05, 0.14, 0.11, 0.08, 0.08, 0.08, 0.12, 0.34]
        hc = [1]

        self.add_section_heading('Passage A — Genesis 1:1–5 (Creation Narrative) (1–4)')
        rows_a = [
            ['1', 'בָּרָא', '', '', '', '', '', ''],
            ['2', 'וַיְהִי', '', '', '', '', '', ''],
            ['3', 'וַיַּרְא', '', '', '', '', '', ''],
            ['4', 'וַיִּקְרָא', '', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'בָּרָא', 'Perfect', '3', 's', 'm', 'ברא', 'Simple Past'],
            ['2', 'וַיְהִי', 'Wayyiqtol', '3', 's', 'm', 'היה', 'Sequential Past'],
            ['3', 'וַיַּרְא', 'Wayyiqtol', '3', 's', 'm', 'ראה', 'Sequential Past'],
            ['4', 'וַיִּקְרָא', 'Wayyiqtol', '3', 's', 'm', 'קרא', 'Sequential Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Passage B — Genesis 22:1–4 (Binding of Isaac) (5–8)')
        rows_b = [
            ['5', 'וַיְהִי', '', '', '', '', '', ''],
            ['6', 'וַיַּשְׁכֵּם', '', '', '', '', '', ''],
            ['7', 'וַיָּקׇם', '', '', '', '', '', ''],
            ['8', 'וַיַּרְא', '', '', '', '', '', ''],
        ]
        ans_b = [
            ['5', 'וַיְהִי', 'Wayyiqtol', '3', 's', 'm', 'היה', 'Sequential Past'],
            ['6', 'וַיַּשְׁכֵּם', 'Wayyiqtol', '3', 's', 'm', 'שכם', 'Sequential Past'],
            ['7', 'וַיָּקׇם', 'Wayyiqtol', '3', 's', 'm', 'קום', 'Sequential Past'],
            ['8', 'וַיַּרְא', 'Wayyiqtol', '3', 's', 'm', 'ראה', 'Sequential Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Passage C — Deuteronomy 6:4–7 (The Shema) (9–11)')
        rows_c = [
            ['9', 'וְאָהַבְתָּ', '', '', '', '', '', ''],
            ['10', 'וְשִׁנַּנְתָּם', '', '', '', '', '', ''],
            ['11', 'וְדִבַּרְתָּ', '', '', '', '', '', ''],
        ]
        ans_c = [
            ['9', 'וְאָהַבְתָּ', 'Weqatal', '2', 's', 'm', 'אהב', 'Sequential Future'],
            ['10', 'וְשִׁנַּנְתָּם', 'Weqatal', '2', 's', 'm', 'שנן', 'Sequential Future'],
            ['11', 'וְדִבַּרְתָּ', 'Weqatal', '2', 's', 'm', 'דבר', 'Sequential Future'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Passage D — Exodus 3:1–6 (Burning Bush) (12–16)')
        rows_d = [
            ['12', 'וַיֵּלֶךְ', '', '', '', '', '', ''],
            ['13', 'וַיַּרְא', '', '', '', '', '', ''],
            ['14', 'וַיֵּפֶן', '', '', '', '', '', ''],
            ['15', 'וַיִּקְרָא', '', '', '', '', '', ''],
            ['16', 'וַיֹּאמֶר', '', '', '', '', '', ''],
        ]
        ans_d = [
            ['12', 'וַיֵּלֶךְ', 'Wayyiqtol', '3', 's', 'm', 'הלך', 'Sequential Past'],
            ['13', 'וַיַּרְא', 'Wayyiqtol', '3', 's', 'm', 'ראה', 'Sequential Past'],
            ['14', 'וַיֵּפֶן', 'Wayyiqtol', '3', 's', 'm', 'פנה', 'Sequential Past'],
            ['15', 'וַיִּקְרָא', 'Wayyiqtol', '3', 's', 'm', 'קרא', 'Sequential Past'],
            ['16', 'וַיֹּאמֶר', 'Wayyiqtol', '3', 's', 'm', 'אמר', 'Sequential Past'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)


def build_ch17_passage_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch17', 'exercises',
                               'ch17-passage-exercise')
    path = os.path.join(out_dir, 'ch17-passage-exercise.pdf')
    ex = Ch17PassageExercise(
        title='Chapter 17 — Passage Exercise: Wayyiqtol and Weqatal in Context',
        subtitle='BBH Chapter 17',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch18ParsingDrillExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form, give: (a) Conjugation (Imperative / Imperfect / Jussive / Cohortative), '
            '(b) Person, (c) Number, (d) Gender, (e) Root (lexical form).'
        )
        hdrs_a = ['#', 'Form', 'Conjugation', 'Person', 'Number', 'Gender', 'Root']
        cr_a = [0.05, 0.11, 0.14, 0.09, 0.09, 0.09, 0.43]
        hdrs_b = ['#', 'Form', 'Conjugation', 'Person', 'Number', 'Gender', 'Root', 'Weak Class']
        cr_b = [0.05, 0.10, 0.12, 0.08, 0.08, 0.08, 0.13, 0.36]
        hc = [1]

        self.add_section_heading('Part A — Strong and Common Roots (1–10)')
        rows_a = [
            ['1', 'שְׁמֹר', '', '', '', '', ''],
            ['2', 'שִׁמְרִי', '', '', '', '', ''],
            ['3', 'שִׁמְרוּ', '', '', '', '', ''],
            ['4', 'שְׁמֹרְנָה', '', '', '', '', ''],
            ['5', 'שְׁמַע', '', '', '', '', ''],
            ['6', 'שִׁמְעוּ', '', '', '', '', ''],
            ['7', 'זְכֹר', '', '', '', '', ''],
            ['8', 'חֲזַק', '', '', '', '', ''],
            ['9', 'כְּתֹב', '', '', '', '', ''],
            ['10', 'קְרָא', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'שְׁמֹר', 'Imperative', '2nd', 's', 'm', 'שמר'],
            ['2', 'שִׁמְרִי', 'Imperative', '2nd', 's', 'f', 'שמר'],
            ['3', 'שִׁמְרוּ', 'Imperative', '2nd', 'p', 'm', 'שמר'],
            ['4', 'שְׁמֹרְנָה', 'Imperative', '2nd', 'p', 'f', 'שמר'],
            ['5', 'שְׁמַע', 'Imperative', '2nd', 's', 'm', 'שמע'],
            ['6', 'שִׁמְעוּ', 'Imperative', '2nd', 'p', 'm', 'שמע'],
            ['7', 'זְכֹר', 'Imperative', '2nd', 's', 'm', 'זכר'],
            ['8', 'חֲזַק', 'Imperative', '2nd', 's', 'm', 'חזק'],
            ['9', 'כְּתֹב', 'Imperative', '2nd', 's', 'm', 'כתב'],
            ['10', 'קְרָא', 'Imperative', '2nd', 's', 'm', 'קרא'],
        ]
        self.add_generic_table(headers=hdrs_a, rows=rows_a, col_ratios=cr_a, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Part B — Weak Root Imperatives (11–25)')
        rows_b = [
            ['11', 'לֵךְ', '', '', '', '', '', ''],
            ['12', 'לְכוּ', '', '', '', '', '', ''],
            ['13', 'עֲשֵׂה', '', '', '', '', '', ''],
            ['14', 'עֲשׂוּ', '', '', '', '', '', ''],
            ['15', 'רְאֵה', '', '', '', '', '', ''],
            ['16', 'קוּם', '', '', '', '', '', ''],
            ['17', 'קוּמִי', '', '', '', '', '', ''],
            ['18', 'בֹּא', '', '', '', '', '', ''],
            ['19', 'שׁוּב', '', '', '', '', '', ''],
            ['20', 'שֵׁב', '', '', '', '', '', ''],
            ['21', 'צֵא', '', '', '', '', '', ''],
            ['22', 'תֵּן', '', '', '', '', '', ''],
            ['23', 'תְּנוּ', '', '', '', '', '', ''],
            ['24', 'אֱמֹר', '', '', '', '', '', ''],
            ['25', 'קַח', '', '', '', '', '', ''],
        ]
        ans_b = [
            ['11', 'לֵךְ', 'Imperative', '2nd', 's', 'm', 'הלך', 'I-י'],
            ['12', 'לְכוּ', 'Imperative', '2nd', 'p', 'm', 'הלך', 'I-י'],
            ['13', 'עֲשֵׂה', 'Imperative', '2nd', 's', 'm', 'עשה', 'III-ה + I-gutt.'],
            ['14', 'עֲשׂוּ', 'Imperative', '2nd', 'p', 'm', 'עשה', 'III-ה + I-gutt.'],
            ['15', 'רְאֵה', 'Imperative', '2nd', 's', 'm', 'ראה', 'III-ה'],
            ['16', 'קוּם', 'Imperative', '2nd', 's', 'm', 'קום', 'Biconsonantal'],
            ['17', 'קוּמִי', 'Imperative', '2nd', 's', 'f', 'קום', 'Biconsonantal'],
            ['18', 'בֹּא', 'Imperative', '2nd', 's', 'm', 'בוא', 'Biconsonantal'],
            ['19', 'שׁוּב', 'Imperative', '2nd', 's', 'm', 'שוב', 'Biconsonantal'],
            ['20', 'שֵׁב', 'Imperative', '2nd', 's', 'm', 'ישב', 'I-י'],
            ['21', 'צֵא', 'Imperative', '2nd', 's', 'm', 'יצא', 'I-י + III-א'],
            ['22', 'תֵּן', 'Imperative', '2nd', 's', 'm', 'נתן', 'I-נ'],
            ['23', 'תְּנוּ', 'Imperative', '2nd', 'p', 'm', 'נתן', 'I-נ'],
            ['24', 'אֱמֹר', 'Imperative', '2nd', 's', 'm', 'אמר', 'I-gutt. (א)'],
            ['25', 'קַח', 'Imperative', '2nd', 's', 'm', 'לקח', 'I-י'],
        ]
        self.add_generic_table(headers=hdrs_b, rows=rows_b, col_ratios=cr_b, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Part C — Disambiguation: Imperative, Imperfect, or Jussive? (26–35)')
        rows_c = [
            ['26', 'שְׁמֹר', '', '', '', '', ''],
            ['27', 'יִשְׁמֹר', '', '', '', '', ''],
            ['28', 'אַל־יִשְׁמֹר', '', '', '', '', ''],
            ['29', 'לְכוּ', '', '', '', '', ''],
            ['30', 'יֵלְכוּ', '', '', '', '', ''],
            ['31', 'עֲשֵׂה', '', '', '', '', ''],
            ['32', 'יַעַשׂ', '', '', '', '', ''],
            ['33', 'אַל־תַּעַשׂ', '', '', '', '', ''],
            ['34', 'בֹּא', '', '', '', '', ''],
            ['35', 'יָבֹא', '', '', '', '', ''],
        ]
        ans_c = [
            ['26', 'שְׁמֹר', 'Imperative', '2nd', 's', 'm', 'שמר'],
            ['27', 'יִשְׁמֹר', 'Imperfect', '3rd', 's', 'm', 'שמר'],
            ['28', 'אַל־יִשְׁמֹר', 'Jussive', '3rd', 's', 'm', 'שמר'],
            ['29', 'לְכוּ', 'Imperative', '2nd', 'p', 'm', 'הלך'],
            ['30', 'יֵלְכוּ', 'Imperfect', '3rd', 'p', 'm', 'הלך'],
            ['31', 'עֲשֵׂה', 'Imperative', '2nd', 's', 'm', 'עשה'],
            ['32', 'יַעַשׂ', 'Jussive', '3rd', 's', 'm', 'עשה'],
            ['33', 'אַל־תַּעַשׂ', 'Jussive', '2nd', 's', 'm', 'עשה'],
            ['34', 'בֹּא', 'Imperative', '2nd', 's', 'm', 'בוא'],
            ['35', 'יָבֹא', 'Imperfect', '3rd', 's', 'm', 'בוא'],
        ]
        self.add_generic_table(
            headers=['#', 'Form', 'Form Type', 'Person', 'Number', 'Gender', 'Root'],
            rows=rows_c,
            col_ratios=[0.05, 0.14, 0.14, 0.09, 0.09, 0.09, 0.40],
            heb_cols=hc,
            show_answers=True,
            answer_rows=ans_c,
        )


def build_ch18_parsing_drill(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch18', 'exercises',
                               'ch18-parsing-drill')
    path = os.path.join(out_dir, 'ch18-parsing-drill.pdf')
    ex = Ch18ParsingDrillExercise(
        title='Chapter 18 — Parsing Drill: Qal Imperative',
        subtitle='BBH Chapter 18',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------

class Ch18PassageExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each highlighted form, give: '
            '(a) Form Type (Imperative / Imperfect / Jussive / Weqatal), '
            '(b) Person, (c) Number, (d) Gender, (e) Root (lexical form), '
            '(f) Usage Note.'
        )
        hdrs = ['#', 'Form', 'Form Type', 'Person', 'Number', 'Gender', 'Root', 'Usage Note']
        cr = [0.05, 0.12, 0.11, 0.08, 0.08, 0.08, 0.13, 0.35]
        hc = [1]

        self.add_section_heading('Passage A — Genesis 12:1–3 (Call of Abraham) (1–3)')
        rows_a = [
            ['1', 'לֶךְ', '', '', '', '', '', ''],
            ['2', 'עֲזֹב', '', '', '', '', '', ''],
            ['3', 'וֶהְיֵה', '', '', '', '', '', ''],
        ]
        ans_a = [
            ['1', 'לֶךְ', 'Imperative', '2nd', 's', 'm', 'הלך', 'Direct Command'],
            ['2', 'עֲזֹב', 'Imperative', '2nd', 's', 'm', 'עזב', 'Direct Command'],
            ['3', 'וֶהְיֵה', 'Imperative', '2nd', 's', 'm', 'היה', 'Direct Command'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_a, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_a)

        self.add_section_heading('Passage B — Genesis 22:1–2 (Binding of Isaac) (4–6)')
        rows_b = [
            ['4', 'קַח', '', '', '', '', '', ''],
            ['5', 'וְלֶךְ', '', '', '', '', '', ''],
            ['6', 'וְהַעֲלֵהוּ', '', '', '', '', '', ''],
        ]
        ans_b = [
            ['4', 'קַח', 'Imperative', '2nd', 's', 'm', 'לקח', 'Direct Command'],
            ['5', 'וְלֶךְ', 'Imperative', '2nd', 's', 'm', 'הלך', 'Command Chain'],
            ['6', 'וְהַעֲלֵהוּ', 'Imperative', '2nd', 's', 'm', 'עלה', 'Direct Command (Hiphil)'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_b, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_b)

        self.add_section_heading('Passage C — Deuteronomy 6:4–9 (The Shema) (7–10)')
        rows_c = [
            ['7', 'שְׁמַע', '', '', '', '', '', ''],
            ['8', 'וְאָהַבְתָּ', '', '', '', '', '', ''],
            ['9', 'וְשִׁנַּנְתָּם', '', '', '', '', '', ''],
            ['10', 'וְדִבַּרְתָּ', '', '', '', '', '', ''],
        ]
        ans_c = [
            ['7', 'שְׁמַע', 'Imperative', '2nd', 's', 'm', 'שמע', 'Direct Command'],
            ['8', 'וְאָהַבְתָּ', 'Weqatal', '2nd', 's', 'm', 'אהב', 'Command Chain'],
            ['9', 'וְשִׁנַּנְתָּם', 'Weqatal', '2nd', 's', 'm', 'שנן', 'Command Chain'],
            ['10', 'וְדִבַּרְתָּ', 'Weqatal', '2nd', 's', 'm', 'דבר', 'Command Chain'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_c, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_c)

        self.add_section_heading('Passage D — Genesis 1:28 + Exodus 3:4–5 (Divine Commands) (11–15)')
        rows_d = [
            ['11', 'פְּרוּ', '', '', '', '', '', ''],
            ['12', 'רְבוּ', '', '', '', '', '', ''],
            ['13', 'מִלְאוּ', '', '', '', '', '', ''],
            ['14', 'אַל־תִּקְרַב', '', '', '', '', '', ''],
            ['15', 'שַׁל נְעָלֶיךָ', '', '', '', '', '', ''],
        ]
        ans_d = [
            ['11', 'פְּרוּ', 'Imperative', '2nd', 'p', 'm', 'פרה', 'Direct Command'],
            ['12', 'רְבוּ', 'Imperative', '2nd', 'p', 'm', 'רבה', 'Direct Command'],
            ['13', 'מִלְאוּ', 'Imperative', '2nd', 'p', 'm', 'מלא', 'Direct Command'],
            ['14', 'אַל־תִּקְרַב', 'Jussive', '2nd', 's', 'm', 'קרב', 'Prohibition'],
            ['15', 'שַׁל נְעָלֶיךָ', 'Imperative', '2nd', 's', 'm', 'שלף/של', 'Direct Command'],
        ]
        self.add_generic_table(headers=hdrs, rows=rows_d, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_d)

        self.add_section_heading('Passage E — Numbers 13:17–18 (Scouting Canaan) (16)')
        rows_e = [['16', 'עֲלוּ', '', '', '', '', '', '']]
        ans_e = [['16', 'עֲלוּ', 'Imperative', '2nd', 'p', 'm', 'עלה', 'Direct Command']]
        self.add_generic_table(headers=hdrs, rows=rows_e, col_ratios=cr, heb_cols=hc,
                               show_answers=True, answer_rows=ans_e)


def build_ch18_passage_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch18', 'exercises',
                               'ch18-passage-exercise')
    path = os.path.join(out_dir, 'ch18-passage-exercise.pdf')
    ex = Ch18PassageExercise(
        title='Chapter 18 — Passage Exercise: Qal Imperative in Context',
        subtitle='BBH Chapter 18',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Ch19 — Pronominal Suffixes on Verbs
# ---------------------------------------------------------------------------

class Ch19ParsingDrillExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form, give: (a) Base Verb — conjugation and PGN, '
            '(b) Root, (c) Suffix PGN, (d) Full Gloss.'
        )

        # Part A — Perfect + Suffix (1–8)
        hdrA = ['#', 'Form', 'Base Conjugation', 'Base PGN', 'Root',
                'Suffix PGN', 'Full Gloss']
        crA  = [0.05, 0.13, 0.14, 0.09, 0.10, 0.09, 0.40]
        rowsA = [
            ['1', 'שְׁמָרַ֥נִי', '', '', '', '', ''],
            ['2', 'שְׁמָרוֹ',   '', '', '', '', ''],
            ['3', 'שְׁמָרָ֥נוּ', '', '', '', '', ''],
            ['4', 'שְׁמַרְתַּ֥נִי', '', '', '', '', ''],
            ['5', 'שְׁמַרְתִּ֥יהוּ', '', '', '', '', ''],
            ['6', 'שְׁלָחַ֥נִי', '', '', '', '', ''],
            ['7', 'נְתָנַ֥נִי',  '', '', '', '', ''],
            ['8', 'עֲזָבַ֥נִי',  '', '', '', '', ''],
        ]
        ansA = [
            ['1', 'שְׁמָרַ֥נִי',  'Qal Perfect', '3ms', 'שמר', '1cs', 'he kept me'],
            ['2', 'שְׁמָרוֹ',    'Qal Perfect', '3ms', 'שמר', '3ms', 'he kept him'],
            ['3', 'שְׁמָרָ֥נוּ',  'Qal Perfect', '3ms', 'שמר', '1cp', 'he kept us'],
            ['4', 'שְׁמַרְתַּ֥נִי','Qal Perfect', '2ms', 'שמר', '1cs', 'you kept me'],
            ['5', 'שְׁמַרְתִּ֥יהוּ','Qal Perfect','1cs', 'שמר', '3ms', 'I kept him'],
            ['6', 'שְׁלָחַ֥נִי',  'Qal Perfect', '3ms', 'שלח', '1cs', 'he sent me'],
            ['7', 'נְתָנַ֥נִי',   'Qal Perfect', '3ms', 'נתן', '1cs', 'he gave me'],
            ['8', 'עֲזָבַ֥נִי',   'Qal Perfect', '3ms', 'עזב', '1cs', 'he forsook me'],
        ]
        self.add_section_heading('Part A — Perfect + Suffix (1–8)')
        self.add_generic_table(hdrA, rowsA, crA, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part B — Imperfect + Suffix (Energic Nun) (9–15)
        hdrB = ['#', 'Form', 'Base Conjugation', 'Base PGN', 'Root',
                'Suffix PGN', 'Energic Nun?', 'Full Gloss']
        crB  = [0.05, 0.12, 0.12, 0.09, 0.09, 0.09, 0.09, 0.35]
        rowsB = [
            ['9',  'יִשְׁמְרֵ֥נִי', '', '', '', '', '', ''],
            ['10', 'יִשְׁמְרֶ֥נּוּ', '', '', '', '', '', ''],
            ['11', 'יִשְׁמְרֵ֥נוּ', '', '', '', '', '', ''],
            ['12', 'תִּשְׁמְרֵ֥נִי', '', '', '', '', '', ''],
            ['13', 'יִמְצָאֵ֥נִי', '', '', '', '', '', ''],
            ['14', 'יִשְׁלָחֶ֥נּוּ', '', '', '', '', '', ''],
            ['15', 'יִרְאֶ֥נּוּ',   '', '', '', '', '', ''],
        ]
        ansB = [
            ['9',  'יִשְׁמְרֵ֥נִי', 'Qal Imperfect', '3ms', 'שמר', '1cs', 'No',  'he will keep me'],
            ['10', 'יִשְׁמְרֶ֥נּוּ', 'Qal Imperfect', '3ms', 'שמר', '3ms', 'Yes', 'he will keep him'],
            ['11', 'יִשְׁמְרֵ֥נוּ', 'Qal Imperfect', '3ms', 'שמר', '1cp', 'No',  'he will keep us'],
            ['12', 'תִּשְׁמְרֵ֥נִי', 'Qal Imperfect', '2ms/3fs', 'שמר', '1cs', 'No', 'you/she will keep me'],
            ['13', 'יִמְצָאֵ֥נִי', 'Qal Imperfect', '3ms', 'מצא', '1cs', 'No',  'he will find me'],
            ['14', 'יִשְׁלָחֶ֥נּוּ', 'Qal Imperfect', '3ms', 'שלח', '3ms', 'Yes', 'he will send him'],
            ['15', 'יִרְאֶ֥נּוּ',   'Qal Imperfect', '3ms', 'ראה', '3ms', 'Yes', 'he will see him'],
        ]
        self.add_section_heading('Part B — Imperfect + Suffix / Energic Nun (9–15)')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part C — Imperative and Wayyiqtol + Suffix (16–20)
        hdrC = ['#', 'Form', 'Base Conjugation', 'Base PGN', 'Root',
                'Suffix PGN', 'Full Gloss']
        rowsC = [
            ['16', 'שָׁמְרֵ֥נִי',   '', '', '', '', ''],
            ['17', 'וַיִּשְׁמְרֵ֥הוּ', '', '', '', '', ''],
            ['18', 'וַיִּשְׁלָחֵ֥הוּ', '', '', '', '', ''],
            ['19', 'וַיַּרְאֵ֥הוּ',  '', '', '', '', ''],
            ['20', 'שַׁלְּחֵ֥נִי',   '', '', '', '', ''],
        ]
        ansC = [
            ['16', 'שָׁמְרֵ֥נִי',   'Qal Imperative', '2ms', 'שמר', '1cs', 'Keep me!'],
            ['17', 'וַיִּשְׁמְרֵ֥הוּ', 'Qal Wayyiqtol', '3ms', 'שמר', '3ms', 'and he kept him'],
            ['18', 'וַיִּשְׁלָחֵ֥הוּ', 'Qal Wayyiqtol', '3ms', 'שלח', '3ms', 'and he sent him'],
            ['19', 'וַיַּרְאֵ֥הוּ',  'Qal Wayyiqtol', '3ms', 'ראה', '3ms', 'and he showed/saw him'],
            ['20', 'שַׁלְּחֵ֥נִי',   'Piel Imperative', '2ms', 'שלח', '1cs', 'Send me!'],
        ]
        self.add_section_heading('Part C — Imperative and Wayyiqtol + Suffix (16–20)')
        self.add_generic_table(hdrC, rowsC, crA, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part D — Infinitive Construct + Suffix (21–25)
        hdrD = ['#', 'Form', 'Base Conjugation', 'Root',
                'Suffix PGN', 'Suffix Role', 'Full Gloss']
        crD  = [0.05, 0.13, 0.14, 0.10, 0.09, 0.12, 0.37]
        rowsD = [
            ['21', 'בְּ/שָׁמְר/וֹ',   '', '', '', '', ''],
            ['22', 'כִּ/שְׁמֹ֣עַ/וֹ', '', '', '', '', ''],
            ['23', 'בְּ/רֹאֹת/וֹ',   '', '', '', '', ''],
            ['24', 'לְ/אָהֳבָ֥/הּ',  '', '', '', '', ''],
            ['25', 'כְּ/צֵאת/וֹ',    '', '', '', '', ''],
        ]
        ansD = [
            ['21', 'בְּ/שָׁמְר/וֹ',   'Qal Inf.Const.', 'שמר', '3ms', 'Subject', 'when he kept / in his keeping'],
            ['22', 'כִּ/שְׁמֹ֣עַ/וֹ', 'Qal Inf.Const.', 'שמע', '3ms', 'Subject', 'when he heard'],
            ['23', 'בְּ/רֹאֹת/וֹ',   'Qal Inf.Const.', 'ראה', '3ms', 'Subject', 'when he saw'],
            ['24', 'לְ/אָהֳבָ֥/הּ',  'Qal Inf.Const.', 'אהב', '3fs', 'Subject/Object', 'to love her'],
            ['25', 'כְּ/צֵאת/וֹ',    'Qal Inf.Const.', 'יצא', '3ms', 'Subject', 'when he went out'],
        ]
        self.add_section_heading('Part D — Infinitive Construct + Suffix (21–25)')
        self.add_generic_table(hdrD, rowsD, crD, heb_cols=[1],
                               show_answers=False)

        # Answer key
        self.add_section_break()
        self.add_section_heading('Answer Key — Part A')
        self.add_generic_table(hdrA, rowsA, crA, heb_cols=[1],
                               show_answers=True, answer_rows=ansA)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=True, answer_rows=ansB)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part C')
        self.add_generic_table(hdrC, rowsC, crA, heb_cols=[1],
                               show_answers=True, answer_rows=ansC)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part D')
        self.add_generic_table(hdrD, rowsD, crD, heb_cols=[1],
                               show_answers=True, answer_rows=ansD)


def build_ch19_parsing_drill(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch19', 'exercises',
                               'ch19-parsing-drill')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'ch19-parsing-drill.pdf')
    ex = Ch19ParsingDrillExercise(
        title='Chapter 19 — Parsing Drill: Pronominal Suffixes on Verbs',
        subtitle='BBH Chapter 19',
    )
    return ex.save(path)


class Ch19PassageExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each highlighted form: (a) Base Verb — conjugation and root, '
            '(b) Suffix PGN, (c) Suffix Role (Object / Subject on Inf.Const.), '
            '(d) Full Gloss.'
        )
        hdr = ['#', 'Form', 'Base Conj.', 'Root',
               'Suffix PGN', 'Suffix Role', 'Full Gloss']
        cr  = [0.05, 0.14, 0.14, 0.09, 0.09, 0.10, 0.39]

        passages = [
            ('Passage A — Genesis 28:13–15 (God\'s Promise to Jacob)', [
                ['1', 'וּשְׁמַרְתִּיךָ',  '', '', '', '', ''],
                ['2', 'וַהֲשִׁבֹתִיךָ',  '', '', '', '', ''],
                ['3', 'אֶעֱזָבְךָ',      '', '', '', '', ''],
            ], [
                ['1', 'וּשְׁמַרְתִּיךָ',  'Qal Weqatal 1cs', 'שמר', '2ms', 'Object', 'and I will keep you'],
                ['2', 'וַהֲשִׁבֹתִיךָ',  'Hiphil Weqatal 1cs', 'שוב', '2ms', 'Object', 'and I will bring you back'],
                ['3', 'אֶעֱזָבְךָ',      'Qal Imperfect 1cs', 'עזב', '2ms', 'Object', 'I will forsake you'],
            ]),
            ('Passage B — Genesis 45:4–8 (Joseph Reveals Himself)', [
                ['4', 'שְׁלָחַ֥נִי (first)', '', '', '', '', ''],
                ['5', 'וַיִּשְׁלָחֵ֥נִי',   '', '', '', '', ''],
                ['6', 'מְכַרְתֶּ֥ם אֹתִי',  '', '', '', '', ''],
            ], [
                ['4', 'שְׁלָחַ֥נִי',        'Qal Perfect 3ms', 'שלח', '1cs', 'Object', 'God sent me'],
                ['5', 'וַיִּשְׁלָחֵ֥נִי',   'Qal Wayyiqtol 3ms', 'שלח', '1cs', 'Object', 'and God sent me'],
                ['6', 'מְכַרְתֶּ֥ם אֹתִי',  'Qal Perfect 2mp', 'מכר', '—', '—', 'you sold me (אֹתִי separate)'],
            ]),
            ('Passage C — Psalm 23:1–4 (The LORD My Shepherd)', [
                ['7',  'יַרְבִּיצֵ֑נִי', '', '', '', '', ''],
                ['8',  'יְנַהֲלֵ֥נִי',  '', '', '', '', ''],
                ['9',  'יַנְחֵ֥נִי',    '', '', '', '', ''],
                ['10', 'יְנַחֲמֻ֑נִי',  '', '', '', '', ''],
            ], [
                ['7',  'יַרְבִּיצֵ֑נִי', 'Hiphil Imperfect 3ms', 'רבץ', '1cs', 'Object', 'he makes me lie down'],
                ['8',  'יְנַהֲלֵ֥נִי',  'Piel Imperfect 3ms',   'נהל', '1cs', 'Object', 'he leads me'],
                ['9',  'יַנְחֵ֥נִי',    'Hiphil Imperfect 3ms', 'נחה', '1cs', 'Object', 'he guides me'],
                ['10', 'יְנַחֲמֻ֑נִי',  'Piel Imperfect 3mp',   'נחם', '1cs', 'Object', 'they comfort me'],
            ]),
            ('Passage D — Genesis 39:12–20 (Infinitive Construct + Suffix)', [
                ['11', 'כִּשְׁמֹ֣עַ אֲדֹנָ֗יו', '', '', '', '', ''],
                ['12', 'כְּרְאֹת/וֹ',            '', '', '', '', ''],
                ['13', 'עָזַ֤ב בִּגְד/וֹ',        '', '', '', '', ''],
                ['14', 'בִּהְיוֹת/וֹ',            '', '', '', '', ''],
            ], [
                ['11', 'כִּשְׁמֹ֣עַ',  'Qal Inf.Const.', 'שמע', '3ms (noun)', 'Subject', 'when his master heard'],
                ['12', 'כְּרְאֹת/וֹ', 'Qal Inf.Const.', 'ראה', '3ms', 'Subject', 'when he saw'],
                ['13', 'בִּגְד/וֹ',   'noun suffix',    'בֶּגֶד', '3ms', 'Possessive', 'his garment'],
                ['14', 'בִּהְיוֹת/וֹ', 'Qal Inf.Const.', 'היה', '3ms', 'Subject', 'while he was there'],
            ]),
            ('Passage E — Psalm 16:1 + Deuteronomy 31:6', [
                ['15', 'שָׁמְרֵ֥נִי',    '', '', '', '', ''],
                ['16', 'יַעַזְבֶ֔/ךָּ', '', '', '', '', ''],
            ], [
                ['15', 'שָׁמְרֵ֥נִי',    'Qal Imperative 2ms', 'שמר', '1cs', 'Object', 'Keep me!'],
                ['16', 'יַעַזְבֶ֔/ךָּ', 'Qal Imperfect 3ms',  'עזב', '2ms', 'Object', 'he will forsake you'],
            ]),
        ]

        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=False)
            self.add_section_break()

        self.add_section_heading('Answer Key')
        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)
            self.add_section_break()


def build_ch19_passage_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch19', 'exercises',
                               'ch19-passage-exercise')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'ch19-passage-exercise.pdf')
    ex = Ch19PassageExercise(
        title='Chapter 19 — Passage Exercise: Pronominal Suffixes on Verbs in Context',
        subtitle='BBH Chapter 19',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Ch20 — Qal Infinitive Construct
# ---------------------------------------------------------------------------

class Ch20ParsingDrillExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form: (a) Identify as IC or another form (Imperative / '
            'Imperfect / Perfect), (b) Root, (c) Root class, '
            '(d) Preposition (if any), (e) Function (Purpose / Temporal / '
            'Complementary / Quotative / From / Until).'
        )

        # Part A — Strong and B-class Roots (1–8)
        hdrA = ['#', 'Form', 'IC or other?', 'Root', 'Root Class', 'Prep', 'Function']
        crA  = [0.05, 0.13, 0.12, 0.10, 0.12, 0.08, 0.40]
        rowsA = [
            ['1', 'לִ/שְׁמֹר',  '', '', '', '', ''],
            ['2', 'לִ/שְׁמֹ֣עַ', '', '', '', '', ''],
            ['3', 'כִּ/שְׁמֹ֣עַ', '', '', '', '', ''],
            ['4', 'בִּ/זְכֹר',   '', '', '', '', ''],
            ['5', 'לִ/כְתֹב',   '', '', '', '', ''],
            ['6', 'לֵ/אמֹר',    '', '', '', '', ''],
            ['7', 'לֶ/אֱכֹל',   '', '', '', '', ''],
            ['8', 'מֵ/עֲשׂוֹת', '', '', '', '', ''],
        ]
        ansA = [
            ['1', 'לִ/שְׁמֹר',  'IC', 'שמר', 'Strong A',          'לְ', 'Purpose/Complementary'],
            ['2', 'לִ/שְׁמֹ֣עַ', 'IC', 'שמע', 'Strong B (gutt.)', 'לְ', 'Purpose/Complementary'],
            ['3', 'כִּ/שְׁמֹ֣עַ', 'IC', 'שמע', 'Strong B (gutt.)', 'כְּ', 'Temporal (when/as)'],
            ['4', 'בִּ/זְכֹר',   'IC', 'זכר', 'Strong A',          'בְּ', 'Temporal (when)'],
            ['5', 'לִ/כְתֹב',   'IC', 'כתב', 'Strong A',          'לְ', 'Purpose'],
            ['6', 'לֵ/אמֹר',    'IC', 'אמר', 'I-aleph',           'לְ', 'Quotative'],
            ['7', 'לֶ/אֱכֹל',   'IC', 'אכל', 'I-aleph',           'לְ', 'Purpose/Complementary'],
            ['8', 'מֵ/עֲשׂוֹת', 'IC', 'עשה', 'III-ה + I-gutt.',   'מִן', 'From/cessation'],
        ]
        self.add_section_heading('Part A — Strong and B-class Roots (1–8)')
        self.add_generic_table(hdrA, rowsA, crA, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part B — III-ה and Biconsonantal (9–15): no "IC or other?" column
        hdrB = ['#', 'Form', 'Root', 'Root Class', 'Prep', 'Function']
        crB  = [0.05, 0.14, 0.10, 0.12, 0.08, 0.51]
        rowsB = [
            ['9',  'לִ/רְאוֹת', '', '', '', ''],
            ['10', 'לַ/עֲשׂוֹת', '', '', '', ''],
            ['11', 'הֱיוֹת',     '', '', '', ''],
            ['12', 'לָ/בֹא',     '', '', '', ''],
            ['13', 'לָ/שׁוּב',   '', '', '', ''],
            ['14', 'לָ/מוּת',    '', '', '', ''],
            ['15', 'בְּ/בֹא',    '', '', '', ''],
        ]
        ansB = [
            ['9',  'לִ/רְאוֹת', 'ראה', 'III-ה',           'לְ', 'Purpose'],
            ['10', 'לַ/עֲשׂוֹת', 'עשה', 'III-ה + I-gutt.', 'לְ', 'Purpose/Complementary'],
            ['11', 'הֱיוֹת',     'היה', 'III-ה',           '—',  'Verbal noun/Complementary'],
            ['12', 'לָ/בֹא',     'בוא', 'Biconsonantal',   'לְ', 'Purpose/Complementary'],
            ['13', 'לָ/שׁוּב',   'שוב', 'Biconsonantal',   'לְ', 'Purpose/Complementary'],
            ['14', 'לָ/מוּת',    'מות', 'Biconsonantal',   'לְ', 'Purpose'],
            ['15', 'בְּ/בֹא',    'בוא', 'Biconsonantal',   'בְּ', 'Temporal (when)'],
        ]
        self.add_section_heading('Part B — III-ה and Biconsonantal (9–15)')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part C — I-י, I-נ, and Disambiguation (16–25)
        hdrC = ['#', 'Form', 'IC or other?', 'Root', 'Root Class', 'Notes']
        crC  = [0.05, 0.13, 0.12, 0.10, 0.12, 0.48]
        rowsC = [
            ['16', 'לֶ/כֶת',  '', '', '', ''],
            ['17', 'לָ/שֶׁ/בֶת', '', '', '', ''],
            ['18', 'צֵאת',    '', '', '', ''],
            ['19', 'תֵּת',    '', '', '', ''],
            ['20', 'לָ/דַ/עַת', '', '', '', ''],
            ['21', 'שְׁמֹר',  '', '', '', ''],
            ['22', 'שְׁמֹ֣עַ', '', '', '', ''],
            ['23', 'לֶ/כֶת',  '', '', '', ''],
            ['24', 'יִשְׁמֹר', '', '', '', ''],
            ['25', 'שָׁמַר',  '', '', '', ''],
        ]
        ansC = [
            ['16', 'לֶ/כֶת',  'IC', 'הלך', 'I-י', '"to go"; contracted form'],
            ['17', 'לָ/שֶׁ/בֶת', 'IC', 'ישב', 'I-י', '"to dwell/sit"; yod drops'],
            ['18', 'צֵאת',    'IC', 'יצא', 'I-י + III-א', '"going out"; bare IC with taw'],
            ['19', 'תֵּת',    'IC', 'נתן', 'I-נ', '"to give"; both nuns drop'],
            ['20', 'לָ/דַ/עַת', 'IC', 'ידע', 'I-י', '"to know"'],
            ['21', 'שְׁמֹר',  'IC or Imper.', 'שמר', 'Strong A', 'Ambiguous — context determines'],
            ['22', 'שְׁמֹ֣עַ', 'IC or Imper.', 'שמע', 'Strong B', 'Ambiguous — context determines'],
            ['23', 'לֶ/כֶת',  'IC', 'הלך', 'I-י', 'Cannot be Imperative (which is לֵךְ)'],
            ['24', 'יִשְׁמֹר', 'Imperfect', 'שמר', 'Strong A', 'יִ– prefix = Imperfect'],
            ['25', 'שָׁמַר',  'Perfect', 'שמר', 'Strong A', 'Qamets + patach = Perfect 3ms'],
        ]
        self.add_section_heading('Part C — I-י, I-נ, and Disambiguation (16–25)')
        self.add_generic_table(hdrC, rowsC, crC, heb_cols=[1],
                               show_answers=False)

        # Answer key
        self.add_section_break()
        self.add_section_heading('Answer Key — Part A')
        self.add_generic_table(hdrA, rowsA, crA, heb_cols=[1],
                               show_answers=True, answer_rows=ansA)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=True, answer_rows=ansB)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part C')
        self.add_generic_table(hdrC, rowsC, crC, heb_cols=[1],
                               show_answers=True, answer_rows=ansC)


def build_ch20_parsing_drill(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch20', 'exercises',
                               'ch20-parsing-drill')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'ch20-parsing-drill.pdf')
    ex = Ch20ParsingDrillExercise(
        title='Chapter 20 — Parsing Drill: Qal Infinitive Construct',
        subtitle='BBH Chapter 20',
    )
    return ex.save(path)


class Ch20PassageExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each highlighted IC form: (a) Root, (b) Root class, '
            '(c) Preposition, (d) Function (Purpose / Temporal / '
            'Complementary / Quotative / From / Epexegetical), (e) Gloss.'
        )
        hdr = ['#', 'Form', 'Root', 'Root Class', 'Prep', 'Function', 'Gloss']
        cr  = [0.05, 0.14, 0.10, 0.12, 0.08, 0.14, 0.37]

        passages = [
            ('Passage 1 — Genesis 2:16–17 (The Garden Command)', [
                ['1', 'לֵאמֹ֑ר', '', '', '', '', ''],
            ], [
                ['1', 'לֵאמֹ֑ר', 'אמר', 'I-aleph', 'לְ', 'Quotative', 'saying'],
            ]),
            ('Passage 2 — Genesis 11:5 (Babel)', [
                ['2', 'לִרְאֹ֥ת', '', '', '', '', ''],
            ], [
                ['2', 'לִרְאֹ֥ת', 'ראה', 'III-ה', 'לְ', 'Purpose', 'to see'],
            ]),
            ('Passage 3 — Genesis 19:22 (Sodom)', [
                ['3', 'לַעֲשׂ֣וֹת', '', '', '', '', ''],
            ], [
                ['3', 'לַעֲשׂ֣וֹת', 'עשה', 'III-ה + I-gutt.', 'לְ', 'Complementary', 'to do'],
            ]),
            ('Passage 4 — Genesis 37:18 (Joseph\'s Brothers)', [
                ['4', 'לַהֲמִית֖וֹ', '', '', '', '', ''],
            ], [
                ['4', 'לַהֲמִית֖וֹ', 'מות', 'Biconsonantal (Hiphil IC)', 'לְ', 'Purpose', 'to kill him'],
            ]),
            ('Passage 5 — Genesis 39:18–19 (Potiphar\'s Wife)', [
                ['5', 'כְשָׁמְע֣וֹ',  '', '', '', '', ''],
                ['6', 'כִשְׁמֹ֨עַ',  '', '', '', '', ''],
            ], [
                ['5', 'כְשָׁמְע֣וֹ',  'שמע', 'Strong B (gutt.)', 'כְּ', 'Temporal (as/when)', 'as/when he heard'],
                ['6', 'כִשְׁמֹ֨עַ',  'שמע', 'Strong B (gutt.)', 'כְּ', 'Temporal (when)', 'when he heard'],
            ]),
            ('Passage 6 — Exodus 3:8 (The Burning Bush)', [
                ['7', 'לְהַצִּיל֣וֹ', '', '', '', '', ''],
                ['8', 'לְהַעֲלֹת֤וֹ', '', '', '', '', ''],
            ], [
                ['7', 'לְהַצִּיל֣וֹ', 'נצל', 'Hiphil (I-gutt.)', 'לְ', 'Purpose', 'to deliver him'],
                ['8', 'לְהַעֲלֹת֤וֹ', 'עלה', 'Hiphil (III-ה)',   'לְ', 'Purpose', 'to bring him up'],
            ]),
            ('Passage 7 — Exodus 19:1 (Arrival at Sinai)', [
                ['9', 'לְצֵ֥את', '', '', '', '', ''],
            ], [
                ['9', 'לְצֵ֥את', 'יצא', 'I-י + III-א', 'לְ', 'Epexegetical/Temporal', 'after the going out of'],
            ]),
            ('Passage 8 — Deuteronomy 6:18 (Land Possession)', [
                ['10', 'לְמַ֣עַן + יִיטַב', '', '', '', '', ''],
            ], [
                ['10', 'לְמַ֣עַן + יִיטַב', '—', '—', 'לְמַעַן', 'Purpose', 'NOT IC — purpose particle + finite verb'],
            ]),
            ('Passage 9 — Ecclesiastes 3:1–2 (A Time for Everything)', [
                ['11', 'לָלֶ֖דֶת',  '', '', '', '', ''],
                ['12', 'לָמ֑וּת',   '', '', '', '', ''],
                ['13', 'לִנְטֹ֙עַ֙', '', '', '', '', ''],
                ['14', 'לַעֲק֔וֹר', '', '', '', '', ''],
            ], [
                ['11', 'לָלֶ֖דֶת',  'ילד', 'I-י',               'לְ', 'Epexegetical', 'to be born'],
                ['12', 'לָמ֑וּת',   'מות', 'Biconsonantal',      'לְ', 'Epexegetical', 'to die'],
                ['13', 'לִנְטֹ֙עַ֙', 'נטע', 'Strong B (gutt. R3)','לְ', 'Epexegetical', 'to plant'],
                ['14', 'לַעֲק֔וֹר', 'עקר', 'I-gutt.',            'לְ', 'Epexegetical', 'to uproot'],
            ]),
            ('Passage 10 — Genesis 45:4–5 (Joseph Reveals Himself)', [
                ['15', 'לְמָכְרֵ֥נִי', '', '', '', '', ''],
                ['16', 'לְמִחְיָ֔ה',  '', '', '', '', ''],
            ], [
                ['15', 'לְמָכְרֵ֥נִי', 'מכר', 'Strong A', 'לְ', 'Purpose', 'to sell me'],
                ['16', 'לְמִחְיָ֔ה',  'חיה', 'III-ה',    'לְ', 'Purpose', 'for preservation of life'],
            ]),
        ]

        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=False)
            self.add_section_break()

        self.add_section_heading('Answer Key')
        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)
            self.add_section_break()


def build_ch20_passage_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch20', 'exercises',
                               'ch20-passage-exercise')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'ch20-passage-exercise.pdf')
    ex = Ch20PassageExercise(
        title='Chapter 20 — Passage Exercise: Qal Infinitive Construct in Context',
        subtitle='BBH Chapter 20',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Ch21 — Qal Infinitive Absolute
# ---------------------------------------------------------------------------

class Ch21ParsingDrillExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form: (a) Identify as IA, IC, Imperative, Imperfect, or '
            'Perfect — briefly explain how you know; (b) Root; (c) Root class; '
            '(d) Function if IA (Emphatic / Imperatival / Manner / Progressive).'
        )

        # Part A — Emphatic Pairs (1–8)
        hdrA = ['#', 'Form Pair', 'Which is IA?', 'Root', 'Root Class',
                'Function', 'Gloss']
        crA  = [0.05, 0.20, 0.12, 0.09, 0.12, 0.12, 0.30]
        rowsA = [
            ['1', 'מ֥וֹת — תָּמוּת',         '', '', '', '', ''],
            ['2', 'אָכֹ֥ל — תֹּאכֵֽל',       '', '', '', '', ''],
            ['3', 'שָׁמ֣וֹעַ — תִּשְׁמָע',   '', '', '', '', ''],
            ['4', 'שָׁמ֣וֹר — תִּשְׁמְרוּן', '', '', '', '', ''],
            ['5', 'רָאֹ֣ה — רָאִ֛יתִי',      '', '', '', '', ''],
            ['6', 'טָרֹ֥ף — טֹרַ֖ף',         '', '', '', '', ''],
            ['7', 'נָת֤וֹן — יִנָּתֵן',       '', '', '', '', ''],
            ['8', 'אָבֹ֖ד — תֹּאבֵדוּן',     '', '', '', '', ''],
        ]
        ansA = [
            ['1', 'מ֥וֹת — תָּמוּת',         'מ֥וֹת', 'מות', 'Biconsonantal', 'Emphatic', 'you shall surely die'],
            ['2', 'אָכֹ֥ל — תֹּאכֵֽל',       'אָכֹ֥ל', 'אכל', 'I-aleph',     'Emphatic', 'you may freely eat'],
            ['3', 'שָׁמ֣וֹעַ — תִּשְׁמָע',   'שָׁמ֣וֹעַ', 'שמע', 'Strong B (gutt.)', 'Emphatic', 'hear attentively'],
            ['4', 'שָׁמ֣וֹר — תִּשְׁמְרוּן', 'שָׁמ֣וֹר', 'שמר', 'Strong A',   'Emphatic', 'carefully keep'],
            ['5', 'רָאֹ֣ה — רָאִ֛יתִי',      'רָאֹ֣ה', 'ראה', 'III-ה',       'Emphatic', 'I have surely seen'],
            ['6', 'טָרֹ֥ף — טֹרַ֖ף',         'טָרֹ֥ף', 'טרף', 'Strong A',    'Emphatic', 'he has surely been torn'],
            ['7', 'נָת֤וֹן — יִנָּתֵן',       'נָת֤וֹן', 'נתן', 'I-נ',        'Emphatic', 'it shall certainly be given'],
            ['8', 'אָבֹ֖ד — תֹּאבֵדוּן',     'אָבֹ֖ד', 'אבד', 'Strong A',    'Emphatic', 'you shall utterly perish'],
        ]
        self.add_section_heading('Part A — Emphatic Pairs: IA + Finite Verb (1–8)')
        self.add_generic_table(hdrA, rowsA, crA, heb_cols=[1, 2],
                               show_answers=False)
        self.add_section_break()

        # Part B — Standalone IA Forms (9–14)
        hdrB = ['#', 'Form', 'IA or other?', 'Root', 'Root Class', 'Function']
        crB  = [0.05, 0.13, 0.13, 0.09, 0.12, 0.48]
        rowsB = [
            ['9',  'זָכ֕וֹר', '', '', '', ''],
            ['10', 'שָׁמ֗וֹר', '', '', '', ''],
            ['11', 'הָל֣וֹךְ', '', '', '', ''],
            ['12', 'יָצוֹא֙', '', '', '', ''],
            ['13', 'הָי֧וֹ',  '', '', '', ''],
            ['14', 'גָּאֹ֖ל', '', '', '', ''],
        ]
        ansB = [
            ['9',  'זָכ֕וֹר', 'IA', 'זכר', 'Strong A',    'Imperatival'],
            ['10', 'שָׁמ֗וֹר', 'IA', 'שמר', 'Strong A',    'Imperatival'],
            ['11', 'הָל֣וֹךְ', 'IA', 'הלך', 'I-י',         'Manner/Progressive'],
            ['12', 'יָצוֹא֙', 'IA', 'יצא', 'I-י + III-א', 'Emphatic/Manner'],
            ['13', 'הָי֧וֹ',  'IA', 'היה', 'III-ה',        'Emphatic/Verbal noun'],
            ['14', 'גָּאֹ֖ל', 'IA', 'גאל', 'Strong A',     'Emphatic'],
        ]
        self.add_section_heading('Part B — Standalone IA Forms (9–14)')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part C — Discrimination (15–25)
        hdrC = ['#', 'Form', 'Context given?', 'Identification', 'Root', 'Notes']
        crC  = [0.05, 0.11, 0.18, 0.16, 0.09, 0.41]
        rowsC = [
            ['15', 'מ֥וֹת',    'preceded by לָ',          '', '', ''],
            ['16', 'מ֥וֹת',    'followed by תָּמוּת',     '', '', ''],
            ['17', 'שָׁמ֣וֹר', 'no context',               '', '', ''],
            ['18', 'שְׁמֹר',   'no context',               '', '', ''],
            ['19', 'שָׁמַ֣ר',  'no context',               '', '', ''],
            ['20', 'יִשְׁמֹ֣ר', 'no context',              '', '', ''],
            ['21', 'זָכ֕וֹר',  'imperatival context',      '', '', ''],
            ['22', 'לִ/זְכֹר', 'preceded by כִּי',        '', '', ''],
            ['23', 'לֶ/כֶת',   'no context',               '', '', ''],
            ['24', 'הָל֣וֹךְ', 'followed by וָ/שׁ֑וֹב',  '', '', ''],
            ['25', 'הָלַ֥ךְ',  'no context',               '', '', ''],
        ]
        ansC = [
            ['15', 'מ֥וֹת',    'preceded by לָ',         'IC', 'מות', 'Preposition לָ marks IC; not IA'],
            ['16', 'מ֥וֹת',    'followed by תָּמוּת',    'IA', 'מות', 'No prep; paired with finite verb = emphatic IA'],
            ['17', 'שָׁמ֣וֹר', 'no context',              'IA', 'שמר', 'Qamets under R1 = IA; IC/Imper. would have shewa'],
            ['18', 'שְׁמֹר',   'no context',              'IC or Imper.', 'שמר', 'Shewa under R1 = IC or Imperative 2ms; ambiguous'],
            ['19', 'שָׁמַ֣ר',  'no context',              'Perfect 3ms', 'שמר', 'Qamets + patach = Qal Perfect 3ms'],
            ['20', 'יִשְׁמֹ֣ר', 'no context',             'Imperfect 3ms', 'שמר', 'יִ prefix = Imperfect'],
            ['21', 'זָכ֕וֹר',  'imperatival context',     'Imperatival IA', 'זכר', 'Qamets + holem-waw; stands alone as command'],
            ['22', 'לִ/זְכֹר', 'preceded by כִּי',       'IC', 'זכר', 'לִ prefix = IC; shewa under ז'],
            ['23', 'לֶ/כֶת',   'no context',              'IC', 'הלך', 'I-י contracted IC; IA would be הָל֣וֹךְ'],
            ['24', 'הָל֣וֹךְ', 'followed by וָ/שׁ֑וֹב', 'IA (Manner)', 'הלך', 'Paired IAs describe progressive action'],
            ['25', 'הָלַ֥ךְ',  'no context',              'Perfect 3ms', 'הלך', 'Qamets + patach; IA is הָל֣וֹךְ (holem-waw)'],
        ]
        self.add_section_heading('Part C — Discrimination: IA, IC, Imperative, Imperfect, or Perfect (15–25)')
        self.add_generic_table(hdrC, rowsC, crC, heb_cols=[1],
                               show_answers=False)

        # Answer key
        self.add_section_break()
        self.add_section_heading('Answer Key — Part A')
        self.add_generic_table(hdrA, rowsA, crA, heb_cols=[1, 2],
                               show_answers=True, answer_rows=ansA)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=True, answer_rows=ansB)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part C')
        self.add_generic_table(hdrC, rowsC, crC, heb_cols=[1],
                               show_answers=True, answer_rows=ansC)


def build_ch21_parsing_drill(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch21', 'exercises',
                               'ch21-parsing-drill')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'ch21-parsing-drill.pdf')
    ex = Ch21ParsingDrillExercise(
        title='Chapter 21 — Parsing Drill: Qal Infinitive Absolute',
        subtitle='BBH Chapter 21',
    )
    return ex.save(path)


class Ch21PassageExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each highlighted IA form: (a) Root, (b) Root class, '
            '(c) Function (Emphatic / Imperatival / Manner / Progressive), '
            '(d) Full gloss of the construction.'
        )
        hdr = ['#', 'Form', 'Root', 'Root Class', 'Function', 'Gloss']
        cr  = [0.05, 0.16, 0.09, 0.12, 0.14, 0.44]

        passages = [
            ('Passage 1 — Genesis 2:16–17 (Permission and Prohibition)', [
                ['1', 'אָכֹ֥ל (in אָכֹ֥ל תֹּאכֵֽל)',  '', '', '', ''],
                ['2', 'מ֥וֹת (in מ֥וֹת תָּמוּת)',       '', '', '', ''],
            ], [
                ['1', 'אָכֹ֥ל', 'אכל', 'I-aleph',     'Emphatic', 'you may freely eat'],
                ['2', 'מ֥וֹת',  'מות', 'Biconsonantal', 'Emphatic', 'you shall surely die'],
            ]),
            ('Passage 2 — Exodus 3:7 (The Burning Bush)', [
                ['3', 'רָאֹ֣ה (in רָאֹ֣ה רָאִ֛יתִי)', '', '', '', ''],
            ], [
                ['3', 'רָאֹ֣ה', 'ראה', 'III-ה', 'Emphatic', 'I have surely seen'],
            ]),
            ('Passage 3 — Exodus 20:8 and Deuteronomy 5:12 (Sabbath)', [
                ['4', 'זָכ֕וֹר', '', '', '', ''],
                ['5', 'שָׁמ֗וֹר', '', '', '', ''],
            ], [
                ['4', 'זָכ֕וֹר', 'זכר', 'Strong A', 'Imperatival', 'Remember!'],
                ['5', 'שָׁמ֗וֹר', 'שמר', 'Strong A', 'Imperatival', 'Keep/Observe!'],
            ]),
            ('Passage 4 — Genesis 8:3, 5 (Flood Waters Recede)', [
                ['6', 'הָל֣וֹךְ (Gen 8:3)',  '', '', '', ''],
                ['7', 'וָ/שׁ֑וֹב',          '', '', '', ''],
                ['8', 'הָל֣וֹךְ (Gen 8:5)',  '', '', '', ''],
                ['9', 'וְ/חָס֔וֹר',         '', '', '', ''],
            ], [
                ['6', 'הָל֣וֹךְ', 'הלך', 'I-י',     'Manner/Progressive', 'going'],
                ['7', 'וָ/שׁ֑וֹב', 'שוב', 'Biconsonantal', 'Manner',          'returning'],
                ['8', 'הָל֣וֹךְ', 'הלך', 'I-י',     'Progressive',       'going'],
                ['9', 'וְ/חָס֔וֹר', 'חסר', 'Strong A',    'Progressive',       'decreasing'],
            ]),
            ('Passage 5 — Genesis 26:13 (Isaac\'s Prosperity)', [
                ['10', 'הָלוֹךְ֙',   '', '', '', ''],
                ['11', 'וְ/גָדֵ֔ל', '', '', '', ''],
            ], [
                ['10', 'הָלוֹךְ֙',   'הלך', 'I-י',     'Progressive', 'going/growing'],
                ['11', 'וְ/גָדֵ֔ל', 'גדל', 'Strong A', 'Progressive', 'growing greater'],
            ]),
            ('Passage 6 — Genesis 44:28 (Jacob on Joseph)', [
                ['12', 'טָרֹ֥ף (in טָרֹ֥ף טֹרַ֖ף)', '', '', '', ''],
            ], [
                ['12', 'טָרֹ֥ף', 'טרף', 'Strong A', 'Emphatic', 'he has surely been torn'],
            ]),
            ('Passage 7 — Deuteronomy 6:17 (Covenant Obedience)', [
                ['13', 'שָׁמ֣וֹר (in שָׁמ֣וֹר תִּשְׁמְר֗וּן)', '', '', '', ''],
            ], [
                ['13', 'שָׁמ֣וֹר', 'שמר', 'Strong A', 'Emphatic', 'diligently keep'],
            ]),
            ('Passage 8 — Deuteronomy 8:19 (Warning)', [
                ['14', 'שָׁכֹ֤חַ (in שָׁכֹ֤חַ תִּשְׁכַּח֙)', '', '', '', ''],
            ], [
                ['14', 'שָׁכֹ֤חַ', 'שכח', 'Strong B (gutt. R3)', 'Emphatic', 'ever forget'],
            ]),
            ('Passage 9 — Numbers 15:35 (Death Penalty Formula)', [
                ['15', 'מ֥וֹת (in מ֥וֹת יוּמַ֖ת)', '', '', '', ''],
            ], [
                ['15', 'מ֥וֹת', 'מות', 'Biconsonantal', 'Emphatic', 'shall surely be put to death'],
            ]),
        ]

        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=False)
            self.add_section_break()

        self.add_section_heading('Answer Key')
        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)
            self.add_section_break()


def build_ch21_passage_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch21', 'exercises',
                               'ch21-passage-exercise')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'ch21-passage-exercise.pdf')
    ex = Ch21PassageExercise(
        title='Chapter 21 — Passage Exercise: Qal Infinitive Absolute in Context',
        subtitle='BBH Chapter 21',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Ch22 — Qal Participle (Active and Passive)
# ---------------------------------------------------------------------------

class Ch22ParsingDrillExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each form: (a) Active or Passive participle (or other form), '
            '(b) Root, (c) Root class, (d) Gender and Number, '
            '(e) Function (Attributive / Predicate / Substantive / '
            'Progressive / Occupational / Resultant state).'
        )

        # Part A — Active Participle, Strong Roots (1–8)
        hdrAC = ['#', 'Form', 'Act. or Pass.?', 'Root', 'Root Class',
                 'Gender/Number', 'Function']
        crAC  = [0.05, 0.14, 0.12, 0.09, 0.12, 0.12, 0.36]
        rowsA = [
            ['1', 'שֹׁמֵ֖ר',    '', '', '', '', ''],
            ['2', 'שֹׁמֶ֫רֶת',  '', '', '', '', ''],
            ['3', 'שֹׁמְרִ֖ים', '', '', '', '', ''],
            ['4', 'הַ/שֹּׁמֵ֖ר', '', '', '', '', ''],
            ['5', 'שֹׁמֵ֣עַ',   '', '', '', '', ''],
            ['6', 'שֹׁמְעִ֖ים', '', '', '', '', ''],
            ['7', 'עֹמֵ֖ד',     '', '', '', '', ''],
            ['8', 'עֹבֵ֖ר',     '', '', '', '', ''],
        ]
        ansA = [
            ['1', 'שֹׁמֵ֖ר',    'Active', 'שמר', 'Strong A',     'ms', 'Substantive/Predicate'],
            ['2', 'שֹׁמֶ֫רֶת',  'Active', 'שמר', 'Strong A',     'fs', 'Attributive or Substantive'],
            ['3', 'שֹׁמְרִ֖ים', 'Active', 'שמר', 'Strong A',     'mp', 'Substantive/Attributive'],
            ['4', 'הַ/שֹּׁמֵ֖ר', 'Active', 'שמר', 'Strong A',    'ms', 'Substantive with def. article'],
            ['5', 'שֹׁמֵ֣עַ',   'Active', 'שמע', 'Strong B (gutt.)', 'ms', 'Substantive/Predicate'],
            ['6', 'שֹׁמְעִ֖ים', 'Active', 'שמע', 'Strong B',    'mp', 'Attributive/Substantive'],
            ['7', 'עֹמֵ֖ד',     'Active', 'עמד', 'I-gutt.',      'ms', 'Predicate/Substantive'],
            ['8', 'עֹבֵ֖ר',     'Active', 'עבר', 'Strong A',     'ms', 'Substantive'],
        ]
        self.add_section_heading('Part A — Active Participle, Strong Roots (1–8)')
        self.add_generic_table(hdrAC, rowsA, crAC, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part B — Active Participle, Weak Roots (9–16): no Act./Pass. col
        hdrB = ['#', 'Form', 'Root', 'Root Class', 'Gender/Number', 'Function']
        crB  = [0.05, 0.14, 0.09, 0.14, 0.12, 0.46]
        rowsB = [
            ['9',  'עֹשֶׂ֖ה',   '', '', '', ''],
            ['10', 'עֹשִׂ֖ים',  '', '', '', ''],
            ['11', 'יוֹשֵׁ֖ב', '', '', '', ''],
            ['12', 'בָ֖א',      '', '', '', ''],
            ['13', 'מֵ֖ת',      '', '', '', ''],
            ['14', 'נֹתֵ֥ן',    '', '', '', ''],
            ['15', 'הוֹלֵ֣ךְ', '', '', '', ''],
            ['16', 'גֹּאֵ֣ל',  '', '', '', ''],
        ]
        ansB = [
            ['9',  'עֹשֶׂ֖ה',   'עשה', 'III-ה',    'ms', 'Substantive'],
            ['10', 'עֹשִׂ֖ים',  'עשה', 'III-ה',    'mp', 'Substantive/Attributive'],
            ['11', 'יוֹשֵׁ֖ב', 'ישב', 'I-י',       'ms', 'Occupational/Predicate'],
            ['12', 'בָ֖א',      'בוא', 'Biconsonantal', 'ms', 'Substantive/Predicate'],
            ['13', 'מֵ֖ת',      'מות', 'Biconsonantal', 'ms', 'Predicate/Substantive'],
            ['14', 'נֹתֵ֥ן',    'נתן', 'I-נ',       'ms', 'Substantive'],
            ['15', 'הוֹלֵ֣ךְ', 'הלך', 'I-י',       'ms', 'Predicate/Progressive'],
            ['16', 'גֹּאֵ֣ל',  'גאל', 'Strong A',  'ms', 'Substantive'],
        ]
        self.add_section_heading('Part B — Active Participle, Weak Roots (9–16)')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part C — Passive Participle (17–23)
        rowsC = [
            ['17', 'בָּר֥וּךְ',   '', '', '', '', ''],
            ['18', 'אָר֕וּר',    '', '', '', '', ''],
            ['19', 'כָּת֥וּב',   '', '', '', '', ''],
            ['20', 'בְּרוּכָ֥ה', '', '', '', '', ''],
            ['21', 'כְּתוּבִ֥ים', '', '', '', '', ''],
            ['22', 'נְטוּיָ֖ה',  '', '', '', '', ''],
            ['23', 'בְּלוּלָ֥ה', '', '', '', '', ''],
        ]
        ansC = [
            ['17', 'בָּר֥וּךְ',   'Passive', 'ברך', 'Strong A', 'ms', 'Predicate'],
            ['18', 'אָר֕וּר',    'Passive', 'ארר', 'Geminate',  'ms', 'Predicate'],
            ['19', 'כָּת֥וּב',   'Passive', 'כתב', 'Strong A', 'ms', 'Predicate/Attributive'],
            ['20', 'בְּרוּכָ֥ה', 'Passive', 'ברך', 'Strong A', 'fs', 'Predicate/Attributive'],
            ['21', 'כְּתוּבִ֥ים', 'Passive', 'כתב', 'Strong A', 'mp', 'Attributive'],
            ['22', 'נְטוּיָ֖ה',  'Passive', 'נטה', 'III-ה',    'fs', 'Attributive'],
            ['23', 'בְּלוּלָ֥ה', 'Passive', 'בלל', 'Geminate',  'fs', 'Attributive'],
        ]
        self.add_section_heading('Part C — Passive Participle (17–23)')
        self.add_generic_table(hdrAC, rowsC, crAC, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part D — Discrimination (24–32)
        hdrD = ['#', 'Form', 'Identification', 'Root', 'Notes']
        crD  = [0.05, 0.12, 0.22, 0.09, 0.52]
        rowsD = [
            ['24', 'שֹׁמֵ֖ר',  '', '', ''],
            ['25', 'שָׁמַ֣ר',  '', '', ''],
            ['26', 'יִשְׁמֹ֣ר', '', '', ''],
            ['27', 'שָׁמ֥וּר',  '', '', ''],
            ['28', 'שְׁמֹר',   '', '', ''],
            ['29', 'שָׁמ֣וֹר', '', '', ''],
            ['30', 'בָ֖א',     '', '', ''],
            ['31', 'לָ/בֹא',   '', '', ''],
            ['32', 'יִ/יְשֵׁ֣ב', '', '', ''],
        ]
        ansD = [
            ['24', 'שֹׁמֵ֖ר',  'Qal Active Ptc. ms',         'שמר', 'Holem-waw + tsere'],
            ['25', 'שָׁמַ֣ר',  'Qal Perfect 3ms',             'שמר', 'Qamets + patach'],
            ['26', 'יִשְׁמֹ֣ר', 'Qal Imperfect 3ms',          'שמר', 'יִ prefix'],
            ['27', 'שָׁמ֥וּר',  'Qal Passive Ptc. ms',        'שמר', 'Qamets + shureq (qatûl)'],
            ['28', 'שְׁמֹר',   'Qal IC or Imper. 2ms',        'שמר', 'Shewa + holem; ambiguous'],
            ['29', 'שָׁמ֣וֹר', 'Qal IA',                      'שמר', 'Qamets + holem-waw'],
            ['30', 'בָ֖א',     'Active Ptc. ms or Perfect 3ms','בוא', 'Biconsonantal; context decides'],
            ['31', 'לָ/בֹא',   'Qal IC',                      'בוא', 'לָ prefix = IC'],
            ['32', 'יִ/יְשֵׁ֣ב', 'Qal Imperfect 3ms',         'ישב', 'יִ prefix; ptc. would be יוֹשֵׁ֖ב'],
        ]
        self.add_section_heading('Part D — Discrimination (24–32)')
        self.add_generic_table(hdrD, rowsD, crD, heb_cols=[1],
                               show_answers=False)

        # Answer key
        self.add_section_break()
        self.add_section_heading('Answer Key — Part A')
        self.add_generic_table(hdrAC, rowsA, crAC, heb_cols=[1],
                               show_answers=True, answer_rows=ansA)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=True, answer_rows=ansB)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part C')
        self.add_generic_table(hdrAC, rowsC, crAC, heb_cols=[1],
                               show_answers=True, answer_rows=ansC)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part D')
        self.add_generic_table(hdrD, rowsD, crD, heb_cols=[1],
                               show_answers=True, answer_rows=ansD)


def build_ch22_parsing_drill(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch22', 'exercises',
                               'ch22-parsing-drill')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'ch22-parsing-drill.pdf')
    ex = Ch22ParsingDrillExercise(
        title='Chapter 22 — Parsing Drill: Qal Participle (Active and Passive)',
        subtitle='BBH Chapter 22',
    )
    return ex.save(path)


class Ch22PassageExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each highlighted participle: (a) Active or Passive, '
            '(b) Root, (c) Root class, (d) Gender/Number, '
            '(e) Syntactic function (Attributive / Predicate / Substantive / '
            'Progressive / Occupational / Resultant state), (f) Gloss.'
        )
        hdr = ['#', 'Form', 'Act./Pass.', 'Root', 'Root Class',
               'G/N', 'Function', 'Gloss']
        cr  = [0.05, 0.13, 0.09, 0.08, 0.11, 0.06, 0.13, 0.35]

        passages = [
            ('Passage 1 — Genesis 3:14 and 4:11 (Curse Formulas)', [
                ['1', 'אָר֤וּר (Gen 3:14)', '', '', '', '', '', ''],
                ['2', 'אָר֤וּר (Gen 4:11)', '', '', '', '', '', ''],
            ], [
                ['1', 'אָר֤וּר', 'Passive', 'ארר', 'Geminate', 'ms', 'Predicate', 'you are cursed'],
                ['2', 'אָר֤וּר', 'Passive', 'ארר', 'Geminate', 'ms', 'Predicate', 'cursed are you'],
            ]),
            ('Passage 2 — Genesis 14:19 and 24:27 (Blessing Formulas)', [
                ['3', 'בָּר֤וּךְ (Gen 14:19)', '', '', '', '', '', ''],
                ['4', 'בָּר֤וּךְ (Gen 24:27)', '', '', '', '', '', ''],
            ], [
                ['3', 'בָּר֤וּךְ', 'Passive', 'ברך', 'Strong A', 'ms', 'Predicate', 'blessed is Abram'],
                ['4', 'בָּר֤וּךְ', 'Passive', 'ברך', 'Strong A', 'ms', 'Predicate', 'blessed is the LORD'],
            ]),
            ('Passage 3 — Genesis 18:1 (Abraham at the Tent)', [
                ['5', 'יֹשֵׁ֤ב', '', '', '', '', '', ''],
            ], [
                ['5', 'יֹשֵׁ֤ב', 'Active', 'ישב', 'I-י', 'ms', 'Predicate (circumstantial)', 'sitting'],
            ]),
            ('Passage 4 — Genesis 4:9 (Am I My Brother\'s Keeper?)', [
                ['6', 'שֹׁמֵ֥ר', '', '', '', '', '', ''],
            ], [
                ['6', 'שֹׁמֵ֥ר', 'Active', 'שמר', 'Strong A', 'ms', 'Substantive', 'keeper'],
            ]),
            ('Passage 5 — Exodus 3:2 (The Burning Bush)', [
                ['7', 'בֹּעֵ֣ר', '', '', '', '', '', ''],
            ], [
                ['7', 'בֹּעֵ֣ר', 'Active', 'בער', 'Strong A', 'ms', 'Predicate (attributive)', 'burning'],
            ]),
            ('Passage 6 — Exodus 6:6 (Outstretched Arm)', [
                ['8', 'נְטוּיָ֖ה', '', '', '', '', '', ''],
            ], [
                ['8', 'נְטוּיָ֖ה', 'Passive', 'נטה', 'III-ה', 'fs', 'Attributive', 'outstretched'],
            ]),
            ('Passage 7 — Deuteronomy 9:10 (Tablets Written by God)', [
                ['9', 'כְּתֻבִ֣ים', '', '', '', '', '', ''],
            ], [
                ['9', 'כְּתֻבִ֣ים', 'Passive', 'כתב', 'Strong A', 'mp', 'Attributive', 'written'],
            ]),
            ('Passage 9 — Leviticus 2:4–5 (Grain Offering)', [
                ['10', 'בְּלוּלֹ֥ת', '', '', '', '', '', ''],
            ], [
                ['10', 'בְּלוּלֹ֥ת', 'Passive', 'בלל', 'Geminate', 'fp', 'Attributive', 'mixed with oil'],
            ]),
            ('Passage 10 — Genesis 37:2 and Numbers 27:17 (Shepherd)', [
                ['11', 'רֹעֶ֩ה (Gen 37:2)',  '', '', '', '', '', ''],
                ['12', 'רֹעֶ֖ה (Num 27:17)', '', '', '', '', '', ''],
            ], [
                ['11', 'רֹעֶ֩ה', 'Active', 'רעה', 'III-ה', 'ms', 'Predicate (progressive)', 'was shepherding'],
                ['12', 'רֹעֶ֖ה', 'Active', 'רעה', 'III-ה', 'ms', 'Substantive',             'shepherd'],
            ]),
            ('Passage 11 — Leviticus 25:25 (Kinsman-Redeemer)', [
                ['13', 'גֹאֲל֔וֹ', '', '', '', '', '', ''],
            ], [
                ['13', 'גֹאֲל֔וֹ', 'Active', 'גאל', 'Strong A', 'ms + 3ms sfx', 'Substantive', 'his redeemer'],
            ]),
            ('Passage 12 — Numbers 14:14 (The LORD Among His People)', [
                ['14', 'עֹמֵ֣ד', '', '', '', '', '', ''],
            ], [
                ['14', 'עֹמֵ֣ד', 'Active', 'עמד', 'Strong A', 'ms', 'Predicate', 'standing'],
            ]),
            ('Standalone Forms', [
                ['15', 'נֹתֵ֥ן',    '', '', '', '', '', ''],
                ['16', 'יוֹשְׁבֵ֣י', '', '', '', '', '', ''],
            ], [
                ['15', 'נֹתֵ֥ן',    'Active', 'נתן', 'I-נ', 'ms',        'Substantive', 'giver / one who gives'],
                ['16', 'יוֹשְׁבֵ֣י', 'Active', 'ישב', 'I-י', 'mp const.', 'Attributive/Substantive', 'inhabitants of'],
            ]),
        ]

        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=False)
            self.add_section_break()

        self.add_section_heading('Answer Key')
        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)
            self.add_section_break()


def build_ch22_passage_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch22', 'exercises',
                               'ch22-passage-exercise')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'ch22-passage-exercise.pdf')
    ex = Ch22PassageExercise(
        title='Chapter 22 — Passage Exercise: Qal Participle (Active and Passive) in Context',
        subtitle='BBH Chapter 22',
    )
    return ex.save(path)


# ---------------------------------------------------------------------------
# Ch23 — Clause Analysis / Reading the Clause
# ---------------------------------------------------------------------------

class Ch23ClauseAnalysisExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each clause: (a) Clause type (Verbal VSO / Verbal — fronted / '
            'Verbless / Waw-disjunctive / Circumstantial), '
            '(b) Main verb and conjugation (if any), '
            '(c) Fronted element (if any) and why, '
            '(d) Full English gloss.'
        )

        # Part A — VSO Verbal Clauses (1–4)
        hdrA = ['#', 'Hebrew', 'Clause Type', 'Verb & Conjugation',
                'Subject', 'Object/Predicate', 'Gloss']
        crA  = [0.05, 0.22, 0.12, 0.15, 0.10, 0.14, 0.22]
        rowsA = [
            ['1', 'וַיִּבְרָ֨א אֱלֹהִ֤ים אֶת‑הָ/אָדָ֙ם֙ (Gen 1:27)', '', '', '', '', ''],
            ['2', 'וַיֹּ֤אמֶר יְהוָ֔ה אֶל‑מֹשֶׁ֖ה (Exo 3:7)',        '', '', '', '', ''],
            ['3', 'שָׁמְע֖וּ בְּנֵ֣י יִשְׂרָאֵ֑ל (Deu 6:4)',              '', '', '', '', ''],
            ['4', 'וַיַּ֥רְא אֱלֹהִ֖ים אֶת‑הָ/אוֹר֑ (Gen 1:4)',      '', '', '', '', ''],
        ]
        ansA = [
            ['1', 'וַיִּבְרָ֨א אֱלֹהִ֤ים …', 'Verbal VSO', 'וַיִּבְרָ֨א (Wayyiqtol Qal 3ms)', 'אֱלֹהִ֤ים', 'אֶת‑הָ/אָדָ֙ם֙', 'And God created man'],
            ['2', 'וַיֹּ֤אמֶר יְהוָ֔ה …',     'Verbal VSO', 'וַיֹּ֤אמֶר (Wayyiqtol Qal 3ms)', 'יְהוָ֔ה',    'אֶל‑מֹשֶׁ֖ה (PP)', 'And the LORD said to Moses'],
            ['3', 'שָׁמְע֖וּ בְּנֵ֣י יִשְׂרָאֵ֑ל', 'Verbal VSO', 'שָׁמְע֖וּ (Qal Imper. 2mp)', '— (addressed)', '—', 'Hear, O Israel'],
            ['4', 'וַיַּ֥רְא אֱלֹהִ֖ים …',    'Verbal VSO', 'וַיַּ֥רְא (Wayyiqtol Qal 3ms)',  'אֱלֹהִ֖ים', 'אֶת‑הָ/אוֹר֑', 'And God saw the light'],
        ]
        self.add_section_heading('Part A — Verbal Clauses: Default VSO (1–4)')
        self.add_generic_table(hdrA, rowsA, crA, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part B — Fronted Elements (5–8)
        hdrB = ['#', 'Hebrew', 'What is fronted?', 'Type of element',
                'Why fronted?', 'Gloss']
        crB  = [0.05, 0.22, 0.14, 0.12, 0.22, 0.25]
        rowsB = [
            ['5', 'הַ/יּ֖וֹם יָלַ֥דְתִּי (Psa 2:7)',                   '', '', '', ''],
            ['6', 'וְאֶל‑קַ֥יִן … לֹ֥א שָׁעָֽה (Gen 4:5)',          '', '', '', ''],
            ['7', 'אֶת‑הָ/אָ֖רֶץ הַ/זֹּ֑את אֶתֵּ֥ן … (Gen 12:7)', '', '', '', ''],
            ['8', 'בְּ/צֶ֥לֶם אֱלֹהִ֖ים בָּרָ֣א אֹת֑וֹ (Gen 1:27b)',  '', '', '', ''],
        ]
        ansB = [
            ['5', 'הַ/יּ֖וֹם יָלַ֥דְתִּי',          'הַ/יּ֖וֹם',     'Temporal adverb', 'Emphatic: Today (not another day)', 'Today I have begotten you'],
            ['6', 'וְאֶל‑קַ֥יִן … לֹ֥א שָׁעָֽה', 'אֶל‑קַ֥יִן', 'Prepositional phrase', 'Contrast: to Cain (vs. Abel)', 'But to Cain he did not pay attention'],
            ['7', 'אֶת‑הָ/אָ֖רֶץ … אֶתֵּ֥ן',  'אֶת‑הָ/אָ֖רֶץ', 'Object', 'Emphasis on object: *This land* I will give', 'This land I will give to your offspring'],
            ['8', 'בְּ/צֶ֥לֶם אֱלֹהִ֖ים …',        'בְּ/צֶ֥לֶם אֱלֹהִ֖ים', 'Prepositional phrase', 'Chiastic emphasis: the image is central', 'In the image of God he created him'],
        ]
        self.add_section_heading('Part B — Fronted Elements (5–8)')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part C — Verbless Clauses (9–12)
        hdrC = ['#', 'Hebrew', 'Subject', 'Predicate', 'Implied Copula', 'Gloss']
        crC  = [0.05, 0.26, 0.12, 0.14, 0.12, 0.31]
        rowsC = [
            ['9',  'יְהוָ֥ה אֱלֹהֵ֖ינוּ יְהוָ֥ה אֶחָֽד (Deu 6:4b)', '', '', '', ''],
            ['10', 'טוֹב֙ הָ/אוֹר֑ (Gen 1:4)',                         '', '', '', ''],
            ['11', 'אָנֹכִ֖י יְהוָ֣ה אֱלֹהֶ֑יךָ (Exo 20:2)',          '', '', '', ''],
            ['12', 'הֲ/שֹׁמֵ֥ר אָחִ֖י אָנֹֽכִי (Gen 4:9)',            '', '', '', ''],
        ]
        ansC = [
            ['9',  'יְהוָ֥ה אֱלֹהֵ֖ינוּ …', 'יְהוָ֥ה', 'אֱלֹהֵ֖ינוּ / אֶחָֽד', 'is', 'The LORD is our God; the LORD is one'],
            ['10', 'טוֹב֙ הָ/אוֹר֑',         'הָ/אוֹר',  'טוֹב (pred. adj.)',   'was', 'The light was good'],
            ['11', 'אָנֹכִ֖י יְהוָ֣ה …',     'אָנֹכִ֖י', 'יְהוָ֣ה אֱלֹהֶ֑יךָ', 'am',  'I am the LORD your God'],
            ['12', 'הֲ/שֹׁמֵ֥ר אָחִ֖י אָנֹֽכִי', 'אָנֹכִי', 'שֹׁמֵ֥ר (pred. ptc.)', 'am', 'Am I my brother\'s keeper?'],
        ]
        self.add_section_heading('Part C — Verbless Clauses (9–12)')
        self.add_generic_table(hdrC, rowsC, crC, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part D — Waw-Disjunctive and Circumstantial (13–16)
        hdrD = ['#', 'Hebrew', 'First element after וְ', 'Function',
                'Relation to main narrative', 'Gloss']
        crD  = [0.05, 0.24, 0.12, 0.11, 0.22, 0.26]
        rowsD = [
            ['13', 'וְהָ/אָ֗רֶץ הָיְתָ֥ה תֹ֙הוּ֙ (Gen 1:2)',           '', '', '', ''],
            ['14', 'וְה֗וּא יֹשֵׁ֤ב פֶּֽתַח (Gen 18:1)',                '', '', '', ''],
            ['15', 'וְהַ/נָּחָשׁ֙ הָיָ֣ה עָר֔וּם (Gen 3:1)',            '', '', '', ''],
            ['16', 'וְהוּא֙ לֹ֣א יָדַ֔ע כִּ֥י יְהוָ֖ה עָזְבֽוֹ (Jdg 16:20)', '', '', '', ''],
        ]
        ansD = [
            ['13', 'וְהָ/אָ֗רֶץ הָיְתָ֥ה …', 'הָ/אָ֗רֶץ (noun)', 'Background', 'Off-narrative; sets scene before creation', 'Now the earth was formless and empty'],
            ['14', 'וְה֗וּא יֹשֵׁ֤ב …',       'הוּא + ptc.',        'Simultaneous circumstance', 'What Abraham was doing when LORD appeared', 'while he was sitting at the entrance'],
            ['15', 'וְהַ/נָּחָשׁ֙ …',         'הַ/נָּחָשׁ (noun)', 'Background', 'Introduces serpent before dialogue', 'Now the serpent was more crafty'],
            ['16', 'וְהוּא֙ לֹ֣א יָדַ֔ע …',   'הוּא (pronoun)',     'Contrast/irony', 'Contrasts Samson\'s action with his ignorance', 'but he did not know the LORD had left him'],
        ]
        self.add_section_heading('Part D — Waw-Disjunctive and Circumstantial (13–16)')
        self.add_generic_table(hdrD, rowsD, crD, heb_cols=[1],
                               show_answers=False)
        self.add_section_break()

        # Part E — Mixed Analysis (17–20)
        hdrE = ['#', 'Hebrew', 'Clause Type', 'Special Feature', 'Gloss']
        crE  = [0.05, 0.28, 0.14, 0.26, 0.27]
        rowsE = [
            ['17', 'בְּ/רֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים … (Gen 1:1)',     '', '', ''],
            ['18', 'הִנֵּ֥ה אָנֹכִ֖י שֹׁלֵ֥חַ מַלְאָ֖ךְ (Exo 23:20)', '', '', ''],
            ['19', 'וְאָהַבְתָּ֙ אֵ֣ת יְהוָ֣ה אֱלֹהֶ֔יךָ (Deu 6:5)',  '', '', ''],
            ['20', 'כִּ֣י אֵ֤ין אֱלֹהִים֙ זוּלָ֣תִי (Deu 32:39)',     '', '', ''],
        ]
        ansE = [
            ['17', 'בְּ/רֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים …', 'Verbal — PP fronted', 'Temporal PP בְּ/רֵאשִׁ֖ית fronted; VSO follows', 'In the beginning God created the heavens and the earth'],
            ['18', 'הִנֵּ֥ה אָנֹכִ֖י שֹׁלֵ֥חַ …',       'Verbless / Presentative', 'הִנֵּה + pronoun + participle = vivid present', 'Behold, I am sending an angel before you'],
            ['19', 'וְאָהַבְתָּ֙ אֵ֣ת יְהוָ֣ה …',       'Verbal — Weqatal',       'Weqatal continues imperatival chain from שְׁמַ֖ע', 'And you shall love the LORD your God'],
            ['20', 'כִּ֣י אֵ֤ין אֱלֹהִים֙ …',            'Verbless / Existence',   'אֵין = non-existence particle; כִּי = emphatic', 'For there is no God besides me'],
        ]
        self.add_section_heading('Part E — Mixed Analysis (17–20)')
        self.add_generic_table(hdrE, rowsE, crE, heb_cols=[1],
                               show_answers=False)

        # Answer key
        self.add_section_break()
        self.add_section_heading('Answer Key — Part A')
        self.add_generic_table(hdrA, rowsA, crA, heb_cols=[1],
                               show_answers=True, answer_rows=ansA)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part B')
        self.add_generic_table(hdrB, rowsB, crB, heb_cols=[1],
                               show_answers=True, answer_rows=ansB)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part C')
        self.add_generic_table(hdrC, rowsC, crC, heb_cols=[1],
                               show_answers=True, answer_rows=ansC)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part D')
        self.add_generic_table(hdrD, rowsD, crD, heb_cols=[1],
                               show_answers=True, answer_rows=ansD)
        self.add_section_break()
        self.add_section_heading('Answer Key — Part E')
        self.add_generic_table(hdrE, rowsE, crE, heb_cols=[1],
                               show_answers=True, answer_rows=ansE)


def build_ch23_clause_analysis(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch23', 'exercises',
                               'ch23-clause-analysis')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'ch23-clause-analysis.pdf')
    ex = Ch23ClauseAnalysisExercise(
        title='Chapter 23 — Clause Analysis Drill',
        subtitle='BBH Chapter 23',
    )
    return ex.save(path)


class Ch23PassageExercise(ExercisePDF):
    def _build(self):
        self.add_instructions(
            'For each highlighted clause: (a) identify the clause type, '
            '(b) identify any fronted element and its rhetorical function, '
            '(c) state the verb and its conjugation (if any), '
            '(d) supply the English gloss.'
        )
        hdr = ['#', 'Clause', 'Clause Type', 'Fronted Element (if any)',
               'Verb & Conjugation', 'Gloss']
        cr  = [0.05, 0.24, 0.14, 0.18, 0.16, 0.23]

        passages = [
            ('Passage 1 — Genesis 1:1–4 (Creation Account)', [
                ['1', 'בְּ/רֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים … (Gen 1:1)', '', '', '', ''],
                ['2', 'וְהָ/אָ֗רֶץ הָיְתָ֥ה תֹ֙הוּ֙ וָ/בֹ֔הוּ (Gen 1:2a)', '', '', '', ''],
                ['3', 'וַיֹּ֤אמֶר אֱלֹהִ֙ים֙ (Gen 1:3)',                   '', '', '', ''],
                ['4', 'כִּי‑טוֹב (Gen 1:4b)',                           '', '', '', ''],
            ], [
                ['1', 'בְּ/רֵאשִׁ֖ית בָּרָ֣א …',   'Verbal — PP fronted',         'בְּ/רֵאשִׁ֖ית (temporal PP)', 'בָּרָ֣א — Qal Perfect 3ms', 'In the beginning God created the heavens and the earth'],
                ['2', 'וְהָ/אָ֗רֶץ הָיְתָ֥ה …',    'Waw-disjunctive (Background)', 'הָ/אָ֗רֶץ (noun)',          'הָיְתָ֥ה — Qal Perfect 3fs', 'Now the earth was formless and empty'],
                ['3', 'וַיֹּ֤אמֶר אֱלֹהִ֙ים֙',    'Verbal VSO',                   'None',                        'וַיֹּ֤אמֶר — Wayyiqtol Qal 3ms', 'And God said'],
                ['4', 'כִּי‑טוֹב',              'Verbless (כִּי embedded)',     'None',                        'None', 'that it was good'],
            ]),
            ('Passage 2 — Genesis 3:1–5 (The Serpent and Eve)', [
                ['5', 'וְהַ/נָּחָשׁ֙ הָיָ֣ה עָר֔וּם (Gen 3:1a)', '', '', '', ''],
                ['6', 'וַיֹּ֙אמֶר֙ אֶל‑הָ/אִשָּׁ֔ה (Gen 3:1b)', '', '', '', ''],
                ['7', 'לֹ֥א מ֖וֹת תְּמֻתֽוּן (Gen 3:4)',           '', '', '', ''],
            ], [
                ['5', 'וְהַ/נָּחָשׁ֙ הָיָ֣ה …',    'Waw-disjunctive (Background)', 'הַ/נָּחָשׁ (noun)',         'הָיָ֣ה — Qal Perfect 3ms', 'Now the serpent was more crafty'],
                ['6', 'וַיֹּ֙אמֶר֙ אֶל‑הָ/אִשָּׁ֔ה', 'Verbal VSO',            'None',                       'וַיֹּ֙אמֶר֙ — Wayyiqtol Qal 3ms', 'And he said to the woman'],
                ['7', 'לֹ֥א מ֖וֹת תְּמֻתֽוּן',    'Verbal — IA fronted',          'מ֖וֹת (Inf. Absolute)',      'תְּמֻתֽוּן — Qal Imperfect 2mp', 'You will not surely die'],
            ]),
            ('Passage 3 — Deuteronomy 6:4–5 (The Shema)', [
                ['8',  'שְׁמַ֖ע יִשְׂרָאֵ֑ל (Deu 6:4a)',                            '', '', '', ''],
                ['9',  'יְהוָ֥ה אֱלֹהֵ֖ינוּ יְהוָ֥ה אֶחָֽד (Deu 6:4b)',           '', '', '', ''],
                ['10', 'וְאָהַבְתָּ֙ אֵ֣ת יְהוָ֣ה אֱלֹהֶ֔יךָ (Deu 6:5)',         '', '', '', ''],
            ], [
                ['8',  'שְׁמַ֖ע יִשְׂרָאֵ֑ל',       'Verbal VSO',                  'None', 'שְׁמַ֖ע — Qal Imperative 2ms', 'Hear, O Israel'],
                ['9',  'יְהוָ֥ה אֱלֹהֵ֖ינוּ …',     'Verbless (×2)',               'None', 'None', 'The LORD is our God; the LORD is one'],
                ['10', 'וְאָהַבְתָּ֙ …',             'Verbal — Weqatal',            'None', 'וְאָהַבְתָּ֙ — Weqatal Qal 2ms', 'And you shall love the LORD your God'],
            ]),
            ('Passage 4 — Genesis 22:1–2 (The Binding of Isaac)', [
                ['11', 'וְאַבְרָהָ֖ם זָקֵ֑ן',                           '', '', '', ''],
                ['12', 'אֶת‑יִצְחָ֖ק אֲשֶׁ֣ר אָהַ֑בְתָּ (Gen 22:2b)', '', '', '', ''],
            ], [
                ['11', 'וְאַבְרָהָ֖ם זָקֵ֑ן',           'Waw-disjunctive (Background)', 'אַבְרָהָ֖ם (noun)', 'None (verbless)', 'Now Abraham was old'],
                ['12', 'אֶת‑יִצְחָ֖ק אֲשֶׁ֣ר …', 'Verbal — Object fronted',       'אֶת‑יִצְחָ֖ק (direct obj.)', 'אָהַ֑בְתָּ — Qal Perfect 2ms', 'Isaac, whom you love'],
            ]),
            ('Passage 5 — Judges 16:20 / Genesis 4:9 / Exodus 20:2 (Mixed)', [
                ['13', 'וְהוּא֙ לֹ֣א יָדַ֔ע … (Jdg 16:20)',     '', '', '', ''],
                ['14', 'הֲ/שֹׁמֵ֥ר אָחִ֖י אָנֹֽכִי (Gen 4:9b)', '', '', '', ''],
                ['15', 'אָנֹכִ֖י יְהוָ֣ה אֱלֹהֶ֑יךָ (Exo 20:2)', '', '', '', ''],
            ], [
                ['13', 'וְהוּא֙ לֹ֣א יָדַ֔ע …',     'Waw-disjunctive (Contrast)',   'הוּא (pronoun)',             'יָדַ֔ע — Qal Perfect 3ms', 'but he did not know the LORD had left him'],
                ['14', 'הֲ/שֹׁמֵ֥ר אָחִ֖י אָנֹֽכִי', 'Verbless (interrogative)',    'שֹׁמֵ֥ר (pred. ptc.) + ה interrogative', 'None (verbless)', 'Am I my brother\'s keeper?'],
                ['15', 'אָנֹכִ֖י יְהוָ֣ה אֱלֹהֶ֑יךָ', 'Verbless (identity)',        'None', 'None', 'I am the LORD your God'],
            ]),
        ]

        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=False)
            self.add_section_break()

        self.add_section_heading('Answer Key')
        for title, rows, ans in passages:
            self.add_section_heading(title)
            self.add_generic_table(hdr, rows, cr, heb_cols=[1],
                                   show_answers=True, answer_rows=ans)
            self.add_section_break()


def build_ch23_passage_exercise(out_dir: str = None) -> str:
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', 'output', 'lessons',
                               'hebrew', 'bbh', 'ch23', 'exercises',
                               'ch23-passage-exercise')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'ch23-passage-exercise.pdf')
    ex = Ch23PassageExercise(
        title='Chapter 23 — Passage Exercise: Reading the Clause in Context',
        subtitle='BBH Chapter 23',
    )
    return ex.save(path)


if __name__ == '__main__':
    # Ch1–Ch23 exercises (new)
    builders_ch1_23 = [
        build_ch1_letter_recognition,
        build_ch2_vowel_identification,
        build_ch3_syllable_division,
        build_ch4_noun_parsing,
        build_ch5_article_and_vav,
        build_ch6_preposition_parsing,
        build_ch7_adjective_usage,
        build_ch8_pronoun_identification,
        build_ch9_suffix_parsing,
        build_ch10_construct_chain,
        build_ch11_number_identification,
        build_ch12_verb_overview,
        build_ch13_parsing_drill,
        build_ch13_passage_exercise,
        build_ch14_passage_exercise,
        build_ch14_weak_form_id,
        build_ch15_parsing_drill,
        build_ch15_passage_exercise,
        build_ch16_passage_exercise,
        build_ch16_weak_form_id,
        build_ch17_parsing_drill,
        build_ch17_passage_exercise,
        build_ch18_parsing_drill,
        build_ch18_passage_exercise,
        build_ch19_parsing_drill,
        build_ch19_passage_exercise,
        build_ch20_parsing_drill,
        build_ch20_passage_exercise,
        build_ch21_parsing_drill,
        build_ch21_passage_exercise,
        build_ch22_parsing_drill,
        build_ch22_passage_exercise,
        build_ch23_clause_analysis,
        build_ch23_passage_exercise,
    ]
    for fn in builders_ch1_23:
        try:
            saved = fn()
            print(f'Saved: {saved}')
        except Exception as exc:
            print(f'ERROR in {fn.__name__}: {exc}')

    # Ch24+ exercises (existing)
    p0 = build_ch24_exercise()
    print(f'Saved: {p0}')
    p1 = build_ch24_contrast_exercise()
    print(f'Saved: {p1}')
    p2 = build_ch24_function_sort_exercise()
    print(f'Saved: {p2}')
    p3 = build_ch25_exercise()
    print(f'Saved: {p3}')
    p4 = build_ch25_weak_form_id_exercise()
    print(f'Saved: {p4}')
    p5 = build_ch26_exercise()
    print(f'Saved: {p5}')
    p6 = build_ch26_contrast_exercise()
    print(f'Saved: {p6}')
    p7 = build_ch26_function_sort_exercise()
    print(f'Saved: {p7}')
    p8 = build_ch27_exercise()
    print(f'Saved: {p8}')
    p9 = build_ch27_weak_form_id_exercise()
    print(f'Saved: {p9}')
    p10 = build_ch28_hophal_exercise()
    print(f'Saved: {p10}')
    p11 = build_ch30_exercise()
    print(f'Saved: {p11}')
    p12 = build_ch32_exercise()
    print(f'Saved: {p12}')
    p13 = build_ch33_exercise()
    print(f'Saved: {p13}')
    p12 = build_ch34_hithpael_exercise()
    print(f'Saved: {p12}')
    p13 = build_ch35_hithpael_weak_exercise()
    print(f'Saved: {p13}')
    p14 = build_ch29_hophal_weak_exercise()
    print(f'Saved: {p14}')
    p15 = build_ch31_piel_weak_exercise()
    print(f'Saved: {p15}')
