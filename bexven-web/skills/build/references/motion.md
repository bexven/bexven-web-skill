# Motion

Load at build step 7. Default answer: less. A local-business page with zero animation beyond state feedback is a correct page.

## 1. Gate before you animate

1. **Frequency gate.** Used constantly (nav links, inputs, buttons) → no motion or near-invisible colour change. Occasional (menu, accordion, dialog) → standard short motion. Rare (first view of the hero) → the only place a "moment" may live.
2. **Purpose.** Each animation names its job: feedback, state change, spatial continuity, or explanation. "Looks nice" is cut.
3. **Budget.** At most **one motion moment per page**, and only if DESIGN.md names it. The hero entrance counts as that moment. No section reveals by default.
4. **Niche.** Funeral homes: no hero theatre, no scroll reveals, no autoplay video; state feedback only. Fabrication: a scroll-linked process moment only if DESIGN.md names one.
5. **Same moment everywhere.** The static mock and the later WordPress build carry the same moment; do not add one in the mock that Elementor cannot reproduce cheaply.

Banned regardless: fade-up on every section (AOS-style `.reveal`), staggered load-in of every element, count-up numbers, charts redrawing on mount, pulsing dots, glowing/beam borders, gradient orbs, per-letter text reveals, hover lift/zoom/glow on cards, parallax, smooth-scroll libraries, magnetic buttons, 3D tilt, animated keyboard actions.

## 2. Tokens (put in DESIGN.md `motion`, generated into `:root`)

```yaml
motion:
  ease-out: cubic-bezier(0.23, 1, 0.32, 1)        # enter, exit, default
  ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)    # something crossing the screen
  ease-drawer: cubic-bezier(0.32, 0.72, 0, 1)     # sheets, mobile menu
  dur-press: 120ms      # press, hover colour (100–150)
  dur-state: 200ms      # toggles, accordions, dropdowns (150–250)
  dur-surface: 320ms    # menus, drawers, dialogs (250–400)
  dur-moment: 700ms     # the single named moment (≤800)
```
- Name by purpose, not speed. Exits ≈ 75–80% of the entry duration, ease-out, simultaneous (never reverse-staggered).
- Hover transitions 120–200ms. Focus rings appear instantly, no transition.
- No ease-in on UI. No bounce/overshoot. Linear only for progress bars.
- Never start from `scale(0)`: use 0.94–0.97 + opacity. Popovers scale from their trigger (`transform-origin`); dialogs stay centred.
- Stagger (only inside the moment): 30–80ms steps (up to 120ms in a hero), varied by importance, max ~5 items; never uniform `i * 0.1`, never parent entrance + child stagger.

## 3. Implementation ladder

Climb only as far as the moment needs:
1. **CSS** transitions/animations, `@starting-style` for enter-on-insert, `animation-timeline: view()` for a simple scroll-linked effect (with a static fallback where unsupported). Default for everything; transitions are retargetable, so use them for anything triggered repeatedly.
2. **WAAPI or Motion** (`animate()`, `inView()`), self-hosted, pinned version, `defer`. For a JS-sequenced entrance or once-only in-view moment.
3. **GSAP** only for a named timeline, a scroll-linked/pinned sequence, SplitText, or SVG drawing. Self-host the core + only the plugins used, pinned, `defer`. Use timelines with shared `defaults`, `autoAlpha` for fades, `gsap.context()` / `gsap.matchMedia()` for cleanup and reduced motion, `ScrollTrigger.batch()` for groups; remove `markers` before shipping.
4. **Lenis** only for pinned storytelling the direction names: near-default settings, `syncTouch: false`, reduced motion respected, anchors offset by the header, stopped while the menu or a dialog is open. Never for "premium feel".

Always: animate only `transform`, `opacity` (and `clip-path` if needed). Never width, height, top, left, margin. Never `transition: all`. `will-change` only on the element that moves, removed afterwards. Motion is interruptible; choreography never blocks clicks.

## 4. Content visible without JS

Start from the visible final state in CSS. Hide for an entrance only behind a class JS adds:

```html
<script>document.documentElement.classList.add('js')</script>  <!-- inline in <head>, before CSS paints -->
```
```css
@layer components {
  @media (prefers-reduced-motion: no-preference) {
    .js [data-moment] { opacity: 0; translate: 0 12px; }
    .js [data-moment].is-in {
      opacity: 1; translate: 0 0;
      transition: opacity var(--dur-moment) var(--ease-out), translate var(--dur-moment) var(--ease-out);
    }
  }
  @media (prefers-reduced-motion: reduce) {
    .js [data-moment] { opacity: 0; }
    .js [data-moment].is-in { opacity: 1; transition: opacity 150ms linear; }   /* gentler, not zero */
  }
}
```
```js
// add .is-in once; a failsafe timeout reveals anyway if something breaks
const m = document.querySelectorAll('[data-moment]');
requestAnimationFrame(() => m.forEach((el, i) => setTimeout(() => el.classList.add('is-in'), [0, 60, 140][i] ?? 180)));
setTimeout(() => m.forEach((el) => el.classList.add('is-in')), 1500);
```
For an in-view moment use one `IntersectionObserver` (threshold ~0.3), unobserve after firing, and cover at most 2 sections.

## 5. Reduced motion: gentler, not zero

Under `prefers-reduced-motion: reduce`:
- Remove all movement (translate, scale, rotate, parallax, scroll-linked transforms, autoplay video loops).
- Keep opacity and colour changes, ≤150ms.
- Collapse staggers; show final states without a jump.
- GSAP: inside `gsap.matchMedia()`, skip `from()` tweens in the reduce branch rather than setting `duration: 0`.
- Native `scroll-behavior` stays `auto`; `smooth` only inside `(prefers-reduced-motion: no-preference)`, if at all.
- Video: no autoplay; show the poster; play only on click.

## 6. Component motion defaults

| Element | Motion |
|---|---|
| Link / button hover | colour/underline, `--dur-press`, ease-out; gated by hover media query |
| Button press | `scale: 0.97`, `--dur-press` |
| Accordion / `<details>` | `interpolate-size: allow-keywords` + height transition `--dur-state`, or none |
| Mobile menu / sheet | translate + opacity, `--dur-surface`, `--ease-drawer`; exit ~250ms |
| Dialog | opacity + `scale: 0.97 → 1`, `--dur-surface`, centred |
| Form errors | appear instantly; no shake |
| Success message | opacity in, `--dur-state` |
| Spinner | only if the wait >300ms; label kept |

Scroll: native. No parallax. A sticky header changes nothing on scroll.
