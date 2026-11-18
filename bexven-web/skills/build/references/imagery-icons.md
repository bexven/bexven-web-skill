# Imagery and icons

Load at build steps 5 and 9.

## 1. Photo priority

1. **The client's own photos**: their building, work, vehicles, staff (named, supplied by them), town. Taken from their current site or Google profile in the mock stage; listed in the report so the client can confirm rights.
2. **Self-hosted stock, flagged**: downloaded, optimised, self-hosted, never hot-linked. Mark every one:
   ```html
   <!-- PLACEHOLDER: stock (Unsplash, photographer: J. Doe). Replace with client photo of the chapel entrance. -->
   <img src="/img/chapel-light-placeholder.avif" data-placeholder="stock" alt="…" width="1600" height="1067">
   ```
3. **Neutral placeholder block**: a token-coloured box with the exact `aspect-ratio`, a caption describing the photo needed ("Photo: workshop floor with the press brake, landscape"), `data-placeholder="needed"`. Better than a wrong stock photo.

Rules:
- One decisive real photo beats five mediocre ones. Photos of the actual place and work lead the page; mood stock never replaces the work.
- Never present stock people as staff, owners, customers, families or review authors. Never imply a real family endorses the business.
- Stock clichés banned: laptop + latte, handshake, smiling call-centre headset, generic team, spark-shower welder, generic factory, 3D-render heroes, blueprint-grid decoration.
- No hot-linking Unsplash, Pexels, placehold.co, picsum (lint). Credit stock photographers in one quiet footer or hand-off line. List every stock image in the report; the WordPress build swaps them for client photos.
- Never stock imagery in a logo or brand mark.

## 2. Funeral homes: people rules

- No identifiable people in stock imagery at all. No grieving faces, no smiling seniors, no staged families, no hands-holding-hands close-ups that read as stock grief.
- Prefer: the real building and rooms, light through windows, flowers, natural landscape of the region, textures (wood, stone, linen), detail of hands only if non-identifiable and not staged.
- Staff photos only when the client supplies them, with names and roles.
- Obituary photos come from the client's system; never fabricate notices, names or dates. In a mock, show the notices block with a clearly labelled sample ("Sample notice") or link to their existing notices page.
- No autoplay video, no slideshow hero.

## 3. Treatment

- No text on photos except the hero and one closing band; a scrim only if contrast needs it (measure it).
- No filters, duotones or rounded corners on place photos unless DESIGN.md names the treatment as the signature.
- No geometric masks faking a cut-out; use a real alpha matte if a cut-out is the idea.
- Photo geometry (aspect ratios, crop focus on mobile, corner treatment) comes from DESIGN.md; set `object-position` so mobile crops never cut through faces or the key object.
- Background video only if compressed (<2MB), muted, `playsinline`, poster frame, pause control, stopped under reduced motion. Full-screen stock video is a tell.
- Video instead of GIF.

## 4. Files and markup

- Descriptive filenames: `chapel-entrance-kerkstraat.avif`, not `IMG_1234.jpg`.
- `<picture>`: AVIF → WebP → JPEG; `srcset` 400/800/1200/1600w; honest `sizes` (e.g. `(min-width: 64rem) 60vw, 100vw`).
- Every `<img>` has `width` and `height` (intrinsic ratio) or CSS `aspect-ratio`.
- Budgets: ≤350KB per image, ≤500KB above the fold, ≤1.2MB images total. Hero AVIF at 1600w usually lands 120–250KB at quality ~50.
- LCP image: `fetchpriority="high"`, no lazy; others `loading="lazy" decoding="async"`.
- Alt text: describe what is informative ("Front entrance of the funeral home on Kerkstraat, with ramp"); `alt=""` for decorative images. Never "image of", never keyword stuffing.
- Logos and icons: SVG, optimised, no embedded raster.
- Optimise with a local tool (e.g. `cwebp`/`avifenc` or Pillow); never an online converter for client files.

## 5. Icons

- **One family, one style, one stroke weight per site**, chosen to match the type (logged per niche so the next site in the niche differs). No house default; Lucide/Feather untouched are a tell.
- Stroke follows body weight: ~1.25–1.5 next to light or serif text, ~2 next to bold sans. Fabrication may go heavier for functional items.
- **Inline SVG** of only the icons used, `fill`/`stroke` = `currentColor`, `viewBox` kept, width/height set in em to sit on the text line. No icon font, no sprite library for a handful of icons, no CDN.
  ```html
  <a class="phone" href="tel:+3214123456">
    <svg aria-hidden="true" focusable="false" width="1.1em" height="1.1em" viewBox="0 0 24 24"><path d="…" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>
    014 12 34 56
  </a>
  ```
- Decorative icons `aria-hidden="true"`; icon-only buttons get an accessible name (`aria-label` or visually hidden text).
- **Functional only**: nav, contact (phone, mail, pin, clock), specs, status, form errors, external links. Never decoration.
- **No icon-in-tinted-circle feature grids**, no check-icon list on every section, no emoji or unicode symbols as icons, no cliché metaphors (rocket, lightbulb, handshake, hard-hat clip art).
- Balance icon + text lockups: icon optically centred to the x-height, gap ~0.4em, same colour as text unless it is a status.
- Elementor later: the same sanitised SVGs get uploaded as custom icons, so keep them as clean individual files in `img/icons/`.
