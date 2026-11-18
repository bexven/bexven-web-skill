# Duplicate rules: merged canonical list

Rules that two or more of the 47 sheets state in different words, merged into one canonical rule each (written in our own words). Built from section 3 "Rules" and section 4 "AI tells" of every sheet; numbers refer to `index.md` / sheet filenames. Contradictions are only flagged (`see conflicts.md`), not resolved. Where sources differ only in numbers, a canonical value is picked and the reason given.

**Stats:** about 804 raw tagged rules in section 3 across 47 sheets (plus a few hundred AI-tell items in section 4). They merge into **218 canonical rules** stated by 2+ sources, which carry about 700 source citations (rules and tells), so the merged part is roughly **70% smaller** than the raw statements behind it. The many single-source rules are left out here; most are tool-specific (Vercel CLI, WP-CLI, theme.json, GSAP/Lenis API, Lighthouse flags). Counting those singletons, the whole rule set shrinks by about 50%.

Tag legend: `[ban]` = AI tell to avoid; `[do]` = positive rule; `[num]` = numeric value merged.

---

## Process / brief

- **[do] Derive the visual direction from the client's own world (industry, materials, place, customers' culture, print and signage), not from web trends or habit** — sources: 01, 02, 04, 05, 08, 17, 20, 30, 47
- **[do] Write a short design plan before any code: one governing idea, palette, type roles, layout/first viewport, and principles. Check it against the brief** — sources: 01, 02, 03, 05, 06, 08, 15
- **[do] Commit to one named direction and keep every micro-decision (labels, spacing, accent, type roles) in that register** — sources: 02, 05, 06, 17
- **[do] An explicit brief or brand pin beats every anti-tell rule. Tells only govern the choices the brief leaves open** — sources: 01, 05, 06
- **[do] Ask few questions: ask only about the product or business, at most one when two directions really split. Otherwise state assumptions and go** — sources: 01, 05, 06
- **[do] Run a sameness self-test on the plan: "would a similar prompt land here too?" / "could you guess this from the category alone?" / "could a stranger tell which business this is?"** — sources: 01, 05, 06, 17
- **[do] Spend boldness in one place: one or two strong signatures applied consistently, everything else quiet** — sources: 01, 03, 05, 06 (06: "~80% proven patterns + ~20% distinctive")
- **[do] Remove any element that carries no meaning. Before shipping, cut one more accessory** — sources: 01, 46, 06 (empty section = composition problem, not a filler problem)
- **[do] Keep a record of past choices (fonts, palettes, heroes) so the next project in the same niche lands somewhere new** — sources: 01, 04, 17
- **[do] Turn every user correction into a written class-level rule (with its reason) in DESIGN.md or a Gotchas list. Prefer a lint check over a sentence** — sources: 07, 18
- **[do] Follow the customer's mental model and the niche's expected pages and content (e.g. home services: emergency contact + certifications; funeral home: services, obituaries, pre-planning). Be distinctive in look, not in where things are** — sources: 02, 46
- **[do] Keep one DESIGN.md per client: overview/thesis, 5–7 key characteristics, tokens with names and jobs, short Do/Don't lists with reasons, a "known gaps" list** — sources: 03, 08, 05 (05 writes it *after* the build; timing → see conflicts.md)
- **[do] Keep the Don't list short and specific, each item a hard limit with a reason** — sources: 03, 08
- **[do] Save the static redesign screenshots as the reference for the later WordPress build and compare against them** — sources: 12, 16

## Typography

- **[ban] Don't use the over-used default faces as the brand face: Inter, Roboto, Open Sans, Lato, Montserrat, Poppins, Space Grotesk, Plus Jakarta Sans, DM Sans, Raleway, Arial/system** — sources: 01, 04, 05, 06, 17, 26, 47, 08 (its own examples use them) (lists differ: 17 still *recommends* Space Grotesk and Playfair, which 05/26 call tells → see conflicts.md)
- **[ban] Treat newer "fashionable free" faces as tells too unless picked for a reason (Satoshi, Clash Display, General Sans, Cabinet Grotesk; Fraunces, Playfair "luxury", Instrument Sans, Outfit)** — sources: 05, 26, 27
- **[ban] Never use a system or installed face (system-ui, Arial Black, Impact, Georgia) as the display/brand voice. Self-host a sourced face with a real fallback chain** — sources: 04, 05, 06, 17, 47
- **[do] One family, or two clearly distinct ones; each face gets one role with no crossover** — sources: 01, 03, 04, 06, 17, 28 (03 allows three faces in three roles; canonical: max 2, a third only for a mono role)
- **[do] Display-only faces (experimental/foundry) must be paired with a sturdy text face** — sources: 28, 03, 17
- **[do][num] Body text at least 16px; default 17–18px on desktop; 18px+ for senior audiences** — sources: 02, 04, 05, 14, 47 (47: 15–25 range, 17–20 default; 02: 18+ seniors). Canonical 17–18px desktop / 16px mobile floor, since our niches skew older
- **[do][num] Body line-height about 1.5, unitless** — sources: 02, 04, 06, 14, 47, 08 (unitless). Values: 1.5 (02, 14), 1.5–1.6 (06), 1.5–1.8 (04), 1.2–1.45 (47). Canonical 1.5 (1.4–1.6 by x-height), since four sources cluster there
- **[do][num] Measure about 65ch: set max-width on text containers; never edge-to-edge text** — sources: 01, 04, 05, 06, 07, 47. Values: <80 (01), ≤62 chars (04), 65–75ch (05), 50–75 / 65ch (06), ~65ch (07), 45–90 avg / 60–70ch (47). Canonical `max-width: 65ch` (range 60–70), the overlap of all six
- **[do][num] Tight leading on large headings (about 1.0–1.2)** — sources: 06, 07, 47
- **[do][num] Slight negative tracking on large display, with a floor** — sources: 03, 04, 05, 06, 07. Values: −0.5% to −4.5% at 40px+ (04), floor −0.04em (05), −0.01 to −0.03em (06), ~−0.02em (07). Canonical −0.01 to −0.03em at 32px+, never below −0.04em (05's detector flags "extreme negative tracking")
- **[do][num] All caps only for short strings, always with added tracking** — sources: 03, 06, 47, 05 (all-caps-body detector). Values: +2–6px (03), +0.06–0.1em (06), +0.05–0.12em (47). Canonical +0.06–0.1em. (Whether caps labels should exist at all → see conflicts.md: 01/04 ban them)
- **[do] Sentence case for headings and buttons, one capitalisation style site-wide** — sources: 01, 04, 06, 08, 47, 10 (sentence case on marketing pages)
- **[do] Define a deliberate type scale with named roles (display/headline/body/label/caption): size, weight, line-height, tracking per role** — sources: 01, 03, 05, 06, 08 (ratio: 1.125–1.2 app UI (05), 1.2–1.25 with 6–8 sizes (06); 17 wants 3x jumps → see conflicts.md)
- **[ban] Bold/heavy display weights by default. Use a small weight system (about 400/500/600); 700+ rarely** — sources: 03, 04, 06 (04: headlines at 400, never 700/800; 17 wants extreme 100 vs 900 → see conflicts.md)
- **[ban] Oversized headings over tiny body text** — sources: 04, 05 (display ≤6rem, oversized-h1 detector), 47
- **[do] One explicit emphasis device. No single accented word in a headline (italic/bold/colour switch), no marker highlights, never bold + italic together** — sources: 01, 03, 04, 47
- **[do] Body text left-aligned, ragged right. Never justify body text (unless hyphenated); centre only short lines** — sources: 04, 05 (justified-text detector), 06, 47
- **[do] More space above a heading than below it, so it belongs to the text that follows** — sources: 05, 47
- **[do] `text-wrap: balance` on headings, `pretty` on paragraphs to avoid orphans/widows** — sources: 05, 06, 09, 10 (13: not on SplitText-animated lines)
- **[do] `font-variant-numeric: tabular-nums` for prices, stats, tables and changing numbers** — sources: 05, 06, 07, 09, 10
- **[do] Real typographic characters: curly quotes and apostrophes, real ellipsis …, en/em dashes, non-breaking space between number and unit. Check that the CMS keeps them** — sources: 09, 10, 47
- **[do] Read each font's licence (OFL, ITF FFL, custom EULA) and record it before use. Ship only fonts that allow web embedding/self-hosting, and keep the licence file with the fonts** — sources: 26, 27, 28, 29, 30, 47
- **[do] Check glyph coverage for the client's language (diacritics, Dutch ij, German ß) before choosing a face** — sources: 28, 07 (break-test with diacritic names)
- **[do] Look at real sites in or near the niche to see actual pairings before choosing one** — sources: 21, 30

## Colour

- **[do] Role-named colour tokens (primary, accent, surface, text, border, destructive…) stored once; no raw hex in components** — sources: 02, 03, 06, 08, 15, 16, 34, 35 (06 lints >12 raw hex outside `:root`)
- **[do] Every fill token has a paired "on"/foreground token** — sources: 02, 33, 35
- **[do] Give each colour a human name, a job, and an explicit list of where it may and must NOT appear** — sources: 03, 08
- **[do][num] Exactly one accent, used scarcely (primary CTA, focus ring, links); never invent a second** — sources: 03, 04, 06, 46 (Von Restorff), 08 (few purposeful colours), 15 (primary reserved for CTAs). Values: accent <3% of screen outside the CTA (04), 5–10% of palette, ≤2 visible uses per screen (06). Canonical: about 5% of the surface and ≤2 accent uses per viewport. (05 "committed/drenched" and 17 "dominant colour" disagree → see conflicts.md)
- **[do][num] Neutral-dominant UI: colour comes from photos, product and logo** — sources: 04 (90–95% neutral), 06 (70–90%). Canonical about 85%
- **[ban] Purple/violet/indigo, especially gradients (Tailwind #6366F1/#7C3AED, purple→blue hero gradients, indigo glow on near-black)** — sources: 02 (for trust industries), 04 (hue ~270–330 pushed to blue/rose), 05 (ai-color-palette detector), 06 (P0 lint), 15 (purple preset gradient in its own examples), 17, 37 (02 *recommends* #6366F1 for AI/SaaS rows → see conflicts.md)
- **[ban] Decorative gradients, glows, glassmorphism, grain, gradient text and gradient washes. Use a gradient only if it carries hierarchy** — sources: 01, 03, 04, 05, 06, 08, 36, 37, 38 (17 advises "layered gradients" atmosphere → see conflicts.md)
- **[ban] Cyan/neon-on-near-black single-accent look** — sources: 01, 05, 37
- **[ban] Warm cream ground + high-contrast serif display + terracotta accent as a default** — sources: 01, 05
- **[do] Build palettes in OKLCH (perceptual lightness); same-weight sets = fix L/C, rotate H; derive hovers by shifting L** — sources: 05, 34, 35
- **[do] If the brand colour fails text contrast, use a darker shade of it for text and keep the bright one for fills** — sources: 02 (accents "adjusted to 4.5:1"), 06, 33 (step 11/12 for text, step 9 for fills)
- **[do] Lock the client's existing brand colour and build the scale around it** — sources: 32, 33, 16 (carry exact mockup colours into Elementor)
- **[do] Tint neutrals, secondary text, borders and shadows toward the hue they sit on; never plain grey on colour** — sources: 05, 10, 33, 04 (warm near-black ink)
- **[do] Light vs dark is a deliberate decision, never a default; dark is not the default for local service sites** — sources: 02, 04, 05 (methods differ: by category (02), tech only (04), physical scene (05) → see conflicts.md)
- **[do] If dark mode exists, design it alongside light under the same token names; don't invert** — sources: 05, 08, 31, 35, 02 (test both)
- **[do] Dark themes set `color-scheme`, and `<meta name="theme-color">` matches the page background** — sources: 07, 09, 10
- **[do] On dark surfaces use a surface ladder plus thin semi-transparent borders instead of shadows and solid dark borders** — sources: 03, 06, 10
- **[do] Contrast is designed per touching pair (text-on-bg, button-on-bg), not per swatch** — sources: 32, 31, 08 (linter checks component pairs)

## Layout & spacing

- **[ban] Unvaried default section skeleton (Hero → Features → Pricing → FAQ → CTA; eyebrow + heading + lede + 3 cards on every section)** — sources: 04, 05, 06, 15, 17, 24, 47 (02 picks from named landing-order patterns → see conflicts.md)
- **[ban] Three equal feature cards / same-size icon+heading+text card grids as page structure. Use asymmetric splits (66/33, 60/40), spans, offsets** — sources: 01, 04, 05, 06, 15, 35, 46 (04: card layouts max twice per page)
- **[ban] Hero-metric template: big number + small label + stats strip under the hero** — sources: 01, 04, 05
- **[ban] Fake 01/02/03 numbering and step numbers on parallel items. Structural devices (borders, numbers, dividers) must encode real information** — sources: 01, 04, 05
- **[do] The first viewport shows the most characteristic thing in the client's world (the real place, product, mechanism), not a generic hero** — sources: 01, 04, 05
- **[do] Pace the page: vary density, scale, imagery and quiet between sections instead of perfect symmetry** — sources: 03, 05, 06, 15
- **[do] Named spacing scale on a 4/8px base unit** — sources: 02, 03, 08, 15
- **[do][num] Proximity: spacing inside a group clearly smaller than between groups; section rhythm set by density** — sources: 02, 03, 15, 46. Values: 8–16px inside / 48–96px between (46); 24–96px marketing (02); 48–64px dense vs 120px luxury (03). Canonical 8–16px within groups, 64–120px between sections on desktop (lower end for dense trades, upper for calm/luxury)
- **[do][num] One shared container with a fixed max width for header, sections and footer** — sources: 04 (1280px, 80px gutter), 08 (1200px). Canonical 1200–1280px
- **[do] Mobile-first; no horizontal scroll; reflow at 320px; usable at 200% zoom** — sources: 02, 07, 10, 12, 14
- **[do] Layouts survive short, long and empty content: `min-width:0` on flex children, `overflow-wrap:anywhere` on emails/URLs, never truncate prices/dates** — sources: 07, 09, 10
- **[do] Use `100dvh`/`100svh`, not `100vh`, for full-height heroes** — sources: 06, 07
- **[do] Respect safe-area insets (`env(safe-area-inset-*)`) on full-bleed layouts** — sources: 07, 09, 10
- **[do] Let CSS flex/grid size things; don't measure layout in JS** — sources: 09, 10
- **[do] Adjust optically, not mathematically (±1px, bottom padding slightly larger)** — sources: 06, 10
- **[do] One primary job per section or text element; chunk long copy into short labelled groups** — sources: 01, 46
- **[do] Group with a shared region sparingly; max two box levels. Boxing everything kills the signal** — sources: 04, 46
- **[do] Derive the radius scale from one base or one stated "radius language"; don't mix sharp and round in one view** — sources: 03, 08, 35 (01 calls "one radius everywhere" a tell → see conflicts.md)
- **[do] Nested radii: inner element tighter than its container (concentric)** — sources: 06, 10
- **[do] Align shared elements across side-by-side cards (titles, prices, buttons pinned to the bottom)** — sources: 06, 12 (unequal card heights flagged in QA)

## Components

- **[ban] SaaS card kit: identical rounded cards, mid radius (8–12px) everywhere, the same soft blurred shadow, hairline border + wide shadow** — sources: 01, 03, 04, 05, 35
- **[ban] Cards inside cards / patterned panel inside card** — sources: 04, 05
- **[ban] Coloured border-left/right accent on rounded cards/callouts** — sources: 05, 06
- **[ban] Tracked eyebrow/kicker label above every heading (hero eyebrow chips included)** — sources: 01, 04, 05, 15 (its own examples use one) (47 allows caps eyebrows → see conflicts.md)
- **[ban] Component-library signature effects: shimmer/moving borders, border beams, spotlight/glass cards, aurora/beam backgrounds, globe, bento grid, marquee logo strips, tilt cards, magnetic buttons, text-generate/decrypt effects, number tickers** — sources: 03, 04, 05, 06, 36, 37, 38
- **[do] Specify and build every state: default, hover, focus, active, disabled, loading, error, empty** — sources: 03, 05, 08, 10, 09
- **[do] Hover/active/focus clearly stronger than the rest state** — sources: 09, 10
- **[do] Limit the button vocabulary; one primary CTA per viewport, at most one secondary; never two equal primaries in a fold** — sources: 03, 46, 04 (main action worded the same everywhere)
- **[do] Same role = same style; different roles look different; anything that looks clickable is clickable** — sources: 10, 46
- **[do] Destructive actions need confirmation or undo** — sources: 09, 10
- **[do] No spinner/skeleton for fast loads (<300ms); otherwise skeletons that mirror the final layout, with a show-delay** — sources: 05, 07, 10 (10: 150–300ms delay, 300–500ms minimum visible)
- **[do] Tooltips: delay the first; neighbours then open instantly. Prefer inline help** — sources: 07, 10
- **[do] Every gesture or hover-only action has a visible click/keyboard alternative** — sources: 07, 09, 10
- **[do] No modal or popup unless the task needs interruption; never before the visitor has read anything (no interstitials, chat bubbles, back-to-top clutter)** — sources: 04, 05, 14, 46, 06 (sun/moon toggle, pill "New" badges as chrome tells)
- **[do] Avoid carousels for key content. If one exists: prev/next/pause, stops on focus and reduced motion, native scroll-snap** — sources: 02, 06, 07, 46 (04 bans carousels outright → see conflicts.md)
- **[do] Use accessible primitives/APG patterns for dialogs, menus, toasts; don't hand-roll them** — sources: 07, 10
- **[do] Repeated blocks (service cards, testimonials, CTA band) become reusable components that reference base tokens** — sources: 03, 08, 16
- **[do] Theme browser details: selection colour, focus rings, underline offset, scrollbars, native `<select>` colours** — sources: 05, 09, 10

## Imagery & icons

- **[do] Real photos of the actual business, place and work lead the page; one decisive photo beats five mediocre ones** — sources: 03, 04, 05, 44, 45
- **[ban] Generic stock clichés (laptop + latte, handshake, smiling team or call centre, mood stock instead of the product)** — sources: 04, 44, 45, 47
- **[do] Stock only as clearly flagged placeholders in mockups (attribute + comment + hand-off note); never presented as staff, clients or testimonial authors** — sources: 04, 05, 06, 44, 45
- **[do] Funeral/grief contexts: no identifiable people. Use hands, flowers, light, architecture** — sources: 44, 45
- **[ban] Hot-linked placeholder CDNs (Unsplash, placehold.co, picsum). Download, optimise and self-host, or use a local placeholder block** — sources: 06, 15, 44, 45
- **[do] Alt text: real description for informative images, `alt=""` for decorative ones** — sources: 02, 09, 10, 12, 15
- **[do] Background/hero video only compressed, muted, `playsinline`, with a poster frame and reduced-motion stop** — sources: 10, 45 (47 calls full-screen video backgrounds a trend tell → see conflicts.md)
- **[do] One icon family per site, one weight/stroke** — sources: 02, 05, 06, 42, 43
- **[ban] Emoji or unicode as icons** — sources: 02, 05, 06
- **[do][num] Match icon stroke/weight to the type** — sources: 42, 43, 06, 10. Values: 1.25–1.5 next to light/serif and 2 next to bold sans (43); 1.6–1.8 monoline (06); Thin/Light vs Bold/Fill (42). Canonical: stroke follows body weight (about 1.5 default, 2 for bold industrial)
- **[do] Inline only the SVGs used, with `currentColor`; never load an icon webfont/sprite for a few icons** — sources: 06, 14, 42, 43
- **[ban] Grids of icon-in-tinted-circle/rounded-square feature cards and check-icon lists on every section** — sources: 04, 05, 42, 43
- **[ban] Cliché icon metaphors and default-kit icon sets used untouched (rocket = launch; Lucide/Feather-only)** — sources: 06, 35

## Copy

- **[ban] AI slop vocabulary: delve, elevate, unlock, seamless, unleash, cutting-edge, robust, bespoke, streamline, empower, world-class, game-changer, tapestry, nestled** — sources: 04, 05, 06, 09 (easy/simple/quick)
- **[ban] AI cadences: "X. No Y." runs, "not X but Y", two-fragment headings, em-dash saturation, "WORD — fragment" labels** — sources: 01, 04, 05, 09 (47 recommends proper em dashes for breaks → see conflicts.md)
- **[do] Buttons and links name the specific action or result (verb + object); never Submit, OK, Continue, Read more, Click here** — sources: 01, 04, 05, 06, 08, 09, 10, 14, 15
- **[do] Keep one name per action and concept throughout (nav, hero, closing CTA, phone bar; Publish → Published)** — sources: 01, 04, 08, 10
- **[do] Errors say what happened and how to fix it; no apologies, no "Oops!"** — sources: 01, 05, 06, 08, 09, 10
- **[do] Empty states invite or teach the next action** — sources: 01, 05, 08
- **[do] Never invent facts: metrics, prices, hours, testimonials, reviews, customers. Use real data or a clearly labelled placeholder/assumption** — sources: 02, 04, 05, 06, 46, 03 (list "known gaps" instead of inventing)
- **[do] Testimonials and social proof only when real and verifiable, placed near the CTA** — sources: 02, 04, 44, 45, 46
- **[ban] Lorem ipsum and "Feature one" filler; placeholder copy must read like real content** — sources: 04, 06, 15
- **[do] Plain words from the customer's view, active voice, second person** — sources: 01, 05, 09, 10, 46 (customers' own words)
- **[do] A voice specific to each client (2–3 tone words plus what they rule out), not one house voice for everyone** — sources: 04, 05, 08
- **[do] No exclamation marks (at most one per page, none in success messages)** — sources: 04, 06, 47
- **[do] Numerals for counts; locale-aware number/date/currency via `Intl`; real pluralisation** — sources: 07, 09, 10
- **[do] Credit photographers in one quiet line (footer/hand-off)** — sources: 04, 44, 45

## Motion

- **[do] Respect `prefers-reduced-motion` on every effect (CSS query, `gsap.matchMedia`, Lenis default), showing the finished static state** — sources: 01, 02, 04, 06, 07, 08, 09, 10, 11, 12, 13, 14, 39, 40, 41, 45 (07: "fewer and gentler, not zero", keep opacity; 14: turn all motion off → see conflicts.md)
- **[do] Animate only `transform` and `opacity`; never width/height/top/left/margin** — sources: 02, 04, 06, 07, 08, 09, 10, 13, 14
- **[ban] `transition: all`; list properties explicitly** — sources: 07, 09, 10
- **[ban] Fade/slide-up on every section (AOS-style scroll reveals); allow one orchestrated moment per page** — sources: 01, 04, 05, 07, 13, 17, 39, 41 (04 bans scroll reveals entirely; 07 allows once-only reveals on marketing pages)
- **[do] Every animation names its purpose (feedback, state change, spatial continuity, explanation); "looks cool" is cut** — sources: 01, 06, 07, 09, 10
- **[do][num] Exits faster than entrances** — sources: 02, 04, 05, 07, 08, 09. Values: 150 in / 120 out (04); 210 in / 150 out (09); 250 in / 200 out (07). Canonical exit ≈ 75–80% of entry duration
- **[do][num] Duration bands by job** — sources: 02, 04, 05, 06, 07, 09. Press/hover feedback 50–160ms (04: 90 press, 06: 50–100, 07: 100–160, 05: 100–150); state change 150–300ms (02, 05, 06); dropdown/popover 150–250ms (07); overlays/modals/drawers 200–500ms (05, 06, 07); one focal entrance 500–800ms (05). Canonical: 100–150 / 150–250 / 250–400 / ≤800ms for the single hero moment
- **[do] Ease-out for entrances (strong custom curve, no hand-made ones), no bounce or overshoot by reflex** — sources: 04, 05, 07, 08, 13 (09 uses ease-in for exits; 07 says never ease-in on UI → see conflicts.md)
- **[do] One motion vocabulary: shared duration/easing tokens named by purpose, set once** — sources: 04, 07, 08, 13
- **[ban] Hover lift/scale/glow on every card; keep hover modest and only on clickable things** — sources: 01, 05, 07 (04 makes lift-on-hover mandatory for linked cards → see conflicts.md)
- **[do] Gate hover styles behind `(hover: hover) and (pointer: fine)`** — sources: 04, 07
- **[do] Motion is interruptible; anything moving >5s or autoplaying gets pause/stop** — sources: 02, 04, 09, 10, 14
- **[ban] Infinite decorative loops on persistent elements (pulsing dots/badges, glowing borders, gradient orbs, twinkles)** — sources: 04, 05, 06, 07
- **[ban] Smooth-scroll libraries and parallax on local-business sites by default** — sources: 04, 41, 07 (drop parallax under reduced motion), 02 (turn off hero parallax)
- **[ban] Count-up numbers on load and charts redrawing on mount** — sources: 07, 36
- **[do] CSS first, then WAAPI/small libraries, GSAP only for sequencing/scroll-linking/runtime control** — sources: 07, 10, 13, 17, 40
- **[do] Stagger with one stagger call, varied by importance, short totals; never uniform `i * 0.1` or parent slide + child stagger** — sources: 07, 13
- **[do] `will-change` only on elements that animate, after measuring; never on `*`** — sources: 07, 13
- **[do] Start from an already visible default; hide content for an entrance only once JS runs** — sources: 05, 13
- **[do] Directional slides only for hierarchy or ordered sequences** — sources: 07, 09

## Accessibility

- **[do][num] Contrast: body text 4.5:1, large text 3:1, UI components and focus rings 3:1 against adjacent colour** — sources: 01, 02, 05, 06, 08, 11, 14, 15, 31 (10, 33 prefer APCA: Lc 60/90). Canonical WCAG AA 4.5/3/3, APCA as a second check (04 demands 7:1 for body → see conflicts.md)
- **[do] Visible focus on everything (`:focus-visible`); never `outline: none` without a replacement** — sources: 01, 02, 04, 09, 10, 14
- **[do][num] Touch targets at least 44×44px with 8px+ between; expand hit area invisibly** — sources: 02, 03, 04, 05, 07, 10, 14, 46, 11. Values: 24px desktop / 44 mobile (10, 14), 48 (11, 14's SEO skill). Canonical 44px, 48px for primary mobile CTAs and the phone button
- **[ban] Disabling zoom (`user-scalable=no`, `maximum-scale=1`)** — sources: 02, 07, 09, 10
- **[do] Skip link, `lang`, landmarks, one logical heading hierarchy with no skipped levels** — sources: 04, 06, 09, 10, 11, 14, 15
- **[do] Never colour alone for status; add text or icon** — sources: 02, 10, 14, 46
- **[do] Native elements before ARIA; links are `<a>`, actions are `<button>`, never clickable divs** — sources: 09, 10, 14
- **[do] Decorative icons `aria-hidden`; icon-only buttons get an accessible name** — sources: 02, 09, 10, 11, 12, 14, 42, 43
- **[do] Sticky headers never cover focused elements or anchored headings (`scroll-margin`/`scroll-padding`)** — sources: 02, 09, 10, 14, 41
- **[do] Announce async updates, toasts and validation via polite live regions** — sources: 09, 10, 14
- **[do] Captions/transcripts for meaningful media; no autoplay without controls** — sources: 09, 10, 14
- **[do] Manage focus in dialogs and mobile menus: move in, trap, return on close** — sources: 10, 11
- **[do] Also honour forced-colors, `prefers-contrast` and `prefers-reduced-transparency`** — sources: 07, 11, 12
- **[do] Keep a11y as a silent quality floor checked in audit/QA, not as reminders in the design prompt** — sources: 01, 05

## Performance

- **[do][num] Core Web Vitals targets: LCP ≤2.5s, CLS ≤0.1, INP ≤200ms** — sources: 02 (CLS), 04, 11, 14, 46 (LCP). Values: 04 allows LCP <4.5s under CPU throttling. Canonical: Google "good" thresholds (11/14/46 agree)
- **[do] Every image gets width/height or `aspect-ratio`; reserve space for embeds, fonts and cookie banners (no CLS)** — sources: 02, 09, 10, 11, 14
- **[do] The hero/LCP image is a real `<img>` in the HTML, never lazy, with `fetchpriority="high"`** — sources: 09, 10, 11, 14
- **[do] Lazy-load below-the-fold images (`loading="lazy" decoding="async"`)** — sources: 02, 09, 10, 14
- **[do] AVIF/WebP with `srcset`/`sizes`; never ship the native multi-MB file to mobile** — sources: 02, 09, 11, 14, 44
- **[do] Fonts: self-hosted WOFF2, `font-display: swap`, subset, preload only 1–2 critical files, prefer one variable file** — sources: 05, 09, 10, 14, 26, 11 (size-adjusted fallbacks for CLS)
- **[do][num] Font budget** — sources: 04 (max 2 families / 4 files), 06 (max 2 typefaces), 14 (fonts <100KB). Canonical ≤2 families, ≤4 files, ≤100KB
- **[do][num] Page-weight budget** — sources: 04 (images <1200KiB, single <350KiB), 14 (page <1.5MB, above-fold images <500KB, JS <300KB). Canonical page <1.5MB with images ≤1.2MB, as both agree around that size
- **[do] Scripts `defer`/module; analytics, chat, pixels and widgets after first paint or behind facades** — sources: 09, 14, 39
- **[do] Preconnect to required origins; preload only what is critical/late-discovered** — sources: 09, 10, 14
- **[do] Video (`autoplay muted loop playsinline`) instead of animated GIF** — sources: 09, 10
- **[do] `content-visibility: auto` for long off-screen sections or lists** — sources: 09, 10
- **[do] Batch DOM reads before writes; no layout thrashing** — sources: 09, 10, 13
- **[do] Long CDN cache for static assets (hashed = immutable, HTML revalidates)** — sources: 09, 14
- **[do] Self-host libraries and pin exact versions; no `@latest`, no polyfill CDNs** — sources: 14, 18, 39, 40
- **[do] Measure with a trace under mobile throttling, fix the biggest bottleneck, re-measure the same URL; report lab as lab** — sources: 11, 14, 15
- **[ban] Claiming speed or ranking gains without before/after measurement or field data** — sources: 11, 14

## SEO

- **[do] Every page ships a unique `<title>`, meta description, og:image and canonical** — sources: 04, 06, 11, 12, 14
- **[do] One descriptive primary heading and no skipped levels** — sources: 11, 12, 14, 15 (12 checks for exactly one `<h1>`; 14 says don't fail on more than one → minor, canonical: one h1 as the default)
- **[do] Descriptive link text, never "click here"/"read more"** — sources: 14, 15, 10
- **[do] Lighthouse SEO category as a minimum on every static redesign before outreach** — sources: 11, 14

## Forms / nav

- **[do] Visible label on every field; placeholder is never the label** — sources: 02, 04, 09, 10, 14, 46
- **[do] Correct `type`, `name`, `autocomplete`, `inputmode` (and `enterkeyhint`) on every field** — sources: 07, 09, 10, 14, 46
- **[do] Errors inline next to the field; on submit focus the first error** — sources: 02, 04, 09, 10, 14
- **[do] Never block paste; support password managers and autofill** — sources: 02, 09, 10, 14
- **[do] Mobile input font-size ≥16px (avoids iOS zoom)** — sources: 07, 10
- **[do] Short forms: only the needed fields, no redundant entry** — sources: 02, 14, 46
- **[do] Spellcheck off for email/codes; warn before leaving unsaved changes** — sources: 09, 10
- **[do][num] Main nav kept short** — sources: 04 (4–6 one-word nouns), 46 (5–7). Canonical 5–6 items, the overlap
- **[do] Conventional nav: logo links home top-left, contact last, phone number tappable** — sources: 06, 46, 04
- **[do] Mobile: a phone/quote action within thumb reach (sticky bottom bar after the hero CTA scrolls away)** — sources: 04, 46, 06 (CTA above the fold, phone tappable)
- **[do] Show the current page in nav (`aria-current`)** — sources: 02, 14
- **[do] Real `<a>` links; state lives in the URL; back/forward restores scroll** — sources: 09, 10, 41
- **[do] In-page anchors offset for the sticky header** — sources: 10, 14, 41

## QA / tooling

- **[do][num] Screenshot every page at fixed breakpoints in a real (headless) browser** — sources: 02, 04, 05, 06, 07, 10, 12, 16. Values: 375/768/1024/1440 (+1920) (12); 1440/1024/820/768/390/320 (04); 1440/768/375 (06); 375/768/1280 (16); 320 + widest (07). Canonical 320 / 375 / 768 / 1024 / 1440, the union of the most-cited widths
- **[do][num] Capped build → screenshot → review → fix loop, then hand leftovers to a human** — sources: 04, 05 (max 2 fix rounds), 06, 12 (max 3). Canonical 3 rounds
- **[do] Settle fonts, lazy images and entrance animations before capturing** — sources: 05, 12
- **[do] Run a deterministic lint/detector for AI tells after each generation and feed results into the fix pass** — sources: 05, 06, 07, 08
- **[do] Critique with structure and fresh eyes (separate reviewer, scored dimensions, evidence per finding)** — sources: 01, 05, 06
- **[do] Measure contrast, overlap, tap targets and perf by script, not by eyeballing screenshots** — sources: 11, 12
- **[do] Zero console errors and zero failed (4xx/5xx) requests before handoff** — sources: 11, 12, 14
- **[do] Break-test with worst-case content (long names, diacritics, 0/1/many counts, missing images) and drive every state** — sources: 05, 07, 10
- **[do] Test on real iPhone Safari / a WebKit pass before sending outreach links** — sources: 07, 10, 12, 41
- **[do] Keyboard pass: Tab through the page, check focus order matches visual order** — sources: 11, 14, 41
- **[do] Check the accessibility tree/snapshot for names, heading order and labels** — sources: 10, 11, 12
- **[do] Emulate reduced motion, dark scheme and forced colours on at least the homepage** — sources: 11, 12
- **[do] Playwright (our own Python script) for screenshot sweeps; Chrome DevTools MCP only for traces/Lighthouse/CSS cascade** — sources: 11, 12
- **[do] Browser tools run `--isolated`, never on logged-in client admin profiles unless asked** — sources: 11, 12
- **[do] Write big reports to files and filter them; don't read whole JSON/console dumps into context** — sources: 11, 14
- **[do] Report findings as `file:line - issue`, grouped by file, no preamble** — sources: 09, 10

## WordPress / Elementor

- **[do] Self-host all fonts in WP/Elementor (Custom Fonts or "Load Google Fonts Locally"); no Google/Fontshare CDN calls (GDPR)** — sources: 26, 27, 29
- **[do] Keep the font's licence file next to the uploaded WOFF2** — sources: 28, 29
- **[ban] Builder defaults left in place (Elementor default kit, theme type scale, Angie design system). Override type scale, spacing and colours per client** — sources: 16, 47
- **[do] Design tokens go into global presets/Variables (theme.json settings, Elementor Variables + Global Classes); no inline styles or ad-hoc classes per element** — sources: 15, 16
- **[do] Enqueue scripts from the child theme (never the parent), local copies, in the footer, with dependencies** — sources: 39, 41
- **[do] Fix CSS specificity at the source (inspect the cascade); don't stack `!important`** — sources: 01, 11
- **[do] Audit plugin/widget bloat (scripts per page, render-blocking CSS)** — sources: 11, 15
- **[ban] Risky direct edits on live data (hand-editing `_elementor_data`, unconfirmed prod WP-CLI ops)** — sources: 15, 16

## Skill authoring

- **[do] Keep the always-loaded guidance compact; load detail from references on demand** — sources: 17, 18
- **[do] Anti-tell lists breed new tells: recommended picks become the next default (Space Grotesk, Satoshi, "calm" virtue words), so rotate and re-check the lists** — sources: 04 (over-correction table), 05 ("first palette already spent"), 17, 27, 25, 31
- **[do] Bundle a deterministic checker script when the agent keeps redoing the same checks** — sources: 05, 06, 18
- **[do] Pin tool/library versions in scripts and instructions** — sources: 18, 39, 40
- **[do] Grow the skill from real corrections (a Gotchas list in SKILL.md)** — sources: 07, 18

---

## Strongest consensus (5+ sources)

1. **Respect prefers-reduced-motion** — 16 sources (01, 02, 04, 06, 07, 08, 09, 10, 11, 12, 13, 14, 39, 40, 41, 45)
2. **Contrast 4.5:1 body / 3:1 large + UI** — 11 sources (01, 02, 05, 06, 08, 10, 11, 14, 15, 31, 33)
3. **Specific verb+object button/link labels, no Submit/Read more** — 9 (01, 04, 05, 06, 08, 09, 10, 14, 15)
4. **Animate transform/opacity only** — 9 (02, 04, 06, 07, 08, 09, 10, 13, 14)
5. **Touch targets ≥44px** — 9 (02, 03, 04, 05, 07, 10, 11, 14, 46)
6. **No decorative gradients/glass/glow** — 9 (01, 03, 04, 05, 06, 08, 36, 37, 38)
7. **Visual direction from the client's own world, not trends** — 9 (01, 02, 04, 05, 08, 17, 20, 30, 47)
8. **Role-named tokens, no raw hex in components** — 8 (02, 03, 06, 08, 15, 16, 34, 35)
9. **Avoid over-used default fonts** — 8 (01, 04, 05, 06, 08, 17, 26, 47)
10. **No fade-up on every section; one orchestrated moment** — 8 (01, 04, 05, 07, 13, 17, 39, 41)
11. **Screenshot at fixed breakpoints in a real browser** — 8 (02, 04, 05, 06, 07, 10, 12, 16)
12. **Decorative icons aria-hidden, icon buttons named** — 8 (02, 09, 10, 11, 12, 14, 42, 43)
13. **No three-equal-card / identical card grids** — 7 (01, 04, 05, 06, 15, 35, 46)
14. **No purple/indigo/violet (gradients)** — 7 (02, 04, 05, 06, 15, 17, 37)
15. **No default Hero→Features→Pricing→FAQ→CTA skeleton** — 7 (04, 05, 06, 15, 17, 24, 47)
16. **Never invent facts/metrics/testimonials** — 6 (02, 03, 04, 05, 06, 46)
17. **Visible focus, never outline:none** — 6 (01, 02, 04, 09, 10, 14)
18. **Exit faster than enter** — 6 (02, 04, 05, 07, 08, 09)
19. **Measure ~65ch** — 6 (01, 04, 05, 06, 07, 47)
20. **Visible form labels, never placeholder-only** — 6 (02, 04, 09, 10, 14, 46)
21. **Errors say what happened + how to fix** — 6 (01, 05, 06, 08, 09, 10)
22. **Real photos lead; stock only as flagged placeholders** — 5 each (03, 04, 05, 44, 45 / 04, 05, 06, 44, 45)
23. **One icon family, one weight** — 5 (02, 05, 06, 42, 43)
