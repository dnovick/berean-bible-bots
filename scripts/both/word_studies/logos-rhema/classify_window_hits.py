"""LLM classifier for sliding-window scripture-proximity hits.

Reads:   output/reports/both/word_studies/logos-rhema/window-hits.csv
         (produced by build_logos_rhema_report.py)

Writes:  output/reports/both/word_studies/logos-rhema/window-hits-classified.json
         Incrementally: already-classified refs are skipped, so the script is
         safe to re-run after interruption.

Each entry in the JSON:
  {
    "word_ref": "2Ti 4:2",
    "word_term": "λόγος",
    "verdict": "yes" | "no" | "uncertain",
    "reasoning": "one-sentence explanation"
  }

Usage:
  AWS_PROFILE=<your-profile> python scripts/both/word_studies/logos-rhema/classify_window_hits.py

Requires: ANTHROPIC_API_KEY *or* AWS credentials for Bedrock (us-west-2).
The script tries Bedrock first; if boto3 credentials are unavailable it falls
back to the direct Anthropic API.
"""
import csv
import json
import sys
import time
from pathlib import Path
from typing import Any

REPORT_DIR = Path('output/reports/both/word_studies/logos-rhema')
HITS_CSV = REPORT_DIR / 'window-hits.csv'
CACHE_JSON = REPORT_DIR / 'window-hits-classified.json'

BEDROCK_REGION = 'us-west-2'
BEDROCK_MODEL = 'us.anthropic.claude-sonnet-4-5-20250929-v1:0'

# Context window: grab this many KJV verses before/after the target verse
CONTEXT_VERSES = 3

_SYSTEM = (
    "You are a biblical-Greek lexicographer with expertise in the NT and LXX. "
    "Answer precisely and briefly."
)

_PROMPT_TEMPLATE = """\
Task: decide whether a specific Greek word in a NT verse is being used to refer \
to the written scriptures (OT text, law, prophets, or a canonical text).

Greek term: {term} ({word_form})
Verse: {ref}
Nearest scripture-anchor: {sc_ref} ({sc_term}), {dist} verse(s) away

KJV context ({ctx_range}):
{context}

Question: In {ref}, does {term} refer to the written scriptures (OT text, law, \
prophets, or a scriptural canon)? Consider whether the referent is the written \
word of God, a specific OT passage or book, or the collected scriptures — not \
just any use of "word" or "law" in a general sense.

Respond with exactly this JSON (no markdown fence):
{{"verdict": "yes" | "no" | "uncertain", "reasoning": "<one sentence>"}}
"""


def _load_cache() -> dict:
    if CACHE_JSON.exists():
        return json.loads(CACHE_JSON.read_text(encoding='utf-8'))
    return {}


def _save_cache(cache: dict) -> None:
    CACHE_JSON.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2), encoding='utf-8'
    )


def _make_client() -> tuple:
    try:
        import boto3
        boto3.Session().client('sts').get_caller_identity()
        from anthropic import AnthropicBedrock
        return AnthropicBedrock(aws_region=BEDROCK_REGION), 'bedrock'
    except Exception:
        pass
    import os
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print(
            'ERROR: No AWS credentials available and ANTHROPIC_API_KEY is not set.\n'
            'Set AWS_PROFILE (or AWS env vars) to use Bedrock, or set '
            'ANTHROPIC_API_KEY to use the Anthropic API directly.',
            file=sys.stderr,
        )
        sys.exit(1)
    from anthropic import Anthropic
    return Anthropic(), 'direct'


def _build_context(rows: list, ref: str) -> tuple:
    """Return (context_text, ctx_range_str) with CONTEXT_VERSES before/after ref."""
    refs = [r['word_ref'] for r in rows]
    try:
        idx = refs.index(ref)
    except ValueError:
        return '', ref
    lo = max(0, idx - CONTEXT_VERSES)
    hi = min(len(rows) - 1, idx + CONTEXT_VERSES)
    lines = []
    for i in range(lo, hi + 1):
        r = rows[i]
        marker = '>>> ' if r['word_ref'] == ref else '    '
        lines.append(f"{marker}{r['word_ref']}: {r['kjv_text']}")
    ctx_range = f'{rows[lo]["word_ref"]}–{rows[hi]["word_ref"]}'
    return '\n'.join(lines), ctx_range


def _classify_one(client: Any, model_id: str, row: dict, context: str,
                  ctx_range: str, backend: str) -> dict:
    prompt = _PROMPT_TEMPLATE.format(
        term=row['word_term'],
        word_form=row['greek_form'],
        ref=row['word_ref'],
        sc_ref=row['sc_ref'],
        sc_term=row['sc_term'],
        dist=row['verse_dist'],
        ctx_range=ctx_range,
        context=context,
    )
    if backend == 'bedrock':
        response = client.messages.create(
            model=model_id,
            max_tokens=120,
            system=_SYSTEM,
            messages=[{'role': 'user', 'content': prompt}],
        )
    else:
        response = client.messages.create(
            model='claude-sonnet-4-5',
            max_tokens=120,
            system=_SYSTEM,
            messages=[{'role': 'user', 'content': prompt}],
        )
    raw = response.content[0].text.strip()
    try:
        parsed = json.loads(raw)
        verdict = parsed.get('verdict', 'uncertain')
        reasoning = parsed.get('reasoning', '')
        if verdict not in ('yes', 'no', 'uncertain'):
            verdict = 'uncertain'
    except json.JSONDecodeError:
        verdict = 'uncertain'
        reasoning = f'parse error: {raw[:120]}'
    return {'verdict': verdict, 'reasoning': reasoning}


def main() -> None:
    if not HITS_CSV.exists():
        print(
            f'ERROR: {HITS_CSV} not found.\n'
            'Run build_logos_rhema_report.py first to generate window-hits.csv.',
            file=sys.stderr,
        )
        sys.exit(1)

    with open(HITS_CSV, encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print('window-hits.csv is empty — nothing to classify.')
        return

    # Build per-term row lists for context lookup (sorted by canonical order)
    logos_rows = [r for r in rows if r['word_term'] == 'λόγος']
    rhema_rows = [r for r in rows if r['word_term'] == 'ῥῆμα']

    cache = _load_cache()
    client, backend = _make_client()
    model_id = BEDROCK_MODEL

    print(f'Backend: {backend}  |  Model: {model_id}')
    print(f'Total hits: {len(rows)}  |  Already classified: {len(cache)}\n')

    new_count = 0
    errors = 0
    for i, row in enumerate(rows, 1):
        key = f"{row['word_term']}|{row['word_ref']}"
        if key in cache:
            continue

        term_rows = logos_rows if row['word_term'] == 'λόγος' else rhema_rows
        context, ctx_range = _build_context(term_rows, row['word_ref'])

        try:
            result = _classify_one(client, model_id, row, context, ctx_range, backend)
        except Exception as e:
            print(f'  [{i}/{len(rows)}] ERROR {row["word_ref"]}: {e}')
            errors += 1
            time.sleep(2)
            continue

        cache[key] = {
            'word_ref': row['word_ref'],
            'word_term': row['word_term'],
            'verdict': result['verdict'],
            'reasoning': result['reasoning'],
        }
        new_count += 1
        v = result['verdict'].upper()
        print(f'  [{i}/{len(rows)}] {v:9s} {row["word_term"]} {row["word_ref"]}  '
              f'— {result["reasoning"][:70]}')
        _save_cache(cache)  # write after every hit — safe to interrupt
        time.sleep(0.15)   # gentle rate limiting

    print(f'\nDone. New: {new_count}  Errors: {errors}  Cached: {len(cache)}')
    totals = {'yes': 0, 'no': 0, 'uncertain': 0}
    for v in cache.values():
        totals[v['verdict']] = totals.get(v['verdict'], 0) + 1
    print(f'Verdicts — yes: {totals["yes"]}  no: {totals["no"]}  '
          f'uncertain: {totals["uncertain"]}')


if __name__ == '__main__':
    main()
