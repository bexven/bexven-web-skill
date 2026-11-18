# AI tells - tells v2026-11

Version: **2026-11** · dated 2026-11-18 · next review: 2027-02 (review quarterly; bump the version and set `tells_version:` in each new DESIGN.md).
Single source: `bexven-web/shared/tells.md`, copied into each skill's `references/` by `scripts/sync_shared.py`. Edit here, then re-sync.

**Status:** `active` = banned by default (a client brief or existing brand can override; write the reason in DESIGN.md). `watch` = allowed only with a written non-category reason in DESIGN.md and a passing niche-log check. `retired` = no longer a tell, kept for history.

**Why a dated list.** Tells move: a replacement that is fresh today becomes next year's default (Space Grotesk went from recommended to overused within a year). Banning one tell breeds the next. So the list is never enough alone; always run the two tests below and the niche-log check.

## The two tests (run on every direction and every finished page)

1. **Similar-prompt test:** "Would a similar prompt for another client in this niche land here too?" If yes, change it and note in DESIGN.md what changed.
2. **Guessability test:** "Can the look be guessed from the category alone, or from the category plus this avoid-list?" If yes, rework it.

Supporting checks: *stranger test* (with the logo covered, can someone tell which business this is?) and *memory test* (what would a visitor describe an hour later? "a website" fails).

## Visual

| Tell | Status | First seen | What replaces it |
|---|---|---|---|
| Cream ground + high-contrast serif display + terracotta accent (#F4F1EA / #D97757 family) | active | 2025 | ground and accent sampled from the client's real material; if warm/serif is right, change at least two of ground, face class and accent |
| Near-black ground + one acid green / vermilion / neon accent, glow edges | active | 2025 | dark only via the scene sentence; accent from the brand; no glow |
| Saturated indigo/violet (#6366F1, #4F46E5, #8B5CF6, #7C3AED, #A855F7…), purple→blue/pink/cyan gradients, gradient text | active | 2024 | per-client OKLCH palette; violet only with `brand-source:`; low-chroma plum/aubergine from the client's world is fine |
| Stock #111 / #0f0f0f / #fafafa as black and white | active | 2025 | ink L 0.18-0.26 tinted to brand hue; paper from the client's material |
| Glassmorphism, grain overlays, aurora / spotlight / lamp / beam backgrounds, glows | active | 2024 | flat by default; texture only from real material or a named signature |
| Stock framework palettes (#2563EB blue, slate + safety orange #EA580C for every trade) | active | 2024 | brand or material colour on a custom 12-step scale; stock scales only for greys and semantics |
| Broadsheet kit: hairlines + zero radius + small tracked mono labels + italic display serif | active | 2025 | only for genuinely editorial clients; otherwise one structural device that carries information |
| Weights 100 vs 900 and 3× size jumps as the "bold" move; oversized h1 over tiny body | active | 2025 | one emphasis device; display capped at 6rem; ratio 1.2-1.333 |
| Overused fonts: Inter, Roboto, Open Sans, Lato, system-ui/Arial, Poppins, Montserrat, Raleway, Space Grotesk, Plus Jakarta Sans, IBM Plex, JetBrains Mono, Playfair Display, Crimson | active | 2024-25 | per-niche pools with licence and `last_used`; reuse limits via niche log |
| Fashionable picks: Fraunces, Newsreader, Instrument Serif/Sans, Bricolage Grotesque, DM Sans/Serif, Outfit, Geist, Cormorant, Lora, Syne | watch | 2025-26 | allowed with a non-category reason + niche-log check |
| Free-foundry picks: Satoshi, Clash Display, General Sans, Cabinet Grotesk | watch | 2025-26 | less-used faces from the same foundries, or Velvetyne display where the niche allows |
| Builder defaults left in place (Elementor default kit fonts/colours, one-prompt generated design systems, theme type scale) | active | 2025 | DESIGN.md tokens pushed as Variables / Global Colours |

## Layout

| Tell | Status | First seen | What replaces it |
|---|---|---|---|
| Hero → features → testimonials → FAQ → CTA skeleton; eyebrow + heading + lede + 3 cards on every section | active | 2024 | content from the niche, order and composition from the direction; neighbours never share a layout |
| Big-stat hero, 3-stat strip, count-up numbers | active | 2024 | one hard fact in the hero (town, service, phone, verified year) |
| Fake 01 / 02 / 03 numbering | active | 2025 | numbers only for real sequences |
| Mirrored zig-zag image/text blocks repeated down the page | active | 2025 | max 2 alternations; asymmetric splits, lists, tables |
| Generic stock hero (sunset, lilies, laptop + latte, handshake) with dark overlay | active | 2023 | the client's real place, work or people in the first viewport |
| `100vh` sections everywhere, every section the same height | active | 2025 | sections size to content; `100svh` on the hero only |

## Components

| Tell | Status | First seen | What replaces it |
|---|---|---|---|
| SaaS card kit: identical rounded cards, one 8-12px radius, rgba(0,0,0,.1) shadow, thin border + wide shadow | active | 2024 | elevation table with a ceiling (often flat + tone); radius language per direction |
| Icon-in-tinted-circle feature grid; check-icon lists everywhere; untouched Lucide/Feather defaults | active | 2024 | functional icons only, one family chosen per site, stroke matched to type |
| Tracked caps eyebrows on every section, "A · B · C" meta lines, hero eyebrow chips | active | 2025 | eyebrows off by default; max 2 per page, only with real information |
| "→" on every button; arrows that slide 3px on hover | active | 2025 | verb + object label; arrow only if it is the site's one hover idea |
| Bento grids, logo/testimonial marquees, shimmer and border-beam buttons, number tickers, globes, particles, 3D tilt cards, magnetic buttons, spotlight cards | active | 2024-25 | banned by default; one bespoke interaction tied to the brand if the direction names it |
| Coloured left-border callout cards; cards inside cards | active | 2025 | spacing and type for grouping; max 2 box levels |
| Auto-rotating 3-dot testimonial carousel; "Most popular" badge; three polished invented testimonials | active | 2023 | real reviews with name, date, source, or no review section |
| Sun/moon theme toggle and "New" pill badges as decoration | active | 2025 | one designed mode unless both are needed |
| Self-opening chat bubble, early popup, back-to-top clutter | active | 2023 | phone and form visible; mobile call bar |

## Imagery

| Tell | Status | First seen | What replaces it |
|---|---|---|---|
| Stock clichés: laptop + latte, handshake, smiling team, call-centre headset, spark-shower welder, sunset over water | active | 2023 | client photos > flagged self-hosted stock > neutral placeholder block |
| Stock people presented as staff, families, customers or reviewers | active | 2023 | never; real named staff photos from the client only |
| Hot-linked placeholder images (Unsplash/picsum/placehold URLs); 3D renders for trades; full-screen stock video backgrounds | active | 2024 | downloaded, optimised, self-hosted, flagged with `data-placeholder` |

## Copy

| Tell | Status | First seen | What replaces it |
|---|---|---|---|
| Slop words: delve, elevate, unlock, seamless, unleash, cutting-edge, robust, bespoke, streamline, empower, world-class, game-changer, next-gen, tapestry, nestled, journey (metaphor) | active | 2023 | plain words from the customer's view |
| Cadences: "X. No Y." runs, "not X, but Y", two-fragment headings, "WORD — fragment" labels, more than one em dash per paragraph | active | 2024 | full sentences; headings with a noun |
| "Get started", "Learn more", "Read more", "Submit"; "Oops!"; exclamation marks in confirmations | active | 2023 | verb + object labels; errors say what happened and how to fix it |
| Invented facts: "500+ happy clients", years, awards, prices | active | 2023 | real data or a labelled placeholder listed under Known gaps |
| Over-corrections: comma splices replacing dashes, calm virtue words ("thoughtful", "considered") replacing hype, everything in pairs instead of threes | watch | 2026 | vary rhythm naturally; say the concrete thing |

## Motion

| Tell | Status | First seen | What replaces it |
|---|---|---|---|
| Fade-up on every section (AOS style); staggered page-load reveal on every element | active | 2024 | no section reveals; at most one moment per page (hero counts) |
| Hover lift / zoom / glow on every card; hover not gated to fine pointers | active | 2024 | colour/underline/border states, gated by `(hover:hover) and (pointer:fine)`; one hover-motion idea moving a child |
| Smooth-scroll libraries and parallax on local-business sites; Elementor entrance animations on every widget | active | 2024 | native scroll; Elementor entrance animations off globally |
| Count-up numbers, pulsing badges, glowing borders, per-letter text-generate effects, infinite decorative loops | active | 2024 | none; motion must name its purpose |

## Stale advice (do not follow)

| Advice | Status |
|---|---|
| Category → palette/font mappings (one niche always gets one look), "AI = indigo" | retired advice |
| 2025-era "frontend aesthetics" tips: extreme weight contrast, gradient atmosphere, staggered load reveals, Google Fonts CDN loading, Space Grotesk as the fresh choice | retired advice |
| "Fresh font" shortlists from 2025 (Fraunces, Instrument Serif, Bricolage) | retired advice (now `watch` fonts) |
| Fixed section heights, hidden contact details, `.example` emails, "no testimonials ever" | retired advice (wrong for local SEO) |

## Changelog

- 2026-11-18 - v2026-11 seeded from the Bexven master sheet §12 and conflicts Part 3.
