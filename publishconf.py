#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import pelican_cite


AUTHOR = "Simon Klug"
SITENAME = "Today I learned..."
SITESUBTITLE = "Learning Blog of Simon Klug"
SITEURL = "https://simonklug.de"

PATH = "content"

PUBLICATIONS_SRC = "content/bibliography.bib"

# Regional Settings
TIMEZONE = "Europe/Paris"
DATE_FORMATS = {"en": "%d %b, %Y", "de": "%d %b, %Y"}
LANDING_PAGE_TITLE = "Welcome to my Learning Blog!"
# Plugins and extensions
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.admonition": {},
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.toc": {},
    }
}

PLUGINS = [
    "sitemap",
    "pelican_cite",
    "pelican_katex",
    # "extract_toc",
]
SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.5, "indexes": 0.5, "pages": 0.5},
    "changefreqs": {"articles": "monthly", "indexes": "daily", "pages": "monthly"},
}

# Appearance
THEME = "theme"
TYPOGRIFY = True
DEFAULT_PAGINATION = False

# Defaults
DEFAULT_CATEGORY = "Random"
USE_FOLDER_AS_CATEGORY = True
DEFAULT_DATE = "fs"
ARTICLE_URL = "{slug}"
PAGE_URL = "{slug}"
PAGE_SAVE_AS = "{slug}.html"
TAGS_URL = "tags"
CATEGORIES_URL = "categories"
ARCHIVES_URL = "archives"
SEARCH_URL = "search"

# Feeds
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
CATEGORY_FEED_ATOM = None
CATEGORY_FEED_RSS = None

# Elegant theme
STATIC_PATHS = ["static", "images"]
EXTRA_PATH_METADATA = {
    "static/fonts/": {"path": "fonts/"},
    "static/favicon.ico": {"path": "favicon.ico"},
    "static/robots.txt": {"path": "robots.txt"},
}
# EXTRA_PATH_METADATA = {"extra/_redirects": {"path": "_redirects"}}


DIRECT_TEMPLATES = ["index", "tags", "404"]
TAG_SAVE_AS = ""
AUTHOR_SAVE_AS = "Simon Klug"
CATEGORY_SAVE_AS = ""
USE_SHORTCUT_ICONS = True

# SEO
SITE_DESCRIPTION = "Simon documents his daily learnings in this Blog"


AUTHORS = {
    "Simon Klug": {
        "url": "https://simonklug.de/",
        "blurb": "studies at the Karlsruhe Institute, specializes in Machine Learning. He loves Theatre, Cooking and learning new things.",
        "avatar": "/images/avatars/simonklug.jpeg",
    }
}

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
