# 05 — Impeccable
https://github.com/pbakaus/impeccable · Claude Code plugin / multi-harness skill + Rust CLI ("engine") · Apache-2.0 (iOS/Android refs distilled from MIT ehmo/platform-design-skills, see NOTICE.md) · ~112.6k stars (GitHub page via WebFetch, 2026-11-18) · commit d41d986, 2026-11-16, skill v4.9.2

## 1. What it is
One user-invocable skill (`/impeccable`) with 24 sub-commands (shape, critique, audit, polish, bolder, quieter, typeset, colorize, layout, animate, etc.), a shared "craft floor", and a Rust binary that runs context loading, a 62-rule anti-pattern detector, a "concept-seed" dice roll that assigns design directions, a local decision page, and critique snapshots. Its goal is "out-of-distribution craft": commit to a design world built for the product, not the category default.

## 2. How it works
- **Setup:** `impeccable context` loads PRODUCT.md (product truth: users, purpose, platform), DESIGN.md (durable visual system plus `.impeccable/design.json` tokens) and a per-surface brief (`.impeccable/surfaces/`). If PRODUCT.md is missing, `init` interviews the user first. craft-floor.md must be read right before any UI edit.
- **Modes, chosen per surface:** Persuade (landing, marketing, pricing: bold, full commitment), Operate (app/dashboard: precision, restraint, familiar patterns), Read (docs/articles: calm column, frame carries the brand), Experience (portfolio/gallery: the work leads). A tool's landing page is Persuade even if the product is Operate.
- **Refine vs redesign (core rule):** refinement keeps the existing identity, copy and behaviour. Redesign keeps product truth, content and function but treats the old look as evidence and anti-reference, then replaces it entirely. "Never split the difference" by polishing a look you have discarded.
- **New-work workflow (new-work.md):**
  1. Decide what is already true: redesign / established world (inherit it, even with no DESIGN.md) / incomplete brand (expand) / seeded world / no visual authority (create).
  2. Ask 2–3 *product* questions per mode (Persuade: who must act, what must they believe, what proof exists). Never ask for CSS values or offer canned aesthetic lanes. Never propose a look before the roll, because the answer will just confirm it.
  3. Scale the invention: extending a surface means inheriting it, no tournament. A whole new surface in an existing world means listing 5–7 structurally different layouts; the script deals 3 at random and the user locks one. For a new or replacement world (new-work-world.md): name the product's unique mechanism, the audience's real scene and cultural home. Name "the page this category always ships" and its predictable opposite (both are the rut). List 7 concrete visual systems/artifacts/rituals from the audience's culture spanning at least 3 material families (max 1 candidate from the literal brief metaphor, max 1 from the audience's tools on Persuade). Build full directions, then run `concept-seed`. The dice assign the lead direction and deal catalog "challengers" (paid server catalog), each judged on audience identification and product clarity (wins/competitive/declined). A declined challenger still "donates" one discipline (e.g. palette commitment), never its surface styling. Present: the assigned direction, max 3 challengers, one "IMPECCABLE'S PICK" card, re-roll (plain/safer/bolder), plus a quiet "standing exit", the category standard done straight, which is never recommended.
  4. Commit the world: choose a colour strategy (Restrained / Committed 30–60% one colour / Full palette 3–4 roles / Drenched), decide light vs dark from a written physical scene, pick fonts like objects from the subject's world.
  5. Record a ~150-word "Direction contract" in the surface brief: THESIS, OWN-WORLD, STORY, FIRST VIEWPORT, FORM (+seed reference), FINISH. Never put it in shipped code.
  6. Build fully committed. Comp-led (generate an image comp, then a measured spec plus comp-diff) is the default for Persuade/Experience when image generation exists. Code-led is forced for Operate/Read (their blind evals: comps of working screens scored 2.0–2.9 vs code-led 3–3.5).
  7. Inspect desktop+mobile in batched screenshots (max 2 rounds), run `detect`, then spawn a fresh `impeccable-finish-reviewer` subagent with no conversation history. It returns one of exactly four verdicts: recapture / rebuild / fix / ship. Then `impeccable-documenter` writes DESIGN.md *from the built result*, not before the build.
- **Polish workflow (polish.md):** refinement only, never a concealed redesign; if the concept is wrong say so and recommend redesign/bolder. Establish the system and classify each drift (missing token / one-off implementation / conceptual mismatch / local defect) → gather evidence at real sizes (reads the latest critique snapshot as backlog) → triage in order: broken tasks/data loss/inaccessible > missing states > flow/hierarchy/responsive drift > visual/motion > code cleanup → polish the whole path → verify (mouse, keyboard, touch, all states, zoom) → clean the diff → close the critique snapshot.
- **Critique (critique.md + critique-rubric.md):** two isolated subagents. A = design review (rubric), B = detector plus browser overlay. A must finish before detector output is seen, so the tool cannot anchor the judgement. Without subagents the report opens with a "DEGRADED" banner. Report order: header provenance → **Design Health Score**: Nielsen's 10 heuristics, each 0–4, total /40 (7 and 10 may be n/a on Persuade/Experience, then renormalize: e.g. 24/32). Bands: 36–40 Excellent, 28–35 Good, 20–27 Acceptable, 12–19 Poor, 0–11 Critical (or by % 90/70/50/30). "Most real interfaces score 20–32" → **Design Specificity Verdict** first ("authored for this product or category-interchangeable?") → overall impression → 2–3 what's working → 3–5 priority issues tagged P0 blocking / P1 major / P2 minor / P3 polish (tie-break: "would a user contact support?" → at least P1), each with fix + suggested command → persona red flags → minor observations → provocative questions. It then asks 2–4 targeted questions with concrete options (mandatory if 3+ issues), and recommends commands ending with polish. Cognitive-load checklist (8 items; 0–1 fails good, 2–3 moderate, 4+ critical; ≤4 options per decision point). Five personas: Alex power user, Jordan first-timer, Sam accessibility, Riley stress tester, Casey distracted mobile. Landing pages use Jordan, Riley, Casey. Snapshots are persisted with a score trend line.

## 3. Rules
- [process] Choose the mode from the surface (Persuade/Operate/Read/Experience) and scale ambition to it: bold on marketing pages, restrained precision on app UI
- [process] The brief wins: honour pinned fonts/palettes/eras even if they match a known AI tell; redirecting a clear brief toward your own taste is failure
- [process] Redesign = replace the old look entirely (keep content/function); refinement = keep identity; never polish a look you have decided to discard
- [process] Before inventing, write: the product's unique mechanism, audience scene, cultural home, "the page this category always ships" and its opposite (both banned as defaults)
- [process] Derive 7 visual-world candidates from the audience's culture (artifacts, publications, places, rituals, pre-web form), spanning at least 3 material families; at most 1 from the literal brief metaphor
- [process] Ask only product questions before proposing a direction; never offer aesthetic lanes or ask for CSS values
- [process] Write a short direction contract (thesis, own-world palette+components, story, exact first viewport, form, finish) before code; a block that reads like a mood means the direction isn't decided
- [process] Write DESIGN.md after the build, from what shipped, not as a rulebook up front
- [qa] Review with a fresh agent that never saw the build conversation; give it screenshots, the request and the contract; verdict ∈ recapture/rebuild/fix/ship; max 2 fix rounds
- [qa] Validate captures before review: settle entrance animations, full-page from the top, no blank regions
- [qa] Inspect desktop + mobile (+ user's real viewport) and drive every state (hover, focus, error, empty, overlong content) in one batched round
- [colour] Pick a colour strategy first (Restrained / Committed / Full palette / Drenched); colour commits at page scale (fields owning whole regions), not scattered accents
- [colour] Light vs dark is never a default nor picked by category: write one sentence of physical scene (who, where, under what ambient light) and let it decide
- [colour] On coloured surfaces tint secondary text from the hue; never plain grey. Dark mode is designed, not inverted
- [colour] Prefer OKLCH for new palettes; choose hue from product meaning, never from category association
- [type] Persuade surfaces need faces with a point of view; treat Fraunces, Playfair, Cormorant, Lora, Crimson, Newsreader, Syne, Space Grotesk/Mono, IBM Plex, Inter-as-display, DM Sans/Serif, Outfit, Plus Jakarta, Instrument Sans as "stopped looking" defaults needing a non-subject reason
- [type] Subject associations (books → serif, tech → mono) are exactly what to break
- [type] Body measure 65–75ch, body ≥16px, display ≤6rem, tracking floor -0.04em, balanced headings, more space above a heading than below
- [type] Never use a system/installed display face (Arial Black, Impact) as an own-world display voice; source and self-host
- [type] Light text on dark: a bit more line-height, tracking and weight
- [type] Operate UIs: one family is often enough, fixed rem scale, ratio 1.125–1.2
- [layout] No same-size icon+heading+text card grids as page structure; never nest cards
- [layout] No hero-metric template (big number, small label, stats row)
- [layout] No section numbers 01/02/03 unless the sequence is real information
- [layout] First viewport is a thesis: demonstrate the product's mechanism at real scale; the "memory test" = what would a visitor describe an hour later?
- [layout] Pace the scroll: vary density, scale, image and quiet within one grammar; end on a real close
- [components] Eyebrow/kicker label above a heading is an absolute ban that no brief can earn back; delete it and let the heading work
- [components] No coloured border-left/right >1px on cards/callouts; no gradient text; no decorative glass; no hard offset shadows unless the world is truly neobrutalist
- [components] Every control: default, hover, focus, active, disabled, loading, error, empty; skeletons not spinners; empty states teach
- [components] No modal unless the task needs interruption or protected focus
- [components] Theme browser surfaces: selection, caret, scrollbars, focus rings, underline offset, tabular numerals ("cheapest signal a page was built, not assembled")
- [icon] Real icon library or authored SVG in one stroke/weight; no emoji/unicode as icons
- [image] Use real verified photos of the subject's physical object, not the category; one decisive photo beats five mediocre ones
- [image] No geometric masks faking organic cut-outs; use a real alpha matte
- [image] Author demo content at full fidelity and label it synthetic; never invent prices, customers, benchmarks
- [motion] One authored motion moment per page, not identical entrances on every section; exponential ease-out from an already-visible default
- [motion] Durations: 100–150ms feedback, 150–300 state, 300–500 overlays, 500–800 one focal entrance; exit faster than enter; no bounce/elastic by reflex
- [motion] Hover never moves the element itself or neighbours; animate a child (avoids edge flicker)
- [motion] Operate UIs: 150–250ms, motion only for state, no orchestrated page-load sequences
- [copy] Product's own language; buttons name the action; errors name problem + recovery; no buzzwords (streamline, empower, world-class), no "X. No Y." aphorism cadence, no em-dash saturation
- [a11y] Contrast: body 4.5:1, large 3:1; touch targets 44px; a11y is checked in the audit command, kept out of design-time prompts on purpose (they found reminders made output timid)
- [brand] Never use militarist/hate-movement emblems as decoration even when the subject's world contains them
- [tooling] Run a deterministic detector on edited files and fix mechanical findings before human-style review

## 4. AI tells / anti-patterns it bans
The calibration in new-work.md names four clusters AI lands in regardless of subject: (1) warm cream ground + high-contrast serif display + terracotta/signal-red accent; (2) near-black + one neon accent + glowing edges; (3) broadsheet editorial hairlines + italic display serif + small tracked mono labels; (4) flat saturated ink + black boxes + hard offset shadows + condensed display (neobrutalism). They are legitimate only if the brief asks. Self-test: "if someone could guess your aesthetic from the category alone, or from category-plus-avoidance, rework". It explicitly calls out its own model prior: warm/bookish/family/child subjects default to cream + italic serif + lamplight, so "treat that first palette as already spent".
Detector (62 rules) includes: side-tab, border-accent-on-rounded, overused-font (Inter, Roboto, Fraunces, Geist, Plus Jakarta, Space Grotesk), gradient-text, ai-color-palette (purple/violet gradients, cyan-on-dark), cream-palette, nested-cards, monotonous-spacing, bounce-easing, pulsing-dot, blinking-cursor, hard-offset-shadow, dark-glow, radial-halo/spotlight, marquee, icon-tile-stack (rounded icon square above heading), italic-serif-display, hero-eyebrow-chip, kicker-above-heading, numbered-section-labels, em-dash-overuse, marketing-buzzword, aphoristic-cadence, theater-slop-phrase, oversized-h1, extreme-negative-tracking, gpt-thin-border-wide-shadow (whole row of hairline border + wide shadow), codex-grid-background, repeating-stripes-gradient, plus craft checks (gray-on-color, low-contrast, line-length, tight-leading, justified-text, straggler, tiny-text, all-caps-body, skipped-heading, design-system font/colour/radius drift).
Operate-specific: strangeness without purpose (over-decorated buttons, display fonts in labels, reinvented affordances), "monospace as a costume for technical", sparklines/progress rings as filler.

## 5. Data, assets and scripts it ships (and what they need: Node, Python, Chrome)
- `scripts/impeccable` POSIX launcher (+ .cmd) that runs a prebuilt Rust binary, **downloaded on first run** from GitHub releases (checksummed; not in git). No Node needed for the skill itself. Verbs: context, detect, concept-seed, serve-question (local decision web page), critique-storage, comp-diff, build-phase, surface-brief, embed-prompt, live, hook, doctor, pin, foundations.
- `concept-seed` calls impeccable.style's roll API for catalog worlds (a **paid/private catalog**, "the moat"), sends telemetry (opt-out via DO_NOT_TRACK).
- Plugin hooks: SessionStart + PostToolUse(Edit|Write) run the detector after every UI edit.
- 5 subagents: asset-producer, documenter, finish-reviewer, manual-edit-applier, motion-reviewer.
- Live mode: in-browser JS (live-browser.js, 13.9k lines) to pick elements and iterate variants; needs a dev server + browser. The critique overlay needs browser automation. `npx impeccable detect` is also available as an npm CLI.
- Uses image generation for comps when available.
- Commands besides the core: shape (discovery interview → brief), init (PRODUCT.md), document (DESIGN.md + tokens), extract (tokens/components), audit (a11y/perf/theming/responsive/implementation integrity, scored), bolder, quieter, distill, harden (overflow, i18n, edge cases), onboard, animate, colorize, typeset, layout, delight, overdrive (WebGL/scroll/cinematic), clarify (UX copy), adapt (responsive/print/email), optimize (Core Web Vitals: LCP<2.5s, INP<200ms, CLS<0.1), live, generate.

## 6. Area
design (primary), QA (critique/audit/detector), process/tooling

## 7. Take / skip
Take:
- The surface **mode** split (Persuade for our redesign homepages; Operate rules only for client dashboards). It tells the skill when to be bold vs familiar.
- The **anti-rut derivation**: name the category default page and its opposite, then derive 7 worlds from the client's niche culture (e.g. funeral home: memorial stationery, chapel signage, order-of-service cards…) across ≥3 material families. This is exactly what makes two funeral-home sites differ. Add a cheap random pick among strong candidates (our own dice, no paid API).
- The direction contract (THESIS / OWN-WORLD / FIRST VIEWPORT …) saved per client; useful when the Vercel mock is rebuilt in Elementor.
- The craft-floor bans (eyebrow ban, cards, gradient text, side-border, hero-metric, emoji icons, browser-surface theming) and the 4 named AI-look clusters with the "guessable from category" self-test. The font blacklist.
- Light/dark from the physical use scene.
- Fresh-context reviewer with fixed verdict words and a 2-round cap. The critique format (specificity verdict first, Nielsen /40, P0–P3, personas Jordan/Riley/Casey for landing pages) for client QA reports.
- Polish triage order and the "polish ≠ concealed redesign" rule.
- Motion durations + hover-on-child rule; "prove, don't claim" with demo content marked synthetic and no invented claims (important for cold outreach mocks).
Skip:
- The Rust binary, auto-download, telemetry, paid catalog roll API, live-mode browser JS, decision-page server: too heavy, a network dependency, and against our no-install rule. Reproduce the logic in prose plus a simple local random choice.
- Comp-led image-generation pipeline and comp-diff: overkill for a cold-outreach homepage. Code-led with a written first-viewport contract is enough.
- Native iOS/Android references, the doctor/foundations/pin tooling, PRODUCT.md schema stamps.
- The "IMPECCABLE'S PICK / challenger / donation" tournament ceremony: keep only "assigned + 2 alternates + safe standard option".

## 8. Open questions
- The eyebrow ban is absolute here ("no brief earns it back"), while many design guides (and some agency templates) use eyebrows freely. Bexven needs to choose a position; the Elementor kits we use may ship eyebrow widgets by default.
- The font blacklist bans fonts that other resources recommend (Fraunces, Space Grotesk, DM Sans, Inter). Decide if we adopt it whole or only for Persuade pages.
- The Operate guidance accepts system fonts and familiar patterns; check this against the "no generic fonts" goal for client admin areas (probably irrelevant for WP sites).
- The star count (~112.6k) came from one WebFetch; verify it if it matters.
- Catalog worlds are private (impeccable.style), so we cannot see what the challengers look like; the local tests/fixtures/concept-catalog might show the schema (not read).
- SUGGESTED: ehmo/platform-design-skills - https://github.com/ehmo/platform-design-skills - MIT source of the iOS/Android guidance; low priority for web-only Bexven.
