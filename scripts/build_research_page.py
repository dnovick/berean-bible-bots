#!/usr/bin/env python3
"""
Build mkdocs_src/research/index.md from data/research/.index_manifest.json.

Run any time a paper is added to the manifest:
    python scripts/build_research_page.py
"""

import json
import os
from collections import Counter
from typing import Any, Dict, List

MANIFEST = os.path.join(
    os.path.dirname(__file__), "..", "data", "research", ".index_manifest.json"
)
OUT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "mkdocs_src", "research"
)
OUT_FILE = os.path.join(OUT_DIR, "index.md")


def sort_key(entry: Dict[str, Any]) -> tuple:
    """Sort by author last name, then year, then title."""
    author = entry.get("author", "") or ""
    year = entry.get("year", "") or ""
    title = entry.get("title", "") or ""
    last = author.split(",")[0].strip().lower() if author else "zzz"
    return (last, year, title.lower())


def build_tag_set(papers: List[Dict[str, Any]]) -> List[str]:
    counts: Counter = Counter()
    for p in papers:
        for t in (p.get("tags") or "").split(","):
            t = t.strip()
            if t:
                counts[t] += 1
    return sorted(counts.keys())


def paper_row_html(p: Dict[str, Any], idx: int) -> str:
    title = p.get("title") or "(untitled)"
    author = p.get("author") or ""
    year = p.get("year") or ""
    journal = p.get("journal") or ""
    url = (p.get("url") or "").strip()
    tags = [t.strip() for t in (p.get("tags") or "").split(",") if t.strip()]
    note = p.get("note") or ""

    title_cell = (
        f'<a href="{url}" target="_blank" rel="noopener">{title}</a>'
        if url else title
    )
    tag_html = "".join(
        f'<span class="rp-tag" data-tag="{t}">{t}</span>' for t in tags
    )
    note_html = f'<br><span class="rp-note">{note}</span>' if note else ""
    data_tags = " ".join(tags)
    data_lang = "greek" if "greek" in tags else "hebrew" if (
        "hebrew" in tags or "aramaic" in tags
    ) else "other"

    return (
        f'<tr data-tags="{data_tags}" data-lang="{data_lang}">'
        f'<td class="rp-author">{author}</td>'
        f'<td class="rp-year">{year}</td>'
        f'<td class="rp-title">{title_cell}{note_html}</td>'
        f'<td class="rp-journal">{journal}</td>'
        f'<td class="rp-tags">{tag_html}</td>'
        f'</tr>'
    )


def build_page(papers: List[Dict[str, Any]], all_tags: List[str]) -> str:
    rows = "\n".join(paper_row_html(p, i) for i, p in enumerate(papers))
    tag_buttons = "\n".join(
        f'<button class="rp-filter" data-tag="{t}">{t}</button>'
        for t in all_tags
    )
    count = len(papers)

    return f"""\
# Research Library

<p class="rp-subtitle">
  {count} papers indexed for semantic search.
  Click a tag to filter; click again to clear.
</p>

<div class="rp-controls">
  <button class="rp-filter rp-lang" data-lang="hebrew">Hebrew</button>
  <button class="rp-filter rp-lang" data-lang="greek">Greek</button>
  <span class="rp-sep">|</span>
{tag_buttons}
  <button class="rp-clear" onclick="rpClear()">Clear filters</button>
</div>

<p class="rp-count" id="rp-count">{count} papers shown</p>

<div class="rp-table-wrap">
<table class="rp-table" id="rp-table">
<thead>
<tr>
  <th>Author</th>
  <th>Year</th>
  <th>Title</th>
  <th>Publication</th>
  <th>Tags</th>
</tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
</div>

<style>
.rp-subtitle {{ color: #666; font-style: italic; margin-top: -.3rem; margin-bottom: 1rem; }}
.rp-controls {{ display: flex; flex-wrap: wrap; gap: .4rem; align-items: center; margin-bottom: .6rem; }}
.rp-filter {{
  padding: .22rem .65rem; border-radius: 999px; border: 1px solid #aaa;
  background: #f4f4f4; cursor: pointer; font-size: .8rem; color: #333;
  transition: background .15s, color .15s;
}}
.rp-filter:hover {{ background: #ddd; }}
.rp-filter.active {{ background: #2a6099; color: #fff; border-color: #2a6099; }}
.rp-filter.rp-lang {{ font-weight: bold; }}
.rp-sep {{ color: #bbb; padding: 0 .25rem; }}
.rp-clear {{
  padding: .22rem .65rem; border-radius: 999px; border: 1px solid #c06060;
  background: #fff0f0; cursor: pointer; font-size: .8rem; color: #8b0000;
}}
.rp-clear:hover {{ background: #ffd8d8; }}
.rp-count {{ font-size: .85rem; color: #666; margin-bottom: .4rem; }}
.rp-table-wrap {{ overflow-x: auto; }}
.rp-table {{ border-collapse: collapse; width: 100%; font-size: .88rem; }}
.rp-table th {{
  background: #e0e8f0; padding: .4rem .6rem; border: 1px solid #bbb;
  text-align: left; white-space: nowrap;
}}
.rp-table td {{ padding: .35rem .6rem; border: 1px solid #ddd; vertical-align: top; }}
.rp-table tr[data-tags]:not(.rp-visible) {{ display: none; }}
.rp-author {{ white-space: nowrap; min-width: 8rem; }}
.rp-year {{ white-space: nowrap; text-align: center; }}
.rp-title a {{ color: #1a5c99; }}
.rp-journal {{ font-style: italic; font-size: .82rem; color: #555; min-width: 10rem; }}
.rp-tags {{ min-width: 8rem; }}
.rp-tag {{
  display: inline-block; margin: .1rem .15rem; padding: .1rem .4rem;
  border-radius: 999px; background: #e8f0f8; color: #2a4a6e;
  font-size: .74rem; cursor: pointer; border: 1px solid #c0d0e0;
}}
.rp-tag:hover {{ background: #c8daf0; }}
.rp-note {{ font-size: .78rem; color: #888; font-style: italic; }}
</style>

<script>
(function () {{
  var activeTagFilters = [];
  var activeLangFilter = null;

  function apply() {{
    var rows = document.querySelectorAll('#rp-table tbody tr');
    var shown = 0;
    rows.forEach(function (r) {{
      var tags = (r.dataset.tags || '').split(' ');
      var lang = r.dataset.lang || '';
      var tagMatch = activeTagFilters.length === 0 ||
        activeTagFilters.every(function (f) {{ return tags.indexOf(f) !== -1; }});
      var langMatch = !activeLangFilter || lang === activeLangFilter;
      if (tagMatch && langMatch) {{
        r.classList.add('rp-visible');
        shown++;
      }} else {{
        r.classList.remove('rp-visible');
      }}
    }});
    var el = document.getElementById('rp-count');
    if (el) el.textContent = shown + ' paper' + (shown !== 1 ? 's' : '') + ' shown';
  }}

  // Show all on load
  document.querySelectorAll('#rp-table tbody tr').forEach(function (r) {{
    r.classList.add('rp-visible');
  }});

  document.querySelectorAll('.rp-filter:not(.rp-lang)').forEach(function (btn) {{
    btn.addEventListener('click', function () {{
      var tag = btn.dataset.tag;
      var idx = activeTagFilters.indexOf(tag);
      if (idx === -1) {{ activeTagFilters.push(tag); btn.classList.add('active'); }}
      else {{ activeTagFilters.splice(idx, 1); btn.classList.remove('active'); }}
      apply();
    }});
  }});

  document.querySelectorAll('.rp-filter.rp-lang').forEach(function (btn) {{
    btn.addEventListener('click', function () {{
      var lang = btn.dataset.lang;
      if (activeLangFilter === lang) {{
        activeLangFilter = null; btn.classList.remove('active');
      }} else {{
        document.querySelectorAll('.rp-filter.rp-lang').forEach(function (b) {{
          b.classList.remove('active');
        }});
        activeLangFilter = lang; btn.classList.add('active');
      }}
      apply();
    }});
  }});

  // Clicking a tag chip in the table toggles that filter
  document.querySelector('#rp-table').addEventListener('click', function (e) {{
    var chip = e.target.closest('.rp-tag');
    if (!chip) return;
    var tag = chip.dataset.tag;
    var btn = document.querySelector('.rp-filter[data-tag="' + tag + '"]');
    if (btn) btn.click();
  }});

  window.rpClear = function () {{
    activeTagFilters = [];
    activeLangFilter = null;
    document.querySelectorAll('.rp-filter').forEach(function (b) {{
      b.classList.remove('active');
    }});
    apply();
  }};
}})();
</script>
"""


def main() -> None:
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)

    papers = [
        {**v, "_id": k}
        for k, v in manifest.items()
        if v.get("title")
    ]
    papers.sort(key=sort_key)

    all_tags = build_tag_set(papers)

    os.makedirs(OUT_DIR, exist_ok=True)
    content = build_page(papers, all_tags)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Wrote {OUT_FILE} ({len(papers)} papers, {len(all_tags)} tags)")


if __name__ == "__main__":
    main()
