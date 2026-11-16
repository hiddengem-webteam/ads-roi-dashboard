---
name: post-review
description: Monday Meta Ads post-review, run after the ad spend, pixel and client benchmark checks. Reviews the benchmark's flagged (Action needed), scale and frequency-watch accounts plus new CRM clients with every data source (ad-level Meta pull, budgets by campaign type, pixel/Purchase check, CRM spend range and ROAS goal, PMS month to date, monthly ROI, meeting notes, open Fix List tasks), writes short budget and creative recommendations, adds tasks to the Meta Ads Fix List, drafts one creative message per AM, builds the post-review page on the weekly site and emails Shawal a summary through Mailtrap. Use when the user says "run the post-review", "after reviews", "check flagged and scale accounts", or invokes /post-review.
---

# Post-review

Set up 2026-11-16 (Shawal). It runs after `/ad-spend-check`, `/pixel-domain-check` and `/client-benchmark` for the same date. Their dated `.md`/`.csv` files must exist first.

Output:
- `weekly/Post-Review/Weekly Checks/DATE-post-review.json` (the recommendations; the page and the email are built from it), `.html` and `-email.html`.
- New tasks on the Meta Ads Fix List (https://claude.ai/artifact/5Zraak85dw6QaXeFWVJWJn), source `post-review-DATE`.
- `/weekly/post-review/DATE.html` on the weekly site.
- One email to shawal@hiddengem.media.

Working files go in `weekly/Post-Review/inputs/` and `.claude/skills/post-review/ads.json`. Both are gitignored and rebuilt every run.

## Steps

0. **Mailtrap preflight**: `npx tsx scripts/send-post-review-email.mts DATE --check`. It prints the sender the run will use. Mailtrap only, per the HiddenGem email rule. If no domain can send, say so now and carry on: the page and the tasks still get done, and the email content goes in chat at the end.

1. **CRM**: use the Google Sheets connector on spreadsheet `1oEUngQE3ZXc6U4ciRkkg55UrlR-M065kTmCzG8HFhM4`, tab `Clients - Onboarding`, rows 3 to 60. Read these ranges: `B3:C60` (client, AM), `K3:L60` (Kickoff Call, Funnel Build Due), `S3:S60` (Meta Ads tier), `AN3:AN60` (Share Access to Meta Business Assets), `AY3:AY60` (Ad Campaign Setup), `BS3:BY60` (Setup, Ad Spend Range, ROAS Goal, EMQ, PMS, PMS Connection, Meta Pixel Connection). Rewrite `.claude/skills/post-review/crm.json` with today's `read` date. Keep its `cols` order and write one row per client. Trailing empty cells come back missing, so pad each row to 14 values. The rows must line up with column B.

2. **Fix List dump**: run `rm -rf weekly/Post-Review/inputs/fixlist`. Then call ArtifactData `query` on the Fix List artifact twice, once for collection `tasks` and once for `accounts`. Use `query: {"limit": 1000}` and `out_dir: <repo>/weekly/Post-Review/inputs/fixlist`. `.claude/` is not allowed as an out_dir.

3. **Ad-level pull**: `npx tsx scripts/pull-ad-insights.mts DATE` takes about 3 minutes for 27 accounts. It writes `ads.json`: access to each account and pixel, campaigns with their first and last spend dates, and 7/14/30-day ad insights plus creative copy for every active ad. Accounts come from `ADV` in the client benchmark's `generate_report.py`. A client that is new to the benchmark needs its ADV entry first.

4. **Brief**: `python3 .claude/skills/post-review/build_context.py DATE` writes `weekly/Post-Review/inputs/DATE-context.md`. Read all of it. For each listed client it has the list rows, CRM range use (live $/day × 30.4 against the monthly range), live budgets by campaign type, the pixel and Purchase read, the benchmark's own client block (this month, monthly ROI, meetings, HG AI notes), the ads in the listed campaigns with tiredness flags, reels already scripted in `video/specs`, and open Fix List tasks. The new-client section judges each client against the CRM's Funnel Build Due + 7 days. It counts HiddenGem campaigns by creator, so it ignores the client's and previous agencies' campaigns.

5. **Write the recommendations**: save `weekly/Post-Review/Weekly Checks/DATE-post-review.json` in the shape below and follow the rules in the next section.

6. **Tasks**: run `python3 .claude/skills/post-review/prepare_tasks.py DATE`. It skips any id that is already on the Fix List, writes one JSON file per new task and per missing accounts doc, fills `task_index` and `tasks_added`, and writes `weekly/Post-Review/inputs/DATE-fixlist/writes.json`. Pass that array as `writes` to ArtifactData `batch` on the Fix List. Each entry has a `file_path`, so nothing is retyped. To change a task already written, use ArtifactData `update` with its `if_version`, then edit the JSON to match.

7. **Page**: run `python3 "weekly/Project Data/build_html.py" DATE` (it rebuilds all four pages for the date), then `python3 "weekly/Project Data/build_site.py"`. Check it with headless Chrome at 1440 px wide, and at phone width through a 390 px iframe.

8. **Email**: `npx tsx scripts/send-post-review-email.mts DATE`. The email has the status line, the summary, "Do this week", one line per client with its next step, the new clients to chase and the AM messages. The full page is attached. When `WEEKLY_SITE_URL` is set in `.env`, the email also links to `/weekly/post-review/DATE.html`, so send it after the push. `--dry-run` writes the HTML without sending.

9. **Close**: add a row to `weekly/Project Data/PROJECT.md` section 8 (Run log). Commit with explicit paths: `weekly/Post-Review/Weekly Checks/DATE-*`, `public/weekly`, plus any code you changed. Push only when Shawal says so. Ask open questions with AskUserQuestion.

## JSON shape

```json
{
 "run_date": "YYYY-MM-DD",
 "summary": "2 sentences: the headline call for the week",
 "top_actions": [{"client": "", "text": "one sentence", "task": "task-id"}],
 "sections": {
  "flagged":   [ITEM], "scale": [ITEM], "frequency": [ITEM],
  "new_clients": [{"client": "", "am": "", "status": "live|due|late|blocked|not-started|watch", "metric": "", "read": "", "flags": [], "next": [], "tasks": []}]
 },
 "am_messages": [{"am": "", "clients": [], "message": "plain text, \n for new lines"}],
 "new_tasks": [{"id": "client-topic", "account": "Fix List account name", "priority": "fix|followup|structure|confirm|minor|tidy|deferred", "change": "", "where": ""}],
 "data_notes": []
}
ITEM = {"client", "am", "campaign", "type", "status": "flag|review|scale|freq", "metric": "numbers on one line",
        "read": "one sentence", "budget": [], "creative": [], "context": ["data behind it"], "tasks": ["existing and new ids"]}
```

The first entry of `budget`, then `creative`, then `next` is the email's one line for that client, so put the most important action first.

## Rules for the recommendations

- **Short.** `read` is one sentence of at most about 30 words. Each action is one sentence with the numbers in it. Top actions: at most 6, most urgent first.
- **Link before adding.** If an open Fix List task already covers the action, put its id in `tasks` and don't add a new one. A new task id is `<client-short>-<topic>`, lowercase with hyphens.
- **Scale is checked against the CRM Ad Spend Range.** The range is a monthly budget. Compare live $/day × 30.4 against it. At or over the range, recommend a shift inside the account, or a `confirm` task to get the client's OK and update the CRM, never a plain increase. The 11 Nov Meta Ads Sync set a 5x minimum ROAS for scaling, and the client's ROAS goal applies on top of that.
- **Tracking first.** When the pixel check shows a Purchase over-count (two senders) or under-capture, the ROAS is not reliable. Fix the tracking before any budget call, and say so in the `read`.
- **The 4-campaign structure.** Only Stay On 30A, Táberg, Paradise Pointe, FLOHOM and Awayframes run all four campaigns (13 Nov). The 14 Oct Strategy call limits the 4th campaign to clients with elevated tracking. For everyone else, shift budget between the campaigns they already run.
- **Frequency.** Refresh the creative first. When the new ads go in, pause the most tired ad (high ad-level frequency with 0 purchases). If BoF frequency is above 5 on a small budget, the audience is small, so don't add budget.
- **Creative ideas: 2 or 3 for each flagged or frequency client.** Base them on what is running: ad names, copy, age, hook rate and CTR trend. Check `video/specs`, the 22 Oct review pack (`video/out/team-review-2026-10-22`) and the open tasks first, and name an existing reel by its hook line before asking for new footage.
- **Hands off.** Never recommend stopping a campaign in `DEFERRED` (generate_report.py), and never change a client-run campaign. The brief labels both. Dunya Camp's 'Fall step 2' / 'Step 3' funnel stays as it is (Shawal, 12 Nov).
- **New clients.**
  - `due`: the deadline is ahead and campaigns are not live.
  - `late`: the deadline has passed.
  - `blocked`: no Meta access, no tier or no dates, so nothing can move.
  - `live`: running, with any gaps listed as `flags`.

  Access means the system user can read the ad account and pixel. The CRM's "Share Access" column is only a manual tick. List CRM gaps (range $0, missing dates) as `flags` with a `tidy` or `confirm` task.
- **AM messages.**
  - One message per AM, covering every creative ask for their clients.
  - Friendly and direct, in Shawal's voice. No em dashes.
  - Name reels by their hook line.
  - Ask for QA, footage or Drive sharing, not strategy.
