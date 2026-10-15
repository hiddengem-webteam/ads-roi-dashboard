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

Since 2026-10-15 this project lives inside the ROI dashboard repo (`ads-roi-dashboard`), under `weekly/`. Skills run from the repo root; everything else stays under `weekly/`.

```
<repo root>/
├── .claude/skills/
│   ├── ad-spend-check/SKILL.md          /ad-spend-check
│   ├── pixel-domain-check/SKILL.md      /pixel-domain-check
│   └── client-benchmark/                /client-benchmark + generate_report.py
├── public/weekly/                       generated archive served at /weekly/ by the dashboard; rebuild, never hand-edit
├── netlify.toml                         one site: monthly dashboard at /, weekly archive at /weekly/ (noindex headers + latest redirects)
└── weekly/
    ├── Project Data/                    this file + CHANGELOG.md + build_html.py + build_site.py + serve_site.py + assets/hg-wordmark.svg
    ├── Weekly CSV Reports/              Ads Manager exports, one per week, dated filename
    ├── Ad Spends Checks/Weekly Checks/                       dated reports (.md) + sidecar (.csv) + built .html
    ├── Meta Pixel Reviews/                                   expected-domains.csv + Weekly Checks/
    ├── Client Benchmark Reviews (advanced setups)/Weekly Checks/
    ├── Monthly ROI data/                monthly client-reporting JSON, written by the dashboard's export scripts
    └── HG AI Reports/                   HG AI diagnoses Shawal drops in, client name + date in filename
```

Report filenames are `YYYY-MM-DD-<workflow>.md` with a matching `.csv`, plus a `.html` built from both by `weekly/Project Data/build_html.py`. CSV exports are `YYYY-MM-DD_Www_meta-ads-report.csv`. Paths in the skills are relative to the repo root.

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

Classification is by objective (OUTCOME_LEADS → Lead Gen; OUTCOME_SALES → Retargeting if the name says BoF / Retarget, else MoF lookalike sales, scored on the same ROAS bands). Frequency, cost per booking, CPC, CPM and CTR are diagnostics only. Only campaigns live (ACTIVE) at run time are scored; paused campaigns that spent in the window are listed per client as "Paused in window" and never enter Action needed or the counts (Shawal, 2026-09-23: paused means already acted on). MCP-disabled accounts fall back to the weekly CSV export (21-day window, provisional). No HG AI hand-off block; Shawal drops HG AI reports into the root `HG AI Reports/` folder and the skill summarises them per client.

Output: `Client Benchmark Reviews (advanced setups)/Weekly Checks/YYYY-MM-DD-client-benchmark.md` and `.csv` (one row per campaign, keyed on campaign ID). Report order: header counts, last Meta Ads Strategy meeting (Gemini notes: summary, decisions, next steps), Action needed (Flag then Review), Scale candidates, per-client sections ordered by scored spend (each with a Monthly ROI line, a Meeting notes line and an HG AI notes line), footer.

Next: week-over-week diff in `generate_report.py` (currently hardcodes "First run").

**This month strip (2026-10-15, Shawal).** Every client card starts with direct revenue month to date (booking date, platform direct/OTA rules, shared-PMS tenants narrowed to their own properties), the change against the same day span of the previous month, and promo-code uses for the month. Source: HiddenGem AI platform via `pms_mtd.sql` in the skill folder, run through the Supabase connector and saved as `pms_mtd.json`. Guesty exposes code names, Hostaway only a count, Hospitable and Cloudbeds nothing; clients without a PMS connection show "not tracked".

### 4.4 HTML reports — built 2026-09-21

`weekly/Project Data/build_html.py [YYYY-MM-DD]` reads each workflow's dated `.md` and `.csv` and writes a dated `.html` beside them, styled from the HiddenGem Media design system (`https://claude.ai/artifact/GXb4YMfP8uFmoTPhnWujSk`: Inter, neutral canvas, brand blue for accents only, semantic badges instead of emoji, sentence case, light and dark themes). Each page: masthead with wordmark, stat row, alert callouts for critical findings, filterable tables, per-client cards (benchmark), footer notes. Published as private artifacts; republish to the same URL to keep the link:

| Workflow | Artifact URL (W39, 2026-09-21) |
|---|---|
| Ad spend check | https://claude.ai/artifact/8v1ecvQnHougDxjspvuB66 |
| Pixel domain check | https://claude.ai/artifact/PvVhNRBCtnniJGzsehkTWf |
| Client benchmark | https://claude.ai/artifact/HFu3dZGrVBK9zHuYBu9qJ4 |

**Repo and live archive (added 2026-09-21, merged 2026-10-15).** Until 2026-10-15 this was its own private repo (`https://github.com/hiddengem-webteam/meta-ads-weekly-reviews`) deployed as `hiddengem-ads-reviews.netlify.app` (site id f7b6b654-f0d8-4f24-9d69-03d351daff49, team hgwebteam). It is now the `weekly/` folder of the ROI dashboard repo (`https://github.com/hiddengem-webteam/ads-roi-dashboard`, history kept via subtree merge). `weekly/Project Data/build_site.py` rebuilds `public/weekly/` (index of every Monday, `/weekly/<slug>/<date>.html`, `/weekly/<slug>/latest.html`); the dashboard's Netlify build copies it into `out/weekly/`, so one site serves the monthly dashboard at `/` and this archive at `/weekly/`. Latest-page redirects and the `noindex` header for `/weekly/*` are in the repo's `netlify.toml`. The site must stay behind Netlify password or team access, because the pages name clients, account IDs, pixel IDs and budgets. The old Netlify site can be deleted once the dashboard site has that access control.

Weekly publish, after the three skills have written their `.md` + `.csv`:

```
python3 "weekly/Project Data/build_html.py" YYYY-MM-DD
python3 "weekly/Project Data/build_site.py"
git add -A && git commit -m "Reviews YYYY-MM-DD" && git push
```

Open: email delivery (Mailtrap) not wired yet. Resolved 2026-10-15: deploys ride the dashboard's push-to-deploy, no CLI deploy.

## 5. Client → ad account map (as of 2026-09-21)

All 42 sheet clients matched by name. The sheet's "Ads Account Link" column exports as the word "Acc" with no URL, so IDs below are the reliable key.

| Client (sheet) | AM | Ad account | ID | Connector |
|---|---|---|---|---|
| American River Resort | Nicole | American River Resort | 953162737054331 | ok |
| Asheville River Cabins | Charlotte | Asheville River Cabins Ads | 615836588009747 | ok. Was UNSETTLED 2026-10-05, ACTIVE again by 2026-10-13 |
| Away2PA | Alicia | Away2Pa | 603977626130795 | ok |
| Awayframes | Alicia | Awayframes Ad Account | 2471256056603833 | ok |
| Best Texas Travel | Nicole | Best Texas Travel Ad Account | 1982551189319458 | ok |
| Big Moon Ranch | Charlotte | Big Moon Ranch | 758851247064974 | **Offboarded 2026-09-28** (Shawal). Still on the Master sheet on 2026-10-05 (⚠️). Not in the connector list or the export any more. Not a blocker: if the row is still on the Master sheet, the spend check marks it ⚠️ "offboarded, remove from sheet or set Status to Not Live" and stops once the row is gone |
| Bison Ridge Retreat | Chiara | Bison Ridge Retreat Ad Account | 950241787963535 | MCP disabled → CSV |
| Canopy at Moody Moon Ridge | Kristal | The Canopy At Moody Moon Ridge | 1293707265980102 | ok via the connector; NOT visible to the HiddenGem-Claude system user (decision 31). Second account "Moody Moon Ridge" (Sue Hough) 1061646495537777 is MCP disabled |
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
| Selah Place | Alicia | Selah.place | 1275283434220508 | ok. Was UNSETTLED / not queryable on 2026-09-28; ACTIVE and queryable again on 2026-10-05 |
| Starlight Haven - Hot Springs | Charlotte | Starlight Haven Hot Springs | 901138032027913 | ok, ad set budgets |
| Starlight Haven - Weiss Lake | Charlotte | Starlight Haven Weiss Lake | 74756899 | ok, ad set budgets |
| Stay on 30a | Charlotte | Stay on 30a Ads | 25640434272252212 | ok. Legacy "[NOT IN USE] Stay on 30A" 908452332132644 under HG BM, MCP disabled |
| Stay Saluda NC | Makenna | Stay Saluda Ads | 1863632561215857 | ok |
| Stay Southern Illinois | Chiara | Southern Illinois Cabins Ads | 1661949078036229 | ok |
| Stay With Branch | Kristal | @staywithbranch | 1269399754049770 | ok (delivery stalled from about 1 Oct 2026, see decision 24). Separate "Branch Berkeley Springs" 1517541906010284 exists, not on sheet |
| StayLuxe | Nicole | Stay Luxe Ads | 25033578722931437 | ok |
| Sunapee Stays | Charlotte | Sunapee Stays Ads Account | 651114096215889 | ok |
| Taberg Falls | Alicia | Táberg Falls | 827872700004659 | ok |
| The Cohost Company | Makenna | The Cohost Company Ads | 9141035462679902 | ok |
| The Outpost | Ananya | The Outpost Grand Canyon | 1530849534802936 | ok |
| Three Suns Cabins | Anna | Three Suns Cabins Ad Account | 1210218584137342 | ok |
| Treetop Escapes | Makenna | Treetop Escapes Ads | 967636478877602 | ok |
| Tuxedo Falls | Chiara | Tuxedo Falls - Ad Account | 2077151009889326 | ok |
| Walden Retreats | Anna | (account named by its ID in the export) | 973261794434226 | ok via the API system user; on the Master sheet from 2026-10-13 at $30/day. CRM Advanced |

Active accounts with spend but no sheet row: Hillside Amble (Anna), Cowan Creek Lodges (Anna), Edenwood NC (Charlotte), Stay Different (Anna), Branch Berkeley Springs. Decision pending on whether to add them. Walden Retreats is now on the sheet (row above). Treetop Hideaways, Glasscombe, Cabin Collective, Casey Key Resort and Arca Roatan have no ad account yet.

### 5.1 Client → pixel map (as of 2026-09-21)

Primary pixel per client, plus live secondaries. Full domain expectations live in `Meta Pixel Reviews/expected-domains.csv`.

| Client | Pixel (name → ID) | Owner | Notes |
|---|---|---|---|
| American River Resort | American River Resort - Meta Pixel → 2862601447415133 | HG BM | |
| Asheville River Cabins | Asheville River Cabins Meta Pixel → 1634367080775220 | client BM 3440656856064841 | browser only |
| Away2PA | Away 2PA Meta Pixel → 772693422494226 | HG BM | |
| Awayframes | Awayframes - Meta Pixel → 773898245792839 | HG BM | |
| Best Texas Travel | Best Texas - Meta Pixel → 4108409325970216 | HG BM | |
| Big Moon Ranch | Big Moon Ranch - Meta Pixel → 1208874174466414 | HG BM | client offboarded 2026-09-28; pixel stays in the HG BM listing, expect it to go silent |
| Bison Ridge Retreat | Bison Ridge - Meta Pixel → 1241959234316508 | HG BM | account MCP-disabled, pixel readable |
| Canopy at Moody Moon Ridge | Moody Moon Pixel Main → 861460105842405 | client BM 1798221880199326 | |
| Columbia Gorge Getaways | Columbia Gorge Getaways Pixel → 700947282709400 (primary); CGG Pixel → 595257656540749 (Wix embed only) | client BMs | two live pixels |
| Endless Stays | Endless Stays Meta Pixel → 876508505381758 | HG BM | account MCP-disabled, pixel readable |
| Evergreen Cabins | Evergreen Cabins Meta Pixel → 1474685406530880 | client BM 182684855965772 | |
| FLOHOM | FLO2 Conversion → 139231105894533 | client BM 873976399912644 | FLO1 Conversion, FLO2 never fired |
| Green Springs Inn | GSI - Wix Pixel → 1098954801239133 (primary); Green Springs Inn Event Data → 1602971745164199 (booking engine only) | client BM 168139003880292 | double-counts book.* |
| Hiawassee Glamping | Hiawassee Meta Pixel → 1149628220675980 | HG BM | Event Data pixel never fired |
| Home Base | Home Base Bnb - Meta Pixel → 1467511861488785 | HG BM | homebase.rentamira.com seen 2 Oct 2026, accepted as a vendor host, confirm |
| Inspired Retreats | Inspired Retreats Meta Pixel → 1547510566197386 | HG BM | contaminated by Stay Saluda GHL pages |
| Little River Landing | Little River Landing Meta Pixel → 1816709606431185 | client BM 1764967091370111 | North Star GHL contamination stopped 23 Sep 2026, clean from the 2026-10-05 run |
| Myrinn | Myrinn - Meta Pixel → 1943632852972363 | HG BM | |
| Nature Nooks | Nature Nooks - Meta Pixel → 844302611320158 | HG BM | Event Data pixel never fired |
| North Star Resort & Lodge | North Star Lodge Killington - Meta Pixel → 3440147309499983 (attached; site + GHL, first server events 2026-10-13); Northstar Meta Pixel → 1904436107168032 (HG BM, Cloudbeds + part of GHL, no longer the site) | split | decide canonical; Cloudbeds still only on the HG BM pixel |
| Oak & Ember | Oak & Ember - Meta Pixel → 1729106025177871 | HG BM | Event Data pixel never fired |
| Paradise Pointe | Paradise Pointe - Pixel → 707016175006193 | client BM 1087116839728915 | account MCP-disabled, pixel readable |
| Parker Reserve | Parker Reserve - Pixel → 1188475652520634 | HG BM | |
| Ponderosa Pines Resort | Ponderosa Pines Resort - Meta Pixel → 1293211539656211 (primary, CAPI); Ponderosa Pines Resort's Pixel → 1743173753375733 (client, browser only, also on the main site, found 2026-10-13) | split | double-counts page views; decision 33 |
| Raven Rock Mountain | Raven Rock Meta Pixel → 1359649962298380 | HG BM | NOT shared to ad account 1065186195582056 |
| Red White & Blue Views | Red White & Blue - Meta Pixel → 1625871301864243 | HG BM | |
| Ridge & Falls | Ridge & Falls - Meta Pixel → 1332286819018269 | client BM 1887518261927124 | HG BM copy 2059709192087667 never fired; server events stopped 16 Sep 2026, back from 3 Oct 2026 |
| Selah Place | Selah.Place Event Data → 1235173718368839 (primary); LinkTree → 3327546500757583 | client BM 1662038040809917 | Selah 2026 Pixel never fired; a third pixel "Wix Pixel for fc9ae0e6" 375795251002998 fired once on 22 Sep 2026 |
| Starlight Haven (Hot Springs + Weiss Lake) | Starlight Haven Pixel - ResNexus → 766226461367996 | client BM 735291970494853 | one pixel, two accounts, browser only |
| Stay on 30a | Stay on 30a - Meta Pixel → 1464927198465632 | HG BM | |
| Stay Saluda NC | Stay Saluda - Meta Pixel → 4250460185185664 | HG BM | |
| Stay Southern Illinois | Southern Illinois Cabins - Meta Pixel → 1328561309169535 | HG BM | multi-brand domains |
| Stay With Branch | Branch → 1107997340818783 | client BM 2066827277052066 | Business Meta Pixel dead since May 2026; server (CAPI) events stopped 17 Sep 2026, back from 3 Oct 2026 |
| StayLuxe | StayLuxe Meta Pixel → 4293491110916917 | HG BM | |
| Sunapee Stays | sunapeestays's Pixel → 471248637966769 | client BM 1296150947517054 | |
| Taberg Falls | Taberg Falls - Meta Pixel → 964214909847907 | HG BM | 5 other clients' pixels also shared into this account |
| The Cohost Company | The Cohost Company Meta Pixel → 638998632168952 | client BM 500895838996853 | |
| The Outpost | HG - The Outpost Grand Canyon Event Data → 1691591692267740 (bio only); Outpost Grand Canyon → 734783866381382 (site + Newbook, client BM) | split | decide canonical |
| Three Suns Cabins | Three Suns Cabins - Pixel → 691977289952800 | HG BM | bio subdomain only |
| Treetop Escapes | Treetop Escapes - Pixel → 1178838797064774 | client BM 1190724359426537 | |
| Walden Retreats | Walden Retreat's Data → 505477285266646 | client BM | attached to 973261794434226; waldenretreats.com + ResNexus; clean on 2026-10-13 |
| Tuxedo Falls | Tuxedo Falls - Ad Account's Pixel → 1561325308991270 (attached, silent since 1 Sep 2026); Website → 1839806973541001 (same business, carries site + ResNexus + GHL, ~26k events/week, NOT attached to the ad account) | client BM 1400770510587476 | found 2026-09-28: the site tracks on the unattached pixel |

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

- **A silent attached pixel can hide a live unattached one.** Tuxedo Falls' ad account pixel has been silent since 1 Sep, but a second pixel ("Website") in the same client business carries the whole site. When a pixel is silent, list the client's business datasets in the HG BM listing (same `business_id`) before calling the client untracked.
- **The Ads Manager saved report now carries Campaign delivery and Ad set delivery** (Shawal added them 2026-09-28) and exports 7 days. Both the spend check and the benchmark filter CSV rows to `active`, and the provisional marker is gone. Three of the four CSV accounts moved to ✅ on the spend check the same day.
- **The CRM Advanced list is bigger than the first run showed.** Downloading the sheet with `download_file_content` (base64 CSV) returns the whole Clients - Onboarding tab: 24 Advanced clients on 2026-09-28, including The Outpost, Selah Place, Sunapee Stays, Ridge & Falls, Little River Landing and North Star, which the truncated `read_file_content` view had cut off. Canopy at Moody Moon is Basic there. Use the download, not the read.
- **`ads_get_ad_accounts` can drop an account entirely.** Big Moon Ranch (758851247064974) was MCP-disabled on 21 Sep and absent from all three pages on 28 Sep. Absent means 🔴, and it also needs the CSV export to include the account.
- **hiddengem.media carries client pixels.** HG's own site fired the FLOHOM and Táberg Falls pixels in the week of 21 Sep. Housekeeping, not contamination, but it pollutes those clients' audiences.
- **Gemini's follow-on meeting is titled "Meta Ads x HiddenGem AI Sync"** (organiser Gillian), not "Meta Ads Sync"; search both. A short Strategy call can produce a transcript but no notes ("not enough conversation in a supported language").
- **Ad-account status UNSETTLED shows up as `is_queryable: false`** (Selah Place, Villa Destino, 2026-09-28) while reads still succeed. Treat it as a payment warning, not a blocker.
- **Budgets came back in dollars on 2026-10-05**, not cents (`daily_budget: 20` for a $20/day campaign). Sanity-check the magnitude against 7-day spend before dividing by 100.
- **`read_file_content` on the Master sheet returns only a few sample rows per tab** (6 on 2026-10-05); `download_file_content` with `exportMimeType: text/csv` returns the whole first tab (Meta Ad Links) as base64. Use the download for the Master sheet as well as the CRM.
- **An UNSETTLED account stops delivering within a day or two.** Asheville River Cabins went UNSETTLED / not queryable this week and the export shows all three campaigns not_delivering with $90 spent in 7 days against $80/day of budgets. Score such accounts from the CSV, treat $0 active as ❌ on a Live row, and name the payment issue in the next action.
- **Delivery can stall with budgets intact.** Stay With Branch kept its $20/day budgets but spent $8.50/day with the full daily budget still remaining at read time; the pixel's traffic dropped at the same time. The spend check has no rule for this; it was raised as ⚠️ on judgement and noted in the footer.
- **A reported GHL pixel block is not a fix until the hourly hosts go quiet.** The Saluda → Inspired Retreats block reported on 28 Sep had no effect by 5 Oct; the North Star → Little River Landing one did. Keep a Reported entry open until the host disappears from the window.
- **The export can carry purchases with no conversion value** (Paradise Pointe BoF, 5 purchases, blank value, 2026-10-05), which makes CSV ROAS 0.0x. The generator now says so in the row instead of reporting a bare 0.0x.
- **Monthly ROI files carry a per-client `note`** (September 2026 file, added 2026-10-07): launch-month caveats, missing PMS data, pixel purchases above total bookings (Stay Southern Illinois), and the Paradise Pointe missing-value case. The generator now appends the latest month's note to the client's Monthly ROI line. Months sort by calendar order, not by the July/August hard-coding used before.
- **Direct Marketing API path (2026-10-13).** When the claude.ai Meta connector is unreachable, a system-user token in the repo-root `.env` (`META_ACCESS_TOKEN`, gitignored) gives the same data through graph.facebook.com v21.0: `act_<id>/campaigns` with `adsets{daily_budget}` for budgets (cents, divide by 100), `act_<id>/insights?level=campaign&date_preset=last_7d|last_14d|last_30d` with `actions`, `cost_per_action_type`, `purchase_roas`, `frequency`, `inline_link_clicks`; `158693423705448/owned_pixels` + `client_pixels` and `act_<id>/adspixels` for the pixel inventory; `<pixel>/stats?aggregation=host|event_total_counts|event_source` for domains, totals and the browser/server split. The HiddenGem-Claude system user sees 50 ad accounts, which covers every sheet client except Canopy (1293707265980102) and the offboarded Big Moon Ranch; the four accounts the connector had MCP-disabled read fine. `event_total_counts` here is one row per event (no hidden-dimension repeats). Scripts live in the session scratchpad (`w42/pull.py`, `pull_px.py`).
- **Graph API stats are paginated** (25 buckets a page by default; `paging.next` carries the token). Always follow `next` or pass `limit=500`, otherwise a 7-day host query returns only the first 25 hours (caught 2026-10-13 before the pixel report was written).
- **The HG BM `owned_pixels` edge errors with #200 when `owner_ad_account` is requested**; ask for `id,name,last_fired_time,owner_business` only.
- **A week-over-week diff must survive a source change.** Rows that were CSV-keyed (client + campaign) last week and campaign_id-keyed this week were showing as Removed/New; the generator now falls back to client + campaign name.
- **`aggregation=event_source` on `<pixel>/stats` gives the browser/server split per hour**, which the connector never exposed. Five 'CAPI Setup (HG Ai)' clients turned out to be under 0.2% server-side (FLOHOM, Paradise Pointe, Sunapee, Stay With Branch, Ridge & Falls) while working connections run 30–60%. A single `server_last_fired_time` inside the window is not evidence of a working CAPI; use the share.
- **`event_total_counts` through the Graph API is not windowed** (it returned lifetime-scale totals such as 738k for American River against 15k host events). Use the host sum or the `event_source` sum for 7-day totals and `aggregation=event` for per-event 7-day counts.

## 7. Open decisions

| # | Question | Options | Status |
|---|---|---|---|
| 1 | Dollar floor before Critical on small accounts? | Keep pure % rule / add $15 floor | Open |
| 2 | Add the five unlisted active accounts to the Master sheet? | Yes / No / some | Open |
| 3 | Add account IDs to the Master sheet? | Recommended | Open |
| 4 | Ads Manager saved report: add delivery columns, last 7 days | Recommended | Resolved 2026-09-28: columns added, export is 7 days. Big Moon Ranch no longer needs adding (offboarded 2026-09-28) |
| 5 | AM for North Star Resort & Lodge | Add to CRM | Open |
| 6 | Where does the expected pixel domain per client live? (workflow 2) | Sheet column / file in folder | Resolved 2026-09-21: `Meta Pixel Reviews/expected-domains.csv`, seeded from run 1 with `source=inferred`; Shawal flips rows to `confirmed` |
| 7 | Source and format for weekly ads meeting summary (workflow 3) | Fireflies connector / pasted file | Resolved 2026-09-21: Gemini "Notes by Gemini" docs attached to the weekly "Meta Ads Strategy" and "Meta Ads Sync" calendar events, fetched automatically via the Calendar + Drive connectors. No manual step |
| 8 | Definition of "advanced setup" for workflow 3 filter | | Resolved 2026-09-21: CRM "Clients - Onboarding" tab, Meta Ads column = Advanced |
| 14 | Cost per follower source for IG Discovery scoring (Ads Manager follows result / IG follower delta / cost per profile visit proxy) | | Parked 2026-09-21: ToF not scored in v1 |
| 15 | Do "MoF - Lookalike Sales" campaigns get their own ROAS band, or stay on the Retargeting bands? | Add a band to the doc / keep | Open, currently scored on Retargeting bands |
| 16 | Benchmarks doc: reconcile the summary table with the per-type sections (IG Scale $0.20 vs $0.30, gate $200 vs $500, Investigate lines inside Monitor bands) | Edit the doc | Open, skill uses the Decision Making table |
| 17 | The Drive export of the CRM cuts the Clients - Onboarding table at Oak & Ember; any Advanced clients below that row (The Outpost?) are missed | Move column to a smaller tab / confirm list manually | Resolved 2026-09-28: `download_file_content` (CSV export) returns the full tab; six more Advanced clients scored from this run |
| 9 | North Star: which pixel is canonical (account pixel 3440147309499983 vs HG BM 1904436107168032)? | Pick one, install everywhere, share to account | Open |
| 10 | The Outpost: consolidate HG Event Data pixel and client pixel? | Pick one | Open |
| 11 | Green Springs Inn: stop booking-engine events landing on both pixels | Remove from one | Open |
| 12 | Confirm inferred domains flagged in run 1: canopytreehouse.com, parkerhouseohio.com, Southern Illinois sister brands, links.stayson30a.com, threesunscabins.com, tuxedofalls.com | Shawal confirms, edit expected-domains.csv | Open (tuxedofalls.com confirmed by traffic on the Website pixel 2026-09-28) |
| 13 | Táberg Falls ad account has 5 other clients' pixels shared into it | Remove shares | Open |
| 18 | Tuxedo Falls: share the live "Website" pixel 1839806973541001 to ad account 2077151009889326 and retire 1561325308991270, or install the attached pixel on the site? | Share the live one (recommended) | Open, raised 2026-09-28 (Chiara) |
| 19 | Ad account mapping for the Advanced clients without one (Walden Retreats 973261794434226 seen in the connector; Treetop Hideaways, Glasscombe, and from 2026-10-05 Cabin Collective, Casey Key Resort, Arca Roatan not launched) | Add to section 5 when live | Open |
| 20 | Endless Stays budgets tripled to $200/day (export 21–27 Sep) against a $50 sheet budget | Nicole confirms with client / revert | Resolved 2026-10-05: sheet updated to $200, budgets rebalanced inside the total (Giveaway $75, BoF $75, MoF $50) |
| 21 | Selah Place $100/day prospecting test (4 ad sets) on top of $35/day, sheet says $50; account also UNSETTLED | Alicia confirms; check payment | Resolved 2026-10-13: BoF raised to $35, account at $55/day vs $50 sheet (within tolerance) |
| 22 | Paradise Pointe runs $150/day (new $50 LoL campaign, Shawal 28 Sep) against a $100 sheet budget | Makenna updates the sheet | Open, raised 2026-10-05 |
| 23 | Asheville River Cabins ad account UNSETTLED; all campaigns not delivering since about 29 Sep | Charlotte clears the balance | Resolved 2026-10-13: account ACTIVE, delivering $92/day |
| 24 | Stay With Branch delivery stalled (spending 40% of its $20/day budgets since 1 Oct) | Kristal checks payment / ad review / audiences | Resolved 2026-10-13: $185 spent in the 6–12 Oct week, delivery back |
| 25 | Big Moon Ranch offboarded but the HG BM pixel is still installed on bigmoonranch.com (about 1.6k events a day) | Remove the pixel from the site or transfer it | Open, raised 2026-10-05 |
| 26 | Paradise Pointe BoF: 5 purchases with no conversion value in the export (ROAS 0.0x); the 23 Sep HG AI note already asked for a purchase-tracking check | Verify Purchase value parameter (pixel + CAPI) | Open, raised 2026-10-05. Confirmed 2026-10-07 by the September ROI file: Meta recorded no revenue for 12 retargeting purchases (15–21 Sep and 29–30 Sep); their value was added manually at the average booking value |
| 27 | Walden Retreats runs $48/day (two wedding-lead test campaigns from 8 and 9 Oct on top of the three-campaign structure) against a $30 sheet budget | Anna confirms the test / sheet | Open, raised 2026-10-13 |
| 28 | Stay on 30a raised to $500/day (LoL $200, BoF $150) against a $400 sheet; one more increase makes it ❌ | Charlotte confirms the ceiling / sheet | Open, raised 2026-10-13 |
| 29 | Tàberg Falls cut to $300/day during the week (Giveaway $50, BoF $75, Leads $50, Lookalike $75, Broad $50) against a $400 sheet | Alicia confirms / sheet | Open, raised 2026-10-13 |
| 30 | The Outpost: a second BoF retargeting campaign (10/..) runs beside the 08/29 one, $50/day vs $40 sheet | Anna pauses the old one | Open, raised 2026-10-13 |
| 31 | Grant the HiddenGem-Claude system user access to Canopy's ad account 1293707265980102 so it is not CSV-only on the API path | Shawal, Business Manager | Open, raised 2026-10-13 |
| 32 | CAPI effectively silent on five clients the sheet marks 'CAPI Setup (HG Ai)': FLOHOM, Paradise Pointe, Sunapee Stays, Stay With Branch, Ridge & Falls (under 0.2% of events server-side) | AMs check the HG AI CAPI connections; Shawal decides whether the sheet's tracking column should reflect it | Open, raised 2026-10-13 |
| 33 | Ponderosa Pines Resort has two live pixels on www.ponderosapinesresort.com (HG pixel 1293211539656211 with CAPI + purchases, and 'Ponderosa Pines Resort's Pixel' 1743173753375733, browser only) | Anna confirms which one the ads use, remove the other | Open, raised 2026-10-13 |

## 8. Run log

| Date | Workflow | Mode | Result | Saved? |
|---|---|---|---|---|
| 2026-10-13 | Pixel Domain Check | Fourth run, saved, Marketing API path | 43 clients, 50 pixel rows (49 pixels; Walden Retreats and a second Ponderosa pixel new), 994,294 events in 7d counted once per event (not comparable with the connector's totals). 1 ❌ (Inspired Retreats ← Saluda, week 4: the 7 Oct pixel-events fix had no effect, every day 6–13 Oct, 61% of the pixel's events are server-side so the leak is a CAPI path), 1 🔴 (Canopy pixel and account not visible to the system user), 21 ⚠️ (15 carried + 6 new: CAPI effectively silent on FLOHOM, Paradise Pointe, Sunapee, Stay With Branch, Ridge & Falls per the API's browser/server split; Ponderosa's second live pixel double-counting the site), 27 ✅, 0 fixed. North Star's attached pixel now carries site + GHL + first server events | Yes: `Meta Pixel Reviews/Weekly Checks/2026-10-13-pixel-domain-check.md` + `.csv` |
| 2026-10-13 | Ad Spend Check | Fourth run (Tuesday), saved, Marketing API path | 43 clients (Walden Retreats new on the sheet), 41 live reads through the HiddenGem-Claude system user token (the claude.ai Meta connector was unreachable all session; the token also reads the four MCP-disabled accounts), 1 from CSV (Canopy, no system-user access), 0 🔴. 3 ❌ (Walden $48 vs $30 new, Paradise Pointe $150 vs $100 week 2, Columbia Gorge $40 vs $30 week 4), 10 ⚠️ (Stay on 30a up to $500 vs $400, Tàberg cut to $300 vs $400, The Outpost second BoF $50 vs $40, plus FLOHOM, Away2PA, Three Suns, Canopy, Big Moon Ranch, Ridge & Falls and Little River Landing #REF!), 30 ✅. Fixed: Asheville (balance cleared, delivering), Selah (BoF raised to $35, $55 vs $50), Stay With Branch (delivery back). $3,063/day confirmed live vs $2,870 documented | Yes: `Ad Spends Checks/Weekly Checks/2026-10-13-ad-spend-check.md` + `.csv` |
| 2026-10-13 | Client Benchmark Review | Fourth run, saved, Marketing API path | 27 Advanced in CRM, 22 with an account (Walden Retreats added), all 22 read live (Bison Ridge, Endless, Paradise Pointe, Ponderosa, Asheville move off the CSV). 51 rows, 37 scored, 14 under gate. 1 Flag (Ridge & Falls leads $5.38 CPL week 3), 9 Review (Endless BoF 3.0x and Paradise Pointe BoF 3.6x now on 14-day live data, 7 lead campaigns $1.26–2.29), 12 Monitor, 8 Healthy, 7 Scale (Asheville BoF 60.5x and leads $0.30 new, Ponderosa 15.0x, 30A BoF 28.5x, both Starlights, Selah BoF 19.3x). Frequency watch: Paradise Pointe BoF 5.9. 7 Oct Strategy notes in (attribution script test on Cloudbeds properties) | Yes: `Client Benchmark Reviews (advanced setups)/Weekly Checks/2026-10-13-client-benchmark.md` + `.csv` |
| 2026-10-05 | Ad Spend Check | Third run, saved | 42 clients, 36 live reads, 5 from CSV (Asheville River Cabins joins the CSV set: account UNSETTLED / not queryable), 0 🔴, 1 offboarded row still on the sheet (Big Moon Ranch ⚠️). 4 ❌ (Asheville $0 active vs $80, all campaigns not delivering on an unpaid balance; Paradise Pointe $150 vs $100 after Shawal's $50 LoL campaign; Selah $35 vs $50, test paused but BoF budget not raised; Columbia Gorge $40 vs $30 week 3), 9 ⚠️ (Stay With Branch delivery stalled at $8.50/day on $20 budgets, Stay on 30a, FLOHOM, Ridge & Falls and Little River Landing #REF!, Away2PA comment, Three Suns note, Canopy no budget, Big Moon Ranch sheet row), 29 ✅. Fixed: Endless Stays (sheet now $200). $2,435/day confirmed live vs $2,330 documented for the same accounts | Yes: `Ad Spends Checks/Weekly Checks/2026-10-05-ad-spend-check.md` + `.csv` |
| 2026-10-05 | Pixel Domain Check | Third run, saved | 42 clients, 48 pixel rows (47 pixels), 1,015,667 events in 7d. 1 ❌ (Inspired Retreats ← Saluda, week 3, block not effective: Saluda GHL hosts fire every hour to 5 Oct), 16 ⚠️ (15 carried + Big Moon Ranch's HG BM pixel still live on the offboarded client's site), 31 ✅. 3 fixed: Little River Landing ← North Star (clean window, block holds), Ridge & Falls CAPI back (3 Oct), Stay With Branch CAPI back (3 Oct). North Star's account pixel now receives the GHL funnel and 37 Purchases | Yes: `Meta Pixel Reviews/Weekly Checks/2026-10-05-pixel-domain-check.md` + `.csv` |
| 2026-10-05 | Client Benchmark Review | Third run, saved | CRM re-read: 27 Advanced (21 with an account, 16 live + 5 CSV; Asheville moved to CSV, three new Advanced clients unmapped). 43 rows, 34 scored, 9 under gate. 3 Flag (Endless Stays BoF 0 purchases in the 7-day export, Paradise Pointe BoF 5 purchases but no conversion value in the export, Ridge & Falls leads $7.03 CPL week 2), 8 Review (Saluda BoF 3.8x week 3, Paradise Pointe new LoL 4.4x, 6 lead campaigns $1.29–1.70), 12 Monitor, 5 Healthy, 6 Scale (Selah BoF 16.5x and Ponderosa 28.9x new). Fixed: Tàberg lookalike 10.5x, Endless leads $0.81. Selah's prospecting test paused (removed). Meeting notes from the 1 Oct Strategy call; CSV rows now carry the frequency diagnostic | Yes: `Client Benchmark Reviews (advanced setups)/Weekly Checks/2026-10-05-client-benchmark.md` + `.csv` |
| 2026-09-28 | Ad Spend Check | Second run, saved | 42 clients, 37 live reads, 4 from CSV (export now has delivery columns, provisional marker dropped), 1 🔴 (Big Moon Ranch: account gone from the connector list and missing from the export). 3 ❌ (Endless Stays $200 vs $50, Selah Place $135 vs $50 after a $100/day prospecting test launched, Columbia Gorge $40 vs $30), 7 ⚠️ (Stay on 30a, FLOHOM now 12% under, Ridge & Falls and Little River Landing #REF! sheet cells, Away2PA comment, Three Suns expired note, Canopy no budget), 31 ✅. Fixed: Bison Ridge, Paradise Pointe, Ponderosa (delivery columns), Stay Saluda (sheet updated to $80). $2,615/day confirmed live vs $2,410 documented for the same accounts | Yes: `Ad Spends Checks/Weekly Checks/2026-09-28-ad-spend-check.md` + `.csv` |
| 2026-09-28 | Client Benchmark Review | Second run, saved | CRM re-read: 24 Advanced (21 with an account, 17 live + 4 CSV); Outpost, Selah, Sunapee, Ridge & Falls, Little River Landing, North Star in scope for the first time, Canopy dropped (now Basic). 43 rows, 33 scored, 10 under gate. 2 Flag (Selah prospecting test 1.3x, Ridge & Falls leads $9.35 CPL), 11 Review (Tàberg lookalike 3.8x, Treetop BoF 4.7x new, Saluda BoF 2.6x, 8 lead campaigns $1.04–2.08), 9 Monitor, 6 Healthy, 5 Scale. 3 fixed (Tàberg BoF 7.2x, Paradise Pointe BoF 8.1x from CSV, Treetop leads $0.94). Meeting notes from the two 24 Sep "Meta Ads x HiddenGem AI Sync" calls; 23 Sep Strategy call produced no Gemini notes. HG AI notes for Saluda, Paradise Pointe, Tàberg summarised | Yes: `Client Benchmark Reviews (advanced setups)/Weekly Checks/2026-09-28-client-benchmark.md` + `.csv` |
| 2026-09-28 | Pixel Domain Check | Second run, saved | 42 clients, 48 pixel rows (47 pixels), 1,029,987 events in 7d. 2 ❌ still open (Inspired Retreats ← Saluda unchanged; Little River Landing ← North Star stopped 23 Sep, closes next week if clean), 17 ⚠️ (14 carried over + Tuxedo Falls' real pixel "Website" 1839806973541001 not shared to the ad account, Stay With Branch CAPI silent since 17 Sep, Ridge & Falls CAPI silent since 16 Sep), 29 ✅, 0 fixed | Yes: `Meta Pixel Reviews/Weekly Checks/2026-09-28-pixel-domain-check.md` + `.csv` |
| 2026-09-23 | Client Benchmark Review | Regenerated 2026-09-21 report under the live-campaigns-only rule | 4 paused rows removed (American River paused lead campaign $261.69 CPL, Canopy "09/02 - Sales" 0.5x and ABO test, Green Springs 07/28 lead campaign). Now 35 rows, 28 scored, 7 under gate, 0 Flag, 12 Review, 4 Monitor, 6 Healthy, 6 Scale. Paused spend shown per client. HTML, artifact and site republished | Yes, same files overwritten |
| 2026-09-21 | Client Benchmark Review | First run, saved | 16 Advanced clients, 12 live + 4 from CSV (provisional). 39 campaign rows, 30 scored, 9 under gate. 2 Flag to Shawal (American River paused lead campaign at $261 CPL; Canopy "09/02 - Sales" 0.5x ROAS, paused), 12 Review w/ HG AI (Stay on 30A leads $2.23 CPL, Tàberg both sales campaigns 3.3x / 4.5x, Paradise Pointe retargeting 2.7x, plus 8 lead campaigns at $1.10–2.35 CPL), 4 Monitor, 6 Healthy, 6 Scale (Stay on 30A both sales 23.7x / 30.0x, Asheville retargeting 49.5x, both Starlight Havens ~20x, Ponderosa 24.9x) | Yes: `Client Benchmark Reviews (advanced setups)/Weekly Checks/2026-09-21-client-benchmark.md` + `.csv` |
| 2026-09-21 | Pixel Domain Check | First run, saved | 42 clients, 47 pixel rows (46 pixels), 975,003 events in 7d. 2 ❌ cross-contamination (Inspired Retreats ← Stay Saluda GHL; Little River Landing ← North Star GHL), 14 ⚠️ (Tuxedo Falls silent since 1 Sep, Three Suns bio-only, Outpost + North Star split pixels, Raven Rock pixel not shared to account, Green Springs + Selah double pixels, CGG Wix-only pixel, Asheville no CAPI, Canopy low volume, Parker + Southern Illinois unconfirmed domains), 31 ✅ | Yes, `Meta Pixel Reviews/Weekly Checks/2026-09-21-pixel-domain-check.md` + `.csv` |
| 2026-09-21 | Ad Spend Check | First run, chat only | 42 clients, 37 live reads, 5 via CSV. 1 ❌ (Columbia Gorge), 6 ⚠️, 5 provisional from CSV. $2,620/day confirmed live vs $2,555 documented for the same accounts | No, reviewed in chat |
| 2026-09-21 | Ad Spend Check | Full run, saved | 42 clients, 37 live reads, 5 from CSV (provisional). 2 ❌ (Columbia Gorge, Big Moon Ranch), 10 ⚠️, 30 ✅. $2,620/day confirmed live vs $2,555 documented for the same accounts. Canopy paused all campaigns within the last few days after ~$1.5k MTD | Yes: `Ad Spends Checks/Weekly Checks/2026-09-21-ad-spend-check.md` + `.csv` |

## 9. Actions log (changes made between runs)

What Shawal or an AM changed in the accounts between two Monday runs, so the next run can explain a Fixed / Still open row instead of rediscovering it. Claude adds a row when Shawal reports a change, checks it against the connector where it can, and marks it **Done** (seen in the account), **Planned** (reported but not yet visible) or **Reported** (not checkable). Each skill's diff step reads this table.

| Date | Client | Change | Reported by | Connector check | State | What next week's run should see |
|---|---|---|---|---|---|---|
| 2026-09-28 | Columbia Gorge Getaways | New lead campaign "MoF - Lead Campaign - Retargeting Engagers – 09/28/26" launched at $5/day, replacing the July MoF lead campaign (no longer active) | Shawal | Live at 13:00 PT: Discovery $20 + BoF $15 + new MoF $5 = $40/day | Done | Spend check still ❌ $40 vs $30 sheet until the sheet is updated. Benchmark: new campaign row, under the $100 gate for at least two weeks |
| 2026-09-28 | Selah Place | Payment error on the ad account (the connector's UNSETTLED status) | Shawal | 2026-10-05: account ACTIVE and queryable again, so the payment error is cleared | Done (resolved) | Spend check: 7-day spend will drop well below the live budgets; keep the payment warning until the account is queryable again |
| 2026-09-28 | Selah Place | Move the prospecting test's budget into the BoF retargeting campaign ("BoF-Website Retarget Campaign - 07/24/2026") | Shawal | 2026-10-13: BoF-Website Retarget Campaign now $35/day, test still paused | Done | If done: test paused, BoF above $15/day. Spend check re-totals against the $50 sheet (still over unless the sheet moves). Benchmark: Flag row on the test becomes "Paused in window, not scored"; BoF gets the extra spend |
| 2026-09-28 | Ridge & Falls | Fix the conversion event on the lead campaign and relaunch it | Shawal | 2026-10-13: still the 09/01 lead campaign, no relaunch (CPL $5.38 on 30 days) | Planned (not done by 13 Oct) | If done: a new lead campaign dated late Sep/Oct and the 09/01 one paused; the $9.35 CPL Flag row moves to "Paused in window" and the new row starts under the $100 gate. Pixel check: watch for Lead events resuming on 1332286819018269 |
| 2026-09-28 | Tàberg Falls | Added audience segments; new "MoF - Broad (Acquire new customers) - 09/28/2026" Sales campaign at $50/day (starts 21:00 UTC); Lookalike Sales campaign cut from $100 to $50/day | Shawal | Live: Lookalike $50 + BoF $100 + Giveaway $100 + Leads $60 + Broad $50 = $360/day, same total as the W40 read | Done | Spend check stays ✅ ($360 vs $400 sheet). Benchmark: Lookalike (Review, 3.8x) is on half the budget, judge on 14 days after 28 Sep; Broad is a prospecting Sales campaign, scored on the Retargeting bands per decision 15, under the $200 gate until about 2 Oct |
| 2026-09-28 | Inspired Retreats ← Stay Saluda (pixel) | Blocked the contaminated traffic (Saluda hosts sending to pixel 1547510566197386) | Shawal | 2026-10-05: Saluda hosts still fire the pixel every hour of the 28 Sep to 5 Oct window (last 5 Oct 08:00 PT), 20 to 25% of its events; the block had no effect | Not effective (still ❌) | Pixel check: ❌ row closes only if no staysaluda.com host appears in the 7-day window; if the block was applied 28 Sep the row will still show a few events in the first day of the window, so read the daily buckets before deciding |
| 2026-09-28 | Little River Landing ← North Star (pixel) | Blocked the contaminated traffic | Shawal | 2026-10-05: clean 7-day window, no North Star host; row Fixed | Done (verified 2026-10-05) | Pixel check: ❌ row should close (Fixed) on 5 Oct |
| 2026-09-28 | Big Moon Ranch | Client offboarded | Shawal | Account 758851247064974 already absent from the connector list and the export in the W40 run | Done | Spend check: no longer 🔴. If the row is still on the Master sheet, ⚠️ with "offboarded, remove from sheet or set Status to Not Live"; once removed, the diff shows "Removed from sheet". Pixel check: pixel 1208874174466414 should fall silent; the row drops when the client leaves the sheet |
| 2026-09-28 | Paradise Pointe | New "MoF - LoL Sales Campaign - 09/28/26" at $50/day; account now $150/day (Shawal's 29 Sep change note: "ad spend at $150/day for now") | Shawal | 2026-10-05 export: campaign active, $328 spent 28 Sep–4 Oct, 6 purchases, 4.4x (7 days) | Done | Spend check ❌ $150 vs $100 until the sheet moves. Benchmark: Review (4.4x) on 7 days of CSV data, judge after two full weeks |
| 2026-10-05 | Asheville River Cabins | Account UNSETTLED (unpaid balance); all three campaigns not delivering since about 29 Sep | Claude (connector + export) | 2026-10-13: account_status ACTIVE via the API, $646 spent 6–12 Oct | Resolved | Spend check ❌ until the balance clears and spend returns to about $80/day; benchmark scores nothing while paused in window |
| 2026-10-07 | Inspired Retreats ← Stay Saluda (pixel) | Second fix: Shawal checked the Saluda GHL landing pages (no IR pixel snippet on any of them) and removed the Inspired Retreats pixel from the pixel-events / Conversions API configuration on the Saluda side; the traffic was arriving server-side, not from a page snippet | Shawal | 2026-10-13: Saluda hosts fired the IR pixel every day 6–13 Oct (about 1,000 events, 22%), no change after 7 Oct; 61% of the pixel's events are server-side | Not effective (still ❌) | Pixel check 12 Oct: the 5–12 Oct window still contains 5–7 Oct events from go/bio/links.staysaluda.com; read the hourly buckets and call the row Fixed if no Saluda host appears after 7 Oct. If Saluda hosts persist past 7 Oct, look at the HG AI CAPI connector for Saluda next (decision: see learnings, 'A reported GHL pixel block is not a fix until the hourly hosts go quiet') |
