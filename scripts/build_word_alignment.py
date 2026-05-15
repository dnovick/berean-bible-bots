"""Build IBM Model 1 word-level Hebrew↔LXX alignment."""
import time

from bible_grammar.core.ibm_align import build_word_alignment

print("Building word-level Hebrew↔LXX alignment (IBM Model 1)...")
t0 = time.time()
df = build_word_alignment(n_iter=5, min_prob=0.1)
print(f"Done in {time.time() - t0:.1f}s  —  {len(df):,} word-level alignment pairs")
