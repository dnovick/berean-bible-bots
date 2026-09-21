---
type: policy
scope: berean-bible-bots
status: active
created: 2026-09-21
version: "1.0"
---

# Session Content Pages Policy

This policy governs how static HTML pages (reference tables, interactive exercises, reading
passages) are added to a course session and linked from the session page.

---

## When to add a session HTML page

Add a session HTML page when you need to provide students with content that goes beyond what
a Markdown document can express: interactive filtering, custom typography, RTL Hebrew rendering,
or embedded data visualizations. Examples:

- A frequency reference table (e.g., top Hithpael roots by count)
- An exercise with `<select>` dropdowns or dynamic feedback
- A Scripture reading with proper Hebrew typesetting

---

## Placement on the session page

A session HTML page is **additional content**, not an agenda item. The distinction:

| Type | Placement in YAML | Rendered section |
|---|---|---|
| Lessons, readings (required attendance) | `agenda:` | `## Agenda` |
| Reference pages, supplementary tables | `sections:` (orphaned — not in agenda) | `## Additional Info` |
| Downloadable handouts, PDFs | `files:` | `## Downloads` |

An item appears in `## Additional Info` automatically when its `sections:` heading is **not**
listed in the `agenda:` block. Never add a reference or supplementary page as an agenda item.

---

## Adding a session HTML page — step by step

### 1. Create the HTML page

Write the HTML to `data/courses/<course-id>/<instance-id>/session-<N>/` and name it
descriptively: `hithpael-root-frequencies.html`, `ch34-paradigm-table.html`, etc.

Standards:
- Self-contained (no external assets that aren't on the Artifact CDN allowlist)
- Responsive (`max-width: 960px`, `padding-inline: max(16px, 5vw)`, wraps at 400px)
- Full dark/light theme via `:root` token blocks — `body` must set an explicit background
- Hebrew text uses `font-family: 'Noto Serif Hebrew', serif` (Google Fonts)
- Numbers in columns use `font-variant-numeric: tabular-nums`

### 2. Create the markdown wrapper

Write `data/courses/.../session-<N>/<page-slug>.md` — a short description of the page and a
button linking to the HTML file. The button uses a MkDocs Material button class:

    Brief description of what the page contains and why students should consult it.

    [Open interactive table](page-slug.html){.md-button .md-button--primary}

Replace `page-slug.html` with the actual HTML filename (e.g., `hithpael-root-frequencies.html`).

This `.md` file becomes the "## Additional Info" subpage that the session page links to.
The HTML file is served alongside it.

### 3. Update session.yml

Add the section reference and the asset copy entry:

```yaml
sections:
  - heading: "Human-Readable Heading"
    file: "page-slug.md"

assets:
  - file: "page-slug.html"
```

- `sections:` registers the heading for the "## Additional Info" table and writes the
  subpage from the `.md` file.
- `assets:` copies the HTML to the site output without rendering any links — it is the
  **copy-only** mechanism, distinct from `files:` (which also renders a "## Downloads" entry).

Multiple assets are supported: `assets: [{ file: "a.html" }, { file: "b.svg" }]` or
the short form `assets: ["a.html", "b.svg"]`.

### 4. Validate and commit

```bash
python scripts/validate_courses.py   # must pass
python -m flake8 src/                # must pass
```

Verify the build output for your session: look for both `Wrote .../session-N/<slug>.md`
and `Copied .../session-N/<slug>.html` in the pre-commit log.

---

## Reading files vs. assets

`reading:` items (in-session Scripture passages) also copy HTML files to the output, but
they **additionally** create an agenda entry and register a section URL. Use `assets:` for
any HTML that should not appear in the agenda.

---

## Session schema reference

```yaml
# assets:   static files to copy to the site output (no rendering — no links added to page)
#   - file: filename in this session directory
#   (also accepts a flat string list: assets: ["file1.html", "file2.svg"])
```

This field was added in build_courses.py commit 68f4cc8b (2026-09-21). Sessions created
before that date that need HTML assets should add this field to their `session.yml`.
