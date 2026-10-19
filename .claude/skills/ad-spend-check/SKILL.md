---
name: ad-spend-check
description: Weekly HiddenGem Meta Ads spend ledger. Reads the live daily budget of every client's ad account through the Meta Marketing API, splits it by campaign type (ToF Giveaway, MoF Leads, MoF Sales LoL, BoF Sales), diffs against the previous run, saves a dated report to "weekly/Ad Spends Checks/Weekly Checks" and rewrites the Master Meta Ads sheet's "Meta Ad Spends" tab with the current ledger. Use when the user says "run the ad spend check", "weekly spend audit", "ad spend report", or invokes /ad-spend-check.
---

# Ad Spend Check

You are running the HiddenGem Marketing weekly Meta Ads spend check. It reports what each client's ad account is set to spend per day, by campaign type, and how that moved since the previous run. It does **not** compare against the documented budget on the Master sheet (that comparison was dropped on 2026-10-15 at Shawal's request; reports up to 2026-10-13 still carry it).

Output: `weekly/Ad Spends Checks/Weekly Checks/YYYY-MM-DD-ad-spend-check.{md,csv,html}`, plus the **Meta Ad Spends** tab of the Master Meta Ads sheet rewritten with the current ledger (one row per client, previous run replaced; history lives in the dated CSVs). No email.

Today's date comes from the environment. Use it as `YYYY-MM-DD` in filenames.

## Inputs

| Source | Where | What it gives |
|---|---|---|
| Client map | `weekly/Project Data/PROJECT.md` section 5 | Client, AM, ad account ID. Rows whose Connector cell starts with **Offboarded** are skipped (Big Moon Ranch 2026-09-28, Canopy at Moody Moon Ridge 2026-10-15). |
| Meta Marketing API | system-user token `META_ACCESS_TOKEN` in the repo-root `.env` (gitignored) | Active campaigns, their daily budgets (or their active ad sets' budgets), objective, stop time; account spend for the last 7 days. |
| Previous run | newest `*-ad-spend-check.csv` dated before today in the output folder | Last run's total per account and, from 2026-10-15 on, its campaign list, for the week-over-week diff. |
| Master Meta Ads sheet | Google Sheets `1B6lWqp_0linzf-3n4iqjJbavidZvyLO5yTY3MDhzYaM`, tab "Meta Ad Links" | Only to spot clients on the sheet that are missing from the client map (step 3). The Total Budget column is not used. |

## Step 1: Generate the report

From the repo root:

```
npx tsx scripts/ad-spend-check.mts YYYY-MM-DD
```

The script reads every non-offboarded client in the map, pulls each account's ACTIVE campaigns (campaign `daily_budget`, else the sum of its ACTIVE ad sets' `daily_budget`; cents divided by 100; campaigns past their `stop_time` ignored), buckets them by objective first and then name into ToF Giveaway / MoF Leads / MoF Sales LoL / BoF Sales / Other, reads the account's 7-day `spend`, and diffs the totals and campaign lists against the previous run. It writes:

- `YYYY-MM-DD-ad-spend-check.csv`: `run_date, client, am, ad_account_id, source, tof_giveaway, mof_leads, mof_sales_lol, bof_sales, other, total_live, spend_7d, prev_total, change, status, what_changed, campaigns`. `source` is `live` or `blocked`; `status` is `up`, `down`, `new`, `unchanged`, `blocked` or `first_run`.
- `YYYY-MM-DD-ad-spend-check.md`: header line with the live-read window, a `Meta Ad Spends tab: not pushed yet.` line, the counts table, **Changes since last week**, **Live spend by client** (sorted by total $/day, highest first) and the **Footer**.

If the script reports an account as blocked, do not retry. Note it in the chat summary; the row stays in the report with `n/a` figures. If `META_ACCESS_TOKEN` is missing, stop and say so; there is no connector fallback for this report.

## Step 2: Replace the Meta Ad Spends tab with this run's rows

With the Google Sheets connector:

1. `get_values` on `'Meta Ad Spends'!A1:K1`. The layout (Shawal, 2026-10-15) is
   `Last Update Data | Client | AM | Update source | Total live $/day | ToF Giveaway | MoF Leads | MoF Sales LoL | BoF Sales | Other | Campaign details`.
   If the tab is ever empty, write that header at `A1` first.
2. `get_values` on `'Meta Ad Spends'!B:B` to find the last used row of the previous run.
3. `update_values` on `'Meta Ad Spends'!A2:K<last>` with one row per client from the CSV, sorted by `total_live` descending (ties by client name), followed by rows of empty strings down to the previous last row so nothing from the old run is left behind (Shawal, 2026-10-19: the tab shows the current ledger, it does not accumulate runs; `batch_clear_values` is not permitted, so blank cells are written instead):
   - `Last Update Data`: the run date as text on the first row only, blank on the rest.
   - `Update source`: `Live API` (the normal case); `Live API (blocked, no data)` for a blocked account.
   - Budgets as numbers; `Campaign details` is the CSV's `campaigns` cell.
   Never touch any other tab.
4. Read `'Meta Ad Spends'!B:B` back once and check the non-empty count equals the CSV's client count plus the header.
5. Replace the `Meta Ad Spends tab: not pushed yet.` line in the `.md` with `Meta Ad Spends tab: replaced YYYY-MM-DD HH:MM PT, N rows (rows 2 to B).` using the time of the write. The HTML shows this line as a chip.

If the Sheets connector is not available, leave the line as `not pushed yet`, say so in chat, and do not edit the sheet any other way.

## Step 3: Cross-check the Master sheet for new clients

`get_values` on `'Meta Ad Links'!B:B` (Client Business). Any name there that is not in the client map and not marked Offboarded gets a footer bullet in the `.md`: `- On the Master sheet but not in the client map: <names>. Add the ad account ID to PROJECT.md section 5 to include them next week.` (Glasscombe on 2026-10-15.) Do not look up or invent the account ID during the run; raise it in chat.

## Step 4: Report back in chat

Give the counts line (clients, live reads, blocked, total live $/day with the four type totals, spent last 7 days), the Changes table, and the Meta Ad Spends tab line. Point to the file for the ledger; do not paste it.

## Step 5: Update the project file

In `weekly/Project Data/PROJECT.md`:

1. Add a row to **8. Run log**: date, workflow, mode, the counts line with the notable changes, and whether files were written.
2. Add a bullet to **6. Learnings** only for something new (an account quirk, a bucketing miss, a data-source change).
3. Update **5. Client → ad account map** if a client was added, offboarded or remapped.
4. Resolve an **7. Open decisions** row if the run settled it.

If the skill, the script or the output format changed during the session, add a dated bullet at the top of `weekly/Project Data/CHANGELOG.md`.

## Step 6: Publish

```
python3 "weekly/Project Data/build_html.py" YYYY-MM-DD
python3 "weekly/Project Data/build_site.py"
npx tsx scripts/sync-roi-memory.mts   # needs SUPABASE_SERVICE_ROLE_KEY in .env.local; skip and say so if unset
git add -A && git commit -m "Reviews YYYY-MM-DD" && git push
```

`build_html.py` renders the `.md` and `.csv` to the dated `.html` (it still renders the pre-2026-10-15 sheet-comparison reports with their old layout); `build_site.py` rebuilds `public/weekly/`, which Netlify deploys with the dashboard on the next push to `main`.

## Do not

- Do not compare live budgets against the Master sheet's Total Budget, and do not flag Match / Warning / Critical. Budget discrepancies are the AMs' job to read off the tab.
- Do not send email.
- Do not invent an AM, a budget or an account ID. Missing means `—` or `n/a`.
- Do not retry a blocked account or fall back to an Ads Manager export; note it and move on.
