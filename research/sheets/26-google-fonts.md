# 26 — Google Fonts
https://fonts.google.com · Website (free font library + CDN API) · Mostly SIL OFL 1.1 (some Apache 2.0, Ubuntu Font Licence) · Stars n/a · read 2026-11-18 (homepage + /faq fetched but JS-rendered: only the title came back; terms below are from prior knowledge, verify per family)

## 1. What it is
Google's library of about 1,700 open-licensed families, served from fonts.googleapis.com / fonts.gstatic.com or downloadable. Many are variable fonts (one file with weight/width/opsz axes).
## 2. How it works
Browse, then either use an embed `<link>` (CDN) or download the files. The licence is in each family's "License" tab and ships as OFL.txt in the download.
## 3. Rules
- [type] OFL/Apache allow commercial use, web embedding, self-hosting, bundling in themes and Elementor Custom Fonts upload, and modification. Under OFL you can't sell the font file on its own, and a modified version can't use a Reserved Font Name.
- [wp] Always self-host. A Munich court ruling (LG München I, 20 Jan 2022, 3 O 17493/20) found that loading from the Google CDN without consent sends the visitor's IP to Google, which breaches the GDPR (EUR 100 damages). It was followed by waves of warning letters. In Elementor, turn on "Load Google Fonts Locally" or upload the WOFF2 via Custom Fonts, and confirm in DevTools that no requests go to googleapis/gstatic.
- [perf] Prefer variable WOFF2, subset it (latin / latin-ext), preload one or two files, and use font-display: swap.
## 4. AI tells / anti-patterns it bans
Over-used defaults that read as AI- or template-made: Inter, Poppins, Montserrat, Roboto, Open Sans, Lato, Raleway, Playfair Display (as a "luxury" serif), DM Sans, Space Grotesk, Plus Jakarta Sans. Only use them deliberately.
## 5. Data, assets and scripts it ships
Font files (TTF/variable TTF in the zip). Developers API (needs a key). github.com/google/fonts holds the sources and licences.
## 6. Area
design / development (type, perf, legal)
## 7. Take / skip
Take: the safest licence source. Build a per-niche shortlist from less-used families (e.g. Fraunces, Instrument Serif, Bricolage Grotesque, Familjen Grotesk, Newsreader, Hanken Grotesk) with a licence column, and always self-host. Skip: CDN embeds, and the default families above.
## 8. Open questions
- Fetch returned no body (JS app). Licence and FAQ details weren't verified live this session.
- SUGGESTED: google-webfonts-helper - https://gwfh.mranftl.com - download self-host WOFF2 with CSS
- SUGGESTED: github.com/google/fonts - https://github.com/google/fonts - per-family licence files you can read by machine
