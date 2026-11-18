# 04 — Taste Skill
https://github.com/Leonxlnx/taste-skill · Agent skill repo (Claude Code plugin / Codex / `npx skills`; skill name `design-taste-frontend`, "tasteskill 2.5.1") · MIT · ~118.2k stars (GitHub page, 2026-11-18) · commit f6b7657, 2026-11-07

## 1. What it is
A single, very large, opinionated skill for building company websites "at the figma.com / x.ai bar". It pairs a long rulebook (SKILL.md + 22 references, ~5,900 lines) with a CSS/JS kit, a 64-palette and 39-pairing library, and Node scripts that "deal" design choices at random and then check the page in headless Chrome until a finish gate passes. Other skills (high-end-visual-design, minimalist-ui, industrial-brutalist-ui, gpt-taste, imagegen-*, brandkit...) moved to `taste-skill-classics` and `imagegen-skills` repos; this repo holds only this one.

## 2. How it works
1. **Classify the business** into a kind: software / gaming / tech (hardware) / product / service / place (cafe, bakery, shop, guesthouse...). The kind gates everything: effects, dark pages, shaders, loops, counters and CSS grounds are tech-only; "other" kinds get photographs, flat colour, type, real icons, hero entrance, one dealt moment, hover layer.
2. **Arm the gate** (`gate.mjs --start`), **write all copy first** (fact sheet from brief, a "voice card", one of 12 registers, device budget).
3. **Plan in screens**: line 1 kind, line 2 the deal, one line per section (id, one idea, picture kind, 1 or 2 screens).
4. **Deal, never choose by taste** (the randomisation mechanism):
   - `assets/layout/deal.mjs` picks one of ~11 heroes at random, weighted per page type from `heroes.json`, filtered by which material the brief has (`--has photo,ui,film,object,setting`), avoiding recent ones in `.taste-skill/layout-history.json` ("never the same within three pages"). Place pages never deal: fixed place hero.
   - `scripts/start.mjs deal --page <kind> --trade <trade>` prints 3 palettes + 3 font pairings; agent must take the **first** (next only if it clashes with client logo/photos). Palettes: filtered (bg chroma < 0.045, accent not violet, no `flat-loud` tag, no dark bg off tech, light/quiet grounds for place), trade-matched ones first, Fisher-Yates shuffled with `Math.random`, the folder's last 12 palettes (and optionally last 6 per trade across folders via env `TASTE_SKILL_RECENT`) pushed to the back. Fonts: weighted pick where the kind-fit weight (1-3) is **cubed**, recent faces dimmed (x0.15 if built in last 3, x0.5 if dealt), a class already picked dimmed x0.15. Place pages pick one per group (serif / plain sans / soft sans) with the trade's group first (serif for bakery/restaurant/guesthouse, plain sans for shop/workshop/florist, soft sans for cafe/yoga).
   - `start.mjs css` prints the `:root` token block (must be kept as printed); `start.mjs brand` uses the client's own colours instead.
   - `moments.mjs pick` deals 1 (2 on 8+ sections) "award-site moments", seeded (`--seed`, else random bytes) and cycled through history.
   - Nav / footer / close / rhythm / button style / logo mark: a one-line `node -e` that picks uniformly at random from pipe lists per kind (e.g. software nav `nav-mega|nav-cards|nav-centre`; place also deals photo compositions `pair|strip|tall-small` and `bleed|trio|strip|pair|wall|story`, type moment `address|name`).
   - No fixed seed for palettes/fonts/layout: plain `Math.random` plus history files = variety across builds in the same folder.
5. **Build** from `starter.html` with kit classes only. 6. **Check**: copy-lint (no browser), consistency.mjs (11.5k lines, hundreds of check ids), layout check.mjs at 5 viewports, shoot.mjs screenshots, perf.mjs; then `gate.mjs` until `GATE: PASS`/`OPEN` (max 3 rounds). In Claude Code the gate also runs as a **Stop hook** from frontmatter. 7. **Report**: gate line, waivers, deal and why, stand-in photos, assumed facts.

## 3. Rules
- [process] Classify the business kind first; let it decide effects, darkness, motion budget and section plan
- [process] Deal palette, fonts, hero, nav/footer/close/button style from curated lists with history; record the deal at top of `<body>`; never pick by taste
- [process] Write all copy before layout, from a fact sheet; invent nothing except a searched coined name and marked assumed hours/prices (`data-assumed`)
- [layout] One section per screen: hero alone on screen 1 at 1440x900; every section exactly 1 or 2 viewport heights; no neighbour heading peeking in
- [layout] One `.wrap` (1280 max, 80px gutter; place 1200/120) for header, sections and footer; equal left/right edges, 12-col grid, 24px gap
- [layout] Max two text start lines (left line + one split line); splits always text left, visual right, never alternating; no centred blocks wider than half the wrap
- [layout] Section separation only by full-width ground change or space; no hairlines/shadows between sections, no inset coloured "band" boxes
- [layout] Card layout (2x2, bento, three cards...) max twice a page; neighbours never share a layout
- [layout] Merge blocks under ~495px (quote, logo row, FAQ) into the section above; no strip sections
- [components] Card: barely there, one step off page, 1px border 8-14% ink, no resting blur shadow; two box levels max, never card-in-card or glass
- [motion] Hover is mandatory: linked card lifts 2px (border darkens, optional soft shadow on hover only), photo zooms 1.02-1.03 inside `overflow:hidden` frame (600ms in/400 out), buttons step up 1px and press 1px down + scale .985, underlines draw left-to-right, arrows move 3px; fine pointer only
- [motion] Unlinked card does not move (`.m-nolift`); no tilt, glow, magnetic buttons, carousels, timed tabs, marquees
- [motion] Hero enters once on load (~1.1 s, h1 line by line from word masks, picture settles 1.05 to 1); never a loader or second entrance
- [motion] No scroll reveals/fades/staggers, no parallax on text, no smooth-scroll libs; only the dealt moment's own section may react to scroll
- [motion] Tokens: 150ms in, 120ms out, 90ms press; one ease-out cubic-bezier(.2,.8,.2,1), no overshoot; animate transform/opacity only
- [motion] Anything moving >5 s gets a pause button; reduced motion shows finished stills
- [colour] UI 90-95% neutral; colour from photos, product, real logos; one accent max (primary button, focus, links), <3% of screen elsewhere
- [colour] Never violet/lavender in the page's own design: OKLCH hue ~270-330 is pushed to 255 (blue) or 345 (rose); a deal returning violet is re-dealt; third-party logos keep their colours
- [colour] Near-black ink (never #000), often warm; main ground white or a low-saturation tint from the client (walls, shopfront) covering 55%+ of page height
- [colour] Dark pages and dark heroes are tech only; other kinds: one dark or one brand-colour band max, second half of page
- [colour] Product/service/place: flat colours only, no gradients, grain, texture, glass, backdrop-filter
- [type] Never Inter, Roboto, Open Sans, Lato, Montserrat, Poppins, Space Grotesk, Plus Jakarta Sans or system font
- [type] One family or display + text; max 4 font files; headlines weight 400 (500 tech), never 700/800; tight tracking -0.5% to -4.5% at 40px+
- [type] Body 16px+, line-height 1.5-1.8, 7:1 contrast; muted only for labels/meta; nothing under 13px; lines max 62 chars
- [type] Sentence case everywhere; no tracked caps or small caps labels; highlight by contrast, never coloured marker bars
- [image] Real photographs lead on non-tech pages (place: 12-20 full page, 8-12 compact, <8 = 3-screen short page); no captions under images; credits in one footer line
- [image] Stock/library frames only for detail slots (hands, tools, materials), max 1 in 3, unless draft path; stand-ins listed in report, never passed off as the client's
- [image] Place hero: one full-bleed daylight photo of the actual place, nothing on it; words on the ground below
- [image] No words on photos except hero and one closing band (not on places); no scrim/gradient over photos; no rounded or filtered photos on a place
- [icon] Real full-colour brand icons (fetched), never drawn look-alikes
- [copy] h1 names category + buyer or place; one hard fact on screen 1; noun in every heading; buttons verb + object; main action worded identically in nav, hero, close, phone bar
- [copy] No testimonials, figures or reviews unless the brief gives them verbatim
- [nav] Fixed opaque header, 1px hairline, no blur/shrink/hide/floating pill; 4-6 one-word nouns; full-screen sheet menu on phone
- [nav] Place pages: fixed bottom action bar on phone, appears once the hero button scrolls away
- [forms] Visible labels, 48px fields, errors under fields on submit, success only after a real send, never `action="#"`
- [seo] Title "Name: what for whom/where", one-sentence description, OG image = screenshot of own hero, canonical only when domain known
- [a11y] Skip link, focus ring shown instantly (no transition), heading order, 44px tap targets, `lang` set
- [perf] Budget: images <1200 KiB total, single <350 KiB, fonts max 2 families/4 files, CLS <0.1, LCP <4.5 s (CPU)
- [brand] Contacts: street and district only, no house number/postcode, no real-format phone, `.example` emails (built for demos)
- [qa] Check at 1440, 1024, 820, 768, 390 and 320 in a real headless browser; iterate on a capped number of rounds; waive false FAILs with a reason, never game the checker
- [qa] Section variety on a place without effects: offer and place sections use different photo compositions; one large type moment (address or name)

## 4. AI tells / anti-patterns it bans
- Copy slop words (delve, elevate, unlock, seamless, cutting-edge, bespoke, robust, nestled...) and stock lines ("Unlock the power of", "Whether you're A or B", "Ready to transform your X?", "It's not just X, it's Y")
- Second-gen tells: one warm/wry "house voice" for every client; invented specifics (batch numbers, times, unsourced %); strip of 3-4 stats under the hero; "X. Y." two-fragment headings; number-pair headings; "not X but Y" and substitutes; "No X. No Y." runs; virtue words (honest, calm, quiet, genuinely); dry closer on every paragraph; footer sign-off/pun; origin-story template; three polished testimonials; default cast names (Priya, Okafor, Marcus...; Acme, Kestrel, Lumen...); eyebrow + heading + lede + 3 cards on every section; "Most popular" plan; step numbers on parallel features; "Since [year]" repeats; em dashes; exclamation marks; process talk ("Below you'll find")
- Over-correction table: banning one tell breeds the next (no em dash -> comma splices; no hype -> calm virtue words; avoid threes -> everything in pairs)
- Visual: violet/lavender, gradients/grain/glass off tech, dark sections off tech, scroll fade-ins, parallax, tilt cards, carousels, logo marquees, twinkling/glitter, card > patterned panel > white card nesting, big stat rows, check-icon lists, logo walls, captions under images, "sample/example" notes, popups/chat bubbles/back-to-top, sticky elements, centred hero (except one dealt variant), mirrored zig-zag splits, the generic Inter/Poppins/Space Grotesk fonts, bold huge headlines
- Mood stock or drawings in place of the actual product/place; a product page that never shows the product

## 5. Data, assets and scripts it ships (and what they need: Node, Python, Chrome)
- `library/palettes.json`: 64 palettes (id, name, tags, trades, bg/surface/ink/muted/accent/accentInk, optional dark `fields`, prose note, `seenIn` source sites). Trades: agency 26, game 21, consumer-product 20, studio 17, retail 14, hardware 14, restaurant 13, bakery 12, cafe 11... Tags: light-neutral 18, earth 13, mono-accent 11, dark-neutral 10...
- `library/type.json`: 39 Google Fonts pairings (id, class, kind weights 1-3, moods, display/text/mono family + weights + tracking + axis, `suits`, optional place group serif 9 / plain 5 / soft 4). Classes: neo-grotesk 19, serif 9, geometric 6. Examples: Geist, Host Grotesk, Mona Sans, Funnel, Bricolage/Figtree, Fraunces/Figtree, Newsreader/Hanken, EB Garamond/Jost, Instrument Serif/Sans
- `assets/`: system.css/js, motion.css/js, starter.html, 11 hero demos + heroes.json, UI fragments, diagram cards, `fx-*` components, moments (13 dealt), shader effects/scenes (tech), vetted photo library (Wikimedia/Unsplash WebP + photos.json)
- `scripts/`: start.mjs (deal/css/brand), moments.mjs, photos.mjs (pick/search Wikimedia Commons/fetch/credits), icons.mjs (fetch real logos), copy-lint.mjs, consistency.mjs, shoot.mjs, perf.mjs, gate.mjs, effects.mjs
- Needs: **Node 22+**, **Chrome/Edge/Chromium** (headless, WebGL on CPU), ffmpeg optional; network only for photo/icon fetching. No Python. Installs a Stop hook in Claude Code.

## 6. Area
design, motion, QA, tooling (with strong copy rules)

## 7. Take / skip
Take:
- The "deal from curated lists + history file" mechanism: exactly our need for two funeral homes or two fabrication shops not looking alike. Copy the pattern (trade-tagged palettes, weighted font pick, recent-avoidance, take the first result, write one sentence on why it fits the trade) with our own lists and niches (funeral, metal fab, trades)
- Classify the business kind first and let it gate effects (local trades = photos, flat colour, type; no shaders)
- The copy-tells list, device budget and over-correction table; a lint for slop words and stock phrases
- Equal edges, one wrap, two text lines, no zig-zag, card layout max twice, neighbours differ
- Hover layer numbers (2px lift, 1.03 zoom, 150/120ms, no overshoot) and the "no scroll fade-ins" ban
- Banned font list, 400-weight headlines, 16px body, sentence case, no tracked-caps eyebrows
- Real-browser QA at multiple widths with a capped fix loop; report stand-in photos and assumed facts
Skip / adapt:
- The violet hard ban: fine as a default for our clients, but make it overridable when the client's brand is purple
- "Exactly 1 or 2 viewport heights per section" and pixel-exact rules: too rigid for Elementor and real client content
- Contact obfuscation rule 9 (no house numbers, `.example` emails): suits demos; our real redesigns need real NAP data for local SEO
- The huge kit (11.5k-line checker, shaders, scenes, moments): too heavy to port to WordPress/Elementor; keep ideas, not code
- Mandatory hover on every card and a "dealt moment" on every page: OK for Vercel mockups, keep optional for Elementor builds
- Using Wikimedia stand-ins on outreach mockups: OK only if clearly listed internally; prefer the prospect's own photos scraped from their site/Google profile

## 8. Open questions
- How well does the random deal hold up across many sites in one niche (only 11-13 palettes per place trade)? Our own niche lists will need more depth.
- Star count (118.2k) taken from GitHub page via WebFetch; looks high, verify.
- Mandatory hover lift/zoom conflicts with advice elsewhere that warns against hover-lift cards as an AI tell; decide our stance.
- SUGGESTED: taste-skill-classics - https://github.com/Leonxlnx/taste-skill-classics - older lighter skills (minimalist-ui, industrial-brutalist-ui, high-end-visual-design) may be easier to port than the 2.5 kit
