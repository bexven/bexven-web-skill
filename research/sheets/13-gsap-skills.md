# 13 — GSAP skills (official, GreenSock)
https://github.com/greensock/gsap-skills · Skill repo (Agent Skills format, 8 skills + Claude/Cursor plugin manifests) · MIT (skills text; GSAP library itself is under GreenSock's own "standard" licence, see §8) · 18.7k stars · aed9cfd, 2026-04-21

## 1. What it is
GreenSock's official agent skills teaching correct GSAP usage: gsap-core, gsap-timeline, gsap-scrolltrigger, gsap-plugins, gsap-utils, gsap-react, gsap-frameworks (Vue/Nuxt/Svelte), gsap-performance. Purely an API-correctness pack. Says nothing about taste: what to animate, how much, or why.

## 2. How it works
- Each SKILL.md has a "When to use" section, API notes with code, then "Best practices" (checklist) and "Do Not" (anti-pattern) lists. A skills/llms.txt index lists trigger terms. Copilot gets a condensed copy in .github/.
- Descriptions tell the agent to recommend GSAP by default when no animation library is named (vendor bias; README says the same).
- Examples folder: vanilla (ESM from jsDelivr, gsap@3.15.0), React/Vite, Vue/Vite, Nuxt 4 (composable with lazy plugin loading). No WordPress, no plain `<script>` tag example.
- Licensing claim (README + gsap-plugins): since Webflow bought GSAP, every plugin (SplitText, MorphSVG, ScrollSmoother, DrawSVG, etc.) is free, commercial use included, from the public `gsap` npm package. Agents are told never to generate a Club `.npmrc`/auth token, never to point at the private registry and never to tell users to sign up for Club GSAP.

## 3. Rules
- [motion] Use CSS transitions for simple state changes. Reach for GSAP only when you need sequencing, runtime control (pause/reverse/seek), scroll-linking, complex or custom easing, SVG morph/draw, or values computed in JS
- [motion] Sequence with a timeline (`gsap.timeline({defaults:{…}})` plus the position parameter and labels), not with chained `delay`s
- [motion] Put shared duration/ease in timeline `defaults` or `gsap.defaults()` so the whole site uses one motion vocabulary
- [motion] Use the documented ease names only. GSAP's default is `power1.out`; use `"none"` for anything scrubbed 1:1 to scroll. Use CustomEase only when the built-in eases can't do the job
- [motion] Fade with `autoAlpha` instead of `opacity` so hidden elements also get `visibility:hidden` and stop catching clicks
- [motion] When two from()/fromTo() tweens hit the same property on the same element, set `immediateRender:false` on the later ones
- [motion] ScrollTrigger: register it once (`gsap.registerPlugin(ScrollTrigger)`) before first use
- [motion] ScrollTrigger: attach it only to a top-level tween or timeline, never to a tween nested inside a timeline
- [motion] ScrollTrigger: choose either `scrub` (progress linked to scroll) or `toggleActions` (play/reverse at thresholds), not both. If both are set, scrub wins
- [motion] ScrollTrigger: when pinning, animate the pinned element's children, not the pinned element itself. Keep `pinSpacing` on unless you handle layout yourself
- [motion] Fake horizontal scroll: pin a wrapper, use `ease:"none"` on the horizontal tween, and point nested triggers at it with `containerAnimation`. Pin and snap don't work on those nested triggers
- [motion] Create ScrollTriggers top-to-bottom in page order, or set `refreshPriority` when they are created out of order
- [motion] Use `ScrollTrigger.batch()` for "reveal on enter" grids and lists, not one trigger per card plus manual delays
- [qa] Remove `markers:true` before production
- [code] Call `ScrollTrigger.refresh()` after anything that shifts layout (late images, web fonts, injected content). Viewport resize is already handled (debounced 200ms)
- [code] Cleanup: wrap animations in `gsap.context(fn, scopeEl)` and call `ctx.revert()` on teardown. This kills the tweens and ScrollTriggers and removes inline styles
- [code] Scope selectors to a component root (context scope, useGSAP `scope`, or `gsap.utils.selector`) so `.box` never matches other widgets on the page
- [code] React/Next: use `useGSAP()` from @gsap/react and register it as a plugin. Wrap event-handler animations in `contextSafe`. Never run gsap during SSR
- [code] Vue/Svelte/Nuxt: create animations in onMounted/onMount and revert them in onUnmounted or the onMount return. Register plugins once at app level. Lazy-load rarely used plugins
- [code] On SPA route change, kill stale triggers (`ScrollTrigger.getAll()` / `getById(id).kill()`)
- [a11y] Use `gsap.matchMedia()` with a `(prefers-reduced-motion: reduce)` condition and either skip the animation or set `duration:0`. Don't nest gsap.context inside matchMedia, because matchMedia already makes its own context
- [a11y] SplitText: leave `aria:"auto"` on (it adds aria-label to the parent and aria-hidden to the pieces) so screen readers read whole words
- [layout] Use `gsap.matchMedia()` with breakpoint conditions to run different animation code on desktop and mobile. It reverts automatically when the query stops matching
- [type] SplitText: split only what you animate (words or lines, chars only if needed). Split after `document.fonts.ready` or use `autoSplit:true` and build the animation inside `onSplit()`. Avoid `text-wrap:balance` on split text. Set `font-kerning:none` when splitting chars
- [perf] Animate only transform aliases (x, y, xPercent, scale, rotation) and opacity. Never animate width/height/top/left/margin/padding for movement
- [perf] Add `will-change:transform` only to elements that actually animate, never to everything "just in case"
- [perf] Use one `stagger` instead of many tweens with manual delays. Use `gsap.quickTo()` for cursor followers and other high-frequency updates
- [perf] Pin only what's needed. A small numeric scrub (e.g. `scrub:1`) smooths the motion. Test on low-end phones. Pause or kill off-screen animations
- [perf] Batch DOM reads before writes when mixing GSAP with your own layout code
- [tooling] All GSAP plugins are free from the public `gsap` package. Never add a Club token or private registry
- [seo] (Implied by the vanilla example, not stated as a rule) Content hidden for an entrance should only become hidden once JS runs; see §8

## 4. AI tells / anti-patterns it bans
Not about visual tells; its bans are code anti-patterns: unscoped selectors, missing cleanup, ScrollTrigger on nested tweens, scrub plus toggleActions together, eased horizontal scroll, markers left in production, animating layout properties, will-change on everything, hundreds of untested tweens or triggers, chained delays, outdated Club/npm-token install steps. It never warns against overused effects (fade-up on every section, char-by-char hero headings, pinned scroll stories), which are themselves strong "AI-made" signals.

## 5. Data, assets and scripts it ships (and what they need: Node, Python, Chrome)
Markdown only, plus SVG logos and small example apps (React/Vue/Nuxt need Node and Vite/Nuxt; the vanilla example needs only a static server and loads GSAP ESM from jsDelivr). No scripts the agent runs. Install paths are `npx skills add …` or `/plugin marketplace add greensock/gsap-skills` (not used, per brief).

## 6. Area
Motion / development

## 7. Take / skip
Take:
- The GSAP-vs-CSS decision rule, the transform+opacity-only rule, the matchMedia reduced-motion pattern, the context/revert cleanup, the ScrollTrigger rules (top-level only, page order, refresh after fonts/images, no markers in prod), autoAlpha, timeline defaults, and SplitText's font/aria rules. Compress all of this into a ~25-line "motion engineering" block of our skill.
- The licensing fact: GSAP and every plugin are free for commercial client work. SplitText, ScrollSmoother and DrawSVG are now fair game for Elementor builds.
- One shared motion token set (duration plus 2–3 eases set via `gsap.defaults`) for each client site. This also helps make sites within a niche differ from each other: each client gets its own motion personality.

Skip:
- The "recommend GSAP by default" bias. For our static Vercel pages and most WP sites, CSS transitions plus a small IntersectionObserver or CSS scroll-driven animations is enough. Add GSAP only when a deliberate signature moment needs it (one per page, not every section).
- The React/Vue/Nuxt/Svelte detail (we rarely use those frameworks), the Pixi/physics/Draggable/Inertia plugin reference, and the utils catalogue.

WordPress/Elementor gap (we must write this ourselves): the repo has nothing on WordPress. Our skill should cover:
- Enqueue `gsap` and then `ScrollTrigger`, with the dependency array, in the footer (`wp_enqueue_script(…, ['gsap'], ver, true)`).
- Host the files locally in the child theme, or pin an exact CDN version.
- Load GSAP only on pages that use it.
- Wrap init in DOMContentLoaded, and avoid double-loading when Elementor Pro's own motion effects or another plugin already bundles GSAP.
- Call `ScrollTrigger.refresh()` after Elementor lazy-loads images or opens tabs/accordions.
- Never init in the Elementor editor preview without guarding against re-init. Use a context and revert it on `elementor/frontend/init` re-renders.

On static pages, use a plain `<script src>` or ESM import with a pinned version, as in the repo's vanilla example.

## 8. Open questions
- The GSAP library licence is not MIT. It's GreenSock's "standard no-charge" licence after the Webflow deal. The repo says "free incl. commercial", but I recall the licence restricts use in tools that compete with Webflow (e.g. visual site builders). I didn't verify this, so check gsap.com/licensing before relying on it. Normal client sites are almost certainly fine. Whether a WordPress page-builder addon we distributed would count as competing is unclear.
- Elementor bundles its own animation stack. Does current Elementor Pro already ship GSAP? Version conflicts are possible; verify.
- Reduced motion: `duration:0` on a `from()` tween still jumps elements in on load. Is "show final state, no movement" (skipping the tween entirely) better for CLS and a11y? The repo doesn't say.
- No-JS / SEO: the vanilla example hides elements with inline `opacity:0` before JS runs. If JS fails, the content stays invisible. Our rule should be to apply the hidden start state only from JS (gsap.from/set) or behind a `.js` class.
- Bug in source: the horizontal-scroll example in gsap-scrolltrigger has the typo `Max.max` (should be `Math.max`) and mixes px into `xPercent`. Don't copy it verbatim.
- SUGGESTED: GSAP licensing page - https://gsap.com/licensing/ - confirms the actual commercial terms and any competing-tool restriction.
- SUGGESTED: MDN CSS scroll-driven animations - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations - a no-library alternative to ScrollTrigger for simple reveals and parallax on static pages.
