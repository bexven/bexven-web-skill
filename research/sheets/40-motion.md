# 40 — Motion
https://motion.dev · Website (JS animation library, formerly Framer Motion) · MIT (library); Motion+ is paid · Stars 35.3k (github.com/motiondivision/motion) · Read 2026-11-18

## 1. What it is
Animation library for React, Vue and plain JavaScript. The core library is MIT and free. Motion+ is a paid add-on: $399 one-time per solo developer, billed yearly per seat for teams. It adds 520+ example sources, tutorials, premium UI components/sections, an AI kit/MCP, and the Motion Studio visual editor. The library does not need Motion+.
## 2. How it works
Vanilla: `import { animate, inView, scroll } from "motion"`. No CDN build step is needed: use `cdn.jsdelivr.net/npm/motion@<ver>/+esm` in a `<script type="module">`, or the legacy `dist/motion.js` with a global `Motion`. It uses WAAPI where it can (hardware accelerated).
## 3. Rules
- [motion] Static pages: use vanilla `animate()` for small effects. It needs no React. The "mini" animate starts at about 3.2kb, so it is far lighter than GSAP for simple reveals.
- [motion] Use `inView()` for enter-viewport reveals and `scroll()` for scroll-linked values, instead of hand-written IntersectionObserver code.
- [perf] Pin an exact version (the docs themselves warn against `@latest`). Self-host the ESM file on Vercel.
- [a11y] Check reduced-motion yourself: wrap calls in a `matchMedia('(prefers-reduced-motion: reduce)')` guard (the docs page we read didn't say how it handles this).
- [code] Never copy Motion+ example or component source into client work unless Bexven holds a licence.
## 4. AI tells / anti-patterns it bans
n/a
## 5. Data, assets and scripts it ships
npm package / ESM files. Browser only.
## 6. Area
motion / development
## 7. Take / skip
Take: the lightweight option for static redesign pages (micro-interactions, one or two reveals). Skip: Motion+ (paid; examples push the same look). For WordPress builds use GSAP or Elementor's own effects instead, since Motion's docs focus on React.
## 8. Open questions
- Exact sizes of hybrid animate, inView and scroll weren't on the pages we fetched. Check bundlephobia if it matters.
- Whether the vanilla API respects reduced motion by itself wasn't confirmed.
