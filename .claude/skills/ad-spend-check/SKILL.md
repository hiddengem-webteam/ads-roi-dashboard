---
name: ad-spend-check
description: Weekly HiddenGem Meta Ads budget and spend audit. Compares documented daily budgets in the Master Meta Ads sheet against live budgets in each client's ad account, diffs against last week's run, and saves a dated plain-text report to the "weekly/Ad Spends Checks/Weekly Checks" folder. Use when the user says "run the ad spend check", "weekly spend audit", "budget audit", or invokes /ad-spend-check.
---

# Ad Spend Check

You are running the HiddenGem Marketing weekly Meta Ads budget and spend audit. Output is a plain-text report saved to the `weekly/Ad Spends Checks/Weekly Checks/` folder. No email is sent in this version.

Today's date comes from the environment. Use it as `YYYY-MM-DD` in filenames.

## Inputs

| Source | Where | What to take |
|---|---|---|
| Master Meta Ads sheet | Google Drive file `1B6lWqp_0linzf-3n4iqjJbavidZvyLO5yTY3MDhzYaM` (tab "Meta Ad Links") | Every client row regardless of status. Capture: Client Business, Status, Total Budget (documented $/day), Ads Account Link, Comments. |
| CRM sheet | Google Drive file `1oEUngQE3ZXc6U4ciRkkg55UrlR-M065kTmCzG8HFhM4` | Account manager (AM) per client. If a client appears in several tabs with different AMs, use the most recent tab. If no AM, show `—`. Never guess. |
| Meta ad accounts | `ads_get_ad_accounts`, paginate with `next_cursor` until null (expect 110+ across pages) | `ad_account_id`, `ad_account_name`, `business_name`, `is_ads_mcp_enabled`, `is_queryable`, `not_queryable_reason`. |
| Live budgets | `ads_get_ad_entities` per client account | See "Reading live budgets". |
| Previous report | Newest `weekly/Ad Spends Checks/Weekly Checks/*-ad-spend-check.csv` older than today | Prior Match flag and Notes per ad account ID, for the week-over-week diff. |
| Manual export (fallback) | Newest `weekly/Weekly CSV Reports/*_meta-ads-report.csv` | Ads Manager export used for accounts the connector cannot read. See "CSV fallback". |

Use one `client_conversation_id` for every Meta call in the run.

## Step 1: Read both sheets

Read the Master Meta Ads sheet with `read_file_content`. Take every client row. The first header cell is blank and columns can shift, so anchor on the header names, not positions. Normalise Status to one of `Live`, `Not Live`, `Paused`. Parse Total Budget as a number; blank or non-numeric means "no documented budget".

Read the CRM sheet and build a client -> AM map. Download it with `download_file_content` (`exportMimeType: text/csv`, base64) and parse the Clients - Onboarding tab; `read_file_content` truncates it. Clients with no CRM row keep last week's AM with a note.

Match sheet clients to ad accounts by the account ID in the Ads Account Link column where present, otherwise by name. Record which method was used in Notes when it was name matching.

## Step 2: Fetch all ad accounts

Call `ads_get_ad_accounts` and follow `next_cursor` until it is null. Build a map by `ad_account_id`.

## Step 3: Read live budgets for every client

Do this for every client on the sheet, including Not Live and Paused. Spend on a dark account is the most important thing this report catches.

Access rules. Do not retry these. Before marking a 🔴 Blocker, check the CSV fallback below. If the account is in this week's export, score it from the CSV instead and note the source. Only if it is missing from the export too, flag and move on:

- `is_ads_mcp_enabled: false` -> 🔴 Blocker, Actual $/day `n/a`, note exactly: "Claude doesn't have access — please check the spend manually"
- Account not in the list at all -> 🔴 Blocker, note: "No account access — needs access fix". An account can vanish from the list week to week (Big Moon Ranch, 2026-09-28); check the CSV export before flagging, and if it is missing there too, ask Shawal to add it to the saved report. Exception: a client marked offboarded in `PROJECT.md` section 5 or 9 is not a blocker. If it is still on the Master sheet, mark it ⚠️ with the note "offboarded on <date>, remove from sheet or set Status to Not Live" and skip the account reads.
- `is_queryable: false` -> 🔴 Blocker, note the `not_queryable_reason`
- Two candidate accounts for one client -> query the one owned by the client's own business, not a legacy or "NOT IN USE" account under the HiddenGem BM. Add a ⚠️ note about the duplicate.

### Reading live budgets

On the first run of a session, call `ads_get_field_context` once to confirm the canonical names for the budget and status fields at campaign and adset level, then use those names for the rest of the run.

1. Query `level: campaign`, filtering `campaign.effective_status` IN `["ACTIVE"]`, fields: id, name, effective_status, daily_budget, lifetime_budget, budget_remaining, and any campaign budget flag the field context exposes. Also request `amount_spent` with `date_preset: last_7d`.
2. For each active campaign with a `daily_budget`, use it.
3. For each active campaign with no campaign-level budget, query `level: adset` for that campaign, filtering `adset.effective_status` IN `["ACTIVE"]`, and sum the ad set `daily_budget` values.
4. Lifetime budgets: convert to a daily equivalent as `budget_remaining / days left until end_time`. If there is no end time, use `lifetime_budget / 30` and add a ⚠️ note "lifetime budget, daily figure is an estimate".
5. Meta returns budgets in cents. Divide by 100.
6. Actual $/day for the client = sum of steps 2 to 4 across all active campaigns.
7. Also record 7-day `amount_spent` / 7 as a sanity check. If Actual $/day is 0 but 7-day spend is above $5, note "no active budget but spent $X in the last 7 days" and treat it as active spend for flag purposes.

### CSV fallback for blocked accounts

Shawal drops an Ads Manager export into `weekly/Weekly CSV Reports/` each week. Use it only for accounts the connector cannot read (MCP disabled, not queryable, or absent from the account list). Never prefer it over a live read.

**File handling**
- Pick the newest file in `weekly/Weekly CSV Reports/`. If its name does not already follow `YYYY-MM-DD_Www_meta-ads-report.csv`, rename it to that pattern using today's date and ISO week (e.g. `2026-09-21_W39_meta-ads-report.csv`) before reading it. Tell the user you renamed it.
- Read the `Reporting starts` / `Reporting ends` columns. If `Reporting ends` is more than 7 days before today, treat the file as stale: do not use it, and flag the accounts as 🔴 with the note "CSV export is stale (ends YYYY-MM-DD), please re-export".

**Columns** (UTF-8 with BOM, ad set level, one row per ad set, first row is an account-wide total with a blank Account name; skip it):
`Account name, Campaign name, Ad set name, Campaign delivery, Ad set delivery, Currency, Campaign budget, Campaign budget type, Ad set budget, Ad set budget type, Amount spent (USD), Impressions, Link clicks, Reach, Frequency, Leads, Cost per lead, Purchases, Cost per purchase, Purchases conversion value, ROAS - CM, Reporting starts, Reporting ends`

**Matching**: match `Account name` to the Meta ad account name from `ads_get_ad_accounts` (e.g. "Paradise Pointe Ads", "Bison Ridge Retreat Ad Account"). Fall back to the sheet client name if needed and say so in Notes.

**Computing Actual $/day from the CSV**
1. Group rows by Campaign name. If `Ad set budget` is "Using campaign budget", count the `Campaign budget` once per campaign. Otherwise sum the `Ad set budget` values for that campaign. Only `Daily` budget types count; a `Lifetime` budget is converted as lifetime / days in the reporting period and noted.
2. Actual $/day = sum across campaigns.
3. Also compute spend per day = total `Amount spent (USD)` / number of days in the reporting period. Show both in Notes.

**Delivery columns (added to the saved report 2026-09-28)**: the export carries `Campaign delivery` and `Ad set delivery`. Count a campaign's budget only when its `Campaign delivery` is `active`; list non-active campaigns that spent in the period in Notes. With these columns present the row is no longer provisional. If a future export lacks them, fall back to the old behaviour: count every campaign, say the total probably overstates what is live, and mark the flag provisional.

**Marking**: every row scored from the CSV gets "source: CSV export YYYY-MM-DD to YYYY-MM-DD, not live" at the start of Notes, and `source=csv` in the CSV sidecar (add a `source` column: `live` or `csv`).

## Step 4: Flag each client

Thresholds. `diff` = |Actual − Sheet|, `pct` = diff / Sheet.

| Flag | Rule |
|---|---|
| ✅ Match | Status Live and (diff <= $5 or pct <= 10%); OR Status Not Live/Paused and Actual $/day is 0 and 7-day spend under $5 |
| ⚠️ Warning | Status Live and 10% < pct <= 25%; OR no documented budget; OR duplicate accounts; OR lifetime-budget estimate; OR a Comments note on the sheet that changes the expected figure |
| ❌ Critical | Status Live and pct > 25%; OR any active budget or 7-day spend >= $5 on a Not Live/Paused account |
| 🔴 Blocker | Any access rule from Step 3 |

Spend on a supposedly dark account is always ❌, never downgraded.

Every ⚠️, ❌ and 🔴 row gets a one-line next action in Notes, written for the AM. Examples: "Confirm with client whether $130/day is the new agreed budget, then update sheet", "Pause campaign X, account is marked Not Live", "Request MCP access in Business Manager".

## Step 5: Week-over-week diff

Find the newest `weekly/Ad Spends Checks/Weekly Checks/*-ad-spend-check.csv` dated before today. If none exists, skip this step and write "First run, no prior report" in the Fixed section.

Join on `ad_account_id`. For each row that was ⚠️, ❌ or 🔴 last week:

- Now ✅ -> **Fixed**
- Still flagged, same or worse -> **Still open**, and add the week count (weeks flagged in a row, carried from the previous CSV's `weeks_open` + 1)
- Client no longer on sheet -> **Removed from sheet**

New flags this week are marked **New**.

Also read `weekly/Project Data/PROJECT.md` section 9 (Actions log). If a client's row changed and the log has an entry for it since the previous run, cite the entry in the row's note ("Shawal moved the test budget into BoF on 28 Sep") instead of rediscovering it, and mark a Planned entry Done when the account shows it.

## Step 6: Write the report

Write two files to `weekly/Ad Spends Checks/Weekly Checks/`:

### `YYYY-MM-DD-ad-spend-check.md`

Plain text with pipe tables. Sections in this order:

1. Header line: date, clients reviewed, accounts queried, blocked count, total documented Live $/day, total confirmed live $/day.
2. **Issues, action needed.** ❌ and 🔴 rows first, then ⚠️. Columns: `Client | AM | Flag | Sheet $/day | Actual $/day | Status vs last week | Next action`.
3. **Fixed since last week.** Columns: `Client | AM | Last week | This week | What changed`.
4. **All accounts.** Every client, alphabetical A to Z with no special handling of "The". Columns exactly: `Client | AM | Sheet Status | Sheet $/day | Actual $/day | Match | Notes/Issues`.
5. Footer: clients on sheet, Live vs Not Live/Paused counts, total confirmed daily spend across queryable accounts, blocked count, previous report compared against.

### `YYYY-MM-DD-ad-spend-check.csv`

Machine-readable sidecar for next week's diff and for Supabase later. One row per client, header:

```
run_date,client,am,ad_account_id,sheet_status,sheet_daily_budget,actual_daily_budget,spend_7d,source,flag,diff_status,weeks_open,notes
```

`flag` is one of `match`, `warning`, `critical`, `blocker`. `diff_status` is one of `new`, `still_open`, `fixed`, `unchanged`, `first_run`.

## Step 7: Report back in chat

Give the user the counts line and the Issues table only. Point them to the file for the rest. Do not paste the full table into chat.

## Step 8: Update the project file

Open `weekly/Project Data/PROJECT.md` and:

1. Add a row to **8. Run log** with today's date, mode (saved or chat only), the counts line, and whether files were written.
2. If the run revealed anything not already in **6. Learnings** (a new account quirk, a data-source change, a matching failure), add one bullet. Don't repeat what's there.
3. If a client → account mapping changed or a new client appeared on the sheet, update the table in **5. Client → ad account map**.
4. If an open decision in **7. Open decisions** was resolved during the run, mark it resolved with the date and outcome.

If the skill itself was changed during the session (thresholds, columns, sources, output location), add a dated bullet to `weekly/Project Data/CHANGELOG.md` describing what changed and why. Newest entries go at the top.

## Step 8b: Live budget per campaign type → "Meta Ad Spends" tab (added 2026-10-15, Shawal)

After the report is written, push this week's live daily budget per campaign type for every sheet client into the **Meta Ad Spends** tab of the Master Meta Ads sheet (`1B6lWqp_0linzf-3n4iqjJbavidZvyLO5yTY3MDhzYaM`), one row per client per run, appended under the previous run so the tab keeps a week-by-week history.

1. Write today's documented budgets for the script: from the Master sheet's "Meta Ad Links" tab (already read in Step 1), save `{"<Client Business>": <Total Budget $/day>, ...}` as `.claude/skills/ad-spend-check/sheet-budgets.json` (blank cells and #REF! omitted). Then run `npx tsx scripts/pull-live-budgets.mts YYYY-MM-DD` from the repo root. It reads every active campaign's daily budget through the Marketing API (system-user token in `.env`), buckets them as ToF Giveaway / MoF Leads / MoF Sales LoL / BoF Sales / other (objective first, then name, same rules as the benchmark generator), skips campaigns past their `stop_time`, and writes `weekly/Ad Spends Checks/Weekly Checks/YYYY-MM-DD-ad-spend-by-type.csv` with `sheet_budget`, `diff` and `flag` taken from today's spend-check CSV. Canopy at Moody Moon Ridge comes back as a blocker (decision 31); carry its row with the connector's figures if you read them in step 2, otherwise leave the budgets blank.
2. With the Google Sheets connector, `get_values` on `'Meta Ad Spends'!A1:N1`. If the tab is empty, first write the header row with `update_values` at `'Meta Ad Spends'!A1`:
   `Run date | Client | AM | Ad account ID | Total live $/day | ToF Giveaway | MoF Leads | MoF Sales LoL | BoF Sales | Other | Sheet budget | Diff | Flag | Campaigns`
3. `get_values` on `'Meta Ad Spends'!A:A` to find the first empty row, then `update_values` starting at that row with one row per client from the CSV, in the CSV's order: date as `YYYY-MM-DD` text, ad account ID with a leading apostrophe so it stays text, budgets as numbers, `Flag` as the CSV value (`match` / `warning` / `critical` / `blocker` / `no sheet budget`), `Campaigns` as the CSV's campaign list. Never overwrite earlier runs; never touch any other tab.
4. Read back the written range once and check the row count equals the CSV's client count. Mention the tab in the chat summary ("Meta Ad Spends tab: 42 rows appended for 2026-10-20").

If the Sheets connector is not available in the session, say so, leave the CSV in place, and do not fall back to editing the sheet any other way.

## Step 9: Publish the HTML and the archive

After the `.md` and `.csv` are written and the project files are updated:

```
python3 "weekly/Project Data/build_html.py" YYYY-MM-DD
python3 "weekly/Project Data/build_site.py"
npx tsx scripts/sync-roi-memory.mts   # push the new rows to the roi schema in Supabase
git add -A && git commit -m "Reviews YYYY-MM-DD" && git push
```

This regenerates this workflow's dated `.html` beside its `.md`, rebuilds `public/weekly/` (the merged ROI dashboard serves it at `/weekly/`); Netlify deploys it with the dashboard on the next push to `main`. If the other two workflows have not run yet this week, run this anyway; the index shows "Not run this week" for them until they do.

## Do not

- Do not send email. That comes later.
- Do not skip Not Live or Paused clients.
- Do not call `ads_get_ad_entities` on an account with `is_ads_mcp_enabled: false` or `is_queryable: false`.
- Do not invent an AM, a budget, or an account ID. Missing means `—` or `n/a` with a note.
