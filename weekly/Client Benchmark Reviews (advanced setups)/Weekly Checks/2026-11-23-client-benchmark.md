# Client Benchmark Review (advanced setups) — 2026-11-23

Run: 23 November 2026 (Monday), tenth run, compared against 2026-11-16-client-benchmark.csv. Live reads through the Meta Marketing API with the HG - ROI Dashboard system user, the standing data path (`scripts/pull-campaign-insights.mts`, about 07:10 PT); every account read live and the CSV export 2026-10-19 to 2026-10-25 was not needed for scoring. Scope: clients marked **Advanced** in the CRM "Meta Ads" column (Clients - Onboarding tab), re-read today: 34 clients, 27 with an ad account. New Advanced rows in the CRM this week, with no ad account shared yet: Christiania at Vail (Chiara) and Black Prong (Nicole); Tàberg Falls is listed under Anna in the CRM now. 7 Advanced clients have no ad account mapped (Nine Pines Retreat has one since 18 Nov, $0 spent, not mapped yet). Scoring as since 4 Nov: Sales-objective campaigns only (Retargeting, Prospecting, Sales, on 14-day pixel ROAS); Lead Gen rows and the Discovery bucket row stay in each client's table for context with no state. Changes since last Monday come from each account's Meta activity log (Shawal's 16 Nov changes under his second profile John Martin; paused lookalike builds made through the system user on 19 and 20 Nov). The 18 Nov Meta Ads Strategy meeting agreed that accounts above 10x ROAS may get a 20 to 50% budget increase with the client told; every Scale candidate this week already runs at or above its CRM Ad Spend Range, so none is raised without a wider range. ROAS is read against this week's pixel check where duplicate Purchases inflate it or missing Purchases deflate it.

| Advanced clients | Live reads | From CSV | Rows scored | Under spend gate | Flag to Shawal | Review w/ HG AI | Monitor | Healthy | Scale w/ HG AI | Frequency over 5 | Not scored (lead gen) | Not scored (discovery) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 27 (+7 unmapped) | 27 | 0 | 25 | 17 | 3 | 5 | 6 | 4 | 7 | 0 | 24 | 26 |

States come from the Decision Making table in the Benchmarks doc and apply to Sales-objective campaigns only (Shawal, 4 Nov 2026): Retargeting, Prospecting and Sales campaigns on 14-day pixel ROAS with a $200 gate. Bands: above 15x Scale, 8–15x Healthy, 5–8x Monitor, 2–5x Review, under 2x or zero purchases Flag, inclusive on the lower bound. Lead Gen rows (leads, CPL) and the Discovery bucket row (giveaway + lead spend against 30-day sign-up promo-code revenue from the PMS) are listed under each client for context and carry no state.

## Weekly Meta Ads meetings since last run (Notes by Gemini)

Source: "Notes by Gemini" docs attached to the calendar events, read via Drive. Summary, decisions and next steps as Gemini wrote them; client-specific sentences are pulled into each client's section below. Transcript not used.

### Meta Ads Strategy — 2026-11-18 — doc `1Y5pKeELQBhnfDGZOfa8OyLZm57u28S_t1pKadrIv1B4`

API costs and Meta ads automation and tracking challenges reviewed via workflow analysis

API Costs and Model Settings

API credit charges for Claude workflows prompted recommendations to specify models like Haiku or Sonnet to reduce costs.

Meta Ads and Tracking

Budget automation and accurate attribution were prioritized alongside risk management for ad account restrictions.

Website Development and Scalability

Custom website development was concluded to be unscalable due to client friction and undefined revisions.

Decisions:
- Ad budget increase threshold and policy Client accounts with returns exceeding 10x may have their ad budgets increased by up to 50% provided the account owner is notified.

Next steps:
- Alert the team about Facebook detecting browser extension cursor movements to prevent ad account restrictions as soon as possible.
- Research the Meta and Pipboard MCP integration to confirm safety and feasibility for automated ad management through cloud desktop connectors.
- Send an update into the customer channel regarding the tracking and cookie policy issue to prompt action from the web master's team.
- Respond to Paul with the necessary cookie policy additions for developer Edward to implement on the main site.
- Review the site mechanics to determine how to incorporate phone number data into reservations and the data warehouse.
- Adjust the performance flagging tool to evaluate accounts based on overall return on ad spend rather than strictly retargeting campaign metrics.
- Look into the next big resort client that utilizes iguh.com for potential business development.

## Action needed

Sales-objective campaigns only (Retargeting, Prospecting, Sales; Shawal, 4 Nov 2026). Flag to Shawal before Review w/ HG AI, highest spend first.

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| The Preserve | Alicia | BoF - Website Retargeting Campaign - 11/12/2026 | Retargeting (BoF) | $731 / 14d | ROAS — | Flag to Shawal | New, not in the 16 Nov run |
| Gooseberry Lodges | Alicia | BoF - Sales Campaign - Retargeting Website Visitors - 10.27/2026 | Retargeting (BoF) | $284 / 14d | ROAS — | Flag to Shawal | New flag, was Under gate |
| Little River Landing | Makenna | BoF - Sales Campaign - Retargeting Website Visitors - 09/16/2026 | Retargeting (BoF) | $258 / 14d | ROAS 1.2x | Flag to Shawal | Still open, week 3 |
| Tàberg Falls | Anna | BoF - Website Retargeting Campaign - 08/21/2026 | Retargeting (BoF) | $1,408 / 14d | ROAS 5.0x | Review w/ HG AI | New flag, was Monitor |
| Endless Stays | Nicole | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $832 / 14d | ROAS 4.8x | Review w/ HG AI | Still open, week 8 |
| Endless Stays | Nicole | MoF - Lookalike Sales Campaign - 11/13/2026 | Prospecting (MoF lookalike) | $501 / 14d | ROAS 5.0x | Review w/ HG AI | New flag, was Under gate |
| Stay Saluda NC | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $421 / 14d | ROAS 3.6x | Review w/ HG AI | New flag, was Healthy |
| FLOHOM | Makenna | [Myrtle Beach] MoF - Lookalike Sales Campaign - 09/17/26 | Prospecting (MoF lookalike) | $222 / 14d | ROAS 4.2x | Review w/ HG AI | Still open, week 2 |

## Scale candidates

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| Stay On 30A | Charlotte | MoF - Sales Campaign - HiddenGem Pixel LoL - 07/17/26 | Prospecting (MoF lookalike) | $2,509 / 14d | ROAS 18.6x | Scale w/ HG AI | Was Healthy |
| Paradise Pointe | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $681 / 14d | ROAS 19.1x | Scale w/ HG AI | Was Healthy |
| Selah Place | Alicia | BoF-Website Retarget Campaign - 07/24/2026 | Retargeting (BoF) | $420 / 14d | ROAS 17.6x | Scale w/ HG AI | Unchanged |
| AwayFrames | Alicia | BoF - Sales Campaign - Retargeting Website Visitors 07/31/2026 | Retargeting (BoF) | $343 / 14d | ROAS 24.7x | Scale w/ HG AI | Was Healthy |
| AwayFrames | Alicia | MoF - Lookalike Sales Campaign - 10/29/2026 | Prospecting (MoF lookalike) | $340 / 14d | ROAS 15.7x | Scale w/ HG AI | Was Healthy |
| Starlight Haven Hot Springs | Charlotte | Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | $280 / 14d | ROAS 27.9x | Scale w/ HG AI | Unchanged |
| Ridge & Falls | Makenna | BoF - Sales Campaign - Retargeting Website Visitors - 09/01/26 | Retargeting (BoF) | $207 / 14d | ROAS 25.8x | Scale w/ HG AI | Unchanged |

## Frequency watch (Sales / Retargeting above 5)

Sales, Retargeting and MoF-lookalike campaigns whose 14-day frequency is above 5.0 (Shawal, 6 Oct 2026). Frequency does not change the ROAS state; this is the list to refresh creative or widen the audience on. The diagnostics column still notes anything above 3.0.

| Client | AM | Campaign | Type | Frequency | Spend / window | Governing metric | State |
|---|---|---|---|---|---|---|---|
| — | | | | | | | |

## Per client, ordered by scored MoF + BoF spend

### Stay On 30A — AM Charlotte — account Stay on 30a Ads (25640434272252212) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $3,002 over 30 days.

Blended 30d (every HiddenGem campaign): spend $15,097; pixel purchase value $159,270 + sign-up promo revenue $74,445 = $233,715, ROAS 15.5x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $293,168 from 106 bookings, +33% vs 1 Oct–23 Oct ($220,969 from 79 bookings) · promo codes: 55 uses (EARLY BIRD DIRECT ×30, VIP100 ×14, WELCOME100 ×14, SNOWBIRD30A ×4, WELCOMEBACK15 ×2, CINDYSWANSON10 ×1, ESCAPE30A ×1, HGTEST ×1, RETURNINGGUEST ×1, STAY200 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - RT Website Visitors - 07/13/26 | Retargeting (BoF) | 14d | $2,456 | 10 purchases | ROAS 14.6x | 4.31 | Healthy | CPC $1.42 > $0.62; CPM $33.98 > $16.50; cost/booking $245.58 > $90; freq 4.3 > 3.0 | 30d ROAS 15.2x, 20 purchases | Was Scale w/ HG AI |
| MoF - Sales Campaign - HiddenGem Pixel LoL - 07/17/26 | Prospecting (MoF lookalike) | 14d | $2,509 | 10 purchases | ROAS 18.6x | 1.67 | Scale w/ HG AI | CPC $0.89 > $0.62; CPM $23.94 > $16.50; cost/booking $250.92 > $90 | 30d ROAS 14.9x, 16 purchases | Was Healthy |
| MoF - Lead Campaign - RT Engagers - 07/16/26 | Lead Gen (MoF) | 30d | $1,501 | 905 leads | CPL $1.66 (diagnostic) | — | Not scored (lead gen) | CPC $0.44 > $0.30; CPM $42.19 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.81 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $4,503 | 18 promo bookings, $74,445 | promo ROAS 16.5x | — | Not scored (discovery) | WELCOME100 ×18 $74,445; not counted (not sign-up codes): EARLY BIRD DIRECT ×42 $229,582, VIP100 ×16 $57,674, SNOWBIRD30A ×5 $30,693, RETURNINGGUEST ×1 $4,941, STAY200 ×1 $3,171, WELCOMEBACK15 ×2 $2,524, CINDYSWANSON10 ×1 $1,514, ESCAPE30A ×1 $1,196, HGTEST ×1 $13 | $4,503 in 30 days across ToF - Giveaway Traffic Campaign - 02/05/2026, MoF - Lead Campaign - RT Engagers - 07/16/26, against direct bookings booked 24 Oct–23 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $6,407, 67 Meta-attributed bookings, blended ROAS 32.3x, retargeting ROAS 14.6x, CPL $1.24 on 583 leads · August: spend $12,420, 85 Meta-attributed bookings, blended ROAS 17.8x, retargeting ROAS 15.5x, CPL $2.58 on 594 leads · September: spend $12,606, 91 Meta-attributed bookings, blended ROAS 24.4x, retargeting ROAS 23.1x, CPL $1.52 on 1001 leads · October: spend $15,161, 51 Meta-attributed bookings, blended ROAS 15.5x, retargeting ROAS 17.2x, CPL $1.47 on 1036 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). The LoL lookalike moves up from Healthy (11.6x) to Scale at 18.6x on 10 purchases ($2,509 in 14 days); BoF eases from Scale (15.3x) to Healthy at 14.6x on 10 purchases ($2,456), frequency 4.3. On 16 Nov Shawal moved $50/day from the lookalike to BoF ($150 / $200), so the account stays at $500/day, which is the CRM's $15,000/month range: the 18 Nov rule (raise 20 to 50% above 10x and tell the client) needs a wider range first. Direct revenue month to date $293.2k, +33% on October; EARLY BIRD DIRECT ×30, VIP100 ×14 and WELCOME100 ×14 carry the coded bookings. Discovery read (context only) 16.5x on WELCOME100 ×18.

### Tàberg Falls — AM Anna — account Táberg Falls (827872700004659) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,744 over 30 days.

Blended 30d (every HiddenGem campaign): spend $8,437; pixel purchase value $32,288 + sign-up promo revenue $4,971 = $37,259, ROAS 4.4x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $44,903 from 25 bookings, +0% vs 1 Oct–23 Oct ($44,840 from 30 bookings) · promo codes: 2 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Website Retargeting Campaign - 08/21/2026 | Retargeting (BoF) | 14d | $1,408 | 4 purchases | ROAS 5.0x | 2.94 | Review w/ HG AI | CPC $0.84 > $0.62; CPM $23.33 > $16.50; cost/booking $352.01 > $90 | 30d ROAS 6.3x, 10 purchases | New flag, was Monitor |
| MoF - Lookalike Sales Campaign - 08/21/2026 | Prospecting (MoF lookalike) | 14d | $1,418 | 5 purchases | ROAS 5.7x | 1.45 | Monitor | CPM $17.94 > $16.50; cost/booking $283.50 > $90 | 30d ROAS 5.6x, 9 purchases | Was Healthy |
| MoF - Leads Campaign - 06/19/26 | Lead Gen (MoF) | 30d | $1,257 | 2117 leads | CPL $0.59 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.65 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $3,002 | 2 promo bookings, $4,971 | promo ROAS 1.7x | — | Not scored (discovery) | 2 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $3,002 in 30 days across MoF - Leads Campaign - 06/19/26, ToF - Giveaway Campaign - 07/08/2026, against direct bookings booked 24 Oct–23 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Client-run, not scored: TF / Speed Plan / Clean build (Sales, active), created by Denver Brenizer on 2026-11-21, $248 / 14d, 0 purchases, ROAS —. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Monthly ROI: July: spend $11,739, 80 Meta-attributed bookings, blended ROAS 9.5x, retargeting ROAS 15.8x, CPL $0.67 on 2320 leads · August: spend $11,259, 48 Meta-attributed bookings, blended ROAS 6.3x, retargeting ROAS 8.0x, CPL $0.46 on 4015 leads · September: spend $10,800, 42 Meta-attributed bookings, blended ROAS 5.6x, retargeting ROAS 7.1x, CPL $0.55 on 3261 leads · October: spend $8,391, 34 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 8.3x, CPL $0.58 on 2779 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF slips from Monitor (5.3x) to Review at 5.0x (4.98x) on 4 purchases ($1,408), a new Action row; the lookalike drops from Healthy (10.0x) to Monitor at 5.7x on 5 purchases ($1,418). Both sit under the client's 7x goal in the CRM. On 21 Nov the client side (Denver Brenizer) added 'TF / Speed Plan / Clean build' at $100/day, so the account is $400/day and that campaign is listed, not scored. Discovery read 1.7x: two Hostaway coupon bookings ($4,971) on $3,002 of giveaway and lead spend in 30 days, so whether the sign-up code works on the booking engine is still open (Alicia). Direct revenue month to date flat on October ($44.9k). AM now Anna in the CRM.

### Endless Stays — AM Nicole — account Endless Stays (896372356081479) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $2,094 over 30 days.

Blended 30d (every HiddenGem campaign): spend $6,029; pixel purchase value $11,121 + sign-up promo revenue $0 = $11,121, ROAS 1.8x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $47,920 from 28 bookings, +35% vs 1 Oct–23 Oct ($35,534 from 18 bookings) · promo codes: not tracked by hospitable.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $832 | 2 purchases | ROAS 4.8x | 2.40 | Review w/ HG AI | CPC $0.86 > $0.62; CPM $21.72 > $16.50; cost/booking $416.10 > $90 | 30d ROAS 4.3x, 3 purchases | Still open, week 8 |
| MoF - Lookalike Sales Campaign - 11/13/2026 | Prospecting (MoF lookalike) | 14d | $501 | 1 purchases | ROAS 5.0x | 1.29 | Review w/ HG AI | CPM $18.28 > $16.50; cost/booking $500.60 > $90 | 30d ROAS 5.0x, 1 purchases | New flag, was Under gate |
| MoF Lead Campaign - Retargeting Engagers - 09/09/2026 | Lead Gen (MoF) | 30d | $1,408 | 1236 leads | CPL $1.14 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.29 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $3,501 | — | promo ROAS — | — | Not scored (discovery) | — | $3,501 in 30 days across ToF - Giveaway Traffic Campaign - AZ, FL, VA, PA, TN, MoF Lead Campaign - Retargeting Engagers - 09/09/2026; hospitable does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $1,534, 9 Meta-attributed bookings, blended ROAS 16.0x · August: spend $1,553, 10 Meta-attributed bookings, blended ROAS 11.6x, retargeting ROAS 38.8x, CPL $9.73 on 26 leads · September: spend $2,539, 6 Meta-attributed bookings, blended ROAS 2.9x, retargeting ROAS 4.7x, CPL $1.05 on 532 leads · October: spend $6,184, 5 Meta-attributed bookings, blended ROAS 2.6x, retargeting ROAS 3.3x, CPL $0.89 on 1715 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF stays Review, week 8: 4.8x on 2 purchases ($832 in 14 days), 30-day 4.3x. The 13 Nov lookalike reaches the gate at 5.0x (4.99x) on 1 purchase ($501), a new Review row. Month-to-date direct revenue is $47.9k, +35% on October (28 bookings), while the pixel's Purchases arrive server-side only from the HG AI CAPI (15 against 18 online bookings), so attributed ROAS undercounts what the PMS shows. Next step for Nicole: keep both at budget one more week; if BoF is still under 5x on 30 Nov, move its $50 into the lookalike or the lead campaign.

### The Preserve — AM Alicia — account Preserve Sporting Club & Residences (528888625350386) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $2,459 over 30 days.

Blended 30d (every HiddenGem campaign): spend $4,341; pixel purchase value $0 + sign-up promo revenue $0 = $0, ROAS 0.0x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Website Retargeting Campaign - 11/12/2026 | Retargeting (BoF) | 14d | $731 | 0 purchases | ROAS — | 1.85 | Flag to Shawal | CPC $0.94 > $0.62; CPM $19.23 > $16.50 | no purchases | New, not in the 16 Nov run |
| MoF - Lead Campaign - Retargeting Engagers -  11/11/26 | Lead Gen (MoF) | 30d | $1,150 | 638 leads | CPL $1.80 (diagnostic) | — | Not scored (lead gen) | CPC $0.33 > $0.30; CPM $16.56 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.80 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $3,609 | — | promo ROAS — | — | Not scored (discovery) | — | $3,609 in 30 days across ToF - Giveaway Campaign - 11/10/2026, MoF - Lead Campaign - Retargeting Engagers -  11/11/26; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Client-run, not scored: Cl:Preserve_Ch:Meta_Obj:Conv_Tac:Prospecting_Typ:ABO_Of:EVG_CT:Standard_Notes: (Sales, paused), created by Maddy Watson on 2026-10-21, $175 / 14d, 0 purchases, ROAS —. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: Cl:Preserve_Ch:Meta_Obj:Conv_Tac:Retargeting_Typ:ABO_Of:EVG_CT:Standard_Notes: (Retargeting (BoF), paused), created by Maddy Watson on 2026-10-21, $96 / 14d, 0 purchases, ROAS —. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF crosses the gate with 0 purchases on $731 in 14 days: Flag, new. Tracking comes first: the browser never fires Purchase (18 in 28 days, all server, sender unknown), and since 16 Nov the site fires Lead and CompleteRegistration on most page views (34,128 Lead in the week; pixel check), which also pollutes the retargeting audiences. The lead campaign reads 638 leads at $1.80 on $1,151. The two MoF campaigns Shawal built on 20 Nov (Top 10% Income Earners and Lookalike Sales, $100/day each) have their ad sets paused and have not spent. No PMS connection yet. Next step (Alicia): fix the Lead tag and add a browser Purchase on the booking confirmation before judging BoF.

### Paradise Pointe — AM Makenna — account Paradise Pointe Ads (1585826092078255) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $905 over 30 days.

Blended 30d (every HiddenGem campaign): spend $5,200; pixel purchase value $56,013 + sign-up promo revenue $76,229 = $132,242, ROAS 25.4x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $122,427 from 116 bookings, +16% vs 1 Oct–23 Oct ($105,966 from 109 bookings) · promo codes: 57 uses (WELCOME100 ×48, VIP100 ×6, WELCOME10 ×2, WELCOMEBACK10 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - LoL Sales Campaign - 09/28/26 | Prospecting (MoF lookalike) | 14d | $1,211 | 13 purchases | ROAS 9.3x | 2.24 | Healthy | CPC $0.72 > $0.62; cost/booking $93.14 > $90 | 30d ROAS 14.4x, 27 purchases | Was Scale w/ HG AI |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $681 | 13 purchases | ROAS 19.1x | 4.90 | Scale w/ HG AI | CPC $1.03 > $0.62; freq 4.9 > 3.0 | 30d ROAS 18.2x, 24 purchases | Was Healthy |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $803 | 704 leads | CPL $1.14 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.18 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,708 | 65 promo bookings, $76,229 | promo ROAS 44.6x | — | Not scored (discovery) | WELCOME100 ×62 $71,787, WELCOME10 ×3 $4,442; not counted (not sign-up codes): VIP100 ×6 $7,155, WELCOMEBACK10 ×1 $1,111 | $1,708 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Giveaway Traffic Campaign, against direct bookings booked 24 Oct–23 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $2,237, 74 Meta-attributed bookings, blended ROAS 21.6x, retargeting ROAS 16.7x, CPL $1.01 on 90 leads · August: spend $3,109, 113 Meta-attributed bookings, blended ROAS 23.1x, retargeting ROAS 18.0x, CPL $1.64 on 471 leads · September: spend $3,074, 98 Meta-attributed bookings, blended ROAS 28.8x, retargeting ROAS 13.0x, CPL $0.97 on 764 leads · October: spend $4,651, 124 Meta-attributed bookings, blended ROAS 21.5x, retargeting ROAS 9.8x, CPL $1.03 on 746 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF moves up from Healthy (13.2x) to Scale at 19.1x on 13 purchases ($681), frequency 4.9, just under the 5.0 watch line. The LoL lookalike falls from Scale (20.8x) to Healthy at 9.3x on 13 purchases ($1,211), its first full fortnight at $100/day after the 12 and 13 Nov doubling. The account runs $220/day against a CRM range of $4,500/month, so no raise. Discovery read (context only) 44.6x: WELCOME100 ×62 ($71.8k) in 30 days on $1,708. Direct revenue month to date $122.4k, +16% on October.

### AwayFrames — AM Alicia — account Awayframes Ad Account (2471256056603833) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,169 over 30 days.

Blended 30d (every HiddenGem campaign): spend $4,251; pixel purchase value $23,440 + sign-up promo revenue $0 = $23,440, ROAS 5.5x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $35,043 from 24 bookings, +222% vs 1 Oct–23 Oct ($10,890 from 13 bookings) · promo codes: 0 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors 07/31/2026 | Retargeting (BoF) | 14d | $343 | 6 purchases | ROAS 24.7x | 3.70 | Scale w/ HG AI | CPC $1.43 > $0.62; CPM $21.96 > $16.50; freq 3.7 > 3.0 | 30d ROAS 16.3x, 15 purchases | Was Healthy |
| MoF - Lookalike Sales Campaign - 10/29/2026 | Prospecting (MoF lookalike) | 14d | $340 | 4 purchases | ROAS 15.7x | 1.28 | Scale w/ HG AI | within lines | 30d ROAS 7.2x, 5 purchases | Was Healthy |
| MoF - Lead Campaign - Retargeting Engagers 07/31/2026 | Lead Gen (MoF) | 30d | $1,143 | 780 leads | CPL $1.47 (diagnostic) | — | Not scored (lead gen) | CPC $0.32 > $0.30 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.46 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $2,312 | 0 promo bookings, $0 | promo ROAS 0.0x | — | Not scored (discovery) | 0 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $2,312 in 30 days across ToF - Giveaway Traffic Campaign - 07/31/2026, MoF - Lead Campaign - Retargeting Engagers 07/31/2026, against direct bookings booked 24 Oct–23 Nov with a sign-up code; no sign-up promo bookings in 30 days; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $923, 9 Meta-attributed bookings, blended ROAS 18.6x, CPL $2.44 on 2 leads · August: spend $869, 8 Meta-attributed bookings, blended ROAS 21.8x, retargeting ROAS 27.0x, CPL $2.68 on 58 leads · September: spend $895, 7 Meta-attributed bookings, blended ROAS 11.1x, retargeting ROAS 4.9x, CPL $1.83 on 82 leads · October: spend $1,898, 20 Meta-attributed bookings, blended ROAS 9.9x, retargeting ROAS 15.3x, CPL $1.56 on 316 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). Both Sales campaigns move up to Scale: BoF 24.7x on 6 purchases ($343) and the 10/29 lookalike 15.7x on 4 purchases ($340). Read them with care: the ad account has been UNSETTLED (payment needed) since 16 Nov, so the 14-day window holds only one week of delivery and no ads have run since. Nothing to scale until the balance is paid (Alicia); the account is at the CRM's $6,000/month range anyway. Direct revenue month to date $35.0k, +222% on October. Discovery read 0.0x: no Hostaway coupon booking in 30 days on $2,312.

### Ponderosa Pines Resort — AM Anna — account Ponderosa Pines Resort (1058846326445255) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,105 over 30 days.

Blended 30d (every HiddenGem campaign): spend $3,207; pixel purchase value $10,408 + sign-up promo revenue $0 = $10,408, ROAS 3.2x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $32,149 from 100 bookings, +9% vs 1 Oct–23 Oct ($29,573 from 104 bookings) · promo codes: not tracked by newbook.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Website Retarget Campaign - 07/13/26 | Retargeting (BoF) | 14d | $571 | 9 purchases | ROAS 5.6x | 2.25 | Monitor | CPC $0.68 > $0.62; CPM $16.89 > $16.50 | 30d ROAS 6.4x, 23 purchases | Unchanged |
| MoF - Lookalike Sales Campaign - 11/13/26 | Prospecting (MoF lookalike) | 14d | $391 | 4 purchases | ROAS 7.0x | 1.86 | Monitor | CPC $0.95 > $0.62; CPM $20.74 > $16.50; cost/booking $97.74 > $90 | 30d ROAS 7.0x, 4 purchases | Was Under gate |
| Leads Campaign - 07/16/26 | Lead Gen (MoF) | 30d | $505 | 388 leads | CPL $1.30 (diagnostic) | — | Not scored (lead gen) | CPC $0.34 > $0.30; CPM $17.45 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.52 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,610 | — | promo ROAS — | — | Not scored (discovery) | — | $1,610 in 30 days across Discovery Campaign - Giveaway - June 2026, Leads Campaign - 07/16/26; newbook does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $2,089, 17 Meta-attributed bookings, blended ROAS 3.6x, retargeting ROAS 22.3x, CPL $0.91 on 356 leads · August: spend $3,101, 103 Meta-attributed bookings, blended ROAS 15.0x, retargeting ROAS 21.3x, CPL $1.32 on 471 leads · September: spend $2,985, 119 Meta-attributed bookings, blended ROAS 17.9x, retargeting ROAS 21.6x, CPL $0.84 on 708 leads · October: spend $3,065, 39 Meta-attributed bookings, blended ROAS 6.0x, retargeting ROAS 12.5x, CPL $1.02 on 601 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF holds Monitor, down from 7.5x to 5.6x on 9 purchases ($571); the 13 Nov lookalike reaches the gate at Monitor, 7.0x on 4 purchases ($391). Both are upper bounds: the pixel check still shows the Newbook confirmation firing about 1.8 browser Purchases per booking (week 4). Direct revenue month to date +9% on October. No promo data (Newbook stores no code).

### Treetop Escapes — AM Makenna — account Treetop Escapes Ads (967636478877602) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $901 over 30 days.

Blended 30d (every HiddenGem campaign): spend $3,007; pixel purchase value $16,276 + sign-up promo revenue $13,487 = $29,763, ROAS 9.9x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $35,890 from 41 bookings, −2% vs 1 Oct–23 Oct ($36,690 from 43 bookings) · promo codes: 13 uses (WELCOME100 ×11, VIP100 ×1, WELCOME10 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $559 | 5 purchases | ROAS 7.4x | 3.63 | Monitor | CPC $0.62 > $0.62; CPM $20.10 > $16.50; cost/booking $111.84 > $90; freq 3.6 > 3.0 | 30d ROAS 11.8x, 17 purchases | Was Healthy |
| MoF - Lookalike Sales Campaign - 11/13/2026 | Prospecting (MoF lookalike) | 14d | $198 | 2 purchases | ROAS 10.3x | 1.42 | Under gate | cost/booking $98.94 > $90 | spend $197.87 < $200 gate; 30d ROAS 10.3x, 2 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $705 | 866 leads | CPL $0.81 (diagnostic) | — | Not scored (lead gen) | CPM $15.36 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.00 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,606 | 12 promo bookings, $13,487 | promo ROAS 8.4x | — | Not scored (discovery) | WELCOME100 ×11 $10,165, WELCOME10 ×1 $3,322; not counted (not sign-up codes): VIP100 ×1 $612 | $1,606 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Giveaway Traffic Campaign, against direct bookings booked 24 Oct–23 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $2,487, 44 Meta-attributed bookings, blended ROAS 14.5x, retargeting ROAS 22.2x, CPL $1.48 on 21 leads · August: spend $3,082, 33 Meta-attributed bookings, blended ROAS 12.3x, retargeting ROAS 16.3x, CPL $1.49 on 620 leads · September: spend $2,998, 23 Meta-attributed bookings, blended ROAS 7.9x, retargeting ROAS 7.9x, CPL $0.88 on 1019 leads · October: spend $3,081, 32 Meta-attributed bookings, blended ROAS 10.9x, retargeting ROAS 11.8x, CPL $0.79 on 1164 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF slips from Healthy (13.5x) to Monitor at 7.4x on 5 purchases ($559), frequency 3.6; 30-day 11.8x. The 13 Nov lookalike is still under the gate at 10.3x on 2 purchases ($198). Direct revenue month to date flat on October ($35.9k). Discovery read (context only) 8.4x: WELCOME100 ×11 on $1,606.

### Starlight Haven Hot Springs — AM Charlotte — account Starlight Haven Hot Springs (901138032027913) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $753 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,253; pixel purchase value $13,986 + sign-up promo revenue $0 = $13,986, ROAS 6.2x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $280 | 12 purchases | ROAS 27.9x | 2.12 | Scale w/ HG AI | within lines | 30d ROAS 23.4x, 21 purchases | Unchanged |
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $902 | 2774 leads | CPL $0.33 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.34 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,655 | — | promo ROAS — | — | Not scored (discovery) | — | $1,655 in 30 days across Discovery Campaign - Giveaway - 12/16/2025, New Leads Campaign - 03/03/26; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $2,160, 17 Meta-attributed bookings, blended ROAS 5.1x, retargeting ROAS 17.1x, CPL $0.33 on 2813 leads · August: spend $2,193, 19 Meta-attributed bookings, blended ROAS 6.3x, retargeting ROAS 22.3x, CPL $0.36 on 2589 leads · September: spend $2,155, 61 Meta-attributed bookings, blended ROAS 16.5x, retargeting ROAS 28.5x, CPL $0.34 on 2597 leads · October: spend $2,298, 71 Meta-attributed bookings, blended ROAS 21.0x, retargeting ROAS 22.1x, CPL $0.32 on 2869 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF holds Scale and rises from 18.3x to 27.9x on 12 purchases ($280). The account is at $75/day, the CRM's $2,250/month range. A paused lookalike build ('MoF - Lookalike Sales Campaign - 11/19/2026', created through the system user on 19 Nov) waits in the account; it has no spend.

### Stay Saluda NC — AM Makenna — account Stay Saluda Ads (1863632561215857) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $897 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,580; pixel purchase value $10,362 + sign-up promo revenue $13,995 = $24,357, ROAS 9.4x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $17,535 from 28 bookings, +37% vs 1 Oct–23 Oct ($12,760 from 24 bookings) · promo codes: 14 uses (ENJOY10 ×11, VIP10 ×2, WELCOME10 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $421 | 3 purchases | ROAS 3.6x | 4.28 | Review w/ HG AI | CPC $0.83 > $0.62; CPM $20.78 > $16.50; cost/booking $140.48 > $90; freq 4.3 > 3.0 | 30d ROAS 11.0x, 15 purchases | New flag, was Healthy |
| MoF - Lookalike Sales Campaign - 11/13/2026 | Prospecting (MoF lookalike) | 14d | $190 | 1 purchases | ROAS 2.7x | 1.53 | Under gate | CPM $17.64 > $16.50; cost/booking $190.26 > $90 | spend $190.26 < $200 gate; 30d ROAS 2.7x, 1 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $598 | 595 leads | CPL $1.00 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.02 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,495 | 17 promo bookings, $13,995 | promo ROAS 9.4x | — | Not scored (discovery) | ENJOY10 ×15 $10,825, WELCOME10 ×2 $3,170; not counted (not sign-up codes): VIP10 ×2 $1,298 | $1,495 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Giveaway Traffic Campaign - NC/SC/GA/TN, against direct bookings booked 24 Oct–23 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $2,140, 10 Meta-attributed bookings, blended ROAS 2.6x, retargeting ROAS 0.8x · August: spend $2,367, 10 Meta-attributed bookings, blended ROAS 3.9x, retargeting ROAS 5.2x, CPL $2.59 on 146 leads · September: spend $2,394, 14 Meta-attributed bookings, blended ROAS 3.8x, retargeting ROAS 3.5x, CPL $1.00 on 596 leads · October: spend $2,449, 25 Meta-attributed bookings, blended ROAS 7.0x, retargeting ROAS 5.7x, CPL $0.94 on 647 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF drops from Healthy (14.4x) to Review at 3.6x on 3 purchases ($421 in 14 days), a new Action row; 30-day 11.0x on 15 purchases, frequency 4.3. The pixel recorded only 2 Purchases in the last 7 days against 3 online bookings, so part of the drop is a quiet booking week; nothing changed in the account (activity log empty). The 13 Nov lookalike is under the gate at 2.7x on 1 purchase ($190). Discovery read (context only) 9.4x: ENJOY10 ×15 and WELCOME10 ×2 on $1,495. Direct revenue month to date +37% on October.

### FLOHOM — AM Makenna — account FLOHOM Ads (2100710320122219) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $301 over 30 days.

Blended 30d (every HiddenGem campaign): spend $4,211; pixel purchase value $30,947 + sign-up promo revenue $15,099 = $46,046, ROAS 10.9x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $50,858 from 63 bookings, −40% vs 1 Oct–23 Oct ($85,115 from 94 bookings) · promo codes: 11 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| [Myrtle Beach] MoF - Lookalike Sales Campaign - 09/17/26 | Prospecting (MoF lookalike) | 14d | $222 | 1 purchases | ROAS 4.2x | 2.30 | Review w/ HG AI | CPC $1.23 > $0.62; CPM $21.36 > $16.50; cost/booking $221.60 > $90 | 30d ROAS 6.0x, 2 purchases | Still open, week 2 |
| MoF - Lookalike Sales Campaign - 07/29/26 | Prospecting (MoF lookalike) | 14d | $708 | 9 purchases | ROAS 7.8x | 1.83 | Monitor | CPC $0.65 > $0.62; CPM $19.44 > $16.50 | 30d ROAS 10.7x, 21 purchases | Unchanged |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $711 | 8 purchases | ROAS 12.8x | 2.11 | Healthy | CPM $16.62 > $16.50 | 30d ROAS 7.7x, 12 purchases | Unchanged |
| [Myrtle Beach] MoF - Broad - 11/16/26 | Prospecting (MoF lookalike) | 14d | $67 | 0 purchases | ROAS — | 1.64 | Under gate | CPC $0.96 > $0.62 | spend $67.05 < $200 gate | New, not in the 16 Nov run |
| MoF - Lead Campaign - Retargeting Engagers – 08/17/26 | Lead Gen (MoF) | 30d | $299 | 507 leads | CPL $0.59 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.67 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $600 | 17 promo bookings, $15,099 | promo ROAS 25.2x | — | Not scored (discovery) | 17 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $600 in 30 days across ToF - Giveaway Traffic Campaign, MoF - Lead Campaign - Retargeting Engagers – 08/17/26, against direct bookings booked 24 Oct–23 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $5,555, 103 Meta-attributed bookings, blended ROAS 17.2x, retargeting ROAS 19.1x, CPL $7.66 on 66 leads · August: spend $9,331, 90 Meta-attributed bookings, blended ROAS 8.5x, retargeting ROAS 8.2x, CPL $2.24 on 708 leads · September: spend $8,855, 82 Meta-attributed bookings, blended ROAS 8.9x, retargeting ROAS 8.9x, CPL $0.50 on 2192 leads · October: spend $5,455, 71 Meta-attributed bookings, blended ROAS 12.0x, retargeting ROAS 9.7x, CPL $0.56 on 809 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF holds Healthy, up from 10.0x to 12.8x on 8 purchases ($711). The main lookalike holds Monitor at 7.8x on 9 purchases ($708). The Myrtle Beach lookalike stays Review, week 2, at 4.2x on 1 purchase ($222); on 16 Nov Shawal cut it from $20 to $10/day and added '[Myrtle Beach] MoF - Broad - 11/16/26' at $10/day (0 purchases on $67, under the gate). Direct revenue month to date $50.9k, −40% on October (63 bookings against 94). Discovery read (context only) 25.2x on 17 Hostaway coupon bookings.

### Asheville River Cabins — AM Charlotte — account Asheville River Cabins Ads (615836588009747) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,101 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,796; pixel purchase value $22,078 + sign-up promo revenue $0 = $22,078, ROAS 7.9x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Broad - 06/08/26 | Prospecting (MoF lookalike) | 14d | $694 | 11 purchases | ROAS 13.5x | 2.25 | Healthy | CPC $0.70 > $0.62; CPM $17.34 > $16.50 | 30d ROAS 17.9x, 32 purchases | Was Scale w/ HG AI |
| BoF - Website Retargeting Campaign - 11/16/26 | Retargeting (BoF) | 14d | $132 | 0 purchases | ROAS — | 1.92 | Under gate | CPC $1.04 > $0.62; CPM $18.52 > $16.50 | spend $131.66 < $200 gate | New, not in the 16 Nov run |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $301 | 733 leads | CPL $0.41 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.43 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,402 | — | promo ROAS — | — | Not scored (discovery) | — | $1,402 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Discovery Campaign Giveaway - 09/17/26; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Paused in window, not scored: BoF - Website Retargeting Campaign - 12/11/26 (Retargeting (BoF)), $75 / 14d, 1 purchases, ROAS 11.1x. Live campaigns only are scored (decision 2026-09-23).

Monthly ROI: July: spend $2,029, 39 Meta-attributed bookings, blended ROAS 18.6x, retargeting ROAS 51.6x · August: spend $2,424, 82 Meta-attributed bookings, blended ROAS 27.2x, retargeting ROAS 65.0x, CPL $0.42 on 605 leads · September: spend $2,252, 70 Meta-attributed bookings, blended ROAS 19.1x, retargeting ROAS 42.5x, CPL $0.30 on 936 leads · October: spend $2,233, 68 Meta-attributed bookings, blended ROAS 23.1x, retargeting ROAS 27.4x, CPL $0.32 on 869 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). 'MoF - Broad - 06/08/26' (the old 26x BoF, renamed with no audience on 12 Nov) falls from Scale (26.2x) to Healthy at 13.5x on 11 purchases ($694) as its retargeting history leaves the window. On 16 Nov Shawal rebuilt retargeting as 'BoF - Website Retargeting Campaign - 11/16/26' (Website Visitors 180D, $20/day) in place of the 12/11 one: 0 purchases on $132, under the gate. All Purchases are browser-side: the Cloudbeds API is not enabled for the HG AI CAPI (pixel check, week 10).

### Little River Landing — AM Makenna — account Little River Landing (884285717873613) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,680 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,509; pixel purchase value $691 + sign-up promo revenue $393 = $1,084, ROAS 0.4x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $1,901 from 12 bookings, −22% vs 1 Oct–23 Oct ($2,430 from 14 bookings) · promo codes: 1 uses (STAY10 ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 09/16/2026 | Retargeting (BoF) | 14d | $258 | 1 purchases | ROAS 1.2x | 3.36 | Flag to Shawal | CPC $0.79 > $0.62; cost/booking $258.47 > $90; freq 3.4 > 3.0 | 30d ROAS 1.4x, 2 purchases | Still open, week 3 |
| MoF - Lookalike Sales Campaign - 11/13/2026 | Prospecting (MoF lookalike) | 14d | $189 | 0 purchases | ROAS — | 1.42 | Under gate | CPC $0.74 > $0.62; CPM $17.87 > $16.50 | spend $188.97 < $200 gate | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 09/16/2026 | Lead Gen (MoF) | 30d | $150 | 77 leads | CPL $1.95 (diagnostic) | — | Not scored (lead gen) | CPC $0.50 > $0.30; CPM $25.56 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $2.00 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,830 | 1 promo bookings, $393 | promo ROAS 0.2x | — | Not scored (discovery) | WELCOME10 ×1 $393; not counted (not sign-up codes): STAY10 ×1 $223 | $1,830 in 30 days across ToF - Giveaway Traffic Campaign - AL - 09/16/2026, MoF - Lead Campaign - Retargeting Engagers - 09/16/2026, against direct bookings booked 24 Oct–23 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: September: spend $921, 0 Meta-attributed bookings, blended ROAS —, retargeting ROAS —, CPL $1.86 on 46 leads · October: spend $2,165, 1 Meta-attributed bookings, blended ROAS 0.2x, retargeting ROAS 1.5x, CPL $1.50 on 101 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF stays Flag, week 3: 1.2x on 1 purchase ($258 in 14 days), 30-day 1.4x on 2. Tracking is still the first fix: 3 Purchase in 28 days against 9 PMS online bookings (33%), none since 12 Nov, with the HG AI CAPI off (pixel check ❌). The 13 Nov lookalike has 0 purchases on $189, under the gate. That is $40/day on Sales learning on almost no Purchase signal. Recommendation: pause the lookalike and hold BoF at $20 until the CAPI is on (Makenna / Leshan). Discovery read 0.2x on $1,830.

### Selah Place — AM Alicia — account Selah.place (1275283434220508) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $903 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,423; pixel purchase value $11,154 + sign-up promo revenue $11,137 = $22,291, ROAS 9.2x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $16,717 from 39 bookings, −21% vs 1 Oct–23 Oct ($21,032 from 40 bookings) · promo codes: 14 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF-Website Retarget Campaign - 07/24/2026 | Retargeting (BoF) | 14d | $420 | 14 purchases | ROAS 17.6x | 3.65 | Scale w/ HG AI | CPC $0.70 > $0.62; CPM $24.31 > $16.50; freq 3.6 > 3.0 | 30d ROAS 11.3x, 23 purchases | Unchanged |
| MoF - Lookalike Sales Campaign - 11/13/2026 | Prospecting (MoF lookalike) | 14d | $189 | 2 purchases | ROAS 5.1x | 1.45 | Under gate | cost/booking $94.35 > $90 | spend $188.70 < $200 gate; 30d ROAS 5.1x, 2 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $432 | 490 leads | CPL $0.88 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.98 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,335 | 22 promo bookings, $11,137 | promo ROAS 8.3x | — | Not scored (discovery) | 22 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $1,335 in 30 days across MoF - Lead Campaign - Retargeting Engagers, ToF - Giveaway Traffic Campaign - 08/07/2026, against direct bookings booked 24 Oct–23 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Client-run, not scored: SP / Willow / Pre-Sales / VIP List / 10-2026 (Sales, paused), created by Nathan Jay Herrington on 2026-10-19, $442 / 14d, 2 purchases, ROAS 0.2x. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Willow / Lead Gen / VIP List / 10-2026 (Lead Gen (MoF), active), created by Nathan Jay Herrington on 2026-10-20, $1,852 / 30d, 1071 leads, CPL $1.73. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Willow / Sales / Top-5 Audiences / 11-2026 (Sales, active), created by Nathan Jay Herrington on 2026-10-28, $1,942 / 14d, 14 purchases, ROAS 0.6x. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Black Walnut / Sales / Pre-Sale / 11-2026 (Sales, active), created by Nathan Jay Herrington on 2026-11-05, $51 / 14d, 0 purchases, ROAS —. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Black Walnut / Leads / Early Access / 11-2026 (Lead Gen (MoF), paused), created by Nathan Jay Herrington on 2026-11-07, $762 / 30d, 68 leads, CPL $11.21. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Black Walnut / Leads / BF Pre-Booking / 11-2026 (Lead Gen (MoF), active), created by Nathan Jay Herrington on 2026-11-18, $19 / 30d, 2 leads, CPL $9.28. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Black Walnut / Sales / BF Pre-Booking / 11-2026 (Sales, active), created by Nathan Jay Herrington on 2026-11-18, $19 / 14d, 0 purchases, ROAS —. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: SP / Selah Place / Sales / BF Robe $50 / 11-2026 (Sales, paused), created by Nathan Jay Herrington on 2026-11-18, $5 / 14d, 0 purchases, ROAS —. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Monthly ROI: July: spend $1,054, 4 Meta-attributed bookings, blended ROAS 3.2x, retargeting ROAS 86.3x, CPL $0.80 on 49 leads · August: spend $1,545, 15 Meta-attributed bookings, blended ROAS 4.8x, retargeting ROAS 25.1x, CPL $1.08 on 144 leads · September: spend $1,304, 27 Meta-attributed bookings, blended ROAS 10.4x, retargeting ROAS 38.2x, CPL $0.63 on 232 leads · October: spend $1,842, 23 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 9.7x, CPL $0.61 on 405 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). HiddenGem's BoF holds Scale at 17.6x on 14 purchases ($420), frequency 3.6; the client (Nathan Jay Herrington) raised it from $30 to $50/day on 23 Nov. Read it with care: the pixel's server Purchases run 2.9x the PMS bookings (HG AI CAPI plus Hostaway's CAPI). The 13 Nov lookalike is under the gate at 5.1x. On 22 and 23 Nov the client moved most of the Willow budget into three Black Walnut BF Pre-Booking / Pre-Sale campaigns and switched a BF Robe sales campaign on and off; all client-run, listed not scored. Direct revenue month to date −21% on October.

### Starlight Haven Weiss Lake — AM Charlotte — account Starlight Haven Weiss Lake (74756899) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $0 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,155; pixel purchase value $22,753 + sign-up promo revenue $0 = $22,753, ROAS 10.6x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $688 | 14 purchases | ROAS 7.3x | 2.71 | Monitor | CPC $0.97 > $0.62 | 30d ROAS 16.3x, 46 purchases | Was Scale w/ HG AI |
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $755 | 623 leads | CPL $1.21 (diagnostic) | — | Not scored (lead gen) | CPC $0.36 > $0.30 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.45 | Unchanged |
| Discovery bucket (1 campaign: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $755 | — | promo ROAS — | — | Not scored (discovery) | — | $755 in 30 days across New Leads Campaign - 03/03/26; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $2,163, 41 Meta-attributed bookings, blended ROAS 10.8x, retargeting ROAS 15.2x, CPL $0.74 on 826 leads · August: spend $2,351, 36 Meta-attributed bookings, blended ROAS 10.7x, retargeting ROAS 17.6x, CPL $1.23 on 617 leads · September: spend $2,152, 79 Meta-attributed bookings, blended ROAS 17.4x, retargeting ROAS 23.8x, CPL $1.01 on 734 leads · October: spend $2,142, 53 Meta-attributed bookings, blended ROAS 15.6x, retargeting ROAS 24.2x, CPL $1.09 on 704 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF drops from Scale (17.6x) to Monitor at 7.3x on 14 purchases ($688); 30-day 16.3x on 46 purchases, so this is a softer fortnight rather than a break. A paused lookalike build (11/19/2026, system user) waits in the account with no spend.

### Ridge & Falls — AM Makenna — account Ridge & Falls ad account (1313401330776046) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,506 over 30 days.

Blended 30d (every HiddenGem campaign): spend $2,091; pixel purchase value $9,422 + sign-up promo revenue $0 = $9,422, ROAS 4.5x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $7,531 from 16 bookings, +83% vs 1 Oct–23 Oct ($4,114 from 9 bookings) · promo codes: 9 uses (HELLO10 ×6, STAY10 ×2, 15% ×1).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 09/01/26 | Retargeting (BoF) | 14d | $207 | 11 purchases | ROAS 25.8x | 4.93 | Scale w/ HG AI | freq 4.9 > 3.0 | 30d ROAS 21.6x, 21 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 09/01/26 | Lead Gen (MoF) | 30d | $150 | 55 leads | CPL $2.72 (diagnostic) | — | Not scored (lead gen) | CPC $0.36 > $0.30 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $3.87 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,655 | 0 promo bookings, $0 | promo ROAS 0.0x | — | Not scored (discovery) | no sign-up code bookings in 30 days; not counted (not sign-up codes): HELLO10 ×6 $2,794, STAY10 ×2 $955, 15% ×1 $300 | $1,655 in 30 days across ToF - Giveaway Traffic Campaign - GA, AL - 09/01/26, MoF - Lead Campaign - Retargeting Engagers - 09/01/26, against direct bookings booked 24 Oct–23 Nov with a sign-up code; no sign-up promo bookings in 30 days; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: September: spend $1,036, 0 Meta-attributed bookings, blended ROAS —, retargeting ROAS —, CPL $8.16 on 16 leads · October: spend $1,941, 10 Meta-attributed bookings, blended ROAS 2.5x, retargeting ROAS 18.7x, CPL $2.33 on 64 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF holds Scale at 25.8x on 11 purchases ($207), frequency 4.9. The ROAS is inflated: the pixel receives about 1.7 server Purchases per PMS booking (two senders, week 4). At $70/day the account is at its CRM range. Direct revenue month to date $7.5k, +83% on October. Discovery read 0.0x: HELLO10 ×6 and STAY10 ×2 are not sign-up codes.

### Gooseberry Lodges — AM Alicia — account Gooseberry Ad Account (701051796368186) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $1,060 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,646; pixel purchase value $0 + sign-up promo revenue $0 = $0, ROAS 0.0x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 10.27/2026 | Retargeting (BoF) | 14d | $284 | 0 purchases | ROAS — | 1.83 | Flag to Shawal | CPC $0.93 > $0.62 | no purchases | New flag, was Under gate |
| MoF - Lead Campaign - Retargeting Engagers - 10/27/2026 | Lead Gen (MoF) | 30d | $238 | 144 leads | CPL $1.66 (diagnostic) | — | Not scored (lead gen) | CPC $0.39 > $0.30 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.70 | Unchanged |
| Discovery bucket (3 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,299 | — | promo ROAS — | — | Not scored (discovery) | — | $1,299 in 30 days across ToF - Giveaway Traffic Campaign - SW Drive Markets (LV / SoCal / NUT) - 10/27/2026 (paused), MoF - Lead Campaign - Retargeting Engagers - 10/27/2026, ToF - Giveaway Traffic Campaign - SW Drive Markets (LV / SoCal / NUT) - 10/27/2026; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF crosses the gate with 0 purchases on $284 in 14 days: Flag, new. The pixel recorded 47 browser Purchases in 28 days (11 in the last 7) from the SiteMinder engine, so bookings are tracked but none is attributed to the retargeting ads. The ad account was on a payment hold from 20 Nov until it cleared over the weekend, which cut delivery. Little Hotelier has no API, so the HG AI platform cannot see bookings to compare. Next step (Alicia): check the BoF audience size and whether the Purchase event carries a value; hold the budget at $25/day until the first attributed purchase. Leads $1.66 on 144.

### Green Springs Inn — AM Alicia — account Green Springs Inn (1390516335151357) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $603 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,202; pixel purchase value $7,353 + sign-up promo revenue $16,983 = $24,336, ROAS 20.2x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $31,789 from 65 bookings, +13% vs 1 Oct–23 Oct ($28,112 from 65 bookings) · promo codes: 25 uses (Hostaway does not store code names).

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 08/28/26 | Retargeting (BoF) | 14d | $141 | 8 purchases | ROAS 32.7x | 2.93 | Under gate | CPC $0.87 > $0.62 | spend $140.94 < $200 gate; 30d ROAS 24.5x, 13 purchases | Unchanged |
| MoF - Lead Campaign/08/28/2026 | Lead Gen (MoF) | 30d | $300 | 157 leads | CPL $1.91 (diagnostic) | — | Not scored (lead gen) | CPC $0.36 > $0.30 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.84 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $903 | 31 promo bookings, $16,983 | promo ROAS 18.8x | — | Not scored (discovery) | 31 coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes) | $903 in 30 days across ToF - Giveaway Traffic Campaign - 07/24/2026, MoF - Lead Campaign/08/28/2026, against direct bookings booked 24 Oct–23 Nov with a sign-up code; context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM) | Unchanged |

Monthly ROI: July: spend $1,222, 17 Meta-attributed bookings, blended ROAS 7.8x, retargeting ROAS 14.6x, CPL $5.65 on 8 leads · August: spend $1,247, 23 Meta-attributed bookings, blended ROAS 8.2x, retargeting ROAS 17.1x, CPL $9.09 on 34 leads · September: spend $1,199, 24 Meta-attributed bookings, blended ROAS 8.5x, retargeting ROAS 9.0x, CPL $1.84 on 166 leads · October: spend $1,231, 26 Meta-attributed bookings, blended ROAS 10.6x, retargeting ROAS 9.5x, CPL $1.42 on 214 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF under the gate at 32.7x on 8 purchases ($141). Discovery read (context only) 18.8x on 31 Hostaway coupon bookings (no code names). Direct revenue month to date +13% on October.

### Sunapee Stays — AM Charlotte — account Sunapee Stays Ads Account (651114096215889) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $773 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,253; pixel purchase value $1,737 + sign-up promo revenue $0 = $1,737, ROAS 1.4x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $10,223 from 19 bookings, −60% vs 1 Oct–23 Oct ($25,396 from 45 bookings) · promo codes: not tracked by ownerrez.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $81 | 2 purchases | ROAS 21.6x | 2.68 | Under gate | CPC $0.75 > $0.62 | spend $80.53 < $200 gate; 30d ROAS 7.2x, 2 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $239 | 109 leads | CPL $2.19 (diagnostic) | — | Not scored (lead gen) | CPC $0.52 > $0.30; CPM $20.19 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.84 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $1,012 | — | promo ROAS — | — | Not scored (discovery) | — | $1,012 in 30 days across ToF Discovery Campaign - Giveaway - 06/10/26, MoF - Lead Campaign - Retargeting Engagers; ownerrez does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $939, 16 Meta-attributed bookings, blended ROAS 9.9x, CPL $2.06 on 9 leads · August: spend $1,494, 10 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 25.1x, CPL $2.74 on 112 leads · September: spend $1,495, 14 Meta-attributed bookings, blended ROAS 6.5x, retargeting ROAS 6.7x, CPL $1.64 on 184 leads · October: spend $1,540, 11 Meta-attributed bookings, blended ROAS 3.4x, retargeting ROAS 10.7x, CPL $1.89 on 161 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF under the gate at 21.6x on 2 purchases ($81). Month-to-date direct revenue $10.2k against $25.4k on the same days of October (−60%).

### Glasscombe — AM Charlotte — account Glasscombe (2030318804465316) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $601 over 30 days.

Blended 30d (every HiddenGem campaign): spend $991; pixel purchase value $4,489 + sign-up promo revenue $0 = $4,489, ROAS 4.5x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $11,469 from 21 bookings, +202% vs 1 Oct–23 Oct ($3,801 from 11 bookings) · promo codes: not tracked by cloudbeds.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 10/09/26. | Retargeting (BoF) | 14d | $141 | 5 purchases | ROAS 31.8x | 1.89 | Under gate | CPM $21.56 > $16.50 | spend $141.31 < $200 gate; 30d ROAS 20.5x, 5 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers -  10/09/26 | Lead Gen (MoF) | 30d | $172 | 483 leads | CPL $0.36 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $0.41 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $773 | — | promo ROAS — | — | Not scored (discovery) | — | $773 in 30 days across ToF - Giveaway Traffic Campaign - UK, MoF - Lead Campaign - Retargeting Engagers -  10/09/26; cloudbeds does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: October: spend $541, 2 Meta-attributed bookings, blended ROAS 2.2x, retargeting ROAS —, CPL $0.29 on 306 leads. Note in the October file: LaunchBoom pre-bookings led to high occupancy at low revenue this month (AM note from the tracking sheet).

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF under the gate at 31.8x on 5 purchases ($141); Charlotte raised BoF from $5 to $20 and leads from $5 to $10 on 18 Nov. Leads $0.36 on 483. Direct revenue month to date $11.5k, +202% on October.

### Cabin Collective — AM Chiara — account Cabin Collective (2194562394139883) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $302 over 30 days.

Blended 30d (every HiddenGem campaign): spend $903; pixel purchase value $19,579 + sign-up promo revenue $0 = $19,579, ROAS 21.7x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $41,444 from 23 bookings, −12% vs 1 Oct–23 Oct ($47,309 from 26 bookings) · promo codes: not tracked by ownerrez.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 10/20/26 | Retargeting (BoF) | 14d | $138 | 6 purchases | ROAS 83.2x | 2.32 | Under gate | CPM $17.71 > $16.50 | spend $138.47 < $200 gate; 30d ROAS 64.9x, 12 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 10/20/26 | Lead Gen (MoF) | 30d | $299 | 234 leads | CPL $1.28 (diagnostic) | — | Not scored (lead gen) | within lines | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.49 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $601 | — | promo ROAS — | — | Not scored (discovery) | — | $601 in 30 days across ToF - Giveaway Traffic Campaign - [TX, OK, AR] - 10/20/26, MoF - Lead Campaign - Retargeting Engagers - 10/20/26; ownerrez does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: October: spend $312, 6 Meta-attributed bookings, blended ROAS 28.8x, retargeting ROAS 86.4x, CPL $1.31 on 79 leads. Note in the October file: No booking-level export from the client this month; the direct booking revenue is the client reporting sheet figure and the booking count is unavailable. Attributed revenue comes from Meta-reported retargeting purchases only.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF under the gate at 83.2x on 6 purchases ($138). The ROAS is inflated: since 16 Nov the HG AI CAPI and OwnerRez both send server Purchases (1.5x bookings, pixel check). A paused lookalike build (11/19/2026, system user) waits in the account. Direct revenue month to date −12% on October. Master sheet still reads Not Live.

### The Outpost — AM Anna — account The Outpost Grand Canyon (1530849534802936) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $896 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,200; pixel purchase value $1,032 + sign-up promo revenue $0 = $1,032, ROAS 0.9x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $10,278 from 23 bookings, −40% vs 1 Oct–23 Oct ($17,011 from 37 bookings) · promo codes: not tracked by newbook.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 10/08/2026 | Retargeting (BoF) | 14d | $141 | 1 purchases | ROAS 3.0x | 2.63 | Under gate | CPC $0.84 > $0.62; CPM $17.13 > $16.50; cost/booking $141.47 > $90 | spend $141.47 < $200 gate; 30d ROAS 3.4x, 3 purchases | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $896 | — | promo ROAS — | — | Not scored (discovery) | — | $896 in 30 days across Insta Discovery Campaign - Giveaway - May 2026, Facebook Discovery Campaign - Giveaway - May 2026; newbook does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: July: spend $2,182, 1 Meta-attributed bookings, blended ROAS 0.2x, CPL $1.61 on 202 leads · August: spend $1,876, 7 Meta-attributed bookings, blended ROAS 2.1x, CPL $1.71 on 181 leads · September: spend $2,081, 18 Meta-attributed bookings, blended ROAS 3.8x, retargeting ROAS —, CPL $1.80 on 167 leads · October: spend $2,149, 12 Meta-attributed bookings, blended ROAS 2.8x, retargeting ROAS 1.9x, CPL $1.73 on 176 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). Only the 10/08 BoF is live: 3.1x on 1 purchase ($141), under the gate. Direct revenue month to date −40% on October. Pixel: Purchase capture 55% of 31 online bookings, and the funnel is still split across two pixels.

### Walden Retreats — AM Anna — account Walden Retreats (973261794434226) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $300 over 30 days.

Blended 30d (every HiddenGem campaign): spend $895; pixel purchase value $5,518 + sign-up promo revenue $0 = $5,518, ROAS 6.2x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 06/10/2026 | Retargeting (BoF) | 14d | $135 | 7 purchases | ROAS 29.5x | 2.23 | Under gate | CPC $0.83 > $0.62; CPM $27.04 > $16.50 | spend $134.68 < $200 gate; 30d ROAS 18.7x, 12 purchases | New, not in the 16 Nov run |
| MoF - Lead Campaign - Retargeting Engagers - 10/06/2026 | Lead Gen (MoF) | 30d | $299 | 253 leads | CPL $1.18 (diagnostic) | — | Not scored (lead gen) | CPC $0.35 > $0.30; CPM $17.77 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.22 | Unchanged |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $599 | — | promo ROAS — | — | Not scored (discovery) | — | $599 in 30 days across ToF - Giveaway Traffic Campaign - ATX, HTX, DAL, SATX, FTW - 10/05/2026, MoF - Lead Campaign - Retargeting Engagers - 10/06/2026; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Client-run, not scored: TOF Wedding Leads 10.8.26 (Lead Gen (MoF), paused), created by Lindsey Cooke on 2026-10-08, $266 / 30d, 12 leads, CPL $22.19. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Client-run, not scored: MOF Wedding Leads 10.27.26 (Lead Gen (MoF), paused), created by Lindsey Cooke on 2026-10-27, $32 / 30d, 1 leads, CPL $31.58. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Monthly ROI: October: spend $1,295, 26 Meta-attributed bookings, blended ROAS 16.6x, retargeting ROAS 30.8x, CPL $3.57 on 220 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). Ananya switched the BoF back on on 17 Nov after the VIP promo code issue: 29.5x on 7 purchases ($135), under the gate. The pixel recorded 102 Purchase in 7 days with spikes on 16 and 21 Nov and no PMS to check them against (pixel check), so the ROAS may be inflated. A paused lookalike build (11/20/2026, system user) waits in the account.

### North Star Lodge & Resort — AM Charlotte — account North Star Lodge & Resort Ads (2003562593933799) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $602 over 30 days.

Blended 30d (every HiddenGem campaign): spend $901; pixel purchase value $1,030 + sign-up promo revenue $0 = $1,030, ROAS 1.1x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $48,844 from 79 bookings, −11% vs 1 Oct–23 Oct ($54,731 from 147 bookings) · promo codes: not tracked by cloudbeds.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors - 09/09/2026 | Retargeting (BoF) | 14d | $69 | 2 purchases | ROAS 9.1x | 3.17 | Under gate | CPC $0.95 > $0.62; freq 3.2 > 3.0 | spend $69.18 < $200 gate; 30d ROAS 6.9x, 3 purchases | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 10/02/26 | Lead Gen (MoF) | 30d | $13 | 1 leads | CPL $12.94 (diagnostic) | — | Under gate | CPC $1.29 > $0.30; CPM $29.48 > $14.84 | spend $12.94 < $100 gate | Unchanged |
| MoF - Lead Campaign - Retargeting Engagers - 10/26/26 | Lead Gen (MoF) | 30d | $137 | 69 leads | CPL $1.98 (diagnostic) | — | Not scored (lead gen) | CPC $0.45 > $0.30; CPM $16.56 > $14.84 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.72 | Unchanged |
| Discovery bucket (3 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $752 | — | promo ROAS — | — | Not scored (discovery) | — | $752 in 30 days across ToF - Giveaway Traffic Campaign - 09/09/2002, MoF - Lead Campaign - Retargeting Engagers - 10/02/26, MoF - Lead Campaign - Retargeting Engagers - 10/26/26; cloudbeds does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | Unchanged |

Monthly ROI: September: spend $580, 0 Meta-attributed bookings, blended ROAS — · October: spend $919, 2 Meta-attributed bookings, blended ROAS 0.7x, retargeting ROAS 1.4x, CPL $22.29 on 6 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). BoF under the gate at 9.1x on 2 purchases ($69). The 10/02 lead campaign's ad set is paused (1 lead on $13 in 30 days), so only 10/26 runs (69 leads at $1.98); the spend check now counts the 10/02 campaign as $0. Direct revenue month to date −11% on October. Pixel: Purchase capture 64% of 56 online bookings.

### Dunya Camp — AM Chiara — account Dunya Camp (629838998232110) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $247 over 30 days.

Blended 30d (every HiddenGem campaign): spend $1,195; pixel purchase value $5,533 + sign-up promo revenue $0 = $5,533, ROAS 4.6x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $123 | 0 purchases | ROAS — | 1.36 | Under gate | CPC $0.77 > $0.62 | spend $123.30 < $200 gate | New, not in the 16 Nov run |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $124 | 92 leads | CPL $1.35 (diagnostic) | — | Not scored (lead gen) | CPC $0.35 > $0.30 | only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context; 14d CPL $1.35 | New, not in the 16 Nov run |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $371 | — | promo ROAS — | — | Not scored (discovery) | — | $371 in 30 days across ToF - Giveaway Traffic Campaign, MoF - Lead Campaign - Retargeting Engagers; no PMS connection on the HiddenGem AI platform, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | New, not in the 16 Nov run |

Deferred, not scored: Retargeting - Sales - Step 3 (Retargeting (BoF)), $216 / 14d, 1 purchases, ROAS 4.5x. It optimises on Dunya Camp's custom 'Step 3' event; part of the older custom-event funnel left as is (Shawal, 12 Nov 2026).

Deferred, not scored: Fall step 2 campaign (Sales), $687 / 14d, 0 purchases, ROAS —. It optimises on Dunya Camp's custom 'Step 2' event, not Purchase, so purchase ROAS does not apply; part of the older custom-event funnel left as is (Shawal, 12 Nov 2026).

Client-run, not scored: fall winter purchase 2026 (Sales, active), created by Sangeetha Ramkumar on 2026-10-07, $423 / 14d, 1 purchases, ROAS 6.9x. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). Second week. HiddenGem's build has spent for the first time: BoF $123 with 0 purchases (under the gate) and the lead campaign 92 leads at $1.35. The older funnel continues: 'Fall step 2' (client, Sangeetha Ramkumar, $59 to $43/day on 17 and 19 Nov) is deferred, 'Retargeting - Sales - Step 3' was switched off by the client on 16 Nov, and the client's own 'fall winter purchase 2026' runs at $30/day. The pixel recorded 24 Purchase in 28 days, none since 18 Nov. No PMS connection.

### Arca Boutique Hotel — AM Anna — account Arca Ad account (1003623765640520) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $67 over 30 days.

Blended 30d (every HiddenGem campaign): spend $179; pixel purchase value $1,880 + sign-up promo revenue $0 = $1,880, ROAS 10.5x. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.

This month (booked 1 Nov–23 Nov): direct revenue $79,467 from 25 bookings, −26% vs 1 Oct–23 Oct ($107,692 from 37 bookings) · promo codes: not tracked by cloudbeds.

| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers - 11/16/2026 | Lead Gen (MoF) | 30d | $58 | 63 leads | CPL $0.92 (diagnostic) | — | Under gate | CTR 2.97% < 3.03% | spend $58.23 < $100 gate; 14d CPL $0.92 | New, not in the 16 Nov run |
| BoF - Sales Campaign - Retargeting Website Visitors - 11/18/2026 | Retargeting (BoF) | 14d | $49 | 1 purchases | ROAS 38.5x | 2.17 | Under gate | within lines | spend $48.88 < $200 gate; 30d ROAS 38.5x, 1 purchases | New, not in the 16 Nov run |
| Discovery bucket (2 campaigns: giveaway + leads) | Discovery (ToF + MoF leads) | 30d | $125 | — | promo ROAS — | — | Not scored (discovery) | — | $125 in 30 days across ToF - Discovery Campaign - Giveaway - 11/13/2026, MoF - Lead Campaign - Retargeting Engagers - 11/16/2026; cloudbeds does not store promo codes on the booking, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026) | New, not in the 16 Nov run |

Paused in window, not scored: BoF - Sales Campaign - Retargeting Website Visitors - 11/17/2026 (Retargeting (BoF)), $5 / 14d, 0 purchases, ROAS —. Live campaigns only are scored (decision 2026-09-23).

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: no HG AI reports this week (none filed since 23 Sep). First full build since 16 to 18 Nov (Ananya and Shawal): giveaway $10, lead $10 (63 leads at $0.92, under the gate) and BoF $10 (1 purchase, 38.5x on $49, under the gate). The pixel misses the main site arcaroatan.com while BoF links there (pixel check). Cloudbeds is connected and the HG AI CAPI went on 18 Nov. Direct revenue month to date $79.5k, −26% on October.

### American River Resort — AM Nicole — account American River Resort (953162737054331) — live read

ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): $0 over 30 days.

Blended 30d: no HiddenGem campaign spend in the window.

This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here.

No live Lead Gen, Sales or Discovery campaigns with spend in the window.

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
- Client-run campaigns (created by a non-HiddenGem login per the account activity log, listed under the client, never scored): Tàberg Falls: TF / Speed Plan / Clean build (Denver Brenizer); Selah Place: SP / Willow / Pre-Sales / VIP List / 10-2026 (Nathan Jay Herrington), SP / Willow / Lead Gen / VIP List / 10-2026 (Nathan Jay Herrington), SP / Willow / Sales / Top-5 Audiences / 11-2026 (Nathan Jay Herrington), SP / Black Walnut / Sales / Pre-Sale / 11-2026 (Nathan Jay Herrington), SP / Black Walnut / Leads / Early Access / 11-2026 (Nathan Jay Herrington), SP / Black Walnut / Leads / BF Pre-Booking / 11-2026 (Nathan Jay Herrington), SP / Black Walnut / Sales / BF Pre-Booking / 11-2026 (Nathan Jay Herrington), SP / Selah Place / Sales / BF Robe $50 / 11-2026 (Nathan Jay Herrington); Walden Retreats: TOF Wedding Leads 10.8.26 (Lindsey Cooke), MOF Wedding Leads 10.27.26 (Lindsey Cooke); Dunya Camp: fall winter purchase 2026 (Sangeetha Ramkumar); The Preserve: Cl:Preserve_Ch:Meta_Obj:Conv_Tac:Prospecting_Typ:ABO_Of:EVG_CT:Standard_Notes: (Maddy Watson), Cl:Preserve_Ch:Meta_Obj:Conv_Tac:Retargeting_Typ:ABO_Of:EVG_CT:Standard_Notes: (Maddy Watson). Creators are known for campaigns created in the last 180 days; older campaigns are scored as usual.
- Unclassified campaigns: none.
- Previous report: 2026-11-16-client-benchmark.csv. Diff joined on campaign_id for live rows and client + campaign name for CSV rows. Diff counts: 14 new, 3 still open, 0 fixed, 75 unchanged, 0 removed.
- Scope changes vs 16 Nov: none in the scored set; Christiania at Vail and Black Prong are new Advanced rows in the CRM with no account; Bison Ridge Retreat dropped (Basic in the CRM since 12 Nov). Advanced in the CRM but with no ad account mapping in PROJECT.md section 5, not scored: Treetop Hideaways (AM Kristal), Casey Key Resort (AM Nicole), Nine Pines Retreat (AM Nicole), Lundy Farm (AM Charlotte), Kimpton Mas Olas Resort (AM Charlotte), Christiania at Vail (AM Chiara), Black Prong (AM Nicole). Nine Pines Retreat's ad account 1671947624532383 (created 18 Nov, $0 spent) is waiting to be mapped.
- HG AI reports read from `HG AI Reports/` at the project root, dated since the previous run: none.
- Selah Place's campaigns are named with pipes in Meta ("SP | Willow | Sales | Top-5 Audiences | 11-2026"); shown here with slashes.
- Meeting notes: every "Meta Ads Strategy", "Meta Ads Sync" or "Meta Ads x HiddenGem AI Sync" calendar event since the previous run that has a "Notes by Gemini" attachment, read via Drive. Client names are matched with an alias list (Flow Home = FLOHOM, Tabber / Tipik Falls / Debug Falls = Tàberg Falls, Sailor Place = Selah Place, Stay on 38 = Stay On 30A, Ashwood River Cabins = Asheville River Cabins).
- This month line: direct booking revenue by booking date from the HiddenGem AI platform (pms_bookings, platform direct/OTA rules, tenants on a shared PMS account narrowed to their own properties), month to date at the run date, against the same day span of the previous month. Promo codes come from the booking payload: Guesty stores the code, Hostaway only a coupon id (counted, no names), Hospitable and Cloudbeds nothing. Pulled with pms_mtd.sql through the Supabase connector. Clients without a PMS connection on the platform show no figures.
- Monthly ROI context from `Monthly ROI data/` (July 2026, August 2026, September 2026, October 2026). Revenue there comes from the Client Performance Tracking sheet, not the pixel, so its ROAS is not comparable to the pixel ROAS above.
