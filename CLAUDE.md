# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This is `beatindablock/.github`, the development hub for the **BeatinDaBlock** podcast's web presence (beatindablock.com). It is a content/infra repo, not an application with a build pipeline — there is no `package.json`, no test suite, and no linter configured. Changes are validated by deploying to Cloudflare / WordPress and checking the live behavior, or by reasoning carefully about the code (Workers are small enough to review by hand).

The repo is organized into independent, loosely-coupled pieces that all serve the same site:

- **`cloudflare/`** — the live infrastructure: two Workers, a static Pages site, and a D1 schema.
- **`wordpress/theme/beatindablock/`** — a custom WordPress theme (used for the blog at `beatindablock.wordpress.com`, separate from the Cloudflare Pages static site).
- **`profile/README.md`** — the GitHub org profile page, auto-updated by a scheduled Action.
- **`scripts/`** — one-off Wayback Machine recovery tooling for restoring 2012–2016 content.
- **`docs/`** — phased planning docs (setup guides, content strategy, inventory).

## Commands

There is no build, lint, or test command — treat every change as reviewed manually and validated via deployment.

```bash
# Deploy the static Pages site
wrangler pages deploy cloudflare/pages/public --project-name beatindablock

# Deploy the two Workers (each is deployed independently, not via wrangler.toml's `main`)
wrangler deploy cloudflare/workers/redirect.js --name beatindablock-redirects
wrangler deploy cloudflare/workers/rss-proxy.js --name beatindablock-rss

# Apply/update the D1 schema
wrangler d1 execute beatindablock-episodes --file=cloudflare/db/schema.sql

# Recover archived content from the Wayback Machine (two-step)
bash scripts/list-wayback-snapshots.sh                       # -> docs/wayback-snapshot-list.json
bash scripts/scrape-wayback.sh "<wayback_snapshot_url>"       # -> scraped/<timestamp>/
python3 scripts/extract-content.py scraped/<timestamp>/       # -> docs/extracted-content.json
```

WordPress theme changes have no deploy command from this repo: copy `wordpress/theme/beatindablock/` into a WordPress install's `wp-content/themes/` directory.

## Architecture

### Cloudflare Workers are two separate deployables sharing one `wrangler.toml`

`cloudflare/wrangler.toml` sets `main = "cloudflare/workers/redirect.js"`, but in practice both Workers are deployed independently by name (`beatindablock-redirects`, `beatindablock-rss`) with routes wired up manually in the Cloudflare dashboard (see `docs/CLOUDFLARE-SETUP.md`):

- `beatindablock.com/*` → `redirect.js` (hostname canonicalization + legacy URL map + hourly cron that refreshes the RSS cache in KV)
- `beatindablock.com/api/*` and `beatindablock.com/feed/*` → `rss-proxy.js` (serves cached RSS as XML, or as JSON via `/api/episodes` and `/api/episodes/latest`)

Both Workers independently read/write the same `RSS_CACHE` KV namespace under the key `"latest-feed"` — if you change the cache key or TTL in one, update the other. `redirect.js`'s `LEGACY_REDIRECTS` map is intentionally empty and meant to be filled in as old URLs are recovered via the Wayback scripts.

`rss-proxy.js` parses RSS/XML with hand-rolled regex (`extractTag`/`extractAttr`/`extractEnclosure`), not an XML parser — keep that in mind when the feed format changes.

### Front end fetches episodes from the Worker API, not from D1 directly

`cloudflare/pages/public/assets/js/episodes.js` calls `/api/episodes` (routed to `rss-proxy.js`) to render the homepage's latest-episode card and recent-episodes grid. The D1 database (`cloudflare/db/schema.sql`) defines an `episodes` table with FTS5 full-text search and an `era` column (`archive` vs `new`), but nothing in the current code path queries D1 yet — the live site is driven entirely by the RSS feed. Treat D1 as a planned/partial integration, not the current source of truth.

### Two separate content platforms, not one CMS

- The Cloudflare Pages site (`cloudflare/pages/public/`) is hand-written static HTML/CSS/JS — no templating engine, no build step.
- The WordPress theme (`wordpress/theme/beatindablock/`) is a separate, independently-deployed site (`beatindablock.wordpress.com`) with its own custom post type (`episode`) and taxonomies (`era`, `guest`) registered in `functions.php`. `redirect.js` 301-redirects the WordPress subdomain to the apex domain, so WordPress is being phased out in favor of the static site + Workers, not actively grown.

### Docs in `docs/` are phase-numbered and sequential

`README.md`'s doc table maps each file to a phase (1: Wayback research → 2: content inventory → 3: Cloudflare setup → 4: WordPress setup → 5: strategy). When adding new planning docs, follow this same phase convention rather than introducing an unrelated structure.

### Profile README has a machine-managed section

`.github/workflows/update-readme.yml` runs every 6 hours, scrapes the podcast RSS feed, and rewrites the block between `<!-- EPISODE-START -->` / `<!-- EPISODE-END -->` markers in `profile/README.md` via a Python regex substitution, then commits with `[skip ci]`. Don't hand-edit content between those markers — it will be overwritten on the next run. Editing content outside the markers is safe.
