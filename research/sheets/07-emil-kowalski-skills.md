# 07 — Emil Kowalski skills
https://github.com/emilkowalski/skills · Skill repo (21 Claude/agent skills + 2 cheat sheets) · MIT (c) 2026 Emil Kowalski · 57.9k stars (WebFetch, 2026-11-18) · commit 64eb3de, 2026-11-15

## 1. What it is
A set of opinionated skills from the author of Sonner/Vaul (ex-Vercel, Linear), mostly about motion: when to animate, curves, durations, choreography, gestures, performance, reduced motion. Also covers mobile-web polish (mobile-native), worst-case data testing (break-ui), divergent prototyping (prototype), turning user corrections into DESIGN.md rules (learn-taste), a curated library list, Sonner docs, React Native/Expo motion and a Swift guide (off-topic for us).

## 2. How it works
- Every skill is plain SKILL.md (+ reference files like RECIPES.md, STANDARDS.md, AUDIT.md, CATALOG.md). Nothing to run. Each opens with a fixed one-line greeting, then waits.
- One shared rule core, repeated across skills: **frequency gate → named purpose → cheapest tool → transform/opacity → curve + duration (or spring) → interruption/exit → reduced motion + hover gating**.
- Skills split by job: `animate` (build one), `choreograph` (several elements), `gestures`, `review-animations` (strict diff review, Block/Approve), `improve-animations` (read-only audit → self-contained plan files for cheaper agents), `find-animation-opportunities` (max 5–7 ideas, must list rejected ones), `remove-animations` (subtract only, with "removal hazards"), `animation-performance` (diagnose by symptom table).
- Outputs are forced formats: Before/After/Why tables, timelines (element/role/start/duration), and REQUIRED "rejected/kept" sections so the agent shows restraint.
- `ask-emil` routes: prototype → pick library → build → break-ui / review / mobile-native → learn-taste.

## 3. Rules
- [motion] Gate by frequency first: 100+/day (keyboard shortcuts, command palette, core nav) = no animation; tens/day (hover, list nav) = near-invisible or none; occasional (modals, drawers, toasts) = standard; rare/first-time = the only place for "delight"
- [motion] Never animate keyboard-triggered actions
- [motion] Each animation must name its purpose: feedback, spatial consistency, state indication, preventing a jarring change, explanation (marketing/onboarding only), delight (rare only). "Looks cool" = cut it
- [motion] Don't animate data people read or act on (charts redrawing on mount, numbers counting up on load); only animate a real value change
- [motion] Easing: enter/exit = ease-out; moving on screen = ease-in-out; hover/colour = ease; constant motion/progress = linear; default = ease-out. Never ease-in on UI
- [motion] Built-in CSS curves are too weak; use tokens: `--ease-out: cubic-bezier(0.23,1,0.32,1)`, `--ease-in-out: cubic-bezier(0.77,0,0.175,1)`, `--ease-drawer: cubic-bezier(0.32,0.72,0,1)`; no hand-invented curves (take from easing.dev / easings.co)
- [motion] Durations: press 100–160ms; tooltip/small popover 125–200ms; dropdown/select 150–250ms; modal/drawer 200–500ms; marketing/explanatory may be longer. UI stays under 300ms except modals, drawers, sheets, toasts
- [motion] Exit faster than enter (e.g. 250 in / 200 out, native toast ~20% faster out); exits are simultaneous, never reverse-staggered
- [motion] Slow where the user decides, fast where the system answers (hold-to-confirm: 2s linear fill, 200ms ease-out snap-back)
- [motion] Never start from scale(0); use scale(0.9–0.97) + opacity 0
- [motion] Popovers/dropdowns/tooltips scale from their trigger (transform-origin); modals stay centred
- [motion] Press feedback on every pressable: `:active { transform: scale(0.97) }` (range 0.95–0.98), 160ms ease-out
- [motion] Tooltips: delay the first one; once one is open, neighbours open instantly with no animation
- [motion] Use CSS transitions (retargetable), not @keyframes, for anything triggered rapidly (toasts, toggles); springs for gestures
- [motion] Springs: Motion `{type:"spring", duration:0.5, bounce:0.2}`; bounce 0.1–0.3 and only after a drag/flick (force applied); button-closed = zero bounce. Apple default = critically damped (no overshoot)
- [motion] Exit the way it entered (toast in from bottom leaves through bottom; swipe-dismiss on same axis)
- [motion] Stagger 30–80ms between items, total ≲300ms in product UI; for long lists stagger only the first ~5. Marketing hero may use 100–150ms steps on 0.5–0.6s entrances
- [motion] Uniform stagger is forbidden: vary delay/distance by importance (lead moves most, support less, decoration fades only, containers static); shrinking gaps read as a wave
- [motion] One entrance per container: never animate a panel's entrance AND stagger its children
- [motion] Choreography never blocks clicks; everything visible is clickable
- [motion] Scroll reveals: marketing surfaces only, fire once (`once: true`, margin -100px); fade-in on every section is a defect even on marketing pages; one hero entrance is fine
- [motion] Infinite loops (pulsing badges, glowing borders, gradient orbs, decorative spinners) on persistent elements: run once or remove
- [motion] No spinner/skeleton for things that load in <300ms (the flash reads as a glitch)
- [motion] Idle "attention" loops: first run after ~2.5s, repeat rarely (~6s gap), stop while user interacts
- [motion] Direction follows mental model: forward = content moves left; back = right
- [motion] Match motion to brand personality: playful may bounce, a professional/dashboard product stays crisp and fast
- [motion] When a crossfade double-exposes, add `filter: blur(2px)` during the transition (keep blur <20px)
- [motion] Feel-check every animation: play at 2–5x duration / DevTools 10%, frame-by-frame, real phone, look again next day
- [a11y] prefers-reduced-motion = fewer and gentler, not zero: keep opacity/colour, drop translate/scale/parallax/bounce; collapse staggers so the group appears together
- [a11y] Also honour prefers-reduced-transparency (solidify glass) and prefers-contrast: more; avoid full-viewport moving backgrounds and slow ~0.2Hz oscillations
- [a11y] Never disable zoom (`user-scalable=no`, `maximum-scale=1`); fix input font size instead
- [a11y] Touch targets ≥44×44px; enlarge with an invisible ::before hitbox, not a bigger visual
- [nav] Gate every :hover style behind `@media (hover: hover) and (pointer: fine)`; give touch users `:active` instead (touch makes hover stick after tap)
- [nav] Hover effects: reduce scale/lift/shadow-growth hovers to colour/opacity only, ≤150ms; hover-scale on cards that aren't the main action is decoration
- [nav] Touch: hover-only actions (••• on hover) are unreachable on touch; always provide a visible path
- [code] Animate transform and opacity only (clip-path OK; height only for measured accordions); never `transition: all`
- [code] Use `translateY(100%)` percentages (element's own size) over hard-coded px
- [code] `@starting-style` for CSS-only enter animations; WAAPI for programmatic motion without a library
- [code] CSS/WAAPI beat JS rAF while the page is busy (loading/hydrating); drive drags via direct transform writes, never React state or an inherited CSS variable on the parent
- [code] `will-change: transform` only after you see a 1px shift or measured drops; never on `*` or big containers
- [code] Animate `filter: drop-shadow()` instead of box-shadow when a shadow must animate
- [code] Mobile web baseline: `-webkit-tap-highlight-color: transparent`; inputs ≥16px; `touch-action: manipulation` on buttons/links; `user-select:none` on controls only (never body); `100dvh` app shells, `100svh` heroes; `viewport-fit=cover` + `env(safe-area-inset-*)`; `theme-color` per colour scheme; `overscroll-behavior: contain` on inner scrollers
- [code] Carousels: prefer native `scroll-snap-type: x mandatory`; if JS gesture, `touch-action: pan-y`
- [forms] Set `inputmode`, `type=email/tel`, `autocapitalize="none"`, `enterkeyhint` so the phone keyboard fits the field
- [type] Large headings: tighter tracking (~-0.02em) and tight leading; body tracking ~0, max ~65ch; `font-variant-numeric: tabular-nums` for changing numbers
- [copy] Pluralise with Intl.PluralRules ("1 members" is a bug); relative times switch to absolute dates after 7 days; format numbers with Intl.NumberFormat
- [qa] Break-test with realistic worst-case data (long hyphenated/diacritic names, long emails, 1-letter names, 0/1/1,284 counts, German/French expansion, RTL, emoji, missing fields, 404 images) at real width, 320px, widest, 200% zoom, dark mode
- [qa] Common fixes: `flex-shrink:0` on avatars/icons/badges; `min-width:0` on text columns; `overflow-wrap:anywhere` on emails/URLs; never truncate numbers/prices/dates
- [qa] Test touch/hover/viewport behaviour on a real phone; device emulation hides sticky hover, tap delay, vh bugs, input zoom, safe areas
- [process] Prototype 3 (max 5) genuinely different variants, each on a named axis (layout, density, personality, motion, interaction model) — never "Option A/B/C" or variants differing only in accent colour; show one at a time, full size, in real context
- [process] Turn every user correction (explicit, silent edit, repeated nudge, revert) into a class-level rule with its why in DESIGN.md; prefer a lint/check over a sentence; never invent the why
- [components] Don't hand-roll toasts, dialogs, dropdowns, drawers: use accessible primitives (base-ui, Sonner, Vaul, cmdk)

## 4. AI tells / anti-patterns it bans
Ease-in entrances; scale(0) pop-ins; `transition: all`; popovers growing from centre; fade-in-on-scroll on every section (AOS, `whileInView`, `animate-fade-in` utilities); hover-scale/lift on every card; uniform `delay: i * 0.1` staggers; parent slide + child stagger double entrances; animated command palettes; infinite pulse/glow/gradient-orb loops; count-up numbers on load; charts redrawing on mount; spinners/skeletons on fast loads; ungated hover; tap-highlight flash; `maximum-scale=1`; `100vh` heroes; agents "adding motion by default". README also names solid borders where a semi-transparent shadow belongs.

## 5. Data, assets and scripts it ships (and what they need: Node, Python, Chrome)
Markdown only. No scripts, no assets. Code snippets assume CSS, React + Motion (motion.dev ≥14.2), Base UI, Reanimated 4/Expo (animate-expo), Swift 6 (write-swift). The prototype picker is a verbatim HTML/CSS/JS spec (copyable into a static page). Install is via `npx skills add` (not run).

## 6. Area
Motion (primary), development (mobile web, performance), QA (break-ui), process (prototype, learn-taste). Little on colour/layout/brand.

## 7. Take / skip
Take:
- The frequency/purpose gate, easing table, duration table and three curve tokens as our motion defaults. Precise numbers stop Claude from guessing.
- The "marketing gets more room, but not fade-in on every section" rule. This hits Elementor directly: its per-widget entrance animations make sites look AI/template-made. Allow one hero entrance plus a few meaningful moments, fired once, with non-uniform stagger.
- Hover gating plus `:active` press feedback, and the mobile-native baseline CSS block (works on static Vercel pages and in Elementor custom CSS).
- Reduced-motion "gentler, not zero" pattern.
- The forced REJECTED/KEPT sections in output, so our skill must show what it chose *not* to do.
- break-ui catalog as a QA pass for client sites (long business names, long emails, translated labels, missing images, 320px, 200% zoom).
- prototype's "named axis" rule for divergence. This is a direct tool for making same-niche sites differ (vary layout/density/personality/motion on purpose, not accent colour).
- learn-taste's DESIGN.md loop for keeping per-client and agency-wide rules.
Skip:
- animate-expo, write-swift and ask-sonner: we don't build native apps or React toast stacks.
- React/Motion-specific internals (layoutId, useAnimate, AnimatePresence modes), gestures/drag physics and velocity projection: rarely needed on brochure sites. Keep only "don't hand-roll a drawer/carousel; use native scroll-snap".
- improve-animations' plan-file machinery: too heavy for our flow.
- apple-design's "default to system font" and translucent glass toolbars. Both pull toward the generic look we're trying to avoid.
- The dashboard-oriented "100+/day" framing. Our sites are visited rarely, so the delight budget is larger. But keep the ban on repeated scroll reveals and hover-lift everywhere.

## 8. Open questions
- Internal tension: review-animations flags "pure-fade entrances with no transform", but remove-animations reduces frequent slide/scale entrances to opacity-only. Our skill needs one rule (suggest: opacity-only is fine for frequent or reduced-motion cases).
- Web toast = 400ms `ease` (Sonner), but native toast must stay ≤300ms. The exceptions are brand-specific, not universal.
- apple-design cites "Principles of Great Design (WWDC 2026)". Not verified.
- write-swift (42KB) and animate-expo RECIPES only skimmed (headings + relevant sections). Out of scope for Bexven.
- How to map these to Elementor's built-in Motion Effects (entrance animation, duration presets "slow/normal/fast", no custom bezier in UI) needs testing. Custom CSS may be required for the curve tokens.
- SUGGESTED: Emil Kowalski "You Don't Need Animations" / "7 practical animation tips" / "Agents with Taste" articles - https://emilkowal.ski/ui - source essays behind these rules, useful for rationale.
- SUGGESTED: easing.dev - https://easing.dev - curve library the skills point to for non-default curves.
