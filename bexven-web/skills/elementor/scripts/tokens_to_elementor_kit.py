#!/usr/bin/env python3
"""tokens_to_elementor_kit.py - DESIGN.md YAML front matter -> Elementor site-kit settings JSON.

Reads the YAML front matter of a DESIGN.md (Google DESIGN.md shape: colors,
typography, rounded, spacing, motion; "{colors.primary}" references are
resolved) and prints a JSON object with:

  settings.system_colors / custom_colors
      [{"_id", "title", "color": "#RRGGBB"}]  - oklch()/rgb() converted to hex
      (gamut-clamped by reducing chroma). System ids primary / secondary /
      text / accent are filled from DESIGN.md keys of the same meaning
      (e.g. ink/text -> text, accent/tertiary -> accent); every other colour
      becomes a custom colour with a stable 7-char id.
  settings.system_typography / custom_typography
      [{"_id", "title", "typography_typography": "custom",
        "typography_font_family", "typography_font_size": {"unit","size","sizes"},
        "typography_font_weight", "typography_line_height": {...},
        "typography_letter_spacing": {...}}]
      System primary = display/headline role, secondary = second heading
      role, text = body role, accent = label/button role.
  variables
      Elementor V4 Variables: [{"name", "type": "color"|"font"|"size", "value"}]
      for every colour, font family, font size, radius and spacing token.
  fonts_to_self_host
      Families to upload as Custom Fonts (never load from the Google CDN).

IMPORTANT: Elementor's kit JSON schema is not formally documented and differs
between versions (the colour id key is "_id" in current exports; V4 Variables
are created via the Elementor MCP / editor, not this file). Verify every key
against an export from the TARGET site (Elementor > Tools > Export Kit, then
open site-settings.json) before importing, and adapt if names differ.

Motion tokens are not mapped (Elementor has no global motion setting; keep
entrance animations off and add the one motion moment in custom CSS).

Exit codes: 0 ok, 1 unresolved reference (or any warning with --strict),
2 usage error (missing file, no front matter, YAML error).

Examples
  tokens_to_elementor_kit.py DESIGN.md > kit-fragment.json
  tokens_to_elementor_kit.py DESIGN.md --settings-only -o site-settings.fragment.json
  tokens_to_elementor_kit.py DESIGN.md --variables-only
"""
import argparse
import hashlib
import json
import math
import re
import sys


class UsageError(Exception):
    pass


# ============================================================ DESIGN.md parser
# (Duplicated verbatim from build/scripts/tokens_to_css.py:
#  each skill folder must stay self-contained.)

def split_front_matter(text):
    """Return the YAML text between the leading '---' fences."""
    text = text.lstrip("﻿")
    lines = text.splitlines()
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines) or lines[i].strip() != "---":
        raise UsageError("no YAML front matter: the file must start with a '---' line")
    for j in range(i + 1, len(lines)):
        if lines[j].strip() in ("---", "..."):
            return "\n".join(lines[i + 1:j])
    raise UsageError("front matter is not closed with a second '---' line")


def _strip_comment(line):
    out, q = [], None
    for idx, ch in enumerate(line):
        if q:
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
        elif ch == "#" and (idx == 0 or line[idx - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).rstrip()


def _split_flow(s):
    parts, depth, q, cur = [], 0, None, []
    for ch in s:
        if q:
            cur.append(ch)
            if ch == q:
                q = None
            continue
        if ch in "\"'":
            q = ch
        elif ch in "[{(":
            depth += 1
        elif ch in "]})":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append("".join(cur).strip())
            cur = []
            continue
        cur.append(ch)
    if "".join(cur).strip():
        parts.append("".join(cur).strip())
    return parts


def _scalar(s):
    s = s.strip()
    if s == "":
        return None
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        body = s[1:-1]
        if s[0] == '"':
            body = body.replace('\\"', '"').replace("\\\\", "\\")
        else:
            body = body.replace("''", "'")
        return body
    if s.startswith("[") and s.endswith("]"):
        return [_scalar(p) for p in _split_flow(s[1:-1])]
    if s.startswith("{") and s.endswith("}") and not re.fullmatch(r"\{[\w.-]+\}", s):
        d = {}
        for p in _split_flow(s[1:-1]):
            k, _, v = p.partition(":")
            d[str(_scalar(k))] = _scalar(v)
        return d
    low = s.lower()
    if low in ("true", "yes", "on"):
        return True
    if low in ("false", "no", "off"):
        return False
    if low in ("null", "~"):
        return None
    if re.fullmatch(r"[-+]?\d+", s):
        return int(s)
    if re.fullmatch(r"[-+]?(\d+\.\d*|\.\d+|\d+)([eE][-+]?\d+)?", s):
        return float(s)
    return s


def _key_value(content):
    """Split 'key: value' at the first ': ' (or trailing ':') outside quotes."""
    q = None
    for idx, ch in enumerate(content):
        if q:
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
        elif ch == ":" and (idx + 1 == len(content) or content[idx + 1] in " \t"):
            key = content[:idx].strip()
            if len(key) >= 2 and key[0] == key[-1] and key[0] in "\"'":
                key = key[1:-1]
            return key, content[idx + 1:].strip()
    return None, None


def parse_yaml_subset(text):
    """Parse a practical YAML subset: nested block maps, block lists of
    scalars or maps, scalars, flow lists/maps, comments, | and > blocks."""
    raw = text.splitlines()
    lines = []  # (indent, content, lineno)
    for n, ln in enumerate(raw, 1):
        if "\t" in ln[:len(ln) - len(ln.lstrip())]:
            raise UsageError(f"front matter line {n}: tabs are not allowed for indentation")
        lines.append((len(ln) - len(ln.lstrip(" ")), ln, n))
    pos = 0

    def next_significant(p):
        while p < len(lines):
            c = _strip_comment(lines[p][1]).strip()
            if c:
                return p
            p += 1
        return p

    def block_scalar(p, parent_indent, style):
        buf, ind = [], None
        while p < len(lines):
            indent, ln, _ = lines[p]
            if ln.strip() and indent <= parent_indent:
                break
            if ln.strip():
                ind = indent if ind is None else ind
                buf.append(ln[ind:])
            else:
                buf.append("")
            p += 1
        while buf and buf[-1] == "":
            buf.pop()
        return ("\n".join(buf) if style.startswith("|") else " ".join(b for b in buf if b)), p

    def parse_block(p, indent):
        p = next_significant(p)
        if p >= len(lines):
            return None, p
        content = _strip_comment(lines[p][1]).strip()
        if content.startswith("- ") or content == "-":
            return parse_list(p, lines[p][0])
        return parse_map(p, lines[p][0])

    def parse_value(rest, p, indent):
        if rest in ("|", ">", "|-", ">-", "|+", ">+"):
            return block_scalar(p, indent, rest)
        if rest == "":
            q = next_significant(p)
            if q < len(lines) and lines[q][0] > indent:
                return parse_block(q, lines[q][0])
            if q < len(lines) and lines[q][0] == indent and \
                    _strip_comment(lines[q][1]).strip().startswith("- "):
                return parse_list(q, indent)
            return None, p
        return _scalar(rest), p

    def parse_map(p, indent):
        result = {}
        while True:
            p = next_significant(p)
            if p >= len(lines):
                break
            ind, ln, n = lines[p]
            if ind < indent:
                break
            if ind > indent:
                raise UsageError(f"front matter line {n}: unexpected indentation")
            content = _strip_comment(ln).strip()
            if content.startswith("- "):
                break
            key, rest = _key_value(content)
            if key is None:
                raise UsageError(f"front matter line {n}: expected 'key: value', got {content!r}")
            val, p = parse_value(rest, p + 1, indent)
            result[key] = val
        return result, p

    def parse_list(p, indent):
        result = []
        while True:
            p = next_significant(p)
            if p >= len(lines):
                break
            ind, ln, n = lines[p]
            content = _strip_comment(ln).strip()
            if ind != indent or not (content.startswith("- ") or content == "-"):
                if ind > indent:
                    raise UsageError(f"front matter line {n}: unexpected indentation in list")
                break
            item = content[1:].strip()
            key, rest = _key_value(item) if item else (None, None)
            if key is not None and not item.startswith(("'", '"', "{", "[")):
                # list item that is a map: "- key: value" + following keys
                child_indent = indent + 2 + (len(content[1:]) - len(content[1:].lstrip()) - 1)
                lines[p] = (child_indent, " " * child_indent + item, n)  # re-seat as a map line
                val, p = parse_map(p, child_indent)
                result.append(val)
            elif item == "":
                val, p = parse_value("", p + 1, indent)
                result.append(val)
            else:
                result.append(_scalar(item))
                p += 1
        return result, p

    data, _ = parse_block(0, 0)
    return data if data is not None else {}


def load_front_matter(text):
    fm = split_front_matter(text)
    try:
        import yaml  # type: ignore
    except ImportError:
        yaml = None
    if yaml is not None:
        try:
            data = yaml.safe_load(fm)
        except yaml.YAMLError as e:
            raise UsageError(f"YAML error in front matter: {e}")
    else:
        data = parse_yaml_subset(fm)
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise UsageError("front matter must be a YAML mapping")
    return data


REF_RE = re.compile(r"\{([A-Za-z_][\w-]*(?:\.[\w-]+)+)\}")


def lookup(data, path):
    cur = data
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        elif isinstance(cur, dict) and part.isdigit() and int(part) in cur:
            cur = cur[int(part)]
        else:
            return None
    return cur


def resolve_refs(value, data, on_ref=None, depth=0, missing=None):
    """Replace {a.b} references in a string. on_ref(path, resolved) may return
    a replacement string (e.g. a var()); otherwise the resolved value is used."""
    if not isinstance(value, str) or "{" not in value:
        return value
    if depth > 10:
        raise UsageError(f"reference cycle near {value!r}")

    def sub(m):
        path = m.group(1)
        target = lookup(data, path)
        if target is None or isinstance(target, (dict, list)):
            if missing is not None:
                missing.append(path)
            return m.group(0)
        target = resolve_refs(target, data, None, depth + 1, missing)
        if on_ref:
            rep = on_ref(path, target)
            if rep is not None:
                return rep
        return str(target)

    return REF_RE.sub(sub, value)

# ======================================================== end DESIGN.md parser


# ============================================================ colour (OKLCH -> hex)
def _lin_to_srgb(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def _oklch_to_linear(L, C, H):
    h = math.radians(H)
    a, b = C * math.cos(h), C * math.sin(h)
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)


def _in_gamut(rgb, eps=1e-6):
    return all(-eps <= v <= 1 + eps for v in rgb)


def oklch_to_hex(L, C, H):
    """OKLCH -> #rrggbb, clamping to sRGB by reducing chroma."""
    L = min(max(L, 0.0), 1.0)
    if not _in_gamut(_oklch_to_linear(L, C, H)):
        lo, hi = 0.0, C
        for _ in range(40):
            mid = (lo + hi) / 2
            if _in_gamut(_oklch_to_linear(L, mid, H)):
                lo = mid
            else:
                hi = mid
        C = lo
    rgb = [_lin_to_srgb(min(max(v, 0.0), 1.0)) for v in _oklch_to_linear(L, C, H)]
    return "#" + "".join(f"{round(min(max(v, 0), 1) * 255):02x}" for v in rgb)


def _num(tok, pct_scale):
    tok = tok.strip()
    if tok.endswith("%"):
        return float(tok[:-1]) / 100 * pct_scale
    if tok.lower().endswith("deg"):
        return float(tok[:-3])
    if tok.lower() == "none":
        return 0.0
    return float(tok)


def to_hex(value):
    """Hex / rgb() / oklch() string -> '#rrggbb' (upper-case like Elementor), or None."""
    s = str(value).strip()
    m = re.fullmatch(r"#([0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})", s)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        return "#" + h[:6].upper()
    m = re.fullmatch(r"(oklch|rgba?)\(\s*([^)]*)\)", s, re.I)
    if not m:
        return None
    parts = [p for p in re.split(r"[\s,]+", m.group(2).split("/")[0].strip()) if p]
    if len(parts) < 3:
        return None
    try:
        if m.group(1).lower() == "oklch":
            L = _num(parts[0], 1.0)
            if L > 1 and not parts[0].endswith("%"):
                L /= 100
            return oklch_to_hex(L, _num(parts[1], 0.4), _num(parts[2], 360)).upper()
        vals = [min(max(_num(p, 255), 0), 255) for p in parts[:3]]
        return "#" + "".join(f"{round(v):02X}" for v in vals)
    except ValueError:
        return None


# ============================================================ kit building
SYSTEM_COLOR_KEYS = {
    "primary": ["primary", "brand", "brand-9"],
    "secondary": ["secondary", "surface-strong", "neutral"],
    "text": ["text", "ink", "on-surface", "on-background", "foreground", "body"],
    "accent": ["accent", "tertiary", "action", "cta"],
}
SYSTEM_TYPO_KEYS = {
    "primary": ["display", "display-lg", "display-xl", "headline", "headline-lg", "h1", "heading", "title-lg"],
    "secondary": ["headline-md", "headline", "title", "title-md", "h2", "subheading", "heading-2"],
    "text": ["body", "body-md", "body-lg", "text", "paragraph", "p"],
    "accent": ["label", "label-md", "button", "ui", "caption", "nav"],
}


def slug(s):
    return re.sub(r"[^a-z0-9-]+", "-", str(s).strip().lower()).strip("-") or "x"


def short_id(name):
    """Deterministic 7-char id like Elementor's (stable across re-runs)."""
    return hashlib.md5(name.encode("utf-8")).hexdigest()[:7]


def title_of(key):
    return " ".join(w.capitalize() for w in re.split(r"[-_\s]+", str(key)) if w)


def size_obj(v, default_unit="px"):
    """'64px' -> {'unit': 'px', 'size': 64, 'sizes': []}; clamp() -> custom unit."""
    if v is None:
        return None
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return {"unit": default_unit, "size": v, "sizes": []}
    s = str(v).strip()
    m = re.fullmatch(r"(-?\d*\.?\d+)(px|rem|em|%|vw|vh|ch)?", s)
    if m:
        n = float(m.group(1))
        n = int(n) if n.is_integer() else n
        return {"unit": m.group(2) or default_unit, "size": n, "sizes": []}
    return {"unit": "custom", "size": s, "sizes": []}


def first_family(v):
    fam = str(v).split(",")[0].strip().strip("\"'")
    return fam


def pick_system(keys_map, available):
    chosen, used = {}, set()
    norm = {slug(k): k for k in available}
    for sys_id, candidates in keys_map.items():
        for c in candidates:
            if c in norm and norm[c] not in used:
                chosen[sys_id] = norm[c]
                used.add(norm[c])
                break
    return chosen


def build_kit(data, warnings):
    missing = []

    def R(v):
        return resolve_refs(v, data, None, missing=missing) if isinstance(v, str) else v

    # ---- colours (flatten one level of nesting: brand.9 -> brand-9)
    colors = {}
    for k, v in (data.get("colors") or {}).items():
        if isinstance(v, dict):
            for k2, v2 in v.items():
                colors[f"{k}-{k2}"] = v2
        elif not isinstance(v, list):
            colors[str(k)] = v
    hexes = {}
    for k, v in colors.items():
        h = to_hex(R(v))
        if h is None:
            warnings.append(f"colour {k!r}: cannot convert {v!r} to hex, skipped")
        else:
            hexes[k] = h
    sys_colors = pick_system(SYSTEM_COLOR_KEYS, hexes.keys())
    system_colors, custom_colors, variables = [], [], []
    for sys_id in ("primary", "secondary", "text", "accent"):
        if sys_id in sys_colors:
            k = sys_colors[sys_id]
            system_colors.append({"_id": sys_id, "title": title_of(sys_id), "color": hexes[k]})
        else:
            warnings.append(f"no DESIGN.md colour mapped to system colour {sys_id!r}")
    for k, h in hexes.items():
        if k not in sys_colors.values():
            custom_colors.append({"_id": short_id("color:" + k), "title": title_of(k), "color": h})
        variables.append({"name": f"color-{slug(k)}", "type": "color", "value": h})

    # ---- typography
    typo = {str(k): v for k, v in (data.get("typography") or {}).items() if isinstance(v, dict)}
    sys_typo = pick_system(SYSTEM_TYPO_KEYS, typo.keys())

    def typo_entry(_id, title, spec):
        e = {"_id": _id, "title": title, "typography_typography": "custom"}
        if "fontFamily" in spec:
            e["typography_font_family"] = first_family(R(spec["fontFamily"]))
        if "fontSize" in spec:
            e["typography_font_size"] = size_obj(R(spec["fontSize"]))
        if "fontWeight" in spec:
            e["typography_font_weight"] = str(R(spec["fontWeight"]))
        if "lineHeight" in spec:
            lh = R(spec["lineHeight"])
            e["typography_line_height"] = size_obj(lh, "em")
        if "letterSpacing" in spec:
            ls = size_obj(R(spec["letterSpacing"]), "em")
            if ls and ls["unit"] in ("px", "em"):
                e["typography_letter_spacing"] = ls
            else:
                warnings.append(f"typography {title!r}: letterSpacing {spec['letterSpacing']!r} unsupported, skipped")
        if "textTransform" in spec:
            e["typography_text_transform"] = str(R(spec["textTransform"]))
        for fld in ("typography_font_size", "typography_line_height"):
            if e.get(fld, {}).get("unit") == "custom":
                warnings.append(f"typography {title!r}: {fld} {e[fld]['size']!r} written with unit "
                                "'custom' (needs Elementor 3.12+; otherwise set px + responsive sizes by hand)")
        return e

    system_typography, custom_typography = [], []
    for sys_id in ("primary", "secondary", "text", "accent"):
        if sys_id in sys_typo:
            system_typography.append(typo_entry(sys_id, title_of(sys_id), typo[sys_typo[sys_id]]))
        else:
            warnings.append(f"no DESIGN.md typography role mapped to system typography {sys_id!r}")
    fonts_seen = []
    for role, spec in typo.items():
        if role not in sys_typo.values():
            custom_typography.append(typo_entry(short_id("typo:" + role), title_of(role), spec))
        if "fontFamily" in spec:
            fam = first_family(R(spec["fontFamily"]))
            variables.append({"name": f"font-{slug(role)}", "type": "font", "value": fam})
            if fam not in fonts_seen:
                fonts_seen.append(fam)
        if "fontSize" in spec:
            so = size_obj(R(spec["fontSize"]))
            variables.append({"name": f"text-{slug(role)}", "type": "size",
                              "value": so["size"] if so["unit"] == "custom" else f"{so['size']}{so['unit']}"})

    # ---- sizes: radius + spacing as V4 size variables
    for sec, prefix in (("rounded", "radius"), ("spacing", "space")):
        for k, v in (data.get(sec) or {}).items():
            if isinstance(v, (dict, list)):
                continue
            so = size_obj(R(v))
            variables.append({"name": f"{prefix}-{slug(k)}", "type": "size",
                              "value": so["size"] if so["unit"] == "custom" else f"{so['size']}{so['unit']}"})

    for m in sorted(set(missing)):
        warnings.append(f"unresolved reference {{{m}}}")
    kit = {
        "_note": ("Generated by tokens_to_elementor_kit.py from DESIGN.md. Verify the key names against a "
                  "kit export (Tools > Export Kit > site-settings.json) from the target site before importing; "
                  "Elementor versions differ."),
        "_source": data.get("name") or "DESIGN.md",
        "settings": {
            "system_colors": system_colors,
            "custom_colors": custom_colors,
            "system_typography": system_typography,
            "custom_typography": custom_typography,
        },
        "variables": variables,
        "fonts_to_self_host": fonts_seen,
    }
    return kit, bool(missing)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog=__doc__.split("\n", 1)[1],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("design_md", help="path to DESIGN.md")
    p.add_argument("-o", "--output", help="write JSON here instead of stdout")
    p.add_argument("--settings-only", action="store_true",
                   help="print only the 'settings' object (for pasting into site-settings.json)")
    p.add_argument("--variables-only", action="store_true", help="print only the V4 variables list")
    p.add_argument("--strict", action="store_true", help="exit 1 on any warning, not only unresolved refs")
    args = p.parse_args(argv)
    if args.settings_only and args.variables_only:
        p.error("--settings-only and --variables-only are mutually exclusive")
    warnings = []
    try:
        try:
            with open(args.design_md, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as e:
            raise UsageError(str(e))
        data = load_front_matter(text)
        if not data.get("colors") and not data.get("typography"):
            raise UsageError("front matter has no colors or typography")
        kit, unresolved = build_kit(data, warnings)
    except UsageError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    out = kit["settings"] if args.settings_only else kit["variables"] if args.variables_only else kit
    js = json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(js)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(js)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    if unresolved or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
