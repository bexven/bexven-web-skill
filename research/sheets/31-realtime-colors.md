# 31 — Realtime Colors
https://www.realtimecolors.com · Website (human tool, by Juxtopposed) · Site code CC BY-NC-ND; generated colours/fonts free for commercial use (FAQ) · Stars n/a · Read 2026-11-18

## 1. What it is
Free web tool that previews a 5-colour palette and a heading/body font pair on a realistic sample landing page, live, in light and dark mode.
## 2. How it works
Pick or randomize (Spacebar) colours by harmony (mono/analogous/complementary/split/triadic/tetradic); built-in WCAG AA/AAA contrast checker; export to CSS, Tailwind, SCSS, shades, gradients, plus presets (shadcn, DaisyUI, MUI, Chakra); HEX/RGB/HSL/OKLCH output.
## 3. Rules
- [colour] Five-role model: text + background (neutrals), primary (main CTAs/sections), secondary (lesser buttons, info cards), accent (highlights, links, boxes)
- [a11y] Check every text/background pair against WCAG AA (4.5:1 body) before shipping; AAA where feasible
- [colour] Design light and dark variants together, not dark as an afterthought
## 4. AI tells / anti-patterns it bans
n/a (randomize + harmony presets can itself produce generic results)
## 5. Data, assets and scripts it ships
None usable by an agent; browser UI only (also a Figma plugin). No public API.
## 6. Area
design / tooling
## 7. Take / skip
Take: the 5-role token naming (text/bg/primary/secondary/accent) as a minimal palette contract, and "preview on a real layout" as a human QA step to show clients. Skip: as an agent method — it is a manual GUI; harmony-randomize is the opposite of deliberate, niche-driven colour choices.
## 8. Open questions
Whether the export format can be mirrored in our token file (likely: plain CSS vars). Docs pages (/docs/selecting-colors) not read.
