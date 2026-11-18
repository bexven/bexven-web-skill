# Niche: metal fabrication

Status: first pass · 2026-11-18 · slug for `niche_log.py`: `metal-fabrication`
Constraints and content only. **This file never supplies a palette, font, hero type or section order**; those come from the direction (client's world + seeded pick). Two Bexven fabrication sites may not share display font, palette family, hero type or section order.

## Audience

- **Primary:** buyers, engineers, contractors and facility managers comparing shops for a job. Mostly desktop at work during the day; phone on site. They scan for capability, limits and speed.
- **Secondary:** private customers wanting gates, railings, stairs, one-off pieces. Less technical; need photos and a simple way to ask.
- **Third:** job seekers (welders, operators); a careers link is often worth it.

## Emotional register

Direct, specific, capable, unpretentious. Facts over adjectives. The work and the machines do the talking. Confident without swagger.

## Must-have content

- Capabilities by process: laser / plasma / waterjet cutting, press-brake bending, rolling, welding types (MIG, TIG, stick), machining, finishing (powder coating, galvanising, painting), assembly - only what the client does.
- Materials and limits: steel, stainless, aluminium; thickness ranges; max sheet or part size; tolerances - only figures the client gives.
- Equipment list (named machines, if the client lists them).
- Project portfolio with real photos, each with material, process, size or scope.
- Industries served.
- Quality certifications the client actually holds.
- Request-a-quote form that accepts drawings, plus phone and email.
- Service area / delivery area; address with visiting hours.

## Task paths (each within two clicks of the homepage)

1. "Can you make this, and how fast?" → capabilities + portfolio + quote form.
2. Send drawings for a quote.
3. Check a specific limit (max thickness, sheet size, material).
4. Call the shop.

## Quote form

- Fields: name, company (optional), email or phone, description, quantity, material, needed-by date, file upload.
- Upload accepts PDF, DWG, DXF, STEP (state formats and size limit before the field); show file name after selection with a remove control.
- `tel:` and `mailto:` beside the form for people who would rather call.

## Trust signals

- Real certifications (welding or quality standards) only if the client holds them; show the number or scope if public.
- Named equipment; real shop-floor and finished-part photos.
- Project captions with material and scope.
- Years in business only if verified.
- Repeat-client or partner names only with permission.

## Data presentation

- Spec data (tolerances, max sheet size, materials, thicknesses) in real tables with tabular figures, not icon cards.
- Units with non-breaking spaces (3 mm, 1500 × 3000 mm).

## Imagery rules

- Priority: the client's own shop floor, machines, finished parts, installed work, vehicles.
- No stock welder with spark shower, no generic factory stock, no 3D-render heroes, no blueprint grids as decoration, no hard-hat clip art.
- Consistent crops for the portfolio; captions with facts.

## Icons

Icons may be heavier to match bold type, but only for functional items (capabilities, specs, contact). No icon-in-circle grids.

## Motion

None by default. A scroll-linked or pinned moment is allowed only if the direction names it (e.g. a cut → bend → weld → finish sequence using real photos), covering at most 2 sections and respecting reduced motion.

## Schema and local SEO

- JSON-LD: the closest LocalBusiness subtype (`HomeAndConstructionBusiness` for gates/railings work) or `LocalBusiness` with `makesOffer` / a service list; real NAP, geo, hours, `sameAs`.
- In the full build each capability gets its own crawlable page ("Laser cutting in <Region>").
- Title pattern: "<Business> - metal fabrication in <Town/Region>". Use the industrial park, town and region names customers use.

## Copy no-gos

- "Precision engineered excellence", "your one-stop shop", "industry-leading", "state-of-the-art", "solutions" on its own.
- Invented capacity figures, lead times or stats counters.
- "Why choose us" sections of adjectives.

## Design no-gos

- Grey/blue + safety orange (or yellow) by default: the category's stock answer. Colour comes from the client's livery, materials, paint finishes or signage.
- Stencil, distressed or "grunge metal" type; brushed-metal textures not from real photos.
- Dark hero with spark shower; stats counter; gallery carousel that auto-rotates.

## The rut (the page this niche always ships)

Dark charcoal hero with a stock welder and spark shower; "Precision metal fabrication solutions" in condensed caps; safety orange or yellow accent on slate; Oswald or Bebas Neue + Open Sans; sections Hero → 3 icon cards (cutting, bending, welding) → "Why choose us" with a stats counter (years, projects, clients) → auto-rotating gallery → "Get a quote" band; blueprint grid backgrounds; hard-hat or gear icons. Its obvious opposite (soft pastel "friendly" SaaS look) is also a category guess.
