"""MkDocs hooks — Colab badges and SEO meta tags."""

from __future__ import annotations

SITE_URL = "https://bereanbiblebots.com"
SITE_NAME = "Berean Bible Bots"
SITE_DESC = (
    "Free exercises, flashcard decks, and reference materials for students "
    "of Biblical Hebrew, Aramaic, and Greek."
)
OG_IMAGE = f"{SITE_URL}/assets/logo.png"

GITHUB_REPO = "dnovick/berean-bible-bots"
COLAB_BASE = f"https://colab.research.google.com/github/{GITHUB_REPO}/blob/main/"
COLAB_BADGE_IMG = "https://colab.research.google.com/assets/colab-badge.svg"

_COLAB_BADGE_HTML = (
    '<p style="margin-bottom:1rem;">'
    '<a href="{url}" target="_blank" rel="noopener">'
    '<img src="' + COLAB_BADGE_IMG + '" alt="Open in Colab">'
    "</a></p>\n"
)

_OG_TAGS = """\
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{site_name}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{image}">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{image}">
"""


def on_page_context(context: object, page: object, **kwargs: object) -> object:
    """Inject Open Graph / Twitter Card meta tags into every page."""
    # Build page-specific values
    raw_title = getattr(page, "title", None) or ""
    title = f"{raw_title} — {SITE_NAME}" if raw_title else SITE_NAME

    file_ = getattr(page, "file", None)
    canonical = SITE_URL + "/"
    if file_ is not None:
        dest = getattr(file_, "dest_uri", "")
        clean = dest.replace("index.html", "").rstrip("/")
        canonical = f"{SITE_URL}/{clean}/" if clean else f"{SITE_URL}/"

    og = _OG_TAGS.format(
        site_name=SITE_NAME,
        title=title,
        desc=SITE_DESC,
        url=canonical,
        image=OG_IMAGE,
    )

    # Stash on the page object so the template can pick it up if needed;
    # also inject via on_page_content as a <head> insertion isn't directly
    # possible from hooks — we use extra_head instead via the hook below.
    if hasattr(page, "meta") and isinstance(getattr(page, "meta"), dict):
        getattr(page, "meta")["_og_tags"] = og

    return context


def on_post_page(output: str, page: object, **kwargs: object) -> str:
    """Insert OG tags into <head> of every built page."""
    file_ = getattr(page, "file", None)
    dest = getattr(file_, "dest_uri", "") if file_ is not None else ""
    if not dest.endswith(".html"):
        return output

    is_home = dest in ("index.html", "")
    raw_title = getattr(page, "title", None) or ""
    if is_home or not raw_title or raw_title.lower() == "home":
        full_title = SITE_NAME
    else:
        full_title = f"{raw_title} — {SITE_NAME}"

    canonical = SITE_URL + "/"
    if file_ is not None:
        clean = dest.replace("index.html", "").rstrip("/")
        canonical = f"{SITE_URL}/{clean}/" if clean else f"{SITE_URL}/"

    og = _OG_TAGS.format(
        site_name=SITE_NAME,
        title=full_title,
        desc=SITE_DESC,
        url=canonical,
        image=OG_IMAGE,
    )

    return output.replace("</head>", og + "</head>", 1)


def on_page_content(html: str, page: object, **kwargs: object) -> str:
    """Prepend a Colab launch badge to every notebook page and exclude from search."""
    src = getattr(page, "file", None)
    if src is None:
        return html
    path = str(src.src_uri)
    if not path.startswith("notebooks/"):
        return html

    # Exclude all notebooks/ pages (both .ipynb and index.md) from search.
    meta = getattr(page, "meta", None)
    if isinstance(meta, dict):
        meta.setdefault("search", {})
        if isinstance(meta["search"], dict):
            meta["search"]["exclude"] = True

    if not path.endswith(".ipynb"):
        return html

    colab_url = f"{COLAB_BASE}{path}"
    badge = _COLAB_BADGE_HTML.format(url=colab_url)
    return badge + html


def on_post_build(config: object, **kwargs: object) -> None:
    """Write robots.txt pointing crawlers at the sitemap."""
    import os
    site_dir = getattr(config, "site_dir", None) or "mkdocs_out"
    robots = os.path.join(str(site_dir), "robots.txt")
    with open(robots, "w", encoding="utf-8") as f:
        f.write(
            "User-agent: *\n"
            "Allow: /\n"
            f"Sitemap: {SITE_URL}/sitemap.xml\n"
        )
