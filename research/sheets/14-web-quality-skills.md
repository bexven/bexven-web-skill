# 14 — Web quality skills (addyosmani/web-quality-skills)
https://github.com/addyosmani/web-quality-skills · Agent skill repo (6 skills, Claude Code plugin + Codex + Gemini) · MIT (c) 2026 Addy Osmani · 3.1k stars · commit afa8da9, 2026-08-24 (plugin v2.0.0)

## 1. What it is
Six framework-agnostic, Lighthouse-based quality skills: `web-quality-audit` (orchestrator), `performance`, `core-web-vitals`, `accessibility` (WCAG 2.2), `seo`, `best-practices`. v2 is "measurement-first": it insists on keeping field data, lab traces and source-code guesses apart, and it removed made-up ranking percentages and generic savings estimates. It covers QA and development only. It has nothing on visual design.

## 2. How it works
- Audit loop: (1) set the scope: which URLs, states/journeys, logged-in or public, mobile/desktop; (2) if the page runs, take a live baseline before reading the code; (3) use the runtime failures to decide which source files to inspect; (4) sort findings by impact and confidence, then fix; (5) re-run the same checks and say what is verified and what still needs field data or a human.
- Tool routing: perf goes through a browser trace plus focused insights (Chrome DevTools MCP `performance_start_trace` / `performance_analyze_insight`, insights such as LCPBreakdown, LCPDiscovery, DocumentLatency, RenderBlocking, ThirdParties). A11y/SEO/Best Practices/"Agentic Browsing" go through `lighthouse_audit`, which leaves out performance on purpose. Fallbacks in order: Lighthouse CLI, then PageSpeed Insights UI, then CrUX Vis, then CrUX API (needs a key, so never a prerequisite), then static inspection labelled "hypothesis".
- Evidence hierarchy: CrUX field data (p75, rolling 28 days) shows user impact. Traces/Lighthouse diagnose the cause. A `PerformanceObserver` snippet is a single-session lab observation, never field data. Missing CrUX means "unavailable", not "passing".
- A lab/field reconciliation table (poor/poor = real problem; field poor + lab good = the lab missed real conditions; field good + lab poor = fragile, but don't claim users are failing).
- Output format: evidence table first (signal | scope/conditions | baseline | after | source), then findings by severity (Critical / High / Medium / Low). Each finding has Impact, Evidence type and Fix with file:line, then a recommended priority and verification status.
- Progressive disclosure: SKILL.md files are under 500 lines and the detail is in references/ (MEASUREMENT, RUM, LCP, INP, CLS, WCAG, A11Y-PATTERNS, STRUCTURED-DATA, SECURITY).

## 3. Rules
- [perf] LCP good ≤2.5s, needs improvement 2.5–4s, poor >4s; INP ≤200ms / 200–500 / >500ms; CLS ≤0.1 / 0.1–0.25 / >0.25. Judge at field p75, never on one lab run
- [perf] All three p75 values must be "good" for a route to pass. Never use averages
- [perf] TTFB <800ms (CDN, edge/HTML caching, fewer redirects, watch serverless cold starts)
- [perf] Starting budgets (calibrate per project): total page <1.5MB, JS <300KB compressed, CSS <100KB compressed, above-fold images <500KB, fonts <100KB, third-party <200KB
- [perf] Inline critical CSS under ~14KB. Load the rest via preload+onload with a noscript fallback. No CSS `@import`
- [perf] Scripts use `defer`/`type=module`. `async` only for independent scripts (analytics). No parser-blocking JS in `<head>`
- [perf] Preconnect to required third-party origins. Preload only what the trace shows is discovered late, because extra preloads compete for bandwidth
- [perf] Brotli over gzip. Use HTTP/2 or HTTP/3. Consider 103 Early Hints only when a trace shows slow HTML generation
- [perf] Cache: HTML `no-cache, must-revalidate`; hashed assets `max-age=31536000, immutable`; unhashed `max-age=86400, stale-while-revalidate=604800`
- [perf] Speculation Rules prerender starts at `conservative`/`moderate`. Exclude logout/checkout. Gate analytics on `prerenderingchange`. Chromium-only progressive enhancement
- [perf] Cross-document View Transitions via `@view-transition { navigation: auto; }` (snapshot doesn't count toward CLS)
- [perf] Use facades for YouTube/maps/chat widgets. Load widgets on IntersectionObserver or on interaction
- [perf] For lab decisions run ≥3 equivalent navigations and report median + range with tool version, viewport, CPU/network throttle, cache state and consent state
- [perf] Mobile conditions by default for public sites. Test desktop separately
- [image] The LCP image must be a real `<img>` in the initial HTML (not a CSS background, not JS-rendered), with `fetchpriority="high"` and `loading="eager"`. Never lazy-load it
- [image] Below-fold images get `loading="lazy" decoding="async"`
- [image] Use `<picture>` AVIF, then WebP, then JPEG with `srcset` widths (example 400/800/1200w) and `sizes`. SVG for icons/logos, PNG only when transparency is needed
- [image] Always set `width`/`height` attributes or CSS `aspect-ratio`, using the real intrinsic ratio (a wrong ratio distorts the image; use `object-fit: cover` when cropping)
- [image] Use descriptive filenames (`blue-widget-side.webp`, not `IMG_12345.jpg`)
- [type] Use WOFF2 with `font-display: swap` (or `optional` for non-critical fonts). Preload only the critical heading/body file, with `crossorigin`
- [type] Subset with `unicode-range` (e.g. Latin U+0000-00FF). Prefer one variable font file over several static weights
- [type] When the font swap causes CLS, tune a metric-matched local fallback with `size-adjust` / `ascent-override` / `descent-override` / `line-gap-override`, derived from the real font pair (don't copy the values)
- [type] Body text 16px with line-height 1.5 for mobile readability. Never 10–12px body
- [motion] Animate `transform`/`opacity` only, not width/height/top/left. Use rAF instead of setInterval
- [motion] Respect `prefers-reduced-motion: reduce` (their snippet effectively turns off all animation and smooth scroll)
- [layout] Reserve space for embeds/ads/async blocks (aspect-ratio boxes, fixed slots). Never prepend banners, consent UI or notices above visible content
- [layout] Content reflows at 320px width with no horizontal scroll and stays usable at 200% zoom
- [a11y] Contrast AA: 4.5:1 normal text, 3:1 large text, 3:1 UI components/focus rings. AAA is 7:1 / 4.5:1
- [a11y] Never use only colour for state. Errors combine colour + icon + text
- [a11y] Targets at least 24×24 CSS px (WCAG 2.2 AA). 44×44 recommended (the SEO skill says 48×48)
- [a11y] Use `:focus-visible` outlines (2px solid currentColor, 2px offset). Never strip focus without a replacement
- [a11y] Focus must not be hidden under sticky headers: `scroll-margin-top` (~80px) / `scroll-margin-bottom`
- [a11y] Skip link to `#main-content` as the first element of the page
- [a11y] Native elements before ARIA. Icon buttons need `aria-label` or visually-hidden text, with the SVG `aria-hidden`
- [a11y] `<html lang>`, a logical heading order, landmarks (`header/nav/main/footer`), and `aria-current="page"` in nav
- [a11y] Repeated help (phone, chat, contact link) sits in the same relative position on every page (WCAG 3.2.6)
- [a11y] Captions on video and transcripts on audio. No autoplay without controls
- [forms] Every input has a programmatic label (placeholder alone fails) plus an `autocomplete` token
- [forms] Errors: `aria-invalid`, `aria-describedby` pointing to the message, `role="alert"`/live region, and focus moves to the first error on submit
- [forms] No redundant entry: offer "same as billing" or pre-fill. Allow paste/autofill on passwords
- [seo] Unique `<title>` per page. 50–60 chars is only a lint hint. Meta description ~150–160 chars, also only a hint
- [seo] Do not fail a page just for having more than one `<h1>`. Do require a descriptive primary heading and no skipped levels
- [seo] Self-referencing canonical. robots.txt must not block CSS/JS. Sitemap holds only canonical, indexable URLs (max 50k URLs or 50MB)
- [seo] URLs are lowercase, use hyphens, stay under ~75 chars and avoid parameters
- [seo] Link text is descriptive, never "click here" or "read more". Add breadcrumbs on deep pages
- [seo] JSON-LD must describe visible content only. Use the most specific type and validate in the Rich Results Test
- [seo] AI crawlers: audit each user agent separately (OAI-SearchBot, PerplexityBot, Claude-SearchBot/Claude-User, Google-Extended; GPTBot/ClaudeBot are for training). Blocking Google-Extended does not affect Google Search
- [seo] `llms.txt` is optional and experimental. Never sell it as a ranking or citation factor
- [code] Put `<!DOCTYPE html>` first, then `<meta charset="UTF-8">` as the first element in head, then viewport `width=device-width, initial-scale=1`
- [code] No duplicate IDs, no `<a><button>` nesting, no `<div>` inside `<ul>`. Use semantic HTML5
- [code] No `document.write`, no sync XHR. Make touch/wheel listeners passive. Use feature detection or `@supports`, never UA sniffing
- [code] Clean console in production. Don't ship public source maps (use hidden maps and strip `sourcesContent`)
- [code] Security: HTTPS with no mixed content, HSTS (only once every subdomain is HTTPS), CSP using nonces/hashes rolled out report-only first, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy`, and no `X-XSS-Protection`
- [code] Pin third-party CDN scripts with SRI. Never use polyfill.io-style third-party polyfill CDNs. Self-host
- [code] Ask for permissions (geolocation etc.) only after a user action, with an explanation. No intrusive mobile interstitials
- [qa] Before every deploy: CWV passing, zero axe/Lighthouse a11y errors, zero console errors, HTTPS, meta tags present
- [qa] Lighthouse guardrails: Performance ≥90, Best Practices ≥95, SEO ≥95, A11y "aim for 100 automated, then do manual checks". Scores only catch regressions and prove nothing
- [qa] Manual a11y pass: Tab through the whole page, screen reader (VoiceOver/NVDA/TalkBack), 200% zoom, Windows High Contrast, reduced motion, focus order matches visual order, target sizes
- [process] Never claim a field improvement right after deploy (CrUX lags about 28 days). Report "lab verified, field pending"
- [process] Label every static-only finding as a hypothesis and include the exact command/workflow that verifies it
- [process] Don't attach generic "saves X ms" claims. Measure the LCP subpart before and after
- [tooling] Token hygiene: one trace + one Lighthouse run first, write big reports to files, take text snapshots before screenshots, filter/paginate network and console output

## 4. AI tells / anti-patterns it bans
It has no aesthetic bans. Its "tells" are about quality and evidence:
- Claiming ranking boosts, percentage savings or "users are failing" without field evidence. Treating a Lighthouse score as proof of a11y, security or SEO.
- Hard metadata limits (title must be ≤60) and "only one H1" failures. v2 removed these on purpose.
- Lazy-loading the hero/LCP image. Hero as a CSS background. Hero text fetched client-side.
- Speculative `preload` spam. `outline: none` without a replacement. Click handlers on `<div>`. ARIA where native elements exist.
- Prepending banners/cookie bars that push content down. Images without dimensions.
- `polyfill.io`, `X-XSS-Protection`, exposed source maps, `document.write`.
- Adding WebMCP or `llms.txt` just to raise an audit score.

## 5. Data, assets and scripts it ships (and what they need: Node, Python, Chrome)
- `skills/web-quality-audit/scripts/analyze.sh`: a read-only bash + grep smoke test on .html files (doctype, UTF-8 charset, viewport, `lang`, `<title>`, `<img>` without alt, `http://` URLs). Outputs JSON. **Needs `jq`** (exits otherwise). No Node or Chrome. Max 100 findings, 20 per category per file. Not run, per the brief.
- No other scripts or data files. Everything else is markdown with code snippets.
- External tools the skills expect (optional, with fallbacks): Chrome DevTools MCP (Chrome); Lighthouse CLI (`npx lighthouse ... --only-categories=accessibility`, Node + Chrome); `@axe-core/cli` (Node); PageSpeed Insights / CrUX Vis (web, zero setup); CrUX API (Google Cloud key); `web-vitals` npm library for RUM; `npm audit`. Repo dev tooling: Node 18+, `skills-ref`, markdownlint.
- Packaging: `.claude-plugin/plugin.json` + marketplace.json, a Codex plugin, `gemini-extension.json`.

## 6. Area
QA / development (performance, a11y, SEO, security). It has no design, brand or motion-aesthetics content.

## 7. Take / skip
Take:
- The **evidence model and report format** (evidence table, then severity buckets, then "verified / field pending") as Bexven's QA step for both the Vercel static mockup and the WP build. It reads well for clients too.
- The **CWV thresholds, budgets and LCP-hero rules** (real `<img>`, `fetchpriority=high`, eager, AVIF/WebP `<picture>`, dimensions). These matter most for image-led niche sites (funeral homes, fabrication-shop photo heroes). Elementor's default section-background hero is exactly the anti-pattern, so the WP stage needs an explicit "hero as Image widget" rule.
- **Font rules as a constraint on distinctive typography**: the <100KB font budget plus variable fonts, subsetting, WOFF2, swap and metric-matched fallbacks. These let us use unusual typefaces without a perf penalty and should sit next to our "no generic fonts" rule. Self-host instead of Google Fonts CDN (that saves a preconnect).
- **WCAG 2.2 specifics** (24px targets/44px comfortable, focus-visible ring, scroll-margin under sticky headers, consistent help position, error pattern). Focus-not-obscured and consistent help apply directly to our sticky headers and phone-number CTAs.
- The **CLS rules** for cookie banners and announcement bars. Most agency sites fail here.
- Tap target and 16px/1.5 body-text floors as hard minimums in design tokens.
- Security headers + SRI + the "no third-party polyfill CDN" rule for vercel.json headers.
- `analyze.sh` checks as an idea: rewrite our own tiny check (Python or Playwright) instead of depending on jq.
Skip:
- RUM/`web-vitals` pipeline, Trusted Types, React/Next/Nuxt specifics, service workers, list virtualization, prototype-pollution notes. Too heavy for brochure sites. Mention RUM only for the paid WP stage if asked.
- Speculation Rules `href_matches: "/*"` defaults (risky on WP with logout/cart URLs). Use `conservative` and an exclude list if at all.
- Generic structured-data examples (Product/Article/FAQ). Bexven needs **LocalBusiness subtypes** (FuneralHome, HomeAndConstructionBusiness etc.), which this repo lacks. FAQ rich results have been limited to government/health sites since 2023 and the repo doesn't say so.
- `rel=prev/next` (Google no longer uses it) and sitemap `changefreq`/`priority` (Google ignores them). Both still appear in its SEO examples.
- The blanket reduced-motion kill-switch. Ours should swap motion for fades/static states deliberately, not zero out every transition.
- Monthly/weekly "review" checklists (process for in-house teams, not one-off client builds).
Corrections to carry forward (bugs in source):
- "Large text ≥18px / ≥14px bold" is wrong. WCAG large text is 18pt (24px) or 14pt bold (about 18.66px). Use the correct values.
- The responsive `<picture>` "hero" example uses `loading="lazy"`, which contradicts its own LCP rule. `alt="" role="presentation"` is redundant.
- Tap targets disagree internally: a11y says 24 min / 44 recommended, SEO says 48. Pick 44–48 for primary CTAs.

## 8. Open questions
- Conflicts with common design advice: it mandates `transform`/`opacity`-only animation and blanket reduced-motion, which limits "expressive motion" advice; the font budget (<100KB) caps multi-family type pairings (two variable families max in practice); it has no stance on hover effects, colour palettes, eyebrows or light/dark (QA-only). It recommends a system-font fallback stack (`-apple-system, Segoe UI, Roboto`), which is fine as a fallback but must not become the visible face.
- Elementor/WordPress isn't covered at all (plugin bloat, Elementor CSS/JS weight, image-optimiser plugins, caching plugins). We need our own WP perf notes.
- Do we want Chrome DevTools MCP in our environment? The brief says don't install. Without it the fallback is Lighthouse CLI via Node + Chrome, or Playwright (we already use it) with a `web-vitals` injection for lab-only readings.
- SUGGESTED: Chrome DevTools MCP tool reference - https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md - the live-audit tool names this repo routes everything through.
- SUGGESTED: Google Search Central LocalBusiness structured data - https://developers.google.com/search/docs/appearance/structured-data/local-business - the schema our niche clients actually need, missing here.
- SUGGESTED: web.dev "Optimize web fonts" / font fallback (size-adjust) tools such as Fontaine or capsize - https://web.dev/learn/performance/optimize-web-fonts - to make distinctive custom fonts cheap.
- No URL failures. Star count came from WebFetch (3.1k).
