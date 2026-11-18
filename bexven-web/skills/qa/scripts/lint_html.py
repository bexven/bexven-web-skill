#!/usr/bin/env python3
"""lint_html.py - static lint of a built page for AI tells, a11y floor and local SEO.

Lints one HTML file plus its <style> blocks, style="" attributes and linked
LOCAL stylesheets (<link rel=stylesheet href="relative.css">; remote URLs are
never fetched). Uses only html.parser + regex.

Output: one line per finding
    file:line: [P0-P3] [rule-id] message
then a summary. Priorities: P0 broken, P1 must fix (a11y / legal / tell that
blocks shipping), P2 should fix (strong tell), P3 polish / needs a written reason.

Rules (id - priority - what)
  banned-hex            P1  Tailwind indigo/violet/purple/fuchsia 400-800 hexes (#6366f1, #7c3aed ...)
  violet-hue            P2  other saturated violet (OKLCH hue 260-320, chroma >= 0.08) - needs brand-source in DESIGN.md
  purple-gradient       P2  gradient from purple/violet to blue, cyan or pink
  section-gradient      P2  two-stop linear-gradient as a section/hero/body background (no image)
  stock-black           P2  stock #111 / #111111 / #0f0f0f / #fafafa
  transition-all        P2  transition: all
  keyframes-layout      P2  @keyframes animating width/height/top/left/margin/padding etc.
  outline-none          P1  outline: none / 0 with no :focus-visible rule anywhere
  img-alt               P1  <img> without alt (alt="" is fine for decorative images)
  img-size              P1  <img> without width and height attributes
  input-label           P1  form control without <label for> or wrapping <label> (placeholder-only included)
  input-label-aria      P2  form control named only by aria-label (no visible label)
  generic-cta           P2  button/link text such as "Submit", "Click here", "Read more", "Learn more", "Get started"
  eyebrow               P2  more than 2 eyebrow labels (short caps/tracked element right before h1-h3)
  middot                P3  "A · B · C" meta strings
  arrow-button          P3  arrow glyph in button/link text or button ::after content
  entrance-animation    P2  fade/entrance animation (data-aos, animate__, .reveal, .fade-up, Elementor _animation) on more than 2 sections
  raw-hex               P2  more than 12 raw hex values outside :root
  zoom-disabled         P1  viewport maximum-scale=1 or user-scalable=no
  html-lang             P1  missing <html lang>
  title                 P1  missing or empty <title>
  viewport              P1  missing meta viewport
  meta-description      P2  missing meta description
  heading-order         P2  heading level skipped (e.g. h2 -> h4)
  h1-count              P2  more than one h1, or none
  banned-copy           P2  banned copy words ("elevate", "seamless", "unleash", "Lorem ipsum" ...)
  emoji-icon            P3  emoji used as icons in headings / buttons / links
  overused-font         P3  overused font (Inter, Space Grotesk, Playfair, Fraunces ...) - needs a non-category reason in DESIGN.md
  google-fonts-cdn      P1  fonts.googleapis.com / fonts.gstatic.com (self-host fonts: GDPR)
  backdrop-filter       P3  backdrop-filter (glass) - needs a DESIGN.md justification
  library-effect        P3  component-library effects (marquee, bento, shimmer, aurora, spotlight, gradient text ...)
  stylesheet-missing    P3  linked local stylesheet not found
  local-tel             P1  (--local) no tel: link
  local-jsonld          P1  (--local) no LocalBusiness JSON-LD (@type ending in Business or a known subtype)
  jsonld-invalid        P1  (--local) a JSON-LD block does not parse

Suppress a finding with a comment on the same or the previous line:
    <!-- lint-ignore rule-id -->     /* lint-ignore rule-id other-rule */
("lint-ignore all" suppresses every rule on that line.) A suppression covers
findings reported at that line in that file.

Exit codes: 0 no P0/P1 findings, 1 at least one P0/P1 finding,
2 usage error (file missing, bad arguments).

Examples
  lint_html.py dist/index.html
  lint_html.py dist/index.html --local
  lint_html.py page.html --json > lint.json
"""
import argparse
import json
import math
import os
import re
import sys
from html.parser import HTMLParser

# ----------------------------------------------------------------- data
BANNED_HEX = {
    # indigo 400-800
    "#818cf8": "indigo-400", "#6366f1": "indigo-500", "#4f46e5": "indigo-600",
    "#4338ca": "indigo-700", "#3730a3": "indigo-800",
    # violet 400-800
    "#a78bfa": "violet-400", "#8b5cf6": "violet-500", "#7c3aed": "violet-600",
    "#6d28d9": "violet-700", "#5b21b6": "violet-800",
    # purple 400-800
    "#c084fc": "purple-400", "#a855f7": "purple-500", "#9333ea": "purple-600",
    "#7e22ce": "purple-700", "#6b21a8": "purple-800",
    # fuchsia 400-700
    "#e879f9": "fuchsia-400", "#d946ef": "fuchsia-500", "#c026d3": "fuchsia-600",
    "#a21caf": "fuchsia-700",
}
STOCK_BLACK = {"#111", "#111111", "#0f0f0f", "#fafafa"}
GENERIC_CTA = ["submit", "click here", "read more", "learn more", "get started", "find out more",
               "discover more", "more", "here", "send", "go"]
BANNED_COPY = [
    (r"\belevat(e|es|ed|ing)\b", "elevate"), (r"\bseamless(ly)?\b", "seamless"),
    (r"\bunleash(es|ed|ing)?\b", "unleash"), (r"\bcutting[- ]edge\b", "cutting-edge"),
    (r"\bworld[- ]class\b", "world-class"), (r"\bdelv(e|es|ed|ing)\b", "delve"),
    (r"\btapestry\b", "tapestry"), (r"\bin today['’]s fast[- ]paced\b", "in today's fast-paced"),
    (r"\bgame[- ]changer\b", "game-changer"), (r"\brobust\b", "robust"),
    (r"\bempower(s|ed|ing|ment)?\b", "empower"), (r"\blorem ipsum\b", "Lorem ipsum"),
    (r"\bunlock (your|the)\b", "unlock your/the"), (r"\brevolutioni[sz](e|es|ed|ing)\b", "revolutionize"),
    (r"\bstate[- ]of[- ]the[- ]art\b", "state-of-the-art"), (r"\bnext[- ]level\b", "next-level"),
    (r"\blook no further\b", "look no further"), (r"\bsynerg(y|ies)\b", "synergy"),
    (r"\bnestled\b", "nestled"), (r"\bstreamline[sd]?\b", "streamline"),
]
OVERUSED_FONTS = ["Inter", "Space Grotesk", "Playfair Display", "Playfair", "Fraunces", "DM Sans",
                  "DM Serif", "IBM Plex", "Poppins", "Montserrat", "Satoshi", "Clash Display",
                  "General Sans", "JetBrains Mono", "Roboto", "Open Sans", "Lato", "Raleway"]
LOCAL_BUSINESS_TYPES = {
    "localbusiness", "funeralhome", "funeralparlor", "plumber", "electrician", "hvacbusiness",
    "roofingcontractor", "generalcontractor", "homeandconstructionbusiness", "locksmith",
    "movingcompany", "housepainter", "dentist", "physician", "medicalbusiness", "medicalclinic",
    "legalservice", "attorney", "notary", "accountingservice", "financialservice",
    "autorepair", "autobodyshop", "automotivebusiness", "autodealer", "restaurant",
    "foodestablishment", "cafeorcoffeeshop", "bakery", "barorpub", "store", "hardwarestore",
    "realestateagent", "lodgingbusiness", "hotel", "beautysalon", "hairsalon", "dayspa",
    "healthandbeautybusiness", "veterinarycare", "childcare", "drycleaningorlaundry",
    "professionalservice", "emergencyservice", "sportsactivitylocation", "exercisegym",
    "insuranceagency", "travelagency", "employmentagency", "selfstorage", "recyclingcenter",
    "cemetery", "placeofworship", "manufacturer",
}
LAYOUT_PROPS = re.compile(r"^(width|height|min-width|min-height|max-width|max-height|top|left|right|bottom|"
                          r"inset(-\w+)?|margin(-\w+)?|padding(-\w+)?|font-size|border(-\w+)?-width|"
                          r"grid-template-\w+|flex-basis|line-height|letter-spacing)$")
ANIM_CLASS = re.compile(r"^(animate__\S*|reveal|reveal-\S+|js-reveal|scroll-reveal|fade-up|fade-in|fade-in-up|"
                        r"fadeinup|fade-down|fade-left|fade-right|slide-up|slide-in|aos-animate|aos-init|wow|"
                        r"elementor-invisible|animated|in-view|appear|sr-only-anim)$", re.I)
EFFECT_CLASS = re.compile(r"(marquee|bento|shimmer|border-beam|aurora|spotlight|lamp-effect|beams?-bg|"
                          r"number-ticker|particles|tilt-card|magnet(ic)?-btn|text-generate|gradient-text|"
                          r"glow-card|meteors?)", re.I)
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF☀-➿⭐⭕⬛⬜]")
ARROWS = re.compile("[→⟶➔➜➝➞➡↗⇒]|->")
HEX_RE = re.compile(r"(?<![\w&])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})(?![\w-])")
NAMED = {"purple": "#800080", "violet": "#ee82ee", "indigo": "#4b0082", "blue": "#0000ff",
         "pink": "#ffc0cb", "magenta": "#ff00ff", "fuchsia": "#ff00ff", "cyan": "#00ffff",
         "hotpink": "#ff69b4", "deeppink": "#ff1493", "blueviolet": "#8a2be2", "mediumpurple": "#9370db",
         "royalblue": "#4169e1", "dodgerblue": "#1e90ff", "deepskyblue": "#00bfff", "black": "#000000",
         "white": "#ffffff"}
SECTIONISH = re.compile(r"(^|[\s>+~,(])(section|header|footer|main|body|html|article)\b|hero|banner|masthead|"
                        r"jumbotron|section|splash|cover|band|e-con|elementor-(section|container)|"
                        r"(^|[\s.#_-])bg\b|background|wrapper|page", re.I)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source",
        "track", "wbr"}


# ----------------------------------------------------------------- colour helpers
def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h[:3])
    h = h[:6]
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rgb_to_oklch(rgb):
    r, g, b = (_lin(v) for v in rgb)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360


def parse_css_color(tok, props):
    """Best-effort colour token -> (L, C, H) or None. Resolves var(--x) from :root props."""
    tok = tok.strip()
    for _ in range(5):
        m = re.match(r"var\(\s*(--[\w-]+)\s*(?:,\s*(.*))?\)$", tok)
        if not m:
            break
        tok = props.get(m.group(1), m.group(2) or "").strip()
    low = tok.lower()
    if low in NAMED:
        tok = NAMED[low]
    if HEX_RE.fullmatch(tok):
        return rgb_to_oklch(hex_to_rgb(tok))
    m = re.match(r"rgba?\(([^)]*)\)", low)
    if m:
        parts = [p for p in re.split(r"[\s,/]+", m.group(1)) if p]
        try:
            vals = [float(p[:-1]) * 2.55 if p.endswith("%") else float(p) for p in parts[:3]]
            if len(parts) >= 4:
                alpha = float(parts[3][:-1]) / 100 if parts[3].endswith("%") else float(parts[3])
                if alpha < 0.35:
                    return None  # scrim / overlay - colour not dominant
            return rgb_to_oklch(tuple(min(max(v / 255, 0), 1) for v in vals))
        except ValueError:
            return None
    m = re.match(r"oklch\(([^)]*)\)", low)
    if m:
        parts = [p for p in re.split(r"[\s/]+", m.group(1)) if p]
        try:
            L = float(parts[0][:-1]) / 100 if parts[0].endswith("%") else float(parts[0])
            return L, float(parts[1]), float(parts[2].replace("deg", ""))
        except (ValueError, IndexError):
            return None
    m = re.match(r"hsla?\(([^)]*)\)", low)
    if m:
        parts = [p for p in re.split(r"[\s,/]+", m.group(1)) if p]
        try:
            import colorsys
            h = float(parts[0].replace("deg", "")) / 360
            s = float(parts[1].rstrip("%")) / 100
            li = float(parts[2].rstrip("%")) / 100
            return rgb_to_oklch(colorsys.hls_to_rgb(h, li, s))
        except (ValueError, IndexError):
            return None
    return None


def hue_family(lch):
    if lch is None:
        return None
    L, C, H = lch
    if C < 0.06:
        return "neutral"
    if 270 <= H <= 330:
        return "violet"
    if 220 <= H < 270:
        return "blue"
    if 180 <= H < 220:
        return "cyan"
    if H > 330 or H < 15:
        return "pink"
    return "other"


def split_top(s, sep=","):
    out, depth, cur = [], 0, []
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == sep and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    out.append("".join(cur))
    return [o.strip() for o in out]


def find_gradients(value):
    """Yield (kind, inner_args) for each *-gradient(...) in a CSS value."""
    for m in re.finditer(r"(repeating-)?(linear|radial|conic)-gradient\(", value, re.I):
        start, depth, i = m.end(), 1, m.end()
        while i < len(value) and depth:
            if value[i] == "(":
                depth += 1
            elif value[i] == ")":
                depth -= 1
            i += 1
        yield m.group(2).lower(), value[start:i - 1]


def gradient_stops(kind, inner):
    parts = split_top(inner)
    if parts and re.match(r"^(to\s|-?[\d.]+(deg|turn|rad|grad)|from\s|at\s|circle|ellipse|closest|farthest)",
                          parts[0], re.I):
        parts = parts[1:]
    stops = []
    for p in parts:
        p = p.strip()
        if not p or re.fullmatch(r"-?[\d.]+(%|px|em|rem)?", p):
            continue  # colour hint
        # strip trailing positions
        colour = re.sub(r"(\s+-?[\d.]+(%|px|em|rem|vh|vw)?)+$", "", p).strip()
        stops.append(colour)
    return stops


# ----------------------------------------------------------------- DOM
class Node:
    __slots__ = ("tag", "attrs", "line", "children", "parent", "texts")

    def __init__(self, tag, attrs, line, parent):
        self.tag, self.attrs, self.line, self.parent = tag, attrs, line, parent
        self.children, self.texts = [], []  # children: Node or (text, line)

    def classes(self):
        return (self.attrs.get("class") or "").split()

    def text(self):
        out = []
        for c in self.children:
            if isinstance(c, Node):
                if c.tag not in ("script", "style", "template"):
                    out.append(c.text())
            else:
                out.append(c[0])
        return " ".join(" ".join(out).split())

    def iter(self):
        yield self
        for c in self.children:
            if isinstance(c, Node):
                yield from c.iter()

    def ancestors(self):
        p = self.parent
        while p is not None:
            yield p
            p = p.parent

    def element_children(self):
        return [c for c in self.children if isinstance(c, Node)]


class Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {}, 1, None)
        self.stack = [self.root]
        self.comments = []  # (text, line)
        self.raw_blocks = []  # (tag, attrs, text, line)

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        node = Node(tag, {k: (v if v is not None else "") for k, v in attrs}, line, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        line = self.getpos()[0]
        node = Node(tag, {k: (v if v is not None else "") for k, v in attrs}, line, self.stack[-1])
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        line = self.getpos()[0]
        cur = self.stack[-1]
        if cur.tag in ("style", "script"):
            self.raw_blocks.append((cur.tag, cur.attrs, data, line))
        lead = data[:len(data) - len(data.lstrip())]
        if data.strip():
            cur.children.append((data, line + lead.count("\n")))

    def handle_comment(self, data):
        self.comments.append((data, self.getpos()[0]))


# ----------------------------------------------------------------- CSS parsing
def register_ignore(ignores, fname, line, end_line, standalone, ids):
    """A comment sharing its line with code covers that line only; a comment on
    its own line(s) covers its line(s) and the next line."""
    lines = range(line, end_line + 2) if standalone else [line]
    for rid in re.split(r"[\s,]+", ids.strip()):
        if rid:
            for ln in lines:
                ignores.setdefault(fname, {}).setdefault(ln, set()).add(rid)


def strip_css_comments(css, ignores, fname, base_line):
    """Remove comments keeping newlines; record lint-ignore comments."""
    def rep(m):
        txt = m.group(0)
        mm = re.search(r"lint-ignore\s+([\w\s,-]+)", txt)
        if mm:
            line = base_line + css.count("\n", 0, m.start())
            line_start = css.rfind("\n", 0, m.start()) + 1
            standalone = not css[line_start:m.start()].strip()
            end_line = line + txt.count("\n")
            register_ignore(ignores, fname, line, end_line, standalone, mm.group(1))
        return re.sub(r"[^\n]", " ", txt)
    return re.sub(r"/\*.*?\*/", rep, css, flags=re.S)


def iter_rules(css):
    """Yield (selector, body, body_offset, context) for each style rule.
    context is a tuple of enclosing at-rule preludes (e.g. '@keyframes fade')."""
    def walk(text, offset, ctx):
        i, n, start = 0, len(text), 0
        while i < n:
            ch = text[i]
            if ch == "{":
                prelude = text[start:i].strip()
                depth, j = 1, i + 1
                while j < n and depth:
                    if text[j] == "{":
                        depth += 1
                    elif text[j] == "}":
                        depth -= 1
                    j += 1
                body = text[i + 1:j - 1]
                if prelude.startswith("@") and not prelude.lower().startswith(("@font-face", "@page")):
                    yield from walk(body, offset + i + 1, ctx + (prelude,))
                else:
                    yield prelude, body, offset + i + 1, ctx
                i = j
                start = j
                continue
            if ch == ";" or ch == "}":
                start = i + 1
            i += 1
    yield from walk(css, 0, ())


def iter_decls(body):
    """Yield (prop, value, offset_in_body) for declarations in a rule body."""
    for seg, seg_off in split_decls(body):
        if ":" in seg:
            k, v = seg.split(":", 1)
            lead = len(seg) - len(seg.lstrip())
            yield k.strip().lower(), v.strip(), seg_off + lead


def split_decls(body):
    out, depth, cur_start, q = [], 0, 0, None
    for i, ch in enumerate(body):
        if q:
            if ch == q:
                q = None
            continue
        if ch in "\"'":
            q = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == ";" and depth == 0:
            out.append((body[cur_start:i], cur_start))
            cur_start = i + 1
    if body[cur_start:].strip():
        out.append((body[cur_start:], cur_start))
    return out


# ----------------------------------------------------------------- linter
class Linter:
    def __init__(self, html_path, local=False):
        self.html_path = html_path
        self.local = local
        self.findings = []  # (file, line, prio, rule, msg)
        self.ignores = {}   # file -> line -> set(rule)
        self.css_units = []  # dicts: file, base_line, css (comment-stripped), kind, selector_hint
        self.root_props = {}
        self.uppercase_classes = set()

    def add(self, f, line, prio, rule, msg):
        self.findings.append((f, line, prio, rule, msg))

    # ---------- loading
    def load(self):
        with open(self.html_path, encoding="utf-8", errors="replace") as fh:
            self.html = fh.read()
        b = Builder()
        b.feed(self.html)
        b.close()
        self.dom = b.root
        self.rel = os.path.relpath(self.html_path) if not os.path.isabs(self.html_path) else self.html_path
        src_lines = self.html.splitlines()
        for text, line in b.comments:
            mm = re.search(r"lint-ignore\s+([\w\s,-]+)", text)
            if mm:
                src = src_lines[line - 1] if line - 1 < len(src_lines) else ""
                standalone = not src[:src.find("<!--")].strip() if "<!--" in src else True
                register_ignore(self.ignores, self.rel, line, line + text.count("\n"), standalone, mm.group(1))
        # <style> blocks
        for tag, attrs, text, line in b.raw_blocks:
            if tag == "style":
                self.css_units.append({"file": self.rel, "base": line, "kind": "style",
                                       "css": strip_css_comments(text, self.ignores, self.rel, line)})
        self.jsonld = [(text, line) for tag, attrs, text, line in b.raw_blocks
                       if tag == "script" and (attrs.get("type") or "").lower() == "application/ld+json"]
        # linked local stylesheets
        base_dir = os.path.dirname(os.path.abspath(self.html_path))
        for n in self.dom.iter():
            if n.tag == "link" and "stylesheet" in (n.attrs.get("rel") or "").lower():
                href = (n.attrs.get("href") or "").strip()
                if not href or re.match(r"^(https?:)?//", href) or href.startswith("data:"):
                    continue
                path = href.split("?")[0].split("#")[0]
                full = os.path.normpath(os.path.join(base_dir, path.lstrip("/")) if not path.startswith("/")
                                        else os.path.join(base_dir, path.lstrip("/")))
                if not os.path.exists(full):
                    self.add(self.rel, n.line, "P3", "stylesheet-missing", f"linked stylesheet {href!r} not found")
                    continue
                with open(full, encoding="utf-8", errors="replace") as fh:
                    css = fh.read()
                rel = os.path.relpath(full)
                self.css_units.append({"file": rel, "base": 1, "kind": "file",
                                       "css": strip_css_comments(css, self.ignores, rel, 1)})
        # inline style attributes
        for n in self.dom.iter():
            st = n.attrs.get("style")
            if st:
                self.css_units.append({"file": self.rel, "base": n.line, "kind": "inline", "node": n,
                                       "css": st})
        # :root props + uppercase classes
        for u in self.css_units:
            if u["kind"] == "inline":
                continue
            for sel, body, off, ctx in iter_rules(u["css"]):
                if any(c.lower().startswith("@keyframes") for c in ctx):
                    continue
                decls = list(iter_decls(body))
                if re.search(r"(^|,)\s*(:root|html)\s*(,|$)", sel):
                    for k, v, _ in decls:
                        if k.startswith("--"):
                            self.root_props[k] = v
                if any((k == "text-transform" and "uppercase" in v.lower()) or
                       (k == "letter-spacing" and not re.match(r"^(0|normal|-)", v.strip()))
                       or (k == "font-variant" and "small-caps" in v) for k, v, _ in decls):
                    for cls in re.findall(r"\.([\w-]+)", sel):
                        self.uppercase_classes.add(cls)

    def line_in(self, unit, offset):
        if unit["kind"] == "inline":
            return unit["base"]
        return unit["base"] + unit["css"].count("\n", 0, offset)

    # ---------- CSS rules
    def lint_css(self):
        has_focus_visible = any(":focus-visible" in u["css"] for u in self.css_units)
        raw_hex = []  # (file, line, hex)
        for u in self.css_units:
            f = u["file"]
            if u["kind"] == "inline":
                n = u["node"]
                hint = n.tag + " " + " ".join("." + c for c in n.classes()) + " #" + n.attrs.get("id", "")
                rules = [(hint, u["css"], 0, ())]
            else:
                rules = list(iter_rules(u["css"]))
            for sel, body, off, ctx in rules:
                in_kf = any(c.lower().startswith("@keyframes") for c in ctx)
                is_root = bool(re.search(r"(^|,)\s*:root\s*(,|$)", sel))
                bg_has_image = bool(re.search(r"background(-image)?\s*:[^;]*url\(", body, re.I))
                for prop, val, doff in iter_decls(body):
                    line = self.line_in(u, off + doff)
                    low = val.lower()
                    for hx in HEX_RE.findall(val):
                        h = hx.lower()
                        if h in BANNED_HEX:
                            self.add(f, line, "P1", "banned-hex",
                                     f"{hx} is Tailwind {BANNED_HEX[h]} (stock AI violet/indigo); use the client palette")
                        elif h in STOCK_BLACK:
                            self.add(f, line, "P2", "stock-black",
                                     f"stock {hx}; derive ink/paper from the palette (OKLCH, tinted)")
                        else:
                            lch = rgb_to_oklch(hex_to_rgb(h))
                            if 260 <= lch[2] <= 320 and lch[1] >= 0.08:
                                self.add(f, line, "P2", "violet-hue",
                                         f"{hx} is saturated violet; allowed only with brand-source in DESIGN.md")
                        if not is_root:
                            raw_hex.append((f, line, hx))
                    if re.match(r"transition(-property)?$", prop) and re.search(r"(^|[\s,])all\b", low):
                        self.add(f, line, "P2", "transition-all", "transition: all; list the properties (transform, opacity, colour)")
                    if in_kf and not prop.startswith("--") and LAYOUT_PROPS.match(prop):
                        kf = next(c for c in ctx if c.lower().startswith("@keyframes"))
                        self.add(f, line, "P2", "keyframes-layout",
                                 f"{kf.split()[1] if len(kf.split()) > 1 else '@keyframes'} animates {prop}; animate transform/opacity only")
                    if prop in ("outline", "outline-style", "outline-width") and re.match(r"^(none|0(px)?)\b", low) \
                            and not has_focus_visible:
                        self.add(f, line, "P1", "outline-none",
                                 "outline removed and no :focus-visible rule anywhere; add a visible focus style")
                    if prop in ("backdrop-filter", "-webkit-backdrop-filter") and low not in ("none",):
                        self.add(f, line, "P3", "backdrop-filter", "backdrop-filter (glass); needs a DESIGN.md justification")
                    if prop in ("background-clip", "-webkit-background-clip") and "text" in low:
                        self.add(f, line, "P3", "library-effect", "gradient/clip text effect")
                    if prop == "content" and ARROWS.search(val) and re.search(r"btn|button|cta|link|more", sel, re.I):
                        self.add(f, line, "P3", "arrow-button", f"arrow glyph in {sel.strip()[:40]} content")
                    if prop in ("font-family", "font") or prop.startswith("--font"):
                        self.check_fonts(f, line, val)
                    for kind, inner in find_gradients(val):
                        stops = gradient_stops(kind, inner)
                        fams = [hue_family(parse_css_color(s, self.root_props)) for s in stops]
                        if "violet" in fams and any(x in ("blue", "cyan", "pink") for x in fams):
                            self.add(f, line, "P2", "purple-gradient",
                                     "purple/violet to blue/cyan/pink gradient (stock AI look)")
                        elif kind == "linear" and len(stops) == 2 and prop.startswith("background") \
                                and not bg_has_image and SECTIONISH.search(sel or "") \
                                and stops[0].replace(" ", "") != stops[1].replace(" ", ""):
                            self.add(f, line, "P2", "section-gradient",
                                     f"two-stop linear-gradient on {sel.strip()[:40] or 'section'} background; flat by default or justify in DESIGN.md")
                if not in_kf and EFFECT_CLASS.search(sel or "") and u["kind"] != "inline":
                    self.add(f, self.line_in(u, off), "P3", "library-effect",
                             f"component-library effect selector {sel.strip()[:50]!r}")
            # @import of Google Fonts and keyframe names
            if u["kind"] != "inline":
                for m in re.finditer(r"@import[^;]*fonts\.(googleapis|gstatic)\.com[^;]*;?", u["css"]):
                    self.add(f, self.line_in(u, m.start()), "P1", "google-fonts-cdn",
                             "Google Fonts @import; self-host the font files (GDPR)")
                for m in re.finditer(r"@keyframes\s+([\w-]+)", u["css"]):
                    if EFFECT_CLASS.search(m.group(1)):
                        self.add(f, self.line_in(u, m.start()), "P3", "library-effect",
                                 f"@keyframes {m.group(1)} looks like a component-library effect")
        # SVG/presentation attributes count as raw hex too
        for n in self.dom.iter():
            for a in ("fill", "stroke", "stop-color", "color", "bgcolor"):
                v = n.attrs.get(a) or ""
                for hx in HEX_RE.findall(v):
                    raw_hex.append((self.rel, n.line, hx))
                    if hx.lower() in BANNED_HEX:
                        self.add(self.rel, n.line, "P1", "banned-hex", f"{hx} is Tailwind {BANNED_HEX[hx.lower()]}")
        if len(raw_hex) > 12:
            f, line, hx = raw_hex[12]
            self.add(f, line, "P2", "raw-hex",
                     f"{len(raw_hex)} raw hex values outside :root (limit 12); use role tokens (var(--color-*))")

    def check_fonts(self, f, line, val):
        seen = set()
        for font in OVERUSED_FONTS:
            pat = r"(?<![\w-])" + re.escape(font) + (r"(?![\w-])" if font != "IBM Plex" else "")
            if font == "Inter":
                pat = r"(?<![\w-])Inter(?!\s*Tight)(?![\w-])"
            if font == "Playfair" and "Playfair Display" in seen:
                continue
            if re.search(pat, val, re.I if font != "Inter" else 0):
                seen.add(font)
                self.add(f, line, "P3", "overused-font",
                         f"{font} is an overused default; needs a non-category reason in DESIGN.md")

    # ---------- HTML rules
    def lint_html(self):
        f = self.rel
        nodes = list(self.dom.iter())
        html = next((n for n in nodes if n.tag == "html"), None)
        if html is None or not (html.attrs.get("lang") or "").strip():
            self.add(f, html.line if html else 1, "P1", "html-lang", "missing <html lang>")
        title = next((n for n in nodes if n.tag == "title"), None)
        if title is None or not title.text().strip():
            self.add(f, title.line if title else 1, "P1", "title", "missing or empty <title>")
        metas = [n for n in nodes if n.tag == "meta"]
        vp = next((m for m in metas if (m.attrs.get("name") or "").lower() == "viewport"), None)
        if vp is None:
            self.add(f, 1, "P1", "viewport", "missing <meta name=viewport>")
        else:
            c = (vp.attrs.get("content") or "").lower()
            if re.search(r"maximum-scale\s*=\s*1(\.0*)?(?![\d.])", c) or re.search(r"user-scalable\s*=\s*(no|0)", c):
                self.add(f, vp.line, "P1", "zoom-disabled", "viewport blocks zoom (maximum-scale=1 / user-scalable=no)")
        desc = next((m for m in metas if (m.attrs.get("name") or "").lower() == "description"), None)
        if desc is None or not (desc.attrs.get("content") or "").strip():
            self.add(f, desc.line if desc else 1, "P2", "meta-description", "missing meta description")

        # Google Fonts links + font families in URL
        for n in nodes:
            if n.tag == "link":
                href = n.attrs.get("href") or ""
                if re.search(r"fonts\.(googleapis|gstatic)\.com", href):
                    self.add(f, n.line, "P1", "google-fonts-cdn", "Google Fonts CDN link; self-host the font files (GDPR)")
                    fams = re.findall(r"family=([^&:]+)", href)
                    if fams:
                        self.check_fonts(f, n.line, ", ".join(x.replace("+", " ") for x in fams))

        # images
        for n in nodes:
            if n.tag == "img":
                if "alt" not in n.attrs:
                    self.add(f, n.line, "P1", "img-alt", f"<img src={n.attrs.get('src', '')!r}> has no alt (use alt=\"\" if decorative)")
                if not n.attrs.get("width") or not n.attrs.get("height"):
                    self.add(f, n.line, "P1", "img-size", f"<img src={n.attrs.get('src', '')!r}> lacks width/height (layout shift)")

        # form controls
        labels_for = {n.attrs.get("for") for n in nodes if n.tag == "label" and n.attrs.get("for")}
        for n in nodes:
            if n.tag not in ("input", "select", "textarea"):
                continue
            typ = (n.attrs.get("type") or "text").lower()
            if n.tag == "input" and typ in ("hidden", "submit", "button", "reset", "image"):
                continue
            nid = n.attrs.get("id")
            labelled = (nid and nid in labels_for) or any(a.tag == "label" for a in n.ancestors()) \
                or n.attrs.get("aria-labelledby")
            name = n.attrs.get("name") or nid or typ
            if not labelled:
                if n.attrs.get("aria-label"):
                    self.add(f, n.line, "P2", "input-label-aria", f"{n.tag} {name!r} has only aria-label; add a visible <label>")
                elif n.attrs.get("placeholder"):
                    self.add(f, n.line, "P1", "input-label", f"{n.tag} {name!r} is placeholder-only; add a <label for>")
                else:
                    self.add(f, n.line, "P1", "input-label", f"{n.tag} {name!r} has no associated <label>")

        # buttons / links: generic text, arrows, emoji
        def is_buttonish(n):
            if n.tag == "button":
                return True
            if n.tag == "input" and (n.attrs.get("type") or "").lower() in ("submit", "button"):
                return True
            return n.tag == "a"
        for n in nodes:
            if not is_buttonish(n):
                continue
            txt = n.attrs.get("value", "") if n.tag == "input" else n.text()
            clean = re.sub(r"[^\w\s']", "", ARROWS.sub("", txt)).strip().lower()
            clean = " ".join(clean.split())
            if clean in GENERIC_CTA:
                self.add(f, n.line, "P2", "generic-cta", f"generic {n.tag} text {txt.strip()!r}; say verb + object")
            if ARROWS.search(txt):
                self.add(f, n.line, "P3", "arrow-button", f"arrow glyph in {n.tag} text {txt.strip()[:40]!r}")
            if EMOJI_RE.search(txt):
                self.add(f, n.line, "P3", "emoji-icon", f"emoji in {n.tag} {txt.strip()[:40]!r}; use an inline SVG icon")

        # headings
        heads = [n for n in nodes if re.fullmatch(r"h[1-6]", n.tag)]
        h1s = [h for h in heads if h.tag == "h1"]
        if len(h1s) > 1:
            for h in h1s[1:]:
                self.add(f, h.line, "P2", "h1-count", f"extra h1 ({len(h1s)} on the page); keep one")
        elif not h1s:
            self.add(f, heads[0].line if heads else 1, "P2", "h1-count", "no h1 on the page")
        prev = 0
        for h in heads:
            lvl = int(h.tag[1])
            if prev and lvl > prev + 1:
                self.add(f, h.line, "P2", "heading-order", f"heading jumps from h{prev} to h{lvl}")
            prev = lvl
            if EMOJI_RE.search(h.text()):
                self.add(f, h.line, "P3", "emoji-icon", f"emoji in {h.tag} {h.text()[:40]!r}; use an inline SVG icon")

        # eyebrows
        eyebrows = []
        for h in heads:
            if h.tag not in ("h1", "h2", "h3") or h.parent is None:
                continue
            sibs = h.parent.element_children()
            idx = sibs.index(h)
            cand = None
            if idx > 0:
                cand = sibs[idx - 1]
            elif h.parent.parent is not None and h.parent.tag in ("div",) and len(sibs) == 1:
                # Elementor-style: heading alone in a widget wrapper; look at the wrapper's previous sibling
                ps = h.parent.parent.element_children()
                j = ps.index(h.parent)
                cand = ps[j - 1] if j > 0 else None
            if cand is None or re.fullmatch(r"h[1-6]|img|picture|svg|ul|ol|form|nav|figure|button|a|input", cand.tag):
                continue
            txt = cand.text()
            if not txt or len(txt) > 40 or len(txt.split()) > 6:
                continue
            if self.looks_eyebrow(cand, txt):
                eyebrows.append((cand, txt))
        if len(eyebrows) > 2:
            for i, (n, txt) in enumerate(eyebrows, 1):
                self.add(f, n.line, "P2", "eyebrow",
                         f"eyebrow {i} of {len(eyebrows)} ({txt[:30]!r}); max 2 per page and only if it carries information")

        # text-node checks: middot, banned copy
        for n in nodes:
            if n.tag in ("script", "style", "template"):
                continue
            for c in n.children:
                if isinstance(c, Node):
                    continue
                txt, line = c
                if len(re.findall(r"\s[·•]\s", " " + txt + " ")) >= 2:
                    self.add(f, line, "P3", "middot", f"middot meta string {' '.join(txt.split())[:50]!r}")
                self.check_copy(f, line, txt)
        for n in nodes:
            for a in ("alt", "title", "placeholder", "aria-label"):
                if n.attrs.get(a):
                    self.check_copy(f, n.line, n.attrs[a])
            if n.tag == "meta" and (n.attrs.get("name") or n.attrs.get("property") or "").lower() in (
                    "description", "og:description", "og:title", "twitter:description"):
                self.check_copy(f, n.line, n.attrs.get("content") or "")
            if EFFECT_CLASS.search(n.attrs.get("class") or "") and n.tag not in ("html", "body"):
                self.add(f, n.line, "P3", "library-effect",
                         f"component-library effect class on <{n.tag} class={n.attrs.get('class')[:40]!r}>")

        # entrance animations on sections
        def animated(n):
            if any(k in n.attrs for k in ("data-aos", "data-animate", "data-sal", "data-scroll-reveal",
                                          "data-animation", "data-reveal")):
                return True
            if any(ANIM_CLASS.match(c) for c in n.classes()):
                return True
            ds = n.attrs.get("data-settings") or ""
            if re.search(r'"_?animation"\s*:\s*"(?!none")[^"]+"', ds):
                return True
            return False
        sections = []
        for n in nodes:
            if not animated(n):
                continue
            sec = n
            for a in [n] + list(n.ancestors()):
                if a.tag in ("section", "header", "footer", "article", "aside") or \
                        any(c in ("elementor-section", "e-con", "elementor-top-section") for c in a.classes()):
                    sec = a
                    if a.tag in ("section", "header", "footer") or "elementor-top-section" in a.classes():
                        break
            if sec not in sections:
                sections.append(sec)
        if len(sections) > 2:
            for i, s in enumerate(sections, 1):
                self.add(f, s.line, "P2", "entrance-animation",
                         f"entrance/fade animation in section {i} of {len(sections)}; max one motion moment per page, no section reveals")

        # local business
        if self.local:
            if not any(n.tag == "a" and (n.attrs.get("href") or "").lower().startswith("tel:") for n in nodes):
                self.add(f, 1, "P1", "local-tel", "no tel: link; add a tappable phone number")
            found = False
            for text, line in self.jsonld:
                try:
                    data = json.loads(text)
                except json.JSONDecodeError as e:
                    self.add(f, line, "P1", "jsonld-invalid", f"JSON-LD does not parse: {e.msg} (line {e.lineno})")
                    continue
                if self.has_local_type(data):
                    found = True
            if not found:
                self.add(f, 1, "P1", "local-jsonld",
                         "no LocalBusiness JSON-LD (@type ending in Business or a subtype such as FuneralHome/Plumber)")

    def looks_eyebrow(self, n, txt):
        letters = re.sub(r"[^A-Za-z]", "", txt)
        if len(letters) >= 3 and letters.isupper():
            return True
        for x in [n] + list(n.iter()):
            cls = x.classes()
            if any(re.search(r"eyebrow|kicker|overline|pretitle|pre-title|supertitle|tagline|section-label|"
                             r"subheading-top|label", c, re.I) for c in cls):
                return True
            if any(c in self.uppercase_classes for c in cls):
                return True
            st = (x.attrs.get("style") or "").lower()
            if "uppercase" in st or re.search(r"letter-spacing\s*:\s*(?!0|normal|-)", st):
                return True
        return False

    def check_copy(self, f, line, txt):
        for pat, word in BANNED_COPY:
            if re.search(pat, txt, re.I):
                self.add(f, line, "P2", "banned-copy",
                         f"banned copy word {word!r} in {' '.join(txt.split())[:50]!r}; say the specific thing")

    def has_local_type(self, data):
        stack = [data]
        while stack:
            d = stack.pop()
            if isinstance(d, list):
                stack.extend(d)
            elif isinstance(d, dict):
                t = d.get("@type")
                types = t if isinstance(t, list) else [t]
                for ty in types:
                    if isinstance(ty, str):
                        tl = ty.split("/")[-1].split(":")[-1].lower()
                        if tl.endswith("business") or tl in LOCAL_BUSINESS_TYPES or tl.endswith("store") \
                                or tl.endswith("contractor"):
                            return True
                stack.extend(v for v in d.values() if isinstance(v, (dict, list)))
        return False

    # ---------- run
    def run(self):
        self.load()
        self.lint_css()
        self.lint_html()
        out, seen = [], set()
        for fnd in self.findings:
            f, line, prio, rule, msg = fnd
            ign = self.ignores.get(f, {})
            ids = ign.get(line, set())
            if rule in ids or "all" in ids:
                continue
            key = (f, line, rule, msg)
            if key in seen:
                continue
            seen.add(key)
            out.append(fnd)
        out.sort(key=lambda x: (x[0] != self.rel, x[0], x[1], x[2]))
        return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog=__doc__.split("\n", 1)[1],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("html", help="HTML file to lint")
    p.add_argument("--local", action="store_true",
                   help="local-business page: require a tel: link and LocalBusiness JSON-LD")
    p.add_argument("--json", action="store_true", help="print findings as JSON")
    p.add_argument("--min", choices=["P0", "P1", "P2", "P3"], default="P3",
                   help="only print findings at or above this priority (default P3 = all)")
    args = p.parse_args(argv)
    if not os.path.isfile(args.html):
        print(f"error: {args.html} not found", file=sys.stderr)
        return 2
    lint = Linter(args.html, local=args.local)
    try:
        findings = lint.run()
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    order = ["P0", "P1", "P2", "P3"]
    shown = [x for x in findings if order.index(x[2]) <= order.index(args.min)]
    counts = {k: sum(1 for x in findings if x[2] == k) for k in order}
    if args.json:
        print(json.dumps({"findings": [dict(zip(("file", "line", "priority", "rule", "message"), x)) for x in shown],
                          "counts": counts}, indent=2, ensure_ascii=False))
    else:
        for f, line, prio, rule, msg in shown:
            print(f"{f}:{line}: [{prio}] [{rule}] {msg}")
        print(f"\nsummary: {counts['P0']} P0, {counts['P1']} P1, {counts['P2']} P2, {counts['P3']} P3"
              f" ({len(findings)} findings in {lint.rel}"
              f" + {sum(1 for u in lint.css_units if u['kind'] == 'file')} linked stylesheet(s))")
    return 1 if counts["P0"] or counts["P1"] else 0


if __name__ == "__main__":
    sys.exit(main())
