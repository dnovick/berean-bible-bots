"""Convert S. Blair's Anki .apkg decks to MD / Anki-txt / Flashcards-Deluxe formats.

Source files (temp/):
  1000 words BBH mnemonics, etc..apkg  — 1,000-word vocabulary with mnemonics
  Biblical_Hebrew_-_All_Forms_of_Qatal.apkg — 195 strong-verb paradigm cards
  Hebrew parsing exercises.apkg        — 10,399 OT verb parsing cards

Outputs (output/lessons/hebrew/bbh/sblair/):
  sblair-vocab/       — vocabulary deck (ch2–35 words, tags by chapter)
  sblair-vocab-extra/ — extended OT vocab (cards 507–1000, freq 30–69)
  sblair-paradigm/    — strong verb paradigm deck
  sblair-parsing/     — OT verb parsing deck (large; split by stem)
"""

from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path

APKG_DIR = Path('temp')
OUT_ROOT = Path('output/lessons/hebrew/bbh/sblair')
OUT_ROOT.mkdir(parents=True, exist_ok=True)


def clean(s: str) -> str:
    """Strip HTML tags and normalise whitespace."""
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', str(s))).strip()


# ── Shared helpers ─────────────────────────────────────────────────────────

def write_md(path: Path, title: str, subtitle: str, headers: list[str],
             rows: list[list[str]], note: str = '') -> None:
    lines = [
        f'# {title}', '',
        f'*{subtitle}*', '',
    ]
    if note:
        lines += [f'> {note}', '']
    lines += [
        '| ' + ' | '.join(headers) + ' |',
        '|' + '|'.join(['---'] * len(headers)) + '|',
    ]
    for r in rows:
        safe = [str(c).replace('|', '&#124;') for c in r]
        lines.append('| ' + ' | '.join(safe) + ' |')
    lines.append('')
    path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  MD : {path}')


def write_anki(path: Path, deck: str, rows: list[tuple[str, str, str]]) -> None:
    """rows = (front, back, tags)"""
    lines = [
        '#separator:tab',
        '#html:false',
        '#notetype:Basic',
        f'#deck:{deck}',
        '#tags column:3',
    ]
    for front, back, tags in rows:
        f = front.replace('\t', ' ').replace('\n', ' ')
        b = back.replace('\t', ' ').replace('\n', ' ')
        lines.append(f'{f}\t{b}\t{tags}')
    path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  Anki: {path}')


def write_fd(path: Path, deck: str, rows: list[tuple[str, str]]) -> None:
    """rows = (front, back)"""
    lines = [f'{f.replace(chr(9), " ")}\t{b.replace(chr(9), " ")}\t{deck}'
             for f, b in rows]
    path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  FD  : {path}')


# ── Deck 1a: BBH chapter vocabulary (ch2–35) ─────────────────────────────

def convert_vocab_ch() -> None:
    print('\n=== Deck 1a: BBH Vocab by Chapter ===')
    out = OUT_ROOT / 'sblair-vocab'
    out.mkdir(exist_ok=True)

    con = sqlite3.connect(
        '/tmp/anki_extract/1000 words BBH mnemonics, etc./collection.anki21')

    words: list[tuple] = []
    for row in con.execute('SELECT flds FROM notes'):
        f = row[0].split('\x1f')
        num  = clean(f[0]) if len(f) > 0 else ''
        heb  = clean(f[1]) if len(f) > 1 else ''
        eng  = clean(f[2]) if len(f) > 2 else ''
        freq = clean(f[4]) if len(f) > 4 else ''
        ch   = clean(f[5]) if len(f) > 5 else ''
        root = clean(f[6]) if len(f) > 6 else ''
        if not ch:
            continue
        ch_n = ch.replace('Ch ', '').strip()
        words.append((int(ch_n), int(num) if num.isdigit() else 0,
                      heb, eng, freq, root, ch_n))
    con.close()

    words.sort(key=lambda x: (x[0], x[1]))

    # MD
    md_rows = [[w[2], w[3], w[5] or '—', w[4], f'Ch {w[6]}']
               for w in words]
    write_md(
        out / 'sblair-vocab.md',
        'BBH Vocabulary — Ch2–35 (S. Blair Deck)',
        '527 words keyed to BBH chapters 2–35, with Arabic roots and NT-style frequency counts.',
        ['Hebrew', 'Gloss', 'Root', 'Frequency', 'Chapter'],
        md_rows,
        note='Mnemonic hooks (English-Arabic mnemonics) present in original deck; '
             'stripped here for brevity — see Anki for full mnemonics.'
    )

    # Anki
    anki_rows = []
    for _, _, heb, eng, freq, root, ch_n in words:
        back = eng
        if root:
            back += f' | root: {root}'
        if freq:
            back += f' | {freq}×'
        tags = f'sblair-vocab bbh-ch{ch_n}'
        anki_rows.append((heb, back, tags))
    write_anki(out / 'sblair-vocab.txt',
               'BBH Vocabulary Ch2–35 (S. Blair)', anki_rows)

    # FD
    fd_rows = [(heb, eng + (f' ({root})' if root else '') + (f' — {freq}×' if freq else ''))
               for _, _, heb, eng, freq, root, _ in words]
    write_fd(out / 'sblair-vocab-fd.txt',
             'BBH Vocabulary Ch2–35 (S. Blair)', fd_rows)

    print(f'  {len(words)} words across Ch2–35')


# ── Deck 1b: Extended OT vocabulary (cards 507–1000, freq 30–69) ─────────

def convert_vocab_extra() -> None:
    print('\n=== Deck 1b: Extended OT Vocab (freq 30–69) ===')
    out = OUT_ROOT / 'sblair-vocab-extra'
    out.mkdir(exist_ok=True)

    con = sqlite3.connect(
        '/tmp/anki_extract/1000 words BBH mnemonics, etc./collection.anki21')

    words: list[tuple] = []
    for row in con.execute('SELECT flds FROM notes'):
        f = row[0].split('\x1f')
        num  = clean(f[0]) if len(f) > 0 else ''
        heb  = clean(f[1]) if len(f) > 1 else ''
        eng  = clean(f[2]) if len(f) > 2 else ''
        freq = clean(f[4]) if len(f) > 4 else ''
        ch   = clean(f[5]) if len(f) > 5 else ''
        root = clean(f[6]) if len(f) > 6 else ''
        if ch:
            continue
        words.append((int(num) if num.isdigit() else 9999,
                      heb, eng, freq, root))
    con.close()

    words.sort(key=lambda x: x[0])

    md_rows = [[w[1], w[2], w[4] or '—', w[3]]
               for w in words]
    write_md(
        out / 'sblair-vocab-extra.md',
        'Extended OT Vocabulary — Freq 30–69 (S. Blair Deck)',
        '473 Hebrew words with OT frequency 30–69, beyond the BBH chapter wordlists.',
        ['Hebrew', 'Gloss', 'Root', 'Frequency'],
        md_rows,
    )

    anki_rows = []
    for _, heb, eng, freq, root in words:
        back = eng
        if root:
            back += f' | root: {root}'
        if freq:
            back += f' | {freq}×'
        anki_rows.append((heb, back, 'sblair-vocab-extra'))
    write_anki(out / 'sblair-vocab-extra.txt',
               'Extended OT Vocab Freq 30–69 (S. Blair)', anki_rows)

    fd_rows = [(heb, eng + (f' ({root})' if root else '') + (f' — {freq}×' if freq else ''))
               for _, heb, eng, freq, root in words]
    write_fd(out / 'sblair-vocab-extra-fd.txt',
             'Extended OT Vocab Freq 30–69 (S. Blair)', fd_rows)

    print(f'  {len(words)} words')


# ── Deck 2: Strong verb paradigm (all forms of קטל across 7 stems) ────────

def convert_paradigm() -> None:
    print('\n=== Deck 2: Strong Verb Paradigm (S. Blair) ===')
    out = OUT_ROOT / 'sblair-paradigm'
    out.mkdir(exist_ok=True)

    con = sqlite3.connect(
        '/tmp/anki_extract/Biblical_Hebrew_-_All_Forms_of_Qatal/collection.anki2')
    models = json.loads(con.execute('SELECT models FROM col').fetchone()[0])
    stem_mid = next(
        mid for mid, m in models.items() if 'HebrewStemExercise' in m['name'])

    cards: list[tuple] = []
    for row in con.execute(f'SELECT flds FROM notes WHERE mid = {stem_mid}'):
        f = row[0].split('\x1f')
        form = clean(f[0]) if len(f) > 0 else ''
        stem = clean(f[1]) if len(f) > 1 else ''
        conj = clean(f[2]) if len(f) > 2 else ''
        pgn  = clean(f[3]) if len(f) > 3 else ''
        root = clean(f[4]) if len(f) > 4 else ''
        cards.append((form, stem, conj, pgn, root))
    con.close()

    # Sort by stem order then conjugation
    STEM_ORDER = ['Qal', 'Niphal', 'Piel', 'Pual', 'Hiphil', 'Hophal', 'Hithpael']
    CONJ_ORDER = ['Perfect', 'Imperfect', 'Imperative', 'Infinitive Construct',
                  'Infinitive Absolute', 'Participle', 'Participle Active',
                  'Participle Passive']

    def sort_key(c):
        si = STEM_ORDER.index(c[1]) if c[1] in STEM_ORDER else 99
        ci = next((i for i, x in enumerate(CONJ_ORDER) if x in c[2]), 99)
        return (si, ci, c[3])

    cards.sort(key=sort_key)

    md_rows = [[c[0], c[1], c[2], c[3] or '—', c[4]] for c in cards]
    write_md(
        out / 'sblair-paradigm.md',
        'Hebrew Strong Verb Paradigm — All Stems (S. Blair Deck)',
        '195 cards covering all 7 stems × all conjugations using the paradigm root קטל.',
        ['Form', 'Stem', 'Conjugation', 'PGN', 'Root'],
        md_rows,
    )

    anki_rows = []
    for form, stem, conj, pgn, root in cards:
        back = f'{stem} | {conj}'
        if pgn:
            back += f' | {pgn}'
        back += f' | root: {root}'
        slug = stem.lower().replace(' ', '-').replace('\'', '')
        tags = f'sblair-paradigm stem-{slug}'
        anki_rows.append((form, back, tags))
    write_anki(out / 'sblair-paradigm.txt',
               'Hebrew Strong Verb Paradigm (S. Blair)', anki_rows)

    fd_rows = []
    for form, stem, conj, pgn, root in cards:
        back = f'{stem} — {conj}' + (f' {pgn}' if pgn else '')
        fd_rows.append((form, back))
    write_fd(out / 'sblair-paradigm-fd.txt',
             'Hebrew Strong Verb Paradigm (S. Blair)', fd_rows)

    print(f'  {len(cards)} paradigm cards')


# ── Deck 3: OT verb parsing (10,399 cards) ─────────────────────────────────

def convert_parsing() -> None:
    print('\n=== Deck 3: OT Verb Parsing (S. Blair) ===')
    out = OUT_ROOT / 'sblair-parsing'
    out.mkdir(exist_ok=True)

    con = sqlite3.connect(
        '/tmp/anki_extract/Hebrew parsing exercises/collection.anki21')

    # Normalise stem names to match our conventions
    STEM_MAP = {
        'Qal': 'Qal', 'Nifal': 'Niphal', 'Niphal': 'Niphal',
        'Piel': 'Piel', 'Pual': 'Pual',
        'Hifil': 'Hiphil', 'Hofal': 'Hophal',
        'Hitpael': 'Hithpael', 'Hotpaal': 'Hothpaal',
        'Polel': 'Polel', 'Poel': 'Poel', 'Poal': 'Poal', 'Polal': 'Polal',
        'PassiveQal': 'Passive Qal', 'Tifil': 'Tiphil',
        'Hitpoel': 'Hithpoel', 'Nitpael': 'Nithpael',
    }
    CONJ_MAP = {
        'Perfect': 'Perfect', 'Imperfect': 'Imperfect',
        'Imperative': 'Imperative', 'Participle': 'Participle',
        'PassiveParticiple': 'Passive Participle',
        'InfinitiveConstruct': 'Inf. Construct',
        'InfinitiveAbsolute': 'Inf. Absolute',
    }

    cards: list[tuple] = []
    for row in con.execute('SELECT flds FROM notes'):
        f = row[0].split('\x1f')
        form   = clean(f[0]) if len(f) > 0 else ''
        root   = clean(f[1]) if len(f) > 1 else ''
        stem   = STEM_MAP.get(clean(f[2]) if len(f) > 2 else '', clean(f[2]))
        conj   = CONJ_MAP.get(clean(f[3]) if len(f) > 3 else '', clean(f[3]))
        person = clean(f[4]) if len(f) > 4 else ''
        gender = clean(f[5]) if len(f) > 5 else ''
        number = clean(f[6]) if len(f) > 6 else ''
        psfx   = clean(f[7]) if len(f) > 7 else ''
        gloss  = clean(f[9]) if len(f) > 9 else ''
        freq_i = clean(f[11]) if len(f) > 11 else ''
        freq_v = clean(f[12]) if len(f) > 12 else ''
        verse  = clean(f[13]) if len(f) > 13 else ''

        # Build PGN string
        pgn_parts = [p for p in [person, gender, number] if p]
        pgn = ''.join(pgn_parts) if pgn_parts else ''
        if psfx:
            pgn += f'+{psfx}'

        cards.append((form, root, stem, conj, pgn, gloss, freq_i, freq_v, verse))
    con.close()

    # Write one combined MD (summary table — gloss + parsing)
    md_rows = []
    for form, root, stem, conj, pgn, gloss, freq_i, freq_v, verse in cards[:500]:
        # Limit MD to first 500 — full set too large for static table
        parse_str = f'{stem} {conj} {pgn}'.strip()
        md_rows.append([form, root, parse_str, gloss, freq_i or '—'])

    write_md(
        out / 'sblair-parsing.md',
        'OT Hebrew Verb Parsing — 10,399 Forms (S. Blair Deck)',
        'Attested OT verb forms with full parsing: stem, conjugation, PGN, '
        'gloss, and inflection frequency. First 500 shown; see .txt for full set.',
        ['Form', 'Root', 'Parsing', 'Gloss', 'Inflection Freq'],
        md_rows,
        note='Full 10,399-card dataset in sblair-parsing.txt (Anki) and '
             'sblair-parsing-fd.txt (Flashcards Deluxe).'
    )

    # Full Anki file
    anki_rows = []
    for form, root, stem, conj, pgn, gloss, freq_i, freq_v, verse in cards:
        back_parts = [f'{stem} {conj} {pgn}'.strip()]
        if gloss:
            back_parts.append(f'root {root} — {gloss}')
        if freq_i:
            back_parts.append(f'{freq_i}× inflection')
        if verse:
            back_parts.append(verse[:80])
        back = ' | '.join(back_parts)
        slug = stem.lower().replace(' ', '-').replace('\'', '')
        cslug = conj.lower().replace(' ', '-').replace('.', '')
        tags = f'sblair-parsing stem-{slug} conj-{cslug}'
        anki_rows.append((form, back, tags))

    write_anki(out / 'sblair-parsing.txt',
               'OT Hebrew Verb Parsing (S. Blair)', anki_rows)

    # Full FD file
    fd_rows = []
    for form, root, stem, conj, pgn, gloss, freq_i, freq_v, verse in cards:
        parse = f'{stem} {conj} {pgn}'.strip()
        back = f'{parse} | {root}: {gloss}' if gloss else f'{parse} | root {root}'
        fd_rows.append((form, back))
    write_fd(out / 'sblair-parsing-fd.txt',
             'OT Hebrew Verb Parsing (S. Blair)', fd_rows)

    print(f'  {len(cards)} parsing cards written')


# ── Main ──────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    convert_vocab_ch()
    convert_vocab_extra()
    convert_paradigm()
    convert_parsing()

    print(f'\nAll outputs in: {OUT_ROOT}')
    print('\nRecommendations:')
    print('  sblair-vocab/     → supplement existing ch2–35 vocab decks')
    print('  sblair-vocab-extra/ → standalone "extend your vocabulary" resource')
    print('  sblair-paradigm/  → companion to ch12-ch35 stem lessons')
    print('  sblair-parsing/   → advanced parsing practice; link from relevant chapters')
