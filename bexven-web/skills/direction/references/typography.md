# Typography

Loaded at step 6. How to choose and pair faces, set the scale, and record licences. The pools themselves are in `font-pools.md`.

## 1. Choosing faces

- One family, or two clearly distinct ones, each with one role (display vs body) and no crossover. A third face only for a literal mono/code/data role.
- Choose from `font-pools.md` (niche pool first, then the general pool). No font from memory "because it is a good default".
- Fonts on the overused list (in `font-pools.md` and `tells.md`) need a written non-category reason in DESIGN.md Typography (e.g. "the client's sign is set in it"). "It looks elegant" or "it suits funeral homes" is a category reason and does not count.
- Reuse limits (checked by `niche_log.py check`): the same display font never in any of the last 5 sites in the niche, nor in 2 of the last 5 Bexven sites overall.
- Question subject associations: funeral → script or Trajan-style caps; fabrication → stencil, condensed caps; law → Garamond. These are the rut.
- Never a system or installed face (system-ui, Arial, Georgia, Impact, Times) as the display or brand voice. They are fine in the fallback chain.
- Display-only or experimental faces (most Velvetyne, some Fontshare) pair with a sturdy text face; check weight range, italics and hinting at body sizes.
- Check glyph coverage for the client's language before choosing: diacritics, Dutch ij, German ß, Polish ł, names on obituaries. Test with real names from the client's notices or staff list.
- Set the body text first (face, size, line-height, measure), then headings, hero and decoration.

## 2. Pairing method

1. From the direction's type voice, pick the body face that reads best at 17-19px on a phone (open apertures, clear x-height, real italic).
2. Pick the display face for contrast on one dimension only (structure: serif vs sans; or width; or weight), never several at once.
3. Set a real heading and a real paragraph from the client's content side by side; reject pairings where the two faces argue or look like one face.
4. Record both with licence and source in DESIGN.md.

## 3. Emphasis device (choose exactly one)

| Device | Means | Example |
|---|---|---|
| Weight | hierarchy by 400 → 600 inside one family | single-family grotesque |
| Size | big display vs calm body, weights close | serif display at 500 over 400 body |
| Case | caps for one short UI role only (nav or buttons) | tracked +0.06-0.12em, never headings over one line |
| Face | serif display vs sans body | the classic two-face pair |

Never: a single accented word in a headline (italic, bold or colour switch), marker highlights, bold + italic together, underline except links.

## 4. Scale and rhythm (defaults)

| Item | Default |
|---|---|
| Body size | 18px desktop (17-19), ≥16px mobile, ≥18px for older audiences |
| Body line-height | 1.5 (1.45-1.6 by x-height); light text on dark +0.05 |
| Measure | `max-width: 65ch` (62-70ch) |
| Ratio | 1.2-1.333 for content; the hero may jump further once |
| Display cap | `clamp(…, 6rem)` maximum |
| Large heading leading | 1.0-1.2 |
| Weights | about 400/500/600; 700+ rarely; nothing under 300 for body or UI |
| Display tracking | −0.01 to −0.03em at 32px+, never tighter than −0.04em |
| Small text (11-13px) | +0.01-0.02em |
| Sizes above the fold | max 3 |
| Heading levels in content | 2-3, distinguished by spacing and weight more than size |

Named roles in DESIGN.md front matter: `display`, `headline`, `title`, `body`, `label`, `caption`, each with fontFamily, fontSize, fontWeight, lineHeight and (where non-zero) letterSpacing. Reserve the biggest style for one context only.

## 5. Case and mono

- Sentence case for headings, buttons and nav. A brand may choose Title Case in DESIGN.md; then apply it everywhere, never mixed.
- No caps or mono micro-labels by default (the "broadsheet kit" tell).
- Mono only when the content is literally code or data (a spec table may use tabular figures of the body face instead, which is usually better).
- Real small caps only (`font-variant-caps` on a font that has them).

## 6. Polish the build must carry (note it in DESIGN.md if the face lacks a feature)

- `text-wrap: balance` on headings, `pretty` on paragraphs.
- `font-variant-numeric: tabular-nums` for hours, prices, dates, specs. Check the face has tabular figures.
- Curly quotes, real apostrophes, en dash for ranges (9–17h), ellipsis character, non-breaking space between number and unit.
- Body left-aligned, ragged right; centre only short lines.

## 7. Licences and loading

- Read the licence before use and record it: OFL (Google Fonts, Velvetyne, most GitHub foundries) or ITF FFL (Fontshare). Keep the licence file next to the WOFF2.
- OFL: commercial use, self-hosting, Elementor Custom Fonts upload and theme bundling allowed; don't sell the font file alone.
- ITF FFL: free for commercial use on the client's own site, self-hosted; **no redistribution**: never in public repos, starter kits, sold themes or shared font folders. Verify the FFL text in the downloaded zip before the first use.
- Paid fonts only if the client pays, with the per-domain licence recorded. Never another company's proprietary brand face.
- Always self-host WOFF2, subset (latin / latin-ext via `unicode-range`), `font-display: swap`, one variable file where possible, preload only 1-2 critical files. Budget: ≤2 families, ≤4 files, ≤100KB total.
- No requests to fonts.googleapis.com, fonts.gstatic.com or api.fontshare.com (GDPR; a Munich court fined CDN loading in 2022).
- Fallback chain with a metric-matched local font (`size-adjust`, `ascent-override`) if the swap shifts layout; the build tunes it.

## 8. Update the pool

After ship, set `last_used` for the faces in `font-pools.md` (YYYY-MM) and run `niche_log.py add`. If a face turns up in many AI-made sites, move it to the watch or overused list with the date.
