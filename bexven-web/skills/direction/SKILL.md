---
name: direction
description: "Plan the visual direction for a client website before any code is written: brief intake (infer from the prospect's site, Google profile and photos at mock stage), the niche's category rut, 3-5 distinct directions from the client's world, a seeded pick checked against past Bexven sites in the same niche, then a DESIGN.md with the direction contract and design tokens. Use this whenever starting a new site, a cold-outreach redesign mockup, a rebrand or relaunch, or when asked for a design direction, style guide, brand guide, moodboard, colour palette or font pairing for a website, even if the user only says 'make it look good' or 'start the funeral home mock'. Also covers small jobs (one section or component) with a 5-line mini direction."
license: Proprietary (Bexven)
---

# Direction

Decide what a client site should look and sound like, and write it down as a DESIGN.md that the build and Elementor skills follow. AI-made sites converge on the most probable page for a niche; this skill stops that by naming the niche's rut, deriving several real alternatives from the client's own world, removing ones that repeat recent Bexven work, and picking with a logged seed. Output: one `DESIGN.md` in the project root (direction contract + token front matter) and, after ship, one line in the niche log.

## Small job path (one section, one component, a form, a tweak)

Do not run the full process. If the project has a DESIGN.md or a `:root` token block, reuse it and go straight to `/bexven-web:build`. If not, write a 5-line mini direction at the top of your reply (or in a short DESIGN.md):
1. Scene sentence (who uses it, where, on what device; light or dark follows).
2. Type pair (from `references/font-pools.md`, licence noted) and the one emphasis device.
3. Colour strategy (Restrained / Committed / Drenched), ink, paper, one action accent.
4. One emphasis or signature device (or "none").
5. Radius language (e.g. "2px everywhere, pill buttons").
Then build. Still respect `references/tells.md`.

## Workflow (full direction)

1. **Intake.** Identify the stage.
   - *Mock stage* (cold outreach, no client contact): never ask the prospect anything. Read their current site, Google Business Profile, photos, signage, vehicles, reviews. Collect: real name, NAP, services, service area, hours, logo and existing colours, usable photos, real reviews with source and date, credentials, 3-5 competitors in the same town. Every inference goes into an Assumptions list (`assumed: … because …`).
   - *Build stage* (client said yes): the Assumptions list becomes the client question list. Ask about the business only, never about aesthetics or CSS values.
   - If the designer supplied a *reference brief* (up to 3 human-picked gallery references), read it and note what each reference contributes (one trait each, never "copy this"). Never crawl galleries yourself.
   - Open `references/niches/<niche>.md`. If missing, copy `references/niches/_template.md`, fill it from competitor research, mark it first-pass; save it to the plugin's `shared/niches/<slug>.md` (then run `scripts/sync_shared.py`) so later projects get it, or into the project if the plugin is read-only.
   - Write in 3-5 lines: the client's unique mechanism, the audience scene, and the customers' own words for the services.
2. **Category rut.** Write one paragraph: "the page this niche always ships" (hero, palette, fonts, section order, stock photo, CTA wording). Use the niche file's rut plus what the competitors share. Ban it and its obvious opposite as defaults. Method: `references/rut-and-directions.md`.
3. **Directions.** Write 3-5 directions from the client's world (objects, places, print, rituals, era), spread over at least 3 material families, at most one from the literal trade metaphor. Each one: a name, one governing-idea sentence opening with a concrete reference, 5-7 characteristics, and its value on the axes type voice, colour strategy, layout grammar, imagery treatment, signature moment (plus hero type and section order). Every pair must differ on at least 2 axes; never only by accent colour. Run the similar-prompt and guessability tests (`references/tells.md`) on each.
4. **Check and pick.** For each direction run `niche_log.py check`. Drop any that exit 1 (or change the colliding choice and re-check). Also compare the signature moment by eye with `niche_log.py list --niche <niche>` (the script does not check it). Pick among survivors with `niche_log.py pick … --seed <seed>`, seed = hash of client domain + date (command below). Write one sentence on why the pick fits this client. Show the shortlist, the dropped ones (with reason), the seed and the pick.
5. **Scene sentence.** One sentence: scene of use, audience, existing brand. Light or dark follows from it; category only breaks a tie. Example: "a family on a phone at night, often older relatives; the sign is dark green on white" → light, high contrast.
6. **Palette and fonts.** Colour per `references/colour.md`: lock the existing brand colour if there is one, build scales with `palette.py scale`, derive ink and paper, name the accent's allowed places, check pairs with `palette.py check`. Fonts per `references/typography.md` from `references/font-pools.md`: record licence and source, respect the reuse limits (enforced by step 4's check).
7. **Write DESIGN.md** from `references/design-md-template.md`: front matter tokens + Overview (governing idea + scene sentence) through Known gaps, including Assumptions and `tells_version: 2026-11`. Layout per `references/layout.md`, voice per `references/copy.md`. Verify it parses: `python3 ${CLAUDE_SKILL_DIR}/../build/scripts/tokens_to_css.py DESIGN.md` must exit 0.
8. **Log and hand off.** After the client approves the direction, or when the mock ships, run `niche_log.py add` with the final values (and `--seed`). After QA, sync DESIGN.md to what shipped. Hand off to `/bexven-web:build`.

## Non-negotiable rules

1. No code before DESIGN.md exists (full path) or the mini direction is written (small job path).
2. Mock stage never asks the prospect; every guess is logged under Assumptions. Build stage asks only about the business.
3. Never invent facts: unknown hours, prices, years, counts, credentials and reviews stay unknown and go under Known gaps.
4. Directions come from the client's world, never from trends or "what this niche looks like". Open each with a concrete object, place or era, not adjectives.
5. Every pair of directions differs on ≥2 named axes. Accent colour alone is never a difference.
6. A direction that collides with the niche log (`check` exit 1) is dropped or changed. The pick is seeded and the seed is recorded in DESIGN.md and the log.
7. Niche files give constraints and content only. Never take a palette, font, hero or section order from a niche file or a category association.
8. Light or dark is decided by the scene sentence, written in DESIGN.md. Dark is not the default for local service sites.
9. One action accent with a written allowed-places list (primary CTA, links, focus), max 2 uses per viewport. Brand fields are not accents.
10. Ink and paper derive from the palette (ink OKLCH L 0.18-0.26 tinted to the brand hue); never #000, #111, #0f0f0f, #fafafa, #fff as stock values.
11. Fonts come from `font-pools.md` with a recorded licence, self-hosted. Overused-list fonts need a written non-category reason. Same display font never in any of the last 5 sites in the niche or 2 of the last 5 overall.
12. One emphasis device (weight, size, case or face) and one signature (motion or hover idea, or "none"), both named.
13. Saturated violet (and purple→blue/pink gradients) only when it is the existing brand or the brief asks; record `brand-source:`.
14. Accessibility lives in token numbers (contrast pairs pass in `palette.py check`), not in "remember accessibility" sentences.
15. An explicit client brief or existing brand beats every anti-tell rule; tells govern only what the brief leaves open.

## When to load which reference

| Step | File | Why |
|---|---|---|
| 1 | `references/niches/<niche>.md` (or `_template.md`) | audience, must-have content, trust signals, no-gos, the niche rut |
| 2-3 | `references/rut-and-directions.md` | rut method, axes, strong vs weak direction examples |
| 3, 7 | `references/tells.md` | dated tells v2026-11 and the two tests |
| 3, 7 | `references/layout.md` | hero types, section grammar, neighbour and card limits |
| 5-6 | `references/colour.md` | OKLCH method, roles, strategy, accent places, light/dark |
| 6 | `references/typography.md` + `references/font-pools.md` | pairing method, scale, licences, pools, overused list |
| 7 | `references/design-md-template.md` | DESIGN.md skeleton that parses with `tokens_to_css.py` |
| 7 | `references/copy.md` | voice section, labels, anti-slop words and cadences |

## Scripts

Niche log default path `~/.bexven/niche-log.json`; override with `BEXVEN_NICHE_LOG` or `--log PATH` (placed before the subcommand).

```bash
# seed = hash of client domain + date
python3 -c "import hashlib;print(int(hashlib.sha256(b'example-funeral.com|2026-11-18').hexdigest(),16)%100000)"
python3 ${CLAUDE_SKILL_DIR}/scripts/niche_log.py list --niche funeral-home
python3 ${CLAUDE_SKILL_DIR}/scripts/niche_log.py check --niche funeral-home --display-font "Spectral" \
  --body-font "Public Sans" --palette-family "slate blue + linen" --accent-hue 245 \
  --hero-type type-led --section-order hero,first-steps,notices,services,people,place,contact
python3 ${CLAUDE_SKILL_DIR}/scripts/niche_log.py pick "Parish register" "Garden wall" "Linen and slate" --seed 48213
python3 ${CLAUDE_SKILL_DIR}/scripts/niche_log.py add --client "…" --niche funeral-home --direction "…" \
  --display-font "…" --body-font "…" --palette-family "…" --accent-hue 245 --theme light \
  --hero-type type-led --section-order hero,… --signature-moment "…" --url https://… --seed 48213
python3 ${CLAUDE_SKILL_DIR}/scripts/palette.py scale --hue 245 --chroma 0.06 --name slate
python3 ${CLAUDE_SKILL_DIR}/scripts/palette.py contrast "#1f2a24" "oklch(0.97 0.01 90)"
python3 ${CLAUDE_SKILL_DIR}/../build/scripts/tokens_to_css.py DESIGN.md -o /tmp/tokens.css
python3 ${CLAUDE_SKILL_DIR}/scripts/palette.py check /tmp/tokens.css --pair color-ink:color-paper --pair color-on-accent:color-accent
```

`check` exits 1 on any collision and prints which site it collides with. `palette.py` exits 1 on failing pairs and warns on saturated violet (`--allow-violet` only with a brand source). `palette.py check` reads custom properties from a CSS file's `:root`, so run `tokens_to_css.py -o` first and pass the generated names without the leading `--` (e.g. `color-ink`).

## Gotchas

- `niche_log.py check` compares names after lower-casing and collapsing spaces: write palette families and hero types the same way every time (`deep green + brass`, `photo-split`). Use the hero-type slugs from `references/layout.md`.
- The script does not check the signature moment or icon family; compare those by hand against `list`.
- An empty log means every direction passes; that is fine for the first site in a niche, not proof of distinctiveness. The similar-prompt test still applies.
- The first palette that comes to mind for a warm subject is already spent (cream + serif + terracotta). Change at least two of ground, face class and accent if warm is genuinely right.
- Directions that differ only in mood words ("calm", "warm", "trustworthy") are one direction. Rewrite with objects and axes.
- Writing "Playfair + Inter" or "slate + safety orange" means the rut won. Go back to step 2.
- Do not put token values only in prose; the build reads the YAML front matter. Put tokens in front matter, prose explains use.
- `tokens_to_css.py` lives in the build skill (`${CLAUDE_SKILL_DIR}/../build/scripts/`). If that path is missing (skill installed alone), validate the YAML by eye against `design-md-template.md` and let the build skill run the converter.
- Keep `tokens_to_css.py` happy: one front matter block at line 1, hex values quoted, references as `"{colors.ink}"`.

## Hand-off

When DESIGN.md parses and the pick is recorded, hand off to `/bexven-web:build` (static mock). After the client says yes, `/bexven-web:elementor` reads the same DESIGN.md. QA: `/bexven-web:qa`.
