# 11 — Chrome DevTools MCP
https://github.com/ChromeDevTools/chrome-devtools-mcp · Tool (MCP server + CLI + bundled agent skills) · Apache-2.0 (Google LLC) · 58.2k stars · commit 4559cd5, 2026-11-18 (package v1.13.0)

## 1. What it is
Google's official MCP server (package `chrome-devtools-mcp`, now branded "Chrome DevTools for agents") that lets a coding agent drive and inspect a live Chrome via Puppeteer and the DevTools frontend. Its strength is diagnosis: performance traces with Core Web Vitals insights, Lighthouse audits, console issues with source-mapped stacks, network requests, and the CSS cascade. It also ships a `chrome-devtools` CLI and 8 agent skills.

## 2. How it works
- **Install (record only, we did NOT install):** MCP config `npx -y chrome-devtools-mcp@latest`; for Claude Code `claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest`, or as a plugin (MCP + skills) via `/plugin marketplace add ChromeDevTools/chrome-devtools-mcp` then `/plugin install chrome-devtools-mcp@chrome-devtools-plugins`. The CLI comes from a global npm install.
- **Needs:** Node LTS (engines `^20.19 || ^22.12 || >=23`), npm, Chrome stable or newer (only Chrome / Chrome for Testing are officially supported). Chrome will not start as root, which is common in containers, and it fails inside OS-level MCP sandboxes (Seatbelt or Linux containers). The workaround is `--browser-url` to a Chrome you start yourself.
- **Lifecycle:** Chrome launches lazily on the first browser tool call. It runs headed by default (`--headless` is opt-in) and uses a **persistent profile** at `~/.cache/chrome-devtools-mcp/chrome-profile`. `--isolated` gives a throwaway profile instead. `--autoConnect`, `--browserUrl` and `--wsEndpoint` attach to an existing Chrome.
- **Interaction model:** `take_snapshot` returns the accessibility tree with element `uid`s. Input tools act on those uids. Every page-scoped tool needs a `pageId` (from `list_pages` or `new_page`). Large outputs (traces, screenshots, Lighthouse reports) go to files. The design principle is "semantic summary, not 50k lines of JSON".
- **Tool list (default-on groups):**
  - Input (10): click, drag, fill, fill_form, handle_dialog, hover, press_key, type_text, upload_file, click_at
  - Navigation (6): close_page, list_pages, navigate_page, new_page, select_page, wait_for
  - Emulation (2): `emulate` sets viewport (WxHxDPR, mobile, touch, landscape), colorScheme, prefersReducedMotion, forcedColors, prefersContrast, CPU throttling, network presets (Offline to Fast 4G), geolocation, UA and extra headers. Each call replaces the previous settings. `resize_page` is the second tool.
  - Performance (3): performance_start_trace (reload, autoStop, ignoreCache, filePath), performance_stop_trace, performance_analyze_insight. Insight names seen in the source: LCPBreakdown, LCPDiscovery, RenderBlocking, DocumentLatency, CLSCulprits, INPBreakdown, ImageDelivery, FontDisplay, ThirdParties, Cache, Viewport, DOMSize, ForcedReflow, NetworkDependencyTree.
  - Network (2): list_network_requests (filter by resourceTypes, paginated, keeps the last 3 navigations), get_network_request (headers and bodies, optionally saved to file).
  - Debugging (10): evaluate_script, list_console_messages / get_console_message (type `issue` gives Chrome's own audits), get_css_styles (matched rules, cascade layers, overridden declarations, resolved `var()` values, source lines), lighthouse_audit (a11y, SEO, best practices and "agentic browsing", but **not performance**; desktop or mobile, navigation or snapshot mode), take_screenshot (full page or element, png/jpeg/webp), take_snapshot, screencast_start/stop (mp4), set_logpoints.
  - Memory (14 heap-snapshot tools). The docs disagree on whether these are on by default; the skills say `--memoryDebugging` is required.
- **Opt-in groups (flags):** network mocks (`--categoryNetworkMocks`), extensions, PWA, WebAuthn, WebMCP, third-party dev tools, plus the DevTools-UI comment tools (`--devtools-comments`, Chrome M159+). `--slim` cuts the server down to 3 tools: navigate, evaluate and screenshot.
- **Privacy and telemetry:**
  - Usage statistics go to Google and are **on by default**. Opt out with `--no-usage-statistics`, or set `CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS` or `CI`.
  - Performance tools **send trace URLs to the Google CrUX API** to fetch field data. Turn this off with `--no-performance-crux`.
  - The server checks npm for updates. Turn this off with `CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS`.
  - The MCP client can read everything in the browser profile. `--redactNetworkHeaders` is off by default.
  - File tools are limited to the OS temp dir unless MCP roots, `--filesystemRoot` or `--allowUnrestrictedPaths` say otherwise. The CLI defaults to unrestricted paths.
  - Hardening flags: `--allowedUrlPattern` / `--blockedUrlPattern`, `--no-javascript-evaluation`, `--no-file-navigations`. A config file can set these, so the agent must not be able to write it.

## 3. Rules
- [tooling] Use Playwright as Bexven's default browser driver: scripted, repeatable multi-viewport screenshot sweeps, visual diffs, cross-browser checks (WebKit/Firefox) and anything that runs in CI.
- [tooling] Switch to Chrome DevTools MCP for diagnosis Playwright doesn't give out of the box: CWV traces with named insights, Lighthouse a11y/SEO/best-practice audits, Chrome "issue" console audits, the CSS cascade, and the network waterfall.
- [tooling] Treat DevTools MCP as optional. If its tools aren't in the session, fall back to Playwright plus the Lighthouse CLI and say what was skipped. Never install it for the user.
- [tooling] Recommended server args for agency work: `--isolated --no-usage-statistics --no-performance-crux`, plus `--headless` in CI or on remote boxes.
- [process] For an unlaunched prospect redesign (Vercel preview), keep CrUX off. Field data won't exist anyway, and the preview URL would otherwise go to Google.
- [perf] Run every perf check as navigate, then `performance_start_trace` with reload=true and autoStop=true, then drill into LCPBreakdown, CLSCulprits and RenderBlocking with `performance_analyze_insight`. Don't eyeball screenshots for perf.
- [perf] Measure under mobile constraints: emulate a 390-412px mobile viewport, CPU throttle 4, network "Fast 3G" or "Slow 4G". Report lab numbers as lab, not as field data.
- [perf] Targets: LCP ≤ 2.5 s, CLS ≤ 0.1, INP ≤ 200 ms. Fix the biggest LCP subpart first (load delay and render delay should each be under 10%).
- [perf] Never lazy-load the hero/LCP image. Give it `fetchpriority="high"`, a plain `<img src>`, modern formats and `srcset`, and preload it if it isn't discoverable in the HTML.
- [perf] When CLSCulprits flags web fonts or late images, fix with explicit width/height, `aspect-ratio`, `font-display` plus size-adjusted fallbacks, and space reserved for embeds and cookie banners.
- [perf] Re-run the same trace after a fix and compare the subpart breakdown before calling it done.
- [a11y] Run `lighthouse_audit` (mode navigation, device mobile), then filter the saved report.json for failing audits with jq/node. Don't read the whole report into context.
- [a11y] Also run `list_console_messages` with types ["issue"] and includePreservedMessages=true. Chrome flags missing labels and bad ARIA there.
- [a11y] Use `take_snapshot` to check heading order (no skipped levels), landmarks, and an accessible name on every icon-only button. Compare it with a screenshot to catch visual order differing from DOM order.
- [a11y] Test keyboard: `press_key` Tab / Shift+Tab, snapshot, confirm focus lands where expected, and confirm modals and mobile nav trap focus.
- [a11y] Check tap targets ≥ 48×48 px and contrast by script, not from screenshots. Screenshots only work as a sanity check on text over images or gradients.
- [motion] Emulate `prefersReducedMotion: "reduce"` and confirm scroll/entrance animations are off or reduced.
- [colour] Emulate `forcedColors: "active"` and `colorScheme: "dark"` (if the site supports dark) and check that brand colours don't break legibility.
- [seo] Use the Lighthouse SEO category as a floor (title, meta description, crawlable links, hreflang, robots) on every static redesign before outreach.
- [qa] Before handoff, require zero console errors and zero failed (4xx/5xx) network requests, checked with `list_console_messages` and `list_network_requests`.
- [code] When a style "doesn't apply" (Elementor or theme specificity wars), use `get_css_styles` on the element. The output lists the overridden declarations and the stylesheet line that wins. Fix the cascade, don't pile on `!important`.
- [wp] On WordPress builds, check the network waterfall for plugin bloat: count scripts/styles per page, third-party tags, and render-blocking CSS from Elementor or widgets.
- [tooling] Pass `filePath` for traces and screenshots. Set `includeSnapshot:false` on input actions, and paginate console/network lists to save context.
- [tooling] Take a fresh snapshot after any DOM change. Old uids go stale.
- [tooling] Never point DevTools MCP at a logged-in personal profile or client admin sessions unless the user asks. Every cookie and page is visible to the agent. Use `--isolated`.
- [process] If the bundled skills are installed, keep their version matched to the server. Skills that are out of date call renamed tools or parameters.

## 4. AI tells / anti-patterns it bans
n/a for visual design. Its process anti-patterns: judging contrast or perf from a screenshot; reading whole JSON reports into context; optimising one LCP subpart (e.g. compressing the image) while the real bottleneck is render delay; lazy-loading the LCP image; reusing stale element uids.

## 5. Data, assets and scripts it ships (and what they need: Node, Python, Chrome)
- npm package with two binaries, `chrome-devtools-mcp` and `chrome-devtools` (CLI). Needs Node 20.19+/22.12+, npm and Chrome stable. ffmpeg is optional for screencasts. Lighthouse is bundled (`update-lighthouse` script).
- **Bundled skills** (`skills/`, 881 lines total), each a SKILL.md, some with references:
  - `chrome-devtools`: core workflow (navigate, wait, snapshot, interact; tool selection)
  - `chrome-devtools-cli`: shell usage of the CLI
  - `a11y-debugging`: Lighthouse, console issues, snapshot semantics, focus, tap targets, contrast; ships `references/a11y-snippets.md` with JS snippets for orphaned inputs, tap-target size, contrast and global checks
  - `debug-optimize-lcp`: LCP subparts table, a 5-step trace workflow and a fix catalogue; ships 4 references including LCP snippets
  - `cookie-debugging`: auth, SameSite, consent-banner compliance
  - `memory-leak-debugging`: heap snapshots
  - `inspect-in-devtools`: open/reveal in the DevTools UI and comment threads (Chrome M159+, headed)
  - `troubleshooting`: connection wizard
- Plugin manifests for Claude, Cursor, Gemini and Kimi (`.claude-plugin`, `gemini-extension.json`, etc.).
- Docs: tool-reference, slim-tool-reference, configuration (about 60 flags plus a JSON config file), troubleshooting (root, sandbox, WSL, VM), design-principles.

## 6. Area
QA / tooling (performance, accessibility, debugging)

## 7. Take / skip
- **Take:** treat it as the optional "diagnose" layer of our QA step, used after building and before outreach or handoff. Specifically: the trace + insight workflow for LCP/CLS/INP, Lighthouse a11y/SEO/best-practices with report filtering, console `issue` audits, `get_css_styles` for Elementor specificity bugs, and `emulate` for reduced-motion, forced-colors and dark mode. Paraphrase the LCP subpart model and the a11y workflow into our QA checklist; they're short and correct.
- **Take:** the privacy defaults (`--isolated --no-usage-statistics --no-performance-crux`) as our recommended config line.
- **Skip:** making it a hard dependency. Our skill must still work with Playwright alone, because DevTools MCP is Chrome-only, fails as root or in sandboxes, and its telemetry is on by default.
- **Skip:** memory, extension, PWA, WebAuthn, WebMCP, network-mock and DevTools-comments tools. They don't matter for brochure sites.
- **Skip:** copying its bundled skills into ours verbatim. Reference them instead. They're versioned with the server, so copies would go stale.
- **Playwright vs DevTools MCP:** Playwright for building and regression (deterministic scripts, many viewports, many browsers, CI, screenshots for design review). DevTools MCP for interactive "why is it slow / broken / inaccessible" questions on one page in Chrome.

## 8. Open questions
- The memory tools are listed as on by default (`--categoryMemory` default true), but the bundled skills and the `--memoryDebugging` flag (default false) say they need opt-in. The docs are inconsistent; this doesn't matter for us.
- Is Bexven's QA run in a container as root? If so, Chrome won't start, and the user needs a non-root user or `--browser-url`.
- Should the skill also check the Lighthouse "agentic browsing" category? It's new, and its value for small-business sites is unclear.
- SUGGESTED: Lighthouse CI - https://github.com/GoogleChrome/lighthouse-ci - runs perf + a11y budgets in CI without an MCP server; a fallback when DevTools MCP isn't available.
- SUGGESTED: Playwright MCP - https://github.com/microsoft/playwright-mcp - the direct alternative MCP for agent browser control; compare it before picking a default.
