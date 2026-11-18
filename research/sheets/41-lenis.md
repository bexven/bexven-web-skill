# 41 — Lenis
https://github.com/darkroomengineering/lenis · Repo (JS smooth-scroll library) · MIT · Stars 17.4k · Commit bd89165, 2026-11-13 (v1.3.27)

## 1. What it is
A lightweight smooth-scroll library from darkroom.engineering. It interpolates ("lerps") the scroll position on top of the browser's native scroll. Its MANIFESTO says the real purpose was keeping WebGL scenes and the DOM in sync while scrolling; smooth wheel scrolling came as a side effect. Packages: core `lenis`, plus `lenis/react`, `lenis/vue` and `lenis/snap` (because CSS scroll-snap isn't supported).

## 2. How it works
- `new Lenis({ autoRaf: true })`, or drive it yourself with `lenis.raf(time)` (e.g. from `gsap.ticker`).
- It intercepts wheel input (and touch input only if `syncTouch`) and eases `window` scroll toward the target. Because the real document still scrolls, `position: sticky`, find-in-page and scrollbars keep working, unlike older transform-based "virtual scroll" libraries.
- Needs its CSS (`lenis/dist/lenis.css`): `height:auto` on html/body, `overflow: clip` when stopped, `overscroll-behavior: contain` on opted-out nested areas, and iframes made non-interactive while smoothing.
- GSAP ScrollTrigger: `lenis.on('scroll', ScrollTrigger.update)`, add `lenis.raf` to `gsap.ticker`, and call `gsap.ticker.lagSmoothing(0)`.
- CDN: unpkg `lenis@1.3.27/dist/lenis.min.js` + `lenis.css` (README "no-code" snippet).

## 3. Rules
- [motion] Default for Bexven local-business sites is NO Lenis. Plain native scroll plus `scroll-behavior: smooth` in CSS (inside a no-preference reduced-motion query) for anchor jumps is enough.
- [motion] Use Lenis only when the page truly has scroll-driven storytelling: pinned GSAP ScrollTrigger sequences, parallax layers, WebGL/canvas synced to scroll. Its job there is keeping things in sync, not "feel".
- [motion] If used, stay near the defaults (`lerp` 0.1, or `duration` about 1.0–1.2). Don't go heavier: a long glide feels like the page is lagging behind input.
- [a11y] Keep `respectReducedMotion: true` (the default). With reduce set, lerp becomes 1 and scrollTo/anchor jumps are instant. Never turn it off.
- [a11y] Keep `syncTouch: false` (default) so phones keep native touch momentum. Hijacking touch is unstable on iOS < 16 and annoys users.
- [nav] Set `anchors: true` (with an `offset` for a sticky header), otherwise in-page anchor links break while Lenis runs. Check skip-links and focus still move correctly after the jump.
- [components] Nested scrollers (menus, modals, cookie banners, maps, chat widgets, code blocks): add `data-lenis-prevent`, or use `prevent: (node) => ...`. Use `allowNestedScroll: true` only on light pages, because it walks the DOM on every scroll event.
- [components] Call `lenis.stop()` when a modal or mobile menu opens and `lenis.start()` when it closes, or use `autoToggle` (needs modern browsers + the CSS).
- [code] Always include lenis.css. Without it you get a stuck page, wrong height, or nested areas leaking scroll.
- [perf] Smoothing is capped at 60fps on Safari (30fps on low power). Wheel smoothing stops over iframes (YouTube/Maps embeds). Fixed elements can lag on older Mac Safari. Test on a real Mac + iPhone.
- [perf] Don't combine Lenis with CSS scroll-snap; use `lenis/snap` or skip snapping.
- [wp] On WordPress/Elementor, avoid it by default: it fights Elementor popups, sticky sections, off-canvas menus and third-party widgets. If needed, enqueue the local file in the child theme's footer and test every popup/menu.
- [qa] QA checklist when Lenis is on: keyboard scrolling (Space/PgDn/arrows), anchor links, browser back/forward scroll restore, find-in-page, reduced motion on, nested scrollers, embeds, mobile.

## 4. AI tells / anti-patterns it bans
n/a (library). Our own tell: "Awwwards-style" smooth scroll + fade-ups bolted onto a plumber/funeral-home site. It reads as template-y and hurts usability for older audiences.

## 5. Data, assets and scripts it ships
JS (small; bundlephobia badge, exact size not checked) + lenis.css. React/Vue wrappers, snap plugin, a playground. No server runtime; browser only. Build uses bun/vite (not run).

## 6. Area
motion / development / a11y

## 7. Take / skip
Take: the a11y-safe config (reduced motion on, syncTouch off, anchors on, nested-scroll opt-outs, stop on modal) and the GSAP ticker integration for the rare immersive build (e.g. premium metal-fab portfolio with pinned sequences). Skip: using it as default "polish" on local-business sites, touch hijacking, heavy lerp, `respectReducedMotion: false`.

## 8. Open questions
- Exact minzipped size not verified (bundlephobia not fetched).
- Elementor compatibility only inferred, not tested.
