# Client Benchmark Review (advanced setups) — 2026-11-16

Run: 16 November 2026 (Monday), ninth run, compared against 2026-11-09-client-benchmark.csv. Live reads through the Meta Marketing API with the HG - ROI Dashboard system user, the standing data path (`scripts/pull-campaign-insights.mts`, 08:44 to 08:50 PT); every account read live and the CSV export 2026-10-19 to 2026-10-25 was not needed for scoring. Scope: clients marked **Advanced** in the CRM "Meta Ads" column (Clients - Onboarding tab), re-read today: 32 clients, 26 with an ad account. Bison Ridge Retreat reads Basic since 12 Nov and drops out; Gooseberry Lodges, Dunya Camp and Arca Boutique Hotel were mapped today (Shawal), so their rows are new; Sunapee Stays reads Advanced again. 6 Advanced clients in the CRM have no ad account shared with HiddenGem yet (The Preserve and Kimpton Mas Olas Resort among them). Scoring as since 4 Nov: Sales-objective campaigns only (Retargeting, Prospecting, Sales, on 14-day pixel ROAS); Lead Gen rows and the Discovery bucket row stay in each client's table for context with no state. Changes made in the accounts since last Monday come from each account's Meta activity log (most of the 12 and 13 Nov changes were Shawal's, under his second profile John Martin), and ROAS is read against this week's pixel check where duplicate Purchases inflate it or missing Purchases deflate it.

| Advanced clients | Live reads | From CSV | Rows scored | Under spend gate | Flag to Shawal | Review w/ HG AI | Monitor | Healthy | Scale w/ HG AI | Frequency over 5 | Not scored (lead gen) | Not scored (discovery) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 26 (+6 unmapped) | 26 | 0 | 21 | 15 | 1 | 2 | 3 | 8 | 7 | 2 | 22 | 23 |

States come from the Decision Making table in the Benchmarks doc and apply to Sales-objective campaigns only (Shawal, 4 Nov 2026): Retargeting, Prospecting and Sales campaigns on 14-day pixel ROAS with a $200 gate. Bands: above 15x Scale, 8–15x Healthy, 5–8x Monitor, 2–5x Review, under 2x or zero purchases Flag, inclusive on the lower bound. Lead Gen rows (leads, CPL) and the Discovery bucket row (giveaway + lead spend against 30-day sign-up promo-code revenue from the PMS) are listed under each client for context and carry no state.

## Weekly Meta Ads meetings since last run (Notes by Gemini)

Source: "Notes by Gemini" docs attached to the calendar events, read via Drive. Summary, decisions and next steps as Gemini wrote them; client-specific sentences are pulled into each client's section below. Transcript not used.

### Meta Ads Sync — 2026-11-11 — doc `1Nf-776jbXwMmez7LsipGwzQ0Ft8U-dAGpe7mfNkJiu8`

Meta campaign strategy aligned with client tiering and winter content optimization.

Meta Ads Campaign Structure

Dustin presented a 3-tier Meta ads strategy focusing on discovery, consideration, and conversion campaigns. Hidden Gem artificial intelligence tracks attribution across campaigns to evaluate return on ad spend.

Client Tiering and Access

Clients denying property management system access will transition to the basic tier. Advanced clients require active scaling and master ads sheet setup.

The Preserve Winter Content

The team reviewed winter content optimization and agreed to protect email deliverability. High-definition 4K footage was evaluated for upcoming promotional materials.

Decisions:
- Policy for custom client event requests The team actively debated whether to accommodate custom client marketing requests or establish strict process boundaries upfront without reaching a final agreement.
- Three-campaign Meta ads funnel structure The team locked in a three-campaign Meta ads funnel approach consisting of top-of-funnel discovery, consideration, and purchase retargeting.
- Fifty-fifty attribution credit for booking overlaps The team agreed to use a fifty-fifty credit split for direct bookings that overlap between discovery and retargeting campaigns.
- Master ads sheet for client tracking The team established a master ads sheet to track client PMS platforms, connection status, match rates, return on ad spend goals, and budget ranges.
- Basic Meta ads management for restricted clients The team decided to move clients who deny PMS access to basic Meta ads management without advanced PMS tracking.
- Client budget scaling and tracking criteria The team aligned to prioritize budget increase discussions with clients maintaining over a 10x return on ad spend and track client goals in a master sheet.

Next steps:
- [Alicia Morin] Send the client email: containing the onboarding form, cookie policy, booking site script, website link issues, and privacy policy line removal update to follow up with them.
- [Alicia Morin] Check the events calendar: to verify the exact timing of the Santa's brunch for the Preserve client.
- [Alicia Morin] Meet with Shawal: to determine where to increase the ad spend for Fireflies to ensure strong performance through November.
- [Shawal Nazir] Create the master ads sheet: for advanced meta ads clients to track the property management system, booking engine, connection status, match rate, and return on ad spend goals or budget ranges.
- [Shawal Nazir] Verify tracking setup: during onboarding for new clients by checking property management system or customer relationship management connections, scraping websites with Claude, and evaluating integration compatibility.
- [Shawal Nazir] Lead building the master tracking sheet: to record client setup details including PMS integration status, API connection match rates, and campaign overlap differentiation.
- [Leshan Patterson] Restore the booking attribution view layout: to match the previous version in the hidden artificial intelligence tool for quick data analysis.
- [Leshan Patterson] Update the booking attribution platform interface: to make viewing campaign overlap data more intuitive for users without requiring excessive clicks.
- [Makenna Moran] Send additional winter content: to Aiden for optimization while removing irrelevant warm-weather media assets for the Preserve client.
- [Makenna Moran] Create lead campaign ads: to reach a total of 5 or 6 options for the upcoming campaign following the next meeting.
- [Makenna Moran] Meet with Aiden: to discuss winter content strategy for the preserve.
- [Gillian Conley] Address scope boundaries: on the next call with Paul, Sean, and the team to clarify standard operational processes.
- [Dustin Baker] Inform Paul on the upcoming call: that initial ad spend during Black Friday will experience higher competition and lower returns.

### Meta Ads Strategy — 2026-11-11 — doc `1hD7LB51qRrElHamNsw7yOW20Zd-cOs5a5LJvceuaQdU`

Client payments and revenue targets reviewed with ad attribution structures established and ROAS targets set.

Client Payments and Scale

Outstanding payments were reviewed alongside capacity concerns for new clients. Major clients like the Preserve and Kimpton Masalas generate significantly larger annual revenues than others.

Meta Ads and ROAS

Master sheet organization and attribution setups were discussed to improve weekly ad operations. A 5x minimum return on ad spend bar was established for scaling client campaigns.

Reporting and Pixel Setup

Weekly report visibility was addressed with proposed Monday morning link distributions. Pixel setup complexities were resolved by prioritizing business manager access during onboarding calls.

Decisions:
- Prioritization of The Preserve account setup The team aligned to prioritize The Preserve as an all-hands-on-deck account for maximal meta ads tracking and attribution.
- Initiation of weekly ad ops meetings The participants agreed to begin meeting weekly for ad ops to evaluate performance together.
- Two-week timeline for campaign launch The team established a target two-week timeline for creating campaigns and completing integrations.

Next steps:
- [Dustin Baker] Update the master tracking sheet: with the latest client meta ads setup status and performance estimates to maintain accurate records.
- [Dustin Baker] Review the client reporting sheet weekly: by preparing a short version for each client to discuss during weekly ad ops meetings.
- [Leshan Patterson] Prioritize the preserve client setup: to ensure they have all necessary meta ads performance tracking, attribution, and decision-making resources.
- [Unassigned] Gather ad spend ranges from clients: over the next 2 to 3 months during client conversations to establish proper expectations for advanced setups.
- [Gillian Conley] Sync with the team: on the business management system setup soon.

## Action needed

Sales-objective campaigns only (Retargeting, Prospecting, Sales; Shawal, 4 Nov 2026). Flag to Shawal before Review w/ HG AI, highest spend first.

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| Little River Landing | Makenna | BoF - Sales Campaign - Retargeting Website Visitors - 09/16/2026 | Retargeting (BoF) | $220 / 14d | ROAS 1.4x | Flag to Shawal | Still open, week 2 |
| Endless Stays | Nicole | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $961 / 14d | ROAS 4.1x | Review w/ HG AI | Still open, week 7 (was Flag to Shawal) |
| FLOHOM | Makenna | [Myrtle Beach] MoF - Lookalike Sales Campaign - 09/17/26 | Prospecting (MoF lookalike) | $282 / 14d | ROAS 3.3x | Review w/ HG AI | New flag, was Healthy |

## Scale candidates

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| Stay On 30A | Charlotte | BoF - Sales Campaign - RT Website Visitors - 07/13/26 | Retargeting (BoF) | $2,062 / 14d | ROAS 15.3x | Scale w/ HG AI | Was Healthy |
| Paradise Pointe | Makenna | MoF - LoL Sales Campaign - 09/28/26 | Prospecting (MoF lookalike) | $864 / 14d | ROAS 20.8x | Scale w/ HG AI | Unchanged |
| Starlight Haven Weiss Lake | Charlotte | Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | $644 / 14d | ROAS 17.6x | Scale w/ HG AI | Unchanged |
| Asheville River Cabins | Charlotte | MoF - Broad - 06/08/26 | Prospecting (MoF lookalike) | $556 / 14d | ROAS 26.2x | Scale w/ HG AI | Unchanged |
| Selah Place | Alicia | BoF-Website Retarget Campaign - 07/24/2026 | Retargeting (BoF) | $412 / 14d | ROAS 17.0x | Scale w/ HG AI | Was Monitor |
| Starlight Haven Hot Springs | Charlotte | Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | $275 / 14d | ROAS 18.3x | Scale w/ HG AI | Unchanged |
| Ridge & Falls | Makenna | BoF - Sales Campaign - Retargeting Website Visitors - 09/01/26 | Retargeting (BoF) | $211 / 14d | ROAS 22.9x | Scale w/ HG AI | Unchanged |

## Frequency watch (Sales / Retargeting above 5)

Sales, Retargeting and MoF-lookalike campaigns whose 14-day frequency is above 5.0 (Shawal, 6 Oct 2026). Frequency does not change the ROAS state; this is the list to refresh creative or widen the audience on. The diagnostics column still notes anything above 3.0.

| Client | AM | Campaign | Type | Frequency | Spend / window | Governing metric | State |
|---|---|---|---|---|---|---|---|
| Paradise Pointe | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 5.45 | $681 / 14d | ROAS 13.2x | Healthy |
| Ridge & Falls | Makenna | BoF - Sales Campaign - Retargeting Website Visitors - 09/01/26 | Retargeting (BoF) | 5.34 | $211 / 14d | ROAS 22.9x | Scale w/ HG AI |

## Per client, ordered by scored MoF + BoF spend

### Stay On 30A — AM Charlotte — account Stay on 30a Ads (25640434272252212) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $3,001 over 30 days.

Blended 30d (every HiddenGem campaign): spend $15,033; pixel purchase value $145,306 + sign-up promo revenue $57,929 = $203,235, ROAS 13.5x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $166,981 from 58 bookings, +12% vs 1 Oct–16 Oct ($149,007 from 56 bookings) · promo codes: 29 uses (EARLY BIRD DIRECT ×14, VIP100 ×9, WELCOME100 ×8, WELCOMEBACK15 ×2, ESCAPE30A ×1, RETURNINGGUEST ×1, SNOWBIRD30A ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Sales Campaign - HiddenGem Pixel LoL - 07/17/26 | Prospecting (MoF lookalike) | 14d | $2,743 | 6 purchases | ROAS 11.6x | 1.76 | Healthy | CPC $0.96 > $0.62; CPM $24.08 > $16.50; cost/booking $457.23 > $90 | 30d ROAS 13.5x, 11 purchases | Unchanged |
| BoF - Sales Campaign - RT Website Visitors - 07/13/26 | Retargeting (BoF) | 14d | $2,062 | 6 purchases | ROAS 15.3x | 4.32 | Scale w/ HG AI | CPC $1.82 > $0.62; CPM $32.40 > $16.50; cost/booking $343.73 > $90; freq 4.3 > 3.0 | 30d ROAS 14.1x, 16 purchases | Was Healthy |
| MoF - Lead Campaign - RT Engagers - 07/16/26 | Lead Gen (MoF) | 30d | $1,499 | 939 leads | CPL $1.60 (diagnostic) | — | Not scored (lead gen) | CPC $0.44 > $0.30; CPM $40.47 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.61 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $4,499 | 14 promo bookings, $57,929 | promo ROAS 12.9x | — | Not scored (discovery) | WELCOME100 ×14 $57,929; not counted (not sign-up codes): EARLY BIRD DIRECT ×31 $183,504, VIP100 ×14 $46,893, RETURNINGGUEST ×2 $17,486, SNOWBIRD30A ×2 $8,714, WELCOMEBACK15 ×3 $6,991, ESCAPE30A ×1 $1,196 | $4,499 in 30 days across ToF - Giveaway Traffic Campaign - 02/05/2026, MoF - Lead Campaign - RT Engagers - 07/16/26, against direct bookings booked 17 Oct–16 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $6,407, 67 Meta-attributed bookings, blended ROAS 32.3x, retargeting ROAS 14.6x, CPL $1.24 on 583 leads · August: spend $12,420, 85 Meta-attributed bookings, blended ROAS 17.8x, retargeting ROAS 15.5x, CPL $2.58 on 594 leads · September: spend $12,606, 91 Meta-attributed bookings, blended ROAS 24.4x, retargeting ROAS 23.1x, CPL $1.52 on 1001 leads · October: spend $15,161, 51 Meta-attributed bookings, blended ROAS 15.5x, retargeting ROAS 17.2x, CPL $1.47 on 1036 leads.

Meeting notes (Meta Ads Strategy 2026-11-11): Dustin Baker emphasized setting up stay on 3A attribution for major spenders to improve weekly ad operations meetings by focusing on return on ad spend for discovery, retargeting, and lookalike prospecting campaigns rather than cost per lead.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF moves up from Healthy (14.7x) to Scale at 15.3x on 6 purchases ($2,062 in 14 days), just over the Scale line, frequency 4.3. The LoL lookalike holds Healthy at 11.6x on 6 purchases ($2,743; 13.9x last week). Budget unchanged at $500/day. Direct revenue month to date $167.0k, +12% on the same days of October; EARLY BIRD DIRECT ×14, VIP100 ×9 and WELCOME100 ×8 carry the coded bookings.

### Tàberg Falls — AM Alicia — account Táberg Falls (827872700004659) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,692 over 30 days.

Blended 30d (every HiddenGem campaign): spend $7,814; pixel purchase value $33,642 + sign-up promo revenue $2,008 = $35,650, ROAS 4.6x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $31,662 from 19 bookings, −20% vs 1 Oct–16 Oct ($39,483 from 27 bookings) · promo codes: 1 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Website Retargeting Campaign - 08/21/2026 | Retargeting (BoF) | 14d | $1,392 | 4 purchases | ROAS 5.3x | 3.19 | Monitor | CPC $0.80 > $0.62; CPM $23.02 > $16.50; cost/booking $347.92 > $90; freq 3.2 > 3.0 | 30d ROAS 7.6x, 10 purchases | Unchanged |
| MoF - Lookalike Sales Campaign - 08/21/2026 | Prospecting (MoF lookalike) | 14d | $1,381 | 8 purchases | ROAS 10.0x | 1.63 | Healthy | CPM $19.28 > $16.50; cost/booking $172.58 > $90 | 30d ROAS 6.7x, 9 purchases | Was Monitor |
| MoF - Leads Campaign - 06/19/26 | Lead Gen (MoF) | 30d | $1,327 | 2304 leads | CPL $0.58 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.55 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $3,019 | 1 promo bookings, $2,008 | promo ROAS 0.7x | — | Not scored (discovery) | 1 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $3,019 in 30 days across MoF - Leads Campaign - 06/19/26, ToF - Giveaway Campaign - 07/08/2026, against direct bookings booked 17 Oct–16 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Paused in window, not scored: MoF - Broad (Acquire new customers) - 09/28/2026 (Prospecting (MoF lookalike)), $114 / 14d, 0 purchases, ROAS —. Live campaigns only are scored (decision 2026-09-23).

Monthly ROI: July: spend $11,739, 80 Meta-attributed bookings, blended ROAS 9.5x, retargeting ROAS 15.8x, CPL $0.67 on 2320 leads · August: spend $11,259, 48 Meta-attributed bookings, blended ROAS 6.3x, retargeting ROAS 8.0x, CPL $0.46 on 4015 leads · September: spend $10,800, 42 Meta-attributed bookings, blended ROAS 5.6x, retargeting ROAS 7.1x, CPL $0.55 on 3261 leads · October: spend $8,391, 34 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 8.3x, CPL $0.58 on 2779 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). Lookalike up from Monitor (6.0x) to Healthy at 10.0x on 8 purchases ($1,381), its third week at $100/day. BoF slips inside Monitor from 7.3x to 5.3x on 4 purchases ($1,392), frequency 3.2; one more week down puts it in Review. Discovery read (context only) 0.7x: $3,019 of giveaway and lead spend in 30 days against one Hostaway coupon booking ($2,008), so last week's question for Alicia (does the sign-up code work on the booking engine?) is still open. Direct revenue month to date −20% on October.

### Endless Stays — AM Nicole — account Endless Stays (896372356081479) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $2,203 over 30 days.

Blended 30d (every HiddenGem campaign): spend $6,009; pixel purchase value $8,625 + sign-up promo revenue $0 = $8,625, ROAS 1.4x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $39,839 from 19 bookings, +105% vs 1 Oct–16 Oct ($19,402 from 12 bookings) · promo codes: not tracked by hospitable.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $961 | 2 purchases | ROAS 4.1x | 2.43 | Review w/ HG AI | CPC $0.74 > $0.62; CPM $21.01 > $16.50; cost/booking $480.62 > $90 | 30d ROAS 3.9x, 3 purchases | Still open, week 7 (was Flag to Shawal) |
| MoF - Lookalike Sales Campaign - 11/13/2026 | Prospecting (MoF lookalike) | 14d | $140 | 0 purchases | ROAS — | 1.37 | Under gate | CPC $0.77 > $0.62; CPM $22.20 > $16.50 | spend $139.82 < $200 gate | New, not in the 9 Nov run |
| MoF Lead Campaign - Retargeting Engagers - 09/09/2026 | Lead Gen (MoF) | 30d | $1,478 | 1394 leads | CPL $1.06 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.11 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $3,682 | — | promo ROAS — | — | Not scored (discovery) | — | $3,682 in 30 days across ToF - Giveaway Traffic Campaign - AZ, FL, VA, PA, TN, MoF Lead Campaign - Retargeting Engagers - 09/09/2026; hospitable does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $1,534, 9 Meta-attributed bookings, blended ROAS 16.0x · August: spend $1,553, 10 Meta-attributed bookings, blended ROAS 11.6x, retargeting ROAS 38.8x, CPL $9.73 on 26 leads · September: spend $2,539, 6 Meta-attributed bookings, blended ROAS 2.9x, retargeting ROAS 4.7x, CPL $1.05 on 532 leads · October: spend $6,184, 5 Meta-attributed bookings, blended ROAS 2.6x, retargeting ROAS 3.3x, CPL $0.89 on 1715 leads.

Meeting notes (Meta Ads Sync 2026-11-11): Review of Existing Client Budgets and Account Adjustments: Dustin Baker and Ananya Arora reviewed active client ad accounts and budgets, noting that Endless Days increased their spend to approximately $100 daily, prompting a move to the advanced tier, and Asheville River Cabins was bumped from $30 to $50 daily by Dustin Baker after achieving strong return on ad spend results over several months.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF eases from Flag (0 purchases on $1,034) to Review at 4.1x on 2 purchases ($961 in 14 days), open seven weeks. On 13 Nov Shawal cut BoF from $75 to $50 and moved $50/day into a new lookalike (0 purchases on $140 in three days, under the gate). Month-to-date direct revenue is $39.8k, +105% on October (19 bookings), while the pixel's Purchases arrive server-side only (HG AI CAPI), so attribution, not demand, is the open question.

### AwayFrames — AM Alicia — account Awayframes Ad Account (2471256056603833) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,306 over 30 days.

Blended 30d (every HiddenGem campaign): spend $4,455; pixel purchase value $20,962 + sign-up promo revenue $0 = $20,962, ROAS 4.7x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $26,107 from 20 bookings, +222% vs 1 Oct–16 Oct ($8,097 from 9 bookings) · promo codes: 0 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors 07/31/2026 | Retargeting (BoF) | 14d | $698 | 7 purchases | ROAS 10.2x | 4.51 | Healthy | CPC $1.32 > $0.62; CPM $21.25 > $16.50; cost/booking $99.71 > $90; freq 4.5 > 3.0 | 30d ROAS 13.4x, 14 purchases | Was Monitor |
| MoF - Lookalike Sales Campaign - 10/29/2026 | Prospecting (MoF lookalike) | 14d | $686 | 5 purchases | ROAS 9.3x | 1.33 | Healthy | CPC $0.68 > $0.62; cost/booking $137.18 > $90 | 30d ROAS 7.2x, 5 purchases | Fixed, was Flag to Shawal |
| MoF - Lead Campaign - Retargeting Engagers 07/31/2026 | Lead Gen (MoF) | 30d | $1,176 | 798 leads | CPL $1.47 (diagnostic) | — | Not scored (lead gen) | CPC $0.32 > $0.30 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.36 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $2,482 | 0 promo bookings, $0 | promo ROAS 0.0x | — | Not scored (discovery) | 0 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $2,482 in 30 days across ToF - Giveaway Traffic Campaign - 07/31/2026, MoF - Lead Campaign - Retargeting Engagers 07/31/2026, against direct bookings booked 17 Oct–16 Nov with a sign-up code; no sign-up promo bookings in 30 days; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $923, 9 Meta-attributed bookings, blended ROAS 18.6x, CPL $2.44 on 2 leads · August: spend $869, 8 Meta-attributed bookings, blended ROAS 21.8x, retargeting ROAS 27.0x, CPL $2.68 on 58 leads · September: spend $895, 7 Meta-attributed bookings, blended ROAS 11.1x, retargeting ROAS 4.9x, CPL $1.83 on 82 leads · October: spend $1,898, 20 Meta-attributed bookings, blended ROAS 9.9x, retargeting ROAS 15.3x, CPL $1.56 on 316 leads.

Meeting notes (Meta Ads Sync 2026-11-11): Client Tiering and Budget Scaling Based on Performance: Dustin Baker distinguished between basic clients using a set-and-forget approach with $30 to $50 daily budgets, such as Oak and Ember, and advanced clients where the team actively scales Meta ads to maximize business growth, such as Glasscom and Waveframes.
Meeting notes (Meta Ads Strategy 2026-11-11): Furthermore, Dustin Baker and Gillian Conley reviewed specific return on ad spend targets for various clients, such as a 7x return for Away Frames and Stay Saluted, and a 5x return for Tree Tops, Lodge, and others, with Dustin Baker deciding to set a 5x minimum bar for scaling despite higher inventory availability.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). The 10/29 lookalike is Fixed: from Flag (1.9x) to Healthy at 9.3x on 5 purchases ($686), its third week. BoF up from Monitor (7.3x) to Healthy at 10.2x on 7 purchases ($698), frequency 4.5. Both clear the 7x target set for Awayframes at the 11 Nov Strategy meeting. Direct revenue month to date $26.1k, +222% on October. Discovery read 0.0x: no Hostaway coupon booking in 30 days on $2,482 of giveaway and lead spend.

### Paradise Pointe — AM Makenna — account Paradise Pointe Ads (1585826092078255) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $803 over 30 days.

Blended 30d (every HiddenGem campaign): spend $4,735; pixel purchase value $54,473 + sign-up promo revenue $80,119 = $134,592, ROAS 28.4x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $87,907 from 86 bookings, +22% vs 1 Oct–16 Oct ($72,054 from 73 bookings) · promo codes: 38 uses (WELCOME100 ×37, WELCOMEBACK10 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $681 | 9 purchases | ROAS 13.2x | 5.45 ⚠️ > 5 | Healthy | CPC $0.96 > $0.62; freq 5.4 > 3.0 | 30d ROAS 17.9x, 24 purchases | Unchanged |
| MoF - LoL Sales Campaign - 09/28/26 | Prospecting (MoF lookalike) | 14d | $864 | 15 purchases | ROAS 20.8x | 2.08 | Scale w/ HG AI | within lines | 30d ROAS 16.6x, 27 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $768 | 700 leads | CPL $1.10 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.14 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,571 | 72 promo bookings, $80,119 | promo ROAS 51.0x | — | Not scored (discovery) | WELCOME100 ×71 $78,182, WELCOME10 ×1 $1,937; not counted (not sign-up codes): VIP100 ×1 $1,544, WELCOMEBACK10 ×1 $1,111 | $1,571 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Giveaway Traffic Campaign, against direct bookings booked 17 Oct–16 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $2,237, 74 Meta-attributed bookings, blended ROAS 21.6x, retargeting ROAS 16.7x, CPL $1.01 on 90 leads · August: spend $3,109, 113 Meta-attributed bookings, blended ROAS 23.1x, retargeting ROAS 18.0x, CPL $1.64 on 471 leads · September: spend $3,074, 98 Meta-attributed bookings, blended ROAS 28.8x, retargeting ROAS 13.0x, CPL $0.97 on 764 leads · October: spend $4,651, 124 Meta-attributed bookings, blended ROAS 21.5x, retargeting ROAS 9.8x, CPL $1.03 on 746 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). The LoL lookalike stays Scale at 20.8x on 15 purchases ($864), now at $100/day after Shawal doubled it on 12 and 13 Nov. BoF slips from 15.0x to 13.2x, Healthy, on 9 purchases ($681); its frequency of 5.45 is the highest in the review (Frequency watch, week 3). Discovery read (context only) 51.0x: WELCOME100 ×71 ($78.2k) in 30 days on $1,571. Direct revenue month to date +22% on October.

### Treetop Escapes — AM Makenna — account Treetop Escapes Ads (967636478877602) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $903 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,994; pixel purchase value $19,317 + sign-up promo revenue $17,259 = $36,576, ROAS 12.2x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $28,191 from 32 bookings, +0% vs 1 Oct–16 Oct ($28,060 from 34 bookings) · promo codes: 12 uses (WELCOME100 ×10, VIP100 ×1, WELCOME10 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $553 | 10 purchases | ROAS 13.5x | 3.70 | Healthy | CPM $16.81 > $16.50; freq 3.7 > 3.0 | 30d ROAS 15.5x, 19 purchases | Was Scale w/ HG AI |
| MoF - Lookalike Sales Campaign - 11/13/2026 | Prospecting (MoF lookalike) | 14d | $53 | 1 purchases | ROAS 15.6x | 1.37 | Under gate | CPM $17.48 > $16.50 | spend $52.74 < $200 gate; 30d ROAS 15.6x, 1 purchases | New, not in the 9 Nov run |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $844 | 1097 leads | CPL $0.77 (diagnostic) | — | Not scored (lead gen) | CPM $15.97 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.81 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,747 | 16 promo bookings, $17,259 | promo ROAS 9.9x | — | Not scored (discovery) | WELCOME100 ×15 $13,937, WELCOME10 ×1 $3,322; not counted (not sign-up codes): VIP100 ×2 $2,047 | $1,747 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Giveaway Traffic Campaign, against direct bookings booked 17 Oct–16 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $2,487, 44 Meta-attributed bookings, blended ROAS 14.5x, retargeting ROAS 22.2x, CPL $1.48 on 21 leads · August: spend $3,082, 33 Meta-attributed bookings, blended ROAS 12.3x, retargeting ROAS 16.3x, CPL $1.49 on 620 leads · September: spend $2,998, 23 Meta-attributed bookings, blended ROAS 7.9x, retargeting ROAS 7.9x, CPL $0.88 on 1019 leads · October: spend $3,081, 32 Meta-attributed bookings, blended ROAS 10.9x, retargeting ROAS 11.8x, CPL $0.79 on 1164 leads.

Meeting notes (Meta Ads Strategy 2026-11-11): Furthermore, Dustin Baker and Gillian Conley reviewed specific return on ad spend targets for various clients, such as a 7x return for Away Frames and Stay Saluted, and a 5x return for Tree Tops, Lodge, and others, with Dustin Baker deciding to set a 5x minimum bar for scaling despite higher inventory availability.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF slips from Scale (18.1x) to Healthy at 13.5x on 10 purchases ($553), frequency 3.7, still well above the 5x target from the 11 Nov Strategy meeting. The new 13 Nov lookalike ($20/day, funded by cutting the lead campaign from $30 to $10) has 1 purchase on $53, under the gate. Direct revenue month to date flat on October ($28.2k). Discovery read (context only) 9.9x: WELCOME100 ×15 on $1,747.

### Ponderosa Pines Resort — AM Anna — account Ponderosa Pines Resort (1058846326445255) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,173 over 30 days.

Blended 30d (every HiddenGem campaign): spend $3,048; pixel purchase value $11,068 + sign-up promo revenue $0 = $11,068, ROAS 3.6x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $24,818 from 85 bookings, +9% vs 1 Oct–16 Oct ($22,707 from 81 bookings) · promo codes: not tracked by newbook.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Website Retarget Campaign - 07/13/26 | Retargeting (BoF) | 14d | $552 | 13 purchases | ROAS 7.5x | 2.66 | Monitor | CPC $0.67 > $0.62; CPM $18.11 > $16.50 | 30d ROAS 8.9x, 31 purchases | Unchanged |
| MoF - Lookalike Sales Campaign - 11/13/26 | Prospecting (MoF lookalike) | 14d | $101 | 1 purchases | ROAS 3.9x | 1.55 | Under gate | CPC $0.96 > $0.62; CPM $23.86 > $16.50; cost/booking $101.32 > $90 | spend $101.32 < $200 gate; 30d ROAS 3.9x, 1 purchases | New, not in the 9 Nov run |
| Leads Campaign - 07/16/26 | Lead Gen (MoF) | 30d | $577 | 440 leads | CPL $1.31 (diagnostic) | — | Not scored (lead gen) | CPC $0.34 > $0.30; CPM $17.40 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.49 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,750 | — | promo ROAS — | — | Not scored (discovery) | — | $1,750 in 30 days across Discovery Campaign - Giveaway - June 2026, Leads Campaign - 07/16/26; newbook does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $2,089, 17 Meta-attributed bookings, blended ROAS 3.6x, retargeting ROAS 22.3x, CPL $0.91 on 356 leads · August: spend $3,101, 103 Meta-attributed bookings, blended ROAS 15.0x, retargeting ROAS 21.3x, CPL $1.32 on 471 leads · September: spend $2,985, 119 Meta-attributed bookings, blended ROAS 17.9x, retargeting ROAS 21.6x, CPL $0.84 on 708 leads · October: spend $3,065, 39 Meta-attributed bookings, blended ROAS 6.0x, retargeting ROAS 12.5x, CPL $1.02 on 601 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF holds Monitor at 7.5x on 13 purchases ($552). Read it as an upper bound: the pixel check still shows the Newbook confirmation firing about 1.8 browser Purchases per booking. The new 13 Nov lookalike ($40/day) has 1 purchase on $101, under the gate. Leads $1.31 on 440. Direct revenue month to date +9% on October. No promo data (Newbook stores no code).

### Starlight Haven Hot Springs — AM Charlotte — account Starlight Haven Hot Springs (901138032027913) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $753 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,248; pixel purchase value $12,383 + sign-up promo revenue $0 = $12,383, ROAS 5.5x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $275 | 9 purchases | ROAS 18.3x | 2.01 | Scale w/ HG AI | within lines | 30d ROAS 20.9x, 19 purchases | Unchanged |
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $901 | 2815 leads | CPL $0.32 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.32 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,654 | — | promo ROAS — | — | Not scored (discovery) | — | $1,654 in 30 days across Discovery Campaign - Giveaway - 12/16/2025, New Leads Campaign - 03/03/26; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $2,160, 17 Meta-attributed bookings, blended ROAS 5.1x, retargeting ROAS 17.1x, CPL $0.33 on 2813 leads · August: spend $2,193, 19 Meta-attributed bookings, blended ROAS 6.3x, retargeting ROAS 22.3x, CPL $0.36 on 2589 leads · September: spend $2,155, 61 Meta-attributed bookings, blended ROAS 16.5x, retargeting ROAS 28.5x, CPL $0.34 on 2597 leads · October: spend $2,298, 71 Meta-attributed bookings, blended ROAS 21.0x, retargeting ROAS 22.1x, CPL $0.32 on 2869 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF holds Scale at 18.3x on 9 purchases ($275), up from 15.5x. On 12 Nov the lead campaign's interest and lookalike ad sets were paused and Broad US Engagers raised to $30; leads $0.32 on 2,815.

### FLOHOM — AM Makenna — account FLOHOM Ads (2100710320122219) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $301 over 30 days.

Blended 30d (every HiddenGem campaign): spend $4,197; pixel purchase value $33,891 + sign-up promo revenue $21,345 = $55,236, ROAS 13.2x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $39,010 from 49 bookings, −37% vs 1 Oct–16 Oct ($62,212 from 67 bookings) · promo codes: 11 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| [Myrtle Beach] MoF - Lookalike Sales Campaign - 09/17/26 | Prospecting (MoF lookalike) | 14d | $282 | 1 purchases | ROAS 3.3x | 2.38 | Review w/ HG AI | CPC $1.27 > $0.62; CPM $21.80 > $16.50; cost/booking $282.10 > $90 | 30d ROAS 5.3x, 2 purchases | New flag, was Healthy |
| MoF - Lookalike Sales Campaign - 07/29/26 | Prospecting (MoF lookalike) | 14d | $704 | 7 purchases | ROAS 6.2x | 2.02 | Monitor | CPM $18.96 > $16.50; cost/booking $100.60 > $90 | 30d ROAS 13.3x, 24 purchases | Was Healthy |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $706 | 7 purchases | ROAS 10.0x | 2.18 | Healthy | CPM $16.97 > $16.50; cost/booking $100.86 > $90 | 30d ROAS 7.2x, 13 purchases | Fixed, was Review w/ HG AI |
| MoF - Lead Campaign - Retargeting Engagers – 08/17/26 | Lead Gen (MoF) | 30d | $304 | 512 leads | CPL $0.59 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.60 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $605 | 23 promo bookings, $21,345 | promo ROAS 35.3x | — | Not scored (discovery) | 23 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $605 in 30 days across ToF - Giveaway Traffic Campaign, MoF - Lead Campaign - Retargeting Engagers – 08/17/26, against direct bookings booked 17 Oct–16 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $5,555, 103 Meta-attributed bookings, blended ROAS 17.2x, retargeting ROAS 19.1x, CPL $7.66 on 66 leads · August: spend $9,331, 90 Meta-attributed bookings, blended ROAS 8.5x, retargeting ROAS 8.2x, CPL $2.24 on 708 leads · September: spend $8,855, 82 Meta-attributed bookings, blended ROAS 8.9x, retargeting ROAS 8.9x, CPL $0.50 on 2192 leads · October: spend $5,455, 71 Meta-attributed bookings, blended ROAS 12.0x, retargeting ROAS 9.7x, CPL $0.56 on 809 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF is Fixed: from Review (3.7x) to Healthy at 10.0x on 7 purchases ($706). The Myrtle Beach lookalike drops from Healthy (8.2x) to Review at 3.3x on 1 purchase ($282), a new Action row; the main lookalike slips from Healthy (12.0x) to Monitor at 6.2x on 7 purchases ($704). Direct revenue month to date $39.0k, −37% on October (49 bookings against 67), better than last week's −66%. Budget $140/day.

### Stay Saluda NC — AM Makenna — account Stay Saluda Ads (1863632561215857) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $896 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,452; pixel purchase value $10,013 + sign-up promo revenue $14,427 = $24,440, ROAS 10.0x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $14,682 from 24 bookings, +51% vs 1 Oct–16 Oct ($9,697 from 16 bookings) · promo codes: 12 uses (ENJOY10 ×9, VIP10 ×2, WELCOME10 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $420 | 9 purchases | ROAS 14.4x | 4.62 | Healthy | CPC $0.75 > $0.62; CPM $18.05 > $16.50; freq 4.6 > 3.0 | 30d ROAS 10.5x, 15 purchases | Was Scale w/ HG AI |
| MoF - Lookalike Sales Campaign - 11/13/2026 | Prospecting (MoF lookalike) | 14d | $54 | 1 purchases | ROAS 9.4x | 1.51 | Under gate | CPM $21.83 > $16.50 | spend $54.28 < $200 gate; 30d ROAS 9.4x, 1 purchases | New, not in the 9 Nov run |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $598 | 648 leads | CPL $0.92 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.92 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,494 | 19 promo bookings, $14,427 | promo ROAS 9.7x | — | Not scored (discovery) | ENJOY10 ×16 $10,792, WELCOME10 ×3 $3,635; not counted (not sign-up codes): VIP10 ×2 $1,298, DUBLE10 ×1 $273 | $1,494 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Giveaway Traffic Campaign - NC/SC/GA/TN, against direct bookings booked 17 Oct–16 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $2,140, 10 Meta-attributed bookings, blended ROAS 2.6x, retargeting ROAS 0.8x · August: spend $2,367, 10 Meta-attributed bookings, blended ROAS 3.9x, retargeting ROAS 5.2x, CPL $2.59 on 146 leads · September: spend $2,394, 14 Meta-attributed bookings, blended ROAS 3.8x, retargeting ROAS 3.5x, CPL $1.00 on 596 leads · October: spend $2,449, 25 Meta-attributed bookings, blended ROAS 7.0x, retargeting ROAS 5.7x, CPL $0.94 on 647 leads.

Meeting notes (Meta Ads Strategy 2026-11-11): Furthermore, Dustin Baker and Gillian Conley reviewed specific return on ad spend targets for various clients, such as a 7x return for Away Frames and Stay Saluted, and a 5x return for Tree Tops, Lodge, and others, with Dustin Baker deciding to set a 5x minimum bar for scaling despite higher inventory availability.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF slips from Scale (20.1x) to Healthy at 14.4x on 9 purchases ($420), frequency 4.6, still twice the 7x target set at the 11 Nov Strategy meeting. The new 13 Nov lookalike ($20/day) has 1 purchase on $54, under the gate. Discovery read (context only) 9.7x: ENJOY10 ×16 and WELCOME10 ×3 on $1,494. Direct revenue month to date +51% on October.

### Asheville River Cabins — AM Charlotte — account Asheville River Cabins Ads (615836588009747) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,172 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,565; pixel purchase value $18,723 + sign-up promo revenue $0 = $18,723, ROAS 7.3x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Broad - 06/08/26 | Prospecting (MoF lookalike) | 14d | $556 | 21 purchases | ROAS 26.2x | 2.17 | Scale w/ HG AI | CPM $16.68 > $16.50 | 30d ROAS 17.4x, 28 purchases | Unchanged |
| BoF - Website Retargeting Campaign - 12/11/26 | Retargeting (BoF) | 14d | $63 | 1 purchases | ROAS 13.2x | 2.04 | Under gate | CPC $0.89 > $0.62; CPM $23.73 > $16.50 | spend $63.28 < $200 gate; 30d ROAS 13.2x, 1 purchases | New, not in the 9 Nov run |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $299 | 831 leads | CPL $0.36 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.36 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,471 | — | promo ROAS — | — | Not scored (discovery) | — | $1,471 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Discovery Campaign Giveaway - 09/17/26; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $2,029, 39 Meta-attributed bookings, blended ROAS 18.6x, retargeting ROAS 51.6x · August: spend $2,424, 82 Meta-attributed bookings, blended ROAS 27.2x, retargeting ROAS 65.0x, CPL $0.42 on 605 leads · September: spend $2,252, 70 Meta-attributed bookings, blended ROAS 19.1x, retargeting ROAS 42.5x, CPL $0.30 on 936 leads · October: spend $2,233, 68 Meta-attributed bookings, blended ROAS 23.1x, retargeting ROAS 27.4x, CPL $0.32 on 869 leads.

Meeting notes (Meta Ads Sync 2026-11-11): Review of Existing Client Budgets and Account Adjustments: Dustin Baker and Ananya Arora reviewed active client ad accounts and budgets, noting that Endless Days increased their spend to approximately $100 daily, prompting a move to the advanced tier, and Asheville River Cabins was bumped from $30 to $50 daily by Dustin Baker after achieving strong return on ad spend results over several months. Facebook Application Programming Interface Integration for Cloud Beds: Leshan Patterson reported that Facebook click identifiers are coming through the website, but data is not being sent to Henji because the Application Programming Interface is unavailable through the Asheville River Captain's Cloud Beds account.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). The 06/08 campaign that scored Scale as BoF retargeting (26.4x) was renamed 'MoF - Broad - 06/08/26' with no audience on 12 Nov (Shawal), so it now reads as Prospecting. Its 26.2x on 21 purchases ($556) is mostly retargeting history; the next two weeks show what the broad audience does. Retargeting restarted as 'BoF - Website Retargeting Campaign - 12/11/26' (Website Visitors 180D, value optimisation) at $20/day from 13 Nov: 1 purchase on $63, under the gate. All Purchases are browser-side: Leshan said on 11 Nov that the Cloudbeds API is not enabled on Asheville's account, so the HG AI CAPI cannot send yet.

### Little River Landing — AM Makenna — account Little River Landing (884285717873613) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,788 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,404; pixel purchase value $691 + sign-up promo revenue $393 = $1,084, ROAS 0.5x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $1,500 from 9 bookings, −18% vs 1 Oct–16 Oct ($1,823 from 10 bookings) · promo codes: 1 uses (STAY10 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 09/16/2026 | Retargeting (BoF) | 14d | $220 | 1 purchases | ROAS 1.4x | 3.43 | Flag to Shawal | CPC $0.73 > $0.62; cost/booking $219.53 > $90; freq 3.4 > 3.0 | 30d ROAS 1.7x, 2 purchases | Still open, week 2 |
| MoF - Lookalike Sales Campaign - 11/13/2026 | Prospecting (MoF lookalike) | 14d | $49 | 0 purchases | ROAS — | 1.36 | Under gate | CPC $0.76 > $0.62; CPM $18.38 > $16.50 | spend $49.08 < $200 gate | New, not in the 9 Nov run |
| MoF - Lead Campaign - Retargeting Engagers - 09/16/2026 | Lead Gen (MoF) | 30d | $149 | 74 leads | CPL $2.01 (diagnostic) | — | Not scored (lead gen) | CPC $0.48 > $0.30; CPM $24.55 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.97 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,937 | 1 promo bookings, $393 | promo ROAS 0.2x | — | Not scored (discovery) | WELCOME10 ×1 $393; not counted (not sign-up codes): STAY10 ×1 $298 | $1,937 in 30 days across ToF - Giveaway Traffic Campaign - AL - 09/16/2026, MoF - Lead Campaign - Retargeting Engagers - 09/16/2026, against direct bookings booked 17 Oct–16 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: September: spend $921, 0 Meta-attributed bookings, blended ROAS —, retargeting ROAS —, CPL $1.86 on 46 leads · October: spend $2,165, 1 Meta-attributed bookings, blended ROAS 0.2x, retargeting ROAS 1.5x, CPL $1.50 on 101 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF stays Flag, week 2: 1.4x on 1 purchase ($220 in 14 days). Tracking is still the first fix: 5 Purchase in 28 days against 11 PMS online bookings (45%) with the HG AI CAPI off (pixel check). On 13 Nov BoF went to $20 and a $20 lookalike was added (0 purchases on $49), so the Sales budget is $40/day before the CAPI is on. Discovery read 0.2x on $1,937.

### Starlight Haven Weiss Lake — AM Charlotte — account Starlight Haven Weiss Lake (74756899) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $0 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,113; pixel purchase value $25,152 + sign-up promo revenue $0 = $25,152, ROAS 11.9x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $644 | 23 purchases | ROAS 17.6x | 2.67 | Scale w/ HG AI | CPC $0.97 > $0.62 | 30d ROAS 18.5x, 50 purchases | Unchanged |
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $755 | 655 leads | CPL $1.15 (diagnostic) | — | Not scored (lead gen) | CPC $0.35 > $0.30 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.21 | Unchanged |
| Discovery bucket (1 campaign: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $755 | — | promo ROAS — | — | Not scored (discovery) | — | $755 in 30 days across New Leads Campaign - 03/03/26; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $2,163, 41 Meta-attributed bookings, blended ROAS 10.8x, retargeting ROAS 15.2x, CPL $0.74 on 826 leads · August: spend $2,351, 36 Meta-attributed bookings, blended ROAS 10.7x, retargeting ROAS 17.6x, CPL $1.23 on 617 leads · September: spend $2,152, 79 Meta-attributed bookings, blended ROAS 17.4x, retargeting ROAS 23.8x, CPL $1.01 on 734 leads · October: spend $2,142, 53 Meta-attributed bookings, blended ROAS 15.6x, retargeting ROAS 24.2x, CPL $1.09 on 704 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF holds Scale at 17.6x on 23 purchases ($644), down from 26.2x. The lead campaign's interest and lookalike ad sets were paused on 12 Nov in favour of Broad US Engagers; leads $1.15 on 655.

### Selah Place — AM Alicia — account Selah.place (1275283434220508) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $903 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,212; pixel purchase value $9,115 + sign-up promo revenue $10,582 = $19,697, ROAS 8.9x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $13,807 from 33 bookings, −7% vs 1 Oct–16 Oct ($14,919 from 26 bookings) · promo codes: 9 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF-Website Retarget Campaign - 07/24/2026 | Retargeting (BoF) | 14d | $412 | 14 purchases | ROAS 17.0x | 4.07 | Scale w/ HG AI | CPC $0.67 > $0.62; CPM $22.48 > $16.50; freq 4.1 > 3.0 | 30d ROAS 9.9x, 21 purchases | Was Monitor |
| MoF - Lookalike Sales Campaign - 11/13/2026 | Prospecting (MoF lookalike) | 14d | $49 | 1 purchases | ROAS 4.2x | 1.38 | Under gate | CPM $18.42 > $16.50 | spend $49.47 < $200 gate; 30d ROAS 4.2x, 1 purchases | New, not in the 9 Nov run |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $362 | 467 leads | CPL $0.78 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.89 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,265 | 19 promo bookings, $10,582 | promo ROAS 8.4x | — | Not scored (discovery) | 19 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $1,265 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Giveaway Traffic Campaign - 08/07/2026, against direct bookings booked 17 Oct–16 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Client-run, not scored: SP / Willow / Pre-Sales / VIP List / 10-2026 (Sales, paused), created by Nathan Jay Herrington on 2026-10-19, $831 / 14d, 3 purchases, ROAS 0.2x. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: Instagram post: 🔥 𝐒𝐀𝐂𝐑𝐈𝐅𝐈𝐂𝐄 𝐈𝐒 𝐑𝐄𝐐𝐔𝐈𝐑𝐄𝐃 🔥... (Other, paused), created by Live Intentionally Today LIT on 2026-10-15, $26 / 14d, 0 purchases, ROAS —. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Willow / Lead Gen / VIP List / 10-2026 (Lead Gen (MoF), active), created by Nathan Jay Herrington on 2026-10-20, $1,364 / 30d, 864 leads, CPL $1.58. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Willow / Sales / Top-5 Audiences / 11-2026 (Sales, active), created by Nathan Jay Herrington on 2026-10-28, $2,112 / 14d, 15 purchases, ROAS 0.4x. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Black Walnut / Sales / Pre-Sale / 11-2026 (Sales, paused), created by Nathan Jay Herrington on 2026-11-05, $35 / 14d, 0 purchases, ROAS —. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Black Walnut / Leads / Early Access / 11-2026 (Lead Gen (MoF), paused), created by Nathan Jay Herrington on 2026-11-07, $762 / 30d, 68 leads, CPL $11.21. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Monthly ROI: July: spend $1,054, 4 Meta-attributed bookings, blended ROAS 3.2x, retargeting ROAS 86.3x, CPL $0.80 on 49 leads · August: spend $1,545, 15 Meta-attributed bookings, blended ROAS 4.8x, retargeting ROAS 25.1x, CPL $1.08 on 144 leads · September: spend $1,304, 27 Meta-attributed bookings, blended ROAS 10.4x, retargeting ROAS 38.2x, CPL $0.63 on 232 leads · October: spend $1,842, 23 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 9.7x, CPL $0.61 on 405 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). HiddenGem's BoF jumps from Monitor (5.6x) to Scale at 17.0x on 14 purchases ($412), frequency 4.1. Read it with care: the pixel's server Purchases still run about 2.5x the PMS bookings (HG AI CAPI plus Hostaway's CAPI). The new 13 Nov lookalike ($20/day) is under the gate. The client paused both Black Walnut campaigns and one Willow ad set on 14 Nov, so the account is $345/day, $100 of it HiddenGem's four campaigns.

### Ridge & Falls — AM Makenna — account Ridge & Falls ad account (1313401330776046) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,509 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,063; pixel purchase value $8,596 + sign-up promo revenue $0 = $8,596, ROAS 4.2x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $3,143 from 8 bookings, +117% vs 1 Oct–16 Oct ($1,450 from 4 bookings) · promo codes: 5 uses (HELLO10 ×4, STAY10 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 09/01/26 | Retargeting (BoF) | 14d | $211 | 12 purchases | ROAS 22.9x | 5.34 ⚠️ > 5 | Scale w/ HG AI | freq 5.3 > 3.0 | 30d ROAS 21.2x, 19 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 09/01/26 | Lead Gen (MoF) | 30d | $149 | 59 leads | CPL $2.53 (diagnostic) | — | Not scored (lead gen) | CPC $0.35 > $0.30 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $3.85 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,658 | 0 promo bookings, $0 | promo ROAS 0.0x | — | Not scored (discovery) | no sign-up code bookings in 30 days; not counted (not sign-up codes): HELLO10 ×4 $1,729, STAY10 ×1 $412 | $1,658 in 30 days across ToF - Giveaway Traffic Campaign - GA, AL - 09/01/26, MoF - Lead Campaign - Retargeting Engagers - 09/01/26, against direct bookings booked 17 Oct–16 Nov with a sign-up code; no sign-up promo bookings in 30 days; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: September: spend $1,036, 0 Meta-attributed bookings, blended ROAS —, retargeting ROAS —, CPL $8.16 on 16 leads · October: spend $1,941, 10 Meta-attributed bookings, blended ROAS 2.5x, retargeting ROAS 18.7x, CPL $2.33 on 64 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF holds Scale at 22.9x on 12 purchases ($211), frequency 5.34 (Frequency watch, week 2). The ROAS is inflated: the pixel receives about 1.8 server Purchases per PMS booking (two senders). Direct revenue month to date $3.1k from 8 bookings. Discovery read 0.0x: HELLO10 ×4 and STAY10 ×1 are not sign-up codes.

### Sunapee Stays — AM Charlotte — account Sunapee Stays Ads Account (651114096215889) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $843 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,393; pixel purchase value $591 + sign-up promo revenue $0 = $591, ROAS 0.4x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $3,858 from 12 bookings, −81% vs 1 Oct–16 Oct ($20,061 from 36 bookings) · promo codes: not tracked by ownerrez.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $114 | 0 purchases | ROAS — | 2.91 | Under gate | CPC $0.88 > $0.62 | spend $113.69 < $200 gate; 30d ROAS 2.1x, 1 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $273 | 133 leads | CPL $2.05 (diagnostic) | — | Not scored (lead gen) | CPC $0.49 > $0.30; CPM $19.09 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $2.02 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,116 | — | promo ROAS — | — | Not scored (discovery) | — | $1,116 in 30 days across ToF Discovery Campaign - Giveaway - 06/10/26, MoF - Lead Campaign - Retargeting Engagers; ownerrez does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $939, 16 Meta-attributed bookings, blended ROAS 9.9x, CPL $2.06 on 9 leads · August: spend $1,494, 10 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 25.1x, CPL $2.74 on 112 leads · September: spend $1,495, 14 Meta-attributed bookings, blended ROAS 6.5x, retargeting ROAS 6.7x, CPL $1.64 on 184 leads · October: spend $1,540, 11 Meta-attributed bookings, blended ROAS 3.4x, retargeting ROAS 10.7x, CPL $1.89 on 161 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF under the gate, 0 purchases on $114; Charlotte cut the account from $50 to $30/day on 10 Nov. Month-to-date direct revenue $3.9k against $20.1k on the same days of October (−81%).

### Green Springs Inn — AM Alicia — account Green Springs Inn (1390516335151357) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $602 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,201; pixel purchase value $5,823 + sign-up promo revenue $15,074 = $20,897, ROAS 17.4x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $24,584 from 50 bookings, +22% vs 1 Oct–16 Oct ($20,089 from 43 bookings) · promo codes: 18 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 08/28/26 | Retargeting (BoF) | 14d | $139 | 9 purchases | ROAS 35.9x | 3.08 | Under gate | CPC $0.73 > $0.62; freq 3.1 > 3.0 | spend $138.96 < $200 gate; 30d ROAS 19.4x, 11 purchases | Unchanged |
| MoF - Lead Campaign/08/28/2026 | Lead Gen (MoF) | 30d | $299 | 178 leads | CPL $1.68 (diagnostic) | — | Not scored (lead gen) | CPC $0.33 > $0.30 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.69 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $901 | 29 promo bookings, $15,074 | promo ROAS 16.7x | — | Not scored (discovery) | 29 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $901 in 30 days across ToF - Giveaway Traffic Campaign - 07/24/2026, MoF - Lead Campaign/08/28/2026, against direct bookings booked 17 Oct–16 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $1,222, 17 Meta-attributed bookings, blended ROAS 7.8x, retargeting ROAS 14.6x, CPL $5.65 on 8 leads · August: spend $1,247, 23 Meta-attributed bookings, blended ROAS 8.2x, retargeting ROAS 17.1x, CPL $9.09 on 34 leads · September: spend $1,199, 24 Meta-attributed bookings, blended ROAS 8.5x, retargeting ROAS 9.0x, CPL $1.84 on 166 leads · October: spend $1,231, 26 Meta-attributed bookings, blended ROAS 10.6x, retargeting ROAS 9.5x, CPL $1.42 on 214 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF under the gate at 35.9x on 9 purchases ($139). Discovery read (context only) 16.7x on 29 Hostaway coupon bookings (no code names). Direct revenue month to date +22% on October.

### Gooseberry Lodges — AM Alicia — account Gooseberry Ad Account (701051796368186) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $784 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,086; pixel purchase value $0 + sign-up promo revenue $0 = $0, ROAS 0.0x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 10.27/2026 | Retargeting (BoF) | 14d | $140 | 0 purchases | ROAS — | 1.86 | Under gate | CPC $0.90 > $0.62 | spend $140.08 < $200 gate | New, not in the 9 Nov run |
| MoF - Lead Campaign - Retargeting Engagers - 10/27/2026 | Lead Gen (MoF) | 30d | $133 | 86 leads | CPL $1.55 (diagnostic) | — | Not scored (lead gen) | CPC $0.35 > $0.30 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.43 | New, not in the 9 Nov run |
| Discovery bucket (3 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $917 | — | promo ROAS — | — | Not scored (discovery) | — | $917 in 30 days across ToF - Giveaway Traffic Campaign - SW Drive Markets (LV / SoCal / NUT) - 10/27/2026 (paused), MoF - Lead Campaign - Retargeting Engagers - 10/27/2026, ToF - Giveaway Traffic Campaign - SW Drive Markets (LV / SoCal / NUT) - 10/27/2026; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | New, not in the 9 Nov run |

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes (Meta Ads Sync 2026-11-11): Gooseberry Lodges Property Management Software and Ad Spend: Alicia Morin reported that Gooseberry Lodges experienced low performance in November. Alicia Morin explained that Gooseberry Lodges utilizes the Little Hotelier property management software, which lacks an Application Programming Interface key, preventing integration with Hidden Gem artificial intelligence for insights.
Meeting notes (Meta Ads Strategy 2026-11-11): Gillian Conley noted that while account managers complete this during onboarding, certain clients like Little Hotelier, Gooseberry Lodge, and Wilton are marked as incompatible or lacking access.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). First week in the review (mapped 16 Nov). BoF under the gate, 0 purchases on $140 in 14 days, at $25/day since Alicia's 12 Nov increase. The pixel is browser-only and Little Hotelier has no API, so the HG AI platform cannot see bookings (11 Nov Sync); Alicia plans to meet Shawal about raising spend toward $100/day. Leads $1.55 on 86.

### The Outpost — AM Anna — account The Outpost Grand Canyon (1530849534802936) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $898 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,202; pixel purchase value $1,032 + sign-up promo revenue $0 = $1,032, ROAS 0.9x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $6,459 from 15 bookings, −49% vs 1 Oct–16 Oct ($12,569 from 27 bookings) · promo codes: not tracked by newbook.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 10/08/2026 | Retargeting (BoF) | 14d | $134 | 1 purchases | ROAS 3.2x | 2.57 | Under gate | CPC $0.72 > $0.62; cost/booking $134.48 > $90 | spend $134.48 < $200 gate; 30d ROAS 3.4x, 3 purchases | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $898 | — | promo ROAS — | — | Not scored (discovery) | — | $898 in 30 days across Insta Discovery Campaign - Giveaway - May 2026, Facebook Discovery Campaign - Giveaway - May 2026; newbook does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $2,182, 1 Meta-attributed bookings, blended ROAS 0.2x, CPL $1.61 on 202 leads · August: spend $1,876, 7 Meta-attributed bookings, blended ROAS 2.1x, CPL $1.71 on 181 leads · September: spend $2,081, 18 Meta-attributed bookings, blended ROAS 3.8x, retargeting ROAS —, CPL $1.80 on 167 leads · October: spend $2,149, 12 Meta-attributed bookings, blended ROAS 2.8x, retargeting ROAS 1.9x, CPL $1.73 on 176 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). Only the 10/08 BoF is live: 3.2x on 1 purchase ($134), under the gate. Shawal paused the old 08/29 BoF on 12 Nov, which closes decision 30. Direct revenue month to date −49% on October. Pixel: Purchase capture 49% of 37 online bookings.

### North Star Lodge & Resort — AM Charlotte — account North Star Lodge & Resort Ads (2003562593933799) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $598 over 30 days.

Blended 30d (every HiddenGem campaign): spend $898; pixel purchase value $913 + sign-up promo revenue $0 = $913, ROAS 1.0x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $31,073 from 51 bookings, −30% vs 1 Oct–16 Oct ($44,592 from 94 bookings) · promo codes: not tracked by cloudbeds.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 09/09/2026 | Retargeting (BoF) | 14d | $70 | 2 purchases | ROAS 10.0x | 2.98 | Under gate | CPC $0.75 > $0.62 | spend $70.27 < $200 gate; 30d ROAS 6.1x, 3 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 10/02/26 | Lead Gen (MoF) | 30d | $49 | 1 leads | CPL $49.01 (diagnostic) | — | Under gate | CPC $0.91 > $0.30; CPM $25.39 > $14.84 | spend $49.01 < $100 gate | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 10/26/26 | Lead Gen (MoF) | 30d | $101 | 56 leads | CPL $1.81 (diagnostic) | — | Not scored (lead gen) | CPC $0.41 > $0.30; CPM $16.09 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.43 | Was Under gate, not scored since 4 Nov |
| Discovery bucket (3 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $748 | — | promo ROAS — | — | Not scored (discovery) | — | $748 in 30 days across ToF - Giveaway Traffic Campaign - 09/09/2002, MoF - Lead Campaign - Retargeting Engagers - 10/02/26, MoF - Lead Campaign - Retargeting Engagers - 10/26/26; cloudbeds does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: September: spend $580, 0 Meta-attributed bookings, blended ROAS — · October: spend $919, 2 Meta-attributed bookings, blended ROAS 0.7x, retargeting ROAS 1.4x, CPL $22.29 on 6 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF under the gate at 10.0x on 2 purchases ($70). The 10/02 lead campaign still has 1 lead on $49 in 30 days while 10/26 has 56 at $1.81, so pausing the older one is still open (Charlotte). Direct revenue month to date −30% on October. Pixel: Purchase capture 36% of 76 online bookings; the Cloudbeds browser Purchase is still mostly missing.

### Glasscombe — AM Charlotte — account Glasscombe (2030318804465316) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $595 over 30 days.

Blended 30d (every HiddenGem campaign): spend $889; pixel purchase value $3,078 + sign-up promo revenue $0 = $3,078, ROAS 3.5x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $7,087 from 14 bookings, +209% vs 1 Oct–16 Oct ($2,290 from 7 bookings) · promo codes: not tracked by cloudbeds.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 10/09/26. | Retargeting (BoF) | 14d | $70 | 3 purchases | ROAS 44.0x | 1.80 | Under gate | CPM $18.75 > $16.50 | spend $69.96 < $200 gate; 30d ROAS 20.8x, 3 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers -  10/09/26 | Lead Gen (MoF) | 30d | $146 | 481 leads | CPL $0.30 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.36 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $741 | — | promo ROAS — | — | Not scored (discovery) | — | $741 in 30 days across ToF - Giveaway Traffic Campaign - UK, MoF - Lead Campaign - Retargeting Engagers -  10/09/26; cloudbeds does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: October: spend $541, 2 Meta-attributed bookings, blended ROAS 2.2x, retargeting ROAS —, CPL $0.29 on 306 leads. Note in the October file: LaunchBoom pre-bookings led to high occupancy at low revenue this month (AM note from the tracking sheet).

Meeting notes (Meta Ads Sync 2026-11-11): Client Tiering and Budget Scaling Based on Performance: Dustin Baker distinguished between basic clients using a set-and-forget approach with $30 to $50 daily budgets, such as Oak and Ember, and advanced clients where the team actively scales Meta ads to maximize business growth, such as Glasscom and Waveframes.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF under the gate at 44.0x on 3 purchases ($70); leads $0.30 on 481. Direct revenue month to date $7.1k, +209% on October.

### Cabin Collective — AM Chiara — account Cabin Collective (2194562394139883) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $255 over 30 days.

Blended 30d (every HiddenGem campaign): spend $767; pixel purchase value $11,817 + sign-up promo revenue $0 = $11,817, ROAS 15.4x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–16 Nov): direct revenue $21,608 from 13 bookings, −38% vs 1 Oct–16 Oct ($35,026 from 20 bookings) · promo codes: not tracked by ownerrez.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 10/20/26 | Retargeting (BoF) | 14d | $147 | 2 purchases | ROAS 19.4x | 2.28 | Under gate | within lines | spend $147.12 < $200 gate; 30d ROAS 46.2x, 8 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 10/20/26 | Lead Gen (MoF) | 30d | $256 | 219 leads | CPL $1.17 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.11 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $511 | — | promo ROAS — | — | Not scored (discovery) | — | $511 in 30 days across ToF - Giveaway Traffic Campaign - [TX, OK, AR] - 10/20/26, MoF - Lead Campaign - Retargeting Engagers - 10/20/26; ownerrez does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: October: spend $312, 6 Meta-attributed bookings, blended ROAS 28.8x, retargeting ROAS 86.4x, CPL $1.31 on 79 leads. Note in the October file: No booking-level export from the client this month; the direct booking revenue is the client reporting sheet figure and the booking count is unavailable. Attributed revenue comes from Meta-reported retargeting purchases only.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF under the gate at 19.5x on 2 purchases ($147). The HG AI CAPI sent its first Purchases this morning (16 Nov). Direct revenue month to date −38% on October. Master sheet still reads Not Live.

### Walden Retreats — AM Anna — account Walden Retreats (973261794434226) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $299 over 30 days.

Blended 30d (every HiddenGem campaign): spend $880; pixel purchase value $6,665 + sign-up promo revenue $0 = $6,665, ROAS 7.6x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers - 10/06/2026 | Lead Gen (MoF) | 30d | $299 | 246 leads | CPL $1.22 (diagnostic) | — | Not scored (lead gen) | CPC $0.36 > $0.30; CPM $18.71 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.09 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $598 | — | promo ROAS — | — | Not scored (discovery) | — | $598 in 30 days across ToF - Giveaway Traffic Campaign - ATX, HTX, DAL, SATX, FTW - 10/05/2026, MoF - Lead Campaign - Retargeting Engagers - 10/06/2026; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Paused in window, not scored: BoF - Sales Campaign - Retargeting Website Visitors - 06/10/2026 (Retargeting (BoF)), $120 / 14d, 9 purchases, ROAS 34.8x. Live campaigns only are scored (decision 2026-09-23).

Client-run, not scored: TOF Wedding Leads 10.8.26 (Lead Gen (MoF), paused), created by Lindsey Cooke on 2026-10-08, $435 / 30d, 22 leads, CPL $19.78. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: MOF Wedding Leads 10.27.26 (Lead Gen (MoF), paused), created by Lindsey Cooke on 2026-10-27, $32 / 30d, 1 leads, CPL $31.58. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Monthly ROI: October: spend $1,295, 26 Meta-attributed bookings, blended ROAS 16.6x, retargeting ROAS 30.8x, CPL $3.57 on 220 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). HiddenGem's BoF was paused on 14 Nov (Ananya) at the client's request over an issue with the VIP promo code, while it read 34.8x on 9 purchases ($120, under the gate); the account runs only the giveaway and the lead campaign at $20/day until it restarts. The pixel recorded 85 Purchase in 7 days with no PMS to check against (pixel check).

### American River Resort — AM Nicole — account American River Resort (953162737054331) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $0 over 30 days.

Blended 30d: no HiddenGem campaign spend in the window.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

No live Lead Gen, Sales or Discovery campaigns with spend in the window.

Monthly ROI: July: spend $1,544, 4 Meta-attributed bookings, blended ROAS 1.1x · August: spend $1,529, 3 Meta-attributed bookings, blended ROAS 1.4x, CPL $18.30 on 30 leads · September: spend $1,453, 0 Meta-attributed bookings, blended ROAS —, CPL $1.48 on 377 leads · October: spend $777, 2 Meta-attributed bookings, blended ROAS 15.1x, CPL $1.27 on 244 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). Ads off since 15 Oct: paused, not offboarded. Nothing scored.

### Dunya Camp — AM Chiara — account Dunya Camp (629838998232110) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $0 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,681; pixel purchase value $5,533 + sign-up promo revenue $0 = $5,533, ROAS 2.1x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

No live Lead Gen, Sales or Discovery campaigns with spend in the window.

Deferred, not scored: Retargeting - Sales - Step 3 (Retargeting (BoF)), $413 / 14d, 3 purchases, ROAS 13.4x. It optimises on Dunya Camp's custom 'Step 3' event; part of the older custom-event funnel left as is (Shawal, 12 Nov 2026).

Deferred, not scored: Fall step 2 campaign (Sales), $829 / 14d, 0 purchases, ROAS —. It optimises on Dunya Camp's custom 'Step 2' event, not Purchase, so purchase ROAS does not apply; part of the older custom-event funnel left as is (Shawal, 12 Nov 2026).

Client-run, not scored: fall winter purchase 2026 (Sales, active), created by Sangeetha Ramkumar on 2026-10-07, $411 / 14d, 3 purchases, ROAS 13.9x. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). First week in the review (mapped 16 Nov; $818 spent in the last 7 days). HiddenGem's three-campaign build (Charlotte: giveaway 30 Oct, lead and BoF 13 Nov) was switched on only this morning (Chiara), so none of it has spend in the window. The spend so far is the older funnel: 'Fall step 2' and 'Retargeting - Sales - Step 3' optimise on custom events and are deferred (12 Nov), and the client's own 'fall winter purchase 2026' (Sangeetha Ramkumar, 7 Oct) reads 13.9x. The Blended 30d line counts the deferred campaigns. No PMS connection, and no live pixel visible to HiddenGem (pixel check).

### Arca Boutique Hotel — AM Anna — account Arca Ad account (1003623765640520) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $0 over 30 days.

Blended 30d: no HiddenGem campaign spend in the window.

This month (booked 1 Nov–16 Nov): direct revenue $71,153 from 21 bookings, −17% vs 1 Oct–16 Oct ($85,453 from 29 bookings) · promo codes: not tracked by cloudbeds.

No live Lead Gen, Sales or Discovery campaigns with spend in the window.

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). Mapped 16 Nov. The first campaign, a $10/day giveaway, was created this morning (Ananya); nothing spent yet. Cloudbeds is connected: direct revenue month to date $71.2k from 21 bookings.

## Footer

- Windows: Lead Gen last 30 days, Sales/Retargeting last 14 days (live). CSV accounts use the export period 2026-10-19 to 2026-10-25 (7 days) and are provisional.
- Gates: $100 Lead Gen, $200 Sales/Retargeting. Campaigns under the gate are listed but not judged.
- Classification: by campaign objective (OUTCOME_LEADS → Lead Gen; OUTCOME_SALES → Sales, split into Retargeting (BoF) or MoF lookalike by name; OUTCOME_TRAFFIC / OUTCOME_ENGAGEMENT → ToF, not scored). CSV accounts have no objective column, so classification there is by name.
- Prospecting (MoF lookalike) sales campaigns are scored on the Retargeting ROAS bands because they optimise for purchases. The Benchmarks doc has no separate band for prospecting; Dustin floated a 3x floor on 28 Oct, not yet adopted.
- Scope (Shawal, 2026-11-04): only Sales-objective campaigns carry a state. Lead Gen rows and the Discovery bucket row are context only; they never enter Action needed, Scale candidates or the counts. Rows that were Flag or Review last week on CPL or promo ROAS read "No longer scored" in the diff.
- Discovery bucket (from 2026-10-30, Meta Ads Strategy 2026-10-28; context only since 2026-11-04): one row per client combining the 30-day spend of every HiddenGem ToF (giveaway, keyword) and Lead Gen campaign that spent in the window, paused ones included, against the 30-day revenue of direct bookings carrying a sign-up promo code (WELCOME*, ENJOY*, SIGNUP*, GIVEAWAY*) from the HiddenGem AI platform (pms_mtd.sql). Other codes (VIP, WELCOMEBACK, RETURNING, EARLY BIRD, agent or influencer codes) are listed in the row but not counted. Hostaway stores only a coupon id, so every coupon booking counts there. The promo ROAS is printed for reading only. Clients on a PMS that stores no promo code (Hospitable, Cloudbeds, OwnerRez, Newbook, Lodgify, Uplisting) show no promo data.
- Lead Gen CPL is not a state (28 Oct) and, since 4 Nov, neither is the zero-leads tracking check. CPL stays in the Governing metric column as a diagnostic and the Lead Gen investigate lines still apply.
- Blended 30d line per client: 30-day spend of every HiddenGem campaign against pixel purchase value (Sales rows, spend × ROAS) plus sign-up promo revenue. Not de-duplicated; it is the blended view Dustin asked to keep alongside the buckets, so a budget shift between buckets that lowers the blend is visible.
- Data path: Marketing API v21.0 insights at campaign level through `scripts/pull-campaign-insights.mts` (purchases = omni_purchase, leads = lead, ROAS = purchase_roas, link clicks = inline_link_clicks), the same fields the claude.ai connector exposed. The connector is no longer used for this report (Shawal, 2026-10-19).
- CTR on live rows is Meta's CTR (all clicks), not link CTR. The doc's click-rate lines are probably link CTR, so treat the CTR diagnostic as indicative.
- Frequency and cost per booking are diagnostics only and do not change the state (decision 2026-09-21). From 2026-10-06 (Shawal) every Sales / Retargeting row shows its frequency, and any value above 5.0 is marked ⚠️ in that column and listed in the Frequency watch section; CSV rows use impressions / reach summed over ad sets, which overstates frequency where ad sets overlap.
- Only campaigns live (ACTIVE) at run time are scored. Paused campaigns that spent inside the window are listed per client as "Paused in window" and never enter Action needed or the counts (decision 2026-09-23).
- Client-run campaigns (created by a non-HiddenGem login per the account activity log, listed under the client, never scored): Selah Place: SP / Willow / Pre-Sales / VIP List / 10-2026 (Nathan Jay Herrington), Instagram post: 🔥 𝐒𝐀𝐂𝐑𝐈𝐅𝐈𝐂𝐄 𝐈𝐒 𝐑𝐄𝐐𝐔𝐈𝐑𝐄𝐃 🔥... (Live Intentionally Today LIT), SP / Willow / Lead Gen / VIP List / 10-2026 (Nathan Jay Herrington), SP / Willow / Sales / Top-5 Audiences / 11-2026 (Nathan Jay Herrington), SP / Black Walnut / Sales / Pre-Sale / 11-2026 (Nathan Jay Herrington), SP / Black Walnut / Leads / Early Access / 11-2026 (Nathan Jay Herrington); Walden Retreats: TOF Wedding Leads 10.8.26 (Lindsey Cooke), MOF Wedding Leads 10.27.26 (Lindsey Cooke); Dunya Camp: fall winter purchase 2026 (Sangeetha Ramkumar). Creators are known for campaigns created in the last 180 days; older campaigns are scored as usual.
- Unclassified campaigns: none.
- Previous report: 2026-11-09-client-benchmark.csv. Diff joined on campaign_id for live rows and client + campaign name for CSV rows. Diff counts: 11 new, 2 still open, 2 fixed, 66 unchanged, 0 removed.
- Scope changes vs 9 Nov (Shawal, 16 Nov): Gooseberry Lodges, Dunya Camp and Arca Boutique Hotel mapped and added; Sunapee Stays reads Advanced in the CRM again, so its override is gone; Bison Ridge Retreat dropped (Basic in the CRM since 12 Nov). Advanced in the CRM but with no ad account mapping in PROJECT.md section 5, not scored: Treetop Hideaways (AM Kristal), Casey Key Resort (AM —), Nine Pines Retreat (AM Nicole), Lundy Farm (AM Charlotte), The Preserve (AM Alicia), Kimpton Mas Olas Resort (AM Charlotte). Gooseberry Lodges (no ads running yet, Shawal 9 Nov) and Nine Pines Retreats are on the Master Meta Ads sheet without an account ID.
- HG AI reports read from `HG AI Reports/` at the project root, dated since the previous run: none.
- Selah Place's campaigns are named with pipes in Meta ("SP | Willow | Sales | Top-5 Audiences | 11-2026"); shown here with slashes.
- Meeting notes: every "Meta Ads Strategy", "Meta Ads Sync" or "Meta Ads x HiddenGem AI Sync" calendar event since the previous run that has a "Notes by Gemini" attachment, read via Drive. Client names are matched with an alias list (Flow Home = FLOHOM, Tabber / Tipik Falls / Debug Falls = Tàberg Falls, Sailor Place = Selah Place, Stay on 38 = Stay On 30A, Ashwood River Cabins = Asheville River Cabins).
- This month line: direct booking revenue by booking date from the HiddenGem AI platform (pms_bookings, platform direct/OTA rules, tenants on a shared PMS account narrowed to their own properties), month to date at the run date, against the same day span of the previous month. Promo codes come from the booking payload: Guesty stores the code, Hostaway only a coupon id (counted, no names), Hospitable and Cloudbeds nothing. Pulled with pms_mtd.sql through the Supabase connector. Clients without a PMS connection on the platform show no figures.
- Monthly ROI context from `Monthly ROI data/` (July 2026, August 2026, September 2026, October 2026). Revenue there comes from the Client Performance Tracking sheet, not the pixel, so its ROAS is not comparable to the pixel ROAS above.
