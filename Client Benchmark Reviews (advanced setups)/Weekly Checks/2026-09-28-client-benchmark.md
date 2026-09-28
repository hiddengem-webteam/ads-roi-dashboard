# Client Benchmark Review (advanced setups) — 2026-09-28

Run: 28 September 2026, second run, compared against 2026-09-21-client-benchmark.csv. Live reads via the Meta connector; CSV export 2026-09-21 to 2026-09-27 for the 4 accounts the connector cannot read. Scope: clients marked **Advanced** in the CRM "Meta Ads" column (Clients - Onboarding tab), re-read today: 24 clients, 21 with an ad account. Six clients are in scope for the first time (The Outpost, Selah Place, Sunapee Stays, Ridge & Falls, Little River Landing, North Star Lodge & Resort) and Canopy at Moody Moon has dropped out (CRM now says Basic). Only Lead Gen (MoF) and Sales/Retargeting (BoF) campaigns are scored; IG Discovery and Keyword (ToF) spend is shown for context only.

| Advanced clients | Live reads | From CSV | Campaigns scored | Under spend gate | Flag to Shawal | Review w/ HG AI | Monitor | Healthy | Scale w/ HG AI |
|---|---|---|---|---|---|---|---|---|---|
| 21 (+3 unmapped) | 17 | 4 | 33 | 10 | 2 | 11 | 9 | 6 | 5 |

States come from the Decision Making table in the Benchmarks doc. Lead Gen: CPL under $0.30 Scale, $0.30–0.50 Healthy, $0.50–1.00 Monitor, $1.00–2.50 Review, $2.50+ Flag, 30-day window, $100 gate. Sales/Retargeting: ROAS above 15x Scale, 8–15x Healthy, 5–8x Monitor, 2–5x Review, under 2x Flag, 14-day window, $200 gate. Band edges are inclusive on the lower bound.

## Weekly Meta Ads meetings since last run (Notes by Gemini)

Source: "Notes by Gemini" docs attached to the calendar events, read via Drive. Summary, decisions and next steps as Gemini wrote them; client-specific sentences are pulled into each client's section below. Transcript not used.

### Meta Ads Strategy — 2026-09-23 — doc `1fs5ztTn1bKVuGo0lltwTASgoAeP0hTkJFuG2ykyK42U`

Gemini produced no notes for this call ("not enough conversation in a supported language"); only a 32-minute transcript exists, which this report does not use.

### Meta Ads x HiddenGem AI Sync (12:03 ET) — 2026-09-24 — doc `1dpv2D1nk5cDoHxTAn7yP0Ff7wheeZJ457OHZVLlrNNI`

Meta ads strategy and creative diversification via Andromeda update and campaign consolidation

Meta Ads And Andromeda

Andromeda retrieval system prioritizes creative diversification and massive ad volume over traditional interest targeting. Evaluating performance at adset level prevents premature removal of sequencing assets.

Campaign Structure And Settings

Consolidating campaigns into 1 adset optimizes signal distribution for lower budgets. Keeping Advantage+ audience enabled while disabling unwanted text generation maintains control.

IT Transition And Security

Moving from GoDaddy to a private IT company is approved provided specialists receive existing DNS records to avoid conflicts. Incorporating optimized images into website designs proceeds using shared links.

Decisions:
- Consolidating ad accounts into single ad sets The team aligned on structuring ad campaigns with a single campaign, a single ad set, and a large volume of ads to consolidate event signals.
- Disabling advantage plus placements on ads The team decided to disable advantage plus placements so they do not test unwanted placements like the audience network.
- Disabling advantage plus creative text generation The team aligned on turning off advantage plus creative text generation because the automated text modifications make minimal performance differences.
- Treating legacy tier two clients differently The team aligned on treating tier two legacy clients differently by maintaining simpler, set-and-forget ad strategies with minimal maintenance.

Next steps:
- [Gillian Conley] Share Article: Locate the document regarding creative sequencing and purchase probability to include it in the description.
- [Gillian Conley] Schedule Meeting: Schedule a 30 minute review meeting to discuss and finalize the new ad performance review process.
- [Gillian Conley] Sync Creative Process: Sync with Ananya and Kristal to determine the technical feasibility of the new creative content adaptation strategies.
- [Chiara Henry] Share DNS Records: Provide the GoHighLevel DNS records and subdomain details to the client IT specialist via a screenshot.
- [Chiara Henry] Confirm Image Usage: Notify the client that they are permitted to use the optimized marketing images on their website.

### Meta Ads x HiddenGem AI Sync (13:33 ET) — 2026-09-24 — doc `11gWAmc-R6mCIXj3AlG7j_zLyW583SHloC0JPxJCNud0`

Client evaluation and office expansion and AI ad diagnostics discussion

Client Departure Evaluation

Client departure highlighted launch boom campaign limitations. Traditional financing remains preferable.

Office Expansion Plans

Adjacent office downsizing allowed extra square footage acquisition. Garage bays will become a lounge and gym.

Meta Ads Management

Tiered system for managing Meta ads established. HiddenGem AI tool adopted for ad diagnostics.

Decisions:
- Office space expansion and gym setup The team agreed to take on extra square footage to create a large hangout area and a company gym in the garage bays.
- Monthly cadence for ad performance reviews The team established a monthly cadence consisting of end-of-month budget reviews and mid-month creative refreshes.
- Approval workflow for ad adjustments Account managers will initially coordinate ad budget and creative adjustments with Shawal and Dustin before gaining full autonomy.
- Winter content transition for northern clients The team established a best practice to turn off summer ad creatives and switch to winter content for northern clients.

Next steps:
- [Dustin Baker] Meet with Lan: Discuss the creation of a copy-paste prompt versus system-integrated prompts for ad reporting analysis.
- [The group] Update calendar: Schedule the new monthly ad reporting cadence to ensure consistent performance monitoring.
- [Dustin Baker] Share diagram: Distribute the diagram illustrating the ad deconstruction and analysis process to the team.
- [Shawal] Monitor ad metrics: Review ad KPIs every week to flag performance discrepancies and potential issues.
- [Account managers] Consult managers: Verify creative or budget changes with Shal and Dustin before implementation.
- [The group] Implement winter content: Add winter content to the pipeline for all Tier 01 clients if not already present.
- [The group] Switch seasonal ads: Pause summer advertisement campaigns for northern clients and transition to winter assets.
- [Dustin Baker] Test winter ads: Execute A/B tests in select advertisement accounts to compare summer and winter campaign performance.
- [Gillian Conley] Update intake process: Define location-specific snow requirements in the content intake process for Artificial Intelligence generation.
- [Dustin Baker] Create regional map: Display an office map categorizing client regions by winter weather characteristics.

## Action needed

Sales and Retargeting campaigns first, then Lead Gen. Within each, Flag to Shawal before Review w/ HG AI, highest spend first.

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| Selah Place | Alicia | SP - Prospecting Test - LAL + Interests x Creative - 09-2026 | Sales | $387 / 14d | ROAS 1.3x | Flag to Shawal | New, not in the 21 Sep run |
| Tàberg Falls | Alicia | MoF - Lookalike Sales Campaign - 08/21/2026 | Sales (MoF lookalike) | $1,392 / 14d | ROAS 3.8x | Review w/ HG AI | Still open, week 2 |
| Treetop Escapes | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $542 / 14d | ROAS 4.7x | Review w/ HG AI | New flag, was Healthy |
| Stay Saluda NC | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $412 / 14d | ROAS 2.6x | Review w/ HG AI | Still open, week 2 |
| Ridge & Falls | Makenna | MoF - Lead Campaign - Retargeting Engagers - 09/01/26 | Lead Gen (MoF) | $112 / 30d | CPL $9.35 | Flag to Shawal | New, not in the 21 Sep run |
| Stay On 30A | Charlotte | MoF - Lead Campaign - RT Engagers - 07/16/26 | Lead Gen (MoF) | $1,489 / 30d | CPL $1.69 | Review w/ HG AI | Still open, week 2 |
| Starlight Haven Weiss Lake | Charlotte | New Leads Campaign - 03/03/26 | Lead Gen (MoF) | $747 / 30d | CPL $1.13 | Review w/ HG AI | Still open, week 2 |
| Stay Saluda NC | Makenna | MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | $596 / 30d | CPL $1.04 | Review w/ HG AI | Still open, week 2 |
| American River Resort | Nicole | MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | $441 / 30d | CPL $1.36 | Review w/ HG AI | Still open, week 2 |
| Green Springs Inn | Alicia | MoF - Lead Campaign/08/28/2026 | Lead Gen (MoF) | $301 / 30d | CPL $2.08 | Review w/ HG AI | Still open, week 2 |
| Sunapee Stays | Charlotte | MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | $299 / 30d | CPL $1.92 | Review w/ HG AI | New, not in the 21 Sep run |
| Endless Stays | Nicole | MoF Lead Campaign - Retargeting Engagers - 09/09/2026 | Lead Gen (MoF) | $251 / 7d | CPL $1.06 | Review w/ HG AI | Still open, week 2 |
| AwayFrames | Alicia | MoF - Lead Campaign - Retargeting Engagers 07/31/2026 | Lead Gen (MoF) | $149 / 30d | CPL $2.04 | Review w/ HG AI | Still open, week 2 |

## Scale candidates

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| Stay On 30A | Charlotte | MoF - Sales Campaign - HiddenGem Pixel LoL - 07/17/26 | Sales (MoF lookalike) | $2,377 / 14d | ROAS 20.8x | Scale w/ HG AI | Unchanged |
| Stay On 30A | Charlotte | BoF - Sales Campaign - RT Website Visitors - 07/13/26 | Retargeting (BoF) | $1,586 / 14d | ROAS 32.1x | Scale w/ HG AI | Unchanged |
| Starlight Haven Weiss Lake | Charlotte | Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | $620 / 14d | ROAS 28.0x | Scale w/ HG AI | Unchanged |
| Asheville River Cabins | Charlotte | BoF - Website Retargeting Campaign - 06/08/26 | Retargeting (BoF) | $415 / 14d | ROAS 43.1x | Scale w/ HG AI | Unchanged |
| Starlight Haven Hot Springs | Charlotte | Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | $276 / 14d | ROAS 24.4x | Scale w/ HG AI | Unchanged |

## Per client, ordered by scored MoF + BoF spend

### Stay On 30A — AM Charlotte — account Stay on 30a Ads (25640434272252212) — live read

ToF (Discovery / Keyword) spend, not scored: $2,992 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - RT Engagers - 07/16/26 | Lead Gen (MoF) | 30d | $1,489 | 879 leads | CPL $1.69 | Review w/ HG AI | CPC $0.42 > $0.30; CPM $36.41 > $14.84 | 14d CPL $1.42 | Still open, week 2 |
| MoF - Sales Campaign - HiddenGem Pixel LoL - 07/17/26 | Sales (MoF lookalike) | 14d | $2,377 | 14 purchases | ROAS 20.8x | Scale w/ HG AI | CPC $0.89 > $0.62; CPM $28.89 > $16.50; cost/booking $169.76 > $90 | 30d ROAS 21.5x, 30 purchases | Unchanged |
| BoF - Sales Campaign - RT Website Visitors - 07/13/26 | Retargeting (BoF) | 14d | $1,586 | 16 purchases | ROAS 32.1x | Scale w/ HG AI | CPC $1.30 > $0.62; CPM $32.09 > $16.50; cost/booking $99.10 > $90; freq 4.5 > 3.0 | 30d ROAS 24.9x, 23 purchases | Unchanged |

Monthly ROI: August: spend $12,420, 85 Meta-attributed bookings, blended ROAS 17.8x, retargeting ROAS 15.5x, CPL $2.58 on 594 leads · July: spend $6,407, 67 Meta-attributed bookings, blended ROAS 32.3x, retargeting ROAS 14.6x, CPL $1.24 on 583 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Tàberg Falls — AM Alicia — account Táberg Falls (827872700004659) — live read

ToF (Discovery / Keyword) spend, not scored: $2,997 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lookalike Sales Campaign - 08/21/2026 | Sales (MoF lookalike) | 14d | $1,392 | 3 purchases | ROAS 3.8x | Review w/ HG AI | CPM $30.14 > $16.50; cost/booking $463.89 > $90 | 30d ROAS 5.4x, 9 purchases | Still open, week 2 |
| MoF - Leads Campaign - 06/19/26 | Lead Gen (MoF) | 30d | $1,799 | 3310 leads | CPL $0.54 | Monitor | within lines | 14d CPL $0.55 | Unchanged |
| BoF - Website Retargeting Campaign - 08/21/2026 | Retargeting (BoF) | 14d | $1,385 | 7 purchases | ROAS 7.2x | Monitor | CPC $0.73 > $0.62; CPM $24.18 > $16.50; cost/booking $197.86 > $90; freq 3.3 > 3.0 | 30d ROAS 8.1x, 16 purchases | Fixed, was Review w/ HG AI |

Monthly ROI: August: spend $11,259, 31 Meta-attributed bookings, blended ROAS 4.5x, retargeting ROAS 8.0x, CPL $0.46 on 4015 leads · July: spend $11,739, 80 Meta-attributed bookings, blended ROAS 9.5x, retargeting ROAS 15.8x, CPL $0.67 on 2320 leads.

Meeting notes (Meta Ads x HiddenGem AI Sync (13:33 ET) 2026-09-24): Utilizing HiddenGem AI for Ad Diagnostics: Dustin Baker explained that when ad performance drops trigger an alert (such as Tabberg Falls' lookalike campaign return on ad spend falling to 3.3x), the team uses the HiddenGem AI tool powered by Claude to diagnose the root cause and generate actionable levers, such as adjusting budgets or refreshing ad creatives.

HG AI notes (23 Sep): hold off moving $50/day from the lookalike into retargeting and the giveaway. Both sales campaigns fell together in the last 15 days on flat spend (retargeting 11.2x to 3.7x, lookalike 4.8x to 3.2x), so the cause is shared (creative age, checkout, offer or tracking), not the lookalike. Check retargeting frequency and creative age first; if moving money now, trim the lookalike 20% into the giveaway and leave retargeting alone. Weekend nights to 18 Dec are 46% booked, December weekends 8%.

### FLOHOM — AM Makenna — account FLOHOM Ads (2100710320122219) — live read

ToF (Discovery / Keyword) spend, not scored: $1,713 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers – 08/17/26 | Lead Gen (MoF) | 30d | $1,180 | 2365 leads | CPL $0.50 | Monitor | within lines | 14d CPL $0.62 | Unchanged |
| [Myrtle Beach] MoF - Lookalike Sales Campaign - 09/17/26 | Sales (MoF lookalike) | 14d | $303 | 2 purchases | ROAS 5.6x | Monitor | CPC $1.64 > $0.62; CPM $23.91 > $16.50; cost/booking $151.50 > $90 | 30d ROAS 5.6x, 2 purchases | Was Under gate |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $1,340 | 16 purchases | ROAS 11.4x | Healthy | CPM $17.88 > $16.50 | 30d ROAS 9.0x, 30 purchases | Unchanged |
| MoF - Lookalike Sales Campaign - 07/29/26 | Sales (MoF lookalike) | 14d | $1,318 | 17 purchases | ROAS 11.0x | Healthy | CPC $0.69 > $0.62; CPM $19.48 > $16.50 | 30d ROAS 8.4x, 28 purchases | Unchanged |

Monthly ROI: August: spend $9,331, 57 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 8.2x, CPL $2.24 on 708 leads · July: spend $5,555, 103 Meta-attributed bookings, blended ROAS 17.2x, retargeting ROAS 19.1x, CPL $7.66 on 66 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Treetop Escapes — AM Makenna — account Treetop Escapes Ads (967636478877602) — live read

ToF (Discovery / Keyword) spend, not scored: $900 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $542 | 3 purchases | ROAS 4.7x | Review w/ HG AI | CPM $18.81 > $16.50; cost/booking $180.57 > $90; freq 3.3 > 3.0 | 30d ROAS 9.0x, 11 purchases | New flag, was Healthy |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $898 | 956 leads | CPL $0.94 | Monitor | within lines | 14d CPL $0.83 | Fixed, was Review w/ HG AI |

Monthly ROI: August: spend $3,082, 28 Meta-attributed bookings, blended ROAS 8.8x, retargeting ROAS 16.3x, CPL $1.49 on 620 leads · July: spend $2,487, 44 Meta-attributed bookings, blended ROAS 14.5x, retargeting ROAS 22.2x, CPL $1.48 on 21 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Starlight Haven Weiss Lake — AM Charlotte — account Starlight Haven Weiss Lake (74756899) — live read

ToF (Discovery / Keyword) spend, not scored: $98 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $747 | 662 leads | CPL $1.13 | Review w/ HG AI | CPC $0.31 > $0.30 | 14d CPL $1.00 | Still open, week 2 |
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $620 | 36 purchases | ROAS 28.0x | Scale w/ HG AI | CPC $0.72 > $0.62; CPM $18.76 > $16.50 | 30d ROAS 23.1x, 63 purchases | Unchanged |

Monthly ROI: August: spend $2,351, 36 Meta-attributed bookings, blended ROAS 10.7x, retargeting ROAS 17.6x, CPL $1.23 on 617 leads · July: spend $2,163, 41 Meta-attributed bookings, blended ROAS 10.8x, retargeting ROAS 15.2x, CPL $0.74 on 826 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Starlight Haven Hot Springs — AM Charlotte — account Starlight Haven Hot Springs (901138032027913) — live read

ToF (Discovery / Keyword) spend, not scored: $658 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $898 | 2607 leads | CPL $0.34 | Healthy | within lines | 14d CPL $0.33 | Unchanged |
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $276 | 7 purchases | ROAS 24.4x | Scale w/ HG AI | within lines | 30d ROAS 23.0x, 18 purchases | Unchanged |

Monthly ROI: August: spend $2,193, 19 Meta-attributed bookings, blended ROAS 6.3x, retargeting ROAS 22.3x, CPL $0.36 on 2589 leads · July: spend $2,160, 17 Meta-attributed bookings, blended ROAS 5.1x, retargeting ROAS 17.1x, CPL $0.33 on 2813 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Stay Saluda NC — AM Makenna — account Stay Saluda Ads (1863632561215857) — live read

ToF (Discovery / Keyword) spend, not scored: $896 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $596 | 570 leads | CPL $1.04 | Review w/ HG AI | within lines | 14d CPL $0.92 | Still open, week 2 |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $412 | 2 purchases | ROAS 2.6x | Review w/ HG AI | CPC $0.85 > $0.62; CPM $16.58 > $16.50; cost/booking $206.23 > $90; freq 4.5 > 3.0 | 30d ROAS 4.2x, 7 purchases | Still open, week 2 |

Monthly ROI: August: spend $2,367, 9 Meta-attributed bookings, blended ROAS 3.7x, retargeting ROAS 5.2x, CPL $2.59 on 146 leads · July: spend $2,140, 10 Meta-attributed bookings, blended ROAS 2.6x, retargeting ROAS 0.8x.

Meeting notes: not mentioned in this week's meetings.

HG AI notes (23 Sep): account ROAS 1.71x to 2.12x on the mix change, but BoF retargeting weakened in the second half of the month (6.07x to 2.40x, CTR down 14%) on flat spend. ToF was already scaled to about $25/day on 18 to 22 Sep, so fix the retargeting pool first (4 to 6 fresh review-led ads, add IG/FB engagers and the GHL list), keep ToF steps at 20% or less, and point creative at the open calendar (next 30 days 47% occupied). (file: 2026-09-23 Stay Saluda - HG AI.md)

### Asheville River Cabins — AM Charlotte — account Asheville River Cabins Ads (615836588009747) — live read

ToF (Discovery / Keyword) spend, not scored: $1,205 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $300 | 966 leads | CPL $0.31 | Healthy | within lines | 14d CPL $0.29 | Unchanged |
| BoF - Website Retargeting Campaign - 06/08/26 | Retargeting (BoF) | 14d | $415 | 28 purchases | ROAS 43.1x | Scale w/ HG AI | CPM $20.10 > $16.50 | 30d ROAS 41.9x, 60 purchases | Unchanged |

Monthly ROI: August: spend $2,424, 82 Meta-attributed bookings, blended ROAS 27.2x, retargeting ROAS 65.0x, CPL $0.42 on 605 leads · July: spend $2,029, 39 Meta-attributed bookings, blended ROAS 18.6x, retargeting ROAS 51.6x.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Selah Place — AM Alicia — account Selah.place (1275283434220508) — live read

ToF (Discovery / Keyword) spend, not scored: $1,014 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| SP - Prospecting Test - LAL + Interests x Creative - 09-2026 | Sales | 14d | $387 | 1 purchases | ROAS 1.3x | Flag to Shawal | CPM $17.16 > $16.50; cost/booking $387.03 > $90 | 30d ROAS 1.3x, 1 purchases | New, not in the 21 Sep run |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $145 | 223 leads | CPL $0.65 | Monitor | within lines | 14d CPL $0.59 | New, not in the 21 Sep run |
| BoF-Website Retarget Campaign - 07/24/2026 | Retargeting (BoF) | 14d | $132 | 7 purchases | ROAS 31.1x | Under gate | CPM $17.35 > $16.50; freq 3.1 > 3.0 | spend $132.15 < $200 gate; 30d ROAS 42.4x, 20 purchases | New, not in the 21 Sep run |

Monthly ROI: August: spend $1,545, 15 Meta-attributed bookings, blended ROAS 4.8x, retargeting ROAS 25.1x, CPL $1.08 on 144 leads · July: spend $1,054, 4 Meta-attributed bookings, blended ROAS 3.2x, retargeting ROAS 86.3x, CPL $0.80 on 49 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run. Account status: the connector lists ad account 1275283434220508 as UNSETTLED (unpaid balance) and not queryable this week, although the read went through. Check the payment method before delivery stops.

### Paradise Pointe — AM Makenna — account Paradise Pointe Ads (1585826092078255) — CSV export, provisional

ToF (Discovery / Keyword) spend, not scored: $179 over 7 days (export).

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 7d | $171 | 185 leads | CPL $0.93 | Monitor | within lines; CTR here is link CTR from the export | source: CSV export 2026-09-21 to 2026-09-27 (7 days, not the 30-day window), not live; provisional. Export now carries Campaign delivery, so only active campaigns are scored | Unchanged |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 7d | $336 | 6 purchases | ROAS 8.1x | Healthy | CPC $0.82 > $0.62; CTR 1.57% < 2%; CTR here is link CTR from the export | source: CSV export 2026-09-21 to 2026-09-27 (7 days, not the 14-day window), not live; provisional. Export now carries Campaign delivery, so only active campaigns are scored | Fixed, was Review w/ HG AI |

Monthly ROI: August: spend $3,109, 94 Meta-attributed bookings, blended ROAS 16.8x, retargeting ROAS 18.0x, CPL $1.64 on 471 leads · July: spend $2,237, 74 Meta-attributed bookings, blended ROAS 21.6x, retargeting ROAS 16.7x, CPL $1.01 on 90 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes (23 Sep): Meta-credited BoF retargeting purchases fell 76% month over month (ROAS 20.2x to 4.2x, purchase days 18 to 5) while PMS direct revenue stayed flat at about $134k, and the direct-booking channel label switched from BE-API to website in the same window. Check Purchase tracking (Events Manager, pixel and CAPI, test booking) before changing budget; hold BoF spend, add creative and widen the audience if frequency is above 3. (file: 2026-09-23 Paradise Pointe - HG AI.md)

### Endless Stays — AM Nicole — account Endless Stays (896372356081479) — CSV export, provisional

ToF (Discovery / Keyword) spend, not scored: $521 over 7 days (export).

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF Lead Campaign - Retargeting Engagers - 09/09/2026 | Lead Gen (MoF) | 7d | $251 | 237 leads | CPL $1.06 | Review w/ HG AI | CPM $15.30 > $14.84; CTR here is link CTR from the export | source: CSV export 2026-09-21 to 2026-09-27 (7 days, not the 30-day window), not live; provisional. Export now carries Campaign delivery, so only active campaigns are scored | Still open, week 2 |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 7d | $247 | 1 purchases | ROAS 5.4x | Monitor | CPC $0.74 > $0.62; CPM $25.82 > $16.50; cost/booking $246.63 > $90; CTR here is link CTR from the export | source: CSV export 2026-09-21 to 2026-09-27 (7 days, not the 14-day window), not live; provisional. Export now carries Campaign delivery, so only active campaigns are scored | Was Healthy |

Monthly ROI: August: spend $1,553, 10 Meta-attributed bookings, blended ROAS 11.6x, retargeting ROAS 38.8x, CPL $9.73 on 26 leads · July: spend $1,534, 9 Meta-attributed bookings, blended ROAS 16.0x.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### American River Resort — AM Nicole — account American River Resort (953162737054331) — live read

ToF (Discovery / Keyword) spend, not scored: $903 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $441 | 325 leads | CPL $1.36 | Review w/ HG AI | CPM $16.73 > $14.84 | 14d CPL $1.30 | Still open, week 2 |

Paused in window, not scored: MoF - Lead Campaign - Retargeting Engagers (Lead Gen (MoF)), $105 / 30d, 1 leads, CPL $105.09. Live campaigns only are scored (decision 2026-09-23).

Monthly ROI: August: spend $1,529, 3 Meta-attributed bookings, blended ROAS 1.4x, CPL $18.30 on 30 leads · July: spend $1,544, 4 Meta-attributed bookings, blended ROAS 1.1x.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Sunapee Stays — AM Charlotte — account Sunapee Stays Ads Account (651114096215889) — live read

ToF (Discovery / Keyword) spend, not scored: $900 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $299 | 156 leads | CPL $1.92 | Review w/ HG AI | within lines | 14d CPL $1.62 | New, not in the 21 Sep run |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $140 | 0 purchases | ROAS — | Under gate | CPC $0.67 > $0.62; freq 3.3 > 3.0 | spend $140.06 < $200 gate; 30d ROAS 2.3x, 2 purchases | New, not in the 21 Sep run |

Monthly ROI: August: spend $1,494, 10 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 25.1x, CPL $2.74 on 112 leads · July: spend $939, 16 Meta-attributed bookings, blended ROAS 9.9x, CPL $2.06 on 9 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Green Springs Inn — AM Alicia — account Green Springs Inn (1390516335151357) — live read

ToF (Discovery / Keyword) spend, not scored: $603 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign/08/28/2026 | Lead Gen (MoF) | 30d | $301 | 145 leads | CPL $2.08 | Review w/ HG AI | within lines | 14d CPL $1.57 | Still open, week 2 |
| BoF - Sales Campaign - Retargeting Website Visitors - 08/28/26 | Retargeting (BoF) | 14d | $137 | 5 purchases | ROAS 8.7x | Under gate | CPC $0.71 > $0.62 | spend $137.19 < $200 gate; 30d ROAS 10.9x, 11 purchases | Unchanged |

Monthly ROI: August: spend $1,247, 23 Meta-attributed bookings, blended ROAS 8.2x, retargeting ROAS 17.1x, CPL $9.09 on 34 leads · July: spend $1,222, 17 Meta-attributed bookings, blended ROAS 7.8x, retargeting ROAS 14.6x, CPL $5.65 on 8 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Ponderosa Pines Resort — AM Anna — account Ponderosa Pines Resort (1058846326445255) — CSV export, provisional

ToF (Discovery / Keyword) spend, not scored: $280 over 7 days (export).

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| Leads Campaign - 07/16/26 | Lead Gen (MoF) | 7d | $141 | 181 leads | CPL $0.78 | Monitor | within lines; CTR here is link CTR from the export | source: CSV export 2026-09-21 to 2026-09-27 (7 days, not the 30-day window), not live; provisional. Export now carries Campaign delivery, so only active campaigns are scored | Unchanged |
| Website Retarget Campaign - 07/13/26 | Retargeting (BoF) | 7d | $283 | 8 purchases | ROAS 14.2x | Healthy | CPC $0.86 > $0.62; CPM $19.84 > $16.50; CTR here is link CTR from the export | source: CSV export 2026-09-21 to 2026-09-27 (7 days, not the 14-day window), not live; provisional. Export now carries Campaign delivery, so only active campaigns are scored | Was Scale w/ HG AI |

Monthly ROI: August: spend $3,101, 103 Meta-attributed bookings, blended ROAS 15.0x, retargeting ROAS 21.3x, CPL $1.32 on 471 leads · July: spend $2,089, 17 Meta-attributed bookings, blended ROAS 3.6x, retargeting ROAS 22.3x, CPL $0.91 on 356 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### AwayFrames — AM Alicia — account Awayframes Ad Account (2471256056603833) — live read

ToF (Discovery / Keyword) spend, not scored: $597 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers 07/31/2026 | Lead Gen (MoF) | 30d | $149 | 73 leads | CPL $2.04 | Review w/ HG AI | CPC $0.35 > $0.30 | 14d CPL $1.78 | Still open, week 2 |
| BoF - Sales Campaign - Retargeting Website Visitors 07/31/2026 | Retargeting (BoF) | 14d | $71 | 1 purchases | ROAS 10.2x | Under gate | within lines | spend $71.14 < $200 gate; 30d ROAS 4.8x, 1 purchases | Unchanged |

Monthly ROI: August: spend $869, 8 Meta-attributed bookings, blended ROAS 21.8x, retargeting ROAS 27.0x, CPL $2.68 on 58 leads · July: spend $923, 9 Meta-attributed bookings, blended ROAS 18.6x, CPL $2.44 on 2 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Ridge & Falls — AM Makenna — account Ridge & Falls ad account (1313401330776046) — live read

ToF (Discovery / Keyword) spend, not scored: $656 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers - 09/01/26 | Lead Gen (MoF) | 30d | $112 | 12 leads | CPL $9.35 | Flag to Shawal | CPC $0.32 > $0.30; CPM $21.99 > $14.84 | 14d CPL $9.35 | New, not in the 21 Sep run |
| BoF - Sales Campaign - Retargeting Website Visitors - 09/01/26 | Retargeting (BoF) | 14d | $77 | 0 purchases | ROAS — | Under gate | CPM $23.07 > $16.50; freq 4.1 > 3.0 | spend $76.62 < $200 gate | New, not in the 21 Sep run |

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### The Outpost — AM Anna — account The Outpost Grand Canyon (1530849534802936) — live read

ToF (Discovery / Keyword) spend, not scored: $898 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 08/29/2026 | Retargeting (BoF) | 14d | $136 | 0 purchases | ROAS — | Under gate | CPC $0.65 > $0.62 | spend $136.13 < $200 gate | New, not in the 21 Sep run |

Monthly ROI: August: spend $1,876, 7 Meta-attributed bookings, blended ROAS 2.1x, CPL $1.71 on 181 leads · July: spend $2,182, 1 Meta-attributed bookings, blended ROAS 0.2x, CPL $1.61 on 202 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Little River Landing — AM Makenna — account Little River Landing (884285717873613) — live read

ToF (Discovery / Keyword) spend, not scored: $606 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers - 09/16/2026 | Lead Gen (MoF) | 30d | $69 | 38 leads | CPL $1.82 | Under gate | CPC $0.37 > $0.30; CPM $19.71 > $14.84 | spend $69.08 < $100 gate; 14d CPL $1.82 | New, not in the 21 Sep run |
| BoF - Sales Campaign - Retargeting Website Visitors - 09/16/2026 | Retargeting (BoF) | 14d | $56 | 0 purchases | ROAS — | Under gate | freq 3.2 > 3.0 | spend $56.43 < $200 gate | New, not in the 21 Sep run |

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### Bison Ridge Retreat — AM Chiara — account Bison Ridge Retreat Ad Account (950241787963535) — CSV export, provisional

ToF (Discovery / Keyword) spend, not scored: $142 over 7 days (export).

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - RT Engagers | Lead Gen (MoF) | 7d | $35 | 11 leads | CPL $3.16 | Under gate | CPC $0.40 > $0.30; CTR here is link CTR from the export | source: CSV export 2026-09-21 to 2026-09-27 (7 days, not the 30-day window), not live; provisional. Export now carries Campaign delivery, so only active campaigns are scored; spend $34.77 < $100 gate | Unchanged |
| BoF - Sales Campaign - RT Website Visitors | Retargeting (BoF) | 7d | $33 | 0 purchases | ROAS 0.0x | Under gate | within lines; CTR here is link CTR from the export | source: CSV export 2026-09-21 to 2026-09-27 (7 days, not the 14-day window), not live; provisional. Export now carries Campaign delivery, so only active campaigns are scored; spend $33.37 < $200 gate | Unchanged |

Monthly ROI: August: spend $952, 3 Meta-attributed bookings, blended ROAS 8.0x, retargeting ROAS —, CPL $2.47 on 63 leads · July: spend $924, 9 Meta-attributed bookings, blended ROAS 20.3x, retargeting ROAS —, CPL $1.75 on 23 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

### North Star Lodge & Resort — AM Charlotte — account North Star Lodge & Resort Ads (2003562593933799) — live read

ToF (Discovery / Keyword) spend, not scored: $498 over 30 days.

No live Lead Gen or Sales campaigns with spend in the window.

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in since the previous run.

## Footer

- Windows: Lead Gen last 30 days, Sales/Retargeting last 14 days (live). CSV accounts use the export period 2026-09-21 to 2026-09-27 (7 days) and are provisional.
- Gates: $100 Lead Gen, $200 Sales/Retargeting. Campaigns under the gate are listed but not judged.
- Classification: by campaign objective (OUTCOME_LEADS → Lead Gen; OUTCOME_SALES → Sales, split into Retargeting (BoF) or MoF lookalike by name; OUTCOME_TRAFFIC / OUTCOME_ENGAGEMENT → ToF, not scored). CSV accounts have no objective column, so classification there is by name.
- Sales campaigns with an MoF or lookalike prefix are scored on the Retargeting ROAS bands because they optimise for purchases. The Benchmarks doc has no separate band for prospecting sales campaigns; confirm or add one.
- CTR on live rows is Meta's CTR (all clicks), not link CTR. The doc's click-rate lines are probably link CTR, so treat the CTR diagnostic as indicative.
- Frequency and cost per booking are diagnostics only and do not change the state (decision 2026-09-21).
- Only campaigns live (ACTIVE) at run time are scored. Paused campaigns that spent inside the window are listed per client as "Paused in window" and never enter Action needed or the counts (decision 2026-09-23).
- Unclassified campaigns: none.
- Previous report: 2026-09-21-client-benchmark.csv. Diff joined on campaign_id for live rows and client + campaign name for CSV rows. Diff counts: 11 new, 9 still open, 3 fixed, 20 unchanged, 0 removed.
- Scope changes vs 21 Sep: Canopy at Moody Moon dropped (CRM Meta Ads column now reads Basic (AM Kristal); was Advanced on 21 Sep). Advanced in the CRM but with no ad account mapping in PROJECT.md section 5, not scored: Treetop Hideaways (AM Kristal), Walden Retreats (AM Anna), Glasscombe (AM Charlotte).
- HG AI reports read from `HG AI Reports/` at the project root, dated since the previous run: 2026-09-23 Paradise Pointe - HG AI.md, 2026-09-23 Stay Saluda - HG AI.md, 2026-09-23 Taberg Falls - HG AI.md.
- Selah Place's prospecting campaign is named with pipes in Meta ("SP | Prospecting Test | LAL + Interests x Creative | 09-2026"); shown here with dashes.
- Meeting notes: every "Meta Ads Strategy", "Meta Ads Sync" or "Meta Ads x HiddenGem AI Sync" calendar event since the previous run that has a "Notes by Gemini" attachment, read via Drive. Client names are matched with an alias list (Flow Home = FLOHOM, Tabber = Tàberg Falls).
- Monthly ROI context from `Monthly ROI data/` (August 2026, July 2026). Revenue there comes from the Client Performance Tracking sheet, not the pixel, so its ROAS is not comparable to the pixel ROAS above.
