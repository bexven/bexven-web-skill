# 47 — Butterick's Practical Typography
https://practicaltypography.com · Website (online book, Matthew Butterick) · License: "© 2010–26 Matthew Butterick. All rights reserved." Reproduction needs written permission; fair use excepted. The author asks readers to pay ($19–49) or buy his fonts. Our rules are paraphrased; no text copied · Stars n/a · Read 2026-11-18 (summary-of-key-rules, typography-in-ten-minutes, headings, websites, how-to-pay, legal)

## 1. What it is
An opinionated, practical typography guide aimed at writers (originally lawyers). Its key-rules summary gives firm numbers for body text that map well to web CSS defaults.
## 2. How it works
Get body text right first (size, leading, measure, font), then fix details (quotes, dashes, caps, emphasis, headings). Treat it as guidance, not dogma.
## 3. Rules
- [process] Set body text first (size, line-height, measure, font) before styling headings, hero or decoration
- [type] Body size on the web: 15–25 px (we default 17–20 px desktop, never below 16 px mobile). Adjust per font, since x-heights differ
- [type] Line-height 1.2–1.45 for body (unitless CSS, e.g. `line-height: 1.4`). Tighten for large headings (~1.05–1.2)
- [type] Measure: an average of 45–90 characters per line (2–3 lowercase alphabets). Use `max-width: 60–70ch` on text containers. Never let text run edge to edge on wide screens
- [type] Choose a deliberate, quality font. Avoid default system fonts (Arial, Times New Roman, also overused Georgia/Verdana) as the brand face
- [type] Be careful with the most common free web fonts; prefer less-seen or licensed fonts that fit the client's character (check the licence for web + WordPress use)
- [type] No goofy/novelty fonts or monospace for body text
- [type] Emphasis: use bold or italic sparingly, and never both together. Never underline except links
- [type] All caps only for short strings (under one line: eyebrows, buttons, nav). Always add 5–12% letter-spacing (`letter-spacing: .05–.12em`)
- [type] Use real small caps only (`font-variant-caps` with fonts that have them). Never fake them by scaling capitals
- [type] Kerning always on (`font-kerning: normal`; enable `text-rendering: optimizeLegibility` / ligatures where the font supports them)
- [type] Centered text sparingly: short headings or short hero lines only, never multi-line body paragraphs
- [type] Paragraph separation: use either space between paragraphs (about 0.5–0.75em on web) or a first-line indent, never both. Web default: spacing, no indent
- [type] Justified text only with hyphenation (`hyphens: auto` + `lang` attribute). Default to left-aligned ragged-right on the web
- [type] Headings: no more than 3 levels in content (2 is better). Make them visibly different using spacing and weight rather than giant size jumps on content pages
- [type] Headings: add space above and below, with more above than below so the heading belongs to the text that follows
- [type] Headings: sentence case preferred. No all caps for long headings, no underline, no hyphenation (`hyphens: manual`). Avoid bold+italic together
- [type] Avoid oversized headings and tiny body text on websites (a common web failure)
- [copy] Curly quotes and downward-pointing apostrophes (’), not straight ' and ". Use straight marks only for feet/inches. Check that CMS/Elementor output keeps them
- [copy] Use real dashes: en dash (–) for ranges, em dash (—) or spaced en dash for breaks. Never use "--"
- [copy] Use the ellipsis character (…), ©/™/® symbols, not (c)/TM
- [copy] One space after sentences. No runs of spaces or `&nbsp;` used for layout
- [copy] Ampersands only in proper names/logos, not as a shortcut in body copy
- [copy] Exclamation points: almost none. At most one per page of copy
- [code] Use non-breaking spaces where a break would read badly (e.g. between a number and its unit, "§ 5", short last words in headlines)
- [layout] Don't crowd page edges with dense blocks of nav links. Give text generous margins
- [layout] Be wary of building layouts from big flat blocks of colour
- [brand] Take visual ideas from books, posters, signage, print and the client's own world, not from current web trends
- [brand] Avoid copied web trends: full-screen video backgrounds, default grids, hamburger-over-stock-photo heroes
- [tooling] Frameworks/templates (Bootstrap, Elementor kits) make sites look alike. Override their default type scale and spacing for every client
## 4. AI tells / anti-patterns it bans
Default system/most-popular free fonts, straight quotes and "--", all-caps paragraphs, bold+italic, underlined headings, centered body text, edge-to-edge text, huge headings over tiny body, trend-driven heroes (video bg, hamburger over stock photo), template sameness.
## 5. Data, assets and scripts it ships
No scripts. Commercial fonts (MB Type, $119+) sold separately; not needed.
## 6. Area
design (typography) / QA
## 7. Take / skip
Take: the numeric body-text rules as defaults plus a typography QA checklist (quotes, dashes, caps tracking, measure, paragraph spacing, heading levels). Skip: the 10–12 pt print figures; the strict anti-free-font stance (we use Google/Adobe/Fontshare fonts, but pick less-common ones and pair them with care); modest content-heading sizes do not apply to marketing heroes, where we can use display sizes. Respect copyright: never paste the book's text into the skill.
## 8. Open questions
- Conflict: Butterick discourages Google Fonts generally; our skill likely relies on free fonts. Resolve with a "less overused + licence-checked" font list.
- Conflict: "avoid large colour blocks" vs common section-band layouts; treat as a caution, not a ban.
- SUGGESTED: The Elements of Typographic Style Applied to the Web - http://webtypography.net - CSS-specific versions of classic typography rules
