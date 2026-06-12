"""Generate HTML (and trigger PDF builds) for all BBG exercises.

For each exercise:
- Extracts question rows and answer rows from the PDF source classes in bbg.py
- Determines which columns get <select> dropdowns vs free-text <input>
- Generates HTML with column-aligned answer rows (no collapsed colspan strings)

Usage:
    python3 scripts/build_bbg_exercises.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, '.')

from src.bible_grammar.exercise_pdf import bbg as _bbg  # noqa: E402

OUT_ROOT = Path('data/lessons/bbg')

# ── Shared CSS / JS ───────────────────────────────────────────────────────────

_CSS = """
body{font-family:Georgia,serif;max-width:1000px;margin:2rem auto;padding:0 1rem;font-size:.92rem}
h1{font-size:1.3rem}h2{font-size:1rem;margin-top:1.6rem;border-bottom:1px solid #ccc;padding-bottom:.25rem}
.subtitle{color:#555;font-style:italic;margin-top:-.4rem}
.greek{font-size:1.05em}
table{width:100%;border-collapse:collapse;margin:.5rem 0}
th,td{border:1px solid #ccc;padding:.3rem .4rem;font-size:.86rem;vertical-align:middle}
th{background:#f0f0f0;font-weight:bold;white-space:nowrap}
select.pf,input.pf{width:100%;box-sizing:border-box;border:none;
font-family:inherit;font-size:.86rem;background:#fafafa;padding:2px}
select.pf:focus,input.pf:focus{outline:1px solid #888;background:#fff}
.ans-row{display:none}
.ans-row td{background:#e8f5e9!important;color:#1b5e20;font-size:.82rem}
.rev-btn{margin-top:.2rem;padding:.15rem .5rem;font-size:.8rem;cursor:pointer;
border:1px solid #999;background:#f5f5f5;border-radius:3px}
.rev-btn:hover{background:#e0e0e0}
.controls{margin:.8rem 0;display:flex;gap:.5rem;flex-wrap:wrap}
.controls button{padding:.25rem .7rem;font-size:.82rem;cursor:pointer;
border:1px solid #999;background:#f5f5f5;border-radius:3px}
.controls button:hover{background:#e0e0e0}
.instructions{background:#f9f9f9;border-left:3px solid #1a4a7a;padding:.5rem .7rem;
margin:.8rem 0;font-size:.88rem}
@media print{.controls,.rev-btn{display:none}
.pf{border-bottom:1px solid #333;background:transparent}
.ans-row{display:none!important}}
"""

_JS = """
function toggle(id){
  var r=document.getElementById(id);
  var btn=document.getElementById('b'+id);
  if(r.style.display==='table-row'){
    r.style.display='none'; if(btn)btn.textContent='▶';
  }else{
    r.style.display='table-row'; if(btn)btn.textContent='▼';
  }
}
function showAll(){
  document.querySelectorAll('.ans-row').forEach(function(r){r.style.display='table-row';});
  document.querySelectorAll('.rev-btn').forEach(function(b){b.textContent='▼';});
}
function hideAll(){
  document.querySelectorAll('.ans-row').forEach(function(r){r.style.display='none';});
  document.querySelectorAll('.rev-btn').forEach(function(b){b.textContent='▶';});
}
function clearAll(){
  document.querySelectorAll('.pf').forEach(function(f){
    if(f.tagName==='SELECT')f.value='';else f.value='';
  });
}
"""

_CONTROLS = (
    '<div class="controls">'
    '<button onclick="showAll()">Show All Answers</button>'
    '<button onclick="hideAll()">Hide All Answers</button>'
    '<button onclick="clearAll()">Clear All Inputs</button>'
    '</div>'
)

# Columns that should always be free-text (too many values or free-form)
_FREE_TEXT_COLS = {
    'form', 'lexical form', 'lexical', 'translation', 'translation note',
    'function', 'key signal', 'antecedent', 'context phrase', 'context clue',
    'name', 'sound / pronunciation', 'syllable division',
    'protasis verb (t·v·mood·p·n·lex)',
}


# ── Data extraction ───────────────────────────────────────────────────────────

class _DataCapture:
    """Mixin that captures add_greek_table calls without rendering."""

    def __init__(self) -> None:
        self._q_tables: list[dict] = []
        self._a_tables: list[dict] = []
        self._instructions: str = ''
        self._current_section: str = ''

    def add_instructions(self, text: str) -> None:
        self._instructions = text

    def add_section_heading(self, title: str) -> None:
        self._current_section = title

    def add_note(self, *a: Any, **kw: Any) -> None: pass
    def add_reflection(self, *a: Any, **kw: Any) -> None: pass
    def add_score(self, *a: Any, **kw: Any) -> None: pass
    def add_coverage_table(self, *a: Any, **kw: Any) -> None: pass
    def add_sort_table(self, *a: Any, **kw: Any) -> None: pass
    def add_contrast_table(self, *a: Any, **kw: Any) -> None: pass
    def add_answer_key_sort(self, *a: Any, **kw: Any) -> None: pass
    def add_answer_key_contrast(self, *a: Any, **kw: Any) -> None: pass

    def add_greek_table(
        self, hdrs: list, rows: list, col_ratios: list,
        greek_cols: list | None = None,
        show_answers: bool = False,
        answer_rows: list | None = None,
    ) -> None:
        entry = {
            'section': self._current_section,
            'hdrs': list(hdrs),
            'rows': [list(r) for r in rows],
            'ans': [list(r) for r in (answer_rows or [])],
            'greek_cols': list(greek_cols or []),
        }
        if not show_answers:
            self._q_tables.append(entry)
        else:
            self._a_tables.append(entry)


def _extract(cls: type) -> tuple[str, list[dict]]:
    """Run cls._build on a DataCapture instance; return (instructions, merged_tables)."""

    class Capture(_DataCapture, cls):  # type: ignore[misc]
        def _build_base(self) -> None:
            cls._build(self)  # type: ignore[attr-defined]

    cap = Capture()
    cap._build_base()

    # Merge question tables with their answer tables by index
    merged = []
    for i, qt in enumerate(cap._q_tables):
        at = cap._a_tables[i] if i < len(cap._a_tables) else {}
        merged.append({
            'section': qt['section'],
            'hdrs': qt['hdrs'],
            'rows': qt['rows'],
            'ans': at.get('ans', []),
            'greek_cols': qt['greek_cols'],
        })
    return cap._instructions, merged


# ── HTML generation ───────────────────────────────────────────────────────────

def _determine_inputs(hdrs: list[str], all_ans: list[list]) -> list[str]:
    """Return 'select:opt1|opt2|...' or 'input' for each data column."""
    data_hdrs = hdrs[2:]  # skip # and Form
    col_values: list[set] = [set() for _ in data_hdrs]

    for row in all_ans:
        vals = row[2:]  # skip # and form
        for i, v in enumerate(vals):
            if i < len(col_values):
                col_values[i].add(str(v).strip())

    result = []
    for i, h in enumerate(data_hdrs):
        if h.lower() in _FREE_TEXT_COLS:
            result.append('input')
            continue
        vals = sorted(col_values[i]) if col_values[i] else []
        # Use dropdown if 2–12 distinct values and last char doesn't look like a sentence
        if 2 <= len(vals) <= 12 and all(len(v) < 60 for v in vals):
            result.append('select:' + '|'.join(vals))
        else:
            result.append('input')
    return result


def _sel(options: list[str]) -> str:
    opts = '<option value=""></option>' + ''.join(
        f'<option value="{o}">{o}</option>' for o in options
    )
    return f'<select class="pf">{opts}</select>'


def _inp(rtl: bool = False) -> str:
    style = ' style="direction:rtl;unicode-bidi:embed;"' if rtl else ''
    return f'<input class="pf" type="text"{style}>'


def _build_table_html(
    sec: str, hdrs: list, rows: list, ans: list,
    greek_cols: list, input_specs: list,
    sec_idx: int,
) -> str:
    out = f'<h2>{sec}</h2>' if sec else ''

    out += '<table><thead><tr>'
    for h in hdrs:
        out += f'<th>{h}</th>'
    out += '<th></th></tr></thead><tbody>'

    for row in rows:
        num = row[0]
        form = row[1]
        rid = f's{sec_idx}r{num}'
        is_greek_form = 1 in greek_cols  # Form column (index 1) is Greek

        form_cell = (
            f'<td class="greek">{form}</td>' if is_greek_form
            else f'<td>{form}</td>'
        )

        # Input row
        out += f'<tr><td>{num}</td>{form_cell}'
        for spec in input_specs:
            if spec == 'input':
                out += f'<td>{_inp()}</td>'
            elif spec.startswith('select:'):
                opts = spec[7:].split('|')
                out += f'<td>{_sel(opts)}</td>'
        out += (
            f'<td><button class="rev-btn" id="b{rid}" '
            f'onclick="toggle(\'{rid}\')">&#9654;</button></td></tr>'
        )

        # Answer row — find matching answer
        ans_row = next((a for a in ans if str(a[0]) == str(num)), None)
        if ans_row:
            out += f'<tr class="ans-row" id="{rid}"><td>{num}</td>{form_cell}'
            for j, val in enumerate(ans_row[2:]):
                is_greek_val = (j + 2) in greek_cols
                style = ' style="direction:rtl;unicode-bidi:embed;"' if is_greek_val else ''
                out += f'<td{style}><strong>{val}</strong></td>'
            out += '<td></td></tr>'

    out += '</tbody></table>'
    return out


def build_exercise_html(
    title: str, subtitle: str,
    instructions: str,
    tables: list[dict],
    out_path: Path,
) -> None:
    # Collect all answers to determine dropdown options
    all_ans_combined: list[list] = []
    for t in tables:
        all_ans_combined.extend(t['ans'])

    # Determine input specs from ALL answer data
    if tables:
        hdrs = tables[0]['hdrs']
        input_specs = _determine_inputs(hdrs, all_ans_combined)
    else:
        input_specs = []

    body = ''
    if instructions:
        body += f'<div class="instructions">{instructions}</div>'
    body += _CONTROLS

    for i, t in enumerate(tables):
        body += _build_table_html(
            t['section'], t['hdrs'], t['rows'], t['ans'],
            t['greek_cols'], input_specs, i,
        )

    html = (
        f'<!DOCTYPE html><html lang="en"><head>'
        f'<meta charset="UTF-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{title}</title>'
        f'<style>{_CSS}</style></head><body>'
        f'<h1>{title}</h1>'
        f'<p class="subtitle">{subtitle}</p>'
        f'{body}'
        f'<script>{_JS}</script>'
        f'</body></html>'
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding='utf-8')
    print(f'  HTML: {out_path}')


# ── Exercise registry ─────────────────────────────────────────────────────────

EXERCISES = [
    # (cls_name, title, subtitle, ch, ex_slug, pdf_builder)
    ('BbgCh3AlphabetDrillPDF',
     'Chapter 3 — Greek Alphabet Drill',
     'BBG Chapter 3 · The Alphabet and Pronunciation',
     'ch3', 'ch3-alphabet-drill',
     _bbg.build_bbg_ch3_alphabet_drill),
    ('BbgCh4SyllableDrillPDF',
     'Chapter 4 — Syllabification Drill',
     'BBG Chapter 4 · Punctuation and Syllabification',
     'ch4', 'ch4-syllable-drill',
     _bbg.build_bbg_ch4_syllable_drill),
    ('BbgCh6NomAccParsingPDF',
     'Chapter 6 — Nominative and Accusative Parsing Drill',
     'BBG Chapter 6 · Nominative, Accusative, and the Article',
     'ch6', 'ch6-nom-acc-parsing',
     _bbg.build_bbg_ch6_nom_acc_parsing),
    ('BbgCh7GenDatParsingPDF',
     'Chapter 7 — Genitive and Dative Parsing Drill',
     'BBG Chapter 7 · Genitive and Dative',
     'ch7', 'ch7-gen-dat-parsing',
     _bbg.build_bbg_ch7_gen_dat_parsing),
    ('BbgCh7ArticleIdPDF',
     'Chapter 7 — Definite Article Identification Exercise',
     'BBG Chapter 7 · The Definite Article — Case, Number, and Gender from GNT Context',
     'ch7', 'ch7-article-id',
     _bbg.build_bbg_ch7_article_id),
    ('BbgCh8PrepositionParsingPDF',
     'Chapter 8 — Preposition Parsing Drill',
     'BBG Chapter 8 · Prepositions and εἰμί',
     'ch8', 'ch8-preposition-parsing',
     _bbg.build_bbg_ch8_preposition_parsing),
    ('BbgCh9AdjectiveParsingPDF',
     'Chapter 9 — Adjective Parsing Drill',
     'BBG Chapter 9 · Adjectives',
     'ch9', 'ch9-adjective-parsing',
     _bbg.build_bbg_ch9_adjective_parsing),
    ('BbgCh10ThirdDeclParsingPDF',
     'Chapter 10 — Third Declension Parsing Drill',
     'BBG Chapter 10 · Third Declension',
     'ch10', 'ch10-third-decl-parsing',
     _bbg.build_bbg_ch10_third_decl_parsing),
    ('BbgCh11PronounParsingPDF',
     'Chapter 11 — Personal Pronoun Parsing Drill',
     'BBG Chapter 11 · First and Second Person Pronouns',
     'ch11', 'ch11-pronoun-parsing',
     _bbg.build_bbg_ch11_pronoun_parsing),
    ('BbgCh12AutosParsingPDF',
     'Chapter 12 — αὐτός Parsing Drill',
     'BBG Chapter 12 · αὐτός',
     'ch12', 'ch12-autos-parsing',
     _bbg.build_bbg_ch12_autos_parsing),
    ('BbgCh13DemonstrativeParsingPDF',
     'Chapter 13 — Demonstrative Pronoun Parsing Drill',
     'BBG Chapter 13 · Demonstrative Pronouns/Adjectives',
     'ch13', 'ch13-demonstrative-parsing',
     _bbg.build_bbg_ch13_demonstrative_parsing),
    ('BbgCh14RelativeParsingPDF',
     'Chapter 14 — Relative Pronoun Parsing Drill',
     'BBG Chapter 14 · Relative Pronoun',
     'ch14', 'ch14-relative-parsing',
     _bbg.build_bbg_ch14_relative_parsing),
    ('BbgCh16PresentActiveParsingPDF',
     'Chapter 16 — Present Active Indicative Parsing Drill',
     'BBG Chapter 16 · Present Active Indicative',
     'ch16', 'ch16-present-active-parsing',
     _bbg.build_bbg_ch16_present_active_parsing),
    ('BbgCh17ContractVerbParsingPDF',
     'Chapter 17 — Contract Verb Parsing Drill',
     'BBG Chapter 17 · Contract Verbs',
     'ch17', 'ch17-contract-verb-parsing',
     _bbg.build_bbg_ch17_contract_verb_parsing),
    ('BbgCh18MiddlePassiveParsingPDF',
     'Chapter 18 — Present Middle/Passive Parsing Drill',
     'BBG Chapter 18 · Present Middle/Passive Indicative',
     'ch18', 'ch18-middle-passive-parsing',
     _bbg.build_bbg_ch18_middle_passive_parsing),
    ('BbgCh19FutureParsingPDF',
     'Chapter 19 — Future Active and Middle Parsing Drill',
     'BBG Chapter 19 · Future Active and Middle Indicative',
     'ch19', 'ch19-future-parsing',
     _bbg.build_bbg_ch19_future_parsing),
    ('BbgCh20StemChangeDrillPDF',
     'Chapter 20 — Verbal Root Stem Change Drill',
     'BBG Chapter 20 · Verbal Roots (Patterns 2–4)',
     'ch20', 'ch20-stem-change-drill',
     _bbg.build_bbg_ch20_stem_change_drill),
    ('BbgCh21ImperfectParsingPDF',
     'Chapter 21 — Imperfect Indicative Parsing Drill',
     'BBG Chapter 21 · Imperfect Indicative',
     'ch21', 'ch21-imperfect-parsing',
     _bbg.build_bbg_ch21_imperfect_parsing),
    ('BbgCh22SecondAoristParsingPDF',
     'Chapter 22 — Second Aorist Parsing Drill',
     'BBG Chapter 22 · Second Aorist Active and Middle Indicative',
     'ch22', 'ch22-second-aorist-parsing',
     _bbg.build_bbg_ch22_second_aorist_parsing),
    ('BbgCh22AoristContrastPDF',
     'Chapter 22 — Aorist Contrast Drill',
     'BBG Chapter 22 · First vs. Second Aorist',
     'ch22', 'ch22-aorist-contrast',
     _bbg.build_bbg_ch22_aorist_contrast),
    ('BbgCh23FirstAoristParsingPDF',
     'Chapter 23 — First Aorist Parsing Drill',
     'BBG Chapter 23 · First Aorist Active and Middle Indicative',
     'ch23', 'ch23-first-aorist-parsing',
     _bbg.build_bbg_ch23_first_aorist_parsing),
    ('BbgCh24AoristFuturePassiveParsingPDF',
     'Chapter 24 — Aorist and Future Passive Parsing Drill',
     'BBG Chapter 24 · Aorist and Future Passive Indicative',
     'ch24', 'ch24-aorist-future-passive-parsing',
     _bbg.build_bbg_ch24_aorist_future_passive_parsing),
    ('BbgCh24PassiveFormationPDF',
     'Chapter 24 — Passive Formation Drill',
     'BBG Chapter 24 · Passive Voice Formation',
     'ch24', 'ch24-passive-formation',
     _bbg.build_bbg_ch24_passive_formation),
    ('BbgCh25PerfectParsingPDF',
     'Chapter 25 — Perfect Indicative Parsing Drill',
     'BBG Chapter 25 · Perfect Indicative',
     'ch25', 'ch25-perfect-parsing',
     _bbg.build_bbg_ch25_perfect_parsing),
    ('BbgCh27PresentParticipleParsingPDF',
     'Chapter 27 — Present Adverbial Participle Parsing Drill',
     'BBG Chapter 27 · Imperfective (Present) Adverbial Participles',
     'ch27', 'ch27-present-participle-parsing',
     _bbg.build_bbg_ch27_present_participle_parsing),
    ('BbgCh27ParticipleUseSortPDF',
     'Chapter 27 — Participle Use Sorting Drill',
     'BBG Chapter 27 · Adverbial Participle Functions',
     'ch27', 'ch27-participle-use-sort',
     _bbg.build_bbg_ch27_participle_use_sort),
    ('BbgCh28AoristParticipleParsingPDF',
     'Chapter 28 — Aorist Adverbial Participle Parsing Drill',
     'BBG Chapter 28 · Perfective (Aorist) Adverbial Participles',
     'ch28', 'ch28-aorist-participle-parsing',
     _bbg.build_bbg_ch28_aorist_participle_parsing),
    ('BbgCh28ParticipleTenseContrastPDF',
     'Chapter 28 — Participle Tense Contrast Drill',
     'BBG Chapter 28 · Present vs. Aorist Participle Aspect',
     'ch28', 'ch28-participle-tense-contrast',
     _bbg.build_bbg_ch28_participle_tense_contrast),
    ('BbgCh29AdjectivalParticipleParsingPDF',
     'Chapter 29 — Adjectival Participle Parsing Drill',
     'BBG Chapter 29 · Adjectival Participles',
     'ch29', 'ch29-adjectival-participle-parsing',
     _bbg.build_bbg_ch29_adjectival_participle_parsing),
    ('BbgCh30PerfectParticipleGenAbsPDF',
     'Chapter 30 — Perfect Participles and Genitive Absolutes',
     'BBG Chapter 30 · Combinative Participles and Genitive Absolutes',
     'ch30', 'ch30-perfect-participle-genabs',
     _bbg.build_bbg_ch30_perfect_participle_genabs),
    ('BbgCh31SubjunctiveParsingPDF',
     'Chapter 31 — Subjunctive Parsing Drill',
     'BBG Chapter 31 · Subjunctive',
     'ch31', 'ch31-subjunctive-parsing',
     _bbg.build_bbg_ch31_subjunctive_parsing),
    ('BbgCh31SubjunctiveUseSortPDF',
     'Chapter 31 — Subjunctive Use Sorting Drill',
     'BBG Chapter 31 · Subjunctive Functions',
     'ch31', 'ch31-subjunctive-use-sort',
     _bbg.build_bbg_ch31_subjunctive_use_sort),
    ('BbgCh32InfinitiveParsingPDF',
     'Chapter 32 — Infinitive Parsing Drill',
     'BBG Chapter 32 · Infinitive',
     'ch32', 'ch32-infinitive-parsing',
     _bbg.build_bbg_ch32_infinitive_parsing),
    ('BbgCh33ImperativeParsingPDF',
     'Chapter 33 — Imperative Parsing Drill',
     'BBG Chapter 33 · Imperative',
     'ch33', 'ch33-imperative-parsing',
     _bbg.build_bbg_ch33_imperative_parsing),
    ('BbgCh33ProhibitionDrillPDF',
     'Chapter 33 — Prohibition Drill',
     'BBG Chapter 33 · Prohibitions (μή + Aorist/Present)',
     'ch33', 'ch33-prohibition-drill',
     _bbg.build_bbg_ch33_prohibition_drill),
    ('BbgCh34DidomiParsingPDF',
     'Chapter 34 — δίδωμι Parsing Drill',
     'BBG Chapter 34 · Indicative of δίδωμι',
     'ch34', 'ch34-didomi-parsing',
     _bbg.build_bbg_ch34_didomi_parsing),
    ('BbgCh35ConditionalsdrillPDF',
     'Chapter 35 — Conditional Sentences Drill',
     'BBG Chapter 35 · Conditional Sentences',
     'ch35', 'ch35-conditionals-drill',
     _bbg.build_bbg_ch35_conditionals_drill),
    ('BbgCh36MiVerbsParsingPDF',
     'Chapter 36 — μι-Verbs Parsing Drill',
     'BBG Chapter 36 · ἵστημι, τίθημι, δείκνυμι',
     'ch36', 'ch36-mi-verbs-parsing',
     _bbg.build_bbg_ch36_mi_verbs_parsing),
]


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    for cls_name, title, subtitle, ch, ex_slug, pdf_builder in EXERCISES:
        print(f'\n{ch}/{ex_slug}')
        cls = getattr(_bbg, cls_name)

        # Extract data
        instructions, tables = _extract(cls)

        # Build HTML
        html_path = OUT_ROOT / ch / 'exercises' / ex_slug / f'{ex_slug}.html'
        build_exercise_html(title, subtitle, instructions, tables, html_path)

        # Build PDF
        try:
            pdf_builder()
            print('  PDF: done')
        except Exception as e:
            print(f'  PDF: ERROR — {e}')

    print('\nDone.')
