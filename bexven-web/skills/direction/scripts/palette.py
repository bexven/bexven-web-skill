#!/usr/bin/env python3
"""palette.py - OKLCH colour scales, WCAG contrast and token pair checks (stdlib only).

Subcommands
  scale     Build a 12-step scale from an OKLCH hue + chroma (Radix-style roles:
            1-2 app/section backgrounds, 3-5 component backgrounds (normal /
            hover / active), 6-8 borders and separators, 9-10 solid fills
            (9 = the colour itself, 10 = its hover), 11-12 text (low / high
            contrast). Output is CSS custom properties with a hex fallback and
            an oklch() override inside @supports, or JSON / a table.
            Out-of-gamut colours are clamped to sRGB by reducing chroma
            (hue and lightness are kept).
  convert   Convert one colour between hex and oklch().
  contrast  WCAG 2.x contrast ratio between two colours with AA / AAA flags.
  check     Read a CSS file's :root custom properties and check pairs,
            e.g. --pair text:bg --pair brand-11:brand-2. var() references
            inside :root are resolved.

Colours may be written as #rgb, #rrggbb, #rrggbbaa (alpha ignored),
rgb(r g b) / rgb(r, g, b), or oklch(L C H) with L as 0-1 or a percentage.

Saturated violet (OKLCH hue 260-320 with chroma >= 0.08) is flagged with a
warning (Bexven rule C3: only when it is the client's existing brand colour or
the brief asks for it). Pass --allow-violet to silence it. Low-chroma plum /
aubergine is not flagged.

WCAG 2.2 AA is the pass/fail gate: 4.5:1 body text, 3:1 large text (>=24px
or >=18.66px bold) and UI components / focus indicators.

Exit codes: 0 ok, 1 failing pair(s) (check / contrast with --require),
2 usage error (bad colour, missing property, bad arguments).

Examples
  palette.py scale --hue 155 --chroma 0.09 --name pine
  palette.py scale --hue 75 --chroma 0.12 --lightness 0.62 --name brass --theme dark
  palette.py convert "oklch(0.55 0.09 155)"
  palette.py contrast "#1f2a24" "oklch(0.97 0.01 90)"
  palette.py check site.css --pair ink:paper --pair accent-11:paper --pair on-accent:accent-9 --large-pair heading:paper
"""
import argparse
import json
import math
import re
import sys


class UsageError(Exception):
    pass


# ---------------------------------------------------------------- conversions
def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def linear_to_srgb(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def linear_rgb_to_oklab(r, g, b):
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def oklab_to_linear_rgb(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)


def oklch_to_oklab(L, C, H):
    h = math.radians(H)
    return L, C * math.cos(h), C * math.sin(h)


def oklab_to_oklch(L, a, b):
    C = math.hypot(a, b)
    H = math.degrees(math.atan2(b, a)) % 360
    if C < 1e-4:
        H = 0.0
    return L, C, H


def oklch_to_linear(L, C, H):
    return oklab_to_linear_rgb(*oklch_to_oklab(L, C, H))


def in_gamut(rgb, eps=1e-6):
    return all(-eps <= v <= 1 + eps for v in rgb)


def clamp_chroma(L, C, H):
    """Return (L, C', H) with C' the largest chroma <= C that fits in sRGB."""
    L = min(max(L, 0.0), 1.0)
    if in_gamut(oklch_to_linear(L, C, H)):
        return L, C, H
    lo, hi = 0.0, C
    for _ in range(40):
        mid = (lo + hi) / 2
        if in_gamut(oklch_to_linear(L, mid, H)):
            lo = mid
        else:
            hi = mid
    return L, lo, H


def oklch_to_srgb(L, C, H):
    """OKLCH -> gamma-encoded sRGB floats 0..1 (gamut-clamped by chroma)."""
    L, C, H = clamp_chroma(L, C, H)
    lin = oklch_to_linear(L, C, H)
    return tuple(min(max(linear_to_srgb(min(max(v, 0.0), 1.0)), 0.0), 1.0) for v in lin)


def srgb_to_oklch(r, g, b):
    return oklab_to_oklch(*linear_rgb_to_oklab(srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b)))


def rgb_to_hex(rgb):
    return "#" + "".join(f"{round(v * 255):02x}" for v in rgb)


# ---------------------------------------------------------------- parsing
HEX_RE = re.compile(r"^#([0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
FUNC_RE = re.compile(r"^(oklch|rgba?)\(\s*([^)]*)\)$", re.I)


def _num(tok, pct_scale):
    tok = tok.strip()
    if tok.endswith("%"):
        return float(tok[:-1]) / 100 * pct_scale
    if tok.lower().endswith("deg"):
        return float(tok[:-3])
    if tok.lower() == "none":
        return 0.0
    return float(tok)


def parse_color(text):
    """Parse a colour string -> sRGB floats (0..1). Raises UsageError."""
    s = text.strip()
    m = HEX_RE.match(s)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        h = h[:6]
        return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    m = FUNC_RE.match(s)
    if m:
        kind, body = m.group(1).lower(), m.group(2)
        body = body.split("/")[0]
        parts = [p for p in re.split(r"[\s,]+", body.strip()) if p]
        if len(parts) < 3:
            raise UsageError(f"cannot parse colour {text!r}")
        try:
            if kind == "oklch":
                L = _num(parts[0], 1.0)
                C = _num(parts[1], 0.4)
                H = _num(parts[2], 360)
                if L > 1.0 and not parts[0].endswith("%"):
                    L = L / 100  # tolerate oklch(55 0.1 150)
                return oklch_to_srgb(L, C, H)
            vals = [_num(p, 255) for p in parts[:3]]
            return tuple(min(max(v / 255, 0), 1) for v in vals)
        except ValueError:
            raise UsageError(f"cannot parse colour {text!r}")
    raise UsageError(f"cannot parse colour {text!r} (use hex, rgb() or oklch())")


def fmt_oklch(L, C, H):
    return f"oklch({L * 100:.1f}% {C:.3f} {H:.1f})"


# ---------------------------------------------------------------- contrast
def rel_luminance(rgb):
    r, g, b = (srgb_to_linear(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(c1, c2):
    a, b = rel_luminance(c1), rel_luminance(c2)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def grade(ratio):
    return {
        "AA": ratio >= 4.5, "AAA": ratio >= 7.0,
        "AA_large": ratio >= 3.0, "AAA_large": ratio >= 4.5,
        "UI_3to1": ratio >= 3.0,
    }


def is_saturated_violet(L, C, H):
    return 260 <= H <= 320 and C >= 0.08


def violet_warning(label, rgb):
    L, C, H = srgb_to_oklch(*rgb)
    if is_saturated_violet(L, C, H):
        return (f"warning: {label} is saturated violet ({fmt_oklch(L, C, H)}): hue 260-320 with "
                "chroma >= 0.08 is a Bexven default-ban (C3). Use only if it is the client's existing "
                "brand colour or the brief asks for it; record brand-source in DESIGN.md. "
                "Silence with --allow-violet.")
    return None


# ---------------------------------------------------------------- scale
# (lightness, chroma multiplier) per step. Step 9 uses --lightness exactly.
LIGHT_STEPS = [(0.993, 0.06), (0.980, 0.12), (0.955, 0.22), (0.930, 0.32), (0.900, 0.42),
               (0.865, 0.52), (0.815, 0.64), (0.750, 0.80), (None, 1.00), (None, 1.00),
               (0.470, 0.85), (0.255, 0.55)]
DARK_STEPS = [(0.170, 0.10), (0.200, 0.16), (0.250, 0.30), (0.285, 0.40), (0.320, 0.48),
              (0.365, 0.56), (0.420, 0.66), (0.500, 0.82), (None, 1.00), (None, 1.00),
              (0.810, 0.80), (0.940, 0.30)]
ROLES = ["app background", "subtle background", "component bg", "component bg hover",
         "component bg active", "subtle border", "border", "strong border / focus",
         "solid", "solid hover", "low-contrast text", "high-contrast text"]


def build_scale(hue, chroma, lightness, theme):
    steps = LIGHT_STEPS if theme == "light" else DARK_STEPS
    out = []
    for i, (L, k) in enumerate(steps, start=1):
        if i == 9:
            L = lightness
        elif i == 10:
            L = lightness - 0.045 if theme == "light" else lightness + 0.045
        out.append(list(clamp_chroma(L, chroma * k, hue)))
    # Make step 11 reach 4.5:1 and step 12 reach 7:1 against step 2.
    bg = oklch_to_srgb(*out[1])
    for idx, target in ((10, 4.5), (11, 7.0)):
        for _ in range(60):
            if contrast_ratio(oklch_to_srgb(*out[idx]), bg) >= target:
                break
            L = out[idx][0] + (-0.01 if theme == "light" else 0.01)
            if not 0.0 <= L <= 1.0:
                break
            out[idx] = list(clamp_chroma(L, chroma * steps[idx][1], hue))
    return [tuple(s) for s in out]


def cmd_scale(args):
    if not 0 <= args.hue <= 360:
        raise UsageError("--hue must be 0-360")
    if not 0 <= args.chroma <= 0.4:
        raise UsageError("--chroma must be 0-0.4")
    lightness = args.lightness
    if lightness is None:
        lightness = 0.55 if args.theme == "light" else 0.62
    if not 0.05 <= lightness <= 0.95:
        raise UsageError("--lightness must be 0.05-0.95")
    scale = build_scale(args.hue, args.chroma, lightness, args.theme)
    rows = []
    for i, (L, C, H) in enumerate(scale, start=1):
        rgb = oklch_to_srgb(L, C, H)
        rows.append({"step": i, "role": ROLES[i - 1], "hex": rgb_to_hex(rgb),
                     "oklch": fmt_oklch(L, C, H), "L": round(L, 4), "C": round(C, 4), "H": round(H, 2),
                     "contrast_vs_step1": round(contrast_ratio(rgb, oklch_to_srgb(*scale[0])), 2)})
    if not args.allow_violet:
        w = violet_warning(f"scale {args.name} step 9", oklch_to_srgb(*scale[8]))
        if w:
            print(w, file=sys.stderr)
    clamped = args.chroma - scale[8][1]
    if clamped > 0.002:
        print(f"note: step 9 chroma clamped from {args.chroma:.3f} to {scale[8][1]:.3f} to fit sRGB",
              file=sys.stderr)
    n = args.name
    if args.format == "json":
        print(json.dumps({"name": n, "theme": args.theme, "hue": args.hue, "chroma": args.chroma,
                          "steps": rows}, indent=2))
    elif args.format == "table":
        print(f"{'step':>4}  {'hex':8} {'oklch':28} {'vs 1':>6}  role")
        for r in rows:
            print(f"{r['step']:>4}  {r['hex']:8} {r['oklch']:28} {r['contrast_vs_step1']:>6}  {r['role']}")
    else:
        sel = args.selector
        print(f"/* {n}: OKLCH hue {args.hue:g}, chroma {args.chroma:g}, theme {args.theme}."
              f" Generated by palette.py */")
        print(f"{sel} {{")
        for r in rows:
            print(f"  --{n}-{r['step']}: {r['hex']}; /* {r['role']} */")
        print("}")
        print("@supports (color: oklch(0% 0 0)) {")
        print(f"  {sel} {{")
        for r in rows:
            print(f"    --{n}-{r['step']}: {r['oklch']};")
        print("  }")
        print("}")
    return 0


def cmd_convert(args):
    rgb = parse_color(args.color)
    L, C, H = srgb_to_oklch(*rgb)
    print(f"hex:   {rgb_to_hex(rgb)}")
    print(f"oklch: {fmt_oklch(L, C, H)}")
    print(f"rgb:   rgb({round(rgb[0]*255)} {round(rgb[1]*255)} {round(rgb[2]*255)})")
    if not args.allow_violet:
        w = violet_warning(args.color, rgb)
        if w:
            print(w, file=sys.stderr)
    return 0


def cmd_contrast(args):
    a, b = parse_color(args.fg), parse_color(args.bg)
    r = contrast_ratio(a, b)
    g = grade(r)
    flag = lambda ok: "pass" if ok else "FAIL"
    print(f"{args.fg} on {args.bg}: {r:.2f}:1")
    print(f"  AA normal (4.5): {flag(g['AA'])}   AAA normal (7): {flag(g['AAA'])}")
    print(f"  AA large / UI (3): {flag(g['AA_large'])}   AAA large (4.5): {flag(g['AAA_large'])}")
    if not args.allow_violet:
        for lbl, c in ((args.fg, a), (args.bg, b)):
            w = violet_warning(lbl, c)
            if w:
                print(w, file=sys.stderr)
    if args.require:
        need = {"AA": 4.5, "AAA": 7.0, "AA-large": 3.0, "AAA-large": 4.5}[args.require]
        return 0 if r >= need else 1
    return 0


# ---------------------------------------------------------------- check
COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)


def root_properties(css):
    """Collect custom properties from every :root rule (including ones nested
    in @media/@supports). Later declarations win, except that an oklch value
    inside @supports and its hex fallback describe the same colour anyway."""
    css = COMMENT_RE.sub("", css)
    props = {}
    for m in re.finditer(r"(?<![\w-]):root\b[^{]*\{([^{}]*)\}", css):
        for decl in m.group(1).split(";"):
            if ":" not in decl:
                continue
            k, v = decl.split(":", 1)
            k = k.strip()
            if k.startswith("--"):
                props[k] = v.strip()
    return props


def resolve(props, name, depth=0):
    if depth > 20:
        raise UsageError(f"var() cycle at {name}")
    key = name if name.startswith("--") else "--" + name
    if key not in props:
        raise UsageError(f"custom property {key} not found in :root")
    val = props[key].replace("!important", "").strip()
    m = re.fullmatch(r"var\(\s*(--[\w-]+)\s*(?:,\s*(.+))?\)", val)
    if m:
        if m.group(1) in props:
            return resolve(props, m.group(1), depth + 1)
        if m.group(2):
            return m.group(2).strip()
    return val


def cmd_check(args):
    try:
        with open(args.css, encoding="utf-8") as fh:
            css = fh.read()
    except OSError as e:
        raise UsageError(str(e))
    props = root_properties(css)
    pairs = [(p, 4.5) for p in (args.pair or [])] + [(p, 3.0) for p in (args.large_pair or [])]
    if not pairs:
        raise UsageError("give at least one --pair fg:bg (or --large-pair)")
    failures = 0
    for spec, need in pairs:
        if ":" not in spec:
            raise UsageError(f"pair {spec!r} must look like fg:bg")
        fg, bg = (s.strip() for s in spec.split(":", 1))
        fv, bv = resolve(props, fg), resolve(props, bg)
        r = contrast_ratio(parse_color(fv), parse_color(bv))
        ok = r >= need
        failures += not ok
        lvl = "AAA" if r >= (7.0 if need == 4.5 else 4.5) else ("AA" if ok else "FAIL")
        print(f"{'ok  ' if ok else 'FAIL'} {fg} on {bg}: {r:.2f}:1 (need {need}:1) [{lvl}]  {fv} / {bv}")
    if not args.allow_violet:
        for k in props:
            try:
                rgb = parse_color(resolve(props, k))
            except UsageError:
                continue
            w = violet_warning(k, rgb)
            if w:
                print(w, file=sys.stderr)
    print(f"{len(pairs) - failures}/{len(pairs)} pairs pass")
    return 1 if failures else 0


def build_parser():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog=__doc__.split("\n", 1)[1],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--allow-violet", action="store_true", help="do not warn about saturated violet")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--allow-violet", action="store_true", default=argparse.SUPPRESS,
                        help="do not warn about saturated violet")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scale", parents=[common], help="12-step scale from hue + chroma")
    s.add_argument("--hue", type=float, required=True, help="OKLCH hue 0-360")
    s.add_argument("--chroma", type=float, required=True, help="peak OKLCH chroma (step 9), e.g. 0.09")
    s.add_argument("--lightness", type=float, help="OKLCH L of step 9 (default 0.55 light / 0.62 dark)")
    s.add_argument("--theme", choices=["light", "dark"], default="light")
    s.add_argument("--name", default="brand", help="custom property prefix (default brand)")
    s.add_argument("--selector", default=":root", help="CSS selector for the block (default :root)")
    s.add_argument("--format", choices=["css", "json", "table"], default="css")
    s.set_defaults(func=cmd_scale)

    c = sub.add_parser("convert", parents=[common], help="convert a colour between hex and oklch()")
    c.add_argument("color")
    c.set_defaults(func=cmd_convert)

    k = sub.add_parser("contrast", parents=[common], help="WCAG 2.x contrast ratio of two colours")
    k.add_argument("fg")
    k.add_argument("bg")
    k.add_argument("--require", choices=["AA", "AAA", "AA-large", "AAA-large"],
                   help="exit 1 unless this level passes")
    k.set_defaults(func=cmd_contrast)

    h = sub.add_parser("check", parents=[common], help="check custom-property pairs in a CSS file's :root")
    h.add_argument("css", help="CSS file")
    h.add_argument("--pair", action="append", help="fg:bg needing 4.5:1, names without the leading -- (repeatable)")
    h.add_argument("--large-pair", action="append", help="fg:bg needing 3:1 (large text / UI)")
    h.set_defaults(func=cmd_check)
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except UsageError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
