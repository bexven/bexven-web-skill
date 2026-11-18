# 39 — GSAP
https://gsap.com · Website (JS animation library) · GSAP "Standard No Charge" licence (Webflow-owned; not OSI open source) · Stars n/a (website) · Read 2026-11-18 (licence effective 2025-04-30, modified 2025-05-30; docs show v3.15)

## 1. What it is
Mature JS animation library (tweens, timelines) with plugins such as ScrollTrigger, SplitText, MorphSVG. Since Webflow bought it, all plugins (including the former paid "bonus" ones) are free, commercial use included.
## 2. How it works
Load core + plugins via npm (`npm install gsap`), jsDelivr CDN, or the self-host zip (/minified for script tags, /ESM for bundlers). Register plugins with `gsap.registerPlugin(...)` before use.
## 3. Rules
- [code] Licence: free for any website, web app or client site, including Bexven's. The ban is on *tools*: you need Webflow's written consent to use GSAP inside a no-code/visual animation builder that "competes with Webflow's" animation features. Also no reverse engineering for a competing product and no removing its notices. Webflow can end the licence if you break these terms.
- [wp] FAQ: WordPress plugins aren't automatically banned, and AI-written GSAP code is fine. So never package GSAP into a reusable Elementor/WP visual animation-builder plugin without checking with Webflow first.
- [perf] Static Vercel pages: self-host the minified files or pin an exact jsDelivr version (no `@latest`). Load only the plugins you use and add `defer`.
- [wp] WordPress: in a child theme's functions.php (never the parent theme), `wp_enqueue_script('gsap-js', <core URL>, [], <ver>, true)`. Then enqueue ScrollTrigger and your app.js with `['gsap-js']` as the dependency, loaded in the footer. Prefer local copies in the theme over the CDN.
- [a11y] Wrap effects in `gsap.matchMedia()` with a `(prefers-reduced-motion: no-preference)` condition.
## 4. AI tells / anti-patterns it bans
n/a (library). Our own tell to avoid: fade-up-on-scroll on every section.
## 5. Data, assets and scripts it ships
JS files only (core + separate plugin files; size not checked). Browser only.
## 6. Area
motion / development
## 7. Take / skip
Take: GSAP as the default for anything beyond CSS (timelines, ScrollTrigger pinning, SplitText headings), used sparingly. Cross-reference sheet 13 (gsap-skills). Skip: CDN `@latest`, and any plan to build a product that sells GSAP-powered visual animation editing.
## 8. Open questions
- The WordPress guide's CDN version string was hidden in the fetched text. Pin the current 3.x when building.
- Elementor Pro's built-in Motion Effects may make GSAP unnecessary for simple WP builds. Decide per project.
