# 46 — Laws of UX
https://lawsofux.com · Website (principle catalogue, by Jon Yablonski; companion O'Reilly book) · License: no licence or copyright notice found on homepage or law pages; /about/ returned 404. Treat as all rights reserved: paraphrase only · Stars n/a · Read 2026-11-18

## 1. What it is
A curated catalogue of 30 psychology/HCI principles (Gestalt, cognitive load, decision-making, memory), each with a short definition, takeaways and sources. Good as a checklist of the "why" behind layout and conversion decisions.
## 2. How it works
One page per law (definition, takeaways, origin, further reading), tagged by theme. Our skill should turn each law into a concrete build/QA rule, below.
## 3. Rules
- [components] Aesthetic-Usability: polish the first screen (type, spacing, imagery) because people forgive minor usability issues on attractive sites. Still run usability QA, since looks can hide real problems
- [nav] Choice Overload: keep the main nav to about 5–7 top-level items. Put secondary links in the footer
- [layout] Chunking: break long service copy into short labelled groups (heading + 2–4 lines). No wall-of-text sections
- [copy] Cognitive Bias: use social proof (reviews, years in business, local certifications) near CTAs, honestly and with real data only
- [layout] Cognitive Load: one primary job per section. Remove decorative elements that carry no meaning
- [perf] Doherty Threshold: give feedback on any interaction within 400 ms (button state, spinner, skeleton). Target LCP < 2.5 s on the Vercel demo
- [components] Fitts's Law: make primary CTAs and tap targets at least 44×44 px with generous spacing. Put a phone/quote CTA where the thumb reaches on mobile
- [process] Flow: remove friction from the primary path (quote form, call button). No interstitials or popups before the user has read anything
- [forms] Goal-Gradient: show progress on multi-step forms ("Step 2 of 3"). Pre-fill or collapse optional steps so the finish feels close
- [nav] Hick's Law: give one primary CTA per viewport plus at most one secondary. Do not show 4 equal buttons
- [nav] Jakob's Law: keep conventions (logo top-left links home, nav top-right or top, contact in footer, phone clickable). Be distinctive in visual identity, not in where things are
- [layout] Common Region: use a background/border to group related items (e.g. opening hours + address card). Don't box everything, or the grouping signal is lost
- [space] Proximity: space within a group must be clearly smaller than space between groups (e.g. 8–16 px inside, 48–96 px between sections). Labels sit close to their fields
- [layout] Prägnanz: prefer simple, readable shapes and layouts. Avoid ambiguous overlapping compositions that need decoding
- [components] Similarity: style every link/button of the same role identically, and make different roles look different (never style a non-clickable label like a button)
- [layout] Uniform Connectedness: connect related steps visually (line, shared container) in process/timeline sections
- [process] Mental Model: use the client's customers' words and expected page structure (e.g. funeral home: services, obituaries, pre-planning, contact). Do not invent unusual IA
- [copy] Miller's Law: don't use 7±2 as a hard limit on items. Do group long lists (services, FAQs) into small, scannable sets
- [process] Occam's Razor: remove any element that can go without loss of meaning. Fewer fonts, colours and component variants
- [forms] Paradox of the Active User: put help inline (placeholders aren't labels; use hints and tooltips at point of need). Never rely on instructions people won't read
- [qa] Pareto: spend QA time on the pages and devices that carry most traffic (homepage, contact, mobile)
- [forms] Parkinson's Law: keep forms short (name, contact, message). Use autofill attributes (autocomplete) to cut completion time
- [copy] Peak-End: design a strong moment (hero or key proof) and a good ending (clear footer CTA, friendly thank-you page after form submit)
- [forms] Postel's Law: accept flexible input (phone formats, spaces, case). Validate kindly and output clean data
- [image] Selective Attention: users ignore anything that looks like an ad (banner-blindness). Don't style key info as banners/carousels
- [layout] Serial Position: put the most important nav items and content first and last (e.g. Contact as the last nav item, key CTA in hero and closing section)
- [process] Tesler's Law: absorb complexity in the build (smart defaults, pre-selected options) rather than pushing it to the visitor
- [colour] Von Restorff: make only one element per view stand out (accent colour on the primary CTA). Don't rely on colour alone; use size, shape or label too
- [forms] Working Memory: never make users remember info across pages. Keep context visible (selected service shown on the quote form)
- [copy] Zeigarnik: show incomplete progress to encourage completion (e.g. form progress), and use it sparingly and honestly
## 4. AI tells / anti-patterns it bans
Indirectly: too many equal CTAs, card grids where everything looks alike (no hierarchy, so nothing stands out per Von Restorff), unconventional nav for novelty, cluttered sections.
## 5. Data, assets and scripts it ships
None usable (posters/book are commercial). No code.
## 6. Area
design / QA (UX principles)
## 7. Take / skip
Take: the rules above as a UX QA checklist (tap targets, one primary CTA, proximity spacing, conventional nav, short forms, progress feedback). Skip: the site's own visual style and posters (copyrighted). Skip treating Miller's 7±2 as a hard number. Jakob's Law vs our "don't look generic" goal: keep conventions for where things are and how they behave, and get distinctiveness from type, colour, imagery and section rhythm.
## 8. Open questions
- Licence not stated anywhere we could see; /about/ returned 404. Assume copyright Jon Yablonski; paraphrase only.
- The brief named "each law"; the site currently lists 30 (all covered).
- SUGGESTED: NN/g articles on Fitts/Hick/Jakob - https://www.nngroup.com - evidence-backed detail with web examples
