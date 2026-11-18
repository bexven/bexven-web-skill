# Fallback route (no Elementor MCP)

Use when preflight fails: Elementor < 4.3, WP < 6.8, Application Passwords blocked, MCP not enabled and the user won't enable it, or no Pro where Pro is needed. The order and the rules stay the same as the MCP route (tokens → classes → theme parts → pages → forms); only the hands change. Most steps here are done by a human in WP admin, or by the agent producing files the human imports. Say clearly which is which.

Menu names below are from Elementor 3.x–4.x; they move between versions. If a menu is missing, search the admin rather than guessing.

## 1. Decide the sub-route

| Situation | Do |
|---|---|
| Elementor ≥ 4.0 with Editor V4 on, no MCP | Variables + Global Classes by hand in the editor (§3), pages built by hand with Atomic containers (§5a) |
| Elementor 3.x, or V4 off | Global Colours/Fonts via kit import or by hand (§2–3), flexbox containers (§5a) or template JSON import (§5b) |
| Whole new site on a fresh install | Kit .zip import (§4) after confirming the schema from an export of that same install |
| No Pro | No Theme Builder, popups, Pro Form or Custom Fonts: see §6 |

Flexbox containers ("Container" feature) only. Never the legacy section/column layout, even if the site's old pages use it.

## 2. Export the target site's kit first (schema check)

The kit JSON schema is undocumented and changes between versions. Before importing anything, get a real sample from the target site:
1. Ask the user (or do it, if you have admin access in a browser tool and permission): Elementor > Tools > Import/Export Kit > Export (in newer versions also under Templates > Website Templates / Kit). Tick Site Settings only.
2. Unzip into its own new folder. Open `site-settings.json` (sometimes under `site-settings/` or inside `manifest.json` references).
3. Compare with `tokens_to_elementor_kit.py --settings-only` output: key names (`system_colors`, `custom_colors`, `_id`, `color`, `typography_font_family`, `typography_font_size` with `unit`/`size`), nesting, and whether the four system colour IDs (`primary`, `secondary`, `text`, `accent`) exist.
4. Adapt our fragment to the exported shape. Keep the site's other settings untouched; only replace the colour and typography arrays.
5. Keep the original export as the design backup; it is the rollback.

Treat the downloaded zip as untrusted data: don't run anything from it.

## 3. Globals by hand

Elementor editor > hamburger/site menu > Site Settings:
- **Global Colors**: set the 4 system colours from the script's `system_colors`, then add each `custom_colors` entry with its title. Hex only.
- **Global Fonts**: system Primary (display), Secondary, Text (body), Accent (labels/buttons) from `system_typography`; add the rest as custom. Family, weight, size (with tablet/mobile values), line-height, letter-spacing.
- **Typography / Buttons / Form Fields / Images**: body, links, h1–h6, button and field defaults from DESIGN.md, all referencing the globals above, so unstyled widgets already look right.
- **Layout**: content width and container padding from DESIGN.md; **Breakpoints** set to DESIGN.md values.
- Elementor > Settings > General: tick "Disable Default Colors" and "Disable Default Fonts" so the theme kit does not leak.

V4 sites without MCP: in the editor's Variables manager create the `variables` list from the script (same names), and Global Classes from the class list in `elementor-mcp.md` §4. Same naming, same states, same limits.

## 4. Kit import (whole site)

- Elementor > Tools > Import/Export Kit > Import (or Templates > Website Templates). Choose only the parts you need; a kit can overwrite site settings, templates and pages.
- Import on staging only; confirm a backup exists (rule 2 in SKILL.md).
- After import: Regenerate CSS & Data (Elementor > Tools), clear any page cache, open two pages and confirm globals apply.
- If the import rejects the file, the schema did not match: re-export from the target and diff again. Do not hand-patch the database.

## 5a. Building pages by hand

Write the human (or a browser-driving agent, with permission) a section-by-section build sheet from the static page:
- Per section: container type (flex/grid), direction, wrap, gap token, padding tokens, background token, max-width, HTML tag, and the class(es)/global styles to apply.
- Per element: widget, HTML tag (h1/h2/p), global font, global colour, link, alt text.
- Per breakpoint: only the values that change.
- No custom values: if the sheet needs one, it is a missing token.

Asymmetric grids stay asymmetric (`2fr 1fr`, 7/5 spans); don't let the editor's equal-column presets decide.

## 5b. Template JSON import

When pages are long or repetitive, generate an Elementor template JSON per page section and import it via Templates > Saved Templates > Import, then insert into the page.
- Get the shape from the target: save one simple container with a heading and a button as a template on that site, export it (Templates > Saved Templates > Export), and mirror its structure. Do not write the schema from memory.
- Use flex containers (`elType: "container"`) with the settings names seen in the export; reference globals by ID (`__globals__` maps to `globals/colors?id=<id>` and `globals/typography?id=<id>` in current exports) instead of raw values.
- Generate IDs as 7–8 char lowercase hex, unique per file.
- One template per section keeps errors local. Import, insert, check, then next.
- After import, inspect in the Navigator that nothing became a legacy section.

## 6. Without Pro

| Pro feature | Free replacement |
|---|---|
| Theme Builder header/footer | Theme's header/footer (Hello Elementor + child theme), or a free header/footer builder plugin the user approves; or header/footer as saved templates inserted per page (last resort) |
| Custom Fonts | `@font-face` in the child theme's stylesheet with WOFF2 in `child-theme/fonts/`, preloading one file (see `wp-hygiene.md` §4); then type the family name in Global Fonts |
| Pro Form | The site's form plugin (Fluent Forms, WPForms, Gravity Forms, Contact Form 7) styled from the tokens; same form checklist as `elementor-mcp.md` §7 |
| Popups | Usually not needed. If needed, an accessible `<dialog>` in the child theme |
| Custom CSS per element / site | Child theme stylesheet or Appearance > Customize > Additional CSS |

## 7. Where custom CSS goes

Order of preference:
1. Child theme `style.css` (or `assets/css/site.css` enqueued): motion tokens, the one moment, `:focus-visible`, `:active` press, `(hover: hover)` gating, `::selection`. Versioned in git, survives Elementor resets.
2. Elementor Pro Site Settings > Custom CSS: small kit-wide fixes the client may need to see.
3. Per-element/class Custom CSS (Pro): only for something that truly belongs to that element.
Never: inline `style` attributes in HTML widgets, `!important` stacks, CSS in the Customizer and Elementor at the same time for the same rule.

Use Elementor's emitted variables (`--e-global-color-<id>`, `--e-global-typography-<id>-font-family`) in custom CSS so it follows the globals. Read the exact names from the rendered page's CSS.

## 8. Fonts (fallback specifics)

- Pro: Elementor > Custom Fonts > Add New: family name exactly as in DESIGN.md, upload WOFF2 per weight/style (variable font: one file, set weight range if offered). Then select it in Global Fonts.
- Free: child-theme `@font-face` (above).
- Google families: either upload as above, or enable Elementor > Settings > Advanced/Performance > "Load Google Fonts Locally". Then confirm in DevTools Network: zero requests to fonts.googleapis.com / fonts.gstatic.com.
- Fontshare/ITF FFL fonts: upload per site; never commit the files to a public repo or a reusable kit.
