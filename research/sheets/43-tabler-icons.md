# 43 — Tabler Icons
https://tabler.io/icons · Website / icon library · MIT · 22.7k stars (tabler/tabler-icons) · read 2026-11-18 (CDN example pins 3.46.0)

## 1. What it is
Large free icon set: 6,545 icons (5,491 outline, 1,054 filled) on a 24×24 grid with a 2px stroke by default. You can change stroke width, size and colour.
## 2. How it works
Get them as SVG (`@tabler/icons` npm, the site, or the SVG sprite), as a webfont (`@tabler/icons-webfont`), as framework packages (React, Vue, Svelte, Solid, Preact, Angular, Astro, React Native), or as PNG/PDF/EPS. The site says it is MIT, free for commercial use and "no attribution required".
## 3. Rules
- [icon] Inline only the SVGs we use. Set `stroke-width` to match the body text weight (1.25–1.5 next to light or serif type, 2 next to bold sans)
- [icon] One family per site. Use outline OR filled for a given job; don't mix them at random
- [icon] Use `currentColor` so icons take the text colour and work with dark sections
- [a11y] Use `aria-hidden` on decorative icons and labels on icon-only controls
- [perf] Don't load the webfont or sprite for a few icons
## 4. AI tells / anti-patterns it bans
n/a. Our ban: Tabler's 2px outline look shows up in a lot of SaaS and AI-generated pages. Avoid icon-in-circle feature grids and a checkmark list on every section.
## 5. Data, assets and scripts it ships
SVG/webfont/PNG/PDF/EPS packages on npm and CDN. Nothing to run.
## 6. Area
design / tooling
## 7. Take / skip
Take: the widest coverage for niche items (tools, machinery, urns and similar), so it suits metal fabrication or trades sites, and its adjustable stroke lets icons match the type. Skip: the default 2px stroke left unchanged, and using it as the house icon set on every site, which would make our sites look alike.
## 8. Open questions
The exact current release wasn't stated on GitHub (empty Releases section). Check it on npm before pinning.
