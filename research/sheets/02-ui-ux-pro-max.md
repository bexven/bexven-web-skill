# 02 — UI UX Pro Max
https://github.com/nextlevelbuilder/ui-ux-pro-max-skill · Claude Code skill + Python search CLI (npm installer `ui-ux-pro-max-cli`) · MIT · 151.2k stars (GitHub page, 2026-11-18) · commit f984fcd, 2026-11-18 (skill.json v2.15.0)

## 1. What it is
A "design intelligence" skill: a set of CSV databases (192 product types, each paired 1:1 with a colour palette and a reasoning rule; 80 styles, 51 active; 74 font pairings; 34 landing patterns; 130 UX guidelines; icons; GSAP presets; 22 stack guides) plus a Python BM25 search script. Claude runs the script with a product description and gets back a full design system (pattern, style, palette, fonts, effects, anti-patterns, checklist). There is also a paid "Premium" tier (brand, logo, CIP, banners, slides).

## 2. How it works
- Step 1: Claude pulls product type, audience, style words and the stack (detected from project files, never assumed) out of the request.
- Step 2: `search.py "<product> <industry> <keywords>" --design-system` runs five BM25 searches (product, style, colour, landing, typography). It then looks up the matching `ui-reasoning.csv` row, applies its JSON decision rules (e.g. `if_luxury -> style:liquid-glass`), and prints the design system. Selection is **deterministic**: the top hit wins (no randomness or seed), so the same query always gives the same result.
- Optional `--persist` writes `design-system/<slug>/MASTER.md` plus `pages/<page>.md` overrides. Page files override the master. It never overwrites without `--force`, and `--force` needs the user's approval.
- Optional `--tokens dtcg|css` (W3C token JSON or `:root` vars) and `--preview` (a static HTML preview).
- Optional "dials" 1–10: `--variance` (centred/minimal up to asymmetric/brutalist), `--motion` (attaches a GSAP snippet for subtle/standard/complex), `--density` (spacing scale 24–96 / 16–64 / 8–32px).
- Step 3/4: targeted `--domain ux|color|typography|landing|...` and `--stack html-tailwind|nextjs|...` lookups. Query contract: one intent, 2–5 terms, retry once. If a search returns nothing, say so and label any advice as fallback. Never invent results.
- Before delivery: a priority table (1 a11y to 10 charts) and a pre-delivery checklist in `references/pro-rules.md`.
- **Light/dark logic:** a dark theme is chosen only when the query asks for it or the chosen style is dark-first (10 of 89 styles have Preferred Mode=dark; the rest are "auto"). Otherwise the light palette from the product row is used. Dark palettes are derived from brand tokens, and contrast is checked. Category rows carry the mode stance: e.g. SaaS lists "Dark mode by default" as an anti-pattern, while Financial Dashboard lists "Light mode default" as one and Fintech says `if_dashboard -> mode:dark`. So dark is a per-category decision, used for dashboards, dev tools, OLED, entertainment and space tech. Marketing and service sites default to light.

## 3. Rules
- [process] For a new site, set one visual direction up front (style, palette, fonts, landing pattern, anti-patterns) and save it as a master file. Page-level files may override it.
- [process] Detect the stack from project files. Never fall back to a default stack.
- [process] If no data matches, say so and label the advice as a fallback. Never present invented guidance as data.
- [process] Before regenerating, read the existing design-system master. Never overwrite it silently.
- [brand] Pick the style, colours and fonts from the client's industry, not from habit (each industry has its own row).
- [brand] Each industry row lists "must-have" content (e.g. home services: emergency contact + certifications; legal: case results + credentials; construction: project portfolio).
- [colour] Use semantic tokens (primary/on-primary/secondary/accent/background/foreground/card/muted/border/destructive/ring). No raw hex in components.
- [colour] Every palette pairs each fill with an "on" colour, and accents are adjusted to reach 4.5:1 (notes say "Accent adjusted from #F97316").
- [colour] For trust industries (B2B, legal, banking, insurance, health, government, construction, logistics, senior care, agriculture), the anti-patterns list bans "AI purple/pink gradients".
- [colour] Choose light vs dark per category. Dark suits dashboards, finance data, dev tools and immersive products. Light suits service and marketing sites. Test both themes separately when both exist.
- [type] Base body 16px, line-height 1.5. No body text under 12px. Senior/accessibility audiences 18px+.
- [type] Pair fonts from a curated list, chosen by mood keywords. A Google Fonts catalogue (~1,900 families with popularity and trending rank) is there for individual picks.
- [layout] Build mobile-first. No horizontal scroll, no fixed-px container widths, never disable zoom. Use a 4/8px spacing rhythm.
- [space] Set density on purpose: spacious (24–96px) for marketing pages, dense (8–32px) for dashboards.
- [layout] Choose the landing section order from a named pattern (e.g. Hero > Problem > Solution > Testimonials > CTA). Put social proof before the CTA.
- [motion] Match timing to context. Exits run faster than entries. Never use one duration for everything. Never animate width/height. Honour reduced motion, which should show the static final state (e.g. turn off hero parallax).
- [motion] Hover micro-interactions take 150–300ms. Never use 0ms state changes.
- [components] Carousels and testimonial sliders need previous/next/pause controls and must stop rotating on focus or under reduced motion.
- [icon] Use SVG icons from one consistent family (Phosphor in its data). Never use emoji as icons.
- [icon] Hide decorative icons next to text with aria-hidden. Give icon-only controls an accessible name.
- [a11y] Text contrast 4.5:1 minimum (7:1 only for an explicit AAA target). Keep focus rings visible. Use alt text and keyboard navigation. Never use colour as the only signal.
- [a11y] Touch targets at least 44×44px with 8px+ spacing between them.
- [forms] Use visible labels (never placeholder-only), errors next to the field, helper text, and progressive disclosure. Allow paste and password managers.
- [perf] Use WebP/AVIF and lazy loading, and reserve image space so CLS stays under 0.1.
- [nav] Sticky nav must not cover content or keyboard focus. Show the active state. Use smooth anchor scroll.
- [copy] Testimonials should be real and verified, with photo, name and role. Lead-magnet forms ask only for the fields needed.
- [qa] Check at 375px and in landscape. Check with reduced motion and the largest text size. Measure the modal scrim against the real background.

## 4. AI tells / anti-patterns it bans
- "AI purple/pink gradients" for about 15 trust categories (B2B, healthcare, gov, fintech, legal, insurance, banking, logistics, agriculture, construction, senior care, clinics, pharmacy, civic portals).
- Emoji used as icons, mixed icon families, randomly mixing flat and skeuomorphic styles.
- Per-category bans such as "Static design + no video" (Micro SaaS), "Hidden contact info + no certifications" (home services), "Outdated design + hidden info" (church), "2D-only layouts + poor image quality" (construction).
- Removing focus rings, hover-only interactions, placeholder-only labels, gray-on-gray text, one animation duration for everything.
- It does NOT ban the generic-AI look as such. It **recommends** it in places (see below).

**Indigo #6366F1 / purple for AI:** yes. Product row 18 (AI/Chatbot Platform) gives the colour focus as "Neutral + AI Purple (#6366F1)", and its palette row uses #7C3AED violet + cyan. #6366F1 is the primary for Micro SaaS, Remote Work, Freelancer Platform, Digital Products and Fasting Timer, and appears 14 times in colors.csv in total. Church/Religious also gets violet #7C3AED + gold. So the skill steers AI and indie-SaaS products straight into the indigo/violet cliché while banning it for trust industries.

## 5. Data, assets and scripts it ships (and what they need: Node, Python, Chrome)
- `src/ui-ux-pro-max/data/*.csv` (mirrored in `.claude/skills/ui-ux-pro-max/data`, `cli/assets`):
  - products.csv: type, keywords, primary/secondary style, landing pattern, colour focus, considerations, rtl_level.
  - colors.csv: 18 semantic tokens per product.
  - ui-reasoning.csv: pattern, style priority, colour/type mood, effects, JSON decision rules, anti-patterns, severity.
  - styles.csv: 30 columns including best-for / do-not-use, light/dark support, a11y risk, CSS keywords, status.
  - typography.csv: pairing, Google URL, Tailwind config. Inter is the most used font (12 of 148 slots), then Space Grotesk (7) and Plus Jakarta Sans (6).
  - Also google-fonts.csv (1,934 rows), landing.csv, ux-guidelines.csv, icons.csv (Phosphor), motion.csv (GSAP), charts.csv, react-performance.csv, app-interface.csv, stacks/*.csv (22).
- Scripts: `search.py` (CLI entry), `core.py` (BM25 engine, query rewrite, threshold), `design_system.py` (aggregation, reasoning, light/dark resolution, contrast maths, persistence, tokens), `preview.py` (HTML preview), `reasoning_contract.py`, `validate_data.py`. These need **Python 3 with no extra dependencies**. The installer is Node (`npx ui-ux-pro-max-cli init`). No Chrome needed.
- Extra skills in `.claude/skills/` (brand, design, design-system, slides, banner-design, ui-styling) with logo/CIP/slide CSVs. These are tied to the premium pitch and were not read here.
- Niche coverage for Bexven:
  - **Funeral homes: no row** (no funeral, memorial, grief or cemetery match in any CSV). The nearest rows are Church/Religious (violet + gold, Soft UI), Senior Care (calm blue + green, large text, WCAG AAA) and Legal (navy + gold, trust & authority).
  - **Metal fabrication / manufacturing: no row.** The nearest is Construction/Architecture: Minimalism/Swiss + 3D, slate #64748B + safety orange #EA580C, "blueprint aesthetic", must have a project portfolio. Home Services (blue #1E40AF + orange #EA580C) and Inventory (industrial slate + green) are also close.
  - Construction and Home Services share the same orange accent, so every trades site gets grey/blue + safety orange.

## 6. Area
design (primary), tooling, QA/a11y; some development (stack guides).

## 7. Take / skip
- TAKE: the idea of an industry-to-direction table with must-have content per niche ("credentials", "emergency contact", "project portfolio"). Build our own rows for funeral homes, metal fab, etc.
- TAKE: a semantic token schema with paired on-colours, plus contrast-adjusted accents (this matches tokens in WP/Elementor global colours).
- TAKE: the master + page-override design-system file (MASTER.md), persisted per client. It fits the Vercel-redeploy-to-WP handoff.
- TAKE: the density/variance/motion dials as explicit knobs, an honest "no match means fallback" rule, the accessibility and pre-delivery checklist, and carousel/reduced-motion rules.
- TAKE (adapted): per-category light/dark decisions instead of a global default.
- SKIP: deterministic top-hit selection. The same niche always yields the same palette and font, so two funeral homes or two fab shops would look identical, which is the opposite of our goal. We need seeded variation inside a niche.
- SKIP: its palettes and font list as defaults. They are Tailwind-stock hexes (#2563EB, #6366F1, #EA580C, slate) and lean on Inter, Space Grotesk, Plus Jakarta Sans, Poppins and Playfair+Inter. These are exactly the "AI-made" tells we want to avoid.
- SKIP: the indigo/violet recommendation for AI/SaaS/church, the glassmorphism/aurora/liquid-glass leanings, and the 3D/hyperrealism suggestion for construction (heavy, off-brand for small shops).
- SKIP: running its Python CLI or installing the npm package. We want the knowledge in our own skill, not a dependency. The premium/brand sub-skills are an upsell.

## 8. Open questions
- `references/quick-reference.md` (266 lines, all 130 rules) was only skimmed through the SKILL.md table and not read in full. It might be worth one pass for type and spacing numbers.
- The `--variance` dial biases style choice but is still deterministic. Does it change palettes or fonts? (design_system.py was not read in depth.)
- The google-fonts.csv popularity/trending ranks could drive a "avoid top-N popular fonts" rule in our skill.
- SUGGESTED: impeccable (pbakaus) - https://github.com/pbakaus/impeccable - already cloned in sources. It is a design/critique skill with an anti-AI-slop focus and makes a good contrast to this one.
