---
name: qa
description: "Review and fix a built web page before anyone sees it: Bexven's QA pass for AI-made tells, design specificity (could a stranger tell which business this is?), accessibility (WCAG 2.2 AA), performance, forms and local SEO. Runs a lint script with file:line findings, Playwright screenshots at 375/768/1024/1440 plus a reduced-motion pass, number checks, a scored critique with P0-P3 issues, up to 3 fix rounds and a fresh-context ship/fix/rebuild verdict. Use after building a page or section, before sending a cold-outreach mockup, before launching a WordPress/Elementor build, and whenever asked to critique, audit, review, QA, check or 'look over' a website, landing page, staging URL or an existing client site, even if they only say 'does this look generic?'"
license: Proprietary (Bexven)
---

# Bexven QA

Find what is broken, generic or inaccessible on a built page, fix it, and say honestly whether it ships. Numbers come from scripts (lint, overflow, console, contrast, traces); looks come from screenshots you actually open. Specificity is judged first, because a polished generic page is still a fail for an agency that sells distinctiveness. Works on our static Vercel mocks, Elementor staging URLs and any existing client site (audit-only: report, don't edit, unless asked).

## Scale to the job

- **Small job** (one component, one section, "check this form"): lint the file, screenshot 375 + 1440, run the checks for that component from `references/checks.md`, scan `references/tells.md`, list issues P0–P3, fix, re-shoot once. No scores, personas or subagent.
- **Full page or site**: the whole workflow below.
- **Audit of someone else's site** (prospect, existing client): steps 1–4 and 6, no fix loop; the report is the deliverable.

## Workflow

Make a `qa/` folder next to the page (or in the scratch dir for a remote URL). Keep every artefact there: `qa/lint.json`, `qa/shots/`, `qa/report.md`.

**1. Lint (file:line findings).**
`python3 ${CLAUDE_SKILL_DIR}/scripts/lint_html.py <page.html> [--local] --json > qa/lint.json`
Add `--local` for any local-business page (requires a `tel:` link and parsing LocalBusiness JSON-LD). Run without `--json` for the human-readable `file:line: [P1] [rule-id] message` list. Exit 1 = at least one P0/P1. For a URL, save the rendered HTML first (see Gotchas). Read the rule table below; don't fix yet.

**2. Screenshots, then look at every one.**
`python3 ${CLAUDE_SKILL_DIR}/scripts/screenshots.py <url-or-file> --out qa/shots --json`
`python3 ${CLAUDE_SKILL_DIR}/scripts/screenshots.py <url-or-file> --out qa/shots --name <page>-rm --reduced-motion --json`
Default widths 375,768,1024,1440 (add `--widths 320,375,768,1024,1440,1920` for photo-led heroes or reflow checks; `--dark` only if the site supports dark). The script waits for network idle and `document.fonts.ready`, scrolls to trigger lazy images, and reports horizontal overflow (with the widest offenders) and console/page errors; exit 1 if any. **Open every PNG with Read**, 375 first. Never critique from code or from memory of what you built.

**3. Number checks.** Load `references/checks.md`. The lint does **not** compute contrast or touch-target sizes: run snippet A (contrast) and B (targets) from that file, or compute ratios from DESIGN.md token pairs yourself. Record overflow and console results from step 2. If Chrome DevTools MCP tools are already connected, load `references/devtools-mcp.md` for LCP/CLS/INP traces, Lighthouse a11y/SEO and CSS-cascade questions; otherwise mark those "not measured" and say why.

**4. Visual critique.** Load `references/critique-rubric.md` and `references/tells.md`. In this order:
1. **Specificity verdict**: could a stranger tell which business this is with the logo covered? Would a similar prompt for another client in the niche land here too? Can the look be guessed from the category? What do you remember? Does it carry DESIGN.md's signature? Yes/no + evidence each. A Generic verdict stops craft scoring: recommend rebuild.
2. **Heuristics H1–H10**, 0–4 each, worst sustained level, total /40 with band.
3. **Tells**: every active tell from `tells.md` you can see, with section and width; cross-check lint.
4. **Personas**: two niche visitors (e.g. grieving family on a phone at night; procurement manager comparing shops on desktop) plus a keyboard user.
5. **Issues** P0–P3, each with where, evidence, one concrete fix, and how to verify.

**5. Fix loop, then fresh eyes.** Fix in order P0 → P1 → P2 (P3 if cheap). Re-run lint and re-shoot only what changed; look again. **Max 3 rounds.** Then run a **fresh-context final review**: spawn a subagent (Task/Agent tool) that never saw the build conversation and gets only the screenshot paths, `DESIGN.md` (and the brief/niche file if any), `references/critique-rubric.md` and `references/tells.md`, with this prompt:
> You are reviewing a local-business web page you did not build. Open every screenshot. Using the rubric, give the specificity verdict, H1–H10 scores, active tells and P0–P3 issues with evidence (section + width). End with exactly one word: SHIP, FIX or REBUILD.

If subagents are unavailable, do the review yourself but start the report with "Reviewer: in-context (not independent)". Anything still open after round 3 goes to a human with the list; don't start round 4.

**6. Report.** Write `qa/report.md` with the template in `critique-rubric.md` §6: verdict, specificity, scores, evidence table (lab numbers labelled lab), issues table, what works, persona red flags, waived findings with reasons, known gaps (stock images, placeholders, skipped checks). Give the user the verdict, the P0/P1 count and the report path.

## Non-negotiable rules

1. Specificity verdict before any score; a Generic page is never "fixed" by polish.
2. Numbers by script, looks by screenshot. Never estimate contrast, tap size, overlap or speed from an image.
3. Open every screenshot you take. A screenshot you didn't look at is not QA.
4. WCAG 2.2 AA is a hard gate: 4.5:1 body, 3:1 large text (≥24px or ≥18.66px bold) and UI/focus, targets ≥44px (primary mobile CTA and phone ≥48px), visible focus, zoom never disabled.
5. Invented facts (reviews, years, prices, certifications, hours) are P0, even when they look good. Placeholders must be labelled and listed under Known gaps.
6. Zero console errors and zero failed requests before handoff; no horizontal scroll at 375.
7. Every active tell is at least P1 unless the brief or the client's existing brand asks for it (say so).
8. Max 3 fix rounds, then fresh-context review, then a human. No endless polishing.
9. Waive a finding only with a written reason (`<!-- lint-ignore rule-id -->` plus a line in the report). Never rewrite markup just to dodge the checker.
10. Lab numbers are labelled lab; never claim speed or ranking gains without before/after on the same URL and conditions.
11. Outreach previews and staging must be `noindex`; live client sites must not be. Check which one you are looking at.
12. Never install tools (DevTools MCP, Lighthouse, axe) or change the user's MCP config; use what is there and report what was skipped.
13. Audits of client or prospect sites are read-only unless the user asks for fixes; never log into a client admin with a browser tool unless asked.
14. A fix must respect DESIGN.md. If the fix needs a design change (new colour, new face), flag it rather than improvising tokens.

## When to load which reference

| Step | File | Why |
|---|---|---|
| 3 | `references/checks.md` | Every number (a11y, CWV, budgets, SEO, local, forms) with how to verify it; contrast and target snippets |
| 3 (only if DevTools MCP tools exist) | `references/devtools-mcp.md` | Traces, Lighthouse, CSS cascade; privacy flags |
| 4, 5 | `references/critique-rubric.md` | Specificity tests, H1–H10, personas, P0–P3, report template |
| 4, 5 | `references/tells.md` | Dated active/watch tells list (check its version against DESIGN.md `tells_version`) |
| 4 (if it exists) | `references/niches/<niche>.md` | Audience, must-have content and task paths for personas |

## Lint rule ids (`lint_html.py`)

Lint priority is the script's own; in the report, re-grade with the rubric (an active tell you confirm on screen is P1 even if lint says P2/P3).

| Pri | Rules |
|---|---|
| P1 | `banned-hex` (Tailwind indigo/violet/purple), `outline-none` (with no `:focus-visible` anywhere), `img-alt`, `img-size`, `input-label`, `zoom-disabled`, `html-lang`, `title`, `viewport`, `google-fonts-cdn`, `local-tel`*, `local-jsonld`*, `jsonld-invalid`* |
| P2 | `violet-hue`, `purple-gradient`, `section-gradient`, `stock-black`, `transition-all`, `keyframes-layout`, `input-label-aria`, `generic-cta`, `eyebrow` (>2), `entrance-animation` (>2 sections), `raw-hex` (>12 outside `:root`), `meta-description`, `heading-order`, `h1-count`, `banned-copy` |
| P3 | `middot`, `arrow-button`, `emoji-icon`, `overused-font`, `backdrop-filter`, `library-effect`, `stylesheet-missing` (needs a DESIGN.md reason or a fix) |

\* only with `--local`. Options: `--json`, `--min P1` (filter). Suppress: `<!-- lint-ignore rule-id -->` or `/* lint-ignore rule-id */` on the same or previous line. Exit 0 clean of P0/P1, 1 has P0/P1, 2 usage error.

## Gotchas

- **Lint reads a local file only.** For a URL (Vercel preview, Elementor staging, client site) save the HTML first: `curl -sL <url> -o qa/page.html`, or for JS-rendered pages save `page.content()` from Playwright. Remote stylesheets are never fetched, so CSS rules (hover, transitions, hexes) are weaker on URLs; check those in DevTools or by downloading the CSS next to the HTML with the same relative path.
- Elementor output trips `raw-hex`, `transition-all` and `h1-count` from theme/plugin CSS you don't own; separate "ours" from "theme" in the report and fix ours via Global Classes/Variables.
- `screenshots.py` names files `<name>-<width>.png`; without a different `--name` the reduced-motion pass overwrites the normal shots.
- It needs Playwright for Python with Chromium. If missing (exit 2 with an install hint), tell the user the install command; don't install without asking.
- Overflow is reported but not located visually; open the 375 PNG and the listed offenders together.
- Console errors from third-party embeds (maps, chat) still count; facade them or note them as client-owned.
- Screenshots of `file://` pages can miss fonts loaded from absolute paths; serve the folder (`python3 -m http.server`) if text renders in a fallback face.
- WebKit (iPhone Safari) is not in the script; run one manual WebKit pass before an outreach link goes out (snippet note in `checks.md` §8).
- Lint's `h1-count` flags several h1s; that alone is not an SEO fail. A missing descriptive h1 is.
- Don't read whole Lighthouse JSON or traces into context; filter for failures.

## Hand-off

SHIP on a static mock → deploy/send (back to `/bexven-web:build` for the Vercel step). FIX → `/bexven-web:build` or `/bexven-web:elementor` with the issues table. REBUILD or Generic → `/bexven-web:direction`. After an Elementor build passes, keep `qa/shots/` as the reference for future changes.
