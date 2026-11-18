# 18 — Agent Skills specification
https://agentskills.io/specification · Spec (open standard + docs) · Code Apache-2.0, docs CC-BY-4.0 (repo agentskills/agentskills) · 27.4k stars · read 2026-11-18 (no commit hash shown; 147 commits on main)

## 1. What it is
The open, cross-client format spec for "Agent Skills": a folder with a `SKILL.md` (YAML frontmatter + Markdown) plus optional scripts/references/assets. Also read: Best practices, Optimizing descriptions, Using scripts, Adding skills support (client guide).

## 2. How it works
- Layout: `skill-name/SKILL.md` (required) + optional `scripts/` (runnable code), `references/` (docs loaded on demand, e.g. REFERENCE.md, domain files), `assets/` (templates, images, data/lookup tables, schemas); any other files allowed.
- Progressive disclosure, 3 tiers: (1) catalog = name+description loaded at startup for every skill, ~50–100 tokens each; (2) full SKILL.md body loaded on activation, <5,000 tokens recommended; (3) resources loaded only when the body points to them.
- Activation is model-driven (model reads the catalog and decides) or user-explicit (slash command `/skill-name`). Clients read the file directly or via an activate tool; many strip frontmatter.
- Discovery (client guide): project `<project>/.<client>/skills/` and `.agents/skills/`, user `~/.<client>/skills/` and `~/.agents/skills/`; many also scan `.claude/skills/`. Project-level beats user-level on name collision.
- Validation: `skills-ref validate ./my-skill` (reference lib in the agentskills repo) checks frontmatter and naming.

## 3. Rules
- [tooling] Skill = one directory; `SKILL.md` exactly that filename, YAML frontmatter between `---` lines, then Markdown body
- [tooling] `name` required: 1–64 chars, only a-z, 0-9 and hyphen; no leading/trailing hyphen; no `--`; must equal the parent folder name
- [tooling] `description` required: 1–1024 chars, non-empty; say what it does AND when to use it, with trigger keywords
- [tooling] Optional fields only: `license` (short name or bundled file), `compatibility` (1–500 chars, only if real env needs e.g. "Requires Node 18+, Chrome"), `metadata` (string->string map, unique key names), `allowed-tools` (space-separated, experimental, varies by client)
- [tooling] Quote description values that contain a colon — unquoted `when: ...` is invalid YAML and some clients choke
- [tooling] Keep SKILL.md under 500 lines and under ~5,000 tokens; move detail to `references/`
- [tooling] Reference files with relative paths from the skill root (`references/x.md`, `scripts/y.py`); keep references ONE level deep from SKILL.md, no chains
- [tooling] Keep each reference file focused/small — each one costs context when loaded
- [tooling] Run `skills-ref validate` before shipping
- [process] Say WHEN to load each reference ("Read references/funeral.md if the client is a funeral home"), not a generic "see references/"
- [process] Description phrasing: imperative ("Use this skill when..."), about user intent not internals, a bit pushy (list cases where user doesn't name the domain), a few sentences max
- [process] Test triggering with ~20 realistic queries (8–10 should, 8–10 near-miss shouldn't), 3 runs each, pass threshold 0.5 trigger rate; 60/40 train/validation split; ~5 iterations; pick best by validation score
- [process] Only include what the agent would get wrong without it; cut generic explanations ("would it fail without this line?")
- [process] Moderate detail beats exhaustive docs; one coherent unit of work per skill (not too narrow, not too broad)
- [process] Match prescriptiveness to fragility: freedom + reasons for creative parts, exact commands for fragile steps
- [process] Give a default, not a menu of equal options
- [process] Teach a reusable procedure, not one instance's answer
- [process] Keep a "Gotchas" section in SKILL.md itself; add every correction you make to it
- [process] Use concrete output templates (short inline, long ones in `assets/`), checklists for multi-step flows, validate-fix-repeat loops, plan-validate-execute for batch/destructive work
- [process] Build skills from real project material (our past sites, review comments, fixes), then execute on real tasks and revise from traces
- [tooling] Scripts: no interactive prompts; `--help` with examples; clear errors (what was wrong, what's allowed); JSON to stdout, diagnostics to stderr; idempotent; `--dry-run` for destructive ops; distinct exit codes; bounded output size
- [tooling] Pin versions for one-off tools (`npx pkg@x.y.z`, `uvx`); Python scripts declare deps inline (PEP 723, run with `uv run`)
- [tooling] Bundle a script when the agent keeps reinventing the same logic across runs

## 4. AI tells / anti-patterns it bans
n/a for design. Skill-authoring anti-patterns: vague generic advice ("follow best practices"), LLM-generated skills without domain input, over-long SKILL.md, menus without defaults, deep reference chains, keyword-stuffed descriptions overfit to test queries.

## 5. Data, assets and scripts it ships (and what they need: Node, Python, Chrome)
Spec + docs only. `skills-ref` validator in the repo (not inspected/installed per brief; repo has package.json). Example trigger-eval bash script uses `claude -p ... --output-format json` + `jq`.

## 6. Area
tooling

## 7. Take / skip
- Take: all hard limits (name, 1024-char description, 500 lines / 5k tokens, one-level refs) as our build constraints; niche files in `references/` loaded conditionally (fits "different look per niche"); Gotchas section for AI-design tells; trigger-eval method for our description.
- Take for portability: stick to required + standard optional fields; put Claude-specific extras (e.g. `disable-model-invocation`, `allowed-tools`) only where needed — other clients may ignore them. Install path `.agents/skills/` is the cross-client convention; `.claude/skills/` for Claude Code. Avoid assuming a specific tool name in the body; use relative paths.
- Skip: client-implementation internals (we are authors, not a client); Deno/Bun/Ruby script variants (we use Node + Python).

## 8. Open questions
- Client Showcase page (agentskills.io/clients) rendered empty via WebFetch — list of supporting AIs not confirmed.
- Not read: Evaluating skill output quality — https://agentskills.io/skill-creation/evaluating-skills.md (output-quality evals; likely useful for our QA).
- SUGGESTED: anthropics/skills skill-creator - https://github.com/anthropics/skills/tree/main/skills/skill-creator - automates description trigger-optimization loop.
