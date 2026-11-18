# Layout

Loaded at steps 3 and 7. Defines the hero-type slugs for the niche log, the section grammar, and the limits a direction must respect. Principle: conventional in where things are and how they behave (logo top-left, nav, contact, phone, forms); distinctive in composition.

## 1. Hero types (use these slugs in DESIGN.md and `niche_log.py`)

| Slug | What it is | Good when |
|---|---|---|
| `full-bleed-photo` | one real photo edge to edge, text on it or beside it | the client has one strong photo of the place or work |
| `photo-split` | photo on one side, text on the other (60/40 or 66/33) | decent photos, lots to say in the first viewport |
| `type-led` | large set type, little or no photo | weak photos; editorial or document directions |
| `place-led` | map, street, building drawing or location as the lead | location is the deciding factor (parking, district) |
| `work-sample-led` | one real product/project with its facts beside it | trades, makers, portfolios |
| `list-led` | the first viewport is a useful list (notices, services, hours) | task-heavy sites (funeral notices, opening hours) |
| `split` | two equal halves with different jobs (e.g. call vs plan ahead) | two clear audiences |

Always the same slug spelling. Do not invent a new slug unless none fits; then add it here.

## 2. First viewport

- Shows the most characteristic thing in the client's world, not a generic hero.
- At 1440×900 and 390×844: the H1, one hard fact (town, service, phone, years if verified) and the primary CTA are visible.
- At most 3 type sizes above the fold.
- `min-height` on the hero only, with `100svh` (never `100vh`); all other sections size to content.
- Hero content may sit top-biased rather than centred. No hamburger-over-stock-photo heroes.
- Memory test: what would a visitor describe an hour later? "A website" means rework.

## 3. Section grammar

- Content inventory comes from the niche file (must-haves); order and composition come from the direction.
- Write the composition in words in DESIGN.md Layout, e.g. "full-bleed porch photo; a 60/40 split with the first-steps list; a ruled notices list; one dense services table; a quiet address close".
- Never ship the default skeleton: hero → features → testimonials/pricing → FAQ → CTA, each with eyebrow + heading + lede + 3 cards.
- Neighbouring sections never share a layout. Pace with density, scale, imagery and quiet.
- One primary job per section; long copy chunks into labelled groups (heading + 2-4 lines).
- End on a real close: contact, address, next step. Not a fade-out, not a newsletter box.
- Section order goes into the niche log as a comma list of short slugs (`hero,first-steps,notices,services,people,place,contact`). Use the same slugs consistently so `check` can compare.

## 4. Hard limits

| Limit | Number |
|---|---|
| Card layouts (grids of 2+ equal boxes, bento included) | max 2 per page |
| 3-equal-icon-card grid | not by default |
| Mirrored zig-zag (image left/right alternating) | max 2 alternations |
| Box nesting | max 2 levels, never card in card |
| Eyebrows (small label above a heading) | off by default; max 2 per page, only if they carry information (date, category, real step, location), never on adjacent sections |
| Big-stat hero / 3-stat strip | not used |
| 01/02/03 numbering | only for real sequences |
| Primary CTA | one per viewport; at most one secondary |
| Main nav | 5-6 items, customers' words, contact last |
| Container | one shared max width 1200-1280px |

## 5. Grid and spacing defaults

- Prefer asymmetric splits (66/33, 60/40), spans and offsets over equal columns.
- Spacing scale on a 4 or 8px base; state the philosophy (dense or airy) in DESIGN.md.
- Within a group 8-16px; between sections 64-120px on desktop (dense trades lower, calm niches higher); mobile roughly 60% of desktop.
- More space above a heading than below it. Bottom padding often optically larger than top.
- Text containers `max-width: 65ch` (62-70ch range).
- Structural devices (rules, numbers, borders, labels) must carry real information.

## 6. Sticky and moving UI

- Allowed sticky UI: an opaque header (no blur, shrink or hide-on-scroll by default) and on mobile one call/quote bar that appears after the hero CTA scrolls away.
- No auto-rotating carousels, testimonial sliders or logo marquees. A horizontal `scroll-snap` row only when content overflows, with visible prev/next.
- No popups before the visitor has read anything; no self-opening chat bubbles.

## 7. Radius and elevation (decided here, recorded in Shapes/Elevation)

- One radius language per direction, e.g. "0 on photos and sections, 2px on fields, pill on buttons". Never one 8-12px radius on everything. Don't mix sharp and round in one view.
- Nested radii concentric: inner = outer − padding.
- Elevation table with a ceiling, often flat + tone. No default soft blurred shadow, no thin border + wide shadow card kit.
