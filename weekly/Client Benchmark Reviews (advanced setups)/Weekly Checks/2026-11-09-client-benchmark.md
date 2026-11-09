# Client Benchmark Review (advanced setups) — 2026-11-09

Run: 9 November 2026 (Monday), eighth run, compared against 2026-11-02-client-benchmark.csv. Live reads through the Meta Marketing API with the HiddenGem-Claude system user, the standing data path (`scripts/pull-campaign-insights.mts`, 07:57 to 08:00 PT); every account is live and the CSV export 2026-10-19 to 2026-10-25 was not needed for scoring. Scope: clients marked **Advanced** in the CRM "Meta Ads" column (Clients - Onboarding tab), re-read today: 33 clients, 24 with an ad account, the same 24 as on 2 Nov (Sunapee Stays stays in at Shawal's request although the CRM reads Basic). 9 Advanced clients in the CRM have no ad account yet; The Preserve and Kimpton Mas Olas Resort are new on that list this week. Scoring as since 4 Nov: Sales-objective campaigns only (Retargeting, Prospecting, Sales, on 14-day pixel ROAS); Lead Gen rows and the Discovery bucket row stay in each client's table for context with no state. Changes made in the accounts since last Monday come from each account's Meta activity log, and ROAS is read against this week's pixel check where duplicate Purchases inflate it (Selah Place, Ridge & Falls, Ponderosa) or missing Purchases deflate it (Little River Landing).

| Advanced clients | Live reads | From CSV | Rows scored | Under spend gate | Flag to Shawal | Review w/ HG AI | Monitor | Healthy | Scale w/ HG AI | Frequency over 5 | Not scored (lead gen) | Not scored (discovery) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 24 (+9 unmapped) | 24 | 0 | 21 | 10 | 3 | 1 | 5 | 5 | 7 | 2 | 21 | 24 |

States come from the Decision Making table in the Benchmarks doc and apply to Sales-objective campaigns only (Shawal, 4 Nov 2026): Retargeting, Prospecting and Sales campaigns on 14-day pixel ROAS with a $200 gate. Bands: above 15x Scale, 8–15x Healthy, 5–8x Monitor, 2–5x Review, under 2x or zero purchases Flag, inclusive on the lower bound. Lead Gen rows (leads, CPL) and the Discovery bucket row (giveaway + lead spend against 30-day sign-up promo-code revenue from the PMS) are listed under each client for context and carry no state.

## Weekly Meta Ads meetings since last run (Notes by Gemini)

Source: "Notes by Gemini" docs attached to the calendar events, read via Drive. Summary, decisions and next steps as Gemini wrote them; client-specific sentences are pulled into each client's section below. Transcript not used.

### Meta Ads Strategy — 2026-11-04 — doc `1YGFhUZLiLaM4gLPEVPwLOYxrQ3Ef78eO70ja_rXKnFo`

Strategic shift to independent luxury resorts and asset organization for The Preserve kickoff

Resort Targeting and PMS

Team discussed transitioning toward independent resorts and boutique hotels generating over 1000000 dollars monthly. Discussion covered PMS integration limitations with Res Nexus and Guestie.

Content and Compliance Strategy

Team reviewed high-definition video assets and planned custom landing pages for sample reels. Compliance checks using Claude were proposed to avoid Meta ad bans on sporting club content.

Kickoff and NDA Guidelines

Team coordinated asset downloading and scheduling for the upcoming client kickoff call. Strict adherence to non disclosure agreement guidelines was emphasized for public sharing restrictions.

Decisions:
- Follower Giveaway Proposal Strategy The participants discussed proposing a follower giveaway on the kickoff call while noting they would fall back to lookalike and retargeting ads if the client declines.
- Adopting Independent Resorts As Focus The group aligned on making independent resorts and boutique hotels their primary target market moving forward.
- Custom Coded Sample Page Creation The team agreed to create a custom-coded landing page showcasing multiple sample reel categories rather than using a Google Drive link.
- Meta Terms Compliance Content Filtering The team decided to run all content photos and video clips through an analysis with Claude against Meta terms of service to remove flagged material.
- Migrating and organizing client asset drive The team aligned on downloading all client assets and copying them into their own shared drive to be organized by Alicia and Makenna.

Next steps:
- [Leshan, Gillian] Request PMS Exception: Contact the availability exchange partner for Res Nexus to request an exception regarding API access for lower client counts.
- [Leshan] Verify Meta Tracking: Confirm the connection and proper Meta ad tracking for The Preserve to integrate data with Hidden AI.
- [Aiden, Makenna, Alicia] Organize Client Footage: Filter and categorize raw footage provided by the client into distinct themes including wedding, off-roading, and Hobbit house content.
- [Anton] Create Landing Page: Build a custom landing page to host and display organized sample content reels for client review.
- [Leshan Patterson] Analyze Meta Policies: Run all photos and video clips through artificial intelligence tools to identify potential Meta policy violations. Communicate any worrisome or flagged content for removal or adjustment.
- [Dustin Baker] Estimate Booking Metrics: Use artificial intelligence to analyze the resort website and determine the average daily rate and average booking value.
- [Dustin Baker] Send Kickoff Link: Resend the link for the kickoff call to the clients to ensure they receive it and book a slot.
- [Alicia Morin, Makenna Moran] Organize Client Assets: Download all provided client assets and store them in the team drive. Sort and structure the content into categories for easy review.
- [Anton] Create Reels: Produce 3 voiceover reels for each category including Bentley, Hobbit House, Christmas, and wedding themes. Create additional samples specifically showcasing the restaurant.
- [Dustin Baker] Verify NDA Scope: Consult artificial intelligence to clarify the non-disclosure agreement regarding publicly referencing the client partnership in sales calls.
- [The group] Coordinate Asset Downloads: Post updates in the team chat regarding which asset folders have been downloaded to facilitate collaborative task completion.

## Action needed

Sales-objective campaigns only (Retargeting, Prospecting, Sales; Shawal, 4 Nov 2026). Flag to Shawal before Review w/ HG AI, highest spend first.

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| Endless Stays | Nicole | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $1,034 / 14d | ROAS — | Flag to Shawal | Still open, week 6 (was Review w/ HG AI) |
| AwayFrames | Alicia | MoF - Lookalike Sales Campaign - 10/29/2026 | Prospecting (MoF lookalike) | $550 / 14d | ROAS 1.9x | Flag to Shawal | Still open, week 2 |
| Little River Landing | Makenna | BoF - Sales Campaign - Retargeting Website Visitors - 09/16/2026 | Retargeting (BoF) | $212 / 14d | ROAS — | Flag to Shawal | New flag, was Under gate |
| FLOHOM | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $693 / 14d | ROAS 3.7x | Review w/ HG AI | New flag, was Monitor |

## Scale candidates

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| Paradise Pointe | Makenna | MoF - LoL Sales Campaign - 09/28/26 | Prospecting (MoF lookalike) | $694 / 14d | ROAS 23.0x | Scale w/ HG AI | Was Healthy |
| Starlight Haven Weiss Lake | Charlotte | Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | $619 / 14d | ROAS 26.2x | Scale w/ HG AI | Unchanged |
| Treetop Escapes | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $560 / 14d | ROAS 18.1x | Scale w/ HG AI | Unchanged |
| Asheville River Cabins | Charlotte | BoF - Website Retargeting Campaign - 06/08/26 | Retargeting (BoF) | $429 / 14d | ROAS 26.4x | Scale w/ HG AI | Was Monitor |
| Stay Saluda NC | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $415 / 14d | ROAS 20.1x | Scale w/ HG AI | Was Healthy |
| Starlight Haven Hot Springs | Charlotte | Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | $277 / 14d | ROAS 15.5x | Scale w/ HG AI | Unchanged |
| Ridge & Falls | Makenna | BoF - Sales Campaign - Retargeting Website Visitors - 09/01/26 | Retargeting (BoF) | $210 / 14d | ROAS 19.5x | Scale w/ HG AI | Was Under gate |

## Frequency watch (Sales / Retargeting above 5)

Sales, Retargeting and MoF-lookalike campaigns whose 14-day frequency is above 5.0 (Shawal, 6 Oct 2026). Frequency does not change the ROAS state; this is the list to refresh creative or widen the audience on. The diagnostics column still notes anything above 3.0.

| Client | AM | Campaign | Type | Frequency | Spend / window | Governing metric | State |
|---|---|---|---|---|---|---|---|
| Paradise Pointe | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 5.68 | $695 / 14d | ROAS 15.0x | Healthy |
| Ridge & Falls | Makenna | BoF - Sales Campaign - Retargeting Website Visitors - 09/01/26 | Retargeting (BoF) | 5.21 | $210 / 14d | ROAS 19.5x | Scale w/ HG AI |

## Per client, ordered by scored MoF + BoF spend

### Stay On 30A — AM Charlotte — account Stay on 30a Ads (25640434272252212) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $2,989 over 30 days.

Blended 30d (every HiddenGem campaign): spend $15,028; pixel purchase value $157,634 + sign-up promo revenue $57,361 = $214,995, ROAS 14.3x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $97,383 from 32 bookings, +25% vs 1 Oct–9 Oct ($77,986 from 27 bookings) · promo codes: 17 uses (EARLY BIRD DIRECT ×8, WELCOME100 ×5, VIP100 ×4, WELCOMEBACK15 ×2, ESCAPE30A ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Sales Campaign - HiddenGem Pixel LoL - 07/17/26 | Prospecting (MoF lookalike) | 14d | $2,772 | 6 purchases | ROAS 13.9x | 1.67 | Healthy | CPC $1.08 > $0.62; CPM $24.25 > $16.50; cost/booking $462.08 > $90 | 30d ROAS 15.1x, 15 purchases | Was Scale w/ HG AI |
| BoF - Sales Campaign - RT Website Visitors - 07/13/26 | Retargeting (BoF) | 14d | $2,082 | 8 purchases | ROAS 14.7x | 3.76 | Healthy | CPC $2.12 > $0.62; CPM $30.58 > $16.50; cost/booking $260.31 > $90; freq 3.8 > 3.0 | 30d ROAS 14.8x, 18 purchases | Unchanged |
| MoF - Lead Campaign - RT Engagers - 07/16/26 | Lead Gen (MoF) | 30d | $1,498 | 978 leads | CPL $1.53 (diagnostic) | — | Not scored (lead gen) | CPC $0.43 > $0.30; CPM $39.54 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.57 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $4,487 | 12 promo bookings, $57,361 | promo ROAS 12.8x | — | Not scored (discovery) | WELCOME100 ×12 $57,361; not counted (not sign-up codes): EARLY BIRD DIRECT ×32 $184,830, VIP100 ×15 $45,382, WELCOMEBACK15 ×5 $11,221, RETURNINGGUEST ×1 $9,465, CINDYSWANSON10 ×1 $5,950, SNOWBIRD30A ×1 $3,400, TUCKS20 ×1 $2,173, 10%COAST ×1 $1,199, ESCAPE30A ×1 $1,196 | $4,487 in 30 days across ToF - Giveaway Traffic Campaign - 02/05/2026, MoF - Lead Campaign - RT Engagers - 07/16/26, against direct bookings booked 10 Oct–9 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $6,407, 67 Meta-attributed bookings, blended ROAS 32.3x, retargeting ROAS 14.6x, CPL $1.24 on 583 leads · August: spend $12,420, 85 Meta-attributed bookings, blended ROAS 17.8x, retargeting ROAS 15.5x, CPL $2.58 on 594 leads · September: spend $12,606, 91 Meta-attributed bookings, blended ROAS 24.4x, retargeting ROAS 23.1x, CPL $1.52 on 1001 leads · October: spend $15,161, 51 Meta-attributed bookings, blended ROAS 15.5x, retargeting ROAS 17.2x, CPL $1.47 on 1036 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). The lookalike slips from Scale (17.3x) to Healthy at 13.9x on 6 purchases ($2,772 in 14 days, the largest Sales spend in the review); BoF holds Healthy at 14.7x on 8 purchases ($2,082), frequency 3.8. Budget unchanged at $500/day. Direct revenue month to date $97.4k, +25% on the same days of October. Pixel: 70 Purchase against 67 PMS online bookings (Guesty CAPI).

### Tàberg Falls — AM Alicia — account Táberg Falls (827872700004659) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,611 over 30 days.

Blended 30d (every HiddenGem campaign): spend $7,667; pixel purchase value $39,386 + sign-up promo revenue $0 = $39,386, ROAS 5.1x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $23,256 from 14 bookings, +25% vs 1 Oct–9 Oct ($18,541 from 14 bookings) · promo codes: 0 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Website Retargeting Campaign - 08/21/2026 | Retargeting (BoF) | 14d | $1,241 | 5 purchases | ROAS 7.3x | 3.02 | Monitor | CPC $0.76 > $0.62; CPM $22.76 > $16.50; cost/booking $248.16 > $90; freq 3.0 > 3.0 | 30d ROAS 11.3x, 12 purchases | Was Healthy |
| MoF - Lookalike Sales Campaign - 08/21/2026 | Prospecting (MoF lookalike) | 14d | $1,166 | 4 purchases | ROAS 6.0x | 1.53 | Monitor | CPM $16.65 > $16.50; cost/booking $291.43 > $90 | 30d ROAS 7.4x, 9 purchases | Fixed, was Review w/ HG AI |
| MoF - Leads Campaign - 06/19/26 | Lead Gen (MoF) | 30d | $1,394 | 2457 leads | CPL $0.57 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.53 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $3,005 | 0 promo bookings, $0 | promo ROAS 0.0x | — | Not scored (discovery) | 0 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $3,005 in 30 days across MoF - Leads Campaign - 06/19/26, ToF - Giveaway Campaign - 07/08/2026, against direct bookings booked 10 Oct–9 Nov with a sign-up code; no sign-up promo bookings in 30 days; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Paused in window, not scored: MoF - Broad (Acquire new customers) - 09/28/2026 (Prospecting (MoF lookalike)), $464 / 14d, 0 purchases, ROAS —. Live campaigns only are scored (decision 2026-09-23).

Monthly ROI: July: spend $11,739, 80 Meta-attributed bookings, blended ROAS 9.5x, retargeting ROAS 15.8x, CPL $0.67 on 2320 leads · August: spend $11,259, 48 Meta-attributed bookings, blended ROAS 6.3x, retargeting ROAS 8.0x, CPL $0.46 on 4015 leads · September: spend $10,800, 42 Meta-attributed bookings, blended ROAS 5.6x, retargeting ROAS 7.1x, CPL $0.55 on 3261 leads · October: spend $8,391, 34 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 8.3x, CPL $0.58 on 2779 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). Lookalike Fixed: from Review (2.1x) to Monitor at 6.0x on 4 purchases ($1,166), its second week at $100/day. BoF slips from Healthy (12.0x) to Monitor at 7.3x on 5 purchases ($1,241). Discovery read (context only) 0.0x: $3,005 of giveaway and lead spend in 30 days and not one Hostaway coupon booking, so the sign-up code is either unused or not reaching the PMS; worth Alicia checking the code works on the booking engine. Direct revenue month to date +25% on October. Pixel: 31 Purchase against 38 PMS online bookings (82%).

### Endless Stays — AM Nicole — account Endless Stays (896372356081479) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $2,244 over 30 days.

Blended 30d (every HiddenGem campaign): spend $5,975; pixel purchase value $6,278 + sign-up promo revenue $0 = $6,278, ROAS 1.1x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $20,141 from 11 bookings, +56% vs 1 Oct–9 Oct ($12,925 from 9 bookings) · promo codes: not tracked by hospitable.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $1,034 | 0 purchases | ROAS — | 2.27 | Flag to Shawal | CPC $0.64 > $0.62; CPM $17.93 > $16.50 | no purchases; 30d ROAS 2.8x, 2 purchases | Still open, week 6 (was Review w/ HG AI) |
| MoF Lead Campaign - Retargeting Engagers - 09/09/2026 | Lead Gen (MoF) | 30d | $1,495 | 1562 leads | CPL $0.96 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.03 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $3,739 | — | promo ROAS — | — | Not scored (discovery) | — | $3,739 in 30 days across ToF - Giveaway Traffic Campaign - AZ, FL, VA, PA, TN, MoF Lead Campaign - Retargeting Engagers - 09/09/2026; hospitable does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $1,534, 9 Meta-attributed bookings, blended ROAS 16.0x · August: spend $1,553, 10 Meta-attributed bookings, blended ROAS 11.6x, retargeting ROAS 38.8x, CPL $9.73 on 26 leads · September: spend $2,539, 6 Meta-attributed bookings, blended ROAS 2.9x, retargeting ROAS 4.7x, CPL $1.05 on 532 leads · October: spend $6,184, 5 Meta-attributed bookings, blended ROAS 2.6x, retargeting ROAS 3.3x, CPL $0.89 on 1715 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF goes from Review (4.2x, five weeks) to Flag: 0 purchases attributed on $1,034 in 14 days (2 purchases, 2.8x over 30). The PMS shows 16 online bookings in 28 days and month-to-date direct revenue is +56% on October, and the pixel's 13 Purchases all arrive server-side from the HG AI CAPI with no browser Purchase on the booking confirmation, so the gap looks like attribution as much as performance. Question for Nicole and Shawal: hold BoF at $75/day while the confirmation page gets a browser Purchase, or cut it.

### AwayFrames — AM Alicia — account Awayframes Ad Account (2471256056603833) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,100 over 30 days.

Blended 30d (every HiddenGem campaign): spend $3,291; pixel purchase value $10,263 + sign-up promo revenue $3,270 = $13,533, ROAS 4.1x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $9,916 from 7 bookings, +194% vs 1 Oct–9 Oct ($3,377 from 4 bookings) · promo codes: 0 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lookalike Sales Campaign - 10/29/2026 | Prospecting (MoF lookalike) | 14d | $550 | 1 purchases | ROAS 1.9x | 1.31 | Flag to Shawal | CPC $0.94 > $0.62; CPM $17.15 > $16.50; cost/booking $549.56 > $90 | 30d ROAS 1.9x, 1 purchases | Still open, week 2 |
| BoF - Sales Campaign - Retargeting Website Visitors 07/31/2026 | Retargeting (BoF) | 14d | $696 | 7 purchases | ROAS 7.3x | 4.79 | Monitor | CPC $1.50 > $0.62; CPM $18.49 > $16.50; CTR 1.96% < 2%; cost/booking $99.49 > $90; freq 4.8 > 3.0 | 30d ROAS 11.9x, 10 purchases | Was Scale w/ HG AI |
| MoF - Lead Campaign - Retargeting Engagers 07/31/2026 | Lead Gen (MoF) | 30d | $865 | 588 leads | CPL $1.47 (diagnostic) | — | Not scored (lead gen) | CPC $0.32 > $0.30 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.46 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,965 | 2 promo bookings, $3,270 | promo ROAS 1.7x | — | Not scored (discovery) | 2 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $1,965 in 30 days across ToF - Giveaway Traffic Campaign - 07/31/2026, MoF - Lead Campaign - Retargeting Engagers 07/31/2026, against direct bookings booked 10 Oct–9 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $923, 9 Meta-attributed bookings, blended ROAS 18.6x, CPL $2.44 on 2 leads · August: spend $869, 8 Meta-attributed bookings, blended ROAS 21.8x, retargeting ROAS 27.0x, CPL $2.68 on 58 leads · September: spend $895, 7 Meta-attributed bookings, blended ROAS 11.1x, retargeting ROAS 4.9x, CPL $1.83 on 82 leads · October: spend $1,898, 20 Meta-attributed bookings, blended ROAS 9.9x, retargeting ROAS 15.3x, CPL $1.56 on 316 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). The 10/29 lookalike stays Flag at 1.9x on 1 purchase ($550 in 14 days), second week. BoF drops from Scale (19.9x) to Monitor at 7.3x on 7 purchases ($696), frequency 4.8, in its first full fortnight at $50/day. Both follow the 29 Oct jump from $30 to $200/day. Bookings are rising anyway: month-to-date direct revenue $9.9k against $3.4k on the same days of October (+194%).

### Paradise Pointe — AM Makenna — account Paradise Pointe Ads (1585826092078255) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $748 over 30 days.

Blended 30d (every HiddenGem campaign): spend $4,492; pixel purchase value $45,878 + sign-up promo revenue $86,095 = $131,973, ROAS 29.4x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $42,105 from 40 bookings, +25% vs 1 Oct–9 Oct ($33,786 from 40 bookings) · promo codes: 21 uses (WELCOME100 ×21).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $695 | 8 purchases | ROAS 15.0x | 5.68 ⚠️ > 5 | Healthy | CPC $0.89 > $0.62; freq 5.7 > 3.0 | 30d ROAS 15.4x, 27 purchases | Was Scale w/ HG AI |
| MoF - LoL Sales Campaign - 09/28/26 | Prospecting (MoF lookalike) | 14d | $694 | 12 purchases | ROAS 23.0x | 2.09 | Scale w/ HG AI | within lines | 30d ROAS 15.3x, 26 purchases | Was Healthy |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $747 | 710 leads | CPL $1.05 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.08 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,496 | 72 promo bookings, $86,095 | promo ROAS 57.6x | — | Not scored (discovery) | WELCOME100 ×69 $81,546, WELCOME10 ×3 $4,549; not counted (not sign-up codes): VIP100 ×2 $2,698 | $1,496 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Giveaway Traffic Campaign, against direct bookings booked 10 Oct–9 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $2,237, 74 Meta-attributed bookings, blended ROAS 21.6x, retargeting ROAS 16.7x, CPL $1.01 on 90 leads · August: spend $3,109, 113 Meta-attributed bookings, blended ROAS 23.1x, retargeting ROAS 18.0x, CPL $1.64 on 471 leads · September: spend $3,074, 98 Meta-attributed bookings, blended ROAS 28.8x, retargeting ROAS 13.0x, CPL $0.97 on 764 leads · October: spend $4,651, 124 Meta-attributed bookings, blended ROAS 21.5x, retargeting ROAS 9.8x, CPL $1.03 on 746 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). The LoL lookalike moves up from Healthy (12.7x) to Scale at 23.0x on 12 purchases ($694). BoF dips from Scale (25.0x) to Healthy at 15.0x, just under the Scale line, on 8 purchases ($695); its frequency of 5.68 is the highest in the review (Frequency watch, second week). Discovery read (context only) 57.6x: WELCOME100 ×69 ($81.5k) on $1,496.

### Treetop Escapes — AM Makenna — account Treetop Escapes Ads (967636478877602) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $902 over 30 days.

Blended 30d (every HiddenGem campaign): spend $3,011; pixel purchase value $17,652 + sign-up promo revenue $22,121 = $39,773, ROAS 13.2x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $19,140 from 19 bookings, +34% vs 1 Oct–9 Oct ($14,276 from 17 bookings) · promo codes: 7 uses (WELCOME100 ×6, WELCOME10 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $560 | 12 purchases | ROAS 18.1x | 3.50 | Scale w/ HG AI | freq 3.5 > 3.0 | 30d ROAS 14.6x, 19 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $901 | 1175 leads | CPL $0.77 (diagnostic) | — | Not scored (lead gen) | CPM $17.71 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.75 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,803 | 18 promo bookings, $22,121 | promo ROAS 12.3x | — | Not scored (discovery) | WELCOME100 ×16 $17,354, WELCOME10 ×2 $4,767; not counted (not sign-up codes): VIP100 ×1 $1,435 | $1,803 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Giveaway Traffic Campaign, against direct bookings booked 10 Oct–9 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $2,487, 44 Meta-attributed bookings, blended ROAS 14.5x, retargeting ROAS 22.2x, CPL $1.48 on 21 leads · August: spend $3,082, 33 Meta-attributed bookings, blended ROAS 12.3x, retargeting ROAS 16.3x, CPL $1.49 on 620 leads · September: spend $2,998, 23 Meta-attributed bookings, blended ROAS 7.9x, retargeting ROAS 7.9x, CPL $0.88 on 1019 leads · October: spend $3,081, 32 Meta-attributed bookings, blended ROAS 10.9x, retargeting ROAS 11.8x, CPL $0.79 on 1164 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF holds Scale at 18.1x on 12 purchases ($560), frequency 3.5. Discovery read (context only) 12.3x: WELCOME100 ×16 and WELCOME10 ×2 on $1,803.

### Ponderosa Pines Resort — AM Anna — account Ponderosa Pines Resort (1058846326445255) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,195 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,984; pixel purchase value $9,656 + sign-up promo revenue $0 = $9,656, ROAS 3.2x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $15,844 from 51 bookings, +66% vs 1 Oct–9 Oct ($9,552 from 42 bookings) · promo codes: not tracked by newbook.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Website Retarget Campaign - 07/13/26 | Retargeting (BoF) | 14d | $552 | 13 purchases | ROAS 7.4x | 2.59 | Monitor | CPC $0.74 > $0.62; CPM $20.61 > $16.50 | 30d ROAS 8.1x, 28 purchases | Was Healthy |
| Leads Campaign - 07/16/26 | Lead Gen (MoF) | 30d | $600 | 493 leads | CPL $1.22 (diagnostic) | — | Not scored (lead gen) | CPC $0.32 > $0.30; CPM $17.03 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.17 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,796 | — | promo ROAS — | — | Not scored (discovery) | — | $1,796 in 30 days across Discovery Campaign - Giveaway - June 2026, Leads Campaign - 07/16/26; newbook does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $2,089, 17 Meta-attributed bookings, blended ROAS 3.6x, retargeting ROAS 22.3x, CPL $0.91 on 356 leads · August: spend $3,101, 103 Meta-attributed bookings, blended ROAS 15.0x, retargeting ROAS 21.3x, CPL $1.32 on 471 leads · September: spend $2,985, 119 Meta-attributed bookings, blended ROAS 17.9x, retargeting ROAS 21.6x, CPL $0.84 on 708 leads · October: spend $3,065, 39 Meta-attributed bookings, blended ROAS 6.0x, retargeting ROAS 12.5x, CPL $1.02 on 601 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF slips from Healthy (10.5x) to Monitor at 7.4x on 13 purchases ($552). Read the ROAS as an upper bound: the pixel check shows the Newbook confirmation firing about 1.7 browser Purchases per PMS booking, so attributed purchases and value are inflated. Leads $1.22 on 493. No promo data (Newbook stores no code).

### Starlight Haven Hot Springs — AM Charlotte — account Starlight Haven Hot Springs (901138032027913) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $751 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,250; pixel purchase value $10,189 + sign-up promo revenue $0 = $10,189, ROAS 4.5x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $277 | 6 purchases | ROAS 15.5x | 2.12 | Scale w/ HG AI | within lines | 30d ROAS 17.0x, 15 purchases | Unchanged |
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $899 | 2753 leads | CPL $0.33 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.32 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,650 | — | promo ROAS — | — | Not scored (discovery) | — | $1,650 in 30 days across Discovery Campaign - Giveaway - 12/16/2025, New Leads Campaign - 03/03/26; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $2,160, 17 Meta-attributed bookings, blended ROAS 5.1x, retargeting ROAS 17.1x, CPL $0.33 on 2813 leads · August: spend $2,193, 19 Meta-attributed bookings, blended ROAS 6.3x, retargeting ROAS 22.3x, CPL $0.36 on 2589 leads · September: spend $2,155, 61 Meta-attributed bookings, blended ROAS 16.5x, retargeting ROAS 28.5x, CPL $0.34 on 2597 leads · October: spend $2,298, 71 Meta-attributed bookings, blended ROAS 21.0x, retargeting ROAS 22.1x, CPL $0.32 on 2869 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF stays Scale at 15.5x on 6 purchases ($277), down from 24.2x and just above the Scale line. Leads $0.33 on 2,753.

### FLOHOM — AM Makenna — account FLOHOM Ads (2100710320122219) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $299 over 30 days.

Blended 30d (every HiddenGem campaign): spend $4,649; pixel purchase value $33,631 + sign-up promo revenue $22,584 = $56,215, ROAS 12.1x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $13,845 from 17 bookings, −66% vs 1 Oct–9 Oct ($40,832 from 47 bookings) · promo codes: 7 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $693 | 4 purchases | ROAS 3.7x | 2.33 | Review w/ HG AI | CPM $17.84 > $16.50; cost/booking $173.21 > $90 | 30d ROAS 4.7x, 11 purchases | New flag, was Monitor |
| MoF - Lookalike Sales Campaign - 07/29/26 | Prospecting (MoF lookalike) | 14d | $693 | 9 purchases | ROAS 12.0x | 2.22 | Healthy | CPM $18.48 > $16.50 | 30d ROAS 13.0x, 22 purchases | Was Scale w/ HG AI |
| [Myrtle Beach] MoF - Lookalike Sales Campaign - 09/17/26 | Prospecting (MoF lookalike) | 14d | $277 | 1 purchases | ROAS 8.2x | 2.29 | Healthy | CPC $1.13 > $0.62; CPM $21.63 > $16.50; cost/booking $277.40 > $90 | 30d ROAS 6.6x, 2 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers – 08/17/26 | Lead Gen (MoF) | 30d | $363 | 640 leads | CPL $0.57 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.54 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $663 | 23 promo bookings, $22,584 | promo ROAS 34.1x | — | Not scored (discovery) | 23 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $663 in 30 days across ToF - Giveaway Traffic Campaign, MoF - Lead Campaign - Retargeting Engagers – 08/17/26, against direct bookings booked 10 Oct–9 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $5,555, 103 Meta-attributed bookings, blended ROAS 17.2x, retargeting ROAS 19.1x, CPL $7.66 on 66 leads · August: spend $9,331, 90 Meta-attributed bookings, blended ROAS 8.5x, retargeting ROAS 8.2x, CPL $2.24 on 708 leads · September: spend $8,855, 82 Meta-attributed bookings, blended ROAS 8.9x, retargeting ROAS 8.9x, CPL $0.50 on 2192 leads · October: spend $5,455, 71 Meta-attributed bookings, blended ROAS 12.0x, retargeting ROAS 9.7x, CPL $0.56 on 809 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF slips from Monitor (5.3x) to Review at 3.7x on 4 purchases ($693 in 14 days; 4.7x over 30), a new Action row. The main lookalike drops from Scale (19.8x) to Healthy at 12.0x on 9 purchases; the Myrtle Beach lookalike holds Healthy at 8.2x. Month-to-date direct revenue is $13.8k, −66% on the same days of October (17 bookings against 47), so the lower ROAS tracks a slower booking month, not a tracking change: the pixel still captures 99% of online bookings. Budget $140/day, matching the November target.

### Stay Saluda NC — AM Makenna — account Stay Saluda Ads (1863632561215857) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $896 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,387; pixel purchase value $9,398 + sign-up promo revenue $14,784 = $24,182, ROAS 10.1x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $9,928 from 15 bookings, +49% vs 1 Oct–9 Oct ($6,683 from 11 bookings) · promo codes: 10 uses (ENJOY10 ×8, VIP10 ×2).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $415 | 12 purchases | ROAS 20.1x | 4.44 | Scale w/ HG AI | CPC $0.79 > $0.62; CPM $18.11 > $16.50; freq 4.4 > 3.0 | 30d ROAS 10.5x, 15 purchases | Was Healthy |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $595 | 628 leads | CPL $0.95 (diagnostic) | — | Not scored (lead gen) | CPM $14.95 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.99 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,490 | 18 promo bookings, $14,784 | promo ROAS 9.9x | — | Not scored (discovery) | ENJOY10 ×15 $10,352, WELCOME10 ×3 $4,432; not counted (not sign-up codes): VIP10 ×2 $1,298, DUBLE10 ×1 $273 | $1,490 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Giveaway Traffic Campaign - NC/SC/GA/TN, against direct bookings booked 10 Oct–9 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $2,140, 10 Meta-attributed bookings, blended ROAS 2.6x, retargeting ROAS 0.8x · August: spend $2,367, 10 Meta-attributed bookings, blended ROAS 3.9x, retargeting ROAS 5.2x, CPL $2.59 on 146 leads · September: spend $2,394, 14 Meta-attributed bookings, blended ROAS 3.8x, retargeting ROAS 3.5x, CPL $1.00 on 596 leads · October: spend $2,449, 25 Meta-attributed bookings, blended ROAS 7.0x, retargeting ROAS 5.7x, CPL $0.94 on 647 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF up from Healthy (8.1x) to Scale at 20.1x on 12 purchases ($415), frequency 4.4. Discovery read (context only) 9.9x: ENJOY10 ×15 and WELCOME10 ×3 on $1,490.

### Little River Landing — AM Makenna — account Little River Landing (884285717873613) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,786 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,274; pixel purchase value $393 + sign-up promo revenue $393 = $786, ROAS 0.3x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $1,096 from 7 bookings, +42% vs 1 Oct–9 Oct ($770 from 4 bookings) · promo codes: 0 uses.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 09/16/2026 | Retargeting (BoF) | 14d | $212 | 0 purchases | ROAS — | 3.22 | Flag to Shawal | CPC $0.69 > $0.62; freq 3.2 > 3.0 | no purchases; 30d ROAS 1.2x, 1 purchases | New flag, was Under gate |
| MoF - Lead Campaign - Retargeting Engagers - 09/16/2026 | Lead Gen (MoF) | 30d | $149 | 84 leads | CPL $1.78 (diagnostic) | — | Not scored (lead gen) | CPC $0.46 > $0.30; CPM $22.56 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.82 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,936 | 1 promo bookings, $393 | promo ROAS 0.2x | — | Not scored (discovery) | WELCOME10 ×1 $393 | $1,936 in 30 days across ToF - Giveaway Traffic Campaign - AL - 09/16/2026, MoF - Lead Campaign - Retargeting Engagers - 09/16/2026, against direct bookings booked 10 Oct–9 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: September: spend $921, 0 Meta-attributed bookings, blended ROAS —, retargeting ROAS —, CPL $1.86 on 46 leads · October: spend $2,165, 1 Meta-attributed bookings, blended ROAS 0.2x, retargeting ROAS 1.5x, CPL $1.50 on 101 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF crosses the $200 gate with 0 purchases ($212 in 14 days), a new Flag. Read it with the pixel check: Little River is ❌ on Purchase tracking (4 Purchase in 28 days against 13 PMS online bookings; HG AI CAPI off, the browser never fires Purchase), so the zero is mainly missing tracking. Turning the CAPI on comes before judging the campaign. Discovery read (context only) 0.2x: one WELCOME10 booking on $1,936 of giveaway and lead spend.

### Asheville River Cabins — AM Charlotte — account Asheville River Cabins Ads (615836588009747) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,212 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,431; pixel purchase value $24,613 + sign-up promo revenue $0 = $24,613, ROAS 10.1x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Website Retargeting Campaign - 06/08/26 | Retargeting (BoF) | 14d | $429 | 20 purchases | ROAS 26.4x | 2.20 | Scale w/ HG AI | CPM $16.93 > $16.50 | 30d ROAS 26.7x, 33 purchases | Was Monitor |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $298 | 902 leads | CPL $0.33 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.39 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,510 | — | promo ROAS — | — | Not scored (discovery) | — | $1,510 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Discovery Campaign Giveaway - 09/17/26; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $2,029, 39 Meta-attributed bookings, blended ROAS 18.6x, retargeting ROAS 51.6x · August: spend $2,424, 82 Meta-attributed bookings, blended ROAS 27.2x, retargeting ROAS 65.0x, CPL $0.42 on 605 leads · September: spend $2,252, 70 Meta-attributed bookings, blended ROAS 19.1x, retargeting ROAS 42.5x, CPL $0.30 on 936 leads · October: spend $2,233, 68 Meta-attributed bookings, blended ROAS 23.1x, retargeting ROAS 27.4x, CPL $0.32 on 869 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF up from Monitor (7.9x) to Scale at 26.4x on 20 purchases ($429), frequency 2.2; Dustin raised it from $30 to $50/day on 8 Nov. All of its Purchases are browser-side (no CAPI reaches the pixel), see the pixel check.

### Starlight Haven Weiss Lake — AM Charlotte — account Starlight Haven Weiss Lake (74756899) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $0 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,097; pixel purchase value $31,148 + sign-up promo revenue $0 = $31,148, ROAS 14.9x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $619 | 31 purchases | ROAS 26.2x | 2.61 | Scale w/ HG AI | CPC $0.83 > $0.62 | 30d ROAS 23.1x, 52 purchases | Unchanged |
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $749 | 663 leads | CPL $1.13 (diagnostic) | — | Not scored (lead gen) | CPC $0.36 > $0.30 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.00 | Unchanged |
| Discovery bucket (1 campaign: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $749 | — | promo ROAS — | — | Not scored (discovery) | — | $749 in 30 days across New Leads Campaign - 03/03/26; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $2,163, 41 Meta-attributed bookings, blended ROAS 10.8x, retargeting ROAS 15.2x, CPL $0.74 on 826 leads · August: spend $2,351, 36 Meta-attributed bookings, blended ROAS 10.7x, retargeting ROAS 17.6x, CPL $1.23 on 617 leads · September: spend $2,152, 79 Meta-attributed bookings, blended ROAS 17.4x, retargeting ROAS 23.8x, CPL $1.01 on 734 leads · October: spend $2,142, 53 Meta-attributed bookings, blended ROAS 15.6x, retargeting ROAS 24.2x, CPL $1.09 on 704 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF Scale at 26.2x on 31 purchases ($619), up from 19.6x. Leads $1.13 on 663.

### Ridge & Falls — AM Makenna — account Ridge & Falls ad account (1313401330776046) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,509 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,994; pixel purchase value $6,990 + sign-up promo revenue $0 = $6,990, ROAS 3.5x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $2,340 from 6 bookings, +121% vs 1 Oct–9 Oct ($1,057 from 3 bookings) · promo codes: 3 uses (HELLO10 ×2, STAY10 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 09/01/26 | Retargeting (BoF) | 14d | $210 | 10 purchases | ROAS 19.5x | 5.21 ⚠️ > 5 | Scale w/ HG AI | freq 5.2 > 3.0 | 30d ROAS 20.7x, 15 purchases | Was Under gate |
| MoF - Lead Campaign - Retargeting Engagers - 09/01/26 | Lead Gen (MoF) | 30d | $148 | 68 leads | CPL $2.17 (diagnostic) | — | Not scored (lead gen) | CPC $0.33 > $0.30 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $2.31 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,656 | 0 promo bookings, $0 | promo ROAS 0.0x | — | Not scored (discovery) | no sign-up code bookings in 30 days; not counted (not sign-up codes): HELLO10 ×2 $926, STAY10 ×1 $412 | $1,656 in 30 days across ToF - Giveaway Traffic Campaign - GA, AL - 09/01/26, MoF - Lead Campaign - Retargeting Engagers - 09/01/26, against direct bookings booked 10 Oct–9 Nov with a sign-up code; no sign-up promo bookings in 30 days; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: September: spend $1,036, 0 Meta-attributed bookings, blended ROAS —, retargeting ROAS —, CPL $8.16 on 16 leads · October: spend $1,941, 10 Meta-attributed bookings, blended ROAS 2.5x, retargeting ROAS 18.7x, CPL $2.33 on 64 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF crosses the gate straight into Scale at 19.5x on 10 purchases ($210), with frequency 5.21 (Frequency watch). Treat the ROAS as inflated: the pixel receives about 1.8 server Purchases per PMS booking (HG AI CAPI plus a second sender), so Meta likely counts many bookings twice. Discovery read 0.0x: the only coded bookings were HELLO10 and STAY10, which are not sign-up codes.

### Selah Place — AM Alicia — account Selah.place (1275283434220508) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $850 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,029; pixel purchase value $5,823 + sign-up promo revenue $8,570 = $14,393, ROAS 7.1x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $7,355 from 17 bookings, −35% vs 1 Oct–9 Oct ($11,317 from 20 bookings) · promo codes: 6 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF-Website Retarget Campaign - 07/24/2026 | Retargeting (BoF) | 14d | $414 | 8 purchases | ROAS 5.6x | 4.45 | Monitor | CPC $0.72 > $0.62; CPM $23.43 > $16.50; freq 4.4 > 3.0 | 30d ROAS 6.5x, 15 purchases | Fixed, was Review w/ HG AI |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $283 | 432 leads | CPL $0.65 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.76 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,133 | 17 promo bookings, $8,570 | promo ROAS 7.6x | — | Not scored (discovery) | 17 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $1,133 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Giveaway Traffic Campaign - 08/07/2026, against direct bookings booked 10 Oct–9 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Client-run, not scored: SP / Willow / Pre-Sales / VIP List / 10-2026 (Sales, paused), created by Nathan Jay Herrington on 2026-10-19, $289 / 14d, 2 purchases, ROAS 0.3x. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: Instagram post: 🔥 𝐒𝐀𝐂𝐑𝐈𝐅𝐈𝐂𝐄 𝐈𝐒 𝐑𝐄𝐐𝐔𝐈𝐑𝐄𝐃 🔥... (Other, paused), created by Live Intentionally Today LIT on 2026-10-15, $42 / 14d, 0 purchases, ROAS —. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Willow / Lead Gen / VIP List / 10-2026 (Lead Gen (MoF), active), created by Nathan Jay Herrington on 2026-10-20, $934 / 30d, 603 leads, CPL $1.55. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Willow / Sales / Top-5 Audiences / 11-2026 (Sales, active), created by Nathan Jay Herrington on 2026-10-28, $1,720 / 14d, 13 purchases, ROAS 0.7x. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Black Walnut / Leads / Early Access / 11-2026 (Lead Gen (MoF), active), created by Nathan Jay Herrington on 2026-11-07, $178 / 30d, 15 leads, CPL $11.89. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Monthly ROI: July: spend $1,054, 4 Meta-attributed bookings, blended ROAS 3.2x, retargeting ROAS 86.3x, CPL $0.80 on 49 leads · August: spend $1,545, 15 Meta-attributed bookings, blended ROAS 4.8x, retargeting ROAS 25.1x, CPL $1.08 on 144 leads · September: spend $1,304, 27 Meta-attributed bookings, blended ROAS 10.4x, retargeting ROAS 38.2x, CPL $0.63 on 232 leads · October: spend $1,842, 23 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 9.7x, CPL $0.61 on 405 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). HiddenGem's BoF Fixed: from Review (3.9x) to Monitor at 5.6x on 8 purchases ($414), frequency 4.5. The pixel's server Purchases run 2.4x the PMS bookings (HG AI CAPI plus Hostaway's CAPI), so this ROAS is likely overstated too. The client now runs most of the account: Nathan Herrington's Willow Top-5 Audiences sales campaign ($175/day, 0.7x on $1,720 in 14 days) and, from 5 and 7 Nov, two Black Walnut campaigns ($130/day leads, $50/day sales) on a new Black Walnut pixel. HiddenGem's three campaigns are $70 of the account's $465/day.

### Sunapee Stays — AM Charlotte — account Sunapee Stays Ads Account (651114096215889) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $897 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,496; pixel purchase value $1,533 + sign-up promo revenue $0 = $1,533, ROAS 1.0x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $1,970 from 6 bookings, −85% vs 1 Oct–9 Oct ($13,540 from 25 bookings) · promo codes: not tracked by ownerrez.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $142 | 0 purchases | ROAS — | 2.87 | Under gate | CPC $0.86 > $0.62 | spend $142.00 < $200 gate; 30d ROAS 5.1x, 3 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $300 | 132 leads | CPL $2.27 (diagnostic) | — | Not scored (lead gen) | CPC $0.46 > $0.30; CPM $17.82 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $2.38 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,197 | — | promo ROAS — | — | Not scored (discovery) | — | $1,197 in 30 days across ToF Discovery Campaign - Giveaway - 06/10/26, MoF - Lead Campaign - Retargeting Engagers; ownerrez does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $939, 16 Meta-attributed bookings, blended ROAS 9.9x, CPL $2.06 on 9 leads · August: spend $1,494, 10 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 25.1x, CPL $2.74 on 112 leads · September: spend $1,495, 14 Meta-attributed bookings, blended ROAS 6.5x, retargeting ROAS 6.7x, CPL $1.64 on 184 leads · October: spend $1,540, 11 Meta-attributed bookings, blended ROAS 3.4x, retargeting ROAS 10.7x, CPL $1.89 on 161 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF under the gate, 0 purchases on $142 (5.1x over 30 days). Month-to-date direct revenue $2.0k against $13.5k on the same days of October (−85%).

### Green Springs Inn — AM Alicia — account Green Springs Inn (1390516335151357) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $601 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,199; pixel purchase value $4,376 + sign-up promo revenue $15,714 = $20,090, ROAS 16.8x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $16,161 from 31 bookings, +40% vs 1 Oct–9 Oct ($11,524 from 26 bookings) · promo codes: 11 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 08/28/26 | Retargeting (BoF) | 14d | $138 | 5 purchases | ROAS 20.0x | 3.08 | Under gate | CPC $0.73 > $0.62; freq 3.1 > 3.0 | spend $137.52 < $200 gate; 30d ROAS 14.6x, 9 purchases | Unchanged |
| MoF - Lead Campaign/08/28/2026 | Lead Gen (MoF) | 30d | $299 | 202 leads | CPL $1.48 (diagnostic) | — | Not scored (lead gen) | CPC $0.31 > $0.30 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $2.11 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $900 | 31 promo bookings, $15,714 | promo ROAS 17.5x | — | Not scored (discovery) | 31 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $900 in 30 days across ToF - Giveaway Traffic Campaign - 07/24/2026, MoF - Lead Campaign/08/28/2026, against direct bookings booked 10 Oct–9 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $1,222, 17 Meta-attributed bookings, blended ROAS 7.8x, retargeting ROAS 14.6x, CPL $5.65 on 8 leads · August: spend $1,247, 23 Meta-attributed bookings, blended ROAS 8.2x, retargeting ROAS 17.1x, CPL $9.09 on 34 leads · September: spend $1,199, 24 Meta-attributed bookings, blended ROAS 8.5x, retargeting ROAS 9.0x, CPL $1.84 on 166 leads · October: spend $1,231, 26 Meta-attributed bookings, blended ROAS 10.6x, retargeting ROAS 9.5x, CPL $1.42 on 214 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF under the gate at 20.0x on 5 purchases ($138). Discovery read (context only) 17.5x on 31 Hostaway coupon bookings (no code names).

### The Outpost — AM Anna — account The Outpost Grand Canyon (1530849534802936) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $897 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,197; pixel purchase value $601 + sign-up promo revenue $0 = $601, ROAS 0.5x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $3,410 from 9 bookings, −60% vs 1 Oct–9 Oct ($8,427 from 17 bookings) · promo codes: not tracked by newbook.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 10/08/2026 | Retargeting (BoF) | 14d | $142 | 1 purchases | ROAS 1.5x | 2.37 | Under gate | CPC $0.77 > $0.62; cost/booking $141.82 > $90 | spend $141.82 < $200 gate; 30d ROAS 2.0x, 2 purchases | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $897 | — | promo ROAS — | — | Not scored (discovery) | — | $897 in 30 days across Insta Discovery Campaign - Giveaway - May 2026, Facebook Discovery Campaign - Giveaway - May 2026; newbook does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $2,182, 1 Meta-attributed bookings, blended ROAS 0.2x, CPL $1.61 on 202 leads · August: spend $1,876, 7 Meta-attributed bookings, blended ROAS 2.1x, CPL $1.71 on 181 leads · September: spend $2,081, 18 Meta-attributed bookings, blended ROAS 3.8x, retargeting ROAS —, CPL $1.80 on 167 leads · October: spend $2,149, 12 Meta-attributed bookings, blended ROAS 2.8x, retargeting ROAS 1.9x, CPL $1.73 on 176 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). Only the 10/08 BoF spent ($142, 1 purchase, 1.5x), under the gate; the 08/29 BoF ($10/day) did not spend again, so it is idle (decision 30). Direct revenue month to date −60% on October.

### Walden Retreats — AM Anna — account Walden Retreats (973261794434226) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $301 over 30 days.

Blended 30d (every HiddenGem campaign): spend $904; pixel purchase value $7,223 + sign-up promo revenue $0 = $7,223, ROAS 8.0x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 06/10/2026 | Retargeting (BoF) | 14d | $139 | 4 purchases | ROAS 5.3x | 2.61 | Under gate | CPC $0.88 > $0.62; CPM $24.07 > $16.50 | spend $138.65 < $200 gate; 30d ROAS 23.7x, 13 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 10/06/2026 | Lead Gen (MoF) | 30d | $298 | 239 leads | CPL $1.25 (diagnostic) | — | Not scored (lead gen) | CPC $0.38 > $0.30; CPM $19.23 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.16 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $599 | — | promo ROAS — | — | Not scored (discovery) | — | $599 in 30 days across ToF - Giveaway Traffic Campaign - ATX, HTX, DAL, SATX, FTW - 10/05/2026, MoF - Lead Campaign - Retargeting Engagers - 10/06/2026; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Client-run, not scored: TOF Wedding Leads 10.8.26 (Lead Gen (MoF), paused), created by Lindsey Cooke on 2026-10-08, $555 / 30d, 35 leads, CPL $15.85. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: TOF Wedding Leads (alt aud) 10.9.26 (Lead Gen (MoF), paused), created by Lindsey Cooke on 2026-10-09, $31 / 30d, 0 leads, CPL —. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: MOF Wedding Leads 10.27.26 (Lead Gen (MoF), paused), created by Lindsey Cooke on 2026-10-27, $32 / 30d, 1 leads, CPL $31.58. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Monthly ROI: October: spend $1,295, 26 Meta-attributed bookings, blended ROAS 16.6x, retargeting ROAS 30.8x, CPL $3.57 on 220 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). HiddenGem's BoF under the gate at 5.3x on 4 purchases ($139; 23.7x over 30 days). The client paused its last two wedding-lead campaigns on 2 and 5 Nov, so the account is back to HiddenGem's three campaigns at $30/day.

### North Star Lodge & Resort — AM Charlotte — account North Star Lodge & Resort Ads (2003562593933799) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $599 over 30 days.

Blended 30d (every HiddenGem campaign): spend $902; pixel purchase value $610 + sign-up promo revenue $0 = $610, ROAS 0.7x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $12,362 from 25 bookings, −61% vs 1 Oct–9 Oct ($31,726 from 62 bookings) · promo codes: not tracked by cloudbeds.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers - 10/02/26 | Lead Gen (MoF) | 30d | $83 | 1 leads | CPL $83.46 (diagnostic) | — | Under gate | CPC $0.91 > $0.30; CPM $25.72 > $14.84 | spend $83.46 < $100 gate; 14d CPL $3.14 | Was Not scored (lead gen) |
| BoF - Sales Campaign - Retargeting Website Visitors - 09/09/2026 | Retargeting (BoF) | 14d | $70 | 1 purchases | ROAS 5.7x | 2.74 | Under gate | CPC $0.70 > $0.62 | spend $70.38 < $200 gate; 30d ROAS 4.0x, 2 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 10/26/26 | Lead Gen (MoF) | 30d | $68 | 29 leads | CPL $2.34 (diagnostic) | — | Under gate | CPC $0.44 > $0.30; CPM $16.86 > $14.84 | spend $67.98 < $100 gate; 14d CPL $2.34 | Unchanged |
| Discovery bucket (3 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $750 | — | promo ROAS — | — | Not scored (discovery) | — | $750 in 30 days across ToF - Giveaway Traffic Campaign - 09/09/2002, MoF - Lead Campaign - Retargeting Engagers - 10/02/26, MoF - Lead Campaign - Retargeting Engagers - 10/26/26; cloudbeds does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: September: spend $580, 0 Meta-attributed bookings, blended ROAS — · October: spend $919, 2 Meta-attributed bookings, blended ROAS 0.7x, retargeting ROAS 1.4x, CPL $22.29 on 6 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF under the gate at 5.7x on 1 purchase ($70). Of the two lead campaigns, 10/02 still has 1 lead on $83 in 30 days while 10/26 has 29 at $2.34, so the older one is worth pausing (Charlotte). Direct revenue month to date −61% on October. Pixel: the Cloudbeds browser Purchase is still mostly missing (pixel check).

### Bison Ridge Retreat — AM Chiara — account Bison Ridge Retreat Ad Account (950241787963535) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $599 over 30 days.

Blended 30d (every HiddenGem campaign): spend $898; pixel purchase value $0 + sign-up promo revenue $0 = $0, ROAS 0.0x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - RT Website Visitors | Retargeting (BoF) | 14d | $71 | 0 purchases | ROAS — | 2.02 | Under gate | CPC $0.65 > $0.62 | spend $70.64 < $200 gate | Unchanged |
| MoF - Lead Campaign - RT Engagers | Lead Gen (MoF) | 30d | $149 | 66 leads | CPL $2.26 (diagnostic) | — | Not scored (lead gen) | CPC $0.46 > $0.30; CPM $18.34 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $2.31 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $748 | — | promo ROAS — | — | Not scored (discovery) | — | $748 in 30 days across Discovery Campaign - Giveaway - April 16, 2026 - Copy, MoF - Lead Campaign - RT Engagers; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $924, 9 Meta-attributed bookings, blended ROAS 20.3x, retargeting ROAS —, CPL $1.75 on 23 leads · August: spend $952, 5 Meta-attributed bookings, blended ROAS 11.1x, retargeting ROAS —, CPL $2.47 on 63 leads · September: spend $893, 5 Meta-attributed bookings, blended ROAS 9.3x, retargeting ROAS —, CPL $2.54 on 59 leads · October: spend $922, 1 Meta-attributed bookings, blended ROAS 2.3x, retargeting ROAS —, CPL $2.21 on 68 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF under the gate, 0 purchases on $71; the pixel has no Purchase in 28 days, so BoF has no conversion signal to optimise on (pixel check ⚠️).

### Glasscombe — AM Charlotte — account Glasscombe (2030318804465316) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $527 over 30 days.

Blended 30d (every HiddenGem campaign): spend $783; pixel purchase value $0 + sign-up promo revenue $0 = $0, ROAS 0.0x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $5,551 from 10 bookings, +298% vs 1 Oct–9 Oct ($1,393 from 3 bookings) · promo codes: not tracked by cloudbeds.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 10/09/26. | Retargeting (BoF) | 14d | $69 | 0 purchases | ROAS — | 1.87 | Under gate | CPM $17.95 > $16.50 | spend $68.79 < $200 gate | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers -  10/09/26 | Lead Gen (MoF) | 30d | $128 | 409 leads | CPL $0.31 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.32 | Was Under gate, not scored since 4 Nov |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $655 | — | promo ROAS — | — | Not scored (discovery) | — | $655 in 30 days across ToF - Giveaway Traffic Campaign - UK, MoF - Lead Campaign - Retargeting Engagers -  10/09/26; cloudbeds does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: October: spend $541, 2 Meta-attributed bookings, blended ROAS 2.2x, retargeting ROAS —, CPL $0.29 on 306 leads. Note in the October file: LaunchBoom pre-bookings led to high occupancy at low revenue this month (AM note from the tracking sheet).

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). Both under the gate: leads $0.31 on 409 ($128), BoF 0 purchases on $69. The pixel took 20 Purchase this week (30 in 28 days), so BoF's zero is attribution, not tracking. Direct revenue month to date $5.6k against $1.4k on the same days of October.

### Cabin Collective — AM Chiara — account Cabin Collective (2194562394139883) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $186 over 30 days.

Blended 30d (every HiddenGem campaign): spend $559; pixel purchase value $10,770 + sign-up promo revenue $0 = $10,770, ROAS 19.3x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–9 Nov): direct revenue $14,895 from 9 bookings, −32% vs 1 Oct–9 Oct ($21,841 from 12 bookings) · promo codes: not tracked by ownerrez.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 10/20/26 | Retargeting (BoF) | 14d | $138 | 5 purchases | ROAS 36.7x | 2.25 | Under gate | within lines | spend $138.38 < $200 gate; 30d ROAS 57.9x, 7 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 10/20/26 | Lead Gen (MoF) | 30d | $187 | 157 leads | CPL $1.19 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.16 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $373 | — | promo ROAS — | — | Not scored (discovery) | — | $373 in 30 days across ToF - Giveaway Traffic Campaign - [TX, OK, AR] - 10/20/26, MoF - Lead Campaign - Retargeting Engagers - 10/20/26; ownerrez does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: October: spend $312, 6 Meta-attributed bookings, blended ROAS 28.8x, retargeting ROAS 86.4x, CPL $1.31 on 79 leads. Note in the October file: No booking-level export from the client this month; the direct booking revenue is the client reporting sheet figure and the booking count is unavailable. Attributed revenue comes from Meta-reported retargeting purchases only.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF under the gate at 36.7x on 5 purchases ($138). Leads $1.19 on 157. Master sheet still reads Not Live.

### American River Resort — AM Nicole — account American River Resort (953162737054331) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $196 over 30 days.

Blended 30d (every HiddenGem campaign): spend $327; pixel purchase value $0 + sign-up promo revenue $0 = $0, ROAS 0.0x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $327 | — | promo ROAS — | — | Not scored (discovery) | — | $327 in 30 days across ToF - Giveaway Traffic Campaign - SAC/SJ/SF (paused), MoF - Lead Campaign - Retargeting Engagers (paused); no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Paused in window, not scored: MoF - Lead Campaign - Retargeting Engagers (Lead Gen (MoF)), $132 / 30d, 95 leads, CPL $1.39. Live campaigns only are scored (decision 2026-09-23).

Monthly ROI: July: spend $1,544, 4 Meta-attributed bookings, blended ROAS 1.1x · August: spend $1,529, 3 Meta-attributed bookings, blended ROAS 1.4x, CPL $18.30 on 30 leads · September: spend $1,453, 0 Meta-attributed bookings, blended ROAS —, CPL $1.48 on 377 leads · October: spend $777, 2 Meta-attributed bookings, blended ROAS 15.1x, CPL $1.27 on 244 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). Ads off since 15 Oct: paused, not offboarded. Nothing scored.

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
- Client-run campaigns (created by a non-HiddenGem login per the account activity log, listed under the client, never scored): Selah Place: SP / Willow / Pre-Sales / VIP List / 10-2026 (Nathan Jay Herrington), Instagram post: 🔥 𝐒𝐀𝐂𝐑𝐈𝐅𝐈𝐂𝐄 𝐈𝐒 𝐑𝐄𝐐𝐔𝐈𝐑𝐄𝐃 🔥... (Live Intentionally Today LIT), SP / Willow / Lead Gen / VIP List / 10-2026 (Nathan Jay Herrington), SP / Willow / Sales / Top-5 Audiences / 11-2026 (Nathan Jay Herrington), SP / Black Walnut / Leads / Early Access / 11-2026 (Nathan Jay Herrington); Walden Retreats: TOF Wedding Leads 10.8.26 (Lindsey Cooke), TOF Wedding Leads (alt aud) 10.9.26 (Lindsey Cooke), MOF Wedding Leads 10.27.26 (Lindsey Cooke). Creators are known for campaigns created in the last 180 days; older campaigns are scored as usual.
- Unclassified campaigns: none.
- Previous report: 2026-11-02-client-benchmark.csv. Diff joined on campaign_id for live rows and client + campaign name for CSV rows. Diff counts: 2 new, 2 still open, 2 fixed, 70 unchanged, 0 removed.
- Scope changes vs 2 Nov: none (same 24 accounts); Sunapee Stays kept in scope (CRM Meta Ads column reads Basic since 19 Oct; kept as Advanced at Shawal's request (2026-10-26)). Advanced in the CRM but with no ad account mapping in PROJECT.md section 5, not scored: Treetop Hideaways (AM Kristal), Casey Key Resort (AM —), Arca Roatan (AM Anna), Gooseberry Lodges (AM Alicia), Dunya Camp (AM Chiara), Nine Pines Retreat (AM Nicole), Lundy Farm (AM Charlotte), The Preserve (AM Alicia), Kimpton Mas Olas Resort (AM Charlotte). Gooseberry Lodges (no ads running yet, Shawal 9 Nov) and Nine Pines Retreats are on the Master Meta Ads sheet without an account ID.
- HG AI reports read from `HG AI Reports/` at the project root, dated since the previous run: none.
- Selah Place's campaigns are named with pipes in Meta ("SP | Willow | Sales | Top-5 Audiences | 11-2026"); shown here with slashes.
- Meeting notes: every "Meta Ads Strategy", "Meta Ads Sync" or "Meta Ads x HiddenGem AI Sync" calendar event since the previous run that has a "Notes by Gemini" attachment, read via Drive. Client names are matched with an alias list (Flow Home = FLOHOM, Tabber / Tipik Falls / Debug Falls = Tàberg Falls, Sailor Place = Selah Place, Stay on 38 = Stay On 30A, Ashwood River Cabins = Asheville River Cabins).
- This month line: direct booking revenue by booking date from the HiddenGem AI platform (pms_bookings, platform direct/OTA rules, tenants on a shared PMS account narrowed to their own properties), month to date at the run date, against the same day span of the previous month. Promo codes come from the booking payload: Guesty stores the code, Hostaway only a coupon id (counted, no names), Hospitable and Cloudbeds nothing. Pulled with pms_mtd.sql through the Supabase connector. Clients without a PMS connection on the platform show no figures.
- Monthly ROI context from `Monthly ROI data/` (July 2026, August 2026, September 2026, October 2026). Revenue there comes from the Client Performance Tracking sheet, not the pixel, so its ROAS is not comparable to the pixel ROAS above.
