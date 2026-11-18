#!/usr/bin/env python3
"""niche_log.py - history log of past Bexven sites, collision check and seeded pick.

The log is a JSON file (a list of site records). Default location is
~/.bexven/niche-log.json; override with the BEXVEN_NICHE_LOG environment
variable or --log PATH (the flag wins).

Subcommands
  add    Append a finished site to the log.
  list   Show logged sites (optionally only one niche).
  check  Test a candidate direction against the log. Collisions:
           - display font used in any of the last 5 sites in the niche,
             or in 2+ of the last 5 sites overall
           - same palette_family, hero_type or section_order as any of the
             last 5 sites in the niche
           - accent hue within +/-20 degrees of any of the last 3 in the niche
  pick   Pick one of N direction names. With --seed the pick is
         deterministic; without, a seed is drawn from the clock. The seed is
         printed so it can be recorded in DESIGN.md / the log.

Exit codes: 0 ok / no collisions, 1 collisions found or I/O failure,
2 usage error.

Examples
  niche_log.py add --client "Hale & Sons" --niche funeral-home \\
      --direction "Chapel ledger" --display-font "Cormorant" --body-font "Source Serif 4" \\
      --palette-family "deep green + brass" --accent-hue 85 --theme light \\
      --hero-type photo-split --section-order hero,services,people,obituaries,contact \\
      --signature-moment "candle-light hover on obituary photos" --url https://example.org
  niche_log.py check --niche funeral-home --display-font Cormorant --accent-hue 95
  niche_log.py pick "Chapel ledger" "Quiet garden" "Stone and brass" --seed 4211
"""
import argparse
import datetime as _dt
import json
import os
import random
import sys
import time

DEFAULT_LOG = os.path.join(os.path.expanduser("~"), ".bexven", "niche-log.json")
FIELDS = ["client", "niche", "date", "direction", "display_font", "body_font",
          "palette_family", "accent_hue", "theme", "hero_type", "section_order",
          "signature_moment", "url"]


class UsageError(Exception):
    pass


def log_path(args):
    return args.log or os.environ.get("BEXVEN_NICHE_LOG") or DEFAULT_LOG


def load(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        text = fh.read().strip()
    if not text:
        return []
    data = json.loads(text)
    if isinstance(data, dict) and "sites" in data:
        data = data["sites"]
    if not isinstance(data, list):
        raise ValueError("log file must contain a JSON list of site records")
    return data


def save(path, entries):
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(entries, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)


def norm(s):
    return " ".join(str(s or "").lower().split())


def norm_order(s):
    if isinstance(s, list):
        parts = s
    else:
        parts = str(s or "").split(",")
    return ",".join(norm(p) for p in parts if norm(p))


def hue_dist(a, b):
    d = abs(float(a) - float(b)) % 360
    return min(d, 360 - d)


def by_date(entries):
    # Stable sort by date string (ISO dates sort lexically); undated keep log order.
    return sorted(enumerate(entries), key=lambda t: (str(t[1].get("date") or ""), t[0]))


def last_n(entries, n, niche=None):
    seq = [e for _, e in by_date(entries)]
    if niche is not None:
        seq = [e for e in seq if norm(e.get("niche")) == norm(niche)]
    return seq[-n:]


def cmd_add(args):
    path = log_path(args)
    entries = load(path)
    date = args.date or _dt.date.today().isoformat()
    try:
        _dt.date.fromisoformat(date)
    except ValueError:
        raise UsageError("--date must be YYYY-MM-DD")
    rec = {
        "client": args.client,
        "niche": args.niche,
        "date": date,
        "direction": args.direction,
        "display_font": args.display_font,
        "body_font": args.body_font,
        "palette_family": args.palette_family,
        "accent_hue": int(args.accent_hue) if float(args.accent_hue).is_integer() else args.accent_hue,
        "theme": args.theme,
        "hero_type": args.hero_type,
        "section_order": [p.strip() for p in (args.section_order or "").split(",") if p.strip()],
        "signature_moment": args.signature_moment,
        "url": args.url,
    }
    if args.seed is not None:
        rec["pick_seed"] = args.seed
    entries.append(rec)
    save(path, entries)
    print(f"added {args.client!r} ({args.niche}) to {path} - {len(entries)} site(s) logged")
    return 0


def cmd_list(args):
    entries = load(log_path(args))
    rows = [e for _, e in by_date(entries)]
    if args.niche:
        rows = [e for e in rows if norm(e.get("niche")) == norm(args.niche)]
    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return 0
    if not rows:
        print("no sites logged" + (f" for niche {args.niche!r}" if args.niche else ""))
        return 0
    for e in rows:
        order = e.get("section_order")
        if isinstance(order, list):
            order = ",".join(order)
        print(f"{e.get('date','?')}  {e.get('niche','?'):<18} {e.get('client','?')}")
        print(f"    direction: {e.get('direction','')}  theme: {e.get('theme','')}  hero: {e.get('hero_type','')}")
        print(f"    fonts: {e.get('display_font','')} / {e.get('body_font','')}  "
              f"palette: {e.get('palette_family','')}  accent hue: {e.get('accent_hue','')}")
        print(f"    order: {order or ''}")
        if e.get("signature_moment"):
            print(f"    moment: {e['signature_moment']}")
        if e.get("url"):
            print(f"    url: {e['url']}")
    return 0


def cmd_check(args):
    entries = load(log_path(args))
    niche5 = last_n(entries, 5, args.niche)
    niche3 = last_n(entries, 3, args.niche)
    all5 = last_n(entries, 5)
    reasons = []

    def who(e):
        return f"{e.get('client','?')} ({e.get('date','?')})"

    if args.display_font:
        f = norm(args.display_font)
        hits = [e for e in niche5 if norm(e.get("display_font")) == f]
        if hits:
            reasons.append(f"display font {args.display_font!r} used in last 5 {args.niche} sites: "
                           + ", ".join(who(e) for e in hits))
        hits_all = [e for e in all5 if norm(e.get("display_font")) == f]
        if len(hits_all) >= 2:
            reasons.append(f"display font {args.display_font!r} used in {len(hits_all)} of the last 5 "
                           "sites overall: " + ", ".join(who(e) for e in hits_all))
    if args.body_font:
        # Informational only (not a collision rule), but useful.
        hits = [e for e in niche5 if norm(e.get("body_font")) == norm(args.body_font)]
        if hits:
            print(f"note: body font {args.body_font!r} also used by " + ", ".join(who(e) for e in hits))
    for field, label in (("palette_family", "palette family"), ("hero_type", "hero type")):
        val = getattr(args, field)
        if val:
            hits = [e for e in niche5 if norm(e.get(field)) == norm(val)]
            if hits:
                reasons.append(f"{label} {val!r} matches last 5 {args.niche} sites: "
                               + ", ".join(who(e) for e in hits))
    if args.section_order:
        cand = norm_order(args.section_order)
        hits = [e for e in niche5 if norm_order(e.get("section_order")) == cand]
        if hits:
            reasons.append(f"section order {cand!r} matches last 5 {args.niche} sites: "
                           + ", ".join(who(e) for e in hits))
    if args.accent_hue is not None:
        hits = []
        for e in niche3:
            h = e.get("accent_hue")
            if h is None or h == "":
                continue
            try:
                d = hue_dist(args.accent_hue, h)
            except (TypeError, ValueError):
                continue
            if d <= 20:
                hits.append(f"{who(e)} hue {h} (diff {d:.0f})")
        if hits:
            reasons.append(f"accent hue {args.accent_hue:g} within +/-20 deg of last 3 {args.niche} sites: "
                           + "; ".join(hits))

    print(f"checked against {len(niche5)} recent {args.niche} site(s) and {len(all5)} recent site(s) overall")
    if reasons:
        print("COLLISIONS:")
        for r in reasons:
            print(f"  - {r}")
        return 1
    print("OK: no collisions")
    return 0


def cmd_pick(args):
    names = [n for n in args.names if n.strip()]
    if len(names) < 2:
        raise UsageError("pick needs at least 2 direction names")
    seed = args.seed if args.seed is not None else int(time.time_ns() % 1_000_000_007)
    rng = random.Random(seed)
    chosen = rng.choice(names)
    if args.json:
        print(json.dumps({"chosen": chosen, "seed": seed, "candidates": names}))
    else:
        print(f"chosen: {chosen}")
        print(f"seed: {seed}")
        print(f"candidates: {' | '.join(names)}")
    return 0


def build_parser():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog=__doc__.split("\n", 1)[1],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--log", help="path to the JSON log (default: $BEXVEN_NICHE_LOG or ~/.bexven/niche-log.json)")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="append a finished site to the log")
    a.add_argument("--client", required=True)
    a.add_argument("--niche", required=True, help="niche slug, e.g. funeral-home")
    a.add_argument("--date", help="YYYY-MM-DD (default today)")
    a.add_argument("--direction", required=True, help="direction name")
    a.add_argument("--display-font", required=True)
    a.add_argument("--body-font", required=True)
    a.add_argument("--palette-family", required=True, help='e.g. "deep green + brass"')
    a.add_argument("--accent-hue", type=float, required=True, help="OKLCH hue of the action accent (0-360)")
    a.add_argument("--theme", choices=["light", "dark"], required=True)
    a.add_argument("--hero-type", required=True, help="e.g. photo-split, full-bleed-photo, type-only")
    a.add_argument("--section-order", required=True, help="comma list, e.g. hero,services,about,contact")
    a.add_argument("--signature-moment", default="", help="the one motion/hover idea")
    a.add_argument("--url", default="")
    a.add_argument("--seed", type=int, help="seed used for the pick (optional, recorded)")
    a.set_defaults(func=cmd_add)

    l = sub.add_parser("list", help="list logged sites")
    l.add_argument("--niche")
    l.add_argument("--json", action="store_true", help="print raw JSON")
    l.set_defaults(func=cmd_list)

    c = sub.add_parser("check", help="check a candidate direction for collisions (exit 1 if any)")
    c.add_argument("--niche", required=True)
    c.add_argument("--display-font")
    c.add_argument("--body-font")
    c.add_argument("--palette-family")
    c.add_argument("--accent-hue", type=float)
    c.add_argument("--hero-type")
    c.add_argument("--section-order", help="comma list")
    c.set_defaults(func=cmd_check)

    k = sub.add_parser("pick", help="seeded random pick among direction names")
    k.add_argument("names", nargs="+", help="direction names (quote names with spaces)")
    k.add_argument("--seed", type=int, help="integer seed for a reproducible pick")
    k.add_argument("--json", action="store_true")
    k.set_defaults(func=cmd_pick)
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "accent_hue", None) is not None and not (0 <= args.accent_hue <= 360):
        parser.error("--accent-hue must be between 0 and 360")
    try:
        return args.func(args)
    except UsageError as e:
        parser.error(str(e))
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
