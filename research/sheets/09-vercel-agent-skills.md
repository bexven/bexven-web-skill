# 09 — Vercel agent skills
https://github.com/vercel-labs/agent-skills · Skill repo (Agent Skills format, installable via `npx skills add`) · MIT (README "License: MIT"; `license: MIT` in frontmatter of react-best-practices, composition-patterns, react-view-transitions, react-native-skills; no root LICENSE file; the deploy/CLI/web-design/writing skills carry no per-skill license line) · 34.5k stars, 3.0k forks · commit 1a2c79d, 2026-10-27

## 1. What it is
Vercel's official skill collection: 10 skills, mostly React/Next.js engineering plus Vercel platform ops. Only one is about design (web-design-guidelines) and it is a code-review checklist for UI quality (a11y, forms, motion, typography details), not an aesthetic or "anti-AI-look" guide.

Skills: `web-design-guidelines`, `writing-guidelines`, `react-best-practices` (70 rules), `composition-patterns` (8 rules), `react-view-transitions` (+5 refs), `react-native-skills` (~35 rules), `deploy-to-vercel`, `vercel-cli-with-tokens`, `vercel-optimize` (big Node toolchain), plus zips of some skills for upload.

## 2. How it works
- **web-design-guidelines / writing-guidelines**: tiny SKILL.md (39 lines) that tells the agent to WebFetch a remote `command.md` from `vercel-labs/web-interface-guidelines` (or `writing-guidelines`) on every run, read the files the user names, and print terse `file:line - issue` findings grouped by file (`✓ pass` for clean files). The rules live outside this repo and can change at any time.
- **react-best-practices / composition-patterns / react-native**: SKILL.md is an index (category table with priority CRITICAL→LOW, rule-ID prefixes), one `rules/<prefix>-<name>.md` per rule (frontmatter title/impact/tags, incorrect vs correct code), and a compiled `AGENTS.md` (3,810 lines for React). A build package regenerates AGENTS.md and extracts test cases.
- **react-view-transitions**: decision tables (which transition pattern, in priority order, and which style for which navigation type) + step-by-step implementation audit + CSS recipe file.
- **deploy-to-vercel** (v4.0.0): decision tree. Step 1 runs four read-only checks: git remote, `.vercel/project.json` or `repo.json`, `vercel whoami`, `vercel teams list --format json`. Step 2 picks a method:
  - linked + git remote → ask the user, then commit + push (Vercel builds from the push), get the URL from `vercel ls --format json`;
  - linked, no remote → `vercel deploy [path] -y --no-wait`, then `vercel inspect <url>`;
  - not linked but authenticated → ask which team, then `vercel link --repo --scope <team>` (or plain `link`), then deploy;
  - no CLI → `npm install -g vercel`, `vercel login` (browser), link, deploy;
  - no auth possible (sandbox/agent) → `npx vercel@latest deploy [path] --temporary -y`. Needs no account, builds locally, prints a temporary URL plus a **claim URL** and expiry. Does not work in CI or in an already-linked dir.
  - Defaults: always a **preview**, `--prod` only if asked; always return the URL; do not curl the deployed URL. Needs: Node/npm, Vercel CLI, network to `*.vercel.com` + `registry.npmjs.org`, and optionally a logged-in session.
- **vercel-cli-with-tokens**: same flow, but auth comes from `VERCEL_TOKEN` (checks env → `.env` → any `vercel`-named var, `vca_` prefix → otherwise asks the user to create one at vercel.com/account/tokens). The token is never passed as `--token` (shell history leak). `VERCEL_ORG_ID` + `VERCEL_PROJECT_ID` together skip linking. Also covers `vercel env add/ls/pull/rm`, `vercel domains add`, `vercel inspect --logs`, `vercel logs`, and Stripe Projects plan changes (ask first).
- **vercel-optimize**: metrics-first cost/perf audit of a *deployed* project. Needs CLI v53+, login, a linked dir, Node 20+ and Observability Plus. Runs `collect-signals.mjs`, deterministic gates, then reads only the files those gates point to. Ships per-site-type playbooks (marketing, content, ecommerce...).

## 3. Rules
(From the fetched web-interface-guidelines, paraphrased, plus the relevant repo skills.)
- [a11y] Icon-only buttons and every form control get an accessible label; semantic HTML before ARIA
- [a11y] Decorative images `alt=""` and decorative icons hidden from AT; meaningful images get real alt text
- [a11y] Hierarchical headings, a skip link, polite live region for async updates; captions/transcripts for media
- [a11y] Visible focus everywhere; never drop `outline` without a replacement; prefer `:focus-visible`; sticky headers must not cover the focused element
- [forms] Set `autocomplete`, `name`, the correct `type` and `inputmode`; never block paste; labels clickable
- [forms] Turn spellcheck off for email/code/username; errors inline next to the field; focus first error on submit; warn before leaving unsaved changes
- [motion] Respect `prefers-reduced-motion` (always ship the reduced-motion CSS)
- [motion] Animate only `transform`/`opacity`; never `transition: all`; animations must be interruptible; long autoplay motion needs pause
- [motion] Each transition must communicate something (continuity, data arrived, new place); if you can't say what, leave it out
- [motion] Directional slides only for hierarchy (list→detail) or ordered sequences; lateral/tab moves fade or don't animate
- [motion] Exit faster than enter: recipe tokens ~150 ms exit, ~210 ms enter, ~400 ms move; ease-in for exit, ease-out for enter
- [type] Real ellipsis "…", curly quotes, non-breaking spaces (e.g. between number and unit); loading labels end in "…"
- [type] `font-variant-numeric: tabular-nums` in numeric columns/prices; `text-wrap: balance`/`pretty` on headings
- [layout] Plan for overflow: truncate/clamp/break-word; flex children need `min-width:0`; design empty states and very short/very long content
- [layout] Respect safe-area insets; no stray scrollbars; prefer CSS layout to JS measurement
- [image] Explicit width/height on every image; lazy-load below the fold; prioritise the hero (LCP) image
- [image] Serve hero images sized per viewport (`srcset/sizes`); never the native 4MP file on mobile
- [perf] Preconnect to asset/font origins; preload the critical font; video instead of animated GIF
- [perf] `defer`/`async` on scripts; load analytics, chat widgets, pixels, cookie banners after first paint, in parallel
- [perf] `content-visibility: auto` + `contain-intrinsic-size` for long off-screen sections or lists
- [perf] Batch DOM reads/writes (no layout thrashing); toggle classes rather than setting many inline styles
- [perf] Static marketing pages: long CDN cache (`s-maxage` + `stale-while-revalidate`)
- [nav] UI state lives in the URL (deep-linkable); use real `<a>` links, not clickable divs
- [components] Destructive actions need confirmation or undo
- [components] Buttons/links get hover feedback; hover/active/focus clearly stronger than the rest state
- [components] Touch: set `touch-action`/tap-highlight on purpose; stop overscroll behind modals; every gesture has a non-gesture alternative; use `autoFocus` sparingly
- [colour] Dark themes set `color-scheme`; `<meta name="theme-color">` matches the page background; style native `<select>` explicitly
- [copy] Active voice, second person, numerals for counts, specific button labels ("Save quote" not "Submit"), error text says how to fix it
- [code] Locale-aware dates/numbers via `Intl`; language from the browser, not IP; mark brand names `translate="no"`
- [code] (React) Avoid barrel imports, dynamic-import heavy components, parallelise independent fetches, no components defined inside components, ternary rather than `&&` for conditionals
- [code] (React) Avoid boolean-prop sprawl: use compound components / explicit variants instead
- [qa] Review output as `file:line - issue`, grouped by file, no preamble; it is fast to act on and easy to diff between runs
- [tooling] Deploy previews by default; `--prod` only on explicit request
- [tooling] Ask before any git push; on a linked repo, deploy via git push
- [tooling] Agent/no-login deploy: `vercel deploy --temporary -y` gives URL + claim URL + expiry; keep the claim link private
- [tooling] Tokens via `VERCEL_TOKEN` env only, never as `--token` or typed into echoed commands
- [tooling] Don't run `vercel link`/`project inspect` in an unlinked dir to "check" state (silently links or prompts); `whoami` is safe
- [tooling] Use `-y` and `--no-wait` to avoid blocking; `--format json` for parsing; check status with `vercel inspect <url>` (`--logs` for build logs)
- [tooling] Use `--scope <team>`; ask which team only if there is more than one

## 4. AI tells / anti-patterns it bans
Nothing aesthetic: no rules on fonts, palettes, gradients, card grids, section order or originality. The anti-pattern list is about engineering/UX: disabled zoom (`user-scalable=no`), paste blocking, `transition: all`, removed outlines, clickable `div`s, images without dimensions, unvirtualised long lists, unlabelled inputs, hard-coded date/number formats, gesture-only actions. The writing-guidelines skill (not fetched) bans "easy/simple/quick" and em dashes used as punctuation in docs, per README.

## 5. Data, assets and scripts it ships (and what they need: Node, Python, Chrome)
- Markdown rule libraries (React 70 rules, RN ~35, composition 8) + compiled AGENTS.md; view-transition CSS recipes.
- web-design / writing skills: no local data; they need network access to raw.githubusercontent.com and a WebFetch tool.
- deploy skills: no scripts; need Node/npm, Vercel CLI (`npm i -g vercel` or `npx vercel@latest`), network to `*.vercel.com`/npm registry, and either a browser login, a `VERCEL_TOKEN`, or nothing (temporary deploy).
- vercel-optimize: ~80 Node `.mjs` lib/scripts + tests; needs Node 20+, CLI v53+, a paid Observability Plus plan for route-level metrics. Not run (per brief).
- Repo tooling: `packages/react-best-practices-build` (TS build/validate), discovery-index build script.

## 6. Area
development / QA / tooling (light design-QA via web-design-guidelines)

## 7. Take / skip
- **Take: the web-interface-guidelines checklist as our QA pass.** Paraphrase it into our own `references/ui-qa.md`. Fetching it live (their approach) means the rules can change under us and a remote file gets injected into the prompt. Run it on each static redesign before deploy and output `file:line` findings. Most rules map straight to HTML/CSS and Elementor (custom CSS, attributes).
- **Take: the deploy-to-vercel decision tree for the cold-outreach preview.** For the cold-outreach mockup, `vercel deploy --temporary -y` gives a no-account preview + claim URL, but it expires. For an agency the right setup is `vercel-cli-with-tokens`: an agency `VERCEL_TOKEN` in env, one project per prospect, `vercel deploy -y --no-wait --scope <agency-team>`, preview by default, `--prod` only for the pitch link we send. Keep their safety rules: no `--token` flag, ask before git push, no probing `vercel link`.
- **Take** the motion rules (purposeful transitions, exit faster than enter, transform/opacity only, reduced motion), the perf rules relevant to static pages (hero sizing, defer third-party, preconnect/preload font, CDN caching, content-visibility), and the `file:line` review format.
- **Skip** react-best-practices / composition / RN / view-transitions API details for now: our static pages are plain HTML/CSS and the full builds are WordPress. Revisit only if we adopt Next.js. Skip vercel-optimize: it is for traffic-heavy deployed apps and needs a paid plan.
- **Skip** as a source of "not AI-made" design guidance: it has none. Pair with the aesthetic sources.
- **Conflict:** the web guidelines want Title Case for headings and buttons. Vercel's own writing guidelines (per README) and most modern design advice want sentence case. Pick one per brand; it should not be a global rule.

## 8. Open questions
- The web-design-guidelines rules are not in this repo. I fetched `raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` once (OK, read as a paraphrased summary). The license of that repo was not checked. Check it before copying anything near-verbatim.
- writing-guidelines remote file not fetched (out of scope); could be useful for client copy tone.
- Temporary deploy expiry length is not stated in the skill (the CLI prints it). Check whether that is long enough for an outreach email cycle, or whether we always use the token flow.
- SUGGESTED: Vercel Web Interface Guidelines - https://github.com/vercel-labs/web-interface-guidelines - the actual 100+ rule source behind web-design-guidelines; read it in full and record its license.
- SUGGESTED: Vercel writing guidelines - https://github.com/vercel-labs/writing-guidelines - voice/typography rules (sentence case, banned filler words) relevant to client-site copy.
