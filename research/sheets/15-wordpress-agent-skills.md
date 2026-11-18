# 15 — WordPress agent skills
https://github.com/WordPress/agent-skills · Skill repo (20 skills + build/eval tooling) · GPL-2.0-or-later (LICENSE file, "Copyright (C) 2026 WordPress Contributors") · 2.4k stars · commit 7374e6f, 2026-11-05

## 1. What it is
The official WordPress-community set of agent skills for building WordPress "the modern way": block themes, theme.json, blocks, plugins, REST, WP-CLI, performance, Playground. The README says GPT-5.2 Codex wrote the skills from official Gutenberg/WP docs and WP contributors then reviewed them. Everything targets WordPress 7.0+ / PHP 7.4+. It covers Gutenberg only: nothing on Elementor or any other page builder.

**License note:** GPL-2.0-or-later is copyleft. If we copy or adapt its text or scripts into our skill, our skill becomes a derivative work and must be GPL too. Our skill is not GPL, so we take only facts and ideas (WP API behaviour, workflows), rewrite every rule in our own words, and ship none of its files (.mjs scripts, reference .md files). We can link to it. Facts like "slug `3xl` becomes `--3-xl`" are WordPress behaviour and can't be copyrighted. All rules below are paraphrased.

Skills (20): wordpress-router, wp-project-triage, wp-block-development, **wp-block-themes**, **wp-patterns** (in the repo but missing from the README table), wp-plugin-development, wp-rest-api, wp-interactivity-api, wp-abilities-api, wp-ability-development, wp-abilities-audit, wp-abilities-verify, **wp-wpcli-and-ops**, **wp-performance**, wp-phpstan, **wp-playground**, **blueprint**, **wp-env**, wpds (WordPress Design System: React admin UI, needs the WPDS MCP), wp-plugin-directory-guidelines.
I read in full: wp-block-themes, wp-patterns (SKILL + design-with-tokens, anti-patterns, visual-composition, part of registration), wp-plugin-development (+security), wp-wpcli-and-ops (+safety, search-replace), wp-performance, wp-playground, blueprint (first 120 lines), wp-env (first 60 lines), wordpress-router, wpds.

## 2. How it works
- Each skill has the same layout: a short SKILL.md (When to use / Inputs required / Procedure / Verification / Failure modes / Escalation), detail in `references/`, and Node `.mjs` detector scripts that print JSON.
- A router skill runs a triage script that classifies the repo (plugin, classic theme, block theme, core, full site) and then sends the agent to the right domain skill.
- wp-patterns has the only design workflow. Step 1: make 5 recorded decisions (purpose, tone, spatial composition, type hierarchy, colour strategy). Step 2: sketch the block nesting tree. Step 3: write the pattern PHP file. Steps 4–5: pass a Design Quality checklist and a Technical Validation checklist. Verification happens in Playground (`@wp-playground/cli server --auto-mount`) or by pasting into the Code Editor and checking for "block recovery" prompts.
- Ops skills put safety first: confirm the environment and the target (`--path`/`--url`), back up, dry-run, make the change, re-measure.
- Design principles of the repo itself: small composable skills, short SKILL.md with depth in references, deterministic checks done by scripts, upstream docs treated as the source of truth, an eval scenario for every skill. We should copy this structure for our own skill.

## 3. Rules
- [wp] For new builds, start a block theme from a known-good scaffold (Create Block Theme export, or the minimum set: style.css, theme.json, templates/index.html, parts/header + footer) rather than guessing the layout
- [wp] Use the highest theme.json schema version your minimum supported WP version allows; state that minimum explicitly
- [wp] Keep the two halves of theme.json apart: `settings` = what the editor offers (presets), `styles` = default look. Put brand tokens in settings presets and apply them through styles
- [wp] Style precedence is core → theme.json → child theme → user (DB) customisations. If a theme.json edit seems ignored, check for user overrides first
- [wp] After a client picks a style variation, the choice lives in the DB; editing the JSON file won't change their site
- [wp] Template parts live flat in `parts/` (no subfolders); templates go in `templates/*.html`
- [wp] WP rewrites preset slugs into kebab-case for CSS vars (`3xl` becomes `--wp--preset--font-size--3-xl`, `cardShadow` becomes `--card-shadow`). Write the emitted form, or the var silently uses its fallback. Prefer slugs that need no rewriting (e.g. `display`, `step-5`)
- [wp] WP 6.9+ theme.json can style text inputs/selects (`elements.textInput`, `elements.select`), border-radius presets (`settings.border.radiusSizes`) and button hover/focus, so less custom CSS is needed
- [wp] In patterns, express design only through block attributes and preset slugs: no `<style>`, no `<script>`, no made-up CSS classes, no raw HTML outside block wrappers
- [wp] Pattern PHP runs once at registration, not at render. Never query posts or users in it; use Query Loop / native blocks for anything dynamic
- [wp] Namespace pattern slugs `theme-slug/name`, keep the slug stable when updating, and remember that changing a pattern never updates content already inserted
- [wp] Ask before inventing a theme slug, text domain, asset path, CPT or theme-specific preset. Don't guess
- [process] Before writing any section markup, write down purpose, tone, composition, type hierarchy and colour strategy, then sketch the nesting tree
- [layout] Don't fall back on 3 equal columns or symmetric splits; use 66/33 or 60/40, grid spans and offset content
- [space] Vary padding and block gap by context (tight for related items, generous between sections) instead of one value everywhere; take spacing from the preset scale
- [colour] Vary section backgrounds through the page (light, inverted, accent) and keep the primary colour for CTAs in corporate tones
- [type] Each pattern needs clear heading/body contrast plus at least one deliberate typographic accent
- [copy] Placeholder text must read like real content (no lorem ipsum); buttons name the action ("View our services", not "Read more" / "Click here")
- [image] Use local theme assets via `get_theme_file_uri()` + `esc_url()`, never placeholder services; informational images get translated alt text, decorative ones get empty alt on purpose
- [a11y] Section headings start at h2 (h1 is the page title) and never skip levels; preset colour pairs must reach 4.5:1 for body text and 3:1 for large text
- [code] Escape every user-visible string with esc_html_e/esc_html__, attributes with esc_attr_*, URLs with esc_url, and use the theme's own text domain
- [code] Plugins: one bootstrap file; register hooks, don't do work at file load; keep admin-only code behind admin hooks; register activation hooks at top level
- [code] Security: sanitise/validate input early and escape output late in the matching context; a nonce stops CSRF but does not authorise, so always add `current_user_can`; read named `$_POST` keys after `wp_unslash`; use `$wpdb->prepare` for SQL; treat `nopriv` AJAX as attacker traffic
- [tooling] WP-CLI: treat prod as unsafe unless confirmed; always set `--path`/`--url`; `wp db export` before risky ops; domain moves = export, then `search-replace --dry-run`, then real run, then cache + rewrite flush; db reset/import, bulk deletes and mass prod updates need explicit sign-off
- [tooling] Log date, environment, exact commands and exit codes in ops scripts
- [perf] Measure a baseline first, fix one dominant bottleneck (queries / autoload / object cache / remote HTTP / cron), then re-measure the same URL. Never flush caches, turn on SAVEQUERIES or load-test on prod without approval
- [perf] Use `wp doctor check --all` and `wp profile stage` / `wp profile hook` to find slow hooks (often plugin bloat on builder sites)
- [perf] Block themes without custom stylesheets can render with no render-blocking CSS in WP 6.9 (styles inlined from theme.json), which is a strong argument for keeping design in theme.json
- [qa] Check patterns in Playground at desktop and mobile widths: they show in the inserter, insert without validation errors, stay editable, and locks hold
- [tooling] Prefer Playground (disposable, SQLite, no Docker) for quick previews; use wp-env only when you need MySQL, shell/Composer, or the repo already has `.wp-env.json`. Never point Playground at production data
- [tooling] Blueprints are JSON only and the schema rejects unknown keys; give `refType` when installing from a git branch or tag; shorthand order is unspecified, so use explicit steps when order matters

## 4. AI tells / anti-patterns it bans
Generic patterns (fewer than 3 distinctive choices), 3-equal-column defaults, every section on the same background, uniform padding, lorem ipsum, "Click here/Read more", placeholder image URLs, inline styles and custom classes in block markup, hard-coded hex values where a preset exists, a "one-note palette or repeated gradient treatment" in playful designs.
Possible conflicts: its own examples include an **uppercase letter-spaced eyebrow label** above the hero heading (a known AI tell elsewhere), a centred hero, and a gradient example using the core preset `vivid-cyan-blue-to-vivid-purple` (the purple-gradient tell). Its "alternate section backgrounds" advice can turn into a predictable light/dark/light banding. Its "tone" table maps tone to treatment fairly mechanically (e.g. bold = gradients + uppercase).

## 5. Data, assets and scripts it ships (and what they need: Node, Python, Chrome)
Node `.mjs` detectors: detect_wp_project (592 lines), detect_block_themes, detect_plugins, perf_inspect, wpcli_inspect (perf_inspect and wpcli_inspect also need WP-CLI). Build, install and validate scripts live in `shared/scripts`; WP/Gutenberg version map JSONs in `shared/references`; eval scenario JSONs in `eval/scenarios`. Playground needs Node 20.18+. wp-env needs Docker + Node 18.12+. wpds needs the WPDS MCP server. No Python, no Chrome. Nothing was run, per the brief.

## 6. Area
development / tooling (WP-specific). Some design guidance in wp-patterns.

## 7. Take / skip
**Take (rewritten in our own words):**
- theme.json token discipline, the slug-normalisation gotcha, and the user-override / style-variation DB caveats
- the safety checklists for WP-CLI migrations and search-replace (directly useful when moving a build from staging to the client's domain)
- the security baseline for any custom plugin or snippet we write
- the order "measure, fix one bottleneck, re-measure"
- Playground as the throwaway preview environment
- from wp-patterns: the 5-decision pre-flight, the anti-generic checklist and the composition-move ideas. These fit our anti-AI goals.

**Skip:**
- the abilities-* skills, wpds (React admin UI), phpstan, interactivity/REST (rarely needed for brochure sites), and the plugin-directory guidelines (we don't publish to wp.org)
- copying any file, because of GPL
- its eyebrow-label and preset purple-gradient examples
- the assumption that everything is Gutenberg. **Our main delivery stack is Elementor, which this repo never mentions** (Elementor appears only in a trademark slug list and a PHPStan ignore rule). So Elementor/Hello-theme/kit-global rules have to come from somewhere else.

**DESIGN.md → theme.json mapping (our idea):** one token source, three outputs.
- DESIGN.md colour roles map to `settings.color.palette` (set `defaultPalette:false`), with our own role slugs (e.g. `ink`, `paper`, `signal`, `muted`, `rule`) rather than the generic base/contrast/primary, so different clients don't share a vocabulary
- the type scale maps to `settings.typography.fontSizes` (fluid min/max)
- fonts map to `fontFamilies` with self-hosted `fontFace` files
- the spacing scale maps to `settings.spacing.spacingSizes` (turn off default sizes)
- radii map to `border.radiusSizes`; shadows to `shadow.presets`
- other tokens go in `settings.custom`
- defaults (body, headings, links, buttons, inputs) go in `styles.elements`/`styles.blocks`
- per-niche or per-client variants can be `styles/*.json` variations

The same DESIGN.md tokens can feed the Vercel static page (CSS custom properties) and the Elementor Kit (Global Colors / Global Fonts), which keeps the static redesign and the WP build visually identical. Use kebab-safe slugs so the CSS var names are predictable everywhere.

## 8. Open questions
- Should Bexven's WP phase move toward block themes (better performance, tokens in theme.json) or stay on Elementor? This repo makes the block-theme case, but nothing here helps with Elementor.
- The skills were written by AI and only reviewed by humans (v1). Check version-specific claims (6.9 features, WP 7.0 target) against the official handbook before relying on them.
- No URL errors; star count fetched OK.
- SUGGESTED: Elementor developer docs - https://developers.elementor.com/docs/ - official reference for Kit/global tokens, Hello theme and widgets, since this repo has no Elementor coverage.
- SUGGESTED: Create Block Theme plugin - https://wordpress.org/plugins/create-block-theme/ - the scaffold/export tool the skill recommends, if we ever ship block themes.
