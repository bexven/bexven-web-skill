# Bexven web skill

Claude Code plugin that designs and builds client websites that don't look AI-made, and that keeps sites in the same niche different from each other.

- **Plugin:** This folder has 4 skills: `direction`, `build`, `elementor`, `qa`.
- **Research:** [`research/`](../research/) holds the sources behind every rule:
  - [`index.md`](../research/index.md): all 47 sources plus suggested ones
  - [`sheets/`](../research/sheets/): one sheet per source
  - [`analysis/`](../research/analysis/): duplicates and conflicts
  - [`master/master-sheet.md`](../research/master/master-sheet.md): 454 merged rules, each tagged with its sources
  - [`PLAN.md`](../research/PLAN.md)
- **Credits and licences:** [`CREDITS.md`](../CREDITS.md).

## Install (Claude Code)

The repo is a plugin marketplace named `bexven-skills`. In a terminal:

```bash
claude plugin marketplace add bexven/bexven-web-skill
```

```bash
claude plugin install bexven-web@bexven-skills
```

Or inside a Claude Code session: `/plugin marketplace add bexven/bexven-web-skill`, then `/plugin install bexven-web@bexven-skills`.

The repo is private, so your git must be able to clone it (GitHub CLI login or SSH key).

**Update after changes:**

```bash
claude plugin marketplace update bexven-skills
```

**Requirements:**
- Python 3.9+.
- For screenshots: `pip install playwright`. If Playwright's own Chromium isn't installed, the script falls back to an installed Chrome or Edge.
- Optional:
  - Vercel CLI, for preview deploys
  - the Elementor MCP (Elementor 4.3+ with WordPress 6.8+), for WordPress builds

## The skills

| Skill | Run it as | Use it for |
|---|---|---|
| direction | `/bexven-web:direction` | Brief, the niche's usual look (to avoid), 3–5 directions, a seeded pick checked against the niche history log, then DESIGN.md |
| build | `/bexven-web:build` | Static HTML/CSS pages, sections and components (forms included) from DESIGN.md; Vercel preview |
| elementor | `/bexven-web:elementor` | DESIGN.md + static page → WordPress/Elementor, via Elementor MCP or a kit-JSON fallback |
| qa | `/bexven-web:qa` | Lint, screenshots, contrast and number checks, a scored critique, fix loop, ship / fix / rebuild verdict |

Small jobs (one form or section) take a short path and don't run the whole agency process.

## Niche history log

`direction` records each site's font, palette family, hero type and section order in `~/.bexven/niche-log.json`. You can override the path with the `BEXVEN_NICHE_LOG` environment variable. The next site in the same niche can't reuse them. Keep this file somewhere shared (e.g. a synced folder) so the whole team sees the same history.

## Editing the plugin

- `shared/` holds `tells.md` and `niches/*`, the single source of truth. After editing, run `python3 scripts/sync_shared.py`, which copies them into each skill's `references/`.
- Review `tells.md` every quarter, because AI tells change over time.
- Bump `version` in `.claude-plugin/plugin.json` when you release changes.
- Check with `claude plugin validate .` before pushing.
