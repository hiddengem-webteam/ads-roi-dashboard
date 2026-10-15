# Client Benchmark Review (advanced setups) — 2026-10-13

Run: 13 October 2026 (Tuesday), fourth run, compared against 2026-10-05-client-benchmark.csv. Live reads through the Meta Marketing API with the HiddenGem-Claude system user (11:20 to 11:35 PT), which also reads the four accounts the connector had MCP-disabled, so every account is live this week; the CSV export 2026-10-05 to 2026-10-11 was not needed for scoring. Scope: clients marked **Advanced** in the CRM "Meta Ads" column (Clients - Onboarding tab), re-read today: 27 clients, 22 with an ad account. Walden Retreats enters scope (ad account on the Master sheet from this week). Five Advanced clients in the CRM have no ad account yet. Only Lead Gen (MoF) and Sales/Retargeting (BoF) campaigns are scored; IG Discovery and Keyword (ToF) spend is shown for context only.

| Advanced clients | Live reads | From CSV | Campaigns scored | Under spend gate | Flag to Shawal | Review w/ HG AI | Monitor | Healthy | Scale w/ HG AI | Frequency over 5 |
|---|---|---|---|---|---|---|---|---|---|---|
| 22 (+5 unmapped) | 22 | 0 | 37 | 14 | 1 | 9 | 12 | 8 | 7 | 1 |

States come from the Decision Making table in the Benchmarks doc. Lead Gen: CPL under $0.30 Scale, $0.30–0.50 Healthy, $0.50–1.00 Monitor, $1.00–2.50 Review, $2.50+ Flag, 30-day window, $100 gate. Sales/Retargeting: ROAS above 15x Scale, 8–15x Healthy, 5–8x Monitor, 2–5x Review, under 2x Flag, 14-day window, $200 gate. Band edges are inclusive on the lower bound.

## Weekly Meta Ads meetings since last run (Notes by Gemini)

Source: "Notes by Gemini" docs attached to the calendar events, read via Drive. Summary, decisions and next steps as Gemini wrote them; client-specific sentences are pulled into each client's section below. Transcript not used.

### Meta Ads Strategy — 2026-10-07 — doc `1IDTNY2oBzIjvFxP9T_oKb_YLJzAJ7n-gnFtNqjMxljg`

Competitive analysis covered marketing attribution and offer restructuring for property bookings.

Competitor Analysis and Attribution

Competitor models highlighted client lack of marketing knowledge and attribution tracking challenges.

Technical Tracking and Testing

Custom scripts and plugins improved event match quality scores for property management systems.

Decisions:
- Deployment of custom attribution tracking scripts The team agreed to deploy custom scripts and plugins on booking engines and landing pages to capture click IDs and improve event match quality across Cloudbeds properties.

Next steps:
- [Leshan, Shawal] Sync attribution testing: Meet to discuss the deployment and testing of improved meta ad attribution for clients such as Asheville and Northstar.
- [Leshan] Implement attribution method: Apply the custom plugin and script attribution solution across all supported Property Management Systems.
- [Leshan] Request API access: Inquire about API access for Property Management Systems such as Logify to enable integration with Hinge AI.

## Action needed

Sales and Retargeting campaigns first, then Lead Gen. Within each, Flag to Shawal before Review w/ HG AI, highest spend first.

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| Endless Stays | Nicole | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $1,068 / 14d | ROAS 3.0x | Review w/ HG AI | Still open, week 2 (was Flag to Shawal) |
| Paradise Pointe | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $719 / 14d | ROAS 3.6x | Review w/ HG AI | Still open, week 2 (was Flag to Shawal) |
| Ridge & Falls | Makenna | MoF - Lead Campaign - Retargeting Engagers - 09/01/26 | Lead Gen (MoF) | $188 / 30d | CPL $5.38 | Flag to Shawal | Still open, week 3 |
| Stay On 30A | Charlotte | MoF - Lead Campaign - RT Engagers - 07/16/26 | Lead Gen (MoF) | $1,506 / 30d | CPL $1.33 | Review w/ HG AI | Still open, week 4 |
| American River Resort | Nicole | MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | $603 / 30d | CPL $1.26 | Review w/ HG AI | Still open, week 4 |
| Green Springs Inn | Alicia | MoF - Lead Campaign/08/28/2026 | Lead Gen (MoF) | $304 / 30d | CPL $1.56 | Review w/ HG AI | Still open, week 4 |
| Sunapee Stays | Charlotte | MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | $303 / 30d | CPL $1.56 | Review w/ HG AI | Still open, week 3 |
| AwayFrames | Alicia | MoF - Lead Campaign - Retargeting Engagers 07/31/2026 | Lead Gen (MoF) | $151 / 30d | CPL $1.35 | Review w/ HG AI | Still open, week 4 |
| Bison Ridge Retreat | Chiara | MoF - Lead Campaign - RT Engagers | Lead Gen (MoF) | $151 / 30d | CPL $2.29 | Review w/ HG AI | New flag, was Under gate |
| Little River Landing | Makenna | MoF - Lead Campaign - Retargeting Engagers - 09/16/2026 | Lead Gen (MoF) | $146 / 30d | CPL $1.45 | Review w/ HG AI | Still open, week 2 |

## Scale candidates

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| Stay On 30A | Charlotte | BoF - Sales Campaign - RT Website Visitors - 07/13/26 | Retargeting (BoF) | $1,858 / 14d | ROAS 28.5x | Scale w/ HG AI | Unchanged |
| Starlight Haven Weiss Lake | Charlotte | Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | $627 / 14d | ROAS 27.0x | Scale w/ HG AI | Unchanged |
| Ponderosa Pines Resort | Anna | Website Retarget Campaign - 07/13/26 | Retargeting (BoF) | $552 / 14d | ROAS 15.0x | Scale w/ HG AI | Unchanged |
| Asheville River Cabins | Charlotte | BoF - Website Retargeting Campaign - 06/08/26 | Retargeting (BoF) | $281 / 14d | ROAS 60.5x | Scale w/ HG AI | New, not in the 5 Oct run |
| Starlight Haven Hot Springs | Charlotte | Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | $279 / 14d | ROAS 29.8x | Scale w/ HG AI | Unchanged |
| Selah Place | Alicia | BoF-Website Retarget Campaign - 07/24/2026 | Retargeting (BoF) | $270 / 14d | ROAS 19.3x | Scale w/ HG AI | Unchanged |
| Asheville River Cabins | Charlotte | MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | $256 / 30d | CPL $0.30 | Scale w/ HG AI | New, not in the 5 Oct run |

## Frequency watch (Sales / Retargeting above 5)

Sales, Retargeting and MoF-lookalike campaigns whose 14-day frequency is above 5.0 (Shawal, 6 Oct 2026). Frequency does not change the ROAS state; this is the list to refresh creative or widen the audience on. The diagnostics column still notes anything above 3.0.

| Client | AM | Campaign | Type | Frequency | Spend / window | Governing metric | State |
|---|---|---|---|---|---|---|---|
| Paradise Pointe | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 5.92 | $719 / 14d | ROAS 3.6x | Review w/ HG AI |

## Per client, ordered by scored MoF + BoF spend

### Stay On 30A — AM Charlotte — account Stay on 30a Ads (25640434272252212) — live read

ToF (Discovery / Keyword) spend, not scored: $2,991 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - RT Engagers - 07/16/26 | Lead Gen (MoF) | 30d | $1,506 | 1129 leads | CPL $1.33 | — | Review w/ HG AI | CPC $0.39 > $0.30; CPM $34.56 > $14.84 | 14d CPL $1.32 | Still open, week 4 |
| MoF - Sales Campaign - HiddenGem Pixel LoL - 07/17/26 | Sales (MoF lookalike) | 14d | $2,654 | 8 purchases | ROAS 8.3x | 1.98 | Healthy | CPC $1.00 > $0.62; CPM $25.64 > $16.50; cost/booking $331.80 > $90 | 30d ROAS 14.7x, 26 purchases | Was Scale w/ HG AI |
| BoF - Sales Campaign - RT Website Visitors - 07/13/26 | Retargeting (BoF) | 14d | $1,858 | 13 purchases | ROAS 28.5x | 4.47 | Scale w/ HG AI | CPC $1.64 > $0.62; CPM $28.38 > $16.50; cost/booking $142.96 > $90; freq 4.5 > 3.0 | 30d ROAS 28.8x, 30 purchases | Unchanged |

Monthly ROI: July: spend $6,407, 67 Meta-attributed bookings, blended ROAS 32.3x, retargeting ROAS 14.6x, CPL $1.24 on 583 leads · August: spend $12,420, 85 Meta-attributed bookings, blended ROAS 17.8x, retargeting ROAS 15.5x, CPL $2.58 on 594 leads · September: spend $12,606, 91 Meta-attributed bookings, blended ROAS 24.4x, retargeting ROAS 23.1x, CPL $1.52 on 1001 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Tàberg Falls — AM Alicia — account Táberg Falls (827872700004659) — live read

ToF (Discovery / Keyword) spend, not scored: $2,823 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Leads Campaign - 06/19/26 | Lead Gen (MoF) | 30d | $1,773 | 3190 leads | CPL $0.56 | — | Monitor | within lines | 14d CPL $0.56 | Unchanged |
| MoF - Broad (Acquire new customers) - 09/28/2026 | Sales (MoF lookalike) | 14d | $703 | 3 purchases | ROAS 6.2x | 1.62 | Monitor | CPM $23.06 > $16.50; cost/booking $234.17 > $90 | 30d ROAS 6.0x, 3 purchases | Unchanged |
| BoF - Website Retargeting Campaign - 08/21/2026 | Retargeting (BoF) | 14d | $1,316 | 7 purchases | ROAS 9.7x | 3.00 | Healthy | CPC $0.71 > $0.62; CPM $24.45 > $16.50; cost/booking $188.01 > $90 | 30d ROAS 7.7x, 14 purchases | Was Monitor |
| MoF - Lookalike Sales Campaign - 08/21/2026 | Sales (MoF lookalike) | 14d | $807 | 7 purchases | ROAS 13.9x | 1.42 | Healthy | CPM $20.46 > $16.50; cost/booking $115.24 > $90 | 30d ROAS 6.8x, 10 purchases | Unchanged |

Monthly ROI: July: spend $11,739, 80 Meta-attributed bookings, blended ROAS 9.5x, retargeting ROAS 15.8x, CPL $0.67 on 2320 leads · August: spend $11,259, 31 Meta-attributed bookings, blended ROAS 4.5x, retargeting ROAS 8.0x, CPL $0.46 on 4015 leads · September: spend $10,800, 27 Meta-attributed bookings, blended ROAS 4.0x, retargeting ROAS 7.1x, CPL $0.55 on 3261 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. Budgets were cut during the week (BoF $100 to $75, Giveaway $100 to $50, Leads $60 to $50, Lookalike up to $75); Broad stays at $50. The 14-day window straddles the change.

### FLOHOM — AM Makenna — account FLOHOM Ads (2100710320122219) — live read

ToF (Discovery / Keyword) spend, not scored: $641 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $1,256 | 11 purchases | ROAS 6.0x | 2.47 | Monitor | CPC $0.71 > $0.62; CPM $19.95 > $16.50; cost/booking $114.16 > $90 | 30d ROAS 8.1x, 27 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers – 08/17/26 | Lead Gen (MoF) | 30d | $763 | 1357 leads | CPL $0.56 | — | Monitor | within lines | 14d CPL $0.51 | Unchanged |
| MoF - Lookalike Sales Campaign - 07/29/26 | Sales (MoF lookalike) | 14d | $1,120 | 12 purchases | ROAS 9.8x | 2.19 | Healthy | CPC $0.79 > $0.62; CPM $23.46 > $16.50; cost/booking $93.29 > $90 | 30d ROAS 11.0x, 32 purchases | Unchanged |
| [Myrtle Beach] MoF - Lookalike Sales Campaign - 09/17/26 | Sales (MoF lookalike) | 14d | $278 | 3 purchases | ROAS 14.9x | 2.72 | Healthy | CPC $1.06 > $0.62; CPM $21.49 > $16.50; cost/booking $92.61 > $90 | 30d ROAS 9.7x, 5 purchases | Unchanged |

Monthly ROI: July: spend $5,555, 103 Meta-attributed bookings, blended ROAS 17.2x, retargeting ROAS 19.1x, CPL $7.66 on 66 leads · August: spend $9,331, 57 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 8.2x, CPL $2.24 on 708 leads · September: spend $8,855, 66 Meta-attributed bookings, blended ROAS 6.7x, retargeting ROAS 8.9x, CPL $0.50 on 2192 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Paradise Pointe — AM Makenna — account Paradise Pointe Ads (1585826092078255) — live read

ToF (Discovery / Keyword) spend, not scored: $753 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $719 | 13 purchases | ROAS 3.6x | 5.92 ⚠️ > 5 | Review w/ HG AI | CPC $0.96 > $0.62; freq 5.9 > 3.0 | 30d ROAS 4.5x, 33 purchases | Still open, week 2 (was Flag to Shawal) |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $753 | 798 leads | CPL $0.94 | — | Monitor | within lines | 14d CPL $0.93 | Unchanged |
| MoF - LoL Sales Campaign - 09/28/26 | Sales (MoF lookalike) | 14d | $713 | 23 purchases | ROAS 8.7x | 2.27 | Healthy | CPC $0.67 > $0.62 | 30d ROAS 8.5x, 23 purchases | Fixed, was Review w/ HG AI |

Monthly ROI: July: spend $2,237, 74 Meta-attributed bookings, blended ROAS 21.6x, retargeting ROAS 16.7x, CPL $1.01 on 90 leads · August: spend $3,109, 94 Meta-attributed bookings, blended ROAS 16.8x, retargeting ROAS 18.0x, CPL $1.64 on 471 leads · September: spend $3,074, 48 Meta-attributed bookings, blended ROAS 7.0x, retargeting ROAS 13.0x, CPL $0.97 on 764 leads. Note in the September file: Meta did not record revenue for 12 retargeting purchases (week of Sep 15–21 and Sep 29–30); their value was added manually at the average booking value (12 × $1,170.59 = $14,047.08) and the ROAS updated.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. Read live this week (API system user). September ROI file: Meta recorded no revenue for 12 retargeting purchases in late September; live purchase_roas now carries value again. Dustin's 1 Oct next step (disable low-performing ads, new variations into retargeting) is not yet checkable here.

### Endless Stays — AM Nicole — account Endless Stays (896372356081479) — live read

ToF (Discovery / Keyword) spend, not scored: $1,909 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $1,068 | 2 purchases | ROAS 3.0x | 2.50 | Review w/ HG AI | CPM $18.48 > $16.50; cost/booking $534.24 > $90 | 30d ROAS 3.1x, 3 purchases | Still open, week 2 (was Flag to Shawal) |
| MoF Lead Campaign - Retargeting Engagers - 09/09/2026 | Lead Gen (MoF) | 30d | $1,083 | 1253 leads | CPL $0.86 | — | Monitor | within lines | 14d CPL $0.78 | Unchanged |

Monthly ROI: July: spend $1,534, 9 Meta-attributed bookings, blended ROAS 16.0x · August: spend $1,553, 10 Meta-attributed bookings, blended ROAS 11.6x, retargeting ROAS 38.8x, CPL $9.73 on 26 leads · September: spend $2,539, 6 Meta-attributed bookings, blended ROAS 2.9x, retargeting ROAS 4.7x, CPL $1.05 on 532 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Treetop Escapes — AM Makenna — account Treetop Escapes Ads (967636478877602) — live read

ToF (Discovery / Keyword) spend, not scored: $903 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $906 | 1126 leads | CPL $0.80 | — | Monitor | CPM $16.58 > $14.84 | 14d CPL $0.81 | Unchanged |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $574 | 5 purchases | ROAS 8.9x | 3.45 | Healthy | CPM $19.37 > $16.50; cost/booking $114.82 > $90; freq 3.4 > 3.0 | 30d ROAS 7.7x, 9 purchases | Unchanged |

Monthly ROI: July: spend $2,487, 44 Meta-attributed bookings, blended ROAS 14.5x, retargeting ROAS 22.2x, CPL $1.48 on 21 leads · August: spend $3,082, 28 Meta-attributed bookings, blended ROAS 8.8x, retargeting ROAS 16.3x, CPL $1.49 on 620 leads · September: spend $2,998, 10 Meta-attributed bookings, blended ROAS 3.8x, retargeting ROAS 7.9x, CPL $0.88 on 1019 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Starlight Haven Weiss Lake — AM Charlotte — account Starlight Haven Weiss Lake (74756899) — live read

ToF (Discovery / Keyword) spend, not scored: $23 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $755 | 765 leads | CPL $0.99 | — | Monitor | CPC $0.32 > $0.30 | 14d CPL $0.97 | Unchanged |
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $627 | 24 purchases | ROAS 27.0x | 2.87 | Scale w/ HG AI | CPC $0.76 > $0.62; CPM $17.57 > $16.50 | 30d ROAS 26.3x, 62 purchases | Unchanged |

Monthly ROI: July: spend $2,163, 41 Meta-attributed bookings, blended ROAS 10.8x, retargeting ROAS 15.2x, CPL $0.74 on 826 leads · August: spend $2,351, 36 Meta-attributed bookings, blended ROAS 10.7x, retargeting ROAS 17.6x, CPL $1.23 on 617 leads · September: spend $2,152, 79 Meta-attributed bookings, blended ROAS 17.4x, retargeting ROAS 23.8x, CPL $1.01 on 734 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Starlight Haven Hot Springs — AM Charlotte — account Starlight Haven Hot Springs (901138032027913) — live read

ToF (Discovery / Keyword) spend, not scored: $731 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $908 | 2789 leads | CPL $0.33 | — | Healthy | within lines | 14d CPL $0.31 | Unchanged |
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $279 | 12 purchases | ROAS 29.8x | 2.05 | Scale w/ HG AI | within lines | 30d ROAS 26.4x, 20 purchases | Unchanged |

Monthly ROI: July: spend $2,160, 17 Meta-attributed bookings, blended ROAS 5.1x, retargeting ROAS 17.1x, CPL $0.33 on 2813 leads · August: spend $2,193, 19 Meta-attributed bookings, blended ROAS 6.3x, retargeting ROAS 22.3x, CPL $0.36 on 2589 leads · September: spend $2,155, 61 Meta-attributed bookings, blended ROAS 16.5x, retargeting ROAS 28.5x, CPL $0.34 on 2597 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Ponderosa Pines Resort — AM Anna — account Ponderosa Pines Resort (1058846326445255) — live read

ToF (Discovery / Keyword) spend, not scored: $1,295 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Leads Campaign - 07/16/26 | Lead Gen (MoF) | 30d | $599 | 761 leads | CPL $0.79 | — | Monitor | within lines | 14d CPL $0.80 | Unchanged |
| Website Retarget Campaign - 07/13/26 | Retargeting (BoF) | 14d | $552 | 14 purchases | ROAS 15.0x | 3.15 | Scale w/ HG AI | CPC $0.74 > $0.62; CPM $21.12 > $16.50; freq 3.1 > 3.0 | 30d ROAS 18.2x, 41 purchases | Unchanged |

Monthly ROI: July: spend $2,089, 17 Meta-attributed bookings, blended ROAS 3.6x, retargeting ROAS 22.3x, CPL $0.91 on 356 leads · August: spend $3,101, 103 Meta-attributed bookings, blended ROAS 15.0x, retargeting ROAS 21.3x, CPL $1.32 on 471 leads · September: spend $2,985, 119 Meta-attributed bookings, blended ROAS 17.9x, retargeting ROAS 21.6x, CPL $0.84 on 708 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Stay Saluda NC — AM Makenna — account Stay Saluda Ads (1863632561215857) — live read

ToF (Discovery / Keyword) spend, not scored: $900 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $602 | 636 leads | CPL $0.95 | — | Monitor | within lines | 14d CPL $0.95 | Unchanged |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $418 | 4 purchases | ROAS 5.7x | 4.98 | Monitor | CPC $0.74 > $0.62; CPM $18.54 > $16.50; cost/booking $104.62 > $90; freq 5.0 > 3.0 | 30d ROAS 4.9x, 8 purchases | Fixed, was Review w/ HG AI |

Monthly ROI: July: spend $2,140, 10 Meta-attributed bookings, blended ROAS 2.6x, retargeting ROAS 0.8x · August: spend $2,367, 9 Meta-attributed bookings, blended ROAS 3.7x, retargeting ROAS 5.2x, CPL $2.59 on 146 leads · September: spend $2,394, 6 Meta-attributed bookings, blended ROAS 1.3x, retargeting ROAS 3.5x, CPL $1.00 on 596 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### American River Resort — AM Nicole — account American River Resort (953162737054331) — live read

ToF (Discovery / Keyword) spend, not scored: $901 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $603 | 480 leads | CPL $1.26 | — | Review w/ HG AI | CPM $16.04 > $14.84 | 14d CPL $1.26 | Still open, week 4 |

Monthly ROI: July: spend $1,544, 4 Meta-attributed bookings, blended ROAS 1.1x · August: spend $1,529, 3 Meta-attributed bookings, blended ROAS 1.4x, CPL $18.30 on 30 leads · September: spend $1,453, 0 Meta-attributed bookings, blended ROAS —, CPL $1.48 on 377 leads. Note in the September file: We had no promo code usages this month.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Asheville River Cabins — AM Charlotte — account Asheville River Cabins Ads (615836588009747) — live read

ToF (Discovery / Keyword) spend, not scored: $1,026 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Website Retargeting Campaign - 06/08/26 | Retargeting (BoF) | 14d | $281 | 14 purchases | ROAS 60.5x | 1.94 | Scale w/ HG AI | CPM $19.78 > $16.50 | 30d ROAS 49.5x, 46 purchases | New, not in the 5 Oct run |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $256 | 856 leads | CPL $0.30 | — | Scale w/ HG AI | within lines | 14d CPL $0.33 | New, not in the 5 Oct run |

Monthly ROI: July: spend $2,029, 39 Meta-attributed bookings, blended ROAS 18.6x, retargeting ROAS 51.6x · August: spend $2,424, 82 Meta-attributed bookings, blended ROAS 27.2x, retargeting ROAS 65.0x, CPL $0.42 on 605 leads · September: spend $2,252, 70 Meta-attributed bookings, blended ROAS 19.1x, retargeting ROAS 42.5x, CPL $0.30 on 936 leads.

Meeting notes (Meta Ads Strategy 2026-10-07): Testing Attribution and Platform Compatibility Across Properties: Dustin Baker and Leshan Patterson discuss testing the new attribution methods on specific properties utilizing Cloudbeds, including Asheville River Cabins, Northstar, and Glass Homes.

HG AI notes: none dropped in since the previous run. Read live again (account ACTIVE, balance cleared). Delivery resumed about 6 Oct, so the 14-day window includes the dark week. 7 Oct meeting: Asheville is one of the Cloudbeds properties for the new attribution script test.

### Green Springs Inn — AM Alicia — account Green Springs Inn (1390516335151357) — live read

ToF (Discovery / Keyword) spend, not scored: $606 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign/08/28/2026 | Lead Gen (MoF) | 30d | $304 | 195 leads | CPL $1.56 | — | Review w/ HG AI | within lines | 14d CPL $1.48 | Still open, week 4 |
| BoF - Sales Campaign - Retargeting Website Visitors - 08/28/26 | Retargeting (BoF) | 14d | $141 | 5 purchases | ROAS 15.2x | 3.40 | Under gate | CPC $0.67 > $0.62; freq 3.4 > 3.0 | spend $140.88 < $200 gate; 30d ROAS 11.2x, 10 purchases | Unchanged |

Monthly ROI: July: spend $1,222, 17 Meta-attributed bookings, blended ROAS 7.8x, retargeting ROAS 14.6x, CPL $5.65 on 8 leads · August: spend $1,247, 23 Meta-attributed bookings, blended ROAS 8.2x, retargeting ROAS 17.1x, CPL $9.09 on 34 leads · September: spend $1,199, 24 Meta-attributed bookings, blended ROAS 8.5x, retargeting ROAS 9.0x, CPL $1.84 on 166 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Sunapee Stays — AM Charlotte — account Sunapee Stays Ads Account (651114096215889) — live read

ToF (Discovery / Keyword) spend, not scored: $906 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $303 | 194 leads | CPL $1.56 | — | Review w/ HG AI | CPM $15.60 > $14.84 | 14d CPL $1.48 | Still open, week 3 |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $137 | 4 purchases | ROAS 22.4x | 3.27 | Under gate | CPC $0.90 > $0.62; freq 3.3 > 3.0 | spend $137.08 < $200 gate; 30d ROAS 10.2x, 4 purchases | Unchanged |

Monthly ROI: July: spend $939, 16 Meta-attributed bookings, blended ROAS 9.9x, CPL $2.06 on 9 leads · August: spend $1,494, 10 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 25.1x, CPL $2.74 on 112 leads · September: spend $1,495, 14 Meta-attributed bookings, blended ROAS 6.5x, retargeting ROAS 6.7x, CPL $1.64 on 184 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Selah Place — AM Alicia — account Selah.place (1275283434220508) — live read

ToF (Discovery / Keyword) spend, not scored: $670 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $152 | 269 leads | CPL $0.56 | — | Monitor | within lines | 14d CPL $0.56 | Unchanged |
| BoF-Website Retarget Campaign - 07/24/2026 | Retargeting (BoF) | 14d | $270 | 11 purchases | ROAS 19.3x | 3.90 | Scale w/ HG AI | CPM $17.81 > $16.50; freq 3.9 > 3.0 | 30d ROAS 23.5x, 19 purchases | Unchanged |

Paused in window, not scored: SP / Prospecting Test / LAL + Interests x Creative / 09-2026 (Sales), $35 / 14d, 0 purchases, ROAS —. Live campaigns only are scored (decision 2026-09-23).

Monthly ROI: July: spend $1,054, 4 Meta-attributed bookings, blended ROAS 3.2x, retargeting ROAS 86.3x, CPL $0.80 on 49 leads · August: spend $1,545, 15 Meta-attributed bookings, blended ROAS 4.8x, retargeting ROAS 25.1x, CPL $1.08 on 144 leads · September: spend $1,304, 27 Meta-attributed bookings, blended ROAS 10.4x, retargeting ROAS 38.2x, CPL $0.63 on 232 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. Actions log: the BoF retargeting budget was raised from $15 to $35 this week (the planned move of the paused test's budget, now Done); the 14-day window still mostly reflects the $15 level.

### Ridge & Falls — AM Makenna — account Ridge & Falls ad account (1313401330776046) — live read

ToF (Discovery / Keyword) spend, not scored: $1,410 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers - 09/01/26 | Lead Gen (MoF) | 30d | $188 | 35 leads | CPL $5.38 | — | Flag to Shawal | CPC $0.33 > $0.30; CPM $17.63 > $14.84 | 14d CPL $3.02 | Still open, week 3 |
| BoF - Sales Campaign - Retargeting Website Visitors - 09/01/26 | Retargeting (BoF) | 14d | $71 | 3 purchases | ROAS 15.2x | 3.74 | Under gate | freq 3.7 > 3.0 | spend $70.52 < $200 gate; 30d ROAS 7.1x, 3 purchases | Unchanged |

Monthly ROI: September: spend $1,036, 0 Meta-attributed bookings, blended ROAS —, retargeting ROAS —, CPL $8.16 on 16 leads. Note in the September file: Newly launched campaigns — $1,036.47 spent, no revenue from ads yet (spend exceeds the $871.49 September direct revenue, as expected for a launch month).

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. Actions log: the lead-campaign relaunch with a fixed conversion event (planned 28 Sep) has still not happened; the 09/01 campaign is the live one.

### Bison Ridge Retreat — AM Chiara — account Bison Ridge Retreat Ad Account (950241787963535) — live read

ToF (Discovery / Keyword) spend, not scored: $599 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - RT Engagers | Lead Gen (MoF) | 30d | $151 | 66 leads | CPL $2.29 | — | Review w/ HG AI | CPC $0.36 > $0.30 | 14d CPL $2.12 | New flag, was Under gate |
| BoF - Sales Campaign - RT Website Visitors | Retargeting (BoF) | 14d | $74 | 0 purchases | ROAS — | 1.97 | Under gate | CPC $0.66 > $0.62 | spend $74.32 < $200 gate | Unchanged |

Monthly ROI: July: spend $924, 9 Meta-attributed bookings, blended ROAS 20.3x, retargeting ROAS —, CPL $1.75 on 23 leads · August: spend $952, 3 Meta-attributed bookings, blended ROAS 8.0x, retargeting ROAS —, CPL $2.47 on 63 leads · September: spend $893, 5 Meta-attributed bookings, blended ROAS 9.3x, retargeting ROAS —, CPL $2.54 on 59 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### AwayFrames — AM Alicia — account Awayframes Ad Account (2471256056603833) — live read

ToF (Discovery / Keyword) spend, not scored: $599 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers 07/31/2026 | Lead Gen (MoF) | 30d | $151 | 112 leads | CPL $1.35 | — | Review w/ HG AI | within lines | 14d CPL $1.03 | Still open, week 4 |
| BoF - Sales Campaign - Retargeting Website Visitors 07/31/2026 | Retargeting (BoF) | 14d | $72 | 1 purchases | ROAS 9.1x | 2.51 | Under gate | CPC $0.64 > $0.62 | spend $71.53 < $200 gate; 30d ROAS 9.1x, 2 purchases | Unchanged |

Monthly ROI: July: spend $923, 9 Meta-attributed bookings, blended ROAS 18.6x, CPL $2.44 on 2 leads · August: spend $869, 8 Meta-attributed bookings, blended ROAS 21.8x, retargeting ROAS 27.0x, CPL $2.68 on 58 leads · September: spend $895, 7 Meta-attributed bookings, blended ROAS 11.1x, retargeting ROAS 4.9x, CPL $1.83 on 82 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Walden Retreats — AM Anna — account Walden Retreats (973261794434226) — live read

ToF (Discovery / Keyword) spend, not scored: $81 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers - 10/06/2026 | Lead Gen (MoF) | 30d | $67 | 59 leads | CPL $1.14 | — | Under gate | CPC $0.37 > $0.30; CPM $17.09 > $14.84 | spend $67.47 < $100 gate; 14d CPL $1.14 | New, not in the 5 Oct run |
| TOF Wedding Leads 10.8.26 | Lead Gen (MoF) | 30d | $64 | 8 leads | CPL $8.02 | — | Under gate | CPM $21.61 > $14.84 | spend $64.17 < $100 gate; 14d CPL $8.02 | New, not in the 5 Oct run |
| BoF - Sales Campaign - Retargeting Website Visitors - 06/10/2026 | Retargeting (BoF) | 14d | $61 | 4 purchases | ROAS 36.3x | 1.56 | Under gate | CPC $0.69 > $0.62; CPM $18.52 > $16.50 | spend $60.81 < $200 gate; 30d ROAS 36.3x, 4 purchases | New, not in the 5 Oct run |
| TOF Wedding Leads (alt aud) 10.9.26 | Lead Gen (MoF) | 30d | $27 | 0 leads | CPL — | — | Under gate | CPC $1.50 > $0.30; CPM $28.27 > $14.84 | spend $26.94 < $100 gate | New, not in the 5 Oct run |

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. New in scope: ad account 973261794434226 appeared on the Master sheet this week. Campaigns launched 6 to 9 Oct, so every row is on a few days of data.

### Little River Landing — AM Makenna — account Little River Landing (884285717873613) — live read

ToF (Discovery / Keyword) spend, not scored: $1,433 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers - 09/16/2026 | Lead Gen (MoF) | 30d | $146 | 101 leads | CPL $1.45 | — | Review w/ HG AI | CPC $0.37 > $0.30; CPM $18.92 > $14.84 | 14d CPL $1.22 | Still open, week 2 |
| BoF - Sales Campaign - Retargeting Website Visitors - 09/16/2026 | Retargeting (BoF) | 14d | $70 | 0 purchases | ROAS — | 3.11 | Under gate | freq 3.1 > 3.0 | spend $70.21 < $200 gate | Unchanged |

Monthly ROI: September: spend $921, 0 Meta-attributed bookings, blended ROAS —, retargeting ROAS —, CPL $1.86 on 46 leads. Note in the September file: Newly launched campaigns — $921.36 spent, no revenue from ads yet.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### The Outpost — AM Anna — account The Outpost Grand Canyon (1530849534802936) — live read

ToF (Discovery / Keyword) spend, not scored: $902 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 08/29/2026 | Retargeting (BoF) | 14d | $97 | 0 purchases | ROAS — | 2.00 | Under gate | CPC $0.66 > $0.62 | spend $96.69 < $200 gate | Unchanged |
| BoF - Sales Campaign - Retargeting Website Visitors - 10/08/2026 | Retargeting (BoF) | 14d | $44 | 0 purchases | ROAS — | 1.51 | Under gate | within lines | spend $44.29 < $200 gate | New, not in the 5 Oct run |

Monthly ROI: July: spend $2,182, 1 Meta-attributed bookings, blended ROAS 0.2x, CPL $1.61 on 202 leads · August: spend $1,876, 7 Meta-attributed bookings, blended ROAS 2.1x, CPL $1.71 on 181 leads · September: spend $2,081, 18 Meta-attributed bookings, blended ROAS 3.8x, retargeting ROAS —, CPL $1.80 on 167 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. A second BoF campaign (dated 10/..) runs beside the 08/29 one this week; both are scored if over the gate.

### North Star Lodge & Resort — AM Charlotte — account North Star Lodge & Resort Ads (2003562593933799) — live read

ToF (Discovery / Keyword) spend, not scored: $787 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 09/09/2026 | Retargeting (BoF) | 14d | $64 | 0 purchases | ROAS — | 3.28 | Under gate | CPC $0.90 > $0.62; freq 3.3 > 3.0 | spend $64.02 < $200 gate | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 10/02/26 | Lead Gen (MoF) | 30d | $41 | 0 leads | CPL — | — | Under gate | CPC $0.91 > $0.30; CPM $25.67 > $14.84 | spend $40.74 < $100 gate | New, not in the 5 Oct run |

Monthly ROI: September: spend $580, 0 Meta-attributed bookings, blended ROAS —. Note in the September file: Newly launched campaigns — $579.92 spent, no revenue from ads yet. Revenue shown is from the client reporting sheet; no booking-level data this month.

Meeting notes (Meta Ads Strategy 2026-10-07): Testing Attribution and Platform Compatibility Across Properties: Dustin Baker and Leshan Patterson discuss testing the new attribution methods on specific properties utilizing Cloudbeds, including Asheville River Cabins, Northstar, and Glass Homes.

HG AI notes: none dropped in since the previous run. 7 Oct meeting: North Star is one of the Cloudbeds properties for the new attribution script test (Leshan).

## Footer

- Windows: Lead Gen last 30 days, Sales/Retargeting last 14 days (live). CSV accounts use the export period 2026-10-05 to 2026-10-11 (7 days) and are provisional.
- Gates: $100 Lead Gen, $200 Sales/Retargeting. Campaigns under the gate are listed but not judged.
- Classification: by campaign objective (OUTCOME_LEADS → Lead Gen; OUTCOME_SALES → Sales, split into Retargeting (BoF) or MoF lookalike by name; OUTCOME_TRAFFIC / OUTCOME_ENGAGEMENT → ToF, not scored). CSV accounts have no objective column, so classification there is by name.
- Sales campaigns with an MoF or lookalike prefix are scored on the Retargeting ROAS bands because they optimise for purchases. The Benchmarks doc has no separate band for prospecting sales campaigns; confirm or add one.
- Data path this week: Marketing API v21.0 insights at campaign level (purchases = omni_purchase, leads = lead, ROAS = purchase_roas, link clicks = inline_link_clicks), same fields the connector exposes.
- CTR on live rows is Meta's CTR (all clicks), not link CTR. The doc's click-rate lines are probably link CTR, so treat the CTR diagnostic as indicative.
- Frequency and cost per booking are diagnostics only and do not change the state (decision 2026-09-21). From 2026-10-06 (Shawal) every Sales / Retargeting row shows its frequency, and any value above 5.0 is marked ⚠️ in that column and listed in the Frequency watch section; CSV rows use impressions / reach summed over ad sets, which overstates frequency where ad sets overlap.
- Only campaigns live (ACTIVE) at run time are scored. Paused campaigns that spent inside the window are listed per client as "Paused in window" and never enter Action needed or the counts (decision 2026-09-23).
- Unclassified campaigns: none.
- Previous report: 2026-10-05-client-benchmark.csv. Diff joined on campaign_id for live rows and client + campaign name for CSV rows. Diff counts: 9 new, 9 still open, 2 fixed, 31 unchanged, 0 removed.
- Scope changes vs 5 Oct: Walden Retreats added (account 973261794434226 now on the Master sheet); Bison Ridge, Endless Stays, Paradise Pointe, Ponderosa and Asheville move from CSV to live reads. Advanced in the CRM but with no ad account mapping in PROJECT.md section 5, not scored: Treetop Hideaways (AM Kristal), Glasscombe (AM Charlotte), Cabin Collective (AM Chiara), Casey Key Resort (AM Alicia), Arca Roatan (AM Anna).
- HG AI reports read from `HG AI Reports/` at the project root, dated since the previous run: none.
- Selah Place's prospecting campaign (paused this week) is named with pipes in Meta ("SP | Prospecting Test | LAL + Interests x Creative | 09-2026"); shown here with slashes.
- Meeting notes: every "Meta Ads Strategy", "Meta Ads Sync" or "Meta Ads x HiddenGem AI Sync" calendar event since the previous run that has a "Notes by Gemini" attachment, read via Drive. Client names are matched with an alias list (Flow Home = FLOHOM, Tabber / Tipik Falls / Debug Falls = Tàberg Falls, Sailor Place = Selah Place, Stay on 38 = Stay On 30A, Ashwood River Cabins = Asheville River Cabins).
- Monthly ROI context from `Monthly ROI data/` (July 2026, August 2026, September 2026). Revenue there comes from the Client Performance Tracking sheet, not the pixel, so its ROAS is not comparable to the pixel ROAS above.
