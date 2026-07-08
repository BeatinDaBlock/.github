#!/usr/bin/env bash
# scripts/scrape-wayback.sh
#
# Usage:
#   bash scripts/scrape-wayback.sh "https://web.archive.org/web/20130615120000/beatindablock.com/"
#
# Mirrors a Wayback Machine snapshot for content recovery.
# Requirements: wget (brew install wget on macOS)

set -euo pipefail

BASE_URL="${1:?Usage: $0 <wayback_snapshot_url>}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="scraped/${TIMESTAMP}"

mkdir -p "$OUTPUT_DIR"

echo "Scraping: $BASE_URL"
echo "Output:   $OUTPUT_DIR"

wget \
  --mirror \
  --convert-links \
  --adjust-extension \
  --page-requisites \
  --no-parent \
  --wait=1 \
  --random-wait \
  --timeout=30 \
  --tries=3 \
  --user-agent="Mozilla/5.0 (compatible; BeatinDaBlockArchiver/1.0)" \
  --directory-prefix="$OUTPUT_DIR" \
  "$BASE_URL"

echo "Done. Files saved to: $OUTPUT_DIR"
echo "Next: python3 scripts/extract-content.py $OUTPUT_DIR"
