# 10 — Web Interface Guidelines (Vercel)
https://github.com/vercel-labs/web-interface-guidelines · Guideline spec + review command · MIT · 1.2k stars · commit 434b7f9 (2026-10-05)

## 1. What it is
A "living, non-exhaustive" checklist of hundreds of small UI-quality decisions (interactions, focus, forms, motion, layout, content, perf, theming), mostly framework-agnostic with some React/Next.js items. Ships in three forms: README (prose), AGENTS.md (MUST/SHOULD/NEVER), and command.md (a review slash-command). A short "Vercel-specific" copywriting section is labelled as brand preference, not universal.

## 2. How it works
- README = human-readable spec, each rule a bold one-liner + short explanation.
- AGENTS.md = same rules compressed into MUST/SHOULD/NEVER for agents to apply during generation.
- command.md = audit prompt: read files given as args, check against rules + an explicit anti-pattern list, output terse `file:line - issue` findings grouped by file, "✓ pass" for clean files, no preamble.
- install.sh curls command.md into ~/.claude/commands etc. (not run; not needed — we can fold the rules into our own skill).
- It does NOT address aesthetics/originality; it is a craft/correctness floor that sits under any visual direction.

## 3. Rules
- [a11y] Every flow is keyboard-operable, following WAI-ARIA APG patterns
- [a11y] Every focusable element shows a visible focus ring; use `:focus-visible` (not `:focus`), `:focus-within` for grouped controls
- [a11y] Never `outline: none` without a visible replacement
- [a11y] Sticky headers/footers/banners/overlays never cover the focused element (use `scroll-padding`/`scroll-margin`)
- [a11y] Manage focus in dialogs/menus: trap, move in, return on close
- [a11y] Hit targets ≥24px desktop, ≥44px mobile; expand hit area if the visual is smaller
- [a11y] Never disable zoom (`user-scalable=no`, `maximum-scale=1`)
- [a11y] Prefer native elements (`button`, `a`, `label`, `table`) before ARIA
- [a11y] Icon-only buttons get a descriptive `aria-label`; decorative icons `aria-hidden="true"`
- [a11y] Images need `alt` (`alt=""` if decorative)
- [a11y] Accessible names exist even when the visual design omits visible labels
- [a11y] Don't rely on colour alone for status; add text/icon cue
- [a11y] Hierarchical h1–h6 and a "Skip to content" link
- [a11y] Toasts and inline validation announced via `aria-live="polite"`
- [a11y] Video: captions/transcripts for meaningful media; keyboard-operable controls; decorative media hidden from AT
- [a11y] Verify names/hiding in the browser accessibility tree
- [a11y] Contrast: meet it, ideally checked with APCA rather than WCAG 2 ratio alone
- [a11y] Charts use colour-blind-safe palettes
- [nav] Navigation uses `<a>`/`<Link>` so Cmd/Ctrl/middle-click work; never `<div onClick>` or `<button>` for links
- [nav] `<div>`/`<span>` with click handlers should be `<button>`
- [nav] State (filters, tabs, pagination, open panels) lives in the URL; deep-link everything
- [nav] Back/Forward restores scroll position
- [nav] `scroll-margin-top` on anchored headings so sticky headers don't hide them
- [nav] `<title>` reflects the current page/context
- [nav] No dead ends: every screen offers a next step or recovery path
- [components] If something looks clickable, it is clickable (no dead zones)
- [components] Loading buttons show a spinner and keep the original label
- [components] Spinners/skeletons: ~150–300ms show-delay and ~300–500ms minimum visible time to avoid flicker
- [components] Skeletons mirror final content exactly (no layout shift)
- [components] Confirm destructive actions or offer Undo with a safe window
- [components] Optimistic UI where success is likely; roll back or Undo on failure
- [components] Tooltips: delay the first, then peers in the group appear instantly; prefer inline help over tooltips
- [components] Design every state: empty, sparse, dense, error
- [components] Layouts survive short, average and very long content (truncate/line-clamp/break-words; `min-width:0` on flex children)
- [components] Empty strings/arrays never render broken UI
- [components] Hover/active/focus states have more contrast than the rest state; every button/link has a hover state
- [components] Gestures (drag/swipe/pinch) always have a click and keyboard alternative
- [components] During drag: disable text selection, set `inert` on the dragged element
- [components] Autofocus only on desktop with a single primary input; rarely on mobile
- [forms] Every control has an associated `<label>`; clicking the label focuses the control
- [forms] Checkbox/radio label and control share one generous hit target
- [forms] Mobile input font-size ≥16px (prevents iOS zoom)
- [forms] Never block paste; never block keystrokes — accept input, then validate with a message
- [forms] Don't pre-disable submit; allow submitting incomplete forms to show validation
- [forms] Submit stays enabled until the request starts, then disabled + spinner (+ idempotency key)
- [forms] Errors inline next to their field; on submit, focus the first error
- [forms] Set `autocomplete`, meaningful `name`, correct `type` and `inputmode`
- [forms] Disable spellcheck on email, codes, usernames
- [forms] Placeholders show an example value/pattern and end with `…`
- [forms] Enter submits single-input forms; in textarea Cmd/Ctrl+Enter submits, Enter = newline
- [forms] Warn before navigating away with unsaved changes
- [forms] Trim values (text expansion adds trailing spaces); support password managers and pasted OTP codes
- [forms] Non-auth fields (search) avoid names/autocomplete that trigger password managers
- [forms] Native `<select>`: set explicit `background-color` and `color` (Windows dark-mode bug)
- [motion] Honour `prefers-reduced-motion` with a reduced variant (muted loops stop too)
- [motion] Prefer CSS > Web Animations API > JS libraries
- [motion] Animate only `transform`/`opacity`; never `top/left/width/height`
- [motion] Never `transition: all`; list the properties explicitly
- [motion] Animate only to clarify cause/effect or for deliberate delight
- [motion] Easing chosen for what changes (size, distance, trigger); correct `transform-origin`
- [motion] Animations are interruptible by user input
- [motion] No autoplay except muted, non-essential loops; motion >5s alongside content needs pause/stop/hide
- [motion] SVG: transform `<g>` wrappers with `transform-box: fill-box; transform-origin: center`
- [motion] Animate a wrapper rather than scaling text directly (anti-aliasing artefacts)
- [layout] Every element aligns deliberately to grid, baseline, edge or optical centre; adjust ±1px optically
- [layout] Balance icon+text lockups (stroke weight, size, spacing, colour)
- [layout] Verify on mobile, laptop and ultra-wide (zoom to 50% to simulate)
- [layout] Respect safe areas with `env(safe-area-inset-*)` on full-bleed layouts
- [layout] No unwanted scrollbars; fix overflow (test with macOS "always show scroll bars")
- [layout] Let CSS flex/grid size things; don't measure layout in JS
- [layout] `overscroll-behavior: contain` in modals/drawers; `none` on `<html>` only under `@media (pointer: fine)`
- [layout] `touch-action: manipulation`; set `-webkit-tap-highlight-color` to fit the design
- [type] Use `…` not `...`; curly quotes not straight
- [type] Avoid widows/orphans: `text-wrap: balance`/`pretty` on headings
- [type] `font-variant-numeric: tabular-nums` for numbers that get compared (tables, prices, stats)
- [type] Non-breaking spaces to glue units, shortcuts, brand names (`10&nbsp;MB`)
- [type] Menu items that open a follow-up and in-progress states end with `…` ("Rename…", "Saving…")
- [colour] Layered shadows (ambient + direct, ≥2 layers); combine with semi-transparent borders for crisp edges
- [colour] Nested radii: child ≤ parent and concentric
- [colour] On coloured backgrounds, tint borders/shadows/text toward the same hue
- [colour] `color-scheme: dark` on `<html>` for dark themes; `<meta name="theme-color">` matches page background
- [colour] Dark fades via CSS masks can band; use a background image instead
- [perf] `<img>` has explicit width/height; reserve space (no CLS)
- [perf] Preload/`fetchpriority="high"` only above-the-fold images; `loading="lazy"` for the rest
- [perf] `<link rel="preconnect">` for CDN/font origins
- [perf] Preload critical fonts with `font-display: swap`; subset via `unicode-range`, limit variable axes
- [perf] Use `<video autoplay muted loop playsinline>` instead of animated GIF, with still fallback
- [perf] Virtualize or `content-visibility: auto` for long lists (>50 items)
- [perf] No layout reads in render; batch DOM reads/writes
- [perf] Move long tasks off the main thread (Web Workers)
- [perf] Mutations (POST/PATCH/DELETE) target <500ms
- [qa] Test iOS Low Power Mode and macOS Safari; profile with CPU+network throttling, extensions off
- [code] Hydration-safe inputs (`value` needs `onChange`, or use `defaultValue`); guard date/time rendering against mismatch
- [code] Locale-aware dates/numbers/currency via `Intl.*`; detect language from `Accept-Language`/`navigator.languages`, never IP
- [code] `translate="no"` on brand/product names and code tokens
- [copy] Active voice, second person, action-oriented ("Install the CLI")
- [copy] Specific button labels ("Save API Key", not "Continue")
- [copy] Error messages say how to fix it, not just what failed
- [copy] Numerals for counts ("8 deployments"); space between number and unit
- [copy] Currency: 0 or 2 decimals consistently within a context, never mixed
- [copy] Keep nouns consistent; as few unique terms as possible; be concise
- [copy] (Vercel-only) Title Case for app headings/buttons, sentence case on marketing pages; `&` over "and"
- [process] Run an audit pass on generated UI: output `file:line - issue`, grouped by file, no preamble

## 4. AI tells / anti-patterns it bans
Not about visual "AI look" at all — it bans sloppy-implementation tells common in generated code: `transition: all`; `outline: none` with no replacement; disabled zoom; `<div onClick>`/click-handler spans; images without dimensions; inputs without labels; icon buttons without aria-label; blocked paste; hardcoded date/number formats; unjustified `autoFocus`; animated GIFs; gesture-only actions; three-dot `...` and straight quotes; generic "Continue" buttons; colour-only status.

## 5. Data, assets and scripts it ships (and what they need: Node, Python, Chrome)
README.md, AGENTS.md, command.md (Claude Code-compatible slash command), install.sh (bash + curl, copies command.md into agent config dirs — not run). README also points to `npx skills add vercel-labs/agent-skills --skill web-design-guidelines` (not installed). No data, fonts or images.

## 6. Area
development / QA (with some design craft: shadows, radii, alignment, typography details)

## 7. Take / skip
- TAKE: almost all of sections Interactions, Forms, Animations, Layout, Content, Performance, Design as our "build quality floor" checklist — applies equally to static Vercel pages and WP/Elementor output (Elementor often emits `transition: all`, missing focus rings, unlabeled icon buttons, images without dimensions).
- TAKE: command.md's anti-pattern list + terse `file:line` output format as a model for our own QA/review step (Playwright can verify several: focus visibility, CLS, overflow scrollbars, aria-labels).
- TAKE: typography polish (`…`, curly quotes, `&nbsp;` units, `text-wrap: balance`, tabular-nums) — cheap and makes sites look hand-crafted.
- TAKE: copy rules (specific CTAs, errors with fixes, numerals) — useful for contact/quote forms on SMB sites.
- SKIP/ADAPT: Vercel-only copy rules (Title Case on buttons, `&` over "and") — brand preferences; client voice should decide.
- SKIP: React/Next-specific items (re-renders, React Scan, nuqs, hydration, optimistic updates, virtualized lists, Web Workers, 500ms mutation budget) — mostly irrelevant for brochure sites; keep only as notes for app-like builds.
- SKIP: install.sh and the external `npx skills` command.
- Note: gives zero aesthetic direction; must be paired with taste/originality sources (01, 04, 05).

## 8. Open questions
- Rule "Mobile input size" offers `maximum-scale=1` as an alternative, but the same doc (AGENTS.md/command.md) flags `maximum-scale=1` as an anti-pattern — internal contradiction; we should use the 16px font route only.
- APCA vs WCAG 2: APCA is not yet a legal standard; for client compliance (ADA/EAA) we likely still need WCAG 2.2 AA as the gate, APCA as a secondary check.
- "Every button/link has a hover state" and "interactions increase contrast" may conflict with taste-skill advice to keep hover effects minimal — reconcile as "hover feedback yes, decorative hover animations no".
- SUGGESTED: vercel-labs/agent-skills (web-design-guidelines skill) - https://github.com/vercel-labs/agent-skills - packaged review skill built on this spec; may include more/updated rules.
