# Local SEO, head and performance budgets

Load at build steps 8–9.

## 1. NAP consistency

- Name, address, phone come from the prospect's own site or Google Business Profile, copied exactly (same spelling, abbreviations, suite numbers). Written identically in the header/footer, contact block, and JSON-LD.
- Phone: display in local format, `href="tel:+<country><number>"` with no spaces. Same position on every page.
- If two sources disagree, use the Google profile version and note the conflict in the report.
- Unknown hours/details: leave them out of both page and JSON-LD; list under Known gaps. Never guess.

## 2. Head template

```html
<title>Uitvaartzorg Peeters – funeral director in Geel</title>          <!-- Business – service in Town, ~50–60 chars -->
<meta name="description" content="…">                                  <!-- ~150–160 chars, real facts, no slop -->
<meta name="robots" content="noindex, nofollow">                       <!-- OUTREACH PREVIEW ONLY: remove at launch -->
<!-- canonical: self-referencing on the client's own domain at launch; omit on a preview we host -->
<meta property="og:type" content="website">
<meta property="og:title" content="…">
<meta property="og:description" content="…">
<meta property="og:image" content="https://<preview-host>/img/og-1200x630.jpg">
<meta property="og:locale" content="nl_BE">
<meta name="theme-color" content="…">                                  <!-- the header/paper colour -->
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
```
- Unique title and description per page; title leads with the business, then service and town.
- **Outreach previews are `noindex, nofollow`** until the client owns the site, and carry **no canonical to a domain we do not control**. Also add the header (see vercel-deploy.md) as a belt-and-braces measure.
- Headings: one h1 naming the service and the place or buyer ("Funeral director in Geel and the Kempen"); every heading contains a noun; logical h2/h3 order. Keywords come from the customers' words, not stuffing.
- Descriptive link text; no "click here". Breadcrumbs on deep pages in the full build.
- URLs lowercase, hyphenated, short. Obituaries, capabilities, services get crawlable HTML pages in the full build (never PDFs or iframes).

## 3. LocalBusiness JSON-LD

Use the most specific subtype and mark up **only what is visible on the page**.

| Niche | `@type` |
|---|---|
| Funeral home | `FuneralHome` |
| Metal fabrication / welding | `HomeAndConstructionBusiness` or `LocalBusiness` + `makesOffer` (no exact fabrication type exists) |
| Plumber / electrician / roofer / HVAC | `Plumber` / `Electrician` / `RoofingContractor` / `HVACBusiness` |
| Dentist / physio | `Dentist` / `PhysicalTherapy` |
| Restaurant / bakery | `Restaurant` / `Bakery` |
| Car repair | `AutoRepair` |
| Lawyer / accountant | `LegalService` / `AccountingService` |
| Unsure | `LocalBusiness` |

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FuneralHome",
  "name": "Uitvaartzorg Peeters",
  "url": "https://www.example.be/",
  "telephone": "+3214123456",
  "email": "info@example.be",
  "image": "https://<host>/img/chapel-entrance-kerkstraat.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Kerkstraat 12",
    "postalCode": "2440",
    "addressLocality": "Geel",
    "addressCountry": "BE"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 51.1612, "longitude": 4.9896 },
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "09:00", "closes": "17:00" }
  ],
  "areaServed": ["Geel", "Kasterlee", "Mol"],
  "sameAs": ["https://www.facebook.com/…", "https://maps.google.com/?cid=…"]
}
</script>
```
- `url` is the client's real domain (the business entity's site), even on a preview.
- 24/7 phone availability: say it in text; only model hours that are real opening hours.
- Geo from the Google profile pin (4 decimals is enough). Omit if unknown.
- No `aggregateRating`/`review` for self-collected or copied reviews. No fields the page does not show.
- Fabrication: list services with `makesOffer` → `Offer` → `itemOffered: {"@type":"Service","name":"Laser cutting"}`.
- Validate with the Rich Results Test / Schema validator before hand-off (QA checks it matches visible NAP).

## 4. Core Web Vitals and budgets

Targets ("good", p75): **LCP ≤2.5s, INP ≤200ms, CLS ≤0.1**. TTFB <800ms. Lighthouse: Performance ≥90, Best Practices ≥95, SEO ≥95, Accessibility 100 (automated) before outreach. Report lab numbers as lab; never promise ranking gains.

| Budget | Limit |
|---|---|
| Whole page | <1.5MB |
| Images total / each / above fold | ≤1.2MB / ≤350KB / <500KB |
| JS | <300KB (a static mock typically needs <15KB) |
| CSS | <100KB compressed; inline critical ≤14KB on the mock |
| Third-party | <200KB, after first paint or behind facades |
| Fonts | ≤2 families, ≤4 files, ≤100KB total |

- LCP element: real `<img>` in the HTML, `fetchpriority="high"`, not lazy, not CSS background. Preload it only if discovered late.
- Reserve space for everything: image dimensions, map facade `aspect-ratio`, cookie banner slot, font fallback metrics.
- Scripts `defer` or `type="module"`; nothing parser-blocking in `<head>` except the one-line `.js` class setter.
- `content-visibility: auto; contain-intrinsic-size: auto 800px;` on long off-screen sections.
- Preconnect only to origins actually used (usually none: everything is self-hosted).

## 5. Image formats

AVIF first, WebP second, JPEG fallback via `<picture>`; SVG for logos and icons; PNG only for screenshots needing lossless. Widths 400/800/1200/1600. Details in imagery-icons.md.

## 6. Font loading

- **Self-host WOFF2 only.** Zero requests to fonts.googleapis.com, fonts.gstatic.com, api.fontshare.com (GDPR; a German court fined CDN font use in 2022). Download the files, keep each font's licence file in `fonts/`.
- Licence check before use: OFL preferred; ITF FFL (Fontshare) faces only on the client's own site, never in public repos; paid faces only with a client licence recorded.
- **Budget: ≤2 families, ≤4 files, ≤100KB total.** Prefer one variable file per family. Subset to latin + latin-ext via `unicode-range` (check diacritics the client needs, e.g. ë, é, ij, ß).
- `font-display: swap`.
- **Preload only the 1–2 files used above the fold**, with `crossorigin` (required even same-origin):
  ```html
  <link rel="preload" href="/fonts/display-var.woff2" as="font" type="font/woff2" crossorigin>
  ```
  ```css
  @font-face {
    font-family: "Display";  /* real family name from DESIGN.md */
    src: url("/fonts/display-var.woff2") format("woff2");
    font-weight: 400 700; font-style: normal; font-display: swap;
    unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+20AC, U+2122, U+2212;
  }
  @font-face {               /* metric-matched fallback to stop swap CLS */
    font-family: "Display Fallback"; src: local("Arial");
    size-adjust: 104%; ascent-override: 92%; descent-override: 24%; line-gap-override: 0%;
  }
  :root { --font-display-stack: "Display", "Display Fallback", sans-serif; }
  ```
  Tune the override percentages against the real pair (compare screenshots or measure the swap shift); the numbers above are placeholders.
- Fallback stacks end in a generic family. A system face is never the brand voice.

## 7. Launch checklist (full build, not the preview)

Remove `noindex`, add self-referencing canonical, robots.txt that never blocks CSS/JS, sitemap of canonical URLs only, Google profile URL in `sameAs`, security headers (see vercel-deploy.md).
