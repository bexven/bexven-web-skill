# 08 — DESIGN.md spec (Google Labs)
https://github.com/google-labs-code/design.md · Format spec + Node CLI (linter/exporter) · Apache-2.0 · 28.9k stars · commit db977b3, 2026-11-17 (spec version "alpha", CLI @google/design.md 0.4.1)

## 1. What it is
An open, plain-text format for handing a visual identity to coding agents: one `DESIGN.md` file = YAML design tokens (exact values) + markdown prose (the why and how to apply them). Ships with a TypeScript CLI that lints, diffs and exports the tokens (Tailwind v3/v4, W3C DTCG). Spec is alpha and still changing.

## 2. How it works
- Tokens live in YAML front matter (`---` fences at top) and/or fenced ```yaml blocks inside the matching `##` section. All blocks merge into one tree; each top-level key may appear only once across the file (duplicate = file rejected).
- Top-level schema: `version` (opt, "alpha"), `name` (the only truly required field), `description` (opt), `omitted` (opt list of intentionally skipped sections, optionally with a reason), `colors`, `typography`, `rounded`, `spacing`, `motion`, `components`. Unknown extra keys are allowed (custom extension); keys that look like typos (`colours`) get warned.
- Types: Color = any CSS colour string (hex recommended; converted to sRGB for contrast checks). Dimension = number + px/em/rem. Duration = number + ms. Typography = object {fontFamily, fontSize, fontWeight, lineHeight (unitless preferred), letterSpacing, fontFeature, fontVariation}. Motion = {duration, delay, timingFunction}. Spacing may also be a unitless number (column counts).
- References: `{colors.primary}` style dot paths; must point to a primitive, except inside `components` where composite refs (`{typography.label-md}`) are allowed. Prose may also cite tokens as `{colors.paper}`.
- Groups: colors/typography/rounded/spacing accept nested sub-maps (e.g. `light`/`dark` modes, `sm/md/lg/xl` breakpoints), flattened to dot paths; a flat key and a grouped key that collapse to the same CSS var name is an error.
- Components: map of name -> {backgroundColor, textColor, typography, rounded, padding, size, height, width}; states are sibling keys (`button-primary-hover`). Unknown properties accepted with a warning.
- External refs: inline code span `@path/file.ext[#fragment]` points to companion files (HTML sticker sheets with `<!-- COMPONENT: name -->` markers, other .md guides). All paths resolve from the DESIGN.md folder; leading `/` or escaping the folder is an error.
- Sections: `##` headings in fixed order (any may be omitted, present ones must keep order): 1 Overview (alias Brand & Style), 2 Colors, 3 Typography, 4 Layout (Layout & Spacing), 5 Elevation & Depth, 6 Shapes, 7 Motion & Micro-interaction, 8 Voice & Content Strategy, 9 Components, 10 Do's and Don'ts. Unknown sections (e.g. `## Iconography`) are preserved. Duplicate headings reject the file. Optional `#` title is ignored.
- Consumption by agents: read tokens as normative values, prose as intent; Overview is the fallback for any decision no token covers; Do's/Don'ts are guardrails. `design.md spec` prints the spec for injecting into a prompt; `lint` returns JSON findings an agent can act on.
- PHILOSOPHY.md: prose is the heart of the format; tokens are "context, not rendering instructions". A specific real-world reference ("1970s graduate lecture handout") beats adjectives ("modern, clean, premium"), which pull the model to the generic middle. A specific reference brings its negative constraints for free; add a short, deliberate Don'ts list on top.

## 3. Rules
- [brand] Open every brief with a concrete real-world reference object/place/era, not a list of adjectives
- [brand] Overview states personality, audience and the emotional response; it is the fallback for undecided choices
- [process] One DESIGN.md per client, kept in the project root; tokens are the source of truth, prose explains use
- [process] Keep the 10 sections in canonical order; omit irrelevant ones rather than padding them, and list them under `omitted` with a reason
- [colour] Always define a `primary` colour (linter warns otherwise; agents invent one)
- [colour] Give each colour a descriptive human name and an explicit job in prose, including where it must never appear
- [colour] Prefer few, purposeful colours; every colour token should be used by some component (orphaned-token warning)
- [colour] Put mode-dependent surfaces/text under `light`/`dark` groups; brand roles stay top level
- [type] Always define typography tokens (missing = agent falls back to default fonts, i.e. the generic look)
- [type] 9–15 type levels named by role (display/headline/body/label/caption + size); use unitless line-height
- [type] Responsive sizes go in `sm/md/lg/xl` breakpoint groups
- [space] Spacing scale as named tokens (xs–xl plus gutter, margin, columns); describe the grid model in Layout prose
- [layout] Layout prose names the grid model and max width (e.g. fluid mobile, fixed 1200px desktop)
- [components] Elevation section says how hierarchy is shown: shadow spec (blur, spread, colour) or the flat alternative (borders, tone)
- [components] Shapes: one stated radius language; don't mix sharp and round in one view
- [components] Component tokens reference base tokens (`{colors.x}`), with hover/active as sibling keys
- [components] Point to real component markup with `@components/file.html#name` refs when a kit exists
- [motion] Name motion tokens by purpose (state-change, surface-enter, surface-exit), not speed
- [motion] Small changes faster than big ones; entering decelerates, leaving accelerates; animate transform/opacity only
- [motion] Honour prefers-reduced-motion; state what deliberately never moves
- [copy] Voice section: 2–3 tone adjectives plus what they rule out; one capitalisation style; canonical terms with banned synonyms
- [copy] Buttons are verb phrases naming the outcome, never "OK"/"Submit"; define empty/error-state wording and date/number formats
- [a11y] Component text/background pairs must meet WCAG AA 4.5:1 (linter checks)
- [qa] Keep the Don'ts list short and specific; a long rambling list means the reference was too vague
- [tooling] Lint the brief (`lint`, JSON out, exit 1 on errors) and `diff` revisions to catch regressions
- [tooling] Export tokens to Tailwind v4 `@theme` CSS / DTCG JSON instead of hand-copying values

## 4. AI tells / anti-patterns it bans
- Adjective-only briefs ("modern, clean, trustworthy, premium") -> generic centre-of-distribution output
- Missing primary colour or missing typography -> agent auto-generates / defaults (the classic AI look)
- Philosophy example Don'ts: hero moment on a page that shouldn't have one, italic standfirst under big title ("Substack register"), decorative corner ornaments/glyphs, gratuitous gradients, glows, glass, drop shadows, dark mode
- Generic button labels; inconsistent capitalisation/terminology
- Note: the shipped examples themselves use Inter / Plus Jakarta Sans / Space Grotesk, Material-3-style 50-token colour lists and glassmorphism, i.e. common AI-tell choices. The format does not prevent generic designs; quality depends on what is written into it.

## 5. Data, assets and scripts it ships (and what they need: Node, Python, Chrome)
- `docs/spec.md` (generated, ~620 lines), `PHILOSOPHY.md`, 3 examples (DESIGN.md + tailwind.config.js + design_tokens.json each), ~9 linter fixtures (Heritage, Meridian, Alpine Observatory, etc.).
- CLI `@google/design.md` (npm, Node >=18; built with Bun; deps: unified/remark, yaml, zod, citty). Commands: `lint`, `diff`, `export` (json-tailwind, css-tailwind, dtcg), `spec`. Also a JS library export (`lint(markdown)`). No Python, no Chrome.
- 11 lint rules: broken-ref (error); missing-primary, contrast-ratio, orphaned-tokens, missing-typography, section-order, unknown-key, token-like-ignored (warning); token-summary, missing-sections, omitted-rules (info). Orphan rule treats MD3 colour families as always "used".
- Not run (per brief); assessed from source only.

## 6. Area
brand / design (format), tooling (linter/exporter)

## 7. Take / skip
Take:
- Adopt DESIGN.md as the per-client design brief format. It fits well: plain markdown any agent reads, exact tokens, a section skeleton that covers type, colour, layout, motion, voice and Do's/Don'ts, and extension keys/sections for our own needs. One file per client also makes niche differentiation auditable (diff two funeral-home briefs).
- The PHILOSOPHY principle "specific reference > adjectives" as a mandatory first step of our brief, with a short client-specific Don'ts list (this is our anti-sameness lever).
- Use custom sections/keys for Bexven-specific choices: e.g. `## Iconography`, `## Imagery`, section-order/page-structure choices, and a "differs from" note vs other sites in the niche. Unknown sections are preserved by spec.
- `export --format css-tailwind` / `dtcg` idea: generate CSS custom properties for the Vercel static page and map the same tokens to Elementor global colours/fonts later, so static redesign and WP build share one source.
- Optional `lint` as a QA gate (needs Node + npx from npm; fine on dev machines, keep optional so the skill works without it). Contrast check is useful.
Skip:
- The examples' token style (MD3 50-colour palettes, Inter/Plus Jakarta Sans, glass) — copy the structure, not the content.
- Component token schema beyond basics: limited properties (no border, shadow, gap); Elementor widgets won't map 1:1. Keep components mostly prose + key tokens.
- Treating the spec as stable: alpha, expect changes; pin our own template to this commit's rules.

## 8. Open questions
- Should our template require Voice & Content Strategy and Do's/Don'ts (spec makes all sections optional)? Recommend yes.
- How to represent page structure / section order per site (not in spec)? Checked: the `section-order` rule filters out unknown headings, so a custom `## Page Structure` (or `## Imagery`, `## Iconography`) can sit anywhere without warnings. Open point is only what we put in it.
- Mapping DTCG export to Elementor Global Kit JSON — needs a small converter of our own.
- SUGGESTED: W3C Design Tokens Format Module - https://tr.designtokens.org/format/ - the token standard DESIGN.md borrows from; useful if we build an Elementor kit converter.
