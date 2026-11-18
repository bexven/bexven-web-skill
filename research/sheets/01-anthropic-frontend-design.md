# 01 — Anthropic frontend-design
https://github.com/anthropics/skills/tree/main/skills/frontend-design · Claude skill (single SKILL.md, ~9 KB, no assets) · Apache-2.0 (LICENSE.txt in each skill folder; also brand-guidelines, theme-factory, webapp-testing, skill-creator) · ~197k stars (repo) · commit e4bb5d9, 2026-11-16 (read 2026-11-18)

## 1. What it is
Anthropic's official skill for "distinctive, intentional" UI design. It is pure prose with no scripts or data. It frames Claude as the design lead of a studio whose client has already rejected templated work. It is the closest existing thing to Bexven's goal: it names the current AI-design clusters explicitly and makes a plan, check, build, critique loop mandatory.

## 2. How it works
- **Persona and stakes:** every client gets a distinct identity, and the client pays for a point of view, so taking risks is allowed when the brief justifies them.
- **Ground in the subject:** if the brief doesn't name the product, audience and main job, propose them and confirm. Distinctive choices come from the subject's industry, materials and vernacular. Use real content throughout.
- **Two passes:**
  1. Write a compact token plan: 4–6 named hex colours; typefaces and their roles; a layout concept as one-sentence prose plus ASCII wireframes, with alignment stated; and the principles that make this page unique.
  2. Review the plan against the brief. Mentally run a similar prompt: if you would land in the same place, that part is a default, so revise it and say what changed and why.
- **Build, then critique:** take screenshots and review them. "Remove one accessory" (Chanel). Keep notes on what was tried so later passes do something new.
- **The brief overrides the tells.** Where the brief pins down a visual direction, follow it exactly, even when it asks for one of the listed AI looks. The tells only govern the axes the brief leaves open.
- **Writing section:** copy is design content. Write from the user's view, use active voice, and make each element do one job.

### Sibling skills (skimmed)
- **brand-guidelines:** applies Anthropic's own brand: #141413 dark, #faf9f5 light, #d97757 orange plus blue and green accents, Poppins headings, Lora body. It is built for python-pptx output. It shows the pattern for a brand-token skill (palette, font roles, fallbacks). It is also the source of tell #1: cream with a serif and terracotta is literally Claude's own look.
- **theme-factory:** 10 preset themes (`themes/*.md`, each with 4 hex colours, a header/body font pair and a "best used for" line) plus `theme-showcase.pdf`. Flow: show the showcase, ask the user to pick, wait for confirmation, apply. It can also generate a custom theme and show it for review. The fonts are system defaults (DejaVu Sans/Serif, FreeSans/FreeSerif), and the names are generic (Ocean Depths, Golden Hour…). That is the opposite of frontend-design's "no default families" rule. Useful only as a file format for named presets.
- **webapp-testing:** Python Playwright. Its decision tree: if the page is static HTML, read the file for selectors; if it is a dynamic app, start the server through `scripts/with_server.py` (lifecycle helper, multi-server). Then recon before acting: wait for `networkidle`, take a screenshot or dump the DOM, then act. Bundled scripts are treated as black boxes (`--help` first, don't read the source) to save context. Examples cover element discovery, file:// static pages and console-log capture.
- **skill-creator:** a meta-skill for drafting a skill, testing it, evaluating the results and iterating. Key guidance:
  - **Size:** SKILL.md under ~500 lines. When it gets close, add a layer of hierarchy with clear pointers to where to read next. Reference files over 300 lines get a table of contents.
  - **Progressive disclosure, three levels:** metadata (~100 words, always loaded) → SKILL.md body (loaded on trigger) → bundled resources (read on demand; scripts can run without being loaded). When a skill covers several frameworks or domains, put each variant in its own reference file.
  - **Description:** this is the trigger. Put all "when to use" information there, not in the body. Make it a bit "pushy", because Claude tends to undertrigger skills: list adjacent phrasings, including requests that never name the skill.
  - **Style:** explain why a rule matters rather than writing heavy MUSTs, and don't overfit to examples.
  - **Evals:** 2–3 realistic prompts, each run with the skill and without it (or against the old version), in parallel. Draft assertions while the runs go, then do an analyst pass and a human review in an HTML viewer.
  - **Trigger evals:** 20 queries, half should trigger and half should not, built on near-misses. They are optimised by `run_loop.py` with a 60/40 train/test split and 3 runs per query.

## 3. Rules
- [process] If the brief lacks subject, audience or primary job, propose them and confirm before designing
- [process] Draw visual choices from the subject's industry, materials and vernacular, not from a style trend
- [process] Write the token plan first (4–6 named hex colours, type roles, layout prose plus ASCII wireframe, alignment, principles), then review it against the brief before writing code
- [process] Run the "would a similar prompt land here too?" test on every plan item. Revise any default and note what changed and why
- [process] The brief's explicit visual direction beats every anti-tell rule. Tells only govern the axes the brief leaves free
- [layout] Open the hero with the most characteristic thing in the subject's world (headline, image, animation, demo). Treat "big number + small label + stats + gradient accent" as a default to justify, not to reach for
- [type] Use one family or two clearly distinct ones. Don't use the families you would pick for any project
- [type] Set a clear scale per Bringhurst (The Elements of Typographic Style), with intentional weights, widths and spacing. Headline type should be an active design element
- [type] Lines under 80 characters. Serif body text may run slightly longer and gets slightly more line-height than sans
- [type] Don't accent a single word in a headline (italic, bold or a colour switch)
- [type] Don't use all-caps labels or unneeded labels above content
- [layout] Structural devices (borders, numbering, eyebrows, dividers) must encode information. Use 01/02/03 only for real sequences
- [motion] Allow one orchestrated moment (a page-load sequence or one reveal) rather than scattered effects
- [motion] Don't fade-and-slide-up every section, and don't add hover transitions to every card
- [motion] Motion that responds to a user action (open, expand, confirm) is fine when it shows what changed
- [components] Avoid the SaaS card kit: identical rounded cards, one radius everywhere, the same rgba(0,0,0,.1) shadow, gradient washes
- [brand] Spend boldness in one place: one memorable element, everything around it quiet. Cut any decoration that doesn't serve the brief
- [a11y] Silent quality floor: responsive to mobile, visible keyboard focus, prefers-reduced-motion respected, accessible contrast, harmonious palette
- [code] Watch CSS specificity clashes (e.g. `.section` padding vs `.cta` margin cancelling each other)
- [qa] Screenshot and critique while building. Remove one accessory before shipping
- [process] Keep notes on what was tried so the next project does something new
- [copy] Write from the user's view in plain words ("notifications", not "webhook config"). Describe, don't sell
- [copy] Active voice. A CTA names its exact result ("Save changes", not "Submit"). Keep an action's name the same through the flow (Publish → Published)
- [copy] Errors explain what happened and how to fix it, with no apologies. Empty states invite action
- [copy] Sentence case, plain verbs, no filler, one job per text element

## 4. AI tells / anti-patterns it bans
The skill names five clusters. It calls them legitimate for some briefs, but defaults when the brief didn't ask for them:
1. Warm cream background (~#F4F1EA) with a high-contrast serif display and a terracotta/clay accent (~#D97757, Claude's own UI accent).
2. Near-black background with a single acid-green or vermilion accent.
3. Broadsheet look: hairline rules, zero radius, dense newspaper columns.
4. SaaS card kit: identical rounded cards, one radius, the same soft grey shadow, decorative gradient washes.
5. Template chrome:
   - a tracked ALL-CAPS eyebrow above every heading
   - "A · B · C" middle-dot meta strings
   - "WORD — fragment" labels with a spaced em dash
   - #0B0B0B/#111 standing in for black
   - monospace for small data labels
   - "→" appended to link and button text

It also flags:
- a single accented word in a headline
- all-caps labels
- unneeded labels above content
- fake 01/02/03 numbering
- the big-stat hero with a gradient accent
- fade-up on every section
- hover transitions on every card

## 5. Data, assets and scripts it ships (and what they need: Node, Python, Chrome)
- **frontend-design:** none (prose only).
- **brand-guidelines:** none (assumes python-pptx and installed Poppins/Lora).
- **theme-factory:** 10 theme .md files and a PDF showcase.
- **webapp-testing:** `with_server.py` and 3 example scripts. Needs Python, Playwright and Chromium.
- **skill-creator:** Python scripts (eval runner, description optimiser, benchmark aggregator, packager, validator), an HTML eval viewer and 3 subagent prompts (grader, comparator, analyzer). Needs Python and the `claude` CLI. Not run, per the brief.

## 6. Area
Design (primary), plus copy and process. The siblings cover brand (brand-guidelines, theme-factory), QA (webapp-testing) and tooling (skill-creator).

## 7. Take / skip
**Take:**
- The whole tell list, verbatim in spirit, as our baseline "default detector". It is current, from the model vendor, and includes the newer cream/serif/terracotta and black/acid-green clusters.
- The plan → self-review → build → screenshot-critique loop, with the "similar prompt" test.
- "The brief wins" precedence. Bexven clients sometimes really do want a dark or serif look.
- Subject-grounding as the main source of difference. This is the key to making two funeral homes look different.
- The copy rules, the quality floor, and the CSS specificity warning (very relevant to Elementor/global CSS).
- The "notes on what was tried" idea. Bexven should make it concrete with a per-niche log of palettes, fonts and layouts already used, so the next site in that niche avoids them.

**Take from siblings:**
- skill-creator's under-500-line SKILL.md with references split by stack (static HTML / Elementor / Shopify Liquid).
- skill-creator's pushy trigger description.
- skill-creator's with/without-skill eval runs. Use them to prove our skill actually beats baseline Claude on niche prompts.
- webapp-testing's recon-then-act Playwright pattern for our screenshot critique and QA step.

**Skip:**
- theme-factory's preset themes and system fonts. Fixed presets recreate sameness across clients, which is exactly what we are fighting. Keep only the file format idea (palette, fonts, "best for").
- brand-guidelines' content. It is Anthropic's own brand and *is* tell #1. Keep only the pattern (a per-client brand-token file).
- The persona fluff and the mandatory "confirm with client" step. In cold outreach there is no client to ask, so the skill should make and log assumptions instead.

**Conflicts with common advice:**
- It doesn't ban hover. It bans hover transitions on *every* card and welcomes feedback motion.
- Eyebrows aren't banned outright. They must carry information, and all-caps eyebrows on every heading are a tell.
- Purple/indigo gradients are not named specifically; it targets "gradient washes" in general.
- It prefers deliberate, subject-derived choices over randomisation.
- Light vs dark is neutral: both a cream and a near-black cluster are listed as tells.

## 8. Open questions
- The tell list is a moving target ("right now"). How should Bexven version and refresh it?
- How should "confirm with the client" map onto cold outreach? Probably: log assumptions in the plan.
- There are no examples or wireframe samples. Should our skill ship worked niche examples (with the risk that they become new defaults)?
- SUGGESTED: anthropics/skills `web-artifacts-builder` and `canvas-design` - https://github.com/anthropics/skills/tree/main/skills - siblings in the same repo that may hold more build or visual guidance (not read).
