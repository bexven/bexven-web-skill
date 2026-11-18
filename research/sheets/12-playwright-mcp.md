# 12 — Playwright MCP
https://github.com/microsoft/playwright-mcp · Tool (MCP server, npm `@playwright/mcp` v0.0.85) · Apache-2.0 · 39.8k stars · commit 16347fa, 2026-11-17

## 1. What it is
Microsoft's MCP server that lets an LLM drive a real browser through Playwright. By default it works from **accessibility snapshots** (a structured text tree with element refs), not pixels, so it needs no vision model. The repo is only a thin wrapper (README, config types, Docker). The source lives in the Playwright monorepo under `packages/playwright-core/src/tools/mcp`.

## 2. How it works
- **Loop:** `browser_navigate` → `browser_snapshot` (an ARIA tree with refs like `e12`) → act on a ref (`browser_click`, `browser_type`, `browser_fill_form`...) → each action returns a fresh snapshot. `browser_find` searches the snapshot for text or a regex, which is cheaper than pulling the whole tree.
- **Snapshot mode (default):** deterministic and text-only. `--snapshot-boxes` / `boxes:true` adds each element's x,y,w,h in CSS px, so it can catch layout overlap without images. `--snapshot-mode none` turns off the automatic snapshots.
- **Vision mode (`--caps=vision`):** adds coordinate mouse tools (`browser_mouse_click_xy`, `_move_xy`, `_drag_xy`, `_down`, `_up`, `_wheel`). The model reads a screenshot and clicks by x/y. It is only meant for elements missing from the a11y tree, such as canvas, custom widgets or sliders.
- **Screenshots work in both modes:** `browser_take_screenshot` (viewport, `fullPage`, single element, `scale` css or device, png/jpeg/webp, saved to a file). The image goes back to the model unless you pass `--image-responses omit`.
- **Tool groups.** Core is always on. The rest are opt-in via `--caps=`:
  - Core: navigate, navigate_back, snapshot, find, take_screenshot, click, hover, drag, drop, type, press_key, fill_form, select_option, file_upload, handle_dialog, wait_for, resize, emulate_media (colour scheme, reduced motion, forced colours, contrast, print), evaluate (JS), run_code_unsafe (raw Playwright code, RCE-equivalent), console_messages, network_requests / network_request, close.
  - Tabs: browser_tabs.
  - `network`: route / unroute / route_list (mocking), network_state_set (offline).
  - `storage`: cookies, local and session storage get/set/list/clear, storage_state save/restore.
  - `devtools`: highlight / hide_highlight, annotate (the user draws on a screenshot), start/stop_recording (the user's actions become Playwright code), tracing, video with chapters and action callouts, resume.
  - `vision`: the coordinate mouse tools above.
  - `pdf`: browser_pdf_save.
  - `testing`: generate_locator, verify_element_visible / list_visible / text_visible / value.
  - `config`: browser_get_config.
- **Useful flags for us:** `--viewport-size 1440x900`, `--device "iPhone 15"`, `--mobile`, `--headless`, `--isolated`, `--browser chrome|firefox|webkit|msedge`, `--output-dir`, `--codegen python` (recorded or generated code comes out as Python), `--init-script`, `--storage-state`, `--extension` (attach to the user's logged-in Chrome or Edge), `--cdp-endpoint`.
- **Profile:** persistent by default (`~/.cache/ms-playwright/mcp-{channel}-{hash}`), one browser per workspace. Use `--isolated` to run clients in parallel.
- **Install (NOT done here):** `claude mcp add playwright npx @playwright/mcp@latest`, or the standard `mcpServers` JSON (`npx @playwright/mcp@latest`). A Docker image `mcr.microsoft.com/playwright/mcp` exists (headless Chromium only). An HTTP transport is available via `--port 8931`.
- **README's own alternative:** for **coding agents**, the README recommends **Playwright CLI + SKILLs** (github.com/microsoft/playwright-cli). Its reason is token cost: MCP loads big tool schemas and verbose a11y trees into context. The README keeps MCP for long-running exploratory or self-healing loops where persistent browser state is worth the tokens.

## 3. Rules
- [tooling] Default QA path: a plain **Python Playwright script** that we own. It loops over breakpoints and saves full-page PNGs to `qa/shots/{page}-{width}.png`. It is cheap, repeatable and needs no MCP schema in context. Bexven already runs Playwright with Python.
- [tooling] Use Playwright MCP only for **interactive, exploratory** checks where Claude has to look, act and look again: menu toggles, sliders, popups, form flows, Elementor editor quirks, or reproducing a client-reported bug.
- [tooling] If browser control is needed often in Claude Code, prefer Playwright CLI + skill over MCP to save context. Check first that it is installed. Do not assume it is.
- [tooling] Use Chrome DevTools MCP, not Playwright MCP, for performance traces, Lighthouse/CWV, CSS computed styles and deep network/console debugging. Use Playwright MCP for cross-browser checks (WebKit = Safari proxy, Firefox) and device emulation.
- [qa] Screenshot every page at fixed breakpoints: **375, 768, 1024, 1440** (add 1920 for hero-heavy pages). Use full-page plus a viewport (above-the-fold) shot at each width.
- [qa] Visual QA loop: build → screenshot all breakpoints → Claude reviews each image against the design brief and AI-tell list → fix → re-shoot only the changed pages. Stop after it passes or after 3 rounds, then flag what is left for a human.
- [qa] Review screenshots for concrete faults: horizontal scroll, text overflow, overlapping elements, orphan words in headings, images cropped through faces, CTA below the fold on mobile, and unequal card heights where they matter.
- [qa] Use `boxes`/`--snapshot-boxes` or a Python `bounding_box()` check to detect overlap and off-canvas elements numerically. Do not rely on eyeballing.
- [qa] Shoot after fonts and lazy images have loaded: wait for `networkidle` plus `document.fonts.ready`, and scroll the page once to trigger lazy loading before a full-page shot.
- [qa] Turn off or finish animations before shooting (emulate `reducedMotion: reduce` or wait for them to end), so frames are not caught mid-fade.
- [a11y] Read the accessibility snapshot as a free a11y audit: missing button and link names, heading order, unlabeled form fields, and images without alt.
- [a11y] Check `prefers-color-scheme`, `prefers-reduced-motion` and `forced-colors` with emulate_media on at least the homepage.
- [qa] Check the console for errors and the network for 404s on every page before handing anything to a client.
- [qa] Run the WebKit pass once per site before sending an outreach link. Clients and prospects often open links on iPhone Safari.
- [process] Save the breakpoint screenshots of the Vercel redesign as the visual reference for the later WordPress/Elementor build, then compare the WP build against them.
- [process] Store screenshots in the project (`qa/shots/`) with predictable names. Do not let the MCP auto-name them into a temp output dir.
- [tooling] Never enable `browser_run_code_unsafe`, `--allow-unrestricted-file-access` or `--extension` on a client's logged-in admin unless the user explicitly asks. The README states that the MCP is not a security boundary.
- [tooling] Use `--isolated` (no persisted cookies) when testing client or prospect sites, so state does not leak between projects.
- [seo] Use a quick evaluate or a Python check for `<title>`, meta description, one `<h1>`, canonical and OG tags while the page is open anyway.

## 4. AI tells / anti-patterns it bans
n/a (this is a tool, not design guidance). The one relevant point: it is the means of *seeing* the rendered page. Without screenshots, Claude cannot catch visual AI tells such as identical cards, generic hero layouts or bad crops. The a11y tree alone shows structure, not looks.

## 5. Data, assets and scripts it ships (and what they need: Node, Python, Chrome)
- Needs Node.js >= 20 and an MCP client. Browsers come from Playwright (Chromium by default; Chrome, Edge, Firefox and WebKit are options). A headed browser needs a display, otherwise use `--headless` or the HTTP `--port` mode.
- The repo ships `cli.js` and `index.js` (thin entry points), `config.d.ts` (the full config schema), a Dockerfile and tests. It has no design data. Pins Playwright 1.66.0-alpha.
- Code generation can emit Python (`--codegen python`), so flows explored via MCP can become our Python QA scripts.

## 6. Area
QA / tooling

## 7. Take / skip
- **Take:** the breakpoint screenshot plus visual-review loop as a required step in the skill. Use snapshot boxes or bounding boxes for numeric layout checks, emulate_media for dark mode and reduced motion, console and network checks, WebKit for a Safari check, and `--codegen python` to turn exploration into scripts.
- **Take (as policy):** Python script first, MCP second, and Playwright CLI + skill if we want agent browser control without the token cost. Bexven's existing Python and Playwright stack covers 90% of QA more cheaply.
- **Skip:** vision/coordinate mode (rarely needed for brochure sites), the storage and network-mocking caps, video and tracing (except for a client demo), `--extension`, and Docker. Do not make the skill depend on an MCP being installed. It should degrade to the Python script.
- **Chrome DevTools MCP vs this:** use DevTools MCP for perf/Lighthouse and CSS debugging (Chrome only). Use Playwright MCP for multi-browser checks, devices and interaction. Pick one per session to limit context.

## 8. Open questions
- The Chrome DevTools MCP comparison above comes from general knowledge. It is not in this repo, so verify it against its own README.
- Playwright CLI was not read. Check its exact commands and whether its skill fits our Claude Code setup.
- SUGGESTED: Playwright CLI - https://github.com/microsoft/playwright-cli - the README names it as the token-efficient alternative for coding agents.
- SUGGESTED: Chrome DevTools MCP - https://github.com/ChromeDevTools/chrome-devtools-mcp - needed to settle when to use it vs Playwright MCP (perf traces, Lighthouse).
