# 06 — Open Design (OpenDesign)
https://github.com/nexu-io/open-design · Desktop/web app + daemon + bundled skill/design-system library · Apache-2.0 (some vendored skills keep MIT/other upstream licenses) · ~108.3k stars · commit 0725880, 2026-11-18

## 1. What it is
A local-first "AI design agent workspace": an Electron/Next.js app plus a Node daemon (`od` CLI) that detects a coding-agent CLI you already have (Claude Code, Codex, Cursor...), feeds it a skill + a design system + craft rules, and streams single-file HTML artifacts into a sandboxed preview with comment mode. The repo also ships the content library: ~170 skills, ~70 design templates, 151 design-system packages and 12 "craft" rulebooks. There is a paid cloud tier (open-design.ai).

## 2. How it works
- Four content axes, each a folder of Markdown:
  - `skills/` = functional capabilities (brief, audit, brand-extract, imagegen...). SKILL.md + optional assets/references.
  - `design-templates/` = artifact shapes (saas-landing, pricing-page, waitlist-page, dashboard, decks, critique...). Same SKILL.md format plus `example.html`.
  - `design-systems/<slug>/` = brand package: `manifest.json`, `DESIGN.md` (prose: theme, palette roles, type, components, layout, elevation, do/don't, responsive, "Agent Prompt Guide"), `tokens.css` (fixed semantic vars: `--bg --surface --fg --muted --border --accent --font-display --text-* --space-* --radius-* --elev-* --motion-*`), often also `design-tokens.json`, `tailwind-v4.css`, `components.html`, preview.
  - `craft/` = brand-agnostic rulebooks (typography, typography-hierarchy, color, anti-ai-slop, animation-discipline, accessibility-baseline, state-coverage, form-validation, laws-of-ux, rtl-and-bidi).
- Skill front-matter has an `od:` block: `mode`, `scenario`, `design_system.requires`, `craft.requires: [typography, color, anti-ai-slop]`, typed `inputs`/`parameters` (sliders), `upstream`.
- Prompt assembly order (docs/skills-protocol.md): DESIGN.md body -> requested craft files -> skill body. Brand tokens win over craft; craft fills the gaps. Only requested craft files are injected (token cost control).
- After generation, `apps/daemon/src/lint-artifact.ts` (regex/CSS-parse linter, ~1000 lines TS) scans the HTML and sends P0/P1/P2 findings back to the agent as a system reminder, so it self-corrects.
- Every editable element gets `data-od-id` so the UI's comment mode can target it.
- Many skills are vendored or stubbed from other repos: `frontend-design` (Anthropic), `taste-skill`/`redesign-skill`/`minimalist-skill` (Leonxlnx/taste-skill, MIT), `impeccable-design-polish` (pbakaus/impeccable), `web-design-guidelines` (Vercel), `critique` (alchaincyf/huashu-design), `plan-design-review`/`design-review` (garrytan/gstack — only catalogue stubs pointing upstream). Craft color/type/anti-slop files are adapted from referodesign/refero_skill (MIT).

## 3. Rules
- [process] Load three layers in order: brand file (palette/fonts) -> universal craft rules -> page-type workflow; brand values override craft defaults
- [process] Before code, state a one-line design read: page kind, audience, vibe, aesthetic family (from taste-skill)
- [process] Ask at most one clarifying question, only when two plausible directions really diverge; otherwise declare and proceed
- [process] Pick one named direction and keep every micro-decision (labels, spacing, accent, serif/mono roles) in that register
- [brand] Every colour and font comes from the project token file; no new hex values in components (linter flags >12 raw hex outside `:root`)
- [code] Name tokens by role (`--accent`, `--success`), never by hue (`--blue-500`)
- [colour] Palette shares: neutrals 70–90%, one accent 5–10%, semantic 0–5%, effects <1%
- [colour] Exactly one accent; never invent a second one
- [colour] At most 2 visible accent uses per screen (e.g. one label + one primary CTA); links and focus rings count
- [colour] Avoid pure #000/#fff; use about #0f0f0f / #fafafa backgrounds and #111 / #f0f0f0 text
- [colour] On dark surfaces use thin semi-transparent white borders (~8% alpha) rather than solid dark borders
- [colour] If the brand colour fails contrast for text, use a darker shade for text and keep the bright one for fills
- [colour] Gradients only to separate hierarchy, never to decorate empty space; no two-stop hero gradients
- [a11y] Contrast gates: body 4.5:1, large text 3:1, UI components vs adjacent surface 3:1
- [type] Multiplicative scale (1.2 or 1.25), 6–8 sizes per page, no more than 3 sizes above the fold
- [type] Leading: display 1.0–1.2, body 1.5–1.6, small 1.5
- [type] ALL CAPS always gets +0.06 to +0.1em tracking; headings 32px+ get −0.01 to −0.02em; display 48px+ −0.02 to −0.03em
- [type] Small text 11–13px gets slightly positive tracking (+0.01–0.02em); buttons/labels +0.02em
- [type] Max 2 typefaces; always a real fallback chain; never `system-ui` alone on headings
- [type] Body measure 50–75 characters (`max-width: 65ch`); never justify body text
- [type] Three-weight system (~400 read / ~500 emphasise / ~600 announce); 700+ rarely needed
- [type] Use `text-wrap: balance`/`pretty` to kill orphans; tabular figures for numbers in data
- [layout] Do not ship the unvaried Hero -> Features -> Pricing -> FAQ -> CTA skeleton; add at least one unconventional section (full-bleed quote wall, comparison vs status quo, inline mini demo)
- [layout] Replace three equal feature cards with zig-zag, asymmetric grid, horizontal scroll or masonry
- [layout] Alternate density (one tight section, one breathing section) instead of perfect symmetry
- [layout] Hero content top-biased, not vertically centred (warm-editorial system); use `min-height: 100dvh`, not `100vh`
- [layout] Align shared elements across side-by-side cards (titles, prices, feature lists, buttons pinned to bottom)
- [space] Bottom padding often needs to be slightly larger than top; adjust optically, not mathematically
- [components] Cards only when elevation means hierarchy; never a rounded card with a coloured left border
- [components] Vary radius: tighter on inner elements, softer on containers
- [icon] No emoji as icons; one consistent monoline SVG set (~1.6–1.8px stroke, `currentColor`); avoid cliché metaphors (rocket = launch)
- [copy] No invented metrics ("10x faster", "99.9% uptime"); use real data or a clearly labelled placeholder
- [copy] No filler or lorem; an empty section is a composition problem, not a word-count problem
- [copy] Ban list: elevate, seamless, unleash, next-gen, game-changer, delve, tapestry; specific verbs on buttons ("Start tracking" > "Get started")
- [copy] Sentence-case headings, no exclamation marks in success messages, no "Oops!"
- [image] No hot-linked placeholder CDNs (Unsplash, placehold.co, picsum); use a local placeholder block
- [motion] Animate only movement through space/time/state (navigation, expansion, progress, feedback), not to decorate or signal "premium"
- [motion] Durations: 50–100ms press/hover, 150ms default confirmation, 200–300ms entering UI, 300–500ms cross-screen; frequent hovers <=200ms; mobile 20–30% shorter
- [motion] Animate `transform`/`opacity` only; always provide a reduced-motion fallback
- [brand] Aim for ~80% proven patterns + ~20% distinctive choice: one bold visual move, specific voice, one memorable micro-interaction, one insider detail
- [qa] "Soul test": a stranger seeing a screenshot should be able to tell which business it is; if not, it is a template
- [qa] Lint the output for P0 tells after every generation and feed findings back for a fix pass
- [qa] Critique on 5 dimensions scored 0–10 (direction consistency, hierarchy, detail, functionality, innovation), evidence per score citing classes/elements, score = worst sustained band, no grade inflation; output Keep / Fix / Quick-wins
- [qa] Check at 1440 / 768 / 375 widths; landing CTA above the fold, phone number tappable on mobile
- [process] Redesign fix order: font swap -> palette cleanup -> hover/active states -> layout/spacing -> replace generic components -> loading/empty/error states -> type polish
- [seo] Always ship title, meta description, og:image, favicon, skip link, legal links, custom 404

## 4. AI tells / anti-patterns it bans
P0 (auto-linted): hard-coded Tailwind indigo/violet accents (#6366f1, #4f46e5, #4338ca, #3730a3, #8b5cf6, #7c3aed, #a855f7); purple->blue / blue->cyan / indigo->pink hero gradients; emoji icons in headings/buttons/lists; sans display font when the system binds a serif; rounded card + coloured left border; invented metric phrasing; lorem/"feature one"; `scrollIntoView`. P1: ALL CAPS without tracking; external placeholder image URLs; >12 raw hex outside `:root`; accent used 6+ times. Guidance: Hero-Features-Pricing-FAQ-CTA skeleton; blob/wave SVG backgrounds; perfect symmetry; 3 equal feature cards; centred hero over dark mesh; glassmorphism everywhere; infinite micro-animations; Inter + slate-900; Lucide/Feather-only icons; pill "New" badges; accordion FAQ; 3-dot testimonial carousel; 4-column footer link farm; sun/moon toggle; "John Doe", "Acme", round fake numbers; a single random dark section in a light page.

## 5. Data, assets and scripts it ships (and what they need: Node, Python, Chrome)
- Full app: Node 24 + pnpm 10.33, Next.js web, Electron desktop, better-sqlite3, daemon `od` CLI with MCP installers for 20+ agents; browser sessions/media use Chromium (daemon `browser-sessions.ts`). Docker option. We do not need any of it.
- Pure-Markdown/CSS (no runtime needed, reusable as data): `craft/*.md` (~1,950 lines), 151 `design-systems/*/DESIGN.md` + `tokens.css` (+ `tailwind-v4.css`, `components.html`), design-template SKILL.md + `example.html` (saas-landing, pricing-page, waitlist-page, web-prototype variants, critique).
- `apps/daemon/src/lint-artifact.ts`: TypeScript, needs Node (tsx) — but its rule list is simple enough to re-implement as a small Python checker over our HTML.
- Some skills (fal-*, venice-*, imagegen) need paid API keys; several "skills" are only stubs linking upstream.

## 6. Area
design (primary) · QA (linter + critique) · tooling (app, out of scope)

## 7. Take / skip
Take:
- The layered architecture: per-client brand file (DESIGN.md + tokens.css with a fixed semantic token contract) + universal craft rules + page-type workflow. Map it to Bexven: one DESIGN.md/tokens.css per client built at outreach time, reused unchanged for the WordPress/Elementor build (tokens -> Elementor global colours/fonts).
- `craft/anti-ai-slop.md`, `typography.md`, `color.md`, `animation-discipline.md` numbers almost verbatim as our rulebook (re-worded; Apache/MIT allow it, keep attribution to refero_skill).
- The post-generation linter idea: write our own Python checker (indigo hexes, two-stop gradients, emoji icons, invented metrics, lorem, caps tracking, raw-hex count, accent count, external placeholder images) and run it before every Vercel deploy.
- The 5-dimension critique with evidence + "worst sustained band" + Keep/Fix/Quick-wins as our QA step.
- The DESIGN.md section skeleton (theme, colour roles, type, components, layout, elevation, do/don't, responsive, agent guide) as our client brand-file template.
- Taste-skill's "design read" line and the 80/20 soul rule — directly useful for making same-niche sites differ.
Skip:
- The app, daemon, MCP installers, cloud — irrelevant to a Claude Code skill.
- Brand-clone systems (Stripe, Apple, Nike, Tesla...): trademark-flavoured, not for client work.
- The auto-generated style systems (cafe, brutalism, luxury): thin, generic ("Token from style foundations"), Poppins-everywhere, and DESIGN.md often contradicts tokens.css (cafe: Poppins/#5D4432 in prose vs Georgia+Inter/#9b5b32 in tokens). Only hand-written ones like warm-editorial are good references.
- The saas-landing template's fixed section order — it contradicts the repo's own anti-slop rule.
- Redesign-skill extras that are themselves trendy tells (grain everywhere, spotlight borders, glassmorphism, parallax stacks, "Geist/Satoshi/Outfit" as the default replacement font).

## 8. Open questions
- Internal conflicts to resolve in our skill: (a) anti-slop bans purple, yet the Stripe system is "signature purple gradients" (#533afd is not on the lint list); (b) craft says ALL CAPS labels are fine with tracking, redesign-skill says avoid all-caps subheaders; (c) warm-editorial bans sentence-case H1/H2 while redesign-skill demands sentence case; (d) taste-skill makes dark mode mandatory for consumer pages, redesign-skill warns against stray dark sections; (e) redesign-skill wants hover scale on every button and texture/grain, craft's animation-discipline says don't animate to signal "premium".
- warm-editorial itself is the "cream + serif + terracotta" look that other sources call an AI tell — use as structure reference, not as a default palette.
- Star count from README banner says 100K; GitHub page showed ~108.3k.
- SUGGESTED: refero_skill - https://github.com/referodesign/refero_skill - original source of the craft/anti-slop rules (MIT)
- SUGGESTED: huashu-design - https://github.com/alchaincyf/huashu-design - origin of the 5-dimension critique flow
- SUGGESTED: gstack (plan-design-review) - https://github.com/garrytan/gstack - 0–10 per-dimension design gate with AI-slop flags
