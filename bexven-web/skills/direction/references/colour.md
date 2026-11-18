# Colour

Loaded at steps 5-6. Method for a client palette in OKLCH, the token roles, strategy, accent limits, ink and paper, the purple rule, and light vs dark.

## 1. Where colour comes from

1. Lock the client's existing brand colour (logo, sign, vehicles, uniforms). Convert it: `palette.py convert "#2f4858"` → OKLCH L, C, H.
2. If there is no usable brand colour, sample from the client's real material: brick, stone, timber, paint finish, landscape, print. Write the source next to the token (`# from porch paint`).
3. Never from category association (funeral = gold/burgundy, trades = slate + safety orange, "trust" = blue). Never from stock Tailwind, Radix or shadcn hues as the brand colour.
4. No palette randomisers or palette APIs. Palettes are reasoned, then checked.

## 2. OKLCH method

- L = lightness 0-1, C = chroma (0 grey to ~0.37 max; most brand colours 0.04-0.16), H = hue angle.
- Shades vary L; same-weight sets keep L and C and rotate H; hover = shift L by ~0.04-0.06.
- Build a 12-step scale around the brand hue:
  `palette.py scale --hue <H> --chroma <C> --name <name>` (add `--lightness <L>` to put the exact brand colour on step 9; `--theme dark` for a dark scale).
- Step jobs: 1-2 page/section grounds · 3-5 component fills (rest/hover/pressed) · 6-8 borders, separators, focus · 9-10 solid fill and its hover · 11-12 text (low/high contrast).
- Greys: a neutral or brand-tinted grey scale (same script, chroma 0.005-0.02 at the brand hue). Tint secondary text, borders and shadows toward the surface they sit on; never plain grey on colour.
- Out-of-gamut colours are clamped to sRGB by the script (chroma reduced, hue and L kept). Write sRGB hex as the token; wider P3 only inside `@media (color-gamut: p3)` in the build.
- Hex in DESIGN.md front matter (Elementor global colours take hex), OKLCH source in a comment.

## 3. Token roles

Role names, defined once: `paper`, `surface`, `ink`, `ink-muted`, `border`, `primary`, `on-primary`, `accent`, `on-accent`, `focus`, `danger`, `on-danger`. Optional: `surface-2`, `field` (a brand field colour for Committed strategies), `on-field`.
- Every fill has an `on-` pair that passes contrast.
- Every colour has a human name, a job, and where it may and must never appear (DESIGN.md Colors section).
- Always a `primary`; no orphan tokens.
- Contrast is checked per touching pair (text on surface, button on section), not per swatch.

## 4. Strategy (one of the direction axes)

| Strategy | Share | Typical use |
|---|---|---|
| Restrained | ~85% neutral (paper/ink), brand colour in type and a few fields | document, editorial, calm niches |
| Committed | brand colour owns 30-60% of the page as fields (hero, one or two sections, footer) | strong existing livery, bold signage |
| Drenched | one colour is the page ground; type and photos sit on it | a client whose identity is one colour |

Section grounds vary only with intent: no predictable light/dark/light banding, no lone unexplained dark band.

## 5. The action accent

- Exactly one action accent. Never invent a second.
- Allowed places, written in DESIGN.md: primary CTA, text links, focus ring. Nothing else by default.
- Max 2 uses per viewport. Brand fields (Committed/Drenched) are not accents and do not count.
- If the brand colour fails text contrast, use a darker step (11-12) for text and keep the bright one for fills.
- Accent hue goes into the niche log (`--accent-hue`); `check` flags ±20° of the last 3 sites in the niche.

## 6. Ink and paper

- Ink: OKLCH L 0.18-0.26 with a slight tint of the brand hue (chroma 0.01-0.04). Never stock #000, #111, #0f0f0f.
- Paper: from the client's material (linen, limestone, whitewash, galvanised steel grey). Never stock #fafafa or pure #fff as a thoughtless default (pure white is fine when it is the client's material, e.g. white signage; say so).
- Body text on older-audience sites (funeral, senior care) aims for 7:1; everyone else at least 4.5:1.

## 7. Contrast gate

WCAG 2.2 AA is pass/fail: body 4.5:1; large text (≥24px, or ≥18.66px bold) and UI components/focus rings 3:1. APCA is advisory for thin or light text.
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/palette.py contrast "#1e2a33" "#f6f3ec"
python3 ${CLAUDE_SKILL_DIR}/../build/scripts/tokens_to_css.py DESIGN.md -o /tmp/tokens.css
python3 ${CLAUDE_SKILL_DIR}/scripts/palette.py check /tmp/tokens.css \
  --pair color-ink:color-paper --pair color-ink-muted:color-paper \
  --pair color-on-primary:color-primary --pair color-on-accent:color-accent \
  --large-pair color-focus:color-paper
```
Tokens are not accepted until every pair passes. Record the ratios in DESIGN.md Colors.

## 8. The purple rule

- Not by default: Tailwind indigo/violet hexes (#6366F1 #4F46E5 #4338CA #3730A3 #8B5CF6 #7C3AED #A855F7 and near matches), purple→blue/pink/cyan gradients, gradient text.
- The ban is about saturation, not hue: saturated violet/indigo (OKLCH hue 260-320 with chroma ≥ 0.08) needs a `brand-source:` line in DESIGN.md (existing brand or explicit brief). `palette.py` and `lint_html.py` use exactly this threshold. `--allow-violet` only with a brand source.
- Deep low-chroma plum or aubergine (C < 0.08) from the client's world, and purple-tinted neutrals, are fine.
- Never violet because of category ("AI", church, spirituality).

## 9. Flat by default

- No generic gradient washes, grain overlays, glass (`backdrop-filter`), glows, aurora or spotlight backgrounds.
- Texture or depth only from the client's real material (photos, scanned paper, metal, signage) or a named signature, with a reason in DESIGN.md.
- Gradients only when they carry hierarchy (e.g. a scrim for text on a photo when contrast needs it).

## 10. Light vs dark

- Decide from the scene sentence (scene of use, audience, existing brand). Category only breaks a tie.
- Dark is not the default for local service sites. Dark needs a scene reason ("used at night in a dim workshop" is weak; "the brand is white-on-black signage and the audience is young" is a reason).
- If both modes ship, design both under the same token names; never invert. Dark: `color-scheme: dark`, matching `theme-color`, a 3-4 step surface ladder with ~8% alpha borders instead of shadows, light text gets slightly more line-height and weight.
- Generate the dark brand scale with `palette.py scale … --theme dark` rather than flipping the light one.

## 11. Tells to avoid (see `tells.md`)

Cream + high-contrast serif + terracotta; near-black + one acid/neon accent with glow; slate + safety orange for every trade; stock #111/#fafafa; saturated violet gradients. If a warm palette is genuinely right, change at least two of ground, face class and accent compared with the cream/serif/terracotta tell.
