"""
Pelican plugin: link_graph
Scans all article content for internal links and builds a graph data
structure (nodes + edges) that is injected into the Jinja2 template
context as the variable GRAPH_DATA (JSON string).
"""

import re
import json
import html
from pelican import signals

_TAG_RE = re.compile(r"<[^>]+>")


def clean_title(s):
    """Strip HTML tags and decode entities from a title string."""
    return html.unescape(_TAG_RE.sub("", s))


def build_graph(generator):
    # Include hidden articles (status: hidden) alongside published ones
    articles = list(generator.articles) + list(getattr(generator, "hidden_articles", []))
    if not articles:
        return
    # Build a set of valid slugs and their metadata
    slug_info = {
        art.slug: {"id": art.slug, "title": clean_title(art.title), "url": "/" + art.url.rstrip("/")}
        for art in articles
    }

    # Regex to capture href="/slug" or href="slug"  (internal links only)
    href_re = re.compile(r'href=["\']/?([^"\'#?/][^"\'#?/]*?)/?["\']')

    adj = {slug: set() for slug in slug_info}
    edges = []
    seen_edges = set()

    for art in articles:
        targets = href_re.findall(art.content)
        for raw in targets:
            target = raw.strip("/")
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


def register():
    signals.article_generator_finalized.connect(build_graph)
