"""Pelican plugin: extract_toc.

Extracts a generated table of contents block from article/page HTML and stores it in ``content.toc`` while removing it from ``content._content``.

This implementation intentionally uses only Python stdlib (html.parser).
"""

from html import escape, unescape
from html.parser import HTMLParser
from typing import Any, Protocol

from pelican import contents, signals


class _HasTocContent(Protocol):
    _content: str
    toc: str


class _TocParser(HTMLParser):
    """Capture the first ToC-like block and rebuild remaining HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self._output = []
        self._toc = []
        self._capturing = False
        self._tag_stack = []
        self._found = False

    @staticmethod
    def _is_toc_container(tag: str, attrs: dict[str, str | None]) -> bool:
        classes = set((attrs.get("class") or "").split())
        if tag == "div" and "toc" in classes:
            return True
        if tag == "div" and "contents" in classes and "topic" in classes:
            return True
        return tag == "nav" and (attrs.get("id") or "") == "TOC"

    def _append(self, text: str) -> None:
        if self._capturing:
            self._toc.append(text)
        else:
            self._output.append(text)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        text = self.get_starttag_text() or ""
        if not self._capturing and not self._found and self._is_toc_container(tag, attrs_dict):
            self._capturing = True
            self._found = True
            self._tag_stack.append(tag)
            self._toc.append(text)
            return
        if self._capturing:
            self._tag_stack.append(tag)
        self._append(text)

    def handle_endtag(self, tag: str) -> None:
        text = f"</{tag}>"
        if self._capturing:
            self._toc.append(text)
            if self._tag_stack:
                self._tag_stack.pop()
            if not self._tag_stack:
                self._capturing = False
            return
        self._output.append(text)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_text = "".join(
            f' {name}="{value}"' if value is not None else f" {name}"
            for name, value in attrs
        )
        text = f"<{tag}{attrs_text}/>"
        self._append(text)

    def handle_data(self, data: str) -> None:
        self._append(data)

    def handle_entityref(self, name: str) -> None:
        self._append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self._append(f"&#{name};")

    def handle_comment(self, data: str) -> None:
        self._append(f"<!--{data}-->")

    def handle_decl(self, decl: str) -> None:
        self._append(f"<!{decl}>")

    def handle_pi(self, data: str) -> None:
        self._append(f"<?{data}>")

    @property
    def content_html(self) -> str:
        return "".join(self._output)

    @property
    def toc_html(self) -> str:
        return "".join(self._toc)


class _HeadingParser(HTMLParser):
    """Collect heading items from HTML to build a fallback ToC."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.headings: list[tuple[int, str, str]] = []
        self._active_level: int | None = None
        self._active_id: str | None = None
        self._active_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self._active_level is None and len(tag) == 2 and tag.startswith("h") and tag[1].isdigit():
            level = int(tag[1])
            if 1 <= level <= 6:
                attrs_dict = dict(attrs)
                self._active_level = level
                self._active_id = (attrs_dict.get("id") or "").strip()
                self._active_text = []

    def handle_endtag(self, tag: str) -> None:
        if self._active_level is None:
            return
        if tag.lower() != f"h{self._active_level}":
            return

        text = unescape("".join(self._active_text)).strip()
        if self._active_id and text:
            self.headings.append((self._active_level, self._active_id, text))

        self._active_level = None
        self._active_id = None
        self._active_text = []

    def handle_data(self, data: str) -> None:
        if self._active_level is not None:
            self._active_text.append(data)

    def handle_entityref(self, name: str) -> None:
        if self._active_level is not None:
            self._active_text.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        if self._active_level is not None:
            self._active_text.append(f"&#{name};")


def _render_toc_nodes(nodes: list[dict[str, Any]]) -> str:
    if not nodes:
        return '<ul><li><a href="#">Top</a></li></ul>'

    parts = ["<ul>"]
    for node in nodes:
        node_id = str(node["id"])
        node_title = str(node["title"])
        node_children = node["children"]
        parts.append(f'<li><a href="#{escape(node_id, quote=True)}">{escape(node_title)}</a>')
        if node_children:
            parts.append(_render_toc_nodes(node_children))
        parts.append("</li>")
    parts.append("</ul>")
    return "".join(parts)


def _build_fallback_toc(html_content: str) -> str:
    heading_parser = _HeadingParser()
    heading_parser.feed(html_content)
    heading_parser.close()

    headings = heading_parser.headings
    if not headings:
        return '<ul><li><a href="#">Top</a></li></ul>'

    base_level = min(level for level, _, _ in headings)
    root_nodes: list[dict[str, Any]] = []
    stack: list[dict[str, Any]] = [
        {"level": base_level - 1, "children": root_nodes}
    ]

    for level, heading_id, title in headings:
        normalized_level = max(base_level, level)
        while stack and int(stack[-1]["level"]) >= normalized_level:
            stack.pop()

        max_child_level = int(stack[-1]["level"]) + 1
        if normalized_level > max_child_level:
            normalized_level = max_child_level

        node = {"id": heading_id, "title": title, "children": []}
        stack[-1]["children"].append(node)
        stack.append({"level": normalized_level, "children": node["children"]})

    return _render_toc_nodes(root_nodes)


def extract_toc(content: _HasTocContent | contents.Static) -> None:
    """Extract ToC HTML and attach it to the Pelican content object."""
    if isinstance(content, contents.Static):
        return

    parser = _TocParser()
    parser.feed(content._content)
    parser.close()

    toc_html = parser.toc_html.strip()
    content._content = parser.content_html
    content.toc = toc_html or _build_fallback_toc(content._content)


def register() -> None:
    """Register the extract_toc plugin with Pelican."""
    signals.content_object_init.connect(extract_toc)
