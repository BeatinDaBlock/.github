# Cloudflare Configuration

This directory contains all Cloudflare-related configuration for `beatindablock.com`.

## Structure

```
cloudflare/
├── wrangler.toml          # Cloudflare Workers & Pages project config
├── workers/
│   ├── redirect.js        # Handles legacy URL redirects + wordpress.com → .com
│   └── rss-proxy.js       # Caches and serves the podcast RSS feed at the edge
└── pages/
    ├── public/            # Static site files (HTML, CSS, JS, assets)
    └── src/               # Source files (build → public/)
```

## Deployment

### Workers

```bash
# Install Wrangler CLI
npm install -g wrangler

# Authenticate
wrangler login

# Deploy redirect worker
wrangler deploy cloudflare/workers/redirect.js --name beatindablock-redirects

# Deploy RSS proxy worker
wrangler deploy cloudflare/workers/rss-proxy.js --name beatindablock-rss
```

### Pages (Static Site)

```bash
# Deploy from the pages directory
wrangler pages deploy cloudflare/pages/public --project-name beatindablock
```

## Services to Enable in Cloudflare Dashboard

After connecting the domain:

1. **SSL/TLS** → Full (strict)
2. **Cloudflare Pages** → Connect repo, set build dir to `cloudflare/pages/public`
3. **Cloudflare Images** → Upload brand assets and episode artwork
4. **Cloudflare Stream** → For hosting podcast video/audio (optional)
5. **Cloudflare Analytics** → Enable Web Analytics (privacy-first, no cookies)
6. **Cloudflare Turnstile** → Create a widget for the contact form (free tier)
7. **Cloudflare D1** → Create database: `beatindablock-episodes`
8. **Cloudflare R2** → Create bucket: `beatindablock-audio`
9. **Cloudflare Workers** → Deploy `redirect.js` and `rss-proxy.js`
