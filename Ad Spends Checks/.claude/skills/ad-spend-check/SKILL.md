---
name: ad-spend-check
description: Weekly HiddenGem Meta Ads budget and spend audit. Compares documented daily budgets in the Master Meta Ads sheet against live budgets in each client's ad account, diffs against last week's run, and saves a dated plain-text report to the "Ad Spends Checks/Weekly Checks" folder. Use when the user says "run the ad spend check", "weekly spend audit", "budget audit", or invokes /ad-spend-check.
---

# Ad Spend Check

You are running the HiddenGem Marketing weekly Meta Ads budget and spend audit. Output is a plain-text report saved to the `Ad Spends Checks/Weekly Checks/` folder. No email is sent in this version.

Today's date comes from the environment. Use it as `YYYY-MM-DD` in filenames.

## Inputs

| Source | Where | What to take |
|---|---|---|
| Master Meta Ads sheet | Google Drive file `1B6lWqp_0linzf-3n4iqjJbavidZvyLO5yTY3MDhzYaM` (tab "Meta Ad Links") | Every client row regardless of status. Capture: Client Business, Status, Total Budget (documented $/day), Ads Account Link, Comments. |
| CRM sheet | Google Drive file `1oEUngQE3ZXc6U4ciRkkg55UrlR-M065kTmCzG8HFhM4` | Account manager (AM) per client. If a client appears in several tabs with different AMs, use the most recent tab. If no AM, show `—`. Never guess. |
| Meta ad accounts | `ads_get_ad_accounts`, paginate with `next_cursor` until null (expect 110+ across pages) | `ad_account_id`, `ad_account_name`, `business_name`, `is_ads_mcp_enabled`, `is_queryable`, `not_queryable_reason`. |
| Live budgets | `ads_get_ad_entities` per client account | See "Reading live budgets". |
| Previous report | Newest `Ad Spends Checks/Weekly Checks/*-ad-spend-check.csv` older than today | Prior Match flag and Notes per ad account ID, for the week-over-week diff. |
| Manual export (fallback) | Newest `Weekly CSV Reports/*_meta-ads-report.csv` | Ads Manager export used for accounts the connector cannot read. See "CSV fallback". |

Use one `client_conversation_id` for every Meta call in the run.

## Step 1: Read both sheets

Read the Master Meta Ads sheet with `read_file_content`. Take every client row. The first header cell is blank and columns can shift, so anchor on the header names, not positions. Normalise Status to one of `Live`, `Not Live`, `Paused`. Parse Total Budget as a number; blank or non-numeric means "no documented budget".

Read the CRM sheet and build a client -> AM map.

Match sheet clients to ad accounts by the account ID in the Ads Account Link column where present, otherwise by name. Record which method was used in Notes when it was name matching.

## Step 2: Fetch all ad accounts

Call `ads_get_ad_accounts` and follow `next_cursor` until it is null. Build a map by `ad_account_id`.

## Step 3: Read live budgets for every client

Do this for every client on the sheet, including Not Live and Paused. Spend on a dark account is the most important thing this report catches.

Access rules. Do not retry these. Before marking a 🔴 Blocker, check the CSV fallback below. If the account is in this week's export, score it from the CSV instead and note the source. Only if it is missing from the export too, flag and move on:

- `is_ads_mcp_enabled: false` -> 🔴 Blocker, Actual $/day `n/a`, note exactly: "Claude doesn't have access — please check the spend manually"
- Account not in the list at all -> 🔴 Blocker, note: "No account access — needs access fix"
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

Shawal drops an Ads Manager export into `Weekly CSV Reports/` each week. Use it only for accounts the connector cannot read (MCP disabled, not queryable, or absent from the account list). Never prefer it over a live read.

**File handling**
- Pick the newest file in `Weekly CSV Reports/`. If its name does not already follow `YYYY-MM-DD_Www_meta-ads-report.csv`, rename it to that pattern using today's date and ISO week (e.g. `2026-09-21_W39_meta-ads-report.csv`) before reading it. Tell the user you renamed it.
- Read the `Reporting starts` / `Reporting ends` columns. If `Reporting ends` is more than 7 days before today, treat the file as stale: do not use it, and flag the accounts as 🔴 with the note "CSV export is stale (ends YYYY-MM-DD), please re-export".

**Columns** (UTF-8 with BOM, ad set level, one row per ad set, first row is an account-wide total with a blank Account name; skip it):
`Account name, Campaign name, Ad set name, Currency, Campaign budget, Campaign budget type, Ad set budget, Ad set budget type, Amount spent (USD), Impressions, Link clicks, Purchases, Cost per purchase, Purchases conversion value, Leads, Cost per lead, Reporting starts, Reporting ends`

**Matching**: match `Account name` to the Meta ad account name from `ads_get_ad_accounts` (e.g. "Paradise Pointe Ads", "Bison Ridge Retreat Ad Account"). Fall back to the sheet client name if needed and say so in Notes.

**Computing Actual $/day from the CSV**
1. Group rows by Campaign name. If `Ad set budget` is "Using campaign budget", count the `Campaign budget` once per campaign. Otherwise sum the `Ad set budget` values for that campaign. Only `Daily` budget types count; a `Lifetime` budget is converted as lifetime / days in the reporting period and noted.
2. Actual $/day = sum across campaigns.
3. Also compute spend per day = total `Amount spent (USD)` / number of days in the reporting period. Show both in Notes.

**Known limitation**: the export has no delivery or status column, so it includes campaigns that were paused or replaced during the period. Budget totals from the CSV therefore tend to overstate what is live today. When spend per day is well below the budget total, say so and mark the flag as provisional. Ask the user to add the "Campaign delivery" and "Ad set delivery" columns to the saved report and export the last 7 days; once those columns exist, filter to Active rows only and drop the provisional marker.

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

Find the newest `Ad Spends Checks/Weekly Checks/*-ad-spend-check.csv` dated before today. If none exists, skip this step and write "First run, no prior report" in the Fixed section.

Join on `ad_account_id`. For each row that was ⚠️, ❌ or 🔴 last week:

- Now ✅ -> **Fixed**
- Still flagged, same or worse -> **Still open**, and add the week count (weeks flagged in a row, carried from the previous CSV's `weeks_open` + 1)
- Client no longer on sheet -> **Removed from sheet**

New flags this week are marked **New**.

## Step 6: Write the report

Write two files to `Ad Spends Checks/Weekly Checks/`:

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

Open `Project Data/PROJECT.md` and:

1. Add a row to **8. Run log** with today's date, mode (saved or chat only), the counts line, and whether files were written.
2. If the run revealed anything not already in **6. Learnings** (a new account quirk, a data-source change, a matching failure), add one bullet. Don't repeat what's there.
3. If a client → account mapping changed or a new client appeared on the sheet, update the table in **5. Client → ad account map**.
4. If an open decision in **7. Open decisions** was resolved during the run, mark it resolved with the date and outcome.

If the skill itself was changed during the session (thresholds, columns, sources, output location), add a dated bullet to `Project Data/CHANGELOG.md` describing what changed and why. Newest entries go at the top.

## Step 9: Publish the HTML and the archive

After the `.md` and `.csv` are written and the project files are updated:

```
python3 "Project Data/build_html.py" YYYY-MM-DD
python3 "Project Data/build_site.py"
git add -A && git commit -m "Reviews YYYY-MM-DD" && git push
npx netlify-cli deploy --prod --no-build --dir site --site f7b6b654-f0d8-4f24-9d69-03d351daff49
```

This regenerates this workflow's dated `.html` beside its `.md`, rebuilds `site/` and publishes it to `https://hiddengem-ads-reviews.netlify.app`. If the other two workflows have not run yet this week, run this anyway; the index shows "Not run this week" for them until they do.

## Do not

- Do not send email. That comes later.
- Do not skip Not Live or Paused clients.
- Do not call `ads_get_ad_entities` on an account with `is_ads_mcp_enabled: false` or `is_queryable: false`.
- Do not invent an AM, a budget, or an account ID. Missing means `—` or `n/a` with a note.
