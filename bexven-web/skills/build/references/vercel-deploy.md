# Vercel deploy

Load at build step 11. Only deploy when the user asks, or when the outreach flow calls for a preview link. Run QA first.

## Defaults

- **Preview by default.** `--prod` only when the user explicitly asks for production in this conversation.
- **Token from the `VERCEL_TOKEN` environment variable only.** Never pass `--token` on the command line (it lands in shell history and logs), never echo it, never write it into files or the repo.
- **Ask before any `git push`** or commit that would trigger a Vercel build.
- **Do not run `vercel link`** (or project-inspecting commands) in an unlinked folder "to check": it silently links or prompts. `vercel whoami` is safe.
- One Vercel project per prospect, under the agency team (`--scope <team>`).
- Outreach previews are `noindex` (meta tag in HTML **and** the header below).
- Return the URL to the user. Do not curl the deployed URL to "verify"; QA uses Playwright on the URL if needed.

## Pre-flight (read-only)

```bash
command -v vercel || echo "no CLI"        # CLI present? (else: npx vercel@<pinned-version> …)
test -n "$VERCEL_TOKEN" && echo "token set" || echo "no token"
vercel whoami                              # safe; confirms auth
test -f .vercel/project.json && cat .vercel/project.json   # already linked?
git remote -v 2>/dev/null                  # git-connected project?
```
Pin the CLI version when using `npx` (e.g. `npx vercel@<version>`), never `@latest` in instructions or scripts.

## Project files for a static mock

`vercel.json` in the project root:
```json
{
  "cleanUrls": true,
  "headers": [
    { "source": "/(.*)", "headers": [
      { "key": "X-Robots-Tag", "value": "noindex, nofollow" },
      { "key": "X-Content-Type-Options", "value": "nosniff" },
      { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
      { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()" }
    ]},
    { "source": "/(fonts|img|css|js)/(.*)", "headers": [
      { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
    ]}
  ]
}
```
- Remove the `X-Robots-Tag` header (and the meta robots tag) only at real launch on the client's domain.
- Use `immutable` caching only if asset filenames change when content changes; otherwise drop that block.
- No `X-XSS-Protection`. No polyfill CDNs. No public source maps.
- `.vercelignore`: exclude `DESIGN.md`, `qa/`, raw photo folders and `.env*` so internal notes and assumptions are not public.

## Path A: token deploy (agency default)

```bash
# linked or not, VERCEL_TOKEN in env, team scope known
vercel deploy . --yes --scope <team>                  # preview; prints the URL
vercel deploy . --yes --scope <team> --no-wait        # don't block on build
vercel inspect <deployment-url> --scope <team>        # status; add --logs for build logs
```
- First deploy in an unlinked folder with `--yes` creates/links a project named after the folder; name the folder after the prospect (`peeters-uitvaart-mock`) before deploying.
- `VERCEL_ORG_ID` + `VERCEL_PROJECT_ID` in env (both) skip linking for an existing project.
- For scripted runs, parse output rather than guessing; use `--format json` where the installed CLI version supports it (check `vercel deploy --help`).
- **Production** (only on explicit request): `vercel deploy . --prod --yes --scope <team>`.

## Path B: git-connected project

If the folder has a git remote connected to Vercel: a push builds automatically. **Ask the user before committing and pushing.** Preview = any non-production branch; production = the production branch, so never push to it without an explicit request. Get the URL from `vercel ls --scope <team>`.

## Path C: temporary deploy (no account, no token)

For a quick look when no token is available (sandbox, first test):
```bash
npx vercel@<pinned-version> deploy . --temporary --yes
```
- Prints a temporary URL, a **claim URL** and an expiry. Treat the claim URL as a secret: give it only to the user, never put it in the outreach email or the page.
- Expires; not for links sent to prospects. Does not work in CI or in an already-linked folder.

## Domains and naming

- Use the generated `*.vercel.app` preview URL or an agency subdomain; never a domain that implies we own the prospect's brand.
- Do not add custom domains or env vars (`vercel domains add`, `vercel env add`) unless the user asks.

## Report back

URL, preview vs production, deployment status, whether `noindex` is active (meta + header), and the claim URL (Path C only, private).
