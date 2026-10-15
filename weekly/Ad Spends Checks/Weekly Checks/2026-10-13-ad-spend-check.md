# Ad Spend Check — 2026-10-13

Run: 13 October 2026 (Tuesday; live reads 11:20–11:35 PT through the Meta Marketing API with the HiddenGem-Claude system user, because the claude.ai Meta connector was not reachable; CSV export 2026-10-05 to 2026-10-11 for 1 account the system user cannot read). Fourth run, compared against 2026-10-05.

| Clients on sheet | Live reads | From CSV | Blocked | Documented Live $/day | Confirmed live $/day (live reads) | Documented for the same accounts |
|---|---|---|---|---|---|---|
| 43 | 41 | 1 | 0 | $2,920 | $3,063 | $2,870 |

## Issues, action needed

| Client | AM | Flag | Sheet $/day | Actual $/day | Status vs last week | Next action |
|---|---|---|---|---|---|---|
| Columbia Gorge Getaways | Chiara | ❌ | $30 | $40 | Still open, week 4 | confirm the agreed budget with the client, then fix the sheet or the campaigns |
| Paradise Pointe | Makenna | ❌ | $100 | $150 | Still open, week 2 | update the sheet to $150 |
| Walden Retreats | Anna | ❌ | $30 | $48 | New (new on the sheet) | confirm the wedding test with the client and put the agreed total on the sheet, or pause the test. Matched by account ID 973261794434226 (the export names the account by its ID) |
| Away2PA | Alicia | ⚠️ | $40 | $40 | Still open, week 4 | remove or correct the comment |
| Big Moon Ranch | Charlotte | ⚠️ | $50 | n/a | Still open, week 4 | remove the row from the sheet or set Status to Not Live. AM carried from earlier reports; no CRM row |
| Canopy at Moody Moon Ridge | Kristal | ⚠️ | — | $0 | Still open, week 4 | confirm whether the account is meant to be paused; if so set the sheet Status to Paused, otherwise add a budget. Also grant the HiddenGem-Claude system user access to the account. AM carried from last week |
| FLOHOM | Makenna | ⚠️ | $250 | $220 | Still open, week 4 | update the sheet to $220 or confirm the target is still $250 |
| Little River Landing | Makenna | ⚠️ | — | $65 | Still open, week 3 | repair the budget cell on the sheet ($65) |
| Ridge & Falls | Makenna | ⚠️ | — | $60 | Still open, week 3 | repair the budget cell on the sheet ($60) |
| Stay on 30a | Charlotte | ⚠️ | $400 | $500 | Still open, week 4 | update the sheet to $500 or confirm the agreed ceiling |
| Taberg Falls | Alicia | ⚠️ | $400 | $300 | New | confirm the new $300 level with the client and update the sheet, or restore the budgets |
| The Outpost | Anna | ⚠️ | $40 | $50 | New | pause the old 08/29 BoF if the 10/.. one replaces it, then the account is back at $40 |
| Three Suns Cabins | Kristal | ⚠️ | $15 | $15 | Still open, week 4 | confirm the October budget with the client and update the note |

## Fixed since last week

| Client | AM | Last week | This week | What changed |
|---|---|---|---|---|
| Asheville River Cabins | Charlotte | ❌ $0 vs $80 sheet | ✅ $80 vs $80 sheet | Giveaway $40 + BoF $30 + MoF $10 = $80; spend $646 in 7 days ($92/day, catching up after the outage). Account status ACTIVE again, so the unpaid balance is cleared. |
| Selah Place | Alicia | ❌ $35 vs $50 sheet | ✅ $55 vs $50 sheet | BoF retargeting raised from $15 to $35 (the planned move of the paused test's budget, actions log, now Done), so live is Giveaway $15 + BoF $35 + Lead $5 = $55, 10% over the $50 sheet and within tolerance. Spend $278 in 7 days ($40/day) because the change landed mid-week. Account ACTIVE. About 75 old Instagram boosted posts remain ACTIVE on exhausted lifetime budgets, not spending. |
| Stay With Branch | Kristal | ⚠️ $20 vs $20 sheet | ✅ $20 vs $20 sheet | Delivery recovered: $185 spent in 7 days ($26/day) on $20/day budgets (MoF $5 + Discovery $15), after $59 the week before. |

## All accounts

| Client | AM | Sheet Status | Sheet $/day | Actual $/day | Match | Notes/Issues |
|---|---|---|---|---|---|---|
| American River Resort | Nicole | Live | $50 | $50 | ✅ | 2 campaigns (Giveaway $30, Leads $20). |
| Asheville River Cabins | Charlotte | Live | $80 | $80 | ✅ | Giveaway $40 + BoF $30 + MoF $10 = $80; spend $646 in 7 days ($92/day, catching up after the outage). Account status ACTIVE again, so the unpaid balance is cleared. |
| Away2PA | Alicia | Live | $40 | $40 | ⚠️ | Week 4: live matches the $40 budget (Giveaway $30 + MoF $5 + BoF $5), but the sheet comment still says "Its on $60/day". Next action (Alicia): remove or correct the comment. |
| Awayframes | Alicia | Live | $30 | $30 | ✅ |  |
| Best Texas Travel | Nicole | Live | $30 | $30 | ✅ |  |
| Big Moon Ranch | Charlotte | Live | $50 | n/a | ⚠️ | Week 4: offboarded on 2026-09-28 but the row is still on the Master sheet as Live with a $50 budget. The API system user has no access to account 758851247064974 and it is absent from the export, as expected. Next action (Charlotte): remove the row from the sheet or set Status to Not Live. AM carried from earlier reports; no CRM row. |
| Bison Ridge Retreat | Chiara | Live | $30 | $30 | ✅ | Read live for the first time (API system user, the connector had this account MCP-disabled): Discovery $20 + BoF $5 + MoF $5 = $30. |
| Canopy at Moody Moon Ridge | Kristal | Live | — | $0 | ⚠️ | source: CSV export 2026-10-05 to 2026-10-11, not live (the API system user has no access to account 1293707265980102; it is absent from the export, so $0 spend). Week 4: no documented budget on the sheet (comment: "Removed the budget since its changing regularly"), still no active campaigns. Next action (Kristal): confirm whether the account is meant to be paused; if so set the sheet Status to Paused, otherwise add a budget. Also grant the HiddenGem-Claude system user access to the account. AM carried from last week. |
| Columbia Gorge Getaways | Chiara | Live | $30 | $40 | ❌ | Week 4: Discovery $20 + BoF $15 + MoF $5 = $40, still $10 over the $30 sheet (33%). Next action (Chiara): confirm the agreed budget with the client, then fix the sheet or the campaigns. |
| Endless Stays | Nicole | Live | $200 | $200 | ✅ | Read live for the first time (API system user): Giveaway $75 + BoF $75 + MoF Lead $50 = $200, spend $1,438 in 7 days ($205/day). |
| Evergreen Cabins | Nicole | Live | $40 | $40 | ✅ |  |
| FLOHOM | Makenna | Live | $250 | $220 | ⚠️ | Week 4: 5 active campaigns = $220/day (BoF $90, Lookalike $80, Myrtle Beach Lookalike $20, Lead $20, Giveaway $10), 12% under the $250 sheet. Next action (Makenna): update the sheet to $220 or confirm the target is still $250. |
| Green Springs Inn | Alicia | Live | $40 | $40 | ✅ | One old boosted post (Mother's Day Brunch) still ACTIVE on an exhausted $50 lifetime budget, not spending. |
| Hiawassee Glamping | Alicia | Live | $30 | $30 | ✅ |  |
| Home Base | Charlotte | Live | $50 | $50 | ✅ |  |
| Inspired Retreats | Makenna | Live | $60 | $60 | ✅ | Queried "Inspired Retreats Ads 2.0" under HG BM. |
| Little River Landing | Makenna | Live | — | $65 | ⚠️ | Week 3: sheet budget cell still reads #REF!, so there is no documented budget to compare against. Live: Giveaway $55 + BoF $5 + MoF $5 = $65, unchanged. Next action (Makenna): repair the budget cell on the sheet ($65). |
| Myrinn | Kristal | Live | $30 | $30 | ✅ | Account sits under HG Marketing BM. |
| Nature Nooks | Kristal | Live | $30 | $30 | ✅ | Giveaway $10 + Keyword Engagement $10 + MoF Lead $10. |
| North Star Resort & Lodge | Charlotte | Live | $30 | $30 | ✅ | Giveaway $20 + BoF $5 + MoF Lead (10/02) $5 = $30; the new MoF campaign is now spending. |
| Oak & Ember | Chiara | Live | $30 | $30 | ✅ |  |
| Paradise Pointe | Makenna | Live | $100 | $150 | ❌ | Week 2, read live for the first time (API system user): LoL Sales $50 + BoF $50 + MoF Lead $25 + Giveaway $25 = $150/day, 50% over the $100 sheet; spend $1,066 in 7 days ($152/day). The $50 LoL campaign is Shawal's 28 Sep change (actions log, Done); only the sheet is behind. Next action (Makenna): update the sheet to $150. |
| Parker Reserve | Kristal | Live | $10 | $10 | ✅ | 4-Campaign Structure column says Not Live, Status says Live; one $10 Discovery campaign live. |
| Ponderosa Pines Resort | Anna | Live | $100 | $100 | ✅ | Read live for the first time (API system user): Retarget $40 + Discovery $40 + Leads $20 = $100. |
| Raven Rock Mountain | Kristal | Not Live | — | $0 | ✅ | No campaigns in the account at all, correct for Not Live. |
| Red White & Blue Views | Nicole | Live | $45 | $45 | ✅ |  |
| Ridge & Falls | Makenna | Live | — | $60 | ⚠️ | Week 3: sheet budget cell still reads #REF!, so there is no documented budget to compare against. Live: Giveaway $50 + BoF $5 + MoF $5 = $60, unchanged. The lead-campaign relaunch planned on 28 Sep (actions log) has still not happened; the 09/01 lead campaign is the live one. Next action (Makenna): repair the budget cell on the sheet ($60). |
| Selah Place | Alicia | Live | $50 | $55 | ✅ | BoF retargeting raised from $15 to $35 (the planned move of the paused test's budget, actions log, now Done), so live is Giveaway $15 + BoF $35 + Lead $5 = $55, 10% over the $50 sheet and within tolerance. Spend $278 in 7 days ($40/day) because the change landed mid-week. Account ACTIVE. About 75 old Instagram boosted posts remain ACTIVE on exhausted lifetime budgets, not spending. |
| Starlight Haven - Hot Springs | Charlotte | Live | $75 | $75 | ✅ | Budgets at ad set level (6 active ad sets = $75). |
| Starlight Haven - Weiss Lake | Charlotte | Live | $65 | $70 | ✅ | Budgets at ad set level (5 active ad sets = $70, $5 over sheet, within tolerance): Retargeting $45 + Leads $25. |
| Stay on 30a | Charlotte | Live | $400 | $500 | ⚠️ | Week 4, up again: MoF LoL $200 (was $180) + BoF $150 (was $120) + Giveaway $100 + MoF Leads $50 = $500, now 25% over the $400 sheet (the warning limit; one more increase makes it ❌); spend $3,470 in 7 days ($496/day). Next action (Charlotte): update the sheet to $500 or confirm the agreed ceiling. |
| Stay Saluda NC | Makenna | Live | $80 | $80 | ✅ | Giveaway $30 + BoF $30 + MoF $20 = $80. |
| Stay Southern Illinois | Chiara | Live | $30 | $30 | ✅ |  |
| Stay With Branch | Kristal | Live | $20 | $20 | ✅ | Delivery recovered: $185 spent in 7 days ($26/day) on $20/day budgets (MoF $5 + Discovery $15), after $59 the week before. |
| StayLuxe | Kristal | Live | $20 | $20 | ✅ | ToF Winter $10 (ad set budget) + MoF $5 + BoF $5 = $20. |
| Sunapee Stays | Charlotte | Live | $50 | $50 | ✅ |  |
| Taberg Falls | Alicia | Live | $400 | $300 | ⚠️ | New: budgets cut during the week to BoF $75 (was $100) + Lookalike $75 (was $50) + Giveaway $50 (was $100) + Leads $50 (was $60) + Broad $50 = $300/day, 25% under the $400 sheet (the warning limit); spend $2,288 in 7 days ($327/day) reflects the higher budgets early in the week. Next action (Alicia): confirm the new $300 level with the client and update the sheet, or restore the budgets. |
| The Cohost Company | Makenna | Live | $130 | $130 | ✅ |  |
| The Outpost | Anna | Live | $40 | $50 | ⚠️ | New: a second BoF campaign "BoF - Sales Campaign - Retargeting Website Visitors - 10/.." ($10) is ACTIVE beside the original 08/29 BoF ($10), both spending, plus the two Giveaways at $15 = $50/day, 25% over the $40 sheet; the export marks the 08/29 one as not delivering. A boosted post ($12.58/day, ended 22 May) is still ACTIVE but not spending and is excluded. Next action (Anna): pause the old 08/29 BoF if the 10/.. one replaces it, then the account is back at $40. |
| Three Suns Cabins | Kristal | Live | $15 | $15 | ⚠️ | Week 4: matches at $15, but the sheet note "Running at $15 until Sept" has expired. Next action (Kristal): confirm the October budget with the client and update the note. |
| Treetop Escapes | Makenna | Live | $100 | $100 | ✅ |  |
| Tuxedo Falls | Chiara | Live | $30 | $30 | ✅ |  |
| Walden Retreats | Anna | Live | $30 | $48 | ❌ | New on the Master sheet this week (Live, $30). Live: Giveaway $10 + MoF Lead (10/06) $10 + BoF $10 + "TOF Wedding Leads 10.8.26" $15 + "TOF Wedding Leads (alt aud) 10.9.26" $3 = $48/day, 60% over the $30 sheet; spend $296 in 7 days ($42/day). The two wedding-lead campaigns launched 8 and 9 Oct on top of the three-campaign structure. Next action (Anna): confirm the wedding test with the client and put the agreed total on the sheet, or pause the test. Matched by account ID 973261794434226 (the export names the account by its ID). |

## Footer

- Clients on sheet: 43 (42 Live, 1 Not Live/Paused). Walden Retreats joined the sheet this week.
- Live reads: 41 through the Marketing API (the system user sees 50 ad accounts, including the four the connector had MCP-disabled: Bison Ridge, Endless Stays, Paradise Pointe, Ponderosa, now read live). Scored from CSV export: 1 (Canopy, no system-user access). Blocked: 0. Offboarded but still on the sheet: 1 (Big Moon Ranch).
- Confirmed daily budget across live-read accounts: $3,063 vs $2,870 documented
- Including CSV-scored accounts: $3,063 vs $2,870 documented
- Flags: 3 ❌, 0 🔴, 10 ⚠️, 30 ✅. Diff vs 2026-10-05: 3 new, 10 still open, 3 fixed, 27 unchanged
- Previous report: 2026-10-05-ad-spend-check.csv
- Actions log entries checked (PROJECT.md section 9): Selah Place BoF budget move now Done ($35); Ridge & Falls relaunch still Planned; Paradise Pointe LoL campaign Done, sheet still $100; Asheville balance cleared (account ACTIVE, delivering). Shawal has not yet reported this week's changes, so Tàberg's cuts, Stay on 30a's increases, The Outpost's second BoF and Walden's wedding tests are observed, not confirmed.
- Budgets from the Marketing API arrive in cents and were divided by 100 (the connector returned dollars last week); ad set level budgets summed for Starlight Haven (both) and StayLuxe's ToF Winter campaign.
- Sheet changes since last week: Walden Retreats row added ($30). Paradise Pointe still $100, Ridge & Falls and Little River Landing still #REF!, Big Moon Ranch still listed.

## Not on the sheet

Active ad accounts with spend in the export and no Master sheet row: Edenwood NC ($10/day Giveaway) and HiddenGem Marketing, which runs three Outpost campaigns at $30/day (FB Discovery, Insta Discovery, Outpost Leads) in HG's own account alongside The Outpost's $50. Not checked. Decision pending on adding them.
