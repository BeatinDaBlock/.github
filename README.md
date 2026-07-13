# BeatinDaBlock — Development Repository

> 🎙️ **[beatindablock.com](https://beatindablock.com)** | Underground hip-hop podcast since 2012

📦 Repository: [`BeatinDaBlock/.github`](https://github.com/BeatinDaBlock/.github)

This is the development hub for the BeatinDaBlock web presence. It contains:

- **Cloudflare Pages** static site (`cloudflare/pages/`)
- **Cloudflare Workers** scripts (`cloudflare/workers/`)
- **WordPress theme** (`wordpress/theme/beatindablock/`)
- **GitHub profile** page (`profile/README.md`)
- **Documentation** (`docs/`)

---

## Quick Start

### Deploy to Cloudflare Pages

```bash
npm install -g wrangler
wrangler login
wrangler pages deploy cloudflare/pages/public --project-name beatindablock
```

### Deploy Workers

```bash
wrangler deploy cloudflare/workers/redirect.js --name beatindablock-redirects
wrangler deploy cloudflare/workers/rss-proxy.js --name beatindablock-rss
```

### Install WordPress Theme

Copy `wordpress/theme/beatindablock/` to your WordPress `wp-content/themes/` directory.

---

## Documentation

| Doc | Description |
|-----|-------------|
| [`docs/WAYBACK-RESEARCH.md`](docs/WAYBACK-RESEARCH.md) | Phase 1: How to recover 2012–2016 content from the Wayback Machine |
| [`docs/CONTENT-INVENTORY.md`](docs/CONTENT-INVENTORY.md) | Phase 2: Content inventory template — fill in as you scrape |
| [`docs/CLOUDFLARE-SETUP.md`](docs/CLOUDFLARE-SETUP.md) | Phase 3: Step-by-step Cloudflare configuration guide |
| [`docs/WORDPRESS-SETUP.md`](docs/WORDPRESS-SETUP.md) | Phase 4: WordPress site design & setup |
| [`docs/STRATEGY.md`](docs/STRATEGY.md) | Phase 5: Full website strategy (SEO, content, monetization) |

---

## Repository Structure

```
.github/
  workflows/
    update-readme.yml     # Auto-updates profile README with latest episode
cloudflare/
  wrangler.toml           # Cloudflare project config
  db/
    schema.sql            # D1 database schema
  workers/
    redirect.js           # URL redirects + RSS cache refresh (cron)
    rss-proxy.js          # RSS feed proxy + JSON API endpoint
  pages/
    public/               # Static site (deploy this to Cloudflare Pages)
      index.html
      episodes/index.html
      about/index.html
      contact/index.html
      assets/
        css/style.css
        js/episodes.js
docs/
  WAYBACK-RESEARCH.md
  CONTENT-INVENTORY.md
  CLOUDFLARE-SETUP.md
  WORDPRESS-SETUP.md
  STRATEGY.md
profile/
  README.md               # GitHub org profile page
wordpress/
  theme/
    beatindablock/        # Custom WordPress theme
      style.css
      functions.php
      index.php
      header.php
      footer.php
      single-episode.php
```