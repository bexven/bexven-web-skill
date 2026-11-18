---
name: build
description: "Build distinctive, non-generic static HTML/CSS pages, sections and components from a client's DESIGN.md, following Bexven house rules: tokens generated into :root CSS, semantic markup, fluid type, accessible forms, anti-slop copy, one named motion moment, local SEO (NAP, tel: links, LocalBusiness JSON-LD, noindex on outreach previews), self-hosted fonts, then an optional Vercel preview deploy. Use whenever coding, redesigning or fixing a web page, homepage, landing page, cold-outreach mockup, section, contact or quote form, header, footer or any HTML/CSS component, even when the user does not mention DESIGN.md. Small jobs (one form or section) take a short path; a whole page or site with no DESIGN.md goes to /bexven-web:direction first."
license: Proprietary (Bexven)
---

# Build: static HTML/CSS from DESIGN.md

Turns a decided direction (DESIGN.md) into plain HTML/CSS that looks like it belongs to this one client and no other, passes the accessibility and performance floors, and is ready for QA and a Vercel preview. Plain HTML + one CSS file + JS only for the menu, the form and the one named motion moment. No frameworks, no component libraries, no CDNs. The direction is already decided: your job is to execute it precisely, not to re-design it or fall back to "a normal website".

## 0. Size the job first

| Job | Path |
|---|---|
| Full page, homepage, site, outreach mockup, **and DESIGN.md exists** | Full workflow below |
| Full page/site, **no DESIGN.md** | Stop. Hand off to `/bexven-web:direction`, then come back |
| Small job (one form, one section, header/footer, a component, a fix) | Small-job path |

**Small-job path.** If the project has DESIGN.md or a tokens file, reuse its tokens and skip to step 3. If not, write this 5-line mini direction as a comment at the top of the CSS, then build:
1. Scene sentence: who uses it, on what device, in what state of mind.
2. Type pair: one text face (+ optional display face), self-hosted, not on the overused list in `references/tells.md`.
3. Colour strategy: Restrained / Committed / Drenched + ink, paper, one action accent (derived, never #000/#111/#fafafa).
4. One emphasis device: weight, size, case or face. Only that one.
5. Radius language: e.g. "0 everywhere, pill buttons" or "4px fields, 0 sections".
Then do steps 3–8 that apply (a form needs step 6 and the forms section of `references/components.md`; skip deploy unless asked).

## Workflow (full job)

1. **Read DESIGN.md** in full: thesis, key characteristics, tokens, composition pattern, first viewport, emphasis device, signature, motion moment, Do/Don't, Assumptions, Known gaps, `tells_version`. Open `references/niches/<niche>.md` for must-have content and no-gos. Skim `references/tells.md`. Write a 6-line build note (section list in order with each section's layout, the one moment, the hover idea, fonts to self-host) before any code.
2. **Generate tokens:** `python3 ${CLAUDE_SKILL_DIR}/scripts/tokens_to_css.py DESIGN.md -o css/tokens.css`. Exit 1 = unresolved reference or nothing to output; exit 2 = no front matter or YAML error. Fix DESIGN.md, never hand-patch tokens.css. Components use only these custom properties.
3. **Semantic skeleton** following the composition pattern named in DESIGN.md: skip link, `header/nav/main/footer`, one h1, h2 per section, no skipped levels. Neighbouring sections never share a layout. Load `references/html-css-craft.md`.
4. **Type and colour** from tokens: fluid sizes with `clamp()`, measure 65ch, body ≥17px (≥18px for older audiences), the single emphasis device, accent only in its listed places (max 2 per viewport).
5. **Components:** nav, CTAs, cards (≤2 card layouts per page), reviews (real only), NAP block, map facade, forms. Load `references/components.md`. Icons and images: load `references/imagery-icons.md`.
6. **Copy pass:** every string from the fact sheet/DESIGN.md; nothing invented; unknowns get `data-assumed` and go in the report. Run the slop check (vocabulary, cadences, button labels) against `references/tells.md`. Verb + object on every button.
7. **Motion:** only the moment DESIGN.md names (or none). States: hover gated, `:active`, `:focus-visible`. Load `references/motion.md`.
8. **Local SEO + head:** title, description, canonical rules, OG, LocalBusiness subtype JSON-LD matching visible NAP, `tel:` links, `noindex` on outreach previews. Load `references/seo-local.md`.
9. **Fonts and assets:** self-host WOFF2 (≤2 families, ≤4 files, ≤100KB), preload 1–2 critical files, `<picture>` AVIF/WebP with width/height. Check no requests to Google Fonts, Fontshare or image CDNs remain.
10. **Self-check, then hand off** to `/bexven-web:qa` with: file paths, the build note, assumptions, stock images used, known gaps. Fix what QA returns (max 3 rounds).
11. **Deploy (optional):** Vercel preview only when asked or when the outreach flow calls for it. Load `references/vercel-deploy.md`. Preview by default; `--prod` only on explicit request; token from `VERCEL_TOKEN`, never `--token`; ask before any git push.

## Non-negotiable rules

1. No raw hex/rgb/oklch in component CSS; only tokens from `:root`. Missing token → add it to DESIGN.md and regenerate.
2. Never ship the default skeleton (hero → 3 feature cards → testimonials → FAQ → CTA, eyebrow + heading + lede on each). Follow the DESIGN.md composition pattern.
3. Never invent facts: hours, prices, years, counts, credentials, reviews, staff names. Real data or a visible, labelled placeholder plus `data-assumed`.
4. Use the prospect's real public NAP, written identically in header/footer, contact block and JSON-LD; phone is a `tel:` link with the international number in the href.
5. Every interactive element: default, hover (inside `@media (hover:hover) and (pointer:fine)`), `:focus-visible` (2px solid, 2px offset, ≥3:1), `:active`, disabled. No card lift/zoom; at most one hover-motion idea, the one named in DESIGN.md, moving a child.
6. Contrast is a gate: body 4.5:1 (7:1 for funeral/older audiences), large text and UI 3:1. Touch targets ≥44px, phone button and mobile CTA ≥48px.
7. Forms: visible labels, correct types and autocomplete, specific submit label, real endpoint or a clearly labelled demo state. Never `action="#"`, never a fake success.
8. At most one motion moment per page (hero counts). No section reveals, no smooth-scroll library, no parallax. Content visible without JS. Animate only transform/opacity; never `transition: all`.
9. Self-host everything: fonts, images, scripts (pinned versions). Zero requests to fonts.googleapis.com, fonts.gstatic.com, api.fontshare.com, unsplash, pexels, placehold.co, picsum.
10. LCP image is a real `<img>` in the HTML with `fetchpriority="high"`, not lazy, not a CSS background. Every image has width/height.
11. No auto-rotating carousels, marquees, popups, self-opening chat, bento grids, icon-in-circle grids, gradient text, glass, glow, grain.
12. Sentence case unless DESIGN.md says otherwise; no single accented word in headlines; eyebrows off (max 2, only when informative).
13. Outreach previews carry `<meta name="robots" content="noindex, nofollow">` and no canonical to a domain we do not control.
14. Hero `min-height: 100svh` at most; other sections size to content. No `100vh`.
15. An explicit client brief or existing brand pin beats any anti-tell rule; record the reason in DESIGN.md.

## When to load which reference

| Step | File | Why |
|---|---|---|
| 1 | `references/niches/<niche>.md` | Must-have content, register, schema type, no-gos |
| 1, 6 | `references/tells.md` | Dated tells: fonts, palettes, components, copy, motion |
| 3–4 | `references/html-css-craft.md` | File layout, layers, fluid type, spacing, polish, a11y CSS |
| 5 | `references/components.md` | Nav, CTAs, cards, reviews, NAP, maps, sticky UI, **full form recipe** |
| 5, 9 | `references/imagery-icons.md` | Photo priority, placeholders, funeral people rules, icon family |
| 7 | `references/motion.md` | Frequency gate, tokens, ladder, reduced motion |
| 8–9 | `references/seo-local.md` | Head tags, JSON-LD, CWV and asset budgets, font loading |
| 11 | `references/vercel-deploy.md` | Preview deploy, temporary deploy, token handling |

## Script

`${CLAUDE_SKILL_DIR}/scripts/tokens_to_css.py DESIGN.md [-o OUTPUT] [--refs var|literal] [--selector SELECTOR]`
- Reads the DESIGN.md YAML front matter (`colors`, `typography`, `rounded`, `spacing`, `motion`) and prints a `:root` block: `--color-*`, `--font-<role>`, `--text-<role>` (+ `--weight`, `--line-height`, `--tracking` suffixes), `--radius-*`, `--space-*`, `--ease-*`, `--dur-*`.
- `{colors.primary}` references become `var(--color-primary)` by default; `--refs literal` inlines values.
- Colours pass through unchanged. Bare numbers get px (sizes, radii, spacing) or em (letterSpacing).
- Fluid `clamp()` sizes are not generated: write them in `base.css` from the `--text-*` min/max tokens (see html-css-craft.md).

## Default file layout

```
index.html
css/tokens.css      # generated, never edited by hand
css/styles.css      # @layer reset, base, layout, components, utilities
js/site.js          # menu, form, the one moment (defer)
fonts/*.woff2 + LICENSE files
img/*.avif|webp|jpg (descriptive names)
```

## Gotchas

- The model's pull is toward Inter/system fonts, an 8–12px radius on everything, a soft shadow on every card, three equal columns and centred everything. Check each against DESIGN.md before writing it.
- `tokens_to_css.py` emits `--text-display-lg` as one fixed size. Do not paste it as the final h1 size; build the `clamp()` from it.
- "Fade-up on scroll" sneaks in via a reused `.reveal` class. Delete it unless it is the named moment.
- Placeholder text inside inputs is not a label, and grey placeholder fails contrast anyway.
- A form demo that says "Thanks, we'll be in touch" without sending anything is a fake success. Use a labelled demo state.
- `display:none` honeypots get skipped by bots; hide off-screen instead (see components.md).
- JSON-LD that lists hours or a rating not visible on the page is a spam signal. Mark up only visible content.
- `scroll-behavior: smooth` outside a reduced-motion query, and hover rules outside the hover media query, are the two most common lint failures.
- Forgetting `noindex` on an outreach preview can let a mock outrank the prospect's real site.
- Em-dash density creeps in during the copy pass: max one per paragraph.

## Hand-off

When the page builds cleanly: `/bexven-web:qa` (screenshots, lint, critique). After the client says yes: `/bexven-web:elementor`.
