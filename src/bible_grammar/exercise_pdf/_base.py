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
from typing import Any, List, Optional, Tuple, cast
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
UNICODE_TRANSLIT_FONT = None   # set to font name if Arial Unicode MS is available


def _register_fonts() -> None:
    global _FONTS_REGISTERED, UNICODE_TRANSLIT_FONT
    if _FONTS_REGISTERED:
        return
    pdfmetrics.registerFont(TTFont('ArialHebrew',     '/System/Library/Fonts/ArialHB.ttc', subfontIndex=2))
    pdfmetrics.registerFont(TTFont('ArialHebrewBold', '/System/Library/Fonts/ArialHB.ttc', subfontIndex=3))
    # Try to register Arial Unicode MS for transliteration columns (Latin Extended, IPA).
    # Typically installed with Microsoft Office at one of these paths.
    _arial_unicode_candidates = [
        '/Library/Fonts/Arial Unicode MS.ttf',
        os.path.expanduser('~/Library/Fonts/Arial Unicode MS.ttf'),
        '/Library/Fonts/Arial Unicode.ttf',
        '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
    ]
    for _path in _arial_unicode_candidates:
        if os.path.exists(_path):
            try:
                pdfmetrics.registerFont(TTFont('ArialUnicode', _path))
                UNICODE_TRANSLIT_FONT = 'ArialUnicode'
            except Exception:
                pass
            break
    _FONTS_REGISTERED = True


def _heb(text: str) -> str:
    """Apply bidi algorithm so ReportLab draws Hebrew glyphs left-to-right."""
    return get_display(text)


def _mixed_font(bold: bool = False) -> str:
    """Return the best available font for strings mixing Latin and Hebrew text.

    Arial Unicode covers both scripts in one font, so Latin + Hebrew can coexist
    in a single drawString call without glyph-block rendering artefacts.
    Falls back to ArialHebrew when Arial Unicode is not available (Hebrew only
    will still render; Latin will appear as glyphs from the Hebrew font).
    """
    if UNICODE_TRANSLIT_FONT:
        return UNICODE_TRANSLIT_FONT
    return 'ArialHebrewBold' if bold else 'ArialHebrew'


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

    _canvas: canvas.Canvas   # assigned in save() before any drawing method runs
    _path: Optional[str]
    _fields: List[Tuple[Any, ...]]

    def __init__(self, title: str, subtitle: str = '') -> None:
        _register_fonts()
        self.title    = title
        self.subtitle = subtitle
        self._canvas  = cast(canvas.Canvas, None)  # real value set in save()
        self._path    = None
        self._y       = 0.0
        self._page    = 0
        self._fields  = []   # (name, x, y, w, h, default_value, answer_value)
        self._field_idx = 0

    # ------------------------------------------------------------------ pages
    def _usable_w(self) -> float:
        return self.PAGE_W - self.MARGIN_L - self.MARGIN_R

    def _col_widths(self) -> List[float]:
        w = self._usable_w()
        return [r * w for r in self.COL_RATIOS]

    def _new_page(self) -> None:
        if self._page > 0:
            self._canvas.showPage()
        self._page += 1
        self._y = self.PAGE_H - self.MARGIN_T
        self._draw_header()

    def _draw_header(self) -> None:
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

    def _check_space(self, needed: float) -> None:
        if self._y - needed < self.MARGIN_B:
            self._new_page()

    # ---------------------------------------------------------------- helpers
    def _hline(self, y: float, color: Any = C_RULE, width: float = 0.5) -> None:
        self._canvas.setStrokeColor(color)
        self._canvas.setLineWidth(width)
        self._canvas.line(self.MARGIN_L, y, self.PAGE_W - self.MARGIN_R, y)

    def _wrapped_height(self, text: str, font: str, size: float, max_w: float) -> float:
        lines = simpleSplit(text, font, size, max_w)
        return len(lines) * (size + 2)

    def _draw_wrapped(self, text: str, font: str, size: float,
                       x: float, y: float, max_w: float, color: Any = black) -> float:
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
    def add_instructions(self, text: str) -> None:
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

    def add_section_heading(self, text: str) -> None:
        self._check_space(0.5 * inch)
        self._y -= 0.12 * inch
        self._canvas.setFont('Helvetica-Bold', self.HEAD_SIZE)
        self._canvas.setFillColor(C_HEADING)
        self._canvas.drawString(self.MARGIN_L, self._y, text)
        self._y -= (self.HEAD_SIZE + 4)
        self._hline(self._y + 2, color=HexColor('#aaaaaa'), width=0.75)
        self._y -= 0.08 * inch

    def add_drill_with_answer_key(self, headers: list, rows: list, answers: list,
                                   col_ratios: Optional[list] = None,
                                   heb_cols: Optional[list] = None,
                                   translit_cols: Optional[list] = None,
                                   section_title: str = 'Items 1–20',
                                   answer_title: str = 'Answer Key',
                                   greek_cols: Optional[list] = None,
                                   use_greek: bool = False,
                                   answer_heb_cols: Optional[list] = None) -> None:
        """Render a drill section followed by an answer key section."""
        if use_greek:
            self.add_section_heading(section_title)
            self.add_greek_table(headers, rows, col_ratios, greek_cols=greek_cols, show_answers=False)  # type: ignore[attr-defined]
            self.add_section_heading(answer_title)
            self.add_greek_table(headers, rows, col_ratios, greek_cols=greek_cols,  # type: ignore[attr-defined]
                                 show_answers=True, answer_rows=answers)
        else:
            self.add_section_heading(section_title)
            self.add_generic_table(headers, rows, col_ratios=col_ratios,
                                   heb_cols=heb_cols, translit_cols=translit_cols,
                                   show_answers=False)
            self.add_section_heading(answer_title)
            self.add_generic_table(headers, rows, col_ratios=col_ratios,
                                   heb_cols=heb_cols, translit_cols=translit_cols,
                                   show_answers=True, answer_rows=answers,
                                   answer_heb_cols=answer_heb_cols)

    def add_multi_part_drill(self, parts: list,
                             heb_cols: Optional[list] = None,
                             translit_cols: Optional[list] = None,
                             greek_cols: Optional[list] = None,
                             use_greek: bool = False) -> None:
        """
        Render multiple drill parts each followed by their answer key.

        parts: list of dicts with keys:
            title       — section heading string (e.g. 'Part A — Long Vowels (1–5)')
            headers     — column header list
            rows        — blank/prompt rows
            answers     — answer rows
            col_ratios  — (optional) override col_ratios for this part
            translit_cols — (optional) override translit_cols for this part
            greek_cols  — (optional) override greek_cols for this part
        """
        for part in parts:
            ptitle = part['title']
            headers = part['headers']
            rows = part['rows']
            answers = part['answers']
            cr = part.get('col_ratios', None)
            tc = part.get('translit_cols', translit_cols)
            gc = part.get('greek_cols', greek_cols)
            self.add_drill_with_answer_key(
                headers, rows, answers,
                col_ratios=cr,
                heb_cols=heb_cols,
                translit_cols=tc,
                section_title=ptitle,
                answer_title=f'{ptitle} — Answer Key',
                greek_cols=gc,
                use_greek=use_greek,
            )

    def add_section_break(self) -> None:
        self._check_space(0.3 * inch)
        self._y -= 0.12 * inch
        c = self._canvas
        c.setStrokeColor(HexColor('#cccccc'))
        c.setLineWidth(0.5)
        c.setDash(4, 4)
        c.line(self.MARGIN_L, self._y, self.PAGE_W - self.MARGIN_R, self._y)
        c.setDash()
        self._y -= 0.15 * inch

    def add_passage(self, block: PassageBlock) -> None:
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

    def add_verb_table(self, verbs: list, show_answers: bool = True) -> None:
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
                          col_ratios: Optional[list] = None,
                          heb_cols: Optional[list] = None,
                          translit_cols: Optional[list] = None,
                          show_answers: bool = True,
                          answer_rows: Optional[list] = None,
                          answer_heb_cols: Optional[list] = None) -> None:
        """
        Draw a generic parse table with arbitrary columns.

        headers: column header strings
        rows: list of row data (each row is a list of strings, same length as headers)
        col_ratios: proportional widths (must sum to ~1.0); if None, equal widths
        heb_cols: indices of columns that contain Hebrew/Aramaic text (right-aligned, ArialHebrew font)
        translit_cols: indices of columns that contain transliteration (Latin Extended / IPA).
                       Uses Arial Unicode MS if registered, otherwise falls back to Helvetica.
        show_answers: if True, draw green answer rows below each input row
        answer_rows: if show_answers, the answer data (same shape as rows); if None, answers = rows
        answer_heb_cols: additional column indices that are Hebrew only in answer rows (blank input in question row)
        """
        if col_ratios is None:
            col_ratios = [1.0 / len(headers)] * len(headers)
        if heb_cols is None:
            heb_cols = []
        if translit_cols is None:
            translit_cols = []
        if answer_heb_cols is None:
            answer_heb_cols = []
        _tlit_font = UNICODE_TRANSLIT_FONT if UNICODE_TRANSLIT_FONT else 'Helvetica'

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
                    # Hebrew/Aramaic column — display text (no field), right-aligned
                    c.setFont('ArialHebrew', self.HEB_SIZE - 2)
                    c.setFillColor(black)
                    c.drawRightString(cx + col_w - 3, y - self.ROW_H + 7, _heb(cell))
                elif col_idx == 0:
                    # First column (usually item number) — display only
                    c.setFont('Helvetica-Bold', self.LABEL_SIZE)
                    c.setFillColor(HexColor('#666666'))
                    c.drawCentredString(cx + col_w / 2, y - self.ROW_H + 8, str(cell))
                elif col_idx in translit_cols and cell:
                    # Transliteration column with content — display only (no field)
                    c.setFont(_tlit_font, self.LABEL_SIZE)
                    c.setFillColor(black)
                    c.drawString(cx + 3, y - self.ROW_H + 8, cell)
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
                    elif col_idx in heb_cols or col_idx in answer_heb_cols:
                        c.setFont('ArialHebrew', self.LABEL_SIZE)
                        c.setFillColor(C_ANSWER_FG)
                        c.drawRightString(cx + col_w - 3, y - self.ANSWER_H + 6, _heb(cell))
                    elif col_idx in translit_cols:
                        c.setFont(_tlit_font, self.LABEL_SIZE)
                        c.setFillColor(C_ANSWER_FG)
                        lines = simpleSplit(cell, _tlit_font, self.LABEL_SIZE, col_w - 6)
                        c.drawString(cx + 3, y - self.ANSWER_H + 6, lines[0] if lines else cell)
                    else:
                        c.setFont('Helvetica', self.LABEL_SIZE)
                        c.setFillColor(C_ANSWER_FG)
                        lines = simpleSplit(cell, 'Helvetica', self.LABEL_SIZE, col_w - 6)
                        c.drawString(cx + 3, y - self.ANSWER_H + 6, lines[0] if lines else cell)
                    cx += col_w

                y -= self.ANSWER_H

        self._y = y - 0.1 * inch

    def add_note(self, text: str) -> None:
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

    def add_score(self, text: str) -> None:
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

    def add_coverage_table(self, rows: list) -> None:
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

    def add_contrast_table(self, entries: list, show_answers: bool = True) -> None:
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

    def add_answer_key_contrast(self, entries: list) -> None:
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
            c.setFont(_mixed_font(), self.LABEL_SIZE)
            c.setFillColor(HexColor('#444444'))
            lines = simpleSplit(e.answer_note, _mixed_font(), self.LABEL_SIZE, cw[4] - 6)
            c.drawString(cx + 3, self._y - row_h + 6, lines[0] if lines else e.answer_note)
            self._y -= row_h

        self._y -= 0.1 * inch

    def add_answer_key_sort(self, entries: list) -> None:
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
            c.setFont(_mixed_font(), self.LABEL_SIZE)
            c.setFillColor(HexColor('#444444'))
            lines = simpleSplit(e.explanation, _mixed_font(), self.LABEL_SIZE, cw[4] - 6)
            c.drawString(cx + 3, self._y - row_h + 5, lines[0] if lines else e.explanation)
            self._y -= row_h

        self._y -= 0.1 * inch

    def add_sort_table(self, entries: list, show_answers: bool = True) -> None:
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
                lines = simpleSplit(e.explanation, _mixed_font(), self.LABEL_SIZE, cw[4] - 6)
                c.setFont(_mixed_font(), self.LABEL_SIZE)
                c.setFillColor(C_ANSWER_FG)
                c.drawString(cx + 3, y - self.ANSWER_H + 6, lines[0] if lines else e.explanation)
                cx += cw[4]
                c.setFont('Helvetica-Bold', self.LABEL_SIZE)
                c.drawString(cx + 3, y - self.ANSWER_H + 6, e.function)
                y -= self.ANSWER_H

        self._y = y - 0.08 * inch

    def add_nh_table(self, entries: list, show_answers: bool = True) -> None:
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

    def add_bg_table(self, entries: list, show_answers: bool = True) -> None:
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

    def add_reflection(self, questions: list) -> None:
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
    def save(self, path: str) -> str:
        self._path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._canvas = canvas.Canvas(path, pagesize=LETTER)
        self._canvas.setTitle(self.title)
        self._canvas.setAuthor('Berean Bible Bots')
        self._canvas.setSubject('Biblical Hebrew Passage Exercise')
        self._page = 0
        self._y = 0.0
        self._field_idx = 0
        self._new_page()
        self._build()
        self._canvas.save()
        return path

    def _build(self) -> None:
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

    def _render_passages(self, show_answers: bool) -> None:
        raise NotImplementedError('Subclass must implement _render_passages()')

    def _build(self) -> None:
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


def _build_exercise_pdf(klass: Any, title: str, subtitle: str,
                        path_parts: list, filename: str,
                        out_dir: Optional[str] = None) -> str:
    """
    Instantiate `klass(title, subtitle)`, save to the standard output path, and return the path.

    path_parts: sub-path components under output/lessons/ (e.g. ['aramaic','bba','ch1','exercises','ch1-letter-recognition'])
    filename:   PDF filename without directory (e.g. 'ch1-letter-recognition.pdf')
    """
    if out_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, '..', '..', '..', 'output', 'lessons', *path_parts)
    path = os.path.join(out_dir, filename)
    return klass(title=title, subtitle=subtitle).save(path)
