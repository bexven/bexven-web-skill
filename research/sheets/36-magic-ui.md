# 36 — Magic UI
https://magicui.design · Animated component library (shadcn companion) · MIT (free tier); Magic UI Pro = paid blocks/templates, price not shown · 23.4k stars (github.com/magicuidesign/magicui) · read 2026-11-18

## 1. What it is
150+ free animated React components/effects for landing pages, installed shadcn-style; Pro adds 50+ landing blocks and templates. Stack: React + TypeScript + Tailwind + Motion (Framer Motion). Not usable directly in Bexven's static HTML or Elementor builds.
## 2. How it works
Copy/CLI install into a Next/React project; effects driven by Motion and Tailwind keyframes.
## 3. Rules
n/a (gallery, not a guideline source).
## 4. AI tells / anti-patterns it bans
Bans none. Its signature effects (known from the library; homepage itself only named "Dither Field" as new) are now strong AI/template tells: shimmer button, border beam, animated beam connectors, marquee logo strip, bento grid, globe, particles, animated gradient text, number ticker, dot/grid pattern backgrounds.
## 5. Data, assets and scripts it ships
React/TS source, Node CLI; Motion dependency.
## 6. Area
motion / components
## 7. Take / skip
Skip as defaults: list these effects in the skill's "AI tells" ban list (especially shimmer/border-beam buttons, logo marquee under hero, bento feature grid, gradient headline text). At most borrow a single interaction idea when it serves the client's story, re-implemented in plain CSS/JS (CSS keyframes, IntersectionObserver) with prefers-reduced-motion respected.
## 8. Open questions
Pro pricing/licence terms not on homepage (not read). Component names above not confirmed on the fetched page.
