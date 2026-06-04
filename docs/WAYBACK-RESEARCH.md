# Phase 1: Wayback Machine Research Guide

## Overview

This document explains how to recover historical BeatinDaBlock content from the Internet Archive (Wayback Machine) covering 2012–2016.

> **Note:** The agent sandbox cannot reach archive.org. The URLs, scripts, and methodology below are ready to run from your own machine.

---

## Step 1 — Find Snapshots

Open a browser and visit each of these Wayback Machine calendar pages:

| URL to check | Wayback calendar link |
|---|---|
| `beatindablock.com` | https://web.archive.org/web/20120101000000*/beatindablock.com |
| `www.beatindablock.com` | https://web.archive.org/web/20120101000000*/www.beatindablock.com |
| `beatindablock.blogspot.com` | https://web.archive.org/web/20120101000000*/beatindablock.blogspot.com |
| `beatindablock.tumblr.com` | https://web.archive.org/web/20120101000000*/beatindablock.tumblr.com |
| `beatindablock.wordpress.com` | https://web.archive.org/web/20120101000000*/beatindablock.wordpress.com |

For each URL that has snapshots:
1. Click a year (2012–2016) to see available dates
2. Click any highlighted date to view that snapshot
3. Note the full archived URL (e.g., `https://web.archive.org/web/20130615120000/beatindablock.com/`)

---

## Step 2 — Bulk Scrape with wget

Once you have one or more working Wayback URLs, run this script on your local machine:

```bash
#!/usr/bin/env bash
# scripts/scrape-wayback.sh
# Usage: bash scrape-wayback.sh "https://web.archive.org/web/20130615120000/beatindablock.com/"

BASE_URL="${1:?Usage: $0 <wayback_url>}"
OUTPUT_DIR="scraped/$(date +%Y%m%d_%H%M%S)"

mkdir -p "$OUTPUT_DIR"

wget \
  --mirror \
  --convert-links \
  --adjust-extension \
  --page-requisites \
  --no-parent \
  --wait=1 \
  --random-wait \
  --user-agent="Mozilla/5.0 (compatible; BeatinDaBlockArchiver/1.0)" \
  --directory-prefix="$OUTPUT_DIR" \
  "$BASE_URL"

echo "Scrape complete. Files saved to: $OUTPUT_DIR"
```

Save this as `scripts/scrape-wayback.sh` and run it once per snapshot URL you want to capture.

---

## Step 3 — Extract Content

After scraping, use this Python script to extract text content from the downloaded HTML:

```python
#!/usr/bin/env python3
# scripts/extract-content.py
# Usage: python3 extract-content.py scraped/20240101_120000/

import os, sys, json
from pathlib import Path
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_tags = {"script", "style", "head"}
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self._skip = True

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            stripped = data.strip()
            if stripped:
                self.text.append(stripped)

def extract_file(path):
    try:
        html = Path(path).read_text(errors="replace")
        parser = TextExtractor()
        parser.feed(html)
        return " ".join(parser.text)
    except Exception as e:
        return f"[ERROR reading {path}: {e}]"

if __name__ == "__main__":
    base = Path(sys.argv[1] if len(sys.argv) > 1 else "scraped")
    results = []
    for f in base.rglob("*.html"):
        text = extract_file(f)
        results.append({"file": str(f), "text": text})
    out = Path("docs/extracted-content.json")
    out.write_text(json.dumps(results, indent=2))
    print(f"Extracted {len(results)} pages → {out}")
```

---

## Step 4 — What to Look For

When browsing the scraped pages, record the following in `docs/CONTENT-INVENTORY.md`:

### Episodes
- Episode title
- Guest name(s)
- Air date / publish date
- Short description or show notes
- Any embedded audio player URL

### Branding
- Logo image(s) — save to `assets/images/`
- Color scheme (hex codes from CSS)
- Fonts used
- Tagline or slogan

### "About" Content
- Show description
- Host bio(s)
- Social media handles (Twitter, Facebook, Instagram, SoundCloud, etc.)

### Blog Posts / Show Notes
- Post titles and dates
- Full text if available

---

## Wayback Machine CDX API (Automated Snapshot List)

Run this from your terminal to get a JSON list of all snapshots for a domain:

```bash
# List all snapshots for beatindablock.com between 2012 and 2016
curl "https://web.archive.org/cdx/search/cdx?\
url=beatindablock.com/*\
&output=json\
&from=20120101\
&to=20161231\
&limit=500\
&fl=timestamp,original,statuscode,mimetype" \
> docs/wayback-snapshot-list.json

echo "Snapshots saved."
```

This gives you a complete index of everything archived — use it to prioritize which pages to scrape first.

---

## Status

- [ ] beatindablock.com snapshots found
- [ ] beatindablock.blogspot.com checked
- [ ] beatindablock.tumblr.com checked
- [ ] beatindablock.wordpress.com checked
- [ ] wget scrape completed
- [ ] Content extracted to `docs/extracted-content.json`
- [ ] Content inventory filled in (`docs/CONTENT-INVENTORY.md`)
