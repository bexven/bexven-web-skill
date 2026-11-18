# 44 — Unsplash
https://unsplash.com · Website / stock photos + API · Unsplash License (custom, not CC0) · Stars n/a · read 2026-11-18 (/license + API guidelines)

## 1. What it is
Free high-resolution stock photo library under its own Unsplash License, plus a public API.
## 2. How it works
Licence: an "irrevocable, nonexclusive, worldwide" right to download, copy, modify, distribute and use photos, commercial use included, without asking permission. Attribution is not required (it is a courtesy). Restrictions: you can't sell images "without significant modification", and you can't compile images to build a competing service. The licence page doesn't cover endorsement, identifiable people or trademarks, and there are no model or property releases, so the risk stays with us.
API (key from the Unsplash developer portal; keep the Access/Secret key on the server): you must hotlink the `photo.urls` images, call `links.download_location` when a user picks a photo, and credit the photographer and Unsplash with links that carry `?utm_source=<app>&utm_medium=referral`. Don't use "Unsplash" in the app name and don't copy its core experience.
## 3. Rules
- [image] Use stock only as clearly marked placeholders in cold-outreach mockups (e.g. a `data-placeholder="replace-with-client-photo"` attribute plus an HTML comment, and a note in the hand-off). The real build uses the client's own photos
- [image] Never use stock people as staff, owners, clients or "families we served". No invented testimonials or headshots
- [image] Funeral homes: no identifiable grieving people. Prefer hands, flowers, light, architecture and landscape, and nothing that suggests a real family is endorsing the business
- [image] For mockups, download, optimise (AVIF/WebP, sized) and self-host. Hotlinking applies only when you use the API
- [tooling] If we script the API: call download_location, show the credit with UTM links, and keep the key out of client code
- [copy] Add a credit line in the mockup even though it isn't required. It's polite and makes swapping photos easier
## 4. AI tells / anti-patterns it bans
n/a. Our ban: the familiar Unsplash hero shots (laptop and latte, handshake, generic smiling team) mark a site as a template.
## 5. Data, assets and scripts it ships
Photos plus a REST API (needs a key). Nothing to run.
## 6. Area
design / tooling
## 7. Take / skip
Take: a quick source of mood and placeholder images for the Vercel redesign. Skip: stock in final WordPress builds wherever the client can supply real photos, and the API, since a manual download is enough for a few mockups.
## 8. Open questions
Rate limits for demo and production keys weren't shown on the guidelines page. Endorsement and people limits are in Unsplash's Terms/FAQ (not read).
