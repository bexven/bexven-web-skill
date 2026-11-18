# Rut and directions

Loaded at steps 2-3. How to name the category rut, derive directions from the client's world, and tell a strong direction from a weak one.

## 1. Writing the rut

The rut is the page a model (or a template shop) would produce for this niche with no other context. Write it as one paragraph covering six slots:

| Slot | Question |
|---|---|
| Hero | What fills the first viewport? (stock photo type, overlay, headline formula) |
| Palette | Which 2-3 colours does every competitor use? |
| Fonts | Which pairing? (often one overused sans, sometimes a "luxury" serif) |
| Section order | The usual skeleton, in order |
| Imagery | The stock photo everyone buys |
| Copy | The headline and CTA formulas |

Sources: the niche file's "The rut" section, plus 3-5 real competitor sites in the same town or region (note their shared defaults). Then:
- Ban the rut as a default.
- Ban its obvious opposite too (the rut inverted is still category-driven: "funeral homes are soft, so make it brutal" is a guess from the category).
- Put the competitors' shared defaults on a per-project avoid list in DESIGN.md Overview ("Rut avoided").

## 2. Mining the client's world

Before writing directions, list 10-15 concrete things from the client's world. Sources, in order of value:
1. Their own material: building, signage, vehicles, uniforms, letterhead, old adverts, the logo's real colours, interior finishes, the products or work itself.
2. Place: town, street, landscape, local stone or brick, regional print traditions, the era the business was founded.
3. Rituals and documents of the trade: order-of-service booklets, register books, memorial cards, cut lists, work orders, mill certificates, shop drawings, inspection tags.
4. Pre-web print forms in the field: almanacs, parish newsletters, trade catalogues, engineering handbooks, railway timetables, hardware store signage.

Spread directions across at least 3 material families (e.g. paper/print, architecture/place, product/material, landscape/nature, civic/signage). At most one direction may be the literal trade metaphor (coffins and lilies; sparks and steel plate).

## 3. The axes

Every direction states a value on each axis. Every pair of directions differs on at least 2.

| Axis | Example values |
|---|---|
| Type voice | humanist serif text + plain sans; single grotesque family with width contrast; transitional serif display + sturdy sans; condensed industrial sans + book serif; slab display |
| Colour strategy | Restrained (~85% neutral, accent scarce); Committed (brand colour owns 30-60% of the page as fields); Drenched (one colour is the page) |
| Layout grammar | long single column with marginalia; asymmetric 60/40 splits; ledger/table rhythm; full-bleed photo bands alternating with dense text; index/list-led |
| Imagery treatment | full-colour documentary; one large photo per section; cropped details (hands, materials); monochrome or duotone from the palette; type-led with few photos |
| Signature moment | one hover idea, one entrance, one scroll sequence, or "none"; must come from the world (a register line drawing in under a link; a spec table row highlighting) |
| Also log | hero type (slug from `layout.md`), section order, density (dense / airy), emphasis device |

## 4. Writing one direction

```
Name: <2-3 words, a thing not a mood>
Governing idea: <one sentence that opens with a concrete object, place or era>
Characteristics (5-7): type voice · colour strategy + palette family · layout grammar · imagery · signature · density · emphasis device
Hero type / section order: <slug> / <comma list>
From the client's world because: <evidence from intake>
Similar-prompt test: <would another client in this niche land here? what makes it this client's?>
```

A direction that reads like a mood board ("warm, modern, trustworthy, clean") is not decided. Replace each adjective with the object it came from.

## 5. Funeral home examples (generic, fictional client)

Fictional client: family-run funeral home in a small river town, founded 1952, red-brick building with a white-painted porch, logo in dark green, current site uses a sunset-over-water stock photo.

**Rut:** full-width sunset or lilies photo with a dark overlay, centred serif headline "Honoring lives with dignity and compassion", cream background, gold or burgundy accent, Playfair Display + a stock sans, sections Welcome → Services (3 icon cards: burial, cremation, pre-planning) → Testimonials slider → Obituaries link → Contact, script font somewhere, dove or candle icons.

**Weak directions (do not ship):**
- "Elegant and serene: soft cream, gold accents, a refined serif, peaceful imagery." The rut in nicer words; no client evidence.
- "Modern and minimal: white, black, lots of space, a clean sans." Differs from the rut by adjectives only; could be any business.
- "Like the first one but navy instead of gold." Differs on one axis (accent).
- "Bold and unexpected: black ground, neon type." The rut's opposite, guessed from the category, wrong for the audience.

**Strong directions:**
1. **Parish register.** The handwritten register books where local deaths and services were recorded. Transitional serif text at generous size, ruled lines as real separators between notices, Restrained (linen paper, brand-green ink, one rust accent), single column with dated marginalia for service times, notices lead the page after the phone number, few photos, signature: a ruled line draws under links on hover. Hero type `type-led`.
2. **Red brick and porch.** The building itself. Full-bleed documentary photo of the real porch at dusk, Committed (brick-red fields from the facade sampled in OKLCH, porch-white text), sturdy humanist sans throughout with weight as emphasis, 60/40 splits alternating with one full-width band, signature: none. Hero type `full-bleed-photo`.
3. **River path.** The town's riverside walk where the cemetery sits. Landscape detail crops (stone, water, reeds), Restrained with a deep green-grey field for the first-steps section only, humanist serif display + plain sans, airy spacing, a short "what to do now" list as the second section, signature: slow cross-fade between two real photos in the hero (respects reduced motion). Hero type `photo-split`.

Pairs differ on type voice, colour strategy, layout grammar and imagery; none needs the stock sunset.

## 6. Metal fabrication examples (generic, fictional client)

Fictional client: 25-person fabrication shop in an industrial park, laser cutting, press-brake bending, MIG/TIG welding, powder coating in-house; trucks painted deep blue with a yellow stripe; current site is a dark template with a spark-shower hero.

**Rut:** dark charcoal hero with a stock welder and spark shower, "Precision metal fabrication solutions" in condensed caps, safety orange or yellow accent on slate, Oswald or Bebas + Open Sans, sections Hero → 3 icon cards (cutting, bending, welding) → "Why choose us" with stats counter (years, projects, clients) → gallery carousel → Get a quote; blueprint grid backgrounds.

**Weak directions:**
- "Industrial strength: dark steel greys, bold condensed type, orange accents." The rut.
- "Clean and corporate: white, blue, a friendly sans." Generic B2B; no shop evidence.
- "Raw and gritty: textures, distressed type, rust." Category guess (the stencil/rust cliché), and texture not taken from the client's material.

**Strong directions:**
1. **Work order.** The shop's own job traveller and cut list. Light paper ground, ink tinted to the truck blue, one yellow accent for the quote CTA (Restrained), a grotesque family with width contrast (wide for headings, normal for text), capabilities as a real table with tolerances and max sheet sizes (tabular figures), dense spacing. Signature: table row highlight on hover. Hero type `work-sample-led` (a real cut part with its spec beside it).
2. **Fleet livery.** The trucks. Committed: truck-blue fields own the hero and the closing quote section, yellow stripe used once as a structural rule, condensed sans for display only, book-like serif for body copy (unexpected for the trade, readable for engineers), full-bleed real photo of a loaded truck, 66/33 splits below. Signature: none. Hero type `full-bleed-photo`.
3. **Finishing booth.** The powder-coat colour cards the shop offers. Restrained neutral page, but the portfolio is organised by finish with real RAL swatches as small labelled chips (information, not decoration), humanist sans, project photos in consistent 4:3 crops with material, thickness and finish captions, list-led layout. Hero type `split` with the newest project.

## 7. Checks before moving on

- Run the similar-prompt test and the guessability test (see `tells.md`) on each direction; revise and note what changed.
- Every direction names its evidence from intake. No evidence = not from the client's world.
- Each pair differs on ≥2 axes. Write the differing axes beside each pair if unsure.
- Then step 4: `niche_log.py check` each, drop collisions, seeded `pick`.
