from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white

from ._base import ExercisePDF, _register_fonts, C_RULE, C_FIELD_BG

# ===========================================================================
# BBG (Basics of Biblical Greek) Exercise PDF Builders
# ===========================================================================

_GREEK_FONT_REGISTERED = False


def _register_greek_fonts():
    """Register a TTF font with full Greek Unicode coverage."""
    global _GREEK_FONT_REGISTERED
    if _GREEK_FONT_REGISTERED:
        return
    # ArialHB.ttc subfontIndex=0 is the base Arial (Latin + Greek + more)
    # Fall back to Helvetica if unavailable (Greek will be missing but PDF will generate)
    import os
    candidates = [
        ('/System/Library/Fonts/ArialHB.ttc', 0),
        ('/Library/Fonts/Arial Unicode.ttf', None),
        ('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', None),
    ]
    registered = False
    for fpath, idx in candidates:
        if os.path.exists(fpath):
            try:
                if idx is not None:
                    pdfmetrics.registerFont(TTFont('GreekFont', fpath, subfontIndex=idx))
                else:
                    pdfmetrics.registerFont(TTFont('GreekFont', fpath))
                registered = True
                break
            except Exception:
                continue
    if not registered:
        # Last resort: use a built-in name alias (no Greek glyphs but PDF still generates)
        pdfmetrics.registerFont(TTFont.__new__(TTFont))  # skip — just use Helvetica alias
        # Map 'GreekFont' to Helvetica as fallback
        try:
            pdfmetrics.registerFontFamily('GreekFont', normal='Helvetica',
                                          bold='Helvetica-Bold',
                                          italic='Helvetica-Oblique')
        except Exception:
            pass
    _GREEK_FONT_REGISTERED = True


class GreekExercisePDF(ExercisePDF):
    """Base class for BBG Greek exercises. Uses GreekFont for Greek text columns."""

    # Override heading color for Greek exercises (blue instead of Hebrew green)
    def __init__(self, title: str, subtitle: str = ''):
        _register_fonts()           # Hebrew fonts (needed by base class)
        _register_greek_fonts()     # Greek font
        super().__init__(title, subtitle)

    def add_greek_table(self, headers: list, rows: list,
                        col_ratios: list = None,
                        greek_cols: list = None,
                        show_answers: bool = True,
                        answer_rows: list = None):
        """
        Draw a parse table with Greek text support.
        greek_cols: indices of columns that display Greek (rendered with GreekFont).
        Other columns behave like add_generic_table.
        """
        if col_ratios is None:
            col_ratios = [1.0 / len(headers)] * len(headers)
        if greek_cols is None:
            greek_cols = []

        w = self._usable_w()
        cw = [r * w for r in col_ratios]
        x0 = self.MARGIN_L
        answer_data = answer_rows if answer_rows is not None else rows

        needed = (self.HEADER_H
                  + len(rows) * (self.ROW_H + (self.ANSWER_H if show_answers else 0))
                  + 0.08 * inch)
        self._check_space(needed)

        c = self._canvas
        C_GRK_HEADING = HexColor('#1a4a7a')   # blue for Greek exercises

        # Header row
        y = self._y
        c.setFillColor(C_GRK_HEADING)
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.4)
        c.rect(x0, y - self.HEADER_H, sum(cw), self.HEADER_H, fill=1, stroke=1)
        cx = x0
        c.setFont('Helvetica-Bold', self.LABEL_SIZE)
        c.setFillColor(white)
        for hdr, col_w in zip(headers, cw):
            if hdr:
                c.drawString(cx + 3, y - self.HEADER_H + 5, hdr)
            cx += col_w
        y -= self.HEADER_H

        for row_idx, row in enumerate(rows):
            self._check_space(self.ROW_H + (self.ANSWER_H if show_answers else 0))

            # Input row
            row_bg = HexColor('#f0f4fa') if row_idx % 2 == 0 else white
            c.setFillColor(row_bg)
            c.setStrokeColor(C_RULE)
            c.setLineWidth(0.4)
            c.rect(x0, y - self.ROW_H, sum(cw), self.ROW_H, fill=1, stroke=1)

            cx = x0
            for col_idx, (cell, col_w) in enumerate(zip(row, cw)):
                if col_idx in greek_cols:
                    # Greek column — display text, centered, GreekFont
                    try:
                        gfont = 'GreekFont'
                        c.setFont(gfont, self.BODY_SIZE + 1)
                    except Exception:
                        c.setFont('Helvetica', self.BODY_SIZE + 1)
                    c.setFillColor(black)
                    c.drawCentredString(cx + col_w / 2, y - self.ROW_H + 7, cell)
                elif col_idx == 0:
                    # Item number column — display only
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

            # Answer row
            if show_answers:
                ans_row = answer_data[row_idx]
                ans_text = '  ·  '.join(str(v) for v in ans_row[1:] if v)
                needed_h = self.ANSWER_H
                c.setFillColor(HexColor('#e8f0fb'))
                c.setStrokeColor(C_RULE)
                c.setLineWidth(0.3)
                c.rect(x0, y - needed_h, sum(cw), needed_h, fill=1, stroke=1)
                c.setFont('Helvetica', self.LABEL_SIZE - 0.5)
                c.setFillColor(HexColor('#1a4a7a'))
                c.drawString(x0 + 4, y - needed_h + 4, ans_text)
                y -= needed_h

        self._y = y - 0.08 * inch


# ---------------------------------------------------------------------------
# BBG Ch3 — Alphabet Drill PDF
# ---------------------------------------------------------------------------
