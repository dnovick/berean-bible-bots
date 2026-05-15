#!/usr/bin/env python3
"""Parse all source data and build the processed database."""
import time

from bible_grammar.core.ingest import load_all
from bible_grammar.core.translations import load_translations
from bible_grammar.core.lxx import load_lxx
from bible_grammar.core.db import save, save_translations, save_lxx
from bible_grammar.core.alignment import save_alignment, build_alignment

if __name__ == "__main__":
    t0 = time.time()

    print("Loading TAHOT + TAGNT (Hebrew/Greek morphology)...")
    df = load_all()
    print(f"  {len(df):,} words loaded in {time.time() - t0:.1f}s")
    print(f"  OT: {(df.source == 'TAHOT').sum():,}  NT: {(df.source == 'TAGNT').sum():,}")
    save(df)

    print("\nLoading translations (KJV, Vulgate, Peshitta NT)...")
    t1 = time.time()
    tr = load_translations()
    print(f"  {len(tr):,} verses loaded in {time.time() - t1:.1f}s")
    save_translations(tr)

    print("\nLoading LXX Septuagint (CenterBLC/LXX via TextFabric)...")
    t2 = time.time()
    lxx = load_lxx()
    print(f"  {len(lxx):,} words loaded in {time.time() - t2:.1f}s")
    canon = lxx[~lxx.is_deuterocanon]
    deut = lxx[lxx.is_deuterocanon]
    print(f"  Canonical OT books: {len(canon):,}  Deuterocanonical: {len(deut):,}")
    save_lxx(lxx)

    print("\nBuilding Hebrew↔LXX verse-level alignment...")
    t3 = time.time()
    alignment = build_alignment(heb_df=df, lxx_df=lxx)
    print(f"  {len(alignment):,} co-occurrence pairs in {time.time() - t3:.1f}s")
    save_alignment(alignment)

    print(f"\nAll done in {time.time() - t0:.1f}s")
