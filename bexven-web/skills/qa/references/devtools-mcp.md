# Chrome DevTools MCP (optional)

Load at **step 3** only when the session already has `chrome-devtools` tools (names like `performance_start_trace`, `lighthouse_audit`, `get_css_styles`). It is a diagnosis layer on top of the Python Playwright scripts, never a requirement. {11,12,14}

**Never install it yourself**, never edit the user's MCP config, never run `npx chrome-devtools-mcp`. If it is missing, say which checks were skipped and use the fallbacks at the bottom.

## When to use which tool

| Job | Use | Why |
|---|---|---|
| Breakpoint screenshots, reduced-motion pass, overflow, console and failed requests, repeat runs | `screenshots.py` (Python Playwright) | Cheap, repeatable, same files every round, no MCP schema in context. Default. |
| WebKit / Safari check, Firefox | Playwright (script, or Playwright MCP if connected) | DevTools MCP is Chrome-only. |
| Clicking through a menu, form flow, popup, Elementor editor quirk, reproducing a client bug | Playwright MCP if connected, otherwise a short Python Playwright snippet | Look → act → look loops. |
| LCP / CLS / INP lab trace with named causes | **DevTools MCP** | Trace insights name the culprit (LCP subpart, CLS source). |
| Lighthouse accessibility, SEO, best-practices | **DevTools MCP** `lighthouse_audit`, or Lighthouse CLI | Note: the MCP's Lighthouse run excludes performance; use the trace for perf. |
| "Why doesn't this style apply?" (Elementor/theme specificity) | **DevTools MCP** `get_css_styles` | Shows matched rules, overridden declarations, resolved `var()` and the winning stylesheet line. |
| Chrome's own issue audits (missing labels, bad ARIA, cookies) | **DevTools MCP** `list_console_messages` with types `["issue"]` | Not available from Playwright. |
| WordPress plugin bloat, render-blocking CSS, third-party tags | **DevTools MCP** `list_network_requests` | Waterfall with resource types. |

Pick one browser MCP per session to keep context small.

## Recommended server flags (tell the user; do not set them yourself)

```
--isolated --no-usage-statistics --no-performance-crux
```
Add `--headless` on remote boxes or CI. Environment opt-out for update checks: `CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS=1`.

Why these matter:
- **Usage statistics go to Google by default.** `--no-usage-statistics` stops that.
- **Performance tools send the traced URL to Google's CrUX API** for field data. An unlaunched Vercel preview of a prospect's redesign must not leave the machine that way, and it has no field data anyway. `--no-performance-crux` stops that.
- **The default profile is persistent** and the agent can read every cookie and page in it. `--isolated` gives a throwaway profile. Never point it at a logged-in client WordPress admin unless the user asks; for Elementor staging use a separate staging login.
- Do not enable unrestricted file paths, and keep traces inside the project (`qa/`).

If the connected server was started without these flags and the page is an unlaunched preview, tell the user before running a performance trace.

Chrome will not start as root in many containers. If launch fails, tell the user the options (non-root user, or `--browser-url` to a Chrome they start); do not try to fix the environment.

## Recipes

**LCP / CLS (lab)**
1. `emulate`: viewport ~390×844 mobile with touch, CPU throttling 4, network "Slow 4G". (Each `emulate` call replaces the previous settings, so set all at once.)
2. `navigate_page` to the URL.
3. `performance_start_trace` with `reload: true`, `autoStop: true`, and `filePath: qa/trace-<page>-<n>.json`.
4. `performance_analyze_insight` for `LCPBreakdown`, `LCPDiscovery`, `RenderBlocking`, `CLSCulprits`; add `ImageDelivery`, `FontDisplay`, `ThirdParties` when relevant.
5. Fix the **largest LCP subpart** first (load delay and render delay should each be under ~10% of LCP). Compressing the image does nothing if the delay is render-blocking CSS.
6. Repeat ≥3 navigations; report the median with conditions. Label it **lab**. Re-trace the same URL after the fix and compare subparts.

INP needs real interaction: in a trace, click the menu toggle and submit the form, then read `INPBreakdown`. If you cannot interact, report INP as "not measured".

**Accessibility**
1. `lighthouse_audit` mode navigation, device mobile, output to file.
2. Filter the saved JSON for failing audits only (score < 1). Never read the whole report into context.
3. `list_console_messages` types `["issue"]`, `includePreservedMessages: true`.
4. `take_snapshot`: heading order, landmarks, accessible names on icon-only buttons; compare to a screenshot for DOM vs visual order.
5. Keyboard: `press_key` Tab / Shift+Tab, snapshot after each, confirm focus is visible and the mobile menu traps and returns focus. Take a fresh snapshot after any DOM change (old uids go stale).
6. `emulate` with `prefersReducedMotion: "reduce"`, then `forcedColors: "active"`, then `colorScheme: "dark"` if the site supports dark.

**CSS cascade (Elementor, theme, plugin conflicts)**
`take_snapshot` → find the element uid → `get_css_styles`. Read which declaration is overridden and which file/line wins. Fix the selector or move the style into the right Global Class/Variable; do not stack `!important`.

**Console and network gate**
`list_console_messages` (errors) and `list_network_requests` (filter for status ≥400). Both must be empty before handoff. Paginate; do not dump everything.

## Context hygiene
- Pass `filePath` for traces, screenshots and reports; read summaries, not dumps.
- Set `includeSnapshot: false` on input actions unless you need the tree.
- Paginate console and network lists.

## Fallbacks when DevTools MCP is absent
- Console errors, failed requests, overflow, reduced motion: `screenshots.py` already covers them.
- Lighthouse a11y/SEO/best-practices: Lighthouse CLI, only if `lighthouse` is already installed (`lighthouse --version`); write JSON to `qa/` and filter. Do not install it.
- Performance: if nothing is available, report "LCP/CLS/INP not measured (no trace tool)", list the static perf findings from lint (LCP image lazy, missing dimensions, CDN fonts, render-blocking scripts) as hypotheses, and suggest PageSpeed Insights only for a site that is already public (never for an unlaunched preview).
