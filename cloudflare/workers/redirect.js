/**
 * Cloudflare Worker: redirect.js
 *
 * Handles:
 *  1. beatindablock.wordpress.com  → beatindablock.com  (301)
 *  2. Legacy URL patterns from the 2012–2016 site          (301)
 *  3. www.beatindablock.com        → beatindablock.com  (301)
 *  4. Everything else → passes through to the Pages site
 */

// ─── Legacy URL map (old path → new path) ────────────────────────────────────
// Populate this as you recover old URLs from the Wayback Machine scrape.
const LEGACY_REDIRECTS = {
  // Example entries — update with real discovered URLs:
  // "/episode-1":             "/episodes/episode-1/",
  // "/about-us":              "/about/",
  // "/?p=123":                "/episodes/episode-slug/",
};

// ─── Handler ──────────────────────────────────────────────────────────────────
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const { hostname, pathname, search } = url;

    // 1. Redirect wordpress.com subdomain
    if (hostname === "beatindablock.wordpress.com") {
      const newUrl = `https://beatindablock.com${pathname}${search}`;
      return Response.redirect(newUrl, 301);
    }

    // 2. Redirect www to apex
    if (hostname === "www.beatindablock.com") {
      const newUrl = `https://beatindablock.com${pathname}${search}`;
      return Response.redirect(newUrl, 301);
    }

    // 3. Legacy URL redirects
    const legacyTarget = LEGACY_REDIRECTS[pathname] ?? LEGACY_REDIRECTS[pathname.replace(/\/$/, "")];
    if (legacyTarget) {
      return Response.redirect(`https://beatindablock.com${legacyTarget}`, 301);
    }

    // 4. Pass through to origin (Cloudflare Pages)
    return fetch(request);
  },

  // Cron trigger: refresh RSS cache in KV
  async scheduled(event, env, ctx) {
    ctx.waitUntil(refreshRssCache(env));
  },
};

async function refreshRssCache(env) {
  try {
    const feedUrl = env.RSS_FEED_URL ?? "https://beatindablock.com/feed/podcast";
    const res = await fetch(feedUrl, {
      headers: { "User-Agent": "BeatinDaBlock-Worker/1.0" },
    });
    if (!res.ok) return;
    const xml = await res.text();
    // Cache for 1 hour
    await env.RSS_CACHE.put("latest-feed", xml, { expirationTtl: 3600 });
  } catch (err) {
    console.error("RSS cache refresh failed:", err);
  }
}
