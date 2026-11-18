# 16 — Elementor MCP
https://elementor.com/roadmap/ + https://elementor.com/changelog/ · Tool · Proprietary service inside Elementor (core plugin GPL-2.0+; Pro is a paid licence) · Stars n/a · Read 2026-11-18 (latest Pro 4.4.1, 2026-11-16)

## 1. What it is
Elementor's own official MCP server, built into the plugin. It lets an MCP client (Claude Code, Claude Desktop, Codex, Cursor, "Other") read and build Elementor pages as native, editable Elementor structures. Introduced in 4.3.0 (2026-09-22) and marked "Released" on the roadmap; press coverage in Sept 2026 called it a beta, and Elementor's own pages no longer use that label. Extended in 4.4.0 (2026-11-09), with fixes in 4.3.3, 4.3.4, 4.3.6 and 4.4.1. It sits next to "Angie", Elementor's agent inside the editor (since 4.1.0, May 2026), which builds pages, design systems, forms and loops from a prompt.

## 2. How it works
- Requirements (help article): WordPress 6.8+ and Elementor Core + Pro 4.3.0+. Whether Pro is truly needed is unclear. The launch blog says basic sections are free and only Pro elements need a Pro plan. The AI gets the same permissions as the WP user (in practice an admin). The changelog's minimum is WP 6.8 (set in 4.1.0). PHP 7.4 is the last minimum stated.
- Setup (do NOT run here): WP admin > Elementor > Elementor MCP > Enable MCP access > choose a client > tick the box > Generate Prompt. This creates a WP Application Password, labelled e.g. "Elementor MCP – Claude Code". You paste the generated prompt into the AI tool. There is also a manual config option. The transport is not documented (it looks like HTTP to the site using the Application Password). 4.3.4 added an error for when Application Passwords are unavailable, and some hosts or security plugins turn them off.
- Revoke: Users > Profile > Application Passwords > Revoke. To cut off every client: Elementor > Elementor MCP > Turn off.
- Tools (4.3): read page structure; build and redesign Atomic (Editor V4) pages and layouts, including a whole page in one call; create, apply and reorder Global Classes and Variables (colours, fonts, sizes), with states (hover etc.) and breakpoints; place, fill or create Components; dynamic data (post fields, ACF, taxonomies); theme parts (header, footer, archive, popup) with display conditions.
- Added in 4.4.0: many legacy (V3) and Pro widgets, forms (with WebMCP for MCP-built forms), popup triggers, renaming elements, Media Library uploads, undo via revisions, cache clearing, System Info and licence info. "Agent Ready" (readiness score, bot access controls) is a separate feature.
- With Angie installed as well: the AI can also reach WordPress Abilities API abilities (WooCommerce, Yoast, ACF, WPForms...) and create custom widgets. Neither page mentions the WordPress MCP Adapter.
- Output is saved as a DRAFT, not published. If the editor and the AI change the same page at the same time, Elementor flags the conflict.
- Roadmap: "Extended MCP tools" (ETA Nov 2026, mostly shipped in 4.4); "MCP Skills" for complex workflows (ETA Q1 2027); Atomic Mega Menu and pre-built atomic structures (4.5, Q1 2027).

## 3. Rules
- [wp] Check Elementor >= 4.3 and WP >= 6.8 and that Application Passwords work before planning an MCP build. If any check fails, use the fallback below.
- [process] Build order through MCP: (1) Variables for the palette, type scale and spacing, taken from the static page's CSS custom properties; (2) Global Classes for the repeated patterns (buttons, cards, section shells); (3) header and footer as theme parts with display conditions; (4) pages built from Atomic containers/grids that use those classes; (5) forms and popups.
- [code] Map the static CSS 1:1. :root tokens become Variables, utility/component classes become Global Classes, flex/grid sections become Atomic flexbox/grid containers. Do not paste inline styles onto each element.
- [brand] Move the exact fonts and colours we chose for the Vercel mockup into Variables. Never accept Elementor's default kit (its default fonts and colours) or Angie's generated design system unchanged. This keeps two sites in the same niche from looking alike.
- [components] Turn repeated blocks (service cards, testimonials, CTA band) into Components so the client edits each one in a single place.
- [qa] Treat the MCP output as a draft. Compare it in the editor with the Vercel page at 375/768/1280 px (Playwright screenshots of both), then publish by hand.
- [qa] Use the revisions-based undo tool when a build call goes wrong. Never hand-edit _elementor_data in the database.
- [tooling] Use the client's admin user and a dedicated Application Password. Revoke it at handover and turn MCP off on live sites when the build is finished.
- [wp] Use legacy V3 widgets only when there is no Atomic equivalent yet (e.g. mega menu before 4.5). V4 Atomic elements are the default for new sites since 4.0.
- [perf] Keep the class count lean (the limit is 1000) and reuse Variables instead of one-off values.
- [process] Fallback without MCP: (a) set the Site Settings / Global Colours + Global Fonts (or V4 Variables + Classes) by hand from the token list; (b) generate an Elementor JSON template (containers with flex direction, gap and padding, using the global colour/font IDs) and import it via Templates > Import, or use a Kit .zip for whole sites; (c) rebuild in the editor by hand, using flexbox containers and never the legacy section/column layout.

## 4. AI tells / anti-patterns it bans
n/a. It is a build tool. Risk: Angie's "design system from one prompt" and its prompt-built pages will drift toward generic AI defaults. Our skill must supply the design system itself and use MCP only to carry it out.

## 5. Data, assets and scripts it ships (and what they need: Node, Python, Chrome)
Nothing to download. The server is built into the Elementor plugin on the client's WordPress site. It needs an MCP-capable client and a reachable site with Application Passwords enabled. Some abilities need the separate Angie plugin.

## 6. Area
tooling / development (WordPress build stage)

## 7. Take / skip
- Take: MCP as the main route from the approved Vercel mockup to an Elementor build, in the order Variables > Classes > theme parts > pages. Keep draft-then-review and revoke-at-handover.
- Take: the JSON template / kit import fallback for hosts where MCP or Application Passwords are blocked, or for sites older than 4.3.
- Skip: letting Angie design. Skip Agent Ready and the Abilities API extras for now, since they are not needed for a visual rebuild.
- Never install anything or enable MCP from the skill without the user's explicit OK on the client site.

## 8. Open questions
- Is Elementor Pro required for MCP at all? The help article lists Core + Pro 4.3.0. The launch blog says basic features are free.
- The transport and the manual config format are not documented on the pages read (only a generated prompt is described).
- The changelog page is ~580k characters. Only the first 100k (the Pro changelog) was read, so Core-only entries may be missing. The roadmap and changelog disagree on some ETAs (List and Carousel are already shipped in 4.4.0).
- SUGGESTED: Elementor Help "How to Build and Edit Your Site Using Elementor MCP" - elementor.com/help - the real tool list and prompt examples.
- SUGGESTED: msrbuilds/elementor-mcp (third-party, 61–118 tools, works on older and free installs) - https://github.com/msrbuilds/elementor-mcp - possible fallback when the official MCP is unavailable.
- Sources also read: elementor.com/blog/elementor-mcp-launch/, elementor.com/help/?p=171107, plus one WebSearch.
