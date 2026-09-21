# Meta Ads Analysis — Project File

Owner: Shawal (HiddenGem Marketing)
Started: 2026-09-21
Status: building. All 3 workflows runnable as plain-text reports; each had its first saved run on 2026-09-21. HTML versions of all three W39 reports published as claude.ai artifacts on 2026-09-21 (section 4.4).

This file is the single source of truth for the project. Claude updates it at the end of every workflow run: the Run Log gets a new row, Learnings gets anything new, Open Decisions gets resolved or added to. Major changes also go in `CHANGELOG.md`.

---

## 1. Purpose

Three weekly Meta Ads review workflows, run manually from VS Code (Claude Code), each saving a dated plain-text report to its own folder and comparing against the previous week's report to show what was fixed and what is still open.

Long-term: automate with Supabase as the store, then move to HTML email output. Not before the manual system is proven.

## 2. Folder layout

```
Meta Ads Analysis - 21:09:26/
├── Project Data/                     this file + CHANGELOG.md + build_html.py (HTML report builder) + assets/hg-wordmark.svg
├── Weekly CSV Reports/               Ads Manager exports, one per week, dated filename
├── Ad Spends Checks/
│   ├── .claude/skills/ad-spend-check/SKILL.md   the runnable skill (/ad-spend-check)
│   └── Weekly Checks/                dated reports (.md) + sidecar (.csv), one pair per run
├── Meta Pixel Reviews/
│   ├── .claude/skills/pixel-domain-check/SKILL.md   the runnable skill (/pixel-domain-check)
│   ├── expected-domains.csv          source of truth for each client's expected domains (seeded 2026-09-21, all inferred)
│   └── Weekly Checks/                dated reports (.md) + sidecar (.csv), one pair per run
├── Monthly ROI data/                 monthly ROI JSON per month (Shawal drops these in; July + August 2026 so far)
└── Client Benchmark Reviews (advanced setups)/
    ├── .claude/skills/client-benchmark/SKILL.md   the runnable skill (/client-benchmark) + generate_report.py
    ├── HG AI Reports/                HG AI diagnoses Shawal drops in, client name in filename
    └── Weekly Checks/                dated reports (.md) + sidecar (.csv), one pair per run
```

Convention: each workflow folder holds its own hidden `.claude/skills/<name>/SKILL.md` and a `Weekly Checks/` folder for outputs. Report filenames are `YYYY-MM-DD-<workflow>.md` with a matching `.csv`, plus a `.html` built from both by `Project Data/build_html.py`. CSV exports are `YYYY-MM-DD_Www_meta-ads-report.csv`.

## 3. Data sources

| Source | Location | Used for |
|---|---|---|
| HiddenGem Master Meta Ads sheet | Google Sheet `1B6lWqp_0linzf-3n4iqjJbavidZvyLO5yTY3MDhzYaM`, tab "Meta Ad Links" | Client list, Status (Live / Not Live / Paused), Total Budget ($/day), Comments |
| CRM - HiddenGem Media | Google Sheet `1oEUngQE3ZXc6U4ciRkkg55UrlR-M065kTmCzG8HFhM4` | Account manager per client. Tab priority: Management Clients, then the "#, Account Manager, Client, Priority" tab, then the Content tab (Client, MA, AM), then Mastermind |
| Meta Ads connector (claude.ai) | `ads_get_ad_accounts`, `ads_get_ad_entities`, `ads_get_field_context` | Live budgets and 7-day spend. 112 ad accounts visible across 3 pages |
| Weekly Ads Manager export | `Weekly CSV Reports/` | Fallback for accounts the connector cannot read |
| Meta datasets (pixels) | `ads_get_datasets` (business `158693423705448` + per account), `ads_get_dataset_stats` (host, event_total_counts), `ads_get_dataset_quality` | Pixel inventory, sending domains, 7-day event totals, EMQ. 73 datasets visible in the HG BM |
| Expected domains | `Meta Pixel Reviews/expected-domains.csv` | Per client/pixel: expected domains, accepted extra hosts, source (sheet / confirmed / inferred) |
| Benchmarks doc | Google Doc `1KVMRJcmw6cVhHy7sj48vHRPJWNLid4tUiHTWOnkCFSE` | Decision Making table (states per CPL / ROAS band), per-type Investigate lines, windows and gates for workflow 3 |
| CRM "Meta Ads" column | CRM sheet, tab "Clients - Onboarding" (header says "Management Clients"), column R | Basic / Advanced. Advanced = in scope for workflow 3 (16 clients on 2026-09-21) |
| Monthly ROI data | `Monthly ROI data/*.json` | Per client per month: Meta spend, Meta-attributed bookings, blended ROAS, retargeting ROAS, new-leads CPL. Revenue is from the Client Performance Tracking sheet, not the pixel |
| Weekly Meta Ads meeting notes | Google Calendar events "Meta Ads Strategy" (Dustin, Wed 1–2pm ET) and "Meta Ads Sync" (Dustin, Thu 11–11:30am ET), each with a "Notes by Gemini" attachment → Google Doc, read via Drive. Latest: `1Hoq1JUk1tFxSCUeYexeEELfVSZwTq7eJ2Pi_NvVDF4A` (Strategy 2026-09-16), `1oMlKzZdFQxYCXKMiFnaG-2ews_EkudXgG0zivvI2l1c` (Sync 2026-09-17) | Workflow 3 "Weekly meetings" section (Summary, Decisions, Next steps per meeting) and per-client mentions from the Details sections. Alias map in the generator handles Gemini misspellings |
| Campaign insights | `ads_get_ad_entities` level campaign, `last_30d` and `last_14d`, fields `lead`, `cost_per_lead`, `omni_purchase`, `cost_per_omni_purchase`, `purchase_roas`, `cpm`, `ctr`, `cost_per_link_click`, `frequency` | Workflow 3 governing metrics and diagnostics |
| Local scratch | Claude's session scratchpad | Sheet parsing, never the project folders |

Not connected: Mailtrap (email sending), Fireflies (meeting summaries), Instagram Graph API (organic data).

## 4. Workflows

### 4.1 Ad Spend Check — built, `/ad-spend-check`

Compares the documented daily budget on the Master sheet against the live daily budget in each client's ad account. Every client on the sheet is checked, including Not Live and Paused, because spend on a dark account is the most important thing this report catches.

Flags:

| Flag | Rule |
|---|---|
| ✅ Match | Live and within 10% or $5; or Not Live/Paused with zero active budget and under $5 spend in 7 days |
| ⚠️ Warning | Live and 10–25% off; or no documented budget; or duplicate accounts; or lifetime-budget estimate; or a sheet Comment that changes the expected figure |
| ❌ Critical | Live and more than 25% off; or any active budget or ≥$5 7-day spend on a Not Live/Paused account |
| 🔴 Blocker | MCP disabled, not queryable, or account not in the list, AND not in this week's CSV export |

Budget reading: campaign `daily_budget` where set; otherwise sum of active ad set `daily_budget` (non-CBO accounts); lifetime budgets converted to a daily estimate. 7-day `amount_spent` / 7 is a sanity check. Campaigns past their `stop_time` are ignored even if status says ACTIVE.

Week-over-week: joins on ad account ID against the previous `.csv` sidecar, marks New / Still open (with week count) / Fixed.

Output: `Ad Spends Checks/Weekly Checks/YYYY-MM-DD-ad-spend-check.md` and `.csv`. Report order: header counts, Issues with next actions, Fixed since last week, All accounts (alphabetical, strict A→Z), footer.

CSV fallback: for blocked accounts only. Reads the newest `Weekly CSV Reports/*_meta-ads-report.csv`, groups by campaign, counts campaign budget once or sums ad set budgets, marks the row "source: CSV export, not live". Provisional while the export lacks delivery columns.

### 4.2 Pixel Domain Check — built, `/pixel-domain-check`

Verifies each client's Meta Pixel receives events only from that client's own site, link pages, GHL funnel and booking engine; flags cross-contamination (another client's domain firing into a pixel), silent or low-volume pixels, and split or duplicate pixel setups. Ported from the Cowork "Pixel Domain Audit (Email)" brief with the email step removed.

Flags:

| Flag | Rule |
|---|---|
| ✅ Match | Events > 0 and every sending host is the client's own domain or an accepted secondary (GHL, PMS booking engine, Wix static host, HG netlify staging, dev hosts) |
| ⚠️ Warning | Zero/very low events on a Live client; main site absent (only bio or booking engine firing); funnel split across two live pixels; two pixels double-counting; pixel not shared to the ad account; sheet says CAPI but no server events; expected domain inferred and not brand-named; minor unknown host |
| ❌ Critical | Any host belonging to another sheet client, or a meaningful share from a domain that clearly isn't the client's. Offending domain named |
| 🔴 Blocker | No pixel found anywhere, or pixel unreadable |

Reading: HG BM dataset listing first (covers MCP-disabled accounts too), then per-account listings to see what is attached. Domains from `host` aggregation; totals from `event_total_counts` (sum every row). Expected domains from `expected-domains.csv`.

Week-over-week: joins on pixel ID against the previous `.csv` sidecar.

Output: `Meta Pixel Reviews/Weekly Checks/YYYY-MM-DD-pixel-domain-check.md` and `.csv`. Report order: header counts, Critical issues (with cross-contamination callout), Warnings, Fixed since last week, All pixels (alphabetical, strict A→Z), footer.

### 4.3 Client Benchmark Review (advanced setups) — built, `/client-benchmark`

Scores every Lead Gen (MoF) and Sales / Retargeting (BoF) campaign of each CRM-Advanced client against the Benchmarks doc, adds monthly ROI context, and saves a dated report. Built 2026-09-21 after a one-question-at-a-time session with Shawal; decisions recorded in the skill and CHANGELOG.

Scope: clients with Meta Ads = Advanced in the CRM (16 on 2026-09-21). Only CRM clients are scored. IG Discovery / Keyword (ToF) campaigns are shown as a spend line, not scored; cost per follower is parked.

States (Decision Making table, lower bound inclusive):

| State | Lead Gen CPL (30d, $100 gate) | Sales / Retargeting ROAS (14d, $200 gate) | Action in doc |
|---|---|---|---|
| Scale w/ HG AI | < $0.30 | > 15x | Full context to HG AI, it picks which campaign gets budget |
| Healthy | $0.30–0.50 | 8–15x | No change |
| Monitor | $0.50–1.00 | 5–8x | Watch next window |
| Review w/ HG AI | $1.00–2.50 | 2–5x | HG AI diagnoses |
| Flag to Shawal | ≥ $2.50 or no leads | < 2x or no purchases | Manual review, likely setup / technical |

Classification is by objective (OUTCOME_LEADS → Lead Gen; OUTCOME_SALES → Retargeting if the name says BoF / Retarget, else MoF lookalike sales, scored on the same ROAS bands). Frequency, cost per booking, CPC, CPM and CTR are diagnostics only. Paused campaigns that spent in the window are scored and marked. MCP-disabled accounts fall back to the weekly CSV export (21-day window, provisional). No HG AI hand-off block; Shawal drops HG AI reports into `HG AI Reports/` and the skill summarises them per client.

Output: `Client Benchmark Reviews (advanced setups)/Weekly Checks/YYYY-MM-DD-client-benchmark.md` and `.csv` (one row per campaign, keyed on campaign ID). Report order: header counts, last Meta Ads Strategy meeting (Gemini notes: summary, decisions, next steps), Action needed (Flag then Review), Scale candidates, per-client sections ordered by scored spend (each with a Monthly ROI line, a Meeting notes line and an HG AI notes line), footer.

Next: week-over-week diff in `generate_report.py` (currently hardcodes "First run").

### 4.4 HTML reports — built 2026-09-21

`Project Data/build_html.py [YYYY-MM-DD]` reads each workflow's dated `.md` and `.csv` and writes a dated `.html` beside them, styled from the HiddenGem Media design system (`https://claude.ai/artifact/GXb4YMfP8uFmoTPhnWujSk`: Inter, neutral canvas, brand blue for accents only, semantic badges instead of emoji, sentence case, light and dark themes). Each page: masthead with wordmark, stat row, alert callouts for critical findings, filterable tables, per-client cards (benchmark), footer notes. Published as private artifacts; republish to the same URL to keep the link:

| Workflow | Artifact URL (W39, 2026-09-21) |
|---|---|
| Ad spend check | https://claude.ai/artifact/8v1ecvQnHougDxjspvuB66 |
| Pixel domain check | https://claude.ai/artifact/PvVhNRBCtnniJGzsehkTWf |
| Client benchmark | https://claude.ai/artifact/HFu3dZGrVBK9zHuYBu9qJ4 |

Open: one stable URL per workflow (overwrite weekly) or one artifact per week. Email delivery (Mailtrap) not wired yet.

## 5. Client → ad account map (as of 2026-09-21)

All 42 sheet clients matched by name. The sheet's "Ads Account Link" column exports as the word "Acc" with no URL, so IDs below are the reliable key.

| Client (sheet) | AM | Ad account | ID | Connector |
|---|---|---|---|---|
| American River Resort | Nicole | American River Resort | 953162737054331 | ok |
| Asheville River Cabins | Charlotte | Asheville River Cabins Ads | 615836588009747 | ok |
| Away2PA | Alicia | Away2Pa | 603977626130795 | ok |
| Awayframes | Alicia | Awayframes Ad Account | 2471256056603833 | ok |
| Best Texas Travel | Nicole | Best Texas Travel Ad Account | 1982551189319458 | ok |
| Big Moon Ranch | Charlotte | Big Moon Ranch | 758851247064974 | MCP disabled → CSV |
| Bison Ridge Retreat | Chiara | Bison Ridge Retreat Ad Account | 950241787963535 | MCP disabled → CSV |
| Canopy at Moody Moon Ridge | Alicia | The Canopy At Moody Moon Ridge | 1293707265980102 | ok. Second account "Moody Moon Ridge" (Sue Hough) 1061646495537777 is MCP disabled |
| Columbia Gorge Getaways | Chiara | CGG | 490940113157881 | ok |
| Endless Stays | Nicole | Endless Stays | 896372356081479 | MCP disabled → CSV |
| Evergreen Cabins | Nicole | Evergreen Cabins Ads | 453808647114273 | ok |
| FLOHOM | Makenna | FLOHOM Ads | 2100710320122219 | ok |
| Green Springs Inn | Alicia | Green Springs Inn | 1390516335151357 | ok |
| Hiawassee Glamping | Alicia | Hiawassee Glamping | 4219624811692502 | ok |
| Home Base | Charlotte | Home Base bnbs | 3224125791099903 | ok |
| Inspired Retreats | Makenna | Inspired Retreats Ads 2.0 (under HG Marketing BM) | 1494841894957652 | ok. Original client account 2807065489488604 is CLOSED |
| Little River Landing | Makenna | Little River Landing | 884285717873613 | ok |
| Myrinn | Charlotte | Myrinn - Ad Account 2.0 (under HG Marketing BM) | 1668286333836716 | ok |
| Nature Nooks | Kristal | Nature Nooks Ad Account | 1796752774213285 | ok |
| North Star Resort & Lodge | — | North Star Lodge & Resort Ads | 2003562593933799 | ok. No AM in CRM |
| Oak & Ember | Chiara | Oak & Ember Ad Account | 831762063342909 | ok |
| Paradise Pointe | Makenna | Paradise Pointe Ads | 1585826092078255 | MCP disabled → CSV |
| Parker Reserve | Nicole | Parker Reserve | 1002927148609804 | ok |
| Ponderosa Pines Resort | Anna | Ponderosa Pines Resort | 1058846326445255 | MCP disabled → CSV |
| Raven Rock Mountain | Anna | Raven Rock Mountain Ad Account | 1065186195582056 | ok |
| Red White & Blue Views | Nicole | Red White & Blue Views | 1419930382946246 | ok |
| Ridge & Falls | Makenna | Ridge & Falls ad account | 1313401330776046 | ok |
| Selah Place | Alicia | Selah.place | 1275283434220508 | ok |
| Starlight Haven - Hot Springs | Charlotte | Starlight Haven Hot Springs | 901138032027913 | ok, ad set budgets |
| Starlight Haven - Weiss Lake | Charlotte | Starlight Haven Weiss Lake | 74756899 | ok, ad set budgets |
| Stay on 30a | Charlotte | Stay on 30a Ads | 25640434272252212 | ok. Legacy "[NOT IN USE] Stay on 30A" 908452332132644 under HG BM, MCP disabled |
| Stay Saluda NC | Makenna | Stay Saluda Ads | 1863632561215857 | ok |
| Stay Southern Illinois | Chiara | Southern Illinois Cabins Ads | 1661949078036229 | ok |
| Stay With Branch | Charlotte | @staywithbranch | 1269399754049770 | ok. Separate "Branch Berkeley Springs" 1517541906010284 exists, not on sheet |
| StayLuxe | Nicole | Stay Luxe Ads | 25033578722931437 | ok |
| Sunapee Stays | Charlotte | Sunapee Stays Ads Account | 651114096215889 | ok |
| Taberg Falls | Alicia | Táberg Falls | 827872700004659 | ok |
| The Cohost Company | Makenna | The Cohost Company Ads | 9141035462679902 | ok |
| The Outpost | Ananya | The Outpost Grand Canyon | 1530849534802936 | ok |
| Three Suns Cabins | Anna | Three Suns Cabins Ad Account | 1210218584137342 | ok |
| Treetop Escapes | Makenna | Treetop Escapes Ads | 967636478877602 | ok |
| Tuxedo Falls | Chiara | Tuxedo Falls - Ad Account | 2077151009889326 | ok |

Active accounts with spend but no sheet row: Hillside Amble (Anna), Cowan Creek Lodges (Anna), Edenwood NC (Charlotte), Stay Different (Anna), Branch Berkeley Springs. Decision pending on whether to add them.

### 5.1 Client → pixel map (as of 2026-09-21)

Primary pixel per client, plus live secondaries. Full domain expectations live in `Meta Pixel Reviews/expected-domains.csv`.

| Client | Pixel (name → ID) | Owner | Notes |
|---|---|---|---|
| American River Resort | American River Resort - Meta Pixel → 2862601447415133 | HG BM | |
| Asheville River Cabins | Asheville River Cabins Meta Pixel → 1634367080775220 | client BM 3440656856064841 | browser only |
| Away2PA | Away 2PA Meta Pixel → 772693422494226 | HG BM | |
| Awayframes | Awayframes - Meta Pixel → 773898245792839 | HG BM | |
| Best Texas Travel | Best Texas - Meta Pixel → 4108409325970216 | HG BM | |
| Big Moon Ranch | Big Moon Ranch - Meta Pixel → 1208874174466414 | HG BM | account MCP-disabled, pixel readable |
| Bison Ridge Retreat | Bison Ridge - Meta Pixel → 1241959234316508 | HG BM | account MCP-disabled, pixel readable |
| Canopy at Moody Moon Ridge | Moody Moon Pixel Main → 861460105842405 | client BM 1798221880199326 | |
| Columbia Gorge Getaways | Columbia Gorge Getaways Pixel → 700947282709400 (primary); CGG Pixel → 595257656540749 (Wix embed only) | client BMs | two live pixels |
| Endless Stays | Endless Stays Meta Pixel → 876508505381758 | HG BM | account MCP-disabled, pixel readable |
| Evergreen Cabins | Evergreen Cabins Meta Pixel → 1474685406530880 | client BM 182684855965772 | |
| FLOHOM | FLO2 Conversion → 139231105894533 | client BM 873976399912644 | FLO1 Conversion, FLO2 never fired |
| Green Springs Inn | GSI - Wix Pixel → 1098954801239133 (primary); Green Springs Inn Event Data → 1602971745164199 (booking engine only) | client BM 168139003880292 | double-counts book.* |
| Hiawassee Glamping | Hiawassee Meta Pixel → 1149628220675980 | HG BM | Event Data pixel never fired |
| Home Base | Home Base Bnb - Meta Pixel → 1467511861488785 | HG BM | |
| Inspired Retreats | Inspired Retreats Meta Pixel → 1547510566197386 | HG BM | contaminated by Stay Saluda GHL pages |
| Little River Landing | Little River Landing Meta Pixel → 1816709606431185 | client BM 1764967091370111 | contaminated by North Star GHL pages |
| Myrinn | Myrinn - Meta Pixel → 1943632852972363 | HG BM | |
| Nature Nooks | Nature Nooks - Meta Pixel → 844302611320158 | HG BM | Event Data pixel never fired |
| North Star Resort & Lodge | North Star Lodge Killington - Meta Pixel → 3440147309499983 (attached, site only); Northstar Meta Pixel → 1904436107168032 (HG BM, Cloudbeds + GHL) | split | decide canonical |
| Oak & Ember | Oak & Ember - Meta Pixel → 1729106025177871 | HG BM | Event Data pixel never fired |
| Paradise Pointe | Paradise Pointe - Pixel → 707016175006193 | client BM 1087116839728915 | account MCP-disabled, pixel readable |
| Parker Reserve | Parker Reserve - Pixel → 1188475652520634 | HG BM | |
| Ponderosa Pines Resort | Ponderosa Pines Resort - Meta Pixel → 1293211539656211 | HG BM | account MCP-disabled, pixel readable |
| Raven Rock Mountain | Raven Rock Meta Pixel → 1359649962298380 | HG BM | NOT shared to ad account 1065186195582056 |
| Red White & Blue Views | Red White & Blue - Meta Pixel → 1625871301864243 | HG BM | |
| Ridge & Falls | Ridge & Falls - Meta Pixel → 1332286819018269 | client BM 1887518261927124 | HG BM copy 2059709192087667 never fired |
| Selah Place | Selah.Place Event Data → 1235173718368839 (primary); LinkTree → 3327546500757583 | client BM 1662038040809917 | Selah 2026 Pixel never fired |
| Starlight Haven (Hot Springs + Weiss Lake) | Starlight Haven Pixel - ResNexus → 766226461367996 | client BM 735291970494853 | one pixel, two accounts, browser only |
| Stay on 30a | Stay on 30a - Meta Pixel → 1464927198465632 | HG BM | |
| Stay Saluda NC | Stay Saluda - Meta Pixel → 4250460185185664 | HG BM | |
| Stay Southern Illinois | Southern Illinois Cabins - Meta Pixel → 1328561309169535 | HG BM | multi-brand domains |
| Stay With Branch | Branch → 1107997340818783 | client BM 2066827277052066 | Business Meta Pixel dead since May 2026 |
| StayLuxe | StayLuxe Meta Pixel → 4293491110916917 | HG BM | |
| Sunapee Stays | sunapeestays's Pixel → 471248637966769 | client BM 1296150947517054 | |
| Taberg Falls | Taberg Falls - Meta Pixel → 964214909847907 | HG BM | 5 other clients' pixels also shared into this account |
| The Cohost Company | The Cohost Company Meta Pixel → 638998632168952 | client BM 500895838996853 | |
| The Outpost | HG - The Outpost Grand Canyon Event Data → 1691591692267740 (bio only); Outpost Grand Canyon → 734783866381382 (site + Newbook, client BM) | split | decide canonical |
| Three Suns Cabins | Three Suns Cabins - Pixel → 691977289952800 | HG BM | bio subdomain only |
| Treetop Escapes | Treetop Escapes - Pixel → 1178838797064774 | client BM 1190724359426537 | |
| Tuxedo Falls | Tuxedo Falls - Ad Account's Pixel → 1561325308991270 | client BM 1400770510587476 | silent since 1 Sep 2026 |

## 6. Learnings

Things that were not obvious and change how the workflows are built or run.

- **Cloud routines can't reach the Desktop.** `/schedule` runs in Anthropic's cloud, so folder-based outputs need manual runs from VS Code. Automation later means moving storage to Supabase or Drive.
- **Google Drive sheet reads are large.** Both sheets exceed the tool output limit and get saved to disk. Parse them locally with Python rather than reading in chunks. The sheet comes back as Markdown pipe tables, one table per tab, tabs separated by blank lines.
- **The Master sheet's account links don't export.** The "Ads Account Link" column shows "Acc" with no URL. Matching is by name and worked for all 42, but the ID map in section 5 is the durable key.
- **CRM has AMs in five tabs with inconsistent client names.** Management Clients is the primary. Some clients (Best Texas, Columbia Gorge, Little River Landing, Oak & Ember, Ridge & Falls, Selah, Sunapee, The Outpost, Tuxedo Falls) only appear in the Content tab. Names vary ("Stay On 30A" vs "Stay on 30A", "Red, White & Blue Views", "Nature Nooks Acadia").
- **Two accounts hold budgets at ad set level**: both Starlight Haven accounts. A campaign-only read shows them as $0. Always fall through to ad sets when a campaign has no budget.
- **Old boosted posts stay ACTIVE forever.** Selah Place (70+), The Outpost (4) and Green Springs (1) have boosted-post campaigns with status ACTIVE but a `stop_time` months in the past. They don't spend. Exclude anything past its stop time.
- **The Meta connector's IG tools are boost-only.** No organic comments, engagement or views. Organic data needs the Instagram Graph API with `instagram_manage_insights`, or a third-party aggregator.
- **The Ads Manager export has no status column.** Month-to-date exports include paused and recreated campaigns, so budget totals overstate what's live (Stay on 30a: CSV $500 vs live $450). Fix: add Campaign delivery / Ad set delivery columns and export last 7 days.
- **The CSV catches things the live read misses.** Canopy at Moody Moon Ridge spent ~$1,500 in 1–21 Sep but had zero active campaigns on 21 Sep. A live-only check shows "nothing running"; the export shows it was running until days ago.
- **Threshold sensitivity on small accounts.** A $10 difference on a $30 account is 33% and reads as Critical. Decision pending on a dollar floor.
- **Meta connector calls need a shared `client_conversation_id`** across a run and return budgets as formatted strings ("$30.00 USD"), not cents, despite the API docs.
- **The HG BM dataset listing covers almost every client pixel**, including pixels of MCP-disabled accounts, because clients share their pixels into the HG BM. Stats on those pixels work even when the ad account itself is blocked.
- **`ads_get_datasets` returns every dataset twice** (pixel row + wrapper row with a 1970 `last_fired_time`). Dedupe on ID, keep the latest timestamps.
- **`event_total_counts` rows for one event sum to that event's total.** Sum all rows for total events. `host`/`event` aggregations are hourly only and too long to sum by hand.
- **The Master sheet has no website domain column.** Expected domains live in `Meta Pixel Reviews/expected-domains.csv`, seeded from brand names and observed traffic; treat brand-named domains as confirmed, others as "inferred, confirm".
- **GHL funnel cloning leaks pixel IDs.** Both cross-contamination cases found on 2026-09-21 were another client's `go.` GHL subdomain firing into a pixel, one-way. Check the GHL sub-account tracking settings first.
- **Booking engines push events in bursts** (book.* hosts, holidayfuture, ResNexus): 1k to 18k events in a single hour. Weekly totals on those pixels are not comparable to page-view-only pixels.
- **Several clients run two live pixels** (Columbia Gorge, Green Springs, Selah, North Star, The Outpost) with the funnel split or double-counted between them.
- **The Benchmarks doc contradicts itself.** Summary table vs per-type sections disagree on the IG Discovery Scale line ($0.20 vs $0.30), the Retargeting gate ($200 vs $500), and Investigate lines that sit inside "no change" bands (ROAS 8.3x, CPL $0.80). Resolved 2026-09-21: Decision Making table wins, $200 gate, per-type values are notes only.
- **Meta insights have no purchase value field in the connector**; `purchase_roas` × spend gives it. `omni_purchase` is the purchase count, `lead` the lead count. `ctr` is all-clicks CTR, not link CTR.
- **HG campaign naming carries the funnel stage** (ToF / MoF / BoF prefix) and objectives line up with it in 155 of 156 campaigns, so objective-first classification works without a lookup table. "MoF - Lookalike Sales" campaigns optimise for purchases and have no band of their own in the doc.
- **The CRM "Clients - Onboarding" tab has a Meta Ads Basic / Advanced column** that defines workflow 3 scope. The Drive export truncates that table at Oak & Ember; rows below (The Outpost, Selah Place and later) only appear in other tabs, so check the tab in the browser when the list looks short.
- **Monthly ROI JSON ROAS is not pixel ROAS.** Revenue there is from the Client Performance Tracking sheet and bookings are Meta-attributed via link-in-bio / promo code / UTM, so it runs lower than `purchase_roas` (Tàberg: 4.5x blended August vs 8.2x pixel 30d).
- **Gemini misspells client names in meeting notes** ("Flow Home", "Tabber", "Tabber Falls"). Matching needs an alias list, kept in the generator's `ALIASES` map.
- **Gemini meeting notes are reachable without Fireflies.** The "Meta Ads Strategy" calendar event carries the "Notes by Gemini" Google Doc as an attachment (owner Dustin, shared to Shawal). The doc has Quick notes, Full notes (Summary / Decisions / Next steps / Details) and a Transcript; the Full notes sections parse cleanly, the transcript is noise. The word "Transcript" also appears in a link near the top, so cut at the transcript heading, not the first occurrence.
- **Canopy at Moody Moon paused everything after five Sales campaigns ran at 0.15x to 0.47x ROAS with $71 to $94 CPMs** in Aug–Sep. That is a setup problem, not a creative one, and is why the spend check saw zero live budget.

## 7. Open decisions

| # | Question | Options | Status |
|---|---|---|---|
| 1 | Dollar floor before Critical on small accounts? | Keep pure % rule / add $15 floor | Open |
| 2 | Add the five unlisted active accounts to the Master sheet? | Yes / No / some | Open |
| 3 | Add account IDs to the Master sheet? | Recommended | Open |
| 4 | Ads Manager saved report: add delivery columns, last 7 days | Recommended | Open, Shawal to change the saved report |
| 5 | AM for North Star Resort & Lodge | Add to CRM | Open |
| 6 | Where does the expected pixel domain per client live? (workflow 2) | Sheet column / file in folder | Resolved 2026-09-21: `Meta Pixel Reviews/expected-domains.csv`, seeded from run 1 with `source=inferred`; Shawal flips rows to `confirmed` |
| 7 | Source and format for weekly ads meeting summary (workflow 3) | Fireflies connector / pasted file | Resolved 2026-09-21: Gemini "Notes by Gemini" docs attached to the weekly "Meta Ads Strategy" and "Meta Ads Sync" calendar events, fetched automatically via the Calendar + Drive connectors. No manual step |
| 8 | Definition of "advanced setup" for workflow 3 filter | | Resolved 2026-09-21: CRM "Clients - Onboarding" tab, Meta Ads column = Advanced |
| 14 | Cost per follower source for IG Discovery scoring (Ads Manager follows result / IG follower delta / cost per profile visit proxy) | | Parked 2026-09-21: ToF not scored in v1 |
| 15 | Do "MoF - Lookalike Sales" campaigns get their own ROAS band, or stay on the Retargeting bands? | Add a band to the doc / keep | Open, currently scored on Retargeting bands |
| 16 | Benchmarks doc: reconcile the summary table with the per-type sections (IG Scale $0.20 vs $0.30, gate $200 vs $500, Investigate lines inside Monitor bands) | Edit the doc | Open, skill uses the Decision Making table |
| 17 | The Drive export of the CRM cuts the Clients - Onboarding table at Oak & Ember; any Advanced clients below that row (The Outpost?) are missed | Move column to a smaller tab / confirm list manually | Open |
| 9 | North Star: which pixel is canonical (account pixel 3440147309499983 vs HG BM 1904436107168032)? | Pick one, install everywhere, share to account | Open |
| 10 | The Outpost: consolidate HG Event Data pixel and client pixel? | Pick one | Open |
| 11 | Green Springs Inn: stop booking-engine events landing on both pixels | Remove from one | Open |
| 12 | Confirm inferred domains flagged in run 1: canopytreehouse.com, parkerhouseohio.com, Southern Illinois sister brands, links.stayson30a.com, threesunscabins.com, tuxedofalls.com | Shawal confirms, edit expected-domains.csv | Open |
| 13 | Táberg Falls ad account has 5 other clients' pixels shared into it | Remove shares | Open |

## 8. Run log

| Date | Workflow | Mode | Result | Saved? |
|---|---|---|---|---|
| 2026-09-21 | Client Benchmark Review | First run, saved | 16 Advanced clients, 12 live + 4 from CSV (provisional). 39 campaign rows, 30 scored, 9 under gate. 2 Flag to Shawal (American River paused lead campaign at $261 CPL; Canopy "09/02 - Sales" 0.5x ROAS, paused), 12 Review w/ HG AI (Stay on 30A leads $2.23 CPL, Tàberg both sales campaigns 3.3x / 4.5x, Paradise Pointe retargeting 2.7x, plus 8 lead campaigns at $1.10–2.35 CPL), 4 Monitor, 6 Healthy, 6 Scale (Stay on 30A both sales 23.7x / 30.0x, Asheville retargeting 49.5x, both Starlight Havens ~20x, Ponderosa 24.9x) | Yes: `Client Benchmark Reviews (advanced setups)/Weekly Checks/2026-09-21-client-benchmark.md` + `.csv` |
| 2026-09-21 | Pixel Domain Check | First run, saved | 42 clients, 47 pixel rows (46 pixels), 975,003 events in 7d. 2 ❌ cross-contamination (Inspired Retreats ← Stay Saluda GHL; Little River Landing ← North Star GHL), 14 ⚠️ (Tuxedo Falls silent since 1 Sep, Three Suns bio-only, Outpost + North Star split pixels, Raven Rock pixel not shared to account, Green Springs + Selah double pixels, CGG Wix-only pixel, Asheville no CAPI, Canopy low volume, Parker + Southern Illinois unconfirmed domains), 31 ✅ | Yes, `Meta Pixel Reviews/Weekly Checks/2026-09-21-pixel-domain-check.md` + `.csv` |
| 2026-09-21 | Ad Spend Check | First run, chat only | 42 clients, 37 live reads, 5 via CSV. 1 ❌ (Columbia Gorge), 6 ⚠️, 5 provisional from CSV. $2,620/day confirmed live vs $2,555 documented for the same accounts | No, reviewed in chat |
| 2026-09-21 | Ad Spend Check | Full run, saved | 42 clients, 37 live reads, 5 from CSV (provisional). 2 ❌ (Columbia Gorge, Big Moon Ranch), 10 ⚠️, 30 ✅. $2,620/day confirmed live vs $2,555 documented for the same accounts. Canopy paused all campaigns within the last few days after ~$1.5k MTD | Yes: `Ad Spends Checks/Weekly Checks/2026-09-21-ad-spend-check.md` + `.csv` |
