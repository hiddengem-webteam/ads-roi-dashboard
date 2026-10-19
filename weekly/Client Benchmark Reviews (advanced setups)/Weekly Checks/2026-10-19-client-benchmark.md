# Client Benchmark Review (advanced setups) — 2026-10-19

Run: 19 October 2026 (Monday), fifth run, compared against 2026-10-13-client-benchmark.csv. Live reads through the Meta Marketing API with the HiddenGem-Claude system user, now the standing data path (`scripts/pull-campaign-insights.mts`, 09:37 to 09:38 PT); every account is live and the CSV export 2026-10-05 to 2026-10-11 was not needed for scoring. Scope: clients marked **Advanced** in the CRM "Meta Ads" column (Clients - Onboarding tab), re-read today: 26 clients, 21 with an ad account. Sunapee Stays leaves scope (CRM now says Basic). Five Advanced clients in the CRM have no ad account yet. Only Lead Gen (MoF) and Sales/Retargeting (BoF) campaigns are scored; IG Discovery and Keyword (ToF) spend is shown for context only.

| Advanced clients | Live reads | From CSV | Campaigns scored | Under spend gate | Flag to Shawal | Review w/ HG AI | Monitor | Healthy | Scale w/ HG AI | Frequency over 5 |
|---|---|---|---|---|---|---|---|---|---|---|
| 21 (+5 unmapped) | 21 | 0 | 37 | 10 | 2 | 12 | 11 | 8 | 4 | 1 |

States come from the Decision Making table in the Benchmarks doc. Lead Gen: CPL under $0.30 Scale, $0.30–0.50 Healthy, $0.50–1.00 Monitor, $1.00–2.50 Review, $2.50+ Flag, 30-day window, $100 gate. Sales/Retargeting: ROAS above 15x Scale, 8–15x Healthy, 5–8x Monitor, 2–5x Review, under 2x Flag, 14-day window, $200 gate. Band edges are inclusive on the lower bound.

## Weekly Meta Ads meetings since last run (Notes by Gemini)

Source: "Notes by Gemini" docs attached to the calendar events, read via Drive. Summary, decisions and next steps as Gemini wrote them; client-specific sentences are pulled into each client's section below. Transcript not used.

### Meta Ads Strategy — 2026-10-14 — doc `14s5-eW49GhSjyoeunooM1-kBX7O_Rr4X8pE_rS9WmhE`

Website development discussions and advertising strategies for property management platforms.

Backend Code Perspectives

Discussion on robust backend development versus surface level artificial intelligence tools.

Meta Ad Campaign Structure

Overview of three campaign funnel strategy and tracking challenges for clients.

Cloud Beds Tracking Improvements

Custom scripts improved tracking and matched reservation identifiers for clients.

Decisions:
- Creation of Cloud Beds website templates The creation of a website template for Cloud Beds clients was discussed, with final approval deferred pending client pitching evaluations.
- Transition to four-campaign meta ad structure The team agreed to transition from a three-campaign to a four-campaign strategy for clients with elevated tracking capabilities.
- Prioritization of Cloud Beds tracking integration The team aligned on prioritizing Cloud Beds as the primary PMS platform for implementing the improved EMQ tracking approach.

Next steps:
- [Leshan Patterson] Setup Tracking: Complete the setup of the tracking approach for the remaining 2 clients.
- [Shawal Nazir] Request API Access: Request API access from the host for Asheville River Cabins.
- [Leshan Patterson] Request Script Approval: Consult Brandon to obtain authorization for adding scripts to the landing page.
- [Leshan Patterson] Develop Website Template: Create a website template compatible with the Cloud Beds API.
- [Dustin Baker, Shawal Nazir] Sync Meeting: Sync at 9:30 AM to discuss scaling clients and Best Texas Travel numbers before the 10:00 AM call.
- [Dustin Baker, Leshan Patterson] Discuss Next Initiative: Discuss the next strategic initiative and potential website pitching.

## Action needed

Sales and Retargeting campaigns first, then Lead Gen. Within each, Flag to Shawal before Review w/ HG AI, highest spend first.

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| FLOHOM | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $1,123 / 14d | ROAS 4.0x | Review w/ HG AI | New flag, was Monitor |
| Endless Stays | Nicole | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $1,030 / 14d | ROAS 3.1x | Review w/ HG AI | Still open, week 3 |
| Tàberg Falls | Alicia | MoF - Broad (Acquire new customers) - 09/28/2026 | Sales (MoF lookalike) | $698 / 14d | ROAS 3.9x | Review w/ HG AI | New flag, was Monitor |
| Paradise Pointe | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $693 / 14d | ROAS 3.7x | Review w/ HG AI | Still open, week 3 |
| Treetop Escapes | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $571 / 14d | ROAS 2.5x | Review w/ HG AI | New flag, was Healthy |
| Stay Saluda NC | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $416 / 14d | ROAS 4.3x | Review w/ HG AI | New flag, was Monitor |
| Walden Retreats | Anna | TOF Wedding Leads 10.8.26 | Lead Gen (MoF) | $201 / 30d | CPL $10.07 | Flag to Shawal | New flag, was Under gate |
| Ridge & Falls | Makenna | MoF - Lead Campaign - Retargeting Engagers - 09/01/26 | Lead Gen (MoF) | $147 / 30d | CPL $3.51 | Flag to Shawal | Still open, week 4 |
| Stay On 30A | Charlotte | MoF - Lead Campaign - RT Engagers - 07/16/26 | Lead Gen (MoF) | $1,501 / 30d | CPL $1.37 | Review w/ HG AI | Still open, week 5 |
| Green Springs Inn | Alicia | MoF - Lead Campaign/08/28/2026 | Lead Gen (MoF) | $300 / 30d | CPL $1.35 | Review w/ HG AI | Still open, week 5 |
| Little River Landing | Makenna | MoF - Lead Campaign - Retargeting Engagers - 09/16/2026 | Lead Gen (MoF) | $152 / 30d | CPL $1.37 | Review w/ HG AI | Still open, week 3 |
| Bison Ridge Retreat | Chiara | MoF - Lead Campaign - RT Engagers | Lead Gen (MoF) | $149 / 30d | CPL $2.26 | Review w/ HG AI | Still open, week 2 |
| AwayFrames | Alicia | MoF - Lead Campaign - Retargeting Engagers 07/31/2026 | Lead Gen (MoF) | $149 / 30d | CPL $1.43 | Review w/ HG AI | Still open, week 5 |
| Walden Retreats | Anna | MoF - Lead Campaign - Retargeting Engagers - 10/06/2026 | Lead Gen (MoF) | $127 / 30d | CPL $1.30 | Review w/ HG AI | New flag, was Under gate |

Removed since last week (flagged on 13 Oct, not scored today): American River Resort: MoF - Lead Campaign - Retargeting Engagers (Review w/ HG AI); Sunapee Stays: MoF - Lead Campaign - Retargeting Engagers (Review w/ HG AI).

## Scale candidates

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| Stay On 30A | Charlotte | BoF - Sales Campaign - RT Website Visitors - 07/13/26 | Retargeting (BoF) | $2,048 / 14d | ROAS 22.0x | Scale w/ HG AI | Unchanged |
| Starlight Haven Weiss Lake | Charlotte | Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | $631 / 14d | ROAS 25.3x | Scale w/ HG AI | Unchanged |
| Asheville River Cabins | Charlotte | BoF - Website Retargeting Campaign - 06/08/26 | Retargeting (BoF) | $455 / 14d | ROAS 43.1x | Scale w/ HG AI | Unchanged |
| Starlight Haven Hot Springs | Charlotte | Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | $279 / 14d | ROAS 22.3x | Scale w/ HG AI | Unchanged |

## Frequency watch (Sales / Retargeting above 5)

Sales, Retargeting and MoF-lookalike campaigns whose 14-day frequency is above 5.0 (Shawal, 6 Oct 2026). Frequency does not change the ROAS state; this is the list to refresh creative or widen the audience on. The diagnostics column still notes anything above 3.0.

| Client | AM | Campaign | Type | Frequency | Spend / window | Governing metric | State |
|---|---|---|---|---|---|---|---|
| Paradise Pointe | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 5.66 | $693 / 14d | ROAS 3.7x | Review w/ HG AI |

## Per client, ordered by scored MoF + BoF spend

### Stay On 30A — AM Charlotte — account Stay on 30a Ads (25640434272252212) — live read

ToF (Discovery / Keyword) spend, not scored: $3,001 over 30 days.

This month (booked 1 Oct–19 Oct): direct revenue $174,861 from 66 bookings, −38% vs 1 Sep–19 Sep ($280,111 from 89 bookings) · promo codes: 30 uses (VIP100 ×11, EARLY BIRD DIRECT ×9, WELCOME100 ×4, WELCOMEBACK15 ×3, CINDYSWANSON10 ×2, 10%COAST ×1, ESCAPE30A ×1, RETURNINGGUEST ×1, TUCKS20 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - RT Engagers - 07/16/26 | Lead Gen (MoF) | 30d | $1,501 | 1096 leads | CPL $1.37 | — | Review w/ HG AI | CPC $0.40 > $0.30; CPM $35.76 > $14.84 | 14d CPL $1.41 | Still open, week 5 |
| MoF - Sales Campaign - HiddenGem Pixel LoL - 07/17/26 | Sales (MoF lookalike) | 14d | $2,775 | 9 purchases | ROAS 8.8x | 2.05 | Healthy | CPC $0.98 > $0.62; CPM $24.26 > $16.50; cost/booking $308.29 > $90 | 30d ROAS 14.7x, 29 purchases | Unchanged |
| BoF - Sales Campaign - RT Website Visitors - 07/13/26 | Retargeting (BoF) | 14d | $2,048 | 13 purchases | ROAS 22.0x | 4.41 | Scale w/ HG AI | CPC $1.71 > $0.62; CPM $27.25 > $16.50; cost/booking $157.51 > $90; freq 4.4 > 3.0 | 30d ROAS 26.4x, 30 purchases | Unchanged |

Monthly ROI: July: spend $6,407, 67 Meta-attributed bookings, blended ROAS 32.3x, retargeting ROAS 14.6x, CPL $1.24 on 583 leads · August: spend $12,420, 85 Meta-attributed bookings, blended ROAS 17.8x, retargeting ROAS 15.5x, CPL $2.58 on 594 leads · September: spend $12,606, 91 Meta-attributed bookings, blended ROAS 24.4x, retargeting ROAS 23.1x, CPL $1.52 on 1001 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Tàberg Falls — AM Alicia — account Táberg Falls (827872700004659) — live read

ToF (Discovery / Keyword) spend, not scored: $2,515 over 30 days.

This month (booked 1 Oct–19 Oct): direct revenue $40,472 from 28 bookings, −10% vs 1 Sep–19 Sep ($44,762 from 28 bookings) · promo codes: 2 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Broad (Acquire new customers) - 09/28/2026 | Sales (MoF lookalike) | 14d | $698 | 2 purchases | ROAS 3.9x | 1.60 | Review w/ HG AI | CPM $23.75 > $16.50; cost/booking $348.98 > $90 | 30d ROAS 4.3x, 3 purchases | New flag, was Monitor |
| MoF - Leads Campaign - 06/19/26 | Lead Gen (MoF) | 30d | $1,707 | 3008 leads | CPL $0.57 | — | Monitor | within lines | 14d CPL $0.56 | Unchanged |
| BoF - Website Retargeting Campaign - 08/21/2026 | Retargeting (BoF) | 14d | $1,031 | 7 purchases | ROAS 12.9x | 2.89 | Healthy | CPC $0.70 > $0.62; CPM $24.29 > $16.50; cost/booking $147.31 > $90 | 30d ROAS 8.8x, 14 purchases | Unchanged |
| MoF - Lookalike Sales Campaign - 08/21/2026 | Sales (MoF lookalike) | 14d | $826 | 5 purchases | ROAS 9.8x | 1.45 | Healthy | CPM $21.19 > $16.50; cost/booking $165.11 > $90 | 30d ROAS 9.3x, 12 purchases | Unchanged |

Monthly ROI: July: spend $11,739, 80 Meta-attributed bookings, blended ROAS 9.5x, retargeting ROAS 15.8x, CPL $0.67 on 2320 leads · August: spend $11,259, 31 Meta-attributed bookings, blended ROAS 4.5x, retargeting ROAS 8.0x, CPL $0.46 on 4015 leads · September: spend $10,800, 27 Meta-attributed bookings, blended ROAS 4.0x, retargeting ROAS 7.1x, CPL $0.55 on 3261 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. Budgets were cut on 13 Oct (today $250/day: Giveaway $50, Leads $50, Lookalike $50, Broad $50, BoF $50), so this 14-day window is mostly on the cut budgets. The Broad prospecting campaign (3.9x on 2 purchases, $698) moves to Review; it is scored on the Retargeting bands (see footer).

### FLOHOM — AM Makenna — account FLOHOM Ads (2100710320122219) — live read

ToF (Discovery / Keyword) spend, not scored: $362 over 30 days.

This month (booked 1 Oct–19 Oct): direct revenue $70,350 from 78 bookings, −25% vs 1 Sep–19 Sep ($94,407 from 101 bookings) · promo codes: 14 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $1,123 | 6 purchases | ROAS 4.0x | 2.43 | Review w/ HG AI | CPC $0.73 > $0.62; CPM $20.44 > $16.50; cost/booking $187.16 > $90 | 30d ROAS 7.1x, 22 purchases | New flag, was Monitor |
| MoF - Lead Campaign - Retargeting Engagers – 08/17/26 | Lead Gen (MoF) | 30d | $662 | 1179 leads | CPL $0.56 | — | Monitor | within lines | 14d CPL $0.59 | Unchanged |
| [Myrtle Beach] MoF - Lookalike Sales Campaign - 09/17/26 | Sales (MoF lookalike) | 14d | $282 | 1 purchases | ROAS 6.0x | 2.41 | Monitor | CPC $0.93 > $0.62; CPM $20.14 > $16.50; cost/booking $282.19 > $90 | 30d ROAS 9.7x, 5 purchases | Was Healthy |
| MoF - Lookalike Sales Campaign - 07/29/26 | Sales (MoF lookalike) | 14d | $1,012 | 10 purchases | ROAS 9.7x | 2.34 | Healthy | CPC $0.84 > $0.62; CPM $22.94 > $16.50; cost/booking $101.19 > $90 | 30d ROAS 9.3x, 23 purchases | Unchanged |

Monthly ROI: July: spend $5,555, 103 Meta-attributed bookings, blended ROAS 17.2x, retargeting ROAS 19.1x, CPL $7.66 on 66 leads · August: spend $9,331, 57 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 8.2x, CPL $2.24 on 708 leads · September: spend $8,855, 66 Meta-attributed bookings, blended ROAS 6.7x, retargeting ROAS 8.9x, CPL $0.50 on 2192 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. BoF 4.0x on 14 days (6 purchases) against 7.1x on 30 days: the last two weeks are the soft patch, and October direct revenue is 25% below September's same span. The [Myrtle Beach] lookalike slips to Monitor at 6.0x on 1 purchase.

### Endless Stays — AM Nicole — account Endless Stays (896372356081479) — live read

ToF (Discovery / Keyword) spend, not scored: $2,166 over 30 days.

This month (booked 1 Oct–19 Oct): direct revenue $26,056 from 16 bookings, +381% vs 1 Sep–19 Sep ($5,421 from 18 bookings) · promo codes: not tracked by hospitable.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $1,030 | 2 purchases | ROAS 3.1x | 2.64 | Review w/ HG AI | CPM $18.71 > $16.50; cost/booking $514.93 > $90 | 30d ROAS 2.5x, 3 purchases | Still open, week 3 |
| MoF Lead Campaign - Retargeting Engagers - 09/09/2026 | Lead Gen (MoF) | 30d | $1,311 | 1544 leads | CPL $0.85 | — | Monitor | within lines | 14d CPL $0.80 | Unchanged |

Monthly ROI: July: spend $1,534, 9 Meta-attributed bookings, blended ROAS 16.0x · August: spend $1,553, 10 Meta-attributed bookings, blended ROAS 11.6x, retargeting ROAS 38.8x, CPL $9.73 on 26 leads · September: spend $2,539, 6 Meta-attributed bookings, blended ROAS 2.9x, retargeting ROAS 4.7x, CPL $1.05 on 532 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. BoF 3.1x, third week at Review. October direct revenue is $26k against $5.4k in September's same span (+381%), so direct bookings are landing outside the pixel's view; check the purchase event on the Hospitable booking flow.

### Paradise Pointe — AM Makenna — account Paradise Pointe Ads (1585826092078255) — live read

ToF (Discovery / Keyword) spend, not scored: $749 over 30 days.

This month (booked 1 Oct–19 Oct): direct revenue $82,137 from 86 bookings, −11% vs 1 Sep–19 Sep ($92,477 from 80 bookings) · promo codes: 2 uses (WELCOME10 ×1, WELCOME100 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $693 | 13 purchases | ROAS 3.7x | 5.66 ⚠️ > 5 | Review w/ HG AI | CPC $0.98 > $0.62; freq 5.7 > 3.0 | 30d ROAS 3.6x, 27 purchases | Still open, week 3 |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $753 | 791 leads | CPL $0.95 | — | Monitor | within lines | 14d CPL $1.00 | Unchanged |
| MoF - LoL Sales Campaign - 09/28/26 | Sales (MoF lookalike) | 14d | $699 | 21 purchases | ROAS 9.4x | 2.61 | Healthy | CPC $0.74 > $0.62 | 30d ROAS 7.8x, 27 purchases | Unchanged |

Monthly ROI: July: spend $2,237, 74 Meta-attributed bookings, blended ROAS 21.6x, retargeting ROAS 16.7x, CPL $1.01 on 90 leads · August: spend $3,109, 94 Meta-attributed bookings, blended ROAS 16.8x, retargeting ROAS 18.0x, CPL $1.64 on 471 leads · September: spend $3,074, 48 Meta-attributed bookings, blended ROAS 7.0x, retargeting ROAS 13.0x, CPL $0.97 on 764 leads. Note in the September file: Meta did not record revenue for 12 retargeting purchases (week of Sep 15–21 and Sep 29–30); their value was added manually at the average booking value (12 × $1,170.59 = $14,047.08) and the ROAS updated.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. BoF 3.7x, third week at Review, frequency 5.7 and still the only Frequency-watch row. September ROI file: Meta recorded no revenue for 12 retargeting purchases; the purchase-value check (decision 26) is still open, so the live ROAS may understate.

### Treetop Escapes — AM Makenna — account Treetop Escapes Ads (967636478877602) — live read

ToF (Discovery / Keyword) spend, not scored: $902 over 30 days.

This month (booked 1 Oct–19 Oct): direct revenue $30,708 from 37 bookings, +25% vs 1 Sep–19 Sep ($24,469 from 27 bookings) · promo codes: 1 uses (WELCOME10 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $571 | 3 purchases | ROAS 2.5x | 3.31 | Review w/ HG AI | CPM $18.84 > $16.50; cost/booking $190.47 > $90; freq 3.3 > 3.0 | 30d ROAS 7.1x, 10 purchases | New flag, was Healthy |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $904 | 1149 leads | CPL $0.79 | — | Monitor | CPM $18.16 > $14.84 | 14d CPL $0.82 | Unchanged |

Monthly ROI: July: spend $2,487, 44 Meta-attributed bookings, blended ROAS 14.5x, retargeting ROAS 22.2x, CPL $1.48 on 21 leads · August: spend $3,082, 28 Meta-attributed bookings, blended ROAS 8.8x, retargeting ROAS 16.3x, CPL $1.49 on 620 leads · September: spend $2,998, 10 Meta-attributed bookings, blended ROAS 3.8x, retargeting ROAS 7.9x, CPL $0.88 on 1019 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. BoF 2.5x on 3 purchases in 14 days (7.1x on 30), first Review since the 28 Sep run (4.7x then). October direct revenue is up 25% on September's span, so bookings are arriving that the pixel does not credit to the campaign.

### Starlight Haven Weiss Lake — AM Charlotte — account Starlight Haven Weiss Lake (74756899) — live read

ToF (Discovery / Keyword) spend, not scored: $0 over 30 days.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $753 | 772 leads | CPL $0.98 | — | Monitor | CPC $0.33 > $0.30 | 14d CPL $1.15 | Unchanged |
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $631 | 22 purchases | ROAS 25.3x | 2.63 | Scale w/ HG AI | CPC $0.81 > $0.62 | 30d ROAS 25.2x, 54 purchases | Unchanged |

Monthly ROI: July: spend $2,163, 41 Meta-attributed bookings, blended ROAS 10.8x, retargeting ROAS 15.2x, CPL $0.74 on 826 leads · August: spend $2,351, 36 Meta-attributed bookings, blended ROAS 10.7x, retargeting ROAS 17.6x, CPL $1.23 on 617 leads · September: spend $2,152, 79 Meta-attributed bookings, blended ROAS 17.4x, retargeting ROAS 23.8x, CPL $1.01 on 734 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Starlight Haven Hot Springs — AM Charlotte — account Starlight Haven Hot Springs (901138032027913) — live read

ToF (Discovery / Keyword) spend, not scored: $752 over 30 days.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $904 | 2761 leads | CPL $0.33 | — | Healthy | within lines | 14d CPL $0.32 | Unchanged |
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $279 | 10 purchases | ROAS 22.3x | 1.95 | Scale w/ HG AI | within lines | 30d ROAS 29.0x, 22 purchases | Unchanged |

Monthly ROI: July: spend $2,160, 17 Meta-attributed bookings, blended ROAS 5.1x, retargeting ROAS 17.1x, CPL $0.33 on 2813 leads · August: spend $2,193, 19 Meta-attributed bookings, blended ROAS 6.3x, retargeting ROAS 22.3x, CPL $0.36 on 2589 leads · September: spend $2,155, 61 Meta-attributed bookings, blended ROAS 16.5x, retargeting ROAS 28.5x, CPL $0.34 on 2597 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Ponderosa Pines Resort — AM Anna — account Ponderosa Pines Resort (1058846326445255) — live read

ToF (Discovery / Keyword) spend, not scored: $1,204 over 30 days.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Leads Campaign - 07/16/26 | Lead Gen (MoF) | 30d | $600 | 706 leads | CPL $0.85 | — | Monitor | within lines | 14d CPL $1.02 | Unchanged |
| Website Retarget Campaign - 07/13/26 | Retargeting (BoF) | 14d | $551 | 10 purchases | ROAS 7.6x | 3.07 | Monitor | CPC $0.70 > $0.62; CPM $19.87 > $16.50; freq 3.1 > 3.0 | 30d ROAS 15.2x, 36 purchases | Was Scale w/ HG AI |

Monthly ROI: July: spend $2,089, 17 Meta-attributed bookings, blended ROAS 3.6x, retargeting ROAS 22.3x, CPL $0.91 on 356 leads · August: spend $3,101, 103 Meta-attributed bookings, blended ROAS 15.0x, retargeting ROAS 21.3x, CPL $1.32 on 471 leads · September: spend $2,985, 119 Meta-attributed bookings, blended ROAS 17.9x, retargeting ROAS 21.6x, CPL $0.84 on 708 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. BoF 7.6x on 14 days (15.2x on 30): a 14-day dip takes it from Scale to Monitor; frequency 3.1.

### Stay Saluda NC — AM Makenna — account Stay Saluda Ads (1863632561215857) — live read

ToF (Discovery / Keyword) spend, not scored: $898 over 30 days.

This month (booked 1 Oct–19 Oct): direct revenue $9,834 from 17 bookings, +3% vs 1 Sep–19 Sep ($9,507 from 17 bookings) · promo codes: 5 uses (WELCOME10 ×4, VIP10 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $416 | 3 purchases | ROAS 4.3x | 4.67 | Review w/ HG AI | CPC $0.73 > $0.62; CPM $17.30 > $16.50; cost/booking $138.64 > $90; freq 4.7 > 3.0 | 30d ROAS 3.8x, 6 purchases | New flag, was Monitor |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $596 | 630 leads | CPL $0.95 | — | Monitor | within lines | 14d CPL $0.96 | Unchanged |

Monthly ROI: July: spend $2,140, 10 Meta-attributed bookings, blended ROAS 2.6x, retargeting ROAS 0.8x · August: spend $2,367, 9 Meta-attributed bookings, blended ROAS 3.7x, retargeting ROAS 5.2x, CPL $2.59 on 146 leads · September: spend $2,394, 6 Meta-attributed bookings, blended ROAS 1.3x, retargeting ROAS 3.5x, CPL $1.00 on 596 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. BoF 4.3x on 3 purchases with frequency 4.7 and climbing. The Saluda GHL hosts still fire the Inspired Retreats pixel (pixel check, week 5).

### Asheville River Cabins — AM Charlotte — account Asheville River Cabins Ads (615836588009747) — live read

ToF (Discovery / Keyword) spend, not scored: $1,021 over 30 days.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $255 | 837 leads | CPL $0.30 | — | Healthy | within lines | 14d CPL $0.31 | Was Scale w/ HG AI |
| BoF - Website Retargeting Campaign - 06/08/26 | Retargeting (BoF) | 14d | $455 | 18 purchases | ROAS 43.1x | 2.09 | Scale w/ HG AI | CPM $20.21 > $16.50 | 30d ROAS 41.4x, 34 purchases | Unchanged |

Monthly ROI: July: spend $2,029, 39 Meta-attributed bookings, blended ROAS 18.6x, retargeting ROAS 51.6x · August: spend $2,424, 82 Meta-attributed bookings, blended ROAS 27.2x, retargeting ROAS 65.0x, CPL $0.42 on 605 leads · September: spend $2,252, 70 Meta-attributed bookings, blended ROAS 19.1x, retargeting ROAS 42.5x, CPL $0.30 on 936 leads.

Meeting notes (Meta Ads Strategy 2026-10-14): Event Match Quality Limitations and Proposed Four-Campaign Strategy: Dustin Baker addressed tracking challenges with bottom-funnel purchase campaigns, noting that Event Match Quality is low at approximately five out of ten for clients without custom-coded websites, such as Asheville River Cabins or Green Springs Inn. Cloud Beds Tracking Improvements and Click ID Implementation: Leshan Patterson reported progress on improving Event Match Quality for non-artificial intelligence website clients using Cloud Beds, noting that custom scripts added to the Asheville River Cabins account successfully recorded Facebook click identifiers from reservations. Dustin Baker heavily criticized the poor booking flow and user experience of existing Cloud Beds websites—citing Salmon Rapids Lodge and Asheville River Cabins—where users searching specific accommodations are redirected back to square one.

HG AI notes: none dropped in since the previous run. 14 Oct Strategy: Leshan's custom script in the Cloudbeds account recorded Facebook click IDs on reservations; sending them to Meta through CAPI needs host API access, which Shawal is requesting. The leads campaign slips from Scale to Healthy at $0.30 (band edge); BoF 43.1x holds.

### Selah Place — AM Alicia — account Selah.place (1275283434220508) — live read

ToF (Discovery / Keyword) spend, not scored: $599 over 30 days.

This month (booked 1 Oct–19 Oct): direct revenue $16,622 from 31 bookings, −2% vs 1 Sep–19 Sep ($17,036 from 34 bookings) · promo codes: 12 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $179 | 307 leads | CPL $0.58 | — | Monitor | within lines | 14d CPL $0.53 | Unchanged |
| BoF-Website Retarget Campaign - 07/24/2026 | Retargeting (BoF) | 14d | $344 | 8 purchases | ROAS 11.7x | 4.10 | Healthy | CPM $17.83 > $16.50; freq 4.1 > 3.0 | 30d ROAS 14.5x, 16 purchases | Was Scale w/ HG AI |

Paused in window, not scored: SP / Prospecting Test / LAL + Interests x Creative / 09-2026 (Sales), $422 / 14d, 1 purchases, ROAS 1.1x. Live campaigns only are scored (decision 2026-09-23).

Monthly ROI: July: spend $1,054, 4 Meta-attributed bookings, blended ROAS 3.2x, retargeting ROAS 86.3x, CPL $0.80 on 49 leads · August: spend $1,545, 15 Meta-attributed bookings, blended ROAS 4.8x, retargeting ROAS 25.1x, CPL $1.08 on 144 leads · September: spend $1,304, 27 Meta-attributed bookings, blended ROAS 10.4x, retargeting ROAS 38.2x, CPL $0.63 on 232 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. Actions log: the BoF retargeting budget was raised on 13 Oct (planned move of the paused test's budget, Done; the spend check reads $30/day today), so this 14-day window is the first mostly on the higher budget. BoF 11.7x on 8 purchases sits below the 15x Scale line; the paused prospecting test's trailing spend (1.1x) is listed, not scored.

### Walden Retreats — AM Anna — account Walden Retreats (973261794434226) — live read

ToF (Discovery / Keyword) spend, not scored: $137 over 30 days.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| TOF Wedding Leads 10.8.26 | Lead Gen (MoF) | 30d | $201 | 20 leads | CPL $10.07 | — | Flag to Shawal | CPM $24.27 > $14.84 | 14d CPL $10.07 | New flag, was Under gate |
| MoF - Lead Campaign - Retargeting Engagers - 10/06/2026 | Lead Gen (MoF) | 30d | $127 | 98 leads | CPL $1.30 | — | Review w/ HG AI | CPC $0.40 > $0.30; CPM $18.25 > $14.84 | 14d CPL $1.30 | New flag, was Under gate |
| BoF - Sales Campaign - Retargeting Website Visitors - 06/10/2026 | Retargeting (BoF) | 14d | $118 | 9 purchases | ROAS 56.9x | 1.79 | Under gate | CPC $0.63 > $0.62; CPM $19.51 > $16.50 | spend $118.31 < $200 gate; 30d ROAS 56.9x, 9 purchases | Unchanged |

Paused in window, not scored: TOF Wedding Leads (alt aud) 10.9.26 (Lead Gen (MoF)), $31 / 30d, 0 leads, CPL —. Live campaigns only are scored (decision 2026-09-23).

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. The wedding-lead test (TOF Wedding Leads 10.8.26, $24/day) crosses the $100 gate for the first time at $10.07 CPL on 20 leads. Wedding enquiries are a different lead type from the email-list leads the CPL bands were set for, so read the Flag as a prompt to agree a wedding CPL target with Anna, not as a failure. The alt-audience variant (10.9.26) is paused. BoF 56.9x on $118, under the gate.

### Green Springs Inn — AM Alicia — account Green Springs Inn (1390516335151357) — live read

ToF (Discovery / Keyword) spend, not scored: $602 over 30 days.

This month (booked 1 Oct–19 Oct): direct revenue $23,196 from 52 bookings, +1% vs 1 Sep–19 Sep ($22,918 from 68 bookings) · promo codes: 19 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign/08/28/2026 | Lead Gen (MoF) | 30d | $300 | 222 leads | CPL $1.35 | — | Review w/ HG AI | within lines | 14d CPL $1.18 | Still open, week 5 |
| BoF - Sales Campaign - Retargeting Website Visitors - 08/28/26 | Retargeting (BoF) | 14d | $137 | 3 purchases | ROAS 10.4x | 3.14 | Under gate | CPC $0.68 > $0.62; freq 3.1 > 3.0 | spend $137.19 < $200 gate; 30d ROAS 9.8x, 8 purchases | Unchanged |

Monthly ROI: July: spend $1,222, 17 Meta-attributed bookings, blended ROAS 7.8x, retargeting ROAS 14.6x, CPL $5.65 on 8 leads · August: spend $1,247, 23 Meta-attributed bookings, blended ROAS 8.2x, retargeting ROAS 17.1x, CPL $9.09 on 34 leads · September: spend $1,199, 24 Meta-attributed bookings, blended ROAS 8.5x, retargeting ROAS 9.0x, CPL $1.84 on 166 leads.

Meeting notes (Meta Ads Strategy 2026-10-14): Event Match Quality Limitations and Proposed Four-Campaign Strategy: Dustin Baker addressed tracking challenges with bottom-funnel purchase campaigns, noting that Event Match Quality is low at approximately five out of ten for clients without custom-coded websites, such as Asheville River Cabins or Green Springs Inn.

HG AI notes: none dropped in since the previous run.

### Little River Landing — AM Makenna — account Little River Landing (884285717873613) — live read

ToF (Discovery / Keyword) spend, not scored: $1,652 over 30 days.

This month (booked 1 Oct–19 Oct): direct revenue $2,688 from 12 bookings, +0% vs 1 Sep–19 Sep ($2,694 from 16 bookings) · promo codes: 0 uses.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers - 09/16/2026 | Lead Gen (MoF) | 30d | $152 | 111 leads | CPL $1.37 | — | Review w/ HG AI | CPC $0.37 > $0.30; CPM $18.55 > $14.84 | 14d CPL $1.33 | Still open, week 3 |
| BoF - Sales Campaign - Retargeting Website Visitors - 09/16/2026 | Retargeting (BoF) | 14d | $83 | 0 purchases | ROAS — | 2.90 | Under gate | within lines | spend $82.90 < $200 gate | Unchanged |

Monthly ROI: September: spend $921, 0 Meta-attributed bookings, blended ROAS —, retargeting ROAS —, CPL $1.86 on 46 leads. Note in the September file: Newly launched campaigns — $921.36 spent, no revenue from ads yet.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Ridge & Falls — AM Makenna — account Ridge & Falls ad account (1313401330776046) — live read

ToF (Discovery / Keyword) spend, not scored: $1,506 over 30 days.

This month (booked 1 Oct–19 Oct): direct revenue $2,782 from 7 bookings, +219% vs 1 Sep–19 Sep ($871 from 2 bookings) · promo codes: 0 uses.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers - 09/01/26 | Lead Gen (MoF) | 30d | $147 | 42 leads | CPL $3.51 | — | Flag to Shawal | CPC $0.32 > $0.30; CPM $15.12 > $14.84 | 14d CPL $2.76 | Still open, week 4 |
| BoF - Sales Campaign - Retargeting Website Visitors - 09/01/26 | Retargeting (BoF) | 14d | $84 | 1 purchases | ROAS 4.8x | 3.84 | Under gate | freq 3.8 > 3.0 | spend $84.15 < $200 gate; 30d ROAS 9.1x, 4 purchases | Unchanged |

Monthly ROI: September: spend $1,036, 0 Meta-attributed bookings, blended ROAS —, retargeting ROAS —, CPL $8.16 on 16 leads. Note in the September file: Newly launched campaigns — $1,036.47 spent, no revenue from ads yet (spend exceeds the $871.49 September direct revenue, as expected for a launch month).

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. Actions log: the lead-campaign relaunch with a fixed conversion event (planned 28 Sep) has still not happened; the 09/01 campaign is the live one and is in its fourth week at Flag ($3.51 CPL on 30 days, $2.76 on 14). October direct revenue is up on a very small base.

### Bison Ridge Retreat — AM Chiara — account Bison Ridge Retreat Ad Account (950241787963535) — live read

ToF (Discovery / Keyword) spend, not scored: $597 over 30 days.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - RT Engagers | Lead Gen (MoF) | 30d | $149 | 66 leads | CPL $2.26 | — | Review w/ HG AI | CPC $0.37 > $0.30 | 14d CPL $2.48 | Still open, week 2 |
| BoF - Sales Campaign - RT Website Visitors | Retargeting (BoF) | 14d | $71 | 0 purchases | ROAS — | 1.84 | Under gate | within lines | spend $70.77 < $200 gate | Unchanged |

Monthly ROI: July: spend $924, 9 Meta-attributed bookings, blended ROAS 20.3x, retargeting ROAS —, CPL $1.75 on 23 leads · August: spend $952, 3 Meta-attributed bookings, blended ROAS 8.0x, retargeting ROAS —, CPL $2.47 on 63 leads · September: spend $893, 5 Meta-attributed bookings, blended ROAS 9.3x, retargeting ROAS —, CPL $2.54 on 59 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### AwayFrames — AM Alicia — account Awayframes Ad Account (2471256056603833) — live read

ToF (Discovery / Keyword) spend, not scored: $601 over 30 days.

This month (booked 1 Oct–19 Oct): direct revenue $10,354 from 12 bookings, −34% vs 1 Sep–19 Sep ($15,681 from 10 bookings) · promo codes: 5 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers 07/31/2026 | Lead Gen (MoF) | 30d | $149 | 104 leads | CPL $1.43 | — | Review w/ HG AI | CPC $0.30 > $0.30 | 14d CPL $1.30 | Still open, week 5 |
| BoF - Sales Campaign - Retargeting Website Visitors 07/31/2026 | Retargeting (BoF) | 14d | $69 | 1 purchases | ROAS 9.4x | 2.59 | Under gate | within lines | spend $69.37 < $200 gate; 30d ROAS 9.3x, 2 purchases | Unchanged |

Monthly ROI: July: spend $923, 9 Meta-attributed bookings, blended ROAS 18.6x, CPL $2.44 on 2 leads · August: spend $869, 8 Meta-attributed bookings, blended ROAS 21.8x, retargeting ROAS 27.0x, CPL $2.68 on 58 leads · September: spend $895, 7 Meta-attributed bookings, blended ROAS 11.1x, retargeting ROAS 4.9x, CPL $1.83 on 82 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### North Star Lodge & Resort — AM Charlotte — account North Star Lodge & Resort Ads (2003562593933799) — live read

ToF (Discovery / Keyword) spend, not scored: $729 over 30 days.

This month (booked 1 Oct–19 Oct): direct revenue $48,275 from 108 bookings, −17% vs 1 Sep–19 Sep ($58,249 from 94 bookings) · promo codes: not tracked by cloudbeds.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 09/09/2026 | Retargeting (BoF) | 14d | $70 | 0 purchases | ROAS — | 2.86 | Under gate | CPC $1.21 > $0.62 | spend $70.12 < $200 gate | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 10/02/26 | Lead Gen (MoF) | 30d | $68 | 0 leads | CPL — | — | Under gate | CPC $0.93 > $0.30; CPM $24.04 > $14.84 | spend $68.21 < $100 gate | Unchanged |

Monthly ROI: September: spend $580, 0 Meta-attributed bookings, blended ROAS —. Note in the September file: Newly launched campaigns — $579.92 spent, no revenue from ads yet. Revenue shown is from the client reporting sheet; no booking-level data this month.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. 14 Oct Strategy: the full plugin, script and API set is installed (Leshan); BoF spend is low ($70 in 14 days) and no BoF reservation has come through yet, though clicks are visible in the platform.

### The Outpost — AM Anna — account The Outpost Grand Canyon (1530849534802936) — live read

ToF (Discovery / Keyword) spend, not scored: $897 over 30 days.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 10/08/2026 | Retargeting (BoF) | 14d | $102 | 0 purchases | ROAS — | 1.85 | Under gate | within lines | spend $102.42 < $200 gate | Unchanged |
| BoF - Sales Campaign - Retargeting Website Visitors - 08/29/2026 | Retargeting (BoF) | 14d | $35 | 0 purchases | ROAS — | 1.63 | Under gate | CPC $0.67 > $0.62 | spend $34.63 < $200 gate | Unchanged |

Monthly ROI: July: spend $2,182, 1 Meta-attributed bookings, blended ROAS 0.2x, CPL $1.61 on 202 leads · August: spend $1,876, 7 Meta-attributed bookings, blended ROAS 2.1x, CPL $1.71 on 181 leads · September: spend $2,081, 18 Meta-attributed bookings, blended ROAS 3.8x, retargeting ROAS —, CPL $1.80 on 167 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. The second BoF campaign (10/08, $10/day) runs beside the 08/29 one; both are under the $200 gate with 0 purchases in 14 days. Decision 30 (pause the old one) is still open.

### American River Resort — AM Nicole — account American River Resort (953162737054331) — live read

ToF (Discovery / Keyword) spend, not scored: $827 over 30 days.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

No live Lead Gen or Sales campaigns with spend in the window.

Paused in window, not scored: MoF - Lead Campaign - Retargeting Engagers (Lead Gen (MoF)), $551 / 30d, 436 leads, CPL $1.26. Live campaigns only are scored (decision 2026-09-23).

Monthly ROI: July: spend $1,544, 4 Meta-attributed bookings, blended ROAS 1.1x · August: spend $1,529, 3 Meta-attributed bookings, blended ROAS 1.4x, CPL $18.30 on 30 leads · September: spend $1,453, 0 Meta-attributed bookings, blended ROAS —, CPL $1.48 on 377 leads. Note in the September file: We had no promo code usages this month.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. Both campaigns stopped between 15 and 19 Oct (spend check: $0/day live today). The lead campaign spent $551 in the window and is paused now, so nothing is scored. Confirm with Nicole whether this is a pause or an offboarding.

## Footer

- Windows: Lead Gen last 30 days, Sales/Retargeting last 14 days (live). CSV accounts use the export period 2026-10-05 to 2026-10-11 (7 days) and are provisional.
- Gates: $100 Lead Gen, $200 Sales/Retargeting. Campaigns under the gate are listed but not judged.
- Classification: by campaign objective (OUTCOME_LEADS → Lead Gen; OUTCOME_SALES → Sales, split into Retargeting (BoF) or MoF lookalike by name; OUTCOME_TRAFFIC / OUTCOME_ENGAGEMENT → ToF, not scored). CSV accounts have no objective column, so classification there is by name.
- Sales campaigns with an MoF or lookalike prefix are scored on the Retargeting ROAS bands because they optimise for purchases. The Benchmarks doc has no separate band for prospecting sales campaigns; confirm or add one.
- Data path: Marketing API v21.0 insights at campaign level through `scripts/pull-campaign-insights.mts` (purchases = omni_purchase, leads = lead, ROAS = purchase_roas, link clicks = inline_link_clicks), the same fields the claude.ai connector exposed. The connector is no longer used for this report (Shawal, 2026-10-19).
- CTR on live rows is Meta's CTR (all clicks), not link CTR. The doc's click-rate lines are probably link CTR, so treat the CTR diagnostic as indicative.
- Frequency and cost per booking are diagnostics only and do not change the state (decision 2026-09-21). From 2026-10-06 (Shawal) every Sales / Retargeting row shows its frequency, and any value above 5.0 is marked ⚠️ in that column and listed in the Frequency watch section; CSV rows use impressions / reach summed over ad sets, which overstates frequency where ad sets overlap.
- Only campaigns live (ACTIVE) at run time are scored. Paused campaigns that spent inside the window are listed per client as "Paused in window" and never enter Action needed or the counts (decision 2026-09-23).
- Unclassified campaigns: Selah Place: Instagram post: 🔥 𝐒𝐀𝐂𝐑𝐈𝐅𝐈𝐂𝐄 𝐈𝐒 𝐑𝐄𝐐𝐔𝐈𝐑𝐄𝐃 🔥....
- Previous report: 2026-10-13-client-benchmark.csv. Diff joined on campaign_id for live rows and client + campaign name for CSV rows. Diff counts: 6 new, 8 still open, 0 fixed, 33 unchanged, 2 removed.
- Scope changes vs 13 Oct: Sunapee Stays dropped (CRM Meta Ads column now Basic, was Advanced on 13 Oct; account 651114096215889 still runs $50/day and stays in the spend and pixel checks). Advanced in the CRM but with no ad account mapping in PROJECT.md section 5, not scored: Treetop Hideaways (AM Kristal), Glasscombe (AM Charlotte), Cabin Collective (AM Chiara), Casey Key Resort (AM Alicia), Arca Roatan (AM Anna).
- HG AI reports read from `HG AI Reports/` at the project root, dated since the previous run: none.
- Selah Place's prospecting campaign (paused this week) is named with pipes in Meta ("SP | Prospecting Test | LAL + Interests x Creative | 09-2026"); shown here with slashes.
- Meeting notes: every "Meta Ads Strategy", "Meta Ads Sync" or "Meta Ads x HiddenGem AI Sync" calendar event since the previous run that has a "Notes by Gemini" attachment, read via Drive. Client names are matched with an alias list (Flow Home = FLOHOM, Tabber / Tipik Falls / Debug Falls = Tàberg Falls, Sailor Place = Selah Place, Stay on 38 = Stay On 30A, Ashwood River Cabins = Asheville River Cabins).
- This month line: direct booking revenue by booking date from the HiddenGem AI platform (pms_bookings, platform direct/OTA rules, tenants on a shared PMS account narrowed to their own properties), month to date at the run date, against the same day span of the previous month. Promo codes come from the booking payload: Guesty stores the code, Hostaway only a coupon id (counted, no names), Hospitable and Cloudbeds nothing. Pulled with pms_mtd.sql through the Supabase connector. Clients without a PMS connection on the platform show no figures.
- Monthly ROI context from `Monthly ROI data/` (July 2026, August 2026, September 2026). Revenue there comes from the Client Performance Tracking sheet, not the pixel, so its ROAS is not comparable to the pixel ROAS above.
