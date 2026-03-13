"""Pelican plugin: minify_output.

Post-processes generated HTML files after Pelican finished writing output:
1) Minify HTML/CSS/JS with minify_html.
2) Minify inline JavaScript with terser (via npx) for mangling/compression.
3) Purge unused CSS per page with purgecss (via npx), writing page-local CSS files.

This is intentionally pragmatic/"quick and dirty" and degrades gracefully when
Node tooling is unavailable.
"""

import hashlib
import os
import pathlib
import re
import shutil
import subprocess
import tempfile
from urllib.parse import urlsplit

import minify_html
from pelican import signals

SCRIPT_RE = re.compile(r"(<script(?=[^>]*>)(?![^>]*\bsrc\b)[^>]*>)(.*?)(</script>)", re.IGNORECASE | re.DOTALL)
CSS_LINK_RE = re.compile(
    r'(<link[^>]*\brel=["\']stylesheet["\'][^>]*\bhref=["\'])([^"\']+)(["\'][^>]*>)',
    re.IGNORECASE,
)


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    # Validate that only trusted commands are executed
    allowed_commands = {"npx", "terser", "purgecss"}
    if not cmd or cmd[0] not in allowed_commands:
        raise ValueError(f"Untrusted command: {cmd[0] if cmd else 'empty'}")
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def _minify_inline_js_with_terser(html_text: str) -> tuple[str, int]:
    """Minifies inline JavaScript blocks using terser via npx. Returns (transformed_html, count_of_blocks_minified)."""
    if not shutil.which("npx"):
        return html_text, 0

    changed = 0

    def repl(match: re.Match) -> str:
        """Replacement function for re.sub to minify inline JavaScript."""
        nonlocal changed
        open_tag, js_body, close_tag = match.groups()
        if not js_body.strip():
            return match.group(0)
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as js_in:
                js_in.write(js_body)
                in_path = js_in.name
            with tempfile.NamedTemporaryFile("r", suffix=".js", delete=False, encoding="utf-8") as js_out:
                out_path = js_out.name
            _run(
                [
                    "npx",
                    "--yes",
                    "terser",
                    in_path,
                    "--compress",
                    "--mangle",
                    "--format",
                    "keep_numbers=true",
                    "--output",
                    out_path,
                ]
            )
            minified_js = pathlib.Path(out_path).read_text(encoding="utf-8")
            changed += 1
            return f"{open_tag}{minified_js}{close_tag}"
        except Exception as e:
            print(f"[minify_output] terser failed for inline script: {e}")
            return match.group(0)
        finally:
            for p in (locals().get("in_path"), locals().get("out_path")):
                if p and os.path.exists(p):
                    os.unlink(p)

    return SCRIPT_RE.sub(repl, html_text), changed


def _resolve_local_css(output_path: str, html_path: str, href: str) -> pathlib.Path | None:
    """Resolves a local CSS file path from an HTML link href. Returns the absolute Path if valid and exists, otherwise None."""
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        return None
    if href.startswith("//"):
        return None

    path_part = parsed.path
    if not path_part.lower().endswith(".css"):
        return None

    if path_part.startswith("/"):
        css_abs = pathlib.Path(output_path) / path_part.lstrip("/")
    else:
        css_abs = pathlib.Path(html_path).parent / path_part
    css_abs = css_abs.resolve()

    try:
        css_abs.relative_to(pathlib.Path(output_path).resolve())
    except ValueError:
        return None

    if not css_abs.exists() or not css_abs.is_file():
        return None

    return css_abs


def _purge_css_for_page(output_path: str, html_path: str, html_text: str) -> tuple[str, int]:
    """Purges unused CSS for the given HTML page using purgecss."""
    if not shutil.which("npx"):
        return html_text, 0

    replaced = 0
    html_dir = pathlib.Path(html_path).parent

    def repl(match: re.Match) -> str:
        nonlocal replaced
        prefix, href, suffix = match.groups()
        css_file = _resolve_local_css(output_path, html_path, href)
        if not css_file:
            return match.group(0)
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp_html:
                tmp_html.write(html_text)
                html_in = tmp_html.name

            out_dir = tempfile.mkdtemp(prefix="purgecss-")
            _run(
                [
                    "npx",
                    "--yes",
                    "purgecss",
                    "--content",
                    html_in,
                    "--css",
                    str(css_file),
                    "--output",
                    out_dir,
                ]
            )

            generated = pathlib.Path(out_dir) / css_file.name
            if not generated.exists():
                return match.group(0)

            css_data = generated.read_bytes()
            digest = hashlib.sha1((str(html_path) + str(css_file)).encode("utf-8")).hexdigest()[:10]
            new_name = f"{css_file.stem}.{digest}.purged.css"
            new_abs = html_dir / new_name
            new_abs.write_bytes(css_data)

            rel_href = os.path.relpath(new_abs, html_dir).replace(os.sep, "/")
            replaced += 1
            return f"{prefix}{rel_href}{suffix}"
        except Exception as e:
            print(f"[minify_output] purgecss failed for {css_file}: {e}")
            return match.group(0)
        finally:
            if "html_in" in locals() and os.path.exists(html_in):
                os.unlink(html_in)
            if "out_dir" in locals() and os.path.exists(out_dir):
                shutil.rmtree(out_dir, ignore_errors=True)

    return CSS_LINK_RE.sub(repl, html_text), replaced


def minify_all_html(pelican) -> None:
    """Minifies all HTML files in the Pelican output directory."""
    output_path = pelican.output_path
    total_before = 0
    total_after = 0
    count = 0
    js_blocks_minified = 0
    css_links_purged = 0

    for root, _, files in os.walk(output_path):
        for fname in files:
            if not fname.endswith(".html"):
                continue
            fpath = os.path.join(root, fname)
            original = pathlib.Path(fpath).read_text(encoding="utf-8")
            transformed = original

            try:
                transformed = minify_html.minify(
                    transformed,
                    # Inline JS is minified separately by terser below.
                    # Keeping JS untouched here avoids syntax edge-cases like
                    # `cond ? .25 : 1` becoming `cond?.25:1` in output.
                    minify_js=False,
                    minify_css=True,
                    keep_html_and_head_opening_tags=True,
                    keep_comments=False,
                )
            except Exception as e:
                print(f"[minify_output] HTML minify skipped for {fpath}: {e}")

            transformed, js_count = _minify_inline_js_with_terser(transformed)
            transformed, css_count = _purge_css_for_page(output_path, fpath, transformed)

            pathlib.Path(fpath).write_text(transformed, encoding="utf-8")

            total_before += len(original.encode("utf-8"))
            total_after += len(transformed.encode("utf-8"))
            count += 1
            js_blocks_minified += js_count
            css_links_purged += css_count

    if count:
        saved = total_before - total_after
        pct = saved / total_before * 100 if total_before else 0
        print(
            f"[minify_output] Processed {count} HTML files: "
            f"{total_before / 1024:.1f} KB -> {total_after / 1024:.1f} KB "
            f"(saved {saved / 1024:.1f} KB, {pct:.1f}%), "
            f"terser scripts: {js_blocks_minified}, purged CSS links: {css_links_purged}"
        )


def register() -> None:
    """Pelican plugin registration."""
    signals.finalized.connect(minify_all_html)
