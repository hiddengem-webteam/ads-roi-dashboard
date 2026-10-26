# Client Benchmark Review (advanced setups) — 2026-10-26

Run: 26 October 2026 (Monday), sixth run, compared against 2026-10-19-client-benchmark.csv. Live reads through the Meta Marketing API with the HiddenGem-Claude system user, the standing data path (`scripts/pull-campaign-insights.mts`, 06:57 to 06:59 PT); every account is live and the CSV export 2026-10-19 to 2026-10-25 was not needed for scoring. Scope: clients marked **Advanced** in the CRM "Meta Ads" column (Clients - Onboarding tab), re-read today: 31 clients, 24 with an ad account. Sunapee Stays is back in scope at Shawal's request although the CRM reads Basic; Glasscombe and Cabin Collective get their first live reads now that their accounts are in the client map. Seven Advanced clients in the CRM have no ad account yet. Only Lead Gen (MoF) and Sales/Retargeting (BoF) campaigns are scored; IG Discovery and Keyword (ToF) spend is shown for context only.

| Advanced clients | Live reads | From CSV | Campaigns scored | Under spend gate | Flag to Shawal | Review w/ HG AI | Monitor | Healthy | Scale w/ HG AI | Frequency over 5 |
|---|---|---|---|---|---|---|---|---|---|---|
| 24 (+7 unmapped) | 24 | 0 | 37 | 13 | 3 | 10 | 12 | 7 | 5 | 1 |

States come from the Decision Making table in the Benchmarks doc. Lead Gen: CPL under $0.30 Scale, $0.30–0.50 Healthy, $0.50–1.00 Monitor, $1.00–2.50 Review, $2.50+ Flag, 30-day window, $100 gate. Sales/Retargeting: ROAS above 15x Scale, 8–15x Healthy, 5–8x Monitor, 2–5x Review, under 2x Flag, 14-day window, $200 gate. Band edges are inclusive on the lower bound.

## Weekly Meta Ads meetings since last run (Notes by Gemini)

Source: "Notes by Gemini" docs attached to the calendar events, read via Drive. Summary, decisions and next steps as Gemini wrote them; client-specific sentences are pulled into each client's section below. Transcript not used.

### Meta Ads Strategy — 2026-10-21 — doc `1WuGjeZnHtMEibfhpZ2wky-XTdW6MVJYFvTMKfNkY0eE`

Database spend cap approved with AI attribution strategies and Meta ads focus.

Database Spend Cap Approval

Spend cap for cash egress disabled to accommodate expanding client database usage.

Meta Ads Attribution Solution

Automated duplicate removal process implemented through Hidden Gem AI to ensure reporting accuracy.

Prioritizing Meta Ads Automation

Transition to local open-source models tabled to focus on high-leverage Meta ads automation.

Decisions:
- Attribution model for ad campaigns and promo codes The team aligned on implementing a matching algorithm within Hidden Gem AI to reconcile purchase events, promo code usages, and property management system data to prevent double-counting in ad attribution.
- Automated attribution approach to resolve booking double-counting The team aligned on using an automated attribution approach where Hidden Gem AI checks reservation amounts and promo code usage against Meta ads conversions API data to eliminate double-counting.
- Cloud Beds API coupon exposure verification Leshan will contact Cloud Beds to confirm that their API exposes coupons and reservation values.
- Tabling local AI model transition The team agreed to table local AI model migration for a couple of months until hardware or open-source models advance further.

Next steps:
- [Pooja Murugavel] Contact Gillian: Inform Gillian about the intent to disable the spend cap to accommodate increased storage requirements for new clients.
- [The group] Resolve Attribution: Analyze purchase values to correlate retargeting ad events with promo code usages to prevent double counting of booking revenue.
- [Leshan Patterson] Contact Cloudbeds: Confirm if the Cloudbeds API exposes coupon data associated with reservation values.
- [Shawal Nazir, Dustin Baker] Sync Attribution Strategy: Map out and verify the matching algorithm to attribute purchase events to bookings. Coordinate the logic for deduplication and promo code tracking within the system.
- [Dustin Baker] Solidify ROAS Goals: Confirm target return on ad spend benchmarks with clients to finalize performance goals. Set specific budget ranges based on these agreed metrics.
- [Leshan Patterson] Organize Sync Meetings: Schedule and lead meetings to discuss budget recommendations and attribution implementation. Coordinate with the team to align on project execution steps.
- [Dustin Baker] AI Strategy: Discuss the AI team strategy on the subsequent meeting link.

## Action needed

Sales and Retargeting campaigns first, then Lead Gen. Within each, Flag to Shawal before Review w/ HG AI, highest spend first.

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| Stay Saluda NC | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $422 / 14d | ROAS 1.7x | Flag to Shawal | Still open, week 2 (was Review w/ HG AI) |
| Endless Stays | Nicole | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $1,055 / 14d | ROAS 4.4x | Review w/ HG AI | Still open, week 4 |
| Ridge & Falls | Makenna | MoF - Lead Campaign - Retargeting Engagers - 09/01/26 | Lead Gen (MoF) | $150 / 30d | CPL $2.63 | Flag to Shawal | Still open, week 5 |
| North Star Lodge & Resort | Charlotte | MoF - Lead Campaign - Retargeting Engagers - 10/02/26 | Lead Gen (MoF) | $104 / 30d | CPL — | Flag to Shawal | New flag, was Under gate |
| Stay On 30A | Charlotte | MoF - Lead Campaign - RT Engagers - 07/16/26 | Lead Gen (MoF) | $1,502 / 30d | CPL $1.41 | Review w/ HG AI | Still open, week 6 |
| Starlight Haven Weiss Lake | Charlotte | New Leads Campaign - 03/03/26 | Lead Gen (MoF) | $752 / 30d | CPL $1.06 | Review w/ HG AI | New flag, was Monitor |
| Paradise Pointe | Makenna | MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | $749 / 30d | CPL $1.01 | Review w/ HG AI | New flag, was Monitor |
| Sunapee Stays | Charlotte | MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | $302 / 30d | CPL $1.70 | Review w/ HG AI | New, not in the 19 Oct run |
| Green Springs Inn | Alicia | MoF - Lead Campaign/08/28/2026 | Lead Gen (MoF) | $301 / 30d | CPL $1.37 | Review w/ HG AI | Still open, week 6 |
| Walden Retreats | Anna | MoF - Lead Campaign - Retargeting Engagers - 10/06/2026 | Lead Gen (MoF) | $198 / 30d | CPL $1.28 | Review w/ HG AI | Still open, week 2 |
| Bison Ridge Retreat | Chiara | MoF - Lead Campaign - RT Engagers | Lead Gen (MoF) | $151 / 30d | CPL $1.98 | Review w/ HG AI | Still open, week 3 |
| Little River Landing | Makenna | MoF - Lead Campaign - Retargeting Engagers - 09/16/2026 | Lead Gen (MoF) | $150 / 30d | CPL $1.53 | Review w/ HG AI | Still open, week 4 |
| AwayFrames | Alicia | MoF - Lead Campaign - Retargeting Engagers 07/31/2026 | Lead Gen (MoF) | $150 / 30d | CPL $1.35 | Review w/ HG AI | Still open, week 6 |

## Scale candidates

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| Stay On 30A | Charlotte | MoF - Sales Campaign - HiddenGem Pixel LoL - 07/17/26 | Sales (MoF lookalike) | $2,811 / 14d | ROAS 18.6x | Scale w/ HG AI | Was Healthy |
| Stay On 30A | Charlotte | BoF - Sales Campaign - RT Website Visitors - 07/13/26 | Retargeting (BoF) | $2,107 / 14d | ROAS 15.9x | Scale w/ HG AI | Unchanged |
| Paradise Pointe | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $710 / 14d | ROAS 15.1x | Scale w/ HG AI | Fixed, was Review w/ HG AI |
| Starlight Haven Weiss Lake | Charlotte | Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | $629 / 14d | ROAS 21.2x | Scale w/ HG AI | Unchanged |
| Starlight Haven Hot Springs | Charlotte | Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | $281 / 14d | ROAS 21.0x | Scale w/ HG AI | Unchanged |

## Frequency watch (Sales / Retargeting above 5)

Sales, Retargeting and MoF-lookalike campaigns whose 14-day frequency is above 5.0 (Shawal, 6 Oct 2026). Frequency does not change the ROAS state; this is the list to refresh creative or widen the audience on. The diagnostics column still notes anything above 3.0.

| Client | AM | Campaign | Type | Frequency | Spend / window | Governing metric | State |
|---|---|---|---|---|---|---|---|
| Paradise Pointe | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 6.33 | $710 / 14d | ROAS 15.1x | Scale w/ HG AI |

## Per client, ordered by scored MoF + BoF spend

### Stay On 30A — AM Charlotte — account Stay on 30a Ads (25640434272252212) — live read

ToF (Discovery / Keyword) spend, not scored: $3,003 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $248,725 from 94 bookings, −27% vs 1 Sep–26 Sep ($339,687 from 121 bookings) · promo codes: 40 uses (EARLY BIRD DIRECT ×17, VIP100 ×13, WELCOME100 ×6, WELCOMEBACK15 ×3, CINDYSWANSON10 ×2, 10%COAST ×1, ESCAPE30A ×1, RETURNINGGUEST ×1, TUCKS20 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - RT Engagers - 07/16/26 | Lead Gen (MoF) | 30d | $1,502 | 1069 leads | CPL $1.41 | — | Review w/ HG AI | CPC $0.42 > $0.30; CPM $37.23 > $14.84 | 14d CPL $1.52 | Still open, week 6 |
| MoF - Sales Campaign - HiddenGem Pixel LoL - 07/17/26 | Sales (MoF lookalike) | 14d | $2,811 | 9 purchases | ROAS 18.6x | 1.93 | Scale w/ HG AI | CPC $0.91 > $0.62; CPM $23.80 > $16.50; cost/booking $312.37 > $90 | 30d ROAS 14.4x, 21 purchases | Was Healthy |
| BoF - Sales Campaign - RT Website Visitors - 07/13/26 | Retargeting (BoF) | 14d | $2,107 | 9 purchases | ROAS 15.9x | 4.51 | Scale w/ HG AI | CPC $1.69 > $0.62; CPM $26.42 > $16.50; cost/booking $234.07 > $90; freq 4.5 > 3.0 | 30d ROAS 22.5x, 25 purchases | Unchanged |

Monthly ROI: July: spend $6,407, 67 Meta-attributed bookings, blended ROAS 32.3x, retargeting ROAS 14.6x, CPL $1.24 on 583 leads · August: spend $12,420, 85 Meta-attributed bookings, blended ROAS 17.8x, retargeting ROAS 15.5x, CPL $2.58 on 594 leads · September: spend $12,606, 91 Meta-attributed bookings, blended ROAS 24.4x, retargeting ROAS 23.1x, CPL $1.52 on 1001 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). The HiddenGem Pixel lookalike campaign moves up to Scale at 18.6x ($2,811 in 14 days, 9 purchases; 14.4x on 30 days), joining the BoF at 15.9x. Leads $1.41, sixth week at Review on 1,069 leads. October direct revenue $249k from 94 bookings, 27% below September's same span, with 40 promo-code uses (EARLY BIRD DIRECT ×17, VIP100 ×13).

### Tàberg Falls — AM Alicia — account Táberg Falls (827872700004659) — live read

ToF (Discovery / Keyword) spend, not scored: $2,163 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $49,504 from 34 bookings, −8% vs 1 Sep–26 Sep ($53,715 from 36 bookings) · promo codes: 2 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Leads Campaign - 06/19/26 | Lead Gen (MoF) | 30d | $1,635 | 2794 leads | CPL $0.59 | — | Monitor | within lines | 14d CPL $0.59 | Unchanged |
| MoF - Lookalike Sales Campaign - 08/21/2026 | Sales (MoF lookalike) | 14d | $745 | 4 purchases | ROAS 7.9x | 1.66 | Monitor | CPM $23.62 > $16.50; cost/booking $186.25 > $90 | 30d ROAS 12.0x, 13 purchases | Was Healthy |
| BoF - Website Retargeting Campaign - 08/21/2026 | Retargeting (BoF) | 14d | $733 | 6 purchases | ROAS 14.8x | 2.99 | Healthy | CPC $0.69 > $0.62; CPM $25.36 > $16.50; cost/booking $122.11 > $90 | 30d ROAS 10.2x, 13 purchases | Unchanged |

Paused in window, not scored: MoF - Broad (Acquire new customers) - 09/28/2026 (Sales (MoF lookalike)), $359 / 14d, 0 purchases, ROAS —. Live campaigns only are scored (decision 2026-09-23).

Monthly ROI: July: spend $11,739, 80 Meta-attributed bookings, blended ROAS 9.5x, retargeting ROAS 15.8x, CPL $0.67 on 2320 leads · August: spend $11,259, 31 Meta-attributed bookings, blended ROAS 4.5x, retargeting ROAS 8.0x, CPL $0.46 on 4015 leads · September: spend $10,800, 27 Meta-attributed bookings, blended ROAS 4.0x, retargeting ROAS 7.1x, CPL $0.55 on 3261 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). The Broad prospecting campaign (09/28) was paused this week after $359 in the window with no purchases, so the account is back to four campaigns at $200/day. BoF 14.8x Healthy on 6 purchases, Lookalike 8.0x Monitor, leads $0.59 Monitor on 2,794 leads.

### Endless Stays — AM Nicole — account Endless Stays (896372356081479) — live read

ToF (Discovery / Keyword) spend, not scored: $2,298 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $42,667 from 21 bookings, +429% vs 1 Sep–26 Sep ($8,071 from 27 bookings) · promo codes: not tracked by hospitable.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $1,055 | 1 purchases | ROAS 4.4x | 2.91 | Review w/ HG AI | CPC $0.68 > $0.62; CPM $18.92 > $16.50; cost/booking $1,055.32 > $90 | 30d ROAS 3.6x, 3 purchases | Still open, week 4 |
| MoF Lead Campaign - Retargeting Engagers - 09/09/2026 | Lead Gen (MoF) | 30d | $1,486 | 1724 leads | CPL $0.86 | — | Monitor | within lines | 14d CPL $0.95 | Unchanged |

Monthly ROI: July: spend $1,534, 9 Meta-attributed bookings, blended ROAS 16.0x · August: spend $1,553, 10 Meta-attributed bookings, blended ROAS 11.6x, retargeting ROAS 38.8x, CPL $9.73 on 26 leads · September: spend $2,539, 6 Meta-attributed bookings, blended ROAS 2.9x, retargeting ROAS 4.7x, CPL $1.05 on 532 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). BoF 4.4x on a single purchase ($1,055 in 14 days; 3.6x on 3 purchases over 30), fourth week at Review and the biggest Review spend on the list. The platform shows October direct revenue at $42.7k against $8.1k in September's same span (+429%) while the pixel recorded 5 Purchase events all week, so bookings are landing outside the pixel's view; the Hospitable booking flow's purchase event is the thing to check.

### FLOHOM — AM Makenna — account FLOHOM Ads (2100710320122219) — live read

ToF (Discovery / Keyword) spend, not scored: $300 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $89,485 from 102 bookings, −25% vs 1 Sep–26 Sep ($119,117 from 129 bookings) · promo codes: 18 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $837 | 6 purchases | ROAS 5.2x | 2.27 | Monitor | CPC $0.69 > $0.62; CPM $20.38 > $16.50; cost/booking $139.47 > $90 | 30d ROAS 5.7x, 19 purchases | Fixed, was Review w/ HG AI |
| MoF - Lead Campaign - Retargeting Engagers – 08/17/26 | Lead Gen (MoF) | 30d | $502 | 953 leads | CPL $0.53 | — | Monitor | within lines | 14d CPL $0.58 | Unchanged |
| [Myrtle Beach] MoF - Lookalike Sales Campaign - 09/17/26 | Sales (MoF lookalike) | 14d | $280 | 1 purchases | ROAS 6.1x | 2.31 | Monitor | CPC $1.05 > $0.62; CPM $19.90 > $16.50; cost/booking $279.86 > $90 | 30d ROAS 9.7x, 4 purchases | Unchanged |
| MoF - Lookalike Sales Campaign - 07/29/26 | Sales (MoF lookalike) | 14d | $799 | 10 purchases | ROAS 12.3x | 2.38 | Healthy | CPC $0.69 > $0.62; CPM $20.38 > $16.50 | 30d ROAS 11.2x, 24 purchases | Unchanged |

Monthly ROI: July: spend $5,555, 103 Meta-attributed bookings, blended ROAS 17.2x, retargeting ROAS 19.1x, CPL $7.66 on 66 leads · August: spend $9,331, 57 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 8.2x, CPL $2.24 on 708 leads · September: spend $8,855, 66 Meta-attributed bookings, blended ROAS 6.7x, retargeting ROAS 8.9x, CPL $0.50 on 2192 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). BoF Fixed: 5.2x on 6 purchases ($837 in 14 days; 5.7x on 19 purchases over 30) lifts it from Review to Monitor. Lookalike 12.3x Healthy, Myrtle Beach lookalike 6.1x Monitor, leads $0.53 Monitor. October direct revenue is 25% below September's same span.

### Paradise Pointe — AM Makenna — account Paradise Pointe Ads (1585826092078255) — live read

ToF (Discovery / Keyword) spend, not scored: $753 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $114,538 from 120 bookings, +2% vs 1 Sep–26 Sep ($112,170 from 99 bookings) · promo codes: 2 uses (WELCOME10 ×1, WELCOME100 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $749 | 738 leads | CPL $1.01 | — | Review w/ HG AI | within lines | 14d CPL $1.05 | New flag, was Monitor |
| MoF - LoL Sales Campaign - 09/28/26 | Sales (MoF lookalike) | 14d | $702 | 10 purchases | ROAS 7.7x | 2.60 | Monitor | CPC $0.71 > $0.62 | 30d ROAS 8.4x, 31 purchases | Was Healthy |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $710 | 17 purchases | ROAS 15.1x | 6.33 ⚠️ > 5 | Scale w/ HG AI | CPC $0.92 > $0.62; freq 6.3 > 3.0 | 30d ROAS 8.8x, 28 purchases | Fixed, was Review w/ HG AI |

Monthly ROI: July: spend $2,237, 74 Meta-attributed bookings, blended ROAS 21.6x, retargeting ROAS 16.7x, CPL $1.01 on 90 leads · August: spend $3,109, 94 Meta-attributed bookings, blended ROAS 16.8x, retargeting ROAS 18.0x, CPL $1.64 on 471 leads · September: spend $3,074, 48 Meta-attributed bookings, blended ROAS 7.0x, retargeting ROAS 13.0x, CPL $0.97 on 764 leads. Note in the September file: Meta did not record revenue for 12 retargeting purchases (week of Sep 15–21 and Sep 29–30); their value was added manually at the average booking value (12 × $1,170.59 = $14,047.08) and the ROAS updated.

Meeting notes (Meta Ads Strategy 2026-10-21): Meta Ads Attribution Challenge and Double Counting Risk: Dustin Baker presented an attribution challenge using Paradise Point data, explaining the difficulty in crediting direct booking revenue to top-of-funnel giveaway and lead campaigns without double counting against retargeting and purchase campaigns that utilize pixel tracking, welcome 100 promo codes, and email matches.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). BoF Fixed: 15.1x on 17 purchases ($710 in 14 days) takes it from Review to Scale, although 30 days read 8.8x and frequency is 6.3, the only Frequency-watch row, so the audience is being hit hard. Leads tip into Review at $1.01 (band edge). 21 Oct Strategy used this account as the double-counting example: a $730.55 booking on 21 Oct with WELCOME100 was credited by both the BoF pixel and the promo code; the attribution matching algorithm agreed at that meeting is the fix. CAPI still silent (pixel check, week 3).

### Treetop Escapes — AM Makenna — account Treetop Escapes Ads (967636478877602) — live read

ToF (Discovery / Keyword) spend, not scored: $902 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $38,488 from 44 bookings, +18% vs 1 Sep–26 Sep ($32,577 from 38 bookings) · promo codes: 1 uses (WELCOME10 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $902 | 1142 leads | CPL $0.79 | — | Monitor | CPM $19.22 > $14.84 | 14d CPL $0.78 | Unchanged |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $559 | 6 purchases | ROAS 12.4x | 3.35 | Healthy | CPM $18.26 > $16.50; cost/booking $93.11 > $90; freq 3.4 > 3.0 | 30d ROAS 10.9x, 12 purchases | Fixed, was Review w/ HG AI |

Monthly ROI: July: spend $2,487, 44 Meta-attributed bookings, blended ROAS 14.5x, retargeting ROAS 22.2x, CPL $1.48 on 21 leads · August: spend $3,082, 28 Meta-attributed bookings, blended ROAS 8.8x, retargeting ROAS 16.3x, CPL $1.49 on 620 leads · September: spend $2,998, 10 Meta-attributed bookings, blended ROAS 3.8x, retargeting ROAS 7.9x, CPL $0.88 on 1019 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). BoF Fixed: 12.4x on 6 purchases ($559 in 14 days) takes it from Review to Healthy. Leads $0.79 Monitor on 1,142 leads. October direct revenue up 18% on September's span.

### Starlight Haven Weiss Lake — AM Charlotte — account Starlight Haven Weiss Lake (74756899) — live read

ToF (Discovery / Keyword) spend, not scored: $0 over 30 days.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $752 | 707 leads | CPL $1.06 | — | Review w/ HG AI | CPC $0.36 > $0.30 | 14d CPL $1.26 | New flag, was Monitor |
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $629 | 19 purchases | ROAS 21.2x | 2.46 | Scale w/ HG AI | CPC $0.77 > $0.62; CPM $16.59 > $16.50 | 30d ROAS 22.9x, 44 purchases | Unchanged |

Monthly ROI: July: spend $2,163, 41 Meta-attributed bookings, blended ROAS 10.8x, retargeting ROAS 15.2x, CPL $0.74 on 826 leads · August: spend $2,351, 36 Meta-attributed bookings, blended ROAS 10.7x, retargeting ROAS 17.6x, CPL $1.23 on 617 leads · September: spend $2,152, 79 Meta-attributed bookings, blended ROAS 17.4x, retargeting ROAS 23.8x, CPL $1.01 on 734 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). Leads slip from Monitor to Review at $1.06 (band edge; $1.26 on 14 days), 707 leads on $752. BoF holds at Scale, 21.2x on 19 purchases.

### Starlight Haven Hot Springs — AM Charlotte — account Starlight Haven Hot Springs (901138032027913) — live read

ToF (Discovery / Keyword) spend, not scored: $752 over 30 days.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $902 | 2859 leads | CPL $0.32 | — | Healthy | within lines | 14d CPL $0.32 | Unchanged |
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $281 | 9 purchases | ROAS 21.0x | 1.95 | Scale w/ HG AI | within lines | 30d ROAS 24.3x, 21 purchases | Unchanged |

Monthly ROI: July: spend $2,160, 17 Meta-attributed bookings, blended ROAS 5.1x, retargeting ROAS 17.1x, CPL $0.33 on 2813 leads · August: spend $2,193, 19 Meta-attributed bookings, blended ROAS 6.3x, retargeting ROAS 22.3x, CPL $0.36 on 2589 leads · September: spend $2,155, 61 Meta-attributed bookings, blended ROAS 16.5x, retargeting ROAS 28.5x, CPL $0.34 on 2597 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). Both campaigns in good shape: leads $0.32 Healthy on 2,859 leads, BoF 21.0x Scale on 9 purchases.

### Ponderosa Pines Resort — AM Anna — account Ponderosa Pines Resort (1058846326445255) — live read

ToF (Discovery / Keyword) spend, not scored: $1,199 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $36,767 from 126 bookings, −11% vs 1 Sep–26 Sep ($41,238 from 139 bookings) · promo codes: not tracked by newbook.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Leads Campaign - 07/16/26 | Lead Gen (MoF) | 30d | $599 | 618 leads | CPL $0.97 | — | Monitor | within lines | 14d CPL $1.29 | Unchanged |
| Website Retarget Campaign - 07/13/26 | Retargeting (BoF) | 14d | $562 | 14 purchases | ROAS 9.4x | 2.87 | Healthy | CPC $0.71 > $0.62; CPM $21.07 > $16.50 | 30d ROAS 13.3x, 33 purchases | Was Monitor |

Monthly ROI: July: spend $2,089, 17 Meta-attributed bookings, blended ROAS 3.6x, retargeting ROAS 22.3x, CPL $0.91 on 356 leads · August: spend $3,101, 103 Meta-attributed bookings, blended ROAS 15.0x, retargeting ROAS 21.3x, CPL $1.32 on 471 leads · September: spend $2,985, 119 Meta-attributed bookings, blended ROAS 17.9x, retargeting ROAS 21.6x, CPL $0.84 on 708 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). BoF 9.4x Healthy on 14 purchases (13.3x on 30), leads $0.97 Monitor, frequency 2.9. October direct revenue 11% below September's span.

### Stay Saluda NC — AM Makenna — account Stay Saluda Ads (1863632561215857) — live read

ToF (Discovery / Keyword) spend, not scored: $898 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $13,712 from 26 bookings, −21% vs 1 Sep–26 Sep ($17,410 from 27 bookings) · promo codes: 7 uses (WELCOME10 ×5, DUBLE10 ×1, VIP10 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $422 | 2 purchases | ROAS 1.7x | 4.73 | Flag to Shawal | CPC $0.78 > $0.62; CPM $17.76 > $16.50; cost/booking $211.22 > $90; freq 4.7 > 3.0 | 30d ROAS 4.0x, 7 purchases | Still open, week 2 (was Review w/ HG AI) |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $600 | 651 leads | CPL $0.92 | — | Monitor | within lines | 14d CPL $0.91 | Unchanged |

Monthly ROI: July: spend $2,140, 10 Meta-attributed bookings, blended ROAS 2.6x, retargeting ROAS 0.8x · August: spend $2,367, 9 Meta-attributed bookings, blended ROAS 3.7x, retargeting ROAS 5.2x, CPL $2.59 on 146 leads · September: spend $2,394, 6 Meta-attributed bookings, blended ROAS 1.3x, retargeting ROAS 3.5x, CPL $1.00 on 596 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). BoF drops from Review (4.3x) to Flag at 1.7x on 2 purchases ($422 in 14 days; 4.0x on 7 purchases over 30), frequency 4.7 and still climbing, so the retargeting pool is saturated. Leads hold at $0.92 (Monitor). October direct revenue is 21% below September's same span. The Saluda GHL hosts still fire the Inspired Retreats pixel (pixel check, week 6).

### Asheville River Cabins — AM Charlotte — account Asheville River Cabins Ads (615836588009747) — live read

ToF (Discovery / Keyword) spend, not scored: $1,018 over 30 days.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Website Retargeting Campaign - 06/08/26 | Retargeting (BoF) | 14d | $417 | 7 purchases | ROAS 11.6x | 2.18 | Healthy | CPM $21.33 > $16.50 | 30d ROAS 35.3x, 27 purchases | Was Scale w/ HG AI |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $255 | 811 leads | CPL $0.31 | — | Healthy | within lines | 14d CPL $0.29 | Unchanged |

Monthly ROI: July: spend $2,029, 39 Meta-attributed bookings, blended ROAS 18.6x, retargeting ROAS 51.6x · August: spend $2,424, 82 Meta-attributed bookings, blended ROAS 27.2x, retargeting ROAS 65.0x, CPL $0.42 on 605 leads · September: spend $2,252, 70 Meta-attributed bookings, blended ROAS 19.1x, retargeting ROAS 42.5x, CPL $0.30 on 936 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). BoF 11.6x Healthy on 7 purchases (35.3x on 30 days), leads $0.31 Healthy. 21 Oct Strategy: Leshan is contacting Cloudbeds to confirm the API exposes coupon and reservation data, which is also what the CAPI send through HG AI needs; the pixel is still browser-only.

### Selah Place — AM Alicia — account Selah.place (1275283434220508) — live read

ToF (Discovery / Keyword) spend, not scored: $641 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $21,173 from 42 bookings, −4% vs 1 Sep–26 Sep ($22,126 from 41 bookings) · promo codes: 15 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF-Website Retarget Campaign - 07/24/2026 | Retargeting (BoF) | 14d | $430 | 6 purchases | ROAS 7.5x | 4.13 | Monitor | CPM $19.74 > $16.50; freq 4.1 > 3.0 | 30d ROAS 10.9x, 15 purchases | Was Healthy |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $214 | 368 leads | CPL $0.58 | — | Monitor | within lines | 14d CPL $0.57 | Unchanged |

Client-run, not scored: SP / Prospecting Test / LAL + Interests x Creative / 09-2026 (Sales, paused), created by Nathan Jay Herrington on 2026-09-21, $79 / 14d, 0 purchases, ROAS —. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Willow / Pre-Sales / VIP List / 10-2026 (Sales, paused), created by Nathan Jay Herrington on 2026-10-19, $543 / 14d, 1 purchases, ROAS 0.1x. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: Instagram post: 🔥 𝐒𝐀𝐂𝐑𝐈𝐅𝐈𝐂𝐄 𝐈𝐒 𝐑𝐄𝐐𝐔𝐈𝐑𝐄𝐃 🔥... (Other, paused), created by Live Intentionally Today LIT on 2026-10-15, $42 / 14d, 0 purchases, ROAS —. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Willow / Lead Gen / VIP List / 10-2026 (Lead Gen (MoF), active), created by Nathan Jay Herrington on 2026-10-20, $356 / 30d, 173 leads, CPL $2.06. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Monthly ROI: July: spend $1,054, 4 Meta-attributed bookings, blended ROAS 3.2x, retargeting ROAS 86.3x, CPL $0.80 on 49 leads · August: spend $1,545, 15 Meta-attributed bookings, blended ROAS 4.8x, retargeting ROAS 25.1x, CPL $1.08 on 144 leads · September: spend $1,304, 27 Meta-attributed bookings, blended ROAS 10.4x, retargeting ROAS 38.2x, CPL $0.63 on 232 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). The new $55/day 'SP / Willow / Lead Gen / VIP List' campaign (spend check: account up from $70 to $125/day) was created by Nathan Jay Herrington on the client side, so it is listed below and not scored: $356 in 30 days, 173 leads at $2.06. HiddenGem's BoF 7.5x on 6 purchases (Monitor, frequency 4.1) and leads $0.58 (Monitor) are unchanged.

### Green Springs Inn — AM Alicia — account Green Springs Inn (1390516335151357) — live read

ToF (Discovery / Keyword) spend, not scored: $603 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $32,158 from 74 bookings, +8% vs 1 Sep–26 Sep ($29,868 from 88 bookings) · promo codes: 26 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign/08/28/2026 | Lead Gen (MoF) | 30d | $301 | 220 leads | CPL $1.37 | — | Review w/ HG AI | within lines | 14d CPL $1.22 | Still open, week 6 |
| BoF - Sales Campaign - Retargeting Website Visitors - 08/28/26 | Retargeting (BoF) | 14d | $143 | 3 purchases | ROAS 7.4x | 3.29 | Under gate | CPC $0.71 > $0.62; freq 3.3 > 3.0 | spend $142.77 < $200 gate; 30d ROAS 9.7x, 8 purchases | Unchanged |

Monthly ROI: July: spend $1,222, 17 Meta-attributed bookings, blended ROAS 7.8x, retargeting ROAS 14.6x, CPL $5.65 on 8 leads · August: spend $1,247, 23 Meta-attributed bookings, blended ROAS 8.2x, retargeting ROAS 17.1x, CPL $9.09 on 34 leads · September: spend $1,199, 24 Meta-attributed bookings, blended ROAS 8.5x, retargeting ROAS 9.0x, CPL $1.84 on 166 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). Leads $1.37, sixth week at Review ($1.22 on 14 days, improving). BoF 7.4x on 3 purchases, under the gate at $143.

### Sunapee Stays — AM Charlotte — account Sunapee Stays Ads Account (651114096215889) — live read

ToF (Discovery / Keyword) spend, not scored: $901 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $25,396 from 45 bookings, −37% vs 1 Sep–26 Sep ($40,231 from 45 bookings) · promo codes: not tracked by ownerrez.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $302 | 178 leads | CPL $1.70 | — | Review w/ HG AI | CPC $0.36 > $0.30; CPM $16.84 > $14.84 | 14d CPL $2.17 | New, not in the 19 Oct run |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $138 | 3 purchases | ROAS 11.1x | 2.91 | Under gate | CPC $0.89 > $0.62 | spend $138.39 < $200 gate; 30d ROAS 15.4x, 7 purchases | New, not in the 19 Oct run |

Monthly ROI: July: spend $939, 16 Meta-attributed bookings, blended ROAS 9.9x, CPL $2.06 on 9 leads · August: spend $1,494, 10 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 25.1x, CPL $2.74 on 112 leads · September: spend $1,495, 14 Meta-attributed bookings, blended ROAS 6.5x, retargeting ROAS 6.7x, CPL $1.64 on 184 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). Back in the advanced reporting at Shawal's request (the CRM reads Basic since 19 Oct). Leads $1.70 on 30 days ($2.17 on 14) enters at Review; BoF 11.1x on 3 purchases is under the $200 gate ($138; 15.4x on 7 purchases over 30 days). October direct revenue $25.4k, 37% below September's span.

### Walden Retreats — AM Anna — account Walden Retreats (973261794434226) — live read

ToF (Discovery / Keyword) spend, not scored: $206 over 30 days.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers - 10/06/2026 | Lead Gen (MoF) | 30d | $198 | 155 leads | CPL $1.28 | — | Review w/ HG AI | CPC $0.40 > $0.30; CPM $19.41 > $14.84 | 14d CPL $1.35 | Still open, week 2 |
| BoF - Sales Campaign - Retargeting Website Visitors - 06/10/2026 | Retargeting (BoF) | 14d | $139 | 9 purchases | ROAS 46.6x | 2.36 | Under gate | CPC $0.70 > $0.62; CPM $23.14 > $16.50 | spend $139.13 < $200 gate; 30d ROAS 39.7x, 10 purchases | Unchanged |

Client-run, not scored: TOF Wedding Leads 10.8.26 (Lead Gen (MoF), active), created by Lindsey Cooke on 2026-10-08, $370 / 30d, 26 leads, CPL $14.22. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: TOF Wedding Leads (alt aud) 10.9.26 (Lead Gen (MoF), paused), created by Lindsey Cooke on 2026-10-09, $31 / 30d, 0 leads, CPL —. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). HiddenGem's leads campaign $1.28 on 155 leads, second week at Review; BoF 46.6x on 9 purchases but under the gate at $139. The client's own 'TOF Wedding Leads' campaign (Lindsey Cooke) is listed below and not scored: $14.22 CPL on 26 leads over 30 days.

### Ridge & Falls — AM Makenna — account Ridge & Falls ad account (1313401330776046) — live read

ToF (Discovery / Keyword) spend, not scored: $1,508 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $4,031 from 9 bookings, +363% vs 1 Sep–26 Sep ($871 from 2 bookings) · promo codes: 0 uses.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers - 09/01/26 | Lead Gen (MoF) | 30d | $150 | 57 leads | CPL $2.63 | — | Flag to Shawal | CPC $0.32 > $0.30 | 14d CPL $2.05 | Still open, week 5 |
| BoF - Sales Campaign - Retargeting Website Visitors - 09/01/26 | Retargeting (BoF) | 14d | $118 | 5 purchases | ROAS 24.7x | 4.04 | Under gate | freq 4.0 > 3.0 | spend $117.83 < $200 gate; 30d ROAS 20.2x, 8 purchases | Unchanged |

Monthly ROI: September: spend $1,036, 0 Meta-attributed bookings, blended ROAS —, retargeting ROAS —, CPL $8.16 on 16 leads. Note in the September file: Newly launched campaigns — $1,036.47 spent, no revenue from ads yet (spend exceeds the $871.49 September direct revenue, as expected for a launch month).

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). Flag, week 5: $2.63 CPL on 30 days ($2.05 on 14) on the 09/01 lead campaign; the relaunch with a fixed conversion event (planned 28 Sep) has still not happened. BoF 24.7x on 5 purchases but under the $200 gate ($118). October direct revenue $4.0k from 9 bookings against $871 in September's span.

### Little River Landing — AM Makenna — account Little River Landing (884285717873613) — live read

ToF (Discovery / Keyword) spend, not scored: $1,654 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $3,577 from 16 bookings, −2% vs 1 Sep–26 Sep ($3,665 from 20 bookings) · promo codes: 0 uses.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers - 09/16/2026 | Lead Gen (MoF) | 30d | $150 | 98 leads | CPL $1.53 | — | Review w/ HG AI | CPC $0.41 > $0.30; CPM $19.56 > $14.84 | 14d CPL $1.83 | Still open, week 4 |
| BoF - Sales Campaign - Retargeting Website Visitors - 09/16/2026 | Retargeting (BoF) | 14d | $116 | 1 purchases | ROAS 3.4x | 3.05 | Under gate | cost/booking $115.61 > $90; freq 3.1 > 3.0 | spend $115.61 < $200 gate; 30d ROAS 2.0x, 1 purchases | Unchanged |

Monthly ROI: September: spend $921, 0 Meta-attributed bookings, blended ROAS —, retargeting ROAS —, CPL $1.86 on 46 leads. Note in the September file: Newly launched campaigns — $921.36 spent, no revenue from ads yet.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). Leads $1.53, fourth week at Review. BoF 3.4x on 1 purchase, under the gate ($116).

### Bison Ridge Retreat — AM Chiara — account Bison Ridge Retreat Ad Account (950241787963535) — live read

ToF (Discovery / Keyword) spend, not scored: $599 over 30 days.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - RT Engagers | Lead Gen (MoF) | 30d | $151 | 76 leads | CPL $1.98 | — | Review w/ HG AI | CPC $0.39 > $0.30 | 14d CPL $2.20 | Still open, week 3 |
| BoF - Sales Campaign - RT Website Visitors | Retargeting (BoF) | 14d | $69 | 0 purchases | ROAS — | 1.87 | Under gate | within lines | spend $69.31 < $200 gate | Unchanged |

Monthly ROI: July: spend $924, 9 Meta-attributed bookings, blended ROAS 20.3x, retargeting ROAS —, CPL $1.75 on 23 leads · August: spend $952, 3 Meta-attributed bookings, blended ROAS 8.0x, retargeting ROAS —, CPL $2.47 on 63 leads · September: spend $893, 5 Meta-attributed bookings, blended ROAS 9.3x, retargeting ROAS —, CPL $2.54 on 59 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). Leads $1.98 on 76 leads, third week at Review ($2.20 on 14 days, worsening). BoF 0 purchases on $69, under the gate.

### AwayFrames — AM Alicia — account Awayframes Ad Account (2471256056603833) — live read

ToF (Discovery / Keyword) spend, not scored: $600 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $14,311 from 16 bookings, −9% vs 1 Sep–26 Sep ($15,681 from 10 bookings) · promo codes: 5 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers 07/31/2026 | Lead Gen (MoF) | 30d | $150 | 111 leads | CPL $1.35 | — | Review w/ HG AI | CPC $0.30 > $0.30 | 14d CPL $1.68 | Still open, week 6 |
| BoF - Sales Campaign - Retargeting Website Visitors 07/31/2026 | Retargeting (BoF) | 14d | $69 | 2 purchases | ROAS 50.4x | 2.70 | Under gate | CPC $0.66 > $0.62 | spend $69.30 < $200 gate; 30d ROAS 27.5x, 3 purchases | Unchanged |

Monthly ROI: July: spend $923, 9 Meta-attributed bookings, blended ROAS 18.6x, CPL $2.44 on 2 leads · August: spend $869, 8 Meta-attributed bookings, blended ROAS 21.8x, retargeting ROAS 27.0x, CPL $2.68 on 58 leads · September: spend $895, 7 Meta-attributed bookings, blended ROAS 11.1x, retargeting ROAS 4.9x, CPL $1.83 on 82 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). Leads $1.35, sixth week at Review on $5/day. BoF 50.4x on 2 purchases, under the gate.

### North Star Lodge & Resort — AM Charlotte — account North Star Lodge & Resort Ads (2003562593933799) — live read

ToF (Discovery / Keyword) spend, not scored: $656 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $63,390 from 159 bookings, −64% vs 1 Sep–26 Sep ($176,945 from 183 bookings) · promo codes: not tracked by cloudbeds.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers - 10/02/26 | Lead Gen (MoF) | 30d | $104 | 0 leads | CPL — | — | Flag to Shawal | CPC $0.90 > $0.30; CPM $24.53 > $14.84 | no leads | New flag, was Under gate |
| BoF - Sales Campaign - Retargeting Website Visitors - 09/09/2026 | Retargeting (BoF) | 14d | $70 | 1 purchases | ROAS 3.0x | 2.69 | Under gate | CPC $0.98 > $0.62 | spend $69.86 < $200 gate; 30d ROAS 1.7x, 1 purchases | Unchanged |

Monthly ROI: September: spend $580, 0 Meta-attributed bookings, blended ROAS —. Note in the September file: Newly launched campaigns — $579.92 spent, no revenue from ads yet. Revenue shown is from the client reporting sheet; no booking-level data this month.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). New Flag: the 10/02 lead campaign crossed the $100 gate at $104 with 0 leads (CPC $0.90, CPM $24.53), so it is scored for the first time and has nothing to show. BoF $70 in 14 days, 1 purchase, under the gate. Pixel check this week: the Cloudbeds booking engine stopped firing either North Star pixel after the morning of 19 Oct, so booking-engine purchases are no longer reaching Meta; Charlotte and Leshan to confirm what changed in Cloudbeds (14 Oct plugin and script install) and reinstall the canonical pixel. October direct revenue is 64% below September's span (shoulder season in Killington).

### The Outpost — AM Anna — account The Outpost Grand Canyon (1530849534802936) — live read

ToF (Discovery / Keyword) spend, not scored: $894 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $20,278 from 45 bookings, −32% vs 1 Sep–26 Sep ($29,764 from 69 bookings) · promo codes: not tracked by newbook.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 10/08/2026 | Retargeting (BoF) | 14d | $136 | 1 purchases | ROAS 2.8x | 2.11 | Under gate | CPC $0.66 > $0.62; cost/booking $136.49 > $90 | spend $136.49 < $200 gate; 30d ROAS 2.2x, 1 purchases | Unchanged |

Monthly ROI: July: spend $2,182, 1 Meta-attributed bookings, blended ROAS 0.2x, CPL $1.61 on 202 leads · August: spend $1,876, 7 Meta-attributed bookings, blended ROAS 2.1x, CPL $1.71 on 181 leads · September: spend $2,081, 18 Meta-attributed bookings, blended ROAS 3.8x, retargeting ROAS —, CPL $1.80 on 167 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). Only the 10/08 BoF campaign spent in the window ($136, 1 purchase, 2.8x), under the gate; the 08/29 one is no longer spending. Decision 30 (pause the old one) can close if it stays that way.

### Glasscombe — AM Charlotte — account Glasscombe (2030318804465316) — live read

ToF (Discovery / Keyword) spend, not scored: $248 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $4,759 from 13 bookings, −56% vs 1 Sep–26 Sep ($10,790 from 25 bookings) · promo codes: not tracked by cloudbeds.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 10/09/26. | Retargeting (BoF) | 14d | $59 | 0 purchases | ROAS — | 1.80 | Under gate | within lines | spend $58.91 < $200 gate | New, not in the 19 Oct run |
| MoF - Lead Campaign - Retargeting Engagers -  10/09/26 | Lead Gen (MoF) | 30d | $58 | 190 leads | CPL $0.31 | — | Under gate | within lines | spend $58.23 < $100 gate; 14d CPL $0.31 | New, not in the 19 Oct run |

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). First live read (account 2030318804465316 added to the client map today; the three campaigns were created by Charlotte on 13 and 14 Oct). Both scored campaigns are under the gate: leads $0.31 on 190 leads ($58), which would be Healthy at the gate, and BoF 0 purchases on $59. October direct revenue is 56% below September's span (UK shoulder season).

### Cabin Collective — AM Chiara — account Cabin Collective (2194562394139883) — live read

ToF (Discovery / Keyword) spend, not scored: $46 over 30 days.

This month (booked 1 Oct–26 Oct): direct revenue $52,815 from 28 bookings, +64% vs 1 Sep–26 Sep ($32,229 from 19 bookings) · promo codes: not tracked by ownerrez.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 10/20/26 | Retargeting (BoF) | 14d | $48 | 2 purchases | ROAS 119.9x | 1.73 | Under gate | within lines | spend $47.52 < $200 gate; 30d ROAS 119.9x, 2 purchases | New, not in the 19 Oct run |
| MoF - Lead Campaign - Retargeting Engagers - 10/20/26 | Lead Gen (MoF) | 30d | $47 | 36 leads | CPL $1.30 | — | Under gate | CPC $0.36 > $0.30; CPM $17.41 > $14.84 | spend $46.95 < $100 gate; 14d CPL $1.30 | New, not in the 19 Oct run |

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). First live read: the three-campaign structure launched 20 Oct (created by Chiara on 21 Oct), account added to the client map today. Under the gate on both: leads $1.30 on 36 leads ($47), BoF 2 purchases on $48 (119.9x). The platform shows October direct revenue $52.8k from 28 bookings, +64% on September's span.

### American River Resort — AM Nicole — account American River Resort (953162737054331) — live read

ToF (Discovery / Keyword) spend, not scored: $616 over 30 days.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

No live Lead Gen or Sales campaigns with spend in the window.

Paused in window, not scored: MoF - Lead Campaign - Retargeting Engagers (Lead Gen (MoF)), $414 / 30d, 329 leads, CPL $1.26. Live campaigns only are scored (decision 2026-09-23).

Monthly ROI: July: spend $1,544, 4 Meta-attributed bookings, blended ROAS 1.1x · August: spend $1,529, 3 Meta-attributed bookings, blended ROAS 1.4x, CPL $18.30 on 30 leads · September: spend $1,453, 0 Meta-attributed bookings, blended ROAS —, CPL $1.48 on 377 leads. Note in the September file: We had no promo code usages this month.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (not run, Shawal 26 Oct). Ads off since 15 Oct: paused, not offboarded (Shawal, 26 Oct). The lead campaign's trailing spend ($414, 329 leads at $1.26) is listed as paused and nothing is scored. The row stays until the campaigns come back.

## Footer

- Windows: Lead Gen last 30 days, Sales/Retargeting last 14 days (live). CSV accounts use the export period 2026-10-19 to 2026-10-25 (7 days) and are provisional.
- Gates: $100 Lead Gen, $200 Sales/Retargeting. Campaigns under the gate are listed but not judged.
- Classification: by campaign objective (OUTCOME_LEADS → Lead Gen; OUTCOME_SALES → Sales, split into Retargeting (BoF) or MoF lookalike by name; OUTCOME_TRAFFIC / OUTCOME_ENGAGEMENT → ToF, not scored). CSV accounts have no objective column, so classification there is by name.
- Sales campaigns with an MoF or lookalike prefix are scored on the Retargeting ROAS bands because they optimise for purchases. The Benchmarks doc has no separate band for prospecting sales campaigns; confirm or add one.
- Data path: Marketing API v21.0 insights at campaign level through `scripts/pull-campaign-insights.mts` (purchases = omni_purchase, leads = lead, ROAS = purchase_roas, link clicks = inline_link_clicks), the same fields the claude.ai connector exposed. The connector is no longer used for this report (Shawal, 2026-10-19).
- CTR on live rows is Meta's CTR (all clicks), not link CTR. The doc's click-rate lines are probably link CTR, so treat the CTR diagnostic as indicative.
- Frequency and cost per booking are diagnostics only and do not change the state (decision 2026-09-21). From 2026-10-06 (Shawal) every Sales / Retargeting row shows its frequency, and any value above 5.0 is marked ⚠️ in that column and listed in the Frequency watch section; CSV rows use impressions / reach summed over ad sets, which overstates frequency where ad sets overlap.
- Only campaigns live (ACTIVE) at run time are scored. Paused campaigns that spent inside the window are listed per client as "Paused in window" and never enter Action needed or the counts (decision 2026-09-23).
- Client-run campaigns (created by a non-HiddenGem login per the account activity log, listed under the client, never scored): Selah Place: SP / Prospecting Test / LAL + Interests x Creative / 09-2026 (Nathan Jay Herrington), SP / Willow / Pre-Sales / VIP List / 10-2026 (Nathan Jay Herrington), Instagram post: 🔥 𝐒𝐀𝐂𝐑𝐈𝐅𝐈𝐂𝐄 𝐈𝐒 𝐑𝐄𝐐𝐔𝐈𝐑𝐄𝐃 🔥... (Live Intentionally Today LIT), SP / Willow / Lead Gen / VIP List / 10-2026 (Nathan Jay Herrington); Walden Retreats: TOF Wedding Leads 10.8.26 (Lindsey Cooke), TOF Wedding Leads (alt aud) 10.9.26 (Lindsey Cooke). Creators are known for campaigns created in the last 180 days; older campaigns are scored as usual.
- Unclassified campaigns: none.
- Previous report: 2026-10-19-client-benchmark.csv. Diff joined on campaign_id for live rows and client + campaign name for CSV rows. Diff counts: 9 new, 9 still open, 3 fixed, 29 unchanged, 0 removed.
- Scope changes vs 19 Oct: Glasscombe (2030318804465316) and Cabin Collective (2194562394139883) added with their first live reads; Sunapee Stays kept in scope (CRM Meta Ads column reads Basic since 19 Oct; kept as Advanced at Shawal's request (2026-10-26)). Advanced in the CRM but with no ad account mapping in PROJECT.md section 5, not scored: Treetop Hideaways (AM Kristal), Casey Key Resort (AM Alicia), Arca Roatan (AM Anna), Gooseberry Lodges (AM Alicia), Dunya Camp (AM Chiara), Nine Pines Retreat (AM Nicole), Lundy Farm (AM Charlotte).
- HG AI reports read from `HG AI Reports/` at the project root, dated since the previous run: none.
- Selah Place's prospecting campaign (paused this week) is named with pipes in Meta ("SP | Prospecting Test | LAL + Interests x Creative | 09-2026"); shown here with slashes.
- Meeting notes: every "Meta Ads Strategy", "Meta Ads Sync" or "Meta Ads x HiddenGem AI Sync" calendar event since the previous run that has a "Notes by Gemini" attachment, read via Drive. Client names are matched with an alias list (Flow Home = FLOHOM, Tabber / Tipik Falls / Debug Falls = Tàberg Falls, Sailor Place = Selah Place, Stay on 38 = Stay On 30A, Ashwood River Cabins = Asheville River Cabins).
- This month line: direct booking revenue by booking date from the HiddenGem AI platform (pms_bookings, platform direct/OTA rules, tenants on a shared PMS account narrowed to their own properties), month to date at the run date, against the same day span of the previous month. Promo codes come from the booking payload: Guesty stores the code, Hostaway only a coupon id (counted, no names), Hospitable and Cloudbeds nothing. Pulled with pms_mtd.sql through the Supabase connector. Clients without a PMS connection on the platform show no figures.
- Monthly ROI context from `Monthly ROI data/` (July 2026, August 2026, September 2026). Revenue there comes from the Client Performance Tracking sheet, not the pixel, so its ROAS is not comparable to the pixel ROAS above.
