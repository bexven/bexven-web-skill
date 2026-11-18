# Elementor MCP route

Elementor ships its own MCP server inside the plugin (Core/Pro 4.3.0, 2026-09-22; extended in 4.4.0, 2026-11-09; fixes through 4.4.1). It reads and writes native, editable Elementor structures on the client's site. Facts below were read from Elementor's changelog, roadmap, launch post and help article on 2026-11-18 {16}. Menu labels move between versions: if one is not where stated, search the admin, do not guess.

## 1. Setup (human steps; the agent never does these)

Give the user this list when preflight finds MCP is not connected. Wait for confirmation.

1. Staging site, not production (host staging, a clone, or Playground for a dry run, see `wp-hygiene.md` §9).
2. WordPress ≥ 6.8, PHP ≥ 7.4. Elementor Core and Pro updated to ≥ 4.3.0 (4.4.x recommended: forms, uploads, undo).
3. Create a dedicated WP user for the build (Administrator is needed for theme parts and site settings), e.g. `bexven-build`. The AI acts with this user's permissions.
4. WP admin > Elementor > Elementor MCP > Enable MCP access > choose the client (Claude Code) > accept the notice > Generate Prompt. This creates an Application Password named like "Elementor MCP – Claude Code" on the logged-in user, so do it logged in as the build user.
5. Paste the generated prompt/config into Claude Code (or use the manual config option shown on the same screen). Restart the session so the tools load.
6. If generation fails with an Application Passwords error: a security plugin or the host has disabled them (common: Wordfence/iThemes settings, `WP_ENVIRONMENT_TYPE` rules, Basic Auth stripped by the server). Fix on the host or use the fallback route.
7. Afterwards: Users > Profile > Application Passwords > Revoke; Elementor > Elementor MCP > Turn off on any live site.

The transport and manual config format are not documented in what we read. Do not hand-write a config from memory; use the generated one.

## 2. Tool capabilities by version

Use the tool names the connected server actually lists; these are capability groups, not names.

| Since | Capability | Use it for |
|---|---|---|
| 4.3 | Read page structure | Preflight, conflict checks, verifying what was written |
| 4.3 | Build/redesign Atomic (V4) pages and layouts, a whole page per call | Step 4. Prefer one section per call: easier to verify and undo |
| 4.3 | Create, apply, reorder Global Classes; Variables (colour, font, size) incl. states and breakpoints | Steps 1–2 |
| 4.3 | Place, fill, create Components | Repeated blocks |
| 4.3 | Dynamic data (post fields, ACF, taxonomies) | Services/team/locations from CPTs if the site has them |
| 4.3 | Theme parts (header, footer, archive, popup) with display conditions | Step 3 |
| 4.4 | Many legacy V3 and Pro widgets | Only where no Atomic element exists |
| 4.4 | Forms (MCP-built forms get WebMCP), popup triggers | Step 5 |
| 4.4 | Rename elements | Navigator names that match static class/section names |
| 4.4 | Media Library uploads | Client photos, SVG logo (sanitised), Open Graph image |
| 4.4 | Undo via revisions | Any bad call |
| 4.4 | Cache clearing, System Info, licence info | Preflight; after global changes |

With the separate Angie plugin installed, the AI can also reach WordPress Abilities (WooCommerce, Yoast, ACF, WPForms…) and create custom widgets. Not needed for a visual rebuild; do not install Angie for this.

On 4.3.x without 4.4: no MCP forms or uploads. Upload media by hand (ask the user) and build the form in the editor or with the site's form plugin.

## 3. Build order

1. Variables: colours, fonts, font sizes, spacing, radii (from `tokens_to_elementor_kit.py --variables-only`).
2. Global Colours + Global Fonts (kit) from the same values, so V3 widgets and future client edits share the palette.
3. Site Settings that are not tokens: breakpoints matching DESIGN.md, container default width/padding, body/link/heading defaults, default colours and fonts disabled.
4. Global Classes for repeated patterns, bound to Variables, with states and breakpoint values.
5. Components for repeated blocks.
6. Header and footer theme parts, display condition "Entire site" (minus exceptions). Leave unpublished until asked.
7. Pages, one section at a time, top to bottom. After each section: read the structure back and compare with the static DOM.
8. Forms, then popups (only if the task needs one).
9. Clear cache, then QA.

Never start with pages "to see how it looks": pages built before classes collect inline values that never get cleaned up.

## 4. Mapping the static page

Static CSS is the spec. Names stay the same on both sides so QA can diff them.

| Static (from build skill) | Elementor | Notes |
|---|---|---|
| `:root { --color-ink: #1d2320 }` | Variable `color-ink` (colour) + Global Colour "Ink" | Script names: `color-<key>` |
| `--font-display: "Font", serif` | Variable `font-display` (font) + Global Font family | Upload the font first (`wp-hygiene.md` §4) |
| `--text-body: 1.0625rem` / `clamp(...)` | Variable `text-body` (size) | Fluid `clamp()` goes in as a custom unit; check it renders |
| `--space-4: 1.5rem` | Variable `space-4` (size) | Use for gaps and padding only |
| `--radius-card: 6px` | Variable `radius-card` (size) | |
| `--dur-*`, `--ease-*` | Not mapped | Keep in child-theme CSS for the one moment and state transitions |
| `.btn`, `.btn--primary` | Global Classes `btn`, `btn-primary` | Base + modifier; states on the class |
| `.card`, `.review` | Global Class + Component | Component holds structure, class holds look |
| `.section`, `.section--inverse` | Global Classes on the section container | Padding, background, max-width via Variables |
| `.field`, `.field__error` | Form widget styling bound to Variables; Global Class where the form is Atomic | Error text colour from a role Variable |
| `display:flex; gap` section | Atomic flexbox container, gap = `space-*` | Direction/wrap/align per breakpoint |
| `display:grid; grid-template-columns: 2fr 1fr` | Atomic grid container | Keep the asymmetric split; do not "simplify" to equal columns |
| `<img>` hero with `fetchpriority="high"` | Atomic Image element, lazy load off for this one | Never a container background |
| Inline SVG icon | Uploaded sanitised SVG / custom icon | One icon family, same weight |
| `<header>`, `<nav>`, `<main>`, `<footer>`, `h1–h3` | Element HTML tag setting | Elementor defaults to `div`/`h2` |
| One-off value used once | Not allowed | Add a token to DESIGN.md or reuse an existing one |

Class naming: lowercase, hyphenated, no prefixes like `e-` that collide with Elementor's own. Keep the count small; a brochure site rarely needs more than 40–80.

## 5. States and breakpoints

- States on a class: normal, hover, focus, active (and whatever else the version offers). Copy the static values exactly.
- Hover is not gated by `(hover: hover) and (pointer: fine)` in Elementor. Keep hover to colour/underline/border/shadow changes; no lift/scale on cards (one hover-motion idea per site at most, on a child, as in DESIGN.md).
- Focus: confirm the rendered CSS uses `:focus-visible` or a visible ring; if the class state compiles to `:focus` only, add in custom CSS: `.btn:focus-visible { outline: 2px solid var(--e-global-color-…); outline-offset: 3px }` using the real variable name from the rendered page.
- `:active` press feedback (`scale(.97)`, ~120 ms) belongs in custom CSS if the class state can't express transforms with transitions.
- Breakpoints: Elementor V4 styles cascade desktop → tablet → mobile. Defaults are mobile ≤767, tablet ≤1024 (optional mobile-extra, tablet-extra, laptop 1366, widescreen 2400). Set them to the DESIGN.md breakpoints before building and enable only those you use.
- Fluid type/spacing via `clamp()` Variables needs fewer breakpoint overrides; prefer it when the static CSS used it.
- Test 375, 768, 1280 in the editor's responsive mode and in a real browser; the editor preview is not proof.

## 6. Drafts, conflicts, undo

- MCP output saves as a draft. Leave it there. Publishing is a separate, explicit user request.
- If the user (or anyone) edits the same page in the editor while the agent writes, Elementor flags a conflict. Stop, re-read the page structure, merge, continue. Never force your version.
- Before large rewrites of an existing page: note the current revision (or ask the MCP for it); use the revisions-based undo if a call breaks the page.
- After global changes (Variables, classes, kit): clear Elementor's CSS cache (4.4 tool, or Elementor > Tools > Regenerate CSS & Data).
- Never write `_elementor_data` or `_elementor_page_settings` directly.

## 7. Forms checklist (Elementor Pro Form or form plugin)

From the build skill's form rules, as they apply here:
- Visible label on every field (label toggle on); placeholders are hints, not labels.
- Required fields marked in text ("required") or optional ones marked; consistent.
- `type` and autocomplete correct (email, tel, name); phone accepts spaces/dashes; no input masks that block paste.
- Field height ≥ 44 px, input font ≥ 16 px on mobile.
- Button names the result: "Send message", "Request a quote". Never "Submit"/"Send".
- Error messages (custom messages setting) say what is wrong and how to fix it; no "Oops".
- Success message only after a real send, says what happens next and when, no exclamation mark.
- Actions after submit: email to the client's real address (or a redirect to a thank-you page). Test delivery end to end; WordPress `wp_mail` from many hosts lands in spam, so use an SMTP plugin the client approves.
- Spam: Honeypot field on; no reCAPTCHA by default. Turnstile only if spam persists, mentioned in the privacy text.
- One plain consent sentence under the button with a privacy-policy link; checkbox only when legally needed, never pre-ticked.
- `tel:` and `mailto:` links visible next to the form.
- File upload (quote forms): formats and size limit stated before the field.
- Popups: only when the task needs one, never on page load, never before the visitor has read anything; triggers on click (e.g. "Request a quote" button). Esc closes, focus returns to the trigger.

## 8. Limits and unknowns (2026-11)

- Pro requirement for MCP: unclear (help article says Core + Pro 4.3; launch post says basic sections are free). Trust the connected server's tool list.
- Global Classes: hard limit 1000 per site.
- No Atomic mega menu until 4.5 (roadmap Q1 2027); use the V3/Pro Nav Menu widget meanwhile. "MCP Skills" and pre-built atomic structures are roadmap items, not available.
- No global motion setting; motion tokens stay in custom CSS.
- Whether colour Variables accept `oklch()` is unverified: hex only.
- Transport/manual config undocumented; use the generated prompt.
- Third-party alternative (msrbuilds/elementor-mcp, works on older/free installs) is unreviewed. Do not install it without the user's decision; it is not part of our default route.
