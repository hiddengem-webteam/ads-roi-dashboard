# Changelog

Major changes to the Meta Ads Analysis project. Newest first. Small wording fixes don't go here; anything that changes what a workflow reads, how it scores, or where it writes does.

## 2026-10-07

- **September 2026 ROI file added** (`Monthly ROI data/September 2026 - Client Reporting (1).json`, 39 clients, Shawal 7 Oct). The benchmark generator now orders ROI months by calendar (July → August → September) instead of a July/August hard-coding, and appends the latest month's per-client `note` to the Monthly ROI line. The 2026-10-05 benchmark was regenerated and republished with the September context.

## 2026-10-06

- **Client Benchmark shows frequency on every Sales / Retargeting row and flags it above 5** (Shawal, 6 Oct: "add the frequency for the sales campaigns, flag it if it's going above 5"). `generate_report.py` adds a Frequency column to the per-client tables (14-day live value, impressions / reach for CSV rows, `—` on Lead Gen), marks values above 5.0 with ⚠️, adds a "Frequency watch" section after Scale candidates and a count in the header table, and writes `frequency` + `freq_flag` to the sidecar. States are unchanged: ROAS alone still sets them. `build_html.py` renders the new column, section and stat tile and still reads older reports without the column. The 2026-10-05 report was regenerated and republished.

## 2026-10-05

- **Week 41 run of all three reviews** (5 Oct): reports, sidecars, HTML and the Netlify archive published. Benchmark generator now resolves `ROOT` from its own location (the project moved to `HG - Github Stuff/meta-ads-weekly-reviews`), names a CSV row whose purchases carry no conversion value instead of showing a bare 0.0x ROAS, and strips Gemini's section breaks from the per-client meeting lines. Spend check: an UNSETTLED account (Asheville) is scored from the CSV with $0 active and flagged ❌ with the payment issue named; a stalled-delivery account (Stay With Branch) is raised ⚠️ on judgement and the footer says so.
- **Client Benchmark CSV fallback now carries the frequency diagnostic** (Shawal, 5 Oct: keep a check on retargeting frequency). `generate_report.py` aggregates the export's Reach column alongside Impressions and derives campaign frequency as impressions / reach (approximate where ad sets overlap in audience), so CSV-scored Sales / Retargeting rows get the same "freq > 3.0" diagnostic as live rows. Reach and Frequency are now required columns in the weekly export; the W41 export (28 Sep – 4 Oct) already has them. States are unchanged: frequency stays a diagnostic.

## 2026-09-28

- **Big Moon Ranch offboarded** (Shawal, 28 Sep). The W40 🔴 for the missing account is closed; the spend check treats a sheet row for an offboarded client as ⚠️ sheet housekeeping, not a blocker. Ad-spend skill and section 5 maps updated.
- **Actions log added** (`PROJECT.md` section 9). Shawal reported the day's account changes after the W40 run (CGG new lead campaign, Selah payment error and planned budget move, Ridge & Falls lead relaunch planned, Tàberg new Broad campaign at $50 and Lookalike cut to $50, pixel contamination blocked). Each was checked against the connector and logged as Done / Planned / Reported with what next week's diff should see. The three skills' diff steps now read the log.
- **Week 40 run of all three reviews** (28 Sep): first week-over-week diffs. Reports, sidecars, HTML, artifacts and the Netlify archive published.
- **Client Benchmark generator now diffs against the previous sidecar** (`campaign_id` for live rows, client + campaign for CSV rows): "Status vs last week" and "Change vs last week" columns, `diff_status` / `weeks_open` in the CSV, a "Removed since last week" line, and per-client HG AI one-liners read from `HG AI Reports/`. The Advanced list is rebuilt from the CRM download each run (24 clients, 21 mapped); Gemini docs titled "Meta Ads x HiddenGem AI Sync" are included. CSV-fallback rows honour the export's new Campaign delivery column.
- **Ad Spend Check uses the export's delivery columns.** Only campaigns with Campaign delivery = active count toward the CSV budget total; the "provisional" marker is dropped. Skill text updated.
- **Pixel check learning:** when a client's attached pixel is silent, check the HG BM listing for another dataset under the same client business before calling the client untracked (Tuxedo Falls). Skill text updated; `expected-domains.csv` gained the Tuxedo "Website" pixel row.

- **HG AI Reports folder moved to the project root.** Shawal had created a top-level `HG AI Reports/` and was looking there; the nested copy under the benchmark folder is removed and the skill reads the root folder. First three notes (Stay Saluda, Paradise Pointe, Táberg Falls, HG AI chats of 2026-09-23) transcribed from screenshots and saved there.

## 2026-09-23

- **Client Benchmark scores live campaigns only.** Shawal's ruling: a paused campaign has already been acted on, so it must not drive Flag / Review. `generate_report.py` and the skill now skip any campaign whose `effective_status` is not ACTIVE, list it under the client as "Paused in window, not scored" with spend, results and governing value, and keep it out of Action needed and the counts. The 2026-09-21 report and sidecar were regenerated under the rule (both former Flag rows were paused campaigns; Flag count is now 0). HTML report, claude.ai artifact and the Netlify archive republished.
- **Action needed order:** Sales and Retargeting campaigns first, then Lead Gen; within each Flag before Review, highest spend first. Same order for Scale candidates. Applied to the generator, the skill, the HTML builder and the saved 2026-09-21 report.
- **Local preview server** added at `Project Data/serve_site.py` (no-cache, port 8765).

## 2026-09-21 (night)

- **Git repo + live archive.** Project folder pushed to private repo `hiddengem-webteam/meta-ads-weekly-reviews`. `Project Data/build_site.py` builds `site/` (index of every Monday's three reviews, dated pages, latest redirects); Netlify site `hiddengem-ads-reviews` (team hgwebteam) serves it at `https://hiddengem-ads-reviews.netlify.app`. Each skill's last step now includes rebuilding the HTML and site, committing, pushing and deploying.
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
