#!/usr/bin/env python3
"""
scripts/extract-content.py

Extracts text content from scraped HTML files and writes a JSON summary
to docs/extracted-content.json.

Usage:
    python3 scripts/extract-content.py scraped/20240101_120000/
"""

import os
import sys
import json
import re
from pathlib import Path
from html.parser import HTMLParser


class TextExtractor(HTMLParser):
    SKIP_TAGS = {"script", "style", "head", "noscript", "iframe"}

    def __init__(self):
        super().__init__()
        self.text: list[str] = []
        self.title: str = ""
        self._skip = False
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self._skip = True
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS:
            self._skip = False
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        stripped = data.strip()
        if not stripped:
            return
        if self._in_title:
            self.title = stripped
        elif not self._skip:
            self.text.append(stripped)


def extract_file(path: Path) -> dict:
    try:
        html = path.read_text(errors="replace")
        parser = TextExtractor()
        parser.feed(html)
        # Strip Wayback Machine toolbar noise
        text = " ".join(parser.text)
        text = re.sub(r"Wayback Machine.*?(?=\w{4,})", "", text, flags=re.DOTALL)
        return {
            "file": str(path),
            "title": parser.title,
            "text": text[:5000],  # cap per file
        }
    except Exception as exc:
        return {"file": str(path), "title": "", "text": f"[ERROR: {exc}]"}


def main():
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("scraped")
    if not base.exists():
        print(f"Directory not found: {base}", file=sys.stderr)
        sys.exit(1)

    html_files = list(base.rglob("*.html")) + list(base.rglob("*.htm"))
    print(f"Found {len(html_files)} HTML files in {base}")

    results = [extract_file(f) for f in html_files]

    out = Path("docs/extracted-content.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"Extracted {len(results)} pages → {out}")
    print("Review the file and populate docs/CONTENT-INVENTORY.md")


if __name__ == "__main__":
    main()
