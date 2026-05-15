"""Build IBM Model 1 word-level Hebrew↔LXX alignment."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bible_grammar.ibm_align import build_word_alignment  # noqa: E402
import time  # noqa: E402

print("Building word-level Hebrew↔LXX alignment (IBM Model 1)...")
t0 = time.time()
df = build_word_alignment(n_iter=5, min_prob=0.1)
print(f"Done in {time.time()-t0:.1f}s  —  {len(df):,} word-level alignment pairs")
