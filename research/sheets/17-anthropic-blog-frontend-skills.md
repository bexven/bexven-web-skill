# 17 — Anthropic, Improving frontend design through Skills
https://claude.com/blog/improving-frontend-design-through-skills · Article (blog, "Best practices") · License: none stated (blog © Anthropic; linked repos carry their own licences) · Stars: n/a · Published 2025-11-12, read 2026-11-18

## 1. What it is
A blog post by Anthropic's Applied AI team (Rajasekaran, Wei, Bricken) on why Claude's default frontends look generic, and how a short skill (about 400 tokens) steers it toward distinctive design. It is the reasoning behind the `frontend-design` plugin/skill and the frontend-aesthetics cookbook notebook. It also introduces the `web-artifacts-builder` skill.

## 2. How it works
- Problem: "distributional convergence". Without guidance the model picks the most likely options from web training data: Inter, purple gradient on white, little or no motion. The result is the "AI slop" look, which weakens brand identity and makes the output easy to spot as AI-made.
- Why a skill and not a system prompt: detailed design guidance is long. Keeping it in every prompt wastes context on tasks that aren't design work, and extra context can hurt performance. A skill is a markdown file that loads only when it's needed.
- How the prompt is laid out: (1) a short framing of the "on-distribution" problem, (2) guidance for each dimension (typography, colour/theme, motion, backgrounds), (3) anti-convergence reminders at the end.
- "Prompt altitude": aim between hard-coded rules (exact hex codes) and vague direction ("make it nice"). Name concrete alternatives, but let the model choose.
- Overall method they propose: find the convergent defaults, give concrete alternatives, pitch them at the right altitude, package the result as a reusable skill. Teams can encode their own design system the same way.
- `web-artifacts-builder`: ships scripts that scaffold a multi-file React + Tailwind + shadcn/ui project, then bundle it with Parcel into a single HTML file. That keeps the artifact single-file while saving tokens.

## 3. Rules
- [type] Don't default to Inter, Roboto, Open Sans, Lato, Arial or system fonts
- [type] Choose by mood: code (JetBrains Mono, Fira Code, Space Grotesk), editorial (Playfair Display, Crimson Pro), technical (IBM Plex, Source Sans 3), distinctive (Bricolage Grotesque, Newsreader)
- [type] Pair for high contrast: display + mono, serif + geometric sans, or one variable font across extreme weights
- [type] Use extreme weights (100/200 against 800/900), not 400 against 600
- [type] Make size jumps of 3x or more between levels, not 1.5x
- [type] Pick one distinctive face and use it decisively; load it from Google Fonts
- [colour] Commit to one cohesive aesthetic and define it as CSS variables
- [colour] A dominant colour with sharp accents beats a timid, evenly spread palette
- [colour] Take palettes from IDE themes and cultural or historical aesthetics, not generic SaaS
- [colour] Avoid purple gradients on white
- [brand] A named theme (their example: RPG, with parchment texture, ornate borders, medieval serif headings) can set the whole visual system at once
- [motion] Put motion into one orchestrated page load with staggered reveals (animation-delay), not scattered micro-interactions
- [motion] Use CSS-only animation for HTML; use the Motion library in React when it's available
- [layout] Avoid predictable layouts and stock component patterns; design for the specific context
- [image] Build atmosphere behind content: layered gradients, geometric patterns, effects that fit the theme. Not flat solid fills
- [process] Watch for new convergence: even a recommended font becomes the new default (Claude overused Space Grotesk), so finish with a reminder to vary choices
- [process] Keep the design guidance compact and load it on demand, not in an always-on prompt
- [tooling] For complex single-file deliverables, scaffold a multi-file project and bundle it at the end

## 4. AI tells / anti-patterns it bans
Inter, Roboto, Open Sans, Lato, Arial and system fonts; purple gradient on white; flat solid backgrounds; timid, evenly spread palettes; small weight and size steps; scattered micro-interactions or no motion; cookie-cutter layouts and components; repeating one "safe" pick across every output (Space Grotesk).

## 5. Data, assets and scripts it ships (and what they need: Node, Python, Chrome)
The article itself ships nothing. It links: the anthropics/skills repo (web-artifacts-builder: scaffold + Parcel bundling scripts, which need Node), skill-creator, the claude-code `plugins/frontend-design` plugin, and claude-cookbooks `prompting_for_frontend_aesthetics.ipynb` (Python notebook).

## 6. Area
design (typography/colour/motion), with a process/tooling angle on how to structure skills

## 7. Take / skip
- Take: the diagnosis and the framing. Bexven's "doesn't look AI-made" goal is the same problem. Take the high-contrast type rules (extreme weights, 3x steps), dominant colour + sharp accent, one orchestrated load animation, atmospheric backgrounds, and the explicit banned-defaults list.
- Take: the anti-convergence lesson. Any font or palette list we ship will become the new default. For niche variety (two funeral homes must not match), rotate or derive choices per client (brand, locale, era, materials) instead of shipping a fixed shortlist.
- Take: keep SKILL.md short and at the right altitude. Put longer references (font pairings per niche, Elementor specifics) in on-demand files.
- Skip/adapt: their example fonts are already becoming tells (Space Grotesk, Playfair, JetBrains Mono on non-dev sites). Treat them as examples only.
- Skip/adapt: "commit boldly / dark theme / RPG" suits demos. Local-service clients (funeral homes, fabricators) need restraint, readability and trust, so boldness should come from type and colour decisions, not from gimmicks.
- Adapt: motion advice must respect prefers-reduced-motion, and in Elementor builds should use native entrance animations or light CSS, not the React Motion library.
- Skip: web-artifacts-builder (React/shadcn single-file artifacts) doesn't fit our static HTML / WordPress pipeline, though its "scaffold, then bundle" idea is sound.

## 8. Open questions
- No measured results: only qualitative before/after screenshots (SaaS landing, blog, admin dashboard; whiteboard and task-manager apps for web-artifacts-builder). No metrics or user testing.
- Licence of the linked frontend-design plugin and cookbook not checked here. Verify before reusing any wording.
- SUGGESTED: Anthropic cookbook "Prompting for frontend aesthetics" - https://github.com/anthropics/claude-cookbooks (prompting_for_frontend_aesthetics.ipynb) - contains the full ~400-token prompt and comparisons
- SUGGESTED: Anthropic "Effective context engineering for AI agents" - anthropic.com/engineering - source of the "prompt altitude" idea cited here
