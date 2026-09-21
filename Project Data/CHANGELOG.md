# Changelog

Major changes to the Meta Ads Analysis project. Newest first. Small wording fixes don't go here; anything that changes what a workflow reads, how it scores, or where it writes does.

## 2026-09-21 (night)

- **Git repo + live archive.** Project folder pushed to private repo `hiddengem-webteam/meta-ads-weekly-reviews`. `Project Data/build_site.py` builds `site/` (index of every Monday's three reviews, dated pages, latest redirects); Netlify site `hg-ads-reviews` serves it at `https://hg-ads-reviews.netlify.app`. Each skill's last step now includes rebuilding the HTML and site, committing, pushing and deploying.
- **HTML reports added.** `Project Data/build_html.py` turns each workflow's dated `.md` + `.csv` into a `.html` in the same `Weekly Checks/` folder, styled from the HiddenGem Media design system (Untitled UI base: Inter, neutral grays, brand blue `#0066DE` accents, green/amber/red badges with dots in place of the ✅⚠️❌🔴 emoji, sentence case, dark mode). Wordmark copied to `Project Data/assets/hg-wordmark.svg`. All three W39 pages published as claude.ai artifacts; URLs in `PROJECT.md` section 4.4.
- **Reviewed the Cowork-era emails** (7 Sep spend + pixel audits, 31 Aug creative report). Findings not yet turned into decisions: sheet lost 5 clients and gained 2 between 7 and 21 Sep; Táberg at exactly 10% flipped ❌→✅ under the new rule; sister-account spend (Stay With Branch) flipped ❌→✅; Stay Southern Illinois flipped ❌→⚠️ on the same evidence; Tuxedo Falls pixel died ~1 Sep; the creative report is a fourth workflow with no skill yet.

## 2026-09-21 (evening)

- **Client Benchmark skill created** at `Client Benchmark Reviews (advanced setups)/.claude/skills/client-benchmark/SKILL.md` with `generate_report.py`. Decisions taken with Shawal in chat:
  - Decision Making table in the Benchmarks doc (`1KVMRJcmw6cVhHy7sj48vHRPJWNLid4tUiHTWOnkCFSE`) is the only source of state; per-type Investigate/Target/Strong values are diagnostics.
  - Scope is Lead Gen (MoF, CPL, 30d, $100 gate) and Sales/Retargeting (BoF, ROAS, 14d, $200 gate). IG Discovery / Keyword (ToF) spend is shown, not scored. Cost per follower parked.
  - ROAS alone sets the Retargeting state; frequency and cost per booking are notes.
  - Advanced list = CRM "Clients - Onboarding" tab, "Meta Ads" column = Advanced. Only CRM clients are scored.
  - No HG AI hand-off block. Shawal drops HG AI reports into `HG AI Reports/`; the skill summarises them per client.
  - Sales campaigns with an MoF/lookalike prefix are scored on the Retargeting ROAS bands (doc has no prospecting-sales band).
- **Folder `Monthly ROI data/` added** by Shawal (July and August ROI JSON). The benchmark report adds one ROI context line per client from these.
- **Folder `Client Benchmark Reviews (advanced setups)/HG AI Reports/` added** for HG AI diagnoses.
- **Meeting notes wired into Client Benchmark.** The skill fetches every "Meta Ads Strategy" and "Meta Ads Sync" calendar event since the previous run that has a "Notes by Gemini" attachment and reads the docs from Drive. Report gains a "Weekly Meta Ads meetings" section (Summary, Decisions, Next steps per meeting) and per-client "Meeting notes" lines from the Details sections, with an alias map for Gemini's misspellings. Resolves open decision 7; Fireflies not needed.
- **First Client Benchmark run**, saved and regenerated with the meeting section. Results in `PROJECT.md` run log.

## 2026-09-21 (later)

- **Pixel Domain Check skill created** at `Meta Pixel Reviews/.claude/skills/pixel-domain-check/SKILL.md`, ported from the Cowork "Pixel Domain Audit (Email)" brief with these changes:
  - No email step. Writes a dated `.md` report and `.csv` sidecar to `Meta Pixel Reviews/Weekly Checks/`.
  - Week-over-week diff on pixel ID, marking New / Still open / Fixed.
  - Expected domains read from `Meta Pixel Reviews/expected-domains.csv` instead of being re-inferred each run; rows carry `source` = sheet / confirmed / inferred.
  - Inventory reads the HiddenGem BM dataset listing first (covers MCP-disabled accounts), then per-account listings to see what is attached; dedupes the doubled rows the connector returns.
  - Totals come from `event_total_counts` (sum all rows); domains from the `host` aggregation. `ads_pixel_event_read` and `ads_get_dataset_details` dropped as uninformative.
  - Accepted secondary hosts spelled out: GHL, PMS booking engines (Cloudbeds, OwnerRez, Hospitable, Guesty, ResNexus, Newbook, holidayfuture, Uplisting), Wix static hosts, HG netlify staging, localhost, Linktree, facebook.com.
  - Inferred domains that contain the client's brand name are treated as confirmed; only non-brand inferred domains trigger ⚠️.
- **`Meta Pixel Reviews/expected-domains.csv` added**, 47 rows seeded from the first run, all `inferred` except Sunapee Stays (`sheet`).
- **First Pixel Domain Check run, saved.** Results in `PROJECT.md` run log. Two cross-contamination cases found.
- **PROJECT.md gained section 5.1** (client → pixel map) and open decisions 9 to 13; decision 6 resolved.

## 2026-09-21

- **Project started.** Three workflow folders created: Meta Pixel Reviews, Ad Spends Checks, Client Benchmark Reviews (advanced setups).
- **Decision: manual runs first.** Workflows run from VS Code, outputs saved to folders. Cloud scheduling deferred because cloud routines can't reach the Desktop. Supabase planned as the future store.
- **Decision: plain-text tables for now.** HTML email output deferred until the system is proven.
- **Ad Spend Check skill created** at `Ad Spends Checks/.claude/skills/ad-spend-check/SKILL.md`, ported from the Cowork "Weekly fb report" instructions with these changes:
  - No email step. Writes a dated `.md` report and `.csv` sidecar to `Ad Spends Checks/Weekly Checks/`.
  - Week-over-week diff on ad account ID, marking New / Still open / Fixed.
  - Fixed thresholds: ≤10% or ≤$5 match, 10–25% warning, >25% critical. Dark-account spend always critical.
  - Reads ad set budgets when a campaign has none (fixes Starlight Haven showing $0).
  - Converts lifetime budgets to a daily estimate; ignores campaigns past their stop time.
- **Folder `Weekly CSV Reports/` added** for Ads Manager exports. Skill renames drops to `YYYY-MM-DD_Www_meta-ads-report.csv`.
- **CSV fallback added to Ad Spend Check.** Blocked accounts (MCP disabled or not queryable) are scored from the weekly export instead of flagged red, marked "source: CSV export, not live". Sidecar gains a `source` column.
- **First Ad Spend Check run**, chat only, not saved. Results in `PROJECT.md` run log.
- **`Project Data/` folder added** with this changelog and `PROJECT.md`. Skill updates both at the end of each run.
