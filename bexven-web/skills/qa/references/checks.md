# Checks (numbers)

Load at **step 3**. Every check has a number or a yes/no and a way to verify it. Measure numbers by script or tool, **never by eyeballing a screenshot**; screenshots are for looks only (C19). {10,11,12,14}

**How column:**
- `lint:<id>` = `lint_html.py` rule id (static, one HTML file + local CSS)
- `shots` = `screenshots.py` report (overflow, console/page errors, PNGs)
- `js` = a short Playwright snippet you run (two ready-made ones at the bottom)
- `devtools` = Chrome DevTools MCP if connected (`devtools-mcp.md`)
- `manual` = you do it by hand and say so in the report

**What the scripts do NOT cover** (so you must): contrast ratios, touch-target sizes, skip link, landmarks, hover gating, `aria-current`, duplicate IDs, autocomplete, `action="#"`, lazy LCP image, canonical/OG/noindex, NAP match between JSON-LD and visible text, failed network requests that log no console error, keyboard and form behaviour.

Precedence: explicit client brief or existing brand > these floors > Bexven defaults. A floor (a11y, legal, perf) is never waived for looks.

---

## 1. Accessibility (WCAG 2.2 AA is the gate)

| Check | Pass | How |
|---|---|---|
| Body text contrast | ≥4.5:1 | js snippet A (computed colours), or compute from DESIGN.md token pairs: L = 0.2126R+0.7152G+0.0722B on linearised sRGB, ratio (L1+0.05)/(L2+0.05) |
| Large text (≥24px, or ≥18.66px bold) | ≥3:1 | as above |
| UI components, state borders, focus ring | ≥3:1 against adjacent colour | js A on the element + manual |
| Older audience (funeral, senior care) | body aims 7:1, body ≥18px | js A |
| Text over images or gradients | worst-case area behind the text still passes | screenshot crop + sample darkest/lightest pixel; add a scrim if unsure |
| APCA (advisory) | flag thin or light text under Lc 60 that passes WCAG | manual note, never a fail alone |
| Focus visible | every focusable element shows a `:focus-visible` ring | `lint:outline-none` + manual Tab pass |
| Focus not obscured | sticky header/phone bar never covers focus; `scroll-margin-top` ≈ header height | manual Tab pass at 375 |
| Touch targets | ≥44×44px, ≥8px apart; primary mobile CTA and phone button ≥48px tall | js snippet B at 375 |
| Zoom | no `user-scalable=no` / `maximum-scale=1` | `lint:zoom-disabled` |
| Reflow | no horizontal scroll at 320/375; usable at 200% zoom | `shots` (overflow; add `--widths 320,375,768,1024,1440`) + manual zoom |
| `<html lang>` | present | `lint:html-lang` |
| Skip link first, landmarks `header/nav/main/footer` | present | manual (view source / a11y snapshot) |
| Headings | one descriptive h1; no skipped levels | `lint:h1-count`, `lint:heading-order` |
| Images | `alt` on every `<img>`; `alt=""` for decorative | `lint:img-alt` |
| Icons | decorative SVG `aria-hidden="true"`; icon-only buttons named | manual / a11y snapshot |
| Native elements | links `<a>`, actions `<button>`; no clickable divs; no `<a><button>` | manual |
| Current page | `aria-current="page"` in nav | manual |
| Colour alone | status never colour-only | manual |
| Mobile menu / dialogs | focus moves in, trapped, Escape closes, returns to toggle | manual keyboard or devtools |
| Consistent help | phone/contact in the same relative place on every page | manual across pages |
| Media | no autoplay with sound; anything moving >5s has a pause | manual |
| Forced colours / dark | page stays legible | `shots --dark` if the site supports dark; devtools or js `emulate_media(forced_colors="active")` |

## 2. Motion

| Check | Pass | How |
|---|---|---|
| Reduced-motion pass | under `reduce`: no movement, opacity/colour ≤150ms, final states shown | `shots --reduced-motion --name <page>-rm`, compare with normal shots |
| Content visible without JS | nothing starts hidden unless behind a `.js` class | js: new context with `java_script_enabled=False`, screenshot, compare |
| Entrance animations | ≤1 motion moment per page; no fade-up on every section | `lint:entrance-animation` (fires at >2 sections) + look at shots |
| `transition: all` | none | `lint:transition-all` |
| Animated properties | `transform`, `opacity` (clip-path ok) only | `lint:keyframes-layout` |
| Hover gated | `:hover` inside `@media (hover: hover) and (pointer: fine)` | manual grep of CSS |
| Smooth scroll | only inside `(prefers-reduced-motion: no-preference)`; no smooth-scroll library | manual grep |
| Carousels | no auto-rotation | manual (wait 10s at 1440) |

## 3. Performance (lab numbers are labelled lab)

| Check | Pass | How |
|---|---|---|
| LCP | ≤2.5s (2.5–4 needs work, >4 poor) | devtools trace, mobile ≈390px, CPU 4×, Slow 4G, median of 3; otherwise "not measured" |
| INP | ≤200ms (200–500 needs work) | devtools trace with real clicks; otherwise "not measured" |
| CLS | ≤0.1 (0.1–0.25 needs work) | devtools `CLSCulprits`; else js `PerformanceObserver` layout-shift sum, labelled single lab session |
| TTFB | <800ms | devtools / js `performance.getEntriesByType('navigation')` |
| LCP image | real `<img>` in initial HTML, not lazy, not a CSS background, `fetchpriority="high"` | manual (find the hero element in source) |
| Image dimensions | `width`/`height` on every `<img>` (or `aspect-ratio`) | `lint:img-size` |
| Below-fold images | `loading="lazy" decoding="async"` | manual grep |
| Formats | `<picture>` AVIF/WebP + `srcset`/`sizes`; SVG logos/icons | manual |
| Page weight | <1.5MB | js: sum `transferSize` of resource entries, or devtools network |
| Images | ≤1.2MB total, ≤350KB each, above-fold <500KB | js / `ls -la` on local assets |
| Fonts | ≤100KB, WOFF2, self-hosted, `font-display: swap`, ≤2 families | `lint:google-fonts-cdn` + asset sizes |
| JS / CSS / third-party | <300KB / <100KB compressed / <200KB | network |
| Scripts | `defer` or `type="module"`; no parser-blocking JS in head; no CSS `@import` | manual grep |
| Maps / video embeds | facade (static image + link) | manual |
| Lighthouse (guardrail only) | Perf ≥90, Best Practices ≥95, SEO ≥95, A11y 100 automated | devtools, or Lighthouse CLI if already installed |

Never claim speed or ranking gains without before/after numbers from the same URL and conditions. Field data lags ~28 days: write "lab verified, field pending".

## 4. Code and console

| Check | Pass | How |
|---|---|---|
| Console errors / uncaught page errors | 0 | `shots` |
| Failed requests (4xx/5xx) | 0 | Chromium logs most as console errors (`shots`); confirm with devtools network or a js `page.on("response")` filter |
| Doctype, charset first, viewport | present | `lint:viewport` + manual |
| Duplicate IDs | none | js `document.querySelectorAll('[id]')` count vs Set |
| Raw hex outside `:root` | ≤12 | `lint:raw-hex` |
| Third-party CDNs | none; versions pinned | `lint:google-fonts-cdn` + manual grep for `cdn`/`@latest` |

## 5. SEO and markup

| Check | Pass | How |
|---|---|---|
| `<title>` | present, unique, "Business – service in Town"; ~50–60 chars is a hint | `lint:title` + manual |
| Meta description | present; ~150–160 chars is a hint | `lint:meta-description` |
| Canonical | self-referencing on live sites; **none** to a domain we don't control on outreach previews | manual |
| Open Graph | og:title, og:description, og:image | manual |
| `noindex` | on outreach previews and staging; never on live | manual (ask which it is) |
| Link and button text | descriptive; never "Submit", "Click here", "Read more", "Learn more", "Get started" | `lint:generic-cta` |
| Copy | no slop words, no lorem | `lint:banned-copy` |
| Multiple h1 | not a fail alone; descriptive primary heading is | `lint:h1-count` (treat as P3 on CMS pages) |

## 6. Local business (lint with `--local`)

| Check | Pass | How |
|---|---|---|
| Phone | `tel:` with international format, header or footer on every page, same position site-wide | `lint:local-tel` + manual across pages |
| JSON-LD | parses; `LocalBusiness` or most specific subtype (`FuneralHome`, `HomeAndConstructionBusiness`…) | `lint:local-jsonld`, `lint:jsonld-invalid` |
| JSON-LD content | only visible facts: name, address, geo, phone, hours, url, sameAs, image | manual |
| NAP | identical in footer, contact page, JSON-LD and Google profile | manual (compare strings character by character) |
| Hours | real list/table with tabular figures; matches JSON-LD | manual |
| Address | links to a maps search | manual |
| Map | facade, not an eager iframe | manual |
| Real facts | no invented reviews, years, prices, certifications; placeholders labelled and listed in Known gaps | manual — **P0** if invented |

## 7. Forms (contact and quote)

| Check | Pass | How |
|---|---|---|
| Labels | visible `<label for>` on every field; placeholder never the label | `lint:input-label`, `lint:input-label-aria` |
| Types | `email`, `tel`, `date`, `file`, `<textarea>`; `inputmode` for numbers | manual |
| Autocomplete | `name`, `email`, `tel`, `street-address`, `postal-code`, `organization` on personal fields | manual |
| Field size | ≥16px font on mobile; ≥44px tall | js snippet B covers height; font via computed style |
| Required | marked in text, consistently | manual |
| Submit label | names the result ("Request a quote") | `lint:generic-cta` |
| Action | never `action="#"`; working endpoint or labelled demo state | manual + real submit |
| Errors | inline under field, `aria-invalid` + `aria-describedby`, focus to first error, colour + icon + text, no "Oops" | manual: submit empty, then a bad email |
| Success | only after a real send; polite live region; says what happens next and when; no "!" | manual |
| Failure | keeps typed input; offers phone and email | manual (js `context.set_offline(True)` then submit) |
| Alternatives | `tel:` and `mailto:` beside the form | manual |
| Spam | off-screen honeypot with `aria-hidden`, `tabindex="-1"`; no CAPTCHA by default | manual |
| Consent | one plain sentence + privacy link; no pre-ticked box | manual |
| Quote uploads (fabrication) | formats (PDF, DWG, DXF, STEP) and size limit stated; file name shown after pick | manual |

## 8. Break tests (manual, once per site)

- Worst-case content: very long name, diacritics, long email, 0/1/many reviews, a missing image.
- One **WebKit** pass before an outreach link goes out (iPhone Safari): js with `p.webkit.launch()` at 375; check fonts, sticky header, form fields.
- Keyboard: Tab through the homepage; focus order matches visual order.
- Spend time where traffic is: homepage, contact page, mobile.

## 9. Elementor / WordPress extras

- Lint the rendered HTML (save it first, see SKILL.md gotchas); `lint:entrance-animation` catches Elementor `_animation`.
- Compare against the saved static screenshots at 375/768/1024/1440; differences are issues unless agreed.
- Hero is an Image widget (real `<img>`), not a section background.
- No `fonts.googleapis.com` / `fonts.gstatic.com` requests.
- Count scripts and styles per page; flag plugin bloat and render-blocking CSS (devtools network).
- Specificity bugs: inspect the cascade (`get_css_styles`), never stack `!important`.
- Staging stays `noindex` until launch; live must not be.

---

## Snippets (Python Playwright; run from the scratch dir, pass the URL as an argument)

**A. Contrast of visible text** — prints elements under the AA floor at one width.
```python
import sys
from playwright.sync_api import sync_playwright
JS = """() => {
 const lin=c=>{c/=255;return c<=0.03928?c/12.92:((c+0.055)/1.055)**2.4};
 const L=([r,g,b])=>0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b);
 const rgb=s=>(s.match(/[\\d.]+/g)||[]).map(Number);
 const bg=el=>{for(;el;el=el.parentElement){const c=rgb(getComputedStyle(el).backgroundColor);
   if(c.length>=3&&(c[3]===undefined||c[3]>0.5))return c.slice(0,3);}return [255,255,255]};
 const out=[];
 for(const el of document.querySelectorAll('body *')){
  if(![...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))continue;
  const s=getComputedStyle(el); if(s.visibility==='hidden'||s.display==='none')continue;
  const a=L(rgb(s.color).slice(0,3)), b=L(bg(el));
  const r=(Math.max(a,b)+0.05)/(Math.min(a,b)+0.05);
  const px=parseFloat(s.fontSize), big=px>=24||(px>=18.66&&+s.fontWeight>=700);
  if(r<(big?3:4.5)) out.push([r.toFixed(2),px,el.tagName,el.textContent.trim().slice(0,40)]);
 } return out;}"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 375, "height": 900})
    pg.goto(sys.argv[1], wait_until="networkidle")
    for row in pg.evaluate(JS): print(*row, sep=" | ")
    b.close()
```
It reads solid backgrounds only; text over images, gradients or translucent layers needs a manual check.

**B. Touch targets at 375** — swap the `evaluate` body for:
```javascript
() => [...document.querySelectorAll('a,button,input,select,textarea,[role=button]')]
  .map(e => [e, e.getBoundingClientRect()])
  .filter(([e, r]) => r.width && r.height && (r.width < 44 || r.height < 44))
  .map(([e, r]) => [Math.round(r.width), Math.round(r.height), e.tagName, (e.textContent || e.name || '').trim().slice(0, 30)])
```
Inline text links inside paragraphs are exempt; buttons, nav items, phone links and form fields are not.
