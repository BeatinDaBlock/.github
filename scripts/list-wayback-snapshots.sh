#!/usr/bin/env bash
# scripts/list-wayback-snapshots.sh
#
# Uses the Wayback Machine CDX API to list all archived snapshots
# for beatindablock.com between 2012 and 2016.
#
# Usage:
#   bash scripts/list-wayback-snapshots.sh
#
# Output: docs/wayback-snapshot-list.json

set -euo pipefail

OUTPUT="docs/wayback-snapshot-list.json"
mkdir -p docs

echo "Fetching Wayback Machine snapshot list..."

curl -sSf \
  "https://web.archive.org/cdx/search/cdx\
?url=beatindablock.com/*\
&output=json\
&from=20120101\
&to=20161231\
&limit=1000\
&fl=timestamp,original,statuscode,mimetype\
&filter=statuscode:200\
&collapse=urlkey" \
  > "$OUTPUT"

COUNT=$(python3 -c "import json,sys; d=json.load(open('$OUTPUT')); print(len(d)-1)" 2>/dev/null || echo "unknown")
echo "Found $COUNT snapshots -> $OUTPUT"
echo ""
echo "Next: Pick specific snapshot URLs and run:"
echo "  bash scripts/scrape-wayback.sh <snapshot_url>"
