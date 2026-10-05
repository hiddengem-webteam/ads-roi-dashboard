# Ad Spend Check — 2026-10-05

Run: 5 October 2026 (live reads 09:05–09:55 PT, CSV export 2026-09-28 to 2026-10-04 for 5 accounts the connector cannot read). Third run, compared against 2026-09-28.

| Clients on sheet | Live reads | From CSV | Blocked | Documented Live $/day | Confirmed live $/day (live reads) | Documented for the same accounts |
|---|---|---|---|---|---|---|
| 42 | 36 | 5 | 0 | $2,890 | $2,435 | $2,330 |

## Issues, action needed

| Client | AM | Flag | Sheet $/day | Actual $/day | Status vs last week | Next action |
|---|---|---|---|---|---|---|
| Asheville River Cabins | Charlotte | ❌ | $80 | $0 | New | clear the unpaid balance or fix the payment method so the campaigns resume; the client is losing a full week of a Live budget |
| Columbia Gorge Getaways | Chiara | ❌ | $30 | $40 | Still open, week 3 | confirm the agreed budget with the client, then fix the sheet or the campaigns |
| Paradise Pointe | Makenna | ❌ | $100 | $150 | New | update the sheet to $150 and note the LoL test |
| Selah Place | Alicia | ❌ | $50 | $35 | Still open, week 2 | either raise BoF to bring the account back to $50 as planned, or set the sheet to $35 |
| Away2PA | Alicia | ⚠️ | $40 | $40 | Still open, week 3 | remove or correct the comment |
| Big Moon Ranch | Charlotte | ⚠️ | $50 | n/a | Still open, week 3 (was blocker) | remove the row from the sheet or set Status to Not Live. AM carried from earlier reports; no CRM row. The HG BM pixel on bigmoonranch.com is still firing (see pixel check) |
| Canopy at Moody Moon Ridge | Kristal | ⚠️ | — | $0 | Still open, week 3 | confirm whether the account is meant to be paused; if so set the sheet Status to Paused, otherwise add a budget. AM carried from last week (no row in the CRM onboarding export) |
| FLOHOM | Makenna | ⚠️ | $250 | $220 | Still open, week 3 | update the sheet to $220 or confirm the target is still $250 |
| Little River Landing | Makenna | ⚠️ | — | $65 | Still open, week 2 | repair the budget cell on the sheet ($65) |
| Ridge & Falls | Makenna | ⚠️ | — | $60 | Still open, week 2 | repair the budget cell on the sheet ($60) |
| Stay With Branch | Kristal | ⚠️ | $20 | $20 | New | open the account and check for a payment, ad-review or audience issue on both campaigns |
| Stay on 30a | Charlotte | ⚠️ | $400 | $450 | Still open, week 3 | update the sheet to $450 or confirm |
| Three Suns Cabins | Kristal | ⚠️ | $15 | $15 | Still open, week 3 | confirm the October budget with the client and update the note |

## Fixed since last week

| Client | AM | Last week | This week | What changed |
|---|---|---|---|---|
| Endless Stays | Nicole | ❌ $200 vs $50 sheet | ✅ $200 vs $200 sheet | Sheet updated to $200 since last week. Budgets were rebalanced inside the same total: Giveaway $75 (was $100) + BoF $75 (was $50) + MoF Lead $50 = $200/day; spend $1,390 in 7 days ($199/day), so the account is now delivering its full budget. |

## All accounts

| Client | AM | Sheet Status | Sheet $/day | Actual $/day | Match | Notes/Issues |
|---|---|---|---|---|---|---|
| American River Resort | Nicole | Live | $50 | $50 | ✅ | 2 campaigns (Giveaway $30, Leads $20). |
| Asheville River Cabins | Charlotte | Live | $80 | $0 | ❌ | source: CSV export 2026-09-28 to 2026-10-04, not live. The connector now lists the account as UNSETTLED (unpaid balance) and not queryable. In the export all three campaigns (Giveaway $40, BoF $30, MoF $10 = $80 configured) show Campaign delivery = not_delivering, and the account spent only $90 in the 7 days ($13/day) against an $80/day sheet budget, so delivery stopped around 29 Sep. Treated as $0 active. Next action (Charlotte): clear the unpaid balance or fix the payment method so the campaigns resume; the client is losing a full week of a Live budget. |
| Away2PA | Alicia | Live | $40 | $40 | ⚠️ | Week 3: live matches the $40 budget (Giveaway $30 + MoF $5 + BoF $5), but the sheet comment still says "Its on $60/day". Next action (Alicia): remove or correct the comment. |
| Awayframes | Alicia | Live | $30 | $30 | ✅ |  |
| Best Texas Travel | Nicole | Live | $30 | $30 | ✅ |  |
| Big Moon Ranch | Charlotte | Live | $50 | n/a | ⚠️ | Offboarded on 2026-09-28 (actions log), so no longer a blocker, but the row is still on the Master sheet as Live with a $50 budget. Account 758851247064974 is absent from the connector list and the export. Next action (Charlotte): remove the row from the sheet or set Status to Not Live. AM carried from earlier reports; no CRM row. The HG BM pixel on bigmoonranch.com is still firing (see pixel check). |
| Bison Ridge Retreat | Chiara | Live | $30 | $30 | ✅ | source: CSV export 2026-09-28 to 2026-10-04, not live. 3 active campaigns: Discovery $20 + BoF $5 + MoF $5 = $30, spend $210 in 7 days ($30/day). |
| Canopy at Moody Moon Ridge | Kristal | Live | — | $0 | ⚠️ | Week 3: no documented budget on the sheet (comment: "Removed the budget since its changing regularly"), still no active campaigns and $0 in the last 7 days. Next action (Kristal): confirm whether the account is meant to be paused; if so set the sheet Status to Paused, otherwise add a budget. AM carried from last week (no row in the CRM onboarding export). |
| Columbia Gorge Getaways | Chiara | Live | $30 | $40 | ❌ | Week 3: Discovery $20 + BoF $15 + MoF $5 = $40, still $10 over the $30 sheet (33%). The new lead campaign Shawal launched 28 Sep (actions log, Done) replaced the July one at the same $5. Next action (Chiara): confirm the agreed budget with the client, then fix the sheet or the campaigns. |
| Endless Stays | Nicole | Live | $200 | $200 | ✅ | source: CSV export 2026-09-28 to 2026-10-04, not live. Sheet updated to $200 since last week. Budgets were rebalanced inside the same total: Giveaway $75 (was $100) + BoF $75 (was $50) + MoF Lead $50 = $200/day; spend $1,390 in 7 days ($199/day), so the account is now delivering its full budget. |
| Evergreen Cabins | Nicole | Live | $40 | $40 | ✅ |  |
| FLOHOM | Makenna | Live | $250 | $220 | ⚠️ | Week 3: 5 active campaigns = $220/day (BoF $90, Lookalike $80, Myrtle Beach Lookalike $20, Lead $20, Giveaway $10), 12% under the $250 sheet; spend $1,536 in 7 days ($219/day). Next action (Makenna): update the sheet to $220 or confirm the target is still $250. |
| Green Springs Inn | Alicia | Live | $40 | $40 | ✅ | One old boosted post (Mother's Day Brunch) still ACTIVE on an exhausted $50 lifetime budget, not spending. |
| Hiawassee Glamping | Alicia | Live | $30 | $30 | ✅ |  |
| Home Base | Charlotte | Live | $50 | $50 | ✅ |  |
| Inspired Retreats | Makenna | Live | $60 | $60 | ✅ | Queried "Inspired Retreats Ads 2.0" under HG BM. |
| Little River Landing | Makenna | Live | — | $65 | ⚠️ | Week 2: sheet budget cell still reads #REF! (broken formula), so there is no documented budget to compare against. Live: Giveaway $55 + BoF $5 + MoF $5 = $65, unchanged. Next action (Makenna): repair the budget cell on the sheet ($65). |
| Myrinn | Kristal | Live | $30 | $30 | ✅ | Account sits under HG Marketing BM. |
| Nature Nooks | Kristal | Live | $30 | $30 | ✅ | Giveaway $10 + Keyword Engagement $10 + MoF Lead $10. |
| North Star Resort & Lodge | Charlotte | Live | $30 | $30 | ✅ | Total unchanged at $30 but the structure changed: Giveaway cut from $30 to $20, new BoF retargeting campaign (09/09, $5) and new MoF lead campaign (10/02, $5, launched 2 Oct, no spend yet). |
| Oak & Ember | Chiara | Live | $30 | $30 | ✅ |  |
| Paradise Pointe | Makenna | Live | $100 | $150 | ❌ | source: CSV export 2026-09-28 to 2026-10-04, not live. New: a lookalike sales campaign "MoF - LoL Sales Campaign - 09/28/26" at $50/day sits beside BoF $50 + MoF Lead $25 + Giveaway $25 = $150/day, 50% over the $100 sheet; spend $1,037 in 7 days ($148/day). Shawal's 29 Sep change note already records this ("ad spend at $150/day for now"), so the budget is intentional and only the sheet is behind. Next action (Makenna): update the sheet to $150 and note the LoL test. |
| Parker Reserve | Kristal | Live | $10 | $10 | ✅ | 4-Campaign Structure column says Not Live, Status says Live; one $10 Discovery campaign live. |
| Ponderosa Pines Resort | Anna | Live | $100 | $100 | ✅ | source: CSV export 2026-09-28 to 2026-10-04, not live. Retarget $40 + Discovery $40 + Leads $20 = $100, spend $702 in 7 days ($100/day). |
| Raven Rock Mountain | Kristal | Not Live | — | $0 | ✅ | No active campaigns, correct for Not Live. |
| Red White & Blue Views | Nicole | Live | $45 | $45 | ✅ |  |
| Ridge & Falls | Makenna | Live | — | $60 | ⚠️ | Week 2: sheet budget cell still reads #REF!, so there is no documented budget to compare against. Live: Giveaway $50 + BoF $5 + MoF $5 = $60, unchanged. The lead-campaign relaunch planned on 28 Sep (actions log) has not happened: the 09/01 lead campaign is still the active one. Next action (Makenna): repair the budget cell on the sheet ($60). |
| Selah Place | Alicia | Live | $50 | $35 | ❌ | Week 2, changed direction: the $100/day prospecting test is no longer active (actions log: paused, Done) and the account is back to ACTIVE and queryable, so the payment error is cleared. But the plan to move the test budget into the BoF retargeting campaign has not happened: BoF is still $15, so live is Giveaway $15 + BoF $15 + Lead $5 = $35/day, 30% under the $50 sheet; spend $264 in 7 days ($38/day). Sheet comment now reads "Additional campaign started by Owner". Next action (Alicia): either raise BoF to bring the account back to $50 as planned, or set the sheet to $35. |
| Starlight Haven - Hot Springs | Charlotte | Live | $75 | $75 | ✅ | Budgets at ad set level (6 active ad sets: $25 + $15 + $10 + $10 + $10 + $5). |
| Starlight Haven - Weiss Lake | Charlotte | Live | $65 | $70 | ✅ | Budgets at ad set level (5 active ad sets: $25 + $20 + $10 + $10 + $5 = $70, $5 over sheet, within tolerance). Only 2 campaigns are active now; the Discovery campaign counted last week is no longer active, total unchanged. |
| Stay on 30a | Charlotte | Live | $400 | $450 | ⚠️ | Week 3: MoF LoL $180 + BoF $120 + Giveaway $100 + MoF Leads $50 = $450, 12.5% over the $400 sheet; spend $3,161 in 7 days ($452/day). Next action (Charlotte): update the sheet to $450 or confirm. |
| Stay Saluda NC | Makenna | Live | $80 | $80 | ✅ | Giveaway $30 + BoF $30 + MoF $20 = $80. |
| Stay Southern Illinois | Chiara | Live | $30 | $30 | ✅ |  |
| Stay With Branch | Kristal | Live | $20 | $20 | ⚠️ | Budgets match the sheet (MoF $5 + Discovery $15 = $20) but the account spent only $59 in 7 days ($8.50/day) and both campaigns still showed their full daily budget remaining at the time of the read, so delivery has stalled since about 1 Oct (the pixel's traffic dropped at the same time). Flagged on delivery, not on budget. Next action (Kristal): open the account and check for a payment, ad-review or audience issue on both campaigns. |
| StayLuxe | Kristal | Live | $20 | $20 | ✅ | New "ToF Winter - Giveaway Traffic Campaign - CA/VA/NV - 10/01/26" launched 1 Oct with a $10 ad set budget, MoF $5 + BoF $5 on campaign budgets = $20. |
| Sunapee Stays | Charlotte | Live | $50 | $50 | ✅ |  |
| Taberg Falls | Alicia | Live | $400 | $360 | ✅ | 10% under sheet, at the match threshold. Shawal's 28 Sep changes (actions log, Done) show in the account: new Broad sales campaign $50 + Lookalike cut to $50 + BoF $100 + Giveaway $100 + Leads $60 = $360. |
| The Cohost Company | Makenna | Live | $130 | $130 | ✅ |  |
| The Outpost | Anna | Live | $40 | $40 | ✅ | 3 campaigns = $40. A boosted post still shows a $12.58 daily budget but ended 22 May; 3 boosted posts on exhausted lifetime budgets; archive pass still recommended. |
| Three Suns Cabins | Kristal | Live | $15 | $15 | ⚠️ | Week 3: matches at $15, but the sheet note "Running at $15 until Sept" has expired. Next action (Kristal): confirm the October budget with the client and update the note. |
| Treetop Escapes | Makenna | Live | $100 | $100 | ✅ |  |
| Tuxedo Falls | Chiara | Live | $30 | $30 | ✅ |  |

## Footer

- Clients on sheet: 42 (41 Live, 1 Not Live/Paused)
- Live connector reads: 36. Scored from CSV export: 5 (Asheville River Cabins joins the CSV set this week because the connector lists it as UNSETTLED / not queryable). Blocked: 0. Offboarded but still on the sheet: 1 (Big Moon Ranch)
- Confirmed daily budget across live-read accounts: $2,435 vs $2,330 documented
- Including CSV-scored accounts: $2,915 vs $2,840 documented
- Flags: 4 ❌, 0 🔴, 9 ⚠️, 29 ✅. Diff vs 2026-09-28: 3 new, 10 still open, 1 fixed, 28 unchanged
- Previous report: 2026-09-28-ad-spend-check.csv
- Actions log entries checked (PROJECT.md section 9): Columbia Gorge Getaways new lead campaign Done; Selah Place test paused Done but the BoF budget move is still Planned; Ridge & Falls relaunch still Planned; Tàberg Falls restructure Done; Big Moon Ranch offboarded Done. Paradise Pointe's new $50 LoL campaign matches Shawal's 29 Sep change note and is added to the log as Done.
- Stay With Branch is the only ⚠️ raised on delivery rather than budget: budgets match the sheet but the account spent 40% of them; the skill has no rule for this, so it is a judgement call and is noted here.
- Sheet changes since last week: Endless Stays budget $50 → $200 (now matches), Selah Place comment added, Canopy still blank, Ridge & Falls and Little River Landing still #REF!.
- Ad set level budgets: Starlight Haven Hot Springs and Weiss Lake (all campaigns) and StayLuxe's new ToF Winter campaign were read at ad set level and summed. Budgets came back in dollars this week, not cents.

## Not on the sheet

Active ad accounts with spend in the export and no Master sheet row: Edenwood NC and HiddenGem Marketing are still present; Branch Berkeley Springs has dropped out of the export this week (41 accounts in the file, 42 last week). Not checked. Decision pending on adding them.
