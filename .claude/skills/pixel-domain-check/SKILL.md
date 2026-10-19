---
name: pixel-domain-check
description: Weekly HiddenGem Meta Pixel domain and event audit. Verifies every client's pixel is receiving events from that client's own domains, flags cross-contamination (another client's domain firing into a pixel), silent or low-volume pixels, and split/duplicate pixel setups. Diffs against last week and saves a dated plain-text report to "weekly/Meta Pixel Reviews/Weekly Checks". Use when the user says "run the pixel check", "pixel audit", "pixel domain check", or invokes /pixel-domain-check.
---

# Pixel Domain Check

You are running the HiddenGem Marketing weekly Meta Pixel domain audit. Goal: confirm each client's pixel receives events only from that client's own website, link-in-bio, GoHighLevel (GHL) funnel and booking-engine domains, and flag any pixel receiving events from a different client's domain (cross-contamination) or from a site that clearly isn't the client's. Output is a plain-text report saved to `weekly/Meta Pixel Reviews/Weekly Checks/`. No email is sent in this version.

Today's date comes from the environment. Use it as `YYYY-MM-DD` in filenames.

## Inputs

| Source | Where | What to take |
|---|---|---|
| Master Meta Ads sheet | Google Drive file `1B6lWqp_0linzf-3n4iqjJbavidZvyLO5yTY3MDhzYaM` | Tab "Meta Ad Links": every client row regardless of Status. Capture Client Business, Status, Attribution Tracking Setup (e.g. "(6/10) CAPI Setup (HG Ai)", "(3/10) Browser Events Only"). PMS tab (columns Client, Done, Integration Doable?, PMS): the client's PMS, used to recognise booking-engine hosts. Do not copy the API keys column anywhere. |
| Expected domains | `weekly/Meta Pixel Reviews/expected-domains.csv` | One row per client (and per pixel where a client has several): expected primary domains, accepted extra hosts, source (`sheet`, `confirmed`, `inferred`). This file is the source of truth for what "the client's own domain" means. The Master sheet has no website column. |
| Client → ad account map | `weekly/Project Data/PROJECT.md` section 5 | Ad account IDs per client. |
| Pixel inventory, domains, events, browser/server split | `npx tsx scripts/pull-pixel-stats.mts YYYY-MM-DD` from the repo root (Meta Marketing API, system-user token `META_ACCESS_TOKEN` in the repo-root `.env`), which writes `pixel_pull.json` next to this file | One entry per pixel: name, id, owning business, `last_fired_time`, which listings returned it (`hg_owned_pixels`, `hg_client_pixels`, `act_<id>`, `direct`), which client accounts it is attached to, `hosts` (count, first and last hour, per-day counts for the 7-day window), `events` (total per event name), `sources` (browser vs server), `total_events`, `server_events`, `error`. This file is the whole Meta read for the run. |
| Previous report | Newest `weekly/Meta Pixel Reviews/Weekly Checks/*-pixel-domain-check.csv` dated before today | Prior flag and notes per pixel ID for the week-over-week diff. |

The claude.ai Meta connector is not used for this report any more (Shawal, 2026-10-19); the script is the only Meta read. If `META_ACCESS_TOKEN` is missing, stop and say so.

## Step 1: Read the sheet and the expected-domains file

Read the Master sheet with `read_file_content`. It is large and gets saved to disk; parse it locally with Python. The first header cell is blank and columns can shift, so anchor on header names. Take every client on the "Meta Ad Links" tab, plus Attribution Tracking Setup. Read the PMS tab for each client's PMS.

Read `expected-domains.csv`. If a client on the sheet has no row, add one at the end of the run with `source=inferred` and flag the row ⚠️ "expected domain inferred, confirm".

## Step 2: Pull everything with the script

From the repo root:

```
npx tsx scripts/pull-pixel-stats.mts YYYY-MM-DD
```

The script reads the client map (section 5, Offboarded rows skipped) and the pixel map (section 5.1) from PROJECT.md, lists the HiddenGem BM's `owned_pixels` and `client_pixels` (business `158693423705448`), lists `act_<id>/adspixels` for every client account (what is attached where), reads directly any mapped pixel that no listing returned, and then pulls three `stats` aggregations for the last 7 days for every pixel that fired in the last 28 days or is in the pixel map: `host` (hourly buckets, folded into per-host totals with first/last hour and per-day counts), `event_total_counts` and `event_source`. It prints one line per pixel and writes `pixel_pull.json` in this folder. It takes a few minutes; run it in the background and carry on with step 1.

Access rules, do not retry:
- A listing error on an account (`account_errors` in the JSON) means the system user cannot see that account. The pixel may still be in the HG BM listing or readable directly; note "account not visible to the system user, pixel read via HG BM / directly".
- Pixel visible nowhere → 🔴 Blocker, note "No pixel found, confirm one exists or create one".
- Attached pixel silent (zero events) → before flagging, look for another pixel with the same `owner_business` that did fire (Tuxedo Falls' "Website" pixel, 2026-09-28). If one exists, give it its own ⚠️ row ("live but not shared to the ad account") and write the next action as share-or-swap.
- A pixel whose `error` field is set could not be read → 🔴 Blocker, note "Claude doesn't have access, please check the pixel manually".
- `is_unavailable` or `(not readable)` as the name: the pixel sits in a client business that has not shared it with HG and is not attached to any account the system user sees.

## Step 3: Read the pull

Work from `pixel_pull.json` with Python in the scratchpad, never by eye:

1. Dedupe is already done (one entry per pixel id). Match pixels to clients by the pixel map first, then by name and owning business for anything new. Every pixel that fired in the last 28 days gets its own row; pixels that never fired or last fired more than 28 days ago are listed in the Notes of the client's primary row ("also present, dead since …"), not as rows, unless the client has no other pixel.
2. Pixels in the HG BM that belong to no sheet client (test pixels, "Do Not Use", prospects) are listed once in a footer line, not in the table.
3. `total_events` is the 7-day total (the API returns one bucket per event name for the window; the script sums them). `hosts[*].daily` gives the per-day shape of each host, which is what settles "did the block work" questions.
4. `sources` splits events into browser and server (CAPI). A client whose sheet says CAPI but whose `server_events` is zero or under about 1% of the total gets the "CAPI effectively silent" warning.
5. EMQ is not pulled on this path; write "EMQ n/a" where the table needs it.

## Step 4: Classify each host

For each host on a pixel, decide which bucket it falls into:

| Bucket | Examples | Counts as |
|---|---|---|
| Client primary domain | `stayendless.com`, `www.selah.place` | expected |
| Client subdomain | `bio.`, `go.`, `links.`, `info.`, `book.`, `join.`, `shop.` on the client's domain | expected |
| Client second brand domain listed in expected-domains.csv | `awaytopa.com` for Away2PA | expected |
| GHL | `api.leadconnectorhq.com`, `sites.leadconnectorhq.com`, `go.<client>` | acceptable |
| Booking engine / PMS | `hotels.cloudbeds.com`, `us1.cloudbeds.com`, `booking.ownerrez.com`, `app.ownerrez.com`, `booking.hospitable.com`, `*.hospitable.rentals`, `*.guestybookings.com`, `resnexus.com`, `bookingsus.newbook.cloud`, `*.holidayfuture.com`, `*.bookeddirectly.host` | acceptable |
| Site builder static host | `*.filesusr.com` (Wix) | acceptable |
| HG staging / dev | `*.netlify.app` named after the client, `localhost`, `127.0.0.1` | acceptable, note it |
| Link services | `linktr.ee`, `www.facebook.com` | acceptable |
| **Another sheet client's domain** | `go.staysaluda.com` on the Inspired Retreats pixel | **❌ contamination** |
| Unknown domain | anything else | ⚠️ if under ~5% of events, ❌ if a meaningful share |

Build the set of all clients' expected domains first, then check every host on every pixel against the *other* clients' sets. That is how cross-contamination is found.

## Step 5: Flag each pixel row

| Flag | Rule |
|---|---|
| ✅ Match | Events > 0 and every host is expected or acceptable |
| ⚠️ Warning | Zero or very low events on a Live client (under ~100/day with an active budget); expected domain could only be inferred and does not contain the client's brand name; a minor unknown host with negligible volume; only a link-in-bio or booking-engine host is firing and the main site is absent; the client's funnel is split across two live pixels; two live pixels receive the same events (double counting); pixel exists but is not shared to the ad account; sheet says CAPI but `server_last_fired_time` is never |
| ❌ Critical | Any host that belongs to another client, at any volume; or a meaningful share of events from a domain that clearly isn't the client's. Always name the offending domain. |
| 🔴 Blocker | No pixel found anywhere, or the pixel cannot be read |

Inferred expected domains: on the first run every domain was inferred from the brand name plus observed traffic. Treat an inferred domain as confirmed when it contains the client's brand name (e.g. `bisonridgeretreat.com` for Bison Ridge Retreat). Only flag ⚠️ for inference when the domain does not (e.g. `canopytreehouse.com`, `parkerhouseohio.com`).

Cross-contamination callout: if a domain from client A appears on client B's pixel, write it up in the Critical section naming both clients, the domain, the share of B's events it represents, and since when. Also check A's own pixel to say whether the leak is one-way (A's pages carry B's pixel ID) or both ways.

Every ⚠️, ❌ and 🔴 row gets a one-line next action written for the account manager.

## Step 6: Week-over-week diff

Find the newest `*-pixel-domain-check.csv` dated before today. If none, write "First run, no prior report". Join on `pixel_id`. Rows flagged last week that are ✅ now → **Fixed**. Still flagged → **Still open** with `weeks_open` + 1. New flags → **New**. Pixels gone → **Removed**.

Also read `weekly/Project Data/PROJECT.md` section 9 (Actions log). A contamination row that Shawal reports as blocked mid-window may still carry a few foreign events from the first day of the window; read the daily buckets, and if the foreign host stops on the day of the block, call the row Fixed and say so in the note.

## Step 7: Write the report

Write two files to `weekly/Meta Pixel Reviews/Weekly Checks/`.

### `YYYY-MM-DD-pixel-domain-check.md`

Pipe tables, sections in this order:

1. Header line: date, clients on sheet, pixel rows reviewed, pixels receiving events correctly (✅ count), ❌ / ⚠️ / 🔴 counts, total events across all pixels in 7 days (count each shared pixel once).
2. **Critical issues** (❌ and 🔴), including the cross-contamination callout.
3. **Warnings** (⚠️).
4. **Fixed since last week.**
5. **All pixels**, alphabetical by client A→Z, no special handling of "The". Columns exactly: `Client | Pixel Name | Pixel ID | Events (last 7d) | Domains Seen | Expected Domain(s) | Match | Notes/Issues`. No account manager column.
6. Footer: clients on sheet, pixels found, with events / silent / blocked, total events, pixels in HG BM not on the sheet, previous report compared against, and the inferred-domain rule.

### `YYYY-MM-DD-pixel-domain-check.csv`

One row per pixel row in the table, header:

```
run_date,client,pixel_id,pixel_name,ad_account_id,events_7d,server_events,domains_seen,expected_domains,expected_source,flag,diff_status,weeks_open,notes
```

`flag` is `match`, `warning`, `critical`, `blocker`. `diff_status` is `new`, `still_open`, `fixed`, `unchanged`, `first_run`. `domains_seen` and `expected_domains` are `|`-separated.

## Step 8: Report back in chat

Give the header line, the Critical section and the Warnings table. Point to the file for the rest. Do not paste the full table.

## Step 9: Update the project files

1. `weekly/Project Data/PROJECT.md`: add a run log row; update section 5.1 if a pixel was added, removed or reassigned; add any new learning to section 6; resolve or add open decisions in section 7.
2. `weekly/Meta Pixel Reviews/expected-domains.csv`: add rows for new clients (`source=inferred`), and flip `inferred` to `confirmed` only when Shawal says so.
3. If the skill itself changed, add a dated bullet to `weekly/Project Data/CHANGELOG.md`.

## API quirks (learned 2026-10-13 and 2026-10-19)

- Every `stats` response carries `paging.next`, even when a single bucket already covers the window. Following it on `event_total_counts` or `event_source` repeats the bucket and inflates totals about 60x. The script only pages when a response is full (500 buckets); do not "fix" that.
- `host` returns hourly buckets (about 168 for 7 days); `event_total_counts` and `event_source` return one bucket for the window.
- The HG BM `client_pixels` edge returns pixels client businesses have shared with HiddenGem; `owned_pixels` the ones HG owns. Pixels in a client business that are neither shared nor attached to a visible account can only be read if the system user has been granted access.
- Older notes on the claude.ai connector (`ads_get_datasets` duplicates, hidden-dimension repeats in `event_total_counts`, quality time-outs) no longer apply.

## Step 10: Publish the HTML and the archive

After the `.md` and `.csv` are written and the project files are updated:

```
python3 "weekly/Project Data/build_html.py" YYYY-MM-DD
python3 "weekly/Project Data/build_site.py"
npx tsx scripts/sync-roi-memory.mts   # push the new rows to the roi schema in Supabase
git add -A && git commit -m "Reviews YYYY-MM-DD" && git push
```

This regenerates this workflow's dated `.html` beside its `.md`, rebuilds `public/weekly/` (the merged ROI dashboard serves it at `/weekly/`); Netlify deploys it with the dashboard on the next push to `main`. If the other two workflows have not run yet this week, run this anyway; the index shows "Not run this week" for them until they do.

## Do not

- Do not send email.
- Do not skip Not Live or Paused clients; a silent pixel on a paused account is still worth a row.
- Do not treat a booking-engine, GHL, Wix or netlify host as contamination.
- Do not invent an expected domain as fact; mark it inferred.
- Do not copy API keys from the PMS tab into any file.
