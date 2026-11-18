#!/usr/bin/env python3
"""tokens_to_css.py - DESIGN.md YAML front matter -> a :root CSS custom-property block.

Reads the YAML front matter (between the first two '---' lines) of a
DESIGN.md in the Google DESIGN.md shape and prints CSS:

  colors:      primary: "#1f3b2d"          -> --color-primary
  typography:  display-lg:                 -> --font-display-lg   (fontFamily)
                 fontFamily: Cormorant        --text-display-lg   (fontSize)
                 fontSize: 64px               --text-display-lg--weight
                 fontWeight: 500              --text-display-lg--line-height
                 lineHeight: 1.05             --text-display-lg--tracking
                 letterSpacing: -0.01em
  rounded:     md: 6px                     -> --radius-md
  spacing:     4: 16px                     -> --space-4
  motion:      ease-out: cubic-bezier(...) -> --ease-out
               dur-fast: 150ms             -> --dur-fast
               (nested maps also work: motion.easing.out -> --ease-out,
                motion.duration.fast -> --dur-fast; any key holding a
                cubic-bezier()/linear()/steps() value becomes --ease-*, any
                time value (ms/s) becomes --dur-*)

Token references such as "{colors.primary}" are resolved. By default they
become var(--color-primary) so the link survives in CSS; --refs literal
inlines the resolved value instead.

Bare numbers get units: fontSize / rounded / spacing -> px, letterSpacing -> em;
lineHeight and fontWeight stay unitless. Colour values are passed through
unchanged (hex or oklch()); give hex fallbacks in DESIGN.md if you need them.

PyYAML is used when importable; otherwise a built-in YAML-subset parser
handles nested maps, scalars (quoted/unquoted strings, numbers, booleans,
null), comments, simple lists and flow lists.

Exit codes: 0 ok, 1 unresolved reference or nothing to output,
2 usage error (missing file, no front matter, YAML error).

Examples
  tokens_to_css.py DESIGN.md > tokens.css
  tokens_to_css.py DESIGN.md --refs literal --selector ':root' -o src/tokens.css
"""
import argparse
import re
import sys


class UsageError(Exception):
    pass


# ============================================================ DESIGN.md parser
# (Duplicated verbatim in elementor/scripts/tokens_to_elementor_kit.py:
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


def slug(s):
    return re.sub(r"[^a-z0-9-]+", "-", str(s).strip().lower()).strip("-") or "x"


def with_unit(v, unit):
    if isinstance(v, bool) or v is None:
        return v
    if isinstance(v, (int, float)):
        return "0" if v == 0 else f"{v:g}{unit}"
    if isinstance(v, str) and re.fullmatch(r"-?\d+(\.\d+)?", v.strip()):
        return with_unit(float(v), unit)
    return v


GENERIC = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "ui-serif",
           "ui-sans-serif", "ui-monospace", "ui-rounded", "emoji", "math", "fangsong"}


def font_stack(v):
    if isinstance(v, list):
        parts = [str(x) for x in v]
    else:
        parts = [p.strip() for p in str(v).split(",")]
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if p.startswith("var(") or p[0] in "\"'" or p.lower() in GENERIC or re.fullmatch(r"[\w-]+", p):
            out.append(p)
        else:
            out.append(f'"{p}"')
    return ", ".join(out)


def is_time(v):
    return isinstance(v, str) and re.fullmatch(r"-?\d*\.?\d+(ms|s)", v.strip()) is not None


def is_easing(v):
    return isinstance(v, str) and re.match(r"(cubic-bezier|linear|steps)\(|^(ease|ease-in|ease-out|ease-in-out)$",
                                           v.strip()) is not None


# section -> (css prefix)
PREFIX = {"colors": "color", "rounded": "radius", "spacing": "space"}


def var_for(path):
    """Map a token path to the custom property this script emits for it."""
    parts = path.split(".")
    sec = parts[0]
    if sec in PREFIX and len(parts) == 2:
        return f"var(--{PREFIX[sec]}-{slug(parts[1])})"
    if sec == "typography" and len(parts) == 3:
        role, prop = slug(parts[1]), parts[2]
        name = {"fontFamily": f"--font-{role}", "fontSize": f"--text-{role}",
                "fontWeight": f"--text-{role}--weight", "lineHeight": f"--text-{role}--line-height",
                "letterSpacing": f"--text-{role}--tracking"}.get(prop)
        return f"var({name})" if name else None
    if sec == "motion":
        return None  # motion names are inferred from values; inline
    return None


def flatten_motion(node, trail=()):
    """Yield (name_parts, value) leaves of the motion section."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield from flatten_motion(v, trail + (str(k),))
    else:
        yield trail, node


def motion_props(motion, resolve):
    out = []
    for trail, v in flatten_motion(motion):
        v = resolve(v)
        if not trail:
            continue
        group = trail[0].lower()
        rest = [slug(t) for t in trail[1:]]
        leaf = slug("-".join(trail))
        if group in ("easing", "easings", "ease", "eases", "curves") and rest:
            out.append((f"--ease-{'-'.join(rest)}", v))
        elif group in ("duration", "durations", "dur", "timing") and rest:
            out.append((f"--dur-{'-'.join(rest)}", with_unit(v, "ms")))
        elif is_easing(str(v)):
            name = leaf[5:] if leaf.startswith("ease-") else leaf
            out.append((f"--ease-{name}", v))
        elif is_time(str(v)) or isinstance(v, (int, float)):
            name = leaf
            for pre in ("duration-", "dur-"):
                if name.startswith(pre):
                    name = name[len(pre):]
            out.append((f"--dur-{name}", with_unit(v, "ms")))
        else:
            out.append((f"--motion-{leaf}", v))
    return out


def build_css(data, refs_mode, selector):
    missing = []

    def on_ref(path, target):
        if refs_mode == "var":
            return var_for(path)
        return None

    def R(v):
        return resolve_refs(v, data, on_ref, missing=missing) if isinstance(v, str) else v

    groups = []
    colors = data.get("colors") or {}
    if isinstance(colors, dict) and colors:
        groups.append(("Colours", [(f"--color-{slug(k)}", R(v)) for k, v in colors.items()
                                   if not isinstance(v, (dict, list))]))
        # one level of nesting (e.g. colors.brand.9) -> --color-brand-9
        nested = []
        for k, v in colors.items():
            if isinstance(v, dict):
                for k2, v2 in v.items():
                    nested.append((f"--color-{slug(k)}-{slug(k2)}", R(v2)))
        if nested:
            groups[-1][1].extend(nested)

    typo = data.get("typography") or {}
    if isinstance(typo, dict) and typo:
        props = []
        for role, spec in typo.items():
            r = slug(role)
            if not isinstance(spec, dict):
                props.append((f"--font-{r}", font_stack(R(spec))))
                continue
            if "fontFamily" in spec:
                fam = R(spec["fontFamily"])
                props.append((f"--font-{r}", fam if str(fam).startswith("var(") else font_stack(fam)))
            if "fontSize" in spec:
                props.append((f"--text-{r}", with_unit(R(spec["fontSize"]), "px")))
            if "fontWeight" in spec:
                props.append((f"--text-{r}--weight", R(spec["fontWeight"])))
            if "lineHeight" in spec:
                props.append((f"--text-{r}--line-height", R(spec["lineHeight"])))
            if "letterSpacing" in spec:
                props.append((f"--text-{r}--tracking", with_unit(R(spec["letterSpacing"]), "em")))
            for extra, suffix in (("fontFeature", "font-feature"), ("fontVariation", "font-variation"),
                                  ("textTransform", "text-transform")):
                if extra in spec:
                    props.append((f"--text-{r}--{suffix}", R(spec[extra])))
        groups.append(("Typography", props))

    for sec, title in (("rounded", "Radius"), ("spacing", "Spacing")):
        node = data.get(sec) or {}
        if isinstance(node, dict) and node:
            groups.append((title, [(f"--{PREFIX[sec]}-{slug(k)}", with_unit(R(v), "px"))
                                   for k, v in node.items() if not isinstance(v, (dict, list))]))

    motion = data.get("motion") or {}
    if isinstance(motion, dict) and motion:
        groups.append(("Motion", motion_props(motion, R)))

    groups = [(t, ps) for t, ps in groups if ps]
    if not groups:
        raise UsageError("front matter has no colors / typography / rounded / spacing / motion tokens")

    title = data.get("name") or "DESIGN.md"
    lines = [f"/* Tokens generated from {title} by tokens_to_css.py. Edit DESIGN.md, not this block. */",
             f"{selector} {{"]
    for t, ps in groups:
        lines.append(f"  /* {t} */")
        for k, v in ps:
            if v is None:
                continue
            if isinstance(v, bool):
                v = str(v).lower()
            lines.append(f"  {k}: {v};")
    lines.append("}")
    return "\n".join(lines) + "\n", sorted(set(missing))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog=__doc__.split("\n", 1)[1],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("design_md", help="path to DESIGN.md")
    p.add_argument("-o", "--output", help="write CSS here instead of stdout")
    p.add_argument("--refs", choices=["var", "literal"], default="var",
                   help="how {token.refs} are written: var(--...) (default) or the literal value")
    p.add_argument("--selector", default=":root", help="selector for the block (default :root)")
    args = p.parse_args(argv)
    try:
        try:
            with open(args.design_md, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as e:
            raise UsageError(str(e))
        data = load_front_matter(text)
        css, missing = build_css(data, args.refs, args.selector)
    except UsageError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(css)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(css)
    if missing:
        for m in missing:
            print(f"error: unresolved reference {{{m}}}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
