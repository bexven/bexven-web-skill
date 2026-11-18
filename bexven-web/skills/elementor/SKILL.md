---
name: elementor
description: "Convert an approved DESIGN.md and static HTML/CSS page into a WordPress/Elementor build that looks identical: preflight checks, Elementor MCP (Variables, Global Classes, header/footer theme parts, Atomic flex/grid containers, forms, popups) or a kit-JSON/template fallback when MCP is missing, child theme, self-hosted fonts, everything kept as drafts. Use whenever the task is building, rebuilding, migrating or editing a WordPress or Elementor site, page, header, footer, form or global kit, setting up Elementor global colours/fonts from design tokens, or turning a Vercel mockup into Elementor, even when the user only says 'put this on WordPress' or 'do it in Elementor'. Also use for a single Elementor section or form fix."
license: Proprietary (Bexven)
---

# Elementor build

Purpose: carry an approved design (DESIGN.md tokens + the static page we showed the client) into WordPress/Elementor without losing anything that made it distinctive. The design is already decided; this skill executes it. Elementor's defaults (kit fonts and colours, entrance animations, Angie's one-prompt design system, generic widget styling) are the main risk: each one pulls the site back toward every other Elementor site. Everything is built as a draft, on staging, with a dedicated credential, and nothing is published without an explicit request.

## Small job path

One section, one form, one header fix, a colour change: do not run the full workflow.
1. Confirm which site and page, and that it is staging or that the user has confirmed production (rule 2).
2. Read the project's DESIGN.md (or the site's existing Global Colours/Fonts/Variables). Reuse them. If neither exists, write a 5-line mini direction into the chat (scene sentence, type pair, colour strategy, one emphasis device, radius language) and use it.
3. Build in a draft using existing Global Classes/Variables only; add a class only if the pattern repeats.
4. Run the relevant part of step 8 (screenshots at 375/1280 + lint on the changed page). Report what changed and where.

## Workflow (full build)

0. **Preflight.** Decide the route before building anything. Check, and write the results into the chat as a short table:
   - Is an Elementor MCP server connected in this session (tools exposed by the site's built-in Elementor MCP)? If yes, call its System Info / licence tool (4.4+) for versions.
   - Elementor (Core and Pro) ≥ 4.3.0; WordPress ≥ 6.8; Pro licence yes/no; Editor V4 (Atomic) on or off.
   - Application Passwords work (an authenticated `GET /wp-json/wp/v2/users/me` returns the build user, not 401). Security plugins and some hosts disable them.
   - Staging URL vs production URL; a backup or restore point exists.
   **Route:** all checks pass → MCP route (`references/elementor-mcp.md`). Any check fails → fallback route (`references/elementor-fallback.md`). Do not upgrade plugins, enable MCP or create credentials yourself: list the human steps from `elementor-mcp.md` §1 and wait.
1. **Tokens → globals.** Run `tokens_to_elementor_kit.py` on DESIGN.md. MCP route: create Variables (colour, font, size) from `variables`, and set Global Colours/Fonts from `settings` so V3 widgets and the client's future edits use the same palette. Fallback: import or enter `settings` by hand. Hex only. Replace the default kit entirely; turn off Elementor's default colours and fonts.
2. **Global Classes.** One class per repeated pattern in the static CSS (buttons, cards, section shells, eyebrow-free headings, form fields), named like the static class, values bound to Variables. States (hover, focus, active) and breakpoints live on the class.
3. **Theme parts.** Header and footer as theme parts with display conditions (entire site, minus exceptions). Popups only if the task needs them. Pro needed for Theme Builder; without Pro see `elementor-fallback.md` §6.
4. **Pages.** Atomic flex/grid containers mirroring the static DOM section by section, using the classes from step 2. Map static CSS 1:1. No per-element inline styling; if a value is not in a Variable or Class, it is either a missing token (add it to DESIGN.md and the kit) or a mistake. Repeated blocks (service card, review, CTA band) become Components. The LCP hero image is an Image element, not a container background.
5. **Forms and popups.** Elementor Pro Form, or the site's existing form plugin, following the build skill's form rules (checklist in `references/elementor-mcp.md` §7). Test real email delivery.
6. **Global settings.** Entrance animations off everywhere (only the one motion moment named in DESIGN.md, added in custom CSS/JS); fonts self-hosted (Load Google Fonts Locally, or WOFF2 uploaded as Custom Fonts); lazy load on below-fold images; performance features on. See `references/wp-hygiene.md`.
7. **Drafts only.** Pages, templates and theme parts stay draft/unpublished. Publishing, activating a header/footer on a live site, or changing the front page needs the user's explicit request in this session.
8. **QA.** Hand the staging/preview URL to `/bexven-web:qa`: screenshots at 375/768/1280 compared with the saved Vercel screenshots, lint (including `_animation` in `data-settings`), contrast, Lighthouse. Fix, re-check, max 3 rounds.
9. **Sync.** Update DESIGN.md to what shipped: new tokens, renamed classes, Elementor-specific notes (class names, template IDs, known gaps). The built site wins on drift; record why.

## Non-negotiable rules

1. **Drafts only.** Never publish, never switch a live header/footer, never change Reading settings without an explicit request in this session.
2. **Production is unsafe by default.** Work on staging. Touch production only after the user confirms the URL is production and agrees, and only after a backup (host snapshot or `wp db export`) plus an Elementor revision exists.
3. **The AI acts with the WP user's permissions.** Use a dedicated build user and a dedicated Application Password labelled for this job; tell the user to revoke it and turn Elementor MCP off at handover. Never paste a password into chat, files or commits.
4. **Never accept builder defaults.** Elementor's default kit, Angie-generated design systems, Hello theme type scale and default button styles are replaced by DESIGN.md values. Do not ask Angie to design anything.
5. **Hex only** for Global Colours and colour Variables (the script converts OKLCH). Verify each against DESIGN.md.
6. **Tokens and classes, not inline values.** Every colour, font, size, radius and gap comes from a Variable; every repeated look from a Global Class. Keep classes lean (hard limit 1000; aim well under 100 for a brochure site).
7. **Atomic containers first.** Legacy V3 widgets only where no Atomic element exists (e.g. mega menu before 4.5, some Pro widgets). Never section/column layout.
8. **Entrance animations off.** No `_animation` on any element. At most one motion moment per page, the same one the static mock had, honouring reduced motion.
9. **Fonts self-hosted.** No requests to fonts.googleapis.com, fonts.gstatic.com or api.fontshare.com. WOFF2 only, licence file kept with the project.
10. **Never hand-edit `_elementor_data`** in the database or via raw meta writes. Bad call? Use the revisions-based undo (4.4+) or restore a revision.
11. **One writer per page.** Do not build a page while someone has it open in the editor; Elementor flags conflicts, but resolve by re-reading the page, never by overwriting.
12. **No installs without OK.** No plugin installs, updates, theme switches or MCP enablement on a client site without the user's explicit approval.
13. **Same moment, same content.** The WP build carries the static page's copy, structure and motion moment; stock images are swapped for client photos where supplied, and the swap is listed.

## When to load which reference

| Step | Load | Why |
|---|---|---|
| 0 (MCP present or planned) | `references/elementor-mcp.md` | Human setup steps, per-version tool list, build order, mapping table, states/breakpoints, drafts, limits |
| 0 (any check fails) | `references/elementor-fallback.md` | Kit import, custom fonts, hand build or template JSON import, custom CSS location, exporting the target site's kit to confirm schema |
| 3, 6, and any PHP/JS/plugin work | `references/wp-hygiene.md` | Child theme, enqueueing (incl. GSAP), fonts, images, caching, security, WP-CLI, Playground, widget accessibility, GPL |
| 4 and 8 | `references/tells.md` | Builder-default and AI-made tells to avoid while building and to check before hand-off |

## Script

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/tokens_to_elementor_kit.py DESIGN.md -o kit-fragment.json   # full object
python3 ${CLAUDE_SKILL_DIR}/scripts/tokens_to_elementor_kit.py DESIGN.md --variables-only     # V4 Variables list
python3 ${CLAUDE_SKILL_DIR}/scripts/tokens_to_elementor_kit.py DESIGN.md --settings-only -o site-settings.fragment.json
python3 ${CLAUDE_SKILL_DIR}/scripts/tokens_to_elementor_kit.py DESIGN.md --strict             # fail on any warning
```
Output: `settings` (system/custom colours and typography, kit-style), `variables` (`color-*`, `font-*`, `text-*`, `radius-*`, `space-*`), `fonts_to_self_host`. Warnings go to stderr; exit 1 = unresolved `{ref}` (or any warning with `--strict`), 2 = bad input. Read every warning. The kit schema is undocumented and changes between versions: before any import, export the target site's kit and match keys (`elementor-fallback.md` §2). Motion tokens are not mapped.

## Gotchas

- Elementor ≥4.3 is not the same as "MCP enabled": a human must enable it (Elementor > Elementor MCP) and generate the client prompt/password. If the tools are not in this session, say so; do not guess an API.
- Whether MCP needs Pro is unclear (help article says Core + Pro; launch post says basic features work free). Check what the connected server actually exposes.
- Application Passwords fail silently on some hosts (security plugins, Basic Auth stripped by the server). A 401 on `/users/me` with a correct password means the host, not you.
- Global Colours and V4 colour Variables are separate stores. Set both from the same hex values or V3 widgets and the client's later edits drift.
- Elementor breakpoints default to 767/1024 px; the static CSS may use others. Match DESIGN.md breakpoints in Site Settings > Layout > Breakpoints before building, or the 768 px comparison breaks.
- Hover states on Global Classes are not gated by `(hover: hover)`. Keep hover changes to colour/underline/border so a sticky hover on touch is harmless; never lift or scale cards.
- `focus` on a class state may not equal `:focus-visible`. Check the rendered CSS; add a `:focus-visible` rule in custom CSS if needed.
- Elementor adds wrapper `div`s; the static page's heading levels and landmark elements (`header`, `nav`, `main`, `footer`) must be set explicitly on elements (HTML tag setting), or they come out as `div`/`h2`.
- Theme parts built while another header template is active stay hidden until conditions are set; do not "fix" by publishing.
- The Hello theme ships its own heading and link styles; they bleed through where a Variable is not bound. Set body/heading/link defaults in the kit.
- GSAP: check whether the site already loads a copy (view source, filter for `gsap`) before enqueueing another.

## Hand-off

When the draft build is complete and checked against the staging URL, run `/bexven-web:qa` on it; after QA passes, sync DESIGN.md (step 9) and remind the user to publish by hand and revoke the Application Password.
