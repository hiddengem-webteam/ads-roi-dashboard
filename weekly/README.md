# Meta Ads weekly reviews

HiddenGem Marketing's three weekly Meta Ads reviews, run every Monday from Claude Code. This folder was the standalone `meta-ads-weekly-reviews` repo until 2026-10-15; it now lives inside the ROI dashboard so the weekly and monthly reports ship from one site.

| Workflow | Skill (repo root) | Outputs |
|---|---|---|
| Ad spend check | `.claude/skills/ad-spend-check` | `weekly/Ad Spends Checks/Weekly Checks/YYYY-MM-DD-ad-spend-check.{md,csv,html}` |
| Pixel domain check | `.claude/skills/pixel-domain-check` | `weekly/Meta Pixel Reviews/Weekly Checks/YYYY-MM-DD-pixel-domain-check.{md,csv,html}` |
| Client benchmark (advanced setups) | `.claude/skills/client-benchmark` | `weekly/Client Benchmark Reviews (advanced setups)/Weekly Checks/YYYY-MM-DD-client-benchmark.{md,csv,html}` |

Run the skills from the repo root (`/ad-spend-check`, `/pixel-domain-check`, `/client-benchmark`). `weekly/Project Data/PROJECT.md` is the source of truth: data sources, rules, client maps, learnings, open decisions and the run log. `weekly/Project Data/CHANGELOG.md` records changes to the workflows.

## Weekly publish

```sh
python3 "weekly/Project Data/build_html.py" YYYY-MM-DD   # .md + .csv -> .html for each workflow
python3 "weekly/Project Data/build_site.py"
npx tsx scripts/sync-roi-memory.mts   # push the new rows to the roi schema in Supabase              # rebuilds public/weekly/ (index + every dated page)
git add -A && git commit -m "Reviews YYYY-MM-DD" && git push
```

Netlify builds the dashboard on every push to `main`; the Next.js static export copies `public/weekly/` into `out/weekly/`, so the archive is served at `/weekly/` on the same site as the monthly ROI dashboard. Pages carry `noindex` (see the repo's `netlify.toml`). They name clients, ad account IDs, pixel IDs and budgets, so the site should stay behind Netlify's password or team access.

Local preview: `python3 "weekly/Project Data/serve_site.py"` then open http://127.0.0.1:8765/weekly/.

## Site layout

- `/weekly/` — every review date, newest first, three cards per Monday, with a link back to the monthly dashboard
- `/weekly/ad-spend/YYYY-MM-DD.html`, `/weekly/pixel-domains/YYYY-MM-DD.html`, `/weekly/client-benchmark/YYYY-MM-DD.html`
- `/weekly/ad-spend`, `/weekly/pixel-domains`, `/weekly/client-benchmark` redirect to the latest page

## Monthly ROI input

`weekly/Monthly ROI data/` holds one client-reporting JSON per month; the client benchmark reads it for ROI context. The dashboard's `scripts/export-<month>-client-reporting.mts` scripts now write it here directly, so there is no longer a copy step.
