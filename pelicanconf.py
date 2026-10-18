IMEZONE = "Europe/Paris"
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

PLUGIN_PATHS = ["plugins"]
PLUGINS = [
    "sitemap",
    "pelican_cite",
    "pelican_katex",
    "link_graph",
    "extract_toc",
    "obsidian",
    #"minify_output",
]
SITEMAP = {
    "format": "xml",
    "exclude": [r"404\.html$"],
    "priorities": {"articles": 0.5, "indexes": 0.5, "pages": 0.5},
    "changefreqs": {"articles": "monthly", "indexes": "daily", "pages": "monthly"},
}

# Appearance
THEME = "theme"
TYPOGRIFY = True
DEFAULT_PAGINATION = False

# Defaults
DEFAULT_CATEGORY = "Random"
# Draft rendering requires a category even when category pages are disabled.
DEFAULT_METADATA = {"category": DEFAULT_CATEGORY}
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
    # "static/fonts": {"path": "fonts"},
    "static/favicon.ico": {"path": "favicon.ico"},
    "static/robots.txt": {"path": "robots.txt"},
    "static/llms.txt": {"path": "llms.txt"},
}
# EXTRA_PATH_METADATA = {"extra/_redirects": {"path": "_redirects"}}


DIRECT_TEMPLATES = ["index", "tags", "404"]
TAG_SAVE_AS = ""
AUTHOR_SAVE_AS = "Simon Klug"
CATEGORY_SAVE_AS = ""
USE_SHORTCUT_ICONS = True

# SEO
SITE_DESCRIPTION = "Simon Klug writes about artificial intelligence, education, software, theatre, and learning. He works on AI and digitalisation at Bosch and gives workshops and talks."


AUTHORS = {
    "Simon Klug": {
        "url": "https://simonklug.de/",
        "blurb": "Simon Klug works on artificial intelligence and digitalisation at Bosch in Karlsruhe, Germany. He writes about AI, education, software, theatre, and learning, and gives workshops and talks.",
        "avatar": "/images/avatars/simonklug.jpeg",
    }
}

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# Graph panel: how many hops from the current article to show (1 = direct links only)
GRAPH_DEPTH = 2
