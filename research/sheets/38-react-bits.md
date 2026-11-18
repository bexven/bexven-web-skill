# 38 — React Bits
https://reactbits.dev · Animated React components, text effects and backgrounds · MIT + Commons Clause ("free for personal and commercial use", but no selling the components themselves); a "Pro" tier is linked, details not shown · 52.3k stars (github.com/DavidHDev/react-bits) · read 2026-11-18

## 1. What it is
215+ creative components in five categories (text animations, animations, components, backgrounds, micro-interactions), each in JS/TS × plain CSS/Tailwind variants. Installed as owned source (copy, shadcn CLI or jsrepo). React-only; not usable directly in Bexven's static HTML or Elementor.
## 2. How it works
Copy source or CLI install; many backgrounds use WebGL/canvas (e.g. via three/ogl), text effects use GSAP or Motion.
## 3. Rules
n/a (gallery).
## 4. AI tells / anti-patterns it bans
Bans none. Its popular pieces (known from the library, not named on the fetched homepage) have become vibe-coded tells: split/blur/shiny/gradient text reveals, decrypted text, aurora/silk/iridescence/liquid-chrome WebGL backgrounds, particles/hyperspeed, magnet buttons, click spark, splash cursor, tilted cards.
## 5. Data, assets and scripts it ships
React source; deps vary (GSAP, Motion, three/ogl). Needs Node toolchain.
## 6. Area
motion
## 7. Take / skip
Skip as defaults and ban the WebGL hero backgrounds and per-letter text reveals on headlines (also perf/a11y cost). Because CSS variants exist, it is the easiest of the four to read for mechanism; at most borrow one small micro-interaction idea and rewrite it in vanilla CSS/JS with reduced-motion fallback. Commons Clause: never repackage its code into a sellable template/theme.
## 8. Open questions
Pro tier contents/price not shown. Full Commons Clause text not read (LICENSE.md).
