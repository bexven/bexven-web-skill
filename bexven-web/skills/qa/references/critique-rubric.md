# Critique rubric

Load at **step 4** (visual critique) and **step 6** (report). The fresh-context reviewer in step 5 gets this file too.

Order is fixed: **specificity verdict → heuristic scores → tells → personas → issues (P0–P3) → report.** Judge looks first, before you read lint output in detail, so the tool does not anchor the judgement. {05,06}

Inputs you need open: the screenshots (all widths), `DESIGN.md` (direction contract, tokens, the named signature and motion moment), the brief or niche file if there is one, and `references/tells.md`.

---

## 1. Specificity verdict (always first)

Answer each question with **yes / no + one line of evidence** taken from the screenshots (name the section, element or class). No evidence, no answer.

| # | Test | Fails when |
|---|---|---|
| S1 | **Stranger test.** Cover the logo and business name. Could a stranger tell which business this is, in which town? | Only the logo and H1 text identify it; the rest would fit any client. |
| S2 | **Similar-prompt test.** Would the same prompt for another client in this niche land on this page too? | You can picture the competitor's version and it is the same page with a different name. |
| S3 | **Guessability test.** Could the look be guessed from the category alone (funeral = cream + serif; fabrication = charcoal + safety orange)? Or from the category plus our avoid-list? | The palette, type class or hero type is the category's stock answer. |
| S4 | **Memory test.** Close the screenshots. Name the one thing you remember. Is it the signature DESIGN.md names? | You remember nothing, or you remember a generic effect (gradient, card grid, big stat). |
| S5 | **Direction match.** Does the page carry the DESIGN.md scene sentence, type pair, colour strategy and named signature? | The build drifted to defaults; the signature is missing or diluted across five places. |

**Verdict:**
- **Specific** — S1–S5 all pass. Go on to heuristics.
- **Partly specific** — one or two fail. Name what is generic and the smallest change that fixes it (one section, one device). These become P1 issues.
- **Generic** — S2 or S3 fails *and* S1 fails. Stop scoring craft. The recommendation is **rebuild** from the direction (or back to `/bexven-web:direction` if the direction itself is the category default). Polishing a generic page is wasted work.

For an existing client site under audit, S5 becomes "does it carry the client's existing brand consistently?" and a Generic verdict is a sales finding ("the site looks like its competitors"), not a rebuild order.

---

## 2. Heuristic scores (0–4 each, total /40)

Score from evidence. Use the **worst sustained level**: if the hero is a 4 and three sections are a 2, the score is 2. Most real sites land 20–32; a 36+ needs no open P1. No grade inflation, no half points.

Scale: **0** broken or absent · **1** major problems · **2** works with clear friction · **3** good, minor issues · **4** nothing to fix.

| # | Heuristic | What a 4 looks like on a local-business site |
|---|---|---|
| H1 | **Task path** | The niche's main task (call, quote, find a service time, opening hours) is reachable in one tap from the first mobile viewport and in ≤2 clicks on desktop. |
| H2 | **Hierarchy** | One clear H1 naming service + place; one primary CTA per viewport; the eye lands in the intended order at 375 and 1440. |
| H3 | **Trust and proof** | Real NAP, real photos, real reviews with source and date, credentials the client holds, all near the CTA. Nothing invented. |
| H4 | **Clarity of copy** | Plain customer words, nouns in headings, buttons name the result, no slop vocabulary or AI cadences, no placeholder text. |
| H5 | **Consistency** | Same role = same style; one CTA wording site-wide; tokens used everywhere (no stray hexes, radii or fonts). |
| H6 | **Typography** | Readable body (≥16px; ≥18px for older audiences), measure 45–75ch, real scale steps, no orphans in headings, display face carries the direction. |
| H7 | **Colour and contrast** | Strategy from DESIGN.md held; accent rare and meaningful; contrast passes (numbers from step 3, not your eye). |
| H8 | **Layout and rhythm** | Section grammar varies with content; spacing has rhythm, not one gap everywhere; nothing cramped or empty-feeling at any width. |
| H9 | **Responsive integrity** | No overflow, overlap, clipped text or bad crops at 375/768/1024/1440; mobile is designed, not stacked desktop. |
| H10 | **States and feedback** | Visible focus, hover gated to fine pointers, press feedback, form errors/success designed, reduced-motion respected. |

**Bands:** 36–40 Excellent · 28–35 Good · 20–27 Acceptable · 12–19 Poor · 0–11 Critical.
A page ships at **Good or better with zero P0 and zero P1**. Specificity is not averaged in: a Generic verdict overrides any score.

---

## 3. Tells check

Open `references/tells.md` (dated list; check its version against the `tells_version` in DESIGN.md). For each screenshot, list every **active** tell you see with its section. A **watch** tell is fine only if DESIGN.md gives a written non-category reason for it. Cross-check against the lint output from step 1: lint catches code-level tells (hexes, class names, keyframes, eyebrows); you catch composition tells lint cannot see (identical card rows, stock-photo hero, big-stat strip, hero → features → testimonials → FAQ → CTA skeleton, cards in cards, the broadsheet kit on a non-editorial client).

Every active tell is at least **P1**. An explicit brief or existing client brand that asks for it wins; note that and move on.

---

## 4. Persona checks

Walk the page as 2–3 visitors who actually use this business. Use the niche file's audience if it exists; otherwise write two personas in one line each before you start. For each, answer: *Can they do their task? What stops them? Where do they hesitate?* Red flags go into the issue list.

| Persona | Device and state | Checks |
|---|---|---|
| **Grieving family member** (funeral home) | Phone at 375, at night, distressed, maybe older | 24/7 phone visible without scrolling and tappable; "someone has just died, what now" path findable; service times in ≤2 taps; body ≥18px; no motion, popups, chat bubbles or sales tone. |
| **Pre-planner** (funeral home) | Tablet or desktop, calm, weeks ahead | Pricing or "how costs work" reachable; staff named; plan-ahead form short and reassuring. |
| **Procurement manager / engineer** (fabrication) | Desktop 1440 at work, comparing 3 shops | Capabilities, materials, thickness and size limits in real tables; certifications; portfolio with material and scope; quote form takes drawings (PDF/DWG/DXF/STEP) within 2 clicks. |
| **Site foreman** (fabrication, trades) | Phone outdoors, glare, one hand | Phone number and quote CTA in thumb reach; contrast holds in sunlight (aim higher than 4.5:1); no tiny tap targets. |
| **Homeowner** (any trade) | Phone, evening, first visit | Understands what the business does and where within 5 seconds; sees real work and reviews; can call or send a short form. |
| **Keyboard / screen-reader user** | Desktop, no mouse | Skip link, visible focus, logical order, labelled fields, menu traps and returns focus. |
| **Distracted mobile visitor** | Phone, interrupted mid-form | Form keeps input; errors say how to fix; success says what happens next and when. |

Pick the two most relevant to the niche plus the keyboard user. Landing pages without a niche file: homeowner, distracted mobile, keyboard.

---

## 5. Severity (P0–P3)

| Level | Meaning | Examples |
|---|---|---|
| **P0 — blocking** | Broken, inaccessible or illegal. Never ship. | Contrast below WCAG AA on body or CTA; form that cannot send or fakes success; invented reviews, prices, hours, years or certifications; missing or wrong phone/NAP; horizontal scroll at 375; content hidden when JS fails; console errors that break a feature; zoom disabled. |
| **P1 — major** | AI tell, off-direction, or a real task obstacle. Fix before ship. | Any active tell; specificity test fails; signature missing; CTA below the mobile fold; primary task >2 clicks; generic stock hero; touch targets <44px on key actions; missing LocalBusiness JSON-LD on a local page. |
| **P2 — minor** | Craft issue a careful visitor notices. | Orphan in a heading; uneven card heights; spacing rhythm breaks; one off-token colour; weak hover state; image crop through a face; long title truncation. |
| **P3 — polish** | Nice to fix if time allows. | `::selection` colour; underline offset; tabular figures in hours; optical alignment. |

**Tie-break:** "Would this make a visitor phone the business confused, give up, or distrust it?" If yes, it is at least P1. When unsure between two levels, take the higher one for P0/P1 and the lower one for P2/P3.

Each issue: **ID, severity, where (section + width, or `file:line`), evidence, fix (one concrete change), check (how you will verify it).**

---

## 6. Report template

Write the report in this order. Keep it to one screen per section; link to files rather than pasting dumps.

```
# QA report — <page or URL> — <date>
Scope: <pages, widths, browsers> · Build: <static | Elementor staging | existing site> · tells v<version>
Reviewer: <in-context | fresh-context subagent> · Round <n of 3>

## Verdict: SHIP | FIX | REBUILD
<one sentence why>

## Specificity: Specific | Partly specific | Generic
S1 stranger … S2 similar-prompt … S3 guessability … S4 memory … S5 direction  (yes/no + evidence each)

## Scores: <total>/40 (<band>)
H1 … H10 one line each: score — evidence

## Evidence (numbers)
| Check | Conditions | Result | Source |
| lint | lint_html.py [--local] | 0 error / 3 warn | qa/lint.json |
| contrast | … | … | script |
| overflow 375 | … | none | screenshots.py |
| console / failed requests | … | 0 / 0 | screenshots.py |
| LCP / CLS / INP | lab, mobile, 4x CPU, Slow 4G, median of 3 | … | DevTools MCP / Lighthouse CLI / skipped |

## Issues
| ID | Sev | Where | Evidence | Fix | Verify |
| Q1 | P0 | … | … | … | … |

## What works (2–3 items, specific)

## Persona red flags

## Waived findings (rule id, reason)

## Known gaps and assumptions
Stock images used · placeholders still present · lab-only metrics (field pending) · checks skipped and why
```

Verdict rules:
- **SHIP** — Specific, ≥28/40, zero P0, zero P1, lint clean (or every remaining finding waived with a reason).
- **FIX** — Specific or Partly specific, issues are fixable in place. List them in fix order: P0 → P1 → P2.
- **REBUILD** — Generic verdict, or the direction is not carried and fixing would mean replacing most sections. Say which step to go back to.
