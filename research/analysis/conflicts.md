# Conflicts between sources — and how Bexven's skill should resolve them

Read 2026-11-18 from all 47 sheets (`sheets/01`–`47`; there is no index.md, so numbering comes from the filenames). Source numbers in brackets, e.g. [04] = Taste Skill.
Format per item: Side A / Side B / why it confuses an AI / **Recommended resolution** (testable) / confidence.
General precedence used throughout: **explicit client brief or existing brand > hard floors (a11y, legal, perf) > Bexven defaults > source opinions** [01][05][06].

---

## Part 1 — The five known conflicts (lead's positions, refined)

### C1. Hover motion: mandatory lift/zoom vs "hover on every card is a tell" — confidence: high
- **Side A (hover everywhere, with motion):** Taste [04] makes hover mandatory: a linked card lifts 2px, a photo zooms 1.02–1.03 inside an `overflow:hidden` frame, buttons step up 1px, arrows move 3px (fine pointer only). UUPM [02] puts 150–300ms hover micro-interactions everywhere and never 0ms. WIG [10][09]: every button/link has a hover state, and hover/active/focus show more contrast than rest. Open Design's redesign-skill [06] wants hover scale on every button.
- **Side B (restraint):** Anthropic [01] says hover transitions on every card are a tell. Emil [07] turns scale/lift/shadow-growth hovers into colour/opacity changes of 150ms or less, and calls hover-scale on secondary cards decoration. Impeccable [05]: hover never moves the element itself or its neighbours; animate a child. Open Design craft [06]: don't animate to signal "premium". Awesome DESIGN.md [03] documents no hover at all (an extraction policy, not a design rule).
- **Why it confuses:** both sides say "hover", but A means *feedback* and B means *decorative motion*. An AI told both will either lift every card or remove hover feedback altogether. Both outcomes are wrong.
- **Recommended resolution:**
  1. Every interactive element (link, button, linked card, form control) has visible hover, `:focus-visible` and `:active` states that change colour, underline, border or shadow, with more contrast than rest [10]. QA test: hover each control and see a computed-style change.
  2. Put all `:hover` rules inside `@media (hover:hover) and (pointer:fine)`. Touch gets `:active` [07]. Lint test: no ungated `:hover` rule.
  3. Hover transitions take 120–200ms, use `transform`/`opacity`/colour only, and never `transition: all` [04][07][10]. Focus rings appear instantly, with no transition [04].
  4. No default lift, scale or shadow growth on cards. At most one hover-motion idea per site, chosen and named in DESIGN.md. It moves a child (an image inside its frame, an arrow, an underline drawing in), never the card box [05].
  5. Unlinked cards never react to hover [04].
- **Note:** press feedback (`:active { scale(.97) }` [07], Taste's 1px press [04]) is not hover motion. Keep it on buttons, because it is the only feedback touch users get. Taste's photo zoom already moves a child, so it qualifies as the site's single hover idea; its 2px card lift does not.

### C2. Eyebrow / kicker labels — confidence: high
- **Side A (ban):** Impeccable [05] bans them outright: "no brief earns it back", and its detector flags `kicker-above-heading` and `hero-eyebrow-chip`. Taste [04] bans tracked-caps and small-caps labels and lists "eyebrow + heading + lede + 3 cards on every section" as a tell. Anthropic [01] calls "a tracked ALL-CAPS eyebrow above every heading" template chrome, and says labels must encode information.
- **Side B (use):** real brands use them: WIRED category eyebrows and Sanity mono eyebrows [03]. The WordPress pattern examples [15] ship an uppercase tracked eyebrow over the hero. Butterick [47] permits caps for short strings such as eyebrows when they are tracked. Elementor kits ship eyebrow widgets [05 §8]. Anthropic's "brief wins" rule [01] can override the ban.
- **Why it confuses:** an absolute ban next to real-world use. Elementor kits put an eyebrow on every section by default.
- **Recommended resolution:** eyebrows are off by default. One is allowed only when its text carries information the heading lacks: a category, a date, a step in a real sequence, or a location. "Our services" above "Services we offer" fails that test. Maximum two per page, never on adjacent sections, and none in the hero unless it carries a date or category. If used, sentence case or tracked small text in the body colour, not the accent colour [06: accent uses count toward a limit of 2 per screen]. An explicit brief wins. Lint: count elements that sit directly before an h1/h2 and are styled smaller and tracked; more than 2 fails.
- **Note (pushback):** the sheets do not support "Taste: max 1–2 per page". Sheet [04] bans tracked-caps labels outright and only limits *card layouts* to two per page. The "max 2" figure is ours, so attribute it to Bexven, not to Taste.

### C3. Purple / violet / indigo — confidence: high
- **Side A (ban):** Taste [04] never uses OKLCH hue ~270–330 in the page's own design: it pushes violet to 255 or 345 and re-deals any violet palette. Open Design [06] lints these as P0: Tailwind `#6366f1 #4f46e5 #4338ca #3730a3 #8b5cf6 #7c3aed #a855f7`, plus purple→blue, blue→cyan and indigo→pink hero gradients. The Anthropic blog [17] says "avoid purple gradients on white". Impeccable's detector [05] flags purple/violet gradients and cyan-on-dark. UUPM [02] bans "AI purple/pink gradients" for about 15 trust industries.
- **Side B (recommend or ship):** UUPM [02] recommends "AI Purple #6366F1" for AI/chatbot products, uses #6366F1 as primary for Micro SaaS and others (14 times in colors.csv), and gives Church violet #7C3AED with gold. Open Design ships a Stripe system with "signature purple gradients" (#533afd, not on its own lint list) [06]. Real brands use it: Linear, Stripe, Kraken, Mercury [03]. The WordPress core preset `vivid-cyan-blue-to-vivid-purple` appears in WP pattern examples [15]. Radix's mauve gray is purple-tinted [33].
- **Why it confuses:** one source bans a hue band that another recommends for a whole category, and real brands own it.
- **Recommended resolution:** ban the listed Tailwind indigo/violet hexes and any purple→blue/pink/cyan gradient as defaults (lint). Violet or indigo as an accent or brand colour is allowed only when it is the client's existing brand colour (taken from their logo or site) or the brief asks for it. Never choose it because of the category: drop UUPM's AI-indigo and church-violet guidance. Lint: any hex within ΔE 5 of the list, or any gradient with a stop at hue 260–320, needs a `brand-source:` note in DESIGN.md.
- **Note:** Taste's 270–330 band is broader than the problem. Deep, low-chroma plum or aubergine (OKLCH C < 0.08) taken from a client's world, such as a funeral home's chapel textiles or existing signage, and purple-tinted neutrals, are not the AI tell. The tell is saturated indigo/violet and purple gradients. Make the default ban chroma-aware rather than hue-only.

### C4. Random vs deliberate choices — confidence: high
- **Side A (random):** Taste [04] "deals" palette, fonts, hero, nav and footer with `Math.random`, with history files pushing recently used options to the back; the agent must take the first result and "never pick by taste". Realtime Colors [31] randomizes by harmony rule.
- **Side B (deliberate):** Anthropic [01] derives choices from the subject's industry, materials and vernacular and runs the "would a similar prompt land here?" test. Impeccable [05] builds 7 culture-derived candidates across ≥3 material families, *then* rolls dice among them, and never proposes a look before the roll. Emil [07] prototypes 3–5 variants, each differing on a named axis and never only by accent colour. UUPM [02] is deterministic (the top BM25 hit wins), which is a third failure mode: the same niche always gets the same output. The agent-skills spec [18] says "give a default, not a menu".
- **Why it confuses:** "never choose by taste" and "derive from the subject" read as opposites. Pure randomness ignores the client; pure deliberation converges on the model's prior, so two funeral homes get the same "tasteful" answer.
- **Recommended resolution:** build a deliberate shortlist, then pick at random from it:
  1. Derive 3–5 directions from the client's world (place, materials, era, signage, competitors' "category page" named and avoided [05]). Each must differ on at least 2 named axes (type class, colour strategy, layout grammar, density, motion idea) [07].
  2. Discard any direction that collides with the per-niche history log (same direction, display font, palette family or hero type as any of the last N sites in that niche, N ≥ 5).
  3. Pick among the survivors with a seeded random draw. Record the seed (e.g. a hash of the client domain plus the date) so the pick is reproducible.
  4. Write one sentence saying why the pick fits the client [04], and append it to the niche log.
- **Note:** cold outreach has no client to confirm with [01 §7], so the skill makes and logs assumptions instead of asking.

### C5. Light vs dark — confidence: high (medium for exact wording)
- **Side A:** Impeccable [05]: light or dark is never a default and never chosen by category. Write one sentence of physical scene (who, where, what ambient light).
- **Side B:** UUPM [02] decides per category (dark for dashboards, dev tools and entertainment; light for service and marketing sites). Taste [04] allows dark pages and heroes only for tech, with at most one dark or brand band in the second half of the page. Open Design's vendored taste-skill makes dark mandatory for consumer pages, while its redesign-skill warns against a random dark section [06 §8d]. Anthropic [01] lists both a cream cluster and a near-black cluster as tells. Awwwards [19] winners skew dark.
- **Why it confuses:** three different decision procedures, and one source contradicts itself.
- **Recommended resolution:** decide from a one-sentence scene of use plus audience plus existing brand (e.g. "grieving family on a phone at night, often older relatives, existing sign is dark green on white"). Use category only to break a tie. Record the sentence and the decision in DESIGN.md (`## Overview → mode rationale`). No unexplained single dark band in a light page: a band of inverted colour needs a stated reason. If both modes ship, design both, don't invert [05][31].

---

## Part 2 — Other conflicts found in the sheets

### C6. Accessibility in design prompts vs audit-only — high
- **A:** Impeccable [05] keeps a11y reminders out of design-time prompts on purpose, because they made output timid, and checks it in `audit`.
- **B:** UUPM [02] ranks a11y as priority 1. WIG [10], web-quality [14] and Anthropic's "silent quality floor" [01] apply it during the build.
- **Confuses:** should the model think about a11y while designing or not?
- **Resolution:** a11y is enforced through **numbers in tokens and lint**, not through prose in the creative brief. Palette generation must pass 4.5:1 for body text and 3:1 for large text/UI before it is accepted, and type tokens carry body ≥16px and tap targets ≥44px. No "remember accessibility" sentences in the direction step. A separate audit gate runs after the build [14][11]. Bold design ships only if the audit passes.

### C7. Sentence case vs Title Case — high
- **A:** WIG [10] uses Title Case for app headings and buttons (labelled Vercel-only; marketing pages use sentence case). The agent-skills sheet [09] reads it as "the guidelines want Title Case". Open Design's warm-editorial system bans sentence-case H1/H2 [06 §8c].
- **B:** sentence case in [01][04][06 craft][47].
- **Resolution:** sentence case by default for headings, buttons and nav. DESIGN.md `## Voice` may choose Title Case for a brand, applied consistently. Lint: within one page, headings never mix the two styles.

### C8. WCAG 2 vs APCA, and how much contrast — high
- **A:** WIG [10] prefers APCA. Radix [33] defines text steps by APCA Lc 60/90. OKLCH/Harmonizer [34] builds palettes on APCA.
- **B:** WCAG 2.2 AA in [02][06][08 linter][14][31]. Taste [04] wants 7:1 on body text. UUPM [02] uses 7:1 only for an explicit AAA target.
- **Resolution:** WCAG 2.2 AA is the pass/fail gate, because it is the legal reference for ADA/EAA [10 §8]: 4.5:1 body, 3:1 large text (24px, or 18.66px bold; the "18px" in [14] is a bug) and 3:1 for UI and focus rings. APCA is advisory: flag thin or light text that passes WCAG but scores below Lc 60. Body text aims for 7:1 when the audience skews older (funeral homes, senior care).

### C9. Scroll reveals / fade-ups — high
- **A (allow):** the Anthropic blog [17] wants one orchestrated load with staggered reveals. Emil [07] allows scroll reveals on marketing pages, fired once. GSAP skills [13] use `ScrollTrigger.batch` for reveal grids. Motion [40] uses `inView()` for reveals. UUPM's motion dial attaches GSAP snippets [02].
- **B (ban):** Taste [04] has no scroll reveals at all. Anthropic [01] says don't fade-and-slide every section. Emil [07] calls fade-in on every section a defect. Lenis sheet [41] calls fade-ups on local sites a tell.
- **Resolution:** zero section reveals by default. If the direction names a scroll moment, it applies to at most 2 sections, fires once, uses non-uniform stagger [07], and never hides content without JS: the hidden start state is set by JS or behind a `.js` class [13 §8]. Lint: count elements with entrance animation classes; more than the named moment fails.

### C10. One motion moment vs Elementor entrance animations (and Taste's mandatory moments) — high
- **A:** Elementor's per-widget Motion Effects entrance animations are easy to set and widely used [07 §7][17 §7: "use native entrance animations"]. Taste [04] makes a hero entrance and a dealt "moment" mandatory on every page.
- **B:** one authored moment per page in [01][05][07]. Taste's own sheet [04 §7] says to keep the moment optional for Elementor builds.
- **Resolution:** turn off Elementor entrance animations globally (Site Settings, or a lint on `data-settings` `_animation`). One motion moment per page at most, and it is optional. The hero entrance counts as that moment. The static mock and the WP build must carry the *same* moment.

### C11. GSAP by default vs CSS first — high
- **A:** GSAP skills [13] tell the agent to recommend GSAP whenever no library is named (a vendor bias). The GSAP sheet [39] says "take GSAP as the default for anything beyond CSS". UUPM [02] ships GSAP presets.
- **B:** WIG [10] orders CSS > WAAPI > JS. The Anthropic blog [17] uses CSS-only for HTML. Emil [07] prefers CSS transitions, `@starting-style` and WAAPI. Motion mini [40] is about 3kb.
- **Resolution:** state changes use CSS. Small JS reveals use WAAPI or Motion `animate()`/`inView()`. GSAP only for a named signature moment that needs a timeline, scroll-linking, SplitText or SVG draw. On WP, check whether Elementor Pro already bundles it before enqueueing [13 §8]. Self-host and pin versions; never `@latest` [39][40].

### C12. Smooth scroll — high
- **A:** UUPM [02] says "use smooth anchor scroll". Lenis exists for awards-style feel [19][41].
- **B:** Taste [04] bans smooth-scroll libraries. Lenis's own sheet [41] says no Lenis by default and that it fights Elementor popups and sticky sections. Web-quality [14] turns smooth scroll off under reduced motion. Open Design lints `scrollIntoView` as P0 [06].
- **Resolution:** native scroll, plus `scroll-behavior: smooth` only inside `(prefers-reduced-motion: no-preference)` for anchor jumps, with `scroll-margin-top` for sticky headers [10][14]. Lenis only with pinned or scroll-linked storytelling, using the a11y-safe config from [41].

### C13. Taste's section-height rigidity vs real content and Elementor — medium
- **A:** Taste [04]: every section is exactly 1 or 2 viewport heights, the hero is alone on screen 1 at 1440×900, blocks under ~495px merge into the section above, and sections are separated only by a ground change (no hairlines).
- **B:** density and rhythm are brand decisions (Nintendo dense, Bugatti airy) [03]. Alternate density [06]. Taste's own sheet calls the rule too rigid for Elementor [04 §7].
- **Resolution:** drop the viewport-multiple rule. Keep two checks: (a) the first viewport at 1440×900 and 390×844 shows the H1, one hard fact and the primary CTA; (b) neighbouring sections differ in layout or density. Section height follows content, with `min-height` only on the hero (`100svh`, not `100vh` [07]).

### C14. Hidden contacts and no testimonials (Taste demos) vs local SEO — high
- **A:** Taste [04] shows only street and district (no house number or postcode), uses no real-format phone numbers and `.example` emails, and allows no testimonials or figures unless the brief gives them verbatim.
- **B:** UUPM [02] bans hidden contact info for home services. Web-quality [14] requires repeated help in the same position on every page (WCAG 3.2.6). Laws of UX [46]: phone clickable, social proof near CTAs. Open Design [06]: phone tappable on mobile. Local SEO needs consistent NAP and LocalBusiness JSON-LD [14 §7].
- **Resolution:** redesign mocks use the prospect's **real public** NAP (from their site or Google profile), tappable `tel:`, and LocalBusiness subtype JSON-LD. Anything inferred gets `data-assumed` and goes in the report [04]. Reviews appear only as real quotes with their source (e.g. Google, with name and date). Never invented testimonials, figures or headshots [04][06][44][45].

### C15. Jakob's law vs distinctiveness — high
- **A:** Laws of UX [46]: keep conventions (logo top-left, nav at the top, contact in the footer, the expected IA such as funeral home → services, obituaries, pre-planning).
- **B:** Impeccable [05] bans "the page this category always ships". Open Design [06] wants at least one unconventional section. httpster [24] lists "unusual navigation" as a style filter.
- **Resolution:** be conventional in **where things are and how they behave** (nav, logo, contact, IA labels, forms); be distinctive in **identity and composition** (type, colour, imagery, section grammar, one signature) [46 §7]. Lint: nav ≤7 items with a real `<a>`, logo links home, phone in header or footer.

### C16. Deterministic industry mapping vs same-niche variety — high
- **A:** UUPM [02] maps each industry to one palette, style and font (trades → slate + safety orange `#EA580C`). Icon sheets map weight to niche (Thin for funeral, Bold for fabrication) [42][43]. Velvetyne [28] rules out display faces for funeral and legal. Taste [04] uses trade-tagged palettes with trade matches first.
- **B:** Impeccable [05]: choose hue from product meaning, never from category; subject associations (books → serif) are "exactly what to break". The Anthropic blog [17]: derive per client.
- **Resolution:** the niche table supplies **constraints and must-have content** (credentials, emergency contact, portfolio, obituaries, readable sizes for older audiences), never the palette or font itself. Choices come from C4's shortlist plus history. Test: two sites in the same niche must not share display font, palette family or hero type.

### C17. Free vs paid fonts, and how to load them — high
- **A:** Butterick [47] discourages common free fonts. Typewolf [30] mostly shows paid foundry faces. DESIGN.md brand files use proprietary faces [03]. The Anthropic blog [17] says load from Google Fonts.
- **B:** OFL fonts [26][28], ITF FFL [27] and uncut [29] are free. Fonts must be self-hosted for GDPR (LG München 2022) [26][27]. Web-quality [14] sets a font budget under 100KB.
- **Resolution:** default to free fonts with a **recorded, verified licence** (OFL preferred; ITF FFL self-hosted on the client site, never in public repos or kits). Always self-host WOFF2, subsetted, at most 2 families and 4 files. Paid fonts only if the client pays, with the per-domain licence recorded. Proprietary brand faces never. Lint: no requests to googleapis, gstatic or api.fontshare.

### C18. Font recommendations that contradict each other's ban lists — high
- **A (recommends):** Anthropic blog [17]: Space Grotesk, JetBrains Mono, Playfair, IBM Plex, Bricolage, Newsreader, Crimson Pro. Google Fonts sheet [26]: Fraunces, Instrument Serif, Bricolage, Newsreader, Hanken for our shortlist. Taste type.json [04]: Geist, Fraunces/Figtree, Newsreader/Hanken, Instrument Serif/Sans. Open Design redesign-skill [06]: Geist, Satoshi, Outfit as replacements. UUPM [02]: Inter (most used), Space Grotesk, Plus Jakarta.
- **B (bans):** Impeccable [05] calls Fraunces, Playfair, Newsreader, Plex, Space Grotesk, DM Sans, Outfit, Plus Jakarta and Instrument Sans "stopped looking" defaults, and its detector flags Geist and Fraunces. Taste [04] bans Inter, Montserrat, Poppins, Space Grotesk and Plus Jakarta. Fontshare [27] names Satoshi, Clash, General Sans and Cabinet as tells.
- **Confuses:** one source's replacement font is another source's banned font.
- **Resolution:** no fixed recommended list in SKILL.md. Keep per-niche font pools in `references/` with a licence column and a `last_used` date, plus a dated "overused" list (see Part 3). A font from the overused list needs a non-category reason written in DESIGN.md. The same display font may not appear in 2 of the last 5 Bexven sites overall, or in any of the last 5 in the same niche.

### C19. Screenshot review vs text-tree / metric QA — high
- **A:** screenshot critique loops in [01][05][12]: 4 breakpoints, max 2–3 rounds, fresh-context reviewer [05].
- **B:** don't judge contrast or perf from screenshots [11]. The a11y snapshot is the default and is cheap [12]. Measure overlap with bounding boxes [12]. Playwright's README prefers CLI over MCP for token cost [12].
- **Resolution:** both, split by job. Scripts check numbers (contrast, tap size, overflow and overlap boxes, CLS/LCP traces, console/404, heading order) and output `file:line` findings [10]. Screenshots (after `fonts.ready`, lazy loading and finished animations [12]) are judged only for visual tells and "soul test" questions [06]. Use a reviewer without conversation history, 2 rounds max, then hand the rest to a human. Python Playwright script first, MCP optional [11][12].

### C20. DESIGN.md before vs after the build — medium
- **A:** Impeccable [05] writes DESIGN.md *after* the build, from what shipped.
- **B:** before, as the brief and source of truth, in [02 MASTER.md][03][06][08]. Emil's learn-taste [07] keeps updating it.
- **Resolution:** before the build, write a short direction contract plus token front matter, because the Elementor build depends on it [05 contract][08]. After QA, sync DESIGN.md to the built page (the shipped page wins on drift) and add any corrections as rules with their reason [07]. Test: `design.md lint` [08], or our own check that every token in CSS exists in DESIGN.md and the reverse.

### C21. ALL CAPS and mono labels — high
- **A (allow):** Open Design craft [06]: caps are fine with +0.06–0.1em tracking. Butterick [47]: caps for short strings with 5–12% tracking. DESIGN.md brands [03]: uppercase labels with 2–6px tracking, mono for buttons, nav and captions.
- **B (ban):** Anthropic [01] bans all-caps labels and mono small data labels (template chrome). Taste [04] bans tracked caps. Impeccable [05] flags all-caps body, "small tracked mono labels" (cluster 3) and "monospace as a costume".
- **Resolution:** no caps or mono micro-labels by default. If the direction chooses caps for a short UI role (nav or buttons only), apply it to that one role site-wide, tracked 0.06–0.12em, and never on headings over one line. Mono only when the content is literally code or data.

### C22. Atmosphere vs flat colour — medium
- **A:** the Anthropic blog [17]: layered gradients, patterns and textures, "not flat solid fills". Open Design redesign-skill [06] uses grain everywhere. Butterick [47] warns against big flat colour blocks.
- **B:** Taste [04]: flat colour only off tech (no gradients, grain or glass). Open Design craft [06]: gradients only for hierarchy, no two-stop hero gradients. DESIGN.md [03][08]: no decorative gradients, glows or glass.
- **Resolution:** flat by default. Texture or depth only from the client's real material (photography, scanned paper, metal, signage) or a named signature. No generic gradient washes, grain overlays or glass. Lint: `backdrop-filter` and two-stop `linear-gradient` on section backgrounds need a DESIGN.md justification.

### C23. Type contrast: extreme weights vs restrained weights — medium
- **A:** the Anthropic blog [17]: weights 100/200 against 800/900, size jumps of 3× or more.
- **B:** Taste [04]: headlines at 400 (500 for tech), never 700/800. Open Design [06]: 400/500/600, scale 1.2–1.25, at most 3 sizes above the fold. Impeccable [05]: display ≤6rem, with an `oversized-h1` detector rule. Butterick [47]: avoid oversized headings. Bugatti and WIRED ban bold [03].
- **Resolution:** the direction picks **one emphasis device** (weight, size, case or face) and records it [03]. Display text is capped at `clamp(…, 6rem)`. No body or UI text under weight 300. Ratio 1.2–1.333 for content pages; a hero may jump further once.

### C24. Colour quantity: committed fields vs 90% neutral — medium
- **A:** Impeccable [05]: colour commits at page scale (Committed 30–60%, Drenched). The Anthropic blog [17]: a dominant colour with sharp accents. WP patterns [15]: vary section backgrounds (light, inverted, accent).
- **B:** Taste [04]: UI 90–95% neutral, accent under 3%. Open Design [06]: neutrals 70–90%, one accent at 5–10%, at most 2 accent uses per screen. DESIGN.md brands [03]: one scarce accent with an allowed-places list.
- **Resolution:** colour strategy is a named choice in the direction (Restrained, Committed or Drenched [05]) and goes in the C4 axes. Whatever the strategy, the **action accent** keeps a written allowed-places list (CTA, link, focus) [03] and a limit of 2 uses per screen [06]. Brand *fields* are not accents.

### C25. Near-black: "use #111" vs "#111 is a tell" — high
- **A:** Open Design [06]: avoid pure black and white; use #0f0f0f/#fafafa grounds and #111 text.
- **B:** Anthropic [01]: "#0B0B0B/#111 standing in for black" is template chrome. Taste [04]: near-black ink, often warm, never #000.
- **Resolution:** ink and paper are derived from the palette (OKLCH, ink L≈0.18–0.26 with a slight tint of the brand hue; paper from the client's material), never the stock #111, #0f0f0f or #fafafa. Lint: flag those exact hexes.

### C26. Layout grammar: zig-zag vs no zig-zag; card grids — medium
- **A:** Open Design [06]: replace 3 equal cards with zig-zag, asymmetric grid, horizontal scroll or masonry. WP patterns [15]: 66/33 and 60/40 splits.
- **B:** Taste [04]: splits always put text left and visual right, never mirrored zig-zag, and card layouts (bento included) at most twice. Impeccable [05]: no icon-heading-text card grids as page structure.
- **Resolution:** no repeated mirrored zig-zag (more than 2 alternations is a tell), no 3-equal-icon-card grid by default, card layouts at most 2 per page, neighbouring sections never share a layout [04]. Record hero type and section order in the niche log.

### C27. Section order: named pattern vs "don't ship the skeleton" — medium
- **A:** UUPM [02] picks the order from a named landing pattern (Hero > Problem > Solution > Testimonials > CTA). Open Design's saas-landing template has a fixed order [06].
- **B:** Open Design anti-slop [06] says don't ship Hero→Features→Pricing→FAQ→CTA. Laws of UX [46]: follow the customers' mental model.
- **Resolution:** content inventory comes from the niche (must-haves); order and composition come from the direction. The niche log blocks reuse of the same order for the next site in that niche.

### C28. Carousels, marquees, sticky UI — medium
- **A:** UUPM [02]: carousels with prev/next/pause controls. Taste [04]: fixed header plus a phone bottom action bar on place pages. Pexels [45]: hero video loops are fine.
- **B:** Taste [04] also bans carousels, marquees, sticky elements, popups and back-to-top, which contradicts its own fixed header and bar. Open Design [06]: the 3-dot testimonial carousel is a tell.
- **Resolution:** no auto-rotating carousels or logo marquees. Use a horizontal `scroll-snap` row only when content overflows [07]. Allowed sticky UI: an opaque header and, on mobile, one call/quote bar. Anything moving for more than 5s has a pause control [04][10].

### C29. Reduced motion: kill everything vs gentler — high
- **A:** web-quality [14] turns off all animation and smooth scroll. GSAP [13] sets `duration:0`.
- **B:** Emil [07]: fewer and gentler, not zero (keep opacity and colour, drop translate, scale and parallax).
- **Resolution:** under `reduce`, keep opacity/colour transitions of 150ms or less, remove all movement, and show final states without a jump. Skip `from()` tweens entirely instead of using `duration:0` [13 §8]. Test: emulate reduce and confirm no transform animations.

### C30. Asking the client vs cold outreach — high
- **A:** Anthropic [01] proposes and confirms with the client. Impeccable [05] runs an interview (`init`/`shape`). Open Design [06] asks at most one question.
- **B:** cold outreach has no client [01 §7].
- **Resolution:** mock stage: never ask; infer from the prospect's site, Google profile and photos, and log every assumption in an "Assumptions" block of DESIGN.md. Build stage (client said yes): the assumptions become the question list.

### C31. Imagery sources — medium
- **A:** Taste [04] uses Wikimedia/Unsplash stand-ins from a vetted library. Pexels [45]: video hero loops.
- **B:** Open Design [06]: no hot-linked placeholder CDNs, use a local placeholder block. Impeccable [05]: real verified photos of the subject. Stock people as staff is banned [44][45].
- **Resolution:** priority: the prospect's own photos, then self-hosted stock flagged with `data-placeholder` (never people presented as staff, families or customers; none identifiable in funeral contexts), then a neutral placeholder block. Stock is listed in the report and replaced in the WP build.

### C32. Icon set defaults — medium
- **A:** UUPM [02] uses Phosphor in its data, and the Phosphor sheet [42] calls it a strong default. Tabler [43] has the widest coverage.
- **B:** Open Design [06]: Lucide/Feather-only is a tell. Tabler's default 2px outline is a SaaS look [43]. shadcn's Lucide is part of the stock look [35]. Duotone everywhere is a template tell [42].
- **Resolution:** no house icon set. Choose the family and stroke per site to match type weight, inline the SVGs, one family only, and log it per niche. Icons are functional (nav, contact, specs), never an icon-in-tinted-circle grid.

### C33. Numeric drift on shared basics — medium
Sources agree on the idea but not the number; an AI will pick one at random. Bexven defaults:
| Item | Values in sources | Bexven rule |
|---|---|---|
| Body measure | <80 [01], ≤62 [04], 65–75ch [05], 50–75 [06], 45–90 [47] | `max-width: 62–70ch` |
| Body line-height | 1.5 [02][14], 1.5–1.8 [04], 1.5–1.6 [06], 1.2–1.45 [47] | 1.45–1.6 by font x-height |
| Body size | 16 [02][14], 16+ [04], 15–25 [47] | 17–19px desktop, ≥16 mobile, ≥18 senior audiences |
| Tap target | 24/44 [10][14], 44 [02][07], 48 [11][14 SEO] | ≥44px all, 48px primary CTA |
| Hover / UI durations | 150–300 [02], ≤150 [07], 150/120 [04], ≤200 [06] | 120–200ms in, exits ~20% faster |

---

## Part 3 — Outdated rules / AI tells that have moved

**Principle:** tells move. The 2025 Anthropic blog [17] recommended Space Grotesk, and within a year Claude was over-using it; today's replacement list becomes next year's tell, and banning one tell breeds the next (Taste's over-correction table [04]). So the skill keeps:
1. **`references/tells.md`**, dated and versioned. Each row: tell, first seen, source(s), status `active | watch | retired`, replacement guidance. Review it quarterly and bump the version in DESIGN.md (`tells_version:`).
2. **The similar-prompt test** [01] on every plan item: "would a similar prompt for another client in this niche land here too?" If yes, revise and note what changed.
3. **The guessability test** [05]: if the look can be guessed from the category alone, or from the category plus the avoid-list, rework it.
4. **History logs** (per niche and agency-wide): fonts, palette family, hero type, section order and motion idea per site, checked mechanically (C4, C18).
A fixed blacklist alone is not enough.

| Now-a-tell | Still recommended / shipped by | What replaces it |
|---|---|---|
| Cream ground + high-contrast serif + terracotta (#F4F1EA / #D97757) | Open Design warm-editorial system [06]; Anthropic brand-guidelines (Claude's own look) [01]; the blog's "parchment" theme example [17]; Impeccable notes its own warm/bookish prior [05] | Ground and accent sampled from the client's real material (signage, building, product photos); if warm/serif is genuinely right, change at least two of ground, face class and accent |
| Near-black + one acid-green/vermilion/neon accent, glow edges | Awwwards trend [19]; Aceternity dark heroes [37]; Linear-style DESIGN.md [03]; Taste dark-neutral palettes for tech [04] | Dark only via C5's scene sentence; accent from brand, no glow |
| Broadsheet: hairlines + zero radius + small tracked mono labels + italic display serif | DESIGN.md brands (WIRED, "0 everywhere + pill", mono roles) [03]; editorial advice [47] | Only for genuinely editorial clients; otherwise one structural device that carries information [01] |
| SaaS card kit: identical rounded cards, one radius, rgba(0,0,0,.1) shadow, thin border + wide shadow | shadcn defaults (0.625rem radius, zinc) [35]; WIG "layered shadows + semi-transparent borders" [10] (= Impeccable's `gpt-thin-border-wide-shadow`) [05]; DESIGN.md spec examples [08]; Open Design saas-landing [06] | Elevation table with a stated ceiling (often flat + tone) [03]; radius language per direction |
| Template chrome: tracked caps eyebrows, "A · B · C" meta, "WORD — fragment", #111 black, mono data labels, "→" on buttons | Taste's hover arrows that move 3px [04]; Open Design #111 text [06]; WP pattern eyebrow [15] | C2, C21, C25; buttons say verb + object with no arrow glyph unless it is the site's one hover idea |
| Fonts: Inter, Roboto, Open Sans, Lato, Poppins, Montserrat, Raleway | UUPM (Inter most used) [02]; DESIGN.md examples [08]; Anthropic brand Poppins [01]; Open Design auto systems (Poppins) [06] | Per-niche pools + log (C18) |
| Fonts: Space Grotesk, JetBrains Mono, IBM Plex, Playfair Display, Crimson | Anthropic blog [17]; UUPM (Space Grotesk ×7, Playfair+Inter) [02] | Same; mono only for real code |
| Fonts: Fraunces, Newsreader, Instrument Serif/Sans, Bricolage, DM Sans/Serif, Plus Jakarta, Outfit, Geist | Google Fonts sheet shortlist [26]; Taste type.json [04]; Open Design redesign-skill [06] | Status `watch`: allowed with a written non-category reason, and the niche log check |
| Fonts: Satoshi, Clash Display, General Sans, Cabinet Grotesk | Open Design redesign-skill (Satoshi) [06] | Less-used faces from the same foundries [27] or Velvetyne display [28] where the niche allows |
| Component-library effects: bento grid, logo/testimonial marquee, shimmer/border-beam buttons, aurora/spotlight/lamp/beams, gradient text, number ticker, globe, particles, 3D tilt, text-generate/per-letter reveals, magnet buttons | Magic UI [36], Aceternity [37], React Bits [38] themselves; Taste allows bento within its card limit [04]; Open Design redesign-skill spotlight borders and grain [06] | Banned by default (lint class names and keyframes); one bespoke CSS/JS interaction tied to the brand if the direction names it |
| UUPM stock Tailwind palettes (#2563EB, #6366F1, #EA580C + slate), glassmorphism, liquid-glass for luxury, 3D for construction, trades = slate + safety orange | UUPM data [02] | Per-client OKLCH palette from brand or material [34]; Radix role steps for structure only [33] |
| Stock Radix/shadcn hues as the brand colour | [33][35] | Custom 12-step brand scale beside Radix grays |
| 2025 blog's own advice: weights 100 vs 900, 3× size jumps, atmospheric gradient backgrounds, staggered page-load reveals, load from Google Fonts CDN, "commit boldly / dark / RPG" | Anthropic blog 2025-11 [17] (still the rationale behind [01]) | C23 (one emphasis device), C22 (flat by default), C9/C10 (one optional moment), C17 (self-host), C5 (scene-based mode) |
| Elementor default kit fonts and colours; Angie's one-prompt design system | [16] | DESIGN.md tokens pushed as Variables/Global Colours [16] |
| Big-stat hero, 3-stat strip, three polished testimonials, "Most popular" plan, icon-in-tinted-circle grid, check-icon lists, generic Unsplash hero (laptop and latte, handshake) | Common outputs; UUPM wants testimonials before CTA [02] | Real proof only (C14); functional icons (C32); prospect photos (C31) |

**Watch-list entries the sources flagged themselves:** Space Grotesk overuse [17]; "first palette is already spent" for warm subjects [05]; over-correction pairs (no em dash → comma splices; no hype → calm virtue words; avoid threes → everything in pairs) [04]. Seed `tells.md` v1 with every row above, dated 2026-11-18.
