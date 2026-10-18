# simonklug.de

Personal Website

## Requirments
* Pelican Katex needs `node.js` to render to file

## Build

Run `uv run pelican -s publishconf.py content`.

Category pages are disabled. An explicit category in `DEFAULT_METADATA` keeps
draft rendering compatible with Pelican 4.12, which does not apply
`DEFAULT_CATEGORY` when `CATEGORY_SAVE_AS` is empty.

Run regression tests with `uv run python -m unittest discover -s tests`.
