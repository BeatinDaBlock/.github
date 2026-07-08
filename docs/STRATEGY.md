# Phase 5: Website Strategy — BeatinDaBlock

## Vision

Revive BeatinDaBlock as the definitive digital home for underground hip-hop culture — anchored at `beatindablock.com`, powered by Cloudflare, and backed by a recovered archive from 2012–2016.

---

## Domain Authority Rebuild

### SEO Foundation

1. **Submit sitemap** to Google Search Console:
   - `https://beatindablock.com/sitemap.xml` (WordPress auto-generates this)
   - Also submit to Bing Webmaster Tools

2. **Reclaim old backlinks:**
   - Download the Wayback Machine snapshot list (`docs/wayback-snapshot-list.json`)
   - Use a tool like Ahrefs or Moz to find backlinks pointing to the old URL structure
   - Add 301 redirects in `cloudflare/workers/redirect.js` for any old URLs

3. **Canonical tags:**
   - Ensure all pages have `<link rel="canonical" href="https://beatindablock.com/..." />`
   - WordPress Yoast SEO handles this automatically

4. **Schema markup:**
   - Add `PodcastSeries` schema to the homepage
   - Add `PodcastEpisode` schema to each episode page

### Target Keywords

| Keyword | Intent | Page |
|---------|--------|------|
| "underground hip hop podcast" | informational | Home |
| "beatindablock podcast" | navigational | Home |
| "hip hop beats podcast 2012" | historical | About |
| "[guest name] interview" | navigational | Episode pages |

---

## Content Strategy

### Throwback Archive (Quick Win)

As soon as Wayback Machine scrape is complete:
1. Publish all recovered episodes as "archive" posts with original dates
2. Write a "We're Back" announcement post linking to the archive
3. Post on social media: _"Found our old episodes — drop a comment if you remember these 🔥"_

### New Content Cadence

| Type | Frequency | Platform |
|------|-----------|---------|
| New episode | Bi-weekly | beatindablock.com, Apple, Spotify |
| Show notes / blog post | Per episode | beatindablock.com/blog |
| Social clip (60-sec) | Per episode | Instagram, TikTok, X |
| Throwback post | Weekly | X, Instagram |

### Podcast Distribution

Submit the RSS feed (`https://beatindablock.com/feed/podcast`) to:
- Apple Podcasts: https://podcastsconnect.apple.com
- Spotify for Podcasters: https://podcasters.spotify.com
- Amazon Music / Audible
- iHeartRadio
- Pocket Casts (auto-discovers via RSS)
- Google Podcasts (deprecated → YouTube Music)

---

## Cloudflare-Native Feature Strategy

### Cloudflare D1 — Episode Database

Use D1 as the primary episode metadata store:
- Powers the `/api/episodes` JSON endpoint
- Enables full-text search on the site without a third-party service
- Supports filtering by guest, era, date range

```sql
-- Example query: archive episodes from 2012–2016
SELECT title, pub_date, guest FROM episodes WHERE era = 'archive' ORDER BY pub_date ASC;
```

### Cloudflare R2 — Audio Storage

All podcast audio files stored in R2:
- No egress fees (free bandwidth)
- ~$0.015/GB storage per month
- Serve via `https://audio.beatindablock.com` (custom domain on R2 bucket)

### Cloudflare Stream — Video Podcast

If video episodes are produced:
- Upload to Cloudflare Stream
- Embed via iframe or Stream Player SDK
- ~$5/1000 min stored + $1/1000 min delivered

### Workers AI — Auto Transcription & Summaries

Use Cloudflare Workers AI to:
1. Generate episode transcripts (Whisper model)
2. Auto-summarize episode for SEO meta description
3. Extract guest names and topics for tags

```javascript
// workers/transcribe.js (sketch)
const result = await env.AI.run('@cf/openai/whisper', {
  audio: audioBuffer,
});
const transcript = result.text;
```

### Cloudflare Turnstile — Contact Form

- Zero friction for real users (no CAPTCHA puzzles)
- Blocks bots automatically
- Free tier: unlimited challenges

---

## Social Media Strategy

| Platform | Goal | Content type |
|----------|------|-------------|
| X (Twitter) | Community, news | Episode drops, hot takes, throwbacks |
| Instagram | Visual brand | Cover art, quotes, clips |
| TikTok | Discovery, growth | 60-sec episode clips, beat drops |
| YouTube | Long-form | Full video episodes (future) |
| GitHub | Developer credibility | Open source theme, this repo |

---

## Monetization (Future)

1. **Podcast sponsorships** — once downloads reach ~500/ep
2. **Merch** — Printful + WooCommerce integration
3. **Patreon / membership** — bonus episodes, early access
4. **Cloudflare R2** — sell beat packs / exclusive audio via R2 + Workers

---

## KPIs to Track

| Metric | Tool | Target (Year 1) |
|--------|------|-----------------|
| Monthly website visitors | Cloudflare Analytics | 5,000 |
| Episode downloads | RSS analytics / Podtrac | 200/ep |
| Apple Podcasts followers | Podcasts Connect | 100 |
| Email subscribers | ConvertKit / Mailchimp | 250 |
| Backlinks recovered | Ahrefs | 20 |
