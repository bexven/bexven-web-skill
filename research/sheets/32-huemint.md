# 32 — Huemint
https://huemint.com · Website + public API (ML palette generator) · Proprietary; public API "for non-commercial applications", as-is, no uptime guarantee · Stars n/a · Read 2026-11-18

## 1. What it is
AI colour-palette generator for brands, websites and illustrations that shows palettes applied to mockups.
## 2. How it works
User sets number of colours and an adjacency matrix: per colour pair, a CIE Delta-E contrast target (100 = max, 1 = min, 0 = not adjacent). Three engines: random sampling from a designer-palette distribution (top 1% matches kept), a transformer over a 4096-token colour codebook, and a diffusion model. Creativity slider = sampling temperature (0–2.4, default 1.2). Colours can be locked. POST api.huemint.com/color (mode, num_colors, temperature, num_results, adjacency, palette).
## 3. Rules
- [colour] Think of a palette as a graph: specify how strongly each pair that actually touches (text-on-bg, button-on-bg) must contrast, and leave non-touching pairs unconstrained
- [colour] Lock the client's existing brand colour and generate the rest around it
## 4. AI tells / anti-patterns it bans
n/a
## 5. Data, assets and scripts it ships
HTTP API only (no key documented); no downloadable data.
## 6. Area
design / tooling
## 7. Take / skip
Take: the adjacency-matrix idea as a reasoning method our agent can do itself (list touching pairs, set contrast targets, verify with WCAG/APCA). Skip: calling the API in client work — licence is non-commercial, and an agency pipeline is commercial; also uptime not guaranteed.
## 8. Open questions
Delta-E is not a legibility metric; contrast still needs a WCAG/APCA check. Commercial licensing terms not published.
