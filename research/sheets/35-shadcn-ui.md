# 35 — shadcn/ui
https://ui.shadcn.com · Component code-distribution system (React) · MIT · 128.5k stars (github.com/shadcn-ui/ui) · read 2026-11-18

## 1. What it is
Not a library you import: a CLI + flat-file registry that copies accessible component source (Radix/Base UI primitives, Tailwind) into your project to edit. Default look (neutral greys, rounded-lg, thin borders, Inter-ish sans) is now the baseline of most AI-generated SaaS UI.
## 2. How it works
`components.json` + CLI pulls component files into the repo; theming via CSS variables mapped to Tailwind utilities (`bg-background`, `text-primary`). Stack: React + Tailwind (Next/Vite etc.). Bexven ships static HTML/CSS and WordPress/Elementor, so the components themselves are unusable as-is.
## 3. Rules
- [colour] Name tokens by role, not hue: each surface has a `-foreground` pair (primary/primary-foreground, card, popover, secondary, muted, accent), plus destructive, border, input, ring, chart-1..5.
- [colour] Write token values in oklch(); dark mode overrides the same names under one selector (`.dark`) instead of new names.
- [space] One base `--radius`, derive sm/lg/xl with calc() multipliers so the whole radius scale changes from one value.
- [code] New token = define in :root and dark scope, then expose it; never hard-code hex in components.
## 4. AI tells / anti-patterns it bans
Bans none; it *is* a tell when untouched: zinc/slate neutral palette, default radius 0.625rem, card-with-border grid, outline+solid button pair, Lucide icons, muted grey subcopy.
## 5. Data, assets and scripts it ships
React/TS components, CLI (Node). Nothing usable in plain HTML or Elementor without porting.
## 6. Area
development / design-system (tokens)
## 7. Take / skip
Take: the role-based token naming (surface/foreground pairs, single radius base, oklch, one dark-mode override scope) as the schema for our CSS custom properties and for Elementor Global Colors naming. Skip: components, default base colours (Neutral/Zinc/Stone…), default radius and the stock "shadcn look"; always re-skin tokens per client.
## 8. Open questions
Latest commit date not visible. Elementor Global Colors cannot express foreground pairs natively — need a naming convention (e.g. "Primary / Primary-on").
