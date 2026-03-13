"""Pelican plugin: link_graph
Scans all article content for internal links and builds a graph data
structure (nodes + edges) that is injected into the Jinja2 template
context as the variable GRAPH_DATA (JSON string).
"""

import html
import json
import re
from urllib.parse import unquote, urlsplit

from pelican import signals

_TAG_RE = re.compile(r"<[^>]+>")
_SITE_HOSTS = {"simonklug.de", "www.simonklug.de"}


def clean_title(s):
    """Strip HTML tags and decode entities from a title string."""
    return html.unescape(_TAG_RE.sub("", s))


def _normalize_path_key(path: str) -> str:
    """Normalize a URL path to a canonical lookup key."""
    key = unquote((path or "").strip()).strip("/")
    if key.endswith("/index.html"):
        key = key[: -len("/index.html")]
    elif key == "index.html":
        key = ""
    if key.endswith(".html"):
        key = key[: -len(".html")]
    return key


def _href_to_internal_key(href: str) -> str | None:
    """Return normalized internal path key or None for external/non-page hrefs."""
    if not href:
        return None
    href = href.strip()
    if not href or href.startswith("#"):
        return None

    parsed = urlsplit(href)
    if parsed.scheme in {"mailto", "tel", "javascript"}:
        return None

    if parsed.netloc and parsed.netloc.lower() not in _SITE_HOSTS:
        return None

    return _normalize_path_key(parsed.path)


def build_graph(generator) -> None:
    # Include hidden articles (status: hidden) alongside published ones
    articles = list(generator.articles) + list(getattr(generator, "hidden_articles", []))
    if not articles:
        return
    # Build a set of valid slugs and their metadata
    slug_info = {
        art.slug: {"id": art.slug, "title": clean_title(art.title), "url": "/" + art.url.rstrip("/")}
        for art in articles
    }

    # Map normalized internal URL/path variants back to canonical slugs.
    path_to_slug = {}
    for art in articles:
        variants = {
            _normalize_path_key(art.slug),
            _normalize_path_key(art.url),
            _normalize_path_key("/" + art.url.lstrip("/")),
        }
        for key in variants:
            if key:
                path_to_slug[key] = art.slug

    # Capture all href values and decide internal/external in Python.
    href_re = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)

    adj = {slug: set() for slug in slug_info}
    edges = []
    seen_edges = set()

    for art in articles:
        targets = href_re.findall(art.content)
        for href in targets:
            key = _href_to_internal_key(href)
            if not key:
                continue
            target = path_to_slug.get(key)
            if target and target in slug_info and target != art.slug:
                key = (min(art.slug, target), max(art.slug, target))
                if key not in seen_edges:
                    seen_edges.add(key)
                    edges.append({"source": art.slug, "target": target})
                adj[art.slug].add(target)
                adj[target].add(art.slug)

    nodes = [{**info, "degree": len(adj[slug])} for slug, info in slug_info.items()]

    depth = generator.settings.get("GRAPH_DEPTH", 2)
    graph_json = json.dumps({"nodes": nodes, "links": edges, "depth": depth}, ensure_ascii=False)
    generator.context["GRAPH_DATA"] = graph_json


def register() -> None:
    signals.article_generator_finalized.connect(build_graph)
