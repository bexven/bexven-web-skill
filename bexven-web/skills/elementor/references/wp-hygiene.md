# WordPress hygiene for Elementor builds

House defaults for anything outside the Elementor canvas: theme, scripts, fonts, images, performance, security, ops. Rules are in our own words; WordPress API behaviour is stated as fact {13,15,26,27}.

## 1. Theme: Hello Elementor + child theme

- Default parent: Hello Elementor (minimal, made for Elementor). If the client's site already runs another theme with a reason (e.g. Astra with Woo), keep it and add a child theme to that.
- All custom code goes in a child theme, never in the parent (updates erase it) and never in "code snippet" boxes scattered across plugins.
- Minimum child theme: `style.css` (header with `Template: hello-elementor`), `functions.php`, `fonts/`, `assets/css/`, `assets/js/`. Version it in the project's git repo.
- Hello's own styles: turn off what you replace (Hello theme settings offer toggles for header/footer, page title, reset/theme CSS in recent versions). Unbound Hello defaults are a classic "looks like Elementor" tell.
- Page title: hide Hello's automatic title when the design has its own h1, and check exactly one h1 per page.

## 2. Enqueueing scripts and styles

- Register and enqueue from the child theme's `functions.php` on `wp_enqueue_scripts`; never hardcode `<script>` tags in header/footer templates or HTML widgets.
- Scripts in the footer with dependencies and a version: `wp_enqueue_script( 'site', get_stylesheet_directory_uri() . '/assets/js/site.js', array(), '1.0.3', array( 'in_footer' => true, 'strategy' => 'defer' ) );` (array form needs WP ≥ 6.3; older: pass `true`).
- Version strings: bump on change (or `filemtime()` of the file) so caches refresh.
- Load page-specific scripts only on those pages (`is_front_page()`, `is_page( 'contact' )`), not site-wide.
- Local copies only; no third-party CDNs at runtime. Pin exact versions in the filename or a comment.
- Stylesheet: enqueue the child `style.css` after the parent's handle as a dependency.

## 3. GSAP (only for a named moment)

Default is no GSAP: CSS transitions cover state changes and most single moments. Add GSAP only if DESIGN.md names a moment that needs a timeline, scroll-linking, SplitText or SVG drawing, and the static mock used it.
- First check for an existing copy: view the front-end source and the Network panel for `gsap`. Elementor or another plugin may already load one; whether current Elementor Pro bundles GSAP is unverified, so check rather than assume. Two copies = version conflicts and double weight.
- If needed: copy pinned files (e.g. `gsap.min.js`, `ScrollTrigger.min.js` from the same version) into `assets/js/vendor/`; enqueue `gsap` in the footer, then `gsap-st` with `array( 'gsap' )`, then `site-motion` with `array( 'gsap', 'gsap-st' )`. Only on the page with the moment.
- Init after `DOMContentLoaded`; register plugins once; scope selectors to the moment's root; wrap in `gsap.context()`.
- Reduced motion via `gsap.matchMedia()`: under `reduce`, skip `from()` tweens (show the final state), keep only ≤150 ms opacity/colour changes.
- Hidden start states only from JS (never inline `opacity:0` in the markup): content must show if JS fails.
- Elementor editor: guard against re-init in the preview (`elementorFrontend.isEditMode()`), revert the context on re-render.
- Call `ScrollTrigger.refresh()` after late images, web fonts (`document.fonts.ready`), or opened tabs/accordions. Remove `markers` before hand-off.
- GSAP and its plugins are free for client sites; never add a Club token or private registry. Don't package GSAP into a reusable visual animation-builder plugin (licence restriction on competing tools).

## 4. Fonts

- Self-host always. Loading from Google's CDN without consent sends visitor IPs to Google; a German court (LG München I, 2022) ruled that a GDPR breach. Fontshare's CDN has the same issue.
- Elementor Pro: Custom Fonts, WOFF2 per weight/style (or one variable WOFF2). Free: child-theme `@font-face`:
  ```css
  @font-face { font-family: "Display Name"; src: url("fonts/display-var.woff2") format("woff2");
    font-weight: 300 800; font-style: normal; font-display: swap; }
  ```
- Google families already used by Elementor widgets: turn on "Load Google Fonts Locally" (Elementor settings, Performance/Advanced tab).
- Subset to the languages used (latin, plus latin-ext for names with diacritics). Preload at most 1–2 files (the display face above the fold) with `<link rel="preload" as="font" type="font/woff2" crossorigin>` via `wp_head`.
- Disable font sets nobody uses (e.g. Font Awesome/eicons if the site uses its own SVG icons) only after checking no widget depends on them.
- Verify: DevTools Network filtered by "font" shows only same-origin WOFF2; zero googleapis/gstatic/fontshare requests.
- Keep each font's licence file in the project. Fontshare (ITF FFL) files: per-site upload only, never in a public repo or reusable kit.

## 5. Images

- Upload sizes: hero/full-width ≤ 2400 px wide, content images ≤ 1600 px; WebP or AVIF where the host supports it (WP ≥ 6.5 handles AVIF uploads if the server's image library does).
- Target weights: hero < 350 KB, others < 200 KB, total per page ≤ 1.2 MB.
- WordPress generates `srcset`; make sure the theme registers sensible sizes and the Image element uses "Full" or a large size so `srcset` has range.
- LCP image (usually the hero): an Image element, lazy load off, `fetchpriority="high"` (WP adds it to the first large image automatically since 6.3; confirm in source). Never a container background.
- Below-fold images lazy (WP core adds `loading="lazy"`; Elementor's "Lazy Load Background Images" setting covers backgrounds).
- Every image has width/height; alt text written per image (informational = describe, decorative = empty alt on purpose).
- SVG uploads: sanitise first (Elementor's SVG upload setting or a sanitiser); only from trusted sources.
- List every stock image still in the build; replace with client photos where supplied.

## 6. Performance and caching

- Turn on Elementor's performance features that are stable in the installed version (optimised DOM output, improved asset loading / CSS loading, inline font icons). Re-test after each.
- One caching plugin or the host's built-in cache, not two. Typical: host cache (Kinsta, WP Engine, SiteGround) or LiteSpeed Cache on LiteSpeed servers, WP Rocket elsewhere. Exclude form pages from aggressive JS delay if it breaks forms.
- Don't stack optimisation plugins (minify + delay + combine from three tools); conflicts are the usual cause of broken Elementor pages.
- Audit plugins: anything inactive gets removed; each active plugin earns its place. Check scripts per page in the Network panel.
- Measure → fix the biggest problem → re-measure the same URL, mobile throttling, median of 3 runs. Targets: LCP ≤ 2.5 s, CLS ≤ 0.1, INP ≤ 200 ms.
- Never flush caches, enable query logging or load-test on production without approval.
- After changing globals or classes: Elementor > Tools > Regenerate CSS & Data, then purge the page cache.

## 7. Security basics

- Build credentials: dedicated user, dedicated Application Password, revoked at handover; MCP turned off on live sites.
- Admin accounts: strong unique passwords, 2FA for humans, no shared "admin" user, least privilege for the client's editors (Editor role, not Administrator, unless they need it).
- Keep WP, plugins and themes updated on staging first; remove abandoned plugins.
- Disable file editing in admin (`define( 'DISALLOW_FILE_EDIT', true );` in wp-config, with user OK).
- Custom PHP: sanitise input early, escape output late (`esc_html`, `esc_attr`, `esc_url`), nonces plus `current_user_can()` on every action, `$wpdb->prepare()` for SQL, treat unauthenticated AJAX as hostile.
- Never commit secrets (wp-config, app passwords, SMTP keys) to git.
- Backups: host daily backups plus one manual snapshot before any build session.

## 8. WP-CLI tips

- Treat any environment as production until confirmed. Always pass `--path=` and/or `--url=`.
- Read-only checks first: `wp core version`, `wp plugin list --status=active`, `wp theme list`, `wp option get siteurl`, `wp user list --role=administrator`.
- Backup before risky work: `wp db export backup-$(date +%F-%H%M).sql`.
- Domain moves (staging → live): export, `wp search-replace 'https://staging.example' 'https://example.com' --all-tables --dry-run`, review counts, run for real, then `wp cache flush` and `wp rewrite flush`. Elementor stores URLs in its data: afterwards use Elementor > Tools > Replace URL (or `wp elementor replace-urls <old> <new>` where the Elementor CLI is available), then regenerate CSS (`wp elementor flush-css`). Command names differ between Elementor versions: confirm with `wp elementor --help` first.
- `db reset/import`, bulk deletes, mass plugin updates on production need explicit sign-off.
- Log date, environment, commands and exit codes in the hand-off notes.

## 9. Playground for local testing

- WordPress Playground (`npx @wp-playground/cli server`, Node 20+) gives a disposable WP with SQLite in seconds; no Docker. Good for: testing the child theme, a kit import dry run, checking a template JSON imports cleanly, reproducing a widget bug.
- Free Elementor installs from wordpress.org inside Playground; Pro needs its zip and licence, so Pro-only checks belong on staging.
- Blueprints (JSON) can preinstall plugins/theme and set options; keep one per project if you reuse it.
- Never point Playground at production data or import a live database into it with customer data.
- Playground is not an MCP target for the client build; use the client's staging.

## 10. Accessibility of Elementor widgets

Widgets don't guarantee accessibility; check each one used:
- Headings: set the HTML tag per heading (one h1, no skipped levels); don't pick tags for size.
- Landmarks: header/nav/main/footer tags on the right containers; one `main`.
- Nav Menu: keyboard-operable, visible focus, mobile toggle is a `button` with `aria-expanded`; test with Tab and Esc.
- Buttons vs links: links go somewhere, buttons do something. Elementor's Button widget renders `<a>`; for actions use a real button.
- Icon-only links (social, phone): accessible names (aria-label) on each.
- Tabs/accordions/toggles: prefer native `<details>` or Elementor's Atomic versions; check arrow-key/Enter behaviour and that collapsed content isn't the only copy of key info.
- Sliders/carousels: avoid; never autoplay. If unavoidable: visible prev/next, pause, swipe and keyboard.
- Forms: visible labels, errors tied to fields, focus to first error (Pro Form's default messages need rewriting).
- Contrast from tokens: body ≥ 4.5:1, large text/UI ≥ 3:1. Check after Hello/kit defaults are removed.
- Elementor's "Accessibility" options (e.g. skip link from Hello, focus outline) stay on; never remove focus outlines.

## 11. GPL note

- WordPress, Elementor Core and Hello are GPL-2.0+. PHP that hooks into WordPress (our child themes, small plugins) is distributed under GPL-compatible terms when shipped to the client; that's normal and fine.
- Our skill text is our own. The WordPress agent-skills repo is GPL: we take facts and ideas only and never copy its text or scripts into Bexven material.
- Elementor Pro is GPL but licensed per site for updates/support: use the client's own licence, not an agency key left behind.
- Font and image licences are separate from GPL: keep licence files; Fontshare files are never redistributed.
