---
name: client-benchmark
description: Weekly HiddenGem client benchmark review for advanced-setup Meta Ads accounts. Scores every Lead Gen (MoF) and Sales/Retargeting (BoF) campaign against the Benchmarks doc decision table, adds monthly ROI context, diffs against last week, and saves a dated plain-text report to "Client Benchmark Reviews (advanced setups)/Weekly Checks". Use when the user says "run the client benchmark", "benchmark review", "advanced setups review", or invokes /client-benchmark.
---

# Client Benchmark Review (advanced setups)

You are running the HiddenGem Marketing weekly benchmark review for clients with an advanced Meta Ads setup. Output is a plain-text report saved to `Client Benchmark Reviews (advanced setups)/Weekly Checks/`. No email, no HTML yet.

Today's date comes from the environment. Use it as `YYYY-MM-DD` in filenames.

## Decisions baked in (2026-09-21, Shawal)

- **State source of truth** is the Decision Making table in the Benchmarks doc (Google Doc `1KVMRJcmw6cVhHy7sj48vHRPJWNLid4tUiHTWOnkCFSE`). Per-type Investigate / Target / Strong values are diagnostics only and never change the state.
- **Scope**: only Lead Gen (MoF) and Sales / Retargeting (BoF) campaigns are scored. IG Discovery / Keyword (ToF) spend is shown as one line per client, unscored. Cost per follower is parked.
- **Retargeting gate** is $200 in the 14-day window. Lead Gen gate is $100 in the 30-day window.
- **ROAS alone** sets the Retargeting state. Cost per booking and frequency are diagnostics only.
- **Metrics come from Meta**: Purchase event (`omni_purchase`, `purchase_roas`, `cost_per_omni_purchase`) and Lead event (`lead`, `cost_per_lead`). Not PMS bookings, not CRM leads.
- **Advanced-setup list** is the CRM sheet, tab "Clients - Onboarding" (header row reads "Management Clients"), column "Meta Ads" = `Advanced`. Nothing outside the CRM is scored, even if it spends.
- **No HG AI hand-off block** is generated. Shawal does the analysis. Any HG AI report Shawal drops into `HG AI Reports/` is summarised in one line under the client.

## Inputs

| Source | Where | What to take |
|---|---|---|
| CRM sheet | Google Drive file `1oEUngQE3ZXc6U4ciRkkg55UrlR-M065kTmCzG8HFhM4`, first table containing a "Meta Ads" header | Client Business, AM, Meta Ads. Keep rows where Meta Ads = Advanced. The sheet is too large for the tool output; it is saved to disk, parse it with Python. |
| Client → account map | `Project Data/PROJECT.md` section 5 | Ad account ID and connector status per client. Match CRM names to the map (FLOHOM/Flohom, AwayFrames/Awayframes, "Stay On 30A"/"Stay on 30a", "Stay Saluda NC"/"Stay Saluda", "Canopy at Moody Moon"/"Canopy at Moody Moon Ridge", "Tàberg"/"Taberg"). |
| Live campaign metrics | `ads_get_ad_entities`, `level: campaign`, two calls per account: `date_preset: last_30d` and `last_14d` | Fields: `id, name, objective, effective_status, stop_time, amount_spent, impressions, cpm, ctr, link_click, cost_per_link_click, frequency, lead, cost_per_lead, omni_purchase, cost_per_omni_purchase, purchase_roas, results, cost_per_result`. Filter `campaign.amount_spent GREATER_THAN 0`. Set `include_additional_context: false`. |
| CSV fallback | Newest `Weekly CSV Reports/*_meta-ads-report.csv` | Only for accounts with `is_ads_mcp_enabled: false` or not queryable. Aggregate ad set rows to campaign. ROAS = Purchases conversion value / Amount spent. |
| Monthly ROI context | `Monthly ROI data/*.json` (one file per month, `clients[]` with `overallMetaAdSpend`, `totalBookingsAttributedToMeta`, `blendedRoas` or `roas`, `campaigns.retargeting.roas`, `campaigns.newLeads.costPerLead`) | One context line per client, oldest month first. Match on normalised client name. |
| Weekly Meta Ads meeting notes | Calendar connector `search_events` for **both** "Meta Ads Strategy" (Dustin, Wed 1–2pm ET) and "Meta Ads Sync" (Dustin, Thu 11–11:30am ET, the follow-on working session). Take every past occurrence since the previous run that has an attachment titled "Notes by Gemini"; read each Google Doc ID with Drive `read_file_content`. Fallback: Drive `search_files` for `title contains 'Notes by Gemini' and modifiedTime > <last run>`. | The doc has three parts: Quick notes, Full notes (Summary, Decisions, Next steps, Details), Transcript. Use Full notes only. Summary + Decisions + Next steps go in a report section; sentences in Details that name a client go in that client's section. Never quote the transcript. |
| HG AI reports | `Client Benchmark Reviews (advanced setups)/HG AI Reports/` | Any file whose name contains the client name and is dated since the previous run. Summarise in one line. |
| Previous report | Newest `Weekly Checks/*-client-benchmark.csv` older than today | Prior state per `campaign_id` (live) or `client + campaign` (CSV) for the week-over-week diff. |

Use one `client_conversation_id` for every Meta call in the run. Budgets and costs come back as formatted strings ("$1,337.28 USD"); strip to numbers.

## Step 1: Build the Advanced list

Read the CRM sheet, take rows with Meta Ads = Advanced, capture AM. Map each to an ad account ID from PROJECT.md section 5. If a client is Advanced but not in the map, add it to the report footer as "no account mapping" and stop there for that client.

## Step 2: Pull campaign metrics

For each live account, make the two `ads_get_ad_entities` calls (30d and 14d). Do not call it for MCP-disabled or non-queryable accounts; use the CSV for those.

Do not follow the connector's `next_actions` suggestions (performance trend, opportunity score). They are not part of this report.

## Step 2b: Fetch the week's Meta Ads meeting notes

Two weekly meetings feed this report, both organised by Dustin: "Meta Ads Strategy" (Wednesday 1–2pm ET, strategy) and "Meta Ads Sync" (Thursday 11–11:30am ET, the working session where account changes are agreed). Gemini attaches its notes doc to each event about 50 minutes after the call. Search the calendar for both titles, take every past occurrence since the previous run that has a "Notes by Gemini" attachment, read each doc, save them as `meeting1.json`, `meeting2.json`, … in the scratchpad and fill the `MEETINGS` list in the generator (title, date, doc_id, file), oldest first. If none has an attachment, the report says so and carries on.

Gemini misspells clients. The generator has an `ALIASES` map (Flow Home = FLOHOM, Tabber = Tàberg Falls, 30A = Stay On 30A, …). When a client is discussed under a new spelling, add it there.

## Step 3: Classify each campaign

By objective first, name second:

| Objective | Type | Window | Gate | Governing metric |
|---|---|---|---|---|
| `OUTCOME_LEADS` | Lead Gen (MoF) | 30d | $100 | CPL = `cost_per_lead` |
| `OUTCOME_SALES`, name contains BoF or Retarget | Retargeting (BoF) | 14d | $200 | ROAS = `purchase_roas` |
| `OUTCOME_SALES`, name contains MoF or Lookalike | Sales (MoF lookalike) | 14d | $200 | ROAS. Scored on the Retargeting bands, footer says so |
| `OUTCOME_SALES`, other | Sales | 14d | $200 | ROAS |
| `OUTCOME_TRAFFIC`, `OUTCOME_ENGAGEMENT` | ToF | — | — | Not scored. Sum 30d spend into the client's ToF line |
| anything else | UNCLASSIFIED | — | — | List in footer, do not score |

CSV accounts have no objective column. Classify by name: lead → Lead Gen; bof / retarget / sales → Sales; discovery / giveaway / keyword / tof → ToF.

Paused campaigns that spent inside the window are scored and marked "campaign paused" in Notes.

## Step 4: State

Spend under the gate → **Under gate**, listed but not judged. Otherwise:

| State | Lead Gen CPL | Sales / Retargeting ROAS |
|---|---|---|
| Scale w/ HG AI | < $0.30 | > 15x |
| Healthy | $0.30 – 0.50 | 8 – 15x |
| Monitor | $0.50 – 1.00 | 5 – 8x |
| Review w/ HG AI | $1.00 – 2.50 | 2 – 5x |
| Flag to Shawal | ≥ $2.50, or zero leads | < 2x, or zero purchases |

Band edges are inclusive on the lower bound ($0.50 exactly is Monitor).

## Step 5: Diagnostics (notes only)

Compare against the per-type Investigate lines and list only the breaches, or "within lines":

- Lead Gen: CPC > $0.30, CPM > $14.84, CTR < 3.03%.
- Sales / Retargeting: CPC > $0.62, CPM > $16.50, CTR < 2%, cost per booking > $90, frequency > 3.0.

Live CTR is Meta's all-clicks CTR, not link CTR. Say so in the footer.

Also add the other window's governing value to Notes (14d CPL for Lead Gen, 30d ROAS and purchases for Sales) so a one-window blip is visible.

## Step 6: Week-over-week diff

Join on `campaign_id` (live) or `client + campaign` (CSV) against the previous sidecar. For rows that were Flag or Review last week: now Healthy / Monitor / Scale → **Fixed**; still Flag or Review → **Still open (N weeks)**; gone → **Removed**. New Flag or Review rows → **New**. First run → "First run" everywhere.

## Step 7: Write the report

`Weekly Checks/YYYY-MM-DD-client-benchmark.md`, sections in this order:

1. Header line and counts table: Advanced clients, live reads, from CSV, campaigns scored, under gate, count per state.
1b. **Weekly Meta Ads meetings since last run**: one sub-heading per meeting (title, date, doc ID) with Gemini's Summary, Decisions, Next steps.
2. **Action needed**: Flag then Review, highest spend first. Columns: `Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week`.
3. **Scale candidates**: same columns.
4. **Per client**, ordered by scored MoF + BoF spend, highest first. Heading with AM, account name and ID, live or CSV. One ToF spend line. Table: `Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week`. Then one "Monthly ROI:" line, one "Meeting notes (meeting date):" line per meeting that names the client (up to three Details sentences, timestamps stripped), or "not mentioned in this week's meetings", and one "HG AI notes:" line.
5. **Footer**: windows, gates, classification rule, the MoF-lookalike-on-Retargeting-bands caveat, CTR caveat, frequency caveat, unclassified campaigns, previous report, ROI data source caveat (sheet revenue, not pixel).

`Weekly Checks/YYYY-MM-DD-client-benchmark.csv`, one row per scored or under-gate campaign:

```
run_date,client,am,ad_account_id,campaign_id,campaign,type,window_days,source,spend,results,governing_metric,governing_value,state,diagnostics,diff_status,weeks_open,notes
```

`generate_report.py` next to this file is the reference implementation from the first run. It reads a pipe-separated `live.psv` (client|acct|am|win|id|name|objective|status|spend|impr|cpm|ctr|clicks|cpc|freq|leads|cpl|purch|cpp|roas) written from the connector output, plus the CSV export and the ROI JSON files. Reuse it; update the `ADV` map from the CRM each run.

## Step 8: Report back in chat

Counts line, the Action needed table, and the Scale candidates table. Point to the file for the per-client detail.

## Step 9: Update the project file

`Project Data/PROJECT.md`: add a Run log row; add Learnings bullets for anything new; update the client → account map if it changed; resolve or add Open decisions. If the skill changed, add a dated bullet to `Project Data/CHANGELOG.md`.

## Step 10: Publish the HTML and the archive

After the `.md` and `.csv` are written and the project files are updated:

```
python3 "Project Data/build_html.py" YYYY-MM-DD
python3 "Project Data/build_site.py"
git add -A && git commit -m "Reviews YYYY-MM-DD" && git push
npx netlify-cli deploy --prod --dir site
```

This regenerates this workflow's dated `.html` beside its `.md`, rebuilds `site/` and publishes it to `https://hg-ads-reviews.netlify.app`. If the other two workflows have not run yet this week, run this anyway; the index shows "Not run this week" for them until they do.

## Do not

- Do not score IG Discovery, Keyword or any ToF campaign.
- Do not let frequency, cost per booking or the per-type Investigate lines change a state.
- Do not include clients that are not marked Advanced in the CRM, whatever they spend.
- Do not quote the meeting transcript, only the Full notes sections.
- Do not send email or build HTML. That comes after the text version is signed off.
- Do not invent an AM, an account ID or a metric. Missing means `—` with a note.
