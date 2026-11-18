#!/usr/bin/env python3
"""screenshots.py - full-page Playwright screenshots at QA widths, plus overflow and console checks.

For each width (default 375, 768, 1024, 1440) the page is loaded in Chromium
at deviceScaleFactor 1, then:
  1. wait for the 'networkidle' load state and document.fonts.ready
  2. scroll to the bottom in steps (triggers lazy images / inView code), then
     back to the top, and wait for network idle + fonts again
  3. save a full-page PNG to --out as <name>-<width>.png
  4. report horizontal overflow (documentElement.scrollWidth > clientWidth),
     the widest offending elements, and console errors / uncaught page errors

TARGET may be an http(s) URL, a file:// URL or a local file path (converted to
file://). Only the given page and the resources it requests are loaded.

Options
  --reduced-motion   emulate prefers-reduced-motion: reduce
  --dark             emulate prefers-color-scheme: dark
  --widths 375,1440  override widths
  --height 900       viewport height (full-page capture ignores it for the PNG)
  --json             print the report as JSON

Requires Playwright for Python (from playwright.sync_api import sync_playwright).
Uses Playwright's bundled Chromium; if that is not installed it falls back to
an installed Google Chrome or Edge (channel "chrome" / "msedge").

Exit codes: 0 ok, 1 horizontal overflow, console errors or a load failure at
any width, 2 usage error (bad widths, missing file, Playwright missing).

Examples
  screenshots.py dist/index.html --out shots/
  screenshots.py https://preview.example.vercel.app --out shots --reduced-motion
  screenshots.py file:///abs/path/page.html --widths 375,1440 --json
"""
import argparse
import json
import os
import re
import sys
from urllib.parse import urlparse
from pathlib import Path

DEFAULT_WIDTHS = [375, 768, 1024, 1440]

SCROLL_JS = """
async () => {
  const step = Math.max(200, Math.floor(window.innerHeight * 0.8));
  let y = 0;
  for (let i = 0; i < 200; i++) {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    if (y >= max) break;
    y = Math.min(y + step, max);
    window.scrollTo(0, y);
    await new Promise(r => setTimeout(r, 120));
  }
  await new Promise(r => setTimeout(r, 300));
  window.scrollTo(0, 0);
  await new Promise(r => setTimeout(r, 200));
}
"""

OVERFLOW_JS = """
() => {
  const de = document.documentElement;
  const cw = de.clientWidth;
  const offenders = [];
  if (de.scrollWidth > cw) {
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) continue;
      if (r.right > cw + 1 || r.left < -1) {
        let p = el.parentElement, clipped = false;
        while (p && p !== document.body) {
          const s = getComputedStyle(p);
          if (/(hidden|clip|auto|scroll)/.test(s.overflowX)) { clipped = true; break; }
          p = p.parentElement;
        }
        if (clipped) continue;
        let sel = el.tagName.toLowerCase();
        if (el.id) sel += '#' + el.id;
        else if (el.classList.length) sel += '.' + [...el.classList].slice(0, 2).join('.');
        offenders.push({selector: sel, left: Math.round(r.left), right: Math.round(r.right),
                        width: Math.round(r.width)});
      }
    }
  }
  offenders.sort((a, b) => b.right - a.right);
  return {scrollWidth: de.scrollWidth, clientWidth: cw, overflow: de.scrollWidth > cw,
          offenders: offenders.slice(0, 5), height: de.scrollHeight};
}
"""


def to_url(target):
    if re.match(r"^(https?|file)://", target, re.I):
        if target.lower().startswith("file://"):
            path = urlparse(target).path
            if not os.path.exists(path):
                raise FileNotFoundError(path)
        return target
    p = Path(target)
    if not p.exists():
        raise FileNotFoundError(target)
    return p.resolve().as_uri()


def slug_for(url):
    u = urlparse(url)
    if u.scheme == "file":
        base = Path(u.path).stem or "page"
    else:
        base = (u.netloc + u.path).strip("/") or "page"
    return re.sub(r"[^A-Za-z0-9_-]+", "-", base).strip("-")[:60] or "page"


def parse_widths(s):
    try:
        ws = [int(x) for x in s.split(",") if x.strip()]
    except ValueError:
        raise argparse.ArgumentTypeError("widths must be comma-separated integers")
    if not ws or any(w < 200 or w > 4000 for w in ws):
        raise argparse.ArgumentTypeError("each width must be 200-4000")
    return ws


def shoot(url, widths, out_dir, name, height, reduced, dark, timeout_ms):
    from playwright.sync_api import sync_playwright, Error as PWError
    results = []
    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch()
        except PWError as first:
            # Bundled Chromium missing (playwright install not run): try an installed Chrome / Edge.
            browser = None
            for channel in ("chrome", "msedge"):
                try:
                    browser = pw.chromium.launch(channel=channel)
                    print(f"note: bundled Chromium unavailable, using installed {channel}", file=sys.stderr)
                    break
                except PWError:
                    continue
            if browser is None:
                raise first
        try:
            for w in widths:
                ctx = browser.new_context(viewport={"width": w, "height": height}, device_scale_factor=1,
                                          reduced_motion="reduce" if reduced else "no-preference",
                                          color_scheme="dark" if dark else "light")
                page = ctx.new_page()
                errors = []
                page.on("console", lambda m, errors=errors: errors.append(f"console.{m.type}: {m.text}")
                        if m.type == "error" else None)
                page.on("pageerror", lambda e, errors=errors: errors.append(f"pageerror: {e}"))
                page.on("requestfailed", lambda r, errors=errors: errors.append(
                    f"requestfailed: {r.url} ({r.failure})"))
                res = {"width": w, "file": None, "errors": errors, "load_error": None}
                try:
                    page.goto(url, wait_until="load", timeout=timeout_ms)
                    try:
                        page.wait_for_load_state("networkidle", timeout=timeout_ms)
                    except PWError:
                        errors.append("warning: networkidle not reached before timeout")
                    page.evaluate("() => document.fonts.ready.then(() => true)")
                    page.evaluate(SCROLL_JS)
                    try:
                        page.wait_for_load_state("networkidle", timeout=timeout_ms)
                    except PWError:
                        pass
                    page.evaluate("() => document.fonts.ready.then(() => true)")
                    res.update(page.evaluate(OVERFLOW_JS))
                    path = os.path.join(out_dir, f"{name}-{w}.png")
                    page.screenshot(path=path, full_page=True)
                    res["file"] = path
                except PWError as e:
                    res["load_error"] = str(e).splitlines()[0]
                finally:
                    ctx.close()
                results.append(res)
        finally:
            browser.close()
    return results


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog=__doc__.split("\n", 1)[1],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("target", help="URL (http/https/file) or local HTML file")
    p.add_argument("--out", default="screenshots", help="output directory (default ./screenshots)")
    p.add_argument("--widths", type=parse_widths, default=DEFAULT_WIDTHS, help="comma list (default 375,768,1024,1440)")
    p.add_argument("--height", type=int, default=900, help="viewport height (default 900)")
    p.add_argument("--name", help="file name prefix (default derived from the target)")
    p.add_argument("--reduced-motion", action="store_true", help="emulate prefers-reduced-motion: reduce")
    p.add_argument("--dark", action="store_true", help="emulate prefers-color-scheme: dark")
    p.add_argument("--timeout", type=int, default=30, help="per-step timeout in seconds (default 30)")
    p.add_argument("--json", action="store_true", help="print the report as JSON")
    args = p.parse_args(argv)
    try:
        url = to_url(args.target)
    except FileNotFoundError as e:
        print(f"error: file not found: {e}", file=sys.stderr)
        return 2
    try:
        import playwright.sync_api  # noqa: F401
    except ImportError:
        print("error: Playwright for Python is not installed (pip install playwright && playwright install chromium)",
              file=sys.stderr)
        return 2
    os.makedirs(args.out, exist_ok=True)
    name = args.name or slug_for(url)
    try:
        results = shoot(url, args.widths, args.out, name, args.height, args.reduced_motion, args.dark,
                        args.timeout * 1000)
    except Exception as e:  # browser launch failure etc.
        print(f"error: {type(e).__name__}: {str(e).splitlines()[0] if str(e) else ''}", file=sys.stderr)
        return 1
    failed = False
    if args.json:
        print(json.dumps({"url": url, "reduced_motion": args.reduced_motion, "results": results}, indent=2))
    for r in results:
        real_errors = [e for e in r["errors"] if not e.startswith("warning:")]
        bad = bool(r["load_error"] or r.get("overflow") or real_errors)
        failed |= bad
        if args.json:
            continue
        if r["load_error"]:
            print(f"{r['width']:>5}px  LOAD FAILED: {r['load_error']}")
            continue
        status = "FAIL" if bad else "ok  "
        print(f"{r['width']:>5}px  {status} {r['file']}  (page height {r['height']}px)")
        if r.get("overflow"):
            print(f"         horizontal overflow: scrollWidth {r['scrollWidth']} > clientWidth {r['clientWidth']}")
            for o in r["offenders"]:
                print(f"           {o['selector']} spans {o['left']}..{o['right']}px")
        for e in r["errors"]:
            print(f"         {e}")
    if not args.json:
        print("result: " + ("issues found" if failed else "no overflow, no console errors"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
