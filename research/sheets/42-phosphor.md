# 42 — Phosphor Icons
https://phosphoricons.com · Website / icon library · MIT ("MIT © Phosphor Icons") · 7.8k stars (phosphor-icons/homepage repo) · read 2026-11-18

## 1. What it is
Flexible open icon family (README says "1,248 icons and counting"; base glyph count, multiplied across weights) in six weights: Thin, Light, Regular, Bold, Fill, Duotone. Drawn on a 16px design grid, so it scales cleanly.
## 2. How it works
Get assets as SVG (site download / `@phosphor-icons/core` npm catalog), as a webfont (`@phosphor-icons/web`, one stylesheet per weight, `<i class="ph ph-cube">`), or as framework packages (`@phosphor-icons/react`, Vue, Flutter and others). MIT: free commercial use, keep the licence notice when you redistribute the package, no visible credit needed on the site.
## 3. Rules
- [icon] Inline the SVGs we use (copied from core); don't load the full webfont (one CSS file per weight) for 6 icons on a static page
- [icon] Pick ONE weight per site to match the type weight (Thin/Light for elegant serif sites such as funeral homes, Bold/Fill for industrial/fab shops); Duotone only as a deliberate brand accent
- [icon] One icon family per site; never mix Phosphor with Tabler/Lucide/etc. in the same build
- [a11y] Decorative icons get `aria-hidden="true"`; icon-only buttons need an accessible label
- [wp] In Elementor builds, upload the same SVGs (sanitised) as custom icons, not a plugin's icon pack
## 4. AI tells / anti-patterns it bans
n/a (not a design guide). Our ban: no grids of identical icon-in-tinted-circle feature cards; icons should be functional (nav, contact, specs), not decoration filling every card.
## 5. Data, assets and scripts it ships
SVG catalog + webfonts via npm/CDN; nothing to run. Node only if you use the npm packages.
## 6. Area
design / tooling
## 7. Take / skip
Take: Phosphor as a strong default when a site needs a warmer/softer look than Tabler, because its weight range lets icons match the typography. Skip: the webfont delivery and Duotone-everywhere looks (a common "template" tell).
## 8. Open questions
phosphoricons.com is a JS app; WebFetch only got the title, so details come from the GitHub homepage README. The 1,248 count may be out of date; check `@phosphor-icons/core` for the current number. SUGGESTED: phosphor-icons/core - https://github.com/phosphor-icons/core - the source of the raw SVGs and current version.
