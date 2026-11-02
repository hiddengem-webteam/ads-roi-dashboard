# Client Benchmark Review (advanced setups) — 2026-11-02

Run: 2 November 2026 (Monday), seventh run, compared against 2026-10-26-client-benchmark.csv. Live reads through the Meta Marketing API with the HiddenGem-Claude system user, the standing data path (`scripts/pull-campaign-insights.mts`, 07:36 to 07:38 PT); every account is live and the CSV export 2026-10-19 to 2026-10-25 was not needed for scoring. Scope: clients marked **Advanced** in the CRM "Meta Ads" column (Clients - Onboarding tab), re-read today: 31 clients, 24 with an ad account, unchanged from 26 Oct (Sunapee Stays stays in at Shawal's request although the CRM reads Basic). Seven Advanced clients in the CRM have no ad account yet. First Monday run with the Discovery bucket rows (giveaway + lead spend scored on sign-up promo-code revenue, 28 Oct decision, built 30 Oct), so every Discovery row reads New and the Lead Gen rows that were Flag or Review on cost per lead read "CPL state retired". Only Lead Gen (MoF) and Sales/Retargeting (BoF) campaigns are scored; IG Discovery and Keyword (ToF) spend is shown for context and inside the Discovery row.

| Advanced clients | Live reads | From CSV | Rows scored | Under spend gate | Flag to Shawal | Review w/ HG AI | Monitor | Healthy | Scale w/ HG AI | Frequency over 5 | Tracked in Discovery | No promo data |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 24 (+7 unmapped) | 24 | 0 | 30 | 12 | 4 | 4 | 2 | 11 | 9 | 1 | 21 | 13 |

States come from the Decision Making table in the Benchmarks doc, applied per bucket since the 28 Oct Meta Ads Strategy meeting. Every state is a ROAS state: Sales / Retargeting / Prospecting campaigns on 14-day pixel ROAS ($200 gate); the Discovery bucket (giveaway + lead campaigns of a client, one row) on 30-day sign-up promo-code ROAS from the PMS ($200 gate). Bands: above 15x Scale, 8–15x Healthy, 5–8x Monitor, 2–5x Review, under 2x Flag, inclusive on the lower bound. Lead Gen campaigns show their CPL as a diagnostic and are marked Tracked in Discovery; the only direct Lead Gen flag is the tracking check (spend over the $100 gate with zero leads). Clients whose PMS does not store promo codes get No promo data on the Discovery row.

## Weekly Meta Ads meetings since last run (Notes by Gemini)

Source: "Notes by Gemini" docs attached to the calendar events, read via Drive. Summary, decisions and next steps as Gemini wrote them; client-specific sentences are pulled into each client's section below. Transcript not used.

### Meta Ads Strategy — 2026-10-28 — doc `1PZCCkySabRZwn7_CUglqupOKUp6FUglJexarX709VKA`

Campaign attribution updates and automated ad scaling strategies with targeted client segmentation implementation.

Integration and Campaign Structure

Property Management System coupon integration and campaign categorization into discovery, lookalike prospecting, and retargeting were reviewed. Automated attribution models were developed to distinguish reservation values.

Attribution and Performance Analysis

Booking attribution dashboards for September revealed overlapping data that required weighted credit approaches. Ad weight was shifted toward discovery to improve overall performance metrics.

Agency Scalability and Hiring

Dustin Baker proposed hiring 1 to 2 sales closers to eliminate operational bottlenecks and expand agency capacity. Automated meta ads and strategic campaign scaling aimed to transform direct bookings for independent resorts.

Decisions:
- Three-bucket internal ad tracking structure The team established a three-bucket internal structure for ad spend, revenue, and ROAS-based flagging covering discovery, prospecting, and retargeting.
- Internal dashboard update for three pillars The team agreed to update the internal dashboard to display performance across the three ad pillars.
- Prioritization of discovery in marketing efforts The participants aligned on weighting efforts more toward discovery because it helps move the needle better.

Next steps:
- [Shawal Nazir] Review Hinge Integration: Examine the attribution breakdown under the campaigns page for hinge integration and provide feedback. Ensure the information is useful for reporting purposes.
- [Dustin Baker] Send NDA Website: Share the website link for the new NDA prospect mentioned during the meeting.
- [Shawal Nazir] Share Reporting Documents: Send the weekly Facebook ads reporting document and the hidden gem AI action items document to Dustin Baker.
- [Dustin Baker] Review Action Items: Analyze the weekly action items document and provide feedback once received from Shawal Nazir.
- [Leshan Patterson] Integrate API: Incorporate the Jer reserve API into the current property management system integration.
- [Shawal Nazir] Conduct ROI Analysis: Calculate the October return on ad spend based on the new promo code methodology discussed.
- [Shawal Nazir] Update Flagging System: Modify the tracking dashboard to include flagging for individual campaign return on ad spend.
- [Shawal Nazir] Create Client Master List: Create a master list of advanced clients including their connection type, specific goals, and budget ranges to feed into the internal AI system.
- [Dustin Baker] Review Call Scripts: Review recent call scripts for new clients to establish clear goals and budget ranges for future scaling.
- [Leshan Patterson] Update Internal Dashboard: Update the internal dashboard to incorporate the three-pillar attribution approach for the selected advanced clients.
- [Shawal Nazir] Audit Performance Data: Audit September performance data for Stay on 38 and other advanced clients to identify discrepancies or issues with the attribution model.

## Action needed

Sales, Retargeting and Prospecting campaigns first, then Discovery buckets, then Lead Gen tracking checks. Within each, Flag to Shawal before Review w/ HG AI, highest spend first.

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| AwayFrames | Alicia | MoF - Lookalike Sales Campaign - 10/29/2026 | Prospecting (MoF lookalike) | $203 / 14d | ROAS — | Flag to Shawal | New, not in the 26 Oct run |
| Endless Stays | Nicole | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $1,094 / 14d | ROAS 4.2x | Review w/ HG AI | Still open, week 5 |
| Tàberg Falls | Alicia | MoF - Lookalike Sales Campaign - 08/21/2026 | Prospecting (MoF lookalike) | $827 / 14d | ROAS 2.1x | Review w/ HG AI | New flag, was Monitor |
| Selah Place | Alicia | BoF-Website Retarget Campaign - 07/24/2026 | Retargeting (BoF) | $420 / 14d | ROAS 3.9x | Review w/ HG AI | New flag, was Monitor |
| Tàberg Falls | Alicia | Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | $3,381 / 30d | promo ROAS 0.4x | Flag to Shawal | New, not in the 26 Oct run |
| Little River Landing | Makenna | Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | $1,874 / 30d | promo ROAS 0.2x | Flag to Shawal | New, not in the 26 Oct run |
| Ridge & Falls | Makenna | Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | $1,656 / 30d | promo ROAS 0.0x | Flag to Shawal | New, not in the 26 Oct run |
| AwayFrames | Alicia | Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | $1,445 / 30d | promo ROAS 2.8x | Review w/ HG AI | New, not in the 26 Oct run |

## Scale candidates

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| Stay On 30A | Charlotte | MoF - Sales Campaign - HiddenGem Pixel LoL - 07/17/26 | Prospecting (MoF lookalike) | $2,860 / 14d | ROAS 17.3x | Scale w/ HG AI | Unchanged |
| Paradise Pointe | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $702 / 14d | ROAS 25.0x | Scale w/ HG AI | Unchanged |
| FLOHOM | Makenna | MoF - Lookalike Sales Campaign - 07/29/26 | Prospecting (MoF lookalike) | $693 / 14d | ROAS 19.8x | Scale w/ HG AI | Was Healthy |
| Starlight Haven Weiss Lake | Charlotte | Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | $626 / 14d | ROAS 19.5x | Scale w/ HG AI | Unchanged |
| Treetop Escapes | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $560 / 14d | ROAS 19.7x | Scale w/ HG AI | Was Healthy |
| AwayFrames | Alicia | BoF - Sales Campaign - Retargeting Website Visitors 07/31/2026 | Retargeting (BoF) | $376 / 14d | ROAS 19.9x | Scale w/ HG AI | Was Under gate |
| Starlight Haven Hot Springs | Charlotte | Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | $280 / 14d | ROAS 24.2x | Scale w/ HG AI | Unchanged |
| Paradise Pointe | Makenna | Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | $1,503 / 30d | promo ROAS 49.6x | Scale w/ HG AI | New, not in the 26 Oct run |
| FLOHOM | Makenna | Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | $726 / 30d | promo ROAS 27.9x | Scale w/ HG AI | New, not in the 26 Oct run |

## Frequency watch (Sales / Retargeting above 5)

Sales, Retargeting and MoF-lookalike campaigns whose 14-day frequency is above 5.0 (Shawal, 6 Oct 2026). Frequency does not change the ROAS state; this is the list to refresh creative or widen the audience on. The diagnostics column still notes anything above 3.0.

| Client | AM | Campaign | Type | Frequency | Spend / window | Governing metric | State |
|---|---|---|---|---|---|---|---|
| Paradise Pointe | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 5.85 | $702 / 14d | ROAS 25.0x | Scale w/ HG AI |

## Per client, ordered by scored MoF + BoF spend

### Stay On 30A — AM Charlotte — account Stay on 30a Ads (25640434272252212) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $3,011 over 30 days.

Blended 30d (every HiddenGem campaign): spend $14,956; pixel purchase value $177,746 + sign-up promo revenue $55,209 = $232,955, ROAS 15.6x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $13,115 from 6 bookings, +127% vs 1 Oct–2 Oct ($5,784 from 3 bookings) · promo codes: 5 uses (EARLY BIRD DIRECT ×2, VIP100 ×2, WELCOME100 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $4,508 | 10 promo bookings, $55,209 | promo ROAS 12.2x | — | Healthy | WELCOME100 ×10 $55,209; not counted (not sign-up codes): EARLY BIRD DIRECT ×27 $142,444, VIP100 ×16 $41,853, RETURNINGGUEST ×1 $9,465, WELCOMEBACK15 ×3 $8,697, CINDYSWANSON10 ×2 $7,264, SNOWBIRD30A ×1 $3,400, ESCAPE30A ×1 $2,818, TUCKS20 ×1 $2,173, 10%COAST ×1 $1,199 | $4,508 in 30 days across ToF - Giveaway Traffic Campaign - 02/05/2026, MoF - Lead Campaign - RT Engagers - 07/16/26, against direct bookings booked 3 Oct–2 Nov with a sign-up code | New, not in the 26 Oct run |
| BoF - Sales Campaign - RT Website Visitors - 07/13/26 | Retargeting (BoF) | 14d | $2,132 | 9 purchases | ROAS 13.3x | 3.82 | Healthy | CPC $1.95 > $0.62; CPM $27.18 > $16.50; cost/booking $236.92 > $90; freq 3.8 > 3.0 | 30d ROAS 21.2x, 25 purchases | Was Scale w/ HG AI |
| MoF - Sales Campaign - HiddenGem Pixel LoL - 07/17/26 | Prospecting (MoF lookalike) | 14d | $2,860 | 5 purchases | ROAS 17.3x | 1.68 | Scale w/ HG AI | CPC $1.00 > $0.62; CPM $22.20 > $16.50; cost/booking $572.01 > $90 | 30d ROAS 13.9x, 16 purchases | Unchanged |
| MoF - Lead Campaign - RT Engagers - 07/16/26 | Lead Gen (MoF) | 30d | $1,497 | 1005 leads | CPL $1.49 (diagnostic) | — | Tracked in Discovery | CPC $0.43 > $0.30; CPM $39.27 > $14.84 | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $1.58 | CPL state retired (28 Oct decision), was Review w/ HG AI; see the Discovery row |

Monthly ROI: July: spend $6,407, 67 Meta-attributed bookings, blended ROAS 32.3x, retargeting ROAS 14.6x, CPL $1.24 on 583 leads · August: spend $12,420, 85 Meta-attributed bookings, blended ROAS 17.8x, retargeting ROAS 15.5x, CPL $2.58 on 594 leads · September: spend $12,606, 91 Meta-attributed bookings, blended ROAS 24.4x, retargeting ROAS 23.1x, CPL $1.52 on 1001 leads.

Meeting notes (Meta Ads Strategy 2026-10-28): Hinge and PMS Coupon Integration Updates: Leshan Patterson stated that they were working on the hinge integration under campaigns and booking attribution for stay on 38, with plans to roll it out to all clients that have Property Management System coupon integration, including flow home, tree tops escapes, stay on 38, saluda, and tab fel. Selection of Advanced Clients for Rollout: Dustin Baker and Shawal Nazir discussed creating a formal, short list of advanced clients—such as Asheville, Stay on 38, Arca, and Rhodin—with established budget ranges and clear return on ad spend goals (e.g., five times for Asheville, seven times for Flowhome) rather than relying on basic tier labels. Booking Attribution Dashboard Review for September: Leshan Patterson presented the version one booking attribution dashboard for Stay on 38 for September, revealing an overlap of 9 bookings worth 34,000 dollars that would have been double counted if top-of-funnel and retargeting figures were simply added together.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). BoF slips from Scale to Healthy at 13.3x on 9 purchases ($2,132 in 14 days; CPC $1.95, cost per booking $237, frequency 3.8), while the HiddenGem Pixel lookalike holds Scale at 17.3x on 5 purchases ($2,860). Discovery row enters at Healthy, 12.3x: the ToF giveaway plus the leads campaign cost $4,508 in 30 days and WELCOME100 bookings brought $55.2k; the EARLY BIRD DIRECT (×27, $142k), VIP100 (×16, $41.9k) and WELCOMEBACK15 codes are shown but not counted as sign-up codes. Leads $1.49 on 1,005 leads, CPL now a diagnostic. 28 Oct Strategy: the platform's campaign attribution (Hinge) is being built on this account first and Shawal is to audit its September attribution for discrepancies. Pixel check: 70 Purchase in 28 days, all server-side from Guesty, against 65 online bookings.

### Tàberg Falls — AM Alicia — account Táberg Falls (827872700004659) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $1,849 over 30 days.

Blended 30d (every HiddenGem campaign): spend $8,091; pixel purchase value $41,161 + sign-up promo revenue $1,240 = $42,401, ROAS 5.2x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $3,634 from 2 bookings, +25% vs 1 Oct–2 Oct ($2,912 from 2 bookings) · promo codes: 0 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $3,381 | 1 promo bookings, $1,240 | promo ROAS 0.4x | — | Flag to Shawal | 1 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $3,381 in 30 days across MoF - Leads Campaign - 06/19/26, ToF - Giveaway Campaign - 07/08/2026, against direct bookings booked 3 Oct–2 Nov with a sign-up code | New, not in the 26 Oct run |
| MoF - Lookalike Sales Campaign - 08/21/2026 | Prospecting (MoF lookalike) | 14d | $827 | 1 purchases | ROAS 2.1x | 1.44 | Review w/ HG AI | cost/booking $826.94 > $90 | 30d ROAS 8.2x, 9 purchases | New flag, was Monitor |
| BoF - Website Retargeting Campaign - 08/21/2026 | Retargeting (BoF) | 14d | $886 | 6 purchases | ROAS 12.0x | 2.85 | Healthy | CPC $0.72 > $0.62; CPM $23.91 > $16.50; cost/booking $147.72 > $90 | 30d ROAS 11.3x, 13 purchases | Unchanged |
| MoF - Leads Campaign - 06/19/26 | Lead Gen (MoF) | 30d | $1,532 | 2689 leads | CPL $0.57 (diagnostic) | — | Tracked in Discovery | within lines | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $0.59 | Was Monitor, CPL no longer scored |

Paused in window, not scored: MoF - Broad (Acquire new customers) - 09/28/2026 (Prospecting (MoF lookalike)), $13 / 14d, 0 purchases, ROAS —. Live campaigns only are scored (decision 2026-09-23).

Monthly ROI: July: spend $11,739, 80 Meta-attributed bookings, blended ROAS 9.5x, retargeting ROAS 15.8x, CPL $0.67 on 2320 leads · August: spend $11,259, 31 Meta-attributed bookings, blended ROAS 4.5x, retargeting ROAS 8.0x, CPL $0.46 on 4015 leads · September: spend $10,800, 27 Meta-attributed bookings, blended ROAS 4.0x, retargeting ROAS 7.1x, CPL $0.55 on 3261 leads.

Meeting notes (Meta Ads Strategy 2026-10-28): Hinge and PMS Coupon Integration Updates: Leshan Patterson stated that they were working on the hinge integration under campaigns and booking attribution for stay on 38, with plans to roll it out to all clients that have Property Management System coupon integration, including flow home, tree tops escapes, stay on 38, saluda, and tab fel.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). Two new Action rows. The lookalike prospecting campaign drops from Monitor (8.0x) to Review at 2.1x on a single purchase ($827 in 14 days) the week its budget doubled from $50 to $100/day; 30 days read 4.0x on 4 purchases, so the audience has cooled rather than broken. The Discovery row flags at 0.4x: $3,381 of giveaway and lead spend in 30 days against one coupon booking ($1,240) in Hostaway, while the leads campaign delivered 2,689 leads at $0.57. Either the sign-up codes are not being redeemed or Hostaway is not recording the coupon on those bookings; Alicia to check a few recent WELCOME bookings in Hostaway before the row is read as a performance problem. BoF 12.0x Healthy on 6 purchases ($886, also doubled to $100/day). The paused Broad prospecting test spent $13 in the window. 28 Oct Strategy: Tàberg is on the list for the platform's promo-code attribution rollout.

### Endless Stays — AM Nicole — account Endless Stays (896372356081479) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $2,257 over 30 days.

Blended 30d (every HiddenGem campaign): spend $6,055; pixel purchase value $7,811 + sign-up promo revenue $0 = $7,811, ROAS 1.3x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $0 from 0 bookings, no direct revenue in 1 Oct–2 Oct to compare against · promo codes: not tracked by hospitable.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $1,094 | 1 purchases | ROAS 4.2x | 2.45 | Review w/ HG AI | CPC $0.62 > $0.62; CPM $16.76 > $16.50; cost/booking $1,093.76 > $90 | 30d ROAS 3.4x, 3 purchases | Still open, week 5 |
| MoF Lead Campaign - Retargeting Engagers - 09/09/2026 | Lead Gen (MoF) | 30d | $1,498 | 1656 leads | CPL $0.90 (diagnostic) | — | Tracked in Discovery | within lines | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $1.04 | Was Monitor, CPL no longer scored |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $3,755 | — | promo ROAS — | — | No promo data | — | $3,755 in 30 days across ToF - Giveaway Traffic Campaign - AZ, FL, VA, PA, TN, MoF Lead Campaign - Retargeting Engagers - 09/09/2026; hospitable does not store promo codes on the booking, so sign-up revenue cannot be measured and the bucket is not scored | New, not in the 26 Oct run |

Monthly ROI: July: spend $1,534, 9 Meta-attributed bookings, blended ROAS 16.0x · August: spend $1,553, 10 Meta-attributed bookings, blended ROAS 11.6x, retargeting ROAS 38.8x, CPL $9.73 on 26 leads · September: spend $2,539, 6 Meta-attributed bookings, blended ROAS 2.9x, retargeting ROAS 4.7x, CPL $1.05 on 532 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). BoF 4.2x on one purchase ($1,094 in 14 days, cost per booking $1,094; 3.3x on 3 purchases over 30), fifth week at Review and the largest Review spend on the list. Leads $0.90 on 1,656 leads. The Discovery row cannot be scored (Hospitable stores no promo code), so $3,755 of 30-day giveaway and lead spend has no revenue read at all; this is the biggest blind spot the new buckets expose. Pixel check: 13 Purchase in 28 days, all from the HG AI CAPI, against 13 online bookings, so the pixel is complete but the bookings themselves are few.

### Paradise Pointe — AM Makenna — account Paradise Pointe Ads (1585826092078255) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $753 over 30 days.

Blended 30d (every HiddenGem campaign): spend $4,510; pixel purchase value $35,881 + sign-up promo revenue $74,605 = $110,486, ROAS 24.5x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $7,838 from 7 bookings, +57% vs 1 Oct–2 Oct ($5,007 from 7 bookings) · promo codes: 3 uses (WELCOME100 ×3).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - LoL Sales Campaign - 09/28/26 | Prospecting (MoF lookalike) | 14d | $691 | 10 purchases | ROAS 12.7x | 2.19 | Healthy | CPC $0.63 > $0.62 | 30d ROAS 10.5x, 34 purchases | Was Monitor |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,503 | 66 promo bookings, $74,605 | promo ROAS 49.6x | — | Scale w/ HG AI | WELCOME100 ×63 $70,056, WELCOME10 ×3 $4,549; not counted (not sign-up codes): VIP100 ×3 $3,074 | $1,503 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Giveaway Traffic Campaign, against direct bookings booked 3 Oct–2 Nov with a sign-up code | New, not in the 26 Oct run |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $702 | 15 purchases | ROAS 25.0x | 5.85 ⚠️ > 5 | Scale w/ HG AI | CPC $0.88 > $0.62; freq 5.9 > 3.0 | 30d ROAS 13.4x, 31 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $751 | 735 leads | CPL $1.02 (diagnostic) | — | Tracked in Discovery | within lines | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $1.04 | CPL state retired (28 Oct decision), was Review w/ HG AI; see the Discovery row |

Monthly ROI: July: spend $2,237, 74 Meta-attributed bookings, blended ROAS 21.6x, retargeting ROAS 16.7x, CPL $1.01 on 90 leads · August: spend $3,109, 94 Meta-attributed bookings, blended ROAS 16.8x, retargeting ROAS 18.0x, CPL $1.64 on 471 leads · September: spend $3,074, 48 Meta-attributed bookings, blended ROAS 7.0x, retargeting ROAS 13.0x, CPL $0.97 on 764 leads. Note in the September file: Meta did not record revenue for 12 retargeting purchases (week of Sep 15–21 and Sep 29–30); their value was added manually at the average booking value (12 × $1,170.59 = $14,047.08) and the ROAS updated.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). Strongest account this week. BoF 25.0x Scale on 15 purchases ($702; 15.1x last week), but frequency 5.85 keeps it the only Frequency-watch row, and the pixel check shows browser Purchases at 148% of online bookings (a confirmation page that fires on reload), so the pixel ROAS is overstated; the Discovery row says the same thing from the PMS side at 49.6x: $1,503 of giveaway and lead spend against 66 WELCOME100 and WELCOME10 bookings worth $74.6k in 30 days. Lookalike 12.7x Healthy on 10 purchases (up from Monitor). Leads $1.02 on 735 leads. This month +57% on October's same two days.

### Treetop Escapes — AM Makenna — account Treetop Escapes Ads (967636478877602) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $904 over 30 days.

Blended 30d (every HiddenGem campaign): spend $3,013; pixel purchase value $14,841 + sign-up promo revenue $21,598 = $36,439, ROAS 12.1x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $5,617 from 4 bookings, +1% vs 1 Oct–2 Oct ($5,572 from 5 bookings) · promo codes: 2 uses (WELCOME100 ×2).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,807 | 19 promo bookings, $21,598 | promo ROAS 12.0x | — | Healthy | WELCOME100 ×17 $18,627, WELCOME10 ×2 $2,971; not counted (not sign-up codes): VIP100 ×1 $1,435 | $1,807 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Giveaway Traffic Campaign, against direct bookings booked 3 Oct–2 Nov with a sign-up code | New, not in the 26 Oct run |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $560 | 9 purchases | ROAS 19.7x | 3.31 | Scale w/ HG AI | CPM $16.60 > $16.50; freq 3.3 > 3.0 | 30d ROAS 12.3x, 15 purchases | Was Healthy |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $903 | 1146 leads | CPL $0.79 (diagnostic) | — | Tracked in Discovery | CPM $19.57 > $14.84 | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $0.77 | Was Monitor, CPL no longer scored |

Monthly ROI: July: spend $2,487, 44 Meta-attributed bookings, blended ROAS 14.5x, retargeting ROAS 22.2x, CPL $1.48 on 21 leads · August: spend $3,082, 28 Meta-attributed bookings, blended ROAS 8.8x, retargeting ROAS 16.3x, CPL $1.49 on 620 leads · September: spend $2,998, 10 Meta-attributed bookings, blended ROAS 3.8x, retargeting ROAS 7.9x, CPL $0.88 on 1019 leads.

Meeting notes (Meta Ads Strategy 2026-10-28): Hinge and PMS Coupon Integration Updates: Leshan Patterson stated that they were working on the hinge integration under campaigns and booking attribution for stay on 38, with plans to roll it out to all clients that have Property Management System coupon integration, including flow home, tree tops escapes, stay on 38, saluda, and tab fel.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). BoF up from Healthy to Scale at 19.7x on 9 purchases ($560 in 14 days), frequency 3.3. Discovery row Healthy at 12.0x: $1,807 of giveaway and lead spend against WELCOME100 ×17 and WELCOME10 ×2 bookings worth $21.6k. Leads $0.79 on 1,146 leads. 28 Oct Strategy: on the promo-code attribution rollout list.

### Ponderosa Pines Resort — AM Anna — account Ponderosa Pines Resort (1058846326445255) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $1,204 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,998; pixel purchase value $14,104 + sign-up promo revenue $0 = $14,104, ROAS 4.7x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $2,621 from 6 bookings, +47% vs 1 Oct–2 Oct ($1,784 from 7 bookings) · promo codes: not tracked by newbook.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Website Retarget Campaign - 07/13/26 | Retargeting (BoF) | 14d | $563 | 16 purchases | ROAS 10.5x | 2.49 | Healthy | CPC $0.75 > $0.62; CPM $21.87 > $16.50 | 30d ROAS 11.8x, 31 purchases | Unchanged |
| Leads Campaign - 07/16/26 | Lead Gen (MoF) | 30d | $598 | 564 leads | CPL $1.06 (diagnostic) | — | Tracked in Discovery | CPM $14.88 > $14.84 | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $1.20 | Was Monitor, CPL no longer scored |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,802 | — | promo ROAS — | — | No promo data | — | $1,802 in 30 days across Discovery Campaign - Giveaway - June 2026, Leads Campaign - 07/16/26; newbook does not store promo codes on the booking, so sign-up revenue cannot be measured and the bucket is not scored | New, not in the 26 Oct run |

Monthly ROI: July: spend $2,089, 17 Meta-attributed bookings, blended ROAS 3.6x, retargeting ROAS 22.3x, CPL $0.91 on 356 leads · August: spend $3,101, 103 Meta-attributed bookings, blended ROAS 15.0x, retargeting ROAS 21.3x, CPL $1.32 on 471 leads · September: spend $2,985, 119 Meta-attributed bookings, blended ROAS 17.9x, retargeting ROAS 21.6x, CPL $0.84 on 708 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). BoF 10.5x Healthy on 16 purchases ($563; 9.4x last week), frequency 2.5. Leads $1.06 on 564 leads. Discovery row has no promo data (Newbook stores no code) on $1,802 of 30-day spend. Pixel check caveat: browser Purchases are 1.66x the PMS bookings (313 Purchase against 125 bookings in 28 days), so the pixel ROAS here is inflated by the Newbook confirmation firing more than once per booking; Anna to fix the confirmation event. This month +47%.

### Starlight Haven Hot Springs — AM Charlotte — account Starlight Haven Hot Springs (901138032027913) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $756 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,252; pixel purchase value $13,504 + sign-up promo revenue $0 = $13,504, ROAS 6.0x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $280 | 9 purchases | ROAS 24.2x | 2.06 | Scale w/ HG AI | within lines | 30d ROAS 22.7x, 20 purchases | Unchanged |
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $901 | 2848 leads | CPL $0.32 (diagnostic) | — | Tracked in Discovery | within lines | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $0.31 | Was Healthy, CPL no longer scored |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,657 | — | promo ROAS — | — | No promo data | — | $1,657 in 30 days across Discovery Campaign - Giveaway - 12/16/2025, New Leads Campaign - 03/03/26; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured and the bucket is not scored | New, not in the 26 Oct run |

Monthly ROI: July: spend $2,160, 17 Meta-attributed bookings, blended ROAS 5.1x, retargeting ROAS 17.1x, CPL $0.33 on 2813 leads · August: spend $2,193, 19 Meta-attributed bookings, blended ROAS 6.3x, retargeting ROAS 22.3x, CPL $0.36 on 2589 leads · September: spend $2,155, 61 Meta-attributed bookings, blended ROAS 16.5x, retargeting ROAS 28.5x, CPL $0.34 on 2597 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). Both campaigns in good shape: BoF 24.2x Scale on 9 purchases ($280), leads $0.32 on 2,848 leads. No promo data (ResNexus) for the Discovery row on $1,657 of spend.

### FLOHOM — AM Makenna — account FLOHOM Ads (2100710320122219) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $300 over 30 days.

Blended 30d (every HiddenGem campaign): spend $5,175; pixel purchase value $40,683 + sign-up promo revenue $20,299 = $60,982, ROAS 11.8x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $2,172 from 4 bookings, −72% vs 1 Oct–2 Oct ($7,813 from 11 bookings) · promo codes: 1 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $696 | 6 purchases | ROAS 5.3x | 2.27 | Monitor | CPC $0.67 > $0.62; CPM $19.37 > $16.50; cost/booking $116.03 > $90 | 30d ROAS 4.8x, 14 purchases | Unchanged |
| [Myrtle Beach] MoF - Lookalike Sales Campaign - 09/17/26 | Prospecting (MoF lookalike) | 14d | $275 | 1 purchases | ROAS 8.2x | 2.28 | Healthy | CPC $1.10 > $0.62; CPM $21.01 > $16.50; cost/booking $274.57 > $90 | 30d ROAS 9.6x, 3 purchases | Was Monitor |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $726 | 22 promo bookings, $20,299 | promo ROAS 27.9x | — | Scale w/ HG AI | 22 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $726 in 30 days across ToF - Giveaway Traffic Campaign, MoF - Lead Campaign - Retargeting Engagers – 08/17/26, against direct bookings booked 3 Oct–2 Nov with a sign-up code | New, not in the 26 Oct run |
| MoF - Lookalike Sales Campaign - 07/29/26 | Prospecting (MoF lookalike) | 14d | $693 | 15 purchases | ROAS 19.8x | 2.28 | Scale w/ HG AI | CPC $0.63 > $0.62; CPM $18.87 > $16.50 | 30d ROAS 13.7x, 27 purchases | Was Healthy |
| MoF - Lead Campaign - Retargeting Engagers – 08/17/26 | Lead Gen (MoF) | 30d | $427 | 760 leads | CPL $0.56 (diagnostic) | — | Tracked in Discovery | within lines | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $0.52 | Was Monitor, CPL no longer scored |

Monthly ROI: July: spend $5,555, 103 Meta-attributed bookings, blended ROAS 17.2x, retargeting ROAS 19.1x, CPL $7.66 on 66 leads · August: spend $9,331, 57 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 8.2x, CPL $2.24 on 708 leads · September: spend $8,855, 66 Meta-attributed bookings, blended ROAS 6.7x, retargeting ROAS 8.9x, CPL $0.50 on 2192 leads.

Meeting notes (Meta Ads Strategy 2026-10-28): Hinge and PMS Coupon Integration Updates: Leshan Patterson stated that they were working on the hinge integration under campaigns and booking attribution for stay on 38, with plans to roll it out to all clients that have Property Management System coupon integration, including flow home, tree tops escapes, stay on 38, saluda, and tab fel.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). Lookalike up from Healthy to Scale at 19.8x on 15 purchases ($693 in 14 days); Myrtle Beach lookalike 8.2x Healthy on 1 purchase ($275); BoF 5.3x Monitor on 6 purchases, unchanged. Discovery row enters at Scale, 27.9x: $726 of giveaway and lead spend against 22 coupon bookings ($20.3k) in Hostaway, which stores no code names, so every coupon booking counts (caveat). Leads $0.56 on 760 leads. Pixel check: booking-engine traffic on book.flohom.com fell 90% from 31 Oct while Purchases kept arriving server-side from Hostaway's CAPI (100 in 28 days against 103 online bookings); Makenna to check the booking page pixel. 28 Oct Strategy: FLOHOM is on the promo-code attribution rollout list.

### AwayFrames — AM Alicia — account Awayframes Ad Account (2471256056603833) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $890 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,105; pixel purchase value $8,128 + sign-up promo revenue $4,059 = $12,187, ROAS 5.8x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $3,435 from 2 bookings, +33% vs 1 Oct–2 Oct ($2,589 from 3 bookings) · promo codes: 0 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lookalike Sales Campaign - 10/29/2026 | Prospecting (MoF lookalike) | 14d | $203 | 0 purchases | ROAS — | 1.33 | Flag to Shawal | CPC $1.24 > $0.62; CPM $17.47 > $16.50 | no purchases | New, not in the 26 Oct run |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,445 | 3 promo bookings, $4,059 | promo ROAS 2.8x | — | Review w/ HG AI | 3 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $1,445 in 30 days across ToF - Giveaway Traffic Campaign - 07/31/2026, MoF - Lead Campaign - Retargeting Engagers 07/31/2026, against direct bookings booked 3 Oct–2 Nov with a sign-up code | New, not in the 26 Oct run |
| BoF - Sales Campaign - Retargeting Website Visitors 07/31/2026 | Retargeting (BoF) | 14d | $376 | 7 purchases | ROAS 19.9x | 4.32 | Scale w/ HG AI | CPC $1.72 > $0.62; CPM $16.57 > $16.50; CTR 1.68% < 2%; freq 4.3 > 3.0 | 30d ROAS 17.8x, 8 purchases | Was Under gate |
| MoF - Lead Campaign - Retargeting Engagers 07/31/2026 | Lead Gen (MoF) | 30d | $555 | 350 leads | CPL $1.58 (diagnostic) | — | Tracked in Discovery | CPC $0.34 > $0.30 | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $1.63 | CPL state retired (28 Oct decision), was Review w/ HG AI; see the Discovery row |

Monthly ROI: July: spend $923, 9 Meta-attributed bookings, blended ROAS 18.6x, CPL $2.44 on 2 leads · August: spend $869, 8 Meta-attributed bookings, blended ROAS 21.8x, retargeting ROAS 27.0x, CPL $2.68 on 58 leads · September: spend $895, 7 Meta-attributed bookings, blended ROAS 11.1x, retargeting ROAS 4.9x, CPL $1.83 on 82 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). Budget went from $30 to $200/day on 29 Oct (spend check), so the account is in its first week at scale. The new MoF lookalike (10/29) has $203 in 14 days and no purchase yet, which the rules read as Flag; it is four days old, so treat it as a tracking check to re-read next week rather than a verdict. BoF crosses the gate for the first time at 19.9x on 7 purchases ($376) and enters Scale (frequency 4.3). Discovery row Review at 2.8x: $1,445 of giveaway and lead spend against 3 coupon bookings ($4,059) in Hostaway. Leads $1.58 on 350 leads. Pixel check: 24 Purchase in 28 days, all server-side, against 20 online bookings; the HG AI CAPI toggle is OFF while its ledger still shows sends to 28 Oct, so Hostaway's CAPI is now the sender.

### Stay Saluda NC — AM Makenna — account Stay Saluda Ads (1863632561215857) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $903 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,396; pixel purchase value $5,229 + sign-up promo revenue $13,299 = $18,528, ROAS 7.7x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $2,043 from 3 bookings, +89% vs 1 Oct–2 Oct ($1,082 from 2 bookings) · promo codes: 2 uses (ENJOY10 ×2).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,499 | 18 promo bookings, $13,299 | promo ROAS 8.9x | — | Healthy | ENJOY10 ×12 $6,755, WELCOME10 ×6 $6,544; not counted (not sign-up codes): VIP10 ×1 $769, DUBLE10 ×1 $273 | $1,499 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Giveaway Traffic Campaign - NC/SC/GA/TN, against direct bookings booked 3 Oct–2 Nov with a sign-up code | New, not in the 26 Oct run |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $425 | 6 purchases | ROAS 8.1x | 4.27 | Healthy | CPC $0.81 > $0.62; CPM $19.64 > $16.50; freq 4.3 > 3.0 | 30d ROAS 5.8x, 9 purchases | Fixed, was Flag to Shawal |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $596 | 632 leads | CPL $0.94 (diagnostic) | — | Tracked in Discovery | CPM $15.30 > $14.84 | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $0.97 | Was Monitor, CPL no longer scored |

Monthly ROI: July: spend $2,140, 10 Meta-attributed bookings, blended ROAS 2.6x, retargeting ROAS 0.8x · August: spend $2,367, 9 Meta-attributed bookings, blended ROAS 3.7x, retargeting ROAS 5.2x, CPL $2.59 on 146 leads · September: spend $2,394, 6 Meta-attributed bookings, blended ROAS 1.3x, retargeting ROAS 3.5x, CPL $1.00 on 596 leads.

Meeting notes (Meta Ads Strategy 2026-10-28): Hinge and PMS Coupon Integration Updates: Leshan Patterson stated that they were working on the hinge integration under campaigns and booking attribution for stay on 38, with plans to roll it out to all clients that have Property Management System coupon integration, including flow home, tree tops escapes, stay on 38, saluda, and tab fel. Weekly Ads Reporting and Creative Adjustments: Shawal Nazir shared that they distribute a weekly Facebook ads report showing improving ad performance and fewer flags, noting that account managers and marketing assistants help with creatives when red flags arise, such as a recent creative need for sh saluda.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). BoF Fixed: from Flag (1.7x) to Healthy at 8.1x on 6 purchases ($425 in 14 days; 7.1x on 11 purchases over 30), although frequency 4.3 is still high. Discovery row Healthy at 8.9x: $1,499 of giveaway and lead spend against ENJOY10 ×12 and WELCOME10 ×6 bookings worth $13.3k. Leads $0.94 on 632 leads. This month +89% on October's same two days. 28 Oct Strategy: on the promo-code attribution rollout list. Pixel: the Saluda GHL hosts still fire the Inspired Retreats pixel (week 7).

### Little River Landing — AM Makenna — account Little River Landing (884285717873613) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $1,725 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,148; pixel purchase value $393 + sign-up promo revenue $393 = $786, ROAS 0.4x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $226 from 2 bookings, +15% vs 1 Oct–2 Oct ($197 from 1 bookings) · promo codes: 0 uses.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,874 | 1 promo bookings, $393 | promo ROAS 0.2x | — | Flag to Shawal | WELCOME10 ×1 $393 | $1,874 in 30 days across ToF - Giveaway Traffic Campaign - AL - 09/16/2026, MoF - Lead Campaign - Retargeting Engagers - 09/16/2026, against direct bookings booked 3 Oct–2 Nov with a sign-up code | New, not in the 26 Oct run |
| BoF - Sales Campaign - Retargeting Website Visitors - 09/16/2026 | Retargeting (BoF) | 14d | $179 | 1 purchases | ROAS 2.2x | 2.96 | Under gate | CPC $0.68 > $0.62; cost/booking $178.89 > $90 | spend $178.89 < $200 gate; 30d ROAS 1.4x, 1 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 09/16/2026 | Lead Gen (MoF) | 30d | $149 | 95 leads | CPL $1.57 (diagnostic) | — | Tracked in Discovery | CPC $0.45 > $0.30; CPM $21.89 > $14.84 | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $2.00 | CPL state retired (28 Oct decision), was Review w/ HG AI; see the Discovery row |

Monthly ROI: September: spend $921, 0 Meta-attributed bookings, blended ROAS —, retargeting ROAS —, CPL $1.86 on 46 leads. Note in the September file: Newly launched campaigns — $921.36 spent, no revenue from ads yet.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). Discovery row flags at 0.2x: $1,874 of giveaway and lead spend in 30 days ($65/day on the giveaway) against one WELCOME10 booking ($393). Leads $1.57 on 95 leads on $5/day. BoF under the gate, 2.2x on 1 purchase ($179). The pixel check is ❌ here too (3 Purchase in 28 days against 11 online bookings, HG AI CAPI OFF), so the $15/day BoF is optimising on a quarter of the real bookings. Next action (Makenna / Leshan): turn the HG AI CAPI on for the tenant and check sign-up code redemption in Guesty.

### Asheville River Cabins — AM Charlotte — account Asheville River Cabins Ads (615836588009747) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $1,163 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,327; pixel purchase value $22,921 + sign-up promo revenue $0 = $22,921, ROAS 9.8x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Website Retargeting Campaign - 06/08/26 | Retargeting (BoF) | 14d | $417 | 7 purchases | ROAS 7.9x | 2.30 | Monitor | CPM $20.05 > $16.50 | 30d ROAS 26.3x, 25 purchases | Was Healthy |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $292 | 889 leads | CPL $0.33 (diagnostic) | — | Tracked in Discovery | within lines | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $0.36 | Was Healthy, CPL no longer scored |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,455 | — | promo ROAS — | — | No promo data | — | $1,455 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Discovery Campaign Giveaway - 09/17/26; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured and the bucket is not scored | New, not in the 26 Oct run |

Monthly ROI: July: spend $2,029, 39 Meta-attributed bookings, blended ROAS 18.6x, retargeting ROAS 51.6x · August: spend $2,424, 82 Meta-attributed bookings, blended ROAS 27.2x, retargeting ROAS 65.0x, CPL $0.42 on 605 leads · September: spend $2,252, 70 Meta-attributed bookings, blended ROAS 19.1x, retargeting ROAS 42.5x, CPL $0.30 on 936 leads.

Meeting notes (Meta Ads Strategy 2026-10-28): Selection of Advanced Clients for Rollout: Dustin Baker and Shawal Nazir discussed creating a formal, short list of advanced clients—such as Asheville, Stay on 38, Arca, and Rhodin—with established budget ranges and clear return on ad spend goals (e.g., five times for Asheville, seven times for Flowhome) rather than relying on basic tier labels.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). BoF slips from Healthy to Monitor at 7.9x on 7 purchases ($417 in 14 days; 20.6x on 30 days), CPM $20. Leads $0.33 on 889 leads. No promo data for the Discovery row ($1,455 of spend): the 28 Oct notes say Leshan has integrated Cloudbeds to show promo-code data, but the platform's Cloudbeds bookings still carry no code field in the query this report uses, so Leshan to confirm where the Cloudbeds coupon lands (also applies to Glasscombe and North Star). 28 Oct Strategy: Asheville named as one of the advanced clients to get a formal budget range and ROAS goal (five times was the example). Pixel: still browser-only, 0 server events, the one CAPI-silent row left.

### Starlight Haven Weiss Lake — AM Charlotte — account Starlight Haven Weiss Lake (74756899) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $0 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,094; pixel purchase value $30,935 + sign-up promo revenue $0 = $30,935, ROAS 14.8x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $626 | 24 purchases | ROAS 19.5x | 2.60 | Scale w/ HG AI | CPC $0.76 > $0.62 | 30d ROAS 23.0x, 50 purchases | Unchanged |
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $749 | 676 leads | CPL $1.11 (diagnostic) | — | Tracked in Discovery | CPC $0.36 > $0.30 | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $1.11 | CPL state retired (28 Oct decision), was Review w/ HG AI; see the Discovery row |
| Discovery bucket (1 campaign: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $749 | — | promo ROAS — | — | No promo data | — | $749 in 30 days across New Leads Campaign - 03/03/26; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured and the bucket is not scored | New, not in the 26 Oct run |

Monthly ROI: July: spend $2,163, 41 Meta-attributed bookings, blended ROAS 10.8x, retargeting ROAS 15.2x, CPL $0.74 on 826 leads · August: spend $2,351, 36 Meta-attributed bookings, blended ROAS 10.7x, retargeting ROAS 17.6x, CPL $1.23 on 617 leads · September: spend $2,152, 79 Meta-attributed bookings, blended ROAS 17.4x, retargeting ROAS 23.8x, CPL $1.01 on 734 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). BoF 19.5x Scale on 24 purchases ($626). Leads $1.11 on 676 leads (CPL state retired). No promo data (ResNexus) on $749.

### Ridge & Falls — AM Makenna — account Ridge & Falls ad account (1313401330776046) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $1,508 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,924; pixel purchase value $4,322 + sign-up promo revenue $0 = $4,322, ROAS 2.2x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $972 from 2 bookings, +290% vs 1 Oct–2 Oct ($249 from 1 bookings) · promo codes: 1 uses (HELLO10 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,656 | 0 promo bookings, $0 | promo ROAS 0.0x | — | Flag to Shawal | no sign-up code bookings in 30 days; not counted (not sign-up codes): HELLO10 ×1 $463 | $1,656 in 30 days across ToF - Giveaway Traffic Campaign - GA, AL - 09/01/26, MoF - Lead Campaign - Retargeting Engagers - 09/01/26, against direct bookings booked 3 Oct–2 Nov with a sign-up code; no sign-up promo bookings in 30 days | New, not in the 26 Oct run |
| BoF - Sales Campaign - Retargeting Website Visitors - 09/01/26 | Retargeting (BoF) | 14d | $174 | 6 purchases | ROAS 19.2x | 4.59 | Under gate | freq 4.6 > 3.0 | spend $173.74 < $200 gate; 30d ROAS 16.2x, 8 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 09/01/26 | Lead Gen (MoF) | 30d | $149 | 67 leads | CPL $2.22 (diagnostic) | — | Tracked in Discovery | CPC $0.35 > $0.30 | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $1.85 | CPL state retired (28 Oct decision), was Flag to Shawal; see the Discovery row |

Monthly ROI: September: spend $1,036, 0 Meta-attributed bookings, blended ROAS —, retargeting ROAS —, CPL $8.16 on 16 leads. Note in the September file: Newly launched campaigns — $1,036.47 spent, no revenue from ads yet (spend exceeds the $871.49 September direct revenue, as expected for a launch month).

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). Discovery row flags at 0.0x: $1,656 of giveaway and lead spend in 30 days and no booking with a sign-up code; the one coded booking was HELLO10 ($463), which is not in the sign-up list (WELCOME, ENJOY, SIGNUP, GIVEAWAY). Shawal to say whether HELLO10 is Ridge & Falls' sign-up code; if so the row reads 0.3x, still a Flag. Leads $2.22 on 67 leads ($149 on $5/day; CPL state retired). BoF 19.2x on 6 purchases but under the gate ($174). Pixel check: 19 server Purchase against 11 online bookings, the HG AI CAPI plus a second sender; one should be switched off.

### Selah Place — AM Alicia — account Selah.place (1275283434220508) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $755 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,803; pixel purchase value $6,008 + sign-up promo revenue $10,338 = $16,346, ROAS 9.1x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $874 from 2 bookings, −68% vs 1 Oct–2 Oct ($2,707 from 5 bookings) · promo codes: 1 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF-Website Retarget Campaign - 07/24/2026 | Retargeting (BoF) | 14d | $420 | 6 purchases | ROAS 3.9x | 4.46 | Review w/ HG AI | CPC $0.71 > $0.62; CPM $24.25 > $16.50; freq 4.5 > 3.0 | 30d ROAS 7.5x, 15 purchases | New flag, was Monitor |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,003 | 19 promo bookings, $10,338 | promo ROAS 10.3x | — | Healthy | 19 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $1,003 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Giveaway Traffic Campaign - 08/07/2026, against direct bookings booked 3 Oct–2 Nov with a sign-up code | New, not in the 26 Oct run |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $249 | 410 leads | CPL $0.61 (diagnostic) | — | Tracked in Discovery | within lines | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $0.67 | Was Monitor, CPL no longer scored |

Client-run, not scored: SP / Willow / Pre-Sales / VIP List / 10-2026 (Sales, paused), created by Nathan Jay Herrington on 2026-10-19, $831 / 14d, 3 purchases, ROAS 0.2x. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: Instagram post: 🔥 𝐒𝐀𝐂𝐑𝐈𝐅𝐈𝐂𝐄 𝐈𝐒 𝐑𝐄𝐐𝐔𝐈𝐑𝐄𝐃 🔥... (Other, paused), created by Live Intentionally Today LIT on 2026-10-15, $10 / 14d, 0 purchases, ROAS —. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Willow / Lead Gen / VIP List / 10-2026 (Lead Gen (MoF), active), created by Nathan Jay Herrington on 2026-10-20, $666 / 30d, 376 leads, CPL $1.77. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Willow / Sales / Top-5 Audiences / 11-2026 (Sales, active), created by Nathan Jay Herrington on 2026-10-28, $705 / 14d, 7 purchases, ROAS 1.2x. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Monthly ROI: July: spend $1,054, 4 Meta-attributed bookings, blended ROAS 3.2x, retargeting ROAS 86.3x, CPL $0.80 on 49 leads · August: spend $1,545, 15 Meta-attributed bookings, blended ROAS 4.8x, retargeting ROAS 25.1x, CPL $1.08 on 144 leads · September: spend $1,304, 27 Meta-attributed bookings, blended ROAS 10.4x, retargeting ROAS 38.2x, CPL $0.63 on 232 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). HiddenGem's BoF drops from Monitor (7.5x) to Review at 3.9x on 6 purchases ($420 in 14 days), frequency 4.5. Discovery row Healthy at 10.3x: $1,003 of giveaway and lead spend against 19 coupon bookings ($10.3k) in Hostaway. Leads $0.61 on 410 leads. The client (Nathan Jay Herrington) now runs four campaigns of their own, listed below and not scored: the new 'SP / Willow / Sales / Top-5 Audiences / 11-2026' at $135/day since 28 Oct reads 1.2x on 7 purchases ($705), the VIP List lead campaign $1.77 on 376 leads, the paused Pre-Sales test 0.2x. Account spend is $245/day, of which HiddenGem's three campaigns are $70. Pixel check: the HG AI CAPI and Hostaway's CAPI both send a server Purchase per booking (80 server Purchase against 44 bookings), so pixel ROAS across the account is roughly doubled; one sender should be switched off.

### Sunapee Stays — AM Charlotte — account Sunapee Stays Ads Account (651114096215889) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $906 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,506; pixel purchase value $2,783 + sign-up promo revenue $0 = $2,783, ROAS 1.8x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $411 from 1 bookings, −77% vs 1 Oct–2 Oct ($1,774 from 6 bookings) · promo codes: not tracked by ownerrez.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $140 | 1 purchases | ROAS 4.2x | 2.69 | Under gate | CPC $0.79 > $0.62; cost/booking $139.88 > $90 | spend $139.88 < $200 gate; 30d ROAS 9.2x, 5 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $299 | 147 leads | CPL $2.04 (diagnostic) | — | Tracked in Discovery | CPC $0.42 > $0.30; CPM $16.80 > $14.84 | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $2.21 | CPL state retired (28 Oct decision), was Review w/ HG AI; see the Discovery row |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,205 | — | promo ROAS — | — | No promo data | — | $1,205 in 30 days across ToF Discovery Campaign - Giveaway - 06/10/26, MoF - Lead Campaign - Retargeting Engagers; ownerrez does not store promo codes on the booking, so sign-up revenue cannot be measured and the bucket is not scored | New, not in the 26 Oct run |

Monthly ROI: July: spend $939, 16 Meta-attributed bookings, blended ROAS 9.9x, CPL $2.06 on 9 leads · August: spend $1,494, 10 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 25.1x, CPL $2.74 on 112 leads · September: spend $1,495, 14 Meta-attributed bookings, blended ROAS 6.5x, retargeting ROAS 6.7x, CPL $1.64 on 184 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). Leads $2.04 on 147 leads ($299; CPL state retired, was Review). BoF 4.2x on 1 purchase, under the gate ($140). No promo data (OwnerRez) on $1,205 of Discovery spend. Pixel: reclassified this week, the HG AI CAPI sends every booking (42 of 42).

### Green Springs Inn — AM Alicia — account Green Springs Inn (1390516335151357) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $605 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,205; pixel purchase value $2,925 + sign-up promo revenue $13,549 = $16,474, ROAS 13.7x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $1,802 from 4 bookings, −29% vs 1 Oct–2 Oct ($2,531 from 3 bookings) · promo codes: 2 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $904 | 29 promo bookings, $13,549 | promo ROAS 15.0x | — | Healthy | 29 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $904 in 30 days across ToF - Giveaway Traffic Campaign - 07/24/2026, MoF - Lead Campaign/08/28/2026, against direct bookings booked 3 Oct–2 Nov with a sign-up code | New, not in the 26 Oct run |
| BoF - Sales Campaign - Retargeting Website Visitors - 08/28/26 | Retargeting (BoF) | 14d | $141 | 2 purchases | ROAS 5.9x | 3.20 | Under gate | CPC $0.83 > $0.62; freq 3.2 > 3.0 | spend $141.47 < $200 gate; 30d ROAS 9.7x, 7 purchases | Unchanged |
| MoF - Lead Campaign/08/28/2026 | Lead Gen (MoF) | 30d | $299 | 206 leads | CPL $1.45 (diagnostic) | — | Tracked in Discovery | within lines | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $1.81 | CPL state retired (28 Oct decision), was Review w/ HG AI; see the Discovery row |

Monthly ROI: July: spend $1,222, 17 Meta-attributed bookings, blended ROAS 7.8x, retargeting ROAS 14.6x, CPL $5.65 on 8 leads · August: spend $1,247, 23 Meta-attributed bookings, blended ROAS 8.2x, retargeting ROAS 17.1x, CPL $9.09 on 34 leads · September: spend $1,199, 24 Meta-attributed bookings, blended ROAS 8.5x, retargeting ROAS 9.0x, CPL $1.84 on 166 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). Discovery row Healthy at 15.0x: $904 of giveaway and lead spend against 29 coupon bookings ($13.5k) in Hostaway. Leads $1.45 on 206 leads (CPL state retired, was Review week 6). BoF 5.9x on 2 purchases, under the gate ($141).

### The Outpost — AM Anna — account The Outpost Grand Canyon (1530849534802936) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $899 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,207; pixel purchase value $601 + sign-up promo revenue $0 = $601, ROAS 0.5x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $1,339 from 4 bookings, −43% vs 1 Oct–2 Oct ($2,340 from 4 bookings) · promo codes: not tracked by newbook.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 10/08/2026 | Retargeting (BoF) | 14d | $148 | 2 purchases | ROAS 4.1x | 2.24 | Under gate | CPC $0.75 > $0.62; CPM $16.93 > $16.50 | spend $148.04 < $200 gate; 30d ROAS 2.4x, 2 purchases | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $899 | — | promo ROAS — | — | No promo data | — | $899 in 30 days across Insta Discovery Campaign - Giveaway - May 2026, Facebook Discovery Campaign - Giveaway - May 2026; newbook does not store promo codes on the booking, so sign-up revenue cannot be measured and the bucket is not scored | New, not in the 26 Oct run |

Monthly ROI: July: spend $2,182, 1 Meta-attributed bookings, blended ROAS 0.2x, CPL $1.61 on 202 leads · August: spend $1,876, 7 Meta-attributed bookings, blended ROAS 2.1x, CPL $1.71 on 181 leads · September: spend $2,081, 18 Meta-attributed bookings, blended ROAS 3.8x, retargeting ROAS —, CPL $1.80 on 167 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). Only the 10/08 BoF campaign spent in the window ($148, 2 purchases, 4.1x), under the gate; the 08/29 one carries a $10 budget but did not spend. No promo data (Newbook) on $899 of Discovery spend. Pixel check: Purchase capture 35% (17 server Purchase against 49 online bookings), browser never fires Purchase.

### Bison Ridge Retreat — AM Chiara — account Bison Ridge Retreat Ad Account (950241787963535) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $600 over 30 days.

Blended 30d (every HiddenGem campaign): spend $902; pixel purchase value $0 + sign-up promo revenue $0 = $0, ROAS 0.0x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - RT Website Visitors | Retargeting (BoF) | 14d | $71 | 0 purchases | ROAS — | 1.94 | Under gate | within lines | spend $71.11 < $200 gate | Unchanged |
| MoF - Lead Campaign - RT Engagers | Lead Gen (MoF) | 30d | $149 | 70 leads | CPL $2.13 (diagnostic) | — | Tracked in Discovery | CPC $0.44 > $0.30; CPM $17.14 > $14.84 | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $1.95 | CPL state retired (28 Oct decision), was Review w/ HG AI; see the Discovery row |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $749 | — | promo ROAS — | — | No promo data | — | $749 in 30 days across Discovery Campaign - Giveaway - April 16, 2026 - Copy, MoF - Lead Campaign - RT Engagers; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured and the bucket is not scored | New, not in the 26 Oct run |

Monthly ROI: July: spend $924, 9 Meta-attributed bookings, blended ROAS 20.3x, retargeting ROAS —, CPL $1.75 on 23 leads · August: spend $952, 3 Meta-attributed bookings, blended ROAS 8.0x, retargeting ROAS —, CPL $2.47 on 63 leads · September: spend $893, 5 Meta-attributed bookings, blended ROAS 9.3x, retargeting ROAS —, CPL $2.54 on 59 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). Leads $2.13 on 70 leads ($149; CPL state retired, was Review). BoF 0 purchases on $71, under the gate. No promo data on $749 of Discovery spend (no PMS in the platform). Pixel: the server side went silent this week; sheet says browser only.

### Walden Retreats — AM Anna — account Walden Retreats (973261794434226) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $278 over 30 days.

Blended 30d (every HiddenGem campaign): spend $806; pixel purchase value $7,538 + sign-up promo revenue $0 = $7,538, ROAS 9.4x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 06/10/2026 | Retargeting (BoF) | 14d | $141 | 1 purchases | ROAS 5.7x | 2.54 | Under gate | CPC $0.85 > $0.62; CPM $25.09 > $16.50; cost/booking $141.45 > $90 | spend $141.45 < $200 gate; 30d ROAS 29.0x, 10 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 10/06/2026 | Lead Gen (MoF) | 30d | $268 | 207 leads | CPL $1.30 (diagnostic) | — | Tracked in Discovery | CPC $0.40 > $0.30; CPM $19.87 > $14.84 | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $1.29 | CPL state retired (28 Oct decision), was Review w/ HG AI; see the Discovery row |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $546 | — | promo ROAS — | — | No promo data | — | $546 in 30 days across ToF - Giveaway Traffic Campaign - ATX, HTX, DAL, SATX, FTW - 10/05/2026, MoF - Lead Campaign - Retargeting Engagers - 10/06/2026; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured and the bucket is not scored | New, not in the 26 Oct run |

Client-run, not scored: TOF Wedding Leads 10.8.26 (Lead Gen (MoF), active), created by Lindsey Cooke on 2026-10-08, $509 / 30d, 29 leads, CPL $17.56. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: TOF Wedding Leads (alt aud) 10.9.26 (Lead Gen (MoF), paused), created by Lindsey Cooke on 2026-10-09, $31 / 30d, 0 leads, CPL —. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: MOF Wedding Leads 10.27.26 (Lead Gen (MoF), active), created by Lindsey Cooke on 2026-10-27, $28 / 30d, 1 leads, CPL $28.31. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). HiddenGem's leads campaign $1.30 on 207 leads (CPL state retired, was Review); BoF 5.7x on 1 purchase, under the gate ($141). No promo data (ResNexus) on $546. The client's own wedding campaigns are listed below and not scored: 'TOF Wedding Leads 10.8.26' $17.56 on 29 leads and the new 'MOF Wedding Leads 10.27.26' (Lindsey Cooke, $5/day) with 1 lead so far.

### North Star Lodge & Resort — AM Charlotte — account North Star Lodge & Resort Ads (2003562593933799) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $600 over 30 days.

Blended 30d (every HiddenGem campaign): spend $899; pixel purchase value $212 + sign-up promo revenue $0 = $212, ROAS 0.2x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $248 from 4 bookings, −97% vs 1 Oct–2 Oct ($8,399 from 18 bookings) · promo codes: not tracked by cloudbeds.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 09/09/2026 | Retargeting (BoF) | 14d | $70 | 1 purchases | ROAS 3.0x | 2.74 | Under gate | CPC $0.79 > $0.62 | spend $70.45 < $200 gate; 30d ROAS 1.3x, 1 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 10/26/26 | Lead Gen (MoF) | 30d | $34 | 9 leads | CPL $3.79 (diagnostic) | — | Under gate | CPC $0.64 > $0.30; CPM $20.99 > $14.84 | spend $34.13 < $100 gate; 14d CPL $3.79 | New, not in the 26 Oct run |
| MoF - Lead Campaign - Retargeting Engagers - 10/02/26 | Lead Gen (MoF) | 30d | $107 | 1 leads | CPL $106.66 (diagnostic) | — | Tracked in Discovery | CPC $0.91 > $0.30; CPM $24.90 > $14.84 | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $38.45 | CPL state retired (28 Oct decision), was Flag to Shawal; see the Discovery row |
| Discovery bucket (3 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $741 | — | promo ROAS — | — | No promo data | — | $741 in 30 days across ToF - Giveaway Traffic Campaign - 09/09/2002, MoF - Lead Campaign - Retargeting Engagers - 10/02/26, MoF - Lead Campaign - Retargeting Engagers - 10/26/26; cloudbeds does not store promo codes on the booking, so sign-up revenue cannot be measured and the bucket is not scored | New, not in the 26 Oct run |

Monthly ROI: September: spend $580, 0 Meta-attributed bookings, blended ROAS —. Note in the September file: Newly launched campaigns — $579.92 spent, no revenue from ads yet. Revenue shown is from the client reporting sheet; no booking-level data this month.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). Last week's tracking Flag clears on a technicality: the 10/02 lead campaign now has 1 lead on $107 ($106.66 CPL), so the zero-lead check no longer fires, and a second lead campaign (10/26, $34, 9 leads at $3.79) has started. BoF under the gate ($70, 1 purchase). No promo data (Cloudbeds; see the Asheville note on where Cloudbeds coupons land). Pixel check this week: the Cloudbeds booking engine fired the account pixel once all week and the HG BM pixel is dead since 26 Oct, Purchase capture 37% of 94 online bookings and the HG AI send looks stalled since 3 Oct, so the BoF has little to optimise on until the engine pixel is reinstalled (Charlotte / Leshan).

### American River Resort — AM Nicole — account American River Resort (953162737054331) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $408 over 30 days.

Blended 30d (every HiddenGem campaign): spend $679; pixel purchase value $0 + sign-up promo revenue $0 = $0, ROAS 0.0x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $679 | — | promo ROAS — | — | No promo data | — | $679 in 30 days across ToF - Giveaway Traffic Campaign - SAC/SJ/SF (paused), MoF - Lead Campaign - Retargeting Engagers (paused); no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured and the bucket is not scored | New, not in the 26 Oct run |

Paused in window, not scored: MoF - Lead Campaign - Retargeting Engagers (Lead Gen (MoF)), $271 / 30d, 204 leads, CPL $1.33. Live campaigns only are scored (decision 2026-09-23).

Monthly ROI: July: spend $1,544, 4 Meta-attributed bookings, blended ROAS 1.1x · August: spend $1,529, 3 Meta-attributed bookings, blended ROAS 1.4x, CPL $18.30 on 30 leads · September: spend $1,453, 0 Meta-attributed bookings, blended ROAS —, CPL $1.48 on 377 leads. Note in the September file: We had no promo code usages this month.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). Ads off since 15 Oct: paused, not offboarded. The lead campaign's trailing spend ($271, 204 leads at $1.33) is listed as paused and nothing is scored; the Discovery row shows $679 of trailing 30-day spend with no promo data (Arctic PMS, not in the platform).

### Glasscombe — AM Charlotte — account Glasscombe (2030318804465316) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $390 over 30 days.

Blended 30d (every HiddenGem campaign): spend $576; pixel purchase value $0 + sign-up promo revenue $0 = $0, ROAS 0.0x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $0 from 0 bookings, −100% vs 1 Oct–2 Oct ($396 from 1 bookings) · promo codes: not tracked by cloudbeds.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers -  10/09/26 | Lead Gen (MoF) | 30d | $93 | 315 leads | CPL $0.30 (diagnostic) | — | Under gate | within lines | spend $93.23 < $100 gate; 14d CPL $0.26 | Unchanged |
| BoF - Sales Campaign - Retargeting Website Visitors - 10/09/26. | Retargeting (BoF) | 14d | $69 | 0 purchases | ROAS — | 1.83 | Under gate | within lines | spend $69.30 < $200 gate | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $483 | — | promo ROAS — | — | No promo data | — | $483 in 30 days across ToF - Giveaway Traffic Campaign - UK, MoF - Lead Campaign - Retargeting Engagers -  10/09/26; cloudbeds does not store promo codes on the booking, so sign-up revenue cannot be measured and the bucket is not scored | New, not in the 26 Oct run |

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). Both under the gate: leads $0.30 on 315 leads ($93), BoF 0 purchases on $69. No promo data (Cloudbeds) on $483. The platform's month-to-date reads $0 after two days of November.

### Cabin Collective — AM Chiara — account Cabin Collective (2194562394139883) — live read

ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: $111 over 30 days.

Blended 30d (every HiddenGem campaign): spend $331; pixel purchase value $8,956 + sign-up promo revenue $0 = $8,956, ROAS 27.0x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–2 Nov): direct revenue $5,061 from 2 bookings, −35% vs 1 Oct–2 Oct ($7,755 from 4 bookings) · promo codes: not tracked by ownerrez.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 10/20/26 | Retargeting (BoF) | 14d | $109 | 6 purchases | ROAS 82.2x | 2.12 | Under gate | CPM $16.75 > $16.50 | spend $108.89 < $200 gate; 30d ROAS 82.2x, 6 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 10/20/26 | Lead Gen (MoF) | 30d | $111 | 89 leads | CPL $1.25 (diagnostic) | — | Tracked in Discovery | within lines | CPL is a diagnostic only; the ROAS state is on this client's Discovery row; 14d CPL $1.25 | Was Under gate, CPL no longer scored |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $223 | — | promo ROAS — | — | No promo data | — | $223 in 30 days across ToF - Giveaway Traffic Campaign - [TX, OK, AR] - 10/20/26, MoF - Lead Campaign - Retargeting Engagers - 10/20/26; ownerrez does not store promo codes on the booking, so sign-up revenue cannot be measured and the bucket is not scored | New, not in the 26 Oct run |

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 26 Oct). Leads cross the $100 gate at $1.25 on 89 leads ($111), now Tracked in Discovery; BoF 82x on 6 purchases but under the gate ($109). No promo data (OwnerRez) on $223. Master sheet Status still Not Live although the account has spent since 20 Oct.

## Footer

- Windows: Lead Gen last 30 days, Sales/Retargeting last 14 days (live). CSV accounts use the export period 2026-10-19 to 2026-10-25 (7 days) and are provisional.
- Gates: $100 Lead Gen, $200 Sales/Retargeting. Campaigns under the gate are listed but not judged.
- Classification: by campaign objective (OUTCOME_LEADS → Lead Gen; OUTCOME_SALES → Sales, split into Retargeting (BoF) or MoF lookalike by name; OUTCOME_TRAFFIC / OUTCOME_ENGAGEMENT → ToF, not scored). CSV accounts have no objective column, so classification there is by name.
- Prospecting (MoF lookalike) sales campaigns are scored on the Retargeting ROAS bands because they optimise for purchases. The Benchmarks doc has no separate band for prospecting; Dustin floated a 3x floor on 28 Oct, not yet adopted.
- Discovery bucket (from 2026-10-30, Meta Ads Strategy 2026-10-28): one row per client combining the 30-day spend of every HiddenGem ToF (giveaway, keyword) and Lead Gen campaign that spent in the window, paused ones included, against the 30-day revenue of direct bookings carrying a sign-up promo code (WELCOME*, ENJOY*, SIGNUP*, GIVEAWAY*) from the HiddenGem AI platform (pms_mtd.sql). Other codes (VIP, WELCOMEBACK, RETURNING, EARLY BIRD, agent or influencer codes) are listed in the row but not counted. Hostaway stores only a coupon id, so every coupon booking counts there. Scored on the Sales ROAS bands with a $200 gate until the Benchmarks doc gets a Discovery band. Clients on a PMS that stores no promo code (Hospitable, Cloudbeds, OwnerRez, Newbook, Lodgify, Uplisting) are marked No promo data and not scored.
- Lead Gen CPL is no longer a state (28 Oct). It stays in the Governing metric column as a diagnostic, the Lead Gen investigate lines still apply, and the one direct flag left is the tracking check: spend over the $100 gate with zero leads. Rows that were Flag or Review on CPL last week read "CPL state retired" in the diff rather than Fixed.
- Blended 30d line per client: 30-day spend of every HiddenGem campaign against pixel purchase value (Sales rows, spend × ROAS) plus sign-up promo revenue. Not de-duplicated; it is the blended view Dustin asked to keep alongside the buckets, so a budget shift between buckets that lowers the blend is visible.
- Data path: Marketing API v21.0 insights at campaign level through `scripts/pull-campaign-insights.mts` (purchases = omni_purchase, leads = lead, ROAS = purchase_roas, link clicks = inline_link_clicks), the same fields the claude.ai connector exposed. The connector is no longer used for this report (Shawal, 2026-10-19).
- CTR on live rows is Meta's CTR (all clicks), not link CTR. The doc's click-rate lines are probably link CTR, so treat the CTR diagnostic as indicative.
- Frequency and cost per booking are diagnostics only and do not change the state (decision 2026-09-21). From 2026-10-06 (Shawal) every Sales / Retargeting row shows its frequency, and any value above 5.0 is marked ⚠️ in that column and listed in the Frequency watch section; CSV rows use impressions / reach summed over ad sets, which overstates frequency where ad sets overlap.
- Only campaigns live (ACTIVE) at run time are scored. Paused campaigns that spent inside the window are listed per client as "Paused in window" and never enter Action needed or the counts (decision 2026-09-23).
- Client-run campaigns (created by a non-HiddenGem login per the account activity log, listed under the client, never scored): Selah Place: SP / Willow / Pre-Sales / VIP List / 10-2026 (Nathan Jay Herrington), Instagram post: 🔥 𝐒𝐀𝐂𝐑𝐈𝐅𝐈𝐂𝐄 𝐈𝐒 𝐑𝐄𝐐𝐔𝐈𝐑𝐄𝐃 🔥... (Live Intentionally Today LIT), SP / Willow / Lead Gen / VIP List / 10-2026 (Nathan Jay Herrington), SP / Willow / Sales / Top-5 Audiences / 11-2026 (Nathan Jay Herrington); Walden Retreats: TOF Wedding Leads 10.8.26 (Lindsey Cooke), TOF Wedding Leads (alt aud) 10.9.26 (Lindsey Cooke), MOF Wedding Leads 10.27.26 (Lindsey Cooke). Creators are known for campaigns created in the last 180 days; older campaigns are scored as usual.
- Unclassified campaigns: none.
- Previous report: 2026-10-26-client-benchmark.csv. Diff joined on campaign_id for live rows and client + campaign name for CSV rows. Diff counts: 28 new, 1 still open, 1 fixed, 35 unchanged, 0 removed.
- Scope changes vs 26 Oct: none (same 24 accounts); Sunapee Stays kept in scope (CRM Meta Ads column reads Basic since 19 Oct; kept as Advanced at Shawal's request (2026-10-26)). Advanced in the CRM but with no ad account mapping in PROJECT.md section 5, not scored: Treetop Hideaways (AM Kristal), Casey Key Resort (AM Alicia), Arca Roatan (AM Anna), Gooseberry Lodges (AM Alicia), Dunya Camp (AM Chiara), Nine Pines Retreat (AM Nicole), Lundy Farm (AM Charlotte). Gooseberry Lodges also appeared on the Master Meta Ads sheet this week, still with no account ID.
- HG AI reports read from `HG AI Reports/` at the project root, dated since the previous run: none.
- Selah Place's prospecting campaign (paused this week) is named with pipes in Meta ("SP | Prospecting Test | LAL + Interests x Creative | 09-2026"); shown here with slashes.
- Meeting notes: every "Meta Ads Strategy", "Meta Ads Sync" or "Meta Ads x HiddenGem AI Sync" calendar event since the previous run that has a "Notes by Gemini" attachment, read via Drive. Client names are matched with an alias list (Flow Home = FLOHOM, Tabber / Tipik Falls / Debug Falls = Tàberg Falls, Sailor Place = Selah Place, Stay on 38 = Stay On 30A, Ashwood River Cabins = Asheville River Cabins).
- This month line: direct booking revenue by booking date from the HiddenGem AI platform (pms_bookings, platform direct/OTA rules, tenants on a shared PMS account narrowed to their own properties), month to date at the run date, against the same day span of the previous month. Promo codes come from the booking payload: Guesty stores the code, Hostaway only a coupon id (counted, no names), Hospitable and Cloudbeds nothing. Pulled with pms_mtd.sql through the Supabase connector. Clients without a PMS connection on the platform show no figures.
- Monthly ROI context from `Monthly ROI data/` (July 2026, August 2026, September 2026). Revenue there comes from the Client Performance Tracking sheet, not the pixel, so its ROAS is not comparable to the pixel ROAS above.
