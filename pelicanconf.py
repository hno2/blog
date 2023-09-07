#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import pelican_cite


AUTHOR = "Simon Klug"
SITENAME = "Today I learned..."
SITESUBTITLE = "Learning Blog of Simon Klug"
SITEURL = ""

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
SITE_DESCRIPTION = "Explore the personal blog of Simon Klug where everyday experiences transform into valuable lessons. Join me as I delve into the worlds of theatre, master the art of leading a good workshop, dive into AI topics, and unravel the mysteries of education. Follow along on my journey of continuous learning and discovery."


AUTHORS = {
    "Simon Klug": {
        "url": "https://simonklug.de/",
        "blurb": "In the world of Artificial Intelligence and digitalization, I'm Simon Klug, a passionate explorer and a day-to-day learner, located in Karlsruhe. By day, I bring my love for AI to life at Bosch, leading the charge in training our teams for the future. But my journey doesn't stop there. When I am not immersed in the world of technology and work, you'll find me on a theatre stage, running, cooking or failing in new acrobatic skills.",
        "avatar": "/images/avatars/simonklug.jpeg",
    }
}

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
