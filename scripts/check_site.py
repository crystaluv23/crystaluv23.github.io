#!/usr/bin/env python3
"""Check a built Hugo site without external packages or network requests."""

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urljoin, urlsplit


REQUIRED_FILES = (
    "index.html", "archives/index.html", "search/index.html", "tags/index.html",
    "faq/index.html", "404.html", "index.json", "index.xml",
)
CSS_URL = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", re.IGNORECASE)
CSS_IMPORT = re.compile(r"@import\s+['\"]([^'\"]+)['\"]", re.IGNORECASE)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.canonical = None
        self.is_article = False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonical = attrs.get("href")
        if tag == "article" and "post-single" in attrs.get("class", "").split():
            self.is_article = True
        for name in ("href", "src", "poster", "data-src"):
            if attrs.get(name):
                self.links.append(attrs[name])
        # Hugo's responsive image URLs do not contain unescaped commas.
        if attrs.get("srcset") and not attrs["srcset"].startswith("data:"):
            self.links.extend(item.strip().split()[0]
                              for item in attrs["srcset"].split(",") if item.strip())
        self.links.extend(CSS_URL.findall(attrs.get("style", "")))


def page_url(path, root, base_url):
    relative = path.relative_to(root).as_posix()
    if relative.endswith("index.html"):
        relative = relative[:-len("index.html")]
    return urljoin(base_url, quote(relative))


def local_target(link, source_url, base_url, root):
    """Map same-origin URLs to output files, including project-site prefixes."""
    if not link.strip() or link.startswith("#"):
        return None
    target = urlsplit(urljoin(source_url, link.strip()))
    base = urlsplit(base_url)
    if target.scheme not in ("http", "https") or target.netloc != base.netloc:
        return None
    target_path = unquote(target.path)
    base_path = unquote(base.path).rstrip("/")
    if base_path and not (target_path == base_path or target_path.startswith(base_path + "/")):
        raise ValueError("same-site URL is outside baseURL")
    relative = target_path[len(base_path):].lstrip("/")
    file = (root / relative).resolve()
    if not file.is_relative_to(root):
        raise ValueError("URL escapes output directory")
    if file.is_dir():
        file /= "index.html"
    return file


def check_site(root):
    errors = []
    for name in REQUIRED_FILES:
        if not (root / name).is_file():
            errors.append(f"Missing required output: {name}")
    if errors:
        return errors, None

    homepage = (root / "index.html").read_text(encoding="utf-8")
    home_parser = PageParser()
    home_parser.feed(homepage)
    base_url = home_parser.canonical
    if not base_url or not urlsplit(base_url).netloc:
        return ["Homepage must have an absolute canonical URL."], None
    base_url = base_url.rstrip("/") + "/"
    if re.search(r"lilian\s*weng|lilianweng|@lilian", homepage, re.IGNORECASE):
        errors.append("Homepage contains the reference author's identity.")

    checked_links = 0

    def check_link(link, source, source_url):
        nonlocal checked_links
        try:
            target = local_target(link, source_url, base_url, root)
        except ValueError as error:
            errors.append(f"{source}: {link!r}: {error}")
            return
        if target is not None:
            checked_links += 1
            if not target.is_file():
                errors.append(f"{source}: missing target {link!r}")

    html_files = sorted(root.rglob("*.html"))
    generated_posts = set()
    for path in html_files:
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        if path.relative_to(root).parts[0] == "posts" and parser.is_article:
            generated_posts.add(path)
        for link in parser.links:
            check_link(link, path.relative_to(root), page_url(path, root, base_url))

    css_files = sorted(root.rglob("*.css"))
    for path in css_files:
        css = path.read_text(encoding="utf-8")
        for link in CSS_URL.findall(css) + CSS_IMPORT.findall(css):
            check_link(link, path.relative_to(root), page_url(path, root, base_url))

    post_count = 0
    try:
        entries = json.loads((root / "index.json").read_text(encoding="utf-8"))
        if not isinstance(entries, list):
            raise ValueError("expected an array of search entries")
        post_links = set()
        for entry in entries:
            if (not isinstance(entry, dict) or not isinstance(entry.get("title"), str)
                    or not entry["title"] or not isinstance(entry.get("permalink"), str)
                    or not entry["permalink"]):
                errors.append("Search index contains an entry without title or permalink.")
                continue
            permalink = entry["permalink"]
            check_link(permalink, "index.json", base_url)
            target = local_target(permalink, base_url, base_url, root)
            if target in generated_posts:
                post_links.add(target)
        post_count = len(post_links)
        for missing in sorted(generated_posts - post_links):
            errors.append(f"Search index does not cover article: {missing.relative_to(root)}")
    except (ValueError, TypeError) as error:
        errors.append(f"Invalid search index: {error}")

    try:
        feed = ET.parse(root / "index.xml")
        items = feed.findall("./channel/item")
        if generated_posts and not items:
            errors.append("RSS feed has no articles.")
        for item in items:
            link = item.findtext("link")
            if link:
                check_link(link, "index.xml", base_url)
    except ET.ParseError as error:
        errors.append(f"Invalid RSS feed: {error}")

    summary = (f"{len(html_files)} HTML pages, {len(css_files)} CSS files, "
               f"{checked_links} internal references, {post_count} searchable articles; "
               f"baseURL {base_url}")
    return errors, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", default="public", type=Path)
    args = parser.parse_args()
    errors, summary = check_site(args.directory.resolve())
    if errors:
        print("Site check failed:", file=sys.stderr)
        for error in sorted(set(errors)):
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"Site check passed: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
