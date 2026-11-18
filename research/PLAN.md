# PLAN — Bexven web design skill (for approval; nothing built yet)

Date: 2026-11-18 · Inputs: `index.md`, `sheets/01–47`, `analysis/duplicates.md`, `analysis/conflicts.md`

---

## 1. What I read

| | Count |
|---|---|
| Resources on the list | 47 |
| Fully read (OK) | 39 |
| Partial (JS-rendered pages or details from prior knowledge, marked in the sheet) | 6: Google Fonts, Fontshare, Velvetyne (licence text not rendered), Magic UI, React Bits (effects list unconfirmed), Phosphor (read from GitHub README instead) |
| Failed | 2: **Land-book** and **Lapa Ninja** (HTTP 403 twice). Placeholder sheets marked unverified |
| GitHub repos cloned (`--depth 1`) | 16, all succeeded |
| Suggested extra resources logged (not read) | 25 (see `index.md` → Suggested) |

Notes:
- The GitHub API was blocked here, so star counts come from the repo web pages. Taste Skill's 118k looks high; re-check it.
- A usage limit cut off 7 subagents mid-run. Sheets 14–16 were already complete. The two website groups were resumed and finished.
- To save cost, the 29 small website sheets were written by 7 group subagents (still one sheet per site). Every repo, spec, tool and article got its own subagent.
- Safety: no scripts from the clones were run and nothing was installed. **Claude Code auto-discovered Impeccable's own `.claude/skills` inside the clone.** I didn't use it. Delete `sources/` (or move it out of any project folder) once we're done, so it can't load by accident.

## 2. Master-sheet outline (what `master/master-sheet.md` will cover)

Every rule is written in our own words, tagged by area and tagged with its source numbers.

0. **Principles**: why AI sites converge ("distributional convergence"); conventional structure plus distinctive identity (Jakob's law, split); tells move over time.
1. **Process**
   - **Brief intake**: mock stage (infer from the prospect's site, Google profile and photos, and log every assumption) vs build stage (assumptions become client questions).
   - **The category rut**: write down "the page this niche always ships", then avoid it.
   - **Direction shortlist**: 3–5 directions from the client's world, each differing on named axes.
   - **Seeded pick**: choose among the shortlist, checked against the niche history log.
   - **Direction contract + DESIGN.md**: written before the build and synced after QA.
2. **Niche layer**: per niche, required content, constraints (audience age, emotional register, trust signals, local SEO) and no-gos. Never a fixed palette or font. Funeral homes and metal fabrication first.
3. **Typography**: pairing method, one emphasis device, scale ratios, measure, line-height, body size, caps rules, typographic polish (curly quotes, real dashes, nbsp, tabular numbers, balanced wrapping), self-hosting and licences, per-niche font pools with a licence column and a `last_used` date.
4. **Colour**: OKLCH method; role tokens with paired "on" colours; a 12-step scale built from the brand hue; strategy (Restrained / Committed / Drenched); allowed places for the accent; ink and paper derived from the palette; how light vs dark is decided.
5. **Layout and composition**: section grammar, hero types, neighbouring sections differ, rules on zig-zag and card grids, first-viewport check, spacing scale (less space inside groups than between them).
6. **Components and patterns**: nav, header and footer, CTAs, forms, cards, reviews (real only), contact/NAP, maps, carousels (no auto-rotate), sticky UI.
7. **Imagery and icons**: photo priority (client > flagged stock > placeholder block); funeral-specific limits on people; one icon family and weight, inline SVG.
8. **Copy**: anti-slop vocabulary and sentence patterns, button labels, no invented facts, sentence case, local voice.
9. **Motion**: frequency gate, one moment per page, easing and duration tokens, reduced motion (gentler, not zero), CSS → Motion → GSAP ladder, no smooth scroll by default, Elementor entrance animations off.
10. **Accessibility**: enforced through numbers (contrast, targets, focus, labels, headings), checked by lint and audit, not by reminders in the creative brief.
11. **Performance and SEO**: Core Web Vitals thresholds, images, font loading, LocalBusiness JSON-LD, meta, headings.
12. **AI tells list** (dated, versioned): visual, layout, component, copy and motion tells, plus "moved" tells (cream + serif + terracotta, near-black + acid accent, hairlines + mono labels, SaaS card kit, template chrome, overused fonts, component-library effects).
13. **QA and critique**: script checks (`file:line` output), screenshot review at breakpoints, a critique rubric (specificity verdict, then heuristics, P0–P3), fresh-context final review, max 3 fix rounds.
14. **Build targets**
   - **Static HTML/CSS on Vercel**: preview deploys, `--prod` only on request.
   - **WordPress/Elementor**
     - Elementor MCP (built-in since 4.3): Variables → Global Classes → theme parts → Atomic containers → forms. Drafts only.
     - Fallback when MCP isn't available: kit JSON and template import.
   - **Shopify Liquid**: parked (see §6).
15. **Tooling**: Playwright (Python) as the default; Chrome DevTools MCP as an optional diagnostic layer (privacy flags); Playwright MCP only for interactive exploring.

## 3. Duplicates merged and conflicts (please confirm)

### Biggest merges (from ~804 raw rules → 218 canonical rules with 2+ sources)
1. Respect `prefers-reduced-motion`: 16 sources.
2. Contrast 4.5:1 body, 3:1 large text and UI: 11.
3. Specific verb+object labels, never "Submit" or "Read more": 9.
4. Animate only transform and opacity: 9.
5. Touch targets ≥44px: 9.
6. No decorative gradients, glass or glow: 9.
7. Take the direction from the client's world, not trends: 9.
8. Role-named tokens, no raw hex in components: 8.
9. Avoid overused default fonts: 8.
10. No fade-up on every section; one moment instead: 8.

Numeric merges: measure ~65ch, body line-height 1.5, exits ~75–80% of entry duration, screenshot widths 375/768/1024/1440, accent max 2 uses per screen.

### Conflicts and my recommended resolution
| # | Conflict | Recommendation |
|---|---|---|
| C1 | **Hover**: Taste/UUPM require lift/zoom; Anthropic calls hover-on-every-card a tell; Emil/Impeccable ban moving the card | Every interactive element gets a visible hover, focus and active state (colour, underline, shadow), gated by `(hover:hover) and (pointer:fine)`. No default lift or zoom on cards. At most one hover-motion idea per site, named in the direction, moving a child (e.g. image inside its frame), not the card. Keep `:active` press feedback; it's what touch users get. |
| C2 | **Eyebrows**: Impeccable bans them; Anthropic calls them a tell unless the brief overrides; real brands use them | Off by default. Allowed only when the label carries information the heading lacks (category, date, real step, location). Max 2 per page, never on every section. An explicit brief wins. (Correction: Taste doesn't allow "1–2 per page"; it bans tracked-caps labels. The max of 2 is our rule.) |
| C3 | **Purple**: Taste bans hue 270–330; UUPM recommends #6366F1 for AI; Open Design bans purple but ships Stripe | Lint-ban the Tailwind indigo/violet hexes and purple→blue/pink/cyan gradients as defaults. Violet only when it is the client's existing brand colour or the brief asks for it. Drop UUPM's AI-indigo advice. The ban targets **saturated** violet, not hue alone: a deep, low-chroma plum or aubergine from a funeral home's world is fine. |
| C4 | **Random vs deliberate** | Hybrid. Derive 3–5 directions deliberately from the client's world, each differing on ≥2 named axes (type voice, colour strategy, layout grammar, imagery treatment, signature moment). Remove any that collide with the niche history log. Then make a **seeded, logged random pick**. Deliberate quality, random tie-break, guaranteed variety within a niche. |
| C5 | **Light vs dark**: Impeccable uses scene of use; UUPM uses category; Taste allows dark for tech only | Decide from one sentence covering scene of use, audience and existing brand (e.g. "grieving family on a phone at night; older relatives; existing sign dark green on white"). Category only breaks a tie. Record the sentence in DESIGN.md. |
| C6 | Accessibility in design prompts (most sources) vs audit-only (Impeccable) | Enforce with numbers in the tokens plus lint plus an audit gate. No "remember accessibility" lines in the creative brief. |
| C7 | Title Case (Vercel guidelines) vs sentence case | Sentence case by default; a brand may choose Title Case in DESIGN.md, applied consistently. |
| C8 | WCAG 2 vs APCA | WCAG 2.2 AA is the pass/fail gate (it's the legal reference). APCA is advisory, for thin or light text. |
| C9/C10 | Scroll reveals and Elementor entrance animations vs "one moment" | No section reveals by default. Elementor entrance animations off globally. At most one motion moment per page (the hero counts), and the static mock and the WP build carry the same moment. Content is never hidden if JS fails. |
| C11/C12 | GSAP by default; smooth scroll for a "premium" feel | Ladder: CSS → Motion `animate()/inView()` → GSAP only for a named timeline, scroll or SVG moment. Native scroll; Lenis only for pinned storytelling. |
| C13/C14 | Taste's rigid section heights, hidden contacts and no testimonials | Drop them. Use the prospect's real public NAP, `tel:` links and LocalBusiness JSON-LD; real reviews only, with their source; `min-height` on the hero only (`100svh`). |
| C15 | Jakob's law vs distinctiveness | Conventional in **where things are and how they behave**; distinctive in **identity and composition**. |
| C16 | UUPM's deterministic niche → palette/font mapping | The niche table supplies constraints and required content only; style comes from C4. Two sites in one niche may not share display font, palette family, hero type or section order. |
| C17/C18 | Font advice contradicts other sources' ban lists | No fixed font list in SKILL.md. Use per-niche pools with a licence column and `last_used`, plus a dated overused list. The same display font can't appear in 2 of the last 5 Bexven sites, or in any of the last 5 in that niche. Always self-host. |
| C19 | Screenshot review vs metrics/text tree | Both, split by job. Scripts check numbers; screenshots are judged only for visual tells and specificity. |
| C20 | DESIGN.md before (Google, Open Design) vs after (Impeccable) | Before: a short direction contract plus tokens, because the Elementor build depends on them. After QA: sync DESIGN.md to what shipped. |
| C21–C28 | Caps/mono labels, atmosphere, weight contrast, colour quantity, #111 vs tell, zig-zag, section order, carousels | All resolved in `conflicts.md` with testable lint rules, e.g. flag stock `#111/#0f0f0f/#fafafa`, ≤2 card layouts per page, no auto-rotating carousels or marquees. |
| C29 | Reduced motion: kill everything vs gentler | Gentler: keep ≤150ms opacity and colour changes, remove movement. |
| C30 | Ask the client vs cold outreach | Mock stage: never ask, infer and log. Build stage: ask. |

### Outdated rules / tells that moved
- **Now tells**
  - cream + serif + terracotta
  - near-black + one acid-green or vermilion accent
  - broadsheet hairlines + zero radius + mono labels
  - the shadcn/SaaS card kit
  - template chrome (eyebrows, "A · B · C", "→" on buttons)
  - bento grids, marquees, shimmer buttons, aurora and spotlight backgrounds, gradient text
- **Fonts that became defaults:** Inter, Space Grotesk, Playfair, Fraunces, DM Sans, Plex, Poppins, Montserrat, Satoshi, Clash Display, General Sans, JetBrains Mono.
- **Stale sources:** UUPM's stock Tailwind palettes and glassmorphism; the 2025 Anthropic blog's own font suggestions; the Google Fonts sheet's "fresh" shortlist (Fraunces, Instrument Serif, Bricolage).
- **Principle:** don't rely only on a blacklist. Keep a **dated, versioned `tells.md`** plus two tests: "would a similar prompt land here too?" and "can the look be guessed from the category?"

## 4. Recommendation: one plugin with 4 focused skills

**Size estimate**
- Master sheet: ~218 merged rules plus ~150 single-source rules worth keeping ≈ 370 rules ≈ 450–550 lines ≈ 10–12k tokens.
- Add the workflows, the niche files, the tells list, the Elementor mapping and the QA rubric, and the whole skill body comes to ~1,600–2,000 lines ≈ 22–28k tokens.
- The spec says SKILL.md should stay under 500 lines / ~5k tokens, and that a skill's body stays in context once invoked (compaction re-attaches the first 5k tokens of each).
- **A single skill can't hold this lean.** Even with references, one universal SKILL.md would have to route between four very different jobs.

**Are the tasks separate enough?** Yes. They happen at different times and in different sessions:
1. **Direction**: brief → rut → shortlist → pick → DESIGN.md. Runs once per prospect.
2. **Build static**: DESIGN.md → HTML/CSS homepage on Vercel. Cold-outreach stage.
3. **Elementor build**: DESIGN.md + static page → WordPress/Elementor. Runs only after the client says yes, often weeks later.
4. **QA/critique**: runs after 2 and after 3, and on any existing site.

Brand guide isn't its own task: DESIGN.md *is* the brand guide, produced by Direction. A separate brand skill would duplicate it.

**What loads when**
| Always (every session) | On invoke | Only when needed |
|---|---|---|
| 4 descriptions ≈ 4 × 80–100 tokens | that one SKILL.md, ≤ ~200 lines / ~2.5k tokens | reference files (one niche file, typography, colour, motion, tells, Elementor mapping…) and scripts (run, not loaded) |

A typical cold-outreach session loads Direction + Build + QA ≈ 7.5k tokens of SKILL.md plus 3–5 references, versus ~25k if everything sat in one file.

**Discovery check**
- Claude Code does **not** document nested grouping folders inside `skills/` (`.claude/skills/group/skill/SKILL.md`), so I won't rely on them.
- It **does** load a **plugin** with several skills under `<plugin>/skills/<name>/SKILL.md`, namespaced `/plugin:skill`.
- So: **one plugin folder `bexven-web/` with 4 skills.** It gives us one versioned folder you can share through a private git marketplace, plus clean names (`/bexven-web:direction`).
- Fallback if you'd rather not use a plugin: the same 4 folders flat in `.claude/skills/` as `bexven-direction`, `bexven-build`, `bexven-elementor`, `bexven-qa`. Same files, no other changes.

## 5. Proposed folder tree

```
skill-research/
  master/master-sheet.md            # merged rules, sources tagged (Step 4.1)
  CREDITS.md                        # every source + licence
  bexven-web/                       # Claude Code plugin
    .claude-plugin/plugin.json
    README.md                       # install + workflow overview
    shared/                         # single source of truth (dev only)
      tells.md  craft-floor.md  niches/…
    scripts/sync_shared.py          # copies shared/ into each skill's references/ so each skill stays self-contained and portable
    skills/
      direction/
        SKILL.md
        references/  rut-and-directions.md · design-md-template.md · typography.md · colour.md · layout.md · copy.md · tells.md · niches/funeral-home.md · niches/metal-fabrication.md · niches/_template.md · font-pools.md
        scripts/     niche_log.py (history + seeded pick + collision check) · palette.py (OKLCH scale + WCAG check + hex fallback)
      build/
        SKILL.md
        references/  html-css-craft.md · components.md · motion.md · imagery-icons.md · seo-local.md · tells.md · vercel-deploy.md
        scripts/     tokens_to_css.py (DESIGN.md front matter → :root CSS)
      elementor/
        SKILL.md
        references/  elementor-mcp.md (build order, Variables/Classes mapping) · elementor-fallback.md (kit JSON, template import, custom fonts) · wp-hygiene.md (child theme, enqueue, perf, security) · tells.md
        scripts/     tokens_to_elementor_kit.py (DESIGN.md → kit JSON: global colours, fonts, sizes)
      qa/
        SKILL.md
        references/  critique-rubric.md · checks.md (a11y/perf/SEO numbers) · tells.md · devtools-mcp.md (optional, privacy flags)
        scripts/     screenshots.py (Playwright, 375/768/1024/1440, waits for fonts) · lint_html.py (tells, banned hexes, gradients, eyebrows, animation counts, contrast, NAP/JSON-LD, file:line output)
```

**SKILL.md vs references vs scripts**
- **SKILL.md** is the workflow steps, the 10–15 non-negotiable rules, a Gotchas section, and *when to load each reference*. No long lists.
- **references/** hold the detail, one level deep, each loaded for a named step (e.g. "Step 3: open `niches/<niche>.md`; if missing, copy `_template.md` and fill it").
- **scripts/** are Python 3 only (your stack). Playwright is already installed for you. No Node required, and nothing is downloaded at run time.

**Trigger descriptions (draft)**
- **direction**: "Plan the visual direction for a client website before any code: brief intake, niche research, 3–5 distinct directions, a seeded pick checked against past sites in the same niche, and a DESIGN.md brand/token file. Use when starting a new site, a cold-outreach redesign mockup, a rebrand, or when asked for a design direction, style guide or brand guide for a website."
- **build**: "Build a distinctive, non-generic static homepage or site in HTML/CSS from a DESIGN.md (Bexven house rules: typography, colour tokens, layout, copy, motion, local SEO, AI-tell avoidance) and deploy a preview to Vercel. Use when coding or redesigning a web page, landing page or cold-outreach mockup."
- **elementor**: "Convert an approved DESIGN.md and static page into a WordPress/Elementor build: Elementor MCP (Variables, Global Classes, Atomic containers, theme parts) or kit-JSON fallback, child theme, self-hosted fonts. Use when building or editing a WordPress or Elementor site."
- **qa**: "Review a built web page for AI-made tells, design specificity, accessibility, performance and local SEO using Playwright screenshots, a lint script and a scored critique; outputs file:line fixes. Use after building a page, before sending a mockup, or when asked to critique, audit or QA a website."

Before shipping, I'll run a trigger test: ~20 queries per skill (half near-misses), as the spec suggests.

## 6. What I'd drop, and why
- **Taste Skill's Node scripts and Stop-hook gate**: Node-only, very rigid (fixed section heights, hidden contacts, `.example` emails), and they conflict with local SEO. We keep its copy anti-slop ideas and the "deal from a curated list" idea, rewritten.
- **Impeccable's Rust binary, paid catalogue API and telemetry**: external downloads and data leaving the machine. We keep its methods (rut, worlds, rubric) in our own words.
- **UUPM's CSV data and deterministic mapping**: same niche gives the same look, the palettes are stock Tailwind, and it's glass-heavy. We keep only the idea of required content per niche.
- **Open Design's app (Electron/Next)**: too heavy. We keep its linter checklist (as Python) and its 80/20 rule.
- **Real-brand DESIGN.md files (awesome-design-md)** as templates: trade-dress risk and they defeat distinctiveness. We keep the structure only.
- **Component libraries (shadcn, Magic UI, Aceternity, React Bits)**: React-only, and their signature effects are now tells. We keep only shadcn's token-naming convention.
- **Playwright MCP as the default**: its own README recommends the CLI for coding agents. Our Python screenshot script is cheaper.
- **Vercel's live-fetched guidelines**: replaced by our paraphrased checklist (no network at run time). Their Title Case copy rule is dropped.
- **Lenis by default, smooth scroll, GSAP by default**: see C11/C12.
- **Huemint API** (non-commercial only) and **Realtime Colors randomise**: anti-deliberate.
- **theme-factory / brand-guidelines** (Anthropic): fixed preset themes, and its brand is itself tell #1.
- **Crawling the galleries**: their terms forbid it. Galleries become a human step: the designer drops 3 references into a "reference brief" the agent reads.
- **Shopify Liquid and other AIs**: out of scope now. The structure is portable (Agent Skills spec; `sync_shared.py` keeps skills self-contained) for later.

## 7. Risks and open questions
1. **Elementor MCP is new** (4.3.0, Sept 2026; extended in 4.4). Is Pro required, and is the V4 Atomic editor active on your sites? Some hosts disable Application Passwords. *I'll write both the MCP path and the kit-JSON fallback.* **Question:** which Elementor version and licence do your client sites run?
2. **Niche history log location.** It must persist across projects. *Recommendation:* one agency file, e.g. `~/bexven/niche-log.json` or a small private git repo. **Question:** where do you want it?
3. **Shared files across skills.** I'll copy shared references into each skill with `sync_shared.py` rather than relying on cross-skill paths (more robust, portable). The cost is that edits go in `shared/` and you re-run sync.
4. **Licences**
   - WordPress agent-skills is GPL: rules in our own words only.
   - Practical Typography and Laws of UX are all rights reserved: paraphrase only.
   - Fontshare files can't be redistributed: never commit them to public repos.
   - GSAP's terms forbid building a competing visual animation builder; ordinary site use is fine.
5. **Unverified items**: Land-book and Lapa Ninja (403), the exact Fontshare ITF FFL wording, Magic UI and React Bits effect lists, and whether Elementor global colours accept `oklch()` (we'll emit hex).
6. **Trigger collisions**: if Anthropic's frontend-design, Impeccable or Taste are installed alongside, they may fire instead of ours. Uninstall them or keep descriptions distinct, and delete `sources/` afterwards.
7. **Tells drift**: the tells list goes stale within months. `tells.md` carries a date and a "review quarterly" note.
8. **Scope of the first niche files**: I'll write `funeral-home.md` and `metal-fabrication.md` plus a template. **Question:** any other niches you want in v1?
9. **Plugin vs flat folders**: I recommend the plugin. **Question:** confirm, or ask for the flat fallback.

**Waiting for your go-ahead before Step 4** (master sheet → skills → CREDITS.md).
