# Meta Ads weekly reviews

HiddenGem Marketing's three weekly Meta Ads reviews, run every Monday from Claude Code and tracked here.

| Workflow | Skill | Outputs |
|---|---|---|
| Ad spend check | `Ad Spends Checks/.claude/skills/ad-spend-check` | `Ad Spends Checks/Weekly Checks/YYYY-MM-DD-ad-spend-check.{md,csv,html}` |
| Pixel domain check | `Meta Pixel Reviews/.claude/skills/pixel-domain-check` | `Meta Pixel Reviews/Weekly Checks/YYYY-MM-DD-pixel-domain-check.{md,csv,html}` |
| Client benchmark (advanced setups) | `Client Benchmark Reviews (advanced setups)/.claude/skills/client-benchmark` | `Client Benchmark Reviews (advanced setups)/Weekly Checks/YYYY-MM-DD-client-benchmark.{md,csv,html}` |

`Project Data/PROJECT.md` is the source of truth for the project: data sources, rules, client maps, learnings, open decisions and the run log. `Project Data/CHANGELOG.md` records changes to the workflows.

## Weekly publish

```sh
python3 "Project Data/build_html.py" YYYY-MM-DD   # .md + .csv -> .html for each workflow
python3 "Project Data/build_site.py"              # rebuilds site/ (index + every dated page)
git add -A && git commit -m "Reviews YYYY-MM-DD" && git push
```

Netlify publishes `site/` on every push to `main`. Pages are marked `noindex`; the repo is private and the site should stay behind Netlify's password or team access, because the reports name clients, ad account IDs, pixel IDs and budgets.

## Site layout

- `/` — every review date, newest first, three cards per Monday
- `/ad-spend/YYYY-MM-DD.html`, `/pixel-domains/YYYY-MM-DD.html`, `/client-benchmark/YYYY-MM-DD.html`
- `/ad-spend`, `/pixel-domains`, `/client-benchmark` redirect to the latest page
