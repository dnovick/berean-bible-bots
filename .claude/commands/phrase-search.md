# Phrase Search

Search for consecutive word sequences in Hebrew OT, Greek NT, or LXX.

**Usage:** `/phrase-search <token1> <token2> [token3 ...] [in <book>] [corpus <OT|NT|LXX>]`

Each token may be:
- A Strong's number: `H1697`, `G3056`
- A Hebrew or Greek lemma: `שָׁלוֹם`, `λόγος`
- A wildcard `*` — matches any single word

Natural language instructions like "find X in Y" or "search for A followed by B in Isaiah" are also fine — interpret them and call phrase_search() accordingly.

**Examples:**
- `/phrase-search H1697 H3068` — דְּבַר יְהוָה "word of the LORD" in OT
- `/phrase-search H1697 H3068 in Jer` — same, restricted to Jeremiah
- `/phrase-search G3056 G2316 corpus NT` — λόγος θεοῦ in NT
- `/phrase-search λόγος θεός corpus NT` — same using Greek lemmas
- `/phrase-search H1697 * H3068` — H1697 + any word + H3068

---

```python
import sys, re
sys.path.insert(0, 'src')
from bible_grammar import phrase_search, print_phrase_results

args = "$ARGUMENTS".strip()

# Parse optional corpus and book from natural language or flags
corpus = 'OT'
book = None

corpus_match = re.search(r'\bcorpus\s+(OT|NT|LXX)\b', args, re.I)
if corpus_match:
    corpus = corpus_match.group(1).upper()
    args = args[:corpus_match.start()] + args[corpus_match.end():]

in_match = re.search(r'\bin\s+([A-Za-z0-9]+)\b', args, re.I)
if in_match:
    book = in_match.group(1)
    args = args[:in_match.start()] + args[in_match.end():]

# Infer corpus from tokens if not specified
if corpus == 'OT' and re.search(r'\bG\d{3,5}[A-Z]?\b', args):
    corpus = 'NT'

# Tokenize remaining args
tokens = args.split()
tokens = [t if t != '*' else '*' for t in tokens if t]

if not tokens:
    print("Usage: /phrase-search <token1> <token2> ...")
else:
    kwargs = {'corpus': corpus}
    if book:
        kwargs['book'] = book
    df = phrase_search(tokens, **kwargs)
    phrase_str = '  '.join(tokens)
    scope = f" in {book}" if book else ""
    print(f"\nPhrase search: {phrase_str}  [{corpus}{scope}]")
    print_phrase_results(df, max_rows=25)
```
