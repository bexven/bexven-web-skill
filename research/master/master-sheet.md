# Bexven web-design master rule sheet

Version 1.0 · 2026-11-18 · Tells list: v2026-11 (review quarterly)
Inputs: `sheets/01–47`, `analysis/duplicates.md` (218 canonical rules), `analysis/conflicts.md` (C1–C33), `PLAN.md` §2–§3.

**Purpose.** One merged, de-duplicated rule set for Bexven's web-design skill. Scope: local-business client sites, built first as a static HTML/CSS redesign on Vercel (cold outreach), then as a full WordPress/Elementor site once the client says yes. Every rule is written in our own words; sources are cited, not quoted. This sheet is the source the four skills (`direction`, `build`, `elementor`, `qa`) and their reference files are cut from.

**How to read a line.** `- [area] Rule. {src: NN,NN}`
- `[area]` is the topic tag: `[process] [brand] [type] [colour] [layout] [space] [components] [nav] [forms] [image] [icon] [copy] [motion] [a11y] [perf] [seo] [code] [wp] [qa] [tooling]`.
- `{src: …}` lists sheet numbers from `research/sheets/` (e.g. 05 = Impeccable, 10 = Web Interface Guidelines). Rules backed by several sources were merged in `duplicates.md`.
- `{src: Bexven; C4; 01,05,07}` marks a Bexven decision that settles conflict C4 in `conflicts.md`; the numbers after it are the sources that disagreed. `{src: Bexven}` alone is a house rule no source covers (mostly forms, niches, build workflow).
- `(lint)` means the rule must become a mechanical check in `qa/scripts/lint_html.py` or the screenshot script, not just prose.
- Precedence when rules collide: explicit client brief or existing brand > hard floors (a11y, legal, performance) > Bexven defaults > source opinions. {src: Bexven; 01,05,06}

---

## 0. Principles

- [process] AI-made sites converge because a model with no strong context falls back on its most probable answer; every default (font, palette, section order, hover, copy rhythm) is a pull toward the same page. Treat any choice made "because it is normal for websites" as suspect. {src: 01,05,17}
- [process] Take the visual direction from the client's own world (trade, materials, place, era, signage, print, customers' culture), never from web trends or habit. {src: 01,02,04,05,08,17,20,30,47}
- [process] Be conventional in where things are and how they behave (logo, nav, contact, forms, page names); be distinctive in identity and composition (type, colour, imagery, section grammar, one signature). {src: Bexven; C15; 46,05,06,24}
- [process] Spend boldness in one place: one or two signatures applied consistently, everything else quiet (roughly 80% proven patterns, 20% distinctive). {src: 01,03,05,06}
- [process] Remove anything that carries no meaning; before shipping, cut one more accessory. An empty-feeling section is a composition problem, not a call for filler. {src: 01,06,46}
- [process] Tells move: today's recommended replacement becomes next year's default. Never rely on a blacklist alone; pair the dated tells list (§12) with the similar-prompt test and the guessability test. {src: 04,05,17,25,27,31}
- [process] Similar-prompt test: "would a similar prompt for another client in this niche land here too?" If yes, change it and note what changed. {src: 01,05,06,17}
- [process] Guessability test: if the look can be guessed from the category alone (or the category plus our avoid-list), rework it. {src: 05}
- [process] Stranger test: could someone tell which business this is with the logo covered? {src: 01,06}
- [process] Accessibility, performance and legal rules are floors enforced by numbers and checks, not by reminders in the creative brief; boldness ships only if the audit passes. {src: Bexven; C6; 01,02,05,10,14}
- [process] An explicit brief or brand pin beats every anti-tell rule; tells only govern choices the brief leaves open. {src: 01,05,06}
- [process] Give a default, not a menu of equal options, wherever a rule allows a choice. {src: 18}

## 1. Process

### 1.1 Brief intake
- [process] Mock stage (cold outreach): never ask the prospect anything. Infer from their current site, Google Business Profile, photos, signage and reviews, and log every assumption in an `Assumptions` block of DESIGN.md. {src: Bexven; C30; 01,05,06}
- [process] Build stage (client said yes): turn the Assumptions block into the client question list; ask only about the business, never about aesthetics or CSS values. {src: Bexven; C30; 01,05,06}
- [process] Collect before designing: business name, real public NAP, services, service area, hours, existing logo and colours, real photos, real reviews with source, credentials, competitors in the same town. {src: Bexven; C14; 02,14,46}
- [process] Classify the surface first (persuade, inform, operate) and scale ambition to it: local marketing homepages persuade; booking or quote flows operate and stay restrained. {src: 04,05}
- [process] Write the client's unique mechanism (what they do that others don't), the audience scene, and the customers' own words for the services before any visual choice. {src: 05,46}
- [process] Redesign means replacing the old look entirely while keeping content and function; never polish a look you have already decided to discard. {src: 05}
- [process] The designer may add up to 3 human-picked gallery references to a "reference brief"; the agent reads that brief and never crawls galleries itself. {src: 19,21,22,23,24,25}
- [process] Never invent facts at intake: unknown hours, prices, years, counts and credentials stay unknown, marked `data-assumed` and listed in the report. {src: 02,03,04,05,06,46}

### 1.2 The category rut
- [process] Write down "the page this niche always ships" (its hero, palette, fonts, section order, stock photo) in one paragraph, then ban it and its obvious opposite as defaults. {src: 05}
- [process] Look at 3–5 real competitor sites in the same niche and region and note their shared defaults; those defaults go on the per-project avoid list. {src: 05,21,30}

### 1.3 Direction shortlist
- [process] Derive 3–5 directions from the client's world (artifacts, publications, places, rituals, pre-web print forms), spread over at least 3 material families, with at most one taken from the literal trade metaphor. {src: 05,07}
- [process] Each direction differs from the others on at least 2 named axes: type voice, colour strategy, layout grammar, density, imagery treatment, signature moment. Never differ only by accent colour. {src: Bexven; C4; 05,07}
- [process] Write each direction as one sentence of governing idea plus 5–7 key characteristics; a direction that reads like a mood board ("warm, modern, trustworthy") is not decided yet. {src: 03,05,08}
- [process] Open every direction with a concrete reference object, place or era, not a list of adjectives. {src: 08}

### 1.4 Seeded pick
- [process] Drop any direction that collides with the niche history log: same display font, palette family, hero type, section order or motion idea as any of the last 5 sites in that niche. (lint) {src: Bexven; C4; C16; 01,04,17}
- [process] Pick among survivors with a seeded random draw; seed = hash of client domain + date, recorded so the pick is reproducible. {src: Bexven; C4; 04,05,31}
- [process] Write one sentence on why the pick fits this client and append the pick (font, palette family, hero type, section order, motion idea, icon family) to the niche log and the agency log. {src: Bexven; C4; 04}
- [process] The same display font may not appear in 2 of the last 5 Bexven sites overall, or in any of the last 5 in the same niche. (lint) {src: Bexven; C18; 04,05,17,26,27}

### 1.5 Direction contract and DESIGN.md
- [process] Before code, write a short direction contract: thesis, palette and component ideas from the client's world, page story, exact first viewport, colour strategy, mode rationale, the one emphasis device, the one signature. {src: Bexven; C20; 01,02,05,06,08}
- [process] Keep one DESIGN.md per client in the project root: overview, 5–7 key characteristics, tokens in front matter with names and jobs, short Do/Don't lists with reasons, Assumptions, Known gaps, `tells_version`. {src: 03,05,08}
- [process] Tokens are the source of truth; prose explains how they are used. Keep sections in a fixed order and list omitted ones with a reason instead of padding. {src: 08}
- [process] Keep the Don't list short; each item is a hard limit with its reason. A long rambling list means the direction is vague. {src: 03,08}
- [process] After QA, sync DESIGN.md to what shipped (the built page wins on drift) and check every CSS token exists in DESIGN.md and the reverse. (lint) {src: Bexven; C20; 05,07,08}
- [process] Turn every human correction into a class-level rule with its reason (DESIGN.md or the skill's Gotchas list); prefer a lint check over a sentence. {src: 07,18}
- [process] Save the Vercel mock's breakpoint screenshots as the visual reference for the later WordPress build. {src: 12,16}

## 2. Niche layer

- [process] A niche file supplies audience, register, must-have content, trust signals, local SEO type and no-gos. It never supplies a palette, font, hero or section order. {src: Bexven; C16; 02,05,17}
- [process] Two sites in the same niche may not share display font, palette family, hero type or section order. (lint against niche log) {src: Bexven; C16}
- [process] Content inventory comes from the niche; order and composition come from the direction. {src: Bexven; C27; 02,06,46}
- [process] Follow the customers' mental model for page names and IA in the niche; novelty lives in the look, not the menu. {src: 02,46}
- [process] Missing niche file: copy `niches/_template.md`, fill it from competitor research, mark it first-pass. {src: Bexven; 18}

### 2.1 Funeral homes (first pass)
- [brand] Audience: families arranging a funeral in the first 24–72 hours, often on a phone, often at night, often older relatives; second audience: people pre-planning their own funeral calmly, weeks ahead. {src: Bexven; C5; 02,05,46}
- [brand] Register: calm, plain, dignified, warm without being sentimental; quiet confidence, never sales energy, never cheerful. {src: Bexven; 17,28}
- [process] Must-have content: phone number reachable 24/7 shown in the header, services (burial, cremation, memorial), current obituaries/notices with service times, pre-planning, pricing or "how costs work" page (where local rules require a price list, link it), location with parking and accessibility, staff introduced by name, contact form. {src: 02,46; Bexven}
- [process] Must-have task paths: "someone has just died, what do I do now" (a short step list and the phone number), find a service time, send flowers or condolences, plan ahead. {src: Bexven; 46}
- [brand] Trust signals: years serving the town (only if verified), licence or association memberships, real named staff photos supplied by the client, real reviews with source and date, the building itself. {src: 02,46; C14}
- [type] Readability floor: body ≥18px, body contrast aims for 7:1, generous line-height, no thin display weights for running text. {src: Bexven; C8; C33; 02}
- [image] No identifiable people in stock; prefer hands, flowers, light, architecture, landscape and the real building. Never imply a real family endorses the business. {src: 44,45}
- [motion] Minimal motion: no hero entrance theatre, no scroll reveals, no autoplaying video. {src: Bexven; 41; C9}
- [colour] Deep low-chroma plums, aubergines, greens or greys are allowed when taken from the client's world; saturated violet is not (see §4). {src: Bexven; C3}
- [type] Experimental or novelty display faces read as gimmicky here; the expressive move comes from layout, photography or a restrained serif/sans choice. {src: 28}
- [seo] Schema type `FuneralHome` (LocalBusiness subtype) with real NAP, hours, geo and sameAs; obituary pages are crawlable HTML, not PDFs or iframes. {src: 14; Bexven}
- [copy] No-gos: euphemism stacks ("journey", "celebration of life" as a slogan), urgency or discount language, stock condolence clichés as headings, emoji, exclamation marks, countdowns, popups, chat bubbles that open by themselves. {src: Bexven; 04,05,06}

### 2.2 Metal fabrication shops (first pass)
- [brand] Audience: buyers, engineers, contractors and facility managers comparing shops for a job; also private customers for gates, railings or one-offs. Mostly desktop at work during the day, phone on site. {src: Bexven; 02}
- [brand] Register: direct, specific, capable, unpretentious; facts over adjectives; the work and the machines do the talking. {src: Bexven; 04,05}
- [process] Must-have content: capabilities (processes such as laser/plasma cutting, bending, welding types, finishing), materials and thickness/size limits, equipment list, project portfolio with real photos, industries served, quality certifications, request-a-quote form that accepts drawings, service area, phone. {src: 02; Bexven}
- [process] Must-have task path: "can you make this, and how fast?" answered by capabilities + portfolio + quote form within two clicks of the homepage. {src: Bexven; 46}
- [brand] Trust signals: real certifications (e.g. welding or quality standards) only if the client holds them, named equipment, project photos with material and scope, years in business if verified, repeat-client names only with permission. {src: 02,46; C14}
- [forms] The quote form accepts file uploads (PDF, DWG, DXF, STEP) with stated size limits, plus quantity, material and needed-by date. {src: Bexven}
- [image] Real shop-floor and finished-part photography leads; no stock welders with spark showers, no generic factory stock, no 3D-render heroes. {src: 04,05,44; C31}
- [colour] Not grey/blue + safety orange by default; that is the category's stock answer. Take colour from the client's livery, materials, paint finishes or signage. {src: Bexven; C16; 02}
- [icon] Icons may be heavier to match bold type, but only for functional items (capabilities, specs, contact). {src: 42,43; C32}
- [layout] Spec data (tolerances, max sheet size, materials) goes in real tables with tabular figures, not icon cards. {src: 05,06,07,09,10}
- [motion] A scroll-linked or pinned moment is allowed only if the direction names it (e.g. a process sequence); otherwise none. {src: Bexven; C11; 41}
- [seo] Schema: the closest LocalBusiness subtype (e.g. `HomeAndConstructionBusiness`) or `LocalBusiness` with `makesOffer`/service lists; capabilities get their own crawlable pages in the full build. {src: 14; Bexven}
- [copy] No-gos: "precision engineered excellence"-style slogans, invented capacity figures, "industry-leading", stock blueprint grids as decoration, hard-hat clip art. {src: Bexven; 04,05,06}

## 3. Typography

### 3.1 Choosing faces
- [type] Use one family, or two clearly distinct ones, each with one role and no crossover; a third face only for a literal mono/code role. {src: 01,03,04,06,17,28}
- [type] No fixed recommended font list in the skill; choose from per-niche font pools in `references/font-pools.md`, each with a licence column and a `last_used` date. {src: Bexven; C18; 02,04,05,06,17,26}
- [type] Fonts on the overused list (§12) need a non-category reason written in DESIGN.md. {src: Bexven; C18; 04,05,27}
- [type] Never use a system or installed face (system-ui, Arial, Georgia, Impact) as the display or brand voice; source and self-host a face with a real fallback chain. {src: 04,05,06,17,47}
- [type] Subject associations (books → serif, tech → mono, fabrication → stencil) are exactly what to question. {src: 05}
- [type] Display-only or experimental faces must be paired with a sturdy text face; check weight range and hinting. {src: 03,17,28}
- [type] Check glyph coverage for the client's language (diacritics, Dutch ij, German ß, names on obituaries) before choosing. {src: 07,28}
- [type] Look at real sites in or near the niche to see actual pairings before choosing one. {src: 21,30}
- [type] Set body text first (face, size, line-height, measure), then headings, hero and decoration. {src: 47}

### 3.2 Scale, size, rhythm
- [type] Body 17–19px on desktop, never below 16px on mobile, 18px+ for older audiences. {src: Bexven; C33; 02,04,05,14,47}
- [type] Body line-height 1.45–1.6 (unitless), chosen by the face's x-height; default 1.5. {src: Bexven; C33; 02,04,06,08,14,47}
- [type] Measure `max-width: 62–70ch` on text containers, default 65ch; never edge-to-edge text. (lint) {src: Bexven; C33; 01,04,05,06,07,47}
- [type] Large headings leading 1.0–1.2. {src: 06,07,47}
- [type] Light text on dark grounds gets slightly more line-height, tracking and weight. {src: 05}
- [type] Named type roles (display, headline, title, body, label, caption) each with size, weight, line-height and tracking; ratio 1.2–1.333 for content pages; the hero may jump further once. {src: Bexven; C23; 01,03,05,06,08}
- [type] Display text capped with `clamp(…, 6rem)`; no oversized headings over tiny body text. (lint) {src: Bexven; C23; 04,05,47}
- [type] At most 3 type sizes above the fold. {src: 06}
- [type] Small weight system (about 400/500/600); 700+ rarely; no body or UI text under weight 300. {src: Bexven; C23; 03,04,06}
- [type] Reserve the biggest display style for one context only. {src: 03}
- [type] More space above a heading than below it. {src: 05,47}
- [type] Content headings: 2–3 levels, distinguished by spacing and weight rather than giant size jumps. {src: 47}
- [type] Paragraph separation by space (about 0.5–0.75em) or first-line indent, never both. {src: 47}

### 3.3 Emphasis, case, tracking
- [type] The direction picks one emphasis device (weight, size, case or face) and records it. {src: Bexven; C23; 03,17}
- [type] No single accented word in a headline (italic, bold or colour switch), no marker highlights, never bold + italic together, no underline except links. (lint) {src: 01,03,04,47}
- [type] Sentence case for headings, buttons and nav by default; a brand may choose Title Case in DESIGN.md, applied consistently; never mix on one page. (lint) {src: Bexven; C7; 01,04,06,08,10,47}
- [type] No caps or mono micro-labels by default. If the direction picks caps for one short UI role (nav or buttons), use it for that role site-wide, tracked +0.06–0.12em, never on headings over one line. {src: Bexven; C21; 01,03,04,05,06,47}
- [type] Mono only when the content is literally code or data. {src: Bexven; C21; 05}
- [type] Display tracking −0.01 to −0.03em at 32px+, never tighter than −0.04em; small text 11–13px gets +0.01–0.02em. (lint) {src: 03,04,05,06,07}
- [type] Real small caps only (`font-variant-caps` with a font that has them); never scaled capitals. {src: 47}
- [type] Body left-aligned, ragged right; never justify body without hyphenation; centre only short lines. (lint) {src: 04,05,06,47}

### 3.4 Typographic polish
- [type] `text-wrap: balance` on headings, `pretty` on paragraphs (not on SplitText-animated lines). {src: 05,06,09,10,13}
- [type] `font-variant-numeric: tabular-nums` for prices, hours, specs, tables and changing numbers. {src: 05,06,07,09,10}
- [type] Curly quotes and apostrophes, real ellipsis …, en dash for ranges (9–17h), em dash or spaced en dash for breaks, ©/™ symbols; check the CMS keeps them. (lint) {src: 09,10,47}
- [type] Non-breaking space between number and unit, in "§ 5", and before short last words in headlines. {src: 09,10,47}
- [type] Kerning on (`font-kerning: normal`); ligatures where the font supports them. {src: 47}

### 3.5 Loading and licences
- [type] Read and record each font's licence (OFL, ITF FFL, EULA) before use; ship only faces that allow web self-hosting; keep the licence file next to the WOFF2. {src: 26,27,28,29,30,47}
- [type] Default to free fonts with a verified licence (OFL preferred). ITF FFL faces are self-hosted on the client site only, never in public repos, kits or sold themes. {src: Bexven; C17; 26,27}
- [type] Paid fonts only if the client pays, with the per-domain licence recorded; never proprietary brand faces of other companies. {src: Bexven; C17; 03,30}
- [perf] Always self-host WOFF2, subsetted (latin/latin-ext via `unicode-range`), `font-display: swap`, one variable file where possible, preload only the 1–2 critical files with `crossorigin`. {src: 05,09,10,11,14,26}
- [perf] Font budget: ≤2 families, ≤4 files, ≤100KB total. (lint) {src: 04,06,14}
- [perf] If the font swap causes CLS, tune a metric-matched fallback (`size-adjust`, `ascent-override`, `descent-override`) from the real pair. {src: 11,14}
- [code] No requests to fonts.googleapis.com, fonts.gstatic.com or api.fontshare.com (GDPR, LG München 2022). (lint) {src: 26,27,29}

## 4. Colour

### 4.1 Method
- [colour] Build palettes in OKLCH: same-weight sets fix L and C and rotate H; shades vary L; derive hover by shifting L. {src: 05,34,35}
- [colour] Keep every colour inside sRGB; write the sRGB value first and wider P3 only inside `@media (color-gamut: p3)`. {src: 34}
- [colour] Emit hex fallbacks alongside OKLCH where a target (Elementor globals, older browsers) may not accept `oklch()`. {src: 34; Bexven}
- [colour] Lock the client's existing brand colour (from logo, sign, vehicles) and build a 12-step scale around it. {src: 16,32,33}
- [colour] Choose hue from the client's real material and meaning, never from category association. {src: 05}
- [colour] Steps by job: 1–2 backgrounds, 3–5 component fills (rest/hover/pressed), 6–8 borders and focus rings, 9–10 solid fill and its hover, 11–12 text. {src: 33}
- [colour] Use stock scales (Radix, shadcn, Tailwind) only for greys and semantic colours, never as the brand colour. {src: 33,35}
- [colour] Pair a grey tinted toward the brand hue for warmth, or a neutral grey; tint secondary text, borders and shadows toward the surface they sit on, never plain grey on colour. {src: 04,05,10,33}

### 4.2 Tokens
- [colour] Role-named tokens (`--color-primary`, `--color-surface`, `--color-text`, `--color-border`, `--color-accent`, `--color-danger`…) defined once in `:root`; no raw hex in components. (lint: >12 raw hex outside `:root` fails) {src: 02,03,06,08,15,16,34,35}
- [colour] Every fill token has a paired "on" token that passes contrast. {src: 02,33,35}
- [colour] Each colour has a human name, a job, and a written list of where it may and must never appear. {src: 03,08}
- [colour] Always define a `primary`; every token is used somewhere (no orphans). (lint) {src: 08}
- [colour] Contrast is designed per touching pair (text on surface, button on section), not per swatch. {src: 08,31,32}

### 4.3 Strategy and accent
- [colour] Colour strategy is a named choice in the direction: Restrained (neutral-dominant, ~85% neutral), Committed (brand colour owns 30–60% of the page as fields) or Drenched; it counts as one of the shortlist axes. {src: Bexven; C24; 04,05,06,17}
- [colour] Whatever the strategy, the action accent has a written allowed-places list (primary CTA, links, focus ring) and at most 2 uses per viewport; brand fields are not accents. (lint) {src: Bexven; C24; 03,04,06,46}
- [colour] Exactly one action accent; never invent a second. {src: 03,04,06,08,15,46}
- [colour] If the brand colour fails text contrast, use a darker step of it for text and keep the bright one for fills. {src: 02,06,33}
- [colour] Flat by default; texture or depth only from the client's real material (photos, scanned paper, metal, signage) or a named signature; no generic gradient washes, grain overlays or glass. (lint: `backdrop-filter` and two-stop section gradients need a DESIGN.md reason) {src: Bexven; C22; 03,04,06,08,17,47}
- [colour] Gradients only when they carry hierarchy, never to fill empty space. {src: 01,03,04,05,06,08,36,37,38}
- [colour] No default purple: lint-ban the Tailwind indigo/violet hexes (#6366F1 #4F46E5 #4338CA #3730A3 #8B5CF6 #7C3AED #A855F7, ΔE ≤5) and any purple→blue/pink/cyan gradient. (lint) {src: Bexven; C3; 02,04,05,06,15,17,37}
- [colour] The purple ban is saturation-based: saturated violet/indigo (OKLCH hue ~260–320 with C ≥ 0.08) needs a `brand-source:` note (existing brand or brief); deep low-chroma plum or aubergine (C < 0.08) from the client's world and purple-tinted neutrals are fine. (lint) {src: Bexven; C3; 04,06,33}
- [colour] Never choose violet because of category (e.g. "AI", church); UUPM's category colours are dropped. {src: Bexven; C3; 02}
- [colour] Ink and paper are derived from the palette (ink OKLCH L ≈ 0.18–0.26 with a slight brand tint; paper from the client's material), never stock #000, #111, #0f0f0f, #fafafa. (lint) {src: Bexven; C25; 01,04,06}
- [colour] Vary section grounds only with intent; no predictable light/dark/light banding, and no unexplained single dark band in a light page. {src: Bexven; C5; 04,15}

### 4.4 Light vs dark
- [colour] Light or dark is decided from one sentence covering scene of use, audience and existing brand (e.g. "family on a phone at night; older relatives; sign is dark green on white"); category only breaks a tie. Record it as `mode rationale` in DESIGN.md. {src: Bexven; C5; 02,04,05,06}
- [colour] Dark is not the default for local service sites. {src: 02,04,05}
- [colour] If both modes ship, design them together under the same token names; never invert. {src: 02,05,08,31,35}
- [colour] Dark themes set `color-scheme: dark` and a matching `<meta name="theme-color">`; style native `<select>` colours explicitly. {src: 07,09,10}
- [colour] On dark surfaces build hierarchy with a 3–4 step surface ladder and thin semi-transparent borders (~8% alpha) instead of shadows. {src: 03,06,10}

## 5. Layout and composition

### 5.1 Section grammar
- [layout] Never ship the default skeleton (hero → features → testimonials/pricing → FAQ → CTA, each with eyebrow + heading + lede + 3 cards). {src: 04,05,06,15,17,24,47}
- [layout] The direction names the page's composition pattern in words (e.g. "full-bleed photo, then a 60/40 split, then a hairline-divided list, close on the address"). {src: 03,15}
- [layout] Neighbouring sections never share a layout; pace the page by varying density, scale, imagery and quiet. (lint) {src: Bexven; C26; 03,04,05,06,15}
- [layout] Card layouts (grids of 2+ equal boxes, bento included) at most twice per page; no 3-equal-icon-card grid by default. (lint) {src: Bexven; C26; 01,04,05,06,15,35,46}
- [layout] Prefer asymmetric splits (66/33, 60/40), spans and offsets over equal columns. {src: 06,15}
- [layout] No mirrored zig-zag beyond 2 alternations. (lint) {src: Bexven; C26; 04,06}
- [layout] No hero-metric template (big number, small label, stats strip). {src: 01,04,05}
- [layout] Structural devices (numbers, dividers, borders, labels) must encode real information; 01/02/03 only for real sequences. {src: 01,04,05}
- [layout] One primary job per section; chunk long copy into labelled groups (heading + 2–4 lines). {src: 01,46}
- [layout] Group with shared regions sparingly; max two box levels; never card in card. {src: 04,05,46}
- [layout] Section height follows content; `min-height` only on the hero, using `100svh`/`100dvh`, never `100vh`. {src: Bexven; C13; 04,06,07}
- [layout] End the page on a real close (contact, address, next step), not a fade-out. {src: 05,46}
- [layout] The niche log records hero type and section order; the next site in the niche may not reuse them. {src: Bexven; C26; C27}

### 5.2 Hero and first viewport
- [layout] The first viewport shows the most characteristic thing in the client's world (the real building, the work, the people the client supplied), not a generic hero. {src: 01,04,05}
- [layout] First-viewport check at 1440×900 and 390×844: H1, one hard fact (town, service, phone, years) and the primary CTA are visible. (lint via screenshot script) {src: Bexven; C13; 04}
- [layout] Memory test: what would a visitor describe an hour later? If the answer is "a website", rework the hero. {src: 05}
- [layout] Hero types are an axis in the shortlist (full-bleed photo, split, type-led, map/place-led, work-sample-led); log the one used. {src: Bexven; C4}
- [layout] Hero content may sit top-biased rather than vertically centred; no hamburger-over-stock-photo heroes. {src: 06,47}

### 5.3 Grid, spacing, shape
- [space] Named spacing scale on a 4 or 8px base; one stated whitespace philosophy (dense or airy) in DESIGN.md. {src: 02,03,08,15}
- [space] Spacing inside a group clearly smaller than between groups: 8–16px within, 64–120px between sections on desktop (lower for dense trades, higher for calm niches); labels sit close to their fields. {src: 02,03,15,46}
- [space] Vary padding by context, never one value everywhere; bottom padding often optically larger than top. {src: 06,10,15}
- [layout] One shared container (max 1200–1280px) for header, sections and footer; equal edges. {src: 04,08}
- [layout] Mobile-first; no horizontal scroll; reflow at 320px; usable at 200% zoom. (lint) {src: 02,07,10,12,14}
- [layout] Layouts survive short, long and empty content: `min-width: 0` on flex children, `overflow-wrap: anywhere` on emails and URLs, never truncate prices, dates or names. {src: 07,09,10}
- [layout] Respect `env(safe-area-inset-*)` on full-bleed layouts and fixed bars. {src: 07,09,10}
- [layout] CSS grid/flex sizes things; never measure layout in JS. {src: 09,10}
- [layout] Align deliberately to grid, baseline or optical centre; adjust ±1px optically. {src: 06,10}
- [layout] Align shared elements across side-by-side cards (titles, prices, buttons pinned to the bottom). {src: 06,12}
- [components] One radius language per direction, stated in DESIGN.md (e.g. "0 everywhere, pill for buttons"); never one mid radius (8–12px) on everything; don't mix sharp and round in one view. {src: Bexven; 01,03,08,35}
- [components] Nested radii are concentric: inner radius = outer radius − padding. {src: 06,10}
- [components] An elevation table with a stated ceiling (often flat + tone); no default soft blurred shadow. {src: 03,08}

## 6. Components and patterns

### 6.1 States and interaction
- [components] Every interactive element has default, hover, `:focus-visible`, `:active`, disabled and (where relevant) loading, error and empty states. {src: 03,05,08,09,10}
- [components] Hover, focus and active states change colour, underline, border or shadow with more contrast than rest. (QA: computed-style change on hover) {src: Bexven; C1; 09,10}
- [components] All `:hover` rules live inside `@media (hover: hover) and (pointer: fine)`; touch gets `:active`. (lint) {src: Bexven; C1; 04,07}
- [components] Keep `:active` press feedback on buttons (`scale(0.97)`, range 0.95–0.98, ~100–160ms); it is the only feedback touch users get. {src: Bexven; C1; 04,07}
- [components] No default lift, scale or shadow growth on cards; at most one hover-motion idea per site, named in DESIGN.md, moving a child (image inside its frame, an arrow, an underline drawing in), never the card box. {src: Bexven; C1; 01,04,05,07}
- [components] Unlinked cards never react to hover; anything that looks clickable is clickable, and nothing else looks clickable. {src: 04,10,46}
- [components] Same role = same style; different roles look different. {src: 10,46}
- [components] Theme browser details: `::selection`, caret, focus ring, underline offset, scrollbar, native `<select>`. {src: 05,09,10}
- [components] Loading buttons keep their label and add a spinner; feedback within 400ms of any action. {src: 10,46}
- [components] No spinner or skeleton for loads under 300ms; otherwise skeletons mirroring the final layout, 150–300ms show-delay. {src: 05,07,10}
- [components] Every hover-only or gesture action has a visible click and keyboard alternative. {src: 07,09,10}
- [components] Use accessible APG patterns for dialogs, menus and disclosures; never hand-roll focus handling. {src: 07,10}
- [components] Repeated blocks (service item, review, CTA band) become reusable components that reference tokens. {src: 03,08,16}

### 6.2 Header, nav, footer
- [nav] Logo top-left linking home; main nav 5–6 short nouns using the customers' words; contact last; secondary links in the footer. (lint: ≤7 items) {src: Bexven; C15; 04,06,46}
- [nav] Opaque sticky header allowed; no blur, shrink, hide-on-scroll or floating pill by default. {src: Bexven; C28; 04}
- [nav] Phone number tappable (`tel:`) in the header or footer on every page, in the same position site-wide. (lint) {src: 06,14,46}
- [nav] Mobile: one call or quote bar within thumb reach, appearing once the hero CTA scrolls away; it never covers content or focus. {src: Bexven; C28; 04,06,46}
- [nav] Mark the current page with `aria-current="page"`. {src: 02,14}
- [nav] Real `<a>` links; state lives in the URL; back/forward restores scroll. {src: 09,10,41}
- [nav] In-page anchors and focused elements clear the sticky header (`scroll-margin-top`/`scroll-padding-top` ~ header height). {src: 02,09,10,14,41}
- [nav] Mobile menu: full-screen or sheet, focus moves in, is trapped, returns to the toggle on close; Escape closes it. {src: 04,10,11}
- [nav] No dead ends: every page offers a next step. {src: 10}
- [nav] Footer carries full NAP, hours, service area, legal links and photo credits in one quiet line. {src: 04,14,44,45}

### 6.3 Calls to action
- [components] One primary CTA per viewport, at most one secondary; never two equal primaries in a fold. {src: 03,04,46}
- [components] The main action is worded identically in nav, hero, closing section and phone bar. {src: 01,04,08,10}
- [components] Put the key CTA in the hero and the closing section (first and last). {src: 46}
- [components] No "→" glyph on buttons unless it is the site's one hover idea. {src: Bexven; C1; 01,04}
- [components] Primary mobile CTAs and the phone button are ≥48px tall. {src: Bexven; C33; 11,14}

### 6.4 Forms (contact and quote)
- [forms] Ask only what the job needs: name, one contact channel (phone or email), message; quote forms add service, location and timing. Every extra field needs a reason. {src: 02,14,46}
- [forms] Visible `<label for>` on every field; clicking the label focuses the field; placeholder is never the label. (lint) {src: 02,04,09,10,14,46}
- [forms] Placeholders, if used, show an example format and end with "…"; hints sit below the label, linked with `aria-describedby`. {src: 10,46}
- [forms] Correct input types: `type="email"`, `type="tel"`, `type="date"`, `type="file"`, `<textarea>` for messages; `inputmode` for numeric fields. {src: 07,09,10,14,46}
- [forms] Autocomplete tokens on every personal field: `name`, `given-name`, `family-name`, `email`, `tel`, `street-address`, `postal-code`, `address-level2`, `organization`. (lint) {src: 07,09,10,14,46}
- [forms] Meaningful `name` attributes; `spellcheck="false"` on email; `enterkeyhint` where it helps. {src: 07,09,10}
- [forms] Field font-size ≥16px on mobile (prevents iOS zoom); fields ≥44px tall (48px preferred). {src: 04,07,10}
- [forms] Accept flexible input (spaces, dashes, brackets in phone numbers, mixed case); trim values; never block paste or keystrokes. {src: 02,09,10,14,46}
- [forms] Mark required fields in text ("required") or mark the optional ones, consistently; never by colour or asterisk alone. {src: Bexven; 10,14}
- [forms] Don't pre-disable submit; validate on submit (and on blur after the first error), then show all errors. {src: 10}
- [forms] Errors inline under their field: what went wrong and how to fix it, no "Oops"; set `aria-invalid="true"` and `aria-describedby` on the field; move focus to the first error; colour + icon + text. {src: 01,02,04,05,09,10,14}
- [forms] For long forms add an error summary at the top with links to each field, announced via `role="alert"`. {src: 14; Bexven}
- [forms] Submit stays enabled until the request starts, then shows a spinner, keeps its label and blocks double-submit. {src: 10}
- [forms] Success only after a real send: an on-page message or thank-you page in a polite live region that says what happens next and when ("We'll call you back within one working day"); no exclamation marks. Never `action="#"`. (lint) {src: 04,06,10,46}
- [forms] Server or network failure: keep everything the visitor typed, say it failed, and offer the phone number and email as the fallback. {src: Bexven}
- [forms] Always show a `tel:` link and a `mailto:` link next to the form, for people who would rather call or write. {src: Bexven; C14; 46}
- [forms] Spam: a visually hidden honeypot field (hidden off-screen with `aria-hidden` and `tabindex="-1"`, `autocomplete="off"`) plus a minimum time-to-submit check server-side; no CAPTCHA by default. If spam persists, use a privacy-friendly challenge (e.g. Turnstile) and say so in the privacy text. {src: Bexven}
- [forms] Consent text: one plain sentence under the submit button saying what the data is used for, with a link to the privacy policy; a checkbox only when the jurisdiction or a newsletter opt-in needs it, never pre-ticked. {src: Bexven}
- [forms] Button label names the result: "Send message", "Request a quote", "Ask for a call back"; never "Submit" or "Send" alone. (lint) {src: 01,04,05,06,08,09,10,14,15}
- [forms] File upload (quotes): state accepted formats and size limit before the field; show file name after selection with a remove control. {src: Bexven}
- [forms] Multi-step forms show progress ("Step 2 of 3") and keep earlier answers visible. {src: 46}
- [forms] Static Vercel mocks: forms post to a working endpoint or show a clearly labelled demo state; never a fake success. In WordPress, use Elementor Pro Forms or the site's form plugin with email delivery tested. {src: Bexven; 04}
- [forms] Avoid names and autocomplete values that trigger password managers on non-login fields. {src: 10}

### 6.5 Cards, reviews, proof
- [components] Cards only when elevation means hierarchy; barely there (one step off the ground, light border, no resting blur shadow). {src: 04,06}
- [components] No coloured border-left/right accent on rounded cards or callouts. (lint) {src: 05,06}
- [components] Reviews only as real quotes with name (or initials), date and source (e.g. Google); never invented, never stock headshots. {src: Bexven; C14; 02,04,44,45,46}
- [components] Place real proof (reviews, credentials, years) near the CTA. {src: 02,46}
- [components] No "Most popular" badges, three polished testimonials or fake logo strips. {src: Bexven; C14; 02,06}

### 6.6 Contact, NAP, maps
- [components] Use the prospect's real public name, address and phone (from their site or Google profile), written identically everywhere. {src: Bexven; C14; 14}
- [components] Hours in a real list or table with tabular figures; holiday hours editable in the WP build. {src: Bexven; 10}
- [perf] Maps behind a facade (static image + "Open in Maps" link); load the embed only on interaction. {src: 14}
- [components] Address links to a maps search; phone uses `tel:` with the international format in the href. {src: Bexven}

### 6.7 Carousels, popups, sticky UI
- [components] No auto-rotating carousels, testimonial sliders or logo marquees; use a horizontal `scroll-snap` row only when content overflows, with visible prev/next. (lint) {src: Bexven; C28; 02,04,06,07,46}
- [components] Anything moving for more than 5s gets a pause control. {src: 02,04,09,10,14}
- [components] No modals or popups unless the task needs them; never before the visitor has read anything; no self-opening chat bubbles, back-to-top clutter or "New" pill badges. {src: 04,05,06,14,46}
- [components] Cookie banners never push content down or cover the CTA; reserve their space. {src: 11,14}
- [components] Destructive actions need confirmation or undo. {src: 09,10}

## 7. Imagery and icons

- [image] Photo priority: the client's own photos, then self-hosted stock flagged with `data-placeholder` plus an HTML comment and a hand-off note, then a neutral placeholder block. {src: Bexven; C31; 04,05,06,44,45}
- [image] One decisive real photo beats five mediocre ones; photos of the actual place, work and staff lead the page. {src: 03,04,05,44,45}
- [image] Never present stock people as staff, owners, customers, families or review authors. {src: 04,44,45}
- [image] No stock clichés: laptop + latte, handshake, smiling call-centre, generic team, mood stock instead of the work. {src: 04,44,45,47}
- [image] Never hot-link Unsplash, Pexels, placehold.co or picsum; download, optimise and self-host. (lint) {src: 06,15,44,45}
- [image] List every stock image in the report; the WordPress build replaces them with client photos. {src: Bexven; C31; 04}
- [image] Credit photographers in one quiet line (footer or hand-off). {src: 04,44,45}
- [image] No text on photos except the hero and one closing band; no scrims or gradients over photos unless contrast needs it; no filters or rounded corners on place photos. {src: 04}
- [image] Document photo geometry (aspect ratios, crop focus on mobile, corner treatment) in DESIGN.md; check crops never cut through faces. {src: 03,12}
- [image] No geometric masks faking cut-outs; use a real alpha matte. {src: 05}
- [image] Background video only if compressed, muted, `playsinline`, with poster frame, pause control and reduced-motion stop; full-screen video backgrounds are a trend tell by default. {src: 10,45,47}
- [image] Never put stock imagery in logos or brand marks. {src: 45}
- [image] Descriptive filenames (`chapel-entrance-oak-street.webp`, not `IMG_1234.jpg`). {src: 14}
- [image] Alt text: real description for informative images, `alt=""` for decorative ones; WP builds keep alt text editable. {src: 02,09,10,12,15}
- [icon] No house icon set: choose the family per site to match the type, inline only the SVGs used, one family, one style (outline or filled per job), logged per niche. {src: Bexven; C32; 02,05,06,35,42,43}
- [icon] Stroke follows body weight: ~1.25–1.5 next to light or serif type, ~2 next to bold sans. {src: 06,10,42,43}
- [icon] Use `currentColor`; never an icon webfont or sprite for a handful of icons. {src: 06,14,42,43}
- [icon] Icons are functional (nav, contact, specs, status), never an icon-in-tinted-circle feature grid or check-icon lists on every section. (lint) {src: Bexven; C32; 04,05,42,43}
- [icon] No emoji or unicode symbols as icons; no cliché metaphors (rocket, lightbulb, handshake). {src: 02,05,06,35}
- [icon] Balance icon + text lockups (size, stroke, spacing, colour). {src: 10}
- [wp] In Elementor, upload the same sanitised SVGs as custom icons rather than a plugin icon pack. {src: 42}

## 8. Copy

- [copy] Write all copy before layout, from a fact sheet; nothing invented except clearly marked assumptions. {src: 04,06}
- [copy] Never invent metrics, prices, hours, testimonials, customers, awards or years; use real data or a labelled placeholder and list it under Known gaps. {src: 02,03,04,05,06,46}
- [copy] No lorem ipsum or "Feature one"; placeholder copy reads like real content. {src: 04,06,15}
- [copy] Plain words from the customer's view, active voice, second person; describe, don't sell. {src: 01,05,09,10,46}
- [copy] A voice per client: 2–3 tone words plus what each rules out, written in DESIGN.md; canonical terms with banned synonyms. {src: 04,05,08}
- [copy] H1 names the service and the place or buyer; every heading contains a noun. {src: 04}
- [copy] Buttons and links name the action or result (verb + object); never Submit, OK, Continue, Learn more, Read more, Click here. (lint) {src: 01,04,05,06,08,09,10,14,15}
- [copy] One name per action and concept throughout. {src: 01,04,08,10}
- [copy] Ban slop vocabulary: delve, elevate, unlock, seamless, unleash, cutting-edge, robust, bespoke, streamline, empower, world-class, game-changer, next-gen, tapestry, nestled, journey (as a metaphor). (lint) {src: 04,05,06,09}
- [copy] Ban AI cadences: "X. No Y." runs, "not X, but Y", two-fragment headings, "WORD — fragment" labels, em-dash saturation (more than one em dash per paragraph). (lint) {src: 01,04,05,09}
- [copy] Avoid over-correction: no comma splices replacing dashes, no calm virtue words ("thoughtful", "considered") replacing hype, not everything in pairs instead of threes. {src: 04}
- [copy] Em dashes for real breaks are fine in moderation; the tell is density, not the character. {src: Bexven; 04,47}
- [copy] Almost no exclamation marks (at most one per page, none in success or error messages). (lint) {src: 04,06,47}
- [copy] Errors say what happened and how to fix it; no apologies, no "Oops". {src: 01,05,06,08,09,10}
- [copy] Empty states and thank-you pages say what happens next. {src: 01,05,08,46}
- [copy] Numerals for counts; space between number and unit; consistent currency decimals; dates and times in the local format (`Intl` where scripted). {src: 07,09,10}
- [copy] Ampersands only in names and logos. {src: 47}
- [copy] Menu items that open a follow-up and in-progress labels end with "…" ("Sending…"). {src: 10}
- [copy] Local voice: use the town, street and landmark names customers use. {src: Bexven; 46}
- [copy] Mark brand names `translate="no"`. {src: 09,10}

## 9. Motion

### 9.1 Whether to animate
- [motion] Gate by frequency: things used constantly (nav, form inputs) get no or near-invisible motion; occasional events (menu, dialog) get standard motion; only rare moments may "delight". {src: 07}
- [motion] Every animation names its purpose (feedback, state change, spatial continuity, explanation); "looks nice" is cut. {src: 01,06,07,09,10}
- [motion] No section reveals by default. At most one motion moment per page, optional; the hero entrance counts as that moment. (lint: entrance-animation count) {src: Bexven; C9; C10; 01,04,05,07,13,17,39,41}
- [motion] If the direction names a scroll moment it covers at most 2 sections, fires once, and uses non-uniform stagger. {src: Bexven; C9; 07,13}
- [motion] The static mock and the WordPress build carry the same moment. {src: Bexven; C10}
- [motion] Content is never hidden if JS fails: start from the visible state and hide for an entrance only behind a `.js` class or in JS. (lint) {src: Bexven; C9; 05,13}
- [motion] No count-up numbers, charts redrawing on mount, infinite decorative loops (pulsing dots, glowing borders, gradient orbs) or per-letter text reveals. {src: 04,05,06,07,36}
- [motion] Never animate keyboard-triggered actions. {src: 07}
- [motion] Choreography never blocks clicks; everything visible is clickable. {src: 07}

### 9.2 Tokens
- [motion] One motion vocabulary set once as tokens named by purpose, not speed. {src: 04,07,08,13}
- [motion] Durations: `--dur-press` 100–150ms (press, hover colour), `--dur-state` 150–250ms (toggles, dropdowns, accordions), `--dur-surface` 250–400ms (menus, drawers, dialogs), `--dur-moment` ≤800ms (the single hero moment). {src: 02,04,05,06,07,09}
- [motion] Hover transitions 120–200ms; focus rings appear instantly with no transition. {src: Bexven; C1; C33; 04,07,10}
- [motion] Exits ≈75–80% of the entry duration; exits are simultaneous, never reverse-staggered. {src: 02,04,05,07,08,09}
- [motion] Easing tokens: `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)` for enter, exit and default; `--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)` for things moving across the screen; `--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1)`; linear only for progress. {src: 07,13}
- [motion] No ease-in on UI; exits use ease-out at the shorter duration. {src: Bexven; 07,09}
- [motion] No bounce or overshoot by reflex; local-business sites stay crisp. {src: 04,05,07,08}
- [motion] Never start from `scale(0)`; use 0.9–0.97 plus opacity. {src: 07}
- [motion] Popovers scale from their trigger (`transform-origin`); dialogs stay centred. {src: 07}
- [motion] Stagger with one stagger call, 30–80ms steps (100–150ms allowed in one hero), varied by importance; never uniform `i * 0.1`; never a parent entrance plus child stagger. {src: 07,13}
- [motion] Directional slides only for hierarchy or ordered sequences. {src: 07,09}

### 9.3 Implementation
- [motion] Animate only `transform` and `opacity` (clip-path acceptable); never width, height, top, left or margin. (lint) {src: 02,04,06,07,08,09,10,13,14}
- [motion] Never `transition: all`; list properties. (lint) {src: 07,09,10}
- [motion] Use CSS transitions (retargetable) for anything triggered repeatedly; `@starting-style` for CSS-only enter. {src: 07}
- [motion] Ladder: CSS → WAAPI or Motion `animate()`/`inView()` → GSAP only for a named timeline, scroll-linked, SplitText or SVG-draw moment. {src: Bexven; C11; 07,10,13,17,40}
- [motion] Self-host libraries and pin exact versions; never `@latest`; load only plugins used, with `defer`. {src: 14,18,39,40}
- [motion] GSAP: sequence with timelines, shared `defaults`, `autoAlpha` for fades, `ScrollTrigger.batch()` for grids, `gsap.context()` cleanup, remove `markers` before production. {src: 13}
- [motion] `will-change` only on elements that animate, never on `*`. {src: 07,13}
- [motion] Motion is interruptible by user input. {src: 02,04,09,10,14}
- [motion] Native scroll. `scroll-behavior: smooth` only inside `(prefers-reduced-motion: no-preference)`. No smooth-scroll library or parallax by default. {src: Bexven; C12; 02,04,07,14,41}
- [motion] Lenis only for pinned or scroll-linked storytelling, near default settings, `respectReducedMotion` on, `syncTouch` off, anchors with header offset, stopped while menus or dialogs are open. {src: Bexven; C12; 41}
- [motion] Under `prefers-reduced-motion: reduce`: keep opacity and colour changes ≤150ms, remove all movement, collapse staggers, show final states without a jump; skip GSAP `from()` tweens rather than setting `duration: 0`. (QA: emulate reduce) {src: Bexven; C29; 07,13,14}
- [motion] Respect `prefers-reduced-motion` on every effect, including video loops. {src: 01,02,04,06,07,08,09,10,11,12,13,14,39,40,41,45}
- [wp] Elementor entrance animations off globally; lint `_animation` in `data-settings`. (lint) {src: Bexven; C10; 07,17}

## 10. Accessibility

- [a11y] WCAG 2.2 AA is the pass/fail gate: body text 4.5:1, large text (≥24px, or ≥18.66px bold) 3:1, UI components and focus rings 3:1 against adjacent colours. (lint) {src: Bexven; C8; 01,02,05,06,08,11,14,15,31}
- [a11y] APCA is advisory: flag thin or light text that passes WCAG but scores below Lc 60 (body aims Lc 75+). {src: Bexven; C8; 10,33,34}
- [a11y] Older audiences (funeral, senior care): body text aims for 7:1. {src: Bexven; C8; 02,04}
- [a11y] Palette generation must pass the contrast gate before tokens are accepted. {src: Bexven; C6}
- [a11y] Visible focus on every focusable element via `:focus-visible` (e.g. 2px solid, 2px offset); never `outline: none` without a replacement. (lint) {src: 01,02,04,09,10,14}
- [a11y] Touch targets ≥44×44px with ≥8px between; primary mobile CTA and phone button ≥48px; enlarge hit areas invisibly rather than visually. (lint) {src: Bexven; C33; 02,03,04,05,07,10,11,14,46}
- [a11y] Never disable zoom (`user-scalable=no`, `maximum-scale=1`). (lint) {src: 02,07,09,10}
- [a11y] Skip link to `#main` as the first focusable element; `<html lang>`; landmarks `header/nav/main/footer`. (lint) {src: 04,06,09,10,11,14,15}
- [a11y] One descriptive h1, then a logical hierarchy with no skipped levels; section headings start at h2. (lint) {src: 11,12,14,15}
- [a11y] Native elements before ARIA; links are `<a>`, actions are `<button>`; no clickable divs; no `<a><button>` nesting. (lint) {src: 09,10,14}
- [a11y] Decorative icons `aria-hidden="true"`; icon-only buttons get an accessible name. (lint) {src: 02,09,10,11,12,14,42,43}
- [a11y] Never colour alone for status; add text or an icon. {src: 02,10,14,46}
- [a11y] Async updates, toasts and form results announced via polite live regions. {src: 09,10,14}
- [a11y] Captions or transcripts for meaningful media; no autoplay with sound; autoplay without controls is banned. {src: 09,10,14}
- [a11y] Dialogs and mobile menus move focus in, trap it and return it on close. {src: 10,11}
- [a11y] Sticky UI never covers focused elements. {src: 02,09,10,14,41}
- [a11y] Repeated help (phone, contact link) sits in the same relative position on every page (WCAG 3.2.6). {src: 14}
- [a11y] Honour `forced-colors`, `prefers-contrast` and `prefers-reduced-transparency`. {src: 07,11,12}
- [a11y] No "remember accessibility" lines in the direction step; the numbers live in tokens, lint and the audit gate. {src: Bexven; C6; 01,05}

## 11. Performance and SEO

### 11.1 Performance
- [perf] Core Web Vitals "good": LCP ≤2.5s, INP ≤200ms, CLS ≤0.1, judged at field p75; all three must pass. Needs-improvement bands: LCP 2.5–4s, INP 200–500ms, CLS 0.1–0.25. {src: 02,04,11,14,46}
- [perf] TTFB <800ms. {src: 14}
- [perf] Budgets (starting point): page <1.5MB, images ≤1.2MB total and ≤350KB each, above-fold images <500KB, JS <300KB, CSS <100KB compressed, third-party <200KB. (lint) {src: 04,14}
- [perf] The LCP image is a real `<img>` in the initial HTML, never lazy, never a CSS background, with `fetchpriority="high"`; preload it only if it is discovered late. (lint) {src: 09,10,11,14}
- [perf] Below-fold images `loading="lazy" decoding="async"`. {src: 02,09,10,14}
- [perf] `<picture>` AVIF → WebP → JPEG with `srcset` (e.g. 400/800/1200/1600w) and `sizes`; SVG for logos and icons. {src: 02,09,11,14,44}
- [perf] Every image has `width`/`height` or `aspect-ratio`; reserve space for embeds, fonts and cookie banners. (lint) {src: 02,09,10,11,14}
- [perf] Inline critical CSS (≤14KB) on the static mock; no CSS `@import`. {src: 14}
- [perf] Scripts `defer` or `type="module"`; no parser-blocking JS in `<head>`; analytics, chat and pixels after first paint or behind facades. {src: 09,14,39}
- [perf] Preconnect only to required origins; preload only what a trace shows is discovered late. {src: 09,10,14}
- [perf] Video instead of animated GIF. {src: 09,10}
- [perf] `content-visibility: auto` with `contain-intrinsic-size` for long off-screen sections. {src: 09,10}
- [perf] Cache: HTML revalidates; hashed assets `max-age=31536000, immutable`. {src: 09,14}
- [perf] Measure with a trace under mobile throttling (CPU 4×, Slow 4G, ~390px), fix the biggest LCP subpart, re-measure the same URL; run ≥3 navigations and report the median. {src: 11,14,15}
- [perf] Report lab as lab; never claim speed or ranking gains without before/after measurement; field data lags ~28 days. {src: 11,14}
- [perf] Lighthouse guardrails: Performance ≥90, Best Practices ≥95, SEO ≥95, Accessibility 100 automated then manual checks; scores catch regressions and prove nothing alone. {src: 14}

### 11.2 SEO and markup
- [seo] Every page: unique `<title>` ("Business – service in Town", ~50–60 chars as a hint), meta description (~150–160 chars as a hint), self-referencing canonical, og:title/description/image. (lint) {src: 04,06,11,12,14}
- [seo] LocalBusiness JSON-LD using the most specific subtype, describing only visible content: name, address, geo, phone, hours, URL, sameAs, image; validate in the Rich Results Test. (lint: present and matches visible NAP) {src: Bexven; C14; 14}
- [seo] NAP identical in markup, footer, contact page and Google profile. {src: Bexven; C14; 14}
- [seo] Descriptive link text; breadcrumbs on deep pages. {src: 10,14,15}
- [seo] URLs lowercase, hyphenated, short, no parameters; robots.txt never blocks CSS/JS; sitemap lists only canonical URLs. {src: 14}
- [seo] Static mocks for outreach: `noindex` until the client owns the site, and no canonical to a domain we don't control. {src: Bexven; 04,11}
- [seo] Lighthouse SEO category as a floor on every static redesign before outreach. {src: 11,14}
- [seo] Don't sell `llms.txt` or AI-crawler tweaks as ranking factors. {src: 14}
- [code] `<!DOCTYPE html>`, `<meta charset>` first in head, viewport `width=device-width, initial-scale=1`; no duplicate IDs; semantic HTML5. (lint) {src: 14}
- [code] Zero console errors and zero failed requests; no `document.write`; passive touch/wheel listeners; no public source maps. {src: 11,12,14}
- [code] Security headers on Vercel: HTTPS, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy`; no `X-XSS-Protection`; no polyfill CDNs. {src: 14}

## 12. AI tells list (tells v2026-11)

Dated 2026-11-18. Status: `active` = banned by default; `watch` = allowed only with a written non-category reason in DESIGN.md and the niche-log check. Review quarterly; bump `tells_version` in each DESIGN.md. The full table (first seen, sources, replacement) lives in `references/tells.md`.

### 12.1 Visual
- [colour] active: cream ground + high-contrast serif display + terracotta accent (e.g. #F4F1EA/#D97757); if warm/serif is right, change at least two of ground, face class and accent. {src: 01,05,06,17}
- [colour] active: near-black ground + one acid green, vermilion or neon accent with glow edges. {src: 01,03,05,19,37}
- [colour] active: saturated indigo/violet and purple→blue/pink/cyan gradients; gradient text. {src: Bexven; C3; 02,04,05,06,15,17,37}
- [colour] active: stock #111/#0f0f0f/#fafafa standing in for black and white. {src: Bexven; C25; 01,06}
- [colour] active: decorative glassmorphism, grain overlays, aurora, spotlight, lamp and beam backgrounds, glows. {src: 01,03,04,05,06,36,37,38}
- [colour] active: UUPM stock palettes (#2563EB, #6366F1, slate + safety orange #EA580C for every trade). {src: 02}
- [type] active: broadsheet kit (hairlines + zero radius + small tracked mono labels + italic display serif) outside genuinely editorial clients. {src: 01,03,05,47}
- [type] active fonts (overused defaults): Inter, Roboto, Open Sans, Lato, Arial/system, Poppins, Montserrat, Raleway, Space Grotesk, Plus Jakarta Sans, IBM Plex, JetBrains Mono, Playfair Display, Crimson. {src: 01,02,04,05,06,08,17,26,47}
- [type] watch fonts: Fraunces, Newsreader, Instrument Serif/Sans, Bricolage Grotesque, DM Sans/Serif, Outfit, Geist, Cormorant, Lora, Syne. {src: 04,05,06,26}
- [type] watch fonts (fashionable free foundry picks): Satoshi, Clash Display, General Sans, Cabinet Grotesk. {src: 05,06,27}
- [type] active: weights 100 vs 900 and 3× size jumps as a "bold" move; oversized h1 over tiny body. {src: Bexven; C23; 04,05,17,47}

### 12.2 Layout and components
- [layout] active: hero → features → testimonials → FAQ → CTA skeleton; eyebrow + heading + lede + 3 cards on every section. {src: 04,05,06,15,17,24,47}
- [layout] active: big-stat hero and 3-stat strip; fake 01/02/03 numbering. {src: 01,04,05}
- [components] active: SaaS card kit (identical rounded cards, one 8–12px radius, rgba(0,0,0,.1) shadow, thin border + wide shadow). {src: 01,03,04,05,10,35}
- [components] active: icon-in-tinted-circle feature grids; check-icon lists everywhere; Lucide/Feather defaults untouched. {src: 04,05,06,35,42,43}
- [components] active: tracked caps eyebrows on every section; "A · B · C" meta lines; "→" on every button; hero eyebrow chips. {src: Bexven; C2; 01,04,05,15}
- [components] active: bento grids, logo/testimonial marquees, shimmer and border-beam buttons, number tickers, globes, particles, 3D tilt cards, magnetic buttons, spotlight cards. (lint class names and keyframes) {src: 03,04,05,06,36,37,38}
- [components] active: coloured left-border callout cards; cards in cards. {src: 04,05,06}
- [components] active: auto-rotating 3-dot testimonial carousel; "Most popular" badge; three polished invented testimonials. {src: 02,06; C14; C28}
- [components] active: builder defaults left in place (Elementor default kit fonts/colours, Angie one-prompt design system, theme type scale). {src: 16,47}
- [components] active: sun/moon theme toggle and "New" pill badges as chrome. {src: 06}

### 12.3 Eyebrows (rule, not just a tell)
- [components] Eyebrows are off by default; one is allowed only when it carries information the heading lacks (category, date, real step, location). Max 2 per page (Bexven's number), never on adjacent sections, none in the hero unless it is a date or category; body colour, not accent. An explicit brief wins. (lint: >2 small tracked elements directly before h1/h2 fails) {src: Bexven; C2; 01,03,04,05,15,47}

### 12.4 Imagery
- [image] active: laptop + latte, handshake, smiling team, call-centre headset, spark-shower welder, generic Unsplash hero. {src: 04,44,45,47}
- [image] active: hot-linked placeholder images; 3D renders for trades; full-screen stock video backgrounds. {src: 02,06,15,47}

### 12.5 Copy
- [copy] active: slop vocabulary (§8) and cadences ("X. No Y.", "not X but Y", "WORD — fragment"). {src: 01,04,05,06,09}
- [copy] watch: over-corrections (comma splices, calm virtue words, everything in pairs). {src: 04}
- [copy] active: "Get started", "Learn more", "Submit"; "Oops!"; exclamation marks in confirmations. {src: 01,05,06,09,10}

### 12.6 Motion
- [motion] active: fade-up on every section (AOS style); staggered page-load reveal on every element. {src: 01,04,05,07,13,17,41}
- [motion] active: hover lift/zoom/glow on every card; ungated hover. {src: Bexven; C1; 01,05,07}
- [motion] active: smooth-scroll libraries and parallax on local-business sites; Elementor entrance animations on every widget. {src: Bexven; C10; C12; 04,41}
- [motion] active: count-up numbers, pulsing badges, glowing borders, per-letter text-generate effects. {src: 04,05,06,07,36,37,38}

### 12.7 Stale advice (do not follow)
- [process] Retired: UUPM's category→palette/font mapping and AI-indigo advice; the 2025 Anthropic blog's font suggestions, extreme weights, gradient atmosphere and Google Fonts CDN loading; the Google Fonts sheet's "fresh" shortlist. {src: Bexven; C3; C16; C17; C18; C22; C23; 02,17,26}
- [process] Retired: Taste's fixed section heights, hidden contacts, `.example` emails and no-testimonial rule (fine for demos, wrong for local SEO). {src: Bexven; C13; C14; 04}

## 13. QA and critique

### 13.1 Script checks (numbers)
- [qa] Run the lint script after every generation; output `file:line - issue`, grouped by file, no preamble; feed results into the fix pass. {src: 05,06,07,08,09,10}
- [qa] Script checks: contrast pairs, tap sizes, overflow and overlap (bounding boxes), heading order, labels, alt, `lang`, skip link, banned hexes/gradients/fonts/class names, eyebrow and card-layout counts, entrance-animation count, ungated hover, `transition: all`, CDN font requests, NAP/JSON-LD match, meta tags. {src: Bexven; C19; 05,06,10,11,12}
- [qa] Measure contrast, overlap, tap targets and performance by script, never by eyeballing screenshots. {src: 11,12}
- [qa] Zero console errors and zero 4xx/5xx requests before handoff. {src: 11,12,14}
- [qa] Read the accessibility snapshot for names, heading order and labels. {src: 10,11,12}
- [qa] Write big reports (Lighthouse JSON, traces) to files and filter them; never read whole dumps into context. {src: 11,14}
- [qa] Waive a false finding only with a written reason; never game the checker. {src: 04}

### 13.2 Screenshot review (looks)
- [qa] Screenshot at 320, 375, 768, 1024 and 1440 (add 1920 for photo-led heroes), full page plus first viewport, saved as `qa/shots/{page}-{width}.png`. {src: 02,04,05,06,07,10,12,16}
- [qa] Before capture: wait for network idle and `document.fonts.ready`, scroll once to trigger lazy images, finish or disable animations (emulate reduced motion). {src: 05,12}
- [qa] Screenshots are judged only for visual tells, specificity and composition: identical cards, generic hero, bad crops, orphans in headings, CTA below the mobile fold, unequal card heights. {src: Bexven; C19; 06,12}
- [qa] Emulate reduced motion, forced colours and (if supported) dark scheme on at least the homepage. {src: 11,12}
- [qa] Keyboard pass: Tab through the page; focus order matches visual order; menus and dialogs trap focus. {src: 11,14,41}
- [qa] Break-test with worst-case content: long names, diacritics, 0/1/many items, missing images, very long email addresses. {src: 05,07,10}
- [qa] One WebKit pass per site before sending an outreach link (prospects open on iPhone Safari). {src: 07,10,12,41}
- [qa] Spend QA time where traffic is: homepage, contact, mobile. {src: 46}

### 13.3 Critique rubric
- [qa] Order: first a specificity verdict (similar-prompt, guessability, stranger and memory tests), then heuristics, then craft. {src: Bexven; 01,05,06}
- [qa] Use a fresh-context reviewer that never saw the build conversation; give it the screenshots, the brief and the direction contract; it returns a verdict (rebuild, fix, ship) with evidence per finding. {src: 01,05,06}
- [qa] Severity: P0 broken or illegal (a11y gate fail, invented facts, broken form), P1 AI tell or off-direction, P2 craft issue, P3 polish. {src: Bexven; 06}
- [qa] Max 3 build → screenshot → fix rounds; leftovers go to a human with the list. {src: Bexven; C19; 04,05,06,12}
- [qa] Compare the WordPress build against the saved Vercel screenshots at 375/768/1280. {src: 12,16}
- [qa] Report includes: assumptions made, stock images used, known gaps, lab-only metrics marked as such. {src: Bexven; 04,14}

## 14. Build targets

### 14.1 Static HTML/CSS on Vercel
- [code] Plain HTML/CSS with tokens in `:root` generated from DESIGN.md front matter; JS only for the menu, form and the one named moment. {src: Bexven; 06,08}
- [code] Self-host all assets (fonts, images, libraries); no runtime fetches from third-party CDNs. {src: 14,26,39,40}
- [tooling] Deploy previews by default; `--prod` only on explicit request. {src: 09}
- [tooling] Token via `VERCEL_TOKEN` env only, never on the command line; use `--scope` for the team; `-y` and `--format json` for scripted runs. {src: 09}
- [tooling] Don't run `vercel link` in an unlinked folder to "check" state; `vercel whoami` is safe. Ask before any git push. {src: 09}
- [tooling] Temporary no-login deploys produce a claim link; keep it private. {src: 09}
- [seo] Outreach previews are `noindex` (see §11.2). {src: Bexven}

### 14.2 WordPress/Elementor via Elementor MCP
- [wp] Pre-flight: Elementor ≥4.3, WordPress ≥6.8, Application Passwords working, V4 Atomic editor active; if any check fails, use the fallback. {src: 16}
- [wp] Build order: (1) Variables for colour, type scale and spacing from the static page's `:root`; (2) Global Classes for repeated patterns (buttons, cards, section shells); (3) header and footer as theme parts with display conditions; (4) pages from Atomic flex/grid containers using those classes; (5) forms and popups. {src: 16}
- [wp] Map the static CSS 1:1: tokens → Variables, component classes → Global Classes, sections → Atomic containers; no inline styles per element. {src: 15,16}
- [wp] Carry the exact mock fonts and colours into Variables; never accept the Elementor default kit or an Angie-generated design system. {src: 16,47}
- [wp] Emit hex for Elementor global colours (OKLCH support unverified). {src: Bexven; 34}
- [wp] Repeated blocks become Components so the client edits each in one place. {src: 16}
- [wp] Keep the Global Class count lean; reuse Variables instead of one-off values. {src: 16}
- [wp] Use legacy V3 widgets only where no Atomic equivalent exists yet. {src: 16}
- [wp] MCP output is a draft: compare against the Vercel screenshots, then publish by hand. {src: 16}
- [wp] Use the revisions-based undo on a bad call; never hand-edit `_elementor_data`. {src: 15,16}
- [wp] Use a dedicated Application Password; revoke it at handover and turn MCP off on live sites. {src: 16}

### 14.3 WordPress fallback (no MCP)
- [wp] Set Site Settings by hand from the token list: Global Colours, Global Fonts (or V4 Variables and Classes). {src: 16}
- [wp] Generate an Elementor JSON template (flex containers with direction, gap and padding using global colour/font IDs) and import via Templates → Import; a Kit .zip for whole sites. {src: 16}
- [wp] Rebuilding by hand: flexbox containers only, never legacy section/column layout. {src: 16}

### 14.4 WordPress hygiene
- [wp] Self-host fonts via Elementor Custom Fonts (or "Load Google Fonts Locally") with the licence file kept alongside; confirm in DevTools that no googleapis/gstatic requests remain. {src: 26,27,28,29}
- [wp] Enqueue scripts from a child theme (never the parent), local copies, in the footer, with dependencies; check whether Elementor Pro already bundles GSAP. {src: 13,39,41}
- [wp] Don't package GSAP into a reusable visual animation-builder plugin. {src: 39}
- [wp] Fix specificity at the source by inspecting the cascade; don't stack `!important`. {src: 01,11}
- [wp] Audit plugin and widget bloat: scripts per page, render-blocking CSS, third-party tags. {src: 11,15}
- [wp] The LCP hero is an Image widget (real `<img>`), not a section background. {src: 14}
- [wp] Turn off Elementor entrance animations globally (see §9). {src: Bexven; C10}
- [wp] Treat production as unsafe for WP-CLI unless confirmed: set `--path`/`--url`, `wp db export` first, `search-replace --dry-run` before real runs; destructive ops need explicit sign-off. {src: 15}
- [wp] Escape output and sanitise input in any custom PHP (esc_html/esc_attr/esc_url, nonces plus capability checks, `$wpdb->prepare`). {src: 15}

### 14.5 Parked
- [process] Shopify Liquid and non-Claude agents are out of scope for v1; keep the structure portable. {src: Bexven; 18}

## 15. Tooling

- [tooling] Default QA driver: our own Python Playwright script (breakpoint screenshot sweep, bounding-box checks, console and network capture). {src: 11,12}
- [tooling] Chrome DevTools MCP is optional, for CWV traces, Lighthouse, Chrome issue audits and the CSS cascade; if absent, fall back to Playwright plus Lighthouse CLI and say what was skipped. Never install it for the user. {src: 11}
- [tooling] DevTools MCP flags for agency work: `--isolated --no-usage-statistics --no-performance-crux` (CrUX off for unlaunched previews). {src: 11}
- [tooling] Playwright MCP only for interactive exploration (menus, form flows, editor quirks, reproducing a client bug). {src: 12}
- [tooling] Browser tools run isolated, never on logged-in client admin profiles unless asked; never enable unrestricted file access or code-execution options. {src: 11,12}
- [tooling] Take a fresh snapshot after any DOM change (old element IDs go stale). {src: 11}
- [tooling] Scripts are Python 3, non-interactive, with `--help`, JSON to stdout, diagnostics to stderr, distinct exit codes, idempotent, `--dry-run` for destructive work, bounded output. {src: 18}
- [tooling] Pin versions for any tool or library named in a script or instruction. {src: 18,39,40}
- [tooling] Bundle a script whenever the agent keeps redoing the same check by hand. {src: 05,06,18}
- [tooling] Keep SKILL.md files under ~500 lines/5k tokens; detail lives in references one level deep, each loaded at a named step ("open `niches/funeral-home.md` if the client is a funeral home"). {src: 17,18}
- [tooling] Each skill keeps a Gotchas section grown from real corrections. {src: 07,18}
- [tooling] Don't install or keep other design skills (frontend-design, Impeccable, Taste) alongside ours; delete cloned `sources/` so their skills can't auto-load. {src: Bexven}
- [tooling] Galleries (Awwwards, SiteInspire, Land-book, Lapa Ninja, httpster, Minimal Gallery) are human reference steps only; their terms forbid scraping. {src: 19,20,21,22,23,24,25}
- [tooling] Unsplash/Pexels via API only if scripted with download tracking and credit; keys stay out of client code. {src: 44,45}
- [tooling] Huemint (non-commercial API) and palette randomisers are not used; palettes come from the client's world and the OKLCH script. {src: 31,32}
