#!/usr/bin/env python3
"""sync_shared.py - copy shared/ files into each skill's references/ folder.

bexven-web/shared/ is the single source of truth for files several skills
need (tells.md, niches/*). Each skill must stay
self-contained, so this script copies every shared file into
skills/<skill>/references/<same relative path> for every skill listed for it
in MAPPING below. Edit shared/, never the copies.

MAPPING keys are paths relative to shared/ and may use glob patterns
(fnmatch, '*' also matches '/'). The first matching pattern wins. Shared
files that match no pattern are reported as warnings and not copied.

Modes
  (default)  copy new or changed files, report what changed
  --check    copy nothing; exit 1 if any copy is missing or differs
  --dry-run  show what would be copied

Exit codes: 0 in sync / copied, 1 out of date (--check) or copy failure,
2 usage error (shared/ or skills/ not found).

Examples
  python3 scripts/sync_shared.py
  python3 scripts/sync_shared.py --check     # CI / pre-commit
"""
import argparse
import filecmp
import fnmatch
import os
import shutil
import sys

# shared path (relative to shared/) -> skills that get a copy in references/
MAPPING = {
    "tells.md": ["direction", "build", "elementor", "qa"],
    "niches/*": ["direction", "build"],
}

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def shared_files(shared_dir):
    for dirpath, dirnames, filenames in os.walk(shared_dir):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for fn in sorted(filenames):
            if fn.startswith(".") or fn.endswith("~"):
                continue
            full = os.path.join(dirpath, fn)
            yield os.path.relpath(full, shared_dir).replace(os.sep, "/")


def targets_for(rel):
    for pattern, skills in MAPPING.items():
        if fnmatch.fnmatch(rel, pattern):
            return skills
    return None


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog=__doc__.split("\n", 1)[1],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", default=PLUGIN_ROOT, help="plugin root holding shared/ and skills/ (default: this plugin)")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="exit 1 if any copy is missing or out of date")
    mode.add_argument("--dry-run", action="store_true", help="show what would be copied")
    p.add_argument("-q", "--quiet", action="store_true", help="only print changes and problems")
    args = p.parse_args(argv)

    shared_dir = os.path.join(args.root, "shared")
    skills_dir = os.path.join(args.root, "skills")
    if not os.path.isdir(shared_dir) or not os.path.isdir(skills_dir):
        print(f"error: {args.root} must contain shared/ and skills/", file=sys.stderr)
        return 2
    for skills in MAPPING.values():
        for s in skills:
            if not os.path.isdir(os.path.join(skills_dir, s)):
                print(f"error: MAPPING names skill {s!r} but skills/{s}/ does not exist", file=sys.stderr)
                return 2

    stale, copied, ok, failed = [], [], 0, 0
    n_files = 0
    for rel in shared_files(shared_dir):
        n_files += 1
        skills = targets_for(rel)
        if skills is None:
            print(f"warning: shared/{rel} matches no MAPPING pattern; not copied", file=sys.stderr)
            continue
        src = os.path.join(shared_dir, rel)
        for s in skills:
            dst = os.path.join(skills_dir, s, "references", rel)
            shown = f"skills/{s}/references/{rel}"
            if os.path.exists(dst) and filecmp.cmp(src, dst, shallow=False):
                ok += 1
                continue
            state = "missing" if not os.path.exists(dst) else "differs"
            if args.check:
                stale.append(f"{shown} ({state})")
            elif args.dry_run:
                print(f"would copy shared/{rel} -> {shown} ({state})")
            else:
                try:
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy2(src, dst)
                    copied.append(shown)
                    print(f"copied shared/{rel} -> {shown} ({state})")
                except OSError as e:
                    failed += 1
                    print(f"error: {shown}: {e}", file=sys.stderr)

    if args.check:
        if stale:
            print("out of date (run scripts/sync_shared.py):")
            for s in stale:
                print(f"  {s}")
            return 1
        if not args.quiet:
            print(f"in sync: {ok} copies of {n_files} shared file(s)")
        return 0
    if not args.quiet and not args.dry_run:
        print(f"done: {len(copied)} copied, {ok} already up to date, {n_files} shared file(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
