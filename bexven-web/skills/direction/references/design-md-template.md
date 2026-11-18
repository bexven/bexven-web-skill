# DESIGN.md template

Loaded at step 7. One DESIGN.md per client, in the project root. Shape follows Google's DESIGN.md spec (alpha): YAML front matter for tokens, then `##` sections in a fixed order. Tokens are the source of truth; prose explains how they are used. Bexven adds three sections after Do's and Don'ts: Assumptions, Known gaps, and a direction record.

## Rules for filling it

- Front matter starts on line 1 with `---` and ends with the next `---`. Only one front matter block. Each top-level key appears once.
- Quote every colour (`"#2b3a33"`). Write the hex value (sRGB) as the token; put the OKLCH source in a comment so Elementor (hex only) and CSS share one value. If you want oklch() in CSS, `palette.py scale` gives the `@supports` block for the build to add.
- References use `"{colors.ink}"`. `tokens_to_css.py` resolves them to `var(--color-ink)`.
- Bare numbers get units from the converter: fontSize, rounded, spacing → px; letterSpacing → em. lineHeight and fontWeight stay unitless. Write `clamp()` values as quoted strings.
- Motion keys: any value with `cubic-bezier()`/`linear()`/`steps()` becomes `--ease-*`; any ms/s value becomes `--dur-*`.
- Colour token names are roles, not hues: `paper`, `ink`, `ink-muted`, `surface`, `border`, `primary`, `on-primary`, `accent`, `on-accent`, `focus`, `danger`. Every fill has its `on-` pair. Always define `primary`. Every token must be used by the build (no orphans).
- Sections keep this order; omit one only by listing it under `omitted:` with a reason. Never pad.
- Keep Do's/Don'ts short: each is a hard limit with its reason.
- Check: `python3 ${CLAUDE_SKILL_DIR}/../build/scripts/tokens_to_css.py DESIGN.md` exits 0 and prints `--color-*`, `--font-*`, `--text-*`, `--radius-*`, `--space-*`, `--ease-*`, `--dur-*`.

## Converter output names (for the build)

| Front matter | CSS custom property |
|---|---|
| `colors.ink` | `--color-ink` |
| `typography.body.fontFamily` / `fontSize` / `fontWeight` / `lineHeight` / `letterSpacing` | `--font-body`, `--text-body`, `--text-body--weight`, `--text-body--line-height`, `--text-body--tracking` |
| `rounded.sm` | `--radius-sm` |
| `spacing.4` | `--space-4` |
| `motion.ease-out` / `motion.dur-state` | `--ease-out` / `--dur-state` |

## Template (copy from the line below the fence)

```markdown
---
version: alpha
name: "<Client name>"
description: "<Direction name>: <one-line governing idea>"
tells_version: "2026-11"
stage: mock            # mock | build
direction: "<Direction name>"
seed: 00000            # from niche_log.py pick
niche: "<niche-slug>"
hero_type: "<slug from layout.md>"
section_order: "hero,…,contact"
palette_family: "<e.g. slate blue + linen>"
mode: light            # light | dark (from the scene sentence)
colors:
  paper: "#f6f3ec"        # oklch(0.965 0.012 85) - from <real material>
  surface: "#ece7dc"      # one step off paper
  ink: "#1e2a33"          # oklch(0.25 0.03 245) - brand-tinted ink
  ink-muted: "#4a5560"    # secondary text, passes 4.5:1 on paper
  border: "#cfc8ba"
  primary: "#2f4858"      # brand colour (locked from <logo/sign>)
  on-primary: "#f6f3ec"
  accent: "#8a4b2a"       # action accent: primary CTA, links, focus only
  on-accent: "#fbf8f2"
  focus: "{colors.accent}"
  danger: "#9b2c2c"
  on-danger: "#ffffff"
typography:
  display:
    fontFamily: "<Display face>, <fallback>, serif"
    fontSize: "clamp(2.5rem, 1.6rem + 3.6vw, 4.5rem)"
    fontWeight: 500
    lineHeight: 1.05
    letterSpacing: -0.02
  headline:
    fontFamily: "<Display face>, <fallback>, serif"
    fontSize: "clamp(1.75rem, 1.4rem + 1.4vw, 2.5rem)"
    fontWeight: 500
    lineHeight: 1.15
    letterSpacing: -0.01
  title:
    fontFamily: "<Body face>, <fallback>, sans-serif"
    fontSize: 22
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: "<Body face>, <fallback>, sans-serif"
    fontSize: 18
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "<Body face>, <fallback>, sans-serif"
    fontSize: 15
    fontWeight: 500
    lineHeight: 1.3
    letterSpacing: 0.01
  caption:
    fontFamily: "<Body face>, <fallback>, sans-serif"
    fontSize: 14
    fontWeight: 400
    lineHeight: 1.45
rounded:
  none: 0
  sm: 2
  pill: 999
spacing:
  1: 4
  2: 8
  3: 12
  4: 16
  6: 24
  8: 32
  12: 48
  16: 64
  24: 96
  30: 120
motion:
  ease-out: "cubic-bezier(0.23, 1, 0.32, 1)"
  ease-in-out: "cubic-bezier(0.77, 0, 0.175, 1)"
  ease-drawer: "cubic-bezier(0.32, 0.72, 0, 1)"
  dur-press: 120ms
  dur-state: 200ms
  dur-surface: 320ms
  dur-moment: 700ms
---

# <Client name> - design

## Overview
**Governing idea:** <one sentence opening with a concrete object, place or era from the client's world>.
**Scene sentence:** <scene of use; audience; existing brand> → <light|dark>.
**Key characteristics:** 5-7 bullets (type voice, colour strategy, layout grammar, imagery treatment, signature moment, density).
**Why this fits:** one sentence. **Rut avoided:** one sentence naming what the niche usually ships.
**Emphasis device:** <weight | size | case | face>. **Signature:** <the one motion/hover idea, or none>.
**Differs from niche log:** display font, palette family, hero type, section order vs last 5 in niche (`check` passed).

## Colors
Strategy: <Restrained | Committed | Drenched> - <share of page, where brand fields sit>.
Per token: name, job, where it may appear, where it must never appear.
Accent allowed places: primary CTA, text links, focus ring. Max 2 uses per viewport.
Contrast pairs checked (`palette.py check`): ink/paper x:1, ink-muted/paper x:1, on-primary/primary x:1, on-accent/accent x:1, focus/paper x:1.
brand-source: <logo/sign/brief, only if saturated violet or other flagged hue>.

## Typography
Faces: <display> (<licence>, <source>), <body> (<licence>, <source>); self-hosted WOFF2, subsets, file budget ≤4 files/≤100KB.
Overused-list reason (if any): <non-category reason>.
Scale ratio, measure (65ch), case (sentence case), numerals (tabular for hours, prices, specs), caps/mono roles (none by default).

## Layout
Composition in words, section by section, in order (each neighbour differs). Hero type and exact first viewport at 1440×900 and 390×844 (H1, one hard fact, primary CTA). Container width, whitespace philosophy (dense/airy), section spacing. Card layouts used (max 2).

## Elevation
Ceiling: <flat + tone | one hairline | one shadow level>. Surface ladder. No default blurred shadow.

## Shapes
Radius language: <e.g. 0 on images and sections, 2px on fields, pill on buttons>. Nested radii concentric. Image geometry: aspect ratios, mobile crop focus, corners.

## Motion
The one moment (or none) and where; hover idea (child moves, never the card); durations from tokens; reduced motion keeps ≤150ms opacity/colour only. Same moment in mock and WP build.

## Voice & Content
2-3 tone words, each with what it rules out. Canonical terms (and banned synonyms). Main CTA wording, identical everywhere. Local names used (town, street, landmarks).

## Components
Header/nav (items in customers' words), primary and secondary button, link, form fields, the niche's key component (notice list, capabilities table…), footer with NAP. States: hover (gated), focus-visible, active, disabled.

## Do's and Don'ts
- Do <x> - because <reason>.
- Don't <y> - because <reason>.
(5-8 items total)

## Iconography & Imagery
Icon family + stroke (one family, inline SVG, functional only). Photo priority: client photos > flagged stock (`data-placeholder`) > placeholder block. Imagery treatment.

## Assumptions
- assumed: <fact> - because <evidence> - ask at build stage: <question>.

## Known gaps
- <missing item: photos, hours, reviews, licence numbers> - placeholder used: <how marked>.
```

## Notes

- `omitted:` example in front matter (a simple block list of quoted strings, which both parsers read):
  ```yaml
  omitted:
    - "Elevation: flat site, no layers"
  ```
- The extra keys (`tells_version`, `stage`, `direction`, `seed`, `niche`, `hero_type`, `section_order`, `palette_family`, `mode`) are allowed extensions; `tokens_to_css.py` ignores them. They mirror the `niche_log.py add` fields so logging is a copy job.
- After QA, sync: the shipped page wins on drift. Update tokens and prose, then re-run the converter and the niche log entry if a logged value changed.
- Dark mode shipped alongside light: same token names, defined twice (the build adds a `[data-theme=dark]` or media-query block); design both, never invert.
