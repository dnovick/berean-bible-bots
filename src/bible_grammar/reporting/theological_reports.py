"""
Pre-built theological study reports using the word-trajectory pipeline.

Generates curated cross-testament lexical studies for a standard set of
theologically significant Hebrew/Greek terms.

Public API
──────────
run_theological_report(term_key, ...)   → report dict
run_all_theological_reports(...)        → list of paths
print_all_trajectories(...)             → terminal survey
THEOLOGICAL_TRAJECTORIES                → dict of term entries
"""

from __future__ import annotations
import pandas as pd
from pathlib import Path


# ── Term registry ─────────────────────────────────────────────────────────────

THEOLOGICAL_TRAJECTORIES: dict[str, dict] = {
    # Creation
    'bara': {
        'strongs':  'H1254',
        'name':     'בָּרָא (bārāʾ)',
        'gloss':    'create',
        'theme':    'Creation',
        'notes':    'Exclusively divine creation verb in OT; how does LXX/NT handle this?',
    },
    # Covenant
    'berith': {
        'strongs':  'H1285',
        'name':     'בְּרִית (bərît)',
        'gloss':    'covenant',
        'theme':    'Covenant',
        'notes':    'Central covenant term; LXX renders consistently as διαθήκη.',
    },
    # Spirit
    'ruach': {
        'strongs':  'H7307',
        'name':     'רוּחַ (rûaḥ)',
        'gloss':    'spirit/wind/breath',
        'theme':    'Spirit',
        'notes':    'Pneuma in LXX/NT; high theological continuity expected.',
    },
    # Peace
    'shalom': {
        'strongs':  'H7965',
        'name':     'שָׁלוֹם (šālôm)',
        'gloss':    'peace/completeness/welfare',
        'theme':    'Peace',
        'notes':    'Εἰρήνη in LXX/NT; richer OT semantic range than Greek word.',
    },
    # Righteousness
    'tsedeq': {
        'strongs':  'H6664',
        'name':     'צֶדֶק (ṣeḏeq)',
        'gloss':    'righteousness',
        'theme':    'Righteousness',
        'notes':    'OT legal/relational righteousness; δικαιοσύνη carries it into NT.',
    },
    # Lovingkindness
    'hesed': {
        'strongs':  'H2617',
        'name':     'חֶסֶד (ḥeseḏ)',
        'gloss':    'steadfast love/lovingkindness',
        'theme':    'Covenant Love',
        'notes':    'Famously hard to translate; LXX uses ἔλεος (mercy) most often.',
    },
    # Salvation
    'yeshua': {
        'strongs':  'H3444',
        'name':     'יְשׁוּעָה (yəšûʿāh)',
        'gloss':    'salvation/deliverance',
        'theme':    'Salvation',
        'notes':    'Root of the name Jesus; σωτηρία is the LXX/NT counterpart.',
    },
    # Glory
    'kavod': {
        'strongs':  'H3519',
        'name':     'כָּבוֹד (kāḇôḏ)',
        'gloss':    'glory/honour/weight',
        'theme':    'Glory',
        'notes':    'δόξα in LXX/NT; both carry divine radiance and human honour.',
    },
    # Love
    'ahav': {
        'strongs':  'H0157',
        'name':     'אָהַב (ʾāhaḇ)',
        'gloss':    'love',
        'theme':    'Love',
        'notes':    'LXX uses ἀγαπάω; NT ἀγάπη is the dominant term.',
    },
    # Faith/Trust
    'emunah': {
        'strongs':  'H0530',
        'name':     'אֱמוּנָה (ʾĕmûnāh)',
        'gloss':    'faithfulness/steadfastness',
        'theme':    'Faith',
        'notes':    'LXX πίστις; NT πίστις has richer "faith/belief" sense.',
    },
    # Law/Torah
    'torah': {
        'strongs':  'H8451',
        'name':     'תּוֹרָה (tôrāh)',
        'gloss':    'law/instruction/Torah',
        'theme':    'Law',
        'notes':    'νόμος in LXX/NT; Paul\'s usage is heavily debated.',
    },
    # Redemption
    'padah': {
        'strongs':  'H6299',
        'name':     'פָּדָה (pāḏāh)',
        'gloss':    'redeem/ransom',
        'theme':    'Redemption',
        'notes':    'One of three OT redemption roots; λυτρόω in LXX.',
    },
    # Atonement
    'kaphar': {
        'strongs':  'H3722',
        'name':     'כָּפַר (kāp̄ar)',
        'gloss':    'atone/cover/make atonement',
        'theme':    'Atonement',
        'notes':    'Denominative from "cover"; LXX ἱλάσκομαι/ἐξιλάσκομαι.',
    },
    # Holy
    'qadosh': {
        'strongs':  'H6918',
        'name':     'קָדוֹשׁ (qāḏôš)',
        'gloss':    'holy/set apart',
        'theme':    'Holiness',
        'notes':    'ἅγιος in LXX/NT; very high consistency.',
    },
}


# ── Runner ────────────────────────────────────────────────────────────────────

def run_theological_report(
    term_key: str,
    *,
    output_dir: str = 'output/reports/theological',
) -> dict:
    """
    Generate a full trajectory report for one theological term.

    Parameters
    ----------
    term_key   : key from THEOLOGICAL_TRAJECTORIES (e.g. 'shalom', 'ruach')
    output_dir : directory for Markdown + chart output

    Returns the term entry dict with added 'report_path' and 'trajectory' keys.
    """
    from ..lexical.trajectory import save_trajectory_report, word_trajectory

    if term_key not in THEOLOGICAL_TRAJECTORIES:
        keys = ', '.join(THEOLOGICAL_TRAJECTORIES)
        raise KeyError(f"Unknown term {term_key!r}. Available: {keys}")

    entry = dict(THEOLOGICAL_TRAJECTORIES[term_key])
    strongs = entry['strongs']

    print(f"\n{'─'*60}")
    print(f"  {entry['name']}  —  {entry['gloss']}")
    print(f"  Theme: {entry['theme']}")
    print(f"  {entry['notes']}")

    path = save_trajectory_report(strongs, output_dir=output_dir)
    entry['report_path'] = path
    entry['trajectory'] = word_trajectory(strongs)
    return entry


def run_all_theological_reports(
    *,
    output_dir: str = 'output/reports/theological',
    keys: list[str] | None = None,
) -> list[str]:
    """
    Generate trajectory reports for all (or selected) theological terms.

    Parameters
    ----------
    output_dir : directory for output
    keys       : optional subset of THEOLOGICAL_TRAJECTORIES keys

    Returns list of Markdown file paths.
    """
    targets = keys or list(THEOLOGICAL_TRAJECTORIES)
    paths = []
    errors = []

    print(f"\n{'═'*60}")
    print(f"  Theological Trajectory Reports ({len(targets)} terms)")
    print(f"  Output: {output_dir}")
    print(f"{'═'*60}")

    for key in targets:
        try:
            entry = run_theological_report(key, output_dir=output_dir)
            paths.append(entry['report_path'])
        except Exception as e:
            print(f"  Warning: {key} failed — {e}")
            errors.append(key)

    print(f"\n{'═'*60}")
    print(f"  Done: {len(paths)} reports generated")
    if errors:
        print(f"  Failed: {', '.join(errors)}")
    _write_index(paths, output_dir)
    return paths


def print_all_trajectories(
    keys: list[str] | None = None,
) -> None:
    """Print a terminal survey of all (or selected) theological trajectories."""
    from ..lexical.trajectory import print_trajectory

    targets = keys or list(THEOLOGICAL_TRAJECTORIES)
    for key in targets:
        entry = THEOLOGICAL_TRAJECTORIES[key]
        print_trajectory(entry['strongs'])


def theological_summary_table() -> 'pd.DataFrame':
    """
    Return a DataFrame summarising all theological term trajectories:
    term | strongs | ot_total | lxx_total | nt_total | continuity
    """
    import pandas as pd
    from ..lexical.trajectory import word_trajectory

    rows = []
    for key, entry in THEOLOGICAL_TRAJECTORIES.items():
        try:
            t = word_trajectory(entry['strongs'])
            rows.append({
                'term_key':    key,
                'name':        entry['name'],
                'theme':       entry['theme'],
                'strongs':     entry['strongs'],
                'ot_total':    t['ot_total'],
                'lxx_total':   t['lxx_total'],
                'nt_total':    t['nt_total'],
                'nt_strongs':  t.get('nt_strongs', ''),
                'nt_lemma':    t.get('nt_lemma', ''),
                'lxx_pct':     t.get('lxx_consistency_pct', 0),
                'continuity':  t['continuity'],
            })
        except Exception as e:
            rows.append({'term_key': key, 'name': entry['name'], 'error': str(e)})

    return pd.DataFrame(rows)


def print_theological_summary() -> None:
    """Print a compact cross-testament summary table for all terms."""
    df = theological_summary_table()
    w = 100
    print(f"\n{'═'*w}")
    print("  Theological Term Trajectories — Summary")
    print(f"{'═'*w}")
    print(f"  {'Term':<14} {'Theme':<14} {'OT':>6} {'LXX':>6} {'NT':>6}  {'NT Word':<14} {'LXX%':>5}  {'Continuity'}")  # noqa: E501
    print(f"  {'-'*13} {'-'*13} {'-'*6} {'-'*6} {'-'*6}  {'-'*13} {'-'*5}  {'-'*10}")
    for _, r in df.iterrows():
        if 'error' in r and pd.notna(r.get('error', None)):
            print(f"  {str(r['term_key']):<14}  ERROR: {r.get('error', '')}")
            continue
        print(
            f"  {str(r['term_key']):<14} {str(r.get('theme', '')):<14} "
            f"{int(r.get('ot_total', 0)):>6} {int(r.get('lxx_total', 0)):>6} "
            f"{int(r.get('nt_total', 0)):>6}  {str(r.get('nt_lemma', '')):<14} "
            f"{float(r.get('lxx_pct', 0)):>5.0f}%  {str(r.get('continuity', ''))}"
        )
    print()


# ── Index file ────────────────────────────────────────────────────────────────

def _write_index(paths: list[str], output_dir: str) -> None:
    """Write a README.md index linking all generated reports."""
    out = Path(output_dir)
    lines = [
        "# Theological Term Trajectories",
        "",
        "Cross-testament lexical studies tracing key Hebrew theological terms "
        "through the LXX Septuagint into the Greek New Testament.",
        "",
        "| Term | Theme | Strongs | Gloss | Report |",
        "|---|---|---|---|---|",
    ]
    for key, entry in THEOLOGICAL_TRAJECTORIES.items():
        slug = entry['strongs'].lower()
        md_file = f"trajectory-{slug}.md"
        full_path = out / md_file
        link = f"[Report]({md_file})" if full_path.exists() else "—"
        lines.append(
            f"| {entry['name']} | {entry['theme']} | "
            f"{entry['strongs']} | {entry['gloss']} | {link} |"
        )
    lines += [
        "",
        "---",
        "_Generated by berean-bible-bots theological_reports module._",
    ]
    idx_path = out / "README.md"
    idx_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  Index: {idx_path}")
