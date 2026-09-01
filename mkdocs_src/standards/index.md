# Content Standards

These documents define the rules for each content domain in the Berean Bible Bots project. They are the authoritative specifications that validators enforce and that agents consult before working on content of that type.

| Document | Domain | Enforced by |
|---|---|---|
| [Exercise Standards](exercises.md) | Exercise files (.md, .html, .pdf), HTML format, input types, answer rows | `scripts/validate_exercises.py` |
| [Lesson Standards](lessons.md) | Chapter directory layout, README structure, Anki decks, session management | `scripts/validate_lessons.py`, `scripts/validate_courses.py` |
| [Report Standards](reports.md) | Build scripts, CSV exports, README indexes, report structure, nav registration | manual + `scripts/validate_nav.py` |
| [Language & Display Standards](language.md) | No transliterations, table format, RTL/bidi, NT text tradition, BBH naming | manual + `scripts/validate_links.py` |

For operational policies (what agents are permitted to do autonomously), see [`docs/policies/`](../policies/).
