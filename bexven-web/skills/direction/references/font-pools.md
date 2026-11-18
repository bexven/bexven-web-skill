# Font pools

Loaded at step 6. Per-niche pools of free fonts with a known licence. Pick from the niche pool first, then the general pool. A pool is a starting set, not a ranking: the direction's type voice decides, and `niche_log.py check` enforces the reuse limits (display font not in any of the last 5 sites in the niche, nor 2 of the last 5 overall).

**Licence key**
- **OFL** = SIL Open Font License 1.1. Commercial use, self-hosting, Elementor Custom Fonts upload, theme bundling allowed; do not sell the files alone. Sources: Google Fonts (GF), Velvetyne (VT), GitHub foundry repos (GH).
- **ITF FFL** = Indian Type Foundry Free Font License (Fontshare, FS). Commercial use allowed. **Self-host on the client site only, no redistribution**: never in public repos, kits, sold themes or shared font folders.
- Before first use of any face: open the licence file inside the download (OFL.txt / FFL PDF) and confirm it. The research pass could not render the licence pages live (2026-11), so the licence column is our current reading, to be confirmed per download. Record licence and source in DESIGN.md.

Update `last_used` (YYYY-MM) after a site ships. Fonts on the overused list at the end are not in these pools.

## Funeral home

Readable at 18px+ for older readers; calm, dignified. Experimental or novelty display faces read as gimmicky here, so no Velvetyne. Expressive moves come from layout and photography.

### Display

| Family | Voice | Licence | Source | Notes | last_used |
|---|---|---|---|---|---|
| Spectral | quiet, bookish screen serif | OFL | GF | light-ish colour; use 500 for headings | — |
| Libre Caslon Display | formal, printed, old-town | OFL | GF | display sizes only (≥32px); pair with Libre Caslon Text or a sans | — |
| Castoro | warm Dutch-style serif | OFL | GF | regular + italic only; good for short headings | — |
| Gloock | high-contrast, sculpted | OFL | GF | one weight; large sizes only; strong but not luxury-cliché | — |
| Brygada 1918 | sturdy, civic, early-20th-century | OFL | GF | variable weight; fits register or memorial-card directions | — |
| Marcellus | engraved, inscriptional | OFL | GF | lettering on stone; sentence case only, never tracked caps headings | — |
| Hedvig Letters Serif | calm, contemporary serif | OFL | GF | optical size axis; works small and large | — |
| Ibarra Real Nova | classical Spanish book face | OFL | GF | elegant without being script | — |
| Linden Hill | old-style, literary | OFL | GF | regular + italic; short headings only | — |
| Petrona | soft, rounded serif | OFL | GF | wide weight range; also body | — |
| Fanwood Text | small-press, intimate | OFL | GF | regular + italic; headings ≥28px | — |
| Gambetta | lively transitional serif | ITF FFL | FS | self-host, no redistribution | — |
| Erode | firm, contemporary serif | ITF FFL | FS | self-host, no redistribution | — |
| Sentient | plain, gentle serif | ITF FFL | FS | self-host, no redistribution; also body | — |

### Body

| Family | Voice | Licence | Source | Notes | last_used |
|---|---|---|---|---|---|
| Source Serif 4 | steady, readable serif | OFL | GF | optical sizes; excellent at 18px | — |
| Literata | warm reading serif | OFL | GF | made for long reading; opsz axis | — |
| Alegreya | humanist, calligraphic serif | OFL | GF | has a matching Alegreya Sans | — |
| Gelasio | Georgia-metric serif | OFL | GF | metric match makes a CLS-free fallback | — |
| Public Sans | neutral, civic sans | OFL | GF | very clear; tabular figures | — |
| Atkinson Hyperlegible Next | legibility-first sans | OFL | GF | made for low vision; confirm licence in download | — |
| Albert Sans | friendly geometric-humanist | OFL | GF | variable | — |
| Figtree | clear, gentle sans | OFL | GF | good at small sizes | — |
| Source Sans 3 | plain humanist sans | OFL | GF | pairs with Source Serif 4 as one system | — |
| Switzer | neutral grotesque | ITF FFL | FS | self-host, no redistribution | — |

## Metal fabrication

Direct, specific, capable. Width contrast and sturdy grotesques suit the trade; avoid the stencil and distressed-type cliché. Spec tables need tabular figures. Oswald and Bebas Neue are the category's stock answer (overused list).

### Display

| Family | Voice | Licence | Source | Notes | last_used |
|---|---|---|---|---|---|
| Archivo | grotesque with width axis | OFL | GF | use the wide or condensed width for headings, normal for text | — |
| Big Shoulders Display | tall, civic, signage | OFL | GF | Chicago-signage origin; headings only | — |
| Barlow Condensed | road-sign, compact | OFL | GF | pairs with Barlow for one system | — |
| Sofia Sans Extra Condensed | narrow, crisp | OFL | GF | large sizes; long product names fit | — |
| Antonio | narrow, firm | OFL | GF | caps-like presence without caps | — |
| Saira Condensed | technical, squared | OFL | GF | pairs with Saira | — |
| Mona Sans | grotesque with width axis | OFL | GH (also GF) | wide headings, regular text | — |
| Hubot Sans | squared, mechanical | OFL | GH | sibling of Mona Sans | — |
| Familjen Grotesk | sturdy, slightly quirky | OFL | GF | good in mid sizes | — |
| Schibsted Grotesk | newspaper grotesque | OFL | GF | firm headings; also body | — |
| Anybody | width and weight axes | OFL | GF | can go very wide or very narrow; pick one width | — |
| Zilla Slab | slab, engineered | OFL | GF | slab voice without Western-saloon cliché | — |
| Terminal Grotesque | raw, pixel-edged | OFL | VT | display only; only for a deliberately rough direction | — |
| Sporting Grotesque | squared, sporty | OFL | VT | display only; check latin-ext | — |
| Outward | ultra-condensed | OFL | VT | very large sizes only | — |
| Tanker | heavy, poster | ITF FFL | FS | self-host, no redistribution; one weight | — |
| Panchang | wide, flat | ITF FFL | FS | self-host, no redistribution | — |

### Body

| Family | Voice | Licence | Source | Notes | last_used |
|---|---|---|---|---|---|
| Archivo | plain grotesque | OFL | GF | normal width for text | — |
| Barlow | plain, slightly rounded | OFL | GF | tabular figures | — |
| Public Sans | neutral, civic | OFL | GF | very clear tables | — |
| Chivo | sturdy grotesque | OFL | GF | variable | — |
| Libre Franklin | American gothic | OFL | GF | classic trade feel | — |
| Red Hat Text | open, technical | OFL | GF | has Red Hat Mono sibling | — |
| Overpass | highway-sign derived | OFL | GF | has Overpass Mono | — |
| Sofia Sans | crisp, neutral | OFL | GF | width family available | — |
| Source Serif 4 | readable serif | OFL | GF | for "book serif in a trade" directions | — |
| Supreme | neutral grotesque | ITF FFL | FS | self-host, no redistribution | — |

### Mono (only for literal data or code)

| Family | Licence | Source | Notes | last_used |
|---|---|---|---|---|
| Martian Mono | OFL | GF | width axis | — |
| Red Hat Mono | OFL | GF | pairs with Red Hat Text | — |
| Spline Sans Mono | OFL | GF | soft | — |

Prefer the body face's tabular figures over mono for spec tables.

## General pool (any niche, after the niche pool)

### Display

| Family | Voice | Licence | Source | Notes | last_used |
|---|---|---|---|---|---|
| Young Serif | heavy, friendly old-style | OFL | GF | one weight | — |
| Bodoni Moda | high-contrast didone | OFL | GF | large sizes only; fashion-adjacent | — |
| Besley | Clarendon-style, warm | OFL | GF | strong headings | — |
| Libre Bodoni | sturdier didone | OFL | GF | text-safe didone | — |
| Sora | geometric, open | OFL | GF | — | — |
| Rethink Sans | contemporary grotesque | OFL | GF | also body | — |
| Wix Madefor Display | neutral, confident | OFL | GF | pairs with Wix Madefor Text | — |
| Darker Grotesque | tall, compressed | OFL | GF | large sizes | — |
| Alumni Sans | narrow, tall | OFL | GF | — | — |
| Basteleur | sharp, expressive serif | OFL | VT | display only; culture/food/events | — |
| Avara | angular serif | OFL | VT | display only | — |
| Happy Times at the IKOB | quirky Times-like serif | OFL | VT | display only | — |
| Fengardo Neue | rounded geometric | OFL | VT | display only | — |
| Zodiak | high-contrast serif | ITF FFL | FS | self-host, no redistribution | — |
| Boska | sharp display serif | ITF FFL | FS | self-host, no redistribution | — |
| Melodrama | condensed display serif | ITF FFL | FS | self-host, no redistribution | — |
| Telma | rounded display | ITF FFL | FS | self-host, no redistribution | — |

### Body

| Family | Voice | Licence | Source | Notes | last_used |
|---|---|---|---|---|---|
| Petrona | soft serif | OFL | GF | — | — |
| Faustina | compact serif | OFL | GF | — | — |
| Piazzolla | sturdy serif, opsz | OFL | GF | — | — |
| Commissioner | humanist-grotesque, flare axis | OFL | GF | — | — |
| Golos Text | neutral, Cyrillic-strong | OFL | GF | — | — |
| Onest | clear grotesque | OFL | GF | — | — |
| Karla | quirky grotesque | OFL | GF | — | — |
| Gantari | geometric, friendly | OFL | GF | — | — |
| Author | plain grotesque | ITF FFL | FS | self-host, no redistribution | — |
| Synonym | neutral sans | ITF FFL | FS | self-host, no redistribution | — |

## Overused - needs a reason (list dated 2026-11)

A face below may be used only with a written non-category reason in DESIGN.md Typography (e.g. the client's existing sign or logotype uses it), plus a passing `niche_log.py check`. Review this list quarterly with `tells.md`.

| Status | Families |
|---|---|
| active (default for AI/template builds) | Inter, Roboto, Open Sans, Lato, Arial/system-ui, Poppins, Montserrat, Raleway, Space Grotesk, Plus Jakarta Sans, IBM Plex (Sans/Serif/Mono), JetBrains Mono, Playfair Display, Crimson (Text/Pro) |
| watch (fashionable "fresh" picks, now common) | Fraunces, Newsreader, Instrument Serif, Instrument Sans, Bricolage Grotesque, DM Sans, DM Serif, Outfit, Geist, Cormorant (all cuts), Lora, Syne |
| watch (fashionable free-foundry picks) | Satoshi, Clash Display, General Sans, Cabinet Grotesk |
| watch (Bexven addition 2026-11: category stock answers) | Oswald and Bebas Neue (trades), Cinzel and script faces (funeral), Merriweather, Nunito, Manrope, Work Sans, Libre Baskerville, Josefin Sans |
